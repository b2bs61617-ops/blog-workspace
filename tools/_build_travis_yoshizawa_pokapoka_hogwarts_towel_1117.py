# -*- coding: utf-8 -*-
"""chomoand-4.blog: 2026-11-16『ぽかぽか』で吉澤閑也のカバンから出てきたハンカチ(オシリ特定 11/17)。

根拠:
- 映像(TVer 月曜(2) epoa245iv0 の 2446〜2456秒あたり、1080pコマ hk2/005・020):
  キーポルの中に入っていて、ほかの出演者が取り出して台に置いた。グレージュのタオル地+赤い縁、
  オレンジの「HOGWARTS EXPRESS」、茶色い線の機関車、黄色×赤の紋章 → 公式写真と一致。
  下半分のレンガ柄と「PLATFORM 9¾」は折れていて見えない
- 音声(faster-whisper medium): スタジオで「ハンカチや」「ハンカチか」と言われただけ。ハリポタの話はなし
  (クイズの答え「タオル」は別の白いタオルのこと)
- 商品: Harry Potter SHOP(公式通販)「ホグワーツ特急 タオルハンカチ」770円(オシリのスクショで確認)
  オーガニックコットン/メーカー丸眞/約25×25cm/綿100%(オシリの商品説明スクショで確認 11/17)
- 2026/9/10 松倉・吉澤がスタジオツアー東京「闇の魔術のハロウィーン」をインスタで紹介
  (松倉 DdGd4IwE5LE / 吉澤 DdIt8IfEvDL 自撮り・ホグワーツ特急 / 吉澤 DdGjqb5owAs カーニバル動画)
- 「スタジオツアーで買った」とは書かない(本人発言なし)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "travis"
KEY = "travis_yoshizawa_pokapoka_hogwarts_towel_1117"
TITLE = "【ぽかぽか】吉澤閑也のハンカチはどこの？ハリポタのホグワーツ特急！"
SLUG = "yoshizawa-shizuya-pokapoka-handkerchief-hogwarts-express-1117"
CATEGORIES = [3]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / "tj_yoshizawa_pokapoka_hogwarts_towel_1117_eyecatch_canva.jpg"
EYECATCH_ALT = "吉澤閑也のホグワーツ特急のタオルハンカチ"

MEDIA_JSON = blogkit.ROOT / "images" / "pokapoka1116" / "media.json"
MEDIA = json.loads(MEDIA_JSON.read_text(encoding="utf-8"))
NEW_MEDIA = {
    "yoshizawa_hogwarts_towel_bag_1116": ("吉澤閑也のルイ・ヴィトンのバッグに入っていたハンカチ", 1280, 720),
    "yoshizawa_hogwarts_towel_table_1116": ("吉澤閑也のカバンから出てきたホグワーツ特急のハンカチ", 1280, 720),
    "yoshizawa_hogwarts_towel_closeup_1116": ("吉澤閑也のホグワーツ特急のタオルハンカチのアップ", 672, 702),
}

BAG = "https://chomoand-4.blog/?p=2921"
PIYONG = "https://chomoand-4.blog/?p=2955"
PERFUME = "https://chomoand-4.blog/?p=2821"
MATSUKURA_WATCH = "https://chomoand-4.blog/?p=1759"
OFFICIAL = "https://harrypottershop.jp/products/hogwarts-express-mini-towel"
SRC = "出典:フジテレビ『ぽかぽか』2026年11月16日放送"

b = blogkit.Blocks("#c9a227", "#f2dc8f", "#fdf8e6")
L = b.link


def ensure_media():
    wp = None
    for k, (alt, _w, _h) in NEW_MEDIA.items():
        if k in MEDIA:
            continue
        wp = wp or blogkit.WP(SITE)
        mid = wp.upload_media(str(MEDIA_JSON.parent / (k + ".jpg")), alt)
        m = wp.get("/media/{}".format(mid))
        MEDIA[k] = {"id": mid, "url": m["source_url"], "alt": alt}
        MEDIA_JSON.write_text(json.dumps(MEDIA, ensure_ascii=False, indent=1), encoding="utf-8")
        print("画像を上げた:", k, mid)


def fig(key):
    m = MEDIA[key]
    _alt, w, h = NEW_MEDIA[key]
    style = "max-width:100%;height:auto;" if w > h else "max-width:420px;width:100%;height:auto;"
    return b.html(
        '<figure class="wp-block-image size-large" style="text-align:center;"><img src="{0}" alt="{1}" width="{3}" height="{4}" '
        'style="{5}"><figcaption style="font-size:0.8em;color:#888;">{2}</figcaption></figure>'
        .format(m["url"], m["alt"], SRC, w, h, style))


def insta(code, account, name):
    url = "https://www.instagram.com/p/{}/?utm_source=ig_embed&amp;utm_campaign=loading".format(code)
    return b.html(
        '<div style="max-width:540px;margin:0 auto 16px;"><blockquote class="instagram-media" data-instgrm-permalink="'
        + url + '" data-instgrm-version="14" style="background:#FFF;border:0;border-radius:3px;'
        'box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);margin:1px;max-width:540px;min-width:326px;'
        'padding:0;width:calc(100% - 2px);"><a href="' + url + '" target="_blank" rel="noopener">'
        + "{}(@{})さんのInstagram投稿".format(name, account)
        + '</a></blockquote>\n<script async src="https://www.instagram.com/embed.js"></script></div>')


def build():
    out = ""

    # ---- リード
    out += b.p(
        "2026年11月16日(月)の『ぽかぽか』で、吉澤閑也さんがふだん使っているカバンの中身を見せてくれました。",
        "ルイ・ヴィトンのバッグからは、ハリー・ポッターのハンカチが出てきました。",
    )
    out += b.p(
        "このハンカチは、" + b.mark("ハリー・ポッター公式ショップの「ホグワーツ特急 タオルハンカチ」") + "とみられます。",
        "吉澤さんは2026年9月に、松倉海斗さんといっしょにハリー・ポッターのお仕事もしていました。",
        "この記事では、ハンカチの特ちょうや値段、ハリポタとのつながりをまとめます。",
    )
    out += b.wakaru([
        "吉澤閑也のハンカチのブランド",
        "番組の映像と商品のくらべ",
        "ホグワーツ特急 タオルハンカチの値段と買える場所",
        "松倉海斗とのハリー・ポッターのお仕事",
    ])

    # ---- 結論
    out += b.h2("吉澤閑也のハンカチはどこの？")
    out += b.mini(
        ("ショップ", "ハリー・ポッター ショップ(公式通販)"),
        ("商品", "ホグワーツ特急 タオルハンカチ"),
        ("値段", "770円(税込)"),
        ("素材", "オーガニックコットン"),
    )
    out += fig("yoshizawa_hogwarts_towel_table_1116")
    out += b.p(
        "カバンの中身を出していく途中で、いっしょにいた出演者がハンカチを取り出して、台の上に置きました。",
        "スタジオでは「ハンカチや」と声が上がっただけで、吉澤さんからブランドの話はありませんでした。",
    )
    out += b.p(
        "そこで映像をアップにして、柄や色を商品とくらべています。",
        "バッグとほかの中身は、" + L(BAG, "吉澤閑也のぽかぽかのカバンの記事") + "で紹介しています。",
    )

    # ---- くらべ
    out += b.h2("番組の映像と商品をくらべてみた")
    out += fig("yoshizawa_hogwarts_towel_closeup_1116")
    out += b.p(
        "アップで見ると、公式ショップの「ホグワーツ特急 タオルハンカチ」と特ちょうが同じでした。",
    )
    out += b.checks([
        "グレージュ(灰色がかったベージュ)のタオル地",
        "まわりのふちが赤いパイピング",
        "オレンジ色の「HOGWARTS EXPRESS」の文字",
        "細い線の刺しゅうでえがいた蒸気機関車",
        "機関車の前に、黄色と赤の「HOGWARTS EXPRESS」の紋章",
    ])
    out += b.p(
        "台の上では、ハンカチが横向きで置かれていました。",
        "文字が縦に見えますが、向きを変えると商品写真と同じ並びになります。",
    )
    out += fig("yoshizawa_hogwarts_towel_bag_1116")
    out += b.p(
        "バッグの中に入っていたときも、赤いふちと紋章、オレンジの文字が見えていました。",
    )
    out += b.p(
        "商品の下半分には、オレンジのレンガの模様と「PLATFORM 9¾」の文字があります。",
        "番組ではハンカチが折れていて、この部分は映っていませんでした。",
        "それ以外の柄や色はすべて同じなので、同じ商品とみられます。",
    )

    out += b.h3("どんなハンカチ？")
    out += b.table(("", "内容"), [
        ("商品名", "ホグワーツ特急 タオルハンカチ"),
        ("値段", "770円(税込)"),
        ("メーカー", "丸眞(Marushin)"),
        ("サイズ", "約25cm×25cm"),
        ("素材", "綿100%(オーガニックコットン)"),
        ("デザイン", "ホグワーツ特急の機関車・「HOGWARTS EXPRESS」・9と3/4番線"),
    ])
    out += b.p(
        "ホグワーツ特急は、ハリーたちがロンドンのキングズ・クロス駅の9と3/4番線から乗る、ホグワーツ行きの赤い汽車です。",
        "公式ショップでは「ロンドンからホグワーツへ向かっているかのような」デザインと紹介されています。",
        "落ちついた色の生地に、あざやかな赤の刺しゅうで蒸気機関車がえがかれています。",
        "落ちついた色の生地なので、大人の男性が持っても子どもっぽく見えません。",
    )

    # ---- 値段と買える場所
    out += b.h2("値段と買える場所は？")
    out += b.p(
        "値段は770円(税込)です。",
        "ワーナー ブラザースのハリー・ポッター公式グッズの通販サイト「ハリー・ポッター ショップ」で買えます。",
        L(OFFICIAL, "ハリー・ポッター ショップの商品ページはこちら") + "です。",
    )
    out += b.p(
        "公式ショップには、同じシリーズでホグワーツやスリザリンなどのタオルハンカチもあります。",
        "在庫や値段は変わることがあるので、商品ページで確かめてください。",
    )
    out += b.p(
        "52万円台のルイ・ヴィトンのバッグに、770円のハリポタのハンカチを入れているのが、吉澤さんらしいところです。",
    )

    # ---- ハリポタのお仕事
    out += b.h2("9月に松倉海斗とハリー・ポッターのお仕事")
    out += b.p(
        "吉澤さんと松倉海斗さんは、2026年9月10日に「ワーナー ブラザース スタジオツアー東京 - メイキング・オブ・ハリー・ポッター」のイベントを、そろってInstagramで紹介していました。",
        "この日から始まった特別企画「闇の魔術のハロウィーン」のお仕事です。",
    )
    out += b.p(
        "吉澤さんは「楽しくて珍しく自撮りしてた」「ホグワーツがデカすぎてびっくりだった」とつづっています。",
    )
    out += insta("DdIt8IfEvDL", "shizuya.yoshizawa_tj", "吉澤閑也")
    out += b.p(
        "もう1つの投稿では、ホグワーツ特急の前で「カーニバル」をおどる動画を載せていました。",
        "「テンション上がりすぎてカーニバルしちゃいました」とのことです。",
    )
    out += insta("DdGjqb5owAs", "shizuya.yoshizawa_tj", "吉澤閑也")
    out += b.p(
        "スタジオツアー東京には、映画の撮影で使われたものと同じ形のホグワーツ特急の機関車が展示されています。",
        "9と3/4番線のホームも再現されていて、人気の写真スポットです。",
        "吉澤さんの投稿にも、この赤い機関車と「9¾」の文字が写っていました。",
        "ハンカチにえがかれているのも、まさにこの機関車です。",
    )
    out += b.p(
        "松倉さんも同じ日に、大広間に浮かぶジャック・オー・ランタンや、デスイーターが登場する館内のようすを紹介していました。",
    )
    out += insta("DdGd4IwE5LE", "machu_tj_1114", "松倉海斗")
    out += b.p(
        "松倉さんは2025年5月にもスタジオツアー東京の写真を載せていて、「ハリポタ最高すぎた。」とつづるほどのハリポタ好きです。",
        "そのときのようすは" + L(MATSUKURA_WATCH, "松倉海斗の腕時計の記事") + "でもふれています。",
    )
    out += b.p(
        "吉澤さんは番組でハンカチの話をしていないので、いつどこで手に入れたのかは分かっていません。",
        "ただ、吉澤さんはホグワーツ特急の前で写真や動画をとっていました。",
        "その吉澤さんが同じホグワーツ特急のハンカチを持ち歩いているのは、ファンにはうれしいポイントですね。",
        "お仕事の思い出として、ふだん使いしているのかもしれません。",
    )

    # ---- まとめ
    out += b.h2("まとめ")
    out += b.checks([
        "2026年11月16日の『ぽかぽか』で吉澤のカバンからハンカチ",
        "ハリー・ポッター ショップの「ホグワーツ特急 タオルハンカチ」とみられる",
        "値段は770円(税込)、約25cm×25cmのオーガニックコットン",
        "9月には松倉海斗とスタジオツアー東京のお仕事も",
    ])
    out += b.p(
        "770円で吉澤さんとおそろいにできるので、ハリポタ好きの人もぜひチェックしてみてくださいね！",
    )
    out += b.p(
        "同じバッグについていたキーホルダーは、" + L(PIYONG, "吉澤閑也のキーホルダーの記事") + "で紹介しています。",
        "カバンから出てきた香水は、" + L(PERFUME, "吉澤閑也の香水の記事") + "でまとめています。",
    )
    return out


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    base = blogkit.strip_mi(TITLE)
    print("タイトル文字数(【未】抜き):", len(base))
    assert len(base) <= 35
    if "--build-only" not in sys.argv:
        ensure_media()
    else:
        for k, (alt, _w, _h) in NEW_MEDIA.items():
            MEDIA.setdefault(k, {"url": "images/pokapoka1116/" + k + ".jpg", "alt": alt})
    out = blogkit.finalize(build(), SITE, NAMES)
    (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
    if "--build-only" in sys.argv:
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
