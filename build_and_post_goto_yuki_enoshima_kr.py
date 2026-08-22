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

SOURCE_OFFICIAL = "https://x.com/KO1KEYZofficial/status/2090038569876545590"
SOURCE_FACE = "https://x.com/G_YUKI_FACE/status/2090076439425241137"
SOURCE_HOBBYOFF = "https://x.com/hb_hashimoto/status/2083780842472526027"

# 日本語版アップロード時にすでにアップロード済みのメディアIDを再利用
MEDIA_IDS = {
    "official": 11543,
    "img2": 11544,
    "img3": 11545,
    "img4": 11546,
    "img5": 11547,
    "img6": 11548,
    "img7": 11620,
    "eyecatch": 11550,
}

media_cache = {}
def get_media(key):
    if key not in media_cache:
        media_cache[key] = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{MEDIA_IDS[key]}", headers=HEADERS_AUTH).json()
    return media_cache[key]


def build_img_html(media, alt, source_url):
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
    return f'''<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">출처:{source_url}</figcaption>
</figure>'''


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


img_official_html = wphtml(build_img_html(get_media("official"), "코이노트에 올라온 YUKI(고토 유이)의 사진, 뒤로 에노시마로 보이는 섬 그림자가 보인다", SOURCE_OFFICIAL))
img2_html = wphtml(build_img_html(get_media("img2"), "목재 데크와 붉은 난간이 있는 통로, 멀리 에노시마가 보이는 풍경", SOURCE_FACE))
img3_html = wphtml(build_img_html(get_media("img3"), "바닷가 데크에서 보이는 백사장과 에노시마 방향 풍경", SOURCE_FACE))
img4_html = wphtml(build_img_html(get_media("img4"), "시설 내 목재 통로, 뒤로 건물과 파란 하늘이 펼쳐진 풍경", SOURCE_FACE))
img5_html = wphtml(build_img_html(get_media("img5"), "밤, 야자수와 주차장을 배경으로 한 YUKI, 뒤로 파랗게 조명이 켜진 타워가 보인다", SOURCE_FACE))
img6_html = wphtml(build_img_html(get_media("img6"), "밤, 클래식카를 배경으로 한 YUKI, 같은 파란 타워가 보인다", SOURCE_FACE))
img7_html = wphtml(build_img_html(get_media("img7"), "\"해피 마린\" 수달 인형 3마리, 색깔별로 쌓아 올려져 있다", SOURCE_HOBBYOFF))


def p(sentences):
    body = "<br>\n".join(sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


ACCENT = "#8a8378"


def capbox(ttl, rows):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ddd9d3;padding:8px 12px;background:#f7f6f4;white-space:nowrap;">{k}</td>'
        f'<td style="border:1px solid #ddd9d3;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:6px;overflow:hidden;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<div style="padding:14px 18px;background:#f7f6f4;">
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>
</div>''')


def minibox(inner):
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f6f4;">
{inner}
</div>''')


