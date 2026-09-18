# -*- coding: utf-8 -*-
"""RYOGAの自己紹介NARUTO考察記事(JP post 13189)の韓国語版・英語版下書きを作成する。
画像は言語分けなしなのでJPと同じmedia(13186 kick / 13187 pose / 13188 reveal)を再利用。
KRは韓国語アイキャッチを別生成、ENはJPと同じアイキャッチ(media 13190)を使う。
"""
import base64, json, os, re, subprocess, sys
from pathlib import Path

import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f'{ENV["WP_KOIKEYS_USERNAME"]}:{ENV["WP_KOIKEYS_APP_PASSWORD"]}'.encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"}

JA_ID = 13189
KICK_MEDIA = 13186
POSE_MEDIA = 13187
REVEAL_MEDIA = 13188
JP_EYECATCH_MEDIA = 13190
VIDEO_URL = "https://www.youtube.com/watch?v=KTlObvSe1SM"

AB, AL, BG = "#c3cbe0", "#5b6fa8", "#f0f2f8"

RYOGA_PROFILE_IMG = "https://chomoand-1.com/wp-content/uploads/2026/08/ryoga_concept_photo1-333x500.jpg"
RYOGA_PROFILE_IMG_SRCSET = ("https://chomoand-1.com/wp-content/uploads/2026/08/ryoga_concept_photo1-200x300.jpg 200w, "
                             "https://chomoand-1.com/wp-content/uploads/2026/08/ryoga_concept_photo1-333x500.jpg 333w, "
                             "https://chomoand-1.com/wp-content/uploads/2026/08/ryoga_concept_photo1.jpg 780w")


