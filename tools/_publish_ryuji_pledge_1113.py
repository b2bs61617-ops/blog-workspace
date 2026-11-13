# 2026-11-13 chomoand-1.com ID15806(+KR15807/EN15808) KO1KEYZ debut pledge RYUJI portraits: publish -> Indexing/Naver -> X(JA+KR) (Yuka request)
import sys, subprocess
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, x_auto_post_buffer as xb
env = xb.load_env(ROOT / ".env")
U = env["WP_KOIKEYS_URL"].rstrip("/"); A = (env["WP_KOIKEYS_USERNAME"], env["WP_KOIKEYS_APP_PASSWORD"])
JA, KR, EN = 15806, 15807, 15808
JA_TEXT = "RYUJIくんがメンバー11人の似顔絵描いたら、点数が20点〜99点までバラバラすぎて情緒ぶっ壊れた😂🎨\n最後のサプライズで泣いた…😭💕"
JA_TAGS = "#KO1KEYZ #RYUJI #杉山竜司"
KR_TEXT = "류지가 멤버 11명 초상화 그렸는데 점수가 20점부터 99점까지 미쳤다😂🎨\n마지막 서프라이즈에 심장 터짐😭💕"
KR_TAGS = "#KO1KEYZ #코이키즈 #RYUJI #류지 #스기야마류지"
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
        print(tool, PID, (out.stdout + out.stderr).strip().splitlines()[-1:] , flush=True)
imgs = xb.fetch_article_images(U, JA)
try: print("X JA", len(imgs), "imgs", xb.post_thread(JA_TEXT, JA_TAGS, imgs, links[JA]), flush=True)
except Exception as e: print("X JA FAIL", e, flush=True)
try: print("X KR", len(imgs), "imgs", xb.post_thread(KR_TEXT, KR_TAGS, imgs, links[KR], threads=False), flush=True)
except Exception as e: print("X KR FAIL", e, flush=True)
