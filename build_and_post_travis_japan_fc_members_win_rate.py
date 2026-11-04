# -*- coding: utf-8 -*-
# chomoand-4.blog: トラジャのFC会員数と当選率の推移(@WS7x10のまとめポスト)+2027ツアーの規模から当選率を予想
# 会員数・当選率は公式発表ではなくSNSでまとめられた数字。2027ツアーのキャパは venue_capacity(2006)、申込数は odds_survey(2115)と同じ数字
import json, sys, subprocess
from pathlib import Path
import requests

from build_and_post_travis_japan_tour2027_odds_survey import (
    ROOT, WP_URL, HJSON, SITE, ACC, BORDER, BG, n, p, h2, h3, wphtml, mark, link,
    whatbox, minibox, table2, checklist, related, upload_media,
    VENUES as TOUR2027, SURVEY_TOTAL, SUM_VOTES, OSAKA_B)

IMG_DIR = ROOT / "images" / "tj_fc_members_win_rate"
EYECATCH = IMG_DIR / "tj_fc_members_win_rate_eyecatch_canva.jpg"
STATE = IMG_DIR / "_state.json"
DRY = "--dry" in sys.argv

TITLE = "【未】トラジャのFC会員数は何人？当選率の推移と2027ツアーの予想"
SLUG = "travis-japan-fc-members-win-rate"

SRC_URL = "https://x.com/WS7x10/status/2115653428961812858"
# 2027ツアー申込時期の会員数: @WS7x10「FC会員数 10月末速報版」(10/24)で31万。
# 10/30〜11/2に「新規入会の会員番号が32万台」という投稿が複数(例: 11/2「32万4千くらい」)
SRC_2027_URL = "https://x.com/WS7x10/status/2113919405872881941"
MEMBERS_2027 = 31
MEMBERS_2027_NO = 32  # member-number basis

# (年, ツアー名, 都市, 公演, 動員(万), 会員数(万), 当選率%)
TOURS = [
    (2023, "THE SHOW〜ただいま、おかえり〜", 5, 23, 23.5, 13, 92.2),
    (2024, "Road to Authenticity", 8, 29, 31, 15, 92.9),
    (2025, "VIIsual", 8, 28, 31, 19, 88.2),
    (2026, "'s travelers", 8, 29, 32, 25, 69.2),
]

ODDS_ARTICLE = ("トラジャ2027ツアーの倍率は？会場別の申込状況を比較！", "travis-japan-2027-tour-odds-by-venue-2115")
CAPACITY_ARTICLE = ("トラジャ2027ツアー会場のキャパは？収容人数と公演数まとめ！", "travis-japan-2027-tour-venue-capacity-2006")
SCHEDULE_ARTICLE = ("トラジャ2027ツアー『Jewelry Basket』の会場・日程まとめ！", "travis-japan-2027-tour-jewelry-basket-schedule-1973")
FC_ARTICLE = ("トラジャのFCはいつ入るのが正解？ツアー発表は毎年10月末！", "travis-japan-fanclub-when-to-join-1643")
PRODUCE_ARTICLE = ("トラジャのアルバム・コンサートは毎年違うメンバーがプロデュース？", "is-toraja-concert-produced-by-214")

SHOWS_2027 = sum(len(v[3]) for v in TOUR2027)
CAP_2027_KNOWN = sum(v[2] * len(v[3]) for v in TOUR2027 if v[2])  # Aichi excluded (capacity not published)
SEATS_2027 = 35  # 万, rough: known 7 venues (34.6万) + Aichi, max capacity basis
assert SHOWS_2027 == 30


def ratio(t):
    return t[4] / t[5]


def hbars(rows, maxv, unit):
    items = []
    for label, v in rows:
        items.append(f'''<div style="display:flex;align-items:center;margin:0 0 6px 0;font-size:0.9em;">
<span style="flex:0 0 7.5em;">{label}</span>
<span style="flex:1;background:#eee;border-radius:2px;"><span style="display:block;width:{v / maxv * 100:.1f}%;background:{ACC};height:16px;border-radius:2px;"></span></span>
<span style="flex:0 0 4.2em;text-align:right;">{v:g}{unit}</span>
</div>''')
    return wphtml(f'<div style="border:1px solid {BORDER};border-radius:4px;padding:12px 14px;margin:0 0 16px 0;background:#fff;">\n' + "\n".join(items) + "\n</div>")


