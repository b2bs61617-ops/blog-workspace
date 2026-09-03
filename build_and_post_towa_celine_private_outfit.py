# -*- coding: utf-8 -*-
import json, base64, os, subprocess, sys
from pathlib import Path
from urllib.parse import quote

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

SOURCE_TWEET = "https://x.com/Towa_OUTFITS/status/2095105005040935194"
IMG_COLLAGE = ROOT / "images" / "towa_celine_private_outfit_source.jpg"

G_BORDER = "#9bc96e"
G_BG = "#f5faec"
BUY_BORDER = "#ddd9d3"
BUY_BAR = "#8a8378"
BUY_BG = "#f7f6f4"

# published TOWA related articles
L_GIVENCHY = "https://chomoand-1.com/towa-givenchy-tshirt-siyoung-dance-11855"
L_LOUNGE = "https://chomoand-1.com/what-brand-is-towas-loungewear-11093"
L_JAGAIMO = "https://chomoand-1.com/is-towas-new-character-jagaimo-11691"
L_WIKI = "https://chomoand-1.com/hamadatowa_wiki-2452"

# purchase links
CELINE_JP = "https://www.celine.com/ja-jp/celine-men/accessoire/casquettes-et-accessoires-souples/"
BUYMA_CAP = "https://www.buyma.com/r/_CELINE-%E3%82%BB%E3%83%AA%E3%83%BC%E3%83%8C/keyword-" + quote("リシュリュー キャップ") + "/"
BUYMA_TEE = "https://www.buyma.com/r/_CELINE-%E3%82%BB%E3%83%AA%E3%83%BC%E3%83%8C/keyword-" + quote("タイダイ Tシャツ") + "/"
VESTIAIRE_TEE = "https://www.vestiairecollective.com/search/?q=" + quote("celine tie dye t-shirt")
GRAILED_TEE = "https://www.grailed.com/designers/celine/t-shirts"


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


def media_obj(mid):
    return requests.get(f"{WP_URL}/wp-json/wp/v2/media/{mid}", headers=HEADERS_AUTH).json()


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


print("uploading source collage image...")
collage_media = upload_media_from_file(
    IMG_COLLAGE, "towa_celine_private_outfit_source.jpg",
    "グリーンのCELINEキャップとタイダイのCELINE Tシャツを着たTOWAの私服コーデ",
)
COLLAGE_ID = collage_media["id"]
print("collage", COLLAGE_ID)

CAP_JP = f'出典:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>'
CAP_KR = f'출처:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>'
CAP_EN = f'Source:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>'


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


def make_eyecatch(args, out_path):
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"), *args, "--out", str(out_path)],
        check=True,
    )
    mr = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HEADERS_AUTH, "Content-Type": "image/png",
                 "Content-Disposition": f'attachment; filename="{out_path.name}"'},
        data=out_path.read_bytes(),
    )
    mr.raise_for_status()
    return mr.json()["id"]


# ============================== JP ==============================
img_jp = build_img_html(
    collage_media,
    "グリーンのCELINEキャップとタイダイのCELINE Tシャツを着たTOWAの私服コーデ",
    CAP_JP,
)

JP_TITLE = "TOWAの私服はCELINE！帽子とTシャツの値段は？"
JP_SLUG = "towa-private-celine-cap-tshirt"

