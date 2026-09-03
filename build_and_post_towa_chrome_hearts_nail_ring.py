# -*- coding: utf-8 -*-
"""Build & post the TOWA Chrome Hearts "Nail Ring CH+ Flat" article (JP/KR/EN) to chomoand-1.com.

Source: @NYAN_TOWORLD post identifying CHROME HEARTS "NAILRING CH PLUS FLAT (SILVER)".
Creates chomoand-1.com drafts (JP + KR + EN) with the KO1KEYZ eyecatch template.
"""
import base64, json, os
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

SOURCE_TWEET = "https://x.com/NYAN_TOWORLD/status/2093217803214155831"
IMG_SELFIE = ROOT / "images" / "ko1keyz_towa_chrome_hearts_nail_ring_selfie.jpg"
IMG_PRODUCT = ROOT / "images" / "ko1keyz_towa_chrome_hearts_nail_ring_product.jpg"
EYECATCH_JP = ROOT / "images" / "ko1keyz_towa_chrome_hearts_nail_ring_eyecatch.png"
EYECATCH_KR = ROOT / "images" / "ko1keyz_towa_chrome_hearts_nail_ring_eyecatch_kr.png"

# TOWA member green accent (not a member-color clash for UI boxes)
G_BORDER = "#6fa843"
G_BG = "#f5f9ed"
G_SOFT = "#d7e7bf"
BOX_BORDER = "#ccc"
BOX_HEAD = "#f0f0f0"

# published TOWA related articles
L_GIVENCHY = "https://chomoand-1.com/towa-givenchy-tshirt-siyoung-dance-11855"
L_LOUNGE = "https://chomoand-1.com/what-brand-is-towas-loungewear-11093"
L_FAMILY = "https://chomoand-1.com/what-is-the-family-compositio-11059"

BASE_SLUG = "towa-chrome-hearts-nail-ring"


