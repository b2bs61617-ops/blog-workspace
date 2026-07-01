# -*- coding: utf-8 -*-
import asyncio
import sys
from playwright.async_api import async_playwright
from datetime import datetime
import os

sys.stdout.reconfigure(encoding='utf-8')

TARGET_URL = "https://x.com/chanmina1014"
SCROLL_AMOUNT = 500
PAUSE_SECONDS = 1
MAX_SCROLLS = 30

OUTPUT_DIR = r"c:\Users\ti071\Desktop\ブログ作業場\x_capture"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ログイン情報を保存するフォルダ（次回以降は自動ログイン）
SESSION_DIR = r"c:\Users\ti071\Desktop\ブログ作業場\x_session"


def print_table(scroll_num, items):
    print(f"\n{'='*80}")
    print(f"  スクロール #{scroll_num}  ({datetime.now().strftime('%H:%M:%S')})")
    print(f"{'='*80}")
    if not items:
        print("  （投稿が見つかりませんでした）")
        return
    print(f"  {'#':<4} {'投稿テキスト（先頭60文字）':<62} {'画像'}")
    print(f"  {'-'*4} {'-'*62} {'-'*6}")
    for i, item in enumerate(items, 1):
        text = (item["text"] or "（テキストなし）").replace("\n", " ")
        text = text[:60] + "…" if len(text) > 60 else text
        img_count = len(item["images"])
        print(f"  {i:<4} {text:<62} {img_count}枚")
        for url in item["images"]:
            print(f"       🖼  {url}")


async def extract_posts(page):
    return await page.evaluate("""
        () => {
            const results = [];
            const tweetTexts = document.querySelectorAll('[data-testid="tweetText"]');
            tweetTexts.forEach(el => {
                const article = el.closest('article') || el.closest('[data-testid="cellInnerDiv"]');
                const text = el.innerText || '';
                const imgs = article
                    ? Array.from(article.querySelectorAll('img[src*="pbs.twimg.com"]')).map(img => img.src)
                    : [];
                results.push({ text, images: imgs });
            });
            if (results.length === 0) {
                const imgs = document.querySelectorAll('img[src*="pbs.twimg.com/media"]');
                imgs.forEach(img => {
                    results.push({ text: '（テキストなし）', images: [img.src] });
                });
            }
            return results;
        }
    """)


async def main():
    async with async_playwright() as p:
        # セッション保存フォルダがあれば自動ログイン、なければ手動ログイン
        already_logged_in = os.path.exists(SESSION_DIR) and os.listdir(SESSION_DIR)

        print("ブラウザ起動中…")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            slow_mo=50,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            ignore_default_args=["--enable-automation"],
        )
        page = context.pages[0] if context.pages else await context.new_page()

        if not already_logged_in:
            # 初回：ログインしてもらう
            print("\n" + "="*60)
            print("  【初回のみ】Xにログインしてください！")
            print("  ログインが完了したらEnterキーを押してください")
            print("="*60 + "\n")
            await page.goto("https://x.com/login", wait_until="domcontentloaded")
            input(">>> ログイン完了後にEnterを押してください: ")
            print("ログイン情報を保存しました（次回から自動ログイン）")
        else:
            print("保存済みセッションで自動ログイン！")

        print(f"\nターゲットページへ移動: {TARGET_URL}")
        await page.goto(TARGET_URL, wait_until="domcontentloaded")
        await asyncio.sleep(4)

        print("\nスクロールキャプチャ開始！（Ctrl+C で終了）")
        print(f"設定: スクロール量={SCROLL_AMOUNT}px / 静止={PAUSE_SECONDS}秒 / 最大{MAX_SCROLLS}回\n")

        for scroll_num in range(1, MAX_SCROLLS + 1):
            items = await extract_posts(page)
            print_table(scroll_num, items)

            shot_path = os.path.join(OUTPUT_DIR, f"scroll_{scroll_num:03d}.png")
            await page.screenshot(path=shot_path)

            await asyncio.sleep(PAUSE_SECONDS)
            await page.mouse.wheel(0, SCROLL_AMOUNT)
            await asyncio.sleep(0.5)

        print("\n完了！スクリーンショットの保存先:")
        print(OUTPUT_DIR)
        await context.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n手動停止しました！")
