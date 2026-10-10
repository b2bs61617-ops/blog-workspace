# -*- coding: utf-8 -*-
# chomoand-4.blog: 宮近海斗CMのタカラ無炭酸チューハイ「するり」10/13全ルート販売(販売店拡大)記事
import json, base64, os, re, sys, subprocess
from pathlib import Path
import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_CHOMO4_URL"].rstrip("/")
AUTH = base64.b64encode(f'{ENV["WP_CHOMO4_USERNAME"]}:{ENV["WP_CHOMO4_APP_PASSWORD"]}'.encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}
HJSON = {**HEADERS_AUTH, "Content-Type": "application/json"}

EYECATCH = ROOT / "images" / "miyachika_sururi_sales_expand_eyecatch.jpg"
SRC = "https://x.com/sururi_TaKaRa/status/2108829897691148603"
DRY = "--dry" in sys.argv

TITLE = "宮近海斗CMのするりはどこで買える？10/13からスーパーでも！"

BORDER = "#f3d6d6"
ACCENT = "#ef9a9a"
BG = "#fdf3f3"


def upload_media(filepath: Path):
    headers = {**HEADERS_AUTH, "Content-Type": "image/jpeg",
               "Content-Disposition": f'attachment; filename="{filepath.name}"'}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=filepath.read_bytes())
    r.raise_for_status()
    return r.json()


def p(sentences):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(sentences) + "</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def whatbox(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(rows):
    lines = "\n".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
        for i, (k, v) in enumerate(rows))
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{lines}
</div>''')


def table(header, rows):
    th = "".join(f'<td style="border:1px solid #ccc;background:{BG};padding:8px;font-weight:bold;">{c}</td>' for c in header)
    trs = "\n".join("<tr>" + "".join(f'<td style="border:1px solid #ccc;padding:8px;">{c}</td>' for c in r) + "</tr>" for r in rows)
    return wphtml(f'''<table style="width:100%;border-collapse:collapse;margin:0 0 16px 0;">
<tbody>
<tr>{th}</tr>
{trs}
</tbody>
</table>''')


def summary(items):
    lis = "\n".join(
        f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {ACCENT};border-radius:3px;color:{ACCENT};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{i}</p>'
        for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">まとめ</p>
<div style="padding:14px 18px;background:{BG};">
{lis}
</div>
</div>''')


