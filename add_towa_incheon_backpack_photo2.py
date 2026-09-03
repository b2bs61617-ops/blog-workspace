# -*- coding: utf-8 -*-
"""Insert a 2nd Incheon Airport video-frame photo (backpack worn on the back
while walking) into the TOWA drafts (JP 12193 / KR 12197 / EN 12198)."""
import json, base64, os
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
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}
HJSON = {**H, "Content-Type": "application/json"}

SRC = "https://x.com/m8msan/status/2083199846501298429"
IMG = ROOT / "images" / "towa_incheon_shark_backpack_2.jpg"

ALT = {
    "ja": "仁川空港でサメ型のリュックを背負って歩くKO1KEYZのメンバー",
    "ko": "인천공항에서 상어 모양 백팩을 메고 걷는 KO1KEYZ 멤버",
    "en": "A KO1KEYZ member walking with the shark backpack on his back at Incheon Airport",
}
CAP = {
    "ja": f'出典:<a href="{SRC}" target="_blank" rel="noopener">X(旧Twitter)</a>',
    "ko": f'출처:<a href="{SRC}" target="_blank" rel="noopener">X(구 트위터)</a>',
    "en": f'Source: <a href="{SRC}" target="_blank" rel="noopener">X (formerly Twitter)</a>',
}

r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers={
    **H, "Content-Type": "image/jpeg",
    "Content-Disposition": 'attachment; filename="towa_incheon_shark_backpack_2.jpg"'},
    data=IMG.read_bytes())
r.raise_for_status()
media = r.json()
MID = media["id"]
sizes = media.get("media_details", {}).get("sizes", {})
fw = media["media_details"]["width"]
fh = media["media_details"]["height"]
large = sizes.get("large") or {"source_url": media["source_url"], "width": fw, "height": fh}
medium = sizes.get("medium") or large
iw = large["width"]
ih = large.get("height") or int(iw * fh / fw)
srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {media["source_url"]} {fw}w'
print("media", MID, media["source_url"])


def figure(lang):
    return f'''<!-- wp:html -->
<figure class="wp-block-image size-large" style="text-align:center;">
<img src="{large["source_url"]}" alt="{ALT[lang]}" width="{iw}" height="{ih}"
  style="max-width:100%;height:auto;margin:0 auto;"
  srcset="{srcset}"
  sizes="(max-width: {iw}px) 100vw, {iw}px">
<figcaption style="text-align:center;font-size:12px;">{CAP[lang]}</figcaption>
</figure>
<!-- /wp:html -->'''


ANCHOR = {
    12193: ("ja", "遠目には黒いシンプルなバックパックに見えますが、近くで見るとひと目で「サメ」とわかる、遊び心のあるデザインになっています。</p>\n<!-- /wp:paragraph -->"),
    12197: ("ko", "멀리서 보면 검고 심플한 백팩처럼 보이지만, 가까이서 보면 한눈에 '상어'라고 알 수 있는 장난기 있는 디자인입니다.</p>\n<!-- /wp:paragraph -->"),
    12198: ("en", "From a distance it reads as a plain black backpack, but up close it's unmistakably a shark — a playful design.</p>\n<!-- /wp:paragraph -->"),
}

for pid, (lang, anchor) in ANCHOR.items():
    cur = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=H)
    cur.raise_for_status()
    content = cur.json()["content"]["raw"]
    if "towa_incheon_shark_backpack_2" in content:
        raise SystemExit(f"[{pid}] 2nd figure already present")
    if anchor not in content:
        raise SystemExit(f"[{pid}] anchor not found")
    content = content.replace(anchor, anchor + "\n\n" + figure(lang), 1)
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=HJSON,
                      data=json.dumps({"status": "draft", "content": content}).encode("utf-8"))
    r.raise_for_status()
    print("updated", pid)

print("DONE")
