from fix_youtube_embeds import fix_html, HOOK_CMD_RE

WRAPPED = ('<!-- wp:html -->\n<div style="position:relative;padding-top:56.25%;">'
           '<iframe src="https://www.youtube.com/embed/WBUHuDk_BFg" title="x" allowfullscreen></iframe></div>\n'
           '<!-- /wp:html -->')


def test_wrapped_block_becomes_wp_embed():
    new, n = fix_html("<p>a</p>\n\n" + WRAPPED + "\n\n<p>b</p>")
    assert n == 1
    assert "<iframe" not in new
    assert '<!-- wp:embed {"url":"https://www.youtube.com/watch?v=WBUHuDk_BFg"' in new
    assert new.startswith("<p>a</p>") and new.endswith("<p>b</p>")


def test_bare_iframe_gets_referrerpolicy():
    raw = '<div><p>x</p><iframe src="https://www.youtube.com/embed/abcdefghijk"></iframe></div>'
    new, n = fix_html(raw)
    assert n == 1
    assert 'referrerpolicy="strict-origin-when-cross-origin"' in new


def test_already_ok_untouched():
    raw = ('<iframe src="https://www.youtube.com/embed/abcdefghijk" referrerpolicy="strict-origin-when-cross-origin"></iframe>'
           '<iframe src="https://maps.google.com/maps?q=a&output=embed"></iframe>')
    assert fix_html(raw) == (raw, 0)


def test_wrapped_block_with_referrerpolicy_untouched():
    raw = WRAPPED.replace('allowfullscreen', 'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen')
    assert fix_html(raw) == (raw, 0)


def test_hook_command_filter():
    assert HOOK_CMD_RE.search("python3 build_and_post_x.py")
    assert HOOK_CMD_RE.search('cd a && python tools/_edit_1110.py --dry')
    assert not HOOK_CMD_RE.search("git status")
