"""chomoand-2.com(Snow Man)アイキャッチ。

chomoand-4.blog(トラジャ)の水彩デザイン(tools/eyecatch_torahja_canva.py)を流用し、
色だけSnow Manのメンバーカラーに差し替える(eyecatch_kitetsu.pyと同じ作り)。

構成:
    上段(小)  : 「Snow Man」(既定)または分類
    中央(特大): 個人記事=メンバー名 / グループ記事=話題のキーワード
    下段(中)  : タイトルの残り1〜2行
背景: 個人記事=メンバーカラーの水彩、グループ記事=9色まぜ(group)。

使い方:
    python tools/eyecatch_snowman.py \
        --main "目黒蓮" \
        --bottom "私服のジャケットはどこの？" --bottom "ブランドを調査！" \
        --color-key 目黒蓮 --out images/xxx_eyecatch.jpg
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eyecatch_torahja_canva as base  # noqa: E402

# メンバーカラー(2026-10-18、一般に知られている色。違っていたら直す)
SNOWMAN_WATERCOLORS: dict[str, list[str]] = {
    "岩本照": ["#f2cf4a", "#f7e08a", "#fbefc2"],  # 黄
    "深澤辰哉": ["#a98bd6", "#c7b2e6", "#e3d8f3"],  # 紫
    "ラウール": ["#b9bdc2", "#d6d9dc", "#eceef0"],  # 白(シルバーグレー)
    "渡辺翔太": ["#6fa8e0", "#a3c8ee", "#d1e4f7"],  # 青
    "向井康二": ["#f2a14f", "#f7c28c", "#fbe0c4"],  # オレンジ
    "阿部亮平": ["#5fbf7a", "#9ad8a8", "#c9ebd2"],  # 緑
    "目黒蓮": ["#7d8087", "#a6a8ad", "#d2d3d6"],  # 黒(文字が読めるようグレー寄り)
    "宮舘涼太": ["#e0646f", "#ee9aa0", "#f7cbcd"],  # 赤
    "佐久間大介": ["#ec92c2", "#f3bcda", "#f9def0"],  # ピンク
    "group": ["#f2cf4a", "#a98bd6", "#6fa8e0", "#f2a14f", "#5fbf7a", "#e0646f", "#ec92c2"],
}

# build_html() はモジュールの WATERCOLORS を参照するので中身を差し替える
base.WATERCOLORS.clear()
base.WATERCOLORS.update(SNOWMAN_WATERCOLORS)


def main() -> None:
    ap = argparse.ArgumentParser(description="chomoand-2.com(Snow Man)アイキャッチ生成")
    ap.add_argument("--top", default="Snow Man", help="上段(小)。既定はSnow Man")
    ap.add_argument("--main", required=True, help="中央(特大)。個人=メンバー名/グループ=話題キーワード")
    ap.add_argument("--bottom", action="append", default=[], help="下段(複数指定で複数行、最大2行)")
    ap.add_argument("--color-key", required=True,
                    help=f"{'/'.join(SNOWMAN_WATERCOLORS)}。2人回は「目黒蓮+ラウール」で左右二色")
    ap.add_argument("--seed", type=int, default=None, help="水彩の形を固定する乱数シード")
    ap.add_argument("--out", required=True, help="出力パス(.jpg/.png)")
    a = ap.parse_args()
    keys = a.color_key.split("+")
    for k in keys:
        if k not in SNOWMAN_WATERCOLORS:
            ap.error(f"--color-key に無い色: {k}")
    if len(keys) > 2:
        ap.error("--color-key の+つなぎは2人まで")
    if len(a.bottom) > 2:
        ap.error("--bottom は2行まで")
    print("done:", base.render(base.build_html(a.top, a.main, a.bottom, a.color_key, a.seed), Path(a.out)))


if __name__ == "__main__":
    main()
