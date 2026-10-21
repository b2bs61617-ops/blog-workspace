# -*- coding: utf-8 -*-
# chomoand-4.blog: トラジャのFCはいつ入るのが正解？ツアー発表時期とFC受付の流れ(2026-10-21)
import json, base64, os, re, sys, subprocess
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
AUTH = base64.b64encode(f'{ENV["WP_CHOMO4_USERNAME"]}:{ENV["WP_CHOMO4_APP_PASSWORD"]}'.encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}
HJSON = {**HEADERS_AUTH, "Content-Type": "application/json"}

IMG_DIR = ROOT / "images" / "tj_fc_timing"
EYECATCH = IMG_DIR / "tj_fc_timing_eyecatch_canva.jpg"
DRY = "--dry" in sys.argv
UPDATE_ID = 1643

TITLE = "トラジャのFCはいつ入るのが正解？ツアー発表は毎年10月末！"
SLUG = "travis-japan-fanclub-when-to-join"

# グループ記事なので紫
ACC = "#7e57c2"
BORDER = "#d9cdf0"
BG = "#f5f2fb"

FC_URL = "https://www.familyclub.jp/join/detail/f/TJ"


def p(sentences):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(sentences) + "</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def mark(text):
    return f'<strong><span class="swl-marker mark_yellow">{text}</span></strong>'


def whatbox(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(rows):
    lines = "\n".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
        for i, (k, v) in enumerate(rows))
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{lines}
</div>''')


def table2(header, rows):
    th = "".join(f"<th>{c}</th>" for c in header)
    trs = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><thead><tr>{th}</tr></thead><tbody>
{trs}
</tbody></table></figure>
<!-- /wp:table -->'''


