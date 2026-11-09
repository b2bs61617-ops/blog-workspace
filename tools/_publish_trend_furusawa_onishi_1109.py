# 2026-11-09 chomoand.com ID13045 (Furusawa x Onishi rumor fact-check) publish -> Indexing -> X(@chomotirend) (Yuka request)
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
PID = 13045
TEXT = "【検証】古澤里紗と大西流星の「結婚計画流出」…😱\n100万回以上見られた投稿の正体、調べてみたら意外な事実が…！\n広まったタイミングにも理由があった👀"
TAGS = "#古澤里紗 #大西流星 #CUTIESTREET"
if "--check" in sys.argv:
    print(xb.weighted_length(TEXT + "\n" + TAGS)); sys.exit()
title = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()["title"]["raw"].replace("【未】", "")
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"status": "publish", "title": title}, auth=A, timeout=60).json()
link = r.get("link"); print("PUBLISH", PID, r.get("status"), r.get("title", {}).get("rendered"), link, flush=True)
try: print("INDEX", google_indexing.notify(link), flush=True)
except Exception as e: print("INDEX FAIL", e, flush=True)
try:
    imgs = xb.fetch_article_images(U, PID)
    print("X RESULT", len(imgs), "imgs", xb.post_thread(TEXT, TAGS, imgs, link, account="trend"), flush=True)
except Exception as e: print("X FAIL", e, flush=True)
