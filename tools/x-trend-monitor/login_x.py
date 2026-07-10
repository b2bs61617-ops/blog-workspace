"""X-Trend-Monitor用のXログイン(PCごとに初回1回だけ手動実行する)。
koikeyz-monitorとはプロファイルを分けてある(30分おき実行と毎朝7時実行が同じプロファイルを
同時に掴むとブラウザのプロファイルロックで衝突するため)。
"""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

PROFILE_DIR = str(Path.home() / "x_trend_monitor_profile")


async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR, headless=False, channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://x.com/login", wait_until="domcontentloaded")
        print("ブラウザでXにログインしてください。ログインできたらこのウィンドウでEnterキーを押してください。")
        input()
        await context.close()
        print("ログイン状態を保存しました。")


if __name__ == "__main__":
    asyncio.run(main())
