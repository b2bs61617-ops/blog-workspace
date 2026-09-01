# -*- coding: utf-8 -*-
import json, base64, os, subprocess, sys
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

JP_POST_ID = 12030
JP_SLUG = "how-many-piercings-do-ko1keyz"
CHART_IMG = ROOT / "images" / "ko1keyz_piercing_count_chart_kr.png"


def upload_media_from_file(path: Path, filename: str, content_type: str = "image/png"):
    headers = {
        **HEADERS_AUTH,
        "Content-Type": content_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=path.read_bytes())
    r.raise_for_status()
    return r.json()


chart_media = upload_media_from_file(CHART_IMG, "ko1keyz_piercing_count_chart_kr.png")
print("chart_media", chart_media["id"])


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


chart_html = "<!-- wp:html -->\n" + build_img_html(
    chart_media,
    "KO1KEYZ 12명의 피어싱 개수를 좌우 합산으로 정리한 도표",
    "X에 공유된 관찰 정보를 바탕으로 작성. 개수는 좌우 귀의 합계입니다.",
) + "\n<!-- /wp:html -->"


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


EMOJI_URL = "https://chomoand-1.com/summary-of-ko1keyz-member-emoj-10560"
CHEMI_URL = "https://chomoand-1.com/ko1keyz-chemi-names-11773"
SHOE_URL = "https://chomoand-1.com/what-are-the-shoe-sizes-of-ko1-11551"
RYUJI_URL = "https://chomoand-1.com/is-ryuji-left-handed-investiga-11388"

title = "KO1KEYZ 피어싱은 몇 개? 최다는 TOWA로 5개!"

blocks = []

blocks.append(p([
    "KO1KEYZ(코이키즈)는 귀 피어싱에 멤버별 개성이 잘 드러나는 그룹이에요.",
    "X에서는 멤버들의 귀를 한 명씩 관찰해 피어싱 위치를 정리한 게시글이 화제가 됐는데, 그에 따르면 <strong>가장 많은 것은 TOWA(하마다 토와)의 5개, 이어서 DAIKI(가토 다이키)의 4개, KOSUKE(테루이 코스케)의 3개</strong> 순이었어요.",
    "이 글에서는 12명 각자의 피어싱 개수를 좌우 내역과 함께 정리하고, 별 모티브나 골드 등 실제로 목격된 디자인도 함께 정리해볼게요.",
]))

blocks.append(titlebox("이 글에서 알 수 있는 것", [
    "멤버 12명 각자의 피어싱 개수(좌우 귀 내역 포함)",
    "피어싱이 많은 멤버・하지 않은 멤버",
    "KOSUKE의 별 피어싱 등 목격된 디자인",
]))

blocks.append(h2("KO1KEYZ 멤버들의 피어싱은 몇 개? 12명 정리"))
blocks.append(minibox('<p style="margin:0;"><strong>최다는 TOWA의 5개, 이어서 DAIKI가 4개, KOSUKE가 3개.</strong>KEITO・RYUJI・YOSHIKI・YUKI가 2개씩이고, 나머지 5명은 하지 않았어요.</p>'))
blocks.append(p([
    "정리의 바탕이 된 것은 2026년 8월 말에 X에 공유된, 멤버들의 귀를 한 명씩 관찰해 피어싱 구멍 위치를 적어둔 게시글이에요.",
    "여기에 데뷔 싱글 아티스트 사진이나 라이브・방송에서 보이는 모습을 더해 정리하면, 12명의 피어싱 개수는 다음과 같아요.",
]))
blocks.append(chart_html)
blocks.append(p([
    "좌우 귀의 내역까지 포함해 표로 정리하면 아래와 같아요.",
]))
blocks.append(table_block(
    ["멤버", "오른쪽 귀", "왼쪽 귀", "합계"],
    [
        ["TOWA(하마다 토와)", "2", "3", "5"],
        ["DAIKI(가토 다이키)", "2", "2", "4"],
        ["KOSUKE(테루이 코스케)", "1", "2", "3"],
        ["KEITO(오노 케이토)", "1", "1", "2"],
        ["RYUJI(스기야마 류지)", "1", "1", "2"],
        ["YUKI(고토 유이)", "1", "1", "2"],
        ["YOSHIKI(야다 요시키)", "1", "1", "2"],
        ["ISSA(야나기야 잇사)", "0", "0", "0"],
        ["YURA(아베 유라)", "0", "0", "0"],
        ["RYOGA(이이즈카 료가)", "0", "0", "0"],
        ["SIYOUNG(박시영)", "0", "0", "0"],
        ["SHINHAENG(오신행)", "0", "0", "0"],
    ],
))
blocks.append(p([
    f'<strong><span class="swl-marker mark_green" style="font-size:1.15em;">TOWA만 연골(헬릭스)에도 뚫어서 왼쪽 귀 3개・오른쪽 귀 2개로 합계 5개</span></strong>로 눈에 띄게 많아요.',
    "1~2개가 중심인 그룹 안에서 TOWA・DAIKI・KOSUKE 3명이 피어싱이 많은 편이라는 구도예요.",
]))
blocks.append(p([
    "다만 사진 각도에 따라 좌우 어느 쪽 귀인지 보기 어려운 부분도 있어서, YOSHIKI・YURA・YUKI의 일부는 게시글 작성자도 「자신이 없다」고 했어요.",
    "세부 개수는 앞으로 달라질 수 있다는 점만 먼저 말씀드릴게요.",
]))

