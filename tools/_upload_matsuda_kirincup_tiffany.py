# -*- coding: utf-8 -*-
"""One-off: upload 松田元太 Kirin Cup watching outfit (Ray-Ban/Tiffany/Bottega) article to chomoand-4.blog as draft."""
import re
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
env = {}
for l in open(ROOT / ".env", encoding="utf-8"):
    l = l.strip()
    if "=" in l and not l.startswith("#"):
        k, v = l.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
U = env["WP_CHOMO4_URL"].rstrip("/")
A = (env["WP_CHOMO4_USERNAME"], env["WP_CHOMO4_APP_PASSWORD"])

TITLE = "【サッカー観戦】松田元太の私服はどこの？ネックレスはティファニー？"
SLUG = "genta-matsuda-kirin-cup-outfit-tiffany"
SRC = "https://www.instagram.com/p/DeMby7jk9Ik/"
IMAGES = {
    "IMG_FULL": ("matsuda_kirincup_selfie.jpg",
                 "国立競技場の観客席で宮近海斗・吉澤閑也と自撮りする、キャメルのニットにゴールドのメガネの松田元太", f"出典:{SRC}"),
    "IMG_STADIUM": ("matsuda_kirincup_stadium.jpg",
                    "試合後に花火が打ち上がる夜の国立競技場", f"出典:{SRC}"),
    "IMG_GLASSES": ("matsuda_kirincup_glasses_zoom.jpg",
                    "松田元太がかけていたゴールドのメタルフレームのメガネのアップ", f"出典:{SRC}(一部を拡大)"),
    "IMG_NECK": ("matsuda_kirincup_necklace_zoom.jpg",
                 "キャメルのVネックニットからのぞくゴールドのチェーンネックレスのアップ", f"出典:{SRC}(一部を拡大)"),
}


def upload(path, ctype):
    r = requests.post(f"{U}/wp-json/wp/v2/media", auth=A, data=path.read_bytes(), headers={
        "Content-Type": ctype,
        "Content-Disposition": f'attachment; filename="{path.name}"'}, timeout=120)
    r.raise_for_status()
    return r.json()


html = (ROOT / "articles/matsuda_genta_kirincup_tiffany_outfit.html").read_text(encoding="utf-8")
for key, (fn, alt, cap) in IMAGES.items():
    m = upload(ROOT / "images" / fn, "image/jpeg")
    s = m["media_details"]["sizes"]
    lg = s.get("large", s["full"]); md = s.get("medium", lg); fu = s["full"]
    fig = (f'<!-- wp:html -->\n<figure class="wp-block-image size-large">\n'
           f'<img src="{lg["source_url"]}" alt="{alt}" width="{lg["width"]}" height="{lg["height"]}" style="max-width:100%;height:auto;" '
           f'srcset="{md["source_url"]} {md["width"]}w, {lg["source_url"]} {lg["width"]}w, {fu["source_url"]} {fu["width"]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
           f'<figcaption style="font-size:0.8em;color:#888;">{cap}</figcaption>\n</figure>\n<!-- /wp:html -->')
    html = html.replace(f"<!-- {key} -->", fig)
    print("media", key, m["id"])
assert "IMG_" not in html and "<hr" not in html

ey = upload(ROOT / "images/matsuda_genta_kirincup_tiffany_eyecatch_canva.jpg", "image/jpeg")
print("eyecatch media", ey["id"])

r = requests.post(f"{U}/wp-json/wp/v2/posts", auth=A, json={
    "title": TITLE, "content": html, "slug": SLUG, "status": "draft",
    "categories": [3, 7], "author": 2, "featured_media": ey["id"]}, timeout=120)
r.raise_for_status()
p = r.json()
print("POST", p["id"], p["status"], p["slug"], f"{U}/?p={p['id']}")
text = re.sub(r"<[^>]+>", "", html)
print("chars", len(re.sub(r"\s", "", text)))
