# -*- coding: utf-8 -*-
# 2026-11-11 CD発売延期(11/18→12/16)を、公開中のJewelry Basket関連記事6本に反映(オシリ許可済み)
# usage: python _edit_1111b_jewelry_basket_postponed_others.py [--dry]
import re
import sys

import requests
import _jb_fc_lib as L

DRY = "--dry" in sys.argv
P, Q = r"[\(（]", r"[\)）]"
TD = r"<td[^>]*>"
NOTE = "もとは11月18日(水)発売の予定でしたが、商品の一部に不備が見つかったため、2026年11月11日に延期が発表されました(配信は11月18日から予定どおり)。"

EDITS = {
    1973: [
        (r"ツアー名は、11月18日に発売される4thアルバムと同じ「Jewelry Basket」です。",
         "ツアー名は、12月16日に発売される4thアルバムと同じ「Jewelry Basket」です(CDは11月18日から延期)。"),
        (r"応募券は、11月18日発売の4thアルバム「Jewelry Basket」の",
         "応募券は、12月16日発売(11月18日から延期)の4thアルバム「Jewelry Basket」の"),
        (rf"<strong>応募期間:</strong>2026年11月17日{P}火{Q}〜11月29日{P}日{Q}23:59",
         "<strong>応募期間:</strong>2026年12月15日(火)10:00〜12月20日(日)23:59(延期にともない変更)"),
        (rf"<strong>当選発表:</strong>2026年12月23日{P}水{Q}12:00予定",
         "<strong>当選発表:</strong>2027年1月13日(水)12:00予定(延期にともない変更)"),
        (rf"ツアーと同じタイトルの4thアルバム「Jewelry Basket」は、2026年11月18日{P}水{Q}に発売されます。",
         "ツアーと同じタイトルの4thアルバム「Jewelry Basket」のCDは、2026年12月16日(水)に発売されます。<br>\n" + NOTE),
        (r"ツアーのもとになる4thアルバム「Jewelry Basket」は11月18日発売",
         "ツアーのもとになる4thアルバム「Jewelry Basket」のCDは12月16日発売(11月18日から延期)"),
    ],
    1724: [
        (rf"『Jewelry Basket』が、2026年11月18日{P}水{Q}に発売されます。",
         "『Jewelry Basket』のCDが、2026年12月16日(水)に発売されます。<br>\n" + NOTE),
        (rf"<strong>発売日:</strong>2026年11月18日{P}水{Q}",
         "<strong>発売日:</strong>2026年12月16日(水)※11月18日から延期"),
        (r"発売日の11月18日を締め切りと思い込んでいると間に合わないので",
         "発売日(12月16日に延期)を締め切りと思い込んでいると間に合わないので"),
        (rf"『Jewelry Basket』の発売日は2026年11月18日{P}水{Q}です。",
         "『Jewelry Basket』のCDの発売日は、11月18日から延期になり、2026年12月16日(水)になりました。<br>\nFC限定盤も、ほかの形態と同じく12月16日発売です。"),
        (r"発売日の11月18日ちょうどに届くとは限りません。",
         "発売日の12月16日ちょうどに届くとは限りません。"),
    ],
    1939: [
        (rf"(4th「Jewelry Basket」</td>{TD})2026年11月18日(</td>)", r"\g<1>2026年12月16日\g<2>"),
        (r"4thアルバム「Jewelry Basket」は2026年11月18日発売で、これまでの12月から1か月早い発売になります。",
         "4thアルバム「Jewelry Basket」は11月18日発売の予定でしたが、延期になり、2026年12月16日発売になりました。<br>\n結果として、これまでと同じ12月の発売です。"),
        (r"4thアルバム「Jewelry Basket」は2026年11月18日発売</p>",
         "4thアルバム「Jewelry Basket」のCDは2026年12月16日発売(11月18日から延期)</p>"),
    ],
    1543: [
        (rf"(発売日</td>{TD})2026年11月18日{P}水{Q}", r"\g<1>2026年12月16日(水)<br>※11月18日から延期"),
        (rf"発売日の11月18日{P}水{Q}まではあと1か月ほどあります。",
         "CDの発売日は11月18日から延期になり、12月16日(水)になりました(配信は11月18日から)。"),
    ],
    1630: [
        (r"<p>11月18日に発売されるTravis Japanの4thアルバム『Jewelry Basket』で、",
         "<p>12月16日に発売されるTravis Japanの4thアルバム『Jewelry Basket』(CDは11月18日から延期)で、"),
        (r"11月18日の発売日を楽しみに待ちたいですね！",
         "CDの発売日は12月16日に延期になりましたが、楽しみに待ちたいですね！"),
    ],
    958: [
        (rf"(発売日</td>{TD})2026年11月18日(</td>)", r"\g<1>2026年12月16日(11月18日から延期)\g<2>"),
        (r"発売日の11月18日にCDを手に取ったら、",
         "発売日の12月16日(11月18日から延期)にCDを手に取ったら、"),
    ],
}

for pid, edits in EDITS.items():
    po = requests.get(f"{L.WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=L.HEADERS_AUTH).json()
    html = po["content"]["raw"]
    for pat, rep in edits:
        n = len(re.findall(pat, html))
        assert n == 1, (pid, n, pat)
        html = re.sub(pat, rep.replace("\\g<", "\x00").replace("\\", "\\\\").replace("\x00", "\\g<"), html)
    left = re.findall(r".{0,20}(?:11月18日|11月17日|11月29日|12月23日).{0,20}", re.sub(r"<[^>]+>", "", html))
    print(pid, "left:", [x for x in left if "延期" not in x and "配信" not in x])
    if DRY:
        continue
    r = requests.post(f"{L.WP_URL}/wp-json/wp/v2/posts/{pid}", headers=L.HEADERS_AUTH, json={"content": html})
    r.raise_for_status()
    raw = requests.get(f"{L.WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=L.HEADERS_AUTH).json()
    print(pid, raw["status"], "12月16日" in raw["content"]["raw"], raw["content"]["raw"] == html)
