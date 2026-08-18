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


def upload_image(path, filename):
    with open(path, "rb") as f:
        data = f.read()
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={
            **HEADERS_AUTH,
            "Content-Type": "image/jpeg",
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
        data=data,
    )
    r.raise_for_status()
    return r.json()


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


EXISTING_POST_ID = 11468
EXISTING_TREKKA_MEDIA_ID = 11466
EXISTING_KUJI_MEDIA_ID = 11467
EXISTING_EYECATCH_MEDIA_ID = 11469

if EXISTING_POST_ID:
    print("reusing already-uploaded images (update run)...")
    r1 = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{EXISTING_TREKKA_MEDIA_ID}", headers=HEADERS_AUTH)
    r1.raise_for_status()
    img_trekka = r1.json()
    r2 = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{EXISTING_KUJI_MEDIA_ID}", headers=HEADERS_AUTH)
    r2.raise_for_status()
    img_kuji = r2.json()
else:
    print("uploading images...")
    img_trekka = upload_image(
        ROOT / "tools" / "Xiy" / "posts_temp_tweet2" / "images" / "post_1_img_1.jpg",
        "ko1keyz_fanclub_booth_trekka_sample.jpg",
    )
    print("trekka sample media id", img_trekka["id"])

    img_kuji = upload_image(
        ROOT / "tools" / "Xiy" / "posts_temp_tweet3" / "images" / "post_1_img_1.jpg",
        "ko1keyz_fanclub_booth_kuji_overview.jpg",
    )
    print("kuji overview media id", img_kuji["id"])

TREKKA_CAPTION = '出典:<a href="https://x.com/KO1KEYZofficial/status/2089630884013961359" target="_blank" rel="noopener">https://x.com/KO1KEYZofficial/status/2089630884013961359</a>'
img_trekka_html = f"<!-- wp:html -->\n{build_img_html(img_trekka, 'KO1KEYZ FANCLUB BOOTH FCトレカのサンプル画像(12種ランダム1枚)', TREKKA_CAPTION)}\n<!-- /wp:html -->"

KUJI_CAPTION = '出典:<a href="https://x.com/_siyoungtokki_/status/2089653778618466339" target="_blank" rel="noopener">https://x.com/_siyoungtokki_/status/2089653778618466339</a>'
img_kuji_html = f"<!-- wp:html -->\n{build_img_html(img_kuji, 'KO1KEYZ FANCLUB BOOTH FCトレカ・KO1LYくじの概要', KUJI_CAPTION)}\n<!-- /wp:html -->"


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def hr():
    return '<!-- wp:separator --><hr class="wp-block-separator has-alpha-channel-opacity"/><!-- /wp:separator -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


# KO1KEYZ記事のUIボックスはメンバーカラーと被らない彩度低めのウォームグレーで統一
ACCENT = "#8a8378"
BORDER = "#ded9d2"
BG = "#f8f6f4"


def capbox(ttl, rows):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;white-space:nowrap;">{k}</td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{ttl}</p>
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>''')


def titlebox(ttl, items):
    lis = "\n".join(f"<li>{t}</li>" for t in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(html_body):
    return wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f7f7;">
{html_body}
</div>''')


def notebox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


FANMEETING_PREDICT_URL = "https://chomoand-1.com/ko1keyz-live-10270"
DEBUT_EVENTS_URL = "https://chomoand-1.com/what-events-will-be-held-to-co-2-11307"
SCHEDULE_URL = "https://chomoand-1.com/what-is-ko1keyzs-future-schedu-10860"

title = "KO1KEYZファンミFCブースはチケットなしで参加できる?"

blocks = []

blocks.append(p([
    "2026年8月18日、KO1KEYZ公式X・公式サイトで、8月21日から始まる『2026 KO1KEYZ 1ST FAN MEETING』にてFANCLUB BOOTHを実施することが発表されました。",
    "内容は<strong>①FC月会費まとめて払いコース限定のオリジナルトレカプレゼント</strong>と<strong>②FC会員なら誰でも参加できるKO1LYくじ</strong>の2本立てで、<strong>どちらも公演のチケットを持っていなくても参加できる</strong>のが大きなポイントです。",
    "この記事では、2つの特典の対象者・参加方法・回数制限などを詳しく整理します。",
]))

blocks.append(titlebox("この記事でわかること", [
    "FCトレカ(月会費まとめて払いコース限定)の内容",
    "KO1LYくじ(FC会員限定)の内容と特賞",
    "チケットがなくても参加できるのか",
]))

