# -*- coding: utf-8 -*-
"""SixTONES日産スタジアムの双眼鏡は何倍？(chomoand-0.com)。2026-11-20夜 オシリ依頼(トラジャ3334の横展開)。公演は11/21・22。

材料:
- 日産スタジアム: 最大72,327人、1階約34,000席/2階約38,000席(チケットサイトの座席解説)、屋根は1階19列目より後ろと2階のみ(1238と同じ)
- 陸上トラックつきでピッチ(105m×68m)の外側にスタンド → ステージの反対側のスタンドは100m以上
- MILESixTONESの演出(味スタのレポ): U字の外周・タワー型トロッコ・フロート・Bステージ/センター(ブログのレポ、細部は食い違いあり)
- 倍率の目安は量販店・比較サイトの一般的な目安。商品はトラジャ3334と同じ(アリーナH+8×21WP/ATERA II H12×30)
- 楽天APIはこのPCで403なので検索リンク枠

    python tools/_build_sixtones_nissan_binoculars_1120.py --build-only
    python tools/_build_sixtones_nissan_binoculars_1120.py              # 下書き投稿
    python tools/_build_sixtones_nissan_binoculars_1120.py --update
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
import affiliate_box as ab  # noqa: E402
import affiliate_linker as al  # noqa: E402

SITE = "sixtones"
KEY = "sixtones_nissan_binoculars_1120"
TITLE = "SixTONES日産スタジアムの双眼鏡は何倍？席別のおすすめ！"
SLUG = "sixtones-nissan-binoculars"
CATEGORIES = [15]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "SixTONES日産スタジアムの双眼鏡は何倍？"

S = "https://chomoand-0.com/"
U1238 = S + "sixtones-stadium-nissan-fashion-goods-1238"
U1509 = S + "sixtones-live-seat-when-1509"
U1567 = S + "sixtones-milesixtones-nissan-setlist-1567"
U1637 = S + "sixtones-nissan-kaerikata-1637"
U1269 = S + "sixtones-nagai-atsuzoko-boots-rain-1269"
X_NISSAN = "https://x.com/SixTONES_SME/status/2119332762721378714"
SRC_QA = "https://www.nissan-stadium.jp/qa/detail.php?m=6&a=57"
SRC_SEAT = "https://tour.l-tike.com/contents/media/article20250604.html"

# 中立色で書き、あとで sixtones_theme.per_section がグループ色(6色ストライプ)に直す
b = blogkit.Blocks("#333333", "#d5d5d5", "#f5f5f5")
L = b.link
_ENV = ab.load_keys()


def amz_url(q):
    return al.build_amazon_search_url(q, _ENV.get("AMAZON_ASSOCIATE_TAG"))


def rk_url(q):
    import urllib.parse
    t = urllib.parse.quote("https://search.rakuten.co.jp/search/mall/" + urllib.parse.quote(q) + "/", safe="")
    return "https://hb.afl.rakuten.co.jp/hgc/{}/?pc={}&m={}".format(_ENV["RAKUTEN_AFFILIATE_ID"], t, t)


def box(title, q, note=""):
    return ab.build_box(rk_url(q), None, title, amz_url(q), note=note, border="#333333") + "\n\n"


def related(items):
    lis = "\n".join("<li>{}</li>".format(L(u, t)) for u, t in items)
    return b.html('<div style="border:1px solid #d5d5d5;border-left:4px solid #333333;border-radius:4px;'
                  'padding:12px 18px;margin:0 0 16px 0;background:#f5f5f5;">\n'
                  '<p style="margin:0 0 6px 0;font-weight:bold;">あわせて読みたい</p>\n'
                  '<ul style="margin:0;padding-left:1.2em;">\n' + lis + "\n</ul>\n</div>")


out = ab.NOTICE + "\n\n"
out += b.p("SixTONES初のスタジアムツアー「MILESixTONES」も、いよいよ最後の日産スタジアム公演です。",
           "11月21日(土)・22日(日)の2日間、どちらも16時30分に始まります。")
out += b.p("日産スタジアムは、最大7万人以上が入る日本でいちばん大きいスタジアムです。",
           "「双眼鏡は何倍がいい？」「アリーナ席でもいる？」という人に向けて、" + b.mark("席の場所ごとのおすすめの倍率") + "をまとめました。")
out += b.wakaru(["日産スタジアムの広さと、ステージまでの距離",
                 "アリーナ・1階・2階、席ごとのおすすめ倍率",
                 "トロッコやフロートのときの双眼鏡の使い方",
                 "8倍・10倍・12倍(防振)のおすすめ",
                 "夜のスタジアムで気をつけること"])

# ---------------------------------------------------------------- 結論
out += b.h2("SixTONES日産スタジアムの双眼鏡は何倍？10倍が基本")
out += b.p("結論からいうと、日産スタジアムでは" + b.mark("10倍") + "があると安心です。",
           "スタンドの上のほうや、ステージと反対側の席なら、12倍の防振双眼鏡があると表情までしっかり見えます。")
out += b.table(("席の場所", "おすすめ", "ポイント"),
               [("アリーナの前のほう", "8倍", "トロッコが近くに来たら肉眼で"),
                ("アリーナの後ろ・1階スタンド", "10倍", "モニターと双眼鏡を使い分ける"),
                ("2階スタンド", "10〜12倍", "手ブレしにくい防振があると楽"),
                ("ステージの反対側のスタンド", "12倍(防振)", "ステージまで100m以上")])
out += b.p("家電量販店や比較サイトでも、「ステージまで75m以下なら8倍以下」「スタンド後方や2階席は10〜12倍」が目安とされています。",
           "ただ、倍率が高いほど手ブレしやすく、見える範囲もせまくなります。",
           "防振機能がない双眼鏡なら、10倍までにしておくのがおすすめです。")
out += b.html('<figure class="wp-block-image size-large"><img src="https://chomoand-0.com/wp-content/uploads/2026/11/sixtones_nissan_1238_nagai_board_1116-500x375.jpg" '
              'alt="MILESixTONES長居公演の看板(右下に日産スタジアム11月21日・22日の文字)" class="wp-image-1579"/>'
              '<figcaption style="font-size:0.8em;color:#888;">出典:' + L(X_NISSAN, "SixTONES公式X") + '</figcaption></figure>')

# ---------------------------------------------------------------- 広さ
out += b.h2("日産スタジアムはどのくらい広い？")
out += b.mini(("最大収容人数", "72,327人(日本最大)"),
              ("スタンド", "1階席 約34,000席/2階席 約38,000席"),
              ("グラウンド", "サッカーのピッチ105m×68mのまわりに陸上トラック"),
              ("屋根", "1階席の19列目より後ろと2階席だけ"))
out += b.p("日産スタジアムは陸上競技場なので、サッカーのピッチのまわりに陸上のトラックがあり、その外側にスタンドがあります。",
           "ピッチの長さだけで105mあるので、" + b.mark("ステージと反対側のスタンドは100m以上") + "離れることになります。")
out += b.p("スタンドは1階と2階の2段で、2階席は上から全体を見わたせるぶん、ステージまでの距離は長くなります。",
           "アリーナツアーのつもりで8倍を持っていくと、2階席では「もう少し大きく見たい」と感じやすい会場です。")
out += b.p("出典:" + L(SRC_SEAT, "ローチケ旅行 日産スタジアムの座席解説") + "/" + L(SRC_QA, "日産スタジアム Q&A"))

# ---------------------------------------------------------------- 席別
out += b.h2("席別のおすすめ倍率")
out += b.h3("アリーナ席：8〜10倍")
out += b.p("グラウンドの上に並ぶアリーナ席は、ステージにいちばん近い席です。",
           "それでも後ろのブロックはステージから50m以上はなれるので、8〜10倍があると表情が見やすくなります。")
out += b.p("アリーナ席は平らな床にイスが並ぶので、前の人の頭でステージが見えにくいこともあります。",
           "そんなときは双眼鏡で、すき間からメンバーを追いかけるのも1つの方法です。")

out += b.h3("1階スタンド：10倍")
out += b.p("1階スタンドは段差があるので、アリーナ席より前の人の頭が気になりにくい席です。",
           "ただ、トラックをはさむぶんステージまでは遠くなるので、10倍がおすすめです。")

out += b.h3("2階スタンド：10〜12倍")
out += b.p("2階スタンドは、ステージや外周を上から見わたせる席です。",
           "フォーメーションや照明の演出はよく見えますが、表情まで見たいなら10倍以上がほしいところです。")
out += b.p("ステージと反対側の2階席や、スタンドの上のほうになったら、12倍の防振双眼鏡があると安心です。")

out += b.h3("トロッコ・フロートのときは低めの倍率で")
out += b.p("味の素スタジアムの公演では、U字の外周をフロートやタワーのようなトロッコが回る演出がありました。",
           "トロッコが集まってセンターステージになる場面もあったと、参加した人のレポに書かれています。",
           "メンバーがスタンドの近くまで来てくれる時間もあります。")
out += b.p("動いているメンバーを高い倍率で追うと、すぐに見えなくなってしまいます。",
           b.mark("トロッコやフロートが近くに来たら、双眼鏡を下ろして肉眼で") + "見るのがおすすめです。",
           "ステージの上で歌っているときや、遠くの外周にいるときに双眼鏡を使うと、見のがしが少なくなります。")
out += b.p("セットリストは" + L(U1567, "SixTONES日産スタジアムのセトリは？") + "でまとめています。",
           "推しのソロパートの曲を先にチェックしておくと、双眼鏡を使うタイミングも決めやすいです。")

# ---------------------------------------------------------------- おすすめ
out += b.h2("日産スタジアムにおすすめの双眼鏡")
out += b.h3("アリーナ席なら8倍：ビクセン アリーナH+8×21WP")
out += b.mini(("倍率", "8倍"), ("重さ", "約195g"), ("特長", "コンサート向けの軽くて小さい双眼鏡。防水"))
out += b.p("コンサートで使うことを考えて作られた、ビクセンの「アリーナ」シリーズです。",
           "195gと軽く、ペンライトと持ちかえながらでも疲れにくいのがうれしいポイントです。",
           "防水なので、急な雨でも安心です。")
out += box("ビクセン 双眼鏡 アリーナH+8×21WP", "ビクセン アリーナH+ 8x21WP", "色はブルー・イエロー・パープル・グリーンなどがあります")

out += b.h3("スタンド席なら10倍")
out += b.p("1階スタンドやアリーナの後ろなら10倍がおすすめです。",
           "夜のスタジアムで使うので、レンズ(口径)が少し大きくて明るく見えるものを選ぶと、表情がくっきり見えます。")
out += box("コンサート用 双眼鏡 10倍", "双眼鏡 10倍 コンサート", "重さ・明るさ・防振機能のありなしを見くらべて選んでください")

out += b.h3("2階席なら12倍の防振：ビクセン ATERA II H12×30")
out += b.mini(("倍率", "12倍"), ("重さ", "約422g(電池別)"), ("値段の目安", "8万円前後"), ("特長", "手ブレをおさえる防振機能つき"))
out += b.p("ボタンを押すと手ブレをおさえてくれる防振双眼鏡です。",
           "12倍でも画面がゆれにくいので、2階スタンドからでもメンバーの表情までくっきり見えます。")
out += b.p("値段は高めですが、ドームやスタジアムによく行く人には心強い1台です。",
           "1回だけ使いたいなら、双眼鏡のレンタルを使う方法もあります。")
out += box("ビクセン 防振双眼鏡 ATERA II H12×30", "ビクセン ATERA II H12x30", "電池が必要です。前の日に動くか確かめておきましょう")

# ---------------------------------------------------------------- 注意
out += b.h2("夜のスタジアムで双眼鏡を使うときの注意点")
out += b.p("16時30分に始まるので、ライブの途中からは暗くなります。",
           "11月のスタジアムは夜になるとかなり冷えるので、双眼鏡を使うときにも気をつけたいことがあります。")
out += b.checks(["暗い時間はレンズが小さいと暗く見えるので、明るさも気にして選ぶ",
                 "手袋をしたままでもピントを合わせやすいか、前もって試しておく",
                 "寒いと電池が早く減るので、防振双眼鏡は予備の電池を持っていく",
                 "身を乗り出したり、立ち上がって高い位置で構えたりしない",
                 "ストラップを首にかけて、スタンドから落とさないようにする"])
out += b.p("スタンドの階段は急なので、双眼鏡はケースに入れて、両手を空けて移動しましょう。",
           "当日の服装や防寒は" + L(U1238, "SixTONES日産スタジアムの服装は？") + "でくわしく紹介しています。")

# ---------------------------------------------------------------- まとめ
out += b.h2("まとめ")
out += b.checks(["日産スタジアムは最大72,327人の日本最大のスタジアム",
                 "ステージと反対側のスタンドは100m以上はなれる",
                 "アリーナ席は8〜10倍、1階スタンドは10倍が目安",
                 "2階スタンドやステージの反対側は12倍の防振双眼鏡があると安心",
                 "トロッコやフロートが近くに来たら、双眼鏡を下ろして肉眼で"])
out += b.p("初のスタジアムツアーの最後の2日間です。",
           "双眼鏡とモニター、肉眼をうまく使い分けて、SixTONESの6人をしっかり目に焼きつけてください！")
out += related([(U1238, "SixTONES日産スタジアムの服装は？開演時間とグッズも！"),
                (U1637, "SixTONES日産スタジアムの帰り方は？飲み物の持ち込みルールも！"),
                (U1567, "SixTONES日産スタジアムのセトリは？予習したい34曲！"),
                (U1509, "SixTONESのライブの席はいつ分かる？"),
                (U1269, "長居公演で話題になった厚底ブーツと雨の日の足元対策")])

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    import sixtones_theme
    out = blogkit.finalize(out, SITE, NAMES)
    out = out.replace('<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">',
                      '<div style="border:1px solid #d5d5d5;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">')
    out = sixtones_theme.per_section(out)
    if "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った", blogkit.ARTICLES / (KEY + ".html"), len(TITLE))
    else:
        if not EYECATCH.exists():
            subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "eyecatch_sixtones.py"),
                            "--main", "双眼鏡は何倍？", "--bottom", "日産スタジアム", "--bottom", "席別のおすすめ！",
                            "--color-key", "group", "--out", str(EYECATCH)], check=True)
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
