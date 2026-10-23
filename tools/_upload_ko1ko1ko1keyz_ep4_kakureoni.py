# -*- coding: utf-8 -*-
"""Upload JP + KR + EN drafts: KO1! KO1! KO1KEYZ EP.4 hide-and-seek recap (chomoand-1.com)."""
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
SRC = "https://www.youtube.com/watch?v=rAZ4LQYwNoM"


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
    "rules": {"ja": "KO1! KO1! KO1KEYZ EP.4のかくれ鬼のルール", "ko": "KO1! KO1! KO1KEYZ EP.4 숨바꼭질 술래잡기 규칙", "en": "Hide-and-seek rules in KO1! KO1! KO1KEYZ EP.4"},
    "oni": {"ja": "2階の教室で作戦会議をする鬼のYOSHIKIとRYOGA", "ko": "2층 교실에서 작전 회의를 하는 술래 YOSHIKI와 RYOGA", "en": "Taggers YOSHIKI and RYOGA planning in the 2nd-floor classroom"},
    "keito": {"ja": "KEITOが細工をした1階の保健室", "ko": "KEITO가 장치를 해 둔 1층 보건실", "en": "The 1st-floor nurse's office KEITO set up"},
    "towa": {"ja": "1階職員室の棚に隠れたTOWA", "ko": "1층 교무실 수납장에 숨은 TOWA", "en": "TOWA hiding in a cabinet in the staff room"},
    "issa": {"ja": "校門近くの茂みに隠れるISSA", "ko": "정문 근처 수풀에 숨은 ISSA", "en": "ISSA hiding in the bushes near the school gate"},
    "yura": {"ja": "体育館の裏の木の陰に隠れるYURA", "ko": "체육관 뒤 나무 그늘에 숨은 YURA", "en": "YURA hiding among the trees behind the gym"},
    "start": {"ja": "チャイムが鳴りかくれ鬼が始まった保健室", "ko": "종이 울리고 술래잡기가 시작된 보건실", "en": "The nurse's office as the chime starts the game"},
    "gym": {"ja": "SHINHAENGが見つかった体育館", "ko": "SHINHAENG이 발견된 체육관", "en": "The gym where SHINHAENG was spotted"},
}
FILES = {k: f"ko1ko1ko1keyz_ep4_{k}.jpg" for k in ALTS}
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
BASE_SLUG = "ko1-ko1-ko1keyz-ep4-hide-and-seek"

jp = api("/wp-json/wp/v2/posts", {
    "title": "KO1!KO1!KO1KEYZ EP.4まとめ！かくれ鬼の隠れ場所は？",
    "slug": BASE_SLUG,
    "content": load("ko1ko1ko1keyz_ep4_kakureoni.html", "ja"),
    "status": "draft", "categories": CATS, "author": 2,
    "meta": {"jetpack_publicize_message": (
        "コイキーズ「KO1! KO1! KO1KEYZ」EP.4は放課後かくれ鬼の前編。鬼はYOSHIKIとRYOGA。"
        "TOWAは職員室の棚、ISSAは校門近くの茂み、YURAは体育館裏、RYUJI・KOSUKE・DAIKIは保健室へ。策士KEITOの細工とSIYOUNGの居場所は後編へ。")},
}, "POST")
JP_ID = jp["id"]
jp_media = upload_media(REPO + r"\images\ko1ko1ko1keyz_ep4_eyecatch.png", "ko1ko1ko1keyz_ep4_eyecatch.png", "image/png")["id"]
api(f"/wp-json/wp/v2/posts/{JP_ID}", {"featured_media": jp_media, "status": "draft"}, "POST")
print("JP", JP_ID, jp["link"], "media", jp_media)

kr_media = upload_media(REPO + r"\images\ko1ko1ko1keyz_ep4_eyecatch_kr.png", "ko1ko1ko1keyz_ep4_eyecatch_kr.png", "image/png")["id"]

JOBS = [
    dict(lang="ko", suffix="-kr", md="ko1ko1ko1keyz_ep4_kakureoni_kr.html", media=kr_media,
         title="KO1!KO1!KO1KEYZ EP.4 정리! 숨바꼭질 술래잡기 은신처는?",
         sns="코이키즈 'KO1! KO1! KO1KEYZ' EP.4는 방과 후 숨바꼭질 술래잡기 전편. 술래는 YOSHIKI와 RYOGA. TOWA는 교무실 수납장, ISSA는 정문 근처 수풀, YURA는 체육관 뒤, RYUJI·KOSUKE·DAIKI는 보건실로. KEITO의 장치와 SIYOUNG의 행방은 후편에서."),
    dict(lang="en", suffix="-en", md="ko1ko1ko1keyz_ep4_kakureoni_en.html", media=jp_media,
         title="KO1! KO1! KO1KEYZ EP.4 Recap: Where Did Everyone Hide?",
         sns="KO1! KO1! KO1KEYZ EP.4 is part one of an after-school hide-and-seek. YOSHIKI and RYOGA are it. TOWA hides in a staff-room cabinet, ISSA in bushes by the gate, YURA behind the gym, and RYUJI, KOSUKE and DAIKI in the nurse's office. SIYOUNG's spot is saved for part two."),
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
