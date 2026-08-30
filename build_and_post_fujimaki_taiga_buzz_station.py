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


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


ACCENT = "#8a8378"   # KO1KEYZ非メンバー(日プ新世界)記事のニュートラルなウォームグレー
BORDER = "#ddd9d3"
BG = "#f7f6f4"
TDBG = "#f3f1ee"


def infotable(ttl, rows):
    tds = "\n".join(
        f'<tr><td style="background:{TDBG};border:1px solid {BORDER};padding:8px 12px;width:32%;">{k}</td>'
        f'<td style="border:1px solid {BORDER};padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{ttl}</p>
<table style="border-collapse:collapse;width:100%;">
{tds}
</table>
</div>''')


def whatbox(ttl, items):
    lis = "\n".join(f'<li style="margin:0 0 8px 0;">{t}</li>' for t in items[:-1])
    lis += f'\n<li style="margin:0;">{items[-1]}</li>'
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def mk(cls, text):
    return f'<span class="swl-marker {cls}">{text}</span>'


def mkstrong(cls, text):
    return f'<strong><span class="swl-marker {cls}" style="font-size:1.15em;">{text}</span></strong>'


PRTIMES_URL = "https://prtimes.jp/main/html/rd/p/000000533.000141380.html"
ZENSE_URL = "https://chomoand-1.com/produce101japanshinsekai_zense-2748"
MATOME8_URL = "https://chomoand-1.com/produce101japanshinsekai_8matome-8577"
RECIPE_URL = "https://chomoand-1.com/produce101japan_ryourirecipi-8604"

title = "藤牧大雅がBUZZ STATIONにゲスト出演！日時や聴き方は？"

blocks = []

blocks.append(p([
    "『PRODUCE 101 JAPAN 新世界』(日プ新世界)に出演した藤牧大雅さんが、よゐこ・濱口優さんがパーソナリティを務めるラジオ番組「濱口優のBUZZ STATION」にゲスト出演することが発表されました。",
    "出演回は<strong>2026年9月18日(金)18:00〜18:50</strong>で、渋谷の公開スタジオからの生放送です。",
    "この記事では、放送の日時と聴き方、「BUZZ STATION」がどんな番組なのか、そして藤牧大雅さんのこれまでの経歴と直近のファンミーティング情報まで整理します。",
]))

blocks.append(infotable("藤牧大雅ゲスト出演回の基本情報", [
    ("番組名", "濱口優のBUZZ STATION"),
    ("放送日時", "2026年9月18日(金)18:00〜18:50"),
    ("放送局", "Shibuya Cross-FM(渋谷クロスFM)93.8MHz"),
    ("パーソナリティ", "濱口優(よゐこ)"),
    ("形式", "渋谷の公開スタジオからの生放送"),
]))

blocks.append(h2("藤牧大雅の「BUZZ STATION」ゲスト出演が決定"))
blocks.append(p([
    "株式会社BUZZ GROUPからのプレスリリースで、藤牧大雅さんが「濱口優のBUZZ STATION」9月放送回にゲスト出演することが明らかになりました。",
    "発表では「虹プロ2・ボイプラ2・日プ新世界を駆け抜けた藤牧大雅が登場」と紹介されており、複数のオーディション番組を経験してきた実力派としての出演です。",
    "番組では、<strong>これまでのオーディションで培った経験、アーティストとしての現在地、そしてこれからの挑戦</strong>について、本人の言葉で語られる予定とされています。",
]))
blocks.append(p([
    "日プ新世界の放送終了後は、SNSやライブ配信を中心に活動してきた藤牧大雅さんにとって、ラジオ番組へのゲスト出演は貴重な機会です。",
    "オーディションでのパフォーマンスだけでなく、素のトークやこれからの目標がじっくり聞けるのは、ファンにとって見逃せないところと言えます。",
    f'発表の詳細は<a href="{PRTIMES_URL}" target="_blank" rel="noopener">PR TIMESのプレスリリース</a>で確認できます。',
]))

blocks.append(h2("「BUZZ STATION」ってどんな番組？"))
blocks.append(p([
    "「濱口優のBUZZ STATION」は、2026年4月3日にスタートしたラジオ番組です。",
    "よゐこの濱口優さんがパーソナリティを務め、「ラジオを聴く」から「ラジオを体験する」新しいエンタメをコンセプトに掲げています。",
    "放送は毎月第1・第3金曜日の18:00〜18:50で、Shibuya Cross-FMの公開スタジオから生放送されています。",
]))
blocks.append(minibox('''<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">濱口優のBUZZ STATIONとは？</p>
<p style="margin:0;">Shibuya Cross-FM(93.8MHz)で放送中のラジオ番組。<br>
毎月第1・第3金曜18:00〜18:50に、渋谷の公開スタジオから濱口優(よゐこ)がパーソナリティとして生放送でお届けする。<br>
出演を希望するアーティストを随時募集しており、これまでにUNIVER23、NeoStellaといったグループがゲスト出演している。</p>'''))
blocks.append(p([
    "公開スタジオからの生放送のため、スタジオの様子を見に行けば、濱口優さんやゲストと同じ空間でラジオ収録の臨場感を体感できるのも特徴です。",
    "藤牧大雅さんの出演回も同じ形式で放送されるとみられます。",
]))

blocks.append(h2("放送はいつ？聴き方は？"))
blocks.append(p([
    "藤牧大雅さんのゲスト出演回は、" + mkstrong("mark_yellow", "2026年9月18日(金)18:00〜18:50") + "の放送です。",
    "Shibuya Cross-FMは、渋谷・神南エリアを中心にカバーするミニFM局で、周波数は93.8MHz。",
    "電波が届くのはスタジオ周辺のみのため、エリア外の人はインターネット配信で聴くことになります。",
]))
blocks.append(whatbox("BUZZ STATIONの聴き方", [
    "渋谷・神南周辺:FMラジオを93.8MHzに合わせる",
    "エリア外:Shibuya Cross-FM公式サイト(shibuyacrossfm.jp)の映像付きストリーミングで視聴",
    "radiko(ラジコ)には非対応のため、アプリからは聴けない",
    "聞き逃した場合は、YouTubeのアーカイブ動画で後追い視聴できることがある",
]))
blocks.append(p([
    "放送直前や当日は、番組公式X・Shibuya Cross-FM公式サイトで最新の配信リンクや進行時間が案内されるので、そちらをチェックしておくと確実です。",
    "生放送なので、リアルタイムで聴くと番組へのメッセージが読まれる可能性もあります。",
]))

blocks.append(h2("藤牧大雅ってどんな人？"))
blocks.append(p([
    "藤牧大雅(ふじまき たいが)さんは、数々のオーディション番組に挑戦し続けてきた練習生です。",
    "JYPの練習生として約4年半を過ごしたのち、日本と韓国のサバイバル番組に立て続けに参加してきました。",
]))
blocks.append(infotable("藤牧大雅 プロフィール", [
    ("名前", "藤牧大雅(ふじまき たいが)"),
    ("生年月日", "2005年5月17日"),
    ("出身地", "東京都"),
    ("身長", "181cm"),
    ("特技", "作詞、ラップ、ダンス"),
    ("趣味", "ギター、筋トレ"),
]))
blocks.append(p([
    "オーディション歴は非常に豊富です。",
    "『Nizi Project Season 2』(虹プロ2)では韓国合宿まで進出し、続く『BOYS II PLANET』(ボイプラ2)では最終順位65位という結果でした。",
    "そして2026年放送の『PRODUCE 101 JAPAN 新世界』では" + mk("mark_yellow", "最終順位42位・Aクラス") + "まで勝ち上がり、第8話で惜しくも脱落。デビューグループ「KO1KEYZ(コイキーズ)」入りはなりませんでした。",
    f'日プ新世界での戦いぶりは<a href="{MATOME8_URL}" target="_blank" rel="noopener">第8話まとめ記事</a>や<a href="{ZENSE_URL}" target="_blank" rel="noopener">練習生の前世一覧</a>でも触れています。',
]))
blocks.append(p([
    "数えきれないほどのオーディションを経てもなお挑戦を続ける姿勢から、ファンの間では「不屈の挑戦者」と呼ばれています。",
    "ラップや作詞のスキルは高く評価されており、韓国語・中国語も話せるマルチな一面も持っています。",
]))

blocks.append(h2("9月3日には自費・無料のファンミーティングも"))
blocks.append(p([
    "ラジオ出演に先立ち、藤牧大雅さんは2026年9月3日(木)18:30から、東京・有楽町のヒューリックホール東京で初のファンミーティングを開催します。",
    "注目されているのは、このイベントが" + mkstrong("mark_yellow", "本人の貯金による自費開催・入場無料") + "だという点です。",
    "虹プロ2の脱落後からボイプラ2に出るまでの間にアルバイトで貯めたお金を使い、会場費などの経費を自分で計算したうえで企画したことを明かしています。",
]))
blocks.append(p([
    "パフォーマンスの構成まで一人で計画を立て、家族の許可も得たうえでの開催とのこと。",
    "チケットの予約受付はすでに始まっており、本人のInstagram(@taiga17517)のプロフィール欄のリンクから申し込めます。",
    "ファンミーティングで直接会い、その2週間後にはラジオでトークを聴く、という流れを楽しめる9月になりそうです。",
]))

blocks.append(h2("まとめ"))
blocks.append(wphtml(f'''<div style="border:2px solid {ACCENT};border-radius:8px;background:rgba(138,131,120,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; 藤牧大雅が「濱口優のBUZZ STATION」9月放送回にゲスト出演<br>
&#10003; 放送は2026年9月18日(金)18:00〜18:50、Shibuya Cross-FM(93.8MHz)<br>
&#10003; エリア外は公式サイトの映像付き配信で視聴、radikoは非対応<br>
&#10003; 番組ではオーディションで培った経験やこれからの挑戦を語る予定<br>
&#10003; 9月3日にはヒューリックホール東京で自費・無料のファンミーティングも開催
</p>
</div>'''))
blocks.append(p([
    "日プ新世界でデビューは逃したものの、藤牧大雅さんの活動はむしろここから本格化していきそうです。",
    "ラジオでどんな言葉が飛び出すのか、放送日を楽しみに待ちたいですね！",
]))
blocks.append(wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">日プ新世界の関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{ZENSE_URL}" target="_blank" rel="noopener">【日プ新世界】練習生の前世一覧！元K-POPアイドルや経歴を徹底調査！</a></li>
<li><a href="{MATOME8_URL}" target="_blank" rel="noopener">【日プ新世界】第8話まとめ｜コンセプト評価・KCON・第2回順位発表式結果！</a></li>
<li><a href="{RECIPE_URL}" target="_blank" rel="noopener">【日プ新世界】練習生が作った料理のレシピまとめ！意外な料理男子も判明！</a></li>
</ul>
</div>'''))