def upload_media_from_file(path: Path, filename: str, alt: str, content_type: str = "image/jpeg"):
    headers = {
        **HEADERS_AUTH,
        "Content-Type": content_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=path.read_bytes())
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
<figure class="wp-block-image size-large" style="text-align:center;">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;margin:0 auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>
</figure>
<!-- /wp:html -->'''


def post_draft(title, content, slug, lang, categories, featured_media, summary, translations=None):
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "lang": lang,
        "categories": categories,
        "featured_media": featured_media,
        "author": 2,
        "meta": {"jetpack_publicize_message": summary},
    }
    if translations:
        payload["translations"] = translations
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    return r.json()


def upload_eyecatch(path: Path):
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HEADERS_AUTH, "Content-Type": "image/png",
                 "Content-Disposition": f'attachment; filename="{path.name}"'},
        data=path.read_bytes(),
    )
    r.raise_for_status()
    return r.json()["id"]


print("uploading source images...")
selfie_media = upload_media_from_file(
    IMG_SELFIE, "ko1keyz_towa_chrome_hearts_nail_ring_selfie.jpg",
    "自撮りオフショットでシルバーのネイルリングを着けたTOWA",
)
product_media = upload_media_from_file(
    IMG_PRODUCT, "ko1keyz_towa_chrome_hearts_nail_ring_product.jpg",
    "クロムハーツ ネイル リング CHプラス フラットの単体画像",
)
print("selfie", selfie_media["id"], "product", product_media["id"])

CAP_JP = f'出典:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">X(旧Twitter)</a>'
CAP_KR = f'출처:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">X(옛 트위터)</a>'
CAP_EN = f'Source:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">X (formerly Twitter)</a>'

print("uploading eyecatches...")
JP_EYECATCH_ID = upload_eyecatch(EYECATCH_JP)
KR_EYECATCH_ID = upload_eyecatch(EYECATCH_KR)
print("eyecatch jp", JP_EYECATCH_ID, "kr", KR_EYECATCH_ID)

# ============================== JP ==============================
selfie_jp = build_img_html(selfie_media, "自撮りオフショットでシルバーのネイルリングを着けたTOWA", CAP_JP)
product_jp = build_img_html(product_media, "クロムハーツ ネイル リング CHプラス フラットの単体画像", CAP_JP)

JP_TITLE = "TOWAが自撮りで着けてたリングは？クロムハーツ！"
JP_SLUG = BASE_SLUG

JP_CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZ(コイキーズ)のTOWA(濱田永遠)さんが、鏡越しの自撮りオフショットで指に着けていたシルバーの指輪。<br>
公開直後はカルティエの「ジュスト アン クル」ではないかと言われていましたが、その後よりはっきり写った画像と着用アイテムの情報が出てきたことで、正体は<strong>クロムハーツ(Chrome Hearts)の「ネイル リング CHプラス フラット」</strong>とみられることがわかりました。<br>
この記事では、リングのデザインの特徴、よく似ているカルティエとの見分け方、気になる価格と購入先までまとめます。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BOX_BORDER};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">TOWA着用リングの基本情報</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;width:32%;">アイテム</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">リング(指輪)</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">ブランド</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">クロムハーツ(Chrome Hearts)</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">モデル</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">ネイル リング CHプラス フラット(NAIL RING CH＋ FLAT)</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">素材</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">シルバー925</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">参考価格</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">約11万〜13万円(新品・専門店の実勢価格)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">TOWAが着けているシルバーリングはどんなデザイン？</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>話題になっているのは、TOWAさんが鏡越しに自撮りしたオフショットの1枚です。<br>
くたっとしたブラウンのデニムジャケットにチェックシャツ、シルバーのチェーンネックレスを合わせたコーデで、スマホを持つ手の指に太めのシルバーリングがはっきりと写っています。<br>
その後にファンクラブ向けのトーク配信「KO1KEYZ Chat(プラチャ)」でも同じリングを着けている様子が確認されており、単発の衣装ではなく普段から愛用しているアイテムだと考えられます。</p>
<!-- /wp:paragraph -->

{selfie_jp}

<!-- wp:paragraph -->
<p>リングは、<span class="swl-marker mark_green">1本の釘が指にぐるりと巻き付いたような形</span>をしています。<br>
釘の頭にあたる部分が円盤状に平らで、反対側の先端が輪の上に少し重なるデザインです。<br>
衣装ではなくプライベートの自撮りでの着用のため、スタイリストが用意したものではなく本人の私物とみられます。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">ブランドはクロムハーツの「ネイル リング CHプラス フラット」</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>太めのシルバー、釘モチーフ、そして平らな釘の頭に入った<span class="swl-marker mark_green">クロムハーツの十字マーク(CHプラス)</span>。<br>
これらの特徴から、TOWAさんのリングは<span class="swl-marker mark_green" style="font-size:1.15em;"><strong>クロムハーツの「ネイル リング CHプラス フラット(NAIL RING CH＋ FLAT)」</strong></span>と考えて間違いなさそうです。<br>
釘の頭を平らに潰した「フラット」タイプに、クロムハーツを象徴するクロス(CHプラス)の刻印を組み合わせた定番リングで、バンドの内側には「CHROME HEARTS」のレタリングとクロス、製造年(2012など)の刻印が入ります。</p>
<!-- /wp:paragraph -->

{product_jp}

<!-- wp:html -->
<div style="border:1px solid {G_SOFT};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">クロムハーツ(Chrome Hearts)とは？</p>
<p style="margin:0;">1988年にアメリカ・ロサンゼルスで創業したシルバーアクセサリー＆レザーブランド。<br>
ゴシック様式のクロス(十字架)やダガー(短剣)をあしらった重厚なシルバー925のジュエリーが看板で、国内外のアーティストや俳優に長年愛されています。<br>
日本では路面の直営店のみでの取り扱いが基本で、公式サイトでのオンライン販売は行っていません。</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>CHプラス フラットは幅3mmほどのすっきりしたバンドで、釘の頭のクロス部分は直径8mm弱。<br>
ゴツすぎず着けやすいサイズ感で、シルバーチェーンやリングを重ね着けするTOWAさんの普段のスタイルにもよくなじんでいます。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">カルティエ「ジュスト アン クル」とよく似ている</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>TOWAさんのリングが最初にカルティエと言われたのは、<span class="swl-marker mark_green">カルティエにも釘モチーフの定番リング「ジュスト アン クル」がある</span>からです。<br>
「ジュスト アン クル(Juste un Clou)」はフランス語で「ただの釘」という意味で、1本の釘を指に巻き付けたようなフォルムはクロムハーツのネイル リングと遠目にはそっくりです。<br>
ただ、素材と頭のデザインをよく見ると両者ははっきり違います。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BOX_BORDER};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">見分け方の3つのポイント</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;width:24%;">釘の頭</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">クロムハーツ(CHプラス フラット)は頭が円盤状で、クロスの刻印が入る。カルティエは頭が小さく、六角形でロゴなし。</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">素材</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">クロムハーツはシルバー925で少し青みがかった白。カルティエは18Kゴールドやプラチナなどの貴金属。</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">刻印</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">クロムハーツはバンド内側に「CHROME HEARTS」の文字・クロス・製造年。カルティエは刻印が控えめでロゴも目立たない。</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>TOWAさんのリングは、平らな釘の頭に入ったクロスの刻印と、武骨で重量感のあるシルバーの質感からクロムハーツと判断できます。<br>
価格帯もヒントになり、カルティエのジュスト アン クル(リング)は18Kゴールドで20万円台〜と貴金属らしい値段なのに対し、クロムハーツのシルバー925は10万円台前半で、むしろこちらの方が手が届きやすい価格です。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">価格は？どこで買える？</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>クロムハーツは定価を公表しておらず、公式サイトでのオンライン販売も行っていません。<br>
ネイル リング CHプラス フラット(シルバー)の新品は、直営店やクロムハーツ専門店での実勢価格で<span class="swl-marker mark_green" style="font-size:1.15em;"><strong>おおよそ11万〜13万円(税込)</strong></span>ほど。<br>
リユース品や並行輸入品なら、サイズやコンディションによって5万〜13万円前後で流通しています。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_SOFT};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">クロムハーツ ネイル リングの購入先</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li style="margin:0 0 8px 0;">クロムハーツ直営店(東京・大阪などの路面店。店舗情報は公式サイトで確認)</li>
<li style="margin:0 0 8px 0;">RINKAN・GINZA RASIN・2nd STREET などの中古・リユースショップ(オンラインでも在庫あり)</li>
<li style="margin:0 0 8px 0;">SNKRDUNK(スニーカーダンク)・BUYMA などの並行・マーケットプレイス系</li>
<li style="margin:0;">メルカリ・ヤフオク!(個体差や真贋の見極めに注意)</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>人気モデルのため直営店でも品薄になりやすく、狙っているサイズがあれば見つけたタイミングで確保するのが現実的です。<br>
中古市場にはコピー品も多く出回っているので、購入前に刻印やシリアル、付属のインボイスの有無をしっかり確認しておきたいところです。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">まとめ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:2px solid {G_BORDER};border-radius:8px;background:rgba(111,168,67,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; TOWAが自撮りオフショットで着けていたのはクロムハーツの「ネイル リング CHプラス フラット」<br>
&#10003; 素材はシルバー925、釘の頭が円盤状でクロス(CHプラス)の刻印入り<br>
&#10003; カルティエ「ジュスト アン クル」と似ているが、頭のデザインと素材で見分けられる<br>
&#10003; 参考価格は新品で約11万〜13万円。公式通販はなく、直営店かリユースショップで探すのが基本
</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>釘モチーフのリングは重ね着けもしやすく、シルバーアクセ入門の1本としても人気があります。<br>
TOWAさんの手元コーデが気になっていた人は、まずはリユースショップで実物を眺めてみるところから始めてみてはいかがでしょうか！</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_SOFT};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">TOWA(濱田永遠)の関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">TOWAがSIYOUNGとの動画で着ていたGIVENCHYのTシャツを調べた記事</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">TOWAの部屋着(GELATO PIQUE×ドラえもん)のブランドを調べた記事</a></li>
<li><a href="{L_FAMILY}" target="_blank" rel="noopener">TOWA(濱田永遠)の家族構成をまとめた記事</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

JP_SUMMARY = "KO1KEYZ・TOWAが自撮りで着けていたシルバーリングは、クロムハーツの「ネイル リング CHプラス フラット」。釘の頭にクロス(CHプラス)の刻印が入るのが特徴で、カルティエのジュスト アン クルとの見分け方や、新品で約11万〜13万円という価格、買える場所までまとめました。"

jp_post = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, "ja", [66, 63, 104], JP_EYECATCH_ID, JP_SUMMARY)
JP_POST_ID = jp_post["id"]
print("JP_POST_ID", JP_POST_ID, jp_post["slug"], jp_post.get("link"))


# ============================== KR ==============================
selfie_kr = build_img_html(selfie_media, "셀카 오프숏에서 실버 네일 링을 낀 TOWA", CAP_KR)
product_kr = build_img_html(product_media, "크롬하츠 네일 링 CH플러스 플랫 단품 이미지", CAP_KR)

KR_TITLE = "TOWA가 셀카에서 낀 반지는? 크롬하츠!"
KR_SLUG = f"{BASE_SLUG}-kr"

KR_CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZ(코이키즈)의 TOWA(하마다 토와)가 거울 셀카 오프숏에서 손가락에 끼고 있던 실버 반지.<br>
공개 직후에는 까르띠에의 '쥐스트 앵 끌루'가 아니냐는 말이 많았지만, 이후 더 선명하게 찍힌 사진과 착용 아이템 정보가 나오면서 정체는 <strong>크롬하츠(Chrome Hearts)의 '네일 링 CH플러스 플랫'</strong>으로 보이는 것으로 확인됐습니다.<br>
이 글에서는 반지의 디자인 특징, 아주 비슷한 까르띠에와의 구별법, 궁금한 가격과 구입처까지 정리합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BOX_BORDER};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">TOWA 착용 반지의 기본 정보</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;width:32%;">아이템</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">반지(링)</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">브랜드</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">크롬하츠(Chrome Hearts)</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">모델</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">네일 링 CH플러스 플랫(NAIL RING CH＋ FLAT)</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">소재</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">실버925</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">참고가</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">약 11만〜13만 엔(신품・전문점 실거래가)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">TOWA가 낀 실버 반지는 어떤 디자인?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>화제가 된 것은 TOWA가 거울로 셀카를 찍은 오프숏 한 장입니다.<br>
헐렁한 브라운 데님 재킷에 체크 셔츠, 실버 체인 목걸이를 매치한 코디로, 스마트폰을 든 손의 손가락에 두툼한 실버 반지가 또렷하게 찍혀 있습니다.<br>
이후 팬클럽용 토크 방송 'KO1KEYZ Chat(플러스챗)'에서도 같은 반지를 낀 모습이 확인되어, 일회성 의상이 아니라 평소에 애용하는 아이템으로 보입니다.</p>
<!-- /wp:paragraph -->

{selfie_kr}

<!-- wp:paragraph -->
<p>반지는 <span class="swl-marker mark_green">못 하나가 손가락을 빙 둘러 감은 듯한 형태</span>를 하고 있습니다.<br>
못의 머리 부분이 원반 모양으로 평평하고, 반대쪽 끝이 링 위에 살짝 겹치는 디자인입니다.<br>
의상이 아니라 사적인 셀카에서의 착용이라, 스타일리스트가 준비한 것이 아닌 본인의 사물로 보입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">브랜드는 크롬하츠의 '네일 링 CH플러스 플랫'</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>두툼한 실버, 못 모티프, 그리고 평평한 못 머리에 들어간 <span class="swl-marker mark_green">크롬하츠의 십자 마크(CH플러스)</span>.<br>
이런 특징으로 볼 때, TOWA의 반지는 <span class="swl-marker mark_green" style="font-size:1.15em;"><strong>크롬하츠의 '네일 링 CH플러스 플랫(NAIL RING CH＋ FLAT)'</strong></span>으로 봐도 틀림없어 보입니다.<br>
못 머리를 평평하게 누른 '플랫' 타입에, 크롬하츠를 상징하는 크로스(CH플러스) 각인을 조합한 스테디셀러 반지로, 밴드 안쪽에는 'CHROME HEARTS' 레터링과 크로스, 제조 연도(2012 등)의 각인이 들어갑니다.</p>
<!-- /wp:paragraph -->

{product_kr}

<!-- wp:html -->
<div style="border:1px solid {G_SOFT};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">크롬하츠(Chrome Hearts)란?</p>
<p style="margin:0;">1988년 미국 로스앤젤레스에서 창업한 실버 액세서리＆레더 브랜드.<br>
고딕 양식의 크로스(십자가)나 대거(단검)를 넣은 묵직한 실버925 주얼리가 간판으로, 국내외 아티스트와 배우에게 오랫동안 사랑받고 있습니다.<br>
일본에서는 노면 직영점에서만 취급하는 것이 기본이며, 공식 사이트에서의 온라인 판매는 하지 않습니다.</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>CH플러스 플랫은 폭 3mm 정도의 깔끔한 밴드로, 못 머리의 크로스 부분은 지름 8mm 남짓.<br>
너무 투박하지 않고 끼기 편한 사이즈감으로, 실버 체인이나 반지를 레이어드하는 TOWA의 평소 스타일에도 잘 어울립니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">까르띠에 '쥐스트 앵 끌루'와 아주 비슷하다</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>TOWA의 반지가 처음에 까르띠에라고 불린 것은, <span class="swl-marker mark_green">까르띠에에도 못 모티프의 스테디셀러 반지 '쥐스트 앵 끌루'가 있기</span> 때문입니다.<br>
'쥐스트 앵 끌루(Juste un Clou)'는 프랑스어로 '그저 못'이라는 뜻으로, 못 하나를 손가락에 감은 듯한 형태는 크롬하츠의 네일 링과 멀리서 보면 꼭 닮았습니다.<br>
다만 소재와 머리 디자인을 잘 보면 둘은 확실히 다릅니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BOX_BORDER};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">구별하는 3가지 포인트</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;width:24%;">못 머리</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">크롬하츠(CH플러스 플랫)는 머리가 원반 모양이고 크로스 각인이 들어간다. 까르띠에는 머리가 작고 육각형이며 로고가 없다.</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">소재</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">크롬하츠는 실버925로 살짝 푸른빛이 도는 흰색. 까르띠에는 18K 골드나 플래티넘 등 귀금속.</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">각인</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">크롬하츠는 밴드 안쪽에 'CHROME HEARTS' 글자・크로스・제조 연도. 까르띠에는 각인이 절제되어 있고 로고도 눈에 띄지 않는다.</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>TOWA의 반지는 평평한 못 머리에 들어간 크로스 각인과, 투박하고 묵직한 실버의 질감으로 크롬하츠라고 판단할 수 있습니다.<br>
가격대도 힌트가 되는데, 까르띠에의 쥐스트 앵 끌루(반지)는 18K 골드로 20만 엔대〜라는 귀금속다운 가격인 반면, 크롬하츠의 실버925는 10만 엔대 초반으로 오히려 이쪽이 더 접근하기 쉬운 가격입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">가격은? 어디서 살 수 있어?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>크롬하츠는 정가를 공개하지 않고, 공식 사이트에서의 온라인 판매도 하지 않습니다.<br>
네일 링 CH플러스 플랫(실버)의 신품은 직영점이나 크롬하츠 전문점에서의 실거래가로 <span class="swl-marker mark_green" style="font-size:1.15em;"><strong>대략 11만〜13만 엔(세금 포함)</strong></span> 정도.<br>
리유즈 제품이나 병행 수입품이라면 사이즈와 컨디션에 따라 5만〜13만 엔 전후로 유통되고 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_SOFT};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">크롬하츠 네일 링 구입처</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li style="margin:0 0 8px 0;">크롬하츠 직영점(도쿄・오사카 등의 노면점. 매장 정보는 공식 사이트에서 확인)</li>
<li style="margin:0 0 8px 0;">RINKAN・GINZA RASIN・2nd STREET 등의 중고・리유즈 숍(온라인에도 재고 있음)</li>
<li style="margin:0 0 8px 0;">SNKRDUNK(스니커덩크)・BUYMA 등의 병행・마켓플레이스 계열</li>
<li style="margin:0;">메루카리・야후옥션(개체 차이와 진위 판별에 주의)</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>인기 모델이라 직영점에서도 품절되기 쉬워, 노리는 사이즈가 있다면 발견했을 때 확보하는 것이 현실적입니다.<br>
중고 시장에는 카피 제품도 많이 돌고 있으니, 구입 전에 각인이나 시리얼, 부속 인보이스의 유무를 꼼꼼히 확인해 두고 싶은 부분입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">정리</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:2px solid {G_BORDER};border-radius:8px;background:rgba(111,168,67,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; TOWA가 셀카 오프숏에서 낀 것은 크롬하츠의 '네일 링 CH플러스 플랫'<br>
&#10003; 소재는 실버925, 못 머리가 원반 모양이고 크로스(CH플러스) 각인 있음<br>
&#10003; 까르띠에 '쥐스트 앵 끌루'와 비슷하지만, 머리 디자인과 소재로 구별할 수 있다<br>
&#10003; 참고가는 신품으로 약 11만〜13만 엔. 공식 온라인 판매는 없고 직영점이나 리유즈 숍에서 찾는 것이 기본
</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>못 모티프의 반지는 레이어드도 하기 쉬워, 실버 액세서리 입문용 한 개로도 인기가 있습니다.<br>
TOWA의 손끝 코디가 궁금했던 분은, 우선 리유즈 숍에서 실물을 구경해 보는 것부터 시작해 보는 건 어떨까요!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_SOFT};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">TOWA(하마다 토와) 관련 글</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">TOWA가 SIYOUNG과의 영상에서 입은 GIVENCHY 티셔츠를 알아본 글</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">TOWA의 룸웨어(GELATO PIQUE×도라에몽) 브랜드를 알아본 글</a></li>
<li><a href="{L_FAMILY}" target="_blank" rel="noopener">TOWA(하마다 토와)의 가족 구성을 정리한 글</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

KR_SUMMARY = "KO1KEYZ TOWA가 셀카에서 낀 실버 반지는 크롬하츠의 '네일 링 CH플러스 플랫'. 못 머리에 크로스(CH플러스) 각인이 들어가는 것이 특징으로, 까르띠에 쥐스트 앵 끌루와의 구별법과 신품 약 11만〜13만 엔이라는 가격, 구입처까지 정리했습니다."

kr_post = post_draft(KR_TITLE, KR_CONTENT, KR_SLUG, "ko", [74, 78, 108], KR_EYECATCH_ID, KR_SUMMARY,
                     translations={"ja": JP_POST_ID})
print("KR_POST_ID", kr_post["id"], kr_post["slug"], kr_post.get("link"))


# ============================== EN ==============================
selfie_en = build_img_html(selfie_media, "TOWA wearing a silver nail ring in a mirror-selfie off-shot", CAP_EN)
product_en = build_img_html(product_media, "Chrome Hearts Nail Ring CH Plus Flat, product shot", CAP_EN)

EN_TITLE = "The Ring TOWA Wore in His Selfie? It's Chrome Hearts!"
EN_SLUG = f"{BASE_SLUG}-en"

EN_CONTENT = f"""<!-- wp:paragraph -->
<p>The silver ring KO1KEYZ's TOWA (Towa Hamada) was wearing in a mirror-selfie off-shot.<br>
Right after it surfaced, fans guessed it was Cartier's "Juste un Clou," but once clearer photos and item info came out, it looks like the real answer is <strong>Chrome Hearts' "Nail Ring CH Plus Flat."</strong><br>
This article covers the ring's design details, how to tell it apart from the very similar Cartier piece, and the price and where to buy.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BOX_BORDER};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">TOWA's ring: the basics</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;width:32%;">Item</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">Ring</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">Brand</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">Chrome Hearts</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">Model</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">Nail Ring CH Plus Flat (NAIL RING CH＋ FLAT)</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">Material</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">Sterling silver 925</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">Reference price</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">about 110,000–130,000 yen (new, specialist-shop street price)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What does TOWA's silver ring look like?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The photo people are talking about is a mirror-selfie off-shot of TOWA.<br>
He's in a slouchy brown denim jacket over a check shirt with a silver chain necklace, and on the hand holding his phone you can clearly see a chunky silver ring.<br>
He was later seen wearing the same ring on the fan-club talk stream "KO1KEYZ Chat (Pracha)," so it seems to be something he wears regularly rather than a one-off styling choice.</p>
<!-- /wp:paragraph -->

{selfie_en}

<!-- wp:paragraph -->
<p>The ring is shaped like <span class="swl-marker mark_green">a single nail wrapped all the way around the finger</span>.<br>
The nail head is a flat disc, and the pointed end overlaps the band slightly on the other side.<br>
Since he's wearing it in a private selfie rather than in costume, it's likely his own piece and not something a stylist provided.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The brand is Chrome Hearts: the "Nail Ring CH Plus Flat"</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A chunky silver band, a nail motif, and <span class="swl-marker mark_green">the Chrome Hearts cross (CH Plus)</span> stamped into the flat nail head.<br>
From these, TOWA's ring is almost certainly the <span class="swl-marker mark_green" style="font-size:1.15em;"><strong>Chrome Hearts "Nail Ring CH Plus Flat" (NAIL RING CH＋ FLAT)</strong></span>.<br>
It's a staple ring that combines a flattened "flat" nail head with the brand's signature cross (CH Plus) stamp, and the inside of the band carries "CHROME HEARTS" lettering, a cross, and a production year (such as 2012).</p>
<!-- /wp:paragraph -->

{product_en}

<!-- wp:html -->
<div style="border:1px solid {G_SOFT};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">What is Chrome Hearts?</p>
<p style="margin:0;">A silver-jewelry and leather brand founded in Los Angeles in 1988.<br>
It's known for heavy sterling-silver 925 jewelry featuring Gothic crosses and daggers, and has been favored by musicians and actors around the world for decades.<br>
In Japan it's basically sold only at its own street-level boutiques, with no online sales on the official site.</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>The CH Plus Flat has a clean band around 3mm wide, with the cross on the nail head just under 8mm across.<br>
It's an easy-to-wear size that isn't too bulky, and it fits right in with TOWA's usual habit of stacking silver chains and rings.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">It looks a lot like Cartier's "Juste un Clou"</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The reason TOWA's ring was first called Cartier is that <span class="swl-marker mark_green">Cartier also has a nail-motif staple ring, the "Juste un Clou."</span><br>
"Juste un Clou" is French for "just a nail," and its form — a single nail wound around the finger — looks just like the Chrome Hearts nail ring from a distance.<br>
Look closely at the material and the head, though, and the two are clearly different.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BOX_BORDER};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">Three ways to tell them apart</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;width:24%;">Nail head</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">Chrome Hearts (CH Plus Flat) has a disc-shaped head stamped with a cross. Cartier's head is small, hexagonal, and has no logo.</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">Material</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">Chrome Hearts is sterling silver 925, a slightly bluish white. Cartier is a precious metal such as 18K gold or platinum.</td></tr>
<tr><td style="background:{BOX_HEAD};border:1px solid {BOX_BORDER};padding:8px 12px;">Stamps</td><td style="border:1px solid {BOX_BORDER};padding:8px 12px;">Chrome Hearts stamps "CHROME HEARTS," a cross and a production year inside the band. Cartier's markings are restrained and its logo is not prominent.</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>TOWA's ring reads as Chrome Hearts thanks to the cross stamped into the flat nail head and the rugged, heavy feel of the silver.<br>
Price is another clue: Cartier's Juste un Clou ring is 18K gold and starts in the 200,000-yen range, while Chrome Hearts' silver 925 sits in the low 100,000s — so the Chrome Hearts one is actually the more accessible of the two.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How much is it, and where can you buy it?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Chrome Hearts doesn't publish list prices and doesn't sell online through its official site.<br>
A new Nail Ring CH Plus Flat (silver) runs <span class="swl-marker mark_green" style="font-size:1.15em;"><strong>roughly 110,000–130,000 yen (tax incl.)</strong></span> at boutiques and Chrome Hearts specialist shops.<br>
Pre-owned or parallel-import pieces trade at around 50,000–130,000 yen depending on size and condition.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_SOFT};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">Where to buy the Chrome Hearts nail ring</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li style="margin:0 0 8px 0;">Chrome Hearts boutiques (street-level stores in Tokyo, Osaka, etc.; check the official site for locations)</li>
<li style="margin:0 0 8px 0;">Pre-owned / resale shops such as RINKAN, GINZA RASIN and 2nd STREET (stock online too)</li>
<li style="margin:0 0 8px 0;">Parallel / marketplace channels such as SNKRDUNK and BUYMA</li>
<li style="margin:0;">Mercari and Yahoo! Auctions (watch for individual variation and authenticity)</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>It's a popular model and often out of stock even at the boutiques, so if there's a size you want, it's realistic to grab it when you spot it.<br>
The secondhand market is also full of copies, so check the stamps, serial and whether an invoice is included before buying.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Summary</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:2px solid {G_BORDER};border-radius:8px;background:rgba(111,168,67,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; The ring TOWA wore in his selfie off-shot is Chrome Hearts' "Nail Ring CH Plus Flat"<br>
&#10003; It's sterling silver 925, with a disc-shaped nail head stamped with the cross (CH Plus)<br>
&#10003; It resembles Cartier's "Juste un Clou," but the head design and material tell them apart<br>
&#10003; Reference price is about 110,000–130,000 yen new; no official online sales, so look at boutiques or resale shops
</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Nail-motif rings stack easily and are popular as a first piece of silver jewelry.<br>
If you've been eyeing TOWA's hand styling, starting by looking at one in person at a resale shop isn't a bad move!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_SOFT};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">More on TOWA (Towa Hamada)</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">Identifying the GIVENCHY tee TOWA wore in his video with SIYOUNG</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">Identifying the brand of TOWA's loungewear (GELATO PIQUE x Doraemon)</a></li>
<li><a href="{L_FAMILY}" target="_blank" rel="noopener">A rundown of TOWA's (Towa Hamada) family</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

EN_SUMMARY = "The silver ring KO1KEYZ's TOWA wore in a selfie is Chrome Hearts' \"Nail Ring CH Plus Flat.\" The cross (CH Plus) stamped into the flat nail head is the giveaway; here's how to tell it from Cartier's Juste un Clou, plus the roughly 110,000-130,000 yen price and where to buy."

en_post = post_draft(EN_TITLE, EN_CONTENT, EN_SLUG, "en", [110, 114], JP_EYECATCH_ID, EN_SUMMARY,
                     translations={"ja": JP_POST_ID})
print("EN_POST_ID", en_post["id"], en_post["slug"], en_post.get("link"))

print("\n=== DONE ===")
print("JP", JP_POST_ID, f"{WP_URL}/wp-admin/post.php?post={JP_POST_ID}&action=edit")
print("KR", kr_post["id"], f"{WP_URL}/wp-admin/post.php?post={kr_post['id']}&action=edit")
print("EN", en_post["id"], f"{WP_URL}/wp-admin/post.php?post={en_post['id']}&action=edit")
