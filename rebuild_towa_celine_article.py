# -*- coding: utf-8 -*-
"""Full rebuild of the TOWA CELINE outfit article body (JP 12125 / KR 12127 /
EN 12128). The look was shown on Plus Message (プラチャ); do NOT lean on the
outfit-tracking X post or its collage image. Only the legit Plus-Chat two-shot
(media 12174) is embedded."""
import base64, json, os
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}
HJ = {**H, "Content-Type": "application/json"}

SHOT_MEDIA_ID = 12174
COLLAGE_MEDIA_ID = 12123  # fan compilation - drop it
SOURCE_TWEET = "https://x.com/girlyoshiki/status/2095169972456525922"

G_BORDER, G_BG = "#9bc96e", "#f5faec"
BUY_BORDER, BUY_BAR, BUY_BG = "#ddd9d3", "#8a8378", "#f7f6f4"

L_GIVENCHY = "https://chomoand-1.com/towa-givenchy-tshirt-siyoung-dance-11855"
L_LOUNGE = "https://chomoand-1.com/what-brand-is-towas-loungewear-11093"
L_JAGAIMO = "https://chomoand-1.com/is-towas-new-character-jagaimo-11691"
L_WIKI = "https://chomoand-1.com/hamadatowa_wiki-2452"
L_PRACHA = "https://chomoand-1.com/what-is-ko1keyz-pracha-how-to-11497"

CELINE_JP = "https://www.celine.com/ja-jp/celine-men/accessoire/casquettes-et-accessoires-souples/"
BUYMA_CAP = "https://www.buyma.com/r/_CELINE-%E3%82%BB%E3%83%AA%E3%83%BC%E3%83%8C/keyword-" + quote("リシュリュー キャップ") + "/"
BUYMA_TEE = "https://www.buyma.com/r/_CELINE-%E3%82%BB%E3%83%AA%E3%83%BC%E3%83%8C/keyword-" + quote("タイダイ Tシャツ") + "/"
VESTIAIRE_TEE = "https://www.vestiairecollective.com/search/?q=" + quote("celine tie dye t-shirt")
GRAILED_TEE = "https://www.grailed.com/designers/celine/t-shirts"

shot = requests.get(f"{WP}/wp-json/wp/v2/media/{SHOT_MEDIA_ID}", headers=H).json()


def img_html(media, alt, caption):
    sizes = media.get("media_details", {}).get("sizes", {})
    fu = media["source_url"]; fw = media["media_details"]["width"]; fh = media["media_details"]["height"]
    lg = sizes.get("large", {"source_url": fu, "width": fw})
    md = sizes.get("medium", {"source_url": fu, "width": fw})
    w = lg["width"]; h = int(w * fh / fw)
    srcset = f'{md["source_url"]} {md["width"]}w, {lg["source_url"]} {lg["width"]}w, {fu} {fw}w'
    return (f'<!-- wp:html -->\n<figure class="wp-block-image size-large">\n'
            f'<img src="{lg["source_url"]}" alt="{alt}" width="{w}" height="{h}"\n'
            f'  style="max-width:100%;height:auto;"\n  srcset="{srcset}"\n'
            f'  sizes="(max-width: {w}px) 100vw, {w}px">\n'
            f'<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>\n'
            f'</figure>\n<!-- /wp:html -->')


IMG_JP = img_html(shot, "プライベートの食事で緑のCELINEキャップとタイダイTシャツを着たTOWA",
                  f'出典:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>')
IMG_KR = img_html(shot, "사적인 식사에서 그린 CELINE 캡과 타이다이 티셔츠를 입은 TOWA",
                  f'출처:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>')
IMG_EN = img_html(shot, "TOWA wearing the green CELINE cap and tie-dye tee at a private meal",
                  f'Source:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>')


