# -*- coding: utf-8 -*-
# chomoand-4.blog: トラジャ2027ツアー「Jewelry Basket」FC先行の当落結果・当選率(倍率)を、当落当日(2026-11-20 15:00発表)のSNSアンケートからまとめる
# 数字の出どころ(本文ではアカウント名・リンクを出さない=docs/rules.md「SNS数字は『SNSの投稿をもとにした』」):
#   全体・会場別: @ticket_festa の当落アンケート(全体1本+会場別8本、締切11/21 15:02) https://x.com/ticket_festa/status/2123658306418053537
#   会員番号別: @WS7x10 のゾーン別当落アンケート(3本、締切11/21 3:00) https://x.com/WS7x10/status/2123657796273217772
#   取得: fxtwitter API 2026-11-20 18:30ごろ(途中経過)。締切後に数字を差し替えて再実行する(state保存、同じIDを上書き)
# 当落時刻15:00は @WS7x10 当落時刻ポスト(2123658139828666803)とX上の当選報告(15時台)で確認
import json, sys, subprocess
from pathlib import Path
import requests

from build_and_post_travis_japan_tour2027_odds_survey import (
    ROOT, WP_URL, HJSON, SITE, ACC, BORDER, n, p, h2, h3, wphtml, mark,
    whatbox, minibox, table2, checklist, related, upload_media, VENUES as TOUR2027)

IMG_DIR = ROOT / "images" / "tj_toraku_result_2027"
EYECATCH = IMG_DIR / "tj_toraku_result_2027_eyecatch_canva.jpg"
STATE = IMG_DIR / "_state.json"
DRY = "--dry" in sys.argv

BASE_TITLE = "トラジャ2027ツアーの当落倍率は？当選率を会場別に調査！"
TITLE = "【未】" + BASE_TITLE
assert len(BASE_TITLE) <= 35, len(BASE_TITLE)
SLUG = "travis-japan-2027-tour-toraku-result"

AS_OF = "11月20日18時半ごろ"
FINAL = False  # True after the polls close (11/21) and the numbers are replaced

# 全体(当選, 落選) ※「閲覧用」は除く
OVERALL = (2793, 981)
PREV_SAME_SURVEY = 78.5  # 前回's travelersの同じ形式の調査(当落直前の投稿で紹介されていた数字)
PREV_FINAL = 69.2        # 前回の当選率(2197と同じ、SNSでまとめられた最終の数字)

# 会場別(会場名, 当選, 落選) ※TOUR2027と同じ順番
VENUE_RESULTS = [
    ("横浜アリーナ", 359, 212),
    ("セキスイハイムスーパーアリーナ", 101, 123),
    ("マリンメッセ福岡A館", 155, 147),
    ("Aichi Sky Expo Aホール", 148, 146),
    ("ららアリーナ 東京ベイ", 355, 201),
    ("真駒内セキスイハイムアイスアリーナ", 102, 143),
    ("大阪城ホール", 139, 337),
    ("エコパアリーナ", 218, 312),
]
assert [v[0] for v in VENUE_RESULTS] == [v[0] for v in TOUR2027]

# 会員番号別(ゾーン, 当選, 落選)
ZONES = [
    ("1番〜4万番台", 2312, 1020),
    ("5万〜9万番台", 1657, 967),
    ("10万〜14万番台", 821, 482),
    ("15万〜19万番台", 1307, 716),
    ("20万〜24万番台", 1396, 677),
    ("25万〜30万番台以降", 2118, 1305),
]

ODDS_ARTICLE = ("トラジャ2027ツアーの倍率は？会場別の申込状況を比較！", "travis-japan-2027-tour-odds-by-venue-2115")
WINRATE_ARTICLE = ("トラジャ2027ツアーの当選率は？FC会員数と過去の推移から予想！", "travis-japan-2027-tour-win-rate-2197")
TIME_ARTICLE = ("トラジャ当落は何時？2027ツアーの発表時間を過去4回から予想！", "travis-japan-toraku-time-3230")
SEATED_ARTICLE = ("トラジャの着ブロは当たりにくい？当選率と席の位置は？", "travis-japan-seated-block-odds-2159")
CAPACITY_ARTICLE = ("トラジャ2027ツアー会場のキャパは？収容人数と公演数まとめ！", "travis-japan-2027-tour-venue-capacity-2006")
SCHEDULE_ARTICLE = ("トラジャ2027ツアー『Jewelry Basket』の会場・日程まとめ！", "travis-japan-2027-tour-jewelry-basket-schedule-1973")
CD_ARTICLE = ("トラジャのアルバムCD延期はなぜ？発売記念イベントはどうなる？", "travis-japan-jewelry-basket-cd-postponed-2505")


