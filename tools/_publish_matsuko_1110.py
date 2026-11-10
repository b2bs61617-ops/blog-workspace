# 2026-11-10 chomoand.com ID13070/13072 (Matsuko no Shiranai Sekai 11/10 guests) publish -> Indexing -> X(@chomotirend) (Yuka request)
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
    (13070, "【マツコの知らない世界】宮廷ドレスで「ごきげんよう」と登場した汐音凛さん👗\nドレスもかつらも全部手作りで約300着…！\n「日本のマリー・アントワネット」と呼ばれた理由と意外な経歴とは👀",
     "#マツコの知らない世界 #汐音凛 #宮廷ドレス"),
    (13072, "【マツコの知らない世界】漁港食堂を1000軒食べ歩いた野本良平さん🐟\n実はただのグルメじゃなかった…！\n魚の流通の常識をひっくり返した経歴がすごすぎる👀",
     "#マツコの知らない世界 #野本良平 #漁港食堂"),
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
