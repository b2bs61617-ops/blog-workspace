# -*- coding: utf-8 -*-
# chomoand-4.blog: Travis Japan Concert Tour 2027「Jewelry Basket」会場別の申込状況・激戦度(申込日程アンケートの集計×キャパ)
# 回答数は申込日程アンケート(@memo_suruyou、締切11/3)の最終集計グラフ(2026-11-04に中間1,283件→最終3,124件へ差し替え)
# 公開済み(ID 2115)。再投稿は `--update-live` で本文だけ差し替える(タイトル・公開状態は触らない)
# キャパ・公演数は build_and_post_travis_japan_tour2027_venue_capacity.py(下書き2006)と同じ数字
import json, base64, os, sys, subprocess
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

IMG_DIR = ROOT / "images" / "tj_tour2027_odds"
EYECATCH = IMG_DIR / "tj_tour2027_odds_eyecatch_canva.jpg"
STATE = IMG_DIR / "_state.json"
DRY = "--dry" in sys.argv

TITLE = "【未】トラジャ2027ツアーの倍率は？会場別の申込状況を比較"
SLUG = "travis-japan-2027-tour-odds-by-venue"
SITE = "https://chomoand-4.blog/"
SCHEDULE_ARTICLE = ("トラジャ2027ツアー『Jewelry Basket』の会場・日程まとめ！", "travis-japan-2027-tour-jewelry-basket-schedule-1973")
CAPACITY_ARTICLE = ("トラジャ2027ツアー会場のキャパは？収容人数と公演数まとめ", "travis-japan-2027-tour-venue-capacity")

SURVEY_URL = "https://x.com/memo_suruyou/status/2117659539277529348"
SURVEY_AS_OF = "11月3日の最終集計"
SURVEY_TOTAL = 3124

# (会場, 地域, 最大収容人数 or None, [(公演, 回答数)])
VENUES = [
    ("横浜アリーナ", "神奈川", 17000, [("1/4(月)", 1125), ("1/5(火)昼", 966), ("1/5(火)夜", 909), ("1/6(水)", 890), ("1/7(木)昼", 940), ("1/7(木)夜", 900)]),
    ("セキスイハイムスーパーアリーナ", "宮城", 7063, [("1/16(土)昼", 651), ("1/16(土)夜", 646), ("1/17(日)", 686)]),
    ("マリンメッセ福岡A館", "福岡", 15000, [("2/13(土)昼", 615), ("2/13(土)夜", 606), ("2/14(日)", 641)]),
    ("Aichi Sky Expo Aホール", "愛知", None, [("2/20(土)昼", 679), ("2/20(土)夜", 633), ("2/21(日)", 706)]),
    ("ららアリーナ 東京ベイ", "千葉", 11000, [("3/26(金)", 731), ("3/27(土)昼", 972), ("3/27(土)夜", 911), ("3/28(日)昼", 1002), ("3/28(日)夜", 849)]),
    ("真駒内セキスイハイムアイスアリーナ", "北海道", 11500, [("4/3(土)昼", 481), ("4/3(土)夜", 516), ("4/4(日)", 496)]),
    ("大阪城ホール", "大阪", 16000, [("5/1(土)", 1097), ("5/2(日)昼", 1250), ("5/2(日)夜", 1139)]),
    ("エコパアリーナ", "静岡", 10000, [("5/22(土)昼", 1045), ("5/22(土)夜", 997), ("5/23(日)昼", 1211), ("5/23(日)夜", 1238)]),
]
OSAKA_B = 11200
assert sum(len(v[3]) for v in VENUES) == 30

