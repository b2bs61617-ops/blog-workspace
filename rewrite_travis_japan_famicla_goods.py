# -*- coding: utf-8 -*-
"""chomoand-0.com post 823 (Travis Japan ファミクラ新グッズ) を9/10発売・価格判明でリライト."""
import base64
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
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

POST_ID = 823
PURPLE = "#7e57c2"
PURPLE_BG = "#f5f2fb"
PURPLE_CELL = "#ece5f7"

ANNOUNCE_TWEET = "https://x.com/MerchCompany_jp/status/2094983655685079245"
MAKING_TWEET = "https://x.com/MerchCompany_jp/status/2088189132866769113"
STORE_DIARY = "https://famikura-store.jp/s/j/diary/detail/5799"

MAKING_IMG_SRC = "https://chomoand-0.com/wp-content/uploads/2026/08/travis_japan_famiclastore_ambassador_goods_making-1024x576.jpg"
MAKING_IMG_SRCSET = (
    "https://chomoand-0.com/wp-content/uploads/2026/08/travis_japan_famiclastore_ambassador_goods_making-500x281.jpg 500w, "
    "https://chomoand-0.com/wp-content/uploads/2026/08/travis_japan_famiclastore_ambassador_goods_making-1024x576.jpg 1024w, "
    "https://chomoand-0.com/wp-content/uploads/2026/08/travis_japan_famiclastore_ambassador_goods_making.jpg 1920w"
)

UA = {"User-Agent": "Mozilla/5.0"}


# ---------- image upload ----------
def upload_media(pbs_url: str, filename: str, alt: str) -> dict:
    data = requests.get(pbs_url, headers=UA, timeout=60).content
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={
            **HEADERS_AUTH,
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": "image/jpeg",
        },
        data=data,
    )
    r.raise_for_status()
    m = r.json()
    if alt:
        requests.post(
            f"{WP_URL}/wp-json/wp/v2/media/{m['id']}",
            headers={**HEADERS_AUTH, "Content-Type": "application/json"},
            data=json.dumps({"alt_text": alt}).encode("utf-8"),
        )
    return m


def figure_from_media(m: dict, alt: str, source_url: str) -> str:
    sizes = m.get("media_details", {}).get("sizes", {})
    full_url = m["source_url"]
    full_w = m["media_details"]["width"]
    full_h = m["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    img_w = large["width"]
    img_h = int(img_w * full_h / full_w)
    srcset = (
        f'{medium["source_url"]} {medium["width"]}w, '
        f'{large["source_url"]} {large["width"]}w, '
        f'{full_url} {full_w}w'
    )
    return wphtml(
        f'''<figure class="wp-block-image size-large">
<img src="{large["source_url"]}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="font-size:0.8em;color:#888;">出典:{source_url}</figcaption>
</figure>'''
    )


# ---------- block helpers ----------
def p(lines):
    body = "<br>\n".join(lines)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def line_box(title, rows):
    trs = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:{PURPLE_CELL};width:150px;"><strong>{k}</strong></td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(
        f'''<div style="border:1px solid {PURPLE};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>
<table style="border-collapse:collapse;width:100%;"><tbody>
{trs}
</tbody></table>
</div>'''
    )


def wakaru_box(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(
        f'''<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{PURPLE};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{PURPLE_BG};">
{lis}
</ul>
</div>'''
    )


def mini_box(rows):
    ps = "\n".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
        for i, (k, v) in enumerate(rows)
    )
    return wphtml(
        f'''<div style="border:1px solid #ddd;border-left:4px solid {PURPLE};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{PURPLE_BG};">
{ps}
</div>'''
    )


def reaction_box(category, quotes):
    lis = "\n".join(f"<li>「{q}」</li>" for q in quotes)
    return wphtml(
        f'''<div class="swell-block-capbox cap_box is-style-small_ttl">
<div class="cap_box_ttl">{category}</div>
<div class="cap_box_content">
<ul>{lis}</ul>
</div>
</div>'''
    )


def check_badge():
    return (
        f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {PURPLE};'
        f'border-radius:3px;color:{PURPLE};font-weight:bold;text-align:center;margin-right:6px;'
        f'font-size:0.85em;">&#10003;</span>'
    )


# ---------- eyecatch ----------
def build_eyecatch() -> Path:
    out = ROOT / "images" / "travis_japan_famicla_goods_eyecatch.png"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "eyecatch_chomoand0.py"),
            "--top", "Travis Japan",
            "--main", "シール帳・|クリアポーチ",
            "--bottom", "ファミクラ新グッズは",
            "--bottom", "9月10日発売！",
            "--color-key", "group",
            "--out", str(out),
        ],
        check=True,
    )
    return out


