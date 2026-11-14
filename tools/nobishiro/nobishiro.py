# -*- coding: utf-8 -*-
"""伸びしろ診断(2026-11-14〜)。公開済みの記事を全サイトから集め、「直す順番つきリスト」をHTML+CSVで出す。

記事は読むだけで、書き換えない。鍵が無くても動く(公開記事は認証なしで読める)。
Search Consoleの鍵(.envのGOOGLE_INDEXING_CREDENTIALS_PATH)があれば検索データも足す。無ければ飛ばす。

usage:
    python tools/nobishiro/nobishiro.py                    # 全サイト
    python tools/nobishiro/nobishiro.py --site snowman     # 1サイトだけ(カンマ区切りで複数可)
    --links   動画・X・外部リンクの切れも調べる(時間がかかる。全サイトで10〜20分)
    --no-gsc  Search Consoleを見ない / --no-open 終わってもブラウザを開かない / --limit 50 お試し用
結果は tools/nobishiro/out/ に出る(そのPCにだけ残る)。Python 3.9対応。
"""
import argparse
import csv
import datetime
import html as htmllib
import re
import sys
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import blogkit  # noqa: E402
import fact_check  # noqa: E402

OUT = HERE / "out"
STOP = set("有力 理由 場所 値段 特定 紹介 まとめ 一覧 予想 考察 結果 発表 最新 情報 画像 動画 私服 衣装 ブランド 判明 調査 "
           "何者 本名 年齢 学歴 経歴 家族 彼女 彼氏 結婚 現在 出演 放送 配信 公式 話題 反応 感想 意味 方法 時間 日程 "
           "いつ どこ だれ なぜ 記事 番組 メンバー グッズ ライブ ツアー 公演 会場 写真 愛用 着用 同じ 全部 今日 今年".split())
TOKEN = re.compile(r"[一-龥々ヶ]{2,}|[ァ-ヴー]{3,}|[A-Za-z][A-Za-z0-9.'&!-]{2,}")


# ---------------------------------------------------------------- 1記事を測る
def norm_url(url):
    u = re.sub(r"^https?://(www\.)?", "", htmllib.unescape(url).split("#")[0].split("?")[0])
    return u.rstrip("/").lower()


def measure(post, domain, today):
    """記事1本の数字を出す(ネットを見ない)。"""
    body = post["content"]["rendered"]
    title = htmllib.unescape(re.sub(r"<[^>]+>", "", post["title"]["rendered"])).strip()
    hrefs = [htmllib.unescape(h) for h in re.findall(r'<a\b[^>]*\shref="([^"]+)"', body)]
    internal = [h for h in hrefs if domain in h]
    imgs = re.findall(r"<img\b[^>]*>", body)
    try:
        import easy_read
        easy_ng = len(easy_read.check(body)[0])
    except ImportError:
        easy_ng = 0
    modified = datetime.date.fromisoformat(post["modified"][:10])
    return {
        "id": post["id"], "url": post["link"], "title": title, "slug": post.get("slug", ""),
        "chars": fact_check.char_count(body), "h2": len(re.findall(r"<h2\b", body)), "h3": len(re.findall(r"<h3\b", body)),
        "links_out": len(internal), "out_urls": sorted({norm_url(h) for h in hrefs}),
        "img_no_alt": sum(1 for t in imgs if not re.search(r'\salt="[^"]+"', t)), "imgs": len(imgs),
        "no_eyecatch": not post.get("featured_media"), "hr": bool(re.search(r"<hr\b", body)),
        "easy_ng": easy_ng, "days": (today - modified).days, "published": post["date"][:10],
        "title_len": len(title), "question": title.endswith(("？", "！", "?", "!")),
        "links_in": 0, "dead": [], "gsc": None, "text": fact_check.plain(body),
    }


def count_inbound(rows):
    """全サイトまとめて、ほかの記事からリンクされている数を数える。"""
    by_url = {norm_url(r["url"]): r for r in rows}
    for r in rows:
        for u in r["out_urls"]:
            target = by_url.get(u)
            if target is not None and target is not r:
                target["links_in"] += 1


