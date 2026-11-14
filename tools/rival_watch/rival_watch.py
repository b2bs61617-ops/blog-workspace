# -*- coding: utf-8 -*-
"""ライバルブログ見張り(2026-11-14〜)。ほかのアイドル専門ブログの新着タイトルを毎日集めて、
「何のネタを・どのブログが・いつ書いたか」を一覧にする。本文は読まない(タイトルとURLだけ)。

元データ: tools/data/rivals.json(見張るブログ)+ tools/data/members.json(名前でグループ分け)。
分かること: ① 複数のブログが同時に書いたネタ(需要が高い) ② グループ別の新着 ③ ネタの種類の数(ライバルが何を気にしているか)。

usage:
    python tools/rival_watch/rival_watch.py                     # 新着を集めて結果ページを開く(直近48時間)
    --hours 72 / --site snowman / --no-own / --no-open
    python tools/rival_watch/rival_watch.py --add https://example.com/ --group snowman   # 見張るブログを足す
    python tools/rival_watch/rival_watch.py --discover --site snowman                    # ライバル候補をYahoo!検索から探す
    python tools/rival_watch/rival_watch.py --discover --site snowman --save             # 見つけた候補を名簿に足す
結果は tools/rival_watch/out/ に出る。標準ライブラリだけで動く(--discover だけ playwright が要る)。Python 3.9対応。
"""
import argparse
import datetime
import email.utils
import html as htmllib
import json
import re
import sys
import time
import urllib.request
import webbrowser
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlparse

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import blogkit  # noqa: E402

DATA = TOOLS / "data"
RIVALS = DATA / "rivals.json"
OUT = HERE / "out"
STATE = HERE / "state.json"
HISTORY = HERE / "history.jsonl"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
FEED_GUESSES = ["feed/", "feed", "?feed=rss2", "rss", "rss.xml", "atom.xml", "index.rdf", "index.xml", "feed.xml"]
# ブログサービスは1つのドメインにたくさんのブログが入っているので、ユーザー名までを1ブログとして数える
SHARED_HOSTS = ("ameblo.jp", "note.com", "blog.livedoor.jp", "plaza.rakuten.co.jp", "blog.goo.ne.jp")

# ネタの種類。上から順に見て、最初に当たったものにする(「私服のブランド」は私服、「ロケ地のお店」はロケ地)
TOPICS = [
    ("熱愛・結婚", ["熱愛", "彼女", "彼氏", "匂わせ", "交際", "破局", "好きなタイプ", "元カノ", "結婚相手", "結婚発表", "結婚して", "結婚した",
                "結婚は", "結婚？", "結婚!", "結婚！", "既婚", "お嫁", "妻は"]),
    ("学歴・家族", ["学歴", "高校", "大学", "中学", "出身", "実家", "家族", "兄弟", "父親", "母親", "本名", "身長", "年齢", "プロフィール", "経歴"]),
    ("ロケ地・お店", ["ロケ地", "撮影場所", "聖地", "式場", "どこの店", "お店", "カフェ", "レストラン", "ホテル", "旅館", "店舗", "行き方", "場所はどこ"]),
    ("食べ物・買える物", ["食べた", "どこで買える", "お取り寄せ", "スイーツ", "シュークリーム", "フィナンシェ", "ケーキ", "チョコ", "弁当", "ラーメン",
                  "差し入れ", "メニュー", "レシピ", "お菓子", "パン", "ドリンク", "手土産"]),
    ("私服・愛用品", ["私服", "衣装", "着用", "ブランド", "愛用", "私物", "香水", "時計", "指輪", "ネックレス", "ピアス", "バッグ", "リュック",
                 "スニーカー", "靴", "帽子", "キャップ", "メガネ", "サングラス", "パーカー", "ニット", "コート", "ジャケット", "シャツ",
                 "アクセ", "リップ", "コスメ", "スマホケース", "愛車", "バイク", "おそろい", "プレゼント", "チャーム", "家電", "どこの？"]),
    ("チケット・ライブ", ["チケット", "当落", "倍率", "リセール", "一般発売", "セトリ", "ライブ", "ツアー", "ドーム", "座席", "アリーナ", "コンサート",
                   "日程", "会場", "レポ", "ファンミ"]),
    ("グッズ・発売", ["グッズ", "特典", "予約", "発売", "売り切れ", "再販", "通販", "アクスタ", "うちわ", "ペンライト", "トレカ", "円盤",
                 "アルバム", "シングル", "写真集", "カレンダー", "雑誌", "表紙", "コラボ", "ポップアップ"]),
    ("テレビ・出演", ["出演", "番組", "ドラマ", "映画", "CM", "放送", "キャスト", "ゲスト", "主演", "見逃し", "配信", "ラジオ", "YouTube", "舞台"]),
    ("髪型・見た目", ["髪型", "髪色", "金髪", "黒髪", "ヘア", "ビジュ", "痩せ", "太っ", "筋肉", "メイク", "タトゥー"]),
    ("発言・エピソード", ["発言", "エピソード", "仲良し", "不仲", "コンビ", "関係", "理由", "なぜ", "真相", "意味", "由来", "炎上", "謝罪", "脱退", "活動休止"]),
]
STOP = set("まとめ 一覧 最新 情報 紹介 調査 特定 画像 写真 動画 話題 理由 値段 どこ いつ なぜ 誰 何 公式 最新情報 徹底調査 判明 "
           "メンバー グループ ファン 記事 内容 詳細 解説 考察 予想 感想 本当 現在 今日 昨日 明日 今年 について".split())
