# -*- coding: utf-8 -*-
"""chomoand-2.com Snow Manの雑誌着用アクセまとめ2026(2026-11-21 オシリ依頼)。

根拠: ブランド公式Xの「着用いただきました」告知+LION HEART PRESSページ。調査メモ articles/mag_acc_2026_research.md。
第三者の特定投稿は使わない。値段はショップのページで確かめた分だけ書く。
    python tools/_build_upload_sm_mag_acc_2026_1121.py --build-only
    python tools/_build_upload_sm_mag_acc_2026_1121.py            # 【未】下書き投稿
    python tools/_build_upload_sm_mag_acc_2026_1121.py --update
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
from _mag_acc_2026_common import Media, NOTICE, aff  # noqa: E402

SITE = "snowman"
KEY = "sm_mag_acc_2026_1121"
TITLE = "Snow Manの雑誌着用アクセまとめ2026！ブランドや値段は？"
SLUG = "snow-man-magazine-accessories-2026"
CATEGORIES = [4, 6, 11, 13, 14]
NAMES = ["土屋太鳳"]
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "Snow Manの雑誌着用アクセまとめ2026"
X_TEXT = ""
X_TAGS = "#SnowMan"

LH = "https://lionheart-store.com/cp/press/detail/{}/"

b = blogkit.Blocks("#3f8fd2", "#cfe3f5", "#eef6fc")
M = Media(SITE, KEY, b)
IMGS = {
    "sm_2024341575942430942_2": "e.m.のストーンが並んだイヤーカフ",
    "sm_2055276546185932903_1": "ScatのHook bangle GOLD",
    "sm_2069688050083631286_1": "stlllのLattice ring",
    "sm_2096894996553031917_1": "LHMEのビジューY字ネックレス",
    "sm_2122887709048152239_0": "FADE,のTIGRIS knot pave ring",
    "sm_2123074554386075859_0": "objet sayokoのsilver925×クリスタルイヤーカフ",
}


def build():
    o = NOTICE
    o += b.p("Snow Manのメンバーは、雑誌のグラビアでもたくさんのアクセサリーを着けています。",
             "撮影のあと、ブランドの公式アカウントが「着用いただきました」と教えてくれることも多いです。")
    o += b.p("この記事では、" + b.mark("2026年に発売された雑誌で着用したアクセサリー") + "を、ブランドの公式発表をもとにまとめました。",
             "ブランド名・商品名と、ショップで確認できた値段も紹介します。")
    o += b.wakaru(["2026年の雑誌で着用したアクセの一覧",
                   "宮舘涼太が表紙のananで着けたリングとイヤーカフ",
                   "岩本照・佐久間大介・阿部亮平の着用アクセ",
                   "アクセを買えるお店"])

    # ---- 一覧
    o += b.h2("Snow Manの雑誌着用アクセ一覧【2026年】")
    o += b.p("まずは、2026年に発売された雑誌で着用したアクセサリーを、発売の順に表にまとめました。",
             "くわしくは、このあと雑誌ごとに紹介します。")
    o += b.table(("雑誌", "メンバー", "アクセ(ブランド)"), [
        ("美的 2026年4月号増刊", "佐久間大介", "ネックレス・イヤーカフ(e.m.)"),
        ("anan No.2489", "岩本照", "リング2点(kofulu)・ネックレス(TaTa)"),
        ("FINEBOYS 2026年6月号", "阿部亮平", "バングル・リング(Scat)"),
        ("anan No.2501", "宮舘涼太", "リング(stlll)・ネックレス(O-KI)"),
        ("月刊TVガイド 2026年10月号", "岩本照", "ネックレス(LHME)"),
        ("BARFOUT! LATE SUMMER 2026", "佐久間大介", "ネックレス・イヤーカフ(LHME)"),
        ("BARFOUT! EARLY AUTUMN 2026", "岩本照", "ネックレス(LHME)"),
        ("Ray 2026年11月号", "佐久間大介", "ネックレス(LHME)"),
        ("STAGE navi vol.116", "岩本照", "ネックレス(LHME)"),
        ("anan No.2520", "宮舘涼太", "リング3点・イヤーカフ・ネックレス(FADE,ほか)"),
    ])
    o += b.p("LHMEは、シルバーアクセサリーで有名な「LION HEART(ライオンハート)」のブランドです。",
             "2026年は、岩本照と佐久間大介が何度も着けています。")

    # ---- 美的
    o += b.h2("美的 2026年4月号増刊：佐久間大介はe.m.のネックレス")
    o += b.mini(("雑誌", "美的 2026年4月号増刊(SPECIAL EDITION)・表紙"),
                ("メンバー", "佐久間大介"),
                ("ブランド", "e.m.(イーエム)"),
                ("アイテム", "ネックレス 0401_an41/左耳 2401_er98/右耳 2001_er40"))
    o += b.p("ピンクの髪が印象的な美的の表紙では、e.m.のジュエリーを着けています。",
             "首元には一粒のストーンがついたシンプルなネックレス、耳にはストーンがぐるりと並んだイヤーカフです。")
    o += b.p("e.m.は、日本のジュエリーブランドです。",
             "公式アカウントが商品番号まで紹介してくれているので、公式サイトで番号を入れると同じものを探せます。")
    o += M.fig("sm_2024341575942430942_2", "em_grp_official")

    # ---- anan 2489
    o += aff("e.m.(イーエム)のネックレス", "e.m. イーエム ネックレス", "#3f8fd2")
    o += b.h2("anan No.2489：岩本照はkofuluとTaTa")
    o += b.mini(("雑誌", "anan No.2489(2026年3月25日発売)・表紙"),
                ("メンバー", "岩本照(松田元太とのW表紙)"),
                ("ブランド", "kofulu/TaTa"),
                ("アイテム", "リング2点・ゴールドのネックレス"))
    o += b.p("Travis Japanの松田元太とW表紙をかざった号です。",
             "岩本照は、13〜17ページで小さな天然石のリングを2つ着けています。")
    o += b.table(("ブランド", "アイテム", "値段"), [
        ("kofulu", "ローズクォーツ petit square(リング)", "7,800円"),
        ("kofulu", "byaubu ガーネット(リング)", "7,800円"),
        ("TaTa", "[ Basic ] necklace / spin anchor (gold)", "4,400円(税込)"),
    ])
    o += b.p("kofuluの値段は、ブランドの告知に書かれていた金額です。",
             "TaTaのネックレスは、細かいアンカーチェーンを使った定番のアイテムです。")
    o += b.xembed("https://x.com/kofulujewelry/status/2038873470227108145")
    o += b.xembed("https://x.com/_tata_atelier_/status/2037104209196433470")

    # ---- FINEBOYS
    o += aff("kofulu(コフル)のリング", "kofulu リング", "#3f8fd2")
    o += aff("TaTa(タタ)のネックレス", "TaTa ネックレス アトリエ", "#3f8fd2")
    o += b.h2("FINEBOYS 6月号：阿部亮平はScatのバングル")
    o += b.mini(("雑誌", "FINEBOYS 2026年6月号・表紙"),
                ("メンバー", "阿部亮平"),
                ("ブランド", "Scat(スキャット)"),
                ("アイテム", "\"Hook\" bangle(GOLD)/\"Chain\" link ring(GOLD)"))
    o += b.p("創刊40周年のFINEBOYSで、阿部亮平が表紙を飾った号です。",
             "手元には、ゴールドのバングルとチェーンの形をしたリングを着けています。")
    o += b.p("バングルは、2本の線をフックのように引っかけたデザインです。",
             "リングはチェーンのコマをつないだ形で、太めでも上品に見えます。")
    o += M.fig("sm_2055276546185932903_1", "_scat_official")

    # ---- anan 2501
    o += aff("Scat(スキャット)のバングル", "Scat バングル", "#3f8fd2")
    o += b.h2("anan No.2501：宮舘涼太のstlllのリングは即完売")
    o += b.mini(("雑誌", "anan No.2501(2026年6月24日発売)・表紙"),
                ("メンバー", "宮舘涼太"),
                ("ブランド", "stlll/O-KI"),
                ("アイテム", "Lattice ring/ネックレス"))
    o += b.p("「魅せるカラダ」特集で、宮舘涼太が表紙を飾った号です。",
             "表紙で着けているstlllの「Lattice ring」は、ひし形の格子もようが立体的に彫られたリングです。")
    o += b.p("このリングは、発売のあと" + b.mark("すぐに完売") + "しました。",
             "stlllは6月から7月にかけて再販を2回行っていて、ファンの反響の大きさがわかります。")
    o += b.p("同じ号では、O-KIのネックレスも着けています。",
             "表紙で重ねづけしているネックレスのうちの1本です。")
    o += M.fig("sm_2069688050083631286_1", "stlll_official")
    o += b.xembed("https://x.com/oki_jewelry/status/2074380464455037157")

    # ---- LHME 岩本
    o += aff("stlll(スティル)のリング", "stlll リング", "#3f8fd2")
    o += aff("O-KI(オーキ)のアクセ", "O-KI ジュエリー", "#3f8fd2")
    o += b.h2("岩本照はLHMEのネックレスを何度も着用")
    o += b.p("2026年の後半、岩本照は3冊の雑誌でLION HEARTのブランド「LHME」のネックレスを着けています。",
             "なかでも" + b.mark("ビジューY字ネックレスは2回") + "登場しました。")
    o += b.table(("雑誌", "アイテム", "値段(税込)"), [
        ("月刊TVガイド 2026年10月号", "ビジューY字ネックレス(2NC024A)", "7,480円"),
        ("BARFOUT! EARLY AUTUMN 2026", "MELLOWパールミックスボールチェーンネックレス ミディアム(2NC037A)", "5,500円"),
        ("STAGE navi vol.116", "ビジューY字ネックレス(2NC024A)", "7,480円"),
    ])
    o += b.p("ビジューY字ネックレスは、丸いパーツからジルコニアのバーが下がるデザインです。",
             "サージカルステンレス製で、金属アレルギーが心配な人にもうれしい素材です。")
    o += b.p("BARFOUT!では、白いパールと黒い玉を交互に並べたネックレスを着けています。",
             "くわしくは、" + b.link(LH.format(364), "LION HEART公式のPRESSページ") + "でも見られます。")
    o += M.fig("sm_2096894996553031917_1", "LHME2020")

    # ---- LHME 佐久間
    o += aff("LHME(ライオンハート)のネックレス", "LHME ライオンハート ネックレス", "#3f8fd2")
    o += b.h2("佐久間大介はLHMEのパールネックレスとイヤーカフ")
    o += b.p("佐久間大介も、2026年はLHMEのアクセサリーを2冊で着けています。")
    o += b.table(("雑誌", "アイテム", "値段(税込)"), [
        ("BARFOUT! LATE SUMMER 2026", "MELLOWパールミックスボールチェーンネックレス ラージ(2NC036A)", "5,500円"),
        ("BARFOUT! LATE SUMMER 2026", "チェーンドロップイヤーカフ 3連(2EC003I)", "3,300円"),
        ("Ray 2026年11月号", "Momentオーバルチェーンネックレス ハーフダブル(2NC032A)", "6,050円"),
    ])
    o += b.p("BARFOUT!は、土屋太鳳と2人で表紙を飾った号です。",
             "岩本照が着けたものと同じシリーズのパールネックレスで、こちらは一回り大きいラージサイズです。")
    o += b.xembed("https://x.com/LHME2020/status/2097257384678658314")

    # ---- anan 2520
    o += aff("LHMEのパールネックレス・イヤーカフ", "LHME パール ネックレス", "#3f8fd2")
    o += b.h2("anan No.2520：宮舘涼太は4ブランドのアクセを着用")
    o += b.mini(("雑誌", "anan No.2520(2026年11月18日発売)・表紙"),
                ("メンバー", "宮舘涼太"),
                ("ブランド", "FADE,/objet sayoko/vivid market/kulolecoco"),
                ("アイテム", "リング3点・イヤーカフ・ネックレス"))
    o += b.p("「ときめきギフト」特集で、宮舘涼太が表紙を飾った号です。",
             "この1冊だけで、" + b.mark("4つのブランドが着用を発表") + "しています。")
    o += b.table(("ブランド", "アイテム", "値段"), [
        ("FADE,", "TIGRIS | knot pave ring(SILVER)", "3,850円(税込)"),
        ("objet sayoko", "silver925×クリスタルイヤーカフ", "23,100円(税込)"),
        ("vivid market", "Halo Knot ring", "公式ショップで確認"),
        ("kulolecoco", "プリンセスリング Gold", "7,800円"),
        ("kulolecoco", "ロープチェーン Gold", "4,800円"),
    ])
    o += b.p("objet sayokoのイヤーカフは、表紙と14・16・17ページで着けています。",
             "クリスタルのしずくが揺れるデザインで、オンラインの即納分は残りわずかになっています。")
    o += b.p("vivid marketのリングは、16ページで右手の小指に着けています。",
             "パールのモチーフをあえて下向きにした着け方に、ブランドも感動したと話していました。")
    o += M.fig("sm_2122887709048152239_0", "fade__official")
    o += M.fig("sm_2123074554386075859_0", "objetsayoko")
    o += b.xembed("https://x.com/vividmarket2020/status/2123010605561118880")

    # ---- 購入先
    o += aff("FADE,(フェード)のアクセ", "FADE アクセサリー", "#3f8fd2")
    o += aff("objet sayoko(オブジェサヨコ)のイヤーカフ", "objet sayoko イヤーカフ", "#3f8fd2")
    o += aff("kulolecoco(クロレココ)のアクセ", "kulolecoco", "#3f8fd2")
    o += b.h2("Snow Manの雑誌着用アクセが買えるお店")
    o += b.p("紹介したアクセサリーは、どれもブランドの公式オンラインショップで買えます。",
             "人気のアイテムは完売や予約販売になることがあるので、早めにチェックしてみてください。")
    o += b.checks(["e.m.:公式オンラインショップ(商品番号で検索)",
                   "kofulu・Scat・O-KI・kulolecoco:各ブランドの公式ショップ・公式SNS",
                   "TaTa:TaTa online store",
                   "stlll:stlll公式オンラインストア(再販は公式SNSで告知)",
                   "LHME(LION HEART):LION HEART公式オンラインストア",
                   "FADE,:hemca(TIGRIS)",
                   "objet sayoko・vivid market:各ブランドのBASE・STORESのショップ"])

    # ---- まとめ
    o += b.h2("まとめ")
    o += b.checks(["2026年は、宮舘涼太が表紙のananで着けたアクセが特に話題になった",
                   "anan No.2501のstlllのリングは即完売し、2回再販された",
                   "岩本照と佐久間大介は、LHMEのネックレスを何度も着けている",
                   "1万円以下で買えるアイテムも多く、おそろいにしやすい"])
    o += b.p("雑誌のアクセは、手に取りやすい値段のものが多いのがうれしいところです。",
             "推しとおそろいのアクセで、毎日のコーデを楽しんでみてくださいね。")

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
