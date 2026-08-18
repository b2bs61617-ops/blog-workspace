# -*- coding: utf-8 -*-
import base64, os, json, re
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

JP_POST_ID = 11468
JP_SLUG = "can-i-participate-in-the-ko1ke"
TREKKA_MEDIA_ID = 11466
KUJI_MEDIA_ID = 11467


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def hr():
    return '<!-- wp:separator --><hr class="wp-block-separator has-alpha-channel-opacity"/><!-- /wp:separator -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


ACCENT = "#8a8378"
BORDER = "#ded9d2"
BG = "#f8f6f4"


def capbox(ttl, rows):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;white-space:nowrap;">{k}</td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{ttl}</p>
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>''')


def titlebox(ttl, items):
    lis = "\n".join(f"<li>{t}</li>" for t in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(html_body):
    return wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f7f7;">
{html_body}
</div>''')


def notebox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{html_body}
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


TREKKA_CAPTION_KR = '출처:<a href="https://x.com/KO1KEYZofficial/status/2089630884013961359" target="_blank" rel="noopener">https://x.com/KO1KEYZofficial/status/2089630884013961359</a>'
img_trekka_html = build_img_html(TREKKA_MEDIA_ID, "KO1KEYZ FANCLUB BOOTH FC 포토카드 샘플 이미지(12종 중 랜덤 1장)", TREKKA_CAPTION_KR)

KUJI_CAPTION_KR = '출처:<a href="https://x.com/_siyoungtokki_/status/2089653778618466339" target="_blank" rel="noopener">https://x.com/_siyoungtokki_/status/2089653778618466339</a>'
img_kuji_html = build_img_html(KUJI_MEDIA_ID, "KO1KEYZ FANCLUB BOOTH FC 포토카드・KO1LY 복권 개요", KUJI_CAPTION_KR)

FANMEETING_PREDICT_URL_KR = "https://chomoand-1.com/ko/ko1keyz-live-kr-10755"
DEBUT_EVENTS_URL_KR = "https://chomoand-1.com/ko/what-events-will-be-held-to-co-2-kr-11312"
SCHEDULE_URL_KR = "https://chomoand-1.com/ko/what-is-ko1keyzs-future-schedu-kr-10863"

title = "KO1KEYZ 팬미팅 FC부스에서 포토카드・복권 받을 수 있을까?"

blocks = []

blocks.append(p([
    "2026년 8월 18일, KO1KEYZ 공식 X・공식 사이트를 통해 8월 21일부터 시작되는 『2026 KO1KEYZ 1ST FAN MEETING』에서 FANCLUB BOOTH를 진행한다는 소식이 발표되었습니다.",
    "내용은 <strong>①월회비 일괄결제 코스 한정 오리지널 포토카드 증정</strong>과 <strong>②FC 회원이라면 누구나 참여할 수 있는 KO1LY 복권</strong> 두 가지로, <strong>둘 다 공연 티켓이 없어도 참여할 수 있다</strong>는 점이 큰 포인트입니다.",
    "이 글에서는 두 특전의 대상자・참여 방법・참여 횟수 제한 등을 자세히 정리합니다.",
]))

blocks.append(titlebox("이 글에서 알 수 있는 것", [
    "FC 포토카드(월회비 일괄결제 코스 한정)의 내용",
    "KO1LY 복권(FC 회원 한정)의 내용과 특상",
    "티켓이 없어도 참여할 수 있는지 여부",
]))

blocks.append(h2("애초에 『2026 KO1KEYZ 1ST FAN MEETING』이란?"))
blocks.append(capbox("공연 개요", [
    ("도쿄 공연", "TOYOTA ARENA TOKYO／2026년 8월 21일(금)〜23일(일)"),
    ("효고 공연", "고베 월드 기념홀／2026년 9월 9일(수)〜10일(목)"),
]))
blocks.append(p([
    "KO1KEYZ에게는 첫 팬미팅으로, 드디어 이번 주말 8월 21일부터 도쿄 공연이 시작됩니다.",
    f"개최 개요 자체에 대해서는 이전에 예상 기사로 정리한 <a href=\"{FANMEETING_PREDICT_URL_KR}\" target=\"_blank\" rel=\"noopener\">KO1KEYZ 라이브・팬미팅은 언제? 라포네 성향으로 일정 대예상!</a>도 참고해보세요.",
    "그리고 개막을 코앞에 둔 8월 18일, 공식 측에서 새롭게 FANCLUB BOOTH 진행을 발표한 것이 이번 글의 내용입니다.",
]))

