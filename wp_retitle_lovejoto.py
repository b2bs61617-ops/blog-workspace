import json, base64, urllib.request
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

people = [
    ("kiichan", "きぃちゃん"),
    ("tsuchan", "つーちゃん"),
    ("baby", "Baby"),
    ("amo", "あも"),
    ("milk", "Milk"),
    ("otosan", "おとさん"),
    ("nisei", "二世"),
    ("tenten", "てんてん"),
    ("tekarin", "てかりん"),
    ("tackle", "タックル"),
    ("yanbo", "ヤンボー"),
]

TYPE_TITLES = {
    "wiki": "ラヴ上等2｜{nick}のwikiプロフィール!本名・経歴・SNSまとめ",
    "shokugyo_nenshu": "ラヴ上等2 {nick}の職業は?気になる年収も調査!",
    "gakureki": "ラヴ上等2 {nick}の学歴は?出身校・経歴を徹底調査!",
    "hanzaireki": "ラヴ上等2 {nick}に逮捕歴はある?犯罪歴を徹底調査!",
}

START_ID = 11642
post_id = START_ID
updated = []
errors = []

for key, nick in people:
    for typ, title_fmt in TYPE_TITLES.items():
        new_title = title_fmt.format(nick=nick)
        try:
            res = api(f"posts/{post_id}", "POST", {"title": new_title})
            updated.append((post_id, res.get("title", {}).get("rendered", new_title)))
            print(f"OK id:{post_id} -> {new_title}")
        except Exception as e:
            errors.append(f"FAILED id:{post_id}: {e}")
            print(f"FAILED id:{post_id}: {e}")
        post_id += 1

print(f"\n合計: {len(updated)}件更新 / {len(errors)}件失敗")
if errors:
    for e in errors:
        print(e)
