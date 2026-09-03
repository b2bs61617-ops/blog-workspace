# -*- coding: utf-8 -*-
import json, base64, os
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

JP_POST_ID = 12245
JP_SLUG = "ko1keyz-kobe-fan-meeting-strea"


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


ACCENT = "#8a8378"
BORDER = "#ded9d2"
BG = "#f8f6f4"


def titlebox(ttl, items, ordered=False):
    tag = "ol" if ordered else "ul"
    lis = "\n".join(f"<li>{t}</li>" for t in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<{tag} style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</{tag}>
</div>''')


def minibox(html_body):
    return wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f7f7;">
{html_body}
</div>''')


def notebox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def wptable(headers, rows):
    thead = "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;font-weight:bold;">{h}</td>' for h in headers)
    trs = "\n".join(
        "<tr>" + "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;">{c}</td>' for c in row) + "</tr>"
        for row in rows
    )
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr>{thead}</tr>
{trs}
</tbody></table></figure>
<!-- /wp:table -->'''


def fanmi_figure(alt, caption):
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="https://chomoand-1.com/wp-content/uploads/2026/08/ko1keyz_fanmi_day1_rehearsal-500x333.jpg" alt="{alt}" width="500" height="333"
  style="max-width:100%;height:auto;"
  srcset="https://chomoand-1.com/wp-content/uploads/2026/08/ko1keyz_fanmi_day1_rehearsal-300x200.jpg 300w, https://chomoand-1.com/wp-content/uploads/2026/08/ko1keyz_fanmi_day1_rehearsal-500x333.jpg 500w, https://chomoand-1.com/wp-content/uploads/2026/08/ko1keyz_fanmi_day1_rehearsal.jpg 780w"
  sizes="(max-width: 500px) 100vw, 500px">
<figcaption style="text-align:center;font-size:12px;">{caption}(출처:<a href="https://x.com/KO1KEYZofficial/status/2090703676507922768" target="_blank" rel="noopener">https://x.com/KO1KEYZofficial/status/2090703676507922768</a>)</figcaption>
</figure>''')


OFFICIAL_NEWS = "https://ko1keyz.com/news/detail/99"
VENUE_URL = "https://chomoand-1.com/ko/ko1keyz-fan-meeting-kr-10770"
CAMERA_URL = "https://chomoand-1.com/ko/?p=11733"
LEMINO_URL = "https://chomoand-1.com/ko/?p=11313"
SCHEDULE_URL = "https://chomoand-1.com/ko/?p=10863"

title = "코이키즈 고베 팬미팅 생중계 확정! 시청 방법은?"

blocks = []

blocks.append(p([
    "2026년 9월 3일, KO1KEYZ(코이키즈)의 공식 X와 공식 사이트에서 첫 팬미팅 『2026 KO1KEYZ 1ST FAN MEETING』의 <strong>효고 공연을 전 세계에 생중계</strong>한다고 발표했습니다.",
    "중계되는 것은 <strong>효고 2일째・저녁 공연 1회차뿐</strong>이며, 일시는 <strong>2026년 9월 10일(목) 18:30(JST)</strong>부터입니다. 다시보기(아카이브) 중계는 없습니다.",
    "이 글에서는 어느 공연이 생중계되는지, 시청권 가격과 판매 기간, 구매부터 시청까지의 흐름, 그리고 아카이브・영상물(블루레이) 발매 전망까지 정리해 소개합니다.",
]))

blocks.append(titlebox("이 글에서 알 수 있는 것", [
    "생중계되는 것은 어느 공연인지",
    "중계 일시와 시청권 가격",
    "시청권 판매 기간과 시청까지의 흐름",
    "아카이브 중계・영상물 발매의 유무",
]))

