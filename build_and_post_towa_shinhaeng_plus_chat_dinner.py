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

SOURCE_TWEET = "https://x.com/girlyoshiki/status/2095169972456525922"
IMG_SHOT = ROOT / "images" / "towa_shinhaeng_dinner_source.jpg"

G_BORDER = "#9bc96e"
G_BG = "#f5faec"

# related (published) permalinks
L_PRACHA = "https://chomoand-1.com/what-is-ko1keyz-pracha-how-to-11497"
L_JAGAIMO = "https://chomoand-1.com/is-towas-new-character-jagaimo-11691"
L_GIVENCHY = "https://chomoand-1.com/towa-givenchy-tshirt-siyoung-dance-11855"
L_LOUNGE = "https://chomoand-1.com/what-brand-is-towas-loungewear-11093"
L_WIKI = "https://chomoand-1.com/hamadatowa_wiki-2452"
L_PROFILE12 = "https://chomoand-1.com/profile-12-9725"
# CELINE outfit article — still a draft at build time (JP post 12125); permalink once published:
L_CELINE = "https://chomoand-1.com/towa-private-celine-cap-tshirt-12125"


def upload_media_from_file(path: Path, filename: str, alt: str, content_type: str = "image/jpeg"):
    data = path.read_bytes()
    headers = {
        **HEADERS_AUTH,
        "Content-Type": content_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=data)
    r.raise_for_status()
    media = r.json()
    r2 = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media/{media['id']}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps({"alt_text": alt, "title": alt}).encode("utf-8"),
    )
    r2.raise_for_status()
    return media


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
    return f'''<!-- wp:html -->
<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>
</figure>
<!-- /wp:html -->'''


def post_draft(title, content, slug, lang, categories, featured_media, summary, translations=None):
    payload = {
        "title": title, "content": content, "slug": slug, "status": "draft",
        "lang": lang, "categories": categories, "featured_media": featured_media,
        "author": 2, "meta": {"jetpack_publicize_message": summary},
    }
    if translations:
        payload["translations"] = translations
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts",
                      headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    return r.json()


def make_eyecatch(args, out_path):
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"), *args, "--out", str(out_path)], check=True)
    mr = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                       headers={**HEADERS_AUTH, "Content-Type": "image/png",
                                "Content-Disposition": f'attachment; filename="{out_path.name}"'},
                       data=out_path.read_bytes())
    mr.raise_for_status()
    return mr.json()["id"]


print("uploading 2-shot image...")
shot_media = upload_media_from_file(
    IMG_SHOT, "towa_shinhaeng_plus_chat_dinner.jpg",
    "プラチャで公開されたTOWAとSHINHAENGの2ショット",
)
print("shot", shot_media["id"])

CAP_JP = f'出典:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>'
CAP_KR = f'출처:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>'
CAP_EN = f'Source:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>'


# ============================== JP ==============================
img_jp = build_img_html(shot_media, "プラチャで公開されたTOWAとSHINHAENGの2ショット", CAP_JP)

JP_TITLE = "TOWAがプラチャで明かしたごはん相手はSHINHAENG！"
JP_SLUG = "towa-shinhaeng-plus-chat-dinner"

