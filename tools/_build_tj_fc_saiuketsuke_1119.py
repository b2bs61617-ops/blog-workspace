# -*- coding: utf-8 -*-
"""トラジャ『Jewelry Basket』FC限定盤 再受付(chomoand-4.blog)。2026-11-19 オシリ依頼(元ネタ=公式X 2122978355159167038 の引用ポスト)。

    python tools/_build_tj_fc_saiuketsuke_1119.py --build-only
    python tools/_build_tj_fc_saiuketsuke_1119.py              # 下書き投稿
    python tools/_build_tj_fc_saiuketsuke_1119.py --update
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "travis"
KEY = "tj_fc_saiuketsuke_1119"
TITLE = "トラジャFC盤の再受付はいつまで？イベント応募に間に合う？"
SLUG = "travis-japan-jewelry-basket-fc-edition-reorder"
CATEGORIES = [3]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "トラジャFC限定盤の再受付"
X_TEXT = ""
X_TAGS = "#TravisJapan #JewelryBasket"

OFFICIAL_X = "https://x.com/TravisJapan_cr/status/2122978355159167038"
UMJ = "https://www.universal-music.co.jp/travisjapan/news/2026-11-18/"
STORE = "https://famikura-store.jp/s/j/page/TravisJapan4thALBUM"
SP = "https://sp.universal-music.co.jp/travisjapan/4th_album/"
TEASER = "https://www.youtube.com/watch?v=WO5_dmT7UQQ"
A_HOWTO = "https://chomoand-4.blog/travis-japan-album-fc-edition-how-to-buy-1724"
A_POSTPONE = "https://chomoand-4.blog/travis-japan-jewelry-basket-cd-postponed-2505"
A_UNIT = "https://chomoand-4.blog/jewelry-basket-unit-songs-members-1630"
A_DIGITAL = "https://chomoand-4.blog/travis-japan-jewelry-basket-digital-release-2778"
A_FCJOIN = "https://chomoand-4.blog/travis-japan-fanclub-when-to-join-1643"
A_WHERE = "https://chomoand-4.blog/jewelry-basket-where-can-i-buy-922"

b = blogkit.Blocks("#7e57c2", "#d9cdee", "#f5f2fb")
L = b.link
UP = "https://chomoand-4.blog/wp-content/uploads/2026/10/"


def img(name, alt, cap):
    return b.html('<figure class="wp-block-image size-large"><img src="{}{}_web-1024x576.jpg" alt="{}" width="1024" height="576" '
                  'style="max-width:100%;height:auto;"><figcaption>{}</figcaption></figure>'.format(UP, name, alt, cap))


out = ""
out += b.p("Travis Japan(トラジャ)のアルバム『Jewelry Basket』のFC盤が、また申し込めるようになりました。",
           "再受付は" + b.mark("2026年11月19日(木)18:00〜12月4日(金)23:59") + "です。", "数に限りがあるので、早く終わることもあります。",
           "ただ、公式は「届くのが発売記念イベントの応募の締め切り近く、または締め切りのあとになるかも」と注意しています。")
out += b.p("この記事では、再受付の期間と申し込み方、FC盤だけの中身、イベント応募に間に合うのかを、公式の案内をもとにまとめます。")
out += b.wakaru(["FC限定盤の再受付はいつからいつまでか",
                 "なぜ再受付になったのか",
                 "1回目の受付と同じ商品なのか",
                 "申し込みの流れと送料",
                 "発売記念イベントの応募に間に合うのか",
                 "FC盤だけのユニット曲と特典映像"])

# ---------------------------------------------------------------- 結論
out += b.h2("トラジャFC盤の再受付はいつまで？12月4日(金)23:59")
out += b.mini(("再受付", "2026年11月19日(木)18:00〜12月4日(金)23:59"),
              ("買える場所", "ファミクラストアオンラインだけ"),
              ("買える人", "Travis Japanのファンクラブ会員"),
              ("値段(税込)", "Blu-ray付き5,480円/DVD付き4,980円"),
              ("CDの発売日", "2026年12月16日(水)"))
out += b.p("再受付の期間は、11月19日(木)の夕方6時から12月4日(金)の夜11時59分までの約2週間です。",
           "公式は「数量には限りがございます」「上限数に達し次第、販売を終了」としています。",
           "つまり、12月4日まで必ず買えるわけではありません。")
out += b.p("発表は11月18日(水)の夕方6時ごろで、トラジャの公式Xとユニバーサル ミュージックのサイトで同時に出ました。")
out += b.xembed(OFFICIAL_X)
out += b.p("出典:" + L(UMJ, "「Jewelry Basket」FC限定盤 お申し込み再受付のお知らせ(ユニバーサル ミュージック)"))

out += b.h3("1回目の受付はいつだった？")
out += b.p("FC限定盤の1回目の受付は、2026年8月26日(水)18:00〜11月6日(金)23:59でした。",
           "11月6日でいったん締め切られていたので、「買いそびれた」という人にとっては2回目のチャンスです。")
out += b.table(("受付", "期間"),
               [("1回目", "2026年8月26日(水)18:00〜11月6日(金)23:59"),
                ("2回目(再受付)", "2026年11月19日(木)18:00〜12月4日(金)23:59")])
out += b.p("ファミクラストアの特設ページには、2つの受付期間が並んで書かれています。",
           "1回目の締め切りや申し込みのくわしい流れは、" + L(A_HOWTO, "トラジャのアルバムFC盤はどこで買える？") + "でも紹介しています。")

# ---------------------------------------------------------------- 理由
out += b.h2("なぜFC盤の再受付になった？")
out += b.p("公式の案内では、再受付のきっかけは" + b.mark("楽曲の配信が始まったこと") + "とされています。",
           "『Jewelry Basket』は、CDより先に2026年11月18日(水)から配信が始まりました。")
out += b.p("公式の文では、配信で曲を聴いてユニット曲や特典映像、ブレスレットが気になった人に「この機会にチェックして」と呼びかけています。",
           "配信には入っていないユニット曲3曲は、FC限定盤でしか聴けません。")
out += b.p("配信された全12曲は、" + L(A_DIGITAL, "Jewelry Basket配信はいつ？全12曲とPOP STARも！") + "にまとめています。")

out += b.h3("CDの発売延期とは関係ある？")
out += b.p("CDは、もともと11月18日(水)発売の予定でした。",
           "11月11日に「商品の一部に不備」があったとして、全形態のCDが12月16日(水)に延期されています。")
out += b.p("延期のお知らせでは「CD発売までの間も楽しめる機会を準備中」とも書かれていました。",
           "ただ、今回の再受付がその「機会」なのかどうかは、公式ははっきり書いていません。",
           "延期のくわしい流れは" + L(A_POSTPONE, "トラジャのアルバムCD延期はなぜ？") + "をどうぞ。")

out += b.h3("1回目と同じ商品？")
out += b.p("ファミクラストアの特設ページには、「8月26日〜11月6日に販売された商品と同じ」と書かれています。",
           "中身や値段、品番は1回目とまったく同じです。",
           "ファミクラストアで買ったときの「トレーディングカード3種セット」も、今回の案内に書かれています。")

# ---------------------------------------------------------------- 申し込み
out += b.h2("FC盤の再受付の申し込み方は？")
out += b.p("申し込みは、ファミクラストアオンラインの「Travis Japan 4th ALBUM」特設ページからです。",
           "流れは1回目と同じで、ファンクラブ会員だけが申し込めます。")
out += b.table(("ステップ", "やること"),
               [("1", "ファンクラブに入会する(会員でない方だけ)"),
                ("2", "ファミクラストアオンラインのアカウントを用意する(無料)"),
                ("3", "特設ページを開き、ログインしてファンクラブの認証をする"),
                ("4", "Blu-ray付き(PROJ-1942)かDVD付き(PROJ-1943)を選ぶ"),
                ("5", "ほかの商品は入れずに、FC盤だけで注文する"),
                ("6", "支払い方法を選んで注文を決める")])
out += b.p("FC限定盤は、ほかの商品と一緒には買えません。",
           "グッズなどもほしい場合は、注文を分ける必要があります。")
out += b.p("申し込みは" + L(STORE, "ファミクラストアオンラインの特設ページ") + "から進められます。")

out += b.h3("ファンクラブに入っていなくても買える？")
out += b.p("FC限定盤は、Travis Japanのファンクラブ会員だけが買える商品です。",
           "まだ会員でない方も、12月4日までに入会すれば申し込めます。")
out += b.p("入会には、入会金1,000円・年会費4,000円・事務手数料140円の合計5,140円がかかります。",
           "会員番号は、お金の支払いが確認されてから24時間以内にメールで届きます。",
           "コンビニ払いだと支払いに行くまで手続きが終わらないので、早めに済ませておきましょう。")
out += b.p("入会のタイミングは" + L(A_FCJOIN, "トラジャのFCはいつ入るのが正解？") + "でくわしく紹介しています。")

out += b.h3("送料と支払い方法は？")
out += b.mini(("送料", "宅配便1配送につき全国一律770円(税込)"),
              ("支払い", "クレジットカード/コンビニ・Pay-easy・ネットバンキング"),
              ("手数料", "カードは無料、それ以外は1件187円(税込)"))
out += b.p("送料770円を足すと、Blu-ray付きは6,250円、DVD付きは5,750円です。",
           "金額は、注文の画面でもう一度確かめてください。")
out += b.p("コンビニ払いなどの前払いは、お金を払った時点で注文が決まります。",
           "数に限りがある今回は、その場で手続きが終わるクレジットカードが安心です。")

out += b.h3("Blu-ray付きとDVD付き、どちらを選ぶ？")
out += b.p("2つの違いは、特典映像のディスクがBlu-rayかDVDかだけです。",
           "ユニット曲のCDや映像の中身、ブレスレットはどちらにも付きます。")
out += b.p("家のプレーヤーがBlu-rayを見られるならBlu-ray付き、DVDしか見られないならDVD付きを選びましょう。")

# ---------------------------------------------------------------- イベント
out += b.h2("再受付のFC盤で発売記念イベントの応募は間に合う？")
out += b.p("いちばん気をつけたいのが、発売記念イベントの応募です。",
           "『Jewelry Basket』は全7形態のCDに応募券が1枚ずつ入っていて、FC限定盤にも入っています。")
out += b.mini(("イベント", "スペシャルライブ&トーク&お見送り会"),
              ("日程", "2027年1月20日(水)大阪・1月27日(水)神奈川"),
              ("応募期間", "2026年12月15日(火)10:00〜12月20日(日)23:59"),
              ("当選発表", "2027年1月13日(水)12:00"))
out += b.p("応募できるのは12月15日(火)から12月20日(日)までの6日間です。",
           "一方で、FC限定盤は12月16日(水)の発売日以降に、準備ができたものから順番に送られます。")
out += b.p("再受付のお知らせには、はっきりこう書かれています。", b.mark("届くのはイベントの応募の締め切り近くか、締め切りのあとになる場合がある"),
           "公式も「お届け予定日を必ずご自身でご確認の上ご注文ください」と呼びかけています。")

out += b.h3("イベントに応募したい人はどうする？")
out += b.p("再受付のFC盤の応募券は、イベントに使えないかもしれません。",
           "注文の前に、販売ページのお届け予定日を必ず見ておきましょう。")
out += b.p("初回T盤・初回J盤・通常盤にも、応募券は1枚ずつ入っています。",
           "応募は1枚で1口で、何口でも応募できます。",
           "イベントにどうしても応募したいなら、一般のお店で買う形態も合わせて考えるとよさそうです。")
out += b.p("一般のお店の特典とJewelry Charmの色は" + L(A_WHERE, "【Jewelry Basket】特典どこで買う？") + "にまとめています。")
out += b.checks(["応募期間は12月15日(火)〜20日(日)の6日間だけ",
                 "FC盤は12月16日(水)以降に順番に発送",
                 "再受付の分は応募の締め切り後に届くこともある",
                 "注文前に販売ページのお届け予定日を確認する",
                 "応募券は一般のお店の3形態にも入っている"])

# ---------------------------------------------------------------- 中身
out += b.h2("FC盤だけの中身は？ユニット曲3曲と特典映像")
out += b.mini(("Disc1(CD)", "全形態共通の12曲"),
              ("Disc2(CD)", "ユニット曲3曲"),
              ("Disc3(Blu-ray/DVD)", "特典映像 約44分"),
              ("グッズ", "オリジナルブレスレット"),
              ("仕様", "ワンピースボックス+トールデジパック+ブックレットC"),
              ("購入特典", "トレーディングカード3種セット"))
out += img("jb_unit_bts_group", "Jewelry Basket -Behind the scenes-の7人", "出典:Travis Japan公式YouTube(FC限定盤の予告映像)")
out += b.p("FC限定盤のいちばんの目玉は、ほかでは聴けないユニット曲3曲です。")
out += b.table(("ユニット曲", "メンバー"),
               [("パブロフとシュレディンガー", "宮近海斗・七五三掛龍也"),
                ("Fly/Fall", "中村海人・川島如恵留・松田元太"),
                ("カーニバル！アミーゴ！", "吉澤閑也・松倉海斗")])
out += img("jb_unit_pavlov", "パブロフとシュレディンガーのレコーディング風景", "パブロフとシュレディンガーのレコーディング(出典:Travis Japan公式YouTube)")
out += img("jb_unit_flyfall", "Fly/Fallのレコーディング風景", "Fly/Fallのレコーディング(出典:Travis Japan公式YouTube)")
out += img("jb_unit_carnival", "カーニバル！アミーゴ！のレコーディング風景", "カーニバル！アミーゴ！のレコーディング(出典:Travis Japan公式YouTube)")
out += b.p("特典映像は約44分で、アルバム作りの裏側やユニット曲のレコーディングの様子が入っています。",
           "スタジアムで撮った「On My Road -Stadium ver.-」のビデオクリップも見られます。")
out += b.p("公式YouTubeでは、FC限定盤の特典映像の予告も公開されています。")
out += b.youtube(TEASER)
out += b.p("ユニット曲の組み合わせや歴代のユニット曲は、" + L(A_UNIT, "【Jewelry Basket】FC限定盤ユニット曲の組合わせは？") + "で紹介しています。")

out += b.h3("Disc1の収録曲は？")
out += b.p("Disc1は全形態で同じ12曲です。", "4月に出たシングル「陰ニモ日向ニモ」も入っています。")
out += b.table(("曲順", "曲名"), [(str(i + 1), t) for i, t in enumerate(
    ["POP STAR", "EGO", "Idolights", "Homie", "Synchronization", "きゅんTiger", "Good Vibes",
     "陰ニモ日向ニモ", "カタオモイの体温", "LOVE ME DO", "チェックメイト", "365"])])
out += b.p("出典:" + L(SP, "Travis Japan 4th Album「Jewelry Basket」特設サイト"))

# ---------------------------------------------------------------- 反応
out += b.h2("FC盤の再受付にファンの反応は？")
out += b.p("Xでは、お知らせの淡々とした書き方に「もっとうれしそうに知らせて」「【朗報】や星を付けて」とツッコむ声がありました。",
           "それくらい、FC盤をもう一度買えるのはファンにとってうれしいニュースです。")
out += b.p("1回目で買いそびれた人や、配信を聴いてユニット曲が気になった人には、待っていたチャンスといえます。",
           "ただ、イベントの応募に使いたい人は、お届け予定日の注意書きを読んでから決めるのが安心です。")

# ---------------------------------------------------------------- まとめ
out += b.h2("まとめ")
out += b.checks(["FC盤の再受付は11月19日(木)18:00〜12月4日(金)23:59",
                 "数に限りがあり、期間内でも早く終わることがある",
                 "1回目と同じ商品で、ファンクラブ会員だけが買える",
                 "再受付のきっかけは楽曲の配信スタート",
                 "届くのはイベントの応募締め切り(12月20日)後になることも",
                 "ユニット曲3曲と約44分の特典映像はFC盤だけ"])
out += b.p("ユニット曲3曲が聴けるのはFC盤だけなので、迷っている人はこのチャンスを逃さないでほしいです。",
           "イベントに応募したい人は、お届け予定日だけはしっかり確かめておきましょう！")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = blogkit.finalize(out, SITE, NAMES)
    if "--publish" in sys.argv:
        import json
        state = json.loads((blogkit.ARTICLES / (KEY + "_posted.json")).read_text(encoding="utf-8"))
        blogkit.publish(SITE, state["post"], X_TEXT, X_TAGS)
    elif "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
