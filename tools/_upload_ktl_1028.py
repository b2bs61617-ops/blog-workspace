# -*- coding: utf-8 -*-
"""Upload the KEY TO LIT articles built by _build_ktl_1028.py to chomoand-5.site as drafts.

usage: python tools/_upload_ktl_1028.py [--update-content]
--update-content: 投稿済みの下書きの本文だけを articles/ の最新HTMLで上書きする(タイトル・スラッグは触らない)。
Reads articles/ktl_1028_manifest.json, posts each article as a draft with its eyecatch
(images/ktl_{key}_eyecatch.jpg), then replaces the {{LINK:key}} placeholders with the new
draft IDs. Already-posted keys are recorded in articles/ktl_1028_posted.json so a re-run
skips them instead of creating duplicates.
"""
import sys, os, re, json, base64, socket, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO, "articles", "ktl_1028_manifest.json")
POSTED = os.path.join(REPO, "articles", "ktl_1028_posted.json")

# docs/wordpress.md の投稿者表(chomoand-5.site列)
AUTHORS = {"USER1": 2, "Tomoki": 1}

env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
if not env.get("WP_CHOMO5_APP_PASSWORD"):
    sys.exit("このPCの.envにWP_CHOMO5_*が無いワン。設定済みのPCで実行してワン")
BASE = env["WP_CHOMO5_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_CHOMO5_USERNAME']}:{env['WP_CHOMO5_APP_PASSWORD']}".encode()).decode()
host = socket.gethostname().split(".")[0]
AUTHOR = next((v for k, v in AUTHORS.items() if host.lower().startswith(k.lower())), None)
if AUTHOR is None:
    sys.exit(f"hostname {host} の投稿者がdocs/wordpress.mdの表に無いワン。表に追記してから実行してワン")


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


def main():
    articles = json.load(open(MANIFEST, encoding="utf-8"))
    posted = json.load(open(POSTED, encoding="utf-8")) if os.path.exists(POSTED) else {}

    update_only = "--update-content" in sys.argv
    for a in articles:
        if update_only:
            break
        if a["key"] in posted:
            print(f"skip {a['key']} (already draft {posted[a['key']]})")
            continue
        html = open(os.path.join(REPO, a["file"]), encoding="utf-8").read()
        post = jpost("/wp-json/wp/v2/posts", {
            "title": a["title"], "content": html, "slug": a["slug"], "status": "draft",
            "categories": a["categories"], "author": AUTHOR})
        img = os.path.join(REPO, "images", f"ktl_{a['key']}_eyecatch.jpg")
        media = req("/wp-json/wp/v2/media", open(img, "rb").read(),
                    {"Content-Type": "image/jpeg",
                     "Content-Disposition": f'attachment; filename="ktl_{a["key"]}_eyecatch.jpg"'})
        jpost(f"/wp-json/wp/v2/media/{media['id']}", {"alt_text": a["title"]})
        jpost(f"/wp-json/wp/v2/posts/{post['id']}", {"featured_media": media["id"]})
        posted[a["key"]] = post["id"]
        json.dump(posted, open(POSTED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"draft {post['id']} media {media['id']} {a['title']}")

    # 新記事どうしのリンクを実IDに置き換える(下書きなので ?p=ID 形式)
    for a in articles:
        html = open(os.path.join(REPO, a["file"]), encoding="utf-8").read()
        if "{{LINK:" not in html:
            continue
        fixed = re.sub(r"\{\{LINK:(\w+)\}\}", lambda m: f"{BASE}/?p={posted[m.group(1)]}", html)
        jpost(f"/wp-json/wp/v2/posts/{posted[a['key']]}", {"content": fixed, "status": "draft"})
        print(f"links fixed {posted[a['key']]}")

    for a in articles:
        print(f"{BASE}/?p={posted[a['key']]}  {a['title']}")


if __name__ == "__main__":
    main()
