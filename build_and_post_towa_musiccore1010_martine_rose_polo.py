# -*- coding: utf-8 -*-
"""TOWAが2026-10-10のMBC「ショー！音楽中心」の日に着ていた衣装のポロ=Martine Rose Oversized Polo (Grey Black Stripe) 674JE09059。
写真: 公式X https://x.com/KO1KEYZofficial/status/2108829636817813744 (音楽中心お礼、赤い壁の前) → blockquote埋め込み
      公式TikTok https://www.tiktok.com/@ko1keyzofficial/video/7695000081384164626 (10/10 20:30公開、'KO1KEYZ'(Korean ver.)
      SHINHAENG SIYOUNG TOWA YOSHIKI YUKI YURA、体育館セット) → 28.5〜29.0秒のフレームを切り出し
裏取り: Naked(nakedcph.com) vendoritemno:674JE09059 の商品写真と照合(赤い三角+martineロゴ・MARTINE SPORT 20/07 ROSEの紋章・
        青い「TOTAL participation」刺しゅう・黒襟+赤い裏・パイル地のボーダー)。
        SS26(Machine-A/Family 3.0/Jentestore)、ポルトガル製(Jentestore/Ekseption)、綿85%・ポリエステル15%(Machine-A/Family 3.0)。
        価格: FWRD 555ドル、Jentestore 정가783,000원→425,000원(品切れ)、Naked 2,800DKK→1,680DKK(10-12時点でS在庫あり)。
        公式ストア(martine-rose.com)には10-12時点で掲載なし。ナパピリコラボのEGOポロ(鹿の子・別物)と混同しない。
"""
from pathlib import Path

import cv2
from PIL import Image

from _mubank1009_helpers import ROOT, WP_URL, wp_upload, img_html, post_draft, make_eyecatch, h2, p, UI

# TOWA公式メンバーカラー(黄緑)に寄せたパステル配色(既存TOWA記事14407・バレンシアガ記事と統一)
ui = UI(AB="#d7e7bf", AL="#6fa843", BG="#f5f9ed", TH="#e6f0d8", marker="mark_green")

SRC_X = "https://x.com/KO1KEYZofficial/status/2108829636817813744"
SRC_TT = "https://www.tiktok.com/@ko1keyzofficial/video/7695000081384164626"
VIDEO = Path(r"C:\Users\s30se\AppData\Local\Temp\claude\c--Users-s30se-OneDrive--------CHOMO\9f7d6c19-dad5-4a45-b1b7-fe576668dc5f\scratchpad\towa1012\tt\v.mp4")

NAKED = "https://nakedcph.com/products/martine-rose-oversized-polo-grey-black-stripe-gry-674je09059"
FWRD = "https://www.fwrd.com/product-martine-rose-oversized-polo-in-grey-black-stripe/MROS-MS59/?d=Mens"
JENTE = "https://jentestore.com/goods/view?no=2595940"
MR = "https://www.martine-rose.com/"

OFFICIAL_EMBED = """<!-- wp:html -->
<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><a href="https://twitter.com/KO1KEYZofficial/status/2108829636817813744">https://twitter.com/KO1KEYZofficial/status/2108829636817813744</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
<!-- /wp:html -->"""

