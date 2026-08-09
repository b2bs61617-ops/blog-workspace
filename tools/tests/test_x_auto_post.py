"""x_auto_post.py(記事公開時のX自動投稿)のテスト。

実際のAPI通信(post_thread)はtweepy/ネットワークが絡みモックが重いので対象外にし、
文字数計算・本文組み立て・サイト別認証情報の取り出しといった純粋関数のみを見る。
"""
from x_auto_post import (
    weighted_length,
    truncate_to_weight,
    compose_tweet_text,
    get_site_credentials,
)


class TestWeightedLength:
    def test_ascii_counts_as_one(self):
        assert weighted_length("abc") == 3

    def test_japanese_counts_as_two(self):
        assert weighted_length("あいう") == 6

    def test_mixed(self):
        assert weighted_length("ab日") == 2 + 2


class TestTruncateToWeight:
    def test_no_truncation_needed(self):
        assert truncate_to_weight("abc", 10) == "abc"

    def test_truncates_japanese_text(self):
        # 全角3文字(重み6)を重み4までに切ると2文字だけ残る
        assert truncate_to_weight("あいう", 4) == "あい"

    def test_does_not_split_over_budget(self):
        # "あ"(重み2)を追加すると重み3を超えるので1文字も入らない
        assert truncate_to_weight("あ", 1) == ""


class TestComposeTweetText:
    def test_combines_hook_and_hashtags(self):
        text = compose_tweet_text("フック文", "#今日好き #今日好きになりました")
        assert text == "フック文\n\n#今日好き #今日好きになりました"

    def test_no_hashtags_returns_hook_only(self):
        assert compose_tweet_text("フック文", "") == "フック文"

    def test_truncates_long_hook_to_fit_280_weight(self):
        long_hook = "あ" * 200
        hashtags = "#今日好き"
        text = compose_tweet_text(long_hook, hashtags, max_weight=280)
        assert weighted_length(text) <= 280
        assert text.endswith(hashtags)

    def test_hashtags_never_dropped_when_hook_shrinks(self):
        long_hook = "あ" * 500
        hashtags = "#今日好き #今日好きになりました"
        text = compose_tweet_text(long_hook, hashtags, max_weight=280)
        assert hashtags in text


class TestGetSiteCredentials:
    def test_returns_none_when_unset(self):
        assert get_site_credentials("trend", {}) is None

    def test_returns_none_when_partially_set(self):
        env = {"X_TREND_API_KEY": "k", "X_TREND_API_SECRET": "s"}
        assert get_site_credentials("trend", env) is None

    def test_returns_dict_when_fully_set(self):
        env = {
            "X_TREND_API_KEY": "k",
            "X_TREND_API_SECRET": "s",
            "X_TREND_ACCESS_TOKEN": "t",
            "X_TREND_ACCESS_TOKEN_SECRET": "ts",
        }
        creds = get_site_credentials("trend", env)
        assert creds == {
            "api_key": "k",
            "api_secret": "s",
            "access_token": "t",
            "access_token_secret": "ts",
        }

    def test_unknown_site_raises(self):
        import pytest
        with pytest.raises(ValueError):
            get_site_credentials("unknown", {})
