# 2026-11-17 chomoand-0.com ID1545 (SixTONES jump rope test) X/Threads REPOST with only the title frame (the first post's result-table frame gave away the answer; Yuka deleted it by hand) (Yuka request)
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

link = "https://chomoand-0.com/sixtones-jump-rope-test-results-1545"
imgs = [u for u in xb.fetch_article_images(U, PID) if "nawatobi_title" in str(u)]
assert len(imgs) == 1, imgs
print("X RESULT", len(imgs), "imgs", xb.post_thread(TEXT, TAGS, imgs, link), flush=True)
