# -*- coding: utf-8 -*-
import base64, os, json
from pathlib import Path
import requests

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
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

VIDEO_URL = "https://youtu.be/bipgdNcr3ok"


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def hr():
    return '<!-- wp:separator --><hr class="wp-block-separator has-alpha-channel-opacity"/><!-- /wp:separator -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def capbox(ttl, rows, style="is-style-small_ttl"):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;white-space:nowrap;">{k}</td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div class="swell-block-capbox cap_box {style}">
<div class="cap_box_ttl">{ttl}</div>
<div class="cap_box_content">
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>
</div>''')


def build_img_html(media_id, alt, caption):
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{media_id}", headers=HEADERS_AUTH)
    r.raise_for_status()
    media = r.json()
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    full_w = media["media_details"]["width"]
    full_h = media["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    img_src = large["source_url"]
    img_w = large["width"]
    img_h = int(img_w * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {full_w}w'
    html = f'''<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>
</figure>'''
    return f"<!-- wp:html -->\n{html}\n<!-- /wp:html -->"


VIDEO_CAPTION = f'출처:KO1KEYZ 공식 유튜브「🌙 KO1KEYZ Night Routine...⭐️」({VIDEO_URL})'
img1_html = build_img_html(11129, "SIYOUNG 파트의 타이틀 카드", VIDEO_CAPTION)
img2_html = build_img_html(11130, "시트 마스크를 붙인 채 붉은색 LED 뷰티기기를 볼에 대는 SIYOUNG", VIDEO_CAPTION)
img3_html = build_img_html(11131, "드레스룸에서 잠옷을 개는 SIYOUNG", VIDEO_CAPTION)

title = "KO1KEYZ SIYOUNG의 뷰티기기·세럼 가격은?나이트루틴서 공개"

blocks = []

blocks.append(p([
    "KO1KEYZ 공식 유튜브 채널에서, 멤버들 각자의 목욕 후부터 잠들기 전까지를 담은 「🌙 KO1KEYZ Night Routine...⭐️」가 공개되었습니다.",
    "그중에서도 SIYOUNG(박시영)의 파트는 <strong>시트 마스크를 붙인 채 뷰티기기를 사용하는 본격적인 스킨케어</strong>가 공개되어, X(트위터)에서는 &quot;뷰티 간호사로 일하고 있다&quot;는 팬이 사용 아이템을 특정하는 게시물을 올려 화제가 되고 있습니다.",
    "이번 기사에서는 SIYOUNG이 사용하고 있는 세럼과 뷰티기기의 정체, 그리고 그다운 정성스러운 나이트루틴의 흐름을 자세히 소개합니다.",
]))
blocks.append(hr())

blocks.append(h2("영상 정보"))
blocks.append(capbox("영상 정보", [
    ("영상 제목", "🌙 KO1KEYZ Night Routine...⭐️"),
    ("채널", "KO1KEYZ 공식 유튜브"),
    ("공개일", "2026년 8월 10일"),
    ("출연", "DAIKI・ISSA・KEITO・KOSUKE・RYOGA・RYUJI・SHINHAENG・SIYOUNG・TOWA・YOSHIKI・YUKI・YURA 12명(이 기사에서는 SIYOUNG의 파트를 중심으로 소개)"),
    ("URL", f'<a href="{VIDEO_URL}" target="_blank" rel="noopener">{VIDEO_URL}</a>'),
]))
blocks.append(hr())

blocks.append(h2("SIYOUNG(박시영)은 어떤 사람?"))
blocks.append(capbox("SIYOUNG 프로필", [
    ("이름", "박시영(PARK SIYOUNG)"),
    ("생년월일", "2003년 5월 6일"),
    ("나이", "23세(2026년 8월 기준)"),
    ("출신지", "한국・경기도"),
    ("신장", "178cm"),
    ("멤버 컬러", "화이트"),
    ("경력", "7인조 보이그룹 「MIRAE(미래소년)」의 전 멤버. 2021년 데뷔, 2023년 7월 탈퇴"),
]))
blocks.append(p([
    "SIYOUNG은 한국 출신 연습생으로, K-POP식 댄스 실력과 단정한 비주얼을 갖춘 실력파입니다.",
    "7인조 보이그룹 「MIRAE(미래소년)」의 메인 댄서 라인으로 2021년 데뷔했고, 2023년 7월 그룹을 탈퇴한 뒤 2026년 방영된 『PRODUCE 101 JAPAN 新世界(일프4)』에 출연해 KO1KEYZ 멤버가 되었습니다.",
    "이전에 공개되었던 위키풍 프로필 기사(<a href=\"https://chomoand-1.com/parksiyoung_wiki-kr\" target=\"_blank\" rel=\"noopener\">박시영의 위키 경력은? 데뷔 경험 있는 실력파!</a>)에서도 몸을 쓰는 능력과 안무 재현도의 높은 완성도가 소개된 바 있는데, 이번 나이트루틴에서는 그 실력을 뒷받침하는 뷰티 습관이 드러났습니다.",
]))
blocks.append(hr())

blocks.append(h2("과묵하지만 정성스럽게, SIYOUNG의 나이트루틴"))
blocks.append(wphtml('''<div style="border:1px solid #dde3e8;border-left:4px solid #a9b6c2;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f5f7f9;">
<p style="margin:0;"><strong>흐름:</strong>시트 마스크+뷰티기기→토너→세럼→마사지(뷰티기기)→크림→향수→하루를 돌아보는 일기→취침</p>
</div>'''))
blocks.append(img1_html)
blocks.append(p([
    "영상은, 다른 멤버 파트에서 룸메이트로 이름이 언급되었던 SIYOUNG이 조용히 &quot;안녕하세요&quot;라고 인사하는 장면으로 시작됩니다.",
    "조명이 밝은 욕실에서 촬영되었던 KEITO 파트와는 대조적으로, SIYOUNG의 파트는 조명을 낮춘 침실에서 진행되어 차분한 분위기 속에서 담담하게 스킨케어를 이어가는 모습이 인상적입니다.",
    "가장 먼저 하는 것이 시트 마스크로, 붙인 채 뷰티기기를 볼에 대며 &quot;먼저 마스크를 하면서, 이게 중요하다고 생각해서 매일 하고 있어요&quot;라고 이야기합니다.",
    "그다음은 토너, 세럼 순으로 단계를 거치고, 마지막에는 마사지용 뷰티기기로 얼굴 주변 림프를 흘려주는 꼼꼼한 케어를 진행했습니다.",
]))
blocks.append(hr())

blocks.append(h2("밝혀진 뷰티 아이템의 정체는?"))
blocks.append(img2_html)
blocks.append(p([
    "영상을 확인해 본 결과, SIYOUNG이 사용하고 있는 아이템은 다음 두 가지로 보입니다.",
    "첫 번째는 시트 마스크 위에서 볼에 대고 있던 뷰티기기로, 한국 피부과 유래 코스메 브랜드 medicube(메디큐브)의 「부스터 프로X2」로 추정됩니다.",
    "8가지 모드와 8가지 LED 컬러를 탑재한 핸디형 뷰티기기로, 영상에서도 붉은색 LED를 켠 채 마스크 위에서 케어하는 모습이 확인되었습니다.",
    "두 번째는 토너 다음에 사용한 세럼으로, Dr.G(닥터지)의 「R.E.D BLEMISH 클리어 하이알시카 수딩 세럼」과 성분・패키지 특징이 일치합니다.",
    "저분자 히알루론산과 병풀 추출물(시카)을 배합해, 열이 오른 피부를 빠르게 진정시키도록 설계된 세럼으로, 한국에서는 진정 케어의 정석으로 알려져 있습니다.",
]))
blocks.append(capbox("사용 아이템 가격 정리", [
    ("medicube 부스터 프로X2", "35,500엔(세금 포함)"),
    ("Dr.G R.E.D BLEMISH 클리어 하이알시카 수딩 세럼 50mL", "2,750엔(세금 포함)"),
    ("<strong>합계</strong>", "<strong>38,250엔(세금 포함)</strong>"),
], style="is-style-onborder_ttl"))
blocks.append(p([
    "두 가지를 합치면 세금 포함 <strong>38,250엔</strong>이라는 금액이 되는데, 둘 다 한국 코스메답게 진정・정돈 케어에 특화된 아이템으로 구성되어 있는 것이 특징입니다.",
    "다만 영상에서 아이템명이 직접 언급된 것은 아니기 때문에, 어디까지나 영상에서 확인되는 특징을 바탕으로 한 추정이라는 점은 유의해야 합니다.",
]))
blocks.append(capbox("구매처", [
    ("medicube 부스터 프로X2", '<a href="https://themedicube.jp/products/booster-pro-x2" target="_blank" rel="noopener nofollow">MEDICUBE 공식 온라인숍(일본)</a>'),
    ("Dr.G R.E.D BLEMISH 클리어 하이알시카 수딩 세럼", '<a href="https://www.qoo10.jp/shop/drg" target="_blank" rel="noopener nofollow">Dr.G 공식 Qoo10 숍(일본)</a>'),
]))
blocks.append(hr())

blocks.append(h2("하루를 돌아본 뒤 잠드는, SIYOUNG다운 마무리"))
blocks.append(img3_html)
blocks.append(p([
    "스킨케어를 마친 뒤, SIYOUNG은 자기 전 습관으로 &quot;오늘 하루를 보고 확인해서, 제가 오늘 잘못한 게 있으면 내일은 더 완벽한 사람이 되도록 매일 바라요&quot;라고 말하며, 그날의 반성과 바람을 일기처럼 정리하는 시간을 소개했습니다.",
    "화려한 연출이나 토크로 보여주는 타입이 아니라, 담담한 몸짓 곳곳에서 정성스러움이 묻어나는 것이 SIYOUNG다운 점으로, 마지막에는 &quot;끝까지 영상 봐주셔서 정말 감사합니다&quot;라며 조용히 마무리합니다.",
    "MIRAE에서의 활동 경험을 거치며, 몸을 쓰는 방식과 자기 관리에 대한 높은 의식이 곳곳에서 느껴지는 나이트루틴이었습니다.",
]))
blocks.append(hr())

blocks.append(h2("정리"))
blocks.append(wphtml('''<div class="swell-block-capbox cap_box is-style-small_ttl">
<div class="cap_box_ttl">SIYOUNG 나이트루틴 정리</div>
<div class="cap_box_content">
<p class="has-border -border02 wp-block-paragraph">
✔ <strong>사용 아이템(추정)</strong>:medicube 부스터 프로X2(35,500엔)+Dr.G R.E.D BLEMISH 클리어 하이알시카 수딩 세럼(2,750엔)<br>
✔ <strong>합계 금액</strong>:38,250엔(세금 포함)<br>
✔ <strong>사용 타이밍</strong>:시트 마스크 위에서 뷰티기기, 토너 다음에 세럼<br>
✔ <strong>마무리</strong>:하루를 돌아보고, 내일에 대한 바람을 정리한 뒤 취침<br>
✔ <strong>배경</strong>:한국 보이그룹 「MIRAE」 활동 경험을 가진 실력파
</p>
<p>조명을 낮춘 조용한 분위기 속에서 착실하게 케어를 이어가는, SIYOUNG다운 나이트루틴이었습니다.<br>
아직 SIYOUNG의 매력을 잘 모른다는 분들도, 이번 기회에 본편 영상도 함께 봐 보시는 건 어떨까요!</p>
</div>
</div>'''))
blocks.append(wphtml('''<div style="border:1px solid #dde3e8;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f5f7f9;">
<p style="margin:0 0 8px 0;"><strong>SIYOUNG에 대해서는, 이 블로그의 다른 기사에서도 자세히 소개하고 있습니다.</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="https://chomoand-1.com/parksiyoung_wiki-kr" target="_blank" rel="noopener">위키풍 프로필・경력을 정리한 기사</a></li>
<li><a href="https://chomoand-1.com/parksiyoung_gakureki-kr" target="_blank" rel="noopener">학력을 조사한 기사</a></li>
</ul>
</div>'''))

content = "\n\n".join(blocks)
print("content chars:", len(content))

EXISTING_KR_POST_ID = 11138

payload = {"title": title, "content": content, "status": "draft", "featured_media": 11155}
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_KR_POST_ID}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("UPDATED KR POST_ID", post["id"])
print("KR LINK", post["link"])

with open(ROOT / "tmp_siyoung_night_routine_kr_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
