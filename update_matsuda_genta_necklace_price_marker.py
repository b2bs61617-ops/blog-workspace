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

    old = """<p>ティファニー ハードウェアのグラジュエイテッド リンク ネックレスは、素材やダイヤモンドの有無によって価格帯に大きな幅があります。<br>
一番手に取りやすいスターリングシルバーのシンプルなタイプで<strong>45万円前後</strong>、ダイヤモンドを使わないイエローゴールドのタイプでも<strong>330万円前後</strong>という価格帯です。<br>
一方、松田元太さんが着けていたようなパヴェダイヤモンドをあしらったゴールドの上位モデルになると価格は一気に跳ね上がり、ホワイトゴールド×ダイヤモンドのタイプで1,000万円台に達するモデルも存在します。<br>
今回話題になった投稿でも、参考価格として<strong>1,468万5,000円</strong>という金額が紹介されており、ハードウェアシリーズの中でもかなり上位のモデルにあたることがうかがえます。</p>"""

    new = """<p>ティファニー ハードウェアのグラジュエイテッド リンク ネックレスは、素材やダイヤモンドの有無によって価格帯に大きな幅があります。<br>
一番手に取りやすいスターリングシルバーのシンプルなタイプで<strong><span class="swl-marker mark_blue">45万円前後</span></strong>、ダイヤモンドを使わないイエローゴールドのタイプでも<strong><span class="swl-marker mark_blue">330万円前後</span></strong>という価格帯です。<br>
一方、松田元太さんが着けていたようなパヴェダイヤモンドをあしらったゴールドの上位モデルになると価格は一気に跳ね上がり、ホワイトゴールド×ダイヤモンドのタイプで<strong><span class="swl-marker mark_blue">1,000万円台</span></strong>に達するモデルも存在します。<br>
松田元太さんが着けていたモデルの参考価格も<strong><span class="swl-marker mark_blue">1,468万5,000円</span></strong>ほどとみられ、ハードウェアシリーズの中でもかなり上位のモデルにあたることがうかがえます。</p>"""

    assert old in content, "target paragraph not found"
    content = content.replace(old, new)

    result = update_content(POST_ID, content)
    print("UPDATED", result.get("id"), "status:", result.get("status"))
