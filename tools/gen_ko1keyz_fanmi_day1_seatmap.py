# -*- coding: utf-8 -*-
"""
現地の座席案内板の写真(アリーナ客席図、22everic氏の投稿
https://x.com/22everic/status/2090789679465709589 で共有)をもとに、
KO1KEYZ 1STファンミ東京公演DAY1記事に載せる座席ブロック図を作成する。
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
FONT_PATH = ROOT / "assets" / "fonts" / "MPLUSRounded1c-Black.ttf"

W, H = 1000, 1300
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
BLOCK_FILL = (198, 226, 240)
BLOCK_BORDER = (20, 20, 20)
BG = (255, 255, 255)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)


def font(size):
    return ImageFont.truetype(str(FONT_PATH), size)


def centered_text(box, text, size, fill=WHITE):
    x0, y0, x1, y1 = box
    f = font(size)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx = x0 + (x1 - x0 - tw) / 2 - bbox[0]
    cy = y0 + (y1 - y0 - th) / 2 - bbox[1]
    draw.text((cx, cy), text, font=f, fill=fill)


# タイトルバー
title_box = (40, 30, W - 40, 120)
draw.rectangle(title_box, fill=BLACK)
centered_text(title_box, "アリーナ客席図", 44)

# ステージ
stage_box = (W * 0.22, 150, W * 0.78, 260)
draw.rectangle(stage_box, fill=BLACK)
centered_text(stage_box, "ステージ", 40)

# 客席ブロック(A/B/C列 x 7ブロック)
grid_top = 300
grid_bottom = 980
row_h = (grid_bottom - grid_top) / 3
grid_left = 60
grid_right = W - 60
col_w = (grid_right - grid_left) / 7
row_labels = ["A", "B", "C"]

for r, row_label in enumerate(row_labels):
    y0 = grid_top + r * row_h
    y1 = y0 + row_h - 14
    for c in range(7):
        x0 = grid_left + c * col_w
        x1 = x0 + col_w - 10
        draw.rectangle((x0, y0, x1, y1), fill=BLOCK_FILL, outline=BLOCK_BORDER, width=3)
        centered_text((x0, y0, x1, y1), f"{row_label}{c + 1}", 34, fill=BLACK)

# 下段: D2 / 機材 / D6
bottom_y0 = grid_bottom + 20
bottom_y1 = bottom_y0 + 140

d2_box = (grid_left, bottom_y0, grid_left + col_w * 1.4 - 10, bottom_y1)
draw.rectangle(d2_box, fill=BLOCK_FILL, outline=BLOCK_BORDER, width=3)
centered_text(d2_box, "D2", 34, fill=BLACK)

equip_box = (grid_left + col_w * 1.6, bottom_y0, grid_left + col_w * 5.4 - 10, bottom_y1)
draw.rectangle(equip_box, fill=BLACK)
centered_text(equip_box, "機材", 34)

d6_box = (grid_left + col_w * 5.6, bottom_y0, grid_right - 10, bottom_y1)
draw.rectangle(d6_box, fill=BLOCK_FILL, outline=BLOCK_BORDER, width=3)
centered_text(d6_box, "D6", 34, fill=BLACK)

# 出典キャプション
cap_font = font(22)
cap_text = "現地の座席案内板の写真をもとに作成"
bbox = draw.textbbox((0, 0), cap_text, font=cap_font)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) / 2, H - 60), cap_text, font=cap_font, fill=(120, 120, 120))

out_path = ROOT / "images" / "ko1keyz_fanmi_day1_seatmap_official.png"
img.save(out_path)
print("saved", out_path)
