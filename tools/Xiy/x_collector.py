import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import asyncio
import argparse
import sys
import time
import json
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
import requests
from io import BytesIO
import re

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

try:
    from PIL import Image, ImageTk
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_OK = True
except ImportError:
    PLAYWRIGHT_OK = False

try:
    from playwright_stealth import Stealth
    STEALTH_OK = True
except ImportError:
    STEALTH_OK = False

try:
    from google import genai as google_genai
    GEMINI_OK = True
except ImportError:
    GEMINI_OK = False

try:
    import yt_dlp
    YTDLP_OK = True
except ImportError:
    YTDLP_OK = False

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YT_TRANSCRIPT_OK = True
except ImportError:
    YT_TRANSCRIPT_OK = False

try:
    from faster_whisper import WhisperModel
    WHISPER_OK = True
except ImportError:
    WHISPER_OK = False

try:
    import torch
    CUDA_OK = torch.cuda.is_available()
except ImportError:
    CUDA_OK = False

PROFILE_DIR = str(Path.home() / "x_collector_profile")
THUMB_SIZE = (150, 150)
CONFIG_FILE = str(Path(__file__).parent / "xiy_config.json")

# navigator.webdriver等の自動化フィンガープリントをX側に検知されて
# 「JavaScriptを使用できません」の偽ブロックページを返されることがあるため、
# 実際のシステムChromeが本来持つ言語設定に合わせてstealthパッチを当てる。
STEALTH_KWARGS = dict(navigator_languages_override=("ja-JP", "ja"))


async def launch_browser_context(p):
    context = await p.chromium.launch_persistent_context(
        PROFILE_DIR, headless=False, channel="chrome", slow_mo=50,
        args=["--disable-blink-features=AutomationControlled"],
    )
    if STEALTH_OK:
        await Stealth(**STEALTH_KWARGS).apply_stealth_async(context)
    return context


def x_full_size_url(url: str) -> str:
    url = re.sub(r"name=\w+", "name=orig", url)
    if "name=" not in url:
        url += ("&" if "?" in url else "?") + "name=orig"
    return url


def detect_platform(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    if "instagram.com" in url:
        return "instagram"
    if "x.com/explore" in url or "twitter.com/explore" in url:
        return "trending"
    return "x"


def build_x_search_url(keyword: str, tab: str = "live") -> str:
    url = f"https://x.com/search?q={quote(keyword)}"
    if tab == "live":
        url += "&f=live"
    return url


def load_api_key() -> str:
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f).get("gemini_api_key", "").strip()
    except Exception:
        return ""


# ── インスタのポップアップを自動で閉じる ──
async def dismiss_instagram_popups(page):
    for text in ["後で", "今はしない", "キャンセル"]:
        try:
            btn = page.get_by_role("button", name=text)
            if await btn.is_visible():
                await btn.click()
                await page.wait_for_timeout(500)
        except Exception:
            pass
    # 「登録する/ログイン」の未ログイン向け誘導ダイアログはEscapeで閉じる
    # (閉じるボタンは固定ヘッダーに遮られてクリックできないため)。
    # 投稿詳細ダイアログには「登録する」の文言がないので誤って閉じない。
    try:
        signup_dialog = page.locator('div[role="dialog"]', has_text="登録する")
        if await signup_dialog.count():
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(500)
    except Exception:
        pass


# ── 検索結果ページ: 「おすすめ」ではなく「最新」タブに切り替える ──
async def switch_to_latest_tab(page):
    try:
        tab = page.get_by_role("tab", name="最新")
        if await tab.count():
            await tab.first.click()
            await page.wait_for_timeout(1500)
    except Exception:
        pass


# ログイン画面は入力欄がモーダルで出るなどパターンが多くURLも変わらないことがあるため、
# 「未ログイン状態の見た目」を当てにいくのではなく「ログイン済みの時だけ出るナビ要素」の
# 有無で判定する(SideNav_AccountSwitcher_ButtonはX上のログイン済みシェルで安定して出る)。
async def is_x_logged_in(page) -> bool:
    try:
        el = await page.query_selector(
            '[data-testid="SideNav_AccountSwitcher_Button"], [data-testid="AppTabBar_Home_Link"]')
        return el is not None
    except Exception:
        return False


# ── Xのログイン待ち(未ログインのまま収集ループに入り、投稿0件のタイムアウトで
#    ブラウザごと閉じてログイン画面が消えてしまうのを防ぐ) ──
async def wait_for_x_login(page, should_continue, on_status):
    if await is_x_logged_in(page):
        return
    on_status("Xにログインしてください（ログイン完了まで待機します）...")
    for _ in range(180):
        if not should_continue():
            return
        await page.wait_for_timeout(1000)
        if await is_x_logged_in(page):
            break
    await page.wait_for_timeout(1500)


