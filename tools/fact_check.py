# -*- coding: utf-8 -*-
"""投稿前の事実チェック係(2026-11-14〜)。下書きを機械で調べ、公開前に直すところを出す。

調べること:
  日付と曜日 / メンバー名・グループ名の字 / 年齢・誕生日・メンバーカラー(名簿 tools/data/members.json)/
  タイトル(35字・全角？！・数字が本文にあるか)/ 字数・見出し・区切り線・ブロック形式 /
  さん付けの抜け(honorific)/ 読みにくい文(easy_read)/ 気をつける言葉(学校の断定など)/
  リンク切れ(--no-net で省く)/ 外部AIに食いちがいを聞く(--ai、無くても動く)

usage:
    python tools/fact_check.py 記事.html --site snowman --title "タイトル" [--names "内村光良,LISA"]
    python tools/fact_check.py --site trend --post-id 13187        # WordPressの下書き/公開記事を直接調べる
    --no-net リンク切れを調べない / --ai 外部AIにも聞く / --json 機械向けに出す
NGが1件でもあれば終了コード1。Python 3.9対応。
"""
import datetime
import html as htmllib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
MEMBERS_JSON = TOOLS / "data" / "members.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

ZEN = str.maketrans("０１２３４５６７８９／（）", "0123456789/()")  # 全角→半角
# 旧字・異体字 → よくある打ちまちがい
OLD_NEW = {"髙": "高", "﨑": "崎", "澤": "沢", "舘": "館", "濱": "浜", "邊": "辺", "邉": "辺", "齋": "斎", "齊": "斉",
           "國": "国", "廣": "広", "櫻": "桜", "眞": "真", "德": "徳", "惠": "恵", "塚": "塚"}
COLORS = {"黄": ("黄色", "黄", "イエロー"), "紫": ("紫", "パープル"), "白": ("白", "ホワイト"), "青": ("青", "ブルー"),
          "オレンジ": ("オレンジ", "橙"), "緑": ("緑", "グリーン"), "黒": ("黒", "ブラック"), "赤": ("赤", "レッド"),
          "ピンク": ("ピンク", "桃色")}
WEEK = "月火水木金土日"
SOFT = ("可能性", "推測", "思われ", "ようです", "とされ", "といわれ", "と言われ", "公表", "本人", "明か", "語っ", "話し",
        "かもしれ", "でしょう", "うわさ", "噂", "説", "？", "?")
SENSITIVE = [
    (re.compile(r"(小学校|中学校|高校|高等学校|大学)(に|へ)?(通って|在籍して|進学して|入学して)(います|いる|いました|いた)"),
     "学校の断定(本人が公表していなければ「〜と推測されます」などにする)"),
    (re.compile(r"出身小学校は|[^\s、。]{2,12}小学校(出身|の出身|を卒業)"), "小学校名(未成年・一般人なら書かない)"),
    (re.compile(r"自宅(は|の場所|の住所)|住所は|最寄り駅は"), "住まいの特定につながる記述"),
    (re.compile(r"逮捕|前科|犯罪歴|薬物|不倫|中絶|整形(して|した|疑惑)|帰化|在日"), "名誉にかかわる言葉(出典を確かめる。うわさだけなら書かない)"),
]
SKIP_LINK_HOSTS = ("amazon.", "amzn.", "rakuten.", "r10.to", "instagram.com", "tiktok.com", "google.com/maps",
                   "maps.google", "threads.net", "threads.com", "facebook.com", "line.me")


# ---------------------------------------------------------------- 名簿
def load_groups(path=None):
    return json.loads(Path(path or MEMBERS_JSON).read_text(encoding="utf-8"))["groups"]


def all_members(groups):
    return [dict(m, group=g) for g, conf in groups.items() for m in conf["members"]]


def variants(name):
    """旧字を新字に打ちまちがえた形を作る(髙地優吾 → 高地優吾)。"""
    out = set()
    hits = [i for i, ch in enumerate(name) if ch in OLD_NEW and OLD_NEW[ch] != ch]
    for i in hits:
        out.add(name[:i] + OLD_NEW[name[i]] + name[i + 1:])
    if len(hits) > 1:
        out.add("".join(OLD_NEW.get(ch, ch) for ch in name))
    out.discard(name)
    return sorted(out)


def wrong_map(groups):
    """まちがった書き方 → 正しい書き方。正しい名前の一部になっているものは入れない。"""
    correct = [m["name"] for m in all_members(groups)] + [c["label"] for c in groups.values()]
    out = {}
    for g, conf in groups.items():
        for w in conf.get("wrong", []):
            out[w] = conf["label"]
        for m in conf["members"]:
            for w in list(m.get("wrong", [])) + variants(m["name"]):
                out[w] = m["name"]
            for w in list(m.get("wrong", [])):
                for v in variants(w):
                    out.setdefault(v, m["name"])
    return {w: r for w, r in out.items() if not any(w in c for c in correct)}


