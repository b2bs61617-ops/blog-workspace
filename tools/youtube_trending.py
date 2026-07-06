"""YouTube Data API v3で日本の急上昇動画を取得するスクリプト。

chomoand.com新方針(TikTok/YouTube発バズインフルエンサーのwiki記事)のための
「旬な人物発見」の情報源。docs/chomoand-pivot.md参照。

事前準備(初回のみ):
  1. Google Cloud Consoleでプロジェクトを作成(または既存プロジェクトを流用)
  2. 「APIとサービス」→「ライブラリ」で「YouTube Data API v3」を有効化
  3. 「認証情報」→「認証情報を作成」→「APIキー」で発行
     (制限を「YouTube Data API v3」のみに絞ると安全)
  4. .envに YOUTUBE_API_KEY を設定する

実行:
  python tools/youtube_trending.py
  python tools/youtube_trending.py --max 50
"""
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path
from collections import Counter

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
API_URL = "https://www.googleapis.com/youtube/v3/videos"


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


def fetch_trending(api_key, region="JP", max_results=50):
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region,
        "maxResults": str(max_results),
        "key": api_key,
    }
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=15) as r:
        data = json.loads(r.read())
    if "error" in data:
        raise RuntimeError(data["error"].get("message", str(data["error"])))
    return data.get("items", [])


def summarize(items):
    channel_counts = Counter(item["snippet"]["channelTitle"] for item in items)
    rows = []
    for item in items:
        rows.append({
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "views": int(item["statistics"].get("viewCount", 0)),
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "channel_video_count": channel_counts[item["snippet"]["channelTitle"]],
        })
    return rows


if __name__ == "__main__":
    env = load_env(ROOT / ".env")
    api_key = env.get("YOUTUBE_API_KEY")
    if not api_key:
        print("エラー: .envにYOUTUBE_API_KEYが設定されてないワン")
        sys.exit(1)

    max_results = 50
    if "--max" in sys.argv:
        idx = sys.argv.index("--max")
        max_results = int(sys.argv[idx + 1])

    items = fetch_trending(api_key, max_results=max_results)
    rows = summarize(items)

    print(f"# 日本の急上昇動画 上位{len(rows)}件\n")
    for i, row in enumerate(rows, 1):
        flag = f"(同チャンネル{row['channel_video_count']}本ランクイン)" if row["channel_video_count"] > 1 else ""
        print(f"{i}. [{row['channel']}] {row['title']} — 再生数{row['views']:,} {flag}")
        print(f"   {row['url']}")