JP_CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZのTOWA(濱田永遠)さんの私服姿がXで公開され、身につけていた帽子とTシャツに注目が集まっています。<br>
結論から書くと、<strong>帽子もTシャツもどちらも「CELINE(セリーヌ)」のアイテム</strong>で、帽子が「トリオンフ リシュリュー キャップ」(参考価格 約86,900円)、Tシャツがタイダイ柄に赤いハートを配した「CELINE PARIS」Tシャツ(参考価格 約154,000円)とみられます。<br>
トップスと帽子だけで合わせておよそ24万円という、いかにもハイブランドらしい私服コーデです。<br>
この記事では、コーデが公開された経緯と、CELINEの2アイテムそれぞれのデザイン・価格・買える場所をまとめます。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li>私服コーデが公開された経緯</li>
<li>帽子(CELINE トリオンフ リシュリュー キャップ)の特徴と価格</li>
<li>Tシャツ(CELINE タイダイ ハート柄)の特徴と価格</li>
<li>それぞれどこで買えるか</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">どんな私服姿?Xで公開されたCELINEコーデ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>公開元:</strong>Xの私服・衣装まとめアカウントの投稿</p>
<p style="margin:4px 0 0 0;"><strong>コーデ:</strong>グリーンのCELINEキャップ+レインボーのタイダイTシャツ</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>今回話題になっているのは、KO1KEYZのメンバーの私服や衣装を追っているXアカウントが公開した、TOWAさんの全身コーデの写真です。<br>
鮮やかなグリーンのベースボールキャップに、赤・青・黄・ピンクが渦を巻くタイダイ柄のTシャツを合わせた、色使いの目立つスタイルになっています。<br>
Tシャツの胸元にはサイケデリックな書体の「CELINE PARIS」の文字と大きな赤いハートが入っており、そこからブランドを調べる動きが広がりました。<br>
投稿には参考として、CELINE公式サイトに掲載されたキャップとTシャツの商品ページも並べられていました。</p>
<!-- /wp:paragraph -->

{img_jp}

<!-- wp:heading -->
<h2 class="wp-block-heading">帽子は?CELINE「トリオンフ リシュリュー キャップ」</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>ブランド:</strong>CELINE(セリーヌ)</p>
<p style="margin:4px 0 0 0;"><strong>アイテム:</strong>トリオンフ リシュリュー キャップ ライトコットンツイル(グリーン)</p>
<p style="margin:4px 0 0 0;"><strong>参考価格:</strong>約86,900円(税込)</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>TOWAさんがかぶっていたグリーンのキャップは、CELINEの定番「トリオンフ リシュリュー キャップ」です。<br>
フロントにはCELINEを象徴する「トリオンフ(凱旋門)」モチーフが同色の刺繍で控えめに入り、ライトコットンツイル素材の6枚はぎで仕立てられています。<br>
名前にある「リシュリュー」は、ツバ(ブリム)にステッチを効かせて丸みを持たせた仕様のことです。<br>
ブラック・ホワイト・カーキといった定番色に加え、TOWAさんが選んだような発色のよいグリーンもシーズンカラーとして展開されています。<br>
参考価格は約86,900円(税込)で、CELINE公式サイトや直営店、一部百貨店で今も購入できる現行アイテムです。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BUY_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BUY_BAR};color:#fff;">帽子(トリオンフ リシュリュー キャップ)の購入先</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BUY_BG};">
<li style="margin:0 0 8px 0;"><a href="{CELINE_JP}" target="_blank" rel="noopener">CELINE公式サイト(celine.com)の帽子カテゴリ</a></li>
<li style="margin:0;"><a href="{BUYMA_CAP}" target="_blank" rel="noopener">BUYMAで「CELINE リシュリュー キャップ」を探す</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Tシャツは?CELINEのタイダイ「ハート」Tシャツ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>ブランド:</strong>CELINE(セリーヌ/エディ・スリマン期)</p>
<p style="margin:4px 0 0 0;"><strong>アイテム:</strong>タイダイ柄「CELINE PARIS」Tシャツ(リブコットンジャージー)</p>
<p style="margin:4px 0 0 0;"><strong>参考価格:</strong>約154,000円 ※現在は主に二次流通</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Tシャツも同じくCELINEのもので、リブ編みのコットンジャージーを使ったスリムフィットのクルーネックに、レインボーのタイダイをほどこしたデザインとみられます。<br>
渦を巻くタイダイへ赤いハートと、うねるような書体の「CELINE PARIS」を重ねたグラフィックは、デザイナーのエディ・スリマンが手がけた2021年ごろのCELINE HOMME(通称「Dancing Kid」)のタイダイ・シリーズに近い雰囲気を持っています。<br>
参考価格はおよそ154,000円とされますが、すでに数年前のコレクションのため、現在はCELINEの現行ラインナップには並んでいません。<br>
今は古着・リユースショップや海外の二次流通サイトで見かける形になっており、状態やサイズによって価格差が大きく、目安として10万円前後から流通しています。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BUY_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BUY_BAR};color:#fff;">Tシャツ(CELINE タイダイ ハート柄)の購入先</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BUY_BG};">
<li style="margin:0 0 8px 0;"><a href="{BUYMA_TEE}" target="_blank" rel="noopener">BUYMAで「CELINE タイダイ Tシャツ」を探す</a></li>
<li style="margin:0 0 8px 0;"><a href="{VESTIAIRE_TEE}" target="_blank" rel="noopener">Vestiaire Collectiveで「celine tie dye t-shirt」を探す</a></li>
<li style="margin:0;"><a href="{GRAILED_TEE}" target="_blank" rel="noopener">Grailed(グレイルド)のCELINE Tシャツ一覧</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">これはTOWAの私物?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>今回のコーデについて、本人や運営からの公式な発信はなく、私物と言い切れる情報は出ていません。<br>
ただ、ステージ衣装ではない普段着の写真として広まっていることから、TOWAさん自身が私服として選んだ可能性が高いとみられます。<br>
TOWAさんはこれまでも、SIYOUNGさんとのダンス動画で着ていた<a href="{L_GIVENCHY}" target="_blank" rel="noopener">GIVENCHYの「4G」グラフィックTシャツ</a>など、ハイブランドの服をたびたび身につけており、ファッション好きな一面が知られています。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">まとめ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>TOWAの私服姿がXで公開され、帽子とTシャツがともにCELINEだと話題に</li>
<li>帽子はCELINE「トリオンフ リシュリュー キャップ」(グリーン)で参考価格 約86,900円、現行品</li>
<li>TシャツはCELINEのタイダイ「ハート」柄(エディ・スリマン期・2021年ごろ)で参考価格 約154,000円、現在は二次流通が中心</li>
<li>2点合わせておよそ24万円のハイブランドコーデ</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>合計で20万円を超えるコーデを、派手すぎず自然に着こなすあたりに、TOWAさんらしいセンスがうかがえます。<br>
グリーンのキャップは今も手に入るので、雰囲気だけでも取り入れてみたい方は公式サイトをのぞいてみてはいかがでしょうか!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">TOWA(濱田永遠)さんの関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">SIYOUNGとのダンス動画で着ていたGIVENCHY「4G」Tシャツを特定した記事</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">ナイトルーティンで着ていたルームウェアのブランドを特定した記事</a></li>
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">TOWAの新キャラクター「じゃがいもっぷりん」を紹介した記事</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">TOWA(濱田永遠)のwiki風プロフィール・経歴をまとめた記事</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

