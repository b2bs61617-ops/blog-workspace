# -*- coding: utf-8 -*-
import base64, os, json
from pathlib import Path
import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
WP_USER = ENV["WP_KOIKEYS_USERNAME"]
WP_PASS = ENV["WP_KOIKEYS_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

eyecatch_path = ROOT / "images" / "keito_night_routine_eyecatch.png"
data = eyecatch_path.read_bytes()
headers = {
    **HEADERS_AUTH,
    "Content-Type": "image/png",
    "Content-Disposition": 'attachment; filename="keito_night_routine_eyecatch.png"',
}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=data)
r.raise_for_status()
media = r.json()
print("eyecatch media id:", media["id"])

POST_ID = 11083
r2 = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"status": "draft", "featured_media": media["id"]}).encode("utf-8"),
)
r2.raise_for_status()
print("updated post", POST_ID, "featured_media ->", media["id"])
