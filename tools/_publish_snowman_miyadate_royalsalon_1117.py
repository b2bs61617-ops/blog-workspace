# 2026-11-17 chomoand-2.com ID705 (Miyadate Royal Salon outfit) publish -> Indexing -> X/Threads with article photos (Yuka)
import os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, google_indexing, x_auto_post_buffer as xb
_orig = xb.load_env
def load_env(_path):
    env = _orig(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in _orig(xb.DRIVE_ENV).items() if v and not k.startswith("GOOGLE_INDEXING")}); return env
google_indexing.load_env = load_env
env = load_env(None)
U = env["WP_CHOMO2_URL"].rstrip("/"); A = (env["WP_CHOMO2_USERNAME"], env["WP_CHOMO2_APP_PASSWORD"])
PID = 705
TEXT = 'ロイヤルサロンの宮舘涼太くん、スタジオで紅茶飲んでる私服が優勝すぎる…🫖✨\n胸に十字架の黒ハーフジップと、赤いキスマークのローファー😭💋\n足もとまで貴族で心臓もたない\U0001fae0'
TAGS = "#SnowMan #宮舘涼太 #ロイヤルサロン"
if "--check" in sys.argv:
    print(xb.weighted_length(xb.compose_tweet_text(TEXT, TAGS))); sys.exit()
title = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()["title"]["raw"].replace("【未】", "")
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"status": "publish", "title": title}, auth=A, timeout=60).json()
link = r.get("link"); print("PUBLISH", PID, r.get("status"), r.get("title", {}).get("rendered"), link, flush=True)
try: print("INDEX", google_indexing.notify(link), flush=True)
except Exception as e: print("INDEX FAIL", e, flush=True)
IMGS = xb.fetch_article_images(U, PID); print("IMAGES", len(IMGS), flush=True)
if not IMGS: print("X SKIP: no photos"); sys.exit()
try: print("X RESULT", xb.post_thread(TEXT, TAGS, IMGS, link), flush=True)
except Exception as e: print("X FAIL", e, flush=True)
