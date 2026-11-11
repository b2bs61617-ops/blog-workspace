# -*- coding: utf-8 -*-
# 2026-11-11 CD発売延期(11/18→12/16)に合わせて、公開記事922(Jewelry Basket特典)の日付を更新(オシリ許可済み)
# usage: python _edit_1111_jewelry_basket_922_cd_postponed.py [--dry]
import re
import sys

import requests
import _jb_fc_lib as L

PID = 922
DRY = "--dry" in sys.argv
P = r"[\(（]"
Q = r"[\)）]"


def sub_once(html, pattern, repl):
    n = len(re.findall(pattern, html))
    assert n == 1, (n, pattern)
    return re.sub(pattern, lambda m: repl, html)


po = requests.get(f"{L.WP_URL}/wp-json/wp/v2/posts/{PID}?context=edit", headers=L.HEADERS_AUTH).json()
html = po["content"]["raw"]

# 1. lead
html = sub_once(
    html,
    rf"『Jewelry Basket』が、2026年11月18日{P}水{Q}に発売されます。",
    "『Jewelry Basket』のCDが、2026年12月16日(水)に発売されます。<br>\n"
    "もとは11月18日(水)発売の予定でしたが、商品の一部に不備が見つかったため、"
    "2026年11月11日に延期が発表されました(配信は11月18日から予定どおり)。",
)
# 2. spec table
html = sub_once(
    html,
    rf'(発売日</td><td style="[^"]*">)2026年11月18日{P}水{Q}',
    None,
) if False else re.sub(
    rf'(発売日</td><td style="[^"]*">)2026年11月18日{P}水{Q}',
    lambda m: m.group(1) + "2026年12月16日(水)<br>※11月18日から延期", html, count=1)
# 3. tower records box
html = sub_once(
    html,
    rf"<strong>店頭入荷:</strong>11月17日{P}火{Q}予定{P}発売日の前日{Q}",
    "<strong>店頭入荷:</strong>発売延期のため、お店の新しい案内を確認(もとは11月17日(火)予定)",
)
# 4. tower records paragraph
html = sub_once(
    html,
    r"タワーレコードの店頭告知では、国内盤の入荷予定日は発売日前日の<strong>11月17日[^<]*</strong>となっていて、店頭ならいわゆる「フラゲ」ができる見込みです。",
    "タワーレコードの店頭告知では、もとは発売日前日の<strong>11月17日(火)</strong>に入荷する予定でした。<br>\n"
    "ただ、CDの発売日が12月16日(水)に延期されたため、入荷日も変わる見込みです。",
)
# 5. event box
html = sub_once(
    html,
    rf"<strong>応募期間:</strong>2026年11月17日{P}火{Q}〜11月29日{P}日{Q}23:59",
    "<strong>応募期間:</strong>2026年12月15日(火)10:00〜12月20日(日)23:59(延期にともない変更)",
)
html = sub_once(
    html,
    rf"<strong>当選発表:</strong>2026年12月23日{P}水{Q}12:00予定",
    "<strong>当選発表:</strong>2027年1月13日(水)12:00予定(延期にともない変更)",
)
# 6. sales table
html = sub_once(
    html,
    r'(4th『Jewelry Basket』</td><td style="[^"]*">)2026年11月18日(</td>)',
    None,
) if False else re.sub(
    r'(4th『Jewelry Basket』</td><td style="[^"]*">)2026年11月18日(</td>)',
    lambda m: m.group(1) + "2026年12月16日" + m.group(2), html, count=1)
html = sub_once(
    html,
    r"これまでは12月発売が続いていましたが、今回は11月中旬と少し早めのリリースです。",
    "今回は11月中旬に発売の予定でしたが、延期により、これまでと同じ12月の発売になりました。",
)
# 7. summary checklist
html = sub_once(html, r"『Jewelry Basket』は2026年11月18日発売、",
                "『Jewelry Basket』のCDは2026年12月16日発売(11月18日から延期)、")
html = sub_once(html, r"店頭入荷は11月17日予定",
                "店頭入荷はお店の新しい案内を確認")

must = ["2026年12月16日(水)に発売されます", "12月15日(火)10:00〜12月20日(日)23:59", "2027年1月13日(水)12:00予定",
        "※11月18日から延期", "2026年12月16日</td>", "延期により、これまでと同じ12月"]
for m in must:
    assert m in html, m
left = [x for x in ["11月29日", "12月23日"] if x in html]
print("left:", left, "11/18 count:", html.count("11月18日"), "11/17 count:", html.count("11月17日"))
if DRY:
    sys.exit()
r = requests.post(f"{L.WP_URL}/wp-json/wp/v2/posts/{PID}", headers=L.HEADERS_AUTH, json={"content": html})
r.raise_for_status()
raw = requests.get(f"{L.WP_URL}/wp-json/wp/v2/posts/{PID}?context=edit", headers=L.HEADERS_AUTH).json()
print(PID, raw["status"], all(m in raw["content"]["raw"] for m in must))
