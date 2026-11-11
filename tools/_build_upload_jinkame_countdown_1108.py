# -*- coding: utf-8 -*-
"""亀梨和也×赤西仁 jinkame.com カウントダウン記事(chomoand.com 芸能・トレンド)を組み立てて下書き投稿する(2026-11-08、オシリ依頼)。
usage: python tools/_build_upload_jinkame_countdown_1108.py [--update-content] [--build-only]
状態は articles/jinkame_countdown_posted.json に控え、再実行で重複投稿しない。
方針: 何が発表されるかは未発表なので予想は予想と明記する。
"""
import sys, os, json, base64, socket, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "articles", "jinkame_countdown_1108.html")
POSTED = os.path.join(REPO, "articles", "jinkame_countdown_posted.json")
BASE_TITLE = "亀梨和也と赤西仁が18年ぶりライブ！チケット申込方法は？"
assert len(BASE_TITLE) <= 35, len(BASE_TITLE)
TITLE = "【未】" + BASE_TITLE
SLUG = "kamenashi-akanishi-jinkame-countdown"
CATEGORIES = [37]
AUTHORS = {"USER1": 3, "Tomoki": 4}
EYECATCH = os.path.join(REPO, "images", "jinkame_countdown_eyecatch.png")

A, B, BG = "#2c2924", "#cfc6b8", "#f8f5ef"
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


KAME_X = "https://x.com/K_KAMEofficial/status/2119399539958251525"
JIN_X = "https://x.com/Jin_Akanishi/status/2119399545532776926"

MAP = ('<iframe src="https://maps.google.com/maps?q=K%E3%82%A2%E3%83%AA%E3%83%BC%E3%83%8A%E6%A8%AA%E6%B5%9C&z=15&output=embed" '
       'width="100%" height="320" style="border:0;max-width:100%;" allowfullscreen="" loading="lazy"></iframe>')
JIN_NEWS = "https://jinakanishi.com/news/detail/1093"

out = ""
out += p("亀梨和也と赤西仁が、" + mark("2027年8月18日・19日にKアリーナ横浜で2人のライブを開く") + "ことを発表しました。",
         "2人がそろってライブをするのは、18年ぶりです。",
         "11月8日から続いていたjinkame.comのカウントダウンが、11月11日の朝6時に終わり、この発表が出ました。")
out += p("チケットは、2人それぞれのファンクラブで先に申し込みを受け付ける予定です。",
         "この記事では、ライブの日程と会場、チケットの申し込み方法、カウントダウンから発表までの流れをまとめました。")

out += html(f'''
<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>仁亀ライブの日程と会場</li>
<li>チケットの申し込み方法</li>
<li>Kアリーナ横浜への行き方</li>
<li>カウントダウンから発表までの流れ</li>
<li>11月8日と11月11日が選ばれた理由</li>
<li>仁亀のこれまでの歩みとファンの反応</li>
</ul>
</div>''')

# ---- 発表 ----
out += h2("仁亀ライブの日程と会場は？")
out += mini(("公演名", "KAZUYA KAMENASHI - JIN AKANISHI LIVE 2027"), ("日程", "2027年8月18日(水)・19日(木)の2日間"),
            ("会場", "Kアリーナ横浜(神奈川県)"), ("発表日", "2026年11月11日(水)朝6時"),
            ("公式サイト", "jinkame.com"))
out += p("11月11日の朝6時、jinkame.comのカウントダウンが0になり、ライブの開催が発表されました。",
         "公演名は「KAZUYA KAMENASHI - JIN AKANISHI LIVE 2027」です。",
         "日程は2027年8月18日(水)と19日(木)の2日間で、会場はKアリーナ横浜です。")
out += p("2人がそろってライブのステージに立つのは、" + mark("2009年以来、18年ぶり") + "と報じられています。",
         "発表からおよそ9か月後の、夏休みシーズンのライブになります。")
out += h3("カウントダウンの「×」が「-」に変わった")
out += p("発表と同時に、サイトの見た目にも変化がありました。",
         "カウントダウン中は2人の名前の間が「×」でしたが、発表後は" + mark("「-(ハイフン)」") + "に変わったのです。")
