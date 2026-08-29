"""追跡者(@YSB_DANCHO)が公開している Google マップ「リアルタイム位置共有」リンクを
ヘッドレスブラウザ(webdriver 判定を回避)で開き、共有ピンの**正確な座標**を取得する。

Google は座標を DOM/URL には正しく出さない(URL の @lat,lng は最大 ~1km ずれる)。
位置共有の実データは内部 RPC `.../maps/_/MapsWizUi/data/batchexecute` の応答に
`[null,null,<lat>,<lng>]` という形で 14 桁精度で入っている。それを拾う。

post dict:
  {"id","date"(ISO8601 JST),"author":"share_map","text","source":"share_map","url":"",
   "_latlng":[lat,lng],"_addr":"横浜市青葉区千草台"}
座標が取れない/関東外/古い(N分以上前)場合は空 list(記事は触られない)。
"""
import asyncio
import re
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path

import requests

JST = timezone(timedelta(hours=9))
ROOT = Path(__file__).resolve().parents[2]

LAT_MIN, LAT_MAX = 35.10, 36.30      # 関東(神奈川〜東京〜埼玉南部)
LNG_MIN, LNG_MAX = 138.90, 140.30

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
_STEALTH = "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"

_FRESH_RE = re.compile(r"(たった今|今すぐ|(\d+)\s*分前|(\d+)\s*秒前)")
# 位置共有の実座標: batchexecute 応答内の [null,null,<lat>,<lng>]
_PIN_RE = re.compile(r"\[null,null,(3[0-9]\.\d{4,}),(1[0-9]{2}\.\d{4,})\]")
_AT_RE = re.compile(r"/@(-?\d+\.\d+),(-?\d+\.\d+)")


def _save_map_crop(png_bytes, out_path):
    """スクショから地図部分(右側)だけ切り出して保存。左の検索サイドパネルは捨てる。
    失敗したら元スクショをそのまま保存する。"""
    try:
        from PIL import Image
        im = Image.open(BytesIO(png_bytes)).convert("RGB")
        w, h = im.size
        left = int(w * 0.42)   # 左サイドパネル(店名・住所)を除外して地図だけ残す
        im.crop((left, 0, w, h)).save(out_path, "PNG")
    except Exception:
        try:
            Path(out_path).write_bytes(png_bytes)
        except Exception:
            pass


_VISION_PROMPT = """これは24時間テレビ マラソンの追跡者(@YSB_DANCHO)のリアルタイム位置共有の
Google マップ画面です。丸いアイコン(共有ピン)が走者のいる現在地です。

ピンのある場所を日本語で簡潔に answer:
1行目: ピン直下の「市区町村＋町丁目」(例: 横浜市青葉区市ケ尾町)。読み取れた文字だけを根拠にする。
2行目: ピン周辺に見える駅名・幹線道路名・橋・河川・ランドマーク(読めるものだけ)。

【ルール】
- 地図が無い/文字が読めない/判別できないときは1行目に「判別不可」とだけ書く。
- 推測で地名をでっち上げない。地図に書かれた文字だけ。
- 2行以内。前置き・説明を付けない。"""


def _vision_read(png_path):
    """撮った地図スクショを Gemini Vision に読ませ、ピン位置の説明文を返す。
    逆ジオコーディング(座標→住所)より、地図に書かれた地名を直接読む方が確実。"""
    import os

    key = None
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip()
    key = key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return ""
    try:
        from google import genai
        from google.genai import types

        png = Path(png_path).read_bytes()
        client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=45000))
        for m in ("gemini-3.5-flash", "gemini-3.6-flash", "gemini-3.1-flash-lite"):
            try:
                resp = client.models.generate_content(
                    model=m,
                    contents=[types.Part.from_bytes(data=png, mime_type="image/png"),
                              _VISION_PROMPT],
                )
                txt = (resp.text or "").strip()
                if txt and not txt.splitlines()[0].strip().startswith("判別不可"):
                    return " / ".join(l.strip() for l in txt.splitlines() if l.strip())
                return ""
            except Exception as e:  # noqa: BLE001
                if not any(s in str(e) for s in ("404", "NOT_FOUND", "not available", "503",
                                                 "504", "429", "UNAVAILABLE", "DEADLINE_EXCEEDED",
                                                 "overloaded")):
                    return ""
    except Exception:
        return ""
    return ""


def _reverse_geocode(lat, lng):
    """座標→日本語の市区町村＋小地名。失敗で空文字。"""
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": f"{lat:.7f}", "lon": f"{lng:.7f}", "format": "json",
                    "accept-language": "ja", "zoom": "17"},
            headers={"User-Agent": "marathon-tracker/1.0"}, timeout=15,
        )
        a = r.json().get("address", {})
        parts = [a.get(k) for k in ("city", "town", "village", "city_district",
                                    "suburb", "neighbourhood", "quarter")]
        parts = [p for p in parts if p]
        return "".join(dict.fromkeys(parts[:3]))
    except Exception:
        return ""


