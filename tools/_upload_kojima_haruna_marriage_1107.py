# -*- coding: utf-8 -*-
"""小嶋陽菜 結婚相手記事をchomoand.com(トレンド速報)へ下書き投稿する(2026-11-07)。
認証はENV_FILE(既定: リポジトリ.env)から読む。ユカのMacはGoogleドライブの.envを渡す。
状態は articles/kojima_haruna_marriage_posted.json に控え、再実行で重複投稿しない。
"""
import os, sys, json, base64, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(REPO, "articles", "kojima_haruna_marriage_husband.html")
POSTED = os.path.join(REPO, "articles", "kojima_haruna_marriage_posted.json")
EYECATCH = os.path.join(REPO, "images", "kojima_haruna_marriage_eyecatch.png")
TITLE = "小嶋陽菜の旦那は何者？一般男性説と過去の熱愛相手を調査！"
SLUG = "kojima-haruna-husband"
CATEGORIES = [37]  # 芸能・トレンド
AUTHOR = 4  # ユカのMacからのchomoand.com投稿はVIVANT記事と同じauthor 4

env = {}
for line in open(os.environ.get("ENV_FILE", os.path.join(REPO, ".env")), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_TREND_USERNAME']}:{env['WP_TREND_APP_PASSWORD']}".encode()).decode()


def req(path, data=None, headers=None, method="POST"):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode('utf-8', 'ignore')[:500]}")


def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})


state = json.load(open(POSTED, encoding="utf-8")) if os.path.exists(POSTED) else {}
save = lambda: json.dump(state, open(POSTED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

html = open(ART, encoding="utf-8").read()
if "post" not in state:
    p = jpost("/wp-json/wp/v2/posts", {"title": TITLE, "content": html, "slug": SLUG, "status": "draft",
                                       "categories": CATEGORIES, "author": AUTHOR})
    state["post"] = p["id"]; save()
elif "--update-content" in sys.argv:
    jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"content": html, "status": "draft"})
if "eyecatch" not in state:
    m = req("/wp-json/wp/v2/media", open(EYECATCH, "rb").read(),
            {"Content-Type": "image/png", "Content-Disposition": 'attachment; filename="kojima_haruna_marriage_eyecatch.png"'})
    jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": "小嶋陽菜の旦那は何者？結婚＆第1子出産を発表"})
    state["eyecatch"] = m["id"]; save()
    jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"featured_media": state["eyecatch"]})
p = req(f"/wp-json/wp/v2/posts/{state['post']}?context=edit", method="GET")
print(p["id"], p["status"], p["author"], p["categories"], p["featured_media"], p["title"]["raw"])
print(f"{BASE}/wp-admin/post.php?post={p['id']}&action=edit")
