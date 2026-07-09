"""google_indexing.py(記事公開時のGoogleインデックス即時登録)のテスト。

実際のAPI通信(request_indexing)はサービスアカウント認証が絡み
モックが重いので対象外にし、リクエストボディ組み立ての純粋関数のみを見る。
"""
from google_indexing import build_notification_body


class TestBuildNotificationBody:
    def test_default_type_is_url_updated(self):
        assert build_notification_body("https://chomoand.com/?p=123") == {
            "url": "https://chomoand.com/?p=123",
            "type": "URL_UPDATED",
        }

    def test_custom_notification_type(self):
        body = build_notification_body("https://chomoand.com/?p=123", "URL_DELETED")
        assert body["type"] == "URL_DELETED"
