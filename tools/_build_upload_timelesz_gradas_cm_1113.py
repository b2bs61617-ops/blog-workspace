# -*- coding: utf-8 -*-
"""timelesz ABCマート新CM「MY STYLE MY GRADAS」篇 × 猪俣周杜は映ってる？検証記事(chomoand.com 芸能・トレンド)を組み立てて下書き投稿する(2026-11-13、オシリ依頼)。
usage: python tools/_build_upload_timelesz_gradas_cm_1113.py [--update-content] [--build-only]
状態は articles/timelesz_gradas_cm_posted.json に控え、再実行で重複投稿しない。
"""
import sys, os, json, base64, socket, urllib.request, urllib.error, urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
OUT = os.path.join(REPO, "articles", "timelesz_gradas_cm_1113.html")
POSTED = os.path.join(REPO, "articles", "timelesz_gradas_cm_posted.json")
BASE_TITLE = "timelesz新CMに猪俣周杜は映ってる？8人目の足は誰？"
assert len(BASE_TITLE) <= 35, len(BASE_TITLE)
TITLE = "【未】" + BASE_TITLE
SLUG = "timelesz-abc-mart-gradas-cm-inomata"
CATEGORIES = [37]
AUTHORS = {"USER1": 3, "Tomoki": 4}
EYECATCH = os.path.join(REPO, "images", "timelesz_gradas_cm_eyecatch.png")

A, B, BG = "#9b3d4f", "#e9c3cb", "#fdf4f6"
TH = f"border:1px solid #ccc;padding:8px 12px;background:{A};color:#fff;"
TD = "border:1px solid #ccc;padding:8px 12px;"
TDZ = TD + f"background:{BG};"


def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n'


def html(s):
    return "<!-- wp:html -->\n" + s.strip() + "\n<!-- /wp:html -->\n\n"


def table(head, rows):
    h = "".join(f'<th style="{TH}">{c}</th>' for c in head) if head else ""
    body = ""
    for i, r in enumerate(rows):
        st = TDZ if i % 2 else TD
        body += "<tr>" + "".join(f'<td style="{st}">{c}</td>' for c in r) + "</tr>\n"
    thead = f"<thead><tr>{h}</tr></thead>\n" if head else ""
    return ("<!-- wp:table -->\n<figure class=\"wp-block-table\"><table class=\"has-fixed-layout\">"
            f"{thead}<tbody>\n{body}</tbody></table></figure>\n<!-- /wp:table -->\n\n")


def mini(*kv):
    inner = "".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>' for i, (k, v) in enumerate(kv))
    return html(f'<div style="border:1px solid {B};border-left:4px solid {A};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">{inner}</div>')


def mark(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def xembed(url):
    return ('<!-- wp:embed {"url":"' + url + '","type":"rich","providerNameSlug":"twitter","responsive":true} -->\n'
            '<figure class="wp-block-embed is-type-rich is-provider-twitter wp-block-embed-twitter">'
            f'<div class="wp-block-embed__wrapper">\n{url}\n</div></figure>\n<!-- /wp:embed -->\n\n')


CHK = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {A};border-radius:3px;'
       f'color:{A};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')

ABC_X = "https://x.com/ABCMART_INFO/status/2121030283101458472"
MDPR_X = "https://x.com/modelpress/status/2120954796819771898"
ABC_PAGE = "https://www.abc-mart.net/shop/e/e0001121/"
RAKUTEN_ITEM = "https://item.rakuten.co.jp/abc-mart/7149800001/"
RAKUTEN_IMG = "https://shop.r10s.jp/abc-mart/cabinet/sku-1/sku-3/7149800001.jpg"

import affiliate_box as ab  # noqa: E402
_env = ab.load_keys()
_aff = _env.get("RAKUTEN_AFFILIATE_ID", "")
if _aff:
    q = urllib.parse.quote(RAKUTEN_ITEM, safe="")
    RAKUTEN_AFF = f"https://hb.afl.rakuten.co.jp/hgc/{_aff}/?pc={q}&m={q}"
else:
    RAKUTEN_AFF = RAKUTEN_ITEM
BOX = ab.build_box(RAKUTEN_AFF, RAKUTEN_IMG, "adidas GRADAS 2.0 W LB8420(紺×茶)ABC-MART限定", None,
                   "松島聡・篠塚大輝が履いている色。ほかの3色は公式通販で", B, "GRADAS 2.0 LB8420 紺 茶")

out = ab.NOTICE + "\n\n"
out += p("timeleszが出演するABCマートの新しいCMが、2026年11月13日に公開されました。",
         "アディダスの「GRADAS 2.0」の新色を紹介するCMです。")
