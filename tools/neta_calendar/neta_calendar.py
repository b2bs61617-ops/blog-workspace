# -*- coding: utf-8 -*-
"""ネタ先読みカレンダー(2026-11-14〜)。検索が伸びる前に仕込む記事を、2〜4週間ぶん並べる。

元データ: tools/data/members.json(誕生日)+ tools/data/events.json(行事・記念日・毎週の番組)。
種類ごとに「何日前に書くか」を持ち、今日から見て「今すぐ / 今週書く / 来週書く / そのあと」に分ける。
サイト内に同じ話題の記事があるかを調べて「新規 / 更新」を付ける(--no-net で省く)。
確かめていない日にちは「要確認」と出す。マツの記憶で日にちを足さない(足すときは出どころを書く)。

usage:
    python tools/neta_calendar/neta_calendar.py              # 今日から35日ぶん
    --days 60 / --site snowman / --no-net / --no-open
結果は tools/neta_calendar/out/ に出る。Python 3.9対応。
"""
import argparse
import datetime
import html as htmllib
import json
import sys
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import blogkit  # noqa: E402

DATA = TOOLS / "data"
OUT = HERE / "out"
WEEK = "月火水木金土日"
BUCKETS = ["今すぐ書く", "今週書く", "来週書く", "そのあと"]


def load_data():
    members = json.loads((DATA / "members.json").read_text(encoding="utf-8"))["groups"]
    events = json.loads((DATA / "events.json").read_text(encoding="utf-8"))
    return members, events


def next_date(month, day, today):
    """今日以降でいちばん近い month/day。dayがNoneなら月の1日。2/29は平年なら2/28。"""
    for y in (today.year, today.year + 1):
        try:
            d = datetime.date(y, month, day or 1)
        except ValueError:
            d = datetime.date(y, month, 28)
        if d >= today or (day is None and d.month == today.month and d.year == today.year):
            return d
    return d


def bucket(write_by, today):
    gap = (write_by - today).days
    return BUCKETS[0] if gap <= 0 else BUCKETS[1] if gap <= 7 else BUCKETS[2] if gap <= 14 else BUCKETS[3]


def birthday_items(members, lead, today, days, sites=None):
    out = []
    for g, conf in members.items():
        site_key = next((k for k, s in blogkit.SITES.items() if s["group"] == g), None)
        if sites and site_key not in sites:
            continue
        for m in conf["members"]:
            shown = m.get("stage") or m["name"]
            if not m.get("birthday"):
                continue
            b = datetime.date.fromisoformat(m["birthday"])
            d = next_date(b.month, b.day, today)
            if (d - today).days > days:
                continue
            out.append({"date": d, "exact": True, "kind": "誕生日", "site": site_key, "verified": True,
                        "name": "{}の誕生日({}歳)".format(shown, d.year - b.year),
                        "angle": "誕生日のお祝い投稿まとめ・メンバーからのメッセージ・プレゼント・これまでの1年",
                        "search": m["name"] + " 誕生日", "write_by": d - datetime.timedelta(days=lead),
                        "source": m.get("source", "")})
    return out


def event_items(events, today, days, sites=None):
    lead = events["lead_days"]
    out = []
    for e in events["events"]:
        targets = [s for s in e["sites"] if not sites or s in sites]
        if not targets:
            continue
        ld = e.get("lead_days", lead.get(e["kind"], 14))
        if e["kind"] == "weekly":
            d = today + datetime.timedelta(days=(WEEK.index(e["weekday"]) - today.weekday()) % 7)
            if e.get("until") and d > datetime.date.fromisoformat(e["until"]):
                continue
            exact = True
        else:
            d = next_date(e["month"], e.get("day"), today)
            exact = e.get("day") is not None
        write_by = d - datetime.timedelta(days=ld)
        if (write_by - today).days > days:
            continue
        for s in targets:
            out.append({"date": d, "exact": exact, "kind": {"weekly": "毎週の番組", "anniversary": "記念日", "season": "季節",
                        "yearly": "毎年の行事", "once": "単発"}.get(e["kind"], e["kind"]), "site": s,
                        "verified": bool(e.get("verified")), "name": e["name"], "angle": e.get("angle", ""),
                        "search": e.get("search") or e["name"].split("(")[0].split("(")[0], "write_by": write_by,
                        "source": e.get("source", "")})
    return out


def build(members, events, today, days=35, sites=None):
    items = birthday_items(members, events["lead_days"]["birthday"], today, days + events["lead_days"]["birthday"], sites)
    items = [i for i in items if (i["write_by"] - today).days <= days] + event_items(events, today, days, sites)
    for i in items:
        i["bucket"] = bucket(i["write_by"], today)
    items.sort(key=lambda i: (BUCKETS.index(i["bucket"]), i["date"], i["site"] or ""))
    return items


def unverified_members(members):
    return [m["name"] for conf in members.values() for m in conf["members"] if not m.get("birthday")]


def find_existing(items, env):
    """サイト内に同じ話題の記事があるか(公開記事を検索)。あれば「更新」、無ければ「新規」。"""
    cache = {}
    for i in items:
        key = (i["site"], i["search"])
        if key not in cache:
            try:
                cache[key] = blogkit.WP(i["site"], env).get("/posts", auth=False, search=i["search"], per_page=3,
                                                            _fields="id,link,title")
            except Exception:  # noqa: BLE001
                cache[key] = None
        hits = cache[key]
        i["existing"] = None if hits is None else [{"id": h["id"], "url": h["link"],
                                                    "title": htmllib.unescape(h["title"]["rendered"])} for h in hits]


