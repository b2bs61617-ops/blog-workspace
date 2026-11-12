# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) 2026-11-12放送『素のまんま』(深澤・目黒+渡辺乱入)の
「渡辺翔太 空港置き去り事件(カナダeTA申請)」記事HTMLを組み立てる。

usage: python3 tools/_build_snowman_sunomanma_eta_1112.py
articles/snowman_sunomanma_eta.html と articles/snowman_sunomanma_eta_manifest.json を書き出す。
投稿は tools/_upload_snowman_sunomanma_eta_1112.py。
材料: tools/Xiy/posts_20261112_suno*(X/Threadsのファン聞き書きレポ)。第三者アカウントの埋め込み・画像は使わない。
"""
import os, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chomoand-2.com"
ACC = "#4f8fd0"      # 渡辺翔太のメンバーカラー(青)
BG = "#f1f6fc"
LINE = "#d3e2f3"
MK = "#d1e4f7"
QR = "https://www.joqr.co.jp/qr/program/snow/"
ETA = "https://www.canada.ca/ja/immigration-refugees-citizenship/services/visit-canada/eta.html"
RADIKO = "https://radiko.jp/"


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


def voice(lines):
    """ファンの声(要約)を吹き出し風の枠で並べる。特定アカウントは出さない。"""
    lis = "\n".join(f'<p style="margin:0 0 8px 0;padding:8px 12px;background:#fff;border-radius:12px;border:1px solid {LINE};">{t}</p>' for t in lines)
    return html(f'<div style="padding:12px;margin:0 0 16px 0;background:{BG};border-radius:6px;">\n{lis}\n</div>')


body = "".join([
    p("2026年11月12日(木)の『Snow Manの素のまんま』は、深澤辰哉と目黒蓮の回でした。",
      "途中から渡辺翔太も加わり、3人で話した「空港置き去り事件」がXで大きな話題になっています。"),
    p("結論から言うと、" + mk("カナダに入るための「eTA」という申請を、深澤辰哉と渡辺翔太が2人とも出し忘れていた") + "という話です。",
      "空港でその場で申請し、深澤辰哉は約2分で許可が出ました。",
      "渡辺翔太だけ間に合わず、空港に1人残されてしまったそうです。"),
    listbox("この記事でわかること", ["空港置き去り事件とは？何があった？",
                              "渡辺翔太はどうやってカナダへ行った？",
                              "3人のトークとファンの反応",
                              "そもそもeTAって何？どれくらいで通る？",
                              "目黒蓮が2週連続で出演した理由"], big=True),

    h2("空港置き去り事件とは？何があった？"),
    keybox([("放送", "2026年11月12日(木)21時〜 文化放送『Snow Manの素のまんま』"),
            ("出演", "深澤辰哉・目黒蓮(途中から渡辺翔太)"),
            ("話の中身", "カナダへ行く日に、空港でeTAの申請漏れが分かった"),
            ("結果", "深澤辰哉だけ先に出発、渡辺翔太は1日おくれでカナダへ")]),
    p("深澤辰哉と渡辺翔太は、カナダで撮影中の目黒蓮に会いに行こうとしていました。",
      "ところが空港のチェックインカウンターで、カナダに必要な申請をしていないことが分かったそうです。"),
    p("この話は、札幌公演の初日のMCでも少し話していたそうです。",
      "今回のラジオでは、本人たちの言葉で一番くわしく語られました。"),
    p("※ここで紹介するセリフや流れは、放送を聴いたファンのレポをもとにまとめたものです。",
      "言い回しは実際の放送と少しちがう場合があります。"),

    h3("出発1時間前に申請漏れが発覚"),
    p("2人が空港に着いたのは、出発の1時間〜1時間半ほど前だったようです。",
      "カウンターで申請をしていないと分かり、2人ともその場でスマホから申請しました。"),
    p("深澤辰哉は「やべ！終わった」と思ったそうです。",
      "それでも「挑戦はしなきゃいけない」と、手続きを打ち込み続けたと話していました。"),

    h3("深澤辰哉は約2分で許可、空港スタッフも大喜び"),
    p("深澤辰哉の申請は、" + mk("なんと約2分で許可が出た") + "そうです。",
      "「通りました！」と伝えると、空港のスタッフさんたちも「やったー！」と喜んでくれたといいます。"),
    p("ところが「なべきたぞ！」と横を見ると、渡辺翔太の顔から血の気が引いていたそうです。",
      "渡辺翔太の申請は、なかなか許可が出ませんでした。"),

    h3("「ふっか、先行っててくれ」渡辺翔太が1人残る"),
    p("残り15分、10分、5分と時間がへっても、渡辺翔太の許可は来ません。",
      "深澤辰哉によると、渡辺翔太は目をつぶって、もう悟ったような顔をしていたそうです。"),
    p("そして渡辺翔太は「ふっか、先行っててくれ。後から追いかけるから」と伝えました。",
      "深澤辰哉は渡辺翔太をカウンターに残し、走って飛行機に乗ったそうです。"),

    h2("渡辺翔太はどうやってカナダへ行った？"),
    p("1人残った渡辺翔太は、空港の人に「渡辺さん乗れないので、タクシー乗り場はあちらです」と案内されたそうです。",
      "その日の便は、もうありませんでした。"),
    p("さらに不運なことに、" + mk("家へ帰るタクシーの中で申請の許可が出た") + "そうです。",
      "渡辺翔太は「あの時のタクシーから見た東京の夜景は忘れられない」と話していました。"),
    p("そして次の日の朝いちばんに、もう一度空港へ行ったそうです。",
      "こうして渡辺翔太は、1日おくれでカナダに着きました。"),
    table([["", "深澤辰哉", "渡辺翔太"],
           ["申請の結果", "約2分で許可", "出発に間に合わず"],
           ["その日", "予定の便で出発", "タクシーで帰宅"],
           ["カナダ到着", "予定どおり", "1日おくれ"]]),

    h2("3人のトークとファンの反応"),
    h3("目黒蓮「1人しか来ないの？」"),
    p("カナダで待っていた目黒蓮は、2人で来ると聞いていたそうです。",
      "なので「え、1人しか来ないの？」「しょっぴー空港まで来て帰ったの！？」と驚いたといいます。"),
    p("深澤辰哉は、渡辺翔太に「今ここでこうしてるよ」と様子だけは送っていたそうです。",
      "次の日、渡辺翔太は「不思議な顔」でカナダの空港に現れたと話していました。"),
    p("目黒蓮は「この話もう知ってるのにおもしろすぎる」と、何度も笑っていたそうです。"),

    h3("途中から渡辺翔太が乱入"),
    p("放送の途中で、目黒蓮が「あれっ、渡辺さんじゃないすか！」と声を上げます。",
      "ちょうど渡辺翔太の話をしていたところに、本人が登場したそうです。"),
    p("深澤辰哉が話の流れを話し、ところどころで渡辺翔太が当時の気持ちを話す流れでした。",
      "3人でずっとゲラゲラ笑っていて、聴いている側まで楽しくなる回だったようです。"),

    h3("Xでは「不憫だけどおもしろい」の声"),
    p("放送の後、Xでは空港の話への感想がたくさん投稿されていました。",
      "多かったのは、残された渡辺翔太の顔を想像して笑ってしまう、という声です。"),
    voice(["空港のカウンターに1人残されたしょっぴーを想像したら、不憫すぎておもしろい",
           "帰りのタクシーで申請が通るの、さすが持ってる男",
           "2分で通ったふっかさんもミラクル起こしてておもしろい",
           "自分も申請を忘れて、空港で同じ経験をしたことがある",
           "今年聴いたSnow Manのエピソードでトップ3に入る"]),
    p("「なんで深澤辰哉だけすぐ通ったの？」と不思議に思う声もありました。",
      "ただ、許可が出るまでの時間に差が出た理由は、放送では話されていないようです。"),

    h2("そもそもeTAって何？どれくらいで通る？"),
    p("eTA(イータ)は、" + mk("飛行機でカナダに入る人が出発前に取る「電子渡航認証」") + "です。",
      "日本のパスポートを持つ人も、観光などで飛行機でカナダへ行くなら必要です。"),
    table([["項目", "内容"],
           ["申請方法", "カナダ政府の公式サイトからネットで申請"],
           ["費用", "7カナダドル(約800円前後)"],
           ["許可までの時間", "多くは数分。書類を求められると数日かかることも"],
           ["有効期間", "最長5年(パスポートの期限まで)"]]),
    p("カナダ政府によると、多くの人は申請から数分で許可が出ます。",
      "ただし、追加の確認が必要になると、数日かかることもあると案内されています。"),
    p("つまり、深澤辰哉の「約2分」はよくあるパターンです。",
      "渡辺翔太のように時間がかかるケースもあるので、出発の数日前までに申請しておくと安心です。"),
    p("申請は公式サイトから行えます。",
      f"高い手数料を取る代行サイトもあるので注意しましょう。出典:{a(ETA, 'カナダ政府 eTA公式ページ')}"),

    h2("目黒蓮が2週連続で出演した理由"),
    p("目黒蓮は、海外ドラマ『SHOGUN 将軍』シーズン2の撮影で、長くカナダに行っていました。",
      "前の週の11月5日の放送は、日本に帰ってきてから初めての『素のまんま』でした。"),
    p("11月5日は渡辺翔太の誕生日で、渡辺翔太と目黒蓮の回でした。",
      "そして今週は深澤辰哉との回になり、" + mk("2週連続で目黒蓮の声が聴けた") + "とファンは大喜びでした。"),
    h3("カナダではSnow ManのMVを見せていた"),
    p("今回の放送では、目黒蓮のカナダでの話もたくさん出ました。",
      "目黒蓮は、現地の共演者やスタッフにSnow ManのMVを見せていたそうです。"),
    p("メンバー1人ずつの紹介もしていたと話していたそうです。",
      "ファンからは「Snow Manのメンバーという誇りを持って撮影していたんだね」という声が上がっていました。"),
    h3("最後は目黒蓮の「巻けよ！」"),
    p("3人の話は止まらず、時間が足りなくなるほどでした。",
      "最後には目黒蓮が深澤辰哉に「(時間を)巻けよ！」とツッコミを入れていたそうです。"),
    p("曲は『Secret Touch』がかかり、CMもSnow Manのものばかりだったそうです。",
      "「30分じゃ足りない」「延長してほしい」という声も多く見られました。"),

    h2("素のまんまの聴き方"),
    p("『Snow Manの素のまんま』は、文化放送で毎週木曜21時から30分の番組です。",
      f"放送から1週間は、{a(RADIKO, 'radiko')}のタイムフリーで聴き直せます。"),
    p("地方のラジオ局でも、曜日や時間をずらして放送されています。",
      f"くわしくは{a(QR, '文化放送の番組ページ')}で確認してください。"),
    p("YouTubeなどに出回っている無断アップの音声は、番組の聴取率に入りません。",
      "Snow Manを応援するなら、radikoなどの正しい方法で聴きましょう。"),

    listbox("まとめ", ["空港置き去り事件は、カナダのeTA申請を出し忘れていた話",
                    "深澤辰哉は約2分で許可が出て、予定どおり出発",
                    "渡辺翔太は間に合わず、帰りのタクシーの中で許可が出た",
                    "渡辺翔太は次の日の朝に出発し、1日おくれでカナダへ",
                    "eTAは多くは数分で通るが、数日かかることもある",
                    "目黒蓮はカナダ撮影から帰国し、2週連続の出演だった"], big=True),
    p("血の気が引いたしょっぴーと、2分で通ったふっかの差がおもしろすぎる回でした。",
      "タクシーから見た東京の夜景の話は、何度聴いても笑ってしまいますね。",
      "まだ聴いていない人は、ぜひタイムフリーで3人の笑い声を聴いてみてください。"),
])

ARTICLES = [
    {"key": "sunomanma_eta", "title": "【未】渡辺翔太の空港置き去り事件とは？素のまんまでカナダeTAの真相",
     "slug": "watanabe-shota-airport-eta-sunomanma",
     "categories": [4, 7, 9, 12], "frames": [], "html": body},
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
    with open(os.path.join(REPO, "articles", "snowman_sunomanma_eta_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
