"""X/Threadsで「ちいかわクリニック」の疑問・反応を集める(2026-11-13、返信取得なし)。"""
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

QW = "(抽選 OR LINE OR 当選 OR 落選 OR 応募 OR 申し込み OR 繋がらない OR エラー OR 顔写真 OR らんど OR 第2弾 OR 第二弾)"
JOBS = [
    ("q", "x", f'ちいかわクリニック {QW} since:2026-11-13 lang:ja -filter:retweets'),
    ("all", "x", 'ちいかわクリニック since:2026-11-13 lang:ja -filter:retweets'),
    ("all", "threads", "ちいかわクリニック"),
]
LIMIT = 120

async def main():
    async with async_playwright() as p:
        ctx = await xc.launch_browser_context(p)
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        for group, site, kw in JOBS:
            out = HERE / f"{group}_{site}.json"
            if out.exists():
                continue
            posts = []
            url = xc.build_threads_search_url(kw) if site == "threads" else xc.build_x_search_url(kw)
            print(f"\n■ {group}/{site}: {url}", flush=True)
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                print(f"  goto失敗 {e}", flush=True); continue
            await page.wait_for_timeout(4000)
            if site == "x":
                await xc.switch_to_latest_tab(page)
            try:
                fn = xc.collect_threads if site == "threads" else xc.collect_x
                await fn(page, ctx, lambda: len(posts) < LIMIT, lambda m: None, posts.append)
            except Exception as e:
                print(f"  中断 {type(e).__name__}: {e}", flush=True)
            out.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  {len(posts)}件 -> {out.name}", flush=True)
            await page.wait_for_timeout(5000)
        await ctx.close()

asyncio.run(main())