JP_SUMMARY = "KO1KEYZ・TOWAの私服姿がXで公開。帽子はCELINE「トリオンフ リシュリュー キャップ」(約86,900円)、TシャツはCELINEのタイダイ「ハート」柄(約154,000円)で、2点でおよそ24万円のハイブランドコーデでした。"

JP_EYECATCH_ID = make_eyecatch(
    ["--top", "TOWAの私服はどこの？", "--main", "KO1KEYZ", "--bottom", "CELINEの帽子とTシャツと判明！"],
    ROOT / "images" / "towa_celine_private_outfit_eyecatch.png",
)
print("JP_EYECATCH_ID", JP_EYECATCH_ID)

jp_post = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, "ja", [66, 63, 104], JP_EYECATCH_ID, JP_SUMMARY)
JP_POST_ID = jp_post["id"]
print("JP_POST_ID", JP_POST_ID, jp_post["slug"], jp_post.get("link"))


# ============================== KR ==============================
img_kr = build_img_html(
    collage_media,
    "그린 CELINE 캡과 타이다이 CELINE 티셔츠를 입은 TOWA의 사복 코디",
    CAP_KR,
)

KR_TITLE = "TOWA의 사복은 CELINE! 모자와 티셔츠 가격은?"
KR_SLUG = f"{JP_SLUG}-kr"

