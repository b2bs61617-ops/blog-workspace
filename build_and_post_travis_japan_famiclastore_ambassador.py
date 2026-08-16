# -*- coding: utf-8 -*-
import json, base64, os, re, urllib.request, urllib.parse
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
WP_URL = ENV["WP_AUDITION_URL"].rstrip("/")
WP_USER = ENV["WP_AUDITION_USERNAME"]
WP_PASS = ENV["WP_AUDITION_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

PURPLE = "#7e57c2"
PURPLE_BG = "#f5f2fb"

# ---------- STEP A: upload images to WP media library ----------
def upload_media(filepath: Path, filename: str, content_type: str):
    data = filepath.read_bytes()
    headers = {
        **HEADERS_AUTH,
        "Content-Type": content_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=data)
    r.raise_for_status()
    return r.json()


TWEET_IMG_PATH = ROOT / "tools" / "Xiy" / "posts_merchcompany_20260816" / "images" / "post_1_img_1.jpg"
TWEET_URL = "https://x.com/MerchCompany_jp/status/2088189132866769113"

tweet_media = upload_media(
    TWEET_IMG_PATH, "travis_japan_famiclastore_ambassador_goods_making.jpg", "image/jpeg"
)
print("tweet media id:", tweet_media["id"], tweet_media["source_url"])

eyecatch_path = ROOT / "images" / "travis_japan_famiclastore_ambassador_eyecatch.png"
eyecatch_media = upload_media(
    eyecatch_path, "travis_japan_famiclastore_ambassador_eyecatch.png", "image/png"
)
print("eyecatch media id:", eyecatch_media["id"])

sizes = tweet_media.get("media_details", {}).get("sizes", {})
full_url = tweet_media["source_url"]
full_w = tweet_media["media_details"]["width"]
full_h = tweet_media["media_details"]["height"]
large = sizes.get("large", {"source_url": full_url, "width": full_w})
medium = sizes.get("medium", {"source_url": full_url, "width": full_w})

img_src = large["source_url"]
img_w = large["width"]
img_h = int(img_w * full_h / full_w)

srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {full_w}w'

# ---------- STEP B: build content HTML ----------
title = "Travis Japanのファミクラ新グッズはいつ発売？"


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def hr():
    return '<!-- wp:separator --><hr class="wp-block-separator has-alpha-channel-opacity"/><!-- /wp:separator -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def info_box(ttl, rows):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;width:140px;"><strong>{k}</strong></td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {PURPLE};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{PURPLE_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{ttl}</p>
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>''')


def wakaru_box(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{PURPLE};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{PURPLE_BG};">
{lis}
</ul>
</div>''')


def mini_box(rows):
    ps = "\n".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
        for i, (k, v) in enumerate(rows)
    )
    return wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {PURPLE};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{PURPLE_BG};">
{ps}
</div>''')


def reaction_box(category, quotes):
    lis = "\n".join(f"<li>「{q}」</li>" for q in quotes)
    return wphtml(f'''<div class="swell-block-capbox cap_box is-style-small_ttl">
<div class="cap_box_ttl">{category}</div>
<div class="cap_box_content">
<ul>{lis}</ul>
</div>
</div>''')


def image_block(alt):
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="font-size:0.8em;color:#888;">出典:{TWEET_URL}</figcaption>
</figure>''')


blocks = []

blocks.append(p([
    "Travis Japanが、2026-2027年度の「ファミクラストアアンバサダー」としてプロデュースする新グッズの制作動画を公開しました。",
    "今回発表されたのは<strong>「クリアポーチ」</strong>と<strong>「シール帳」</strong>の2アイテムで、発売時期は<strong>2026年秋頃</strong>を予定しているとのことです。",
]))
blocks.append(p([
    "この記事では、メンバー自らアイロンビーズを使ってデザインを手作りした制作の裏側や、5代目アンバサダーとしてのTravis Japanの立ち位置まで詳しく紹介します。",
]))

