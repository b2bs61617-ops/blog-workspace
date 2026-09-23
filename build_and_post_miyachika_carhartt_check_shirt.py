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


FRAMES = ROOT / "frames_tmp" / "miyachika_carhartt_shirt2"

photo_2025_media = upload_media(
    FRAMES / "photo_2025_05.jpg",
    "miyachika_kaito_carhartt_shirt_2025_05.jpg",
    "image/jpeg",
)
print("photo_2025 media id:", photo_2025_media["id"], photo_2025_media["source_url"])

photo_2026_media = upload_media(
    FRAMES / "photo_2026_05.jpg",
    "miyachika_kaito_carhartt_shirt_2026_05.jpg",
    "image/jpeg",
)
print("photo_2026 media id:", photo_2026_media["id"], photo_2026_media["source_url"])

eyecatch_media = upload_media(
    ROOT / "images" / "miyachika_kaito_carhartt_shirt_eyecatch_chomoand0.png",
    "miyachika_kaito_carhartt_shirt_eyecatch.png",
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


photo2025_src, photo2025_w, photo2025_h, photo2025_srcset = img_urls(photo_2025_media)
photo2026_src, photo2026_w, photo2026_h, photo2026_srcset = img_urls(photo_2026_media)

# ---------- content builders ----------
title = "宮近海斗の私服チェックシャツはカーハートと判明！"

BORDER = "#f3d6d6"
ACCENT = "#ef9a9a"
BG = "#fdf3f3"


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
<figcaption style="font-size:0.8em;color:#888;">{caption}</figcaption>
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
    "Travis Japanの宮近海斗が、1年以上の間隔をあけた2枚の私服スナップで、同じチェック柄のシャツを着用している姿が確認できます。",
    "調べてみたところ、このシャツは<strong><span class=\"swl-marker mark_pink\" style=\"font-size:1.15em;\">ワークウェアブランド「Carhartt(カーハート)」のチェック柄フランネルシャツ(参考価格22,000円相当)</span></strong>とみられることが分かりました。",
    "この記事では、2枚の着用シーンとあわせて、シャツの特徴やブランドの背景を詳しく紹介します。",
]))
blocks.append(whatbox([
    "2枚の私服スナップに写っていた着用シーン",
    "シャツのブランド・価格帯",
    "生地・柄の特徴",
    "Carharttというブランドについて",
]))

blocks.append(h2("1年越しで確認された同じチェックシャツ"))
blocks.append(minibox([
    ("1枚目", "2025年5月ごろ撮影とみられる私服姿。ビーニー帽・メガネ・ゴールドネックレスを合わせたセルフィー"),
    ("2枚目", "2026年5月ごろ撮影とみられる場面。ピンマイクを着けた「J」キャップ姿で、白Tシャツの上に同じシャツを羽織っている"),
    ("共通点", "黒・グレー・白を基調にしたチェック柄の長袖シャツ"),
]))
blocks.append(p([
    "2枚の写真は撮影時期がおよそ1年離れているにもかかわらず、同じ黒×グレー×白のチェック柄シャツが確認できます。",
    "1枚目はプライベート感の強いセルフィーで、シャツの前を開けてゴールドのネックレスをのぞかせるスタイリング。",
    "2枚目はコンサートやイベントの合間とみられるオフショットで、白Tシャツの上に同じシャツを羽織って着崩しています。",
    "1着を長く着回している様子がうかがえ、私服としてお気に入りのアイテムであることがうかがえます。",
]))
blocks.append(image_block(
    photo2025_src, photo2025_w, photo2025_h, photo2025_srcset,
    "宮近海斗が私服で着用していたチェック柄シャツ(2025年5月ごろ)",
    "本人私服スナップ(2025年5月ごろ撮影とみられる)",
))
blocks.append(image_block(
    photo2026_src, photo2026_w, photo2026_h, photo2026_srcset,
    "宮近海斗が私服で着用していたチェック柄シャツ(2026年5月ごろ)",
    "本人私服スナップ(2026年5月ごろ撮影とみられる)",
))

