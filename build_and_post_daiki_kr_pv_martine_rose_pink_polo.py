# -*- coding: utf-8 -*-
"""DAIKIが「'KO1KEYZ' (Korean ver.) Performance Video」(wCp_X6CBQS8、10/6公開)で着ていたピンクのポロ
=Martine Rose「OVERSIZED S/S POLO in WASHED PINK」674JE02110(SS26、MC7)。着用者はユーザーがDAIKIと確認(10-12)。
公式ストア: 297ポンド→148.50ポンド、鹿の子・綿100%・ポルトガル製、10-12時点でS・Mに在庫あり。
TOWAのグレー(674JE09059、記事14704)と同じデザインの色違い。省エネのためJP版のみ(KR/ENはあとで)。
"""
from pathlib import Path

import cv2
from PIL import Image

from _mubank1009_helpers import ROOT, WP_URL, wp_upload, img_html, post_draft, make_eyecatch, h2, p, UI

# DAIKI単独記事なのでメンバーカラーの緑(既存DAIKI記事14296と同じ)
ui = UI(AB="#cfe6d6", AL="#3f9a63", BG="#f2f9f4", TH="#e3f1e7", marker="mark_green")

PV = "https://www.youtube.com/watch?v=wCp_X6CBQS8"
PINK = "https://www.martine-rose.com/products/oversized-s-s-polo-in-washed-pink"
TOWA_POLO = "https://chomoand-1.com/?p=14704"  # 下書き。公開時にslugのURLへ差し替え
VIDEO = Path(r"C:\Users\s30se\AppData\Local\Temp\claude\c--Users-s30se-OneDrive--------CHOMO\9f7d6c19-dad5-4a45-b1b7-fe576668dc5f\scratchpad\towa1012\pv\pv.mp4")

JP_REL = [
    ("https://chomoand-1.com/daiki-gimpo-airport-bape-paisley-shark-hoodie-14296", "DAIKIが金浦空港で着ていたBAPEのパーカーの記事"),
    ("https://chomoand-1.com/daiki-gentle-monster-kiko-sunglasses-green-video-11899", "DAIKIのジェントルモンスターのサングラスの記事"),
    ("https://chomoand-1.com/does-daikis-bracelet-match-kinarigoten-11368", "DAIKIのブレスレットの記事"),
    ("https://chomoand-1.com/katodaiki_wiki-538", "DAIKI(加藤大樹)のwiki風プロフィールの記事"),
]


def frame_at(sec):
    cap = cv2.VideoCapture(str(VIDEO))
    cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    ok, fr = cap.read()
    cap.release()
    if not ok:
        raise RuntimeError(f"frame at {sec}s not readable")
    return Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))


img_dir = ROOT / "images"
p_dance = img_dir / "daiki_kr_pv_pink_polo_dance.jpg"
p_close = img_dir / "daiki_kr_pv_pink_polo_closeup.jpg"
frame_at(19.0).save(p_dance, quality=90)
frame_at(118.5).save(p_close, quality=90)
m_dance = wp_upload(p_dance, "image/jpeg")
m_close = wp_upload(p_close, "image/jpeg")
print("MEDIA", m_dance["id"], m_close["id"])

JP_TITLE = "【DAIKI】韓国語版パフォーマンス動画のピンクのポロはどこの？"
JP_SLUG = "daiki-korean-ver-performance-video-martine-rose-pink-polo"

