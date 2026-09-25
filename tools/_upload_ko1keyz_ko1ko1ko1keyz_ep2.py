# -*- coding: utf-8 -*-
"""Upload JP + KR + EN drafts: KO1! KO1! KO1KEYZ EP.2 学級裁判 summary article (chomoand-1.com)."""
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
VIDEO = "https://www.youtube.com/watch?v=KJ_NmQr5Pug"


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
    "classroom": {"ja": "学級裁判を開廷する裁判長TOWAと教室のKO1KEYZメンバー", "ko": "학급 재판을 개정하는 재판장 TOWA와 교실의 KO1KEYZ 멤버들", "en": "Judge TOWA opening the class trial with the KO1KEYZ members in the classroom"},
    "daiki_yuzai": {"ja": "パパラッチ罪で有罪となったDAIKI", "ko": "파파라치죄로 유죄가 된 DAIKI", "en": "DAIKI found guilty of Paparazzi"},
    "issa_kawaisugiru": {"ja": "かわいすぎる罪に問われたISSA", "ko": "너무 귀여운 죄로 기소된 ISSA", "en": "ISSA charged with Being Too Cute"},
    "yuki_yuzai": {"ja": "話聞いていない罪で有罪となったYUKI", "ko": "말 안 듣는 죄로 유죄가 된 YUKI", "en": "YUKI found guilty of Not Listening"},
    "ryoga_tension": {"ja": "テンション謎罪に問われたRYOGA", "ko": "텐션 미스터리죄로 기소된 RYOGA", "en": "RYOGA charged with Mysterious Energy"},
}
CAP = {"ja": "出典:", "ko": "출처:", "en": "Source: "}

media = {}
for key in ALTS:
    fn = f"ko1ko1ko1keyz_ep2_{key}.jpg"
    m = upload_media(REPO + rf"\images\{fn}", fn, "image/jpeg")
    s = m["media_details"]["sizes"]
    media[key] = {"id": m["id"], "full": (m["source_url"], m["media_details"]["width"], m["media_details"]["height"]),
                  "large": (s.get("large", {}).get("source_url", m["source_url"]), s.get("large", {}).get("width", m["media_details"]["width"]), s.get("large", {}).get("height", m["media_details"]["height"])),
                  "medium": (s["medium"]["source_url"], s["medium"]["width"], s["medium"]["height"])}
    print("img", key, m["id"])


def fig(key, lang):
    d = media[key]; L = d["large"]; M = d["medium"]; F = d["full"]
    return ('<!-- wp:image {"sizeSlug":"large","linkDestination":"none"} -->\n'
            f'<figure class="wp-block-image size-large"><img src="{L[0]}" alt="{ALTS[key][lang]}" width="{L[1]}" height="{L[2]}" style="max-width:100%;height:auto;" '
            f'srcset="{M[0]} {M[1]}w, {L[0]} {L[1]}w, {F[0]} {F[1]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
            f'<figcaption class="wp-element-caption" style="text-align:center;font-size:12px;">{CAP[lang]}{VIDEO}</figcaption></figure>\n'
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


CATS = [66, 62]
BASE_SLUG = "ko1-ko1-ko1keyz-ep2-class-trial"

jp = api("/wp-json/wp/v2/posts", {
    "title": "KO1!KO1!KO1KEYZ EP.2まとめ！学級裁判で有罪は誰？",
    "slug": BASE_SLUG,
    "content": load("ko1keyz_ko1ko1ko1keyz_ep2_gakkyu_saiban.html", "ja"),
    "status": "draft", "categories": CATS, "author": 2,
    "meta": {"jetpack_publicize_message": (
        "「KO1! KO1! KO1KEYZ」EP.2は裁判長TOWAによる学級裁判。DAIKI・YUKI・RYOGAが有罪、ISSAだけ無罪に。"
        "パパラッチ罪・かわいすぎる罪など4つの裁判の訴えと、懲役10年や5秒真顔といった判決の中身をまとめました。")},
}, "POST")
JP_ID = jp["id"]
jp_media = upload_media(REPO + r"\images\ko1keyz_ko1ko1ko1keyz_ep2_eyecatch.png", "ko1keyz_ko1ko1ko1keyz_ep2_eyecatch.png", "image/png")["id"]
api(f"/wp-json/wp/v2/posts/{JP_ID}", {"featured_media": jp_media, "status": "draft"}, "POST")
print("JP", JP_ID, jp["link"], "media", jp_media)

kr_media = upload_media(REPO + r"\images\ko1keyz_ko1ko1ko1keyz_ep2_eyecatch_kr.png", "ko1keyz_ko1ko1ko1keyz_ep2_eyecatch_kr.png", "image/png")["id"]

JOBS = [
    dict(lang="ko", suffix="-kr", md="ko1keyz_ko1ko1ko1keyz_ep2_gakkyu_saiban_kr.html", media=kr_media,
         title="KO1!KO1!KO1KEYZ EP.2 정리! 학급 재판에서 유죄는 누구?",
         sns="'KO1! KO1! KO1KEYZ' EP.2는 재판장 TOWA의 학급 재판. DAIKI·YUKI·RYOGA는 유죄, ISSA만 무죄였어요. 파파라치죄·너무 귀여운 죄 등 4건의 고소 내용과 징역 10년·5초 무표정 같은 판결을 정리했어요."),
    dict(lang="en", suffix="-en", md="ko1keyz_ko1ko1ko1keyz_ep2_gakkyu_saiban_en.html", media=jp_media,
         title="KO1! KO1! KO1KEYZ EP.2 Recap: Who Was Found Guilty in the Class Trial?",
         sns="In EP.2 of \"KO1! KO1! KO1KEYZ,\" judge TOWA runs a class trial: DAIKI, YUKI and RYOGA are found guilty, and only ISSA is acquitted. Here are all four complaints and sentences, from \"10 years\" to a 5-second straight face."),
]
out = {"jp": {"id": JP_ID, "media": jp_media}}
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