TOKEN_RE = re.compile(r"[一-龥々ヶ]{2,}|[ァ-ヴー]{3,}|[A-Za-z][A-Za-z0-9'&.]{2,}")


# ---------------------------------------------------------------- 純粋関数(テスト対象)
def parse_date(text):
    """RSSの日付(RFC822)とAtomの日付(ISO8601)を、タイムゾーンつきのdatetimeにする。読めなければNone。"""
    text = (text or "").strip()
    if not text:
        return None
    try:
        d = email.utils.parsedate_to_datetime(text)
    except (TypeError, ValueError, IndexError):
        d = None
    if d is None:
        t = re.sub(r"(\.\d+)", "", text.replace("Z", "+00:00"))
        t = re.sub(r"([+-]\d\d)(\d\d)$", r"\1:\2", t)
        try:
            d = datetime.datetime.fromisoformat(t)
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=datetime.timezone.utc)
    return d


def _local(tag):
    return tag.rsplit("}", 1)[-1].lower() if isinstance(tag, str) else ""


def parse_feed(xml_bytes):
    """RSS2.0 / RSS1.0(RDF) / Atom を読んで [{title, url, date}] を新しい順で返す。フィードでなければ空。"""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []
    items = []
    for el in root.iter():
        if _local(el.tag) not in ("item", "entry"):
            continue
        title = url = date = None
        for c in el:
            name = _local(c.tag)
            if name == "title" and title is None:
                title = "".join(c.itertext()).strip()
            elif name == "link":
                href = c.get("href")
                if href and c.get("rel", "alternate") == "alternate":
                    url = url or href.strip()
                elif not href and (c.text or "").strip():
                    url = url or c.text.strip()
            elif name in ("pubdate", "date", "published", "updated") and date is None:
                date = parse_date(c.text)
        if title and url:
            items.append({"title": htmllib.unescape(re.sub(r"\s+", " ", title)), "url": url, "date": date})
    far = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    items.sort(key=lambda i: i["date"] or far, reverse=True)
    return items


def parse_sitemap(xml_bytes):
    """サイトマップを読む。("index", [子サイトマップのURL]) か ("urls", [{url, date}]) を返す。読めなければ ("", [])。"""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return "", []
    kind = "index" if _local(root.tag) == "sitemapindex" else "urls" if _local(root.tag) == "urlset" else ""
    rows = []
    for el in root:
        loc = date = None
        for c in el:
            if _local(c.tag) == "loc":
                loc = (c.text or "").strip()
            elif _local(c.tag) == "lastmod":
                date = parse_date(c.text)
        if loc:
            rows.append({"url": loc, "date": date})
    if kind == "index":
        # 記事のサイトマップを先に(固定ページ・カテゴリ・画像のものは後ろへ)、新しい順
        far = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
        rows.sort(key=lambda r: (not re.search(r"post", r["url"], re.I) or bool(re.search(r"page|categor|tag|author|image|video", r["url"], re.I)),
                                 -(r["date"] or far).timestamp()))
        return kind, [r["url"] for r in rows]
    return kind, rows


def page_title(page_html):
    """記事ページのタイトル。「記事名 | サイト名」のサイト名は落とす。"""
    m = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)', page_html, flags=re.I) \
        or re.search(r"<title[^>]*>(.*?)</title>", page_html, flags=re.I | re.S)
    if not m:
        return ""
    t = htmllib.unescape(re.sub(r"\s+", " ", m.group(1))).strip()
    parts = re.split(r"\s+[|｜–—-]\s+", t)
    return parts[0] if len(parts) > 1 and len(parts[0]) >= 8 else t


