# -*- coding: utf-8 -*-
"""映画『マッチング』ラストの意味・犯人考察(地上波初放送 2026-09-29) -> chomoand.com 公開投稿.

本文は articles/matching_movie_last_kousatsu.html を読み込み、Gutenbergブロックへ変換する
(<hr>は除去、表は wp:table、箇条書きは wp:html)。
"""
import json, base64, os, re, sys, urllib.request, urllib.parse
from pathlib import Path

import requests

ROOT = Path(__file__).parent
sys.stdout.reconfigure(encoding="utf-8")


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


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_TREND_USERNAME']}:{ENV['WP_TREND_APP_PASSWORD']}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

EXISTING_POST_ID = None
STATUS = "publish"
EYECATCH_PATH = ROOT / "images" / "matching_movie_last_eyecatch.png"
SOURCE = ROOT / "articles" / "matching_movie_last_kousatsu.html"

title = "映画マッチングの最後の意味は？犯人は吐夢か影山か、ラストの笑みと異母姉弟の真相をネタバレ考察"


def style_table(inner):
    def row(m):
        cells = re.findall(r"<td>(.*?)</td>", m.group(1), re.S)
        k, v = cells[0], cells[1]
        return (
            f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;width:170px;"><strong>{k}</strong></td>'
            f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        )
    rows = re.sub(r"<tr>(.*?)</tr>", row, inner, flags=re.S)
    return (
        '<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n'
        f"{rows.strip()}\n</tbody></table></figure>\n<!-- /wp:table -->"
    )


def to_blocks(src):
    out = []
    for m in re.finditer(r"<(p|h2|h3|table|ul)>(.*?)</\1>|<hr>", src, re.S):
        tag, inner = m.group(1), m.group(2)
        if tag is None:
            continue  # <hr> は全削除ルール
        if tag == "p":
            out.append(f"<!-- wp:paragraph -->\n<p>{inner}</p>\n<!-- /wp:paragraph -->")
        elif tag == "h2":
            out.append(f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{inner}</h2>\n<!-- /wp:heading -->')
        elif tag == "h3":
            out.append(f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{inner}</h3>\n<!-- /wp:heading -->')
        elif tag == "table":
            out.append(style_table(inner))
        elif tag == "ul":
            out.append(
                "<!-- wp:html -->\n"
                '<div style="border:1px solid #ddd;border-left:4px solid #8e6cc0;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f5fb;">\n'
                f'<ul style="margin:0;padding-left:1.2em;">{inner}</ul>\n</div>\n<!-- /wp:html -->'
            )
    return "\n\n".join(out)


content = to_blocks(SOURCE.read_text(encoding="utf-8"))


def get_slug(title_text):
    url = ("https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q="
           + urllib.parse.quote(title_text))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    en = "".join(seg[0] for seg in data[0])
    slug = re.sub(r"[^a-z0-9\s-]", "", en.lower())
    slug = re.sub(r"\s+", "-", slug.strip())
    return re.sub(r"-+", "-", slug)[:30].rstrip("-")


try:
    slug = get_slug(title)
except Exception as e:
    print("slug translate failed, fallback:", e)
    slug = "matching-movie-ending-meaning"
print("slug:", slug)

# カテゴリ: 「映画」があれば併用、なければ速報記事と同じ37
cats = requests.get(f"{WP_URL}/wp-json/wp/v2/categories?per_page=100", headers=HEADERS_AUTH).json()
cat_ids = [c["id"] for c in cats if c["name"] in ("映画",)] or [37]
print("categories:", cat_ids, [c["name"] for c in cats if c["id"] in cat_ids])

with open(EYECATCH_PATH, "rb") as f:
    img = f.read()
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/media",
    headers={**HEADERS_AUTH, "Content-Type": "image/png",
             "Content-Disposition": 'attachment; filename="matching_movie_last_eyecatch.png"'},
    data=img,
)
r.raise_for_status()
media_id = r.json()["id"]
print("EYECATCH_MEDIA_ID", media_id)

payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": STATUS,
    "categories": cat_ids,
    "author": 4,
    "featured_media": media_id,
}
endpoint = f"{WP_URL}/wp-json/wp/v2/posts" + (f"/{EXISTING_POST_ID}" if EXISTING_POST_ID else "")
r = requests.post(endpoint, headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                  data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"])
print("SLUG", post["slug"])
print("STATUS", post["status"])
print("LINK", post["link"])