KR_CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZ의 TOWA(하마다 토와)의 사복 차림이 X에 공개되면서, 쓰고 입은 모자와 티셔츠에 관심이 쏠리고 있습니다.<br>
결론부터 말하면, <strong>모자도 티셔츠도 모두 'CELINE(셀린느)' 아이템</strong>으로, 모자는 '트리옹프 리슐리외 캡'(참고가 약 86,900엔), 티셔츠는 타이다이 무늬에 빨간 하트를 넣은 'CELINE PARIS' 티셔츠(참고가 약 154,000엔)로 보입니다.<br>
상의와 모자만으로 합쳐서 약 24만 엔이라는, 그야말로 하이브랜드다운 사복 코디입니다.<br>
이 글에서는 코디가 공개된 경위와, CELINE 두 아이템 각각의 디자인・가격・살 수 있는 곳을 정리합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">이 글에서 알 수 있는 것</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li>사복 코디가 공개된 경위</li>
<li>모자(CELINE 트리옹프 리슐리외 캡)의 특징과 가격</li>
<li>티셔츠(CELINE 타이다이 하트 무늬)의 특징과 가격</li>
<li>각각 어디서 살 수 있는지</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">어떤 사복 차림? X에 공개된 CELINE 코디</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>공개처:</strong>X의 사복・의상 정리 계정 게시물</p>
<p style="margin:4px 0 0 0;"><strong>코디:</strong>그린 CELINE 캡 + 레인보우 타이다이 티셔츠</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>이번에 화제가 된 것은, KO1KEYZ 멤버의 사복이나 의상을 추적하는 X 계정이 공개한 TOWA의 전신 코디 사진입니다.<br>
선명한 그린 베이스볼 캡에, 빨강・파랑・노랑・핑크가 소용돌이치는 타이다이 무늬 티셔츠를 매치한, 색 사용이 눈에 띄는 스타일입니다.<br>
티셔츠 가슴 부분에는 사이키델릭한 서체의 'CELINE PARIS' 글자와 큰 빨간 하트가 들어가 있어, 거기서 브랜드를 찾는 움직임이 퍼졌습니다.<br>
게시물에는 참고로 CELINE 공식 사이트에 실린 캡과 티셔츠의 상품 페이지도 함께 올라와 있었습니다.</p>
<!-- /wp:paragraph -->

{img_kr}

