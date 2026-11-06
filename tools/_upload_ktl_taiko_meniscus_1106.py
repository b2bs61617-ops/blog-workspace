# -*- coding: utf-8 -*-
"""Post the Sasaki Taiko meniscus re-tear article to chomoand-5.site as a draft (2026-11-06)."""
import os, json, base64, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TITLE = "【佐々木大光】半月板再断裂はなぜ？デビューへの影響や復帰時期は？"
SLUG = "sasaki-taiko-meniscus-retear"
HTML = os.path.join(REPO, "articles", "ktl_taiko_meniscus_retear.html")
IMG = os.path.join(REPO, "images", "ktl_taiko_meniscus_eyecatch.jpg")

env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    line = line.strip()
    if line.startswith("WP_CHOMO5_") and "=" in line:
        k, v = line.split("=", 1)
        env[k] = v.strip().strip('"')
BASE = env["WP_CHOMO5_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_CHOMO5_USERNAME']}:{env['WP_CHOMO5_APP_PASSWORD']}".encode()).decode()


def req(path, data, headers):
    r = urllib.request.Request(BASE + path, data=data, method="POST")
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in headers.items():
        r.add_header(k, v)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})


post = jpost("/wp-json/wp/v2/posts", {"title": TITLE, "content": open(HTML, encoding="utf-8").read(),
                                     "slug": SLUG, "status": "draft", "categories": [4, 10], "author": 2})
media = req("/wp-json/wp/v2/media", open(IMG, "rb").read(),
            {"Content-Type": "image/jpeg", "Content-Disposition": 'attachment; filename="ktl_taiko_meniscus_eyecatch.jpg"'})
jpost(f"/wp-json/wp/v2/media/{media['id']}", {"alt_text": TITLE})
jpost(f"/wp-json/wp/v2/posts/{post['id']}", {"featured_media": media["id"]})
print(f"draft {post['id']} media {media['id']} {BASE}/?p={post['id']}")
