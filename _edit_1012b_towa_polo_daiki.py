# -*- coding: utf-8 -*-
"""TOWAポロ記事(14704/14706/14707)のピンク色違いの着用者を「ほかのメンバー」→DAIKIに(ユーザー確認済み、10-12)。JPはDAIKI記事14720へリンク。"""
import requests
import _mubank1009_helpers as h

edits = {
    14704: ("Performance Videoではほかのメンバーが同じデザインのピンクの色違いを着ている場面もあります。",
            "Performance Videoでは、DAIKIが同じデザインのピンクの色違いを着ています(<a href=\"https://chomoand-1.com/?p=14720\">DAIKIのピンクのポロの記事</a>)。"),
    14706: ("Performance Video에서는 다른 멤버가 같은 디자인의 핑크 컬러를 입은 장면도 있습니다.",
            "Performance Video에서는 DAIKI가 같은 디자인의 핑크 컬러를 입었습니다."),
    14707: ("In the Performance Video, another member wears the same design in pink.",
            "In the Performance Video, DAIKI wears the same design in pink."),
}
for pid, (a, b) in edits.items():
    r = requests.get(f"{h.WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=h.HEADERS_AUTH, timeout=60).json()
    assert r["status"] == "draft"
    raw = r["content"]["raw"]
    assert raw.count(a) == 1, (pid, a[:30])
    u = requests.post(f"{h.WP_URL}/wp-json/wp/v2/posts/{pid}", headers=h.HEADERS_AUTH,
                      json={"content": raw.replace(a, b), "status": "draft"}, timeout=60)
    print(pid, u.status_code, u.json().get("status"))
