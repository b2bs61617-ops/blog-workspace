"""chomoand-4.blog(Travis Japan)アイキャッチ: 2026-09-30にCanva(design DAHWCN9D3pk)で
公開記事に適用された「水彩にじみ+グレー丸ゴシック」デザインをHTML+Playwrightで再現する。

構成(Canva版の型):
    上段(小)  : 「Travis Japan」または分類(例: 4thアルバム『Jewelry Basket』)
    中央(特大): 個人記事=メンバー名 / グループ記事=話題のキーワード
    下段(中)  : タイトルの残り1〜2行
背景: 個人記事=メンバーカラーの水彩、グループ記事=紫系の水彩。

使い方:
    python tools/eyecatch_torahja_canva.py \
        --top "Travis Japan" --main "宮近海斗" \
        --bottom "アウトレットで購入のTシャツは？" --bottom "バレンシアガと判明！" \
        --color-key 宮近海斗 --out images/xxx_eyecatch.png
"""

from __future__ import annotations

import argparse
import html as html_mod
import random
from pathlib import Path

CANVAS_W = 1075
CANVAS_H = 650
TEXT_COLOR = "#4f4f4f"

# 水彩の色(濃いめ, 中間, 薄め)。Canva版の実物から拾った色味
WATERCOLORS: dict[str, list[str]] = {
    "宮近海斗": ["#e8707f", "#f2a3a8", "#f7c9c4"],  # 赤
    "中村海人": ["#5fbf9a", "#9ad8bd", "#c9ebdc"],  # 緑
    "七五三掛龍也": ["#e7a1c8", "#f1c3dc", "#f7dff0"],  # ピンク
    "川島如恵留": ["#b9bdc2", "#d6d9dc", "#eceef0"],  # 白(シルバーグレー)
    "吉澤閑也": ["#f2cf5b", "#f7e08f", "#fbefc4"],  # 黄
    "松田元太": ["#7fb0e0", "#a9cbee", "#d3e5f7"],  # 青
    "松倉海斗": ["#e88a5a", "#f2b28a", "#f8d4bb"],  # オレンジ
    "group": ["#9b86d6", "#c3b2ea", "#e6dcf6"],  # 紫
    "group_warm": ["#a58bd8", "#f2a98a", "#f6cdd6"],  # 紫×ピーチ(複数メンバー回など)
}


def _blob_svg(colors: list[str], rnd: random.Random, colors_right: list[str] | None = None) -> str:
    """フィルタで縁をにじませた水彩blob群+飛沫+金のラメ.

    colors_right を渡すと2人回の二色展開: 左半分=colors、右半分=colors_right で塗り分ける。
    """
    blobs = []
    # 文字の後ろに小さめの水彩を何層も重ねる(Canva素材のアルコールインク風)
    n = 9
    for i in range(n):
        if colors_right:  # 二色展開は左右に交互に置いて量をそろえる
            cx = CANVAS_W * (rnd.uniform(0.16, 0.46) if i % 2 == 0 else rnd.uniform(0.54, 0.84))
        else:
            cx = CANVAS_W * rnd.uniform(0.22, 0.78)
        cy = CANVAS_H * rnd.uniform(0.12, 0.88)
        r = rnd.uniform(85, 165)
        pal = colors_right if (colors_right and cx > CANVAS_W / 2) else colors
        col = pal[(i // 2 if colors_right else i) % len(pal)]
        op = rnd.uniform(0.28, 0.5)
        blobs.append(
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{col}" fill-opacity="{op:.2f}" '
            f'style="mix-blend-mode:multiply" filter="url(#wc{i % 2})"/>'
        )
        # 縁の濃い溜まり
        blobs.append(
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r * 0.96:.0f}" fill="none" stroke="{pal[0]}" '
            f'stroke-opacity="0.35" stroke-width="3" filter="url(#wc{i % 2})"/>'
        )
    dots = []
    for _ in range(110):
        x = rnd.uniform(0.15, 0.85) * CANVAS_W
        y = rnd.uniform(0.05, 0.95) * CANVAS_H
        r = rnd.choice([1.2, 1.8, 2.4, 3, 4, 5])
        dpal = colors_right if (colors_right and x > CANVAS_W / 2) else colors
        dots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{rnd.choice(dpal[:2])}" fill-opacity="0.55"/>')
    gold = []
    for _ in range(28):
        x = rnd.uniform(0.55, 0.95) * CANVAS_W
        y = rnd.uniform(0.02, 0.4) * CANVAS_H
        gold.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1, 2.6):.1f}" fill="#d4ae5a" fill-opacity="0.8"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" style="position:absolute;inset:0">
