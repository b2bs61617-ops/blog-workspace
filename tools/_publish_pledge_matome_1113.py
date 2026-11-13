# 2026-11-13 chomoand-1.com ID15827(+KR15828/EN15829) KO1KEYZ debut pledge matome (12 members): publish -> Indexing/Naver -> X(JA+KR) (Yuka request)
import sys, subprocess
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, x_auto_post_buffer as xb
env = xb.load_env(ROOT / ".env")
U = env["WP_KOIKEYS_URL"].rstrip("/"); A = (env["WP_KOIKEYS_USERNAME"], env["WP_KOIKEYS_APP_PASSWORD"])
JA, KR, EN = 15827, 15828, 15829
JA_TEXT = "KO1KEYZ12人のデビュー公約、全部並べたら仲良しすぎて致死量なんだが…😭🫶\nサンタになる子に手紙書く子、食べ物系は3人もいて優勝🍰✨"
JA_TAGS = "#KO1KEYZ #コイキーズ #デビュー公約"
KR_TEXT = "코이키즈 12명 데뷔 공약 다 모아봤는데 사이 좋은 거 반칙이야…😭🫶\n산타 되는 멤버, 편지 쓰는 멤버, 음식 공약만 3명이라니 미쳤다🍰✨"
KR_TAGS = "#KO1KEYZ #코이키즈 #데뷔공약"
if "--check" in sys.argv:
    print(xb.weighted_length(JA_TEXT + "\n" + JA_TAGS), xb.weighted_length(KR_TEXT + "\n" + KR_TAGS)); sys.exit()
links = {}
for PID in (JA, KR, EN):
    title = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()["title"]["raw"].replace("【未】", "")
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"status": "publish", "title": title}, auth=A, timeout=60).json()
    links[PID] = r.get("link"); print("PUBLISH", PID, r.get("status"), r.get("title", {}).get("rendered"), r.get("link"), flush=True)
for PID, link in links.items():
    for tool in ("google_indexing.py", "naver_indexnow.py"):
        out = subprocess.run([sys.executable, str(ROOT / "tools" / tool), link], capture_output=True, text=True)
        print(tool, PID, " ".join(out.stdout.split())[:200], flush=True)
imgs = xb.fetch_article_images(U, JA)
try: print("X JA", len(imgs), "imgs", xb.post_thread(JA_TEXT, JA_TAGS, imgs, links[JA]), flush=True)
except Exception as e: print("X JA FAIL", e, flush=True)
try: print("X KR", len(imgs), "imgs", xb.post_thread(KR_TEXT, KR_TAGS, imgs, links[KR], threads=False), flush=True)
except Exception as e: print("X KR FAIL", e, flush=True)
