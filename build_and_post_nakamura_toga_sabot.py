# -*- coding: utf-8 -*-
# chomoand-4.blog: 中村海人 放課後GAMING LIFE(2026-10-10 BOMBANANA!回 / 10-03 リズム天国回)の私服
# TOGA VIRILIS EYELET METAL SABOT + CHANEL カメリアビーニー再着用
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

IMG_DIR = ROOT / "frames_tmp" / "nakamura_toga_sabot"
EYECATCH = ROOT / "images" / "nakamura_toga_sabot_eyecatch.jpg"
VID_BOMB = "FafFiYjTjeU"
VID_RHYTHM = "1vmf-Cq5wjI"
SRC_BOMB = f"https://www.youtube.com/watch?v={VID_BOMB}"
SRC_RHYTHM = f"https://www.youtube.com/watch?v={VID_RHYTHM}"
DRY = "--dry" in sys.argv

TITLE = "【放課後GAMING】中村海人のサンダルはどこの？TOGAと判明！"

BORDER = "#c9ebdc"
ACCENT = "#5fbf9a"
BG = "#f1faf5"


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


def ytembed(vid, title):
    return wphtml(f'''<div style="position:relative;width:100%;padding-top:56.25%;margin:0 0 16px 0;">
<iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://www.youtube.com/embed/{vid}" title="{title}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>''')


MEDIA = {}


def img(key, alt, src):
    if DRY:
        return f"[[IMG {key}: {alt}]]"
    m = MEDIA[key]
    url = m["source_url"]
    w, h = m["media_details"]["width"], m["media_details"]["height"]
    sizes = m["media_details"].get("sizes", {})
    med = sizes.get("medium", {"source_url": url, "width": w})
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{url}" alt="{alt}" width="{w}" height="{h}"
  style="max-width:100%;height:auto;"
  srcset="{med["source_url"]} {med["width"]}w, {url} {w}w"
  sizes="(max-width: {w}px) 100vw, {w}px">
