"""LINE Messaging APIでのブロードキャスト通知送信スクリプト。

事前準備(初回のみ):
  1. .envに LINE_CHANNEL_ACCESS_TOKEN を設定する
  2. 通知を受け取りたい人全員がLINE公式アカウントを友だち追加する
     (以降、友だち追加した人全員に自動で届く。userIdの個別登録は不要)

通知送信:
  python tools/line_notify.py "記事を更新したワン"

他のスクリプトから使う場合:
  from tools.line_notify import notify
  notify("記事を更新したワン")
"""
import sys
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
API_BASE = "https://api.line.me/v2/bot"


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


def _request(url, token, data=None, method="GET"):
    headers = {"Authorization": f"Bearer {token}"}
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read()
        return json.loads(raw) if raw else {}


def get_follower_ids(token):
    """友だち追加済みユーザーのuserId一覧を取得する(初回セットアップ用)。"""
    return _request(f"{API_BASE}/followers/ids", token)


def send_message(token, user_id, text):
    """指定したuserIdにテキストメッセージをプッシュ送信する。"""
    data = {"to": user_id, "messages": [{"type": "text", "text": text}]}
    return _request(f"{API_BASE}/message/push", token, data=data, method="POST")


def broadcast_message(token, text):
    """公式アカウントを友だち追加している全員にテキストメッセージを送る。"""
    data = {"messages": [{"type": "text", "text": text}]}
    return _request(f"{API_BASE}/message/broadcast", token, data=data, method="POST")


def notify(text):
    """.envの設定を使って、友だち登録している全員にメッセージを送る共通関数。"""
    env = {**load_env(ROOT / ".env")}
    token = env.get("LINE_CHANNEL_ACCESS_TOKEN")
    if not token:
        print("LINE_CHANNEL_ACCESS_TOKEN が.envに未設定のため通知をスキップしたワン")
        return None
    return broadcast_message(token, text)


if __name__ == "__main__":
    env = load_env(ROOT / ".env")
    token = env.get("LINE_CHANNEL_ACCESS_TOKEN")
    if not token:
        print("エラー: .envにLINE_CHANNEL_ACCESS_TOKENが設定されてないワン")
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == "--get-user-id":
        result = get_follower_ids(token)
        user_ids = result.get("userIds", [])
        if not user_ids:
            print("フォロワーが見つからなかったワン。公式アカウントを友だち追加してから少し待って再実行してみてワン")
            print("(LINE側の反映に数分〜数日かかることがある)")
        else:
            print("見つかったuserId一覧ワン(1人だけなら先頭のIDを.envのLINE_USER_IDに設定してね):")
            for uid in user_ids:
                print(f"  {uid}")
    elif len(sys.argv) > 1:
        message = sys.argv[1]
        broadcast_message(token, message)
        print("送信したワン")
    else:
        print("使い方: python tools/line_notify.py \"メッセージ\"")
        print("      python tools/line_notify.py --get-user-id")
