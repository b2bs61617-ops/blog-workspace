# -*- coding: utf-8 -*-
"""chomoand-0.com: 松村北斗の愛用水筒(ハイドロフラスク)記事(2026-11-09 オシリ依頼)
根拠: 日刊スポーツ「サタジャニ」2022年4月の愛用品コーナー(本人コメント+写真、ブル男公式Xで紙面公開)
usage: python tools/_build_hokuto_suito_hydroflask_1109.py [--dry]
"""
import json, base64, os, re, sys, subprocess, socket
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "articles" / "hokuto_suito_hydroflask_1109.html"
POSTED = ROOT / "articles" / "hokuto_suito_hydroflask_1109_posted.json"
EYECATCH = ROOT / "images" / "hokuto_suito_hydroflask_1109_eyecatch.jpg"
DRY = "--dry" in sys.argv

TITLE_BODY = "松村北斗の愛用水筒はどこの？ハイドロフラスクの黒と判明"
TITLE = "【未】" + TITLE_BODY

BAR, BG, BORDER = "#333333", "#f5f5f5", "#d5d5d5"
MARK = "#d2d3d6"


def p(s):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(s) + "</p>\n<!-- /wp:paragraph -->"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def mk(t):
    return f'<strong><span style="font-size:1.1em;background:linear-gradient(transparent 60%,{MARK} 60%);">{t}</span></strong>'


def box(title, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BAR};color:#fff;">{title}</p>
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
    trs = "\n".join("<tr>" + "".join(f'<td style="padding:8px;border:1px solid {BORDER};">{c}</td>' for c in r) + "</tr>" for r in rows)
    return wphtml(f'''<div style="overflow-x:auto;margin:0 0 16px 0;">
<table style="border-collapse:collapse;width:100%;min-width:480px;font-size:0.92em;">
<thead><tr style="background:{BAR};color:#fff;">{th}</tr></thead>
<tbody>
{trs}
</tbody></table></div>''')


def summary(items):
    lis = "\n".join(
        f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {BAR};border-radius:3px;color:{BAR};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{i}</p>'
        for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BAR};color:#fff;">まとめ</p>
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
NIKKAN_TWEET = "https://twitter.com/nikkan_blueo/status/1514561712527085578"
EMBED = wphtml(f'''<blockquote class="twitter-tweet" data-lang="ja"><p lang="ja" dir="ltr">【#ブル男 の #サタジャニ 制作中】<br>今週は #松村北斗 さんです</p>&mdash; 日刊スポーツ ブル男 (@nikkan_blueo) <a href="{NIKKAN_TWEET}">2022年4月14日</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>''')

b = []
b.append(p([
    "SixTONESの松村北斗が愛用している水筒。",
    "ライブにも持っていくほどのお気に入りで、「どこのブランドなの？」と気になっている人も多いのではないでしょうか。",
    "調べてみると、北斗さんは2022年4月の日刊スポーツの連載「サタジャニ」で、" + mk("愛用品として水筒を紹介") + "していました。",
    "紙面に載った写真から、その水筒は" + mk("アメリカのボトルブランド「ハイドロフラスク」のスタンダードマウス(ブラック)") + "とみられます。",
    "この記事では、北斗さんが水筒を買ったきっかけ、ハイドロフラスクの特徴、サイズや値段、買える場所までまとめて紹介します。",
]))
b.append(box("この記事でわかること", [
    "松村北斗の愛用水筒のブランドとモデル",
    "水筒を買ったきっかけ(本人コメント)",
    "ハイドロフラスクはどんなブランド？",
    "サイズ・価格と買える場所",
]))

b.append(h2("松村北斗の愛用水筒はハイドロフラスク"))
b.append(minibox([
    ("ブランド", "Hydro Flask(ハイドロフラスク)"),
    ("モデル", "スタンダードマウス(フレックスキャップ)とみられる"),
    ("カラー", "ブラック"),
    ("紹介された場所", "日刊スポーツ「サタジャニ」(2022年4月)"),
]))
b.append(p([
    "日刊スポーツの「サタジャニ」は、毎週土曜日の紙面でジャニーズ(現STARTO ENTERTAINMENT)のタレントを1人ずつ取り上げていた連載です。",
    "2022年4月は、朝ドラ『カムカムエヴリバディ』で話題を集めていた松村北斗の回で、紙面の「愛用品」のコーナーで紹介されたのが水筒でした。",
    "担当記者の公式アカウントが、制作中の紙面の写真を公開しています。",
]))
b.append(EMBED)
b.append(p([
    "北斗さんは愛用品について、次のようにコメントしていました。",
    mk("「水筒です。自分のステージドリンクとかもこだわり始めたので買いました。使い始めて1、2年くらい。」"),
    "2022年の時点で「1、2年」なので、デビューした2020年ごろから使い始めた計算になります。",
    "ライブやコンサートのたびに持ち歩いている、まさに相棒のような水筒です。",
]))
b.append(h3("写真からわかるポイント"))
b.append(p([
    "紙面の写真に写っているのは、マットな質感の黒いボトルです。",
    "ふたには輪っか状の持ち手がついていて、ふたと本体の境目には銀色のステンレスのリングが見えます。",
    "この「輪っかの持ち手つきのふた」と「首元の銀のリング」は、ハイドロフラスクの定番ボトル「スタンダードマウス」にフレックスキャップを付けたときの特徴そのものです。",
    "細長いシルエットから、容量は532mL(18oz)か621mL(21oz)のどちらかと考えられますが、写真だけでは決めきれないので、ここは2つとも紹介します。",
]))
b.append(h3("ステージドリンクにもこだわる北斗"))
b.append(p([
    "「ステージドリンクとかもこだわり始めた」という言葉からは、ライブで飲むものまで自分で考えて用意する北斗さんらしさが伝わってきます。",
    "コンサートのMCで水を飲むときも、いつも同じ自分のボトルなら、温度や量を自分好みにしておけて安心です。",
    "2026年9月の味の素スタジアム公演でも、アンコールで自分のボトルの水を森本慎太郎の胸めがけてかけ、自分も頭から水をかぶって大笑いする場面があったと話題になりました。",
    "ステージの上でもボトルが欠かせない存在なのがわかります。",
]))

