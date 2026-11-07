# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) すのちゅーぶジョナサン回(2026-11-04、F9qbyNJPS6E)で渡辺翔太が着ていたトッズ日本限定ロンTの記事HTMLを組み立てる。

usage: python tools/_build_snowman_watanabe_tods_longtee_1107.py
articles/snowman_wtlt.html と articles/snowman_wtlt_manifest.json を書き出す。
投稿は tools/_upload_snowman_watanabe_tods_longtee_1107.py({{IMG:name}} を images/snowman_wtlt_frame_{name}.jpg のURLに置き換える)。
"""
import os, json
from urllib.parse import quote

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACC = "#3f7fc4"      # 渡辺翔太のメンバーカラー(青)
BG = "#eef5fc"
LINE = "#cfe0f3"
MK = "#d6e2f0"

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


def quote_box(lines, src):
    body = "<br>\n".join(lines)
    return html(f'<div style="border:1px solid {LINE};border-radius:4px;padding:12px 18px;margin:0 0 16px 0;background:{BG};">\n'
                f'<p style="margin:0;">{body}</p>\n<p style="margin:6px 0 0 0;font-size:0.85em;color:#777;text-align:right;">{src}</p>\n</div>')


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


def ytembed(vid):
    return html(f'<div style="position:relative;width:100%;padding-top:56.25%;margin:0 0 16px 0;">'
                f'<iframe src="https://www.youtube.com/embed/{vid}" title="YouTube video" loading="lazy" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" '
                'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')


def frame(name, alt, src, label):
    return html('<figure class="wp-block-image size-large">\n'
                f'<img src="{{{{IMG:{name}}}}}" alt="{alt}" width="1280" height="720" style="max-width:100%;height:auto;" loading="lazy">\n'
                f'<figcaption style="font-size:0.8em;color:#888;">出典:<a href="{src}" target="_blank" rel="noopener">{label}</a></figcaption>\n</figure>')


def gmap(q):
    return html(f'<iframe src="https://www.google.com/maps?q={quote(q)}&output=embed" width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy"></iframe>')



SITE = "https://chomoand-2.com"
VID = "F9qbyNJPS6E"
YT = f"https://www.youtube.com/watch?v={VID}"
TODS = "https://www.tods.com/jp-ja/%E3%83%AD%E3%83%B3%E3%82%B0-%E3%82%B9%E3%83%AA%E3%83%BC%E3%83%96-T-%E3%82%B7%E3%83%A3%E3%83%84/p/X5UB3535900Z2EB001/"
TL = f'<a href="{TODS}" target="_blank" rel="noopener">トッズ公式オンラインストア</a>'

body = "".join([
    p("2026年11月4日に配信されたSnow Manの公式YouTube「すのちゅーぶ」のジョナサン回で、渡辺翔太さんが着ていた白いロンT。",
      "胸に青い「TO/DS」のロゴが入ったこのロンTは、" + mk("トッズ(TOD'S)の日本限定「ロング スリーブ T シャツ」75,900円(税込)") + "とみられます。",
      "この記事では、ロンTの商品名・値段・品番、動画のロンTと同じだと言える理由、在庫の状況、どこで買えるかをまとめます。"),
    ytembed(VID),
    listbox("この記事でわかること", ["渡辺翔太がすのちゅーぶで着ていたロンTのブランドと商品名", "値段・品番・素材", "動画のロンTと同じだと言える理由",
                              "サイズと在庫(2026年11月7日時点)・どこで買えるか", "渡辺翔太とトッズの関係"], big=True),

    h2("渡辺翔太のロンTはトッズの日本限定「ロング スリーブ T シャツ」"),
    keybox([("ブランド", "トッズ(TOD'S)"), ("商品名", "ロング スリーブ T シャツ(日本限定)"), ("値段", "75,900円(税込)")]),
    p("ジョナサン回の渡辺翔太さんは、白の長袖Tシャツにブラウンのセルフレームの眼鏡、淡いブルーのデニムという、すっきりしたコーデでした。",
      "このロンTの胸に入っているのが、トッズのロゴを「TO」と「DS」の2段に分けた青いロゴです。"),
    frame("seated", "すのちゅーぶジョナサン回でトッズのロンTを着た渡辺翔太", YT, "Snow Man公式YouTube"),
    table([["項目", "内容"],
           ["ブランド", "トッズ(TOD'S)"],
           ["商品名", "ロング スリーブ T シャツ"],
           ["値段", "75,900円(税込)"],
           ["品番", "X5UB3535900Z2EB001"],
           ["色", "ホワイト(全3色)"],
           ["素材", "コットン100%"],
           ["生産国", "イタリア"],
           ["そのほか", "日本限定・胸にトッズのロゴの刺繍"]]),
    p(f"出典:{TL}(2026年11月7日確認)"),
    p("公式の説明は「胸にトッズ ロゴの刺繍を施した、ロング スリーブ ラウンドネック T シャツ」。",
      f"ロゴはプリントではなく{mk('刺繍')}で、近くで見ると糸の立体感があります。",
      "首元の内側にはトッズのネームタグと、オレンジのテープが付いています。"),

    h2("動画のロンTと同じだと言える理由"),
    p("動画の映像と公式の商品写真を見比べると、次の点が一致しています。"),
    listbox("動画と公式の商品の一致点", [
        "白の長袖で、丸首(ラウンドネック)",
        "ロゴが「TO」と「DS」の2段に分かれている",
        "ロゴの色が鮮やかな青で、角ばったステンシル風の太い文字",
        "ロゴの位置が左胸(本人から見て左)で、大きさも同じくらい",
    ]),
    frame("opening", "すのちゅーぶジョナサン回のオープニングでトッズのロンTを着た渡辺翔太", YT, "Snow Man公式YouTube"),
    p("トッズのロゴは、ふだんは「TOD'S」と1行で書かれることがほとんどです。",
      "2段に分けたこのデザインは珍しく、ひと目でこのロンTだと分かる目印になっています。",
      "本人や公式からの説明はないものの、デザインがここまで一致しているので、同じ商品とみてよさそうです。"),

    h2("サイズと在庫・どこで買える？"),
    h3("サイズはXXSからXXXLまで"),
    p("サイズはXXS・XS・S・M・L・XL・XXL・XXXLの8サイズです。",
      f"2026年11月7日に公式オンラインストアを確認したときは、{mk('S〜XXXLが売り切れで、在庫があるのはXXSとXSだけ')}でした。",
      "売り切れのサイズには「入荷のお知らせ」のボタンがあり、再入荷したときにメールで知らせてもらえます。"),
    table([["サイズ", "在庫(2026年11月7日時点)"],
           ["XXS・XS", "あり"],
           ["S・M・L・XL・XXL・XXXL", "売り切れ(入荷のお知らせあり)"]]),
    p("在庫は日々変わるので、気になる人は早めにチェックしてみてください。"),
    h3("買えるのはトッズの公式オンラインストアと直営店"),
    listbox("購入先", [
        f"{TL}(ロング スリーブ T シャツ 75,900円)",
        "トッズの直営店(公式サイトの「店舗在庫を確認」から、近くのお店の在庫を調べられる)",
        "日本限定の商品なので、海外のトッズのサイトでは扱っていないとみられる",
    ]),
    p("お店に問い合わせるときは、品番「X5UB3535900Z2EB001」を伝えるとスムーズです。",
      "色はホワイトのほかに2色あり、公式オンラインストアの商品ページで切り替えて見られます。"),
    p("白い服で刺繍のロゴが入っているので、洗うときは付属のお手入れの説明書を確認してからにしましょう。"),

    h2("渡辺翔太はトッズのブランドアンバサダー"),
    keybox([("就任発表", "2026年1月26日"), ("ポイント", "トッズのブランドアンバサダーに日本人男性が選ばれたのは初めて")]),
    p(f"渡辺翔太さんは2026年1月26日、{mk('日本人男性で初めてのトッズのブランドアンバサダー')}に就任しました。",
      "2月にはアンバサダーとして初めてミラノコレクションに出席し、10月にはInstagramに「TOD'Sの秋」と題したトッズのコーデを載せています。"),
    p("就任のときには、トッズの服について「シンプルこそ至高」という自分の考え方にも通じている、と話していました。",
      "今回のロンTも、白に青いロゴだけのシンプルなデザインで、その言葉どおりのアイテムです。",
      "撮影でトッズを着る機会が多い渡辺翔太さんですが、YouTubeのラフな企画でも、さりげなくトッズを取り入れていました。"),
    related([("渡辺翔太インスタ「TOD'Sの秋」の服はどれ？トッズの値段は？", f"{SITE}/shota-watanabe-tods-autumn-bomber-price-343")]),

    h2("ジョナサン回はどんな動画？"),
    p("このロンTを着ていたのは、渡辺翔太さんの持ち込み企画「ジョナサンの秋のおすすめメニューTOP10を当てよう！」の回です。",
      "向井康二さん・宮舘涼太さんと3人で、人気TOP10に入っていそうなメニューを予想して注文しました。",
      "渡辺翔太さんは頼んだ3品がすべて圏外で没収になり、自分の企画なのに「プレゼンター後悔中」というテロップが出るほどでした。"),
    p("ロケ地のお店や、動画で公開されたランキングは別の記事でまとめています。"),
    related([("【ジョナサン人気TOP10を当てろ！】ロケ地はどこ？店舗とランキング", f"{SITE}/?p=574")]),

    listbox("まとめ", ["渡辺翔太がすのちゅーぶジョナサン回で着ていたのは、トッズの日本限定「ロング スリーブ T シャツ」とみられる",
                    "値段は75,900円(税込)、品番X5UB3535900Z2EB001、コットン100%・イタリア製",
                    "胸の「TO/DS」2段ロゴは刺繍で、色・形・位置が動画と一致",
                    "2026年11月7日時点でS〜XXXLは売り切れ、XXS・XSのみ在庫あり",
                    "買えるのはトッズ公式オンラインストアと直営店"], big=True),
    p("アンバサダーらしく、ふだんの企画でもトッズを着こなしていた渡辺翔太さん。",
      "日本限定のアイテムなので、気になった人は公式オンラインストアの在庫をチェックしてみてください。"),
])

ARTICLES = [
    {"key": "wtlt", "title": "【未】【ジョナサン人気TOP10を当てろ！】渡辺翔太のロンTはどこの？値段も",
     "slug": "shota-watanabe-tods-long-sleeve-tee",
     "categories": [4, 9], "frames": ["seated", "opening"], "html": body},
]


def main():
    manifest = []
    for a in ARTICLES:
        path = os.path.join("articles", f"snowman_{a['key']}.html")
        with open(os.path.join(REPO, path), "w", encoding="utf-8") as f:
            f.write(a["html"])
        m = {k: v for k, v in a.items() if k != "html"}
        m["file"] = path.replace("\\", "/")
        manifest.append(m)
        print("wrote", path)
    with open(os.path.join(REPO, "articles", "snowman_wtlt_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
