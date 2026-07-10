"""tools/x-trend-monitor/trend_monitor.py の純粋関数のテスト。"""
from datetime import datetime

from trend_monitor import (
    filter_new_trends,
    mark_seen,
    parse_trend_lines,
    prune_state,
    should_notify_failure,
)

NOW = datetime(2026, 7, 10, 12, 0, 0)


class TestParseTrendLines:
    def test_standard_block(self):
        parsed = parse_trend_lines(["1", "トレンド", "大谷翔平", "12.3万件のポスト"])
        assert parsed == {"name": "大谷翔平", "category": "トレンド", "volume": "12.3万件のポスト"}

    def test_category_with_middle_dot(self):
        parsed = parse_trend_lines(["2", "音楽 · トレンド", "#NewJeans"])
        assert parsed["name"] == "#NewJeans"
        assert parsed["category"] == "音楽 · トレンド"
        assert parsed["volume"] == ""

    def test_japan_trend_category(self):
        parsed = parse_trend_lines(["日本のトレンド", "呪術廻戦", "5.4万件のポスト"])
        assert parsed["name"] == "呪術廻戦"

    def test_promoted_is_skipped(self):
        assert parse_trend_lines(["プロモーション", "○○キャンペーン"]) is None

    def test_empty_lines_only(self):
        assert parse_trend_lines(["", "  ", "3"]) is None

    def test_english_volume_suffix(self):
        parsed = parse_trend_lines(["4", "トレンド", "WBC", "31.2K posts"])
        assert parsed["name"] == "WBC"
        assert parsed["volume"] == "31.2K posts"


class TestFilterNewTrends:
    def test_unseen_trend_is_new(self):
        trends = [{"name": "大谷翔平"}]
        assert filter_new_trends(trends, {}, now=NOW) == trends

    def test_recently_seen_trend_is_filtered(self):
        state = {"大谷翔平": "2026-07-10T09:00:00"}  # 3時間前 < 24h
        assert filter_new_trends([{"name": "大谷翔平"}], state, now=NOW) == []

    def test_cooldown_expired_trend_is_new_again(self):
        state = {"大谷翔平": "2026-07-08T09:00:00"}  # 2日前 > 24h
        assert filter_new_trends([{"name": "大谷翔平"}], state, now=NOW) == [{"name": "大谷翔平"}]

    def test_broken_state_value_treated_as_new(self):
        state = {"大谷翔平": "not-a-date"}
        assert filter_new_trends([{"name": "大谷翔平"}], state, now=NOW) == [{"name": "大谷翔平"}]


class TestState:
    def test_mark_seen_records_timestamp(self):
        state = mark_seen({}, [{"name": "大谷翔平"}], now=NOW)
        assert state["大谷翔平"] == "2026-07-10T12:00:00"

    def test_prune_removes_old_entries(self):
        state = {
            "古いトレンド": "2026-06-01T00:00:00",
            "新しいトレンド": "2026-07-10T09:00:00",
            "_last_failure_notify": "2026-06-01T00:00:00",  # メタ情報は日付が古くても残す
        }
        pruned = prune_state(state, now=NOW, keep_days=14)
        assert "古いトレンド" not in pruned
        assert "新しいトレンド" in pruned
        assert "_last_failure_notify" in pruned

    def test_prune_drops_broken_values(self):
        assert prune_state({"壊れた値": 123}, now=NOW) == {}


class TestShouldNotifyFailure:
    def test_first_failure_notifies(self):
        assert should_notify_failure({}, now=NOW) is True

    def test_recent_failure_suppresses(self):
        state = {"_last_failure_notify": "2026-07-10T10:00:00"}  # 2時間前 < 6h
        assert should_notify_failure(state, now=NOW) is False

    def test_old_failure_notifies_again(self):
        state = {"_last_failure_notify": "2026-07-10T01:00:00"}  # 11時間前 > 6h
        assert should_notify_failure(state, now=NOW) is True
