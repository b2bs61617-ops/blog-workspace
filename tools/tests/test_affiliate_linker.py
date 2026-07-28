"""affiliate_linker.py(コイキーズ記事の商品アフィリエイトリンク提案)のテスト。

外部API(楽天商品検索・Amazon)を叩く部分はモックが重いので対象外にし、
「Amazon検索リンクの組み立て」「楽天APIレスポンスの整形」という
リンクの正しさに直結する純粋関数だけを見る。
"""
from affiliate_linker import build_amazon_search_url, parse_rakuten_items, search_product


class TestBuildAmazonSearchUrl:
    def test_includes_keyword_and_tag(self):
        url = build_amazon_search_url("ネックレス", "mytag-22")
        assert url.startswith("https://www.amazon.co.jp/s?")
        assert "tag=mytag-22" in url

    def test_encodes_japanese_keyword(self):
        url = build_amazon_search_url("加藤大樹 ネックレス", "mytag-22")
        assert "k=%E5%8A%A0%E8%97%A4%E5%A4%A7%E6%A8%B9" in url

    def test_encodes_ampersand_in_keyword(self):
        url = build_amazon_search_url("A&B ブランド", "mytag-22")
        assert "A%26B" in url

    def test_omits_tag_param_when_tag_missing(self):
        url = build_amazon_search_url("ネックレス", None)
        assert "tag=" not in url


class TestParseRakutenItems:
    def test_extracts_expected_fields_with_affiliate_url(self):
        raw = [{
            "Item": {
                "itemName": "テストネックレス",
                "itemPrice": 3980,
                "shopName": "テストショップ",
                "itemUrl": "https://item.rakuten.co.jp/plain/",
                "affiliateUrl": "https://hb.afl.rakuten.co.jp/tracked/",
                "mediumImageUrls": [{"imageUrl": "https://image.rakuten.co.jp/x.jpg"}],
                "reviewAverage": 4.5,
                "reviewCount": 12,
            }
        }]
        result = parse_rakuten_items(raw)
        assert result == [{
            "name": "テストネックレス",
            "price": 3980,
            "shop": "テストショップ",
            "url": "https://hb.afl.rakuten.co.jp/tracked/",
            "image": "https://image.rakuten.co.jp/x.jpg",
            "review_average": 4.5,
            "review_count": 12,
        }]

    def test_falls_back_to_item_url_when_no_affiliate_url(self):
        raw = [{"Item": {"itemName": "商品", "itemUrl": "https://item.rakuten.co.jp/plain/"}}]
        result = parse_rakuten_items(raw)
        assert result[0]["url"] == "https://item.rakuten.co.jp/plain/"

    def test_handles_missing_image(self):
        raw = [{"Item": {"itemName": "商品", "mediumImageUrls": []}}]
        result = parse_rakuten_items(raw)
        assert result[0]["image"] is None

    def test_empty_list_returns_empty(self):
        assert parse_rakuten_items([]) == []


class TestSearchProduct:
    def test_skips_rakuten_when_app_id_missing(self):
        result = search_product("ネックレス", env={})
        assert result["rakuten"] == []
        assert "RAKUTEN_APP_ID" in result["rakuten_error"]

    def test_flags_amazon_tag_missing(self):
        result = search_product("ネックレス", env={})
        assert result.get("amazon_tag_missing") is True
        assert "tag=" not in result["amazon_search_url"]

    def test_skips_rakuten_when_access_key_missing(self):
        result = search_product("ネックレス", env={"RAKUTEN_APP_ID": "dummy-app-id"})
        assert result["rakuten"] == []
        assert "RAKUTEN_ACCESS_KEY" in result["rakuten_error"]

    def test_builds_amazon_url_with_configured_tag(self):
        result = search_product("ネックレス", env={"AMAZON_ASSOCIATE_TAG": "mytag-22"})
        assert "tag=mytag-22" in result["amazon_search_url"]
        assert "amazon_tag_missing" not in result
