# -*- coding: utf-8 -*-
"""KEITO(小野慶人) アリミノ スパイスプラス ウェットワックス パッケージモデル説記事: JP + KR + EN 下書き投稿。"""
import json, base64, os, re, subprocess, sys
from pathlib import Path
import urllib.request

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
WP_USER = ENV["WP_KOIKEYS_USERNAME"]
WP_PASS = ENV["WP_KOIKEYS_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HDR = {"Authorization": f"Basic {AUTH}"}

FALLBACK_SLUG = "keito-arimino-spiceplus-package"


def api(path, payload, method="POST"):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(WP_URL + path, data=data, method=method,
                                 headers={**HDR, "Content-Type": "application/json; charset=utf-8"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def upload_media(path, fname):
    req = urllib.request.Request(WP_URL + "/wp-json/wp/v2/media", data=Path(path).read_bytes(), method="POST",
                                 headers={**HDR, "Content-Type": "image/png",
                                          "Content-Disposition": f'attachment; filename="{fname}"'})
    return json.loads(urllib.request.urlopen(req, timeout=90).read())


def get_slug(title, fallback):
    try:
        import urllib.parse
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={urllib.parse.quote(title)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=15).read())
        en = "".join(seg[0] for seg in data[0])
        slug = re.sub(r"[^a-z0-9\s-]", "", en.lower())
        slug = re.sub(r"\s+", "-", slug.strip())
        slug = re.sub(r"-+", "-", slug)[:30].rstrip("-")
        return slug or fallback
    except Exception as e:
        print("translate failed:", e)
        return fallback


def plain_len(html):
    return len(re.sub(r"<!--.*?-->|<[^>]+>", "", html, flags=re.S))


def make_eyecatch(top, main, bottom, out_name, seed, lang=None):
    out = ROOT / "images" / out_name
    cmd = [sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
           "--top", top, "--main", main, "--bottom", bottom,
           "--out", str(out), "--seed", str(seed)]
    if lang:
        cmd += ["--lang", lang]
    subprocess.run(cmd, check=True)
    return upload_media(out, out_name)["id"]


def post_new(title, content, slug, categories, summary, featured_media, lang=None, ja_id=None):
    payload = {"title": title, "content": content, "slug": slug, "status": "draft",
               "categories": categories, "author": 2, "featured_media": featured_media,
               "meta": {"jetpack_publicize_message": summary}}
    if lang:
        payload["lang"] = lang
        payload["translations"] = {"ja": ja_id}
    return api("/wp-json/wp/v2/posts", payload)


# ============================ JAPANESE ============================
TITLE = "【KEITO】ワックスのパッケージモデルは小野慶人？"
md = (ROOT / "articles" / "ko1keyz_keito_arimino_spiceplus_package.md").read_text(encoding="utf-8")
JP_CONTENT = re.sub(r"\A#[^\n]*\n+", "", md).strip()
assert "<hr" not in JP_CONTENT and "\n---\n" not in JP_CONTENT, "hr found"

JP_SUMMARY = ("KO1KEYZのKEITO(小野慶人)がアリミノ「スパイスプラス ウェットワックス」のパッケージモデルでは、という声がXで広がっています。"
             "続報では一般人時代のスポット仕事の一つ、同時期にKOSEのメイクモデルも、という証言も。"
             "いずれも質問サイト発の未確認情報で、商品の詳細やモデル時代の経歴とあわせて整理しました。")

SLUG = get_slug(TITLE, FALLBACK_SLUG)
print("JP SLUG:", SLUG, "| len(content):", plain_len(JP_CONTENT), "| len(title):", len(TITLE))

jp_eye_id = make_eyecatch(
    "KEITOがワックスのパッケージモデル？", "KO1KEYZ", "アリミノSPICE+ウェットワックスの噂",
    "ko1keyz_keito_arimino_spiceplus_package_eyecatch.png", seed=0)
print("JP eyecatch media id:", jp_eye_id)

jp_post = post_new(TITLE, JP_CONTENT, SLUG, [66, 63, 94], JP_SUMMARY, jp_eye_id)
JP_ID = jp_post["id"]
print("JP_POST_ID:", JP_ID, "| slug:", jp_post["slug"], "| preview:", f"{WP_URL}/?p={JP_ID}")

# ============================ KOREAN ============================
KR_TITLE = "KO1KEYZ KEITO(오노 케이토)가 왁스 패키지 모델이었다?"

KR_CONTENT = """<!-- wp:paragraph -->
<p>KO1KEYZ의 KEITO(오노 케이토)를 두고, 「드러그스토어에서 파는 헤어 왁스 패키지에 찍혀 있는 사람이 KEITO 아니야?」라는 목소리가 X에서 퍼지며 564건이 넘는 「좋아요」를 모으고 있습니다.<br>
화제가 된 상품은 아리미노의 「스파이스 플러스 웨트 왁스」이고, 계기는 어느 질문 사이트에서의 대화였습니다.<br>
다만 <strong>아리미노와 KEITO 측 어느 쪽에서도 공식 발표는 없으며, 패키지 모델이 KEITO 본인인지 여부는 현재 확인되지 않았습니다</strong>. 이 기사에서는 무엇이 화제가 되고 있는지, 그 왁스가 어떤 상품인지, 그리고 KEITO의 「일반인 시절」 활동을 근거로 「있을 법한 이야기인지」를 정리합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #f2ddc4;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;background:#fdf6ee;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">화제의 기본 정보</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;width:32%;">인물</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">KEITO(오노 케이토／KO1KEYZ)</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">화제의 상품</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">아리미노 스파이스 플러스 웨트 왁스(80g・세금 포함 1,540엔)</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">향</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">풋사과(페어＆민트) 향</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">계기</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">질문 사이트 글이 X에서 확산(2026년 8월 30일경). 후속 글에서 KOSE 메이크업 모델설도 등장</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">상황</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">「일반인 시절의 단발성 일 중 하나」라는 팬의 증언. 공식 발표는 없고 미확인</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">왁스 패키지가 「KEITO 아니야?」라며 화제로</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>X에서 퍼지고 있는 것은 온라인 쇼핑몰 상품 페이지와 질문 사이트에서의 대화를 한 장으로 정리한 이미지입니다.<br>
거기에서는 드러그스토어에서 일한다는 사람이 「확인해 보니 지금은 이미 다른 사람 패키지로 바뀐 것 같다」 「내가 일하는 매장에는 KEITO 버전이 2개 정도밖에 남아 있지 않았다」라고 답하고 있습니다.<br>
글에는 「오노케이토다!! 대단해」 같은 놀라움의 한마디가 덧붙어, KO1KEYZ 팬들 사이에서 「모델 시절에 이런 일도 했었구나」라고 받아들여졌습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>이 글에는 후속도 있어, 다른 질문 사이트의 답변으로 「왁스 건은 오노 씨가 일반인 시절(Popteen 관련 사무소를 나와, 사회인이 된 뒤 사무소에 소속되어 있지 않던 시기)에 하던 일 중 하나」 「같은 시기에 KOSE의 메이크업 모델 등도 하고 있다」라는 설명이 나오고 있습니다.<br>
이에 따르면, 화제의 패키지는 데뷔 전——그것도 소속 사무소가 없던 사회인 시절의 단발성 일이었다는 이야기가 됩니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>다만 왁스 튜브에 실린 얼굴 사진은 꽤 작고, 헤어스타일도 메이크업도 모델용입니다.<br>
SNS에서도 「닮았지만 단언은 못 하겠다」라는 신중한 견해가 많아, 지금으로서는 <strong><span class="swl-marker mark_orange" style="font-size:1.15em;">팬의 증언과 추측 단계</span></strong>에 머물러 있습니다. 아리미노・KOSE의 공식 사이트나 KEITO 본인의 SNS에서 기용을 인정하는 정보는 나오지 않았습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">화제의 왁스 「아리미노 스파이스 플러스 웨트 왁스」란?</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #f2ddc4;border-left:4px solid #e0812f;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#fdf6ee;">
<p style="margin:0;"><strong>상품명:</strong>아리미노 스파이스 플러스(SPICE+) 웨트 왁스</p>
<p style="margin:4px 0 0 0;"><strong>용량・가격:</strong>80g／희망 소비자가 세금 포함 1,540엔</p>
<p style="margin:4px 0 0 0;"><strong>타입:</strong>물기 있는 윤기・다발감을 오래 유지하는 웨트 하드 계열</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>아리미노의 「스파이스 플러스(SPICE+)」는, 미용사들의 지지가 두터웠던 「스파이스 프리미엄」을 2021년경 풀 리뉴얼해 탄생한 남성용 스타일링 브랜드입니다.<br>
그중 웨트 왁스는, 젖은 듯한 윤기와 다발감을 장시간 유지하는 타입으로, 어른스럽고 나른한 숏〜미디엄에 어울린다고 공식은 설명하고 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>용량은 80g, 희망 소비자가는 세금 포함 1,540엔. 풋사과(페어＆민트) 향으로, 드러그스토어나 버라이어티숍에서 널리 취급되는 스테디셀러 아이템입니다.<br>
대형 온라인 쇼핑몰의 리뷰는 별점 4.2 안팎(900건 이상)으로 평가도 높고, 상품 페이지에 「최근 한 달간 300개 이상 구매됨」이라고 표시될 만큼 잘 나가는 인기 상품이기도 합니다.<br>
즉, 많은 사람이 일상적으로 집어 드는 왁스 패키지에, 데뷔 전의 KEITO로 보이는 인물이 찍혀 있었다——는 점이 팬에게 놀라운 포인트가 되고 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #e8d6bd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#e0812f;color:#fff;">스파이스 플러스 웨트 왁스 구입처</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:#fdf6ee;">
<li style="margin:0 0 8px 0;"><a href="https://www.arimino.co.jp/products/spiceplus/wet_wax/" target="_blank" rel="noopener">아리미노 공식 사이트 상품 페이지</a></li>
<li style="margin:0 0 8px 0;"><a href="https://search.rakuten.co.jp/search/mall/%E3%82%A2%E3%83%AA%E3%83%9F%E3%83%8E%20%E3%82%B9%E3%83%91%E3%82%A4%E3%82%B9%E3%83%97%E3%83%A9%E3%82%B9%20%E3%82%A6%E3%82%A7%E3%83%83%E3%83%88%E3%83%AF%E3%83%83%E3%82%AF%E3%82%B9/" target="_blank" rel="noopener">라쿠텐에서 「아리미노 스파이스 플러스 웨트 왁스」 검색</a></li>
<li style="margin:0;"><a href="https://www.amazon.co.jp/s?k=%E3%82%A2%E3%83%AA%E3%83%9F%E3%83%8E+%E3%82%B9%E3%83%91%E3%82%A4%E3%82%B9%E3%83%97%E3%83%A9%E3%82%B9+%E3%82%A6%E3%82%A7%E3%83%83%E3%83%88%E3%83%AF%E3%83%83%E3%82%AF%E3%82%B9" target="_blank" rel="noopener">아마존에서 「아리미노 스파이스 플러스 웨트 왁스」 검색</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>유통량이 많은 상품이라, 드러그스토어나 디스카운트 스토어 매장에서도 찾기 쉬운 왁스입니다.<br>
다만 뒤에서 이야기하듯, 현재 매장에 놓인 것은 패키지 디자인이나 모델 사진이 교체된 시기로 보이기 때문에, 화제가 된 「KEITO 버전」과 같은 모습이라고는 할 수 없습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">KEITO의 「일반인 시절」 일이란?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>KEITO는 2020년경부터 「Men's Popteen」의 전속 모델을 약 2년 맡아, 대학 재학 중에 간사이와 도쿄를 오가며 지면과 영상 일을 쌓아 왔습니다.<br>
그 후에는 Popteen 관련 사무소를 떠나, 종합 PR 회사(주식회사 플래티넘)에서 회사원으로 일하면서, 평일은 회사원・휴일은 모델이라는 두 가지 일을 병행합니다.<br>
2025년 말에 PR 회사를 퇴사하고 「PRODUCE 101 JAPAN 신세계」에 참가해, 파이널에서 순위를 크게 올려 7위로 KO1KEYZ 데뷔 멤버에 선발되었습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>이번에 화제가 된 왁스나 KOSE 메이크업 모델 일은, 팬의 설명에 따르면 이 「사무소에 소속되어 있지 않던 사회인 시절」에 받은 단발성 건으로 여겨지고 있습니다.<br>
고단샤 「Men's VOCE」에서는 남성 모델・크리에이터로서 스킨케어와 메이크업 연재도 가지고 있어, 뷰티 분야에 강한 인물로 알려져 있기도 합니다.<br>
소속 사무소가 없는 프리랜서 입장에서, 헤어케어나 코스메 상품 비주얼・메이크업 모델에 기용되었다——는 흐름 자체는, 경력과 잘 맞아떨어집니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #f2ddc4;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;background:#fdf6ee;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">KEITO 프로필</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;width:32%;">이름</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">KEITO(오노 케이토)</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">생년월일</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">2000년 7월 25일</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">출신</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">고치현</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">키</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">약 172cm</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">그룹</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">KO1KEYZ(멤버 컬러: 오렌지)</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">모델 경력</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">Men's Popteen 전속 모델(2020년경〜약 2년), Men's VOCE 연재, 사회인 시절엔 프리로 코스메・헤어 계열 모델 일도(팬 정보)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>특히 KEITO는 「내추럴 계열의 깔끔한 비주얼」이 강점이라, 폭넓은 층에게 가닿는 드러그스토어 코스메나 왁스의 이미지와도 잘 어울릴 것 같습니다.<br>
다만 이것들은 어디까지나 팬 발(發) 정보로, 건의 명칭이나 시기를 제조사가 공표한 것은 아니라는 점은 짚어 두고 싶습니다.<br>
KEITO가 어떤 길을 거쳐 KO1KEYZ에 도달했는지는, <a href="https://chomoand-1.com/ono-keito-p101-68" target="_blank" rel="noopener">오노 케이토는 누구? 모델・크리에이터 경력을 정리한 기사(일본어)</a>에서도 자세히 소개하고 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">현재 패키지는 어떻게 되어 있나?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>질문 사이트에서 드러그스토어 점원이 답한 대로, 지금 매장에 놓인 「스파이스 플러스 웨트 왁스」는 패키지 모델 사진이 교체된 시기로 보입니다.<br>
스파이스 시리즈는 리뉴얼 때마다 디자인이나 시리즈 특유의 「얼굴 마크」를 바꿔 온 이력이 있어, 모델 사진 교체 자체는 드문 일이 아닙니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>그래서 설령 KEITO가 기용되었다 하더라도, 그것은 몇 년 전의 한 시기뿐이라는 이야기가 됩니다.<br>
지금부터 매장에서 「KEITO 버전」을 찾아도 발견하지 못할 가능성이 높다는 것이 팬들 사이의 받아들임입니다.<br>
진위를 포함해, 아리미노나 KEITO 측에서 새로운 정보가 나오면 이 기사에 추가하겠습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">정리</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:2px solid #e0812f;border-radius:8px;background:rgba(224,129,47,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; X에서 KEITO(오노 케이토)가 「헤어 왁스 패키지 모델 아니야?」라며 화제로<br>
&#10003; 상품은 아리미노 「스파이스 플러스 웨트 왁스」(80g・세금 포함 1,540엔)<br>
&#10003; 후속 글에서는 「일반인 시절의 단발성 일 중 하나」 「같은 시기에 KOSE 메이크업 모델도」라는 팬의 증언도<br>
&#10003; 모두 질문 사이트 발 정보로, 아리미노・KOSE・본인의 공식 발표는 없고 미확인<br>
&#10003; KEITO는 Men's Popteen 전속 모델・Men's VOCE 연재 등 뷰티에 강한 경력이라, 경력과 모순되지는 않음<br>
&#10003; 현재는 다른 디자인／다른 모델로 교체되었다는 목소리가 있어, 「KEITO 버전」은 구하기 어려울 듯
</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>만약 정말로 KEITO의 패키지였다면, 데뷔 전부터 전국 드러그스토어에 "KEITO가 놓여 있었다"는 이야기가 됩니다.<br>
회사원을 하면서 코스메나 헤어 일도 받던 시기가 있었다는 점까지 포함해, 오래된 팬일수록 반가운 발견입니다. 매장에서 「KEITO 버전」 패키지를 만나면 럭키!? 당분간은 장 보러 갈 때마다 왁스 진열대를 계속 확인하게 될 것 같네요!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #f2ddc4;border-left:4px solid #e0812f;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#fdf6ee;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">관련 기사</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-1.com/ono-keito-p101-68" target="_blank" rel="noopener">【일프4】오노 케이토는 누구? 모델・크리에이터, 과거엔 PR 회사 근무도(일본어)</a></li>
<li><a href="https://chomoand-1.com/meimon-keitooo-71" target="_blank" rel="noopener">오노 케이토의 학력은? 출신 고교・대학은 편차치 60 이상 명문!(일본어)</a></li>
<li><a href="https://chomoand-1.com/what-are-the-shoe-sizes-of-ko1-11551" target="_blank" rel="noopener">KO1KEYZ 멤버 12명의 신발 사이즈를 조사한 기사(일본어)</a></li>
</ul>
</div>
<!-- /wp:html -->"""

print("KR len(content):", plain_len(KR_CONTENT), "| len(title):", len(KR_TITLE))
kr_eye_id = make_eyecatch(
    "KEITO가 왁스 패키지 모델?", "KO1KEYZ", "아리미노 SPICE+ 웨트왁스 소문",
    "ko1keyz_keito_arimino_spiceplus_package_eyecatch_kr.png", seed=JP_ID, lang="kr")
print("KR eyecatch media id:", kr_eye_id)
KR_SUMMARY = ("KO1KEYZ의 KEITO(오노 케이토)가 아리미노 「스파이스 플러스 웨트 왁스」의 패키지 모델이었다는 목소리가 X에서 퍼지고 있습니다. "
             "후속 글에서는 일반인 시절의 단발성 일 중 하나, 같은 시기 KOSE 메이크업 모델도 했다는 증언도. "
             "모두 질문 사이트 발 미확인 정보로, 상품 정보와 모델 시절 경력과 함께 정리했습니다.")
kr_post = post_new(KR_TITLE, KR_CONTENT, jp_post["slug"] + "-kr", [74, 78], KR_SUMMARY, kr_eye_id, lang="ko", ja_id=JP_ID)
print("KR_POST_ID:", kr_post["id"], "| slug:", kr_post["slug"], "| preview:", f"{WP_URL}/?p={kr_post['id']}")

# ============================ ENGLISH ============================
EN_TITLE = "Was KO1KEYZ's KEITO a Hair Wax Package Model?"

EN_CONTENT = """<!-- wp:paragraph -->
<p>Fans have been passing around the idea that KEITO (Keito Ono) of KO1KEYZ is the person pictured on the package of a hair wax sold in Japanese drugstores, and the post has drawn more than 564 likes on X.<br>
The product in question is Arimino's "Spice Plus Wet Wax," and it started from an exchange on a Q&amp;A site.<br>
That said, <strong>neither Arimino nor KEITO's side has made any official announcement, so whether the package model is really KEITO is unconfirmed at this point</strong>. This article covers what is being talked about, what kind of product the wax is, and whether it is a plausible story given KEITO's work during his "private citizen" years.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #f2ddc4;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;background:#fdf6ee;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">The talking point at a glance</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;width:32%;">Person</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">KEITO (Keito Ono / KO1KEYZ)</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">Product</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">Arimino Spice Plus Wet Wax (80g, 1,540 yen incl. tax)</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">Scent</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">Green apple (pear &amp; mint) scent</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">Origin</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">A Q&amp;A-site post that spread on X around Aug 30, 2026; a follow-up also raised a KOSE makeup-model claim</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">Status</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">Fans say it was "one of his spot jobs before his idol career." No official confirmation; unverified</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why fans think the wax package might be KEITO</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>What is circulating on X is a single image that combines an online shop's product page with an exchange from a Q&amp;A site.<br>
In it, someone who says they work at a drugstore writes that "when I checked, the package seems to have already switched to a different person," and that "at the store where I work there were only about two of the KEITO version left."<br>
The post is captioned with a surprised "Onokeito!! Amazing," and KO1KEYZ fans took it as "so he did this kind of work back in his modeling days."</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>There is also a follow-up. Another Q&amp;A-site answer explains that "the wax is one of the jobs Ono did during his private-citizen period — after he left the Popteen-related agency and became a company employee with no agency," and that "around the same time he also did makeup-model work for KOSE."<br>
By this account, the package in question dates to before his debut — a spot job from a period when he had no agency at all.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Still, the face photo on the wax tube is quite small, and the hair and makeup are done in a model style.<br>
On social media, plenty of people are cautious, saying "it looks like him but I can't say for sure," so for now this stays at the <strong><span class="swl-marker mark_orange" style="font-size:1.15em;">level of fan testimony and guesswork</span></strong>. Nothing on Arimino's or KOSE's official sites, or on KEITO's own social media, confirms the casting.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What is "Arimino Spice Plus Wet Wax"?</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #f2ddc4;border-left:4px solid #e0812f;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#fdf6ee;">
<p style="margin:0;"><strong>Product:</strong> Arimino Spice Plus (SPICE+) Wet Wax</p>
<p style="margin:4px 0 0 0;"><strong>Size / price:</strong> 80g / suggested retail 1,540 yen incl. tax</p>
<p style="margin:4px 0 0 0;"><strong>Type:</strong> Wet-hard wax that holds a glossy, piecey finish</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Arimino's "Spice Plus (SPICE+)" is a men's styling brand launched around 2021 as a full renewal of "Spice Premium," which had a strong following among hairstylists.<br>
Within the line, the Wet Wax is described by the brand as a type that keeps a wet-look shine and defined separation for a long time, suited to a grown-up, moody short-to-medium style.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>It comes in an 80g tube at a suggested price of 1,540 yen including tax, in a green apple (pear &amp; mint) scent, and it is a staple widely stocked at drugstores and variety shops.<br>
Reviews on major online stores sit around 4.2 stars (1,000-plus ratings), and the listing even shows "300+ bought in the past month," so it is a brisk seller.<br>
The point for fans is exactly that: a wax that huge numbers of ordinary shoppers pick up every day had someone who looks like a pre-debut KEITO on the package.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #e8d6bd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#e0812f;color:#fff;">Where to buy Spice Plus Wet Wax</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:#fdf6ee;">
<li style="margin:0 0 8px 0;"><a href="https://www.arimino.co.jp/products/spiceplus/wet_wax/" target="_blank" rel="noopener">Arimino official product page</a></li>
<li style="margin:0 0 8px 0;"><a href="https://search.rakuten.co.jp/search/mall/%E3%82%A2%E3%83%AA%E3%83%9F%E3%83%8E%20%E3%82%B9%E3%83%91%E3%82%A4%E3%82%B9%E3%83%97%E3%83%A9%E3%82%B9%20%E3%82%A6%E3%82%A7%E3%83%83%E3%83%88%E3%83%AF%E3%83%83%E3%82%AF%E3%82%B9/" target="_blank" rel="noopener">Search Rakuten for "Arimino Spice Plus Wet Wax"</a></li>
<li style="margin:0;"><a href="https://www.amazon.co.jp/s?k=%E3%82%A2%E3%83%AA%E3%83%9F%E3%83%8E+%E3%82%B9%E3%83%91%E3%82%A4%E3%82%B9%E3%83%97%E3%83%A9%E3%82%B9+%E3%82%A6%E3%82%A7%E3%83%83%E3%83%88%E3%83%AF%E3%83%83%E3%82%AF%E3%82%B9" target="_blank" rel="noopener">Search Amazon for "Arimino Spice Plus Wet Wax"</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Because it is widely distributed, it is an easy wax to find on the shelves of drugstores and discount stores.<br>
As noted below, though, the versions on shelves now appear to be from a period when the package design and model photo had already changed, so they will not necessarily look like the "KEITO version" people are talking about.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What did KEITO do during his "private citizen" years?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>KEITO served as an exclusive model for "Men's Popteen" for about two years from around 2020, building up magazine and video work while shuttling between the Kansai region and Tokyo as a university student.<br>
After that he left the Popteen-related agency and worked as an office employee at a general PR company (Platinum Inc.), keeping up a double life of weekday office work and weekend modeling.<br>
He left the PR company at the end of 2025 to join "PRODUCE 101 JAPAN The Shinsekai," climbed sharply in the finale, and was chosen as a debut member of KO1KEYZ in 7th place.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>According to fans, the wax and the KOSE makeup-model work both date to this "office-worker period with no agency," taken on as one-off jobs.<br>
He has also had a skincare and makeup column in Kodansha's "Men's VOCE" as a male model and creator, and is known for being strong in the beauty field.<br>
The idea that, as a freelancer with no agency, he was cast for cosmetics and haircare visuals and makeup-model work fits his career well.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #f2ddc4;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;background:#fdf6ee;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">KEITO profile</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;width:32%;">Name</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">KEITO (Keito Ono)</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">Date of birth</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">July 25, 2000</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">From</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">Kochi Prefecture</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">Height</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">About 172cm</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">Group</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">KO1KEYZ (member color: orange)</td></tr>
<tr><td style="background:#f6e7d4;border:1px solid #e8d6bd;padding:8px 12px;">Modeling</td><td style="border:1px solid #e8d6bd;padding:8px 12px;">Men's Popteen exclusive model (~2 years from around 2020), Men's VOCE column; freelance cosmetics/hair modeling in his office-worker years (per fans)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>KEITO's strength is a natural, clean-cut look, which would sit well with the image of drugstore cosmetics and wax aimed at a wide audience.<br>
Even so, all of this is fan-sourced, and no maker has publicly named the jobs or the dates, which is worth keeping in mind.<br>
For how KEITO got to KO1KEYZ, see our <a href="https://chomoand-1.com/ono-keito-p101-68" target="_blank" rel="noopener">article on who Keito Ono is and his model/creator career (in Japanese)</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What does the package look like now?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>As the drugstore staffer said on the Q&amp;A site, the "Spice Plus Wet Wax" on shelves now appears to be from a period when the package model photo had changed.<br>
The Spice series has changed its design and its trademark "face mark" with each renewal, so swapping the model photo is nothing unusual.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>So even if KEITO was used, it would only have been for a limited stretch a few years ago.<br>
Fans generally accept that hunting for a "KEITO version" in stores now is unlikely to turn one up.<br>
If Arimino or KEITO's side releases anything new, including on whether it is true, we will add it here.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Summary</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:2px solid #e0812f;border-radius:8px;background:rgba(224,129,47,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; On X, KEITO (Keito Ono) is rumored to be a hair wax package model<br>
&#10003; The product is Arimino "Spice Plus Wet Wax" (80g, 1,540 yen incl. tax)<br>
&#10003; A follow-up adds fan testimony of "one of his pre-debut spot jobs" and "KOSE makeup model around the same time"<br>
&#10003; All of it is from a Q&amp;A site; there is no official word from Arimino, KOSE or KEITO, so it is unverified<br>
&#10003; KEITO has a beauty-heavy resume (Men's Popteen exclusive model, Men's VOCE column), so it is not inconsistent<br>
&#10003; The package is said to have switched to a different design/model, so a "KEITO version" is hard to find now
</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>If it really is KEITO's package, then he was literally on drugstore shelves nationwide long before his debut.<br>
Together with the fact that he took cosmetics and hair jobs while holding down an office job, it is the kind of discovery longtime fans will love. Spotting a "KEITO version" on a shelf would be a lucky find, and you may catch yourself checking the wax aisle every time you shop for a while.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #f2ddc4;border-left:4px solid #e0812f;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#fdf6ee;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">Related articles</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-1.com/ono-keito-p101-68" target="_blank" rel="noopener">Who is Keito Ono? Model, creator and former PR-company employee (in Japanese)</a></li>
<li><a href="https://chomoand-1.com/meimon-keitooo-71" target="_blank" rel="noopener">Keito Ono's education: a top-tier high school and university (in Japanese)</a></li>
<li><a href="https://chomoand-1.com/what-are-the-shoe-sizes-of-ko1-11551" target="_blank" rel="noopener">Shoe sizes of all 12 KO1KEYZ members (in Japanese)</a></li>
</ul>
</div>
<!-- /wp:html -->"""

print("EN len(content):", plain_len(EN_CONTENT), "| len(title):", len(EN_TITLE))
EN_SUMMARY = ("Fans on X think KEITO (Keito Ono) of KO1KEYZ is the package model for Arimino's Spice Plus Wet Wax, "
             "with a follow-up claim that he also did KOSE makeup-model work in the same period. It is all unverified "
             "Q&A-site talk; we lay out the product details and his modeling background.")
en_post = post_new(EN_TITLE, EN_CONTENT, jp_post["slug"] + "-en", [110, 118], EN_SUMMARY, jp_eye_id, lang="en", ja_id=JP_ID)
print("EN_POST_ID:", en_post["id"], "| slug:", en_post["slug"], "| preview:", f"{WP_URL}/?p={en_post['id']}")

(ROOT / "tmp_keito_arimino_spiceplus_ids.txt").write_text(
    f"jp={JP_ID} slug={jp_post['slug']} jp_eyecatch={jp_eye_id}\n"
    f"kr={kr_post['id']} slug={kr_post['slug']} kr_eyecatch={kr_eye_id}\n"
    f"en={en_post['id']} slug={en_post['slug']} en_eyecatch={jp_eye_id}\n",
    encoding="utf-8")
print("\nDONE.")
print("JP edit:", f"{WP_URL}/wp-admin/post.php?post={JP_ID}&action=edit")
