# 2026-11-19 Snow Man(chomoand-2.com) ユカ依頼: 834(公開済み)はX/Threadsのみ、768・829を公開→YouTube埋め込み修正→Indexing→X/Threads(3分おき)
# ローカル.envにWP_CHOMO2_*/BUFFER_*が無いため、Googleドライブの.envで補う(ローカルへはコピーしない)
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
U = os.environ["WP_CHOMO2_URL"].rstrip("/"); A = (os.environ["WP_CHOMO2_USERNAME"], os.environ["WP_CHOMO2_APP_PASSWORD"])
PY = sys.executable
WRAP = ("import sys,json,pathlib;from urllib.parse import urlparse;sys.path.insert(0,'tools');import x_auto_post_buffer as m;o=m.load_env\n"
        "def le(p):\n e=o(p);d=o(pathlib.Path(%r))\n for k,v in d.items():\n  if k.startswith('BUFFER_') and not e.get(k): e[k]=v\n return e\n"
        "m.load_env=le;text,tags,pid,url=sys.argv[1:5];s=urlparse(url)\n"
        "imgs=m.fetch_article_images(f'{s.scheme}://{s.netloc}',int(pid));print('images:',len(imgs))\n"
        "print(json.dumps(m.post_thread(text,tags,imgs,url),ensure_ascii=False,indent=2))") % DRIVE
POSTS = [
 (834, "は？？Snow Manが載る雑誌、11月20日から5冊も出るの供給過多すぎる😭🔥\nめめの連載は8ページもあって、通販はもう売り切れ表示…！\n発売日と予約できるお店まとめたよ🫶✨", "#SnowMan #目黒蓮 #すの担"),
 (768, "速報🚨ラウールくん、FNS歌謡祭にまさかの名前で出演決定…！\n世界的DJとのコラボを生放送で見られるの心臓もたない🫠💕\n出演日と歌う曲の情報まとめたよ🫶", "#SnowMan #ラウール #FNS歌謡祭"),
 (829, "赤いリボンまとった舘様のanan、破壊力えぐい…🌹😭\n愛用中のスキンケア、限定キットは16,610円だって👀\nどこで買えるかもまとめたよ🫶✨", "#SnowMan #宮舘涼太 #anan"),
]
TO_PUBLISH = [768, 829]
links = {}
for pid, _, _ in POSTS:
    if pid in TO_PUBLISH:
        cur = requests.get(f"{U}/wp-json/wp/v2/posts/{pid}?context=edit", auth=A, timeout=60).json()
        title = cur["title"]["raw"].replace("【未】", "").strip().lstrip("\u3000").strip()
        r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", json={"status": "publish", "title": title}, auth=A, timeout=60).json()
    else:
        r = requests.get(f"{U}/wp-json/wp/v2/posts/{pid}", auth=A, timeout=60).json()
    links[pid] = r.get("link"); print("POST", pid, r.get("status"), r.get("title", {}).get("rendered"), r.get("link"), flush=True)
print(subprocess.run([PY, os.path.join(ROOT, "tools", "fix_youtube_embeds.py"), "--site", "CHOMO2", "--ids", *[str(p) for p in TO_PUBLISH]], cwd=ROOT, capture_output=True, text=True).stdout, flush=True)
for pid in TO_PUBLISH:
    subprocess.run([PY, os.path.join(ROOT, "tools", "google_indexing.py"), links[pid]], cwd=ROOT)
for i, (pid, text, tags) in enumerate(POSTS):
    if i: time.sleep(180)
    print("X", pid, time.strftime("%H:%M:%S"), flush=True)
    subprocess.run([PY, "-c", WRAP, text, tags, str(pid), links[pid]], cwd=ROOT)
print("DONE", flush=True)
