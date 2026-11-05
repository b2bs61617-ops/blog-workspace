# -*- coding: utf-8 -*-
"""Upload JP + KR + EN drafts: KO1! KO1! KO1KEYZ EP.4 part 2 hide-and-seek recap (chomoand-1.com)."""
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
SRC = "https://www.youtube.com/watch?v=M1XEXbFuEWQ"


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


ALTS = {
    "issa": {"ja": "連携プレーで確保されるISSA", "ko": "연계 플레이로 잡히는 ISSA", "en": "ISSA caught by the taggers' teamwork"},
    "gym": {"ja": "体育館の外で同時に捕まったDAIKIとKEITO", "ko": "체육관 밖에서 동시에 잡힌 DAIKI와 KEITO", "en": "DAIKI and KEITO caught together outside the gym"},
    "kosuke": {"ja": "鬼たちの挟み撃ちで捕まったKOSUKE", "ko": "술래들의 협공에 잡힌 KOSUKE", "en": "KOSUKE caught in a pincer move"},
    "ryuji": {"ja": "1階保健室で捕まったRYUJI", "ko": "1층 보건실에서 잡힌 RYUJI", "en": "RYUJI caught in the nurse's office"},
    "yuki": {"ja": "2階音楽室で捕まったYUKI", "ko": "2층 음악실에서 잡힌 YUKI", "en": "YUKI caught in the music room"},
    "three": {"ja": "残る逃走者はSIYOUNG・SHINHAENG・YURAの3人", "ko": "남은 도망자는 SIYOUNG·SHINHAENG·YURA 3명", "en": "Three runners left: SIYOUNG, SHINHAENG and YURA"},
    "shinhaeng": {"ja": "屋上から見つかり捕まったSHINHAENG", "ko": "옥상에서 발견되어 잡힌 SHINHAENG", "en": "SHINHAENG caught after being spotted from the roof"},
    "towa": {"ja": "2階バルコニーで逃走者宣言をするTOWA", "ko": "2층 발코니에서 도망자 선언을 하는 TOWA", "en": "TOWA insisting he is still a runner on the balcony"},
    "touch": {"ja": "答え合わせで「タッチしたよ?」と話すISSA", "ko": "정답 확인에서 터치했다고 말하는 ISSA", "en": "ISSA revealing he tagged TOWA"},
    "yura": {"ja": "体育館の後ろの木の中に隠れ続けたYURA", "ko": "체육관 뒤 나무 속에 계속 숨어 있던 YURA", "en": "YURA hiding inside a tree behind the gym"},
    "siyoung": {"ja": "隠れ場所を明かすSIYOUNG", "ko": "은신처를 밝히는 SIYOUNG", "en": "SIYOUNG revealing his hiding spot"},
    "studio": {"ja": "SIYOUNGが隠れていた放送室の向かいの部屋", "ko": "SIYOUNG이 숨어 있던 방송실 맞은편 방", "en": "The room across from the broadcast room where SIYOUNG hid"},
}
FILES = {k: f"ko1ko1ko1keyz_ep4b_{k}.jpg" for k in ALTS}
CAP = {"ja": "出典:", "ko": "출처:", "en": "Source: "}

media = {}
for key, fn in FILES.items():
    m = upload_media(REPO + rf"\images\{fn}", fn, "image/jpeg")
    s = m["media_details"]["sizes"]
    full = (m["source_url"], m["media_details"]["width"], m["media_details"]["height"])
    media[key] = {"id": m["id"], "full": full,
                  "large": (s["large"]["source_url"], s["large"]["width"], s["large"]["height"]) if "large" in s else full,
                  "medium": (s["medium"]["source_url"], s["medium"]["width"], s["medium"]["height"])}
    print("img", key, m["id"])


