# -*- coding: utf-8 -*-
"""宮舘涼太 匂わせ説検証記事を chomoand.com(トレンド)へ下書き投稿. 本文は build_and_post_miyadate_niowase_kensho.py build の出力を流用."""
import base64
from pathlib import Path
import requests
from build_and_post_miyadate_niowase_kensho import ENV, HTML_PATH, title, slug

ROOT = Path(__file__).parent
EYE = ROOT / "images" / "miyadate_niowase_kensho_trend_eyecatch.png"
url = ENV["WP_TREND_URL"].rstrip("/")
h = {"Authorization": "Basic " + base64.b64encode(f"{ENV['WP_TREND_USERNAME']}:{ENV['WP_TREND_APP_PASSWORD']}".encode()).decode()}
r = requests.post(f"{url}/wp-json/wp/v2/media", headers={**h, "Content-Type": "image/png",
                  "Content-Disposition": f'attachment; filename="{EYE.name}"'}, data=EYE.read_bytes(), timeout=60)
r.raise_for_status(); mid = r.json()["id"]
payload = {"title": title, "slug": slug, "content": HTML_PATH.read_text(encoding="utf-8"), "status": "draft",
           "categories": [37], "author": 3, "featured_media": mid}  # 37=芸能・トレンド, 3=momo
r = requests.post(f"{url}/wp-json/wp/v2/posts", headers={**h, "Content-Type": "application/json"}, json=payload, timeout=60)
r.raise_for_status(); d = r.json()
print("POST_ID", d["id"], d["status"], "MEDIA", mid, f"{url}/?p={d['id']}")
