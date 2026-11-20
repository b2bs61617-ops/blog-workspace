# -*- coding: utf-8 -*-
"""Snow ManドームツアーALL SUITEの双眼鏡は何倍？(chomoand-2.com)。2026-11-20夜 オシリ依頼(トラジャ3334の横展開)。

材料:
- 日程(公式発表の転載が複数一致): 札幌10/30〜11/1(終了)/名古屋バンテリン11/26〜29/福岡PayPay12/4〜6/東京ドーム12/23〜26/京セラ2027/1/4〜7
- 演出はID462(10/30のレポ): メイン(ホテルのセット)/センター(三段)/バック(リフター)/サイド(一塁・三塁)/アリーナトロッコ2種/外周フロート/気球3台/ドローン
- 写真: 公式X 2116825070811185296(札幌公演終了の集合写真)を tools/Xiy/_sm_allsuite_1120 から
- 倍率の目安は量販店・比較サイトの一般的な目安。商品はトラジャ3334・SixTONES1652と同じ。楽天APIはこのPCで403なので検索リンク枠
- アイキャッチは予備ツール(eyecatch_snowman.py)。Canva上書きはMCPが使えるときに差し替え

    python tools/_build_snowman_allsuite_binoculars_1120.py --build-only
    python tools/_build_snowman_allsuite_binoculars_1120.py              # 下書き投稿
    python tools/_build_snowman_allsuite_binoculars_1120.py --update
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
import affiliate_box as ab  # noqa: E402
import affiliate_linker as al  # noqa: E402

SITE = "snowman"
KEY = "snowman_allsuite_binoculars_1120"
TITLE = "Snow Manドームツアーの双眼鏡は何倍？会場別のおすすめ！"
SLUG = "snow-man-all-suite-dome-binoculars"
CATEGORIES = [4]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "Snow ManドームツアーALL SUITEの双眼鏡は何倍？"
X_TEXT = ""
X_TAGS = "#SnowMan #SnowMan_ALLSUITE"

S = "https://chomoand-2.com/"
A_SET = S + "snow-man-all-suite-stage-set-direction-462"
A_FIRST = S + "snow-man-first-live-what-to-bring-id-96"
A_SOLO = S + "snow-man-live-solo-50s-182"
X_PHOTO = "https://x.com/SN__20200122/status/2116825070811185296"
PHOTO = blogkit.ROOT / "tools" / "Xiy" / "_sm_allsuite_1120" / "images" / "post_1_img_1.jpg"
MEDIA_CACHE = blogkit.ARTICLES / (KEY + "_media.json")

ACC = "#3f8fd2"   # グループ記事なのでSnow Manのロゴ色寄りの青(1人のメンカラにしない)
b = blogkit.Blocks(ACC, "#cfe3f5", "#eef6fc")
L = b.link
_ENV = ab.load_keys()


def amz_url(q):
    return al.build_amazon_search_url(q, _ENV.get("AMAZON_ASSOCIATE_TAG"))


def rk_url(q):
    import urllib.parse
    t = urllib.parse.quote("https://search.rakuten.co.jp/search/mall/" + urllib.parse.quote(q) + "/", safe="")
    return "https://hb.afl.rakuten.co.jp/hgc/{}/?pc={}&m={}".format(_ENV["RAKUTEN_AFFILIATE_ID"], t, t)


def box(title, q, note=""):
    return ab.build_box(rk_url(q), None, title, amz_url(q), note=note, border=ACC) + "\n\n"


def listbox(title, items):
    lis = "".join("<li>{}</li>".format(i) for i in items)
    return b.html('<div style="border:1px solid #cfe3f5;border-left:4px solid {a};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;">'
                  '<p style="margin:0 0 6px 0;font-weight:bold;color:{a};">{t}</p><ul style="margin:0;padding-left:20px;">{l}</ul></div>'
                  .format(a=ACC, t=title, l=lis))


def photo():
    if "--build-only" in sys.argv:
        src, w, h = "x", 1200, 900
    else:
        cache = json.loads(MEDIA_CACHE.read_text(encoding="utf-8")) if MEDIA_CACHE.exists() else {}
        if "photo" not in cache:
            wp = blogkit.WP(SITE)
            mid = wp.upload_media(str(PHOTO), "Snow Man DOME TOUR 2026-2027 ALL SUITE札幌公演後の9人")
            cache["photo"] = wp.get("/media/{}".format(mid))
            blogkit.ARTICLES.mkdir(exist_ok=True)
            MEDIA_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        m = cache["photo"]
        big = m["media_details"].get("sizes", {}).get("large") or {
            "source_url": m["source_url"], "width": m["media_details"]["width"], "height": m["media_details"]["height"]}
        src, w, h = big["source_url"], big["width"], big["height"]
    return b.html('<figure class="wp-block-image size-large"><img src="{}" alt="Snow Man DOME TOUR 2026-2027 ALL SUITE札幌公演後の9人" '
                  'width="{}" height="{}" style="max-width:100%;height:auto;"><figcaption style="font-size:0.8em;color:#888;">'
                  '出典:<a href="{}" target="_blank" rel="noopener">Snow Man公式X</a></figcaption></figure>'.format(src, w, h, X_PHOTO))


out = ab.NOTICE + "\n\n"
out += b.p("Snow Manの5大ドームツアー「ALL SUITE」は、10月30日の札幌から始まりました。",
           "このあと名古屋・福岡・東京・大阪と続き、2027年1月7日の京セラドーム大阪までまわります。")
out += b.p("ドームはとにかく広いので、双眼鏡はほぼ必須です。",
           "「何倍を買えばいい？」という人に向けて、" + b.mark("ドームの席ごと・会場ごとのおすすめの倍率") + "をまとめました。")
out += b.wakaru(["ALL SUITEの残りの日程と会場",
                 "ドームで双眼鏡は何倍がいいか(席別)",
                 "会場ごとのポイント",
                 "気球やトロッコのときの使い方",
                 "8倍・10倍・12倍(防振)のおすすめ"])

# ---------------------------------------------------------------- 結論
out += b.h2("Snow Manのドームツアーの双眼鏡は何倍？10〜12倍が基本")
out += b.p("結論からいうと、ドームでは" + b.mark("10倍か12倍") + "がおすすめです。",
           "アリーナツアーなら8倍で足りることが多いですが、ドームはスタンドの後ろや上の席だとステージから100m以上はなれます。")
out += b.table(("席の場所", "おすすめ", "ポイント"),
               [("アリーナの前のほう", "8倍", "トロッコが近くに来たら肉眼で"),
                ("アリーナの後ろ・スタンドの下のほう", "10倍", "モニターと双眼鏡を使い分ける"),
                ("スタンドの上のほう・天井席", "12倍(防振)", "ステージまで100m以上"),
                ("ステージの真横・後ろの席", "10倍", "センターやバックステージが近いことも")])
out += b.p("家電量販店や比較サイトでも、ドームなど広い会場は8〜12倍、スタンド後方は10〜12倍が目安とされています。",
           "ただ、12倍は手ブレしやすいので、手ブレをおさえる防振機能つきを選ぶと見やすくなります。")
out += photo()

# ---------------------------------------------------------------- 日程・会場
out += b.h2("ALL SUITEの残りの日程と会場別のおすすめ")
out += b.table(("会場", "日程", "おすすめ"),
               [("札幌 大和ハウス プレミストドーム", "10/30〜11/1(終了)", "―"),
                ("名古屋 バンテリンドーム ナゴヤ", "11/26(木)〜29(日)", "10〜12倍"),
                ("福岡 みずほPayPayドーム福岡", "12/4(金)〜6(日)", "10〜12倍"),
                ("東京 東京ドーム", "12/23(水)〜26(土)", "10〜12倍"),
                ("大阪 京セラドーム大阪", "2027/1/4(月)〜7(木)", "12倍(上の階は防振)")])
out += b.p("どのドームも、アリーナ席の前のほう以外は10倍以上があると安心です。",
           "開演時間は会場や日によってちがうので、チケットや公式の案内で確かめてください。")

out += b.h3("京セラドーム大阪は上の階がとくに遠い")
out += b.p("京セラドーム大阪は、スタンドが上下にいくつもの階に分かれていて、いちばん上の階は高さもあります。",
           "上の階になったら、" + b.mark("12倍の防振双眼鏡") + "があると表情までしっかり見られます。",
           "階段も急なので、双眼鏡はケースに入れて両手を空けて移動しましょう。")

out += b.h3("東京ドームは2階席と外野側に注意")
out += b.p("東京ドームは、1階スタンドの上に2階席があります。",
           "2階席やメインステージの反対側(外野側)のスタンドは、ステージまでかなり遠くなるので10〜12倍がおすすめです。")

out += b.h3("名古屋・福岡はスタンドの後ろなら12倍")
out += b.p("バンテリンドーム ナゴヤとみずほPayPayドーム福岡も、スタンドの後ろのほうはステージから遠くなります。",
           "スタンドの前のほうなら10倍、後ろや上のほうなら12倍があると安心です。")

# ---------------------------------------------------------------- 演出
out += b.h2("ALL SUITEの演出と双眼鏡の使い方")
out += b.p("ALL SUITEは、ホテルをテーマにしたステージです。",
           "10月30日の札幌公演のレポでは、ステージはメイン・センター・バック・サイドの4か所にありました。")
out += listbox("ALL SUITEのおもな演出(札幌公演のレポより)",
               ["メインステージ:ホテルのセット(エレベーター・小部屋)",
                "センターステージ:高さが変わる三段のステージ",
                "バックステージ:リフターで上下するステージ",
                "サイドステージ:一塁側・三塁側の近く",
                "アリーナトロッコ2種と、外周をまわるフロート",
                "上空を飛ぶ飛行船型の気球3台"])
out += b.p("センターやバックステージ、サイドステージがあるので、" + b.mark("ステージの真横や後ろの席でも、メンバーが近くに来る時間") + "があります。",
           "スタンドの上のほうの席でも、気球が近くを通ることがあります。")
out += b.p("動いているトロッコやフロート、気球を高い倍率で追いかけると、すぐに見うしなってしまいます。",
           "メンバーが近くに来たら双眼鏡を下ろして肉眼で、メインステージで歌っているときは双眼鏡で、と使い分けるのがおすすめです。")
out += b.p("ステージのセットや演出は" + L(A_SET, "ALL SUITEのセットはどうなってる？") + "でくわしく紹介しています。")

# ---------------------------------------------------------------- おすすめ
out += b.h2("Snow Manのドームにおすすめの双眼鏡")
out += b.h3("アリーナ席なら8倍：ビクセン アリーナH+8×21WP")
out += b.mini(("倍率", "8倍"), ("重さ", "約195g"), ("特長", "コンサート向けの軽くて小さい双眼鏡。防水"))
out += b.p("コンサートで使うことを考えて作られた、ビクセンの「アリーナ」シリーズです。",
           "195gと軽く、ペンライトと持ちかえながらでも疲れにくいのがうれしいポイントです。",
           "アリーナ席の前のほうや、サブの1台にぴったりです。")
out += box("ビクセン 双眼鏡 アリーナH+8×21WP", "ビクセン アリーナH+ 8x21WP", "色はブルー・イエロー・パープル・グリーンなどがあります")

out += b.h3("スタンド席なら10倍")
out += b.p("アリーナの後ろやスタンドの下のほうなら10倍がおすすめです。",
           "ドームは照明が暗くなる演出も多いので、レンズ(口径)が少し大きくて明るく見えるものを選ぶと見やすくなります。")
out += box("コンサート用 双眼鏡 10倍", "双眼鏡 10倍 コンサート", "重さ・明るさ・防振機能のありなしを見くらべて選んでください")

out += b.h3("天井席なら12倍の防振：ビクセン ATERA II H12×30")
out += b.mini(("倍率", "12倍"), ("重さ", "約422g(電池別)"), ("値段の目安", "8万円前後"), ("特長", "手ブレをおさえる防振機能つき"))
out += b.p("ボタンを押すと手ブレをおさえてくれる防振双眼鏡です。",
           "12倍でも画面がゆれにくいので、ドームの上の階からでもメンバーの表情までくっきり見えます。")
out += b.p("値段は高めですが、ドームツアーに何回も入る人には心強い1台です。",
           "1回だけ使いたいなら、双眼鏡のレンタルを使う方法もあります。")
out += box("ビクセン 防振双眼鏡 ATERA II H12×30", "ビクセン ATERA II H12x30", "電池が必要です。前の日に動くか確かめておきましょう")

# ---------------------------------------------------------------- 注意
out += b.h2("双眼鏡を使うときの注意点")
out += b.checks(["身を乗り出したり、立ち上がって高い位置で構えたりしない",
                 "ストラップを首にかけて、スタンドから落とさないようにする",
                 "防振双眼鏡は電池が切れていないか前の日に確かめる",
                 "ペンライトやうちわと持ちかえやすいよう、ポーチやケースを用意する",
                 "双眼鏡ばかり見ず、ステージ全体の演出も楽しむ"])
out += b.p("持ち物全体のチェックは" + L(A_FIRST, "Snow Manライブ初参戦の持ち物は？") + "も参考にしてください。",
           "1人で行く人は" + L(A_SOLO, "Snow Manライブに1人で参戦は大丈夫？") + "もどうぞ。")

# ---------------------------------------------------------------- まとめ
out += b.h2("まとめ")
out += b.checks(["ALL SUITEは名古屋11/26〜、福岡12/4〜、東京12/23〜、大阪1/4〜",
                 "ドームでは10〜12倍が基本、アリーナの前のほうなら8倍",
                 "京セラドームの上の階や東京ドームの2階席は12倍の防振があると安心",
                 "センター・バック・サイドステージや気球で、遠い席にも近づく時間がある",
                 "トロッコや気球が近くに来たら、双眼鏡を下ろして肉眼で"])
out += b.p("9人の表情やダンスの細かいところまで見られると、ドームのライブがもっと楽しくなります。",
           "自分の席が分かったら、この記事を見ながら準備してみてください！")
out += listbox("あわせて読みたい",
               ['<a href="{}">{}</a>'.format(A_SET, "ALL SUITEのセットはどうなってる？演出は誰が担当？"),
                '<a href="{}">{}</a>'.format(A_FIRST, "Snow Manライブ初参戦の持ち物は？身分証・年齢層も解説！"),
                '<a href="{}">{}</a>'.format(A_SOLO, "Snow Manライブに1人で参戦は大丈夫？50代でも楽しめる？")])

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = blogkit.finalize(out, SITE, NAMES)
    if "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った", blogkit.ARTICLES / (KEY + ".html"), len(TITLE))
    else:
        if not EYECATCH.exists():
            subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "eyecatch_snowman.py"),
                            "--main", "双眼鏡は何倍？", "--bottom", "ドームツアーALL SUITE", "--bottom", "会場別のおすすめ！",
                            "--color-key", "group", "--out", str(EYECATCH)], check=True)
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
