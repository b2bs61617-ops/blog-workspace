def test_shape_ng_when_assistant_name_in_body():
    import fact_check
    body = "<!-- wp:paragraph --><p>マツの予想では2%です。</p><!-- /wp:paragraph --><h2>x</h2>"
    ng, _ = fact_check.check_shape(body, min_chars=0)
    assert any("マツ" in x for x in ng)
    ok = "<!-- wp:paragraph --><p>マツダスタジアムとマツコの番組。</p><!-- /wp:paragraph --><h2>x</h2>"
    ng, _ = fact_check.check_shape(ok, min_chars=0)
    assert not any("マツ" in x for x in ng)
