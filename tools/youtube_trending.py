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
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"
GROWING_THRESHOLD = 300_000  # この登録者数未満は「伸び盛り候補」として優先表示する


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


def is_excluded_channel(name):
    """YouTube自動生成の-Topicチャンネルや企業・公式チャンネルを除外する。"""
    if name.endswith("- Topic"):
        return True
    return "official" in name.lower() or "公式" in name


def fetch_trending(api_key, region="JP", max_results=50):
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region,
        "maxResults": str(max_results),
        "key": api_key,
    }
    url = f"{VIDEOS_URL}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=15) as r:
        data = json.loads(r.read())
    if "error" in data:
        raise RuntimeError(data["error"].get("message", str(data["error"])))
    return data.get("items", [])


def fetch_subscriber_counts(api_key, channel_ids):
    """channelId -> 登録者数(非公開ならNone) のdictを返す。一度に最大50件まで。"""
    result = {}
    unique_ids = list(dict.fromkeys(channel_ids))
    for i in range(0, len(unique_ids), 50):
        batch = unique_ids[i:i + 50]
        params = {"part": "statistics", "id": ",".join(batch), "key": api_key}
        url = f"{CHANNELS_URL}?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read())
        if "error" in data:
            raise RuntimeError(data["error"].get("message", str(data["error"])))
        for ch in data.get("items", []):
            stats = ch["statistics"]
            if stats.get("hiddenSubscriberCount"):
                result[ch["id"]] = None
            else:
                result[ch["id"]] = int(stats.get("subscriberCount", 0))
    return result


def summarize(items, subscriber_counts):
    channel_counts = Counter(item["snippet"]["channelTitle"] for item in items)
    rows = []
    for item in items:
        channel_id = item["snippet"]["channelId"]
        rows.append({
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "views": int(item["statistics"].get("viewCount", 0)),
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "channel_video_count": channel_counts[item["snippet"]["channelTitle"]],
            "subscribers": subscriber_counts.get(channel_id),
        })
    return rows


def format_subscribers(n):
    return "非公開" if n is None else f"{n:,}"


def print_row(i, row):
    flag = f"(同チャンネル{row['channel_video_count']}本ランクイン)" if row["channel_video_count"] > 1 else ""
    print(f"{i}. [{row['channel']}] 登録者数{format_subscribers(row['subscribers'])} — {row['title']} — 再生数{row['views']:,} {flag}")
    print(f"   {row['url']}")


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
    items = [item for item in items if not is_excluded_channel(item["snippet"]["channelTitle"])]
    channel_ids = [item["snippet"]["channelId"] for item in items]
    subscriber_counts = fetch_subscriber_counts(api_key, channel_ids)
    rows = summarize(items, subscriber_counts)

    growing_idx = {
        i for i, r in enumerate(rows)
        if r["subscribers"] is not None and r["subscribers"] < GROWING_THRESHOLD
    }
    growing = sorted((rows[i] for i in growing_idx), key=lambda r: r["subscribers"])
    others = [r for i, r in enumerate(rows) if i not in growing_idx]

    print(f"# 日本の急上昇動画 上位{len(rows)}件\n")

    if growing:
        print(f"## 伸び盛り候補(登録者数{GROWING_THRESHOLD:,}人未満・登録者数が少ない順)\n")
        for i, row in enumerate(growing, 1):
            print_row(i, row)
        print()

    print("## その他(急上昇順)\n")
    for i, row in enumerate(others, 1):
        print_row(i, row)
