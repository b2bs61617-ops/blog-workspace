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
BASE_TITLE = "亀梨和也と赤西仁が謎のカウントダウン！11/11に何が始まる？"
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

out = ""
out += p("2026年11月8日の夜、亀梨和也と赤西仁が、それぞれの公式Xで" + mark("同じサイト「jinkame.com」") + "を同時に公開しました。",
         "サイトには2人の名前と、カウントダウンだけが表示されています。",
         "カウントダウンが終わるのは" + mark("11月11日(水)の朝6時") + "です。",
         "かつてKAT-TUNで「仁亀(じんかめ)」と呼ばれた2人が、いったい何を始めるのでしょうか。",
         "この記事では、今わかっていることと、11月8日・11月11日という日付の意味、そして何が発表されるのかの予想をまとめました。")

out += html(f'''
<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>亀梨和也と赤西仁が公開したサイトの中身</li>
<li>カウントダウンが終わる日時</li>
<li>11月8日と11月11日が選ばれた理由</li>
<li>11月11日に何が発表されるのかの予想</li>
<li>仁亀のこれまでの歩み</li>
<li>ファンの反応</li>
</ul>
</div>''')

# ---- 何が起きた ----
out += h2("亀梨和也と赤西仁が同じサイトを同時に公開")
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

out += h3("カウントダウンが終わるのは11月11日の朝6時")
out += p("サイトに表示されているカウントダウンの終わりは、" + mark("2026年11月11日(水)の朝6時ちょうど") + "に設定されています。",
         "カウントダウンが始まったのは11月8日の21時なので、ちょうど2日と9時間の予告期間です。",
         "サイトの仕組みを見ると、カウントダウンが0になると「View Site」というボタンが出てきて、そこから本当のサイトが開く作りになっています。",
         "11月11日の朝6時に、ここで何かが発表されるのは間違いなさそうです。")

# ---- 日付の意味 ----
out += h2("11月8日と11月11日に込められた意味")
out += p("今回の発表は、日付の選び方にも意味がありそうです。")
out += h3("11月8日は2人の入所日")
out += p("カウントダウンが始まった11月8日は、" + mark("亀梨和也と赤西仁がそろって事務所に入所した日") + "です。",
         "2人は1998年11月8日に入所した同期で、ジュニア時代から一緒に活動してきました。",
         "さらに1年前の2025年11月8日には、亀梨和也・上田竜也・中丸雄一の3人がKAT-TUNの“解散後”ライブ『Break the KAT-TUN』を開いていて、その会場には赤西仁も観客として足を運んでいました。",
         "2人にとって、11月8日は特別な日だといえます。")
out += h3("11月11日は「仁亀2ショット」からちょうど1年")
out += p("カウントダウンが終わる11月11日にも、思い当たることがあります。",
         "ちょうど1年前の" + mark("2025年11月11日") + "、亀梨和也が自身のInstagramで赤西仁との2ショット写真を公開しました。",
         "赤西仁がKAT-TUNを脱退してから、2人の2ショットが公開されたのはこのときが初めてで、添えられた言葉は英語で「It was a good time」の一言だけでした。",
         "それからちょうど1年後に何かが始まるとしたら、ファンにとってはたまらない演出ですね。")
out += p("また「11」が2つ並ぶ11月11日は、2人が並ぶ姿を思わせる日付でもあります。",
         "こちらは公式に説明されたわけではありませんが、そう受け取ったファンもいるようです。")

# ---- 予想 ----
out += h2("11月11日に何が発表される？考えられる5つの可能性")
out += p("発表の内容は、まだまったく明かされていません。",
         "ここからは、サイトの作りやこれまでの報道をもとにした" + mark("予想") + "です。")
out += table(("可能性", "考えられる理由"), [
    ("ユニット結成・楽曲リリース", "「OFFICIAL SITE」と書かれていて、1回きりではなく続けて活動する前提に見える"),
    ("ライブ・ファンイベント", "2人でイベントを計画していると週刊誌で報じられたことがある"),
    ("YouTubeなどの配信企画", "亀梨和也は「亀チャンネル」を運営していて、動画での発信に慣れている"),
    ("ドラマ・映画での共演", "『ごくせん』以来の共演を望む声は多い。ただ、朝6時の解禁は作品発表としてはやや珍しい"),
    ("ブランド・グッズの立ち上げ", "「JINKAME」というブランド名のような表記が使われている"),
])
out += p("中でも可能性が高そうなのが、" + mark("2人での音楽活動やイベント") + "です。",
         "サイトの説明文に「OFFICIAL SITE」とあることから、ひとつの作品の宣伝ではなく、「仁亀」として継続的に活動していく場所を作ったように見えます。",
         "赤西仁は独立後もアーティストとして音楽活動を続けていて、亀梨和也も2025年に独立してから自分の名前で活動の幅を広げています。",
         "それぞれが事務所を離れて自由に動ける立場になった今だからこそ、実現できる企画なのかもしれません。")