# ── トレンドページ収集 ──
async def collect_trending(page, should_continue, on_status, on_post):
    await wait_for_x_login(page, should_continue, on_status)
    if not should_continue():
        return

    on_status("トレンドページを解析中...")
    await page.wait_for_timeout(4000)

    debug_path = str(Path(__file__).parent / "trending_debug.html")
    try:
        html = await page.content()
        Path(debug_path).write_text(html, encoding="utf-8")
    except Exception:
        pass

    selectors = [
        '[data-testid="trend"]',
        'div[data-testid="trendingCell"]',
        'div[role="button"] span[dir="ltr"]',
    ]

    items = []
    for sel in selectors:
        items = await page.query_selector_all(sel)
        if items:
            on_status(f"セレクタ '{sel}' で {len(items)}件 検出")
            break

    if not items:
        on_status("トレンド要素が見つかりませんでした。trending_debug.htmlを確認してください。")
        return

    count = 0
    now_str = datetime.now().strftime("%Y/%m/%d %H:%M")
    for item in items:
        try:
            text = (await item.inner_text()).strip()
            if not text:
                continue
            post = {"platform": "x", "date": now_str, "text": text, "images": []}
            count += 1
            on_post(post)
        except Exception:
            continue

    on_status(f"トレンド取得完了: {count}件")


# ── X収集 ──
async def collect_x(page, should_continue, on_status, on_post):
    await wait_for_x_login(page, should_continue, on_status)
    if not should_continue():
        return

    seen = set()
    count = 0
    last_new_time = time.monotonic()

    while should_continue():
        articles = await page.query_selector_all('article[data-testid="tweet"]')
        prev_article_count = len(articles)

        for article in articles:
            try:
                text_el = await article.query_selector('[data-testid="tweetText"]')
                text = (await text_el.inner_text()).strip() if text_el else ""

                tweet_id = None
                tweet_url = None
                status_link = await article.query_selector('a[href*="/status/"]')
                if status_link:
                    href = await status_link.get_attribute("href")
                    m = re.search(r'/status/(\d+)', href or "")
                    if m:
                        tweet_id = m.group(1)
                        tweet_url = "https://x.com" + href if href and href.startswith("/") else href

                img_els = await article.query_selector_all('img[src*="pbs.twimg.com/media"]')
                img_urls = []
                for img_el in img_els:
                    src = await img_el.get_attribute("src")
                    if src:
                        img_urls.append(x_full_size_url(src))

                if not text and not img_urls:
                    continue
                dedup_key = tweet_id or text
                if dedup_key in seen:
                    continue
                seen.add(dedup_key)

                date_str = ""
                time_el = await article.query_selector("time")
                if time_el:
                    dt_attr = await time_el.get_attribute("datetime")
                    if dt_attr:
                        dt = datetime.fromisoformat(dt_attr.replace("Z", "+00:00"))
                        date_str = dt.strftime("%Y/%m/%d %H:%M")

                post = {"platform": "x", "date": date_str, "text": text, "images": img_urls, "url": tweet_url}
                count += 1
                on_post(post)
                last_new_time = time.monotonic()
            except Exception:
                continue

        await page.evaluate(f"window.scrollBy(0, {random.randint(650, 1150)})")
        try:
            await page.wait_for_function(
                f"document.querySelectorAll('article[data-testid=\\\"tweet\\\"]').length > {prev_article_count}",
                timeout=3000
            )
        except Exception:
            await page.wait_for_timeout(400)

        elapsed = int(time.monotonic() - last_new_time)
        if elapsed >= 10:
            break
        on_status(f"[X] 取得済み: {count}件 ／ 新着待機: {elapsed}秒 / 10秒")


# ── Instagram収集（グリッドを左上から順にクリック） ──
async def collect_instagram(page, should_continue, on_status, on_post):
    processed = set()
    count = 0

    if "instagram.com/accounts/" in page.url:
        on_status("Instagramにログインしてください（ログイン完了まで待機します）...")
        for _ in range(180):
            if not should_continue():
                return
            await page.wait_for_timeout(1000)
            if "instagram.com/accounts/" not in page.url:
                break
        await page.wait_for_timeout(1500)

    await dismiss_instagram_popups(page)
    last_new_time = time.monotonic()

    while should_continue():
        elapsed = int(time.monotonic() - last_new_time)
        if elapsed >= 10:
            break

        links = await page.query_selector_all('a[href*="/p/"]')
        new_links = []
        for link in links:
            href = await link.get_attribute("href")
            if href and href not in processed:
                new_links.append((href, link))

        if not new_links:
            on_status(f"[Instagram] 取得済み: {count}件 ／ 新着待機: {elapsed}秒 / 10秒")
            await page.evaluate(f"window.scrollBy(0, {random.randint(650, 1150)})")
            await page.wait_for_timeout(500)
            continue

        for href, link in new_links:
            if not should_continue():
                break
            processed.add(href)

            try:
                await dismiss_instagram_popups(page)
                await link.click()
                try:
                    await page.wait_for_selector('div[role="dialog"]', timeout=5000)
                except Exception:
                    await page.wait_for_timeout(800)
                await dismiss_instagram_popups(page)

                dialog = await page.query_selector('div[role="dialog"]')
                search_root = dialog if dialog else page

                img_urls = []
                for img in await search_root.query_selector_all("img"):
                    src = await img.get_attribute("src") or ""
                    if ("cdninstagram" in src or "fbcdn" in src) and not any(
                        x in src for x in ["s150x150", "s32x32", "s48x48", "s75x75", "e0/p"]
                    ):
                        img_urls.append(src)

                caption = ""
                caption_selectors = [
                    "ul > li:first-child span[dir='auto']",
                    "h1",
                    "article div[dir='auto'] > span",
                    "ul li:first-child div span",
                ]
                for sel in caption_selectors:
                    try:
                        el = await search_root.query_selector(sel)
                        if el:
                            t = (await el.inner_text()).strip()
                            if t and len(t) > 1:
                                caption = t
                                break
                    except Exception:
                        continue

                date_str = ""
                time_el = await search_root.query_selector("time")
                if time_el:
                    dt_attr = await time_el.get_attribute("datetime")
                    if dt_attr:
                        dt = datetime.fromisoformat(dt_attr.replace("Z", "+00:00"))
                        date_str = dt.strftime("%Y/%m/%d %H:%M")

                if img_urls:
                    post = {"platform": "instagram", "date": date_str,
                            "text": caption, "images": img_urls[:4]}
                    count += 1
                    on_post(post)
                    last_new_time = time.monotonic()
                    on_status(f"[Instagram] 取得済み: {count}件")

                await page.keyboard.press("Escape")
                await page.wait_for_timeout(300)

            except Exception:
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(200)
                continue

        await page.evaluate(f"window.scrollBy(0, {random.randint(650, 1150)})")
        await page.wait_for_timeout(400)