async def _read(share_url, wait_ms, shot_path=None):
    from playwright.async_api import async_playwright

    out = {"pin": None, "at": None, "fresh": ""}
    async with async_playwright() as p:
        b = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--lang=ja-JP"],
        )
        ctx = await b.new_context(
            viewport={"width": 1200, "height": 900}, locale="ja-JP",
            timezone_id="Asia/Tokyo", user_agent=_UA,
        )
        await ctx.add_init_script(_STEALTH)
        pg = await ctx.new_page()

        pins = []

        async def on_resp(resp):
            if "batchexecute" not in resp.url:
                return
            try:
                body = await resp.text()
            except Exception:
                return
            for m in _PIN_RE.finditer(body):
                try:
                    pins.append((float(m.group(1)), float(m.group(2))))
                except ValueError:
                    pass

        pg.on("response", on_resp)
        try:
            await pg.goto(share_url, wait_until="domcontentloaded", timeout=40000)
            # 共有位置データ(batchexecute)は数秒おきにポーリングされる。
            # 1回でも確実に拾えるよう長めに待つ。
            await pg.wait_for_timeout(wait_ms)
        except Exception:
            try:
                await b.close()
            except Exception:
                pass
            return out

        # 最後に観測されたピンを採用(移動中は最新が末尾)
        kanto = [(la, ln) for la, ln in pins
                 if LAT_MIN <= la <= LAT_MAX and LNG_MIN <= ln <= LNG_MAX]
        if kanto:
            out["pin"] = kanto[-1]

        m = _AT_RE.search(pg.url)
        if m:
            out["at"] = (float(m.group(1)), float(m.group(2)))

        try:
            el = await pg.query_selector('div[role="main"]') or await pg.query_selector("body")
            txt = (await el.inner_text()) if el else ""
        except Exception:
            txt = ""
        for ln in (l.strip() for l in txt.splitlines() if l.strip()):
            fm = _FRESH_RE.search(ln)
            if fm:
                out["fresh"] = fm.group(1)
                break

        if shot_path:
            try:
                raw = await pg.screenshot()
                _save_map_crop(raw, shot_path)
            except Exception:
                pass
        try:
            await b.close()
        except Exception:
            pass
    return out


def fetch(share_url, wait_ms=22000, shot_path=None):
    if not share_url:
        return []
    try:
        r = asyncio.run(_read(share_url, wait_ms, shot_path))
    except Exception:
        return []

    pin = r.get("pin") or r.get("at")   # 実座標が取れなければ URL 中心を暫定利用
    if not pin:
        return []
    lat, lng = pin
    if not (LAT_MIN <= lat <= LAT_MAX and LNG_MIN <= lng <= LNG_MAX):
        return []

    fresh = r.get("fresh", "")
    mm = re.search(r"(\d+)\s*分前", fresh)
    if mm and int(mm.group(1)) > 12:      # 12分より前の位置は使わない
        return []

    now = datetime.now(JST)
    exact = r.get("pin") is not None
    have_shot = bool(shot_path and Path(shot_path).exists())

    # 現在地の説明は「地図スクショを Vision で直読み」を最優先。
    # 内部RPCのピン座標(exact)が取れているときだけ逆ジオコーディングも併用する。
    vision = _vision_read(shot_path) if have_shot else ""
    geo = _reverse_geocode(lat, lng) if exact else ""

    if vision:
        body = "追跡者(@YSB_DANCHO)の位置共有マップ: " + vision
        if exact:
            body += f"（{lat:.5f},{lng:.5f}）"
        addr = vision
    elif exact and geo:
        body = f"追跡者(@YSB_DANCHO)のリアルタイム位置共有では、現在地は {geo} 付近（{lat:.5f},{lng:.5f}）。"
        addr = geo
    else:
        # スクショも読めず座標も不正確 → 断定できる情報が無い。使わない。
        return []
    if fresh:
        body += f"(位置情報の更新: {fresh})"

    post = {
        "id": f"sharemap:{now:%Y%m%d%H%M}",
        "date": now.isoformat(),
        "author": "share_map",
        "text": body,
        "source": "share_map",
        "url": "",
        "_addr": addr,
        "_latlng": [round(lat, 7), round(lng, 7)],
        "_exact": exact,
    }
    if have_shot:
        post["_shot"] = str(shot_path)
        post["_fresh"] = fresh
    return [post]


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--wait", type=int, default=12000)
    ap.add_argument("--shot", default="")
    a = ap.parse_args()
    for x in fetch(a.url, wait_ms=a.wait, shot_path=(a.shot or None)):
        print(x["text"])
        print("latlng:", x["_latlng"], "exact:", x["_exact"])
