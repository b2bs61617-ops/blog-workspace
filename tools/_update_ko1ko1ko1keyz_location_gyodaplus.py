# -*- coding: utf-8 -*-
"""Re-push content of KO1! KO1! KO1KEYZ location drafts (JP14549/KR14553/EN14554) using already-uploaded media."""
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


ns = {}
src = open(REPO + r"\tools\_upload_ko1ko1ko1keyz_location_gyodaplus.py", encoding="utf-8").read()
exec(src[src.index("ALTS = {"):src.index("media = {}")], ns)
ALTS, CAP = ns["ALTS"], ns["CAP"]
SRC = "https://www.youtube.com/watch?v=em11KNTF-iA"
IDS = {"exterior": 14540, "sticker": 14541, "flag": 14542, "gym": 14543, "banner": 14544,
       "phone": 14545, "stairs": 14546, "lockers": 14547, "jungle": 14548}
media = {}
for key, mid in IDS.items():
    m = api(f"/wp-json/wp/v2/media/{mid}")
    s = m["media_details"]["sizes"]
    full = (m["source_url"], m["media_details"]["width"], m["media_details"]["height"])
    media[key] = {"full": full,
                  "large": (s["large"]["source_url"], s["large"]["width"], s["large"]["height"]) if "large" in s else full,
                  "medium": (s["medium"]["source_url"], s["medium"]["width"], s["medium"]["height"])}


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
        c = c.replace("{{IMG_" + key + "}}", fig(key, lang))
    assert "{{" not in c
    return c.strip()


JOBS = [
    (14549, "ko1ko1ko1keyz_location_gyodaplus.html", "ja",
     "コイキーズ「KO1! KO1! KO1KEYZ」キュントゥグン学園のロケ地は、埼玉県行田市の学校スタジオ「ギョウダプラス」(旧太田東小)。"
     "消火器ステッカーの市外局番、体育館の行田市旗、校庭の遊具まで公式写真と6か所一致。EP.3で使われた場所も場面ごとに紹介します。"),
    (14553, "ko1ko1ko1keyz_location_gyodaplus_kr.html", "ko",
     "코이키즈 'KO1! KO1! KO1KEYZ' 큔투군 학원의 촬영지는 사이타마현 교다시의 학교 스튜디오 '교다플러스'(옛 오타히가시 초등학교)예요. 소화기 스티커의 지역번호, 체육관의 교다시 시기, 운동장 놀이기구까지 공식 사진과 6곳이 일치했어요."),
    (14554, "ko1ko1ko1keyz_location_gyodaplus_en.html", "en",
     "The Kyuntugun Academy school in KO1KEYZ's \"KO1! KO1! KO1KEYZ\" is GYODA+, a school studio in Gyoda, Saitama (former Ota-Higashi Elementary). A fire extinguisher sticker, the Gyoda City flag and six matches with official photos, down to the playground equipment, gave it away."),
]
for pid, fn, lang, sns in JOBS:
    p = api(f"/wp-json/wp/v2/posts/{pid}", {"content": load(fn, lang), "status": "draft",
                                            "meta": {"jetpack_publicize_message": sns}}, "POST")
    print(pid, p["status"], p["slug"])