out += p("公開直後から、Xでは" + mark("「周杜くんが一瞬映ってる」") + "という声が広がりました。",
         "猪俣周杜は、9月にtimeleszを離れた元メンバーです。",
         "足元のアップが映るシーンでも「8人目の足では？」と話題になっています。")
out += p("結論から言うと、" + mark("足元のアップは今の7人のもの") + "でした。",
         "一方で、冒頭の昔の映像には、観客の影に半分かくれた人物がほんの一瞬映っています。",
         "この記事では、CMの場面を1つずつ見ながら、ファンの声と公式の情報を整理しました。")

out += html(f'''
<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>新CMの内容と公開日</li>
<li>猪俣周杜が映っているといわれる場面</li>
<li>「8人目の足」の正体</li>
<li>靴は何種類？メンバーの着用カラー</li>
<li>購入特典と買える場所</li>
</ul>
</div>''')

# ---- 概要 ----
out += h2("timeleszのABCマート新CMはどんな内容？")
out += mini(("CM名", "「MY STYLE MY GRADAS」篇(約51秒)"),
            ("公開日", "2026年11月13日(金)"),
            ("商品", "アディダス「GRADAS 2.0」新色4色(ABCマート限定)"),
            ("出演", "timelesz(7人)"),
            ("テーマ", "進化"))
out += p("CMの舞台は、レトロな写真館のような空間です。",
         "7人が2人や3人に分かれて、ピンクの背景の前で写真を撮り合います。")
out += p("CMの最初には、これまでのアディダスのCMの映像がスクリーンに流れます。",
         "その映像を、観客の影ごしに見る演出です。",
         "画面には「ずっと変わらない、ぼくらのままで」という言葉も出てきます。")
out += xembed(ABC_X)
out += p("アディダスとtimeleszのキャンペーンは、今回で5回目です。",
         "アンバサダーとしては2年目に入りました。",
         "Xには「起用を続けてくれてありがとう」「さっそく買いました」という声がたくさん届いています。")

# ---- 映ってる？ ----
out += h2("猪俣周杜は映ってる？ファンがざわついた2つの場面")
out += p("ファンの間で話題になっている場面は、大きく分けて2つあります。",
         "冒頭の昔の映像と、足元のアップのシーンです。")
out += h3("場面1：冒頭の振り返り映像(0〜5秒あたり)")
out += p("CMの最初の5秒ほどは、これまでのCM映像をスクリーンで流す場面です。",
         "手前には観客の影があり、スクリーンの一部をかくしています。")
out += p("4秒あたりで、マイクを持った2人のうしろに、" + mark("観客の影に半分かくれた人物") + "がちらっと映ります。",
         "Xではこの場面を切り取って「周杜くん一瞬映ってる！」と投稿する人が何人もいました。")
out += p("ただ、顔がはっきり見えるわけではありません。",
         "ABCマートやアディダスも、この場面について何も説明していません。",
         "そのため、この記事でも本人だとは言い切れません。")
out += p("とはいえ、ちょうど影で顔がかくれる位置なのは確かです。",
         "「影で目立たなくしたのでは」と感じたファンが多かったようです。",
         "「こんなの泣いちゃう」と、思わず胸が熱くなったという声もありました。")

out += h3("場面2：足元のアップは「まさしゅー」？")
out += p("もう1つは、ピンクの背景の前で2人の足元が映る場面(24秒あたり)です。",
         "白いステッチのデニムに白×紺の靴、グレーのスウェットに紺×茶の靴という組み合わせです。")
out += p("この足元を見て、" + mark("「まさしゅー(橋本将生さんと猪俣周杜さん)では？」") + "という声が上がりました。",
         "「まさしゅー」は、橋本将生と猪俣周杜の2人を呼ぶときのファンの呼び名です。")
out += p("しかし、この直前の19〜20秒あたりに、同じ2人の全身が映っています。",
         "ベージュのジャケットの人と、紺のカーディガンに白いタートルネックの人です。",
         "ズボンも靴も足元のアップと同じなので、" + mark("足元は今の2人を寄りで撮ったもの") + "だと分かります。")
out += p("ABCマートの公式ページには、メンバーごとの「着用カラー」が書かれています。",
         "白×紺(LB8421)を履いているのは菊池風磨と橋本将生です。",
         "紺×茶(LB8420)を履いているのは松島聡と篠塚大輝です。")
out += p("インタビューでも、橋本将生と篠塚大輝はおたがいの成長について話していました。",
         "公式の着用カラーとあわせると、" + mark("この足元は橋本将生と篠塚大輝の可能性が高い") + "です。",
         "少なくとも、昔の映像を使った場面ではありません。")

out += h3("足は8人分あるの？")
out += p("CMには、暗い床の上で足元を横に流して映すシーンもあります(5〜10秒あたり)。",
         "ここでも「数えたら8人いる」という声がありました。")