# ---------------------------------------------------------------- 文字の取り出し
def plain(html):
    s = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    s = re.sub(r"<(script|style|iframe)\b.*?</\1>", "", s, flags=re.S)
    s = re.sub(r"<br\s*/?>|</(p|li|h[1-6]|td|th|tr|div|figcaption|blockquote)>", "\n", s)
    s = htmllib.unescape(re.sub(r"<[^>]+>", "", s))
    s = re.sub(r"https?://\S+", "", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[。！？!?])|\n", text) if s and s.strip()]


def char_count(html):
    return len(re.sub(r"\s", "", plain(html)))


# ---------------------------------------------------------------- 日付と曜日
_PAREN = r"\s*\(\s*([月火水木金土日])(?:曜日?)?(?:[・、,]?祝日?)?\s*\)"
_DATE_RES = [re.compile(r"(?:(\d{4})年\s*)?(\d{1,2})月\s*(\d{1,2})日" + _PAREN),
             re.compile(r"(?<![\d/.])(?:(\d{4})/)?(\d{1,2})/(\d{1,2})" + _PAREN)]


def check_dates(text, today=None):
    today = today or datetime.date.today()
    t = text.translate(ZEN)
    ng, warn, seen = [], [], set()
    for rx in _DATE_RES:
        for m in rx.finditer(t):
            y, mo, d, w = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
            label = m.group(0).strip()
            if (m.start(), label) in seen:
                continue
            seen.add((m.start(), label))
            explicit = bool(y)
            if not y:
                back = re.findall(r"((?:19|20)\d{2})年", t[max(0, m.start() - 150):m.start()])
                y = back[-1] if back else today.year
            y = int(y)
            try:
                real = WEEK[datetime.date(y, mo, d).weekday()]
            except ValueError:
                ng.append("[日付] 「{}」は存在しない日付".format(label))
                continue
            if real == w:
                continue
            near = [yy for yy in (y - 1, y + 1) if _weekday(yy, mo, d) == w]
            if near and not explicit:
                warn.append("[日付] 「{}」は{}年だと({})。{}年なら合う→年を確かめる".format(label, y, real, near[0]))
            else:
                ng.append("[日付] 「{}」の曜日がちがう。{}年{}月{}日は({})".format(label, y, mo, d, real))
    return ng, warn


def _weekday(y, mo, d):
    try:
        return WEEK[datetime.date(y, mo, d).weekday()]
    except ValueError:
        return None


# ---------------------------------------------------------------- 名前・年齢・誕生日・カラー
def check_names(text, groups):
    ng = []
    for w, right in sorted(wrong_map(groups).items(), key=lambda x: -len(x[0])):
        n = len(re.findall(re.escape(w), text))
        if n:
            ng.append("[名前] 「{}」→ 正しくは「{}」({}か所)".format(w, right, n))
    return ng


def age_on(birthday, today):
    b = datetime.date.fromisoformat(birthday)
    return today.year - b.year - ((today.month, today.day) < (b.month, b.day))


def check_profiles(text, groups, today=None):
    """年齢・誕生日・メンバーカラーが名簿と合っているか。名簿に値がある人だけ調べる。"""
    today = today or datetime.date.today()
    t = text.translate(ZEN)
    members = all_members(groups)
    ng, warn = [], []
    for m in members:
        if not m.get("birthday"):
            continue
        age, name = age_on(m["birthday"], today), re.escape(m["name"])
        for x in re.finditer(name + r"(?:さん|くん)?(?:\((\d{1,2})歳?\)|は(?:現在|いま|今)?(\d{1,2})歳)", t):
            said = int(x.group(1) or x.group(2))
            if said not in (age, age + 1):
                ng.append("[年齢] {}は{}歳のはず(本文は{}歳。{}生まれ)".format(m["name"], age, said, m["birthday"]))
    for s in sentences(t):
        hit = [m for m in members if m["name"] in s]
        if len(hit) != 1:
            continue
        m = hit[0]
        if m.get("birthday"):
            b = datetime.date.fromisoformat(m["birthday"])
            for x in re.finditer(r"(?:(\d{4})年)?(\d{1,2})月(\d{1,2})日(?:生まれ|が誕生日|に誕生)|誕生日(?:は|の)(\d{1,2})月(\d{1,2})日", s):
                y = x.group(1)
                mo, d = int(x.group(2) or x.group(4)), int(x.group(3) or x.group(5))
                if (mo, d) != (b.month, b.day) or (y and int(y) != b.year):
                    ng.append("[誕生日] {}の誕生日は{}年{}月{}日(本文「{}」)".format(m["name"], b.year, b.month, b.day, x.group(0)))
        if m.get("color"):
            x = re.search(r"(?:メンバーカラー|メンカラ)(?:は|が|の|である|=|:|：|、)?\s*[「『]?(" +
                          "|".join(sorted((w for ws in COLORS.values() for w in ws), key=len, reverse=True)) + ")", s)
            if x and x.group(1) not in COLORS.get(m["color"], (m["color"],)):
                warn.append("[カラー] {}のメンバーカラーは{}(本文「{}」)".format(m["name"], m["color"], x.group(0)))
    return ng, warn


