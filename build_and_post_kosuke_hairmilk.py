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

FRAME_DIR = ROOT / "frames_kosuke"
VIDEO_URL = "https://youtu.be/bipgdNcr3ok"


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


EXISTING_MEDIA_IDS = [11133, 11134, 11135]

if len(EXISTING_MEDIA_IDS) == 3:
    print("reusing already-uploaded images...", EXISTING_MEDIA_IDS)
    img1_media, img2_media, img3_media = [
        requests.get(f"{WP_URL}/wp-json/wp/v2/media/{mid}", headers=HEADERS_AUTH).json()
        for mid in EXISTING_MEDIA_IDS
    ]
else:
    print("uploading images...")
    img1_media = upload_media(FRAME_DIR / "t514.jpg", "kosuke_night_routine_hairmilk.jpg", "image/jpeg")
    img2_media = upload_media(FRAME_DIR / "t486.jpg", "kosuke_night_routine_pack.jpg", "image/jpeg")
    img3_media = upload_media(FRAME_DIR / "t498.jpg", "kosuke_night_routine_daikicream.jpg", "image/jpeg")
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
img1_html = f"<!-- wp:html -->\n{build_img_html(img1_media, 'KOSUKEが髪にヘアミルクをつけてドライヤーで乾かしているシーン', VIDEO_CAPTION)}\n<!-- /wp:html -->"
img2_html = f"<!-- wp:html -->\n{build_img_html(img2_media, 'KOSUKEがシートパックをつけているシーン', VIDEO_CAPTION)}\n<!-- /wp:html -->"
img3_html = f"<!-- wp:html -->\n{build_img_html(img3_media, 'KOSUKEがDAIKIから借りたクリームをつけているシーン', VIDEO_CAPTION)}\n<!-- /wp:html -->"


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


def capbox_list(ttl, items, style="is-style-small_ttl"):
    lis = "\n".join(f"<li>「{t}」</li>" for t in items)
    return wphtml(f'''<div class="swell-block-capbox cap_box {style}">
<div class="cap_box_ttl">{ttl}</div>
<div class="cap_box_content">
<ul>
{lis}
</ul>
</div>
</div>''')


title = "KO1KEYZ康祐のヘアミルクは?ナイトルーティンで判明"

blocks = []

blocks.append(p([
    "KO1KEYZの公式YouTubeチャンネルで、メンバーそれぞれのお風呂上がりから就寝までを追った「🌙 KO1KEYZ Night Routine...⭐️」が公開されました。",
    "そのなかでもKOSUKE(照井康祐)のパートでは、<strong>サラサラの髪をキープするヘアミルクの使用シーン</strong>が話題になり、Xでは愛用ブランドを特定する投稿まで登場しています。",
    "この記事では、KOSUKEが使っているヘアミルクの正体と、ナイトルーティン全体で見えた素顔を詳しく紹介します。",
]))
blocks.append(hr())

blocks.append(h2("動画情報"))
blocks.append(capbox("動画情報", [
    ("動画タイトル", "🌙 KO1KEYZ Night Routine...⭐️"),
    ("チャンネル", "KO1KEYZ公式YouTube"),
    ("公開日", "2026年8月10日"),
    ("出演", "DAIKI・ISSA・KEITO・KOSUKE・RYOGA・RYUJI・SHINHAENG・SIYOUNG・TOWA・YOSHIKI・YUKI・YURAの12人(この記事ではKOSUKEのパートを中心に紹介)"),
    ("URL", f'<a href="{VIDEO_URL}" target="_blank" rel="noopener">{VIDEO_URL}</a>'),
]))
blocks.append(hr())

blocks.append(h2("KOSUKE(照井康祐)はどんな人?"))
blocks.append(capbox("KOSUKEのプロフィール", [
    ("本名", "照井康祐(てるい こうすけ)"),
    ("生年月日", "2007年12月2日"),
    ("年齢", "18歳"),
    ("出身地", "千葉県"),
    ("身長", "174cm"),
    ("MBTI", "ISTP"),
    ("メンバーカラー", "赤"),
    ("日プでの成績", "最終順位11位(381,605票)、初回評価Cクラスからの逆転デビュー"),
]))
blocks.append(p([
    "KOSUKEは『PRODUCE 101 JAPAN 新世界』参加前、LDH運営のEXPG TOKYOでダンスを学び、その後ワタナベエンターテインメント傘下の「DBSing」でも活動していたダンス実力者です。",
    "以前公開されていた前世・経歴の調査記事(<a href=\"https://chomoand-1.com/teruikosuke_profile-106\" target=\"_blank\" rel=\"noopener\">【日プ4】照井康祐の前世やプロフは？元EXPG生で高いダンススキル！</a>)でも紹介された通り、ダンス・ラップ両面で存在感を発揮するオールラウンダーとして知られています。",
    "そんなKOSUKEの今回のナイトルーティンでは、ダンスの実力とはまた違う、丁寧な美容へのこだわりが見えるシーンが多く映っていました。",
]))
blocks.append(hr())

