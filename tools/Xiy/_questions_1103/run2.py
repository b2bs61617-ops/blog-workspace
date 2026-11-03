"""キーワード別にXの話題/最新を集める(返信なし)。"""
import asyncio, json, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import x_collector as xc
from playwright.async_api import async_playwright
async def no_replies(*a, **k): return []
xc.fetch_x_replies = no_replies
JOBS = [
 ("marching", "駒大苫小牧 Snow Man", "top", 40),
 ("marching_live", "(マーチング OR 吹奏楽) (スノ OR SnowMan OR \"Snow Man\") 高校 -filter:retweets", "live", 60),
 ("stage", "ALL SUITE (セット OR 演出 OR 気球 OR フロート OR 噴水 OR 水) スノ -filter:retweets", "top", 60),
 ("enshutsu", "ALL SUITE 演出 (ラウール OR 岩本 OR 深澤 OR 総合演出) -filter:retweets", "top", 40),
 ("badreq", "(\"Bad Request\" OR badrequest OR \"bad request\") (ファミクラ OR FC限定 OR 大晦日 OR ファンクラブ)", "live", 40),
 ("nagai", "長居 SixTONES (持ち物 OR 雨 OR 厚底 OR 寒さ OR カッパ OR ポンチョ OR 傘) -filter:retweets", "live", 60),
 ("nagai_resale", "SixTONES 長居 リセール -filter:retweets", "live", 40),
 ("tj_apply", "トラジャ (1枚 OR 2枚) (昼夜 OR 同日 OR 2公演 OR 複数公演) 申し込み -filter:retweets", "live", 40),
 ("ego_choreo", "EGO 振付 (トラジャ OR TravisJapan OR \"Travis Japan\") -filter:retweets", "top", 40),
 ("fns_snow", "FNS歌謡祭 Snow Man (何歌う OR 歌唱曲 OR 9人) -filter:retweets", "top", 30),
]
async def main():
    only = sys.argv[1:]
    async with async_playwright() as p:
        ctx = await xc.launch_browser_context(p)
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        for key, kw, tab, lim in JOBS:
            if only and key not in only: continue
            posts = []
            url = xc.build_x_search_url(kw, tab=tab)
            print(f"■ {key}", flush=True)
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(4000)
            if tab == "live": await xc.switch_to_latest_tab(page)
            try:
                await xc.collect_x(page, ctx, lambda: len(posts) < lim, lambda m: None, posts.append)
            except Exception as e:
                print(f"  中断 {e}", flush=True)
            (HERE / f"q2_{key}.json").write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  {len(posts)}件", flush=True)
            await page.wait_for_timeout(4000)
        await ctx.close()
asyncio.run(main())
