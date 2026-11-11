# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) ラウールがAlan Walker公式X動画(2026-11-09「YUME - November 20!」)で
着けていた黒いハートのネックレス(Crystal Haze)の記事HTMLを組み立てる。

usage: python tools/_build_snowman_raul_crystalhaze_1111.py
articles/snowman_raul_crystalhaze.html と articles/snowman_raul_crystalhaze_manifest.json を書き出す。
投稿は tools/_upload_snowman_raul_crystalhaze_1111.py。
第三者(特定アカウント)の画像・言及は使わず、Alan Walker本人のXポスト埋め込み+公式動画のフレームで構成する。
"""
import os, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chomoand-2.com"
ACC = "#8a9096"      # ラウールのメンバーカラー(白)はグレーで代用
BG = "#f4f5f6"
LINE = "#d6d9dc"
MK = "#e3e6e9"
CH = "https://www.crystalhazejewelry.com/en-us"
CH_SERENA = "https://www.crystalhazejewelry.com/en-us/collections/the-serena-collection"
CH_JELLY = "https://www.crystalhazejewelry.com/en-us/collections/jelly-heart-collection"
HBX = "https://hbx.com/jp/women/brands/crystal-haze"
AVEX = "https://avexnet.jp/news/1038137"
MENT = "https://mentrecording.jp/snowman/news/detail.php?id=1137178"


def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n"


def mk(text):
    return f'<strong><span style="font-size:1.1em;background:linear-gradient(transparent 60%,{MK} 60%);">{text}</span></strong>'


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n'


def html(s):
    return "<!-- wp:html -->\n" + s + "\n<!-- /wp:html -->\n"


def a(url, label):
    return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'


def listbox(title, items, big=False):
    fs = "font-size:1.05em;" if big else ""
    pad = "10px 18px" if big else "8px 16px"
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return html(f'<div style="border:1px solid {ACC if big else LINE};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                f'<p style="font-weight:bold;{fs}margin:0;padding:{pad};background:{ACC};color:#fff;">{title}</p>\n'
                f'<ul style="margin:0;padding:12px 18px 12px 34px;background:{BG};">\n{lis}\n</ul>\n</div>')


def keybox(rows):
    out = []
    for i, (k, v) in enumerate(rows):
        m = "0" if i == 0 else "4px 0 0 0"
        out.append(f'<p style="margin:{m};"><strong>{k}:</strong>{v}</p>')
    return html(f'<div style="border:1px solid {LINE};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">\n'
                + "\n".join(out) + "\n</div>")


def table(rows):
    trs = []
    for i, r in enumerate(rows):
        st = f' style="background:{BG};font-weight:bold;"' if i == 0 else ""
        trs.append("<tr>" + "".join(f"<td{st}>{c}</td>" for c in r) + "</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            + "".join(trs) + "</tbody></table></figure>\n<!-- /wp:table -->\n")


def xembed(user, sid):
    return html(f'<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><a href="https://twitter.com/{user}/status/{sid}">https://twitter.com/{user}/status/{sid}</a></blockquote>\n'
                '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def figure(name, alt, cap):
    return html(f'<figure style="margin:0 0 16px 0;text-align:center;"><img src="{{{{IMG:{name}}}}}" alt="{alt}" style="max-width:100%;height:auto;" loading="lazy">'
                f'<figcaption style="font-size:12px;color:#888;">{cap}</figcaption></figure>')


def related(items):
    lis = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in items)
    return html(f'<div style="border:1px solid {LINE};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;">\n'
                f'<p style="margin:0 0 6px 0;font-weight:bold;color:{ACC};">あわせて読みたい</p>\n<ul style="margin:0;padding-left:20px;">{lis}</ul>\n</div>')


body = "".join([
    p("2026年11月9日、アラン・ウォーカーさんが公式Xに「YUME - November 20!」と動画を投稿しました。",
      "Snow Manのラウールさんとのコラボ曲「YUME」の発表動画です。",
      "動画のラウールさんが首に着けていた黒いハートのネックレスは、" + mk("ノルウェーのブランド「クリスタルヘイズ(Crystal Haze)」") + "のものとみられます。"),
    xembed("IAmAlanWalker", "2119733746714996876"),
    listbox("この記事でわかること", ["ラウールの黒いハートのネックレスのブランドと商品名",
                              "動画のネックレスと同じだと言える理由",
                              "値段は？日本円でいくら？",
                              "どこで買える？",
                              "コラボ曲「YUME」とアラン・ウォーカー"], big=True),

    h2("ラウールのネックレスはクリスタルヘイズ"),
    keybox([("ブランド", "クリスタルヘイズ(Crystal Haze)"),
            ("チェーン", "セリーナ ネックレス(Serena Necklace)の黒"),
            ("ハート", "ジェリーハート ペンダント(Jelly Heart Pendant)の黒"),
            ("値段の目安", "2つで約5万〜6万円(1ドル153円で計算)")]),
    p("ラウールさんが着けていたのは、黒い石がすき間なく並んだ細いチェーンに、黒いハートを1つ下げたネックレスです。",
      "クリスタルヘイズでは、チェーンとハートは別々に売られています。",
      "そのため、" + mk("チェーンとペンダントを自分で組み合わせて着けていた") + "とみられます。"),
    figure("neck", "ラウールの黒いハートのネックレス", "出典:Alan Walker公式X(2026年11月9日の動画)より"),
    table([["パーツ", "商品名", "公式の値段"],
           ["チェーン", "セリーナ ネックレス(黒・シルバー)", "295ドル(約4万5,000円)"],
           ["ハート", "ジェリーハート ペンダント(黒)", "35〜60ドル(約5,400〜9,200円)"]]),
    p("値段は公式オンラインストア(アメリカ向け)のドル表示です。",
      "円の金額は1ドル153円で計算した目安なので、実際の支払いは為替や送料で変わります。"),

    h2("動画のネックレスと同じだと言える理由"),
    p("アラン・ウォーカーさんの動画で、ラウールさんはアイボリーのざっくりしたニットに、白いシャツを合わせていました。",
      "その首元をアップにすると、次の点がクリスタルヘイズの商品と一致します。"),
    listbox("動画とクリスタルヘイズの一致点", [
        "チェーンが、黒い小さな石をすき間なく並べたテニスチェーン",
        "石の土台はシルバーで、黒い石がつぶつぶに見える",
        "ハートはぷっくりと丸みのある形で、表面がキラキラした黒",
        "ハートの上に、チェーンに通すための小さな金具(コネクター)が付いている",
    ]),
    p("セリーナ ネックレスは、クリスタルヘイズの一番人気のシリーズです。",
      "黒い石だけで作られたシルバーのモデルもあり、動画の細い黒いチェーンとよく似ています。",
      "ジェリーハートも同じブランドの人気ペンダントで、黒いモデルがあります。"),
    p("ただし、本人やアラン・ウォーカーさんがブランド名を出したわけではありません。",
      "ここでは、形と色がそろっていることから「クリスタルヘイズとみられる」としています。"),

    h2("クリスタルヘイズとは？ノルウェー生まれのブランド"),
    p("クリスタルヘイズ(Crystal Haze)は、" + mk("2017年にノルウェーのオスロで生まれたジュエリーブランド") + "です。",
      "女性デザイナー2人が立ち上げたブランドです。"),
    p("子どものころに街のお店で見かけた、キャンディのようなアクセサリーがテーマです。",
      "カラフルな石やグミのようなクマ、ハートのモチーフが人気で、海外のセレクトショップでも売られています。"),
    p("実は、アラン・ウォーカーさんもノルウェー出身。",
      "そして「YUME」は、ラウールさんが日本からオスロまで行って、一緒に作った曲です。",
      "曲が生まれた街のブランドを着けていたのは、うれしい偶然かもしれません。"),
    h3("セリーナ ネックレスの特徴"),
    p("セリーナは、小さな石を一列に並べたテニスネックレスのシリーズです。",
      "色は、クリア・ピンク・グリーン・虹色など10色以上あります。",
      "ラウールさんが着けていたのは、黒い石とシルバーの組み合わせとみられます。"),
    p("素材は真鍮(しんちゅう)にメッキをかけたもので、石はキュービックジルコニアです。",
      "長さを調節できるアジャスターが付いているので、男性でも着けやすいつくりです。"),
    h3("ジェリーハート ペンダントの特徴"),
    p("ジェリーハートは、その名のとおりゼリーのようにぷっくりしたハートのペンダントです。",
      "チェーンに通す金具には、シンプルな「クラシック」と、石が付いた「パヴェ」の2種類があります。",
      "クラシックは35ドル前後、パヴェは55〜60ドル前後です。"),

    h2("どこで買える？"),
    listbox("購入先", [
        f"クリスタルヘイズ公式オンラインストア:{a(CH, '公式サイト')}(海外から発送)。{a(CH_SERENA, 'セリーナ')}・{a(CH_JELLY, 'ジェリーハート')}の一覧あり",
        f"HBX:{a(HBX, 'クリスタルヘイズの商品一覧')}(日本語ページあり)",
        "FARFETCHなどの海外通販サイト",
    ]),
    p("日本にはクリスタルヘイズの直営店がないため、買うなら通販が中心です。",
      "人気の色は売り切れになることも多く、黒のチェーンも公式ストアで品切れの表示が出ていた時期があります。",
      "海外通販では、関税や送料がかかることも覚えておきましょう。"),

    h2("ラウールとアラン・ウォーカーのコラボ曲「YUME」"),
    keybox([("曲名", "YUME(Alan Walker feat. Raul)"),
            ("配信日", "2026年11月20日(金)"),
            ("ポイント", "アラン・ウォーカーさん初の日本人アーティストとのコラボ")]),
    p("アラン・ウォーカーさんは、ノルウェー出身のDJ・音楽プロデューサーです。",
      "曲の再生回数は世界で合計1,000億回をこえる、世界的なアーティストです。"),
    p("2人は数か月前にニューヨークで初めて会いました。",
      "その後、ラウールさんがオスロのスタジオへ行き、一緒に曲を仕上げたそうです。",
      f"出典:{a(AVEX, 'avex')}・{a(MENT, 'MENT RECORDING')}"),
    p("歌詞はほとんどが英語ですが、サビには「夢は消えない」という日本語が入っています。",
      "動画の最後では、ラウールさんが英語で「次に会うときは東京でこの曲をやろう」と話していました。"),
    h3("動画のほかのファッション"),
    p("動画の途中には、レンガの壁の前で2人が握手する写真もはさまれています。",
      "こちらのラウールさんは、サングラスにクリーム色のシャツ、ベージュのワイドパンツという姿でした。",
      "ニットやシャツのブランドは、今のところ分かっていません。分かりしだい追記します。"),
    related([("ラウールの腕時計はカルティエ？タンク マストのモデルと値段", f"{SITE}/raul-cartier-tank-must-watch-497")]),

    listbox("まとめ", ["ラウールが11/9のアラン・ウォーカー動画で着けていた黒いハートのネックレスは、クリスタルヘイズとみられる",
                    "チェーンはセリーナ ネックレスの黒(295ドル・約4万5,000円)",
                    "ハートはジェリーハート ペンダントの黒(35〜60ドル・約5,400〜9,200円)",
                    "クリスタルヘイズはアラン・ウォーカーと同じノルウェー・オスロのブランド",
                    "コラボ曲「YUME」は2026年11月20日に配信"], big=True),
    p("世界的なアーティストとのコラボ発表の場で、ラウールさんはかわいい黒ハートを合わせていました。",
      "11月20日の「YUME」の配信もあわせて楽しみに待ちましょう。"),
])

ARTICLES = [
    {"key": "raul_crystalhaze", "title": "【未】ラウールのネックレスはどこの？アラン・ウォーカー動画の黒ハート",
     "slug": "raul-crystal-haze-heart-necklace",
     "categories": [4, 8], "frames": ["neck"], "html": body},
]


def main():
    manifest = []
    for art in ARTICLES:
        base = art["title"].replace("【未】", "")
        assert art["title"].startswith("【未】") and len(base) <= 35, (len(base), base)
        print("title len", len(base))
        path = os.path.join("articles", f"snowman_{art['key']}.html")
        with open(os.path.join(REPO, path), "w", encoding="utf-8") as f:
            f.write(art["html"])
        m = {k: v for k, v in art.items() if k != "html"}
        m["file"] = path.replace("\\", "/")
        manifest.append(m)
        print("wrote", path, len(art["html"]))
    with open(os.path.join(REPO, "articles", "snowman_raul_crystalhaze_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
