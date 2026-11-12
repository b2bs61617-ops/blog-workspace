# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) 目黒蓮がZoff「紫外線 vs. Zoff」の新ビジュアル(2026-11-12更新)でかけていた
メガネ(ZK192001-14E1)の記事HTMLを組み立てる。

usage: python tools/_build_snowman_meguro_zoff_1112.py
articles/snowman_meguro_zoff.html と articles/snowman_meguro_zoff_manifest.json を書き出す。
投稿は tools/_upload_snowman_meguro_zoff_1112.py。
根拠はZoff公式CMページ(zoff-uvcut.aspx)の「広告着用商品 ZK192001_14E1」表記。第三者の特定投稿は使わない。
"""
import os, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chomoand-2.com"
ACC = "#333333"      # 目黒蓮のメンバーカラー(黒)
BG = "#f4f4f4"
LINE = "#d4d4d4"
MK = "#dedede"
ZUV = "https://www.zoff.co.jp/shop/contents/zoff-uvcut.aspx"
ZK = "https://www.zoff.co.jp/shop/g/gZK192001-14E1/"
ZUVLENS = "https://www.zoff.co.jp/shop/contents/zoffuv.aspx"
TFT = "https://www.thefirsttimes.jp/?p=896563"


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



YT_CM = "e2g_uF2NToQ"
YT_MK = "SIxlXG9OVlk"


def yt(vid):
    url = f"https://www.youtube.com/watch?v={vid}"
    return (f'<!-- wp:embed {{"url":"{url}","type":"video","providerNameSlug":"youtube","responsive":true,'
            f'"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->\n'
            f'<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube '
            f'wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\n{url}\n'
            f"</div></figure>\n<!-- /wp:embed -->\n")


body = "".join([
    p("2026年11月12日、Zoffの公式サイトで、目黒蓮さんの新しい広告ビジュアルが公開されました。",
      "「紫外線 vs. Zoff」シリーズの、透明なメガネをかけた1枚です。",
      "このメガネは、" + mk("Zoffの「ZK192001-14E1」(1万2,100円)") + "です。"),
    listbox("この記事でわかること", ["目黒蓮が新ビジュアルでかけているメガネの商品名と型番",
                              "値段は？CMと同じ透明レンズにするといくら？",
                              "サイズ・重さ・色違い",
                              "どこで買える？オンラインでの買い方",
                              "CM「紫外線 vs. Zoff」篇の内容"], big=True),

    h2("目黒蓮のZoffメガネはZK192001-14E1"),
    keybox([("ブランド", "Zoff(ゾフ)"),
            ("商品名", "目元に華やかさをプラスするメタルフレーム/CLASSIC[中顔面短縮みえメガネ]"),
            ("型番", "ZK192001-14E1(ブラック)"),
            ("値段", "1万2,100円(税込・セットレンズ込み)"),
            ("広告と同じレンズ", "Zoff UVクリアレンズ(+4,400円〜)")]),
    p("Zoffの「紫外線 vs. Zoff」特設ページには、" + mk("「広告着用商品」としてこのメガネがのっています") + "。",
      "つまり、ファンの予想ではなく、Zoff公式が出している答えです。"),
    figure("product", "目黒蓮がZoffの広告でかけているメガネZK192001-14E1",
           "出典:Zoff公式オンラインストア(ZK192001-14E1)"),
    p("黒くて細い丸いフチに、金色の鼻の部分(ブリッジ)とつるを合わせたメガネです。",
      "広告の写真でも、黒いフチと金色のブリッジがはっきり見えます。"),
    p(f"公式ページ:{a(ZUV, 'Zoff「紫外線 vs. Zoff」特設ページ')}・{a(ZK, '商品ページ(ZK192001-14E1)')}"),

    h2("値段は？CMと同じにするといくら？"),
    p("フレームの値段は1万2,100円(税込)です。",
      "この値段には、ふつうの透明レンズ(セットレンズ)が入っています。"),
    p("広告のテーマは「透明でもUV100%CUT」です。",
      "広告と同じにしたいなら、" + mk("「Zoff UVクリアレンズ」に変える") + "のがおすすめです。",
      "UVクリアレンズは、フレーム代に4,400円〜をたした値段になります。"),
    table([["組み合わせ", "値段(税込)"],
           ["フレーム+セットレンズ", "1万2,100円"],
           ["フレーム+UVクリアレンズ", "1万6,500円〜"]]),
    p("値段は2026年11月12日にZoff公式オンラインストアで確認したものです。",
      "セールや店によって変わることがあるので、買う前に確かめてください。"),
    h3("UVクリアレンズってどんなレンズ？"),
    p("見た目はふつうの透明レンズなのに、紫外線を100%カットするレンズです。",
      "数字はISO12312-1という国際的な基準で測ったものだそうです。"),
    listbox("UVクリアレンズのポイント", ["色が付いていないので、だてメガネ感覚で使える",
                                    "紫外線100%カット(ISO12312-1基準)",
                                    "レンズの裏側にもUVカットコート",
                                    "超撥水(ちょうはっすい)で、お手入れがかんたん",
                                    "度付きでも、度なしでも作れる"]),
    p("サングラスは、職場や学校ではかけにくいことがありますよね。",
      "透明なレンズなら、いつものメガネと同じ感覚で紫外線対策ができます。",
      f"詳しくは{a(ZUVLENS, 'Zoff UVクリアレンズのページ')}にのっています。"),

    h2("サイズ・重さ・色違い"),
    table([["項目", "内容"],
           ["形", "ボストン(フチが全部あるフルリム)"],
           ["サイズ", "50□21-142"],
           ["重さ", "13.8g(デモレンズなし)"],
           ["素材", "フロント:ステンレス"],
           ["仕上がりの大きさ", "横 約141mm・縦 約46mm"]]),
    p("「50□21-142」は、レンズの横幅50mm、鼻の部分21mm、つるの長さ142mmという意味です。",
      "13.8gととても軽いので、1日中かけていても疲れにくそうです。"),
    p("男女どちらでも使えるデザインで、Zoffの「CLASSIC」シリーズのロングセラーです。",
      "「中顔面短縮みえメガネ」とも呼ばれ、ほほの余白を小さく見せる形として人気があります。"),
    h3("色は4色"),
    table([["型番", "色"],
           ["ZK192001-14E1", "ブラック×ゴールド(目黒蓮の色)"],
           ["ZK192001-18E1", "ブラック×シルバー"],
           ["ZK192001-43E1", "ブラウン"],
           ["ZK192001-49E1", "べっこう柄のブラウン"]]),
    p("目黒蓮さんと同じにしたいなら、型番の最後が「14E1」のブラックを選びましょう。",
      "18E1も黒いフチですが、ブリッジとつるがシルバーなので印象が少しちがいます。"),

    h2("どこで買える？オンラインでの買い方"),
    listbox("購入先", [f"Zoff公式オンラインストア:{a(ZK, 'ZK192001-14E1の商品ページ')}",
                    "全国のZoffのお店(在庫は公式サイトの「店頭の在庫を探す」で確認できる)"]),
    p("11月12日の時点で、オンラインストアでは「在庫残りわずか」と表示されていました。",
      "広告の公開で人気が集まりそうなので、気になる人は早めにチェックしてください。"),
    h3("オンラインでUVクリアレンズにする方法"),
    listbox("オンラインストアでの手順", ["メガネをカートに入れる",
                                  "カートの画面で「サイト上で選ぶ」を選ぶ",
                                  "「度付き」か「度無し」を選ぶ",
                                  "レンズの種類で「Zoff UVクリア(透明)レンズ」を選ぶ",
                                  "届け先と支払い方法を選んで注文する"]),
    p("フレームだけオンラインで買って、あとでお店でレンズを選ぶこともできます。",
      "その場合はレンズ交換券が届き、UVクリアレンズ代の4,400円はお店で払います。"),

    h2("CM「紫外線 vs. Zoff」篇とは"),
    keybox([("CM名", "「紫外線 vs. Zoff」篇"),
            ("放送開始", "2026年10月9日から全国で順番に"),
            ("撮影場所", "カナダ"),
            ("メッセージ", "みんなのめのため、未来のため。")]),
    yt(YT_CM),
    p("目黒蓮さんは、Zoffのグローバルブランドアンバサダーをつとめています。",
      "このCMは、10月10日の「目の愛護デー」に合わせて作られました。"),
    p("目黒蓮さんが訪れた街で、働く人も子どもたちも、みんなが自然にサングラスをかけている。",
      "そんな「目を守るのが当たり前の未来」をえがいたCMです。",
      "Zoffは、2030年までに日本のサングラスをかける人を「ふたりにひとり」にする目標もかかげています。"),
    p("撮影は、目黒蓮さんがドラマの撮影で滞在していたカナダで行われました。",
      "テレビCMの中で目黒蓮さんがかけているのは、紫外線で色が変わる「調光レンズ」です。",
      f"出典:{a(TFT, 'THE FIRST TIMES')}・{a(ZUV, 'Zoff公式')}"),
    h3("11月12日の新ビジュアルは「ALL SEASON」"),
    p("今回の新しい広告には「ALL SEASON」という言葉が入っています。",
      "夏だけでなく、秋も冬も1年中、目の紫外線対策をしようというメッセージです。"),
    p("テレビCMの調光レンズとはちがい、新ビジュアルは透明なレンズのメガネです。",
      "サングラスに抵抗がある人でも、まねしやすいスタイルになっています。"),
    p("背景にはカラフルな建物が写っていて、CMと同じくカナダで撮った写真とみられます。",
      "チェックのシャツに白いTシャツを合わせた、さわやかなコーディネートでした。",
      "シャツのブランドは、今のところ公式には出ていません。"),
    h3("メイキング映像も公開中"),
    yt(YT_MK),
    p("メイキング映像では、カナダでの撮影のうら側や、目黒蓮さんのインタビューが見られます。",
      "アイドルじゃなかったらつきたい仕事や、2030年の目標なども話しています。"),

    related([("【目黒蓮】札幌ライブのブルガリネックレスの値段は？驚愕の金額！", f"{SITE}/meguro-ren-bvlgari-serpenti-viper-necklace-live-487"),
             ("目黒蓮のエル12月号特別版はいつ発売？カナダ撮影の中身！", f"{SITE}/ren-meguro-elle-japon-december-special-105")]),

    listbox("まとめ", ["目黒蓮が11/12のZoff新ビジュアルでかけているメガネは「ZK192001-14E1」",
                    "Zoff公式の特設ページに「広告着用商品」としてのっている",
                    "値段は1万2,100円(税込・セットレンズ込み)",
                    "広告と同じUVクリアレンズにすると1万6,500円〜",
                    "13.8gの軽いボストン型で、色はブラック×ゴールド",
                    "Zoffのオンラインストアと全国のお店で買える"], big=True),
    p("1万円台で目黒蓮さんとおそろいにできるのは、ファンにはうれしいですよね。",
      "透明レンズなら毎日かけられるので、紫外線対策もかねてチェックしてみてください。"),
])

ARTICLES = [
    {"key": "meguro_zoff", "title": "【未】目黒蓮のZoffメガネはどれ？新CMの型番と値段は1万2100円！",
     "slug": "meguro-ren-zoff-glasses-zk192001",
     "categories": [4, 12], "frames": ["product"], "html": body},
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
    with open(os.path.join(REPO, "articles", "snowman_meguro_zoff_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
