# -*- coding: utf-8 -*-
"""anan AWARD 2026(2026-11-14 授賞式・ニューヒーロー部門)でKEY TO LITが着けていたアクセ 4本(chomoand-5.site)。

    python tools/_build_ktl_anan_acc_1116.py iwasaki|reia_glasses|reia_cuff|mizuki [--build-only|--update]
    python tools/_build_ktl_anan_acc_1116.py all

きっかけはオシリが送ったXの投稿(@_KTLs_outfits_ = 他人の特定アカウント)。記事では画像も名前も出さない。
人物の写真は anan公式YouTube「【生配信アーカイブ】anan AWARD 2026 授賞式」(FZCoDW52xXA)のコマ。
商品: スワロフスキー公式/正規店の表記、Wanderlust公式(韓国)のページで確認(2026-11-16)。
楽天APIはこのPCのIPが許可されず403 → 楽天は検索結果ページへのアフィリエイトリンク(草津記事と同じ方式)。
"""
import json
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
import affiliate_box as ab  # noqa: E402
import affiliate_linker as al  # noqa: E402
from _ktl_items_lib import p, mark, h2, h3, learn, info, checks, buy, table  # noqa: E402
from _upload_ktl_items_1018 import apply_theme  # noqa: E402

SITE = "ktl"
S = "https://chomoand-5.site/"
YT = "https://www.youtube.com/watch?v=FZCoDW52xXA"
YT_KTL = "https://www.youtube.com/watch?v=FZCoDW52xXA&t=1970s"
SRC = 'anan公式YouTube「<a href="%s" target="_blank" rel="noopener">【生配信アーカイブ】anan AWARD 2026 授賞式</a>」' % YT_KTL
AWARD = "https://ananweb.jp/award"
MEDIA_JSON = blogkit.ARTICLES / "ktl_anan_acc_1116_media.json"

SW_JP = "https://www.swarovski.com/ja-JP/"
SW_VIENNA = "https://www.swarovski.com/ja-JP/s-vienna-collection/"
SW_MATRIX = "https://www.swarovski.com/ja-JP/c-swa-root/%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA%E3%83%BC/f/collection/collection-matrix"
ZOZO_MESMERA = "https://store.shopping.yahoo.co.jp/zozo/107653140.html"
WL = "https://wanderlustseoul.com/"
WL_CL = "https://wanderlustseoul.com/product/detail.html?product_no=23"

# 既存記事(chomoand-5.site、2026-11-16確認)
P_ANAN = S + "?p=646"
P_EVENT = S + "?p=711"
P_MOSCOT = S + "?p=54"
P_PALM = S + "?p=551"
P_HERMES = S + "?p=398"
P_TOMFORD = S + "?p=368"
P_RL = S + "?p=42"


def ia(t, u):
    return '<a href="%s">%s</a>' % (u, t)


def a(t, u):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, t)


def _html(inner):
    return "<!-- wp:html -->\n%s\n<!-- /wp:html -->" % inner


def img(name, alt):
    ids = json.loads(MEDIA_JSON.read_text(encoding="utf-8")) if MEDIA_JSON.exists() else {}
    m = ids.get(name, {"id": 0, "url": "images/" + name})
    return ('<!-- wp:image {"id":%d,"sizeSlug":"full","linkDestination":"none"} -->\n'
            '<figure class="wp-block-image size-full"><img src="%s" alt="%s" class="wp-image-%d" '
            'style="max-width:100%%;height:auto;"/>'
            '<figcaption style="font-size:0.8em;color:#888;">出典:%s</figcaption></figure>\n'
            '<!-- /wp:image -->') % (m["id"], m["url"], alt, m["id"], SRC)


def aff_box(title, kw, note, border):
    """楽天は検索結果ページへのアフィリエイトリンク、Amazonは検索リンク。"""
    env = ab.load_keys()
    amz = al.build_amazon_search_url(kw, env.get("AMAZON_ASSOCIATE_TAG"))
    q = urllib.parse.quote("https://search.rakuten.co.jp/search/mall/" + urllib.parse.quote(kw) + "/", safe="")
    rk = "https://hb.afl.rakuten.co.jp/hgc/{}/?pc={}&m={}".format(env["RAKUTEN_AFFILIATE_ID"], q, q)
    return ab.build_box(rk, None, title, amz, note, border), rk, amz


