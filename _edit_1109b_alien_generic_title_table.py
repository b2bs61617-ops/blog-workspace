# -*- coding: utf-8 -*-
"""2026-11-09 オシリ: おそろいメンバーが増えても使えるよう、エイリアン記事(15478/79/80)のタイトルをメンバー名なしの案Aに変更し、
冒頭に「エイリアンを付けていたメンバー一覧」表を追加(増えたら行を足す)。"""
import json
import requests
from _mubank1009_helpers import WP_URL, HEADERS_AUTH, p

HJ = {**HEADERS_AUTH, "Content-Type": "application/json"}
WAKARU = '<!-- wp:html -->\n<div style="border:1px solid #cdd5e6;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">'


def table(head, rows):
    th = "".join(f"<td><strong>{c}</strong></td>" for c in head)
    trs = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n'
            f"<tr>{th}</tr>\n{trs}\n</tbody></table></figure>\n<!-- /wp:table -->")


def patch(pid, title, intro, tbl, extra=(), anchor=WAKARU):
    d = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", params={"context": "edit"}, headers=HEADERS_AUTH).json()
    t = d["content"]["raw"]
    assert anchor in t and "wp:table" not in t.split(anchor)[0], pid
    t = t.replace(anchor, intro + "\n\n" + tbl + "\n\n" + anchor, 1)
    for old, new in extra:
        assert t.count(old) == 1, (pid, old)
        t = t.replace(old, new)
    T = title
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=HJ,
                      data=json.dumps({"title": T, "content": t}).encode("utf-8"))
    r.raise_for_status()
    print(pid, r.json()["status"], r.json()["title"]["raw"])


JT = "【未】【KO1KEYZ】おそろいの光るエイリアンキーホルダーはどこの？"
assert len(JT.replace("【未】", "")) <= 35
patch(15478, JT,
      p("11月9日の時点で、エイリアンのキーホルダーが確認できたメンバーは次の3人です。<br>\nほかのメンバーのバッグでも見つかりしだい、この表に追記していきます。"),
      table(["メンバー", "確認した日・場所", "瞳の色", "付けていたところ"], [
          ["TOWA", "11月9日・金浦空港", "グリーン", "ディオールのバッグの持ち手"],
          ["KOSUKE", "11月9日・金浦空港", "映像では不明", "ベージュのボアのバッグ(ほかのキーホルダーと一緒に)"],
          ["YURA", "11月9日・金浦空港", "映像では不明", "黒いチェーンのバッグ(TOWAにもらったロケットの隣)"],
      ]))
patch(15479, "【未】【KO1KEYZ】커플템 야광 에일리언 키링은 어디 거?",
      p("11월 9일 기준으로 에일리언 키링이 확인된 멤버는 아래 3명입니다. 다른 멤버에게서도 발견되면 표에 추가하겠습니다."),
      table(["멤버", "날짜・장소", "눈 색", "단 곳"], [
          ["TOWA", "11/9 김포공항", "그린", "디올 가방 손잡이"],
          ["KOSUKE", "11/9 김포공항", "확인 불가", "베이지 보아 가방"],
          ["YURA", "11/9 김포공항", "확인 불가", "검은 체인 가방(TOWA가 준 로켓 옆)"],
      ]), extra=[(">TOWA와 KOSUKE의 키링</p>", ">TOWA・KOSUKE・YURA의 키링</p>")], anchor="<!-- wp:heading -->")
patch(15480, "【未】[KO1KEYZ] Matching Glow-in-the-Dark Alien Keychains: Which Brand?",
      p("As of November 9, three members have been spotted with the alien keychain. We'll add more to this table if it shows up on other members' bags."),
      table(["Member", "Date / place", "Eye color", "Where"], [
          ["TOWA", "Nov 9, Gimpo Airport", "Green", "Handle of his Dior bag"],
          ["KOSUKE", "Nov 9, Gimpo Airport", "Not visible", "Beige shearling bag"],
          ["YURA", "Nov 9, Gimpo Airport", "Not visible", "Black chain bag, next to TOWA's rocket"],
      ]), extra=[(">TOWA and KOSUKE's keychain</p>", ">TOWA, KOSUKE and YURA's keychains</p>")], anchor="<!-- wp:heading -->")
