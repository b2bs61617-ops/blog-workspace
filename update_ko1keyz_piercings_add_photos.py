# -*- coding: utf-8 -*-
"""ピアス記事に、メンバーのピアス姿がわかる写真(KOSUKE=星ピアス、RYUJI=複数フープ+イヤーカフ)を挿入。
どちらもデビューシングルのアー写(静止画)で、被写体が明確に確認できるもののみ採用。
TOWA/DAIKI/YUKIはMVフレーム・AIファンアート・被写体不明瞭のため今回は見送り。"""
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

KOSUKE_SRC = "https://x.com/sirosarah_/status/2081327240084902227"
RYUJI_SRC = "https://x.com/twoberry77/status/2080444452095889813"


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


kosuke_m = upload(ROOT / "images" / "ko1keyz_piercing_kosuke_star.jpg",
                  "ko1keyz_piercing_kosuke_star.jpg", "耳たぶのシルバーフープと星モチーフのピアスを着けたKOSUKE")
ryuji_m = upload(ROOT / "images" / "ko1keyz_piercing_ryuji_hoops.jpg",
                 "ko1keyz_piercing_ryuji_hoops.jpg", "両耳に複数のシルバーピアスとイヤーカフを着けたRYUJI")
print("kosuke media", kosuke_m["id"], " ryuji media", ryuji_m["id"])


def fig(media, alt, caption_label, src):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    fw = media["media_details"]["width"]
    fh = media["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": fw})
    medium = sizes.get("medium", {"source_url": full_url, "width": fw})
    iw = large["width"]
    ih = int(iw * fh / fw)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {fw}w'
    return (
        "<!-- wp:html -->\n"
        '<figure class="wp-block-image size-large">\n'
        f'<img src="{large["source_url"]}" alt="{alt}" width="{iw}" height="{ih}"\n'
        '  style="max-width:100%;height:auto;"\n'
        f'  srcset="{srcset}"\n'
        f'  sizes="(max-width: {iw}px) 100vw, {iw}px">\n'
        f'<figcaption style="text-align:center;font-size:12px;">{caption_label}<a href="{src}" target="_blank" rel="noopener">X(旧Twitter)</a></figcaption>\n'
        "</figure>\n"
        "<!-- /wp:html -->"
    )


# 各言語: (KOSUKE box末尾のアンカー, RYUJI box末尾のアンカー, figcaptionラベル, X表記)
LANG = {
 12030: dict(
   k_anchor="この星ピアスはトレードマークとして定着しつつあります。</p>\n</div>\n<!-- /wp:html -->",
   r_anchor="耳元の変化はこまめにあります。</p>\n</div>\n<!-- /wp:html -->",
   k_alt="耳たぶのシルバーフープの上に星モチーフのピアスを着けたKOSUKE",
   r_alt="両耳に複数のシルバーピアスとイヤーカフを着けたRYUJI",
   label="出典:", xlabel="X(旧Twitter)"),
 12034: dict(
   k_anchor="이 별 피어싱은 트레이드마크로 자리잡아가고 있어요.</p>\n</div>\n<!-- /wp:html -->",
   r_anchor="귀 부분의 변화가 잦은 편이에요.</p>\n</div>\n<!-- /wp:html -->",
   k_alt="귓불의 실버 후프 위에 별 모티브 피어싱을 착용한 KOSUKE",
   r_alt="양쪽 귀에 여러 개의 실버 피어싱과 이어 커프를 착용한 RYUJI",
   label="출처:", xlabel="X(옛 트위터)"),
 12038: dict(
   k_anchor="so the star piercing is turning into a trademark.</p>\n</div>\n<!-- /wp:html -->",
   r_anchor="so his ears are rarely the same twice.</p>\n</div>\n<!-- /wp:html -->",
   k_alt="KOSUKE wearing a star-shaped stud above a silver hoop on his earlobe",
   r_alt="RYUJI wearing several silver earrings and an ear cuff across both ears",
   label="Source: ", xlabel="X (Twitter)"),
}


def fig2(media, alt, label, xlabel, src):
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


for pid, cfg in LANG.items():
    j = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=H, params={"context": "edit"}).json()
    raw = j["content"]["raw"]
    for anchor, media, alt in [
        (cfg["k_anchor"], kosuke_m, cfg["k_alt"]),
        (cfg["r_anchor"], ryuji_m, cfg["r_alt"]),
    ]:
        if raw.count(anchor) != 1:
            raise SystemExit(f"[{pid}] anchor not unique ({raw.count(anchor)}):\n{anchor[:100]}")
        src = KOSUKE_SRC if media is kosuke_m else RYUJI_SRC
        raw = raw.replace(anchor, anchor + fig2(media, alt, cfg["label"], cfg["xlabel"], src))
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}",
                      headers={**H, "Content-Type": "application/json"},
                      data=json.dumps({"content": raw, "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    print(f"[{pid}] photos inserted OK")
