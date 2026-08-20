import base64, json, os, urllib.request
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

ENV = {**load_env(ROOT / ".env"), **os.environ}
SITE = ENV["WP_AUDITION_URL"].rstrip("/")
USER = ENV["WP_AUDITION_USERNAME"]
APP_PW = ENV["WP_AUDITION_APP_PASSWORD"]
AUTH = base64.b64encode(f"{USER}:{APP_PW}".encode()).decode()
HEADERS_JSON = {"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"}

def get_post(post_id):
    req = urllib.request.Request(f"{SITE}/wp-json/wp/v2/posts/{post_id}?context=edit", headers={"Authorization": f"Basic {AUTH}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def update_content(post_id, content):
    payload = {"content": content, "status": "draft"}
    req = urllib.request.Request(
        f"{SITE}/wp-json/wp/v2/posts/{post_id}",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers=HEADERS_JSON,
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

POST_ID = 850

if __name__ == "__main__":
    post = get_post(POST_ID)
    content = post["content"]["raw"]

    old = """<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-0.com/?p=812">サマソニ衣装で着用していたベルトのブランドを調べた記事</a></li>
<li><a href="https://chomoand-0.com/?p=638">On My Roadで履いていたスニーカーを特定した記事</a></li>
</ul>"""
    new = """<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-0.com/?p=859">同じディズニーでのショットで着用していたボーダーTシャツを特定した記事</a></li>
<li><a href="https://chomoand-0.com/?p=812">サマソニ衣装で着用していたベルトのブランドを調べた記事</a></li>
<li><a href="https://chomoand-0.com/?p=638">On My Roadで履いていたスニーカーを特定した記事</a></li>
</ul>"""
    assert old in content, "target list not found"
    content = content.replace(old, new)

    result = update_content(POST_ID, content)
    print("UPDATED", result.get("id"), "status:", result.get("status"))