def wakaru_box(items, ttl):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:#f7f6f4;">
{lis}
</ul>
</div>''')


title = "【KO1KEYZ】YUKI 코이노트 사진 장소와 수달의 정체는?"

blocks = []

blocks.append(p([
    "KO1KEYZ의 YUKI(고토 유이)가 2026년 8월 19일에 업데이트한 공식 팬클럽 콘텐츠 'KO1NOTE(코이노트)'의 사진 속 배경을 살펴봤습니다.",
    "사진에는 바다와 섬 그림자, 그리고 하얀 타워 같은 것이 함께 찍혀 있는데, 이곳이 <strong>가나가와현 후지사와시의 에노시마, 그 중에서도 신에노시마 수족관(에노스이)</strong>일 가능성이 높다는 것을 확인했습니다.",
    "이 글에서는 사진에서 읽을 수 있는 근거와 함께, 화제가 되고 있는 '새 가족' 수달에 대해서도 소개합니다.",
]))

blocks.append(capbox("코이노트 업데이트 정보", [
    ("업데이트일", "2026년 8월 19일"),
    ("담당 멤버", "YUKI(고토 유이)"),
    ("내용", "사진과 코멘트 업데이트"),
    ("게재처", "KO1KEYZ 공식 사이트 내 'KO1NOTE'"),
]))

blocks.append(wakaru_box([
    "코이노트 사진 배경의 정체",
    "촬영 장소가 신에노시마 수족관(에노스이)으로 보이는 근거",
    "화제의 '새 가족' 수달 이야기",
], "이 글에서 알 수 있는 것"))

blocks.append(h2("코이노트에 공개된 사진 확인하기"))
blocks.append(minibox('<p style="margin:0;"><strong>업데이트 내용:</strong>2026년 8월 19일, YUKI가 "KO1LY 안녕! YUKI입니다!"라는 코멘트와 함께 여러 장의 사진을 공개</p>'))
blocks.append(img_official_html)
blocks.append(p([
    "공개된 사진 중 한 장에는 New Era의 검은색 캡을 쓰고 큰 가방을 어깨에 멘 YUKI의 모습이 담겨 있습니다.",
    "뒤로는 바다와 그 너머로 떠 있는 초록빛 섬 그림자, 섬 위에 서 있는 하얀 타워 같은 실루엣이 인상적인 한 장입니다.",
    "이 게시물에는 곧바로 반응이 이어졌고, '수족관 가고 싶어졌어ㅋㅋ', '에노스이 갔으려나~ 가까우니까 가볼게', '에노스이 갔던 거네 그걸 첫 번째 사진으로 하는 것도 진짜 귀엽다' 같은 댓글이 달렸습니다.",
    "'에노스이'는 신에노시마 수족관의 애칭으로, 지역 팬들 사이에서는 익숙한 표현입니다.",
]))

blocks.append(h2("사진 배경에 찍힌 섬과 타워의 정체는?"))
blocks.append(minibox('<p style="margin:0;"><strong>배경의 정체(추정):</strong>가나가와현 후지사와시의 "에노시마", 섬 위의 하얀 타워는 전망 등대 "에노시마 씨캔들"로 보임</p>'))
blocks.append(p([
    "사진 배경을 자세히 보면, 바다에 떠 있는 섬의 윤곽과 그 정상 부근에 서 있는 하얗고 가느다란 타워를 확인할 수 있습니다.",
    "이 섬의 형태와 타워의 위치 관계는 가나가와현 후지사와시에 있는 관광 명소 '에노시마', 그리고 섬 안 사무엘 코킹 정원에 있는 전망 등대 '에노시마 씨캔들'의 특징과 일치합니다.",
    "에노시마는 쇼난 지역을 대표하는 관광지로, 섬 전체의 초록에 둘러싸이듯 솟아 있는 씨캔들의 모습은 현지에서는 익숙한 랜드마크로 알려져 있습니다.",
    "사진의 촬영 각도로 볼 때도 에노시마를 바다 너머로 바라볼 수 있는 해안 어딘가에서 촬영된 것으로 보입니다.",
]))

blocks.append(h2("촬영 장소는 신에노시마 수족관(에노스이)?"))
blocks.append(minibox('<p style="margin:0;"><strong>구체적인 촬영 장소(추정):</strong>에노시마가 보이는 바닷가 목재 데크, 붉은빛이 도는 난간이 특징인 통로</p>'))
blocks.append(p([
    "코이노트와 같은 날 게시된 관련 이미지를 살펴보니, 나무결의 데크와 붉은빛을 띤 난간이 이어지는 통로 사진이 여러 장 발견됐습니다.",
    "이 데크에서 보이는 풍경도 바다 너머로 에노시마와 씨캔들이 떠 있는 구도로, YUKI의 사진과 매우 비슷한 경관입니다.",
]))
blocks.append(img2_html)
blocks.append(p([
    "지붕이 있는 통로와 벤치가 늘어선 이 데크의 분위기는 신에노시마 수족관(에노스이)의 관내에서 야외 테라스로 이어지는 통로의 특징과 매우 비슷합니다.",
    "에노스이는 가타세 해안에 면한 위치로, 관내 창문과 야외 데크에서 바다 너머 에노시마를 한눈에 볼 수 있는 것으로 알려진 수족관입니다.",
]))
blocks.append(img3_html)
blocks.append(img4_html)
blocks.append(p([
    "백사장과 해안선, 그리고 목재 통로가 이어지는 모습을 봐도 이 일대가 수족관 부지 내일 가능성이 높아 보입니다.",
    "단정할 수는 없지만, 여러 장의 사진 모두에 공통적으로 에노시마로 보이는 섬 그림자가 찍혀 있는 것으로 볼 때, YUKI가 이날 방문한 곳은 <strong>가타세 해안에 면한 신에노시마 수족관(에노스이)</strong>일 가능성이 높아 보입니다.",
]))

blocks.append(h2("'새 가족' 수달 이야기"))
blocks.append(minibox('<p style="margin:0;"><strong>새 가족의 정체(추정):</strong>신에노시마 수족관의 꽝 없는 "인형 뽑기"(1등~3등 등) 경품, 아기수달(코츠메카와우소) 인형 "해피 마린"</p>'))
blocks.append(p([
    "이번 코이노트 업데이트를 둘러싸고, YUKI가 새로 맞이했다는 '가족'도 화제가 되고 있습니다.",
    "찾아보니 이 인형은 <strong><span class=\"swl-marker mark_yellow\">신에노시마 수족관(에노스이)에서 인기가 많은 \"인형 뽑기\"의 경품인 아기수달 인형 \"해피 마린\"</span></strong>일 가능성이 높다는 것을 확인했습니다.",
    "동그란 눈과 통통한 귀여운 외형, 몰캉몰캉한 부드러운 촉감이 특징으로 기념품이나 힐링 아이템으로 큰 인기를 끌고 있습니다.",
]))
blocks.append(img7_html)
blocks.append(p([
    "사진처럼 <strong>라이트브라운·브라운·다크브라운의 3가지 색상</strong>이 있는 것으로 보이며, 색깔별로 나란히 두면 더욱 귀여움이 배가되는 인기 아이템입니다.",
    "이 인형 뽑기는 1등~3등 등 등급이 있는 '꽝 없는 뽑기'로, 관내에서 부담 없이 도전할 수 있는 것도 매력 중 하나입니다.",
    "신에노시마 수족관 공식 사이트의 \"오터숍\" 페이지에 따르면, 인형 뽑기 \"수달\"은 <strong>1회 1,100엔</strong>으로, 꽝이 없어 반드시 당첨되는 뽑기입니다.",
    "경품 크기는 등급에 따라 상당한 차이가 있으며, 자세한 내용은 다음과 같습니다.",
]))
blocks.append('''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr><td>등급</td><td>사이즈 기준</td></tr>
<tr><td>1등</td><td>약 90cm</td></tr>
<tr><td>2등</td><td>약 57cm</td></tr>
<tr><td>3등</td><td>약 33cm</td></tr>
</tbody></table></figure>
<!-- /wp:table -->''')
blocks.append(p([
    "수량 한정으로 소진되는 대로 종료된다고 합니다.",
    "YUKI가 실제로 몇 등을 뽑았는지, 어떤 사이즈의 인형을 손에 넣었는지까지는 알려져 있지 않지만, 이렇게 크기 차이가 크다는 걸 알고 나니 더 궁금해지는 부분입니다.",
    "수족관을 방문한 흐름과 함께 생각해보면, 코이노트 사진 속 장소가 신에노시마 수족관으로 보인다는 점과도 맞아떨어져, 관내 인형 뽑기에서 이 \"해피 마린\"을 손에 넣었을 가능성이 높아 보입니다.",
    "이후 유료 채팅 서비스 \"KO1KEYZ Chat\"에서도 YUKI가 같은 색깔의 수달 인형을 안고 있는 모습을 공개해, 실제로 \"해피 마린\"을 가족으로 맞이했다는 것을 짐작하게 합니다.",
    "다만 YUKI 본인이 수족관이나 \"해피 마린\"에 대해 직접 설명한 적은 없어, 어디까지나 사진·댓글·상품 정보로 추측할 수 있는 범위에 머무른다는 점은 유의할 필요가 있습니다.",
]))

blocks.append(h2("YUKI는 예전부터 에노시마를 좋아했을까?"))
blocks.append(minibox('<p style="margin:0;"><strong>출신지:</strong>가나가와현(에노시마가 있는 후지사와시와 같은 현)</p>'))
blocks.append(p([
    "같은 게시물에는 밤에 촬영된 것으로 보이는 사진도 함께 올라와 있었습니다.",
    "야자수가 늘어선 주차장을 배경으로 한 컷으로, 멀리에는 파란색으로 조명이 켜진 타워가 은은하게 떠올라 있습니다.",
]))
blocks.append(img5_html)
blocks.append(p([
    "에노시마 씨캔들은 밤이 되면 다양한 색으로 조명이 켜지는 것으로 알려져 있고, 이 파란 조명 역시 그 특징 중 하나입니다.",
    "다른 한 장은 클래식카를 배경으로 한 컷인데, 여기에도 같은 위치에 파란 타워의 불빛이 찍혀 있습니다.",
]))
blocks.append(img6_html)
blocks.append(p([
    "낮에 찍힌 코이노트 사진과는 다른 날 촬영된 것으로 보이는 이 사진들로 미루어 볼 때, YUKI가 이번뿐 아니라 여러 차례 에노시마를 방문했을 가능성이 엿보입니다.",
    "YUKI의 출신지는 가나가와현으로, 에노시마가 있는 후지사와시도 같은 현 안에 있습니다.",
    "실제로 이번 게시물에는 현지 팬으로 보이는 사람의 '고향 와줘서 고마워'라는 댓글도 달려 있어, 에노시마 주변이 현지 팬들에게도 친숙한 장소임을 짐작할 수 있습니다.",
]))

blocks.append(h2("신에노시마 수족관(에노스이)은 어떤 곳?"))
blocks.append(p([
    "신에노시마 수족관(에노스이)은 가나가와현 후지사와시의 가타세 해안에 면한 수족관으로, 사가미만의 생물을 중심으로 전시하는 '사가미만 존', 해파리 전시로 유명한 '해파리 판타지 홀' 등이 인기 있는 공간입니다.",
    "관내에서 바다 너머로 에노시마를 바라볼 수 있는 전망으로도 알려져 있어, 데이트·관광 명소로도 정평이 나 있는 곳입니다.",
    "쇼난 지역의 인기 시설인 만큼, KO1KEYZ 멤버가 개인적으로 방문했다는 사실이 확인되면 현지 팬들을 중심으로 더욱 화제가 될 것으로 보입니다.",
]))
blocks.append(wphtml('''<iframe
  src="https://maps.google.com/maps?q=%E6%96%B0%E6%B1%9F%E3%83%8E%E5%B3%B6%E6%B0%B4%E6%97%8F%E9%A4%A8&t=&z=15&ie=UTF8&iwloc=&output=embed"
  width="100%" height="350" frameborder="0" scrolling="no"
  style="border:0;" loading="lazy">