<figcaption style="font-size:0.8em;color:#888;">出典:{src}</figcaption>
</figure>''')


KEYS = ["scene", "sabot", "beanie"]
if not DRY:
    for k in KEYS:
        MEDIA[k] = upload_media(IMG_DIR / f"{k}.jpg")
        print("media", k, MEDIA[k]["id"])

URL_TOGA_MEN = "https://int.toga.jp/products/aj1066"
URL_TOGA_WOMEN = "https://int.toga.jp/products/aj1058"
URL_STACTILE = "https://stactile-kyoto.com/products/eyelet-metal-sabotmen"
URL_STUDIOUS = "https://studious.co.jp/shop/g/g125274001162/"
URL_HBX = "https://hbx.com/jp/men/brands/toga-virilis/eyelet-metal-sabot-black-1"
URL_MERCARI = "https://jp.mercari.com/search?keyword=TOGA%20%E3%83%A1%E3%82%BF%E3%83%AB%E3%82%B5%E3%83%9C"
URL_CHANEL_ART = "https://chomoand-4.blog/where-does-kaito-nakamuras-cas-729"
A = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
MARK = '<strong><span class="swl-marker mark_yellow">{}</span></strong>'

b = []
b.append(p([
    "2026年10月10日、YouTubeチャンネル「放課後GAMING LIFE」で、中村海人さん・神山智洋さん・長尾謙杜さんの3人による協力爆弾解除ゲーム「BOMBANANA!(ボンバナナ)」の回が公開されました。",
    "中村さんはこの回、緑のチェックシャツにCHANELのニット帽というラフな私服姿で登場しています。",
    "そして足元に合わせていたのが、銀の金具がびっしり付いた黒いサボサンダルでした。",
    "動画を拡大して確認したところ、このサンダルは" + MARK.format("TOGA(トーガ)の「EYELET METAL SABOT(アイレット メタル サボ)」") + "とみられます。",
    "この記事では、サンダルを特定した決め手と価格・購入先、あわせて着ていたニット帽、そして動画の内容をまとめます。",
]))
b.append(whatbox([
    "中村海人さんが「放課後GAMING LIFE」で履いていたサンダルのブランド",
    "TOGAのメンズ版・レディース版の違いと価格",
    "今から買える購入先",
    "同じ日に被っていたCHANELのニット帽",
    "BOMBANANA!回の動画の内容",
]))
b.append(minibox([
    ("着用動画", "「放課後GAMING LIFE」BOMBANANA!回(2026年10月10日公開)、リズム天国 ミラクルスターズ回(2026年10月3日公開)"),
    ("ブランド", "TOGA(メンズライン「TOGA VIRILIS」/レディースライン「TOGA PULLA」)"),
    ("アイテム", "EYELET METAL SABOT(アイレット メタル サボ)"),
    ("品番", "AJ1066(メンズ)/AJ1058(レディース)"),
    ("定価", "61,600円(税込)"),
]))
b.append(ytembed(VID_BOMB, "チームワーク完璧！と自信満々の3人がお猿さんになって爆弾解除【BOMBANANA!】"))

b.append(h2("中村海人のサンダルはTOGAの「メタル サボ」"))
b.append(p([
    "中村さんの足元がよく見えるのは、同じメンバーで撮影された10月3日公開の「リズム天国 ミラクルスターズ」回です。",
    "冒頭、3人がソファに並んで座るシーンで中村さんが足を組んでいて、サンダルの横側がはっきり映っていました。",
    "BOMBANANA!回でもテーブルの下に同じサンダルが映っていて、2本続けて同じ足元だったことが分かります。",
]))
b.append(img("sabot", "ソファで足を組む中村海人の足元。銀のバックルとコンチョ、ハトメが付いた黒いサボサンダル", SRC_RHYTHM))
b.append(h3("① 甲を留めるウエスタン調のバックル"))
b.append(p([
    "まず目に入るのが、甲のストラップに付いた大きな銀のバックルです。",
    "縁にギザギザの彫りが入ったウエスタン調のデザインで、これはTOGAのシューズやベルトに共通して使われている金具と同じ形でした。",
    "ストラップはバックルで長さを調整できるつくりになっています。",
]))
b.append(h3("② つま先のコンチョ・ハトメ・スタッズ"))
b.append(p([
    "つま先には、花のような模様の丸いコンチョと、小さな穴のあいたハトメ(アイレット)がランダムに並んでいます。",
    "さらにソールとの境目には、丸いスタッズが一列にぐるりと打たれていました。",
    "商品名の「EYELET METAL」はこのハトメと金具のことで、この配置が中村さんのサンダルと一致します。",
]))
b.append(h3("③ ギザギザのシャークソール"))
b.append(p([
    "決め手の3つ目は、のこぎりの刃のようにギザギザした厚底のソールです。",
    "TOGAではこれを「シャークソール」と呼んでいて、メタル サボの特徴のひとつになっています。",
    "かかとが開いたサボ型で、厚底のわりに脱ぎ履きしやすいのもポイントです。",
]))
b.append(p([
    "公式サイトの商品写真は" + A(URL_TOGA_MEN, "TOGA公式オンラインストア(メンズ)") + "で確認できます。",
    "見比べると、バックルの位置やコンチョの並び方まで中村さんのサンダルとそっくりですよ。",
]))

b.append(h2("メンズとレディースどっち？価格と購入先"))
b.append(p([
    "メタル サボは、メンズラインの「TOGA VIRILIS(トーガ ビリリース)」とレディースラインの「TOGA PULLA(トーガ プルラ)」の両方から出ています。",
    "見た目はほぼ同じで、違いはサイズ展開です。",
    "レディース(品番AJ1058)は36〜39(22.5〜24.5cm)、メンズ(品番AJ1066)は40〜46(約25〜31cm)まで展開されています。",
    "中村さんがどちらを履いているかは動画だけでは断定できませんが、サイズを考えるとメンズのTOGA VIRILIS版の可能性が高そうです。",
]))
b.append(table(["項目", "内容"], [
    ["ブランド", "TOGA VIRILIS(メンズ)/TOGA PULLA(レディース)"],
    ["商品名", "EYELET METAL SABOT"],
    ["品番", "AJ1066(メンズ)/AJ1058(レディース)"],
    ["カラー", "ブラック"],
    ["素材", "アッパー:牛革、ソール:合成ゴム、金具:合金"],
    ["ヒール", "2.5cm"],
    ["生産国", "ポルトガル"],
    ["定価", "61,600円(税込)"],
]))
b.append(p([
    "国内の定価はメンズ・レディースとも61,600円(税込)です。",
    "レディース版はセレクトショップのSTUDIOUSで同じ価格で販売されていましたが、全サイズ売り切れになっていました。",
    "メンズ版は京都のセレクトショップ「STACTILE KYOTO」に61,600円(税込)で掲載されていて、ここが今いちばん定価で手に入れやすい購入先です。",
]))
b.append(table(["購入先", "価格", "備考"], [
    [A(URL_STACTILE, "STACTILE KYOTO(メンズ)"), "61,600円(税込)", "サイズ40〜46"],
    [A(URL_STUDIOUS, "STUDIOUS(レディース)"), "61,600円(税込)", "全サイズ売り切れ"],
    [A(URL_TOGA_MEN, "TOGA公式 海外ストア(メンズ)"), "525ドル", "海外発送・関税別"],
    [A(URL_HBX, "HBX(メンズ)"), "79,695円(関税込)", "返品・交換不可"],
    [A(URL_MERCARI, "メルカリ"), "中古・個人出品", "状態とサイズを要確認"],
]))
b.append(p([
    "金具が多いぶん重さもあるので、できれば店頭で試し履きしてからのほうが安心です。",
    "フリマアプリで探すときは「TOGA メタルサボ」「TOGA サボ」で検索し、メンズかレディースかのサイズ表記をよく確認してくださいね。",
]))
b.append(p([
    "ちなみにTOGAは、デザイナーの古田泰子さんが1997年に東京で立ち上げたブランドです。",
    "ウエスタンの金具を使ったシューズやブーツが人気で、メタル サボもその代表的なアイテムのひとつになっています。",
]))

b.append(h2("ニット帽は前にも被っていたCHANELのカメリアビーニー"))
b.append(p([
    "BOMBANANA!回で中村さんが被っていた黒いニット帽は、" + A(URL_CHANEL_ART, "千賀健永さんのインスタライブに登場したときと同じCHANELのビーニー") + "とみられます。",
    "前回はライブ配信の映像で少し見えにくかったのですが、今回はゲーム中のワイプで正面から大きく映っていて、カメリア(椿)の形をした白い編み柄の真ん中に、CHANELのCCロゴが入っているのがはっきり分かりました。",
]))
b.append(img("beanie", "黒いニット帽の正面に、白いカメリア柄とCHANELのCCロゴが入っている中村海人のアップ", SRC_BOMB))
b.append(p([
    "このビーニーはCHANELの「Beanie Cashmere」(品番AAA748B19217NACWY)で、2023年秋冬のカシミヤ100%のアイテムです。",
    "ブティック取り扱い品のため公式オンラインでは価格が出ておらず、海外のリセールショップでは650〜850ドルほどで取引されています。",
    "千賀さんのインスタライブに続いての登場なので、秋冬のお気に入りなのかもしれませんね。",
]))

b.append(h2("そのほかのコーディネート"))
b.append(img("scene", "BOMBANANA!回のオープニングで、黒いニット帽に緑のチェックシャツを着た中村海人", SRC_BOMB))
b.append(p([
    "この日の中村さんは、ミントグリーンと黒のブロックチェックのシャツを羽織り、中にグレーのリブタンクトップを合わせていました。",
    "下は淡い色のワイドデニムで、足元のメタル サボが黒のアクセントになっています。",
    "シャツとタンクトップ、デニムはロゴなどの手がかりが映っておらず、ブランドは特定できませんでした。",
    "新しい情報が分かりしだい追記します。",
]))

b.append(h2("BOMBANANA!回はどんな動画？"))
b.append(p([
    "今回プレイした「BOMBANANA!」は、3人でしか遊べない協力型の爆弾解除ゲームです。",
    "プレイヤーは「見猿(見ざる)」「言わ猿(言わざる)」「聞か猿(聞かざる)」の3匹の猿になり、それぞれ違う情報を持った状態で、制限時間内に爆弾の解除を目指します。",
    "見猿だけが爆弾を見て操作でき、言わ猿は解除手順をジェスチャーでしか伝えられず、聞か猿はその間をつなぐ役割です。",
]))
b.append(p([
    "最初は中村さんが言わ猿、神山さんが見猿、長尾さんが聞か猿でスタート。",
    "しゃべれない中村さんが身ぶり手ぶりでケーブルの色を伝えようとするものの、なかなか伝わらずに苦戦する場面から始まります。",
    "途中で役割を入れ替えながら、レバーの上げ下げや数字の計算、ランプの色の組み合わせといった仕掛けを1つずつ攻略していきました。",
]))
b.append(p([
    "目標は全30ステージのうち10ステージクリアでしたが、結果はレベル6まで。",
    "それでも最後のステージは3人の息がぴったり合ってすんなりクリアでき、「これ詰めてたらレベル10は行けたかもしれない」と手応えを感じていました。",
    "締めでは「猿が可愛かった」という感想も飛び出し、3人のテンポのいい掛け合いが楽しめる回になっています。",
]))

b.append(summary([
    "中村海人さんが「放課後GAMING LIFE」で履いていたサンダルは、TOGAの「EYELET METAL SABOT」とみられる",
    "ウエスタン調のバックル、コンチョとハトメ、ギザギザのシャークソールが決め手",
    "メンズ(TOGA VIRILIS・AJ1066)とレディース(TOGA PULLA・AJ1058)があり、定価はどちらも61,600円(税込)",
    "メンズ版はSTACTILE KYOTOで定価購入でき、レディース版はSTUDIOUSで売り切れ",
    "ニット帽は千賀健永さんのインスタライブでも被っていたCHANELのカメリアビーニー",
]))
b.append(p([
    "ラフなチェックシャツに、CHANELのビーニーとTOGAのサボを合わせるあたりに、中村さんらしいこだわりを感じますね。",
    "これからも中村さんの私服が分かりしだい、このブログで紹介していきます。",
]))
b.append(linkbox([
    (URL_CHANEL_ART, "千賀健永の配信で中村海人が被ってたビーニーはCHANEL？"),
    ("https://chomoand-4.blog/is-kaito-nakamuras-private-clo-724", "中村海人の私服はAMIRI×クロムハーツ？Jリーグ開幕戦の一枚を分析"),
    ("https://chomoand-4.blog/where-is-kaito-nakamuras-black-1015", "中村海人の黒Tシャツはどこの？セリーヌのトリオンフと判明！"),
    ("https://chomoand-4.blog/is-kaito-nakamuras-chanel-bag-1020", "中村海人のシャネルバッグはソーブラックのマトラッセ？"),
]))

content = "\n\n".join(b)
plain = re.sub(r"<!--.*?-->|<[^>]+>|\[\[IMG.*?\]\]", "", content, flags=re.S)
print("chars:", len(re.sub(r"\s", "", plain)))
(ROOT / "articles" / "nakamura_toga_sabot.html").write_text(content, encoding="utf-8")
if DRY:
    sys.exit()

payload = {"title": TITLE, "content": content, "status": "draft",
           "slug": "nakamura-kaito-toga-metal-sabot", "categories": [3, 10], "author": 2}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"], "status", post["status"], "SLUG", post["slug"])

eye = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
     "--main", "中村海人",
     "--bottom", "放課後GAMINGのサンダルは", "--bottom", "TOGAと判明！",
     "--color-key", "中村海人", "--out", str(EYECATCH)],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
)
print(eye.stdout[-300:], eye.stderr[-300:])
if eye.returncode == 0:
    em = upload_media(EYECATCH)
    requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}", headers=HJSON,
                  data=json.dumps({"featured_media": em["id"], "status": "draft"}).encode("utf-8")).raise_for_status()
    print("eyecatch media", em["id"])
print("DONE")
