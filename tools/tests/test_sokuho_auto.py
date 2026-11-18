# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "neta_watch"))
import sokuho_auto as s  # noqa: E402


def test_fix_title_keeps_english_spaces():
    assert s.fix_title("前田真剣佑が初主演! SIDE by SIDE の放送日は?") == "前田真剣佑が初主演！SIDE by SIDEの放送日は？"


def test_title_ok():
    assert s.title_ok("小嶋陽菜が結婚！")
    assert not s.title_ok("小嶋陽菜が結婚")
    assert not s.title_ok("あ" * 35 + "？")


def test_heavy_words():
    assert s.heavy_by_words("俳優が逮捕", None) == ["逮捕"]
    assert s.heavy_by_words("ドラマ主演が決定") == []


def test_is_major():
    assert s.is_major("https://www.nikkansports.com/entertainment/news/1.html")
    assert s.is_major("https://news.yahoo.co.jp/articles/abc")
    assert not s.is_major("https://example-matome.com/nikkansports.com")


def test_clean_slug_and_split():
    assert s.clean_slug("Kojima Haruna!!", "k").startswith("kojima-haruna-")
    assert s.split_sentences("一文目。二文目！三文目") == ["一文目。", "二文目！", "三文目"]


def test_pick_images_only_news_accounts():
    story = {"posts": [{"handle": "fan123", "id": "1", "images": ["https://pbs.twimg.com/media/a.jpg"]},
                       {"handle": "nikkansports", "id": "2", "images": ["https://pbs.twimg.com/media/b.jpg?name=small"]}]}
    got = s.pick_images(story)
    assert got == [("https://pbs.twimg.com/media/b.jpg?name=large", "https://x.com/nikkansports/status/2")]
