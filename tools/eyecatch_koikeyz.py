"""KO1KEYZブログ(chomoand-1.com)統一アイキャッチ生成ツール.

Canvaの「Webinar/Keynote Presentation」テンプレで作られた既存アイキャッチと
同じ見た目(16:9・オフホワイト+パステルスモーク背景・極太丸ゴシック黒文字・センター揃え)を
HTML+Playwrightで再現する。

使い方:
    python tools/eyecatch_koikeyz.py \
        --top "ファンミーティングの会場は?" \
        --main "KO1KEYZ" \
        --bottom "アクセスや会場のキャパを調査!" \
        --out images/ko1keyz_xxx_eyecatch.png

--bottom は複数指定で複数行になる。--seed を固定すると背景の滲みが毎回同じになる。
"""

from __future__ import annotations

import argparse
import html as html_mod
import random
from pathlib import Path

CANVAS_W = 1200
CANVAS_H = 675  # 16:9(既存アイキャッチと同じ比率)

REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = REPO_ROOT / "assets" / "fonts" / "MPLUSRounded1c-Black.ttf"

# 背景のパステルスモーク(既存テンプレの配色。統一感のため色は固定し、位置だけ揺らす)
SMOKE_COLORS = [
    "rgba(240,150,160,0.95)",  # ピンク
    "rgba(246,178,130,0.85)",  # サーモン/オレンジ
    "rgba(196,165,220,0.80)",  # ラベンダー
    "rgba(186,214,170,0.70)",  # ペールグリーン
    "rgba(250,205,205,0.85)",  # ベビーピンク
]

BASE_BG = "#f2efe9"  # オフホワイト/クリーム
TEXT_COLOR = "#1c1c1c"

# 文字の最大サイズ(実際のサイズはブラウザ側で幅いっぱいまで自動フィットさせる)
MAX_SIZE_TOP = 90
MAX_SIZE_MAIN = 200
MAX_SIZE_BOTTOM = 78
FIT_WIDTH = 1090  # テキストを収める横幅(左右に少し余白)


def build_html(top: str, main: str, bottom_lines: list[str], seed: int | None = None) -> str:
    """アイキャッチのHTMLを組み立てる(副作用なし)."""
    rng = random.Random(seed)

    blobs = []
    for color in SMOKE_COLORS:
        # 中央に寄せて重ねる(実テンプレは中央にスモークが集まり、四隅は無地のクリーム)
        size = rng.randint(420, 640)
        cx = rng.randint(430, 770)
        cy = rng.randint(230, 450)
        blobs.append(
            f'<div class="smoke" style="width:{size}px;height:{size}px;'
            f"left:{cx - size // 2}px;top:{cy - size // 2}px;"
            f'background:radial-gradient(circle,{color} 0%,transparent 66%);"></div>'
        )

    top_html = (
        f'<div class="fit top" data-max="{MAX_SIZE_TOP}">{html_mod.escape(top)}</div>'
        if top
        else ""
    )
    bottom_html = ""
    if bottom_lines:
        lines = "<br>".join(html_mod.escape(line) for line in bottom_lines)
        bottom_html = f'<div class="fit bottom" data-max="{MAX_SIZE_BOTTOM}">{lines}</div>'

    font_url = FONT_PATH.as_uri()

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
@font-face {{
  font-family: 'KoikeyzRounded';
  src: url('{font_url}') format('truetype');
  font-weight: 900;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: {CANVAS_W}px; height: {CANVAS_H}px; overflow: hidden; }}
.canvas {{
  position: relative;
  width: {CANVAS_W}px; height: {CANVAS_H}px;
  background: {BASE_BG};
  overflow: hidden;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 24px;
  font-family: 'KoikeyzRounded', 'Yu Gothic', sans-serif;
  font-weight: 900;
  color: {TEXT_COLOR};
  text-align: center;
}}
.smoke {{ position: absolute; border-radius: 50%; filter: blur(80px); }}
.fit {{ position: relative; z-index: 1; white-space: nowrap; line-height: 1.35; }}
.main {{ letter-spacing: 0.02em; line-height: 1.05; }}
</style>
</head>
<body>
<div class="canvas">
  {''.join(blobs)}
  {top_html}
  <div class="fit main" data-max="{MAX_SIZE_MAIN}">{html_mod.escape(main)}</div>
  {bottom_html}
</div>
<script>
// 各行を横幅いっぱい({FIT_WIDTH}px)まで拡大する(Canvaテンプレの「文字が画面いっぱい」の質感を再現)
document.fonts.ready.then(() => {{
  for (const el of document.querySelectorAll('.fit')) {{
    const max = parseInt(el.dataset.max, 10);
    let size = max;
    el.style.fontSize = size + 'px';
    while (size > 20 && el.getBoundingClientRect().width > {FIT_WIDTH}) {{
      size -= 2;
      el.style.fontSize = size + 'px';
    }}
  }}
  document.body.dataset.fitted = '1';
}});
</script>
</body>
</html>
"""


def render(html_text: str, out_path: Path) -> Path:
    """HTMLをPNGに書き出す."""
    from playwright.sync_api import sync_playwright

    out_path = Path(out_path).resolve()  # file:// URIにするため絶対パス化
    out_path.parent.mkdir(parents=True, exist_ok=True)
    html_path = out_path.with_suffix(".html")
    html_path.write_text(html_text, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H})
        page.goto(html_path.as_uri())
        page.wait_for_selector("body[data-fitted='1']")  # フォント読込+文字サイズ自動フィット完了待ち
        page.screenshot(path=str(out_path))
        browser.close()
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="KO1KEYZブログ統一アイキャッチ生成")
    parser.add_argument("--top", default="", help="上段の問いかけ・所属など")
    parser.add_argument("--main", required=True, help="中央の主役テキスト(グループ名・人物名)")
    parser.add_argument("--bottom", action="append", default=[], help="下段(複数指定で複数行)")
    parser.add_argument("--out", required=True, help="出力PNGパス")
    parser.add_argument("--seed", type=int, default=None, help="背景の滲みを固定する乱数シード")
    args = parser.parse_args()

    path = render(build_html(args.top, args.main, args.bottom, args.seed), Path(args.out))
    print(f"done: {path}")


if __name__ == "__main__":
    main()
