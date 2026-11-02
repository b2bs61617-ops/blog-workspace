# -*- coding: utf-8 -*-
"""One-off: upload 5 drafts (逆引きランキング第2弾 2026-10-31 summary + 4 item articles) to chomoand-4.blog."""
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
VID = "https://www.youtube.com/watch?v=-F7LZTim60c"
SRC = f'<a href="{VID}" target="_blank" rel="noopener">Travis Japan公式YouTube「【ランキング】今度は７人で逆引き！」</a>'

POSTS = {
    "summary": dict(title="【未】【逆引きランキング】トラジャ第2弾の結果は？お題と順位まとめ！", slug="travis-japan-gyakubiki-ranking-2-results",
                    cats=[3], html="travis_ranking2_1031_summary.html", eye="tj_rank2_1031_summary_eyecatch_canva.jpg", imgs={
                        "IMG_ALL": ("tj_rank2_1031_all7.jpg", "逆引きランキング第2弾で7人の名前が書かれたフリップを並べたTravis Japan", "27:05ごろ"),
                        "IMG_BOARD": ("tj_rank2_1031_board.jpg", "第2ラウンドで決まった1位しずから7位しめまでの順位", "9:05ごろ")}),
    "yoshizawa": dict(title="【未】吉澤閑也のTAIPEIのTシャツはどこの？クロムハーツと判明！", slug="yoshizawa-shizuya-chrome-hearts-taipei-pocket-tee",
                      cats=[3, 12], html="travis_ranking2_1031_yoshizawa.html", eye="tj_rank2_1031_yoshizawa_eyecatch_canva.jpg", imgs={
                          "IMG_FRONT": ("shizuya_rank1031_front.jpg", "黒のポケットTシャツを着て笑う吉澤閑也", "4:20ごろ"),
                          "IMG_POCKET": ("shizuya_rank1031_pocket.jpg", "吉澤閑也のTシャツの胸ポケットのホースシューロゴ", "4:20ごろ、胸ポケットを拡大"),
                          "IMG_BACK": ("shizuya_rank1031_back_taipei.jpg", "吉澤閑也のTシャツの背中のホースシューとTAIPEIの文字", "8:05ごろ")}),
    "nakamura": dict(title="【未】中村海人のジャージはどこの？アクネ ストゥディオズと判明！", slug="nakamura-kaito-acne-studios-track-jacket",
                     cats=[3, 10], html="travis_ranking2_1031_nakamura.html", eye="tj_rank2_1031_nakamura_eyecatch_canva.jpg", imgs={
                         "IMG_FRONT": ("umi_rank1031_front.jpg", "黒のトラックジャケットに黒のキャップの中村海人", "16:20ごろ"),
                         "IMG_BACK": ("umi_rank1031_jacket_back.jpg", "中村海人のトラックジャケットの背中のAcne Studiosのロゴ", "8:05ごろ"),
                         "IMG_CAP": ("umi_rank1031_cap.jpg", "中村海人のキャップの赤いセメタリークロス", "4:20ごろ、キャップを拡大")}),
    "matsukura": dict(title="【未】松倉海斗のボーダーポロはどこの？セリーヌと判明！", slug="matsukura-kaito-celine-triomphe-striped-polo",
                      cats=[3, 6], html="travis_ranking2_1031_matsukura.html", eye="tj_rank2_1031_matsukura_eyecatch_canva.jpg", imgs={
                          "IMG_POLO": ("matchu_rank1031_polo.jpg", "緑と黄色のボーダーのポロシャツを着て腕を組む松倉海斗", "1:50ごろ"),
                          "IMG_LOGO": ("matchu_rank1031_triomphe.jpg", "松倉海斗のポロシャツの胸のトリオンフの刺しゅう", "1:50ごろ、胸元を拡大")}),
    "matsuda": dict(title="【未】松田元太のブラジルのシャツはどこの？ジョーダンと判明！", slug="matsuda-genta-jordan-brazil-strike-top",
                    cats=[3, 7], html="travis_ranking2_1031_matsuda.html", eye="tj_rank2_1031_matsuda_eyecatch_canva.jpg", imgs={
                        "IMG_JERSEY": ("genta_rank1031_jersey.jpg", "ジョーダン×ブラジル代表の黒のシャツを着た松田元太", "13:20ごろ"),
                        "IMG_CAP": ("genta_rank1031_cap.jpg", "ベージュのキャップを後ろ向きにかぶりフリップを持つ松田元太", "15:05ごろ")}),
}
ID_KEYS = {"SUMMARY_ID": "summary", "YOSHIZAWA_ID": "yoshizawa", "NAKAMURA_ID": "nakamura", "MATSUKURA_ID": "matsukura", "MATSUDA_ID": "matsuda"}


def upload(path):
    r = requests.post(f"{U}/wp-json/wp/v2/media", auth=A, data=path.read_bytes(), headers={
        "Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{path.name}"'}, timeout=180)
    r.raise_for_status()
    return r.json()


def fig(m, alt, cap):
    s = m["media_details"]["sizes"]
    lg = s.get("large", s["full"]); md = s.get("medium", lg); fu = s["full"]
    return (f'<!-- wp:html -->\n<figure class="wp-block-image size-large">\n'
            f'<img src="{lg["source_url"]}" alt="{alt}" width="{lg["width"]}" height="{lg["height"]}" style="max-width:100%;height:auto;" '
            f'srcset="{md["source_url"]} {md["width"]}w, {lg["source_url"]} {lg["width"]}w, {fu["source_url"]} {fu["width"]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
            f'<figcaption style="font-size:0.8em;color:#888;">出典:{SRC}({cap})</figcaption>\n</figure>\n<!-- /wp:html -->')


ids, htmls = {}, {}
for key, d in POSTS.items():
    html = (ROOT / "articles" / d["html"]).read_text(encoding="utf-8")
    for ph, (fn, alt, cap) in d["imgs"].items():
        m = upload(ROOT / "images" / fn)
        html = html.replace(f"<!-- {ph} -->", fig(m, alt, cap))
    assert "<!-- IMG_" not in html and "<hr" not in html
    ey = upload(ROOT / "images" / d["eye"])
    r = requests.post(f"{U}/wp-json/wp/v2/posts", auth=A, json={
        "title": d["title"], "content": html, "slug": d["slug"], "status": "draft",
        "categories": d["cats"], "author": 2, "featured_media": ey["id"]}, timeout=180)
    r.raise_for_status()
    ids[key] = r.json()["id"]; htmls[key] = html
    print("POST", key, ids[key])

for key, html in htmls.items():
    new = html
    for ph, k in ID_KEYS.items():
        new = new.replace(ph, str(ids[k]))
    if new != html:
        r = requests.post(f"{U}/wp-json/wp/v2/posts/{ids[key]}", auth=A, json={"content": new, "status": "draft"}, timeout=180)
        r.raise_for_status()
        print("UPDATED", key, r.json()["status"])
    text = re.sub(r"<[^>]+>", "", new)
    print(key, ids[key], f"{U}/?p={ids[key]}", "chars", len(re.sub(r"\s", "", text)), "leftover_ph", [p for p in ID_KEYS if p in new])
