"""サジェスト穴場ファインダー。マツ(Claude)のトークンを使わずに「名前+あいうえお」のネタ探しをする。

やること:
  1. Googleサジェストを「名前 」「名前 あ〜ん」「名前 a〜z」で集める(無料・キー不要)
  2. 各キーワードをYahoo!検索(中身はGoogleと同じ)で上位10件チェックし、競合の強さを判定
       ◎穴場   … タイトルにキーワードを含む記事がほぼ無い
       ○狙える … 少しある
       ×激戦   … 多い / 大手メディアが押さえている
     (Googleを直接見るとCAPTCHAで止められるので Yahoo! を使う。rank_check.py と同じ理由)
  3. ◎と○のキーワードについて、Gemini(無料枠, ai_hub経由)でタイトル案を3つずつ作る
  4. CSV(Excelでそのまま開ける)とHTMLレポートを out/ に出す

実行:
  python tools/suggest-finder/suggest_finder.py "松倉海斗"
  python tools/suggest-finder/suggest_finder.py "松倉海斗" --max 30        # 競合チェックは先頭30件だけ
  python tools/suggest-finder/suggest_finder.py "松倉海斗" --suggest-only  # サジェスト収集だけ(1分)
  python tools/suggest-finder/suggest_finder.py "松倉海斗" --no-ai         # タイトル案を作らない
  run.bat をダブルクリックしても動く(名前を聞かれる)

Yahoo!は連続アクセスするとブロックされるので、1件ごとに数秒空ける。150件で15分前後かかる。
競合チェックの結果は cache/ に7日間とっておくので、途中で止めても再実行すれば続きから進む。
"""
import argparse
import csv
import html
import json
import os
import random
import re
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, urlparse

import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))

OUT_DIR = HERE / "out"
CACHE_FILE = HERE / "cache" / "serp_cache.json"
CACHE_DAYS = 7

HIRAGANA = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
ALPHABET = list("abcdefghijklmnopqrstuvwxyz")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
# Yahoo!の通常の検索結果(知恵袋枠・画像枠などは含まない)
YAHOO_ORGANIC_SELECTOR = ".Algo a.sw-Card__titleInner"

# ドメインの種類。上から順に判定する(blog.livedoor.jp を news.livedoor より先に見る等)
DOMAIN_KINDS = [
    ("qa", ["chiebukuro.yahoo.co.jp", "oshiete.goo.ne.jp", "okwave.jp", "girlschannel.net", "5ch.net",
            "2ch.sc", "bakusai.com", "detail.chiebukuro", "hatelabo.jp", "anond.hatelabo.jp"]),
    ("sns", ["x.com", "twitter.com", "instagram.com", "tiktok.com", "youtube.com", "youtu.be", "facebook.com",
             "threads.net", "threads.com", "lit.link", "linktr.ee"]),
    ("ec", ["amazon.co.jp", "rakuten.co.jp", "mercari.com", "shopping.yahoo.co.jp", "paypayfleamarket",
            "fril.jp", "zozo.jp", "auctions.yahoo.co.jp", "suruga-ya.jp", "famikura-store.jp", "booth.pm"]),
    ("blog", ["ameblo.jp", "hatenablog.com", "hatenablog.jp", "hateblo.jp", "hatenadiary", "note.com",
              "blog.livedoor.jp", "livedoor.blog", "fc2.com", "seesaa.net", "blog.goo.ne.jp", "muragon.com",
              "jugem.jp", "blog.jp", "exblog.jp", "cocolog-nifty.com"]),
    ("strong", ["wikipedia.org", "starto.jp", "oricon.co.jp", "modelpress.jp", "mdpr.jp", "news.yahoo.co.jp",
                "mantan-web.jp", "thetv.jp", "crank-in.net", "natalie.mu", "cinematoday.jp", "nikkansports.com",
                "sponichi.co.jp", "sanspo.com", "hochi.news", "daily.co.jp", "encount.press", "j-cast.com",
                "bunshun.jp", "smart-flash.jp", "jisin.jp", "news-postseven.com", "nhk.or.jp", "tvguide.or.jp",
                "news.livedoor.com", "excite.co.jp", "nifty.com", "biglobe.ne.jp", "jprime.jp", "friday.kodansha.co.jp",
                "vivi.tv", "with-online.jp", "nonno.hpplus.jp", "elle.com", "vogue.co.jp", "ananweb.jp",
                "tv-asahi.co.jp", "ntv.co.jp", "tbs.co.jp", "fujitv.co.jp", "tv-tokyo.co.jp", "baike.baidu.com",
                "weblio.jp", "talent-databank.co.jp", "plus.tver.jp", "tver.jp", "abema.tv", "netflix.com"]),
]
KIND_LABEL = {"qa": "Q&A・掲示板", "sns": "SNS・動画", "ec": "通販", "blog": "ブログ", "strong": "公式・大手",
              "site": "個人/中小サイト", "own": "自サイト"}


