# -*- coding: utf-8 -*-
"""Upload drafts: KO1KEYZ (JP/KR/EN, chomoand-1.com) + Travis Japan (chomoand-4.blog) TV schedule 10/4-10/10."""
import re, json, base64, urllib.request

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip().strip('"')


class Site:
    def __init__(self, key):
        self.base = env[f"WP_{key}_URL"].rstrip("/")
        self.auth = base64.b64encode(f"{env[f'WP_{key}_USERNAME']}:{env[f'WP_{key}_APP_PASSWORD']}".encode()).decode()

    def api(self, path, body=None, method="GET"):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method)
        req.add_header("Authorization", "Basic " + self.auth)
        if data:
            req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode("utf-8"))

    def media(self, fn):
        req = urllib.request.Request(self.base + "/wp-json/wp/v2/media", data=open(REPO + rf"\images\{fn}", "rb").read(), method="POST")
        req.add_header("Authorization", "Basic " + self.auth)
        req.add_header("Content-Type", "image/png")
        req.add_header("Content-Disposition", f'attachment; filename="{fn}"')
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode("utf-8"))["id"]


def load(name):
    c = open(REPO + rf"\articles\{name}", encoding="utf-8").read()
    return re.sub(r"<hr\s*/?>", "", c).strip()


out = {}
# --- KO1KEYZ ---
k = Site("KOIKEYS")
BASE_SLUG = "ko1keyz-tv-schedule-1004-1010"
CATS = [66, 62]
jp_media = k.media("ko1keyz_tv_schedule_1004_1010_eyecatch.png")
kr_media = k.media("ko1keyz_tv_schedule_1004_1010_eyecatch_kr.png")
JOBS = [
    dict(lang=None, suffix="", f="ko1keyz_tv_schedule_1004_1010.html", media=jp_media,
         title="KO1KEYZのテレビ出演は？10/4〜10/10の放送予定まとめ！",
         sns="デビュー週のKO1KEYZのテレビ出演は、10/7(水)日本テレビ「DayDay.」と10/8(木)Mnet「M COUNTDOWN」日韓同時生放送。デビュー日のYouTube生配信や学園#2、今週お休みのM:ZINEの次回放送日まで日付順にまとめました。"),
    dict(lang="ko", suffix="-kr", f="ko1keyz_tv_schedule_1004_1010_kr.html", media=kr_media,
         title="KO1KEYZ TV 출연은? 10/4~10/10 방송 일정 정리!",
         sns="데뷔 주간 KO1KEYZ의 TV 출연은 10/7(수) 니혼TV 'DayDay.'와 10/8(목) Mnet 'M COUNTDOWN' 한일 동시 생방송이에요. 데뷔일 YouTube 생방송, 학원 #2, 이번 주 쉬는 M:ZINE 다음 방송일까지 날짜순으로 정리했어요."),
    dict(lang="en", suffix="-en", f="ko1keyz_tv_schedule_1004_1010_en.html", media=jp_media,
         title="KO1KEYZ TV Appearances 10/4-10/10: Debut Week Schedule!",
         sns="KO1KEYZ's debut-week TV: Nippon TV's DayDay. on Wed 10/7 and Mnet's M COUNTDOWN live on Thu 10/8. Plus the debut-day YouTube livestream, Gakuen #2, and when M:ZINE returns."),
]
for j in JOBS:
    body = {"title": j["title"], "slug": BASE_SLUG + j["suffix"], "content": load(j["f"]), "status": "draft",
            "categories": CATS, "author": 2, "featured_media": j["media"],
            "meta": {"jetpack_publicize_message": j["sns"]}}
    if j["lang"]:
        body["lang"] = j["lang"]
    p = k.api("/wp-json/wp/v2/posts", body, "POST")
    out["ko1keyz_" + (j["lang"] or "ja")] = {"id": p["id"], "slug": p["slug"], "link": p["link"], "media": j["media"]}
    print("KO1KEYZ", j["lang"] or "ja", p["id"], p["slug"], p["link"])

# --- Travis Japan ---
t = Site("CHOMO4")
tj_media = t.media("travis_japan_tv_schedule_1004_1010_eyecatch.png")
p = t.api("/wp-json/wp/v2/posts", {
    "title": "トラジャのテレビ出演は？10/4〜10/10の放送予定まとめ！",
    "slug": "travis-japan-tv-schedule-1004-1010",
    "content": load("travis_japan_tv_schedule_1004_1010.html"),
    "status": "draft", "categories": [3], "author": 2, "featured_media": tj_media,
}, "POST")
out["travis"] = {"id": p["id"], "slug": p["slug"], "link": p["link"], "media": tj_media}
print("TJ", p["id"], p["slug"], p["link"], tj_media)
print(json.dumps(out, ensure_ascii=False))