# ---------------------------------------------------------------- タイトル・形
def check_title(title, text):
    ng, warn = [], []
    if not title:
        return ng, warn
    title = title.replace("【未】", "").strip()
    if len(title) > 35:
        ng.append("[タイトル] {}字(35字まで)".format(len(title)))
    if re.search(r"[?!]", title):
        ng.append("[タイトル] 半角の ? ! がある(全角の？！にする)")
    if not title.endswith(("？", "！")):
        warn.append("[タイトル] 最後が全角の？か！で終わっていない")
    body = text.translate(ZEN)
    for num in re.findall(r"\d+(?:[.,]\d+)*", title.translate(ZEN)):
        if not re.search(r"(?<!\d)" + re.escape(num) + r"(?!\d)", body):
            warn.append("[タイトル] 数字「{}」が本文に出てこない".format(num))
    return ng, warn


def check_shape(html, min_chars=2500):
    ng, warn = [], []
    n = char_count(html)
    if n < min_chars:
        ng.append("[字数] {}字({}字以上にする)".format(n, min_chars))
    if "<!-- wp:" not in html:
        ng.append("[形] ブロック形式(<!-- wp:〜 -->)になっていない(広告が入らない)")
    if re.search(r"<hr\b|wp:separator", html):
        ng.append("[形] 区切り線(<hr>)がある(全部取る)")
    if not re.search(r"<h2\b", html):
        ng.append("[形] H2見出しが無い")
    if "【未】" in plain(html):
        warn.append("[形] 本文に【未】が入っている")
    no_br = 0
    for p in re.findall(r"<p\b[^>]*>(.*?)</p>", html, re.S):
        no_br += len(re.findall("。(?!\\s*(?:<br|$|」|』|\\)|）|</))", p.strip()))
    if no_br >= 3:
        warn.append("[形] 「。」のあとに<br>が無いところが{}か所".format(no_br))
    for fig in re.findall(r"<figure\b(?:(?!</figure>).)*<img\b(?:(?!</figure>).)*</figure>", html, re.S):
        if "figcaption" not in fig:
            warn.append("[形] 出典(figcaption)の無い画像: " + (re.search(r'src="([^"]+)"', fig) or [None, "?"])[1][-50:])
    return ng, warn


def check_sensitive(text):
    warn = []
    for s in sentences(text):
        for rx, msg in SENSITIVE:
            if rx.search(s) and not any(w in s for w in SOFT):
                warn.append("[気をつける言葉] {}: {}".format(msg, s[:50]))
    return warn


# ---------------------------------------------------------------- リンク切れ
def extract_urls(html):
    urls = re.findall(r'(?:href|src)="(https?://[^"]+)"', html)
    urls += re.findall(r'wp-block-embed__wrapper">\s*(https?://\S+?)\s*</div>', html)
    out = []
    for u in urls:
        u = htmllib.unescape(u)
        if u not in out:
            out.append(u)
    return out


def classify_url(url):
    low = url.lower()
    if re.search(r"(twitter|x)\.com/[^/]+/status/\d+", low):
        return "x"
    if "youtube.com/" in low or "youtu.be/" in low:
        return "youtube"
    if any(h in low for h in SKIP_LINK_HOSTS):
        return "skip"
    return "web"