JP_CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZのTOWA(濱田永遠)さんが、2026年9月2日にプラスメッセージ(通称プラチャ)で「今からごはん」と発信し、誰と食べるのかをファンに当てさせるクイズを出しました。<br>
出したヒントは「子犬」。<br>
その正体は、<strong><span class="swl-marker mark_green">同じKO1KEYZのSHINHAENG(オ・シンヘン)さん</span></strong>で、あわせて2人の食事中の2ショットも公開されました。<br>
「子犬」というヒントは、SHINHAENGさんのコンセプトキーワード「おバカなワンちゃん」にちなんだものとみられます。<br>
この記事では、プラチャでのやりとりの流れ、「子犬」ヒントの意味、そして2人の仲の良さについてまとめます。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li>プラチャでのやりとりの流れ(「ヒントは子犬」→SHINHAENG発表)</li>
<li>「子犬」ヒントの意味(SHINHAENGの公式キーワード)</li>
<li>TOWAとSHINHAENGの仲の良さ</li>
<li>2ショットでTOWAが着ている私服について</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">プラチャで何があった?「ヒントは子犬」からのSHINHAENG発表</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>日付:</strong>2026年9月2日</p>
<p style="margin:4px 0 0 0;"><strong>発信元:</strong>TOWAのプラスメッセージ(プラチャ)</p>
<p style="margin:4px 0 0 0;"><strong>内容:</strong>夕食のクイズ→「ヒントは子犬」→SHINHAENGと2ショットを公開</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>この日、TOWAさんはプラチャで「今からごはん」と切り出し、ハンバーガーの絵文字を送りました。<br>
続けて「誰と食べるでしょう?」とファンに問いかけ、ヒントとして「子犬」という一言だけを残します。<br>
ファンからの反応を受けて「ヒントというより答えだったかも」と付け足したあと、最後に「SHINHAENGです」と種明かしをし、2人で写った写真も送られてきました。<br>
プラチャは、メンバーが1対1のトーク画面のような形でメッセージや写真を届けてくれる有料サービスで、こうした日常のワンシーンが本人の言葉で流れてくるのが魅力です(仕組みは<a href="{L_PRACHA}" target="_blank" rel="noopener">プラチャの料金・使い方をまとめた記事</a>で解説しています)。</p>
<!-- /wp:paragraph -->

{img_jp}

<!-- wp:paragraph -->
<p>公開された写真は勢いのあるブレた1枚で、グリーンのキャップをかぶったTOWAさんが指ハートを作り、隣で黒いキャップに黒TシャツのSHINHAENGさんが笑顔を見せています。<br>
店内の様子から、ふたりでゆっくり食事を楽しんでいた場面だとうかがえます。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">「子犬」ヒントの意味は?SHINHAENGの「おバカなワンちゃん」</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>本名:</strong>オ・シンヘン(呉信行)</p>
<p style="margin:4px 0 0 0;"><strong>生年月日:</strong>2004年5月3日</p>
<p style="margin:4px 0 0 0;"><strong>出身:</strong>韓国・木浦(モクポ)</p>
<p style="margin:4px 0 0 0;"><strong>『PRODUCE 101 JAPAN 新世界』最終順位:</strong>4位</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>ヒントの「子犬」は、SHINHAENGさん本人のキャラクターを指しています。<br>
SHINHAENGさんは番組時代から自身を「おバカなワンちゃん」と表現しており、天然な発言やくるくる変わる表情、いつもにこにこした笑顔でグループのムードメーカー的な立ち位置にいます。<br>
ファンの間でも「子犬っぽい」「わんこみたい」と言われることが多く、TOWAさんがヒントに人の名前ではなく「子犬」を選んだのは、名前を伏せつつも分かる人には一発で分かる、絶妙な出し方だったと言えます。<br>
なお、SHINHAENGさんの経歴や人柄は<a href="{L_PROFILE12}" target="_blank" rel="noopener">KO1KEYZ12人のプロフィール記事</a>でもまとめています。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">TOWAとSHINHAENGの仲は?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>TOWAさんとSHINHAENGさんは、以前からファンの間で仲の良いコンビとして知られています。<br>
2026年8月には、TOWAさんがSHINHAENGさんの靴の側面にオリジナルキャラクター「じゃがいもっぷりん」をこっそり描き足していたことが見つかり、大きな話題になりました(詳しくは<a href="{L_JAGAIMO}" target="_blank" rel="noopener">「じゃがいもっぷりん」を紹介した記事</a>へ)。<br>
SHINHAENGさんを表す絵文字がじゃがいも(🥔)であることや、2人でおそろいのアクセサリーをつけていたという指摘もあり、日頃から距離の近い間柄がうかがえます。<br>
今回のように仕事の合間にプライベートで一緒に食事へ行く様子がプラチャで共有されたことで、その仲の良さがあらためて伝わってきました。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">2ショットのTOWAの私服はCELINEのコーデ</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>今回の2ショットでTOWAさんが身につけているのは、グリーンのキャップと、赤いハートに「CELINE PARIS」の文字が入ったタイダイ柄のTシャツです。<br>
これはどちらも「CELINE(セリーヌ)」のアイテムで、キャップが「トリオンフ リシュリュー キャップ」(参考価格 約86,900円)、Tシャツがエディ・スリマン期のタイダイTシャツで、参考価格は約154,000円とみられます。<br>
プライベートの食事にこのコーデで出かけていることから、ステージ衣装ではなくTOWAさん自身の私服として愛用しているアイテムだと考えられます。<br>
2着の詳細は<a href="{L_CELINE}" target="_blank" rel="noopener">TOWAの私服CELINEコーデをまとめた記事</a>で解説しています。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">まとめ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>2026年9月2日、TOWAがプラチャで「今からごはん」→「ヒントは子犬」とクイズを出題</li>
<li>答えは<strong>SHINHAENG(オ・シンヘン)</strong>で、2人の食事中の2ショットも公開</li>
<li>「子犬」はSHINHAENGのコンセプトキーワード「おバカなワンちゃん」にちなんだヒント</li>
<li>2人はじゃがいもっぷりんの落書きなどで知られる仲良しコンビ</li>
<li>2ショットのTOWAの私服は、キャップもTシャツもCELINE</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>クイズ形式で焦らしてから種明かしをするあたりに、ファンとのやりとりを楽しんでいるTOWAさんらしさが出ています。<br>
プラチャに登録していると、こうしたメンバー同士のプライベートな時間がふとした形で届くので、2人の関係をこれから追いかけたくなった方はチェックしてみてくださいね!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">TOWA(濱田永遠)さんの関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_CELINE}" target="_blank" rel="noopener">この2ショットの私服(CELINEのキャップとTシャツ)をまとめた記事</a></li>
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">SHINHAENGの靴に描いた新キャラ「じゃがいもっぷりん」を紹介した記事</a></li>
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">SIYOUNGとのダンス動画で着ていたGIVENCHY「4G」Tシャツを特定した記事</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">ナイトルーティンで着ていたルームウェアのブランドを特定した記事</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">TOWA(濱田永遠)のwiki風プロフィール・経歴をまとめた記事</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

