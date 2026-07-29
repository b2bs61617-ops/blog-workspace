"""tools/youtube-talent-monitor/visual_analysis.py の純粋関数のテスト。"""
from visual_analysis import compute_timestamps, build_vision_prompt


class TestComputeTimestamps:
    def test_returns_empty_for_zero_duration(self):
        assert compute_timestamps(0) == []

    def test_returns_empty_for_zero_count(self):
        assert compute_timestamps(600, count=0) == []

    def test_single_frame_uses_midpoint_of_range(self):
        ts = compute_timestamps(1000, count=1, min_frac=0.1, max_frac=0.9)
        assert ts == [500.0]

    def test_frames_stay_within_min_max_fraction(self):
        ts = compute_timestamps(1000, count=5, min_frac=0.1, max_frac=0.9)
        assert ts[0] == 100.0
        assert ts[-1] == 900.0
        assert len(ts) == 5

    def test_frames_are_evenly_spaced(self):
        ts = compute_timestamps(1200, count=4, min_frac=0.0, max_frac=1.0)
        gaps = [round(ts[i + 1] - ts[i], 3) for i in range(len(ts) - 1)]
        assert len(set(gaps)) == 1

    def test_default_excludes_opening_and_ending(self):
        # デフォルトはmin_frac=0.05, max_frac=0.95なので冒頭・末尾ちょうどは含まれない
        ts = compute_timestamps(1000)
        assert ts[0] == 50.0
        assert ts[-1] == 950.0


class TestBuildVisionPrompt:
    def test_includes_title_and_count(self):
        prompt = build_vision_prompt("木村拓哉の築地散歩", 12)
        assert "木村拓哉の築地散歩" in prompt
        assert "12枚" in prompt

    def test_includes_analysis_categories(self):
        prompt = build_vision_prompt("テスト動画", 5)
        assert "服装" in prompt
        assert "アクセサリー" in prompt
        assert "ロケーション" in prompt
