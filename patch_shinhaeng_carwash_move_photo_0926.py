# -*- coding: utf-8 -*-
"""SHINHAENG洗車場記事(JP13716/KR13717/EN13718・下書き)の公式写真をプロフィール節から導入文の直下へ移動する。"""
import base64, json, re, sys
from pathlib import Path
import requests
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent
env = {}
for l in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    l = l.strip()
    if "=" in l and not l.startswith("#"):
        k, v = l.split("=", 1); env[k.strip()] = v.strip().strip('"')
HA = {"Authorization": "Basic " + base64.b64encode(f"{env['WP_KOIKEYS_USERNAME']}:{env['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()}
W = env["WP_KOIKEYS_URL"].rstrip("/") + "/wp-json/wp/v2"
FIG = re.compile(r'\n\n<!-- wp:html -->\n<figure class="wp-block-image size-large">\n<img src="[^"]*shinhaeng_official_profile_photo.*?</figure>\n<!-- /wp:html -->', re.S)
END_P = "<!-- /wp:paragraph -->"

for pid in (13716, 13717, 13718):
    d = requests.get(f"{W}/posts/{pid}", params={"context": "edit"}, headers=HA).json()
    assert d["status"] == "draft", d["status"]
    raw = d["content"]["raw"]
    ms = FIG.findall(raw)
    assert len(ms) == 1, (pid, len(ms))
    fig = ms[0]
    raw = raw.replace(fig, "", 1)
    i = raw.index(END_P) + len(END_P)  # 導入文(最初の段落)の直後
    raw = raw[:i] + fig + raw[i:]
    r = requests.post(f"{W}/posts/{pid}", headers={**HA, "Content-Type": "application/json"},
                      data=json.dumps({"content": raw, "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    v = requests.get(f"{W}/posts/{pid}", params={"context": "edit"}, headers=HA).json()["content"]["raw"]
    pos_fig = v.find("shinhaeng_official_profile_photo"); pos_info = v.find("<table")
    print(pid, "photo count", v.count("shinhaeng_official_profile_photo-"), "| photo before info box:", 0 < pos_fig < pos_info)
