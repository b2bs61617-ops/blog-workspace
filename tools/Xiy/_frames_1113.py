import sys, cv2
v, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(v)
for t in sys.argv[3:]:
    m, s = t.split(':'); sec = int(m)*60+float(s)
    cap.set(cv2.CAP_PROP_POS_MSEC, sec*1000); ok, f = cap.read()
    if ok: cv2.imwrite(f"{out}/f_{t.replace(':','-')}.jpg", f, [cv2.IMWRITE_JPEG_QUALITY, 92])
