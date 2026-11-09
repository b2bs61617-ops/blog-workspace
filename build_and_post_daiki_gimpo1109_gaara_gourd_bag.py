# -*- coding: utf-8 -*-
"""DAIKI(加藤大樹)の2026-11-09金浦出国時のバッグ = NARUTO 我愛羅のひょうたん型バックパック(Great Eastern Entertainment GE-5456)。
きっかけ: オシリが共有したファン投稿2件(本文では触れない)。人物はオシリがDAIKIと確認。
裏取り: WoWKorea映像 5:55-6:02(チェックイン)の4Kコマと、Great Eastern版の商品写真(poggers.com)を比較。
  一致点=クリーム色のキャンバス地、上の口が茶色の布+巾着ひも、くびれの赤い帯(ベルト状)、カーキの肩ひも1本、黒枠の文字パッチ、ひび割れの線。
  別物との差: ニジゲンノモリ限定「我愛羅のひょうたん風リュック」(9,400円、2024/12/24〜)は帯が青紫、
  バンプレスト「なりきりぬいぐるみ～我愛羅のひょうたん～」(2025/8プライズ)は帯が太い赤の布でリュック機能なし。
  Great Eastern版: 約12x11x25インチ(約30x28x63cm)、米国で69.99ドル前後(poggers/eBay)、Entertainment Earthでは販売終了。
画像: WoWKorea FAN 公式YouTube WBUHuDk_BFg 303.5s(ロビー)/357.5s(チェックイン全身)/359.5s(バッグ)。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "tools"))
from honorific import add_san, missing
from _mubank1009_helpers import ROOT, WP_URL, post_draft, make_eyecatch, wp_upload, img_html, h2, p, UI

SCR = Path(r"C:\Users\s30se\AppData\Local\Temp\claude\c9a2de9076135094\7bf9d986-4e43-49d4-8517-9024e6170bcc\scratchpad\x")
WOW_ID = "WBUHuDk_BFg"
WOW_URL = f"https://www.youtube.com/watch?v={WOW_ID}"
NIJI_URL = "https://nijigennomori.com/2024/11/22/narutoboruto-555/"
AMZ = "https://www.amazon.co.jp/s?k=NARUTO+%E6%88%91%E6%84%9B%E7%BE%85+%E3%81%B2%E3%82%87%E3%81%86%E3%81%9F%E3%82%93+%E3%83%AA%E3%83%A5%E3%83%83%E3%82%AF&tag=chomoand03-22"
YT = f'''<!-- wp:html -->
<div style="position:relative;width:100%;padding-top:56.25%;margin:1em 0;"><iframe src="https://www.youtube.com/embed/{WOW_ID}?start=355" title="KO1KEYZ Gimpo Airport 2026-11-09" loading="lazy" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
<!-- /wp:html -->'''

media = {}
for key, src, dst in [("lobby", "daiki_lobby.jpg", "daiki_gimpo1109_lobby.jpg"),
                      ("full", "daiki_full.jpg", "daiki_gimpo1109_gaara_gourd_full.jpg"),
                      ("bag", "daiki_bag.jpg", "daiki_gimpo1109_gaara_gourd_bag.jpg")]:
    d = ROOT / "images" / dst
    d.write_bytes((SCR / src).read_bytes())
    media[key] = wp_upload(d, "image/jpeg")
    print("MEDIA", key, media[key]["id"])

ui = UI(AB="#d9d9de", AL="#5b5f6b", BG="#f5f5f7", TH="#e8e8ec", marker="mark_yellow")

REL_JP = [
    ("https://chomoand-1.com/daiki-gimpo-airport-bape-paisley-shark-hoodie-14296", "DAIKIが金浦空港で着ていたBAPEのペイズリー柄シャークパーカーの記事"),
    ("https://chomoand-1.com/daiki-autograph-midori-frog-13800", "DAIKIのサインがなぜ「Midori」なのかを調べた記事"),
    ("https://chomoand-1.com/ryoga-gimpo-airport-celine-naruto-tee-14283", "RYOGAが10月7日の金浦空港で着ていたユニクロのNARUTO Tシャツの記事"),
    ("https://chomoand-1.com/ryoga-gimpo-airport-naruto-jujutsu-keychains-15163", "RYOGAのバッグに付いていたNARUTOと呪術廻戦のキーホルダーの記事"),
    ("https://chomoand-1.com/?p=15478", "同じ日にTOWA・KOSUKE・YURAが付けていたおそろいのエイリアンキーホルダーの記事"),
    ("https://chomoand-1.com/?p=15507", "同じ日のKEITOのFANCY CLUBのバッグの記事"),
]

PR = '<!-- wp:paragraph -->\n<p style="font-size:12px;color:#888;">本記事はプロモーションを含みます</p>\n<!-- /wp:paragraph -->'
AFF = f'(<a href="{AMZ}" target="_blank" rel="nofollow sponsored noopener">Amazonで見る</a>)'

JP = "\n\n".join([
    PR,
    p("KO1KEYZ(コイキーズ)のDAIKI(加藤大樹)が、11月9日に韓国・金浦空港から日本へ向かったときに肩にかけていた、大きなひょうたん型のバッグ。<br>\n"
      "クリーム色の胴体に赤い帯、黒い枠の文字のパッチという見た目は、まさにNARUTOの我愛羅が背負っている「砂のひょうたん」そのものでした。<br>\n"
      f"形や作りから、アメリカのGreat Eastern Entertainment(グレートイースタン)の{ui.mark('NARUTO公式ライセンス品「我愛羅のひょうたんスペシャルバックパック」', True)}とみられます。<br>\n"
      f"アメリカでの販売価格は{ui.mark('約70ドル(1万円前後)', True)}です。"),
    ui.infobox("DAIKIの空港バッグ", [
        ("メーカー", "Great Eastern Entertainment(アメリカ)"),
        ("商品名", "NARUTO 我愛羅のひょうたんスペシャルバックパック(Gaara's Gourd Special Backpack)"),
        ("品番", "GE-5456"),
        ("価格", "約70ドル(アメリカの販売店での価格)"),
        ("着用日", "2026年11月9日(金浦国際空港から羽田へ出国)"),
    ]),
    ui.knowbox("この記事でわかること", ["DAIKIが空港で持っていたひょうたんバッグの正体", "Great Eastern版と分かるポイント", "値段・サイズ・買い方", "よく似たニジゲンノモリ版・プライズ版との違い"]),

    h2("DAIKIが11月9日の金浦空港で持っていたひょうたんバッグ"),
    ui.minibox([("日付：", "2026年11月9日(日)午後"), ("場所：", "韓国・金浦国際空港(羽田行き)")]),
    p("KO1KEYZは韓国で初めての単独ファンミーティングを終え、11月9日の午後に金浦国際空港から羽田空港へ出国しました。<br>\n"
      "その様子は、韓国エンタメメディアWoWKoreaの公式YouTubeが4Kで公開しています。<br>\n"
      "DAIKIは空港のロビーでは、缶バッジをたくさん付けた緑のキャップに、緑と黒のヒョウ柄のようなファーのパーカーという、メンバーカラーの緑づくしのコーデで登場しました。"),
    img_html(media["lobby"], "金浦空港のロビーで緑のキャップとヒョウ柄パーカー姿のDAIKI(加藤大樹)", f"出典：{WOW_URL}"),
    p("そして搭乗手続きのカウンターに並んだとき、肩にかけていたのが、存在感たっぷりの<strong>ひょうたん型のバッグ</strong>です。<br>\n"
      "動画では6分前後、カウンターの前でマスクを外して本人確認をしている場面で、バッグ全体がよく映っています。"),
    YT,
    img_html(media["full"], "金浦空港のチェックインで我愛羅のひょうたんバッグを肩にかけるDAIKI(加藤大樹)", f"出典：{WOW_URL}"),
    p("黒いバックパックのメンバーが並ぶなかで、ひとりだけ大きなひょうたんを背負っている姿は、まるで我愛羅のコスプレのようでもあります。<br>\n"
      "空港ファッションにアニメのアイテムを堂々と取り入れるところに、DAIKIの遊び心が出ていますね。"),

    h2("我愛羅の「砂のひょうたん」とは？"),
    p("我愛羅(があら)は、漫画・アニメ『NARUTO -ナルト-』に登場する砂隠れの里の忍で、のちに五代目風影になる人気キャラクターです。<br>\n"
      "いつも背中に大きなひょうたんを背負っていて、その中に入っている砂をあやつって戦います。<br>\n"
      "ひょうたんのくびれには赤い帯が巻かれ、表面には四角い枠の模様が入っているのが特徴です。<br>\n"
      "このデザインはファンの間でもとても有名で、これまでにリュックやぬいぐるみなど、いろいろなグッズになっています。"),

    h2("Great Eastern版のひょうたんバックパックと分かるポイント"),
    img_html(media["bag"], "DAIKI(加藤大樹)のひょうたんバッグの赤い帯と巾着ひも", f"出典：{WOW_URL}"),
    p("バッグを近くで見ると、Great Eastern Entertainmentのひょうたんバックパックと同じ特徴がいくつも見つかります。"),
    ui.barbox("DAIKIのバッグとGreat Eastern版の共通点", [
        "全体がクリーム色のキャンバス地で、上下2つのふくらみがあるひょうたん型",
        "上の口が茶色の布になっていて、巾着のひもで絞るつくり",
        "くびれ部分に、ベルトのような細めの赤い帯",
        "上から斜めにかけるカーキ色の肩ひもが1本",
        "黒い四角い枠の文字のパッチと、表面に描かれたひび割れの線",
    ]),
    p("とくに、口を巾着のひもで絞るつくりと、カーキ色の1本の肩ひもは、ほかのひょうたんグッズにはないGreat Eastern版ならではのポイントです。<br>\n"
      "ただし本人や事務所が商品名を明かしたわけではないので、この記事では「とみられる」としています。"),

    h2("我愛羅のひょうたんバックパックの値段とサイズ"),
    ui.minibox([("価格：", "約70ドル(アメリカ)"), ("サイズ：", "約30×28×63cm")]),
    p(f"Great Eastern版のひょうたんバックパックは、アメリカのアニメグッズ店で{ui.mark('69.99ドル前後', True)}で販売されてきました{AFF}。<br>\n"
      "日本円にすると1万円前後です。<br>\n"
      "高さは約25インチ(約63cm)もあり、子どもの身長の半分くらいある、かなりの大きさです。"),
    ui.infobox("Great Eastern 我愛羅のひょうたんスペシャルバックパック", [
        ("メーカー", "Great Eastern Entertainment(アメリカ)"),
        ("品番", "GE-5456"),
        ("ライセンス", "NARUTO 公式ライセンス品"),
        ("サイズ", "約12×11×25インチ(約30×28×63cm)"),
        ("つくり", "キャンバス地、巾着ひもの口、横のファスナー、肩ひも1本"),
        ("価格", "69.99ドル前後(アメリカの販売店)"),
    ]),
    p("もともとアメリカ向けの商品のため、日本の公式ショップでは取り扱いがありません。<br>\n"
      "アメリカの大手グッズ店ではすでに「販売終了」になっているところもあり、今はAmazonの海外からの出品や、eBayなどの海外通販・フリマで探すのが中心です。<br>\n"
      "海外から取り寄せる場合は送料や関税がかかり、元の値段より高くなることが多いので、買う前に合計金額をよく確認しましょう。"),

    h2("よく似たひょうたんグッズとの違い"),
    p("我愛羅のひょうたんグッズは、ほかにも日本で発売されたものがあります。<br>\n"
      "見た目が似ているので、DAIKIのバッグとの違いをまとめました。"),
    ui.infobox("ほかの我愛羅のひょうたんグッズ", [
        ("ニジゲンノモリ限定「我愛羅のひょうたん風リュック」", "兵庫・淡路島の「NARUTO&BORUTO 忍里」のオリジナルグッズ。2024年12月24日〜、単品9,400円。帯が青紫色"),
        ("バンプレスト「なりきりぬいぐるみ～我愛羅のひょうたん～」", "2025年8月登場のプライズ(景品)。太い赤い布の帯で、ぬいぐるみなのでバッグとしての機能はない"),
        ("Great Eastern「ひょうたんスペシャルバックパック」", "アメリカのメーカーの公式ライセンス品。細い赤い帯・巾着ひもの口・カーキの肩ひも。DAIKIのバッグはこれとみられる"),
    ]),
    p(f"ニジゲンノモリ版は、帯が青紫色のひもになっているので、赤い帯のDAIKIのバッグとはちがいます(<a href=\"{NIJI_URL}\" target=\"_blank\" rel=\"noopener\">ニジゲンノモリ公式</a>)。<br>\n"
      "バンプレストのぬいぐるみは、くびれの赤い部分が太い布になっていて、口の巾着ひもや肩ひもの形もちがいます。<br>\n"
      "空港で荷物を入れて持ち歩いていたことを考えても、実際にバッグとして使えるGreat Eastern版の可能性が高いといえます。"),

    h2("KO1KEYZにはNARUTO好きが多い？"),
    p("KO1KEYZでNARUTO好きといえば、RYOGAの名前を思い浮かべるファンも多いはずです。<br>\n"
      "RYOGAは10月7日の金浦空港でユニクロのNARUTOのTシャツを着ていたほか、10月23日にはバッグに波風ミナトやうちはサスケのマスコットを付けていました。<br>\n"
      "そこに今回、DAIKIが我愛羅のひょうたんバッグで登場したことで、グループの中にNARUTO好きが2人いることになりました。<br>\n"
      "これからDAIKIとRYOGAの2人で、NARUTOの話で盛り上がる場面も見られるかもしれませんね。"),

    h2("まとめ"),
    ui.summarybox([
        "DAIKIは11月9日、金浦空港から羽田へ向かうときにひょうたん型のバッグを持っていた",
        "バッグはNARUTOの我愛羅の「砂のひょうたん」をモチーフにしたもの",
        "Great Eastern Entertainmentの「我愛羅のひょうたんスペシャルバックパック」(GE-5456)とみられる",
        "アメリカでの価格は約70ドル、高さ約63cmの大きめサイズ",
        "日本では海外通販やAmazonの海外出品で探すのが中心",
    ]),
    p("緑のキャップとヒョウ柄のパーカーに、我愛羅のひょうたんを合わせたDAIKIの空港コーデでした。<br>\n"
      "次の空港では、どんなアイテムで登場するのか楽しみですね！"),
    ui.linkbox("DAIKI・KO1KEYZの関連記事", REL_JP),
])
JP = add_san(JP, "ko1keyz")
print("missing", missing(JP, "ko1keyz"))
print("JP chars", len(JP))

SLUG = "daiki-gimpo-airport-naruto-gaara-gourd-backpack"
TITLE = "【KO1KEYZ】DAIKIの空港バッグはどこの？我愛羅のひょうたん！"
assert len(TITLE) <= 35, len(TITLE)
SUM = ("KO1KEYZのDAIKI(加藤大樹)が11月9日の金浦空港で持っていたひょうたん型のバッグは、NARUTO我愛羅の「砂のひょうたん」をモチーフにした"
       "Great Eastern Entertainmentのスペシャルバックパックとみられます。")
EYE = make_eyecatch(["--top", "DAIKIの空港バッグは？", "--main", "KO1KEYZ", "--bottom", "我愛羅のひょうたん！"],
                    ROOT / "images" / "daiki_gimpo1109_gaara_eyecatch.png")
jp = post_draft("【未】" + TITLE, JP, SLUG, "ja", [66, 82, 63], EYE, SUM)
print("JP", jp["id"])

KR = "\n\n".join([
    p("KO1KEYZ(코이키즈) DAIKI(加藤大樹/카토 다이키)가 11월 9일 김포공항에서 일본으로 출국할 때 멘 커다란 호리병 모양 가방은 "
      + ui.mark('NARUTO 가아라의 "모래 호리병"을 본뜬 Great Eastern Entertainment의 공식 라이선스 백팩', True) + "으로 보입니다. "
      + f"미국 판매가는 {ui.mark('약 70달러', True)}입니다."),
    ui.infobox("DAIKI의 공항 가방", [
        ("제조사", "Great Eastern Entertainment(미국)"),
        ("상품명", "NARUTO Gaara's Gourd Special Backpack"),
        ("품번", "GE-5456"),
        ("가격", "약 70달러(미국 판매가)"),
        ("착용일", "2026년 11월 9일(김포국제공항 → 하네다)"),
    ]),
    h2("11월 9일 김포공항의 DAIKI"),
    p("한국 첫 단독 팬미팅을 마친 KO1KEYZ는 11월 9일 오후 김포공항에서 하네다로 출국했습니다. WoWKorea 공식 유튜브가 4K로 공개했습니다. "
      "DAIKI는 배지를 단 초록 캡과 초록・검정 호피 무늬 퍼 후드로 멤버 컬러인 초록을 맞췄습니다."),
    img_html(media["lobby"], "김포공항 로비의 DAIKI(카토 다이키)", f"출처:{WOW_URL}"),
    YT,
    img_html(media["full"], "체크인 카운터에서 가아라의 호리병 가방을 멘 DAIKI", f"출처:{WOW_URL}"),
    h2("Great Eastern 백팩으로 보는 이유"),
    img_html(media["bag"], "DAIKI 호리병 가방의 빨간 띠와 조임끈", f"출처:{WOW_URL}"),
    p("크림색 캔버스 원단, 갈색 천에 조임끈이 달린 입구, 잘록한 부분의 가는 빨간 띠, 카키색 어깨끈 하나, 검은 테두리 문자 패치와 금 간 무늬가 일치합니다. "
      "띠가 청보라색인 니지겐노모리 한정 백팩(9,400엔)이나, 굵은 빨간 천 띠의 반프레스토 인형과는 다릅니다. 다만 본인이나 소속사가 밝힌 것은 아닙니다."),
    h2("가격・사이즈"),
    p("미국 굿즈숍 판매가 69.99달러 전후, 크기 약 30×28×63cm. 일본 공식 판매는 없고 해외 직구나 중고 거래로 구하는 경우가 많습니다."),
    h2("정리"),
    ui.summarybox([
        "가방: NARUTO 가아라 호리병 모티브의 Great Eastern 스페셜 백팩(GE-5456)으로 보임",
        "미국 판매가 약 70달러, 높이 약 63cm",
    ]),
])
kr = post_draft("【未】【KO1KEYZ】DAIKI 공항 가방은? 가아라 호리병!", KR, SLUG + "-kr", "ko", [74, 78], EYE,
                "KO1KEYZ DAIKI가 11월 9일 김포공항에서 멘 호리병 가방은 NARUTO 가아라 모티브의 Great Eastern 백팩으로 보입니다.",
                translations={"ja": jp["id"]})
print("KR", kr["id"])

EN = "\n\n".join([
    p("The huge gourd-shaped bag KO1KEYZ's DAIKI (Kato Daiki) carried at Gimpo Airport on November 9 appears to be "
      + ui.mark("Great Eastern Entertainment's officially licensed NARUTO Gaara's Gourd Special Backpack", True) + ", sold for about $70 in the US."),
    ui.infobox("DAIKI's airport bag", [
        ("Maker", "Great Eastern Entertainment (US)"),
        ("Item", "NARUTO Gaara's Gourd Special Backpack"),
        ("Item no.", "GE-5456"),
        ("Price", "About $70 (US retailers)"),
        ("Seen on", "November 9, 2026 (Gimpo → Haneda)"),
    ]),
    h2("DAIKI at Gimpo Airport on November 9"),
    p("After their first solo fan meeting in Korea, KO1KEYZ flew from Gimpo to Haneda on November 9, posted in 4K by WoWKorea's official YouTube channel. "
      "DAIKI went all green, his member color, with a pin-covered green cap and a green-and-black leopard-style fur hoodie."),
    img_html(media["lobby"], "DAIKI (Kato Daiki) in the Gimpo Airport lobby", f"Source: {WOW_URL}"),
    YT,
    img_html(media["full"], "DAIKI carrying Gaara's gourd bag at check-in", f"Source: {WOW_URL}"),
    h2("Why it looks like the Great Eastern backpack"),
    img_html(media["bag"], "The red band and drawstring on DAIKI's gourd bag", f"Source: {WOW_URL}"),
    p("Cream canvas, a brown drawstring top, a thin red band at the waist, a single khaki strap, black-framed kanji patches and painted cracks all match. "
      "It differs from the Nijigen no Mori park-exclusive backpack (¥9,400, purple-blue band) and the Banpresto prize plush (wide red cloth band, not a real bag). DAIKI hasn't named the bag himself, though."),
    h2("Price and size"),
    p("Around $69.99 at US anime shops, about 12 x 11 x 25 inches. It isn't sold officially in Japan, so it's mostly found through import listings and resale sites."),
    h2("Summary"),
    ui.summarybox([
        "Bag: appears to be Great Eastern's NARUTO Gaara's Gourd Special Backpack (GE-5456)",
        "About $70 in the US, about 25 inches tall",
    ]),
])
en = post_draft("【未】[KO1KEYZ] DAIKI's Airport Bag: Gaara's Gourd!", EN, SLUG + "-en", "en", [110, 118], EYE,
                "KO1KEYZ's DAIKI carried what appears to be Great Eastern's NARUTO Gaara's Gourd Special Backpack at Gimpo Airport on Nov 9.",
                translations={"ja": jp["id"], "ko": kr["id"]})
print("EN", en["id"])
print("IDS", jp["id"], kr["id"], en["id"])
