# -*- coding: utf-8 -*-
"""chomoand-4.blog: 2026-11-19の『Jewelry Basket』配信記念インスタライブ(#TJgramLIVE)で7人が着ていた服(2026-11-20 オシリ依頼)。

根拠:
- Travis Japan公式Instagramのアーカイブ https://www.instagram.com/travis_japan_official/reel/Df7GWKxk_7K/
  (2026-11-19 21:38 JST投稿、約20分31秒)。動画は左右反転していたので、反転を戻した画(m_*/z_*)だけ使う。
- 着用者の割り当ては材料メモ末尾「オシリ確認済み(11/20)」が最優先:
  Umbro=宮近 / メガネ白T=松田 / ジャージ=川島 / CHANELビーニー=中村 / CELINEエンジ帽=松倉 /
  アイボリーニット=七五三掛 / 赤髪黒ジップ=吉澤。紙を持って立ち上がったのは松田(cs_standupで確認)。
- CELINEビーニー: 公式「CELINE BEANIE IN WOOL CASHMERE」(AA0H92I93、ウール90%・カシミヤ10%、イタリア製)。
  バーガンディの色ページと日本の定価は未確認。US公式の帽子一覧の検索結果でBURGUNDY 420ドル(要約のみ)→断定しない。
- CHANELビーニー: 既存記事729/1583の調べ(Beanie Cashmere AAA748B19217NACWY、カシミヤ100%、2023年秋冬、公式価格非公開)。
- ジャージ: 既存記事1213(中村海人デザインのオリジナル、メンバーカラー違い、販売未定)。川島のメンカラ=白。
- 話の内容は自動文字起こし(粗い)。発言者は特定しない書き方にする。
- ファンの特定投稿・ファンのX投稿は使わない。
- リンク先は公開中の記事だけ(2505 CD延期・2421パナスタ服の色・2471熊本は下書きなのでリンクしない)。
"""
import json
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
import affiliate_box as ab  # noqa: E402

SITE = "travis"
KEY = "tj_jewelrybasket_reel_shifuku_1120"
TITLE = "【未】【インライ】トラジャ私服どこの？松倉CELINE帽・宮近Umbro！"
SLUG = "travis-japan-tjgramlive-1119-outfit-celine-umbro"
CATEGORIES = [3]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch_canva.jpg")
EYECATCH_ALT = "Travis Japanのインスタライブの私服"

IMG_DIR = blogkit.ROOT / "images" / "tj_jb_reel_1120"
MEDIA_JSON = IMG_DIR / "media.json"
MEDIA = json.loads(MEDIA_JSON.read_text(encoding="utf-8")) if MEDIA_JSON.exists() else {}
NEW_MEDIA = {
    "tj_jb_inrai_1119_group": "インスタライブのスクショタイムで集まったTravis Japanの7人",
    "tj_jb_inrai_1119_seated": "インスタライブで座って話すTravis Japanの7人の服装",
    "tj_jb_inrai_1119_umbro": "宮近海斗の黒いスウェットの胸のUmbroのロゴ",
    "tj_jb_inrai_1119_miyachika": "インスタライブの最後にアップで映った宮近海斗",
    "tj_jb_inrai_1119_celine_beanie": "松倉海斗のエンジ色のCELINEのニット帽",
    "tj_jb_inrai_1119_celine_hoodie": "松倉海斗のCELINE PARISのロゴのグレーのパーカーと黒いレザー",
    "tj_jb_inrai_1119_chanel_beanie": "中村海人のCHANELのカメリアのビーニー",
    "tj_jb_inrai_1119_jersey": "川島如恵留のTravis Japanのロゴ入りのジャージ",
    "tj_jb_inrai_1119_whitetee": "松田元太のアート柄の白いTシャツ",
    "tj_jb_inrai_1119_watch": "松田元太の金色のケースにターコイズの文字盤の腕時計",
    "tj_jb_inrai_1119_knit": "七五三掛龍也のアイボリーのダイヤ柄のニットとストライプのシャツ",
    "tj_jb_inrai_1119_seated2": "黒いジップパーカーの吉澤閑也とCELINEのパーカーの松倉海斗",
    "tj_jb_inrai_1119_standup": "紙を持って立ち上がった松田元太",
    "tj_jb_inrai_1119_standup2": "紙を持つ松田元太と止めに行く七五三掛龍也",
}