# ================================================================= JP
JP = f"""<!-- wp:paragraph -->
<p>KO1KEYZのTOWA(濱田永遠)さんがプラスメッセージ(通称プラチャ)で見せた私服コーデが話題になり、身につけていた帽子とTシャツに注目が集まっています。<br>
結論から書くと、<strong>帽子もTシャツもどちらも「CELINE(セリーヌ)」のアイテム</strong>で、帽子が「トリオンフ リシュリュー キャップ」(参考価格 約86,900円)、Tシャツがタイダイ柄に赤いハートを配した「CELINE PARIS」Tシャツ(参考価格 約154,000円)とみられます。<br>
トップスと帽子だけで合わせておよそ24万円という、ハイブランドらしい私服コーデです。<br>
この記事では、CELINEの2アイテムそれぞれのデザイン・価格・買える場所をまとめます。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li>帽子(CELINE トリオンフ リシュリュー キャップ)の特徴と価格</li>
<li>Tシャツ(CELINE タイダイ ハート柄)の特徴と価格</li>
<li>それぞれどこで買えるか</li>
<li>これはTOWAの私物なのか</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">どんなコーデ?プラチャで見せた私服</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>このコーデは、TOWAさんがプラチャ(プラスメッセージ)で届けた、メンバーとの食事のワンシーンの写真で確認できます。<br>
鮮やかなグリーンのベースボールキャップに、赤・青・黄・ピンクが渦を巻くタイダイ柄のTシャツを合わせた、色数の多いスタイルです。<br>
Tシャツの胸元には、サイケデリックな書体の「CELINE PARIS」と大きな赤いハートがプリントされています。<br>
プラチャは、メンバーが1対1のトーク画面のような形でメッセージや写真を届けてくれる有料サービスです(仕組みは<a href="{L_PRACHA}" target="_blank" rel="noopener">プラチャの料金・使い方をまとめた記事</a>で解説しています)。</p>
<!-- /wp:paragraph -->

{IMG_JP}

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
<p>グリーンのキャップは、CELINEの定番「トリオンフ リシュリュー キャップ」です。<br>
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
ただ、プラチャではメンバーとのプライベートな食事の場でも同じコーデで出かけている様子が見られ、ステージ衣装ではなくTOWAさん自身が私服として愛用しているアイテムとみて良さそうです。<br>
TOWAさんはこれまでも、SIYOUNGさんとのダンス動画で着ていた<a href="{L_GIVENCHY}" target="_blank" rel="noopener">GIVENCHYの「4G」グラフィックTシャツ</a>など、ハイブランドの服をたびたび身につけており、ファッション好きな一面が知られています。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">まとめ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>TOWAがプラチャで見せた私服コーデが、帽子もTシャツもCELINEだと話題に</li>
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
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">SHINHAENGの靴に描いた新キャラ「じゃがいもっぷりん」を紹介した記事</a></li>
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">SIYOUNGとのダンス動画で着ていたGIVENCHY「4G」Tシャツを特定した記事</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">ナイトルーティンで着ていたルームウェアのブランドを特定した記事</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">TOWA(濱田永遠)のwiki風プロフィール・経歴をまとめた記事</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

JP_SUMMARY = "KO1KEYZ・TOWAがプラチャで見せた私服コーデが話題。帽子はCELINE「トリオンフ リシュリュー キャップ」(約86,900円)、TシャツはCELINEのタイダイ「ハート」柄(約154,000円)で、2点でおよそ24万円のコーデでした。"


# ================================================================= KR
KR = f"""<!-- wp:paragraph -->
<p>KO1KEYZ의 TOWA(하마다 토와)가 플러스 메시지(통칭 플러스챗)에서 보여준 사복 코디가 화제가 되며, 쓰고 입은 모자와 티셔츠에 관심이 쏠리고 있습니다.<br>
결론부터 말하면, <strong>모자도 티셔츠도 모두 'CELINE(셀린느)' 아이템</strong>으로, 모자는 '트리옹프 리슐리외 캡'(참고가 약 86,900엔), 티셔츠는 타이다이 무늬에 빨간 하트를 넣은 'CELINE PARIS' 티셔츠(참고가 약 154,000엔)로 보입니다.<br>
상의와 모자만으로 합쳐서 약 24만 엔이라는, 하이브랜드다운 사복 코디입니다.<br>
이 글에서는 CELINE 두 아이템 각각의 디자인・가격・살 수 있는 곳을 정리합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">이 글에서 알 수 있는 것</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li>모자(CELINE 트리옹프 리슐리외 캡)의 특징과 가격</li>
<li>티셔츠(CELINE 타이다이 하트 무늬)의 특징과 가격</li>
<li>각각 어디서 살 수 있는지</li>
<li>이건 TOWA의 사물인지</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">어떤 코디? 플러스챗에서 보여준 사복</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>이 코디는 TOWA가 플러스챗(플러스 메시지)으로 보낸, 멤버와의 식사 한 장면 사진에서 확인할 수 있습니다.<br>
선명한 그린 베이스볼 캡에, 빨강・파랑・노랑・핑크가 소용돌이치는 타이다이 무늬 티셔츠를 매치한, 색이 많은 스타일입니다.<br>
티셔츠 가슴 부분에는 사이키델릭한 서체의 'CELINE PARIS'와 큰 빨간 하트가 프린트되어 있습니다.<br>
플러스챗은 멤버가 1대1 대화창 같은 형태로 메시지와 사진을 보내 주는 유료 서비스입니다(구조는 <a href="{L_PRACHA}" target="_blank" rel="noopener">플러스챗 요금・사용법을 정리한 글</a>에서 설명합니다).</p>
<!-- /wp:paragraph -->

