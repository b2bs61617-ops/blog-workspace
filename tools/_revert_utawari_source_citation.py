# -*- coding: utf-8 -*-
"""Revert the source-tweet link back to a vaguer, non-linked phrasing per
user's follow-up: directly linking the exact source tweet made the 1:1
correspondence between the article and one fan's post too obvious/awkward.
Reverts to '(SNSで話題になっている)'-style wording, no link, no account
name -- applied to all 6 live drafts."""
import json, base64, urllib.request

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip().strip('"')

U = env["WP_KOIKEYS_USERNAME"]; P = env["WP_KOIKEYS_APP_PASSWORD"]; BASE = env["WP_KOIKEYS_URL"]
AUTH = base64.b64encode(f"{U}:{P}".encode()).decode()


def api(path, body=None, method="GET"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Authorization", "Basic " + AUTH)
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


RA_URL = "https://x.com/arigato___ryg/status/2098005662219546687"
BA_URL = "https://x.com/arigato___ryg/status/2097996056495845704"

JOBS = [
    (12980,
     f'<p>X(旧Twitter)の<a href="{RA_URL}" target="_blank" rel="noopener">こちらの投稿</a>で公開されていた耳コピをもとに、メンバー絵文字をローマ字の名前へ置き換えた歌割りが以下です。<br>',
     "<p>SNSで話題になっているファンの聞き取り(耳コピ)をもとに、メンバー絵文字をローマ字の名前へ置き換えた歌割りが以下です。<br>"),
    (12983,
     f'<p>X(旧Twitter)の<a href="{BA_URL}" target="_blank" rel="noopener">こちらの投稿</a>で公開されていた耳コピをもとに、メンバー絵文字をローマ字の名前へ置き換えた歌割りが以下です。<br>',
     "<p>SNSで話題になっているファンの聞き取り(耳コピ)をもとに、メンバー絵文字をローマ字の名前へ置き換えた歌割りが以下です。<br>"),
    (12989,
     f'<p>X(구 트위터)의 <a href="{RA_URL}" target="_blank" rel="noopener">이 게시물</a>에서 공개됐던 청취(귀로 듣고 옮긴 것)를 바탕으로, 멤버 이모지를 로마자 이름으로 바꾼 파트 분배는 아래와 같습니다.<br>',
     "<p>SNS에서 화제가 되고 있는 팬들의 청취(귀로 듣고 옮긴 것)를 바탕으로, 멤버 이모지를 로마자 이름으로 바꾼 파트 분배는 아래와 같습니다.<br>"),
    (12992,
     f'<p>X(구 트위터)의 <a href="{BA_URL}" target="_blank" rel="noopener">이 게시물</a>에서 공개됐던 청취(귀로 듣고 옮긴 것)를 바탕으로, 멤버 이모지를 로마자 이름으로 바꾼 파트 분배는 아래와 같습니다.<br>',
     "<p>SNS에서 화제가 되고 있는 팬들의 청취(귀로 듣고 옮긴 것)를 바탕으로, 멤버 이모지를 로마자 이름으로 바꾼 파트 분배는 아래와 같습니다.<br>"),
    (12990,
     f'<p>Based on the listening notes shared in <a href="{RA_URL}" target="_blank" rel="noopener">this X (formerly Twitter) post</a>, here is the part distribution with each member\'s emoji swapped for their romanized name.<br>',
     "<p>Based on fans' listening notes that have been getting attention on social media, here is the part distribution with each member's emoji swapped for their romanized name.<br>"),
    (12993,
     f'<p>Based on the listening notes shared in <a href="{BA_URL}" target="_blank" rel="noopener">this X (formerly Twitter) post</a>, here is the part distribution with each member\'s emoji swapped for their romanized name.<br>',
     "<p>Based on fans' listening notes that have been getting attention on social media, here is the part distribution with each member's emoji swapped for their romanized name.<br>"),
]

for pid, old, new in JOBS:
    cur = api(f"/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content,slug")
    raw = cur["content"]["raw"]
    if old not in raw:
        print(f"!! not found in {pid}")
        continue
    raw2 = raw.replace(old, new)
    api(f"/wp-json/wp/v2/posts/{pid}", {"content": raw2, "status": "draft"}, "POST")
    print(f"reverted {pid} OK")