blocks.append(info_box("新グッズ情報", [
    ("商品", "クリアポーチ・シール帳(アンバサダープロデュースグッズ)"),
    ("発売時期", "2026年秋頃予定"),
    ("販売場所", "ファミクラストア(店舗・オンライン)"),
    ("デザイン", "Travis Japanメンバーが手作りしたアイロンビーズのモチーフを使用"),
    ("アンバサダー", "2026-2027年度 ファミクラストアアンバサダー(5代目)"),
]))

blocks.append(wakaru_box([
    "新グッズ「クリアポーチ」「シール帳」の発売時期・企画意図",
    "アイロンビーズでのデザイン制作の舞台裏",
    "ファミクラストアアンバサダーとは何か・歴代アンバサダー",
]))

blocks.append(h2("新グッズ「クリアポーチ」「シール帳」はいつ発売？"))
blocks.append(mini_box([
    ("商品", "クリアポーチ・シール帳"),
    ("発売時期", "2026年秋頃予定"),
]))
blocks.append(p([
    "公開された動画は「2026-27｜アンバサダー プロデュースグッズ制作中！」と題されたもので、Travis Japanの7人が2チームに分かれてグッズのデザイン作りに挑む様子が収められています。",
    "グッズの選定理由について、メンバーは「シールには自分たちのステッカーを貼ってもいいし、他のアーティストのシールを集めたり交換したりしても楽しい」「クリアポーチは小物入れとして使いやすく、アクリルスタンドを入れるのにも良さそう」と説明していました。",
    "普段使いしやすいアイテムをファミクラストアアンバサダーとして選んだ形で、発売時期は動画の最後で改めて「秋頃に販売開始予定」と案内されています。",
    "価格やサイズなど具体的なスペックはまだ発表されておらず、公式からの続報を待つ必要があります。",
]))
blocks.append(image_block("Travis Japanがファミクラストアアンバサダープロデュースグッズを制作している告知画像"))

blocks.append(hr())

blocks.append(h2("メンバー自らアイロンビーズでデザイン制作！舞台裏を紹介"))
blocks.append(mini_box([
    ("制作アイテム", "アイロンビーズ"),
    ("作ったモチーフ", "ハート・ダイヤモンド・ひまわり・花冠 など"),
]))
blocks.append(p([
    "グッズに使われるデザインのモチーフは、メンバーが童心に返って取り組んだアイロンビーズ作りから生まれました。",
    "2チームに分かれての制作となり、動画の説明ではAチームがトークを楽しみながら順調に作業を進める一方、Bチームはハプニング続出のわちゃわちゃした展開になったと紹介されています。",
    "色の指定はあるもののモチーフの形は自由とのことで、ハートやダイヤモンド、ひまわり、花冠風のモチーフなど、メンバーそれぞれの個性が出た作品が並びました。",
    "なかでもハート型を選んだメンバーには「キャラに似合ってる」という声が上がる場面もあり、担当パートを決める過程そのものも和気あいあいとした雰囲気だったようです。",
]))
blocks.append(p([
    "Bチームでは、せっかく組み上げたビーズがアイロンの熱でバラバラになってしまうアクシデントも発生。",
    "作り直しになったメンバーにほかのメンバーが手を貸し、最終的にひまわりのモチーフを一緒に完成させる一幕もあり、制作を通してメンバー同士の掛け合いが存分に楽しめる内容になっていました。",
    "作業の合間には子どもの頃の手芸経験についてのトークも展開され、あるメンバーが5人兄弟の末っ子で妹がいないと話す場面など、グッズ制作をきっかけにした素顔のやり取りも垣間見えました。",
]))

blocks.append(hr())

