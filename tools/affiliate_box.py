# -*- coding: utf-8 -*-
"""記事の主役の商品に「商品写真+楽天/Amazonボタン」の枠(アフィリエイト)を作る(2026-11-11〜 全サイト、ユカ指示).

楽天商品検索APIで候補を出し、選んだ候補の写真(楽天の商品画像)とアフィリエイトURLで、
WordPressにそのまま貼れる <!-- wp:html --> ブロックを出力する。Amazonは検索結果ページへのリンク。
キーはローカル.env → 空ならGoogleドライブの.env(ユカのMac)から読む。

使い方:
  python tools/affiliate_box.py "象印 炎舞炊き NX-AB10 BZ"                 # 候補一覧(番号・値段・店・商品名・画像)
  python tools/affiliate_box.py "象印 炎舞炊き NX-AB10 BZ" --pick 3 \\
      --title "象印 圧力IH炊飯ジャー 炎舞炊き NX-AB10(5.5合炊き)" \\
      --note "写真は黒(NX-AB10-BZ)。白(NX-AB10-WZ)もあります" \\
      --amazon "象印 炎舞炊き NX-AB10" --border "#f3c6d9" -o box.html   # 枠のHTMLを書き出す
  python tools/affiliate_box.py --notice    # 本文の一番上に置くPR表記(本記事はプロモーションを含みます)

候補の商品名が記事の商品と一致しているか(型番・色)は必ず目で確かめてから --pick する。
ふるさと納税・セット品・中古・別型番は選ばない。
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import affiliate_linker as al  # noqa: E402

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
DRIVE_ENV = Path(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))
KEYS = ("RAKUTEN_APP_ID", "RAKUTEN_ACCESS_KEY", "RAKUTEN_AFFILIATE_ID", "AMAZON_ASSOCIATE_TAG")
NOTICE = '<!-- wp:html -->\n<p style="font-size:12px;color:#888;">本記事はプロモーションを含みます</p>\n<!-- /wp:html -->'
SPON = 'target="_blank" rel="nofollow sponsored noopener"'
SKIP_WORDS = ("ふるさと納税", "中古", "訳あり", "セット", "レンタル")


def load_keys() -> dict:
    env = al.load_env(ROOT / ".env")
    if DRIVE_ENV.exists():
        for k, v in al.load_env(DRIVE_ENV).items():
            if k in KEYS and not env.get(k) and v:
                env[k] = v.strip("\"'")
    return env


def big_image(url: str | None, size: int = 400) -> str | None:
    """楽天の128x128サムネURLを、記事用の大きめサイズに差し替える。"""
    if not url:
        return None
    if "_ex=" in url:
        return re.sub(r"_ex=\d+x\d+", f"_ex={size}x{size}", url)
    return url + ("&" if "?" in url else "?") + f"_ex={size}x{size}"


def looks_bad(name: str) -> bool:
    return any(w in (name or "") for w in SKIP_WORDS)


def build_box(rakuten_url: str | None, image_url: str | None, title: str, amazon_url: str | None,
              note: str = "", border: str = "#dddddd", alt: str = "") -> str:
    """商品写真+ボタンの枠。楽天/Amazonどちらか片方だけでも作れる。"""
    if not (rakuten_url or amazon_url):
        raise ValueError("楽天かAmazonのどちらかのURLが要るワン")
    btn = ("display:inline-block;margin:4px;padding:10px 18px;border-radius:4px;color:#fff;"
           "font-weight:bold;text-decoration:none;")
    t = html.escape(title)
    lines = [f'<div style="border:1px solid {border};border-radius:4px;padding:16px;margin:0 0 16px 0;'
             f'background:#fff;text-align:center;">']
    if image_url:
        img = (f'<img src="{html.escape(image_url)}" alt="{html.escape(alt or title)}" width="300" height="300" '
               f'style="max-width:100%;height:auto;">')
        link = rakuten_url or amazon_url
        lines.append(f'<a href="{html.escape(link)}" {SPON}>{img}</a>')
    lines.append(f'<p style="margin:8px 0 4px 0;font-weight:bold;">{t}</p>')
    if note:
        lines.append(f'<p style="margin:0 0 8px 0;font-size:0.85em;color:#888;">{html.escape(note)}</p>')
    if rakuten_url:
        lines.append(f'<a href="{html.escape(rakuten_url)}" {SPON} style="{btn}background:#bf0000;">楽天で見る</a>')
    if amazon_url:
        lines.append(f'<a href="{html.escape(amazon_url)}" {SPON} style="{btn}background:#232f3e;">Amazonで見る</a>')
    lines.append("</div>")
    return "<!-- wp:html -->\n" + "\n".join(lines) + "\n<!-- /wp:html -->"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keyword", nargs="?")
    ap.add_argument("--hits", type=int, default=10)
    ap.add_argument("--pick", type=int, help="候補の番号(1〜)。指定すると枠のHTMLを出す")
    ap.add_argument("--title", help="枠に出す商品名(省略時は楽天の商品名)")
    ap.add_argument("--note", default="", help="商品名の下の小さい注記(色違いなど)")
    ap.add_argument("--amazon", help="Amazon検索キーワード(省略時はkeyword)。none でAmazonなし")
    ap.add_argument("--border", default="#dddddd", help="枠線の色(記事のメンバーカラーなどに合わせる)")
    ap.add_argument("-o", "--out", help="HTMLの書き出し先(省略時は画面に出す)")
    ap.add_argument("--notice", action="store_true", help="PR表記のブロックだけ出す")
    a = ap.parse_args()

    if a.notice:
        print(NOTICE)
        return
    if not a.keyword:
        ap.error("keyword が要るワン")

    env = load_keys()
    if not (env.get("RAKUTEN_APP_ID") and env.get("RAKUTEN_ACCESS_KEY")):
        print("楽天のキーが見つからないワン(.env / Googleドライブの.env)", file=sys.stderr)
        items = []
    else:
        items = al.fetch_rakuten_items(env["RAKUTEN_APP_ID"], env["RAKUTEN_ACCESS_KEY"],
                                       env.get("RAKUTEN_AFFILIATE_ID"), a.keyword, hits=a.hits)
    amazon = None
    if (a.amazon or "").lower() != "none":
        amazon = al.build_amazon_search_url(a.amazon or a.keyword, env.get("AMAZON_ASSOCIATE_TAG"))

    if a.pick is None:
        for i, c in enumerate(items, 1):
            mark = "  ×" if looks_bad(c["name"]) else ""
            print(f"[{i}] {c['price']:,}円 | {c['shop']} | {c['name'][:80]}{mark}")
            print(f"     画像: {big_image(c['image'])}")
        print(f"\nAmazon検索: {amazon}")
        print("→ 型番・色が合う候補を選んで --pick N で枠を作るワン(×=ふるさと納税・中古など選ばない)")
        return

    if not 1 <= a.pick <= len(items):
        sys.exit(f"--pick は 1〜{len(items)} で指定してワン")
    c = items[a.pick - 1]
    box = build_box(c["url"], big_image(c["image"]), a.title or c["name"], amazon, a.note, a.border)
    if a.out:
        Path(a.out).write_text(box, encoding="utf-8")
        print(f"wrote {a.out}  ({c['price']:,}円 / {c['shop']})")
    else:
        print(box)


if __name__ == "__main__":
    main()