JP_SUMMARY = "KO1KEYZ・TOWAがプラチャで「今からごはん」「ヒントは子犬」とクイズを出題。答えはSHINHAENG(オ・シンヘン)で、2ショットも公開されました。「子犬」はSHINHAENGの公式キーワード「おバカなワンちゃん」にちなんだヒントです。"

JP_EYECATCH_ID = make_eyecatch(
    ["--top", "TOWAのごはん相手は誰？", "--main", "KO1KEYZ", "--bottom", "SHINHAENGと判明！ヒントは子犬"],
    ROOT / "images" / "towa_shinhaeng_plus_chat_dinner_eyecatch.png",
)
print("JP_EYECATCH_ID", JP_EYECATCH_ID)

jp_post = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, "ja", [66, 63, 104], JP_EYECATCH_ID, JP_SUMMARY)
JP_POST_ID = jp_post["id"]
print("JP_POST_ID", JP_POST_ID, jp_post["slug"], jp_post.get("link"))


# ============================== KR ==============================
img_kr = build_img_html(shot_media, "플러스챗에 공개된 TOWA와 SHINHAENG의 투샷", CAP_KR)

KR_TITLE = "TOWA가 플러스챗에서 밝힌 식사 상대는 SHINHAENG!"
KR_SLUG = f"{JP_SLUG}-kr"

