# -*- coding: utf-8 -*-
"""Post the Furusawa Risa x Onishi Ryusei marriage-plan rumor fact-check to chomoand.com (trend blog) as a draft (2026-11-09).
Category 37 (芸能・トレンド), author 3 (momo)."""
import os, json, base64, urllib.request
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"')
BASE = env["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_TREND_USERNAME']}:{env['WP_TREND_APP_PASSWORD']}".encode()).decode()
POSTED = os.path.join(REPO, "articles", "trend_furusawa_onishi_rumor_1109_posted.json")

def req(path, data, headers):
    r = urllib.request.Request(BASE + path, data=data, method="POST")
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in headers.items(): r.add_header(k, v)
    return json.loads(urllib.request.urlopen(r, timeout=120).read().decode("utf-8"))

def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})

if os.path.exists(POSTED):
    raise SystemExit(f"already posted: {open(POSTED).read()}")
html = open(os.path.join(REPO, "articles", "trend_furusawa_onishi_rumor_1109.html"), encoding="utf-8").read()
title = "【未】古澤里紗と大西流星の結婚計画は本当？流出投稿の真相を検証"
base = title.replace("【未】", ""); assert title.startswith("【未】") and len(base) <= 35, len(base)
post = jpost("/wp-json/wp/v2/posts", {"title": title, "content": html, "slug": "furusawa-risa-onishi-ryusei-rumor-fact-check",
                                      "status": "draft", "categories": [37], "author": 3})
img = os.path.join(REPO, "images", "trend_furusawa_onishi_rumor_eyecatch.png")
m = req("/wp-json/wp/v2/media", open(img, "rb").read(),
        {"Content-Type": "image/png", "Content-Disposition": 'attachment; filename="trend_furusawa_onishi_rumor_eyecatch.png"'})
jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": title.replace("【未】", "")})
jpost(f"/wp-json/wp/v2/posts/{post['id']}", {"featured_media": m["id"], "status": "draft"})
json.dump({"post": post["id"], "media": m["id"]}, open(POSTED, "w"))
print(f"draft {post['id']} media {m['id']} {BASE}/?p={post['id']}")
