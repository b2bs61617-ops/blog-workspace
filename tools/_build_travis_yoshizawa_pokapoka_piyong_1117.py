# -*- coding: utf-8 -*-
"""chomoand-4.blog: 2026-11-16『ぽかぽか』で吉澤閑也のルイ・ヴィトン キーポルについていた黒猫のキーホルダー(オシリ依頼 11/17)。

根拠:
- 映像(TVer 月曜(2) epoa245iv0 の1080pコマ 2395/2404): ショルダーストラップの金具に黒いぬいぐるみ。
  黄色い目、黒い体にカラフルな糸のスプリンクル、下にワッフルコーン → 形・色が一致
- 商品: COMFORT「PIYONG 삐용이 Ice Cream Keyring」(公式 comfortseoul.com/product/.../767)
  公式説明: カラフルなスプリンクルをかけたピヨンのアイスクリームキーリング、ワッフルコーンの上にダブルアイスの形のピヨン。
  色 Black / ポリエステル90% 金属10% / 幅6cm 高さ23cm / 手作業で形が少しずつ違う / 製造 中国
  定価 ₩42,000(韓国サイトは品切れ表示 11/17確認、英語サイトは USD 38.00→セール中 USD 30.40 ~11/29)
  商品画像のフォルダが 2023/11 → 2023年11月ごろの発売とみられる
- ふつうの「PIYONG Keyring」(₩52,000、幅11cm、両手に磁石)とは別の商品
- 日本: 正規取扱いは見つからず。BUYMA で約5,900〜7,800円(11/17検索)
- 第三者の私物特定投稿(X)は記事に使わない(画像・言及なし)
- 円換算: 1ドル約1,330ウォン(11/11)・約160円(11/16) → 100ウォン≒12円
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "travis"
KEY = "travis_yoshizawa_pokapoka_piyong_1117"
TITLE = "【ぽかぽか】吉澤閑也のキーホルダーはどこの？黒猫アイスのピヨン！"
SLUG = "yoshizawa-shizuya-pokapoka-keychain-comfort-piyong-1117"
CATEGORIES = [3]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / "tj_yoshizawa_pokapoka_piyong_1117_eyecatch_canva.jpg"
EYECATCH_ALT = "吉澤閑也のバッグについていた黒猫のキーホルダー"
X_TEXT = "閑也くんのヴィトンのバッグに、黒猫がアイスになったキーホルダーついてたの気づいた？😭🖤🍦\n韓国のブランドのもので、ギャップがかわいすぎる…"
X_TAGS = "#TravisJapan #吉澤閑也 #ぽかぽか"

MEDIA_JSON = blogkit.ROOT / "images" / "pokapoka1116" / "media.json"
MEDIA = json.loads(MEDIA_JSON.read_text(encoding="utf-8"))
NEW_MEDIA = {
    "yoshizawa_piyong_keepall_1116": "吉澤閑也のルイ・ヴィトンのバッグについていた黒猫のキーホルダー",
    "yoshizawa_piyong_closeup_1116": "吉澤閑也のバッグの黒猫のアイスクリームのキーホルダーのアップ",
}

BAG = "https://chomoand-4.blog/?p=2921"
PERFUME = "https://chomoand-4.blog/?p=2821"
NAKAMURA_KH = "https://chomoand-4.blog/?p=2929"
OFFICIAL = "https://en.comfortseoul.com/product/piyong-ice-cream-keyring/767/"
SRC = "出典:フジテレビ『ぽかぽか』2026年11月16日放送"

b = blogkit.Blocks("#c9a227", "#f2dc8f", "#fdf8e6")
L = b.link


def ensure_media():
    wp = None
    for k, alt in NEW_MEDIA.items():
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
    return b.html(
        '<figure class="wp-block-image size-large"><img src="{0}" alt="{1}" width="1280" height="720" '
        'style="max-width:100%;height:auto;"><figcaption style="font-size:0.8em;color:#888;">{2}</figcaption></figure>'
        .format(m["url"], m["alt"], SRC))


def build():
    out = ""

    # ---- リード
    out += b.p(
        "2026年11月16日(月)の『ぽかぽか』で、吉澤閑也さんがふだん使っているカバンを見せてくれました。",
        "ルイ・ヴィトンの水色のボストンバッグには、黒い猫のキーホルダーがついていました。",
    )
    out += b.p(
        "このキーホルダーは、" + b.mark("韓国のブランドCOMFORT(コンフォート)の「PIYONG(ピヨン)アイスクリームキーリング」") + "とみられます。",
        "黒猫がアイスクリームになって、ワッフルコーンにのっているデザインです。",
        "この記事では、キーホルダーの特ちょうや値段、買える場所をまとめます。",
    )
    out += b.wakaru([
        "吉澤閑也のキーホルダーのブランド",
        "ピヨンのアイスクリームキーリングの特ちょう",
        "COMFORTとピヨンってなに？",
        "値段と買える場所",
    ])

    # ---- 結論
    out += b.h2("吉澤閑也のキーホルダーはどこの？")
    out += b.mini(
        ("ブランド", "COMFORT(コンフォート)・韓国"),
        ("商品", "PIYONG 삐용이 Ice Cream Keyring(ピヨン アイスクリームキーリング)"),
        ("色", "ブラック"),
        ("値段", "42,000ウォン(約5,000円)"),
    )
    out += fig("yoshizawa_piyong_keepall_1116")
    out += b.p(
        "キーホルダーがついていたのは、ルイ・ヴィトンのキーポルのショルダーストラップの金具です。",
        "バッグを正面から映したときに、右はしに黒いぬいぐるみが下がっているのが見えました。",
    )
    out += b.p(
        "番組ではキーホルダーの話はなく、吉澤さんもブランドは話していませんでした。",
        "そこで映像をアップにして、形や色を商品とくらべています。",
        "バッグとカバンの中身は、" + L(BAG, "吉澤閑也のぽかぽかのカバンの記事") + "で紹介しています。",
    )

    # ---- 特ちょう
    out += b.h2("黒猫のアイスクリームのキーホルダー")
    out += fig("yoshizawa_piyong_closeup_1116")
    out += b.p(
        "アップで見ると、COMFORTのピヨンのアイスクリームキーリングと特ちょうが同じでした。",
    )
    out += b.checks([
        "黒い猫のぬいぐるみに、黄色い目",
        "黒い体に、赤や青や黄色の糸で入ったスプリンクル(カラフルなトッピング)",
        "下にはベージュのワッフルコーン",
        "金属の金具でバッグにつながっている",
    ])
    out += b.p(
        "公式サイトでは、「カラフルなスプリンクルをかけたピヨンのアイスクリームキーリング」と紹介されています。",
        "ワッフルコーンの上に、ダブルのアイスの形になったピヨンがのっているデザインです。",
    )
    out += b.p(
        "ただ、映像では横向きで小さく、顔やブランドのタグまでは見えませんでした。",
        "形と色、スプリンクルの刺しゅうがすべて同じなので、同じ商品とみられます。",
    )

    out += b.h3("キーホルダーのサイズと素材")
    out += b.table(("", "内容"), [
        ("色", "ブラック"),
        ("サイズ", "幅6cm・高さ23cm(金具をふくむ)"),
        ("素材", "ポリエステル90%・金属10%"),
        ("つくり", "1つずつ手作業でぬっていて、目や鼻、コーンの長さが少しずつちがう"),
    ])
    out += b.p(
        "高さ23cmは金具までふくめた長さなので、ぬいぐるみの部分は手のひらくらいの大きさです。",
        "大きなボストンバッグにつけても、ちょうどよく目立つサイズ感でした。",
    )

    # ---- ブランド
    out += b.h2("COMFORTとピヨンってなに？")
    out += b.p(
        "COMFORT(コンフォート)は、韓国・ソウルのブランドです。",
        "洋服や雑貨をあつかうお店で、自分たちで作るキーリングがとくに人気です。",
    )
    out += b.p(
        "「ピヨン(삐용이)」は、COMFORTのキャラクターの黒猫です。",
        "黄色い目と、ペロッと出したピンクの舌がトレードマークです。",
        "ピヨンのキーリングには、ふつうの形のほかに、アイスや色ちがいなどいろいろな種類があります。",
    )
    out += b.h3("ふつうのピヨンのキーリングとのちがい")
    out += b.table(("", "アイスクリーム", "ふつうのピヨン"), [
        ("形", "アイスになってコーンにのっている", "手足のある猫の形"),
        ("値段", "42,000ウォン(約5,000円)", "52,000ウォン(約6,200円)"),
        ("サイズ", "幅6cm・高さ23cm", "幅11cm・高さ23cm"),
        ("とくちょう", "カラフルなスプリンクル", "両手に磁石がついている"),
    ])
    out += b.p(
        "ふつうのピヨンは手足があり、両手の磁石で手を合わせたり、何匹もつなげたりできます。",
        "吉澤さんのものには手足がなく、下にコーンが見えるので、アイスクリームのほうだと考えられます。",
    )

    # ---- 値段と買える場所
    out += b.h2("値段と買える場所は？")
    out += b.mini(
        ("公式の値段", "42,000ウォン(約5,000円)"),
        ("日本のお店", "正規の取りあつかいは見つからず"),
        ("通販の相場", "約5,900円〜7,800円(BUYMA)"),
    )
    out += b.p(
        "公式の値段は42,000ウォンで、日本円にすると約5,000円です。",
        "日本円は2026年11月ごろのレート(100ウォン=約12円)で計算しています。",
    )
    out += b.p(
        "COMFORTの韓国のオンラインストアでは、2026年11月17日に見たとき「品切れ」になっていました。",
        "英語版のストアでは38ドルで、11月29日までセール価格になっていましたが、注文できるかは商品ページで確かめてください。",
        L(OFFICIAL, "COMFORT公式の商品ページはこちら") + "です。",
    )
    out += b.p(
        "日本のお店では、アイスクリームのキーリングの正規の取りあつかいは見つかりませんでした。",
        "海外の買い物を代わりにしてくれる通販サイトのBUYMAでは、送料こみで約5,900円〜7,800円で出品されています(2026年11月17日に確認)。",
    )
    out += b.p(
        "人気のキャラクターなので、にた形のにせものも出回っています。",
        "フリマや通販で買うときは、タグに「COMFORT」と入っているか、写真と説明をよく確かめてください。",
    )

    # ---- 着こなし
    out += b.h2("ヴィトンのバッグにかわいいキーホルダー")
    out += b.p(
        "吉澤さんのバッグは、52万円台のルイ・ヴィトンのキーポルです。",
        "そこに5,000円ほどのゆるい黒猫を合わせているのが、とてもおしゃれなところです。",
    )
    out += b.p(
        "水色のデニムのバッグに黒いぬいぐるみがよく目立って、大人っぽいバッグがぐっとかわいく見えます。",
        "同じバッグに、前から長くつけているお気に入りのようです。",
    )
    out += b.p(
        "同じ日の『ぽかぽか』では、中村海人さんもバッグにスティッチとレゴのキーホルダーをつけていました。",
        "くわしくは" + L(NAKAMURA_KH, "中村海人のぽかぽかのキーホルダーの記事") + "で紹介しています。",
    )

    # ---- まとめ
    out += b.h2("まとめ")
    out += b.checks([
        "2026年11月16日の『ぽかぽか』で吉澤のバッグに黒猫のキーホルダー",
        "韓国COMFORTのピヨン アイスクリームキーリングとみられる",
        "公式の値段は42,000ウォン(約5,000円)",
        "日本では正規のお店が見つからず、通販で約5,900円〜",
    ])
    out += b.p(
        "クールなヴィトンのバッグに、ゆるかわいい黒猫のアイスを合わせるのが吉澤さんらしいポイントでした。",
        "おそろいにしたい人は、ぜひさがしてみてくださいね！",
    )
    out += b.p(
        "同じバッグから出てきた香水は、" + L(PERFUME, "吉澤閑也のぽかぽかの香水の記事") + "でまとめています。",
    )
    return out


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("タイトル文字数:", len(TITLE))
    if "--build-only" not in sys.argv:
        ensure_media()
    else:
        for k, alt in NEW_MEDIA.items():
            MEDIA.setdefault(k, {"url": "images/pokapoka1116/" + k + ".jpg", "alt": alt})
    out = blogkit.finalize(build(), SITE, NAMES)
    if "--build-only" in sys.argv:
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
