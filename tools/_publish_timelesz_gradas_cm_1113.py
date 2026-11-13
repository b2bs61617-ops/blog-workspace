# 2026-11-13 chomoand.com ID13176 (timelesz GRADAS CM) publish -> Indexing -> X(@chomotirend) (Yuka request)
# WP_TREND_*/BUFFER_* come from the Google Drive .env; GOOGLE_INDEXING* stays local (Drive value is a Windows path)
import os, sys
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
U = env["WP_TREND_URL"].rstrip("/"); A = (env["WP_TREND_USERNAME"], env["WP_TREND_APP_PASSWORD"])
POSTS = [
    (13176, "timeleszのABCマート新CM、冒頭4秒に\"影にかくれた人物\"が…👀\nXでは「周杜くんでは？」と騒然🚨\nさらに足元アップに「8人目の足」説まで…！\n全シーン確かめたら意外な結論に😱",
     "#timelesz #タイムレス #ABCマート #GRADAS"),
]
if "--check" in sys.argv:
    for _, t, g in POSTS: print(xb.weighted_length(t + "\n" + g))
    sys.exit()
for PID, TEXT, TAGS in POSTS:
    title = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()["title"]["raw"].replace("【未】", "")
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"status": "publish", "title": title}, auth=A, timeout=60).json()
    link = r.get("link"); print("PUBLISH", PID, r.get("status"), r.get("title", {}).get("rendered"), link, flush=True)
    try: print("INDEX", google_indexing.notify(link), flush=True)
    except Exception as e: print("INDEX FAIL", e, flush=True)
    try:
        imgs = xb.fetch_article_images(U, PID)
        print("X RESULT", len(imgs), "imgs", xb.post_thread(TEXT, TAGS, imgs, link, account="trend"), flush=True)
    except Exception as e: print("X FAIL", e, flush=True)
