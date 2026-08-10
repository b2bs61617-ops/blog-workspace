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


def capbox_list(ttl, items, style="is-style-small_ttl"):
    lis = "\n".join(f"<li>「{t}」</li>" for t in items)
    return wphtml(f'''<div class="swell-block-capbox cap_box {style}">
<div class="cap_box_ttl">{ttl}</div>
<div class="cap_box_content">
<ul>
{lis}
</ul>
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
img1_html = build_img_html(11080, "KEITO가 LED 마스크형 뷰티기기를 쓴 채 스트레칭하는 장면", VIDEO_CAPTION)
img2_html = build_img_html(11081, "KEITO가 흰색 핸즈프리형 뷰티기기를 얼굴에 대고 있는 장면", VIDEO_CAPTION)
img3_html = build_img_html(11082, "KEITO가 프로틴 쉐이커를 흔들고 있는 장면", VIDEO_CAPTION)

title = "KO1KEYZ 케이토의 뷰티기기 가격은?나이트루틴서 공개"

blocks = []

blocks.append(p([
    "KO1KEYZ 공식 유튜브 채널에서, 멤버들 각자의 목욕 후부터 잠들기 전까지를 담은 「🌙 KO1KEYZ Night Routine...⭐️」가 공개되었습니다.",
    "그중에서도 KEITO(오노 케이토)의 파트는 <strong>뷰티기기 2종을 번갈아 사용하는 본격적인 스킨케어</strong>가 공개되어, X(트위터)에서는 사용 아이템의 합계 금액을 계산한 게시물까지 등장하며 화제가 되고 있습니다.",
    "이번 기사에서는 KEITO가 사용하고 있는 뷰티기기의 정체와 가격, 그리고 나이트루틴 전체의 흐름을 자세히 소개합니다.",
]))
blocks.append(hr())

blocks.append(h2("영상 정보"))
blocks.append(capbox("영상 정보", [
    ("영상 제목", "🌙 KO1KEYZ Night Routine...⭐️"),
    ("채널", "KO1KEYZ 공식 유튜브"),
    ("공개일", "2026년 8월 10일"),
    ("출연", "DAIKI・ISSA・KEITO・KOSUKE・RYOGA・RYUJI・SHINHAENG・SIYOUNG・TOWA・YOSHIKI・YUKI・YURA 12명(이 기사에서는 KEITO의 파트를 중심으로 소개)"),
    ("URL", f'<a href="{VIDEO_URL}" target="_blank" rel="noopener">{VIDEO_URL}</a>'),
]))
blocks.append(hr())

blocks.append(h2("KEITO(오노 케이토)는 어떤 사람?"))
blocks.append(capbox("KEITO 프로필", [
    ("본명", "오노 케이토(小野慶人)"),
    ("생년월일", "2000년 7월 25일"),
    ("나이", "25세(KO1KEYZ 최연장자)"),
    ("출신지", "고치현"),
    ("신장", "172cm"),
    ("MBTI", "ENTJ"),
    ("일프 성적", "최종 순위 7위(408,598표), 순위권 밖에서 역전해 데뷔"),
]))
blocks.append(p([
    "KEITO는 『PRODUCE 101 JAPAN 新世界』 참가 전, 평일에는 <a href=\"https://chomoand-1.com/keito_work-10086\" target=\"_blank\" rel=\"noopener\">회사원으로 일하면서 뷰티 정보를 발신하는 크리에이터</a>로도 활동했던 경력의 소유자입니다.",
    "Popteen이나 MEN'S VOCE 같은 패션·뷰티 잡지에서 모델도 맡은 적이 있어, 뷰티에 관한 지식과 경험은 12명 중에서도 단연 돋보입니다.",
    "이전에 공개되었던 애용 스킨케어 조사 기사(<a href=\"https://chomoand-1.com/keito_no_item-109\" target=\"_blank\" rel=\"noopener\">오노 케이토의 뷰티법 정리! 애용 스킨케어와 미肌 비결을 철저 조사!</a>)에서도 보습과 투명감 케어에 대한 애착이 소개된 바 있는데, 이번 나이트루틴에서는 한층 더 깊이 있는 뷰티기기에 대한 고집이 드러났습니다.",
]))
blocks.append(hr())

blocks.append(h2("목욕 후부터 잠들기 전까지, 정성스러운 뷰티 루틴"))
blocks.append(wphtml('''<div style="border:1px solid #f3caa0;border-left:4px solid #e8871e;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#fff6ea;">
<p style="margin:0;"><strong>흐름:</strong>입욕→스트레칭하며 뷰티기기(10분)→청즙→스킨케어(뷰티기기 2회)→드라이→가샤(마사지)→프로틴으로 취침</p>
</div>'''))
blocks.append(img1_html)
blocks.append(p([
    "영상은 KEITO가 「얼른 씻고 올게요」라고 말하며 욕실로 향하는 장면으로 시작됩니다.",
    "목욕 후 가장 먼저 하는 것이 스트레칭인데, 그 동안 LED 마스크형 뷰티기기를 착용하고 붉게 빛나는 화면을 보여주며 「뷰티기기가 10분이라서, 10분 스트레칭하면서 시간 낭비 없이 쓰고 있어요」라고 이야기합니다.",
    "스트레칭과 동시에 매일 청즙을 마시는 것도 습관으로 삼고 있다고 하는데, 한정된 시간 안에 케어와 컨디션 관리를 동시에 끝내는 효율성이 돋보입니다.",
    "뷰티기기를 벗은 뒤에는 스킨(화장수)에 이르기까지 여러 단계가 있다는 스킨케어로 넘어가, 머리를 말린 뒤 다음 날 아침의 붓기를 막기 위한 가벼운 가샤 마사지로 마무리하는, 꽤나 꼼꼼한 흐름이었습니다.",
]))
blocks.append(hr())

blocks.append(h2("밝혀진 뷰티기기는 2종류, 합계 얼마?"))
blocks.append(img2_html)
blocks.append(p([
    "영상에 나온 뷰티기기를 확인해 본 결과, 성격이 다른 두 가지 기기를 번갈아 사용하고 있다는 것을 알 수 있었습니다.",
    "첫 번째는 목욕 후 스트레칭 타임에 착용했던 LED 마스크형 기기로, CurrentBody Skin(커런트바디 스킨)의 「LED 라이트 테라피 마스크 시리즈2」로 보입니다.",
    "붉은색을 중심으로 한 LED 라이트를 피부에 조사하는 타입의 뷰티기기로, 전 세계적으로도 점유율이 큰 브랜드의 상위 모델입니다.",
    "두 번째는 스킨케어 과정에서 얼굴에 대고 있던 흰색 핸즈프리형 기기로, 시세이도와 야만(YA-MAN)이 공동 개발한 뷰티 브랜드 「EFFECTIM(에펙팀)」의 「퀵 페이셜 트레이너」와 특징이 일치합니다.",
    "독자 기술인 「간섭파 EMS」를 통해 단 3분의 사용만으로도 표정근에 작용하도록 설계된 뷰티기기입니다.",
]))
blocks.append(capbox("사용 아이템 가격 정리", [
    ("CurrentBody Skin LED 라이트 테라피 마스크 시리즈2", "77,000엔(세금 포함)"),
    ("EFFECTIM 퀵 페이셜 트레이너", "59,400엔(세금 포함)"),
    ("<strong>합계</strong>", "<strong>136,400엔(세금 포함)</strong>"),
], style="is-style-onborder_ttl"))
blocks.append(p([
    "두 가지를 합치면 세금 포함 <strong>136,400엔</strong>이라는 금액이 되는데, X에서도 이 합계 금액을 계산한 게시물이 반응을 모으고 있었습니다.",
    "영상 속에서 KEITO는 두 번째 EFFECTIM에 대해 「내일 촬영이 있어서 붓기를 예방하기 위한 뷰티기기」라고 설명하며, 다음 날 스케줄을 위한 컨디션 조절로 나눠 쓰고 있다는 것을 알 수 있습니다.",
    "스킨케어 마지막에는 「내일 아침 붓고 싶지 않을 때는 밤에도 하지만, 아침에 일어나서도 해요」라고도 말해, 아침저녁 어느 타이밍에도 쓸 수 있는 아이템으로 활용하고 있는 듯합니다.",
]))
blocks.append(hr())

blocks.append(h2("촬영 전날이기에, 프로틴으로 마무리하는 밤"))
blocks.append(img3_html)
blocks.append(p([
    "스킨케어와 머리 말리기를 마친 뒤, KEITO는 「오늘 저녁을 일찍 먹어서 너무 배고파요」라며 공복을 밝히면서도, 「그래도 붓고 싶지 않고 밤도 늦었고 내일 촬영이라 프로틴 마시고 잘게요」라며 굳이 식사 대신 프로틴을 선택하며 하루를 마무리했습니다.",
    "뷰티기기로 붓기 예방에 신경 쓴 직후이니만큼, 취침 전 식사 내용에도 같은 의식이 향해 있다는 것을 알 수 있는 장면입니다.",
    "뷰티 정보 발신자로서의 경험이 뒷받침된, 몸의 안팎을 동시에 케어하는 자세가 엿보이는 나이트루틴이었습니다.",
]))
blocks.append(hr())

blocks.append(h2("SNS 반응"))
blocks.append(capbox_list("뷰티기기의 밝기에 놀라는 반응", [
    "뷰티기기의 너무 강한 빛에 놀라 허둥대는 게 완전 신급",
    "목소리 뒤집힌 거 너무 귀여워",
    "진짜로 당황한 목소리라 ㅋㅋㅋㅋ",
]))
blocks.append(capbox_list("뷰티에 대한 고집에 반응하는 목소리", [
    "오노 케이토와 뷰티기기의 조합이 재밌다",
    "이 뷰티기기 갖고 싶어서 계속 장바구니에 넣어놨는데 아직도 못 사고 있어……",
    "본인의 신조가 몸은 먼저 먹는 것으로 만들어진다는 거라 뷰티기기는 그걸 해결한 다음 얘기인 듯",
]))
blocks.append(p([
    "영상 공개 직후부터, 뷰티기기의 존재감과 꼼꼼한 사용법에 놀라는 반응이 많이 보였습니다.",
    "그중에는 관심은 있지만 가격이 부담스러워 구매를 망설이고 있다는 공감의 목소리도 있어, 136,400엔이라는 금액이 주는 임팩트의 크기를 짐작할 수 있습니다.",
]))
blocks.append(hr())

blocks.append(h2("정리"))
blocks.append(wphtml('''<div class="swell-block-capbox cap_box is-style-small_ttl">
<div class="cap_box_ttl">KEITO 나이트루틴 정리</div>
<div class="cap_box_content">
<p class="has-border -border02 wp-block-paragraph">
✔ <strong>사용 아이템</strong>:CurrentBody Skin LED 라이트 테라피 마스크 시리즈2(77,000엔)+EFFECTIM 퀵 페이셜 트레이너(59,400엔)<br>
✔ <strong>합계 금액</strong>:136,400엔(세금 포함)<br>
✔ <strong>사용 타이밍</strong>:목욕 후 스트레칭 중과, 스킨케어 과정 중(붓기 예방)<br>
✔ <strong>마무리</strong>:다음 날 촬영을 위해 야식 대신 프로틴 선택<br>
✔ <strong>배경</strong>:데뷔 전부터 뷰티 크리에이터·모델로 활동했던 경력
</p>
<p>전직 뷰티 크리에이터라는 커리어 그대로, 기기 선택부터 사용 타이밍까지 이치에 맞는 나이트루틴이었습니다.<br>
아직 KEITO의 뷰티 지식에 익숙하지 않은 분들도, 이번 기회에 본편 영상도 함께 봐 보시는 건 어떨까요!</p>
</div>
</div>'''))
blocks.append(p([
    "KEITO에 대해서는, 이 블로그의 다른 기사에서도 자세히 소개하고 있습니다.",
]))
blocks.append(wphtml('''<ul>
<li><a href="https://chomoand-1.com/keito_work-10086" target="_blank" rel="noopener">회사원 시절 근무처를 조사한 기사</a></li>
<li><a href="https://chomoand-1.com/keito_zoff-7563" target="_blank" rel="noopener">애용 안경 브랜드를 조사한 기사</a></li>
<li><a href="https://chomoand-1.com/meimon-keitooo-71" target="_blank" rel="noopener">출신 고등학교・대학교 학력을 조사한 기사</a></li>
<li><a href="https://chomoand-1.com/ono-keito-p101-68" target="_blank" rel="noopener">모델・크리에이터로서의 경력을 정리한 기사</a></li>
<li><a href="https://chomoand-1.com/keito_no_item-109" target="_blank" rel="noopener">애용 스킨케어 아이템을 정리한 기사</a></li>
</ul>'''))

content = "\n\n".join(blocks)
print("content chars:", len(content))

JP_POST_ID = 11083
JP_SLUG = "how-much-does-ko1keyz-keitos-f"
KR_SLUG = JP_SLUG + "-kr"
FEATURED_MEDIA = 11084

payload = {
    "title": title,
    "content": content,
    "slug": KR_SLUG,
    "status": "draft",
    "categories": [74, 78],
    "author": 2,
    "featured_media": FEATURED_MEDIA,
    "lang": "ko",
    "translations": {"ja": JP_POST_ID},
}
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("KR POST_ID", post["id"])
print("KR SLUG", post["slug"])
print("KR LINK", post["link"])
