"""tools/youtube-talent-monitor/video_monitor.py の純粋関数のテスト。"""
from video_monitor import diff_new_videos, format_notification, MAX_NOTIFY_LINES

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
