# -*- coding: utf-8 -*-
"""Split the SixTONES "すとらじ" outfits draft (chomoand-0.com ID1341) into 4 member articles (2026-11-06).

usage: python tools/_upload_sixtones_sutoraji_split_1106.py
- hokuto reuses draft 1341 (title/slug/categories/content/eyecatch are overwritten, status stays draft).
- morimoto/kochi/juri are created as new drafts.
- Body = articles/sixtones_sutoraji_split_1106/{key}.html with {{VIDEO}}, {{RELATED}}, {{IMG:name}}, {{LINK:key}} filled in.
- Honorifics are applied with tools/honorific.py before posting.
- IDs (posts/media) are kept in articles/sixtones_sutoraji_split_1106/posted.json, so re-running updates instead of duplicating.
"""
import os, sys, json, base64, socket, subprocess, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(REPO, "articles", "sixtones_sutoraji_split_1106")
POSTED = os.path.join(DIR, "posted.json")
SRC = "https://www.youtube.com/watch?v=_vikLYJCfaE"
AUTHORS = {"USER1": 2, "Tomoki": 1, "Yuka-MacBook-NEO": 1}

ARTICLES = [
    {"key": "hokuto", "title": "【未】松村北斗のジャージはどこの？すとらじ着用adidas×NIGOを特定！",
     "slug": "matsumura-hokuto-sutoraji-adidas", "categories": [15, 18],
     "anchor": "松村北斗がすとらじで着ていたadidas×NIGOのジャージを調査した記事"},
    {"key": "morimoto", "title": "【未】森本慎太郎のパーカーはどこの？すとらじ着用TRIBALを特定！",
     "slug": "morimoto-shintaro-sutoraji-tribal", "categories": [15, 20],
     "anchor": "森本慎太郎がすとらじで着ていたTRIBAL×Mister Cartoonのパーカーを調査した記事"},
    {"key": "kochi", "title": "【未】髙地優吾のジャケットはどこの？すとらじ着用NEW ERAを特定！",
     "slug": "kochi-yugo-sutoraji-newera", "categories": [15, 19],
     "anchor": "髙地優吾がすとらじで着ていたNEW ERAのトラックジャケットを調査した記事"},
    {"key": "juri", "title": "【未】田中樹のブレスレットはどこの？すとらじ着用のティファニーを調査！",
     "slug": "tanaka-juri-sutoraji-tiffany", "categories": [15, 21],
     "anchor": "田中樹がすとらじで着けていたティファニー タイタンのブレスレットを調査した記事"},
]
IMAGES = {
    "all": "すとらじで近況報告 SixTONES6人がトークする様子",
    "hokuto": "adidasサッカー日本代表コレクションのトラックジャケットを着た松村北斗",
    "hokuto2": "ピンク×緑のジャージに赤いメッシュベストを重ねた松村北斗",
    "morimoto": "TRIBAL×Mister Cartoonのジップパーカーを着た森本慎太郎",
    "morimoto2": "胸にTribal Mister Cartoonの刺しゅうが入った森本慎太郎のパーカー",
    "kochi": "NEW ERAのネイビーのトラックジャケットを着た髙地優吾",
    "kochi2": "左胸に丸い革パッチが付いた髙地優吾のトラックジャケット",
    "juri": "田中樹が着けていたゴールドのリンクブレスレット",
    "juri2": "トゲのパーツが見える田中樹のブレスレット",
}
NON_MEMBER_NAMES = "大橋高歩,NIGO,ファレル・ウィリアムス,ボビー・ルイス,ジョーイ,マーク・マチャド,エミネム,50セント,ビヨンセ,コービー・ブライアント"

env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_AUDITION_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_AUDITION_USERNAME']}:{env['WP_AUDITION_APP_PASSWORD']}".encode()).decode()
host = socket.gethostname().split(".")[0]
AUTHOR = next((v for k, v in AUTHORS.items() if host.lower().startswith(k.lower())), None)
if AUTHOR is None:
    sys.exit(f"hostname {host} の投稿者がdocs/wordpress.mdの表に無いワン")


def req(path, data=None, headers=None, method="POST"):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode('utf-8', 'ignore')[:500]}")


def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})


posted = json.load(open(POSTED, encoding="utf-8"))


