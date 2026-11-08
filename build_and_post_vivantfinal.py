# -*- coding: utf-8 -*-
"""VIVANT 最終回(第24話)(2026-11-08放送) 考察5記事 -> chomoand.com 下書き投稿.

articles/vivantfinal_0*.html を Gutenberg ブロックへ変換し、
下書きで投稿する(アイキャッチはCanva DAGnrXY2_5I 上書き→別途 featured_media)。
<!--RELATED--> は他4記事への関連記事ボックス。
再実行時は tmp_vivantfinal_ids.json の記事IDを更新する(title/slugは送らない)。
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
IDS_FILE = ROOT / "tmp_vivantfinal_ids.json"

ARTICLES = [
    ("vivantfinal_01_kaoru", "VIVANT最終回の薫は何者？白い手袋の意味と正体を考察！",
     "vivant-24-kaoru-shotai", "最終回の薫は何者？白い手袋の意味と正体"),
    ("vivantfinal_02_beki", "VIVANTベキと薫は顔見知り？紹介シーンの違和感を考察！",
     "vivant-24-beki-kaoru-kaomishiri", "ベキと薫は顔見知り？紹介シーンの違和感"),
    ("vivantfinal_03_juice", "VIVANT最終回で乃木は薬を盛られた？ジュースと寝坊の謎を考察！",
     "vivant-24-nogi-kusuri-juice", "乃木は薬を盛られた？ジュースと寝坊の謎"),
    ("vivantfinal_04_movie", "映画VIVANTはいつ公開？チケット発売日と最終回の続きを解説！",
     "vivant-movie-1204-ticket", "映画VIVANTはいつ公開？チケット発売日"),
    ("vivantfinal_05_nozaki", "VIVANT野崎とリュウはいつから組んでた？中央特務局とは？",
     "vivant-24-nozaki-ryu-itsukara", "野崎とリュウはいつから組んでた？中央特務局とは"),
    ("vivantfinal_06_manju", "VIVANT最終回の別班饅頭の意味は？誰が置いたか次の任務を考察！",
     "vivant-24-beppan-manju", "最終回の別班饅頭の意味は？誰が置いた？"),
    ("vivantfinal_07_elisha", "VIVANTエリシャは最終回で死んだ？核融合データの在りかも解説！",
     "vivant-24-elisha-data", "エリシャは死んだ？核融合データの在りか"),
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

        payload = {"content": content}  # 既存記事のstatusは触らない(公開済みを下書きに戻さない)
        if base in ids:
            endpoint = f"{WP_URL}/wp-json/wp/v2/posts/{ids[base]['id']}"
        else:
            payload.update({"title": title, "slug": slug, "status": "draft", "categories": [37], "author": 4})
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
