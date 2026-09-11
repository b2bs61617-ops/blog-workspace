# -*- coding: utf-8 -*-
"""JP-only uploader for the two KO1KEYZ utawari (song part-distribution) articles."""
import re, json, base64, urllib.request, sys

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip().strip('"')

U = env["WP_KOIKEYS_USERNAME"]; P = env["WP_KOIKEYS_APP_PASSWORD"]; BASE = env["WP_KOIKEYS_URL"]
AUTH = base64.b64encode(f"{U}:{P}".encode()).decode()


def api(path, body=None, method="GET"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Authorization", "Basic " + AUTH)
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload_media(path, filename):
    img = open(path, "rb").read()
    req = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=img, method="POST")
    req.add_header("Authorization", "Basic " + AUTH)
    req.add_header("Content-Type", "image/png")
    req.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    with urllib.request.urlopen(req) as r:
        return json.load(r)["id"]


def convert(md_text):
    """STEP1/1.5: strip H1, treat rest as already wp:-block-tagged HTML (our .md files
    already contain full wp:heading/wp:paragraph/wp:html/wp:table blocks), just strip
    any leftover <hr> and blank the H1 line."""
    lines = [l for l in md_text.split("\n") if not l.startswith("# ")]
    html = "\n".join(lines).strip()
    html = re.sub(r"<hr\s*/?>", "", html)
    return html


ARTICLES = [
    {
        "key": "run_again",
        "md": r"\articles\ko1keyz_run_again_utawari.md",
        "title": "KO1KEYZ「Run Again」の歌割りは？全12人のパート！",
        "slug": "ko1keyz-run-again-utawari",
        "eyecatch": r"\images\ko1keyz_run_again_utawari_eyecatch.png",
        "sns": ("KO1KEYZが1ST FAN MEETINGのアンコールで披露した「Run Again -KO1KEYZ ver.-」。"
                "日プ新世界ファイナルの曲を12人でどう歌い分けているのか、ファンの聞き取りをもとにした歌割り(パート分け)を、"
                "絵文字をローマ字の名前に変換して一覧にまとめました。"),
    },
    {
        "key": "black_angel",
        "md": r"\articles\ko1keyz_black_angel_utawari.md",
        "title": "KO1KEYZ「BLACK ANGEL」の歌割りは？6人パート！",
        "slug": "ko1keyz-black-angel-utawari",
        "eyecatch": r"\images\ko1keyz_black_angel_utawari_eyecatch.png",
        "sns": ("KO1KEYZが1ST FAN MEETINGで披露した「BLACK ANGEL -KO1KEYZ 6人ver.-」。"
                "日プ新世界のコンセプト評価で1位を獲得したダーク&セクシーな楽曲を、RYOGA・RYUJI・SHINHAENG・SIYOUNG・"
                "YUKI・YURAの6人がどう歌い分けているのか、歌割りを一覧にまとめました。"),
    },
]

results = {}
for a in ARTICLES:
    md = open(REPO + a["md"], encoding="utf-8").read()
    content = convert(md)
    post = api("/wp-json/wp/v2/posts", {
        "title": a["title"], "slug": a["slug"], "content": content, "status": "draft",
        "categories": [66, 62], "author": 2,
        "meta": {"jetpack_publicize_message": a["sns"]},
    }, "POST")
    pid = post["id"]
    media_id = upload_media(REPO + a["eyecatch"], a["key"] + "_eyecatch.png")
    api("/wp-json/wp/v2/posts/" + str(pid), {"featured_media": media_id, "status": "draft"}, "POST")
    results[a["key"]] = {"id": pid, "slug": a["slug"], "media_id": media_id, "link": post.get("link")}
    print(f"{a['key']}: id={pid} slug={a['slug']} media_id={media_id} preview={BASE}/?p={pid}")

print(json.dumps(results, ensure_ascii=False))