JP_REL = [
    ("https://chomoand-1.com/towa-music-bank-celine-velvet-track-jacket-14407", "TOWAのミュージックバンク出勤の私服(セリーヌ×クロムハーツ)の記事"),
    ("https://chomoand-1.com/towa-gimpo-airport-chrome-hearts-hoodie-14289", "TOWAが金浦空港で着ていたクロムハーツのパーカーの記事"),
    ("https://chomoand-1.com/towa-private-celine-cap-tshirt-12125", "TOWAの私服(CELINEの帽子とTシャツ)の値段を調べた記事"),
    ("https://chomoand-1.com/towa-chrome-hearts-nail-ring-12200", "TOWAが自撮りで着けていたクロムハーツのリングの記事"),
    ("https://chomoand-1.com/hamadatowa_wiki-2452", "TOWA(濱田永遠)のwiki風プロフィール・経歴の記事"),
]
KR_REL = [
    ("https://chomoand-1.com/ko/towa-music-bank-celine-velvet-track-jacket-kr-14409", "TOWA 뮤직뱅크 출근길 사복(셀린느×크롬하츠) 글"),
    ("https://chomoand-1.com/ko/towa-gimpo-airport-chrome-hearts-hoodie-kr-14291", "TOWA가 김포공항에서 입은 크롬하츠 후드 글"),
    ("https://chomoand-1.com/ko/towa-private-celine-cap-tshirt-kr-12127", "TOWA의 사복(CELINE 모자와 티셔츠) 가격 글"),
    ("https://chomoand-1.com/ko/towa-chrome-hearts-nail-ring-kr-12201", "TOWA가 셀카에서 낀 크롬하츠 반지 글"),
]
EN_REL = [
    ("https://chomoand-1.com/en/towa-music-bank-celine-velvet-track-jacket-en-14410", "TOWA's Music Bank commute outfit (CELINE × Chrome Hearts)"),
    ("https://chomoand-1.com/en/towa-gimpo-airport-chrome-hearts-hoodie-en-14292", "TOWA's Chrome Hearts hoodie at Gimpo Airport"),
    ("https://chomoand-1.com/en/towa-private-celine-cap-tshirt-en-12128", "TOWA's off-duty CELINE cap and tee"),
    ("https://chomoand-1.com/en/towa-chrome-hearts-nail-ring-en-12202", "The Chrome Hearts ring TOWA wore in his selfie"),
]


# ---------- 公式TikTokから本文用の2枚を切り出す ----------
def frame_at(sec):
    cap = cv2.VideoCapture(str(VIDEO))
    cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    ok, fr = cap.read()
    cap.release()
    if not ok:
        raise RuntimeError(f"frame at {sec}s not readable")
    return Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))


img_dir = ROOT / "images"
p_group = img_dir / "towa_musiccore1010_tiktok_group.jpg"
p_towa = img_dir / "towa_musiccore1010_martine_rose_polo.jpg"
frame_at(28.5).crop((0, 160, 1080, 1760)).save(p_group, quality=90)
frame_at(29.0).crop((0, 640, 640, 1500)).save(p_towa, quality=92)

m_group = wp_upload(p_group, "image/jpeg")
m_towa = wp_upload(p_towa, "image/jpeg")
print("MEDIA", m_group["id"], m_towa["id"])

# ============================== JP ==============================
JP_TITLE = "【TOWA】音楽中心の衣装ポロはマーティンローズ！値段は？"
JP_SLUG = "towa-music-core-martine-rose-stripe-polo"

