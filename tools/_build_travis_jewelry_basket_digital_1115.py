# -*- coding: utf-8 -*-
"""トラジャ4thアルバム『Jewelry Basket』配信はいつから?全12曲とPOP STAR(chomoand-4.blog)。2026-11-15 発信あつめから。

    python tools/_build_travis_jewelry_basket_digital_1115.py              # 下書き投稿
    python tools/_build_travis_jewelry_basket_digital_1115.py --build-only
    python tools/_build_travis_jewelry_basket_digital_1115.py --update
配信が始まったら、配信サービスの一覧と始まった時刻を --update で足す。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "travis"
KEY = "travis_jewelry_basket_digital_1115"
TITLE = "Jewelry Basket配信はいつ？全12曲とPOP STARも！"
SLUG = "travis-japan-jewelry-basket-digital-release"
CATEGORIES = [3]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch_canva.jpg")
EYECATCH_ALT = "Travis Japan Jewelry Basketの配信"

X_COUNT = "https://twitter.com/TravisJapan_cr/status/2121528567528067512"
X_SHU1 = "https://twitter.com/TravisJapan_cr/status/2121409520748675081"
LNK = "https://travisjapan.lnk.to/JewelryBasketAL"
RS = "https://realsound.jp/2026/10/post-2550618.html"
SITE_URL = "https://chomoand-4.blog/"

b = blogkit.Blocks("#7e57c2", "#d9cdee", "#f5f2fb")
L = b.link
out = ""
out += b.p("Travis Japanの4thアルバム『Jewelry Basket』は、" + b.mark("11月18日(水)から配信") + "がスタートします。",
           "CDは12月16日(水)に発売がのびましたが、配信は予定どおりです。",
           "11月14日(土)には『シューイチ』で、リード曲「POP STAR」が地上波で初めて披露されました。")
out += b.p("この記事では、配信の日にちと聴き方、全12曲、そして「POP STAR」の見どころをまとめました。",
           "※2026年11月15日時点の情報です。")
out += b.wakaru(["アルバムの配信はいつから？",
                 "どこで聴ける？配信とCDのちがい",
                 "全12曲の曲名",
                 "『シューイチ』で初披露した「POP STAR」",
                 "配信日の前後に見られる番組"])

out += b.h2("Jewelry Basketの配信はいつから？")
out += b.mini(("作品", "4thアルバム『Jewelry Basket』"),
              ("配信", "2026年11月18日(水)から"),
              ("CD", "2026年12月16日(水)発売(11月18日からのびた)"),
              ("曲数", "全12曲"),
              ("リード曲", "POP STAR"))
out += b.p("配信が始まるのは、11月18日(水)です。",
           "公式Xでは、11月14日(土)に「あと4日」とカウントダウンの投稿がありました。")
out += b.xembed(X_COUNT)
out += b.h3("配信は何時から？")
out += b.p("11月15日の時点で、配信が始まる時刻は発表されていません。",
           "音楽の配信は、発売日の0時に一斉に始まることが多いです。",
           "17日(火)の夜から18日(水)に日付が変わるころに、配信サービスを開いてみるとよさそうです。")
out += b.p("同じ日の深夜には、日本テレビ『上田と女DEEP』の音楽コーナー「夜の音」にTravis Japanが出演します。",
           "番組を見ながら、配信開始を待つ人も多そうです。")

out += b.h2("どこで聴ける？配信とCDのちがい")
out += b.p("配信のリンクは、公式がまとめたページから選べます。",
           "ふだん使っている音楽アプリを選ぶと、そのまま聴いたり、ダウンロードしたりできます。")
out += b.p("出典:" + L(LNK, "Travis Japan『Jewelry Basket』公式配信リンク"))
out += b.h3("配信で買ってもイベントには申しこめない")
out += b.p("気をつけたいのは、発売記念イベントの応募です。",
           "応募券は" + b.mark("CDの中にだけ") + "入っています。",
           "配信で聴いたり買ったりしても、イベントには申しこめません。")
out += b.p("CDの発売がのびた理由や、イベントの新しい応募期間は " +
           L(SITE_URL + "travis-japan-jewelry-basket-cd-postponed-2505", "トラジャのアルバムCD延期はなぜ？発売記念イベントはどうなる？") +
           " でまとめています。")
out += b.table(("", "配信", "CD"),
               [("いつから", "11月18日(水)", "12月16日(水)"),
                ("イベント応募", "できない", "できる(応募券入り)"),
                ("特典映像", "なし", "形によってあり")])

out += b.h2("全12曲の曲名")
out += b.p("収録曲は、10月に公開されたトラックリストで発表されています。",
           "全部の形で、同じ12曲が入ります。")
out += b.table(("曲順", "曲名"),
               [("1", "POP STAR(リード曲)"), ("2", "EGO"), ("3", "Idolights"), ("4", "Homie"),
                ("5", "Synchronization"), ("6", "きゅんTiger"), ("7", "Good Vibes"), ("8", "陰ニモ日向ニモ"),
                ("9", "カタオモイの体温"), ("10", "LOVE ME DO"), ("11", "チェックメイト"), ("12", "365")])
out += b.p("出典:" + L(RS, "Real Sound(2026年10月)"))
out += b.p("2曲目の「EGO」は、ひと足早く10月12日から配信されています。",
           "「愛することはエゴなのか」という問いを描いた、ダンスのラブソングです。",
           "振り付けを担当した人は " + L(SITE_URL + "travis-japan-ego-choreographer-2180", "トラジャのEGOの振付師は誰？") +
           " で紹介しています。")
out += b.p("リード曲の「POP STAR」は1曲目に入っています。",
           "アルバムを再生すると、最初に流れるのがこの曲です。")

out += b.h2("『シューイチ』で初披露した「POP STAR」")
out += b.p("11月14日(土)、7人は日本テレビ『シューイチ』に生出演しました。",
           "ここで、リード曲の「POP STAR」を" + b.mark("地上波で初めて") + "披露しています。",
           "放送のあと、公式Xにはスタジオでの7人の写真が投稿されました。")
out += b.xembed(X_SHU1)
out += b.h3("白い衣装がキラキラ")
out += b.p("写真の7人は、そろって白いセットアップの衣装を着ています。",
           "ジャケットには、シルバーのビーズやチェーンのような飾りがたくさん付いていました。",
           "アルバム名の『Jewelry Basket(宝石のかご)』に合わせたような、宝石っぽい衣装です。")
out += b.p("全員が白い靴までそろえていて、遠くからでも目をひくコーディネートでした。",
           "スタジオのあかるいセットの中でも、7人の衣装がひときわ光って見えます。")
out += b.h3("MVの公開はまだ")
out += b.p("公式Xは、投稿の最後に「MV公開もお楽しみに」と書いています。",
           "11月15日の時点で、「POP STAR」のMVの公開日は発表されていません。",
           "配信開始の11月18日前後に公開される可能性もあるので、公式YouTubeの通知をオンにしておくと安心です。")

out += b.h2("配信日の前後に見られる番組")
out += b.p("配信の週は、7人そろっての出演がいくつかあります。")
out += b.table(("日時", "番組"),
               [("11/16(月)23:00", "けるとめる(フジテレビ)"),
                ("11/18(水)1:14", "上田と女DEEP「夜の音」(日本テレビ)"),
                ("11/28(土)", "ベストアーティスト(日本テレビ)")])
out += b.p("『上田と女DEEP』の「夜の音」では、3曲を披露する予定です。",
           "くわしい時間は " + L(SITE_URL + "travis-japan-tv-schedule-1115-1121-2572", "トラジャのテレビ出演は？11/15〜21の放送予定まとめ") +
           " でまとめています。")

out += b.h2("よくある質問")
out += b.h3("CDの予約はそのままでいい？")
out += b.p("はい、予約したCDはそのまま有効です。",
           "発売日が12月16日(水)に変わっただけなので、キャンセルや予約のしなおしは必要ありません。",
           "お店から別の案内が来たときは、その内容にしたがいましょう。")
out += b.h3("イベントの応募はいつ？")
out += b.p("CDに入っている応募券での応募は、12月15日(火)10時から12月20日(日)23時59分までです。",
           "当選の発表は、2027年1月13日(水)の12時です。",
           "イベントは1月20日(水)に大阪、1月27日(水)に神奈川で行われます。")
out += b.p("通販で予約した人は、CDが届く日を確かめておきましょう。",
           "届くのがおそいと、6日間しかない応募期間に間にあわないおそれがあります。")
out += b.h3("配信だけで全部の曲が聴ける？")
out += b.p("はい、配信でもCDと同じ12曲が聴けます。",
           "ちがうのは、CDの形ごとに付く特典映像や、イベントの応募券です。",
           "曲を早く聴きたい人は配信、イベントや映像も楽しみたい人はCDも、という選び方ができます。")

out += b.h2("まとめ")
out += b.checks(["『Jewelry Basket』の配信は11月18日(水)から(時刻は未発表)",
                 "CDは12月16日(水)発売。イベントの応募はCDだけ",
                 "全12曲、リード曲は「POP STAR」",
                 "11月14日の『シューイチ』で「POP STAR」を地上波初披露",
                 "MVの公開日はまだ発表されていない"])
out += b.p("CDが届くまで1か月待つことになりましたが、曲は一足先に聴けます。",
           "18日は、7人の新しい12曲をたっぷり楽しみたいですね。")

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
