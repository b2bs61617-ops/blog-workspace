# -*- coding: utf-8 -*-
"""ファンの声あつめ(2026-11-19〜 トモキ依頼)。neta_watch.py --auto のSNSの回(7・13・19・23時)に呼ばれる。
マツ(Claude)を使わずPCだけで動く。

グループ名とメンバーの名前(tools/data/members.json)で X と Threads を検索し、
ファンの投稿・ニュース・コメント欄から「？」付きの疑問を集めて、Gemini(無料)に
「記事にすると読まれそうな疑問」を選ばせる。結果は neta_watch の pending に入り、8時・20時のLINEにのる。

見る範囲(1回あたり):
- 名前ごとに X の「最新」 と Threads の「最近」を、それぞれ上から約30件(SCROLLS回スクロール)
- 前の回より古い投稿は捨てる(初回は直近 FIRST_HOURS 時間)。一度見た投稿も捨てる
- グループ名だけは「話題(人気)」も見て、コメントの多い投稿 REPLY_POSTS 件のコメント欄まで読む(XとThreads)
- うちのアカウント(@chomoand17・@chomotirend)の投稿は数えない
"""
import asyncio
import datetime
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
for _p in (TOOLS, TOOLS / "Xiy", TOOLS / "x-sokuho", TOOLS / "threads-questions"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

MEMBERS = TOOLS / "data" / "members.json"
SCROLLS = 4             # 1つの検索でのスクロール回数(だいたい25〜35件)
REPLY_POSTS = 3         # グループ名の「話題」上位から、コメント欄まで読む投稿の数
FIRST_HOURS = 24        # 初回にさかのぼる時間
MAX_HOURS = 12          # 前の回から時間があいても、これより古い投稿は見ない
MAX_Q_PER_GROUP = 150   # 1グループでGeminiに渡す疑問の上限
PICK_PER_GROUP = 5      # 1グループでLINEにのせる疑問の数
SEEN_KEEP = 6000
# Xの検索はトレンドアカウント(@chomotirend)のブラウザで行う(2026-11-19 トモキ指示。@chomoand17に負担をかけない)
X_PROFILE = str(Path.home() / "x_trend_profile")
X_ACCOUNT = "chomotirend"
OWN_ACCOUNTS = ("chomoand17", "chomotirend", "@chomoand17", "@chomotirend")  # うちの投稿は数えない
QUESTION_RE = re.compile(r"[？?]")
# 「？」が無くても疑問になっている言い方
ASK_RE = re.compile(r"(どこの|どこで|どこに|どこ産|何て曲|なんて曲|何の曲|誰[がのだ]|いつから|いつまで|教えて|知りたい|気になる|わかる人|分かる人|知ってる人|ブランド|特定)")
URL_RE = re.compile(r"(https?://)?[\w.-]+\.(jp|com|net|be|co|me|ly|tv)/\S*")


# ---------------------------------------------------------------- 小さな部品(テストあり)
def keywords_for(group_data):
    """グループ名・よく使う呼び名・メンバー名。[(検索語, グループ名か)]"""
    out = [(group_data["label"], True)]
    out += [(a, False) for a in group_data.get("aliases", []) if len(a) >= 3 and re.search(r"[ぁ-んァ-ヶ一-龥]", a)][:1]
    out += [(m["name"], False) for m in group_data.get("members", [])]
    return out


def extract_questions(text):
    """本文から「？」や「どこの」「教えて」などを含む疑問の文だけ。URLは消す。短すぎるもの・長すぎるものは捨てる。"""
    text = URL_RE.sub("", text or "")
    parts = re.split(r"(?<=[？?！!。\n])", text)
    out = []
    for s in parts:
        s = s.strip().replace("\n", " ")
        if (QUESTION_RE.search(s) or ASK_RE.search(s)) and 6 <= len(s) <= 140:
            out.append(s)
    return out


def parse_time(value):
    try:
        return datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def fresh(post, since):
    """投稿の時刻が since より新しいか(時刻がとれなければ新しい扱い)。"""
    t = parse_time(post.get("time"))
    return t is None or t >= since


def since_time(last_iso, now):
    last = parse_time(last_iso) if last_iso else None
    if not last:
        return now - datetime.timedelta(hours=FIRST_HOURS)
    return max(last, now - datetime.timedelta(hours=MAX_HOURS))


# ---------------------------------------------------------------- ブラウザ
X_JS = """() => [...document.querySelectorAll('article[data-testid="tweet"]')].map(a => {
  const t = a.querySelector('[data-testid="tweetText"]');
  const tm = a.querySelector('time');
  const l = tm ? tm.closest('a') : a.querySelector('a[href*="/status/"]');
  const r = a.querySelector('[data-testid="reply"]');
  return {text: t ? t.innerText : '', time: tm ? tm.getAttribute('datetime') : null,
          url: l ? l.href.split('?')[0] : null, replies: r ? (r.getAttribute('aria-label') || '') : ''};
})"""

TH_JS = """() => [...document.querySelectorAll('div[data-pressable-container="true"]')].map(e => {
  const a = e.querySelector('a[href*="/post/"]');
  const tm = e.querySelector('time');
  return {raw: e.innerText, time: tm ? tm.getAttribute('datetime') : null, url: a ? a.href.split('?')[0] : null};
})"""


async def scroll_collect(page, url, js, to_post, scrolls=SCROLLS, wait=3500):
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(wait)
    posts, stall = {}, 0
    for _ in range(scrolls):
        before = len(posts)
        for c in await page.evaluate(js):
            p = to_post(c)
            if p and p["text"]:
                posts.setdefault(p["url"] or p["text"], p)
        stall = stall + 1 if len(posts) == before else 0
        if stall >= 2:
            break
        await page.evaluate("window.scrollBy(0, {})".format(random.randint(800, 1200)))
        await page.wait_for_timeout(random.randint(1400, 2200))
    return list(posts.values())


def reply_count(label):
    """「12 件の返信。返信する」→12。「1.2万件の返信」→12000。"""
    m = re.search(r"([\d,.]+)\s*(万)?", label or "")
    if not m:
        return 0
    try:
        n = float(m.group(1).replace(",", ""))
    except ValueError:
        return 0
    return int(n * 10000) if m.group(2) else int(n)


def own_account(url):
    return bool(url) and any("/{}/".format(h) in url.lower() for h in OWN_ACCOUNTS)


def x_post(c):
    if own_account(c.get("url")):
        return None
    return {"text": (c.get("text") or "").strip(), "time": c.get("time"), "url": c.get("url"),
            "replies": reply_count(c.get("replies"))}


def th_post(c):
    from threads_questions import post_body
    if own_account(c.get("url")):
        return None
    return {"text": post_body(c.get("raw") or ""), "time": c.get("time"), "url": c.get("url")}


async def launch_x(p):
    import x_collector as xc
    Path(X_PROFILE).mkdir(exist_ok=True)
    ctx = await p.chromium.launch_persistent_context(
        xc.pick_profile(X_PROFILE), headless=False, channel="chrome", slow_mo=50,
        args=["--disable-blink-features=AutomationControlled"])
    if xc.STEALTH_OK:
        await xc.Stealth(**xc.STEALTH_KWARGS).apply_stealth_async(ctx)
    return ctx


async def x_account(page):
    """いまログインしているXのアカウント(「名前 @handle」)。ログインしていなければ空。"""
    await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(4000)
    el = await page.query_selector('[data-testid="SideNav_AccountSwitcher_Button"]')
    return (await el.inner_text()).replace(chr(10), " ") if el else ""


async def login_x(minutes=15):
    """トレンドアカウントでログインしてもらう(初回だけ)。ログインできたら閉じる。"""
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        ctx = await launch_x(p)
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        who = await x_account(page)
        if X_ACCOUNT in who.lower():
            print("もうログインできているワン:", who)
            await ctx.close()
            return True
        await page.goto("https://x.com/login", wait_until="domcontentloaded", timeout=30000)
        print("開いたブラウザで @{} にログインしてワン(最大{}分待つ)".format(X_ACCOUNT, minutes), flush=True)
        for _ in range(minutes * 12):
            await page.wait_for_timeout(5000)
            try:
                el = await page.query_selector('[data-testid="SideNav_AccountSwitcher_Button"]')
                who = (await el.inner_text()).replace(chr(10), " ") if el else ""
            except Exception:  # noqa: BLE001
                who = ""
            if X_ACCOUNT in who.lower():
                print("ログインできたワン:", who, flush=True)
                await page.wait_for_timeout(3000)
                await ctx.close()
                return True
            if who:
                print("別のアカウントでログインしているワン:", who, flush=True)
        await ctx.close()
        return False


async def search_x(groups, since, log):
    from playwright.async_api import async_playwright
    import x_collector as xc
    out = []
    async with async_playwright() as p:
        ctx = await launch_x(p)
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        try:
            who = await x_account(page)
            if X_ACCOUNT not in who.lower():
                log("  X: @{}でログインしていないので飛ばす(いま: {})。`python tools/neta_watch/fan_search.py --login`でログインしてワン".format(
                    X_ACCOUNT, who or "ログインなし"))
                return out
            for g, kws in groups:
                for kw, is_group in kws:
                    try:
                        posts = await scroll_collect(page, xc.build_x_search_url(kw, "live"), X_JS, x_post)
                        posts = [dict(x, group=g, kw=kw, platform="X") for x in posts if fresh(x, since)]
                        if is_group:
                            top = await scroll_collect(page, xc.build_x_search_url(kw, "top"), X_JS, x_post, scrolls=3)
                            cand = {x["url"]: x for x in top + posts if x["url"] and x.get("replies", 0) >= 3}
                            for t in sorted(cand.values(), key=lambda x: -x["replies"])[:REPLY_POSTS]:  # コメントが多い順
                                try:  # 投稿のページ=1件目が元の投稿、下がコメント(時刻の無いものは広告なので外す)
                                    thread = await scroll_collect(page, t["url"], X_JS, x_post, scrolls=4)
                                except Exception:  # noqa: BLE001
                                    thread = []
                                for r in thread:
                                    if r["url"] and r["url"] != t["url"] and r.get("time"):
                                        posts.append({"text": r["text"], "time": None, "url": r["url"], "group": g, "kw": kw,
                                                      "platform": "Xコメント欄"})
                                await page.wait_for_timeout(random.randint(1500, 3000))
                        out += posts
                        log("  X {}: {}件(うちコメント欄 {}件)".format(kw, len(posts), sum(1 for x in posts if x["platform"] == "Xコメント欄")))
                    except Exception as e:  # noqa: BLE001
                        log("  X {}: 失敗 {}".format(kw, str(e).split("\n")[0][:80]))
                    await page.wait_for_timeout(random.randint(2500, 5000))
        finally:
            await ctx.close()
    return out


async def search_threads(groups, since, log):
    from playwright.async_api import async_playwright
    import threads_questions as tq
    from x_collector import pick_profile
    out = []
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            pick_profile(tq.PROFILE_DIR), headless=False, channel="chrome", slow_mo=50,
            args=["--disable-blink-features=AutomationControlled"])
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        try:
            await page.goto(tq.search_url(groups[0][1][0][0], True), wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(5000)
            if not await tq.is_logged_in(page):
                log("  Threads: ログインしていないので飛ばす")
                return out
            for g, kws in groups:
                for kw, is_group in kws:
                    try:
                        posts = await scroll_collect(page, tq.search_url(kw, True), TH_JS, th_post, wait=4000)
                        posts = [dict(x, group=g, kw=kw, platform="Threads") for x in posts if fresh(x, since)]
                        if is_group:  # 人気の投稿のコメント欄(スレッドの2件目から下)
                            top = await scroll_collect(page, tq.search_url(kw, False), TH_JS, th_post, scrolls=2, wait=4000)
                            for t in [x for x in top if x["url"]][:REPLY_POSTS]:
                                try:
                                    thread = await scroll_collect(page, t["url"], TH_JS, th_post, scrolls=3, wait=3500)
                                except Exception:  # noqa: BLE001
                                    thread = []
                                posts += [{"text": x["text"], "time": None, "url": t["url"], "group": g, "kw": kw,
                                           "platform": "Threadsコメント欄"} for x in thread[1:]]
                                await page.wait_for_timeout(random.randint(1500, 3000))
                        out += posts
                        log("  Threads {}: {}件(うちコメント欄 {}件)".format(kw, len(posts), sum(1 for x in posts if x["platform"] == "Threadsコメント欄")))
                    except Exception as e:  # noqa: BLE001
                        log("  Threads {}: 失敗 {}".format(kw, str(e).split("\n")[0][:80]))
                    await page.wait_for_timeout(random.randint(2500, 5000))
        finally:
            await ctx.close()
    return out


# ---------------------------------------------------------------- Gemini
PICK_PROMPT = """あなたは{glabel}のファン向けブログの編集者です。
下はXとThreadsで「{glabel}」やメンバー({members})の名前で検索して集めた、ファンの投稿・コメントの中の「？」付きの文です。
番号: [どこ] 文 の形です。

この中から、ブログ記事にすると多くのファンが検索して読みそうな「疑問」を最大{n}個選んでください。
- 同じことを聞いている文はまとめて1つにし、何件あったか数える
- 選ぶもの: 衣装・アクセサリー・場所・店・番組やCMの内容・発売や放送の日時・メンバーの発言の意味 など、調べれば答えが書けるもの
- 選ばないもの: ただの感想(「かっこよすぎない？」)、{glabel}と関係ない人の話、悪口や個人の詮索、答えの書きようがないもの
- 一般のファン個人のことは書かない

JSONの配列だけを返してください:
[{{"question": "記事のタイトルにできる形の疑問(30字くらい)", "count": 件数, "member": "関係するメンバー名(グループ全体なら空)", "why": "なぜ気になっているか・背景(60字以内)", "nos": [元の番号...]}}]
1つも無ければ [] を返してください。

{lines}"""


def pick_questions(nw, client, model, glabel, members, rows, n=PICK_PER_GROUP):
    from google.genai import types
    lines = "\n".join("{}: [{}] {}".format(i, r["platform"], r["q"]) for i, r in enumerate(rows, 1))
    res = client.models.generate_content(
        model=model, contents=PICK_PROMPT.format(glabel=glabel, members=members, n=n, lines=lines),
        config=types.GenerateContentConfig(response_mime_type="application/json"))
    data = nw.parse_json_text(res.text)
    return [d for d in data if isinstance(d, dict) and d.get("question")] if isinstance(data, list) else []


# ---------------------------------------------------------------- 入口
def run(nw, state, now, log, only_group=None, max_kw=None):
    """nw = neta_watch モジュール(__main__ で動いているものをそのまま渡す)。"""
    groups_data = json.loads(MEMBERS.read_text(encoding="utf-8"))["groups"]
    order = [s["group"] for s in nw.hasshin.blogkit.SITES.values() if s["group"]]
    groups = []
    for g in order:
        if g in groups_data and (not only_group or g == only_group):
            kws = keywords_for(groups_data[g])
            groups.append((g, kws[:max_kw] if max_kw else kws))
    since = since_time(state.get("fan_last"), now)
    log("ファンの声: {}グループ・{}語をXとThreadsで検索({}より新しい投稿)".format(
        len(groups), sum(len(k) for _, k in groups), since.astimezone().strftime("%m/%d %H:%M")))
    posts = asyncio.run(search_x(groups, since, log))
    posts += asyncio.run(search_threads(groups, since, log))

    seen = set(state.get("fan_seen", []))
    folder = nw.day_dir(now) / "ファンの声_{}".format(now.astimezone().strftime("%H%M"))
    memo = ["ファンの声あつめ {}(投稿 {}件)".format(now.astimezone().strftime("%m/%d %H:%M"), len(posts)), ""]
    client = None
    total = 0
    for g, _ in groups:
        rows, qs = [], set()
        for p in posts:
            if p["group"] != g:
                continue
            for q in extract_questions(p["text"]):
                key = q[:60]
                if key in qs or key in seen:
                    continue
                qs.add(key)
                rows.append({"q": q, "platform": p["platform"], "url": p["url"], "kw": p["kw"]})
        rows = rows[:MAX_Q_PER_GROUP]
        seen.update(qs)
        glabel = nw.hasshin.glabel(g)
        memo += ["■{} 「？」の文 {}件".format(glabel, len(rows))]
        if not rows:
            memo.append("")
            continue
        client = client or nw.gemini_client()
        picks = []
        for model in (nw.GEMINI_MODEL,) + tuple(m for m in nw.sokuho_auto.GEMINI_MODELS if m != nw.GEMINI_MODEL):
            try:
                picks = pick_questions(nw, client, model, glabel, nw.member_names(g) or "不明", rows)
                break
            except Exception as e:  # noqa: BLE001
                log("  {} 判定に失敗({}): {}".format(glabel, model, str(e)[:100]))
        for d in picks:
            nos = [n for n in (d.get("nos") or []) if isinstance(n, int) and 1 <= n <= len(rows)]
            src = [rows[n - 1] for n in nos]
            url = next((r["url"] for r in src if r["url"]), "")
            memo.append("★{}({}件){} {}".format(d["question"], d.get("count") or len(src) or 1,
                                               " [" + d["member"] + "]" if d.get("member") else "", d.get("why", "")))
            memo += ["   ・[{}] {} {}".format(r["platform"], r["q"], r["url"] or "") for r in src[:5]]
            state.setdefault("pending", []).append({
                "group": g, "platform": "ファンの疑問", "account": "", "title": d["question"],
                "url": url, "date": now.isoformat(),
                "summary": "{}件の声{}。{}".format(d.get("count") or len(src) or 1,
                                                  "(" + d["member"] + ")" if d.get("member") else "", d.get("why", "")),
                "neta": [], "ideas": [], "folder": str(folder.relative_to(nw.OUT))})
            total += 1
        memo.append("  (ぜんぶの「？」)")
        memo += ["   - [{}/{}] {}".format(r["platform"], r["kw"], r["q"]) for r in rows]
        memo.append("")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "一覧.txt").write_text("\n".join(memo), encoding="utf-8")
    state["fan_seen"] = list(seen)[-SEEN_KEEP:]
    if not (only_group or max_kw):  # ためしの回は時刻を残さない(本番の回が飛ばないように)
        state["fan_last"] = now.isoformat()
    nw.save_state(state)
    log("  ファンの疑問 {}個をLINE待ちに入れた → {}".format(total, folder))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "--login" in sys.argv:
        sys.exit(0 if asyncio.run(login_x()) else 1)
    print("使い方: python tools/neta_watch/fan_search.py --login  (Xのトレンドアカウントでログインする・初回だけ)")