def score(r):
    """直す優先度の点数と理由。点が高いほど先に直す。"""
    pts, why = 0, []

    def add(n, msg):
        nonlocal pts
        pts += n
        why.append(msg)

    g = r.get("gsc")
    if g:
        if g["impressions"] >= 100 and g["ctr"] < 0.02:
            add(30, "表示{}回なのにクリック{}回(タイトルを見直す)".format(g["impressions"], g["clicks"]))
        if 8 <= g["position"] <= 20 and g["impressions"] >= 30:
            add(25, "検索{:.0f}位(あと少しで上位。加筆・内部リンクで押し上げる)".format(g["position"]))
    if r["dead"]:
        add(min(20 * len(r["dead"]), 40), "リンク切れ{}件".format(len(r["dead"])))
    if r["chars"] < 1500:
        add(25, "{}字(かなり短い)".format(r["chars"]))
    elif r["chars"] < 2500:
        add(15, "{}字(2,500字未満)".format(r["chars"]))
    if r["links_in"] == 0:
        add(15, "どの記事からもリンクされていない")
    if r["links_out"] == 0:
        add(10, "内部リンクが無い")
    if r["no_eyecatch"]:
        add(10, "アイキャッチが無い")
    if r["h2"] < 3:
        add(5, "H2が{}個".format(r["h2"]))
    if r["title_len"] > 35:
        add(5, "タイトル{}字".format(r["title_len"]))
    if not r["question"]:
        add(3, "タイトルが？！で終わっていない")
    if r["img_no_alt"]:
        add(3, "説明文(alt)の無い画像{}枚".format(r["img_no_alt"]))
    if r["hr"]:
        add(3, "区切り線が残っている")
    if r["easy_ng"]:
        add(min(r["easy_ng"], 10), "読みにくい文{}か所".format(r["easy_ng"]))
    if r["days"] > 365:
        add(8, "更新から{}日".format(r["days"]))
    elif r["days"] > 180:
        add(5, "更新から{}日".format(r["days"]))
    return pts, why


# ---------------------------------------------------------------- 内部リンクの案
def title_tokens(title, skip=()):
    out = []
    for t in TOKEN.findall(title):
        if t not in STOP and t not in skip and len(t) >= 3 and t not in out:
            out.append(t)
    return out


def link_ideas(rows, skip_words=(), per_post=3, rare=3):
    """「記事Aの題の言葉が記事Bの本文に出るのに、BからAへのリンクが無い」組。同じサイトの中だけ。"""
    toks = {r["id"]: title_tokens(r["title"], skip_words) for r in rows}
    df = {}
    for ts in toks.values():
        for t in ts:
            df[t] = df.get(t, 0) + 1
    ideas = []
    for b in rows:
        found = []
        for a in rows:
            if a is b or norm_url(a["url"]) in b["out_urls"]:
                continue
            hit = [t for t in toks[a["id"]] if df[t] <= rare and t in b["text"] and t not in b["title"]]
            if hit:
                found.append((sum(len(t) for t in hit), a, hit))
        found.sort(key=lambda x: -x[0])
        ideas += [{"from": b, "to": a, "words": hit, "weight": w} for w, a, hit in found[:per_post]]
    ideas.sort(key=lambda x: -x["weight"])
    return ideas


# ---------------------------------------------------------------- Search Console(あれば)
def fetch_gsc(domain, env, days=28):
    """{正規化URL: {clicks, impressions, ctr, position}}。使えなければ None。"""
    cred = env.get("GOOGLE_INDEXING_CREDENTIALS_PATH")
    if not cred or not Path(cred).exists():
        return None
    try:
        import check_search_console
        session = check_search_console.build_session(cred)
        end = datetime.date.today() - datetime.timedelta(days=2)
        body = {"startDate": str(end - datetime.timedelta(days=days)), "endDate": str(end),
                "dimensions": ["page"], "rowLimit": 5000}
        for site_url in ("sc-domain:" + domain, "https://{}/".format(domain)):
            from urllib.parse import quote
            r = session.post("https://www.googleapis.com/webmasters/v3/sites/{}/searchAnalytics/query"
                             .format(quote(site_url, safe="")), json=body, timeout=60)
            if r.status_code == 200:
                return {norm_url(x["keys"][0]): {"clicks": int(x["clicks"]), "impressions": int(x["impressions"]),
                                                "ctr": x["ctr"], "position": x["position"]} for x in r.json().get("rows", [])}
    except Exception as e:  # noqa: BLE001
        print("  Search Consoleは使えなかった({})".format(str(e)[:60]))
    return None