blocks.append(h2("피어싱이 많은 TOP3는? TOWA・DAIKI・KOSUKE"))
blocks.append(minibox('<p style="margin:0;"><strong>상위는 TOWA(5)・DAIKI(4)・KOSUKE(3).</strong>3명 모두 여러 개를 뚫었고, 착용하는 피어싱 디자인도 잘 알려져 있어요.</p>'))
blocks.append(p([
    "<strong>TOWA(하마다 토와)</strong>는 왼쪽 귀에 3개, 오른쪽 귀에 2개.",
    "귓불뿐 아니라 연골에도 구멍이 있어, 12명 중 유일한 5개 보유자예요.",
    "셀카 오프숏에서는 실버 소재의 작은 스터드나 링을 착용하는 경우가 많고, 손가락 반지나 체인 목걸이와 함께 실버로 통일하는 것이 TOWA의 스타일로 자리잡았어요.",
]))
blocks.append(p([
    "<strong>DAIKI(가토 다이키)</strong>는 좌우 2개씩 합계 4개.",
    "본인이 X에서 「한국 공연까지 하고 싶은 것」 중 하나로 <strong>「피어싱 늘리기」</strong>를 꼽아서, 앞으로 더 늘어날 가능성이 있어요.",
    f'7월 중순 사복에서는 피어싱과 옷 색을 YOSHIKI와의 케미명 <a href="{CHEMI_URL}" target="_blank" rel="noopener">「데카네코」</a> 컬러로 맞췄다고 화제가 된 적도 있었어요.',
]))
blocks.append(p([
    "<strong>KOSUKE(테루이 코스케)</strong>는 오른쪽 귀 1개・왼쪽 귀 2개로 합계 3개.",
    '데뷔 싱글 아티스트 사진에서 착용한 <strong><span class="swl-marker mark_pink">별 모티브 피어싱</span></strong>이 팬들 사이에서 「별 피어싱」이라 불리며 「똑같은 걸 사러 가야겠다」는 반응이 이어졌어요.',
    f'멤버 컬러인 빨강과 함께 KOSUKE의 <a href="{EMOJI_URL}" target="_blank" rel="noopener">멤버 이모지도 별(🌟)</a>이라서, 이 별 피어싱은 트레이드마크로 자리잡아가고 있어요.',
]))

blocks.append(h2("2개씩 뚫은 멤버는? RYUJI・KEITO・YOSHIKI・YUKI"))
blocks.append(minibox('<p style="margin:0;"><strong>RYUJI・KEITO・YOSHIKI・YUKI 4명은 좌우 1개씩 합계 2개.</strong>그중 RYUJI는 피어싱을 자주 바꿔 끼는 타입이에요.</p>'))
blocks.append(p([
    "<strong>RYUJI(스기야마 류지)</strong>는 좌우 1개씩.",
    "데뷔 싱글 아티스트 사진에서는 피어싱과 이어 커프를 함께 착용했고, 팬들도 「피어싱과 이어 커프」를 최애 포인트로 꼽았어요.",
    "시기에 따라 실버에서 골드로 바꾸는 등 교체도 잦아서, 반려견과 노는 오프숏에서 「전보다 피어싱이 확실히 골드가 됐다」고 알아채거나, 「늘 하던 피어싱을 뺐다」며 뺀 날에 반응이 오는 등 귀 부분의 변화가 자주 포착되고 있어요.",
]))
blocks.append(p([
    "<strong>KEITO(오노 케이토)</strong>도 좌우 1개씩 2개로, 장식이 적은 실버 스터드가 중심이에요.",
    "<strong>YOSHIKI(야다 요시키)</strong>는 좌우 1개씩으로 보이지만, 오른쪽 귀 구멍은 관찰 게시글에서도 「자신이 없다」고 해서 확실히 확인되는 것은 1개예요.",
    "<strong>YUKI(고토 유이)</strong>도 좌우 1개씩 2개로, 2026년 8월 사진에서 피어싱을 착용한 모습이 확인돼 「얼굴도 잘생겼는데 피어싱까지 했다」는 반응이 있었어요.",
]))

