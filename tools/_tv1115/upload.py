# -*- coding: utf-8 -*-
"""Upload drafts: TV schedule 11/15-11/21 for 5 groups (KO1KEYZ JP/KR/EN). Titles start with 【未】. Author = momo (id 2)."""
import os, sys, re, json, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wp import api, env, REPO
import base64


def media(key, fn, ctype, alt):
    base = env[f"WP_{key}_URL"].rstrip("/")
    auth = base64.b64encode(f"{env[f'WP_{key}_USERNAME']}:{env[f'WP_{key}_APP_PASSWORD']}".encode()).decode()
    req = urllib.request.Request(base + "/wp-json/wp/v2/media", data=open(REPO + rf"\images\{fn}", "rb").read(), method="POST")
    req.add_header("Authorization", "Basic " + auth)
    req.add_header("Content-Type", ctype)
    req.add_header("Content-Disposition", f'attachment; filename="{fn}"')
    mid = json.loads(urllib.request.urlopen(req).read().decode())["id"]
    api(key, f"/wp-json/wp/v2/media/{mid}", {"alt_text": alt})
    return mid


def load(name):
    return open(REPO + rf"\articles\{name}", encoding="utf-8").read().strip()


out = {}


def post(key, label, title, slug, fn, cats, mid, extra=None):
    body = {"title": title, "slug": slug, "content": load(fn), "status": "draft", "categories": cats, "author": 2, "featured_media": mid}
    body.update(extra or {})
    r = api(key, "/wp-json/wp/v2/posts", body)
    out[label] = {"id": r["id"], "status": r["status"], "link": r["link"], "media": mid}
    print(label, r["id"], r["status"], r["title"]["raw"], r["link"])


for key, label, title, slug, fn, cats in [
    ("CHOMO4", "travis", "トラジャのテレビ出演は？11/15〜11/21の放送予定まとめ！", "travis-japan-tv-schedule-1115-1121", "travis_japan", [3]),
    ("CHOMO5", "ktl", "【KEY TO LIT】テレビ出演は？11/15〜21の放送予定！", "key-to-lit-tv-schedule-1115-1121", "key_to_lit", [4, 6, 7, 8, 9, 10]),
    ("CHOMO2", "snowman", "【Snow Man】テレビ出演は？11/15〜21の放送予定まとめ！", "snow-man-tv-schedule-1115-1121", "snowman", [4]),
    ("AUDITION", "sixtones", "SixTONESのテレビ出演は？11/15〜21の放送予定まとめ！", "sixtones-tv-schedule-1115-1121", "sixtones", [15]),
]:
    mid = media(key, f"{fn}_tv_schedule_1115_1121_eyecatch.jpg", "image/jpeg", title)
    post(key, label, "【未】" + title, slug, f"{fn}_tv_schedule_1115_1121.html", cats, mid)

jp_media = media("KOIKEYS", "ko1keyz_tv_schedule_1115_1121_eyecatch.png", "image/png", "KO1KEYZのテレビ出演は？11/15〜11/21の放送予定まとめ！")
kr_media = media("KOIKEYS", "ko1keyz_tv_schedule_1115_1121_eyecatch_kr.png", "image/png", "KO1KEYZ TV 출연은? 11/15~11/21 방송 일정 정리!")
BASE = "ko1keyz-tv-schedule-1115-1121"
for lang, suf, fn, mid, title, sns in [
    (None, "", "ko1keyz_tv_schedule_1115_1121.html", jp_media,
     "【未】【KO1KEYZ】テレビ出演は？11/15〜21の放送予定まとめ！",
     "デビュー7週目のKO1KEYZ、11/21(土)は京セラドーム大阪の「2026 MAMA AWARDS」に出演！生中継の見方、11/15(日)締め切りのFC先行・グッズ通販まで日付順にまとめました。"),
    ("ko", "-kr", "ko1keyz_tv_schedule_1115_1121_kr.html", kr_media,
     "【未】KO1KEYZ TV 출연은? 11/15~11/21 방송 일정 정리!",
     "데뷔 7주 차 KO1KEYZ, 11/21(토) 교세라돔 오사카 '2026 MAMA AWARDS' 출연! 생중계 시청 방법과 11/15(일) 마감 일정까지 정리했어요."),
    ("en", "-en", "ko1keyz_tv_schedule_1115_1121_en.html", jp_media,
     "【未】KO1KEYZ TV Appearances 11/15-11/21: Week 7 Schedule!",
     "KO1KEYZ week 7: 2026 MAMA AWARDS at Kyocera Dome Osaka on 11/21, how to watch live, plus the 11/15 presale and goods deadlines."),
]:
    extra = {"meta": {"jetpack_publicize_message": sns}}
    if lang:
        extra["lang"] = lang
    post("KOIKEYS", "ko1keyz_" + (lang or "ja"), title, BASE + suf, fn, [66, 62], mid, extra)

json.dump(out, open(REPO + r"\articles\tv_schedule_1115_1121_posted.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
