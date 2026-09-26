# -*- coding: utf-8 -*-
"""SHINHAENG洗車場記事(JP13716/KR13717/EN13718・下書き)のプロフィール節に公式PROFILE PHOTO(media 13724)を入れる。
出典: https://x.com/KO1KEYZofficial/status/2067445194119577851 (KO1KEYZ公式 PROFILE PHOTO #SHINHAENG)
"""
import base64, json, sys
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
SRC = "https://x.com/KO1KEYZofficial/status/2067445194119577851"
MEDIA_ID = 13724

m = requests.get(f"{W}/media/{MEDIA_ID}", headers=HA).json()
md = m["media_details"]; sz = md["sizes"]
full, fw, fh = m["source_url"], md["width"], md["height"]
lg, me = sz["large"], sz["medium"]
iw = lg["width"]; ih = int(iw * fh / fw)
srcset = f'{me["source_url"]} {me["width"]}w, {lg["source_url"]} {lg["width"]}w, {full} {fw}w'


def fig(alt, label, note):
    return f'''<!-- wp:html -->
<figure class="wp-block-image size-large">
<img src="{lg["source_url"]}" alt="{alt}" width="{iw}" height="{ih}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {iw}px) 100vw, {iw}px">
<figcaption style="text-align:center;font-size:12px;">{label}<a href="{SRC}" target="_blank" rel="noopener">{SRC}</a>{note}</figcaption>
</figure>
<!-- /wp:html -->'''


TARGETS = {
    13716: ("SHINHAENG(オ・シンヘン)のプロフィール", fig("KO1KEYZ SHINHAENG(オ・シンヘン)の公式プロフィール写真", "出典:", "(KO1KEYZ公式のプロフィール写真)")),
    13717: ("SHINHAENG(오신행) 프로필", fig("KO1KEYZ SHINHAENG(오신행) 공식 프로필 사진", "출처: ", " (KO1KEYZ 공식 프로필 사진)")),
    13718: ("SHINHAENG (Oh Shin-haeng) profile", fig("KO1KEYZ SHINHAENG (Oh Shin-haeng) official profile photo", "Source: ", " (KO1KEYZ official profile photo)")),
}

for pid, (heading, figure) in TARGETS.items():
    d = requests.get(f"{W}/posts/{pid}", params={"context": "edit"}, headers=HA).json()
    assert d["status"] == "draft", d["status"]
    raw = d["content"]["raw"]
    if "shinhaeng_official_profile_photo" in raw:
        print(pid, "already has photo"); continue
    key = f'<h2 class="wp-block-heading">{heading}</h2>\n<!-- /wp:heading -->'
    assert raw.count(key) == 1, (pid, heading)
    i = raw.index(key) + len(key)
    raw = raw[:i] + "\n\n" + figure + raw[i:]
    r = requests.post(f"{W}/posts/{pid}", headers={**HA, "Content-Type": "application/json"},
                      data=json.dumps({"content": raw, "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    v = requests.get(f"{W}/posts/{pid}", params={"context": "edit"}, headers=HA).json()
    print(pid, v["status"], "verified" if "shinhaeng_official_profile_photo" in v["content"]["raw"] else "NOT REFLECTED")
