"""AdSenseの読み取り許可を1回だけ取得し、リフレッシュトークンを保存するスクリプト。

AdSense Management APIはサービスアカウント非対応のため、トモキのGoogleアカウントで
ブラウザの「許可」を1回押してもらい、その結果(トークン)をDriveに保存する。
以降は site_dashboard.py がこのトークンで自動的にAdSenseを読みに行く。

実行: python tools/site-dashboard/adsense_auth.py
"""
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

DRIVE_DIR = Path(r"G:\マイドライブ\ブログ関係")
CLIENT_FILE = DRIVE_DIR / "adsense-oauth.json"
TOKEN_FILE = DRIVE_DIR / "adsense-token.json"
SCOPES = ["https://www.googleapis.com/auth/adsense.readonly"]


def main():
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_FILE), SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    print(f"保存しました: {TOKEN_FILE}")


if __name__ == "__main__":
    main()
