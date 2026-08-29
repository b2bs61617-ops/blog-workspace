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

import requests

JST = timezone(timedelta(hours=9))

LAT_MIN, LAT_MAX = 35.10, 36.30      # 関東(神奈川〜東京〜埼玉南部)
LNG_MIN, LNG_MAX = 138.90, 140.30

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
_STEALTH = "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"

_FRESH_RE = re.compile(r"(たった今|今すぐ|(\d+)\s*分前|(\d+)\s*秒前)")
# 位置共有の実座標: batchexecute 応答内の [null,null,<lat>,<lng>]
_PIN_RE = re.compile(r"\[null,null,(3[0-9]\.\d{4,}),(1[0-9]{2}\.\d{4,})\]")
_AT_RE = re.compile(r"/@(-?\d+\.\d+),(-?\d+\.\d+)")


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
            viewport={"width": 1100, "height": 900}, locale="ja-JP",
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
                await pg.screenshot(path=shot_path)
            except Exception:
                pass
        try:
            await b.close()
        except Exception:
            pass
    return out


def fetch(share_url, wait_ms=12000, shot_path=None):
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

    label = _reverse_geocode(lat, lng)
    if not label:
        return []

    now = datetime.now(JST)
    exact = r.get("pin") is not None
    body = (f"追跡者(@YSB_DANCHO)のリアルタイム位置共有では、現在地は {label} 付近"
            + (f"（{lat:.5f},{lng:.5f}）" if exact else "（おおよそ）")
            + "。" + (f"(位置情報の更新: {fresh})" if fresh else ""))
    return [{
        "id": f"sharemap:{now:%Y%m%d%H%M}",
        "date": now.isoformat(),
        "author": "share_map",
        "text": body,
        "source": "share_map",
        "url": "",
        "_addr": label,
        "_latlng": [round(lat, 7), round(lng, 7)],
        "_exact": exact,
    }]


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