def fetch_media_img_html(media_id, alt, caption):
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{media_id}", headers={"Authorization": f"Basic {AUTH}"})
    r.raise_for_status()
    m = r.json()
    sizes = m.get("media_details", {}).get("sizes", {})
    full_url = m["source_url"]; full_w = m["media_details"]["width"]; full_h = m["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    iw = large["width"]; ih = int(iw * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {full_w}w'
    return (f'<!-- wp:html -->\n<figure class="wp-block-image size-large">\n'
            f'<img src="{large["source_url"]}" alt="{alt}" width="{iw}" height="{ih}"\n'
            f'  style="max-width:100%;height:auto;"\n  srcset="{srcset}"\n'
            f'  sizes="(max-width: {iw}px) 100vw, {iw}px">\n'
            f'<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>\n</figure>\n<!-- /wp:html -->')


PROFILE_IMG_HTML = f"""<!-- wp:html -->
<figure class="wp-block-image size-large" style="text-align:center;">
  <img src="{RYOGA_PROFILE_IMG}" alt="RYOGA profile photo" style="max-width:333px;width:100%;height:auto;margin:0 auto;" srcset="{RYOGA_PROFILE_IMG_SRCSET}">
  <figcaption style="text-align:center;font-size:12px;">Source:<a href="https://x.com/KO1KEYZofficial/status/2081673449924374924" target="_blank" rel="noopener">@KO1KEYZofficial(X)</a></figcaption>
</figure>
<!-- /wp:html -->"""

VIDEO_LABEL_KR = 'KO1KEYZ 공식 유튜브 「[EP.1] KO1! KO1! KO1KEYZ｜큥투군 학원〜신입생 오디션〜」'
VIDEO_LABEL_EN = 'KO1KEYZ official YouTube, "[EP.1] KO1! KO1! KO1KEYZ | Kyuntugun Academy - New Student Audition"'

# ---------------- KOREAN ----------------
KR_TITLE = "RYOGA의 자기소개가 설마 카쿠레의 술? NARUTO 드립에 다들 뒤집어졌다"
KR_SLUG = "ryoga-jikoshoukai-naruto-kuchiyose-kr"

kr_kick = fetch_media_img_html(KICK_MEDIA, "자기소개 중 축구 킥 동작을 재현하는 RYOGA(이이즈카 료가)",
    f'출처:{VIDEO_LABEL_KR}')
kr_pose = fetch_media_img_html(POSE_MEDIA, "자기소개 도중 양팔을 크게 움직이는 수수께끼의 포즈를 보여주는 RYOGA(이이즈카 료가)",
    f'출처:{VIDEO_LABEL_KR}')
kr_reveal = fetch_media_img_html(REVEAL_MEDIA, "한바탕 움직인 뒤 진지한 얼굴로 「애니와 만화를 정말 좋아합니다」라고 말하는 RYOGA(이이즈카 료가)",
    f'출처:{VIDEO_LABEL_KR}')

KR_CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZ(코이키즈)의 새 프로그램 「KO1! KO1! KO1KEYZ」 첫 회에서, RYOGA(이이즈카 료가)의 자기소개 코너가 SNS에서 큰 화제가 되고 있습니다.<br>
음악이 갑자기 멈추더니 축구 킥 동작, 그리고 양팔을 사용한 수수께끼의 포즈를 연달아 선보이고, 진지한 얼굴로 「애니와 만화를 정말 좋아합니다」라고 말해버리는, 1분 사이에 정보량이 지나치게 많은 자기소개였기 때문입니다.<br>
팬들 사이에서는 이 포즈의 원조가 「NARUTO의 카쿠레의 술 아니야?」 「아니, 진격의 거인의 거인화 같은데」 「드래곤볼의 원기옥 아니야?」로 의견이 갈리고 있어, 아직 진상은 확실치 않습니다.<br>
이 글에서는 방송 내용을 되짚어보며 RYOGA의 자기소개에서 무슨 일이 있었는지, 그리고 그 포즈의 원조가 무엇이었는지를 짚어봅니다.</p>
<!-- /wp:paragraph -->

{PROFILE_IMG_HTML}

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AL};color:#fff;">이 글에서 알 수 있는 것</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>「KO1! KO1! KO1KEYZ」 첫 회가 어떤 프로그램인지</li>
<li>RYOGA의 자기소개에서 실제로 무슨 일이 있었는지</li>
<li>수수께끼 포즈의 원조 후보(NARUTO・진격의 거인・드래곤볼)</li>
<li>NARUTO설이 유력해 보이는 이유</li>
<li>RYOGA가 원래 「자기소개 장인」이었다는 과거 에피소드</li>
<li>SNS 팬들의 반응</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">「KO1!KO1!KO1KEYZ」 첫 회는 어떤 프로그램?</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>프로그램:</strong>KO1! KO1! KO1KEYZ 1화 「큥투군 학원〜신입생 오디션〜」</p>
<p style="margin:4px 0 0 0;"><strong>공개:</strong>KO1KEYZ 공식 유튜브에서 무료 공개, 2026년 9월 17일(목) 21:00〜, 매주 목요일 업데이트</p>
<p style="margin:4px 0 0 0;"><strong>내용:</strong>멤버 12명이 「큥투군 학원」의 신입생이라는 설정으로 1인당 1분씩 자기소개를 한 뒤, 「가장 친해지고 싶다」고 생각한 1명에게 투표</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>「KO1! KO1! KO1KEYZ」는 KO1KEYZ 공식 유튜브 채널에서 2026년 9월 17일(목) 21:00부터 무료 공개가 시작된 새 프로그램입니다.<br>
기념할 첫 회는 「큥투군 학원〜신입생 오디션〜」이라는 학원 콩트 기획으로, 멤버 12명이 같은 반에 전학 온 신입생이라는 설정으로 등장합니다.<br>
룰은 한 명씩 1분간 자기소개를 한 뒤, 전원의 자기소개가 끝나면 「가장 친구가 되고 싶다고 생각한 사람」에게 1표를 던지는 것.<br>
최다 득표를 얻은 멤버가 「친구가 되고 싶은 신입생 넘버원」이 되는 구조로, 멤버들은 주어진 1분을 최대한 활용해 개성을 어필했습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">RYOGA의 자기소개에서 무슨 일이? 흐름을 자세히 살펴보기</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>수많은 자기소개 중에서도 SNS에서 특히 반응이 컸던 것이 RYOGA의 자기소개입니다.<br>
「군마현 출신 이이즈카 료가라고 합니다」라고 이름을 밝히자 같은 군마현 출신 멤버가 「친해지면 좋겠다」고 말을 걸고, 「어떻게 왔어?」라는 질문에 「그냥 전철로」라고 농담을 던지는 등, 초반에는 화기애애한 분위기로 진행됩니다.<br>
그런데 여기서부터 RYOGA의 자기소개는 단숨에 속도를 올립니다.</p>
<!-- /wp:paragraph -->

