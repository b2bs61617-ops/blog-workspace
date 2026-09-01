# -*- coding: utf-8 -*-
"""KO1KEYZ メンバー別ピアス数の一覧図(記事本文用).

Xで話題になった観察ポスト(左右の耳のピアス位置をまとめたもの)の数値を、
chomoand-1.com の記事デザインに合わせて自前レイアウトで作図し直す。
ファンが作った画像そのものは転載せず、数値だけを使って別レイアウトで再構成する方針。

    python tools/gen_ko1keyz_piercing_chart.py            # 日本語版
    python tools/gen_ko1keyz_piercing_chart.py --lang en  # 英語版
    python tools/gen_ko1keyz_piercing_chart.py --lang kr  # 韓国語版
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "images"

FONT_R = "C:/Windows/Fonts/BIZ-UDGothicR.ttc"
FONT_B = "C:/Windows/Fonts/BIZ-UDGothicB.ttc"

BG = "#faf9f7"
CARD = "#ffffff"
BORDER = "#ded9d2"
INK = "#2b2b2b"
SUB = "#8a8378"

# (English, 日本語, 한국어, member color, right ear, left ear)
MEMBERS = [
    ("TOWA", "濱田永遠", "하마다 토와", "#A5CD39", 2, 3),
    ("DAIKI", "加藤大樹", "가토 다이키", "#1FA24A", 2, 2),
    ("KOSUKE", "照井康祐", "테루이 코스케", "#E60027", 1, 2),
    ("KEITO", "小野慶人", "오노 케이토", "#EF7C00", 1, 1),
    ("RYUJI", "杉山竜司", "스기야마 류지", "#F5C518", 1, 1),
    ("YUKI", "後藤結", "고토 유이", "#8A5CC0", 1, 1),
    ("YOSHIKI", "矢田佳暉", "야다 요시키", "#F29CC2", 1, 1),
    ("ISSA", "柳谷伊冴", "야나기야 잇사", "#6DCFF6", 0, 0),
    ("YURA", "安部結蘭", "아베 유라", "#1477C6", 0, 0),
    ("RYOGA", "飯塚亮賀", "이이즈카 료가", "#24357F", 0, 0),
    ("SIYOUNG", "パク・シヨン", "박시영", "#FAFAFA", 0, 0),
    ("SHINHAENG", "オ・シンヘン", "오신행", "#7B4A2E", 0, 0),
]

TITLE = {
    "ja": "コイキーズ メンバー別・ピアスの数",
    "en": "KO1KEYZ — Ear Piercings by Member",
    "kr": "KO1KEYZ 멤버별 피어싱 개수",
}
FOOT = {
    "ja": "※Xでの観察情報をもとに作成。左右の耳を合算した数(0はホールが確認できないメンバー)。",
    "en": "Based on fan observations shared on X. Totals combine both ears (0 = no visible piercings).",
    "kr": "X에 공유된 관찰 정보를 바탕으로 작성. 좌우 귀를 합산한 개수(0은 피어싱이 확인되지 않은 멤버).",
}


def hex2rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def draw_chart(lang: str) -> Path:
    W = 1200
    pad = 40
    header_h = 96
    row_h = 60
    H = header_h + row_h * len(MEMBERS) + 78

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(FONT_B, 34)
    f_name = ImageFont.truetype(FONT_B, 25)
    f_sub = ImageFont.truetype(FONT_R, 18)
    f_num = ImageFont.truetype(FONT_B, 30)
    f_foot = ImageFont.truetype(FONT_R, 17)

    d.text((pad, 34), TITLE[lang], font=f_title, fill=INK)

    # card
    card_top = header_h
    card_bottom = header_h + row_h * len(MEMBERS)
    d.rounded_rectangle([pad, card_top, W - pad, card_bottom], radius=14,
                        fill=CARD, outline=BORDER, width=2)

    max_count = 5
    dot_x0 = 430
    dot_gap = 34
    dot_r = 12

    for i, (en, ja, kr, color, r_ear, l_ear) in enumerate(MEMBERS):
        cy = card_top + row_h * i + row_h // 2
        if i:
            d.line([pad + 18, card_top + row_h * i, W - pad - 18, card_top + row_h * i],
                   fill="#efece7", width=1)

        # member color chip
        rgb = hex2rgb(color)
        chip_outline = "#cfcac2" if sum(rgb) > 720 else color
        d.ellipse([pad + 22, cy - 13, pad + 48, cy + 13], fill=color, outline=chip_outline, width=2)

        # names
        d.text((pad + 66, cy - 20), en, font=f_name, fill=INK)
        label2 = {"ja": ja, "en": ja, "kr": kr}[lang]
        d.text((pad + 66, cy + 8), label2, font=f_sub, fill=SUB)

        total = r_ear + l_ear
        if total == 0:
            d.text((dot_x0, cy - 12), "—", font=f_num, fill="#c8c3bb")
        else:
            for k in range(total):
                x = dot_x0 + k * dot_gap
                d.ellipse([x, cy - dot_r, x + dot_r * 2, cy + dot_r],
                          fill=color, outline=chip_outline, width=2)

        # total number at right
        num = str(total)
        tw = d.textlength(num, font=f_num)
        num_fill = INK if total else "#c8c3bb"
        d.text((W - pad - 30 - tw, cy - 18), num, font=f_num, fill=num_fill)

    d.text((pad, card_bottom + 26), FOOT[lang], font=f_foot, fill=SUB)

    OUT_DIR.mkdir(exist_ok=True)
    suffix = "" if lang == "ja" else f"_{lang}"
    out = OUT_DIR / f"ko1keyz_piercing_count_chart{suffix}.png"
    img.save(out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="ja", choices=["ja", "en", "kr"])
    args = ap.parse_args()
    p = draw_chart(args.lang)
    print("saved", p)