# ---------------------------------------------------------------- 純粋関数(テスト対象)

def normalize(text):
    """全角半角・大文字小文字・ひらがなカタカナ・空白の違いを吸収して比較用にする。"""
    t = unicodedata.normalize("NFKC", text or "").lower()
    t = "".join(chr(ord(c) + 0x60) if "ぁ" <= c <= "ゖ" else c for c in t)  # ひらがな→カタカナ
    return re.sub(r"[\s　・\-_/|｜]+", "", t)


def build_queries(name):
    """サジェストを取りに行く検索語の一覧。"""
    base = name.strip()
    return [base + " "] + [f"{base} {c}" for c in HIRAGANA + ALPHABET]


def suffix_of(keyword, name):
    """「松倉海斗 アクスタ 歴代」→「アクスタ 歴代」。名前部分を取り除いた残り。"""
    kw, target = keyword.strip(), normalize(name)
    for i in range(1, len(kw) + 1):
        if normalize(kw[:i]) == target:
            return kw[i:].strip()
    return kw


def classify_domain(url, own_domains=()):
    host = (urlparse(url).hostname or "").lower()
    if any(d and d in host for d in own_domains):
        return "own"
    for kind, domains in DOMAIN_KINDS:
        if any(host == d or host.endswith("." + d) or d in url for d in domains):
            return kind
    return "site"


def title_match(title, name, suffix):
    """full=名前もサジェスト語も全部タイトルに入っている / partial=サジェスト語だけ入っている / none"""
    t = normalize(title)
    words = [normalize(w) for w in re.split(r"[\s　]+", suffix) if normalize(w)]
    if not words:
        return "none"
    if not all(w in t for w in words):
        return "none"
    return "full" if normalize(name) in t else "partial"


def judge(results, name, suffix):
    """上位結果から競合の強さを判定する。results = [{"url","title","kind"}...]"""
    full_blog = full_strong = partial = weak = 0
    own = None
    for r in results:
        m = title_match(r["title"], name, suffix)
        kind = r["kind"]
        if kind == "own":
            own = own or r["url"]
            continue
        if kind in ("qa", "sns"):
            weak += 1
            continue
        if m == "full":
            if kind == "strong":
                full_strong += 1
            elif kind in ("blog", "site"):
                full_blog += 1
        elif m == "partial" and kind in ("blog", "site", "strong"):
            partial += 1
    score = full_blog * 1.0 + full_strong * 2.0 + partial * 0.5
    if score < 1:
        mark = "◎"
    elif score < 3:
        mark = "○"
    else:
        mark = "×"
    return {"mark": mark, "score": score, "full_blog": full_blog, "full_strong": full_strong,
            "partial": partial, "weak": weak, "own": own}


MARK_ORDER = {"◎": 0, "○": 1, "×": 2, "-": 3}


# ---------------------------------------------------------------- 収集

def fetch_suggest(query):
    r = requests.get("https://suggestqueries.google.com/complete/search",
                     params={"client": "firefox", "hl": "ja", "ie": "utf-8", "oe": "utf-8", "q": query},
                     headers={"User-Agent": UA}, timeout=15)
    r.raise_for_status()
    return json.loads(r.content.decode("utf-8"))[1]


def collect_suggestions(name):
    """[(キーワード, 元にした検索語, サジェスト内の順位)] を重複なしで返す。"""
    seen, out = set(), []
    queries = build_queries(name)
    for i, q in enumerate(queries, 1):
        print(f"\rサジェスト収集中 {i}/{len(queries)} 「{q.strip()}」      ", end="", flush=True)
        try:
            items = fetch_suggest(q)
        except Exception as e:  # noqa: BLE001
            print(f"\n  取得失敗({q}): {e}")
            items = []
        for pos, kw in enumerate(items, 1):
            key = normalize(kw)
            if key == normalize(name) or key in seen:
                continue
            seen.add(key)
            out.append({"keyword": kw, "source": q.strip(), "pos": pos})
        time.sleep(0.4)
    print(f"\nサジェスト {len(out)} 件集まったワン")
    return out


