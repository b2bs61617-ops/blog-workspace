# -*- coding: utf-8 -*-
"""KO1KEYZ Official MV をローカルにDL(映像のみ137)して、TOWAのりんごシーンを探すコンタクトシートを作る。"""
import sys
from pathlib import Path

import cv2
import yt_dlp
from PIL import Image

VIDEO_URL = sys.argv[1] if len(sys.argv) > 1 else "https://www.youtube.com/watch?v=75MEFldsJKc"
SCRATCH = Path(r"C:\Users\s30se\AppData\Local\Temp\claude\c--Users-s30se-OneDrive--------CHOMO\1bc817a6-7819-48a8-8427-f7c44c8fa240\scratchpad")
MP4 = SCRATCH / "ko1keyz_mv.mp4"
OUT = Path(__file__).resolve().parent.parent / "images" / "_ko1keyz_mv_contactsheet.png"

if not MP4.exists():
    with yt_dlp.YoutubeDL({
        "quiet": True, "format": "137/136/135/bestvideo[ext=mp4]",
        "outtmpl": str(MP4), "noprogress": True,
    }) as ydl:
        ydl.download([VIDEO_URL])
print("mp4:", MP4, MP4.stat().st_size, "bytes")

cap = cv2.VideoCapture(str(MP4), cv2.CAP_FFMPEG)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
n = cap.get(cv2.CAP_PROP_FRAME_COUNT)
dur = n / fps
print("fps", fps, "frames", n, "dur", round(dur, 1))

STEP = 2.0
TILE_W = 240
cols = 12
tiles = []
fi = 0
step_frames = int(round(STEP * fps))
cur = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    if cur % step_frames == 0:
        t = cur / fps
        h, w = frame.shape[:2]
        th = int(TILE_W * h / w)
        small = cv2.resize(frame, (TILE_W, th))
        label = f"{int(t//60):d}:{t%60:04.1f}"
        cv2.putText(small, label, (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(small, label, (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
    cur += 1
cap.release()

th = tiles[0].shape[0]
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * TILE_W, rows * th), "black")
for i, tile in enumerate(tiles):
    sheet.paste(Image.fromarray(tile), ((i % cols) * TILE_W, (i // cols) * th))
sheet.save(OUT)
print("saved", OUT, sheet.size, f"{len(tiles)} tiles @ {STEP}s (step {step_frames}f)")
