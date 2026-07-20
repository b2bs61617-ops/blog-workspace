import json, base64, subprocess, sys, urllib.request, mimetypes
from pathlib import Path

ROOT = Path(__file__).parent

def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env

ENV = load_env(ROOT / ".env")
WP_SITE_URL = ENV["WP_TREND_URL"].rstrip("/")
WP_USER = ENV["WP_TREND_USERNAME"]
WP_PASS = ENV["WP_TREND_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()

def api(path, method="GET", payload=None, raw=None, content_type=None, extra_headers=None):
    url = f"{WP_SITE_URL}/wp-json/wp/v2/{path}"
    headers = {"Authorization": f"Basic {AUTH}", "User-Agent": "Mozilla/5.0"}
    if extra_headers:
        headers.update(extra_headers)
    if raw is not None:
        data = raw
        headers["Content-Type"] = content_type
    elif payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    else:
        data = None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

people = [
    ("kiichan", "きぃちゃん", 0),
    ("tsuchan", "つーちゃん", 33),
    ("baby", "Baby", 65),
    ("amo", "あも", 98),
    ("milk", "Milk", 131),
    ("otosan", "おとさん", 163),
    ("nisei", "二世", 196),
    ("tenten", "てんてん", 229),
    ("tekarin", "てかりん", 262),
    ("tackle", "タックル", 294),
    ("yanbo", "ヤンボー", 327),
]

TYPE_SPEC = {
    "wiki": {
        "top": ["ラヴ上等2", "wiki・プロフィール"],
        "bottom": ["本名・経歴を調査", "SNSまとめ"],
    },
    "shokugyo_nenshu": {
        "top": ["ラヴ上等2", "職業・年収"],
        "bottom": ["気になる年収を", "徹底調査!"],
    },
    "gakureki": {
        "top": ["ラヴ上等2", "学歴"],
        "bottom": ["出身校・経歴を", "徹底調査!"],
    },
    "hanzaireki": {
        "top": ["ラヴ上等2", "逮捕歴・犯罪歴"],
        "bottom": ["気になる噂を", "徹底調査!"],
    },
}

START_ID = 11642
post_id = START_ID
results = []
errors = []

for key, nick, hue in people:
    for typ, spec in TYPE_SPEC.items():
        out_path = ROOT / "images" / f"lovejoto_{key}_{typ}_eyecatch_chomoand.png"
        cmd = [sys.executable, "tools/eyecatch_chomoand.py"]
        for t in spec["top"]:
            cmd += ["--top", t]
        cmd += ["--main", nick]
        for b in spec["bottom"]:
            cmd += ["--bottom", b]
        cmd += ["--hue", str(hue), "--out", str(out_path)]

        try:
            subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            errors.append(f"GEN FAILED id:{post_id} {key}_{typ}: {e.stderr.decode(errors='ignore')[:300]}")
            post_id += 1
            continue

        try:
            img_bytes = out_path.read_bytes()
            media = api(
                "media", "POST", raw=img_bytes, content_type="image/png",
                extra_headers={"Content-Disposition": f'attachment; filename="{out_path.name}"'},
            )
            media_id = media["id"]
            api(f"posts/{post_id}", "POST", {"featured_media": media_id})
            results.append((post_id, key, typ, media_id))
            print(f"OK id:{post_id} {key}_{typ} media:{media_id}")
        except Exception as e:
            errors.append(f"UPLOAD FAILED id:{post_id} {key}_{typ}: {e}")
            print(f"UPLOAD FAILED id:{post_id} {key}_{typ}: {e}")

        post_id += 1

print(f"\n合計: {len(results)}件成功 / {len(errors)}件失敗")
if errors:
    for e in errors:
        print(e)
