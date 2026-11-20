# 2026-11-21 KO1KEYZ(chomoand-1.com) ユカ依頼: ID16398(EP.5ケミメモリー)+KR16404/EN16405を公開→Indexing/Naver→X(日・韓)/Threads(日)は11/21 9:00にBuffer予約
# 公開前チェック済み: check_ko1keyz_title OK / sync_ko1keyz_eyecatch でKR・EN揃え / fix_youtube_embeds 直す所なし
import os, sys, subprocess, requests
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for l in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); k = k.strip()
        if not os.environ.get(k): os.environ[k] = v.strip().strip("\"'")
U = os.environ["WP_KOIKEYS_URL"].rstrip("/"); A = (os.environ["WP_KOIKEYS_USERNAME"], os.environ["WP_KOIKEYS_APP_PASSWORD"])
PY = sys.executable
JP, KR, EN = 16398, 16404, 16405
DUE_JP = "2026-11-21T09:00:00+09:00"; DUE_KR = "2026-11-21T09:03:00+09:00"
links = {}
for pid in (JP, KR, EN):
    cur = requests.get(f"{U}/wp-json/wp/v2/posts/{pid}?context=edit", auth=A, timeout=60).json()
    title = cur["title"]["raw"].replace("【未】", "").strip().lstrip("　").strip()
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", json={"status": "publish", "title": title}, auth=A, timeout=60).json()
    links[pid] = r.get("link"); print("POST", pid, r.get("status"), title, r.get("link"), flush=True)
for pid in (JP, KR, EN):
    subprocess.run([PY, os.path.join(ROOT, "tools", "google_indexing.py"), links[pid]], cwd=ROOT)
    subprocess.run([PY, os.path.join(ROOT, "tools", "naver_indexnow.py"), links[pid]], cwd=ROOT)
JP_TEXT = "は？？KO1KEYZの韓国合宿の裏話、供給過多すぎる😭🍉\n大きな包丁でスイカ切ってくれたメンバーに、深夜のリビングがゲーセン化、生乾きのにおい事件まで…\n12人のケミメモリー全部まとめたよ🫶"
KR_TEXT = "KO1KEYZ 한국 합숙 비하인드 너무 많아서 미쳤다😭🍉\n큰 칼로 수박 잘라준 멤버, 새벽 거실 게임센터, 덜 마른 빨래 냄새 사건까지…\nEP.5 케미 메모리 12명 전부 정리했어🫶"
X = os.path.join(ROOT, "tools", "x_auto_post_buffer.py")
subprocess.run([PY, X, "--text", JP_TEXT, "--hashtags", "#KO1KEYZ #KO1KO1KO1KEYZ", "--post-id", str(JP), "--url", links[JP], "--due-at", DUE_JP], cwd=ROOT)
subprocess.run([PY, X, "--text", KR_TEXT, "--hashtags", "#KO1KEYZ #코이키즈", "--post-id", str(JP), "--url", links[KR], "--due-at", DUE_KR, "--no-threads"], cwd=ROOT)
print("DONE", flush=True)