<!-- wp:heading -->
<h2 class="wp-block-heading">모자는? CELINE '트리옹프 리슐리외 캡'</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>브랜드:</strong>CELINE(셀린느)</p>
<p style="margin:4px 0 0 0;"><strong>아이템:</strong>트리옹프 리슐리외 캡 라이트 코튼 트윌(그린)</p>
<p style="margin:4px 0 0 0;"><strong>참고가:</strong>약 86,900엔(세금 포함)</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>TOWA가 쓰고 있던 그린 캡은 CELINE의 스테디셀러 '트리옹프 리슐리외 캡'입니다.<br>
앞면에는 CELINE를 상징하는 '트리옹프(개선문)' 모티프가 같은 색 자수로 은은하게 들어가 있고, 라이트 코튼 트윌 소재의 6조각 재단으로 만들어졌습니다.<br>
이름에 있는 '리슐리외'는 챙(브림)에 스티치를 넣어 둥그스름하게 만든 사양을 가리킵니다.<br>
블랙・화이트・카키 같은 기본색에 더해, TOWA가 고른 것 같은 발색 좋은 그린도 시즌 컬러로 전개되고 있습니다.<br>
참고가는 약 86,900엔(세금 포함)이며, CELINE 공식 사이트나 직영점, 일부 백화점에서 지금도 살 수 있는 현행 아이템입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BUY_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BUY_BAR};color:#fff;">모자(트리옹프 리슐리외 캡) 구입처</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BUY_BG};">
<li style="margin:0 0 8px 0;"><a href="{CELINE_JP}" target="_blank" rel="noopener">CELINE 공식 사이트(celine.com)의 모자 카테고리</a></li>
<li style="margin:0;"><a href="{BUYMA_CAP}" target="_blank" rel="noopener">BUYMA에서 'CELINE 리슐리외 캡' 검색</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">티셔츠는? CELINE의 타이다이 '하트' 티셔츠</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>브랜드:</strong>CELINE(셀린느 / 에디 슬리먼 시기)</p>
<p style="margin:4px 0 0 0;"><strong>아이템:</strong>타이다이 무늬 'CELINE PARIS' 티셔츠(립 코튼 저지)</p>
<p style="margin:4px 0 0 0;"><strong>참고가:</strong>약 154,000엔 ※현재는 주로 중고 유통</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>티셔츠도 마찬가지로 CELINE 제품으로, 립 조직의 코튼 저지를 쓴 슬림 핏 크루넥에 레인보우 타이다이를 입힌 디자인으로 보입니다.<br>
소용돌이치는 타이다이에 빨간 하트와, 굽이치는 서체의 'CELINE PARIS'를 겹친 그래픽은, 디자이너 에디 슬리먼이 맡았던 2021년경 CELINE HOMME(통칭 'Dancing Kid')의 타이다이 시리즈와 비슷한 분위기를 지니고 있습니다.<br>
참고가는 약 154,000엔으로 알려져 있지만, 이미 몇 년 전 컬렉션이라 현재 CELINE 현행 라인업에는 없습니다.<br>
지금은 구제・리유즈 숍이나 해외 중고 유통 사이트에서 볼 수 있는 형태이며, 상태와 사이즈에 따라 가격 차가 커서 대략 10만 엔 전후부터 유통되고 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BUY_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BUY_BAR};color:#fff;">티셔츠(CELINE 타이다이 하트) 구입처</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BUY_BG};">
<li style="margin:0 0 8px 0;"><a href="{BUYMA_TEE}" target="_blank" rel="noopener">BUYMA에서 'CELINE 타이다이 티셔츠' 검색</a></li>
<li style="margin:0 0 8px 0;"><a href="{VESTIAIRE_TEE}" target="_blank" rel="noopener">Vestiaire Collective에서 'celine tie dye t-shirt' 검색</a></li>
<li style="margin:0;"><a href="{GRAILED_TEE}" target="_blank" rel="noopener">Grailed(그레일드)의 CELINE 티셔츠 목록</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">이건 TOWA의 사물?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>이번 코디에 대해 본인이나 운영 측의 공식 언급은 없어, 사물이라고 단언할 수 있는 정보는 나오지 않았습니다.<br>
다만 무대 의상이 아닌 평상복 사진으로 퍼지고 있어, TOWA 본인이 사복으로 고른 것일 가능성이 높다고 보입니다.<br>
TOWA는 지금까지도 SIYOUNG과의 댄스 영상에서 입었던 <a href="{L_GIVENCHY}" target="_blank" rel="noopener">GIVENCHY의 '4G' 그래픽 티셔츠</a> 등, 하이브랜드 옷을 자주 착용해 와서 패션을 좋아하는 면모가 알려져 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">정리</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>TOWA의 사복 차림이 X에 공개되어, 모자와 티셔츠가 모두 CELINE이라고 화제</li>
<li>모자는 CELINE '트리옹프 리슐리외 캡'(그린)으로 참고가 약 86,900엔, 현행품</li>
<li>티셔츠는 CELINE의 타이다이 '하트' 무늬(에디 슬리먼 시기・2021년경)로 참고가 약 154,000엔, 현재는 중고 유통이 중심</li>
<li>두 점 합쳐서 약 24만 엔의 하이브랜드 코디</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>합쳐서 20만 엔이 넘는 코디를, 과하지 않고 자연스럽게 소화하는 데서 TOWA다운 센스가 느껴집니다.<br>
그린 캡은 지금도 구할 수 있으니, 분위기만이라도 따라 해 보고 싶은 분은 공식 사이트를 들여다보는 것도 좋겠네요!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">TOWA(하마다 토와) 관련 글</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">SIYOUNG과의 댄스 영상에서 입은 GIVENCHY '4G' 티셔츠를 정리한 글</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">나이트 루틴에서 입은 룸웨어 브랜드를 특정한 글</a></li>
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">TOWA의 새 캐릭터 '자가이못푸린'을 소개한 글</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">TOWA(하마다 토와)의 위키풍 프로필・경력을 정리한 글</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

KR_SUMMARY = "KO1KEYZ TOWA의 사복 차림이 X에 공개. 모자는 CELINE '트리옹프 리슐리외 캡'(약 86,900엔), 티셔츠는 CELINE의 타이다이 '하트' 무늬(약 154,000엔)로, 두 점에 약 24만 엔의 하이브랜드 코디입니다."

