"""chomoand-1.com(コイキーズブログ)で、日本語記事に韓国語版・英語版(下書き含む)が
作られているかをチェックするスクリプト。

blog-uploadスキルSTEP6(韓国語)・STEP7(英語)は「日本語投稿後に自動で多言語版を作る」設計だが、
GET /wp-json/wp/v2/posts はPolylangの`lang`/`translations`フィールドを
返さない(docs/korea-expansion.md参照)ため、これまでSTEP6/7が本当に実行され
成功したかを外から確認する手段がなかった。このスクリプトはslugの命名規則
(韓国語版は元記事slug + "-kr"、英語版は元記事slug + "-en")で日本語記事と
突き合わせ、各言語版が見つからない日本語記事を一覧化する。

2026-08-19に韓国語専用の check_kr_translation_gaps.py から改名・拡張した
(英語版導入に伴い、docs/english-expansion.md参照)。

**下書き(status=draft)も含めて取得するため、WordPressの認証情報(.env)が必須。**
公開済み記事だけを見るサイトマップ等では「下書きのまま止まっている」ケースと
「本当に一度も作られていない」ケースを区別できないので、必ずこのスクリプトを
使うこと。

実行:
  python tools/check_translation_gaps.py
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ROOT = Path(__file__).parent.parent
ENV = {**load_env(ROOT / ".env"), **os.environ}

# (Polylang URLセグメント, slugサフィックス, 表示名)
LANGS = [
    ("/ko/", "-kr", "韓国語"),
    ("/en/", "-en", "英語"),
]


def fetch_all_posts(site_url, auth_header):
    """status=publish,draft の全記事を(id, slug, link, status, date)のリストで返す"""
    posts = []
    page = 1
    while True:
        url = (
            f"{site_url}/wp-json/wp/v2/posts"
            f"?status=publish,draft&per_page=100&page={page}"
            f"&_fields=id,slug,link,status,date"
        )
        req = urllib.request.Request(url, headers={"Authorization": f"Basic {auth_header}"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                batch = json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 400:
                # ページ範囲外(WPの仕様)。ここで終了
                break
            raise
        if not batch:
            break
        posts.extend(batch)
        page += 1
    return posts


def is_translation(post):
    """いずれかの言語版URLセグメントを含むか"""
    return any(segment in post["link"] for segment, _, _ in LANGS)


def main():
    site_url = ENV.get("WP_KOIKEYS_URL", "").rstrip("/")
    user = ENV.get("WP_KOIKEYS_USERNAME", "")
    app_password = ENV.get("WP_KOIKEYS_APP_PASSWORD", "")
    if not (site_url and user and app_password):
        print(
            "WP_KOIKEYS_URL / WP_KOIKEYS_USERNAME / WP_KOIKEYS_APP_PASSWORD が"
            ".envに設定されていないワン。この情報を持っているPCで実行してほしいワン。",
            file=sys.stderr,
        )
        sys.exit(1)

    auth_header = base64.b64encode(f"{user}:{app_password}".encode()).decode()
    posts = fetch_all_posts(site_url, auth_header)

    jp_posts = [p for p in posts if not is_translation(p)]

    print(f"日本語記事: {len(jp_posts)}件\n")

    any_gaps = False
    for segment, suffix, label in LANGS:
        lang_posts = [p for p in posts if segment in p["link"]]
        print(f"{label}記事(下書き含む): {len(lang_posts)}件")

        gaps = []
        for jp in jp_posts:
            jp_slug = jp["slug"]
            matched = [p for p in lang_posts if p["slug"].startswith(f"{jp_slug}{suffix}")]
            if not matched:
                gaps.append(jp)

        if not gaps:
            print(f"  → {label}版が見つからない日本語記事はなかったワン。\n")
            continue

        any_gaps = True
        print(f"  → {label}版が見つからない日本語記事: {len(gaps)}件")
        for jp in sorted(gaps, key=lambda p: p["date"]):
            print(f"    - [{jp['status']}] {jp['date']} id={jp['id']} slug={jp['slug']}")
            print(f"      {jp['link']}")
        print()

    if not any_gaps:
        print("すべての日本語記事に韓国語版・英語版が揃っているワン。")


if __name__ == "__main__":
    main()
