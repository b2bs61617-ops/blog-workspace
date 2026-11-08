# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) 佐久間大介のX(2026-11-08「今日は履きたくなって膝下ハーフパンツ (^^)」)で
履いていたクロムハーツ×コンバース「ガンスリンガー」ハイカットの記事HTMLを組み立てる。

usage: python tools/_build_snowman_sakuma_ch_converse_1108.py
articles/snowman_sakuma_ch_converse.html と articles/snowman_sakuma_ch_converse_manifest.json を書き出す。
投稿は tools/_upload_snowman_sakuma_ch_converse_1108.py。
第三者(特定アカウント)の画像は使わず、本人のXポストを埋め込む方針。
"""
import os, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chomoand-2.com"
ACC = "#d9589f"      # 佐久間大介のメンバーカラー(ピンク)
BG = "#fdf0f7"
LINE = "#f3cfe3"
MK = "#f7d6e8"
X_USER = "SAK_SAK_SAKUMA"
X_ID = "2119293494842020042"
LIFE = "https://chromehearts.jpn.com/"
LIFE_GUIDE = "https://lifeonline.jp/chromehearts-and-converse-collaboration"
RAKUMA = "https://fril.jp/brand/161/keyword/2476"
REALREAL = "https://www.therealreal.com/products/men/shoes/sneakers/chrome-hearts-x-converse-gunslinger-sneakers-drp0c"
REALCLO = "https://www.realclothes.jp/shoes/converse/kaitori.html/page/2?detail=897057"


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


def related(items):
    lis = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in items)
    return html(f'<div style="border:1px solid {LINE};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;">\n'
                f'<p style="margin:0 0 6px 0;font-weight:bold;color:{ACC};">あわせて読みたい</p>\n<ul style="margin:0;padding-left:20px;">{lis}</ul>\n</div>')


body = "".join([
    p("2026年11月8日、Snow Manの佐久間大介さんがXに「今日は履きたくなって膝下ハーフパンツ (^^)」と足元の写真を投稿しました。",
      "写真に写っていた黒いハイカットのスニーカーは、" + mk("クロムハーツ×コンバースの「ガンスリンガー」") + "とみられます。",
      "この記事では、スニーカーの名前・特徴・値段(中古の相場)と、「250万円」といううわさが本当なのかをまとめます。"),
    xembed(X_USER, X_ID),
    listbox("この記事でわかること", ["佐久間大介がXで履いていたスニーカーのブランドとモデル名",
                              "写真のスニーカーと同じだと言える理由",
                              "値段は？「250万円」は本当？(2026年11月8日時点の相場)",
                              "どこで買える？"], big=True),

    h2("佐久間大介の靴はクロムハーツ×コンバース「ガンスリンガー」"),
    keybox([("ブランド", "クロムハーツ(CHROME HEARTS)×コンバース(CONVERSE)"),
            ("モデル", "オールスター レザー ハイカット「ガンスリンガー」"),
            ("中古の相場", "約40万〜85万円(2026年11月8日時点)")]),
    p("佐久間大介さんの写真は、上から足元を撮ったもの。",
      "黒い膝下のハーフパンツに、白地に黒いラインの入ったソックス、そして黒レザーのハイカットスニーカーを合わせています。",
      "このスニーカーは、コンバースの定番「オールスター」のハイカットをベースに、クロムハーツがレザーとシルバーのパーツで仕上げたものです。"),
    table([["項目", "内容"],
           ["ブランド", "クロムハーツ×コンバース"],
           ["モデル", "オールスター レザー ハイカット「ガンスリンガー」"],
           ["コンバースの品番", "1S581(買取店の商品名より)"],
           ["色", "ブラック(つま先・ソールは白)"],
           ["素材", "レザー、シルバーのバックル・ボタン"],
           ["特徴", "ひもの代わりにバックル付きのストラップ5本、かかとにジップ"],
           ["定価", "公式の発表なし(クロムハーツの店頭のみで販売)"]]),
    p("「ガンスリンガー」はクロムハーツのベルトで使われている、角が丸い四角形のバックルの名前です。",
      "このスニーカーは、そのガンスリンガーバックルを" + mk("1足に5個ずつ") + "付けた、かなり重厚なつくりになっています。"),

    h2("写真のスニーカーと同じだと言える理由"),
    p("佐久間大介さんの写真と、中古市場に出ている「ガンスリンガー」の写真を見比べると、次の点が一致しています。"),
    listbox("写真と「ガンスリンガー」の一致点", [
        "黒のスムースレザーのハイカットで、つま先が白いオールスターの形",
        "ひもの代わりに、横向きのストラップが片足5本",
        "ストラップの先に、角が丸い四角形のシルバーのバックル(ガンスリンガーバックル)",
        "ストラップの反対側に、丸いシルバーのボタンが並ぶ",
        "くるぶしの内側に、コンバースの丸い「ALL STAR」パッチ",
    ]),
    p("コンバースのオールスターにバックル付きのストラップを並べたスニーカーは、ほかではほとんど見かけません。",
      "本人がブランド名を書いているわけではありませんが、ここまで特徴が一致しているので、同じモデルとみてよさそうです。"),
    p("ちなみに、合わせているソックスにもゴシック体のような文字が入っていますが、写真からは文字が読み取れず、ブランドまでは分かりませんでした。"),

    h2("値段は？「250万円」は本当？"),
    h3("定価は公表されていない"),
    p("クロムハーツとコンバースのスニーカーは、大量生産のコラボ商品ではありません。",
      "コンバースのオールスターをもとに、クロムハーツが自社のレザーやシルバーのパーツで仕上げ、クロムハーツの店舗だけで売られてきたものとされています。",
      "そのため" + mk("公式の定価は公表されておらず") + "、今は中古でしか手に入らないモデルです。",
      f"出典:{a(LIFE_GUIDE, 'LIFE「クロムハーツ×コンバースは実在する？」')}"),
    h3("中古の相場は約40万〜85万円"),
    p("2026年11月8日に調べた、ガンスリンガーの中古の取引・買取の例は次のとおりです。"),
    table([["どこで", "状態", "価格"],
           [a(LIFE, "クロムハーツ買取専門店LIFE"), "中古(状態S)", "420,000円(買取実績)"],
           [a(RAKUMA, "ラクマ"), "中古", "680,000円(売り切れ)"],
           [a(RAKUMA, "ラクマ"), "新品未使用", "740,000円(売り切れ)"],
           ["楽天市場の中古ショップ", "中古", "849,900円(販売価格)"],
           [a(REALREAL, "The RealReal(アメリカ)"), "中古・US9.5", "2,800ドル(約43万円)"]]),
    p("買取が約42万円、売れた値段が68万〜74万円、お店の販売価格が85万円ほど。",
      "クロムハーツの買取店のまとめでも、レザーのコンバースやガンスリンガーは「60万〜100万円以上」の取引があるとされています。",
      "サイズや状態、パーツがそろっているかで大きく変わりますが、" + mk("中古でもおよそ40万〜85万円") + "が目安です。"),
    h3("「250万円」は確認できず"),
    p("SNSでは、佐久間大介さんのスニーカーの値段として「取引価格 約250万円」という数字も出回っています。",
      "ただ、今回調べた範囲では、" + mk("250万円で取引された例は見つかりませんでした") + "。",
      "サイズがめずらしい新品などで高い値段が付くことはありえますが、ふつうの相場は数十万円台〜100万円前後と考えておくのがよさそうです。"),
    p("とはいえ、スニーカー1足で40万円以上というのは、やはりかなりの高級品。",
      "シルバーのバックルとボタンだけでも、クロムハーツのアクセサリー何個分にもなります。"),

    h2("どこで買える？"),
    listbox("購入先", [
        "クロムハーツの店舗:もともと店頭だけで売られていたモデルで、今は店頭でもまず見かけない",
        f"中古の買取・販売店:{a(REALCLO, 'リアクロ')}などのブランド買取店で取り扱われることがある",
        "フリマアプリ(ラクマ・メルカリなど)・海外の中古サイト(The RealReal・Grailedなど)",
    ]),
    p("中古で買うときは、バックルやボタンの欠けや交換がないか、付属品がそろっているかを必ず確認しましょう。",
      "クロムハーツは偽物も多いブランドなので、クロムハーツに詳しいお店で買うのが安心です。"),

    h2("佐久間大介はクロムハーツ好き？"),
    p("佐久間大介さんは、これまでもXやInstagramで私服を載せていて、ルイ・ヴィトンやブレゲなどの高級ブランドを身につけた姿が話題になってきました。",
      "今回は「履きたくなって」というひと言どおり、黒いハーフパンツにソックスを見せて、主役のスニーカーが目立つコーデでした。"),
    related([("佐久間大介X写真の時計はブレゲ？スースクリプションの値段は？", f"{SITE}/daisuke-sakuma-breguet-souscription-price-360")]),

    listbox("まとめ", ["佐久間大介が11/8のXで履いていたのは、クロムハーツ×コンバースの「ガンスリンガー」とみられる",
                    "黒レザーのオールスター ハイカットに、ガンスリンガーバックル付きのストラップが片足5本",
                    "定価は公表されておらず、クロムハーツの店頭のみで売られていたモデル",
                    "中古の相場は約40万〜85万円(2026年11月8日時点)",
                    "SNSで出回っている「約250万円」は、取引例が見つからず確認できなかった"], big=True),
    p("さりげない足元の写真でしたが、履いていたのは40万円を超えるレアなスニーカーでした。",
      "佐久間大介さんの私服は、また新しいアイテムが分かりしだい追記します。"),
])

ARTICLES = [
    {"key": "sakuma_ch_converse", "title": "【未】佐久間大介の靴はクロムハーツ？スニーカーの値段も！",
     "slug": "daisuke-sakuma-chrome-hearts-converse-gunslinger",
     "categories": [4, 14], "html": body},
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
    with open(os.path.join(REPO, "articles", "snowman_sakuma_ch_converse_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
