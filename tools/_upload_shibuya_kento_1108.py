# -*- coding: utf-8 -*-
"""渋谷謙人 3記事(学歴・何者・歴代彼女)をchomoand.com(トレンド速報)へ下書き投稿する(2026-11-08 ユカ依頼)。
認証はENV_FILE(既定: リポジトリ.env)から読む。ユカのMacはGoogleドライブの.envを渡す。
状態は articles/shibuya_kento_posted.json に控え、再実行で重複投稿しない。--update-content で本文だけ更新。
"""
import os, sys, json, base64, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTED = os.path.join(REPO, "articles", "shibuya_kento_posted.json")
CATEGORIES = [37]  # 芸能・トレンド
AUTHOR = 4
ARTICLES = [
    ("gakureki", "渋谷謙人の学歴は？出身高校を中退した理由と子役・サッカー二刀流の学生時代",
     "shibuya-kento-gakureki", "渋谷謙人の学歴は？高校中退の理由と子役時代"),
    ("nanimono", "渋谷謙人は何者？のっちの結婚相手は子役出身の大河俳優！経歴と実家を調査",
     "shibuya-kento-nanimono", "渋谷謙人は何者？子役出身の経歴と実家"),
    ("kanojo", "渋谷謙人の歴代彼女は誰？のっちとの馴れ初めや鈴木えみとの噂を調査！",
     "shibuya-kento-kanojo", "渋谷謙人の歴代彼女は誰？鈴木えみとの噂も調査"),
]

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

for key, title, slug, alt in ARTICLES:
    s = state.setdefault(key, {})
    html = open(os.path.join(REPO, "articles", f"shibuya_kento_{key}.html"), encoding="utf-8").read()
    if "post" not in s:
        p = jpost("/wp-json/wp/v2/posts", {"title": title, "content": html, "slug": slug, "status": "draft",
                                           "categories": CATEGORIES, "author": AUTHOR})
        s["post"] = p["id"]; save()
    elif "--update-content" in sys.argv:
        jpost(f"/wp-json/wp/v2/posts/{s['post']}", {"content": html, "status": "draft"})
    if "eyecatch" not in s:
        img = os.path.join(REPO, "images", f"shibuya_kento_{key}_eyecatch.png")
        m = req("/wp-json/wp/v2/media", open(img, "rb").read(),
                {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="shibuya_kento_{key}_eyecatch.png"'})
        jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": alt})
        s["eyecatch"] = m["id"]; save()
        jpost(f"/wp-json/wp/v2/posts/{s['post']}", {"featured_media": s["eyecatch"]})
    p = req(f"/wp-json/wp/v2/posts/{s['post']}?context=edit", method="GET")
    print(key, p["id"], p["status"], p["featured_media"], p["slug"], p.get("permalink_template", ""), p["title"]["raw"])
    print(f"  {BASE}/wp-admin/post.php?post={p['id']}&action=edit")
