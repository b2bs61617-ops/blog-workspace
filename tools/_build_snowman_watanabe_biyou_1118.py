# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) 渡辺翔太の愛用スキンケア・コスメまとめ(2026-11-18)。

材料: articles/watanabe_biyou_aiyouhin_1118_research.md
アンバサダー商品(フラルネ・スキコン・デンティス・SBC)と、2020年バズリズムで映った私物を分けて書く。
楽天APIはIP未許可(CLIENT_IP_NOT_ALLOWED)のため、楽天は検索結果ページへのアフィリエイトリンク(rk_url)、Amazonも検索リンク。

    python tools/_build_snowman_watanabe_biyou_1118.py --build-only   # articles/<KEY>.html を作るだけ
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
import affiliate_box as ab  # noqa: E402
import affiliate_linker as al  # noqa: E402

# ---- ここから記事ごとに書きかえる ----
SITE = "snowman"
KEY = "snowman_watanabe_biyou_1118"
TITLE = "渡辺翔太の愛用スキンケアは？化粧水や美容液・値段も調査！"   # 【未】は blogkit が自動で付ける
SLUG = "watanabe-shota-skincare-cosme-price"
CATEGORIES = [4, 9]                 # Snow Man / 渡辺翔太
NAMES = ["広瀬アリス", "バカリズム"]              # さんを付ける「メンバー以外の人名」
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.png")
EYECATCH_ALT = "渡辺翔太の愛用スキンケア"
X_TEXT = ""
X_TAGS = "#SnowMan #渡辺翔太"

ACC = "#3f7fc4"   # 渡辺翔太のメンバーカラー(青)
b = blogkit.Blocks(ACC, "#cfe0f3", "#eef5fc")
L = blogkit.Blocks.link
SPON = 'target="_blank" rel="nofollow sponsored noopener"'
_ENV = ab.load_keys()


def amz_url(q):
    return al.build_amazon_search_url(q, _ENV.get("AMAZON_ASSOCIATE_TAG"))


def rk_url(q):
    """楽天APIはこのPCのIPが未許可(CLIENT_IP_NOT_ALLOWED)なので、楽天の検索結果ページへのアフィリエイトリンクにする。"""
    import urllib.parse
    t = urllib.parse.quote("https://search.rakuten.co.jp/search/mall/" + urllib.parse.quote(q) + "/", safe="")
    return "https://hb.afl.rakuten.co.jp/hgc/{}/?pc={}&m={}".format(_ENV["RAKUTEN_AFFILIATE_ID"], t, t)


def amz_box(title, q, note=""):
    """楽天(検索リンク)+Amazon(検索リンク)の枠。"""
    return ab.build_box(rk_url(q), None, title, amz_url(q), note=note, border=ACC) + "\n\n"


def amz_inline(q):
    return '(<a href="{}" {}>Amazonで見る</a>)'.format(amz_url(q), SPON)


def steps(items):
    rows = ""
    for i, (t, d) in enumerate(items, 1):
        rows += ('<div style="display:flex;align-items:flex-start;margin:{};">'
                 '<span style="flex:0 0 auto;display:inline-block;width:1.8em;height:1.8em;line-height:1.8em;border-radius:50%;'
                 'background:{};color:#fff;font-weight:bold;text-align:center;margin-right:10px;">{}</span>'
                 '<span><strong>{}</strong><br><span style="font-size:0.9em;color:#555;">{}</span></span></div>'
                 ).format("0" if i == 1 else "10px 0 0 0", ACC, i, t, d)
    return b.html('<div style="border:1px solid {};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">'
                  '<p style="font-weight:bold;margin:0;padding:8px 16px;background:{};color:#fff;">渡辺翔太のスキンケアの順番</p>'
                  '<div style="padding:14px 18px;background:{};">{}</div></div>'.format(ACC, ACC, "#eef5fc", rows))


def shopbox(items):
    lis = "".join("<li>{}</li>".format(i) for i in items)
    return b.html('<div style="border:1px solid #cfe0f3;border-left:4px solid {a};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;">'
                  '<p style="margin:0 0 6px 0;font-weight:bold;color:{a};">購入先</p><ul style="margin:0;padding-left:20px;">{l}</ul></div>'
                  .format(a=ACC, l=lis))


