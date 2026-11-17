# 2026-11-17 chomoand-0.com ID1545 (SixTONES jump rope test) publish -> YouTube embed fix -> Indexing -> X/Threads (Yuka request)
# Draft already has 2 frames from the official YouTube video, so no photo is added.
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
PID = 1545
TEXT = "大人6人が本気で縄跳び検定…！\nSixTONESがおそろいの体操服でぴょんぴょんしてて可愛さ致死量😭\n6人の最高は何級だったと思う？👀"
TAGS = "#SixTONES #スト担 #縄跳び検定"

p = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()
title = p["title"]["raw"].replace("【未】", "")
wp_env = {**os.environ, **{k: v for k, v in env.items() if k.startswith("WP_AUDITION_")}}
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"status": "publish", "title": title}, auth=A, timeout=60).json()
link = r.get("link"); print("PUBLISH", PID, r.get("status"), r.get("title", {}).get("rendered"), link, flush=True)
print(subprocess.run([sys.executable, str(ROOT / "tools/fix_youtube_embeds.py"), "--site", "AUDITION", "--ids", str(PID)], env=wp_env, capture_output=True, text=True).stdout, flush=True)
try: print("INDEX", google_indexing.notify(link), flush=True)
except Exception as e: print("INDEX FAIL", e, flush=True)
try:
    imgs = xb.fetch_article_images(U, PID)
    print("X RESULT", len(imgs), "imgs", xb.post_thread(TEXT, TAGS, imgs, link), flush=True)
except Exception as e: print("X FAIL", e, flush=True)
