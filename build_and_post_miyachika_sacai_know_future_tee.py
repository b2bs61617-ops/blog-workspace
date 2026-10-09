# -*- coding: utf-8 -*-
# chomoand-4.blog: 宮近海斗 ノキドア観劇(2026-10-09 X投稿)の私服 sacai KNOW FUTURE Tシャツ記事
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

IMG_DIR = ROOT / "frames_tmp" / "miyachika_sacai"
EYECATCH = ROOT / "images" / "miyachika_sacai_know_future_tee_eyecatch.jpg"
SRC = "https://x.com/Miyachika_TJ/status/2108460988110655854"
DRY = "--dry" in sys.argv

TITLE = "【観劇私服】宮近海斗の黒Tシャツはどこの？sacaiと判明！"

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


KEYS = ["chest", "patch"]
if not DRY:
    for k in KEYS:
        MEDIA[k] = upload_media(IMG_DIR / f"{k}.jpg")
        print("media", k, MEDIA[k]["id"])

URL_SACAI = "https://www.sacai.jp/"
URL_MERCARI = "https://jp.mercari.com/search?keyword=sacai%20KNOW%20FUTURE%20T"
URL_2ND = "https://www.2ndstreet.jp/search?category=810001&brand%5B%5D=005922"
URL_STAGE = "https://www.sakigake.jp/news/article/20260925EN0002/"
A = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
MARK = '<strong><span class="swl-marker mark_yellow">{}</span></strong>'

b = []
b.append(p([
    "2026年10月9日、宮近海斗さんが自身のXに、川島如恵留さんとの2ショット写真を投稿しました。",
    "川島如恵留さんが上田竜也さんとW主演を務める舞台『ノッキンオン・ロックドドア THE STAGE』を観劇したときの1枚で、川島さんはおなじみの「X」ポーズ、宮近さんは黒のカーディガンに黒Tシャツというシックな私服姿です。",
    "そのTシャツの胸元には、赤い丸に「KNOW FUTURE」の文字が入った刺繍ロゴがありました。",
    "写真をアップで確認したところ、このTシャツは" + MARK.format("sacai(サカイ)の「KNOW FUTURE T-Shirt」(2024年春夏)") + "とみられます。",
    "この記事では、Tシャツのデザインの特徴や「KNOW FUTURE」という言葉の意味、価格と今から買える場所をまとめます。",
]))
b.append(whatbox([
    "宮近海斗さんがノキドア観劇で着ていた黒Tシャツのブランド",
    "胸の「KNOW FUTURE」刺繍の意味",
    "Tシャツの品番・定価・カラー展開",
    "今から買える購入先(公式・中古)",
]))
b.append(minibox([
    ("着用日", "2026年10月9日のX投稿(舞台『ノッキンオン・ロックドドア THE STAGE』観劇時)"),
    ("ブランド", "sacai(サカイ)"),
    ("アイテム", "KNOW FUTURE T-Shirt(左胸に小さな刺繍ロゴ)"),
    ("品番", "24-0723S(2024年春夏)"),
    ("定価", "19,800円(税込)とみられる"),
]))
b.append(xembed(SRC))