def related(items):
    lis = "".join('<li><a href="{}">{}</a></li>'.format(u, t) for t, u in items)
    return b.html('<div style="border:1px solid #cfe0f3;border-left:4px solid {a};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;">'
                  '<p style="margin:0 0 6px 0;font-weight:bold;color:{a};">あわせて読みたい</p><ul style="margin:0;padding-left:20px;">{l}</ul></div>'
                  .format(a=ACC, l=lis))


# 出典
ALBION = "https://www.albion.co.jp/"
FLA_SP = "https://flarune-special.albion.co.jp/"
LIBERTA = "https://www.liberta-online.jp/"
SBC = "https://www.s-b-c.net/"
IPSA = "https://www.ipsa.co.jp/"
MAQUIA_23 = "https://maquia.hpplus.jp/column/beautynewsflash/86053/"
VOCE_25 = "https://i-voce.jp/feed/4440704/"
BAILA_24 = "https://baila.hpplus.jp/beauty/skincare/61470"
FS_LIP = "https://www.fashionsnap.com/article/2024-03-15/flarune-lipbar-shotawatanabe/"
WWD_SP = "https://www.wwdjapan.com/articles/2067567"
FS_MASK = "https://www.fashionsnap.com/article/2026-01-08/flarune-produce-mask/"
MAQUIA_SK = "https://maquia.hpplus.jp/column/beautynewsflash/107207/"
WWD_SK26 = "https://www.wwdjapan.com/?p=2400334"
WWD_DEN = "https://www.wwdjapan.com/articles/1821865"
RS_DEN = "https://realsound.jp/2025/10/post-2174957.html"
NONNO_SBC = "https://nonno.hpplus.jp/entertainment/ikemen/380000/"
BITEKI_SBC = "https://www.biteki.com/3033315/"
BITEKI_2507 = "https://www.biteki.com/1997887/"
BITEKI_2602 = "https://www.biteki.com/2091624/"
ORICON_TOMATO = "https://www.oricon.co.jp/news/2487450/full/"
BAILA_22 = "https://baila.hpplus.jp/lifestyle/entertainment/50841"
X_FLA = "https://x.com/albion_flarune/status/2097867661266854205"
# フラルネ公式Xの動画サムネ(公式の投稿)。投稿時にWPへ上げ直す(build-onlyでは元のURLのまま)
IMG_FLA = "https://chomoand-2.com/wp-content/uploads/2026/11/snowman_watanabe_biyou_1118_flarune_times.jpg"  # media 723(公式動画1:13の場面)

# 内部リンク
IN_PERFUME = "https://chomoand-2.com/snow-man-member-perfume-165"
IN_NICK = "https://chomoand-2.com/watanabe-shota-nickname-shoppy-74"
IN_FUKKA = "https://chomoand-2.com/fukazawa-tatsuya-solo-cm-mediheal-72"
IN_TODS = "https://chomoand-2.com/shota-watanabe-tods-autumn-bomber-price-343"

DATE_NOTE = "値段は2026年11月18日時点の公式サイトの価格(税込)です。"

out = ""
out += ab.NOTICE + "\n\n"
out += b.p("Snow Manの中でも「美容番長」として知られる渡辺翔太さん。",
           "ふだんどんなスキンケアを使っているのか、気になっている人も多いですよね。",
           "結論から言うと、" + b.mark("2023年からアンバサダーをつとめるアルビオンの「フラルネ」を、自宅にもフルラインでそろえている") + "と話しています。")
out += b.p("この記事では、フラルネを使う順番と、全商品の容量・値段をまとめました。",
           "あわせて、2020年の番組で映った「当時の私物」も、アンバサダー商品と分けて紹介します。")
out += b.mini(("名前", "渡辺翔太(わたなべ しょうた)"),
              ("生年月日", "1992年11月5日"),
              ("グループ", "Snow Man(メンバーカラーは青)"),
              ("美容の仕事", "アルビオン「フラルネ」「スキコン」、デンティス、SBC湘南美容クリニックのアンバサダー"))
out += b.p("ファンからは「しょっぴー」の愛称で親しまれています。",
           "呼び名の由来は" + L(IN_NICK, "しょっぴーの名付け親は誰？") + "で紹介しています。")
out += b.wakaru(["渡辺翔太が自宅でも使っているスキンケアのブランド",
                 "スキンケアの順番と、乳液を何プッシュ使うか",
                 "化粧水・美容液・クリームの容量と値段",
                 "渡辺翔太プロデュースの限定コスメ",
                 "歯みがき粉と美容クリニック",
                 "2020年の番組で映った当時の私物",
                 "水やトマトジュースなど毎日の美容習慣"])

