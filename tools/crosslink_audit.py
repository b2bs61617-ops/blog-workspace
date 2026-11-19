# -*- coding: utf-8 -*-
"""公開記事どうしの内部リンク(相互リンク)が足りない記事を探して、関連記事を足す(2026-11-19 オシリ依頼「回遊増やしたい」)。

    python tools/crosslink_audit.py audit  --site travis            # 読むだけ。足りない記事と追加案を articles/crosslink_<site>.json に出す
    python tools/crosslink_audit.py apply  --site travis [--limit N] # 追加案どおりに本文の一番下へ関連記事を足す(元の本文は backups/ に保存)

ルール(docs/rules.md「関連記事boxの配置は記事の一番下」「リンク文字は記事の中身」):
- 公開記事だけ。下書きにはリンクしない。KO1KEYZは日本語版どうしだけ(/ko/ /en/ は触らない)
- 既にリンクしている記事は足さない。1記事に足すのは最大3本
- 関連の強さ = 同じメンバーがタイトルにいる・同じ【】(番組・企画)・タイトルの言葉の重なり
- リンク先は「まだあまりリンクされていない記事」を優先(回遊の行き止まりを減らす)
- 既に記事末に関連記事の枠があればその中の<ul>に足す。無ければ「あわせて読みたい」の枠を一番下に作る
"""
import argparse
import datetime
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE_GROUP = {"sixtones": "sixtones", "ko1keyz": "ko1keyz", "snowman": "snowman", "travis": "travis", "ktl": "ktl"}
COLORS = {"sixtones": ("#1a3c4c", "#f3f6f8"), "ko1keyz": ("#1a3c4c", "#f3f6f8"), "snowman": ("#1a3c4c", "#f3f6f8"),
          "travis": ("#7e57c2", "#f5f2fb"), "ktl": ("#1a3c4c", "#f3f6f8")}
MAX_ADD = 3
MIN_OUT = 3          # これ未満の内部リンクしかない記事に足す
MARK = "crosslink-1119"
STOP = set("どこ ブランド 値段 いつ 誰 何 なぜ 理由 まとめ 記事 判明 調査 特定 徹底 私服 紹介 正体 意味 由来 場所 ロケ地 は の が を に と で も や".split())


def members(group):
    d = json.loads((blogkit.ROOT / "tools" / "data" / "members.json").read_text(encoding="utf-8"))
    g = d["groups"].get(group, {})
    out = []
    for m in g.get("members", []):
        names = {m["name"]}
        if re.search(r"[ぁ-んァ-ン一-龥]", m["name"]) and len(m["name"]) >= 3:
            names.add(m["name"][:2])  # 名字(宮近・七五三掛は3字だが2字でも当たる)
        for a in m.get("aliases", []):
            names.add(a)
        out.append((m["name"], [n for n in names if len(n) >= 2]))
    return out


def title_of(p):
    t = p["title"].get("raw") or p["title"].get("rendered", "")
    return html.unescape(re.sub(r"<[^>]+>", "", t)).strip()


def tags(t):
    return set(re.findall(r"【([^】]+)】", t))


def words(t):
    t = re.sub(r"【[^】]+】", " ", t)
    ws = set(re.findall(r"[A-Za-z][A-Za-z0-9&'.\-]{2,}|[ァ-ヴー]{3,}|[一-龥]{2,}", t))
    return {w for w in ws if w not in STOP}


def score(v, w):
    s = 4 * len(v["members"] & w["members"])
    if v["members"] and w["members"] and v["members"] == w["members"]:
        s += 2
    s += 5 * len(v["tags"] & w["tags"])
    s += 2 * len(v["words"] & w["words"])
    return s


def is_jp(p, site_key):
    if site_key != "ko1keyz":
        return True
    return not re.search(r"/(ko|en)/", p["link"]) and not re.search(r"-(kr|en)$", p["slug"])


def strip_added(content):
    """このツールが足した部分を外す(raw / rendered どちらでも)。"""
    content = re.sub(r'<li class="crosslink-1119">.*?</li>', "", content, flags=re.S)
    content = re.sub(r'\s*<!-- wp:html -->\s*<div class="crosslink-1119".*?<!-- /wp:html -->\n*', "", content, flags=re.S)
    content = re.sub(r'<div class="crosslink-1119".*?</ul></div>', "", content, flags=re.S)
    return content