def related(items):
    lis = "\n".join('<li style="margin:0 0 6px 0;">%s</li>' % ia(t, u) for t, u in items)
    return _html('<div style="border:1px solid #c9d6e6;border-left:4px solid #3d5a80;border-radius:4px;'
                 'margin:0 0 16px 0;padding:14px 18px;background:#eef3f8;">\n'
                 '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい</p>\n'
                 '<ul style="margin:0;padding-left:1.3em;">\n%s\n</ul>\n</div>' % lis)


def award_info():
    return info([("イベント", "anan AWARD 2026 授賞式"),
                 ("日にち", "2026年11月14日(土)"),
                 ("受賞", "ニューヒーロー部門"),
                 ("配信", "anan公式YouTubeで無料生配信(アーカイブあり)"),
                 ("登壇", "岩﨑大昇、井上瑞稀、中村嶺亜、猪狩蒼弥(佐々木大光は欠席)")])


def award_story(focus):
    """授賞式の様子(4本共通)。focus = その記事のメンバーについての1段落(文のリスト)。"""
    return [h2("anan AWARD 2026の授賞式はどんな様子だった？"),
            p("KEY TO LITは、2026年を象徴する人に贈られる『anan AWARD 2026』で、ニューヒーロー部門を受賞しました。",
              "授賞式では、金のananパンダトロフィーを4人がそれぞれ受け取りました。",
              "佐々木大光は、けがの療養のため欠席でした。"),
            p("岩﨑大昇は「12月9日のデビューに向けて頑張ろうという時に、すてきな賞をいただけて力になる」と喜びを話しました。",
              "5人で叶えたい夢を聞かれると「史上最高傑作と呼ばれる存在になる」と答えています。"),
            p("中村嶺亜は、ジュニアとして『anan』のソロ表紙を飾った思い出と、5人での初表紙が緊急重版になったうれしさを語りました。",
              "井上瑞稀は、デビュー発表のあと5人でファミレスに行ったエピソードを披露し、最後は「次は5人で登壇したい」としめくくりました。"),
            p(*focus),
            p("授賞式の流れや受賞の背景は、" + ia("anan AWARD 2026の登壇記事", P_ANAN) + "でもまとめています。")]


# =====================================================================================
ARTS = {}

# ------------------------------------------------------------------ 岩﨑大昇 Vienna set
ARTS["iwasaki"] = dict(
    member="岩﨑大昇", cats=[4, 6], slug="iwasaki-taisho-swarovski-vienna-set-anan-award",
    title="岩﨑大昇のanan AWARDのネックレスはどこの？スワロフスキー！",
    eye=("岩﨑大昇", ["anan AWARDのネックレスは", "スワロフスキー！"]),
    imgs=[("ktl_anan1114_iwasaki.jpg", "anan AWARD 2026の授賞式で大きなクリスタルのネックレスを着けた岩﨑大昇"),
          ("ktl_anan1114_iwasaki2.jpg", "anan AWARD 2026の授賞式で話す岩﨑大昇")],
)


