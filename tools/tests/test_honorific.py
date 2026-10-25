from honorific import add_san, missing


def test_adds_san_to_full_name_and_surname():
    assert add_san("<p>目黒蓮が連絡。宮舘も驚いた。</p>", "snowman") == "<p>目黒蓮さんが連絡。宮舘さんも驚いた。</p>"


def test_full_name_not_double_counted():
    assert add_san("<p>宮舘涼太の役</p>", "snowman") == "<p>宮舘涼太さんの役</p>"


def test_keeps_links_quotes_tags_and_product_names():
    html = ('<p><a href="https://x/?p=80">目黒蓮はイケメン？</a>「目黒蓮すごい」目黒蓮特別版、めめ担、'
            '目黒蓮さん</p><img alt="目黒蓮">')
    assert add_san(html, "snowman") == html


def test_missing_reports_only_unprotected():
    assert len(missing('<p>阿部亮平と<a href="#">阿部亮平</a>「阿部亮平」</p>', "snowman")) == 1


def test_surname_only_within_group():
    assert add_san("<p>中村悠一</p>", "snowman") == "<p>中村悠一</p>"