# ---------------------------------------------------------------- リンク切れ(--links)
def find_dead(rows, workers=12):
    wanted = {}
    for r in rows:
        for u in fact_check.extract_urls(r.pop("_body")):
            if fact_check.classify_url(u) in ("x", "youtube"):
                wanted.setdefault(u, []).append(r)
    urls = list(wanted)
    print("  動画・Xのリンク {}件を確認中…".format(len(urls)))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for u, (state, msg) in zip(urls, ex.map(fact_check.check_url, urls)):
            if state == "dead":
                for r in wanted[u]:
                    r["dead"].append(u)


# ---------------------------------------------------------------- 出力
CSS = """body{font-family:system-ui,sans-serif;margin:0;padding:16px;background:#f6f7f9;color:#222;line-height:1.6}
h1{font-size:1.3em}h2{font-size:1.1em;margin-top:28px}.card{background:#fff;border-radius:8px;padding:12px 14px;margin:8px 0;
box-shadow:0 1px 2px rgba(0,0,0,.08)}.pts{display:inline-block;min-width:2.4em;text-align:center;background:#c2410c;color:#fff;
border-radius:12px;padding:0 8px;font-weight:bold;margin-right:8px}.site{font-size:.8em;background:#eee;border-radius:4px;padding:1px 6px;
margin-right:6px}.why{margin:6px 0 0;padding-left:1.2em;font-size:.92em}a{color:#1d4ed8;word-break:break-all}.sub{color:#666;font-size:.85em}
select,input{font-size:1em;padding:4px;margin:4px 8px 4px 0}@media(prefers-color-scheme:dark){body{background:#16181c;color:#e6e6e6}
.card{background:#22252b}.site{background:#333}.sub{color:#aaa}a{color:#8ab4f8}}"""


def write_html(path, rows, ideas, meta):
    esc = htmllib.escape
    cards = []
    for r in rows:
        g = r.get("gsc")
        sub = "{}字 / H2 {} / リンクされた数 {} / 更新 {}日前".format(r["chars"], r["h2"], r["links_in"], r["days"])
        if g:
            sub += " / 表示{} クリック{} 平均{:.0f}位".format(g["impressions"], g["clicks"], g["position"])
        cards.append('<div class="card" data-site="{k}" data-pts="{p}"><span class="pts">{p}</span><span class="site">{s}</span>'
                     '<a href="{u}" target="_blank" rel="noopener">{t}</a><div class="sub">{sub}</div><ul class="why">{w}</ul></div>'
                     .format(k=r["site"], p=r["score"], s=esc(r["label"]), u=esc(r["url"]), t=esc(r["title"]), sub=esc(sub),
                             w="".join("<li>{}</li>".format(esc(x)) for x in r["why"])))
    idea_cards = []
    for i in ideas:
        idea_cards.append('<div class="card" data-site="{k}"><span class="site">{s}</span><a href="{bu}" target="_blank" rel="noopener">{bt}</a>'
                          '<div class="sub">↑この記事の本文に「{w}」が出てくる → 下の記事へリンクを足す案</div>'
                          '<a href="{au}" target="_blank" rel="noopener">{at}</a></div>'
                          .format(k=i["from"]["site"], s=esc(i["from"]["label"]), bu=esc(i["from"]["url"]), bt=esc(i["from"]["title"]),
                                  w=esc("・".join(i["words"])), au=esc(i["to"]["url"]), at=esc(i["to"]["title"])))
    opts = "".join('<option value="{}">{}</option>'.format(k, esc(v)) for k, v in meta["sites"])
    page = """<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>伸びしろ診断 {date}</title><style>{css}</style></head><body>
<h1>伸びしろ診断 {date}</h1><p class="sub">公開記事 {n}本。点が高いほど先に直すと効く。{gsc}{links}記事は書き換えていない。</p>
<select id="f"><option value="">全サイト</option>{opts}</select><label>点数 <input id="m" type="number" value="20" style="width:4em"> 点以上</label>
<h2>直す順番</h2><div id="list">{cards}</div><h2>内部リンクの案({ni}件)</h2><p class="sub">機械が言葉の一致だけで出した案。関係が薄いものは無視してよい。</p>
<div id="ideas">{ideas}</div>
<script>var f=document.getElementById('f'),m=document.getElementById('m');function go(){{document.querySelectorAll('.card').forEach(function(c){{
var ok=(!f.value||c.dataset.site===f.value)&&(!c.dataset.pts||+c.dataset.pts>=+m.value);c.style.display=ok?'':'none'}})}}
f.onchange=m.oninput=go;go();</script></body></html>""".format(
        date=meta["date"], css=CSS, n=len(rows), opts=opts, cards="\n".join(cards), ideas="\n".join(idea_cards), ni=len(ideas),
        gsc="検索データあり。" if meta["gsc"] else "検索データなし(鍵が無いPC)。", links="リンク切れも確認ずみ。" if meta["links"] else "")
    Path(path).write_text(page, encoding="utf-8")


