# 2026-11-13 chomoand-5.site ID691 (キテレツキテル HYROX gym location) publish -> YouTube embed fix -> Indexing -> X/Threads (Yuka request)
# WP_CHOMO5_*/BUFFER_* come from the Google Drive .env; GOOGLE_INDEXING* stays local (Drive value is a Windows path)
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
U = env["WP_CHOMO5_URL"].rstrip("/"); A = (env["WP_CHOMO5_USERNAME"], env["WP_CHOMO5_APP_PASSWORD"])
POSTS = [
    (691, "キテレツキテルのHYROX回、5人がガチで挑んだジムってどこか気になってた人いる？👀\nシャンデリアに大はしゃぎの5人、可愛さ致死量😭💕\n会員じゃなくても1回5,500円で入れるらしい…聖地巡礼したすぎる🔥",
     "#KEYTOLIT #キテレツキテル #佐久間大介"),
]
if "--check" in sys.argv:
    for _, t, g in POSTS: print(xb.weighted_length(t + "\n" + g))
    sys.exit()
wp_env = {**os.environ, **{k: v for k, v in env.items() if k.startswith("WP_CHOMO5_")}}
for PID, TEXT, TAGS in POSTS:
    print(subprocess.run([sys.executable, str(ROOT / "tools/fix_youtube_embeds.py"), "--site", "CHOMO5", "--ids", str(PID)], env=wp_env, capture_output=True, text=True).stdout, flush=True)
    title = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()["title"]["raw"].replace("【未】", "")
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"status": "publish", "title": title}, auth=A, timeout=60).json()
    link = r.get("link"); print("PUBLISH", PID, r.get("status"), r.get("title", {}).get("rendered"), link, flush=True)
    try: print("INDEX", google_indexing.notify(link), flush=True)
    except Exception as e: print("INDEX FAIL", e, flush=True)
    try:
        imgs = xb.fetch_article_images(U, PID)
        print("X RESULT", len(imgs), "imgs", xb.post_thread(TEXT, TAGS, imgs, link), flush=True)
    except Exception as e: print("X FAIL", e, flush=True)
