# -*- coding: utf-8 -*-
# chomoand-4.blog: ちゃかうみ原宿散歩(公式YouTube 2026-10-17)のロケ地・食べたもの・買った靴まとめ(2026-10-18)
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

IMG_DIR = ROOT / "images" / "chakaumi_harajuku_1017"
EYECATCH = ROOT / "images" / "chakaumi_harajuku_1017_eyecatch_canva.jpg"
DRY = "--dry" in sys.argv

TITLE = "【原宿散歩】宮近海斗と中村海人のロケ地は？食べ物・靴も特定！"

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


def gmap(q):
    from urllib.parse import quote
    return wphtml(f'<iframe src="https://maps.google.com/maps?q={quote(q)}&t=&z=16&ie=UTF8&iwloc=&output=embed" '
                  'width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>')


from urllib.parse import quote

A = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
M = lambda t: f'<strong><span class="swl-marker mark_pink">{t}</span></strong>'

YT = "https://www.youtube.com/watch?v=fxDMIN2JK0c"
CAP = A(YT, "Travis Japan公式YouTube「【原宿散歩】ほぼプライベート！ちゃかうみでお散歩♬」")
URL_NIKE = "https://www.nike.com/jp/t/" + quote("ナイキ-ムーン-シュー-og-メンズシューズ-7GU8trtm")
URL_BONDI = "https://www.fashionsnap.com/article/2026-01-30/bondi-7-reprint/"
URL_SC_PR = "https://adv.tokyo-np.co.jp/prtimes/article127827/"
URL_PV = "https://www.hotpepper.jp/strJ003532334/"
URL_SURURI = "https://chomoand-4.blog/miyachika-sururi-where-to-buy-supermarket-1403"
URL_GENTA = "https://chomoand-4.blog/when-does-genta-meshi-soda-rel-132"
URL_TV = "https://chomoand-4.blog/travis-japan-tv-schedule-1018-1024-1545"
URL_744 = "https://chomoand-4.blog/what-is-kaito-miyachikas-birth-744"

IMGS = {
    "takeshita": ("takeshita.jpg", "竹下通りを歩く中村海人と宮近海斗"),
    "le_shiner": ("le_shiner.jpg", "レ・シャイナーの10円パン「原宿レインボーチーズ」を持つ中村海人"),
    "fountain": ("fountain.jpg", "噴水のある小道をのぞきこむ中村海人と宮近海斗"),
    "beetle": ("beetle.jpg", "大衆食堂BEETLEの看板"),
    "abcmart": ("abcmart.jpg", "ABC-MART グランドステージ原宿の外観"),
    "nike": ("nike_moon.jpg", "中村海人がマネージャーに選んだナイキ ムーン シュー OG"),
    "hoka": ("hoka_bondi7.jpg", "宮近海斗がマネージャーに選んだHOKA ボンダイ7"),
    "churros": ("churros_truck.jpg", "STREET CHURROS原宿のキッチンカーでチュリンを注文する2人"),
    "sururi": ("sururi.jpg", "宮近海斗がアンバサダーを務める「するり」の話をする2人"),
    "pastavola": ("pastavola.jpg", "PASTAVOLA外苑前店の前に着いた中村海人と宮近海斗"),
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
    "Travis Japanの公式YouTubeで2026年10月17日に公開された「【原宿散歩】ほぼプライベート！ちゃかうみでお散歩♬」。",
    "宮近海斗さんと中村海人さんの「ちゃかうみ」コンビが、竹下通りからたらこパスタのお店まで、タクシーを使わずに歩いた回です。",
]))
b.append(p([
    "動画を止めながら確かめてみると、" + M("食べたのはレ・シャイナーの10円パンとSTREET CHURROSのチュリン") + "でした。",
    "マネージャーさんへのプレゼントとして" + M("ナイキ ムーン シュー OGとHOKA ボンダイ7") + "を買い、ゴールは外苑前の生パスタ店「PASTAVOLA」です。",
    "この記事では、歩いたルートの順番、寄ったお店の場所、買った靴の値段まで、まとめて紹介します。",
]))
b.append(whatbox(["歩いたルートと寄った場所", "食べたもの・飲んだもの", "マネージャーさんに買った靴と値段", "ゴールのたらこパスタのお店"]))