out += p("また、発表が朝6時というのもポイントです。",
         "朝の情報番組やネットニュースが動き出す時間帯なので、" + mark("大きなニュースとして一斉に広げたい") + "という狙いがあるのではないでしょうか。")
out += p("一部の週刊誌では、以前から2人が一緒にイベントを計画していると報じられていました。",
         "ただし、これはあくまで報道ベースの話で、本人たちが認めたものではありません。",
         "答え合わせは11月11日の朝6時です。")

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
])
out += p("2人はジュニア時代から「仁亀」と呼ばれ、シンメトリーのコンビとして圧倒的な人気を集めていました。",
         "2005年の『ごくせん』第2シリーズでは、赤西仁が小田切竜、亀梨和也が矢吹隼人を演じ、2人そろって大ブレイクしています。")
out += p("ところが2010年7月に赤西仁がKAT-TUNを脱退してからは、2人が一緒にいる姿はほとんど見られなくなりました。",
         "それが変わり始めたのが、KAT-TUN解散後の2025年です。",
         "11月8日のライブに赤西仁が足を運び、11月11日には2ショットが公開されて、ファンの間では「令和に仁亀が見られるなんて」と大きな話題になりました。",
         "そして今回のカウントダウンで、" + mark("2人が並んで何かを発表するのは、脱退から約16年ぶり") + "ということになります。")

# ---- 反応 ----
out += h2("ファンの反応は？「まさかの仁亀!?」")
out += p("突然のカウントダウンに、ファンからは驚きと喜びの声があふれています。",
         "ニュースでも紹介された反応には、次のようなものがありました。")
out += html(f'''<div style="border:1px solid {B};border-left:4px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;">「待って待って!!仁亀!?」</p>
<p style="margin:6px 0 0 0;">「夢じゃないよね!?」</p>
<p style="margin:6px 0 0 0;">「さすがに令和に仁亀はエグいって」</p>
<p style="margin:6px 0 0 0;">「仁亀待ってました！」</p>
<p style="margin:6px 0 0 0;">「楽しみすぎてドキドキです」</p>
</div>''')
out += p("ほかにも「11/11の朝6時に何が起こるの？」と、発表の時間に合わせて早起きを決めたファンの声も多く見られます。",
         "長年「仁亀」の復活を待ち続けてきたファンにとっては、待ちに待った瞬間といえそうです。")

# ---- 見逃さない ----
out += h2("発表を見逃さないためには")
out += p("発表は11月11日(水)の朝6時です。",
         "見逃さないために、次の3つをチェックしておきましょう。")
out += table(None, [
    ("<strong>公式サイト</strong>", "jinkame.com(カウントダウン終了後に「View Site」が表示される)"),
    ("<strong>亀梨和也のX</strong>", "@K_KAMEofficial"),
    ("<strong>赤西仁のX</strong>", "@Jin_Akanishi"),
])
out += p("2人のXアカウントをフォローして通知をオンにしておけば、発表の瞬間を見逃さずにすみます。",
         "この記事でも、発表内容がわかりしだい追記していきます。")

# ---- まとめ ----
out += h2("まとめ")
items = [
    "2026年11月8日21時、亀梨和也と赤西仁が同じサイト「jinkame.com」を同時に公開",
    "サイトは「KAZUYA KAMENASHI × JIN AKANISHI OFFICIAL SITE」",
    "カウントダウンの終了は11月11日(水)朝6時",
    "11月8日は2人の入所日、11月11日は仁亀2ショット公開からちょうど1年",
    "発表内容は未公表。音楽活動やイベントなど、2人での継続的な活動の可能性",
]
out += html(f'<div style="border:1px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">'
            + "".join(f'<p style="margin:{"0" if i == 0 else "6px 0 0 0"};">{CHK}{t}</p>' for i, t in enumerate(items)) + "</div>")
out += p("脱退から約16年、ついに仁亀が並んで何かを始めようとしています。",
         "11月11日の朝6時、どんな発表が待っているのか楽しみに待ちましょう。")

sys.path.insert(0, os.path.join(REPO, "tools"))
from honorific import add_san  # noqa: E402
out = add_san(out, "ko1keyz", ["亀梨和也", "赤西仁", "上田竜也", "中丸雄一"])
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
        jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"content": out, "status": "draft"})
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