blocks.append(h2("피어싱을 하지 않은 멤버는? 5명"))
blocks.append(minibox('<p style="margin:0;"><strong>ISSA・YURA・RYOGA・SIYOUNG・SHINHAENG 5명은 현재 피어싱 구멍이 확인되지 않아요.</strong></p>'))
blocks.append(p([
    "야구에 전념했던 ISSA(야나기야 잇사), 축구에 전념했던 RYOGA(이이즈카 료가), 한국 출신인 SIYOUNG(박시영)과 SHINHAENG(오신행) 등, 지금까지 활동에서 피어싱을 뚫을 기회가 적었던 멤버들이 모여 있어요.",
    "다만 데뷔 후에 메이크업이나 의상에 맞춰 뚫는 멤버가 나올 가능성은 충분해요.",
    "실제로 RYUJI도 활동 초기에는 피어싱 색이나 개수가 지금과 달랐기 때문에, 이 목록은 「2026년 가을 시점의 스냅샷」 정도로 봐두는 게 좋을 것 같아요.",
]))

blocks.append(titlebox("정리", [
    "피어싱이 가장 많은 것은 TOWA로, 연골 포함 합계 5개",
    "이어서 DAIKI가 4개, KOSUKE가 3개. KEITO・RYUJI・YOSHIKI・YUKI가 2개씩",
    "ISSA・YURA・RYOGA・SIYOUNG・SHINHAENG 5명은 피어싱 구멍이 확인되지 않음",
    "KOSUKE의 별 모티브, RYUJI의 골드＋이어 커프 등 디자인도 멤버별로 개성 있음",
]))
blocks.append(p([
    "귀 부분까지 보면 실버로 통일하는 TOWA, 별을 트레이드마크로 삼는 KOSUKE 등 멤버들의 취향이 의외로 뚜렷하게 드러나요.",
    "라이브 영상이나 아티스트 사진을 볼 때는 꼭 귀 부분에도 주목해보세요!",
]))

blocks.append(minibox(f'''<p style="margin:0 0 8px 0;"><strong>KO1KEYZ에 대해서는 이 블로그의 다른 글에서도 자세히 소개하고 있어요.</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{EMOJI_URL}" target="_blank" rel="noopener">멤버 12명의 이모지와 그 의미 정리(일본어)</a></li>
<li><a href="{SHOE_URL}" target="_blank" rel="noopener">KO1KEYZ 멤버들의 신발 사이즈는? 신세카이 의상 전시에서 밝혀져!</a></li>
<li><a href="{RYUJI_URL}" target="_blank" rel="noopener">RYUJI는 왼손잡이? 양손잡이설 진실 조사!</a></li>
<li><a href="{CHEMI_URL}" target="_blank" rel="noopener">KO1KEYZ 케미명 정리! 「데카네코」 「토와스케」란?</a></li>
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

EYECATCH_PATH = ROOT / "images" / "ko1keyz_piercings_eyecatch_kr.png"
subprocess.run([
    sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
    "--top", "피어싱은 몇 개?",
    "--main", "KO1KEYZ",
    "--bottom", "멤버 12명의 귀를 조사!",
    "--bottom", "최다는 TOWA로 5개",
    "--lang", "kr",
    "--out", str(EYECATCH_PATH),
    "--seed", str(post["id"]),
], check=True)

eyecatch_media = upload_media_from_file(EYECATCH_PATH, "ko1keyz_piercings_eyecatch_kr.png")
KR_EYECATCH_ID = eyecatch_media["id"]
print("KR_EYECATCH_ID", KR_EYECATCH_ID)

featured_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"featured_media": KR_EYECATCH_ID, "status": "draft"}).encode("utf-8"),
)
featured_r.raise_for_status()
print("FEATURED_MEDIA set to", KR_EYECATCH_ID)

(ROOT / "tmp_ko1keyz_piercings_kr_postid.txt").write_text(str(post["id"]), encoding="utf-8")
