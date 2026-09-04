# -*- coding: utf-8 -*-
"""Add bold + larger + yellow-marker emphasis to the ABEMA 'how to watch' sentence in the Mynavi TGC drafts (JP/KR/EN)."""
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
        return json.load(r)


OPEN = '<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">'
CLOSE = '</span></strong>'

TARGETS = {
    12280: "ABEMAはスマホアプリでもパソコンのブラウザでも視聴でき、会員登録やチケット購入をしなくても再生できます。",
    12284: "ABEMA는 스마트폰 앱에서도 PC 브라우저에서도 볼 수 있고, 회원 가입이나 티켓 구매 없이 재생할 수 있습니다.",
    12285: "You can watch ABEMA on the smartphone app or in a PC browser, and no account or ticket purchase is needed to press play.",
}

for pid, sentence in TARGETS.items():
    post = api(f"/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content", method="GET")
    raw = post["content"]["raw"]
    wrapped = OPEN + sentence + CLOSE
    if wrapped in raw:
        print(f"{pid}: already emphasized, skipping")
        continue
    if raw.count(sentence) != 1:
        print(f"{pid}: FOUND {raw.count(sentence)} occurrences, aborting this one")
        continue
    new_raw = raw.replace(sentence, wrapped, 1)
    res = api(f"/wp-json/wp/v2/posts/{pid}", {"content": new_raw, "status": "draft"}, "POST")
    chk = api(f"/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content", method="GET")
    ok = wrapped in chk["content"]["raw"]
    print(f"{pid}: updated, len {len(raw)} -> {len(chk['content']['raw'])}, emphasis present: {ok}")
