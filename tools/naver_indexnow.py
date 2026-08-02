"""IndexNowプロトコルで記事URLをNaverへ即時通知するスクリプト。

Naverは2023年7月からIndexNowプロトコル(Bing・Yandex等と共通の公開API)に
対応しており、Google Indexing APIのようなOAuth/サービスアカウントなしで
GETリクエスト1本でインデックス登録をリクエストできる。
ブラウザ操作(Naver Search Advisorへのログイン等)は一切不要。

事前準備(初回のみ、トモキ本人が実施): docs/naver-search-advisor-setup.md 参照。
要点は「キーを生成し、そのキーをファイル名にしたtxtファイル
(中身はキー文字列のみ)をサイトのドメイン直下に置く」の1回だけ。

実行:
  python tools/naver_indexnow.py https://chomoand-1.com/ko/xxxxx

他のスクリプトから使う場合:
  from tools.naver_indexnow import notify
  notify("https://chomoand-1.com/ko/xxxxx")
"""
import sys
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
INDEXNOW_URL = "https://searchadvisor.naver.com/indexnow"


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


def request_indexing(url, key):
    """IndexNowにURLを1件通知する(GETのみ、キー保有の証明はサイト直下のtxtファイルで行う)。"""
    params = urllib.parse.urlencode({"url": url, "key": key})
    req = urllib.request.Request(f"{INDEXNOW_URL}?{params}", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, r.read().decode("utf-8", errors="ignore")


def notify(url):
    """.envの設定を使ってインデックス登録をリクエストする共通関数。未設定なら何もせずNoneを返す。"""
    env = load_env(ROOT / ".env")
    key = env.get("NAVER_INDEXNOW_KEY")
    if not key:
        print("NAVER_INDEXNOW_KEY が.envに未設定のためNaverへの通知をスキップしたワン")
        return None
    status, body = request_indexing(url, key)
    return {"status": status, "body": body}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python tools/naver_indexnow.py <URL>")
        sys.exit(1)

    env = load_env(ROOT / ".env")
    key = env.get("NAVER_INDEXNOW_KEY")
    if not key:
        print("エラー: .envにNAVER_INDEXNOW_KEYが設定されてないワン")
        sys.exit(1)

    status, body = request_indexing(sys.argv[1], key)
    print(json.dumps({"status": status, "body": body}, ensure_ascii=False, indent=2))
