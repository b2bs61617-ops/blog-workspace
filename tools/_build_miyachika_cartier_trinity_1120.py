# -*- coding: utf-8 -*-
"""chomoand-4.blog: 宮近海斗が『トーキング千鳥！』(2026-11-19放送)で着けていたゴールドのネックレス
= カルティエ「トリニティ クッション」ペンダントとみられる(2026-11-20)。

根拠: articles/miyachika_cartier_trinity_1120_research.md
- 放送: 2026/11/19(木)21:40〜 TBS『トーキング千鳥！』第3弾「先輩後輩言いたい放題SP」(THE FIRST TIMES)
- TVer https://tver.jp/episodes/epuygh6p2x の3:38付近のフレーム(neck_c8 / c_8)
- 番組公式X 11/17 アフタートーキング動画(af_crop_055)
- 商品: カルティエ公式 トリニティ一覧(CRB7224955 ¥638,000)・商品ページ(3色ゴールド、リング3.8mm×1.3mm、
  チェーン50/60cm、1924年ルイ・カルティエ考案)
- 3色の意味は公式ページで確認できず → 「よく紹介される」書き方。色との対応は書かない。
- 刻印は見えないので断定しない(有力)。私物かスタイリスト用意かは不明。
- 7月の着用・青い名札の写真・ファンの特定投稿は使わない。
- 11/19インスタライブ(Umbroスウェット)は首元が見えず確認できない。インライ私服記事は下書きなのでリンクしない。
"""
import json
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
import affiliate_box as ab  # noqa: E402

SITE = "travis"
KEY = "miyachika_cartier_trinity_1120"
TITLE = "【未】【トーキング千鳥】宮近海斗のネックレスはカルティエのトリニティ？"
SLUG = "miyachika-kaito-talking-chidori-cartier-trinity-necklace"
CATEGORIES = [3]
NAMES = ["ジェシー", "津田篤宏"]
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch_canva.jpg")
EYECATCH_ALT = "宮近海斗のカルティエのトリニティのネックレス"

IMG_DIR = blogkit.ROOT / "images" / "miyachika_trinity_1120"
MEDIA_JSON = IMG_DIR / "media.json"
MEDIA = json.loads(MEDIA_JSON.read_text(encoding="utf-8")) if MEDIA_JSON.exists() else {}
NEW_MEDIA = {
    "tc_miyachika_trinity_neck": "宮近海斗の胸元のゴールドのネックレスのアップ",
    "tc_miyachika_trinity_scene": "トーキング千鳥でストライプシャツに黒いジャケットを着た宮近海斗",
    "tc_miyachika_trinity_after": "アフタートーキングの動画に映る宮近海斗のネックレス",
}

TVER = "https://tver.jp/episodes/epuygh6p2x"
X_AFTER = "https://x.com/talking_chidori/status/2122615744424730970"
NEWS = "https://www.thefirsttimes.jp/?p=917518"
CARTIER_LIST = "https://www.cartier.com/ja-jp/jewellery/collections/trinity/"
CARTIER_ITEM = ("https://www.cartier.com/ja-jp/jewellery/necklaces/trinity/"
                "%E3%83%88%E3%83%AA%E3%83%8B%E3%83%86%E3%82%A3-%E3%82%AF%E3%83%83%E3%82%B7%E3%83%A7%E3%83%B3-"
                "%E3%83%98-%E3%83%B3%E3%82%BF-%E3%83%B3%E3%83%88--CRB7224955")
CARTIER_US = "https://www.cartier.com/en-us/jewelry/necklaces/trinity/trinity-necklace-CRB7224955.html"

U_RING = "https://chomoand-4.blog/miyachika-ego-ring-tom-wood-pave-signet-1512"
U_SACAI = "https://chomoand-4.blog/miyachika-sacai-know-future-tee-1400"
U_DIOR = "https://chomoand-4.blog/where-are-kaito-miyachikas-sun-982"
U_BALENCIAGA = "https://chomoand-4.blog/where-did-kaito-miyachika-get-965"
U_SENPAI = "https://chomoand-4.blog/miyachika-kaito-senpai-inohara-yara-1773"