out += p("ハイフンは、KAT-TUNのファンの呼び名でもあります。",
         "このことに気づいたファンが多く、Xでは「仁亀ライブ」と並んで「ハイフン」がトレンド入りしました。",
         "「ハイフンを大事にしてくれている」「カウントダウンがハイフンになるの天才」という声が上がっています。")

# ---- チケット ----
out += h2("仁亀ライブのチケットの申し込み方法は？")
out += p("チケットは、" + mark("2人のファンクラブで先に申し込みを受け付ける予定") + "です。",
         "対象となるのは、次の2つの会員です。")
out += table(("ファンクラブ", "先行の対象"), [
    ("亀梨和也のオフィシャルファンクラブ", "W会員"),
    ("赤西仁のオフィシャルファンクラブ「JIP's」", "プレミアム会員"),
])
out += p("申し込みの日程や値段など、くわしい内容は後日発表とされています。",
         "赤西仁の公式サイトによると、JIP'sにこれから入る人は、通常会員とプレミアム会員の両方に登録が必要です。",
         "プレミアム会員の受付期間中に入会すれば、先行に申し込めると案内されています。")
out += p("なお、会場への問い合わせはしないよう呼びかけられています。",
         "最新の情報はjinkame.comで発表されるので、こまめにチェックしておきましょう。")
out += table(None, [
    ("<strong>ライブの公式サイト</strong>", "jinkame.com"),
    ("<strong>赤西仁のお知らせ</strong>", f'<a href="{JIN_NEWS}" target="_blank" rel="noopener">jinakanishi.com</a>'),
    ("<strong>亀梨和也のX</strong>", "@K_KAMEofficial"),
    ("<strong>赤西仁のX</strong>", "@Jin_Akanishi"),
])

# ---- 会場 ----
out += h2("会場のKアリーナ横浜はどこ？")
out += mini(("収容人数", "約2万人"), ("最寄り駅", "みなとみらい線 新高島駅から歩いて約5分"),
            ("横浜駅から", "東口から歩いて約11分"))
out += p("Kアリーナ横浜は、横浜のみなとみらいにある音楽専用のアリーナです。",
         "約2万人が入れる大きな会場で、どの席からもステージが見やすい作りになっています。")
out += p("新高島駅からは歩いて約5分、JR横浜駅の東口からは歩いて約11分です。",
         "新横浜駅の近くにある「横浜アリーナ」とは別の会場なので、まちがえないよう注意しましょう。")
out += html(MAP)

# ---- 流れ ----
out += h2("カウントダウンから発表までの流れ")
out += mini(("公開日時", "2026年11月8日(日)21時ちょうど"), ("サイト", "jinkame.com"),
            ("亀梨和也の投稿", "「Coming soon」"), ("赤西仁の投稿", "「Hello」"),
            ("カウントダウン終了", "2026年11月11日(水)朝6時"))
out += p("始まりは11月8日の21時ちょうどでした。",
         "まず亀梨和也が「Coming soon」の一言とともにjinkame.comのURLを投稿。",
         "その" + mark("わずか1秒後") + "に、赤西仁も「Hello」の一言で同じURLを投稿しました。",
         "2人が示し合わせて同時に発信したのは明らかで、ファンの間では一気に話題になりました。")
out += xembed(KAME_X)
out += xembed(JIN_X)
out += p("投稿から約1時間で、亀梨和也のポストは110万回以上、赤西仁のポストは130万回以上表示されています(11月8日22時ごろの時点)。",
         "いいねも2人合わせて8万件を超えていて、注目度の高さがわかります。")

out += h3("jinkame.comには何が書いてある？")
out += p("サイトを開くと、生成りのような落ち着いた背景に「KAZUYA KAMENASHI」「JIN AKANISHI」の2人の名前が並び、その下にカウントダウンが表示されます。",
         "ページの一番下には「© 2026 JINKAME」の文字があります。",
         "名前の文字は、バラバラに散らばった状態からひとつずつ集まってくるアニメーションになっていて、凝った作りです。")
