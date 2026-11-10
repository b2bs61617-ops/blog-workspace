# -*- coding: utf-8 -*-
"""chomoand-0.com: 松村北斗がヤンマースタジアム長居で履いていたスニーカー(adidas ADISTAR CONTROL 5 KJ8804)記事(2026-11-10 オシリ依頼)
根拠: SixTONES公式Instagram 2026-11-08投稿(DfevzSpzJAU)の写真と商品画像の照合(クロームの3本線・えんじの紐/ライン・水色メッシュ・こげ茶ソール)
価格・発売日: スニダン KJ8804 (定価16,500円/2026-02-03発売)、海外発売 2026-01-15
usage: python tools/_build_hokuto_adistar_control5_1110.py [--dry]
"""
import json, base64, os, re, sys, subprocess
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "articles" / "hokuto_adistar_control5_1110.html"
POSTED = ROOT / "articles" / "hokuto_adistar_control5_1110_posted.json"
EYECATCH = ROOT / "images" / "hokuto_adistar_control5_1110_eyecatch.jpg"
DRY = "--dry" in sys.argv

TITLE_BODY = "松村北斗が長居で履いたスニーカーはどこの？アディダスと判明"
TITLE = "【未】" + TITLE_BODY
assert len(TITLE_BODY) <= 35, len(TITLE_BODY)

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


IG = "https://www.instagram.com/p/DfevzSpzJAU/"
EMBED = wphtml(f'''<blockquote class="instagram-media" data-instgrm-permalink="{IG}?utm_source=ig_embed" data-instgrm-version="14" style="background:#FFF;border:0;margin:1px auto;max-width:540px;min-width:280px;width:calc(100% - 2px);"><a href="{IG}" target="_blank" rel="noopener">SixTONES公式Instagramの投稿を見る</a></blockquote>
<script async src="//www.instagram.com/embed.js"></script>''')
AMAZON = "https://www.amazon.co.jp/s?k=%E3%82%A2%E3%83%87%E3%82%A3%E3%82%B9%E3%82%BF%E3%83%BC+%E3%82%B3%E3%83%B3%E3%83%88%E3%83%AD%E3%83%BC%E3%83%AB+5&tag=chomoand03-22"
SNKRDUNK = "https://snkrdunk.com/products/KJ8804"

b = []
b.append(p([
    "SixTONESの公式Instagramに、長居公演を終えた6人の写真が投稿されました。",
    "松村北斗の足元に光る銀色のスニーカーが、「どこの？」と気になった人も多いはずです。",
]))
b.append(p([
    "写真と商品を見比べると、北斗さんの靴は" + mk("アディダスの「アディスター コントロール 5」") + "とみられます。",
    "色は" + mk("プリラブドブルー/ダークブラウン(品番KJ8804)") + "です。",
    "この記事では、見比べたポイント、靴の特徴、値段や買える場所まで紹介します。",
]))
b.append(box("この記事でわかること", [
    "松村北斗が長居で履いていたスニーカーのブランドとモデル",
    "写真と商品を見比べたポイント",
    "アディスター コントロール 5はどんなスニーカー？",
    "価格・サイズと買える場所",
]))

b.append(h2("松村北斗のスニーカーはアディダスのアディスター コントロール 5"))
b.append(minibox([
    ("ブランド", "adidas(アディダス)"),
    ("モデル", "ADISTAR CONTROL 5(アディスター コントロール 5)"),
    ("カラー", "プリラブドブルー/ダークブラウン/グレーファイブ"),
    ("品番", "KJ8804"),
    ("定価", "16,500円(税込)"),
]))
b.append(p([
    "写っていたのは、2026年11月8日にSixTONESの公式Instagramに投稿された1枚です。",
    "「ヤンマースタジアム長居ありがとうございました！」というメッセージとともに、6人がバックステージの通路で並んでいます。",
    "北斗さんは写真の右端、黒とオレンジのユニフォームに黒のハーフパンツを合わせたスタイルです。",
]))
b.append(EMBED)
b.append(p([
    "投稿には「風邪引かないように暖かくしてねー！」「ラストは日産スタジアム！まだまだいくぜー！」という言葉も添えられていて、ツアーがいよいよ最終地に向かう熱さが伝わってきます。",
]))

