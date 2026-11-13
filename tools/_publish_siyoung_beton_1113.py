# 2026-11-13 chomoand-1.com ID15838(+KR15839/EN15840) KO1KEYZ SIYOUNG pracha paper bag bakery: publish -> Indexing/Naver -> X(JA+KR) (Yuka request)
import sys, subprocess
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, x_auto_post_buffer as xb
env = xb.load_env(ROOT / ".env")
U = env["WP_KOIKEYS_URL"].rstrip("/"); A = (env["WP_KOIKEYS_USERNAME"], env["WP_KOIKEYS_APP_PASSWORD"])
JA, KR, EN = 15838, 15839, 15840
JA_TEXT = "シヨンくんがプラチャで紙袋持って「じゃーん！」してくれたの可愛すぎて心臓爆発🫠🥐\n袋の正体、いつも行列のソウルの塩パン名店っぽい…食べたすぎる😭✨"
JA_TAGS = "#KO1KEYZ #SIYOUNG #パクシヨン"
KR_TEXT = "시영이 프챗에서 종이봉투 들고 짜잔 하는 거 너무 귀여워서 심장 터짐🫠🥐\n봉투 정체가 줄 서서 먹는 서울 소금빵 맛집 같대…진짜 먹고 싶다😭✨"
KR_TAGS = "#KO1KEYZ #코이키즈 #SIYOUNG #시영 #박시영"
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
