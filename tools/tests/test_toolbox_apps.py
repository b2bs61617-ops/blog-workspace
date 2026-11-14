# -*- coding: utf-8 -*-
"""伸びしろ診断 / ネタ先読みカレンダー / 道具箱 / 誕生日確認 の純粋関数のテスト。"""
import datetime

import pytest

import neta_calendar as nc
import nobishiro as nb
import toolbox
import verify_birthdays as vb

TODAY = datetime.date(2026, 11, 14)


def _post(pid, title, body, link=None, modified="2026-11-01T00:00:00", media=5):
    return {"id": pid, "link": link or "https://chomoand-2.com/p-{}/".format(pid), "slug": "p-{}".format(pid),
            "title": {"rendered": title}, "content": {"rendered": body}, "modified": modified,
            "date": modified, "featured_media": media}


# ---------------- nobishiro
def test_norm_url():
    assert nb.norm_url("https://www.Chomoand-2.com/abc-12/?x=1#y") == "chomoand-2.com/abc-12"


def test_measure_and_inbound_and_score():
    a = _post(1, "目黒蓮のニットはどこの？", '<h2>a</h2><p>' + "あ" * 3000 + '</p><a href="https://chomoand-2.com/p-2/">x</a>'
              '<img src="a.jpg" alt="x"><h2>b</h2><h2>c</h2>')
    b = _post(2, "短い記事", "<h2>a</h2><p>短い</p><hr><img src='b.jpg'>", modified="2025-01-01T00:00:00", media=0)
    rows = [nb.measure(p, "chomoand-2.com", TODAY) for p in (a, b)]
    nb.count_inbound(rows)
    ra, rb = rows
    assert ra["links_out"] == 1 and ra["links_in"] == 0 and rb["links_in"] == 1
    assert ra["question"] and not rb["question"] and rb["no_eyecatch"] and rb["hr"] and rb["img_no_alt"] == 1
    pa, wa = nb.score(ra)
    pb, wb = nb.score(rb)
    assert pb > pa
    assert any("かなり短い" in x for x in wb) and any("アイキャッチ" in x for x in wb) and any("更新から" in x for x in wb)
    assert wa[0] == "どの記事からもリンクされていない" and not any("字" in x and "短い" in x for x in wa)


def test_score_uses_search_data():
    r = nb.measure(_post(1, "題？", "<h2>a</h2><h2>b</h2><h2>c</h2><p>" + "あ" * 3000 + "</p>"), "chomoand-2.com", TODAY)
    r.update({"links_in": 2, "links_out": 1, "gsc": {"impressions": 500, "clicks": 2, "ctr": 0.004, "position": 9.2}})
    pts, why = nb.score(r)
    assert pts >= 55 and "表示500回" in why[0] and "検索9位" in why[1]


def test_title_tokens_and_link_ideas():
    assert nb.title_tokens("【いのありちねん】知念侑李の免許合宿はどこ？浜松自動車学校が有力", skip={"知念侑李"}) == ["免許合宿", "浜松自動車学校"]
    a = nb.measure(_post(1, "松茸ロケ地の峰屋本店はどこ？", "<p>本文</p>"), "chomoand-2.com", TODAY)
    b = nb.measure(_post(2, "すのちゅーぶまとめ！", "<p>松茸の回で行った峰屋本店が話題。</p>"), "chomoand-2.com", TODAY)
    c = nb.measure(_post(3, "関係ない記事？", '<p>峰屋本店</p><a href="https://chomoand-2.com/p-1/">リンクずみ</a>'), "chomoand-2.com", TODAY)
    ideas = nb.link_ideas([a, b, c])
    assert [(i["from"]["id"], i["to"]["id"]) for i in ideas] == [(2, 1)]


# ---------------- neta_calendar
def test_next_date_and_bucket():
    assert nc.next_date(11, 14, TODAY) == TODAY
    assert nc.next_date(11, 13, TODAY) == datetime.date(2027, 11, 13)
    assert nc.next_date(11, None, TODAY) == datetime.date(2026, 11, 1)   # 今月の「日にち未定」は今月扱い
    assert nc.next_date(2, 29, TODAY) == datetime.date(2027, 2, 28)
    d = datetime.timedelta
    assert [nc.bucket(TODAY + d(days=n), TODAY) for n in (-3, 0, 7, 8, 14, 15)] == ["今すぐ書く", "今すぐ書く", "今週書く", "来週書く", "来週書く", "そのあと"]


