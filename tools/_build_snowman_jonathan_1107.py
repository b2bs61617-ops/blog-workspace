# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) すのちゅーぶ「ジョナサン人気TOP10を当てろ！」(2026-11-04配信、F9qbyNJPS6E)のロケ地=ジョナサン宮前平店の記事HTMLを組み立てる。

usage: python tools/_build_snowman_jonathan_1107.py
articles/snowman_jonathan_location.html と articles/snowman_jonathan_location_manifest.json を書き出す。
投稿は tools/_upload_snowman_jonathan_1107.py({{IMG:name}} を images/snowman_jonathan_frame_{name}.jpg のURLに置き換える)。
"""
import os, json, sys
from urllib.parse import quote

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ACC = "#3f7fc4"      # 渡辺presents回なので渡辺翔太のメンバーカラー(青)
BG = "#eef5fc"
LINE = "#cfe0f3"
MK = "#d6e2f0"

def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n"


def mk(text):
    return f'<strong><span style="font-size:1.1em;background:linear-gradient(transparent 60%,{MK} 60%);">{text}</span></strong>'


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n'


def html(s):
    return "<!-- wp:html -->\n" + s + "\n<!-- /wp:html -->\n"


def listbox(title, items, big=False):
    fs = "font-size:1.05em;" if big else ""
    pad = "10px 18px" if big else "8px 16px"
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return html(f'<div style="border:1px solid {ACC if big else LINE};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                f'<p style="font-weight:bold;{fs}margin:0;padding:{pad};background:{ACC};color:#fff;">{title}</p>\n'
                f'<ul style="margin:0;padding:12px 18px 12px 34px;background:{BG};">\n{lis}\n</ul>\n</div>')


def keybox(rows):
    out = []
    for i, (k, v) in enumerate(rows):
        m = "0" if i == 0 else "4px 0 0 0"
        out.append(f'<p style="margin:{m};"><strong>{k}:</strong>{v}</p>')
    return html(f'<div style="border:1px solid {LINE};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">\n'
                + "\n".join(out) + "\n</div>")


def quote_box(lines, src):
    body = "<br>\n".join(lines)
    return html(f'<div style="border:1px solid {LINE};border-radius:4px;padding:12px 18px;margin:0 0 16px 0;background:{BG};">\n'
                f'<p style="margin:0;">{body}</p>\n<p style="margin:6px 0 0 0;font-size:0.85em;color:#777;text-align:right;">{src}</p>\n</div>')


def table(rows):
    trs = []
    for i, r in enumerate(rows):
        st = f' style="background:{BG};font-weight:bold;"' if i == 0 else ""
        trs.append("<tr>" + "".join(f"<td{st}>{c}</td>" for c in r) + "</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            + "".join(trs) + "</tbody></table></figure>\n<!-- /wp:table -->\n")


def related(items):
    lis = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in items)
    return html(f'<div style="border:1px solid {LINE};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;">\n'
                f'<p style="margin:0 0 6px 0;font-weight:bold;color:{ACC};">あわせて読みたい</p>\n<ul style="margin:0;padding-left:20px;">{lis}</ul>\n</div>')


def ytembed(vid):
    return html(f'<div style="position:relative;width:100%;padding-top:56.25%;margin:0 0 16px 0;">'
                f'<iframe src="https://www.youtube.com/embed/{vid}" title="YouTube video" loading="lazy" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" '
                'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')


def frame(name, alt, src, label):
    return html('<figure class="wp-block-image size-large">\n'
                f'<img src="{{{{IMG:{name}}}}}" alt="{alt}" width="1280" height="720" style="max-width:100%;height:auto;" loading="lazy">\n'
                f'<figcaption style="font-size:0.8em;color:#888;">出典:<a href="{src}" target="_blank" rel="noopener">{label}</a></figcaption>\n</figure>')


def gmap(q):
    return html(f'<iframe src="https://www.google.com/maps?q={quote(q)}&output=embed" width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy"></iframe>')



import _build_snowman_jonathan_1107_body as B

body = B.build(p, mk, h2, h3, html, listbox, keybox, table, related, ytembed, frame, gmap)

ARTICLES = [
    {"key": "jonathan_location", "title": "【未】【ジョナサン人気TOP10を当てろ！】ロケ地はどこ？店舗とランキング",
     "slug": "snow-man-youtube-jonathan-location-ranking",
     "categories": [4, 9, 10, 13], "frames": ["sign", "exterior", "top10", "rank20"], "html": body},
]


def main():
    manifest = []
    for a in ARTICLES:
        path = os.path.join("articles", f"snowman_{a['key']}.html")
        with open(os.path.join(REPO, path), "w", encoding="utf-8") as f:
            f.write(a["html"])
        m = {k: v for k, v in a.items() if k != "html"}
        m["file"] = path.replace("\\", "/")
        manifest.append(m)
        print("wrote", path)
    with open(os.path.join(REPO, "articles", "snowman_jonathan_location_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
