# -*- coding: utf-8 -*-
"""KO1KEYZ『2026 KO1KEYZ 1ST FAN MEETING IN SEOUL』公式グッズ事前EC販売(2026-10-16開始)。
一次情報:
- 公式サイト https://ko1keyz.com/news/detail/179 (10/14、ラインナップ・期間・お届け11/3〜・特典・決済)
- 公式X JP 2110298314747040013 / KR 2110298956521689320 (10/14 LINE UP)、開始告知 JP 2111026866731847844 / KR 2111027116762398912
- LAPONE STORE products.json(35商品の価格・サイズ・上限)。10/16 21:46 JSTの売り切れ: うちわKEITO/RYOGA/SHINHAENG/YUKI・トレカ122種・缶バッジ・IDフォトホルダー。TシャツはSのみ掲載
- 公演: news/74(会場・3公演)、news/110(11/8 19:00追加)。配送はshipping-policyで日本の住所・電話番号のみ
きっかけはファンの告知まとめ投稿(本文では触れない)。公式X投稿は埋め込み。グループ記事なのでUI色はウォームグレー。
"""
import requests

import base64, json, os, re, subprocess, sys
from pathlib import Path

import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

AB = "#ddd9d3"
AL = "#8a8378"
BG = "#f7f6f4"
TH = "#ece9e4"



def wp_upload(path, mime):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HEADERS_AUTH, "Content-Type": mime,
                               "Content-Disposition": f'attachment; filename="{path.name}"'},
                      data=path.read_bytes())
    r.raise_for_status()
    return r.json()


def post_draft(title, content, slug, lang, categories, featured_media, summary, translations=None):
    payload = {"title": title, "content": content, "slug": slug, "status": "draft", "lang": lang,
               "categories": categories, "featured_media": featured_media, "author": 2,
               "meta": {"jetpack_publicize_message": summary}}
    if translations:
        payload["translations"] = translations
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts",
                      headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    return r.json()


def make_eyecatch(args, out_path):
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"), *args, "--out", str(out_path)], check=True)
    return wp_upload(out_path, "image/png")["id"]


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def p(t):
    return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"


def mark(t, big=False):
    s = ' style="font-size:1.15em;"' if big else ""
    return f'<strong><span class="swl-marker mark_yellow"{s}>{t}</span></strong>'


def html(block):
    return f"<!-- wp:html -->\n{block}\n<!-- /wp:html -->"


def minibox(rows):
    ps = [f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}</strong>{v}</p>' for i, (k, v) in enumerate(rows)]
    return html(f'<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">\n'
                + "\n".join(ps) + "\n</div>")


def infobox(title, rows, w="32%"):
    trs = "\n".join(f'<tr><td style="background:{TH};border:1px solid {AB};padding:8px 12px;width:{w};">{k}</td>'
                    f'<td style="border:1px solid {AB};padding:8px 12px;">{v}</td></tr>' for k, v in rows)
    return html(f'<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>\n'
                f'<table style="border-collapse:collapse;width:100%;">\n{trs}\n</table>\n</div>')


def barbox(title, items, ordered=False):
    tag = "ol" if ordered else "ul"
    lis = "\n".join(f'<li style="margin:{"0" if i == len(items) - 1 else "0 0 8px 0"};">{it}</li>' for i, it in enumerate(items))
    return html(f'<div style="border:1px solid {AB};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AL};color:#fff;">{title}</p>\n'
                f'<{tag} style="margin:0;padding:14px 18px 14px 34px;background:{BG};">\n{lis}\n</{tag}>\n</div>')


def personbox(name, body):
    return html(f'<div style="border:1px solid {AB};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">\n'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;color:{AL};">{name}</p>\n'
                f'<p style="margin:0;">{body}</p>\n</div>')


def linkbox(title, links):
    lis = "\n".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for u, t in links)
    return html(f'<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">\n'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n'
                f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>')


CHECK = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;'
         f'color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')


def summarybox(items):
    return html(f'<div style="border:2px solid {AL};border-radius:8px;background:{BG};padding:1em 1.25em;margin:0 0 16px 0;">\n<p style="margin:0;">\n'
                + "<br>\n".join(CHECK + it for it in items) + "\n</p>\n</div>")


def note(t):
    return p(f'<span style="font-size:0.9em;color:#666;">{t}</span>')


def tweet(url, lang="ja"):
    return html(f'<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{url}">{url}</a></blockquote>\n'
                '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')




TW_LINEUP = "https://twitter.com/KO1KEYZofficial/status/2110298314747040013"
TW_START = "https://twitter.com/KO1KEYZofficial/status/2111026866731847844"
TW_LINEUP_KR = "https://twitter.com/KO1KEYZofficial/status/2110298956521689320"
TW_START_KR = "https://twitter.com/KO1KEYZofficial/status/2111027116762398912"
STORE = "https://store.lapone.jp/collections/2026-ko1keyz-1stfm-inseoul-ec"
NEWS = "https://ko1keyz.com/news/detail/179"
MAP = ('<iframe src="https://maps.google.com/maps?q=Blue%20Square%20Hannam-dong%20Seoul&t=&z=15&ie=UTF8&iwloc=&output=embed" '
       'width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>')

