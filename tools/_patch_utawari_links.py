# -*- coding: utf-8 -*-
"""Patch the reciprocal placeholder links between the two utawari articles with real URLs.
Reads the exact placeholder <li> line straight out of the local .md source (avoids
hand-retyping Japanese text into this script, which caused a mismatch previously)."""
import json, base64, urllib.request, re

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip().strip('"')

U = env["WP_KOIKEYS_USERNAME"]; P = env["WP_KOIKEYS_APP_PASSWORD"]; BASE = env["WP_KOIKEYS_URL"]
AUTH = base64.b64encode(f"{U}:{P}".encode()).decode()


def api(path, body=None, method="GET"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Authorization", "Basic " + AUTH)
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


def get_placeholder_li(md_path, marker):
    text = open(REPO + md_path, encoding="utf-8").read()
    for line in text.split("\n"):
        if marker in line and line.strip().startswith("<li>"):
            return line.strip()
    raise SystemExit(f"placeholder line with marker {marker!r} not found in {md_path}")


RUN_AGAIN_ID = 12980
BLACK_ANGEL_ID = 12983
RUN_AGAIN_URL = f"{BASE}/ko1keyz-run-again-utawari-{RUN_AGAIN_ID}"
BLACK_ANGEL_URL = f"{BASE}/ko1keyz-black-angel-utawari-{BLACK_ANGEL_ID}"

run_again_old_li = get_placeholder_li(r"\articles\ko1keyz_run_again_utawari.md", "BLACK ANGEL\u6b4c\u5272\u308a\u8a18\u4e8bURL")
black_angel_old_li = get_placeholder_li(r"\articles\ko1keyz_black_angel_utawari.md", "Run Again\u6b4c\u5272\u308a\u8a18\u4e8bURL")

RUN_AGAIN_TITLE = "KO1KEYZ\u300cRun Again\u300d\u306e\u6b4c\u5272\u308a\u306f\uff1f\u5168\uff11\uff12\u4eba\u306e\u30d1\u30fc\u30c8\uff01"
BLACK_ANGEL_TITLE = "KO1KEYZ\u300cBLACK ANGEL\u300d(6\u4eba ver.)\u306e\u6b4c\u5272\u308a\u3092\u307e\u3068\u3081\u305f\u8a18\u4e8b"

JOBS = [
    (RUN_AGAIN_ID, run_again_old_li, f'<li><a href="{BLACK_ANGEL_URL}" target="_blank" rel="noopener">{BLACK_ANGEL_TITLE}</a></li>'),
    (BLACK_ANGEL_ID, black_angel_old_li, f'<li><a href="{RUN_AGAIN_URL}" target="_blank" rel="noopener">{RUN_AGAIN_TITLE}</a></li>'),
]

for pid, old_li, new_li in JOBS:
    cur = api(f"/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content,slug")
    raw = cur["content"]["raw"]
    if old_li not in raw:
        print(f"!! placeholder not found in post {pid} (len={len(raw)})")
        print("looked for:", old_li)
        continue
    raw2 = raw.replace(old_li, new_li)
    api(f"/wp-json/wp/v2/posts/{pid}", {"content": raw2, "status": "draft"}, "POST")
    print(f"patched post {pid} OK -> {new_li[:80]}...")
