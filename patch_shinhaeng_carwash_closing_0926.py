# -*- coding: utf-8 -*-
"""SHINHAENG洗車場記事(JP13716/KR13717/EN13718・下書き)のまとめ後の感想にファン目線の一言を追加。"""
import base64, json, sys
from pathlib import Path
import requests
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent
env = {}
for l in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    l = l.strip()
    if "=" in l and not l.startswith("#"):
        k, v = l.split("=", 1); env[k.strip()] = v.strip().strip('"')
HA = {"Authorization": "Basic " + base64.b64encode(f"{env['WP_KOIKEYS_USERNAME']}:{env['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()}
W = env["WP_KOIKEYS_URL"].rstrip("/") + "/wp-json/wp/v2"

EDITS = {
    13716: ("SHINHAENGのパフォーマンスがまた違って見えてきますね！</p>",
            "SHINHAENGのパフォーマンスがまた違って見えてきますね！<br>\n"
            "夜の洗車場で踏ん張っていた人だと思うと、トーク会でファン一人ひとりに丁寧に向き合ってくれる姿にも、ぐっとくるものがあります。<br>\n"
            "お父さんが「木浦」の表記をあれほど喜んでいたと知った今、KO1LYとしてはいつか木浦での凱旋ステージが実現する日まで、つい夢見てしまいます！</p>"),
    13717: ("SHINHAENG의 무대가 또 다르게 보일 거예요!</p>",
            "SHINHAENG의 무대가 또 다르게 보일 거예요!<br>\n"
            "밤새 세차장에서 버텨 온 사람이라고 생각하면, 토크회에서 팬 한 명 한 명에게 정성껏 대해 주는 모습에도 괜히 뭉클해져요.<br>\n"
            "아버지가 '목포' 표기를 그렇게 기뻐했다는 걸 알고 나니, KO1LY로서는 언젠가 목포 금의환향 무대가 열리는 날까지 꿈꾸게 되네요!</p>"),
    13718: ("may look a little different next time you watch!</p>",
            "may look a little different next time you watch!<br>\n"
            "Knowing he pushed through nights at a car wash makes the care he shows each fan at talk events hit a little harder.<br>\n"
            "And after hearing how happy his dad was to see \"Mokpo\" on screen, it's hard for any KO1LY not to dream of a homecoming stage in Mokpo someday!</p>"),
}

for pid, (old, new) in EDITS.items():
    d = requests.get(f"{W}/posts/{pid}", params={"context": "edit"}, headers=HA).json()
    assert d["status"] == "draft", d["status"]
    raw = d["content"]["raw"]
    assert raw.count(old) == 1, (pid, raw.count(old))
    raw = raw.replace(old, new)
    r = requests.post(f"{W}/posts/{pid}", headers={**HA, "Content-Type": "application/json"},
                      data=json.dumps({"content": raw, "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    v = requests.get(f"{W}/posts/{pid}", params={"context": "edit"}, headers=HA).json()
    print(pid, v["status"], "verified" if new in v["content"]["raw"] else "NOT REFLECTED")
