"""追跡者(@YSB_DANCHO)が公開している Google マップの「リアルタイム位置共有」リンクを
ヘッドレスブラウザで開き、地図の焦点座標(＝共有ピン位置)をネットワーク要求から拾って
逆ジオコーディングし、x_fetch と同じ形の post dict を返す。

- Google は位置共有の座標を DOM/URL には出さないが、地図描画に伴う
  `/maps/preview/pegman` などの要求 URL に焦点座標が乗る。それを拾う。
- 座標が日本(関東)の妥当な範囲に無い/ばらつきすぎる場合は何も返さない(記事は触られない)。

post dict:
  {"id","date"(ISO8601 JST),"author":"share_map","text","source":"share_map","url":""}
"""
import asyncio
import re
import statistics
from datetime import datetime, timedelta, timezone

import requests

JST = timezone(timedelta(hours=9))

# 関東のざっくり妥当範囲(神奈川〜東京〜埼玉南部)
LAT_MIN, LAT_MAX = 35.10, 36.30
LNG_MIN, LNG_MAX = 138.90, 140.30

_COORD_RE = re.compile(r"(3[5-6]\.\d{4,}),(-?1[0-9]{2}\.\d{4,})")


def _reverse_geocode(lat, lng):
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
        # 「横浜市」＋「港北区」＋「小机町」のように市区町村＋小地名を優先で組み立て
        label = "".join(dict.fromkeys(parts[:3]))
        return label or r.json().get("display_name", "").split(",")[0]
    except Exception:
        return ""


async def _collect_coords(share_url, wait_ms):
    from playwright.async_api import async_playwright

    coords = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={"width": 1200, "height": 800},
                                  locale="ja-JP", timezone_id="Asia/Tokyo")
        pg = await ctx.new_page()

        async def on_resp(resp):
            u = resp.url
            if "pegman" not in u and "/maps/preview/" not in u and "/maps/vt" not in u:
                return
            for m in _COORD_RE.finditer(u):
                try:
                    la, ln = float(m.group(1)), float(m.group(2))
                except ValueError:
                    continue
                if LAT_MIN <= la <= LAT_MAX and LNG_MIN <= ln <= LNG_MAX:
                    coords.append((la, ln))

        pg.on("response", on_resp)
        try:
            await pg.goto(share_url, wait_until="domcontentloaded", timeout=40000)
            await pg.wait_for_timeout(wait_ms)
        except Exception:
            pass
        try:
            await b.close()
        except Exception:
            pass
    return coords


def _consensus(coords):
    """関東内の座標群から代表点を1つ。ばらつきすぎたら None。"""
    if not coords:
        return None
    if len(coords) == 1:
        return coords[0]
    lats = sorted(c[0] for c in coords)
    lngs = sorted(c[1] for c in coords)
    mlat = statistics.median(lats)
    mlng = statistics.median(lngs)
    # 中央値から ~3km 以内の点だけ採用
    near = [c for c in coords
            if abs(c[0] - mlat) < 0.03 and abs(c[1] - mlng) < 0.035]
    if len(near) < max(2, len(coords) // 3):
        return None
    return (statistics.mean([c[0] for c in near]),
            statistics.mean([c[1] for c in near]))


def fetch(share_url, wait_ms=13000):
    if not share_url:
        return []
    try:
        coords = asyncio.run(_collect_coords(share_url, wait_ms))
    except Exception:
        return []
    pt = _consensus(coords)
    if not pt:
        return []
    lat, lng = pt
    label = _reverse_geocode(lat, lng)
    now = datetime.now(JST)
    body = f"追跡者(@YSB_DANCHO)が公開しているGoogleマップのリアルタイム位置共有より、現在地はおおよそ {label}（緯度{lat:.5f}／経度{lng:.5f}）付近。"
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
    ap.add_argument("--wait", type=int, default=13000)
    a = ap.parse_args()
    for r in fetch(a.url, wait_ms=a.wait):
        print(r["text"])
        print("latlng:", r.get("_latlng"))
    else:
        pass
