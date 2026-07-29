"""tools/youtube-talent-monitor/video_monitor.py の純粋関数のテスト。"""
from video_monitor import diff_new_videos, format_notification, parse_feed_xml, MAX_NOTIFY_LINES

VIDEOS = [
    {"video_id": "v3", "title": "動画3(最新)", "published_at": "2026-07-29T10:00:00Z"},
    {"video_id": "v2", "title": "動画2", "published_at": "2026-07-28T10:00:00Z"},
    {"video_id": "v1", "title": "動画1", "published_at": "2026-07-27T10:00:00Z"},
]


class TestDiffNewVideos:
    def test_first_run_only_latest_one(self):
        assert diff_new_videos(VIDEOS, None) == [VIDEOS[0]]

    def test_no_new_video_when_latest_already_seen(self):
        assert diff_new_videos(VIDEOS, "v3") == []

    def test_returns_only_videos_newer_than_last_seen(self):
        assert diff_new_videos(VIDEOS, "v2") == [VIDEOS[0]]

    def test_multiple_new_videos_since_last_check(self):
        assert diff_new_videos(VIDEOS, "v1") == [VIDEOS[0], VIDEOS[1]]

    def test_last_seen_not_in_list_returns_all(self):
        # 保持期間を超えて再生リストから外れた等、last_seen_idが見つからない場合は全件返す
        assert diff_new_videos(VIDEOS, "old-deleted-video") == VIDEOS

    def test_empty_videos(self):
        assert diff_new_videos([], "v1") == []


class TestFormatNotification:
    def test_single_channel_single_video(self):
        msg = format_notification({"嵐": [VIDEOS[0]]})
        assert "嵐" in msg
        assert "動画3(最新)" in msg
        assert "https://youtu.be/v3" in msg

    def test_multiple_channels(self):
        msg = format_notification({"嵐": [VIDEOS[0]], "SixTONES": [VIDEOS[1]]})
        assert "嵐" in msg
        assert "SixTONES" in msg

    def test_truncates_beyond_max_notify_lines(self):
        many = {f"ch{i}": [{"video_id": f"v{i}", "title": f"title{i}", "published_at": ""}]
                for i in range(MAX_NOTIFY_LINES + 5)}
        msg = format_notification(many)
        assert "ほか5件" in msg
        assert msg.count("https://youtu.be/") == MAX_NOTIFY_LINES


SAMPLE_FEED_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns:media="http://search.yahoo.com/mrss/" xmlns="http://www.w3.org/2005/Atom">
 <link rel="self" href="http://www.youtube.com/feeds/videos.xml?channel_id=UCxxxx"/>
 <id>yt:channel:xxxx</id>
 <yt:channelId>UCxxxx</yt:channelId>
 <title>テストチャンネル</title>
 <entry>
  <id>yt:video:aaa1111</id>
  <yt:videoId>aaa1111</yt:videoId>
  <yt:channelId>UCxxxx</yt:channelId>
  <title>新しい動画</title>
  <link rel="alternate" href="https://www.youtube.com/watch?v=aaa1111"/>
  <published>2026-07-29T10:00:00+00:00</published>
  <updated>2026-07-29T10:05:00+00:00</updated>
 </entry>
 <entry>
  <id>yt:video:bbb2222</id>
  <yt:videoId>bbb2222</yt:videoId>
  <yt:channelId>UCxxxx</yt:channelId>
  <title>古い動画</title>
  <link rel="alternate" href="https://www.youtube.com/watch?v=bbb2222"/>
  <published>2026-07-20T10:00:00+00:00</published>
  <updated>2026-07-20T10:05:00+00:00</updated>
 </entry>
</feed>
"""


class TestParseFeedXml:
    def test_extracts_videos_in_feed_order(self):
        videos = parse_feed_xml(SAMPLE_FEED_XML)
        assert videos == [
            {"video_id": "aaa1111", "title": "新しい動画", "published_at": "2026-07-29T10:00:00+00:00"},
            {"video_id": "bbb2222", "title": "古い動画", "published_at": "2026-07-20T10:00:00+00:00"},
        ]

    def test_empty_feed_has_no_entries(self):
        empty = '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://www.youtube.com/xml/schemas/2015"></feed>'
        assert parse_feed_xml(empty) == []
