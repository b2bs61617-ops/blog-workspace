# -*- coding: utf-8 -*-
"""Add a fan-voice closing line to the TOWA shark backpack drafts (JP 12193 / KR 12197 / EN 12198)."""
import json, base64, os
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
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}
HJSON = {**H, "Content-Type": "application/json"}

EDITS = {
    12193: (
        "<p>派手すぎず、でも背負うとしっかり目を引くサメリュックは、TOWAさんのくだけた雰囲気ともよく合っています。<br>\n気になった人は、まずは公式オンラインストアでサイズとカラーをチェックしてみてはいかがでしょうか！</p>",
        "<p>派手すぎず、でも背負うとしっかり目を引くサメリュックは、TOWAさんのくだけた雰囲気ともよく合っています。<br>\nお手頃な価格なので、同じものを手に入れて、これを背負ってライブやイベントでTOWAさんに会いに行くのも楽しそうです。<br>\n気になった人は、まずは公式オンラインストアでサイズとカラーをチェックしてみてはいかがでしょうか！</p>",
    ),
    12197: (
        "<p>과하지 않으면서도 메면 확실히 눈길을 끄는 상어 백팩은, TOWA의 편안한 분위기와도 잘 어울립니다.<br>\n궁금해진 분은 우선 공식 온라인 스토어에서 사이즈와 컬러를 확인해 보는 건 어떨까요!</p>",
        "<p>과하지 않으면서도 메면 확실히 눈길을 끄는 상어 백팩은, TOWA의 편안한 분위기와도 잘 어울립니다.<br>\n가격도 부담 없으니, 같은 걸 손에 넣어서 이 백팩을 메고 라이브나 이벤트에서 TOWA를 만나러 가는 것도 즐거울 것 같습니다.<br>\n궁금해진 분은 우선 공식 온라인 스토어에서 사이즈와 컬러를 확인해 보는 건 어떨까요!</p>",
    ),
    12198: (
        "<p>Not too loud, but a real head-turner once it's on your back, the shark bag suits TOWA's laid-back vibe well.<br>\nIf it caught your eye, start by checking the sizes and colors on the official online store!</p>",
        "<p>Not too loud, but a real head-turner once it's on your back, the shark bag suits TOWA's laid-back vibe well.<br>\nIt's easy on the wallet too, so grabbing one yourself and wearing it to a show or event to go see TOWA sounds like fun.<br>\nIf it caught your eye, start by checking the sizes and colors on the official online store!</p>",
    ),
}

for pid, (old, new) in EDITS.items():
    cur = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=H)
    cur.raise_for_status()
    content = cur.json()["content"]["raw"]
    if new in content:
        raise SystemExit(f"[{pid}] already updated")
    if old not in content:
        raise SystemExit(f"[{pid}] anchor not found")
    content = content.replace(old, new, 1)
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=HJSON,
                      data=json.dumps({"status": "draft", "content": content}).encode("utf-8"))
    r.raise_for_status()
    print("updated", pid)

print("DONE")