def fig(key, lang):
    d = media[key]; L = d["large"]; M = d["medium"]; F = d["full"]
    return ('<!-- wp:image {"sizeSlug":"large","linkDestination":"none"} -->\n'
            f'<figure class="wp-block-image size-large"><img src="{L[0]}" alt="{ALTS[key][lang]}" width="{L[1]}" height="{L[2]}" style="max-width:100%;height:auto;" '
            f'srcset="{M[0]} {M[1]}w, {L[0]} {L[1]}w, {F[0]} {F[1]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
            f'<figcaption class="wp-element-caption" style="text-align:center;font-size:12px;">{CAP[lang]}{SRC}</figcaption></figure>\n'
            '<!-- /wp:image -->')


def load(name, lang):
    c = open(REPO + rf"\articles\{name}", encoding="utf-8").read()
    c = re.sub(r"<hr\s*/?>", "", c)
    for key in ALTS:
        ph = "{{IMG_" + key + "}}"
        assert ph in c, (name, ph)
        c = c.replace(ph, fig(key, lang))
    assert "{{" not in c
    return c.strip()


CATS = [66]
BASE_SLUG = "ko1-ko1-ko1keyz-ep4-hide-and-seek-part2"

jp = api("/wp-json/wp/v2/posts", {
    "title": "KO1!KO1!KO1KEYZ EP.4後編まとめ！逃げ切ったのは誰？",
    "slug": BASE_SLUG,
    "content": load("ko1ko1ko1keyz_ep4b_kakureoni_kouhen.html", "ja"),
    "status": "draft", "categories": CATS, "author": 2,
    "meta": {"jetpack_publicize_message": ("コイキーズ「KO1! KO1! KO1KEYZ」EP.4後編は放課後かくれ鬼の後半戦。鬼がどんどん増える中、最後まで逃げ切ったのは2人だけ。TOWAの「タッチされてません」宣言の真相と、立入禁止疑惑が出た隠れ場所にも注目。")},
}, "POST")
JP_ID = jp["id"]
jp_media = upload_media(REPO + r"\images\ko1ko1ko1keyz_ep4b_eyecatch.png", "ko1ko1ko1keyz_ep4b_eyecatch.png", "image/png")["id"]
api(f"/wp-json/wp/v2/posts/{JP_ID}", {"featured_media": jp_media, "status": "draft"}, "POST")
print("JP", JP_ID, jp["link"], "media", jp_media)

kr_media = jp_media

JOBS = [
    dict(lang="ko", suffix="-kr", md="ko1ko1ko1keyz_ep4b_kakureoni_kouhen_kr.html", media=kr_media,
         title="KO1!KO1!KO1KEYZ EP.4 후편 정리! 끝까지 살아남은 멤버는?",
         sns="코이키즈 'KO1! KO1! KO1KEYZ' EP.4 후편은 방과 후 숨바꼭질 술래잡기 후반전. 술래가 계속 늘어나는 가운데 끝까지 살아남은 건 단 2명. TOWA의 '터치 안 당했어요' 선언의 진실과 출입금지 의혹이 나온 은신처도 주목."),
    dict(lang="en", suffix="-en", md="ko1ko1ko1keyz_ep4b_kakureoni_kouhen_en.html", media=jp_media,
         title="KO1! KO1! KO1KEYZ EP.4 Part 2 Recap: Who Escaped Until the End?",
         sns="KO1! KO1! KO1KEYZ EP.4 Part 2 is the second half of the after-school hide-and-seek. As the taggers multiply, only two members make it to the end. Plus the truth behind TOWA's 'I wasn't tagged' claim and a hiding spot that may have been off-limits."),
]
out = {"jp": {"id": JP_ID, "media": jp_media}, "images": {k: v["id"] for k, v in media.items()}}
for j in JOBS:
    p = api("/wp-json/wp/v2/posts", {
        "title": j["title"], "slug": BASE_SLUG + j["suffix"], "content": load(j["md"], j["lang"]),
        "status": "draft", "categories": CATS, "author": 2, "featured_media": j["media"],
        "lang": j["lang"],
        "meta": {"jetpack_publicize_message": j["sns"]},
    }, "POST")
    out[j["lang"]] = {"id": p["id"], "slug": p["slug"], "link": p["link"], "media": j["media"]}
    print(j["lang"], p["id"], p["slug"], p["link"])
print(json.dumps(out, ensure_ascii=False))
