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
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
WP_USER = ENV["WP_KOIKEYS_USERNAME"]
WP_PASS = ENV["WP_KOIKEYS_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

SOURCE_OFFICIAL = "https://x.com/KO1KEYZofficial/status/2090038569876545590"
SOURCE_FACE = "https://x.com/G_YUKI_FACE/status/2090076439425241137"

IMG_DIR1 = ROOT / "tools" / "Xiy" / "posts_goto_yui_enoshima_1" / "images"
IMG_DIR2 = ROOT / "tools" / "Xiy" / "posts_goto_yui_enoshima_2" / "images"

IMG_OFFICIAL_PATH = IMG_DIR1 / "post_1_img_1.jpg"
IMG2_PATH = IMG_DIR2 / "post_1_img_2.jpg"
IMG3_PATH = IMG_DIR2 / "post_1_img_3.jpg"
IMG4_PATH = IMG_DIR2 / "post_1_img_4.jpg"
IMG5_PATH = IMG_DIR2 / "post_1_img_5.jpg"
IMG6_PATH = IMG_DIR2 / "post_1_img_6.jpg"

EYECATCH_PATH = ROOT / "images" / "goto_yuki_enoshima_eyecatch.png"


def upload_media_from_file(path: Path, filename: str, content_type="image/jpeg"):
    img_bytes = path.read_bytes()
    headers = {
        **HEADERS_AUTH,
        "Content-Type": content_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=img_bytes)
    r.raise_for_status()
    return r.json()


EXISTING_MEDIA_IDS = {
    "official": 11543,
    "img2": 11544,
    "img3": 11545,
    "img4": 11546,
    "img5": 11547,
    "img6": 11548,
}

def get_or_upload(key, path, filename, content_type="image/jpeg"):
    if key in EXISTING_MEDIA_IDS:
        return requests.get(f"{WP_URL}/wp-json/wp/v2/media/{EXISTING_MEDIA_IDS[key]}", headers=HEADERS_AUTH).json()
    print("uploading", key, "...")
    return upload_media_from_file(path, filename, content_type)


img_official_media = get_or_upload("official", IMG_OFFICIAL_PATH, "goto_yuki_koinote_enoshima.jpg")
img2_media = get_or_upload("img2", IMG2_PATH, "goto_yuki_enosui_deck1.jpg")
img3_media = get_or_upload("img3", IMG3_PATH, "goto_yuki_enosui_deck2.jpg")
img4_media = get_or_upload("img4", IMG4_PATH, "goto_yuki_enosui_deck3.jpg")
img5_media = get_or_upload("img5", IMG5_PATH, "goto_yuki_enoshima_night1.jpg")
img6_media = get_or_upload("img6", IMG6_PATH, "goto_yuki_enoshima_night2.jpg")
print("uploaded media ids:", img_official_media["id"], img2_media["id"], img3_media["id"], img4_media["id"], img5_media["id"], img6_media["id"])


def build_img_html(media, alt, source_url):
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
    return f'''<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">出典:{source_url}</figcaption>
</figure>'''


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


img_official_html = wphtml(build_img_html(img_official_media, "YUKI(後藤結)のコイノート更新写真、背景に江ノ島とみられる島影が写る", SOURCE_OFFICIAL))
img2_html = wphtml(build_img_html(img2_media, "木製デッキと赤い手すりの通路、奥に江ノ島が見える景色", SOURCE_FACE))
img3_html = wphtml(build_img_html(img3_media, "海沿いのデッキから見える砂浜と江ノ島方面の景色", SOURCE_FACE))
img4_html = wphtml(build_img_html(img4_media, "施設内の木製通路、奥に建物と青空が広がる景色", SOURCE_FACE))
img5_html = wphtml(build_img_html(img5_media, "夜、ヤシの木と駐車場を背景にしたYUKI、奥に青くライトアップされたタワーが見える", SOURCE_FACE))
img6_html = wphtml(build_img_html(img6_media, "夜、旧車を背景にしたYUKI、奥に同じ青いタワーが見える", SOURCE_FACE))


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def capbox(ttl, rows):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ddd9d3;padding:8px 12px;background:#f7f6f4;white-space:nowrap;">{k}</td>'
        f'<td style="border:1px solid #ddd9d3;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:6px;overflow:hidden;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<div style="padding:14px 18px;background:#f7f6f4;">
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>
</div>''')


def minibox(html_inner):
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f6f4;">
{html_inner}
</div>''')


