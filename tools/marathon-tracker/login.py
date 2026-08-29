"""24時間マラソン現在地トラッカー: X ログイン(初回のみ)。

使い方:
    python tools/marathon-tracker/login.py            # 自動検知(既定 最大4分待ち)
    python tools/marathon-tracker/login.py --wait 300 # 待ち時間を変える
    python tools/marathon-tracker/login.py --enter    # 昔どおり Enter で確定

ブラウザ(既定は playwright 同梱 chromium)が開くので X にログインする。
ホーム(タイムライン)が表示されたのを検知したら自動でプロファイルを保存して閉じる。
ログイン状態は ~/marathon_tracker_profile に保存され、以降 tracker.py が
ヘッドレスで再利用する。
"""
import argparse
import asyncio
import os
from pathlib import Path

from playwright.async_api import async_playwright

PROFILE_DIR = str(Path.home() / "marathon_tracker_profile")


async def _logged_in(page):
    try:
        if "/home" in page.url:
            return True
        el = await page.query_selector('[data-testid="SideNav_NewTweet_Button"], [data-testid="AppTabBar_Home_Link"]')
        return el is not None
    except Exception:
        return False


async def main(wait_seconds: int, use_enter: bool):
    async with async_playwright() as p:
        kw = {}
        ch = os.environ.get("MARATHON_PW_CHANNEL", "").strip()
        if ch:
            kw["channel"] = ch
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            **kw,
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://x.com/login", wait_until="domcontentloaded")
        print("ブラウザで X にログインしてください。")

        if use_enter:
            print("ログインできてタイムラインが見えたら、このウィンドウで Enter を押してください。")
            await asyncio.get_event_loop().run_in_executor(None, input)
        else:
            print(f"ログイン完了を自動で検知します(最大 {wait_seconds} 秒待ち)...")
            waited = 0
            while waited < wait_seconds:
                if await _logged_in(page):
                    print("ログインを検知しました。数秒待って保存します。")
                    await page.wait_for_timeout(4000)
                    break
                await page.wait_for_timeout(3000)
                waited += 3
            else:
                print("時間切れ。今の状態のまま保存します(未ログインなら再実行してください)。")

        await context.close()
        print(f"ログイン状態を保存しました: {PROFILE_DIR}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--wait", type=int, default=240, help="自動検知の最大待ち秒数")
    ap.add_argument("--enter", action="store_true", help="Enter キーで確定する旧方式")
    a = ap.parse_args()
    asyncio.run(main(a.wait, a.enter))
