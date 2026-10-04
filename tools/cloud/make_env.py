"""Build .env (and google-indexing-key.json) from environment variables.

Claude Code on the web (cloud sessions) cannot read the Google Drive .env, so the
secrets are registered as environment variables in the cloud environment settings.
Our tools read the .env file directly, so this script writes it out at session start.

Usage: python3 tools/cloud/make_env.py
"""
import base64
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PREFIXES = (
    "WP_", "BUFFER_", "RAKUTEN_", "AMAZON_", "GEMINI_", "LINE_",
    "NAVER_", "X_TREND_", "X_AUDITION_", "X_KOIKEYS_", "YOUTUBE_",
)


def main():
    lines = []
    for key in sorted(os.environ):
        if key.startswith(PREFIXES) and os.environ[key].strip():
            lines.append(f"{key}={os.environ[key].strip()}")

    # Service account JSON is passed as base64 to avoid newline issues in the env settings UI.
    key_b64 = os.environ.get("GOOGLE_INDEXING_KEY_B64", "").strip()
    if key_b64:
        key_path = ROOT / "google-indexing-key.json"
        key_path.write_bytes(base64.b64decode(key_b64))
        lines.append(f"GOOGLE_INDEXING_CREDENTIALS_PATH={key_path}")

    if not lines:
        print("[cloud] 環境変数に秘密情報が1つも無いワン。クラウド環境の設定で登録してワン")
        return

    (ROOT / ".env").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[cloud] .env を生成したワン ({len(lines)}項目)")


if __name__ == "__main__":
    main()