out += p("SNSでシェアしたときに表示される説明文には、" + mark("「KAZUYA KAMENASHI × JIN AKANISHI OFFICIAL SITE」") + "と書かれています。",
         "つまりこのサイトは、ただの告知ページではなく、2人の「公式サイト」として作られているということです。")

out += h3("11月11日の朝6時にライブを発表")
out += p("カウントダウンの終わりは、" + mark("2026年11月11日(水)の朝6時ちょうど") + "に設定されていました。",
         "11月8日の21時に始まったので、ちょうど2日と9時間の予告期間です。")
out += p("0になると「View Site」のボタンが出て、本当のサイトが開きました。",
         "そこで発表されたのが、2027年8月のライブです。")

# ---- 日付の意味 ----
out += h2("11月8日と11月11日に込められた意味")
out += p("今回の発表は、日付の選び方にも意味がありそうです。")
out += h3("11月8日は2人の入所日")
out += p("カウントダウンが始まった11月8日は、" + mark("亀梨和也と赤西仁がそろって事務所に入所した日") + "です。",
         "2人は1998年11月8日に入所した同期で、ジュニア時代から一緒に活動してきました。",
         "さらに1年前の2025年11月8日には、亀梨和也・上田竜也・中丸雄一の3人がライブ『Break the KAT-TUN』を開きました。",
         "KAT-TUNの“解散後”のライブで、会場には赤西仁も観客として足を運んでいました。",
         "2人にとって、11月8日は特別な日だといえます。")
out += h3("11月11日は「仁亀2ショット」からちょうど1年")
out += p("カウントダウンが終わる11月11日にも、思い当たることがあります。",
         "ちょうど1年前の" + mark("2025年11月11日") + "、亀梨和也が自身のInstagramで赤西仁との2ショット写真を公開しました。",
         "赤西仁がKAT-TUNを脱退してから、2人の2ショットが公開されたのはこのときが初めてで、添えられた言葉は英語で「It was a good time」の一言だけでした。",
         "それからちょうど1年後に何かが始まるとしたら、ファンにとってはたまらない演出ですね。")
out += p("また「11」が2つ並ぶ11月11日は、2人が並ぶ姿を思わせる日付でもあります。",
         "こちらは公式に説明されたわけではありませんが、そう受け取ったファンもいるようです。")

# ---- 今後 ----
out += h2("ライブ以外の活動もある？")
out += p("サイトの説明文には、「KAZUYA KAMENASHI × JIN AKANISHI OFFICIAL SITE」と書かれています。",
         "1回きりの告知ページではなく、「公式サイト」として作られているのがポイントです。")
out += p("そのため、ライブのあとも2人での活動が続くのでは、と期待する声があります。",
         "赤西仁は独立後も音楽活動を続けていて、亀梨和也も2025年の独立後に活動の幅を広げています。",
         "新曲やグッズなど、今後の追加発表にも注目です。")
out += p("ただし、ライブ以外の予定は、11月11日の時点では何も発表されていません。",
         "新しい情報が出たら、この記事に追記します。")

# ---- 歴史 ----
out += h2("仁亀のこれまでの歩み")
out += p("「仁亀」がどれだけ特別な存在なのか、2人の歩みを振り返ってみます。")
out += table(("時期", "出来事"), [
    ("1998年11月8日", "亀梨和也と赤西仁がそろって入所"),
    ("2001年", "KAT-TUN結成。2人はグループの両エースに"),
    ("2005年1月", "ドラマ『ごくせん』第2シリーズにそろって出演し、大ブレイク"),
    ("2006年3月", "KAT-TUNがシングル「Real Face」でCDデビュー"),
    ("2010年7月", "赤西仁がKAT-TUNを脱退"),
    ("2025年3月31日", "KAT-TUNが解散。亀梨和也は事務所を退所"),
    ("2025年11月8日", "『Break the KAT-TUN』を赤西仁が観客として見守る"),
    ("2025年11月11日", "亀梨和也が赤西仁との2ショットをInstagramで公開"),
    ("2026年11月8日", "2人がjinkame.comでカウントダウンを開始"),
    ("2026年11月11日", "2027年8月のライブ開催を発表"),
])
out += p("2人はジュニア時代から「仁亀」と呼ばれ、シンメトリーのコンビとして圧倒的な人気を集めていました。",
         "2005年の『ごくせん』第2シリーズでは、赤西仁が小田切竜、亀梨和也が矢吹隼人を演じ、2人そろって大ブレイクしています。")
