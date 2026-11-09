# 2026-11-09 SixTONES(chomoand-0.com) ID1436(愛用香水まとめ)・ID1440(北斗の水筒)を公開→Indexing→X/Threadsを3分おきに即時投稿(ユカ依頼)
# このMacの.envにはWP_AUDITION_*/BUFFER_*が無いので、Googleドライブの.envを読ませる(SIXTONES_ENV_FILE)
# 1440の本文画像は楽天の商品写真(ロゴで答えがバレる)なのでXは画像なしで投稿する
import os, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, google_indexing, x_auto_post_buffer as xb
ENV_FILE = Path(os.environ.get("SIXTONES_ENV_FILE") or ROOT / ".env")
_orig = xb.load_env
def load_env(_path):
    env = _orig(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in _orig(ENV_FILE).items() if v and not k.startswith("GOOGLE_INDEXING")}); return env  # ドライブ.envのIndexing鍵パスはWindows用なのでローカルを優先
xb.load_env = google_indexing.load_env = load_env
env = load_env(None)
U = env["WP_AUDITION_URL"].rstrip("/"); A = (env["WP_AUDITION_USERNAME"], env["WP_AUDITION_APP_PASSWORD"])
POSTS = [
    (1436, "SixTONESの愛用香水まとめたら、個性出すぎて優勝🏆✨\n樹くんはまさかのハイブランド、ジェシーは甘めの香り…？\n推しと同じ香りまとうの、致死量すぎて無理😭💕", "#SixTONES #スト担 #田中樹", True),
    (1440, "北斗くん、ずっと相棒にしてる水筒があるって知ってた？👀\nマットな黒のボトル、実はアメリカ生まれのブランドなんだって…\nセンス良すぎて沼確定🫠🖤", "#SixTONES #松村北斗", False),
]
if "--check" in sys.argv:
    for pid, t, h, _ in POSTS: print(pid, xb.weighted_length(t + "\n" + h))
    sys.exit()
for i, (pid, text, tags, use_imgs) in enumerate(POSTS):
    if i: time.sleep(180)
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", json={"status": "publish"}, auth=A, timeout=60).json()
    link = r.get("link"); print("PUBLISH", pid, r.get("status"), r.get("title", {}).get("rendered"), link, flush=True)
    try: print("INDEX", google_indexing.notify(link), flush=True)
    except Exception as e: print("INDEX FAIL", e, flush=True)
    try:
        imgs = xb.fetch_article_images(U, pid) if use_imgs else []
        print("X RESULT", time.strftime("%H:%M:%S"), len(imgs), "imgs", xb.post_thread(text, tags, imgs, link), flush=True)
    except Exception as e: print("X FAIL", e, flush=True)
print("DONE", flush=True)