blocks.append(h2("サラサラヘアーの秘訣、愛用ヘアミルクをチェック"))
blocks.append(img1_html)
blocks.append(p([
    "動画のなかでとくに注目を集めたのが、ドライヤー前に髪へヘアミルクをなじませているシーンです。",
    "画面には「髪にミルクをしっかりつけて乾かしてます」という字幕が添えられており、保湿を意識しながら丁寧に髪を乾かす様子が映っています。",
    "この場面を見たXユーザーが「康祐のサラサラヘアーの秘訣は&PAIRのヘアミルク」と投稿したことで、使用アイテムのブランドが一気に拡散されました。",
]))
blocks.append(hr())

blocks.append(h2("判明したヘアミルクの正体は「&PAIR」"))
blocks.append(p([
    "投稿や動画の内容を照らし合わせると、KOSUKEが使っているのは株式会社ヴィークレアのヘアケアブランド「&PAIR(アンドペア)」のヘアミルクとみられます。",
    "&PAIRは『PRODUCE 101 JAPAN 新世界』の協賛パートナーに正式決定しているブランドで、番組期間中には対象商品の購入者に最終回観覧チケットが当たるコラボキャンペーンも実施されていました。",
    "KOSUKE自身、日プ新世界の練習生時代からこのブランドに親しみがあったと考えると、デビュー後も使い続けている自然な流れがうかがえます。",
]))
blocks.append(capbox("&PAIR コントロール リペア 2in1 ヘアミルクミストの情報", [
    ("ブランド", "&PAIR(アンドペア)/株式会社ヴィークレア"),
    ("内容量", "150mL"),
    ("価格", "1,595円(税込)"),
    ("特徴", "ゆっくりプッシュでミルク状、素早くプッシュでミスト状になる2way式"),
    ("香り", "ピンクローズ in ブルーバーベナ"),
    ("購入先", '<a href="https://vicrea.net/shopbrand/andpair/" target="_blank" rel="noopener">公式ストア</a> / <a href="https://www.amazon.co.jp/dp/B0DZX2CPQH" target="_blank" rel="noopener">Amazon</a> / <a href="https://item.rakuten.co.jp/vicrea/pair_mist1/" target="_blank" rel="noopener">楽天市場</a>'),
], style="is-style-onborder_ttl"))
blocks.append(p([
    "このシリーズ最大の特徴は、プッシュの仕方で質感が変わる2way式という仕組みです。",
    "ゆっくり押すとしっとりまとまるミルク状になり、ドライヤー前のうねり・アホ毛抑制に向いています。",
    "反対に素早く押すと軽いミスト状になるため、朝の寝癖直しやスタイリングの仕上げにも使い分けられる設計になっています。",
    "税込1,595円と手に取りやすい価格ながら、KOSUKEのような艶やかなサラサラヘアーを再現できるとあって、投稿を見たファンの間でも購入の動きが広がっていました。",
]))
blocks.append(hr())

blocks.append(h2("ナイトルーティンで見えたKOSUKEのこだわり"))
blocks.append(img2_html)
blocks.append(p([
    "ヘアミルク以外にも、KOSUKEのルーティンには丁寧なスキンケアの工程がいくつも映っていました。",
    "シートパックを両手できっちり密着させ、「では7・8分後に」とコメントしてしっかり時間を置く場面もその一つです。",
    "パックを外したあとは「クリームのピカピカ感が残っていますが終わりました」と、うるおいが行き渡った肌の状態を確認しながら仕上げていました。",
]))
blocks.append(img3_html)
blocks.append(p([
    "印象的だったのは、字幕で「DAIKIくんから借りたクリームをつけます」と紹介されていた場面です。",
    "自分のアイテムだけでなく、メンバーのDAIKIからクリームを借りて試すというやり取りからは、KO1KEYZらしい仲の良さも垣間見えました。",
    "動画の中盤ではKEITOが顔をのぞかせる場面もあり、「我がKO1KEYZのヒョンでございます」と茶目っ気たっぷりに声をかけるひとコマも。",
    "メンバー同士が自然に行き来する共同生活ならではの空気感が伝わってくるルーティンでした。",
]))
blocks.append(hr())

