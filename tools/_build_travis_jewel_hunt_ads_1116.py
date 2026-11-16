# -*- coding: utf-8 -*-
"""トラジャ『Jewelry Basket』の街の広告(大阪駅・道頓堀・渋谷)とJewel Hunt(chomoand-4.blog)。2026-11-16 ライバル見張りから。

    python3 tools/_build_travis_jewel_hunt_ads_1116.py              # 下書き投稿
    python3 tools/_build_travis_jewel_hunt_ads_1116.py --build-only
    python3 tools/_build_travis_jewel_hunt_ads_1116.py --update
材料: tools/Xiy/posts_1116_jewelhunt_{live,osaka,shibuya}/ と公式発表(UNIVERSAL MUSIC・公式X・特設ページ)。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "travis"
KEY = "travis_jewel_hunt_ads_1116"
TITLE = "トラジャの広告はどこ？大阪駅・道頓堀・渋谷の場所といつまで！"
SLUG = "travis-japan-jewelry-basket-ads-osaka-dotonbori-shibuya"
CATEGORIES = [3]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch_canva.jpg")
EYECATCH_ALT = "Travis Japan Jewelry Basketの広告の場所"
X_TEXT = ""
X_TAGS = "#TravisJapan #トラジャとジュエルハント"

X_OFFICIAL = "https://twitter.com/TravisJapan_cr/status/2122224078098694447"
X_DOTONBORI = "https://twitter.com/TravisJapan_cr/status/2122162925922406744"
X_SCRAMBLE = "https://twitter.com/TravisJapan_cr/status/2122162843101569331"
X_YAMANOTE = "https://twitter.com/TravisJapan_cr/status/2122162778312224876"
X_COUNT2 = "https://x.com/TravisJapan_cr/status/2122254904358228279"
PHOTO = blogkit.ROOT / "images" / (KEY + "_official.jpg")
PHOTO_ALT = "Jewelry Basketの白いビジューの衣装を着たTravis Japanのメンバー"
MEDIA_CACHE = blogkit.ARTICLES / (KEY + "_media.json")
X_OSAKA_SOUTH = "https://twitter.com/Machu_to_kyomo/status/2122293605029343284"
X_OSAKA_SAKURA = "https://twitter.com/Machu_to_kyomo/status/2122290316921172406"
UM_NEWS = "https://www.universal-music.co.jp/travisjapan/news/2026-11-16/"
JW_TOP = "https://sp.universal-music.co.jp/travisjapan/4th_album/jw/top/index.html"
SITE_URL = "https://chomoand-4.blog/"

b = blogkit.Blocks("#7e57c2", "#d9cdee", "#f5f2fb")
L = b.link


def photo_block():
    dry = "--build-only" in sys.argv
    if dry:
        src, w, h = "x", 1473, 852
    else:
        cache = json.loads(MEDIA_CACHE.read_text(encoding="utf-8")) if MEDIA_CACHE.exists() else {}
        if "photo" not in cache:
            wp = blogkit.WP(SITE)
            mid = wp.upload_media(str(PHOTO), PHOTO_ALT)
            cache["photo"] = wp.get("/media/{}".format(mid))
            MEDIA_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        m = cache["photo"]
        sz = m["media_details"].get("sizes", {})
        big = sz.get("large") or {"source_url": m["source_url"], "width": m["media_details"]["width"],
                                  "height": m["media_details"]["height"]}
        src, w, h = big["source_url"], big["width"], big["height"]
    return b.html('<figure class="wp-block-image size-large"><img src="{}" alt="{}" width="{}" height="{}" '
                  'style="max-width:100%;height:auto;"><figcaption style="font-size:0.8em;color:#888;">'
                  '出典:{}</figcaption></figure>'.format(src, PHOTO_ALT, w, h, X_COUNT2))


out = ""
out += b.p("Travis Japanの4thアルバム『Jewelry Basket』の広告が、大阪と渋谷の街に出ています。",
           "場所は" + b.mark("JR大阪駅・道頓堀のTSUTAYA EBISUBASHI・渋谷駅のまわり") + "です。",
           "QRコードを読んで宝石を集める「Jewel Hunt」は、" + b.mark("11月16日(月)〜22日(日)") + "の7日間です。")
out += b.p("この記事では、広告がある場所を駅の出口や建物の名前までしぼってまとめました。",
           "流れる回数の目安や、Jewel Huntの遊び方、気をつけたいことも紹介します。",
           "※2026年11月16日時点の情報です。")
out += b.mini(("企画", "Jewel Hunt(ジュエルハント)"),
              ("期間", "2026年11月16日(月)〜22日(日)"),
              ("場所", "JR大阪駅/渋谷駅のまわり・センター街"),
              ("大型ビジョン", "道頓堀・渋谷スクランブルスクエア・山手線(同じ期間)"),
              ("きっかけ", "11月18日(水)のアルバム配信"))
out += b.wakaru(["広告はいつからいつまで？",
                 "大阪駅の広告はどこ？",
                 "道頓堀の大型ビジョンはどこ？",
                 "渋谷の広告はどこ？",
                 "Jewel Huntの遊び方",
                 "見に行く前に知っておきたいこと"])

out += b.h2("トラジャの広告はいつからいつまで？")
out += b.mini(("Jewel Hunt", "11月16日(月)〜22日(日)"),
              ("大型ビジョン", "11月16日(月)〜22日(日)"))
out += b.p("Jewel Huntの期間は、11月16日(月)から22日(日)までです。",
           "公式Xでは、16日の16時ごろに企画のスタートが発表されました。")
out += b.xembed(X_OFFICIAL)
out += b.p("この企画は、アルバムの配信が11月18日(水)に始まるのを記念したものです。",
           "配信日をはさんだ1週間、7人が大阪と渋谷の街をジャックしている形になります。")
out += b.h3("大型ビジョンの放映もいつまで？")
out += b.p("道頓堀・渋谷スクランブルスクエア・山手線の映像も、同じ" + b.mark("11月16日(月)〜22日(日)") + "です。",
           "公式Xが、16日の正午にそれぞれの期間を発表しています。",
           "ただし放映の状況は予告なく変わることがあるので、早めに見に行くと安心です。")
out += photo_block()
out += b.p("大型ビジョンで流れているのは、撮りおろしのスペシャル映像です。",
           "街のポスターやサイネージには、写真のような白いビジューの衣装のビジュアルも使われています。",
           "この写真は、公式Xが配信まで「あと2日」のカウントダウンで投稿したものです。")
out += b.p("アルバムの配信日や全12曲は " +
           L(SITE_URL + "travis-japan-jewelry-basket-digital-release-2778", "Jewelry Basket配信はいつ？全12曲とPOP STARも！") +
           " でまとめています。")

out += b.h2("大阪駅の広告はどこ？")
out += b.mini(("場所", "JR大阪駅の改札の外"),
              ("出口", "南口・桜橋口・御堂筋線から上がってすぐ"),
              ("形", "柱などのデジタルサイネージ(動く広告)"))
out += b.p("大阪駅の広告は、" + b.mark("JR大阪駅の改札の外にあるデジタルサイネージ") + "です。",
           "紙のポスターではなく、ほかの広告と順番に切りかわって流れます。",
           "実際に見られているのは、おもに次の3か所です。")
out += b.table(("場所", "目印", "流れる順番の例"),
               [("南口(改札の外)", "改札を出てすぐの柱", "ルクアのメガネの広告のあと"),
                ("桜橋口(改札の外)", "西側の出口", "USJの広告のあと"),
                ("御堂筋線側", "551のお店の近く", "面ごとにメンバーがちがう")])
out += b.h3("南口は改札を出てすぐの柱")
out += b.p("いちばん見つけやすいのは、JR大阪駅の南口です。",
           "改札を出てすぐの柱に、たて長のサイネージがならんでいます。",
           "ルクアのメガネの広告などのあとに、トラジャの映像が流れます。")
out += b.xembed(X_OSAKA_SOUTH)
out += b.p("白いキラキラの衣装と、こい色のスーツの2種類が流れています。",
           "どちらも「2026.11.18 Digital Release / 12.16 CD Release」の文字入りです。",
           "画面の下にあるQRコードが、Jewel Huntの入り口になっています。")
out += b.h3("桜橋口はほかの広告と順番に流れる")
out += b.p("西側の桜橋口にも、改札の外にサイネージがあります。",
           "ムーミンやUSJの広告などと順番に切りかわるので、少し待つことになります。")
out += b.xembed(X_OSAKA_SAKURA)
out += b.p("メンバー1人ずつの画像は、1回の放映で何人か続けて出ます。",
           "7人そろった動画は短いので、先にスマホを構えて待っておくと撮りやすいです。")
out += b.h3("御堂筋線から上がってすぐの場所も")
out += b.p("地下鉄御堂筋線の梅田駅から上がってすぐ、551のお店があるあたりにもサイネージがあります。",
           "面ごとに出てくるメンバーがちがうので、何か所か回るのがおすすめです。")
out += b.gmap("JR大阪駅 南口")
out += b.p("大阪駅はとても広く、ガラスの反射で写真が撮りにくい場所もあります。",
           "反射が気になるときは、少しななめから撮ると写りこみがへります。")

out += b.h2("道頓堀の大型ビジョンはどこ？")
out += b.mini(("場所", "TSUTAYA EBISUBASHI(つたや えびすばし)の上"),
              ("ビジョン", "ヒットビジョン(大型ビジョン)"),
              ("回数の目安", "1時間に4回ほど(15分おき)"))
out += b.p("道頓堀の広告は、" + b.mark("戎橋のすぐそばにあるTSUTAYA EBISUBASHIの大型ビジョン") + "です。",
           "1階にスターバックスが入っている、ひときわ大きい画面のビルです。",
           "大阪駅とはちがい、こちらはQRコードを読む企画ではありません。")
out += b.xembed(X_DOTONBORI)
out += b.p("公式Xでは、ここで「スペシャル映像を放映中」と案内しています。",
           "ビジョンは上と下の2面に分かれていて、上の面ではメンバーの動く映像が流れます。",
           "下の面には、白い衣装の7人がならんだアルバムの画像が大きく出ます。",
           "ピンクの背景に「4th Album Jewelry Basket」の文字が入った、はなやかなデザインです。")
out += b.h3("何分ごとに流れる？")
out += b.p("16日の午後には、14時ちょうど・15分・30分・45分に流れたという投稿がありました。",
           "15分おき、1時間に4回くらいのペースとみられます。",
           "時間はずれることもあるので、少し余裕をもって待つのがおすすめです。")
out += b.gmap("TSUTAYA EBISUBASHI")
out += b.p("戎橋のまわりは、昼も夜も人がとても多い場所です。",
           "橋の上で立ち止まると通行のじゃまになるので、はしに寄ってから見上げましょう。",
           "グリコの看板を見に行くついでに立ち寄れる距離です。")

out += b.h2("渋谷の広告はどこ？")
out += b.mini(("Jewel Hunt", "渋谷駅のまわり・センター街"),
              ("大型ビジョン", "渋谷スクランブルスクエア・スクランブル交差点"),
              ("ほか", "MAGNET by SHIBUYA109・山手線の車内"))
out += b.p("渋谷では、" + b.mark("駅のまわりとセンター街") + "でJewel Huntができます。",
           "そのほかに、大型ビジョンや電車の中の画面でも映像が流れています。")
out += b.table(("場所", "形", "回数の目安"),
               [("センター街", "ポスター・ビジョン", "QRで宝石を集める"),
                ("渋谷スクランブルスクエア", "大型ビジョン", "くり返し放映"),
                ("スクランブル交差点", "大型ビジョン", "30分に1回ほど"),
                ("MAGNET by SHIBUYA109", "大型ビジョン", "10分おきの可能性"),
                ("山手線", "窓の上の画面", "20〜30分に1回ほど")])
out += b.h3("センター街はポスターがたくさん")
out += b.p("センター街には、トラジャのポスターがいくつも出ています。",
           "メンバーごとに2種類あるので、全部見つけるには歩き回ることになります。",
           "外国からの観光客も多く、夕方はかなりこみあいます。")
out += b.p("Jewel Huntを全部そろえるのに、2時間かかったという声もありました。",
           "時間に余裕のある日に行くか、何日かに分けて回るのがよさそうです。")
out += b.gmap("渋谷センター街")
out += b.h3("スクランブルスクエアと交差点の大型ビジョン")
out += b.p("駅の真上にある渋谷スクランブルスクエアのビジョンでも、7人の映像が流れています。",
           "スクランブル交差点のまわりのビジョンでも、30分に1回ほど見られるようです。")
out += b.xembed(X_SCRAMBLE)
out += b.p("交差点のビジョンは、道路の向こう側から見ると画面全体が入って撮りやすいです。",
           "信号待ちの間にスマホを構える人も多いので、まわりに気をつけましょう。")
out += b.h3("MAGNETと山手線の車内も")
out += b.p("スクランブル交差点の角にあるMAGNET by SHIBUYA109のビジョンでも流れています。",
           "16時40分に見かけたという投稿があり、10分おきくらいかもしれません。")
out += b.p("山手線の窓の上の画面「まどうえビジョン」にも、トラジャが登場しています。",
           "20〜30分に1回くらいで、ほかの広告のあとに急に始まるようです。",
           "山手線を3分の1周ほど乗れば、1回は見られる計算になります。")
out += b.xembed(X_YAMANOTE)

out += b.h2("Jewel Huntの遊び方")
out += b.mini(("集めるもの", "7人分のJEWEL(宝石)"),
              ("ビジュアル", "1人2種類・全14枚"),
              ("ごほうび", "スマホで見られるスペシャルムービー"))
out += b.p("Jewel Huntは、街のポスターやビジョンのQRコードを読んで宝石を集める企画です。",
           "同じメンバーの2種類のビジュアルを読むと、そのメンバーの色の宝石ができあがります。",
           "7人分そろえると、" + b.mark("スマホでスペシャルムービーが見られます") + "。")
out += b.table(("メンバー", "宝石の色"),
               [("宮近海斗", "赤"), ("中村海人", "緑"), ("七五三掛龍也", "ピンク"),
                ("川島如恵留", "白"), ("吉澤閑也", "黄"), ("松田元太", "青"), ("松倉海斗", "オレンジ")])
out += b.p("宝石の色は、それぞれのメンバーカラーです。",
           "メンバーの色やよく使う絵文字は " +
           L(SITE_URL + "travis-japan-member-emoji-1929", "トラジャのメンバーの絵文字は？よく使う絵文字とメンカラ！") +
           " でも紹介しています。")
out += b.h3("ムービーは3種類、チャレンジは3回まで")
out += b.p("特設ページによると、ムービーは全部で3種類あります。",
           "チャレンジは3回までで、毎回ちがうムービーが届くしくみです。",
           "全部見たい人は、14枚を3周することになります。")
out += b.p("ムービーは通信量が多いので、Wi-Fiでの視聴がすすめられています。",
           "録画や保存、SNSへの投稿は禁止なので気をつけましょう。")
out += b.h3("記録が消えないための3つの注意")
out += b.p("宝石の記録はスマホのブラウザに残るので、開き方がとても大事です。",
           "特設ページでは、次の3つが案内されています。")
out += b.checks(["LINEなどアプリの中のQRリーダーではなく、毎回同じブラウザで開く",
                 "プライベートブラウズ(シークレットモード)はオフにする",
                 "iPhoneはSafari、AndroidはChromeの最新版を使う"])
out += b.p("シークレットモードのままだと、ページを閉じたときに記録が消えてしまいます。",
           "機種変更をすると記録は引きつげず、消えた記録はもとに戻せません。",
           "くわしくは " + L(JW_TOP, "Jewel Huntの特設ページ") + " で確かめてください。")
out += b.h3("QRコードが読めないときは")
out += b.p("ビジョンに近すぎると、QRコードが読めないことがあります。",
           "少しはなれて、QRコード全体が画面に入るようにすると読みやすくなります。",
           "ガラスの反射が強いときは、立つ位置を少しずらしてみましょう。")

out += b.h2("見に行く前に知っておきたいこと")
out += b.p("公式は、まわりの人や通行のじゃまにならないよう、長く立ち止まったり撮影したりしないでとお願いしています。",
           "駅の中でも同じで、QRコードは安全な場所から読むよう案内されています。")
out += b.p("駅員さんやお店、広告の会社への問い合わせもしないようにと書かれています。",
           "場所が分からないときは、この記事やSNSの写真で確かめましょう。",
           "出典:" + L(UM_NEWS, "UNIVERSAL MUSIC JAPAN(2026年11月16日)"))
out += b.h3("どの時間に行くのがいい？")
out += b.p("大阪駅も渋谷も、朝と夕方の通勤の時間はとてもこみあいます。",
           "平日の昼間なら、比べると人が少なく、写真も撮りやすいです。",
           "道頓堀は夜のほうが画面が明るく見えるので、写真は暗くなってからがきれいです。")
out += b.h3("CDの発売や番組もチェック")
out += b.p("CDは12月16日(水)に発売がのびています。",
           "理由や発売記念イベントのことは " +
           L(SITE_URL + "travis-japan-jewelry-basket-cd-postponed-2505", "トラジャのアルバムCD延期はなぜ？発売記念イベントはどうなる？") +
           " でまとめています。")
out += b.p("配信の週は、テレビの出演もいくつかあります。",
           "放送の予定は " +
           L(SITE_URL + "travis-japan-tv-schedule-1115-1121-2572", "トラジャのテレビ出演は？2026年11/15〜21の放送予定まとめ！") +
           " で確かめられます。")

out += b.h2("まとめ")
out += b.checks(["Jewel Huntは11月16日(月)〜22日(日)、大阪駅と渋谷駅のまわり・センター街",
                 "大阪駅は改札の外の南口・桜橋口・御堂筋線側のサイネージ",
                 "道頓堀はTSUTAYA EBISUBASHIの大型ビジョン。15分おきくらい",
                 "渋谷はセンター街のポスターと、スクランブルスクエアなどの大型ビジョン",
                 "7人分の宝石を集めると、スペシャルムービーが見られる(3種類)"])
out += b.p("街を歩きながら7人を探すのは、本当に宝探しのようで楽しそうですね。",
           "配信日の18日をはさんだ1週間、近くに行く人はぜひ足を運んでみてはいかがでしょうか！")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = blogkit.finalize(out, SITE, NAMES)
    if "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