def upload_eyecatch(path: Path) -> dict:
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={
            **HEADERS_AUTH,
            "Content-Disposition": f'attachment; filename="{path.name}"',
            "Content-Type": "image/png",
        },
        data=path.read_bytes(),
    )
    r.raise_for_status()
    return r.json()


# ---------- content ----------
def build_content(reveal_fig: str, sticker_fig: str) -> str:
    b = []

    b.append(p([
        'Travis Japanが2026-2027年度「ファミクラストアアンバサダー」としてプロデュースした新グッズ「シール帳」「クリアポーチ」が、'
        f'<strong>2026年9月10日(木)</strong>にファミクラストア(店舗・オンライン)で発売されます。',
        'オンラインストアは同日10時からの販売で、価格は'
        '<strong>シール帳が1,500円、クリアポーチが1,300円(いずれも税込)</strong>です。',
    ]))
    b.append(p([
        '制作動画が公開された8月中旬の時点では「秋頃発売予定」としか案内されていませんでしたが、9月2日の公式発表で発売日・価格・デザインの全貌が一気に明らかになりました。',
        'ここでは2アイテムの仕様と「平成ポップ」なデザインの中身、メンバーがアイロンビーズでモチーフを手作りした制作の舞台裏、そして5代目アンバサダーとしてのTravis Japanの立ち位置までまとめて紹介します。',
    ]))

    b.append(line_box("新グッズ基本情報", [
        ("商品", "シール帳／クリアポーチ(アンバサダープロデュースグッズ)"),
        ("発売日", "2026年9月10日(木)　※オンラインは10:00〜"),
        ("価格", "シール帳 1,500円／クリアポーチ 1,300円(税込)"),
        ("販売場所", "ファミクラストア(店舗・オンライン)"),
        ("デザイン", "「平成ポップ」テーマ。アイロンビーズのモチーフをドット絵化"),
        ("アンバサダー", "2026-2027年度 ファミクラストアアンバサダー(5代目)"),
    ]))

    b.append(wakaru_box([
        "シール帳・クリアポーチの発売日・価格・仕様",
        "「平成ポップ」デザインの中身と付属ステッカーの内容",
        "アイロンビーズ制作のチーム編成と舞台裏",
        "ファミクラストアアンバサダーの歴代グループ",
    ]))

    # --- H2 1 ---
    b.append(h2("シール帳・クリアポーチはいつ発売？価格は？"))
    b.append(mini_box([
        ("発売日", "2026年9月10日(木)／オンラインは10:00〜"),
        ("価格", "シール帳 1,500円・クリアポーチ 1,300円(税込)"),
    ]))
    b.append(p([
        '9月2日にファミクラストア公式が新商品情報を発表し、発売日は<strong>9月10日(木)</strong>に決まりました。',
        '店舗は同日の営業開始から、オンラインストアは同日10時から購入できます。',
        '価格はシール帳が1,500円、クリアポーチが1,300円(いずれも税込)。',
        '制作動画が出た8月中旬は「秋頃販売開始予定」としか言われていなかったので、9月上旬スタートはファンの体感より少し早い到着になりました。',
    ]))
    b.append(p([
        'クリアポーチはWファスナータイプで、メインの収納とは別に外ポケットが付いた作りです。',
        '公式では外ポケットにミニフォトを入れる使い方が提案されていて、透明素材なのでトレカやアクリルスタンドを見せながら持ち歩けます。',
        'シール帳のほうは、付属のアンバサダーステッカーや手持ちのシールを自由に貼ってカスタマイズできる仕様。',
        'サイズや素材の細かい数値は発売時の商品ページで公開される見込みで、店頭で実物を確かめてから選びたいアイテムです。',
    ]))
    b.append(reveal_fig)

    # --- H2 2 ---
    b.append(h2("どんなデザイン？「平成ポップ」なドット絵モチーフ"))
    b.append(mini_box([
        ("テーマ", "平成ポップ／ドット絵(ピクセルアート)"),
        ("キーワード", "「TOGETHER with your HAPPINESS!」・方眼柄・ビションフリーゼ"),
    ]))
    b.append(p([
        'デザインは、メンバーが作ったアイロンビーズのモチーフを<strong>ドット絵(ピクセルアート)</strong>に落とし込んだ、1990〜2000年代の空気感がある「平成ポップ」なテイストです。',
        'ショッキングピンクを基調に、方眼ノート風の格子模様、ハート・星・虹・ダイヤ・ひまわり・"LIKE"ボタンといったドットアイコンがびっしり散りばめられています。',
        'アンバサダーのスローガン「TOGETHER with your HAPPINESS!」や「FAMILY CLUB. STORE」のロゴも、ピクセル調のフォントで配置されました。',
    ]))
    b.append(p([
        'シール帳にはステッカーがセットで付属します。',
        'ファミクラストアの公式キャラクターであるビションフリーゼ(白いモコモコの犬)のシールをはじめ、「OSAKA」「SHIBUYA」「NAGOYA」「FUKUOKA」など店舗のある街の名前をあしらったご当地風ステッカー、メンバーの集合写真をプリントしたフォトカード風シール、7人がカフェのカウンターに並んだアニメ風イラストのカードなどがラインナップ。',
        'リング式のバインダーになっていて、リフィルを足しながらアルバムのように育てていける中身になっています。',
    ]))
    b.append(sticker_fig)

    # --- H2 3 ---
    b.append(h2("メンバーがアイロンビーズでデザイン！制作の舞台裏"))
    b.append(mini_box([
        ("制作", "アイロンビーズ"),
        ("Aチーム", "川島如恵留・宮近海斗・中村海人・七五三掛龍也(4人)"),
        ("Bチーム", "松田元太・松倉海斗・吉澤閑也(3人)"),
    ]))
    b.append(p([
        'デザインのモチーフは、8月に公開された制作動画「2026-27｜アンバサダー プロデュースグッズ制作中！」でメンバーが童心に返って取り組んだアイロンビーズ作りから生まれました。',
        '7人は2チームに分かれて制作し、川島如恵留・宮近海斗・中村海人・七五三掛龍也のAチームがトークを楽しみながら順調に進める一方、松田元太・松倉海斗・吉澤閑也のBチームはハプニング続出のわちゃわちゃした空気に。',
        '色の指定はあってもモチーフの形は自由とのことで、ハート・ダイヤ・ひまわり・花冠風のモチーフなど、各自の個性が出た作品が並びました。',
        'Aチームでは七五三掛龍也がハート型を選び、周囲から「キャラに似合ってる」と声が飛ぶ場面もありました。',
    ]))
    b.append(p([
        'Bチームでは、せっかく組んだビーズがアイロンの熱でバラバラになるアクシデントも発生。',
        '作り直しになったメンバーに松倉海斗が手を貸し、ひまわりのモチーフを一緒に完成させる一幕もあって、メンバー同士の掛け合いがたっぷり詰まった動画になっています。',
        '合間には子どもの頃の手芸トークも広がり、吉澤閑也が5人きょうだいの末っ子だと明かすなど、グッズ制作をきっかけにした素顔のやり取りも見どころでした。',
    ]))
    b.append(wphtml(
        f'''<figure class="wp-block-image size-large">
<img src="{MAKING_IMG_SRC}" alt="Travis Japanがアイロンビーズでファミクラストアアンバサダーグッズのデザインを制作している告知画像" width="1024" height="576"
  style="max-width:100%;height:auto;"
  srcset="{MAKING_IMG_SRCSET}"
  sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption style="font-size:0.8em;color:#888;">出典:{MAKING_TWEET}</figcaption>
</figure>'''
    ))

    # --- H2 4 ---
    b.append(h2("Travis Japanは何代目？ファミクラストアアンバサダーとは"))
    b.append(mini_box([
        ("代目", "5代目(2026-2027年度)"),
        ("歴代アンバサダー", "Hey! Say! JUMP(2022年度)→Sexy Zone(2023年度)→WEST.(2024年度)→なにわ男子(2025年度)→Travis Japan(2026-2027年度)"),
    ]))
    b.append(p([
        'ファミクラストアは、STARTO ENTERTAINMENT所属タレントの公式グッズを扱う通販・実店舗サービスです。',
        '「ファミクラストアアンバサダー」は、1年間グループがブランドの顔となってプロデュースグッズの企画・販売や店舗装飾、YouTube企画などを担当する制度で、Travis Japanは歴代5組目にあたります。',
        '過去にはHey! Say! JUMP、Sexy Zone、WEST.、なにわ男子がアンバサダーを務め、いずれも1年を通じて複数回のグッズ展開を行ってきました。',
        'Travis Japanも今年度すでに、水彩風イラストの「Summer Sketch」シリーズ(ましかくフォト・ポストカード・ステッカー・アクリルスタンドなど)を夏に発売しており、今回のシール帳・クリアポーチはそれに続く秋の新展開という位置づけです。',
    ]))

    # --- H2 5 ---
    b.append(h2("SNSでの反応"))
    b.append(reaction_box("発売への期待", [
        "9/10まで待ちきれない",
        "オンライン10時、絶対張り付く",
    ]))
    b.append(reaction_box("デザインへの反応", [
        "平成ポップってテーマが刺さりすぎる",
        "ドット絵のアイコンが全部かわいい",
    ]))
    b.append(reaction_box("制作動画への反応", [
        "トラジャらしさ全開で癒された",
        "アイロンビーズ懐かしすぎる",
    ]))

    # --- まとめ ---
    b.append(h2("まとめ"))
    cb = check_badge()
    b.append(wphtml(
        f'''<div style="border:1px solid {PURPLE};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{PURPLE_BG};">
<ul style="margin:0;padding-left:0;list-style:none;">
<li style="margin:0 0 6px 0;">{cb}シール帳・クリアポーチは<strong>2026年9月10日(木)</strong>発売。オンラインは同日10時から</li>
<li style="margin:0 0 6px 0;">{cb}価格はシール帳<strong>1,500円</strong>・クリアポーチ<strong>1,300円</strong>(税込)</li>
<li style="margin:0 0 6px 0;">{cb}デザインは「平成ポップ」なドット絵。アイロンビーズのモチーフが元になっている</li>
<li style="margin:0 0 6px 0;">{cb}クリアポーチはWファスナー＋外ポケット、シール帳はステッカー付きでカスタム可能</li>
<li style="margin:0;">{cb}Travis Japanは歴代5組目のファミクラストアアンバサダー</li>
</ul>
</div>'''
    ))
    b.append(p([
        '格子柄やドットアイコンにピンとくる世代にはたまらない仕上がりなので、9月10日はオンラインの10時か店舗の開店直後を狙ってチェックしてみてください！',
    ]))

    b.append(wphtml(
        f'''<div style="border:1px solid {PURPLE};border-left:4px solid {PURPLE};border-radius:4px;padding:14px 18px;margin:16px 0 0 0;background:{PURPLE_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-0.com/why-did-torajas-member-colors-538">Travis Japanのメンバーカラーの由来・変更エピソードをまとめた記事</a></li>
<li><a href="https://chomoand-0.com/were-there-9-initial-members-o-330">Travis Japanの結成メンバー・脱退メンバーを整理した記事</a></li>
</ul>
</div>'''
    ))

    return "\n\n".join(b)


