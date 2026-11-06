# -*- coding: utf-8 -*-
"""11/6リライト分をWPに反映(本文更新+下書きの【未】外し。statusは変えない)。"""
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

ITEMS = [("CHOMO4", 2348, "travis_japan_tv_schedule_1108_1114.html"), ("CHOMO5", 582, "key_to_lit_tv_schedule_1108_1114.html"),
         ("CHOMO2", 523, "snowman_tv_schedule_1108_1114.html"), ("AUDITION", 1292, "sixtones_tv_schedule_1108_1114.html"),
         ("KOIKEYS", 15407, "ko1keyz_tv_schedule_1108_1114.html"), ("KOIKEYS", 15408, "ko1keyz_tv_schedule_1108_1114_kr.html"),
         ("KOIKEYS", 15409, "ko1keyz_tv_schedule_1108_1114_en.html")]
for key, pid, fn in ITEMS:
    cur = api(key, f"/wp-json/wp/v2/posts/{pid}?context=edit")
    content = re.sub(r"<hr\s*/?>", "", open(REPO + rf"\articles\{fn}", encoding="utf-8").read()).strip()
    body = {"content": content}
    t = cur["title"]["raw"]
    if t.startswith("【未】"):
        body["title"] = t[3:]
    r = api(key, f"/wp-json/wp/v2/posts/{pid}", body)
    print(key, pid, r["status"], r["title"]["raw"], r["modified"])
