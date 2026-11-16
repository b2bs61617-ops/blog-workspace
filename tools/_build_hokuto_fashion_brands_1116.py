# -*- coding: utf-8 -*-
"""chomoand-0.com: 松村北斗の私服・衣装の愛用ブランド総まとめ(2026-11-16、ライバル fashion-collemi の型)。

材料: articles/hokuto_fashion_brands_1116_research.md
- adidas: すとらじ回(ID1341 adidas×NIGO 日本代表コレクション 9,350円)とスパイスカレー回(ID1503 品番不明)は
  別の回として分けて書く(同じ商品と決めつけない)。スニーカー=ID1488 ADISTAR CONTROL 5。
- CHANEL=来場ゲスト(アンバサダーではない。「招待」「初パリコレ」は一次で未確認なので書かない)。服の契約ブランドは見つからない。
- MOTHERHOUSE(ドラマ衣装)は公式未確認なので書かない。メガネも入れない。
写真: LOEWE公式X(G7xk...)・静岡県公式X(HIrb...)は投稿時にWPメディアへ上げ直す。
      すとらじ(media 1339)・スパイスカレー回(media 1536)はWPにある公式YouTubeのフレームを再利用。
      The Fashion Post・ELLE Japan・日刊スポーツ記者のXとSixTONES公式Instagramは埋め込み。

    python3 tools/_build_hokuto_fashion_brands_1116.py --build-only   # articles/<KEY>.html を作るだけ
"""
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "sixtones"
KEY = "hokuto_fashion_brands_1116"
TITLE = "【2026年】松村北斗の私服ブランドは？CHANELの衣装も！"
SLUG = "matsumura-hokuto-fashion-brand-matome"
CATEGORIES = [15, 18]
NAMES = ["NIGO", "ガブリエル・シャネル", "ルイス・ウェイン", "玉森裕太"]
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "松村北斗の私服・衣装の愛用ブランドまとめ"
X_TEXT = ""
X_TAGS = "#SixTONES #松村北斗"

# 無彩色で書いて、最後に sixtones_theme で北斗(黒)の色にする
BAR, BG, BORDER, MARK = "#333333", "#f5f5f5", "#d5d5d5", "#d2d3d6"
b = blogkit.Blocks(BAR, BORDER, BG)
L = b.link


def mk(t):
    return ('<strong><span style="font-size:1.1em;background:linear-gradient(transparent 60%,{} 60%);">{}</span></strong>'
            .format(MARK, t))


def fig(src, alt, w, h, cap):
    return b.html('<figure class="wp-block-image size-large"><img src="{}" alt="{}" width="{}" height="{}" '
                  'style="max-width:100%;height:auto;" loading="lazy"><figcaption style="font-size:0.8em;color:#888;">'
                  '出典:<a href="{}" target="_blank" rel="noopener">{}</a></figcaption></figure>'
                  .format(src, alt, w, h, cap, cap))


def box(title, items):
    lis = "\n".join("<li>{}</li>".format(i) for i in items)
    return b.html('<div style="border:1px solid {};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                  '<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{};color:#fff;">{}</p>\n'
                  '<ul style="margin:0;padding:14px 18px 14px 34px;background:{};">\n{}\n</ul>\n</div>'
                  .format(BORDER, BAR, title, BG, lis))


def linkbox(items):
    lis = "\n".join('<li><a href="{}">{}</a></li>'.format(u, t) for u, t in items)
    return b.html('<div style="border:1px solid {};border-left:4px solid {};border-radius:4px;margin:0 0 16px 0;'
                  'padding:14px 18px;background:{};">\n<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">'
                  'あわせて読みたい</p>\n<ul style="margin:0;padding-left:1.3em;">\n{}\n</ul>\n</div>'
                  .format(BORDER, BAR, BG, lis))


def igembed(url):
    return b.html('<blockquote class="instagram-media" data-instgrm-permalink="{0}?utm_source=ig_embed" '
                  'data-instgrm-version="14" style="background:#FFF;border:0;margin:1px auto;max-width:540px;'
                  'min-width:280px;width:calc(100% - 2px);"><a href="{0}" target="_blank" rel="noopener">'
                  'SixTONES公式Instagramの投稿を見る</a></blockquote>\n'
                  '<script async src="//www.instagram.com/embed.js"></script>'.format(url))


