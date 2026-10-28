"""Threadsをキーワード検索し、自動スクロールで投稿(+上位投稿のリプライ)を集めて「？」付きの疑問を抜き出す
(chomoand-2.com=Snow Man / chomoand-0.com=SixTONES記事のネタ探し用。Xの tools/x-sokuho/sokuho_questions.py のThreads版)。

- ブラウザはThreads専用のログイン済みプロファイル(~/threads_profile)を使う。使用中なら ~/threads_profile_2 に自動で切り替える。初回はログイン完了まで待つ
- 出力: reports/threads_YYYYmmdd_HHMM.json と .md(疑問の多い順)
- 使い方: python threads_questions.py [--group sixtones] [--keywords "Snow Man" 目黒蓮 ...] [--scrolls 10] [--replies 3]
"""
import argparse
import asyncio
import json
import os
import random
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
TOOLS = ROOT.parent
sys.path.insert(0, str(TOOLS / "x-sokuho"))

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from playwright.async_api import async_playwright  # noqa: E402
from sokuho_questions import extract_questions  # noqa: E402
from x_collector import pick_profile  # noqa: E402

REPORTS_DIR = ROOT / "reports"
PROFILE_DIR = os.path.expanduser("~/threads_profile")
GROUP_KEYWORDS = {
    "snowman": ["Snow Man", "スノーマン", "岩本照", "深澤辰哉", "ラウール", "渡辺翔太",
                "向井康二", "阿部亮平", "目黒蓮", "宮舘涼太", "佐久間大介"],
    "sixtones": ["SixTONES", "ストーンズ", "ジェシー", "京本大我", "松村北斗", "髙地優吾",
                 "森本慎太郎", "田中樹"],
    "kitetsu": ["KEY TO LIT", "キテレツ", "岩﨑大昇", "井上瑞稀", "中村嶺亜", "猪狩蒼弥", "佐々木大光"],
}
DEFAULT_KEYWORDS = GROUP_KEYWORDS["snowman"]
POST_SEL = 'div[data-pressable-container="true"]'
# 投稿カードのinnerTextに混じる本文以外の行(投稿時刻・数字だけの行・UI文言)
NOISE_RE = re.compile(r"^(\d+(秒|分|時間|日|週間)|\d{1,4}/\d{1,2}(/\d{1,2})?|[\d,.万千]+|翻訳を見る|もっと見る|作成者|·|/)$")


def search_url(keyword, recent):
    return f"https://www.threads.com/search?q={quote(keyword)}&serp_type=default" + ("&filter=recent" if recent else "")


async def is_logged_in(page):
    return "login" not in page.url and await page.query_selector(POST_SEL) is not None


async def wait_for_login(page):
    await page.goto(search_url(DEFAULT_KEYWORDS[0], True), wait_until="domcontentloaded")
    await page.wait_for_timeout(5000)
    if await is_logged_in(page):
        return True
    print("Threadsにログインしてください(Instagramアカウントでログイン。完了まで最大5分待ちます)...")
    for _ in range(300):
        await page.wait_for_timeout(1000)
        if "threads.com" in page.url and "login" not in page.url:
            await page.goto(search_url(DEFAULT_KEYWORDS[0], True), wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            if await is_logged_in(page):
                return True
    return False


def post_body(raw):
    """投稿カードのinnerTextから、1行目(ユーザー名)と時刻・いいね数などのノイズ行を除いた本文を返す。"""
    lines = [ln.strip() for ln in raw.split("\n") if ln.strip()]
    return "\n".join(ln for ln in lines[1:] if not NOISE_RE.match(ln))


async def scrape_cards(page):
    return await page.evaluate(f"""() => [...document.querySelectorAll('{POST_SEL}')].map(e => {{
        const a = e.querySelector('a[href*="/post/"]');
        return {{url: a ? a.href.split('?')[0] : null, raw: e.innerText}};
    }})""")


async def collect_posts(page, url, scrolls):
    """検索結果やスレッドのページを自動スクロールし、投稿カードを上から順に集める。新着が止まったら打ち切る。"""
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(4000)
    posts, stall = {}, 0
    for _ in range(scrolls):
        before = len(posts)
        for c in await scrape_cards(page):
            text = post_body(c["raw"])
            if text:
                posts.setdefault(c["url"] or text, {"url": c["url"], "text": text})
        stall = stall + 1 if len(posts) == before else 0
        if stall >= 3:
            break
        await page.evaluate(f"window.scrollBy(0, {random.randint(800, 1300)})")
        await page.wait_for_timeout(random.randint(1500, 2500))
    return list(posts.values())


async def run(args):
    REPORTS_DIR.mkdir(exist_ok=True)
    results = []
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            pick_profile(PROFILE_DIR), headless=False, channel="chrome", slow_mo=50,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else await context.new_page()
        if not await wait_for_login(page):
            print("ログインが確認できなかったので終了します")
            await context.close()
            return

        for kw in args.keywords:
            print(f"■ {kw} を収集中...")
            posts = []
            for recent in (True, False):
                posts += await collect_posts(page, search_url(kw, recent), args.scrolls)
            posts = list({x["url"] or x["text"]: x for x in posts}.values())
            # 上位投稿の詳細ページ=1件目が元投稿、2件目以降がリプライ
            for post in [x for x in posts if x["url"]][: args.replies]:
                try:
                    thread = await collect_posts(page, post["url"], 4)
                    post["replies"] = [x["text"] for x in thread if x["url"] != post["url"]]
                except Exception:
                    post["replies"] = []
            questions, seen = [], set()
            for post in posts:
                for body in [post["text"]] + post.get("replies", []):
                    for q in extract_questions(body):
                        if q not in seen:
                            seen.add(q)
                            questions.append({"q": q, "url": post["url"]})
            results.append({"keyword": kw, "post_count": len(posts), "questions": questions})
            print(f"  投稿{len(posts)}件 / 疑問{len(questions)}件")
            await page.wait_for_timeout(random.randint(3000, 6000))

        await context.close()

    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    json_path = REPORTS_DIR / f"threads_{stamp}.json"
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [f"# Threadsの疑問 {stamp}\n"]
    for r in sorted(results, key=lambda x: -len(x["questions"])):
        md.append(f"## {r['keyword']}(投稿{r['post_count']}件／疑問{len(r['questions'])}件)")
        md += [f"- {q['q']}  ({q['url']})" for q in r["questions"][:40]]
        md.append("")
    json_path.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    print(f"保存完了: {json_path}")


def main():
    ap = argparse.ArgumentParser(description="Threads検索から「？」付きの疑問を集める")
    ap.add_argument("--group", choices=GROUP_KEYWORDS, default="snowman", help="キーワードの組(--keywords未指定時)")
    ap.add_argument("--keywords", nargs="+", default=None)
    ap.add_argument("--scrolls", type=int, default=10, help="検索結果1タブあたりの最大スクロール回数")
    ap.add_argument("--replies", type=int, default=3, help="リプライを読む上位投稿の数(キーワードごと)")
    args = ap.parse_args()
    if args.keywords is None:
        args.keywords = GROUP_KEYWORDS[args.group]
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
