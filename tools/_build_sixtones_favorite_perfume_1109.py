# -*- coding: utf-8 -*-
"""chomoand-0.com: SixTONESメンバーの愛用香水まとめ(2026-11-09 オシリ依頼、トラジャ版 build_and_post_travis_japan_favorite_perfume.py と同じ型)
usage: python tools/_build_sixtones_favorite_perfume_1109.py [--dry]
 1) articles/sixtones_favorite_perfume_1109.html を無彩色で書き出す
 2) honorific.py fix/check → sixtones_theme.py --per-section
 3) 下書き投稿(タイトル先頭【未】)+アイキャッチ(eyecatch_sixtones.py)
"""
import json, base64, os, re, sys, subprocess, socket
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "articles" / "sixtones_favorite_perfume_1109.html"
POSTED = ROOT / "articles" / "sixtones_favorite_perfume_1109_posted.json"
EYECATCH = ROOT / "images" / "sixtones_favorite_perfume_1109_eyecatch.jpg"
DRY = "--dry" in sys.argv

TITLE_BODY = "SixTONESの愛用香水まとめ！田中樹はディオール？北斗の香りも"
TITLE = "【未】" + TITLE_BODY

BAR, BG, BORDER = "#333333", "#f5f5f5", "#d5d5d5"
STRIPE = ('<div style="height:5px;background:linear-gradient(90deg,#d2414f 0%,#d2414f 16%,#d6588a 16%,#d6588a 33%,'
          '#2b2b2b 33%,#2b2b2b 50%,#c99a06 50%,#c99a06 66%,#3a9468 66%,#3a9468 83%,#3a78c9 83%,#3a78c9 100%);"></div>')
MK = {"ジェシー": "#f9cbd0", "京本大我": "#f8cfe0", "松村北斗": "#d6d6d6", "髙地優吾": "#fbe7a1", "森本慎太郎": "#c8ead6", "田中樹": "#cddff6"}


def p(sentences):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(sentences) + "</p>\n<!-- /wp:paragraph -->"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def mk(member, text):
    return (f'<strong><span style="font-size:1.1em;background:linear-gradient(transparent 60%,{MK[member]} 60%);">'
            f'{text}</span></strong>')


def box(title, items, stripe=False):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
{STRIPE if stripe else ""}<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BAR};color:#fff;">{title}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(rows):
    lines = "\n".join(f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
                      for i, (k, v) in enumerate(rows))
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {BAR};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{lines}
</div>''')


def table(header, rows):
    th = "".join(f'<th style="padding:8px;border:1px solid {BORDER};">{c}</th>' for c in header)
    trs = "\n".join("<tr>" + "".join(f'<td style="padding:8px;border:1px solid {BORDER};">{c}</td>' for c in r) + "</tr>"
                    for r in rows)
    return wphtml(f'''<div style="overflow-x:auto;margin:0 0 16px 0;">
<table style="border-collapse:collapse;width:100%;min-width:560px;font-size:0.92em;">
<thead><tr style="background:{BAR};color:#fff;">{th}</tr></thead>
<tbody>
{trs}
</tbody></table></div>''')


def summary(items):
    lis = "\n".join(
        f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {BAR};border-radius:3px;color:{BAR};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{i}</p>'
        for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
{STRIPE}<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BAR};color:#fff;">まとめ</p>
<div style="padding:14px 18px;background:{BG};">
{lis}
</div>
</div>''')


