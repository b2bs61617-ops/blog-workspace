# 2026-11-17 chomoand-0.com ID1548 (SixTONES goods seiriken / Nissan) add official photo -> publish -> YouTube embed fix -> Indexing -> X/Threads (Yuka request)
# Draft had 0 photos, so reuse the official @SixTONES_SME Nissan board photo (media 1579, already used in ID1238) right under the Nissan sales-time H2.
# WP_AUDITION_*/BUFFER_* come from the Google Drive .env; GOOGLE_INDEXING* stays local (Drive value is a Windows path)
import os, sys, subprocess
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, google_indexing, x_auto_post_buffer as xb
ENV_FILE = Path(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))
_orig = xb.load_env
def load_env(_path):
    env = _orig(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in _orig(ENV_FILE).items() if v and not k.startswith("GOOGLE_INDEXING")}); return env
xb.load_env = google_indexing.load_env = load_env
env = load_env(None)
U = env["WP_AUDITION_URL"].rstrip("/"); A = (env["WP_AUDITION_USERNAME"], env["WP_AUDITION_APP_PASSWORD"])
PID = 1548
TEXT = "日産のスト担さん、グッズ整理券の準備できてる？🚨\nチケ外れてても会場でグッズ買えるって知ってた？👀\n販売は2日間とも10時〜17時！取り方4ステップまとめたよ🫶"
TAGS = "#SixTONES #スト担 #MILESixTONES"
H2 = '<h2 class="wp-block-heading">日産スタジアムのグッズ販売日と時間</h2>\n<!-- /wp:heading -->'
FIG = '''

<!-- wp:image {"id":1579,"sizeSlug":"large"} -->
<figure class="wp-block-image size-large"><img src="https://chomoand-0.com/wp-content/uploads/2026/11/sixtones_nissan_1238_nagai_board_1116-500x375.jpg" alt="MILESixTONES長居公演の看板(右下に日産スタジアム11月21日・22日の文字)" class="wp-image-1579" width="500" height="375" style="max-width:100%;height:auto;" srcset="https://chomoand-0.com/wp-content/uploads/2026/11/sixtones_nissan_1238_nagai_board_1116-500x375.jpg 500w, https://chomoand-0.com/wp-content/uploads/2026/11/sixtones_nissan_1238_nagai_board_1116-768x576.jpg 768w, https://chomoand-0.com/wp-content/uploads/2026/11/sixtones_nissan_1238_nagai_board_1116.jpg 1440w" sizes="(max-width: 1024px) 100vw, 1024px"><figcaption style="font-size:0.8em;color:#888;">出典:https://x.com/SixTONES_SME/status/2119332762721378714</figcaption></figure>
<!-- /wp:image -->'''

p = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()
content, title = p["content"]["raw"], p["title"]["raw"].replace("【未】", "")
if "wp-image-1579" not in content:
    assert content.count(H2) == 1, "insert point not found"
    content = content.replace(H2, H2 + FIG)
wp_env = {**os.environ, **{k: v for k, v in env.items() if k.startswith("WP_AUDITION_")}}
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"content": content, "status": "publish", "title": title}, auth=A, timeout=60).json()
link = r.get("link"); print("PUBLISH", PID, r.get("status"), r.get("title", {}).get("rendered"), link, flush=True)
print(subprocess.run([sys.executable, str(ROOT / "tools/fix_youtube_embeds.py"), "--site", "AUDITION", "--ids", str(PID)], env=wp_env, capture_output=True, text=True).stdout, flush=True)
try: print("INDEX", google_indexing.notify(link), flush=True)
except Exception as e: print("INDEX FAIL", e, flush=True)
try:
    imgs = xb.fetch_article_images(U, PID)
    print("X RESULT", len(imgs), "imgs", xb.post_thread(TEXT, TAGS, imgs, link), flush=True)
except Exception as e: print("X FAIL", e, flush=True)