KR_CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZ의 TOWA(하마다 토와)가 2026년 9월 2일 플러스 메시지(통칭 플러스챗)에서 '지금부터 밥'이라고 알리며, 누구와 먹는지 팬들에게 맞혀 보라는 퀴즈를 냈습니다.<br>
낸 힌트는 '강아지'.<br>
그 정체는 <strong><span class="swl-marker mark_green">같은 KO1KEYZ의 SHINHAENG(오신행)</span></strong>이었고, 두 사람이 식사 중에 찍은 투샷도 함께 공개됐습니다.<br>
'강아지'라는 힌트는 SHINHAENG의 콘셉트 키워드 '멍청한 강아지(おバカなワンちゃん)'에서 따온 것으로 보입니다.<br>
이 글에서는 플러스챗에서의 대화 흐름, '강아지' 힌트의 의미, 그리고 두 사람의 사이에 대해 정리합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">이 글에서 알 수 있는 것</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li>플러스챗에서의 대화 흐름('힌트는 강아지' → SHINHAENG 발표)</li>
<li>'강아지' 힌트의 의미(SHINHAENG의 공식 키워드)</li>
<li>TOWA와 SHINHAENG의 사이</li>
<li>투샷에서 TOWA가 입은 사복</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">플러스챗에서 무슨 일이? '힌트는 강아지'에서 SHINHAENG 발표까지</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>날짜:</strong>2026년 9월 2일</p>
<p style="margin:4px 0 0 0;"><strong>발신:</strong>TOWA의 플러스 메시지(플러스챗)</p>
<p style="margin:4px 0 0 0;"><strong>내용:</strong>저녁 식사 퀴즈 → '힌트는 강아지' → SHINHAENG과 투샷 공개</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>이날 TOWA는 플러스챗에서 '지금부터 밥'이라고 운을 떼며 햄버거 이모지를 보냈습니다.<br>
이어 '누구와 먹을까요?'라고 팬들에게 물으며, 힌트로 '강아지'라는 한마디만 남깁니다.<br>
팬들의 반응을 받고 '힌트라기보다 답이었을지도'라고 덧붙인 뒤, 마지막에 'SHINHAENG입니다'라고 정답을 공개하고 두 사람이 함께 찍은 사진도 보냈습니다.<br>
플러스챗은 멤버가 1대1 대화창 같은 형태로 메시지와 사진을 보내 주는 유료 서비스로, 이런 일상의 한 장면이 본인의 말로 전해지는 것이 매력입니다(구조는 <a href="{L_PRACHA}" target="_blank" rel="noopener">플러스챗 요금・사용법을 정리한 글</a>에서 설명합니다).</p>
<!-- /wp:paragraph -->

{img_kr}