b.append(h3("写真と商品を見比べたポイント"))
b.append(p([
    "写真の北斗さんの足元を拡大して、アディスター コントロール 5のKJ8804と見比べてみました。",
    "一致しているポイントは次の4つです。",
]))
b.append(table(["見えるポイント", "北斗さんの写真", "KJ8804"], [
    ["サイドのライン", "鏡のように光る銀色の3本線", "クロームシルバーのパーツで囲まれた3本線"],
    ["靴ひも・ライン", "えんじ色(赤紫)の靴ひもとライン", "えんじ色(バーガンディ)の靴ひもとライン"],
    ["メッシュ部分", "右足のつま先側に水色が見える", "水色(プリラブドブルー)のメッシュ"],
    ["ソール", "こげ茶色の厚めのソール", "ダークブラウンのソール"],
]))
b.append(p([
    "銀色のパーツとえんじ色の靴ひもの組み合わせは、かなり目立ちます。",
    mk("同じモデルの別の色とは、見た目がはっきり違う") + "のがポイントです。",
    "左足は照明が反射して銀色に見えていますが、右足をよく見ると水色のメッシュがのぞいていて、商品写真の配色と一致します。",
    "ただし、公式から「このスニーカーです」と発表されたわけではないので、写真から推定した結果として紹介しています。",
]))

b.append(h2("アディスター コントロール 5はどんなスニーカー？"))
b.append(p([
    "アディスター コントロール 5は、" + mk("2000年代のランニングシューズを今っぽくよみがえらせた") + "アディダスのスニーカーです。",
    "ここ数年は「Y2K」と呼ばれる2000年代風のファッションが人気です。",
    "銀色のパーツを使った、昔のランニングシューズ風のデザインが注目されています。",
]))
b.append(table(["項目", "内容"], [
    ["アッパー(甲の部分)", "2色を重ねた二重構造のメッシュ+クロームのパーツ"],
    ["ミッドソール", "EVA素材で軽くクッション性がある"],
    ["かかと", "着地をなめらかにする「Formotion(フォーモーション)」パーツ"],
    ["アウトソール", "ラバー"],
    ["フィット", "標準(レギュラーフィット)"],
]))
b.append(p([
    "見た目はごつめですが、もとはランニングシューズなので、長時間歩いても疲れにくいのがうれしいところです。",
    "ライブの移動や楽屋での待ち時間など、動き回る日にぴったりの1足ですね。",
]))
b.append(h3("北斗のコーデのポイント"))
b.append(p([
    "この日の北斗さんは、黒のユニフォームに黒のハーフパンツ、グレーのソックスという落ち着いた色合わせでした。",
    "全体が暗めの色でまとまっているぶん、銀色に光るスニーカーが足元のアクセントになっています。",
    "グレーのソックスが靴のシルバーとなじんでいて、ハーフパンツでも足元がうるさく見えないバランスです。",
]))

