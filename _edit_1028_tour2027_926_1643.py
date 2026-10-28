# -*- coding: utf-8 -*-
# 2027ツアー「Jewelry Basket」発表(2026-10-28)を受けて、c4公開記事926(会場予想)と1643(FCいつ入る)を追記・修正
import sys
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))
from build_and_post_travis_japan_tour2027_jewelry_basket import (
    WP_URL, HJSON, p, h2, h3, minibox, table2, wphtml, mark, ACC, BORDER, BG)

DRY = "--dry" in sys.argv
LIVE_URL = "https://www.youtube.com/watch?v=GDUJdc_ytzo"

SCHEDULE_ROWS = [
    ["1/4(月)〜1/7(木)", "神奈川", "横浜アリーナ"],
    ["1/16(土)〜1/17(日)", "宮城", "セキスイハイムスーパーアリーナ"],
    ["2/13(土)〜2/14(日)", "福岡", "マリンメッセ福岡A館"],
    ["2/20(土)〜2/21(日)", "愛知", "Aichi Sky Expo Aホール"],
    ["3/26(金)〜3/28(日)", "千葉", "ららアリーナ 東京ベイ"],
    ["4/3(土)〜4/4(日)", "北海道", "真駒内セキスイハイムアイスアリーナ"],
    ["5/1(土)〜5/2(日)", "大阪", "大阪城ホール"],
    ["5/22(土)〜5/23(日)", "静岡", "エコパアリーナ"],
]


def update_box(title, lines):
    body = "<br>\n".join(lines)
    return wphtml(f'''<div style="border:2px solid {ACC};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">{title}</p>
<p style="margin:0;padding:14px 18px;background:{BG};">{body}</p>
</div>''')


def replace_once(html, old, new):
    n = html.count(old)
    assert n == 1, (n, old[:80])
    return html.replace(old, new)


def get(pid):
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=HJSON)
    r.raise_for_status()
    return r.json()["content"]["raw"]


def put(pid, html, must):
    if DRY:
        Path(f"backups/tour2027_1028/{pid}_new.html").write_text(html, encoding="utf-8")
        print(pid, "dry ok", len(html))
        return
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=HJSON, json={"content": html})
    r.raise_for_status()
    raw = get(pid)
    assert all(m in raw for m in must), "not reflected"
    print(pid, r.json()["status"], "updated")


# ------------------------------------------------------------------ 926
html = get(926)
first_p_end = "この記事では、過去3年のツアー会場と各会場の空き日程から、2027年ツアーの会場と日程、発表時期を予想していきます。</p>\n<!-- /wp:paragraph -->"
html = replace_once(html, first_p_end, first_p_end + "\n\n" + update_box("【2026年10月28日追記】予想どおり1月4日の横アリから開幕！", [
    "2026年10月28日、デビュー4周年記念のYouTube生配信で「Travis Japan Concert Tour 2027『Jewelry Basket』」の開催が発表されました。",
    f"初日は{mark('予想どおり2027年1月4日(月)の横浜アリーナ')}で、5月23日(日)のエコパアリーナまで全国8会場を回ります。",
    "発表された日程と予想の答え合わせは、記事の後半の「発表された2027年ツアーの日程は？予想と答え合わせ」にまとめました。",
]))

html = replace_once(html, "2023年10月28日・2024年10月28日・2025年10月30日", "2023年10月28日・2024年10月28日・2025年10月28日")
html = replace_once(html, '<td style="border:1px solid #d9cfee;padding:8px 12px;">2025年10月30日</td>',
                    '<td style="border:1px solid #d9cfee;padding:8px 12px;">2025年10月28日</td>')
html = replace_once(html, "2023年と2024年はまさにその当日、2025年も2日後の10月30日に発表されていて、",
                    "2023年・2024年・2025年と3年続けてまさにその当日に発表されていて、")
html = replace_once(html, 'font-weight:bold;">2027(未発表)</td>\n<td style="border:1px solid #d9cfee;padding:8px 12px;background:#fff6db;font-weight:bold;">?</td>',
                    'font-weight:bold;">2027 Jewelry Basket</td>\n<td style="border:1px solid #d9cfee;padding:8px 12px;background:#fff6db;font-weight:bold;">2026年10月28日</td>')
html = replace_once(html, 'font-weight:bold;">2026年11月18日</td>\n<td style="border:1px solid #d9cfee;padding:8px 12px;background:#fff6db;font-weight:bold;">?</td>',
                    'font-weight:bold;">2026年11月18日</td>\n<td style="border:1px solid #d9cfee;padding:8px 12px;background:#fff6db;font-weight:bold;">2027年1月4日</td>')

