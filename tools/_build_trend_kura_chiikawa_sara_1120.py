# -*- coding: utf-8 -*-
"""chomoand.com下書き「くら寿司ちいかわ皿の抽選はいつ？応募方法と受け取り方は？」(2026-11-20 ユカ依頼、Xトレンドから)。

根拠: くら寿司公式 https://www.kurasushi.co.jp/topic/009011.html (案内画像261119chiikawa_LP_B.jpgの文字を読んだ)、
公式X @mutenkurasushi 11/19、ちいかわ公式X 8/10(コラボ告知画像)、グルメWatch 11/19、Yahoo!ニュース(オタク総研)11/20
(9/5不正判明・9/6中止、元は税込3,000円ごと先着、メルカリ11/27〜12/10出品禁止)。
飲食が必要かは公式に書いていない → 「案内には書かれていない」と書く。

    python3 tools/_build_trend_kura_chiikawa_sara_1120.py                # 下書き投稿
    python3 tools/_build_trend_kura_chiikawa_sara_1120.py --build-only
    python3 tools/_build_trend_kura_chiikawa_sara_1120.py --update
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "trend"
KEY = "trend_kura_chiikawa_sara_1120"
TITLE = "くら寿司ちいかわ皿の抽選はいつ？応募方法と受け取り方は？"
SLUG = "kurasushi-chiikawa-sushizara-line"
CATEGORIES = [37]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "くら寿司ちいかわ皿の抽選はいつ？"
X_TEXT = ""
X_TAGS = "#ちいかわ #くら寿司"

OFFICIAL = "https://www.kurasushi.co.jp/topic/009011.html"
X_KURA = "https://x.com/mutenkurasushi/status/2123219714029576479"
X_KOUHOU = "https://x.com/chiikawa_kouhou/status/2086618535766491395"
GOURMET = "https://gourmet.watch.impress.co.jp/docs/news/2157822.html"
YAHOO = "https://news.yahoo.co.jp/articles/aa99c634617768646b2cde25a7cb85b0fbdf5522"
MEDIA_CACHE = blogkit.ARTICLES / (KEY + "_media.json")
PHOTOS = {
    "collab": (blogkit.ROOT / "images" / (KEY + "_collab.jpg"), "ちいかわ×くら寿司コラボキャンペーンの告知画像", X_KOUHOU),
    "plates": (blogkit.ROOT / "images" / (KEY + "_plates.jpg"), "ちいかわオリジナル寿司皿 全4種", OFFICIAL),
}

b = blogkit.Blocks("#db2777", "#f9c6dc", "#fff4f8")
p, h2, h3, mk, L = b.p, b.h2, b.h3, b.mark, b.link


def photo(key):
    import json
    path, alt, src_url = PHOTOS[key]
    if "--build-only" in sys.argv:
        src, w, h = "x", 1200, 675
    else:
        cache = json.loads(MEDIA_CACHE.read_text(encoding="utf-8")) if MEDIA_CACHE.exists() else {}
        if key not in cache:
            wp = blogkit.WP(SITE)
            mid = wp.upload_media(str(path), alt)
            cache[key] = wp.get("/media/{}".format(mid))
            MEDIA_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        m = cache[key]
        big = m["media_details"].get("sizes", {}).get("large") or {
            "source_url": m["source_url"], "width": m["media_details"]["width"], "height": m["media_details"]["height"]}
        src, w, h = big["source_url"], big["width"], big["height"]
    return b.html('<figure class="wp-block-image size-large"><img src="{}" alt="{}" width="{}" height="{}" '
                  'style="max-width:100%;height:auto;"><figcaption style="font-size:0.8em;color:#888;">'
                  '出典:<a href="{}" target="_blank" rel="noopener">{}</a></figcaption></figure>'
                  .format(src, alt, w, h, src_url, src_url))


out = ""

out += p("9月に配られるはずだった、くら寿司の「ちいかわ」寿司皿。",
         "中止になってから約2か月、ついに配り方が決まりました。")
out += p("結論から言うと、" + mk("抽選は11月25日(水)11時から12月6日(日)20時まで") + "です。",
         "お店ごとの公式LINEで応募して、当たった人だけがお店でお皿をもらえます。")
out += p("この記事では、応募のやり方と受け取り方を順番にまとめました。",
         "「絵柄は選べる？」「食事は必要？」といった疑問にも答えていきます。")
out += b.mini(("抽選期間", "2026年11月25日(水)11時〜12月6日(日)20時"),
              ("引き換え期間", "2026年11月27日(金)〜12月6日(日)、毎日11時〜20時"),
              ("当たる人数", "全国で100万名(なくなり次第終了)"),
              ("景品", "ちいかわオリジナル寿司皿(全4種)"),
              ("応募方法", "受け取りたいお店のくら寿司公式LINEから"))
out += b.wakaru([
    "ちいかわ寿司皿の抽選期間と引き換え期間",
    "LINEでの応募のやり方",
    "当たったときの受け取り方",
    "絵柄は選べるのか・食事は必要なのか",
    "9月に配布が中止になった理由",
])

out += h2("くら寿司ちいかわ寿司皿の抽選はいつ？")
out += b.mini(("答え", "抽選は11/25(水)11時〜12/6(日)20時、受け取りは11/27(金)〜12/6(日)"))
out += p("くら寿司は11月19日(木)、公式サイトと公式Xで配り方を発表しました。",
         "前は先着順の予定でしたが、今回は" + mk("お店ごとのLINE抽選") + "に変わっています。")
out += b.xembed(X_KURA)
out += b.table(("やること", "期間"), [
    ("LINEで抽選に参加", "11/25(水)11時〜12/6(日)20時"),
    ("お店で受け取る", "11/27(金)〜12/6(日) 11時〜20時"),
])
out += p("気をつけたいのは、" + mk("お店ごとに当たる数が決まっている") + "ことです。",
         "その数に届いたお店は、12月6日を待たずに抽選が終わります。",
         "確実に参加したいなら、11月25日の早めの時間に応募しておくのが安心です。")
out += p("当たる人は全国のくら寿司を合わせて100万名です。",
         "1店舗あたり何人当たるかは、公表されていません。")

out += h2("ちいかわ寿司皿はどんなデザイン？全4種を紹介")
out += b.mini(("答え", "ちいかわ・ハチワレ・うさぎ・みんなの4種類"))
out += photo("plates")
out += p("お皿は全部で4種類あり、どれもくら寿司の制服を着たデザインです。",
         "ふちには「CHIIKAWA × KURASUSHI」の文字が入っています。")
out += b.table(("番号", "絵柄", "色"), [
    ("1", "ちいかわ(お寿司を持っている)", "ピンク"),
    ("2", "ハチワレ(お寿司を持っている)", "水色"),
    ("3", "うさぎ(お皿を重ねて持っている)", "オレンジ"),
    ("4", "みんな(ちいかわたちが集合)", "ブラウン"),
])
out += p("お皿には「NOT FOR SALE(非売品)」と書かれています。",
         "お店で買うことはできないので、手に入れるには今回の抽選に当たるしかありません。")

out += h2("ちいかわ寿司皿のLINE抽選の応募方法")
out += b.mini(("答え", "お店の公式LINEを友だち追加→ホームの「抽選参加画面」から参加"))
out += h3("ステップ1 受け取りたいお店のLINEを友だち追加する")
out += p("くら寿司は、お店ごとに公式LINEのアカウントがあります。",
         "まずは" + mk("お皿を受け取りに行きたいお店") + "のLINEを友だち追加しましょう。")
out += p("前から友だち追加しているお店でも、そのまま参加できます。",
         "ただし、そのLINEをブロックしていると抽選の対象外になるので注意してください。")
out += h3("ステップ2 ホームタブから「抽選参加画面」を開く")
out += p("友だち追加したら、そのお店のLINEのホームタブを押します。",
         "「抽選参加画面」が出てくるので、そこから抽選に参加します。")
out += h3("ステップ3 当たるとクーポンが出る")
out += p("当たった場合は、その場でクーポンが表示されます。",
         mk("はずれの場合は、クーポンは表示されません。"),
         "結果はLINEの画面で分かるので、参加したら画面をよく見ておきましょう。")
out += p("当選クーポン1枚で、お皿1枚と引き換えられます。",
         "応募は1店舗にしてほしいと、くら寿司はお願いしています。")

out += h2("ちいかわ寿司皿の受け取り方は？")
out += b.mini(("答え", "当たったお店で、LINEのクーポン画面を店員さんに見せる"))
out += p("引き換え期間中に、当たったお店へ行きます。",
         "店員さんにスマホのクーポン画面を見せて、確認してもらったら「使用済みにする」を押します。")
out += p("受け取るときの注意点は、次のとおりです。")
out += b.checks(["当たったお店でしか受け取れない(ほかのお店では引き換え不可)",
                 "スクリーンショットなど画像を見せても引き換えできない",
                 "当たったLINEアカウントの画面でしか使えない",
                 "先に自分で「使用済み」を押すと無効になる",
                 "引き換えは毎日11時〜20時、期間外は受け取れない"])
out += p("とくに、" + mk("スクリーンショットではダメ") + "という点は忘れがちです。",
         "家族のスマホで当たった場合は、そのスマホを持ってお店に行く必要があります。")
out += h3("お店の前で並ぶのはNG")
out += p("くら寿司は、引き換えが始まる前からお店の前で待ったり並んだりしないよう呼びかけています。",
         "当たった人には、期間中に順番に渡すとしています。")

out += h2("ちいかわ寿司皿の絵柄は選べる？食事は必要？")
out += h3("絵柄は選べないこともある")
out += p("公式の案内では、お店の在庫によって" + mk("希望の絵柄を選べない場合がある") + "とされています。",
         "来たお客さんから順番に渡すので、遅い時間だと人気の絵柄がなくなっているかもしれません。")
out += p("どうしても欲しい絵柄があるなら、引き換え期間の早い日に行くのがおすすめです。",
         "ただし、前に書いたとおり開店前から並ぶのは控えましょう。")
out += h3("食事が必要とは書かれていない")
out += p("前の配り方は「お会計3,000円(税込)ごとに1枚」でした。",
         "今回の案内には、" + mk("お皿を受け取るのに食事が必要とは書かれていません。"))
out += p("クーポンを見せて受け取る流れなので、引き換えだけでも大丈夫そうです。",
         "せっかくお店に行くなら、お寿司を食べて帰るのもいいですね。")

out += h2("ちいかわ寿司皿は9月になぜ中止になった？")
out += b.mini(("答え", "従業員の不正がわかり、9月6日からコラボ全体が中止に"))
out += p("くら寿司と「ちいかわ」のコラボは、2026年8月21日(金)から始まりました。",
         "寿司皿は、9月18日(金)からお会計3,000円ごとに先着で配る予定でした。")
out += photo("collab")
out += p("ところが、コラボの景品がフリマアプリにたくさん出品されているとSNSで話題になりました。",
         "くら寿司が調べたところ、9月5日(土)に従業員の不正がわかったと発表しています("
         + L(YAHOO, "Yahoo!ニュース") + ")。")
out += p("そして9月6日(日)から、コラボのキャンペーン全体が中止になりました。",
         "このとき寿司皿は配られる前だったので、ずっと「お皿はどうなるの？」と待つ声が続いていました。")
out += b.table(("日付", "できごと"), [
    ("8/21(金)", "ちいかわコラボがスタート"),
    ("9/5(土)", "従業員の不正がわかったと発表"),
    ("9/6(日)", "コラボのキャンペーンを中止"),
    ("11/19(木)", "寿司皿をLINE抽選で配ると発表"),
    ("11/25(水)", "LINE抽選スタート"),
])
out += h3("メルカリは寿司皿の出品を一時禁止に")
out += p("転売を防ぐため、メルカリは11月27日から12月10日まで、この寿司皿の出品を禁止すると発表しました。",
         "くら寿司も、転売目的の応募やクーポンのゆずり渡しを禁止しています。")

out += h2("ちいかわ寿司皿の抽選へのSNSの反応")
out += p("配布が決まったことを喜ぶ声がある一方で、仕組みへの不安や不満も多く見られました。")
out += b.checks(["廃棄されると思っていたので、配ってもらえるだけでうれしい",
                 "LINEのアカウントをいくつも作れば、何回も応募できてしまうのでは",
                 "コラボ中にたくさん食べた人が、優先されないのは残念",
                 "当たったあとに、また朝から並ぶことになるのか心配"])
out += p("複数アカウントについては、公式の案内に細かい決まりは書かれていません。",
         "ただ「1店舗での参加」をお願いしているので、マナーを守って応募したいですね。")

out += h2("まとめ")
out += b.checks(["抽選は11/25(水)11時〜12/6(日)20時、お店ごとの公式LINEから",
                 "当たる数に届いたお店は、期間中でも抽選が終わる",
                 "当たればその場でクーポンが出る(はずれは何も出ない)",
                 "受け取りは11/27(金)〜12/6(日)の11時〜20時、当たったお店だけ",
                 "スクショは不可、絵柄は選べないこともある"])
out += p("一度は中止になったお皿なので、待っていたファンにとってはうれしいニュースですね。",
         "11月25日になったら、行きやすいお店のLINEから忘れずに応募してみてはいかがでしょうか！")
out += p("参考: " + L(OFFICIAL, "くら寿司公式 ちいかわ オリジナル寿司皿 LINE抽選プレゼント！")
         + "/" + L(GOURMET, "グルメWatch"))
# 関連記事(2026-11-20 ユカ指示。WP下書きにはユカの手直しを残したまま末尾に追記済み)
out += b.html('<div style="border:1px solid #f9c6dc;border-left:4px solid #db2777;border-radius:4px;'
              'padding:12px 18px;margin:16px 0;background:#fff4f8;"><p style="margin:0 0 6px 0;font-weight:bold;">関連記事</p>'
              '<ul style="margin:0;padding-left:1.4em;">'
              '<li><a href="https://chomoand.com/chiikawa-clinic-chusen-yoyaku/">ちいかわクリニックの抽選はいつ？予約販売の注意点と会場一覧</a></li>'
              '<li><a href="https://chomoand.com/pasutaraisuke/">パスタライ助の名前の由来は？ハチワレのアカウント名がバズる理由</a></li>'
              '</ul></div>')

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = blogkit.finalize(out, SITE, NAMES)
    if "--publish" in sys.argv:
        import json
        state = json.loads((blogkit.ARTICLES / (KEY + "_posted.json")).read_text(encoding="utf-8"))
        blogkit.publish(SITE, state["post"], X_TEXT, X_TAGS)
    elif "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
