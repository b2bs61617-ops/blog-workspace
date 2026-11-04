# 2026-11-04 キテレツ下書き4本(井上瑞稀誕生日インライの私服)を公開→Indexing、X/Threadsは3分おきに即時投稿
# このMacの.envにはWP_CHOMO5_*/BUFFER_*が無いので、Googleドライブの.envを読ませる
import os, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, google_indexing, x_auto_post_buffer as xb
ENV_FILE = Path(os.environ.get("KITETSU_ENV_FILE") or ROOT / ".env")
_orig = xb.load_env
def load_env(_path):
    env = _orig(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in _orig(ENV_FILE).items() if v}); return env
xb.load_env = google_indexing.load_env = load_env
env = load_env(None)
U = env["WP_CHOMO5_URL"].rstrip("/"); A = (env["WP_CHOMO5_USERNAME"], env["WP_CHOMO5_APP_PASSWORD"])
POSTS = [  # X投稿順(同じメンバーは間を空ける)
    (541, "瑞稀くんの誕生日インライ、主役たすきの下からのぞく赤いハート…🥺❤️\n黒タートルのニット、お値段5万円超えで破壊力えぐい😭🔥", "#KEYTOLIT #井上瑞稀"),
    (547, "は？？ガリさんのロイヤルブルーのスウェット、まさかのアメフトチームのものだった🏈💙\nしかも古着で数千円〜って…センス天才か？😭✨", "#KEYTOLIT #猪狩蒼弥"),
    (544, "瑞稀くんの誕生日インライ、ほぼ映ってない足元まで特定しちゃった👀\n茶色のふわふわショート丈、冬の定番すぎて真似したい人続出の予感🫶", "#KEYTOLIT #井上瑞稀"),
    (551, "嶺亜くんの悪魔ツノ×スカジャン、反則すぎて心臓爆発😈💥\nヤシの木刺しゅうのあのスカジャン、お値段まさかの30万円前後…！Snow Manのあの人も着てた😳", "#KEYTOLIT #中村嶺亜"),
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
        res = xb.post_thread(text, tags, imgs, links[pid])
        print("X RESULT", pid, len(imgs), "imgs", res, flush=True)
    except Exception as e: print("X FAIL", pid, e, flush=True)
print("DONE", flush=True)
