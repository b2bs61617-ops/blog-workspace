# -*- coding: utf-8 -*-
"""LOST10 第6話(2026-11-20放送) 考察4記事 -> chomoand.com 下書き.

articles/lost10ep6_0*.html(手書きHTML)をブロック形式にして、公式Xの場面写真を
最初のH2の情報ボックスの下に入れ、blogkit.upload_draft で下書きにする。

    python tools/_build_lost10ep6.py all --build-only   # チェックだけ
    python tools/_build_lost10ep6.py all                # 下書き
    python tools/_build_lost10ep6.py doku --update      # 本文の上書き
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "trend"
CATEGORIES = [37]
ACCENT = "#2e4a3f"
BASE = "https://chomoand.com/"
NAMES = ["横浜流星", "小栗旬", "岩谷健司", "井口理", "松下洸平", "飯豊まりえ", "野呂佳代",
         "木内天奏", "中村アン", "塚原あゆ子"]

ARTS = {
    "doku": ("lost10ep6_01_doku", "LOST10小駒に毒を盛ったのは誰？コルヒチンの入手先を考察！",
             "lost10-6-koma-doku-hannin", "小駒に毒を盛ったのは誰？犯人候補4人(6話)"),
    "heya": ("lost10ep6_02_heya", "LOST10直の部屋を荒らしたのは誰？手帳を川に捨てた理由も考察！",
             "lost10-6-nao-heya-arashi", "直の部屋を荒らしたのは誰？手帳を捨てた理由(6話)"),
    "techo": ("lost10ep6_03_techo", "LOST10田畠の手帳の中身は？ツガル案件と30万の意味を考察！",
              "lost10-6-tabata-techo", "田畠の手帳の中身は？ツガル案件と30万(6話)"),
    "nobori": ("lost10ep6_04_nobori", "LOST10登里は何者？薬物鑑定の結果と小駒との関係を考察！",
               "lost10-6-nobori-nanimono", "登里は何者？薬物鑑定の結果(6話)"),
}
OLD = [
    ("lost10-yoshino-hannin", "吉野先生が犯人？怪しい5つの理由(4話)"),
    ("lost10-4-nao-musume-akane", "直の娘はなぜ亡くなった？妻あかねとの関係(4話)"),
    ("lost10-4-monden-nanimono", "門伝は何者？強すぎる正体と生きていた理由(4話)"),
]
PHOTOS = {
    "doku": ("lost10ep6_HXeacEnbsAARPcW.jpg", "https://x.com/lost10_tbs/status/2123370708692815883",
             "コーヒーを手にする小駒(第6話・公式Xより)"),
    "heya": ("lost10ep6_HXeacE1a4AEhNkA.jpg", "https://x.com/lost10_tbs/status/2123370708692815883",
             "第6話の直(公式Xより)"),
    "techo": ("lost10ep6_HXeacEibwAAIPXE.jpg", "https://x.com/lost10_tbs/status/2123370708692815883",
              "第6話の吉野先生(公式Xより)"),
    "nobori": ("lost10ep6_HXkrU3VaMAABjVq.jpg", "https://x.com/lost10_tbs/status/2123776342365987237",
               "第6話の場面写真(公式Xより)"),
}
PHOTO_CACHE = blogkit.ARTICLES / "lost10ep6_photos.json"


def related_box(self_key):
    items = "".join('<li><a href="{}{}/">{}</a></li>'.format(BASE, v[2], v[3]) for k, v in ARTS.items() if k != self_key)
    items += "".join('<li><a href="{}{}/">{}</a></li>'.format(BASE, s, a) for s, a in OLD)
    return ('<div style="border:1px solid #ddd;border-left:4px solid {a};border-radius:4px;padding:14px 18px;'
            'margin:0 0 16px 0;background:#f7f7f7;"><p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">'
            '関連記事</p><ul style="margin:0;padding-left:1.3em;">{i}</ul></div>').format(a=ACCENT, i=items)


def photo_url(k, dry):
    if dry:
        return "https://example.com/x.jpg"
    d = json.loads(PHOTO_CACHE.read_text(encoding="utf-8")) if PHOTO_CACHE.exists() else {}
    if k not in d:
        wp = blogkit.WP(SITE)
        mid = wp.upload_media(str(blogkit.ROOT / "images" / PHOTOS[k][0]), PHOTOS[k][2])
        m = wp.get("/media/{}".format(mid))
        sizes = m.get("media_details", {}).get("sizes", {})
        d[k] = (sizes.get("medium_large") or sizes.get("large") or sizes.get("full") or {}).get("source_url", m["source_url"])
        PHOTO_CACHE.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return d[k]


def photo_html(k, url):
    _, src, cap = PHOTOS[k]
    return ('<div><figure style="margin:0 0 16px 0;text-align:center;"><img src="' + url + '" alt="' + cap
            + '" style="max-width:100%;height:auto;" loading="lazy"><figcaption style="font-size:0.8em;color:#888;">'
            + cap + ' 出典:<a href="' + src + '" target="_blank" rel="noopener">' + src + '</a></figcaption></figure></div>')


def style_table(inner):
    rows = re.findall(r"<tr>(.*?)</tr>", inner, re.S)
    out = []
    for i, row in enumerate(rows):
        cells = re.findall(r"<td>(.*?)</td>", row, re.S)
        if i == 0:
            tds = "".join('<td style="border:1px solid #ccc;padding:8px 12px;background:{};color:#fff;"><strong>{}</strong></td>'
                          .format(ACCENT, c) for c in cells)
        else:
            bg = "#ffffff" if i % 2 else "#f4f7f8"
            tds = "".join('<td style="border:1px solid #ccc;padding:8px 12px;background:{};">{}</td>'.format(bg, c) for c in cells)
        out.append("<tr>{}</tr>".format(tds))
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n'
            + "\n".join(out) + "\n</tbody></table></figure>\n<!-- /wp:table -->")


def to_blocks(src):
    out = []
    pattern = r"<div[^>]*>.*?</div>|<(p|h2|h3|table|ul)>(.*?)</\1>"
    for m in re.finditer(pattern, src, re.S):
        whole, tag, inner = m.group(0), m.group(1), m.group(2)
        if whole.startswith("<div"):
            if whole.startswith("<div><figure"):
                whole = whole[5:-6]
            out.append("<!-- wp:html -->\n{}\n<!-- /wp:html -->".format(whole))
        elif tag == "p":
            out.append("<!-- wp:paragraph -->\n<p>{}</p>\n<!-- /wp:paragraph -->".format(inner))
        elif tag == "h2":
            out.append('<!-- wp:heading -->\n<h2 class="wp-block-heading">{}</h2>\n<!-- /wp:heading -->'.format(inner))
        elif tag == "h3":
            out.append('<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{}</h3>\n<!-- /wp:heading -->'.format(inner))
        elif tag == "table":
            out.append(style_table(inner))
        elif tag == "ul":
            if "&#10003;" in inner:
                items = inner.replace("<li>&#10003; ", '<li style="list-style:none;margin-left:-1.2em;"><span style="display:inline-block;border:1px solid '
                                      + ACCENT + ';color:' + ACCENT + ';font-size:0.8em;line-height:1;padding:2px 3px;margin-right:6px;">&#10003;</span>')
                out.append('<!-- wp:html -->\n<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">'
                           '<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:' + ACCENT
                           + ';color:#fff;">この記事のまとめ</p><ul style="margin:0;padding:14px 18px 14px 34px;background:#f7f7f7;">'
                           + items + '</ul></div>\n<!-- /wp:html -->')
            else:
                out.append('<!-- wp:html -->\n<div style="border:1px solid #ddd;border-left:4px solid ' + ACCENT
                           + ';border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f7f7;">'
                           '<ul style="margin:0;padding-left:1.2em;">' + inner + '</ul></div>\n<!-- /wp:html -->')
    return "\n\n".join(out)


def build(k, dry):
    key = ARTS[k][0]
    src = (blogkit.ARTICLES / (key + ".html")).read_text(encoding="utf-8")
    src = src.replace("<!--RELATED-->", related_box(k))
    # 写真: 最初のH2の直後の情報ボックスの下
    m = re.search(r"<h2>.*?</h2>\s*<div[^>]*>.*?</div>", src, re.S)
    src = src[:m.end()] + "\n" + photo_html(k, photo_url(k, dry)) + src[m.end():]
    return blogkit.finalize(to_blocks(src), SITE, NAMES)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    dry = "--build-only" in sys.argv
    targets = [a for a in sys.argv[1:] if not a.startswith("--")]
    if targets in (["all"], []):
        targets = list(ARTS)
    for t in targets:
        key, title, slug, _ = ARTS[t]
        out = build(t, dry)
        eye = blogkit.ROOT / "images" / (key + "_eyecatch.jpg")
        if dry:
            import fact_check
            rep = fact_check.run(out, site_key=SITE, title=title, names=NAMES, net=False)
            print("==", t, len(title), "字")
            print(fact_check.format_report(rep))
            (blogkit.ARTICLES / (key + "_built.html")).write_text(out, encoding="utf-8")
        else:
            blogkit.upload_draft(SITE, key + "_wp", title, out, slug, CATEGORIES, eye, title,
                                 names=NAMES, update="--update" in sys.argv)
