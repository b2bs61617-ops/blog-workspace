# -*- coding: utf-8 -*-
"""Upload KEY TO LIT item articles (2026-10-18 batch) to chomoand-5.site as drafts.

usage: python tools/_upload_ktl_items_1018.py a|b|all [--only key1,key2] [--related]
State (post/media ids) is kept in tools/_ktl_items_1018_state.json so re-runs skip done work.
"""
import sys, os, re, json, base64, subprocess, urllib.request, urllib.error

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
sys.path.insert(0, REPO + r"\tools")
from _ktl_items_lib import build, ACC, LIGHT  # noqa: E402

STATE = REPO + r"\tools\_ktl_items_1018_state.json"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_CHOMO5_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_CHOMO5_USERNAME']}:{env['WP_CHOMO5_APP_PASSWORD']}".encode()).decode()
AUTHOR = 2  # hostname USER1 -> momo


def req(path, data=None, headers=None, method="POST"):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode('utf-8', 'ignore')[:500]}")


def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})


def upload(path, fn, alt=""):
    m = req("/wp-json/wp/v2/media", open(path, "rb").read(),
            {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{fn}"'})
    if alt:
        jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": alt})
    return m


def figure(m, alt, cap):
    sz = m.get("media_details", {}).get("sizes", {})
    full = m["source_url"]
    fw, fh = m["media_details"].get("width"), m["media_details"].get("height")
    lg = sz.get("large") or {"source_url": full, "width": fw, "height": fh}
    srcset = []
    if "medium" in sz:
        srcset.append(f"{sz['medium']['source_url']} {sz['medium']['width']}w")
    if "large" in sz:
        srcset.append(f"{sz['large']['source_url']} {sz['large']['width']}w")
    srcset.append(f"{full} {fw}w")
    return ("<!-- wp:html -->\n<figure class=\"wp-block-image size-large\">\n"
            f"<img src=\"{lg['source_url']}\" alt=\"{alt}\" width=\"{lg['width']}\" height=\"{lg['height']}\"\n"
            "  style=\"max-width:100%;height:auto;\"\n"
            f"  srcset=\"{', '.join(srcset)}\"\n  sizes=\"(max-width: 1024px) 100vw, 1024px\">\n"
            f"<figcaption style=\"font-size:0.8em;color:#888;\">{cap}</figcaption>\n</figure>\n<!-- /wp:html -->")


def related_box(art, arts, state):
    mine = [a for a in arts if a["key"] != art["key"] and a["key"] in state["posts"]]
    pick = [a for a in mine if a["scene"] == art["scene"]]
    pick += [a for a in mine if a["member"] == art["member"] and a not in pick]
    pick = pick[:6]
    if not pick:
        return ""
    lis = "\n".join(f'<li><a href="{BASE}/?p={state["posts"][a["key"]]}">{a["title"]}</a></li>' for a in pick)
    return ("<!-- wp:html -->\n"
            f'<div style="border:1px solid #c9d6e6;border-left:4px solid {ACC};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{LIGHT};">\n'
            '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい</p>\n'
            f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>\n<!-- /wp:html -->')


# Member-color themes (2026-10-18 user rule: KTL item articles use the subject member's color)
THEMES = {
    "岩﨑大昇": dict(acc="#7d848c", light="#f3f4f5", border="#d5d8dc", cell="#e6e8eb", mark="#dfe2e6"),  # white -> silver gray
    "井上瑞稀": dict(acc="#d2414f", light="#fdf0f1", border="#f2c4c9", cell="#fadde0", mark="#f9cbd0"),  # red
    "中村嶺亜": dict(acc="#d6588a", light="#fdf1f6", border="#f3c6d9", cell="#fbe3ed", mark="#f8cfe0"),  # pink
    "猪狩蒼弥": dict(acc="#3a9468", light="#edf7f1", border="#c2e3d0", cell="#d9efe2", mark="#c8ead6"),  # green
    "佐々木大光": dict(acc="#3a78c9", light="#eef4fc", border="#c5d9f2", cell="#dce9f8", mark="#cddff6"),  # blue
}


def apply_theme(html, member):
    t = THEMES[member]
    html = (html.replace("#3d5a80", t["acc"]).replace("#eef3f8", t["light"])
                .replace("#c9d6e6", t["border"]).replace("#e3ebf4", t["cell"]))
    html = html.replace('<span class="swl-marker mark_yellow" style="font-size:1.1em;">',
                        f'<span style="font-size:1.1em;background:linear-gradient(transparent 60%,{t["mark"]} 60%);">')
    return html


def render(art, state, arts, with_related):
    html = build(art["blocks"])
    for k, (path, alt, cap) in art["images"].items():
        mid = state["media"].get(f"{art['key']}:{k}")
        m = state["media_obj"][str(mid)]
        html = html.replace(f"[[IMG:{k}]]", figure(m, alt, cap))
    html = html.replace("[[RELATED]]", related_box(art, arts, state) if with_related else "")
    html = re.sub(r"<hr\s*/?>", "", html)
    assert "[[IMG:" not in html, art["key"]
    return apply_theme(html, art["member"])


def main():
    which = sys.argv[1]
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    arts = []
    if which in ("a", "all"):
        from _ktl_items_articles_a import ARTICLES as A
        arts += A
    if which in ("b", "all"):
        from _ktl_items_articles_b import ARTICLES as B
        arts += B
    state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {"posts": {}, "media": {}, "media_obj": {}, "eye": {}}
    for a in arts:
        n = len(a["title"])
        assert n <= 35, (a["title"], n)

    if "--related" in sys.argv:
        for a in arts:
            if a["key"] not in state["posts"] or (only and a["key"] not in only):
                continue
            html = render(a, state, arts, True)
            jpost(f"/wp-json/wp/v2/posts/{state['posts'][a['key']]}", {"content": html, "status": "draft"})
            print("related updated", a["key"], state["posts"][a["key"]])
        return

    for a in arts:
        if only and a["key"] not in only:
            continue
        if a["key"] in state["posts"]:
            print("skip (posted)", a["key"], state["posts"][a["key"]])
            continue
        for k, (path, alt, cap) in a["images"].items():
            sk = f"{a['key']}:{k}"
            if sk not in state["media"]:
                m = upload(path, f"ktl_{a['key']}_{k}.jpg", alt)
                state["media"][sk] = m["id"]
                state["media_obj"][str(m["id"])] = {"source_url": m["source_url"], "media_details": m["media_details"]}
                json.dump(state, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        # eyecatch
        eye_out = REPO + rf"\images\ktl_{a['key']}_eyecatch.jpg"
        if a["key"] not in state["eye"]:
            main_txt, bottoms = a["eye"]
            cmd = [sys.executable, REPO + r"\tools\eyecatch_kitetsu.py", "--main", main_txt,
                   "--color-key", a.get("eye_color", a["member"]), "--out", eye_out]
            for b in bottoms:
                cmd += ["--bottom", b]
            subprocess.run(cmd, check=True, cwd=REPO)
            em = upload(eye_out, os.path.basename(eye_out))
            state["eye"][a["key"]] = em["id"]
            json.dump(state, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        html = render(a, state, arts, False)
        post = jpost("/wp-json/wp/v2/posts", {
            "title": a["title"], "slug": a["slug"], "content": html, "status": "draft",
            "categories": a["cats"], "author": AUTHOR, "featured_media": state["eye"][a["key"]]})
        state["posts"][a["key"]] = post["id"]
        json.dump(state, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("posted", a["key"], post["id"], post["slug"])


if __name__ == "__main__":
    main()
