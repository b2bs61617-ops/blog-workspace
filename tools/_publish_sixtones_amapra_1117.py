# 2026-11-17 chomoand-0.com ID1556 (SixTONES on Amazon Prime Video) add 2 official Prime Video photos -> publish -> YouTube embed fix -> Indexing -> X/Threads (Yuka request)
# Draft had 0 photos. Season 1 H3: ep4 scene photo (@PrimeVideo_JP). Season 2 H3: SEASON2 key visual (@PrimeVideo_JP).
# X/Threads get only the scene photo: the key visual shows the title "ワロタ！", which is the article's answer.
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
PID = 1556
PHOTOS = [  # (H3 to insert under, image, alt, source)
    ('<h3 class="wp-block-heading">シーズン1(2025年)</h3>\n<!-- /wp:heading -->', ROOT / "images/x/sixtones_warota_ep4_scene_primevideo.jpg",
     "『ワロタ！』第4話の場面写真(コント「桃太郎」)", "https://x.com/PrimeVideo_JP/status/1961700452321382799"),
    ('<h3 class="wp-block-heading">シーズン2(2026年)</h3>\n<!-- /wp:heading -->', ROOT / "images/x/sixtones_warota_s2_visual_primevideo.jpg",
     "『ワロタ！SEASON2』のメインビジュアル", "https://x.com/PrimeVideo_JP/status/2071429701571088487"),
]
SNS_ONLY = "sixtones_warota_ep4_scene_primevideo"
TEXT = "え、アマプラでSixTONESがこんなに見られるの？👀\n6人の体当たりっぷりが反則すぎて腹筋崩壊😂\nどれから見るか迷う人向けにおすすめ5つまとめたよ🫶"
TAGS = "#SixTONES #スト担 #アマプラ"

def figure(img, alt, src):
    m = requests.post(f"{U}/wp-json/wp/v2/media", data=img.read_bytes(), auth=A, timeout=120,
                      headers={"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{img.name}"'}).json()
    requests.post(f"{U}/wp-json/wp/v2/media/{m['id']}", json={"alt_text": alt}, auth=A, timeout=60)
    s = m["media_details"]["sizes"]; lg = s.get("large") or s.get("medium") or {"source_url": m["source_url"], "width": m["media_details"]["width"], "height": m["media_details"]["height"]}
    srcset = ", ".join(f'{s[k]["source_url"]} {s[k]["width"]}w' for k in ("medium", "medium_large") if k in s) + f', {m["source_url"]} {m["media_details"]["width"]}w'
    print("MEDIA", m["id"], lg["source_url"], flush=True)
    return (f'\n\n<!-- wp:image {{"id":{m["id"]},"sizeSlug":"large"}} -->\n<figure class="wp-block-image size-large"><img src="{lg["source_url"]}" alt="{alt}" class="wp-image-{m["id"]}" '
            f'width="{lg["width"]}" height="{lg["height"]}" style="max-width:100%;height:auto;" srcset="{srcset}" sizes="(max-width: 1024px) 100vw, 1024px">'
            f'<figcaption style="font-size:0.8em;color:#888;">出典:{src}</figcaption></figure>\n<!-- /wp:image -->')

p = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()
content, title = p["content"]["raw"], p["title"]["raw"].replace("【未】", "")
for h3, img, alt, src in PHOTOS:
    if src in content: continue
    assert content.count(h3) == 1, h3
    content = content.replace(h3, h3 + figure(img, alt, src))
wp_env = {**os.environ, **{k: v for k, v in env.items() if k.startswith("WP_AUDITION_")}}
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"content": content, "status": "publish", "title": title}, auth=A, timeout=60).json()
link = r.get("link"); print("PUBLISH", PID, r.get("status"), r.get("title", {}).get("rendered"), link, flush=True)
print(subprocess.run([sys.executable, str(ROOT / "tools/fix_youtube_embeds.py"), "--site", "AUDITION", "--ids", str(PID)], env=wp_env, capture_output=True, text=True).stdout, flush=True)
try: print("INDEX", google_indexing.notify(link), flush=True)
except Exception as e: print("INDEX FAIL", e, flush=True)
try:
    imgs = [u for u in xb.fetch_article_images(U, PID) if SNS_ONLY in u]
    assert len(imgs) == 1, imgs
    print("X RESULT", len(imgs), "imgs", xb.post_thread(TEXT, TAGS, imgs, link), flush=True)
except Exception as e: print("X FAIL", e, flush=True)