{kr_kick}

<!-- wp:paragraph -->
<p>먼저 튀어나온 것이 「축구를 15년간 해왔습니다. 그래서 운동에는 조금 자신이 있습니다」라는 소개에 맞춘, 제법 본격적인 킥 동작입니다.<br>
중・고등학교 시절 축구에 몰두했던 RYOGA다운, 말이 아니라 몸으로 말하는 자기소개였지만, 이건 아직 서막에 불과했습니다.</p>
<!-- /wp:paragraph -->

{kr_pose}

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>화제 포인트:</strong>킥 동작 직후, RYOGA는 양팔을 크게 움직이는 수수께끼의 포즈를 선보였다.<br>정체를 알 수 없었던 같은 반 역할의 멤버들에게서 「그리고」 「뭐야 그게? 뭐야 그게?」라는 당혹스러운 목소리가 나왔다</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>음악이 한순간 멈출 정도의 정적을 만든 뒤 터져 나온 이 포즈에, 주변 멤버들은 저도 모르게 「뭐야 그게? 뭐야 그게?」라고 입을 모을 만큼 당황한 모습이었습니다.<br>
그리고 그렇게 격렬하게 움직인 직후라고는 믿기지 않을 만큼 차분한 진지한 얼굴로 나온 말이 <strong>「애니와 만화를 정말 좋아합니다」</strong>였습니다.</p>
<!-- /wp:paragraph -->

{kr_reveal}

