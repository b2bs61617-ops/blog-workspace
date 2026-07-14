"""eyecatch_koikeyz.build_html の単体テスト(描画そのものではなく組み立てロジックを検証)."""

from eyecatch_koikeyz import CANVAS_H, CANVAS_W, build_html


def test_canvas_is_16_9():
    assert round(CANVAS_W / CANVAS_H, 3) == round(16 / 9, 3)


def test_texts_are_included():
    html = build_html("運営の愛?", "KO1KEYZ", ["「!」はなぜ12個?", "誕生日投稿でのこだわりも!"], seed=1)
    assert "運営の愛?" in html
    assert "KO1KEYZ" in html
    assert "「!」はなぜ12個?<br>誕生日投稿でのこだわりも!" in html


def test_top_and_bottom_are_optional():
    html = build_html("", "YUKI", [], seed=1)
    assert 'class="fit top"' not in html
    assert 'class="fit bottom"' not in html
    assert "YUKI" in html


def test_html_is_escaped():
    html = build_html("", "<script>alert(1)</script>", [], seed=1)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_same_seed_is_reproducible():
    a = build_html("上", "KO1KEYZ", ["下"], seed=42)
    b = build_html("上", "KO1KEYZ", ["下"], seed=42)
    assert a == b


def test_different_seed_changes_background_only():
    a = build_html("上", "KO1KEYZ", ["下"], seed=1)
    b = build_html("上", "KO1KEYZ", ["下"], seed=2)
    assert a != b  # 背景スモークの位置が変わる
