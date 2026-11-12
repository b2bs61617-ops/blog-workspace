"""X/Threadsで「小麦とバターと復讐と6話のロケ地・衣装を集める(2026-11-12、返信取得なし)。"""
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

JOBS = [
    ("loc", "x", '(小麦とバターと復讐と OR 小麦バター OR 伊能先生) (ロケ地 OR 八鶴 OR 東金 OR シェラトン OR 都ホテル OR 病院) since:2026-11-10 -filter:retweets'),
    ("cos", "x", '(伊能先生 OR 小麦とバターと復讐と) (衣装 OR カーディガン OR シャツ OR ブランド OR どこの OR 指輪 OR エプロン) since:2026-11-10 -filter:retweets'),
    ("all", "x", '(小麦とバターと復讐と OR 伊能先生) 6話 since:2026-11-11 -filter:retweets'),
]
LIMIT = 80

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
