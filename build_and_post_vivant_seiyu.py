# -*- coding: utf-8 -*-
"""VIVANT声優一覧(第19話時点、随時追記) -> chomoand.com 下書き投稿.

articles/vivant_seiyu_list.html を Gutenberg ブロックへ変換し、
アイキャッチ(tools/eyecatch_chomoand0.py --title)を作ってアップロード、下書きで投稿する。
変換は build_and_post_vivant_19.py と同じ(X埋め込みのblockquoteだけ追加対応)。
再実行時は tmp_vivant_seiyu_id.json の記事IDを更新する(title/slugは送らない、status: draftは必ず送る)。
"""
import base64, json, os, re, subprocess, sys
from pathlib import Path

import requests

ROOT = Path(__file__).parent
sys.stdout.reconfigure(encoding="utf-8")
ACCENT = "#1a3c4c"
BASE = "vivant_seiyu_list"
TITLE = "VIVANT声優一覧！誰が誰の声？担当役と登場話まとめ"
SLUG = "vivant-voice-actors-list"


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
ID_FILE = ROOT / "tmp_vivant_seiyu_id.json"

RELATED = [
    ("vivant-wada-death-19", "VIVANT和田さんは死亡した？生存の可能性を考察"),
    ("vivant-ryu-nogi-blood", "VIVANTリュウと乃木は血縁？そっくりな理由を考察"),
    ("vivant-beki-alive", "VIVANTベキは生きてる？生存説を考察"),
    ("vivant-traitor-who", "VIVANT裏切り者は誰？候補を考察"),
    ("vivant-kurosu-tsubasa-nishigaki", "VIVANT黒須の実家にいた弟・翼は誰？西垣匠を解説"),
]


def related_box():
    items = "".join(f'<li><a href="{WP_URL}/{slug}/">{anchor}</a></li>' for slug, anchor in RELATED)
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


def to_blocks(src):
    src = src.replace("<!--RELATED-->", related_box())
    out = []
    pattern = r"<blockquote[^>]*>.*?</blockquote>|<div[^>]*>.*?</div>|<(p|h2|h3|table|ul)>(.*?)</\1>|<hr>"
    for m in re.finditer(pattern, src, re.S):
        whole, tag, inner = m.group(0), m.group(1), m.group(2)
        if whole.startswith("<blockquote"):
            out.append(
                "<!-- wp:html -->\n" + whole
                + '\n<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n<!-- /wp:html -->'
            )
        elif whole.startswith("<div"):
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
            if "&#10003;" in inner:
                out.append(
                    "<!-- wp:html -->\n"
                    '<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">'
                    f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">この記事のまとめ</p>'
                    f'<ul style="margin:0;padding:14px 18px 14px 34px;background:#f7f7f7;">{items}</ul></div>\n<!-- /wp:html -->'
                )
            else:
                out.append(
                    "<!-- wp:html -->\n"
                    f'<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f7f7;">'
                    f'<ul style="margin:0;padding-left:1.2em;">{inner}</ul></div>\n<!-- /wp:html -->'
                )
    return "\n\n".join(out)


def main():
    content = to_blocks((ROOT / "articles" / f"{BASE}.html").read_text(encoding="utf-8"))
    plain = re.sub(r"<[^>]+>|<!--.*?-->", "", content, flags=re.S)
    print(f"title={len(TITLE)}字 body≈{len(re.sub(r'\s', '', plain))}字")
    if "--dry" in sys.argv:
        (ROOT / "tmp_vivant_seiyu_blocks.html").write_text(content, encoding="utf-8")
        return

    ids = json.loads(ID_FILE.read_text(encoding="utf-8")) if ID_FILE.exists() else {}
    payload = {"content": content, "status": "draft"}
    if ids:
        endpoint = f"{WP_URL}/wp-json/wp/v2/posts/{ids['id']}"
    else:
        eyecatch = ROOT / "images" / f"{BASE}_eyecatch.png"
        subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_chomoand0.py"), "--title", TITLE, "--out", str(eyecatch)],
                       check=True, env={**os.environ, "PYTHONUTF8": "1"})
        r = requests.post(
            f"{WP_URL}/wp-json/wp/v2/media",
            headers={**HEADERS_AUTH, "Content-Type": "image/png",
                     "Content-Disposition": f'attachment; filename="{BASE}_eyecatch.png"'},
            data=eyecatch.read_bytes(),
        )
        r.raise_for_status()
        payload.update({"title": TITLE, "slug": SLUG, "featured_media": r.json()["id"],
                        "categories": [37], "author": 4})
        endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
    r = requests.post(endpoint, headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    post = r.json()
    ids = {"id": post["id"], "media": post["featured_media"], "slug": post.get("slug") or SLUG}
    ID_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"POST_ID {post['id']} STATUS {post['status']} MEDIA {post['featured_media']} SLUG {ids['slug']}")


if __name__ == "__main__":
    main()
