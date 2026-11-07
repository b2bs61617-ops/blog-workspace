# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) 岩本照のInstagram(2026-11-07「呼吸して～🍂」#MySicilyBag)で着ていた
ドルチェ&ガッバーナのチェックコート・スパンコール入りタートルネック・マイ シシリー バッグの記事HTMLを組み立てる。

usage: python tools/_build_snowman_iwamoto_dg_checkcoat_1107.py
articles/snowman_iwamoto_dg_checkcoat_1107.html と articles/snowman_iwamoto_dg_checkcoat_1107_manifest.json を書き出す。
商品情報・値段は dolcegabbana.jp の商品ページ(2026-11-07確認)。第三者の特定投稿の画像・言及は使わない。
"""
import os, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chomoand-2.com"
ACC = "#b8901c"      # 岩本照のメンバーカラー(黄)
LINE = "#efe1a8"
BG = "#fcf8e8"
MK = "#f5e7a6"
IG_CODE = "Dfb5lX_kgCP"
IG = f"https://www.instagram.com/p/{IG_CODE}/"


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


def ig_embed(label):
    u = f"https://www.instagram.com/p/{IG_CODE}/?utm_source=ig_embed&amp;utm_campaign=loading"
    return html(f'<blockquote class="instagram-media" data-instgrm-permalink="{u}" data-instgrm-version="14" '
                'style="background:#FFF;border:0;border-radius:3px;box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);'
                'margin:1px auto 16px;max-width:540px;min-width:326px;padding:0;width:99.375%;">'
                f'<a href="{u}" target="_blank" rel="noopener">{label}</a></blockquote>\n'
                '<script async src="https://www.instagram.com/embed.js"></script>')


def src(name, url, date):
    return f'出典:<a href="{url}" target="_blank" rel="noopener">{name}</a>({date})'


DGJP = "https://www.dolcegabbana.jp/ja-jp/"
COAT = DGJP + "single-breasted-check-coat-G061BTFQZAWS8100"
KNIT = DGJP + "wool-turtleneck-pullover-with-sequins-GXW98TJGMKWM0023"
BAG = DGJP + "%E3%83%9E%E3%82%A4-%E3%82%B7%E3%82%B7%E3%83%AA%E3%83%BC-%E3%82%AB%E3%83%BC%E3%83%95%E3%82%B9%E3%82%AD%E3%83%B3-%E3%83%8F%E3%83%B3%E3%83%89%E3%83%90%E3%83%83%E3%82%B0-BM2757B3T0580999"
TFT_AMB = "https://www.thefirsttimes.jp/?p=712222"
MILAN = f"{SITE}/?p=421"    # ミラノのドルガバ私服記事(下書き)
AIRBAG = f"{SITE}/?p=431"   # 空港バッグ記事(下書き)
DATE = "2026年11月7日確認"

body = "".join([
    p("岩本照さんが2026年11月7日、自身のInstagramに「呼吸して～🍂」と添えて、紅葉の中で撮った写真と動画を投稿しました。",
      f"着ていたのは、茶色のチェック柄のロングコートに、ブラウンのジップニット。手には大きな黒いバッグを持った{mk('全身ドルチェ&ガッバーナのコーデ')}です。",
      "投稿には「#MySicilyBag」のハッシュタグも付いていました。",
      "この記事では、岩本照さんが着ていたコート・ニット・バッグの商品名と値段を、ドルチェ&ガッバーナの公式サイトで確認してまとめました。"),
    listbox("この記事でわかること", ["11/7のInstagramに載せた秋コーデの写真",
                                    "コートはドルチェ&ガッバーナ「Single-breasted check coat」",
                                    "ニットは「Wool turtleneck pullover with sequins」",
                                    "バッグは「マイ シシリー カーフスキン ハンドバッグ」",
                                    "それぞれの値段・素材と在庫",
                                    "3点そろえたときの合計金額"], big=True),

    h2("岩本照がInstagramに載せた秋の写真"),
    keybox([("投稿日", "2026年11月7日"),
            ("アカウント", "岩本照さん本人のInstagram(@hikaru.iwamoto_sn_official)"),
            ("投稿文", "「呼吸して～🍂」(タグは@dolcegabbana・#MySicilyBag・#ドルチェガッバーナ・#DGxHIKARUなど)"),
            ("内容", "写真9枚+動画1本(紅葉の前・タイル張りの壁の前で撮影)")]),
    ig_embed("岩本照さんのInstagram投稿(2026年11月7日)"),
    p("1〜2枚目は、色づいた木々とビル街を背に、石の手すりにもたれて遠くを見る写真です。",
      "3枚目からはタイル張りの白い壁の前に移動して、大きなバッグを両手で持ったり、髪をかき上げたり。",
      f"空を見上げて目を閉じる写真もあり、投稿文の「呼吸して～」のとおり、{mk('秋の空気を深呼吸しているような')}1枚になっていました。"),
    p("最後の動画では、バッグを持ったままくるっと回ったり、コートのすそをひるがえしたりと、楽しそうに動く岩本照さんが見られます。",
      "ひざ下まである長いコートなので、動くたびにチェック柄が大きくゆれるのがよくわかります。",
      src("岩本照 Instagram", IG, "2026年11月7日")),

    h2("コートはドルチェ&ガッバーナ「Single-breasted check coat」"),
    table([["項目", "内容"],
           ["ブランド", "ドルチェ&ガッバーナ(DOLCE&GABBANA)"],
           ["商品名", "Single-breasted check coat(シングルブレスト チェック コート)"],
           ["品番", "G061BTFQZAW"],
           ["色", "マルチカラー(茶・ベージュ系のチェック)"],
           ["素材", "バージンウール55%・シルク24%・アルパカ13%・ポリアミド4%・モヘア4%(裏地はビスコース100%)"],
           ["つくり", "2つボタンのシングル・裏地付き・イタリア製"],
           ["着丈", "後ろ中心で120cm(サイズ48)"],
           ["値段", "1,023,000円(税込)"]]),
    p(f"コートは、ドルチェ&ガッバーナの{mk('「Single-breasted check coat」')}とみられます。",
      "こげ茶とベージュの糸を織り交ぜたツイードのような生地に、大きな格子のチェック柄。ボタンは2つで、胸もとの大きなえりと腰のフラップポケットも、公式の商品写真と同じです。"),
    p("素材はウールが中心ですが、シルク・アルパカ・モヘアも入っていて、表面にほどよい毛足とツヤがあります。",
      "着丈は後ろ中心で120cmもあり、モデル(身長185cm)が着てもふくらはぎまで届く長さ。",
      "岩本照さんの写真でも、ひざ下まですっぽり隠れるロング丈になっていました。",
      src("ドルチェ&ガッバーナ公式", COAT, DATE)),

    h3("値段は1,023,000円"),
    p(f"日本の公式オンラインストアでの値段は{mk('1,023,000円(税込)')}です。",
      "2026年11月7日の時点では、サイズ44〜60のうち48と50だけが在庫ありになっていました。",
      "気になる人は早めに公式オンラインストアかブティックで確認するのが確実です。"),

    h2("ニットは「Wool turtleneck pullover with sequins」"),
    table([["項目", "内容"],
           ["ブランド", "ドルチェ&ガッバーナ(DOLCE&GABBANA)"],
           ["商品名", "Wool turtleneck pullover with sequins(スパンコール付き ウール タートルネック)"],
           ["品番", "GXW98TJGMKW"],
           ["色", "ブラウン"],
           ["素材", "バージンウール98%・ポリエステル2%"],
           ["つくり", "長袖・ジップ開閉・イタリア製"],
           ["値段", "594,000円(税込)"]]),
    p("コートの下に着ていたのは、えりの高いブラウンのニットです。",
      f"首もとにジップが付いたハーフジップ型で、ドルチェ&ガッバーナの{mk('「Wool turtleneck pullover with sequins」')}と特徴が一致します。",
      "太めのリブ編みに、小さなスパンコールがところどころに散りばめられているのがポイント。"),
    p("写真をよく見ると、コートのそでから出たニットの袖口に、キラッと光る粒が見えます。",
      "遠目にはシンプルなブラウンのニットなのに、近くで見ると光る。そんな遊び心のある1枚です。",
      src("ドルチェ&ガッバーナ公式", KNIT, DATE)),

    h3("値段は594,000円"),
    p(f"日本の公式オンラインストアでの値段は{mk('594,000円(税込)')}です。",
      "2026年11月7日の時点では、XSとSが在庫あり、M〜XXLは在庫なしになっていました。"),

    h2("バッグは「マイ シシリー カーフスキン ハンドバッグ」"),
    table([["項目", "内容"],
           ["ブランド", "ドルチェ&ガッバーナ(DOLCE&GABBANA)"],
           ["商品名", "マイ シシリー カーフスキン ハンドバッグ"],
           ["品番", "BM2757B3T05"],
           ["色", "ブラック"],
           ["素材", "外側:カーフスキン95%・PVC5%/内側:コットン100%"],
           ["つくり", "レザーハンドル・取り外しと長さ調節ができるショルダーストラップ・タックイン開閉・シルバートーン金具・イタリア製"],
           ["コレクション", "2026-27秋冬メンズ「THE PORTRAIT OF MAN」"],
           ["値段", "946,000円(税込)"]]),
    p(f"手に持っていた黒い大きなバッグは、ドルチェ&ガッバーナの{mk('「マイ シシリー カーフスキン ハンドバッグ」')}です。",
      "投稿に「#MySicilyBag」のハッシュタグが付いていることからも、このバッグが主役の投稿だったことがわかります。"),
    p("「シシリー」はドルチェ&ガッバーナを代表するバッグのシリーズで、もともとはウィメンズの台形のハンドバッグとして知られています。",
      "今回のものは、2026-27秋冬メンズコレクション「THE PORTRAIT OF MAN」のメンズ用。",
      "セミグロス仕上げのカーフスキンに、かぶせぶたの上のロゴプレート、ハンドルから下がるネームタグと南京錠のチャームなど、写真と同じディテールが公式ページでも確認できます。"),
    p("ショルダーストラップが付いているので、手持ちと肩掛けの2通りで使えます。",
      "岩本照さんも、紅葉の前では肩から下げて、壁の前では両手で持ってと、写真ごとに持ち方を変えていました。",
      src("ドルチェ&ガッバーナ公式", BAG, DATE)),

    h3("値段は946,000円"),
    p(f"日本の公式オンラインストアでの値段は{mk('946,000円(税込)')}です。",
      "2026年11月7日の時点では在庫ありになっていました。",
      "ロゴ入りのダストバッグと箱が付いてきます。"),

    h2("3点そろえるといくら？"),
    table([["アイテム", "商品名", "値段(税込)", "購入先"],
           ["コート", "Single-breasted check coat", "1,023,000円", f'<a href="{COAT}" target="_blank" rel="noopener">公式オンラインストア</a>'],
           ["ニット", "Wool turtleneck pullover with sequins", "594,000円", f'<a href="{KNIT}" target="_blank" rel="noopener">公式オンラインストア</a>'],
           ["バッグ", "マイ シシリー カーフスキン ハンドバッグ", "946,000円", f'<a href="{BAG}" target="_blank" rel="noopener">公式オンラインストア</a>'],
           ["合計", "", "2,563,000円", ""]]),
    p(f"コート・ニット・バッグの3点で、合計は{mk('2,563,000円')}になります。",
      "どれも2026年11月7日の時点で、ドルチェ&ガッバーナの日本の公式オンラインストアに掲載されています。"),

    h2("パンツや靴は？"),
    keybox([("パンツ", "こげ茶のワイドなストレートパンツ(品名は未特定)"),
            ("靴", "黒いレザーのローファー、甲にシルバーの金具付き(品名は未特定)"),
            ("ピアス", "金色の小ぶりなフープ(品名は未特定)")]),
    p("パンツはニットと同じこげ茶系で、コートの下からのぞく色をそろえていました。",
      "足もとは、甲にシルバーの金具が付いた黒いローファー。バッグの金具と同じシルバーで、小物の色までそろえていたようです。",
      "パンツ・靴・ピアスの品名は、わかりしだい追記します。"),

    h2("岩本照とドルチェ&ガッバーナ"),
    p("岩本照さんは、2025年10月にドルチェ&ガッバーナのジャパンアンバサダーに就任しています。",
      src("THE FIRST TIMES", TFT_AMB, "2025年10月30日")),
    p("2026年9月にはミラノで行われたドルチェ&ガッバーナのショーに出席し、10月4日にはミラノのカフェで撮った写真をInstagramに投稿していました。",
      "このときもモヘアのカーディガンや水玉のシャツなど、全身ドルチェ&ガッバーナのコーデでした。"),
    p(f'ミラノで着ていたカーディガン・シャツ・ピアスは<a href="{MILAN}">こちらの記事</a>、ミラノへ向かう空港で持っていたバッグは<a href="{AIRBAG}">こちらの記事</a>でまとめています。'),
    p("ミラノでは水色のモヘアでやわらかく、今回は茶色のチェックで秋らしく。",
      "投稿文はどちらも「呼吸して～」で、季節ごとのドルチェ&ガッバーナのコーデを見せてくれるシリーズのようになっています。"),

    h2("まとめ"),
    listbox("まとめ", ["岩本照は11/7、紅葉の中で撮った写真と動画をInstagramに投稿",
                      "コートはドルチェ&ガッバーナ「Single-breasted check coat」(1,023,000円)",
                      "ニットは「Wool turtleneck pullover with sequins」(594,000円)",
                      "バッグは「マイ シシリー カーフスキン ハンドバッグ」(946,000円)",
                      "3点の合計は2,563,000円",
                      "バッグは2026-27秋冬メンズコレクションの新作"], big=True),
    related([("岩本照インスタのドルガバ私服はどれ？カーディガンの値段も！", MILAN),
             ("岩本照の空港バッグはドルガバのどれ？値段とサイズも！", AIRBAG),
             ("岩本照の愛称は？ひーくんと照兄の違い！", f"{SITE}/iwamoto-hikaru-nickname-244")]),
])

TITLE = "【未】岩本照のチェックコートはどこの？ドルガバのバッグと値段も！"
assert len(TITLE.replace("【未】", "")) <= 35, len(TITLE.replace("【未】", ""))

ARTICLES = [
    {"key": "iwamoto_dg_checkcoat_1107", "title": TITLE,
     "slug": "hikaru-iwamoto-dolce-gabbana-check-coat-my-sicily",
     "categories": [4, 6], "html": body},
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
        print("wrote", path, len(a["html"]))
    with open(os.path.join(REPO, "articles", "snowman_iwamoto_dg_checkcoat_1107_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
