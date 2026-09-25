# -*- coding: utf-8 -*-
"""Travis Japan 2027 tour venue prediction (Yokohama Arena opening + other arenas), chomoand-4.blog draft."""
import json, base64, os, re, sys, urllib.request, urllib.parse
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
WP_URL = ENV["WP_CHOMO4_URL"].rstrip("/")
WP_USER = ENV["WP_CHOMO4_USERNAME"]
WP_PASS = ENV["WP_CHOMO4_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

# ---------- group color palette (Travis Japan purple, per docs/rules.md) ----------
BORDER = "#d9cfee"
ACCENT = "#7e57c2"
BG = "#f5f2fb"
ZEBRA = "#faf8fd"

title = "トラジャ2027年ツアーも横アリ初日？会場を空き日程から予想！"


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def mark(text):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{text}</span></strong>'


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


def linkbox(box_title, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{box_title}</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


def checklist(items):
    lis = "\n".join(
        f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {ACCENT};border-radius:3px;color:{ACCENT};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{i}</p>'
        for i in items
    )
    return wphtml(f'''<div style="border:2px solid {ACCENT};border-radius:8px;background:{BG};padding:1em 1.25em;margin:0 0 16px 0;">
{lis}
</div>''')


def table(header, rows, highlight_rows=()):
    th = "\n".join(
        f'<td style="border:1px solid {BORDER};padding:8px 12px;background:{ACCENT};color:#fff;font-weight:bold;">{c}</td>'
        for c in header
    )
    trs = [f"<tr>\n{th}\n</tr>"]
    for i, row in enumerate(rows):
        if i in highlight_rows:
            cell_bg = "background:#fff6db;font-weight:bold;"
        elif i % 2 == 1:
            cell_bg = f"background:{ZEBRA};"
        else:
            cell_bg = ""
        cells = "\n".join(
            f'<td style="border:1px solid {BORDER};padding:8px 12px;{cell_bg}">{c}</td>' for c in row
        )
        trs.append(f"<tr>\n{cells}\n</tr>")
    body = "\n".join(trs)
    return f'<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n{body}\n</tbody></table></figure>\n<!-- /wp:table -->'


def gmap(q):
    return wphtml(
        f'<iframe src="https://maps.google.com/maps?q={urllib.parse.quote(q)}&t=&z=15&ie=UTF8&iwloc=&output=embed" '
        'width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>'
    )


# ---------- images: frames from official YouTube trailers (uploaded to WP media, see json) ----------
MEDIA = json.loads((ROOT / "articles" / "travis_japan_2027_tour_media.json").read_text(encoding="utf-8"))
YT_TEASER = "https://www.youtube.com/watch?v=FsUisvoVOik"
YT_STANDARD = "https://www.youtube.com/watch?v=HkzhJiV7TSQ"


def fig(key, src_url):
    m = MEDIA[key]
    (full, fw, fh), (large, lw, lh), (med, mw, mh) = m["full"], m["large"], m["medium"]
    return f'''<!-- wp:image {{"id":{m["id"]},"sizeSlug":"large"}} -->
<figure class="wp-block-image size-large"><img src="{large}" alt="{m["alt"]}" class="wp-image-{m["id"]}" width="{lw}" height="{lh}" style="max-width:100%;height:auto;" srcset="{med} {mw}w, {large} {lw}w, {full} {fw}w" sizes="(max-width: 1024px) 100vw, 1024px"/><figcaption style="font-size:0.8em;color:#888;">出典:{src_url}</figcaption></figure>
<!-- /wp:image -->'''


# ---------- other-venue section (filled from official venue schedules) ----------
from venue_section_2027 import venue_blocks  # noqa: E402  (generated alongside this script)

blocks = []

blocks.append(p([
    "Travis Japanの全国アリーナツアーは、2024年・2025年・2026年と<strong>3年連続で「1月4日の横浜アリーナ」から幕を開けています</strong>。",
    "11月18日に4thアルバム「Jewelry Basket」の発売を控え、次のツアーも年明けの横アリから始まるのか気になっているファンも多いのではないでしょうか。",
    "そこで横浜アリーナの公式スケジュールを確認してみたところ、<strong>2027年1月1日〜10日はまだ1件も予定が入っていない</strong>ことが分かりました。",
    "この記事では、過去3年のツアー会場と各会場の空き日程から、2027年ツアーの会場と日程、発表時期を予想していきます。",
]))

blocks.append(whatbox([
    "過去3年のアリーナツアー会場一覧",
    "3年連続「1月4日・横浜アリーナ」スタートの流れ",
    "2027年1月の横浜アリーナの空き状況",
    "ほかの常連会場の空き状況",
    "ツアー発表はいつ頃になりそうか",
    "横浜アリーナへのアクセス",
]))

# ---- history table ----
blocks.append(h2("【一覧】トラジャの歴代アリーナツアー会場(2024〜2026年)"))
blocks.append(p([
    "まずは、1stアルバム以降の3回のアリーナツアーで回った会場を並べてみます。",
    "どの年も8会場を回っていて、そのうち半分以上は毎年のように使われている常連会場でした。",
]))
blocks.append(table(
    ["会場", "2024年", "2025年", "2026年"],
    [
        ["横浜アリーナ(神奈川)", "1/4〜6", "1/4〜7", "1/4〜7"],
        ["大阪城ホール(大阪)", "2/21〜23", "5/4〜6", "3/27〜28"],
        ["マリンメッセ福岡A館(福岡)", "2/10〜11", "3/29〜30", "5/5〜6"],
        ["エコパアリーナ(静岡)", "3/9〜10", "4/5〜6", "4/25〜26"],
        ["日本ガイシホール(愛知)<br>※現・クロコくんホール", "1/17〜18", "―", "3/11〜12"],
        ["Aichi Sky Expo(愛知)", "―", "2/8〜9", "―"],
        ["セキスイハイムスーパーアリーナ(宮城)", "1/27〜28", "3/15〜16", "―"],
        ["真駒内セキスイハイムアイスアリーナ(北海道)", "3/23〜24", "5/31〜6/1", "―"],
        ["北海きたえーる(北海道)", "―", "―", "2/21〜22"],
        ["ららアリーナ 東京ベイ(千葉)", "―", "6/7〜8", "5/22〜24"],
        ["朱鷺メッセ(新潟)", "1/13〜14", "―", "―"],
        ["サンドーム福井(福井)", "―", "―", "2/7〜8"],
    ],
    highlight_rows=(0,),
))
blocks.append(p([
    "ツアー名は2024年が「Road to Authenticity」、2025年が「VIIsual」、2026年が「's travelers」で、いずれも前年12月に出たアルバムを引っ提げたツアーでした。",
    "横浜アリーナ・大阪城ホール・マリンメッセ福岡・エコパアリーナの4会場は3年すべてに登場していて、トラジャの“ホーム”と呼べる顔ぶれです。",
    "一方で、愛知はガイシホールとAichi Sky Expo、北海道は真駒内ときたえーるのように、同じ地域でも年によって会場が入れ替わっています。",
    "新潟・宮城・福井のように、年によって回ったり回らなかったりする地域があるのもポイントです。",
]))
blocks.append(fig("out_center_stage", YT_TEASER))
blocks.append(p([
    "こちらは2026年の「's travelers」の横浜アリーナ公演で、アリーナの真ん中に置かれた円形のセンターステージに7人が並んだ場面です。",
    "1万人を超える大きな会場でも、客席のすぐ近くまでステージが張り出す演出を楽しめるのも、トラジャのアリーナツアーならではといえます。",
]))

# ---- Yokohama pattern ----
blocks.append(h2("3年連続で「1月4日・横浜アリーナ」から開幕"))
blocks.append(minibox([
    ("初日", "2024年・2025年・2026年とも1月4日"),
    ("会場", "横浜アリーナ(3〜4日間)"),
    ("設営", "毎年1月1日〜3日(2026年は前年12月27日から)"),
]))
blocks.append(p([
    "トラジャのツアーでいちばん分かりやすい法則が、<strong>初日が毎年「1月4日の横浜アリーナ」</strong>という点です。",
    "横浜アリーナの公式サイトには過去のイベントの設営日まで残っていて、それを見ると3年とも1月1日〜3日が設営日になっていました。",
    "2026年はさらに早く、前年の12月27日から準備に入っていたようです。",
    "元日から会場を押さえてセットを組み、三が日明けの4日に開幕するのが、トラジャのツアーの定番の流れになっています。",
]))
blocks.append(fig("out_yokoari_audience", YT_TEASER))
blocks.append(p([
    "2026年1月の横浜アリーナ公演では、スタンド席の上のほうまでペンライトの光で埋め尽くされていました。",
    "この横アリ公演はBlu-ray・DVD「Travis Japan Concert Tour 2026 's travelers」(2026年8月26日発売)に収録されていて、公式YouTubeのティザー映像でも会場の熱気を見ることができます。",
]))
blocks.append(p([
    "2025年の「VIIsual」と2026年の「's travelers」は、どちらも1月4日〜7日の4日間でした。",
    "年明けの横アリはお正月休みと重なるので、遠方から遠征しやすいのもうれしいところです。",
]))

# ---- Yokohama 2027 availability ----
blocks.append(h2("2027年1月の横浜アリーナの空き状況は？"))
blocks.append(minibox([
    ("1月1日〜10日", "予定なし(空き)"),
    ("1月11日", "横浜市 二十歳の市民を祝うつどい"),
    ("確認日", "2026年9月25日時点の横浜アリーナ公式イベントカレンダー"),
]))
blocks.append(p([
    "では、肝心の2027年1月はどうなっているのでしょうか。",
    "横浜アリーナの公式イベントカレンダーで2026年12月〜2027年2月を調べてみると、次のような予定が入っていました。",
]))
blocks.append(table(
    ["日付", "予定"],
    [
        ["2026年12月25日〜27日", "桑田佳祐の公演の設営"],
        ["2026年12月28日・30日・31日", "桑田佳祐 夏祭りツアー 2026"],
        ["2027年1月1日〜10日", "予定なし"],
        ["2027年1月11日", "横浜市 二十歳の市民を祝うつどい"],
        ["2027年1月23日", "FRUITS ZIPPERのオールナイトニッポンX in 横浜アリーナ"],
        ["2027年1月30日・31日", "WayV CONCERT TOUR"],
        ["2027年2月20日・21日", "GLAY ARENA TOUR"],
    ],
    highlight_rows=(2,),
))
blocks.append(p([
    f"表を見ると分かるように、{mark('2027年1月1日から10日までは、まるごと予定が入っていません')}。",
    "過去3年と同じ「1月1日〜3日に設営、4日〜7日に公演」という組み方なら、そっくりそのまま収まる空き方です。",
    "11日には毎年恒例の横浜市の二十歳のつどいが入っているので、その手前で公演を終える日程とも矛盾しません。",
]))
blocks.append(p([
    "ちなみに2026年のツアーでは年末の12月27日から設営していましたが、2027年は12月31日まで桑田佳祐の公演が入っています。",
    "そのため、もし横アリで開幕するなら、2024年・2025年と同じく元日からの設営になりそうです。",
]))
blocks.append(p([
    "ただし、公式カレンダーに載るのは主催者から情報が届いたイベントだけです。",
    "まだ発表前のツアーは載っていないことも多いため、「空いている=何も入らない」とは限りません。",
    "逆にいえば、トラジャのツアーが発表されれば、この1月上旬の空白に入ってくる可能性は十分ありそうです。",
]))
blocks.append(gmap("横浜アリーナ"))

# ---- other venues ----
blocks.extend(venue_blocks(p=p, h2=h2, h3=h3, minibox=minibox, table=table, mark=mark, fig=lambda k: fig(k, YT_STANDARD)))

# ---- announcement timing ----
blocks.append(h2("ツアー発表はいつ？デビュー記念日の10月28日前後が濃厚"))
blocks.append(minibox([
    ("過去の発表日", "2023年10月28日・2024年10月28日・2025年10月30日"),
    ("2026年の予想", "10月28日(デビュー4周年)前後"),
]))
blocks.append(p([
    "過去3回のツアーは、いずれも前年の10月下旬に開催が発表されています。",
]))
blocks.append(table(
    ["ツアー", "発表日", "アルバム発売日", "初日"],
    [
        ["2024 Road to Authenticity", "2023年10月28日", "2023年12月20日", "2024年1月4日"],
        ["2025 VIIsual", "2024年10月28日", "2024年12月4日", "2025年1月4日"],
        ["2026 's travelers", "2025年10月30日", "2025年12月1日", "2026年1月4日"],
        ["2027(未発表)", "?", "2026年11月18日", "?"],
    ],
    highlight_rows=(3,),
))
blocks.append(p([
    "10月28日はTravis Japanが2022年に世界デビューした記念日です。",
    "2023年と2024年はまさにその当日、2025年も2日後の10月30日に発表されていて、<strong>デビュー記念日に合わせて次のツアーを告知するのが恒例</strong>になっています。",
    "2026年の10月28日はデビュー4周年にあたるため、この日前後に2027年ツアーの発表があるのではないかと期待が高まっています。",
]))
blocks.append(p([
    "もう1つ注目したいのが、アルバムの発売時期です。",
    "これまでは12月発売のアルバムから約1カ月後の1月4日に初日を迎えていましたが、4thアルバム「Jewelry Basket」は例年より少し早い11月18日発売となっています。",
    "アルバムからツアーまでの流れが例年どおりなら、年明けの横アリ開幕というスケジュールにも十分間に合いそうです。",
    "今回のアルバムは吉澤閑也がプロデュースを担当しており、過去のツアーと同じようにツアーの演出にも吉澤のカラーが出るのか楽しみなところです。",
]))

# ---- access ----
blocks.append(h2("横浜アリーナへのアクセスは？"))
blocks.append(minibox([
    ("住所", "神奈川県横浜市港北区新横浜3-10"),
    ("最寄り駅", "新横浜駅(JR・新幹線・地下鉄ブルーライン・相鉄・東急)"),
    ("駐車場", "なし(車での来場は控えるよう案内あり)"),
]))
blocks.append(p([
    "横浜アリーナの最寄りは新横浜駅で、どの路線からでも歩いて5分ほどで着きます。",
    "横浜市営地下鉄ブルーライン・相鉄新横浜線・東急新横浜線は出口7・8から徒歩4分、JR横浜線は北口から、東海道新幹線は東口からそれぞれ徒歩5分です。",
    "新幹線の駅から歩いて行けるので、大阪・名古屋方面からの遠征でも乗り換えなしで向かえるのが便利なところでしょう。",
]))
blocks.append(p([
    "注意したいのは、会場に駐車場も駐輪場もないことです。",
    "公式サイトでも車での来場は控えるよう案内されているので、基本は電車で向かうことになります。",
    "終演後は新横浜駅が大混雑するため、帰りの新幹線は時間に余裕を持って取っておくと安心です。",
]))

# ---- summary ----
blocks.append(h2("まとめ"))
blocks.append(checklist([
    "トラジャのアリーナツアーは2024〜2026年の3年連続で1月4日の横浜アリーナから開幕",
    "毎年1月1日〜3日を設営日にして、4日に初日を迎えるのが定番",
    "2027年1月の横浜アリーナは1日〜10日がまだ空き(2026年9月25日時点)",
    "横アリ・大阪城ホール・マリンメッセ福岡・エコパアリーナは3年連続で使われた常連会場",
    "ツアー発表は例年デビュー記念日の10月28日前後",
    "4thアルバム「Jewelry Basket」は2026年11月18日発売",
]))
blocks.append(p([
    "ここまでの流れがそのまま続くなら、2027年も元日明けの横浜アリーナでトラジャに会えるかもしれません。",
    "10月28日前後の発表に備えて、今のうちからお正月の予定を空けておくのもよさそうです！",
]))
blocks.append(linkbox("あわせて読みたい", [
    '<a href="https://chomoand-4.blog/is-toraja-concert-produced-by-214">トラジャのアルバム・コンサートは毎年違うメンバーがプロデュース？</a>',
    '<a href="https://chomoand-4.blog/what-is-koropen-penlight-color-change-597">「コロペン」とは？ペンライトの色を変える意味を解説！</a>',
    '<a href="https://chomoand-4.blog/starto-countdown-concert-2027-705">STARTOカウコン2027年男は誰？Netflix世界配信決定！</a>',
]))

content = "\n\n".join(blocks)

if "--dry" in sys.argv:
    out = ROOT / "articles" / "travis_japan_2027_tour_venue_prediction.html"
    out.write_text(content, encoding="utf-8")
    text = re.sub(r"<[^>]+>", "", content)
    text = re.sub(r"\s+", "", text)
    print("title chars:", len(title))
    print("body chars:", len(text))
    print("saved:", out)
    sys.exit(0)


# ---------- slug (hand-picked for the target keywords instead of machine translation) ----------
slug = "travis-japan-2027-tour-venue-prediction"
print("slug:", slug)

payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": "draft",
    "categories": [3],
    "author": 2,
}

# Draft already exists (post 926): later runs only refresh the body so title/slug never get re-sent.
EXISTING_POST_ID = 926
if EXISTING_POST_ID:
    payload = {"content": content}

r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts" + (f"/{EXISTING_POST_ID}" if EXISTING_POST_ID else ""),
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"])
print("SLUG", post["slug"])
print("PREVIEW", f"{WP_URL}/?p={post['id']}")
