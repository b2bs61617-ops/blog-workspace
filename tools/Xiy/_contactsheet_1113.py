# -*- coding: utf-8 -*-
"""Make contact sheets from a video. Usage: python _contactsheet_1113.py VIDEO OUTPREFIX N_FRAMES [COLS] [START END]"""
import sys
import cv2
import numpy as np

v, pre, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 4
cap = cv2.VideoCapture(v)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
dur = total / fps
s = float(sys.argv[5]) if len(sys.argv) > 5 else 0
e = float(sys.argv[6]) if len(sys.argv) > 6 else dur
print("duration", round(dur, 1))
tiles = []
for i in range(n):
    t = s + (e - s) * (i + 0.5) / n
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    if not ok:
        continue
    h, w = f.shape[:2]
    sc = 360 / w
    f = cv2.resize(f, (360, int(h * sc)))
    cv2.putText(f, f"{int(t//60)}:{int(t%60):02d}", (8, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    tiles.append(f)
per = cols * 2
for k in range(0, len(tiles), per):
    grp = tiles[k:k + per]
    while len(grp) % cols:
        grp.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(grp[r:r + cols]) for r in range(0, len(grp), cols)]
    cv2.imwrite(f"{pre}_{k // per:02d}.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 80])