def internal_ids(content, domain, by_slug, by_link):
    """hrefだけでなく、埋め込み(ブログカード)のURL・postIdも拾う。"""
    ids = set(int(x) for x in re.findall(r'"postId"\s*:\s*(\d+)', content))
    urls = re.findall(r'https?://(?:www\.)?' + re.escape(domain) + r"/[^\s\"'<>]*", content)
    for u in urls:
        m = re.search(r"[?&]p=(\d+)", u)
        if m:
            ids.add(int(m.group(1)))
            continue
        h = re.sub(r"/embed/?.*$", "", u.split("#")[0].split("?")[0]).rstrip("/")
        if h in by_link:
            ids.add(by_link[h])
            continue
        slug = h.rsplit("/", 1)[-1]
        if slug in by_slug:
            ids.add(by_slug[slug])
    return ids


def all_posts(wp):
    """公開記事を本文raw込みで全部読む(認証あり・context=edit)。"""
    import urllib.parse
    out, page = [], 1
    while True:
        q = urllib.parse.urlencode({"per_page": 100, "page": page, "status": "publish", "context": "edit",
                                    "_fields": "id,date,link,slug,title,content"})
        body, headers = wp._req("/posts?" + q, raw=True)
        out += body
        if page >= int(headers.get("X-WP-TotalPages", 1)):
            return out
        page += 1


def audit(site_key):
    wp = blogkit.WP(site_key)
    dom = blogkit.site(site_key)["domain"]
    posts = [p for p in all_posts(wp) if is_jp(p, site_key)]
    by_slug = {p["slug"]: p["id"] for p in posts}
    by_link = {p["link"].rstrip("/"): p["id"] for p in posts}
    mem = members(SITE_GROUP[site_key])
    info = {}
    for p in posts:
        t = title_of(p)
        if t.startswith("【未】"):
            continue
        ms = {full for full, ns in mem if any(n in t for n in ns)}
        info[p["id"]] = dict(id=p["id"], title=t, link=p["link"], date=p["date"], members=ms, tags=tags(t),
                             words=words(t), out=internal_ids(strip_added(p["content"]["raw"] + p["content"]["rendered"]), dom, by_slug, by_link) - {p["id"]})
    inbound = {i: 0 for i in info}
    for v in info.values():
        for o in v["out"]:
            if o in inbound:
                inbound[o] += 1
    plan = []
    for v in sorted(info.values(), key=lambda x: x["date"]):
        if len(v["out"] & set(info)) >= MIN_OUT:
            continue
        cands = []
        for w in info.values():
            if w["id"] == v["id"] or w["id"] in v["out"]:
                continue
            s = score(v, w)
            if s < 4:
                continue
            s += max(0, 3 - inbound[w["id"]])  # まだリンクの少ない記事を少し優先
            cands.append((s, w["date"], w["id"]))
        cands.sort(reverse=True)
        need = min(MAX_ADD, max(1, MIN_OUT - len(v["out"] & set(info))))
        pick = [c[2] for c in cands[:need]]
        if pick:
            for i in pick:
                inbound[i] += 1
            plan.append(dict(id=v["id"], title=v["title"], add=[dict(id=i, title=info[i]["title"], link=info[i]["link"])
                                                                for i in pick]))
    # 2段目: どこからもリンクされていない記事を、いちばん近い記事の関連枠に入れてもらう
    plan_by = {x["id"]: x for x in plan}
    for oid in [i for i, n in inbound.items() if n == 0]:
        o = info[oid]
        best = None
        for w in info.values():
            if w["id"] == oid or oid in w["out"]:
                continue
            cur = plan_by.get(w["id"])
            if cur and (len(cur["add"]) >= MAX_ADD or any(a["id"] == oid for a in cur["add"])):
                continue
            sc = score(o, w)
            if sc >= 4 and (best is None or sc > best[0]):
                best = (sc, w["id"])
        if best:
            wid = best[1]
            if wid not in plan_by:
                plan_by[wid] = dict(id=wid, title=info[wid]["title"], add=[])
                plan.append(plan_by[wid])
            plan_by[wid]["add"].append(dict(id=oid, title=o["title"], link=o["link"]))
            inbound[oid] += 1
    orphans = [info[i]["title"] for i, n in inbound.items() if n == 0]
    res = dict(site=site_key, posts=len(info), to_fix=len(plan), add_links=sum(len(x["add"]) for x in plan),
               orphans_after=len(orphans), orphans=orphans, plan=plan)
    out = blogkit.ARTICLES / "crosslink_{}.json".format(site_key)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print("{}: 公開{}本 / 足す記事{}本 / 足すリンク{}本 / それでもリンクされない記事{}本 → {}".format(
        site_key, res["posts"], res["to_fix"], res["add_links"], res["orphans_after"], out))
    return res