IG = "https://www.instagram.com/travis_japan_official/reel/Df7GWKxk_7K/"
SRC = "出典:Travis Japan公式Instagram(2026年11月19日のインスタライブのアーカイブ)"
CELINE_US = "https://www.celine.com/en-us/celine-shop-men/accessories/hats-and-soft-accessories/celine-beanie-in-wool-cashmere-AA0H92I93.38AO.html"
CELINE_JP = "https://www.celine.com/ja-jp/"

U_JERSEY = "https://chomoand-4.blog/where-is-the-jersey-from-genta-1213"
U_CHANEL_SENGA = "https://chomoand-4.blog/where-does-kaito-nakamuras-cas-729"
U_CHAKAUMI = "https://chomoand-4.blog/chakaumi-harajuku-sanpo-outfit-tomford-1583"
U_MATSU_CELINE = "https://chomoand-4.blog/matsukura-kaito-celine-knit-hoodie-1666"
U_DIGITAL = "https://chomoand-4.blog/travis-japan-jewelry-basket-digital-release-2778"
U_JEWELHUNT = "https://chomoand-4.blog/travis-japan-jewelry-basket-ads-osaka-dotonbori-shibuya-2908"
U_TAIPEI = "https://chomoand-4.blog/kawashima-taipei-dome-y3-setup-1433"

_K = ab.load_keys()
_TAG = _K.get("AMAZON_ASSOCIATE_TAG", "")


def rk(q):
    s = "https://search.rakuten.co.jp/search/mall/" + urllib.parse.quote(q) + "/"
    return ("https://hb.afl.rakuten.co.jp/hgc/{}/?pc=".format(_K["RAKUTEN_AFFILIATE_ID"])
            + urllib.parse.quote(s, safe="") + "&m=" + urllib.parse.quote(s, safe=""))


def amz(q):
    return "https://www.amazon.co.jp/s?k=" + urllib.parse.quote(q) + ("&tag=" + _TAG if _TAG else "")


b = blogkit.Blocks("#7e57c2", "#b39ddb", "#f5f2fb")
L = b.link


def ensure_media():
    wp = None
    for k, alt in NEW_MEDIA.items():
        if k in MEDIA and str(MEDIA[k].get("url", "")).startswith("http"):
            continue
        wp = wp or blogkit.WP(SITE)
        mid = wp.upload_media(str(IMG_DIR / (k + ".jpg")), alt)
        m = wp.get("/media/{}".format(mid))
        MEDIA[k] = {"id": mid, "url": m["source_url"], "alt": alt}
        MEDIA_JSON.write_text(json.dumps(MEDIA, ensure_ascii=False, indent=1), encoding="utf-8")
        print("画像を上げた:", k, mid)


def fig(k, w=360):
    m = MEDIA[k]
    return b.html(
        '<figure class="wp-block-image size-large"><img src="{0}" alt="{1}" '
        'style="max-width:{3}px;width:100%;height:auto;display:block;margin:0 auto;">'
        '<figcaption style="font-size:0.8em;color:#888;text-align:center;">{2}</figcaption></figure>'
        .format(m["url"], m["alt"], '出典：<a href="{0}" target="_blank" rel="noopener">{0}</a>'.format(IG), w))


def igembed(url):
    return b.html('<blockquote class="instagram-media" data-instgrm-permalink="{0}?utm_source=ig_embed" '
                  'data-instgrm-version="14" style="background:#FFF;border:0;margin:1px auto;max-width:540px;'
                  'min-width:280px;width:calc(100% - 2px);"><a href="{0}" target="_blank" rel="noopener">'
                  'Travis Japan公式Instagramの投稿を見る</a></blockquote>\n'
                  '<script async src="//www.instagram.com/embed.js"></script>'.format(url))