blocks.append(h2("생중계되는 것은 효고 2일째・저녁 공연뿐"))
blocks.append(minibox('<p style="margin:0;"><strong>중계 대상:</strong>효고(고베 월드 기념홀) 2일째・저녁 공연</p>\n<p style="margin:4px 0 0 0;"><strong>중계 일시:</strong>2026년 9월 10일(목) 18:30(6:30pm) JST~ ※저녁 공연 개연과 동시에 시작</p>'))
blocks.append(p([
    "『2026 KO1KEYZ 1ST FAN MEETING』의 효고 공연은 고베 월드 기념홀에서 9월 9일(수)・10일(목) 이틀간, 낮・저녁 합쳐 총 4회차가 열립니다. 이번에 생중계 대상이 된 것은 그중 마지막 회차인 <strong>9월 10일(목) 저녁 공연</strong>뿐입니다.",
    "중계 시작은 저녁 공연 개연과 같은 18:30(JST). 생중계만 진행되며 <strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">다시보기(아카이브) 중계는 제공되지 않습니다</span></strong>. 당일 그 시간에 실시간으로 시청해야 합니다.",
    "도쿄 공연(8월 21일~23일・TOYOTA ARENA TOKYO)은 이미 종료되었기 때문에, 첫 팬미팅의 모습을 영상으로 즐길 수 있는 것은 사실상 이 효고・저녁 공연 생중계가 유일한 기회가 됩니다.",
]))
blocks.append(wptable(
    ["공연", "개장", "개연", "생중계"],
    [
        ["9/9(수) 낮", "12:30", "13:30", "없음"],
        ["9/9(수) 저녁<br>[추가 공연]", "17:30", "18:30", "없음"],
        ["9/10(목) 낮<br>[추가 공연]", "12:30", "13:30", "없음"],
        ["9/10(목) 저녁", "17:30", "18:30", "〇 생중계 대상"],
    ],
))
blocks.append(p([
    "발표는 공식 X(@KO1KEYZofficial)와 공식 사이트 뉴스를 통해 이루어졌고, 「효고 공연을 전 세계에 생중계 결정」이라는 문구와 함께 순식간에 확산되었습니다. 데뷔 전 그룹임에도 첫 팬미팅에 대한 높은 관심을 엿볼 수 있습니다.",
    "티켓을 구하지 못한 팬이나, 간사이까지 갈 수 없는 지방・해외 팬에게는 이 생중계가 멤버들의 모습을 다 함께 볼 수 있는 소중한 기회가 될 것 같습니다.",
]))

blocks.append(h2("시청권 가격과 중계 서비스는?"))
blocks.append(minibox('<p style="margin:0;"><strong>시청권:</strong>3,600엔(세금 포함)＋각종 시스템 이용료</p>\n<p style="margin:4px 0 0 0;"><strong>중계 서비스:</strong>일본 국내=Lemino・로손 티켓/해외용 서비스도 별도 준비</p>'))
blocks.append(p([
    "<strong><span class=\"swl-marker mark_yellow\">시청권 가격은 3,600엔(세금 포함)</span></strong>입니다. 이와 별도로 중계 플랫폼별 시스템 이용료가 추가됩니다.",
    f"<span class=\"swl-marker mark_yellow\">일본 국내용 중계는 Lemino와 로손 티켓</span>, 해외용으로도 별도 중계 서비스가 준비되어 있습니다. 대응 서비스나 결제 방법 등 자세한 정보는 <a href=\"{OFFICIAL_NEWS}\" target=\"_blank\" rel=\"noopener\">공식 사이트 공지 페이지</a>에서 확인할 수 있습니다.",
    "현장 좌석 티켓과 비교하면, 생중계는 3,600엔 정도로 집에서 볼 수 있어 참여 장벽이 상당히 낮습니다. 데뷔 전 그룹의 팬미팅을 부담 없이 들여다볼 수 있는 기회가 될 것 같습니다.",
]))
blocks.append(p([
    "덧붙는 시스템 이용료는 플랫폼에 따라 금액이 달라집니다. X에서는 Lemino와 로손 티켓 모두 티켓플러스 수수료가 붙기 때문에, 실제로 양쪽 구매 화면을 비교한 팬들에게서 「합계 금액이 수백 엔 정도 차이가 났다」는 보고가 올라오고 있습니다.",
    "또한 로손 티켓은 결제가 로손・미니스톱에서의 매장 입금으로 한정되며, 신용카드 결제에는 대응하지 않는다는 이야기도 있었습니다. 카드로 빠르게 사고 싶다면 Lemino, 매장에서 한꺼번에 지불하고 싶다면 로손 티켓 식으로 선택하게 될 것 같습니다. 최종 결제 총액은 구매 전에 각 서비스 화면에서 반드시 확인하세요.",
]))