# ---- 内部リンク(すべて公開済み)
U_SUTORAJI = "https://chomoand-0.com/matsumura-hokuto-sutoraji-adidas-1341"
U_PINK = "https://chomoand-0.com/hokuto-matsumura-pink-adidas-spice-curry-1503"
U_ADISTAR = "https://chomoand-0.com/matsumura-hokuto-adistar-control5-1488"
U_ACCE = "https://chomoand-0.com/sixtones-accessory-brand-matome-1359"
U_SUITO = "https://chomoand-0.com/matsumura-hokuto-suito-hydroflask-1440"
U_PERFUME = "https://chomoand-0.com/sixtones-favorite-perfume-1436"
U_PROFILE = "https://chomoand-0.com/matsumura-hokuto-profile-education-1150"
U_MINORU = "https://chomoand-0.com/matsumura-hokuto-gyugyutten-minoru-1477"

# ---- 出典
X_LOEWE = "https://x.com/LoeweJP/status/1998592255213568127"
X_TFP = "https://x.com/THEFASHIONPOST/status/2113456429315338607"
X_ELLE = "https://x.com/ellejapan/status/2107217597267886385"
X_SHIZUOKA = "https://x.com/wakamono_gakari/status/2056697973321744793"
X_NIKKAN = "https://twitter.com/nikkan_blueo/status/1514561712527085578"
IG_NAGAI = "https://www.instagram.com/p/DfevzSpzJAU/"
YT_SUTORAJI = "https://www.youtube.com/watch?v=_vikLYJCfaE"
YT_CURRY = "https://www.youtube.com/watch?v=04i0PrJyDd0"
TFP = "https://fashionpost.jp/fashion/401842"
MNN = "https://www.mensnonno.jp/fashion/luxury-brands/675142/"
PRECIOUS = "https://precious.jp/articles/-/56871"
TFT_CHANEL = "https://www.thefirsttimes.jp/news/0000894166/"
TFT_LOEWE = "https://www.thefirsttimes.jp/?p=732913"
ADVERTIMES = "https://www.advertimes.com/20260928/article558793/"
BITEKI = "https://www.biteki.com/2112298/"
SNKRDUNK = "https://snkrdunk.com/products/KJ8804"
ROLE = "https://role-inc.com/products/vertical-half-bangle-silver-narrativeplatoon"

# 投稿時にWPへ上げ直すX画像(build-onlyでは元のURLのまま)
IMG_LOEWE1 = "https://pbs.twimg.com/media/G7xkA9SakAAyhgc.jpg?name=orig"
IMG_LOEWE2 = "https://pbs.twimg.com/media/G7xkA-iaMAEdi3h.jpg?name=orig"
IMG_SHIZUOKA = "https://pbs.twimg.com/media/HIrb54rbkAA5hN0.jpg?name=orig"
REHOST = [IMG_LOEWE1, IMG_LOEWE2, IMG_SHIZUOKA]
# WPにある公式YouTubeのフレーム
IMG_SUTORAJI = "https://chomoand-0.com/wp-content/uploads/2026/11/sixtones_sutoraji_hokuto.jpg"
IMG_CURRY = "https://chomoand-0.com/wp-content/uploads/2026/11/a912410a8c5b4c85b7b32aef0010246d-1536x823.png"

out = ""

# ---- リード
out += b.p(
    "ライブや公式YouTube、雑誌で見る松村北斗さんの服は、いつも「どこの？」と気になります。",
    "2026年はパリコレにも来場し、北斗さんのファッションへの注目は一気に高まりました。",
)
out += b.p(
    "調べてみると、" + mk("公式の動画や写真でよく見るのはadidas(アディダス)") + "でした。",
    "雑誌やパリではCHANEL・LOEWE・BOTTEGA VENETAなどのハイブランドも着ています。",
    "この記事では、ブランドごとに商品名・値段・買える場所までまとめました。",
)
out += b.mini(("名前", "松村北斗(まつむら ほくと)"), ("グループ", "SixTONES"), ("生年月日", "1995年6月18日"),
              ("メンバーカラー", "黒"), ("よく見るブランド", "adidasのジャージ・スニーカー"))
