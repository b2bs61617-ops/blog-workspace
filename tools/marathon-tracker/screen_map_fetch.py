"""デスクトップに出しっぱなしの Google マップ画面をスクショして、
Gemini Vision に「今どのあたりが中心に映っているか」を読ませる。

人間(トモキ)がランナーの現在地に地図を合わせておく前提。ロボットは読むだけ。

戻り値は x_fetch / yt_chat_fetch と同じ形の post dict:
  {"id", "date"(ISO8601 JST), "author": "screen_map", "text", "source": "screen_map", "url": ""}
判別できなければ空 list を返す(記事は触られない)。
"""
import io
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9))

VISION_PROMPT = """これはデスクトップのスクリーンショットです。24時間テレビのマラソンランナー(星野真里)の
現在地を表示している Google マップが映っている想定です。

地図部分だけを見て、次を日本語で簡潔に answer:
- 地図の中心付近はどの都道府県・市区町村・エリアか
- 中心付近に見える地名・駅名・道路名・ランドマーク・ピンの吹き出し文字(読めるもの)
- 走行ルートやピンが複数あるなら、いちばん新しそうな(先頭の)位置

【ルール】
- 地図が映っていない/文字が小さすぎて読めない/どこか判別できない場合は、先頭に「判別不可」とだけ書く。
- 推測で市区町村名をでっち上げない。はっきり読み取れた文字だけを根拠にする。
- ピンの吹き出しやアイコンのラベルが不鮮明なら無理に文字起こしせず「(ラベル不鮮明)」と書く。
- 5行以内。"""


def _load_env():
    env = {}
    root = Path(__file__).resolve().parents[2]
    f = root / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def _grab_png(region=None):
    """region: [left, top, width, height] or None(プライマリ全体)。PNG bytes を返す。"""
    import mss
    import mss.tools

    with mss.MSS() as sct:
        if region and len(region) == 4:
            mon = {"left": region[0], "top": region[1], "width": region[2], "height": region[3]}
        else:
            mon = sct.monitors[1]  # プライマリ
        shot = sct.grab(mon)
        return mss.tools.to_png(shot.rgb, shot.size)


def _downscale_png(png_bytes, max_w=1600):
    """4K のままだと重い・トークン食うので長辺を縮める。"""
    from PIL import Image

    im = Image.open(io.BytesIO(png_bytes))
    if im.width > max_w:
        h = int(im.height * max_w / im.width)
        im = im.resize((max_w, h), Image.LANCZOS)
    out = io.BytesIO()
    im.save(out, format="PNG", optimize=True)
    return out.getvalue()


def _ask_gemini(png_bytes, api_key, model="gemini-3.5-flash"):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=45000))
    models = [model, "gemini-3.6-flash", "gemini-3.1-flash-lite"]
    last = None
    for m in models:
        try:
            resp = client.models.generate_content(
                model=m,
                contents=[
                    types.Part.from_bytes(data=png_bytes, mime_type="image/png"),
                    VISION_PROMPT,
                ],
            )
            return (resp.text or "").strip()
        except Exception as e:  # noqa: BLE001
            last = e
            if not any(s in str(e) for s in ("404", "NOT_FOUND", "not available",
                                             "503", "504", "429", "UNAVAILABLE",
                                             "DEADLINE_EXCEEDED", "overloaded")):
                raise
    raise RuntimeError(f"Gemini Vision 失敗: {last}")


def fetch(region=None, save_shot_to=None, model="gemini-3.5-flash"):
    env = _load_env()
    key = env.get("GEMINI_API_KEY")
    if not key:
        return []
    try:
        png = _grab_png(region)
    except Exception:
        return []
    try:
        png = _downscale_png(png)
    except Exception:
        pass
    if save_shot_to:
        try:
            Path(save_shot_to).write_bytes(png)
        except Exception:
            pass
    try:
        text = _ask_gemini(png, key, model=model)
    except Exception:
        return []
    if not text:
        return []
    first = text.splitlines()[0].strip() if text.splitlines() else text
    if text.startswith("判別不可") or first.startswith("判別不可") or "判別不可" in first:
        return []

    now = datetime.now(JST)
    return [{
        "id": f"map:{now:%Y%m%d%H%M}",  # 分単位で1件(重複防止)
        "date": now.isoformat(),
        "author": "screen_map",
        "text": "デスクトップのGoogleマップ画面より: " + " / ".join(
            ln.strip() for ln in text.splitlines() if ln.strip()
        ),
        "source": "screen_map",
        "url": "",
    }]


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--region", help="left,top,width,height", default=None)
    ap.add_argument("--save", default="tools/marathon-tracker/logs/last_map_shot.png")
    a = ap.parse_args()
    reg = [int(x) for x in a.region.split(",")] if a.region else None
    res = fetch(region=reg, save_shot_to=a.save)
    print(f"--- {len(res)} entries ---")
    for r in res:
        print(r["date"])
        print(r["text"])
