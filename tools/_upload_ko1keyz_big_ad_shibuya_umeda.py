# -*- coding: utf-8 -*-
"""Upload JP + KR + EN drafts: KO1KEYZ debut big ads at Shibuya Big 20 / Umeda D-St. (chomoand-1.com)."""
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


OFFICIAL = "https://x.com/KO1KEYZofficial/status/2106897159719174220"
IMGS = {
    "official": ("ko1keyz_bigad_official.jpg", OFFICIAL,
                 {"ja": "KO1KEYZ大型広告の公式告知画像「KO1KEYZ: VISIT LIST」",
                  "ko": "KO1KEYZ 대형 광고 공식 공지 이미지 'KO1KEYZ: VISIT LIST'",
                  "en": "Official KO1KEYZ: VISIT LIST announcement image for the station ads"}),
    "shibuya": ("ko1keyz_bigad_shibuya.jpg", "https://x.com/randomdaisuki/status/2106969066863026281",
                {"ja": "東急東横線渋谷駅ビッグ20に掲出されたKO1KEYZ12人のソロカット広告",
                 "ko": "도큐 도요코선 시부야역 빅 20에 걸린 KO1KEYZ 12명의 솔로 컷 광고",
                 "en": "KO1KEYZ's 12 solo-shot ad at Big 20, Tokyu Toyoko Line Shibuya Station"}),
    "umeda_corridor": ("ko1keyz_bigad_umeda_corridor.jpg", "https://x.com/gochiusa_mineta/status/2106916573198119039",
                       {"ja": "阪急大阪梅田駅1階D通路に並ぶKO1KEYZのD-St.広告",
                        "ko": "한큐 오사카우메다역 1층 D 통로에 늘어선 KO1KEYZ D-St. 광고",
                        "en": "KO1KEYZ D-St. ads lining D Passage on the 1st floor of Hankyu Osaka-umeda Station"}),
    "umeda_group": ("ko1keyz_bigad_umeda_group.jpg", "https://x.com/gochiusa_mineta/status/2106916573198119039",
                    {"ja": "D-St.のKO1KEYZ集合写真とジャケット写真の面",
                     "ko": "D-St.의 KO1KEYZ 단체 사진과 재킷 사진 면",
                     "en": "The D-St. panel with the KO1KEYZ group photo and jacket photo"}),
    "umeda_four": ("ko1keyz_bigad_umeda_four.jpg", "https://x.com/gochiusa_mineta/status/2106916573198119039",
                   {"ja": "D-St.のKO1KEYZメンバー4人ずつの面",
                    "ko": "D-St.의 KO1KEYZ 멤버 4명씩 들어간 면",
                    "en": "A D-St. panel featuring four KO1KEYZ members"}),
}
CAP = {"ja": "出典:", "ko": "출처:", "en": "Source: "}

media = {}
for key, (fn, src, alts) in IMGS.items():
    m = upload_media(REPO + rf"\images\{fn}", fn, "image/jpeg")
    s = m["media_details"]["sizes"]
    full = (m["source_url"], m["media_details"]["width"], m["media_details"]["height"])
    media[key] = {"id": m["id"], "full": full, "src": src, "alts": alts,
                  "large": (s["large"]["source_url"], s["large"]["width"], s["large"]["height"]) if "large" in s else full,
                  "medium": (s["medium"]["source_url"], s["medium"]["width"], s["medium"]["height"])}
    print("img", key, m["id"])


def fig(key, lang):
    d = media[key]; L = d["large"]; M = d["medium"]; F = d["full"]
    return ('<!-- wp:image {"sizeSlug":"large","linkDestination":"none"} -->\n'
            f'<figure class="wp-block-image size-large"><img src="{L[0]}" alt="{d["alts"][lang]}" width="{L[1]}" height="{L[2]}" style="max-width:100%;height:auto;" '
            f'srcset="{M[0]} {M[1]}w, {L[0]} {L[1]}w, {F[0]} {F[1]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
            f'<figcaption class="wp-element-caption" style="text-align:center;font-size:12px;">{CAP[lang]}{d["src"]}</figcaption></figure>\n'
            '<!-- /wp:image -->')


def load(name, lang):
    c = open(REPO + rf"\articles\{name}", encoding="utf-8").read()
    c = re.sub(r"<hr\s*/?>", "", c)
    for key in IMGS:
        ph = "{{IMG_" + key + "}}"
        assert ph in c, (name, ph)
        c = c.replace(ph, fig(key, lang))
    assert "{{" not in c
    return c.strip()


CATS = [66, 62]
BASE_SLUG = "ko1keyz-big-ad-shibuya-umeda"

jp = api("/wp-json/wp/v2/posts", {
    "title": "KO1KEYZの大型広告はどこ？渋谷・梅田の行き方と期間！",
    "slug": BASE_SLUG,
    "content": load("ko1keyz_big_ad_shibuya_umeda.html", "ja"),
    "status": "draft", "categories": CATS, "author": 2,
    "meta": {"jetpack_publicize_message": (
        "KO1KEYZのデビュー記念大型広告が10/5〜10/11、東急東横線渋谷駅「ビッグ20」と阪急大阪梅田駅「D-St.」①〜④に登場。"
        "渋谷は宮益坂東改札を出てB1出口方面、梅田は1階D通路のHEP FIVE側。行き方と広告デザインの違い、近くのCDショップ展示までまとめました。")},
}, "POST")
JP_ID = jp["id"]
jp_media = upload_media(REPO + r"\images\ko1keyz_big_ad_eyecatch.png", "ko1keyz_big_ad_eyecatch.png", "image/png")["id"]
api(f"/wp-json/wp/v2/posts/{JP_ID}", {"featured_media": jp_media, "status": "draft"}, "POST")
print("JP", JP_ID, jp["link"], "media", jp_media)

kr_media = upload_media(REPO + r"\images\ko1keyz_big_ad_eyecatch_kr.png", "ko1keyz_big_ad_eyecatch_kr.png", "image/png")["id"]

JOBS = [
    dict(lang="ko", suffix="-kr", md="ko1keyz_big_ad_shibuya_umeda_kr.html", media=kr_media,
         title="KO1KEYZ 대형 광고는 어디? 시부야・우메다 가는 길과 기간!",
         sns="KO1KEYZ 데뷔 기념 대형 광고가 10/5~10/11 도큐 도요코선 시부야역 '빅 20'과 한큐 오사카우메다역 'D-St.' ①~④에 등장했어요. 시부야는 미야마스자카 동쪽 개찰구로 나가 B1 출구 방면, 우메다는 1층 D 통로 HEP FIVE 쪽이에요."),
    dict(lang="en", suffix="-en", md="ko1keyz_big_ad_shibuya_umeda_en.html", media=jp_media,
         title="Where Are KO1KEYZ's Big Station Ads? Shibuya & Umeda Guide!",
         sns="KO1KEYZ's debut ads are up Oct 5-11 at \"Big 20\" in Tokyu Toyoko Line Shibuya Station and \"D-St.\" (1-4) in Hankyu Osaka-umeda Station. In Shibuya, exit the Miyamasuzaka East Gate toward Exit B1; in Umeda, head to 1F D Passage on the HEP FIVE side."),
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