def feed_links(page_html, base):
    """ページの <link rel="alternate" type="application/rss+xml"> からフィードのURLを取り出す。"""
    out = []
    for tag in re.findall(r"<link\b[^>]*>", page_html, flags=re.I):
        if not re.search(r"application/(rss|atom|rdf)\+xml", tag, flags=re.I):
            continue
        m = re.search(r"""href\s*=\s*["']([^"']+)""", tag, flags=re.I)
        if m and "comments" not in m.group(1):
            out.append(urljoin(base, htmllib.unescape(m.group(1))))
    return out


def blog_key(url):
    """同じブログかどうかを見分ける名前。ふつうはドメイン、ブログサービスはドメイン+ユーザー名。"""
    u = urlparse(url if "://" in url else "https://" + url)
    host = (u.hostname or "").lower()
    host = host[4:] if host.startswith("www.") else host
    if host in SHARED_HOSTS:
        first = u.path.strip("/").split("/")[0]
        return host + "/" + first if first else host
    return host


def name_table(members):
    """[(探す文字, グループ, メンバーの正式な名前 or None)]。長い文字から先に当てる。"""
    rows = []
    for g, conf in members.items():
        for w in [conf["label"]] + conf.get("aliases", []):
            if len(w) >= 3:
                rows.append((w.lower(), g, None))
        for m in conf["members"]:
            rows.append((m["name"].lower(), g, m["name"]))
            if m.get("stage"):
                rows.append((m["stage"].lower(), g, m["name"]))
    rows.sort(key=lambda r: -len(r[0]))
    return rows


def tag_title(title, table):
    """タイトルに出てくるグループとメンバーを返す。英字の芸名(ISSAなど)は単語として出たときだけ当てる。"""
    low = title.lower()
    groups, names = [], []
    for word, g, name in table:
        if word.isascii():
            hit = re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", low)
        else:
            hit = word in low
        if hit:
            if g not in groups:
                groups.append(g)
            if name and name not in names:
                names.append(name)
    return groups, names


def topic_of(title):
    for label, words in TOPICS:
        if any(w in title for w in words):  # 英字は大文字小文字どおりに見る(「170cm」をCMと数えない)
            return label
    return "そのほか"


def tokens(title, skip=()):
    """かぶり判定に使う、タイトルの中の固有の言葉(メンバー名・ありふれた言葉は除く)。"""
    t = title
    for s in sorted(skip, key=len, reverse=True):
        t = re.sub(re.escape(s), " ", t, flags=re.I)
    out = []
    for w in TOKEN_RE.findall(t):
        if w not in STOP and w.lower() not in out:
            out.append(w.lower())
    return out


def find_overlaps(posts):
    """別々のブログが、同じメンバー(メンバー名が無ければ同じグループ)について同じ言葉で書いている組を探す。"""
    groups = []
    for p in posts:
        who = set(p["members"]) or set("g:" + g for g in p["groups"])
        if not who or not p["tokens"]:
            continue
        for g in groups:
            if g["who"] & who and len(set(g["tokens"]) & set(p["tokens"])) >= 1:
                g["posts"].append(p)
                g["who"] |= who
                g["tokens"] = [t for t in g["tokens"] if t in p["tokens"]] or g["tokens"]
                break
        else:
            groups.append({"who": set(who), "tokens": list(p["tokens"]), "posts": [p]})
    out = [g for g in groups if len(set(x["blog"] for x in g["posts"])) >= 2]
    out.sort(key=lambda g: -len(set(x["blog"] for x in g["posts"])))
    return out


def topic_counts(posts):
    c = {}
    for p in posts:
        c[p["topic"]] = c.get(p["topic"], 0) + 1
    return sorted(c.items(), key=lambda kv: -kv[1])


# ---------------------------------------------------------------- 通信
def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ja,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def find_feed(url):
    """ブログのトップのURLから、読めるフィードを探す。(フィードのURL, 記事) を返す。無ければ (None, [])。"""
    base = url if url.endswith("/") or urlparse(url).path.count(".") else url + "/"
    cands = []
    try:
        cands += feed_links(fetch(url).decode("utf-8", "replace"), url)
    except Exception:  # noqa: BLE001
        pass
    cands += [urljoin(base, g) for g in FEED_GUESSES]
    seen = set()
    for c in cands:
        if c in seen:
            continue
        seen.add(c)
        try:
            items = parse_feed(fetch(c, timeout=12))
        except Exception:  # noqa: BLE001
            continue
        if items:
            return c, items
    return None, []