</iframe>'''))

blocks.append(h2("정리"))
blocks.append(wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:6px;overflow:hidden;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">YUKI 코이노트 사진 촬영 장소 정리</p>
<div style="padding:14px 18px;background:#f7f6f4;">
<p style="margin:0;">
✔ <strong>촬영일:</strong>2026년 8월 19일 업데이트된 코이노트에서 공개<br>
✔ <strong>배경의 정체:</strong>가나가와현 후지사와시의 에노시마, 하얀 타워는 전망 등대 '에노시마 씨캔들'로 보임<br>
✔ <strong>촬영 장소(추정):</strong>에노시마가 보이는 바닷가 데크가 있는 신에노시마 수족관(에노스이)<br>
✔ <strong>화제의 가족:</strong>신에노시마 수족관의 꽝 없는 "인형 뽑기"(1등~3등 등)로 만날 수 있는 아기수달 인형 "해피 마린"으로 보임<br>
✔ <strong>과거 방문 이력:</strong>밤에 촬영된 것으로 보이는 사진도 있어, 이전부터 에노시마를 방문했을 가능성이 있음
</p>
</div>
</div>'''))

blocks.append(p([
    "신에노시마 수족관이나 가나가와현 어딘가에서 우연히 YUKI와 마주치는 건 아닐까…라는 기대를 살짝 품게 될 정도로, 에노시마를 정말 좋아하는 것 같네요!",
    "공식 사이트에 따르면 이 인형 뽑기는 수량 한정으로, <strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;text-decoration:underline;\">소진되는 대로 종료</span></strong>된다고 합니다.",
    "YUKI와 같은 \"해피 마린\"을 가족으로 맞이하고 싶다면 서둘러 신에노시마 수족관에 다녀오는 수밖에 없겠네요! 지금 당장이라도 가고 싶을 정도네요・・・관심 있으신 분들은 함께 도전해봐요!",
]))