def body_iwasaki(F):
    border = "#d5d8dc"
    box, rk, amz = aff_box("スワロフスキー Vienna(ウィーン)", "スワロフスキー Vienna",
                           "楽天・Amazonは検索結果ページです。セット品が無いときはネックレス・ピアスを単品で探してください", border)
    o = [ab.NOTICE,
         p("2026年11月14日(土)の『anan AWARD 2026』授賞式で、KEY TO LITの岩﨑大昇が着けていた大きなクリスタルのネックレスが話題です。",
           "このネックレスとピアスは、" + mark("SWAROVSKI(スワロフスキー)の「Vienna(ウィーン)セット」") + "とみられます。"),
         p("この記事では、ネックレスが映った場面、商品の特徴と値段、Viennaコレクションの由来、授賞式の様子までまとめました。"),
         learn(["ネックレスが映った場面", "ネックレスのブランドと商品名", "値段と買える場所",
                "Viennaコレクションとは", "岩﨑大昇の授賞式のコーデ", "授賞式の様子"]),

         h2("岩﨑大昇のネックレスが映った場面は？"),
         award_info(),
         img(*F["imgs"][0]),
         p("岩﨑大昇は、黒のベロアのジャケットを胸元を大きく開けて着て、首にはクリスタルがびっしり並んだ太いチェーンのネックレスを着けていました。",
           "照明が当たるたびに首元がキラキラと光り、ステージの上でもひときわ目立っていました。"),
         p("耳には、ネックレスと同じように、ねじれたクリスタルのモチーフのピアスが光っています。",
           "ネックレスとピアスが同じデザインでそろっているのが、セットとみられる理由です。"),

         h2("ネックレスはスワロフスキーのViennaセット"),
         info([("ブランド", "SWAROVSKI(スワロフスキー)"),
               ("商品名", "Vienna セット(ネックレスとピアス)"),
               ("カット・色", "ミックスカット、ホワイト"),
               ("金具", "ロジウム・プレーティング(シルバー色)"),
               ("値段", "198,000円(スワロフスキー公式サイトの日本向けの表示)")]),
         p("太いチェーンの輪のひとつひとつに、小さなクリスタルがすき間なく並べられたデザインです。",
           "輪はねじれた形になっていて、クリスタルの列が羽のように重なって見えます。"),
         p("ピアスも同じねじれたモチーフで、ネックレスと合わせると首元から耳元まで一体感が出ます。",
           "1つ1つの粒が小さいので、大ぶりでもギラギラしすぎず、上品に光るのが特徴です。"),
         h3("見分け方のポイント"),
         checks(["クリスタルが一面に並んだ太いチェーン", "輪がねじれていて、羽のような列に見える",
                 "シルバー色の金具(ロジウム・プレーティング)", "同じモチーフのピアスがセット"]),

         h2("値段と買える場所は？"),
         p("スワロフスキー公式サイトの日本向けページでは、Viennaセットは198,000円で紹介されています。",
           "Viennaコレクションは高価格帯のラインで、公式のオンラインでは在庫が無く、店頭のみの扱いになることもあります。"),
         p("気になる人は、まず公式サイトで在庫を見て、無いときは近くのスワロフスキーのお店に問い合わせるのが確実です。"),
         _html(box),
         buy([("スワロフスキー公式サイト(Viennaコレクション)", SW_VIENNA),
              ("楽天市場で探す", rk), ("Amazonで探す", amz)]),
         p("値段や在庫は変わることがあるので、買う前に最新の情報を確認してください(2026年11月16日に確認)。"),

         h2("Viennaコレクションとは？"),
         p("Viennaは、スワロフスキーの創業130周年を記念して作られたコレクションです。",
           "スワロフスキーのシンボルである白鳥(スワン)からヒントを得ていて、羽のような重なりがデザインの特徴になっています。"),
         p("デザインしたのは、スワロフスキーのグローバル・クリエイティブ・ディレクターのジョヴァンナ・エンゲルバートです。",
           "2025年のメットガラで初めてお披露目され、チョーカーやイヤーカフなど、迫力のある作品がそろっています。"),
         p("ブランドの本社があるオーストリアの都市ウィーンの名前がつけられていて、スワロフスキーの歴史をたたえるコレクションになっています。"),

         h2("岩﨑大昇の授賞式のコーデ"),
         img(*F["imgs"][1]),
         p("岩﨑大昇は、黒のベロアのジャケットとパンツのセットアップに、黒の革靴を合わせていました。",
           "インナーを着ずにジャケットの胸元を開けることで、ネックレスが主役になるように見せていました。"),
         p("黒のつやのある生地に、白く光るクリスタルを合わせると、ぐっと大人っぽい印象になります。",
           "ふだんの私服でも、黒のニットやシャツに太めのシルバーのネックレスを1本足すだけで、近い雰囲気を作れます。"),
         p("岩﨑大昇は、以前の動画でも" + ia("トム フォードの白のVネックT", P_TOMFORD) + "を着ていて、胸元をすっきり見せるスタイルが似合うメンバーです。"),
         ]
    o += award_story(["岩﨑大昇は、トロフィーを手に司会の質問に答える場面が多く、そのたびに首元のクリスタルが輝いていました。"])
    o += [h2("まとめ"),
          checks(["2026年11月14日のanan AWARD 2026の授賞式で岩﨑大昇が着けていたネックレス",
                  "スワロフスキーの「Vienna セット」とみられる",
                  "公式サイトの日本向けの表示は198,000円",
                  "Viennaはスワロフスキー130周年を記念したコレクション"]),
          p("デビュー直前の大切な授賞式に、ブランドの節目を記念したジュエリーを選んでいたのがすてきです。",
            "アーカイブを見返すときは、話すたびに光る首元にも注目してみてください！"),
          "[[RELATED]]"]
    return o