JP_REL = [
    ("https://chomoand-1.com/ko1keyz-2026-1st-fan-meeting-g-10726", "日本の1STファンミのグッズ・事前EC販売まとめ"),
    ("https://chomoand-1.com/can-i-participate-in-the-ko1ke-11468", "ファンミFCブースでもらえるトレカ・くじの内容"),
    ("https://chomoand-1.com/what-is-oshikatsus-goods-excha-11722", "グッズ交換の「レート」の意味は？"),
    ("https://chomoand-1.com/ko1keyz1st-fan-meeting-tokyo-f-11644", "1STファンミ初日のセトリ・座席表・トロッコ"),
    ("https://chomoand-1.com/ko1keyz-official-app-14275", "KO1KEYZ公式アプリでできること(電子チケット・通知)"),
]
KR_REL = [
    ("https://chomoand-1.com/ko/ko1keyz-2026-1st-fan-meeting-g-kr-10729", "일본 1ST 팬미팅 굿즈・사전 EC 판매 정리"),
    ("https://chomoand-1.com/ko/can-i-participate-in-the-ko1ke-kr-11472", "팬미팅 FC 부스에서 받을 수 있는 포토카드・복권"),
    ("https://chomoand-1.com/ko/what-is-oshikatsus-goods-excha-kr-11725", "굿즈 교환의 '레이트'란?"),
    ("https://chomoand-1.com/ko/ko1keyz1st-fan-meeting-tokyo-f-kr-12762", "1st 팬미 첫날 세트리스트・좌석표・트롤리"),
]
EN_REL = [
    ("https://chomoand-1.com/en/ko1keyz-2026-1st-fan-meeting-g-en-12620", "KO1KEYZ 1ST Fan Meeting (Japan) goods and advance online sales"),
    ("https://chomoand-1.com/en/can-i-participate-in-the-ko1ke-en-12574", "Trading cards and lottery at the fan meeting FC booth"),
    ("https://chomoand-1.com/en/ko1keyz1st-fan-meeting-tokyo-f-en-12764", "1st Fan Meeting Day 1: setlist, seating chart and trolley"),
    ("https://chomoand-1.com/en/ko1keyz-official-app-en-14277", "KO1KEYZ official app: features and e-tickets"),
]


def wptable(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout">'
            f"<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></figure>\n<!-- /wp:table -->")


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->'