blocks.append(h2("시청권 판매 기간과 시청까지의 흐름"))
blocks.append(minibox('<p style="margin:0;"><strong>판매 기간:</strong>2026년 9월 3일(목) 12:00pm ~ 9월 10일(목) 7:00pm(JST)</p>'))
blocks.append(p([
    "시청권 판매 기간은 <strong>2026년 9월 3일(목) 12:00pm~9월 10일(목) 7:00pm(JST)</strong>입니다. 중계 당일 저녁 공연 개연(18:30) 이후에도 잠시 동안은 구매할 수 있지만, 19:00에 판매가 마감됩니다. 아카이브가 없는 만큼, 볼 예정인 사람은 미리 준비해 두는 편이 안심입니다.",
]))
blocks.append(titlebox("시청권 구매~시청까지의 흐름", [
    "일본 국내는 Lemino・로손 티켓, 해외용 서비스 중 이용하고 싶은 중계 페이지에 접속한다",
    "판매 기간 내(9/3 12:00pm~9/10 7:00pm JST)에 시청권(3,600엔＋시스템 이용료)을 구매・결제한다",
    "중계 당일, 구매한 서비스의 앱이나 사이트에 같은 계정으로 로그인한다",
    "9월 10일(목) 18:30(JST) 중계 시작에 맞춰 시청을 시작한다(다시보기 없음)",
], ordered=True))
blocks.append(p([
    "해외에서 시청하는 경우 일본과의 시차에도 주의가 필요합니다. 생중계만 진행되므로, 시작 시각인 18:30(JST)을 자신이 있는 나라의 시간으로 환산해 미리 일정을 잡아 두세요.",
    "당일에는 통신 환경이 좋은 곳에서, 가능하면 Wi-Fi에 연결해 시청하는 것을 추천합니다. 시작 직전에는 회선이 몰릴 수 있으므로, 조금 여유를 두고 중계 페이지를 열어 두면 차분하게 볼 수 있습니다.",
]))

blocks.append(h2("생중계에서는 어떤 모습을 볼 수 있나?"))
blocks.append(fanmi_figure(
    "KO1KEYZ 1ST FAN MEETING 도쿄 공연 무대에 선 12명",
    "도쿄 공연(TOYOTA ARENA TOKYO) 무대에 선 KO1KEYZ 12명",
))
blocks.append(p([
    "첫 팬미팅은 토크 코너, 멤버끼리의 게임, 곡 퍼포먼스, 그리고 종반의 촬영 OK 타임 등으로 구성되어 있습니다. 먼저 열린 도쿄 공연에서는 멤버들이 카트를 타고 객석을 도는 장면이나 앙코르에서의 촬영 가능 타임이 팬들 사이에서 큰 화제가 되었습니다.",
    "이번에 생중계되는 효고・저녁 공연은 총 4회차 중 마지막 회차에 해당하기 때문에, 이틀을 달려온 멤버들의 분위기나 마무리다운 인사도 볼거리가 될 것 같습니다.",
]))