# ---------------- フラルネ
out += b.h2("渡辺翔太の愛用スキンケアはアルビオン「フラルネ」")
out += b.mini(("ブランド", "アルビオン「フラルネ(FLARUNÉ)」"),
              ("使い方", "自宅にフルライン(シリーズ全部)をそろえている"),
              ("関わり", "2023年8月から公式アンバサダー(お仕事で関わる商品)"))
out += b.p("渡辺翔太さんは、2023年8月17日にアルビオンの「フラルネ」の公式アンバサダーになりました。",
           "フラルネは、乳液を化粧水の前に使う「先行乳液」で知られるアルビオンのシリーズです。")
out += b.p("2025年9月の美容誌VOCEでは、" + b.mark("自宅にもフラルネのフルラインをそろえている") + "と話しています。",
           "サウナに行くときのお風呂バッグにも入れているそうです。",
           "出典:" + L(VOCE_25, "VOCE(2025年9月・PR記事)"))
out += b.p("ここで紹介するフラルネとスキコンは、渡辺翔太さんがアンバサダーをつとめる商品です。",
           "雑誌の発言もPR記事の中のものなので、その点は知ったうえで読んでくださいね。")

out += b.h3("スキンケアの順番は？乳液から始める5ステップ")
out += b.p("VOCEで本人が話した、ふだんのお手入れの順番はこちらです。",
           "洗顔のあと、すぐに乳液をなじませるのがポイントです。")
out += steps([("乳液(先行乳液)", "フルリファイン ミルク f EM。おすすめ3プッシュのところを5プッシュ"),
              ("化粧水", "ハイドロボム プラスを多めに"),
              ("美容液", "セラム イン トータル"),
              ("クリーム", "コクメルティ クリーム"),
              ("パウダー", "ブライトニング パウダーを最後に重ねるのが定番")])
out += b.p("乳液はたっぷり5プッシュ使い、余った分は胸元までのばしているそうです。",
           "2024年のBAILAでは、お風呂上がりにまず乳液をコットンでなじませると話していました。",
           "出典:" + L(BAILA_24, "BAILA(2024年3月)"))

out += b.h3("乳液:フラルネ フルリファイン ミルク f EM")
out += b.mini(("商品名", "フラルネ フルリファイン ミルク f EM"),
              ("種類", "先行乳液(化粧水の前に使う乳液)"),
              ("容量・値段", "110g 3,630円/200g 5,830円"))
out += b.p("渡辺翔太さんのスキンケアの「1歩目」になる乳液です。",
           "洗顔後すぐの肌になじませて、あとから使う化粧水を受け止めやすくします。")
out += b.p(DATE_NOTE,
           "2026年3月には、くすみ対策の「ブライトリファイン ミルク f」も出ています。")
out += amz_box("フラルネ フルリファイン ミルク f EM", "フラルネ フルリファイン ミルク f EM",
               "正規品はアルビオン公式・百貨店でも買えます")

out += b.h3("化粧水:フラルネ ハイドロボム プラス")
out += b.mini(("商品名", "フラルネ ハイドロボム プラス"),
              ("種類", "化粧水"),
              ("容量・値段", "110ml 3,630円/200ml 5,830円"))
out += b.p("乳液のあとに使う化粧水で、渡辺翔太さんは「多め」に使うと話しています。",
           "乳液でやわらかくなった肌に、うるおいをしっかり入れるイメージです。")
out += amz_box("フラルネ ハイドロボム プラス", "フラルネ ハイドロボム プラス")

out += b.h3("美容液:フラルネ セラム イン トータル")
out += b.mini(("商品名", "フラルネ セラム イン トータル"),
              ("種類", "美容液"),
              ("容量・値段", "40ml 5,830円"))
out += b.p("化粧水のあとに使う美容液です。",
           "1本で美容液のはたらきをまとめてくれる、シリーズの中心のアイテムです。")
out += amz_box("フラルネ セラム イン トータル", "フラルネ セラム イン トータル")

out += b.h3("クリーム:フラルネ コクメルティ クリーム")
out += b.mini(("商品名", "フラルネ コクメルティ クリーム"),
              ("種類", "クリーム"),
              ("容量・値段", "30g 6,930円"))