def save():
    json.dump(posted, open(POSTED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def media_id(name, path, alt):
    key = f"img:{name}"
    if key not in posted:
        fn = os.path.basename(path)
        m = req("/wp-json/wp/v2/media", open(path, "rb").read(),
                {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{fn}"'})
        jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": alt})
        posted[key] = m["id"]
        save()
    return posted[key]


def figure(name):
    mid = media_id(name, os.path.join(REPO, "images", f"sixtones_sutoraji_{name}.jpg"), IMAGES[name])
    m = req(f"/wp-json/wp/v2/media/{mid}", method="GET")
    sz = m["media_details"].get("sizes", {})
    full = {"source_url": m["source_url"], "width": m["media_details"]["width"], "height": m["media_details"]["height"]}
    large = sz.get("large", full)
    mid_ = sz.get("medium_large", sz.get("medium", large))
    return ("<!-- wp:html -->\n<figure class=\"wp-block-image size-large\">\n"
            f'<img src="{large["source_url"]}" alt="{IMAGES[name]}" width="{large["width"]}" height="{large["height"]}" style="max-width:100%;height:auto;" loading="lazy"\n'
            f'  srcset="{mid_["source_url"]} {mid_["width"]}w, {large["source_url"]} {large["width"]}w, {full["source_url"]} {full["width"]}w" sizes="(max-width: 768px) 100vw, 768px">\n'
            f'<figcaption style="font-size:0.8em;color:#888;">出典:<a href="{SRC}" target="_blank" rel="noopener">{SRC}</a></figcaption>\n'
            "</figure>\n<!-- /wp:html -->\n")


def main():
    # 1) make sure every article has a post ID (new drafts get a placeholder body first)
    for a in ARTICLES:
        if a["key"] not in posted:
            p = jpost("/wp-json/wp/v2/posts", {"title": a["title"], "content": "", "slug": a["slug"],
                                               "status": "draft", "categories": a["categories"], "author": AUTHOR})
            posted[a["key"]] = p["id"]
            save()
            print(f"created draft {p['id']} ({a['key']})")

    video = open(os.path.join(DIR, "common_video.html"), encoding="utf-8").read()
    related_tpl = open(os.path.join(DIR, "common_related.html"), encoding="utf-8").read()
    for a in ARTICLES:
        items = "\n".join(f'<li><a href="{BASE}/?p={posted[o["key"]]}">{o["anchor"]}</a></li>'
                          for o in ARTICLES if o["key"] != a["key"])
        html = open(os.path.join(DIR, f"{a['key']}.html"), encoding="utf-8").read()
        html = html.replace("{{VIDEO}}", video).replace("{{RELATED}}", related_tpl.replace("{{RELATED_ITEMS}}", items))
        tmp = os.path.join(DIR, f"_built_{a['key']}.html")
        open(tmp, "w", encoding="utf-8").write(html)
        hon = [sys.executable, os.path.join(REPO, "tools", "honorific.py")]
        subprocess.run(hon + ["fix", "--group", "sixtones", "--names", NON_MEMBER_NAMES, tmp], check=True)
        r = subprocess.run(hon + ["check", "--group", "sixtones", "--names", NON_MEMBER_NAMES, tmp],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.stdout.strip():
            print(f"[honorific check {a['key']}]\n{r.stdout}")
        html = open(tmp, encoding="utf-8").read()
        for name in IMAGES:
            tag = "{{IMG:" + name + "}}"
            if tag in html:
                html = html.replace(tag, figure(name))
        open(tmp, "w", encoding="utf-8").write(html)
        assert "{{" not in html, f"placeholder left in {a['key']}"
        ec = media_id(f"ec_{a['key']}", os.path.join(REPO, "images", f"sixtones_sutoraji_{a['key']}_eyecatch.jpg"),
                      a["title"].replace("【未】", ""))
        jpost(f"/wp-json/wp/v2/posts/{posted[a['key']]}", {
            "title": a["title"], "content": html, "slug": a["slug"], "status": "draft",
            "categories": a["categories"], "author": AUTHOR, "featured_media": ec})
        print(f"updated {posted[a['key']]} {a['key']}")
    for a in ARTICLES:
        print(f"{BASE}/?p={posted[a['key']]}  {a['title']}")


if __name__ == "__main__":
    main()
