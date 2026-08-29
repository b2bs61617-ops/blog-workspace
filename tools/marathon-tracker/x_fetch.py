"""指定した X アカウントの最新ツイートを取得する(新規実装・単一アカウント特化)。

- ログイン済みプロファイル ~/marathon_tracker_profile を使う(login.py で作成)。
- アカウントの「ポスト」タブ(https://x.com/<name>)を開いて記事化に必要な最小限だけ抜く。
- リツイート/固定ポストは除外。取得できたものを新しい順で返す。
"""
import asyncio
import os
import re
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

from playwright.async_api import async_playwright

PROFILE_DIR = str(Path.home() / "marathon_tracker_profile")

# ツイート本文/リンクから Google マップ URL を拾う。
_MAPS_RE = re.compile(
    r"(?:https?://)?(?:www\.)?"
    r"(?:maps\.app\.goo\.gl/[A-Za-z0-9_-]+"
    r"|goo\.gl/maps/[A-Za-z0-9_-]+"
    r"|maps\.google\.[a-z.]+/[^\s\"'<>]+"
    r"|google\.[a-z.]+/maps[^\s\"'<>]*)",
    re.I,
)
_TCO_RE = re.compile(r"(?:https?://)?t\.co/[A-Za-z0-9]+", re.I)


def _first_maps_url(cands):
    for c in cands:
        if not c:
            continue
        m = _MAPS_RE.search(c)
        if m:
            u = m.group(0)
            return u if u.lower().startswith("http") else "https://" + u
    return ""


def _channel_kw():
    kw = {}
    ch = os.environ.get("MARATHON_PW_CHANNEL", "").strip()
    if ch:
        kw["channel"] = ch
    return kw


def _expand(url, timeout=12):
    """短縮URL(t.co 等)を最終URLへ展開。失敗で ""。"""
    if not url:
        return ""
    if not url.lower().startswith("http"):
        url = "https://" + url
    try:
        import requests
    except Exception:
        return ""
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout,
                          headers={"User-Agent": "Mozilla/5.0"})
        final = r.url or ""
        if not final or final == url:
            with requests.get(url, allow_redirects=True, timeout=timeout,
                              headers={"User-Agent": "Mozilla/5.0"}, stream=True) as g:
                final = g.url or ""
        return final
    except Exception:
        return ""


def _maps_url_from_strings(cands):
    """本文/リンク文字列の集合から Google マップURLを1つ返す。
    直書きが無ければ t.co を展開して地図なら採用する。"""
    direct = _first_maps_url(cands)
    if direct:
        return direct
    for s in cands:
        if not s:
            continue
        mt = _TCO_RE.search(s)
        if not mt:
            continue
        exp = _expand(mt.group(0))
        if exp and _MAPS_RE.search(exp):
            return exp
    return ""


async def _read_tweet_links(tweet_url, timeout=30000):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            PROFILE_DIR, headless=True, slow_mo=20,
            args=["--disable-blink-features=AutomationControlled"],
            **_channel_kw(),
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        cands = []
        try:
            await page.goto(tweet_url, wait_until="domcontentloaded", timeout=timeout)
            await page.wait_for_timeout(4000)
            art = await page.query_selector('article[data-testid="tweet"]')
            scope = art or page
            for a in await scope.query_selector_all("a[href]"):
                h = (await a.get_attribute("href")) or ""
                if h:
                    cands.append(h)
                dt = ((await a.inner_text()) or "").strip()
                if dt:
                    cands.append(dt)
        except Exception:
            pass
        finally:
            await ctx.close()
        return cands


# --- 追跡班アカウント (@24tv24tv 等) が投げる地図ピン投稿から座標を拾う ---
_Q_RE = re.compile(r"[?&]q=(-?\d{1,2}\.\d+)(?:,|%2c)(-?\d{2,3}\.\d+)", re.I)
_LL_RE = re.compile(r"[?&]ll=(-?\d{1,2}\.\d+)(?:,|%2c)(-?\d{2,3}\.\d+)", re.I)
_ATLL_RE = re.compile(r"/@(-?\d{1,2}\.\d+),(-?\d{2,3}\.\d+)")
_PIN_LAT = (34.9, 36.5)      # 関東ざっくり
_PIN_LNG = (138.7, 140.5)


