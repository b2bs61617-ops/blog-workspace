# -*- coding: utf-8 -*-
import json, base64, os, re, subprocess, sys, urllib.request, urllib.parse
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

# 元ネタ:メンバーの耳を1人ずつ観察してピアスホールの位置を書き出したXの投稿(2026-08-31)
SOURCE_TWEET = "https://x.com/idis_midori/status/2094425938150994039"

CHART_IMG = ROOT / "images" / "ko1keyz_piercing_count_chart.png"


def upload_media_from_file(path: Path, filename: str, content_type: str = "image/png"):
    headers = {
        **HEADERS_AUTH,
        "Content-Type": content_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=path.read_bytes())
    r.raise_for_status()
    return r.json()


print("uploading chart image...")
chart_media = upload_media_from_file(CHART_IMG, "ko1keyz_piercing_count_chart.png")
print("chart_media", chart_media["id"])


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


chart_html = "<!-- wp:html -->\n" + build_img_html(
    chart_media,
    "コイキーズ12人のピアスの数を左右合算でまとめた一覧図",
    "Xでの観察情報をもとに作成した一覧。数は左右の耳の合計です。",
) + "\n<!-- /wp:html -->"


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


ACCENT = "#8a8378"
BORDER = "#ded9d2"
BG = "#f8f6f4"


