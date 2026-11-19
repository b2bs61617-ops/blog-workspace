# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) 目黒蓮「午後の紅茶 TEA LATTE」ありがとう駅広告(東京メトロのサイネージ)の場所まとめ。

材料: Xiy収集 tools/Xiy/_meguro_tealatte_ad_a〜c (2026-11-19)
  - 場所はファンの目撃投稿から。掲出期間の公式発表は見つかっていない(推測は「可能性」と書く)
  - 広告コピー「発売2日で1,000万本突破！」(※2026年10月7日時点/シリーズ計)は画像で確認
  - 2,000万本突破は公式インスタの発表とファンが引用しているが、ニュースでは未確認 → 「ファンの間で話題」止まり
  - 渋谷は「あった」という声だけで場所が不明なので表に入れない

    python tools/_build_snowman_meguro_tealatte_ad_1119.py --build-only
    python tools/_build_snowman_meguro_tealatte_ad_1119.py            # 下書き投稿(【未】付き)
    python tools/_build_snowman_meguro_tealatte_ad_1119.py --update   # 下書き本文を上書き
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "snowman"
L = blogkit.Blocks.link

PR_1000 = "https://prtimes.jp/main/html/rd/p/000000057.000117612.html"
NEWS_CM = "https://realsound.jp/2026/10/post-2543108.html"

X_NIHONBASHI = "https://x.com/momchan0216/status/2122902045304951090"
X_3EKI = "https://x.com/momchan0216/status/2122691850507268583"
X_SUBNADE = "https://x.com/kaonyan0619/status/2123047700216332303"
X_SHINJUKU_1116 = "https://x.com/Snowflake_rm/status/2122308752347205903"
X_IKEBUKURO = "https://x.com/adbrex_/status/2122264279739174915"

PHOTOS_STATE = blogkit.ARTICLES / "snowman_meguro_tealatte_ad_1119_photos.json"
PHOTOS = {"nihonbashi": X_NIHONBASHI, "shinjuku": X_SUBNADE, "espresso": X_SHINJUKU_1116, "creammilk": X_SHINJUKU_1116}


def photo_urls(upload):
    """ファンの写真をWPに上げてURLを返す(控えがあれば再利用)。"""
    import json
    done = json.loads(PHOTOS_STATE.read_text(encoding="utf-8")) if PHOTOS_STATE.exists() else {}
    if upload:
        wp = blogkit.WP(SITE)
        for n in PHOTOS:
            if n in done:
                continue
            mid = wp.upload_media(str(blogkit.ROOT / "images" / "meguro_tealatte_ad_{}.jpg".format(n)),
                                  "目黒蓮 午後の紅茶 TEA LATTE 駅広告")
            done[n] = wp.get("/media/{}".format(mid))["source_url"]
            PHOTOS_STATE.write_text(json.dumps(done, ensure_ascii=False, indent=2), encoding="utf-8")
            print("photo", n, mid)
    return {n: done.get(n, "{{IMG:%s}}" % n) for n in PHOTOS}


def fig(img, n, alt, cap):
    user = PHOTOS[n].split("/")[3]
    return blogkit.Blocks.html(
        '<figure style="margin:0 0 16px 0;text-align:center;"><img src="{}" alt="{}" style="max-width:100%;height:auto;" '
        'loading="lazy"><figcaption style="font-size:12px;color:#888;">{} 出典:{}</figcaption></figure>'
        .format(img[n], alt, cap, L(PHOTOS[n], "@" + user + "さんのX")))