blocks.append(h2("아카이브 중계나 영상물 발매는 있나?"))
blocks.append(minibox('<p style="margin:0;"><strong>아카이브 중계:</strong>없음(생중계만)</p>\n<p style="margin:4px 0 0 0;"><strong>영상물 발매(블루레이・DVD):</strong>2026년 9월 3일 시점 발표 없음</p>'))
blocks.append(p([
    "이번 생중계에 아카이브(다시보기) 중계는 없습니다. 중계 종료 후 같은 영상을 다시 볼 수 없는 방식이므로, 시청을 예정하고 있다면 실시간 시청을 전제로 준비해 두세요.",
    "공연 자체의 블루레이・DVD화에 대해서도 현시점에 공식 발표는 없습니다. 회장에 촬영용 카메라가 들어와 있던 것은 확인되었지만, 그것이 영상물 발매로 이어질지는 알 수 없습니다.",
    "참고로, 팬미팅 준비에 밀착한 특별 프로그램이 Lemino에서 방영되는 것은 별도로 발표되었지만, 이는 공연 본편 그 자체가 아니라 다큐멘터리 성격의 콘텐츠입니다. 이번 효고・저녁 공연 생중계와는 다른 콘텐츠이므로 혼동하지 않도록 주의하세요.",
]))

blocks.append(h2("정리"))
blocks.append(notebox('''<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">코이키즈 고베 팬미팅 생중계 정리</p>
<p style="margin:0;">
&#10003; 생중계되는 것은 효고(고베 월드 기념홀) 2일째・저녁 공연뿐<br>
&#10003; 중계 일시는 2026년 9월 10일(목) 18:30(JST)~, 아카이브 중계 없음<br>
&#10003; 시청권은 3,600엔(세금 포함)＋시스템 이용료, 국내는 Lemino・로손 티켓<br>
&#10003; 시스템 이용료는 서비스별로 차이가 있고, 로손 티켓은 매장 입금만 가능하다는 이야기도<br>
&#10003; 판매 기간은 9월 3일(목) 12:00pm~9월 10일(목) 7:00pm(JST)<br>
&#10003; 영상물 발매는 미발표. Lemino 특별 프로그램은 공연 본편과는 별개
</p>'''))
blocks.append(p([
    "현장에 가지 못해도 첫 팬미팅을 실시간으로 지켜볼 수 있다는 점은 반가운 부분입니다. 시차와 판매 마감에 주의해서, 당일에는 미리 중계 페이지를 열고 대기해 두고 싶네요.",
]))
blocks.append(p([
    "다만 중계 시작이 평일 18:30이라, 저녁 식사나 집안일과 딱 겹치기 쉬운 시간대입니다. 특히 어린 자녀가 있는 가정이라면 차분히 화면 앞에 앉기 어렵다는 사람도 많을 것 같습니다.",
    "생중계만 있고 되감기나 아카이브가 없는 점도, 실시간으로 붙어 있기 힘든 사람에게는 솔직히 조금 아쉬운 방식입니다. 시작 시각에 맞출 수 있도록 당일 일정을 미리 조정해 두면 안심입니다.",
    "이 글은 중계 서비스 추가나 시청 방법 변경 등 후속 정보가 들어오는 대로 그때그때 갱신하겠습니다.",
]))

blocks.append(notebox(f'''<p style="margin:0 0 8px 0;"><strong>KO1KEYZ의 팬미팅에 대해서는 이 블로그의 다른 글에서도 소개하고 있습니다.</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{VENUE_URL}" target="_blank" rel="noopener">KO1KEYZ 팬미팅 공연장은 어디? 일정과 접근성도 소개!</a></li>
</ul>'''))

content = "\n\n".join(blocks)
print("content chars:", len(content))

slug = f"{JP_SLUG}-kr"

KR_POST_ID = 12249       # update in place
KR_EYECATCH_MEDIA_ID = 12248

payload = {
    "title": title,
    "content": content,
    "status": "draft",
    "slug": slug,
    "lang": "ko",
    "translations": {"ja": JP_POST_ID},
    "featured_media": KR_EYECATCH_MEDIA_ID,
    "categories": [66, 62],
    "author": 2,
}
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{KR_POST_ID}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("KR POST_ID", post["id"])
print("KR SLUG", post["slug"])
print("KR LINK", post.get("link", f"{WP_URL}/ko/?p={post['id']}"))

with open(ROOT / "tmp_ko1keyz_kobe_fanmi_streaming_kr_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
