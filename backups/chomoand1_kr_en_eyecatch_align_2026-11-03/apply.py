"""KO1KEYZ KR/EN記事のfeatured_mediaをJP版にそろえる(2026-11-03)。
usage: python apply.py apply / python apply.py restore   (before.json の mismatch を使う)"""
import sys, json, base64, urllib.request, os
H = os.path.dirname(os.path.abspath(__file__))
env = {}
for l in open(os.path.join(H, "..", "..", ".env"), encoding="utf-8"):
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); env[k.strip()] = v.strip().strip('"')
B = env["WP_KOIKEYS_URL"].rstrip("/")
A = "Basic " + base64.b64encode(f"{env['WP_KOIKEYS_USERNAME']}:{env['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
rows = json.load(open(os.path.join(H, "before.json"), encoding="utf-8"))["mismatch"]

def set_fm(pid, mid):
    r = urllib.request.Request(f"{B}/wp-json/wp/v2/posts/{pid}", json.dumps({"featured_media": mid}).encode(),
                               {"Authorization": A, "Content-Type": "application/json"}, method="POST")
    return json.load(urllib.request.urlopen(r))["featured_media"]

key = "jp_fm" if sys.argv[1] == "apply" else "before"
ng = 0
for x in rows:
    try:
        got = set_fm(x["post"], x[key])
        if got != x[key]: ng += 1; print("NG", x["post"], got)
    except Exception as e:
        ng += 1; print("ERR", x["post"], e)
print("done", len(rows), "ng", ng)
