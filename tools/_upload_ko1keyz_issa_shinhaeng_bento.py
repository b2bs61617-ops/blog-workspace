# -*- coding: utf-8 -*-
"""Upload JP + KR + EN drafts: ISSA/SHINHAENG bento coincidence article (chomoand-1.com)."""
import re, json, base64, urllib.request

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip().strip('"')

U = env["WP_KOIKEYS_USERNAME"]; P = env["WP_KOIKEYS_APP_PASSWORD"]; BASE = env["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f"{U}:{P}".encode()).decode()


def api(path, body=None, method="GET"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Authorization", "Basic " + AUTH)
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


def upload_media(path, filename, ctype):
    img = open(path, "rb").read()
    req = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=img, method="POST")
    req.add_header("Authorization", "Basic " + AUTH)
    req.add_header("Content-Type", ctype)
    req.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


bento = upload_media(REPO + r"\tools\Xiy\posts_20260922_takusankue_tweet\images\post_1_img_1.jpg", "ko1keyz_issa_bento.jpg", "image/jpeg")
BENTO_URL = bento["source_url"]
print("bento img:", bento["id"], BENTO_URL)


def load(name):
    c = open(REPO + rf"\articles\{name}", encoding="utf-8").read()
    c = re.sub(r"<hr\s*/?>", "", c)
    assert "{{ISSA_BENTO_IMG}}" in c
    return c.replace("{{ISSA_BENTO_IMG}}", BENTO_URL).strip()


CATS = [66, 62]
BASE_SLUG = "issa-shinhaeng-bento"

jp = api("/wp-json/wp/v2/posts", {
    "title": "ISSAとシンヘンの弁当が同じ？まさかの偶然に驚き！",
    "slug": BASE_SLUG,
    "content": load("ko1keyz_issa_shinhaeng_bento_coincidence.html"),
    "status": "draft", "categories": CATS, "author": 2,
    "meta": {"jetpack_publicize_message": (
        "KO1KEYZのISSAが投稿した弁当の写真が話題に。ほぼ同じ時期にSHINHAENGも似た弁当を食べていたとの投稿があり、"
        "Xでは「まさかの一致」に驚く声が上がっています。")},
}, "POST")
JP_ID = jp["id"]
jp_media = upload_media(REPO + r"\images\ko1keyz_issa_shinhaeng_bento_eyecatch.png", "ko1keyz_issa_shinhaeng_bento_eyecatch.png", "image/png")["id"]
api(f"/wp-json/wp/v2/posts/{JP_ID}", {"featured_media": jp_media, "status": "draft"}, "POST")
print("JP", JP_ID, jp["link"], "media", jp_media)

kr_media = upload_media(REPO + r"\images\ko1keyz_issa_shinhaeng_bento_eyecatch_kr.png", "ko1keyz_issa_shinhaeng_bento_eyecatch_kr.png", "image/png")["id"]

JOBS = [
    dict(lang="ko", suffix="-kr", md="ko1keyz_issa_shinhaeng_bento_coincidence_kr.html", media=kr_media,
         title="ISSA와 신행의 도시락이 같다고? 뜻밖의 우연에 깜짝!",
         sns="KO1KEYZ의 ISSA가 올린 도시락 사진이 화제입니다. 거의 같은 시기에 SHINHAENG도 비슷한 도시락을 먹었다는 게시글이 있어, "
             "X에서는 \u201c설마 하는 우연\u201d이라며 놀라는 목소리가 나오고 있습니다."),
    dict(lang="en", suffix="-en", md="ko1keyz_issa_shinhaeng_bento_coincidence_en.html", media=jp_media,
         title="Did ISSA and SHINHAENG Eat the Same Bento? A Surprising Coincidence!",
         sns="A bento photo shared by KO1KEYZ's ISSA has become a talking point. Around the same time, SHINHAENG posted "
             "that he too had eaten a similar bento, and fans on X reacted with surprise at the coincidence."),
]
out = {"jp": {"id": JP_ID, "media": jp_media}}
for j in JOBS:
    p = api("/wp-json/wp/v2/posts", {
        "title": j["title"], "slug": BASE_SLUG + j["suffix"], "content": load(j["md"]),
        "status": "draft", "categories": CATS, "author": 2, "featured_media": j["media"],
        "lang": j["lang"], "translations": {"ja": JP_ID},
        "meta": {"jetpack_publicize_message": j["sns"]},
    }, "POST")
    out[j["lang"]] = {"id": p["id"], "slug": p["slug"], "link": p["link"], "media": j["media"]}
    print(j["lang"], p["id"], p["slug"], p["link"])
print(json.dumps(out, ensure_ascii=False))
