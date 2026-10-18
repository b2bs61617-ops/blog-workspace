# -*- coding: utf-8 -*-
"""Upload draft: KEY TO LIT (chomoand-5.site) magazine appearances 2026-10."""
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


def req(path, data, headers):
    r = urllib.request.Request(BASE + path, data=data, method="POST")
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in headers.items():
        r.add_header(k, v)
    with urllib.request.urlopen(r) as resp:
        return json.loads(resp.read().decode("utf-8"))


fn = "key_to_lit_magazine_appearances_202610_eyecatch.jpg"
media = req("/wp-json/wp/v2/media", open(REPO + rf"\images\{fn}", "rb").read(),
            {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{fn}"'})["id"]
content = re.sub(r"<hr\s*/?>", "", open(REPO + r"\articles\key_to_lit_magazine_appearances_202610.html", encoding="utf-8").read()).strip()
p = req("/wp-json/wp/v2/posts", json.dumps({
    "title": "キテレツの雑誌掲載は？表紙号の発売日と予約方法まとめ！",
    "slug": "key-to-lit-magazine-appearances-2026-autumn",
    "content": content, "status": "draft",
    "categories": [4, 6, 7, 8, 9, 10], "author": 2, "featured_media": media,
}).encode(), {"Content-Type": "application/json"})
print(p["id"], p["slug"], p["link"], media)
