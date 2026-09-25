# -*- coding: utf-8 -*-
"""One-off: upload 松倉海斗 奥多摩・昭和橋 article to chomoand-4.blog as draft."""
import json, re, sys, urllib.parse
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

TITLE = "松倉海斗のインスタの場所はどこ？奥多摩の昭和橋と判明！"
IG_URL = "https://www.instagram.com/p/DN5WwXkk7dk/"
CAP = f"出典:松倉海斗Instagram(@machu_tj_1114) {IG_URL}"
IMAGES = {
    "IG_IMAGE_1": ("matsukura_okutama_ig_1.jpg", "踏切のある坂道に立つ松倉海斗。白い13番のタンクトップにデニムのハーフパンツ姿"),
    "IG_IMAGE_4": ("matsukura_okutama_ig_4.jpg", "奥多摩の昭和橋の上で景色を撮る松倉海斗の後ろ姿。道路の先にENEOSの看板が見える"),
    "IG_IMAGE_6": ("matsukura_okutama_ig_6.jpg", "奥多摩の河原の岩に腰かける松倉海斗"),
}


def upload(path, ctype):
    data = path.read_bytes()
    r = requests.post(f"{U}/wp-json/wp/v2/media", auth=A, data=data, headers={
        "Content-Type": ctype,
        "Content-Disposition": f'attachment; filename="{path.name}"'}, timeout=120)
    r.raise_for_status()
    return r.json()


html = (ROOT / "articles/travis_japan_matsukura_okutama_showabashi.html").read_text(encoding="utf-8")
for key, (fn, alt) in IMAGES.items():
    m = upload(ROOT / "images" / fn, "image/jpeg")
    s = m["media_details"]["sizes"]
    lg = s.get("large", s["full"]); md = s.get("medium", lg); fu = s["full"]
    fig = (f'<!-- wp:html -->\n<figure class="wp-block-image size-large">\n'
           f'<img src="{lg["source_url"]}" alt="{alt}" width="{lg["width"]}" height="{lg["height"]}" style="max-width:100%;height:auto;" '
           f'srcset="{md["source_url"]} {md["width"]}w, {lg["source_url"]} {lg["width"]}w, {fu["source_url"]} {fu["width"]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
           f'<figcaption style="font-size:0.8em;color:#888;">{CAP}</figcaption>\n</figure>\n<!-- /wp:html -->')
    html = html.replace(f"<!-- {key} -->", fig)
    print("media", key, m["id"])
assert "IG_IMAGE" not in html and "<hr" not in html

ey = upload(ROOT / "images/travis_japan_matsukura_okutama_showabashi_eyecatch.png", "image/png")
print("eyecatch media", ey["id"])

tr = requests.get("https://translate.googleapis.com/translate_a/single",
                  params={"client": "gtx", "sl": "ja", "tl": "en", "dt": "t", "q": TITLE}, timeout=30).json()
en = "".join(x[0] for x in tr[0])
slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9 -]", "", en.lower()).strip().replace(" ", "-"))[:30].strip("-")
print("slug", slug, "|", en)

r = requests.post(f"{U}/wp-json/wp/v2/posts", auth=A, json={
    "title": TITLE, "content": html, "slug": slug, "status": "draft",
    "categories": [3, 6], "author": 2, "featured_media": ey["id"]}, timeout=120)
r.raise_for_status()
p = r.json()
print("POST", p["id"], p["status"], p["slug"], f"{U}/?p={p['id']}")
text = re.sub(r"<[^>]+>", "", html)
print("chars", len(re.sub(r"\s", "", text)))
