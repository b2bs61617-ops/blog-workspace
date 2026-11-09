# 2026-11-09 VIVANT「4歳の薫」記事(chomoand.com ID13037)を公開→Indexing、Xは@chomotirend(--account trend)に即時投稿
# このMacの.envにはWP_TREND_*/BUFFER_*が無いので、Googleドライブの.envを読ませる(TREND_ENV_FILE)
import os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, google_indexing, x_auto_post_buffer as xb
ENV_FILE = Path(os.environ.get("TREND_ENV_FILE") or ROOT / ".env")
_orig = xb.load_env
def load_env(_path):
    env = _orig(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in _orig(ENV_FILE).items() if v and not k.startswith("GOOGLE_INDEXING")}); return env  # ドライブ.envのIndexing鍵パスはWindows用なのでローカルを優先
xb.load_env = google_indexing.load_env = load_env
env = load_env(None)
U = env["WP_TREND_URL"].rstrip("/"); A = (env["WP_TREND_USERNAME"], env["WP_TREND_APP_PASSWORD"])
PID = 13037
TEXT = "【VIVANT】\"4歳の薫\"って知ってた？👀\n第21話の放送日、子役事務所が出演を告知→その日の深夜に削除…😱\nなのに最終回まで一度も登場せず。\n消えた理由、映画とつながってる説がヤバい🔥"
TAGS = "#VIVANT #映画VIVANT #二階堂ふみ"
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"status": "publish"}, auth=A, timeout=60).json()
link = r.get("link"); print("PUBLISH", PID, r.get("status"), link, flush=True)
try: print("INDEX", google_indexing.notify(link), flush=True)
except Exception as e: print("INDEX FAIL", e, flush=True)
try:
    imgs = xb.fetch_article_images(U, PID)
    print("X RESULT", len(imgs), "imgs", xb.post_thread(TEXT, TAGS, imgs, link, account="trend"), flush=True)
except Exception as e: print("X FAIL", e, flush=True)