def article(img):
    acc = "#222222"   # 目黒蓮のメンカラ=黒
    b = blogkit.Blocks(acc, "#cfcfcf", "#f5f5f5")
    o = ""
    o += b.p("目黒蓮さんが出演する「午後の紅茶 TEA LATTE」の駅広告が、東京メトロの駅に出ていると話題になっています。",
             "ベレー帽をかぶった目黒蓮さんが「ありがとうございます。」とほほえむ、" + b.mark("感謝のデジタルサイネージ広告") + "です。")
    o += b.p("この記事では、ファンの目撃情報から広告が出ている駅と場所、いつまで見られるのかをまとめます。")
    o += fig(img, "nihonbashi", "目黒蓮 午後の紅茶 駅広告 日本橋駅", "日本橋駅の通路に並ぶ午後の紅茶のサイネージ。")
    o += b.mini(("広告", "キリン「午後の紅茶 TEA LATTE」デジタルサイネージ"),
                ("出演", "目黒蓮(Snow Man)"),
                ("場所", "東京メトロの5駅(新宿・池袋・明治神宮前・日本橋・六本木)で目撃"),
                ("目撃され始めた日", "2026年11月16日(月)"),
                ("掲出期間", "公式の発表なし(11月19日時点)"))
    o += b.wakaru(["目黒蓮さんの午後の紅茶広告が出ている駅と場所",
                   "広告のデザインと「ありがとうございます」の意味",
                   "広告はいつまで見られるのか",
                   "見に行くときの注意"])

    # ---------------------------------------------------------------- 場所
    o += b.h2("目黒蓮の午後の紅茶広告はどこ？駅と場所の一覧")
    o += b.p("2026年11月19日時点で、ファンの投稿から確認できた場所は次の5駅です。",
             "どれも" + b.mark("東京メトロの駅の柱型サイネージ") + "で、同じ通路にずらりと並んでいるのが特徴です。")
    o += b.table(("駅", "場所", "目撃された日"),
                 [("新宿駅", "メトロプロムナード(サブナード方面の地下通路)", "11月16日〜"),
                  ("池袋駅", "丸ノ内線と副都心線の乗り換え通路", "11月16日〜"),
                  ("明治神宮前駅", "4番出口側の改札外", "11月17日〜"),
                  ("日本橋駅", "銀座線と東西線の改札外", "11月18日〜"),
                  ("六本木駅", "六本木交差点側の改札外", "11月18日〜")])
    o += b.p("日付は、ファンが投稿した日です。実際にはもっと前から出ていた可能性もあります。",
             "渋谷駅でも見たという声がありますが、くわしい場所は確認できなかったため表には入れていません。")

    o += b.h3("新宿駅(メトロプロムナード)")
    o += b.p("いちばん早く目撃されたのが新宿駅です。",
             "丸ノ内線の新宿駅から新宿三丁目方面へのびる地下通路「メトロプロムナード」で、サブナードの入り口近くにも並んでいます。")
    o += fig(img, "shinjuku", "目黒蓮 午後の紅茶 駅広告 新宿駅", "新宿駅の地下通路。奥にサブナードの看板が見えます。")
    o += b.xembed(X_SHINJUKU_1116)
    o += b.xembed(X_SUBNADE)

    o += b.h3("池袋駅(丸ノ内線と副都心線の乗り換え通路)")
    o += b.p("池袋駅では、丸ノ内線と副都心線をつなぐ乗り換え通路で見つかっています。",
             "11月16日には池袋駅での目撃投稿がありました。")
    o += b.xembed(X_IKEBUKURO)

    o += b.h3("明治神宮前駅(4番出口側の改札外)")
    o += b.p("明治神宮前〈原宿〉駅では、4番出口側の改札を出たところです。",
             "新宿・池袋とあわせて、同じ方が3駅をまとめて投稿しています。")
    o += b.xembed(X_3EKI)

    o += b.h3("日本橋駅・六本木駅(改札外)")
    o += b.p("日本橋駅は銀座線と東西線の改札外、六本木駅は六本木交差点側の改札外です。",
             "日本橋駅は通路の柱がほぼ全部目黒蓮さんになっていて、" + b.mark("「圧巻」") + "との声も出ています。")
    o += b.xembed(X_NIHONBASHI)

    # ---------------------------------------------------------------- 中身
    o += b.h2("広告のデザインは？ベレー帽の目黒蓮が「ありがとうございます」")
    o += b.p("広告の目黒蓮さんは、茶色のベレー帽にグレーのざっくりニット姿。",
             "片手を頭にのせて、もう片方の手でTEA LATTEのボトルを持っています。")
    o += b.table(("", "ESPRESSO", "CREAM & MILK"),
                 [("背景の色", "青", "白"),
                  ("持っている商品", "午後の紅茶 TEA LATTE with ESPRESSO", "午後の紅茶 TEA LATTE CREAM & MILK"),
                  ("コピー", "ありがとうございます。<br>発売2日で1,000万本突破！", "ありがとうございます。<br>発売2日で1,000万本突破！")])
    o += fig(img, "espresso", "目黒蓮 午後の紅茶 TEA LATTE ESPRESSO 広告", "青い背景のESPRESSO版。")
    o += fig(img, "creammilk", "目黒蓮 午後の紅茶 TEA LATTE CREAM&MILK 広告", "白い背景のCREAM & MILK版。")
    o += b.p("サイネージでは、この2種類が切りかわりながら流れています。",
             "広告の小さな注意書きには「2026年10月7日時点/シリーズ計」と書かれています。")
    o += b.p("ファンの間では「ベレー帽の目黒くんがかわいすぎる」「何度見てもかわいい」と、ベレー帽姿が特に人気です。",
             "CMとはちがう写真なので、駅でしか見られない目黒蓮さんを目当てに足を運ぶファンも多いようです。")

    o += b.h2("TEA LATTEってどんな商品？")
    o += b.p("「午後の紅茶 TEA LATTE」は、" + b.mark("濃いのに後味すっきり") + "をうたう本格ティーラテのシリーズです。",
             "ミルクティーとはちがい、仕事中や勉強中などの「オンの時間」に飲んでほしい紅茶として作られています。")
    o += b.table(("商品", "特徴"),
                 [("TEA LATTE with ESPRESSO(青)", "エスプレッソのように抽出した紅茶を使った、紅茶感の強いラテ"),
                  ("TEA LATTE CREAM & MILK(白)", "クリームとミルクで、まろやかに仕上げたラテ")])
    o += b.p("ファンの投稿を見ると、「エスプレッソが好き」「白よりこっち(青)がおいしい」など、好みが分かれているようです。")

    o += b.h2("なぜ「ありがとう」広告？発売2日で1,000万本")
    o += b.p("「午後の紅茶 TEA LATTE」は、2026年10月6日に発売された新シリーズです。",
             "キリンビバレッジの発表によると、" + b.mark("発売から2日間で1,000万本を突破") + "しました(10月7日時点の出荷数量)。")
    o += b.p("さらに発売15日目(10月20日時点)には1,500万本となり、発売した月の販売計画の約1.5倍になったそうです。",
             "今回の駅広告は、この大ヒットへのお礼の広告とみられます。")
    o += b.p("出典:" + L(PR_1000, "キリンビバレッジのプレスリリース(PR TIMES)"))
    o += b.p("11月18日には「シリーズの出荷本数が2,000万本を突破した」という午後の紅茶公式SNSの報告がファンの間で話題になり、",
             "「おめでとうございます」という投稿もたくさん見られました。")
    o += b.p("テレビCM『紅茶のラテ』篇は10月6日から放送中です。",
             "カナダのカフェで撮影し、目黒蓮さんは英語のセリフにも挑戦しています。(" + L(NEWS_CM, "Real Sound") + ")")

    # ---------------------------------------------------------------- 期間
    o += b.h2("目黒蓮の午後の紅茶広告はいつまで？")
    o += b.p("2026年11月19日時点で、" + b.mark("いつまで出ているかの公式発表は見つかっていません") + "。")
    o += b.p("目撃が始まったのは11月16日(月)です。",
             "駅のデジタルサイネージは1週間ごとに広告が入れかわることが多いため、" + b.mark("11月22日(日)ごろまで") + "の可能性があります。",
             "あくまで予想なので、見に行くなら早めがおすすめです。")
    o += b.p("また、サイネージはほかの広告と順番に流れる場合もあります。",
             "目黒蓮さんが映っていないときは、少し待ってみてください。")

    # ---------------------------------------------------------------- 注意
    o += b.h2("見に行くときの注意")
    o += b.checks(["駅の通路なので、立ち止まって撮るときは通る人のじゃまにならないように",
                   "ほかの人の顔が写らないように撮る",
                   "日本橋・六本木・明治神宮前は改札の外なので、電車に乗らなくても見られる",
                   "池袋の乗り換え通路は改札の中の可能性があるので、きっぷやICカードの準備を",
                   "朝や夕方のラッシュの時間はさけるのがおすすめ"])

    # ---------------------------------------------------------------- まとめ
    o += b.h2("まとめ")
    o += b.checks(["目黒蓮さんの「午後の紅茶 TEA LATTE」感謝広告が東京メトロの駅サイネージに登場",
                   "目撃された駅は新宿・池袋・明治神宮前・日本橋・六本木の5駅(11月19日時点)",
                   "ベレー帽姿で「ありがとうございます。発売2日で1,000万本突破！」",
                   "掲出期間の発表はなく、11月22日(日)ごろまでの可能性",
                   "渋谷など、ほかの駅の情報がわかったら追記します"])
    o += b.p("TEA LATTEを片手に、ベレー帽の目黒蓮さんに会いに行ってみてはいかがでしょうか！")
    return o


A = dict(key="snowman_meguro_tealatte_ad_1119",
         title="【目黒蓮】午後の紅茶の駅広告はどこ？いつまで見られる？",
         slug="meguro-ren-gogo-no-kocha-tea-latte-station-ad", categories=[4, 12],
         eyecatch=blogkit.ROOT / "images" / "snowman_meguro_tealatte_ad_1119_eyecatch.jpg",
         alt="目黒蓮 午後の紅茶 TEA LATTE 駅広告", names=[])


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    build_only = "--build-only" in sys.argv
    h = blogkit.finalize(article(photo_urls(upload=not build_only)), SITE, A["names"])
    print("title len", len(A["title"]))
    if build_only:
        (blogkit.ARTICLES / (A["key"] + ".html")).write_text(h, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (A["key"] + ".html"))
        sys.exit()
    blogkit.upload_draft(SITE, A["key"], A["title"], h, A["slug"], A["categories"], A["eyecatch"], A["alt"],
                         names=A["names"], update="--update" in sys.argv)
