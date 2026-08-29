"""24時間マラソン現在地トラッカー: X ログイン(初回のみ手動)。

使い方:
    python tools/marathon-tracker/login.py

ブラウザ(Chrome)が開くので X にログインし、タイムラインが見える状態に
なったらこのターミナルで Enter を押す。ログイン状態は
    ~/marathon_tracker_profile
に保存され、以降 tracker.py がヘッドレスで再利用する。
"""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

PROFILE_DIR = str(Path.home() / "marathon_tracker_profile")


async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://x.com/login", wait_until="domcontentloaded")
        print("ブラウザで X にログインしてください。")
        print("ログインできてタイムラインが見えたら、このウィンドウで Enter を押してください。")
        input()
        await context.close()
        print(f"ログイン状態を保存しました: {PROFILE_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
