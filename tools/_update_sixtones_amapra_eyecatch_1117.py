# 2026-11-17 chomoand-0.com ID1556 (SixTONES Amazon Prime Video): eyecatch remake, top=Amazonプライムビデオ / main=SixTONES / 3rd=アマプラで見られる作品は？ / 4th=おすすめ5つを紹介！ (Yuka request)
import os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, x_auto_post_buffer as xb
ENV_FILE = Path(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))
env = xb.load_env(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in xb.load_env(ENV_FILE).items() if v and not k.startswith("GOOGLE_INDEXING")})
U = env["WP_AUDITION_URL"].rstrip("/"); A = (env["WP_AUDITION_USERNAME"], env["WP_AUDITION_APP_PASSWORD"])
PID = 1556
IMG = ROOT / "images/sixtones_amapra_1556_eyecatch_v2.jpg"
m = requests.post(f"{U}/wp-json/wp/v2/media", data=IMG.read_bytes(), auth=A, timeout=120,
                  headers={"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{IMG.name}"'}).json()
requests.post(f"{U}/wp-json/wp/v2/media/{m['id']}", json={"alt_text": "SixTONES Amazonプライムビデオ"}, auth=A, timeout=60)
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"featured_media": m["id"]}, auth=A, timeout=60).json()
print("media", m["id"], m["source_url"], "| post", r["id"], r["status"], "featured", r["featured_media"])