out += b.wakaru([
    "松村北斗が公式の動画や写真でよく着るブランド",
    "adidasのジャージ・スニーカーの商品名と値段",
    "CHANEL・LOEWE・BOTTEGA VENETAとの仕事",
    "バングル・水筒・香りなど小物の愛用ブランド",
    "服の契約ブランド・アンバサダーはある？",
])

out += b.p("まずは、この記事で紹介するブランドを時期の順に並べました。")
out += b.table(("時期", "ブランド", "場面"), [
    ("2022年4月", "Hydro Flask(水筒)", "日刊スポーツの愛用品紹介"),
    ("2025年4月", "NARRATIVEPLATOON", "CanCam 6月号"),
    ("2025年10月", "BOTTEGA VENETA", "Precious 11月号"),
    ("2025年12月", "LOEWE", "MEN'S NON-NO WEB"),
    ("2026年10月", "CHANEL", "パリコレ来場"),
    ("2026年10月", "adidas(ジャージ)", "公式YouTube"),
    ("2026年11月", "adidas(スニーカー)", "長居公演"),
])

# ---- adidas
out += b.h2("松村北斗が公式の動画や写真でよく着るのはadidas")
out += b.mini(("答え", "公式の動画や写真でよく見るのはadidasのジャージとスニーカー"),
              ("場面", "公式YouTube・公式Instagram・ライブ"))
out += b.p(
    "公式の動画や写真で北斗さんの服を見ると、よく登場するのがadidasです。",
    "特に3本線のトラックジャケット(ジャージ)は、何度も着ているアイテムです。",
    "2026年の秋だけでも、公式YouTubeの2つの回とライブでadidasを着ていました。",
)
out += b.p(
    "ただ、公式YouTubeの服が私物かスタイリストの用意かは分かりません。",
    "何度も着ていることから、北斗さんの好みに合ったブランドとみられます。",
)
out += b.p(
    "ここでは、回ごとに分けて紹介します。",
    "見た目が似ていても、同じ商品とは限らないためです。",
)

out += b.h3("adidas×NIGOのサッカー日本代表ジャージ(すとらじ)")
out += b.mini(("商品", "adidas サッカー日本代表 スペシャルコレクション トラックジャケット"),
              ("色", "ワンダーモーブ/クルーグリーン(ピンク×緑)"),
              ("定価", "9,350円(税込)"), ("発売", "2022年10月28日"))
out += b.p(
    "SixTONES公式YouTube「すとらじで近況報告」(2026年10月30日公開)で着ていたジャージとみられます。",
    "赤いメッシュのベストを上から重ねた、遊び心のある着こなしでした。",
)
out += fig(IMG_SUTORAJI, "adidasサッカー日本代表コレクションのトラックジャケットを着た松村北斗", 1280, 720, YT_SUTORAJI)
out += b.p(
    "このコレクションは、HUMAN MADEのNIGOさんがデザインしたサッカー日本代表のシリーズです。",
    "春の和菓子「桜餅」がモチーフで、ピンクの体に緑のえりがかわいらしい1着です。",
)
out += b.p(
    "発売は2022年10月で、今は公式ショップではほぼ見かけません。",
    "買うならフリマアプリやリユースショップが中心になります。",
    "状態がよいものは、定価より高い2万円以上で出ていることもあります。",
)
out += b.p("くわしい見分け方は、" + L(U_SUTORAJI, "すとらじで北斗が着ていたadidas×NIGOのジャージの記事") + "で紹介しています。")

out += b.h3("スパイスカレー回のピンクのadidasジャージ")
out += b.p(
    "公式YouTube「おちゃのまSP」の手作りスパイスカレー回(10月下旬公開)でも、北斗さんはピンクのジャージを着ていました。",
    "ピンクの体に緑のえり、そでには3本線が入ったadidasのジャージです。",
)
out += fig(IMG_CURRY, "スパイスカレー回でピンクのadidasジャージを着た松村北斗(右)", 1536, 823, YT_CURRY)
out += b.p(
    "色の組み合わせは、すとらじ回のジャージとよく似ています。",
    "ただ、" + mk("この回の品番はまだ確かめられていません") + "。",
    "公開された回も別なので、同じ商品かどうかは決めつけずに紹介します。",
)
out += b.p(
    "髪色とジャージのピンクがよく合っていて、ほめる声も多く見られました。",
    "この回のくわしい内容は、" + L(U_PINK, "スパイスカレー回のピンクのadidasジャージの記事") + "にまとめています。",
)

