from easy_read import check, fix


def test_fix_kana_but_not_inside_words_or_quotes():
    src = "<p>殆ど出来る。仕事が忙しい。変更に注意。「素敵」と言った。</p>"
    out = fix(src)
    assert "ほとんどできる" in out
    assert "仕事が" in out and "変更に" in out
    assert "「素敵」" in out


def test_check_flags_long_sentence_and_wide_table():
    long = "あ" * 85 + "。"
    ng, _ = check(f"<p>{long}</p><table><tr><td>1</td><td>2</td><td>3</td><td>4</td></tr></table>")
    assert any("1文が長い" in x for x in ng)
    assert any("4列" in x for x in ng)


def test_check_ignores_quote_length_and_passes_short_text():
    ng, warn = check("<p>ファンは「" + "い" * 100 + "」と投稿。短い文です。</p>")
    assert ng == [] and warn == []


BOX = '<div style="border:1px"><p style="margin:0">&#10003;要点</p></div>'
REL = '<div style="border:1px"><p>あわせて読みたい</p><ul><li><a href="#">記事</a></li></ul></div>'


def test_summary_without_comment_is_ng():
    ng, _ = check(f"<h2>トークまとめ</h2><p>本文。</p><h2>まとめ</h2>{BOX}{REL}<p></p>")
    assert any("一言感想" in x for x in ng)


def test_summary_with_comment_passes():
    ng, _ = check(f"<h2>まとめ</h2>{BOX}<p>楽しみですね！</p>{REL}")
    assert not any("一言感想" in x for x in ng)


def test_no_summary_heading_is_not_checked():
    ng, _ = check("<h2>見出し</h2><p>本文です。</p>")
    assert not any("一言感想" in x for x in ng)
