import json, base64, urllib.request, subprocess, sys
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
HEADERS = {"Authorization": f"Basic {AUTH}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

def api(path, method="GET", payload=None):
    url = f"{WP_SITE_URL}/wp-json/wp/v2/{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())

post_ids = list(range(11642, 11686))
published = []
errors = []

for pid in post_ids:
    try:
        res = api(f"posts/{pid}", "POST", {"status": "publish"})
        url = f"{WP_SITE_URL}/?p={pid}"
        published.append((pid, url))
        print(f"OK id:{pid} -> {url}")
    except Exception as e:
        errors.append(f"FAILED id:{pid}: {e}")
        print(f"FAILED id:{pid}: {e}")

print(f"\n合計: {len(published)}件公開 / {len(errors)}件失敗")

for pid, url in published:
    try:
        subprocess.run([sys.executable, "tools/google_indexing.py", url], cwd=ROOT, capture_output=True, timeout=30)
    except Exception:
        pass

if errors:
    for e in errors:
        print(e)