<!-- wp:paragraph -->
<p>여기에 「그리고 이 외모로 집돌이 생활도 정말 좋아합니다」라고 덧붙이고, 「여러분 얘랑 좀 친하게 지내주세요」로 마무리하는, 끝까지 예측 불가능한 자기소개였습니다.<br>
부드러운 인상과의 갭에 주변 멤버들에게서는 「그 외모로?」 「근데 좀 궁금한데」 「궁금하다, 얘기 더 듣고 싶어」라는 반응이 터져 나왔고, 결과적으로 RYOGA는 「가장 친구가 되고 싶은 신입생」 투표에서 여러 표를 얻게 되었습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">수수께끼 포즈의 정체는? NARUTO・진격의 거인・드래곤볼설을 짚어보다</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>화제 포인트:</strong>SNS에서는 RYOGA가 보여준 포즈의 원조를 두고 「NARUTO의 카쿠레의 술」 「진격의 거인의 거인화」 「드래곤볼의 원기옥」이라는 세 가지 설이 오가며 의견이 갈리고 있다</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>방송 직후부터 SNS에서는 그 포즈가 대체 어떤 패러디인지를 두고 추측이 이어졌습니다.<br>
심지어 「자기소개하는 료가, 거인화니 카쿠레의 술이니 원기옥이니 다들 말이 달라서 안 통해서 직접 찾아봤다」며 여러 설이 동시에 오가 정리가 안 되는 상황을 전하는 팬도 있었을 정도입니다.<br>
후보에 오른 세 작품을 정리하면 다음과 같습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0 0 8px 0;font-weight:bold;">포즈의 원조 후보</p>
<ul style="margin:0;padding-left:1.3em;">
<li><strong>NARUTO 「카쿠레의 술」설</strong> — 양손으로 손인을 맺은 뒤 기술을 발동하는 닌자 장면. 「새 반이 되면 자기소개로 카쿠레의 술 하는 타입이구나」라는 팬 게시글도 있었고, 가장 많이 나온 설</li>
<li><strong>진격의 거인 「거인화」설</strong> — 주인공이 각성해 거인으로 변신할 때의, 팔을 치켜올리는 듯한 격렬한 동작을 떠올린 설</li>
<li><strong>드래곤볼 「원기옥」설</strong> — 양손을 들어 에너지를 모으는, 필살기를 쏘기 전의 충전 동작을 떠올린 설</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>셋 다 소년만화・애니 중에서도 손꼽히는 인기 작품이고, 하나같이 「양손을 쓰는 큰 동작」이라는 공통점이 있어서, 영상의 한 장면만으로 하나로 단정 짓기는 솔직히 꽤 어렵습니다.<br>
다만 <a href="https://chomoand-1.com/ko/ryoga-iizuka-anime-manga-list-kr" target="_blank" rel="noopener">RYOGA의 만화・애니 취향을 조사한 다른 글</a>에서 밝혀진 정보와 맞춰보면, <strong>NARUTO설이 가장 유력</strong>하다고 볼 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">NARUTO설이 유력해 보이는 이유</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>RYOGA는 멤버・팬과 소통할 수 있는 앱 「KO1KEYZ Chat(프라챠)」에서 예전부터 만화・애니 드립을 자주 날리는 것으로 알려져 있으며, 그중에서도 <strong>「료가가 좋아한다고 확정된 만화는 NARUTO・呪術廻戦(주술회전)・ONE PIECE」</strong>라고 소개될 만큼 NARUTO에 대한 애정은 이미 확실합니다.<br>
2026년 9월 8일 프라챠에서는 「질풍전까지는 어떻게든 힘내서 봐줘」 「질풍전부터는 이제 못 멈춘다」며 NARUTO에 대해 장문으로 열변을 토하고, 앞으로 볼 팬들에게 시청 지속을 위한 조언까지 남겼을 정도였습니다.<br>
반면 이번에 후보로 오른 진격의 거인이나 드래곤볼에 대해서는, 지금까지 조사에서 「좋아한다」는 발언이나 작품 목록 등재가 확인되지 않았습니다.<br>
이렇게 평소에도 NARUTO 이야기를 자주 하는 RYOGA가, 자기소개라는 주목받는 자리에서 NARUTO의 필살기풍 포즈를 골랐다고 생각하는 것은 결코 부자연스럽지 않을 것입니다.<br>
물론 본인의 공식 코멘트가 있는 것은 아니므로 단정할 수는 없지만, 「카쿠레의 술」설은 RYOGA의 캐릭터와 가장 모순 없는 추측이라고 할 수 있을 것 같습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">사실 RYOGA는 「자기소개 장인」? 과거에도 수많은 전설이</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>화제 포인트:</strong>RYOGA의 개성 넘치는 자기소개는 이번이 처음이 아니라, 『PRODUCE 101 JAPAN 신세계』 시절부터 여러 차례 화제가 됐었다</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>이번 자기소개가 「역시 료가답다」고 느낀 팬이 많았던 데는 이유가 있습니다.<br>
RYOGA는 오디션 프로그램 『PRODUCE 101 JAPAN 신세계』 시절부터 인상적인 자기소개를 여러 번 선보였던 「자기소개 장인」이었습니다.<br>
예를 들어 101초 자기소개 릴레이 기획에서는 「군마현 출신 료가입니다, 15년간 축구를 해왔다」며, 이번과 같은 소재인 군마현 출신・축구 경력 15년을 이미 선보인 바 있습니다.<br>
또 다른 자기소개에서는 「왜인지 발지압 매트 위에서 줄넘기를 한다」는, 맥락 없음이 오히려 화제가 된 적도 있습니다.<br>
억양을 억누른 독특한 말투도 당시부터 「중독성 있다」고 팬들 사이에서 평이 좋았고, 꾸미지 않은 천연 캐릭터는 지금이나 그때나 변함이 없는 듯합니다.<br>
즉 이번 NARUTO(?) 포즈가 들어간 자기소개는, 이런 「예측 불가능한 자기소개」 계보를 잇는, 말하자면 집대성 같은 순간이었다고 할 수 있을 것 같습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">SNS 팬들의 반응</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>방송 직후 SNS는 RYOGA의 자기소개 감상으로 크게 달아올랐습니다.<br>
「자기소개만으로 슈퍼 료가 타임을 만들어낸다」 「음악이 계속 멈춰서 배 아프다」 「R-1 그랑프리급으로 잘 짜여 있다」 등 완성도를 칭찬하는 목소리가 많이 보입니다.<br>
한편 「4차원 감성 미쳤다」 「독특해서 개인 방송을 보고 싶어진다」처럼, RYOGA다운 마이페이스한 캐릭터를 재밌어하는 목소리도 눈에 띄었습니다.<br>
축구 킥 동작에 대해서도 「말도 안 되는 애니・만화 동작보다 축구 차는 모션이 훨씬 진심이라 대박」이라며, 디테일까지 신경 쓴 연기를 평가하는 댓글이 올라오고 있습니다.<br>
「집돌이 생활도 정말 좋아합니다」라는 대목에는 「그런 걸 스스로 말하는 사람 없다」며 웃음소리도 나왔고, 외모와의 갭까지 포함해 종합적으로 사랑받는 자기소개가 된 듯합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">정리</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>「KO1!KO1!KO1KEYZ」 첫 회 「큥투군 학원」에서 RYOGA의 자기소개가 큰 화제가 됨</p>
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>축구 킥 동작 → 수수께끼 포즈 → 진지한 얼굴로 「애니와 만화를 정말 좋아함」이라는, 완급이 있는 1분간 자기소개</p>
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>수수께끼 포즈는 NARUTO 「카쿠레의 술」・진격의 거인 「거인화」・드래곤볼 「원기옥」 세 가지 설이 등장</p>
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>RYOGA 본인이 이미 좋아한다고 확정된 만화에 NARUTO가 포함돼 있어 카쿠레의 술설이 가장 유력</p>
<p style="margin:0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>오디션 시절부터 개성 넘치는 자기소개로 유명한 「자기소개 장인」으로, 이번은 그 집대성 같은 순간이었음</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>1분이라는 짧은 시간에 축구・애니・외모와의 갭까지 눌러 담아 보여준 RYOGA의 자기소개.<br>
수수께끼 포즈의 진상은 아직 본인 입으로 밝혀지지 않았지만, 「KO1!KO1!KO1KEYZ」는 매주 목요일 업데이트되는 프로그램이니 후속 소식이나 본인의 설명이 나오면 다시 전해드리겠습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">RYOGA(이이즈카 료가) 관련 글</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-1.com/ko/ryoga-iizuka-anime-manga-list-kr" target="_blank" rel="noopener">RYOGA의 만화・애니 취향과 정주행 완료 작품 목록을 조사한 글</a></li>
<li><a href="https://chomoand-1.com/ko/iidukaryouga_wiki-kr" target="_blank" rel="noopener">노래・댄스 미경험으로 일프 신세계에 도전한 위키식 이력 글</a></li>
<li><a href="https://chomoand-1.com/ko/ryoga-mark-gonzales-longtee-kr" target="_blank" rel="noopener">한국 브이로그에서 입었던 사복 롱슬리브 티를 특정한 글</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