<!-- wp:paragraph -->
<p>공개된 사진은 흔들린 역동적인 한 장으로, 그린 캡을 쓴 TOWA가 손하트를 만들고, 옆에서 검은 캡에 검은 티셔츠를 입은 SHINHAENG이 미소를 짓고 있습니다.<br>
가게 안 분위기로 보아 둘이서 느긋하게 식사를 즐기던 장면으로 보입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">'강아지' 힌트의 의미는? SHINHAENG의 '멍청한 강아지'</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>본명:</strong>오신행(呉信行)</p>
<p style="margin:4px 0 0 0;"><strong>생년월일:</strong>2004년 5월 3일</p>
<p style="margin:4px 0 0 0;"><strong>출신:</strong>한국 목포</p>
<p style="margin:4px 0 0 0;"><strong>『PRODUCE 101 JAPAN 신세계』 최종 순위:</strong>4위</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>힌트인 '강아지'는 SHINHAENG 본인의 캐릭터를 가리킵니다.<br>
SHINHAENG은 방송 시절부터 자신을 '멍청한 강아지'라고 표현해 왔고, 엉뚱한 발언과 시시각각 바뀌는 표정, 늘 웃는 얼굴로 그룹의 분위기 메이커 같은 위치에 있습니다.<br>
팬들 사이에서도 '강아지상' '멍뭉미'라는 말을 자주 듣기 때문에, TOWA가 힌트에 사람이 아니라 '강아지'를 고른 것은 이름을 감추면서도 아는 사람은 바로 아는, 절묘한 방식이었다고 할 수 있습니다.<br>
SHINHAENG의 경력과 성격은 <a href="{L_PROFILE12}" target="_blank" rel="noopener">KO1KEYZ 12인 프로필 글</a>에서도 정리했습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">TOWA와 SHINHAENG의 사이는?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>TOWA와 SHINHAENG은 예전부터 팬들 사이에서 사이좋은 콤비로 알려져 있습니다.<br>
2026년 8월에는 TOWA가 SHINHAENG의 신발 옆면에 오리지널 캐릭터 '자가이못푸린'을 몰래 그려 넣은 것이 발견되어 큰 화제가 됐습니다(자세한 내용은 <a href="{L_JAGAIMO}" target="_blank" rel="noopener">'자가이못푸린'을 소개한 글</a>에서).<br>
SHINHAENG을 나타내는 이모지가 감자(🥔)인 점, 둘이 커플 액세서리를 하고 있었다는 지적도 있어, 평소 거리가 가까운 사이임을 알 수 있습니다.<br>
이번처럼 일 사이사이에 사적으로 함께 식사하러 가는 모습이 플러스챗으로 공유되면서, 그 사이의 좋음이 다시 한번 전해졌습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">투샷 속 TOWA의 사복은 CELINE 코디</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>이번 투샷에서 TOWA가 입은 것은 그린 캡과, 빨간 하트에 'CELINE PARIS' 글자가 들어간 타이다이 무늬 티셔츠입니다.<br>
둘 다 'CELINE(셀린느)' 아이템으로, 캡은 '트리옹프 리슐리외 캡'(참고가 약 86,900엔), 티셔츠는 에디 슬리먼 시기의 타이다이 티셔츠로 참고가 약 154,000엔으로 보입니다.<br>
사적인 식사에 이 코디로 나온 것으로 보아, 무대 의상이 아니라 TOWA 본인이 사복으로 애용하는 아이템이라고 볼 수 있습니다.<br>
두 벌의 자세한 내용은 <a href="{L_CELINE}" target="_blank" rel="noopener">TOWA의 사복 CELINE 코디를 정리한 글</a>에서 설명합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">정리</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>2026년 9월 2일, TOWA가 플러스챗에서 '지금부터 밥' → '힌트는 강아지' 퀴즈를 출제</li>
<li>정답은 <strong>SHINHAENG(오신행)</strong>이고, 두 사람의 식사 투샷도 공개</li>
<li>'강아지'는 SHINHAENG의 콘셉트 키워드 '멍청한 강아지'에서 온 힌트</li>
<li>두 사람은 '자가이못푸린' 낙서 등으로 알려진 사이좋은 콤비</li>
<li>투샷 속 TOWA의 사복은 캡도 티셔츠도 CELINE</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>퀴즈 형식으로 애태우다가 정답을 공개하는 데서, 팬과의 소통을 즐기는 TOWA다운 면모가 드러납니다.<br>
플러스챗에 등록해 두면 이런 멤버끼리의 사적인 시간이 문득 전해지니, 두 사람의 관계를 앞으로 따라가 보고 싶어진 분은 확인해 보세요!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">TOWA(하마다 토와) 관련 글</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_CELINE}" target="_blank" rel="noopener">이 투샷의 사복(CELINE 캡과 티셔츠)을 정리한 글</a></li>
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">SHINHAENG의 신발에 그린 새 캐릭터 '자가이못푸린'을 소개한 글</a></li>
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">SIYOUNG과의 댄스 영상에서 입은 GIVENCHY '4G' 티셔츠를 특정한 글</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">나이트 루틴에서 입은 룸웨어 브랜드를 특정한 글</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">TOWA(하마다 토와)의 위키풍 프로필・경력을 정리한 글</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

KR_SUMMARY = "KO1KEYZ TOWA가 플러스챗에서 '지금부터 밥' '힌트는 강아지' 퀴즈를 출제. 정답은 SHINHAENG(오신행)이었고 투샷도 공개됐습니다. '강아지'는 SHINHAENG의 공식 키워드 '멍청한 강아지'에서 온 힌트입니다."