def build_ai_prompt(posts, youtube_posts, max_chars=30000):
    posts_text = ""
    i = 0
    for post in posts:
        i += 1
        platform = post.get("platform", "").upper()
        posts_text += f"[資料{i}] [{platform}] {post['date']}\n"
        if post["text"]:
            posts_text += post["text"] + "\n"
        posts_text += "\n"
    for yt in youtube_posts:
        i += 1
        posts_text += f"[資料{i}] [YouTube] {yt['title']}\n"
        posts_text += yt["transcript"] + "\n\n"

    truncated = len(posts_text) > max_chars
    if truncated:
        posts_text = posts_text[:max_chars]

    prompt = f"""以下はある人物のSNS投稿・YouTube動画の文字起こしです。これらに含まれるプライベート情報をカテゴリ別に整理して抽出してください。

【抽出するカテゴリ】
1. 学歴（通っていた学校・大学・卒業年など）
2. 誕生日・年齢
3. 出身地・居住地・地元
4. 家族構成（親・兄弟姉妹・子供など）
5. 交際相手・婚姻状況
6. 職業・所属・活動歴
7. その他のプライベート情報

【注意事項】
- 投稿・動画から読み取れる情報のみ記載し、推測の場合は「（推測）」と明記すること
- 各情報の根拠となる資料番号を【資料〇】の形式で記載すること
- 情報が見つからないカテゴリは「情報なし」と記載すること
- 日本語で回答すること

【SNS投稿・YouTube動画文字起こし一覧】
{posts_text}"""
    return prompt, truncated


def run_ai_analysis_sync(api_key, posts, youtube_posts, status_cb=None):
    status_cb = status_cb or (lambda msg: None)
    prompt, truncated = build_ai_prompt(posts, youtube_posts)
    client = google_genai.Client(api_key=api_key)

    result = None
    for attempt in range(3):
        try:
            if attempt > 0:
                wait_sec = attempt * 15
                status_cb(f"レート制限のため {wait_sec}秒待機してリトライ中...")
                time.sleep(wait_sec)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            result = response.text
            break
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                continue
            raise

    if truncated:
        result = f"※ 投稿が多すぎるため先頭30000文字のみ分析しました。\n\n" + result
    return result


def save_posts_to_dir(save_path, posts, youtube_posts, ai_text=None):
    save_path = Path(save_path)
    save_path.mkdir(parents=True, exist_ok=True)
    img_dir = save_path / "images"
    img_dir.mkdir(exist_ok=True)

    lines = []
    for i, post in enumerate(posts, 1):
        platform = post.get("platform", "").upper()
        lines.append(f"[{i}] [{platform}] {post['date']}")
        if post.get("url"):
            lines.append(f"  URL: {post['url']}")
        if post["text"]:
            lines.append(post["text"])
        for j, img_url in enumerate(post["images"], 1):
            try:
                resp = requests.get(img_url, timeout=15)
                img_file = img_dir / f"post_{i}_img_{j}.jpg"
                img_file.write_bytes(resp.content)
                lines.append(f"  画像: {img_file.name}")
            except Exception:
                pass
        lines.append("─" * 50)

    (save_path / "posts.txt").write_text("\n".join(lines), encoding="utf-8")

    if ai_text:
        (save_path / "ai_analysis.txt").write_text(ai_text, encoding="utf-8")

    if youtube_posts:
        yt_lines = []
        for yt in youtube_posts:
            yt_lines.append(f"[{yt['index']}] {yt['title']}")
            yt_lines.append(yt["url"])
            yt_lines.append(yt["transcript"])
            yt_lines.append("─" * 50)
        (save_path / "youtube_transcripts.txt").write_text(
            "\n".join(yt_lines), encoding="utf-8")

    return save_path


