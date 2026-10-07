# -*- coding: utf-8 -*-
"""水ダウ2・ポリティカルパン2・小麦とバターと復讐と2(2026-10-07) -> chomoand.com 下書き投稿.

articles/*_1007.html を Gutenberg ブロックへ変換し、
アイキャッチ(tools/eyecatch_chomoand0.py --title)を作ってアップロード、公開で投稿する。
<!--RELATED--> は2記事の相互リンクboxに置換。
再実行時は tmp_trend_1007_ids.json の記事IDを更新する(title/slugは送らない)。
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
IDS_FILE = ROOT / "tmp_trend_1007_ids.json"

ARTICLES = [
    ("suidau_kakushi_guest_1007", "水ダウの隠しゲスト「？」は誰？佐藤綺星？なぜ隠した？", "suiyobi-downtown-kakushi-guest-who", "水ダウの隠しゲスト「？」は誰？", "s"),
    ("maskman_tabi4_kuromask_1007", "マスクマン旅第4弾の黒マスクは誰？正体と全結果まとめ！", "maskman-tabi-4-kuro-mask-who", "マスクマン旅第4弾の黒マスクの正体予想", "s"),
    ("political_lupin_meaning_1007", "ポリティカルパンの意味は？どこで区切る？タヌキの声は誰？", "political-lupin-meaning-tanuki-voice", "ポリティカルパンの意味とタヌキの声", "p"),
    ("kawanishi_political_lupin_1007", "JO1川西拓実はポリティカルパンで何役？銀二の役どころは？", "kawanishi-takumi-political-lupin-ginji", "川西拓実が演じる花園銀二の役どころ", "p"),
    ("komugi_recipe_memory_1007", "小麦とバターと復讐とのレシピはなぜ消えた？思い出す方法は？", "komugi-butter-fukushu-recipe-memory", "ミチルのレシピが消えた理由と思い出す方法", "k"),
    ("komugi_gensaku_ketsumatsu_1007", "小麦とバターと復讐との原作は？伊能先生とミチルの結末は？", "komugi-butter-fukushu-gensaku-ketsumatsu", "小麦とバターと復讐との原作と結末", "k"),
]
EXTRA = {}


def related_box(self_slug):
    grp = next(g for _, _, s, _, g in ARTICLES if s == self_slug)
    links = [(s, a) for _, _, s, a, g in ARTICLES if g == grp and s != self_slug] + EXTRA.get(grp, [])
    items = "".join(f'<li><a href="{WP_URL}/{slug}/">{anchor}</a></li>' for slug, anchor in links)
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
    for base, title, slug, _, _ in ARTICLES:
        if only and base not in only:
            continue
        content = to_blocks((ROOT / "articles" / f"{base}.html").read_text(encoding="utf-8"), slug)
        plain = re.sub(r"<[^>]+>|<!--.*?-->", "", content, flags=re.S)
        print(f"[{base}] title={len(title)}字 body≈{len(re.sub(r'\s', '', plain))}字")

        payload = {"content": content, "status": "draft"}
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
                            "status": "draft", "categories": [37], "author": 4})
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
