# -*- coding: utf-8 -*-
import base64, os
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

r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/11083?context=edit", headers=HEADERS_AUTH)
r.raise_for_status()
post = r.json()
(ROOT / "tmp_keito_jp_content.html").write_text(post["content"]["raw"], encoding="utf-8")
(ROOT / "tmp_keito_jp_title.txt").write_text(post["title"]["raw"], encoding="utf-8")
print("saved. title:", post["title"]["raw"])
print("content chars:", len(post["content"]["raw"]))
