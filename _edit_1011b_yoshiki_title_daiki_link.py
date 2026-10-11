# -*- coding: utf-8 -*-
"""10/11: YOSHIKI Gimpo drafts — retitle to include BAPE (still drafts) and link the published DAIKI BAPE article."""
import json, time
from pathlib import Path
import requests
from _mubank1009_helpers import WP_URL as U, HEADERS_AUTH as H

D = {
    14339: ("【YOSHIKI】金浦空港のキーホルダーはメロジョイとBAPE！",
            "ちなみにこの日は、DAIKIもBAPEのシャークパーカーを着て空港に現れていました。<br>",
            'ちなみにこの日は、DAIKIもBAPEのシャークパーカーを着て空港に現れていました(<a href="https://chomoand-1.com/daiki-gimpo-airport-bape-paisley-shark-hoodie-14296" target="_blank" rel="noopener">DAIKIの金浦空港の私服を調べた記事</a>)。<br>'),
    14342: ("【YOSHIKI】김포공항 키링은 멜로조이와 BAPE!",
            "참고로 이날은 DAIKI도 BAPE의 샤크 후디를 입고 공항에 나타났습니다.<br>",
            '참고로 이날은 DAIKI도 BAPE의 샤크 후디를 입고 공항에 나타났습니다(<a href="https://chomoand-1.com/ko/daiki-gimpo-airport-bape-paisley-shark-hoodie-kr-14298" target="_blank" rel="noopener">김포공항 DAIKI 사복 글</a>).<br>'),
    14343: ("[YOSHIKI] His Gimpo Airport Charms: Mellojoy and BAPE!",
            "Fun fact: DAIKI also showed up at the airport that day in a BAPE shark hoodie.<br>",
            'Fun fact: DAIKI also showed up at the airport that day in a BAPE shark hoodie (<a href="https://chomoand-1.com/en/daiki-gimpo-airport-bape-paisley-shark-hoodie-en-14299" target="_blank" rel="noopener">see our article on DAIKI\'s Gimpo outfit</a>).<br>'),
}
for pid, (title, old, new) in D.items():
    d = requests.get(f"{U}/wp-json/wp/v2/posts/{pid}", headers=H, params={"context": "edit"}).json()
    assert d["status"] == "draft"
    raw = d["content"]["raw"]
    Path(f"backups/{pid}_before_1011b.html").write_text(raw, encoding="utf-8")
    assert raw.count(old) == 1, pid
    raw = raw.replace(old, new)
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", headers={**H, "Content-Type": "application/json"},
                      data=json.dumps({"title": title, "content": raw, "status": "draft"}).encode("utf-8"))
    r.raise_for_status(); print(pid, r.json()["status"], r.json()["title"]["raw"])
    time.sleep(2)
for pid in D:
    d = requests.get(f"{U}/wp-json/wp/v2/posts/{pid}", headers=H, params={"context": "edit"}).json()
    print(pid, "verify", "daiki-gimpo" in d["content"]["raw"], d["content"]["raw"].count("BABY MILO"))
