# -*- coding: utf-8 -*-
"""chomoand-5.site ID690: 次回予告の画像(テロップ途中のコマ)を、テロップが出きったコマに差し替える。"""
import re, json, base64, urllib.request
REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = dict(l.strip().split("=", 1) for l in open(REPO + r"\.env", encoding="utf-8") if "=" in l and not l.startswith("#"))
BASE = env["WP_CHOMO5_URL"].strip().strip('"').rstrip("/")
AUTH = base64.b64encode(f"{env['WP_CHOMO5_USERNAME'].strip().strip(chr(34))}:{env['WP_CHOMO5_APP_PASSWORD'].strip().strip(chr(34))}".encode()).decode()
def req(path, data=None, headers=None):
    r = urllib.request.Request(BASE + path, data=data, method="POST" if data is not None else "GET")
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items(): r.add_header(k, v)
    return json.loads(urllib.request.urlopen(r).read().decode("utf-8"))
ALT = "次回予告は中間淳太をおもてなし"
raw = req("/wp-json/wp/v2/posts/690?context=edit&_fields=content")["content"]["raw"]
m_old = re.search(r'<!-- wp:image \{"id":(\d+)[^>]*-->\n<figure[^\n]*alt="%s"[^\n]*\n<!-- /wp:image -->' % ALT, raw)
assert m_old, "old block not found"
old_id = int(m_old.group(1))
fn = "ktl_ep5_hyrox_09b.jpg"
m = req("/wp-json/wp/v2/media", open(REPO + rf"\images\{fn}", "rb").read(),
        {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{fn}"'})
req(f"/wp-json/wp/v2/media/{m['id']}", json.dumps({"alt_text": ALT}).encode(), {"Content-Type": "application/json"})
blk = m_old.group(0).replace(f'"id":{old_id}', f'"id":{m["id"]}').replace(f"wp-image-{old_id}", f"wp-image-{m['id']}")
blk = re.sub(r'src="[^"]+"', f'src="{m["source_url"]}"', blk, count=1)
new = raw.replace(m_old.group(0), blk)
req("/wp-json/wp/v2/posts/690", json.dumps({"content": new}).encode(), {"Content-Type": "application/json"})
chk = req("/wp-json/wp/v2/posts/690?context=edit&_fields=content,status")
print("old", old_id, "new", m["id"], "status", chk["status"], "in_content", f"wp-image-{m['id']}" in chk["content"]["raw"], "old_gone", f"wp-image-{old_id}" not in chk["content"]["raw"])
