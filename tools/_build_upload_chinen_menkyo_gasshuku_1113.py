# -*- coding: utf-8 -*-
"""知念侑李の免許合宿の場所(いのありちねん)記事(chomoand.com 芸能・トレンド)を組み立てて下書き投稿する(2026-11-13、オシリ依頼)。
usage: python tools/_build_upload_chinen_menkyo_gasshuku_1113.py [--update-content] [--build-only]
状態は articles/chinen_menkyo_gasshuku_posted.json に控え、再実行で重複投稿しない。
"""
from urllib.parse import quote
import sys, os, json, base64, socket, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "articles", "chinen_menkyo_gasshuku_1113.html")
POSTED = os.path.join(REPO, "articles", "chinen_menkyo_gasshuku_posted.json")
BASE_TITLE = "【いのありちねん】知念侑李の免許合宿はどこ？浜松自動車学校が有力"
assert len(BASE_TITLE) <= 35, len(BASE_TITLE)
TITLE = "【未】" + BASE_TITLE
SLUG = "chinen-yuri-menkyo-gasshuku-inoarichinen"
CATEGORIES = [37]
AUTHORS = {"USER1": 3, "Tomoki": 4}
EYECATCH = os.path.join(REPO, "images", "chinen_menkyo_gasshuku_eyecatch.png")

A, B, BG = "#c2410c", "#f2c9a8", "#fff7ef"
TH = f"border:1px solid #ccc;padding:8px 12px;background:{A};color:#fff;"
TD = "border:1px solid #ccc;padding:8px 12px;"
TDZ = TD + f"background:{BG};"


def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n'


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


def youtube(url):
    return ('<!-- wp:embed {"url":"' + url + '","type":"video","providerNameSlug":"youtube","responsive":true,'
            '"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->\n'
            '<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">'
            f'<div class="wp-block-embed__wrapper">\n{url}\n</div></figure>\n<!-- /wp:embed -->\n\n')


CHK = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {A};border-radius:3px;'
       f'color:{A};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')

def xembed(url):
    return ('<!-- wp:embed {"url":"' + url + '","type":"rich","providerNameSlug":"twitter","responsive":true} -->\n'
            '<figure class="wp-block-embed is-type-rich is-provider-twitter wp-block-embed-twitter">'
            f'<div class="wp-block-embed__wrapper">\n{url}\n</div></figure>\n<!-- /wp:embed -->\n\n')


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n'



def gmap(q):
    return html(f'<iframe src="https://www.google.com/maps?q={quote(q)}&output=embed" width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy"></iframe>')


ABEMA_X = "https://x.com/ABEMA/status/2121075590698574078"
MDPR_X = "https://x.com/modelpress/status/2121075590904320193"
MDPR_X2 = "https://x.com/modelpress/status/2121076167642149251"
ORICON_X = "https://x.com/oricon/status/2121075598093382123"
SCHOOL = "https://gasyukumenkyo.com/school/14904/"

out = ""
out += p("Hey! Say! JUMPの伊野尾慧・有岡大貴・知念侑李の3人によるABEMAの新番組『いのありちねん』。",
         "この番組が、" + mark("2026年11月18日(水)よる10時から配信スタート") + "します。")
out += p("番組の中で、知念侑李は" + mark("運転免許をとるために免許合宿に参加") + "しました。",
         "ファンの間では「どこの教習所なの？」と話題になっています。",
         "この記事では、番組の内容と、知念侑李が参加した合宿所がどこなのかを調べました。")

out += html(f'''
<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>『いのありちねん』の配信日と内容</li>
<li>知念侑李が参加した免許合宿の場所</li>
<li>合宿所だと考えられる理由</li>
<li>予告で分かった合宿の様子</li>
<li>取材会での3人の話</li>
</ul>
</div>''')

# ---- 番組概要 ----
out += h2("いのありちねんはどんな番組？")
out += mini(("番組名", "『いのありちねん』"),
            ("配信開始", "2026年11月18日(水)よる10時〜"),
            ("配信", "ABEMAで無料独占配信"),
            ("回数", "全9回"),
            ("出演", "伊野尾慧・有岡大貴・知念侑李(Hey! Say! JUMP)"))
out += p("『いのありちねん』は、30代になった3人による" + mark("「大人の放課後」バラエティ") + "です。",
         "Hey! Say! JUMPとして走り続けて、もうすぐ20年。",
         "3人がこれまでできなかったことや、今だからこそやってみたいことに挑戦します。")
