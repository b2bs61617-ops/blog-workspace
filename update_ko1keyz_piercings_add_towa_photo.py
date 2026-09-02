# -*- coding: utf-8 -*-
"""ピアス記事のTOWA枠の直後に、耳たぶ＋軟骨のピアスが見えるTOWAの写真を挿入。
KO1KEYZ「新世界」MVのワンシーン(りんごを額に乗せる=あっぷりんモチーフ)。
公式MVからの直接切り出しを試みたがこの環境ではDL不可(yt-dlp 403)のため、
当該シーンが鮮明に写ったX投稿の静止画を使用。JP/KR/EN。"""
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

SRC = "https://x.com/888_to_wa/status/2087105248896983068"


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


m = upload(ROOT / "images" / "ko1keyz_piercing_towa_helix.jpg",
           "ko1keyz_piercing_towa_helix.jpg",
           "額にりんごを乗せ、耳たぶと軟骨にピアスを着けたTOWA")
print("towa media", m["id"])


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
 12030: dict(anchor="シルバーで統一するのがTOWA流のスタイルになっています。</p>\n</div>\n<!-- /wp:html -->",
             alt="額にりんごを乗せ、耳たぶと軟骨にピアスを着けたTOWA",
             label="出典:", xlabel="X(旧Twitter)"),
 12034: dict(anchor="것이 TOWA의 스타일로 자리잡았어요.</p>\n</div>\n<!-- /wp:html -->",
             alt="이마에 사과를 올리고 귓불과 연골에 피어싱을 착용한 TOWA",
             label="출처:", xlabel="X(옛 트위터)"),
 12038: dict(anchor="a look that has become his signature.</p>\n</div>\n<!-- /wp:html -->",
             alt="TOWA balancing an apple on his forehead, with lobe and cartilage piercings visible",
             label="Source: ", xlabel="X (Twitter)"),
}

for pid, cfg in LANG.items():
    j = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=H, params={"context": "edit"}).json()
    raw = j["content"]["raw"]
    if raw.count(cfg["anchor"]) != 1:
        raise SystemExit(f"[{pid}] anchor not unique ({raw.count(cfg['anchor'])}):\n{cfg['anchor'][:120]}")
    raw = raw.replace(cfg["anchor"], cfg["anchor"] + fig(m, cfg["alt"], cfg["label"], cfg["xlabel"], SRC))
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}",
                      headers={**H, "Content-Type": "application/json"},
                      data=json.dumps({"content": raw, "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    print(f"[{pid}] TOWA photo inserted OK")