out += b.p("お手入れの最後に、うるおいにふたをするクリームです。",
           "シリーズの中ではいちばん高いアイテムですが、少量ずつ使えます。")
out += amz_box("フラルネ コクメルティ クリーム", "フラルネ コクメルティ クリーム")

out += b.h3("仕上げ:フラルネ ブライトニング パウダー")
out += b.mini(("商品名", "フラルネ ブライトニング パウダー(医薬部外品)"),
              ("種類", "仕上げのパウダー"),
              ("容量・値段", "19g 5,500円(2024年5月の発売時)"))
out += b.p("渡辺翔太さんが「最後に重ねるのが定番」と話している仕上げのパウダーです。",
           "値段は2024年5月18日の発売時のものなので、いまの値段は公式サイトで確かめてください。",
           "出典:" + L("https://maquia.hpplus.jp/cosme/167817/", "MAQUIA"))
out += amz_box("フラルネ ブライトニング パウダー", "フラルネ ブライトニング パウダー")

out += b.h3("フラルネ5品の値段一覧")
out += b.table(("商品", "容量", "値段(税込)"),
               [("フルリファイン ミルク f EM", "110g/200g", "3,630円/5,830円"),
                ("ハイドロボム プラス", "110ml/200ml", "3,630円/5,830円"),
                ("セラム イン トータル", "40ml", "5,830円"),
                ("コクメルティ クリーム", "30g", "6,930円"),
                ("ブライトニング パウダー", "19g", "5,500円(発売時)")])
out += b.p("5品を小さいサイズでそろえると、合計で2万5,520円になります。",
           "アルビオンは2026年11月2日に一部の商品を値上げしているので、買う前に最新の値段をチェックしましょう。")
out += shopbox(["アルビオン公式:" + L(ALBION, "アルビオン公式サイト") + "・" + L(FLA_SP, "フラルネ特設サイト"),
                "全国の百貨店のアルビオン売り場、@cosme STORE",
                "楽天市場:" + '<a href="{}" {}>フラルネを楽天で見る</a>'.format(rk_url("フラルネ アルビオン"), SPON),
                "Amazon:" + '<a href="{}" {}>フラルネをAmazonで見る</a>'.format(amz_url("フラルネ アルビオン"), SPON)])
out += b.p("楽天やAmazonは、お店ではない出品者が売っていることも多いです。",
           "確実に正規品を買いたい人は、公式サイトや百貨店を選ぶと安心です。")

out += b.h3("フラルネ公式の「FLARUNÉ TIMES」でキャスター役に")
out += b.p("2026年9月10日には、フラルネ公式Xで「FLARUNÉ TIMES」という動画が公開されました。",
           "渡辺翔太さんがニュースキャスター役になり、8月18日発売の新しいクレンジングと洗顔料を紹介しています。")
out += b.xembed(X_FLA)
out += b.html('<figure style="margin:0 0 16px 0;text-align:center;"><img src="{}" alt="フラルネ公式動画FLARUNÉ TIMESで新しいクレンジングと洗顔料を持つ渡辺翔太" width="1200" height="675" style="max-width:100%;height:auto;" loading="lazy">'
              '<figcaption style="font-size:12px;color:#888;">新しいクレンジングなどを紹介する渡辺翔太さん 出典:{}</figcaption></figure>'.format(IMG_FLA, L(X_FLA, "フラルネ公式X(2026年9月10日)")))
out += b.table(("新商品", "容量", "値段(税込)"),
               [("コクーン クリーム クレンジング", "170g", "3,300円"),
                ("クイックオフ オイル クレンジング", "200ml", "3,300円"),
                ("モイスト ストリンギー ウォッシュ", "120g", "2,750円")])
out += b.p("動画で紹介された新商品は、この3つです。",
           "ただ、本人がふだん使っているという発言はまだ見つかっていません。")
out += b.p("SNSでは、渡辺翔太さんをきっかけにフラルネの先行乳液を使い始めた、という声が多く見られます。",
           "「肌がもちもちになった」という感想や、リップから入ってアルビオンにハマった人もいるようです。")
out += b.p("就任のときには、深澤辰哉さんにフラルネをすすめて、肌をきれいにしてあげたいとも話していました。",
           "その深澤辰哉さんのスキンケアCMは" + L(IN_FUKKA, "深澤辰哉の単独CM・初のMEDIHEALの記事") + "で紹介しています。",
           "出典:" + L(MAQUIA_23, "MAQUIA(2023年8月)"))