out += p("番組の放送が決まったと発表されたのは、2026年4月です。",
         "ABEMA開局10周年の特別番組『30時間限界突破フェス』の中で伝えられました。",
         "発表から半年以上がたち、ようやく配信日が決まりました。")
out += xembed(ABEMA_X)
out += h3("3人それぞれの挑戦")
out += table(("メンバー", "挑戦する内容"), [
    ("伊野尾慧", "Hey! Say! JUMPの新曲を作ってもらうため、フィリピンへ。現地のアーティストにアポなしでお願いしに行く"),
    ("知念侑李", "運転免許をとるため、一般の受講生と一緒に寝泊まりする免許合宿に参加"),
    ("有岡大貴", "これからロケの予定。内容はまだひみつ"),
])
out += p("伊野尾慧のフィリピンロケは「本当にプランゼロ」だったそうです。",
         "現地のテレビ局にも入りこみ、番組の観覧に参加したり、とつぜんステージに上がったりと、波乱の展開が待っています。")
out += p("有岡大貴は「いろいろ計画してるものがありますので、もう少しだけお待ちください！」と話していて、どんな挑戦になるのか楽しみですね。")

# ---- 合宿所 ----
out += h2("知念侑李の免許合宿はどこ？")
out += p("オリコンニュースによると、知念侑李が参加したのは" + mark("静岡県浜松市の自動車教習所") + "です。",
         "浜松市は、知念侑李が中学1年生まで暮らしていた場所です。",
         "長年の夢だった運転免許を、地元の教習所でとることにしたようです。")
out += xembed(MDPR_X)
out += p("番組から教習所の名前は発表されていません。",
         "ただ、予告映像にうつっているものから、" + mark("浜松自動車学校 浜松校が有力") + "だと考えられます。")
out += h3("浜松自動車学校だと考えられる理由")
reasons = [
    "予告の教習車に「Hamaji」「Hamamatsu Driving School」の文字",
    "教習車の後ろにも「浜松 自動車学校」の文字",
    "「浜松市の教習所」という報道と場所が合う",
    "予告の2段ベッドの4人部屋が、学校の宿舎「コミュニティコート」とそっくり",
    "大きな窓と白いイスがならぶ食堂も、学校の写真と似ている",
]
out += html(f'<div style="border:1px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">'
            + "".join(f'<p style="margin:{"0" if i == 0 else "6px 0 0 0"};">{CHK}{t}</p>' for i, t in enumerate(reasons)) + "</div>")
out += p("いちばん大きな手がかりは、" + mark("知念侑李が脱輪させた教習車") + "です。",
         "車の横には「Hamaji」という大きなロゴと「Hamamatsu Driving School」の文字が入っています。",
         "「ハマジ」は、浜松自動車学校のロゴに使われている名前です。")
out += p("また、予告では知念侑李がほかの受講生と2段ベッドの部屋で話す場面があります。",
         "浜松自動車学校には、校舎の敷地の中に男女別の宿舎があり、4人で泊まる部屋も用意されています。",
         "木の2段ベッドや白い机のつくりが、学校が公開している4人部屋の写真とよく似ています。")
out += p("駐車場には「ENTETSU(遠鉄)」と書かれた教習車もうつっていました。",
         "浜松自動車学校は遠鉄グループの教習所とされているので、ここも話が合います。")
out += h3("浜松自動車学校 浜松校ってどんなところ？")
out += gmap("浜松自動車学校 静岡県浜松市中央区丸塚町1")
out += table(None, [
    ("<strong>名前</strong>", "浜松自動車学校 浜松校"),
    ("<strong>住所</strong>", "静岡県浜松市中央区丸塚町1"),
    ("<strong>アクセス</strong>", "浜松駅から送迎バスあり(東海道新幹線で東京から約1時間半)"),
    ("<strong>最短の日数</strong>", "普通車ATは最短15日、MTは最短17日"),
    ("<strong>宿泊</strong>", "敷地内に男女別の宿舎(シングル・ツイン・4人部屋)。ホテルに泊まるプランもあり"),
    ("<strong>とれる免許</strong>", "普通車のほか、中型・大型特殊など"),
])
out += p("浜松自動車学校は、合宿免許の受け入れもしている教習所です。",
         "校舎の中には食堂があり、日がわりのメニューが食べられます。",
         "まわりにはコンビニやスーパーもあり、合宿中も過ごしやすい場所です。")
out += p("合宿のプランや空き状況は、" + f'<a href="{SCHOOL}" target="_blank" rel="noopener">合宿免許の予約サイト</a>' + "で見られます。")

