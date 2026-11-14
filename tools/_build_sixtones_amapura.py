# -*- coding: utf-8 -*-
"""SixTONES アマプラ(Prime Video)で見られる作品まとめ(chomoand-0.com)。2026-11-14 サジェスト穴場◎から。

    python tools/_build_sixtones_amapura.py              # 下書き投稿(【未】は blogkit が自動で付ける)
    python tools/_build_sixtones_amapura.py --build-only
    python tools/_build_sixtones_amapura.py --update
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "sixtones"
KEY = "sixtones_amapura_1114"
TITLE = "SixTONESをアマプラで見るなら？おすすめ作品5つを紹介！"
SLUG = "sixtones-amazon-prime-video"
CATEGORIES = [15, 16]
NAMES = ["福本莉子", "渡辺いっけい", "戸次重幸", "南果歩", "黒谷友香", "石田ひかり", "笹野高史", "大友花恋"]
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "SixTONESがアマプラで見られる作品"

WAROTA1 = "https://www.primevideo.com/detail/0HNNIY9RLGA7DS25BK3LUUQHZA/"
WAROTA2 = "https://www.primevideo.com/detail/0K34UH73VVWUDIC1KZWMZA6DG0"
RIDE = "https://www.primevideo.com/-/ja/detail/0I9SOMVCJPMCCCEN63BABWB8RR/ref=atv_dp_season_select_s4"
OJOU = "https://www.aboutamazon.jp/news/entertainment/amazon-prime-video-new-content-april-2026"
STASON = "https://x.com/SixTONES_SME/status/2095474390523687255"

b = blogkit.Blocks("#333333", "#d5d5d5", "#f5f5f5")
L = b.link
out = ""
out += b.p("Amazonプライム・ビデオ(アマプラ)では、SixTONESが出ている作品をいくつも見られます。",
           "いちばんのおすすめは、SixTONESが本気でコントにいどむ" + b.mark("アマプラ限定の番組『ワロタ！』") + "です。",
           "この記事では、アマプラで見られるSixTONESの作品をまとめました。")
out += b.wakaru(["アマプラで見られるSixTONESの作品一覧",
                 "コント番組『ワロタ！』の見どころ",
                 "デビュー前後に密着したドキュメンタリー",
                 "メンバーが出ている映画",
                 "見るときの注意(見放題かどうか)"])

out += b.h2("アマプラで見られるSixTONESの作品一覧")
out += b.table(("作品", "どんな作品？"),
               [("ワロタ！", "6人のコント番組(2025年)"),
                ("ワロタ！SEASON2", "コント番組の続き(2026年)"),
                ("RIDE ON TIME", "SixTONESに密着したドキュメンタリー"),
                ("Star Song Special", "歌番組。SixTONESが1回出演"),
                ("お嬢と番犬くん", "ジェシーさん主演の映画")])
out += b.p("SixTONESの6人が出ている作品と、メンバーが出ている作品を合わせて、5つ紹介します。",
           "アマプラの作品は時期によって入れかわるので、11月14日の時点の情報です。")

out += b.h2("SixTONESのコント番組『ワロタ！』")
out += b.p("『ワロタ！』は、SixTONESが毎回豪華なゲストをむかえて、本格的なコントにいどむ番組です。",
           "アマプラだけで見られる番組で、テレビでは放送されていません。")
out += b.h3("シーズン1(2025年)")
out += b.mini(("配信", "2025年7月18日〜9月26日"),
              ("話数", "全6話(2週間に1回、金曜日に配信)"),
              ("ゲスト", "渡辺いっけいさん・戸次重幸さん・南果歩さん・黒谷友香さんなど"))
out += b.p("ドラマや映画で活躍する俳優さんが、ゲストとしてコントに参加しました。",
           "ふだんの歌やダンスとはちがう、6人の体当たりの演技が見られます。")
out += b.p("作品ページ:" + L(WAROTA1, "Prime Video『ワロタ！』"))
out += b.h3("シーズン2(2026年)")
out += b.mini(("配信", "2026年7月29日〜8月19日"),
              ("話数", "全8話(毎週水曜日に2話ずつ)"),
              ("ゲスト", "石田ひかりさん・笹野高史さん・大友花恋さんなど"))
out += b.p("シーズン2では、シーズン1のコントの続きに加えて、新しいコントもたくさん作られました。",
           "ジェシーさんは、コント「トオルとマサヤ」を見た人から「筋肉よく育ったね」と言われたと話しています。")
out += b.p("作品ページ:" + L(WAROTA2, "Prime Video『ワロタ！SEASON2』"))
out += b.h3("見どころはシリーズのコント")
out += b.p("『ワロタ！』には、何回にも分けて続く「シリーズのコント」があります。",
           "「SAT」や「寝る前に」「トオルとマサヤ」などは、回をまたいで話が進みます。")
out += b.p("シリーズのコントは、" + b.mark("1話から順番に見る") + "と、話のつながりがわかってもっと楽しめます。",
           "シーズン1とシーズン2を合わせると全14話なので、一気に見るのもおすすめです。")

out += b.h2("デビュー前後に密着『RIDE ON TIME』")
out += b.p("『RIDE ON TIME』は、アーティストのうらがわに密着するドキュメンタリーです。",
           "アマプラでは、SixTONESに密着した回も見られます。")
out += b.table(("話", "内容"),
               [("13話 TONE", "2枚目のアルバム『CITY』を作るようす"),
                ("14話 ism", "ユニット曲のダンス練習やラジオ出演"),
                ("15話 TONES", "アルバムのレコーディング"),
                ("16話 Six", "ツアー『Feel da CITY』横浜公演のうら側")])
out += b.p("この4話は、シーズン4の「SixTONES〜2年目の本音〜」です。",
           "デビュー2年目の6人が、どんな思いで音楽を作っていたのかがわかります。")
out += b.p("ライブのステージだけでは見られない、" + b.mark("6人の本音やうらがわ") + "が見られるのが魅力です。",
           "メンバーのふるさとや母校をたずねる場面もあります。")
out += b.p("作品ページ:" + L(RIDE, "Prime Video『RIDE ON TIME』シーズン4"))

out += b.h2("歌番組『Star Song Special』")
out += b.p("アマプラの歌番組『Star Song Special』シーズン3の12話に、SixTONESが出演しました。",
           "2026年9月に配信され、「Dance Forever」をフルサイズで歌っています。")
out += b.p("テレビの歌番組では短く切られることが多い曲を、最後まで聴けるのがうれしいポイントです。",
           "出典:" + L(STASON, "SixTONES / ソニーミュージック(X)"))

out += b.h2("ジェシー主演の映画『お嬢と番犬くん』")
out += b.p("ジェシーさんが、福本莉子さんとダブル主演した映画です。",
           "2026年4月24日から、アマプラで見放題の独占配信が始まりました。")
out += b.mini(("出演", "福本莉子さん・ジェシーさん(ダブル主演)"),
              ("ジャンル", "学園ラブコメディ"),
              ("アマプラ", "2026年4月24日から見放題で独占配信"))
out += b.p("ジェシーさんの役は、年齢をいつわって高校に入学した、過保護な世話係の若頭です。",
           "番犬のようにヒロインを守る姿が、かっこよくて少しおかしい作品です。")
out += b.p("出典:" + L(OJOU, "About Amazon Japan"))

out += b.h2("どれから見る？おすすめの順番")
out += b.p("はじめてSixTONESの作品を見る人には、次の順番がおすすめです。",
           "気になったところから見ても、もちろん大丈夫です。")
out += b.table(("順番", "作品", "おすすめの理由"),
               [("1", "ワロタ！", "6人の仲のよさと明るさがわかる"),
                ("2", "Star Song Special", "歌のかっこよさを1曲で感じられる"),
                ("3", "RIDE ON TIME", "音楽にかける本気の思いがわかる"),
                ("4", "お嬢と番犬くん", "ジェシーさんの演技を楽しめる")])
out += b.p("まずは『ワロタ！』で、6人のキャラクターをつかむのがおすすめです。",
           "コントで笑ったあとに『RIDE ON TIME』を見ると、真剣な表情とのちがいにおどろくはずです。")
out += b.p("ファンの方は、ライブの前に『RIDE ON TIME』を見直すのもよいでしょう。",
           "6人がどんな思いでステージに立っているのかを知ると、ライブがもっと楽しくなります。")

out += b.h2("アマプラで見るときの注意")
out += b.h3("見放題かどうかを確かめる")
out += b.p("アマプラの作品には、プライム会員なら追加のお金なしで見られる「見放題」の作品と、レンタルや購入が必要な作品があります。",
           "作品ページで、プライムのマークや「見放題」の表示があるかを確かめてから見ましょう。")
out += b.h3("配信が終わることもある")
out += b.p("アマプラの作品は、時期によって配信が終わることがあります。",
           "見たい作品は、早めに見ておくのが安心です。")
out += b.h3("メンバーの名前で探すのが早い")
out += b.p("アマプラの検索で、メンバーの名前を入れると、出ている作品がまとめて出てきます。",
           "新しく配信が始まった作品も見つけやすいので、ときどき検索してみましょう。")

out += b.h2("まとめ")
out += b.checks(["アマプラ限定のコント番組『ワロタ！』はシーズン2まで全14話",
                 "『RIDE ON TIME』でデビュー2年目の6人の本音が見られる",
                 "『Star Song Special』で「Dance Forever」をフルサイズで",
                 "ジェシー主演の映画『お嬢と番犬くん』は見放題で独占配信",
                 "見放題かどうかは作品ページで確かめる"])
out += b.p("歌って踊るSixTONESもかっこいいですが、コントで全力でふざける6人も見のがせません。",
           "まだ見ていない人は、まず『ワロタ！』の1話から見てみてくださいね。")

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