# ---- ルート一覧 ----
b.append(h2("ちゃかうみの原宿散歩ルートを一覧で"))
b.append(p([
    "まずは、動画に出てきた場所を順番に並べてみます。",
    "時間は動画の再生位置のだいたいの目安です。",
]))
b.append(table(["動画の時間", "場所", "したこと"], [
    ["0:00〜", "竹下通り(スタート)", "平日の人の多さにびっくり"],
    ["2:20〜", "レ・シャイナー", "10円パン「原宿レインボーチーズ」を食べる"],
    ["4:50ごろ", "マリオンクレープ", "前を通ってクレープの話"],
    ["6:20〜", "噴水のある小道(ブラームスの小径とみられる)", "噴水をのぞきこむ"],
    ["7:10ごろ", "大衆食堂BEETLE", "趣のある看板を見つける"],
    ["9:10〜", "ABC-MART グランドステージ原宿", "マネージャーさんへの靴を買う"],
    ["11:50〜", "STREET CHURROS 原宿", "中村さんのおごりでチュリン"],
    ["17:30〜", "原宿の交差点〜ウラハラ", "街の変化や高田馬場の思い出話"],
    ["22:00ごろ", "PASTAVOLA 外苑前店(ゴール)", "たらこパスタ店めぐりの1軒目に到着"],
]))
b.append(p([
    "竹下通りから明治通りを渡り、裏原宿を抜けて外苑前まで歩くルートでした。",
    "地図にすると、原宿駅前から青山方面へ2kmほど歩いたことになります。",
]))

# ---- 竹下通り ----
b.append(h2("スタートは平日の竹下通り"))
b.append(minibox([
    ("場所", "竹下通り(東京都渋谷区神宮前1丁目)"),
    ("企画", "宮近さんの「たらこパスタ店めぐり」の1軒目まで歩く"),
]))
b.append(img("takeshita"))
b.append(p([
    "スタート地点は原宿駅前の竹下通りです。",
    "撮影日は平日だったそうですが、通りは人でいっぱいで、2人とも「平日でもこんなに混んでるの？」と驚いていました。",
    "竹下通りを歩くのはかなり久しぶりのようで、昔はアクセサリーのお店が多かったのに、今は食べ歩きのお店が増えたと話しています。",
]))
b.append(p([
    "今回の企画は、宮近さんが以前から話していた「たらこパスタのお店をめぐりたい」という願いをかなえるものです。",
    "ただし条件は「歩いて行くこと」。",
    "途中で食べたいものがあれば寄ってOKというルールで、ゆるい散歩が始まりました。",
]))

