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


def test_no_san_in_headings_tables_toc_and_summary():
    html = ('<h2 class="wp-block-heading">目黒蓮の役</h2>'
            '<figure class="wp-block-table"><table><tbody><tr><td>目黒蓮</td></tr></tbody></table></figure>'
            '<div style="x"><p>この記事でわかること</p><ul><li>目黒蓮の連絡</li></ul></div>'
            '<!-- wp:heading -->\n<h2 class="wp-block-heading">まとめ</h2>\n<!-- /wp:heading -->\n\n'
            '<!-- wp:html -->\n<div><p>目黒蓮が連絡</p></div>\n<!-- /wp:html -->'
            '<p>目黒蓮が連絡</p>')
    out = add_san(html, "snowman")
    assert out.count("目黒蓮さん") == 1 and out.endswith("<p>目黒蓮さんが連絡</p>")


def test_strips_san_already_in_no_san_blocks():
    assert add_san("<h3>阿部亮平さんの財布</h3>", "snowman") == "<h3>阿部亮平の財布</h3>"
