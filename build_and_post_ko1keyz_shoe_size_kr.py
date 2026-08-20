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

JP_POST_ID = 11551
JP_SLUG = "what-are-the-shoe-sizes-of-ko1"
IMG_MEDIA_ID = 11549
EYECATCH_MEDIA_ID = 11553

SOURCE_TWEET = "https://x.com/lalabonbondrop/status/2090264614382788644"

img1_media = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{IMG_MEDIA_ID}", headers=HEADERS_AUTH).json()


def build_img_html(media, alt, caption):
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
<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>
</figure>'''


IMG_CAPTION = f'출처:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>'
img1_html = f"<!-- wp:html -->\n{build_img_html(img1_media, 'HMV 신세카이 의상 전시에서 촬영된, 멤버 6명분의 신발 사이즈 태그', IMG_CAPTION)}\n<!-- /wp:html -->"


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


def titlebox(ttl, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def table_block(headers, rows):
    thead = "".join(f"<td>{h}</td>" for h in headers)
    trows = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr>{thead}</tr>
{trows}
</tbody></table></figure>
<!-- /wp:table -->'''


HEYAWARI_URL = "https://chomoand-1.com/what-is-the-room-allocation-at-11122"
RYUJI_LEFTHANDED_URL = "https://chomoand-1.com/is-ryuji-left-handed-investiga-11388"
DEBUT_SINGLE_URL = "https://chomoand-1.com/when-will-ko1keyzs-debut-singl-10866"

title = "KO1KEYZ 멤버들의 신발 사이즈는? 신세카이 의상 전시에서 밝혀져!"

blocks = []

blocks.append(p([
    "『PRODUCE 101 JAPAN 신세카이』 출신 KO1KEYZ는 2026년 10월 7일 데뷔를 앞두고 매일 새로운 화제를 모으고 있는 그룹이에요.",
    "그런 가운데 HMV에서 진행 중인 데뷔 싱글 『신세카이』 의상 전시를 보러 간 팬이, 신발 안쪽에 붙어 있던 사이즈 태그를 우연히 발견해 X에 공유하면서 화제가 됐어요.",
    f"확인된 6명 중 <strong>가장 큰 사이즈는 RYUJI의 27.5cm, 가장 작은 사이즈는 YOSHIKI와 TOWA의 26.0cm</strong>였어요.<br>\n이 글에서는 X에 공유된 내용을 바탕으로 멤버별 신발 사이즈를 정리해볼게요.",
]))

blocks.append(titlebox("이 글에서 알 수 있는 것", [
    "HMV 신세카이 의상 전시에서 밝혀진 멤버들의 신발 사이즈",
    "사이즈 태그로 확인된 신발 브랜드・품번",
    "이번에 사이즈가 확인되지 않은 멤버",
]))

blocks.append(h2("HMV 신세카이 의상 전시에서 신발 사이즈 태그 확인"))
blocks.append(minibox('<p style="margin:0;"><strong>목격 장소:</strong>HMV(『신세카이』 의상 전시)<br><strong>공유일:</strong>2026년 8월 20일</p>'))
blocks.append(p([
    "X에는 2026년 8월 20일, 『신세카이』 의상 전시를 HMV에서 보고 왔다는 팬이 \"신세카이 의상 전시 보러 갔다가 신발 사이즈 태그가 보였다\"는 내용을 공유했어요.",
    "게시글에는 6명분의 신발 안쪽 사이즈 태그를 촬영한 사진이 함께 올라와, 멤버별 발 사이즈가 그대로 밝혀지는 형태가 됐어요.",
    "작성자에 따르면 이 전시는 HMV에서만 볼 수 있고, 타워레코드는 영업시간 사정으로 확인하지 못했다고 해요.",
]))
blocks.append(img1_html)

