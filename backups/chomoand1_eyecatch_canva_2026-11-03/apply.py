"""KO1KEYZ: Canva書き出しURL → WPメディア → featured_media設定。
usage: python apply.py set <URL> <filename> <post_id> [post_id...]  /  python apply.py restore"""
import sys, json, base64, urllib.request, os
H = os.path.dirname(os.path.abspath(__file__))
env = {}
for l in open(os.path.join(H, "..", "..", ".env"), encoding="utf-8"):
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); env[k.strip()] = v.strip().strip('"')
B = env["WP_KOIKEYS_URL"].rstrip("/")
A = "Basic " + base64.b64encode(f"{env['WP_KOIKEYS_USERNAME']}:{env['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
LOG = os.path.join(H, "log.json")
log = json.load(open(LOG, encoding="utf-8")) if os.path.exists(LOG) else []

def req(path, data=None, headers=None, method=None):
    h = {"Authorization": A, **(headers or {})}
    return json.load(urllib.request.urlopen(urllib.request.Request(B + path, data=data, headers=h, method=method)))

def set_fm(pid, mid):
    return req(f"/wp-json/wp/v2/posts/{pid}", json.dumps({"featured_media": mid}).encode(), {"Content-Type": "application/json"}, "POST")["featured_media"]

if sys.argv[1] == "set":
    url, fn, pids = sys.argv[2], sys.argv[3], [int(x) for x in sys.argv[4:]]
    img = urllib.request.urlopen(url).read()
    m = req("/wp-json/wp/v2/media", img, {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{fn}"'}, "POST")
    print("media", m["id"], m["source_url"])
    for pid in pids:
        before = req(f"/wp-json/wp/v2/posts/{pid}?context=edit&_fields=featured_media")["featured_media"]
        after = set_fm(pid, m["id"])
        log.append({"post": pid, "before": before, "after": after}); print(pid, before, "->", after)
    json.dump(log, open(LOG, "w", encoding="utf-8"), indent=1)
elif sys.argv[1] == "restore":
    for e in reversed(log):
        print(e["post"], "->", set_fm(e["post"], e["before"]))
