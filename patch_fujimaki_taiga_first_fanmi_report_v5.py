# -*- coding: utf-8 -*-
"""藤牧大雅 初ファンミレポ記事(12295) パッチ v5:
- ファンミ当日の様子が分かる公式イベント写真(PR TIMES/株式会社BUZZ GROUP)を3枚追加
  * 会場全景(赤ペンライトで埋まった客席) -> どんなイベント節
  * ソロパフォーマンス -> セトリ節
  * オリジナル曲「Island」パフォーマンス -> セトリ節(Island段落の後)
- 重複していたファン撮影のうちわ写真(12293)を1枚削除
出典表記: PR TIMESプレスリリース(https://prtimes.jp/main/html/rd/p/000000537.000141380.html)
"""
import json, base64, os, re, sys, urllib.request
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
SRC = "https://prtimes.jp/main/html/rd/p/000000537.000141380.html"

IMGS = {
    "crowd": ("https://prcdn.freetls.fastly.net/release_image/141380/537/141380-537-39be1939acabf9beff08c610cfbd47c4-2048x1361.jpg",
              "fujimaki_taiga_first_fanmi_hall.jpg",
              "赤いペンライトで埋まったヒューリックホール東京の客席とステージ"),
    "solo": ("https://prcdn.freetls.fastly.net/release_image/141380/537/141380-537-dd7953876f274b06df2133fdf01fe57a-2768x1848.jpg",
             "fujimaki_taiga_first_fanmi_solo_stage.jpg",
             "初ファンミのステージでパフォーマンスする藤牧大雅"),
    "island": ("https://prcdn.freetls.fastly.net/release_image/141380/537/141380-537-46beeac0a780f116d9cea795d3995fea-2768x1848.jpg",
               "fujimaki_taiga_first_fanmi_island.jpg",
               "風景映像を背景にオリジナル曲を披露する藤牧大雅"),
}

media = {}
for key, (url, fn, alt) in IMGS.items():
    dest = ROOT / "images" / fn
    if not (dest.exists() and dest.stat().st_size > 0):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            dest.write_bytes(r.read())
    up = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**H, "Content-Type": "image/jpeg",
                 "Content-Disposition": f'attachment; filename="{fn}"'},
        data=dest.read_bytes(),
    )
    up.raise_for_status()
    media[key] = up.json()
    print(key, "->", media[key]["id"])


def img_block(m, alt, source_url):
    sizes = m.get("media_details", {}).get("sizes", {})
    full_url = m["source_url"]
    full_w = m["media_details"]["width"]
    full_h = m["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    img_w = large["width"]
    img_h = int(img_w * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {full_w}w'
    return ("<!-- wp:html -->\n<figure class=\"wp-block-image size-large\">\n"
            f'<img src="{large["source_url"]}" alt="{alt}" width="{img_w}" height="{img_h}"\n'
            f'  style="max-width:100%;height:auto;"\n  srcset="{srcset}"\n'
            f'  sizes="(max-width: {img_w}px) 100vw, {img_w}px">\n'
            f'<figcaption style="text-align:center;font-size:12px;">出典:{source_url}</figcaption>\n'
            "</figure>\n<!-- /wp:html -->")


post = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}?context=edit", headers=H).json()
content = post["content"]["raw"]

# 1) 重複うちわ写真(12293 = 出典 _TruTH4me/2095440697465958494)を丸ごと削除
pat = re.compile(
    r"\n\n<!-- wp:html -->\n<figure class=\"wp-block-image size-large\">\n<img [^>]*?alt=\"[^\"]*ありがとう[^\"]*\"[^>]*?>\n"
    r"<figcaption[^>]*>出典:https://x\.com/_TruTH4me/status/2095440697465958494</figcaption>\n</figure>\n<!-- /wp:html -->"
)
content, n = pat.subn("", content, count=1)
print("removed dup uchiwa image:", n)

# 2) 会場全景を「どんなイベント」節の館銘板写真の直後に
anchor_hall = "出典:https://x.com/kina32ponponxu/status/2095531135849869495</figcaption>\n</figure>\n<!-- /wp:html -->"
assert anchor_hall in content, "hall anchor missing"
content = content.replace(anchor_hall, anchor_hall + "\n\n" + img_block(media["crowd"], IMGS["crowd"][2], SRC), 1)

# 3) ソロパフォーマンス写真を演出段落の直後に
anchor_solo = "規模の大きさに驚くファンの声も上がっています。</p>\n<!-- /wp:paragraph -->"
assert anchor_solo in content, "solo anchor missing"
content = content.replace(anchor_solo, anchor_solo + "\n\n" + img_block(media["solo"], IMGS["solo"][2], SRC), 1)

# 4) Island写真をIsland段落の直後に
anchor_island = "パートナーのパートを客席と一緒に歌う場面もあり、会場が一体となりました。</p>\n<!-- /wp:paragraph -->"
assert anchor_island in content, "island anchor missing"
content = content.replace(anchor_island, anchor_island + "\n\n" + img_block(media["island"], IMGS["island"][2], SRC), 1)

r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}",
                  headers=HJSON,
                  data=json.dumps({"content": content, "status": "draft"}).encode("utf-8"))
r.raise_for_status()
print("patched", POST_ID, "->", r.json()["status"])
print("figure count now:", content.count('<figure class="wp-block-image'))