def get_slug(title_text):
    url = (
        "https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q="
        + urllib.parse.quote(title_text)
    )
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    en = "".join(seg[0] for seg in data[0])
    slug = re.sub(r"[^a-z0-9\s-]", "", en.lower())
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)[:40].rstrip("-")
    return slug


def main():
    title = "Travis Japanのシール帳・クリアポーチは9／10発売！"

    print("uploading reveal images...")
    reveal_m = upload_media(
        "https://pbs.twimg.com/media/HRGy1JgaQAA16SS.jpg?name=orig",
        "travis_japan_famicla_seal_pouch_reveal.jpg",
        "Travis Japanファミクラストアアンバサダーのシール帳とクリアポーチの商品画像",
    )
    sticker_m = upload_media(
        "https://pbs.twimg.com/media/HRGy0nGaEAAIJOi.jpg?name=orig",
        "travis_japan_famicla_seal_stickers.jpg",
        "シール帳に付属するステッカーとリング式バインダーの中面",
    )
    reveal_fig = figure_from_media(
        reveal_m,
        "Travis Japanファミクラストアアンバサダーのシール帳とクリアポーチ",
        ANNOUNCE_TWEET,
    )
    sticker_fig = figure_from_media(
        sticker_m,
        "シール帳の中面と付属ステッカー(ビションフリーゼ・ご当地ステッカーなど)",
        ANNOUNCE_TWEET,
    )

    print("building eyecatch...")
    eye_path = build_eyecatch()
    eye_m = upload_eyecatch(eye_path)
    print("eyecatch media id:", eye_m["id"])

    content = build_content(reveal_fig, sticker_fig)
    slug = get_slug(title)
    print("slug:", slug)

    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "featured_media": eye_m["id"],
    }
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print("POST_ID", post["id"])
    print("SLUG", post["slug"])
    print("STATUS", post["status"])
    print("PREVIEW", f"{WP_URL}/?p={post['id']}")


if __name__ == "__main__":
    main()
