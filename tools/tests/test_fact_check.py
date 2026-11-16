def test_shape_ng_when_assistant_name_in_body():
    import fact_check
    body = "<!-- wp:paragraph --><p>マツの予想では2%です。</p><!-- /wp:paragraph --><h2>x</h2>"
    ng, _ = fact_check.check_shape(body, min_chars=0)
    assert any("マツ" in x for x in ng)
    ok = "<!-- wp:paragraph --><p>マツダスタジアムとマツコの番組。</p><!-- /wp:paragraph --><h2>x</h2>"
    ng, _ = fact_check.check_shape(ok, min_chars=0)
    assert not any("マツ" in x for x in ng)


def test_shape_ng_when_group_name_has_san():
    import fact_check
    body = "<!-- wp:paragraph --><p>Aぇ! groupさんは4回でした。</p><!-- /wp:paragraph --><h2>x</h2>"
    ng, _ = fact_check.check_shape(body, min_chars=0)
    assert any("グループ名" in x for x in ng)


def test_shape_ng_when_no_photo():
    import fact_check
    body = "<!-- wp:paragraph --><p>本文。</p><!-- /wp:paragraph --><h2>x</h2>"
    ng, _ = fact_check.check_shape(body, min_chars=0)
    assert any("[写真]" in x for x in ng)
    ng, _ = fact_check.check_shape(body + '<img src="https://example.com/a.jpg">', min_chars=0)
    assert not any("[写真]" in x for x in ng)