KR_SUMMARY = ("KO1KEYZ의 새 프로그램 「KO1!KO1!KO1KEYZ」에서 RYOGA(이이즈카 료가)가 보여준 자기소개 수수께끼 포즈가 화제. "
              "NARUTO의 카쿠레의 술? 진격의 거인? 드래곤볼? SNS에서 갈린 추측과 유력설의 근거를 정리했습니다.")

# ---------------- ENGLISH ----------------
EN_TITLE = "Was RYOGA's Self-Intro a NARUTO Jutsu? Fans Buzzing Over the Mystery Pose"
EN_SLUG = "ryoga-jikoshoukai-naruto-kuchiyose-en"

en_kick = fetch_media_img_html(KICK_MEDIA, "RYOGA (Ryoga Iizuka) re-enacting a soccer kick during his self-introduction",
    f'Source: {VIDEO_LABEL_EN}')
en_pose = fetch_media_img_html(POSE_MEDIA, "RYOGA (Ryoga Iizuka) striking a mysterious pose with both arms during his self-introduction",
    f'Source: {VIDEO_LABEL_EN}')
en_reveal = fetch_media_img_html(REVEAL_MEDIA, 'RYOGA (Ryoga Iizuka) deadpan, saying "I love anime and manga" right after the dramatic pose',
    f'Source: {VIDEO_LABEL_EN}')

