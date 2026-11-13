# -*- coding: utf-8 -*-
"""chomoand-0.com(SixTONES) YouTube「【縄跳び検定に挑戦】オレはもっと飛べたはず」(2026-11-13公開)の概要記事HTMLを組み立てる。

usage: python tools/_build_sixtones_nawatobi_1113.py
articles/sixtones_nawatobi_1113.html と articles/sixtones_nawatobi_1113_manifest.json を書き出す。
投稿は tools/_upload_sixtones_nawatobi_1113.py。
根拠は動画本編(フレーム・テロップ)と所沢市「なわとび検定」公式ページ。字幕はIPブロックで取れず、音声はWhisperで確認。
衣装(白T+青ジャージ)は全員おそろいで、私物の型番まで特定できるものは無かったので私物記事は作っていない。
"""
import os, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chomoand-0.com"
ACC, BG, LINE, MK = "#333333", "#f5f5f5", "#d5d5d5", "#d2d3d6"   # neutral -> sixtones_theme.py --per-section
VID = "4Ec-Qzoqj9c"
YT = f"https://www.youtube.com/watch?v={VID}"
TOKO = "https://www.city.tokorozawa.saitama.jp/kosodatekyouiku/kyoiku/sports/nawatobikenntei.html"


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


def yt(url):
    return (f'<!-- wp:embed {{"url":"{url}","type":"video","providerNameSlug":"youtube","responsive":true,'
            f'"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->\n'
            f'<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube '
            f'wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\n{url}\n'
            f"</div></figure>\n<!-- /wp:embed -->\n")