# ------------------------------------------------------------------ 中村嶺亜 Wanderlust glasses
ARTS["reia_glasses"] = dict(
    member="中村嶺亜", cats=[4, 8], slug="nakamura-reia-wanderlust-birdstar-glasses-anan-award",
    title="中村嶺亜のanan AWARDのメガネはどこの？Wanderlust！",
    eye=("中村嶺亜", ["anan AWARDのメガネは", "Wanderlust！"]),
    imgs=[("ktl_anan1114_reia.jpg", "anan AWARD 2026の授賞式でふちなしのメガネをかけた中村嶺亜"),
          ("ktl_anan1114_reia2.jpg", "anan AWARD 2026の授賞式で話す中村嶺亜")],
)


def body_reia_glasses(F):
    o = [p("2026年11月14日(土)の『anan AWARD 2026』授賞式で、KEY TO LITの中村嶺亜がかけていたふちなしのメガネが話題です。",
           "このメガネは、" + mark("韓国のアイウェアブランドWanderlust(ワンダーラスト)の「BIRDSTAR 01」") + "とみられます。"),
         p("この記事では、メガネが映った場面、商品の特徴とサイズ、値段と買い方、ブランドのことまでまとめました。"),
         learn(["メガネが映った場面", "メガネのブランドと商品名", "サイズと特徴", "値段と日本からの買い方",
                "Wanderlustとはどんなブランド？", "授賞式の様子"]),

         h2("中村嶺亜のメガネが映った場面は？"),
         award_info(),
         img(*F["imgs"][0]),
         p("中村嶺亜は、黒のシャツに黒のネクタイを合わせたオールブラックのスタイルに、ふちの無いシルバーのメガネをかけていました。",
           "レンズのまわりにフレームが無いので、顔の印象をじゃませず、目元がすっきりと見えます。"),
         p("よく見ると、耳にかけるつるの付け根に、小さな星のような飾りが付いています。",
           "照明が当たると、このシルバーの飾りがキラッと光っていました。"),

         h2("メガネはWanderlustのBIRDSTAR 01"),
         info([("ブランド", "Wanderlust(ワンダーラスト、韓国・ソウル)"),
               ("商品名", "BIRDSTAR 01 CL"),
               ("形", "スクエアのふちなし(無地のレンズ)"),
               ("素材", "ステンレス(フレーム・つる)"),
               ("値段", "109,000ウォン(公式サイト)")]),
         p("BIRDSTAR 01は、ブランドの代名詞の「バードスター」の飾りを付けた、ステンレスのふちなしメガネです。",
           "公式の説明では、レンズはブルーライトをカットするタイプになっています。"),
         p("末尾の「CL」は色の名前で、同じ形で「BLK」「YE」というバリエーションもあります。",
           "中村嶺亜がかけていたのは、レンズが透明でシルバーのつるの「CL」とみられます。"),
         h3("サイズと重さ"),
         table(("項目", "サイズ"), [("レンズの横幅", "54mm"), ("レンズの縦幅", "37mm"), ("ブリッジ", "16mm"),
                                     ("全体の横幅", "135mm"), ("つるの長さ", "145mm"), ("重さ", "24g")]),
         p("全体の横幅が135mmと少し大きめなので、顔まわりをしっかり囲むサイズ感です。",
           "24gと軽いので、長い時間かけていても疲れにくいメガネです。"),
         h3("見分け方のポイント"),
         checks(["レンズのまわりにフレームが無いふちなし", "少し横長のスクエアのレンズ",
                 "つるの付け根の星と鳥の飾り", "つるに透かしの入ったシルバーのステンレス"]),

         h2("値段と日本からの買い方は？"),
         p("Wanderlustの公式オンラインストアでは、BIRDSTAR 01は109,000ウォンで売られています。",
           "日本円にすると、1万円台前半くらいです(為替によって変わります)。"),
         p("公式ストアは韓国向けのサイトで、ページによっては売り切れの表示が出ていることもあります。",
           "日本から買うときは、韓国の通販サイトの海外配送や、買い物代行サービスを使う方法があります。"),
         p("日本の楽天市場やAmazonでは、2026年11月16日の時点で同じ商品は見つかりませんでした。",
           "度付きにしたいときは、メガネ店でレンズの交換ができるか相談してみてください。"),
         buy([("Wanderlust公式サイト(韓国)", WL), ("BIRDSTAR 01 CL 商品ページ", WL_CL)]),
         p("値段や在庫は変わることがあるので、買う前に最新の情報を確認してください。"),

         h2("Wanderlustとはどんなブランド？"),
         p("Wanderlustは、韓国・ソウルのアイウェアブランドです。",
           "ブランド名は英語で「旅への強いあこがれ」という意味で、メガネやサングラスを中心に作っています。"),
         p("ブランドを象徴するのが、鳥と星を組み合わせた「バードスター」のモチーフです。",
           "シンプルなメガネにこの飾りをワンポイントで入れていて、さりげなく個性を出せるのが人気のポイントです。"),
         p("KEY TO LITでは、井上瑞稀も以前" + ia("モスコットのメガネ", P_MOSCOT) + "をかけていて、メンバーそれぞれのメガネ選びにも注目が集まっています。"),

         h2("中村嶺亜の授賞式のコーデ"),
         img(*F["imgs"][1]),
         p("中村嶺亜は、黒のジャケットに黒のシャツとネクタイを合わせ、腰には太いベルトを何本も重ねて巻いていました。",
           "全身を黒でそろえつつ、ベルトの重ね付けでシルエットにメリハリを出したコーデです。"),
         p("耳には、スワロフスキーのイヤーカフも着けていました。",
           "ふちなしのメガネとシルバーのアクセサリーで、黒のコーデに軽さと華やかさを足しています。"),
         p("黒のコーデにふちなしのメガネを合わせると、顔まわりが重くならず、知的な印象になります。",
           "ふだんの私服でも、まねしやすい組み合わせです。"),
         ]
    o += award_story(["中村嶺亜は、5人での初表紙について話すとき、ふちなしのメガネ越しにやさしい表情を見せていました。"])
    o += [h2("まとめ"),
          checks(["2026年11月14日のanan AWARD 2026の授賞式で中村嶺亜がかけていたメガネ",
                  "韓国のWanderlust「BIRDSTAR 01 CL」とみられる",
                  "公式サイトでは109,000ウォン、日本円で1万円台前半",
                  "つるの付け根の「バードスター」の飾りが目印"]),
          p("オールブラックのコーデに、ふちなしのメガネを合わせるセンスがさすがです。",
            "アーカイブを見返すときは、つるの付け根の小さな星にも注目してみてください！"),
          "[[RELATED]]"]
    return o


