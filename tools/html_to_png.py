"""HTMLファイルをPNG画像に変換する汎用ツール。

アイキャッチ画像の生成に使う(docs/eyecatch-style.md の汎用テンプレ方式)。
HTMLをChromiumで開いて指定サイズでスクリーンショットを撮るだけ。

使い方:
    # 1枚だけ
    python tools/html_to_png.py images/foo_eyecatch.html

    # 複数まとめて(出力は同名の.png)
    python tools/html_to_png.py images/a_eyecatch.html images/b_eyecatch.html

    # サイズ・出力先を指定
    python tools/html_to_png.py images/foo.html --out images/bar.png --width 1200 --height 675

デフォルトは1200x630(OGP/WordPress標準)。chomoand-1.com(コイキーズ)の
アイキャッチは専用テンプレの tools/eyecatch_koikeyz.py を使うこと。
"""

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def html_to_png(html_path: Path, out_path: Path, width: int, height: int) -> None:
    """HTMLファイルを開いてPNGとして保存する。"""
    url = html_path.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(url)
        page.wait_for_timeout(300)  # webfont/blurの描画待ち
        page.screenshot(path=str(out_path))
        browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="HTMLをPNGに変換する(アイキャッチ生成用)")
    parser.add_argument("html", nargs="+", help="変換元のHTMLファイル(複数可)")
    parser.add_argument("--out", help="出力PNGパス(HTMLが1つのときのみ有効。省略時は同名.png)")
    parser.add_argument("--width", type=int, default=1200, help="幅(デフォルト1200)")
    parser.add_argument("--height", type=int, default=630, help="高さ(デフォルト630)")
    args = parser.parse_args()

    if args.out and len(args.html) > 1:
        print("ERROR: --out は変換元が1つのときのみ指定できる", file=sys.stderr)
        return 1

    for html in args.html:
        html_path = Path(html)
        if not html_path.exists():
            print(f"ERROR: ファイルが見つからない: {html_path}", file=sys.stderr)
            return 1

        out_path = Path(args.out) if args.out else html_path.with_suffix(".png")
        html_to_png(html_path, out_path, args.width, args.height)
        print(f"OK: {html_path} -> {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