JP_CONTENT = "\n\n".join([
    p("KO1KEYZ(コイキーズ)が10月6日に公開した「KO1KEYZ」(Korean ver.)のPerformance Videoで、DAIKIは目を引くピンクのポロシャツを着ていました。<br>\n"
      "胸に青い「TOTAL」の刺しゅうが入った、サッカーのユニフォームのような1着です。<br>\n"
      "このポロは、<strong>ロンドンのブランド「Martine Rose(マーティン・ローズ)」の「OVERSIZED S/S POLO in WASHED PINK」</strong>です。<br>\n"
      "公式オンラインストアでは、定価297ポンドが<strong>半額の148.50ポンド(1ポンド200円換算で約3万円)</strong>になっています。<br>\n"
      "見分けるポイントや生地、TOWAが着ていたグレーとのちがい、買い方まで順番に紹介します。"),
    ui.infobox("DAIKIが着ていたポロシャツ", [
        ("シーン", "「KO1KEYZ」(Korean ver.) Performance Video(2026年10月6日公開)"),
        ("ブランド", "Martine Rose(マーティン・ローズ)"),
        ("商品名", "OVERSIZED S/S POLO in WASHED PINK"),
        ("品番", "674JE02110"),
        ("シーズン", "2026年春夏(SS26)"),
        ("価格", "定価297ポンド→セール148.50ポンド(約3万円)"),
    ]),
    ui.knowbox("この記事でわかること", ["DAIKIが着ていたポロシャツ", "マーティン・ローズと分かるポイント", "生地とサイズ感", "TOWAのグレーとのちがい", "値段と購入先"]),

    h2("Performance VideoでDAIKIが着ていたポロシャツは？"),
    ui.minibox([("アイテム：", "くすんだピンクに黒い襟のポロシャツ"), ("合わせ方：", "うしろ向きのキャップ+デニム")]),
    p("Performance Videoの舞台は、「KO1KEYZ」の横断幕がかかった学校の体育館です。<br>\n"
      "12人はラグビーシャツやサッカーシャツ風のトップスにデニムを合わせた、スポーツチームのような衣装でそろえています。<br>\n"
      "その中でDAIKIは、グレーのキャップをうしろ向きにかぶり、ピンクのポロで登場しました。"),
    img_html(m_dance, "体育館で踊るDAIKI。ピンクのポロシャツにうしろ向きのキャップ", f"出典：{PV}"),
    p(f"ピンクは少し色あせたような{ui.mark('ウォッシュ加工のピンク', True)}で、黒い襟とのコントラストがはっきりしています。<br>\n"
      "ボーダーや紺・黄色のトップスが多いメンバーの中で、明るいピンクのDAIKIはひと目で見つけられるほど目立っていました。<br>\n"
      "動画の後半、ロッカーの前で1人で踊る場面では、胸のロゴまで大きく映ります。"),

    h2("どうしてマーティン・ローズと分かる？見分けポイントは？"),
    ui.minibox([("ポイント①：", "赤い三角+「martine」のロゴ"), ("ポイント②：", "「MARTINE SPORT」の紋章"), ("ポイント③：", "青い「TOTAL participation」の刺しゅう")]),
    img_html(m_close, "ロッカーの前で踊るDAIKI。胸に赤い三角のロゴ、紋章、青いTOTALの刺しゅう", f"出典：{PV}"),
    ui.barbox("マーティン・ローズの公式の商品と一致したポイント", [
        "<strong>左胸のロゴ</strong>：赤い三角のマークの下に、赤い文字で「martine」",
        "<strong>右胸の紋章</strong>：王冠と「MARTINE」「SPORT」、白黒の縦じまの盾",
        "<strong>胸の刺しゅう</strong>：太い青の「TOTAL」と、その下の弧の中に「participation」",
        "<strong>色と襟</strong>：ウォッシュ加工のピンクに、黒い襟",
    ], ordered=True),
    p(f"この4つが、マーティン・ローズ公式オンラインストアの{ui.mark('「OVERSIZED S/S POLO in WASHED PINK」(品番674JE02110)', True)}とそろって一致しました。<br>\n"
      "公式の説明にも、胸に季節のロゴとスポーツクレスト(紋章)の刺しゅうが入っていると書かれています。<br>\n"
      "紋章の左右にある「20」「07」は、ブランドが生まれた2007年のことです。"),

    h2("生地やサイズ感は？"),
    ui.minibox([("素材：", "綿100%の鹿の子"), ("生産：", "ポルトガル製"), ("シルエット：", "ゆったりしたオーバーサイズ")]),
    p(f"公式の表記によると、素材は{ui.mark('綿100%の鹿の子', True)}で、ポルトガルで作られています。<br>\n"
      "鹿の子は、ポロシャツによく使われる細かい凹凸のある生地で、さらっとした肌ざわりが特徴です。<br>\n"
      "ウォッシュ加工がかかっているので、新品でも何度も洗ったような、こなれた色味になっています。"),
    p("シルエットは身幅が広いオーバーサイズで、公式は「だれでも着られる、ゆったりしたつくり」と紹介しています。<br>\n"
      "サイズ表記はいつものサイズで選んでよいとされているので、大きめに着たい人はふだんのサイズ、すっきり着たい人は1サイズ下がよさそうです。<br>\n"
      "DAIKIもひじが隠れるくらいの袖丈で、ラフに着こなしていました。"),

    h2("TOWAのグレーのポロとはどうちがう？"),
    ui.minibox([("同じところ：", "ロゴ・紋章・TOTALの刺しゅう"), ("ちがうところ：", "色・生地・品番")]),
    p(f"同じPerformance Videoで、TOWAは同じデザインのグレーのボーダー版を着ています。<br>\n"
      f"TOWAのポロの詳しい話は<a href=\"{TOWA_POLO}\">TOWAが音楽中心の日に着ていたマーティン・ローズのポロの記事</a>で紹介しています。<br>\n"
      "ロゴや紋章、「TOTAL」の刺しゅうの位置は同じですが、細かいところはけっこうちがいます。"),
    ui.barbox("ピンクとグレーのちがい", [
        "<strong>色</strong>：DAIKIは無地のウォッシュピンク、TOWAはグレー×黒×白のボーダー",
        "<strong>生地</strong>：ピンクは綿100%の鹿の子、グレーはふわっとしたパイル地(綿85%・ポリエステル15%)",
        "<strong>品番</strong>：ピンクは674JE02110、グレーは674JE09059",
        "<strong>買える場所</strong>：ピンクは公式ストアで買える、グレーは海外のセレクトショップのみ",
    ]),
    p("同じデザインを色ちがいで着せて、2人の衣装にまとまりを出しているのがよく分かります。<br>\n"
      "ペアで着たいファン同士なら、ピンクとグレーで分けるのも楽しそうです。"),

    h2("値段は？どこで買える？"),
    ui.minibox([("定価：", "297ポンド(約5万9,000円)"), ("セール：", "148.50ポンド(約3万円)")]),
    p(f"マーティン・ローズの公式オンラインストアでは、{ui.mark('定価297ポンドが半額の148.50ポンド', True)}になっています。<br>\n"
      "1ポンド200円で計算すると、定価は約5万9,000円、セール価格は約3万円です。<br>\n"
      "2026年10月12日時点では、SとMのサイズに在庫があり、XS・L・XLは売り切れていました。"),
    p("海外の公式ストアからの購入になるので、送料や関税は別にかかります。<br>\n"
      "日本への配送条件や総額は、カートに入れたときの表示で確認してください。<br>\n"
      "セールで残っているサイズは少ないので、気になる人は早めにのぞいてみるのがおすすめです。"),
    ui.barbox("購入先", [
        f'<a href="{PINK}" target="_blank" rel="noopener">マーティン・ローズ公式オンラインストア「OVERSIZED S/S POLO in WASHED PINK」</a>：148.50ポンド(定価297ポンド)、S・Mサイズに在庫あり',
    ]),

    h2("まとめ"),
    ui.summarybox([
        "DAIKIが「KO1KEYZ」(Korean ver.)のPerformance Videoで着ていたのは、マーティン・ローズの「OVERSIZED S/S POLO in WASHED PINK」",
        "品番は674JE02110、2026年春夏のアイテム",
        "決め手は赤い三角のmartineロゴ、MARTINE SPORTの紋章、青いTOTALの刺しゅう",
        "綿100%の鹿の子で、ポルトガル製",
        "TOWAのグレーのボーダー版とは色・生地・品番がちがう色ちがい",
        "公式ストアで148.50ポンド(約3万円)、S・Mに在庫あり",
    ]),
    p("体育館の中で、DAIKIのピンクはひときわ明るく映えていました。<br>\n"
      "半額のうちに、DAIKIとおそろいのピンクのポロを手に入れてみてはいかがでしょうか！"),
    ui.linkbox("DAIKI・KO1KEYZの関連記事", JP_REL),
])

JP_SUMMARY = ("DAIKIが「KO1KEYZ」(Korean ver.)のPerformance Videoで着ていたピンクのポロは、マーティン・ローズの"
              "「OVERSIZED S/S POLO in WASHED PINK」(674JE02110)です。公式ストアで148.50ポンド(定価297ポンド)です。")

JP_EYECATCH_ID = make_eyecatch(
    ["--top", "DAIKIのピンクのポロはどこの？", "--main", "KO1KEYZ", "--bottom", "マーティンローズ！"],
    ROOT / "images" / "daiki_kr_pv_pink_polo_eyecatch.png",
)
print("JP_EYECATCH_ID", JP_EYECATCH_ID)
jp_post = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, "ja", [66, 82, 63], JP_EYECATCH_ID, JP_SUMMARY)
print("JP_POST_ID", jp_post["id"], jp_post["slug"], f"{WP_URL}/?p={jp_post['id']}")
