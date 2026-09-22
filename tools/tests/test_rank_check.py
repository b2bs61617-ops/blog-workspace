"""rank_check.py(Yahoo!検索順位チェック)のテスト。

ブラウザ操作(Playwright)そのものはモックが重いので対象外にし、
検索結果リンクの重複除去・順位判定という副作用のない純粋関数のみを見る。
"""
from rank_check import dedupe_urls, find_rank


class TestDedupeUrls:
    def test_removes_duplicates_keeping_first_occurrence(self):
        urls = ["https://a.com/1", "https://b.com/1", "https://a.com/1"]
        assert dedupe_urls(urls) == ["https://a.com/1", "https://b.com/1"]

    def test_excludes_urls_matching_substrings(self):
        urls = [
            "https://a.com/1",
            "https://search.yahoo.co.jp/search?p=x",
            "https://search.yahoo.co.jp/chat?q=x",
            "https://b.com/1",
        ]
        assert dedupe_urls(urls, exclude_substrings=["search.yahoo.co.jp/"]) == [
            "https://a.com/1",
            "https://b.com/1",
        ]

    def test_keeps_other_subdomains_of_excluded_domain(self):
        urls = ["https://travel.yahoo.co.jp/kanko/spot-1"]
        assert dedupe_urls(urls, exclude_substrings=["search.yahoo.co.jp/"]) == urls


class TestFindRank:
    def test_finds_first_matching_domain_rank(self):
        urls = ["https://a.com/1", "https://chomoand-4.blog/x-19", "https://chomoand-4.blog/"]
        rank, matched = find_rank(urls, "chomoand-4.blog")
        assert rank == 2
        assert matched == "https://chomoand-4.blog/x-19"

    def test_returns_none_when_not_found(self):
        urls = ["https://a.com/1", "https://b.com/1"]
        rank, matched = find_rank(urls, "chomoand-4.blog")
        assert rank is None
        assert matched is None
