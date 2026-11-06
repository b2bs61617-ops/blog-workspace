# -*- coding: utf-8 -*-
"""トラジャ以外の11/8〜14 TV記事タイトルに【未】を戻す(2026-11-06 オシリ指示)。"""
import json, base64, urllib.request
REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"')
def api(key, path, body=None):
    base = env[f"WP_{key}_URL"].rstrip("/")
    auth = base64.b64encode(f"{env[f'WP_{key}_USERNAME']}:{env[f'WP_{key}_APP_PASSWORD']}".encode()).decode()
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method="POST" if data else "GET")
    req.add_header("Authorization", "Basic " + auth)
    if data: req.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(req).read().decode())
for key, pid in [("CHOMO5", 582), ("CHOMO2", 523), ("AUDITION", 1292), ("KOIKEYS", 15407), ("KOIKEYS", 15408), ("KOIKEYS", 15409)]:
    t = api(key, f"/wp-json/wp/v2/posts/{pid}?context=edit")["title"]["raw"]
    if not t.startswith("【未】"):
        t = "【未】" + t
        r = api(key, f"/wp-json/wp/v2/posts/{pid}", {"title": t})
    else:
        r = api(key, f"/wp-json/wp/v2/posts/{pid}?context=edit")
    print(key, pid, r["status"], r["title"]["raw"])