blocks.append(h2("KO1KEYZ 멤버 신발 사이즈 정리"))
blocks.append(minibox('<p style="margin:0;"><strong>확인된 것은 12명 중 6명분.</strong>가장 큰 사이즈는 RYUJI의 27.5cm, 가장 작은 사이즈는 YOSHIKI와 TOWA의 26.0cm였어요.</p>'))
blocks.append(p([
    "사이즈 태그에 적혀 있던 내용을 멤버별로 표로 정리했어요.",
]))
blocks.append(table_block(
    ["멤버", "사이즈(cm)", "비고"],
    [
        ["YOSHIKI(야다 요시키)", "26.0", "-"],
        ["TOWA(하마다 토와)", "26.0", "-"],
        ["SHINHAENG(오신행)", "26.5", "-"],
        ["ISSA(야나기야 잇사)", "27.0", "-"],
        ["RYUJI(스기야마 류지)", "27.5", "깔창 없이 착용"],
        ["YURA(아베 유라)", "-", "사진에 사이즈 태그가 찍히지 않아 미확인"],
    ],
))
blocks.append(p([
    f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">가장 큰 RYUJI(27.5cm)와 가장 작은 YOSHIKI・TOWA(26.0cm) 사이에는 1.5cm 차이</span></strong>가 있다는 것도 확인됐어요.',
]))

blocks.append(h2("신발 브랜드・품번도 밝혀져?"))
blocks.append(minibox('<p style="margin:0;"><strong>신발은 PUMA, 품번은 6명 모두 공통으로 「397447-02」였어요.</strong></p>'))
blocks.append(p([
    "사이즈 태그를 자세히 보면 신발은 PUMA 모델로, 6명 모두 품번 「397447-02」가 동일한 것을 확인할 수 있어요.",
    "태그에는 「MADE IN CHINA」 표기와 「07/25」로 보이는 생산 시기 숫자도 적혀 있어, 같은 모델의 신발을 멤버마다 다른 사이즈로 나눠 신고 있는 것으로 보여요.",
    "데뷔 싱글 『신세카이』 무대 의상으로 통일된 신발을 채택한 것으로 보이며, 발끝까지 세심하게 스타일링됐다는 점을 이번 태그 확인을 통해 다시 한번 알 수 있었어요.",
]))

blocks.append(h2("사이즈가 확인되지 않은 나머지 6명은?"))
blocks.append(minibox('<p style="margin:0;"><strong>이번에 태그가 확인된 것은 6명.</strong>나머지 KOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNG은 미확인이에요.</p>'))
blocks.append(p([
    "이번 게시글에서 사이즈 태그가 확인된 것은 YOSHIKI・TOWA・SHINHAENG・ISSA・RYUJI・YURA 6명이었어요.",
    "나머지 KOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNG 6명은 작성자도 다른 전시 매장(타워레코드 등)을 확인하지 못했다고 해서, 현재로서는 사이즈를 알 수 없어요.",
    "다른 매장에서 목격 정보가 나오면 이 글에서도 이어서 전해드릴게요.",
]))

blocks.append(titlebox("정리", [
    "HMV 『신세카이』 의상 전시에서 6명분의 신발 사이즈 태그가 우연히 공개돼 화제",
    "사이즈는 YOSHIKI・TOWA가 26.0cm, SHINHAENG이 26.5cm, ISSA가 27.0cm, RYUJI가 27.5cm",
    "신발은 PUMA의 같은 모델(품번 397447-02)을 전원 사이즈만 다르게 착용",
    "나머지 6명(KOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNG)의 사이즈는 미확인",
]))
blocks.append(p([
    "이런 소소한 발견도 데뷔를 앞둔 KO1KEYZ의 새로운 매력을 알아가는 계기가 되겠죠!",
]))

blocks.append(minibox(f'''<p style="margin:0 0 8px 0;"><strong>KO1KEYZ에 대해서는 이 블로그의 다른 글에서도 자세히 소개하고 있어요.</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{HEYAWARI_URL}" target="_blank" rel="noopener">KO1KEYZ 숙소 방 배정 예상!</a></li>
<li><a href="{RYUJI_LEFTHANDED_URL}" target="_blank" rel="noopener">RYUJI는 왼손잡이? 양손잡이설 진실 조사!</a></li>
<li><a href="{DEBUT_SINGLE_URL}" target="_blank" rel="noopener">데뷔 싱글 『KO1KEYZ』는 언제 발매?수록곡・특전 정리</a></li>
</ul>'''))

content = "\n\n".join(blocks)

slug = JP_SLUG + "-kr"
payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": "draft",
    "categories": [66, 62],
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
print("KR_SLUG", post["slug"])
print("KR_LINK", post.get("link"))

featured_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"featured_media": EYECATCH_MEDIA_ID, "status": "draft"}).encode("utf-8"),
)
featured_r.raise_for_status()
print("FEATURED_MEDIA set to", EYECATCH_MEDIA_ID)

with open(ROOT / "tmp_ko1keyz_shoe_size_kr_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