blocks.append(h2("새 특전①FC 포토카드(월회비 일괄결제 코스 한정)"))
blocks.append(img_trekka_html)
blocks.append(minibox('<p style="margin:0;"><strong>대상:</strong>「월회비 일괄결제 코스」FC 회원(티켓 불필요・당일 가입/코스 변경도 가능)</p>'))
blocks.append(p([
    "첫 번째 특전은 FC의 「월회비 일괄결제 코스」회원 한정으로, 오리지널 포토카드를 1장 증정받을 수 있는 기획입니다.",
    "포토카드는 전 12종 중 랜덤으로 1장 지급되며, 멤버를 직접 고를 수는 없습니다.",
]))
blocks.append(capbox("참여 방법", [
    ("①", "회장 내 POP의 QR코드, 또는 공식 사이트 상단 배너에서 FANCLUB 기획 페이지에 접속해 「교환 페이지는 이쪽」을 탭"),
    ("②", "교환 화면이 표시되면 그대로 FANCLUB BOOTH로 이동"),
    ("③", "스태프 확인 후, 포토카드를 랜덤으로 1장 증정"),
]))
blocks.append(p([
    "<strong>대상은 회장에 방문한 「월회비 일괄결제 코스」회원이며, 당일 이 코스에 신규 가입・코스 변경한 사람도 대상에 포함됩니다.</strong>",
    "공연 티켓이 없는 사람도 참여할 수 있지만, <strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">참여 가능 횟수는 1인 1일 1회까지</span></strong>로, <strong>하루 2공연이 있는 날짜에도 1회까지만 교환할 수 있습니다.</strong>",
]))
blocks.append(notebox('''<p style="margin:0;"><strong>참여 시 유의사항</strong><br>
・본인이 직접 교환 버튼을 눌러 FANCLUB BOOTH에서 교환하기 전에 「교환 완료」 화면이 된 경우, 이유를 불문하고 교환이 불가능합니다.<br>
・당일 회장 주변의 혼잡 상황이나 전파 상황, 부스 종료 시간에 따라 기획 참여나 특전 교환이 불가능할 수 있습니다.</p>'''))

blocks.append(h2("새 특전②KO1LY 복권(FC 회원 한정・코스 무관)"))
blocks.append(minibox('<p style="margin:0;"><strong>대상:</strong>「KO1KEYZ OFFICIAL FANCLUB」회원(코스 무관・티켓 불필요・당일 가입도 가능)</p>'))
blocks.append(p([
    "두 번째 특전은 코스와 상관없이 FC 회원이라면 누구나 참여할 수 있는 「KO1LY 복권」입니다.",
    "특상은 <strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">KO1KEYZ 멤버 전원이 함께하는 배웅 이벤트</strong></span>로, 각 일자 종연 후에 진행됩니다(하루 2공연이 있는 회장은 2부 종연 후 진행).",
]))
blocks.append(capbox("참여 방법", [
    ("①", "회장 내 POP의 QR코드, 또는 공식 사이트 상단 배너에서 FANCLUB 기획 페이지에 접속해 「복권 뽑기」를 탭"),
    ("②", "추첨 결과 확인"),
    ("③", "당첨 화면이 표시된 경우에만 FANCLUB BOOTH로 이동"),
]))
blocks.append(p([
    "꽝인 경우 상품이 없는 대신 FANCLUB BOOTH를 방문할 필요도 없습니다.",
    "복권을 뽑는 것만이라면 누구나 가볍게 도전할 수 있는 기획입니다.",
]))

blocks.append(h2("티켓이 없어도 참여할 수 있을까?"))
blocks.append(img_kuji_html)
blocks.append(p([
    "제목 그대로, FC 포토카드・KO1LY 복권 모두 <strong>공연 티켓이 없는 사람도 참여할 수 있는</strong> 기획입니다.",
    "실제로 X에서도 「티켓 없이도 할 수 있는 거」라며, 티켓이 없어도 FANCLUB BOOTH만을 목적으로 참여할 수 있다는 점을 언급한 게시물이 눈에 띄었습니다.",
    "다만 참여하려면 회장 주변에 있어야 한다는 조건이 있으며, 공식 측에서는 스마트폰의 위치 정보를 미리 켜두도록 안내하고 있습니다.",
    "먼 지역에서 참여하지 못하는 사람을 위한 구제책이 아니라, 어디까지나 「회장에는 오지만 티켓은 없는」 사람을 위한 기획이라는 점을 기억해두면 좋겠습니다.",
]))