MEMBERS = {"travis": {"label": "Travis Japan", "members": [
    {"name": "川島如恵留", "birthday": "1994-11-22"}, {"name": "松田元太", "birthday": "1999-04-19"}, {"name": "誰か", "birthday": None}]}}
EVENTS = {"lead_days": {"birthday": 14, "yearly": 21, "weekly": 0}, "events": [
    {"name": "紅白歌合戦", "kind": "yearly", "month": 12, "day": 31, "sites": ["trend", "travis"], "lead_days": 45, "verified": True},
    {"name": "番組(毎週金曜)", "kind": "weekly", "weekday": "金", "sites": ["trend"], "verified": False},
    {"name": "終わった番組", "kind": "weekly", "weekday": "金", "until": "2026-11-13", "sites": ["trend"]},
    {"name": "夏の行事", "kind": "yearly", "month": 8, "day": 1, "sites": ["trend"], "verified": True}]}


def test_build_calendar():
    items = nc.build(MEMBERS, EVENTS, TODAY, days=35)
    names = [(i["name"], i["site"], i["bucket"]) for i in items]
    assert ("川島如恵留の誕生日(32歳)", "travis", "今すぐ書く") in names
    assert ("紅白歌合戦", "trend", "今週書く") in names and ("紅白歌合戦", "travis", "今週書く") in names
    assert ("番組(毎週金曜)", "trend", "今週書く") in names
    assert not any("松田元太" in n or "終わった" in n or "夏" in n for n, _, _ in names)
    weekly = next(i for i in items if i["kind"] == "毎週の番組")
    assert weekly["date"] == datetime.date(2026, 11, 20) and not weekly["verified"] and weekly["search"] == "番組"
    assert nc.unverified_members(MEMBERS) == ["誰か"]
    assert [i["site"] for i in nc.build(MEMBERS, EVENTS, TODAY, 35, ["travis"])] == ["travis", "travis"]
    text = nc.to_text(items, ["誰か"])
    assert "※要確認" in text and "誰か" in text and "11/22(日)" in text


# ---------------- verify_birthdays
def test_parse_birthday():
    assert vb.parse_birthday("{{生年月日と年齢|1997|2|16}}") == "1997-02-16"
    assert vb.parse_birthday("| 生年 = 1993\n| 生月 = 5\n| 生日 = 17") == "1993-05-17"
    assert vb.parse_birthday("何もない") is None


# ---------------- toolbox
def test_recommend_model():
    assert [toolbox.recommend_model(g) for g in (4, 8, 16, 31.5)] == ["gemma3:1b", "gemma3:4b", "gemma3:4b", "gemma3:12b"]


def test_build_command_is_fixed_shape():
    cmd = toolbox.build_command("fact", {"site": "snowman", "post_id": "687", "net": "on"})
    assert cmd[2].endswith("fact_check.py") and cmd[3:] == ["--site", "snowman", "--post-id", "687"]
    cmd = toolbox.build_command("fact", {"site": "trend", "post_id": "1", "names": "内村光良", "ai": "on"})
    assert cmd[3:] == ["--site", "trend", "--post-id", "1", "--names", "内村光良", "--no-net", "--ai"]
    assert toolbox.build_command("nobishiro", {})[3:] == []
    assert toolbox.build_command("neta", {"days": "abc", "site": "ktl"})[3:] == ["--days", "35", "--site", "ktl"]
    assert toolbox.build_command("xcheck", {"text": "a", "tags": "#a #b"})[3:] == ["check", "--text", "a", "--tags", "#a #b"]


@pytest.mark.parametrize("tool,q", [("fact", {"site": "x; rm -rf", "post_id": "1"}), ("fact", {"site": "trend", "post_id": "1;2"}),
                                    ("fact", {"site": "trend"}), ("suggest", {"name": " "}), ("unknown", {}), ("xcheck", {})])
def test_build_command_rejects_bad_input(tool, q):
    with pytest.raises(ValueError):
        toolbox.build_command(tool, q)
