"""ジャニオタブログ(chomoand-0.com)汎用アイキャッチ生成ツール.

docs/eyecatch-style.md の「汎用テンプレ(chomoand-0.com / chomoand.comのフォールバック用)」を
HTML+Playwrightで再現する。1200x630px、人物名を中央に超大きく、
グラデーションblobの背景(色は毎回ランダム。ただしTravis Japan記事は--color-keyで固定可)。

使い方:
    python tools/eyecatch_chomoand0.py \
        --top "timelesz" \
        --main "橋本将生・猪俣周杜・篠塚大輝" \
        --bottom "『土曜はナニする!?』日帰り旅" \
        --bottom "ロケ地はどこ?" \
        --out images/timelesz_donani_eyecatch.png

--bottom は複数指定で複数行になる。--seed で色パターンを固定できる(未指定ならランダム)。
Travis Japanの記事は --color-key "松倉海斗" のようにメンバー名(個人記事)/"group"(グループ記事)
を指定すると、メンバーカラーのパステル配色で固定される(docs/eyecatch-style.md参照)。
"""

from __future__ import annotations

import argparse
import html as html_mod
import random
from pathlib import Path

CANVAS_W = 1200
CANVAS_H = 630

BASE_BG = "#f5f0eb"
TEXT_COLOR = "#1a1a1a"
SUB_TEXT_COLOR = "#2d2d2d"

# docs/eyecatch-style.md記載の色パターン例(2色1組でランダムに選ぶ)
COLOR_PAIRS = [
    ("rgba(179,157,219,0.7)", "rgba(144,202,249,0.6)"),  # 紫×青
    ("rgba(255,183,77,0.7)", "rgba(239,154,154,0.6)"),  # オレンジ×珊瑚
    ("rgba(165,214,167,0.7)", "rgba(128,203,196,0.6)"),  # 緑×ティール
    ("rgba(239,154,154,0.7)", "rgba(206,147,216,0.6)"),  # 赤×ピンク
    ("rgba(255,238,88,0.7)", "rgba(197,225,165,0.6)"),  # 黄×ライム
    ("rgba(255,204,188,0.7)", "rgba(179,157,219,0.6)"),  # ピーチ×ラベンダー
]

# Travis Japanメンバーカラー(公式カラーをパステル調に薄めたもの)。
# 個人記事は該当メンバー名、グループ全体の記事は "group"(グループカラーの紫)を --color-key に指定する。
# 2026-08-09にユーザー指示: 現職の強い色味ではなく見やすい/おしゃれなパステル調にすること。
TRAVIS_JAPAN_COLORS: dict[str, tuple[str, str, str]] = {
    "宮近海斗": ("rgba(239,154,154,0.65)", "rgba(255,205,178,0.55)", "rgba(239,154,154,0.5)"),  # 赤
    "中村海人": ("rgba(165,214,167,0.65)", "rgba(200,230,201,0.55)", "rgba(165,214,167,0.5)"),  # 緑
    "七五三掛龍也": ("rgba(248,187,208,0.65)", "rgba(255,205,210,0.55)", "rgba(248,187,208,0.5)"),  # ピンク
    "川島如恵留": ("rgba(224,224,224,0.6)", "rgba(207,216,220,0.5)", "rgba(224,224,224,0.45)"),  # 白(シルバーグレー)
    "吉澤閑也": ("rgba(255,241,118,0.6)", "rgba(255,249,196,0.5)", "rgba(255,241,118,0.45)"),  # 黄
    "松田元太": ("rgba(144,202,249,0.65)", "rgba(179,229,252,0.55)", "rgba(144,202,249,0.5)"),  # 青
    "松倉海斗": ("rgba(255,204,128,0.65)", "rgba(255,224,178,0.55)", "rgba(255,204,128,0.5)"),  # オレンジ
    "group": ("rgba(179,157,219,0.65)", "rgba(206,190,234,0.55)", "rgba(179,157,219,0.5)"),  # グループカラー(紫)
}