def build():
    show, road, viis, trav = TOURS
    b = []
    b.append(p([
        f"Travis Japanのファンクラブ会員数は公式には発表されていませんが、SNSの投稿をもとにした数字では、{mark('2026年10月末の時点で約31万人')}とされています。",
        "10月末には、新しく入会した人の会員番号が32万台になったという投稿もいくつも見られました。",
        "デビュー直後の2023年は約13万人だったので、4年でおよそ2.4倍に増えたことになります。",
        "一方でツアーの当選率は、2023年〜2024年の92%台から、2026年の「's travelers」では69.2%まで下がりました。",
        "この記事では、過去4回のツアーの会員数・公演の規模・当選率を並べて、2027年ツアー「Jewelry Basket」の当選率がどうなりそうかを予想します。",
    ]))
    b.append(whatbox([
        "トラジャのファンクラブ会員数の推移",
        "過去4回のツアーの当選率",
        "当選率が下がった理由(会員数と席の数のバランス)",
        "2027年ツアー「Jewelry Basket」の規模",
        "2027年ツアーの当選率の予想",
        "申込が少なめの会場と追加公演",
        "当落発表の時期",
    ]))

    # ---- members ----
    b.append(h2(f"トラジャのFC会員数は何人？最新は約{MEMBERS_2027}万人"))
    b.append(p([
        "SNSの投稿をもとに、ツアーごとの会員数を並べると次のとおりです。",
        "2027年ツアーは、申込が始まった2026年10月末ごろの数字を入れています。",
        "どれもファンクラブの公式発表ではなく、各ツアーの申込時期の目安として見てください。",
    ]))
    rows = []
    prev = None
    for y, name, *_rest in TOURS:
        m = _rest[3]
        rows.append([f"{y}年", name, f"約{m}万人", "―" if prev is None else f"+{m - prev}万人"])
        prev = m
    rows.append(["<strong>2027年</strong>", "Jewelry Basket", f"<strong>約{MEMBERS_2027}万人</strong>", f"+{MEMBERS_2027 - prev}万人"])
    b.append(table2(["年", "ツアー", "会員数", "前回からの増え方"], rows))
    b.append(hbars([(f"{t[0]}年", t[5]) for t in TOURS] + [("2027年", MEMBERS_2027)], MEMBERS_2027, "万人"))
    b.append(p([
        "デビュー記念の2023年ツアーのときは約13万人でした。",
        f"そこから15万人、19万人、25万人、{MEMBERS_2027}万人と増えていて、{mark('ここ2年は1年で6万人ずつ増えている')}のが分かります。",
        "前回からの増え方は+2万人、+4万人、+6万人、+6万人です。",
        "テレビやドラマでメンバーを見かける機会が増え、新しくファンクラブに入った人が多かったと考えられます。",
    ]))
    b.append(h3("10月末には会員番号が32万台に"))
    b.append(p([
        "2027年ツアーが発表された10月末ごろ、SNSでは「会員数が増えた」という投稿が多く見られました。",
        "10月20日ごろには「会員数が31万人になっていた」という投稿があり、10月30日には「もうすぐ32万人」という声が出ています。",
        f"10月31日〜11月2日には、{mark('新しく入会した人の会員番号が32万台だった')}という投稿がいくつも続きました。",
        "ツアーの発表とアルバムの発売が重なったこの時期に、新しくファンクラブに入った人が多かったようです。",
    ]))
    b.append(p([
        "ただし、会員番号は退会した人の番号もふくめて順番につけられるため、会員番号の数がそのまま今の会員数になるわけではありません。",
        f"そのため、この記事では10月末の速報の約{MEMBERS_2027}万人を会員数として使い、会員番号の32万台は参考として紹介します。",
        "ほかの投稿でも「会員数が増えたから今年は当たるか不安」という声が目立ち、ファンのあいだでも当選率を気にする人が増えています。",
    ]))
    b.append(minibox([
        ("数字の出どころ", "SNSの投稿をもとにした数字(ファンクラブの公式発表ではない)"),
        ("注意", "会員数は「約〇万人」の目安で、ツアーごとの申込の時期の数字"),
    ]))

    # ---- win rate ----
    b.append(h2("当選率の推移は？92%台から69.2%へ"))
    b.append(p([
        "当選率についても、SNSの投稿をもとにした数字を見ていきます。",
        "公演の規模(都市・公演数・動員)とあわせて並べると、次のとおりです。",
    ]))
    b.append(table2(["年", "ツアー", "規模", "当選率"], [
        [f"{t[0]}年", t[1], f"{t[2]}都市{t[3]}公演・{t[4]:g}万人", f"<strong>{t[6]}%</strong>" if t is trav else f"{t[6]}%"]
        for t in TOURS]))
    b.append(hbars([(f"{t[0]}年", t[6]) for t in TOURS], 100, "%"))
    b.append(p([
        "2023年の「THE SHOW」と2024年の「Road to Authenticity」は、どちらも当選率が92%台でした。",
        "申し込んだ人のほとんどが当たっていた計算です。",
        f"2025年の「VIIsual」で88.2%に少し下がり、2026年の「's travelers」では{mark('69.2%と一気に20ポイント近く下がりました')}。",
        "前回は、申し込んだ人のおよそ3人に1人が落選していたことになります。",
    ]))
    b.append(p([
        f'前回ツアーの当落発表の直後には、当選が70〜75%という速報の集計も出ていました(<a href="{SITE}{ODDS_ARTICLE[1]}">{ODDS_ARTICLE[0]}</a>で紹介しています)。',
        "最終的な69.2%は、この速報と近い数字です。",
    ]))
    b.append(minibox([
        ("注意", "SNSの投稿をもとにした数字で、公式の当選率ではない"),
        ("数え方", "1回の申込ごとか、1人ごとかはまとめには書かれていない"),
    ]))

    # ---- why ----
    b.append(h2("なぜ当選率が下がった？会員数と席の数のバランス"))
    b.append(p([
        "当選率が下がったいちばんの理由は、会員数の増え方に席の数が追いついていないことです。",
        "公演の規模は2024年から31万人、31万人、32万人とほぼ同じなのに、会員数は15万人から25万人に増えました。",
        "そこで、動員の数を会員数で割って「会員1人あたり何席あるか」を出してみました。",
    ]))
    b.append(table2(["年", "動員", "会員数", "会員1人あたりの席", "当選率"], [
        [f"{t[0]}年", f"{t[4]:g}万人", f"{t[5]}万人", f"<strong>{ratio(t):.2f}席</strong>" if t is trav else f"{ratio(t):.2f}席", f"{t[6]}%"]
        for t in TOURS]))
    b.append(p([
        f"2024年は会員1人あたり{ratio(road):.2f}席あり、全員が2公演ずつ行ってもまだ席が余る計算でした。",
        f"それが2026年には{mark(f'{ratio(trav):.2f}席')}まで減っています。",
        f"1人あたりの席が{ratio(viis):.2f}席から{ratio(trav):.2f}席に減ったタイミングで、当選率も88.2%から69.2%に下がりました。",
        "会員1人あたりの席の数と当選率が、ほぼ同じ動きをしているのが分かります。",
    ]))
    b.append(p([
        "ただし、会員全員が申し込むわけではありませんし、1人で何公演も申し込む人もいます。",
        "この数字は当選率をそのまま計算するものではなく、年ごとの厳しさを比べる目安として見てください。",
    ]))

    # ---- 2027 scale ----
    b.append(h2("2027年ツアーの規模は？8都市30公演"))
    b.append(p([
        f"2027年ツアー「Jewelry Basket」は、1月4日の横浜アリーナから5月23日のエコパアリーナまで、8都市{SHOWS_2027}公演です。",
        "前回の29公演より1公演多くなりました。",
    ]))
    b.append(table2(["会場", "公演数", "最大収容人数"], [
        [f"{v[0]}({v[1]})", f"{len(v[3])}公演", f"{n(v[2])}人" if v[2] else "公表なし"] for v in TOUR2027]))
    b.append(p([
        f"公式に収容人数が出ていない愛知をのぞいた7会場だけで、最大収容人数×公演数は{mark(f'約{CAP_2027_KNOWN / 10000:.1f}万人')}になります。",
        "愛知の3公演を足すと、前回の32万人を上回る規模になりそうです。",
        "ただし最大収容人数はステージを組む前の数字なので、実際に販売される席はこれより少なくなることが多いです。",
        f'会場ごとの収容人数は<a href="{SITE}{CAPACITY_ARTICLE[1]}">{CAPACITY_ARTICLE[0]}</a>でくわしくまとめています。',
    ]))

    # ---- 2027 prediction ----
    b.append(h2("2027年ツアーの当選率は？前回並みか、さらに厳しくなる可能性"))
    b.append(p([
        f"2027年ツアーの申込時期の会員数は約{MEMBERS_2027}万人、会員番号では32万台でした。",
        f"席の数を最大収容人数をもとに約{SEATS_2027}万席として、前回とくらべてみます。",
    ]))
    scen = [
        ("前回のままの約25万人だったら", 25),
        (f"10月末の速報の約{MEMBERS_2027}万人", MEMBERS_2027),
        (f"会員番号の約{MEMBERS_2027_NO}万人", MEMBERS_2027_NO),
    ]
    rows = []
    for label, m in scen:
        r = SEATS_2027 / m
        if r > ratio(trav) + 0.05:
            cmp = "前回より少しゆとりがある"
        elif r >= ratio(trav) - 0.05:
            cmp = "前回とほぼ同じ"
        else:
            cmp = "前回より厳しい"
        rows.append([label, f"{r:.2f}席", cmp])
    b.append(table2(["会員数のパターン", "会員1人あたりの席", "前回(1.28席)とくらべて"], rows))
    b.append(p([
        f"公演の規模は前回より少し大きくなるので、会員数が前回のままなら1人あたりの席は{SEATS_2027 / 25:.2f}席で、少しゆとりが出るはずでした。",
        f"ところが実際には会員数が約{MEMBERS_2027}万人まで増えているので、1人あたりの席は{SEATS_2027 / MEMBERS_2027:.2f}席です。",
        f"前回の{ratio(TOURS[-1]):.2f}席より少なく、{mark('当選率は前回の69.2%より厳しくなる')}可能性が高いといえます。",
        "最大収容人数で計算しているぶん実際の席はもっと少ないので、数字以上に厳しくなることも考えておいたほうがよさそうです。",
    ]))
    b.append(p([
        f"申込日程アンケートの最終集計では、{n(SURVEY_TOTAL)}人が合計{n(SUM_VOTES)}件の公演に申し込んでいました。",
        f"1人あたり平均で{mark(f'約{SUM_VOTES / SURVEY_TOTAL:.1f}公演')}に申し込んでいる計算です。",
        "アンケートに答えるのは熱心なファンが多いとはいえ、多くの人が複数の公演に申し込んでいることが分かります。",
    ]))
    b.append(minibox([
        ("席の数", f"愛知をのぞく7会場の最大収容人数×公演数(約{CAP_2027_KNOWN / 10000:.1f}万人)に愛知を足した目安"),
        ("会員数", f"10月末の速報(約{MEMBERS_2027}万人)と、SNSの投稿にあった会員番号(32万台)"),
        ("注意", "当選率そのものの予想ではなく、前回とくらべた厳しさの目安"),
    ]))

    # ---- tips ----
    b.append(h2("当たりやすい会場はある？申込の少ない会場と追加公演"))
    hok = TOUR2027[5]
    fuk = TOUR2027[2]
    b.append(p([
        f'同じ申込日程アンケートを会場ごとに見ると、申込がいちばん少なかったのは{mark("北海道の真駒内")}で、3公演とも{min(c for _, c in hok[3])}〜{max(c for _, c in hok[3])}件でした。',
        f"福岡のマリンメッセも{min(c for _, c in fuk[3])}〜{max(c for _, c in fuk[3])}件と少なく、最大収容人数も15,000人と大きい会場です。",
        "反対に、千秋楽の静岡や、ゴールデンウィークの大阪には申込が集まっています。",
        f'会場ごとの申込の多さは<a href="{SITE}{ODDS_ARTICLE[1]}">{ODDS_ARTICLE[0]}</a>でくわしく比べています。',
    ]))
    b.append(p([
        "前回のツアーでは、当落発表の日に追加公演が発表されました。",
        "追加公演の当落の集計では、1回目に落選した人の約3割が追加公演で当選しています。",
        "今回も追加公演があるかはまだ分かりませんが、もし落選しても、当落発表の日の公式の案内はチェックしておきましょう。",
    ]))

    # ---- schedule ----
    b.append(h2("2027年ツアーの当落発表はいつ？"))
    b.append(minibox([
        ("FC受付", "2026年10月29日(木)11:00〜11月4日(水)12:00(受付終了)"),
        ("抽選結果", "11月20日(金)以降に案内"),
        ("前回の当落発表", "2025年11月21日"),
    ]))
    b.append(p([
        "ファンクラブの受付は11月4日(水)12時で締め切られました。",
        f"抽選結果は{mark('11月20日(金)以降')}に案内される予定です。",
        "前回は11月21日、前々回は11月25日に当落が出ていたので、今回も11月の下旬になりそうです。",
        f'過去のツアーの発表日や受付期間は<a href="{SITE}{FC_ARTICLE[1]}">{FC_ARTICLE[0]}</a>で一覧にしています。',
    ]))

    # ---- matome ----
    b.append(h2("まとめ"))
    b.append(checklist("この記事のポイント", [
        f"トラジャのFC会員数は公式発表なし、SNSの投稿をもとにした数字では2026年10月末で約{MEMBERS_2027}万人",
        "10月末には新しく入会した人の会員番号が32万台に",
        f"会員数は13万→15万→19万→25万→{MEMBERS_2027}万人と、ここ2年は1年で6万人ずつ増えている",
        "当選率は92.2%→92.9%→88.2%→69.2%と、前回ツアーで大きく下がった",
        f"会員1人あたりの席は{ratio(road):.2f}席(2024年)から{ratio(trav):.2f}席(2026年)に減った",
        f"2027年ツアーは8都市{SHOWS_2027}公演で、規模は前回を上回りそう",
        f"会員1人あたりの席は約{SEATS_2027 / MEMBERS_2027:.2f}席で、当選率は前回の69.2%より厳しくなる可能性が高い",
        "申込が少なめなのは北海道と福岡",
        "抽選結果は11月20日(金)以降に案内",
    ]))
    b.append(p([
        "当落の結果が出たら、2027年ツアーの当選率もこの記事に追記します！",
    ]))
    b.append(related([ODDS_ARTICLE, CAPACITY_ARTICLE, SCHEDULE_ARTICLE, FC_ARTICLE, PRODUCE_ARTICLE]))
    return "\n\n".join(b)


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    html = build()
    if DRY:
        (IMG_DIR / "_dry.html").write_text(html, encoding="utf-8")
        print("dry chars:", len(html), "cap2027 known:", CAP_2027_KNOWN)
        return
    tmp = IMG_DIR / "_post.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis", str(tmp)], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "check", "--group", "travis", str(tmp)], check=True)
    html = tmp.read_text(encoding="utf-8")
    if not EYECATCH.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
                        "--main", "FC会員数", "--bottom", "何人？当選率の推移と",
                        "--bottom", "2027ツアーの予想", "--color-key", "group", "--out", str(EYECATCH)], check=True)
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