blocks.append(h2("Travis Japanは何代目？ファミクラストアアンバサダーとは"))
blocks.append(mini_box([
    ("代目", "5代目(2026-2027年度)"),
    ("歴代アンバサダー", "Hey! Say! JUMP(2022年度)→Sexy Zone(2023年度)→WEST.(2024年度)→なにわ男子(2025年度)→Travis Japan(2026-2027年度)"),
]))
blocks.append(p([
    "ファミクラストアは、STARTO ENTERTAINMENT所属タレントの公式グッズを扱う通販・実店舗サービスです。",
    "「ファミクラストアアンバサダー」は、1年間にわたってグループがブランドの顔となり、プロデュースグッズの企画・販売や店舗装飾、YouTube企画などを担当する制度で、Travis Japanは歴代5組目のアンバサダーに就任しています。",
    "過去にはHey! Say! JUMP、Sexy Zone、WEST.、なにわ男子が歴代アンバサダーを務めており、いずれも1年を通じて複数回のグッズ展開が行われてきました。",
    "Travis Japanは今年度すでに、水彩風のイラストをあしらった「Summer Sketch」シリーズ(ましかくフォト・ポストカード・ステッカー・アクリルスタンドなど)を夏に発売済みで、今回発表されたクリアポーチ・シール帳はそれに続く秋の新展開という位置づけになります。",
]))

blocks.append(hr())

blocks.append(h2("SNSでの反応"))
blocks.append(reaction_box("発売への期待", [
    "秋頃の販売って楽しみすぎる",
    "終始楽しい動画で発売が楽しみです",
]))
blocks.append(reaction_box("グッズへの要望", [
    "シール帳助かるなー、ステッカーとかシールをまとめられたら嬉しい",
    "クリアポーチのサイズ感が気になる、ぬい入れられるサイズだと嬉しい",
]))
blocks.append(reaction_box("制作風景への反応", [
    "アイロンビーズ懐かしすぎた",
    "モチーフ作成にイライラしてたけどとっても可愛い仕上がりで嬉しい",
]))

blocks.append(hr())

blocks.append(h2("まとめ"))
blocks.append(wphtml(f'''<div style="border:1px solid {PURPLE};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{PURPLE_BG};">
<ul style="margin:0;padding-left:1.3em;">
<li>Travis Japanが2026-2027年度「ファミクラストアアンバサダー」としてプロデュースする新グッズ「<strong>クリアポーチ</strong>」「<strong>シール帳</strong>」の発売が決定</li>
<li>発売時期は<strong>2026年秋頃</strong>を予定。価格・詳細サイズなどは続報待ち</li>
<li>デザインのモチーフはメンバー自身がアイロンビーズで手作りしたもので、2チームに分かれての制作過程がYouTubeで公開された</li>
<li>Travis Japanは歴代5組目のアンバサダーで、既に夏の「Summer Sketch」シリーズが発売済み。今回の新グッズはそれに続く秋の展開</li>
</ul>
</div>'''))
blocks.append(p([
    "アンバサダーとしての活動はまだ始まったばかりで、これから秋にかけてさらに新しいグッズや企画が発表される可能性もあります。",
]))
blocks.append(p([
    "クリアポーチやシール帳は普段使いしやすいアイテムなので、発売のタイミングを逃さないよう公式の続報をこまめにチェックしておくのがおすすめです！",
]))

blocks.append(wphtml(f'''<div style="border:1px solid {PURPLE};border-left:4px solid {PURPLE};border-radius:4px;padding:14px 18px;margin:16px 0 0 0;background:{PURPLE_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-0.com/why-did-torajas-member-colors-538">Travis Japanのメンバーカラーの由来・変更エピソードを紹介した記事</a></li>
<li><a href="https://chomoand-0.com/were-there-9-initial-members-o-330">Travis Japanの結成メンバー・脱退メンバーをまとめた記事</a></li>
</ul>
</div>'''))

content = "\n\n".join(blocks)

# ---------- STEP C: slug ----------
def get_slug(title_text):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={urllib.parse.quote(title_text)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    en = "".join(seg[0] for seg in data[0])
    slug = re.sub(r"[^a-z0-9\s-]", "", en.lower())
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)[:30].rstrip("-")
    return slug


slug = get_slug(title)
print("slug:", slug)

# ---------- STEP D: create draft post ----------
payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": "draft",
    "categories": [3, 7],
    "author": 1,
    "featured_media": eyecatch_media["id"],
}
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"])
print("SLUG", post["slug"])
print("PREVIEW", f"{WP_URL}/?p={post['id']}")