def checklist(title, items):
    lis = "\n".join(
        f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {ACC};border-radius:3px;color:{ACC};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{i}</p>'
        for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">{title}</p>
<div style="padding:14px 18px;background:{BG};">
{lis}
</div>
</div>''')


def x_embed(user, tid):
    return wphtml(f'''<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><a href="https://twitter.com/{user}/status/{tid}">https://twitter.com/{user}/status/{tid}</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>''')


blocks = []

# ---- intro ----
blocks.append(p([
    "Travis Japanのライブに行きたいと思ったとき、まず迷うのが「ファンクラブにはいつ入ればいいの？」ということではないでしょうか。",
    "結論からいうと、<strong>ツアーの発表がある10月28日より前に、入会とお支払いまで済ませておくのがいちばん安心</strong>です。",
    "トラジャのツアーは毎年10月28日前後に発表されていて、ファンクラブ会員の申し込みは発表のすぐ後、わずか1週間ほどで締め切られてきました。",
    "この記事では、過去3年のツアー発表日とファンクラブ受付の日程を並べたうえで、入会から会員番号が届くまでの流れや費用を、ファンクラブの公式案内をもとにまとめます。",
]))
blocks.append(whatbox([
    "トラジャのツアーが毎年いつ発表されているか",
    "ファンクラブ会員の申し込み期間はどれくらいか",
    "入会してから会員番号が届くまでの日数",
    "入会金・年会費と支払い期限",
    "会員の有効期間の数え方",
    "入会前にやっておきたい準備",
]))

# ---- announcement history ----
blocks.append(h2("トラジャのツアー発表は毎年いつ？10月28日前後が恒例"))
blocks.append(minibox([
    ("過去の発表日", "2023年・2024年・2025年とも10月28日"),
    ("10月28日は", "Travis Japanの世界デビュー記念日(2022年)"),
    ("ツアー初日", "3年続けて翌年1月4日の横浜アリーナ"),
]))
blocks.append(p([
    "Travis Japanは2022年10月28日に世界デビューしました。",
    "それ以来、全国アリーナツアーの開催は<strong>3年続けてデビュー記念日の10月28日に発表</strong>されています。",
]))
blocks.append(table2(
    ["ツアー", "発表日", "FC会員の申込期間", "抽選結果", "初日"],
    [
        ["2024 Road to Authenticity", "2023年10月28日", "10/30(月)13:00〜11/6(月)12:00", "11/21以降", "2024年1月4日"],
        ["2025 VIIsual", "2024年10月28日", "11/1(金)〜11/8(金)", "11/25", "2025年1月4日"],
        ["2026 's travelers", "2025年10月28日", "10/29(水)12:00〜11/4(火)12:00", "11/21", "2026年1月4日"],
    ],
))
blocks.append(p([
    "どの年も、発表から1〜4日後にファンクラブ会員の申し込みが始まり、<strong>受付期間はおよそ1週間</strong>でした。",
    "2025年10月28日は夜の生配信の中で2026年ツアーの開催が発表され、公式Xにも23時すぎに告知が出ています。",
    "そして翌日の29日お昼12時には、もうファンクラブ会員の受付が始まっていました。",
]))
blocks.append(x_embed("TravisJapan_cr", "1983173494151303371"))
blocks.append(p([
    "2026年ツアーは、そのあと愛知公演が1公演増えて全30公演になりました。",
    "追加公演の会員受付は2025年11月21日15時〜25日12時と、こちらは4日ほどしかありませんでした。",
    "発表を見てからゆっくり入会を考えていると、こうした短い受付にも間に合わないことがあります。",
]))

# ---- why before ----
blocks.append(h2("FCは発表の前に入っておくのが安心な理由"))
blocks.append(p([
    "ファンクラブ会員の申し込みは、入会したときに発行される<strong>会員番号</strong>を使って行います。",
    "つまり、受付の締め切りまでに会員番号が届いていなければ、申し込むことができません。",
]))
blocks.append(p([
    "ファンクラブの公式案内によると、会員番号は<strong>入金が確認されてから24時間以内</strong>にメールで届きます。",
    "クレジットカードで払えばすぐに入金扱いになりますが、コンビニ支払いやPay-easyを選ぶと、自分で払いに行くまでは手続きが終わりません。",
    "受付期間がわずか1週間しかないことを考えると、払い忘れやメールの遅れが1つあるだけで間に合わなくなるおそれがあります。",
]))
blocks.append(p([
    f"そのため、{mark('10月28日の発表を待たずに、入会とお支払いまで済ませておく')}のがいちばん確実です。",
]))

# ---- steps ----
blocks.append(h2("入会から会員番号が届くまでの流れ"))
blocks.append(p([
    "Travis Japanのファンクラブは、STARTO ENTERTAINMENTのアーティストのファンクラブをまとめて運営している「FAMILY CLUB」から入会します。",
    "公式サイトに載っている手順は、次の6ステップです。",
]))
blocks.append(table2(
    ["ステップ", "やること"],
    [
        ["1", "メールアドレスを入力し、会員規約を確認して送信"],
        ["2", "届いた「ファンクラブ入会申込みメール」を確認"],
        ["3", "メールのURLから本人の情報を登録"],
        ["4", "入会金・年会費を支払う(クレジットカード・Pay-easy・コンビニ支払い)"],
        ["5", "入金確認後24時間以内に、会員番号のメールが届く"],
        ["6", "会員証が郵送で届く(手続き完了から2〜3週間ほど)"],
    ],
))
blocks.append(p([
    "ここで気をつけたいのが、ステップ1で入力するメールアドレスです。",
    "公式案内では「fc-member.familyclub.jp」からのメールを受け取れるように設定しておくよう呼びかけていて、iCloudやGmailでは届かない・遅れるといった例もあると書かれています。",
    "なかなかメールが来ないときは、別のアドレスで入会することも考えてみてください。",
]))
blocks.append(p([
    "また、Pay-easyやコンビニ支払いを選んだ場合は、画面に出るお支払い番号を必ずメモしておきましょう。",
    "会員証は紙で郵送されますが、届くまでに2〜3週間かかるので、ツアーの申し込みは会員番号のメールが届いた時点で進められます。",
]))

# ---- fees ----
blocks.append(h2("入会金・年会費はいくら？"))
blocks.append(minibox([
    ("入会金", "1,000円(初年度のみ)"),
    ("年会費", "4,000円"),
    ("事務手数料", "140円"),
    ("入会時の合計", "5,140円"),
]))
blocks.append(p([
    "入会するときに払うのは、入会金1,000円・年会費4,000円・事務手数料140円の<strong>合計5,140円</strong>です。",
    "入会金がかかるのは最初の1回だけで、2年目からは年会費4,000円で続けられます(更新時の手数料は手続きの画面で確認してください)。",
]))
blocks.append(p([
    "会員になると、チケットの優先申し込みのほかに、会報・バースデーカード・会員限定動画・メール伝言板などが受け取れます。",
    "チケット代もファンクラブ価格があり、たとえば2025年の「VIIsual」はファンクラブ9,500円、一般10,000円(いずれも税込)でした。",
]))
blocks.append(h3("支払い期限は申し込んだ日で変わる"))
blocks.append(table2(
    ["入会手続きをした日", "支払い期限"],
    [
        ["毎月1日〜14日", "手続きした日から2週間後"],
        ["毎月15日〜月末", "その月の末日"],
        ["月末の当日", "当日23:59まで(クレジットカードのみ)"],
    ],
))
blocks.append(p([
    "支払い期限には余裕がありますが、期限ぎりぎりまで払わないでいると、その間に受付が終わってしまうこともあります。",
    "ツアーの申し込みに間に合わせたいなら、入会手続きをしたその日のうちに払ってしまうのがおすすめです。",
]))

# ---- validity ----
blocks.append(h2("会員の有効期間は「承認された月の翌月1日から1年間」"))
blocks.append(p([
    "ファンクラブの会員規約では、会員の有効期間は<strong>入会が承認された日の翌月1日から1年間</strong>と決められています。",
    "たとえば10月中に入会が承認されると、有効期間は11月1日から翌年10月31日までになります。",
]))
blocks.append(p([
    "続けたいときは、会員サイトのマイページに出る更新期間のうちに次の年会費を払います。",
    "<strong>更新期間を過ぎると更新はできず、もう一度入会し直すことになる</strong>ので、年会費の支払い時期はカレンダーなどにメモしておくと安心です。",
    "有効期限はマイページで確認できます。",
]))

# ---- 2026 ----
blocks.append(h2("2026年もツアー発表は10月28日？"))
blocks.append(p([
    "2026年10月28日は、Travis Japanのデビュー4周年の記念日です。",
    "2026年10月21日の時点では、2027年のツアーはまだ発表されていません。",
    "これまでの3年と同じ流れなら、10月28日前後に発表があり、その数日後からファンクラブ会員の受付が始まることになります。",
]))
blocks.append(p([
    "11月18日には4thアルバム「Jewelry Basket」の発売も控えています。",
    "これまでのツアーも、どれも前の年の12月に出たアルバムを引っ提げたものでした。",
    '会場の空き日程から2027年ツアーを予想した記事は<a href="https://chomoand-4.blog/travis-japan-2027-tour-venue-prediction-926">トラジャ2027年ツアーも横アリ初日？会場を空き日程から予想！</a>にまとめています。',
    "今年のうちにツアーに申し込みたいなら、10月27日までにファンクラブへの入会と支払いを終えておきましょう。",
]))

# ---- checklist ----
blocks.append(checklist("入会前にやっておきたいこと", [
    "「fc-member.familyclub.jp」からのメールを受け取れるように設定する",
    "支払いはクレジットカードにすると、すぐに入金扱いになる",
    "Pay-easy・コンビニ支払いなら、お支払い番号をメモしてその日のうちに払う",
    "会員番号のメールが届いたかどうかを確認する",
    "ツアー発表(例年10月28日)の前に、ここまで終わらせておく",
]))

# ---- summary ----
blocks.append(h2("まとめ"))
blocks.append(checklist("この記事のポイント", [
    "トラジャのツアーは2023〜2025年の3年続けて10月28日に発表",
    "ファンクラブ会員の受付は発表の1〜4日後から、期間は約1週間",
    "会員番号は入金確認から24時間以内にメールで届く",
    "入会時の費用は合計5,140円(入会金1,000円・年会費4,000円・手数料140円)",
    "有効期間は入会が承認された月の翌月1日から1年間",
    "ツアーに申し込みたいなら、10月28日より前に入会と支払いを済ませるのが安心",
]))
blocks.append(p([
    "受付期間が短いトラジャのツアーは、「発表を見てから入る」だと間に合わないこともあります。",
    "10月28日の発表を落ち着いて待てるように、早めに準備しておきましょう！",
    f'入会の手続きは<a href="{FC_URL}" target="_blank" rel="noopener">FAMILY CLUBのTravis Japan新規入会ページ</a>から進められます。',
]))

content = "\n\n".join(blocks)

if DRY:
    out = ROOT / "articles" / "travis_japan_fc_join_timing.html"
    out.write_text(content, encoding="utf-8")
    text = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", content))
    print("title chars:", len(TITLE))
    print("body chars:", len(text))
    print("saved:", out)
    sys.exit()

if UPDATE_ID:
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{UPDATE_ID}", headers=HJSON,
                      data=json.dumps({"content": content, "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    print("UPDATED", UPDATE_ID, r.json()["status"])
    sys.exit()


def upload_media(filepath: Path, ctype="image/jpeg"):
    headers = {**HEADERS_AUTH, "Content-Type": ctype,
               "Content-Disposition": f'attachment; filename="{filepath.name}"'}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=filepath.read_bytes())
    r.raise_for_status()
    return r.json()


payload = {"title": TITLE, "content": content, "status": "draft", "slug": SLUG, "categories": [3]}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
POST_ID = post["id"]
print("POST_ID", POST_ID, "status", post["status"], "SLUG", post["slug"])

IMG_DIR.mkdir(parents=True, exist_ok=True)
eye = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
     "--main", "ファンクラブ",
     "--bottom", "いつ入るのが正解？", "--bottom", "ツアー発表は毎年10月末！",
     "--color-key", "group", "--out", str(EYECATCH)],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
)
print(eye.stdout[-300:], eye.stderr[-300:])
if eye.returncode == 0:
    em = upload_media(EYECATCH)
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}", headers=HJSON,
                      data=json.dumps({"featured_media": em["id"], "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    print("EYECATCH", em["id"], r.json()["status"])
