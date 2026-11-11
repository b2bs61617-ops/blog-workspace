import pytest

import affiliate_box as ab


def test_big_image_replaces_thumbnail_size():
    u = "https://thumbnail.image.rakuten.co.jp/@0_mall/x/a.jpg?_ex=128x128"
    assert ab.big_image(u).endswith("_ex=400x400")
    assert ab.big_image("https://x/a.jpg").endswith("?_ex=400x400")
    assert ab.big_image(None) is None


def test_looks_bad_flags_furusato():
    assert ab.looks_bad("【ふるさと納税】象印 炊飯器")
    assert not ab.looks_bad("象印 炎舞炊き NX-AB10-BZ")


def test_build_box_has_sponsored_links_and_image():
    h = ab.build_box("https://r/x?a=1&b=2", "https://img/a.jpg", "商品<名>", "https://amzn/s?k=x", note="黒", border="#f00")
    assert h.startswith("<!-- wp:html -->") and h.endswith("<!-- /wp:html -->")
    assert h.count('rel="nofollow sponsored noopener"') == 3
    assert "楽天で見る" in h and "Amazonで見る" in h
    assert "&amp;b=2" in h and "商品&lt;名&gt;" in h
    assert "max-width:100%" in h and "border:1px solid #f00" in h


def test_build_box_amazon_only_and_requires_a_link():
    h = ab.build_box(None, None, "x", "https://amzn/s?k=x")
    assert "楽天で見る" not in h and "Amazonで見る" in h and "<img" not in h
    with pytest.raises(ValueError):
        ab.build_box(None, None, "x", None)
