import asyncio, json, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import x_collector as xc
from playwright.async_api import async_playwright
async def no_replies(*a, **k): return []
xc.fetch_x_replies = no_replies
JOBS = [
 ("akasaka", "赤坂麻里 (EGO OR トラジャ OR TravisJapan OR \"Travis Japan\")", "top", 30),
 ("akasaka_live", "赤坂麻里 振付", "live", 30),
 ("lounge_ego", "トラジャラウンジ EGO 振付", "live", 30),
]
async def main():
    async with async_playwright() as p:
        ctx = await xc.launch_browser_context(p)
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        for key, kw, tab, lim in JOBS:
            posts = []
            await page.goto(xc.build_x_search_url(kw, tab=tab), wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(4000)
            if tab == "live": await xc.switch_to_latest_tab(page)
            try:
                await xc.collect_x(page, ctx, lambda: len(posts) < lim, lambda m: None, posts.append)
            except Exception as e:
                print("err", e)
            (HERE / f"q3_{key}.json").write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
            print(key, len(posts), flush=True)
        await ctx.close()
asyncio.run(main())
