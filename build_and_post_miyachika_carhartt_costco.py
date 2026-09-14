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


FRAMES = ROOT / "frames_tmp" / "miyachika_carhartt"

scene_media = upload_media(
    FRAMES / "hires_578.jpg",
    "miyachika_kaito_carhartt_costco_scene.jpg",
    "image/jpeg",
)
print("scene media id:", scene_media["id"], scene_media["source_url"])

closeup_media = upload_media(
    FRAMES / "crop_back_hi.jpg",
    "miyachika_kaito_carhartt_costco_closeup.jpg",
    "image/jpeg",
)
print("closeup media id:", closeup_media["id"], closeup_media["source_url"])

product_media = upload_media(
    FRAMES / "product_front.jpg",
    "miyachika_kaito_carhartt_spirals_product.jpg",
    "image/jpeg",
)
print("product media id:", product_media["id"], product_media["source_url"])

eyecatch_media = upload_media(
    ROOT / "images" / "miyachika_kaito_carhartt_costco_eyecatch.png",
    "miyachika_kaito_carhartt_costco_eyecatch.png",
    "image/png",
)
print("eyecatch media id:", eyecatch_media["id"])


def img_urls(media):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    full_w = media["media_details"]["width"]
    full_h = media["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    img_src = large["source_url"]
    img_w = large["width"]
    img_h = int(img_w * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {full_w}w'
    return img_src, img_w, img_h, srcset


scene_src, scene_w, scene_h, scene_srcset = img_urls(scene_media)
closeup_src, closeup_w, closeup_h, closeup_srcset = img_urls(closeup_media)
product_src, product_w, product_h, product_srcset = img_urls(product_media)

# ---------- content builders ----------
title = "宮近海斗がコストコで着てたTシャツはCarhartt WIPと判明！"

BORDER = "#f3d6d6"
ACCENT = "#ef9a9a"
BG = "#fdf3f3"

YT_SRC = "Travis Japan公式YouTube「Travis Japan【コストコ】食材爆買いでTJパーティーしようぜ！～買い物編～」"


def p(text_sentences, extra_class=""):
    body = "<br>\n".join(text_sentences)
    cls = f' class="{extra_class}"' if extra_class else ""
    return f"<!-- wp:paragraph -->\n<p{cls}>{body}</p>\n<!-- /wp:paragraph -->"


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
        for i, (k, v) in enumerate(rows)
    )
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{lines}
</div>''')


def linkbox(title, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


def image_block(src, w, h, srcset, alt, caption):
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{src}" alt="{alt}" width="{w}" height="{h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {w}px) 100vw, {w}px">
<figcaption style="font-size:0.8em;color:#888;">出典:{caption}</figcaption>
</figure>''')