def wakaru_box(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:#f7f6f4;">
{lis}
</ul>
</div>''')


# KO1KEYZ記事共通のウォームグレー(メンバーカラーと被らせない、YUKIのメンバーカラーは紫のため特に注意)
ACCENT = "#8a8378"

title = "YUKI(後藤結)のコイノート写真の場所は?えのすいと判明!"

blocks = []

blocks.append(p([
    "KO1KEYZのYUKI(後藤結)が2026年8月19日に更新した公式ファンクラブコンテンツ「KO1NOTE(コイノート)」の写真について、背景に写る景色から撮影場所を調べてみました。",
    "写真には海と島影、そして白いタワーのようなものが写り込んでおり、これが<strong>神奈川県藤沢市の江ノ島、それも新江ノ島水族館(えのすい)</strong>である可能性が高いことが分かりました。",
    "この記事では、写真から読み取れる根拠や、あわせて話題になっている「新しい家族」ことカワウソについても紹介します。",
]))

blocks.append(capbox("コイノート更新情報", [
    ("更新日", "2026年8月19日"),
    ("担当メンバー", "YUKI(後藤結)"),
    ("内容", "写真とコメントの更新"),
    ("掲載先", "KO1KEYZ公式サイト内「KO1NOTE」"),
]))

blocks.append(wakaru_box([
    "コイノートに写った写真の背景の正体",
    "撮影場所が新江ノ島水族館(えのすい)とみられる根拠",
    "話題の「新しい家族」ことカワウソについて",
]))

blocks.append(h2("コイノートで公開された写真をチェック"))
blocks.append(minibox('<p style="margin:0;"><strong>更新内容:</strong>2026年8月19日、YUKIが「KO1LYこんにちは!YUKIです!」というコメントとともに複数枚の写真を公開</p>'))
blocks.append(img_official_html)
blocks.append(p([
    "公開された写真の1枚には、New Eraの黒いキャップをかぶり、大きなバッグを肩にかけたYUKIの姿が写っています。",
    "後ろに広がる海と、その向こうに浮かぶ緑豊かな島影、島の上に立つ白いタワーのようなシルエットが印象的な1枚です。",
    "この投稿には早速反応が集まり、「水族館行きたくなっちゃった笑笑」「えのすい行ったんかな〜近いから行ってみるね」「えのすい行ったのねそれを一枚目にするのもほんと可愛い」といったコメントが寄せられていました。",
    "「えのすい」は新江ノ島水族館の通称で、地元・神奈川県周辺のファンの間ではおなじみの呼び方です。",
]))

blocks.append(h2("写真の背景に写る島とタワーの正体は?"))
blocks.append(minibox('<p style="margin:0;"><strong>背景の正体(推定):</strong>神奈川県藤沢市の「江ノ島」、島の上に立つ白いタワーは展望灯台「江の島シーキャンドル」とみられる</p>'))
blocks.append(p([
    "写真の背景をよく見てみると、海に浮かぶ島の輪郭と、その頂上付近に立つ白くほっそりとしたタワーが確認できます。",
    "この島の形とタワーの位置関係は、神奈川県藤沢市にある観光名所「江ノ島」、そして島内のサムエル・コッキング苑にある展望灯台「江の島シーキャンドル」の見た目の特徴と一致しています。",
    "江ノ島は湘南エリアを代表する観光スポットで、島全体の緑に囲まれるようにそびえるシーキャンドルの姿は、地元では見慣れたランドマークとして知られています。",
    "写真の撮影角度から考えても、江ノ島を海越しに望める沿岸のどこかから撮影されたとみてよさそうです。",
]))

blocks.append(h2("撮影場所は新江ノ島水族館(えのすい)?"))
blocks.append(minibox('<p style="margin:0;"><strong>具体的な撮影スポット(推定):</strong>江ノ島を望む海沿いの木製デッキ、赤みがかった手すりが特徴の通路</p>'))
blocks.append(p([
    "コイノートと同じ日に投稿された関連画像を見比べてみると、木目調のデッキと赤みを帯びた手すりが続く通路の写真が複数枚見つかりました。",
    "このデッキから見える景色も、海の向こうに江ノ島とシーキャンドルが浮かぶ構図になっており、YUKIの写真と非常によく似た景観です。",
]))
blocks.append(img2_html)
blocks.append(p([
    "屋根付きの通路とベンチが並ぶこのデッキの雰囲気は、新江ノ島水族館(えのすい)の館内から屋外テラスへとつながる通路の特徴とよく似ています。",
    "えのすいは片瀬海岸に面した立地で、館内の窓や屋外デッキから海越しに江ノ島を一望できることで知られている水族館です。",
]))
blocks.append(img3_html)
blocks.append(img4_html)
blocks.append(p([
    "砂浜と海岸線、そして木製の通路が続く様子から見ても、この一帯が水族館の敷地内である可能性は高そうです。",
    "断定はできないものの、複数枚の写真すべてに共通して江ノ島とみられる島影が写り込んでいることから、YUKIがこの日訪れたのは<strong>片瀬海岸に面した新江ノ島水族館(えのすい)</strong>とみて間違いなさそうです。",
]))

blocks.append(h2("「新しい家族」ことカワウソについて"))
blocks.append(minibox('<p style="margin:0;"><strong>話題のポイント:</strong>コメント欄で「新しい家族お迎えよかったね」「可愛い家族かわいい」といった反応が相次いでいる</p>'))
blocks.append(p([
    "今回のコイノート更新をめぐっては、YUKIが新しく迎えたという「家族」も話題になっています。",
    "コメント欄には「可愛い家族お迎えよかったね結くんのおかげ今日も幸せ」「新しい家族かわいい」といった反応が寄せられており、YUKIが何らかのぬいぐるみやグッズを新たに迎えたことがうかがえます。",
    "水族館を訪れた流れと合わせて考えると、館内のショップでカワウソをモチーフにしたぬいぐるみやグッズを購入した可能性がありそうですが、この点についてYUKI本人からの詳しい説明はまだなく、あくまで写真とコメントから推測できる範囲にとどまります。",
]))

blocks.append(h2("YUKIは以前から江ノ島がお気に入り?"))
blocks.append(minibox('<p style="margin:0;"><strong>出身地:</strong>神奈川県(江ノ島がある藤沢市と同じ県内)</p>'))
blocks.append(p([
    "同じ投稿には、夜に撮影されたとみられる写真も添えられていました。",
    "ヤシの木が並ぶ駐車場を背景にしたカットで、遠くには青色にライトアップされたタワーがぼんやりと浮かび上がっています。",
]))
blocks.append(img5_html)
blocks.append(p([
    "江の島シーキャンドルは夜になるとさまざまな色にライトアップされることで知られており、この青い光り方も特徴のひとつです。",
    "もう1枚は旧車を背景にしたカットで、こちらにも同じ位置に青いタワーの明かりが写り込んでいます。",
]))
blocks.append(img6_html)
blocks.append(p([
    "昼間のコイノート写真とは別の日に撮影されたとみられるこれらの写真から、YUKIが今回に限らず江ノ島を何度か訪れている可能性がうかがえます。",
    "YUKIの出身地は神奈川県で、江ノ島がある藤沢市も同じ県内にあたります。",
    "実際、今回の投稿には地元とみられるファンから「地元ありがとう」というコメントも寄せられており、江ノ島周辺が地元ファンにとっても身近なスポットであることがうかがえます。",
]))

blocks.append(h2("新江ノ島水族館(えのすい)とはどんな施設?"))
blocks.append(p([
    "新江ノ島水族館(えのすい)は、神奈川県藤沢市の片瀬海岸に面した水族館で、相模湾の生き物を中心に展示する「相模湾ゾーン」や、クラゲの展示で知られる「クラゲファンタジーホール」などが人気のスポットです。",
    "館内から海越しに江ノ島を望める眺望のよさでも知られており、デート・観光スポットとしても定番の場所です。",
    "湘南エリアの人気施設だけに、KO1KEYZのメンバーがプライベートで訪れていたと分かれば、地元ファンを中心に盛り上がりそうです。",
]))
blocks.append(wphtml('''<iframe
  src="https://maps.google.com/maps?q=%E6%96%B0%E6%B1%9F%E3%83%8E%E5%B3%B6%E6%B0%B4%E6%97%8F%E9%A4%A8&t=&z=15&ie=UTF8&iwloc=&output=embed"
  width="100%" height="350" frameborder="0" scrolling="no"
  style="border:0;" loading="lazy">
</iframe>'''))

blocks.append(h2("まとめ"))
blocks.append(wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:6px;overflow:hidden;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">YUKIのコイノート写真の場所まとめ</p>
<div style="padding:14px 18px;background:#f7f6f4;">
<p style="margin:0;">
✔ <strong>撮影日:</strong>2026年8月19日更新のコイノートで公開<br>
✔ <strong>背景の正体:</strong>神奈川県藤沢市の江ノ島、白いタワーは展望灯台「江の島シーキャンドル」とみられる<br>
✔ <strong>撮影場所(推定):</strong>江ノ島を望む海沿いのデッキがある新江ノ島水族館(えのすい)<br>
✔ <strong>話題の家族:</strong>水族館訪問と合わせてカワウソ関連のグッズを迎えた可能性<br>
✔ <strong>過去の訪問歴:</strong>夜に撮影されたとみられる写真もあり、以前から江ノ島を訪れている可能性がある
</p>
<p style="margin:10px 0 0 0;">江ノ島水族館や神奈川県内で、ばったりYUKIに会えるのでは…?と少し期待してしまうくらい、江ノ島がお気に入りのようですね!</p>
</div>
</div>'''))

