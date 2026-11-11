"""話題ごとの深掘り収集(X、返信なし)。usage: python3 run2.py [key ...]"""
import asyncio, json, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import x_collector as xc
from playwright.async_api import async_playwright
async def no_replies(*a, **k): return []
xc.fetch_x_replies = no_replies
JOBS = {
 "kt_covers": ('("KEY TO LIT" OR キテレツ) 表紙 lang:ja -filter:retweets', "top"),
 "kt_mste": ('("KEY TO LIT" OR キテレツ) (Mステ OR 衣装) (腰布 OR チャイナ OR 衣装) lang:ja -filter:retweets', "top"),
 "kt_daiko": ('(佐々木大光 OR 大光くん) (膝 OR 怪我 OR 言わせ) lang:ja -filter:retweets', "top"),
 "kt_penny": ('(ペニーレイン OR 那須) (キテレツ OR "KEY TO LIT" OR 大光) lang:ja -filter:retweets', "top"),
 "st_hokuto_curry": ('(北斗 OR 松村北斗) (カレー OR スパイスカレー) (adidas OR アディダス OR 服 OR 衣装 OR ジャージ) lang:ja -filter:retweets', "top"),
 "st_kyomo_yt": ('(京本大我 OR きょも) (YouTube OR ストチューブ OR 回) (おすすめ OR 好き OR 神回) lang:ja -filter:retweets', "top"),
 "st_nissan": ('(SixTONES OR スト担) 日産 (服装 OR 寒さ OR 防寒 OR 天気 OR 持ち物) lang:ja -filter:retweets', "top"),
 "st_seat": ('(SixTONES OR "Snow Man" OR スト担 OR すの担) (座席 OR 席) 当日 (わからない OR 分からない OR 表示) lang:ja -filter:retweets', "top"),
 "st_kochi_imouto": ('(髙地 OR 高地 OR こーち) 妹 運転 lang:ja -filter:retweets', "top"),
 "st_gosuto": ('(GOスト OR #GOスト) (座椅子 OR 穴) lang:ja -filter:retweets', "top"),
 "sm_bemine": ('("Be mine" OR ビーマイン) ("Snow Man" OR スノ OR すの) lang:ja -filter:retweets', "top"),
 "sm_drive": ('(すのちゅーぶ OR "Snow Man") (横浜 OR ドライブ) (コーヒー OR カフェ OR 新横浜 OR ルート) lang:ja -filter:retweets', "top"),
 "sm_allsuite": ('("ALL SUITE" OR オールスイート OR ALLSUITE) (12/13 OR 1/2 OR 未発表) lang:ja -filter:retweets', "top"),
 "sm_stagehearts": ('(ステヘ OR "Stage Hearts" OR ステージハーツ) (コラボ OR チャンネル) lang:ja -filter:retweets', "top"),
 "sm_anan": ('(宮舘涼太 OR 舘様) anan (暴君 OR 表紙) lang:ja -filter:retweets', "top"),
}
LIMIT = 60
async def main():
    keys = sys.argv[1:] or list(JOBS)
    async with async_playwright() as p:
        ctx = await xc.launch_browser_context(p)
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        for k in keys:
            out = HERE / f"q_{k}.json"
            if out.exists(): continue
            kw, tab = JOBS[k]; posts = []
            url = xc.build_x_search_url(kw, tab)
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                await page.wait_for_timeout(4000)
                await xc.collect_x(page, ctx, lambda: len(posts) < LIMIT, lambda m: None, posts.append)
            except Exception as e:
                print(f"{k} 中断 {type(e).__name__}", flush=True)
            out.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"{k}: {len(posts)}件", flush=True)
            await page.wait_for_timeout(5000)
        await ctx.close()
asyncio.run(main())
