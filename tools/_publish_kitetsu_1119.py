# 2026-11-19 キテレツ(chomoand-5.site) ユカ依頼: 887・867・879・893を公開→YouTube埋め込み修正→Indexing→X/Threads(3分おき)
# ローカル.envにWP_CHOMO5_*/BUFFER_*が無いため、Googleドライブの.envで補う(ローカルへはコピーしない)
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
U = os.environ["WP_CHOMO5_URL"].rstrip("/"); A = (os.environ["WP_CHOMO5_USERNAME"], os.environ["WP_CHOMO5_APP_PASSWORD"])
PY = sys.executable
WRAP = ("import sys,json,pathlib;from urllib.parse import urlparse;sys.path.insert(0,'tools');import x_auto_post_buffer as m;o=m.load_env\n"
        "def le(p):\n e=o(p);d=o(pathlib.Path(%r))\n for k,v in d.items():\n  if k.startswith('BUFFER_') and not e.get(k): e[k]=v\n return e\n"
        "m.load_env=le;text,tags,pid,url=sys.argv[1:5];s=urlparse(url)\n"
        "imgs=m.fetch_article_images(f'{s.scheme}://{s.netloc}',int(pid));print('images:',len(imgs))\n"
        "print(json.dumps(m.post_thread(text,tags,imgs,url),ensure_ascii=False,indent=2))") % DRIVE
POSTS = [
 (887, "キテレツの大光王ロケ地、まさかの仙台のあの名所だった…😭🏯\n伊達政宗ゆかりの場所で5人がわちゃわちゃしてるの尊すぎる🫶\n行き方と料金もまとめたよ✨", "#KEYTOLIT #佐々木大光 #キテレツ"),
 (867, "キテレツキテル第6回、淳太くんにジビエ3品でおもてなし🍖🔥\n大昇くんシェフのワイルドシェフ判定、結果どうなったと思う？👀\nTVerだけの未公開シーンも反則級😭", "#KEYTOLIT #岩﨑大昇 #中間淳太 #キテレツキテル"),
 (879, "キテレツの大光王、ついに開催されたー！！😭👑\n優勝者のスコア15万点超えってどういうこと？？情緒ぶっ壊れた🫠\nクイズの問題と正解もまとめたよ🫶", "#KEYTOLIT #佐々木大光 #キテレツ"),
 (893, "デビュー前のキテレツ表紙ラッシュ、供給過多すぎる📚🔥\n11/20と24は1日に3冊ずつ出るってお財布もたない😭\n発売日順に予約方法までまとめたよ🫶", "#KEYTOLIT #キテレツ"),
]
TO_PUBLISH = [887, 867, 879, 893]
links = {}
for pid, _, _ in POSTS:
    if pid in TO_PUBLISH:
        cur = requests.get(f"{U}/wp-json/wp/v2/posts/{pid}?context=edit", auth=A, timeout=60).json()
        title = cur["title"]["raw"].replace("【未】", "").strip().lstrip("\u3000").strip()
        r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", json={"status": "publish", "title": title}, auth=A, timeout=60).json()
    else:
        r = requests.get(f"{U}/wp-json/wp/v2/posts/{pid}", auth=A, timeout=60).json()
    links[pid] = r.get("link"); print("POST", pid, r.get("status"), r.get("title", {}).get("rendered"), r.get("link"), flush=True)
print(subprocess.run([PY, os.path.join(ROOT, "tools", "fix_youtube_embeds.py"), "--site", "CHOMO5", "--ids", *[str(p) for p in TO_PUBLISH]], cwd=ROOT, capture_output=True, text=True).stdout, flush=True)
for pid in TO_PUBLISH:
    subprocess.run([PY, os.path.join(ROOT, "tools", "google_indexing.py"), links[pid]], cwd=ROOT)
for i, (pid, text, tags) in enumerate(POSTS):
    if i: time.sleep(180)
    print("X", pid, time.strftime("%H:%M:%S"), flush=True)
    subprocess.run([PY, "-c", WRAP, text, tags, str(pid), links[pid]], cwd=ROOT)
print("DONE", flush=True)