KR_EYECATCH_ID = make_eyecatch(
    ["--top", "TOWA의 사복은 어디 거?", "--main", "KO1KEYZ", "--bottom", "CELINE 모자와 티셔츠!", "--lang", "kr"],
    ROOT / "images" / "towa_celine_private_outfit_eyecatch_kr.png",
)
print("KR_EYECATCH_ID", KR_EYECATCH_ID)

kr_post = post_draft(KR_TITLE, KR_CONTENT, KR_SLUG, "ko", [74, 78, 104], KR_EYECATCH_ID, KR_SUMMARY,
                     translations={"ja": JP_POST_ID})
print("KR_POST_ID", kr_post["id"], kr_post["slug"], kr_post.get("link"))


# ============================== EN ==============================
img_en = build_img_html(
    collage_media,
    "TOWA's off-duty outfit: a green CELINE cap and a tie-dye CELINE tee",
    CAP_EN,
)

EN_TITLE = "TOWA's Off-Duty Outfit Is CELINE: What Do the Cap and Tee Cost?"
EN_SLUG = f"{JP_SLUG}-en"

EN_CONTENT = f"""<!-- wp:paragraph -->
<p>An off-duty photo of KO1KEYZ's TOWA (Towa Hamada) has been going around on X, and fans want to know about the cap and T-shirt he's wearing.<br>
The short answer: <strong>both the cap and the tee are CELINE</strong> — the cap is the Triomphe Richelieu Cap (about 86,900 yen), and the tee is a tie-dye "CELINE PARIS" T-shirt with a red heart (about 154,000 yen).<br>
That's roughly 240,000 yen for just a top and a hat, a very high-end take on casual wear.<br>
This article covers how the outfit surfaced, plus the design, price and where to buy each of the two CELINE pieces.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">What this article covers</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li>How the outfit photo surfaced</li>
<li>The cap (CELINE Triomphe Richelieu Cap): details and price</li>
<li>The tee (CELINE tie-dye heart): details and price</li>
<li>Where to buy each one</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The look: a CELINE outfit shared on X</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>Where it surfaced:</strong> a post from an X account that tracks members' outfits</p>
<p style="margin:4px 0 0 0;"><strong>The look:</strong> a green CELINE cap with a rainbow tie-dye tee</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>The photo making the rounds is a full-length shot of TOWA's outfit, shared by an X account that follows the KO1KEYZ members' private clothes and stage looks.<br>
He pairs a vivid green baseball cap with a tie-dye tee swirling in red, blue, yellow and pink — a loud, colorful combination.<br>
Across the chest, the tee carries the words "CELINE PARIS" in a psychedelic typeface next to a large red heart, which is where the brand hunt started.<br>
The post also lined up the CELINE website product pages for the cap and the tee for reference.</p>
<!-- /wp:paragraph -->

{img_en}

<!-- wp:heading -->
<h2 class="wp-block-heading">The cap: CELINE Triomphe Richelieu Cap</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>Brand:</strong> CELINE</p>
<p style="margin:4px 0 0 0;"><strong>Item:</strong> Triomphe Richelieu Cap in light cotton twill (green)</p>
<p style="margin:4px 0 0 0;"><strong>Reference price:</strong> about 86,900 yen (tax incl.)</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>The green cap TOWA is wearing is one of CELINE's staples, the Triomphe Richelieu Cap.<br>
The front carries CELINE's Triomphe (Arc de Triomphe) motif in a subtle tonal embroidery, and the six-panel crown is cut from light cotton twill.<br>
The "Richelieu" in the name refers to the topstitched, curved brim.<br>
Alongside the core black, white and khaki options, the bright green that TOWA chose is offered as a seasonal color.<br>
The reference price is about 86,900 yen (tax incl.), and it's a current item you can still buy on the CELINE website, at CELINE boutiques and at some department stores.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BUY_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BUY_BAR};color:#fff;">Where to buy the cap (Triomphe Richelieu Cap)</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BUY_BG};">
<li style="margin:0 0 8px 0;"><a href="{CELINE_JP}" target="_blank" rel="noopener">The hats category on the CELINE website (celine.com)</a></li>
<li style="margin:0;"><a href="{BUYMA_CAP}" target="_blank" rel="noopener">Search BUYMA for "CELINE Richelieu Cap"</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The tee: CELINE's tie-dye "heart" T-shirt</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{G_BG};">
<p style="margin:0;"><strong>Brand:</strong> CELINE (Hedi Slimane era)</p>
<p style="margin:4px 0 0 0;"><strong>Item:</strong> tie-dye "CELINE PARIS" T-shirt in ribbed cotton jersey</p>
<p style="margin:4px 0 0 0;"><strong>Reference price:</strong> about 154,000 yen — now mostly resale</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>The tee is also CELINE: a slim-fit crew neck in ribbed cotton jersey with an all-over rainbow tie-dye.<br>
The graphic — a red heart and a wavy "CELINE PARIS" logo layered over the swirling tie-dye — is close in feel to the tie-dye run from CELINE HOMME around 2021, the collection often nicknamed "Dancing Kid," designed by Hedi Slimane.<br>
The reference price is said to be around 154,000 yen, but as a collection from a few years back it is no longer part of CELINE's current lineup.<br>
These days it turns up at vintage and resale shops and on overseas secondhand sites, where prices swing widely with condition and size, starting from somewhere around 100,000 yen.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {BUY_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BUY_BAR};color:#fff;">Where to buy the tee (CELINE tie-dye heart)</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BUY_BG};">
<li style="margin:0 0 8px 0;"><a href="{BUYMA_TEE}" target="_blank" rel="noopener">Search BUYMA for "CELINE tie-dye T-shirt"</a></li>
<li style="margin:0 0 8px 0;"><a href="{VESTIAIRE_TEE}" target="_blank" rel="noopener">Search Vestiaire Collective for "celine tie dye t-shirt"</a></li>
<li style="margin:0;"><a href="{GRAILED_TEE}" target="_blank" rel="noopener">Grailed's CELINE T-shirt listings</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Is this TOWA's own?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>There's no official word from TOWA or the label about this outfit, so nothing confirms the pieces are his own.<br>
That said, the photo is circulating as everyday wear rather than a stage look, so it's likely TOWA picked these out himself as street clothes.<br>
He has worn plenty of high-end pieces before, including the <a href="{L_GIVENCHY}" target="_blank" rel="noopener">GIVENCHY "4G" graphic tee</a> from his dance video with SIYOUNG, and he's known among fans for being into fashion.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Summary</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>An off-duty photo of TOWA went around on X, with both the cap and tee turning out to be CELINE</li>
<li>The cap is CELINE's Triomphe Richelieu Cap (green), reference price about 86,900 yen, a current item</li>
<li>The tee is CELINE's tie-dye "heart" design (Hedi Slimane era, around 2021), reference price about 154,000 yen, now mostly resale</li>
<li>Together the two pieces come to roughly 240,000 yen</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Carrying an outfit worth more than 200,000 yen without letting it look flashy says a lot about TOWA's eye for clothes.<br>
The green cap is still available, so if you want to borrow even a little of the vibe, it's worth a look on the official site!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">More on TOWA (Towa Hamada)</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">Identifying the GIVENCHY "4G" tee from his dance video with SIYOUNG</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">Identifying the brand of the loungewear from his night routine</a></li>
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">A look at TOWA's new character "Jagaimoppurin"</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">A wiki-style profile and career rundown for TOWA (Towa Hamada)</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

EN_SUMMARY = "An off-duty photo of KO1KEYZ's TOWA is going around on X. The cap is CELINE's Triomphe Richelieu Cap (about 86,900 yen) and the tee is CELINE's tie-dye \"CELINE PARIS\" heart T-shirt (about 154,000 yen) - roughly 240,000 yen for the pair."

en_post = post_draft(EN_TITLE, EN_CONTENT, EN_SLUG, "en", [110, 114], JP_EYECATCH_ID, EN_SUMMARY,
                     translations={"ja": JP_POST_ID})
print("EN_POST_ID", en_post["id"], en_post["slug"], en_post.get("link"))

print("\n=== DONE ===")
print("JP", JP_POST_ID, f"{WP_URL}/wp-admin/post.php?post={JP_POST_ID}&action=edit")
print("KR", kr_post["id"], f"{WP_URL}/wp-admin/post.php?post={kr_post['id']}&action=edit")
print("EN", en_post["id"], f"{WP_URL}/wp-admin/post.php?post={en_post['id']}&action=edit")