blocks.append(wphtml(f'''<div style="border:1px solid #ddd9d3;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f6f4;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-1.com/what-is-the-family-structure-o-10480">YUKI(後藤結)の家族構成を調査した記事</a></li>
<li><a href="https://chomoand-1.com/what-is-the-room-allocation-at-11122">KO1KEYZ宿舎の部屋割りを予想した記事</a></li>
<li><a href="https://chomoand-1.com/ko1keyz-why-was-the-debut-date-10449">KO1KEYZのデビュー日の理由を解説した記事</a></li>
</ul>
</div>'''))

content = "\n\n".join(blocks)

plain_len = len(re.sub(r"<[^>]+>|<!--.*?-->", "", content))
print("content length (chars):", plain_len)


def get_slug(title, fallback):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={urllib.parse.quote(title)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        en = "".join(seg[0] for seg in data[0])
        slug = re.sub(r"[^a-z0-9\s-]", "", en.lower())
        slug = re.sub(r"\s+", "-", slug.strip())
        slug = re.sub(r"-+", "-", slug)[:30].rstrip("-")
        if slug:
            return slug
    except Exception as e:
        print("translate failed, using fallback slug:", e)
    return fallback


EXISTING_POST_ID = 11552
EXISTING_EYECATCH_MEDIA_ID = 11550

if EXISTING_EYECATCH_MEDIA_ID:
    eyecatch_media = {"id": EXISTING_EYECATCH_MEDIA_ID}
    print("reusing eyecatch media id:", eyecatch_media["id"])
else:
    with open(EYECATCH_PATH, "rb") as f:
        eyecatch_bytes = f.read()
    eyecatch_r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={
            **HEADERS_AUTH,
            "Content-Type": "image/png",
            "Content-Disposition": 'attachment; filename="goto_yuki_enoshima_eyecatch.png"',
        },
        data=eyecatch_bytes,
    )
    eyecatch_r.raise_for_status()
    eyecatch_media = eyecatch_r.json()
    print("eyecatch media id:", eyecatch_media["id"])

if EXISTING_POST_ID:
    payload = {
        "title": title,
        "content": content,
        "status": "draft",
        "featured_media": eyecatch_media["id"],
    }
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_POST_ID}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print("UPDATED_POST_ID", post["id"])
    print("SLUG", post["slug"])
else:
    slug = get_slug(title, "yukis-koinote-photo-location-enoshima")
    print("slug:", slug)
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "categories": [66],
        "author": 2,
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

    r2 = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps({"status": "draft", "featured_media": eyecatch_media["id"]}).encode("utf-8"),
    )
    r2.raise_for_status()

print("PREVIEW", f"{WP_URL}/?p={post['id']}")

with open(ROOT / "tmp_goto_yuki_enoshima_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
