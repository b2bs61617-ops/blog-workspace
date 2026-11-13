# -*- coding: utf-8 -*-
"""めちゃイケ30周年『めちゃ×2メチャってるッ！』地上波初放送記事(chomoand.com 芸能・トレンド)を組み立てて下書き投稿する(2026-11-13、オシリ依頼)。
usage: python tools/_build_upload_mechaike_laposta_1113.py [--update-content] [--build-only]
状態は articles/mechaike_laposta_posted.json に控え、再実行で重複投稿しない。
"""
import sys, os, json, base64, socket, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "articles", "mechaike_laposta_1113.html")
POSTED = os.path.join(REPO, "articles", "mechaike_laposta_posted.json")
BASE_TITLE = "めちゃイケ地上波復活にJO1・INI出演！放送日や見どころは？"
assert len(BASE_TITLE) <= 35, len(BASE_TITLE)
TITLE = "【未】" + BASE_TITLE
SLUG = "mechaike-okamura-laposta-jo1-ini"
CATEGORIES = [37]
AUTHORS = {"USER1": 3, "Tomoki": 4}
EYECATCH = os.path.join(REPO, "images", "mechaike_laposta_eyecatch.png")

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


LAPONE_X = "https://x.com/lapone_info/status/2121030285890576762"
NEWS = "https://cf.lapone.jp/news/detail/208"

out = ""
out += p("岡村隆史がJO1やINIたちと東京ドームを目指した番組『めちゃ×2メチャってるッ！』。",
         "この番組が、" + mark("2026年12月5日(土)18時30分からフジテレビで地上波初放送") + "されます。",
         "放送時間は23時10分までの、約4時間40分です。",
         "『めちゃイケ』の誕生30周年を記念した番組です。",
         "2025年にネットで配信された全12話に、2026年の新しい映像を足して作り直したスペシャル版になっています。")
out += p("JO1・INI・DXTEEN・ME:I・IS:SUEの5グループも出演します。",
         "この記事では、放送日や番組の内容、LAPOSTA 2025で岡村隆史が何をしたのか、見どころをまとめました。")

out += html(f'''
<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>放送日と放送時間</li>
<li>どんな番組なのか</li>
<li>JO1やINIとの関係</li>
<li>LAPOSTA 2025での岡村隆史の登場シーン</li>
<li>配信版との違いと見どころ</li>
</ul>
</div>''')

# ---- 放送日 ----
out += h2("めちゃ×2メチャってるッ！の放送日はいつ？")
out += mini(("番組名", "めちゃイケ誕生30周年記念番組『めちゃ×2メチャってるッ！』"),
            ("放送日", "2026年12月5日(土)"),
            ("時間", "18時30分〜23時10分(約4時間40分)"),
            ("放送局", "フジテレビ系(一部の地域をのぞく)"),
            ("総監督", "片岡飛鳥(『めちゃイケ』の生みの親)"))
out += p("放送は" + mark("12月5日(土)の18時30分から23時10分まで") + "です。",
         "土曜の夜にフジテレビで『めちゃイケ』が見られるのは、2018年の最終回以来になります。",
         "ただし、一部の地域では放送されないので、お住まいの地域の番組表を確かめておきましょう。")
out += p("この発表は、2026年11月13日にLAPONEの公式Xでも伝えられました。")
out += xembed(LAPONE_X)
out += p("番組の公式ハッシュタグは" + mark("「#めちゃメチャ」") + "です。",
         "放送中はXで「#めちゃメチャ」をチェックすると、みんなの感想も楽しめます。")
out += h3("出演者は？")
out += table(("ジャンル", "出演者"), [
    ("MC", "ナインティナイン"),
    ("LAPONE", "JO1、INI、DXTEEN、ME:I、IS:SUE"),
    ("芸人", "レインボー、コットン、ニューヨーク、鬼越トマホーク、オダウエダ、江頭2:50 ほか"),
])
out += p("2025年の配信版には、よゐこの濱口優、オアシズの大久保佳代子、極楽とんぼの山本圭壱も出ていました。",
         "地上波版でどこまで登場するかは、放送を楽しみに待ちましょう。")

