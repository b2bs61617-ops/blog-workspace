"""chomoand-4.blog 残り10記事(下書き8+公開2)のリライト用共通部品(2026-09-19、午前のrw.pyの続き).

- 午前の rw.py(HTML部品)をそのまま使う。
- 下書きの記事は url() の対応表に無いので、before.json のスラッグからURLを作る(U/L/related)。
- push2 は本文(content)だけ送る。title・slug・statusは送らない(公開済みは公開のまま、下書きは下書きのまま)。
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

NEW = Path(__file__).resolve().parent
sys.path.insert(0, str(NEW.parent / "chomoand4_rewrite_2026-09-19"))
import rw  # noqa: E402
from rw import *  # noqa: E402,F401,F403

BEFORE = {
    p["id"]: p
    for p in json.loads((NEW.parent / "chomoand4_eyecatch_3line_2026-09-19" / "before.json").read_text(encoding="utf-8"))
}


def orig(pid):
    return (NEW / "original" / f"{pid}.html").read_text(encoding="utf-8")


def U(pid):
    try:
        return rw.url(pid)
    except KeyError:
        return f"{rw.SITE}/{BEFORE[pid]['slug']}"


def L(pid, text):
    return f'<a href="{U(pid)}">{text}</a>'


def related(links, pal, title="あわせて読みたい関連記事"):
    li = "\n".join(f'<li><a href="{U(pid)}">{t}</a></li>' for pid, t in links)
    return html(
        f'<div style="border:1px solid {pal["border"]};border-left:4px solid {pal["accent"]};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{pal["bg"]};">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n{li}\n</ul>\n</div>'
    )


def push2(pid, content):
    """本文だけ更新(title/slug/statusは送らない)。"""
    base, h = rw._hdr()
    req = urllib.request.Request(
        f"{base}/wp-json/wp/v2/posts/{pid}",
        data=json.dumps({"content": content}).encode("utf-8"),
        headers=h,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            d = json.load(r)
            return d["status"], d["link"], d["title"]["raw"] == BEFORE[pid]["title"]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")[:300]


def run(pid, content, title):
    """python art_XXX.py で文字数確認、--push で本文更新。"""
    import re

    assert title == BEFORE[pid]["title"], "title mismatch"
    assert "<hr" not in content and "---" not in content
    if "--push" in sys.argv:
        print(pid, push2(pid, content))
    else:
        print(pid, "chars", len(re.sub(r"<[^>]+>", "", content)))
