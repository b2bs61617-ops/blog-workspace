# 2026-11-20 Snow Man(chomoand-2.com) ユカ依頼: ID866(ALL SUITE双眼鏡)を公開→YouTube埋め込み修正→Indexing→X/Threadsは11/21 12:00にBuffer予約
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
        "m.load_env=le;text,tags,pid,url,due=sys.argv[1:6];s=urlparse(url)\n"
        "imgs=m.fetch_article_images(f'{s.scheme}://{s.netloc}',int(pid));print('images:',len(imgs))\n"
        "print(json.dumps(m.post_thread(text,tags,imgs,url,due_at=due),ensure_ascii=False,indent=2))") % DRIVE
DUE = "2026-11-21T12:00:00+09:00"
POSTS = [
 (866, "Snow Manのドーム、天井席だと8倍じゃ全然足りないって知ってた…？😭\nALL SUITEは来週から名古屋→福岡→東京→大阪🏨✨\n会場ごと・席ごとに双眼鏡は何倍がいいかまとめたよ🫶", "#SnowMan #ALLSUITE #すの担"),
]
TO_PUBLISH = [866]
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
    print("X", pid, time.strftime("%H:%M:%S"), flush=True)
    subprocess.run([PY, "-c", WRAP, text, tags, str(pid), links[pid], DUE], cwd=ROOT)
print("DONE", flush=True)