def _status(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept-Language": "ja"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:  # noqa: BLE001
        return 0


def check_url(url):
    """(状態, 説明)。状態 = ok / dead / unknown / skip"""
    kind = classify_url(url)
    if kind == "skip":
        return "skip", ""
    if kind == "x":
        u = re.sub(r"https?://(www\.)?(twitter|x)\.com", "https://twitter.com", url.split("?")[0])
        st = _status("https://publish.twitter.com/oembed?omit_script=1&url=" + urllib.parse.quote(u, safe=""))
        return ("ok", "") if st == 200 else ("dead", "Xの投稿が消えた・鍵・凍結({})".format(st)) if st in (403, 404) else ("unknown", str(st))
    if kind == "youtube":
        vid = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})", url)
        if not vid:
            return "skip", ""
        st = _status("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote("https://www.youtube.com/watch?v=" + vid.group(1), safe=""))
        if st == 200:
            return "ok", ""
        return ("dead", "YouTubeが消えた・非公開・埋め込み不可({})".format(st)) if st in (400, 401, 403, 404) else ("unknown", str(st))
    st = _status(url)
    if st in (404, 410):
        return "dead", "ページが無い({})".format(st)
    return ("ok", "") if 200 <= st < 400 else ("unknown", str(st))


def check_links(html, workers=8):
    urls = extract_urls(html)
    ng, warn = [], []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for url, (state, msg) in zip(urls, ex.map(check_url, urls)):
            if state == "dead":
                ng.append("[リンク切れ] {} {}".format(msg, url))
            elif state == "unknown" and classify_url(url) != "web":
                warn.append("[リンク] 確かめられなかった({}) {}".format(msg, url))
    return ng, warn


# ---------------------------------------------------------------- 外部AI(おまけ)
AI_PROMPT = ("次のブログ記事の本文の中で、たがいに食いちがっている記述(日付・数字・名前・場所・順番)だけを探してください。"
             "文章の感想や言い回しの指摘は不要です。食いちがいが無ければ「なし」とだけ答えてください。"
             "あれば1件1行で「・Aでは〜、Bでは〜」の形で、最大5件。\n\n本文:\n")


def check_ai(text):
    try:
        import ai_hub
        _used, ans = ai_hub.call(AI_PROMPT + text[:12000])
    except BaseException as e:  # noqa: BLE001  (SystemExitもここで止める)
        return ["[AI] 聞けなかった({})".format(str(e)[:60])]
    lines = [x.strip() for x in (ans or "").splitlines() if x.strip()]
    if not lines or lines[0].startswith("なし"):
        return []
    return ["[AIの指摘・要確認] " + x for x in lines[:5]]


# ---------------------------------------------------------------- まとめて実行
def run(html, site_key=None, title=None, names=(), net=True, ai=False, today=None, groups=None):
    groups = groups if groups is not None else load_groups()
    text = plain(html)
    full = (title or "") + "\n" + text
    ng, warn = [], []

    def add(result):
        ng.extend(result[0])
        warn.extend(result[1])

    add(check_title(title, text))
    add(check_shape(html))
    add(check_dates(full, today))
    ng.extend(check_names(full, groups))
    add(check_profiles(full, groups, today))
    warn.extend(check_sensitive(text))
    try:
        import easy_read
        e_ng, e_warn = easy_read.check(html)
        ng.extend("[読みやすさ] " + x for x in e_ng)
        warn.extend("[読みやすさ] " + x for x in e_warn)
    except ImportError:
        pass
    try:
        import honorific
        group = None
        if site_key:
            import blogkit
            group = blogkit.site(site_key)["group"]
        if group is None:
            honorific.GROUPS.setdefault("none", {})
            group = "none"
        if group != "none" or names:
            ng.extend("[さん付け] 抜け: …{}…".format(x) for x in honorific.missing(html, group, tuple(names)))
    except ImportError:
        pass
    if net:
        add(check_links(html))
    if ai:
        warn.extend(check_ai(text))
    return {"ng": ng, "warn": warn, "chars": char_count(html), "title": title}


def format_report(rep):
    lines = ["== 事実チェック: NG {}件 / 注意 {}件 / {}字".format(len(rep["ng"]), len(rep["warn"]), rep["chars"])]
    lines += ["  NG   " + x for x in rep["ng"]] + ["  注意 " + x for x in rep["warn"]]
    if not rep["ng"] and not rep["warn"]:
        lines.append("  直すところは見つからなかった")
    return "\n".join(lines)


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="投稿前の事実チェック係")
    ap.add_argument("file", nargs="?")
    ap.add_argument("--site")
    ap.add_argument("--post-id", type=int)
    ap.add_argument("--title")
    ap.add_argument("--names", default="")
    ap.add_argument("--no-net", action="store_true")
    ap.add_argument("--ai", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    title = a.title
    if a.post_id:
        import blogkit
        if not a.site:
            ap.error("--post-id には --site が要る")
        po = blogkit.WP(a.site).get_post(a.post_id)
        html, title = po["content"]["raw"], title or po["title"]["raw"]
    elif a.file:
        html = Path(a.file).read_text(encoding="utf-8")
    else:
        ap.error("記事ファイルか --post-id を指定する")
    names = [n.strip() for n in a.names.split(",") if n.strip()]
    rep = run(html, site_key=a.site, title=title, names=names, net=not a.no_net, ai=a.ai)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else format_report(rep))
    return 1 if rep["ng"] else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
