# -*- coding: utf-8 -*-
import base64, json, re
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


ENV = load_env(ROOT / ".env")

ARTICLES = [
    {
        "key": "acne_matsukura",
        "title": "松倉海斗がコストコで着てたTシャツはAcne Studiosと判明！",
        "slug": "the-t-shirt-that-kaito-matsuku",
    },
    {
        "key": "mm6_kawashima",
        "title": "川島如恵留がコストコで着てたTシャツはMM6と判明！",
        "slug": "kawashima-noeru-costco-mm6-tee",
    },
    {
        "key": "toraja_matome",
        "title": "トラジャがコストコで買ったものは？店はどこ？",
        "slug": "what-did-toraja-buy-at-costco",
    },
    {
        "key": "6crayon_miyachika",
        "title": "宮近海斗がコストコでかぶっていた帽子は6CRAYONと判明！",
        "slug": "the-hat-that-kaito-miyachika-w",
    },
    {
        "key": "carhartt_miyachika",
        "title": "宮近海斗がコストコで着てたTシャツはCarhartt WIPと判明！",
        "slug": "the-t-shirt-kaito-miyachika-wo",
    },
]

# per-article accent color (matches each article's own existing box palette)
COLORS = {
    "acne_matsukura": ("#f5d0a9", "#e8952e", "#fdf3e6"),
    "mm6_kawashima": ("#d9d9d9", "#7a7a7a", "#f4f4f4"),
    "toraja_matome": ("#7e57c2", "#7e57c2", "#f5f2fb"),
    "6crayon_miyachika": ("#f3d6d6", "#ef9a9a", "#fdf3f3"),
    "carhartt_miyachika": ("#f3d6d6", "#ef9a9a", "#fdf3f3"),
}

SITES = {
    "chomoand0": {
        "base_url": "https://chomoand-0.com",
        "env_prefix": "WP_AUDITION",
        "post_ids": {
            "acne_matsukura": 1085,
            "mm6_kawashima": 1090,
            "toraja_matome": 1073,
            "6crayon_miyachika": 1079,
            "carhartt_miyachika": 1072,
        },
    },
    "chomoand4": {
        "base_url": "https://chomoand-4.blog",
        "env_prefix": "WP_CHOMO4",
        "post_ids": {
            "acne_matsukura": 188,
            "mm6_kawashima": 198,
            "toraja_matome": 189,
            "6crayon_miyachika": 202,
            "carhartt_miyachika": 207,
        },
    },
}

TRAILING_BOX_RE = re.compile(
    r'<!-- wp:html -->\s*'
    r'<div style="border:1px solid #[0-9a-fA-F]{3,6};border-left:4px solid #[0-9a-fA-F]{3,6};'
    r'border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:#[0-9a-fA-F]{3,6};">\s*'
    r'<p style="font-weight:bold;font-size:1\.05em;margin:0 0 8px 0;">あわせて読みたい</p>.*?'
    r'</div>\s*<!-- /wp:html -->\s*$',
    re.DOTALL,
)


def build_box(border, accent, bg, links):
    lis = "\n".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in links)
    return (
        '<!-- wp:html -->\n'
        f'<div style="border:1px solid {border};border-left:4px solid {accent};'
        f'border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{bg};">\n'
        '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">コストコ関連記事</p>\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n'
        '</div>\n<!-- /wp:html -->'
    )


for site_key, site in SITES.items():
    url = site["base_url"]
    env_prefix = site["env_prefix"]
    wp_url = ENV[f"{env_prefix}_URL"].rstrip("/")
    user = ENV[f"{env_prefix}_USERNAME"]
    pw = ENV[f"{env_prefix}_APP_PASSWORD"]
    auth = base64.b64encode(f"{user}:{pw}".encode()).decode()
    headers_auth = {"Authorization": f"Basic {auth}"}

    for art in ARTICLES:
        key = art["key"]
        pid = site["post_ids"][key]
        border, accent, bg = COLORS[key]

        siblings = [a for a in ARTICLES if a["key"] != key]
        links = [(a["title"], f'{url}/{a["slug"]}') for a in siblings]

        r = requests.get(
            f"{wp_url}/wp-json/wp/v2/posts/{pid}",
            params={"context": "edit"},
            headers=headers_auth,
        )
        r.raise_for_status()
        post = r.json()
        content = post["content"]["raw"]
        status = post["status"]

        # strip an existing trailing "あわせて読みたい" box (our earlier imperfect attempts)
        content_stripped = TRAILING_BOX_RE.sub("", content).rstrip()

        new_box = build_box(border, accent, bg, links)
        new_content = content_stripped + "\n\n" + new_box

        payload = {"content": new_content, "status": status}
        ur = requests.post(
            f"{wp_url}/wp-json/wp/v2/posts/{pid}",
            headers={**headers_auth, "Content-Type": "application/json"},
            data=json.dumps(payload).encode("utf-8"),
        )
        ur.raise_for_status()
        updated = ur.json()
        print(site_key, pid, key, "-> status:", updated["status"], "content_len:", len(updated["content"]["raw"]))