def box(site_key, items):
    a, bg = COLORS[site_key]
    lis = "".join('<li><a href="{}">{}</a></li>'.format(x["link"], html.escape(x["title"], quote=False)) for x in items)
    return ('<!-- wp:html -->\n<div class="{m}" style="border:1px solid #ddd;border-left:4px solid {a};border-radius:4px;'
            'padding:12px 18px;margin:24px 0 16px 0;background:{bg};">'
            '<p style="font-weight:bold;margin:0 0 6px 0;">あわせて読みたい</p>'
            '<ul style="margin:0;padding-left:1.2em;">{lis}</ul></div>\n<!-- /wp:html -->\n\n').format(m=MARK, a=a, bg=bg, lis=lis)


def merge(raw, site_key, items):
    """記事の最後の見出しより後ろに関連記事の枠(<ul>)があれば、その中に足す。無ければ枠を一番下に作る。"""
    tail_start = max(raw.rfind("<h2"), 0)
    tail = raw[tail_start:]
    hit = max(tail.rfind("関連記事"), tail.rfind("あわせて読みたい"), tail.rfind("合わせて読みたい"))
    if hit >= 0:
        ul_end = tail.find("</ul>", hit)
        if 0 <= ul_end - hit < 2500 and "<h" not in tail[hit:ul_end]:
            lis = "".join('<li class="{}"><a href="{}">{}</a></li>'.format(MARK, x["link"], html.escape(x["title"], quote=False))
                          for x in items)
            pos = tail_start + ul_end
            return raw[:pos] + lis + raw[pos:]
    return raw.rstrip() + "\n\n" + box(site_key, items)


def apply(site_key, limit=None):
    res = json.loads((blogkit.ARTICLES / "crosslink_{}.json".format(site_key)).read_text(encoding="utf-8"))
    wp = blogkit.WP(site_key)
    bk = blogkit.ROOT / "backups" / "crosslink_{}_{}".format(datetime.date.today().strftime("%m%d"), site_key)
    bk.mkdir(parents=True, exist_ok=True)
    done = 0
    for item in res["plan"][:limit] if limit else res["plan"]:
        p = wp.get_post(item["id"])
        if p["status"] != "publish":
            continue
        raw = p["content"]["raw"]
        if MARK in raw:
            print("済み", item["id"])
            continue
        (bk / "{}.html".format(item["id"])).write_text(raw, encoding="utf-8")
        new = merge(raw, site_key, item["add"])
        wp.post("/posts/{}".format(item["id"]), {"content": new})
        chk = wp.get_post(item["id"])["content"]["raw"]
        ok = MARK in chk and all(x["link"] in chk for x in item["add"])
        print("OK" if ok else "!!確認", item["id"], item["title"][:30], "+{}".format(len(item["add"])))
        done += ok
    print("{}: {}本に足した(元の本文は {})".format(site_key, done, bk))


def redo(site_key):
    """1回目(v1)で足した分を外して、新しい案で足し直す。変わらない記事は触らない。"""
    import shutil
    cur = blogkit.ARTICLES / "crosslink_{}.json".format(site_key)
    v1 = blogkit.ARTICLES / "crosslink_{}_v1.json".format(site_key)
    if not v1.exists():
        shutil.copy(cur, v1)
    old_ids = [x["id"] for x in json.loads(v1.read_text(encoding="utf-8"))["plan"]]
    res = audit(site_key)
    plan = {x["id"]: x["add"] for x in res["plan"]}
    wp = blogkit.WP(site_key)
    changed = same = 0
    for pid in sorted(set(old_ids) | set(plan)):
        p = wp.get_post(pid)
        if p["status"] != "publish":
            continue
        raw = p["content"]["raw"]
        base = strip_added(raw)
        new = merge(base, site_key, plan[pid]) if plan.get(pid) else base
        if new.rstrip() == raw.rstrip():
            same += 1
            continue
        bk = blogkit.ROOT / "backups" / "crosslink_1119_{}".format(site_key)
        bk.mkdir(parents=True, exist_ok=True)
        if not (bk / "{}.html".format(pid)).exists():
            (bk / "{}.html".format(pid)).write_text(base, encoding="utf-8")
        wp.post("/posts/{}".format(pid), {"content": new})
        chk = wp.get_post(pid)["content"]["raw"]
        if not all(x["link"] in chk for x in plan.get(pid, [])):
            print("!!確認", pid)
        changed += 1
    print("{}: 直した{}本 / そのまま{}本".format(site_key, changed, same))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["audit", "apply", "redo"])
    ap.add_argument("--site", required=True, choices=list(SITE_GROUP))
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    {"audit": lambda: audit(a.site), "apply": lambda: apply(a.site, a.limit), "redo": lambda: redo(a.site)}[a.cmd]()