def table(rows):
    trs = "\n".join(
        f'<tr><td style="border:1px solid #ccc;background:#f0f0f0;padding:10px 12px;width:30%;"><strong>{k}</strong></td><td style="border:1px solid #ccc;padding:10px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return f'<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n{trs}\n</tbody></table></figure>\n<!-- /wp:table -->'


def checklist(items):
    lis = "\n".join(
        f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {ACCENT};border-radius:3px;color:{ACCENT};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{i}</p>'
        for i in items
    )
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{lis}
</div>''')


blocks = []

blocks.append(p([
    "Travis Japanの宮近海斗が、コストコでの買い出しに密着した公式YouTube動画に、私服のTシャツ姿で登場しました。",
    "調べてみたところ、このTシャツは<strong><span class=\"swl-marker mark_pink\" style=\"font-size:1.15em;\">ストリートブランド「Carhartt WIP(カーハート ダブルアイピー)」の「S/S Spirals T-Shirt」(参考価格9,900円)</span></strong>であることが分かりました。",
    "この記事では、動画に映った着用シーンとあわせて、Tシャツのデザインの特徴やブランドの背景を詳しく紹介します。",
]))
blocks.append(whatbox([
    "着用していた動画の内容",
    "Tシャツのブランド・商品名・価格",
    "バックプリントのデザインの特徴",
    "Carhartt WIPというブランドについて",
]))

blocks.append(h2("宮近海斗が私服Tシャツを着ていたのはどんな動画?"))
blocks.append(minibox([
    ("動画", "Travis Japan公式YouTube「【コストコ】食材爆買いでTJパーティーしようぜ！～買い物編～」"),
    ("公開日", "2026年9月12日"),
    ("出演", "宮近海斗(ちゃか)・松倉海斗(まちゅ)・吉澤閑也(しず)の3人チーム"),
    ("場面", "鮮魚コーナー(KIRKLAND SEAFOODコーナー)前で惣菜を選んでいたシーン"),
]))
blocks.append(p([
    "2026年9月12日に公開された動画は、Travis Japanの7人が3チームに分かれてコストコで食材を「爆買い」し、後日キッチンスタジオでパーティーを開くという企画です。",
    "宮近海斗は松倉海斗・吉澤閑也とともに「ちゃか・まちゅ・しず」チームとして参加しており、惣菜コーナーで商品を選んでいた場面で、宮近が着ていた白Tシャツの背中のデザインがはっきりと映り込んでいました。",
    "オレンジ〜赤のグラデーションで描かれた渦巻き状のロゴが、白Tシャツの背面によく映えています。",
]))
blocks.append(image_block(
    scene_src, scene_w, scene_h, scene_srcset,
    "宮近海斗がコストコのKIRKLAND SEAFOODコーナー前で私服のTシャツを着用している様子",
    YT_SRC,
))

blocks.append(h2("Tシャツは「Carhartt WIP」の「S/S Spirals T-Shirt」と判明"))
blocks.append(minibox([
    ("ブランド", "Carhartt WIP(カーハート ダブルアイピー)"),
    ("商品名", "S/S Spirals T-Shirt"),
    ("参考価格", "9,900円(税込)"),
    ("素材", "オーガニックコットン100%"),
    ("カラー", "ホワイト(このほかブラックなどの展開あり)"),
]))
blocks.append(p([
    "背中のプリントを拡大して確認したところ、渦を巻くように配置された文字の中心に、アンモナイトを思わせる螺旋のグラフィックがあしらわれていることが分かりました。",
    "この螺旋のデザインは、Carhartt WIPの代表的なグラフィックシリーズ「Spirals」のものと特徴が一致しており、商品名は<strong>「S/S Spirals T-Shirt」</strong>、参考価格は9,900円(税込)です。",
    "生地にはオーガニックコットン100%のミディアムウェイトジャージーが使われ、ゆったりとしたルーズフィットシルエットに仕上げられているのも特徴です。",
]))
blocks.append(image_block(
    closeup_src, closeup_w, closeup_h, closeup_srcset,
    "宮近海斗が着用していたTシャツの背中のクローズアップ。渦巻き状のグラフィックとオレンジ〜赤のグラデーション文字が確認できる",
    YT_SRC,
))
blocks.append(p([
    "実際の商品写真と見比べると、渦巻きの中心から放射状に広がる螺旋のライン、そしてそれを囲むように配置された「CARHARTT WORKWEAR PROGRESS 1989」の文字の書体・配置が完全に一致します。",
    "宮近が着ていたのは背中いっぱいに大きくロゴを配置したホワイトカラーで、シンプルな無地のフロントに対してバックのグラフィックを主役にしたデザインバランスが特徴的です。",
]))
blocks.append(image_block(
    product_src, product_w, product_h, product_srcset,
    "Carhartt WIP「S/S Spirals T-Shirt」の商品写真(バック)。渦巻き状のグラフィックとブランドロゴが確認できる",
    "Carhartt WIP取扱店の商品写真",
))

blocks.append(h3("Carhartt WIPはどんなブランド?"))
blocks.append(p([
    "Carhartt WIP(ワーク・イン・プログレス)は、1889年にアメリカ・デトロイトで創業したワークウェアブランド「Carhartt」のヨーロッパライセンスとして、1994年にドイツで誕生したストリートブランドです。",
    "本家譲りのタフな作業服のDNAを受け継ぎながら、スケートボードカルチャーやヨーロッパのストリートファッションと融合させたデザインを展開しているのが特徴です。",
    "現在では欧米のセレクトショップで定番として扱われる人気ブランドに成長しており、日本国内でも複数のセレクトショップが正規取り扱いをしています。",
]))

blocks.append(h2("価格・購入先"))
blocks.append(table([
    ("ブランド", "Carhartt WIP(カーハート ダブルアイピー)"),
    ("商品名", "S/S Spirals T-Shirt"),
    ("参考価格", "9,900円(税込)"),
    ("購入先", "Carhartt WIP公式オンラインストア、正規取扱のセレクトショップなど"),
]))
blocks.append(p([
    "2026年9月時点でシーズン内の商品とみられ、公式オンラインストアや正規取扱店での入手を狙いやすいアイテムです。",
    "気になる方は、Carhartt WIPの店舗やオンラインストアでカラー展開・在庫状況をチェックしてみてください。",
]))

blocks.append(h2("まとめ"))
blocks.append(checklist([
    "宮近海斗が着ていたTシャツはCarhartt WIPの「S/S Spirals T-Shirt」(参考価格9,900円)",
    "話題になったのは2026年9月12日公開のTravis Japan公式YouTube「【コストコ】食材爆買いでTJパーティーしようぜ！～買い物編～」",
    "背中いっぱいに配置された渦巻き状のグラフィックが特徴で、商品写真とロゴの書体・配置が完全に一致",
    "Carhartt WIPは1994年にドイツで生まれた、本家Carharttのヨーロッパ発ストリートブランド",
]))
blocks.append(p([
    "買い出しという何気ない1コマからも私服がチェックされてしまうあたり、宮近海斗への注目度の高さがうかがえます。",
    "気になった方は、宮近と同じCarhartt WIPの「S/S Spirals T-Shirt」をチェックしてみてはいかがでしょうか!",
]))
blocks.append(linkbox("宮近海斗の私物特定記事", [
    '<a href="https://chomoand-0.com/where-does-kaito-miyachika-get-279" target="_blank" rel="noopener">帽子・Tシャツ・スニーカーのブランドを特定</a>',
    '<a href="https://chomoand-0.com/what-brand-is-kaito-miyachikas-casual-t-355" target="_blank" rel="noopener">私服Tシャツ(sacai×インターステラー)を特定</a>',
    '<a href="https://chomoand-0.com/is-kaito-miyachikas-casual-t-s-522" target="_blank" rel="noopener">私服Tシャツ(リーバイス×スカイハイファーム)を特定</a>',
    '<a href="https://chomoand-0.com/what-brand-of-sneakers-is-kait-459" target="_blank" rel="noopener">新曲PVで履いていたスニーカーのブランドを調査</a>',
]))

content = "\n\n".join(blocks)

# ---------- slug ----------
def get_slug(title):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={urllib.parse.quote(title)}"
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

# ---------- create new draft ----------
payload = {
    "title": title,
    "content": content,
    "status": "draft",
    "slug": slug,
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