{IMG_KR}

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
<p>그린 캡은 CELINE의 스테디셀러 '트리옹프 리슐리외 캡'입니다.<br>
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
다만 플러스챗에서 멤버와의 사적인 식사 자리에서도 같은 코디로 나온 모습이 보여, 무대 의상이 아니라 TOWA 본인이 사복으로 애용하는 아이템으로 봐도 좋을 듯합니다.<br>
TOWA는 지금까지도 SIYOUNG과의 댄스 영상에서 입었던 <a href="{L_GIVENCHY}" target="_blank" rel="noopener">GIVENCHY의 '4G' 그래픽 티셔츠</a> 등, 하이브랜드 옷을 자주 착용해 와서 패션을 좋아하는 면모가 알려져 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">정리</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>TOWA가 플러스챗에서 보여준 사복 코디가 모자도 티셔츠도 CELINE이라고 화제</li>
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
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">SHINHAENG의 신발에 그린 새 캐릭터 '자가이못푸린'을 소개한 글</a></li>
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">SIYOUNG과의 댄스 영상에서 입은 GIVENCHY '4G' 티셔츠를 특정한 글</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">나이트 루틴에서 입은 룸웨어 브랜드를 특정한 글</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">TOWA(하마다 토와)의 위키풍 프로필・경력을 정리한 글</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

KR_SUMMARY = "KO1KEYZ TOWA가 플러스챗에서 보여준 사복 코디가 화제. 모자는 CELINE '트리옹프 리슐리외 캡'(약 86,900엔), 티셔츠는 CELINE의 타이다이 '하트' 무늬(약 154,000엔)로, 두 점에 약 24만 엔의 코디입니다."


# ================================================================= EN
EN = f"""<!-- wp:paragraph -->
<p>An off-duty look KO1KEYZ's TOWA (Towa Hamada) showed on Plus Message (nicknamed "Plus Chat") has fans asking about the cap and T-shirt he's wearing.<br>
The short answer: <strong>both the cap and the tee are CELINE</strong> — the cap is the Triomphe Richelieu Cap (about 86,900 yen), and the tee is a tie-dye "CELINE PARIS" T-shirt with a red heart (about 154,000 yen).<br>
That's roughly 240,000 yen for just a top and a hat, a very high-end take on casual wear.<br>
This article covers the design, price and where to buy each of the two CELINE pieces.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_BORDER};color:#fff;">What this article covers</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li>The cap (CELINE Triomphe Richelieu Cap): details and price</li>
<li>The tee (CELINE tie-dye heart): details and price</li>
<li>Where to buy each one</li>
<li>Whether these are TOWA's own</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The look: an outfit shown on Plus Chat</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>You can see this outfit in a photo TOWA sent through Plus Chat (Plus Message), a snapshot from a meal with a member.<br>
He pairs a vivid green baseball cap with a tie-dye tee swirling in red, blue, yellow and pink — a busy, colorful combination.<br>
Across the chest, the tee is printed with "CELINE PARIS" in a psychedelic typeface next to a large red heart.<br>
Plus Chat is a paid service where members send messages and photos in what looks like a one-on-one chat window (we explain how it works in our <a href="{L_PRACHA}" target="_blank" rel="noopener">guide to Plus Chat's price and how to use it</a>).</p>
<!-- /wp:paragraph -->

{IMG_EN}

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
<p>The green cap is one of CELINE's staples, the Triomphe Richelieu Cap.<br>
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
<h2 class="wp-block-heading">Are these TOWA's own?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>There's no official word from TOWA or the label about this outfit, so nothing confirms the pieces are his own.<br>
Still, Plus Chat shows him in the same outfit for a private meal with a member, so it's fair to read these as pieces TOWA genuinely favors off duty rather than stage wear.<br>
He has worn plenty of high-end pieces before, including the <a href="{L_GIVENCHY}" target="_blank" rel="noopener">GIVENCHY "4G" graphic tee</a> from his dance video with SIYOUNG, and he's known among fans for being into fashion.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Summary</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>An off-duty look TOWA showed on Plus Chat turned out to be all CELINE, cap and tee</li>
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
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">The new character "Jagaimoppurin" he drew on SHINHAENG's shoe</a></li>
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">Identifying the GIVENCHY "4G" tee from his dance video with SIYOUNG</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">Identifying the brand of the loungewear from his night routine</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">A wiki-style profile and career rundown for TOWA (Towa Hamada)</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

EN_SUMMARY = 'An off-duty look KO1KEYZ\'s TOWA showed on Plus Chat has fans talking. The cap is CELINE\'s Triomphe Richelieu Cap (about 86,900 yen) and the tee is CELINE\'s tie-dye "CELINE PARIS" heart T-shirt (about 154,000 yen) - roughly 240,000 yen for the pair.'


BODY = {12125: (JP, JP_SUMMARY), 12127: (KR, KR_SUMMARY), 12128: (EN, EN_SUMMARY)}
for pid, (content, summary) in BODY.items():
    r = requests.post(f"{WP}/wp-json/wp/v2/posts/{pid}", headers=HJ,
                      data=json.dumps({"content": content, "status": "draft",
                                       "meta": {"jetpack_publicize_message": summary}}).encode("utf-8"))
    r.raise_for_status()
    print("rebuilt", pid, r.status_code, f"{WP}/wp-admin/post.php?post={pid}&action=edit")

# drop the unused fan-collage image
r = requests.delete(f"{WP}/wp-json/wp/v2/media/{COLLAGE_MEDIA_ID}?force=true", headers=H)
print("deleted collage media", COLLAGE_MEDIA_ID, r.status_code)
print("DONE")
