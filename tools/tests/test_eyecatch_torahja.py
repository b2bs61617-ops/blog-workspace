from eyecatch_torahja import strip_group_name


def test_strips_bracketed_group_name():
    assert strip_group_name("【Travis Japan】ガンバ大阪にサインが飾られてる理由は?") == "ガンバ大阪にサインが飾られてる理由は?"


def test_strips_leading_group_with_particle():
    assert strip_group_name("トラジャの新曲はいつ?") == "新曲はいつ?"


def test_keeps_title_starting_with_particle_char():
    title = "はだかんぼうたちの見逃し配信はどこ？関西の放送時間も！"
    assert strip_group_name(title) == title
