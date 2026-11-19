# -*- coding: utf-8 -*-
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "neta_watch"))
import fan_search as fs  # noqa: E402


def test_extract_questions():
    qs = fs.extract_questions("この服どこのブランド？教えてください！ かっこいい。 https://t.co/abc")
    assert "この服どこのブランド？" in qs
    assert "教えてください！" in qs
    assert all("かっこいい" not in q for q in qs)


def test_reply_count():
    assert fs.reply_count("12 件の返信。返信する") == 12
    assert fs.reply_count("1.2万 件の返信") == 12000
    assert fs.reply_count("") == 0


def test_own_account():
    assert fs.own_account("https://x.com/chomoand17/status/1")
    assert fs.own_account("https://www.threads.com/@chomotirend/post/abc")
    assert not fs.own_account("https://x.com/someone/status/1")


def test_fresh_and_since():
    now = datetime.datetime(2026, 11, 19, 14, tzinfo=datetime.timezone.utc)
    assert fs.since_time(None, now) == now - datetime.timedelta(hours=fs.FIRST_HOURS)
    old = (now - datetime.timedelta(days=3)).isoformat()
    assert fs.since_time(old, now) == now - datetime.timedelta(hours=fs.MAX_HOURS)
    since = now - datetime.timedelta(hours=2)
    assert fs.fresh({"time": "2026-11-19T13:00:00.000Z"}, since)
    assert not fs.fresh({"time": "2026-11-19T11:00:00.000Z"}, since)
    assert fs.fresh({"time": None}, since)


def test_keywords_for():
    kws = fs.keywords_for({"label": "Snow Man", "aliases": ["スノーマン", "スノ"], "members": [{"name": "目黒蓮"}]})
    assert kws == [("Snow Man", True), ("スノーマン", False), ("目黒蓮", False)]