def build():
    out = ""

    # ---- リード
    out += b.p(
        "2026年11月19日の夜、Travis Japanの7人がそろってインスタライブを行いました。",
        "アルバム『Jewelry Basket』の配信開始を記念した配信で、画面に映った私服が気になった人も多いはずです。",
    )
    out += b.p(
        "画面をアップにして確かめると、" + b.mark("松倉海斗はCELINEのニット帽、宮近海斗はUmbroのスウェット") + "でした。",
        "中村海人のCHANELのビーニーや、川島如恵留のオリジナルジャージも映っています。",
        "この記事では、7人の服を1人ずつと、配信で話していた内容をまとめます。",
    )
    out += b.mini(
        ("配信", "Travis Japan公式Instagramのインスタライブ(#TJgramLIVE)"),
        ("日時", "2026年11月19日(木)20時20分ごろ〜約20分"),
        ("出演", "7人全員"),
        ("アーカイブ", "同じ日の21時38分ごろに公式アカウントに投稿"),
    )
    out += b.wakaru([
        "7人の服の一覧",
        "松倉海斗のCELINEのニット帽とパーカー",
        "宮近海斗のUmbroのスウェット",
        "中村海人のCHANELのビーニー",
        "川島如恵留のオリジナルジャージ",
        "松田元太・吉澤閑也・七五三掛龍也の服",
        "インスタライブで話していたこと",
        "松田元太が紙を持って立ち上がった場面",
    ])

    # ---- 一覧
    out += b.h2("インスタライブのトラジャの私服はどこの？7人の一覧")
    out += b.mini(
        ("分かった物", "CELINE・Umbro・CHANEL・オリジナルジャージ"),
        ("分からなかった物", "松田元太・吉澤閑也・七五三掛龍也の服など"),
    )
    out += b.p(
        "インスタライブは、スマホのカメラの映像がそのまま流れるので、画面の左右が反対に映ります。",
        "アーカイブでも「CELINE」や「umbro」の文字が鏡文字になっていました。",
        "この記事の写真は、左右を元に戻したものです。",
    )
    out += fig("tj_jb_inrai_1119_group")
    out += b.p(
        "終わりぎわのスクショタイムで、7人がぎゅっと集まった場面です。",
        "まずは、7人が着ていた服を表にまとめます。",
    )
    out += b.table(("メンバー", "目立っていた服", "ブランド"), [
        ("松倉海斗", "エンジ色のニット帽・グレーのパーカー", "CELINE"),
        ("宮近海斗", "黒のスウェット", "Umbro"),
        ("中村海人", "黒のビーニー(白い花のマーク)", "CHANEL"),
        ("川島如恵留", "黒×白のジャージ", "中村海人デザインのオリジナル"),
        ("松田元太", "メガネ・アート柄の白T・腕時計", "未特定"),
        ("吉澤閑也", "黒のジップパーカー", "未特定"),
        ("七五三掛龍也", "アイボリーのダイヤ柄ニット", "未特定"),
    ])
    out += b.p(
        "インスタライブで着ていた服なので、私物か、用意された服かは分かりません。",
        "ただ、中村さんのビーニーや川島さんのジャージは、これまでの配信にも出てきた物です。",
    )
    out += fig("tj_jb_inrai_1119_seated")
    out += b.p(
        "座って話していた場面では、後ろの列が左から中村さん・松田さん・川島さんです。",
        "前の列は左から宮近さん・松倉さん・吉澤さん・七五三掛さんの順でした。",
    )

    # ---- 松倉
    out += b.h2("松倉海斗のニット帽はCELINE")
    out += b.mini(
        ("ニット帽", "CELINEのロゴ入りビーニーとみられる(エンジ色)"),
        ("パーカー", "CELINEの「CELINE PARIS」ロゴのグレーのパーカー(品番は未特定)"),
        ("ほか", "黒のレザーのブルゾン、ライトブルーのワイドデニム、黒の革靴"),
    )
    out += fig("tj_jb_inrai_1119_celine_beanie")
    out += b.p(
        "いちばん目立っていたのが、松倉さんのエンジ色のニット帽です。",
        "折り返しの部分に、白い大きな文字で「CELINE」と編みこまれています。",
    )
    out += b.p(
        "セリーヌの公式サイトには、同じデザインの「CELINE BEANIE IN WOOL CASHMERE」があります。",
        "折り返しにCELINEの文字を編みこんだビーニーで、ウール90%・カシミヤ10%のイタリア製です。",
        "松倉さんのニット帽は、このビーニーのエンジ色(バーガンディ)とみられます。",
    )
    out += b.p(
        "海外の公式サイトでは、同じデザインのビーニーが400ドル台で出ています。",
        "ただ、エンジ色の商品ページと日本の値段は確かめられていません。",
    )
    out += b.html('<p style="font-size:0.9em;">参考:' + L(CELINE_US, "CELINE公式(アメリカ)の同じデザインのビーニー")
                  + '<br>参考:' + L(CELINE_JP, "セリーヌ日本公式オンラインストア") + "</p>")
    out += fig("tj_jb_inrai_1119_celine_hoodie")
    out += b.p(
        "ニット帽の下には、グレーのパーカーを着ていました。",
        "胸には縁どりのある大きな「CELINE」の文字と、その下に小さく「PARIS」が入っています。",
        "大学のロゴのようなデザインで、セリーヌのフーディーとみられますが、品番までは分かりませんでした。",
    )
    out += b.p(
        "その上に黒のレザーのブルゾンをはおり、下はライトブルーのワイドデニムです。",
        "帽子とパーカーの2つをセリーヌでそろえた、松倉さんらしいコーデでした。",
    )
    out += b.p(
        "松倉さんはセリーヌを着ている姿がよく見られ、" + L(U_MATSU_CELINE, "セリーヌの黒いニットパーカーの記事") + "でも紹介しています。",
    )
    out += ab.build_box(rk("セリーヌ ビーニー ロゴ"), None,
                        "セリーヌ ロゴ入りビーニー",
                        amz("セリーヌ ビーニー ロゴ"),
                        note="楽天・Amazonの検索結果です(色・正規品かどうかを確かめてください)",
                        border="#b39ddb")
    out += "\n"

    # ---- 宮近
    out += b.h2("宮近海斗のスウェットはUmbro")
    out += b.mini(
        ("スウェット", "Umbro(アンブロ)の黒のクルーネック(型番は未特定)"),
        ("目印", "左胸にひし形のロゴと「umbro」の白い刺しゅう"),
        ("ほか", "黒のワイドパンツ、キャメル色のブーツ、小さなピアス"),
    )
    out += fig("tj_jb_inrai_1119_umbro")
    out += b.p(
        "宮近さんが着ていたのは、黒いクルーネックのスウェットです。",
        "左胸に、ひし形のロゴと「umbro」の文字が白い糸で小さく刺しゅうされていました。",
        "これはイギリス生まれのスポーツブランド、Umbro(アンブロ)のロゴです。",
    )
    out += b.p(
        "アンブロはサッカーのユニフォームで知られるブランドです。",
        "最近はセレクトショップとの別注アイテムも多く、街で着る服としても人気があります。",
    )
    out += b.p(
        "ただ、映像では首のタグや背中が見えず、どの商品かまでは分かりませんでした。",
        "ワンポイントのロゴだけのシンプルな黒スウェットは、アンブロでも定番の形です。",
        "似た物を探すなら、「アンブロ ワンポイント スウェット」で探すと見つかりやすいです。",
    )
    out += fig("tj_jb_inrai_1119_miyachika")
    out += b.p(
        "配信の最後には、宮近さんがカメラに近づいてアップで映りました。",
        "このときも、胸のアンブロのロゴがはっきり見えています。",
    )
    out += ab.build_box(rk("アンブロ スウェット ワンポイント 黒"), None,
                        "アンブロ ワンポイントロゴ スウェット(黒)",
                        amz("アンブロ スウェット ワンポイント 黒"),
                        note="楽天・Amazonの検索結果です(宮近海斗の着用品と同じとは限りません)",
                        border="#b39ddb")
    out += "\n"

    # ---- 中村
    out += b.h2("中村海人のビーニーはCHANEL")
    out += b.mini(
        ("ビーニー", "CHANEL「Beanie Cashmere」とみられる(品番AAA748B19217NACWY)"),
        ("素材", "カシミヤ100%(2023年秋冬)"),
        ("値段", "公式は価格非公開(中古は650〜850ドル前後)"),
        ("ほか", "黒のニット、ブルーのデニム"),
    )
    out += fig("tj_jb_inrai_1119_chanel_beanie")
    out += b.p(
        "中村さんは、黒いリブ編みのビーニーをかぶっていました。",
        "白いもこもこの花のモチーフの真ん中に、CHANELの「CC」マークが入っています。",
    )
    out += b.p(
        "このビーニーは、これまでの記事で2回紹介してきた物と同じ見た目です。",
        L(U_CHANEL_SENGA, "千賀健永の配信で中村海人がかぶってたビーニーの記事") + "で、CHANELの「Beanie Cashmere」と調べています。",
        L(U_CHAKAUMI, "ちゃかうみの原宿散歩の私服の記事") + "でも、同じビーニーが出てきました。",
    )
    out += b.p(
        "既存の記事と見くらべても、白い花の形とCCの位置は同じでした。",
        "CHANELの公式サイトでは値段が出ていません。", "海外の中古ショップでは650〜850ドル(目安で約10万〜13万円)ほどです。",
    )
    out += b.p(
        "服は黒のクルーネックのニットに、ブルーのデニムを合わせていました。",
        "黒でまとめた中に、ビーニーの白い花がよく目立っていました。",
    )

    # ---- 川島
    out += b.h2("川島如恵留のジャージは中村海人デザインのオリジナル")
    out += b.mini(
        ("ジャージ", "Travis Japanのロゴ入りトラックジャケット"),
        ("デザイン", "中村海人(メンバーへのプレゼント)"),
        ("販売", "予定なし(2026年11月20日時点で発表なし)"),
    )
    out += fig("tj_jb_inrai_1119_jersey")
    out += b.p(
        "川島さんは、黒に白いラインの入ったトラックジャケットを着ていました。",
        "胸には四角に「T」を組み合わせたマークと、「Travis Japan」の文字が入っています。",
    )
    out += b.p(
        "これは、中村さんがデザインしてメンバーにプレゼントしたオリジナルのジャージです。",
        "10月3日に松田さんがインスタライブで着て、中村さんが作ってくれた物だと紹介していました。",
        "くわしくは" + L(U_JERSEY, "松田元太のインスタライブのジャージの記事") + "でまとめています。",
    )
    out += b.p(
        "そのときの説明では、ジャージはメンバーごとに自分のメンバーカラーが入った色ちがいです。",
        "川島さんのメンバーカラーは白で、今回のジャージもラインやわきのドット柄が白になっていました。",
        "松田さんの青とは色だけがちがう、川島さん用の1着とみられます。",
    )
    out += b.p(
        "耳には金色のフープピアスを着けていました。",
        "川島さんのジャージ姿は、" + L(U_TAIPEI, "台北ドームのY-3のジャージの記事") + "でも紹介しています。",
    )

    # ---- 松田・吉澤・七五三掛
    out += b.h2("松田元太・吉澤閑也・七五三掛龍也の服は？")
    out += b.mini(
        ("松田元太", "黒縁の丸メガネ、アート柄の白T、金色×ターコイズの腕時計(どれも未特定)"),
        ("吉澤閑也", "黒のジップパーカー、グレーのワイドパンツ(未特定)"),
        ("七五三掛龍也", "アイボリーのダイヤ柄ニット、ストライプのシャツ(未特定)"),
    )
    out += b.h3("松田元太はアート柄の白Tと腕時計")
    out += fig("tj_jb_inrai_1119_whitetee")
    out += b.p(
        "松田さんは、黒縁の丸いメガネに白いTシャツを合わせていました。",
        "Tシャツの胸には、赤いだ円と黒い筆のような形をえがいたアートがプリントされています。",
        "ブランドのロゴは見えず、どこの物かは分かりませんでした。",
    )
    out += fig("tj_jb_inrai_1119_watch")
    out += b.p(
        "手首には、金色のケースにターコイズブルーの文字盤の腕時計が見えました。",
        "形は丸型でしたが、映像が小さく、ブランドや型番は確かめられていません。",
        "黒のベルトにグレーのスラックス、黒のローファーを合わせた、きれいめのコーデでした。",
    )
    out += b.h3("吉澤閑也は黒のジップパーカー")
    out += fig("tj_jb_inrai_1119_seated2")
    out += b.p(
        "赤い髪が目立つ吉澤さんは、黒のジップパーカーを着ていました。",
        "白いファスナーが入ったデザインで、下はグレーのワイドパンツです。",
        "首もとには、細い金色のネックレスが光っていました。",
    )
    out += b.p(
        "パーカーにはブランドが分かるロゴが見えず、未特定です。",
    )
    out += b.h3("七五三掛龍也はアイボリーのニット")
    out += fig("tj_jb_inrai_1119_knit")
    out += b.p(
        "七五三掛さんは、アイボリーのVネックのニットを着ていました。",
        "ダイヤの形に透かし編みが入っていて、えりもとからストライプのシャツをのぞかせています。",
    )
    out += b.p(
        "下はベージュのワイドなチノパンに、茶色のレースアップの革靴です。",
        "金色の細いネックレスと、金色のリングも合わせていました。",
        "ニットにもロゴは見えず、ブランドは分かりませんでした。",
    )

    # ---- 話の内容
    out += b.h2("インスタライブで話していたことは？")
    out += b.mini(
        ("お礼", "アルバム『Jewelry Basket』の配信開始とランキング1位"),
        ("おわび", "CDの発売が12月16日に延びたこと"),
        ("お願い", "Jewel Huntの広告を見に行くときのマナー"),
        ("Jリーグ", "スタジアムでのライブに来る人へのお願い"),
    )
    out += igembed(IG)
    out += b.p(
        "配信は「もう8時20分です」というあいさつから始まりました。",
        "同時に見ている人は、すぐに1.7万人をこえたと喜んでいました。",
    )
    out += b.h3("アルバムの配信開始のお礼")
    out += b.p(
        "最初に話したのは、11月18日にアルバム『Jewelry Basket』の配信が始まったことへのお礼でした。",
        "コメントの「MVを見て泣いちゃった」という声を読み上げる場面もありました。",
    )
    out += b.p(
        "MVで共演したジュニアの話や、入所記念日をお祝いする話でも盛り上がっています。",
        "配信開始とMVのことは、" + L(U_DIGITAL, "Jewelry Basket配信開始！MVのジュニア14人は誰？") + "でくわしく書いています。",
    )
    out += b.p(
        "10分ごろには、レコチョクのデイリーランキングで1位になったことも報告しました。",
        "アルバムとハイレゾのランキングで1位になり、メンバーもうれしそうでした。",
    )
    out += b.h3("CDの発売延期のおわび")
    out += b.p(
        "8分20秒ごろには、CDの発売が12月16日(水)になったことについて話しました。",
        "「ちょっと遅れちゃいましたけど、申し訳ないです」と、メンバーがおわびしています。",
        "「完璧な物を届けたいから」と、前向きな気持ちも伝えていました。",
    )
    out += b.p(
        "そのあとは、「ワクワクする時間が増えたってこと」と、待つ時間を楽しんでほしいと話しています。",
    )
    out += b.h3("Jewel Huntの広告とFCのお知らせ")
    out += b.p(
        "11分ごろには、駅の広告をめぐる「Jewel Hunt」の話になりました。",
        "見に行ったファンの動画を見たことや、通行のじゃまにならないようにというお願いを伝えています。",
        "大阪の広告に「行きたかった」という声もありました。",
    )
    out += b.p(
        "広告の場所は、" + L(U_JEWELHUNT, "Jewel Huntの駅広告の場所の記事") + "でまとめています。",
    )
    out += b.p(
        "13分ごろには、FC盤(ファンクラブ限定のCD)の追加受付がFCのメールで発表されたことを紹介しました。",
        "ユニット曲のスペシャル動画が配信されたことも伝えています。",
        "翌日の当落(当選・落選の発表)に向けて、みんなでパワーを送る場面もありました。",
    )
    out += b.h3("Jリーグのスタジアムライブへのお願い")
    out += b.p(
        "16分ごろからは、Jリーグのスタジアムで行う特別ライブの話になりました。",
        "スタジアムには、ホームとアウェイのチームの関係や、着ていくと良くない色があるそうです。",
    )
    out += b.p(
        "メンバーは、分からないことはサポーターの人にSNSで聞いてみてほしいと話していました。",
        "サッカーのファンとトラジャのファンが、いっしょに楽しめるようにというお願いでした。",
    )

    # ---- 立ち上がった場面
    out += b.h2("松田元太が紙を持って立ち上がったのはなぜ？")
    out += b.mini(
        ("時間", "アーカイブの8分50秒ごろ"),
        ("何が起きた", "松田元太が紙を持って立ち上がり、まわりが大あわて"),
        ("止めた人", "七五三掛龍也"),
        ("紙の中身", "発表されていない(まだ秘密の企画とみられる)"),
    )
    out += fig("tj_jb_inrai_1119_standup")
    out += b.p(
        "CDの発売延期の話をしていた8分50秒ごろ、松田さんが紙を手に急に立ち上がりました。",
        "紙を頭の上でひらひらとかかげると、メンバーは「やべえ！やべえ！」と大さわぎになります。",
    )
    out += fig("tj_jb_inrai_1119_standup2")
    out += b.p(
        "すぐに七五三掛さんが立ち上がって、松田さんを止めに行きました。",
        "9分20秒ごろには松田さんも座り直し、手もとで紙を見ている様子が映っています。",
    )
    out += b.p(
        "座ったあとは、「まだサプライズしたい部分あるからね」「頑張って作ったもん」という声が聞こえます。",
        "CDの発売までに向けて準備している、まだ発表前の企画の紙だったとみられます。",
        "紙の中身は配信では見えず、何の企画かは分かっていません。",
    )
    out += b.p(
        "発売が延びたぶん、何かしかけを用意してくれているのかもしれません。",
        "続報が出たら、この記事に追記します。",
    )

    # ---- まとめ
    out += b.h2("まとめ")
    out += b.checks([
        "2026年11月19日の7人のインスタライブはアルバム配信開始の記念",
        "松倉海斗のエンジ色のニット帽とグレーのパーカーはCELINE",
        "宮近海斗の黒スウェットはUmbro(型番は未特定)",
        "中村海人のビーニーはCHANELのBeanie Cashmereとみられる",
        "川島如恵留のジャージは中村海人デザインのオリジナル(メンカラの白)",
        "松田元太・吉澤閑也・七五三掛龍也の服はブランド未特定",
        "8分50秒ごろ、松田元太が紙を持って立ち上がり、止められた(まだ発表前の企画の紙とみられる)",
    ])
    out += b.p(
        "7人それぞれの好みが出ていて、並ぶとファッションショーのような配信でした。",
        "松田さんの紙の中身も気になるので、CD発売までの続報を楽しみに待ってみてはいかがでしょうか！",
    )
    out += b.html(
        '<div style="border:1px solid #b39ddb;border-left:4px solid #7e57c2;background:#f5f2fb;padding:1em 1.2em;margin:1.5em 0;">'
        '<p style="font-weight:bold;margin:0 0 .5em;">あわせて読みたい</p><ul style="margin:0;">'
        '<li><a href="{0}">松田元太のインスタライブのジャージはどこの？中村海人デザインと判明！</a></li>'
        '<li><a href="{1}">千賀健永の配信で中村海人が被ってたビーニーはCHANEL？</a></li>'
        '<li><a href="{2}">松倉海斗の黒ニットパーカーはどこの？セリーヌと判明！</a></li>'
        '<li><a href="{3}">Jewelry Basket配信開始！MVのジュニア14人は誰？</a></li>'
        '<li><a href="{4}">トラジャ大阪駅広告はなぜ1日で終了？道頓堀・渋谷はいつまで？</a></li>'
        '</ul></div>'.format(U_JERSEY, U_CHANEL_SENGA, U_MATSU_CELINE, U_DIGITAL, U_JEWELHUNT))
    return out


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("タイトル文字数(【未】抜き):", len(blogkit.strip_mi(TITLE)))
    if "--build-only" in sys.argv:
        for k, alt in NEW_MEDIA.items():
            MEDIA.setdefault(k, {"url": "images/tj_jb_reel_1120/" + k + ".jpg", "alt": alt})
    else:
        ensure_media()
    out = ab.NOTICE + "\n\n" + blogkit.finalize(build(), SITE, NAMES)
    if "--build-only" in sys.argv:
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