# ---- 内容 ----
out += h2("どんな番組？岡村隆史の「オファーシリーズ」最新作")
out += p("『めちゃイケ』は、1996年から2018年までフジテレビで放送されたバラエティ番組です。",
         "今回の番組は、その人気企画" + mark("「岡村隆史のオファーが来ました」シリーズの最新作") + "です。",
         "岡村隆史がいろいろな世界からのオファーを受けて、本気で挑戦する企画です。")
out += p("これまでダンス、フルマラソン、競馬、ボクシング、歌舞伎、ミュージカルなどに挑んできました。",
         "27歳のときのSMAPのライブへの乱入から始まり、今回でシリーズ16回目です。",
         "50代になってからの挑戦は、今回がはじめてです。")
out += h3("シリーズ最長の484日間を密着")
out += p("撮影は2023年10月から始まり、足かけ3年、" + mark("シリーズ最長の484日間") + "の密着になりました。",
         "きっかけは、岡村隆史の昔からの戦友・江頭2:50の「襲撃」です。")
out += p("岡村隆史のオファーシリーズを見て育った後輩芸人たちが「MM団」を作り、パルクールで岡村隆史を鍛え直そうとしました。",
         "メンバーはニューヨーク、レインボー、コットン、鬼越トマホーク、オダウエダです。",
         "パルクールは、フランス生まれの、走る・跳ぶ・登るを組み合わせたスポーツです。")
out += h3("初日にアキレス腱を断裂")
out += p("ところが、パルクールの" + mark("初日に岡村隆史はアキレス腱を断裂") + "してしまいます。",
         "企画が中止になってもおかしくない大ケガでしたが、カメラは止まりませんでした。",
         "診察室や病院のベッド、自宅での様子まで記録されています。")
out += p("手術とリハビリ、トレーニングをへて、岡村隆史は復活します。",
         "予定より1年おくれのスタートラインに立ったところで、新しいオファーが届きました。")

# ---- LAPONE ----
out += h2("JO1・INIたちとの関係は？オファーしたのはLAPONE")
out += p("今回のオファーは、" + mark("LAPONE ENTERTAINMENTとLAPONE GIRLS") + "から届きました。",
         "JO1・INI・DXTEENが所属するのがLAPONE ENTERTAINMENT、ME:I・IS:SUEが所属するのがLAPONE GIRLSです。",
         "オファーシリーズとしては、7年ぶりの新しいオファーでした。")
out += p("岡村隆史は、オーディション番組『PRODUCE 101 JAPAN』で司会をつとめました。",
         "JO1とINIが生まれた番組で、役職は「国民プロデューサー代表」です。",
         "デビュー前からメンバーを見守ってきた、いわば恩人のような存在です。")
out += p("オファーの中身は、" + mark("東京ドームで開かれる「LAPOSTA 2025」を盛り上げること") + "でした。",
         "LAPONEの社長・崔信化から「『ラポスタ2025』を盛り上げて」とたのまれたと、岡村隆史本人がステージで話しています。")

# ---- LAPOSTA ----
out += h2("LAPOSTA 2025で岡村隆史は何をした？")
out += mini(("イベント", "LAPOSTA 2025 Supported by docomo"),
            ("期間", "2025年1月27日〜2月2日"),
            ("会場", "東京ドームとまわりの施設"),
            ("岡村隆史の登場", "2025年2月2日の東京ドーム最終日"))
out += p("LAPOSTAは、LAPONEのアーティストが集まる合同イベントです。",
         "2025年は3回目の開催で、ME:IとIS:SUEが新しく加わりました。",
         "東京ドームでのライブは3日間あり、岡村隆史が登場したのは最終日の2月2日です。")
out += h3("「シャチョー」の着ぐるみの中身だった")
out += p("この日のライブでは、マスコットの「シャチョー」の着ぐるみが何度もステージに出ていました。",
         "シャチョーは、JO1の鶴房汐恩がデザインしたキャラクターで、社長の崔信化がモデルです。")