# ---------------- スキコン
out += b.h2("化粧水はアルビオン「スキコン」もアンバサダー")
out += b.mini(("商品名", "アルビオン 薬用スキンコンディショナー エッセンシャル N"),
              ("呼び名", "スキコン"),
              ("容量・値段", "110ml 4,180円/165ml 5,830円/330ml 9,680円"),
              ("値段の時期", "2026年11月2日の値上げ後"),
              ("関わり", "2025年5月からアンバサダー"))
out += b.p("渡辺翔太さんは、2025年5月1日からアルビオンの「スキコン」のアンバサダーもつとめています。",
           "スキコンは、1974年から続くアルビオンのロングセラーの化粧水です。")
out += b.p("就任のときには「さっぱりしているのに、みずみずしさや潤い感もあり」と話していました。",
           "2026年5月にも新しいムービーが公開され、アンバサダーを続けています。",
           "出典:" + L(MAQUIA_SK, "MAQUIA(2025年5月)") + "・" + L(WWD_SK26, "WWD(2026年5月)"))
out += b.p(DATE_NOTE,
           "大きいサイズほど1mLあたりは安くなるので、毎日たっぷり使いたい人は330mlがお得です。")
out += amz_box("アルビオン 薬用スキンコンディショナー エッセンシャル N", "アルビオン 薬用スキンコンディショナー エッセンシャル N",
               "110ml・165ml・330mlの3サイズ")

# ---------------- コラボ限定品
out += b.h2("渡辺翔太プロデュースの限定コスメは？")
out += b.mini(("第1弾", "フラルネ リップバー S(2024年4月)"),
              ("第2弾", "フラルネ リップバー SP(2025年4月)"),
              ("第3弾", "ディープモイスト マスク〈パック〉(2026年1月)"))
out += b.p("フラルネでは、渡辺翔太さんが関わった数量限定のコラボ商品が3つ出ています。",
           "どれも発売時の値段で、いまも買えるかはお店で確かめてください。")
out += b.table(("商品", "容量", "値段(税込)"),
               [("リップバー S", "3.0g", "2,750円"),
                ("リップバー SP", "3.0g", "2,750円"),
                ("コラボマスク", "19mL×6枚", "3,850円")])
out += b.h3("リップバー S・SP")
out += b.p("第1弾のリップバー Sは、2024年4月1日に数量限定で発売されました。",
           "渡辺翔太さんが「リップが大好き」と話していたことが、作るきっかけになったそうです。",
           "出典:" + L(FS_LIP, "FASHIONSNAP(2024年3月)"))
out += b.p("第2弾のリップバー SPは、2025年4月1日の発売です。",
           "モヒートの香りに、ミントグリーンの見た目が特徴でした。",
           "出典:" + L(WWD_SP, "WWD(2025年)"))
out += b.p("もとになった定番の「フラルネ リップバー」(3.0g 2,750円)は、いまも公式で扱われています。",
           "トッズの発表会でも、ふだんのバッグにリップクリームを入れていると話していました。",
           "そのブランドは明かしていませんが、リップ好きは本当のようです。")
out += b.p("トッズのアンバサダーとしての着こなしは" + L(IN_TODS, "インスタ「TOD'Sの秋」の服と値段の記事") + "にまとめています。")
out += amz_box("フラルネ リップバー(定番)", "フラルネ リップバー", "コラボ限定のS・SPとは別の定番品です")
out += b.h3("コラボマスク")
out += b.p("第3弾は、2026年1月23日に出たシートマスク「ディープモイスト マスク〈パック〉」です。",
           "「Shota Watanabe Collaboration Mask」として出たコラボ品で、テーマは「夜の癒しタイム」です。",
           "1箱に19mLのマスクが6枚入っています。",
           "出典:" + L(FS_MASK, "FASHIONSNAP(2026年1月)"))
out += b.p("渡辺翔太さんは、飛行機に乗るときの必需品にもシートマスクを挙げています。",
           "ふだんからパックを大事にしている本人らしいアイテムですね。")

# ---------------- デンティス
out += b.h2("歯みがき粉は「デンティス」")
out += b.mini(("商品名", "デンティス チューブ(エクストラフレッシュなど)"),
              ("容量・値段", "100g 1,595円前後(店によって差あり)"),
              ("関わり", "2024年5月からアンバサダー"))