# ---- 10円パン ----
b.append(h2("食べたもの①レ・シャイナーの10円パン"))
b.append(minibox([
    ("お店", "LE SHINER(レ・シャイナー)"),
    ("食べたもの", "10円パン「原宿レインボーチーズ」"),
    ("住所", "東京都渋谷区神宮前1-7-10 COXY176ビル1階"),
]))
b.append(p([
    "最初に寄ったのは、竹下通りにあるレ・シャイナーです。",
    "10円玉の形をしたチーズ入りのパンケーキ「10円パン」を見つけて、「10円って書いてある」と足を止めました。",
    "もちろん値段が10円なのではなく、10円玉の形をしているのが名前の由来です。",
]))
b.append(img("le_shiner"))
b.append(p([
    "2人が選んだのは、チーズがよく伸びると聞いた「原宿レインボーチーズ」。",
    "生地はホットケーキのような甘い香りなのに、食べてみると少ししょっぱめで、中のチーズはモッツァレラ系のあっさりした味だったそうです。",
    "残念ながらチーズはあまり伸びませんでしたが、2人とも「普通にうまい」「正直に美味しい」と気に入っていました。",
]))
b.append(p([
    "画面には「特別に許可をいただいて撮影しています。通常は店先での飲食禁止です」という注意書きが出ていました。",
    "お店の前では食べられないので、同じものを食べに行く人は気をつけてください。",
    "10円パンの値段は、動画の中でも、調べた範囲でも分かりませんでした。",
    "行く前にお店のInstagramなどで確認しておくと安心です。",
]))
b.append(p([
    "レ・シャイナーは、虹色のチーズトーストやレインボーサンドで知られるお店です。",
    "中のチーズにはモッツァレラがたっぷり使われていると紹介されていて、2人の「モッツァレラ系」という感想とも合っています。",
]))
b.append(gmap("LE SHINER 東京都渋谷区神宮前1-7-10"))

# ---- マリオン〜噴水〜BEETLE ----
b.append(h2("マリオンクレープと噴水のある小道"))
b.append(minibox([
    ("通った場所", "マリオンクレープ竹下通り店、噴水のある小道、大衆食堂BEETLE"),
    ("噴水の場所", "竹下通りと並行する「ブラームスの小径」とみられる"),
]))
b.append(p([
    "竹下通りを進むと、行列のできるマリオンクレープの前を通りました。",
    "「マリオンクレープってすごいのよ。俺大好き」という声が出るほどで、お店がリニューアルしてきれいになったことにも気づいていました。",
    "Travis Japanの吉澤閑也さんと七五三掛龍也さんが、お仕事体験の番組でクレープを作っていたという話もしています。",
]))
b.append(h3("噴水はブラームスの小径とみられる"))
b.append(p([
    "竹下通りから1本中に入ると、人の多さがうそのように静かな道になります。",
    "「こういうので落ち着くのは、おじさんになったのかも」と笑いながら歩いた先にあったのが、レンガの広場と噴水です。",
]))
b.append(img("fountain"))
b.append(p([
    "竹下通りと並んで走る細い路地「ブラームスの小径」には噴水があり、レンガの道とヨーロッパ風の街灯が特徴です。",
    "動画に映る噴水・レンガ敷き・壁の街灯がこの小径の雰囲気とよく合うことから、ここで撮った可能性が高いと考えられます。",
    "2人は「コインを入れたら願い事がかなうかも」と噴水をのぞきこんでいましたが、コインは入っていませんでした。",
]))
b.append(gmap("ブラームスの小径 東京都渋谷区神宮前1-15-14"))
b.append(h3("大衆食堂BEETLEの看板も"))
b.append(img("beetle"))
b.append(p([
    "さらに裏道を歩くと、手書きの「2F 大衆食堂 BEETLE」という看板が映ります。",
    "画面には「心くすぐる趣のあるお店!!」というテロップが出ましたが、今回はお店には入っていません。",
    "BEETLEはラフォーレ原宿の裏手のビルの2階にある大衆食堂で、ランチの定食が人気だと紹介されています。",
    "原宿で落ち着いて定食を食べたいときの候補になりそうです。",
]))

# ---- 靴 ----
b.append(h2("買ったもの：マネージャーさんへのプレゼントの靴"))
b.append(minibox([
    ("お店", "ABC-MART グランドステージ原宿(東京都渋谷区神宮前1-9-18)"),
    ("中村海人", "ナイキ ムーン シュー OG"),
    ("宮近海斗", "HOKA ボンダイ7"),
]))
b.append(p([
    "散歩の途中で、いつもお世話になっているマネージャーさんの話になりました。",
    "現場でずっと動き回っているせいで、1年ほどで靴のかかとに穴が開いてしまうことがあるそうです。",
    "「靴をプレゼントしてあげたい」という話になり、2人がそれぞれ1足ずつ選んで、どちらのセンスがいいか勝負することになりました。",
]))
b.append(img("abcmart"))
b.append(p([
    "向かったのは、明治通り沿いにあるABC-MARTの旗艦店「グランドステージ原宿」です。",
    "2人は30分ほどかけて、本気で選んだと話していました。",
]))
b.append(gmap("ABC-MART グランドステージ原宿 東京都渋谷区神宮前1-9-18"))

