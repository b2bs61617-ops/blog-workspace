"""eyecatch_chomoand の単体テスト(描画そのものではなく組み立て・フォールバックロジックを検証)."""

from pathlib import Path

from eyecatch_chomoand import BG_PATH, CANVAS_H, CANVAS_W, build_html, build_pollinations_url, resolve_background


def test_canvas_is_16_9():
    assert round(CANVAS_W / CANVAS_H, 3) == round(16 / 9, 3)


def test_texts_are_included():
    html = build_html(["wiki", "学歴"], "大島空凱", ["パデル日本代表の経歴", "双子を調査!"], hue=140)
    assert "wiki<br>学歴" in html
    assert "大島空凱" in html
    assert "パデル日本代表の経歴<br>双子を調査!" in html
    assert "hue-rotate(140deg)" in html


def test_top_and_bottom_are_optional():
    html = build_html([], "YUKI", [], hue=0)
    assert 'class="fit top"' not in html
    assert 'class="fit bottom"' not in html


def test_html_is_escaped():
    html = build_html([], "<script>alert(1)</script>", [], hue=0)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_bg_path_is_used_in_html():
    custom_bg = Path("C:/tmp/dummy_bg.png")
    html = build_html([], "テスト", [], hue=0, bg_path=custom_bg)
    assert custom_bg.as_uri() in html


def test_build_pollinations_url_includes_size_and_seed():
    url = build_pollinations_url(seed=42)
    assert "width=1200" in url
    assert "height=675" in url
    assert "seed=42" in url
    assert url.startswith("https://image.pollinations.ai/prompt/")


def test_resolve_background_returns_static_when_ai_disabled():
    bg_path, tmp_bg = resolve_background(use_ai=False)
    assert bg_path == BG_PATH
    assert tmp_bg is None


def test_resolve_background_falls_back_on_generation_error(monkeypatch):
    def raise_error(seed):
        raise RuntimeError("network error")

    monkeypatch.setattr("eyecatch_chomoand.generate_ai_background", raise_error)
    bg_path, tmp_bg = resolve_background(use_ai=True)
    assert bg_path == BG_PATH
    assert tmp_bg is None


def test_resolve_background_returns_tmp_file_on_success(monkeypatch, tmp_path):
    monkeypatch.setattr("eyecatch_chomoand.generate_ai_background", lambda seed: b"fake-image-bytes")
    bg_path, tmp_bg = resolve_background(use_ai=True, seed=1)
    try:
        assert bg_path == tmp_bg
        assert tmp_bg.read_bytes() == b"fake-image-bytes"
    finally:
        tmp_bg.unlink(missing_ok=True)
