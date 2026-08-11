"""tools/shorts/(clip_downloader.py・video_maker.py)のURL判定・パス組み立て・
ffmpegコマンド組み立てロジックのテスト(実際のダウンロード・ffmpeg実行は対象外)。
"""
from pathlib import Path

from clip_downloader import detect_source, next_clip_path
from video_maker import (
    build_drawtext_filter,
    build_ffmpeg_command,
    clamp_duration,
    escape_drawtext,
    vertical_scale_pad_filter,
)


class TestDetectSource:
    def test_x_dot_com(self):
        assert detect_source("https://x.com/someuser/status/12345") == "x"

    def test_twitter_dot_com(self):
        assert detect_source("https://twitter.com/someuser/status/12345") == "x"

    def test_instagram(self):
        assert detect_source("https://www.instagram.com/p/abc123/") == "instagram"

    def test_unknown(self):
        assert detect_source("https://example.com/video/1") == "unknown"


class TestNextClipPath:
    def test_first_clip_when_dir_missing(self, tmp_path):
        result = next_clip_path(tmp_path, "some_slug")
        assert result == tmp_path / "some_slug" / "clip_01.mp4"

    def test_skips_existing_numbers(self, tmp_path):
        target = tmp_path / "some_slug"
        target.mkdir()
        (target / "clip_01.mp4").touch()
        (target / "clip_02.mp4").touch()
        result = next_clip_path(tmp_path, "some_slug")
        assert result == target / "clip_03.mp4"

    def test_fills_gap(self, tmp_path):
        target = tmp_path / "some_slug"
        target.mkdir()
        (target / "clip_01.mp4").touch()
        (target / "clip_03.mp4").touch()
        result = next_clip_path(tmp_path, "some_slug")
        assert result == target / "clip_02.mp4"


class TestEscapeDrawtext:
    def test_escapes_colon(self):
        assert escape_drawtext("これマジ:?") == "これマジ\\:?"

    def test_escapes_backslash_before_others(self):
        assert escape_drawtext("a\\b:c") == "a\\\\b\\:c"

    def test_replaces_single_quote_with_fullwidth(self):
        assert escape_drawtext("it's here") == "it’s here"

    def test_escapes_percent(self):
        assert escape_drawtext("100%本物") == "100\\%本物"


class TestVerticalScalePadFilter:
    def test_default_is_9_16(self):
        f = vertical_scale_pad_filter()
        assert "scale=1080:1920" in f
        assert "pad=1080:1920" in f

    def test_custom_size(self):
        f = vertical_scale_pad_filter(540, 960)
        assert "scale=540:960" in f


class TestBuildDrawtextFilter:
    def test_includes_escaped_text(self):
        f = build_drawtext_filter("これ気になった:人", Path("font.ttf"))
        assert "text='これ気になった\\:人'" in f
        assert f.startswith("drawtext=")

    def test_box_can_be_disabled(self):
        f = build_drawtext_filter("hi", Path("font.ttf"), box=False)
        assert "box=1" not in f


class TestClampDuration:
    def test_shorter_than_max_stays_same(self):
        assert clamp_duration(30, max_seconds=60) == 30

    def test_longer_than_max_is_clamped(self):
        assert clamp_duration(90, max_seconds=60) == 60


class TestBuildFfmpegCommand:
    def test_raises_on_empty_clips(self):
        try:
            build_ffmpeg_command([], Path("out.mp4"), "text")
            assert False, "ValueErrorが出るはず"
        except ValueError:
            pass

    def test_single_clip_maps_acat_when_no_bgm(self):
        cmd = build_ffmpeg_command([Path("clip1.mp4")], Path("out.mp4"), "フック文")
        assert "-i" in cmd and str(Path("clip1.mp4")) in cmd
        assert "[acat]" in cmd
        joined = " ".join(cmd)
        assert "concat=n=1:v=1:a=1" in joined
        assert str(Path("out.mp4")) == cmd[-1]

    def test_multiple_clips_concat_count(self):
        cmd = build_ffmpeg_command(
            [Path("clip1.mp4"), Path("clip2.mp4")], Path("out.mp4"), "フック文"
        )
        joined = " ".join(cmd)
        assert "concat=n=2:v=1:a=1" in joined

    def test_bgm_adds_amix_and_extra_input(self):
        cmd = build_ffmpeg_command(
            [Path("clip1.mp4")], Path("out.mp4"), "フック文", bgm_path=Path("bgm.mp3")
        )
        joined = " ".join(cmd)
        assert str(Path("bgm.mp3")) in cmd
        assert "amix=inputs=2" in joined
        assert "[aout]" in cmd