EN_CONTENT = f"""<!-- wp:paragraph -->
<p>RYOGA (Ryoga Iizuka) of KO1KEYZ has fans buzzing after his self-introduction segment in the very first episode of the new show "KO1! KO1! KO1KEYZ."<br>
The music suddenly cut out, and he launched into a soccer kicking motion followed by a mysterious two-armed pose, before flatly declaring "I love anime and manga" — cramming an almost overwhelming amount of content into a single one-minute self-intro.<br>
Online, fans can't agree on what that pose was referencing: "Naruto's Summoning Jutsu," "Attack on Titan's Titan transformation," and "Dragon Ball's Spirit Bomb" have all been floated, and the truth is still unconfirmed.<br>
This article walks through what actually happened during RYOGA's self-introduction and digs into which anime the pose was really referencing.</p>
<!-- /wp:paragraph -->

{PROFILE_IMG_HTML}

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AL};color:#fff;">What this article covers</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>What the first episode of "KO1! KO1! KO1KEYZ" is about</li>
<li>What actually happened during RYOGA's self-introduction</li>
<li>The candidates for the mystery pose (NARUTO, Attack on Titan, Dragon Ball)</li>
<li>Why the NARUTO theory looks the strongest</li>
<li>RYOGA's history as a "self-introduction master" even before debut</li>
<li>How fans reacted online</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What is "KO1!KO1!KO1KEYZ" episode 1 about?</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>Show:</strong> KO1! KO1! KO1KEYZ, Episode 1, "Kyuntugun Academy - New Student Audition"</p>
<p style="margin:4px 0 0 0;"><strong>Streaming:</strong> Free on the KO1KEYZ official YouTube channel, from Thursday, September 17, 2026, 21:00 JST, updating every Thursday</p>
<p style="margin:4px 0 0 0;"><strong>Format:</strong> All 12 members play new transfer students at "Kyuntugun Academy." Each gets one minute to introduce themselves, then everyone votes for the one member they'd most like to be friends with</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>"KO1! KO1! KO1KEYZ" is a new show that began free streaming on the KO1KEYZ official YouTube channel from 21:00 JST on Thursday, September 17, 2026.<br>
The debut episode is a school-comedy sketch titled "Kyuntugun Academy - New Student Audition," in which all 12 members play new students who have just transferred into the same class.<br>
The rule: each member gets one minute to introduce themselves, and once everyone has gone, they each cast a vote for the person they'd most like to become friends with.<br>
Whoever gets the most votes is crowned "the new student everyone wants to be friends with," which pushed every member to make the most of their one minute to show off their personality.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What happened during RYOGA's self-introduction?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Among all twelve self-introductions, RYOGA's drew by far the biggest reaction online.<br>
He opened with "I'm Ryoga Iizuka, from Gunma Prefecture," which prompted another Gunma-native member to say he'd like to get to know him, and when asked "How did you get here?" RYOGA deadpanned "Just by train" — a fairly ordinary, friendly start.<br>
From there, though, things escalated fast.</p>
<!-- /wp:paragraph -->

{en_kick}

<!-- wp:paragraph -->
<p>First came a genuinely committed soccer-kicking motion, timed to the line "I played soccer for 15 years, so I have some confidence in athletics."<br>
It was a very RYOGA touch — he was a dedicated soccer player throughout middle and high school — to back up his words with his whole body. But this was only the opening act.</p>
<!-- /wp:paragraph -->

{en_pose}

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>The moment everyone's talking about:</strong> right after the kick, RYOGA broke into a mysterious two-armed pose that left the other "classmates" completely baffled, prompting them to blurt out "What was that? What was that?"</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>The music paused for a beat before he unleashed the pose, and the other members were so thrown off that they said "What was that? What was that?" almost in unison.<br>
Then, with a calm and completely serious face that seemed impossible right after all that movement, he delivered the line: <strong>"I love anime and manga."</strong></p>
<!-- /wp:paragraph -->

{en_reveal}

<!-- wp:paragraph -->
<p>He kept going, adding "and despite how I look, I also love staying home," before wrapping up with "everyone, please be friends with this guy" — an unpredictable self-introduction right to the very end.<br>
The gap between his soft-spoken appearance and this unexpected reveal drew reactions like "Wait, with that face?" and "Now I'm kind of curious about him, I want to hear more" from the other members, and RYOGA ended up picking up multiple votes in the "who do you want to be friends with" poll as a result.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What was the mystery pose? NARUTO vs. Attack on Titan vs. Dragon Ball</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>The debate:</strong> fans online are split over what RYOGA's pose referenced, with three main theories in circulation: NARUTO's Summoning Jutsu, Attack on Titan's Titan transformation, and Dragon Ball's Spirit Bomb</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>As soon as the episode aired, fans online started debating exactly what the pose was a reference to.<br>
One fan even wrote that they'd seen RYOGA's introduction described as everything from "Titan transformation" to "Summoning Jutsu" to "Spirit Bomb," with no consensus, and had to go look into it themselves.<br>
Here's how the three candidates break down:</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0 0 8px 0;font-weight:bold;">Candidates for the pose's origin</p>
<ul style="margin:0;padding-left:1.3em;">
<li><strong>NARUTO's "Summoning Jutsu"</strong> — the classic ninja move where hand seals are formed with both hands before unleashing a technique. Some fans directly guessed this, calling RYOGA "the type to do a Summoning Jutsu during a self-intro at a new school." This was the most commonly cited theory</li>
<li><strong>Attack on Titan's "Titan transformation"</strong> — the intense arm-raising motion the protagonist makes when awakening and transforming into a Titan</li>
<li><strong>Dragon Ball's "Spirit Bomb"</strong> — the charge-up motion of raising both hands to gather energy before unleashing a signature move</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>All three are hugely popular shonen manga and anime, and all three involve a big two-handed gesture, so it's genuinely hard to pin down just from a single clip.<br>
That said, cross-referencing this with <a href="https://chomoand-1.com/en/ryoga-iizuka-anime-manga-list-en" target="_blank" rel="noopener">our earlier article investigating RYOGA's love of manga and anime</a>, <strong>the NARUTO theory looks like the strongest bet</strong>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why NARUTO is the most likely answer</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>RYOGA is known for frequently dropping manga and anime references on "KO1KEYZ Chat," the app that lets fans get real-time posts from members, and he's specifically been reported to have confirmed loving <strong>NARUTO, Jujutsu Kaisen, and ONE PIECE</strong>.<br>
On September 8, 2026, he even wrote a long post on KO1KEYZ Chat passionately urging fans to "please push through to [NARUTO] Shippuden" and that "once you hit Shippuden, there's no stopping," going out of his way to encourage new viewers to stick with the series.<br>
By contrast, nothing in our research so far has turned up any comment from RYOGA expressing love for Attack on Titan or Dragon Ball, nor have they appeared on any list of his favorites.<br>
Given how often he already talks about NARUTO, it wouldn't be at all surprising for him to choose a NARUTO-style finishing-move pose for a moment as attention-grabbing as a self-introduction.<br>
Of course, without an official comment from RYOGA himself, nothing can be confirmed for certain — but the "Summoning Jutsu" theory fits everything we already know about him remarkably well.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">RYOGA has actually always been a "self-introduction master"</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>Good to know:</strong> this isn't the first time RYOGA's self-introductions have gone viral — he was already known for them back during his "PRODUCE 101 JAPAN THE NEW WORLD" survival-show days</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Part of why this felt so "on brand" for RYOGA is that he's been building this reputation for a while.<br>
Back on "PRODUCE 101 JAPAN THE NEW WORLD," he already had a track record of memorable, unpredictable self-introductions.<br>
In a 101-second self-introduction relay segment, for instance, he introduced himself with "I'm Ryoga from Gunma, I've played soccer for 15 years" — the exact same Gunma-and-soccer combo he used again in this new episode.<br>
In another self-intro, he was recorded doing an out-of-nowhere jump rope routine while standing on an acupressure mat, with the sheer randomness of it becoming a talking point on its own.<br>
Even his flat, understated delivery was already earning him "weirdly addictive" comments from fans back then, so his unfiltered, natural personality hasn't changed a bit.<br>
In other words, this NARUTO(?)-posed self-introduction feels like the culmination of a long line of "you never know what he's going to do next" self-intros.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How fans reacted online</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Right after the episode aired, social media lit up with reactions to RYOGA's self-introduction.<br>
Plenty of fans praised how well put-together it was, with comments like "he can create an entire Super RYOGA Time out of a self-intro alone," "the music kept stopping and it hurts to laugh," and "this is as tightly crafted as a comedy competition act."<br>
Others simply enjoyed how RYOGA being RYOGA came through, with comments like "he's operating on a completely different wavelength and I love it" and "he's so unique I want to watch a solo stream of him now."<br>
His soccer kick also got specific praise, with one fan noting that "the soccer kicking motion was way more committed and realistic than the wild anime pose."<br>
His "I love staying home" line got laughs too — "nobody just volunteers that information" — and between the gap with his looks and the sheer commitment to the bit, the whole self-introduction ended up being widely loved.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Summary</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>RYOGA's self-introduction in "KO1!KO1!KO1KEYZ" episode 1, "Kyuntugun Academy," became a huge talking point</p>
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>His one minute went: soccer kick → mystery pose → a deadpan "I love anime and manga"</p>
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>Three theories emerged for the pose: NARUTO's Summoning Jutsu, Attack on Titan's Titan transformation, and Dragon Ball's Spirit Bomb</p>
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>Since NARUTO is already a confirmed favorite of RYOGA's, the Summoning Jutsu theory looks the most likely</p>
<p style="margin:0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>RYOGA has a track record as a "self-introduction master" going back to his survival-show days, and this felt like the culmination of that streak</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>In just one minute, RYOGA managed to pack in soccer, anime, and a gap-moe reveal all at once.<br>
The truth behind the mystery pose hasn't been confirmed by RYOGA himself yet, but since "KO1!KO1!KO1KEYZ" updates every Thursday, we'll update this article if there's any follow-up or an explanation from the man himself.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">Related articles on RYOGA (Ryoga Iizuka)</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-1.com/en/ryoga-iizuka-anime-manga-list-en" target="_blank" rel="noopener">The article researching RYOGA's love of manga and anime and the titles he's finished</a></li>
<li><a href="https://chomoand-1.com/en/iidukaryouga_wiki-en" target="_blank" rel="noopener">The wiki-style career article on his debut run with no singing or dancing experience</a></li>
<li><a href="https://chomoand-1.com/en/ryoga-mark-gonzales-longtee-en" target="_blank" rel="noopener">The article identifying the long-sleeve tee he wore in the Korea vlog</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

EN_SUMMARY = ("KO1KEYZ's RYOGA (Ryoga Iizuka) had fans buzzing with a mystery pose during his self-introduction on the new show \"KO1!KO1!KO1KEYZ.\" "
              "NARUTO's Summoning Jutsu? Attack on Titan? Dragon Ball? Here's a look at the theories and why one stands out.")


def post_draft(title, content, slug, lang, cats, summary):
    payload = {
        "title": title, "content": content, "slug": slug, "status": "draft",
        "categories": cats, "author": 2,
        "lang": lang, "translations": {"ja": JA_ID},
        "meta": {"jetpack_publicize_message": summary},
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=H, data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    p = r.json()
    plain = len(re.sub(r"<!--.*?-->|<[^>]+>", "", content, flags=re.S))
    print(f"[{lang}] id={p['id']} slug={p['slug']} link={p['link']} chars={plain}")
    return p


kr = post_draft(KR_TITLE, KR_CONTENT, KR_SLUG, "ko", [74], KR_SUMMARY)

KR_EYE = ROOT / "images" / "ryoga_jikoshoukai_naruto_eyecatch_kr.png"
subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
    "--top", "RYOGA의 자기소개가 설마 카쿠레의 술?",
    "--main", "KO1KEYZ",
    "--bottom", "NARUTO 드립에 다들 뒤집어졌다!",
    "--out", str(KR_EYE), "--seed", str(kr["id"]), "--lang", "kr"], check=True)
mr = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers={
    "Authorization": f"Basic {AUTH}", "Content-Type": "image/png",
    "Content-Disposition": 'attachment; filename="ryoga_jikoshoukai_naruto_eyecatch_kr.png"',
}, data=KR_EYE.read_bytes())
mr.raise_for_status()
kr_media = mr.json()["id"]
requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{kr['id']}", headers=H,
              data=json.dumps({"featured_media": kr_media}).encode("utf-8")).raise_for_status()
print("KR eyecatch media", kr_media)

en = post_draft(EN_TITLE, EN_CONTENT, EN_SLUG, "en", [110], EN_SUMMARY)
requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{en['id']}", headers=H,
              data=json.dumps({"featured_media": JP_EYECATCH_MEDIA}).encode("utf-8")).raise_for_status()
print("EN eyecatch media", JP_EYECATCH_MEDIA, "(shared with JP)")

(ROOT / "tmp_ryoga_jikoshoukai_kren_ids.txt").write_text(
    f"kr={kr['id']} kr_slug={kr['slug']} kr_media={kr_media}\nen={en['id']} en_slug={en['slug']}\n", encoding="utf-8")
print("DONE")
