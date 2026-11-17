# 2026-11-17 chomoand-0.com ID1552 (SixTONES acrylic stand history) add official photo -> publish -> YouTube embed fix -> Indexing -> X/Threads (Yuka request)
# Draft had 0 photos and its official X sources were text-only, so add the official @SixTONES_SME 6-member photo posted on 2025-05-01
# (10th anniversary day = release day of the 10th anniversary acrylic stands) under the 10th anniversary H2.
import os, sys, subprocess
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, google_indexing, x_auto_post_buffer as xb
ENV_FILE = Path(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))
_orig = xb.load_env
def load_env(_path):
    env = _orig(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in _orig(ENV_FILE).items() if v and not k.startswith("GOOGLE_INDEXING")}); return env
xb.load_env = google_indexing.load_env = load_env
env = load_env(None)
U = env["WP_AUDITION_URL"].rstrip("/"); A = (env["WP_AUDITION_USERNAME"], env["WP_AUDITION_APP_PASSWORD"])
PID = 1552
SRC = "https://x.com/SixTONES_SME/status/1917897021991817222"
IMG = ROOT / "images/x/sixtones_10th_0501_sme.jpg"
ALT = "結成10周年の2025年5月1日にSixTONES公式Xに投稿された6人の写真"
TEXT = "SixTONESのアクスタ、全部持ってる人いる？👀\nJr.時代から10周年まで歴代まとめたら懐かしすぎて情緒ぶっ壊れた😭\n今から手に入れる方法も調べたよ🫶"
TAGS = "#SixTONES #スト担 #アクスタ"
H2 = '<h2 class="wp-block-heading">結成10周年の両面アクスタ(2025年)</h2>\n<!-- /wp:heading -->'

p = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()
content, title = p["content"]["raw"], p["title"]["raw"].replace("【未】", "")
if SRC not in content:
    assert content.count(H2) == 1, "insert point not found"
    m = requests.post(f"{U}/wp-json/wp/v2/media", data=IMG.read_bytes(), auth=A, timeout=120,
                      headers={"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{IMG.name}"'}).json()
    requests.post(f"{U}/wp-json/wp/v2/media/{m['id']}", json={"alt_text": ALT}, auth=A, timeout=60)
    s = m["media_details"]["sizes"]; lg = s.get("large") or s["medium"]
    srcset = ", ".join(f'{s[k]["source_url"]} {s[k]["width"]}w' for k in ("medium", "large", "medium_large") if k in s) + f', {m["source_url"]} {m["media_details"]["width"]}w'
    fig = (f'\n\n<!-- wp:image {{"id":{m["id"]},"sizeSlug":"large"}} -->\n<figure class="wp-block-image size-large"><img src="{lg["source_url"]}" alt="{ALT}" class="wp-image-{m["id"]}" '
           f'width="{lg["width"]}" height="{lg["height"]}" style="max-width:100%;height:auto;" srcset="{srcset}" sizes="(max-width: 1024px) 100vw, 1024px">'
           f'<figcaption style="font-size:0.8em;color:#888;">出典:{SRC}</figcaption></figure>\n<!-- /wp:image -->')
    content = content.replace(H2, H2 + fig); print("MEDIA", m["id"], lg["source_url"], flush=True)
wp_env = {**os.environ, **{k: v for k, v in env.items() if k.startswith("WP_AUDITION_")}}
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"content": content, "status": "publish", "title": title}, auth=A, timeout=60).json()
link = r.get("link"); print("PUBLISH", PID, r.get("status"), r.get("title", {}).get("rendered"), link, flush=True)
print(subprocess.run([sys.executable, str(ROOT / "tools/fix_youtube_embeds.py"), "--site", "AUDITION", "--ids", str(PID)], env=wp_env, capture_output=True, text=True).stdout, flush=True)
try: print("INDEX", google_indexing.notify(link), flush=True)
except Exception as e: print("INDEX FAIL", e, flush=True)
try:
    imgs = xb.fetch_article_images(U, PID)
    print("X RESULT", len(imgs), "imgs", xb.post_thread(TEXT, TAGS, imgs, link), flush=True)
except Exception as e: print("X FAIL", e, flush=True)
