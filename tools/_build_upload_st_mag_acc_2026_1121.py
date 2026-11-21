# -*- coding: utf-8 -*-
"""chomoand-0.com SixTONESの雑誌着用アクセまとめ2026(2026-11-21 オシリ依頼。既存のアクセまとめID1359とは別記事)。

根拠: ブランド公式Xの「着用いただきました」告知+LION HEART PRESS/NEWSページ。調査メモ articles/mag_acc_2026_research.md。
無彩色で書いて、最後に sixtones_theme.per_section でメンカラにする。
    python tools/_build_upload_st_mag_acc_2026_1121.py --build-only
    python tools/_build_upload_st_mag_acc_2026_1121.py            # 【未】下書き投稿
    python tools/_build_upload_st_mag_acc_2026_1121.py --update
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
import sixtones_theme  # noqa: E402
from _mag_acc_2026_common import Media  # noqa: E402

SITE = "sixtones"
KEY = "st_mag_acc_2026_1121"
TITLE = "SixTONESの雑誌着用アクセまとめ2026！ブランドや値段は？"
SLUG = "sixtones-magazine-accessories-2026"
CATEGORIES = [15, 16, 17, 18, 19, 20, 21]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "SixTONESの雑誌着用アクセまとめ2026"
X_TEXT = ""
X_TAGS = "#SixTONES"

b = blogkit.Blocks("#333333", "#d5d5d5", "#f5f5f5")
M = Media(SITE, KEY, b)
IMGS = {
    "st_2008871244675043666_1": "LION HEARTのヴァーティカルコンフォートリング",
    "st_2018626518071833044_0": "MUのキューブ水晶と淡水パールのチェーンネックレス",
    "st_2018946830651064468_0": "TaTaのPearl rainブレスレット",
    "st_2050052938593394851_0": "FADE,のTIGRIS pave link necklace",
    "st_2098344548153872785_1": "LHMEのポイントパールダブルイヤーカフ",
    "st_2117846708701085809_0": "Spice Jewelryのbasil ring",
}


def build():
    o = ""
    o += b.p("SixTONESのメンバーは、雑誌のグラビアでもさまざまなアクセサリーを着けています。",
             "撮影のあと、ブランドの公式アカウントが「着用いただきました」と発表してくれることも多いです。")
    o += b.p("この記事では、" + b.mark("2026年に発売された雑誌で着用したアクセサリー") + "を、ブランドの公式発表をもとにまとめました。",
             "ブランド名・商品名と、ショップで確認できた値段も紹介します。")
    o += b.wakaru(["2026年の雑誌で着用したアクセの一覧",
                   "STAGE navi vol.108で5人が着けたアクセ",
                   "田中樹が表紙のananで着けたリング",
                   "アクセを買えるお店"])

    # ---- 一覧
    o += b.h2("SixTONESの雑誌着用アクセ一覧【2026年】")
    o += b.p("まずは、2026年に発売された雑誌で着用したアクセサリーを、発売の順に表にまとめました。",
             "くわしくは、このあと雑誌ごとに紹介します。")
    o += b.table(("雑誌", "メンバー", "アクセ(ブランド)"), [
        ("ViVi 2026年2・3月合併号", "松村北斗", "リング(LION HEART)"),
        ("VoCE 3月号 Special Edition", "田中樹", "ネックレス(TaTa)"),
        ("STAGE navi vol.108", "京本・松村・髙地・森本・田中", "リング・ネックレス・ブレスレット(5ブランド)"),
        ("anan No.2487", "松村北斗", "ネックレス(Daisy Lewis)"),
        ("anan No.2494", "髙地優吾・森本慎太郎", "ネックレス(FADE,)・バングル(four seven nine)"),
        ("CanCam 2026年7月号", "京本大我", "リング(LION HEART)"),
        ("BAILA 2026年10月号", "ジェシー", "イヤーカフ(LHME)"),
        ("anan No.2518", "田中樹", "リング4点(e.m.ほか)・ネックレス(LION HEART)"),
        ("CanCam 2027年1月号 特別版", "松村・田中・森本", "リング・ピアス(e.m.)"),
    ])
    o += b.p("田中樹は、1年を通していちばん多くのアクセを着けていました。",
             "6人全員が、少なくとも1回はブランドから着用を発表されています。")

    # ---- ViVi
    o += b.h2("ViVi 2・3月合併号：松村北斗はLION HEARTのリング")
    o += b.mini(("雑誌", "ViVi 2026年2・3月合併号"),
                ("メンバー", "松村北斗"),
                ("ブランド", "LION HEART(ライオンハート)"),
                ("アイテム", "\"for Gift\"ヴァーティカルコンフォートリング/シルバー925"),
                ("値段", "25,300円(税込)"))
    o += b.p("ViViの「国宝級イケメンランキング」の号で、松村北斗が着けていたリングです。",
             "丸い面が平らになった、シグネットリングのような形をしています。")
    o += M.fig("st_2008871244675043666_1", "lion_accessory")

    # ---- VoCE
    o += b.h2("VoCE 3月号：田中樹はTaTaのゴールドネックレス")
    o += b.mini(("雑誌", "VoCE 2026年3月号 Special Edition"),
                ("メンバー", "田中樹"),
                ("ブランド", "TaTa"),
                ("アイテム", "[ Basic ] necklace / spin anchor (gold)"),
                ("値段", "4,400円(税込)"))
    o += b.p("細かいアンカーチェーンを使った、ゴールドのネックレスです。",
             "同じネックレスは、Snow Manの岩本照もanan No.2489で着けています。")
    o += b.xembed("https://x.com/_tata_atelier_/status/2014560669564338476")

    # ---- STAGE navi 108
    o += b.h2("STAGE navi vol.108：5人がパールのアクセを着用")
    o += b.mini(("雑誌", "STAGE navi vol.108(2026年1月28日発売)・表紙"),
                ("メンバー", "京本大我・松村北斗・髙地優吾・森本慎太郎・田中樹"),
                ("ブランド", "LHME/TaTa/Pearl for Life/MU/Mamimi"))
    o += b.p("デビュー6周年を記念して、SixTONESが表紙を飾った号です。",
             "白いパールのアクセサリーが多く、5人それぞれに別のブランドが着用を発表しています。")
    o += b.table(("メンバー", "アイテム(ブランド)", "値段"), [
        ("京本大我", "Carina あこや真珠 トリプルリング(Pearl for Life)", "公式ショップで確認"),
        ("京本大我", "[ Pearl rain ] bracelet(TaTa)", "5,500円(税込)"),
        ("松村北斗", "[ Basic ] pearl bracelet / large(TaTa)", "4,400円(税込)"),
        ("松村北斗・森本慎太郎", "MELLOWパールミックスボールチェーンネックレス(LHME)", "5,500円(税込)"),
        ("松村北斗・森本慎太郎", "MELLOWハーフバロックパールネックレス(LHME)", "4,620円(税込)"),
        ("髙地優吾", "Supple あこや真珠 ハーフブレスレット(Pearl for Life)", "公式ショップで確認"),
        ("田中樹", "キューブ水晶&淡水パールチェーンネックレス(MU)", "10,450円(税込)"),
        ("田中樹", "ゴールドのビーズリング(Mamimi)", "公式SNSで確認"),
    ])
    o += b.p("田中樹のネックレスは、表紙と裏表紙で着けています。",
             "Mamimiのビーズリングは、中ページの3・6・13ページで左手の人差し指に着けています。")
    o += b.p("LHMEのネックレスは、松村北斗と森本慎太郎の2人に着用が発表されています。",
             "どちらがどのネックレスを着けたかは、発表には書かれていませんでした。")
    o += M.fig("st_2018626518071833044_0", "mu_accessory")
    o += M.fig("st_2018946830651064468_0", "_tata_atelier_")

    # ---- anan 2487
    o += b.h2("anan No.2487：松村北斗はDaisy Lewis")
    o += b.mini(("雑誌", "anan No.2487(2026年3月11日発売)"),
                ("メンバー", "松村北斗"),
                ("ブランド", "Daisy Lewis"),
                ("アイテム", "コンビマンテルネックレス(ステンレス)"),
                ("値段", "5,500円"))
    o += b.p("シルバーのねじれたチェーンと、ゴールドのチェーンを1本につないだネックレスです。",
             "ステンレス製なので、水や汗に強いのも特長です。")
    o += b.xembed("https://x.com/Daisylewis_ad/status/2031663028018749680")

    # ---- anan 2494
    o += b.h2("anan No.2494：髙地優吾と森本慎太郎はFADE,")
    o += b.mini(("雑誌", "anan No.2494(2026年5月1日発売)"),
                ("メンバー", "髙地優吾・森本慎太郎"),
                ("ブランド", "FADE,/four seven nine"),
                ("アイテム", "TIGRIS | pave link necklace(色違い)/純銀バングル 02-155"))
    o += b.p("髙地優吾と森本慎太郎は、FADE,の同じネックレスを" + b.mark("色違いで") + "着けています。",
             "大きなチェーンの一部に、キラキラのストーンを敷きつめたデザインです。")
    o += b.table(("アイテム", "メンバー", "値段"), [
        ("TIGRIS | pave link necklace(FADE,)", "髙地優吾・森本慎太郎", "5,500円(税込)"),
        ("純銀バングル 02-155(four seven nine)", "髙地優吾", "公式ショップで確認"),
    ])
    o += b.p("FADE,のネックレスは、6月のCDTVで田中樹も着けて話題になりました。",
             "four seven nineのバングルは、ブランドでいちばんボリュームのある3連風のデザインです。", "髙地優吾は、中づり広告でもこのバングルを着けています。")
    o += M.fig("st_2050052938593394851_0", "fade__official")

    # ---- CanCam 7
    o += b.h2("CanCam 7月号：京本大我はLION HEARTのリング")
    o += b.mini(("雑誌", "CanCam 2026年7月号(連載ページ)"),
                ("メンバー", "京本大我"),
                ("ブランド", "LION HEART"),
                ("アイテム", "\"for Gift\"槌目フラットリング/シルバー925"),
                ("値段", "17,600円(税込)"))
    o += b.p("表面をつちでたたいたような、手づくり感のある平たいリングです。",
             "シンプルなので、ほかのリングとも重ねづけしやすいアイテムです。")
    o += b.xembed("https://x.com/lion_accessory/status/2062829280485077118")

    # ---- BAILA
    o += b.h2("BAILA 10月号：ジェシーはLHMEのイヤーカフ")
    o += b.mini(("雑誌", "BAILA 2026年10月号 特別版・表紙"),
                ("メンバー", "ジェシー"),
                ("ブランド", "LHME"),
                ("アイテム", "MELLOWポイントパールダブルイヤーカフ/シルバー(2EC015A)"),
                ("値段", "4,400円(税込)"))
    o += b.p("BAILAの25周年の号で、SixTONESが表紙を飾りました。",
             "ジェシーが着けたのは、2本のラインにパールを1粒あしらったイヤーカフです。")
    o += M.fig("st_2098344548153872785_1", "LHME2020")

    # ---- anan 2518
    o += b.h2("anan No.2518：田中樹はリング4点とネックレス")
    o += b.mini(("雑誌", "anan No.2518(2026年11月4日発売)・表紙"),
                ("メンバー", "田中樹"),
                ("ブランド", "e.m./Spice Jewelry/LION HEART"))
    o += b.p("田中樹がソロで表紙を飾った号です。",
             "この1冊で、" + b.mark("3つのブランドが着用を発表") + "しています。")
    o += b.table(("アイテム(ブランド)", "値段"), [
        ("リング 2103-AR1083(e.m.)", "40,700円(税込)"),
        ("リング 2403-AR1199(e.m.)", "公式ショップで確認"),
        ("リング 2403-AR1203(e.m.)", "公式ショップで確認"),
        ("basil ring K10YG(Spice Jewelry)", "104,500円"),
        ("ネックレス(LION HEART)", "公式ショップで確認"),
    ])
    o += b.p("Spice Jewelryのbasil ringは、K10のイエローゴールドで作られたリングです。",
             "スーツ姿と黒い衣装のカットの両方で、左手の小指に着けています。")
    o += M.fig("st_2117846708701085809_0", "spicejewelry22")
    o += b.xembed("https://x.com/em_grp_official/status/2117813171906118021")

    # ---- CanCam 2027/1
    o += b.h2("CanCam 2027年1月号：3人がe.m.を着用")
    o += b.mini(("雑誌", "CanCam 2027年1月号 特別版(45周年号)・表紙"),
                ("メンバー", "松村北斗・田中樹・森本慎太郎"),
                ("ブランド", "e.m."))
    o += b.p("CanCamの45周年を記念した号で、SixTONESが特別版の表紙を飾りました。",
             "3人がe.m.のアクセサリーを着けています。")
    o += b.table(("メンバー", "アイテム"), [
        ("松村北斗", "0501-AR88B"),
        ("田中樹", "EMEV-AR559(刻印できるリング)"),
        ("森本慎太郎", "1604-AP508"),
    ])
    o += b.p("e.m.の公式サイトで商品番号を入れると、同じアイテムを探せます。")
    o += b.xembed("https://x.com/em_grp_official/status/2123653490706952287")

    # ---- 購入先
    o += b.h2("SixTONESの雑誌着用アクセが買えるお店")
    o += b.p("紹介したアクセサリーは、どれもブランドの公式オンラインショップで買えます。",
             "人気のアイテムは完売や再入荷待ちになることがあるので、公式SNSもチェックしてみてください。")
    o += b.checks(["LION HEART・LHME:LION HEART公式オンラインストア",
                   "TaTa:TaTa online store",
                   "e.m.:e.m.公式オンラインショップ(商品番号で検索)",
                   "FADE,:hemca(TIGRIS)",
                   "Pearl for Life:WSP公式サイト",
                   "MU・Daisy Lewis・Spice Jewelry:各ブランドのBASE・STORESのショップ",
                   "four seven nine・Mamimi:各ブランドの公式ショップ・公式SNS"])

    # ---- まとめ
    o += b.h2("まとめ")
    o += b.checks(["2026年は、6人全員が雑誌でのアクセ着用を発表されている",
                   "STAGE navi vol.108では、5人がパールのアクセを着けた",
                   "田中樹はananの表紙でリング4点とネックレスを着けた",
                   "5,000円前後で買えるアイテムも多い"])
    o += b.p("同じアクセでも、メンバーによって着け方がちがうのが見ていて楽しいところです。",
             "気になるアイテムがあったら、おそろいで着けてみてくださいね。")
    return o


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "--build-only" not in sys.argv:
        M.ensure(IMGS)
    out = blogkit.finalize(build(), SITE, NAMES)
    out = sixtones_theme.per_section(out)
    if "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