blocks.append(h2("シャツは「Carhartt」のチェック柄フランネルと判明"))
blocks.append(minibox([
    ("ブランド", "Carhartt(カーハート)"),
    ("参考価格", "22,000円相当"),
    ("柄", "黒・グレー・白を基調にしたチェック柄"),
    ("素材感", "厚手のフランネル生地とみられる"),
]))
blocks.append(p([
    "生地の織り方や色の組み合わせから、アメリカのワークウェアブランド「Carhartt」、もしくはそのヨーロッパ発ストリートライン「Carhartt WIP(ワーク・イン・プログレス)」のチェック柄フランネルシャツとみられます。",
    "Carhartt(WIP)のシャツはシーズンごとにチェック柄の名称やカラー展開が変わる定番アイテムで、長袖のチェックシャツは19,800円〜24,200円ほどの価格帯で展開されることが多く、22,000円という価格帯とも矛盾しません。",
    "現時点では販売シーズンが古く、公式サイト上で同一デザインの品番までは特定できていませんが、黒・グレー・白のモノトーン配色は同ブランドのチェックシャツによく見られる定番カラーです。",
]))

blocks.append(h3("Carhartt(WIP)はどんなブランド?"))
blocks.append(p([
    "Carharttは1889年にアメリカ・デトロイトで創業したワークウェアブランドです。",
    "そのヨーロッパライセンスとして1994年にドイツで誕生したのが「Carhartt WIP」で、本家譲りのタフな作業服のDNAを受け継ぎながら、スケートボードカルチャーやヨーロッパのストリートファッションと融合させたデザインを展開しているのが特徴です。",
    "現在では欧米のセレクトショップで定番として扱われる人気ブランドに成長しており、日本国内でも複数のセレクトショップが正規取り扱いをしています。",
]))

blocks.append(h2("価格・購入先"))
blocks.append(table([
    ("ブランド", "Carhartt(カーハート)/ Carhartt WIP"),
    ("参考価格", "22,000円相当(Carhartt WIPの長袖チェックシャツは19,800円〜24,200円ほどの価格帯が中心)"),
    ("購入先", "Carhartt WIP公式オンラインストア、正規取扱のセレクトショップなど"),
]))
blocks.append(p([
    "チェック柄のシャツはシーズンごとに新柄が登場する人気アイテムのため、気になる方は公式オンラインストアや正規取扱店で最新のカラー展開・在庫状況をチェックしてみてください。",
]))

blocks.append(h2("まとめ"))
blocks.append(checklist([
    "宮近海斗は2025年5月・2026年5月と、1年越しで同じチェック柄シャツを私服で愛用",
    "シャツはCarhartt(WIP)のチェック柄フランネルとみられ、参考価格は22,000円相当",
    "黒・グレー・白を基調にしたモノトーン配色で、セルフィーからオフショットまで幅広く着回し",
    "Carhartt WIPは1994年にドイツで生まれた、本家Carharttのヨーロッパ発ストリートブランド",
]))
blocks.append(p([
    "1年以上前のスナップと最近のオフショットで同じ1着を着回しているあたり、宮近海斗が本当に気に入って愛用しているアイテムであることがうかがえます。",
    "気になった方は、宮近と同じCarhartt(WIP)のチェック柄シャツをチェックしてみてはいかがでしょうか!",
]))
blocks.append(linkbox("宮近海斗の私物特定記事", [
    '<a href="https://chomoand-0.com/where-does-kaito-miyachika-get-279" target="_blank" rel="noopener">帽子・Tシャツ・スニーカーのブランドを特定</a>',
    '<a href="https://chomoand-0.com/what-brand-is-kaito-miyachikas-casual-t-355" target="_blank" rel="noopener">私服Tシャツ(sacai×インターステラー)を特定</a>',
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