KR_EYECATCH_ID = make_eyecatch(
    ["--top", "TOWA의 식사 상대는 누구?", "--main", "KO1KEYZ", "--bottom", "SHINHAENG! 힌트는 강아지", "--lang", "kr"],
    ROOT / "images" / "towa_shinhaeng_plus_chat_dinner_eyecatch_kr.png",
)
print("KR_EYECATCH_ID", KR_EYECATCH_ID)

kr_post = post_draft(KR_TITLE, KR_CONTENT, KR_SLUG, "ko", [74, 78, 104], KR_EYECATCH_ID, KR_SUMMARY,
                     translations={"ja": JP_POST_ID})
print("KR_POST_ID", kr_post["id"], kr_post["slug"], kr_post.get("link"))


# ============================== EN ==============================
img_en = build_img_html(shot_media, "TOWA and SHINHAENG in the two-shot shared on Plus Chat", CAP_EN)

EN_TITLE = "TOWA's Plus Chat Reveal: He Had Dinner With SHINHAENG"
EN_SLUG = f"{JP_SLUG}-en"

EN_CONTENT = f"""<!-- wp:paragraph -->
<p>On September 2, 2026, KO1KEYZ's TOWA (Towa Hamada) opened his Plus Message (nicknamed "Plus Chat") with "about to have dinner" and turned it into a guessing game about who he was eating with.<br>
The hint he gave was one word: "puppy."<br>
The answer was <strong><span class="swl-marker mark_green">fellow KO1KEYZ member SHINHAENG (Oh Shin-haeng)</span></strong>, and he shared a two-shot of the pair at dinner.<br>
The "puppy" hint points to SHINHAENG's concept keyword, "a goofy puppy."<br>
This article covers how the Plus Chat exchange played out, what the "puppy" hint means, and how close the two members are.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">What this article covers</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li>How the Plus Chat exchange went ("hint: puppy" to the SHINHAENG reveal)</li>
<li>What the "puppy" hint means (SHINHAENG's official keyword)</li>
<li>How close TOWA and SHINHAENG are</li>
<li>The outfit TOWA is wearing in the two-shot</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What happened on Plus Chat: from "hint: puppy" to the SHINHAENG reveal</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>Date:</strong> September 2, 2026</p>
<p style="margin:4px 0 0 0;"><strong>From:</strong> TOWA's Plus Message (Plus Chat)</p>
<p style="margin:4px 0 0 0;"><strong>What happened:</strong> a dinner guessing game, then "hint: puppy," then a two-shot with SHINHAENG</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>TOWA started by messaging "about to have dinner" and a hamburger emoji.<br>
He then asked fans to guess who he was eating with, leaving just the single word "puppy" as a clue.<br>
After some fan reactions he added that it might have been more of an answer than a hint, and finally confirmed "it's SHINHAENG," attaching a photo of the two of them.<br>
Plus Chat is a paid service where members send messages and photos in what looks like a one-on-one chat window, and the appeal is getting these everyday moments in the member's own words (we explain how it works in our <a href="{L_PRACHA}" target="_blank" rel="noopener">guide to Plus Chat's price and how to use it</a>).</p>
<!-- /wp:paragraph -->

{img_en}

<!-- wp:paragraph -->
<p>The photo is a blurry, high-energy shot: TOWA in a green cap making a finger heart, with SHINHAENG next to him in a black cap and black tee, smiling.<br>
The setting suggests the two were taking their time over a meal together.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What the "puppy" hint means: SHINHAENG's "goofy puppy"</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>Real name:</strong> Oh Shin-haeng</p>
<p style="margin:4px 0 0 0;"><strong>Born:</strong> May 3, 2004</p>
<p style="margin:4px 0 0 0;"><strong>From:</strong> Mokpo, South Korea</p>
<p style="margin:4px 0 0 0;"><strong>Final rank on PRODUCE 101 JAPAN The Ideal:</strong> 4th</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>The "puppy" hint refers to SHINHAENG's own character.<br>
Since his audition days he has described himself as "a goofy puppy," and with his off-the-wall comments, ever-changing expressions and constant smile, he sits in the group as a mood-maker.<br>
Fans often call him puppy-like too, so TOWA choosing "puppy" rather than a name was a neat way to keep it hidden while making it obvious to anyone in the know.<br>
You can read more about SHINHAENG's background and personality in our <a href="{L_PROFILE12}" target="_blank" rel="noopener">profiles of all 12 KO1KEYZ members</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How close are TOWA and SHINHAENG?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>TOWA and SHINHAENG have long been known among fans as a close pair.<br>
In August 2026, TOWA was found to have quietly drawn his original character "Jagaimoppurin" on the side of SHINHAENG's shoe, which became a big talking point (see our <a href="{L_JAGAIMO}" target="_blank" rel="noopener">article on "Jagaimoppurin"</a>).<br>
SHINHAENG's emoji is a potato (🥔), and fans have also pointed out the two wearing matching accessories, so they clearly spend a lot of time together.<br>
Sharing a private meal like this between work on Plus Chat only underlined how well the two get along.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">TOWA's outfit in the two-shot is all CELINE</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>In the two-shot, TOWA is wearing a green cap and a tie-dye T-shirt with a red heart and the words "CELINE PARIS."<br>
Both are CELINE: the cap is the Triomphe Richelieu Cap (reference price about 86,900 yen), and the tee is a tie-dye piece from the Hedi Slimane era, with a reference price of about 154,000 yen.<br>
Wearing this to a private dinner suggests these are pieces TOWA actually favors as street clothes, not stage wear.<br>
We break down both pieces in our <a href="{L_CELINE}" target="_blank" rel="noopener">article on TOWA's off-duty CELINE outfit</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Summary</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>On September 2, 2026, TOWA posted a "about to have dinner" / "hint: puppy" guessing game on Plus Chat</li>
<li>The answer was <strong>SHINHAENG (Oh Shin-haeng)</strong>, and a two-shot of the two at dinner was shared</li>
<li>"Puppy" is a nod to SHINHAENG's concept keyword, "a goofy puppy"</li>
<li>The two are a close pair, known for the "Jagaimoppurin" shoe doodle among other things</li>
<li>TOWA's outfit in the two-shot — cap and tee — is all CELINE</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Teasing fans with a quiz before the reveal is very TOWA, someone who clearly enjoys the back-and-forth with fans.<br>
If you're signed up to Plus Chat, moments like this between members turn up out of nowhere, so it's worth a look if you want to keep following these two!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">More on TOWA (Towa Hamada)</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_CELINE}" target="_blank" rel="noopener">A breakdown of the outfit in this two-shot (the CELINE cap and tee)</a></li>
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">The new character "Jagaimoppurin" he drew on SHINHAENG's shoe</a></li>
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">Identifying the GIVENCHY "4G" tee from his dance video with SIYOUNG</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">Identifying the brand of the loungewear from his night routine</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">A wiki-style profile and career rundown for TOWA (Towa Hamada)</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

EN_SUMMARY = "KO1KEYZ's TOWA turned a Plus Chat post into a guessing game - \"about to have dinner,\" \"hint: puppy\" - and the answer was SHINHAENG (Oh Shin-haeng), with a two-shot to prove it. \"Puppy\" nods to SHINHAENG's keyword, \"a goofy puppy.\""

en_post = post_draft(EN_TITLE, EN_CONTENT, EN_SLUG, "en", [110, 114], JP_EYECATCH_ID, EN_SUMMARY,
                     translations={"ja": JP_POST_ID})
print("EN_POST_ID", en_post["id"], en_post["slug"], en_post.get("link"))

print("\n=== DONE ===")
print("JP", JP_POST_ID, f"{WP_URL}/wp-admin/post.php?post={JP_POST_ID}&action=edit")
print("KR", kr_post["id"], f"{WP_URL}/wp-admin/post.php?post={kr_post['id']}&action=edit")
print("EN", en_post["id"], f"{WP_URL}/wp-admin/post.php?post={en_post['id']}&action=edit")
