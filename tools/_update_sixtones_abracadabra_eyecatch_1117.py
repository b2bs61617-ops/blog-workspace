# 2026-11-17 chomoand-0.com ID1559 (SixTONES ABRACADABRA, draft): eyecatch remake, top=アブラカタブラ / main=SixTONES (Yuka request)
# v3 (same day, after publish): top=シングル「バリア」 / main=SixTONES / 3rd=ABRACADABRA / 4th=何に収録？曲の魅力も！ (Yuka request)
import os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, x_auto_post_buffer as xb
ENV_FILE = Path(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))
env = xb.load_env(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in xb.load_env(ENV_FILE).items() if v and not k.startswith("GOOGLE_INDEXING")})
U = env["WP_AUDITION_URL"].rstrip("/"); A = (env["WP_AUDITION_USERNAME"], env["WP_AUDITION_APP_PASSWORD"])
PID = 1559
IMG = ROOT / "images/sixtones_abracadabra_1559_eyecatch_v3.jpg"
m = requests.post(f"{U}/wp-json/wp/v2/media", data=IMG.read_bytes(), auth=A, timeout=120,
                  headers={"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{IMG.name}"'}).json()
requests.post(f"{U}/wp-json/wp/v2/media/{m['id']}", json={"alt_text": "SixTONES アブラカタブラ"}, auth=A, timeout=60)
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"featured_media": m["id"]}, auth=A, timeout=60).json()
print("media", m["id"], m["source_url"], "| post", r["id"], r["status"], "featured", r["featured_media"])
