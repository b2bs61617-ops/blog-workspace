import asyncio
import json
import re
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright

PROFILE_DIR = str(Path.home() / "koikeyz_monitor_profile")
ROOT = Path(__file__).parent
STATE_FILE = ROOT / "monitor_state.json"
REPORTS_DIR = ROOT / "monitor_reports"
CONFIG_FILE = ROOT / "monitor_config.json"

# KO1KEYZ 正式デビューメンバー12人 + グループ全体
TARGETS = {
    "加藤大樹": "加藤大樹 OR K.DAIKI KO1KEYZ",
    "矢田佳暉": "矢田佳暉 OR YOSHIKI KO1KEYZ",
    "パク・シヨン": "パク・シヨン OR SIYOUNG KO1KEYZ",
    "オ・シンヘン": "オ・シンヘン OR SHINHAENG KO1KEYZ",
    "後藤結": "後藤結 OR YUKI KO1KEYZ",
    "柳谷伊冴": "柳谷伊冴 OR ISSA KO1KEYZ",
    "小野慶人": "小野慶人 OR KEITO KO1KEYZ",
    "安部結蘭": "安部結蘭 OR YURA KO1KEYZ",
    "飯塚亮賀": "飯塚亮賀 OR RYOGA KO1KEYZ",
    "杉山竜司": "杉山竜司 OR RYUJI KO1KEYZ",
    "照井康祐": "照井康祐 OR KOSUKE KO1KEYZ",
    "濱田永遠": "濱田永遠 OR TOWA KO1KEYZ",
    "KO1KEYZ(グループ全体)": "KO1KEYZ OR コイキーズ",
}


# マツが読むレポートに含めない定型ノイズ投稿(トレカ交換・診断コピペ・同行募集など)
NOISE_PATTERNS = [
    r"トレカ",
    r"譲.{0,30}求|求.{0,30}譲",
    r"好き顔No\.?1",
    r"lapone-lanking",
    r"同行(させて|募集|求め|探)",
    r"交換希望|買取希望|お気軽にお声(掛け|がけ)",
    r"郵送希望|郵送or|郵送のみ",
    r"連番|同担様",
    r"#PR\b|tag=[\w-]+-22",  # Amazonアフィリエイトの広告コピペ投稿
]
NOISE_RE = re.compile("|".join(NOISE_PATTERNS))


def is_noise(text: str) -> bool:
    return bool(NOISE_RE.search(text))


def normalize_for_dedup(text: str) -> str:
    # URL・空白・タグ付き引用元アカウント名の揺れを無視して、同一内容のコピペ投稿をまとめる
    t = re.sub(r"https?://\S+", "", text)
    t = re.sub(r"\s+", "", t)
    return t


def dedupe_posts(posts):
    # 同じ告知文が複数アカウントからコピペ投稿されるケースをまとめ、代表1件+件数にする
    groups = {}
    order = []
    for p in posts:
        key = normalize_for_dedup(p["text"])
        if key not in groups:
            groups[key] = {**p, "duplicate_count": 1}
            order.append(key)
        else:
            groups[key]["duplicate_count"] += 1
    return [groups[k] for k in order]


def load_gemini_api_key():
    if not CONFIG_FILE.exists():
        return None
    try:
        config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return config.get("gemini_api_key") or None
    except Exception:
        return None


def summarize_with_gemini(new_by_target, api_key):
    """Geminiで「記事に使えそうな情報」だけ抽出した要約を作る。失敗したらNoneを返す(呼び出し側で生データにフォールバック)。"""
    from google import genai

    lines = []
    for name, posts in new_by_target.items():
        lines.append(f"【{name}】")
        for p in posts:
            dup = f"(同文投稿{p['duplicate_count']}件)" if p.get("duplicate_count", 1) > 1 else ""
            lines.append(f"- {p['text']}{dup}")
    posts_text = "\n".join(lines)

    prompt = f"""以下はKO1KEYZメンバーに関するXの新着投稿一覧です。
コイキーズブログの既存記事を更新するために「記事に反映する価値がある新情報」だけを抽出してください。

【抽出してほしい情報の例】
- 公式発表(デビュー・ライブ・ファンミ・グッズ・出演番組などの日程・詳細)
- メンバーの経歴・エピソードに関わる新事実
- ニュースサイトの記事や公式アカウントの投稿内容

【除外してよいもの】
- ファンの感想・応援メッセージ・「好き」「会いたい」等の感情表現のみの投稿
- 抽選・当落の個人的な報告(具体的な公演日程が伴わないもの)
- その他、記事に書く価値が無いと判断されるもの

該当する情報が無ければメンバー名ごとに「特筆すべき情報なし」と書いてください。
簡潔に日本語で、メンバー名ごとに箇条書きでまとめてください。

【投稿一覧】
{posts_text}"""

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text.strip()


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