<defs>
  <filter id="wc0" x="-30%" y="-30%" width="160%" height="160%">
    <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" seed="{rnd.randint(1, 999)}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="60" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feGaussianBlur in="d" stdDeviation="1.2"/>
  </filter>
  <filter id="wc1" x="-30%" y="-30%" width="160%" height="160%">
    <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="4" seed="{rnd.randint(1, 999)}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="45" xChannelSelector="G" yChannelSelector="B" result="d"/>
    <feGaussianBlur in="d" stdDeviation="0.8"/>
  </filter>
  <filter id="edge" x="-30%" y="-30%" width="160%" height="160%">
    <feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="3" seed="{rnd.randint(1, 999)}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="110" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feGaussianBlur in="d" stdDeviation="2"/>
  </filter>
  <filter id="paper"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2"/>
    <feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0.05 0"/></filter>
</defs>
{"".join(blobs)}
{"".join(dots)}
{"".join(gold)}
</svg>'''


def build_html(top: str, main: str, bottom: list[str], color_key: str, seed: int | None) -> str:
    rnd = random.Random(seed)
    # "宮近海斗+吉澤閑也" のように+でつなぐと左右で二色展開(2人回用)
    keys = color_key.split("+")
    colors = WATERCOLORS[keys[0]]
    colors_right = WATERCOLORS[keys[1]] if len(keys) > 1 else None
    esc = html_mod.escape
    bottom_html = "".join(f'<div class="fit bottom">{esc(b)}</div>' for b in bottom)
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Kosugi+Maru&display=block" rel="stylesheet">
<style>
html,body{{margin:0;padding:0}}
.stage{{position:relative;width:{CANVAS_W}px;height:{CANVAS_H}px;background:#fff;overflow:hidden}}
.text{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-family:'Kosugi Maru',sans-serif;color:{TEXT_COLOR};text-align:center}}
.fit{{white-space:nowrap;line-height:1.12;-webkit-text-stroke-color:{TEXT_COLOR};}}
.top{{font-size:54px;-webkit-text-stroke-width:1.6px;letter-spacing:0.04em;margin-bottom:4px}}
.main{{font-size:165px;-webkit-text-stroke-width:8px;letter-spacing:0.02em;margin-bottom:14px}}
.bottom{{font-size:68px;-webkit-text-stroke-width:4px;line-height:1.2}}
</style></head><body><div class="stage">
{_blob_svg(colors, rnd, colors_right)}
<div class="text">
  <div class="fit top" data-max="{CANVAS_W * 0.8:.0f}">{esc(top)}</div>
  <div class="fit main" data-max="{CANVAS_W * 0.9:.0f}">{esc(main)}</div>
  {bottom_html}
</div></div>
<script>
document.fonts.ready.then(()=>{{
  document.querySelectorAll('.fit').forEach(el=>{{
    const max = +(el.dataset.max || {CANVAS_W * 0.93:.0f});
    let fs = parseFloat(getComputedStyle(el).fontSize);
    while (el.scrollWidth > max && fs > 20) {{ fs -= 2; el.style.fontSize = fs + 'px'; }}
  }});
  document.body.dataset.ready = '1';
}});
</script></body></html>'''


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
        page.wait_for_selector("body[data-ready='1']", timeout=20000)
        page.screenshot(path=str(out_path), type="jpeg" if out_path.suffix.lower() in (".jpg", ".jpeg") else "png",
                        **({"quality": 90} if out_path.suffix.lower() in (".jpg", ".jpeg") else {}))
        browser.close()
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="chomoand-4.blog Canva風アイキャッチ生成")
    ap.add_argument("--top", default="Travis Japan", help="上段(小)。既定はTravis Japan")
    ap.add_argument("--main", required=True, help="中央(特大)。個人=メンバー名/グループ=話題キーワード")
    ap.add_argument("--bottom", action="append", default=[], help="下段(複数指定で複数行、最大2行)")
    ap.add_argument("--color-key", required=True,
                    help=f"{'/'.join(sorted(WATERCOLORS))}。2人回は「宮近海斗+吉澤閑也」で左右二色")
    ap.add_argument("--seed", type=int, default=None, help="水彩の形を固定する乱数シード")
    ap.add_argument("--out", required=True, help="出力パス(.jpg/.png)")
    a = ap.parse_args()
    for k in a.color_key.split("+"):
        if k not in WATERCOLORS:
            ap.error(f"--color-key に無い色: {k}")
    if len(a.color_key.split("+")) > 2:
        ap.error("--color-key の+つなぎは2人まで")
    if len(a.bottom) > 2:
        ap.error("--bottom は2行まで")
    print("done:", render(build_html(a.top, a.main, a.bottom, a.color_key, a.seed), Path(a.out)))


if __name__ == "__main__":
    main()
