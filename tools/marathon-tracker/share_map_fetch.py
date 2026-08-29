"""追跡者(@YSB_DANCHO)が公開している Google マップ「リアルタイム位置共有」リンクを
ヘッドレスブラウザ(webdriver 判定を回避)で開き、
  - 地図の中心座標(＝共有ピン位置)を URL の @lat,lng から取得
  - 共有カードに出る住所テキスト
  - 「たった今 / N分前」の鮮度表示
を取り出して x_fetch と同じ形の post dict を返す。

webdriver 検出を回避しないと Google は共有座標を返さず地図をブラウザ既定位置
(米国のデータセンター)に固定するため、UA 差し替え + navigator.webdriver 潰し必須。

post dict:
  {"id","date"(ISO8601 JST),"author":"share_map","text","source":"share_map","url":"",
   "_latlng":[lat,lng]}
古い(N分以上前)/座標が関東外/読めない場合は空 list を返す(記事は触られない)。
"""
import asyncio
import re
from datetime import datetime, timedelta, timezone

import requests

JST = timezone(timedelta(hours=9))

# 関東のざっくり妥当範囲(神奈川〜東京〜埼玉南部)
LAT_MIN, LAT_MAX = 35.10, 36.30
LNG_MIN, LNG_MAX = 138.90, 140.30

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
_STEALTH = "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"

_FRESH_RE = re.compile(r"(たった今|今すぐ|(\d+)\s*分前|(\d+)\s*秒前)")
_AT_RE = re.compile(r"/@(-?\d+\.\d+),(-?\d+\.\d+)")


async def _read(share_url, wait_ms, shot_path=None):
    from playwright.async_api import async_playwright

    out = {"lat": None, "lng": None, "addr": "", "fresh": "", "stale": True}
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
        try:
            await pg.goto(share_url, wait_until="domcontentloaded", timeout=40000)
            await pg.wait_for_timeout(wait_ms)
        except Exception:
            try:
                await b.close()
            except Exception:
                pass
            return out

        m = _AT_RE.search(pg.url)
        if m:
            out["lat"], out["lng"] = float(m.group(1)), float(m.group(2))

        try:
            el = await pg.query_selector('div[role="main"]') or await pg.query_selector("body")
            txt = (await el.inner_text()) if el else ""
        except Exception:
            txt = ""
        lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
        for ln in lines:
            if ("Japan" in ln or "日本" in ln or "Ward" in ln or ("区" in ln and len(ln) > 6)) \
                    and not out["addr"] and len(ln) < 140:
                out["addr"] = ln
            fm = _FRESH_RE.search(ln)
            if fm and not out["fresh"]:
                out["fresh"] = fm.group(1)

        if out["fresh"]:
            mins = 0
            mm = re.search(r"(\d+)\s*分前", out["fresh"])
            if mm:
                mins = int(mm.group(1))
            out["stale"] = mins > 12  # 12分より前の位置は使わない
        else:
            out["stale"] = out["lat"] is None  # 鮮度表記が読めなくても座標があれば採用

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


def _clean_addr(a):
    a = re.sub(r"^Japan,?\s*", "", a).strip()
    a = re.sub(r"〒?\d{3}-?\d{4}\s*", "", a).strip()
    a = a.replace("Kanagawa,", "神奈川県").replace("Yokohama,", "横浜市")
    a = a.replace(" Ward", "区").replace("-chōme", "丁目").replace("chōme", "丁目")
    return a.strip(" ,")


def _reverse_geocode(lat, lng):
    """座標を日本語の市区町村＋小地名に。失敗したら空文字。"""
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": f"{lat:.6f}", "lon": f"{lng:.6f}", "format": "json",
                    "accept-language": "ja", "zoom": "16"},
            headers={"User-Agent": "marathon-tracker/1.0"}, timeout=15,
        )
        a = r.json().get("address", {})
        parts = [a.get(k) for k in ("city", "town", "village", "city_district",
                                    "suburb", "neighbourhood", "quarter", "road")]
        parts = [p for p in parts if p]
        return "".join(dict.fromkeys(parts[:3]))
    except Exception:
        return ""


def fetch(share_url, wait_ms=11000, shot_path=None):
    if not share_url:
        return []
    try:
        r = asyncio.run(_read(share_url, wait_ms, shot_path))
    except Exception:
        return []
    lat, lng = r.get("lat"), r.get("lng")
    if lat is None or not (LAT_MIN <= lat <= LAT_MAX and LNG_MIN <= lng <= LNG_MAX):
        return []
    if r.get("stale"):
        return []

    now = datetime.now(JST)
    fresh = r.get("fresh", "")
    loc = _reverse_geocode(lat, lng) or _clean_addr(r.get("addr", "")) \
        or f"緯度{lat:.5f}／経度{lng:.5f}付近"
    body = (f"追跡者(@YSB_DANCHO)が公開しているGoogleマップのリアルタイム位置共有より、"
            f"現在地は {loc}（{lat:.5f},{lng:.5f}）。"
            + (f" 位置情報の更新: {fresh}。" if fresh else ""))
    return [{
        "id": f"sharemap:{now:%Y%m%d%H%M}",
        "date": now.isoformat(),
        "author": "share_map",
        "text": body,
        "source": "share_map",
        "url": "",
        "_latlng": [round(lat, 6), round(lng, 6)],
    }]


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--wait", type=int, default=11000)
    ap.add_argument("--shot", default="")
    a = ap.parse_args()
    res = fetch(a.url, wait_ms=a.wait, shot_path=(a.shot or None))
    print(f"--- {len(res)} ---")
    for r in res:
        print(r["text"])
        print("latlng:", r.get("_latlng"))
