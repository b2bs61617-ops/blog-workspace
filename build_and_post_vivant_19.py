# -*- coding: utf-8 -*-
"""VIVANT 第19話(2026-10-04放送) 速報・考察5記事 -> chomoand.com 公開投稿(トモキ指示で即公開).

articles/vivant_0*.html を Gutenberg ブロックへ変換し、
アイキャッチ(tools/eyecatch_chomoand0.py --title)を作ってアップロード、公開で投稿する。
<!--RELATED--> は他4記事への関連記事ボックス。
再実行時は tmp_vivant_19_ids.json の記事IDを更新する(title/slugは送らない)。
"""
import base64, json, os, re, subprocess, sys
from pathlib import Path

import requests

ROOT = Path(__file__).parent
sys.stdout.reconfigure(encoding="utf-8")
ACCENT = "#1a3c4c"


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


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_TREND_USERNAME']}:{ENV['WP_TREND_APP_PASSWORD']}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}
IDS_FILE = ROOT / "tmp_vivant_19_ids.json"

ARTICLES = [
    ("vivant_01_wada", "VIVANT和田さんは死亡した？19話の拷問シーンと生存の可能性を考察！",
     "vivant-wada-death-19", "VIVANT和田さんは死亡した？生存の可能性を考察"),
    ("vivant_02_ryu", "VIVANTリュウと乃木は血縁？そっくりな理由と正体を考察！",
     "vivant-ryu-nogi-blood", "VIVANTリュウと乃木は血縁？そっくりな理由を考察"),
    ("vivant_03_beki", "VIVANTベキは生きてる？生存説と林遣都の登場を考察！",
     "vivant-beki-alive", "VIVANTベキは生きてる？生存説を考察"),
    ("vivant_04_traitor", "VIVANT裏切り者は誰？ノコル「必ず現れる」の意味と候補を考察！",
     "vivant-traitor-who", "VIVANT裏切り者は誰？候補を考察"),
    ("vivant_05_tsubasa", "VIVANT黒須の実家にいた弟・翼は誰？西垣匠の役どころを解説！",
     "vivant-kurosu-tsubasa-nishigaki", "VIVANT黒須の実家にいた弟・翼は誰？西垣匠を解説"),
]


def related_box(self_slug):
    items = "".join(
        f'<li><a href="{WP_URL}/{slug}/">{anchor}</a></li>'
        for _, _, slug, anchor in ARTICLES if slug != self_slug
    )
    return (
        f'<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f7f7;">'
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
            bg = "#ffffff" if i % 2 else "#f4f7f8"
            tds = "".join(
                f'<td style="border:1px solid #ccc;padding:8px 12px;background:{bg};">{c}</td>' for c in cells)
        out.append(f"<tr>{tds}</tr>")
    return (
        '<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n'
        + "\n".join(out)
        + "\n</tbody></table></figure>\n<!-- /wp:table -->"
    )


def to_blocks(src, self_slug):
    src = src.replace("<!--RELATED-->", related_box(self_slug))
    out = []
    pattern = r"<div[^>]*>.*?</div>|<(p|h2|h3|table|ul)>(.*?)</\1>|<hr>"
    for m in re.finditer(pattern, src, re.S):
        whole, tag, inner = m.group(0), m.group(1), m.group(2)
        if whole.startswith("<div"):
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
            items = inner.replace("<li>&#10003; ", '<li style="list-style:none;margin-left:-1.2em;"><span style="display:inline-block;border:1px solid ' + ACCENT + ';color:' + ACCENT + ';font-size:0.8em;line-height:1;padding:2px 3px;margin-right:6px;">&#10003;</span>')
            title = '<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:' + ACCENT + ';color:#fff;">この記事のまとめ</p>' if "&#10003;" in inner else ""
            if title:
                out.append(
                    "<!-- wp:html -->\n"
                    '<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">'
                    f'{title}<ul style="margin:0;padding:14px 18px 14px 34px;background:#f7f7f7;">{items}</ul></div>\n<!-- /wp:html -->'
                )
            else:
                out.append(
                    "<!-- wp:html -->\n"
                    f'<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f7f7;">'
                    f'<ul style="margin:0;padding-left:1.2em;">{inner}</ul></div>\n<!-- /wp:html -->'
                )
    return "\n\n".join(out)


def main():
    only = set(sys.argv[1:])
    ids = json.loads(IDS_FILE.read_text(encoding="utf-8")) if IDS_FILE.exists() else {}
    py = sys.executable
    for base, title, slug, _ in ARTICLES:
        if only and base not in only:
            continue
        content = to_blocks((ROOT / "articles" / f"{base}.html").read_text(encoding="utf-8"), slug)
        plain = re.sub(r"<[^>]+>|<!--.*?-->", "", content, flags=re.S)
        print(f"[{base}] title={len(title)}字 body≈{len(re.sub(r'\s', '', plain))}字")

        payload = {"content": content}
        if base in ids:
            endpoint = f"{WP_URL}/wp-json/wp/v2/posts/{ids[base]['id']}"
        else:
            eyecatch = ROOT / "images" / f"{base}_eyecatch.png"
            subprocess.run([py, str(ROOT / "tools" / "eyecatch_chomoand0.py"), "--title", title, "--out", str(eyecatch)],
                           check=True, env={**os.environ, "PYTHONUTF8": "1"})
            r = requests.post(
                f"{WP_URL}/wp-json/wp/v2/media",
                headers={**HEADERS_AUTH, "Content-Type": "image/png",
                         "Content-Disposition": f'attachment; filename="{base}_eyecatch.png"'},
                data=eyecatch.read_bytes(),
            )
            r.raise_for_status()
            payload.update({"title": title, "slug": slug, "featured_media": r.json()["id"],
                            "status": "publish", "categories": [37], "author": 4})
            endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        r = requests.post(endpoint, headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                          data=json.dumps(payload).encode("utf-8"))
        r.raise_for_status()
        post = r.json()
        ids[base] = {"id": post["id"], "media": post["featured_media"], "slug": post.get("slug") or slug}
        IDS_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  POST_ID {post['id']} STATUS {post['status']} MEDIA {post['featured_media']} SLUG {ids[base]['slug']}")


if __name__ == "__main__":
    main()
