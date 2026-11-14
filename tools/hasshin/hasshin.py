# -*- coding: utf-8 -*-
"""毎日の発信あつめ(2026-11-14〜)。アイドル本人・公式が出した写真つきの発信を1か所に集める。ネタ探しの出発点。

集める先: 公式YouTube(新着動画のサムネ)/ 公式・本人のX / 公式・本人のInstagram。
元データ: tools/data/sources.json(どのアカウントを見るか)。「checked」に日付が入っているアカウントだけ見る
(なりすましを拾わないため。確かめ方は --check)。
写真はPCの中に保存する(マツが写真を見て「次の疑問」を出すため)。リポジトリには入れない。
Xの返信からは「？」の付いた文だけを抜き出す。書いた人の名前やプロフィールは集めない。

usage:
    python tools/hasshin/hasshin.py                 # 直近30時間ぶんを集めて結果ページを開く
    --hours 48 / --site snowman,travis / --no-x / --no-ig / --no-browser(YouTubeだけ) / --replies 0 / --no-open
    python tools/hasshin/hasshin.py --check         # まだ確かめていないアカウントを開いて、表示名を出す
結果は tools/hasshin/out/日付_時刻/ に出る(index.html・items.json・img/)。
ブラウザはXiyと同じログインずみプロファイル(~/x_collector_profile、使用中なら _2, _3)。Python 3.9対応。
"""
import argparse
import asyncio
import datetime
import html as htmllib
import json
import random
import re
import sys
import urllib.request
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
for _p in (TOOLS, TOOLS / "rival_watch", TOOLS / "Xiy"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import blogkit  # noqa: E402
from rival_watch import parse_date, parse_feed  # noqa: E402

DATA = TOOLS / "data"
SOURCES = DATA / "sources.json"
OUT = HERE / "out"
STATE = HERE / "state.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
YT_FEED = "https://www.youtube.com/feeds/videos.xml?channel_id="
PLATFORM = {"youtube": "YouTube", "x": "X", "instagram": "Instagram"}
MAX_IMAGES = 6          # 1つの発信で保存する写真の上限
IG_OPEN_PER_ACCOUNT = 4  # Instagramで1アカウントにつき開く投稿の上限(開きすぎるとログインを止められる)
X_REPLY_POSTS = 3        # Xで返信を見に行く投稿の上限(1アカウントにつき)
QUESTION_RE = re.compile(r"[？?]")

X_EXTRACT_JS = r"""
() => [...document.querySelectorAll('article[data-testid="tweet"]')].map(a => {
  const t = a.querySelector('time');
  const link = t ? t.closest('a') : null;
  const href = link ? (link.getAttribute('href') || '') : '';
  const m = href.match(/^\/([^/]+)\/status\/(\d+)/);
  const textEl = a.querySelector('[data-testid="tweetText"]');
  const imgs = [...a.querySelectorAll('img[src*="pbs.twimg.com/media"]')].map(i => i.src);
  const posters = [...a.querySelectorAll('video[poster]')].map(v => v.poster);
  const ctx = a.querySelector('[data-testid="socialContext"]');
  return {handle: m ? m[1] : '', id: m ? m[2] : '', datetime: t ? t.getAttribute('datetime') : '',
          text: textEl ? textEl.innerText.trim() : '', images: [...new Set(imgs)], posters: [...new Set(posters)],
          context: ctx ? ctx.innerText : ''};
})
"""

IG_GRID_JS = r"""
(n) => [...document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]')].slice(0, n).map(a => {
  const img = a.querySelector('img');
  return {href: a.getAttribute('href') || '', src: img ? img.src : '', alt: img ? (img.alt || '') : ''};
})
"""

IG_POST_JS = r"""
() => {
  const meta = (p) => { const e = document.querySelector('meta[property="' + p + '"]'); return e ? e.content : ''; };
  // 投稿の日時 = ページの中でいちばん古い日時(コメントの日時は必ず投稿より新しい)
  const times = [...document.querySelectorAll('time[datetime]')].map(e => e.getAttribute('datetime')).filter(Boolean).sort();
  // 投稿の写真だけ。下に並ぶ「ほかの投稿」の小さい写真はリンクに包まれているので外す
  const imgs = [...document.querySelectorAll('main img, article img')]
      .filter(i => (i.src || '').includes('-15/') && i.naturalWidth >= 300 && !i.closest('a[href*="/p/"], a[href*="/reel/"]'))
      .map(i => i.src);
  return {datetime: times.length ? times[0] : '', desc: meta('og:description'), title: meta('og:title'),
          og_image: meta('og:image'), images: [...new Set(imgs)]};
}
"""


# ---------------------------------------------------------------- 純粋関数(テスト対象)
def extract_questions(text):
    """文の中から「？」を含む文だけを取り出す。URL・@あて先は消す。"""
    text = re.sub(r"https?://\S+", "", text or "")
    text = re.sub(r"@\w+", "", text)
    parts = re.split(r"(?<=[？?！!。\n])", text)
    return [s.strip() for s in parts if QUESTION_RE.search(s) and len(s.strip()) >= 4]


def pick_questions(replies, limit=8):
    """返信の一覧から「？」付きの文を集める(同じ文は1つに)。書いた人の名前は持たない。"""
    out, seen = [], set()
    for r in replies:
        for q in extract_questions(r.get("text", "")):
            key = re.sub(r"\s+", "", q)
            if key not in seen:
                seen.add(key)
                out.append(q[:120])
    return out[:limit]


def within(date, now, hours):
    return bool(date) and datetime.timedelta(0) <= (now - date) <= datetime.timedelta(hours=hours)


def active_accounts(sources, sites=None, include_unchecked=False):
    """集める対象の一覧 [(グループ, 種類, アカウント)]。checkedが空のものは、指定が無ければ外す。"""
    out = []
    for site_key, s in blogkit.SITES.items():
        g = s["group"]
        if not g or g not in sources["groups"] or (sites and site_key not in sites):
            continue
        for kind in ("youtube", "x", "instagram"):
            for acc in sources["groups"][g].get(kind, []):
                if kind == "youtube" and not acc.get("channel_id"):
                    continue
                if kind != "youtube" and not (acc.get("checked") or include_unchecked):
                    continue
                out.append((g, kind, acc))
    return out


def ig_code(href):
    m = re.search(r"/(p|reel)/([^/?#]+)", href or "")
    return m.group(2) if m else ""


def ig_caption(desc):
    """Instagramの説明文「124K likes, 541 comments - 名前 - 日付: "本文"」から本文だけを取り出す。本文が無ければ空。"""
    m = re.search(r'[:：]\s*["“](.*)', desc or "", flags=re.S)
    return re.sub(r'["”]\s*\.?\s*$', "", m.group(1).strip()).strip() if m else ""


def x_post_item(raw, group, acc):
    """Xの画面から抜いた1件を、共通の形にする。日時が読めないもの・IDが無いものはNone。"""
    date = parse_date(raw.get("datetime"))
    if not raw.get("id") or not date:
        return None
    ctx = raw.get("context", "")
    return {"key": "x:" + raw["id"], "group": group, "platform": "x", "account": acc.get("name") or acc["handle"],
            "handle": acc["handle"], "url": "https://x.com/{}/status/{}".format(raw.get("handle") or acc["handle"], raw["id"]),
            "date": date, "text": raw.get("text", ""), "image_urls": (raw.get("images") or []) + (raw.get("posters") or []),
            "video": bool(raw.get("posters")), "repost": "リポスト" in ctx or "reposted" in ctx.lower(),
            "pinned": "固定" in ctx or "pinned" in ctx.lower(), "questions": []}


def yt_items(xml_bytes, group, acc):
    out = []
    for e in parse_feed(xml_bytes):
        m = re.search(r"[?&]v=([\w-]{11})|/shorts/([\w-]{11})", e["url"])
        vid = (m.group(1) or m.group(2)) if m else ""
        if not vid or not e["date"]:
            continue
        out.append({"key": "yt:" + vid, "group": group, "platform": "youtube", "account": acc["name"], "handle": "",
                    "url": e["url"], "date": e["date"], "text": e["title"], "video": True, "repost": False, "pinned": False,
                    "image_urls": ["https://i.ytimg.com/vi/{}/hqdefault.jpg".format(vid)], "questions": []})
    return out


def full_size(url):
    """Xの写真は大きいサイズで保存する。"""
    if "pbs.twimg.com/media" not in url:
        return url
    url = re.sub(r"name=\w+", "name=large", url)
    return url if "name=" in url else url + ("&" if "?" in url else "?") + "name=large"


# ---------------------------------------------------------------- 通信
def fetch(url, timeout=20, referer=None):
    headers = {"User-Agent": UA, "Accept-Language": "ja,en;q=0.8"}
    if referer:
        headers["Referer"] = referer
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
        return r.read()


def collect_youtube(accounts, now, hours):
    items, failed = [], []
    for g, kind, acc in accounts:
        if kind != "youtube":
            continue
        for attempt in range(3):
            try:
                items += [i for i in yt_items(fetch(YT_FEED + acc["channel_id"], 15), g, acc) if within(i["date"], now, hours)]
                break
            except Exception as e:  # noqa: BLE001  YouTubeのフィードはときどき一瞬だけ失敗する
                if attempt == 2:
                    failed.append("YouTube {}: {}".format(acc["name"], str(e)[:60]))
    return items, failed


async def fetch_replies(context, it, limit):
    """投稿のページを開いて、返信の文だけを集める(書いた人の名前は持たない)。失敗したら空。"""
    out, seen = [], set()
    page = await context.new_page()
    try:
        await asyncio.sleep(random.uniform(1.5, 3.0))
        await page.goto(it["url"], wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(random.randint(2500, 3500))
        for _ in range(4):
            for raw in await page.evaluate(X_EXTRACT_JS):
                if raw["id"] and "x:" + raw["id"] != it["key"] and raw["id"] not in seen and raw["text"]:
                    seen.add(raw["id"])
                    out.append({"text": raw["text"]})
            if len(out) >= limit:
                break
            await page.evaluate("window.scrollBy(0, {})".format(random.randint(700, 1100)))
            await page.wait_for_timeout(random.randint(1000, 1600))
    except Exception:  # noqa: BLE001
        pass
    finally:
        await page.close()
    return out[:limit]


async def collect_x_account(page, context, g, acc, now, hours, replies, xc):
    await page.goto("https://x.com/" + acc["handle"], wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(random.randint(3000, 4500))
    found = {}
    for _ in range(5):
        for raw in await page.evaluate(X_EXTRACT_JS):
            it = x_post_item(raw, g, acc)
            if it and it["key"] not in found:
                found[it["key"]] = it
        await page.evaluate("window.scrollBy(0, {})".format(random.randint(900, 1400)))
        await page.wait_for_timeout(random.randint(900, 1500))
    if not found and xc.X_BLOCK_TEXT in await page.inner_text("body"):
        raise RuntimeError("Xに止められた")
    if not found:
        raise RuntimeError("投稿が1件も見えなかった")
    items = [i for i in found.values() if within(i["date"], now, hours)]
    items.sort(key=lambda i: i["date"], reverse=True)
    if replies:
        for it in [i for i in items if i["image_urls"] and not i["repost"]][:X_REPLY_POSTS]:
            it["questions"] = pick_questions(await fetch_replies(context, it, replies))
    return items


async def collect_ig_account(page, g, acc, now, hours, seen, xc, cache):
    await page.goto("https://www.instagram.com/{}/".format(acc["handle"]), wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(random.randint(4000, 5500))
    if "/accounts/login" in page.url:
        raise RuntimeError("Instagramにログインしていない")
    await xc.dismiss_instagram_popups(page)
    grid = [c for c in await page.evaluate(IG_GRID_JS, 9) if ig_code(c["href"])]
    if not grid:
        raise RuntimeError("投稿が1件も見えなかった")
    items, opened = [], 0
    for cell in grid:
        code = ig_code(cell["href"])
        key = "ig:" + code
        if key in cache:  # 前に開いた投稿は、開き直さずに覚えている中身を使う
            old = dict(cache[key], date=parse_date(cache[key]["date"]))
            if within(old["date"], now, hours):
                items.append(old)
            continue
        if key in seen or opened >= IG_OPEN_PER_ACCOUNT:
            continue
        opened += 1
        url = "https://www.instagram.com" + cell["href"].split("?")[0]
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(random.randint(3500, 5000))
        await page.keyboard.press("Escape")
        info = await page.evaluate(IG_POST_JS)
        date = parse_date(info["datetime"])
        seen[key] = now.isoformat()
        if not within(date, now, hours):
            continue  # 固定された古い投稿など
        images = list(info["images"])
        for _ in range(MAX_IMAGES - 1):  # 複数枚の投稿は「次へ」を押してめくる
            btn = await page.query_selector("button[aria-label='次へ'], button[aria-label='Next']")
            if not btn:
                break
            try:
                await btn.evaluate("b => b.click()")
            except Exception:  # noqa: BLE001  ボタンが何かに隠れて押せないときは、取れた分だけで進む
                break
            await page.wait_for_timeout(random.randint(900, 1400))
            for src in (await page.evaluate(IG_POST_JS))["images"]:
                if src not in images:
                    images.append(src)
        text = ig_caption(info["desc"])
        item = {"key": key, "group": g, "platform": "instagram", "account": acc.get("name") or acc["handle"],
                "handle": acc["handle"], "url": url, "date": date, "text": text or cell["alt"],
                "image_urls": images or ([info["og_image"]] if info["og_image"] else []), "video": "/reel/" in url,
                "repost": False, "pinned": False, "questions": [], "first_seen": now.isoformat()}
        cache[key] = dict(item, date=date.isoformat())
        items.append(item)
        await page.wait_for_timeout(random.randint(1500, 3000))
    return items


async def collect_browser(accounts, now, hours, replies, seen, cache, do_x=True, do_ig=True):
    from playwright.async_api import async_playwright
    import x_collector as xc
    items, failed = [], []
    targets = [(g, k, a) for g, k, a in accounts if (k == "x" and do_x) or (k == "instagram" and do_ig)]
    if not targets:
        return items, failed
    async with async_playwright() as p:
        context = await xc.launch_browser_context(p)
        page = context.pages[0] if context.pages else await context.new_page()
        try:
            if any(k == "x" for _, k, _ in targets):
                await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(3000)
                if not await xc.is_x_logged_in(page):
                    failed.append("Xにログインしていない(Xの分は飛ばした)")
                    targets = [t for t in targets if t[1] != "x"]
            stop = set()
            for g, kind, acc in targets:
                if kind in stop:
                    continue
                print("  {} {}".format(PLATFORM[kind], acc.get("name") or acc["handle"]), flush=True)
                try:
                    if kind == "x":
                        got = await collect_x_account(page, context, g, acc, now, hours, replies, xc)
                    else:
                        got = await collect_ig_account(page, g, acc, now, hours, seen, xc, cache)
                    items += got
                except Exception as e:  # noqa: BLE001
                    msg = str(e).split("\n")[0][:70]
                    failed.append("{} {}: {}".format(PLATFORM[kind], acc.get("name") or acc["handle"], msg))
                    if "ログインしていない" in msg or "止められた" in msg:
                        stop.add(kind)  # 同じ理由で全部失敗するので、その種類はここでやめる
                await page.wait_for_timeout(random.randint(2000, 4500))
        finally:
            await context.close()
    return items, failed


async def check_accounts(accounts):
    """アカウントを1つずつ開いて、表示名を出す。合っていたら sources.json の checked に今日の日付を入れる(人が見て決める)。"""
    from playwright.async_api import async_playwright
    import x_collector as xc
    async with async_playwright() as p:
        context = await xc.launch_browser_context(p)
        page = context.pages[0] if context.pages else await context.new_page()
        try:
            for g, kind, acc in accounts:
                if kind == "youtube":
                    continue
                url = ("https://x.com/" if kind == "x" else "https://www.instagram.com/") + acc["handle"] + ("" if kind == "x" else "/")
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(4500)
                    if kind == "x":
                        el = await page.query_selector('[data-testid="UserName"]')
                        shown = (await el.inner_text()).replace("\n", " ") if el else "(名前が出ない=無いアカウントかも)"
                        badge = "認証バッジあり" if await page.query_selector('[data-testid="UserName"] [data-testid="icon-verified"]') else "バッジなし"
                    else:
                        shown = await page.evaluate("() => (document.querySelector('meta[property=\"og:title\"]')||{}).content || document.title")
                        badge = "認証バッジあり" if await page.query_selector('header svg[aria-label="認証済み"], header svg[aria-label="Verified"]') else "バッジなし"
                    print("[{}] {} @{} → {} / {}{}".format(g, PLATFORM[kind], acc["handle"], shown, badge,
                                                       " (確認ずみ {})".format(acc["checked"]) if acc.get("checked") else ""), flush=True)
                except Exception as e:  # noqa: BLE001
                    print("[{}] {} @{} → 開けなかった: {}".format(g, PLATFORM[kind], acc["handle"], str(e)[:60]), flush=True)
                await page.wait_for_timeout(random.randint(1500, 3000))
        finally:
            await context.close()
    return 0


def save_images(items, out_dir):
    img_dir = out_dir / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    for it in items:
        it["images"] = []
        for n, url in enumerate(it["image_urls"][:MAX_IMAGES], 1):
            name = "{}_{}_{}.jpg".format(it["group"], re.sub(r"\W+", "", it["key"]), n)
            try:
                data = fetch(full_size(url), 20, referer="https://www.instagram.com/" if it["platform"] == "instagram" else None)
                if len(data) < 2000:
                    continue
                (img_dir / name).write_bytes(data)
                it["images"].append("img/" + name)
            except Exception:  # noqa: BLE001
                continue


# ---------------------------------------------------------------- 出力
def when(d):
    return d.astimezone().strftime("%m/%d %H:%M")


def glabel(g):
    return next((s["label"] for s in blogkit.SITES.values() if s["group"] == g), g)


def to_text(items, failed, out_dir, hours):
    lines = ["発信あつめ(直近{}時間): {}件".format(hours, len(items))]
    cur = None
    for it in items:
        if it["group"] != cur:
            cur = it["group"]
            lines.append("\n■ " + glabel(cur))
        marks = "".join([" [新着]" if it.get("new") else "", " [リポスト]" if it["repost"] else "", " [動画]" if it["video"] else ""])
        lines.append("  {} {} {}{}: {}".format(when(it["date"]), PLATFORM[it["platform"]], it["account"], marks,
                                             it["text"].replace("\n", " ")[:80]))
        lines.append("      " + it["url"])
        for img in it.get("images", []):
            lines.append("      写真: " + str(out_dir / img))
        for q in it["questions"]:
            lines.append("      ファンの疑問: " + q)
    if failed:
        lines.append("\n■ 集められなかったもの\n  " + "\n  ".join(failed))
    return "\n".join(lines)


CSS = """body{font-family:system-ui,sans-serif;margin:0;padding:16px;background:#f6f7f9;color:#222;line-height:1.6;max-width:1000px;margin:auto}
h1{font-size:1.3em}h2{font-size:1.1em;margin-top:26px;border-left:5px solid #c2410c;padding-left:8px}.card{background:#fff;border-radius:8px;
padding:10px 14px;margin:10px 0;box-shadow:0 1px 2px rgba(0,0,0,.08)}.tag{font-size:.8em;background:#eee;border-radius:4px;padding:1px 6px;
margin-right:6px;white-space:nowrap}.new{background:#bbf7d0;color:#14532d}.sub{color:#666;font-size:.88em}a{color:#1d4ed8}
.imgs{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}.imgs img{height:230px;max-width:100%;border-radius:6px;object-fit:cover}
.txt{white-space:pre-wrap;word-break:break-word}.q{background:#fef3c7;border-radius:6px;padding:6px 10px;margin-top:6px;font-size:.92em}
.q li{margin-left:14px}.guide{background:#fff7ed;border:1px solid #fdba74}
@media(prefers-color-scheme:dark){body{background:#16181c;color:#e6e6e6}.card{background:#22252b}.tag{background:#333}.sub{color:#aaa}
a{color:#8ab4f8}.new{background:#14532d;color:#dcfce7}.q{background:#3b2f12}.guide{background:#2b2118;border-color:#7c2d12}}"""

GUIDE = ("<div class='card guide'><b>写真を見るときの6つの方向</b>(みんなが最初に思う「どこで・なぜ・いつ」ではなく、その次の疑問を探す)<br>"
         "① 物(服・小物・車は何か、いくらか) ② 人(だれと一緒か、だれが撮ったか) ③ 場所(どこの店・ロケ地か、行けるか)<br>"
         "④ 前との違い(髪型・持ち物が変わったか) ⑤ 過去(前にも同じことがあったか) ⑥ この後(出演・発売に関係するか)<br>"
         "<span class='sub'>一般の人のアカウントは調べない。答えは本人の発言・公式・報道で確かめる。</span></div>")


def to_html(items, failed, hours, now):
    esc = htmllib.escape
    parts, cur = [GUIDE], None
    for it in items:
        if it["group"] != cur:
            cur = it["group"]
            parts.append("<h2>{}</h2>".format(esc(glabel(cur))))
        tags = '<span class="tag">{}</span>'.format(PLATFORM[it["platform"]])
        tags += '<span class="tag new">新着</span>' if it.get("new") else ""
        tags += '<span class="tag">リポスト</span>' if it["repost"] else ""
        tags += '<span class="tag">動画</span>' if it["video"] else ""
        imgs = "".join('<a href="{0}" target="_blank"><img src="{0}" loading="lazy" alt=""></a>'.format(esc(i)) for i in it.get("images", []))
        qs = ""
        if it["questions"]:
            qs = '<div class="q"><b>返信にあった「？」</b>{}</div>'.format("".join("<li>{}</li>".format(esc(q)) for q in it["questions"]))
        parts.append('<div class="card"><div>{tags}<b>{acc}</b> <span class="sub">{w}</span> <a href="{u}" target="_blank" rel="noopener">元の投稿</a></div>'
                     '<div class="imgs">{imgs}</div><div class="txt">{txt}</div>{qs}</div>'.format(
                         tags=tags, acc=esc(it["account"]), w=when(it["date"]), u=esc(it["url"]), imgs=imgs,
                         txt=esc(it["text"][:500]), qs=qs))
    if failed:
        parts.append("<h2>集められなかったもの</h2><div class='card'>{}</div>".format("<br>".join(esc(f) for f in failed)))
    return ('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            "<title>発信あつめ {t}</title><style>{c}</style></head><body><h1>発信あつめ {t}</h1>"
            '<p class="sub">直近{h}時間に、公式と本人が出した発信 {k}件。写真はこのPCの中だけに保存している(記事にそのまま使わない)。</p>{b}</body></html>'
            ).format(t=now.astimezone().strftime("%Y-%m-%d %H:%M"), c=CSS, h=hours, k=len(items),
                     b="\n".join(parts) if items or failed else "<p>この時間の発信は見つからなかったワン</p>")


def main(argv=None):
    ap = argparse.ArgumentParser(description="毎日の発信あつめ")
    ap.add_argument("--hours", type=int, default=30)
    ap.add_argument("--site", default="")
    ap.add_argument("--no-x", action="store_true")
    ap.add_argument("--no-ig", action="store_true")
    ap.add_argument("--no-browser", action="store_true", help="YouTubeだけ(ブラウザを開かない)")
    ap.add_argument("--replies", type=int, default=25, help="Xで1投稿につき見る返信の数(0で見ない)")
    ap.add_argument("--include-unchecked", action="store_true", help="確かめていないアカウントも見る")
    ap.add_argument("--check", action="store_true", help="アカウントを開いて表示名を出す(確かめ用)")
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args(argv)
    sites = [s.strip() for s in a.site.split(",") if s.strip()] or None
    for s in sites or []:
        if s not in blogkit.SITES:
            print("サイト名がちがうワン:", s)
            return 1
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))
    if a.check:
        return asyncio.run(check_accounts(active_accounts(sources, sites, include_unchecked=True)))

    accounts = active_accounts(sources, sites, a.include_unchecked)
    if not accounts:
        print("集める先が名簿に無いワン(tools/data/sources.json)")
        return 1
    now = datetime.datetime.now(datetime.timezone.utc)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    seen = state.setdefault("seen", {})
    cache = state.setdefault("ig_cache", {})
    print("{}か所を見に行くワン…".format(len(accounts)), flush=True)
    items, failed = collect_youtube(accounts, now, a.hours)
    if not a.no_browser:
        try:
            got, f2 = asyncio.run(collect_browser(accounts, now, a.hours, a.replies, seen, cache, not a.no_x, not a.no_ig))
            items += got
            failed += f2
        except Exception as e:  # noqa: BLE001
            failed.append("ブラウザを開けなかった: {}".format(str(e).split("\n")[0][:100]))
    for it in items:
        it["new"] = it["key"] not in seen or it.get("first_seen") == now.isoformat()
    order = [s["group"] for s in blogkit.SITES.values()]
    items.sort(key=lambda i: (order.index(i["group"]), -i["date"].timestamp()))
    out_dir = OUT / now.astimezone().strftime("%Y%m%d_%H%M")
    save_images(items, out_dir)
    for it in items:
        seen[it["key"]] = seen.get(it["key"]) or now.isoformat()
    state["seen"] = dict(sorted(seen.items(), key=lambda kv: kv[1])[-5000:])
    state["ig_cache"] = dict(sorted(cache.items(), key=lambda kv: kv[1]["date"])[-300:])
    STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    print(to_text(items, failed, out_dir, a.hours))
    (out_dir / "items.json").write_text(json.dumps([dict(i, date=i["date"].isoformat()) for i in items], ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    path = out_dir / "index.html"
    path.write_text(to_html(items, failed, a.hours, now), encoding="utf-8")
    print("\nできたワン:", path)
    if not a.no_open:
        webbrowser.open(path.as_uri())
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
