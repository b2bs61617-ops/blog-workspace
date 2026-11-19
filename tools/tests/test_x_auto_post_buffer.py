"""x_auto_post_buffer.threads_text の単体テスト(Threadsは本文の最後にURLを載せる、2026-11-19〜)"""
import x_auto_post_buffer as xb


def test_threads_text_appends_label_and_url_at_end():
    out = xb.threads_text("本文\n\n#SnowMan", "https://chomoand-2.com/a/")
    assert out.startswith("本文\n\n#SnowMan")
    assert out.endswith(f"{xb.THREADS_LINK_LABEL}\nhttps://chomoand-2.com/a/")
    assert "答えはここをクリック" in out
