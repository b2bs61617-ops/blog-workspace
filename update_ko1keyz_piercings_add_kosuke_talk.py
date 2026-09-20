# -*- coding: utf-8 -*-
"""KO1KEYZピアス記事(JP12030/KR12034/EN12038、公開済み)のKOSUKE枠に、1ST ONLINE TALK Day3(2026-09-20)で
判明した「ピアスを開けた時期(中学〜高1ごろ)」を追記。冒頭の「わかること」とまとめにも1行ずつ追加。titleは送らない。"""
import base64, os
from pathlib import Path

import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f'{ENV["WP_KOIKEYS_USERNAME"]}:{ENV["WP_KOIKEYS_APP_PASSWORD"]}'.encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}

EDITS = {
    12030: [
        ("<li>KOSUKEの星ピアスなど、目撃されているデザイン</li>",
         "<li>KOSUKEの星ピアスなど、目撃されているデザイン</li>\n<li>KOSUKEがピアスを開けた時期(トーク会で判明)</li>"),
        ("トレードマークとして定着しつつあります。</p>",
         "トレードマークとして定着しつつあります。<br>\n"
         "9月20日のKO1KEYZ 1ST ONLINE TALK Day3では、ファンから「ピアスめっちゃ好きなんだよね」と声をかけられ、「うーわ今日付けてないわ」と悔しそうな反応を見せました。<br>\n"
         "耳を近づけて「付いてないでしょ」と見せてくれる場面もあったそうです。<br>\n"
         "ピアスを開けた時期を聞かれると<strong><span class=\"swl-marker mark_green\">「中学……高1とか！」</span></strong>と回答していて、10代前半〜半ばにはすでに開けていたようです。ピアス歴は長めで、星ピアスへのこだわりも納得ですね。</p>"),
        ("<li>KOSUKEの星モチーフ、RYUJIのゴールド＋イヤーカフなど、デザインもメンバーごとに個性あり</li>",
         "<li>KOSUKEの星モチーフ、RYUJIのゴールド＋イヤーカフなど、デザインもメンバーごとに個性あり</li>\n<li>KOSUKEがピアスを開けたのは中学〜高1ごろ(1ST ONLINE TALK Day3での本人談)</li>"),
    ],
    12034: [
        ("<li>KOSUKE의 별 피어싱 등 목격된 디자인</li>",
         "<li>KOSUKE의 별 피어싱 등 목격된 디자인</li>\n<li>KOSUKE가 피어싱을 뚫은 시기(토크회에서 밝혀짐)</li>"),
        ("트레이드마크로 자리잡아가고 있어요.</p>",
         "트레이드마크로 자리잡아가고 있어요.<br>\n"
         "9월 20일 KO1KEYZ 1ST ONLINE TALK Day3에서는 팬이 「피어싱 정말 좋아해요」라고 말을 걸자, KOSUKE는 「아~ 오늘은 안 했네」라며 아쉬운 듯한 반응을 보였어요.<br>\n"
         "귀를 가까이 가져와서 「안 했죠」 하고 보여주는 장면도 있었다고 해요.<br>\n"
         "피어싱을 뚫은 시기를 묻자 <strong><span class=\"swl-marker mark_green\">「중학교…… 고1쯤이요!」</span></strong>라고 답해서, 10대 초중반에는 이미 뚫었던 것 같아요. 피어싱 경력이 꽤 길다 보니 별 피어싱에 대한 애정도 납득이 가요.</p>"),
        ("<li>KOSUKE의 별 모티브, RYUJI의 골드＋이어 커프 등 디자인도 멤버별로 개성 있음</li>",
         "<li>KOSUKE의 별 모티브, RYUJI의 골드＋이어 커프 등 디자인도 멤버별로 개성 있음</li>\n<li>KOSUKE가 피어싱을 뚫은 것은 중학교~고1 무렵(1ST ONLINE TALK Day3 본인 발언)</li>"),
    ],
    12038: [
        ("<li>Spotted designs such as KOSUKE's star piercing</li>",
         "<li>Spotted designs such as KOSUKE's star piercing</li>\n<li>When KOSUKE got his ears pierced (revealed at the online talk)</li>"),
        ("the star piercing is turning into a trademark.</p>",
         "the star piercing is turning into a trademark.<br>\n"
         "At KO1KEYZ 1ST ONLINE TALK Day 3 (September 20), a fan told him she loves his piercings, and KOSUKE reacted with a disappointed “Ugh, I’m not wearing them today.”<br>\n"
         "He even leaned in to show his bare ear.<br>\n"
         "Asked when he got them, he answered <strong><span class=\"swl-marker mark_green\">“Middle school… maybe first year of high school!”</span></strong> — so he seems to have been pierced since his early-to-mid teens, which makes his attachment to the star piercing easy to understand.</p>"),
        ("<li>Designs vary by member too, from KOSUKE's star studs to RYUJI's gold pieces and ear cuff</li>",
         "<li>Designs vary by member too, from KOSUKE's star studs to RYUJI's gold pieces and ear cuff</li>\n<li>KOSUKE got his ears pierced around middle school to first-year high school, by his own account at 1ST ONLINE TALK Day 3</li>"),
    ],
}

for pid, edits in EDITS.items():
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=H, timeout=60)
    r.raise_for_status()
    content = r.json()["content"]["raw"]
    for old, new in edits:
        assert content.count(old) == 1, (pid, old[:40], content.count(old))
        content = content.replace(old, new)
    # title is intentionally omitted (published articles' titles never change)
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=H,
                      json={"content": content, "status": "publish"}, timeout=60)
    print(pid, r.status_code, r.json().get("status"), r.json().get("modified"))
