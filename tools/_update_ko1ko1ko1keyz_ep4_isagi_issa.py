# -*- coding: utf-8 -*-
"""EP.4 drafts: add the "潔イッサ" caption and the sawtooth-roof gym / jungle gym location match (JP/KR/EN)."""
import json, base64, urllib.request, cv2

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"')
BASE = env["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f'{env["WP_KOIKEYS_USERNAME"]}:{env["WP_KOIKEYS_APP_PASSWORD"]}'.encode()).decode()
SRC = "https://www.youtube.com/watch?v=rAZ4LQYwNoM"
IDS = {"ja": 15113, "ko": 15117, "en": 15118}
FILES = {"ja": "ko1ko1ko1keyz_ep4_kakureoni.html", "ko": "ko1ko1ko1keyz_ep4_kakureoni_kr.html", "en": "ko1ko1ko1keyz_ep4_kakureoni_en.html"}


def api(path, body=None, method="GET"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Authorization", "Basic " + AUTH)
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


def upload_media(path, filename):
    req = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=open(path, "rb").read(), method="POST")
    req.add_header("Authorization", "Basic " + AUTH)
    req.add_header("Content-Type", "image/jpeg")
    req.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


ALTS = {
    "isagi": {"ja": "「潔イッサ」のテロップが出たISSA", "ko": "「潔イッサ」 자막이 나온 ISSA", "en": "ISSA with the \"潔イッサ\" caption"},
    "schoolyard": {"ja": "ギザギザ屋根の体育館とジャングルジムのある校庭", "ko": "톱니 지붕 체육관과 정글짐이 있는 운동장", "en": "The sawtooth-roofed gym and the schoolyard jungle gym"},
}
SHOTS = {"isagi": 461.5, "schoolyard": 458.5}
CAP = {"ja": "出典:", "ko": "출처:", "en": "Source: "}

v = cv2.VideoCapture(REPO + r"\tools\youtube-talent-monitor\frames\ep4\v720.mp4")
media = {}
for key, t in SHOTS.items():
    fn = f"ko1ko1ko1keyz_ep4_{key}.jpg"
    v.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = v.read(); assert ok
    cv2.imwrite(REPO + rf"\images\{fn}", f, [cv2.IMWRITE_JPEG_QUALITY, 88])
    m = upload_media(REPO + rf"\images\{fn}", fn)
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


ISSA_LINE = {
    "ja": ("ISSAは序盤、「みんなあわててますけどね、余裕ですよと、いうところですかね」と余裕の表情。<br>\n",
           "「こんな調子に乗ってたら捕まっちゃうのでね、隠れたいと思います」と続けたところで、画面には「潔イッサ」のテロップが出ました。<br>\n"
           "「潔い」とISSAを組み合わせた言葉遊びで、隠れ場所が決まったときの「茂ミッサ」と同じ作りのテロップです。<br>\n"),
    "ko": ("ISSA는 초반에 「다들 서두르지만 저는 여유입니다」라며 여유 있는 표정을 지었습니다.<br>\n",
           "「이렇게 우쭐대다가는 잡힐 테니까요, 숨으려고 합니다」라고 이어 말하자, 화면에는 「潔イッサ」라는 자막이 나왔습니다.<br>\n"
           "「潔い(이사기요이, 미련 없이 깔끔하다)」와 ISSA를 합친 말장난으로, 은신처를 정했을 때의 「茂ミッサ」와 같은 방식의 자막입니다.<br>\n"),
    "en": ("<p>ISSA started out with supreme confidence, smiling: \"Everyone else is in full panic mode, but look at me, totally chill.\"<br>\n",
           "He went on, \"If I get too cocky I'll get caught, so I'm going to hide,\" and the caption \"潔イッサ\" (Isagi-ISSA) appeared on screen.<br>\n"
           "It is a pun on <em>isagiyoi</em> (graceful, unflinching) and his name, made the same way as the \"Bush-ISSA\" caption shown later at his hiding spot.<br>\n"),
}
LOC_LINE = {
    "ja": "木の壁に緑のカーテンがかかった体育館が、今回の映像とも一致しています。<br>\n",
    "ko": "나무 벽에 녹색 커튼이 쳐진 체육관이 이번 영상과도 일치합니다.<br>\n",
    "en": "The wooden-walled gymnasium draped with green curtains perfectly matches the scenery in this episode.<br>\n",
}
LOC_ADD = {
    "ja": "校舎の外の映像にも、ギザギザ屋根の体育館と、赤と青のジャングルジムがある校庭が映っていて、EP.3で見えた景色と同じです。<br>\n",
    "ko": "교사 밖 영상에도 톱니 모양 지붕의 체육관과 빨강·파랑 정글짐이 있는 운동장이 비치는데, EP.3에서 보인 풍경과 같습니다.<br>\n",
    "en": "Outdoor shots also show the sawtooth-roofed gym and the schoolyard with a red-and-blue jungle gym, the same view seen in EP.3.<br>\n",
}
ISSA_H2 = {"ja": "ISSAとYURA:外の茂みに隠れた2人</h2>\n<!-- /wp:heading -->\n", "ko": None, "en": "ISSA and YURA: The outdoor bush hiders</h2>\n<!-- /wp:heading -->\n"}
MAP = '<!-- wp:html -->\n<iframe src="https://maps.google.com'


def patch(c, lang, img):
    a, add = ISSA_LINE[lang]
    assert c.count(a) == 1, (lang, "issa"); c = c.replace(a, a + add)
    assert c.count(LOC_LINE[lang]) == 1, (lang, "loc"); c = c.replace(LOC_LINE[lang], LOC_LINE[lang] + LOC_ADD[lang])
    # image right above the ISSA paragraph (after its H2) and right above the map
    h2 = ISSA_H2[lang]
    if h2 is None:
        i = c.index("ISSA는 초반에"); j = c.rfind("<!-- wp:paragraph -->", 0, i)
        c = c[:j] + img("isagi") + "\n\n" + c[j:]
    else:
        assert c.count(h2) == 1, (lang, "h2"); c = c.replace(h2, h2 + "\n" + img("isagi") + "\n")
    assert c.count(MAP) == 1; c = c.replace(MAP, img("schoolyard") + "\n\n" + MAP)
    return c


for lang, pid in IDS.items():
    raw = api(f"/wp-json/wp/v2/posts/{pid}?context=edit")
    assert raw["status"] == "draft", (pid, raw["status"])
    new = patch(raw["content"]["raw"], lang, lambda k: fig(k, lang))
    api(f"/wp-json/wp/v2/posts/{pid}", {"content": new, "status": "draft"}, "POST")
    p = REPO + rf"\articles\{FILES[lang]}"
    local = patch(open(p, encoding="utf-8").read(), lang, lambda k: "{{IMG_" + k + "}}")
    open(p, "w", encoding="utf-8").write(local)
    print("updated", lang, pid)
print(json.dumps({k: d["id"] for k, d in media.items()}))
