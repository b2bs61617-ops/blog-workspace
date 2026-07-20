import json, base64, urllib.request, urllib.parse, re, time
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

def get_or_create_category(name):
    cats = api(f"categories?search={urllib.parse.quote(name)}&per_page=100")
    for c in cats:
        if c["name"] == name:
            return c["id"]
    created = api("categories", "POST", {"name": name})
    return created["id"]

def get_slug(title):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={urllib.parse.quote(title)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    en = "".join(seg[0] for seg in data[0])
    slug = re.sub(r'[^a-z0-9\s-]', '', en.lower())
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)[:30].rstrip('-')
    return slug or "post"

CATEGORY_ID = get_or_create_category("ラヴ上等")
print(f"category id: {CATEGORY_ID}")

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
    "wiki": "ラヴ上等｜{nick}のwikiプロフィール!本名・経歴・SNSまとめ(シーズン2)",
    "shokugyo_nenshu": "ラヴ上等 {nick}の職業は?気になる年収も調査!(シーズン2)",
    "gakureki": "ラヴ上等 {nick}の学歴は?出身校・経歴を徹底調査!(シーズン2)",
    "hanzaireki": "ラヴ上等 {nick}に逮捕歴はある?犯罪歴を徹底調査!(シーズン2)",
}

results = []
errors = []

for key, nick in people:
    for typ, title_fmt in TYPE_TITLES.items():
        fname = f"lovejoto_{key}_{typ}.html"
        fpath = ROOT / "articles" / fname
        if not fpath.exists():
            errors.append(f"MISSING FILE: {fname}")
            continue
        content = fpath.read_text(encoding="utf-8")
        title = title_fmt.format(nick=nick)
        try:
            slug = get_slug(title)
        except Exception as e:
            slug = f"{key}-{typ}"
        try:
            res = api("posts", "POST", {
                "title": title,
                "content": content,
                "slug": slug,
                "status": "draft",
                "categories": [CATEGORY_ID],
            })
            post_id = res.get("id")
            results.append({"file": fname, "id": post_id, "slug": res.get("slug"), "title": title})
            print(f"OK id:{post_id} {fname}")
        except Exception as e:
            errors.append(f"FAILED {fname}: {e}")
            print(f"FAILED {fname}: {e}")
        time.sleep(0.3)

print("\n--- 投稿結果 ---")
for r in results:
    print(f"ID:{r['id']} {WP_SITE_URL}/?p={r['id']}  ({r['file']})")

if errors:
    print("\n--- エラー ---")
    for e in errors:
        print(e)

print(f"\n合計: {len(results)}件成功 / {len(errors)}件失敗")