# 第1希望のX投票(@ticket_festa、11本のスレッド、締切11/3 9:35)。「閲覧用」は除く。最終結果をfxtwitter APIで2026-11-04に取得
POLL_URL = "https://x.com/ticket_festa/status/2115965758962544997"
POLL_AS_OF = "11月3日の最終結果"
POLL = [
    ("神奈川", "1/4(月)", 1028), ("神奈川", "1/5(火)昼", 289), ("神奈川", "1/5(火)夜", 153),
    ("神奈川", "1/6(水)", 119), ("神奈川", "1/7(木)昼", 147), ("神奈川", "1/7(木)夜", 124),
    ("宮城", "1/16(土)昼", 103), ("宮城", "1/16(土)夜", 79), ("宮城", "1/17(日)", 74),
    ("福岡", "2/13(土)昼", 114), ("福岡", "2/13(土)夜", 66), ("福岡", "2/14(日)", 126),
    ("愛知", "2/20(土)昼", 109), ("愛知", "2/20(土)夜", 55), ("愛知", "2/21(日)", 86),
    ("千葉", "3/26(金)", 76), ("千葉", "3/27(土)昼", 133), ("千葉", "3/27(土)夜", 53),
    ("千葉", "3/28(日)昼", 126), ("千葉", "3/28(日)夜", 67),
    ("北海道", "4/3(土)昼", 55), ("北海道", "4/3(土)夜", 68), ("北海道", "4/4(日)", 45),
    ("大阪", "5/1(土)", 153), ("大阪", "5/2(日)昼", 162), ("大阪", "5/2(日)夜", 83),
    ("静岡", "5/22(土)昼", 129), ("静岡", "5/22(土)夜", 115), ("静岡", "5/23(日)昼", 107), ("静岡", "5/23(日)夜", 305),
]
POLL_VIEW_FIRST, POLL_VIEW_OTHERS = 2300, (833, 652, 603, 587, 629, 555, 525, 551, 529, 468)
assert len(POLL) == 30
POLL_TOTAL = sum(c for _, _, c in POLL)

# 前回ツアー(2026年's travelers)の当落アンケート(@WS7x10)
PREV_FLASH_URL = "https://x.com/WS7x10/status/1991751044523782225"
PREV_ADD_URL = "https://x.com/WS7x10/status/1997241362559950880"
FC_ARTICLE = ("トラジャのFCはいつ入るのが正解？ツアー発表は毎年10月末！", "travis-japan-fanclub-when-to-join-1643")

# 申込期間中(10/29〜11/1)のXの投稿から、会場ごとの「申し込む理由」「迷う理由」を要約(引用はしない)
SNS_READ = 140
VOICES = [
    ("横浜アリーナ", "ツアー初日の1/4に行きたい、毎年の「あけおめ公演」、駅から近くて立地がいい", "1/4〜7が平日で仕事や学校と重なる、他グループの公演と日程が重なる"),
    ("宮城", "前回のツアーに東北の会場がなかった、地元公演がうれしい、ファンサをもらいやすい会場という声も", "1月で雪や寒さが心配、会場までのアクセス、1/16(土)が出勤日"),
    ("福岡", "九州・中国地方から行きやすい、誕生日に公演がある", "同じ週末に福岡で他グループのドーム公演があり、ホテルが高い"),
    ("愛知", "毎年愛知に行っている、Sky Expoは人気が分かれそうでねらい目では", "平らな展示場で見えにくそう、他グループの公演と重なる"),
    ("千葉", "首都圏から近い、日曜は昼夜2回", "会場の評判が分かれる"),
    ("北海道", "旅行を兼ねて行きたい、「北海道は当たりやすい？」という期待", "飛行機の時間が合わない、遠征費がかかる"),
    ("大阪", "思い入れのある城ホール、GWで動きやすい、関西から日帰りできる", "毎年激戦なのに3公演だけ、西日本のファンが集まりそう"),
    ("静岡", "千秋楽(オーラス)、小さめの会場でファンサをもらいやすいという声、静岡グルメも楽しみ", "5月の予定がまだ読めない、夜公演は帰りがきつい"),
]


def avg(v):
    return sum(c for _, c in v[3]) / len(v[3])


def per1000(v, cap=None):
    cap = cap or v[2]
    return avg(v) / cap * 1000 if cap else None


ALL_SHOWS = sorted(((f"{v[1]} {d}", c) for v in VENUES for d, c in v[3]), key=lambda x: -x[1])
SUM_VOTES = sum(c for _, c in ALL_SHOWS)
RANK = sorted((v for v in VENUES if v[2]), key=lambda v: -per1000(v))

ACC = "#7e57c2"
BORDER = "#d9cdf0"
BG = "#f5f2fb"


