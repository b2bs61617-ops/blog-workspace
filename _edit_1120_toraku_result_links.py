# -*- coding: utf-8 -*-
# 2026-11-20: 当落結果記事(3305)へのリンクを公開中の 2197(当選率予想)/2115(倍率)/3230(当落時間) に追加
# 「当落が出たら追記します！」の段落を結果の追記に置き換え+「あわせて読みたい」の先頭に3305を追加。本文のみ更新(status送らない)
# 3305が公開されていなければ止まる。--dry で差分だけ表示
import sys
import requests
from build_and_post_travis_japan_tour2027_odds_survey import WP_URL, HJSON

DRY = "--dry" in sys.argv
RESULT_ID = 3305

res = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{RESULT_ID}?context=edit", headers=HJSON).json()
title = res["title"]["raw"].replace("【未】", "")
if res["status"] != "publish":
    if not DRY:
        sys.exit(f"{RESULT_ID} is {res['status']} - publish it first")
    url = "https://chomoand-4.blog/travis-japan-2027-tour-toraku-result-3305"
else:
    url = res["link"]
A = f'<a href="{url}">{title}</a>'
LI = f'<li style="margin:0 0 6px 0;"><a href="{url}">{title}</a></li>\n'

PATCHES = {
    2197: ("<p>当落の結果が出たら、2027年ツアーの実際の当選率もこの記事に追記します！</p>",
           "<p><strong>【11月20日追記】</strong>当落は11月20日(金)15時に発表されました。"
           "SNSの当落アンケートでは、2027年ツアーの当選率は約65〜74%で、予想どおり前回の69.2%とほぼ同じか少し厳しい結果になっています。"
           f"会場別・会員番号別の当選率は{A}でまとめています。</p>"),
    2115: ("<p>当落の結果が出たら、当選・落選の集計もこの記事に追記します！</p>",
           "<p><strong>【11月20日追記】</strong>当落は11月20日(金)15時に発表されました。"
           "SNSの当落アンケートでは、この記事で申込が多かった大阪城ホールが当選率約29%といちばんの激戦、静岡も約41%と当たりにくい結果でした。"
           f"会場別の当選率は{A}でくわしくまとめています。</p>"),
    3230: ("<p>当落が出たら、今回の発表時間もこの記事に追記します！<br>",
           "<p><strong>【11月20日追記】</strong>2027年ツアーの当落は、予想どおり<strong>11月20日(金)15時</strong>に発表されました！2024年・2025年に続いて3回連続の15時です。"
           f"当選率や会場別の結果は{A}でまとめています。<br>"),
}

for pid, (old, new) in PATCHES.items():
    c = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=HJSON).json()["content"]["raw"]
    if url in c:
        print(pid, "already linked, skip")
        continue
    assert c.count(old) == 1, (pid, "old text not found")
    c2 = c.replace(old, new)
    k = c2.find("あわせて読みたい")
    ul = c2.find('<ul style="margin:0;padding-left:1.3em;">\n', k)
    assert k > 0 and ul > 0, (pid, "related box not found")
    ins = ul + len('<ul style="margin:0;padding-left:1.3em;">\n')
    c2 = c2[:ins] + LI + c2[ins:]
    if DRY:
        print("=====", pid, "\n", new, "\n+", LI)
        continue
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=HJSON, json={"content": c2})
    r.raise_for_status()
    chk = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=HJSON).json()
    print(pid, chk["status"], "linked:", chk["content"]["raw"].count(url) == 2)
