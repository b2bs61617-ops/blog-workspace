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

VIDEO_URL = "https://youtu.be/bipgdNcr3ok"

EXISTING_MEDIA_IDS = [11129, 11130, 11131]

img1_media, img2_media, img3_media = [
    requests.get(f"{WP_URL}/wp-json/wp/v2/media/{mid}", headers=HEADERS_AUTH).json()
    for mid in EXISTING_MEDIA_IDS
]
print("img1", img1_media["id"], "img2", img2_media["id"], "img3", img3_media["id"])


def build_img_html(media, alt, caption):
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
<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>
</figure>'''


VIDEO_CAPTION = f'出典:KO1KEYZ公式YouTube「🌙 KO1KEYZ Night Routine...⭐️」({VIDEO_URL})'
img1_html = f"<!-- wp:html -->\n{build_img_html(img1_media, 'SIYOUNGパートのタイトルカード', VIDEO_CAPTION)}\n<!-- /wp:html -->"
img2_html = f"<!-- wp:html -->\n{build_img_html(img2_media, 'シートマスクをつけながら赤色LEDの美顔器を頬に当てるSIYOUNG', VIDEO_CAPTION)}\n<!-- /wp:html -->"
img3_html = f"<!-- wp:html -->\n{build_img_html(img3_media, 'クローゼットで部屋着を畳むSIYOUNG', VIDEO_CAPTION)}\n<!-- /wp:html -->"


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def hr():
    return '<!-- wp:separator --><hr class="wp-block-separator has-alpha-channel-opacity"/><!-- /wp:separator -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def capbox(ttl, rows, style="is-style-small_ttl"):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;white-space:nowrap;">{k}</td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div class="swell-block-capbox cap_box {style}">
<div class="cap_box_ttl">{ttl}</div>
<div class="cap_box_content">
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>
</div>''')


title = "SIYOUNGの美顔器と美容液はいくら?ナイトルーティンで判明"

blocks = []

blocks.append(p([
    "KO1KEYZの公式YouTubeチャンネルで、メンバーそれぞれのお風呂上がりから就寝までを追った「🌙 KO1KEYZ Night Routine...⭐️」が公開されました。",
    "そのなかでもSIYOUNG(パク・シヨン)のパートは、<strong>シートマスクをつけながら美顔器を当てる本格スキンケア</strong>が披露されており、Xでは「美容看護師をしている」というファンが使用アイテムを特定する投稿をして話題になっています。",
    "この記事では、SIYOUNGが使っている美容液と美顔器の正体、そして彼らしい丁寧なナイトルーティンの流れを詳しく紹介します。",
]))
blocks.append(hr())

blocks.append(h2("動画情報"))
blocks.append(capbox("動画情報", [
    ("動画タイトル", "🌙 KO1KEYZ Night Routine...⭐️"),
    ("チャンネル", "KO1KEYZ公式YouTube"),
    ("公開日", "2026年8月10日"),
    ("出演", "DAIKI・ISSA・KEITO・KOSUKE・RYOGA・RYUJI・SHINHAENG・SIYOUNG・TOWA・YOSHIKI・YUKI・YURAの12人(この記事ではSIYOUNGのパートを中心に紹介)"),
    ("URL", f'<a href="{VIDEO_URL}" target="_blank" rel="noopener">{VIDEO_URL}</a>'),
]))
blocks.append(hr())