# ------------------------------------------------------------------ 中村嶺亜 Mesmera ear cuff
ARTS["reia_cuff"] = dict(
    member="中村嶺亜", cats=[4, 8], slug="nakamura-reia-swarovski-mesmera-ear-cuff-anan-award",
    title="中村嶺亜のanan AWARDのイヤーカフはどこの？スワロフスキー！",
    eye=("中村嶺亜", ["anan AWARDのイヤーカフは", "スワロフスキー！"]),
    imgs=[("ktl_anan1114_reia3.jpg", "anan AWARD 2026の授賞式でクリスタルのイヤーカフを着けた中村嶺亜"),
          ("ktl_anan1114_reia2.jpg", "anan AWARD 2026の授賞式で話す中村嶺亜")],
)


def body_reia_cuff(F):
    border = "#f3c6d9"
    box, rk, amz = aff_box("スワロフスキー Mesmera イヤーカフ(マーキスカット・ホワイト)",
                           "スワロフスキー Mesmera イヤーカフ 5747998",
                           "楽天・Amazonは検索結果ページです。品番5747998が目印です", border)
    o = [ab.NOTICE,
         p("2026年11月14日(土)の『anan AWARD 2026』授賞式で、KEY TO LITの中村嶺亜が耳に着けていたクリスタルのイヤーカフが話題です。",
           "このイヤーカフは、" + mark("SWAROVSKI(スワロフスキー)の「Mesmera イヤーカフ マーキスカット」") + "とみられます。"),
         p("この記事では、イヤーカフが映った場面、商品の特徴と値段、Mesmeraコレクションのこと、授賞式の様子までまとめました。"),
         learn(["イヤーカフが映った場面", "イヤーカフのブランドと商品名", "値段と買える場所",
                "Mesmeraとはどんなコレクション？", "イヤーカフの着け方", "授賞式の様子"]),

         h2("中村嶺亜のイヤーカフが映った場面は？"),
         award_info(),
         img(*F["imgs"][0]),
         p("中村嶺亜は、耳の上のほうに、クリスタルがいくつも重なったイヤーカフを着けていました。",
           "ふちなしのメガネのつるのすぐ後ろで、照明が当たるたびに白く光っていました。"),
         p("細長いクリスタルがいくつも重なって、耳の上のほうで小さな花のように光っていました。"),

         h2("イヤーカフはスワロフスキーのMesmera"),
         info([("ブランド", "SWAROVSKI(スワロフスキー)"),
               ("商品名", "Mesmera イヤーカフ"),
               ("カット・色", "マーキスカット、ホワイト"),
               ("金具", "ロジウム・プレーティング(シルバー色)"),
               ("品番", "5747998"),
               ("値段", "26,400円(ZOZOTOWNのスワロフスキー公式ショップ)")]),
         p("マーキスカットは、両はしがとがった、葉っぱやボートのような形のカットです。",
           "このイヤーカフは、大きさの違うマーキスカットのクリスタルを重ねて、葉が茂ったような形にしています。"),
         p("イヤーカフなので、ピアスの穴が無くても、耳のふちにはさむだけで着けられます。",
           "商品写真では、左右2つが並んだ形で紹介されています。"),
         h3("見分け方のポイント"),
         checks(["両はしがとがったマーキスカットのクリスタル", "クリスタルが葉っぱのように重なった形",
                 "耳のふちを包むように着けるカフ", "シルバー色の金具"]),

         h2("値段と買える場所は？"),
         p("ZOZOTOWNのスワロフスキー公式ショップでは、26,400円で売られています(2026年11月16日に確認)。",
           "スワロフスキーの直営店や公式オンラインストアでも探せます。"),
         p("Yahoo!ショッピングなどの並行輸入のお店では、2万円前後で出ていることもあります。",
           "ただし、正規品の保証や返品の条件はお店によって違うので、よく確認してから選んでください。"),
         _html(box),
         buy([("スワロフスキー公式サイト", SW_JP),
              ("ZOZOTOWN スワロフスキー公式ショップ(Mesmera イヤーカフ)", ZOZO_MESMERA),
              ("楽天市場で探す", rk), ("Amazonで探す", amz)]),
         p("値段や在庫は変わることがあるので、買う前に最新の情報を確認してください。"),

         h2("Mesmeraとはどんなコレクション？"),
         p("Mesmera(メスメラ)は、大きくて形の違うクリスタルを大胆に組み合わせた、スワロフスキーの人気コレクションです。",
           "ネックレスやピアス、ブレスレットまでそろっていて、ひとつ着けるだけで華やかになるデザインが多くそろっています。"),
         p("同じMesmeraには、マーキスカット以外にも、いろいろなカットを組み合わせたミックスカットのアイテムもあります。",
           "シルバー色の金具のものが多く、どんな服にも合わせやすいのも人気の理由です。"),
         p("今回の授賞式では、岩﨑大昇と井上瑞稀もスワロフスキーのアクセサリーを着けていました。",
           "メンバー3人がそろってスワロフスキーを選んでいたのも、この日のコーデの見どころです。"),

         h2("イヤーカフの着け方"),
         img(*F["imgs"][1]),
         p("イヤーカフは、耳の上のほうか、真ん中あたりのふちにはさんで、少しずつずらしながら位置を決めます。",
           "強く押しつぶすと金具がゆがむので、やさしくはさむのがコツです。"),
         p("中村嶺亜のようにメガネをかけるときは、つるとぶつからない少し下の位置に着けると、すっきり見えます。",
           "黒のジャケットやシャツと合わせると、クリスタルの白さがいっそう引き立ちます。"),
         p("中村嶺亜は、以前の配信でも" + ia("パーム エンジェルスのスカジャン", P_PALM) + "を着ていて、光るものやつやのあるアイテムを上手に取り入れるメンバーです。"),
         ]
    o += award_story(["中村嶺亜は、ふちなしのメガネにクリスタルのイヤーカフを合わせて、オールブラックのコーデを華やかに仕上げていました。"])
    o += [h2("まとめ"),
          checks(["2026年11月14日のanan AWARD 2026の授賞式で中村嶺亜が着けていたイヤーカフ",
                  "スワロフスキーの「Mesmera イヤーカフ マーキスカット」(品番5747998)とみられる",
                  "ZOZOTOWNの公式ショップでは26,400円",
                  "ピアスの穴が無くても着けられる"]),
          p("メガネとイヤーカフを同じシルバー色でそろえる、細かいところまでこだわったコーデでした。",
            "アーカイブを見返すときは、メガネのつるの後ろで光る耳元にも注目してみてください！"),
          "[[RELATED]]"]
    return o