blocks.append(h2("CD 예약 추첨회와는 무엇이 다를까?"))
blocks.append(p([
    "『2026 KO1KEYZ 1ST FAN MEETING』 회장에서는 이번 FANCLUB BOOTH와는 별도로, 데뷔 싱글 『KO1KEYZ』 3종 세트를 예약하면 참여할 수 있는 <strong>CD 예약 추첨회</strong>도 진행됩니다.",
    "이쪽도 티켓 없이 참여할 수 있으며, 구매하면 반드시 복권과 포토카드를 받을 수 있는 방식이지만, FC 회원 한정인 FANCLUB BOOTH와 달리 CD 예약 추첨회는 누구나 참여할 수 있습니다.",
    f"CD 예약 추첨회의 자세한 참여 방법・특전 내용은 <a href=\"{DEBUT_EVENTS_URL_KR}\" target=\"_blank\" rel=\"noopener\">KO1KEYZ 데뷔 기념 이벤트, 어떤 게 있을까? 타워레코드 한정 사인회＆팬미팅 예약 추첨회 총정리</a>에서 소개하고 있으니, 두 특전을 모두 노리고 싶은 사람은 함께 확인해보세요.",
]))

blocks.append(h2("정리"))
blocks.append(notebox(f'''<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">KO1KEYZ 팬미팅 FANCLUB BOOTH 정리</p>
<p style="margin:0 0 10px 0;">
&#10003; <strong>FC 포토카드</strong>:월회비 일괄결제 코스 한정, 12종 중 랜덤 1장, 1인 1일 1회까지(하루 2공연이어도 1회)<br>
&#10003; <strong>KO1LY 복권</strong>:FC 회원이라면 코스 무관 참여 가능, 특상은 멤버 전원 배웅 이벤트<br>
&#10003; <strong>티켓</strong>:둘 다 공연 티켓 불필요(회장 주변에 있어야 하며, 위치 정보 켜기가 조건)<br>
&#10003; <strong>진행 장소</strong>:『2026 KO1KEYZ 1ST FAN MEETING』(도쿄 공연 8/21〜23・효고 공연 9/9〜10)
</p>
<p style="margin:0;">드디어 이번 주말 개막하는 팬미팅, FC 회원이라면 FANCLUB BOOTH도 꼭 함께 확인해보세요!</p>'''))

blocks.append(notebox(f'''<p style="margin:0 0 8px 0;"><strong>KO1KEYZ에 대해서는 이 블로그의 다른 글에서도 자세히 소개하고 있습니다.</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{DEBUT_EVENTS_URL_KR}" target="_blank" rel="noopener">KO1KEYZ 데뷔 기념 이벤트, 어떤 게 있을까? 타워레코드 한정 사인회＆팬미팅 예약 추첨회 총정리</a></li>
<li><a href="{FANMEETING_PREDICT_URL_KR}" target="_blank" rel="noopener">KO1KEYZ 라이브・팬미팅은 언제? 라포네 성향으로 일정 대예상!</a></li>
<li><a href="{SCHEDULE_URL_KR}" target="_blank" rel="noopener">KO1KEYZ의 앞으로의 스케줄은? 8월〜10월 데뷔까지의 일정</a></li>
</ul>'''))

content = "\n\n".join(blocks)
print("content chars:", len(content))

EXISTING_KR_POST_ID = 11472
EXISTING_KR_EYECATCH_MEDIA_ID = 11471

if EXISTING_KR_POST_ID:
    payload = {"title": title, "content": content, "status": "draft"}
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_KR_POST_ID}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print("UPDATED KR POST_ID", post["id"])
else:
    slug = f"{JP_SLUG}-kr"

    # KR版アイキャッチ(--lang krで生成した専用画像)をアップロード
    eyecatch_path = ROOT / "images" / "ko1keyz_fanclub_booth_eyecatch_kr.png"
    with open(eyecatch_path, "rb") as f:
        eyecatch_data = f.read()
    media_r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={
            **HEADERS_AUTH,
            "Content-Type": "image/png",
            "Content-Disposition": 'attachment; filename="ko1keyz_fanclub_booth_eyecatch_kr.png"',
        },
        data=eyecatch_data,
    )
    media_r.raise_for_status()
    eyecatch_media = media_r.json()
    print("KR EYECATCH_MEDIA_ID", eyecatch_media["id"])

    payload = {
        "title": title,
        "content": content,
        "status": "draft",
        "slug": slug,
        "lang": "ko",
        "translations": {"ja": JP_POST_ID},
        "featured_media": eyecatch_media["id"],
        "categories": [66, 62],
        "author": 2,
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
print("KR LINK", post.get("link", f"{WP_URL}/ko/?p={post['id']}"))

with open(ROOT / "tmp_ko1keyz_fanclub_booth_kr_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
