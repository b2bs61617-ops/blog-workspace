import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from sitemap_watch import domain_of, judge_site  # noqa: E402

NOW = datetime.datetime(2026, 11, 19, tzinfo=datetime.timezone.utc)


def test_domain_of():
    assert domain_of("sc-domain:chomoand.com") == "chomoand.com"
    assert domain_of("https://chomoand-4.blog/") == "chomoand-4.blog"


def test_ok():
    maps = [{"path": "https://a.com/sitemap.xml", "lastDownloaded": "2026-11-18T00:00:00Z", "errors": "0", "warnings": "0"}]
    assert judge_site(maps, NOW) == []


def test_unregistered():
    assert judge_site([], NOW) == ["Search Consoleにサイトマップが未登録"]


def test_errors_and_stale():
    maps = [{"path": "https://a.com/sitemap.xml", "lastDownloaded": "2026-10-01T00:00:00Z", "errors": "2", "warnings": "0"}]
    p = judge_site(maps, NOW)
    assert any("エラー2件" in x for x in p)
    assert any("49日読みに来ていない" in x for x in p)


def test_pending_just_submitted_is_ok():
    maps = [{"path": "https://a.com/sitemap.xml", "lastSubmitted": "2026-11-19T00:00:00Z", "isPending": True, "errors": "0"}]
    assert judge_site(maps, NOW) == []


def test_sitemap_down():
    maps = [{"path": "https://a.com/sitemap.xml", "lastDownloaded": "2026-11-18T00:00:00Z"}]
    assert judge_site(maps, NOW, sitemap_status=404) == ["sitemap.xmlが開けない(HTTP 404)"]
