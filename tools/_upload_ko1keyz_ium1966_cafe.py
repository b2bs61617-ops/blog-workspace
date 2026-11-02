# -*- coding: utf-8 -*-
"""Upload JP + KR + EN drafts: KO1KEYZ Korea Vlog hanok cafe ium1966 (chomoand-1.com)."""
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


VLOG = "https://www.youtube.com/watch?v=EPf6uKYCBeY"
FAN = "https://x.com/shiro_whitemusk/status/2117144803830088007"
SRC = {"telop": VLOG, "table": VLOG, "cake": FAN, "front": FAN}
CAP = {
    "telop": {"ja": "出典：KO1KEYZ公式YouTube「[#KO1LOG] KO1KEYZ Korea Vlog｜KEITO KOSUKE RYUJI TOWA YOSHIKI」より",
              "ko": "출처: KO1KEYZ 공식 YouTube '[#KO1LOG] KO1KEYZ Korea Vlog｜KEITO KOSUKE RYUJI TOWA YOSHIKI'",
              "en": "Source: KO1KEYZ official YouTube, \"[#KO1LOG] KO1KEYZ Korea Vlog | KEITO KOSUKE RYUJI TOWA YOSHIKI\""},
}
CAP["table"] = CAP["telop"]
CAP["cake"] = {"ja": "出典：", "ko": "출처: ", "en": "Source: "}
CAP["front"] = CAP["cake"]
ALTS = {
    "telop": {"ja": "韓国VlogでIUM1996のテロップが出た韓屋カフェの座敷", "ko": "한국 브이로그에서 IUM1996 자막이 나온 한옥 카페의 좌식 방", "en": "The floor-seating room of the hanok cafe shown with the IUM1996 caption in the Korea Vlog"},
    "table": {"ja": "ium1966でマンゴーのパフェやドリンクを囲むKO1KEYZ", "ko": "ium1966에서 망고 파르페와 음료를 둘러싼 KO1KEYZ", "en": "KO1KEYZ with mango parfaits and drinks at ium1966"},
    "cake": {"ja": "ium1966の抹茶ドリンクとシャインマスカットの生クリームケーキ", "ko": "ium1966의 말차 음료와 샤인머스캣 생크림 케이크", "en": "A matcha drink and a Shine Muscat cream cake at ium1966"},
    "front": {"ja": "弘大の韓屋カフェium1966の外観", "ko": "홍대 한옥 카페 ium1966 외관", "en": "Exterior of the hanok cafe ium1966 in Hongdae"},
}
FILES = {"telop": "ko1keyz_ium1966_vlog_telop.jpg", "table": "ko1keyz_ium1966_vlog_table.jpg",
         "cake": "ko1keyz_ium1966_fan_cake.jpg", "front": "ko1keyz_ium1966_fan_front.jpg"}

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
    cap = CAP[key][lang] if SRC[key] == VLOG else CAP[key][lang] + SRC[key]
    return ('<!-- wp:html -->\n<figure class="wp-block-image size-large" style="margin:8px 0 16px 0;"><img src="' + L[0] + '" alt="' + ALTS[key][lang].replace('"', "&quot;") + '" '
            f'width="{L[1]}" height="{L[2]}" style="max-width:100%;height:auto;" loading="lazy" '
            f'srcset="{M[0]} {M[1]}w, {L[0]} {L[1]}w, {F[0]} {F[1]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
            f'<figcaption class="wp-element-caption" style="text-align:center;font-size:12px;">{cap}</figcaption></figure>\n<!-- /wp:html -->')


def load(name, lang):
    c = open(REPO + rf"\articles\{name}", encoding="utf-8").read()
    c = re.sub(r"<hr\s*/?>", "", c)
    for key in FILES:
        ph = "{{IMG_" + key + "}}"
        assert ph in c, (name, ph)
        c = c.replace(ph, fig(key, lang))
    assert "{{" not in c, name
    return c.strip()


CATS = [66, 104]
BASE_SLUG = "ko1keyz-korea-vlog-hanok-cafe-ium1966"

jp = api("/wp-json/wp/v2/posts", {
    "title": "【未】【KO1KEYZ】TOWAたちが行った弘大の韓屋カフェはどこ？聖地巡礼ガイド！",
    "slug": BASE_SLUG,
    "content": load("ko1keyz_ium1966_hanok_cafe.html", "ja"),
    "status": "draft", "categories": CATS, "author": 2,
    "meta": {"jetpack_publicize_message": (
        "コイキーズの韓国Vlogで、TOWAたち5人が最後に行った韓屋カフェはどこ？テロップの「1996」は実は数字ちがい。"
        "「今までで1番」と言ったパフェの値段、座敷の雰囲気、駅からの行き方と、秋の限定ケーキまでまとめました。")},
}, "POST")
JP_ID = jp["id"]
jp_media = upload_media(REPO + r"\images\ko1keyz_ium1966_eyecatch.png", "ko1keyz_ium1966_eyecatch.png", "image/png")["id"]
api(f"/wp-json/wp/v2/posts/{JP_ID}", {"featured_media": jp_media, "status": "draft"}, "POST")
print("JP", JP_ID, jp["link"], "media", jp_media)

kr_media = upload_media(REPO + r"\images\ko1keyz_ium1966_eyecatch_kr.png", "ko1keyz_ium1966_eyecatch_kr.png", "image/png")["id"]

JOBS = [
    dict(lang="ko", suffix="-kr", cats=[74, 108], md="ko1keyz_ium1966_hanok_cafe_kr.html", media=kr_media,
         title="【未】【KO1KEYZ】TOWA 등이 간 홍대 한옥 카페는 어디? 성지순례 가이드!",
         sns="코이키즈 한국 브이로그에서 TOWA 등 5명이 마지막으로 간 한옥 카페는? 자막의 '1996'은 사실 숫자가 바뀐 것. '지금까지 1등'이라던 파르페 가격, 좌식 방 분위기, 역에서 가는 길, 가을 한정 케이크까지 정리했어요."),
    dict(lang="en", suffix="-en", cats=[110, 114], md="ko1keyz_ium1966_hanok_cafe_en.html", media=jp_media,
         title="【未】[KO1KEYZ] The Hongdae Hanok Cafe from TOWA's Korea Vlog: Visit Guide",
         sns="Where is the hanok cafe TOWA and four other KO1KEYZ members visited in their Korea Vlog? The \"1996\" caption has the digits swapped. Parfait prices, the floor-seating room, directions from the station and the autumn cake, all in one guide."),
]
out = {"jp": {"id": JP_ID, "media": jp_media}, "images": {k: v["id"] for k, v in media.items()}}
for j in JOBS:
    p = api("/wp-json/wp/v2/posts", {
        "title": j["title"], "slug": BASE_SLUG + j["suffix"], "content": load(j["md"], j["lang"]),
        "status": "draft", "categories": j["cats"], "author": 2, "featured_media": j["media"],
        "lang": j["lang"],
        "meta": {"jetpack_publicize_message": j["sns"]},
    }, "POST")
    out[j["lang"]] = {"id": p["id"], "slug": p["slug"], "link": p["link"], "media": j["media"]}
    print(j["lang"], p["id"], p["slug"], p["link"])
print(json.dumps(out, ensure_ascii=False))
