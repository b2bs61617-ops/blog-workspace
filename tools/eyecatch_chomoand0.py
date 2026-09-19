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
import math
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


# 文字の最大サイズ(実際のサイズはブラウザ側で幅+縦の両方に収まるまで自動フィットさせる)。
# 2026-09-17: トモキ指示「文字サイズを全て2倍に」で底上げ(旧: top56/bottom60/main 130,110,90)。
# 幅基準の自動フィットだけだと2倍にしても結局同じ幅で頭打ちになるため、FIT_WIDTH/FIT_HEIGHTも
# キャンバスいっぱいまで広げて実際に大きく見えるようにした。
MAX_SIZE_TOP = 112
MAX_SIZE_BOTTOM = 120
FIT_WIDTH = 1140  # テキストを収める横幅(左右余白を約30pxに縮小)
FIT_HEIGHT = 560  # 全要素合計の縦幅上限(上下余白を約35pxに縮小)。超えたら全体を比率で縮小する
# 行数が多いほど1行あたりの文字量は減るため、行数に応じて上限だけ変える(実サイズはfitで決まる)
MAIN_MAX_BY_LINES = {1: 260, 2: 220, 3: 190, 4: 170}
MAIN_MAX_DEFAULT = 150

# 背景のパステルblobに文字が重なっても読めるよう、白いグロー(縁取り)でコントラストを上げる(2026-09-17〜)
TEXT_GLOW = (
    "0 0 10px rgba(255,255,255,0.95), 0 0 22px rgba(255,255,255,0.85), "
    "0 0 2px rgba(255,255,255,0.95)"
)


def wrap_title(title: str, max_lines: int = 4) -> list[str]:
    """記事タイトルをそのまま使う用に、行数をタイトルの長さから自動算出してバランス良く改行する.

    1行に収める文字数が多すぎると自動フィットで文字が小さくなるため、
    「幅の制約」と「縦の制約」がだいたい釣り合う行数(概ねsqrt(文字数)に比例)を狙う。
    句読点や記号の直後で切れるように、目標の切れ目付近から後方に探索する。
    """
    title = title.strip()
    n = len(title)
    if n == 0:
        return [title]
    ideal_lines = max(1, min(max_lines, round(math.sqrt(0.4 * n))))
    if ideal_lines == 1:
        return [title]

    chunk_len = math.ceil(n / ideal_lines)
    break_chars = "、。！？!?　 ・"
    radius = 6

    def is_word_char(ch: str) -> bool:
        return ch.isascii() and ch.isalnum()

    def candidates(target: int, limit: int):
        # 目標の切れ目(target)に近い位置から順に試す(target, target-1, target+1, target-2, ...)
        yield target
        for delta in range(1, radius + 1):
            if target - delta >= 0:
                yield target - delta
            if target + delta < limit:
                yield target + delta

    lines: list[str] = []
    remaining = title
    while remaining:
        if len(remaining) <= chunk_len:
            lines.append(remaining)
            break
        best = -1
        # 1) 句読点・記号の直後を、目標の切れ目に近い順に優先
        for i in candidates(chunk_len - 1, len(remaining)):
            if remaining[i] in break_chars:
                best = i
                break
        # 2) 見つからなければ、英数字の単語(ブランド名など)の途中を避けて探す
        if best == -1:
            for i in candidates(chunk_len - 1, len(remaining) - 1):
                if not (is_word_char(remaining[i]) and is_word_char(remaining[i + 1])):
                    best = i
                    break
        if best == -1:
            best = chunk_len - 1
        lines.append(remaining[: best + 1])
        remaining = remaining[best + 1 :]
    return lines


