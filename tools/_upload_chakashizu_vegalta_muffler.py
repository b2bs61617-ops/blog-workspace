# -*- coding: utf-8 -*-
"""One-off: upload ちゃかしず ベガルタ towel muffler article to chomoand-4.blog as draft."""
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

TITLE = "宮近海斗と吉澤閑也がユアスタで巻いたタオルマフラーはどこの？"
SRC1 = "https://x.com/vegaltaphoto/status/2106624522879385632"
IMAGES = {
    "IMG_WIDE": ("chakashizu_vegalta_wide.jpg",
                 "ユアスタのピッチでベガルタ仙台のタオルマフラーを巻いて手を挙げる吉澤閑也と宮近海斗",
                 f"出典:{SRC1}"),
    "IMG_MIYACHIKA": ("chakashizu_vegalta_miyachika.jpg",
                      "紺地に白いVEGALTA SENDAIロゴのタオルマフラーを巻いた宮近海斗",
                      f"出典:{SRC1}"),
    "IMG_YOSHIZAWA": ("chakashizu_vegalta_yoshizawa.jpg",
                      "金地にエンブレムとSINCE1994が入ったタオルマフラーを巻いた吉澤閑也",
                      f"出典:{SRC1}"),
    "IMG_BACK": ("chakashizu_vegalta_back.jpg",
                 "背中にSHIZU 42とCHAKA 09が入った黒いユニフォームでドリブル対決に臨む2人",
                 f"出典:{SRC1}"),
}


def upload(path, ctype):
    r = requests.post(f"{U}/wp-json/wp/v2/media", auth=A, data=path.read_bytes(), headers={
        "Content-Type": ctype,
        "Content-Disposition": f'attachment; filename="{path.name}"'}, timeout=120)
    r.raise_for_status()
    return r.json()


html = (ROOT / "articles/chakashizu_vegalta_towel_muffler.html").read_text(encoding="utf-8")
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

ey = upload(ROOT / "images/chakashizu_vegalta_towel_muffler_eyecatch.png", "image/png")
print("eyecatch media", ey["id"])

tr = requests.get("https://translate.googleapis.com/translate_a/single",
                  params={"client": "gtx", "sl": "ja", "tl": "en", "dt": "t", "q": TITLE}, timeout=30).json()
en = "".join(x[0] for x in tr[0])
slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9 -]", "", en.lower()).strip().replace(" ", "-"))[:30].strip("-")
print("slug", slug, "|", en)

r = requests.post(f"{U}/wp-json/wp/v2/posts", auth=A, json={
    "title": TITLE, "content": html, "slug": slug, "status": "draft",
    "categories": [3, 9, 12], "author": 2, "featured_media": ey["id"]}, timeout=120)
r.raise_for_status()
p = r.json()
print("POST", p["id"], p["status"], p["slug"], f"{U}/?p={p['id']}")
text = re.sub(r"<[^>]+>", "", html)
print("chars", len(re.sub(r"\s", "", text)))