b.append(h2("宮近海斗の黒Tシャツはsacaiの「KNOW FUTURE」"))
b.append(p([
    "宮近さんの写真を拡大すると、黒のTシャツの左胸に、赤い丸の真ん中を白い帯が横切るデザインの刺繍が入っています。",
    "帯の部分には「KNOW FUTURE」の文字があり、これはsacaiが2024年春夏シーズンに展開した「KNOW FUTURE」シリーズのロゴと一致します。",
    "Tシャツ自体は無地の黒で、胸のロゴだけがアクセントになったシンプルなつくりです。",
]))
b.append(img("chest", "黒のカーディガンの下に、胸に赤い「KNOW FUTURE」刺繍が入った黒Tシャツを着た宮近海斗"))
b.append(h3("① 左胸の赤い丸ロゴ"))
b.append(p([
    "いちばんの決め手は、左胸にある赤い丸のロゴです。",
    "丸の中央に白い帯があり、そこに「KNOW FUTURE」と入るデザインは、sacaiの「KNOW FUTURE T-Shirt」のスモールロゴと同じ配置・配色でした。",
    "プリントではなく刺繍なので糸の立体感があり、写真でも縁がくっきりしているのが分かります。",
]))
b.append(img("patch", "左胸の赤い丸に白い帯で「KNOW FUTURE」と入った刺繍ロゴのアップ"))
b.append(h3("② 無地のボディに小さなロゴだけ"))
b.append(p([
    "同じ「KNOW FUTURE」シリーズには、胸に大きくグラフィックを入れたプリントTシャツ(品番24-0720S)もあります。",
    "ただ、宮近さんが着ていたのはロゴが左胸に小さく入るだけのタイプなので、品番24-0723Sのスモールロゴのほうとみられます。",
    "カーディガンを羽織っても胸元のロゴがちょうどのぞく位置にあり、重ね着に向いた一枚です。",
]))
b.append(h3("③ 黒カーディガン×ゴールドのネックレスで大人っぽく"))
b.append(p([
    "この日の宮近さんは、Tシャツの上に金ボタンの黒いカーディガンを重ね、ゴールドのコインモチーフのネックレスと小ぶりのフープピアスを合わせていました。",
    "黒一色のコーディネートに、赤いロゴとゴールドの小物が効いていて、観劇らしいきちんと感もあるスタイルです。",
    "カーディガンとネックレスのブランドは、この写真だけでは特定できませんでした。",
]))

b.append(h2("「KNOW FUTURE」ってどういう意味？"))
b.append(p([
    "「KNOW FUTURE」は、パンクロックの代表的なフレーズ「NO FUTURE(未来なんてない)」をもじった言葉です。",
    "「NO(ない)」を同じ発音の「KNOW(知る)」に置き換えることで、「未来を知る」という前向きなメッセージに変えています。",
    "sacaiは2024年春夏コレクションでこの言葉をテーマのひとつにしていて、Tシャツなどにロゴとして使われました。",
    "パンクの反骨精神を残しつつ、希望を感じさせる言葉にしているのがsacaiらしいところですね。",
]))
b.append(p([
    "ちなみにsacai(サカイ)は、デザイナーの阿部千登勢さんが1999年に立ち上げた日本のブランドです。",
    "異素材を組み合わせたデザインで知られ、パリコレクションにも参加しています。",
    "宮近さんは以前、" + A("https://chomoand-4.blog/what-brand-is-kaito-miyachikas-casual-t-92", "「リズム天国」でもsacai×『インターステラー』のTシャツ") + "を着ていたことがあり、sacaiのTシャツはお気に入りのひとつなのかもしれません。",
    "また、メンバーの松田元太さんも同じ「KNOW FUTURE」ロゴのTシャツを色違いで着ていたとみられ、「ちゃかげん」のおそろいなのではと注目が集まっています。",
]))

b.append(h2("Tシャツの価格・購入先"))
b.append(p([
    "sacaiの「KNOW FUTURE T-Shirt」(品番24-0723S)の定価は、19,800円(税込)とみられます。",
    "カラーは黒のほか、白・グレー・ネイビーなどが展開されていました。",
    "2024年春夏のアイテムのため、公式オンラインストアでは現在取り扱いが見当たらず、新品で手に入れるのは難しい状況です。",
]))
b.append(table(["項目", "内容"], [
    ["ブランド", "sacai(サカイ)"],
    ["商品名", "KNOW FUTURE T-Shirt"],
    ["品番", "24-0723S"],
    ["シーズン", "2024年春夏"],
    ["カラー", "ブラック(宮近さん着用)、ホワイト、グレー、ネイビーなど"],
    ["素材", "コットン100%"],
    ["定価", "19,800円(税込)とみられる"],
    ["購入先", A(URL_SACAI, "sacai公式サイト") + "(現在は取り扱いなし)/" + A(URL_MERCARI, "メルカリ(sacai KNOW FUTURE Tで検索)") + "/" + A(URL_2ND, "セカンドストリート(sacaiのTシャツ一覧)")],
]))
b.append(p([
    "今から探すなら、メルカリなどのフリマアプリや、セカンドストリートのような古着店が現実的です。",
    "検索するときは「sacai KNOW FUTURE」で探し、胸に大きくプリントが入った24-0720Sではなく、左胸に小さな刺繍が入ったタイプかどうかを写真で確認してください。",
    "sacaiのTシャツはサイズ表記が「1〜5」の数字なので、実寸もあわせてチェックすると失敗しにくいですよ。",
]))