blocks.append(h2("そもそも『2026 KO1KEYZ 1ST FAN MEETING』とは?"))
blocks.append(capbox("公演概要", [
    ("東京公演", "TOYOTA ARENA TOKYO／2026年8月21日(金)〜23日(日)"),
    ("兵庫公演", "神戸ワールド記念ホール／2026年9月9日(水)〜10日(木)"),
]))
blocks.append(p([
    "KO1KEYZにとって初めてとなるファンミーティングで、いよいよ東京公演が今週末の8月21日からスタートします。",
    f"開催概要そのものについては、以前予想記事としてまとめた<a href=\"{FANMEETING_PREDICT_URL}\" target=\"_blank\" rel=\"noopener\">KO1KEYZのライブ・ファンミはいつ？ラポネ傾向から日程を大予想！</a>も参考にしてみてください。",
    "そして開幕が目前に迫った8月18日、公式から新たにFANCLUB BOOTHの実施が発表された、というのが今回の記事の内容です。",
]))

blocks.append(h2("新特典①FCトレカ(月会費まとめて払いコース限定)"))
blocks.append(img_trekka_html)
blocks.append(minibox('<p style="margin:0;"><strong>対象:</strong>「月会費まとめて払いコース」のFC会員(チケット不要・当日入会/コース変更でもOK)</p>'))
blocks.append(p([
    "1つ目の特典は、FCの「月会費まとめて払いコース」会員限定で、オリジナルトレカを1枚プレゼントしてもらえる企画です。",
    "トレカは全12種のうちランダムで1枚渡され、メンバーを選ぶことはできません。",
]))
blocks.append(capbox("参加方法", [
    ("①", "会場内のPOPのQRコード、または公式サイトトップのバナーからFANCLUB企画ページにアクセスし、「引き換えページはこちら」をタップ"),
    ("②", "引き換え画面が表示されたら、そのままFANCLUB BOOTHへ"),
    ("③", "スタッフの確認後、トレカをランダムで1枚プレゼント"),
]))
blocks.append(p([
    "<strong>対象となるのは会場に来た「月会費まとめて払いコース」会員で、当日そのコースに新規入会・コース変更した人も対象に含まれます。</strong>",
    "公演チケットを持っていない人でも参加できますが、<strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">参加できる回数は1人1日1回まで</span></strong>で、<strong>1日2公演がある日程でも1回までしか引き換えられません。</strong>",
]))
blocks.append(notebox('''<p style="margin:0;"><strong>参加にあたっての注意事項</strong><br>
・自分で引き換えボタンを押してしまい、FANCLUB BOOTHでの引き換え前に「引き換え完了」画面になっている場合、理由を問わず引き換えはできません。<br>
・当日の会場周辺の混雑状況や電波状況、ブースの終了時間によっては、企画への参加や特典の引き換えができないことがあります。</p>'''))

blocks.append(h2("新特典②KO1LYくじ(FC会員限定・コース不問)"))
blocks.append(minibox('<p style="margin:0;"><strong>対象:</strong>「KO1KEYZ OFFICIAL FANCLUB」会員(コース不問・チケット不要・当日入会でもOK)</p>'))
blocks.append(p([
    "2つ目の特典は、コースを問わずFC会員なら誰でも参加できる「KO1LYくじ」です。",
    "特賞は<strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">KO1KEYZメンバー全員によるお見送り会</span></strong>で、各日の終演後に実施されます(1日2公演がある会場は、第2部の終演後に実施)。",
]))
blocks.append(capbox("参加方法", [
    ("①", "会場内のPOPのQRコード、または公式サイトトップのバナーからFANCLUB企画ページにアクセスし、「くじを引く」をタップ"),
    ("②", "抽選結果を確認"),
    ("③", "当選画面が表示された場合のみ、FANCLUB BOOTHへ"),
]))
blocks.append(p([
    "はずれの場合は賞品がない代わりに、FANCLUB BOOTHへ足を運ぶ必要もありません。",
    "くじを引くだけなら誰でも気軽に挑戦できる企画になっています。",
]))

blocks.append(h2("チケットがなくても参加できる?"))
blocks.append(img_kuji_html)
blocks.append(p([
    "見出しの通り、FCトレカ・KO1LYくじのどちらも<strong>公演のチケットを持っていない人が参加できる</strong>企画です。",
    "実際にXでも、「チケットなくてもできるやつ」と、チケットを持っていなくてもFANCLUB BOOTHだけを目当てに参加できることに触れた投稿が見られました。",
    "ただし、参加には会場周辺にいることが条件になっており、公式からはスマートフォンの位置情報をあらかじめオンにしておくよう案内されています。",
    "遠方から参加できない人向けの救済ではなく、あくまで「会場には来るがチケットは持っていない」人向けの企画という位置づけです。",
]))

