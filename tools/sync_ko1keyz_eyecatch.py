"""KO1KEYZ(chomoand-1.com)の韓国語版・英語版のアイキャッチを日本語版と同じ画像にそろえる。

韓国語版=日本語版slug+"-kr"、英語版=+"-en"(mu-plugin ko1keyz-i18n-autolinkと同じ規則)で探す。
usage:
  python tools/sync_ko1keyz_eyecatch.py 15284 [15360 ...]   # 日本語版IDを指定(publishスキルSTEP0.6)
  python tools/sync_ko1keyz_eyecatch.py --all                # 全記事を点検してズレていれば直す
"""
import sys, json, base64, urllib.request, urllib.parse, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = {}
for l in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); env[k.strip()] = v.strip().strip('"')
B = env["WP_KOIKEYS_URL"].rstrip("/")
A = "Basic " + base64.b64encode(f"{env['WP_KOIKEYS_USERNAME']}:{env['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
ST = "publish,draft,future,pending,private"


def get(path):
    return json.load(urllib.request.urlopen(urllib.request.Request(B + path, headers={"Authorization": A})))


def set_fm(pid, mid):
    r = urllib.request.Request(f"{B}/wp-json/wp/v2/posts/{pid}", json.dumps({"featured_media": mid}).encode(),
                               {"Authorization": A, "Content-Type": "application/json"}, method="POST")
    return json.load(urllib.request.urlopen(r))["featured_media"]


def by_slug(slug):
    r = get(f"/wp-json/wp/v2/posts?slug={urllib.parse.quote(slug)}&status={ST}&context=edit&_fields=id,featured_media")
    return r[0] if r else None


def sync(jp_id):
    jp = get(f"/wp-json/wp/v2/posts/{jp_id}?context=edit&_fields=id,slug,featured_media")
    if not jp["featured_media"]:
        print(f"{jp_id}: 日本語版にアイキャッチが無いのでスキップ"); return
    for suf in ("kr", "en"):
        t = by_slug(f"{jp['slug']}-{suf}")
        if not t:
            print(f"{jp_id}: {suf}版なし"); continue
        if t["featured_media"] == jp["featured_media"]:
            print(f"{jp_id}: {suf}版 {t['id']} OK"); continue
        got = set_fm(t["id"], jp["featured_media"])
        print(f"{jp_id}: {suf}版 {t['id']} {t['featured_media']} -> {got}")


def sync_all():
    posts, p = [], 1
    while True:
        r = urllib.request.urlopen(urllib.request.Request(
            f"{B}/wp-json/wp/v2/posts?status={ST}&per_page=100&page={p}&context=edit&_fields=id,slug,featured_media",
            headers={"Authorization": A}))
        posts += json.load(r)
        if p >= int(r.headers["X-WP-TotalPages"]): break
        p += 1
    slugs = {x["slug"]: x for x in posts}
    n = 0
    for x in posts:
        for suf in ("kr", "en"):
            t = slugs.get(f"{x['slug']}-{suf}")
            if t and x["featured_media"] and t["featured_media"] != x["featured_media"]:
                got = set_fm(t["id"], x["featured_media"]); n += 1
                print(f"{x['id']}: {suf}版 {t['id']} {t['featured_media']} -> {got}")
    print("直した数", n)


if __name__ == "__main__":
    if sys.argv[1:] == ["--all"]:
        sync_all()
    else:
        for i in sys.argv[1:]:
            sync(int(i))
