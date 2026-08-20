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


SCRATCH = Path(
    r"C:\Users\s30se\AppData\Local\Temp\claude\c--Users-s30se-OneDrive--------CHOMO\c1cebd12-aef5-4bdb-8efe-c17c8cc5945c\scratchpad\miyachika_cap"
)

group_media = upload_media(
    SCRATCH / "group5.jpg",
    "miyachika_kaito_kismyft2_senga_travis_5nin.jpg",
    "image/jpeg",
)
print("group media id:", group_media["id"], group_media["source_url"])

closeup_media = upload_media(
    SCRATCH / "closeup.jpg",
    "miyachika_kaito_newera_atmos_cap_closeup.jpg",
    "image/jpeg",
)
print("closeup media id:", closeup_media["id"], closeup_media["source_url"])

product_media = upload_media(
    SCRATCH / "product.jpg",
    "miyachika_kaito_newera_atmos_cap_product.jpg",
    "image/jpeg",
)
print("product media id:", product_media["id"], product_media["source_url"])

eyecatch_media = upload_media(
    ROOT / "images" / "miyachika_kaito_newera_atmos_cap_eyecatch.png",
    "miyachika_kaito_newera_atmos_cap_eyecatch.png",
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


group_src, group_w, group_h, group_srcset = img_urls(group_media)
closeup_src, closeup_w, closeup_h, closeup_srcset = img_urls(closeup_media)
product_src, product_w, product_h, product_srcset = img_urls(product_media)

# ---------- content builders ----------
title = "【キストラ】宮近海斗がかぶってた帽子はNEW ERA×atmos?"

BORDER = "#f3d6d6"
ACCENT = "#ef9a9a"
BG = "#fdf3f3"


def p(text_sentences, extra_class=""):
    body = "<br>\n".join(text_sentences)
    cls = f' class="{extra_class}"' if extra_class else ""
    return f"<!-- wp:paragraph -->\n<p{cls}>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


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


blocks = []

blocks.append(p([
    "Travis Japanの宮近海斗が、Kis-My-Ft2の千賀健永ら5人で写った1枚が2026年8月19日にXで話題になりました。",
    "写真の中で宮近海斗がかぶっていた帽子は、<strong>NEW ERA×atmosのコラボ9FIFTYスナップバック(参考価格¥7,150)</strong>で、atmosの創業25周年を記念したモデルと特定されています。",
    "この記事では帽子のブランド・デザインの特徴に加え、5人が一緒に写っていた経緯についても詳しく紹介します。",
]))
blocks.append(whatbox([
    "帽子のブランドと価格",
    "25周年記念モデルのデザインの特徴",
    "宮近海斗と千賀健永らが集まっていた理由",
]))

blocks.append(h2("宮近海斗の帽子はNEW ERA×atmosの25周年記念モデル"))
blocks.append(minibox([
    ("ブランド", "NEW ERA×atmos"),
    ("モデル", "9FIFTY スナップバック"),
    ("参考価格", "¥7,150(帽子・記念ピンバッジ・バンダナのセット)"),
]))
blocks.append(p([
    "気になって調べてみたところ、宮近海斗がかぶっていた帽子は<strong><span class=\"swl-marker mark_pink\" style=\"font-size:1.15em;\">NEW ERA×atmosのコラボモデル「9FIFTY スナップバック」</span></strong>であることが分かりました。",
    "atmosはスニーカー・ストリートウェアを扱う人気セレクトショップで、2000年の創業から数えて2025年で25周年を迎えたことを記念して、NEW ERAとのコラボキャップが2025年秋冬(25fw)シーズンに展開されました。",
    "参考価格は¥7,150となっていますが、単なるキャップ単体ではなく、25周年の記念ピンバッジとオリジナルバンダナがセットになった仕様で、この価格帯はコラボアイテムとしてはお手頃な部類に入ります。",
]))
blocks.append(image_block(
    product_src, product_w, product_h, product_srcset,
    "NEW ERA×atmos 9FIFTYスナップバックの商品写真。生成りのクラウンに黒のブリム、atmosロゴの刺繍と25周年記念ピンバッジが確認できる",
    "https://x.com/06150922_/status/2090180599806128577",
))
blocks.append(p([
    "商品写真を見ると、生成り(アイボリー)のクラウンに黒のブリムを組み合わせたツートンカラーが特徴です。",
    "フロントには黒で縁取られたatmosのオリジナルロゴが立体的な刺繍で施され、サイド部分には定番のNEW ERAフラッグロゴがさりげなく添えられています。",
    "帽体は9FIFTYというシルエットで、フラッグシップモデルである59FIFTYと同じ型ながら、後ろのスナップバックでサイズ調整ができる扱いやすいタイプです。",
]))

blocks.append(h2("宮近海斗と千賀健永らが集まっていたのはなぜ?"))
blocks.append(minibox([
    ("きっかけ", "『音楽の日2026』DREAMダンス企画「楽園ベイベー」"),
    ("メンバー", "千賀健永(Kis-My-Ft2)・宮近海斗・中村海人・七五三掛龍也・松倉海斗(Travis Japan)"),
]))
blocks.append(p([
    "5人が集まっていた背景をたどると、2026年7月18日放送の『音楽の日2026』にたどり着きます。",
    "この日はSTARTO ENTERTAINMENT選抜チームとして、Kis-My-Ft2の千賀健永とTravis Japanの宮近海斗・中村海人・七五三掛龍也・松倉海斗の5人が、DREAMダンス企画でRIP SLYMEの「楽園ベイベー」を披露しました。",
    "放送後もファンの間では「#超楽園ベイベー」のハッシュタグで盛り上がりが続いており、5人のグループ間の交流にも注目が集まっていました。",
]))
blocks.append(image_block(
    group_src, group_w, group_h, group_srcset,
    "千賀健永・宮近海斗・中村海人・七五三掛龍也・松倉海斗の5人が並んで写った写真。宮近海斗はNEW ERA×atmosのキャップとサングラスを着用",
    "https://x.com/senga_beautych/status/2090048402805633230",
))
blocks.append(p([
    "そして2026年8月19日、千賀健永の公式YouTubeチャンネルのXアカウントから、この5人が「完全プライベートで束の間の夏休みを過ごした」ことが明かされました。",
    "同じ投稿では、当時のことや『音楽の日』の裏話を語るトーク動画を収録予定であることも告知されており、今後の配信が楽しみなファンも多いようです。",
    "冒頭で紹介した写真は、この夏休みの集まりの中で撮られた1枚だったというわけです。",
]))

blocks.append(h2("私物かどうかについて"))
blocks.append(p([
    "今回の帽子は、番組収録やロケなどの公式な場ではなく、完全プライベートの集まりで身につけられていたものです。",
    "そのため、スタイリストが用意した衣装ではなく本人の私物である可能性が高いとみられますが、宮近海斗自身がブランドを公表したわけではない点には留意が必要です。",
    "画像を細かく見比べたファンによって、ロゴの形や配色からNEW ERA×atmosのコラボモデルとほぼ一致すると特定されました。",
]))

blocks.append(h2("まとめ"))
blocks.append(wphtml('''<ul>
<li>宮近海斗がかぶっていた帽子はNEW ERA×atmosのコラボ「9FIFTY スナップバック」(参考価格¥7,150)</li>
<li>atmosの創業25周年を記念した2025年秋冬(25fw)モデルで、記念ピンバッジとバンダナがセットになっている</li>
<li>生成りのクラウン×黒のブリムに、atmosロゴの立体刺繍が施されたデザイン</li>
<li>写真は『音楽の日2026』のDREAMダンス企画「楽園ベイベー」で共演した千賀健永・中村海人・七五三掛龍也・松倉海斗との、プライベートな集まりで撮影されたもの</li>
</ul>'''))
blocks.append(p([
    "グループの垣根を越えた5人の仲の良さが伝わってくる1枚に、思わずほっこりしたファンも多かったのではないでしょうか。",
    "気になる人はぜひ、宮近海斗と同じNEW ERA×atmosの25周年記念キャップをチェックしてみてください!",
]))
blocks.append(linkbox("宮近海斗の私物特定記事", [
    '<a href="https://chomoand-0.com/where-does-kaito-miyachika-get-279" target="_blank" rel="noopener">帽子・Tシャツ・スニーカーのブランドを特定</a>',
    '<a href="https://chomoand-0.com/what-brand-is-kaito-miyachikas-casual-t-355" target="_blank" rel="noopener">私服Tシャツ(sacai×インターステラー)を特定</a>',
    '<a href="https://chomoand-0.com/what-brand-of-sneakers-is-kait-459" target="_blank" rel="noopener">新曲PVで履いていたスニーカーのブランドを調査</a>',
    '<a href="https://chomoand-0.com/what-brand-of-glasses-does-kai-286" target="_blank" rel="noopener">メガネブランドをRay-Banと特定</a>',
    '<a href="https://chomoand-0.com/is-kaito-miyachikas-casual-t-s-522" target="_blank" rel="noopener">私服Tシャツ(リーバイス×スカイハイファーム)を特定</a>',
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