# ------------------------------------------------------------------ 井上瑞稀 Matrix hoop
ARTS["mizuki"] = dict(
    member="井上瑞稀", cats=[4, 7], slug="inoue-mizuki-swarovski-matrix-hoop-earrings-anan-award",
    title="井上瑞稀のanan AWARDのピアスはどこの？スワロフスキー！",
    eye=("井上瑞稀", ["anan AWARDのピアスは", "スワロフスキー！"]),
    imgs=[("ktl_anan1114_mizuki.jpg", "anan AWARD 2026の授賞式でクリスタルのフープピアスを着けた井上瑞稀"),
          ("ktl_anan1114_mizuki2.jpg", "anan AWARD 2026の授賞式で話す井上瑞稀")],
)


def body_mizuki(F):
    border = "#f2c4c9"
    box, rk, amz = aff_box("スワロフスキー Matrix フープピアス(ホワイト・ロジウム)",
                           "スワロフスキー Matrix フープピアス 5753572",
                           "楽天・Amazonは検索結果ページです。品番5753572が目印です", border)
    o = [ab.NOTICE,
         p("2026年11月14日(土)の『anan AWARD 2026』授賞式で、KEY TO LITの井上瑞稀が着けていたクリスタルのピアスが話題です。",
           "このピアスは、" + mark("SWAROVSKI(スワロフスキー)の「Matrix フープピアス」") + "とみられます。"),
         p("この記事では、ピアスが映った場面、商品の特徴と値段、Matrixコレクションのこと、授賞式の様子までまとめました。"),
         learn(["ピアスが映った場面", "ピアスのブランドと商品名", "値段と買える場所",
                "Matrixとはどんなコレクション？", "井上瑞稀の授賞式のコーデ", "授賞式の様子"]),

         h2("井上瑞稀のピアスが映った場面は？"),
         award_info(),
         img(*F["imgs"][0]),
         p("井上瑞稀は、金のボタンが並んだ軍服のような黒のジャケットを着て、耳には小さなクリスタルのピアスを着けていました。",
           "髪の間から耳元がのぞくたびに、クリスタルがキラッと光っていました。"),
         p("小ぶりですが、照明が当たるとしっかり光り、黒のジャケットによく映えていました。"),

         h2("ピアスはスワロフスキーのMatrixフープピアス"),
         info([("ブランド", "SWAROVSKI(スワロフスキー)"),
               ("商品名", "Matrix フープピアス"),
               ("カット・色", "ラウンドカット、ホワイト(クリア)"),
               ("金具", "ロジウム・プレーティング(シルバー色)"),
               ("品番", "5753572"),
               ("大きさ", "直径15mmくらい(海外の正規店の表記)")]),
         p("左右でデザインが少し違う、アシンメトリーのフープピアスです。",
           "片方はフープの外側に、大きな丸いクリスタルと、小さなクリスタルの列が付いています。"),
         p("もう片方は、クリスタルの列とフープが2本並んだような形で、耳に着けると重ね付けしたように見えます。",
           "1組で2つのデザインが楽しめるのが、このピアスの面白いところです。"),
         h3("見分け方のポイント"),
         checks(["小ぶりなシルバーのフープ", "丸いクリスタル(ラウンドカット)が縦に並ぶ",
                 "片方に大きなクリスタルが1つ付く", "左右でデザインが違うアシンメトリー"]),

         h2("値段と買える場所は？"),
         p("Yahoo!ショッピングの並行輸入のお店では、19,800円で売られていました(2026年11月16日に確認)。",
           "日本の公式サイトでの値段は、確認できませんでした。"),
         p("新しいデザインで、取り扱いのあるお店はまだ多くありません。",
           "スワロフスキーの直営店や公式サイトで、品番5753572を伝えて探してもらうのが確実です。"),
         _html(box),
         buy([("スワロフスキー公式サイト(Matrixコレクション)", SW_MATRIX),
              ("楽天市場で探す", rk), ("Amazonで探す", amz)]),
         p("並行輸入品は、正規品の保証や返品の条件がお店によって違うので、よく確認してから選んでください。"),

         h2("Matrixとはどんなコレクション？"),
         p("Matrix(マトリックス)は、丸いラウンドカットなど、シンプルなカットのクリスタルを並べたスワロフスキーの定番コレクションです。",
           "ピアスやネックレス、ブレスレットなどがそろっていて、毎日使いやすいデザインが多いのが特徴です。"),
         p("Matrixのフープピアスは、1万円前後の小さなものから、大きなクリスタルを使った華やかなものまで、たくさんの種類があります。",
           "シンプルなぶん、男性でも取り入れやすいアクセサリーです。"),
         p("今回の授賞式では、岩﨑大昇と中村嶺亜もスワロフスキーのアクセサリーを着けていました。",
           "井上瑞稀は、3人の中でいちばん小ぶりなアイテムを選んでいました。"),

         h2("井上瑞稀の授賞式のコーデ"),
         img(*F["imgs"][1]),
         p("井上瑞稀は、金のボタンが並んだ軍服のようなジャケットに、黒のパンツと黒の革靴を合わせていました。",
           "手には黒のレースの手袋をしていて、クラシックで少しミステリアスな雰囲気のコーデです。"),
         p("ジャケットが主役のコーデなので、耳元は小ぶりなフープピアスでさりげなく光らせていました。",
           "シルバーのピアスは、金ボタンとも相性が良く、黒のコーデのアクセントになっていました。"),
         p("井上瑞稀は、以前の自撮りでも" + ia("エルメスのシェーヌダンクルのブレスレット", P_HERMES) + "を着けていて、シルバーのアクセサリーをよく取り入れています。"),
         ]
    o += award_story(["井上瑞稀は、ファミレスのエピソードを楽しそうに話し、最後は配信を見ている佐々木大光とファンに向けて言葉を送りました。"])
    o += [h2("まとめ"),
          checks(["2026年11月14日のanan AWARD 2026の授賞式で井上瑞稀が着けていたピアス",
                  "スワロフスキーの「Matrix フープピアス」(品番5753572)とみられる",
                  "並行輸入のお店では19,800円(2026年11月16日)",
                  "左右でデザインが違うアシンメトリーのフープ"]),
          p("軍服のようなジャケットに、小さく光るピアスを合わせるバランスがすてきでした。",
            "アーカイブを見返すときは、髪の間からのぞく耳元にも注目してみてください！"),
          "[[RELATED]]"]
    return o


