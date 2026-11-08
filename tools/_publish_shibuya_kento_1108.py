# 2026-11-08 渋谷謙人3記事(chomoand.com)を公開→Indexing、Xは@chomotirend(--account trend)に3分おきで即時投稿
# このMacの.envにはWP_TREND_*/BUFFER_*が無いので、Googleドライブの.envを読ませる(TREND_ENV_FILE)
import os, sys, time
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
POSTS = [
    (12987, "え、のっちの結婚相手って誰！？と検索した人、絶対見たことある👀\n8歳デビュー、14歳で大河出演、今まさに\"あの大河\"に出演中…！\n実家の家業も意外すぎた🔥", "#のっち #渋谷謙人 #豊臣兄弟"),
    (12984, "【のっち結婚】お相手の渋谷謙人、実は元ヴェルディJr.ユース⚽\n中学で「両立はもう難しい」とサッカーを諦めて役者一本に…\n高校も\"ある理由\"で途中で…😳", "#のっち #渋谷謙人 #Perfume"),
    (12990, "【電撃婚】のっち×渋谷謙人、熱愛報道ゼロからの結婚😱\n過去に名前が挙がった元カノは\"たった1人\"…\nしかもあの人気ドラマの共演者だった⚡", "#のっち #渋谷謙人 #Perfume"),
]
links = {}
for pid, _, _ in POSTS:
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", json={"status": "publish"}, auth=A, timeout=60).json()
    links[pid] = r.get("link"); print("PUBLISH", pid, r.get("status"), r.get("link"), flush=True)
    try: print("INDEX", pid, google_indexing.notify(r.get("link")), flush=True)
    except Exception as e: print("INDEX FAIL", pid, e, flush=True)
for i, (pid, text, tags) in enumerate(POSTS):
    if i: time.sleep(180)
    print("X", pid, time.strftime("%H:%M:%S"), flush=True)
    try:
        imgs = xb.fetch_article_images(U, pid)
        res = xb.post_thread(text, tags, imgs, links[pid], account="trend")
        print("X RESULT", pid, len(imgs), "imgs", res, flush=True)
    except Exception as e: print("X FAIL", pid, e, flush=True)
print("DONE", flush=True)
