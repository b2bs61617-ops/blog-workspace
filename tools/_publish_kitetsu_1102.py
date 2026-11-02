# 2026-11-02 キテレツ下書き2本を公開→Indexing、トラジャのX投稿が終わってから3分おきにX/Threads即時投稿
import os, sys, time, subprocess, requests
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for l in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip("\"'"))
U = os.environ["WP_CHOMO5_URL"].rstrip("/"); A = (os.environ["WP_CHOMO5_USERNAME"], os.environ["WP_CHOMO5_APP_PASSWORD"])
PY = sys.executable
TORAHJA_LOG = os.path.join(ROOT, "logs", "publish_1102.log")
POSTS = [
    (536, "今週のキテレツ、5人そろう番組で嶺亜くんの胸キュンデート術が見られるの無理すぎ😭💕\n週末は歌番組での歌唱もあるよ…！録画予約はお早めに📺✨", "#KEYTOLIT #キテレツ"),
    (528, "キテレツでいちばん早く入所したのは誰？😳\n最初の2人は同じオーディション、最後の2人も同じ日の入所…エモすぎて泣く😭💕", "#KEYTOLIT #キテレツ"),
]
links = {}
for pid, _, _ in POSTS:
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", json={"status": "publish"}, auth=A, timeout=60).json()
    links[pid] = r.get("link"); print("PUBLISH", pid, r.get("status"), r.get("link"), flush=True)
    subprocess.run([PY, os.path.join(ROOT, "tools", "google_indexing.py"), r.get("link")], cwd=ROOT)
while "DONE" not in open(TORAHJA_LOG, encoding="utf-8", errors="ignore").read():
    time.sleep(10)
for pid, text, tags in POSTS:
    time.sleep(180)
    print("X", pid, time.strftime("%H:%M:%S"), flush=True)
    subprocess.run([PY, os.path.join(ROOT, "tools", "x_auto_post_buffer.py"), "--text", text, "--hashtags", tags,
                    "--post-id", str(pid), "--url", links[pid]], cwd=ROOT)
print("DONE", flush=True)
