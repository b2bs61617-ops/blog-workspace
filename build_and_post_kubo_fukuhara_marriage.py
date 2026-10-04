# -*- coding: utf-8 -*-
"""久保建英×福原遥 結婚(2026-10-02発表) 6記事 -> chomoand.com 下書き投稿.

articles/kubo_fukuhara_0X_*.html を Gutenberg ブロックへ変換し、
アイキャッチ(tools/eyecatch_chomoand0.py --title)を作ってアップロード、下書きで投稿する。
<!--RELATED--> は他5記事への関連記事boxに置き換える。
再実行時は tmp_kubo_fukuhara_ids.json の記事IDを更新する(title/slugは送らない)。
"""
import base64, json, os, re, socket, subprocess, sys
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
IDS_FILE = ROOT / "tmp_kubo_fukuhara_ids.json"
# docs/wordpress.md の投稿者表(chomoand.com): USER1=momo(3) / Tomoki=and(4)
AUTHOR = 3 if socket.gethostname().upper() == "USER1" else 4

ARTICLES = [
    ("kubo_fukuhara_01_naresome", "久保建英と福原遥の馴れ初めは？1〜2年の猛アタックで結婚！",
     "kubo-fukuhara-how-they-met", "久保建英と福原遥の馴れ初め・交際の流れ"),
    ("kubo_fukuhara_02_kubo_kanojo", "久保建英の歴代彼女は誰？噂の女性まとめと福原遥が初の公認に！",
     "takefusa-kubo-ex-girlfriends", "久保建英の歴代彼女と噂の真相"),
    ("kubo_fukuhara_03_fukuhara_kareshi", "福原遥の歴代彼氏は誰？噂の共演者5人と久保建英との結婚！",
     "haruka-fukuhara-ex-boyfriends", "福原遥の歴代彼氏と噂の共演者5人"),
    ("kubo_fukuhara_04_hiduke_riyu", "久保建英と福原遥の結婚発表日は10月3日？この日を選んだ理由！",
     "kubo-fukuhara-marriage-date-reason", "久保建英と福原遥が結婚発表日を選んだ理由"),
    ("kubo_fukuhara_05_yubiwa", "久保建英と福原遥の結婚指輪の価格は？ブランドと値段を予想！",
     "kubo-fukuhara-wedding-ring-price", "久保建英と福原遥の結婚指輪の価格・ブランド予想"),
    ("kubo_fukuhara_06_kubo_nenshu", "久保建英の年収はいくら？年俸9億円超+CMで推定総額を計算！",
     "takefusa-kubo-annual-income", "久保建英の年収・年俸の内訳"),
    ("kubo_fukuhara_07_yubiwa_brand", "久保建英と福原遥の結婚指輪のブランドは？ブルガリのフェディか！",
     "kubo-fukuhara-wedding-ring-brand", "久保建英と福原遥の結婚指輪のブランド(ブルガリ「フェディ」説)"),
]


def related_box(self_slug):
    items = "".join(
        f'<li><a href="{WP_URL}/{slug}/">{anchor}</a></li>'
        for _, _, slug, anchor in ARTICLES if slug != self_slug
    )
    return (
        f'<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f7f7;">'
        '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">久保建英と福原遥の結婚 関連記事</p>'
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
    pattern = r"<div[^>]*>.*?</div>|<iframe[^>]*>.*?</iframe>|<(p|h2|h3|table|ul)>(.*?)</\1>|<hr>"
    for m in re.finditer(pattern, src, re.S):
        whole, tag, inner = m.group(0), m.group(1), m.group(2)
        if whole.startswith(("<div", "<iframe")):
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
                            "status": "draft", "categories": [37], "author": AUTHOR})
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
