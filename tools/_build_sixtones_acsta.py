# -*- coding: utf-8 -*-
"""SixTONES アクスタ歴代一覧(chomoand-0.com)。2026-11-14 オシリとサジェスト穴場ファインダーの◎から作成。

    python tools/_build_sixtones_acsta.py              # 下書き投稿(【未】は blogkit が自動で付ける)
    python tools/_build_sixtones_acsta.py --build-only
    python tools/_build_sixtones_acsta.py --update
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "sixtones"
KEY = "sixtones_acsta_1114"
TITLE = "SixTONESのアクスタ歴代一覧！値段や今買える場所は？"
SLUG = "sixtones-acsta-list"
CATEGORIES = [15]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "SixTONESのアクスタ歴代一覧"

FEST = "https://x.com/SixTONESinfo/status/1568177247315689473"
ANNIV = "https://x.com/MerchCompany_jp/status/1914876890982297645"
STADIUM = "https://starto.jp/s/p/live/10499?artist=119"
NISSAN = "https://chomoand-0.com/sixtones-stadium-nissan-fashion-goods-1238"

b = blogkit.Blocks("#333333", "#d5d5d5", "#f5f5f5")
L = b.link
out = ""
out += b.p("SixTONESのアクスタ(アクリルスタンド)は、これまでに何種類か発売されてきました。",
           "いちばん新しいのは、2025年5月に出た" + b.mark("結成10周年の両面アクスタ(1,500円)") + "です。",
           "この記事では、歴代のアクスタと値段、今から手に入れる方法をまとめました。")
out += b.wakaru(["SixTONESの歴代アクスタ一覧",
                 "それぞれの値段と発売日",
                 "ツアーグッズにアクスタはある？",
                 "今アクスタを買える場所",
                 "アクスタの飾り方・持ち歩き方"])

out += b.h2("SixTONESの歴代アクスタ一覧")
out += b.table(("発売", "シリーズ", "値段"),
               [("2019年〜2020年", "ジャニーズ アイランドストア", "公式の記録が見つからず"),
                ("2022年9月", "Johnny's アクスタFest", "各1,200円"),
                ("2025年5月", "SixTONES AnniVERSARY 両面アクスタ", "各1,500円")])
out += b.p("大きく分けると、ジャニーズJr.時代のもの、デビュー後のオンライン限定のもの、結成10周年のものの3つです。",
           "どれもメンバー1人ずつの個人のアクスタで、6人分そろえて飾るファンも多いです。")
out += b.p("値段は、公式から発表された当時の値段です。",
           "今はフリマなどで、当時の値段より高く売られていることがあります。")

out += b.h2("ジャニーズJr.時代のアクスタ(アイランドストア)")
out += b.p("SixTONESがまだジャニーズJr.だったころ、Jr.のグッズのお店「ジャニーズ アイランドストア」でアクスタが売られていました。",
           "2019年に発売されたものが、SixTONESのアクスタの始まりと言われています。")
out += b.p("アイランドストアのアクスタは、2019年から2020年にかけて何回か発売されました。",
           "回ごとに衣装がちがうので、「第1弾」「20夏」のように呼び分けられています。")
out += b.mini(("いつ", "2019年〜2020年(デビュー前)"),
              ("どこで", "ジャニーズ アイランドストア"),
              ("今は", "販売終了。中古でしか手に入らない"))
out += b.p("デビュー前のアクスタなので、今では" + b.mark("Jr.時代の思い出がつまった貴重なグッズ") + "になっています。",
           "当時の値段は、公式の記録が見つからなかったので、ここでは書いていません。")

out += b.h2("Johnny's アクスタFest(2022年)")
out += b.p("2022年9月10日に、事務所のオンラインストア「Johnny's アクスタFest」がオープンしました。",
           "所属するグループのメンバーのアクスタが、いっせいに発売された企画です。")
out += b.mini(("発売日", "2022年9月10日(土)12時から"),
              ("値段", "各1,200円"),
              ("大きさ", "高さ110〜173mm・はば29〜94mm"),
              ("決まり", "1人1アイテム2点まで・数量限定・オンライン限定"))
out += b.p("販売の決まりは、当時こう案内されていました。",
           "アクセスが集中して、なかなか買えなかったという声も多かったアクスタです。")
out += b.p("参考:" + L(FEST, "SixTONES info(X)"))

out += b.h2("結成10周年の両面アクスタ(2025年)")
out += b.p("2025年5月1日、結成10周年の記念グッズ「SixTONES AnniVERSARY」が発売されました。",
           "その中の1つが、メンバー6人それぞれの" + b.mark("両面アクリルスタンド") + "です。")
out += b.mini(("発売日", "2025年5月1日(木)"),
              ("値段", "各1,500円(6種)"),
              ("どこで", "ファミクラストア(お店・オンライン)"),
              ("いっしょに出たグッズ", "オリジナルフォト・ステッカーセット・ミニフォトセット"))
out += b.p("5月1日は、SixTONESが結成した日です。",
           "記念日に合わせて出たアクスタなので、10周年の記念に買ったファンも多いグッズです。")
out += b.p("出典:" + L(ANNIV, "ファミクラストア(X)"))

out += b.h2("ツアーグッズにアクスタはある？")
out += b.p("2026年のツアー「MILESixTONES」のグッズには、アクスタは入っていません。",
           "スタジアムツアーのグッズは、フォトブック・うちわ・ユニフォーム・タオル・ステッカー・ペンライトです。")
out += b.p("ライブ会場でアクスタを買うことはできないので、気をつけましょう。",
           "日産スタジアム公演のグッズは" + L(NISSAN, "SixTONES日産スタジアムの服装は？開演時間とグッズも！") + "でまとめています。")
out += b.p("出典:" + L(STADIUM, "MILESixTONES(スタジアムツアー)｜STARTO ENTERTAINMENT"))

out += b.h2("今アクスタを買える場所")
out += b.h3("公式:ファミクラストア")
out += b.p("新しいアクスタが出るときは、公式のお店「ファミクラストア」で売られることが多いです。",
           "お店とオンラインの両方があります。")
out += b.p("結成10周年の両面アクスタは、ファミクラストアで売られていました。",
           "在庫があるかどうかは時期で変わるので、公式のサイトで確かめてください。")
out += b.h3("販売が終わったアクスタは中古で")
out += b.p("アイランドストアやアクスタFestのアクスタは、もう公式では売っていません。",
           "ほしい場合は、フリマアプリや中古のグッズのお店で探すことになります。")
out += b.checks(["当時の値段より高く売られていることが多い",
                 "台紙つきかどうかで値段が変わる",
                 "写真で傷や保護フィルムの有無を確かめる",
                 "公式ではない、にせものに気をつける"])
out += b.p("特に人気のメンバーや、数の少ないアクスタは値段が上がりやすいです。",
           "あせって高く買わないように、いくつかのお店を見くらべてから決めましょう。")

out += b.h2("アクスタの飾り方・持ち歩き方")
out += b.h3("6人そろえて飾る")
out += b.p("アクスタは、6人そろえて並べると一気にライブのステージのようになります。",
           "メンバーカラーの小物をいっしょに置くと、もっとはなやかになります。")
out += b.table(("メンバー", "メンバーカラー"),
               [("ジェシー", "赤"), ("京本大我", "ピンク"), ("松村北斗", "黒"),
                ("髙地優吾", "黄"), ("森本慎太郎", "緑"), ("田中樹", "青")])
out += b.h3("持ち歩くときはケースに")
out += b.p("アクスタを持ってカフェやライブに行き、写真をとるファンも多いです。",
           "持ち歩くときは、傷がつかないように専用のケースやポーチに入れましょう。")
out += b.p("アクリルは、こすれると細かい傷がつきやすい素材です。",
           "保護フィルムは、飾るときまではがさずにおくと、きれいなまま保てます。")

out += b.h2("SixTONESのアクスタについてよくある質問")
out += b.h3("新しいアクスタは出る？")
out += b.p("11月14日の時点で、新しいアクスタの発表はありません。",
           "これまでは記念日やオンラインの企画に合わせて出ていたので、次の記念日に出るかもしれません。")
out += b.h3("グループ全員のアクスタはある？")
out += b.p("ここで紹介したアクスタは、どれもメンバー1人ずつのものです。",
           "全員そろえたいときは、6種類を集めることになります。")

out += b.h2("まとめ")
out += b.checks(["SixTONESのアクスタはJr.時代のアイランドストアから始まった",
                 "2022年のアクスタFestは各1,200円",
                 "2025年の結成10周年の両面アクスタは各1,500円",
                 "2026年のツアーグッズにアクスタはない",
                 "販売が終わったアクスタは中古で探す"])
out += b.p("アクスタは、6人を並べるだけで部屋がSixTONESでいっぱいになるうれしいグッズです。",
           "新しいアクスタの発表があったら、この記事でもお知らせしますね。")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    import sixtones_theme
    out = blogkit.finalize(out, SITE, NAMES)
    out = out.replace('<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">',
                      '<div style="border:1px solid #d5d5d5;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">')
    out = sixtones_theme.per_section(out)
    if "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
