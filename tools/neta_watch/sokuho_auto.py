# -*- coding: utf-8 -*-
"""速報の見張り(2026-11-19〜 トモキ依頼)。neta_watch.py --auto から呼ばれる。マツ(Claude)を使わずPCだけで動く。

- 夜中(0〜6時台)は毎時: Xの「速報」ラベルが付いたニュースを拾う → 大手ニュース(NHK・スポーツ紙など)で裏取り →
  重い話(訃報・逮捕・事件事故・災害・不倫など)かを判定 →
    ・ふつうの話: chomoand.com に記事を書いて公開 → Indexing → @chomotirend(X/Threads)へ投稿
    ・重い話 / 事実チェックNG / Xの写真が無い: 下書きで止める(朝トモキが見て公開)
- 昼(7・13・19時): 速報の一覧だけ集めて、LINEの8時・20時のまとめに入れる(記事は作らない)
- 結果はぜんぶ neta_watch の pending に入れて、LINEのまとめ(8時・20時)で知らせる

決まりごと(トモキ 2026-11-19): 自動で公開するのは0〜7時だけ/重い話は下書き止め/
「速報ラベル + 大手ニュースで確認できたもの」だけ/通知は朝8時のまとめに入れる。

usage:
    python tools/neta_watch/sokuho_auto.py --test        # 今すぐ1回。記事は作るがWordPressには出さない(HTMLを保存するだけ)
    python tools/neta_watch/sokuho_auto.py --list        # 速報の一覧だけ(昼と同じ動き)
"""
import argparse
import asyncio
import datetime
import hashlib
import html as htmllib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