def label_date(i):
    d = i["date"]
    return "{}/{}({})".format(d.month, d.day, WEEK[d.weekday()]) if i["exact"] else "{}月(日にち要確認)".format(d.month)


def to_text(items, missing):
    lines, cur = [], None
    for i in items:
        if i["bucket"] != cur:
            cur = i["bucket"]
            lines.append("\n■ " + cur)
        ex = i.get("existing")
        state = "" if ex is None else " [更新: ID{}]".format(ex[0]["id"]) if ex else " [新規]"
        lines.append("  {} [{}] {}{}{}".format(label_date(i), blogkit.SITES[i["site"]]["label"], i["name"],
                                               "" if i["verified"] else " ※要確認", state))
    if missing:
        lines.append("\n誕生日が未確認で出していない人: " + "、".join(missing))
    return "\n".join(lines).strip()


CSS = """body{font-family:system-ui,sans-serif;margin:0;padding:16px;background:#f6f7f9;color:#222;line-height:1.6}h1{font-size:1.3em}
h2{font-size:1.1em;margin-top:26px;border-left:5px solid #c2410c;padding-left:8px}.card{background:#fff;border-radius:8px;padding:10px 14px;
margin:8px 0;box-shadow:0 1px 2px rgba(0,0,0,.08)}.d{font-weight:bold;margin-right:8px}.tag{font-size:.8em;background:#eee;border-radius:4px;
padding:1px 6px;margin-right:6px}.warn{background:#fde68a;color:#7c2d12}.new{background:#bbf7d0;color:#14532d}.upd{background:#bfdbfe;color:#1e3a8a}
.sub{color:#666;font-size:.88em}a{color:#1d4ed8}@media(prefers-color-scheme:dark){body{background:#16181c;color:#e6e6e6}.card{background:#22252b}
.tag{background:#333}.sub{color:#aaa}a{color:#8ab4f8}.warn{background:#92400e;color:#fef3c7}.new{background:#14532d;color:#dcfce7}
.upd{background:#1e3a8a;color:#dbeafe}}"""


def to_html(items, missing, today, days):
    esc = htmllib.escape
    parts, cur = [], None
    for i in items:
        if i["bucket"] != cur:
            cur = i["bucket"]
            parts.append("<h2>{}</h2>".format(cur))
        ex = i.get("existing")
        state = ""
        if ex:
            state = '<span class="tag upd">更新</span>' + " ".join(
                '<a href="{}" target="_blank" rel="noopener">{}</a>'.format(esc(h["url"]), esc(h["title"][:28])) for h in ex[:2])
        elif ex is not None:
            state = '<span class="tag new">新規</span>サイト内に同じ話題の記事は見つからない'
        parts.append('<div class="card"><span class="d">{d}</span><span class="tag">{s}</span><span class="tag">{k}</span>{w}'
                     '<div><b>{n}</b></div><div class="sub">{a}</div><div class="sub">書く目安: {wb} まで {st}</div>{src}</div>'
                     .format(d=label_date(i), s=esc(blogkit.SITES[i["site"]]["label"]), k=i["kind"], n=esc(i["name"]), a=esc(i["angle"]),
                             w="" if i["verified"] else '<span class="tag warn">要確認</span>',
                             wb="{}/{}".format(i["write_by"].month, i["write_by"].day), st=state,
                             src='<div class="sub">出どころ: {}</div>'.format(esc(i["source"])) if i["source"] else ""))
    miss = '<p class="sub">誕生日が未確認で出していない人: {}</p>'.format(esc("、".join(missing))) if missing else ""
    return ('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            "<title>ネタ先読みカレンダー {t}</title><style>{c}</style></head><body><h1>ネタ先読みカレンダー {t}</h1>"
            '<p class="sub">今日から{n}日ぶん。「要確認」は日にち・内容を公式で確かめてから書く。</p>{b}{m}</body></html>'
            ).format(t=today, c=CSS, n=days, b="\n".join(parts) or "<p>この期間に仕込むネタは無いワン</p>", m=miss)


def main(argv=None):
    ap = argparse.ArgumentParser(description="ネタ先読みカレンダー")
    ap.add_argument("--days", type=int, default=35)
    ap.add_argument("--site", default="")
    ap.add_argument("--no-net", action="store_true")
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args(argv)
    today = datetime.date.today()
    sites = [s.strip() for s in a.site.split(",") if s.strip()] or None
    members, events = load_data()
    items = build(members, events, today, a.days, sites)
    if not a.no_net:
        find_existing(items, blogkit.load_env())
    missing = unverified_members(members)
    print(to_text(items, missing))
    OUT.mkdir(exist_ok=True)
    path = OUT / "neta_calendar_{}.html".format(today.strftime("%Y%m%d"))
    path.write_text(to_html(items, missing, today, a.days), encoding="utf-8")
    print("\nできたワン:", path)
    if not a.no_open:
        webbrowser.open(path.as_uri())
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
