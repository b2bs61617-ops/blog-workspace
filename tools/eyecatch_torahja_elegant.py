"""chomoand-4.blog(Travis Japan)用アイキャッチ「エレガント版」.

2026-09-22〜、トモキが「もっとおしゃれな感じにしたい」と添付した参考画像を再現するツール。
極太丸ゴシック+ビビッドな3行デザイン(tools/eyecatch_torahja.py)とは別系統で、
細めのセリフ/サンセリフ+淡いグラデーション背景の上品なテイスト。

- 上段/下段: Noto Sans JP Light(細め・字間広め)
- 中央: Cormorant Garamond(英字エレガントセリフ)。日本語を渡すとNoto Sans JPで代替表示。
- 背景: 淡いラベンダー×クリームのグラデーション(--hueで色相を回せる)

使い方:
    python tools/eyecatch_torahja_elegant.py \
        --top "コストコ食材で作った" \
        --main "Travis Japan" \
        --bottom "全9品は？レシピも！" \
        --out images/xxx_eyecatch.png
"""

from __future__ import annotations

import argparse
import html as html_mod
import random
import re
from pathlib import Path

CANVAS_W = 1200
CANVAS_H = 630
REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_SERIF = REPO_ROOT / "assets" / "fonts" / "CormorantGaramond-Regular.ttf"
FONT_SANS_LIGHT = REPO_ROOT / "assets" / "fonts" / "NotoSansJP-Light.ttf"
FONT_SANS_REGULAR = REPO_ROOT / "assets" / "fonts" / "NotoSansJP-Regular.ttf"

MAX_SIZE_TOP = 34
MAX_SIZE_MAIN = 150
MAX_SIZE_BOTTOM = 36
FIT_WIDTH = 1000

# 日本語(かな/漢字)が含まれるかどうか(--mainをセリフ体で組むかの判定に使う)
_JP_RE = re.compile(r"[぀-ヿ一-鿿]")


def build_html(
    top: str,
    main: str,
    bottom: str,
    hue: int | None = None,
) -> str:
    """アイキャッチのHTMLを組み立てる(副作用なし)."""
    rng = random.Random()
    hue_deg = hue if hue is not None else rng.randint(-18, 18)
    main_is_jp = bool(_JP_RE.search(main))
    main_font = "'SansL'" if main_is_jp else "'Serif'"

    top_html = f'<div class="fit top" data-max="{MAX_SIZE_TOP}">{html_mod.escape(top)}</div>' if top else ""
    bottom_html = (
        f'<div class="fit bottom" data-max="{MAX_SIZE_BOTTOM}">{html_mod.escape(bottom)}</div>' if bottom else ""
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
@font-face {{ font-family: 'Serif'; src: url('{FONT_SERIF.as_uri()}') format('truetype'); font-weight: 400; }}
@font-face {{ font-family: 'SansL'; src: url('{FONT_SANS_LIGHT.as_uri()}') format('truetype'); font-weight: 300; }}
@font-face {{ font-family: 'SansR'; src: url('{FONT_SANS_REGULAR.as_uri()}') format('truetype'); font-weight: 400; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: {CANVAS_W}px; height: {CANVAS_H}px; overflow: hidden; }}
.stage {{
  position: relative; width: {CANVAS_W}px; height: {CANVAS_H}px; overflow: hidden;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 34px;
  background: linear-gradient(135deg, #fdfcfb 0%, #fbf9fa 45%, #f9f7f9 100%);
  filter: hue-rotate({hue_deg}deg);
}}
.blob {{ position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.28; }}
.b1 {{ width: 620px; height: 620px; left: -220px; top: -260px; background: #e3c9e8; }}
.b2 {{ width: 560px; height: 560px; right: -200px; bottom: -240px; background: #f4d9c6; }}
.b3 {{ width: 420px; height: 420px; left: 34%; top: 20%; background: #ffffff; opacity: 0.6; }}
.frame {{ position: absolute; inset: 26px; border: 1px solid rgba(60,50,60,0.16); }}
.fit {{ position: relative; z-index: 1; white-space: nowrap; color: #4f4a46; font-family: 'SansL', sans-serif; font-weight: 300; letter-spacing: 0.32em; text-indent: 0.32em; }}
.main {{ position: relative; z-index: 1; white-space: nowrap; color: #2c2622; font-family: {main_font}, 'SansR', sans-serif; letter-spacing: 0.05em; font-weight: 400; }}
</style>
</head>
<body>
<div class="stage">
  <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
  <div class="frame"></div>
  {top_html}
  <div class="fit main" data-max="{MAX_SIZE_MAIN}">{html_mod.escape(main)}</div>
  {bottom_html}
</div>
<script>
document.fonts.ready.then(() => {{
  for (const el of document.querySelectorAll('.fit')) {{
    const max = parseInt(el.dataset.max, 10);
    let size = max;
    el.style.fontSize = size + 'px';
    while (size > 14 && el.getBoundingClientRect().width > {FIT_WIDTH}) {{
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
    from playwright.sync_api import sync_playwright

    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    html_path = out_path.with_suffix(".html")
    html_path.write_text(html_text, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H})
        page.goto(html_path.as_uri())
        page.wait_for_selector("body[data-fitted='1']")
        page.screenshot(path=str(out_path))
        browser.close()
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="chomoand-4.blog(Travis Japan)アイキャッチ エレガント版")
    ap.add_argument("--top", default="", help="上段(小さめ・細字)")
    ap.add_argument("--main", required=True, help="中央の主役テキスト(英字はセリフ体、日本語はサンセリフで表示)")
    ap.add_argument("--bottom", default="", help="下段(小さめ・細字)")
    ap.add_argument("--hue", type=int, default=None, help="背景の色相回転角(-18〜18程度)を固定する場合に指定")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    html_text = build_html(args.top, args.main, args.bottom, args.hue)
    print(f"done: {render(html_text, Path(args.out))}")


if __name__ == "__main__":
    main()