out += b.p("口元のケアでは、リベルタの歯みがき粉「デンティス」のアンバサダーをつとめています。",
           "2024年5月23日の就任のときに、" + b.mark("1日に5回も歯をみがく") + "と話して話題になりました。")
out += b.p("仕事場でも必ずみがくそうで、トラベルセットを持ち歩いているそうです。",
           "メンバーの阿部亮平さんには「デンティスチューブ エクストラフレッシュ」をすすめたと明かしています。",
           "出典:" + L(WWD_DEN, "WWD(2024年5月)"))
out += b.p("2025年10月には、1人3役をこなした「3人のデンティス」篇のCMも公開されました。",
           "値段は、楽天のデンティス公式ストアや@cosmeで1,595円(税込)で売られていました(11月18日時点)。",
           "出典:" + L(RS_DEN, "リアルサウンド(2025年10月)"))
out += amz_box("デンティス チューブ エクストラフレッシュ 100g", "デンティス チューブ エクストラフレッシュ 100g")
out += shopbox(["リベルタ公式:" + L(LIBERTA, "リベルタ オンラインショップ"),
                "楽天市場(デンティス公式ストアあり):" + '<a href="{}" {}>デンティスを楽天で見る</a>'.format(rk_url("デンティス チューブ 100g"), SPON),
                "@cosme、ドラッグストア",
                "Amazon:" + '<a href="{}" {}>デンティスをAmazonで見る</a>'.format(amz_url("デンティス チューブ 100g"), SPON)])

# ---------------- SBC
out += b.h2("美容クリニックはSBC湘南美容クリニック")
out += b.mini(("クリニック", "SBC湘南美容クリニック"),
              ("通う頻度", "月1回(2026年7月の発表会での発言)"),
              ("受けていること", "光治療(IPL)・イオン導入"))
out += b.p("渡辺翔太さんは、SBC湘南美容クリニックのアンバサダーも約4年つとめています。",
           "2023年4月には、初めての単独CMも放送されました。")
out += b.p("2026年7月6日の新CM発表会では、月1回通っていて「おサボりした月は一度もない」と話しています。",
           "月1回、光治療(IPL)やイオン導入などを受けているそうです。",
           "出典:" + L(NONNO_SBC, "non-no(2026年7月)") + "・" + L(BITEKI_SBC, "美的(2026年7月)"))
out += b.p("ちなみに2022年のBAILAでは、そのころは2週間に1度通っていると話していました。",
           "美容クリニックや飲む日焼け止めのサプリは「メンバーの過半数に広まりました」とも話しています。",
           "サプリの商品名は話していないので、この記事でも名前は出しません。")
out += b.p("美容医療は、人によって合う・合わないがあります。",
           "施術の内容は" + L(SBC, "SBC湘南美容クリニックの公式サイト") + "で紹介されています。")

# ---------------- 2020年の私物
out += b.h2("2020年ごろのバズリズムで映ったとされる私物")
out += b.mini(("番組", "『バズリズム02』(日本テレビ)"),
              ("時期", "2020年ごろ"),
              ("注意", "6年前の情報で、いまも使っているかは分からない"))
out += b.p("アンバサダーになる前の私物では、2020年ごろの『バズリズム02』で自宅の洗面台が映ったといわれています。",
           "『バズリズム02』は、バカリズムさんが司会の日本テレビの音楽番組です。")
out += b.p("ただし、これは" + b.mark("6年ほど前の当時の様子") + "です。",
           "いまも使っているかは分からず、画面から読み取った商品名には推測も入っています。",
           "細かい種類までは決めつけず、ブランドと商品の種類で紹介します。")
out += b.table(("ブランド", "映っていたとされるもの"),
               [("イプサ", "化粧水・乳液など"),
                ("RMK", "ローション、クレンジングオイルなど"),
                ("MiMC", "バームクリームなどのコスメ"),
                ("キールズ", "リップバーム"),
                ("ドクタージャルト", "クリーム"),
                ("SABON", "ボディスクラブ"),
                ("無印良品", "化粧水")])
out += b.p("まとめサイトでは、イプサの化粧水の名前がよく挙がっています。",
           "ただ、商品は新しく切りかわっていることもあるので、" + L(IPSA, "イプサ公式サイト") + "で確かめてください。")
out += b.p("美容家電では、パナソニックのスチーマー「ナノケア」や、リファカラット フェイスも映っていたといわれています。",
           "アンバサダー商品とちがって、どれも本人が商品名を話したわけではない点に注意してくださいね。")