if sys.stdout is None:  # pythonw では画面が無い。print で落ちないように
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
    sys.stderr = sys.stdout

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
REPO = TOOLS.parent
for _p in (TOOLS, TOOLS / "hasshin", TOOLS / "rival_watch", TOOLS / "Xiy", TOOLS / "x-sokuho", TOOLS / "x-trend-monitor", HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import blogkit  # noqa: E402
import hasshin  # noqa: E402

SITE = "trend"
NIGHT_HOURS = tuple(range(0, 7))   # 自動で公開してよい時刻(0:00〜6:59)
DAY_HOURS = (7, 13, 19)            # 昼は一覧だけ
MAX_ARTICLES_PER_RUN = 2
MAX_ARTICLES_PER_NIGHT = 4
MIN_CHARS = 2500                   # docs/rules.md の最低字数
DRAFT_BELOW_CHARS = 2000           # これより短いときは公開しないで下書き
CAT_TREND, CAT_DRAMA = 37, 38
GEMINI_MODELS = ("gemini-flash-latest", "gemini-3.5-flash", "gemini-3-flash-preview", "gemini-flash-lite-latest",
                 "gemini-3.1-flash-lite")

# 裏取りに使う大手ニュース(Google ニュース / Tavily のドメイン)
MAJOR_DOMAINS = (
    "nhk.or.jp", "news.yahoo.co.jp", "kyodonews.jp", "nordot.app", "jiji.com", "asahi.com", "yomiuri.co.jp",
    "mainichi.jp", "nikkei.com", "sankei.com", "tokyo-np.co.jp", "chunichi.co.jp", "47news.jp",
    "nikkansports.com", "sponichi.co.jp", "hochi.news", "sanspo.com", "daily.co.jp", "oricon.co.jp",
    "natalie.mu", "mantan-web.jp", "modelpress.jp", "fnn.jp", "news.tv-asahi.co.jp", "news.ntv.co.jp",
    "newsdig.tbs.co.jp", "tbs.co.jp", "fujitv.co.jp", "excite.co.jp", "news.livedoor.com",
)
# 記事の写真に使ってよいXアカウント(報道・公式)。一般人の投稿の写真は使わない
NEWS_HANDLES = {h.lower() for h in (
    "nhk_news", "nhk_pr", "YahooNewsTopics", "Yahoo_JAPAN_PR", "oricon", "ORICONNEWS", "natalie_mu", "owarai_natalie",
    "eiga_natalie", "comic_natalie", "stage_natalie", "modelpress", "mantanweb", "nikkansports", "nikkan_geinou",
    "Sponichi_Annex", "sponichiannex", "hochi_news", "SANSPOCOM", "Daily_Online", "livedoornews", "kyodo_official",
    "jijicom", "asahi", "Yomiuri_Online", "mainichi", "nikkei", "Sankei_news", "tbsnewsdig", "news24ntv", "ntv_news24",
    "ANNnewsCH", "FNN_News", "fnn_prime", "TOKYOMX", "47news", "Kyodo_English", "cinematoday", "crank_in_net",
    "thetv_jp", "WEBザテレビジョン", "musicnatalie", "barks_news", "sanspo_geino", "daily_geino", "chunichi_sports",
)}
HEAVY_WORDS = ("死去", "死亡", "訃報", "逝去", "亡くな", "急死", "他界", "逮捕", "容疑", "書類送検", "起訴", "送検", "被告",
               "事件", "事故", "火災", "地震", "津波", "噴火", "災害", "殺", "自殺", "不倫", "離婚", "性加害", "性被害",
               "暴行", "被害", "入院", "病気", "闘病", "活動休止", "引退", "謝罪", "不祥事", "炎上")

ACCENT, BORDER, BG = "#c2410c", "#f2c9a8", "#fff7ef"


def log(*a):
    import neta_watch
    neta_watch.log(*a)


# ---------------------------------------------------------------- 小さな部品(テストあり)
def story_key(name):
    return "sokuho:" + re.sub(r"\s+", "", name or "")[:60]


def heavy_by_words(*texts):
    s = " ".join(t or "" for t in texts)
    return [w for w in HEAVY_WORDS if w in s]


def is_major(url):
    host = urllib.parse.urlparse(url or "").netloc.lower()
    return any(host == d or host.endswith("." + d) for d in MAJOR_DOMAINS)


def fix_title(t):
    t = (t or "").strip().replace("?", "？").replace("!", "！").replace("【未】", "")
    # 日本語どうしの間の空白だけ消す(「SIDE by SIDE」のような英語の空白は残す)
    return re.sub(r"(?<=[^\x00-\x7f])\s+|\s+(?=[^\x00-\x7f])", "", t)


def title_ok(t):
    return bool(t) and len(t) <= 35 and t.endswith(("？", "！"))


def clean_slug(s, key):
    s = re.sub(r"[^a-z0-9-]+", "-", (s or "").lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)[:60].strip("-")
    return (s or "sokuho") + "-" + hashlib.md5(key.encode("utf-8")).hexdigest()[:4]


def text_len(html):
    s = re.sub(r"<!--.*?-->|<(script|style|iframe|figure)\b.*?</\1>", "", html, flags=re.S)
    s = htmllib.unescape(re.sub(r"<[^>]+>", "", s))
    return len(re.sub(r"\s+", "", s))


def split_sentences(text):
    """句点ごとに1行にする(docs/rules.md: 句点ごとに<br>)。"""
    if isinstance(text, list):
        return [x.strip() for x in text if x and x.strip()]
    parts = re.split(r"(?<=[。！？])", text or "")
    return [x.strip() for x in parts if x.strip()]


def esc(s):
    return htmllib.escape(s or "", quote=False)


def tonight(now_local):
    return now_local.strftime("%Y-%m-%d")


# ---------------------------------------------------------------- Xの速報を集める
async def _collect(max_stories, seen):
    from playwright.async_api import async_playwright
    import x_collector as xc
    import sokuho_questions as sq
    out = []
    async with async_playwright() as p:
        ctx = await xc.launch_browser_context(p)
        try:
            page = ctx.pages[0] if ctx.pages else await ctx.new_page()
            await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(4000)
            if not await xc.is_x_logged_in(page):
                raise RuntimeError("Xにログインしていない(Xiyのブラウザでログインし直してワン)")
            stories = [t for t in await sq.collect_stories(page, 1) if t.get("sokuho")]
            for t in stories:
                t["key"] = story_key(t["name"])
            new = [t for t in stories if t["key"] not in seen][:max_stories]
            for t in new:
                posts = {}
                if t.get("url"):
                    try:
                        await page.goto(t["url"], wait_until="domcontentloaded", timeout=30000)
                        await page.wait_for_timeout(3500)
                        for _ in range(4):
                            for raw in await page.evaluate(hasshin.X_EXTRACT_JS):
                                if raw.get("id"):
                                    posts.setdefault(raw["id"], raw)
                            await page.evaluate("window.scrollBy(0, 1000)")
                            await page.wait_for_timeout(1500)
                    except Exception as e:  # noqa: BLE001
                        log("  速報の投稿が読めなかった:", t["name"], str(e)[:100])
                t["posts"] = list(posts.values())
                qs = []
                for x in t["posts"]:
                    for q in sq.extract_questions(x.get("text", "")):
                        if q not in qs:
                            qs.append(q)
                t["questions"] = qs[:20]
                out.append(t)
        finally:
            await ctx.close()
    return out


def collect(max_stories, seen):
    return asyncio.run(_collect(max_stories, seen))


# ---------------------------------------------------------------- 裏取り
def google_news(query, hours=24):
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": query + " when:1d", "hl": "ja", "gl": "JP", "ceid": "JP:ja"})
    root = ET.fromstring(hasshin.fetch(url, 20))
    now = datetime.datetime.now(datetime.timezone.utc)
    out = []
    for it in root.iter("item"):
        src = it.find("source")
        src_url = src.get("url") if src is not None else ""
        try:
            from email.utils import parsedate_to_datetime
            d = parsedate_to_datetime(it.findtext("pubDate"))
        except Exception:  # noqa: BLE001
            d = now
        if (now - d).total_seconds() > hours * 3600:
            continue
        out.append({"title": it.findtext("title") or "", "url": it.findtext("link") or "", "source_url": src_url,
                    "source": src.text if src is not None else "", "major": is_major(src_url)})
    return out


def tavily_major(query, e):
    if not e.get("TAVILY_API_KEY"):
        return []
    import ai_hub
    try:
        res = ai_hub.tavily_search(query, e, 8, topic="news", days=2, include_domains=list(MAJOR_DOMAINS))
    except Exception as ex:  # noqa: BLE001
        log("  Tavilyで調べられなかった:", str(ex)[:120])
        return []
    return [r for r in res if is_major(r.get("url"))]


def gemini_json(prompt, parts=()):
    import neta_watch
    from google.genai import types
    client = neta_watch.gemini_client()
    last = None
    # 無料枠はモデルごと。昼の動画解析で1つ目を使い切っていても、ほかのモデルなら動く(2026-11-19に確認)
    for model in dict.fromkeys(GEMINI_MODELS):
        for attempt in range(2):
            try:
                res = client.models.generate_content(model=model, contents=[*parts, prompt],
                                                     config=types.GenerateContentConfig(response_mime_type="application/json"))
                data = neta_watch.parse_json_text(res.text)
                if data is not None:
                    return data
                last = "返事がJSONでない"
            except Exception as ex:  # noqa: BLE001
                last = ex
                if any(s in str(ex) for s in ("503", "UNAVAILABLE", "high demand")) and attempt == 0:
                    time.sleep(20)
                    continue
            break
    raise RuntimeError("Geminiが使えなかった: {}".format(str(last)[:200]))


JUDGE_PROMPT = """あなたは日本のトレンド速報ブログ(芸能・新商品やイベント・スポーツ・恋愛リアリティ番組・ドラマが中心)の編集者です。
Xで「速報」として話題のニュース「{name}」について、下の大手ニュースの記事と照らして、次のJSONだけを返してください。

{{"confirmed": 大手ニュースの記事が同じ出来事を伝えていれば true(名前が似ているだけ・うわさ・憶測なら false),
 "heavy": 人の死・逮捕や容疑・事件・事故・災害・病気・不倫やスキャンダル・離婚・誹謗中傷・謝罪会見など、まちがえると人を傷つける重い話なら true,
 "fit": このブログの読者(芸能・エンタメ・スポーツ・話題の商品やイベントが好きな人)が知りたがる話なら true(政治・国際・経済だけの話は false),
 "category": "芸能|ドラマ|スポーツ|新商品・イベント|その他",
 "names": ["記事に出てくる人物・グループ・番組の名前(正式表記)"],
 "one_line": "何が起きたかを1文で"}}

Xでの説明: {summary}

大手ニュース:
{news}"""


WRITE_PROMPT = """あなたは日本のトレンド速報ブログ chomoand.com のライターです。下の「大手ニュースの記事」だけを根拠に、
速報記事を書いてください。読者が検索しそうな「疑問」に正面から答える記事にします。

話題: {name}
何が起きたか: {one_line}
Xで多かった疑問(？付きの投稿から): {questions}

ルール:
- タイトルは35字以内・疑問形で、最後は全角の「？」か「！」。人物名や番組名を前の方に入れる。
- 書いてよい事実は大手ニュースの記事にあることだけ。分からないことは「まだ発表されていません」と書き、予想するときは「〜とみられます」「〜かもしれません」と予想と分かる書き方にする。
- Xの一般の人の投稿の文をそのまま引用しない。投稿者の名前・アカウントも書かない。「SNSで話題」「元ネタの投稿」の話は書かない。
- 書き手(AI・ライター)を主語にしない。「この記事では〜をまとめました」はOK。
- やさしい言葉で、1文は短く。人名には「さん」を付けない(あとで自動で付ける)。
- 本文(lead・sections・matome の合計)は3000字くらい。H2の見出しは4〜6個で、見出しも疑問に答える形にする。
- 最後のH2の後に「まとめ」を入れる(matome に3〜5個の要点)。
- X投稿文(x_text): @chomotirend用。楽しく、続きが気になる緊迫感のある短い文。1行目にいちばん気になる疑問か意外な事実。
  記事の答え(結論)は書かずヒントだけ。絵文字は全体で1〜3個(🚨⚡😱🔥👀など)。2〜3行・110字以内。人物名か番組名を必ず入れる。
  URL・ハッシュタグ・「コメント欄」「こちら👇」「詳しくは」「記事」などの誘導の言葉は入れない。
- x_tags: ハッシュタグ2〜4個(人物名・番組名・グループ名。芸名と本名が違えば本名のタグも)。半角スペース区切り。
- eyecatch: アイキャッチの文字。main=いちばん大きく出す人物名や話題(10字くらいまで)、top=上の段(15字くらい)、bottom=下の段(15字くらい・タイトルの疑問)。記号は全角。

次のJSONだけを返してください:
{{"title": "...", "slug": "英小文字とハイフンのローマ字(例: kojima-haruna-marriage)",
 "lead": ["導入の文(1要素=1文)", "..."],
 "wakaru": ["この記事でわかること(3〜4個)"],
 "sections": [{{"h2": "見出し", "paras": [["1文", "1文"], ["次の段落の1文"]]}}],
 "matome": ["まとめの要点"],
 "x_text": "...", "x_tags": "#... #...",
 "eyecatch": {{"top": "...", "main": "...", "bottom": "..."}},
 "image_alt": "記事の写真の説明(短く)"}}

大手ニュースの記事:
{news}"""


def news_block(items, per=1500):
    out = []
    for i, x in enumerate(items, 1):
        out.append("[{}] {}\nURL: {}\n{}".format(i, x.get("title", ""), x.get("url", ""), (x.get("content") or "")[:per]))
    return "\n\n".join(out)


# ---------------------------------------------------------------- 記事を組み立てる
def pick_images(story, limit=2):
    """報道・公式アカウントの投稿の写真だけ。[(画像URL, 投稿URL)]"""
    out = []
    for x in story.get("posts", []):
        if (x.get("handle") or "").lower() not in NEWS_HANDLES:
            continue
        imgs = (x.get("images") or []) + (x.get("posters") or [])
        if not imgs:
            continue
        out.append((hasshin.full_size(imgs[0]), "https://x.com/{}/status/{}".format(x["handle"], x["id"])))
        if len(out) >= limit:
            break
    return out


def figure(wp, media_id, post_url, alt):
    m = wp.get("/media/{}".format(media_id))
    sizes = (m.get("media_details") or {}).get("sizes") or {}
    full = sizes.get("full") or {"source_url": m.get("source_url"), "width": 1200, "height": 675}
    large = sizes.get("large") or full
    medium = sizes.get("medium") or large
    return blogkit.Blocks.html(
        '<figure class="wp-block-image size-large">\n'
        '<img src="{l}" alt="{alt}" width="{lw}" height="{lh}" style="max-width:100%;height:auto;" '
        'srcset="{m} {mw}w, {l} {lw}w, {f} {fw}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
        '<figcaption style="font-size:0.8em;color:#888;">出典:{u}</figcaption>\n</figure>'.format(
            l=large["source_url"], lw=large.get("width", ""), lh=large.get("height", ""), alt=esc(alt),
            m=medium["source_url"], mw=medium.get("width", ""), f=full["source_url"], fw=full.get("width", ""),
            u=blogkit.Blocks.link(post_url, post_url)))


def build_html(art, figures, sources):
    b = blogkit.Blocks(ACCENT, BORDER, BG)
    out = b.p(*[esc(x) for x in split_sentences(art.get("lead"))])
    if art.get("wakaru"):
        out += b.wakaru([esc(x) for x in art["wakaru"]])
    if figures:
        out += figures[0]
    for i, sec in enumerate(art.get("sections") or []):
        out += b.h2(esc(sec.get("h2", "")))
        for para in sec.get("paras") or []:
            lines = split_sentences(para)
            if lines:
                out += b.p(*[esc(x) for x in lines])
        if i == 1 and len(figures) > 1:
            out += figures[1]
    if art.get("matome"):
        out += b.h2("まとめ")
        out += b.checks([esc(x) for x in art["matome"]])
    if sources:
        links = [b.link(s["url"], esc(s.get("title") or s["url"])) for s in sources[:4]]
        out += b.p("参考:", *links)
    return out


def make_eyecatch(ey, out_path):
    cmd = [sys.executable.replace("pythonw.exe", "python.exe"), str(TOOLS / "eyecatch_chomoand.py"), "--fallback-ok",
           "--bg-prompt", "breaking news style abstract background, bold diagonal light streaks, vivid gradient, "
                          "right side glowing shapes, left half plain, no text, no people, flat illustration",
           "--main", fix_title(ey.get("main") or "速報"), "--out", str(out_path)]
    for k in ("top", "bottom"):
        if ey.get(k):
            cmd += ["--" + k, fix_title(ey[k])]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if r.returncode != 0 or not out_path.exists():
        raise RuntimeError("アイキャッチが作れなかった: " + (r.stderr or r.stdout)[-200:])
    return out_path


def art_len(art):
    parts = list(art.get("lead") or []) + list(art.get("matome") or [])
    for sec in art.get("sections") or []:
        for para in sec.get("paras") or []:
            parts += split_sentences(para)
    return sum(len(re.sub(r"\s+", "", str(x))) for x in parts)


LENGTHEN_PROMPT = """下のブログ記事(JSON)は本文が{n}字しかありません。3000字以上にしてください。
- 大手ニュースの記事にある事実だけで、各見出しの段落を増やす・見出しを1〜2個足す(読者が気になる疑問に答える見出し)。
- 経歴・これまでの出演作・関係する人の情報など、ニュースに書いてある周辺情報も使ってよい。書いていないことは作らない。
- title・x_text・x_tags・eyecatch・slug はそのまま。同じ形のJSONだけを返してください。

記事:
{art}

大手ニュースの記事:
{news}"""


def lengthen(art, sources):
    """本文が2,500字に足りなければ1回だけ書き足させる(docs/rules.md の最低字数)。"""
    n = art_len(art)
    if n >= MIN_CHARS:
        return art
    try:
        more = gemini_json(LENGTHEN_PROMPT.format(n=n, art=json.dumps(art, ensure_ascii=False), news=news_block(sources)))
    except Exception as ex:  # noqa: BLE001
        log("  書き足せなかった:", str(ex)[:120])
        return art
    if isinstance(more, dict) and more.get("sections") and art_len(more) > n:
        for k in ("title", "x_text", "x_tags", "eyecatch", "slug", "image_alt"):
            more[k] = art.get(k)
        log("  書き足した: {}字 → {}字".format(n, art_len(more)))
        return more
    return art


def write_article(story, judge, sources):
    art = None
    prompt = WRITE_PROMPT.format(name=story["name"], one_line=judge.get("one_line", ""),
                                 questions=" / ".join(story.get("questions", [])[:10]) or "(なし)",
                                 news=news_block(sources))
    for attempt in range(2):
        art = gemini_json(prompt)
        if not isinstance(art, dict):
            continue
        art["title"] = fix_title(art.get("title"))
        if title_ok(art["title"]) and art.get("sections"):
            return lengthen(art, sources)
        prompt += "\n\n(前回のタイトル「{}」はルール違反。35字以内・最後は全角の？か！にして、全体を作り直してください)".format(art["title"])
    raise RuntimeError("記事の形にならなかった(タイトル: {})".format((art or {}).get("title")))


def x_post(art, html):
    import xpost_ideas
    text, tags = (art.get("x_text") or "").strip(), (art.get("x_tags") or "").strip()
    if text and not xpost_ideas.problems(text, tags):
        return text, tags
    try:
        _, ok, _ = xpost_ideas.generate(html, art["title"], account="trend", n=5)
        if ok:
            return ok[0]["text"], ok[0]["tags"]
    except Exception as ex:  # noqa: BLE001
        log("  X文を作り直せなかった:", str(ex)[:120])
    return None, None


# ---------------------------------------------------------------- 1件を処理
def handle_story(story, now_local, allow_publish, test=False):
    """戻り値: LINEのまとめに入れる1件(dict)。"""
    e = blogkit.load_env()
    name = story["name"]
    entry = {"group": "sokuho", "platform": "速報", "account": "X", "title": name[:60],
             "url": story.get("url") or "", "date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "summary": story.get("summary", "")[:200], "neta": [], "ideas": story.get("questions", [])[:2], "folder": ""}
    gn = []
    try:
        gn = google_news(name)
    except Exception as ex:  # noqa: BLE001
        log("  Googleニュースが読めなかった:", str(ex)[:100])
    tv = tavily_major(name, e)
    major_gn = [x for x in gn if x["major"]]
    if not tv and not major_gn:
        entry["summary"] = "(大手ニュースでまだ確認できないので記事にしなかった) " + entry["summary"]
        log("  裏取りできず:", name)
        return entry
    sources = tv or [{"title": x["title"], "url": x["url"], "content": ""} for x in major_gn]
    judge = gemini_json(JUDGE_PROMPT.format(name=name, summary=story.get("summary", ""),
                                            news=news_block(sources + [{"title": x["title"], "url": x["url"]} for x in major_gn[:5]], 800)))
    if not isinstance(judge, dict) or not judge.get("confirmed"):
        entry["summary"] = "(大手ニュースと内容が合わないので記事にしなかった) " + entry["summary"]
        log("  大手ニュースと合わない:", name)
        return entry
    if not judge.get("fit"):
        entry["summary"] = "(このブログ向けの話ではないので見送り) " + (judge.get("one_line") or entry["summary"])
        log("  ブログ向けでない:", name)
        return entry
    words = heavy_by_words(name, story.get("summary"), judge.get("one_line"))
    heavy = bool(judge.get("heavy") or words)
    if not tv:
        entry["summary"] = "(大手ニュースの本文が取れず、記事は書けなかった) " + (judge.get("one_line") or "")
        return entry

    art = write_article(story, judge, tv)
    names = [n for n in judge.get("names") or [] if n]
    reasons = []
    if heavy:
        reasons.append("重い話題({})".format("・".join(words) if words else "AIの判定"))
    if not allow_publish:
        reasons.append("自動で公開する時間(0〜7時)の外")
    imgs = pick_images(story)
    if not imgs:
        reasons.append("報道・公式のXの写真が見つからない")

    if test:
        html = build_html(art, ["<!-- 写真: {} -->\n".format(u) for _, u in imgs], tv)
        p = Path(tempfile.gettempdir()) / "sokuho_test_{}.html".format(hashlib.md5(name.encode()).hexdigest()[:6])
        p.write_text("<h1>{}</h1>\n{}".format(esc(art["title"]), html), encoding="utf-8")
        log("  [テスト] 記事を保存:", p, "/ 字数", text_len(html), "/ 公開しない理由:", reasons or "なし")
        x_text, x_tags = x_post(art, html)
        log("  [テスト] X文:", x_text, x_tags)
        entry["summary"] = "[テスト] " + art["title"]
        return entry

    wp = blogkit.WP(SITE, e)
    figures = []
    for img_url, post_url in imgs:
        try:
            data = hasshin.fetch(img_url, 30, referer="https://x.com/")
            tmp = Path(tempfile.gettempdir()) / "sokuho_{}.jpg".format(hashlib.md5(img_url.encode()).hexdigest()[:10])
            tmp.write_bytes(data)
            figures.append(figure(wp, wp.upload_media(str(tmp), art.get("image_alt") or name), post_url,
                                  art.get("image_alt") or name))
        except Exception as ex:  # noqa: BLE001
            log("  写真を入れられなかった:", str(ex)[:120])
    if not figures and "報道・公式のXの写真が見つからない" not in reasons:
        reasons.append("写真をアップできなかった")
    html = blogkit.finalize(build_html(art, figures, tv), SITE, names)
    n = text_len(html)
    if n < DRAFT_BELOW_CHARS:
        reasons.append("字数が少ない({}字)".format(n))

    key = "sokuho_{}_{}".format(now_local.strftime("%Y%m%d"), hashlib.md5(name.encode()).hexdigest()[:6])
    eyecatch = None
    try:
        eyecatch = make_eyecatch(art.get("eyecatch") or {}, REPO / "images" / (key + "_eyecatch.png"))
    except Exception as ex:  # noqa: BLE001
        log("  ", ex)
    cats = [CAT_DRAMA, CAT_TREND] if judge.get("category") == "ドラマ" else [CAT_TREND]
    slug = clean_slug(art.get("slug"), key)
    try:
        po = blogkit.upload_draft(SITE, key, art["title"], html, slug, cats, eyecatch, art["title"], names, env=e)
    except SystemExit as ex:  # 事実チェックNGなど → 下書きだけにする
        reasons.append("事実チェックで要確認({})".format(str(ex)[:60]))
        po = blogkit.upload_draft(SITE, key, art["title"], html, slug, cats, eyecatch, art["title"], names, env=e, force=True)
    link = "{}/?p={}".format(wp.base, po["id"])
    if reasons:
        entry.update(title=art["title"], url=link,
                     summary="📝下書きで止めた(ID{})。理由: {}。朝に見て公開してワン".format(po["id"], "/".join(reasons)))
        log("  下書きで止めた:", po["id"], reasons)
        return entry
    x_text, x_tags = x_post(art, html)
    res = blogkit.publish(SITE, po["id"], x_text or "", x_tags or "", env=e, x=bool(x_text))
    entry.update(title=art["title"], url=res.get("link") or link,
                 summary="🌙自動で公開した(ID{}・{}字){}".format(po["id"], n, "・X投稿済み" if x_text and res.get("x") else "・Xは出せなかった"))
    log("  自動で公開:", po["id"], art["title"], "X" if res.get("x") else "Xなし")
    return entry


# ---------------------------------------------------------------- 入口(neta_watch から呼ぶ)
def run(state, now, mode, test=False):
    """mode: "night"(記事まで) / "list"(一覧だけ)。neta_watch の state を使う。"""
    now_local = now.astimezone()
    seen = set(state.setdefault("sokuho_seen", []))
    stories = collect(8 if mode == "list" else 4, seen)
    log("速報: 新しい速報 {}件({})".format(len(stories), "記事まで" if mode == "night" else "一覧だけ"))
    nights = state.setdefault("sokuho_night", {})
    made = 0
    for t in stories:
        seen.add(t["key"])
        entry = None
        if mode == "night" and made < MAX_ARTICLES_PER_RUN and nights.get(tonight(now_local), 0) < MAX_ARTICLES_PER_NIGHT:
            log("  速報を調べる:", t["name"])
            try:
                entry = handle_story(t, now_local, allow_publish=now_local.hour in NIGHT_HOURS, test=test)
                if "下書き" in entry["summary"] or "公開" in entry["summary"]:
                    made += 1
                    nights[tonight(now_local)] = nights.get(tonight(now_local), 0) + 1
            except Exception as ex:  # noqa: BLE001
                log("  速報の処理でエラー:", t["name"], str(ex)[:200])
        if entry is None:
            entry = {"group": "sokuho", "platform": "速報", "account": "X", "title": t["name"][:60], "url": t.get("url") or "",
                     "date": now.isoformat(), "summary": (t.get("summary") or "")[:200], "neta": [],
                     "ideas": t.get("questions", [])[:2], "folder": ""}
        if not test:
            state.setdefault("pending", []).append(entry)
        state["sokuho_seen"] = list(seen)[-3000:]
    state["sokuho_night"] = dict(sorted(nights.items())[-14:])
    state["sokuho_last"] = now.isoformat()


def main(argv=None):
    ap = argparse.ArgumentParser(description="速報の見張り")
    ap.add_argument("--test", action="store_true", help="記事まで作るがWordPressには出さない")
    ap.add_argument("--list", action="store_true", help="速報の一覧だけ")
    a = ap.parse_args(argv)
    if not (a.test or a.list):
        ap.print_help()
        return 1
    import neta_watch
    state = neta_watch.load_state() if not a.test else {"sokuho_seen": []}
    now = datetime.datetime.now(datetime.timezone.utc)
    run(state, now, "list" if a.list else "night", test=a.test)
    if a.list:
        for p in state.get("pending", []):
            if p.get("group") == "sokuho":
                print("-", p["title"], p["url"], p["summary"][:80])
        print("(--list はためしなので、記録には残さない)")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