def load_cache():
    try:
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}
    limit = time.time() - CACHE_DAYS * 86400
    return {k: v for k, v in data.items() if v.get("ts", 0) > limit}


def save_cache(cache):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")


class YahooBlocked(Exception):
    pass


def yahoo_top(page, keyword, num=10):
    page.goto(f"https://search.yahoo.co.jp/search?p={quote(keyword)}", wait_until="domcontentloaded", timeout=30000)
    try:
        page.wait_for_selector(YAHOO_ORGANIC_SELECTOR, timeout=8000)
    except Exception:  # noqa: BLE001
        body = page.inner_text("body")[:2000]
        if any(s in body for s in ("ロボット", "アクセスが集中", "一時的にご利用", "captcha", "CAPTCHA")):
            raise YahooBlocked(body[:200])
        return [], 0  # 本当に結果が0件
    raw = page.eval_on_selector_all(
        YAHOO_ORGANIC_SELECTOR,
        "els => els.map(e => ({url: e.href, title: ((e.querySelector('h3')||e).innerText||'').trim()}))")
    chiebukuro = page.eval_on_selector_all("a[href*='chiebukuro.yahoo.co.jp/qa/']", "els => els.length")
    seen, out = set(), []
    for r in raw:
        u = r["url"].split("#")[0]
        if not r["title"] or u in seen or "search.yahoo.co.jp" in u:
            continue
        seen.add(u)
        out.append({"url": u, "title": r["title"]})
    return out[:num], chiebukuro


def check_competition(items, name, own_domains, max_n, headless=True):
    from playwright.sync_api import sync_playwright

    cache = load_cache()
    targets = items[:max_n] if max_n else items
    todo = [it for it in targets if it["keyword"] not in cache]
    print(f"競合チェック {len(targets)} 件(うちキャッシュ済み {len(targets) - len(todo)} 件)")
    if todo:
        eta = len(todo) * 6 // 60 + 1
        print(f"  Yahoo!を1件ずつ見るので、だいたい {eta} 分かかるワン。途中で止めても次回は続きから")
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(channel="chrome", headless=headless)
            except Exception:  # noqa: BLE001  Chrome未インストールのPCは同梱Chromiumで
                browser = p.chromium.launch(headless=headless)
            page = browser.new_context(locale="ja-JP", user_agent=UA, viewport={"width": 1280, "height": 1600}).new_page()
            try:
                for i, it in enumerate(todo, 1):
                    kw = it["keyword"]
                    print(f"\r  {i}/{len(todo)} 「{kw}」                    ", end="", flush=True)
                    try:
                        got = yahoo_top(page, kw)
                    except YahooBlocked:
                        print("\nYahoo!にブロックされたので一旦ここで止めるワン。時間を置いて再実行すると続きからやるワン")
                        break
                    except Exception as e:  # noqa: BLE001
                        print(f"\n  失敗: {kw}: {e}")
                        continue
                    top, chie = got
                    cache[kw] = {"ts": time.time(), "top": top, "chiebukuro": chie}
                    if i % 5 == 0:
                        save_cache(cache)
                    time.sleep(random.uniform(3.5, 6.5))
            finally:
                save_cache(cache)
                browser.close()
            print()
    for it in items:
        c = cache.get(it["keyword"])
        if not c:
            it.update({"mark": "-", "score": None, "top": [], "chiebukuro": 0})
            continue
        top = [dict(r, kind=classify_domain(r["url"], own_domains)) for r in c["top"]]
        it["top"] = top
        it["chiebukuro"] = c.get("chiebukuro", 0)
        it.update(judge(top, name, suffix_of(it["keyword"], name)))
    return items


# ---------------------------------------------------------------- タイトル案(Gemini)