# ---------------- 美容法
out += b.h2("渡辺翔太の美容法・毎日の習慣は？")
out += b.mini(("飲みもの", "朝の水500mL、トマトジュース1日1リットルくらい"),
              ("夜のケア", "眠くてもメイクを落として保湿"),
              ("その他", "深夜サウナ、クエン酸ドリンク、髪は3ステップのトリートメント"))
out += b.p("スキンケア用品だけでなく、毎日の習慣も渡辺翔太さんの美肌を支えています。",
           "2023年のフラルネの就任時には、" + b.mark("毎朝、水を500mL飲みきる") + "と話していました。")
out += b.p("2026年10月19日の『THE バトルSHOW』では、トマトジュースを1日1リットルくらい飲むと明かしています。",
           "トマトにふくまれる、体のサビを防ぐ成分(抗酸化成分)を意識しているそうです。",
           "出典:" + L(ORICON_TOMATO, "オリコン(2026年10月)"))
out += b.p("美的2025年7月号では「スキンケアのベースは皆さんと同じ、日々の洗顔と保湿です」と話しました。",
           "どんなに眠くても、メイクは必ず落として保湿するそうです。",
           "出典:" + L(BITEKI_2507, "美的(2025年5月)"))
out += b.p("深夜にサウナへ行き、そのあとパックをして保湿する日もあるそうです。",
           "広瀬アリスに教わった、クエン酸と重曹のドリンクを飲んでいるとも話していました。")
out += b.h3("美的ベストビューティマンで男性初の殿堂入り")
out += b.p("渡辺翔太さんは、美的のベストビューティマンに3回選ばれ、男性で初めて殿堂入りしました。",
           "美的2026年2月号では、飛行機の必需品にシートマスクとのどスプレーを挙げています。",
           "出典:" + L(BITEKI_2602, "美的(2025年12月)"))
out += b.p("クエン酸は粉末を水に溶かして飲み、髪は3ステップのトリートメントでケアしているそうです。",
           "ここで挙げたアイテムは、ブランド名までは話していません。")

# ---------------- 香水
out += b.h2("渡辺翔太の香水はジバンシィのπ？")
out += b.p("スキンケアと一緒によく調べられているのが、渡辺翔太さんの香水です。",
           "ジバンシィの「π(パイ)」、ディオールの「ディオール オム」、イソップの「タシット」を使っていたといわれています。")
out += b.p("メンバー9人の香水は" + L(IN_PERFUME, "Snow Manの愛用香水まとめ(9人の好きな香りとブランド)") + "で、くわしく紹介しています。")

# ---------------- まとめ
out += b.h2("まとめ")
out += b.checks(["アンバサダーのアルビオン「フラルネ」を、自宅にもフルラインでそろえている",
                 "順番は乳液(5プッシュ)→化粧水→美容液→クリーム→パウダー",
                 "フラルネ5品は小さいサイズで合計2万5,520円(11/18時点・パウダーは発売時の値段)",
                 "化粧水「スキコン」、歯みがき粉「デンティス」もアンバサダー",
                 "美容クリニックはSBC湘南美容クリニックに月1回",
                 "コラボ限定品はリップバー S・SPとコラボマスクの3つ",
                 "2020年ごろのバズリズムで映ったとされるイプサやRMKは、いまも使っているか不明",
                 "水500mLとトマトジュース1リットルなど、毎日の習慣も大事にしている"])
out += b.p("まずは先行乳液の5プッシュから、渡辺翔太さんのお手入れをまねしてみてはいかがでしょうか！")
out += related([("ラブトラ35+はどこで見れる？渡辺翔太MCの番組", "https://chomoand-2.com/love-transit-35-watanabe-shota-mc-46"),
                ("渡辺翔太の空港置き去り事件とは？カナダeTAの真相", "https://chomoand-2.com/watanabe-shota-airport-eta-sunomanma-669"),
                ("Snow Manのゆり組とは？名前の由来は幼稚園のクラス", "https://chomoand-2.com/snow-man-yurigumi-221"),
                ("深澤辰哉のクロムハーツはどれ？愛用の時計と私服ブランド", "https://chomoand-2.com/fukazawa-tatsuya-chrome-hearts-watch-185")])
# ---- ここまで ----

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = blogkit.finalize(out, SITE, NAMES)   # さん付け → ひらがな直し
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
