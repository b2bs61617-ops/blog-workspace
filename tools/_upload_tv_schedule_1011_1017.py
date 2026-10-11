# -*- coding: utf-8 -*-
"""Upload drafts: KO1KEYZ (JP/KR/EN, chomoand-1.com) + Travis Japan (chomoand-4.blog) TV schedule 10/11-10/17."""
import re, json, base64, subprocess, sys, urllib.request

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

    def media(self, fn, ctype):
        req = urllib.request.Request(self.base + "/wp-json/wp/v2/media", data=open(REPO + rf"\images\{fn}", "rb").read(), method="POST")
        req.add_header("Authorization", "Basic " + self.auth)
        req.add_header("Content-Type", ctype)
        req.add_header("Content-Disposition", f'attachment; filename="{fn}"')
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode("utf-8"))["id"]


def load(name):
    c = open(REPO + rf"\articles\{name}", encoding="utf-8").read()
    return re.sub(r"<hr\s*/?>", "", c).strip()


def run(args):
    subprocess.run([sys.executable] + args, cwd=REPO, check=True)


# --- eyecatches (generated beforehand with these args) ---
if "--gen" in sys.argv:
  run(["tools/eyecatch_koikeyz.py", "--top", "テレビ出演はいつ？", "--main", "KO1KEYZ",
       "--bottom", "10/11〜10/17の放送予定まとめ！", "--out", "images/ko1keyz_tv_schedule_1011_1017_eyecatch.png"])
  run(["tools/eyecatch_koikeyz.py", "--lang", "kr", "--top", "TV 출연 언제?", "--main", "KO1KEYZ",
       "--bottom", "10/11~10/17 방송 일정 정리!", "--out", "images/ko1keyz_tv_schedule_1011_1017_eyecatch_kr.png"])
  run(["tools/eyecatch_torahja_canva.py", "--top", "Travis Japan", "--main", "テレビ出演",
       "--bottom", "10/11〜10/17の放送予定まとめ！", "--color-key", "group",
     "--out", "images/travis_japan_tv_schedule_1011_1017_eyecatch.jpg"])

out = {}
# --- KO1KEYZ ---
k = Site("KOIKEYS")
BASE_SLUG = "ko1keyz-tv-schedule-1011-1017"
CATS = [66, 62]
jp_media = k.media("ko1keyz_tv_schedule_1011_1017_eyecatch.png", "image/png")
kr_media = k.media("ko1keyz_tv_schedule_1011_1017_eyecatch_kr.png", "image/png")
JOBS = [
    dict(lang=None, suffix="", f="ko1keyz_tv_schedule_1011_1017.html", media=jp_media,
         title="KO1KEYZのテレビ出演は？10/11〜10/17の放送予定まとめ！",
         sns="デビュー2週目のKO1KEYZは、10/16(金)深夜のテレ朝「M:ZINE」で「バラエティー101新世界」に挑戦！10/11のSBS人気歌謡、M COUNTDOWN字幕版、MV放送、YouTube・Leminoの予定まで日付順にまとめました。"),
    dict(lang="ko", suffix="-kr", f="ko1keyz_tv_schedule_1011_1017_kr.html", media=kr_media,
         title="KO1KEYZ TV 출연은? 10/11~10/17 방송 일정 정리!",
         sns="데뷔 2주 차 KO1KEYZ는 10/17(토) 새벽 TV아사히 'M:ZINE'에서 '버라이어티 101 신세카이'에 도전! 10/11 SBS 인기가요, M COUNTDOWN 자막판, MV 방송, YouTube·Lemino 일정까지 날짜순으로 정리했어요."),
    dict(lang="en", suffix="-en", f="ko1keyz_tv_schedule_1011_1017_en.html", media=jp_media,
         title="KO1KEYZ TV Appearances 10/11-10/17: Week 2 Schedule!",
         sns="KO1KEYZ's second week: TV Asahi's M:ZINE \"Variety 101 Shinsekai\" special (early Sat 10/17) and SBS Inkigayo on Sun 10/11, plus M COUNTDOWN subtitled reruns, MV airings, and YouTube/Lemino releases."),
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
tj_media = t.media("travis_japan_tv_schedule_1011_1017_eyecatch.jpg", "image/jpeg")
p = t.api("/wp-json/wp/v2/posts", {
    "title": "トラジャのテレビ出演は？10/11〜10/17の放送予定まとめ！",
    "slug": "travis-japan-tv-schedule-1011-1017",
    "content": load("travis_japan_tv_schedule_1011_1017.html"),
    "status": "draft", "categories": [3], "author": 2, "featured_media": tj_media,
}, "POST")
out["travis"] = {"id": p["id"], "slug": p["slug"], "link": p["link"], "media": tj_media}
print("TJ", p["id"], p["slug"], p["link"], tj_media)
print(json.dumps(out, ensure_ascii=False))
