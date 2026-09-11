# -*- coding: utf-8 -*-
"""Apply the two flow/readability fixes (requested after review) to all 6 live
utawari drafts (JP/KR/EN x Run Again/BLACK ANGEL):
1. BLACK ANGEL 'notable points': pull the long quoted pre-chorus lyric out of
   the run-on <strong> sentence into its own small bordered quote box.
2. Both songs, both 'notable points' sections: pull the "see also our emoji /
   color articles" reference sentence out into its own small bordered box,
   instead of tacking it onto the end of the analysis paragraph via <br>.
"""
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


BOX_OPEN = '<!-- wp:html -->\n<div style="border-left:3px solid #8a8378;background:#f7f6f4;padding:8px 14px;margin:0 0 12px 0;font-size:0.9em;color:#555;">'
BOX_OPEN_QUOTE = '<!-- wp:html -->\n<div style="border-left:3px solid #8a8378;background:#f7f6f4;padding:8px 14px;margin:0 0 12px 0;font-size:0.95em;color:#555;">'
BOX_CLOSE = '</div>\n<!-- /wp:html -->'

JOBS = []

# ---- 1) BLACK ANGEL wanna-love-you quote box: JP / KR / EN ----
JOBS.append((12983,
    '<p>\u9593\u594f\u3067\u633f\u307e\u308b<strong>\u300cPray / \u95c7\u306b\u67d3\u3081\u3066\u3053\u306e\u307e\u307e2\u4eba / Sol\u611b\u300d\u306f\u30011\u56de\u76eeSHINHAENG\u30012\u56de\u76eeYURA</strong>\u3068\u62c5\u5f53\u3057\u307e\u3059\u3002<br>\n'
    '\u30d7\u30ea\u30b3\u30fc\u30e9\u30b9\u306e<strong>\u300c\u541b\u306b\u5815\u3061\u3066\u884c\u304ffalling / \u4f55\u5ea6\u3082\u6c42\u3081\u7d9a\u3051\u308bpain / Settle me down, so settle me down / \u5206\u304b\u3063\u3066\u3044\u308b\u306e\u306b wanna love you\u300d\u3082\u30011\u756a\u30682\u756a\u3067\u6b4c\u30474\u4eba\u304c\u307e\u308b\u3054\u3068\u5165\u308c\u66ff\u308f\u308b</strong>\u73cd\u3057\u3044\u69cb\u6210\u3067\u3059(1\u756a:YURA\u2192RYUJI\u2192YUKI\u2192SIYOUNG\u30012\u756a:SIYOUNG\u2192RYOGA\u2192YUKI\u2192SHINHAENG)\u3002<br>\n'
    '\u3053\u306e\u66f2\u3067\u552f\u4e00\u306e\u639b\u3051\u5408\u3044\u304c<strong>\u300c\u5168\u3066\u3092\u6349\u3052\u3088\u3046\u300d\u306eRYOGA\u30fbYUKI</strong>\u3067\u3001\u30c0\u30fc\u30af\u306a\u4e16\u754c\u89b3\u306e\u4e2d\u3067\u3082\u5225\u4eba\u306e\u58f0\u304c\u91cd\u306a\u308b\u5370\u8c61\u7684\u306a\u4e00\u7bc0\u306b\u306a\u3063\u3066\u3044\u307e\u3059\u3002</p>',
    '<p>\u9593\u594f\u3067\u633f\u307e\u308b<strong>\u300cPray / \u95c7\u306b\u67d3\u3081\u3066\u3053\u306e\u307e\u307e2\u4eba / Sol\u611b\u300d\u306f\u30011\u56de\u76eeSHINHAENG\u30012\u56de\u76eeYURA</strong>\u3068\u62c5\u5f53\u3057\u307e\u3059\u3002</p>\n'
    '<!-- /wp:paragraph -->\n\n' + BOX_OPEN_QUOTE +
    '\u300c\u541b\u306b\u5815\u3061\u3066\u884c\u304ffalling / \u4f55\u5ea6\u3082\u6c42\u3081\u7d9a\u3051\u308bpain / Settle me down, so settle me down / \u5206\u304b\u3063\u3066\u3044\u308b\u306e\u306b wanna love you\u300d' + BOX_CLOSE +
    '\n\n<!-- wp:paragraph -->\n<p>\u3053\u306e\u30d7\u30ea\u30b3\u30fc\u30e9\u30b9\u3082\u3001<strong>1\u756a\u30682\u756a\u3067\u6b4c\u30474\u4eba\u304c\u307e\u308b\u3054\u3068\u5165\u308c\u66ff\u308f\u308b</strong>\u73cd\u3057\u3044\u69cb\u6210\u3067\u3059(1\u756a:YURA\u2192RYUJI\u2192YUKI\u2192SIYOUNG\u30012\u756a:SIYOUNG\u2192RYOGA\u2192YUKI\u2192SHINHAENG)\u3002<br>\n'
    '\u3053\u306e\u66f2\u3067\u552f\u4e00\u306e\u639b\u3051\u5408\u3044\u304c<strong>\u300c\u5168\u3066\u3092\u6349\u3052\u3088\u3046\u300d\u306eRYOGA\u30fbYUKI</strong>\u3067\u3001\u30c0\u30fc\u30af\u306a\u4e16\u754c\u89b3\u306e\u4e2d\u3067\u3082\u5225\u4eba\u306e\u58f0\u304c\u91cd\u306a\u308b\u5370\u8c61\u7684\u306a\u4e00\u7bc0\u306b\u306a\u3063\u3066\u3044\u307e\u3059\u3002</p>',
))

with open(REPO + r"\tools\_flow_fixes_data.json", encoding="utf-8") as f:
    extra = json.load(f)

for pid, old, new in extra:
    JOBS.append((pid, old, new))

for pid, old, new in JOBS:
    cur = api(f"/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content,slug")
    raw = cur["content"]["raw"]
    if old not in raw:
        print(f"!! not found in {pid} (looking for {old[:60]!r}...)")
        continue
    raw2 = raw.replace(old, new)
    api(f"/wp-json/wp/v2/posts/{pid}", {"content": raw2, "status": "draft"}, "POST")
    print(f"patched {pid} OK")