JP_CONTENT = "\n\n".join([
    p("2026年10月10日、KO1KEYZ(コイキーズ)は韓国MBCの音楽番組「ショー！音楽中心」に出演しました。<br>\n"
      "その日に公式Xが公開したTOWAの写真で、グレーのボーダーに青い「TOTAL」の文字が入ったポロシャツが気になった人も多いのではないでしょうか。<br>\n"
      "このポロは、<strong>ロンドンのブランド「Martine Rose(マーティン・ローズ)」の2026年春夏の「Oversized Polo(グレー×ブラックストライプ)」</strong>です。<br>\n"
      "海外の定価は<strong>555ドル(1ドル150円換算で約8万3,000円)</strong>で、今はセールで4割ほど安く買えるショップもあります。<br>\n"
      "見分けるポイント、素材やサイズ感、どこで買えるかまで順番に紹介します。"),
    ui.infobox("TOWAが着ていたポロシャツ", [
        ("シーン", "2026年10月10日 MBC「ショー！音楽中心」出演日の公式写真、同日公開の公式TikTok"),
        ("ブランド", "Martine Rose(マーティン・ローズ)"),
        ("商品名", "Oversized Polo(Grey Black Stripe)"),
        ("品番", "674JE09059"),
        ("シーズン", "2026年春夏(SS26)"),
        ("価格", "定価555ドル(約8万3,000円)、セールで1,680デンマーククローネ(約3万9,000円)など"),
    ]),
    ui.knowbox("この記事でわかること", ["TOWAが着ていたポロシャツ", "マーティン・ローズと分かるポイント", "素材とサイズ感", "マーティン・ローズはどんなブランド？", "値段と購入先"]),

    h2("音楽中心の日にTOWAが着ていたポロシャツは？"),
    ui.minibox([("アイテム：", "グレー×黒×白のボーダーのポロシャツ"), ("登場：", "公式Xの音楽中心お礼写真+公式TikTok")]),
    p("音楽番組に出演すると、KO1KEYZの公式Xはメンバー1人ずつの写真を「감사합니다！(ありがとうございました)」の言葉と一緒に公開しています。<br>\n"
      "10月10日の音楽中心の回で、TOWAは深い赤の壁の前で手を猫の爪のように曲げたポーズを見せていました。<br>\n"
      "着ていたのは、グレーの地に黒と白の線がランダムに走るボーダーのポロシャツです。"),
    OFFICIAL_EMBED,
    p(f"首元は黒い襟で、合わせの内側にだけ赤い布がのぞいています。<br>\n"
      f"中には白いTシャツを重ね、ゆったりした身幅と、ひじまで届く長めの袖でラフに着こなしていました。<br>\n"
      f"胸には{ui.mark('赤い三角のロゴ、右胸の丸い紋章、真ん中の青い「TOTAL」の刺しゅう', True)}が並び、90年代のサッカーのユニフォームのような雰囲気です。"),
    p("同じ日の夜には、公式TikTokで「KO1KEYZ」(Korean ver.)のダンス動画も公開されました。<br>\n"
      "SHINHAENG・SIYOUNG・TOWA・YOSHIKI・YUKI・YURAの6人が、「KO1KEYZ」の横断幕がかかった体育館で踊る動画です。<br>\n"
      "6人ともラグビーシャツやサッカーシャツ風のトップスにデニムを合わせていて、TOWAもこのポロに淡い色のワイドデニムと白いスニーカーで登場しています。"),
    img_html(m_group, "体育館で「KO1KEYZ」(Korean ver.)を踊るメンバー6人。左端のTOWAはグレーのボーダーのポロシャツ", f"出典：{SRC_TT}"),
    p("公式写真にも公式TikTokにも同じポロで登場していて、この日の「KO1KEYZ」の活動のために用意された衣装です。<br>\n"
      "ほかの5人もラグビーシャツやサッカーシャツ風のトップスでそろえていて、体育館のセットとあわせて「スポーツチーム」のようなコンセプトになっていました。"),

    h2("どうしてマーティン・ローズと分かる？見分けポイントは？"),
    ui.minibox([("ポイント①：", "赤い三角+「martine」のロゴ"), ("ポイント②：", "「MARTINE SPORT」の紋章"), ("ポイント③：", "青い「TOTAL participation」の刺しゅう")]),
    p("TikTokの動画では、TOWAがカメラに近づく場面で胸元のロゴがはっきり映ります。<br>\n"
      "かがんでポーズを決めた瞬間に、赤いロゴと青い刺しゅう、紋章が一度にとらえられていました。"),
    img_html(m_towa, "TikTokの動画でポーズを決めるTOWA。胸に赤い三角のロゴと青いTOTALの刺しゅう", f"出典：{SRC_TT}"),
    ui.barbox("マーティン・ローズの商品写真と一致したポイント", [
        "<strong>左胸のロゴ</strong>：赤い三角のマークの下に、赤い文字で「martine」",
        "<strong>右胸の紋章</strong>：王冠の下に「MARTINE」「SPORT」、白黒の縦じまの盾、左右に「20」「07」、下に「ROSE」",
        "<strong>胸の刺しゅう</strong>：太い青の「TOTAL」と、その下の弧の中に「participation」",
        "<strong>襟と生地</strong>：黒い襟と赤い裏地、ふわっとしたパイル地のグレー×黒×白のボーダー",
    ], ordered=True),
    p(f"この4つが、海外のセレクトショップに並ぶ{ui.mark('品番674JE09059の「Oversized Polo(Grey Black Stripe)」', True)}の商品写真とすべてそろいました。<br>\n"
      "ボーダーの太さや線の途切れ方までよく似ているので、同じ商品と考えてよいでしょう。<br>\n"
      "紋章の「20」「07」は、マーティン・ローズがブランドを立ち上げた2007年を指しています。"),
    p("ちなみに、マーティン・ローズにはナパピリ(Napapijri)とのコラボで作った「EGO S/S POLO SHIRT」という、同じグレー×黒のボーダーのポロもあります。<br>\n"
      "ただ、こちらは鹿の子(ポロシャツによくある凹凸のある生地)で、胸に「TOTAL」の刺しゅうや紋章はありません。<br>\n"
      "色だけで探すと間違えやすいので、ロゴの有無を確かめるのがおすすめです。"),

    h2("素材やサイズ感は？"),
    ui.minibox([("素材：", "綿85%・ポリエステル15%"), ("生産：", "ポルトガル製"), ("シルエット：", "ゆったりしたオーバーサイズ")]),
    p(f"海外のショップの表記によると、素材は{ui.mark('綿85%・ポリエステル15%', True)}で、ポルトガルで作られています。<br>\n"
      "写真で見ると生地の表面がタオルのようにふわっとしていて、ベロアに近いパイル地のような質感です。<br>\n"
      "光の当たり方でボーダーの白がやわらかく見えるのも、この生地ならではでしょう。"),
    p("商品名のとおり、身幅が広くて肩が落ちるオーバーサイズのつくりです。<br>\n"
      "TOWAが着ると袖がひじの下まで来て、裾もお尻がかくれるくらいの長さになっていました。<br>\n"
      "ジャストサイズで着たい人は、ふだんより1サイズ下げるのもひとつの手です。"),
    p("襟は黒の無地で、前立ての内側は赤です。<br>\n"
      "ボタンは表から見えないように隠されていて、すっきりした首元に仕上がっています。"),

    h2("マーティン・ローズはどんなブランド？"),
    ui.minibox([("創業：", "2007年、ロンドン"), ("デザイナー：", "マーティン・ローズ"), ("得意なもの：", "サッカーや90年代のストリートを元にした服")]),
    p("マーティン・ローズは、イギリス・ロンドンを拠点にするデザイナー、マーティン・ローズ本人の名前をつけたブランドです。<br>\n"
      "2007年に始まり、ロンドンのクラブ文化やサッカーのユニフォーム、90年代のストリートの空気を取り入れた服で知られています。<br>\n"
      "わざと大きく作ったシルエットや、スポーツブランドのようなロゴ使いが持ち味です。"),
    p("バレンシアガのメンズのデザインに関わったことや、ナイキとのコラボスニーカー「Shox MR4」でも話題になりました。<br>\n"
      "今回のポロも、架空のスポーツブランドのような三角のロゴや、チームのエンブレム風の紋章をのせた、ブランドらしい1着です。<br>\n"
      "TOWAのくしゃっとした金髪と合わせると、サッカー少年のような親しみやすさが出ていました。"),

    h2("値段は？どこで買える？"),
    ui.minibox([("定価：", "555ドル(約8万3,000円)"), ("セール：", "1,680デンマーククローネ(約3万9,000円)など")]),
    p(f"アメリカの通販サイトFWRDでは、{ui.mark('定価555ドル(1ドル150円換算で約8万3,000円)', True)}で掲載されていました。<br>\n"
      "韓国のセレクトショップJentestoreの定価は関税込みで783,000ウォンで、セールで425,000ウォンまで下がっていましたが、今は品切れです。"),
    p("2026年10月12日時点でいちばん手が届きやすいのは、デンマークのショップNakedです。<br>\n"
      "定価2,800デンマーククローネのところ、4割引きの1,680デンマーククローネ(1クローネ23円換算で約3万9,000円)になっていて、Sサイズに在庫がありました。<br>\n"
      "海外からの取り寄せになるので、送料や関税は別にかかり、日本への配送条件は注文前に確認してください。"),
    p("マーティン・ローズの公式オンラインストアには、10月12日時点でこのポロは並んでいませんでした。<br>\n"
      "セールで動いているサイズはすぐなくなりやすいので、気になる人は早めにチェックしておくと安心です。"),
    ui.barbox("購入先・価格を確認できるページ", [
        f'<a href="{NAKED}" target="_blank" rel="noopener">Naked(デンマーク)</a>：1,680デンマーククローネ(定価2,800クローネ)、Sサイズに在庫あり',
        f'<a href="{FWRD}" target="_blank" rel="noopener">FWRD(アメリカ)</a>：定価555ドル',
        f'<a href="{JENTE}" target="_blank" rel="noopener">Jentestore(韓国)</a>：定価783,000ウォン→425,000ウォン(品切れ)',
        f'<a href="{MR}" target="_blank" rel="noopener">マーティン・ローズ公式オンラインストア</a>：新作のチェックに',
    ]),

    h2("まとめ"),
    ui.summarybox([
        "TOWAが2026年10月10日の音楽中心の日に着ていたのは、マーティン・ローズの「Oversized Polo(Grey Black Stripe)」",
        "品番は674JE09059、2026年春夏のアイテム",
        "決め手は赤い三角のmartineロゴ、MARTINE SPORTの紋章、青いTOTALの刺しゅう",
        "素材は綿85%・ポリエステル15%のパイル地で、ポルトガル製",
        "定価は555ドル(約8万3,000円)、セールなら約3万9,000円で買えるショップも",
    ]),
    p("公式写真でもTikTokでも、ボーダーと青いロゴがよく映えていました。<br>\n"
      "サイズが残っているうちに、TOWAとおそろいのサッカー風ポロをチェックしてみてください！"),
    ui.linkbox("TOWA・KO1KEYZの関連記事", JP_REL),
])