def a(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'


# ============================== JP ==============================
JP_TITLE = "KO1KEYZソウルファンミのグッズは？事前EC販売の値段と特典！"
JP_SLUG = "ko1keyz-seoul-fanmeeting-goods-presale"

JP_CONTENT = "\n\n".join([
    p("11月にソウルで開かれるKO1KEYZ(コイキーズ)初の韓国ファンミーティングに向けて、公式グッズの販売が始まりました。<br>\n"
      f"『2026 KO1KEYZ 1ST FAN MEETING IN SEOUL』のグッズは、{mark('LAPONE STOREで2026年10月16日(金)18:30〜10月18日(日)23:59まで事前EC販売', True)}されています。<br>\n"
      f"ソウル公演の新作は{mark('トレーディングカード(1,100円)・ジャガードマフラータオル(2,500円)・RANDOM TOY(550円)の3種類')}で、夏の日本ファンミのグッズも同じページで買えます。<br>\n"
      "さらに7,000円(税込)買うごとに、ソウル公演限定のソロトレカが先着で1枚もらえます。<br>\n"
      "この記事では、グッズの値段と中身、購入特典をもらうための組み合わせ、売り切れの状況、届く日や支払い方法までまとめました。"),
    infobox("ソウルファンミ グッズ事前EC販売の基本情報", [
        ("公演名", "2026 KO1KEYZ 1ST FAN MEETING IN SEOUL"),
        ("公演日", "2026年11月7日(土)14:00・19:00、11月8日(日)14:00・19:00の全4公演"),
        ("会場", "BLUESQUARE WOORI WON BANKING HALL(韓国・ソウル)"),
        ("受付期間", "2026年10月16日(金)18:30〜10月18日(日)23:59"),
        ("販売サイト", a(STORE, "LAPONE STORE")),
        ("お届け予定", "11月3日(火・祝)から順次(公演前に届く予定)"),
        ("購入特典", "7,000円(税込)ごとにソウル公演トレカ1枚(ランダム/ソロ12種)を先着でプレゼント"),
    ]),
    barbox("この記事でわかること", [
        "ソウル公演の新作グッズと値段",
        "日本ファンミのグッズも買える？",
        "購入特典のトレカと7,000円の組み合わせ",
        "売り切れているグッズ",
        "販売期間・届く日・支払い方法",
        "韓国から買える？",
        "ソウルファンミの日程と会場",
    ]),

    h2("KO1KEYZソウルファンミの新作グッズと値段は？"),
    minibox([("新作：", "トレーディングカード・ジャガードマフラータオル・RANDOM TOYの3種類"),
             ("値段：", "550円〜2,500円")]),
    p("ソウル公演のグッズラインナップは、10月14日にKO1KEYZ公式サイトと公式Xで公開されました。<br>\n"
      "告知画像はパステルの水色に黄色のロゴという配色で、日本ファンミの青系デザインとはがらりと雰囲気が変わっています。"),
    tweet(TW_LINEUP),
    p("ソウル公演のために新しく作られたグッズは、次の3種類です。"),
    wptable(["グッズ", "値段(税込)", "中身・サイズ", "1会計の上限"], [
        ["トレーディングカード", "1,100円", "3枚セットランダム/全64種、約55×90mm", "50点まで"],
        ["ジャガードマフラータオル", "2,500円", "約1,100×200mm、綿100%", "上限の記載なし"],
        ["RANDOM TOY", "550円", "4種類のうちどれか1点(全48種)", "20点まで"],
    ]),
    p(f"トレーディングカードは{mark('全64種')}と、日本ファンミのトレカ(全122種)の約半分の種類数です。<br>\n"
      "公式の画像を見ると、日本ファンミのデニム衣装とは違う、白や水色を基調にした新しい撮りおろしのカットが使われています。<br>\n"
      "ジャガードマフラータオルは水色の地に黄色の「KO1KEYZ」ロゴを織り込んだデザインで、端にはハートのマークもあしらわれています。<br>\n"
      "織り柄なので、プリントのタオルより色落ちしにくいのがうれしいポイントです。"),
    h3("RANDOM TOYの中身は？4種類48パターン"),
    p(f"いちばん気になるのが、{mark('1回550円のRANDOM TOY', True)}でしょう。<br>\n"
      "中身は次の4種類のうちどれか1点で、それぞれメンバー12人分あるので、全部で48パターンになります。"),
    wptable(["種類", "サイズ・素材", "ポイント"], [
        ["顔面アクリルキーホルダー", "約35×44mm以内・アクリル", "顔の形に切り抜いたキーホルダー。つなげて使える"],
        ["ミニセルカアクリルキーホルダー", "約44×58mm・アクリル", "メンバーカラーのフレームに自撮り風の写真"],
        ["ネームプレート", "約60×25mm・アクリル", "メンバー本人がハングルで書いた名前入り"],
        ["ステッカー4枚セット", "約60×60mm以内・紙", "メンバー本人が描いたイラスト入り"],
    ]),
    p("ネームプレートには「Name lettering by KO1KEYZ」、ステッカーには「Illustrated by KO1KEYZ」と書かれていて、どちらもメンバーの手書きがそのままグッズになっています。<br>\n"
      "ネームプレートは「다이키(ダイキ)」「잇사(イッサ)」のようにハングルで名前が書かれているので、韓国公演らしさがいちばん出ているアイテムかもしれません。<br>\n"
      "なお、RANDOM TOYはカプセルではなく、中が見えないアルミの袋に入って届きます。<br>\n"
      "会場で売られるものも同じ袋入りと案内されているので、開けるまで何が出るか分からないドキドキ感は通販でも会場でも変わりません。"),

    h2("日本ファンミのグッズも買える？"),
    minibox([("再販：", "8月の『2026 KO1KEYZ 1ST FAN MEETING』のグッズ10種類"),
             ("注意：", "Tシャツ(ロゴ入り)はSサイズのみ")]),
    p(f"今回の販売ページには、ソウル公演の新作だけでなく、{mark('8月に東京・兵庫で開かれた『2026 KO1KEYZ 1ST FAN MEETING』のグッズ')}も並んでいます。<br>\n"
      "夏のファンミで買い逃したグッズがある方にとっては、もう一度手に入れるチャンスです。"),
    wptable(["グッズ", "値段(税込)", "1会計の上限"], [
        ["BIGうちわ(全12種)", "1,100円", "各メンバー1点まで"],
        ["アクリルスタンド(全12種)", "1,100円", "各メンバー1点まで"],
        ["トレーディングカード(3枚セットランダム/全122種)", "1,100円", "50点まで"],
        ["缶バッジ(ランダム/全24種)", "500円", "上限の記載なし"],
        ["トラックTシャツ(SHORT/M/L)", "5,500円", "サイズ問わず2点まで"],
        ["Tシャツ(Sのみ)", "5,500円", "2点まで"],
        ["プレートライト(ライトイエロー)", "2,300円", "1点まで"],
        ["ミニハンディファン", "3,300円", "上限の記載なし"],
        ["ジェリートートバッグ", "5,500円", "上限の記載なし"],
        ["IDフォトホルダー(IDフォト全12種付き)", "2,500円", "上限の記載なし"],
    ]),
    p("夏の事前EC販売のときはTシャツがS/M/Lの3サイズでしたが、今回の販売ページにあるのはSサイズだけです。<br>\n"
      "ミニハンディファンはUSB Type-Cで充電する3段階の風量切り替えタイプで、11月の韓国では出番が少なそうですが、ライブ中の熱気対策に使う人もいそうです。<br>\n"
      f"夏のファンミのグッズがどんな内容だったかは、{a('https://chomoand-1.com/ko1keyz-2026-1st-fan-meeting-g-10726', '日本の1STファンミのグッズ・事前EC販売まとめ')}でくわしく紹介しています。"),

    h2("購入特典のトレカは？7,000円ごとに1枚"),
    minibox([("特典：", "ソウル公演トレーディングカード1枚(ランダム/ソロ12種)"),
             ("条件：", "1回の会計で7,000円(税込)ごと・先着")]),
    p(f"事前EC販売でグッズを{mark('7,000円(税込)買うごとに、ソウル公演のトレーディングカードが1枚', True)}もらえます。<br>\n"
      "特典のトレカはメンバー12人のソロカット12種類からランダムで、会場で配られるものと同じ絵柄です。<br>\n"
      "日本ファンミのグッズも対象に入るので、うちわやアクスタと組み合わせて7,000円を目指せます。"),
    p("ただし、7,000円に送料や手数料はふくまれません。<br>\n"
      "何回かに分けて買った金額を合わせることもできないので、特典を狙うなら1回の会計でまとめて買う必要があります。<br>\n"
      "14,000円なら2枚、21,000円なら3枚と、7,000円ごとに1枚ずつ増える仕組みです。<br>\n"
      "予定の数がなくなった時点で特典は終わるため、早めに注文したほうが安心でしょう。"),
    barbox("7,000円をこえる組み合わせの例", [
        "トレカ(64種)×7=7,700円",
        "RANDOM TOY×13=7,150円",
        "Tシャツ1枚+トレカ1個+RANDOM TOY1個=7,150円",
        "推しのうちわ+アクスタ+マフラータオル+トレカ2個+RANDOM TOY1個=7,450円",
    ]),
    p("ちょうど7,000円にぴったり合う組み合わせは作りにくいので、550円のRANDOM TOYで金額を調整するのが手軽です。<br>\n"
      "7,000円に少し届かないときは、RANDOM TOYを1つ足すと条件を満たせることが多いですよ。"),

    h2("売り切れているグッズはある？"),
    minibox([("売り切れ表示(10/16 21:45時点)：", "日本ファンミのBIGうちわ4人分・トレカ(122種)・缶バッジ・IDフォトホルダー")]),
    p("販売が始まった10月16日の夜(21時45分ごろ)に販売ページを確認したところ、日本ファンミのグッズの一部がすでに売り切れになっていました。"),
    barbox("売り切れ表示になっていたグッズ", [
        "BIGうちわ(KEITO・RYOGA・SHINHAENG・YUKI)",
        "トレーディングカード(3枚セットランダム/全122種)",
        "缶バッジ(ランダム/全24種)",
        "IDフォトホルダー",
    ]),
    p(f"一方で、{mark('ソウル公演の新作3種類と、アクリルスタンド12人分はこの時点ではすべて買える状態')}でした。<br>\n"
      "夏のファンミの在庫を出しているぶん、日本ファンミのグッズは数が少なめなのかもしれません。<br>\n"
      "公式の案内には「販売期間中、在庫が戻る場合もございます」とあるので、売り切れのグッズも期間中にときどきのぞいてみる価値はあります。"),

    h2("販売期間・届く日・支払い方法は？"),
    minibox([("販売期間：", "10月16日(金)18:30〜10月18日(日)23:59"), ("お届け：", "11月3日(火・祝)から順次")]),
    p(f"受付は{mark('10月18日(日)23:59まで', True)}の3日間だけです。<br>\n"
      "販売サイトはLAPONE STOREのみで、KO1KEYZ OFFICIAL STOREでの取り扱いは案内されていません。<br>\n"
      "商品は11月3日(火・祝)から順次届く予定で、11月7日のソウル公演の前に手元にそろう見込みです。<br>\n"
      "ただし、発送は注文した順番ではなく、注文の内容や届け先の地域によって前後します。"),
    tweet(TW_START),
    infobox("使える支払い方法", [
        ("クレジットカード", "Visa、Mastercard、American Express、JCB、ダイナースクラブカード、Discover"),
        ("スマホ決済", "PayPay、au PAY、楽天ペイ、d払い、メルペイ"),
        ("コンビニ払い(前払い)", "デイリーヤマザキ、ファミリーマート、ローソン、ミニストップ、セイコーマート"),
        ("後払い", "Paidyあと払い"),
    ]),
    p("コンビニ払いは前払いで、注文してから3日以内にお金を払わないと注文が自動でキャンセルされます。<br>\n"
      "受付最終日の10月18日に注文した場合でも、期限は注文日から3日以内なので、忘れないうちに支払いを済ませておきましょう。"),
    h3("ほかの商品と一緒にカートに入れると決済できない"),
    p(f"気をつけたいのが、{mark('ソウル公演・日本ファンミのグッズと、それ以外の商品を同じカートに入れると決済できない')}点です。<br>\n"
      "LAPONE STOREでほかのアーティストのグッズやCDなども一緒に買おうとすると、手続きが先に進みません。<br>\n"
      "ソウル公演と日本ファンミのグッズ同士なら一緒に買えるので、今回のグッズだけでカートをまとめてください。<br>\n"
      "期間中は何度でも注文できますが、会計ごとに送料がかかる点もおさえておきたいところです。"),

    h2("韓国から買える？海外配送は？"),
    minibox([("配送先：", "日本国内のみ(日本の住所・電話番号が必要)")]),
    p("LAPONE STOREの配送ポリシーでは、届け先の住所は日本語で、電話番号は日本で使えるものを登録するよう決められています。<br>\n"
      f"海外の電話番号は届け先として使えないため、{mark('今回の事前EC販売は実質的に日本国内に住んでいる人向け')}です。<br>\n"
      "ソウル公演に日本から遠征する方は、出発前の11月3日以降に自宅で受け取れる計算になります。<br>\n"
      "特典のトレカが「会場販売の絵柄と同じ」とされていることから、会場でもグッズが売られる予定とみられ、韓国に住んでいる方はそちらが中心になりそうです。"),

    h2("ソウルファンミの日程と会場は？"),
    minibox([("日程：", "11月7日(土)・8日(日)の全4公演"), ("会場：", "BLUESQUARE WOORI WON BANKING HALL")]),
    p("『2026 KO1KEYZ 1ST FAN MEETING IN SEOUL』は、KO1KEYZにとって初めての韓国でのファンミーティングです。<br>\n"
      f"最初は3公演の予定でしたが、9月に{mark('11月8日(日)19:00の追加公演')}が決まり、全4公演になりました。"),
    wptable(["日にち", "開演"], [
        ["11月7日(土)", "14:00"],
        ["11月7日(土)", "19:00"],
        ["11月8日(日)", "14:00"],
        ["11月8日(日)", "19:00(追加公演)"],
    ]),
    p("会場のBLUESQUARE WOORI WON BANKING HALLは、ソウル・龍山区の漢南洞にある複合文化施設「BLUESQUARE」の中のホールです。<br>\n"
      "地下鉄6号線の漢江鎮駅からすぐの場所にあり、K-POPのコンサートやミュージカルでよく使われています。<br>\n"
      "10月7日に日本と韓国で同時デビューしたばかりのKO1KEYZにとって、韓国のファンと直接会える大事なステージになりますね。"),
    html(MAP),
    note("※2026年10月16日時点の情報です。在庫・販売内容は変わる場合があるので、最新の情報はKO1KEYZ公式サイト・LAPONE STOREでご確認ください。"),

    h2("まとめ"),
    summarybox([
        "ソウルファンミのグッズはLAPONE STOREで10/16(金)18:30〜10/18(日)23:59に事前EC販売",
        "新作はトレカ(1,100円)・マフラータオル(2,500円)・RANDOM TOY(550円)の3種類",
        "日本ファンミのうちわ・アクスタ・Tシャツなども一緒に買える",
        "7,000円(税込)ごとにソウル公演のソロトレカ1枚が先着でもらえる",
        "日本ファンミのうちわ4人分・トレカ・缶バッジ・IDフォトホルダーは10/16夜の時点で売り切れ表示",
        "お届けは11/3(火・祝)から順次で、配送は日本国内のみ",
    ]),
    p("RANDOM TOYのネームプレートやステッカーは、メンバーの手書きが入ったソウル公演ならではのグッズです。<br>\n"
      "受付は10月18日(日)23:59までなので、気になるグッズがある方は早めにカートに入れておきましょう！"),
    linkbox("KO1KEYZの関連記事", JP_REL),
])

JP_SUMMARY = ("コイキーズ(KO1KEYZ)初のソウルファンミのグッズがLAPONE STOREで事前EC販売中！新作はトレカ・マフラータオル・RANDOM TOYの3種類で、7,000円ごとにソロトレカの特典も。受付は10/18(日)23:59まで。")

# ============================== KR ==============================
KR_TITLE = "KO1KEYZ 서울 팬미팅 굿즈는? 사전 EC 판매 가격과 특전!"
KR_SLUG = f"{JP_SLUG}-kr"

KR_CONTENT = "\n\n".join([
    p("11월 서울에서 열리는 KO1KEYZ(코이키즈)의 첫 한국 팬미팅을 앞두고 공식 굿즈 판매가 시작됐습니다.<br>\n"
      f"『2026 KO1KEYZ 1ST FAN MEETING IN SEOUL』 굿즈는 {mark('LAPONE STORE에서 2026년 10월 16일(금) 18:30~10월 18일(일) 23:59(일본 시간)까지 사전 EC 판매', True)} 중이에요.<br>\n"
      f"서울 공연 신상품은 {mark('트레이딩 카드(1,100엔)・자카드 머플러 타월(2,500엔)・RANDOM TOY(550엔) 3종')}이고, 여름 일본 팬미팅 굿즈도 같은 페이지에서 살 수 있습니다.<br>\n"
      "다만 LAPONE STORE는 일본 국내 배송만 가능하다는 점에 주의해야 해요.<br>\n"
      "이 글에서는 굿즈 가격과 구성, 구매 특전, 품절 상황, 배송과 결제 방법까지 정리했습니다."),
    infobox("서울 팬미팅 굿즈 사전 EC 판매 기본 정보", [
        ("공연명", "2026 KO1KEYZ 1ST FAN MEETING IN SEOUL"),
        ("공연일", "2026년 11월 7일(토) 14:00・19:00, 11월 8일(일) 14:00・19:00 총 4회"),
        ("공연장", "블루스퀘어 우리WON뱅킹홀"),
        ("접수 기간", "2026년 10월 16일(금) 18:30~10월 18일(일) 23:59(일본 시간)"),
        ("판매처", a(STORE, "LAPONE STORE")),
        ("배송 예정", "11월 3일(화)부터 순차 배송(일본 국내만)"),
        ("구매 특전", "7,000엔(세금 포함)마다 서울 공연 트레이딩 카드 1장(랜덤/솔로 12종) 선착순 증정"),
    ]),
    barbox("이 글에서 알 수 있는 것", [
        "서울 공연 신상품 굿즈와 가격",
        "일본 팬미팅 굿즈도 살 수 있을까?",
        "구매 특전 트레이딩 카드",
        "품절된 굿즈",
        "판매 기간・배송・결제 방법",
        "한국에서도 살 수 있을까?",
    ]),
    h2("KO1KEYZ 서울 팬미팅 신상품 굿즈와 가격은?"),
    minibox([("신상품: ", "트레이딩 카드・자카드 머플러 타월・RANDOM TOY 3종"), ("가격: ", "550엔~2,500엔")]),
    p("서울 공연 굿즈 라인업은 10월 14일 KO1KEYZ 공식 사이트와 공식 X에서 공개됐어요.<br>\n"
      "파스텔 하늘색에 노란 로고를 더한 디자인으로, 일본 팬미팅의 파란 계열 디자인과는 분위기가 꽤 다릅니다."),
    tweet(TW_LINEUP_KR, "ko"),
    wptable(["굿즈", "가격(세금 포함)", "구성・사이즈", "1회 결제 한도"], [
        ["트레이딩 카드", "1,100엔", "3장 세트 랜덤/총 64종, 약 55×90mm", "50개까지"],
        ["자카드 머플러 타월", "2,500엔", "약 1,100×200mm, 면 100%", "기재 없음"],
        ["RANDOM TOY", "550엔", "4종류 중 1개(총 48종)", "20개까지"],
    ]),
    p(f"트레이딩 카드는 {mark('총 64종')}으로, 일본 팬미팅 트레카(총 122종)의 절반 정도예요.<br>\n"
      "공식 이미지를 보면 일본 팬미팅의 데님 의상과는 다른, 흰색과 하늘색 위주의 새로운 컷이 사용됐습니다.<br>\n"
      "머플러 타월은 하늘색 바탕에 노란 'KO1KEYZ' 로고를 직조한 디자인이에요."),
    h3("RANDOM TOY 구성은? 4종류 48가지"),
    wptable(["종류", "사이즈・소재", "포인트"], [
        ["얼굴 아크릴 키홀더", "약 35×44mm 이내・아크릴", "얼굴 모양으로 자른 키홀더, 연결해서 사용 가능"],
        ["미니 셀카 아크릴 키홀더", "약 44×58mm・아크릴", "멤버 컬러 프레임에 셀카풍 사진"],
        ["네임 플레이트", "약 60×25mm・아크릴", "멤버가 직접 한글로 쓴 이름"],
        ["스티커 4장 세트", "약 60×60mm 이내・종이", "멤버가 직접 그린 일러스트"],
    ]),
    p("네임 플레이트에는 'Name lettering by KO1KEYZ', 스티커에는 'Illustrated by KO1KEYZ'라고 적혀 있어 멤버들의 손글씨와 그림이 그대로 굿즈가 됐어요.<br>\n"
      "RANDOM TOY는 캡슐이 아니라 속이 보이지 않는 알루미늄 봉투에 담겨 배송됩니다."),
    h2("일본 팬미팅 굿즈도 살 수 있을까?"),
    minibox([("재판매: ", "8월 『2026 KO1KEYZ 1ST FAN MEETING』 굿즈"), ("주의: ", "로고 티셔츠는 S 사이즈만")]),
    p("이번 판매 페이지에는 8월 도쿄・효고에서 열린 일본 팬미팅 굿즈도 함께 올라와 있어요.<br>\n"
      "BIG 부채・아크릴 스탠드(각 1,100엔), 트레이딩 카드(1,100엔), 캔뱃지(500엔), 트랙 티셔츠・티셔츠(각 5,500엔), 플레이트 라이트(2,300엔), 미니 핸디 선풍기(3,300엔), 젤리 토트백(5,500엔), ID 포토 홀더(2,500엔) 등입니다."),
    h2("구매 특전 트레이딩 카드는?"),
    minibox([("특전: ", "서울 공연 트레이딩 카드 1장(랜덤/솔로 12종)"), ("조건: ", "1회 결제 7,000엔(세금 포함)마다・선착순")]),
    p(f"사전 EC 판매에서 {mark('7,000엔(세금 포함)마다 서울 공연 트레이딩 카드 1장', True)}을 받을 수 있어요.<br>\n"
      "특전 카드는 멤버 12명의 솔로 컷 12종 중 랜덤이며, 공연장에서 받는 것과 같은 디자인입니다.<br>\n"
      "배송료・수수료는 포함되지 않고, 여러 번 나눠 산 금액은 합산되지 않아요.<br>\n"
      "550엔짜리 RANDOM TOY로 금액을 맞추면 편합니다(예: 티셔츠+트레카+RANDOM TOY=7,150엔)."),
    h2("품절된 굿즈는?"),
    minibox([("품절 표시(10/16 21:45 일본 시간 기준): ", "일본 팬미팅 BIG 부채 4명분・트레카(122종)・캔뱃지・ID 포토 홀더")]),
    p("판매 첫날 밤에 확인해 보니, 일본 팬미팅 굿즈 일부가 이미 품절 상태였어요.<br>\n"
      "BIG 부채(KEITO・RYOGA・SHINHAENG・YUKI), 트레이딩 카드(총 122종), 캔뱃지, ID 포토 홀더가 품절 표시였습니다.<br>\n"
      "서울 공연 신상품 3종과 아크릴 스탠드 12명분은 이 시점에 모두 구매 가능했어요.<br>\n"
      "판매 기간 중 재고가 다시 들어올 수도 있다고 안내되어 있습니다."),
    h2("판매 기간・배송・결제 방법은?"),
    minibox([("판매 기간: ", "10월 16일(금) 18:30~10월 18일(일) 23:59(일본 시간)"), ("배송: ", "11월 3일(화)부터 순차")]),
    p("판매처는 LAPONE STORE뿐이며, 상품은 11월 3일부터 순차 배송되어 서울 공연 전에 도착할 예정이에요.<br>\n"
      "결제는 신용카드, 일본 스마트폰 결제(PayPay 등), 일본 편의점 결제(선불), Paidy 후불을 쓸 수 있습니다.<br>\n"
      f"또 {mark('서울・일본 팬미팅 굿즈와 다른 상품을 같은 장바구니에 넣으면 결제가 안 된다')}는 점도 주의하세요."),
    tweet(TW_START_KR, "ko"),
    h2("한국에서도 살 수 있을까? 해외 배송은?"),
    minibox([("배송지: ", "일본 국내만(일본 주소・전화번호 필요)")]),
    p(f"LAPONE STORE 배송 정책상 주소는 일본어로, 전화번호는 일본에서 쓸 수 있는 번호를 등록해야 해요.<br>\n"
      f"해외 전화번호는 배송 정보로 쓸 수 없기 때문에 {mark('이번 사전 EC 판매는 사실상 일본 거주자 대상')}입니다.<br>\n"
      "특전 카드가 '공연장 판매와 같은 디자인'이라고 안내된 만큼 공연장에서도 굿즈 판매가 있을 것으로 보여, 한국에 사는 팬은 현장 판매가 중심이 될 것 같아요."),
    h2("서울 팬미팅 일정과 공연장은?"),
    minibox([("일정: ", "11월 7일(토)・8일(일) 총 4회"), ("공연장: ", "블루스퀘어 우리WON뱅킹홀")]),
    p("처음에는 3회 공연이었지만, 9월에 11월 8일(일) 19:00 추가 공연이 결정되어 총 4회가 됐어요.<br>\n"
      "공연장인 블루스퀘어 우리WON뱅킹홀은 서울 용산구 한남동에 있으며, 지하철 6호선 한강진역 바로 앞입니다.<br>\n"
      "10월 7일 한일 동시 데뷔한 KO1KEYZ에게 한국 팬들과 직접 만나는 소중한 무대가 되겠네요."),
    html(MAP),
    note("※2026년 10월 16일 기준 정보입니다. 최신 정보는 KO1KEYZ 공식 사이트와 LAPONE STORE에서 확인해 주세요."),
    h2("정리"),
    summarybox([
        "서울 팬미팅 굿즈는 LAPONE STORE에서 10/16(금) 18:30~10/18(일) 23:59 사전 EC 판매",
        "신상품은 트레카(1,100엔)・머플러 타월(2,500엔)・RANDOM TOY(550엔) 3종",
        "일본 팬미팅 부채・아크릴 스탠드・티셔츠 등도 함께 구매 가능",
        "7,000엔마다 서울 공연 솔로 트레카 1장 선착순 증정",
        "배송은 11/3부터, 일본 국내만 가능",
    ]),
    p("멤버들의 손글씨가 들어간 네임 플레이트와 스티커는 서울 공연만의 굿즈예요.<br>\n"
      "11월 공연이 정말 기다려지네요!"),
    linkbox("KO1KEYZ 관련 글", KR_REL),
])

KR_SUMMARY = ("코이키즈(KO1KEYZ) 첫 서울 팬미팅 굿즈가 LAPONE STORE에서 사전 EC 판매 중! 신상품은 트레카・머플러 타월・RANDOM TOY 3종, 7,000엔마다 솔로 트레카 특전도. 일본 국내 배송만 가능해요.")

# ============================== EN ==============================
EN_TITLE = "KO1KEYZ Seoul Fan Meeting Goods: Prices, Pre-Order Dates and Bonus"
EN_SLUG = f"{JP_SLUG}-en"

EN_CONTENT = "\n\n".join([
    p("Official goods are now on sale ahead of KO1KEYZ's first fan meeting in Korea, coming to Seoul in November.<br>\n"
      f"Goods for \"2026 KO1KEYZ 1ST FAN MEETING IN SEOUL\" are {mark('available for pre-order on LAPONE STORE from 18:30 on Friday, October 16 to 23:59 on Sunday, October 18, 2026 (Japan time)', True)}.<br>\n"
      f"The new Seoul items are {mark('trading cards (1,100 yen), a jacquard muffler towel (2,500 yen) and RANDOM TOY (550 yen)')}, and goods from the summer fan meetings in Japan are on the same page.<br>\n"
      "Note that LAPONE STORE only ships within Japan.<br>\n"
      "This article covers prices, what's inside each item, the purchase bonus, sold-out items, delivery and payment."),
    infobox("Seoul fan meeting goods pre-order at a glance", [
        ("Event", "2026 KO1KEYZ 1ST FAN MEETING IN SEOUL"),
        ("Dates", "Nov 7 (Sat) 14:00 & 19:00, Nov 8 (Sun) 14:00 & 19:00 (4 shows)"),
        ("Venue", "BLUESQUARE WOORI WON BANKING HALL, Seoul"),
        ("Order period", "Oct 16 (Fri) 18:30 to Oct 18 (Sun) 23:59, 2026 (JST)"),
        ("Store", a(STORE, "LAPONE STORE")),
        ("Delivery", "From Nov 3, before the shows (Japan addresses only)"),
        ("Bonus", "1 Seoul trading card (random, 12 solo designs) per 7,000 yen spent, while supplies last"),
    ], w="30%"),
    barbox("In this article", [
        "New Seoul goods and prices",
        "Can you buy the Japan fan meeting goods too?",
        "The purchase bonus card",
        "Sold-out items",
        "Order period, delivery and payment",
        "Can you order from outside Japan?",
    ]),
    h2("What are the new KO1KEYZ Seoul fan meeting goods?"),
    minibox([("New items: ", "Trading cards, jacquard muffler towel, RANDOM TOY"), ("Prices: ", "550 to 2,500 yen")]),
    p("The Seoul goods lineup was revealed on October 14 on KO1KEYZ's official site and X account.<br>\n"
      "The pastel sky blue and yellow design feels very different from the blue tones of the Japan fan meetings."),
    tweet(TW_LINEUP, "en"),
    wptable(["Item", "Price (tax incl.)", "Details", "Limit per order"], [
        ["Trading cards", "1,100 yen", "Random 3-card pack, 64 designs, approx. 55x90mm", "50"],
        ["Jacquard muffler towel", "2,500 yen", "Approx. 1,100x200mm, 100% cotton", "Not stated"],
        ["RANDOM TOY", "550 yen", "1 of 4 item types (48 designs)", "20"],
    ]),
    p(f"The trading cards come in {mark('64 designs')}, about half the 122 of the Japan fan meeting set, and use new white and sky blue photos rather than the denim outfits from the summer.<br>\n"
      "The muffler towel has a yellow KO1KEYZ logo woven into a sky blue base."),
    h3("What's inside RANDOM TOY?"),
    wptable(["Type", "Size / material", "Highlight"], [
        ["Face acrylic keychain", "Up to approx. 35x44mm, acrylic", "Face-shaped cutout that can be linked together"],
        ["Mini selfie acrylic keychain", "Approx. 44x58mm, acrylic", "Selfie-style photo in a member-color frame"],
        ["Name plate", "Approx. 60x25mm, acrylic", "Name handwritten in Korean by the member"],
        ["4-sticker set", "Up to approx. 60x60mm, paper", "Illustrations drawn by the members"],
    ]),
    p("The name plates are marked \"Name lettering by KO1KEYZ\" and the stickers \"Illustrated by KO1KEYZ\", so the members' own handwriting and drawings became the goods.<br>\n"
      "RANDOM TOY ships in an opaque aluminum bag, not a capsule."),
    h2("Can you buy the Japan fan meeting goods too?"),
    minibox([("Restock: ", "Goods from the August \"2026 KO1KEYZ 1ST FAN MEETING\""), ("Note: ", "The logo T-shirt is size S only")]),
    p("The sale page also includes goods from the fan meetings held in Tokyo and Hyogo in August: big uchiwa fans and acrylic stands (1,100 yen each), trading cards (1,100 yen), badges (500 yen), track T-shirt and T-shirt (5,500 yen each), plate light (2,300 yen), mini handy fan (3,300 yen), jelly tote bag (5,500 yen) and ID photo holder (2,500 yen)."),
    h2("What is the purchase bonus?"),
    minibox([("Bonus: ", "1 Seoul trading card (random, 12 solo designs)"), ("Condition: ", "Every 7,000 yen (tax incl.) in a single order")]),
    p(f"For {mark('every 7,000 yen spent in one order, you get one Seoul fan meeting trading card', True)}, while supplies last.<br>\n"
      "The card is one of 12 solo designs, the same as those at the venue.<br>\n"
      "Shipping and fees don't count, and separate orders can't be combined.<br>\n"
      "The 550-yen RANDOM TOY is handy for topping up (e.g. T-shirt + trading cards + RANDOM TOY = 7,150 yen)."),
    h2("Which items are sold out?"),
    minibox([("Sold out (as of 21:45 JST, Oct 16): ", "4 members' big uchiwa, 122-design cards, badges, ID photo holder")]),
    p("When we checked on the evening of launch day, some Japan fan meeting goods were already sold out: the big uchiwa fans for KEITO, RYOGA, SHINHAENG and YUKI, the 122-design trading cards, the badges and the ID photo holder.<br>\n"
      "All three new Seoul items and all 12 acrylic stands were still available at that point.<br>\n"
      "The store notes that stock may come back during the sale period."),
    h2("Order period, delivery and payment"),
    minibox([("Order period: ", "Oct 16 (Fri) 18:30 to Oct 18 (Sun) 23:59 (JST)"), ("Delivery: ", "From Nov 3")]),
    p("Orders are only taken on LAPONE STORE, and items will ship from November 3 so they arrive before the November 7 show.<br>\n"
      "Payment options are credit cards (Visa, Mastercard, American Express, JCB, Diners Club, Discover), Japanese mobile payments such as PayPay, prepaid convenience store payment and Paidy.<br>\n"
      f"Also, {mark('you cannot check out if the cart mixes these fan meeting goods with other products')}."),
    tweet(TW_START, "en"),
    h2("Can you order from outside Japan?"),
    minibox([("Shipping: ", "Japan only (Japanese address and phone number required)")]),
    p(f"LAPONE STORE's shipping policy requires a Japanese-language address and a phone number usable in Japan, and foreign phone numbers are not accepted, so {mark('this pre-order is effectively for people living in Japan')}.<br>\n"
      "Since the bonus card is described as the same design as the venue sale, goods are also expected to be sold at the venue in Seoul."),
    h2("Seoul fan meeting dates and venue"),
    minibox([("Dates: ", "Nov 7 (Sat) and Nov 8 (Sun), 4 shows"), ("Venue: ", "BLUESQUARE WOORI WON BANKING HALL")]),
    p("The event was first planned as three shows, and an extra show at 19:00 on Sunday, November 8 was added in September.<br>\n"
      "The venue is in Hannam-dong, Yongsan-gu, Seoul, right by Hangangjin Station on Subway Line 6.<br>\n"
      "For KO1KEYZ, who debuted in Japan and Korea on October 7, it will be a special chance to meet Korean fans in person."),
    html(MAP),
    note("* Information as of October 16, 2026. Please check KO1KEYZ's official site and LAPONE STORE for the latest details."),
    h2("Summary"),
    summarybox([
        "Seoul fan meeting goods are on pre-order at LAPONE STORE from Oct 16 18:30 to Oct 18 23:59 (JST)",
        "New items: trading cards (1,100 yen), muffler towel (2,500 yen), RANDOM TOY (550 yen)",
        "Japan fan meeting goods are sold on the same page",
        "1 solo trading card per 7,000 yen in a single order, while supplies last",
        "Delivery from Nov 3, Japan addresses only",
    ]),
    p("The handwritten name plates and stickers make RANDOM TOY a Seoul-only treat.<br>\n"
      "November can't come soon enough!"),
    linkbox("More on KO1KEYZ", EN_REL),
])

EN_SUMMARY = ("Goods for KO1KEYZ's first Seoul fan meeting are on pre-order at LAPONE STORE until Oct 18: new trading cards, muffler towel and RANDOM TOY, plus a solo card bonus per 7,000 yen.")


def count(c):
    t = re.sub(r"<!--.*?-->|<script.*?</script>|<iframe.*?</iframe>|<[^>]+>", "", c, flags=re.S)
    return len(re.sub(r"\s", "", t))


if __name__ == "__main__":
    for name, c in [("JP", JP_CONTENT), ("KR", KR_CONTENT), ("EN", EN_CONTENT)]:
        print(name, "chars:", count(c))
    print("JP title len", len(JP_TITLE))
    assert count(JP_CONTENT) >= 2500 and len(JP_TITLE) <= 35
    assert "<hr" not in JP_CONTENT + KR_CONTENT + EN_CONTENT
    if "--dry" in sys.argv:
        sys.exit()

    JP_EYECATCH_ID = make_eyecatch(
        ["--top", "ソウルファンミのグッズは？", "--main", "KO1KEYZ", "--bottom", "事前EC販売の値段と特典！", "--bottom", "10/18(日)23:59まで"],
        ROOT / "images" / "ko1keyz_seoul_fanmeeting_goods_1016_eyecatch.png")
    print("JP_EYECATCH_ID", JP_EYECATCH_ID)
    jp = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, "ja", [66, 62], JP_EYECATCH_ID, JP_SUMMARY)
    print("JP_POST_ID", jp["id"], jp["slug"])

    KR_EYECATCH_ID = make_eyecatch(
        ["--top", "서울 팬미팅 굿즈는?", "--main", "KO1KEYZ", "--bottom", "사전 EC 판매 가격과 특전!", "--bottom", "10/18(일) 23:59까지", "--lang", "kr"],
        ROOT / "images" / "ko1keyz_seoul_fanmeeting_goods_1016_eyecatch_kr.png")
    kr = post_draft(KR_TITLE, KR_CONTENT, KR_SLUG, "ko", [74, 70], KR_EYECATCH_ID, KR_SUMMARY, translations={"ja": jp["id"]})
    print("KR_POST_ID", kr["id"], kr["slug"])

    en = post_draft(EN_TITLE, EN_CONTENT, EN_SLUG, "en", [110, 112], JP_EYECATCH_ID, EN_SUMMARY, translations={"ja": jp["id"]})
    print("EN_POST_ID", en["id"], en["slug"])