blocks.append(h2("SIYOUNG(パク・シヨン)はどんな人?"))
blocks.append(capbox("SIYOUNGのプロフィール", [
    ("名前", "パク・シヨン(박시영・PARK SIYOUNG)"),
    ("生年月日", "2003年5月6日"),
    ("年齢", "23歳(2026年8月時点)"),
    ("出身地", "韓国・京畿道"),
    ("身長", "178cm"),
    ("メンバーカラー", "白"),
    ("経歴", "7人組ボーイズグループ「MIRAE(未来少年)」の元メンバー。2021年デビュー、2023年7月に脱退"),
]))
blocks.append(p([
    "SIYOUNGは、韓国出身の練習生で、K-POP仕込みのダンススキルと端正なビジュアルを持つ実力派です。",
    "7人組ボーイズグループ「MIRAE(未来少年)」のメインダンサーラインとして2021年にデビューし、2023年7月にグループを脱退したのち、2026年放送の『PRODUCE 101 JAPAN 新世界(日プ4)』に出演してKO1KEYZ入りを果たしました。",
    "以前公開されていたwiki風プロフィール記事(<a href=\"https://chomoand-1.com/parksiyoung_wiki-502\" target=\"_blank\" rel=\"noopener\">パク・シヨンのwiki風経歴は?デビュー経験ありの実力派!</a>)でも、体の使い方の綺麗さや振り付けの再現度の高さが紹介されていましたが、今回のナイトルーティンではその実力を支える美容習慣が明らかになりました。",
]))
blocks.append(hr())

blocks.append(h2("寡黙に、でも丁寧に。SIYOUNGのナイトルーティン"))
blocks.append(wphtml('''<div style="border:1px solid #dde3e8;border-left:4px solid #a9b6c2;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f5f7f9;">
<p style="margin:0;"><strong>流れ:</strong>シートマスク+美顔器→トナー→セラム→マッサージ(美顔器)→クリーム→香水→1日を振り返る日記→就寝</p>
</div>'''))
blocks.append(img1_html)
blocks.append(p([
    "動画は、他メンバーのパートでルームメイトとして名前が挙がっていたSIYOUNGが、静かに「こんにちは」と挨拶するところからスタートします。",
    "明るい照明のバスルームで撮影されていたKEITOのパートとは対照的に、SIYOUNGのパートは照明を落とした寝室で進行し、落ち着いた雰囲気のなかで淡々とスキンケアをこなしていくのが印象的です。",
    "まず取り入れているのがシートマスクで、装着しながら美顔器を頬に当て、「まずはパックしながら、これが大事だと思って毎日やっています」とコメント。",
    "そのあとはトナー、セラムと工程を重ね、最後にはマッサージ用の美顔器で顔まわりのリンパを流す念入りなケアを行っていました。",
]))
blocks.append(hr())

blocks.append(h2("判明した美容アイテムの正体は?"))
blocks.append(img2_html)
blocks.append(p([
    "動画を確認したところ、SIYOUNGが使用しているアイテムは次の2点とみられます。",
    "1つ目は、シートマスクの上から頬に当てていた美顔器で、韓国の皮膚科由来コスメブランドmedicube(メディキューブ)の「ブースタープロX2」とみられます。",
    "8種類のモードと8色のLEDライトを搭載したハンディ美顔器で、動画内でも赤色LEDを点灯させながらマスクの上からケアする様子が確認できました。",
    "2つ目は、トナーのあとに使用していたセラムで、Dr.G(ドクタージー)の「R.E.D BLEMISH クリア ハイアルシカ スージングセラム」と成分・パッケージの特徴が一致します。",
    "低分子ヒアルロン酸とツボクサエキス(シカ)を配合し、火照った肌を素早く鎮める設計の美容液で、韓国では鎮静ケアの定番として知られています。",
]))
blocks.append(capbox("使用アイテムの価格まとめ", [
    ("medicube ブースタープロX2", "35,500円(税込)"),
    ("Dr.G R.E.D BLEMISH クリア ハイアルシカ スージングセラム 50mL", "2,750円(税込)"),
    ("<strong>合計</strong>", "<strong>38,250円(税込)</strong>"),
], style="is-style-onborder_ttl"))
blocks.append(p([
    "2つ合わせると税込<strong>38,250円</strong>という金額になり、いずれも韓国コスメらしい鎮静・整肌に特化したアイテムで揃えられているのが特徴です。",
    "なお、動画内でアイテム名が明言されているわけではないため、あくまで映像から読み取れる特徴をもとにした推測であることは留意しておきたいところです。",
]))
blocks.append(capbox("購入先", [
    ("medicube ブースタープロX2", '<a href="https://themedicube.jp/products/booster-pro-x2" target="_blank" rel="noopener nofollow">MEDICUBE公式オンラインショップ</a>'),
    ("Dr.G R.E.D BLEMISH クリア ハイアルシカ スージングセラム", '<a href="https://www.qoo10.jp/shop/drg" target="_blank" rel="noopener nofollow">Dr.G公式Qoo10ショップ</a>'),
]))
blocks.append(hr())