JP_SUMMARY = ("TOWAが10月10日の音楽中心の日に着ていたグレーのボーダーのポロシャツは、マーティン・ローズの"
              "「Oversized Polo(Grey Black Stripe)」(674JE09059)です。定価555ドル、セールで約3万9,000円のショップもあります。")

JP_EYECATCH_ID = make_eyecatch(
    ["--top", "TOWAの衣装ポロはどこの？", "--main", "KO1KEYZ", "--bottom", "マーティンローズ！"],
    ROOT / "images" / "towa_musiccore1010_polo_eyecatch.png",
)
print("JP_EYECATCH_ID", JP_EYECATCH_ID)
jp_post = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, "ja", [66, 63, 104], JP_EYECATCH_ID, JP_SUMMARY)
JP_POST_ID = jp_post["id"]
print("JP_POST_ID", JP_POST_ID, jp_post["slug"])

# ============================== KR ==============================
KR_TITLE = "【TOWA】음악중심 의상 폴로는 마틴로즈! 가격은?"
KR_SLUG = f"{JP_SLUG}-kr"

KR_CONTENT = "\n\n".join([
    p("2026년 10월 10일, KO1KEYZ는 MBC '쇼! 음악중심'에 출연했습니다.<br>\n"
      "이날 공식 X가 공개한 TOWA 사진 속, 회색 스트라이프에 파란 'TOTAL' 글자가 들어간 폴로 셔츠가 눈에 띄었습니다.<br>\n"
      "이 폴로는 <strong>런던 브랜드 'Martine Rose(마틴 로즈)'의 2026 S/S 'Oversized Polo(그레이 블랙 스트라이프)'</strong>입니다.<br>\n"
      "해외 정가는 <strong>555달러</strong>이며, 지금은 40% 정도 할인 판매하는 매장도 있습니다."),
    ui.infobox("TOWA가 입은 폴로 셔츠", [
        ("장면", "2026년 10월 10일 MBC '쇼! 음악중심' 출연일 공식 사진, 같은 날 공개된 공식 틱톡"),
        ("브랜드", "Martine Rose(마틴 로즈)"),
        ("상품명", "Oversized Polo(Grey Black Stripe)"),
        ("품번", "674JE09059"),
        ("시즌", "2026 S/S"),
        ("가격", "정가 555달러, 한국 정가 783,000원(관부가세 포함)"),
    ]),
    h2("음악중심 날 TOWA가 입은 폴로 셔츠는?"),
    ui.minibox([("아이템: ", "회색×검정×흰색 스트라이프 폴로 셔츠"), ("등장: ", "공식 X 음악중심 감사 사진+공식 틱톡")]),
    p("10월 10일 음악중심 회차에서 TOWA는 진한 빨간 벽 앞에서 고양이 발톱 같은 포즈를 취했습니다.<br>\n"
      "검은 칼라에 안쪽만 빨간 원단이 보이고, 흰 티셔츠를 겹쳐 넉넉하게 입었습니다."),
    OFFICIAL_EMBED,
    p("같은 날 밤 공식 틱톡에는 SHINHAENG・SIYOUNG・TOWA・YOSHIKI・YUKI・YURA 6명이 체육관에서 'KO1KEYZ'(Korean ver.)를 추는 영상이 올라왔습니다.<br>\n"
      "TOWA는 이 폴로에 연한 와이드 데님과 흰 스니커즈를 매치했습니다."),
    img_html(m_group, "체육관에서 'KO1KEYZ'(Korean ver.)를 추는 6명. 왼쪽 끝 TOWA는 회색 스트라이프 폴로", f"출처: {SRC_TT}"),
    p("공식 사진과 틱톡 모두 같은 폴로로 등장해, 이날 'KO1KEYZ' 활동을 위해 준비된 의상입니다.<br>\n"
      "다른 5명도 럭비 셔츠・축구 셔츠풍 상의로 맞춰 체육관 세트와 함께 '스포츠 팀' 같은 콘셉트를 보여주었습니다."),
    h2("왜 마틴 로즈라고 할 수 있을까?"),
    img_html(m_towa, "틱톡 영상 속 TOWA. 가슴에 빨간 삼각형 로고와 파란 TOTAL 자수", f"출처: {SRC_TT}"),
    ui.barbox("마틴 로즈 상품 사진과 일치한 포인트", [
        "<strong>왼쪽 가슴 로고</strong>: 빨간 삼각형 마크 아래 빨간 'martine' 글자",
        "<strong>오른쪽 가슴 엠블럼</strong>: 왕관 아래 'MARTINE' 'SPORT', 흑백 세로줄 방패, 좌우 '20' '07', 아래 'ROSE'",
        "<strong>가슴 자수</strong>: 굵은 파란 'TOTAL'과 그 아래 'participation'",
        "<strong>칼라와 원단</strong>: 검은 칼라와 빨간 안감, 파일 원단의 회색×검정×흰색 스트라이프",
    ], ordered=True),
    p(f"네 가지 모두 {ui.mark('품번 674JE09059 Oversized Polo(Grey Black Stripe)', True)}의 상품 사진과 일치했습니다.<br>\n"
      "엠블럼의 '20' '07'은 브랜드가 시작된 2007년을 뜻합니다.<br>\n"
      "나파피리 콜라보 'EGO S/S POLO SHIRT'도 같은 색 스트라이프지만, 피케 원단에 TOTAL 자수와 엠블럼이 없는 다른 상품입니다."),
    h2("소재와 사이즈감은?"),
    p(f"해외 매장 표기에 따르면 소재는 {ui.mark('면 85%・폴리에스터 15%', True)}, 포르투갈 제조입니다.<br>\n"
      "표면이 타월처럼 폭신한 파일 원단이고, 어깨가 떨어지는 오버사이즈 핏입니다.<br>\n"
      "정사이즈로 입고 싶다면 한 사이즈 작게 고르는 것도 방법입니다."),
    h2("마틴 로즈는 어떤 브랜드?"),
    p("마틴 로즈는 런던을 거점으로 하는 디자이너 마틴 로즈가 2007년에 시작한 브랜드입니다.<br>\n"
      "런던 클럽 문화와 축구 유니폼, 90년대 스트리트 감성을 담은 옷으로 알려져 있고, 나이키와의 협업 스니커즈 'Shox MR4'로도 화제가 되었습니다."),
    h2("가격은? 어디서 살 수 있을까?"),
    p(f"미국 FWRD에서는 {ui.mark('정가 555달러', True)}로 올라와 있었습니다.<br>\n"
      "한국 젠테스토어는 정가 783,000원(관부가세 포함)에서 425,000원까지 할인했지만 현재 품절입니다.<br>\n"
      "2026년 10월 12일 기준, 덴마크 Naked에서 정가 2,800크로네의 40% 할인가 1,680크로네로 S 사이즈 재고가 있었습니다(배송비・관세 별도)."),
    ui.barbox("구매처・가격 확인 페이지", [
        f'<a href="{JENTE}" target="_blank" rel="noopener">젠테스토어</a>: 정가 783,000원→425,000원(품절)',
        f'<a href="{NAKED}" target="_blank" rel="noopener">Naked(덴마크)</a>: 1,680크로네, S 재고 있음',
        f'<a href="{FWRD}" target="_blank" rel="noopener">FWRD(미국)</a>: 정가 555달러',
        f'<a href="{MR}" target="_blank" rel="noopener">마틴 로즈 공식 온라인 스토어</a>',
    ]),
    h2("정리"),
    ui.summarybox([
        "TOWA가 2026년 10월 10일 음악중심 날 입은 폴로는 마틴 로즈 'Oversized Polo(Grey Black Stripe)'",
        "품번 674JE09059, 2026 S/S 아이템",
        "결정적 근거는 빨간 삼각형 martine 로고, MARTINE SPORT 엠블럼, 파란 TOTAL 자수",
        "면 85%・폴리에스터 15% 파일 원단, 포르투갈 제조",
        "정가 555달러, 할인 매장도 있음",
    ]),
    p("사이즈가 남아 있을 때 TOWA와 같은 축구풍 폴로를 체크해 보세요!"),
    ui.linkbox("TOWA・KO1KEYZ 관련 글", KR_REL),
])