b.append(h3("中村海人が選んだのはナイキ ムーン シュー OG"))
b.append(img("nike"))
b.append(p([
    "中村さんが選んだのは、画面に「NIKE / ムーン シュー OG」と出たナイキのスニーカーです。",
    "黒いナイロンのアッパーに白いスウッシュの1足で、選んだ理由は次の3つでした。",
]))
b.append(wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.3em;">
<li>毎日走り回るマネージャーさんのために、軽さを重視した</li>
<li>もともと柔らかいので、すぐに足になじみそう</li>
<li>サッカー好きのマネージャーさんに合う、スパイクのようなデザイン</li>
</ul>
</div>'''))
b.append(p([
    "ムーン シューは、1970年代のランニングシューズを今の形で復刻したモデルです。",
    "ナイキ公式サイトでは、ナイロンとレザーを組み合わせたアッパーに、ワッフル柄のラバーソールと説明されています。",
    "重さは27cmで片足約207gと軽く、「軽さ」を一番の理由にした中村さんの選び方にぴったりです。",
]))
b.append(p([
    "黒のカラーは、公式サイトにある「ブラック/ブラック/セーフティオレンジ/セイル(IX3952-001)」とみられます。",
    "ベロのあたりにオレンジっぽい色が少し見えるので、この色の可能性が高そうです。",
]))
b.append(h3("宮近海斗が選んだのはHOKA ボンダイ7"))
b.append(img("hoka"))
b.append(p([
    "宮近さんが選んだのは、画面に「HOKA / BONDI 7」と出たHOKAの厚底シューズです。",
    "「最近流行ってるよね」と言いながら、足を疲れにくくしてくれるリカバリー系の靴として選んだそうです。",
    "厚いのにとても軽いところも決め手になりました。",
]))
b.append(p([
    "ボンダイはHOKAの中でもクッションがいちばん厚いシリーズとして知られています。",
    "ボンダイ7は2026年1月30日に復刻され、HOKAの直営店や公式オンラインストア、一部のお店で売られています。",
    "復刻版は全10色で、価格は23,100円です。",
]))
b.append(p([
    "中村さんは前からマネージャーさんに「靴を買ってあげるね」と約束していたそうです。",
    "そこに宮近さんからも1足届くとは思わないだろう、と普段の宮近さんを「ドケチ」といじる場面もあり、2人の仲の良さが伝わってきました。",
]))
b.append(h3("2足の値段と買える場所"))
b.append(table(["選んだ人", "商品", "参考価格(税込)", "買える場所"], [
    ["中村海人", "ナイキ ムーン シュー OG", "15,730円", A(URL_NIKE, "ナイキ公式オンラインストア")],
    ["宮近海斗", "HOKA ボンダイ7(復刻版)", "23,100円", "HOKA直営店・公式オンラインストア(" + A(URL_BONDI, "発売の記事") + ")"],
]))
b.append(p([
    "どちらもABC-MART グランドステージ原宿で買っていますが、店頭の在庫は色やサイズによって変わります。",
    "同じものがほしい人は、公式オンラインストアもあわせて確認してみてください。",
]))

# ---- チュロス ----
b.append(h2("食べたもの②STREET CHURROSのチュリン"))
b.append(minibox([
    ("お店", "STREET CHURROS 原宿(ラフォーレ原宿1F駐車場横のキッチンカー)"),
    ("食べたもの", "チュリン(600円、原宿店限定)"),
    ("住所", "東京都渋谷区神宮前1-11-6"),
]))
b.append(p([
    "靴を買ったあとは、中村さんのおごりでチュロス休憩です。",
    "寄ったのは、韓国生まれのチュロス専門店「STREET CHURROS」の原宿店で、ラフォーレ原宿の駐車場横にキッチンカーで出店しています。",
]))
b.append(img("churros"))
b.append(p([
    "注文したのは、メニューに「原宿店限定商品」と書かれた「チュリン」(600円)です。",
    "一口サイズのミニチュロスを専用の袋に入れ、好みの味と一緒に振って食べるメニューで、食べ歩きにも向いています。",
    "揚げたてのチュロスは「サクッとしてもちもち」で、2人とも「これ好きな人多いと思う」と大満足でした。",
]))
b.append(p([
    "壁には定番の「オリジナル」が450円と書かれたポスターも貼ってありました。",
    "お店は2026年3月1日にオープンしたばかりで、営業時間は11時から20時です。",
    "ラフォーレ原宿のすぐ横なので、原宿で買い物をするついでに寄りやすい場所にあります。",
]))
b.append(gmap("ラフォーレ原宿 東京都渋谷区神宮前1-11-6"))
b.append(h3("中村海人がついに「するり」を飲んだ話"))
b.append(img("sururi"))
b.append(p([
    "チュロスを食べながら、中村さんが「やっとするり飲んだで」と話す場面もありました。",
    "「するり」は宮近さんがブランドアンバサダーを務める、宝酒造の無炭酸チューハイです。",
    "メンバーが関わっている商品なので気になっていたそうで、「うまかった」と感想を伝えていました。",
]))
b.append(p([
    "さらに、松田元太さんの「元太めし」も食べたそうで、「メンバーのものがコンビニにあると思うと、コンビニ探しが楽しくなる」と話しています。",
    "するりの売っている場所は" + f'<a href="{URL_SURURI}">宮近海斗CMのするりを買えるお店の記事</a>' + "、元太めしは"
    + f'<a href="{URL_GENTA}">元太めし 元太ソーダ味を買える場所の記事</a>' + "にまとめています。",
]))

# ---- 街の話 ----
b.append(h2("原宿の変化と高田馬場の思い出話"))
b.append(minibox([
    ("通った場所", "明治通りの交差点まわり、ウラハラ(裏原宿)"),
    ("思い出の地", "東京・高田馬場"),
]))
b.append(p([
    "チュロスのあとは、明治通りを渡って裏原宿へ向かいます。",
    "「前は古着屋だったのに、こんな大きなモニターができてる」「ドン・キホーテの交差点のほうも工事中」と、街の変わりように驚く2人。",
    "地元の人気の焼き鳥屋さんが駅前の新しい建物に移った話など、原宿散歩とは思えないしみじみとしたトークになりました。",
]))
b.append(p([
    "画面に「トリプルカイト思い出の地」と出たのが、東京・高田馬場です。",
    "高校が高田馬場だったという話から、放課後にラーメンを食べに行ったことや、定食屋さんの大きなチキンカツの思い出が出てきました。",
    "「思い出の場所に3人で行くのもおもしろそう」と、松倉海斗さんも入れた3人での企画を提案していました。",
]))
b.append(p([
    "裏原宿では、ハンバーガーと定食のお店「トニーズ」に中村さんが目をとめる場面もありました。",
    "ただ、目的地はあくまでたらこパスタのお店なので、ここは通り過ぎています。",
    "道中では「ひと口ちょうだい」をやんわり断る宮近さん、というテロップが出るやりとりもありました。",
]))

# ---- ゴール ----
b.append(h2("ゴールのたらこパスタ店は外苑前「PASTAVOLA」"))
b.append(minibox([
    ("お店", "PASTAVOLA(パスターヴォラ)外苑前店"),
    ("住所", "東京都港区南青山2-12-16"),
    ("アクセス", "東京メトロ銀座線 外苑前駅4a出口から徒歩2分"),
]))
b.append(img("pastavola"))
b.append(p([
    "原宿から歩き続けて着いたゴールは、外苑前の生パスタ店「PASTAVOLA」です。",
    "お店の前の看板には「PASTAVOLA」の文字と、もちもちの生パスタの写真が並んでいました。",
    "画面には「たらこパスタ店めぐり 記念すべき第一号店に到着!」というテロップが出ています。",
]))
b.append(p([
    "テロップによると、1軒目は王道ではなく「創作系」のたらこパスタのお店です。",
    "看板を見た2人は「生パスタもちもち系じゃん」「うにといかと明太子だって」と大喜びでした。",
    "次回予告では、うにといかと明太子のパスタと、えびのパスタが並ぶカウンターの様子が流れています。",
]))
b.append(p([
    "PASTAVOLAは、太めでもちもちの生パスタが看板のお店です。",
    "外苑前店の営業時間は、月〜土曜の11時〜14時30分と17時30分〜21時30分で、日曜はお休みです。",
    "生パスタは約20種類あり、価格は1,540円からとなっています(" + A(URL_PV, "ホットペッパーグルメ") + "より)。",
    "2人が食べたパスタの値段や味は、次回の動画で分かりそうです。",
]))
b.append(gmap("パスターヴォラ 外苑前店 東京都港区南青山2-12-16"))
b.append(p([
    "ちなみに、散歩の最後に2人は「誰にもバレてないかも」と笑っていました。",
    "帽子とサングラス、ニット帽とメガネという姿で、原宿の人ごみにすっかりなじんでいたようです。",
]))

# ---- まとめ ----
b.append(h2("まとめ"))
b.append(summary([
    "ルート：竹下通り→ブラームスの小径(とみられる)→ABC-MART→ラフォーレ原宿横→裏原宿→外苑前",
    "食べたもの：レ・シャイナーの10円パン「原宿レインボーチーズ」、STREET CHURROSのチュリン(600円)",
    "買ったもの：中村はナイキ ムーン シュー OG(15,730円)、宮近はHOKA ボンダイ7(23,100円)",
    "ゴール：外苑前の生パスタ店「PASTAVOLA」で、うに・いか・明太子のパスタ",
]))
b.append(p([
    "竹下通りから外苑前まで、食べ歩きと買い物をしながらのんびり歩いた今回の散歩。",
    "同じルートを歩けば、ちゃかうみと同じ10円パンやチュリンを味わえます。",
    "次回のたらこパスタ編もあわせて、原宿から青山までの聖地巡礼を楽しんでみてはいかがでしょうか！",
]))
b.append(linkbox([
    (URL_SURURI, "宮近海斗CMのするりはどこで買える？10/13からスーパーでも！"),
    (URL_GENTA, "【発売中】元太めし 元太ソーダ味はどこで買える？"),
    (URL_744, "宮近海斗の誕生日プレゼントは？千賀健永から贈られたLVビーニーと判明！"),
    (URL_TV, "トラジャのテレビ出演は？10/18〜10/24の放送予定まとめ！"),
]))

content = "\n\n".join(b)
plain = re.sub(r"<!--.*?-->|<[^>]+>", "", content, flags=re.S)
print("chars:", len(re.sub(r"\s", "", plain)), "title len:", len(TITLE))
(ROOT / "articles" / "chakaumi_harajuku_sanpo_1017.html").write_text(content, encoding="utf-8")
if DRY:
    sys.exit()

payload = {"title": TITLE, "content": content, "status": "draft",
           "slug": "chakaumi-harajuku-sanpo-location", "categories": [3, 9, 10], "author": 2}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"], "status", post["status"], "SLUG", post["slug"], post["link"])

eye = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
     "--main", "原宿散歩",
     "--bottom", "ちゃかうみのロケ地は？", "--bottom", "食べ物・買った靴も特定！",
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
