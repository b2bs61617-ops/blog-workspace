"""chomoand-5.site(KEY TO LIT=キテレツ)アイキャッチ。

chomoand-4.blog(トラジャ)の水彩デザイン(tools/eyecatch_torahja_canva.py)を流用し、
色だけKEY TO LITのメンバーカラーに差し替える。

構成:
    上段(小)  : 「KEY TO LIT」(既定)または分類
    中央(特大): 個人記事=メンバー名 / グループ記事=話題のキーワード
    下段(中)  : タイトルの残り1〜2行
背景: 個人記事=メンバーカラーの水彩、グループ記事=5色まぜ(group)。

使い方:
    python tools/eyecatch_kitetsu.py \
        --main "猪狩蒼弥" \
        --bottom "私服のジャケットはどこの？" --bottom "ブランドを調査！" \
        --color-key 猪狩蒼弥 --out images/xxx_eyecatch.jpg
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eyecatch_torahja_canva as base  # noqa: E402

# メンバーカラー(2026-10-17調べ。fanplus経由のジュニア公式プロフィール情報)
KITETSU_WATERCOLORS: dict[str, list[str]] = {
    "岩﨑大昇": ["#b9bdc2", "#d6d9dc", "#eceef0"],  # 白(シルバーグレー)
    "井上瑞稀": ["#e8707f", "#f2a3a8", "#f7c9c4"],  # 赤
    "中村嶺亜": ["#e7a1c8", "#f1c3dc", "#f7dff0"],  # ピンク
    "猪狩蒼弥": ["#5fbf9a", "#9ad8bd", "#c9ebdc"],  # 緑
    "佐々木大光": ["#7fb0e0", "#a9cbee", "#d3e5f7"],  # 青
    "group": ["#e8707f", "#e7a1c8", "#5fbf9a", "#7fb0e0", "#b9bdc2"],  # 5色まぜ
}

# build_html() はモジュールの WATERCOLORS を参照するので中身を差し替える
base.WATERCOLORS.clear()
base.WATERCOLORS.update(KITETSU_WATERCOLORS)


def main() -> None:
    ap = argparse.ArgumentParser(description="chomoand-5.site(KEY TO LIT)アイキャッチ生成")
    ap.add_argument("--top", default="KEY TO LIT", help="上段(小)。既定はKEY TO LIT")
    ap.add_argument("--main", required=True, help="中央(特大)。個人=メンバー名/グループ=話題キーワード")
    ap.add_argument("--bottom", action="append", default=[], help="下段(複数指定で複数行、最大2行)")
    ap.add_argument("--color-key", required=True,
                    help=f"{'/'.join(KITETSU_WATERCOLORS)}。2人回は「井上瑞稀+猪狩蒼弥」で左右二色")
    ap.add_argument("--seed", type=int, default=None, help="水彩の形を固定する乱数シード")
    ap.add_argument("--out", required=True, help="出力パス(.jpg/.png)")
    a = ap.parse_args()
    keys = a.color_key.split("+")
    for k in keys:
        if k not in KITETSU_WATERCOLORS:
            ap.error(f"--color-key に無い色: {k}")
    if len(keys) > 2:
        ap.error("--color-key の+つなぎは2人まで")
    if len(a.bottom) > 2:
        ap.error("--bottom は2行まで")
    print("done:", base.render(base.build_html(a.top, a.main, a.bottom, a.color_key, a.seed), Path(a.out)))


if __name__ == "__main__":
    main()