_K = ab.load_keys()
_TAG = _K.get("AMAZON_ASSOCIATE_TAG", "")


def rk(q):
    s = "https://search.rakuten.co.jp/search/mall/" + urllib.parse.quote(q) + "/"
    return ("https://hb.afl.rakuten.co.jp/hgc/{}/?pc=".format(_K["RAKUTEN_AFFILIATE_ID"])
            + urllib.parse.quote(s, safe="") + "&m=" + urllib.parse.quote(s, safe=""))


def amz(q):
    return "https://www.amazon.co.jp/s?k=" + urllib.parse.quote(q) + ("&tag=" + _TAG if _TAG else "")


# 宮近海斗(赤→パステル)
b = blogkit.Blocks("#ef9a9a", "#f3d6d6", "#fdf3f3")
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


def fig(k, src, w=360):
    m = MEDIA[k]
    return b.html(
        '<figure class="wp-block-image size-large"><img src="{0}" alt="{1}" '
        'style="max-width:{3}px;width:100%;height:auto;display:block;margin:0 auto;">'
        '<figcaption style="font-size:0.8em;color:#888;text-align:center;">{2}</figcaption></figure>'
        .format(m["url"], m["alt"], '出典：<a href="{0}" target="_blank" rel="noopener">{0}</a>'.format(src), w))


