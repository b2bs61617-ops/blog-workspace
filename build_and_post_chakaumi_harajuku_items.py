# -*- coding: utf-8 -*-
# chomoand-4.blog: ちゃかうみ原宿散歩(公式YouTube 2026-10-17)の2人の着用品・アクセサリー(2026-10-19)
import json, base64, os, re, sys, subprocess
from pathlib import Path
import requests
from PIL import Image

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

IMG_DIR = ROOT / "images" / "chakaumi_harajuku_items"
EYECATCH = ROOT / "images" / "chakaumi_harajuku_items_eyecatch_canva.jpg"
DRY = "--dry" in sys.argv

TITLE = "【原宿散歩】宮近海斗と中村海人の私服は？トムフォードでお揃い！"

# 2人回(宮近=赤・中村=緑)なのでグループ色の紫で統一
ACC = "#7e57c2"
BORDER = "#d9cdf0"
BG = "#f5f2fb"


def shrink(src: Path, max_side=1600) -> Path:
    im = Image.open(src).convert("RGB")
    if max(im.size) > max_side:
        im.thumbnail((max_side, max_side))
    out = src.with_name(src.stem + "_web.jpg")
    im.save(out, quality=88)
    return out


def upload_media(filepath: Path, ctype="image/jpeg"):
    headers = {**HEADERS_AUTH, "Content-Type": ctype,
               "Content-Disposition": f'attachment; filename="{filepath.name}"'}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=filepath.read_bytes())
    r.raise_for_status()
    return r.json()


