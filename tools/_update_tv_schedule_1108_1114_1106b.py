# -*- coding: utf-8 -*-
"""11/6夜の追記(プレバト嶺亜・THE夜会森本・ヒルナンデスDAIKI/RYUJI)をWPに反映。本文のみ更新、status・タイトルは変えない。"""
import re, json, base64, urllib.request
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

ITEMS = [("CHOMO5", 582, "key_to_lit_tv_schedule_1108_1114.html"), ("AUDITION", 1292, "sixtones_tv_schedule_1108_1114.html"),
         ("KOIKEYS", 15407, "ko1keyz_tv_schedule_1108_1114.html"), ("KOIKEYS", 15408, "ko1keyz_tv_schedule_1108_1114_kr.html"),
         ("KOIKEYS", 15409, "ko1keyz_tv_schedule_1108_1114_en.html")]
for key, pid, fn in ITEMS:
    content = re.sub(r"<hr\s*/?>", "", open(REPO + rf"\articles\{fn}", encoding="utf-8").read()).strip()
    r = api(key, f"/wp-json/wp/v2/posts/{pid}", {"content": content})
    print(key, pid, r["status"], r["title"]["raw"], r["modified"])
