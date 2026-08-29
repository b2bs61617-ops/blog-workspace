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
