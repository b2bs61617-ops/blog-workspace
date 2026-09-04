# -*- coding: utf-8 -*-
"""藤牧大雅 初ファンミレポ記事(12295)の追記パッチ v2:
- 会場館銘板+うちわ写真(HULIC HALL TOKYO銘板)を「どんなイベント」節に追加
- うちわ提供元を有志ファンダム「MOCHIMOCHI TIGERS」+出資を募った点に更新(紫/赤2種)
出典: https://x.com/kina32ponponxu/status/2095531135849869495
"""
import json, base64, os, sys, urllib.request
from pathlib import Path
import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f'{ENV["WP_KOIKEYS_USERNAME"]}:{ENV["WP_KOIKEYS_APP_PASSWORD"]}'.encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}
HJSON = {**H, "Content-Type": "application/json"}

POST_ID = 12295
SRC = "https://x.com/kina32ponponxu/status/2095531135849869495"
PBS = "https://pbs.twimg.com/media/HRTSdcgbsAAsSCZ.jpg?name=orig"
IMG_PATH = ROOT / "images" / "fujimaki_taiga_first_fanmi_venue_sign.jpg"

if not (IMG_PATH.exists() and IMG_PATH.stat().st_size > 0):
    req = urllib.request.Request(PBS, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        IMG_PATH.write_bytes(r.read())

m = requests.post(
    f"{WP_URL}/wp-json/wp/v2/media",
    headers={**H, "Content-Type": "image/jpeg",
             "Content-Disposition": 'attachment; filename="fujimaki_taiga_first_fanmi_venue_sign.jpg"'},
    data=IMG_PATH.read_bytes(),
)
m.raise_for_status()
media = m.json()
print("venue sign media", media["id"])


def img_block(media, alt, source_url):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    full_w = media["media_details"]["width"]
    full_h = media["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    img_w = large["width"]
    img_h = int(img_w * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {full_w}w'
    return (f'<!-- wp:html -->\n<figure class="wp-block-image size-large">\n'
            f'<img src="{large["source_url"]}" alt="{alt}" width="{img_w}" height="{img_h}"\n'
            f'  style="max-width:100%;height:auto;"\n  srcset="{srcset}"\n'
            f'  sizes="(max-width: {img_w}px) 100vw, {img_w}px">\n'
            f'<figcaption style="text-align:center;font-size:12px;">出典:{source_url}</figcaption>\n'
            f'</figure>\n<!-- /wp:html -->')


post = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}?context=edit", headers=H).json()
content = post["content"]["raw"]

NEW_IMG = img_block(media, "ヒューリックホール東京の館銘板とファンプロジェクトのうちわ", SRC)

REPLACEMENTS = [
    # 1) 館銘板写真を「どんなイベント」節の導入段落直後に挿入
    ("という手書きのメッセージが映し出されました。</p>\n<!-- /wp:paragraph -->",
     "という手書きのメッセージが映し出されました。</p>\n<!-- /wp:paragraph -->\n\n" + NEW_IMG),
    # 2) うちわの提供元・種類を更新
    ("入場時にはうちわとサイリウムが配られましたが、これらは<span class=\"swl-marker mark_yellow\">ファンダム有志が用意したもの</span>だったことが後から明かされ、「本人だけでなくファン側の準備もすごい」と驚きが広がりました。<br>\nうちわは紫地に金色の「Taiga」ロゴと「TAIGA FUJIMAKI 03,09,2026」の文字があしらわれたデザインです。",
     "入場時にはうちわとサイリウムが配られましたが、これらは<span class=\"swl-marker mark_yellow\">有志ファンダム「MOCHIMOCHI TIGERS(もちもちタイガース)」が出資を募って用意したもの</span>だったことが後から明かされ、「本人だけでなくファン側の熱量もすごい」と驚きが広がりました。<br>\nうちわは金色の「Taiga」ロゴと「TAIGA FUJIMAKI 03,09,2026」の文字入りで、紫地・赤地の2種類が用意されました。"),
]

for old, new in REPLACEMENTS:
    if old not in content:
        print("!! NOT FOUND:\n", old[:120])
        sys.exit(1)
    content = content.replace(old, new, 1)

r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}",
                  headers=HJSON,
                  data=json.dumps({"content": content, "status": "draft"}).encode("utf-8"))
r.raise_for_status()
print("patched", POST_ID, "->", r.json()["status"])
