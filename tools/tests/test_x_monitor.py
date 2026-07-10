"""毎朝の自動監視(koikeyz-monitor/x_monitor.py)の純粋関数のテスト。

過去に「収集セレクタが古くて投稿を1件も拾えていなかった」バグが出た経緯があり、
このスクリプトの取りこぼしは記事ネタの見落としに直結する。
特に日付境界(UTC→JST変換)は黙って1日分の投稿を落としうる一番怖い箇所なので重点的に見る。
"""
from datetime import date, datetime

import pytest

from x_monitor import dedupe_posts, is_noise, is_target_date, normalize_for_dedup

# このリポジトリの運用PCはすべて日本(JST, UTC+9)を想定しているため、
# それ以外のタイムゾーンで実行された場合はタイムゾーン依存のテストをスキップする。
_LOCAL_OFFSET = datetime.now().astimezone().utcoffset()
requires_jst = pytest.mark.skipif(
    _LOCAL_OFFSET is None or _LOCAL_OFFSET.total_seconds() != 9 * 3600,
    reason="このテストはJST(UTC+9)で実行するPCを想定している",
)


class TestIsNoise:
    def test_detects_torea_koukan(self):
        assert is_noise("このトレカ譲ってください、条件は郵送のみでお願いします") is True

    def test_detects_doutan_sama(self):
        assert is_noise("同担様、連番希望です") is True

    def test_detects_amazon_affiliate_tag(self):
        assert is_noise("おすすめグッズはこちら http://amazon.co.jp/dp/xxx?tag=abc-22") is True

    def test_normal_fan_post_is_not_noise(self):
        assert is_noise("今日のライブ最高だった!ずっと見ていたい") is False

    def test_empty_string_is_not_noise(self):
        assert is_noise("") is False


class TestNormalizeForDedup:
    def test_removes_urls(self):
        assert normalize_for_dedup("見て https://t.co/abc123 これ") == "見てこれ"

    def test_collapses_whitespace_including_fullwidth_space(self):
        assert normalize_for_dedup("テキスト　です") == normalize_for_dedup("テキストです")

    def test_texts_differing_only_by_url_and_spacing_are_same_key(self):
        a = normalize_for_dedup("告知です  https://x.com/aaa/status/1")
        b = normalize_for_dedup("告知です https://x.com/bbb/status/2")
        assert a == b

    def test_texts_with_different_content_are_different_keys(self):
        a = normalize_for_dedup("告知A")
        b = normalize_for_dedup("告知B")
        assert a != b


class TestIsTargetDate:
    def test_empty_string_is_false(self):
        assert is_target_date("", date(2026, 7, 9)) is False

    def test_invalid_string_is_false(self):
        assert is_target_date("not-a-date", date(2026, 7, 9)) is False

    @requires_jst
    def test_utc_time_that_is_still_previous_day_in_jst(self):
        # UTC 14:00 -> JST 23:00 (同じ日)
        assert is_target_date("2026-07-08T14:00:00Z", date(2026, 7, 8)) is True

    @requires_jst
    def test_utc_time_that_rolls_over_to_next_day_in_jst(self):
        # UTC 15:00 -> JST 00:00 翌日。ここを日付境界と誤認すると1日分丸ごと取りこぼす。
        assert is_target_date("2026-07-08T15:00:00Z", date(2026, 7, 9)) is True
        assert is_target_date("2026-07-08T15:00:00Z", date(2026, 7, 8)) is False


class TestDedupePosts:
    def test_merges_duplicate_text_and_counts(self):
        posts = [
            {"text": "告知です https://x.com/a/1", "date": "2026-07-08T10:00:00Z"},
            {"text": "告知です https://x.com/b/2", "date": "2026-07-08T11:00:00Z"},
            {"text": "別の投稿", "date": "2026-07-08T12:00:00Z"},
        ]
        result = dedupe_posts(posts)
        assert len(result) == 2
        assert result[0]["duplicate_count"] == 2
        assert result[1]["duplicate_count"] == 1

    def test_keeps_first_occurrence_order(self):
        posts = [
            {"text": "B投稿"},
            {"text": "A投稿"},
            {"text": "B投稿"},
        ]
        result = dedupe_posts(posts)
        assert [p["text"] for p in result] == ["B投稿", "A投稿"]

    def test_empty_list_returns_empty_list(self):
        assert dedupe_posts([]) == []
