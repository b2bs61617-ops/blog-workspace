# -*- coding: utf-8 -*-
"""chomoand-4.blog Travis Japanの雑誌着用アクセまとめ2026(2026-11-21 オシリ依頼)。

根拠: ブランド公式Xの「着用いただきました」告知+LION HEART PRESSページ。調査メモ articles/mag_acc_2026_research.md。
    python tools/_build_upload_tj_mag_acc_2026_1121.py --build-only
    python tools/_build_upload_tj_mag_acc_2026_1121.py            # 【未】下書き投稿
    python tools/_build_upload_tj_mag_acc_2026_1121.py --update
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
from _mag_acc_2026_common import Media, NOTICE, aff  # noqa: E402

SITE = "travis"
KEY = "tj_mag_acc_2026_1121"
TITLE = "Travis Japanの雑誌着用アクセ2026！ブランドや値段は？"
SLUG = "travis-japan-magazine-accessories-2026"
CATEGORIES = [3, 4, 6, 7, 8, 9, 11]
NAMES = ["岩本照"]
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch_canva.jpg")
EYECATCH_ALT = "Travis Japanの雑誌着用アクセまとめ2026"
X_TEXT = ""
X_TAGS = "#TravisJapan"

b = blogkit.Blocks("#4a7fc1", "#b9cfeb", "#f1f6fc")
M = Media(SITE, KEY, b)
IMGS = {
    "tj_2037133188443820376_0": "gramiiのmoonstone brass ring",
    "tj_2037133188443820376_2": "gramiiのネックレス",
    "tj_2043660472168137176_1": "LHMEのMELLOWスモールバロックパールネックレス",
    "tj_2092907474244272311_1": "LHMEのMELLOWハーフバロックパールネックレス",
    "tj_2097490177203523947_1": "NARRATIVEPLATOONのVOLUME BRACELET GIGA",
}


def build():
    o = NOTICE
    o += b.p("Travis Japanのメンバーは、雑誌のグラビアでもおしゃれなアクセサリーを着けています。",
             "撮影のあと、ブランドの公式アカウントが「着用いただきました」と発表してくれることもあります。")
    o += b.p("この記事では、" + b.mark("2026年に発売された雑誌で着用したアクセサリー") + "を、ブランドの公式発表をもとにまとめました。",
             "ブランド名・商品名と、ショップで確認できた値段も紹介します。")
    o += b.wakaru(["2026年の雑誌で着用したアクセの一覧",
                   "松田元太がananの表紙で着けたリング",
                   "川島如恵留が2回着けたパールネックレス",
                   "七五三掛龍也が表紙で着けたブレスレット"])

    # ---- 一覧
    o += b.h2("Travis Japanの雑誌着用アクセ一覧【2026年】")
    o += b.p("まずは、2026年に発売された雑誌で着用したアクセサリーを、発売の順に表にまとめました。",
             "くわしくは、このあと雑誌ごとに紹介します。")
    o += b.table(("雑誌", "メンバー", "アクセ(ブランド)"), [
        ("anan No.2489", "松田元太", "リング・ネックレス(gramii)"),
        ("J Movie Magazine Vol.129", "松倉海斗", "ネックレス(LHME)"),
        ("TV station 2026年9号", "川島如恵留", "ネックレス(LHME)"),
        ("TV station 2026年18号", "川島如恵留", "ネックレス(LHME)"),
        ("FINEBOYS 2026年10月号", "七五三掛龍也", "ブレスレット(NARRATIVEPLATOON)"),
    ])
    o += b.p("LHMEは、シルバーアクセサリーで有名な「LION HEART(ライオンハート)」のブランドです。",
             "川島如恵留は、LHMEのパールネックレスを2回着けています。")

    # ---- anan 2489
    o += b.h2("anan No.2489：松田元太はgramii")
    o += b.mini(("雑誌", "anan No.2489(2026年3月25日発売)・表紙"),
                ("メンバー", "松田元太(Snow Manの岩本照とのW表紙)"),
                ("ブランド", "gramii(グラミー)"),
                ("アイテム", "moonstone brass ring/ネックレス"))
    o += b.p("「推し旅」特集で、Snow Manの岩本照とW表紙を飾った号です。",
             "松田元太は、13〜17ページのスタイリングでgramiiのリングとネックレスを着けています。")
    o += b.table(("アイテム", "値段"), [
        ("moonstone brass ring", "8,800円"),
        ("ネックレス(白い天然石のビーズ)", "公式ショップで確認"),
    ])
    o += b.p("リングは、大きなムーンストーンを王冠のようなツメでとめたデザインです。",
             "gramiiのショップでは「松田元太さま衣装協力」と書かれた商品ページになっています。")
    o += M.fig("tj_2037133188443820376_0", "gramii_mf")
    o += M.fig("tj_2037133188443820376_2", "gramii_mf")

    o += aff("gramii(グラミー)のリング", "gramii リング", "#4a7fc1")
    # ---- J Movie
    o += b.h2("J Movie Vol.129：松倉海斗はLHME")
    o += b.mini(("雑誌", "J Movie Magazine Vol.129(2026年4月1日発売)"),
                ("メンバー", "松倉海斗"),
                ("ブランド", "LHME"),
                ("アイテム", "Moment 2wayベネチアンポイントハートネックレス/シルバー(2NE024A)"),
                ("値段", "6,050円(税込)"))
    o += b.p("細いベネチアンチェーンに、小さなハートのモチーフがついたネックレスです。",
             "2通りの着け方ができる2wayタイプで、サージカルステンレス製なので金属アレルギーにも配慮されています。")
    o += b.p("くわしくは、" + b.link("https://lionheart-store.com/cp/press/detail/321/", "LION HEART公式のPRESSページ") + "でも見られます。")

    o += aff("LHMEのハートネックレス", "LHME ライオンハート ハート ネックレス", "#4a7fc1")
    # ---- TV station 9
    o += b.h2("TV station 9号：川島如恵留はパール")
    o += b.mini(("雑誌", "TV station 2026年9号(関東版・4月11日〜24日号)"),
                ("メンバー", "川島如恵留"),
                ("ブランド", "LHME"),
                ("アイテム", "MELLOWスモールバロックパールネックレス/ゴールド(2NC027B)"),
                ("値段", "3,960円(税込)"))
    o += b.p("Travis Japanが巻頭インタビューに登場した号です。",
             "川島如恵留は、小さなバロックパールを連ねたネックレスを着けています。")
    o += M.fig("tj_2043660472168137176_1", "LHME2020")

    # ---- TV station 18
    o += b.h2("TV station 18号：川島如恵留はハーフバロックパール")
    o += b.mini(("雑誌", "TV station 2026年18号(関東版・8月15日〜28日号)"),
                ("メンバー", "川島如恵留"),
                ("ブランド", "LHME"),
                ("アイテム", "MELLOWハーフバロックパールネックレス/シルバー(2NC029A)"),
                ("値段", "4,620円(税込)"))
    o += b.p("川島如恵留と松田元太の連載ページで着けていたネックレスです。",
             "首の後ろはシルバーのチェーン、前側はパールになっていて、シャツにも合わせやすいデザインです。")
    o += b.p("同じネックレスは、SixTONESのメンバーも雑誌で着けています。")
    o += M.fig("tj_2092907474244272311_1", "LHME2020")

    o += aff("LHMEのバロックパールネックレス", "LHME バロックパール ネックレス", "#4a7fc1")
    # ---- FINEBOYS
    o += b.h2("FINEBOYS 10月号：七五三掛龍也は喜平のブレスレット")
    o += b.mini(("雑誌", "FINEBOYS 2026年10月号(2026年9月9日発売)・表紙"),
                ("メンバー", "七五三掛龍也"),
                ("ブランド", "NARRATIVEPLATOON(ナラティブプラトゥーン)"),
                ("アイテム", "VOLUME BRACELET GIGA"))
    o += b.p("七五三掛龍也が表紙を飾った号です。",
             "ボリュームのある喜平チェーンのブレスレットで、手元をはなやかに見せてくれます。")
    o += b.p("ブランドのオンラインショップの商品ページは、記事を書いた時点で見られなくなっていました。",
             "買いたい人は、ブランドの公式SNSで再販の情報をチェックしてみてください。")
    o += M.fig("tj_2097490177203523947_1", "NP_PRESS")

    o += aff("NARRATIVEPLATOON(ナラティブプラトゥーン)のブレスレット", "NARRATIVEPLATOON", "#4a7fc1")
    # ---- おまけ
    o += b.h2("雑誌以外では『陰ニモ日向ニモ』でJUSTIN DAVIS")
    o += b.p("雑誌ではありませんが、2ndシングル『陰ニモ日向ニモ』でもアクセが話題になりました。", "ミュージックビデオとアーティスト写真で、JUSTIN DAVISのネックレスを着けています。",
             "ブランドの発表では、宮近海斗と松田元太の名前が挙がっていました。")
    o += b.xembed("https://x.com/joat_jack/status/2024427846652088679")

    o += aff("JUSTIN DAVIS(ジャスティンデイビス)のネックレス", "JUSTIN DAVIS ネックレス", "#4a7fc1")
    # ---- 購入先
    o += b.h2("Travis Japanの雑誌着用アクセが買えるお店")
    o += b.p("紹介したアクセサリーは、ブランドの公式オンラインショップで買えます。",
             "完売していることもあるので、公式SNSの再入荷のお知らせもチェックしてみてください。")
    o += b.checks(["gramii:gramiiのBASEショップ",
                   "LHME(LION HEART):LION HEART公式オンラインストア",
                   "NARRATIVEPLATOON:ブランドの公式オンラインショップ・公式SNS",
                   "JUSTIN DAVIS:JUSTIN DAVIS公式オンラインストア"])

    # ---- まとめ
    o += b.h2("まとめ")
    o += b.checks(["松田元太はanan No.2489の表紙でgramiiのリングを着けた",
                   "川島如恵留はTV stationでLHMEのパールネックレスを2回着けた",
                   "松倉海斗はLHMEのハートのネックレスを着けた",
                   "七五三掛龍也はFINEBOYSの表紙で喜平のブレスレットを着けた"])
    o += b.p("LHMEのネックレスは4,000円前後からと、手に取りやすい値段なのがうれしいところです。",
             "推しとおそろいのアクセで、毎日のおしゃれを楽しんでみてくださいね。")
    return o


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "--build-only" not in sys.argv:
        M.ensure(IMGS)
    out = blogkit.finalize(build(), SITE, NAMES)
    if "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