# ---- 様子 ----
out += h2("予告で分かった免許合宿の様子")
out += h3("脱輪してパニックに")
out += p("予告では、知念侑李が運転する教習車のタイヤが道からはずれてしまう場面がありました。",
         "テロップは" + mark("「脱輪王」") + "。",
         "運転席であわてる知念侑李には「パニック」の文字がついていました。")
out += p("教習のあと、知念侑李は「S字道路の緊張なのか、前回の授業の後半からずっと頭痛かった」と話しています。",
         "この話には「言い訳」というテロップがつけられ、ファンの笑いをさそっていました。")
out += h3("32歳のぼっち飯から、仲間と打ちとけるまで")
out += p("食堂では、ひとりでご飯を食べる知念侑李に" + mark("「32歳のぼっち飯」") + "というテロップが入りました。",
         "人見知りな一面がよく出ている場面です。")
out += p("でも、合宿が進むと、同じ部屋の受講生たちと一緒にご飯を食べるようになります。",
         "予告の最後には「自分になかったもの、もう忘れてしまったもの、それを持ってる人と一緒にいられた」という言葉も。",
         "「出会いと別れ」というテロップもあり、仲間との別れの場面もありそうです。")
out += p("知念侑李は取材会で「本当に免許を取れるのかというところと、人見知りの知念がどういう風に過ごしたのか、そこも楽しんでいただけたら」と話しています。")

# ---- 取材会 ----
out += h2("取材会での3人の話")
out += h3("助手席に乗せたいのは髙木雄也")
out += p("免許をとったら助手席に乗せたいメンバーを聞かれ、知念侑李は" + mark("髙木雄也") + "の名前をあげました。",
         "理由は「安心感は欲しいというか、技術的にも優れている髙木さんとかを乗せて、何かアドバイスをいただきたい」というものでした。")
out += h3("伊野尾慧「最近見た映像で1番面白かった」")
out += p("伊野尾慧と有岡大貴は、知念侑李の合宿の映像にすっかりハマったようです。",
         "伊野尾慧は" + mark("「最近見た映像で1番面白かった」") + "と話しています。",
         "有岡大貴も、知念侑李のロケを「めちゃめちゃ自然体だった」と笑顔でふり返りました。")
out += p("ふたりは「知念を1人にするのがあんなに面白いとは思わなかった」とも話していました。",
         "知念侑李は「2人以外と絡まないロケがいいっすね」と言っていましたが、「どうやら叶わなそうです」と苦笑いしていました。")
out += xembed(ORICON_X)
out += h3("3人の役割は？")
out += table(("メンバー", "役割"), [
    ("知念侑李", "潤滑油"),
    ("伊野尾慧", "太陽"),
    ("有岡大貴", "サンドバッグ・緩衝材"),
])
out += p("伊野尾慧は知念侑李について「メンバーとメンバーの橋渡しやグループの空気感を知念が担っているんじゃないかな」と話しました。",
         "有岡大貴のことは「サンドバッグみたいに、なんでも受け止めてくれる」、自分のことは「明るくて、みんなを照らしている」と語っています。")
out += xembed(MDPR_X2)

# ---- まとめ ----
out += h2("まとめ")
items = [
    "『いのありちねん』は2026年11月18日(水)よる10時からABEMAで無料独占配信",
    "知念侑李は運転免許をとるため、地元・浜松市の免許合宿に参加",
    "教習車のロゴや宿舎の様子から、合宿所は浜松自動車学校 浜松校が有力",
    "予告では「脱輪王」「32歳のぼっち飯」など、人見知りな知念侑李の姿も",
    "免許をとったら助手席に乗せたいのは髙木雄也",
]
out += html(f'<div style="border:1px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">'
            + "".join(f'<p style="margin:{"0" if i == 0 else "6px 0 0 0"};">{CHK}{t}</p>' for i, t in enumerate(items)) + "</div>")
out += p("知念侑李が無事に免許をとれたのかは、配信で確かめましょう。",
         "教習所の名前が番組で発表されたら、この記事に追記します。")

sys.path.insert(0, os.path.join(REPO, "tools"))
from honorific import add_san  # noqa: E402
out = add_san(out, "ko1keyz", ["伊野尾慧", "有岡大貴", "知念侑李", "髙木雄也"])
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
    jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": "知念侑李 免許合宿 浜松自動車学校 いのありちねん"})
    state["eyecatch"] = m["id"]
    save()
    jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"featured_media": state["eyecatch"]})
po = req(f"/wp-json/wp/v2/posts/{state['post']}?context=edit", method="GET")
print(po["id"], po["status"], po["author"], po["categories"], po["featured_media"], po["title"]["raw"])
print(f"{BASE}/?p={po['id']}")
