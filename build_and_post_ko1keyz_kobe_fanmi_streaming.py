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


def titlebox(ttl, items, ordered=False):
    tag = "ol" if ordered else "ul"
    lis = "\n".join(f"<li>{t}</li>" for t in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<{tag} style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</{tag}>
</div>''')


def minibox(html_body):
    return wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f7f7;">
{html_body}
</div>''')


def notebox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def wptable(headers, rows):
    thead = "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;font-weight:bold;">{h}</td>' for h in headers)
    trs = "\n".join(
        "<tr>" + "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;">{c}</td>' for c in row) + "</tr>"
        for row in rows
    )
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr>{thead}</tr>
{trs}
</tbody></table></figure>
<!-- /wp:table -->'''


OFFICIAL_NEWS = "https://ko1keyz.com/news/detail/99"
VENUE_URL = "https://chomoand-1.com/ko1keyz-fan-meeting-10421"
DAY1_URL = "https://chomoand-1.com/ko1keyz1st-fan-meeting-tokyo-f-11644"
CAMERA_URL = "https://chomoand-1.com/is-there-a-camera-on-ko1keyz1s-11729"
LEMINO_URL = "https://chomoand-1.com/ko1keyz-new-program-will-be-di-11311"
SCHEDULE_URL = "https://chomoand-1.com/what-is-ko1keyzs-future-schedu-10860"

title = "コイキーズ神戸ファンミが生配信決定！視聴方法は？"

blocks = []

blocks.append(p([
    "2026年9月3日、KO1KEYZ(コイキーズ)の公式Xと公式サイトで、初のファンミーティング『2026 KO1KEYZ 1ST FAN MEETING』の<strong>兵庫公演を全世界に生配信する</strong>ことが発表されました。",
    "配信されるのは<strong>兵庫2日目・夜公演の1公演のみ</strong>で、日時は<strong>2026年9月10日(木)18:30(JST)</strong>から。アーカイブ(見逃し)配信はありません。",
    "この記事では、生配信されるのがどの公演なのか、視聴チケットの料金と販売期間、購入から視聴までの流れ、アーカイブや円盤化の見通しまで整理して紹介します。",
]))

blocks.append(titlebox("この記事でわかること", [
    "生配信されるのはどの公演か",
    "配信日時と視聴チケットの料金",
    "チケットの販売期間と視聴までの流れ",
    "アーカイブ配信・円盤化の有無",
]))

blocks.append(h2("生配信されるのは兵庫2日目・夜公演のみ"))
blocks.append(minibox('<p style="margin:0;"><strong>配信対象:</strong>兵庫(神戸ワールド記念ホール)2日目・夜公演</p>\n<p style="margin:4px 0 0 0;"><strong>配信日時:</strong>2026年9月10日(木)18:30(6:30pm)JST〜 ※夜公演の開演と同時にスタート</p>'))
blocks.append(p([
    "『2026 KO1KEYZ 1ST FAN MEETING』の兵庫公演は、神戸ワールド記念ホールで9月9日(水)・10日(木)の2日間、昼夜あわせて計4公演がおこなわれます。今回生配信の対象になったのは、そのうち最終公演にあたる<strong>9月10日(木)の夜公演</strong>だけです。",
    "配信のスタートは夜公演の開演と同じ18:30(JST)。生配信のみで、<strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">アーカイブ(見逃し)配信は用意されていません</span></strong>。当日その時間にリアルタイムで視聴する必要があります。",
    "東京公演(8月21日〜23日・TOYOTA ARENA TOKYO)はすでに終了しているため、初のファンミーティングの模様を映像で楽しめるのは、実質この兵庫・夜公演の生配信が唯一の機会になります。",
]))
blocks.append(wptable(
    ["公演", "開場", "開演", "生配信"],
    [
        ["9/9(水)昼", "12:30", "13:30", "なし"],
        ["9/9(水)夜<br>[追加公演]", "17:30", "18:30", "なし"],
        ["9/10(木)昼<br>[追加公演]", "12:30", "13:30", "なし"],
        ["9/10(木)夜", "17:30", "18:30", "〇 生配信対象"],
    ],
))
blocks.append(p([
    "発表は公式X(@KO1KEYZofficial)と公式サイトのニュースでおこなわれ、「兵庫公演を全世界で生配信決定」という文言とともに一気に拡散されました。デビュー前のグループながら、初のファンミーティングへの注目度の高さがうかがえます。",
    "チケットが取れなかったファンや、関西まで足を運べない遠方・海外のファンにとっては、この生配信がメンバーの姿をそろって見られる貴重なタイミングになりそうです。",
]))

blocks.append(h2("視聴チケットの料金と配信サービスは？"))
blocks.append(minibox('<p style="margin:0;"><strong>視聴チケット:</strong>3,600円(税込)＋各種システム利用料</p>\n<p style="margin:4px 0 0 0;"><strong>配信サービス:</strong>国内=Lemino・ローソンチケット/海外向けにも別サービスを用意</p>'))
blocks.append(p([
    "<strong><span class=\"swl-marker mark_yellow\">視聴チケットの価格は3,600円(税込)</span></strong>です。これとは別に、配信プラットフォームごとのシステム利用料が加算されます。",
    f"<span class=\"swl-marker mark_yellow\">国内向けの配信はLeminoとローソンチケット</span>、海外向けにも別途配信サービスが用意されています。対応サービスや決済方法などのくわしい情報は、<a href=\"{OFFICIAL_NEWS}\" target=\"_blank\" rel=\"noopener\">公式サイトのお知らせページ</a>で確認できます。",
    "現地の座席チケットと比べると、生配信は3,600円ほどで自宅から見られるぶん、参加のハードルはかなり低めです。デビュー前のグループのファンミーティングを気軽にのぞける機会になりそうです。",
]))
blocks.append(p([
    "上乗せされるシステム利用料は、プラットフォームによって金額が変わります。Xでは、LeminoとローソンチケットのどちらもチケットプラスⅠの手数料がかかるため、実際に両方の購入画面を比べたファンから「合計金額は数百円ほど差がついた」という報告が上がっています。",
    "また、ローソンチケットは決済がローソン・ミニストップでの店頭入金に限られ、クレジットカード払いには対応していないという声も見られました。カードでさっと買いたいならLemino、店頭でまとめて支払いたいならローソンチケット、という選び方になりそうです。最終的な支払い総額は、購入前に各サービスの画面で必ず確認してください。",
]))

blocks.append(h2("チケットの販売期間と視聴までの流れ"))
blocks.append(minibox('<p style="margin:0;"><strong>販売期間:</strong>2026年9月3日(木)12:00pm 〜 9月10日(木)7:00pm(JST)</p>'))
blocks.append(p([
    "視聴チケットの販売期間は<strong>2026年9月3日(木)12:00pm〜9月10日(木)7:00pm(JST)</strong>です。配信当日の夜公演開演(18:30)後もしばらくは購入できますが、19:00には販売が締め切られます。アーカイブがないぶん、見たい人は早めに用意しておくと安心です。",
]))
blocks.append(titlebox("視聴チケットの購入〜視聴の流れ", [
    "国内はLemino・ローソンチケット、海外向けサービスのうち、利用したい配信ページにアクセスする",
    "販売期間内(9/3 12:00pm〜9/10 7:00pm JST)に視聴チケット(3,600円＋システム利用料)を購入・決済する",
    "配信当日、購入したサービスのアプリやサイトに同じアカウントでログインする",
    "9月10日(木)18:30(JST)の配信開始にあわせて視聴をスタートする(見逃し配信はなし)",
], ordered=True))
blocks.append(p([
    "海外から視聴する場合は、日本との時差にも注意が必要です。生配信のみなので、開始時刻の18:30(JST)を自分のいる国の時間に置きかえて、事前にスケジュールを押さえておきましょう。",
    "当日は通信環境の良い場所で、できればWi-Fiにつないで視聴するのがおすすめです。開始直前は回線が混み合うこともあるため、少し余裕をもって配信ページを開いておくと落ち着いて見られます。",
]))

blocks.append(h2("生配信ではどんな様子が見られる？"))
blocks.append(p([
    "初のファンミーティングは、トークコーナーやメンバー同士のゲーム、楽曲パフォーマンス、そして終盤の撮影OKタイムなどで構成されています。先に開催された東京公演では、メンバーがトロッコで客席をまわる場面や、アンコールでの撮影可能タイムがファンの間で大きな話題になりました。",
    f"今回生配信される兵庫・夜公演は全4公演のなかの最終公演にあたるため、2日間を走り抜けたメンバーの空気感や、締めくくりならではの挨拶も見どころになりそうです。東京公演当日の様子は<a href=\"{DAY1_URL}\">KO1KEYZ1stファンミ初日(東京)セトリ・座席表・トロッコは？</a>にまとめているので、配信前に予習しておくと当日をより楽しめます。",
]))

blocks.append(h2("アーカイブ配信や円盤化はある？"))
blocks.append(minibox('<p style="margin:0;"><strong>アーカイブ配信:</strong>なし(生配信のみ)</p>\n<p style="margin:4px 0 0 0;"><strong>円盤化(Blu-ray・DVD):</strong>2026年9月3日時点で発表なし</p>'))
blocks.append(p([
    "今回の生配信にアーカイブ(見逃し)配信はありません。配信終了後に同じ映像を見返すことはできない仕組みなので、視聴を予定している人はリアルタイムでの視聴を前提に準備しておきましょう。",
    f"公演そのもののBlu-ray・DVD化についても、現時点で公式からの発表はありません。会場に収録用のカメラが入っていた件や円盤化の可能性については、<a href=\"{CAMERA_URL}\">KO1KEYZ1stファンミにカメラが？円盤化の可能性は？</a>でくわしくまとめています。",
    f"なお、ファンミーティングの準備に密着した特別番組が<a href=\"{LEMINO_URL}\">Leminoで配信されること</a>は別に発表されていますが、こちらは公演本編そのものではなくドキュメンタリー的な内容です。今回の兵庫・夜公演の生配信とは別のコンテンツなので、混同しないよう注意してください。",
]))

blocks.append(h2("まとめ"))
blocks.append(notebox('''<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">コイキーズ神戸ファンミ 生配信まとめ</p>
<p style="margin:0;">
&#10003; 生配信されるのは兵庫(神戸ワールド記念ホール)2日目・夜公演のみ<br>
&#10003; 配信日時は2026年9月10日(木)18:30(JST)〜、アーカイブ配信なし<br>
&#10003; 視聴チケットは3,600円(税込)＋システム利用料、国内はLemino・ローソンチケット<br>
&#10003; システム利用料はサービスで差があり、ローソンチケットは店頭入金のみという声も<br>
&#10003; 販売期間は9月3日(木)12:00pm〜9月10日(木)7:00pm(JST)<br>
&#10003; 円盤化は未発表。Leminoの特別番組は公演本編とは別物
</p>'''))
blocks.append(p([
    "現地に行けなくても、初めてのファンミーティングをリアルタイムで見届けられるのはうれしいところです。時差や販売期限に気をつけて、当日は早めに配信ページを開いて待機しておきたいですね。",
]))

blocks.append(notebox(f'''<p style="margin:0 0 8px 0;"><strong>KO1KEYZのファンミーティングについては、このブログの他の記事でも紹介しています。</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{VENUE_URL}" target="_blank" rel="noopener">KO1KEYZのファンミーティングの会場はどこ？日程やアクセスも紹介！</a></li>
<li><a href="{DAY1_URL}" target="_blank" rel="noopener">KO1KEYZ1stファンミ初日(東京)セトリ・座席表・トロッコは？</a></li>
<li><a href="{CAMERA_URL}" target="_blank" rel="noopener">KO1KEYZ1stファンミにカメラが？円盤化の可能性は？</a></li>
<li><a href="{SCHEDULE_URL}" target="_blank" rel="noopener">KO1KEYZの今後のスケジュールは？デビューまでの日程まとめ</a></li>
</ul>'''))

content = "\n\n".join(blocks)

plain = re.sub(r"<!--.*?-->", "", content, flags=re.S)
plain = re.sub(r"<[^>]+>", "", plain)
print("content length (chars):", len(plain))


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


SUMMARY = "KO1KEYZ初のファンミーティング『2026 KO1KEYZ 1ST FAN MEETING』兵庫公演のうち、9月10日(木)夜公演のみが全世界に生配信されます。視聴チケットは3,600円(税込)、国内はLemino・ローソンチケットで、アーカイブ配信はありません。"

slug = "ko1keyz-kobe-fan-meeting-strea"
print("slug:", slug)

EYECATCH_MEDIA_ID = 12244  # already uploaded on first run
EXISTING_POST_ID = 12245   # update in place

payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": "draft",
    "categories": [66, 62],
    "author": 2,
    "lang": "ja",
    "featured_media": EYECATCH_MEDIA_ID,
    "meta": {"jetpack_publicize_message": SUMMARY},
}
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_POST_ID}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"])
print("SLUG", post["slug"])
print("PREVIEW", f"{WP_URL}/?p={post['id']}")

with open(ROOT / "tmp_ko1keyz_kobe_fanmi_streaming_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
with open(ROOT / "tmp_ko1keyz_kobe_fanmi_streaming_slug.txt", "w", encoding="utf-8") as f:
    f.write(post["slug"])
with open(ROOT / "tmp_ko1keyz_kobe_fanmi_streaming_eyecatch_mediaid.txt", "w", encoding="utf-8") as f:
    f.write(str(EYECATCH_MEDIA_ID))
