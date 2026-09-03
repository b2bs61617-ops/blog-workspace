# -*- coding: utf-8 -*-
"""Delete the (unwanted) SHINHAENG-dinner drafts and fold the real worn photo
into the TOWA CELINE outfit article (JP 12125 / KR 12127 / EN 12128)."""
import base64, json, os
from pathlib import Path

import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}
HJ = {**H, "Content-Type": "application/json"}

SHOT_MEDIA_ID = 12174  # TOWA+SHINHAENG two-shot, already uploaded
SOURCE_TWEET = "https://x.com/girlyoshiki/status/2095169972456525922"

# ---------------------------------------------------------------- delete unwanted
for pid in (12178, 12181, 12182):
    r = requests.delete(f"{WP}/wp-json/wp/v2/posts/{pid}?force=true", headers=H)
    print("deleted post", pid, r.status_code)
for mid in (12176, 12180):
    r = requests.delete(f"{WP}/wp-json/wp/v2/media/{mid}?force=true", headers=H)
    print("deleted media", mid, r.status_code)

# ---------------------------------------------------------------- build worn img
shot = requests.get(f"{WP}/wp-json/wp/v2/media/{SHOT_MEDIA_ID}", headers=H).json()


def img_html(media, alt, caption):
    sizes = media.get("media_details", {}).get("sizes", {})
    fu = media["source_url"]; fw = media["media_details"]["width"]; fh = media["media_details"]["height"]
    lg = sizes.get("large", {"source_url": fu, "width": fw})
    md = sizes.get("medium", {"source_url": fu, "width": fw})
    w = lg["width"]; h = int(w * fh / fw)
    srcset = f'{md["source_url"]} {md["width"]}w, {lg["source_url"]} {lg["width"]}w, {fu} {fw}w'
    return (f'<!-- wp:html -->\n<figure class="wp-block-image size-large">\n'
            f'<img src="{lg["source_url"]}" alt="{alt}" width="{w}" height="{h}"\n'
            f'  style="max-width:100%;height:auto;"\n  srcset="{srcset}"\n'
            f'  sizes="(max-width: {w}px) 100vw, {w}px">\n'
            f'<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>\n'
            f'</figure>\n<!-- /wp:html -->')


CAP = {
    "ja": f'出典:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>',
    "ko": f'출처:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>',
    "en": f'Source:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>',
}
ALT = {
    "ja": "プライベートの食事で緑のCELINEキャップとタイダイTシャツを着たTOWA",
    "ko": "사적인 식사에서 그린 CELINE 캡과 타이다이 티셔츠를 입은 TOWA",
    "en": "TOWA wearing the green CELINE cap and tie-dye tee at a private meal",
}

EDITS = {
    12125: {
        "anchor": '<!-- wp:heading -->\n<h2 class="wp-block-heading">帽子は?CELINE',
        "insert": (
            "<!-- wp:paragraph -->\n"
            "<p>実際に着用している様子は、メンバーとのプライベートな食事の際に公開された写真でも確認できます。<br>\n"
            "グリーンのキャップと、渦を巻くタイダイのTシャツを合わせているのが見て取れます。</p>\n"
            "<!-- /wp:paragraph -->\n\n"
            "{IMG}\n\n"
        ),
        "old": (
            "<p>今回のコーデについて、本人や運営からの公式な発信はなく、私物と言い切れる情報は出ていません。<br>\n"
            "ただ、ステージ衣装ではない普段着の写真として広まっていることから、TOWAさん自身が私服として選んだ可能性が高いとみられます。<br>"
        ),
        "new": (
            "<p>今回のコーデについて、本人や運営からの公式な発信はなく、私物と言い切れる情報は出ていません。<br>\n"
            "ただ、ステージ衣装ではない普段着の写真として広まっており、メンバーとのプライベートな食事の場でも同じコーデで出かけている様子が公開されていることから、TOWAさん自身が私服として愛用しているアイテムとみて良さそうです。<br>"
        ),
    },
    12127: {
        "anchor": '<!-- wp:heading -->\n<h2 class="wp-block-heading">모자는? CELINE',
        "insert": (
            "<!-- wp:paragraph -->\n"
            "<p>실제로 착용한 모습은, 멤버와의 사적인 식사 때 공개된 사진에서도 확인할 수 있습니다.<br>\n"
            "그린 캡과 소용돌이치는 타이다이 티셔츠를 매치한 것을 알 수 있습니다.</p>\n"
            "<!-- /wp:paragraph -->\n\n"
            "{IMG}\n\n"
        ),
        "old": (
            "<p>이번 코디에 대해 본인이나 운영 측의 공식 언급은 없어, 사물이라고 단언할 수 있는 정보는 나오지 않았습니다.<br>\n"
            "다만 무대 의상이 아닌 평상복 사진으로 퍼지고 있어, TOWA 본인이 사복으로 고른 것일 가능성이 높다고 보입니다.<br>"
        ),
        "new": (
            "<p>이번 코디에 대해 본인이나 운영 측의 공식 언급은 없어, 사물이라고 단언할 수 있는 정보는 나오지 않았습니다.<br>\n"
            "다만 무대 의상이 아닌 평상복 사진으로 퍼지고 있고, 멤버와의 사적인 식사 자리에서도 같은 코디로 나온 모습이 공개돼 있어, TOWA 본인이 사복으로 애용하는 아이템으로 봐도 좋을 듯합니다.<br>"
        ),
    },
    12128: {
        "anchor": '<!-- wp:heading -->\n<h2 class="wp-block-heading">The cap: CELINE Triomphe Richelieu Cap</h2>',
        "insert": (
            "<!-- wp:paragraph -->\n"
            "<p>You can also see the outfit worn for real in a photo shared from a private meal with a member.<br>\n"
            "He pairs the green cap with the swirling tie-dye tee.</p>\n"
            "<!-- /wp:paragraph -->\n\n"
            "{IMG}\n\n"
        ),
        "old": (
            "<p>There's no official word from TOWA or the label about this outfit, so nothing confirms the pieces are his own.<br>\n"
            "That said, the photo is circulating as everyday wear rather than a stage look, so it's likely TOWA picked these out himself as street clothes.<br>"
        ),
        "new": (
            "<p>There's no official word from TOWA or the label about this outfit, so nothing confirms the pieces are his own.<br>\n"
            "Still, the photo circulates as everyday wear rather than a stage look, and the same outfit also turns up in a photo shared from a private meal with a member, so it's fair to read these as pieces TOWA genuinely favors off duty.<br>"
        ),
    },
}

LANG_BY_ID = {12125: "ja", 12127: "ko", 12128: "en"}

for pid, e in EDITS.items():
    lang = LANG_BY_ID[pid]
    cur = requests.get(f"{WP}/wp-json/wp/v2/posts/{pid}?context=edit", headers=H).json()
    content = cur["raw"] if "raw" in cur else cur["content"]["raw"]

    if ALT[lang] in content:
        print(pid, "already has worn photo, skipping")
        continue

    assert e["anchor"] in content, f"{pid}: anchor not found"
    assert e["old"] in content, f"{pid}: old paragraph not found"

    block = e["insert"].replace("{IMG}", img_html(shot, ALT[lang], CAP[lang]))
    content = content.replace(e["anchor"], block + e["anchor"], 1)
    content = content.replace(e["old"], e["new"], 1)

    r = requests.post(f"{WP}/wp-json/wp/v2/posts/{pid}", headers=HJ,
                      data=json.dumps({"content": content, "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    print("updated", pid, r.status_code, f"{WP}/wp-admin/post.php?post={pid}&action=edit")

print("DONE")
