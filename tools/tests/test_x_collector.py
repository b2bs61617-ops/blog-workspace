"""Xiy(tools/Xiy/x_collector.py)のURL処理まわりのテスト。

過去に収集セレクタの陳腐化でツイートを1件も拾えなくなったことがあり、
その周辺(URL変換・プラットフォーム判定)も回帰しやすい箇所として重点的に見る。
"""
from x_collector import build_x_search_url, detect_platform, x_full_size_url


class TestXFullSizeUrl:
    def test_replaces_existing_name_param_with_orig(self):
        url = "https://pbs.twimg.com/media/abc.jpg?name=small"
        assert x_full_size_url(url) == "https://pbs.twimg.com/media/abc.jpg?name=orig"

    def test_adds_name_param_when_missing_with_existing_query(self):
        url = "https://pbs.twimg.com/media/abc.jpg?format=jpg"
        assert x_full_size_url(url) == "https://pbs.twimg.com/media/abc.jpg?format=jpg&name=orig"

    def test_adds_name_param_when_no_query_at_all(self):
        url = "https://pbs.twimg.com/media/abc.jpg"
        assert x_full_size_url(url) == "https://pbs.twimg.com/media/abc.jpg?name=orig"


class TestDetectPlatform:
    def test_youtube_watch_url(self):
        assert detect_platform("https://www.youtube.com/watch?v=abc123") == "youtube"

    def test_youtube_short_url(self):
        assert detect_platform("https://youtu.be/abc123") == "youtube"

    def test_instagram_url(self):
        assert detect_platform("https://www.instagram.com/p/abc123/") == "instagram"

    def test_x_explore_is_trending_not_x(self):
        assert detect_platform("https://x.com/explore/tabs/trending") == "trending"

    def test_ordinary_x_post_is_x(self):
        assert detect_platform("https://x.com/someuser/status/12345") == "x"


class TestBuildXSearchUrl:
    def test_live_tab_appends_f_live(self):
        url = build_x_search_url("キナリ", tab="live")
        assert url.startswith("https://x.com/search?q=")
        assert url.endswith("&f=live")

    def test_non_live_tab_has_no_f_param(self):
        url = build_x_search_url("キナリ", tab="top")
        assert "&f=" not in url

    def test_keyword_is_url_encoded(self):
        url = build_x_search_url("A B")
        assert "A+B" in url or "A%20B" in url
