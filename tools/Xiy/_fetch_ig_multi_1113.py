# -*- coding: utf-8 -*-
"""Open several IG posts with the Xiy profile; for each save caption/date text,
every slide screenshot, and all t51 image responses. Usage: python _fetch_ig_multi_1113.py OUTDIR URL..."""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright

PROFILE_DIR = str(Path.home() / "x_collector_profile")
OUT = Path(sys.argv[1]); URLS = sys.argv[2:]
OUT.mkdir(exist_ok=True)


async def main():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(PROFILE_DIR, headless=False, channel="chrome",
                                                         viewport={"width": 1400, "height": 1000},
                                                         args=["--disable-blink-features=AutomationControlled"])
        page = await ctx.new_page()
        cur = {"d": None, "n": 0}

        async def on_resp(r):
            if cur["d"] and "t51." in r.url and r.request.resource_type == "image":
                try:
                    b = await r.body()
                except Exception:
                    return
                if len(b) < 30000:
                    return
                cur["n"] += 1
                (cur["d"] / f"net_{cur['n']:02d}_{len(b)}.jpg").write_bytes(b)
        page.on("response", on_resp)
        for url in URLS:
            code = url.rstrip("/").split("/")[-1]
            d = OUT / code; d.mkdir(exist_ok=True)
            cur["d"], cur["n"] = d, 0
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            await page.keyboard.press("Escape")
            try:
                txt = await page.inner_text("main")
            except Exception:
                txt = ""
            times = await page.eval_on_selector_all("time", "els=>els.map(e=>e.getAttribute('datetime'))")
            (d / "text.txt").write_text(url + "\n" + str(times) + "\n\n" + txt, encoding="utf-8")
            await page.screenshot(path=str(d / "_shot_00.png"))
            for i in range(1, 20):
                btn = await page.query_selector("button[aria-label='次へ'], button[aria-label='Next']")
                if not btn:
                    break
                await btn.click()
                await page.wait_for_timeout(1800)
                await page.screenshot(path=str(d / f"_shot_{i:02d}.png"))
            print(code, "slides", i, "net", cur["n"], flush=True)
        await ctx.close()

asyncio.run(main())
