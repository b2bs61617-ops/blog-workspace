"""check_search_console.py(Search Console URL Inspection一括チェック)のテスト。

実際のAPI通信(inspect_url)はサービスアカウント認証が絡みモックが重いので対象外にし、
サイトマップXMLのパースという副作用のない純粋関数のみを見る。
"""
from check_search_console import parse_sitemap_xml


SITEMAP_INDEX_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://chomoand-1.com/post-sitemap.xml</loc></sitemap>
  <sitemap><loc>https://chomoand-1.com/page-sitemap.xml</loc></sitemap>
</sitemapindex>
"""

URLSET_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://chomoand-1.com/article-1/</loc></url>
  <url><loc>https://chomoand-1.com/article-2/</loc></url>
</urlset>
"""


class TestParseSitemapXml:
    def test_sitemap_index_returns_child_sitemap_urls(self):
        tag, locs = parse_sitemap_xml(SITEMAP_INDEX_XML)
        assert tag == "sitemapindex"
        assert locs == [
            "https://chomoand-1.com/post-sitemap.xml",
            "https://chomoand-1.com/page-sitemap.xml",
        ]

    def test_urlset_returns_page_urls(self):
        tag, locs = parse_sitemap_xml(URLSET_XML)
        assert tag == "urlset"
        assert locs == [
            "https://chomoand-1.com/article-1/",
            "https://chomoand-1.com/article-2/",
        ]
