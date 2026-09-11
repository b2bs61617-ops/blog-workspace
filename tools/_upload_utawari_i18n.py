# -*- coding: utf-8 -*-
"""Upload KR + EN drafts for the two KO1KEYZ utawari articles.
JP originals already live as drafts: run_again=12980 (media 12981), black_angel=12983 (media 12984)."""
import json, base64, urllib.request, re

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
        return json.loads(r.read().decode("utf-8"))


def upload_media(path, filename):
    img = open(path, "rb").read()
    req = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=img, method="POST")
    req.add_header("Authorization", "Basic " + AUTH)
    req.add_header("Content-Type", "image/png")
    req.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))["id"]


def load_content(md_path, table_path):
    text = open(md_path, encoding="utf-8").read()
    lines = [l for l in text.split("\n") if not l.startswith("# ")]
    content = "\n".join(lines).strip()
    content = re.sub(r"<hr\s*/?>", "", content)
    table = open(table_path, encoding="utf-8").read()
    assert "{{TABLE}}" in content, f"no {{{{TABLE}}}} placeholder in {md_path}"
    content = content.replace("{{TABLE}}", table)
    return content


RUN_AGAIN_JP_ID, RUN_AGAIN_JP_MEDIA = 12980, 12981
BLACK_ANGEL_JP_ID, BLACK_ANGEL_JP_MEDIA = 12983, 12984

JOBS = [
    dict(key="run_again_kr", lang="ko", jp_id=RUN_AGAIN_JP_ID,
         md=r"\articles\ko1keyz_run_again_utawari_kr.md", table=r"\tools\_gen_table_run_again_kr.html",
         title="KO1KEYZ 'Run Again' \ud30c\ud2b8 \ubd84\ubc30\ub294? 12\uba85 \uc804\uc6d0 \ucd1d\uc815\ub9ac!",
         slug="ko1keyz-run-again-utawari-kr",
         eyecatch=r"\images\ko1keyz_run_again_utawari_eyecatch_kr.png",
         sns="KO1KEYZ\uac00 1ST FAN MEETING \uc559\ucf54\ub974\uc5d0\uc11c \uc120\ubcf4\uc778 'Run Again -KO1KEYZ ver.-'\uc758 12\uba85 \ud30c\ud2b8 \ubd84\ubc30\ub97c \uc774\ubaa8\uc9c0 \ub300\uc2e0 \ub85c\ub9c8\uc790 \uc774\ub984\uc73c\ub85c \uc815\ub9ac\ud588\uc2b5\ub2c8\ub2e4."),
    dict(key="run_again_en", lang="en", jp_id=RUN_AGAIN_JP_ID,
         md=r"\articles\ko1keyz_run_again_utawari_en.md", table=r"\tools\_gen_table_run_again_en.html",
         title="Who Sings What in KO1KEYZ's \u201cRun Again\u201d? All 12 Members' Parts!",
         slug="ko1keyz-run-again-utawari-en",
         eyecatch=None, media=RUN_AGAIN_JP_MEDIA,
         sns="Who sings what in KO1KEYZ's \u201cRun Again -KO1KEYZ ver.-,\u201d performed at the 1ST FAN MEETING encore? Here's the part distribution for all 12 members, romanized names in place of the emoji fans used."),
    dict(key="black_angel_kr", lang="ko", jp_id=BLACK_ANGEL_JP_ID,
         md=r"\articles\ko1keyz_black_angel_utawari_kr.md", table=r"\tools\_gen_table_black_angel_kr.html",
         title="KO1KEYZ 'BLACK ANGEL' \ud30c\ud2b8 \ubd84\ubc30\ub294? 6\uc778 \ubc84\uc804 \ucd1d\uc815\ub9ac!",
         slug="ko1keyz-black-angel-utawari-kr",
         eyecatch=r"\images\ko1keyz_black_angel_utawari_eyecatch_kr.png",
         sns="KO1KEYZ\uac00 1ST FAN MEETING\uc5d0\uc11c \uc120\ubcf4\uc778 'BLACK ANGEL -KO1KEYZ 6\uc778 ver.-'. RYOGA\xb7RYUJI\xb7SHINHAENG\xb7SIYOUNG\xb7YUKI\xb7YURA 6\uba85\uc758 \ud30c\ud2b8 \ubd84\ubc30\ub97c \uc815\ub9ac\ud588\uc2b5\ub2c8\ub2e4."),
    dict(key="black_angel_en", lang="en", jp_id=BLACK_ANGEL_JP_ID,
         md=r"\articles\ko1keyz_black_angel_utawari_en.md", table=r"\tools\_gen_table_black_angel_en.html",
         title="Who Sings What in KO1KEYZ's \u201cBLACK ANGEL\u201d? The 6-Member Parts!",
         slug="ko1keyz-black-angel-utawari-en",
         eyecatch=None, media=BLACK_ANGEL_JP_MEDIA,
         sns="Who sings what in KO1KEYZ's \u201cBLACK ANGEL -KO1KEYZ 6-member ver.-,\u201d performed at 1ST FAN MEETING by RYOGA, RYUJI, SHINHAENG, SIYOUNG, YUKI and YURA? Here's the full part breakdown."),
]

results = {}
for j in JOBS:
    content = load_content(REPO + j["md"], REPO + j["table"])
    if j.get("eyecatch"):
        media_id = upload_media(REPO + j["eyecatch"], j["key"] + "_eyecatch.png")
    else:
        media_id = j["media"]
    body = {
        "title": j["title"], "slug": j["slug"], "content": content, "status": "draft",
        "categories": [66, 62], "author": 2, "featured_media": media_id,
        "lang": j["lang"], "translations": {"ja": j["jp_id"]},
        "meta": {"jetpack_publicize_message": j["sns"]},
    }
    post = api("/wp-json/wp/v2/posts", body, "POST")
    pid = post["id"]
    results[j["key"]] = {"id": pid, "slug": j["slug"], "media_id": media_id, "link": post.get("link")}
    print(f"{j['key']}: id={pid} slug={j['slug']} media_id={media_id} link={post.get('link')}")

print(json.dumps(results, ensure_ascii=False))