def img_urls(media):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    full_w = media["media_details"]["width"]
    full_h = media["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    w = large["width"]
    h = int(w * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {full_w}w'
    return large["source_url"], w, h, srcset


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
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(rows, title=None):
    head = f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n' if title else ""
    lines = "\n".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
        for i, (k, v) in enumerate(rows))
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{head}{lines}
</div>''')


def table(header, rows):
    th = "".join(f'<td style="border:1px solid #ccc;background:{BORDER};padding:8px;font-weight:bold;">{c}</td>' for c in header)
    trs = "\n".join("<tr>" + "".join(f'<td style="border:1px solid #ccc;padding:8px;">{c}</td>' for c in r) + "</tr>" for r in rows)
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr>{th}</tr>
{trs}
</tbody></table></figure>
<!-- /wp:table -->'''


def summary(items):
    lis = "\n".join(
        f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {ACC};border-radius:3px;color:{ACC};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{i}</p>'
        for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">まとめ</p>
<div style="padding:14px 18px;background:{BG};">
{lis}
</div>
</div>''')


def linkbox(items):
    lis = "\n".join(f'<li><a href="{u}">{t}</a></li>' for u, t in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACC};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


def image_block(media, alt, caption):
    if media is None:  # dry run
        return wphtml(f'<figure class="wp-block-image size-large"><img src="" alt="{alt}"><figcaption style="font-size:0.8em;color:#888;">出典:{caption}</figcaption></figure>')
    src, w, h, srcset = img_urls(media)
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{src}" alt="{alt}" width="{w}" height="{h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {w}px) 100vw, {w}px">
<figcaption style="font-size:0.8em;color:#888;">出典:{caption}</figcaption>
</figure>''')


def igembed(url, label):
    return wphtml(f'''<div style="max-width:540px;margin:0 auto 16px;"><blockquote class="instagram-media" data-instgrm-permalink="{url}?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" style="background:#FFF;border:0;border-radius:3px;box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);margin:1px;max-width:540px;min-width:326px;padding:0;width:calc(100% - 2px);"><a href="{url}?utm_source=ig_embed&amp;utm_campaign=loading" target="_blank" rel="noopener">{label}</a></blockquote>
<script async src="https://www.instagram.com/embed.js"></script></div>''')


A = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
M = lambda t: f'<strong><span class="swl-marker mark_pink">{t}</span></strong>'

YT = "https://www.youtube.com/watch?v=fxDMIN2JK0c"
CAP = A(YT, "Travis Japan公式YouTube「【原宿散歩】ほぼプライベート！ちゃかうみでお散歩♬」")
URL_6C = "https://sixcrayon.com/products/6crayon-flat-brimmed-baseball-cap"
URL_202 = "https://chomoand-4.blog/the-hat-that-kaito-miyachika-w-202"
URL_721 = "https://chomoand-4.blog/what-is-the-birthday-present-f-721"
URL_729 = "https://chomoand-4.blog/where-does-kaito-nakamuras-cas-729"
URL_703 = "https://chomoand-4.blog/kaito-miyachikas-casual-checke-703"
URL_207 = "https://chomoand-4.blog/the-t-shirt-kaito-miyachika-wo-207"
URL_982 = "https://chomoand-4.blog/where-are-kaito-miyachikas-sun-982"

IMGS = {
    "two": ("two_shot.jpg", "竹下通りでカメラに向かう宮近海斗(左)と中村海人(右)"),
    "cap": ("miyachika_cap_glasses.jpg", "宮近海斗のCロゴのキャップとトムフォードのサングラス"),
    "cap_back": ("cap_back.jpg", "宮近海斗のキャップの後ろに入った「Crayon design」の刺しゅう"),
    "hoodie": ("hoodie_sleeve.jpg", "袖にCarharttのロゴが入った宮近海斗のパーカー"),
    "beanie": ("nakamura_beanie.jpg", "中村海人のCHANELのビーニーとトムフォードのメガネ"),
    "glasses": ("nakamura_beanie_glasses_side.jpg", "中村海人のメガネのつるに付いたトムフォードのTのパーツ"),
    "sit": ("outfits_sitting.jpg", "チュロス休憩中の中村海人(左)と宮近海斗(右)の全身"),
}

media = {k: None for k in IMGS}
if not DRY:
    for k, (fn, _) in IMGS.items():
        media[k] = upload_media(shrink(IMG_DIR / fn))
        print("uploaded", k, media[k]["id"])


def img(k):
    return image_block(media[k], IMGS[k][1], CAP)


b = []

# ---- リード ----
b.append(p([
    "2026年10月17日にTravis Japanの公式YouTubeで公開された「【原宿散歩】ほぼプライベート！ちゃかうみでお散歩♬」。",
    "宮近海斗さんと中村海人さんが竹下通りから外苑前まで歩いた回で、「ほぼプライベート」というタイトルどおり、2人とも普段着に近いラフな服装でした。",
]))
b.append(p([
    "映像をアップにして確かめてみると、" + M("2人ともトムフォードのアイウェア") + "を着けていました。",
    "宮近さんはサングラス、中村さんはメガネで、宮近さんのサングラスは中村さんからの誕生日プレゼントとみられます。",
    "ほかにも、宮近さんの" + M("6CRAYONのキャップ") + "、中村さんの" + M("CHANELのビーニー") + "など、過去に着けていたアイテムが次々に登場しています。",
]))
b.append(whatbox(["2人の服装の一覧", "宮近海斗のキャップ・サングラス・パーカー", "中村海人のビーニー・メガネ・シャツ", "値段と買える場所"]))

# ---- 一覧 ----
b.append(h2("ちゃかうみの原宿散歩コーデを一覧で"))
b.append(img("two"))
b.append(p([
    "見分け方は、キャップとサングラスが宮近さん、ニット帽とメガネが中村さんです。",
    "画面のテロップでも、キャップ姿のほうに「宮近海斗」と名前が出ていました。",
    "分かったものを表にまとめます。",
]))
b.append(table(["", "アイテム", "ブランド・モデル"], [
    ["宮近海斗", "キャップ", "6CRAYON「Vintage Flat Top Casual Baseball Cap」(黒)"],
    ["宮近海斗", "サングラス", "TOM FORD(誕生日プレゼントとみられる)"],
    ["宮近海斗", "パーカー", "Carhartt(袖ロゴ入り、モデルは未確定)"],
    ["宮近海斗", "パンツ・時計・ピアス", "黒のワイドパンツ、シルバー×ゴールドの時計、ゴールドのフープピアス(ブランドは未確定)"],
    ["中村海人", "ビーニー", "CHANEL「Beanie Cashmere」とみられる"],
    ["中村海人", "メガネ", "TOM FORD(ブルーライトカットレンズとみられる)"],
    ["中村海人", "シャツ・インナー・デニム", "青×黒のチェックシャツ、白のリブタンクトップ、ライトブルーのデニム(ブランドは未確定)"],
]))

# ---- お揃い ----
b.append(h2("2人のアイウェアはトムフォードでお揃い"))
b.append(minibox([
    ("宮近海斗", "TOM FORDのサングラス(黒フレーム・グレーレンズ)"),
    ("中村海人", "TOM FORDのメガネ(ブラウン系フレーム・クリアレンズ)"),
    ("決め手", "つるの付け根に付いた金属の「T」のパーツ"),
]))
b.append(p([
    "今回いちばん目を引いたのが、2人のアイウェアです。",
    "形の近い黒っぽいフレームで、どちらもつる(テンプル)の付け根に金属の「T」のパーツが付いています。",
    "この「T」はトムフォードのアイウェアの目印になっているデザインです。",
]))
b.append(h3("宮近海斗のサングラスは誕生日プレゼントとみられる"))
b.append(img("cap"))
b.append(p([
    "宮近さんのサングラスは、太めの黒いフレームにグレーのレンズです。",
    "宮近さんは2026年9月22日の誕生日のインスタライブで、中村さんからトムフォードのサングラスをプレゼントされていました。",
    "黒いフレームとTのパーツという特徴が同じなので、そのとき贈られたサングラスを着けている可能性が高そうです。",
    "ただ、ライブの映像は小さく、型番が同じかどうかまでは確かめられませんでした。",
]))
b.append(p([
    "プレゼントの場面は" + f'<a href="{URL_721}">宮近海斗の誕生日プレゼントのサングラスの記事</a>' + "で紹介しています。",
    "宮近さんは別の日に" + f'<a href="{URL_982}">ディオールのサングラス</a>' + "を着けていたこともあり、サングラス好きな一面がうかがえます。",
]))
b.append(h3("中村海人はトムフォードのメガネ"))
b.append(img("glasses"))
b.append(p([
    "中村さんがかけていたのは、色の濃いブラウン系のフレームに透明なレンズのメガネです。",
    "横から見ると、細いつるの付け根にやはり「T」のパーツが付いていて、こちらもトムフォードだと分かります。",
    "サングラスではなくメガネなので、まったく同じものではなく「トムフォードでそろえた」形です。",
]))
b.append(p([
    "レンズにはうっすら青い反射が見えます。",
    "トムフォードのメガネには、型番の最後に「-B」が付く、ブルーライトカットレンズ入りのモデルがあります。",
    "中村さんのメガネもこのタイプの可能性がありますが、型番までは映像から読み取れませんでした。",
]))
b.append(p([
    "プレゼントした中村さんが、自分もトムフォードを選んでいるのはファンとしてうれしいポイントです。",
    "ちなみに中村さんは、" + f'<a href="https://chomoand-4.blog/travis-japan-favorite-perfume-1278">トラジャの愛用香水の記事</a>' + "で紹介したとおり、トムフォードの香水「ロストチェリー」の愛用者でもあります。",
]))

# ---- 宮近 ----
b.append(h2("宮近海斗の服装"))
b.append(minibox([
    ("キャップ", "6CRAYON「Vintage Flat Top Casual Baseball Cap」"),
    ("パーカー", "Carharttの袖ロゴ入りフーディー"),
    ("そのほか", "黒のワイドパンツ、コンビの時計、ゴールドのフープピアス"),
]))
b.append(h3("キャップはコストコ回と同じ6CRAYON"))
b.append(p([
    "黒のキャップの正面には、白い筆記体の「C」の刺しゅうが入っています。",
    "つばは平らで、裏側が緑色になっているのも特徴です。",
    "決め手になったのは、竹下通りを歩く後ろ姿に映った、後ろの「Crayon design」という刺しゅうでした。",
]))
b.append(img("cap_back"))
b.append(p([
    "6CRAYON(シックスクレヨン)の「Vintage Flat Top Casual Baseball Cap」は、販売ページで正面に「C」、後ろに「Crayon Design」の刺しゅうが入ると紹介されています。",
    "素材はコットン100%で、頭まわりは55〜66cm、公式ストアの価格は50ドルです。",
    "公式ストアは中国から発送する海外のショップで、調べた時点では売り切れになっていました。",
]))
b.append(p([
    "宮近さんは9月公開のコストコの動画でも、同じ6CRAYONのキャップをかぶっていました。",
    "詳しくは" + f'<a href="{URL_202}">宮近海斗がコストコでかぶってた帽子の記事</a>' + "にまとめています。",
    "1か月ほどの間に2回も登場しているので、かなりのお気に入りなのかもしれません。",
]))
b.append(h3("パーカーは袖にCarharttのロゴ"))
b.append(img("hoodie"))
b.append(p([
    "グレーのパーカーには、袖に沿って黄色の「Carhartt」のロゴが縦に入っています。",
    "おなかのポケットにも四角いロゴのラベルが付いていて、全体に白いペンキが飛んだような柄が見えます。",
]))
b.append(p([
    "袖に縦ロゴが入るパーカーは、アメリカのCarharttの定番「Loose Fit Midweight Logo Sleeve Graphic Sweatshirt」(K288)と同じデザインです。",
    "アメリカでの定価は60ドル前後で、日本では並行輸入品が多く売られています。",
    "ただ、ペンキの柄が加工なのか着ているうちについたものなのかは分からず、モデル名は確定できませんでした。",
]))
b.append(p([
    "宮近さんはCarharttの服をよく着ていて、" + f'<a href="{URL_207}">コストコ回のTシャツ</a>' + "や" + f'<a href="{URL_703}">私服のチェックシャツ</a>' + "もCarharttでした。",
]))
b.append(h3("時計とピアス、パンツ"))
b.append(p([
    "チュロス休憩の場面では、宮近さんの手首にシルバーとゴールドのコンビの腕時計が映ります。",
    "白っぽい文字盤の丸い時計ですが、映ったのは一瞬で、ブランドまでは確認できませんでした。",
    "耳には両耳ともゴールドのフープピアスが光っています。",
]))
b.append(p([
    "下は黒のワイドパンツで、大きめのパーカーとあわせたゆったりしたシルエットです。",
    "キャップとサングラスで顔まわりを引き締め、全体は黒とグレーでまとめたストリート寄りのコーデでした。",
]))

# ---- 中村 ----
b.append(h2("中村海人の服装"))
b.append(minibox([
    ("ビーニー", "CHANEL「Beanie Cashmere」とみられる"),
    ("シャツ", "青×黒のチェックのネルシャツ"),
    ("そのほか", "白のリブタンクトップ、ライトブルーのデニム、黒い靴"),
]))
b.append(h3("ビーニーはCHANELのカメリアビーニーとみられる"))
b.append(img("beanie"))
b.append(p([
    "黒いリブ編みのビーニーには、白い花の形のモチーフと、まん中にCHANELの「CC」マークが入っています。",
    "中村さんは9月22日の千賀健永さんのインスタライブでも、同じ見た目のビーニーをかぶっていました。",
    "そのときに調べたCHANELの「Beanie Cashmere」(品番AAA748B19217NACWY)とデザインが一致するので、同じものとみられます。",
]))
b.append(p([
    "カシミヤ100%の2023年秋冬のアイテムで、CHANELの公式サイトではブティックでの扱いのため価格が出ていません。",
    "海外の中古ショップでは650〜850ドル(約10万〜13万円)ほどで取引されている人気のモデルです。",
    "詳しくは" + f'<a href="{URL_729}">千賀健永の配信で中村海人がかぶってたビーニーの記事</a>' + "で紹介しています。",
]))
b.append(h3("シャツは青×黒のチェック"))
b.append(img("sit"))
b.append(p([
    "トップスは、水色と黒のチェックがグラデーションのように切り替わる、厚手のネルシャツです。",
    "胸にはふた付きのポケットが2つあり、インナーに白のリブタンクトップを合わせていました。",
    "シャツのタグやロゴは映っておらず、ブランドは分かりませんでした。",
]))
b.append(p([
    "下はライトブルーのゆったりしたデニムに、黒い靴を合わせています。",
    "ニット帽とメガネ、チェックシャツにデニムという、秋らしい落ち着いた組み合わせでした。",
]))

# ---- 価格 ----
b.append(h2("値段と買える場所"))
b.append(p([
    "ブランドとモデルまで分かったものの値段と買える場所をまとめます。",
]))
b.append(table(["着ていた人", "アイテム", "参考価格", "買える場所"], [
    ["宮近海斗", "6CRAYON Vintage Flat Top Casual Baseball Cap(黒)", "50ドル", A(URL_6C, "6CRAYON公式ストア") + "(海外発送・調べた時点で売り切れ)"],
    ["宮近海斗", "Carhartt 袖ロゴのパーカー(K288と同じデザイン)", "60ドル前後(アメリカ定価)", "並行輸入品を扱う通販など"],
    ["中村海人", "CHANEL Beanie Cashmere", "価格非公開(中古は約10万〜13万円)", "CHANELのブティック・中古ショップ"],
    ["2人", "TOM FORDのサングラス・メガネ", "型番が分からず不明", "TOM FORDの取扱店・眼鏡店"],
]))
b.append(p([
    "トムフォードは型番によって値段が大きく変わるため、ここでは参考価格を出していません。",
    "誕生日プレゼントの記事では、トムフォードのサングラスは国内で3万円台後半〜8万円ほどが目安と紹介しています。",
    "6CRAYONのキャップは海外のショップなので、送料や届くまでの日数も確認してから注文してください。",
]))

# ---- まとめ ----
b.append(h2("まとめ"))
b.append(summary([
    "2人ともトムフォードのアイウェア(宮近はサングラス、中村はメガネ)",
    "宮近のサングラスは、中村からの誕生日プレゼントとみられる",
    "宮近のキャップは6CRAYON(50ドル)で、コストコ回と同じもの",
    "宮近のパーカーは袖にCarharttのロゴ入り",
    "中村のビーニーはCHANELの「Beanie Cashmere」とみられる",
]))
b.append(p([
    "プレゼントしたサングラスを宮近さんが着け、中村さんも同じトムフォードのメガネで歩いていた今回の散歩。",
    "ほぼプライベートの動画だからこそ、2人の仲の良さが服装にも表れていたのかもしれません。",
    "ちゃかうみの私服をまねしたい人は、まずはアイウェアからそろえてみてはいかがでしょうか！",
]))
b.append(linkbox([
    (URL_721, "宮近海斗の誕生日プレゼントはサングラス？贈り主は中村海人と判明！"),
    (URL_202, "宮近海斗がコストコでかぶってた帽子は6CRAYONと判明！"),
    (URL_729, "千賀健永の配信で中村海人が被ってたビーニーはCHANEL？"),
    (URL_703, "宮近海斗の私服チェックシャツはカーハートと判明！"),
]))

content = "\n\n".join(b)
plain = re.sub(r"<!--.*?-->|<[^>]+>", "", content, flags=re.S)
print("chars:", len(re.sub(r"\s", "", plain)), "title len:", len(TITLE))
(ROOT / "articles" / "chakaumi_harajuku_items_1017.html").write_text(content, encoding="utf-8")
if DRY:
    sys.exit()

payload = {"title": TITLE, "content": content, "status": "draft",
           "slug": "chakaumi-harajuku-sanpo-outfit-tomford", "categories": [3, 9, 10], "author": 2}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"], "status", post["status"], "SLUG", post["slug"], post["link"])

eye = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
     "--main", "原宿散歩",
     "--bottom", "ちゃかうみの私服は？", "--bottom", "トムフォードでお揃い！",
     "--color-key", "宮近海斗+中村海人", "--out", str(EYECATCH)],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
)
print(eye.stdout[-300:], eye.stderr[-300:])
if eye.returncode == 0:
    em = upload_media(EYECATCH)
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}", headers=HJSON,
                      data=json.dumps({"featured_media": em["id"], "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    print("EYECATCH", em["id"], r.json()["status"])