def sitemap_items(url, depth=0):
    """サイトマップから記事のURLと更新日を集める(新しい順に最大60件)。タイトルは入っていない。"""
    kind, rows = parse_sitemap(fetch(url, timeout=15))
    if kind == "index" and depth < 2:
        out = []
        for child in rows[:2]:
            try:
                out += sitemap_items(child, depth + 1)
            except Exception:  # noqa: BLE001
                continue
        rows = out
    elif kind != "urls":
        return []
    rows = [r for r in rows if urlparse(r["url"]).path.strip("/")]  # トップページは外す
    far = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    rows.sort(key=lambda r: r["date"] or far, reverse=True)
    return rows[:60] if any(r["date"] for r in rows) else rows


def find_sitemap(url):
    """フィードが無いブログ用。読めるサイトマップを探す。(サイトマップのURL, 記事) か (None, [])。"""
    root = "{0.scheme}://{0.netloc}/".format(urlparse(url))
    cands = []
    try:
        cands += re.findall(r"(?im)^sitemap:\s*(\S+)", fetch(root + "robots.txt", timeout=10).decode("utf-8", "replace"))
    except Exception:  # noqa: BLE001
        pass
    cands += [root + p for p in ("wp-sitemap.xml", "sitemap.xml", "sitemap_index.xml", "post-sitemap.xml", "sitemap.xml.gz")]
    seen = set()
    for c in cands:
        if c in seen or c.endswith(".gz"):
            continue
        seen.add(c)
        try:
            items = sitemap_items(c)
        except Exception:  # noqa: BLE001
            continue
        if items:
            return c, items
    return None, []


def find_source(url):
    """(種類, URL, 記事)。種類は "feed" か "sitemap"、見つからなければ (None, None, [])。"""
    feed, items = find_feed(url)
    if feed:
        return "feed", feed, items
    sm, items = find_sitemap(url)
    if sm:
        return "sitemap", sm, items
    return None, None, []


def read_blog(b, titles, max_titles=12):
    """ブログ1つの記事一覧を読む。サイトマップのブログは、新しい記事だけページを開いてタイトルを取る。"""
    if b.get("kind") != "sitemap":
        return parse_feed(fetch(b["feed"]))
    items, opened = [], 0
    for r in sitemap_items(b["feed"])[:40]:
        if r["url"] not in titles and opened < max_titles:
            opened += 1
            try:
                titles[r["url"]] = page_title(fetch(r["url"], timeout=12).decode("utf-8", "replace"))
            except Exception:  # noqa: BLE001
                titles[r["url"]] = ""
            time.sleep(0.6)
        if titles.get(r["url"]):
            items.append({"title": titles[r["url"]], "url": r["url"], "date": r["date"]})
    return items


def load_rivals():
    if not RIVALS.exists():
        return {"_note": "見張るライバルブログの名簿。足すときは rival_watch.py --add URL --group グループ名。", "blogs": [], "ignore": []}
    return json.loads(RIVALS.read_text(encoding="utf-8"))


def save_rivals(data):
    RIVALS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_members():
    return json.loads((DATA / "members.json").read_text(encoding="utf-8"))["groups"]


def own_domains():
    return [s["domain"] for s in blogkit.SITES.values()]


def add_blog(url, groups, name="", source="手で追加"):
    data = load_rivals()
    key = blog_key(url)
    if any(d in key for d in own_domains()):
        print("自分たちのサイトなので足さないワン:", key)
        return 1
    if any(blog_key(b["url"]) == key for b in data["blogs"]):
        print("もう名簿にあるワン:", key)
        return 0
    kind, feed, items = find_source(url)
    if not feed:
        print("新着の一覧(フィードもサイトマップも)が見つからなかったワン。このブログは見張れない:", url)
        return 1
    data["blogs"].append({"name": name or key, "url": url, "feed": feed, "kind": kind, "groups": groups,
                          "added": datetime.date.today().isoformat(), "source": source})
    save_rivals(data)
    print("足したワン: {}({}) {}".format(name or key, feed, "新着の例:「{}」".format(items[0]["title"][:40]) if kind == "feed"
                                    else "サイトマップで見張る(記事{}本)".format(len(items))))
    return 0


# ---------------------------------------------------------------- 候補さがし(Yahoo!検索)
DEEP_SUFFIXES = ["グッズ", "チケット 倍率", "テレビ出演", "私服", "ロケ地 どこ", "香水", "愛用品", "髪型", "仲良し", "まとめ",
                 "読み方", "メンバーカラー", "人気順", "ファン 呼び方", "YouTube ロケ地"]


