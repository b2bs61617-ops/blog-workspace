# -*- coding: utf-8 -*-
"""Block helpers for KEY TO LIT item articles (chomoand-5.site, 2026-10-18 batch).

Each helper returns Gutenberg-wrapped HTML. Images are written as [[IMG:key]]
placeholders and replaced by the upload script after the media upload.
"""
import html

ACC = "#3d5a80"      # site accent (navy)
LIGHT = "#eef3f8"
BORDER = "#c9d6e6"


def p(*sentences):
    """Paragraph; each argument is one sentence (joined with <br>)."""
    body = "<br>\n".join(sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def mark(text):
    return (f'<strong><span class="swl-marker mark_yellow" style="font-size:1.1em;">'
            f'{text}</span></strong>')


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return (f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n'
            f'<!-- /wp:heading -->')


def _html(inner):
    return f"<!-- wp:html -->\n{inner}\n<!-- /wp:html -->"


def learn(items, title="この記事でわかること"):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return _html(
        f'<div style="border:1px solid {ACC};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">{title}</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{LIGHT};">\n{lis}\n</ul>\n</div>')


def info(rows):
    """rows: list of (label, value)."""
    ps = []
    for i, (k, v) in enumerate(rows):
        m = "0" if i == 0 else "4px 0 0 0"
        ps.append(f'<p style="margin:{m};"><strong>{k}:</strong>{v}</p>')
    return _html(
        f'<div style="border:1px solid {BORDER};border-left:4px solid {ACC};border-radius:4px;'
        f'padding:10px 16px;margin:0 0 16px 0;background:{LIGHT};">\n' + "\n".join(ps) + "\n</div>")


_CHK = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {ACC};'
        f'border-radius:3px;color:{ACC};font-weight:bold;text-align:center;margin-right:6px;'
        f'font-size:0.85em;">&#10003;</span>')


def checks(items):
    ps = "\n".join(f'<p style="margin:0 0 8px 0;">{_CHK}{i}</p>' for i in items)
    return _html(
        f'<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;'
        f'background:{LIGHT};">\n{ps}\n</div>')


def buy(items):
    """items: list of (text, url or None)."""
    lis = []
    for t, u in items:
        lis.append(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' if u else f"<li>{t}</li>")
    return _html(
        f'<div style="border:1px solid {ACC};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">購入先</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{LIGHT};">\n' + "\n".join(lis) + "\n</ul>\n</div>")


def table(head, rows):
    th = "".join(f'<th style="background:{ACC};color:#fff;padding:8px 10px;border:1px solid {BORDER};'
                 f'text-align:left;">{h}</th>' for h in head)
    trs = []
    for r in rows:
        tds = [f'<td style="padding:8px 10px;border:1px solid {BORDER};background:#e3ebf4;font-weight:bold;">{r[0]}</td>']
        tds += [f'<td style="padding:8px 10px;border:1px solid {BORDER};background:#fff;">{c}</td>' for c in r[1:]]
        trs.append("<tr>" + "".join(tds) + "</tr>")
    return _html(
        '<div style="overflow-x:auto;margin:0 0 16px 0;">\n'
        '<table style="width:100%;border-collapse:collapse;font-size:0.95em;">\n'
        f"<thead><tr>{th}</tr></thead>\n<tbody>\n" + "\n".join(trs) + "\n</tbody>\n</table>\n</div>")


def img(key):
    return f"[[IMG:{key}]]"


def xembed(user, sid):
    u = f"https://twitter.com/{user}/status/{sid}"
    return _html(
        f'<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><a href="{u}">{u}</a></blockquote>\n'
        '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def igembed(code, label):
    u = f"https://www.instagram.com/p/{code}/?utm_source=ig_embed&amp;utm_campaign=loading"
    return _html(
        f'<blockquote class="instagram-media" data-instgrm-permalink="{u}" data-instgrm-version="14" '
        'style="background:#FFF;border:0;border-radius:3px;box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);'
        'margin:1px auto 16px;max-width:540px;min-width:326px;padding:0;width:99.375%;">'
        f'<a href="{u}" target="_blank" rel="noopener">{html.escape(label)}</a></blockquote>\n'
        '<script async src="https://www.instagram.com/embed.js"></script>')


def related():
    return "[[RELATED]]"


def build(blocks):
    return "\n\n".join(blocks) + "\n"
