# -*- coding: utf-8 -*-
"""トラジャ2027ツアー 会場別の双眼鏡のおすすめ倍率(chomoand-4.blog)。2026-11-20 オシリ依頼(元ネタ=@Rentio_oshi 2123662653159809079)。

Rentioの画像・倍率は使わず、各会場のフロアの広さ(公式/推定)と作りから自分で考えた。
  エコパ 85m×49m=4,165㎡(公式 ecopa.jp)/グランディ21 フロア3,740㎡(公式 mspf.jp、縦84.4m×最大51.2mはファンブログの推定)
  大阪城ホール 83.4m×48.2m・マリンメッセ福岡 78.6m×45.6m・真駒内 68m×40m(推定)= perfume-fan-de-oma.blogspot.com 2014/09
  ららアリーナ アリーナ面積3,245㎡(東京ドームシティMICE)/Aichi Sky Expo ホールA 100m×100m(公式、2006記事と同じ)
  横浜アリーナ 1階センター・2階アリーナA〜F 22列・3〜4階スタンド10列(2006記事と同じ)
倍率の目安は量販店・比較サイトの一般的な目安(75m以下8倍以下/100m前後8〜10倍/スタンド後方10〜12倍)。
商品: ビクセン アリーナH+8×21WP(195g)/ATERA II H12×30(422g・8万円前後)。楽天APIはこのPCで403なので検索リンク枠。

    python tools/_build_tj_binoculars_1120.py --build-only
    python tools/_build_tj_binoculars_1120.py              # 下書き投稿
    python tools/_build_tj_binoculars_1120.py --update
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
import affiliate_box as ab  # noqa: E402
import affiliate_linker as al  # noqa: E402

SITE = "travis"
KEY = "tj_binoculars_1120"
TITLE = "トラジャのツアーで双眼鏡は何倍？会場別におすすめを紹介！"
SLUG = "travis-japan-2027-tour-binoculars"
CATEGORIES = [3]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "トラジャ2027ツアー 双眼鏡は何倍？"
X_TEXT = ""
X_TAGS = "#TravisJapan #JewelryBasket"

A_RESULT = "https://chomoand-4.blog/travis-japan-2027-tour-toraku-result-3305"
A_SCHEDULE = "https://chomoand-4.blog/travis-japan-2027-tour-jewelry-basket-schedule-1973"
A_CAPA = "https://chomoand-4.blog/travis-japan-2027-tour-venue-capacity-2006"
A_CHAKUBURO = "https://chomoand-4.blog/travis-japan-seated-block-odds-2159"
ECOPA = "https://www.ecopa.jp/facility/arena/"
GRANDE = "https://www.mspf.jp/grande21/index.php?action=sisetu_shoukai_arena"
PERFUME = "https://perfume-fan-de-oma.blogspot.com/2014/09/blog-post_2.html"
LALA = "https://www.tokyo-dome.co.jp/mice/case5.html"

ACC = "#7e57c2"
b = blogkit.Blocks(ACC, "#d9cdee", "#f5f2fb")
L = b.link
SPON = 'target="_blank" rel="nofollow sponsored noopener"'
_ENV = ab.load_keys()


def amz_url(q):
    return al.build_amazon_search_url(q, _ENV.get("AMAZON_ASSOCIATE_TAG"))


def rk_url(q):
    """楽天APIはこのPCのIPが未許可なので、楽天の検索結果ページへのアフィリエイトリンクにする。"""
    import urllib.parse
    t = urllib.parse.quote("https://search.rakuten.co.jp/search/mall/" + urllib.parse.quote(q) + "/", safe="")
    return "https://hb.afl.rakuten.co.jp/hgc/{}/?pc={}&m={}".format(_ENV["RAKUTEN_AFFILIATE_ID"], t, t)


def box(title, q, note=""):
    return ab.build_box(rk_url(q), None, title, amz_url(q), note=note, border=ACC) + "\n\n"


def related(items):
    lis = "".join('<li style="margin:0 0 6px 0;"><a href="{}">{}</a></li>'.format(u, t) for u, t in items)
    return b.html('<div style="border:2px solid #d9cdee;background:#f5f2fb;border-radius:8px;padding:14px 18px;margin:24px 0;">'
                  '<p style="font-weight:bold;margin:0 0 8px 0;">あわせて読みたい</p>'
                  '<ul style="margin:0;padding-left:1.2em;">' + lis + '</ul></div>')


out = ab.NOTICE + "\n\n"
out += b.p("Travis Japan(トラジャ)の2027年ツアー『Jewelry Basket』。",
           "11月20日にファンクラブ先行の当落が出て、当選した人はもう準備を始めているころです。")
out += b.p("持ち物で迷いやすいのが双眼鏡です。",
           "「何倍を買えばいいの？」「この会場でいる？」という人に向けて、" + b.mark("8会場それぞれのおすすめの倍率") + "をまとめました。")
out += b.wakaru(["双眼鏡の倍率の選び方(席からの距離の目安)",
                 "8会場の広さと、会場ごとのおすすめ倍率",
                 "いちばん双眼鏡がほしい会場はどこか",
                 "8倍・10倍・12倍(防振)のおすすめ",
                 "双眼鏡を使うときのマナー"])

# ---------------------------------------------------------------- 結論
out += b.h2("トラジャのツアーの双眼鏡は何倍？迷ったら8〜10倍")
out += b.p("結論からいうと、今回のツアーは全部アリーナやホールなので、" + b.mark("8倍か10倍") + "があればほとんどの席で困りません。",
           "ドームのように12倍以上が必要になる会場はありません。")
out += b.p("ただ、同じ会場でも席によってステージまでの距離は大きく変わります。",
           "双眼鏡選びの目安は次のとおりです。")
out += b.table(("席の場所", "ステージまで", "おすすめ"),
               [("アリーナの前のほう", "約30mまで", "なくてもOK(持つなら6〜8倍)"),
                ("アリーナの中〜後ろ・スタンドの前", "約30〜60m", "8倍"),
                ("スタンドの後ろのほう", "約60〜100m", "10倍"),
                ("100m前後かそれ以上", "100m前後〜", "10〜12倍(防振)")])
out += b.p("家電量販店や比較サイトでも、「ステージまで75m以下なら8倍以下」「スタンド後方や2階席は10〜12倍」が目安とされています。",
           "倍率が高いほど大きく見えますが、そのぶん手ブレで画面がゆれやすく、見える範囲もせまくなります。")
out += b.p("「大きいほうがいい」と12倍を選ぶと、かえって推しを見つけにくくなることもあります。",
           "手ブレをおさえる防振機能がない双眼鏡なら、10倍までにしておくと安心です。")

out += b.html('<figure class="wp-block-image size-full"><img src="https://chomoand-4.blog/wp-content/uploads/2026/10/travis-japan-tour-2027-jewelry-basket-schedule.png" '
              'alt="Travis Japan Concert Tour 2027 Jewelry Basket ツアー日程" class="wp-image-1971"/>'
              '<figcaption style="font-size:0.8em;color:#888;">出典:Travis Japan公式YouTube「【Travis Japan】4th Anniversary YouTube LIVE」(2026年10月28日配信)</figcaption></figure>')

# ---------------------------------------------------------------- 会場別
out += b.h2("会場別のおすすめ倍率は？8会場を比較")
out += b.p("8会場の広さと、おすすめの倍率をまとめました。",
           "フロアの広さは、会場の公式ページの数字と、ファンが調べた推定の数字です。")
out += b.table(("会場(最大収容人数)", "フロアの広さ", "おすすめ"),
               [("宮城 セキスイハイムスーパーアリーナ(7,063人)", "3,740㎡(公式)", "8倍"),
                ("千葉 ららアリーナ 東京ベイ(11,000人)", "3,245㎡", "8倍(4階は10倍)"),
                ("北海道 真駒内(11,500人)", "約68m×40m(推定)", "8〜10倍"),
                ("静岡 エコパアリーナ(10,000人)", "85m×49m(公式)", "10倍"),
                ("福岡 マリンメッセ福岡A館(15,000人)", "約79m×46m(推定)", "10倍"),
                ("神奈川 横浜アリーナ(17,000人)", "非公表", "10倍"),
                ("大阪 大阪城ホール(16,000人)", "約83m×48m(推定)", "10倍(2階後方は12倍)"),
                ("愛知 Aichi Sky Expo(公表なし)", "ホールA 100m×100m(公式)", "10倍(後方は12倍)")])
out += b.p("出典:" + L(ECOPA, "エコパアリーナ 施設ガイド") + "/" + L(GRANDE, "グランディ・21 施設紹介") + "/" +
           L(LALA, "東京ドームシティ(ららアリーナ 東京ベイ)") + "/推定値は" + L(PERFUME, "Perfumeのファンでおま！") + "の調べ")
out += b.p("収容人数は" + L(A_CAPA, "トラジャ2027ツアー会場のキャパは？") + "でくわしくまとめています。")

out += b.h3("8倍で足りる会場：宮城・千葉・北海道")
out += b.p("宮城のセキスイハイムスーパーアリーナは、最大7,063人と今回いちばんコンパクトな会場です。",
           "スタンド席も客席との距離が近く、ほとんどの席は8倍で十分です。")
out += b.p("千葉のららアリーナ 東京ベイは、2024年にできた新しいアリーナです。",
           "客席がすり鉢のように並んでいて、いちばん上の4階でもステージが近く感じられる作りになっています。",
           "1〜2階なら8倍、4階なら10倍があると表情までしっかり見えます。")
out += b.p("北海道の真駒内は、スケートリンクを中心にした会場で、フロアは約68m×40mと今回の中では短めです。",
           "8倍を基本にして、スタンドの後ろなら10倍があると安心です。")

out += b.h3("10倍がほしい会場：静岡・福岡・横浜")
out += b.p("静岡のエコパアリーナは、フロアが85m×49mと縦に長い会場です。",
           "フロアの後ろのブロックやスタンドの奥はステージから遠くなるので、10倍がおすすめです。")
out += b.p("福岡のマリンメッセ福岡A館は、最大15,000人の大きな会場です。",
           "フロアのアリーナ席は平らなので、後ろのブロックになると前の人の頭でステージが見えにくいこともあります。")
out += b.p("横浜アリーナは最大17,000人と、今回いちばん大きい会場です。",
           "3〜4階のスタンド席はステージを見下ろす形になるので、表情まで見たい人は10倍を持っていきましょう。")

out += b.h3("いちばん双眼鏡がほしい会場：大阪と愛知")
out += b.p("大阪城ホールは、ステージの組み方しだいで最大16,000人が入る会場です。",
           "スタンドが1階と2階に分かれていて、" + b.mark("2階スタンドの後ろはステージから100m近く") + "になる席もあるといわれています。",
           "2階席になったら、10倍か12倍の防振双眼鏡があると安心です。")
out += b.p("愛知のAichi Sky Expoは、ホールAだけで100m×100mある展示場です。",
           "スタンド席がなく、平らな床にイスを並べる会場なので、後ろのブロックはステージから遠いうえに段差もほとんどありません。")
out += b.p("前の人の頭ごしに見ることになるので、モニターだけでなく双眼鏡でメンバーを追えると楽しみ方が変わります。",
           "後ろのブロックなら10〜12倍が目安です。")
out += b.p("大阪は当選率が約29%といちばんの激戦でした(" + L(A_RESULT, "トラジャ2027ツアーの当落倍率は？") + ")。",
           "せっかく当たった公演なので、双眼鏡でしっかり目に焼きつけたいですね。")

# ---------------------------------------------------------------- おすすめ
out += b.h2("トラジャのライブにおすすめの双眼鏡")
out += b.p("コンサート用の双眼鏡は、軽くて小さいものが人気です。",
           "2〜3時間ずっと持つので、重さもチェックしておきましょう。")

out += b.h3("迷ったら8倍：ビクセン アリーナH+8×21WP")
out += b.mini(("倍率", "8倍"), ("重さ", "約195g"), ("特長", "コンサート向けの軽くて小さい双眼鏡。防水"))
out += b.p("ビクセンの「アリーナ」シリーズは、その名のとおりコンサートで使うことを考えた双眼鏡です。",
           "195gと軽いので、ペンライトと持ちかえながらでも疲れにくいのがうれしいポイントです。",
           "宮城・千葉・北海道など、8倍で足りる会場にぴったりです。")
out += box("ビクセン 双眼鏡 アリーナH+8×21WP", "ビクセン アリーナH+ 8x21WP", "色はブルー・イエロー・パープル・グリーンなどがあります")

out += b.h3("遠い席なら10倍")
out += b.p("静岡・福岡・横浜のスタンド席や、大阪・愛知の後ろのブロックなら10倍がおすすめです。",
           "10倍になると手ブレが気になりやすいので、口径(レンズの大きさ)が少し大きく、両手でしっかり持てるものを選ぶと見やすくなります。")
out += box("コンサート用 双眼鏡 10倍", "双眼鏡 10倍 コンサート", "重さ・明るさ・防振機能のありなしを見くらべて選んでください")

out += b.h3("本気で見たいなら12倍の防振：ビクセン ATERA II H12×30")
out += b.mini(("倍率", "12倍"), ("重さ", "約422g(電池別)"), ("値段の目安", "8万円前後"), ("特長", "手ブレをおさえる防振機能つき"))
out += b.p("ボタンを押すと手ブレをおさえてくれる防振双眼鏡です。",
           "12倍でも画面がゆれにくく、遠い席からでもメンバーの表情までくっきり見えます。")
out += b.p("値段は高めですが、毎年いくつもの公演に行く人や、大阪城ホールの2階スタンドのような遠い席にはとくに心強い1台です。",
           "1回だけ使いたいなら、双眼鏡のレンタルを使う方法もあります。")
out += box("ビクセン 防振双眼鏡 ATERA II H12×30", "ビクセン ATERA II H12x30", "電池が必要です。前の日に動くか確かめておきましょう")

# ---------------------------------------------------------------- マナー
out += b.h2("双眼鏡を使うときの注意点")
out += b.checks(["身を乗り出したり、立ち上がって高い位置で構えたりしない",
                 "ストラップを首にかけて、落とさないようにする",
                 "防振双眼鏡は電池が切れていないか前の日に確かめる",
                 "ペンライトやうちわと持ちかえやすいよう、ポーチやケースを用意する",
                 "暗い会場では、レンズが小さいと暗く見えることもある"])
out += b.p("双眼鏡でずっと1人を追っていると、ステージ全体の演出を見のがしてしまうこともあります。",
           "推しのソロパートや見せ場だけ双眼鏡で見る、というように使い分けるのもおすすめです。")
out += b.p("自分の席がどのあたりになりそうかは、" + L(A_CHAKUBURO, "トラジャの着ブロは当たりにくい？") + "も参考にしてください。")

# ---------------------------------------------------------------- まとめ
out += b.h2("まとめ")
out += b.checks(["今回のツアーはアリーナ・ホールだけなので、8〜10倍があればほとんどの席で困らない",
                 "宮城・千葉・北海道は8倍が目安",
                 "静岡・福岡・横浜は10倍がおすすめ",
                 "大阪城ホールの2階スタンドと愛知の後ろのブロックは10〜12倍",
                 "12倍以上は手ブレしやすいので、防振双眼鏡を選ぶと安心"])
out += b.p("双眼鏡があると、メンバーの表情やダンスの細かいところまで楽しめます。",
           "自分の席が分かったら、この記事を見ながら準備してみてください！")
out += related([(A_SCHEDULE, "トラジャ2027ツアー『Jewelry Basket』の会場・日程まとめ！"),
                (A_CAPA, "トラジャ2027ツアー会場のキャパは？収容人数と公演数まとめ！"),
                (A_RESULT, "トラジャ2027ツアーの当落倍率は？当選率を会場別に調査！"),
                (A_CHAKUBURO, "トラジャの着ブロは当たりにくい？当選率と席の位置は？")])

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
        print("作った:", blogkit.ARTICLES / (KEY + ".html"), len(TITLE))
    else:
        if not EYECATCH.exists():
            subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "eyecatch_torahja_canva.py"),
                            "--top", "Jewelry Basketツアー", "--group", "--main", "双眼鏡は何倍？",
                            "--bottom", "会場別のおすすめ倍率！", "--color-key", "group", "--out", str(EYECATCH)], check=True)
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