async def switch_to_latest_tab(page):
    try:
        tab = page.get_by_role("tab", name="最新")
        if await tab.count():
            await tab.first.click()
            await page.wait_for_timeout(1500)
    except Exception:
        pass


async def collect_search(page, query, max_scroll=6):
    url = f"https://x.com/search?q={urllib.parse.quote(query)}&src=typed_query&f=live"
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(3000)
    await switch_to_latest_tab(page)

    posts = []
    seen = set()
    for _ in range(max_scroll):
        articles = await page.query_selector_all('article[data-testid="tweet"]')
        for article in articles:
            try:
                status_link = await article.query_selector('a[href*="/status/"]')
                if not status_link:
                    continue
                href = await status_link.get_attribute("href")
                m = re.search(r"/status/(\d+)", href or "")
                if not m:
                    continue
                tweet_id = m.group(1)
                if tweet_id in seen:
                    continue
                seen.add(tweet_id)

                text_el = await article.query_selector('div[data-testid="tweetText"]')
                text = (await text_el.inner_text()).strip() if text_el else ""

                date_str = ""
                time_el = await article.query_selector("time")
                if time_el:
                    date_str = (await time_el.get_attribute("datetime")) or ""

                author_el = await article.query_selector('div[data-testid="User-Name"]')
                author = (await author_el.inner_text()).strip().replace("\n", " ") if author_el else ""

                posts.append({
                    "id": tweet_id,
                    "date": date_str,
                    "author": author,
                    "text": text,
                    "url": f"https://x.com/i/status/{tweet_id}",
                })
            except Exception:
                continue
        await page.evaluate("window.scrollBy(0, 1200)")
        await page.wait_for_timeout(800)
    return posts


async def main():
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    new_by_target = {}

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR, headless=False, channel="chrome", slow_mo=30,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else await context.new_page()

        for name, query in TARGETS.items():
            print(f"[{name}] 検索中: {query}")
            seen_ids = set(state.get(name, []))
            try:
                posts = await collect_search(page, query)
            except Exception as e:
                print(f"  失敗: {e}")
                continue

            new_posts = [p for p in posts if p["id"] not in seen_ids]
            useful_posts = [p for p in new_posts if not is_noise(p["text"])]
            noise_count = len(new_posts) - len(useful_posts)
            deduped_posts = dedupe_posts(useful_posts)
            dup_count = len(useful_posts) - len(deduped_posts)
            if deduped_posts:
                new_by_target[name] = deduped_posts
                print(f"  新着 {len(new_posts)}件(ノイズ除外{noise_count}件・重複統合{dup_count}件 → 採用{len(deduped_posts)}件)")
            else:
                print(f"  新着なし(ノイズ{noise_count}件・重複{dup_count}件を除外)")

            all_ids = seen_ids | {p["id"] for p in posts}
            # 肥大化を防ぐため直近500件だけ保持
            state[name] = list(all_ids)[-500:]

        await context.close()

    save_state(state)

    if not new_by_target:
        print("\n新着情報なし")
        return

    REPORTS_DIR.mkdir(exist_ok=True)
    stamp = f"{today}_{int(time.time())}"
    report_path = REPORTS_DIR / f"report_{stamp}.json"
    report_path.write_text(
        json.dumps(new_by_target, ensure_ascii=False, indent=2), encoding="utf-8")

    api_key = load_gemini_api_key()
    summary = None
    if api_key:
        try:
            summary = summarize_with_gemini(new_by_target, api_key)
        except Exception as e:
            print(f"Gemini要約に失敗したのでスキップ(生データのみ出力): {type(e).__name__}: {e}")

    if summary:
        summary_path = REPORTS_DIR / f"report_{stamp}.summary.txt"
        summary_path.write_text(summary, encoding="utf-8")
        print(f"\n新着情報あり → {summary_path} (AI要約あり、生データ: {report_path.name})")
    else:
        print(f"\n新着情報あり → {report_path} (AI要約なし、生データのみ)")


if __name__ == "__main__":
    asyncio.run(main())
