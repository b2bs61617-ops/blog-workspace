"""Google Indexing APIで記事URLの即時インデックス登録をリクエストするスクリプト。

記事公開時にWordPressの投稿URLをGoogleへ即時通知し、
インデックス登録を早める(publishスキルから呼ばれる)。

事前準備(初回のみ、トモキ本人が実施): docs/google-indexing-setup.md 参照。

実行:
  python tools/google_indexing.py https://chomoand.com/?p=123

他のスクリプトから使う場合:
  from tools.google_indexing import request_indexing
  request_indexing("https://chomoand.com/?p=123")
"""
import sys
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
INDEXING_SCOPE = "https://www.googleapis.com/auth/indexing"
INDEXING_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def build_notification_body(url, notification_type="URL_UPDATED"):
    """Indexing APIに送るリクエストボディを組み立てる。"""
    return {"url": url, "type": notification_type}


def request_indexing(url, credentials_path, notification_type="URL_UPDATED"):
    """サービスアカウント認証でIndexing APIにURL通知を送る。"""
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession

    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=[INDEXING_SCOPE]
    )
    session = AuthorizedSession(creds)
    resp = session.post(INDEXING_URL, json=build_notification_body(url, notification_type))
    resp.raise_for_status()
    return resp.json()


def notify(url):
    """.envの設定を使ってインデックス登録をリクエストする共通関数。未設定なら何もせずNoneを返す。"""
    env = load_env(ROOT / ".env")
    credentials_path = env.get("GOOGLE_INDEXING_CREDENTIALS_PATH")
    # .env のパスが(別PC由来などで)見つからない場合は既定の置き場所も探す。
    candidates = [credentials_path] if credentials_path else []
    candidates += [
        str(ROOT / "google-indexing-key.json"),
        str(Path.home() / "google-indexing-key.json"),
    ]
    found = next((p for p in candidates if p and Path(p).exists()), None)
    if not found:
        if not credentials_path:
            print("GOOGLE_INDEXING_CREDENTIALS_PATH が.envに未設定のためインデックス登録をスキップしたワン")
        else:
            print(f"サービスアカウントキーが見つからないためインデックス登録をスキップしたワン: {credentials_path}")
        return None
    return request_indexing(url, found)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python tools/google_indexing.py <URL>")
        sys.exit(1)

    env = load_env(ROOT / ".env")
    credentials_path = env.get("GOOGLE_INDEXING_CREDENTIALS_PATH")
    if not credentials_path:
        print("エラー: .envにGOOGLE_INDEXING_CREDENTIALS_PATHが設定されてないワン")
        sys.exit(1)

    result = request_indexing(sys.argv[1], credentials_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