def _coords_from_str(s):
    if not s:
        return None
    for rx in (_Q_RE, _LL_RE, _ATLL_RE):
        m = rx.search(s)
        if not m:
            continue
        try:
            la, ln = float(m.group(1)), float(m.group(2))
        except ValueError:
            continue
        if _PIN_LAT[0] <= la <= _PIN_LAT[1] and _PIN_LNG[0] <= ln <= _PIN_LNG[1]:
            return (la, ln)
    return None


def latest_pin_from_posts(posts, accounts, expand_limit=3):
    """すでに取得済みの posts から、指定アカウントの最新の地図ピン投稿を1件返す。

    追跡班(@24tv24tv 等)は `maps.google.com/maps?q=<lat>,<lng>` 形式のURLを
    数分おきに投げる。表示URL/本文/`t.co` 展開のどれかから座標を取る。
    戻り値: {"lat","lng","date","text","account","tweet_id"} / 無ければ None。
    """
    accs = {str(a).lstrip("@").lower() for a in accounts}
    cand = [p for p in posts
            if str(p.get("source", "")).lstrip("@").lower() in accs]
    cand.sort(key=lambda x: (_parse_dt(x.get("date", ""))
                             or datetime.min.replace(tzinfo=timezone.utc)),
              reverse=True)
    expands = 0
    for p in cand:
        for s in (p.get("maps_url"), p.get("text")):
            c = _coords_from_str((s or "").replace(" ", ""))
            if c:
                return {"lat": c[0], "lng": c[1], "date": p.get("date", ""),
                        "text": p.get("text", ""),
                        "account": "@" + str(p.get("source", "")).lstrip("@"),
                        "tweet_id": p.get("id", "")}
        tco = p.get("tco_url")
        if tco and expands < expand_limit:
            expands += 1
            c = _coords_from_str(_expand(tco))
            if c:
                return {"lat": c[0], "lng": c[1], "date": p.get("date", ""),
                        "text": p.get("text", ""),
                        "account": "@" + str(p.get("source", "")).lstrip("@"),
                        "tweet_id": p.get("id", "")}
    return None


def map_url_from_tweet(tweet_url):
    """指定した1ツイートを開き、そこに貼られた Google マップURLを返す。無ければ ""。

    @YSB_DANCHO の「本官の現在地」ポストのように、位置共有リンクが t.co / カード表示
    (アンカー文字列は "google.com" だけ)になっていても展開して拾う。
    """
    if not tweet_url:
        return ""
    try:
        cands = asyncio.run(_read_tweet_links(tweet_url))
    except Exception:
        return ""
    return _maps_url_from_strings(cands)


def resolve_danchou_map_url(posts, account, timeout=12):
    """@account の新しい順ポストから最初に見つかる Google マップ URL を返す。

    - まず本文/リンクの表示URLに maps.app.goo.gl 等が入っていないか見る。
    - 見つからず t.co だけのときは HEAD で展開して最終URLが地図なら採用する。
    位置共有リンクは時間で切れて貼り直されるので、毎回いちばん新しいものを拾う。
    """
    acct = account.lstrip("@").lower()
    cand = [p for p in posts
            if str(p.get("source", "")).lstrip("@").lower() == acct]
    cand.sort(key=lambda x: (_parse_dt(x.get("date", ""))
                             or datetime.min.replace(tzinfo=timezone.utc)),
              reverse=True)
    for p in cand:
        if p.get("maps_url"):
            return p["maps_url"]
    for p in cand:
        tco = p.get("tco_url")
        if not tco:
            continue
        exp = _expand(tco, timeout=timeout)
        if exp and _MAPS_RE.search(exp):
            return exp
    return ""


def _parse_dt(s: str):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


