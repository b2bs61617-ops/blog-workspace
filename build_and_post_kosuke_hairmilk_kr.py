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


ACCENT = "#d94f4f"  # KOSUKE의 멤버컬러(빨강)


def capbox(ttl, rows, style="is-style-small_ttl"):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;white-space:nowrap;">{k}</td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f7f7;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{ttl}</p>
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>''')


def capbox_list(ttl, items, style="is-style-small_ttl"):
    lis = "\n".join(f"<li>「{t}」</li>" for t in items)
    return wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f7f7;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{ttl}</p>
<ul style="margin:0;padding-left:1.2em;">
{lis}
</ul>
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
img1_html = build_img_html(11133, "KOSUKE가 머리에 헤어밀크를 바르고 드라이어로 말리는 장면", VIDEO_CAPTION)
img2_html = build_img_html(11134, "KOSUKE가 시트팩을 붙이고 있는 장면", VIDEO_CAPTION)
img3_html = build_img_html(11135, "KOSUKE가 DAIKI에게 빌린 크림을 바르는 장면", VIDEO_CAPTION)

title = "KO1KEYZ KOSUKE의 헤어밀크는?나이트루틴서 공개"

blocks = []

blocks.append(p([
    "KO1KEYZ 공식 유튜브 채널에서, 멤버들 각자의 목욕 후부터 잠들기 전까지를 담은 「🌙 KO1KEYZ Night Routine...⭐️」가 공개되었습니다.",
    "그중에서도 KOSUKE(테루이 코스케)의 파트에서는 <strong>찰랑이는 머릿결을 지켜주는 헤어밀크 사용 장면</strong>이 화제가 되어, X(트위터)에서는 애용 브랜드를 특정하는 게시물까지 등장했습니다.",
    "이번 기사에서는 KOSUKE가 사용하고 있는 헤어밀크의 정체와, 나이트루틴 전체에서 드러난 모습을 자세히 소개합니다.",
]))
blocks.append(hr())

blocks.append(h2("영상 정보"))
blocks.append(capbox("영상 정보", [
    ("영상 제목", "🌙 KO1KEYZ Night Routine...⭐️"),
    ("채널", "KO1KEYZ 공식 유튜브"),
    ("공개일", "2026년 8월 10일"),
    ("출연", "DAIKI・ISSA・KEITO・KOSUKE・RYOGA・RYUJI・SHINHAENG・SIYOUNG・TOWA・YOSHIKI・YUKI・YURA 12명(이 기사에서는 KOSUKE의 파트를 중심으로 소개)"),
    ("URL", f'<a href="{VIDEO_URL}" target="_blank" rel="noopener">{VIDEO_URL}</a>'),
]))
blocks.append(hr())

blocks.append(h2("KOSUKE(테루이 코스케)는 어떤 사람?"))
blocks.append(capbox("KOSUKE 프로필", [
    ("본명", "테루이 코스케(照井康祐)"),
    ("생년월일", "2007년 12월 2일"),
    ("나이", "18세"),
    ("출신지", "치바현"),
    ("신장", "174cm"),
    ("MBTI", "ISTP"),
    ("멤버컬러", "빨강"),
    ("일프 성적", "최종 순위 11위(381,605표), 첫 평가 C클래스에서의 역전 데뷔"),
]))
blocks.append(p([
    "KOSUKE는 『PRODUCE 101 JAPAN 新世界』 참가 전, LDH가 운영하는 EXPG TOKYO에서 댄스를 배웠고, 이후 와타나베 엔터테인먼트 산하의 「DBSing」에서도 활동했던 댄스 실력자입니다.",
    "이전에 공개되었던 전생·경력 조사 기사(<a href=\"https://chomoand-1.com/ko/teruikosuke_profile-kr-10623\" target=\"_blank\" rel=\"noopener\">테루이 코스케의 전생·프로필은? 전 EXPG생, 뛰어난 댄스 실력!</a>)에서도 소개된 것처럼, 댄스·랩 양면에서 존재감을 발휘하는 올라운더로 알려져 있습니다.",
    "그런 KOSUKE의 이번 나이트루틴에서는, 댄스 실력과는 또 다른 꼼꼼한 뷰티에 대한 고집이 엿보이는 장면이 많이 담겨 있었습니다.",
]))
blocks.append(hr())

blocks.append(h2("찰랑이는 머릿결의 비결, 애용 헤어밀크를 확인"))
blocks.append(img1_html)
blocks.append(p([
    "영상 속에서 특히 눈길을 끈 것은, 드라이어 전에 머리에 헤어밀크를 바르는 장면입니다.",
    "화면에는 「머리에 밀크를 꼼꼼히 발라서 말리고 있어요」라는 자막이 붙어 있어, 보습을 신경 쓰며 정성스럽게 머리를 말리는 모습이 담겨 있습니다.",
    "이 장면을 본 X 이용자가 「코스케의 찰랑이는 머릿결의 비결은 &PAIR의 헤어밀크」라고 게시하면서, 사용 아이템의 브랜드가 단숨에 퍼졌습니다.",
]))
blocks.append(hr())

blocks.append(h2("밝혀진 헤어밀크의 정체는 「&PAIR」"))
blocks.append(p([
    "게시물과 영상 내용을 종합해 보면, KOSUKE가 사용하고 있는 것은 주식회사 비크레아의 헤어케어 브랜드 「&PAIR(앤페어)」의 헤어밀크로 보입니다.",
    "&PAIR는 『PRODUCE 101 JAPAN 新世界』의 공식 협찬 파트너로 결정된 브랜드로, 방송 기간 중에는 대상 상품 구매자에게 최종회 관람권이 당첨되는 콜라보 캠페인도 진행되었습니다.",
    "KOSUKE 본인도 일프 신세계 연습생 시절부터 이 브랜드와 친숙했다고 생각하면, 데뷔 후에도 계속 사용하고 있는 자연스러운 흐름으로 보입니다.",
]))
blocks.append(capbox("&PAIR 컨트롤 리페어 2in1 헤어밀크 미스트 정보", [
    ("브랜드", "&PAIR(앤페어)/주식회사 비크레아"),
    ("용량", "150mL"),
    ("가격", "1,595엔(세금 포함)"),
    ("특징", "천천히 누르면 밀크 타입, 빠르게 누르면 미스트 타입이 되는 2way 방식"),
    ("향", "핑크로즈 in 블루버베나"),
    ("구매처", '<a href="https://vicrea.net/shopbrand/andpair/" target="_blank" rel="noopener">공식 스토어</a> / <a href="https://www.amazon.co.jp/dp/B0DZX2CPQH" target="_blank" rel="noopener">Amazon(일본)</a> / <a href="https://item.rakuten.co.jp/vicrea/pair_mist1/" target="_blank" rel="noopener">라쿠텐(일본)</a>'),
], style="is-style-onborder_ttl"))
blocks.append(p([
    "이 시리즈 최대의 특징은, 누르는 방식에 따라 질감이 달라지는 2way 방식이라는 점입니다.",
    "천천히 누르면 촉촉하게 정돈되는 밀크 타입이 되어, 드라이어 전 뜨는 머리·잔머리 억제에 알맞습니다.",
    "반대로 빠르게 누르면 가벼운 미스트 타입이 되기 때문에, 아침 헝클어진 머리 정리나 스타일링 마무리에도 나눠 쓸 수 있는 설계입니다.",
    "세금 포함 1,595엔이라는 부담 없는 가격이면서도 KOSUKE와 같은 윤기 있는 찰랑머리를 재현할 수 있다는 점에서, 게시물을 본 팬들 사이에서도 구매하려는 움직임이 이어졌습니다.",
]))
blocks.append(hr())

blocks.append(h2("나이트루틴에서 드러난 KOSUKE의 고집"))
blocks.append(img2_html)
blocks.append(p([
    "헤어밀크 외에도, KOSUKE의 루틴에는 정성스러운 스킨케어 과정이 여러 번 담겨 있었습니다.",
    "시트팩을 양손으로 꼼꼼히 밀착시키며 「그럼 7・8분 후에」라고 코멘트하며 시간을 충분히 두는 장면도 그중 하나입니다.",
    "팩을 뗀 뒤에는 「크림의 촉촉하고 윤기 있는 느낌이 남아 있지만 끝났습니다」라며, 수분이 골고루 퍼진 피부 상태를 확인하면서 마무리했습니다.",
]))
blocks.append(img3_html)
blocks.append(p([
    "인상적이었던 것은, 자막으로 「DAIKI에게 빌린 크림을 바릅니다」라고 소개된 장면입니다.",
    "자신의 아이템뿐 아니라, 멤버인 DAIKI에게 크림을 빌려 써보는 모습에서는 KO1KEYZ다운 돈독한 사이도 엿볼 수 있었습니다.",
    "영상 중반에는 KEITO가 얼굴을 빼꼼 내미는 장면도 있어, 「우리 KO1KEYZ의 형입니다」라며 장난스럽게 말을 거는 순간도 있었습니다.",
    "멤버끼리 자연스럽게 오가는 공동생활만의 분위기가 느껴지는 루틴이었습니다.",
]))
blocks.append(hr())

blocks.append(h2("SNS 반응"))
blocks.append(capbox_list("헤어밀크 발견에 반응하는 목소리", [
    "코스케의 찰랑이는 머릿결의 비결이 &PAIR의 헤어밀크였다니 소중해",
    "일프 신세계 때도 다들 「샀어요♩ 너무 좋아서♩」라고 하던 그거다",
    "오늘 사러 갈 예정으로 정함",
]))
blocks.append(capbox_list("평소 모습에 반응하는 목소리", [
    "DAIKI한테 크림 빌리는 거 너무 귀여워",
    "케이토가 난입하는 거 훈훈하다",
    "스킨케어 너무 꼼꼼해서 본받고 싶다",
]))
blocks.append(p([
    "영상 공개 직후부터, 헤어밀크 브랜드를 특정하는 게시물과 함께 KOSUKE의 꼼꼼한 뷰티 루틴 자체에 호의적인 반응이 많이 보였습니다.",
    "부담 없는 가격대의 아이템이었다는 점도 구매를 부추기는 포인트가 된 듯합니다.",
]))
blocks.append(hr())

blocks.append(h2("정리"))
blocks.append(wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f7f7;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">KOSUKE 헤어밀크 정리</p>
<p style="margin:0 0 10px 0;">
✔ <strong>사용 아이템</strong>:&PAIR 컨트롤 리페어 2in1 헤어밀크 미스트(150mL・1,595엔)<br>
✔ <strong>사용법</strong>:드라이어 전 밀크 타입으로 보습 유지, 아침에는 미스트 타입으로 헝클어진 머리 정리에도 사용 가능한 2way 방식<br>
✔ <strong>브랜드 배경</strong>:『PRODUCE 101 JAPAN 新世界』의 공식 협찬 파트너, 연습생 시절부터 익숙한 아이템<br>
✔ <strong>루틴의 볼거리</strong>:시트팩과 DAIKI에게 빌린 크림 등, 꼼꼼한 스킨케어와 멤버 간의 교류
</p>
<p style="margin:0;">댄스 실력파의 이미지가 강한 KOSUKE지만, 나이트루틴에서는 뷰티에도 소홀하지 않은 꼼꼼함이 인상적이었습니다.<br>
관심이 생긴 분들은, 꼭 본편 영상도 확인해 보시는 건 어떨까요!</p>
</div>'''))
blocks.append(wphtml('''<div style="border:1px solid #f0b4b4;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#fdecec;">
<p style="margin:0 0 8px 0;"><strong>KOSUKE와 KO1KEYZ에 대해서는, 이 블로그의 다른 기사에서도 자세히 소개하고 있습니다.</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="https://chomoand-1.com/ko/teruikosuke_profile-kr-10623" target="_blank" rel="noopener">테루이 코스케의 전생・프로필을 조사한 기사</a></li>
<li><a href="https://chomoand-1.com/ko/ko1keyz-no-color-kr-10749" target="_blank" rel="noopener">KO1KEYZ 멤버컬러를 정리한 기사</a></li>
<li><a href="https://chomoand-1.com/ko/ko1keyz_gakureki-kr-10737" target="_blank" rel="noopener">KO1KEYZ 멤버들의 학력을 정리한 기사</a></li>
<li><a href="https://chomoand-1.com/ko/profile-12-kr-10734" target="_blank" rel="noopener">KO1KEYZ 멤버 전원의 프로필을 소개한 기사</a></li>
</ul>
</div>'''))

content = "\n\n".join(blocks)
print("content chars:", len(content))

EXISTING_KR_POST_ID = 11139
EYECATCH_MEDIA_ID = 11154  # tools/eyecatch_koikeyz.pyで生成したデザインアイキャッチ(JP版と共通)

payload = {"title": title, "content": content, "status": "draft", "featured_media": EYECATCH_MEDIA_ID}
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_KR_POST_ID}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("UPDATED KR POST_ID", post["id"])
print("KR LINK", post["link"])

with open(ROOT / "tmp_kosuke_hairmilk_kr_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
