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

# ローマ字の区名 → 漢字(想定ルート沿いの横浜市・川崎市・東京都区部)
_WARD_JP = {
    "Tsuzuki": "都筑区", "Midori": "緑区", "Kohoku": "港北区", "Kōhoku": "港北区",
    "Aoba": "青葉区", "Kanagawa": "神奈川区", "Tsurumi": "鶴見区", "Nishi": "西区",
    "Naka": "中区", "Konan": "港南区", "Kōnan": "港南区", "Totsuka": "戸塚区",
    "Nakahara": "中原区", "Takatsu": "高津区", "Miyamae": "宮前区", "Saiwai": "幸区",
    "Kawasaki": "川崎区", "Tama": "多摩区", "Asao": "麻生区",
    "Setagaya": "世田谷区", "Meguro": "目黒区", "Ota": "大田区", "Ōta": "大田区",
    "Shinagawa": "品川区", "Minato": "港区", "Chuo": "中央区", "Chūō": "中央区",
    "Sumida": "墨田区", "Koto": "江東区", "Kōtō": "江東区", "Chiyoda": "千代田区",
    "Shibuya": "渋谷区", "Shinjuku": "新宿区",
}


def _addr_to_jp(a):
    """共有カードの住所(英語表記が多い)を日本語ラベルに整える。"""
    if not a:
        return ""
    a = a.strip().strip(",")
    # 施設名がそのまま出ているケース(例: 東京アライドコーヒーロースターズ)はそのまま尊重
    a = re.sub(r"^Japan,?\s*", "", a)
    a = re.sub(r"〒?\s*\d{3}-?\d{4}\s*", "", a)
    a = a.replace("Yokohama", "横浜市").replace("Kawasaki", "川崎市").replace("Tokyo", "東京都")
    for en, jp in _WARD_JP.items():
        a = re.sub(rf"\b{en}\s*Ward\b", jp, a)
    a = a.replace(" Ward", "区")
    a = re.sub(r"([A-Za-zĀ-ſ]+)chō(?:me)?\b", lambda m: m.group(1) + ("丁目" if "me" in m.group(0) else "町"), a)
    a = a.replace("-chōme", "丁目").replace("chōme", "丁目").replace("-chō", "町")
    a = re.sub(r"Unnamed Road,?\s*", "", a)          # 「名もなき道」＝河川敷の遊歩道等
    a = re.sub(r"\s*,\s*", "", a)                     # 英語住所のカンマ区切りを詰める
    a = re.sub(r"日本$", "", a).strip()
    # 「神奈川県」等の県名は冗長なので削る(市から始める)
    a = re.sub(r"^(神奈川県|東京都|埼玉県)", "", a)
    return a.strip(" ,、")


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
        return _addr_parts(r.json().get("address", {}))
    except Exception:
        return ""


def _addr_parts(a):
    parts = [a.get(k) for k in ("city", "town", "village", "city_district",
                                "suburb", "neighbourhood", "quarter")]
    parts = [p for p in parts if p]
    return "".join(dict.fromkeys(parts[:3]))


def _geocode_card_addr(raw_addr, hint_lat, hint_lng):
    """共有カードの(英語表記が多い)住所文字列を順ジオコーディングし、
    日本語の市区町村ラベルと座標を得る。hint 座標から離れすぎたら不採用。
    戻り値: (label, lat, lng) / 取れなければ ('', None, None)。"""
    q = re.sub(r"\bUnnamed Road,?\s*", "", (raw_addr or "")).strip()
    if not q:
        return "", None, None
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": q, "format": "json", "accept-language": "ja",
                    "addressdetails": "1", "limit": "1", "countrycodes": "jp"},
            headers={"User-Agent": "marathon-tracker/1.0"}, timeout=15,
        )
        arr = r.json()
        if not arr:
            return "", None, None
        d = arr[0]
        la, ln = float(d["lat"]), float(d["lon"])
        # hint(URLの中心座標)から ~6km 以上離れていたら誤ジオコーディングとみなす
        if hint_lat is not None and (abs(la - hint_lat) > 0.06 or abs(ln - hint_lng) > 0.07):
            return "", None, None
        label = _addr_parts(d.get("address", {}))
        return label, la, ln
    except Exception:
        return "", None, None


def fetch(share_url, wait_ms=11000, shot_path=None):
    if not share_url:
        return []
    try:
        r = asyncio.run(_read(share_url, wait_ms, shot_path))
    except Exception:
        return []
    hint_lat, hint_lng = r.get("lat"), r.get("lng")
    if hint_lat is not None and not (LAT_MIN <= hint_lat <= LAT_MAX and LNG_MIN <= hint_lng <= LNG_MAX):
        return []  # URL中心が明らかに関東外(検出失敗)
    if r.get("stale"):
        return []

    # 位置の"正"は共有カードの住所。それを順ジオコーディングして日本語ラベル＋正確な座標に。
    label, lat, lng = _geocode_card_addr(r.get("addr", ""), hint_lat, hint_lng)
    if not label:
        # ジオコーディング失敗時のフォールバック: URL中心座標の逆引き(粗い)
        if hint_lat is None:
            return []
        label = _reverse_geocode(hint_lat, hint_lng)
        lat, lng = hint_lat, hint_lng
    if not label:
        return []

    now = datetime.now(JST)
    fresh = r.get("fresh", "")
    body = (f"追跡者(@YSB_DANCHO)のリアルタイム位置共有では、現在地は {label} 付近。"
            + (f"(位置情報の更新: {fresh})" if fresh else ""))
    return [{
        "id": f"sharemap:{now:%Y%m%d%H%M}",
        "date": now.isoformat(),
        "author": "share_map",
        "text": body,
        "source": "share_map",
        "url": "",
        "_addr": label,
        "_latlng": [round(lat, 6), round(lng, 6)] if lat is not None else None,
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