body = "".join([
    p("2026年11月13日、SixTONESの公式YouTubeに「縄跳び検定に挑戦」の回が公開されました。",
      "小学生のころにやった縄跳びに、大人になった6人が本気でいどむ企画です。",
      "結果は、" + mk("森本慎太郎と田中樹の3級が最高") + "でした。"),
    listbox("この記事でわかること", ["縄跳び検定ってどんなルール？",
                              "6人の最終結果は何級？",
                              "メンバーごとの見どころ",
                              "みんながつまずいた技「返し跳び」とは",
                              "おそろいの体操服コーデ"], big=True),

    h2("SixTONES縄跳び検定の結果は？"),
    keybox([("森本慎太郎", "3級"), ("田中樹", "3級"), ("松村北斗", "4級"),
            ("京本大我", "6級"), ("髙地優吾", "6級"), ("ジェシー", "6級")]),
    p("最後に出た結果の表では、慎太郎と樹の2人が3級でトップでした。",
      "北斗は4級、京本・髙地・ジェシーの3人は6級です。"),
    "{{IMG:result}}\n",
    p("2人は2級にも挑戦しましたが、はやぶさ跳びなどがある2級の壁は高かったようです。",
      "最後に「3級ですね」と結果を受けとめる場面で、検定チャレンジは終わりました。"),
    yt(YT),

    h2("縄跳び検定ってどんなルール？"),
    p("使ったのは、埼玉県所沢市の「なわとび検定カード」です。",
      "8級から1級まであり、級が上がるほど技の数がふえて、むずかしくなります。"),
    "{{IMG:title}}\n",
    p("動画の中では、所沢市児童生徒体力向上推進委員会のお手本動画も流れます。",
      "お手本を見たあと、庭のまん中で1人ずつ挑戦するスタイルでした。"),
    table([["級", "おもな技"],
           ["8級", "両足跳び・左右開閉跳び"],
           ["7級", "前後開閉跳びが加わる"],
           ["6級", "あや跳びが加わる"],
           ["5級", "かけ足跳び・返し跳び・交差サイクル"],
           ["4級", "交互2拍子跳び・側振跳び"],
           ["3級", "二重跳び8回・返しかけ足跳び"],
           ["2級", "はやぶさ跳び8回・3拍子跳び"]]),
    p("技は決まった順番で、続けて跳ばないといけません。",
      "とちゅうで止まったり、順番をまちがえたりすると、やり直しです。"),
    p("動画には「お手本と順番がちがうことがあるが、挑戦なので多めに見て激甘判定の場合がある」とスタッフの注意書きも出ていました。",
      f"検定カードと各級の音声は{a(TOKO, '所沢市の公式ページ')}で見られます。"),

    h2("森本慎太郎は3級！2級にも挑戦"),
    p("黒いLAのキャップがトレードマークの慎太郎は、運動神経ばつぐんの1人として期待されていました。",
      "その言葉どおり、どんどん級を上げていきます。"),
    p("3級は、二重跳び8回や側振跳びなど8つの技を続けて跳ぶむずかしい級です。",
      "慎太郎は、これを跳びきって3級に合格しました。"),
    p("最後は2級にも挑戦し、はやぶさ跳びが入る長い演技にいどみました。",
      "2級には届きませんでしたが、樹とならんでトップの結果です。"),

    h2("田中樹は3級を一発クリア"),
    p("オープニングで「小学校の時めっちゃ上手かった」と話していたのが樹です。",
      "8級もトップバッターで、あっさりクリアしました。"),
    p("3級は、テロップで「一発クリア！」と出るほどスムーズでした。",
      "そのまま2級にも挑戦しましたが、最後は地面にたおれこんで大笑いしていました。"),
    p("この回の樹は、ベージュのLAキャップにノースリーブ、腕には金色の時計という姿です。",
      "体操服風の衣装の中でも、自分らしさが出ていました。"),

    h2("松村北斗は4級、返し跳び講座も"),
    p("北斗は、はじめは1人だけ青いジャージの上着まで着た「体操服フル装備」で参加しました。",
      "動きがきれいで、メンバーから「北斗めっちゃ上手い」と声がかかる場面もありました。"),
    p("見どころは、北斗が先生になって開いた「返し跳び講座」です。",
      "第1回・第2回と2回も開かれ、ほかのメンバーに跳び方を教えていました。"),
    p("3級にも挑戦しましたが、テロップは「北斗3級断念」でした。",
      "それでも4級で、慎太郎と樹のすぐ後ろにつけています。"),

    h2("京本大我は1級に飛び級チャレンジ？"),
    p("京本は、いきなり「1級飛び級！」として挑戦する場面から始まりました。",
      "もちろん結果は×で、あらためて8級からのスタートになりました。"),
    p("6級のあや跳びでは、腕のクロスのコツをメンバーに教わりながら練習していました。",
      "「お股の下に手をやるんじゃなくて」とアドバイスされる場面は、思わず笑ってしまいます。"),
    p("最終結果は6級でした。",
      "MCとして検定カードを読み上げる役も、しっかりつとめていました。"),

    h2("髙地優吾は6級、コツをつかみかけた"),
    p("髙地は、5級の返し跳びで苦戦しました。",
      "とちゅうで「コツを掴み始めたこーち」というテロップが出るほど、上達を見せています。"),
    p("ただ、5級は技が5つ以上つづくむずかしい級です。",
      "最後まで通しきれず、結果は6級でした。"),
    p("ラストの集合シーンでは、キャップをかぶって短パン姿になっていました。",
      "夏の撮影らしい、のびのびした雰囲気が伝わってきます。"),

    h2("ジェシーは6級、返し跳びに苦戦"),
    p("ジェシーも5級の返し跳びでつまずいた1人です。",
      "テロップでは「返し跳び≒ガムシャラ！パフォーマンス？」とつっこまれていました。"),
    p("それでも練習を続けるうちに「何か掴んだジェシー」というテロップが出ます。",
      "あと少しのところまで来ていたので、続きが見たくなる展開でした。"),

    h2("みんながつまずいた「返し跳び」とは"),
    p("今回、いちばん多くのメンバーが止まったのが5級の「返し跳び」です。",
      "縄を体の横で1回まわしてから、そのまま前に戻して跳ぶ技です。"),
    p("横でまわす動きと、前で跳ぶ動きを切りかえるのがむずかしいポイントです。",
      "練習中は「縄が勝手に回転してくれるから」と、力を入れすぎないコツも話されていました。"),
    p("動画の説明文には「#はやぶさ」「#返し跳び」のハッシュタグも付いています。",
      "子どもといっしょに挑戦してみるのも楽しそうですね。"),

    h2("おそろいの体操服コーデにも注目"),
    p("6人は、白いTシャツに青いジャージのズボンという、おそろいの体操服風の衣装でした。",
      "まるで小学校の体育の時間のような見た目です。"),
    listbox("メンバーの着こなしのちがい", ["森本慎太郎:黒のLAキャップ",
                                   "田中樹:ベージュのLAキャップ+ノースリーブ+金色の時計",
                                   "松村北斗:はじめは青いジャージの上着まで着用",
                                   "髙地優吾:ラストはキャップ+短パン",
                                   "京本大我・ジェシー:白T+ジャージのシンプルスタイル"]),
    p("おそろいの衣装なので、私物のブランドまで分かるアイテムはほとんどありませんでした。",
      "そのぶん、キャップや袖の長さで、それぞれの個性が見えるのがおもしろいところです。"),

    listbox("まとめ", ["SixTONESが小学生の「縄跳び検定」に本気で挑戦(2026/11/13公開)",
                    "使ったのは所沢市のなわとび検定カード(8級〜1級)",
                    "最高は森本慎太郎・田中樹の3級",
                    "松村北斗は4級、京本大我・髙地優吾・ジェシーは6級",
                    "みんながつまずいたのは5級の「返し跳び」",
                    "北斗の「返し跳び講座」も見どころ"], big=True),
    p("大人が本気で縄跳びをするだけで、こんなに盛り上がるのはSixTONESならではですね。",
      "1級はまだ遠いので、続編でのリベンジにも期待したくなります。"),
])

ARTICLES = [
    {"key": "nawatobi", "title": "【未】SixTONES縄跳び検定の結果は？最高3級は慎太郎と樹！",
     "slug": "sixtones-jump-rope-test-results",
     "categories": [15],
     "images": {
         "result": {"file": "images/sixtones_nawatobi_result.jpg", "alt": "SixTONES縄跳び検定の最終結果 慎太郎3級 樹3級 髙地6級 ジェシー6級 北斗4級 京本6級", "src": YT},
         "title": {"file": "images/sixtones_nawatobi_title.jpg", "alt": "SixTONESの縄跳び検定に挑戦しよう!のタイトル画面", "src": YT},
     },
     "html": body},
]


def main():
    manifest = []
    for art in ARTICLES:
        base = art["title"].replace("【未】", "")
        assert art["title"].startswith("【未】") and len(base) <= 35, (len(base), base)
        print("title len", len(base))
        path = os.path.join("articles", f"sixtones_{art['key']}_1113.html")
        with open(os.path.join(REPO, path), "w", encoding="utf-8") as f:
            f.write(art["html"])
        m = {k: v for k, v in art.items() if k != "html"}
        m["file"] = path.replace("\\", "/")
        manifest.append(m)
        print("wrote", path, len(art["html"]))
    with open(os.path.join(REPO, "articles", "sixtones_nawatobi_1113_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
