# -*- coding: utf-8 -*-
"""One-off: upload 3 Taipei Dome (YouTube 0eSnpvIFz3Y) outfit articles to chomoand-4.blog as drafts.

松倉海斗=HYSTERIC GLAMOUR tank / 吉澤閑也=Chrome Hearts horseshoe tee / 川島如恵留=Y-3 setup.
Usage: python tools/_upload_travis_taipei_dome_3items.py [matsukura|yoshizawa|kawashima ...]
"""
import re
import sys
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

SRC = "https://www.youtube.com/watch?v=0eSnpvIFz3Y"
CAP = f"出典:{SRC}"
CAP_ZOOM = f"出典:{SRC}(一部を拡大)"

POSTS = {
    "matsukura": {
        "title": "【台北ドーム】松倉海斗のタンクトップはどこの？ヒステリックと判明！",
        "slug": "matsukura-taipei-dome-hysteric-tank",
        "html": "articles/matsukura_taipei_dome_hysteric_tank.html",
        "categories": [3, 6],
        "eyecatch": "images/matsukura_taipei_hysteric_eyecatch_canva.jpg",
        "images": {
            "IMG_REHEARSAL": ("matsukura_taipei_hysteric_rehearsal.jpg",
                              "台北ドームのグラウンドで、グリーンのメッシュタンクトップとベージュのハーフパンツ姿でストレッチする松倉海斗", CAP),
            "IMG_FACE": ("matsukura_taipei_hysteric_face2.jpg",
                         "頭にサングラスをのせ、グリーンのタンクトップにクロスのネックレスを合わせて笑顔を見せる松倉海斗", CAP),
            "IMG_ZOOM": ("matsukura_taipei_hysteric_zoom.jpg",
                         "タンクトップの胸に入った「HYSTERIC」の文字と大きな「84」、数字に重なる女性のイラストのアップ", CAP_ZOOM),
            "IMG_END": ("matsukura_taipei_hysteric_end.jpg",
                        "パフォーマンス後のバックステージで、同じ「HYSTERIC 84」のタンクトップを着た松倉海斗", CAP_ZOOM),
        },
    },
    "yoshizawa": {
        "title": "【台北ドーム】吉澤閑也の黒Tシャツはどこの？クロムハーツと判明！",
        "slug": "yoshizawa-taipei-dome-chrome-hearts-tee",
        "html": "articles/yoshizawa_taipei_dome_chromehearts_tee.html",
        "categories": [3, 12],
        "eyecatch": "images/yoshizawa_taipei_chromehearts_eyecatch_canva.jpg",
        "images": {
            "IMG_BACK": ("yoshizawa_taipei_chromehearts_back.jpg",
                         "台北ドームのグラウンドを歩く、背中に白いホースシューのプリントが入った黒Tシャツ姿の吉澤閑也", CAP),
            "IMG_ZOOM": ("yoshizawa_taipei_chromehearts_zoom.jpg",
                         "黒Tシャツの背中に入った、馬蹄形の「CHROME HEARTS」ロゴと中央のフローラルクロスのアップ", CAP_ZOOM),
            "IMG_REHEARSAL": ("yoshizawa_taipei_chromehearts_rehearsal.jpg",
                              "スペシャルパフォーマンスのリハーサル準備中、背中のクロムハーツのロゴが見える吉澤閑也", CAP),
        },
    },
    "kawashima": {
        "title": "【台北ドーム】川島如恵留のジャージはどこの？Y-3のセットアップ！",
        "slug": "kawashima-taipei-dome-y3-setup",
        "html": "articles/kawashima_taipei_dome_y3_setup.html",
        "categories": [3, 11],
        "eyecatch": "images/kawashima_taipei_y3_eyecatch_canva.jpg",
        "images": {
            "IMG_REHEARSAL": ("kawashima_taipei_y3_rehearsal.jpg",
                              "台北ドームのグラウンドで、グレーの切り替えが入ったダークグリーンのトラックジャケットを着た川島如恵留", CAP),
            "IMG_END": ("kawashima_taipei_y3_end.jpg",
                        "パフォーマンス後のバックステージで、Y-3のトラックジャケットとパンツのセットアップを着た川島如恵留", CAP_ZOOM),
            "IMG_LOGO": ("kawashima_taipei_y3_logo_zoom.jpg",
                         "トラックジャケットの左胸に入った白い「Y-3」ロゴのアップ", CAP_ZOOM),
        },
    },
}


def upload(path, ctype):
    r = requests.post(f"{U}/wp-json/wp/v2/media", auth=A, data=path.read_bytes(), headers={
        "Content-Type": ctype,
        "Content-Disposition": f'attachment; filename="{path.name}"'}, timeout=120)
    r.raise_for_status()
    return r.json()


def figure(m, alt, cap):
    s = m["media_details"]["sizes"]
    fu = s.get("full", {"source_url": m["source_url"], "width": m["media_details"]["width"],
                        "height": m["media_details"]["height"]})
    lg = s.get("large", fu)
    md = s.get("medium", lg)
    return (f'<!-- wp:html -->\n<figure class="wp-block-image size-large">\n'
            f'<img src="{lg["source_url"]}" alt="{alt}" width="{lg["width"]}" height="{lg["height"]}" style="max-width:100%;height:auto;" '
            f'srcset="{md["source_url"]} {md["width"]}w, {lg["source_url"]} {lg["width"]}w, {fu["source_url"]} {fu["width"]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
            f'<figcaption style="font-size:0.8em;color:#888;">{cap}</figcaption>\n</figure>\n<!-- /wp:html -->')


def post(key):
    cfg = POSTS[key]
    html = (ROOT / cfg["html"]).read_text(encoding="utf-8")
    for ph, (fn, alt, cap) in cfg["images"].items():
        m = upload(ROOT / "images" / fn, "image/jpeg")
        html = html.replace(f"<!-- {ph} -->", figure(m, alt, cap))
        print(key, "media", ph, m["id"])
    assert "IMG_" not in html and "<hr" not in html
    ey = upload(ROOT / cfg["eyecatch"], "image/jpeg")
    print(key, "eyecatch media", ey["id"])
    r = requests.post(f"{U}/wp-json/wp/v2/posts", auth=A, json={
        "title": cfg["title"], "content": html, "slug": cfg["slug"], "status": "draft",
        "categories": cfg["categories"], "author": 2, "featured_media": ey["id"]}, timeout=120)
    r.raise_for_status()
    p = r.json()
    print("POST", key, p["id"], p["status"], p["slug"], f"{U}/?p={p['id']}")
    text = re.sub(r"<[^>]+>", "", html)
    print("chars", len(re.sub(r"\s", "", text)))


if __name__ == "__main__":
    for k in (sys.argv[1:] or list(POSTS)):
        post(k)