blocks.append(h2("CD予約抽選会との違いは?"))
blocks.append(p([
    "『2026 KO1KEYZ 1ST FAN MEETING』の会場では、今回のFANCLUB BOOTHとは別に、デビューシングル『KO1KEYZ』の3形態セットを予約すると参加できる<strong>CD予約抽選会</strong>も実施されます。",
    "こちらもチケット不要で参加でき、購入すれば必ずくじとトレカがもらえる仕組みですが、対象がFC会員限定のFANCLUB BOOTHとは異なり、CD予約抽選会は誰でも参加できます。",
    f"CD予約抽選会の詳しい参加方法・特典内容は<a href=\"{DEBUT_EVENTS_URL}\" target=\"_blank\" rel=\"noopener\">KO1KEYZデビュー記念イベントは？タワレコ&ファンミ抽選会</a>で紹介しているので、両方の特典を狙いたい人はあわせてチェックしてみてください。",
]))

blocks.append(h2("まとめ"))
blocks.append(notebox(f'''<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">KO1KEYZファンミFANCLUB BOOTHまとめ</p>
<p style="margin:0 0 10px 0;">
&#10003; <strong>FCトレカ</strong>:月会費まとめて払いコース限定、12種ランダム1枚、1人1日1回まで(1日2公演でも1回)<br>
&#10003; <strong>KO1LYくじ</strong>:FC会員ならコース不問で参加可、特賞はメンバー全員お見送り会<br>
&#10003; <strong>チケット</strong>:どちらも公演チケットは不要(会場近辺にいる必要あり、位置情報オンが条件)<br>
&#10003; <strong>実施会場</strong>:『2026 KO1KEYZ 1ST FAN MEETING』(東京公演8/21〜23・兵庫公演9/9〜10)
</p>
<p style="margin:0;">いよいよ今週末に開幕するファンミーティング、FC会員の人はぜひFANCLUB BOOTHもあわせてチェックしてみてください!</p>'''))

blocks.append(notebox(f'''<p style="margin:0 0 8px 0;"><strong>KO1KEYZについては、このブログの他の記事でも詳しく紹介しています。</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{DEBUT_EVENTS_URL}" target="_blank" rel="noopener">KO1KEYZデビュー記念イベントは？タワレコ&ファンミ抽選会</a></li>
<li><a href="{FANMEETING_PREDICT_URL}" target="_blank" rel="noopener">KO1KEYZのライブ・ファンミはいつ？ラポネ傾向から日程を大予想！</a></li>
<li><a href="{SCHEDULE_URL}" target="_blank" rel="noopener">KO1KEYZの今後のスケジュールは?8月〜10月デビューまでの日程</a></li>
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


SUMMARY = "8月21日開幕のKO1KEYZ 1STファンミでFANCLUB BOOTHが実施決定。FCトレカ・KO1LYくじの対象者や参加方法、チケットなしでも参加できるかをまとめました。"

if EXISTING_POST_ID:
    payload = {"title": title, "content": content, "status": "draft"}
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_POST_ID}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print("UPDATED POST_ID", post["id"])
else:
    slug = get_slug(title, "ko1keyz-fanmeeting-fanclub-booth")
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

# アイキャッチはKO1KEYZ統一テンプレ(文字入り、tools/eyecatch_koikeyz.pyで生成済み)を使う
if EXISTING_POST_ID:
    print("EYECATCH already set to", EXISTING_EYECATCH_MEDIA_ID, "(update run, skipping re-upload)")
else:
    eyecatch_path = ROOT / "images" / "ko1keyz_fanclub_booth_eyecatch.png"
    with open(eyecatch_path, "rb") as f:
        eyecatch_data = f.read()
    media_r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={
            **HEADERS_AUTH,
            "Content-Type": "image/png",
            "Content-Disposition": 'attachment; filename="ko1keyz_fanclub_booth_eyecatch.png"',
        },
        data=eyecatch_data,
    )
    media_r.raise_for_status()
    eyecatch_media = media_r.json()
    print("EYECATCH_MEDIA_ID", eyecatch_media["id"])

    featured_r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps({"featured_media": eyecatch_media["id"], "status": "draft"}).encode("utf-8"),
    )
    featured_r.raise_for_status()
    print("FEATURED_MEDIA set to", eyecatch_media["id"])

with open(ROOT / "tmp_ko1keyz_fanclub_booth_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
with open(ROOT / "tmp_ko1keyz_fanclub_booth_eyecatch_mediaid.txt", "w", encoding="utf-8") as f:
    f.write(str(EXISTING_EYECATCH_MEDIA_ID if EXISTING_POST_ID else eyecatch_media["id"]))
