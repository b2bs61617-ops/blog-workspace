"""KO1KEYZの韓国語投稿でどのハッシュタグが使われているかをXで調べるスクリプト(2026-10-18作成)。
x_collector_profile(ログイン済みのブラウザ)でメンバーごとに韓国語で検索し、タグの出現数を数える。
2026-10-18の結果はdocs/research/ko1keyz-kr-x-hashtags-2026-10-18.jsonに保存し、
publishスキルの「KO1KEYZの韓国語の投稿」のタグ表に反映した。
"""
import asyncio, json, re, sys, urllib.parse
from collections import Counter
from pathlib import Path
from playwright.async_api import async_playwright

PROFILE = str(Path.home() / "x_collector_profile")
OUT = Path(__file__).parent / "kr_tag_result.json"

QUERIES = {
    "GROUP": ["KO1KEYZ lang:ko", "코이키즈", "#코이키즈"],
    "DAIKI": ["다이키 KO1KEYZ", "카토 다이키"],
    "YOSHIKI": ["요시키 KO1KEYZ", "야다 요시키"],
    "SIYOUNG": ["시영 KO1KEYZ", "박시영 KO1KEYZ"],
    "SHINHAENG": ["신행 KO1KEYZ", "오신행"],
    "YUKI": ["유키 KO1KEYZ", "고토 유이", "고토 유키"],
    "ISSA": ["잇사 KO1KEYZ", "야나기야 잇사"],
    "KEITO": ["케이토 KO1KEYZ", "오노 케이토"],
    "YURA": ["유라 KO1KEYZ", "아베 유라"],
    "RYOGA": ["료가 KO1KEYZ", "이이즈카 료가"],
    "RYUJI": ["류지 KO1KEYZ", "스기야마 류지"],
    "KOSUKE": ["코스케 KO1KEYZ", "테루이 코스케"],
    "TOWA": ["토와 KO1KEYZ", "하마다 토와"],
}
TAG_RE = re.compile(r"#[^\s#]+")


async def search(page, q, scrolls=4):
    url = f"https://x.com/search?q={urllib.parse.quote(q)}&src=typed_query&f=live"
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(3500)
    texts, seen = [], set()
    for _ in range(scrolls):
        for el in await page.query_selector_all('div[data-testid="tweetText"]'):
            try:
                t = (await el.inner_text()).strip()
            except Exception:
                continue
            if t not in seen:
                seen.add(t)
                texts.append(t)
        await page.evaluate("window.scrollBy(0, 1500)")
        await page.wait_for_timeout(900)
    return texts


async def main():
    result = {}
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            PROFILE, headless=False, channel="chrome",
            args=["--disable-blink-features=AutomationControlled"])
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        await page.goto("https://x.com/home", wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)
        if "login" in page.url or "flow" in page.url:
            print("NOT_LOGGED_IN", page.url)
            await ctx.close()
            return
        for key, qs in QUERIES.items():
            tags, n, samples = Counter(), 0, []
            for q in qs:
                try:
                    texts = await search(page, q)
                except Exception as e:
                    print(key, q, "ERR", e)
                    continue
                n += len(texts)
                for t in texts:
                    tags.update(TAG_RE.findall(t))
                samples += texts[:3]
                print(key, q, len(texts))
            result[key] = {"posts": n, "tags": tags.most_common(25),
                           "samples": [s[:200] for s in samples[:6]]}
        await ctx.close()
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print("DONE")


asyncio.run(main())