def discover_queries(members, sites, per_site=10, deep=False):
    out = []
    for key in sites:
        g = blogkit.SITES[key]["group"]
        if not g:
            continue
        conf = members[g]
        if deep:  # グループ名×いろいろな話題で、専門ブログを広く探す
            out += [(g, "{} {}".format(conf["label"], w)) for w in DEEP_SUFFIXES]
            continue
        qs = ["{} 私服 ブランド 特定".format(conf["label"]), "{} ロケ地 特定".format(conf["label"])]
        for i, m in enumerate(conf["members"]):
            shown = m.get("stage") and "{} {}".format(conf["label"], m["stage"]) or m["name"]
            qs.append("{} {}".format(shown, ["私服 どこの", "ロケ地 どこ", "愛用 香水", "指輪 ブランド"][i % 4]))
        out += [(g, q) for q in qs[:per_site]]
    return out


def count_candidates(results, ignore=()):
    """[(グループ, 検索語, [{url,title}])] から、何度も出てくる個人/中小サイトを数える。"""
    sys.path.insert(0, str(TOOLS / "suggest-finder"))
    from suggest_finder import classify_domain
    found = {}
    for g, q, top in results:
        for r in top:
            kind = classify_domain(r["url"], own_domains())
            key = blog_key(r["url"])
            if kind not in ("site", "blog") or key in ignore or key in SHARED_HOSTS:
                continue
            c = found.setdefault(key, {"key": key, "url": r["url"], "groups": [], "queries": [], "titles": []})
            if g not in c["groups"]:
                c["groups"].append(g)
            if q not in c["queries"]:
                c["queries"].append(q)
                c["titles"].append(r["title"])
    return sorted(found.values(), key=lambda c: -len(c["queries"]))


