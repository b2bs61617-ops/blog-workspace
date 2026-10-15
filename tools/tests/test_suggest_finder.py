from suggest_finder import build_queries, classify_domain, judge, normalize, suffix_of, title_match


def test_normalize_absorbs_kana_width_case_and_spaces():
    assert normalize("まつく ＡＢＣ") == normalize("マツクabc")


def test_build_queries_covers_blank_kana_and_alphabet():
    q = build_queries("松倉海斗")
    assert q[0] == "松倉海斗 "
    assert "松倉海斗 あ" in q and "松倉海斗 ん" in q and "松倉海斗 z" in q
    assert len(q) == 1 + 46 + 26


def test_suffix_of_strips_name():
    assert suffix_of("松倉海斗 アクスタ 歴代", "松倉海斗") == "アクスタ 歴代"
    assert suffix_of("travis japan あだ名", "Travis Japan") == "あだ名"
    assert suffix_of("別人 アクスタ", "松倉海斗") == "別人 アクスタ"


def test_classify_domain():
    own = ["chomoand-4.blog"]
    assert classify_domain("https://chomoand-4.blog/x", own) == "own"
    assert classify_domain("https://ameblo.jp/foo/entry-1.html", own) == "blog"
    assert classify_domain("https://ja.wikipedia.org/wiki/x", own) == "strong"
    assert classify_domain("https://detail.chiebukuro.yahoo.co.jp/qa/q1", own) == "qa"
    assert classify_domain("https://www.instagram.com/x", own) == "sns"
    assert classify_domain("https://kamocafe.com/travis-name/", own) == "site"


def test_title_match_full_partial_none():
    assert title_match("松倉海斗のアクスタ歴代まとめ", "松倉海斗", "アクスタ 歴代") == "full"
    assert title_match("トラジャ アクスタ 歴代一覧", "松倉海斗", "アクスタ 歴代") == "partial"
    assert title_match("松倉海斗のプロフィール", "松倉海斗", "アクスタ") == "none"
    assert title_match("松倉海斗のあだ名", "松倉海斗", "アダ名") == "full"  # かなの違いは吸収


def _r(title, kind):
    return {"url": "https://example.com/" + title, "title": title, "kind": kind}


def test_judge_marks():
    name, suf = "松倉海斗", "あだ名"
    assert judge([_r("松倉海斗 プロフィール", "strong"), _r("質問", "qa")], name, suf)["mark"] == "◎"
    assert judge([_r("松倉海斗のあだ名", "site")], name, suf)["mark"] == "○"
    many = [_r("松倉海斗のあだ名まとめ", "blog")] * 2 + [_r("松倉海斗 あだ名", "strong")]
    assert judge(many, name, suf)["mark"] == "×"


def test_judge_reports_own_site_without_counting_it():
    res = judge([_r("松倉海斗のあだ名", "own")], "松倉海斗", "あだ名")
    assert res["mark"] == "◎" and res["own"]