out += p("実際に見てみると、靴とズボンの組み合わせは6〜7人分です。",
         "ただ、同じ人の右足と左足が別の人に見えるところもあり、人数ははっきりしません。",
         "暗いシーンの服装も、ほかの場面の7人とよく似ています。")
out += p("今のところ、" + mark("足元で8人目がいると言える決め手はない") + "というのが、この記事の結論です。")

# ---- 背景 ----
out += h2("なぜ猪俣周杜の名前が出たの？")
out += p("猪俣周杜は、2025年にオーディションをへてtimeleszに加わったメンバーでした。",
         "2026年9月までは8人で活動していました。")
out += table(("日付", "出来事"), [
    ("2026年9月14日", "8人でのアディダス「TEKWEN」CMが公開"),
    ("2026年9月19日", "猪俣周杜が傷害の疑いで逮捕。CMが見られなくなる"),
    ("2026年9月30日", "事務所との契約が解除される"),
    ("2026年10月21日", "不起訴(起訴猶予)に"),
    ("2026年11月13日", "7人での新CMが公開"),
])
out += p("9月のCMは、公開からわずか5日で見られなくなりました。",
         "事務所は、ほかの7人はこの件を知らず、関わってもいないと発表しています。")
out += p("そこから約2か月で、ABCマートは7人のtimeleszを続けて起用しました。",
         "ファンからは「すぐにまた起用してくれてありがたい」という声が多く上がっています。",
         "新CMやインタビューの中で、猪俣周杜について触れた部分はありません。")

# ---- 靴 ----
out += h2("靴は何種類？新色4色とメンバーの着用カラー")
out += p("「靴は7種類あるの？」という疑問も見かけましたが、" + mark("新色は4色") + "です。",
         "CMの最後に並ぶ靴も、4色が2足ずつ写っています。",
         "7人がこの4色を分けて履いているので、たくさんあるように見えます。")
out += table(("色", "型番", "値段(税込)"), [
    ("茶×ピンクライン", "LC1384", "8,250円"),
    ("ベージュ×白ライン", "LC1383", "8,250円"),
    ("白×紺ライン", "LB8421", "8,250円"),
    ("紺×茶ライン", "LB8420", "8,250円"),
])
out += p("メンバーが履いている色と、写真で手に持っている色はちがうことがあります。",
         "ABCマートの公式ページに書かれている色をまとめると、次のとおりです。")
out += table(("メンバー", "履いている色", "手に持っている色"), [
    ("佐藤勝利", "茶×ピンク", "ベージュ"),
    ("菊池風磨", "白×紺", "紺×茶"),
    ("松島聡", "紺×茶", "茶×ピンク"),
    ("寺西拓人", "ベージュ", "白×紺"),
    ("原嘉孝", "ベージュ", "ベージュ"),
    ("橋本将生", "白×紺", "紺×茶"),
    ("篠塚大輝", "紺×茶", "茶×ピンク"),
])
out += p("推しと同じ色を選ぶなら、履いている色と持っている色のどちらにするか迷いそうです。",
         "いちばん人気が集まりそうなのは、2人ずつが履いている白×紺と紺×茶ですね。")
out += h3("どこで買える？")
out += p("GRADAS 2.0は" + mark("ABCマート限定") + "の商品です。",
         "全国のABCマートのお店と、ABCマートの公式オンラインストアで買えます。",
         "オンラインでは、4色それぞれ1人1足までです。")
out += p("11月13日の時点で、楽天市場のABCマートのお店には紺×茶(LB8420)が出ています。")
out += BOX
out += p("ほかの3色は、" + f'<a href="{ABC_PAGE}" target="_blank" rel="noopener">ABCマートの特設ページ</a>' + "から見られます。",
         "限定商品なので、ほかのお店の高い転売品には気をつけてください。")

# ---- 特典 ----
out += h2("購入特典はある？")
out += mini(("特典", "GRADAS×timeleszオリジナルノベルティ"),
            ("対象", "GRADAS 2.0の新色4色(LB8420・LB8421・LC1383・LC1384)"),
            ("もらえる数", "対象の靴1足につき1つ"),
            ("期間", "11月13日以降の注文から。なくなりしだい終了"))
out += p("新色を買うと、" + mark("timeleszのオリジナルノベルティ") + "がもらえます。",
         "数に限りがあり、なくなりしだい終わります。",
         "返品するときは、ノベルティもいっしょに返す決まりです。")
out += p("お店では、メンバー1人ずつのソロビジュアルも飾られています。",
         "さらに、お店の中だけで流れるメンバーの音声もあります。")
out += xembed(MDPR_X)

# ---- インタビュー ----
out += h2("インタビューでメンバーは何を話した？")
out += p("新CMにあわせて、メンバーのインタビューも公開されました。",
         "テーマは「進化」です。")