def make_titles(items, name, limit=60):
    try:
        import ai_hub
    except Exception as e:  # noqa: BLE001
        print(f"ai_hub が読めないのでタイトル案はスキップ: {e}")
        return
    targets = [it for it in items if it.get("mark") in ("◎", "○")][:limit]
    if not targets:
        return
    env = ai_hub.load_env()
    for start in range(0, len(targets), 20):
        chunk = targets[start:start + 20]
        kws = "\n".join(f"- {it['keyword']}" for it in chunk)
        prompt = (
            f"芸能トレンドブログ(女性ファン向け)の記事タイトルを考えて。対象は「{name}」。\n"
            "以下の各検索キーワードについて、タイトル案を3つずつ。\n"
            "ルール:\n"
            "- キーワードの語句をそのまま全部含め、なるべく前半に置く\n"
            "- 28〜36文字。検索した人の疑問に答える形(「〜は？」「〜まとめ」「〜を調査」など)\n"
            "- 事実を断定しない。数字や固有名詞を勝手に作らない\n"
            "- 【】は1つまで\n"
            '出力はJSONのみ: {"キーワード": ["案1", "案2", "案3"], ...}\n\n'
            f"{kws}"
        )
        try:
            used, text = ai_hub.call(prompt, env=env)
            data = json.loads(ai_hub.strip_fences(text))
        except Exception as e:  # noqa: BLE001
            print(f"タイトル案の作成に失敗(この20件はスキップ): {str(e)[:200]}")
            continue
        norm = {normalize(k): v for k, v in data.items()}
        for it in chunk:
            it["titles"] = list(norm.get(normalize(it["keyword"]), []))[:3]
        print(f"タイトル案 {start + len(chunk)}/{len(targets)} 件できたワン({used})")


# ---------------------------------------------------------------- 出力

def own_domains_from_env():
    try:
        import ai_hub
        env = ai_hub.load_env()
    except Exception:  # noqa: BLE001
        return []
    return [urlparse(v).hostname for k, v in env.items() if k.startswith("WP_") and k.endswith("_URL") and v]


def write_csv(items, path):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["判定", "キーワード", "スコア", "完全一致ブログ", "完全一致大手", "部分一致", "Q&A・SNS",
                    "知恵袋", "自サイト", "タイトル案1", "タイトル案2", "タイトル案3", "上位10件"])
        for it in items:
            t = (it.get("titles") or []) + ["", "", ""]
            top = " / ".join(f"{r['title']}({KIND_LABEL[r['kind']]})" for r in it.get("top", []))
            w.writerow([it["mark"], it["keyword"], "" if it.get("score") is None else it["score"],
                        it.get("full_blog", ""), it.get("full_strong", ""), it.get("partial", ""), it.get("weak", ""),
                        it.get("chiebukuro", ""), it.get("own") or "", t[0], t[1], t[2], top])


def write_html(items, name, path):
    e = html.escape
    counts = {m: sum(1 for it in items if it["mark"] == m) for m in ("◎", "○", "×", "-")}
    rows = []
    for it in items:
        kw = it["keyword"]
        top = "".join(
            f'<li><span class="k k-{r["kind"]}">{e(KIND_LABEL[r["kind"]])}</span>'
            f'<a href="{e(r["url"])}" target="_blank" rel="noopener">{e(r["title"])}</a></li>'
            for r in it.get("top", []))
        titles = "".join(f"<li>{e(t)}</li>" for t in it.get("titles") or [])
        stats = "" if it.get("score") is None else (
            f'完全一致 ブログ{it["full_blog"]}・大手{it["full_strong"]} / 部分一致{it["partial"]} / '
            f'Q&A・SNS{it["weak"]} / 知恵袋{it["chiebukuro"]}')
        own = f'<div class="own">自サイトが上位にいる: <a href="{e(it["own"])}" target="_blank">{e(it["own"])}</a></div>' if it.get("own") else ""
        rows.append(
            f'<tr data-mark="{it["mark"]}"><td class="m m{MARK_ORDER[it["mark"]]}">{it["mark"]}</td>'
            f'<td><b>{e(kw)}</b><div class="links">'
            f'<a href="https://www.google.com/search?q={quote(kw)}" target="_blank">Google</a> '
            f'<a href="https://search.yahoo.co.jp/search?p={quote(kw)}" target="_blank">Yahoo!</a></div>'
            f'<div class="stats">{stats}</div>{own}</td>'
            f'<td>{"<ol>" + titles + "</ol>" if titles else ""}</td>'
            f'<td>{"<details><summary>上位" + str(len(it.get("top", []))) + "件</summary><ol class=top>" + top + "</ol></details>" if top else ""}</td></tr>')
    doc = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(name)} サジェスト穴場</title>