out += b.h3("スニーカーはadidas ADISTAR CONTROL 5")
out += b.mini(("商品", "adidas ADISTAR CONTROL 5(アディスター コントロール 5)"),
              ("色・品番", "プリラブドブルー/ダークブラウン(KJ8804)"),
              ("定価", "16,500円(税込)"), ("発売", "2026年2月3日(日本)"))
out += b.p(
    "2026年11月のヤンマースタジアム長居公演のあと、SixTONES公式Instagramに6人の写真が上がりました。",
    "北斗さんの足元で光っていた銀色のスニーカーが、このモデルとみられます。",
)
out += igembed(IG_NAGAI)
out += b.p(
    "銀色の3本線、えんじ色の靴ひも、水色のメッシュ、こげ茶のソールが商品写真と一致しました。",
    "2000年代のランニングシューズを今っぽく作り直した、人気のシリーズです。",
)
out += b.p(
    "ウィメンズモデルですが、サイズは28.0cmまであります。",
    "購入先は、adidasの公式オンラインストアや店舗、スニーカー店です。",
    "品切れのときは、" + L(SNKRDUNK, "スニダンのKJ8804のページ") + "で探せます。",
)
out += b.p("見比べたポイントは、" + L(U_ADISTAR, "長居公演で北斗が履いた銀のadistar CONTROL 5の記事") + "にくわしく書いています。")

# ---- ハイブランド
out += b.h2("2025〜2026年はハイブランドとの仕事が増えた")
out += b.mini(("答え", "CHANEL・LOEWE・BOTTEGA VENETAを雑誌やパリで着用"),
              ("注意", "どれもアンバサダー(公式の顔)ではない"))
out += b.p(
    "2025年の秋ごろから、北斗さんはハイブランドを着る仕事が急に増えました。",
    "パリコレへの来場、雑誌の特集、ブランドとの企画などです。",
    "ここでは、ブランドごとに着たアイテムと値段を紹介します。",
)

out += b.h3("CHANEL(シャネル)はパリコレに来場")
out += b.p(
    "2026年10月5日、北斗さんはパリのグラン・パレで開かれたCHANELのショーに来場しました。",
    "2027年春夏コレクションのショーで、ゲストとして会場に姿を見せています。",
)
out += b.p(
    "この日の服装は、サンドベージュのシャツに、バーガンディのニットを肩にかけたスタイルでした。",
    "黒のパンツを合わせ、えりもとにはサングラスをかけていました。",
    "手には小さなレザーのバッグを持っています。",
)
out += b.xembed(X_ELLE)
out += b.p(
    "到着したときは「パリの天気は晴れ。僕の気分も晴れです！」とコメントしています。",
    "ショーの様子は、ELLE JapanやVOGUE JAPANなど多くのメディアが伝えました。",
)
out += b.p(
    "同じパリ滞在では、The Fashion Postの企画「松村北斗とシャネル。革新へのタイムライン」も撮られています。",
    "2026年10月23日に公開され、北斗さんが着たアイテムのクレジットも出ています。",
)
out += b.xembed(X_TFP)
out += b.table(("アイテム", "ブランド・商品", "値段(税込)"), [
    ("シャツ", "CHANEL", "757,900円"),
    ("ウォッチ", "CHANEL「ボーイフレンド」", "2,860,000円"),
    ("バッグ", "CHANEL", "1,158,300円(予定)"),
    ("ニット・靴", "CHANEL", "参考商品"),
    ("パンツ・サングラス", "スタイリスト私物", "なし"),
])
out += b.p(
    "時計の「ボーイフレンド」は、18Kベージュゴールドとカーフの革ベルトを使ったモデルです。",
    "ニットと靴は「参考商品」で、お店で買えるかは分かりません。",
)
out += b.p(
    "撮影では、ガブリエル・シャネルのアパルトマンも見学しています。",
    "着ている服の色が、その部屋で見たソファの色にとても近かったそうです。",
    "北斗さんは「すごく縁深くて特別なエネルギーを感じました」と話しています。",
)
out += b.p(
    "ここで大事なのは、" + mk("CHANELのアンバサダーになったわけではない") + "という点です。",
    "公式の発表は見つからず、立場は「ショーに来場したゲスト」です。",
    "CHANELの服は、CHANELの公式サイトや直営のブティックで扱っています。",
)
out += b.p("詳しい写真と動画は、" + L(TFP, "The Fashion Postの記事") + "で見られます。")