BODIES = {"iwasaki": body_iwasaki, "reia_glasses": body_reia_glasses, "reia_cuff": body_reia_cuff,
          "mizuki": body_mizuki}


def key_of(k):
    return "ktl_anan_acc_1116_" + k


def related_for(k):
    items = []
    for o, A in ARTS.items():
        if o == k:
            continue
        st = blogkit.ARTICLES / (key_of(o) + "_posted.json")
        if st.exists():
            items.append((A["title"], S + "?p=%d" % json.loads(st.read_text(encoding="utf-8"))["post"]))
    items += [("【anan AWARD 2026】キテレツ初登壇！配信は何時から？", P_ANAN),
              ("キテレツ発売記念イベントはいつ？ハイタッチ会の応募方法も！", P_EVENT)]
    return related(items)


def build(k):
    A = ARTS[k]
    out = "\n\n".join(BODIES[k](A)).replace("[[RELATED]]", related_for(k)) + "\n"
    out = apply_theme(out, A["member"])
    return blogkit.finalize(out, SITE, ())


def eyecatch(k):
    import subprocess
    A = ARTS[k]
    out = blogkit.ROOT / "images" / (key_of(k) + "_eyecatch.jpg")
    if not out.exists():
        main, bottoms = A["eye"]
        cmd = [sys.executable, str(blogkit.ROOT / "tools" / "eyecatch_kitetsu.py"), "--top", "anan AWARD 2026",
               "--main", main, "--color-key", A["member"], "--out", str(out)]
        for b in bottoms:
            cmd += ["--bottom", b]
        subprocess.run(cmd, check=True)
    return out


def upload_images(k):
    ids = json.loads(MEDIA_JSON.read_text(encoding="utf-8")) if MEDIA_JSON.exists() else {}
    wp = blogkit.WP(SITE)
    for fn, alt in ARTS[k]["imgs"]:
        if fn in ids:
            continue
        mid = wp.upload_media(str(blogkit.ROOT / "images" / fn), alt)
        m = wp.get("/media/%d" % mid)
        ids[fn] = {"id": mid, "url": m["source_url"]}
        MEDIA_JSON.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    which = list(ARTS) if sys.argv[1] == "all" else [sys.argv[1]]
    for k in which:
        A = ARTS[k]
        if "--build-only" in sys.argv:
            blogkit.ARTICLES.mkdir(exist_ok=True)
            (blogkit.ARTICLES / (key_of(k) + ".html")).write_text(build(k), encoding="utf-8")
            print("作った:", key_of(k))
            continue
        upload_images(k)
        eye = eyecatch(k)
        blogkit.upload_draft(SITE, key_of(k), A["title"], build(k), A["slug"], A["cats"], eye,
                             A["eye"][0] + " " + A["eye"][1][0], update="--update" in sys.argv)
