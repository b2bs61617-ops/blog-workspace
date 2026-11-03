"""X/Threadsでトラジャ・ストーンズ・スノーマンの直近100件を集める(返信取得なし)。"""
import asyncio, json, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import x_collector as xc
from playwright.async_api import async_playwright

async def no_replies(*a, **k):
    return []
xc.fetch_x_replies = no_replies
xc.fetch_threads_replies = no_replies

QW = "(なんで OR なぜ OR どこ OR 誰 OR いつ OR 知りたい OR 教えて OR わかる人 OR 気になる OR どういう OR 何の)"
JOBS = [
    ("travis", "x", f'(トラジャ OR "Travis Japan" OR トラビスジャパン) {QW} lang:ja -filter:retweets'),
    ("sixtones", "x", f'(SixTONES OR ストーンズ OR スト担) {QW} lang:ja -filter:retweets'),
    ("snowman", "x", f'("Snow Man" OR スノーマン OR すの担) {QW} lang:ja -filter:retweets'),
    ("travis", "threads", "Travis Japan"),
    ("sixtones", "threads", "SixTONES"),
    ("snowman", "threads", "Snow Man"),
]
LIMIT = 100

async def main():
    only = sys.argv[1:]
    async with async_playwright() as p:
        ctx = await xc.launch_browser_context(p)
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        for group, site, kw in JOBS:
            if only and site not in only:
                continue
            posts = []
            url = xc.build_threads_search_url(kw) if site == "threads" else xc.build_x_search_url(kw)
            print(f"\n■ {group}/{site}: {url}", flush=True)
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(4000)
            if site == "x":
                await xc.switch_to_latest_tab(page)
            cont = lambda: len(posts) < LIMIT
            try:
                fn = xc.collect_threads if site == "threads" else xc.collect_x
                await fn(page, ctx, cont, lambda m: None, posts.append)
            except Exception as e:
                print(f"  中断 {type(e).__name__}: {e}", flush=True)
            out = HERE / f"{group}_{site}.json"
            out.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  {len(posts)}件 -> {out.name}", flush=True)
            await page.wait_for_timeout(5000)
        await ctx.close()

asyncio.run(main())