out += b.h3("LOEWE(ロエベ)はホリデーコレクションの企画")
out += b.p(
    "2025年12月9日、MEN'S NON-NO WEBで「松村北斗 ロエベをまとい、会いにいく」が公開されました。",
    "LOEWEとのPR企画で、雑誌は2026年1・2月合併号です。",
)
out += b.p(
    "ロエベの公式Xも、この企画を紹介しました。",
    "投稿では「ルイス・ウェインの猫の作品に着想を得たロエベ ホリデーコレクションをまといます」と伝えています。",
)
out += fig(IMG_LOEWE1, "LOEWEのキャッツ フラメンコクラッチを抱えた松村北斗", 960, 1200, X_LOEWE)
out += b.p(
    "写真で北斗さんが抱えているのは、猫の顔が並んだこげ茶色のバッグです。",
    "「キャッツ フラメンコクラッチ」で、値段は486,200円(ミニは414,700円)です。",
    "カーキの中わたシャツに合わせて、やさしい雰囲気に仕上がっています。",
)
out += fig(IMG_LOEWE2, "LOEWEの服を着て茶色のクラッチを持つ松村北斗の全身", 960, 1200, X_LOEWE)
out += b.table(("アイテム", "商品", "値段(税込)"), [
    ("バッグ", "フューチャリスト キャット パズルバッグ スモール", "649,000円"),
    ("バッグ", "キャッツ フラメンコクラッチ", "486,200円"),
    ("バッグ", "キャッツ フラメンコクラッチ ミニ", "414,700円"),
    ("ジャケット", "シアリング デニムジャケット", "939,400円"),
    ("靴", "シューズ", "189,200円"),
    ("靴", "ブーツ", "205,700円"),
])
out += b.p(
    "ほかにもジャケット303,600円、ニット128,700円、マフラー64,900円などを着ています。",
    "問い合わせ先は、ロエベ ジャパン クライアントサービスです。",
    "買うときは、LOEWEの公式サイトか直営店で探すのが確実です。",
)
out += b.p("すべてのクレジットは、" + L(MNN, "MEN'S NON-NO WEBの記事") + "で確かめられます。")

out += b.h3("BOTTEGA VENETAはPreciousで着用")
out += b.p(
    "Precious 2025年11月号(WEB記事は2025年10月7日公開)でも、北斗さんはハイブランドを着ています。",
    "クレジットは「ジャケット520,300円(ボッテガ・ヴェネタ ジャパン)、その他/私物」です。",
)
out += b.p(
    "注目したいのは、" + mk("ジャケット以外は北斗さん本人の私物") + "という点です。",
    "どのアイテムが私物かまでは分かりませんが、雑誌でも自分の服を合わせていることになります。",
    "詳しくは" + L(PRECIOUS, "Preciousの記事") + "で見られます。",
)
out += b.p(
    "このほか、GQ JAPAN 12月号(2026年10月30日発売)や美ST 3月号増刊の表紙も飾りました。",
    "ただ、この2冊は服のブランドの表記が見つからなかったため、ここでは紹介しません。",
)

# ---- 小物
out += b.h2("アクセサリー・水筒・香りの愛用ブランド")
out += b.mini(("バングル", "NARRATIVEPLATOON"), ("水筒", "Hydro Flask(とみられる)"), ("香り", "銘柄は公表なし"))
out += b.p(
    "服だけでなく、小物にも北斗さんらしいこだわりがあります。",
    "雑誌で着けたアクセサリーや、本人が紹介した愛用品をまとめました。",
)

