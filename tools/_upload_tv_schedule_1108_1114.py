# -*- coding: utf-8 -*-
"""Upload drafts: TV schedule 11/8-11/14 for Travis Japan (chomoand-4.blog), KEY TO LIT (chomoand-5.site),
Snow Man (chomoand-2.com), SixTONES (chomoand-0.com), KO1KEYZ JP/KR/EN (chomoand-1.com).
All titles start with 【未】 (to be rewritten right before publishing). Author = momo (id 2, PC USER1)."""
import re, json, base64, sys, urllib.request

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
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

    def media(self, fn, ctype, alt):
        req = urllib.request.Request(self.base + "/wp-json/wp/v2/media", data=open(REPO + rf"\images\{fn}", "rb").read(), method="POST")
        req.add_header("Authorization", "Basic " + self.auth)
        req.add_header("Content-Type", ctype)
        req.add_header("Content-Disposition", f'attachment; filename="{fn}"')
        with urllib.request.urlopen(req) as r:
            mid = json.loads(r.read().decode("utf-8"))["id"]
        self.api(f"/wp-json/wp/v2/media/{mid}", {"alt_text": alt}, "POST")
        return mid


def load(name):
    return re.sub(r"<hr\s*/?>", "", open(REPO + rf"\articles\{name}", encoding="utf-8").read()).strip()


out = {}


def post(site, label, title, slug, fn, cats, media, extra=None):
    body = {"title": title, "slug": slug, "content": load(fn), "status": "draft",
            "categories": cats, "author": 2, "featured_media": media}
    body.update(extra or {})
    p = site.api("/wp-json/wp/v2/posts", body, "POST")
    out[label] = {"id": p["id"], "status": p["status"], "link": p["link"], "media": media}
    print(label, p["id"], p["status"], p["link"])


# --- Travis Japan ---
t = Site("CHOMO4")
title = "【未】トラジャのテレビ出演は？11/8〜11/14の放送予定まとめ！"
post(t, "travis", title, "travis-japan-tv-schedule-1108-1114", "travis_japan_tv_schedule_1108_1114.html", [3],
     t.media("travis_japan_tv_schedule_1108_1114_eyecatch.jpg", "image/jpeg", title[3:]))

# --- KEY TO LIT ---
c5 = Site("CHOMO5")
title = "【未】【KEY TO LIT】テレビ出演は？11/8〜11/14の放送予定まとめ！"
post(c5, "ktl", title, "key-to-lit-tv-schedule-1108-1114", "key_to_lit_tv_schedule_1108_1114.html", [4, 6, 7, 8, 9, 10],
     c5.media("key_to_lit_tv_schedule_1108_1114_eyecatch.jpg", "image/jpeg", title[3:]))

# --- Snow Man ---
c2 = Site("CHOMO2")
title = "【未】Snow Manのテレビ出演は？11/8〜11/14の放送予定まとめ！"
post(c2, "snowman", title, "snow-man-tv-schedule-1108-1114", "snowman_tv_schedule_1108_1114.html", [4],
     c2.media("snowman_tv_schedule_1108_1114_eyecatch.jpg", "image/jpeg", title[3:]))

# --- SixTONES ---
c0 = Site("AUDITION")
title = "【未】SixTONESのテレビ出演は？11/8〜11/14の放送予定まとめ！"
post(c0, "sixtones", title, "sixtones-tv-schedule-1108-1114", "sixtones_tv_schedule_1108_1114.html", [15],
     c0.media("sixtones_tv_schedule_1108_1114_eyecatch.jpg", "image/jpeg", title[3:]))

# --- KO1KEYZ JP/KR/EN ---
k = Site("KOIKEYS")
jp_media = k.media("ko1keyz_tv_schedule_1108_1114_eyecatch.png", "image/png", "KO1KEYZのテレビ出演は？11/8〜11/14の放送予定まとめ！")
kr_media = k.media("ko1keyz_tv_schedule_1108_1114_eyecatch_kr.png", "image/png", "KO1KEYZ TV 출연은? 11/8~11/14 방송 일정 정리!")
BASE = "ko1keyz-tv-schedule-1108-1114"
for lang, suf, fn, media, title, sns in [
    (None, "", "ko1keyz_tv_schedule_1108_1114.html", jp_media,
     "【未】KO1KEYZのテレビ出演は？11/8〜11/14の放送予定まとめ！",
     "デビュー6週目のKO1KEYZ、11/10(火)の日本テレビ「さんま御殿」にYOSHIKIが奈良県代表で出演！ソウルファンミ2日目、KNTVの再放送、LAPOSTA FC先行の締め切りまで日付順にまとめました。"),
    ("ko", "-kr", "ko1keyz_tv_schedule_1108_1114_kr.html", kr_media,
     "【未】KO1KEYZ TV 출연은? 11/8~11/14 방송 일정 정리!",
     "데뷔 6주 차 KO1KEYZ, 11/10(화) 니혼TV '산마 고텐'에 YOSHIKI가 나라현 대표로 출연! 서울 팬미팅 2일 차, KNTV 재방송, LAPOSTA FC 선행 마감까지 정리했어요."),
    ("en", "-en", "ko1keyz_tv_schedule_1108_1114_en.html", jp_media,
     "【未】KO1KEYZ TV Appearances 11/8-11/14: Week 6 Schedule!",
     "KO1KEYZ week 6: YOSHIKI on Nippon TV's Sanma Goten (11/10), day 2 of the Seoul fan meeting, KNTV rerun and the LAPOSTA 2027 presale deadline."),
]:
    extra = {"meta": {"jetpack_publicize_message": sns}}
    if lang:
        extra["lang"] = lang
    post(k, "ko1keyz_" + (lang or "ja"), title, BASE + suf, fn, [66, 62], media, extra)

json.dump(out, open(REPO + r"\articles\tv_schedule_1108_1114_posted.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