def rate(w, l):
    return w / (w + l) * 100


def odds(w, l):
    return (w + l) / w


def short(name):
    return {"横浜アリーナ": "横浜", "セキスイハイムスーパーアリーナ": "宮城", "マリンメッセ福岡A館": "福岡",
            "Aichi Sky Expo Aホール": "愛知", "ららアリーナ 東京ベイ": "千葉", "真駒内セキスイハイムアイスアリーナ": "北海道",
            "大阪城ホール": "大阪", "エコパアリーナ": "静岡"}[name]


def hbars(rows):
    items = []
    for label, v in rows:
        items.append(f'''<div style="display:flex;align-items:center;margin:0 0 6px 0;font-size:0.9em;">
<span style="flex:0 0 8.5em;">{label}</span>
<span style="flex:1;background:#eee;border-radius:2px;"><span style="display:block;width:{v:.1f}%;background:{ACC};height:16px;border-radius:2px;"></span></span>
<span style="flex:0 0 4.2em;text-align:right;">{v:.1f}%</span>
</div>''')
    return wphtml(f'<div style="border:1px solid {BORDER};border-radius:4px;padding:12px 14px;margin:0 0 16px 0;background:#fff;">\n' + "\n".join(items) + "\n</div>")


def build():
    ow, ol = OVERALL
    o_rate = rate(ow, ol)
    zw = sum(z[1] for z in ZONES)
    zl = sum(z[2] for z in ZONES)
    z_rate = rate(zw, zl)
    lo, hi = sorted([o_rate, z_rate])
    vr = sorted(((short(v[0]), rate(v[1], v[2]), odds(v[1], v[2]), v) for v in VENUE_RESULTS), key=lambda x: -x[1])
    best, worst = vr[0], vr[-1]
    zr = [(z[0], rate(z[1], z[2])) for z in ZONES]
    when = "最終集計" if FINAL else f"{AS_OF}の途中経過"

    b = []
    b.append(p([
        f"Travis Japanの2027年ツアー「Jewelry Basket」のFC先行の当落が、11月20日(金)15時に発表されました。",
        f"SNSの当落アンケートをもとにすると、当選率は{mark(f'約{lo:.0f}〜{hi:.0f}%')}、倍率にすると{mark(f'約{100 / hi:.2f}〜{100 / lo:.2f}倍')}です。",
        f"前回のツアーの当選率は69.2%だったので、前回と同じくらいか少し厳しい結果になりました。",
        f"会場別では{best[0]}がいちばん当たりやすく、{mark(f'{worst[0]}は当選率{worst[1]:.0f}%')}といちばんの激戦でした。",
        "この記事では、当落アンケートの結果をもとに、全体・会場別・会員番号別の当選率と倍率をまとめます。",
    ]))
    b.append(whatbox([
        "2027年ツアーの当落発表の日時",
        "全体の当選率と倍率",
        "会場別の当選率と倍率(当たりやすい会場・激戦の会場)",
        "会員番号別の当選率(古い会員ほど当たる？)",
        "前回ツアーとの比較",
        "X(旧Twitter)での当落の反応",
        "落選したときのこれからのチャンス",
    ]))

    # ---- announce ----
    b.append(h2("トラジャ2027ツアーの当落発表はいつ？11月20日15時"))
    b.append(minibox([
        ("ツアー名", "Travis Japan Concert Tour 2027「Jewelry Basket」"),
        ("当落発表", "2026年11月20日(金)15:00ごろ"),
        ("対象", "ファンクラブ(FC)先行の抽選"),
        ("支払い期限", "11月24日(火)23:59"),
        ("公演", "2027年1月4日〜5月23日・8都市30公演"),
    ]))
    b.append(p([
        "当落(とうらく)とは、チケットの抽選に当たったか外れたかの結果のことです。",
        f"今回の当落は{mark('11月20日(金)の15時ごろ')}に出て、15時すぎからXには「当選した」「落選した」という投稿が一気に増えました。",
        "トラジャのツアーの当落は2024年・2025年も15時で、3年続けて15時の発表になりました。",
        f'過去の当落の時間は<a href="{SITE}{TIME_ARTICLE[1]}">{TIME_ARTICLE[0]}</a>でまとめています。',
        "当選した人は、11月24日(火)23時59分までに支払いをすませないと当選が取り消しになるので注意しましょう。",
    ]))

    # ---- overall ----
    b.append(h2(f"トラジャ2027ツアーの当選率は約{lo:.0f}〜{hi:.0f}%！倍率は約{100 / hi:.1f}〜{100 / lo:.1f}倍"))
    b.append(p([
        "当落の発表のあと、SNSでは当選か落選かを答えるアンケートが行われました。",
        f"規模の大きい2つのアンケートの{when}をまとめると、次のとおりです。",
    ]))
    b.append(table2(["アンケート", "回答数", "当選", "落選", "当選率", "倍率"], [
        ["全体の当落アンケート", f"{n(ow + ol)}件", f"{n(ow)}件", f"{n(ol)}件", f"<strong>{o_rate:.1f}%</strong>", f"約{odds(ow, ol):.2f}倍"],
        ["会員番号別の当落アンケート", f"{n(zw + zl)}件", f"{n(zw)}件", f"{n(zl)}件", f"<strong>{z_rate:.1f}%</strong>", f"約{odds(zw, zl):.2f}倍"],
    ]))
    b.append(p([
        f"全体のアンケートでは当選率が{o_rate:.1f}%、会員番号別のアンケートでは{z_rate:.1f}%でした。",
        f"どちらも当選の人が多く、{mark('申し込んだ人のおよそ3人に2人〜4人に3人が当選')}した計算です。",
        f"倍率(申し込んだ人数÷当たった人数)にすると約{odds(ow, ol):.2f}〜{odds(zw, zl):.2f}倍になります。",
        "反対にいえば、3〜4人に1人は全部の申込が落選していたことになります。",
    ]))
    b.append(minibox([
        ("数字の出どころ", f"SNSの当落アンケート({when})"),
        ("数え方", "「見るだけ」の回答はのぞいて、当選と落選の数だけで計算"),
        ("注意", "公式の当選率ではない。アンケートに答えるのは熱心なファンが多い"),
    ]))

    # ---- compare ----
    b.append(h2("前回ツアーとくらべて当選率は下がった？"))
    b.append(p([
        f"前回の2026年ツアー「's travelers」の当選率は、SNSでまとめられた最終の数字で{PREV_FINAL}%でした。",
        f"今回の約{lo:.0f}〜{hi:.0f}%は、{mark('前回とほぼ同じか少し下がった')}くらいの結果です。",
        f"全体の当落アンケートと同じ形式の調査では、前回は当選率が約{PREV_SAME_SURVEY}%だったので、同じ調査どうしでくらべると約{PREV_SAME_SURVEY - o_rate:.0f}ポイント下がっています。",
    ]))
    b.append(table2(["年", "ツアー", "当選率"], [
        ["2023年", "THE SHOW〜ただいま、おかえり〜", "92.2%"],
        ["2024年", "Road to Authenticity", "92.9%"],
        ["2025年", "VIIsual", "88.2%"],
        ["2026年", "'s travelers", f"{PREV_FINAL}%"],
        ["<strong>2027年</strong>", "<strong>Jewelry Basket</strong>", f"<strong>約{lo:.0f}〜{hi:.0f}%</strong>(アンケート)"],
    ]))
    b.append(p([
        "ファンクラブの会員数は、前回の約25万人から今回は約31万人まで増えていました。",
        "公演の数は前回より1公演多いだけなので、会員1人あたりの席は減っていて、当選率が前回を下回るという予想どおりの結果になりそうです。",
        "ただ、92%台だった2023〜2024年から前回の69.2%への落ち方とくらべると、今回の下がり方はゆるやかでした。",
        f'予想の根拠は<a href="{SITE}{WINRATE_ARTICLE[1]}">{WINRATE_ARTICLE[0]}</a>でくわしく書いています。',
    ]))

    # ---- venue ----
    b.append(h2(f"会場別の当選率は？いちばん当たりやすいのは{best[0]}、激戦は{worst[0]}"))
    b.append(p([
        "会場ごとの当落アンケートも行われていました。",
        "それぞれの会場に申し込んだ人のうち、その会場で当選した人の割合を当選率の高い順に並べると次のとおりです。",
    ]))
    b.append(p([
        f"全体の当選率({o_rate:.0f}%)は「どこか1つでも当たったか」の数字なので、会場ごとの当選率はそれより低くなります。",
        "ほかの会場で当たって、この会場は外れた人も「落選」にふくまれるためです。",
    ]))
    b.append(table2(["会場", "公演日", "当選率", "倍率"], [
        [f"{s}({v[0]})", TOUR2027[[t[0] for t in TOUR2027].index(v[0])][3][0][0].replace("昼", "").replace("夜", "") + "〜", f"<strong>{r:.1f}%</strong>" if s in (best[0], worst[0]) else f"{r:.1f}%", f"約{o:.2f}倍"]
        for s, r, o, v in vr]))
    b.append(hbars([(s, r) for s, r, o, v in vr]))
    yk = next(x for x in vr if x[0] == "横浜")
    cb = next(x for x in vr if x[0] == "千葉")
    os_ = next(x for x in vr if x[0] == "大阪")
    sz = next(x for x in vr if x[0] == "静岡")
    hk = next(x for x in vr if x[0] == "北海道")
    b.append(p([
        f"当選率がいちばん高かったのは{best[0]}の{best[1]:.1f}%で、{('千葉' if best[0] == '横浜' else '横浜')}も{(cb if best[0] == '横浜' else yk)[1]:.1f}%と、関東の2会場は6割をこえて当たっています。",
        "どちらも公演数が多く(横浜6公演・千葉5公演)、席の数に余裕があったと考えられます。",
        f"反対に{mark(f'大阪城ホールは当選率{os_[1]:.1f}%')}と、申し込んだ人の3人に2人以上が落選していました。",
        f"倍率は約{os_[2]:.1f}倍で、全会場の中でとびぬけて厳しい結果です。",
    ]))
    b.append(h3("大阪・静岡が激戦になった理由"))
    b.append(p([
        "大阪はゴールデンウィークの3公演だけで、静岡はツアーの最後の千秋楽をふくむ4公演です。",
        f"申込前の日程アンケートでも、この2会場は1公演あたりの申込がとくに多く、もともと激戦が予想されていました(<a href=\"{SITE}{ODDS_ARTICLE[1]}\">{ODDS_ARTICLE[0]}</a>)。",
        f"結果も大阪が{os_[1]:.1f}%、静岡が{sz[1]:.1f}%と、予想どおり当たりにくい会場になりました。",
    ]))
    b.append(h3("申込が少なめだった北海道は？"))
    b.append(p([
        f"申込前のアンケートで申込がいちばん少なかった北海道は、当選率{hk[1]:.1f}%と意外にも低めでした。",
        "北海道は3公演だけなので、申込の数が少なくても席の取り合いになったと考えられます。",
        "Xでも「北海道は申込が少ないと思っていたのに全部落ちた」という声が見られ、申込の少なさがそのまま当たりやすさにはつながらなかったようです。",
    ]))
    b.append(minibox([
        ("計算のしかた", "会場ごとのアンケートの「当選」÷(「当選」+「落選」)"),
        ("注意", "1人で複数の会場に申し込んでいる人も多く、会場ごとの当選率は目安"),
    ]))

    # ---- zone ----
    b.append(h2("会員番号別の当選率は？古い会員が有利とはいえない結果"))
    b.append(p([
        "「会員番号が若い(古くから入っている)ほど当たりやすい」といううわさを確かめるために、会員番号のゾーン別の当落アンケートも行われていました。",
        f"{when}をまとめると次のとおりです。",
    ]))
    b.append(table2(["会員番号", "回答数", "当選率", "倍率"], [
        [z[0], f"{n(z[1] + z[2])}件", f"<strong>{rate(z[1], z[2]):.1f}%</strong>" if i == 0 else f"{rate(z[1], z[2]):.1f}%", f"約{odds(z[1], z[2]):.2f}倍"]
        for i, z in enumerate(ZONES)]))
    b.append(hbars(zr))
    zmax = max(zr, key=lambda x: x[1])
    zmin = min(zr, key=lambda x: x[1])
    b.append(p([
        f"当選率がいちばん高かったのは{zmax[0]}の{zmax[1]:.1f}%、いちばん低かったのは{zmin[0]}の{zmin[1]:.1f}%でした。",
        f"差は{zmax[1] - zmin[1]:.0f}ポイントほどで、{mark('どのゾーンも6割台')}におさまっています。",
        "10万番台より20万番台のほうが当選率が高いなど、番号順にきれいに下がっているわけでもありません。",
        "会員番号で大きな差がついているとはいえず、新しく入会した人にもしっかり当選のチャンスがあったといえます。",
    ]))

    # ---- reactions ----
    b.append(h2("Xでの当落の反応は？「当選ありがとう」と「初めての落選」"))
    b.append(p([
        "15時の発表のあと、Xでは「トラジャ当選」の投稿が2時間ほどで一気に増えました。",
        "「無事に当選しました」「デビューの年から毎年行けている」「今年もメンバーに会える」という喜びの声が多く見られます。",
        "一方で、「毎年当選していたのに今回初めて落選した」「全部落ちてつらい」という声も少なくありません。",
        "当選した人のあいだでは、もう同行者や交換相手を探す投稿も始まっています。",
    ]))
    b.append(p([
        "チケットの譲渡や交換をSNSで個人どうしで行うのは、ファンクラブの規約で禁止されていて、詐欺のトラブルも起きています。",
        "行けなくなったときは、公式のリセールなど決められた方法を使いましょう。",
    ]))

    # ---- after ----
    b.append(h2("落選したら？これからのチケットのチャンス"))
    b.append(p([
        "FC先行で落選しても、まだチケットを手に入れるチャンスはあります。",
        "過去のツアーの流れから、これから考えられるチャンスは次のとおりです(時期はどれも予想です)。",
    ]))
    b.append(table2(["チャンス", "内容", "時期の目安"], [
        ["復活当選", "支払いがなかった席などが、落選した人にあとから当選として回ってくる", "支払い期限(11/24)のあと"],
        ["一般販売", "ファンクラブ会員以外も申し込める販売", "未発表(横浜公演は12月中旬ごろの見込み)"],
        ["制作開放席", "ステージの設営が決まったあとに出る見切れ席など", "各会場の初日の約1週間前"],
        ["公式リセール", "行けなくなった人のチケットを公式で買える", "未発表"],
        ["追加公演", "新しく公演がふえる", "未発表"],
    ]))
    b.append(p([
        f"復活当選は、支払い期限の11月24日(火)をすぎてから出ることが多いので、{mark('落選した人も11月下旬はメールをこまめにチェック')}しておきましょう。",
        "前回のツアーでは当落の日に追加公演が発表されましたが、今回は記事を書いている時点で追加公演の発表はありません。",
        f'また、アルバム『Jewelry Basket』の発売記念イベント(お見送り会)の応募もあるので、ツアーに落選した人はこちらもチェックしてみてください(<a href="{SITE}{CD_ARTICLE[1]}">{CD_ARTICLE[0]}</a>)。',
    ]))

    # ---- matome ----
    b.append(h2("まとめ"))
    b.append(checklist("この記事のポイント", [
        "トラジャ2027ツアー「Jewelry Basket」のFC先行の当落は11月20日(金)15時に発表",
        f"SNSの当落アンケートでは当選率約{lo:.0f}〜{hi:.0f}%、倍率は約{100 / hi:.2f}〜{100 / lo:.2f}倍",
        f"前回の69.2%とほぼ同じか少し厳しい結果",
        f"会場別でいちばん当たりやすいのは{best[0]}({best[1]:.0f}%)、いちばん激戦は{worst[0]}({worst[1]:.0f}%)",
        "大阪・静岡は申込前の予想どおり激戦、申込が少なめの北海道も当選率は低め",
        "会員番号別ではどのゾーンも6割台で、古い会員が大きく有利とはいえない",
        "支払い期限は11月24日(火)23:59、落選した人は復活当選や一般販売に期待",
    ]))
    if not FINAL:
        b.append(p([
            f"数字は{AS_OF}のアンケートの途中経過です。",
            "アンケートの締め切り後に、最終の数字に更新します！",
        ]))
    b.append(related([WINRATE_ARTICLE, ODDS_ARTICLE, TIME_ARTICLE, SEATED_ARTICLE, CAPACITY_ARTICLE, SCHEDULE_ARTICLE]))
    return "\n\n".join(b)


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    html = build()
    if DRY:
        (IMG_DIR / "_dry.html").write_text(html, encoding="utf-8")
        print("dry chars:", len(html))
        return
    tmp = IMG_DIR / "_post.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis", str(tmp)], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "check", "--group", "travis", str(tmp)], check=True)
    html = tmp.read_text(encoding="utf-8")
    if not EYECATCH.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
                        "--top", "Travis Japan 2027ツアー", "--main", "当落倍率は？",
                        "--bottom", "当選率を会場別に調査！", "--color-key", "group", "--out", str(EYECATCH)], check=True)
    if "eyecatch" not in state:
        state["eyecatch"] = upload_media(EYECATCH, TITLE, BASE_TITLE)
        STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    body = {"title": TITLE, "slug": SLUG, "content": html, "status": "draft",
            "categories": [3], "author": 2, "featured_media": state["eyecatch"]["id"]}
    if "post_id" in state:
        cur = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{state['post_id']}?context=edit", headers=HJSON).json()
        if cur.get("status") == "publish":
            body = {"content": html}  # published: content only
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