async def _scrape_articles(page, limit, want_pinned=False):
    posts = []
    seen = set()
    stable = 0
    for _ in range(12):
        articles = await page.query_selector_all('article[data-testid="tweet"]')
        for art in articles:
            try:
                # リツイートはスキップ(社会的文脈の social context バッジで判定)
                sc = await art.query_selector('[data-testid="socialContext"]')
                if sc:
                    txt = (await sc.inner_text()) or ""
                    if ("さんがリツイート" in txt) or ("reposted" in txt.lower()):
                        continue
                    if not want_pinned and (("固定" in txt) or ("Pinned" in txt)):
                        continue

                link = await art.query_selector('a[href*="/status/"]')
                if not link:
                    continue
                href = await link.get_attribute("href") or ""
                m = re.search(r"/status/(\d+)", href)
                if not m:
                    continue
                tid = m.group(1)
                if tid in seen:
                    continue
                seen.add(tid)

                text_el = await art.query_selector('div[data-testid="tweetText"]')
                text = (await text_el.inner_text()).strip() if text_el else ""

                # 地図リンク検出用に本文＋記事内の全リンク(表示URL/href)を集める
                cand_strings = [text]
                try:
                    for a in await art.query_selector_all("a[href]"):
                        h = (await a.get_attribute("href")) or ""
                        if h:
                            cand_strings.append(h)
                        dt = ((await a.inner_text()) or "").strip()
                        if dt:
                            cand_strings.append(dt)
                except Exception:
                    pass
                maps_url = _first_maps_url(cand_strings)
                tco_url = ""
                if not maps_url:
                    for s in cand_strings:
                        mt = _TCO_RE.search(s or "")
                        if mt:
                            tco_url = mt.group(0)
                            if not tco_url.lower().startswith("http"):
                                tco_url = "https://" + tco_url
                            break

                date_str = ""
                t_el = await art.query_selector("time")
                if t_el:
                    date_str = (await t_el.get_attribute("datetime")) or ""

                author = ""
                a_el = await art.query_selector('div[data-testid="User-Name"]')
                if a_el:
                    author = (await a_el.inner_text()).strip().replace("\n", " ")

                posts.append({
                    "id": tid,
                    "date": date_str,
                    "author": author,
                    "text": text,
                    "url": f"https://x.com/i/status/{tid}",
                    "maps_url": maps_url,
                    "tco_url": tco_url,
                })
            except Exception:
                continue
        if len(posts) >= limit or stable >= 3:
            break
        before = len(posts)
        await page.evaluate("window.scrollBy(0, 1600)")
        await page.wait_for_timeout(900)
        stable = stable + 1 if len(posts) == before else 0
    return posts


async def _collect_account(page, name, limit):
    url = f"https://x.com/{name}"
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(3500)
    return await _scrape_articles(page, limit)


async def _collect_search(page, query, limit):
    url = f"https://x.com/search?q={urllib.parse.quote(query)}&src=typed_query&f=live"
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(3500)
    return await _scrape_articles(page, limit)


async def fetch(accounts, search_fallback=None, limit=30, headless=True):
    """accounts: ["screen_name", ...]  戻り値: 新しい順のツイート list。"""
    out = []
    async with async_playwright() as p:
        # channel は環境変数で上書き可(既定: playwright 同梱 chromium)。
        # 同梱 chromium が無い環境向けに "chrome"/"msedge" を指定できる。
        _kw = {}
        _ch = os.environ.get("MARATHON_PW_CHANNEL", "").strip()
        if _ch:
            _kw["channel"] = _ch
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR, headless=headless, slow_mo=20,
            args=["--disable-blink-features=AutomationControlled"],
            **_kw,
        )
        page = context.pages[0] if context.pages else await context.new_page()
        try:
            for name in accounts:
                name = name.lstrip("@").strip()
                if not name:
                    continue
                try:
                    got = await _collect_account(page, name, limit)
                    for g in got:
                        g["source"] = f"@{name}"
                    out.extend(got)
                except Exception as e:
                    print(f"  [warn] @{name} 取得失敗: {e}")
            if not out and search_fallback:
                try:
                    got = await _collect_search(page, search_fallback, limit)
                    for g in got:
                        g["source"] = f"search:{search_fallback}"
                    out.extend(got)
                except Exception as e:
                    print(f"  [warn] 検索フォールバック失敗: {e}")
        finally:
            await context.close()

    # 重複IDをまとめ、新しい順
    uniq = {}
    for pst in out:
        uniq.setdefault(pst["id"], pst)
    posts = list(uniq.values())
    posts.sort(key=lambda x: (_parse_dt(x["date"]) or datetime.min.replace(tzinfo=timezone.utc)), reverse=True)
    return posts


if __name__ == "__main__":
    import json
    import sys

    accs = sys.argv[1:] or []
    res = asyncio.run(fetch(accs, search_fallback="星野真里 マラソン 現在地", headless=False))
    print(json.dumps(res, ensure_ascii=False, indent=2))
