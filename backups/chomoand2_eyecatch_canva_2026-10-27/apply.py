# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man)のアイキャッチをCanvaデザインDAHYbnGesOc版に差し替える(2026-10-27)。

usage: python apply.py <post_id> <image.jpg> [<post_id> <image.jpg> ...]
       python apply.py restore   # before.json の featured_media に戻す
差し替えた結果は after.json に追記する。
"""
import sys, os, json, base64, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_CHOMO2_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_CHOMO2_USERNAME']}:{env['WP_CHOMO2_APP_PASSWORD']}".encode()).decode()


def req(path, data=None, headers=None, method="POST"):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})


before = {str(p["id"]): p for p in json.load(open(os.path.join(HERE, "before.json"), encoding="utf-8"))}
after_path = os.path.join(HERE, "after.json")
after = json.load(open(after_path, encoding="utf-8")) if os.path.exists(after_path) else {}

if sys.argv[1:] == ["restore"]:
    for pid in after:
        jpost(f"/wp-json/wp/v2/posts/{pid}", {"featured_media": before[pid]["fm"]})
        print("restored", pid, before[pid]["fm"])
    sys.exit()

args = sys.argv[1:]
for pid, img in zip(args[::2], args[1::2]):
    name = f"snowman_{pid}_eyecatch_canva.jpg"
    media = req("/wp-json/wp/v2/media", open(img, "rb").read(),
                {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{name}"'})
    jpost(f"/wp-json/wp/v2/media/{media['id']}", {"alt_text": before[pid]["title"]})
    jpost(f"/wp-json/wp/v2/posts/{pid}", {"featured_media": media["id"]})
    after[pid] = media["id"]
    json.dump(after, open(after_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"post {pid}: media {before[pid]['fm']} -> {media['id']}")
