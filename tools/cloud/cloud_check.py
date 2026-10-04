"""Read-only health check for running the blog tools (cloud or local).

Checks .env, WordPress REST auth for every site, Buffer API, Rakuten API and
eyecatch rendering (Playwright + Japanese font). Nothing is posted or changed.

Usage: python3 tools/cloud/cloud_check.py
"""
import re
import sys
import tempfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

results = []


def report(name, ok, detail=""):
    results.append(ok)
    print(f"{'OK ' if ok else 'NG '} {name}" + (f" … {detail}" if detail else ""))


def load_env():
    env = {}
    path = ROOT / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def check_wordpress(env):
    sites = sorted({m.group(1) for k in env if (m := re.match(r"WP_([A-Z0-9]+)_URL$", k))})
    for site in sites:
        url = env.get(f"WP_{site}_URL", "").rstrip("/")
        user = env.get(f"WP_{site}_USERNAME")
        pw = env.get(f"WP_{site}_APP_PASSWORD")
        if not (url and user and pw):
            report(f"WordPress {site}", False, "URL/ユーザー名/アプリパスワードのどれかが未設定")
            continue
        try:
            r = requests.get(f"{url}/wp-json/wp/v2/users/me", auth=(user, pw),
                             params={"context": "edit"}, timeout=20)
            if r.ok:
                report(f"WordPress {site}", True, f"{url} に {r.json().get('name')} でログインOK")
            else:
                report(f"WordPress {site}", False, f"{url} HTTP {r.status_code}")
        except Exception as e:
            report(f"WordPress {site}", False, f"{url} 接続失敗: {type(e).__name__}")


def check_buffer(env):
    token = env.get("BUFFER_ACCESS_TOKEN")
    if not (token and env.get("BUFFER_X_CHANNEL_ID")):
        report("Buffer(X/Threads)", False, "BUFFER_ACCESS_TOKEN / BUFFER_X_CHANNEL_ID 未設定")
        return
    try:
        r = requests.post("https://api.buffer.com", timeout=20,
                          headers={"Authorization": f"Bearer {token}"},
                          json={"query": "query { account { id } }"})
        data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        if r.ok and data.get("data", {}).get("account"):
            report("Buffer(X/Threads)", True, "認証OK")
        else:
            report("Buffer(X/Threads)", False, f"HTTP {r.status_code} {str(data.get('errors', ''))[:120]}")
    except Exception as e:
        report("Buffer(X/Threads)", False, f"接続失敗: {type(e).__name__}")


def check_rakuten(env):
    from affiliate_linker import fetch_rakuten_items
    if not (env.get("RAKUTEN_APP_ID") and env.get("RAKUTEN_ACCESS_KEY")):
        report("楽天API(アフィリ)", False, "未設定")
        return
    try:
        items = fetch_rakuten_items(env["RAKUTEN_APP_ID"], env["RAKUTEN_ACCESS_KEY"],
                                    env.get("RAKUTEN_AFFILIATE_ID"), "リップ", hits=1)
        report("楽天API(アフィリ)", True, f"{len(items)}件取得")
    except Exception as e:
        report("楽天API(アフィリ)", False, f"{e} (IP許可リスト外の可能性。Amazonリンクだけで代用可)")


def check_eyecatch():
    try:
        from playwright.sync_api import sync_playwright
        out = Path(tempfile.gettempdir()) / "cloud_check_eyecatch.png"
        html = ("<body style=\"margin:0;font-family:'Yu Gothic','Meiryo','Noto Sans CJK JP',sans-serif;"
                "font-size:64px;font-weight:900\">日本語テスト漢字かなカナ</body>")
        with sync_playwright() as p:
            b = p.chromium.launch()
            page = b.new_page(viewport={"width": 900, "height": 120})
            page.set_content(html)
            page.screenshot(path=str(out))
            b.close()
        # Open the PNG to confirm the text is not tofu (□□□).
        report("アイキャッチ描画(Chromium)", True, f"テスト画像 {out} を開いて文字化けが無いか目視確認")
    except Exception as e:
        report("アイキャッチ描画(Chromium)", False, f"{type(e).__name__}: {str(e)[:120]}")

    try:
        import subprocess
        fonts = subprocess.run(["fc-list", ":lang=ja"], capture_output=True, text=True).stdout
        report("日本語フォント", bool(fonts.strip()), f"{len(fonts.splitlines())}書体")
    except FileNotFoundError:
        report("日本語フォント", True, "fc-list無し(Windowsなら游ゴシックを使用)")


def main():
    env = load_env()
    report(".env", bool(env), f"{len(env)}項目" if env else "無い。tools/cloud/make_env.py を実行してワン")
    check_wordpress(env)
    check_buffer(env)
    check_rakuten(env)
    check_eyecatch()
    print(f"\n結果: {sum(results)}/{len(results)} OK")


if __name__ == "__main__":
    main()
