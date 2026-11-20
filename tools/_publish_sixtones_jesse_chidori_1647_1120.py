# 2026-11-20 SixTONES(chomoand-0.com)ID1647(トーキング千鳥 ジェシーのネックレス・腕時計)をユカ依頼で公開→YouTube埋め込み修正→Indexing→X/Threads
# ローカル.envにWP_AUDITION_*/BUFFER_*が無いため、Googleドライブの.envで補う(ローカルへはコピーしない)
# GOOGLE_INDEXING*はドライブ側がWindowsパスなので取らない
import os, sys, time, subprocess, requests
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVE = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env")
for p in (os.path.join(ROOT, ".env"), DRIVE):
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if l and not l.startswith("#") and "=" in l:
            k, v = l.split("=", 1); k = k.strip()
            if p == DRIVE and k.startswith("GOOGLE_INDEXING"): continue
            if not os.environ.get(k): os.environ[k] = v.strip().strip("\"'")
U = os.environ["WP_AUDITION_URL"].rstrip("/"); A = (os.environ["WP_AUDITION_USERNAME"], os.environ["WP_AUDITION_APP_PASSWORD"])
PY = sys.executable
WRAP = ("import sys,json,pathlib;from urllib.parse import urlparse;sys.path.insert(0,'tools');import x_auto_post_buffer as m;o=m.load_env\n"
        "def le(p):\n e=o(p);d=o(pathlib.Path(%r))\n for k,v in d.items():\n  if k.startswith('BUFFER_') and not e.get(k): e[k]=v\n return e\n"
        "m.load_env=le;text,tags,pid,url=sys.argv[1:5];s=urlparse(url)\n"
        "imgs=m.fetch_article_images(f'{s.scheme}://{s.netloc}',int(pid));print('images:',len(imgs))\n"
        "print(json.dumps(m.post_thread(text,tags,imgs,url),ensure_ascii=False,indent=2))") % DRIVE
POSTS = [
 (1647, "トーキング千鳥のジェシーくん、手ふるたびに首元と手元がキラッキラで目が離せなかった😭✨\nゴールドのネックレス・ブレス・腕時計の3点盛り、破壊力えぐい…🔥\nブランドとお値段の目安、映像で見くらべたよ👀", "#SixTONES #ジェシー #トーキング千鳥"),
]
links = {}
for pid, _, _ in POSTS:
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", json={"status": "publish"}, auth=A, timeout=60).json()
    links[pid] = r.get("link"); print("PUBLISH", pid, r.get("status"), r.get("title", {}).get("rendered"), r.get("link"), flush=True)
print(subprocess.run([PY, os.path.join(ROOT, "tools", "fix_youtube_embeds.py"), "--site", "AUDITION", "--ids", *[str(p) for p, _, _ in POSTS]], cwd=ROOT, capture_output=True, text=True).stdout, flush=True)
for pid in links:
    subprocess.run([PY, os.path.join(ROOT, "tools", "google_indexing.py"), links[pid]], cwd=ROOT)
for i, (pid, text, tags) in enumerate(POSTS):
    if i: time.sleep(180)
    print("X", pid, time.strftime("%H:%M:%S"), flush=True)
    subprocess.run([PY, "-c", WRAP, text, tags, str(pid), links[pid]], cwd=ROOT)
print("DONE", flush=True)
