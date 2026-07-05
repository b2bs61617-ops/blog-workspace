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

    if new_by_target:
        REPORTS_DIR.mkdir(exist_ok=True)
        report_path = REPORTS_DIR / f"report_{today}_{int(time.time())}.json"
        report_path.write_text(
            json.dumps(new_by_target, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n新着情報あり → {report_path}")
    else:
        print("\n新着情報なし")


if __name__ == "__main__":
    asyncio.run(main())