def discover(sites, save=False, min_hits=2, headless=True, deep=False):
    import random
    from playwright.sync_api import sync_playwright
    sys.path.insert(0, str(TOOLS / "suggest-finder"))
    from suggest_finder import YahooBlocked, yahoo_top
    data = load_rivals()
    known = set(blog_key(b["url"]) for b in data["blogs"])
    cache = HERE / "candidates.json"
    if save and cache.exists() and time.time() - cache.stat().st_mtime < 86400:
        cands = json.loads(cache.read_text(encoding="utf-8"))
        cands = [c for c in cands if c["key"] not in known and c["key"] not in data.get("ignore", []) and c.get("feed")]
        for c in cands:
            data["blogs"].append({"name": c["key"], "url": c["top_url"], "feed": c["feed"], "kind": c["kind"], "groups": c["groups"],
                                  "added": datetime.date.today().isoformat(),
                                  "source": "Yahoo!検索で{}回: {}".format(len(c["queries"]), " / ".join(c["queries"][:3]))})
        save_rivals(data)
        print("さっき探した候補から、名簿に{}件足したワン。外したいブログは tools/data/rivals.json から消してワン".format(len(cands)))
        return 0
    queries = discover_queries(load_members(), sites, deep=deep)
    print("Yahoo!で{}回検索して、よく出てくるブログを探すワン(約{}分)".format(len(queries), len(queries) * 6 // 60 + 1), flush=True)
    results = []
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome", headless=headless)
        except Exception:  # noqa: BLE001
            browser = p.chromium.launch(headless=headless)
        page = browser.new_context(locale="ja-JP", user_agent=UA, viewport={"width": 1280, "height": 1600}).new_page()
        try:
            for i, (g, q) in enumerate(queries, 1):
                print("  {}/{} 「{}」".format(i, len(queries), q), flush=True)
                try:
                    top, _ = yahoo_top(page, q)
                except YahooBlocked:
                    print("Yahoo!に止められたので、ここまでの分でまとめるワン")
                    break
                except Exception as e:  # noqa: BLE001
                    print("    失敗:", e)
                    continue
                results.append((g, q, top))
                time.sleep(random.uniform(3.5, 6.0))
        finally:
            browser.close()
    cands = [c for c in count_candidates(results, set(data.get("ignore", [])) | known) if len(c["queries"]) >= min_hits]
    if not cands:
        print("\n新しい候補は見つからなかったワン")
        return 0
    print("\n■ ライバル候補({}回以上出てきたブログ)".format(min_hits))
    for c in cands:
        top_url = "https://" + c["key"] + "/"
        kind, feed, items = find_source(top_url)
        c["feed"], c["kind"], c["top_url"] = feed, kind, top_url
        print("  {}回 {} [{}] {}".format(len(c["queries"]), c["key"], ",".join(c["groups"]),
                                       {"feed": "見張れる", "sitemap": "見張れる(サイトマップ)"}.get(kind, "見張れない")), flush=True)
        print("      例:「{}」".format(c["titles"][0][:50]))
    cache.write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n大手メディアや公式サイトが混ざっていたら、tools/data/rivals.json の ignore にドメインを書くと外れるワン。")
    if save:
        return discover(sites, save=True, deep=deep)
    print("名簿に足すなら、同じコマンドに --save を付けてワン(24時間以内なら検索し直さない)")
    return 0


# ---------------------------------------------------------------- 見張り本体
def collect(blogs, table, hours, now, state):
    """全部のブログのフィードを読み、直近hours時間の記事と、読めなかったブログを返す。"""
    cutoff = now - datetime.timedelta(hours=hours)
    posts, failed = [], []
    skip = [r[0] for r in table]
    titles = state.setdefault("_titles", {})
    for b in blogs:
        try:
            items = read_blog(b, titles)
        except Exception as e:  # noqa: BLE001
            failed.append((b["name"], str(e)[:80]))
            continue
        if not items:
            failed.append((b["name"], "記事が1件も読めなかった"))
            continue
        seen = set(state.get(b["feed"], []))
        first_run = b["feed"] not in state
        for it in items:
            is_new = it["url"] not in seen
            recent = it["date"] >= cutoff if it["date"] else (is_new and not first_run)
            if not recent:
                continue
            groups, names = tag_title(it["title"], table)
            if not groups and (len(b.get("groups", [])) != 1 or b.get("general")):
                continue  # いろいろ書くブログの、うちのグループと関係ない記事は数えない
            posts.append({"blog": b["name"], "blog_url": b["url"], "title": it["title"], "url": it["url"], "date": it["date"],
                          "groups": groups or list(b.get("groups", []))[:1] if len(b.get("groups", [])) == 1 or groups else [],
                          "members": names, "topic": topic_of(it["title"]), "tokens": tokens(it["title"], skip), "new": is_new,
                          "by_update": b.get("kind") == "sitemap"})
        state[b["feed"]] = list(dict.fromkeys([i["url"] for i in items] + list(seen)))[:300]
    if len(titles) > 4000:
        for k in list(titles)[:len(titles) - 4000]:
            del titles[k]
    posts.sort(key=lambda p: p["date"] or cutoff, reverse=True)
    return posts, failed


def check_own(overlaps, env):
    """かぶりネタについて、うちのサイトに同じ話題の記事があるかを調べる(公開記事の検索)。"""
    for g in overlaps:
        p = g["posts"][0]
        site = next((k for k, s in blogkit.SITES.items() if s["group"] in p["groups"]), None)
        words = (p["members"][:1] or []) + g["tokens"][:1]
        g["own"] = None
        if not site or not words:
            continue
        try:
            hits = blogkit.WP(site, env).get("/posts", auth=False, search=" ".join(words), per_page=3, _fields="id,link,title")
            g["own"] = [{"id": h["id"], "url": h["link"], "title": htmllib.unescape(h["title"]["rendered"])} for h in hits]
            g["own_site"] = blogkit.SITES[site]["label"]
        except Exception:  # noqa: BLE001
            pass


def append_history(posts):
    known = set()
    if HISTORY.exists():
        for line in HISTORY.read_text(encoding="utf-8").splitlines():
            try:
                known.add(json.loads(line)["url"])
            except (ValueError, KeyError):
                pass
    with HISTORY.open("a", encoding="utf-8") as f:
        for p in posts:
            if p["url"] not in known:
                f.write(json.dumps({"date": p["date"].isoformat() if p["date"] else None, "blog": p["blog"], "title": p["title"],
                                    "url": p["url"], "groups": p["groups"], "members": p["members"], "topic": p["topic"]},
                                   ensure_ascii=False) + "\n")


def history_counts(days=30, now=None):
    """たまった記録から、直近days日のネタの種類の数を返す。"""
    if not HISTORY.exists():
        return [], 0
    now = now or datetime.datetime.now(datetime.timezone.utc)
    rows = []
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        try:
            r = json.loads(line)
        except ValueError:
            continue
        d = parse_date(r.get("date") or "")
        if d and (now - d).days <= days:
            rows.append(r)
    return topic_counts(rows), len(rows)


def glabel(g, members):
    return members[g]["label"] if g in members else g


def when(d):
    return d.astimezone().strftime("%m/%d %H:%M") if d else "日時不明"


def stamp(p):
    """サイトマップで見張っているブログは、公開日ではなく更新日しか分からないので印を付ける。"""
    return when(p["date"]) + ("(更新)" if p.get("by_update") else "")


def to_text(posts, overlaps, failed, members, hours):
    lines = ["ライバルブログの新着(直近{}時間): {}本".format(hours, len(posts))]
    if overlaps:
        lines.append("\n■ 複数のブログが書いたネタ(需要が高い)")
        for g in overlaps:
            who = "・".join(sorted(w for w in g["who"] if not w.startswith("g:"))) or "・".join(glabel(w[2:], members) for w in g["who"])
            own = g.get("own")
            state = "" if own is None else " → うちにも記事あり(ID{})".format(own[0]["id"]) if own else " → うちはまだ書いていない"
            lines.append("  {}「{}」 {}ブログ{}".format(who, " ".join(g["tokens"][:3]), len(set(p["blog"] for p in g["posts"])), state))
            for p in g["posts"]:
                lines.append("      {} [{}] {}".format(stamp(p), p["blog"], p["title"][:60]))
    cur = None
    for p in sorted(posts, key=lambda p: (p["groups"][0] if p["groups"] else "zz")):
        g = p["groups"][0] if p["groups"] else None
        if g != cur:
            cur = g
            lines.append("\n■ " + (glabel(g, members) if g else "グループ不明・そのほか"))
        lines.append("  {} [{}] ({}) {}".format(stamp(p), p["blog"], p["topic"], p["title"][:70]))
    counts = topic_counts(posts)
    if counts:
        lines.append("\n■ ネタの種類: " + " / ".join("{}{}本".format(k, v) for k, v in counts))
    if failed:
        lines.append("\n■ 読めなかったブログ: " + "、".join("{}({})".format(n, e) for n, e in failed))
    return "\n".join(lines)


CSS = """body{font-family:system-ui,sans-serif;margin:0;padding:16px;background:#f6f7f9;color:#222;line-height:1.6;max-width:980px;margin:auto}
h1{font-size:1.3em}h2{font-size:1.1em;margin-top:26px;border-left:5px solid #c2410c;padding-left:8px}.card{background:#fff;border-radius:8px;
padding:10px 14px;margin:8px 0;box-shadow:0 1px 2px rgba(0,0,0,.08)}.tag{font-size:.8em;background:#eee;border-radius:4px;padding:1px 6px;
margin-right:6px;white-space:nowrap}.hot{background:#fde68a;color:#7c2d12}.new{background:#bbf7d0;color:#14532d}.upd{background:#bfdbfe;color:#1e3a8a}
.sub{color:#666;font-size:.88em}a{color:#1d4ed8;text-decoration:none}a:hover{text-decoration:underline}.row{margin:4px 0}
.bar{display:inline-block;height:10px;background:#c2410c;border-radius:3px;vertical-align:middle;margin-right:6px}
@media(prefers-color-scheme:dark){body{background:#16181c;color:#e6e6e6}.card{background:#22252b}.tag{background:#333}.sub{color:#aaa}
a{color:#8ab4f8}.hot{background:#92400e;color:#fef3c7}.new{background:#14532d;color:#dcfce7}.upd{background:#1e3a8a;color:#dbeafe}}"""


def to_html(posts, overlaps, failed, members, hours, now, n_blogs, hist):
    esc = htmllib.escape

    def row(p):
        return ('<div class="row"><span class="sub">{w}</span> <span class="tag">{b}</span><span class="tag">{t}</span>'
                '<a href="{u}" target="_blank" rel="noopener">{ti}</a></div>'
                ).format(w=stamp(p), b=esc(p["blog"]), t=p["topic"], u=esc(p["url"]), ti=esc(p["title"]))

    parts = []
    if overlaps:
        parts.append("<h2>複数のブログが書いたネタ(需要が高い)</h2>")
        for g in overlaps:
            who = "・".join(sorted(w for w in g["who"] if not w.startswith("g:"))) or "・".join(glabel(w[2:], members) for w in g["who"])
            own = g.get("own")
            state = ""
            if own:
                state = '<span class="tag upd">うちにも記事あり</span>' + " ".join(
                    '<a href="{}" target="_blank" rel="noopener">{}</a>'.format(esc(h["url"]), esc(h["title"][:30])) for h in own[:2])
            elif own is not None:
                state = '<span class="tag new">うちはまだ書いていない</span>'
            parts.append('<div class="card"><div><span class="tag hot">{n}ブログ</span><b>{who}</b> 「{tok}」 {st}</div>{rows}</div>'.format(
                n=len(set(p["blog"] for p in g["posts"])), who=esc(who), tok=esc(" ".join(g["tokens"][:3])), st=state,
                rows="".join(row(p) for p in g["posts"])))
    by = {}
    for p in posts:
        by.setdefault(p["groups"][0] if p["groups"] else "", []).append(p)
    for g in sorted(by, key=lambda k: (k == "", k)):
        parts.append("<h2>{}({}本)</h2><div class='card'>{}</div>".format(
            esc(glabel(g, members)) if g else "グループ不明・そのほか", len(by[g]), "".join(row(p) for p in by[g])))

    def bars(counts):
        top = max([v for _, v in counts] or [1])
        return "".join('<div class="row"><span class="bar" style="width:{}px"></span>{} {}本</div>'.format(
            int(200 * v / top) + 2, k, v) for k, v in counts)

    parts.append("<h2>ネタの種類(ライバルが何を書いているか)</h2><div class='card'><b>今回</b>{}</div>".format(bars(topic_counts(posts)) or " なし"))
    if hist[1]:
        parts.append("<div class='card'><b>直近30日の合計({}本)</b>{}</div>".format(hist[1], bars(hist[0])))
    if failed:
        parts.append("<h2>読めなかったブログ</h2><div class='card'>{}</div>".format(
            "".join('<div class="row">{} <span class="sub">{}</span></div>'.format(esc(n), esc(e)) for n, e in failed)))
    return ('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            "<title>ライバルブログ見張り {t}</title><style>{c}</style></head><body><h1>ライバルブログ見張り {t}</h1>"
            '<p class="sub">{n}ブログの直近{h}時間の新着 {k}本。タイトルを見るだけで、本文は読まない・写さない。</p>{b}</body></html>'
            ).format(t=now.astimezone().strftime("%Y-%m-%d %H:%M"), c=CSS, n=n_blogs, h=hours, k=len(posts),
                     b="\n".join(parts) or "<p>新着は無いワン</p>")


def main(argv=None):
    ap = argparse.ArgumentParser(description="ライバルブログ見張り")
    ap.add_argument("--hours", type=int, default=48)
    ap.add_argument("--site", default="")
    ap.add_argument("--no-own", action="store_true", help="うちに同じ話題の記事があるかを調べない")
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--add", default="", help="見張るブログのURLを名簿に足す")
    ap.add_argument("--group", default="", help="--add のときのグループ(カンマ区切り)")
    ap.add_argument("--name", default="")
    ap.add_argument("--discover", action="store_true", help="Yahoo!検索からライバル候補を探す")
    ap.add_argument("--save", action="store_true", help="--discover で見つけた候補を名簿に足す")
    ap.add_argument("--deep", action="store_true", help="--discover をグループ名×15の話題で広く探す")
    a = ap.parse_args(argv)
    sites = [s.strip() for s in a.site.split(",") if s.strip()]
    for s in sites:
        if s not in blogkit.SITES:
            print("サイト名がちがうワン:", s)
            return 1
    if a.add:
        return add_blog(a.add, [g.strip() for g in a.group.split(",") if g.strip()], a.name)
    if a.discover:
        return discover(sites or [k for k, s in blogkit.SITES.items() if s["group"]], save=a.save, deep=a.deep)

    members = load_members()
    data = load_rivals()
    want = set(blogkit.SITES[s]["group"] for s in sites)
    blogs = [b for b in data["blogs"] if not want or not b.get("groups") or want & set(b["groups"])]
    if not blogs:
        print("見張るブログがまだ名簿に無いワン。\n  候補を探す: python tools/rival_watch/rival_watch.py --discover --save\n"
              "  手で足す:   python tools/rival_watch/rival_watch.py --add URL --group snowman")
        return 1
    now = datetime.datetime.now(datetime.timezone.utc)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    print("{}ブログの新着を見に行くワン…".format(len(blogs)), flush=True)
    posts, failed = collect(blogs, name_table(members), a.hours, now, state)
    if want:
        posts = [p for p in posts if not p["groups"] or want & set(p["groups"])]
    overlaps = find_overlaps(posts)
    if overlaps and not a.no_own:
        check_own(overlaps, blogkit.load_env())
    STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    append_history(posts)
    print(to_text(posts, overlaps, failed, members, a.hours))
    OUT.mkdir(exist_ok=True)
    path = OUT / "rival_watch_{}.html".format(now.astimezone().strftime("%Y%m%d_%H%M"))
    path.write_text(to_html(posts, overlaps, failed, members, a.hours, now, len(blogs), history_counts(30, now)), encoding="utf-8")
    print("\nできたワン:", path)
    if not a.no_open:
        webbrowser.open(path.as_uri())
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
