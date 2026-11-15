# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) 宮舘涼太が2026-11-15『宮舘涼太のロイヤルサロン』(TBSラジオ)の日に着ていた私服
(クロムハーツのハーフジップスウェット+Duke + Dexterのキスマーク ローファー)の記事HTMLを組み立てる。

usage: python tools/_build_snowman_miyadate_ch_halfzip_1115.py
articles/snowman_miyadate_ch_halfzip_1115.html と articles/snowman_miyadate_ch_halfzip_1115_manifest.json を書き出す。
投稿は tools/_upload_snowman_miyadate_ch_halfzip_1115.py。
写真は番組公式X(@datesama_TBSR)の投稿埋め込みだけ。第三者の特定アカウントの画像・言及は使わない。
"""
import os, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chomoand-2.com"
ACC = "#c0392b"      # 宮舘涼太のメンバーカラー(赤)
LINE = "#f0c4bf"
BG = "#fdf2f1"
MK = "#f9d3cf"

DD_OFFICIAL = "https://dukeanddexter.com/products/wilde-kiss-penny-loafer-mens"
DD_LEVEL = "https://us.levelshoes.com/duke-dexter-wilde-kiss-penny-loafers-black-leather-men-loafers-uzqefj"
END_DD = "https://www.endclothing.com/jp/brands/duke-dexter"
TFT_REG = "https://www.thefirsttimes.jp/?p=587901"
IG_MIYADATE = "https://www.instagram.com/ryota.miyadate0325_sn_official/"
CARTIER = f"{SITE}/?p=502"   # カルティエ×クロムハーツ記事(下書き)
DATE = "2026年11月15日確認"


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


def related(items):
    lis = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in items)
    return html(f'<div style="border:1px solid {LINE};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;">\n'
                f'<p style="margin:0 0 6px 0;font-weight:bold;color:{ACC};">あわせて読みたい</p>\n<ul style="margin:0;padding-left:20px;">{lis}</ul>\n</div>')


def xembed(user, sid):
    return html(f'<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><a href="https://twitter.com/{user}/status/{sid}">https://twitter.com/{user}/status/{sid}</a></blockquote>\n'
                '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def src(name, url, date):
    return f'出典:<a href="{url}" target="_blank" rel="noopener">{name}</a>({date})'


body = "".join([
    p("宮舘涼太さんが2026年11月15日、自身のラジオ番組『宮舘涼太のロイヤルサロン』(TBSラジオ)に出演しました。",
      "番組の公式Xには、放送中のスタジオで紅茶を飲む宮舘涼太さんの写真がアップされています。",
      f"このとき着ていたのが、胸に十字架のパッチが付いた黒いハーフジップ。{mk('クロムハーツのスウェット')}です。"),
    p("同じ日には、宮舘涼太さん本人のInstagramストーリーズにも、番組の看板を持った全身写真が載りました。",
      "足もとは、白い甲に赤いキスマークが入ったローファーです。",
      "この記事では、宮舘涼太さんが着ていたスウェットとローファーのブランド・商品名・値段を調べてまとめました。"),
    listbox("この記事でわかること", ["11/15『ロイヤルサロン』の日の私服コーデ",
                                    "トップスはクロムハーツのハーフジップスウェット",
                                    "ローファーはDuke + Dexter「Wilde Kiss Penny Loafer」",
                                    "それぞれの値段と買える場所",
                                    "チェックシャツ・デニム・メガネは？"], big=True),

    h2("宮舘涼太が『ロイヤルサロン』で着ていた私服"),
    keybox([("日付", "2026年11月15日(日)"),
            ("番組", "TBSラジオ『宮舘涼太のロイヤルサロン』(毎週日曜18:00〜18:30)"),
            ("写真", "番組公式X(@datesama_TBSR)の放送中の投稿+宮舘涼太さん本人のInstagramストーリーズ"),
            ("コーデ", "黒のハーフジップスウェット+赤チェックのシャツ+フレアデニム+キスマークのローファー")]),
    xembed("datesama_TBSR", "2121891444084654174"),
    p("番組の公式Xは、放送が始まってすぐに「『寒くない？急に…』という舘様はメガネとチェックのシャツが素敵です」と投稿しました。",
      f"写真の宮舘涼太さんは、金ぶちのメガネに、{mk('黒のハーフジップ+赤チェックのシャツ')}の重ね着。",
      "白いカップを手に、カメラに向かってちょっと首をかしげています。"),
    xembed("datesama_TBSR", "2121896818263159289"),
    p("続く投稿では、番組の企画「ロイヤル・カラコン・シチュエーション」の途中で、紅茶を飲む横顔をサブ(調整室)から撮った1枚も公開されています。",
      "こちらでは、スウェットのえりもとから赤チェックのシャツがのぞいているのがよくわかります。"),
    p(f'本人の<a href="{IG_MIYADATE}" target="_blank" rel="noopener">Instagram</a>のストーリーズでは、緑のカーテンの前で番組の看板を持った全身写真も載りました。',
      "スウェットの下からはチェックのシャツのすそが長めに出ていて、パンツはすそが広がったフレアデニム。",
      "足もとは黒と白のツートンのローファーで、つま先に赤いキスマークが付いていました。",
      "ストーリーズは24時間で消えるため、この記事では番組公式Xの写真を紹介しています。"),

    h2("トップスはクロムハーツのハーフジップスウェット"),
    table([["項目", "内容"],
           ["ブランド", "クロムハーツ(CHROME HEARTS)"],
           ["アイテム", "ハーフジップのプルオーバースウェット"],
           ["色", "ブラック"],
           ["えり", "スタンドカラー・シルバーのジップ"],
           ["胸", "黒レザーのクロス(十字架)パッチ+ブランド名入りのシルバープレート"],
           ["その他", "おなかにカンガルーポケット・肩が落ちたゆったりシルエット"],
           ["値段", "公式の値段は非公開(中古市場では数十万円台が目安)"]]),
    p(f"宮舘涼太さんのトップスは、{mk('クロムハーツのハーフジップスウェット')}とみられます。",
      "左胸に付いた黒いレザーの十字架と、その上に重ねたシルバーのプレートは、クロムハーツを代表するデザイン。",
      "ストーリーズの写真では、プレートに「CHROME HEARTS」の文字があるのも確認できます。"),
    p("生地は表面がやわらかく起毛した黒で、えりは首もとまで立つスタンドカラー。",
      "胸の下に切り替えのラインが入り、おなかには大きなカンガルーポケットが付いています。",
      "肩の線が腕のほうへ落ちたゆったりしたシルエットなので、下に着たシャツのすそを出しても重たく見えません。"),

    h3("値段は？どこで買える？"),
    p("クロムハーツの服は、日本では直営店などの正規店での販売が中心で、公式サイトに値段が出ていないものがほとんどです。",
      "このハーフジップも、2026年11月15日の時点で公式オンラインストアには見つかりませんでした。"),
    p(f"中古市場をみると、クロスパッチの付いたクロムハーツのスウェットは{mk('数十万円台')}で出品されていることが多く、ハーフジップ型ではさらに高い値段がついている例もあります。",
      "人気のブランドでニセモノも多いので、買うときは正規店か、鑑定の付いた信頼できるお店を選ぶのが安心です。"),

    h2("ローファーはDuke + Dexter「Wilde Kiss Penny Loafer」"),
    table([["項目", "内容"],
           ["ブランド", "Duke + Dexter(デューク アンド デクスター)"],
           ["商品名", "Wilde Kiss Penny Loafer(ワイルド キス ペニーローファー)"],
           ["品番", "PWKISSPEN-KISS"],
           ["色", "ブラック×オフホワイト(甲に赤いキスマーク)"],
           ["素材", "アッパー:イタリアンレザー/裏地:レザー"],
           ["ソール", "25mmのラバーソール"],
           ["つくり", "アーモンドトゥ・ペニーストラップ・ポルトガル製(海外の取扱店の表記)"],
           ["値段", "公式サイト270ポンド/海外の取扱店で350〜370ドル"]]),
    p(f"足もとのローファーは、ロンドンのシューズブランドDuke + Dexterの{mk('「Wilde Kiss Penny Loafer」')}とみられます。",
      "黒いレザーの本体に、甲だけオフホワイトの切り替え。そこに真っ赤なキスマークが1つずつプリントされているのが特徴です。"),
    p("Duke + Dexterは2015年にロンドンで生まれたブランドで、ローファーやブローグなど伝統的な紳士靴に、遊び心のある柄をのせたデザインで知られています。",
      "宮舘涼太さんのような「王道のきれいめ+ちょっと遊び」のコーデにぴったりの1足です。",
      src("Duke + Dexter公式", DD_OFFICIAL, DATE)),

    h3("値段は日本円でおよそ5万円台"),
    p(f"公式サイトでの値段は{mk('270ポンド')}、海外の取扱店では350〜370ドルほどで売られています。",
      "日本円にすると、およそ5万円台です(為替によって変わります)。",
      src("Level Shoes", DD_LEVEL, DATE)),
    p(f'日本では、海外通販サイトEND.の<a href="{END_DD}" target="_blank" rel="noopener">日本語ページ</a>でDuke + Dexterの靴を扱っています。',
      "海外の取扱店では「小さめのつくりなので、ハーフ〜1サイズ大きめがおすすめ」と案内されているので、サイズ選びには注意してください。",
      "2026年11月15日の時点では、公式サイトで売り切れになっているサイズもありました。"),

    h2("チェックシャツ・デニム・メガネは？"),
    keybox([("シャツ", "赤・黄・黒のチェックのネルシャツ(すそが切りっぱなし風、品名は未特定)"),
            ("パンツ", "色落ちしたブルーのフレアデニム(品名は未特定)"),
            ("メガネ", "上だけ黒と金のフレームのブロウ型、テンプルに金の飾り(品名は未特定)"),
            ("腕時計", "金色のケースの時計(品名は未特定)")]),
    p("スウェットの下に重ねた赤チェックのシャツは、宮舘涼太さんのメンバーカラーの赤にぴったり。",
      "すそはほつれたような切りっぱなしで、あえてスウェットの下から長めに出して着ていました。"),
    p("パンツはひざから下が広がるフレアデニムで、キスマークのローファーにすそがかぶるくらいの長さ。",
      "メガネは、上の部分だけ黒と金のフレームが付いたクラシックな形です。",
      "シャツ・デニム・メガネの品名は、わかりしだい追記します。"),

    h2("『宮舘涼太のロイヤルサロン』ってどんな番組？"),
    p("『宮舘涼太のロイヤルサロン』は、宮舘涼太さんがパーソナリティを務めるTBSラジオの番組です。",
      "2025年1月2日の新春スペシャルが好評で、2025年春からレギュラー放送になりました。",
      f"放送は{mk('毎週日曜18:00〜18:30')}。",
      src("THE FIRST TIMES", TFT_REG, "2025年3月21日")),
    p("11月15日の放送では、WAVEコンタクトの提供で「ロイヤル・カラコン・シチュエーション」という企画を行いました。",
      "番組公式Xは毎週、放送中のスタジオの写真をアップしているので、宮舘涼太さんの私服をチェックしたい人はフォローしておくのがおすすめです。"),

    h2("宮舘涼太とクロムハーツ"),
    p("宮舘涼太さんがクロムハーツを着るのは、今回が初めてではありません。",
      "2024年8月のInstagramでは、クロムハーツとリーバイスのコラボデニムに、カルティエの時計を合わせた私服を見せていました。",
      f'そのときの時計とデニムは<a href="{CARTIER}">こちらの記事</a>でまとめています。'),
    p("黒いクロムハーツに、赤のチェックとキスマークのローファー。",
      "ハードなブランドを着ても、どこか上品で華やかにまとまっているのが「舘様」らしいところです。"),

    h2("まとめ"),
    listbox("まとめ", ["宮舘涼太は11/15『ロイヤルサロン』の日、黒のハーフジップ×赤チェックの重ね着",
                      "トップスはクロムハーツのハーフジップスウェット(中古相場は数十万円台)",
                      "ローファーはDuke + Dexter「Wilde Kiss Penny Loafer」(公式270ポンド)",
                      "ローファーは日本円でおよそ5万円台、END.などの海外通販で買える",
                      "シャツ・デニム・メガネは未特定、わかりしだい追記"], big=True),
    related([("宮舘涼太の私物はカルティエとクロムハーツ！時計とデニムの値段は？", CARTIER)]),
])

TITLE = "【未】宮舘涼太の私服はクロムハーツ！キスマークのローファーはどこの？"
assert len(TITLE.replace("【未】", "")) <= 35, len(TITLE.replace("【未】", ""))

ARTICLES = [
    {"key": "miyadate_ch_halfzip_1115", "title": TITLE,
     "slug": "miyadate-ryota-chrome-hearts-halfzip-duke-dexter-loafer",
     "categories": [4, 13], "html": body},
]


def main():
    manifest = []
    for a in ARTICLES:
        path = os.path.join("articles", f"snowman_{a['key']}.html")
        with open(os.path.join(REPO, path), "w", encoding="utf-8") as f:
            f.write(a["html"])
        m = {k: v for k, v in a.items() if k != "html"}
        m["file"] = path
        manifest.append(m)
        print("wrote", path, len(a["html"]), "title len", len(TITLE.replace("【未】", "")))
    with open(os.path.join(REPO, "articles", "snowman_miyadate_ch_halfzip_1115_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
