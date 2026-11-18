import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "neta_watch"))
import neta_watch as nw  # noqa: E402


def test_safe_name_removes_bad_chars():
    assert nw.safe_name('a/b:c*?"<>|d') == "a b c d"
    assert nw.safe_name("") == "no_title"
    assert len(nw.safe_name("x" * 100, 10)) == 10


def test_mmss():
    assert nw.mmss(5) == "0:05"
    assert nw.mmss(125.7) == "2:05"
    assert nw.mmss(3725) == "1:02:05"
    assert nw.mmss(None) == ""


def test_parse_json_text_with_fence():
    assert nw.parse_json_text('```json\n{"a": 1}\n```') == {"a": 1}
    assert nw.parse_json_text('ok [1, 2] end') == [1, 2]
    assert nw.parse_json_text("no json") is None


def test_neta_timestamps_sorted_and_filtered():
    neta = [{"kind": "服", "what": "帽子", "time_sec": 30}, {"kind": "場所", "time_sec": 999}, {"kind": "小物", "time_sec": "x"}]
    out = nw.neta_timestamps(neta, 100, uniform=2)
    assert [round(t) for t, _ in out] == [5, 30, 95]
    assert out[1][1] == "服_帽子"


def test_split_bubbles_limits():
    bubbles, dropped = nw.split_bubbles(["a" * 40] * 10, "H", limit=100, max_bubbles=2)
    assert len(bubbles) == 2 and all(len(b) <= 100 for b in bubbles)
    assert dropped > 0
    bubbles, dropped = nw.split_bubbles(["x", "y"], "H")
    assert bubbles == ["H\n\nx\n\ny"] and dropped == 0


def test_due():
    now = datetime.datetime(2026, 11, 18, 20, 5, tzinfo=datetime.timezone.utc)
    assert nw.due(20, (8, 20), None, now)
    assert not nw.due(19, (8, 20), None, now)
    assert not nw.due(20, (8, 20), (now - datetime.timedelta(minutes=30)).isoformat(), now)
    assert nw.due(20, (8, 20), (now - datetime.timedelta(hours=12)).isoformat(), now)