out += p("アンコールでJO1が「無限大」を歌っているとき、シャチョーが頭を外すと、" + mark("中から金髪にカラコン姿の岡村隆史") + "があらわれました。",
         "会場は大きな歓声につつまれ、岡村隆史はそのままJO1と一緒に「無限大」を踊りました。")
out += p("JO1の川尻蓮がカラコンに気づくと、メンバーからは「JO1にいそう」「かっこいい」という声が上がりました。",
         "岡村隆史は「元国民プロデューサー代表、岡村隆史です」とあいさつしています。")
out += h3("「WOW WAR TONIGHT」で東京ドームがひとつに")
out += p("岡村隆史の希望で、JO1と「WOW WAR TONIGHT 〜時には起こせよムーヴメント〜(JO1 ver.)」も披露しました。",
         "最後はLAPONEのアーティスト全員で「LOVE ALL STAR」を歌い、ライブをしめくくりました。")
out += p("相方の矢部浩之は別の部屋からの中継で登場し、「勝手に踊ったらあかん」「調子乗るな」とツッコミを入れました。",
         "「かっこよくしてもらっても小さい」というひと言に、会場は笑いにつつまれました。")
out += p("このときスクリーンに「ナインティナイン新配信番組制作中！」と出て、サプライズ出演が番組の企画だったと分かりました。",
         "その番組が、今回地上波で放送される『めちゃ×2メチャってるッ！』です。")

# ---- 見どころ ----
out += h2("めちゃ×2メチャってるッ！の見どころは？")
out += h3("JO1・INIの前での「最終オーディション」")
out += p("配信版の第10話では、合同リハーサルの最後に、岡村隆史がダンスを見せる場面があります。",
         "見ているのはJO1とINI、そして社長の崔信化です。",
         "岡村隆史は「最終オーディションという形で」と切り出し、" + mark("こっそり練習してきたINIの「BOMBARDA」とJO1の「無限大」") + "を続けて踊りました。")
out += p("「昨日も緊張であまり眠れなかった」と話す岡村隆史に、INI最年少の松田迅が「それは年だからじゃないんですか？」とツッコミ。",
         "その場が一瞬こおりつき、INIの木村柾哉と西洸人があわてて「すみません！」と頭を下げました。",
         "ダンスが終わると、メンバーは立ち上がりそうな勢いで盛り上がり、拍手を送っています。")
out += h3("ME:Iのリハーサルで大乱闘")
out += p("第9話では、ME:Iのデビュー曲「Click」のダンスブレイクで、岡村隆史がマスコットの「ミャイ」に法被を着せる役に挑みます。",
         "ところが、激しく動くミャイの腕になかなか法被を通せません。")
out += p("言い合いはメンバーも巻きこむ大乱闘になり、空手の黒帯を持つSUZUの蹴りが入る場面も。",
         "MIUからは「できんくせに文句が多いよ」と、きびしいひと言を受けていました。")
out += h3("本番の東京ドームでも大暴れ")
out += p("本番では、INIの「BOMBARDA」のステージに着ぐるみの頭だけで乱入し、アドリブでブレイクダンスを披露しました。",
         "ME:Iのステージでは、ミャイが法被を着るのをいやがってケンカになり、警備員に取りおさえられて退場しています。")
out += p("モニタールームで見ていた矢部浩之は「グッジョブじゃないですか！」とほめました。",
         "岡村隆史も「一つになったんじゃない？」と、手ごたえを話しています。")
out += h3("2026年の岡村隆史を新しく撮影")
out += p("地上波版では、" + mark("2026年の岡村隆史のドキュメントが新しく撮影") + "されています。",
         "2026年秋、岡村隆史は家族とおだやかに暮らしながら、芸人として活動を続けています。")
out += p("2018年の『めちゃイケ』最終回で、岡村隆史は泣きながら「『めちゃイケ』は僕の青春でした！」と叫びました。",
         "それから8年、50代の岡村隆史の「芸人としての今」が、どう描かれるのか注目です。")

