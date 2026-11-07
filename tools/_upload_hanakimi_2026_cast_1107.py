# -*- coding: utf-8 -*-
"""令和版『花ざかりの君たちへ』キャスト比較記事をchomoand.com(トレンド速報)へ下書き投稿する(2026-11-07)。
usage: python tools/_upload_hanakimi_2026_cast_1107.py [--update-content]
状態は articles/hanakimi_2026_cast_posted.json に控え、再実行で重複投稿しない。
"""
import sys, os, json, base64, socket, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(REPO, "articles", "hanakimi_2026_cast_heisei_reiwa.html")
POSTED = os.path.join(REPO, "articles", "hanakimi_2026_cast_posted.json")
TITLE = "【未】花ざかりの君たちへ令和版キャスト！平成の小栗旬の役は誰？"
SLUG = "hanakimi-2026-cast-heisei-reiwa"
CATEGORIES = [37]  # 芸能・トレンド
AUTHORS = {"USER1": 3, "Tomoki": 4}  # docs/wordpress.md chomoand.com列
EYECATCH = os.path.join(REPO, "images", "hanakimi_2026_cast_eyecatch.png")
IMAGES = {
    "official": {"file": "images/hanakimi2026_cast_official.jpg",
                 "alt": "令和版ドラマ『花ざかりの君たちへ』メインキャスト12人のビジュアル",
                 "src": "https://x.com/TVGweb/status/2118826005930680724"},
    "fod2007": {"file": "images/hanakimi2007_cast_fod.jpg",
                "alt": "2007年版ドラマ『花ざかりの君たちへ〜イケメン♂パラダイス〜』のキャスト集合ビジュアル",
                "src": "https://x.com/fujitvplus/status/1456287754757677056"},
}

env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_TREND_USERNAME']}:{env['WP_TREND_APP_PASSWORD']}".encode()).decode()
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


state = json.load(open(POSTED, encoding="utf-8")) if os.path.exists(POSTED) else {}


def save():
    json.dump(state, open(POSTED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def upload(path, ctype, alt):
    fn = os.path.basename(path)
    m = req("/wp-json/wp/v2/media", open(path, "rb").read(),
            {"Content-Type": ctype, "Content-Disposition": f'attachment; filename="{fn}"'})
    jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": alt})
    return m["id"]


def build_html():
    html = open(ART, encoding="utf-8").read()
    for name, im in IMAGES.items():
        key = "img:" + name
        if key not in state:
            state[key] = upload(os.path.join(REPO, im["file"]), "image/jpeg", im["alt"])
            save()
        m = req(f"/wp-json/wp/v2/media/{state[key]}", method="GET")
        sz = m["media_details"].get("sizes", {})
        full = {"source_url": m["source_url"], "width": m["media_details"]["width"], "height": m["media_details"]["height"]}
        large = sz.get("large", full)
        mid = sz.get("medium_large", sz.get("medium", large))
        fig = ("<!-- wp:html -->\n<figure class=\"wp-block-image size-large\">\n"
               f'<img src="{large["source_url"]}" alt="{im["alt"]}" width="{large["width"]}" height="{large["height"]}" style="max-width:100%;height:auto;" loading="lazy"\n'
               f'  srcset="{mid["source_url"]} {mid["width"]}w, {large["source_url"]} {large["width"]}w, {full["source_url"]} {full["width"]}w" sizes="(max-width: 768px) 100vw, 768px">\n'
               f'<figcaption style="font-size:0.8em;color:#888;">出典:<a href="{im["src"]}" target="_blank" rel="noopener">{im["src"]}</a></figcaption>\n'
               "</figure>\n<!-- /wp:html -->\n")
        html = html.replace("{{IMG:" + name + "}}", fig)
    assert "{{IMG:" not in html
    return html


def main():
    html = build_html()
    if "post" in state:
        if "--update-content" in sys.argv:
            jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"content": html, "status": "draft"})
            print("content updated", state["post"])
        else:
            print("already posted", state["post"])
    else:
        p = jpost("/wp-json/wp/v2/posts", {"title": TITLE, "content": html, "slug": SLUG, "status": "draft",
                                           "categories": CATEGORIES, "author": AUTHOR})
        state["post"] = p["id"]
        save()
        print("draft", p["id"])
    if "eyecatch" not in state:
        state["eyecatch"] = upload(EYECATCH, "image/png", "花ざかりの君たちへ令和版キャスト 平成版と比較")
        save()
        jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"featured_media": state["eyecatch"]})
    p = req(f"/wp-json/wp/v2/posts/{state['post']}?context=edit", method="GET")
    print(p["id"], p["status"], p["author"], p["categories"], p["featured_media"], p["title"]["raw"])
    print(f"{BASE}/?p={p['id']}")


if __name__ == "__main__":
    main()