b.append(h2("ハイドロフラスクはどんなブランド？"))
b.append(p([
    "ハイドロフラスクは、2009年にアメリカ・オレゴン州ベンドで生まれたボトルブランドです。",
    "本体はステンレスの二重構造になっていて、" + mk("冷たい飲み物は最大24時間、温かい飲み物は最大12時間") + "温度をキープできるのが特徴です。",
    "表面はさらっとしたパウダーコートで、手に持ったときに滑りにくく、水滴もつきにくくなっています。",
    "カラーバリエーションが豊富で、アウトドア好きはもちろん、街で持ち歩くおしゃれな水筒としても人気があります。",
]))
b.append(p([
    "北斗さんが選んだのは、そのなかでも飾り気のないブラック。",
    "ロゴが控えめで、どんな服装にもなじむシンプルさが魅力です。",
    "ライブの衣装や楽屋の雰囲気をじゃましない、さりげない存在感も魅力ですね。",
]))

b.append(h2("サイズ・価格と買える場所"))
b.append(p([
    "北斗さんの水筒とみられるスタンダードマウスの、日本での価格は次のとおりです(税込、ANAマール掲載価格)。",
]))
b.append(table(["容量", "価格(税込)", "ポイント"], [
    ["18oz(532mL)", "4,950円", "500mLのペットボトルより少し多いくらい。バッグに入れやすい"],
    ["21oz(621mL)", "5,280円", "少し背が高く、ライブやジムなどたっぷり飲みたい日に"],
]))
b.append(p([
    "ふたはモデルによって、持ち手つきの「フレックスキャップ」、ストローで飲める「フレックスストローキャップ」などを選べます。",
    "北斗さんと同じ見た目にしたいなら、輪っかの持ち手がついたフレックスキャップのタイプを選びましょう。",
    "ストローキャップは熱い飲み物には使えないので、温かいお茶を入れたい人も、フレックスキャップがおすすめです。",
]))
b.append(box("買える場所", [
    "ハイドロフラスクの公式オンラインストア",
    "アウトドア用品店・セレクトショップ(取り扱い店舗)",
    "ANAマール、楽天市場、Amazonなどの通販(日本正規品を選ぶと安心)",
]))
b.append(p([
    "人気のカラーやサイズは、時期によって品切れになることもあります。",
    "フリマアプリなどでは並行輸入品や中古品も多いので、長く使うなら正規の販売店で買うのが安心です。",
]))

b.append(h2("まとめ"))
b.append(summary([
    "松村北斗の愛用水筒は、ハイドロフラスクのスタンダードマウス(ブラック)とみられる",
    "2022年4月の日刊スポーツ「サタジャニ」の愛用品コーナーで本人が紹介",
    "買ったきっかけは「ステージドリンクとかもこだわり始めたので」",
    "価格は18oz(532mL)が4,950円、21oz(621mL)が5,280円",
]))
b.append(p([
    "ステージドリンクにまでこだわる北斗さんが、何年も使い続けている水筒。",
    "保冷も保温もしっかりできるので、ライブの持ち物にもぴったりです。",
    "推しとおそろいの水筒で、毎日の水分補給を楽しんでみてはいかがでしょうか！",
]))
b.append(linkbox([
    ("https://chomoand-0.com/jesse-kousui-1206", "ジェシーの香水は何？ビートルジュースで甘い匂いと話題！"),
    ("https://chomoand-0.com/tanaka-juri-sabon-scrub-1178", "田中樹のSABONの香りはどれ？愛用スクラブと使い方！"),
    ("https://chomoand-0.com/kyomoto-taiga-aburae-24h-tv-1187", "京本大我の油絵はどこで見れた？24時間テレビの展示！"),
]))

content = "\n\n".join(b)
OUT.write_text(content, encoding="utf-8")
print("title len (without 【未】):", len(TITLE_BODY))


def run(*args):
    r = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    print(r.stdout[-500:], r.stderr[-500:])
    if r.returncode != 0:
        sys.exit(f"failed: {args}")


run(ROOT / "tools" / "honorific.py", "fix", "--group", "sixtones", OUT)
run(ROOT / "tools" / "sixtones_theme.py", OUT, "--member", "松村北斗")
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
    requests.post(f"{BASE}/wp-json/wp/v2/posts/{posted['post_id']}", headers=AUTH, json={"content": content}).raise_for_status()
    print("UPDATED", posted["post_id"])
    sys.exit()

r = requests.post(f"{BASE}/wp-json/wp/v2/posts", headers=AUTH, json={
    "title": TITLE, "content": content, "status": "draft", "slug": "matsumura-hokuto-suito-hydroflask",
    "categories": [15, 18], "author": AUTHOR})
r.raise_for_status()
post = r.json()
posted["post_id"] = post["id"]
POSTED.write_text(json.dumps(posted, ensure_ascii=False, indent=2), encoding="utf-8")
print("POST_ID", post["id"], post["status"], post["link"])

eye = subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_sixtones.py"), "--main", "松村北斗",
                      "--bottom", "愛用の水筒はどこの？", "--bottom", "ハイドロフラスクの黒",
                      "--color-key", "松村北斗", "--out", str(EYECATCH)],
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