<style>
body{{font-family:"Yu Gothic UI","Meiryo",sans-serif;margin:16px;background:#f6f5f8;color:#222}}
h1{{font-size:20px}} .sum span{{margin-right:14px;font-weight:bold}}
.filters button{{margin:8px 6px 12px 0;padding:6px 12px;border:1px solid #bbb;border-radius:16px;background:#fff;cursor:pointer}}
.filters button.on{{background:#4a3548;color:#fff}}
table{{border-collapse:collapse;width:100%;background:#fff}} td{{border-bottom:1px solid #e3e0e6;padding:8px;vertical-align:top;font-size:14px}}
td.m{{font-size:22px;text-align:center;width:40px}} .m0{{color:#d4145a}} .m1{{color:#e08a00}} .m2{{color:#999}}
.links a{{font-size:12px;margin-right:8px}} .stats{{font-size:12px;color:#666;margin-top:4px}} .own{{font-size:12px;color:#0a7}}
ol{{margin:0;padding-left:20px}} .top li{{margin:2px 0}}
.k{{display:inline-block;font-size:11px;padding:0 6px;border-radius:8px;margin-right:6px;background:#eee}}
.k-blog,.k-site{{background:#ffe1ec}} .k-strong{{background:#d6e4ff}} .k-qa,.k-sns{{background:#e3f6e3}} .k-own{{background:#c9f2e6}}
</style></head><body>
<h1>{e(name)} のサジェスト穴場チェック</h1>
<div class="sum">{datetime.now():%Y-%m-%d %H:%M} / 全{len(items)}件
<span class="m0">◎穴場 {counts["◎"]}</span><span class="m1">○狙える {counts["○"]}</span><span class="m2">×激戦 {counts["×"]}</span><span>未チェック {counts["-"]}</span></div>
<div class="filters"><button class="on" data-f="all">全部</button><button data-f="◎">◎だけ</button><button data-f="◎○">◎と○</button><button data-f="×">×だけ</button></div>
<table>{"".join(rows)}</table>
<script>
document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{{
  document.querySelectorAll('.filters button').forEach(x=>x.classList.toggle('on',x===b));
  const f=b.dataset.f;
  document.querySelectorAll('tr[data-mark]').forEach(tr=>tr.style.display=(f==='all'||f.includes(tr.dataset.mark))?'':'none');
}});
</script></body></html>"""
    Path(path).write_text(doc, encoding="utf-8")


def safe_filename(s):
    return re.sub(r'[\\/:*?"<>|\s]+', "_", s).strip("_") or "result"


def main(argv=None):
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description="Googleサジェスト×競合チェックで穴場キーワードを探す")
    ap.add_argument("name", nargs="?", help="人の名前など(例: 松倉海斗)")
    ap.add_argument("--max", type=int, default=0, help="競合チェックする件数の上限(0=全部)")
    ap.add_argument("--suggest-only", action="store_true", help="サジェスト収集だけして終わる")
    ap.add_argument("--no-ai", action="store_true", help="タイトル案を作らない")
    ap.add_argument("--show", action="store_true", help="ブラウザ画面を表示して実行(デバッグ用)")
    ap.add_argument("--no-open", action="store_true", help="終わったあとにレポートを開かない")
    args = ap.parse_args(argv)

    name = args.name or input("調べたい名前を入力してください: ").strip()
    if not name:
        raise SystemExit("名前が空だワン")

    items = collect_suggestions(name)
    if not items:
        raise SystemExit("サジェストが1件も取れなかったワン")

    if args.suggest_only:
        for it in items:
            it.update({"mark": "-", "score": None, "top": []})
    else:
        check_competition(items, name, own_domains_from_env(), args.max, headless=not args.show)
        if not args.no_ai:
            make_titles(items, name)

    items.sort(key=lambda it: (MARK_ORDER[it["mark"]], it["score"] if it.get("score") is not None else 99))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = OUT_DIR / f"{safe_filename(name)}_{datetime.now():%Y%m%d_%H%M}"
    write_csv(items, f"{stem}.csv")
    write_html(items, name, f"{stem}.html")
    marks = {m: sum(1 for it in items if it["mark"] == m) for m in ("◎", "○", "×")}
    print(f"\n完了だワン！ ◎{marks['◎']} ○{marks['○']} ×{marks['×']}")
    print(f"  {stem}.html\n  {stem}.csv")
    if not args.no_open:
        try:
            os.startfile(f"{stem}.html")  # noqa: S606 (Windows専用)
        except Exception:  # noqa: BLE001
            pass


if __name__ == "__main__":
    main()