def linkbox(items):
    lis = "\n".join(f'<li><a href="{u}">{t}</a></li>' for u, t in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


def xembed(url):
    u = url.replace("x.com", "twitter.com")
    return wphtml(f'''<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><a href="{u}">{u}</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>''')


MEDIA = {}


def img(key, alt):
    if DRY:
        return f"[[IMG {key}: {alt}]]"
    m = MEDIA[key]
    src = m["source_url"]
    w, h = m["media_details"]["width"], m["media_details"]["height"]
    sizes = m["media_details"].get("sizes", {})
    med = sizes.get("medium", {"source_url": src, "width": w})
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{src}" alt="{alt}" width="{w}" height="{h}"
  style="max-width:100%;height:auto;"
  srcset="{med["source_url"]} {med["width"]}w, {src} {w}w"
  sizes="(max-width: {w}px) 100vw, {w}px">
<figcaption style="font-size:0.8em;color:#888;">出典:{SRC}</figcaption>
</figure>''')


def ytembed(vid, title):
    return wphtml(f'''<div style="position:relative;width:100%;padding-top:56.25%;margin:0 0 16px 0;">
<iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://www.youtube.com/embed/{vid}" title="{title}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>''')


URL_REL_0909 = "https://www.takarashuzo.co.jp/news/1188726_1999.html"
URL_REL_CM = "https://www.takarashuzo.co.jp/news/1188643_1999.html"
URL_BRAND = "https://www.takarashuzo.co.jp/products/soft_alcohol/sururi/"
URL_X = "https://x.com/sururi_TaKaRa"
A = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
MARK = '<strong><span class="swl-marker mark_yellow">{}</span></strong>'

b = []
b.append(p([
    "Travis Japanのリーダー・宮近海斗さんがブランドアンバサダーを務める、宝酒造の「タカラ無炭酸チューハイ するり」。",
    "2026年4月の発売時はコンビニ限定だったため、「近所のスーパーで探しても見つからない」という声も少なくありませんでした。",
    "そのするりが、" + MARK.format("2026年10月13日(火)から全国の全ルートで販売開始") + "されます。",
    "スーパーマーケットなどでも買えるようになるうえ、同じ日に新フレーバー〈国産ピンクグレフル〉も加わって全3種類になります。",
    "この記事では、するりがどこで買えるのか、新しい味や価格、宮近さんが出演しているCMの内容までまとめます。",
]))
b.append(whatbox([
    "宮近海斗さんCMの「するり」はどこで買える？(10月13日からの販売店)",
    "新フレーバー〈国産ピンクグレフル〉を含む全3種類の違い",
    "価格・アルコール度数・果汁などのスペック",
    "宮近海斗さん初の単独CMの内容と、本人が語った飲んだ感想",
]))
b.append(minibox([
    ("商品名", "タカラ無炭酸チューハイ「するり」(宝酒造)"),
    ("販売拡大日", "2026年10月13日(火)から全国・全ルートで販売"),
    ("味", "国産シャインマスカット/国産白桃/国産ピンクグレフル(新)"),
    ("スペック", "350ml缶・アルコール5%・甘味料不使用"),
    ("アンバサダー", "宮近海斗(Travis Japan)、初の単独CM"),
]))
b.append(xembed(SRC))

b.append(h2("宮近海斗CMの「するり」はどこで買える？"))
b.append(p([
    "結論から言うと、するりは" + MARK.format("10月13日からはコンビニに加えて、スーパーマーケットなどでも購入できるようになります") + "。",
    "宝酒造が2026年9月9日に出したニュースリリースでは、" + A(URL_REL_0909, "「より多くのお客様にお楽しみいただけるよう、全ルートへ販路を拡大」") + "と発表されました。",
    "ブランドサイトでも、好評につき取扱店が広がり、全国のスーパーマーケットなどでも買えるようになると案内されています。",
]))
b.append(h3("① 4月7日〜10月12日はコンビニ限定"))
b.append(p([
    "するりがデビューしたのは2026年4月7日(火)です。",
    "このときは「コンビニエンスストア先行発売」という形で、全国のコンビニだけで売られていました。",
    "Travis Japanのメンバーでも、松田元太さんがドラマの撮影帰りにコンビニで見つけて飲みながら帰ったと話していて、まさに「コンビニで見かけるお酒」という位置づけだったわけです。",
    "そのときの様子は" + A("https://chomoand-4.blog/where-is-the-jersey-from-genta-1213", "松田元太さんのインスタライブのジャージの記事") + "でも紹介しています。",
]))
b.append(h3("② 10月13日からはスーパーなど全ルートへ"))
b.append(p([
    "10月13日(火)からは、販売ルートが「全ルート」に広がります。",
    "酒類業界で「全ルート」というと、コンビニだけでなくスーパーマーケット、ドラッグストア、酒販店、ディスカウントストアなど、お酒を扱う一般的なお店全般を指すのが一般的です。",
    "ただし、リリースで具体的なチェーン名までは発表されていません。",
    "公式Xでも「店舗によりお取り扱いのない場合がございます」と注意書きがあるので、確実に買いたい方は、行きつけのお店に入荷予定を聞いてみるのが安心です。",
]))
b.append(h3("③ 見つからないときの探し方"))
b.append(p([
    "全ルート販売とはいえ、発売直後はお店によって棚に並ぶタイミングがずれることがあります。",
    "缶チューハイ売り場の中でも、するりは炭酸入りのチューハイとは見た目が違い、水面に果実が浸かったような透明感のあるデザインの缶です。",
    "350ml缶だけの展開なので、500ml缶の棚ではなく350ml缶の列を探してみてください。",
    "それでも見つからないときは、宝酒造のお客様相談室(0120-120-064、平日9時〜17時)に問い合わせる方法もあります。",
]))

b.append(h2("新フレーバー〈国産ピンクグレフル〉が登場！全3種類の違い"))
b.append(p([
    "今回の販路拡大と同時に、3つ目の味〈国産ピンクグレフル〉が新発売されます。",
    "宝酒造によると、ピンクグレープフルーツは「炭酸が苦手な方に人気のフルーツ」として選ばれたそうです。",
    "これまでの〈国産シャインマスカット〉〈国産白桃〉とあわせて、甘めの2種類にほろ苦さのある柑橘系が加わる形になりました。",
]))
b.append(table(["味", "使っている果実", "果汁", "発売日"], [
    ["国産シャインマスカット", "国産シャインマスカットのピューレ", "0.1%", "2026年4月7日"],
    ["国産白桃", "国産白桃のペースト", "0.3%", "2026年4月7日"],
    ["国産ピンクグレフル(新)", "国産ピンクグレープフルーツのペースト", "0.2%", "2026年10月13日"],
]))
b.append(p([
    "3種類とも、国産の果実ペーストやピューレを使い、食品添加物の甘味料は使っていません。",
    "さらに緑茶エキスが加えられていて、炭酸がない分、味がぼやけないように後味を整える役割をしているそうです。",
    "緑茶の風味そのものはしないとのことですが、お茶割り好きで知られる宮近さんのお酒に緑茶エキスが入っているのは、ちょっとうれしい偶然ですね。",
]))
b.append(p([
    "ちなみにピンクグレフルは、9月22日〜26日に渋谷で開かれた無料配布イベント「炭酸卒業式典 PRODUCED BY タカラ無炭酸チューハイするり」で、店頭発売よりひと足早く配られていました。",
]))

b.append(h2("するりの価格・スペック"))
b.append(p([
    "4月にコンビニで先行発売されたときの参考小売価格は、350ml缶1本176円(税抜)でした。",
    "一方、10月13日からの全ルート販売のリリースでは「参考小売価格の設定はございません」とされていて、価格はお店ごとに決まる形になります。",
    "スーパーやディスカウントストアでは、コンビニより少し安く買えることもありそうです。",
]))
b.append(table(["項目", "内容"], [
    ["商品名", "タカラ無炭酸チューハイ「するり」"],
    ["メーカー", "宝酒造"],
    ["品目", "リキュール"],
    ["容量", "350ml缶(24本入りケースあり)"],
    ["アルコール分", "5%(純アルコール量14g/350ml)"],
    ["炭酸", "なし(無炭酸)"],
    ["甘味料", "不使用"],
    ["価格", "コンビニ先行時の参考小売価格176円(税抜)、10/13以降は店舗ごと"],
    ["購入先", "コンビニ・スーパーマーケットなど(10/13〜)"],
    ["公式", A(URL_BRAND, "ブランドサイト") + "/" + A(URL_X, "公式X(@sururi_TaKaRa)")],
]))
b.append(p([
    "アルコール5%は一般的な缶チューハイと同じくらいの度数です。",
    "炭酸がないぶん飲み口がやわらかく、つい進んでしまいやすいので、飲みすぎには気をつけてくださいね。",
]))

b.append(h2("「炭酸がしんどい」から生まれた無炭酸チューハイ"))
b.append(p([
    "するりは、東京で働く20〜30代の会社員と一緒に作り上げたブランドです。",
    "宝酒造の調査では、20代の54.4%、女性の41.2%が「缶チューハイを飲んでいるときに炭酸がしんどいと感じたことがある」と答えたそうです。",
    "そこで、炭酸が苦手で缶チューハイを避けてきた人にも飲んでもらえる、新しいカテゴリーとして開発されました。",
    "ベースには宮崎県の黒壁蔵で造られた樽貯蔵の焼酎がブレンドされていて、炭酸がなくても単調にならない味わいを目指しています。",
]))

b.append(h2("宮近海斗の初単独CMの内容は？"))
b.append(p([
    "宮近さんは、するりの発売に合わせてブランドアンバサダーに起用されました。",
    "Travis Japanとしてはさまざまな広告に出演してきましたが、" + MARK.format("宮近さん1人でのCM出演はこれが初めて") + "です。",
    "Web CMは" + A(URL_REL_CM, "「やっと帰ってきた」篇と「いいこと教えてあげる」篇の2本(各15秒)") + "で、2026年4月7日から配信されています。",
]))
b.append(h3("① 「やっと帰ってきた」篇"))
b.append(p([
    "どちらのCMも、同棲2年目のカップルの日常を「彼女目線」で描いたストーリーです。",
    "「やっと帰ってきた」篇では、帰宅した彼女を待っていた宮近さんが、するりをそっと差し出します。",
    "食卓でするりを飲みながら、ほろ酔いの笑顔で話しかける姿が見どころです。",
]))
b.append(h3("② 「いいこと教えてあげる」篇"))
b.append(p([
    "「いいこと教えてあげる」篇は、ソファに並んで座った2人が、するりのフルーティーなおいしさを分け合うシーンです。",
    "刺激はないけれど心地よい2人の時間を、無炭酸のやさしい飲み口に重ねた演出になっています。",
    "CMの映像はブランドサイトや公式Xで見ることができ、公開当時は「彼氏感が自然すぎる」と大きな反響がありました。",
]))
b.append(h3("③ 起用の理由は「お茶割り好き」"))
b.append(p([
    "宝酒造の企画担当者は、宮近さんを選んだ理由として、普段からお茶割り好きで知られていることを挙げています。",
    "炭酸のないお酒を好む宮近さんを中心に「無炭酸っていいよね」という価値観を広げたい、という狙いだそうです。",
    "また、Travis Japanのリーダーとしてライブの乾杯の掛け声で会場を盛り上げる姿も、ファンと一緒に新商品を盛り上げる存在にぴったりだったとのことです。",
]))

b.append(h2("宮近海斗が語った「するり」の感想"))
b.append(p([
    "宝酒造の公式YouTubeでは、CM撮影直後の宮近さんにインタビューしたメイキング動画が公開されています。",
    "宮近さんは初の単独CMについて、メンバーとも話していたほど挑戦してみたかったことのひとつで、オファーを聞いたときは「素直に上がりました」と喜びを語っていました。",
    "撮影は本当の家のようなスタジオで行われ、自分の好きなものも用意してもらったそうです。",
]))
b.append(ytembed("7F4bnFKLCew", "タカラ無炭酸チューハイするり CMメイキング動画"))
b.append(p([
    "するりを飲んだ感想については、「お酒が好きな方も、あまり得意じゃない方も、タイトルの通りするり飲みやすい」とコメント。",
    "フルーティーなので味の濃い料理にも合わせやすく、お腹がふくれてきても無炭酸だから飲みやすい、と話していました。",
    "最後には「刺激的な毎日もいいですが、たまには僕と一緒に刺激のない心地いい時間で癒されませんか？」と、CMの世界観そのままのメッセージを送っています。",
]))

b.append(summary([
    "宮近海斗さんがCM出演する「タカラ無炭酸チューハイ するり」は、10月13日(火)から全国の全ルートで販売開始",
    "4月7日〜はコンビニ限定だったが、10月13日からはスーパーマーケットなどでも買える(店舗により取り扱いなしの場合あり)",
    "同日に新フレーバー〈国産ピンクグレフル〉が登場し、シャインマスカット・白桃とあわせて全3種類",
    "350ml缶・アルコール5%・甘味料不使用、コンビニ先行時の参考小売価格は176円(税抜)",
    "宮近さん初の単独CMは「やっと帰ってきた」篇と「いいこと教えてあげる」篇の2本",
]))
b.append(p([
    "スーパーでも手に取れるようになれば、まとめ買いしやすくなりますね。",
    "新しいピンクグレフルを飲みながら、宮近さんのCMを見返してみるのもおすすめです。",
]))
b.append(linkbox([
    ("https://chomoand-4.blog/where-is-the-jersey-from-genta-1213", "松田元太のインスタライブのジャージはどこの？中村海人デザインと判明！"),
    ("https://chomoand-4.blog/j-league-when-will-torajas-new-439", "【Jリーグ】トラジャの新CMはいつから？全30パターンの違いは？"),
    ("https://chomoand-4.blog/where-are-the-towel-scarves-th-1220", "宮近海斗と吉澤閑也がユアスタで巻いたタオルマフラーはどこの？"),
    ("https://chomoand-4.blog/what-brand-is-kaito-miyachikas-casual-t-92", "【リズム天国】宮近海斗の黒Tはsacai×インターステラー？"),
]))

content = "\n\n".join(b)
plain = re.sub(r"<!--.*?-->|<[^>]+>|\[\[IMG.*?\]\]", "", content, flags=re.S)
print("chars:", len(re.sub(r"\s", "", plain)))
(ROOT / "articles" / "miyachika_sururi_sales_expand.html").write_text(content, encoding="utf-8")
if DRY:
    sys.exit()

payload = {"title": TITLE, "content": content, "status": "draft",
           "slug": "miyachika-sururi-where-to-buy-supermarket", "categories": [3, 9], "author": 2}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"], "status", post["status"], "SLUG", post["slug"])

eye = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
     "--main", "宮近海斗",
     "--bottom", "CMのするりはどこで買える？", "--bottom", "10/13からスーパーでも！",
     "--color-key", "宮近海斗", "--out", str(EYECATCH)],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
)
print(eye.stdout[-300:], eye.stderr[-300:])
if eye.returncode == 0:
    em = upload_media(EYECATCH)
    requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}", headers=HJSON,
                  data=json.dumps({"featured_media": em["id"], "status": "draft"}).encode("utf-8")).raise_for_status()
    print("eyecatch media", em["id"])
print("DONE")