out += b.h3("バングルはNARRATIVEPLATOON")
out += b.mini(("商品", "NARRATIVEPLATOON vertical Half bangle Silver"), ("値段", "28,600円(税込)"))
out += b.p(
    "CanCam 2025年6月号(2025年4月23日発売)の浴衣グラビアで着けていたバングルです。",
    "取りあつかうセレクトショップ「ROLE」の公式ブログが、着用を紹介していました。",
)
out += b.p(
    "シルバーの細身のデザインで、和装にもふだん着にも合わせやすいのが魅力です。",
    "購入先は" + L(ROLE, "ROLEの公式オンラインショップ") + "です。",
    "ほかのメンバーのアクセも、" + L(U_ACCE, "SixTONESのアクセサリーブランドまとめ") + "で紹介しています。",
)

out += b.h3("水筒はHydro Flaskとみられる")
out += b.p(
    "2022年4月、日刊スポーツの連載「サタジャニ」の愛用品紹介で、北斗さんは黒い水筒を見せました。",
    "形と色から、Hydro Flaskの「スタンダードマウス」(フレックスキャップ・ブラック)とみられます。",
)
out += b.xembed(X_NIKKAN)
out += b.p(
    "本人は「水筒です。自分のステージドリンクとかもこだわり始めたので買いました」と話しています。",
    "使い始めて1、2年くらいとのことで、長く使っている愛用品です。",
)
out += b.p(
    "値段は18oz(約530ml)が4,950円、21oz(約620ml)が5,280円です(どちらも税込)。",
    "楽天やAmazon、ANAのショッピングサイトなどで買えます。",
    "くわしくは" + L(U_SUITO, "北斗の黒いHydro Flaskの水筒の記事") + "で紹介しています。",
)

out += b.h3("香りは「甘すぎず、クールすぎない」が好み")
out += b.p(
    "北斗さんは、ふだん使っている香水の銘柄は公表していません。",
    "Duet 2023年9月号では、好きな香りを「甘すぎず、クールすぎない香り」と答えています。",
)
out += b.p(
    "ラジオ『オールナイトニッポンサタデースペシャル』(2024年10月19日)では、昔の話もしていました。",
    "ジュニア時代は、シャネルの「N°5」をつけて寝ていたそうです。",
)
out += b.p(
    "2026年9月からは、柔軟剤「ラボン」のアンバサダーも務めています。",
    "ほかのメンバーの香りも、" + L(U_PERFUME, "SixTONESの愛用香水まとめ") + "で見られます。",
)

# ---- ドラマ衣装
out += b.h2("ドラマの衣装のブランドは？")
out += b.mini(("答え", "ドラマの服は役の衣装で、公式に発表されたブランドは見つからない"),
              ("小ネタ", "カムカムの稔の学生服が展示された"))
out += b.p(
    "ドラマで着る服は、役のために用意された衣装です。",
    "私服とは別もので、ブランドが公式に発表されることはあまりありません。",
)
out += b.p(
    "衣装の小ネタとしては、朝ドラ『カムカムエヴリバディ』で演じた稔の学生服が展示されたことがあります。",
    "くわしくは" + L(U_MINORU, "カムカムの稔の学生服展示の記事") + "で紹介しています。",
)

# ---- 契約
out += b.h2("服の契約ブランドやアンバサダーはある？")
out += b.mini(("答え", "服のブランドの公式契約は見つからない"),
              ("広告契約", "anummy・ラボン・静岡県のアンバサダー"))
out += b.p(
    "2026年11月の時点で、" + mk("服のブランドとの公式なアンバサダー契約は見つかりませんでした") + "。",
    "CHANELはショーへの来場、LOEWEは雑誌の企画での着用です。",
)
out += b.p("一方で、服以外では3つのアンバサダーを務めています。")
out += b.table(("時期", "相手", "内容"), [
    ("2026年2月", "anummy(ヘアケア)", "ブランドアンバサダー"),
    ("2026年5月", "静岡県", "誕生150周年アンバサダー"),
    ("2026年9月", "ラボン(柔軟剤)", "新しいアンバサダー"),
])
out += b.p(
    "anummyでは、新CM『きっと、たぶん』篇で「ホクト研究員」役を演じました(" + L(BITEKI, "美的") + ")。",
    "ラボンは、約12年続いた玉森裕太さんからバトンを受けつぐ形での起用です(" + L(ADVERTIMES, "AdverTimes") + ")。",
)
out += b.p(
    "地元・静岡県のアンバサダーには、2026年5月19日に委嘱式で任命されました。",
    "黒のスーツ姿で式にのぞんだ写真が、静岡県の公式Xに上がっています。",
)
out += fig(IMG_SHIZUOKA, "静岡県誕生150周年アンバサダーの委嘱式に出た松村北斗", 2048, 1366, X_SHIZUOKA)

