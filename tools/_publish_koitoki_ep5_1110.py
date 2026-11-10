# 2026-11-10 恋とき5話ラスト記事(chomoand.com ID13075)を【未】を外して公開→Indexing、Xは@chomotirend(--account trend)に即時投稿
# このMacの.envにはWP_TREND_*の認証が無いので、Googleドライブの.envを読ませる(TREND_ENV_FILE)
import os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, google_indexing, x_auto_post_buffer as xb
ENV_FILE = Path(os.environ.get("TREND_ENV_FILE") or ROOT / ".env")
_orig = xb.load_env
def load_env(_path):
    env = _orig(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in _orig(ENV_FILE).items() if v and not k.startswith("GOOGLE_INDEXING")}); return env
xb.load_env = google_indexing.load_env = load_env
env = load_env(None)
U = env["WP_TREND_URL"].rstrip("/"); A = (env["WP_TREND_USERNAME"], env["WP_TREND_APP_PASSWORD"])
PID = 13075
TITLE = "恋とき5話ラストのいろはの背中の傷は何？凜花は何者？6話を予想！"
TEXT = "【恋とき5話】ラスト数分で空気が一変…😱\nペットボトルの蓋が当たっただけで、いろはの背中に\"刀傷\"のような跡が⚡\n凜花は握手の瞬間、何に気づいたのか…"
TAGS = "#恋とき #いろはの恋は時代をかける #剛力彩芽"
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"status": "publish", "title": TITLE}, auth=A, timeout=60).json()
link = r.get("link"); print("PUBLISH", PID, r.get("status"), link, r.get("title", {}).get("raw") or r.get("title", {}).get("rendered"), flush=True)
try: print("INDEX", google_indexing.notify(link), flush=True)
except Exception as e: print("INDEX FAIL", e, flush=True)
try:
    imgs = xb.fetch_article_images(U, PID)
    print("X RESULT", len(imgs), "imgs", xb.post_thread(TEXT, TAGS, imgs, link, account="trend"), flush=True)
except Exception as e: print("X FAIL", e, flush=True)