def linkbox(items):
    lis = "\n".join(f'<li><a href="{u}">{t}</a></li>' for u, t in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {BAR};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


A = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
URL_JESSE = "https://chomoand-0.com/jesse-kousui-1206"
URL_SABON = "https://chomoand-0.com/tanaka-juri-sabon-scrub-1178"
URL_DG = "https://mdpr.jp/news/detail/2045446"
URL_SABON_REPORT = "https://www.thefirsttimes.jp/report/0000858781/"
URL_LAVONS = "https://www.advertimes.com/20260928/article558793/"
URL_MUCHA = "https://www.fashionsnap.com/article/2024-10-22/mucha-taiga-kyomoto/"
URL_ACHIKOCHI = "https://www.tv-tokyo.co.jp/plus/entertainment/entry/202602/18416.html"
URL_ANN = "https://mdpr.jp/news/detail/4405662"

b = []

# ---- リード ----
b.append(p([
    "ライブや舞台で近くを通ったとき、「いい匂いがした」とたびたび話題になるSixTONES。",
    "メンバーは香水をどんなふうに使っているのか、雑誌やラジオ、テレビでの発言をさかのぼって調べてみました。",
    "すると、" + mk("田中樹", "田中樹はバニラ系の甘い香り好きで、ディオール「ヒプノティック プワゾン」が有力") + "、"
    + mk("森本慎太郎", "森本慎太郎はジョー マローンのキンモクセイ系") + "、"
    + mk("ジェシー", "ジェシーは2年使い続けた甘い香り") + "と、それぞれのこだわりが見えてきました。",
    "さらに、" + mk("松村北斗", "松村北斗がジュニア時代のジェシーに「寝る前に香水をつけるといい」と教えていた") + "という、ほくじぇファンにはたまらないエピソードもあります。",
    "この記事では、6人それぞれの愛用香水と好きな香り、香りにまつわるお仕事までまとめて紹介します。",
]))
b.append(box("この記事でわかること", [
    "メンバー別の愛用香水・好きな香りの一覧",
    "田中樹とディオール、SABONの関係",
    "森本慎太郎がラジオで話したキンモクセイの香水",
    "ジェシーと松村北斗の「寝る前の香水」エピソード",
    "京本大我・髙地優吾の香りのこだわり",
    "2025年に紹介された6人の最新の香り事情",
], stripe=True))

# ---- 一覧 ----
b.append(h2("SixTONESの愛用香水・好きな香り一覧"))
b.append(p([
    "まずは6人の愛用香水と、本人が話していた好きな香りを一覧にしました。",
    "好きな香りは、2023年8月発売の『Duet』9月号で、メンバーが香りについて答えていた内容がベースです。",
    "銘柄まで本人がはっきり口にしたメンバーは少なく、ほとんどは香りの系統やエピソードが中心です。",
]))
b.append(table(["メンバー", "愛用香水", "好きな香り・ポイント"], [
    ["ジェシー", "2年使い続けている甘い香り(銘柄は非公表)", "甘い香り。2020年にドルチェ＆ガッバーナ「ライトブルー」の広告に起用"],
    ["京本大我", "香水はつけない", "香りのお仕事はカメラマンとして参加(MUCHAのフレグランス)"],
    ["松村北斗", "銘柄は非公表", "甘すぎず、クールすぎない香り。2026年からラボンのアンバサダー"],
    ["髙地優吾", "ネイチャー系の香水を4本目までリピート", "ネイチャー系・ウッディな香り"],
    ["森本慎太郎", "ジョー マローンのキンモクセイ系が有力", "さわやか系からキンモクセイへチェンジ"],
    ["田中樹", "ディオール「ヒプノティック プワゾン」が有力", "バニラ系の甘い香り。2026年からSABONのアンバサダー"],
]))
b.append(p([
    "ここからは、メンバーごとにくわしく見ていきます。",
]))

# ---- 田中樹 ----
b.append(h2("田中樹の愛用香水はディオール「ヒプノティック プワゾン」？"))
b.append(minibox([
    ("愛用香水(有力)", "ディオール「ヒプノティック プワゾン」"),
    ("好きな香り", "バニラ系の甘い香り"),
    ("香りのお仕事", "SABONアンバサダー(2026年8月〜)"),
]))
b.append(p([
    "田中樹の香水として、いちばん名前が挙がるのがディオールの「ヒプノティック プワゾン」です。",
    "1998年に登場したディオールのロングセラーで、ジャスミンとバニラにアーモンドのような甘さが重なる、とろけるような甘い香りが特徴です。",
    "樹さんは2023年の『Duet』で、好きな香りに" + mk("田中樹", "「バニラ系の甘い香り」") + "を挙げていて、ヒプノティック プワゾンはまさにその好みにぴったりの1本と言えます。",
    "ただ、同じアンケートでは「最近はつけない」とも答えていて、本人が商品名まで口にした場面は見つけられなかったので、ここは「有力」としておきます。",
]))
b.append(h3("気になる人のコートに香水を？"))
b.append(p([
    "樹さんの香水エピソードで有名なのが、2024年7月4日放送の『あざとくて何が悪いの？』(テレビ朝日系)で話した恋愛テクニックです。",
    "食事中に相手が席を立ったすきに、相手のコートのすそのほうへ自分の香水を少しだけつけておく、というもの。",
    "コートはあまり洗わないので、数日たって着たときにも香りが残り、自分のことを思い出してもらえるという理屈です。",
    "スタジオではざわつきが起きましたが、それだけ「香りは記憶に残る」と考えているのが伝わってきます。",
]))
b.append(h3("SABONのアンバサダーに就任"))
b.append(p([
    "2026年8月5日には、ボディケアブランド「SABON」のアンバサダーに就任しました。",
    "発表会では、以前からボディスクラブを愛用していることや、理想の休日には" + mk("田中樹", "「映画館へのお出かけ時にはSABONのフレグランスを身にまとう」") + "ことを語っています(" + A(URL_SABON_REPORT, "THE FIRST TIMES") + ")。",
    "帰宅後は映画を観ながらSABONのホームフレグランスも楽しむそうで、部屋の香りにまでこだわる香り好きぶりです。",
    '愛用しているスクラブの香りは「デリケートジャスミン」と「ジェントルマン」で、くわしくは<a href="' + URL_SABON + '">田中樹のSABONの香りを調べた記事</a>でまとめています。',
]))

# ---- 森本慎太郎 ----
b.append(h2("森本慎太郎はジョー マローンのキンモクセイ系"))
b.append(minibox([
    ("愛用香水(有力)", "ジョー マローン ロンドンのキンモクセイ(オスマンサス)系の香り"),
    ("つけ方", "Tシャツのすそをめくって、おなかのあたりにシュッ"),
    ("出典", "TBSラジオ『山里亮太の不毛な議論』(2023年5月31日放送)"),
]))
b.append(p([
    "森本慎太郎は、2023年5月31日放送のTBSラジオ『山里亮太の不毛な議論』にゲスト出演したとき、香水の話をしていました。",
    "当時はドラマ『だが、情熱はある』で山里亮太さんの役を演じていた時期です。",
    "番組では、" + mk("森本慎太郎", "「さわやか系の香水から、キンモクセイのにおいの香水に変えた」") + "と明かし、つけ方は「Tシャツのすそをめくって、おなかのあたりにシュッて吹きかけてる」と話していました。",
    "ブランドはジョー マローン ロンドンで、ジョー マローンのキンモクセイの香りといえば「オスマンサス ブロッサム コロン」があります。",
    "ただし、どの香りかまでは番組でははっきりしていないので、ここは推測です。",
]))
b.append(p([
    "おなかにつけるのは、首や手首よりも香りがやわらかく立ちのぼる、香水上級者のつけ方として知られています。",
    "近くを通ったときにふわっと香るくらいがちょうどいい、という慎太郎さんらしい気づかいかもしれません。",
]))
b.append(h3("好きな香りがジェシー・樹とかぶった"))
b.append(p([
    "慎太郎さんは以前、香水を買いに行ったときのエピソードも話しています。",
    "お店で新作をすすめられ、「これとこれ、いい匂いですね」と答えたら、1つは「ジェシーさんが選んだもの」、もう1つは「樹さんです」と言われたそうです。",
    "「やっぱり好きな匂いって似るんだなと思ったよ」と笑っていて、メンバー同士で香りの好みが近いことがわかるほほえましい話です。",
]))

# ---- ジェシー ----
b.append(h2("ジェシーは2年使い続けた甘い香り"))
b.append(minibox([
    ("愛用香水", "2年使い続けている甘い香り(銘柄は非公表)"),
    ("香りのお仕事", "ドルチェ＆ガッバーナ「ライトブルー オードトワレ」のビジュアル(2020年)"),
]))
b.append(p([
    "ジェシーは2023年の『Duet』で、" + mk("ジェシー", "甘い香りの香水を2年ほど愛用している") + "と答えていました。",
    "ミュージカル『ビートルジュース』やライブで客席の近くを通ったとき、「甘い匂いがした」と話題になるのも納得です。",
    "2020年4月には、ドルチェ＆ガッバーナ ビューティの「ライトブルー オードトワレ」のビジュアルに起用され、撮影のメイキング映像には「美しすぎる」と反響が集まりました(" + A(URL_DG, "モデルプレス") + ")。",
    "ライトブルーはレモンやりんごのさわやかさから始まる香りなので、ふだん使いの「甘い香り」とは別の1本と考えられます。",
    '舞台で話題になった香りについては、<a href="' + URL_JESSE + '">ジェシーの香水を調べた記事</a>でもくわしく書いています。',
]))
b.append(h3("北斗に教わった「寝る前の香水」"))
b.append(p([
    "2024年10月19日放送の『SixTONESのオールナイトニッポンサタデースペシャル』は、ジェシーと松村北斗の2人がパーソナリティを担当した回でした(" + A(URL_ANN, "モデルプレス") + ")。",
    "ジュニア時代の思い出を振り返るなかで、ジェシーが明かしたのが香水のエピソードです。",
    "北斗さんがジェシーの家に泊まりに来たとき、" + mk("松村北斗", "「寝る前に香水つけるといいんだよ。アロマ的な効果もあるし、寝てるときに体に染み込んで翌日いい」") + "と教えてくれたのを覚えている、と話していました。",
    "ジェシーはそのアドバイスを実際に試していたそうで、後輩の北斗さんを「初めて尊敬した」瞬間だったとか。",
    "少年時代の北斗さんがそんな大人びたアドバイスをしていたと思うと、ほほえましいですね。",
]))

# ---- 松村北斗 ----
b.append(h2("松村北斗は甘すぎずクールすぎない香り"))
b.append(minibox([
    ("愛用香水", "銘柄は非公表"),
    ("好きな香り", "甘すぎず、クールすぎない香り"),
    ("香りのお仕事", "ラボンのアンバサダー(2026年9月〜)"),
]))
b.append(p([
    "松村北斗は2023年の『Duet』で、好きな香りを" + mk("松村北斗", "「甘すぎず、クールすぎない香り」") + "と答えていました。",
    "甘い系のジェシー・樹さんと、さわやか系やウッディ系のメンバーのちょうど間くらいの、絶妙なバランスが好みのようです。",
    "先ほどのラジオでは、ジュニア時代はシャネルの「N°5」をつけて寝ていたという話も出ていて、香水を「寝る前につけるもの」として楽しんでいたことがうかがえます。",
]))
b.append(h3("ラボンの新アンバサダーに"))
b.append(p([
    "2026年9月28日には、柔軟剤などのホームケアブランド「ラボン」の新アンバサダーに就任しました(" + A(URL_LAVONS, "AdverTimes") + ")。",
    "約12年続いた玉森裕太さんからのバトンタッチで、新CM「ラボンデイズはじまる篇」は10月1日から全国で放送されています。",
    "CMで使われているのは柔軟剤「シャイニームーンの香り」で、さりげない甘さがさわやかに香るフローラルグリーン系です。",
    "「甘すぎずクールすぎない」という北斗さんの好みにもぴったりの香りなので、同じ香りをまといたい人は柔軟剤から試してみるのもおすすめです。",
]))

# ---- 京本・髙地 ----
b.append(h2("京本大我・髙地優吾の香りのこだわりは？"))
b.append(h3("京本大我は「香水をつけない」派"))
b.append(p([
    "京本大我は2023年の『Duet』で、" + mk("京本大我", "香水はつけない") + "と答えていました。",
    "それでも「香水をつけていないのにいい匂いがする」と言われることがあり、ファンの間ではなぞのひとつになっています。",
    "シャンプーや柔軟剤など、生活の中の香りが自然に残っているのかもしれません。",
]))
b.append(p([
    "香水をつけない一方で、香りのお仕事にはカメラマンとして参加しています。",
    "2024年10月22日発売の「MUCHA(ミュシャ)」のホリデーフレグランス「月と星」では、京本が4種類のオードトワレのビジュアルを撮影しました(" + A(URL_MUCHA, "FASHIONSNAP") + ")。",
    "価格は35mLが各9,790円、10mLが各3,960円です。",
    "2025年のホリデーコレクション「ショコラ・イデアル」でも京本が撮り下ろしたビジュアルが使われていて、香水を「撮る側」で関わっているのが京本らしいところです。",
]))
b.append(h3("髙地優吾はネイチャー系を4本リピート"))
b.append(p([
    "髙地優吾は2023年の『Duet』で、好きな香りを「ネイチャー系でウッディな香り」と答え、" + mk("髙地優吾", "同じ香水がもう4本目に突入している") + "と話していました。",
    "1本を長く使い続けるところに、髙地の一途な性格が出ているようです。",
]))
b.append(p([
    "2026年2月4日放送の『あちこちオードリー』(テレビ東京系)では、友だちやマネージャーに「髙地のニオイがする」と言われ、「俺は臭いのかな」と心配になったエピソードを話していました(" + A(URL_ACHIKOCHI, "テレ東プラス") + ")。",
    "お医者さんにまで相談したそうですが、若林正恭さんは「柔軟剤や香水のにおいでは」と推測。",
    "同じ香水を何年も使い続けているからこそ、まわりの人にとって「髙地の香り」として覚えられているのかもしれません。",
]))

# ---- 2025年の香り事情 ----
b.append(h2("2025年に紹介された6人の最新の香り事情"))
b.append(p([
    "2025年の初めごろには、メンバーの最近の香りの好みも紹介されていました。",
    "2023年の『Duet』のころから変わっているメンバーもいるので、くらべながら見てみてください。",
]))
b.append(table(["メンバー", "2025年に紹介された香り"], [
    ["ジェシー", "やさしくて甘い、スモーキーな香り"],
    ["京本大我", "香りにはこだわりなし。舞台中は入浴剤「きき湯」をまとめ買い"],
    ["松村北斗", "夏はレモングラスやユーカリの虫よけアロマをたく"],
    ["髙地優吾", "季節を問わず、同じ柑橘系の香りを使う"],
    ["森本慎太郎", "5、6年同じウッド系の香りを使う"],
    ["田中樹", "甘めとさわやかの2種類を使い分け"],
]))
b.append(p([
    "ジェシーは2023年から変わらず「甘い香り」派で、スモーキーさが加わった大人っぽい香りになっているようです。",
    "京本大我は相変わらず香水へのこだわりはなく、舞台の期間中は「きき湯」をまとめ買いして、お風呂で体をいたわるのが習慣とのこと。",
    "香水をつけないのに「いい匂い」と言われる理由は、もしかするとお風呂の時間にあるのかもしれません。",
]))
b.append(p([
    "松村北斗は、香水というより部屋で楽しむアロマ派。",
    "夏はレモングラスやユーカリの虫よけアロマをたいているそうで、すっきりした草木系の香りは「甘すぎずクールすぎない」好みにも通じます。",
    "髙地優吾は季節を問わず同じ柑橘系を使っていて、2023年に話していた「同じ香水を4本目」というリピート派ぶりは変わっていません。",
]))
b.append(p([
    "森本慎太郎は「5、6年同じウッド系」と紹介されていて、ラジオで話したキンモクセイの香水と使い分けているのか、香りの系統が変わったのかは気になるところです。",
    "田中樹は「甘めとさわやかの2種類」を使い分けていて、バニラ系の甘い香りと、SABONのボディスクラブ「ジェントルマン」のようなすっきり系をオンとオフで楽しんでいるのかもしれません。",
]))

# ---- まとめ ----
b.append(h2("まとめ"))
b.append(summary([
    "田中樹はバニラ系の甘い香り好き。ディオール「ヒプノティック プワゾン」が有力で、2026年からSABONのアンバサダー",
    "森本慎太郎はラジオで、さわやか系からジョー マローンのキンモクセイ系に変えたと明かした",
    "ジェシーは甘い香りを2年愛用。ジュニア時代に北斗から「寝る前の香水」を教わった",
    "松村北斗は甘すぎずクールすぎない香りが好み。2026年からラボンのアンバサダー",
    "京本大我は香水をつけない派、髙地優吾はネイチャー系の香水を4本目までリピート",
]))
b.append(p([
    "同じグループでも、甘い香り派・さわやか派・つけない派と、香りの楽しみ方は6人それぞれでした。",
    "推しの好きな香りをまとってライブに行けば、いつもとは違うドキドキが味わえそうですね。",
    "新しい情報がわかったら、この記事に追記していきます。",
]))
b.append(linkbox([
    (URL_JESSE, "ジェシーの香水は何？ビートルジュースで甘い匂いと話題！"),
    (URL_SABON, "田中樹のSABONの香りはどれ？愛用スクラブと使い方！"),
    ("https://chomoand-0.com/sixtones-vmaj2026-1203", "SixTONESのVMAJ2026の4冠は何？受賞曲と放送日まとめ！"),
]))

content = "\n\n".join(b)
OUT.write_text(content, encoding="utf-8")
print("title len (without 【未】):", len(TITLE_BODY))


def run(*args):
    r = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    print(r.stdout[-800:], r.stderr[-800:])
    if r.returncode != 0:
        sys.exit(f"failed: {args}")


run(ROOT / "tools" / "honorific.py", "fix", "--group", "sixtones", "--names", "山里亮太,玉森裕太,若林正恭", OUT)
run(ROOT / "tools" / "honorific.py", "check", "--group", "sixtones", OUT)
run(ROOT / "tools" / "sixtones_theme.py", OUT, "--per-section")
content = OUT.read_text(encoding="utf-8")
plain = re.sub(r"<!--.*?-->|<[^>]+>", "", content, flags=re.S)
print("chars:", len(re.sub(r"\s", "", plain)))
if DRY:
    sys.exit()

env = {}
for line in open(ROOT / ".env", encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_AUDITION_URL"].rstrip("/")
AUTH = {"Authorization": "Basic " + base64.b64encode(f"{env['WP_AUDITION_USERNAME']}:{env['WP_AUDITION_APP_PASSWORD']}".encode()).decode()}
AUTHORS = {"USER1": 2, "Tomoki": 1, "Yuka-MacBook-NEO": 1}
host = socket.gethostname().split(".")[0]
AUTHOR = next((v for k, v in AUTHORS.items() if host.lower().startswith(k.lower())), 2)

posted = json.loads(POSTED.read_text(encoding="utf-8")) if POSTED.exists() else {}
if "post_id" in posted:
    r = requests.post(f"{BASE}/wp-json/wp/v2/posts/{posted['post_id']}", headers=AUTH, json={"content": content})
    r.raise_for_status()
    print("UPDATED", posted["post_id"])
    sys.exit()

r = requests.post(f"{BASE}/wp-json/wp/v2/posts", headers=AUTH, json={
    "title": TITLE, "content": content, "status": "draft", "slug": "sixtones-favorite-perfume",
    "categories": [15, 16, 17, 18, 19, 20, 21], "author": AUTHOR})
r.raise_for_status()
post = r.json()
posted["post_id"] = post["id"]
POSTED.write_text(json.dumps(posted, ensure_ascii=False, indent=2), encoding="utf-8")
print("POST_ID", post["id"], post["status"], post["link"])

eye = subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_sixtones.py"), "--main", "愛用香水",
                      "--bottom", "田中樹はディオール？", "--bottom", "北斗・慎太郎の香りも",
                      "--color-key", "group", "--out", str(EYECATCH)],
                     capture_output=True, text=True, encoding="utf-8", errors="replace")
print(eye.stdout[-300:], eye.stderr[-300:])
if eye.returncode == 0:
    m = requests.post(f"{BASE}/wp-json/wp/v2/media", headers={**AUTH, "Content-Type": "image/jpeg",
                      "Content-Disposition": f'attachment; filename="{EYECATCH.name}"'}, data=EYECATCH.read_bytes())
    m.raise_for_status()
    requests.post(f"{BASE}/wp-json/wp/v2/posts/{post['id']}", headers=AUTH,
                  json={"featured_media": m.json()["id"], "status": "draft"}).raise_for_status()
    print("eyecatch media", m.json()["id"])
print("DONE")