out += p("「いちばん成長したと思うメンバーは？」という質問では、橋本将生が篠塚大輝の名前を挙げました。",
         "「色気が出てきて進化している」「髪の毛がめちゃくちゃ伸びた」と話しています。")
out += p("篠塚大輝は、橋本将生について「昔と比べて、声が大きくなったよね」と返しました。",
         "おたがいをよく見ている2人らしいやりとりです。")
out += p("ほかにも、菊池風磨は「訂正する二重線は、無意識に3本にしてますね」とアディダス愛を明かしました。",
         "寺西拓人は「GRADASの進化も、timeleszの進化も見守っていてほしい」と呼びかけています。")

# ---- 歩み ----
out += h2("これまでのアディダスとtimeleszのキャンペーン")
out += table(("時期", "内容"), [
    ("2025年4月", "「CLIMACOOL BOUNCE」のキャンペーンに登場"),
    ("2026年春", "「GRADAS 2.0」のキャンペーン(8人)"),
    ("2026年9月", "「TEKWEN」のCM「さあ、いこう」篇(8人、5日で見られなくなる)"),
    ("2026年11月", "「GRADAS 2.0」新色のCM「MY STYLE MY GRADAS」篇(7人)"),
])
out += p("今回のCMの冒頭に流れる昔の映像は、こうしたキャンペーンの思い出をふり返るものです。",
         "「1年目からの歩みを感じてジーンときた」という感想も多く見られました。")

# ---- まとめ ----
out += h2("まとめ")
items = [
    "timeleszのABCマート新CMは2026年11月13日に公開。出演は7人",
    "冒頭の昔の映像に、観客の影に半分かくれた人物が一瞬映る",
    "その人物が猪俣周杜かどうかは、公式の説明がなく分からない",
    "「まさしゅー」といわれた足元は、今の2人(橋本将生と篠塚大輝の可能性が高い)",
    "新色は4色で各8,250円。買うとオリジナルノベルティがもらえる",
]
out += html(f'<div style="border:1px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">'
            + "".join(f'<p style="margin:{"0" if i == 0 else "6px 0 0 0"};">{CHK}{t}</p>' for i, t in enumerate(items)) + "</div>")
out += p("足元の8人目は今の2人でしたが、ファンが何度も見返したくなる気持ちはよく分かります。",
         "7人の新しいスタートを、おそろいのGRADASで応援したいですね。",
         "新しい情報が出たら、この記事に追記します。")

from honorific import add_san  # noqa: E402
out = add_san(out, "ko1keyz", ["佐藤勝利", "菊池風磨", "松島聡", "寺西拓人", "原嘉孝", "橋本将生", "篠塚大輝", "猪俣周杜"])
import easy_read  # noqa: E402
out = easy_read.fix(out)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(out)
print(OUT, len(out))
if "--build-only" in sys.argv:
    sys.exit()

# ================= upload =================
env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_TREND_USERNAME']}:{env['WP_TREND_APP_PASSWORD']}".encode()).decode()
host = socket.gethostname().split(".")[0]
AUTHOR = next((v for k, v in AUTHORS.items() if host.lower().startswith(k.lower())), None)
if AUTHOR is None:
    sys.exit(f"hostname {host} の投稿者がdocs/wordpress.mdの表に無いワン")


def req(path, data=None, headers=None, method="POST"):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode('utf-8', 'ignore')[:500]}")


def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})


state = json.load(open(POSTED, encoding="utf-8")) if os.path.exists(POSTED) else {}


def save():
    json.dump(state, open(POSTED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if "post" in state:
    if "--update-content" in sys.argv:
        jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"title": TITLE, "content": out, "status": "draft"})
        print("content updated", state["post"])
    else:
        print("already posted", state["post"])
else:
    po = jpost("/wp-json/wp/v2/posts", {"title": TITLE, "content": out, "slug": SLUG, "status": "draft",
                                        "categories": CATEGORIES, "author": AUTHOR})
    state["post"] = po["id"]
    save()
    print("draft", po["id"])
if "eyecatch" not in state and os.path.exists(EYECATCH):
    fn = os.path.basename(EYECATCH)
    m = req("/wp-json/wp/v2/media", open(EYECATCH, "rb").read(),
            {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{fn}"'})
    jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": "timelesz ABCマート 新CM GRADAS 2.0"})
    state["eyecatch"] = m["id"]
    save()
    jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"featured_media": state["eyecatch"]})
po = req(f"/wp-json/wp/v2/posts/{state['post']}?context=edit", method="GET")
print(po["id"], po["status"], po["author"], po["categories"], po["featured_media"], po["title"]["raw"])
print("content has GRADAS table:", "LB8420" in po["content"]["raw"], "len", len(po["content"]["raw"]))
print(f"{BASE}/?p={po['id']}")