blocks.append(h2("SNSでの反応"))
blocks.append(capbox_list("ヘアミルクの発見に反応する声", [
    "康祐のサラサラヘアーの秘訣は&PAIRのヘアミルクだったの尊すぎる",
    "新世界中も「買いました♩良すぎて♩」って話してたやつだ",
    "本日購入予定にした",
]))
blocks.append(capbox_list("普段の様子に反応する声", [
    "DAIKIからクリーム借りてるのかわいすぎ",
    "ケトが乱入してくるのほっこりする",
    "スキンケア丁寧すぎて見習いたい",
]))
blocks.append(p([
    "動画公開直後から、ヘアミルクのブランドを特定する投稿とあわせて、KOSUKEの丁寧な美容ルーティンそのものに好意的な反応が多く見られました。",
    "手が届きやすい価格のアイテムだったことも、購入を後押しするポイントになっていたようです。",
]))
blocks.append(hr())

blocks.append(h2("まとめ"))
blocks.append(wphtml('''<div class="swell-block-capbox cap_box is-style-small_ttl">
<div class="cap_box_ttl">KOSUKEのヘアミルクまとめ</div>
<div class="cap_box_content">
<p class="has-border -border02 wp-block-paragraph">
✔ <strong>使用アイテム</strong>:&PAIR コントロール リペア 2in1 ヘアミルクミスト(150mL・1,595円)<br>
✔ <strong>使い方</strong>:ドライヤー前にミルク状でうるおいキープ、朝はミスト状で寝癖直しにも使える2way式<br>
✔ <strong>ブランド背景</strong>:『PRODUCE 101 JAPAN 新世界』の協賛パートナー、練習生時代から馴染みのあるアイテム<br>
✔ <strong>ルーティンの見どころ</strong>:シートパックやDAIKIから借りたクリームなど、丁寧なスキンケアとメンバー同士の交流
</p>
<p>ダンス実力派のイメージが強いKOSUKEですが、ナイトルーティンでは美容にも手を抜かない丁寧さが印象的でした。<br>
気になった人は、ぜひ本編の動画もチェックしてみてはいかがでしょうか!</p>
</div>
</div>'''))
blocks.append(wphtml('''<div style="border:1px solid #f0b4b4;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#fdecec;">
<p style="margin:0 0 8px 0;"><strong>KOSUKEやKO1KEYZについては、このブログの他の記事でも詳しく紹介しています。</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="https://chomoand-1.com/teruikosuke_profile-106" target="_blank" rel="noopener">照井康祐の前世・プロフィールを調査した記事</a></li>
<li><a href="https://chomoand-1.com/ko1keyz-no-color-10196" target="_blank" rel="noopener">KO1KEYZメンバーカラーをまとめた記事</a></li>
<li><a href="https://chomoand-1.com/ko1keyz_gakureki-9974" target="_blank" rel="noopener">KO1KEYZメンバーの学歴をまとめた記事</a></li>
<li><a href="https://chomoand-1.com/profile-12-9725" target="_blank" rel="noopener">KO1KEYZメンバー全員のプロフィールを紹介した記事</a></li>
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


EXISTING_POST_ID = 11136

SUMMARY = "KO1KEYZ照井康祐のナイトルーティン動画で判明したヘアミルクは&PAIR製。150mL1,595円の2way式で、ドライヤー前はミルク状、朝はミスト状と使い分けられる人気アイテムです。"

if EXISTING_POST_ID:
    payload = {"content": content, "status": "draft"}
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_POST_ID}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print("UPDATED POST_ID", post["id"])
else:
    slug = get_slug(title, "ko1keyz-kosuke-hairmilk-p")
    print("slug:", slug)
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "categories": [66, 63],
        "author": 2,
        "meta": {"jetpack_publicize_message": SUMMARY},
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

featured_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"featured_media": img1_media["id"], "status": "draft"}).encode("utf-8"),
)
featured_r.raise_for_status()
print("FEATURED_MEDIA set to", img1_media["id"])

with open(ROOT / "tmp_kosuke_hairmilk_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