b.append(h2("宮近海斗が観劇した『ノッキンオン・ロックドドア THE STAGE』"))
b.append(p([
    "宮近さんが観劇したのは、青崎有吾さんのミステリー小説を初めて舞台化した『ノッキンオン・ロックドドア THE STAGE』です。",
    "上田竜也さんが御殿場倒理、川島如恵留さんが片無氷雨を演じるW主演作で、" + A(URL_STAGE, "東京公演は2026年10月6日〜25日にEXシアター有明、大阪公演は11月7日〜10日にオリックス劇場") + "で上演されます。",
    "宮近さんは投稿で、上田さんの倒理と川島さんの氷雨のコンビについて「最高でミステリーもストーリーもみなさんのお芝居も最後まで楽しかった」とつづっていました。",
    "「Xに投稿していい？」と聞くといつもXのポーズをしてくれるという川島さんとの、仲の良さが伝わる2ショットです。",
]))

b.append(summary([
    "宮近海斗さんがノキドア観劇の2ショットで着ていた黒Tシャツは、sacaiの「KNOW FUTURE T-Shirt」とみられる",
    "左胸の赤い丸に白い帯で「KNOW FUTURE」と入った刺繍ロゴが決め手",
    "品番24-0723S、2024年春夏のアイテムで定価は19,800円(税込)とみられる",
    "「KNOW FUTURE」はパンクの「NO FUTURE」をもじった前向きなメッセージ",
    "公式では現在取り扱いがなく、探すならメルカリや古着店が中心",
]))
b.append(p([
    "黒のTシャツに赤のワンポイントは、宮近さんのメンバーカラーの赤ともリンクしていて、さりげなくて素敵なチョイスでした。",
    "新しい私服が分かりしだい、またこのブログで紹介していきます。",
]))
b.append(linkbox([
    ("https://chomoand-4.blog/what-brand-is-kaito-miyachikas-casual-t-92", "【リズム天国】宮近海斗の黒Tはsacai×インターステラー？"),
    ("https://chomoand-4.blog/where-did-kaito-miyachika-get-965", "【御殿場】宮近海斗が買ったTシャツはどこの？バレンシアガと判明！"),
    ("https://chomoand-4.blog/where-is-kaito-miyachikas-gree-988", "宮近海斗の緑の炎Tシャツはどこの？YARDSALEと判明！"),
    ("https://chomoand-4.blog/where-are-kaito-miyachikas-sun-982", "宮近海斗のサングラスはどこの？ディオールのDiorTagと判明！"),
]))

content = "\n\n".join(b)
plain = re.sub(r"<!--.*?-->|<[^>]+>|\[\[IMG.*?\]\]", "", content, flags=re.S)
print("chars:", len(re.sub(r"\s", "", plain)))
(ROOT / "articles" / "miyachika_sacai_know_future_tee.html").write_text(content, encoding="utf-8")
if DRY:
    sys.exit()

payload = {"title": TITLE, "content": content, "status": "draft",
           "slug": "miyachika-sacai-know-future-tee", "categories": [3, 9], "author": 2}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"], "status", post["status"], "SLUG", post["slug"])

eye = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
     "--main", "宮近海斗",
     "--bottom", "観劇私服の黒Tシャツは", "--bottom", "sacaiと判明！",
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
