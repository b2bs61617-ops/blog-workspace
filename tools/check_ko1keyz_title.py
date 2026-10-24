"""chomoand-1.com(コイキーズブログ)の記事タイトルにグループ名「KO1KEYZ」が
入っているかをチェックするスクリプト(2026-10-24追加、ユーザー指示)。

メンバー個人記事で「【RYOGA】空港バッグの…」のように活動名だけをタイトルに
入れると、活動名単体では検索に引っかからない(RYOGA・YURA・KEITOなどは
一般的な英字名のため)。メンバー記事でも必ず「【KO1KEYZ】RYOGAの空港バッグ…」
のようにグループ名を入れる。

docs/rules.mdに書くだけだと別PC・別セッションで守られないため
(docs/history.mdの「リード文直後の区切り線バグ」と同じ教訓)、
blog-uploadスキルのSTEP3直後とpublishスキルの公開前にこのスクリプトを
実行し、NGが1件でもあれば終了コード1で止める。

判定: タイトルに「KO1KEYZ」(大文字小文字不問)か「コイキーズ」「코이키즈」が
含まれていればOK。

実行:
  python tools/check_ko1keyz_title.py 15163 15165 15166   # 指定IDだけ
  python tools/check_ko1keyz_title.py --drafts            # 下書き全件
"""
import base64
import json
import os
import re
import sys
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

GROUP_NAME = re.compile(r"KO1KEYZ|コイキーズ|코이키즈", re.IGNORECASE)


def get_json(url, auth_header):
    req = urllib.request.Request(url, headers={"Authorization": auth_header})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))


def fetch_posts(site_url, auth_header, ids):
    if ids:
        return [
            get_json(f"{site_url}/wp-json/wp/v2/posts/{i}?context=edit&_fields=id,status,title", auth_header)
            for i in ids
        ]
    posts = []
    page = 1
    while True:
        url = (
            f"{site_url}/wp-json/wp/v2/posts"
            f"?status=draft&per_page=100&page={page}&context=edit&_fields=id,status,title"
        )
        try:
            batch = get_json(url, auth_header)
        except urllib.error.HTTPError as e:
            if e.code == 400:  # ページ範囲外
                break
            raise
        if not batch:
            break
        posts.extend(batch)
        page += 1
    return posts


def main():
    args = sys.argv[1:]
    ids = [a for a in args if a.isdigit()]
    if not ids and "--drafts" not in args:
        print(__doc__)
        sys.exit(2)

    site_url = ENV["WP_KOIKEYS_URL"].rstrip("/")
    token = base64.b64encode(
        f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()
    ).decode()
    posts = fetch_posts(site_url, f"Basic {token}", ids)

    ng = [p for p in posts if not GROUP_NAME.search(p["title"]["raw"])]
    if not ng:
        print(f"OK: {len(posts)}件すべてタイトルにKO1KEYZが入っています")
        return
    print(f"NG: タイトルにKO1KEYZが入っていない記事が{len(ng)}件あります")
    for p in ng:
        print(f"  {p['id']} [{p['status']}] {p['title']['raw']}")
    print("→ 「【KO1KEYZ】RYOGAの〜」のようにグループ名を入れてから進めること")
    sys.exit(1)


if __name__ == "__main__":
    main()