answer = "\n\n".join([
    h2("発表された2027年ツアーの日程は？予想と答え合わせ"),
    minibox([
        ("ツアー名", "Travis Japan Concert Tour 2027「Jewelry Basket」"),
        ("期間", "2027年1月4日(月)〜5月23日(日)・全国8会場"),
        ("発表", "2026年10月28日 デビュー4周年記念YouTube生配信"),
    ]),
    p([
        "2026年10月28日の21時から行われたデビュー4周年記念の生配信で、2027年のツアー日程が発表されました。",
        "4年続けて、デビュー記念日の当日にツアーが告知されたことになります。",
    ]),
    table2(["日程", "地域", "会場"], SCHEDULE_ROWS),
    p([
        "この記事で予想していた内容と、実際の日程を見比べてみると次のとおりです。",
    ]),
    table2(["予想", "結果"], [
        ["初日は1月4日〜7日ごろの横浜アリーナ", "的中(1/4〜1/7)"],
        ["大阪城ホールは休館明け(3月中旬以降)", "的中(5/1〜2)"],
        ["真駒内は改修明けの3月下旬以降", "的中(4/3〜4)"],
        ["福岡は4月か5月中旬以降", "外れ(2/13〜14)"],
        ["名古屋はクロコくんホールの3月", "外れ(Aichi Sky Expoの2/20〜21)"],
        ["千秋楽は5〜6月のららアリーナ", "外れ(ららは3/26〜28、千秋楽はエコパ)"],
    ]),
    p([
        f"いちばんの注目だった初日は、{mark('予想どおり1月4日の横浜アリーナ')}で、2024年から4年連続の「1月4日・横アリ」スタートとなりました。",
        "1月1日〜10日がまるごと空いていた横アリの予定表に、そのまま当てはまる形です。",
        "工事で使えない時期があった大阪城ホールと真駒内も、どちらも工事明けの日程に組まれていました。",
    ]),
    p([
        "一方で、マリンメッセ福岡は2月、ららアリーナ東京ベイは3月と、予想より早い時期に入っています。",
        "千秋楽は2025年・2026年のららアリーナではなく、初めて静岡のエコパアリーナになりました。",
        "愛知は2026年のガイシホール(現・クロコくんホール)ではなく、2025年に使ったAichi Sky Expoに戻っています。",
        "ファンクラブ受付などの続報が出たら、あわせてお知らせしていきます。",
    ]),
])
html = replace_once(html, '<!-- wp:heading -->\n<h2 class="wp-block-heading">まとめ</h2>', answer + '\n\n<!-- wp:heading -->\n<h2 class="wp-block-heading">まとめ</h2>')
put(926, html, ["予想どおり1月4日の横アリから開幕", "発表された2027年ツアーの日程は", "2025年10月28日"])

# ------------------------------------------------------------------ 1643
html = get(1643)
intro_end = html.index("<!-- /wp:paragraph -->") + len("<!-- /wp:paragraph -->")
html = html[:intro_end] + "\n\n" + update_box("【2026年10月28日追記】2027年ツアーが発表されました", [
    "2026年10月28日のデビュー4周年記念の生配信で、「Travis Japan Concert Tour 2027『Jewelry Basket』」の開催が発表されました。",
    "2027年1月4日(月)の横浜アリーナから、5月23日(日)のエコパアリーナまで全国8会場を回ります。",
    f"ファンクラブ受付の日程は発表の時点ではまだ出ていませんが、2026年ツアーでは{mark('発表の翌日12時から')}受付が始まっていました。",
    "これから入会する人は、今すぐ手続きとお支払いを済ませておきましょう。",
]) + html[intro_end:]

old_sec_start = '<!-- wp:heading -->\n<h2 class="wp-block-heading">2026年もツアー発表は10月28日？</h2>'
old_sec_end = "今年のうちにツアーに申し込みたいなら、10月27日までにファンクラブへの入会と支払いを終えておきましょう。</p>\n<!-- /wp:paragraph -->"
s = html.index(old_sec_start)
e = html.index(old_sec_end) + len(old_sec_end)
new_sec = "\n\n".join([
    h2("2026年もツアー発表は10月28日！2027年ツアーの日程は？"),
    minibox([
        ("ツアー名", "Travis Japan Concert Tour 2027「Jewelry Basket」"),
        ("発表日", "2026年10月28日(デビュー4周年記念のYouTube生配信)"),
        ("期間", "2027年1月4日(月)〜5月23日(日)・全国8会場"),
        ("FC受付", "10月28日の発表時点では未発表"),
    ]),
    p([
        "2026年10月28日、Travis Japanのデビュー4周年の記念日に、2027年のツアー開催が発表されました。",
        f"21時からの生配信の中での発表で、{mark('4年続けてデビュー記念日の当日')}にツアーが告知されたことになります。",
    ]),
    table2(["日程", "地域", "会場"], SCHEDULE_ROWS),
    p([
        "ファンクラブ会員の受付日程は、10月28日の発表の時点ではまだ出ていません。",
        "ただ、2026年のツアーでは発表の翌日12時に受付が始まっていて、これまでの3年も発表から1〜4日後には受付がスタートしています。",
        "受付期間はおよそ1週間なので、まだ入会していない人は今のうちに入会とお支払いまで済ませておくのが安心です。",
        "受付の日程が発表されたら、この記事にも追記していきます。",
    ]),
    p([
        "ツアー名は、11月18日に発売される4thアルバムと同じ「Jewelry Basket」です。",
        "これまでのツアーも、どれも直前に出たアルバムを引っ提げたものでした。",
        '会場の空き日程から2027年ツアーを予想した記事と答え合わせは<a href="https://chomoand-4.blog/travis-japan-2027-tour-venue-prediction-926">トラジャ2027年ツアーも横アリ初日？会場を空き日程から予想！</a>にまとめています。',
    ]),
])
html = html[:s] + new_sec + html[e:]
put(1643, html, ["2027年ツアーが発表されました", "2026年もツアー発表は10月28日！"])
