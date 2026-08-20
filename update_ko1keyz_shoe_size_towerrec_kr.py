# -*- coding: utf-8 -*-
import base64, json
import requests

def load_env(path):
    env = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env

env = load_env('.env')
WP_URL = env['WP_KOIKEYS_URL'].rstrip('/')
AUTH = base64.b64encode(f"{env['WP_KOIKEYS_USERNAME']}:{env['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
h = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}
hget = {'Authorization': f'Basic {AUTH}'}

KOSUKE_MEDIA_ID = 11635
TOWERREC_TWEET = "https://x.com/azmchan1202/status/2090335670049062963"

media = requests.get(f'{WP_URL}/wp-json/wp/v2/media/{KOSUKE_MEDIA_ID}', headers=hget).json()

def build_img_html(media, alt, caption, size_key="large"):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    full_w = media["media_details"]["width"]
    full_h = media["media_details"]["height"]
    chosen = sizes.get(size_key, {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    img_src = chosen["source_url"]
    img_w = chosen["width"]
    img_h = int(img_w * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {chosen["source_url"]} {chosen["width"]}w, {full_url} {full_w}w'
    return f'''<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>
</figure>'''

r = requests.get(f'{WP_URL}/wp-json/wp/v2/posts/11556?context=edit', headers=hget)
r.raise_for_status()
raw = r.json()['content']['raw']

replacements = []

old1 = '''<p>『PRODUCE 101 JAPAN 신세카이』 출신 KO1KEYZ는 2026년 10월 7일 데뷔를 앞두고 매일 새로운 화제를 모으고 있는 그룹이에요.<br>
그런 가운데 HMV에서 진행 중인 데뷔 싱글 『신세카이』 의상 전시를 보러 간 팬이, 신발 안쪽에 붙어 있던 사이즈 태그를 우연히 발견해 X에 공유하면서 화제가 됐어요.<br>
확인된 6명 중 <strong>가장 큰 사이즈는 RYUJI의 27.5cm, 가장 작은 사이즈는 YOSHIKI와 TOWA의 26.0cm</strong>였어요.<br>
이 글에서는 X에 공유된 내용을 바탕으로 멤버별 신발 사이즈를 정리해볼게요.</p>'''
new1 = '''<p>『PRODUCE 101 JAPAN 신세카이』 출신 KO1KEYZ는 2026년 10월 7일 데뷔를 앞두고 매일 새로운 화제를 모으고 있는 그룹이에요.<br>
그런 가운데 HMV와 타워레코드 시부야점에서 진행 중인 데뷔 싱글 『신세카이』 의상 전시를 보러 간 팬들이, 신발 안쪽에 붙어 있던 사이즈 태그를 우연히 발견해 X에 공유하면서 화제가 됐어요.<br>
확인된 10명 중 <strong>가장 큰 사이즈는 RYUJI・KOSUKE・DAIKI의 27.5cm, 가장 작은 사이즈는 YOSHIKI와 TOWA의 26.0cm</strong>였어요.<br>
이 글에서는 X에 공유된 내용을 바탕으로 멤버별 신발 사이즈를 정리해볼게요.</p>'''
replacements.append((old1, new1))

old2 = '''<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ded9d2;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#8a8378;color:#fff;">이 글에서 알 수 있는 것</p>'''
new2 = '''<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ded9d2;border-left:4px solid #8a8378;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f8f6f4;">
<p style="margin:0;"><strong>추가 업데이트(2026년 8월 21일):</strong>타워레코드 시부야점에서 새롭게 공유된 목격 정보로 KOSUKE・DAIKI・SIYOUNG・RYOGA 4명의 사이즈가 새로 확인됐어요. 최신 정보를 반영해 업데이트했어요.</p>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div style="border:1px solid #ded9d2;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#8a8378;color:#fff;">이 글에서 알 수 있는 것</p>'''
replacements.append((old2, new2))

old3 = '<h2 class="wp-block-heading">HMV 신세카이 의상 전시에서 신발 사이즈 태그 확인</h2>'
new3 = '<h2 class="wp-block-heading">HMV・타워레코드 시부야점에서 신발 사이즈 태그 확인</h2>'
replacements.append((old3, new3))

old4 = '<p style="margin:0;"><strong>목격 장소:</strong>HMV(『신세카이』 의상 전시)<br><strong>공유일:</strong>2026년 8월 20일</p>'
new4 = '<p style="margin:0;"><strong>목격 장소:</strong>HMV・타워레코드 시부야점(『신세카이』 의상 전시)<br><strong>공유일:</strong>2026년 8월 20일・21일</p>'
replacements.append((old4, new4))

old5 = '''<figcaption style="text-align:center;font-size:12px;">출처:<a href="https://x.com/lalabonbondrop/status/2090264614382788644" target="_blank" rel="noopener">https://x.com/lalabonbondrop/status/2090264614382788644</a></figcaption>
</figure>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">KO1KEYZ 멤버 신발 사이즈 정리</h2>'''

towerrec_img_html = build_img_html(
    media,
    '타워레코드 시부야점 신세카이 의상 전시에서 촬영된, KOSUKE의 신발 사이즈 태그(품번 397447-02)',
    f'출처:<a href="{TOWERREC_TWEET}" target="_blank" rel="noopener">{TOWERREC_TWEET}</a>',
)

new5 = f'''<figcaption style="text-align:center;font-size:12px;">출처:<a href="https://x.com/lalabonbondrop/status/2090264614382788644" target="_blank" rel="noopener">https://x.com/lalabonbondrop/status/2090264614382788644</a></figcaption>
</figure>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>이어서 2026년 8월 21일에는 타워레코드 시부야점의 전시를 보고 왔다는 다른 팬이 KOSUKE・DAIKI・SIYOUNG・RYOGA의 신발 사이즈 태그를 촬영한 게시글을 올렸어요.<br>
이 게시글에 따르면 KOSUKE와 DAIKI는 둘 다 27.5cm, SIYOUNG은 27.0cm, RYOGA는 26.5cm(태그의 US 사이즈 표기로 추정)라고 해요.<br>
작성자에 따르면 각도상 YUKI와 KEITO의 태그만은 끝내 확인하지 못했다고 해요.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{towerrec_img_html}
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">KO1KEYZ 멤버 신발 사이즈 정리</h2>'''
replacements.append((old5, new5))

old6 = '<p style="margin:0;"><strong>확인된 것은 12명 중 6명분.</strong>가장 큰 사이즈는 RYUJI의 27.5cm, 가장 작은 사이즈는 YOSHIKI와 TOWA의 26.0cm였어요.</p>'
new6 = '<p style="margin:0;"><strong>확인된 것은 12명 중 10명분.</strong>가장 큰 사이즈는 RYUJI・KOSUKE・DAIKI의 27.5cm, 가장 작은 사이즈는 YOSHIKI와 TOWA의 26.0cm였어요.</p>'
replacements.append((old6, new6))

old7 = '''<tr><td>멤버</td><td>사이즈(cm)</td><td>비고</td></tr>
<tr><td>YOSHIKI(야다 요시키)</td><td>26.0</td><td>-</td></tr>
<tr><td>TOWA(하마다 토와)</td><td>26.0</td><td>-</td></tr>
<tr><td>SHINHAENG(오신행)</td><td>26.5</td><td>-</td></tr>
<tr><td>ISSA(야나기야 잇사)</td><td>27.0</td><td>-</td></tr>
<tr><td>RYUJI(스기야마 류지)</td><td>27.5</td><td>깔창 없이 착용</td></tr>
<tr><td>YURA(아베 유라)</td><td>-</td><td>사진에 사이즈 태그가 찍히지 않아 미확인</td></tr>'''
new7 = '''<tr><td>멤버</td><td>사이즈(cm)</td><td>비고</td></tr>
<tr><td>YOSHIKI(야다 요시키)</td><td>26.0</td><td>-</td></tr>
<tr><td>TOWA(하마다 토와)</td><td>26.0</td><td>-</td></tr>
<tr><td>SHINHAENG(오신행)</td><td>26.5</td><td>-</td></tr>
<tr><td>RYOGA(이이즈카 료가)</td><td>26.5(추정)</td><td>US 사이즈 8.5로 추정, cm 표기는 미확인</td></tr>
<tr><td>ISSA(야나기야 잇사)</td><td>27.0</td><td>-</td></tr>
<tr><td>SIYOUNG(박시영)</td><td>27.0</td><td>-</td></tr>
<tr><td>RYUJI(스기야마 류지)</td><td>27.5</td><td>깔창 없이 착용</td></tr>
<tr><td>KOSUKE(테루이 코스케)</td><td>27.5</td><td>-</td></tr>
<tr><td>DAIKI(카토 다이키)</td><td>27.5</td><td>-</td></tr>
<tr><td>YURA(아베 유라)</td><td>-</td><td>신발・이름 태그는 확인됐지만 사이즈 표기는 미확인</td></tr>'''
replacements.append((old7, new7))

old8 = '<p><strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">가장 큰 RYUJI(27.5cm)와 가장 작은 YOSHIKI・TOWA(26.0cm) 사이에는 1.5cm 차이</span></strong>가 있다는 것도 확인됐어요.</p>'
new8 = '<p><strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">가장 큰 RYUJI・KOSUKE・DAIKI(27.5cm)와 가장 작은 YOSHIKI・TOWA(26.0cm) 사이에는 1.5cm 차이</span></strong>가 있다는 것도 확인됐어요.</p>'
replacements.append((old8, new8))

old9 = '<p style="margin:0;"><strong>신발은 PUMA의 「CLUB II ERA(클럽 II 에라)」, 품번은 6명 모두 공통으로 「397447-02」였어요.</strong></p>'
new9 = '<p style="margin:0;"><strong>신발은 PUMA의 「CLUB II ERA(클럽 II 에라)」, 품번은 지금까지 확인된 10명 모두 공통으로 「397447-02」였어요.</strong></p>'
replacements.append((old9, new9))

old10 = '<p>사이즈 태그를 자세히 보면 신발은 PUMA 모델로, 6명 모두 품번 「397447-02」가 동일한 것을 확인할 수 있어요.<br>'
new10 = '<p>사이즈 태그를 자세히 보면 신발은 PUMA 모델로, 지금까지 확인된 10명 모두 품번 「397447-02」가 동일한 것을 확인할 수 있어요.<br>'
replacements.append((old10, new10))

old11 = '<h2 class="wp-block-heading">사이즈가 확인되지 않은 나머지 6명은?</h2>'
new11 = '<h2 class="wp-block-heading">사이즈가 확인되지 않은 나머지 2명은?</h2>'
replacements.append((old11, new11))

old12 = '<p style="margin:0;"><strong>이번에 태그가 확인된 것은 6명.</strong>나머지 KOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNG은 미확인이에요.</p>'
new12 = '<p style="margin:0;"><strong>지금까지 태그가 확인된 것은 10명.</strong>나머지 YUKI・KEITO는 미확인이에요.</p>'
replacements.append((old12, new12))

old13 = '''<p>이번 게시글에서 사이즈 태그가 확인된 것은 YOSHIKI・TOWA・SHINHAENG・ISSA・RYUJI・YURA 6명이었어요.<br>
나머지 KOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNG 6명은 작성자도 다른 전시 매장(타워레코드 등)을 확인하지 못했다고 해서, 현재로서는 사이즈를 알 수 없어요.<br>
다른 매장에서 목격 정보가 나오면 이 글에서도 이어서 전해드릴게요.</p>'''
new13 = '''<p>지금까지의 게시글에서 사이즈 태그가 확인된 것은 YOSHIKI・TOWA・SHINHAENG・ISSA・RYUJI・KOSUKE・DAIKI・SIYOUNG・RYOGA 9명과, 신발・이름 태그만 확인된 YURA를 더한 10명이었어요.<br>
나머지 YUKI・KEITO 2명은 HMV・타워레코드 어느 쪽 작성자도 각도상 확인하지 못했다고 해서, 현재로서는 사이즈를 알 수 없어요.<br>
다른 목격 정보가 나오면 이 글에서도 이어서 전해드릴게요.</p>'''
replacements.append((old13, new13))

old14 = '''<li>HMV 『신세카이』 의상 전시에서 6명분의 신발 사이즈 태그가 우연히 공개돼 화제</li>
<li>사이즈는 YOSHIKI・TOWA가 26.0cm, SHINHAENG이 26.5cm, ISSA가 27.0cm, RYUJI가 27.5cm</li>
<li>신발은 PUMA의 「CLUB II ERA」(품번 397447-02)를 전원 사이즈만 다르게 착용, 참고 가격은 10,450엔(세금 포함)</li>
<li>나머지 6명(KOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNG)의 사이즈는 미확인</li>'''
new14 = '''<li>HMV・타워레코드 시부야점의 『신세카이』 의상 전시에서 10명분의 신발 사이즈 태그가 우연히 공개돼 화제</li>
<li>사이즈는 YOSHIKI・TOWA가 26.0cm, SHINHAENG・RYOGA가 26.5cm, ISSA・SIYOUNG이 27.0cm, RYUJI・KOSUKE・DAIKI가 27.5cm</li>
<li>신발은 PUMA의 「CLUB II ERA」(품번 397447-02)를 지금까지 확인된 10명이 사이즈만 다르게 착용, 참고 가격은 10,450엔(세금 포함)</li>
<li>나머지 2명(YUKI・KEITO)의 사이즈는 미확인</li>'''
replacements.append((old14, new14))

for i, (old, new) in enumerate(replacements, 1):
    cnt = raw.count(old)
    assert cnt == 1, f"replacement {i} matched {cnt} times, expected 1"
    raw = raw.replace(old, new)

ur = requests.post(f'{WP_URL}/wp-json/wp/v2/posts/11556', headers=h, data=json.dumps({"content": raw}).encode('utf-8'))
ur.raise_for_status()
print("KR updated, length:", len(ur.json()['content']['raw']))
open('tmp_kr_updated.html', 'w', encoding='utf-8').write(raw)
