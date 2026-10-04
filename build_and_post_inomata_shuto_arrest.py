# -*- coding: utf-8 -*-
"""猪俣周杜 傷害容疑で逮捕(TV報道)速報記事 -> chomoand.com 下書き投稿.

確認できていない事実(日時・場所・経緯・認否・事務所コメント)は本文に書かない。
続報が入ったらこのスクリプトの本文を更新して再投稿する(下書きIDを EXISTING_POST_ID に入れる)。
"""
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
WP_URL = ENV["WP_TREND_URL"].rstrip("/")
WP_USER = ENV["WP_TREND_USERNAME"]
WP_PASS = ENV["WP_TREND_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

ACCENT = "#546e7a"
ACCENT_BG = "#f3f6f8"

EXISTING_POST_ID = None  # 2回目以降の更新時に下書きIDを入れる
EYECATCH_PATH = ROOT / "images" / "inomata_shuto_arrest_eyecatch.png"

title = "猪俣周杜が傷害容疑で逮捕？何があった？【速報】"


def p(sentences):
    body = "<br>\n".join(sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def table(rows):
    trs = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;width:150px;"><strong>{k}</strong></td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return (
        '<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n'
        f"{trs}\n</tbody></table></figure>\n<!-- /wp:table -->"
    )


def box(ttl, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(
        f'<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{ACCENT_BG};">\n{lis}\n</ul>\n</div>'
    )


blocks = []

blocks.append(p([
    "timeleszの猪俣周杜さんが、傷害の疑いで逮捕されたとテレビのニュースで報じられました。",
    "本記事は、この報道を受けて速報としてお伝えするものです。",
]))
blocks.append(p([
    "現時点では、ネット上の報道や公式発表がまだ出そろっておらず、事実関係の詳細は確認できていません。",
    "確認できた情報から順に追記していきます。",
]))

blocks.append(box("この記事でわかること", [
    "猪俣周杜さんの逮捕報道について、現時点で言えること・言えないこと",
    "猪俣周杜さんのプロフィールと、timeleszでの活動",
    "「傷害」とはどんな罪か、逮捕後の一般的な流れ",
    "続報を確認するときの注意点",
]))

blocks.append(h2("猪俣周杜さんは何があった？報道の内容"))
blocks.append(table([
    ("報じられた内容", "傷害の疑いで逮捕されたとテレビのニュースで報道"),
    ("公式発表", "所属事務所・警察の発表は確認できていません(2026年9月19日時点)"),
    ("詳細", "日時・場所・経緯・認否などは現時点で確認できていません"),
]))
blocks.append(p([
    "逮捕を報じたのはテレビのニュースで、報道の時点ではインターネット上のニュース記事や公式サイトの発表を確認できていません。",
    "そのため、事件の日時や場所、経緯、相手の状況、本人が容疑を認めているかどうかといった点は、いまのところ分かっていません。",
    "確かな情報が出るまでは、SNSの書き込みや憶測を事実として扱わないことが大切です。",
]))
blocks.append(p([
    "なお、猪俣さんは2026年1月期のドラマ『東京P.D. 警視庁広報2係』で犯人役を演じていました。",
    "今回のニュースは、ドラマの役柄とは別の話です。",
    "役の話と混同して広まらないよう、注意して情報を確認してください。",
]))

blocks.append(h2("猪俣周杜さんのプロフィール・timeleszでの活動"))
blocks.append(table([
    ("名前", "猪俣周杜(いのまた しゅうと)"),
    ("生年月日", "2001年8月17日"),
    ("所属グループ", "timelesz"),
    ("加入", "2025年、オーディション「timelesz project」を経て加入した新メンバーの1人"),
]))
blocks.append(p([
    "猪俣周杜さんは、timeleszが新メンバーを募集したオーディション「timelesz project」を経て2025年にグループへ加入しました。",
    "加入後は音楽活動やバラエティー番組に出演し、2026年にはドラマにも出演するなど、活動の幅を広げていました。",
]))

blocks.append(h2("「傷害」とはどんな罪？逮捕後の一般的な流れ"))
blocks.append(p([
    "傷害罪(刑法204条)は、他人の身体に傷害を負わせた場合に問われる罪で、法定刑は15年以下の懲役または50万円以下の罰金です。",
    "相手にけがをさせるに至らなかった場合は、傷害ではなく暴行罪(刑法208条)になります。",
    "今回「傷害」の疑いと報じられているのは、相手にけがを負わせた疑いを指すと考えられます。",
]))
blocks.append(p([
    "逮捕されたあとの一般的な流れは次のとおりです。",
    "警察は逮捕から48時間以内に、事件を検察官に送ります(送検)。",
    "検察官は送検から24時間以内に、裁判官へ勾留を請求するかどうかを判断します。",
    "勾留が認められると、原則10日間、延長を含めて最長20日間、身柄が拘束されます。",
    "その間に検察官が、起訴するか、不起訴にするかを決めます。",
]))
blocks.append(box("知っておきたい注意点", [
    "逮捕は「罪を犯した疑いがある」という段階で、有罪が確定したわけではありません",
    "起訴されるかどうか、どのような処分になるかは、今後の捜査で決まります",
    "被害を受けた方がいる可能性があるため、憶測や誹謗中傷はやめましょう",
]))

blocks.append(h2("今後の見通しと続報の確認方法"))
blocks.append(p([
    "所属事務所やtimeleszの公式サイトから、コメントや今後の活動についての発表が出る可能性があります。",
    "グループの活動やテレビ・ラジオ・ライブなどへの影響も、現時点では分かっていません。",
    "この記事では、公式の発表や大手報道機関の続報を確認できしだい、内容を更新します。",
]))
blocks.append(p([
    "続報を確認するときは、事務所・警察・大手報道機関など、出どころがはっきりした情報を優先してください。",
]))

blocks.append(h2("まとめ"))
blocks.append(box("この記事のまとめ", [
    "timeleszの猪俣周杜さんが、傷害の疑いで逮捕されたとテレビのニュースで報じられた",
    "所属事務所・警察の公式発表や、日時・場所・経緯などの詳細は、現時点で確認できていない",
    "逮捕は有罪の確定ではなく、今後の捜査・処分を見守る必要がある",
    "続報が入りしだい、この記事を更新する",
]))

content = "\n\n".join(blocks)


def get_slug(title_text):
    url = (
        "https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q="
        + urllib.parse.quote(title_text)
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    en = "".join(seg[0] for seg in data[0])
    slug = re.sub(r"[^a-z0-9\s-]", "", en.lower())
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)[:30].rstrip("-")
    return slug


try:
    slug = get_slug(title)
except Exception as e:
    print("slug translate failed, fallback:", e)
    slug = "shuto-inomata-arrested-breaking"
print("slug:", slug)

# upload eyecatch
with open(EYECATCH_PATH, "rb") as f:
    img = f.read()
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/media",
    headers={
        **HEADERS_AUTH,
        "Content-Type": "image/png",
        "Content-Disposition": 'attachment; filename="inomata_shuto_arrest_eyecatch.png"',
    },
    data=img,
)
r.raise_for_status()
media_id = r.json()["id"]
print("EYECATCH_MEDIA_ID", media_id)

payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": "draft",
    "categories": [37],
    "author": 4,
    "featured_media": media_id,
}
endpoint = f"{WP_URL}/wp-json/wp/v2/posts" + (f"/{EXISTING_POST_ID}" if EXISTING_POST_ID else "")
r = requests.post(
    endpoint,
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"])
print("SLUG", post["slug"])
print("STATUS", post["status"])
print("PREVIEW", f"{WP_URL}/?p={post['id']}")