def build():
    out = ""

    # ---- リード
    out += b.p(
        "11月19日の『トーキング千鳥！』で、宮近海斗の胸元に光っていたゴールドのネックレスが気になった人も多いのではないでしょうか。",
        "細いチェーンの先に、ころんとした小さなチャームが1つだけ付いたデザインでした。",
    )
    out += b.p(
        "映像をアップにして見くらべると、" + b.mark("カルティエの「トリニティ クッション」ペンダントとみられます") + "。",
        "日本の定価は638,000円(税込)です。",
        "この記事では、番組の情報と、トリニティと言える理由、商品の値段や由来をまとめます。",
    )
    out += b.mini(
        ("番組", "TBS『トーキング千鳥！』先輩後輩言いたい放題SP"),
        ("放送日", "2026年11月19日(木)21時40分〜"),
        ("ネックレス", "カルティエ「トリニティ クッション」ペンダントとみられる"),
        ("定価", "638,000円(税込)"),
    )
    out += b.wakaru([
        "宮近海斗が出た『トーキング千鳥！』の放送内容",
        "ネックレスがトリニティと言える理由",
        "トリニティ クッションの型番・素材・値段",
        "トリニティの由来と3色のゴールド",
        "ネックレスの合わせ方",
        "ほかの場面で着けていたか",
    ])

    # ---- 番組
    out += b.h2("宮近海斗がネックレスを着けていたのはトーキング千鳥")
    out += b.mini(
        ("放送", "2026年11月19日(木)21時40分〜 TBS系"),
        ("企画", "第3弾「有名人 先輩後輩言いたい放題SP」"),
        ("ペア", "先輩ジェシー(SixTONES)と後輩の宮近海斗"),
        ("見逃し配信", "TVer(11月19日22時57分ごろから配信)"),
    )
    out += b.p(
        "ネックレスが映ったのは、2026年11月19日(木)にTBS系で放送された『トーキング千鳥！』です。",
        "千鳥の2人が、有名人の「先輩と後輩」のペアに本音を聞いていく企画の第3弾でした。",
    )
    out += b.p(
        "宮近さんは、同じ事務所の先輩であるSixTONESのジェシーさんとペアで出演しました。",
        "画面には「付き合い歴16年！」というテロップも出ていて、長い付き合いの2人です。",
    )
    out += fig("tc_miyachika_trinity_scene", TVER, 560)
    out += b.p(
        "「先輩後輩にいくらまで貸せる？」という質問では、ジェシーさんの答えが「500万円」でした。",
        "このとき宮近さんの胸元がしっかり映り、ネックレスがよく見えています。",
    )
    out += b.p(
        "放送は、TVerで見逃し配信されています。",
        "ネックレスが映るのは、配信の3分40秒ごろの「500万円」の場面です。",
    )
    out += b.html('<p style="font-size:0.9em;">' + L(TVER, "TVer『トーキング千鳥』先輩後輩言いたい放題SP")
                  + "<br>" + L(NEWS, "番組の内容を伝えるニュース(THE FIRST TIMES)") + "</p>")
    out += b.p(
        "放送の2日前の11月17日には、番組公式Xで収録のあとの「アフタートーキング！」動画が出ています。",
        "宮近さんとジェシーさん、ダイアンの津田篤宏さんの3人が話す動画で、ここでも同じネックレスが映っていました。",
    )
    out += b.xembed(X_AFTER)
    out += fig("tc_miyachika_trinity_after", X_AFTER)
    out += b.p(
        "服もネックレスも本番と同じなので、収録の日に着けていた物とみられます。",
    )

    # ---- なぜトリニティ
    out += b.h2("宮近海斗のネックレスはカルティエのトリニティ？")
    out += b.mini(
        ("答え", "トリニティ クッション ペンダントとみられる(有力)"),
        ("近い点", "チャームの形・ゴールドの色味・細いチェーン"),
        ("分からない所", "刻印・ロゴは映像で読めず、私物かどうかも不明"),
    )
    out += fig("tc_miyachika_trinity_neck", TVER)
    out += b.p(
        "胸元をアップにすると、細いゴールドのチェーンの先に小さなチャームが1つ下がっています。",
        "白いタンクトップの上で、チャームがきらっと光っているのが分かります。",
    )
    out += b.p(
        "このネックレスをカルティエの「トリニティ クッション」とみる理由は、次の3つです。",
    )
    out += b.table(("見る所", "宮近海斗のネックレス", "トリニティ クッション"), [
        ("チャームの形", "角が丸い四角のような、ふっくらした形", "3本のリングを角の丸い四角に組んだ形"),
        ("色", "金色の中に白っぽい色がまじる", "イエロー・ピンク・ホワイトの3色のゴールド"),
        ("大きさ", "鎖骨のあいだに収まる小ぶりなチャーム", "チャーム全体の大きさは公式に記載なし"),
    ])
    out += b.h3("チャームの形がクッション型")
    out += b.p(
        "トリニティは、3本のリングがからみ合ったデザインです。",
        "ふつうのトリニティはリングが丸いのですが、「クッション」はリングが角の丸い四角になっています。",
    )
    out += b.p(
        "宮近さんのチャームも、丸い輪がゆらゆらしている形ではありませんでした。",
        "ころんとかたまりのように見える形で、クッション型の特ちょうと合っています。",
    )
    out += b.h3("金色の中に白っぽい色が見える")
    out += b.p(
        "チャームをよく見ると、金色の中に、白っぽく光る部分がまじっています。",
        "トリニティはイエロー・ピンク・ホワイトの3色のゴールドを組み合わせているので、色の見え方も一致します。",
        "3色のゴールドと考えると、この見え方の説明がつきます。",
    )
    out += b.h3("小ぶりなサイズと細いチェーン")
    out += b.p(
        "チャームは、宮近さんの鎖骨のあいだに収まるくらいの小ささです。",
        "トリニティ クッション ペンダントも小ぶりなデザインで、公式ではリング1本の長さが3.8mmと書かれています。",
        "チェーンもイエローゴールドの細い物で、映像の見た目とよく似ています。",
    )
    out += b.p(
        "ただし、映像ではチャームの刻印やロゴまでは読めません。",
        "そのため、この記事では「トリニティ クッションとみられる」としています。",
        "番組の衣装として用意された物か、宮近さんの私物かも分かっていません。",
    )

    # ---- スペック
    out += b.h2("トリニティ クッション ペンダントの値段はいくら？")
    out += b.mini(
        ("値段", "638,000円(税込・日本の定価)"),
        ("型番", "B7224955"),
        ("購入先", "カルティエのブティック・公式オンラインストア"),
    )
    out += b.table(("項目", "内容"), [
        ("商品名", "トリニティ クッション ペンダント"),
        ("型番", "B7224955(公式サイトの表記はCRB7224955)"),
        ("素材", "ホワイト・ピンク・イエローゴールド(各750)"),
        ("チェーン", "イエローゴールド750、長さ50cmか60cm"),
        ("リングの大きさ", "長さ3.8mm・幅1.3mm"),
        ("日本の定価", "638,000円(税込)"),
        ("アメリカの値段", "3,900ドル(60cm、1ドル=155円で約60万円)"),
    ])
    out += b.p(
        "カルティエ公式サイトのトリニティの一覧では、このペンダントは638,000円(税込)で出ています。",
        "チェーンの長さは、50cmと60cmから選べます。",
    )
    out += b.p(
        "宮近さんのチェーンは、白いタンクトップのえりより少し下にチャームが来る長さでした。",
        "どちらの長さかは、映像からは決められません。",
    )
    out += b.p(
        "2026年11月20日に見たときは、公式オンラインストアで「在庫がございません」の表示でした。",
        "ほしい人は、カルティエのブティックに問い合わせるのが確実です。",
    )
    out += b.html('<p style="font-size:0.9em;">購入先:' + L(CARTIER_ITEM, "カルティエ公式の商品ページ")
                  + '<br>参考:' + L(CARTIER_LIST, "トリニティの一覧")
                  + '<br>参考:' + L(CARTIER_US, "アメリカの公式ページ") + "</p>")
    out += b.p(
        "同じトリニティのペンダントには、丸いリングのミニ(308,000円)やスモール(412,500円)もあります。",
        "どれも丸いリングの形なので、宮近さんのふっくらしたチャームとはちがう形です。",
    )
    out += ab.build_box(rk("カルティエ トリニティ クッション ネックレス"), None,
                        "カルティエ トリニティ クッション ペンダント",
                        amz("カルティエ トリニティ クッション ネックレス"),
                        note="楽天・Amazonの検索結果です(中古・並行輸入品もあるので、型番と状態を確かめてください)",
                        border="#f3d6d6")
    out += "\n"

    # ---- 由来
    out += b.h2("カルティエのトリニティとは？3色のゴールドの意味")
    out += b.mini(
        ("誕生", "1924年、ルイ・カルティエが考えたリングが始まり"),
        ("デザイン", "3色のゴールドのリングが3本からみ合う形"),
        ("よく言われる意味", "「愛」「友情」「忠誠」"),
    )
    out += b.p(
        "トリニティは、カルティエを代表するジュエリーのシリーズです。",
        "公式サイトによると、始まりは1924年にルイ・カルティエが考えた指輪でした。",
    )
    out += b.p(
        "3本のリングが、からみ合いながらなめらかに動くのが特ちょうです。",
        "2024年に100周年をむかえ、今もリングやネックレスが作られています。",
    )
    out += b.p(
        "3色のゴールドは、「愛」「友情」「忠誠」の3つを表すと紹介されることが多いです。",
        "どの色がどの意味かは紹介によってちがい、公式サイトの説明では確かめられませんでした。",
        "大切な人とのつながりを思わせるデザインです。",
    )
    out += b.p(
        "16年の付き合いの先輩と出た回に、つながりを表すジュエリーを着けていたのも、すてきな偶然ですね。",
    )

    # ---- 合わせ方
    out += b.h2("宮近海斗のネックレスの合わせ方")
    out += b.mini(
        ("トップス", "白いタンクトップ+水色のストライプシャツ"),
        ("アウター", "黒いジャケット(白いスナップボタン)"),
        ("ポイント", "シャツのえりを大きく開けて、ネックレスを見せる"),
    )
    out += b.p(
        "この日の宮近さんは、白いタンクトップの上に水色のストライプのシャツを着ていました。",
        "シャツのボタンを大きく開けて、えりを外に出した着こなしです。",
    )
    out += b.p(
        "その上に、白いスナップボタンの黒いジャケットをはおっていました。",
        "白いタンクトップが下地になるので、細いゴールドのチェーンがはっきり見えます。",
        "耳には小さなゴールドのピアスも合わせて、金色でそろえていました。",
    )
    out += b.p(
        "ネックレスを主役にしたいときは、白い無地のインナーを合わせるとまねしやすいです。",
    )
    out += b.p(
        "宮近さんのアクセサリーは、" + L(U_RING, "EGOのMVで着けていたTOM WOODの指輪の記事") + "でも紹介しています。",
        "ここでもゴールドのアクセサリーを選んでいて、金色が好きなのかもしれません。",
    )

    # ---- 他の場面
    out += b.h2("宮近海斗はほかの場面でもトリニティを着けていた？")
    out += b.mini(
        ("11月17日", "番組公式Xのアフタートーキング動画で同じネックレス"),
        ("11月19日", "放送当日のインスタライブは首元が見えず確認できない"),
    )
    out += b.p(
        "同じネックレスがはっきり映っているのは、『トーキング千鳥！』の本番と、アフタートーキングの動画です。",
        "どちらも同じ日の収録とみられます。",
    )
    out += b.p(
        "放送当日の11月19日には、Travis Japanの7人でインスタライブも行いました。",
        "このときの宮近さんは、首元のつまった黒いスウェットを着ていました。",
        "ネックレスが服にかくれていて、トリニティを着けていたかは確かめられませんでした。",
    )
    out += b.p(
        "ほかの番組やSNSで着けている姿が分かったら、この記事に追記します。",
    )

    # ---- まとめ
    out += b.h2("まとめ")
    out += b.checks([
        "宮近海斗がネックレスを着けていたのは、2026年11月19日(木)放送の『トーキング千鳥！』",
        "先輩ジェシーとの「先輩後輩言いたい放題SP」で、TVerでも見られる",
        "ネックレスはカルティエ「トリニティ クッション」ペンダント(B7224955)とみられる",
        "形と色味が近い、刻印は映像で読めない",
        "日本の定価は638,000円(税込)、チェーンは50cmか60cm",
        "トリニティは1924年生まれ、3色は「愛」「友情」「忠誠」と紹介されることが多い",
        "11月19日のインスタライブは首元が見えず確認できない",
    ])
    out += b.p(
        "16年来の先輩との共演で、さりげなくトリニティを着けていた宮近さん、大人っぽくてすてきでした。",
        "TVerの3分40秒ごろで胸元が見られるので、もう一度チェックしてみてはいかがでしょうか！",
    )
    out += b.html(
        '<div style="border:1px solid #f3d6d6;border-left:4px solid #ef9a9a;background:#fdf3f3;padding:1em 1.2em;margin:1.5em 0;">'
        '<p style="font-weight:bold;margin:0 0 .5em;">あわせて読みたい</p><ul style="margin:0;">'
        '<li><a href="{0}">【EGO】宮近海斗の指輪はどこの？TOM WOODとみられるゴールドリング！</a></li>'
        '<li><a href="{1}">【観劇私服】宮近海斗の黒Tシャツはどこの？sacaiと判明！</a></li>'
        '<li><a href="{2}">宮近海斗のサングラスはどこの？ディオールのDiorTagと判明！</a></li>'
        '<li><a href="{3}">【御殿場】宮近海斗が買ったTシャツはどこの？バレンシアガと判明！</a></li>'
        '<li><a href="{4}">宮近海斗の憧れの先輩は誰？井ノ原快彦と屋良朝幸！</a></li>'
        '</ul></div>'.format(U_RING, U_SACAI, U_DIOR, U_BALENCIAGA, U_SENPAI))
    return out


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("タイトル文字数(【未】抜き):", len(blogkit.strip_mi(TITLE)))
    if "--build-only" in sys.argv:
        for k, alt in NEW_MEDIA.items():
            MEDIA.setdefault(k, {"url": "images/miyachika_trinity_1120/" + k + ".jpg", "alt": alt})
    else:
        ensure_media()
    out = ab.NOTICE + "\n\n" + blogkit.finalize(build(), SITE, NAMES)
    if "--build-only" in sys.argv:
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
