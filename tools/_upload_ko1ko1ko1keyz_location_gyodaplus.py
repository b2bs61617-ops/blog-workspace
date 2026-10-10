# -*- coding: utf-8 -*-
"""Upload JP + KR + EN drafts: KO1! KO1! KO1KEYZ location = GYODA+ (former Ota-Higashi ES, Gyoda) (chomoand-1.com)."""
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
SRC = "https://www.youtube.com/watch?v=em11KNTF-iA"


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
    "exterior": {"ja": "KO1! KO1! KO1KEYZ EP.3の校庭に映る時計付きのガラス張り階段室と校舎", "ko": "KO1! KO1! KO1KEYZ EP.3 운동장 뒤로 보이는 시계 달린 유리 계단실과 교사", "en": "The school building with a glass clock stairwell seen in KO1! KO1! KO1KEYZ EP.3"},
    "sticker": {"ja": "廊下の窓辺に貼られた消火器ステッカー", "ko": "복도 창가에 붙은 소화기 스티커", "en": "Fire extinguisher sticker by the hallway window"},
    "flag": {"ja": "体育館ステージに掲げられた行田市旗", "ko": "체육관 무대에 걸린 교다시 시기", "en": "The Gyoda City flag on the gym stage"},
    "gym": {"ja": "KEITOとRYOGAが撮影した体育館とステージ", "ko": "KEITO와 RYOGA가 촬영한 체육관과 무대", "en": "The gym and stage where KEITO and RYOGA shot"},
    "banner": {"ja": "体育館2階の「根気 本気 元気」の横断幕", "ko": "체육관 2층의 '根気 本気 元気' 현수막", "en": "The banner in the gym's upper gallery"},
    "phone": {"ja": "黒板横の壁掛け電話を使うYOSHIKI", "ko": "칠판 옆 벽걸이 전화를 쓰는 YOSHIKI", "en": "YOSHIKI using the wall phone beside the blackboard"},
    "stairs": {"ja": "YURAとYOSHIKIが撮影した赤い手すりの階段", "ko": "YURA와 YOSHIKI가 촬영한 빨간 난간 계단", "en": "The red-railed staircase where YURA and YOSHIKI shot"},
    "lockers": {"ja": "緑と黄色の縦じま壁の昇降口", "ko": "초록·노랑 세로줄 벽의 현관", "en": "The entrance with a green-and-yellow striped wall"},
    "jungle": {"ja": "校庭のジャングルジムとギザギザ屋根の体育館", "ko": "운동장의 정글짐과 톱니 지붕 체육관", "en": "The jungle gym and sawtooth-roofed gym in the schoolyard"},
}
FILES = {k: f"ko1ko1ko1keyz_location_{k}.jpg" for k in ALTS}
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
BASE_SLUG = "ko1ko1ko1keyz-location-gyoda-plus"

jp = api("/wp-json/wp/v2/posts", {
    "title": "KO1!KO1!KO1KEYZのロケ地はどこ？行田の廃校と判明！",
    "slug": BASE_SLUG,
    "content": load("ko1ko1ko1keyz_location_gyodaplus.html", "ja"),
    "status": "draft", "categories": CATS, "author": 2,
    "meta": {"jetpack_publicize_message": (
        "コイキーズ「KO1! KO1! KO1KEYZ」キュントゥグン学園のロケ地は、埼玉県行田市の学校スタジオ「ギョウダプラス」(旧太田東小)。"
        "消火器ステッカーの市外局番、体育館の行田市旗、公式写真との5か所の一致が決め手。EP.3で使われた場所も場面ごとに紹介します。")},
}, "POST")
JP_ID = jp["id"]
jp_media = upload_media(REPO + r"\images\ko1ko1ko1keyz_location_eyecatch.png", "ko1ko1ko1keyz_location_eyecatch.png", "image/png")["id"]
api(f"/wp-json/wp/v2/posts/{JP_ID}", {"featured_media": jp_media, "status": "draft"}, "POST")
print("JP", JP_ID, jp["link"], "media", jp_media)

kr_media = upload_media(REPO + r"\images\ko1ko1ko1keyz_location_eyecatch_kr.png", "ko1ko1ko1keyz_location_eyecatch_kr.png", "image/png")["id"]

JOBS = [
    dict(lang="ko", suffix="-kr", md="ko1ko1ko1keyz_location_gyodaplus_kr.html", media=kr_media,
         title="KO1!KO1!KO1KEYZ 촬영지는 어디? 교다의 폐교로 판명!",
         sns="코이키즈 'KO1! KO1! KO1KEYZ' 큔투군 학원의 촬영지는 사이타마현 교다시의 학교 스튜디오 '교다플러스'(옛 오타히가시 초등학교)예요. 소화기 스티커의 지역번호, 체육관의 교다시 시기, 공식 사진과의 5곳 일치가 결정적 근거예요."),
    dict(lang="en", suffix="-en", md="ko1ko1ko1keyz_location_gyodaplus_en.html", media=jp_media,
         title="Where Is KO1! KO1! KO1KEYZ Filmed? A Former School in Gyoda!",
         sns="The Kyuntugun Academy school in KO1KEYZ's \"KO1! KO1! KO1KEYZ\" is GYODA+, a school studio in Gyoda, Saitama (former Ota-Higashi Elementary). A fire extinguisher sticker, the Gyoda City flag in the gym and five matches with official photos gave it away."),
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
