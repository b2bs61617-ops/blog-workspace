# -*- coding: utf-8 -*-
"""Add an Onishi Ryusei photo (modelpress official X post) and a closing comment to chomoand.com draft 13045 (2026-11-09, Yuka request)."""
import os, sys, json, base64, urllib.request
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVE_ENV = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env")
env = {}
for line in open(DRIVE_ENV, encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"')
BASE = env["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_TREND_USERNAME']}:{env['WP_TREND_APP_PASSWORD']}".encode()).decode()
POST_ID = 13045
SRC_URL = "https://x.com/modelpress/status/2097965247588126879"
HTML_PATH = os.path.join(REPO, "articles", "trend_furusawa_onishi_rumor_1109.html")
IMG = os.path.join(REPO, "images", "x", "onishi_ryusei_anteprima_modelpress.jpg")

def call(path, data=None, headers=None, method="GET"):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items(): r.add_header(k, v)
    return json.loads(urllib.request.urlopen(r, timeout=120).read().decode("utf-8"))

mode = sys.argv[1]
if mode == "check":
    p = call(f"/wp-json/wp/v2/posts/{POST_ID}?context=edit")
    remote = p["content"]["raw"].strip(); local = open(HTML_PATH, encoding="utf-8").read().strip()
    print("status", p["status"], "| same as local:", remote == local, len(remote), len(local))
elif mode == "upload":
    m = call("/wp-json/wp/v2/media", open(IMG, "rb").read(),
             {"Content-Type": "image/jpeg", "Content-Disposition": 'attachment; filename="onishi_ryusei_anteprima_modelpress.jpg"'}, "POST")
    call(f"/wp-json/wp/v2/media/{m['id']}", json.dumps({"alt_text": "大西流星"}).encode(), {"Content-Type": "application/json"}, "POST")
    s = m["media_details"]["sizes"]
    print(json.dumps({"id": m["id"], "sizes": {k: [v["source_url"], v["width"], v["height"]] for k, v in s.items()},
                      "full": [m["source_url"], m["media_details"]["width"], m["media_details"]["height"]]}, ensure_ascii=False, indent=1))
elif mode == "push":
    html = open(HTML_PATH, encoding="utf-8").read()
    p = call(f"/wp-json/wp/v2/posts/{POST_ID}", json.dumps({"content": html, "status": "draft"}).encode(), {"Content-Type": "application/json"}, "POST")
    print("updated", p["id"], p["status"], f"{BASE}/?p={POST_ID}&preview=true")