blocks.append(h2("1日を振り返ってから眠る、SIYOUNGらしい締めくくり"))
blocks.append(img3_html)
blocks.append(p([
    "スキンケアを終えたあと、SIYOUNGは寝る前の習慣として「今日の1日を見て確認して、僕が今日間違えたこととかあれば、明日はもっと完璧な人になるようにと毎日願います」と話し、その日の反省や願いごとを日記のように整理する時間を紹介していました。",
    "派手な演出やトークで魅せるタイプではなく、淡々とした所作の端々に丁寧さがにじむのがSIYOUNGらしいところで、最後は「最後まで動画を見てくれて本当にありがとうございました」と静かに締めくくっています。",
    "MIRAEでの活動経験を経て、体の使い方や自己管理への意識の高さが随所に感じられるナイトルーティンでした。",
]))
blocks.append(hr())

blocks.append(h2("まとめ"))
blocks.append(wphtml('''<div class="swell-block-capbox cap_box is-style-small_ttl">
<div class="cap_box_ttl">SIYOUNGのナイトルーティンまとめ</div>
<div class="cap_box_content">
<p class="has-border -border02 wp-block-paragraph">
✔ <strong>使用アイテム(推定)</strong>:medicube ブースタープロX2(35,500円)+Dr.G R.E.D BLEMISH クリア ハイアルシカ スージングセラム(2,750円)<br>
✔ <strong>合計金額</strong>:38,250円(税込)<br>
✔ <strong>使うタイミング</strong>:シートマスクの上から美顔器、トナーのあとにセラム<br>
✔ <strong>締めくくり</strong>:1日を振り返り、明日への願いごとを整理してから就寝<br>
✔ <strong>背景</strong>:韓国ボーイズグループ「MIRAE」での活動経験を持つ実力派
</p>
<p>照明を落とした静かな雰囲気のなかで、着実にケアを重ねていくSIYOUNGらしいナイトルーティンでした。<br>
まだSIYOUNGの魅力に詳しくないという人も、これをきっかけに本編の動画も見てみてはいかがでしょうか!</p>
</div>
</div>'''))
blocks.append(wphtml('''<div style="border:1px solid #dde3e8;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f5f7f9;">
<p style="margin:0 0 8px 0;"><strong>SIYOUNGについては、このブログの他の記事でも詳しく紹介しています。</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="https://chomoand-1.com/parksiyoung_wiki-502" target="_blank" rel="noopener">wiki風プロフィール・経歴をまとめた記事</a></li>
<li><a href="https://chomoand-1.com/parksiyoung_gakureki-6022" target="_blank" rel="noopener">学歴を調査した記事</a></li>
</ul>
</div>'''))

content = "\n\n".join(blocks)

print("content length (chars):", len(re.sub(r"<[^>]+>|<!--.*?-->", "", content)))


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


EXISTING_POST_ID = 11132

if EXISTING_POST_ID:
    payload = {"content": content, "status": "draft", "title": title, "featured_media": 11155}
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_POST_ID}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print("UPDATED POST_ID", post["id"])
else:
    slug = get_slug(title, "ko1keyz-siyoung-beauty-items")
    print("slug:", slug)
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "categories": [66, 63],
        "author": 2,
        "featured_media": img2_media["id"],
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

with open(ROOT / "tmp_siyoung_night_routine_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