out += p("ところが2010年7月に赤西仁がKAT-TUNを脱退してからは、2人が一緒にいる姿はほとんど見られなくなりました。",
         "それが変わり始めたのが、KAT-TUN解散後の2025年です。",
         "11月8日のライブに赤西仁が足を運び、11月11日には2ショットが公開されて、ファンの間では「令和に仁亀が見られるなんて」と大きな話題になりました。",
         "そして2026年11月、" + mark("2人でのライブが18年ぶりに決まった") + "のです。")

# ---- 反応 ----
out += h2("ファンの反応は？「生きててよかった」")
out += p("ライブの発表に、ファンからは喜びの声があふれています。",
         "ニュースでも紹介された反応には、次のようなものがありました。")
out += html(f'''<div style="border:1px solid {B};border-left:4px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;">「生きててよかった」</p>
<p style="margin:6px 0 0 0;">「胸熱」</p>
<p style="margin:6px 0 0 0;">「絶対行きたい」</p>
<p style="margin:6px 0 0 0;">「40代の仁亀に会えるなんて夢のよう」</p>
</div>''')
out += p("チケットの倍率を心配する声も多く、今からファンクラブへの入会を考える人も見られます。",
         "カウントダウンが始まった11月8日の時点でも、次のような声が上がっていました。")
out += html(f'''<div style="border:1px solid {B};border-left:4px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;">「待って待って!!仁亀!?」</p>
<p style="margin:6px 0 0 0;">「夢じゃないよね!?」</p>
<p style="margin:6px 0 0 0;">「さすがに令和に仁亀はエグいって」</p>
<p style="margin:6px 0 0 0;">「仁亀待ってました！」</p>
<p style="margin:6px 0 0 0;">「楽しみすぎてドキドキです」</p>
</div>''')
out += p("長年「仁亀」の復活を待ち続けてきたファンにとって、待ちに待った発表になりました。")

# ---- まとめ ----
out += h2("まとめ")
items = [
    "亀梨和也と赤西仁が2027年8月18日・19日にKアリーナ横浜でライブ",
    "2人そろってのライブは2009年以来、18年ぶり",
    "チケットは亀梨和也FCのW会員、赤西仁FC「JIP's」のプレミアム会員で先行予定",
    "申し込み日程や値段はまだ発表されていない",
    "発表と同時にサイトの「×」が「-(ハイフン)」に変わり話題に",
]
out += html(f'<div style="border:1px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">'
            + "".join(f'<p style="margin:{"0" if i == 0 else "6px 0 0 0"};">{CHK}{t}</p>' for i, t in enumerate(items)) + "</div>")
out += p("脱退から約16年、ついに仁亀が同じステージに戻ってきます。",
         "チケットの申し込み日程が分かりしだい、この記事に追記します。")

sys.path.insert(0, os.path.join(REPO, "tools"))
from honorific import add_san  # noqa: E402
out = add_san(out, "ko1keyz", ["亀梨和也", "赤西仁", "上田竜也", "中丸雄一"])
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
    jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": "亀梨和也 赤西仁 jinkame.com カウントダウン"})
    state["eyecatch"] = m["id"]
    save()
    jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"featured_media": state["eyecatch"]})
po = req(f"/wp-json/wp/v2/posts/{state['post']}?context=edit", method="GET")
print(po["id"], po["status"], po["author"], po["categories"], po["featured_media"], po["title"]["raw"])
print(f"{BASE}/?p={po['id']}")