def build_html(
    top: str,
    main: str,
    bottom_lines: list[str],
    seed: int | None = None,
    color_key: str | None = None,
) -> str:
    """アイキャッチのHTMLを組み立てる(副作用なし).

    main は "|" 区切りで複数行に分けられる(例: "橋本将生|猪俣周杜|篠塚大輝")。
    区切り指定がない場合はブラウザの自動改行に任せる。

    color_key を指定すると TRAVIS_JAPAN_COLORS の固定配色を使う(未指定ならランダム)。
    """
    if color_key:
        if color_key not in TRAVIS_JAPAN_COLORS:
            known = ", ".join(TRAVIS_JAPAN_COLORS)
            raise ValueError(f"unknown color_key: {color_key!r} (known: {known})")
        color1, color2, color3 = TRAVIS_JAPAN_COLORS[color_key]
    else:
        rng = random.Random(seed)
        color1, color2 = rng.choice(COLOR_PAIRS)
        color3, _ = rng.choice(COLOR_PAIRS)

    top_html = f'<div class="top-text">{html_mod.escape(top)}</div>' if top else ""
    bottom_html = ""
    if bottom_lines:
        lines = "<br>".join(html_mod.escape(line) for line in bottom_lines)
        bottom_html = f'<div class="bottom-text">{lines}</div>'

    main_lines = main.split("|")
    main_html_text = "<br>".join(html_mod.escape(line) for line in main_lines)
    # 行数が多いほど1行あたりの文字量は減るため、行数に応じて最大フォントサイズを調整する
    main_max_size = {1: 100, 2: 92}.get(len(main_lines), 78)

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: {CANVAS_W}px; height: {CANVAS_H}px; overflow: hidden;
  font-family: 'Yu Gothic', 'Meiryo', 'Hiragino Kaku Gothic ProN', sans-serif; }}
.container {{
  width: {CANVAS_W}px; height: {CANVAS_H}px;
  background: {BASE_BG};
  position: relative;
  display: flex; flex-direction: column;
  justify-content: center; align-items: center; gap: 20px;
  overflow: hidden;
}}
.blob1 {{
  position: absolute; width: 700px; height: 700px; border-radius: 50%;
  background: radial-gradient(circle, {color1} 0%, {color2} 40%, transparent 70%);
  opacity: 0.55; right: -150px; top: -150px; filter: blur(55px);
}}
.blob2 {{
  position: absolute; width: 400px; height: 400px; border-radius: 50%;
  background: radial-gradient(circle, {color3} 0%, transparent 70%);
  opacity: 0.4; left: -80px; bottom: -80px; filter: blur(40px);
}}
.top-text {{ font-size: 44px; font-weight: 700; color: {SUB_TEXT_COLOR}; letter-spacing: 0.1em; z-index: 1; text-align: center; }}
.name {{ font-size: {main_max_size}px; font-weight: 900; color: {TEXT_COLOR}; letter-spacing: 0.04em; z-index: 1; text-align: center; line-height: 1.3; max-width: 1080px; }}
.bottom-text {{ font-size: 46px; font-weight: 700; color: {SUB_TEXT_COLOR}; letter-spacing: 0.05em; z-index: 1; text-align: center; line-height: 1.6; }}
</style>
</head>
<body>
<div class="container">
  <div class="blob1"></div>
  <div class="blob2"></div>
  {top_html}
  <div class="name">{main_html_text}</div>
  {bottom_html}
</div>
</body>
</html>
"""


def render(html_text: str, out_path: Path) -> Path:
    """HTMLをPNGに書き出す."""
    from playwright.sync_api import sync_playwright

    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    html_path = out_path.with_suffix(".html")
    html_path.write_text(html_text, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H})
        page.goto(html_path.as_uri())
        page.screenshot(path=str(out_path))
        browser.close()
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="chomoand-0.com汎用アイキャッチ生成")
    parser.add_argument("--top", default="", help="上段の番組名・所属など")
    parser.add_argument("--main", required=True, help="中央の人物名・主役テキスト")
    parser.add_argument("--bottom", action="append", default=[], help="下段(複数指定で複数行)")
    parser.add_argument("--out", required=True, help="出力PNGパス")
    parser.add_argument("--seed", type=int, default=None, help="色パターンを固定する乱数シード")
    parser.add_argument(
        "--color-key",
        default=None,
        choices=sorted(TRAVIS_JAPAN_COLORS),
        help="Travis Japanメンバーカラー(個人記事はメンバー名、グループ記事は'group')を固定で使う",
    )
    args = parser.parse_args()

    path = render(
        build_html(args.top, args.main, args.bottom, args.seed, args.color_key),
        Path(args.out),
    )
    print(f"done: {path}")


if __name__ == "__main__":
    main()
