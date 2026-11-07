# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) 岩本照がNACK5「ひかリュウ」(2026-11-07放送)で話したバイク(ドラッグスター)の記事HTMLを組み立てる。

usage: python tools/_build_snowman_iwamoto_bike_dragstar_1107.py
articles/snowman_iwamoto_bike_dragstar_1107.html と _manifest.json を書き出す。
発言はオシリが録音した放送(radikoタイムフリー 10:30〜)をfaster-whisperで文字起こししたもの。
第三者の特定投稿の画像は使わない(番組公式Xポストだけ埋め込む)。
"""
import os, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chomoand-2.com"
ACC = "#b8901c"      # 岩本照のメンバーカラー(黄)
LINE = "#efe1a8"
BG = "#fcf8e8"
MK = "#f5e7a6"
OFFICIAL_X = "https://x.com/iwamoto795/status/2118652112817271220"
NACK5 = "https://www.nack5.co.jp/program/hikaru/"
RADIKO = "https://radiko.jp/share/?sid=NACK5&t=20261107073000"
PRESS = "https://bestcalendar.jp/press/154069"


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


def quote(who, lines):
    body = "<br>\n".join(lines)
    return html(f'<div style="border:1px solid {LINE};border-radius:4px;padding:12px 16px;margin:0 0 16px 0;background:#fff;">\n'
                f'<p style="margin:0 0 6px 0;font-weight:bold;color:{ACC};">{who}</p>\n<p style="margin:0;">{body}</p>\n</div>')


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


def x_embed(url):
    return (f'<!-- wp:embed {{"url":"{url}","type":"rich","providerNameSlug":"twitter","responsive":true}} -->\n'
            '<figure class="wp-block-embed is-type-rich is-provider-twitter wp-block-embed-twitter"><div class="wp-block-embed__wrapper">\n'
            f'{url}\n</div></figure>\n<!-- /wp:embed -->\n')


def src(name, url, date):
    return f'出典:<a href="{url}" target="_blank" rel="noopener">{name}</a>({date})'


SRC_RADIO = src("NACK5「岩本照のロウリュウしてもいいですか？」", RADIKO, "2026年11月7日放送")

body = "".join([
    p("岩本照さんが2026年11月7日、NACK5のラジオ「西武鉄道 presents 岩本照のロウリュウしてもいいですか？」(通称ひかリュウ)で、自分のバイクについて話しました。",
      f"リスナーから「おすすめの中型バイクは？」と聞かれ、{mk('「中型(だと)僕はドラッグスターっていうバイクに乗ってた」')}と答えています。",
      "放送のあと、Xでは「ひかるのバイクはドラッグスター」と話題になりました。",
      "この記事では、岩本照さんがラジオで話したバイクの話をくわしく書き起こし、ドラッグスターがどんなバイクなのかもまとめました。"),
    listbox("この記事でわかること", ["岩本照が中型で乗っていたバイクは、ヤマハのドラッグスター",
                                    "11/7のひかリュウで話したバイクトークの中身",
                                    "ドラッグスターはどんなバイク？400と250のちがい",
                                    "岩本照のおすすめは「教習所のCB」",
                                    "いまは大型や、いろんなタイプのバイクにも乗っている",
                                    "同じ回で話した「トリュフ」のハマりもの"], big=True),

    h2("岩本照がラジオで話したバイクの話"),
    keybox([("番組", "西武鉄道 presents 岩本照のロウリュウしてもいいですか？(NACK5)"),
            ("放送日", "2026年11月7日(土)7:30〜8:00"),
            ("コーナー", "リスナーからのメールを読むコーナー"),
            ("話した内容", "中型ではドラッグスターに乗っていた/おすすめは教習所のCB/いまは大型にも乗る")]),
    x_embed(OFFICIAL_X),
    p("11月7日の放送は、予告では「運動の秋！フルマラソン＆筋トレ話」と「新企画が3つ」がメインでした。",
      "バイクの話が出たのは、番組の後半でリスナーからのメールを読んでいたときです。",
      "予告には書かれていなかったので、聞いていたファンにとってはうれしいサプライズになりました。"),

    h3("リスナーからの質問"),
    p("メールを送ったのは、10月はじめから岩本照さんのファンになったというリスナーさん。",
      "初回の放送で岩本照さんがバイクに乗っていると知り、自分も来年あたりにバイクの免許を取ろうと考えている、という内容でした。"),
    quote("リスナーのメール(要約)", [
        "初回放送でバイクにも乗られていることを知り、すぐに調べていってしまいました。",
        "私も来年あたりバイクの免許を取りに行こうかと思っていて、今一番気になるのがホンダのシャドウ400です。",
        "ヒカルくんのおすすめの中型バイクはありますか？バイクへの愛も聞きたいです。"]),
    p("ホンダのシャドウ400は、ゆったり乗れるアメリカンタイプのバイクです。",
      "同じアメリカンタイプのドラッグスターに乗っていた岩本照さんにとっては、ちょうど話しやすい質問だったのかもしれません。"),

    h3("岩本照の答え「ドラッグスターに乗ってた」"),
    quote("岩本照さん", [
        "中型いいですね。",
        f"{mk('中型(だと)僕はドラッグスターっていうバイクに乗ってたって感じですかね。')}"]),
    p(f"ポイントは、{mk('「乗ってた」と過去形で話している')}ところです。",
      "「中型だと」と前置きしているので、中型免許で乗れるバイクの中ではドラッグスターだった、という意味だと考えられます。",
      "あとで紹介するように、いまは大型のバイクにも乗っていると話していました。",
      SRC_RADIO),

    h2("ドラッグスターってどんなバイク？"),
    table([["項目", "内容"],
           ["メーカー", "ヤマハ発動機"],
           ["タイプ", "アメリカン(クルーザー)"],
           ["エンジン", "空冷のV型2気筒"],
           ["主な排気量", "400(ドラッグスター400)/250(ドラッグスター250)"],
           ["必要な免許", "400・250とも普通二輪免許(中型)で乗れる"],
           ["特徴", "低くて長い車体・足つきのよいシート・メッキパーツの多いクラシックな見た目"],
           ["現在", "国内向けは2017年に生産終了。いまは中古車で探すのが中心"]]),
    p(f"ドラッグスターは、{mk('ヤマハのアメリカンタイプのバイク')}です。",
      "車体が低くて長く、シートの位置も低いので、足がしっかり地面につくのが特徴。",
      "タンクやエンジンまわりにメッキのパーツが多く、いかにも「アメリカンバイク」らしい見た目で人気がありました。"),
    p("エンジンは空冷のV型2気筒で、ドコドコという低い音と、ゆったりとした走りが魅力です。",
      "スピードを出すというより、景色を見ながらのんびり走るのが楽しいタイプのバイクといえます。"),
    p("ハンドルやマフラーなどの交換パーツがたくさん出ていて、カスタムを楽しむ人が多いのもドラッグスターの特徴です。",
      "同じドラッグスターでも、乗る人によってまったくちがう見た目になっていることがよくあります。"),

    h3("400と250、岩本照が乗っていたのはどっち？"),
    p("ドラッグスターには、おもに400ccと250ccのモデルがあります。",
      "どちらも普通二輪免許(いわゆる中型免許)で乗れるので、「中型だと」という話し方だけでは、どちらに乗っていたのかはわかりません。",
      "ラジオでは排気量までは話していませんでした。"),
    p("ちなみに、ドラッグスターには1100ccのモデルもありますが、こちらは大型二輪免許が必要です。",
      "岩本照さんは「中型だと」と話していたので、乗っていたのは400か250のどちらかだと考えられます。",
      "車種や年式など、くわしいことがわかったら追記します。"),

    h2("おすすめは「教習所のCB」"),
    p("リスナーの「おすすめの中型バイクは？」という質問に、岩本照さんは意外な答えを返しています。"),
    quote("岩本照さん", [
        "でもなんかこれ勝手なあれですよ、あくまで僕の一意見としてですけど、",
        "教習所で乗るそのCBっていうバイクあるんですけど、",
        f"教習所のバイクやっぱ一番慣れてるから、{mk('一周回って教習所のバイクが一番乗りやすいんじゃないかな')}っていう。"]),
    p("「CB」は、ホンダのバイクのシリーズ名です。",
      "多くの教習所では、ホンダのCB400 SUPER FOURが中型の教習車として長く使われてきました。",
      "教習所でたくさん練習したバイクなら、乗り方のクセもわかっているので安心、というのが岩本照さんの考えです。"),

    h3("「まずは慣れたバイクから」というアドバイス"),
    p("岩本照さんは、バイクならではの難しさについても話していました。"),
    quote("岩本照さん(要約)", [
        "特にバイクは路上教習がないから、教習所の中で教わったら、いきなり外で実践になる。",
        "怖い部分もあると思うけど、レンタルバイク屋さんもあるから、まずは教習所で慣れているバイクに乗ってみて、",
        "外を走るのに慣れて安定してきたら、ちょっと違うバイクにも挑戦してみるのがいいと思う。"]),
    p(f"車の免許とちがって、バイクの免許には路上教習がありません。",
      f"そのぶん、{mk('免許を取ったあとの最初の1台は「慣れたバイク」で')}、というのはとても現実的なアドバイスです。",
      "「乗りたいバイク」をいきなり買うのではなく、レンタルで試してから選ぶという方法も教えてくれました。",
      "これから免許を取るリスナーさんのことを本気で考えた、岩本照さんらしい答えでした。"),

    h2("いまは大型や、いろんなバイクにも乗っている"),
    quote("岩本照さん", [
        f"僕は{mk('大型乗ったりとか、色んなタイプのバイクに乗ったりする')}ので、",
        "またちょっとバイクの話はまたね、時間ある時にしていこうかななんて思ってます。"]),
    p("話の最後で、岩本照さんはいまは大型のバイクにも乗っていると明かしました。",
      "中型のドラッグスターから始まって、大型免許も取り、いろいろなタイプのバイクに乗っているようです。",
      "どのバイクに乗っているのかまでは話していませんでした。"),
    p(f"「またバイクの話は時間ある時に」と言っていたので、{mk('ひかリュウでバイクトークの続きが聞けそう')}です。",
      "いま乗っている大型バイクの車種がわかったら、この記事に追記します。"),

    h2("同じ回で話した「ハマっているもの」はトリュフ"),
    p("バイクの話の少し前には、「最近ハマっているものは？」というメールにも答えていました。"),
    quote("岩本照さん(要約)", [
        "先日イタリアに行かせていただいたときに、毎回お土産でも買ってくるトリュフ塩とトリュフバターを、",
        "焼いたフランスパンにトリュフバターを塗って、上からトリュフ塩をかけて食べるというのをやったんですけど、",
        f"イタリアとフランスのコラボっていう感じで、{mk('最近ちょっとトリュフ系にはハマってますね')}僕は。"]),
    p("岩本照さんは2026年9月、ドルチェ&ガッバーナのショーに出席するためにミラノを訪れています。",
      "そのときに買ってきたお土産で、フランスパンに合わせて食べているそうです。",
      "パンについては「僕はパンを食べないとやっていけない」とも話していて、毎日の食事に欠かせないようでした。",
      SRC_RADIO),

    h2("「ひかリュウ」ってどんな番組？"),
    keybox([("番組名", "西武鉄道 presents 岩本照のロウリュウしてもいいですか？"),
            ("放送局", "FM NACK5(埼玉)"),
            ("放送時間", "毎週土曜 7:30〜8:00"),
            ("放送開始", "2026年10月3日"),
            ("ハッシュタグ", "#ひかリュウ"),
            ("リスナーの呼び名", "トントゥ")]),
    p(f"「ひかリュウ」は、埼玉県出身の岩本照さんにとって{mk('初めてのソロの冠ラジオ番組')}です。",
      "Snow Manの活動の話や、埼玉の地元情報、趣味の筋トレの話、リスナーからのメールなどを、岩本照さんがひとりで話しています。",
      src("FM NACK5 番組ページ", NACK5, "2026年11月7日確認")),
    p("放送を聞き逃しても、radikoのタイムフリーで放送から1週間は聞き直せます。",
      "11月7日の回は、番組の後半(10分ごろから)でトリュフとバイクの話をしていました。",
      "エリア外で聞くにはradikoプレミアム(有料)が必要です。"),

    h2("ファンの反応"),
    p("放送中から、Xでは「#ひかリュウ」のハッシュタグでバイクの話が広まりました。",
      "「ひかるのバイクトーク嬉しい」「バイク遍歴が知れてありがたい」といった声や、ドラッグスターがどんなバイクなのか調べるファンの投稿が多く見られました。",
      "なかには「ひかるのバイクに遭遇したい」という声もあり、バイクに乗る岩本照さんへの注目の高さがうかがえます。"),

    h2("まとめ"),
    listbox("まとめ", ["岩本照は11/7のひかリュウ(NACK5)で、バイクについて話した",
                      "中型ではヤマハのドラッグスターに乗っていた(400か250かは不明)",
                      "おすすめの中型バイクは「教習所のCB」。一番慣れているから",
                      "いまは大型や、いろいろなタイプのバイクにも乗っている",
                      "「バイクの話はまた時間ある時に」と、続きもありそう",
                      "同じ回で、ミラノ土産のトリュフ塩・トリュフバターにハマっていると話した"], big=True),
    related([("岩本照のチェックコートはどこの？ドルガバのバッグと値段も！", f"{SITE}/?p=587"),
             ("岩本照インスタのドルガバ私服はどれ？カーディガンの値段も！", f"{SITE}/?p=421"),
             ("岩本照の愛称は？ひーくんと照兄の違い！", f"{SITE}/iwamoto-hikaru-nickname-244")]),
])

TITLE = "【未】【ひかリュウ】岩本照のバイクは何？ドラッグスターに乗ってた！"
_base = TITLE.replace("【未】", "")
assert TITLE.startswith("【未】") and len(_base) <= 35, len(_base)

ARTICLES = [
    {"key": "iwamoto_bike_dragstar_1107", "title": TITLE,
     "slug": "hikaru-iwamoto-bike-dragstar-radio",
     "categories": [4, 6], "html": body},
]


def main():
    print("title len", len(_base))
    manifest = []
    for a in ARTICLES:
        path = os.path.join("articles", f"snowman_{a['key']}.html")
        with open(os.path.join(REPO, path), "w", encoding="utf-8") as f:
            f.write(a["html"])
        m = {k: v for k, v in a.items() if k != "html"}
        m["file"] = path
        manifest.append(m)
        print("wrote", path, len(a["html"]))
    with open(os.path.join(REPO, "articles", "snowman_iwamoto_bike_dragstar_1107_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