def n(x):
    return f"{x:,}"


def pct(c):
    return f"{c / SURVEY_TOTAL * 100:.1f}%"


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


def link(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'


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


def bars(rows, maxv):
    # 公演別の回答数を横棒で自前描画(元の集計グラフ画像は使わない)
    items = []
    for label, c in rows:
        w = c / maxv * 100
        items.append(f'''<div style="display:flex;align-items:center;margin:0 0 4px 0;font-size:0.85em;">
<span style="flex:0 0 9.5em;">{label}</span>
<span style="flex:1;background:#eee;border-radius:2px;"><span style="display:block;width:{w:.1f}%;background:{ACC};height:14px;border-radius:2px;"></span></span>
<span style="flex:0 0 3.2em;text-align:right;">{c}</span>
</div>''')
    return wphtml(f'<div style="border:1px solid {BORDER};border-radius:4px;padding:12px 14px;margin:0 0 16px 0;background:#fff;">\n' + "\n".join(items) + "\n</div>")


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


def related(items):
    lis = "\n".join(f'<li style="margin:0 0 6px 0;"><a href="{SITE}{s}">{t}</a></li>' for t, s in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACC};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


def build():
    yoko, miya, fuku, aichi, lala, sapo, osaka, eco = VENUES
    top1, top2, top3 = ALL_SHOWS[:3]
    low = ALL_SHOWS[-1]
    b = []
    b.append(p([
        "Travis Japanの2027年ツアー「Jewelry Basket」は、ファンクラブ受付が11月4日(水)12時で締め切られ、あとは当落を待つだけになりました。",
        "当落を待つあいだに気になるのが、「自分が申し込んだ公演はどれくらい激戦なの？」「当たりやすい会場はある？」というところではないでしょうか。",
        f"この記事では、SNSで集められた申込日程アンケートの{SURVEY_AS_OF}({n(SURVEY_TOTAL)}人分)を使って、公演ごとの申込の多さを一覧にしました。",
        "さらに会場のキャパ(最大収容人数)で割り、1,000席あたりで何件の申込があるかを出して、会場ごとの激戦度を比べています。",
    ]))
    b.append(whatbox([
        "全30公演の申込状況",
        "申込がいちばん多い公演・少ない公演",
        "キャパで割った会場別の激戦度ランキング",
        "第1希望でいちばん人気の公演",
        "SNSの投稿から見る、会場ごとの申し込む理由・迷う理由",
        "数字のうえでねらい目といえる会場",
        "前回ツアーの当選率と追加公演",
        "当選率を見るときの注意点",
        "チケット料金と当落発表の時期",
    ]))

    # ---- per show ----
    b.append(h2("トラジャ2027ツアーの申込状況は？全30公演の申込数"))
    b.append(p([
        "申込状況を公演ごとに並べると、次のとおりです。",
        f"割合は、集計できた{n(SURVEY_TOTAL)}人のうち何%がその公演に申し込んだかを表しています。",
    ]))
    rows = []
    for name, area, cap, shows in VENUES:
        for i, (d, c) in enumerate(shows):
            rows.append([area if i == 0 else "", d, f"{c}件", pct(c)])
    b.append(table2(["会場", "公演", "申込数", "割合"], rows))
    b.append(p([
        f"いちばん多いのは{mark(f'ゴールデンウィークの{top1[0]}で{n(top1[1])}件')}でした。",
        f"集計できた人の{pct(top1[1])}が申し込んでいて、5人に2人の割合です。",
        f"次いで千秋楽の{top2[0]}の{n(top2[1])}件、{top3[0]}の{n(top3[1])}件と、ツアー後半の大阪と静岡が上位に並んでいます。",
        f"反対にいちばん少ないのは{low[0]}の{low[1]}件で、いちばん多い公演の半分以下です。",
    ]))
    b.append(bars([(f"{v[1]} {d}", c) for v in VENUES for d, c in v[3]], top1[1]))
    b.append(minibox([
        ("集計", f"申込日程アンケートの{SURVEY_AS_OF}・{n(SURVEY_TOTAL)}人分"),
        ("注意", "複数の公演を選べるため、公演ごとの申込数を足すと人数より多くなる"),
    ]))

    # ---- per 1000 seats ----
    b.append(h2("会場別の激戦度は？1,000席あたりの申込で比べると"))
    b.append(p([
        "申込の数がそのまま倍率になるわけではありません。",
        "横浜アリーナのように大きい会場は、申込が多くても席も多いからです。",
        f"そこで、会場ごとに1公演あたりの平均申込数を出し、{link(SITE + CAPACITY_ARTICLE[1], '会場の最大収容人数')}で割って、1,000席あたりの数にそろえました。",
    ]))
    rows = []
    for i, v in enumerate(RANK, 1):
        name, area, cap, shows = v
        val = per1000(v)
        cell = f"<strong>{val:.1f}</strong>" if i <= 3 else f"{val:.1f}"
        rows.append([f"{i}位", f"{name}({area})", f"{avg(v):.0f}件", f"{n(cap)}人", cell])
    rows.append(["―", f"{aichi[0]}(愛知)", f"{avg(aichi):.0f}件", "公表なし", "出せない"])
    b.append(table2(["順位", "会場", "1公演あたりの平均申込数", "最大収容人数", "1,000席あたり"], rows))
    b.append(p([
        f"1,000席あたりの数がいちばん大きいのは{mark(f'静岡のエコパアリーナ({per1000(eco):.1f})')}でした。",
        f"いちばん小さい福岡({per1000(fuku):.1f})とくらべると、約{per1000(eco) / per1000(fuku):.1f}倍の差があります。",
        "数字が大きいほど、同じ席の数をより多くの人が取り合っていることになります。",
    ]))

    # ---- first choice poll ----
    pt = sorted(POLL, key=lambda x: -x[2])
    b.append(h2(f"第1希望はどこ？初日の横アリ1/4が{pt[0][2]:,}票"))
    b.append(p([
        "ここまでの数字は、申し込んだ公演をすべて数えたものです。",
        "では、いちばん行きたい「第1希望」に絞るとどうなるのでしょうか。",
        f"全30公演から第1希望を1つだけ選んだ投票の{POLL_AS_OF}(合計{n(POLL_TOTAL)}票)を、公演ごとに並べました。",
    ]))
    rows = []
    last = None
    for area, d, c in POLL:
        rows.append([area if area != last else "", d, f"<strong>{n(c)}票</strong>" if c >= 280 else f"{n(c)}票"])
        last = area
    b.append(table2(["会場", "公演", "第1希望の票数"], rows))
    b.append(p([
        f"第1希望でいちばん多いのは{mark(f'ツアー初日の横浜アリーナ1/4(月)で{pt[0][2]:,}票')}でした。",
        f"2位は千秋楽の静岡5/23(日)夜の{pt[1][2]}票、3位は横浜アリーナ1/5(火)昼の{pt[2][2]}票です。",
        "申込全体では静岡と大阪が上位でしたが、第1希望に絞ると初日と千秋楽の2公演が抜けています。",
        "「本命は初日か千秋楽、ほかの公演もあわせて申し込む」という動きが、2つの数字から見えてきます。",
    ]))
    b.append(minibox([
        ("集計", f"{POLL_AS_OF}・合計{n(POLL_TOTAL)}票"),
        ("注意", "会場ごとに分けて集計していて、横浜1/4〜1/5の分はほかより多くの人の目にふれている"),
    ]))
    b.append(p([
        "横浜アリーナ1/4の票の多さには、集計の見られ方の差もありそうです。",
        f"それでも同じ横浜の集計の中で1/5(火)昼は{POLL[1][2]}票、1/5(火)夜は{POLL[2][2]}票なので、1/4に人気が集まっているのは確かです。",
    ]))

    # ---- SNS voices ----
    b.append(h2("会場ごとの決め手は？申し込む理由と迷う理由"))
    b.append(p([
        f"数字だけでは見えない「なぜその会場を選ぶのか」を知るため、申込期間中(10月29日〜11月1日)のSNSの投稿約{SNS_READ}件を本サイトで読み、会場ごとに整理しました。",
        "ほかのグループの話題や、名義のやりとりに関する投稿はのぞいています。",
    ]))
    b.append(table2(["会場", "申し込む理由", "迷う理由"], [[v, a, c] for v, a, c in VOICES]))
    b.append(p([
        "どの会場にも共通して多かったのが、「土日の公演が多く、仕事や学校との調整が必要」「来年5月までの予定がまだ分からない」という悩みです。",
        "ほかのグループのツアーと日程が重なるかどうかで、申し込む会場を決めている人も目立ちました。",
        "また、ひとりで参加するか、同行者を探してから申し込むかで迷っている声も多く見られました。",
    ]))

    # ---- venue detail ----
    b.append(h2("いちばん激戦なのはどこ？会場ごとに見ると"))
    b.append(h3("エコパアリーナ(静岡)：4公演すべてが約1,000件以上"))
    b.append(p([
        f"エコパアリーナは4公演ともおよそ1,000件以上で、平均は{n(round(avg(eco)))}件です。",
        "最大収容人数は10,000人と、8会場の中では小さめの会場です。",
        f"とくに千秋楽の5月23日(日)夜は{n(eco[3][3][1])}件で、集計できた人の{pct(eco[3][3][1])}が申し込み、全公演で2番目の多さでした。",
        f"同じ日の昼も{n(eco[3][2][1])}件と多く、ツアー最後の2公演に申込が集まっています。",
        "席の数が少ない会場にこれだけ申込が集まっているので、1,000席あたりの数は8会場でいちばん大きくなりました。",
    ]))
    b.append(h3("大阪城ホール(大阪)：5/2昼が全公演で最多"))
    b.append(p([
        f"大阪城ホールは平均{n(round(avg(osaka)))}件と、8会場でいちばん申込が多い会場です。",
        f"5月1日(土)・2日(日)はゴールデンウィーク中の土日で、{mark(f'5月2日昼は{n(osaka[3][1][1])}件と全公演で最多')}でした。",
        f"大阪城ホールはステージの組み方で収容人数が変わり、いちばん大きいCパターン(16,000人)なら1,000席あたり{per1000(osaka):.1f}です。",
        f"これが{mark(f'Bパターン(11,200人)だと{per1000(osaka, OSAKA_B):.1f}')}となり、エコパに近い激戦度になります。",
        "どのパターンで組まれるかは発表されていないので、上の表より激しくなる可能性もある会場です。",
    ]))
    b.append(h3("セキスイハイムスーパーアリーナ(宮城)：小さい会場で数字が上がる"))
    b.append(p([
        f"宮城は1公演あたりの平均が{avg(miya):.0f}件と、申込数だけ見ると多くはありません。",
        f"ただ、収容人数が7,063席と8会場でいちばん小さいため、1,000席あたりでは{per1000(miya):.1f}と上位に入りました。",
        "3公演とも646〜686件とほぼ同じで、昼と夜の差もほとんどありません。",
    ]))
    b.append(h3("ららアリーナ 東京ベイ(千葉)：金曜の3/26だけ少なめ"))
    b.append(p([
        f"千葉は5公演の平均が{avg(lala):.0f}件で、1,000席あたりは{per1000(lala):.1f}です。",
        "土日の4公演は849〜1,002件なのに対して、平日の3月26日(金)は731件と少なめでした。",
        "同じ会場の中でも、平日の公演は申込が少ない傾向が見えます。",
    ]))
    b.append(h3("横浜アリーナ(神奈川)：初日1/4に申込が集中"))
    b.append(p([
        f"横浜アリーナは6公演の平均が{avg(yoko):.0f}件と、申込数では上位です。",
        f"それでも最大17,000人と大きい会場なので、1,000席あたりでは{per1000(yoko):.1f}と、ちょうど真ん中あたりでした。",
        f"6公演の中では{mark('ツアー初日の1月4日(月)が1,125件')}と飛びぬけていて、ほかの5公演は890〜966件です。",
    ]))

    # ---- nerai-me ----
    b.append(h2("ねらい目の会場は？数字のうえでは福岡と北海道"))
    b.append(p([
        f"1,000席あたりの数が小さいのは、{mark(f'福岡のマリンメッセ({per1000(fuku):.1f})と北海道の真駒内({per1000(sapo):.1f})')}です。",
        f"福岡は最大15,000人と大きい会場なのに、平均の申込数は{avg(fuku):.0f}件でした。",
        f"北海道は3公演とも481〜516件と全公演の中でいちばん少なく、4月3日(土)昼の{low[1]}件が最少です。",
    ]))
    b.append(p([
        f"愛知は1公演あたり平均{avg(aichi):.0f}件で、宮城や福岡と同じくらいの数でした。",
        "ただし、Aichi Sky Expoは公式に収容人数が出ていないため、1,000席あたりの数は出していません。",
    ]))

    # ---- caution ----
    b.append(h2("当選率はわかる？数字を見るときの注意点"))
    b.append(p([
        "この記事の数字から、実際の当選率(倍率)そのものを出すことはできません。",
        f"集計できたのは{n(SURVEY_TOTAL)}人分で、申し込んだファン全体のごく一部だからです。",
        "わかるのは、「どの会場・どの公演に申込が集まっているか」という会場どうしの比べ合いです。",
    ]))
    b.append(minibox([
        ("集計の範囲", "集計できた人の分だけで、申込全体の数ではない"),
        ("収容人数", "会場の最大の数字で、実際に販売される席はこれより少なくなることが多い"),
        ("複数選択", f"1人で複数の公演を申し込んだ人をふくむ(公演ごとの合計は{n(SUM_VOTES)}件)"),
        ("集計の時点", "申込日程アンケート・第1希望の投票とも、11月3日締切の最終結果"),
    ]))
    b.append(p([
        "とくに大阪城ホールはステージの組み方、愛知は収容人数が分からないため、ほかの会場より誤差が大きくなります。",
        "当落を待つあいだの、ひとつの目安として見てください。",
    ]))

    # ---- previous tour ----
    add_lost_win = 15.1 / (15.1 + 33.7) * 100
    b.append(h2("前回ツアーの当選率は？速報では7割前後が当選"))
    b.append(p([
        "参考までに、前回の2026年ツアー「's travelers」の当落も振り返っておきます。",
        f"当落発表の2025年11月21日の当選・落選の集計では、発表直後(15時10分時点)の速報で{mark('当選が70〜75%')}でした。",
        "集計できた人の中では、7割前後が当選していたことになります。",
    ]))
    b.append(p([
        f'前回は当落発表の日に追加公演が出ていて、会員受付は11月21日15時〜25日12時でした(<a href="{SITE}{FC_ARTICLE[1]}">{FC_ARTICLE[0]}</a>でも紹介しています)。',
        "追加公演の当落の集計(最終1,059票)では、1回目に落選していた人の結果は次のとおりです。",
    ]))
    b.append(table2(["1回目の結果", "追加公演の結果", "割合"], [
        ["当選", "当選", "11.1%"],
        ["当選", "落選", "40.0%"],
        ["落選", "当選", "15.1%"],
        ["落選", "落選", "33.7%"],
    ]))
    b.append(p([
        f"1回目に落選した人だけで見ると、{mark(f'約{add_lost_win:.0f}%が追加公演で当選')}しています。",
        "今回も追加公演があるかはまだ分かりませんが、当落発表の日は公式の案内もチェックしておくと安心です。",
    ]))
    b.append(minibox([
        ("注意", "集計できた人だけの数字。発表直後の速報は、当選した人ほど早く報告する傾向もある"),
    ]))

    # ---- ticket ----
    b.append(h2("チケット料金と当落発表はいつ？"))
    b.append(minibox([
        ("会員チケット料金", "1枚10,300円(指定/立見・税込)"),
        ("申込手数料", "当選した場合に別途800円"),
        ("FC受付", "2026年10月29日(木)11:00〜11月4日(水)12:00(受付終了)"),
        ("抽選結果", "11月20日(金)以降に案内"),
    ]))
    b.append(p([
        "ファンクラブの受付は11月4日(水)の12時で締め切られました。",
        f"抽選結果は{mark('11月20日(金)以降')}に案内される予定です。",
        "前回のツアーも当落発表は11月21日だったので、今回も同じくらいの時期になりそうです。",
        f'公演ごとの開演時間は<a href="{SITE}{SCHEDULE_ARTICLE[1]}">{SCHEDULE_ARTICLE[0]}</a>でまとめています。',
    ]))

    # ---- matome ----
    b.append(h2("まとめ"))
    b.append(checklist("この記事のポイント", [
        f"申込日程アンケートの最終集計({n(SURVEY_TOTAL)}人分)で、いちばん多いのは大阪5/2昼({n(top1[1])}件)、2位は千秋楽の静岡5/23夜",
        f"1,000席あたりの申込でくらべると、いちばん激戦なのはエコパアリーナ({per1000(eco):.1f})",
        f"大阪城ホールはBパターン(11,200人)なら{per1000(osaka, OSAKA_B):.1f}で、エコパに近い激戦度",
        f"数字のうえでねらい目なのは福岡({per1000(fuku):.1f})と北海道({per1000(sapo):.1f})",
        f"第1希望に絞ると初日の横アリ1/4が{pt[0][2]:,}票で断トツ、2位は千秋楽の静岡5/23夜",
        "SNSの声では、日程の都合・他グループとの重なり・遠征のしやすさが会場選びの決め手",
        "前回ツアーは速報で当選70〜75%、1回目落選の約3割が追加公演で当選",
        "同じ会場でも、横アリは初日の1/4、千葉は土日に申込が集まっている",
        "当選率そのものではなく、会場どうしを比べる目安",
        "FC受付は11月4日(水)12:00で終了、抽選結果は11月20日(金)以降",
    ]))
    b.append(p([
        "当落の結果が出たら、当選・落選の集計もこの記事に追記します！",
    ]))
    b.append(related([
        SCHEDULE_ARTICLE,
        CAPACITY_ARTICLE,
        FC_ARTICLE,
    ]))
    return "\n\n".join(b)


def upload_media(path, title, alt=""):
    ctype = "image/png" if path.suffix == ".png" else "image/jpeg"
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers={
        **HEADERS_AUTH, "Content-Disposition": f'attachment; filename="{path.name}"', "Content-Type": ctype},
        data=path.read_bytes())
    r.raise_for_status()
    m = r.json()
    if alt:
        requests.post(f"{WP_URL}/wp-json/wp/v2/media/{m['id']}", headers=HJSON, json={"alt_text": alt, "title": title})
    return {"id": m["id"], "url": m["source_url"]}


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    html = build()
    if DRY:
        (IMG_DIR / "_dry.html").write_text(html, encoding="utf-8")
        print("dry chars:", len(html), "votes:", SUM_VOTES)
        for v in RANK:
            print(v[1], round(per1000(v), 1))
        return
    tmp = IMG_DIR / "_post.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis", str(tmp)], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "check", "--group", "travis", str(tmp)], check=True)
    html = tmp.read_text(encoding="utf-8")
    if "--update-live" in sys.argv:
        # published post: replace content only, keep title/status/eyecatch as they are
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{state['post_id']}", headers=HJSON, json={"content": html})
        r.raise_for_status()
        post = r.json()
        print("updated", post["id"], post["status"], post["link"], "chars", len(html))
        return
    if not EYECATCH.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
                        "--main", "2027ツアー", "--bottom", "会場別の倍率は？",
                        "--bottom", "申込状況を比較", "--color-key", "group", "--out", str(EYECATCH)], check=True)
    if "eyecatch" not in state:
        state["eyecatch"] = upload_media(EYECATCH, TITLE, TITLE.replace("【未】", ""))
        STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    body = {"title": TITLE, "slug": SLUG, "content": html, "status": "draft",
            "categories": [3], "author": 2, "featured_media": state["eyecatch"]["id"]}
    if "post_id" in state:
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{state['post_id']}", headers=HJSON, json=body)
    else:
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, json=body)
    r.raise_for_status()
    post = r.json()
    state["post_id"] = post["id"]
    STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    print("post", post["id"], post["status"], post["link"], "chars", len(html))


if __name__ == "__main__":
    main()
