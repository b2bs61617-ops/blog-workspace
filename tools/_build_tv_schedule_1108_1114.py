# -*- coding: utf-8 -*-
"""Build TV schedule articles 11/8-11/14 (Travis Japan / KEY TO LIT / Snow Man / SixTONES / KO1KEYZ JP).
Source: bangumi.org (Gガイド) listings fetched 2026-11-05 (Tokyo area, terrestrial/BS/CS), official sites.
Titles get 【未】 (to be rewritten just before publishing)."""
import os

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
NOTE = "※2026年11月5日時点の情報です。11/13(金)・14(土)分はまだ番組表が出ていないため、毎週の放送枠から分かる範囲で載せています。放送内容・時間は変更になる場合があるため、最新情報は公式サイトや番組表でご確認ください。"


def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n'


def html(x):
    return f"<!-- wp:html -->\n{x}\n<!-- /wp:html -->\n\n"


class Theme:
    def __init__(self, main, light, border):
        self.main, self.light, self.border = main, light, border

    def toc(self, items):
        lis = "".join(f"<li>{i}</li>\n" for i in items)
        return html(f'<div style="border:1px solid {self.main};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                    f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{self.main};color:#fff;">この記事でわかること</p>\n'
                    f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{self.light};">\n{lis}</ul>\n</div>')

    def info(self, rows):
        ps = []
        for i, (k, v) in enumerate(rows):
            m = "0" if i == 0 else "4px 0 0 0"
            ps.append(f'<p style="margin:{m};"><strong>{k}:</strong>{v}</p>')
        return html(f'<div style="border:1px solid {self.border};border-left:4px solid {self.main};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{self.light};">\n'
                    + "\n".join(ps) + "\n</div>")

    def table(self, head, rows):
        th = "".join(f"<th>{x}</th>" for x in head)
        trs = []
        for r in rows:
            bold = r[-1] is True
            cells = r[:-1] if bold else r
            if bold:
                cells = [f"<strong>{c}</strong>" for c in cells]
            trs.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
        return html(f'<figure class="wp-block-table"><table class="has-fixed-layout"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></figure>')

    def summary(self, items):
        chk = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {self.main};border-radius:3px;'
               f'color:{self.main};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')
        return html(f'<div style="border:1px solid {self.main};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{self.light};">\n'
                    f'<p style="margin:0;">' + "<br>\n".join(chk + i for i in items) + "</p>\n</div>")

    def related(self, title, links):
        lis = "".join(f'<li><a href="{u}">{t}</a></li>\n' for u, t in links)
        return html(f'<div style="border:1px solid {self.border};border-left:4px solid {self.main};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{self.light};">\n'
                    f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n<ul style="margin:0;padding-left:1.3em;">\n{lis}</ul>\n</div>')


def save(name, body):
    with open(os.path.join(REPO, "articles", name), "w", encoding="utf-8") as f:
        f.write(body)
    print(name, len(body))
