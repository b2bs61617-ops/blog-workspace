"""line_notify.py のテスト。

notify()は「.envにトークンが無ければ通知だけ黙ってスキップし、他の処理は止めない」という
CLAUDE.mdに明記された設計を担っている関数なので、その挙動自体を回帰させないために固定する。
実際の.envやネットワークには一切触れないよう、load_env/broadcast_messageは必ずモックする。
"""
from pathlib import Path

import line_notify


class TestLoadEnv:
    def test_parses_key_value_lines(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("LINE_CHANNEL_ACCESS_TOKEN=abc123\nLINE_USER_ID=uid1\n", encoding="utf-8")
        assert line_notify.load_env(env_file) == {
            "LINE_CHANNEL_ACCESS_TOKEN": "abc123",
            "LINE_USER_ID": "uid1",
        }

    def test_ignores_comments_and_blank_lines(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("# comment\n\nKEY=value\n", encoding="utf-8")
        assert line_notify.load_env(env_file) == {"KEY": "value"}

    def test_missing_file_returns_empty_dict(self, tmp_path):
        assert line_notify.load_env(tmp_path / "does_not_exist.env") == {}


class TestNotify:
    def test_skips_silently_when_token_missing(self, monkeypatch):
        monkeypatch.setattr(line_notify, "load_env", lambda path: {})
        called = {}

        def fake_broadcast(token, text):
            called["called"] = True

        monkeypatch.setattr(line_notify, "broadcast_message", fake_broadcast)

        result = line_notify.notify("テスト通知")

        assert result is None
        assert "called" not in called

    def test_broadcasts_when_token_present(self, monkeypatch):
        monkeypatch.setattr(line_notify, "load_env", lambda path: {"LINE_CHANNEL_ACCESS_TOKEN": "dummy-token"})
        captured = {}

        def fake_broadcast(token, text):
            captured["token"] = token
            captured["text"] = text
            return {"ok": True}

        monkeypatch.setattr(line_notify, "broadcast_message", fake_broadcast)

        result = line_notify.notify("テスト通知")

        assert result == {"ok": True}
        assert captured == {"token": "dummy-token", "text": "テスト通知"}
