# -*- coding: utf-8 -*-
"""マツコの知らない世界 11/10 汐音凛・野本良平 何者記事 -> chomoand.com 下書き投稿 (2026-11-10 ユカ依頼).

build_and_post_koitoki.py と同じ変換。配色はVIVANT記事の淡い水色。
再実行時は tmp_matsuko_1110_ids.json の記事IDを更新する(title/slugは送らない、status: draftは必ず送る)。
  python build_and_post_vivant_christmas_cake.py [--dry]
"""
import base64, json, os, re, subprocess, sys
from pathlib import Path

import requests

ROOT = Path(__file__).parent
sys.stdout.reconfigure(encoding="utf-8")
COLORS = {"shione_rin_matsuko": ("#7a2e4a", "#fbf2f5", "#e3c9d3"),
          "nomoto_ryohei_matsuko": ("#1f4e79", "#eef4fa", "#c5d6e6")}
ACCENT, LIGHT, BORDER_L = COLORS["shione_rin_matsuko"]
CATEGORY = 37  # 芸能・トレンド
import socket
AUTHOR = 3 if socket.gethostname().upper() == "USER1" else 4

ARTICLES = [
    {"base": "shione_rin_matsuko", "slug": "shione-rin-matsuko-who",
     "title": "【未】【マツコの知らない世界】汐音凛は何者？宮廷ドレス300着の経歴！",
     "eyecatch": ["--top", "マツコの知らない世界", "--main", "汐音凛は何者？", "--bottom", "宮廷ドレス300着の経歴！"]},
    {"base": "nomoto_ryohei_matsuko", "slug": "nomoto-ryohei-matsuko-who",
     "title": "【未】【マツコの知らない世界】野本良平は何者？羽田市場社長の経歴！",
     "eyecatch": ["--top", "マツコの知らない世界", "--main", "野本良平は何者？", "--bottom", "羽田市場社長の経歴！"]},
]


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


DRIVE_ENV = Path(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))
ENV = {**load_env(ROOT / ".env"), **{k: v.strip("\"'") for k, v in load_env(DRIVE_ENV).items() if v and k.startswith("WP_TREND")}, **os.environ}
WP_URL = ENV["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_TREND_USERNAME']}:{ENV['WP_TREND_APP_PASSWORD']}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}
ID_FILE = ROOT / "tmp_matsuko_1110_ids.json"


RELATED = []


def related_box(current):
    items = "".join(f'<li><a href="{WP_URL}/{slug}/">{title}</a></li>' for slug, title in RELATED)
    return (
        f'<div style="border:1px solid {BORDER_L};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{LIGHT};">'
        '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">関連記事</p>'
        f'<ul style="margin:0;padding-left:1.3em;">{items}</ul></div>'
    )


def style_table(inner):
    rows = re.findall(r"<tr>(.*?)</tr>", inner, re.S)
    out = []
    for i, row in enumerate(rows):
        cells = re.findall(r"<td>(.*?)</td>", row, re.S)
        if i == 0:
            tds = "".join(
                f'<td style="border:1px solid #ccc;padding:8px 12px;background:{ACCENT};color:#fff;"><strong>{c}</strong></td>'
                for c in cells)
        else:
            bg = "#ffffff" if i % 2 else LIGHT
            tds = "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;background:{bg};">{c}</td>' for c in cells)
        out.append(f"<tr>{tds}</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n'
            + "\n".join(out) + "\n</tbody></table></figure>\n<!-- /wp:table -->")


def to_blocks(src, base):
    src = src.replace("<!--RELATED-->", related_box(base) if RELATED else "")
    out = []
    pattern = r"<blockquote[^>]*>.*?</blockquote>|<figure[^>]*>.*?</figure>|<div[^>]*>.*?</div>|<(p|h2|h3|table|ul)>(.*?)</\1>|<hr>"
    for m in re.finditer(pattern, src, re.S):
        whole, tag, inner = m.group(0), m.group(1), m.group(2)
        if whole.startswith("<blockquote"):
            out.append("<!-- wp:html -->\n" + whole
                       + '\n<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n<!-- /wp:html -->')
        elif whole.startswith("<div") or whole.startswith("<figure"):
            out.append(f"<!-- wp:html -->\n{whole}\n<!-- /wp:html -->")
        elif tag is None:
            continue  # <hr> は全削除ルール
        elif tag == "p":
            out.append(f"<!-- wp:paragraph -->\n<p>{inner}</p>\n<!-- /wp:paragraph -->")
        elif tag == "h2":
            out.append(f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{inner}</h2>\n<!-- /wp:heading -->')
        elif tag == "h3":
            out.append(f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{inner}</h3>\n<!-- /wp:heading -->')
        elif tag == "table":
            out.append(style_table(inner))
        elif tag == "ul":
            check = (f'<li style="list-style:none;margin-left:-1.2em;"><span style="display:inline-block;border:1px solid {ACCENT};'
                     f'color:{ACCENT};font-size:0.8em;line-height:1;padding:2px 3px;margin-right:6px;">&#10003;</span>')
            items = inner.replace("<li>&#10003; ", check)
            out.append(
                "<!-- wp:html -->\n"
                f'<div style="border:1px solid {BORDER_L};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">この記事のまとめ</p>'
                f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{LIGHT};">{items}</ul></div>\n<!-- /wp:html -->')
    return "\n\n".join(out)


def main():
    ids = json.loads(ID_FILE.read_text(encoding="utf-8")) if ID_FILE.exists() else {}
    global ACCENT, LIGHT, BORDER_L
    for a in ARTICLES:
        base = a["base"]
        ACCENT, LIGHT, BORDER_L = COLORS[base]
        print(base, "title len (w/o 未):", len(a["title"].replace("【未】", "")))
        content = to_blocks((ROOT / "articles" / f"{base}.html").read_text(encoding="utf-8"), base)
        plain = re.sub(r"<[^>]+>|<!--.*?-->", "", content, flags=re.S)
        body_len = len(re.sub(r"\s", "", plain))
        print(f"[{base}] title={len(a['title'])}字 body≈{body_len}字")
        if "--dry" in sys.argv:
            (ROOT / f"tmp_{base}_blocks.html").write_text(content, encoding="utf-8")
            continue
        payload = {"content": content, "status": "draft"}
        if base in ids:
            endpoint = f"{WP_URL}/wp-json/wp/v2/posts/{ids[base]['id']}"
        else:
            eyecatch = ROOT / "images" / f"{base}_eyecatch.png"
            subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_chomoand0.py"), *a["eyecatch"], "--out", str(eyecatch)],
                           check=True, env={**os.environ, "PYTHONUTF8": "1"})
            r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                              headers={**HEADERS_AUTH, "Content-Type": "image/png",
                                       "Content-Disposition": f'attachment; filename="{base}_eyecatch.png"'},
                              data=eyecatch.read_bytes())
            r.raise_for_status()
            payload.update({"title": a["title"], "slug": a["slug"], "featured_media": r.json()["id"],
                            "categories": [CATEGORY], "author": AUTHOR})
            endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        r = requests.post(endpoint, headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                          data=json.dumps(payload).encode("utf-8"))
        r.raise_for_status()
        post = r.json()
        ids[base] = {"id": post["id"], "media": post["featured_media"], "slug": post.get("slug") or a["slug"]}
        ID_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  POST_ID {post['id']} STATUS {post['status']} MEDIA {post['featured_media']} SLUG {ids[base]['slug']}")


if __name__ == "__main__":
    main()
