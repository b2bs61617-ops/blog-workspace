# -*- coding: utf-8 -*-
"""Patch the reciprocal placeholder links between the KR pair and EN pair of utawari drafts."""
import json, base64, urllib.request

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


RA_KR_ID, BA_KR_ID = 12989, 12992
RA_EN_ID, BA_EN_ID = 12990, 12993
RA_KR_URL = f"{BASE}/ko/ko1keyz-run-again-utawari-kr-{RA_KR_ID}"
BA_KR_URL = f"{BASE}/ko/ko1keyz-black-angel-utawari-kr-{BA_KR_ID}"
RA_EN_URL = f"{BASE}/en/ko1keyz-run-again-utawari-en-{RA_EN_ID}"
BA_EN_URL = f"{BASE}/en/ko1keyz-black-angel-utawari-en-{BA_EN_ID}"

ra_kr_old = get_placeholder_li(r"\articles\ko1keyz_run_again_utawari_kr.md", "BLACK ANGEL KR URL PLACEHOLDER")
ba_kr_old = get_placeholder_li(r"\articles\ko1keyz_black_angel_utawari_kr.md", "Run Again KR URL PLACEHOLDER")
ra_en_old = get_placeholder_li(r"\articles\ko1keyz_run_again_utawari_en.md", "BLACK ANGEL EN URL PLACEHOLDER")
ba_en_old = get_placeholder_li(r"\articles\ko1keyz_black_angel_utawari_en.md", "Run Again EN URL PLACEHOLDER")

BA_KR_TITLE = "\uac00\uc0ac \ubd84\ubc30(6\uc778 ver.) \ud30c\ud2b8 \ubd84\ubc30 \uc815\ub9ac \uae00"
BA_KR_TITLE = "\u300cBLACK ANGEL\u300d(6\uc778 ver.) \ud30c\ud2b8 \ubd84\ubc30\ub97c \uc815\ub9ac\ud55c \uae00"
RA_KR_TITLE = "KO1KEYZ 'Run Again' \ud30c\ud2b8 \ubd84\ubc30\ub294? 12\uba85 \uc804\uc6d0 \ucd1d\uc815\ub9ac!"
BA_EN_TITLE = 'Who Sings What in KO1KEYZ\'s "BLACK ANGEL"? The 6-Member Parts!'
RA_EN_TITLE = 'Who Sings What in KO1KEYZ\'s "Run Again"? All 12 Members\' Parts!'

JOBS = [
    (RA_KR_ID, ra_kr_old, f'<li><a href="{BA_KR_URL}" target="_blank" rel="noopener">{BA_KR_TITLE}</a></li>'),
    (BA_KR_ID, ba_kr_old, f'<li><a href="{RA_KR_URL}" target="_blank" rel="noopener">{RA_KR_TITLE}</a></li>'),
    (RA_EN_ID, ra_en_old, f'<li><a href="{BA_EN_URL}" target="_blank" rel="noopener">{BA_EN_TITLE}</a></li>'),
    (BA_EN_ID, ba_en_old, f'<li><a href="{RA_EN_URL}" target="_blank" rel="noopener">{RA_EN_TITLE}</a></li>'),
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
    print(f"patched post {pid} OK -> {new_li[:90]}...")
