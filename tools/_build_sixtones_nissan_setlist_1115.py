# -*- coding: utf-8 -*-
"""SixTONES日産スタジアムのセトリは?予習したい曲(chomoand-0.com)。2026-11-15 ライバル見張り(日産公演が近い)から。

    python tools/_build_sixtones_nissan_setlist_1115.py              # 下書き投稿
    python tools/_build_sixtones_nissan_setlist_1115.py --build-only
    python tools/_build_sixtones_nissan_setlist_1115.py --update
セトリは味の素スタジアム公演(9/19)のもの。現地の人のX投稿とレポートブログが一致したものをまとめた記事が出典で、
公式の発表ではない。日産公演のあとに変わった曲があれば --update で足す。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "sixtones"
KEY = "sixtones_nissan_setlist_1115"
TITLE = "SixTONES日産スタジアムのセトリは？予習したい34曲！"
SLUG = "sixtones-milesixtones-nissan-setlist"
CATEGORIES = [15]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "SixTONES日産スタジアムのセトリ"

TINPAN = "https://tinpanblog.com/?p=57456"
S = "https://chomoand-0.com/"

b = blogkit.Blocks("#333333", "#d5d5d5", "#f5f5f5")
L = b.link
out = ""
out += b.p("SixTONES初のスタジアムツアー「MILESixTONES」は、11月21日(土)・22日(日)の日産スタジアムで最後をむかえます。",
           "9月の味の素スタジアム公演では、" + b.mark("本編30曲+アンコール4曲の全34曲") + "が歌われたとみられています。",
           "この記事では、そのセットリストをもとに、日産スタジアムの前に予習しておきたい曲をまとめました。")
out += b.p("※セットリストは、味の素スタジアム公演(9月19日)に行った人のX投稿とレポートが一致したものをまとめた記事がもとです。",
           "公式の発表ではないので、曲順が一部ちがう可能性があります。",
           "日産スタジアムでは曲が入れかわることもあるので、ネタバレを見たくない人は注意してください。")
out += b.wakaru(["日産スタジアム公演の日程と開演時間",
                 "味の素スタジアム公演のセットリスト(全34曲)",
                 "セトリの流れと、MCが入るところ",
                 "予習するときのポイント",
                 "当日までにチェックしておきたい記事"])

out += b.h2("日産スタジアム公演はいつ？")
out += b.mini(("ツアー", "SixTONES Stadium Tour「MILESixTONES」"),
              ("日程", "2026年11月21日(土)・22日(日)"),
              ("会場", "神奈川・日産スタジアム"),
              ("開演", "両日16:30"))
out += b.p("ツアーは、9月の東京・味の素スタジアム、11月7日(土)・8日(日)の大阪・ヤンマースタジアム長居と続いてきました。",
           "日産スタジアムの2日間が、ツアーの最終公演です。",
           "開演は16時30分で、3つの会場の中でいちばん早い時間です。")
out += b.p("服装やアクセス、グッズについては " +
           L(S + "sixtones-stadium-nissan-fashion-goods-1238", "SixTONES日産スタジアムの服装は？開演時間とグッズも！") +
           " でまとめています。")

out += b.h2("味の素スタジアム公演のセットリスト")
out += b.p("9月19日(土)の味の素スタジアム公演では、次の34曲が歌われたとみられています。",
           "1曲目は「アンセム」、本編の最後は「Beyond the line」でした。")
out += b.h3("本編(1〜15曲目)")
out += b.table(("曲順", "曲名"),
               [("1", "アンセム"), ("2", "ABARERO"), ("3", "PUNK STAR"), ("4", "こっから"),
                ("-", "(メンバーのあいさつ)"),
                ("5", "彗星の空"), ("6", "一秒"), ("7", "マイオンリー"), ("8", "キカナイ"),
                ("9", "Special Order"), ("10", "Play the game"), ("11", "希望の唄"), ("12", "Fiesta"),
                ("13", "ALL STAR STATUS"), ("-", "(MC)"),
                ("14", "Flower Cloud"), ("15", "朱夏")])
out += b.h3("本編(16〜30曲目)")
out += b.table(("曲順", "曲名"),
               [("16", "PHANTOMSixTONES"), ("17", "merry-go-round"), ("18", "LIKE THAT"), ("19", "Need you"),
                ("20", "Call me"), ("21", "ABRACADABRA"), ("22", "Bang Bang Bangin’"), ("23", "Waves Crash"),
                ("24", "Dance All Night"), ("25", "DON-DON-DON"), ("26", "HANDS UP"), ("27", "SHOCK ME"),
                ("28", "WHIP THAT"), ("29", "Bring The Bass"), ("30", "Beyond the line")])
out += b.h3("アンコール")
out += b.table(("曲順", "曲名"),
               [("EN1", "S.I.X"), ("EN2", "BE CRAZY"), ("EN3", "この星のHIKARI"), ("EN4", "Dance Forever")])
out += b.p("出典:" + L(TINPAN, "tinpanblog(味スタ公演のセットリスト)"))

out += b.h2("セトリの流れと、MCが入るところ")
out += b.p("セットリストを見ると、ライブは大きく4つのブロックに分けて楽しめます。",
           "どこで声を出すか、どこで座って聴くかを考えながら予習すると、当日がもっと楽しくなります。")
out += b.h3("オープニング(1〜4曲目)")
out += b.p("「アンセム」から「こっから」まで、勢いのある曲が4曲続きます。",
           "このあとにメンバーのあいさつが入ります。",
           "最初からペンライトをふる曲が続くので、開演前に電池やスイッチを確かめておきましょう。")
out += b.h3("前半(5〜13曲目)")
out += b.p("「彗星の空」「一秒」などの曲から、「Fiesta」「ALL STAR STATUS」へと進みます。",
           "「ALL STAR STATUS」のあとにはMCがあります。",
           "スタジアムは広いので、MCのあいだにひと息ついて水分をとっておくと安心です。")
out += b.h3("中盤(14〜21曲目)")
out += b.p("「Flower Cloud」「朱夏」から始まり、「PHANTOMSixTONES」「merry-go-round」と続くブロックです。",
           "21曲目には「ABRACADABRA」が入っています。",
           "この曲は、14枚目のシングル『バリア』の初回盤だけに入っている曲なので、予習のときは見落とさないようにしましょう。")
out += b.h3("後半〜ラスト(22〜30曲目)")
out += b.p("「Bang Bang Bangin’」から「Bring The Bass」まで、9曲が一気に続きます。",
           "いちばん盛り上がるところなので、声を出す準備をしておきましょう。",
           "そして本編の最後は「Beyond the line」でしめくくられます。")
out += b.h3("アンコール")
out += b.p("アンコールは、ジュニアのころから歌ってきた「S.I.X」「BE CRAZY」から始まります。",
           "「この星のHIKARI」「Dance Forever」まで、全部で4曲です。",
           "長くファンをしている人には、思い出の曲がそろったアンコールになっています。")

out += b.h2("予習するときのポイント")
out += b.checks(["曲順どおりに並べたプレイリストを作って、通して聴く",
                 "MCの前後の曲(「こっから」「ALL STAR STATUS」)を覚えておくと流れがつかみやすい",
                 "「ABRACADABRA」はシングル『バリア』初回盤だけに入っているので注意",
                 "アンコールの4曲は、昔からの曲も入っているので一度聴いておく",
                 "日産では曲が変わることもあるので、全部を覚えこまなくてOK"])
out += b.p("音楽の配信サービスでSixTONESの曲を探すと、ほとんどの曲は1曲ずつ聴くことができます。",
           "通勤や家事のあいだに、何回か聴いておくだけでも当日のもり上がりがちがいます。")
out += b.h3("大阪公演から変わった？")
out += b.p("11月7日・8日の大阪・長居公演のセットリストは、11月15日の時点で、まとまった情報が見つかっていません。",
           "味の素スタジアムと同じ流れだったかどうかは、はっきりしていません。",
           "日産スタジアム公演のあと、変わった曲がわかればこの記事に追記します。")

out += b.h2("当日までにチェックしておきたいこと")
out += b.p("日産スタジアム公演は、11月下旬の夕方から夜の屋外ライブです。",
           "セトリの予習とあわせて、寒さ対策と帰り道も準備しておきましょう。")
out += b.checks(["開演は16時30分(3会場でいちばん早い)",
                 "夜は10度を下回ることもあるので、真冬に近い防寒を",
                 "電子チケットを表示するスマホの充電とモバイルバッテリー",
                 "帰りは新横浜駅・小机駅が大混雑。ICカードは先にチャージ"])
out += b.p("席がいつわかるのかは " + L(S + "sixtones-live-seat-when-1509", "SixTONESのライブの席はいつ分かる？") +
           "、グッズの通販は " + L(S + "sixtones-stadium-goods-online-shipping-1241", "SixTONESスタジアムグッズ通販はいつ届く？") +
           " でまとめています。")

out += b.h2("まとめ")
out += b.checks(["日産スタジアム公演は11月21日(土)・22日(日)、両日16時30分開演",
                 "味スタ公演は本編30曲+アンコール4曲の全34曲(公式発表ではない)",
                 "1曲目は「アンセム」、本編ラストは「Beyond the line」",
                 "アンコールは「S.I.X」から「Dance Forever」までの4曲",
                 "日産では変わる可能性があるので、ネタバレに注意"])
out += b.p("初めてのスタジアムツアーも、いよいよラストの2日間です。",
           "しっかり予習して、6人といっしょに最後の夜を楽しみましょう。")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = blogkit.finalize(out, SITE, NAMES)
    if "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
