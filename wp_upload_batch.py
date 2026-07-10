import sys, json, base64, re, urllib.request, urllib.parse, os
from pathlib import Path

def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env

ROOT = Path(__file__).parent
ENV = {**load_env(ROOT / ".env"), **os.environ}

# このスクリプトはトレンドブログ(chomoand.com)専用
WP_SITE_URL = ENV["WP_TREND_URL"].rstrip("/")
WP_URL = f"{WP_SITE_URL}/wp-json/wp/v2/posts"
WP_USER = ENV["WP_TREND_USERNAME"]
WP_PASS = ENV["WP_TREND_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()

def md_to_html(md):
    lines = md.strip().split("\n")
    html = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("# "):
            i += 1
            continue
        elif line.startswith("## "):
            html.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("### "):
            html.append(f"<h3>{line[4:].strip()}</h3>")
        elif line.strip() == "---":
            html.append("<hr>")
        elif line.strip().startswith("<"):
            html.append(line.strip())
        elif line.strip() == "":
            pass
        else:
            p = line.strip()
            p = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p)
            if p:
                html.append(f"<p>{p}</p>")
        i += 1
    return "\n".join(html)

def get_slug(title):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={urllib.parse.quote(title)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    en = data[0][0][0]
    slug = re.sub(r'[^a-z0-9\s-]', '', en.lower())
    slug = re.sub(r'[\s]+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)[:30].rstrip('-')
    return slug

def post_wp(title, content, slug):
    payload = json.dumps({"title": title, "content": content, "slug": slug, "status": "draft", "categories": [3]}).encode()
    req = urllib.request.Request(WP_URL, data=payload, method="POST", headers={
        "Authorization": f"Basic {AUTH}",
        "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

articles = [
    ROOT / "articles" / "notch_pachinko_keireki.md",
    ROOT / "articles" / "notch_pachinko_kazoku.md",
]

results = []
for path in articles:
    with open(path, encoding="utf-8") as f:
        md = f.read()
    title = md.split("\n")[0].lstrip("# ").strip()
    content = md_to_html(md)
    slug = get_slug(title)
    res = post_wp(title, content, slug)
    post_id = res.get("id")
    print(f"OK | ID:{post_id} | slug:{slug}")
    print(f"   タイトル: {title[:50]}")
    results.append({"id": post_id, "title": title, "slug": slug})

print("\n--- 投稿完了 ---")
for r in results:
    print(f"ID:{r['id']} https://chomoand.com/?p={r['id']}")