def titlebox(ttl, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def table_block(headers, rows):
    thead = "".join(f"<td>{h}</td>" for h in headers)
    trows = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr>{thead}</tr>
{trows}
</tbody></table></figure>
<!-- /wp:table -->'''


EMOJI_URL = "https://chomoand-1.com/summary-of-ko1keyz-member-emoj-10560"
CHEMI_URL = "https://chomoand-1.com/ko1keyz-chemi-names-11773"
SHOE_URL = "https://chomoand-1.com/what-are-the-shoe-sizes-of-ko1-11551"
RYUJI_URL = "https://chomoand-1.com/is-ryuji-left-handed-investiga-11388"

title = "コイキーズのピアスは何個？最多はTOWAで5つ！"

blocks = []

blocks.append(p([
    "コイキーズ(KO1KEYZ)は、耳元のピアスにメンバーごとの個性が出るグループです。",
    "Xではメンバーの耳を1人ずつ観察してピアスの位置をまとめた投稿が話題になっており、それによると<strong>いちばん多いのはTOWA(濱田永遠)の5つ、続いてDAIKI(加藤大樹)の4つ、KOSUKE(照井康祐)の3つ</strong>という並びでした。",
    "この記事では、12人それぞれのピアスの数を左右の内訳つきで一覧にしたうえで、星モチーフやゴールドなど実際に目撃されているデザインもまとめます。",
]))

blocks.append(titlebox("この記事でわかること", [
    "メンバー12人それぞれのピアスの数(左右の耳の内訳つき)",
    "ピアスが多いメンバー・開けていないメンバー",
    "KOSUKEの星ピアスなど、目撃されているデザイン",
]))

blocks.append(h2("コイキーズメンバーのピアスは何個？12人まとめ"))
blocks.append(minibox('<p style="margin:0;"><strong>最多はTOWAの5つ、次いでDAIKIが4つ、KOSUKEが3つ。</strong>KEITO・RYUJI・YOSHIKI・YUKIが2つずつで、残る5人は開けていません。</p>'))
blocks.append(p([
    "まとめの元になっているのは、2026年8月末にXで公開された、メンバーの耳を1人ずつ観察してピアスホールの位置を書き出した投稿です。",
    "そこにデビューシングルのアーティスト写真やライブ・配信での見え方を重ねて整理すると、12人のピアスの数は次のようになります。",
]))
blocks.append(chart_html)
blocks.append(p([
    "左右の耳の内訳も含めて表にすると、以下のとおりです。",
]))
blocks.append(table_block(
    ["メンバー", "右耳", "左耳", "合計"],
    [
        ["TOWA(濱田永遠)", "2", "3", "5"],
        ["DAIKI(加藤大樹)", "2", "2", "4"],
        ["KOSUKE(照井康祐)", "1", "2", "3"],
        ["KEITO(小野慶人)", "1", "1", "2"],
        ["RYUJI(杉山竜司)", "1", "1", "2"],
        ["YUKI(後藤結)", "1", "1", "2"],
        ["YOSHIKI(矢田佳暉)", "1", "1", "2"],
        ["ISSA(柳谷伊冴)", "0", "0", "0"],
        ["YURA(安部結蘭)", "0", "0", "0"],
        ["RYOGA(飯塚亮賀)", "0", "0", "0"],
        ["SIYOUNG(パク・シヨン)", "0", "0", "0"],
        ["SHINHAENG(オ・シンヘン)", "0", "0", "0"],
    ],
))
blocks.append(p([
    f'<strong><span class="swl-marker mark_green" style="font-size:1.15em;">TOWAだけが軟骨(ヘリックス)にも入れていて、左耳3・右耳2の合計5つ</span></strong>と頭ひとつ抜けています。',
    "1〜2個が中心のグループの中では、TOWA・DAIKI・KOSUKEの3人がピアス多めのグループという構図です。",
]))
blocks.append(p([
    "なお、写真の角度によっては左右どちらの耳か見えづらい部分もあり、YOSHIKI・YURA・YUKIの一部は投稿主も「自信がない」としています。",
    "細かい本数は今後前後する可能性がある点だけ、先にお断りしておきます。",
]))

blocks.append(h2("ピアスが多いTOP3は？TOWA・DAIKI・KOSUKE"))
blocks.append(minibox('<p style="margin:0;"><strong>上位はTOWA(5)・DAIKI(4)・KOSUKE(3)。</strong>3人とも複数ホールで、着けているピアスのデザインもよく知られています。</p>'))
blocks.append(p([
    "<strong>TOWA(濱田永遠)</strong>は左耳に3つ、右耳に2つ。",
    "耳たぶだけでなく軟骨にもホールがあり、12人の中では唯一の5つ持ちです。",
    "自撮りのオフショットではシルバーの小ぶりなスタッドやフープを着けていることが多く、指のリングやチェーンネックレスとあわせてシルバーで統一するのがTOWA流のスタイルになっています。",
]))
blocks.append(p([
    "<strong>DAIKI(加藤大樹)</strong>は左右2つずつの合計4つ。",
    f'本人がXで「韓国公演までにやりたいこと」の一つに<strong>「ピアスを増やす」</strong>と挙げており、今後さらに増える可能性があります。',
    f'7月中旬の私服では、ピアスと服の色をYOSHIKIとのケミ名<a href="{CHEMI_URL}" target="_blank" rel="noopener">「デカ猫」</a>カラーで揃えていたと話題になったこともありました。',
]))
blocks.append(p([
    "<strong>KOSUKE(照井康祐)</strong>は右耳1つ・左耳2つの合計3つ。",
    'デビューシングルのアーティスト写真で着けていた<strong><span class="swl-marker mark_pink">星モチーフのピアス</span></strong>がファンの間で「星のピアス」と呼ばれ、「同じものを探しに行かなきゃ」という声が続出しました。',
    f'メンバーカラーの赤とあわせて、KOSUKEの<a href="{EMOJI_URL}" target="_blank" rel="noopener">メンバー絵文字も星(🌟)</a>なので、この星ピアスはトレードマークとして定着しつつあります。',
]))

blocks.append(h2("2つずつ開けているのは？RYUJI・KEITO・YOSHIKI・YUKI"))
blocks.append(minibox('<p style="margin:0;"><strong>RYUJI・KEITO・YOSHIKI・YUKIの4人は左右1つずつの合計2つ。</strong>中でもRYUJIはピアスをよく付け替えるタイプです。</p>'))
blocks.append(p([
    "<strong>RYUJI(杉山竜司)</strong>は左右1つずつ。",
    "デビューシングルのアー写ではピアスとイヤーカフを重ね付けしていて、ファンからも「ピアスとイヤーカフ」が推しポイントに挙げられていました。",
    "時期によってシルバーからゴールドに変えるなど付け替えも多く、愛犬と遊ぶオフショットで「前と比べてピアスがしっかりゴールドになってる」と気づかれたり、「いつも付けてたピアス取っちゃったの」と外した日に反応があったりと、耳元の変化がこまめに見られています。",
]))
blocks.append(p([
    "<strong>KEITO(小野慶人)</strong>も左右1つずつの2つで、装飾控えめのシルバースタッドが中心です。",
    "<strong>YOSHIKI(矢田佳暉)</strong>は左右1つずつと見られていますが、右耳のホールは観察した投稿でも「自信がない」とされており、はっきり確認できるのは1つです。",
    "<strong>YUKI(後藤結)</strong>も左右1つずつの2つで、2026年8月の写真でピアスを着けている様子が確認され「顔がいいうえにピアスもしてる」と反響がありました。",
]))

blocks.append(h2("ピアスを開けていないメンバーは？5人"))
blocks.append(minibox('<p style="margin:0;"><strong>ISSA・YURA・RYOGA・SIYOUNG・SHINHAENGの5人は、現時点でピアスホールが確認できません。</strong></p>'))
blocks.append(p([
    "野球一筋だったISSA(柳谷伊冴)、サッカー一筋だったRYOGA(飯塚亮賀)、韓国出身のSIYOUNG(パク・シヨン)とSHINHAENG(オ・シンヘン)など、これまでの活動でピアスを開ける機会が少なかったメンバーが並びます。",
    "ただ、デビュー後にメイクや衣装に合わせて開けるメンバーが出てくることは十分に考えられます。",
    "実際、RYUJIも活動初期はピアスの色や本数が今とは違っていたので、この一覧は「2026年秋時点のスナップショット」くらいに捉えておくのがよさそうです。",
]))

blocks.append(titlebox("まとめ", [
    "ピアスが最多なのはTOWAで、軟骨も含めた合計5つ",
    "次いでDAIKIが4つ、KOSUKEが3つ。KEITO・RYUJI・YOSHIKI・YUKIが2つずつ",
    "ISSA・YURA・RYOGA・SIYOUNG・SHINHAENGの5人はピアスホールが確認できない",
    "KOSUKEの星モチーフ、RYUJIのゴールド＋イヤーカフなど、デザインもメンバーごとに個性あり",
]))
blocks.append(p([
    "耳元まで見てみると、シルバーで統一するTOWA、星をトレードマークにするKOSUKEなど、メンバーの好みが意外とはっきり出ています。",
    "ライブ映像やアー写を見るときは、ぜひ耳元にも注目してみてください！",
]))

blocks.append(minibox(f'''<p style="margin:0 0 8px 0;"><strong>コイキーズについては、このブログの他の記事でも詳しく紹介しています。</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{EMOJI_URL}" target="_blank" rel="noopener">メンバー12人の絵文字とその意味まとめ</a></li>
<li><a href="{SHOE_URL}" target="_blank" rel="noopener">KO1KEYZメンバーの靴サイズは？新世界衣装展示で判明！</a></li>
<li><a href="{RYUJI_URL}" target="_blank" rel="noopener">RYUJIは左利き？両利き説の真相を調査！</a></li>
<li><a href="{CHEMI_URL}" target="_blank" rel="noopener">KO1KEYZのケミ名まとめ！「デカ猫」「とわすけ」とは？</a></li>
</ul>'''))

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


SUMMARY = "コイキーズ12人のピアスを1人ずつ調査。最多はTOWAで軟骨含む5つ、次いでDAIKIが4つ、KOSUKEが3つ。KOSUKEの星ピアス、RYUJIのゴールド＋イヤーカフなどデザインもまとめました。"

slug = get_slug(title, "how-many-piercings-do-ko1keyz")
print("slug:", slug)
payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": "draft",
    "categories": [66, 62],
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

EYECATCH_PATH = ROOT / "images" / "ko1keyz_piercings_eyecatch.png"
subprocess.run([
    sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
    "--top", "ピアスは何個？",
    "--main", "KO1KEYZ",
    "--bottom", "メンバー12人の耳元を調査！",
    "--bottom", "最多はTOWAで5つ",
    "--out", str(EYECATCH_PATH),
    "--seed", str(post["id"]),
], check=True)

eyecatch_media = upload_media_from_file(EYECATCH_PATH, "ko1keyz_piercings_eyecatch.png")
EYECATCH_MEDIA_ID = eyecatch_media["id"]
print("EYECATCH_MEDIA_ID", EYECATCH_MEDIA_ID)

featured_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"featured_media": EYECATCH_MEDIA_ID, "status": "draft"}).encode("utf-8"),
)
featured_r.raise_for_status()
print("FEATURED_MEDIA set to", EYECATCH_MEDIA_ID)

for name, val in [
    ("tmp_ko1keyz_piercings_postid.txt", post["id"]),
    ("tmp_ko1keyz_piercings_slug.txt", post["slug"]),
    ("tmp_ko1keyz_piercings_chart_mediaid.txt", chart_media["id"]),
    ("tmp_ko1keyz_piercings_eyecatch_mediaid.txt", EYECATCH_MEDIA_ID),
]:
    (ROOT / name).write_text(str(val), encoding="utf-8")
