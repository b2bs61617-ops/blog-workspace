# 2026-11-17 chomoand-0.com ID1545 (SixTONES jump rope test, draft): eyecatch remake, top=縄跳び検定に挑戦 / 3rd=検定結果は何級？ (Yuka request)
import os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, x_auto_post_buffer as xb
ENV_FILE = Path(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))
env = xb.load_env(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in xb.load_env(ENV_FILE).items() if v and not k.startswith("GOOGLE_INDEXING")})
U = env["WP_AUDITION_URL"].rstrip("/"); A = (env["WP_AUDITION_USERNAME"], env["WP_AUDITION_APP_PASSWORD"])
PID = 1545
IMG = ROOT / "images/sixtones_nawatobi_1545_eyecatch_v2.jpg"
m = requests.post(f"{U}/wp-json/wp/v2/media", data=IMG.read_bytes(), auth=A, timeout=120,
                  headers={"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{IMG.name}"'}).json()
requests.post(f"{U}/wp-json/wp/v2/media/{m['id']}", json={"alt_text": "SixTONES 縄跳び検定"}, auth=A, timeout=60)
r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"featured_media": m["id"]}, auth=A, timeout=60).json()
print("media", m["id"], m["source_url"], "| post", r["id"], r["status"], "featured", r["featured_media"])