blocks.append(wphtml(f'''<div style="border:1px solid #ddd9d3;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f6f4;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">관련 기사</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-1.com/what-is-the-family-structure-o-10480">YUKI(고토 유이)의 가족 구성을 조사한 기사(일본어)</a></li>
<li><a href="https://chomoand-1.com/what-is-the-room-allocation-at-11122">KO1KEYZ 숙소 방 배정을 예상한 기사(일본어)</a></li>
<li><a href="https://chomoand-1.com/ko1keyz-why-was-the-debut-date-10449">KO1KEYZ 데뷔일의 이유를 해설한 기사(일본어)</a></li>
</ul>
</div>'''))

content = "\n\n".join(blocks)
print("content length (chars):", len(content))

JP_POST_ID = 11552
EXISTING_KR_POST_ID = 11560
slug = "where-is-yukis-goto-yui-koi-no-kr"

if EXISTING_KR_POST_ID:
    payload = {
        "title": title,
        "content": content,
        "status": "draft",
    }
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_KR_POST_ID}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print("UPDATED_KR_POST_ID", post["id"])
    print("SLUG", post["slug"])
    print("LINK", post.get("link"))
else:
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "categories": [66],
        "author": 2,
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
    print("KR_POST_ID", post["id"])
    print("SLUG", post["slug"])
    print("LINK", post.get("link"))

r2 = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"status": "draft", "featured_media": MEDIA_IDS["eyecatch"]}).encode("utf-8"),
)
r2.raise_for_status()

print("PREVIEW", f"{WP_URL}/?p={post['id']}")
