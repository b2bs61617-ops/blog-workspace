# -*- coding: utf-8 -*-
"""SixTONES (chomoand-0.com) member-color theming for article HTML.

Articles are written with the neutral palette (header #333333 / bg #f5f5f5 / border #d5d5d5 /
marker #d2d3d6). This tool swaps those for member colors (docs/rules.md "SixTONES記事の色はメンカラ"):

  python tools/sixtones_theme.py article.html --member 田中樹      # whole article in one member's color
  python tools/sixtones_theme.py article.html --per-section        # group article: each H2 (or H3) section
                                                                   # gets the color of the member named in
                                                                   # its heading; group boxes get a 6-color stripe
Rewrites the file in place.
"""
import argparse
import re

NEUTRAL = dict(acc="#333333", light="#f5f5f5", border="#d5d5d5", mark="#d2d3d6")

# 黒/黄は文字・線が読めるように濃いめに寄せる
THEMES = {
    "ジェシー": dict(acc="#d2414f", light="#fdf0f1", border="#f2c4c9", cell="#fadde0", mark="#f9cbd0"),  # red
    "京本大我": dict(acc="#d6588a", light="#fdf1f6", border="#f3c6d9", cell="#fbe3ed", mark="#f8cfe0"),  # pink
    "松村北斗": dict(acc="#2b2b2b", light="#f2f2f2", border="#c9c9c9", cell="#e4e4e4", mark="#d6d6d6"),  # black
    "髙地優吾": dict(acc="#c99a06", light="#fdf8e6", border="#f0dc9a", cell="#fbefc4", mark="#fbe7a1"),  # yellow
    "森本慎太郎": dict(acc="#3a9468", light="#edf7f1", border="#c2e3d0", cell="#d9efe2", mark="#c8ead6"),  # green
    "田中樹": dict(acc="#3a78c9", light="#eef4fc", border="#c5d9f2", cell="#dce9f8", mark="#cddff6"),  # blue
}
ORDER = ["ジェシー", "京本大我", "松村北斗", "髙地優吾", "森本慎太郎", "田中樹"]
STRIPE = ('<div style="height:5px;background:linear-gradient(90deg,'
          + ",".join(f'{THEMES[m]["acc"]} {i*100//6}%,{THEMES[m]["acc"]} {(i+1)*100//6}%' for i, m in enumerate(ORDER))
          + ');"></div>')


def apply_theme(html, member):
    t = THEMES[member]
    for k in ("acc", "light", "border", "mark"):
        html = html.replace(NEUTRAL[k], t[k])
    return html


def members_in(text):
    return [m for m in ORDER if m in text]


def theme_by_headings(chunk, level):
    """Split chunk at headings of `level` and theme each piece by the single member in its heading."""
    pat = rf'(?=<!-- wp:heading(?: \{{"level":{level}\}})? -->\s*<h{level})'
    parts = re.split(pat, chunk)
    out = []
    for p in parts:
        h = re.search(rf"<h{level}[^>]*>(.*?)</h{level}>", p, re.S)
        ms = members_in(h.group(1)) if h else []
        if len(ms) == 1:
            p = apply_theme(p, ms[0])
        elif len(ms) > 1 and level == 2:
            p = theme_by_headings(p, 3)
        out.append(p)
    return "".join(out)


def color_table_rows(html):
    """In group tables, tint the first cell of each row with the member's color."""
    def row(m):
        tr = m.group(0)
        first = re.search(r'<td style="([^"]*)">([^<]*)</td>', tr)
        if not first:
            return tr
        ms = members_in(first.group(2))
        if len(ms) != 1:
            return tr
        t = THEMES[ms[0]]
        new = f'<td style="{first.group(1)}background:{t["cell"]};border-left:4px solid {t["acc"]};font-weight:bold;white-space:nowrap;">{first.group(2)}</td>'
        return tr.replace(first.group(0), new, 1)
    return re.sub(r"<tr>.*?</tr>", row, html, flags=re.S)


def stripe_group_boxes(html):
    """Put the 6-color stripe on top of neutral boxes with a dark title bar (この記事でわかること・まとめ)."""
    return re.sub(r'(<div style="border:1px solid #d5d5d5;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n)',
                  r"\1" + STRIPE + "\n", html)


def per_section(html):
    first_h2 = re.search(r"<!-- wp:heading -->\s*<h2", html)
    head, body = (html[:first_h2.start()], html[first_h2.start():]) if first_h2 else (html, "")
    body = theme_by_headings(body, 2)
    html = head + body
    html = color_table_rows(html)
    html = stripe_group_boxes(html)
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--member", choices=ORDER)
    g.add_argument("--per-section", action="store_true")
    a = ap.parse_args()
    html = open(a.file, encoding="utf-8").read()
    html = apply_theme(html, a.member) if a.member else per_section(html)
    open(a.file, "w", encoding="utf-8").write(html)
    print("themed", a.file)


if __name__ == "__main__":
    main()