# ── 大画面ポップアップ ──
def show_fullscreen(root, url):
    popup = tk.Toplevel(root)
    popup.title("画像プレビュー")
    popup.configure(bg="black")
    popup.bind("<Escape>", lambda e: popup.destroy())
    popup.bind("<Button-1>", lambda e: popup.destroy())

    lbl = tk.Label(popup, text="読み込み中...", bg="black", fg="white",
                   font=("Arial", 14))
    lbl.pack(expand=True)

    def load():
        try:
            resp = requests.get(url, timeout=15)
            img = Image.open(BytesIO(resp.content))
            sw = root.winfo_screenwidth() - 60
            sh = root.winfo_screenheight() - 60
            img.thumbnail((sw, sh), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            popup.after(0, lambda: _show(photo))
        except Exception:
            popup.after(0, popup.destroy)

    def _show(photo):
        lbl.configure(image=photo, text="")
        lbl.image = photo
        popup.geometry(f"{photo.width()}x{photo.height()}")

    threading.Thread(target=load, daemon=True).start()


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self.inner = tk.Frame(self._canvas, bg="white")
        self.inner.bind("<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self._canvas.configure(yscrollcommand=scrollbar.set)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.bind("<MouseWheel>",
            lambda e: self._canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))


class PostCard(tk.Frame):
    def __init__(self, parent, index, post, on_image_click=None, **kwargs):
        super().__init__(parent, relief=tk.RIDGE, bd=1, bg="white", **kwargs)

        header = tk.Frame(self, bg="#f0f4f8", padx=8, pady=4)
        header.pack(fill=tk.X)
        platform_label = "X" if post.get("platform") == "x" else "Instagram"
        tk.Label(header,
                 text=f"#{index}  [{platform_label}]  {post['date']}",
                 fg="#333", bg="#f0f4f8", font=("Arial", 9, "bold")).pack(anchor=tk.W)

        body = tk.Frame(self, bg="white", padx=8, pady=6)
        body.pack(fill=tk.X)
        if post["text"]:
            tk.Label(body, text=post["text"],
                     bg="white", font=("Arial", 10),
                     wraplength=520, justify=tk.LEFT, anchor=tk.W).pack(anchor=tk.W)

        if post["images"] and PIL_OK:
            img_frame = tk.Frame(body, bg="white")
            img_frame.pack(anchor=tk.W, pady=(6, 0))
            for url in post["images"][:4]:
                try:
                    resp = requests.get(url, timeout=8)
                    img = Image.open(BytesIO(resp.content))
                    img.thumbnail(THUMB_SIZE, Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    lbl = tk.Label(img_frame, image=photo, bg="white",
                                   relief=tk.GROOVE, bd=1, cursor="hand2")
                    lbl.image = photo
                    if on_image_click:
                        lbl.bind("<Button-1>", lambda e, u=url: on_image_click(u))
                    lbl.pack(side=tk.LEFT, padx=3)
                except Exception:
                    pass
        elif post["images"] and not PIL_OK:
            tk.Label(body, text=f"画像 {len(post['images'])}枚（pip install Pillow が必要）",
                     fg="gray", bg="white", font=("Arial", 9)).pack(anchor=tk.W)


class CollectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Xiy")
        self.root.geometry("860x800")
        self.root.resizable(True, True)
        self.is_running = False
        self.collected_posts = []
        self.youtube_posts = []
        self.api_key_var = tk.StringVar()
        self.setup_ui()
        self.load_config()

        if not PLAYWRIGHT_OK:
            messagebox.showwarning("エラー",
                "pip install playwright\nplaywright install chromium")
        if not GEMINI_OK:
            messagebox.showwarning("Gemini未導入",
                "AI分析を使うには:\npip install google-genai")

    def _add_context_menu(self, entry):
        menu = tk.Menu(entry, tearoff=0)
        menu.add_command(label="切り取り", command=lambda: entry.event_generate("<<Cut>>"))
        menu.add_command(label="コピー", command=lambda: entry.event_generate("<<Copy>>"))
        menu.add_command(label="貼り付け", command=lambda: entry.event_generate("<<Paste>>"))
        menu.add_separator()
        menu.add_command(label="全て選択", command=lambda: entry.select_range(0, tk.END))
        entry.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    def setup_ui(self):
        # URL入力
        url_frame = tk.LabelFrame(self.root, text="対象URL（X / Instagram / YouTube）",
                                  padx=5, pady=5)
        url_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        self.url_entry = tk.Entry(url_frame, font=("Arial", 10))
        self.url_entry.pack(fill=tk.X, expand=True)
        self._add_context_menu(self.url_entry)

        # AI分析設定
        ai_frame = tk.LabelFrame(self.root, text="AI分析設定（Gemini Flash）",
                                 padx=5, pady=5)
        ai_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        tk.Label(ai_frame, text="Gemini APIキー:").grid(row=0, column=0, sticky=tk.W)
        api_key_entry = tk.Entry(ai_frame, textvariable=self.api_key_var,
                 font=("Arial", 10), width=55, show="*")
        api_key_entry.grid(row=0, column=1, padx=5, sticky=tk.W)
        self._add_context_menu(api_key_entry)
        tk.Button(ai_frame, text="保存", command=self.save_config,
                  width=5).grid(row=0, column=2, padx=3)

        # ボタン群
        bf = tk.Frame(self.root)
        bf.pack(fill=tk.X, padx=10, pady=5)
        self.start_btn = tk.Button(bf, text="▶ 収集開始", command=self.start_collection,
            bg="#1DA1F2", fg="white", font=("Arial", 11, "bold"), width=14)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = tk.Button(bf, text="■ 停止", command=self.stop_collection,
            bg="#E0245E", fg="white", font=("Arial", 11, "bold"), width=14, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.save_btn = tk.Button(bf, text="保存", command=self.save_results,
            font=("Arial", 11), width=10, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="クリア", command=self.clear_results,
            font=("Arial", 11), width=10).pack(side=tk.LEFT, padx=5)
        self.ai_btn = tk.Button(bf, text="再分析", command=self.analyze_with_ai,
            bg="#34A853", fg="white", font=("Arial", 11, "bold"), width=10, state=tk.DISABLED)
        self.ai_btn.pack(side=tk.LEFT, padx=5)

        # ステータスバー
        self.status_var = tk.StringVar(value="待機中...")
        tk.Label(self.root, textvariable=self.status_var, anchor=tk.W,
                 relief=tk.SUNKEN, bg="#f0f0f0", font=("Arial", 10)).pack(
                 fill=tk.X, padx=10, pady=(0, 2))

        # タブ
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        tab1 = tk.Frame(self.notebook)
        self.notebook.add(tab1, text="  収集した投稿  ")
        self.scroll_frame = ScrollableFrame(tab1)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)

        tab2 = tk.Frame(self.notebook)
        self.notebook.add(tab2, text="  AI分析結果  ")
        self.ai_result_text = tk.Text(tab2, font=("Arial", 10), wrap=tk.WORD,
                                      state=tk.DISABLED, padx=8, pady=8)
        ai_sb = ttk.Scrollbar(tab2, orient="vertical", command=self.ai_result_text.yview)
        self.ai_result_text.configure(yscrollcommand=ai_sb.set)
        self.ai_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ai_sb.pack(side=tk.RIGHT, fill=tk.Y)

        tab3 = tk.Frame(self.notebook)
        self.notebook.add(tab3, text="  YouTube文字起こし  ")
        self.yt_text = tk.Text(tab3, font=("Arial", 10), wrap=tk.WORD,
                               state=tk.DISABLED, padx=8, pady=8)
        yt_sb = ttk.Scrollbar(tab3, orient="vertical", command=self.yt_text.yview)
        self.yt_text.configure(yscrollcommand=yt_sb.set)
        self.yt_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yt_sb.pack(side=tk.RIGHT, fill=tk.Y)

    # ── 設定の保存・読み込み ──
    def load_config(self):
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                config = json.load(f)
                self.api_key_var.set(config.get("gemini_api_key", ""))
        except Exception:
            pass

    def save_config(self):
        config = {
            "gemini_api_key": self.api_key_var.get().strip(),
        }
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("保存完了", "設定を保存しました")
        except Exception as e:
            messagebox.showerror("保存エラー", str(e))

    def start_collection(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("URL未入力", "URLを入力してください。")
            return
        platform = detect_platform(url)

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.DISABLED)
        self.ai_btn.config(state=tk.DISABLED)
        self.update_status("起動中...")

        if platform == "youtube":
            if not YTDLP_OK or not YT_TRANSCRIPT_OK:
                missing = []
                if not YTDLP_OK:
                    missing.append("yt-dlp")
                if not YT_TRANSCRIPT_OK:
                    missing.append("youtube-transcript-api")
                messagebox.showerror("ライブラリ不足",
                    f"以下をインストールしてください:\npip install {' '.join(missing)}")
                self.is_running = False
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                return
            self.youtube_posts = []
            self.yt_text.config(state=tk.NORMAL)
            self.yt_text.delete("1.0", tk.END)
            self.yt_text.config(state=tk.DISABLED)
            self.notebook.select(2)
            threading.Thread(target=self._collect_youtube_sync, daemon=True).start()
        else:
            if not PLAYWRIGHT_OK:
                messagebox.showerror("エラー", "Playwrightをインストールしてください。")
                self.is_running = False
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                return
            self.collected_posts = []
            for w in self.scroll_frame.inner.winfo_children():
                w.destroy()
            threading.Thread(target=lambda: asyncio.run(self._collect()), daemon=True).start()

    def stop_collection(self):
        self.is_running = False
        self.update_status("停止中...")

    def clear_results(self):
        for w in self.scroll_frame.inner.winfo_children():
            w.destroy()
        self.collected_posts = []
        self.youtube_posts = []
        self.save_btn.config(state=tk.DISABLED)
        self.ai_btn.config(state=tk.DISABLED)
        self.ai_result_text.config(state=tk.NORMAL)
        self.ai_result_text.delete("1.0", tk.END)
        self.ai_result_text.config(state=tk.DISABLED)
        self.yt_text.config(state=tk.NORMAL)
        self.yt_text.delete("1.0", tk.END)
        self.yt_text.config(state=tk.DISABLED)
        self.update_status("待機中...")

    async def _collect(self):
        url = self.url_entry.get().strip()
        platform = detect_platform(url)
        try:
            async with async_playwright() as p:
                context = await launch_browser_context(p)
                page = context.pages[0] if context.pages else await context.new_page()
                self.update_status(f"[{platform.upper()}] ページを開いています...")
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(3000)

                if platform == "x" and "/search" in url:
                    await switch_to_latest_tab(page)

                should_continue = lambda: self.is_running
                if platform == "x":
                    await collect_x(page, should_continue, self.update_status, self._on_new_post)
                elif platform == "trending":
                    await collect_trending(page, should_continue, self.update_status, self._on_new_post)
                else:
                    await collect_instagram(page, should_continue, self.update_status, self._on_new_post)

                await context.close()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("エラー", str(e)))
        self._finish()

    def _on_new_post(self, post):
        self.collected_posts.append(post)
        self._add_card(len(self.collected_posts), post)

    # ── YouTube文字起こし ──
    def _extract_video_id(self, url):
        for pattern in [r'[?&]v=([a-zA-Z0-9_-]{11})',
                        r'youtu\.be/([a-zA-Z0-9_-]{11})',
                        r'/shorts/([a-zA-Z0-9_-]{11})']:
            m = re.search(pattern, url)
            if m:
                return m.group(1)
        return None

    def _collect_youtube_sync(self):
        url = self.url_entry.get().strip()
        try:
            video_id = self._extract_video_id(url)
            if video_id:
                self.update_status("動画情報を取得中...")
                try:
                    ydl_opts = {"quiet": True, "no_warnings": True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(
                            f"https://www.youtube.com/watch?v={video_id}", download=False)
                    title = info.get("title", video_id) if info else video_id
                except Exception:
                    title = video_id
                videos = [{"id": video_id, "title": title}]
            else:
                self.update_status("チャンネルの動画一覧を取得中...")
                videos = self._get_channel_videos(url)

            videos = [v for v in videos if v.get("id")]
            if not videos:
                self.root.after(0, lambda: messagebox.showwarning(
                    "動画なし", "動画が見つかりませんでした。\nURLを確認してください。"))
                self._finish_youtube(0)
                return

            total = len(videos)
            self.update_status(f"動画 {total}件 を発見。字幕を確認中...")

            idx_of = {v["id"]: i for i, v in enumerate(videos, 1)}
            emitted = set()

            def emit(video, transcript):
                vid_id = video["id"]
                if vid_id in emitted:
                    return
                emitted.add(vid_id)
                yt_post = {
                    "index": idx_of[vid_id],
                    "title": video.get("title", "(タイトル不明)"),
                    "id": vid_id,
                    "url": f"https://www.youtube.com/watch?v={vid_id}",
                    "transcript": transcript or "(字幕なし・取得不可)",
                }
                self.youtube_posts.append(yt_post)
                self._append_youtube_card(yt_post)

            # 字幕チェックはネットワーク待ちが主体なので複数動画をまとめて並列に確認する。
            # 字幕が見つかった動画は取れ次第すぐ表示する
            no_caption = []
            with ThreadPoolExecutor(max_workers=min(6, total)) as ex:
                futures = {
                    ex.submit(self._get_caption_only, v["id"], i, total, v.get("title", "")): v
                    for i, v in enumerate(videos, 1)
                }
                for fut in as_completed(futures):
                    video = futures[fut]
                    transcript = fut.result()
                    if transcript:
                        emit(video, transcript)
                    elif self.is_running:
                        no_caption.append(video)

            # 字幕が無かった動画だけWhisperに回す。DLと文字起こしを重ねて待ち時間を削る
            if no_caption and WHISPER_OK:
                self._whisper_pipeline(no_caption, emit)

            # 中断やWhisper未導入などで処理されなかった動画も欠かさず一覧に残す
            for video in videos:
                emit(video, None)

            # 表示は結果が来た順だが、保存ファイル用に動画本来の並びへ揃える
            self.youtube_posts.sort(key=lambda p: p["index"])

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("YouTubeエラー", str(e)))

        self._finish_youtube(len(self.youtube_posts))

    def _get_channel_videos(self, url):
        ydl_opts = {
            "extract_flat": "in_playlist",
            "quiet": True,
            "no_warnings": True,
            "ignoreerrors": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        if not info:
            return []
        entries = info.get("entries") or []
        return [
            {"id": e["id"], "title": e.get("title", "")}
            for e in entries if e and e.get("id")
        ]

    def _get_caption_only(self, video_id, idx=0, total=0, title=""):
        if not YT_TRANSCRIPT_OK:
            return None
        label = f"[{idx}/{total}] {title[:25]}"
        self.update_status(f"{label} | 字幕を確認中...")
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for lang in ["ja", "en"]:
                try:
                    data = transcript_list.find_transcript([lang]).fetch()
                    self.update_status(f"{label} | 字幕取得完了")
                    return "[字幕] " + " ".join(item["text"] for item in data)
                except Exception:
                    pass
            for t in transcript_list:
                try:
                    data = t.fetch()
                    self.update_status(f"{label} | 字幕取得完了")
                    return "[字幕] " + " ".join(item["text"] for item in data)
                except Exception:
                    pass
        except Exception:
            pass
        return None

    def _whisper_pipeline(self, videos, emit):
        total = len(videos)

        def label_of(video, idx):
            return f"[音声 {idx}/{total}] {video.get('title', '')[:25]}"

        dl_pool = ThreadPoolExecutor(max_workers=1)
        try:
            next_future = dl_pool.submit(self._download_audio, videos[0]["id"], label_of(videos[0], 1))
            for i, video in enumerate(videos):
                if not self.is_running:
                    break
                vid_id = video["id"]
                label = label_of(video, i + 1)

                # 今の動画をWhisperで処理する前に、次の動画の音声DLを裏で先行着手させておく
                if i + 1 < len(videos):
                    nxt = videos[i + 1]
                    prefetch = dl_pool.submit(self._download_audio, nxt["id"], label_of(nxt, i + 2))
                else:
                    prefetch = None

                try:
                    audio_file = next_future.result()
                    text = self._transcribe_audio_file(audio_file, label)
                    emit(video, "[音声] " + text)
                except Exception as e:
                    emit(video, f"(音声文字起こし失敗: {e})")
                finally:
                    self._cleanup_audio(vid_id)

                next_future = prefetch
        finally:
            dl_pool.shutdown(wait=False, cancel_futures=True)

    def _download_audio(self, video_id, label=""):
        import tempfile
        tmp_dir = Path(tempfile.gettempdir()) / "xi_audio"
        tmp_dir.mkdir(exist_ok=True)
        audio_base = tmp_dir / video_id

        last_err = None
        for attempt in range(3):
            try:
                if attempt > 0:
                    self.update_status(f"{label} | 音声DL リトライ {attempt}/2...")
                else:
                    self.update_status(f"{label} | 音声をダウンロード中...")
                ydl_opts = {
                    "format": "bestaudio[ext=m4a]/bestaudio",
                    "outtmpl": str(audio_base) + ".%(ext)s",
                    "quiet": True,
                    "no_warnings": True,
                    "socket_timeout": 60,
                    "retries": 5,
                    "fragment_retries": 5,
                    "http_chunk_size": 1048576,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
                last_err = None
                break
            except Exception as e:
                last_err = e
                time.sleep(5)

        if last_err:
            raise RuntimeError(f"音声DL失敗: {last_err}")

        audio_files = list(tmp_dir.glob(f"{video_id}.*"))
        if not audio_files:
            raise RuntimeError("音声ファイルの取得に失敗")
        return audio_files[0]

    def _transcribe_audio_file(self, audio_file, label=""):
        if not hasattr(self, "_whisper_model"):
            device = "cuda" if CUDA_OK else "cpu"
            compute_type = "float16" if CUDA_OK else "int8"
            self.update_status(f"{label} | Whisperモデル読み込み中（{device}・初回のみ時間がかかります）...")
            self._whisper_model = WhisperModel(
                "small", device=device, compute_type=compute_type,
                cpu_threads=os.cpu_count() or 4)

        self.update_status(f"{label} | Whisper 音声→テキスト変換中...")
        segments, _ = self._whisper_model.transcribe(
            str(audio_file), beam_size=5, vad_filter=True)
        text = " ".join(seg.text.strip() for seg in segments)
        self.update_status(f"{label} | 音声文字起こし完了")
        return text

    def _cleanup_audio(self, video_id):
        import tempfile
        tmp_dir = Path(tempfile.gettempdir()) / "xi_audio"
        for f in tmp_dir.glob(f"{video_id}.*"):
            try:
                f.unlink()
            except Exception:
                pass

    def _append_youtube_card(self, yt_post):
        def _do():
            self.yt_text.config(state=tk.NORMAL)
            self.yt_text.insert(tk.END,
                f"━━━ [{yt_post['index']}] {yt_post['title']}\n"
                f"{yt_post['url']}\n"
                f"{yt_post['transcript']}\n\n")
            self.yt_text.config(state=tk.DISABLED)
            self.yt_text.see(tk.END)
        self.root.after(0, _do)

    def _finish_youtube(self, count):
        def _done():
            import winsound
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            if count:
                self.save_btn.config(state=tk.NORMAL)
                self.ai_btn.config(state=tk.NORMAL)
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            # APIキーがあれば自動でAI分析、なければ通知して終了
            if count and self.api_key_var.get().strip():
                self.status_var.set(f"文字起こし完了 {count}件 → AI分析を開始します...")
                self.root.after(500, self.analyze_with_ai)
            else:
                self.status_var.set(f"文字起こし完了 {count}件")
                if count and not self.api_key_var.get().strip():
                    messagebox.showinfo("完了",
                        f"{count}件の動画を文字起こしました！\nGemini APIキーを入力すると自動でAI分析が始まります。")
                else:
                    messagebox.showinfo("完了", f"{count}件の動画を文字起こしました！")
        self.root.after(0, _done)

    def _add_card(self, index, post):
        self.root.after(0, lambda: PostCard(
            self.scroll_frame.inner, index, post,
            on_image_click=lambda u: show_fullscreen(self.root, u)
        ).pack(fill=tk.X, pady=3, padx=4))

    def update_status(self, msg):
        self.root.after(0, lambda: self.status_var.set(msg))

    def _finish(self):
        def _done():
            import winsound
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            count = len(self.collected_posts)
            if count:
                self.save_btn.config(state=tk.NORMAL)
                self.ai_btn.config(state=tk.NORMAL)
            self.status_var.set(f"収集完了 {count}件 → AI分析を開始します...")
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            # APIキーがあれば自動でAI分析、なければ通知して終了
            if count and self.api_key_var.get().strip():
                self.root.after(500, self.analyze_with_ai)
            else:
                if count and not self.api_key_var.get().strip():
                    messagebox.showinfo("取得完了",
                        f"{count}件取得しました。\nGemini APIキーを入力すると自動でAI分析が始まります。")
                else:
                    messagebox.showinfo("取得完了", f"{count}件の投稿を取得しました！")
        self.root.after(0, _done)

    # ── AI分析 ──
    def analyze_with_ai(self):
        if not GEMINI_OK:
            messagebox.showerror("Gemini未導入",
                "以下を実行してください:\npip install google-genai")
            return
        if not self.collected_posts and not self.youtube_posts:
            messagebox.showwarning("データなし", "先に投稿または動画を収集してください。")
            return
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("APIキー未入力", "Gemini APIキーを入力してください。")
            return

        self.ai_btn.config(state=tk.DISABLED)
        self.update_status("AI分析中...")
        threading.Thread(
            target=lambda: self._run_ai_analysis(api_key), daemon=True).start()

    def _run_ai_analysis(self, api_key):
        try:
            status_cb = lambda msg: self.root.after(0, lambda: self.update_status(msg))
            result = run_ai_analysis_sync(api_key, self.collected_posts, self.youtube_posts, status_cb)
            self.root.after(0, lambda: self._show_ai_results(result))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("AI分析エラー", str(e)))
        finally:
            self.root.after(0, lambda: self.ai_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.update_status(
                f"AI分析完了 / 収集済み: {len(self.collected_posts) + len(self.youtube_posts)}件"))

    def _show_ai_results(self, text):
        self.ai_result_text.config(state=tk.NORMAL)
        self.ai_result_text.delete("1.0", tk.END)
        self.ai_result_text.insert(tk.END, text)
        self.ai_result_text.config(state=tk.DISABLED)
        self.notebook.select(1)

    def save_results(self):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_dir = filedialog.askdirectory(title="保存フォルダを選択")
        if not save_dir:
            return
        save_path = Path(save_dir) / f"posts_{now}"
        ai_text = self.ai_result_text.get("1.0", tk.END).strip()
        save_path = save_posts_to_dir(save_path, self.collected_posts, self.youtube_posts, ai_text or None)
        messagebox.showinfo("保存完了", f"{save_path} に保存しました")


# ── CLIモード(GUIを介さずキーワード/URL指定で自動収集) ──
async def run_cli(args):
    if not PLAYWRIGHT_OK:
        print("Playwrightが未インストールです: pip install playwright / playwright install chromium")
        return

    url = args.url if args.url else build_x_search_url(args.keyword, tab=args.tab)
    platform = detect_platform(url)

    posts = []

    def on_status(msg):
        print(f"\r{msg}".ljust(80), end="", flush=True)

    def on_post(post):
        posts.append(post)
        preview = post["text"][:40].replace("\n", " ")
        print(f"\n[{len(posts)}] {post['date']} {preview}")

    async with async_playwright() as p:
        context = await launch_browser_context(p)
        page = context.pages[0] if context.pages else await context.new_page()
        print(f"[{platform.upper()}] ページを開いています... {url}")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)

        if platform == "x" and "/search" in url:
            await switch_to_latest_tab(page)

        should_continue = lambda: True
        if platform == "x":
            await collect_x(page, should_continue, on_status, on_post)
        elif platform == "trending":
            await collect_trending(page, should_continue, on_status, on_post)
        else:
            await collect_instagram(page, should_continue, on_status, on_post)

        await context.close()

    print(f"\n収集完了: {len(posts)}件")

    ai_text = None
    if posts and not args.no_ai:
        api_key = load_api_key()
        if api_key and GEMINI_OK:
            print("AI分析中...")
            try:
                ai_text = run_ai_analysis_sync(api_key, posts, [], status_cb=print)
            except Exception as e:
                print(f"AI分析エラー: {e}")
        else:
            print("Gemini APIキー未設定のためAI分析はスキップ")

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    label = re.sub(r'[\\/:*?"<>|]', "_", args.keyword or "url")[:30]
    out_dir = Path(args.out) if args.out else Path(__file__).parent / f"posts_{now}_{label}"
    save_path = save_posts_to_dir(out_dir, posts, [], ai_text)
    print(f"保存完了: {save_path}")


def main_cli():
    parser = argparse.ArgumentParser(description="Xiy CLI - GUIなしでX/Instagramを収集する")
    parser.add_argument("--keyword", help="Xでこのキーワードを検索して収集する")
    parser.add_argument("--url", help="収集対象のURLを直接指定する(--keywordの代わり)")
    parser.add_argument("--tab", choices=["live", "top"], default="live",
                         help="X検索のタブ(live=最新, top=話題のツイート。デフォルトlive)")
    parser.add_argument("--out", help="保存先ディレクトリ(省略時はtools/Xiy配下に自動生成)")
    parser.add_argument("--no-ai", action="store_true", help="Gemini AI分析をスキップする")
    args = parser.parse_args()

    if not args.keyword and not args.url:
        parser.error("--keyword または --url のどちらかを指定してください")

    asyncio.run(run_cli(args))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main_cli()
    else:
        root = tk.Tk()
        app = CollectorApp(root)
        root.mainloop()