# ---- 配信版との違い ----
out += h2("配信版との違いは？")
out += p("この番組は、もともと2025年にFODで独占配信されたネット番組です。",
         "全12話、合わせて約7時間の作品でした。")
out += table(("", "配信版(2025年)", "地上波版(2026年)"), [
    ("公開", "FODで独占配信", "フジテレビ系で放送"),
    ("長さ", "全12話・約7時間", "約4時間40分"),
    ("内容", "484日間の密着", "配信版に2026年の新映像を追加"),
])
out += p("配信版は2つに分かれていました。",
         "第1部「あきらめたらそこで試合終了ですよスペシャル!!」は全5話で、2025年10月10日から配信。",
         "第2部「7年ぶりに起こせよムーヴメントスペシャル!!」は全7話で、11月15日から配信されました。",
         "地上波版は、この全12話をもとに、時間の流れにそって組み立て直したスペシャル番組です。")
out += p("配信版を見た人も、新しく撮られた2026年の岡村隆史の映像があるので、楽しめる内容になっています。",
         "見逃し配信については、11月13日の時点ではまだ発表されていません。")

# ---- 年表 ----
out += h2("番組ができるまでの流れ")
out += table(("時期", "出来事"), [
    ("2018年3月", "『めちゃイケ』が最終回"),
    ("2023年10月", "江頭2:50の襲撃でプロジェクトがスタート"),
    ("パルクール初日", "岡村隆史がアキレス腱を断裂"),
    ("手術・リハビリ後", "LAPONEから7年ぶりのオファー"),
    ("2025年2月2日", "LAPOSTA 2025の東京ドームにサプライズ登場"),
    ("2025年10月10日", "FODで第1部(全5話)の配信スタート"),
    ("2025年11月15日", "FODで第2部(全7話)の配信スタート"),
    ("2026年11月13日", "地上波での放送が決定"),
    ("2026年12月5日", "フジテレビ系で地上波初放送"),
])
out += p("くわしい情報は、" + f'<a href="{NEWS}" target="_blank" rel="noopener">LAPONE ENTERTAINMENTの公式ニュース</a>' + "でも見られます。")

# ---- まとめ ----
out += h2("まとめ")
items = [
    "『めちゃ×2メチャってるッ！』は2026年12月5日(土)18時30分からフジテレビ系で放送",
    "放送時間は23時10分までの約4時間40分(一部の地域をのぞく)",
    "JO1・INI・DXTEEN・ME:I・IS:SUEが出演",
    "LAPONEのオファーで岡村隆史がLAPOSTA 2025の東京ドームに立つまでを密着",
    "配信版の全12話に、2026年の新しい映像を足したスペシャル版",
]
out += html(f'<div style="border:1px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">'
            + "".join(f'<p style="margin:{"0" if i == 0 else "6px 0 0 0"};">{CHK}{t}</p>' for i, t in enumerate(items)) + "</div>")
out += p("JO1やINIを見守ってきた岡村隆史が、ケガを乗りこえて東京ドームに立つまでの物語です。",
         "LAPONEファンも『めちゃイケ』ファンも、12月5日の夜は見のがせませんね。",
         "新しい情報が出たら、この記事に追記します。")

sys.path.insert(0, os.path.join(REPO, "tools"))
from honorific import add_san  # noqa: E402
out = add_san(out, "ko1keyz", ["岡村隆史", "矢部浩之", "江頭2:50", "片岡飛鳥", "崔信化", "鶴房汐恩", "川尻蓮",
                               "松田迅", "木村柾哉", "西洸人", "濱口優", "大久保佳代子", "山本圭壱", "SUZU", "MIU"])
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
    jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": "めちゃ×2メチャってるッ 岡村隆史 LAPOSTA JO1 INI"})
    state["eyecatch"] = m["id"]
    save()
    jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"featured_media": state["eyecatch"]})
po = req(f"/wp-json/wp/v2/posts/{state['post']}?context=edit", method="GET")
print(po["id"], po["status"], po["author"], po["categories"], po["featured_media"], po["title"]["raw"])
print(f"{BASE}/?p={po['id']}")