def build_html(
    top: str,
    main: str,
    bottom_lines: list[str],
    seed: int | None = None,
    color_key: str | None = None,
    title: str | None = None,
) -> str:
    """アイキャッチのHTMLを組み立てる(副作用なし).

    title を指定すると top/main/bottom は無視し、記事タイトルをそのまま
    (自動改行のみ加えて)大きく1ブロックで表示する(2026-09-17〜、トモキ指示)。

    title 未指定時は従来通り: main は "|" 区切りで複数行に分けられる
    (例: "橋本将生|猪俣周杜|篠塚大輝")。区切り指定がない場合はブラウザの自動改行に任せる。

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

    if title:
        top_html = ""
        bottom_html = ""
        main_lines = wrap_title(title)
    else:
        top_html = (
            f'<div class="fit top-text" data-max="{MAX_SIZE_TOP}">{html_mod.escape(top)}</div>'
            if top
            else ""
        )
        bottom_html = ""
        if bottom_lines:
            lines = "<br>".join(html_mod.escape(line) for line in bottom_lines)
            bottom_html = f'<div class="fit bottom-text" data-max="{MAX_SIZE_BOTTOM}">{lines}</div>'
        main_lines = main.split("|")

    main_html_text = "<br>".join(html_mod.escape(line) for line in main_lines)
    main_max_size = MAIN_MAX_BY_LINES.get(len(main_lines), MAIN_MAX_DEFAULT)

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
.fit {{ position: relative; z-index: 1; white-space: nowrap; text-align: center; text-shadow: {TEXT_GLOW}; }}
.top-text {{ font-weight: 700; color: {SUB_TEXT_COLOR}; letter-spacing: 0.1em; line-height: 1.3; }}
.name {{ font-weight: 900; color: {TEXT_COLOR}; letter-spacing: 0.04em; line-height: 1.25; }}
.bottom-text {{ font-weight: 700; color: {SUB_TEXT_COLOR}; letter-spacing: 0.05em; line-height: 1.5; }}
</style>
</head>
<body>
<div class="container">
  <div class="blob1"></div>
  <div class="blob2"></div>
  {top_html}
  <div class="fit name" data-max="{main_max_size}">{main_html_text}</div>
  {bottom_html}
</div>
<script>
// 各行を横幅いっぱい({FIT_WIDTH}px)まで拡大する(KO1KEYZ/chomoand.comテンプレと同じ自動フィット)
document.fonts.ready.then(() => {{
  const fitEls = [...document.querySelectorAll('.fit')];
  for (const el of fitEls) {{
    const max = parseInt(el.dataset.max, 10);
    let size = max;
    el.style.fontSize = size + 'px';
    while (size > 20 && el.getBoundingClientRect().width > {FIT_WIDTH}) {{
      size -= 2;
      el.style.fontSize = size + 'px';
    }}
  }}
  // 幅基準でも縦にはみ出すことがある(2026-09-17〜、最大サイズを引き上げたため追加)。
  // 合計の高さがFIT_HEIGHTを超えたら、全要素のフォントサイズを同じ比率で縮小する。
  const gap = 20;
  let totalHeight = fitEls.reduce((sum, el) => sum + el.getBoundingClientRect().height, 0);
  totalHeight += gap * Math.max(0, fitEls.length - 1);
  if (totalHeight > {FIT_HEIGHT}) {{
    const ratio = {FIT_HEIGHT} / totalHeight;
    for (const el of fitEls) {{
      const current = parseFloat(el.style.fontSize);
      el.style.fontSize = Math.max(20, Math.floor(current * ratio)) + 'px';
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

    out_path = Path(out_path).resolve()
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
    parser = argparse.ArgumentParser(description="chomoand-0.com汎用アイキャッチ生成")
    parser.add_argument("--top", default="", help="上段の番組名・所属など(--title指定時は無視)")
    parser.add_argument("--main", help="中央の人物名・主役テキスト(--title指定時は無視)")
    parser.add_argument("--bottom", action="append", default=[], help="下段(複数指定で複数行、--title指定時は無視)")
    parser.add_argument(
        "--title",
        default=None,
        help="記事タイトルをそのまま自動改行して大きく1ブロックで表示する(指定時は--top/--main/--bottomを無視)",
    )
    parser.add_argument("--out", required=True, help="出力PNGパス")
    parser.add_argument("--seed", type=int, default=None, help="色パターンを固定する乱数シード")
    parser.add_argument(
        "--color-key",
        default=None,
        choices=sorted(TRAVIS_JAPAN_COLORS),
        help="Travis Japanメンバーカラー(個人記事はメンバー名、グループ記事は'group')を固定で使う",
    )
    args = parser.parse_args()
    if not args.title and not args.main:
        parser.error("--title か --main のどちらかを指定してください")

    path = render(
        build_html(args.top, args.main or "", args.bottom, args.seed, args.color_key, args.title),
        Path(args.out),
    )
    print(f"done: {path}")


if __name__ == "__main__":
    main()