# ---- SNS
out += b.h2("北斗のファッションへのSNSの反応")
out += b.mini(("答え", "ハイブランドにもジャージにも「似合う」という声が多い"))
out += b.p(
    "パリコレでの姿には、「上品な色味がお似合い」「正統派のかっこよさ」といった声が集まりました(" + L(TFT_CHANEL, "THE FIRST TIMES") + ")。",
    "LOEWEの企画でも、北斗さんとロエベは「相性が良すぎる」という声が見られます(" + L(TFT_LOEWE, "THE FIRST TIMES") + ")。",
)
out += box("SNSの声", [
    "上品な色味がお似合い(CHANEL)",
    "正統派のかっこよさ(CHANEL)",
    "北斗とロエベの相性が良すぎる(LOEWE)",
    "髪色とジャージの色がよく合っている(adidasのピンクジャージ)",
])
out += b.p(
    "ハイブランドでもジャージでも、似合うと言われるのが北斗さんの強みです。",
    "きれいめとカジュアルの両方を着こなせる幅の広さが、人気の理由といえそうです。",
)

# ---- まとめ
out += b.h2("まとめ")
out += b.checks([
    "松村北斗が公式の動画や写真でよく着るのはadidas",
    "すとらじ回はadidas×NIGOの日本代表ジャージ(9,350円)とみられる",
    "スパイスカレー回のピンクのジャージは品番が未確認",
    "スニーカーはADISTAR CONTROL 5(16,500円)とみられる",
    "CHANELはパリコレ来場、LOEWE・BOTTEGA VENETAは雑誌の企画で着用",
    "服のアンバサダー契約はなく、anummy・ラボン・静岡県のアンバサダー",
])
out += b.p(
    "ジャージで笑う姿も、パリでシャネルをまとう姿も、どちらも北斗さんらしさがあります。",
    "まずは手の届くadidasから、北斗さんとおそろいを楽しんでみてはいかがでしょうか！",
)
out += linkbox([
    (U_PROFILE, "松村北斗のプロフィール・学歴まとめ"),
    (U_MINORU, "カムカムの稔の学生服が展示！松村北斗の衣装"),
])


def rehost(html):
    """X画像をWPメディアに上げ直して src を差し替える(投稿のときだけ)。"""
    wp = blogkit.WP(SITE)
    for i, url in enumerate(REHOST, 1):
        if url not in html:
            continue
        f = blogkit.ROOT / "images" / "{}_x{}.jpg".format(KEY, i)
        if not f.exists():
            urllib.request.urlretrieve(url, str(f))
        alt = re.search(r'src="{}" alt="([^"]*)"'.format(re.escape(url)), html).group(1)
        mid = wp.upload_media(str(f), alt)
        m = wp.get("/media/{}".format(mid))
        sizes = m["media_details"].get("sizes", {})
        big = sizes.get("large") or sizes.get("full") or {"source_url": m["source_url"]}
        html = html.replace(url, big["source_url"])
    return html


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    import sixtones_theme  # noqa: E402
    out = blogkit.finalize(out, SITE, NAMES)   # さん付け → ひらがな直し
    out = sixtones_theme.apply_theme(out, "松村北斗")
    assert len(TITLE) <= 35, len(TITLE)
    if "--publish" in sys.argv:
        import json
        state = json.loads((blogkit.ARTICLES / (KEY + "_posted.json")).read_text(encoding="utf-8"))
        blogkit.publish(SITE, state["post"], X_TEXT, X_TAGS)
    elif "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"), "タイトル", len(TITLE), "字")
    else:
        out = rehost(out)
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
