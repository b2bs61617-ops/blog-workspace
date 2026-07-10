"""youtube_trending.py(急上昇動画からネタ探し)のデータ整形ロジックのテスト。

APIを叩く部分(fetch_trending等)はモックが重いので対象外にし、
「除外判定」「表示整形」「集計」という、ネタ選定の精度に直結する純粋関数だけを見る。
"""
from youtube_trending import format_subscribers, is_excluded_channel, summarize


class TestIsExcludedChannel:
    def test_excludes_auto_generated_topic_channel(self):
        assert is_excluded_channel("なにわ男子 - Topic") is True

    def test_excludes_official_in_name(self):
        assert is_excluded_channel("Sony Music Official") is True

    def test_excludes_japanese_koushiki(self):
        assert is_excluded_channel("〇〇公式チャンネル") is True

    def test_does_not_exclude_ordinary_channel(self):
        assert is_excluded_channel("ゆるふわ美容チャンネル") is False


class TestFormatSubscribers:
    def test_none_is_hikoukai(self):
        assert format_subscribers(None) == "非公開"

    def test_number_gets_comma_separated(self):
        assert format_subscribers(1234567) == "1,234,567"

    def test_zero_is_formatted_as_zero_not_hikoukai(self):
        assert format_subscribers(0) == "0"


class TestSummarize:
    def test_builds_rows_with_expected_fields(self):
        items = [
            {
                "id": "vid1",
                "snippet": {"title": "動画A", "channelTitle": "チャンネルA", "channelId": "ch1"},
                "statistics": {"viewCount": "1000"},
            },
        ]
        rows = summarize(items, {"ch1": 5000})
        assert rows == [
            {
                "title": "動画A",
                "channel": "チャンネルA",
                "views": 1000,
                "url": "https://www.youtube.com/watch?v=vid1",
                "channel_video_count": 1,
                "subscribers": 5000,
            }
        ]

    def test_counts_multiple_videos_from_same_channel(self):
        items = [
            {"id": "v1", "snippet": {"title": "A", "channelTitle": "同じ人", "channelId": "c1"}, "statistics": {"viewCount": "10"}},
            {"id": "v2", "snippet": {"title": "B", "channelTitle": "同じ人", "channelId": "c1"}, "statistics": {"viewCount": "20"}},
        ]
        rows = summarize(items, {"c1": 100})
        assert [r["channel_video_count"] for r in rows] == [2, 2]

    def test_missing_subscriber_entry_defaults_to_none(self):
        items = [
            {"id": "v1", "snippet": {"title": "A", "channelTitle": "誰か", "channelId": "unknown"}, "statistics": {"viewCount": "10"}},
        ]
        rows = summarize(items, {})
        assert rows[0]["subscribers"] is None