content = "\n\n".join(blocks)
plain_len = len(re.sub(r"<[^>]+>|<!--.*?-->", "", content))
print("content length (chars):", plain_len)
print("title length:", len(title))


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


SUMMARY = ("日プ新世界に出演した藤牧大雅が、よゐこ・濱口優のラジオ番組「濱口優のBUZZ STATION」に"
           "ゲスト出演。放送は2026年9月18日(金)18時からShibuya Cross-FM。聴き方や本人の経歴、"
           "9月3日の自費・無料ファンミ情報もまとめました。")

slug = get_slug(title, "fujimaki-taiga-buzz-station")
print("slug:", slug)
payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": "draft",
    "categories": [4],
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

EYECATCH_PATH = ROOT / "images" / "fujimaki_taiga_buzz_station_eyecatch.png"
subprocess.run([
    sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
    "--top", "日プ新世界 藤牧大雅",
    "--main", "BUZZ STATION",
    "--bottom", "ラジオにゲスト出演！",
    "--out", str(EYECATCH_PATH),
    "--seed", str(post["id"]),
], check=True)

media2 = requests.post(
    f"{WP_URL}/wp-json/wp/v2/media",
    headers={
        **HEADERS_AUTH,
        "Content-Type": "image/png",
        "Content-Disposition": 'attachment; filename="fujimaki_taiga_buzz_station_eyecatch.png"',
    },
    data=EYECATCH_PATH.read_bytes(),
)
media2.raise_for_status()
EYECATCH_MEDIA_ID = media2.json()["id"]
print("EYECATCH_MEDIA_ID", EYECATCH_MEDIA_ID)

featured_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"featured_media": EYECATCH_MEDIA_ID, "status": "draft"}).encode("utf-8"),
)
featured_r.raise_for_status()
print("FEATURED_MEDIA set to", EYECATCH_MEDIA_ID)

(ROOT / "tmp_fujimaki_taiga_buzz_station_postid.txt").write_text(str(post["id"]), encoding="utf-8")
(ROOT / "tmp_fujimaki_taiga_buzz_station_eyecatch_mediaid.txt").write_text(str(EYECATCH_MEDIA_ID), encoding="utf-8")
(ROOT / "tmp_fujimaki_taiga_buzz_station_slug.txt").write_text(post["slug"], encoding="utf-8")