b.append(h2("価格・サイズと買える場所"))
b.append(p([
    "北斗さんのスニーカーとみられるKJ8804の情報をまとめました。",
]))
b.append(table(["項目", "内容"], [
    ["定価", "16,500円(税込)"],
    ["日本での発売日", "2026年2月3日(海外は2026年1月15日)"],
    ["区分", "ウィメンズモデル"],
    ["サイズ", "22.0〜28.0cm(0.5cm刻み)"],
    ["中古・再販の相場", "スニダンで25,908円〜(2026年11月10日時点)"],
]))
b.append(p([
    "KJ8804は" + mk("ウィメンズモデル") + "ですが、28.0cmまでサイズがあります。",
    "男性でも、足のサイズが合えば履けます。",
    "ウィメンズのサイズ表記はメンズと少しずれることがあるので、買う前にセンチ表記で確認するのがおすすめです。",
    "発売から9か月ほどたち、品切れのサイズもあるようです。",
    "スニダンなどの再販サイトでは、定価より高い値段がついています。",
]))
b.append(box("買える場所", [
    "アディダス公式オンラインストア・アディダスの店舗",
    "atmos(アトモス)などのスニーカーショップ",
    "スニダン・StockXなどのスニーカー再販サイト(定価より高めの場合あり)",
    "Amazon(KJ8804は出品なし、別カラーのみ ※2026年11月10日時点)",
]))
b.append(p([
    "北斗さんの写真をきっかけに人気が出ると、残っているサイズもすぐになくなってしまうかもしれません。",
    "再販サイトで買うときは、品番が「KJ8804」になっているか必ず確認しましょう。",
]))
btn = "display:inline-block;padding:8px 18px;margin:4px 6px 0 0;border-radius:4px;color:#fff;font-weight:bold;text-decoration:none;font-size:0.92em;"
b.append(p([
    "北斗さんと同じKJ8804は、2026年11月10日時点でAmazonに出品がありませんでした。",
    "同じ色がほしい人は、スニダンなどの再販サイトで品番「KJ8804」を探してみてください。",
    "Amazonでは、黒×シルバーなど同じアディスター コントロール 5の別カラーが見つかります。",
]))
b.append(wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;padding:14px 16px;background:#fff;">
<p style="margin:0 0 4px 0;font-weight:bold;">adidas ADISTAR CONTROL 5</p>
<p style="margin:0 0 6px 0;font-size:0.88em;color:#555;">北斗と同じ色(KJ8804)はスニダン、別カラーはAmazonで</p>
<a href="{SNKRDUNK}" target="_blank" rel="noopener" style="{btn}background:#333333;">スニダンでKJ8804を見る</a><a href="{AMAZON}" target="_blank" rel="nofollow sponsored noopener" style="{btn}background:#ff9900;">Amazonで別カラーを見る</a>
</div>'''))

b.append(h2("まとめ"))
b.append(summary([
    "松村北斗が長居で履いた靴は、アディダスのアディスター コントロール 5(KJ8804)とみられる",
    "銀色の3本線・えんじ色の靴ひも・水色のメッシュ・こげ茶のソールが一致",
    "2000年代のランニングシューズを今っぽくよみがえらせたモデル",
    "定価16,500円(税込)、サイズは22.0〜28.0cmのウィメンズモデル",
]))
b.append(p([
    "黒でまとめたユニフォーム姿の足元に、さりげなく光っていた北斗さんのスニーカー。",
    "ツアーはいよいよ日産スタジアムでラストを迎えます。",
    "最終公演でも、北斗さんの足元に注目してみてはいかがでしょうか！",
]))
b.append(linkbox([
    ("https://chomoand-0.com/sixtones-favorite-perfume-1436", "SixTONESの愛用香水まとめ！田中樹はディオール？北斗の香りも"),
    ("https://chomoand-0.com/tanaka-juri-sabon-scrub-1178", "田中樹のSABONの香りはどれ？愛用スクラブと使い方！"),
    ("https://chomoand-0.com/jesse-kousui-1206", "ジェシーの香水は何？ビートルジュースで甘い匂いと話題！"),
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
run(ROOT / "tools" / "easy_read.py", "fix", OUT)
run(ROOT / "tools" / "easy_read.py", "check", OUT)
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
AUTHOR = 2  # オシリの記事は momo(id2)

posted = json.loads(POSTED.read_text(encoding="utf-8")) if POSTED.exists() else {}
if "post_id" in posted:
    requests.post(f"{BASE}/wp-json/wp/v2/posts/{posted['post_id']}", headers=AUTH, json={"content": content}).raise_for_status()
    print("UPDATED", posted["post_id"])
    sys.exit()

r = requests.post(f"{BASE}/wp-json/wp/v2/posts", headers=AUTH, json={
    "title": TITLE, "content": content, "status": "draft", "slug": "matsumura-hokuto-adistar-control5",
    "categories": [15, 18], "author": AUTHOR})
r.raise_for_status()
post = r.json()
posted["post_id"] = post["id"]
POSTED.write_text(json.dumps(posted, ensure_ascii=False, indent=2), encoding="utf-8")
print("POST_ID", post["id"], post["status"], post["link"])

eye = subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_sixtones.py"), "--main", "松村北斗",
                      "--bottom", "長居で履いたスニーカーは", "--bottom", "どこのブランド？",
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
