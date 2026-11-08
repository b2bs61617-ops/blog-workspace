# -*- coding: utf-8 -*-
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def apply(src, out, pairs):
    s = open(src, encoding="utf-8").read()
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, (n, old[:120])
        s = s.replace(old, new)
    open(out, "w", encoding="utf-8", newline="\n").write(s)
    print("ok", out, len(s))


def row(bg, d, prog, mem, bold=False):
    w = (lambda x: f"<strong>{x}</strong>") if bold else (lambda x: x)
    return "<tr>" + "".join(f'<td style="background:{bg};">{w(x)}</td>' for x in (d, prog, mem)) + "</tr>"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n'


def para(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n"


def infobox(accent, bg, border, items):
    ps = []
    for i, (k, v) in enumerate(items):
        m = "0" if i == 0 else "4px 0 0 0"
        ps.append(f'<p style="margin:{m};"><strong>{k}:</strong>{v}</p>')
    return ("<!-- wp:html -->\n"
            f'<div style="border:1px solid {border};border-left:4px solid {accent};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{bg};">\n'
            + "\n".join(ps) + "\n</div>\n<!-- /wp:html -->\n\n")


def CHK(accent):
    return (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {accent};border-radius:3px;'
            f'color:{accent};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')
