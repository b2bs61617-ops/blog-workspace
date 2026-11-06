# -*- coding: utf-8 -*-
"""Upload drafts: 井上瑞稀 誕生日食道楽ロケ地 / 岩﨑大昇 PRADAニット to chomoand-5.site."""
import re, json, base64, urllib.request

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip().strip('"')
BASE = env["WP_CHOMO5_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_CHOMO5_USERNAME']}:{env['WP_CHOMO5_APP_PASSWORD']}".encode()).decode()


def req(path, data=None, headers=None):
    r = urllib.request.Request(BASE + path, data=data, method="POST" if data is not None else "GET")
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    with urllib.request.urlopen(r) as resp:
        return json.loads(resp.read().decode("utf-8"))


def media(fn, alt=""):
    m = req("/wp-json/wp/v2/media", open(REPO + rf"\images\{fn}", "rb").read(),
            {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{fn}"'})
    if alt:
        req(f"/wp-json/wp/v2/media/{m['id']}", json.dumps({"alt_text": alt}).encode(), {"Content-Type": "application/json"})
    return m


def build(article, prefix, imgs, src, src_label, maxw=""):
    html = open(REPO + rf"\articles\{article}.html", encoding="utf-8").read()
    for k, alt in imgs.items():
        m = media(f"{prefix}_{k}.jpg", alt)
        style = f' style="max-width:{maxw};margin-left:auto;margin-right:auto;"' if maxw else ""
        fig = ('<!-- wp:html -->\n'
               '<figure class="wp-block-image size-full"%s><img src="%s" alt="%s" class="wp-image-%d" style="max-width:100%%;height:auto;"/>'
               '<figcaption style="font-size:0.8em;color:#888;">出典:<a href="%s" target="_blank" rel="noopener">%s</a></figcaption></figure>\n'
               '<!-- /wp:html -->') % (style, m["source_url"], alt, m["id"], src, src_label)
        html = html.replace(f"[[IMG_{k}]]", fig)
    html = re.sub(r"<hr\s*/?>", "", html).strip()
    assert "[[" not in html, re.findall(r"\[\[[^\]]+\]\]", html)
    return html


YT = "https://www.youtube.com/watch?v=IZN1evTXHYw"
html1 = build("ktl_mizuki_bday_gourmet_shops", "ktl_mizuki_bday_gourmet", {
    "01": "テジョンデ4号店 鮮-Sen- サンナッチ館の外観",
    "02": "井上瑞稀が食べたカンジャンケジャン",
    "03": "カンジャンケジャンを食べる井上瑞稀",
    "04": "スペシャルカンジャンケジャン丼",
    "05": "人形町今半 東京ガーデンテラス紀尾井町店の入り口",
    "06": "人形町今半の焼松茸",
    "07": "人形町今半の松茸すき焼",
    "08": "人形町今半の松茸御飯",
    "09": "井上瑞稀の誕生日のティラミスケーキ",
}, YT, "ジュニアCHANNEL(YouTube)")
eye1 = media("ktl_mizuki_bday_gourmet_eyecatch.jpg")["id"]
p1 = req("/wp-json/wp/v2/posts", json.dumps({
    "title": "【未】【井上瑞稀】誕生日食道楽のお店はどこ？カンジャンケジャンと松茸！",
    "slug": "mizuki-birthday-gourmet-shops",
    "content": html1, "status": "draft",
    "categories": [4, 7], "author": 2, "featured_media": eye1,
}).encode(), {"Content-Type": "application/json"})
print("POST1", p1["id"], p1["status"], p1["slug"], "eye", eye1)

IG = "https://www.instagram.com/reel/DfPXgefT9lZ/"
html2 = build("ktl_iwasaki_prada_knit", "ktl_iwasaki_prada_knit", {
    "01": "岩﨑大昇のニットの背中の三角ロゴ",
    "02": "ケーキを運ぶネイビーニットの岩﨑大昇",
}, IG, "KEY TO LIT公式Instagram", maxw="360px")
eye2 = media("ktl_iwasaki_prada_knit_eyecatch.jpg")["id"]
p2 = req("/wp-json/wp/v2/posts", json.dumps({
    "title": "【未】【岩﨑大昇】瑞稀誕生日インスタライブのニットはどこの？PRADA！",
    "slug": "iwasaki-taisho-prada-knit",
    "content": html2, "status": "draft",
    "categories": [4, 6, 7], "author": 2, "featured_media": eye2,
}).encode(), {"Content-Type": "application/json"})
print("POST2", p2["id"], p2["status"], p2["slug"], "eye", eye2)
