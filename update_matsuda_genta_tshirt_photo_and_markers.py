import base64, json, os, mimetypes, urllib.request
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

def upload_media(filepath, filename, alt=None):
    data = Path(filepath).read_bytes()
    mime = mimetypes.guess_type(filename)[0] or "image/jpeg"
    req = urllib.request.Request(
        f"{SITE}/wp-json/wp/v2/media",
        data=data,
        method="POST",
        headers={
            "Authorization": f"Basic {AUTH}",
            "Content-Type": mime,
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        media = json.loads(r.read())
    if alt:
        try:
            req2 = urllib.request.Request(
                f"{SITE}/wp-json/wp/v2/media/{media['id']}",
                data=json.dumps({"alt_text": alt, "title": alt}).encode("utf-8"),
                method="POST",
                headers=HEADERS_JSON,
            )
            with urllib.request.urlopen(req2, timeout=30) as r:
                json.loads(r.read())
        except Exception as e:
            print("warn: could not set alt text", e)
    return media

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

POST_ID = 859
IMG_PATH = ROOT / "tools" / "Xiy" / "posts_matsuda_necklace_disney" / "x_images" / "x_img_fullbody.jpg"
NEW_SOURCE_URL = "https://x.com/blue_tiger_eye/status/2090065857234055465"

if __name__ == "__main__":
    print("Uploading full-body photo...")
    photo = upload_media(IMG_PATH, "matsuda_genta_disney_border_tshirt_fullbody.jpg",
                          alt="ディズニーで赤とグレーのボーダーTシャツを着用する松田元太の全身ショット")
    sizes = photo["media_details"]["sizes"]
    large = sizes.get("large") or sizes.get("full")
    medium = sizes.get("medium")
    full = sizes.get("full") or {"source_url": photo["source_url"], "width": photo["media_details"]["width"], "height": photo["media_details"]["height"]}
    srcset = ", ".join(filter(None, [
        f"{medium['source_url']} {medium['width']}w" if medium else None,
        f"{large['source_url']} {large['width']}w",
        f"{full['source_url']} {full['width']}w",
    ]))
    print("PHOTO", photo["id"], large["source_url"])

    post = get_post(POST_ID)
    content = post["content"]["raw"]

    old_figure = """<!-- wp:html -->
<figure class="wp-block-image size-large">
<img src="https://chomoand-0.com/wp-content/uploads/2026/08/matsuda_genta_disney_necklace_selfie-704x1024.jpg" alt="ディズニーでのプライベートショットで、赤とグレーのボーダーTシャツを着用する松田元太" width="704" height="1024" style="max-width:100%;height:auto;" srcset="https://chomoand-0.com/wp-content/uploads/2026/08/matsuda_genta_disney_necklace_selfie-344x500.jpg 344w, https://chomoand-0.com/wp-content/uploads/2026/08/matsuda_genta_disney_necklace_selfie-704x1024.jpg 704w, https://chomoand-0.com/wp-content/uploads/2026/08/matsuda_genta_disney_necklace_selfie.jpg 1179w" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption style="font-size:0.8em;color:#888;">出典:https://x.com/ebikanic/status/2090048548708688254</figcaption>
</figure>
<!-- /wp:html -->"""

    new_figure = f"""<!-- wp:html -->
<figure class="wp-block-image size-large">
<img src="{large['source_url']}" alt="ディズニーで赤とグレーのボーダーTシャツを着用する松田元太の全身ショット" width="{large['width']}" height="{large['height']}" style="max-width:100%;height:auto;" srcset="{srcset}" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption style="font-size:0.8em;color:#888;">出典:{NEW_SOURCE_URL}</figcaption>
</figure>
<!-- /wp:html -->"""

    assert old_figure in content, "figure block not found"
    content = content.replace(old_figure, new_figure)

    old_shibutsu = "ただし、ラジオ収録の仕事着としてだけでなく、家族とのプライベートなディズニー旅行でも同じアイテムを着用していることから、<strong>私物である可能性が高い</strong>と考えられます。"
    new_shibutsu = 'ただし、ラジオ収録の仕事着としてだけでなく、家族とのプライベートなディズニー旅行でも同じアイテムを着用していることから、<strong><span class="swl-marker mark_blue" style="font-size:1.15em;">私物である可能性が高い</span></strong>と考えられます。'
    assert old_shibutsu in content, "shibutsu sentence not found"
    content = content.replace(old_shibutsu, new_shibutsu)

    result = update_content(POST_ID, content)
    print("UPDATED", result.get("id"), "status:", result.get("status"))