KR_SUMMARY = ("TOWA가 10월 10일 음악중심 날 입은 회색 스트라이프 폴로는 마틴 로즈 'Oversized Polo(Grey Black Stripe)'"
              "(674JE09059)입니다. 정가 555달러입니다.")

KR_EYECATCH_ID = make_eyecatch(
    ["--top", "TOWA 의상 폴로는 어디 거?", "--main", "KO1KEYZ", "--bottom", "마틴로즈!", "--lang", "kr"],
    ROOT / "images" / "towa_musiccore1010_polo_eyecatch_kr.png",
)
print("KR_EYECATCH_ID", KR_EYECATCH_ID)
kr_post = post_draft(KR_TITLE, KR_CONTENT, KR_SLUG, "ko", [74, 78, 108], KR_EYECATCH_ID, KR_SUMMARY,
                     translations={"ja": JP_POST_ID})
print("KR_POST_ID", kr_post["id"], kr_post["slug"])

# ============================== EN ==============================
EN_TITLE = "[TOWA] His Music Core Polo Is Martine Rose! How Much Is It?"
EN_SLUG = f"{JP_SLUG}-en"

EN_CONTENT = "\n\n".join([
    p("On October 10, 2026, KO1KEYZ appeared on MBC's \"Show! Music Core.\"<br>\n"
      "In the photo of TOWA the official X account posted that day, he wore a gray striped polo with a big blue \"TOTAL\" on the chest.<br>\n"
      "It's the <strong>Martine Rose Oversized Polo in Grey Black Stripe from Spring/Summer 2026</strong>.<br>\n"
      "It retails for <strong>$555</strong>, and some shops now have it about 40% off."),
    ui.infobox("The polo TOWA wore", [
        ("Scene", "Official photo from the Oct 10, 2026 Music Core appearance, plus the official TikTok posted that day"),
        ("Brand", "Martine Rose"),
        ("Item", "Oversized Polo (Grey Black Stripe)"),
        ("Style code", "674JE09059"),
        ("Season", "SS26"),
        ("Price", "$555 retail; on sale for DKK 1,680 at Naked"),
    ]),
    h2("What polo did TOWA wear on Music Core day?"),
    p("Posing in front of a deep red wall, TOWA wore a gray, black and white striped polo with a black collar, a red inner placket and a white tee underneath."),
    OFFICIAL_EMBED,
    p("That evening, the official TikTok posted a \"KO1KEYZ\" (Korean ver.) dance video of SHINHAENG, SIYOUNG, TOWA, YOSHIKI, YUKI and YURA in a gym set.<br>\n"
      "TOWA paired the same polo with light wide-leg jeans and white sneakers."),
    img_html(m_group, "Six KO1KEYZ members dancing \"KO1KEYZ\" (Korean ver.) in a gym; TOWA, far left, in the gray striped polo", f"Source: {SRC_TT}"),
    p("It shows up in both the official photo and the TikTok, so it's his stage costume for the \"KO1KEYZ\" promotions that day.<br>\n"
      "The other five also wore rugby- and football-style tops, matching the gym set for a sports-team concept."),
    h2("How do we know it's Martine Rose?"),
    img_html(m_towa, "TOWA in the TikTok video, showing the red triangle logo and blue TOTAL embroidery", f"Source: {SRC_TT}"),
    ui.barbox("Points that match the product photos", [
        "<strong>Left chest</strong>: a red triangle above red \"martine\" lettering",
        "<strong>Right chest crest</strong>: crown, \"MARTINE\" \"SPORT,\" a black-and-white striped shield, \"20\" \"07,\" and \"ROSE\"",
        "<strong>Center</strong>: bold blue \"TOTAL\" with \"participation\" below",
        "<strong>Collar and fabric</strong>: black collar, red lining, and a plush terry-like stripe",
    ], ordered=True),
    p(f"All four match {ui.mark('style 674JE09059, the Oversized Polo (Grey Black Stripe)', True)}. The \"20\" and \"07\" on the crest refer to 2007, the year the label launched.<br>\n"
      "Don't confuse it with the Martine Rose x Napapijri \"EGO S/S Polo Shirt\": same colors, but piqué cotton with no TOTAL embroidery or crest."),
    h2("Fabric and fit"),
    p(f"Retailers list it as {ui.mark('85% cotton, 15% polyester', True)}, made in Portugal, with a plush terry-like surface and a dropped-shoulder oversized fit. Size down if you want a regular fit."),
    h2("About Martine Rose"),
    p("Martine Rose is a London label founded in 2007 by designer Martine Rose, known for pieces inspired by club culture, football kits and '90s streetwear, and for her Nike Shox MR4 collaboration."),
    h2("Price and where to buy"),
    p(f"FWRD lists it at {ui.mark('$555', True)}. Korea's Jentestore had it marked down from KRW 783,000 to KRW 425,000 but it's sold out.<br>\n"
      "As of October 12, 2026, Naked in Denmark had it 40% off at DKK 1,680 (from DKK 2,800), with size S in stock. Shipping and duties are extra."),
    ui.barbox("Where to buy", [
        f'<a href="{NAKED}" target="_blank" rel="noopener">Naked (Denmark)</a>: DKK 1,680, size S in stock',
        f'<a href="{FWRD}" target="_blank" rel="noopener">FWRD (US)</a>: $555',
        f'<a href="{JENTE}" target="_blank" rel="noopener">Jentestore (Korea)</a>: sold out',
        f'<a href="{MR}" target="_blank" rel="noopener">Martine Rose official online store</a>',
    ]),
    h2("Summary"),
    ui.summarybox([
        "TOWA's polo on Oct 10, 2026 (Music Core day) is the Martine Rose Oversized Polo (Grey Black Stripe)",
        "Style code 674JE09059, SS26",
        "Key clues: the red triangle martine logo, MARTINE SPORT crest and blue TOTAL embroidery",
        "85% cotton, 15% polyester terry-like fabric, made in Portugal",
        "Retail $555, with some shops offering it on sale",
    ]),
    p("Grab it while sizes last if you want to match TOWA's football-inspired look!"),
    ui.linkbox("More on TOWA and KO1KEYZ", EN_REL),
])

EN_SUMMARY = ("TOWA's gray striped polo on Oct 10 Music Core day is the Martine Rose Oversized Polo (Grey Black Stripe), "
              "style 674JE09059. It retails for $555.")

en_post = post_draft(EN_TITLE, EN_CONTENT, EN_SLUG, "en", [110, 118, 114], JP_EYECATCH_ID, EN_SUMMARY,
                     translations={"ja": JP_POST_ID})
print("EN_POST_ID", en_post["id"], en_post["slug"])

print("\n=== DONE ===")
print("JP", JP_POST_ID, f"{WP_URL}/?p={JP_POST_ID}")
print("KR", kr_post["id"], f"{WP_URL}/?p={kr_post['id']}")
print("EN", en_post["id"], f"{WP_URL}/?p={en_post['id']}")