def write_csv(path, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["サイト", "ID", "点", "タイトル", "URL", "字数", "H2", "H3", "内部リンク", "リンクされた数", "更新からの日数",
                    "表示", "クリック", "CTR", "平均順位", "リンク切れ", "理由"])
        for r in rows:
            g = r.get("gsc") or {}
            w.writerow([r["label"], r["id"], r["score"], r["title"], r["url"], r["chars"], r["h2"], r["h3"], r["links_out"],
                        r["links_in"], r["days"], g.get("impressions", ""), g.get("clicks", ""),
                        "{:.3f}".format(g["ctr"]) if g else "", "{:.1f}".format(g["position"]) if g else "",
                        " ".join(r["dead"]), " / ".join(r["why"])])


def main(argv=None):
    ap = argparse.ArgumentParser(description="伸びしろ診断")
    ap.add_argument("--site", default="")
    ap.add_argument("--links", action="store_true")
    ap.add_argument("--no-gsc", action="store_true")
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args(argv)
    keys = [k.strip() for k in a.site.split(",") if k.strip()] or list(blogkit.SITES)
    env, today = blogkit.load_env(), datetime.date.today()
    groups = fact_check.load_groups()
    skip = {m["name"] for m in fact_check.all_members(groups)} | {c["label"] for c in groups.values()}
    rows, ideas, has_gsc = [], [], False
    for k in keys:
        conf = blogkit.site(k)
        print("{} を読み込み中…".format(conf["label"]), flush=True)
        try:
            posts = blogkit.WP(k, env).public_posts(limit=a.limit)
        except Exception as e:  # noqa: BLE001
            print("  読めなかった({})".format(str(e)[:80]))
            continue
        site_rows = []
        for p in posts:
            r = measure(p, conf["domain"], today)
            r.update({"site": k, "label": conf["label"], "_body": p["content"]["rendered"]})
            site_rows.append(r)
        gsc = None if a.no_gsc else fetch_gsc(conf["domain"], env)
        if gsc:
            has_gsc = True
            for r in site_rows:
                r["gsc"] = gsc.get(norm_url(r["url"]))
        print("  {}本{}".format(len(site_rows), " / 検索データあり" if gsc else ""))
        ideas += link_ideas(site_rows, skip)
        rows += site_rows
    if not rows:
        print("記事が1本も読めなかったワン(ネットを確かめて)")
        return 1
    count_inbound(rows)
    if a.links:
        find_dead(rows)
    for r in rows:
        r.pop("_body", None)
        r["score"], r["why"] = score(r)
    rows.sort(key=lambda r: -r["score"])
    OUT.mkdir(exist_ok=True)
    stamp = today.strftime("%Y%m%d")
    html_path, csv_path = OUT / "nobishiro_{}.html".format(stamp), OUT / "nobishiro_{}.csv".format(stamp)
    meta = {"date": str(today), "gsc": has_gsc, "links": a.links, "sites": [(k, blogkit.SITES[k]["label"]) for k in keys]}
    write_html(html_path, rows, ideas[:300], meta)
    write_csv(csv_path, rows)
    print("できたワン: {}\n          {}".format(html_path, csv_path))
    print("上位5本:")
    for r in rows[:5]:
        print("  {}点 [{}] {} … {}".format(r["score"], r["label"], r["title"][:30], " / ".join(r["why"][:2])))
    if not a.no_open:
        webbrowser.open(html_path.as_uri())
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
