# -*- coding: utf-8 -*-
"""ピアス記事の「12人まとめ」セクション冒頭に、KO1KEYZデビューシングルの
公式ジャケット写真(12人集合)を挿入。出典はモデルプレスの投稿。JP/KR/EN。"""
import base64, json, os
from pathlib import Path

import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f'{ENV["WP_KOIKEYS_USERNAME"]}:{ENV["WP_KOIKEYS_APP_PASSWORD"]}'.encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}

SRC = "https://x.com/modelpress/status/2080134203212210249"


def upload(path, filename, alt):
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**H, "Content-Type": "image/jpeg",
                 "Content-Disposition": f'attachment; filename="{filename}"'},
        data=Path(path).read_bytes(),
    )
    r.raise_for_status()
    m = r.json()
    requests.post(f"{WP_URL}/wp-json/wp/v2/media/{m['id']}",
                  headers={**H, "Content-Type": "application/json"},
                  data=json.dumps({"alt_text": alt}).encode()).raise_for_status()
    return m


gm = upload(ROOT / "images" / "ko1keyz_piercing_group_jacket.jpg",
            "ko1keyz_piercing_group_jacket.jpg",
            "KO1KEYZ 12人が集合したデビューシングルのジャケット写真")
print("group media", gm["id"])


def fig(media, alt, label, xlabel, src):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    fw = media["media_details"]["width"]; fh = media["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": fw})
    medium = sizes.get("medium", {"source_url": full_url, "width": fw})
    iw = large["width"]; ih = int(iw * fh / fw)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {fw}w'
    return (
        "\n\n<!-- wp:html -->\n"
        '<figure class="wp-block-image size-large">\n'
        f'<img src="{large["source_url"]}" alt="{alt}" width="{iw}" height="{ih}"\n'
        '  style="max-width:100%;height:auto;"\n'
        f'  srcset="{srcset}"\n'
        f'  sizes="(max-width: {iw}px) 100vw, {iw}px">\n'
        f'<figcaption style="text-align:center;font-size:12px;">{label}<a href="{src}" target="_blank" rel="noopener">{xlabel}</a></figcaption>\n'
        "</figure>\n"
        "<!-- /wp:html -->"
    )


LANG = {
 12030: dict(anchor="12人のピアスの数は次のように整理できます。</p>\n<!-- /wp:paragraph -->",
             alt="電話ボックスの前に並ぶKO1KEYZ12人のデビューシングルのジャケット写真",
             label="出典:", xlabel="X(旧Twitter)"),
 12034: dict(anchor="12명의 피어싱 개수는 다음과 같이 정리할 수 있어요.</p>\n<!-- /wp:paragraph -->",
             alt="KO1KEYZ 12명이 모인 데뷔 싱글 재킷 사진",
             label="출처:", xlabel="X(옛 트위터)"),
 12038: dict(anchor="the counts break down like this.</p>\n<!-- /wp:paragraph -->",
             alt="Jacket photo of all 12 KO1KEYZ members together for the debut single",
             label="Source: ", xlabel="X (Twitter)"),
}

for pid, cfg in LANG.items():
    j = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=H, params={"context": "edit"}).json()
    raw = j["content"]["raw"]
    if raw.count(cfg["anchor"]) != 1:
        raise SystemExit(f"[{pid}] anchor not unique ({raw.count(cfg['anchor'])})")
    raw = raw.replace(cfg["anchor"], cfg["anchor"] + fig(gm, cfg["alt"], cfg["label"], cfg["xlabel"], SRC))
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}",
                      headers={**H, "Content-Type": "application/json"},
                      data=json.dumps({"content": raw, "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    print(f"[{pid}] group photo inserted OK")
