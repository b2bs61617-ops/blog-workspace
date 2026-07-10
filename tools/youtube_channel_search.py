"""YouTube Data API v3でキーワード検索し、該当するチャンネルの登録者数・開設日を一覧化するスクリプト。

女性筋トレ/フィットネス/ヨガ系YouTuberなど、特定ジャンルのチャンネルがどれくらい
存在するかを調べるためのリサーチ用ツール。tools/youtube_trending.py(急上昇動画ベース)
とは別系統で、こちらはキーワード検索(search.list, type=channel)ベース。

実行:
  python tools/youtube_channel_search.py "女性 筋トレ" "女性 フィットネス" "女性 ヨガ"
  python tools/youtube_channel_search.py "女性 筋トレ" --max 50
"""
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path
from collections import defaultdict

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"


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


def search_channels(api_key, keyword, region="JP", max_results=50):
    """1キーワードにつきsearch.list(type=channel)を必要回数呼び、channelIdのリストを返す。"""
    channel_ids = []
    page_token = None
    while len(channel_ids) < max_results:
        params = {
            "part": "snippet",
            "q": keyword,
            "type": "channel",
            "regionCode": region,
            "relevanceLanguage": "ja",
            "maxResults": str(min(50, max_results - len(channel_ids))),
            "key": api_key,
        }
        if page_token:
            params["pageToken"] = page_token
        url = f"{SEARCH_URL}?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read())
        if "error" in data:
            raise RuntimeError(data["error"].get("message", str(data["error"])))
        for item in data.get("items", []):
            channel_ids.append(item["snippet"]["channelId"])
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return channel_ids


def fetch_channel_details(api_key, channel_ids):
    """channelId -> {title, subscribers, published_at, video_count} のdictを返す。"""
    result = {}
    unique_ids = list(dict.fromkeys(channel_ids))
    for i in range(0, len(unique_ids), 50):
        batch = unique_ids[i:i + 50]
        params = {"part": "snippet,statistics", "id": ",".join(batch), "key": api_key}
        url = f"{CHANNELS_URL}?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read())
        if "error" in data:
            raise RuntimeError(data["error"].get("message", str(data["error"])))
        for ch in data.get("items", []):
            stats = ch["statistics"]
            result[ch["id"]] = {
                "title": ch["snippet"]["title"],
                "published_at": ch["snippet"]["publishedAt"][:10],
                "subscribers": None if stats.get("hiddenSubscriberCount") else int(stats.get("subscriberCount", 0)),
                "video_count": int(stats.get("videoCount", 0)),
            }
    return result


def format_subscribers(n):
    return "非公開" if n is None else f"{n:,}"


if __name__ == "__main__":
    env = load_env(ROOT / ".env")
    api_key = env.get("YOUTUBE_API_KEY")
    if not api_key:
        print("エラー: .envにYOUTUBE_API_KEYが設定されてないワン")
        sys.exit(1)

    max_results = 50
    args = sys.argv[1:]
    if "--max" in args:
        idx = args.index("--max")
        max_results = int(args[idx + 1])
        args = args[:idx] + args[idx + 2:]

    keywords = args or ["女性 筋トレ", "女性 フィットネス", "女性 ヨガ"]

    keyword_to_channel_ids = {}
    channel_to_keywords = defaultdict(list)
    for kw in keywords:
        ids = search_channels(api_key, kw, max_results=max_results)
        keyword_to_channel_ids[kw] = ids
        for cid in ids:
            channel_to_keywords[cid].append(kw)

    all_ids = [cid for ids in keyword_to_channel_ids.values() for cid in ids]
    details = fetch_channel_details(api_key, all_ids)

    print(f"# キーワード別ヒット数\n")
    for kw, ids in keyword_to_channel_ids.items():
        print(f"- 「{kw}」: {len(ids)}件")
    print(f"\n重複除いた総チャンネル数: {len(details)}件\n")

    rows = []
    for cid, kws in channel_to_keywords.items():
        d = details.get(cid)
        if not d:
            continue
        rows.append({
            "title": d["title"],
            "subscribers": d["subscribers"],
            "published_at": d["published_at"],
            "video_count": d["video_count"],
            "keywords": kws,
            "url": f"https://www.youtube.com/channel/{cid}",
        })

    rows.sort(key=lambda r: (r["subscribers"] is None, -(r["subscribers"] or 0)))

    print("# チャンネル一覧(登録者数降順)\n")
    print("| チャンネル名 | 登録者数 | 開設日 | 動画本数 | ヒットキーワード |")
    print("|---|---|---|---|---|")
    for r in rows:
        print(f"| [{r['title']}]({r['url']}) | {format_subscribers(r['subscribers'])} | {r['published_at']} | {r['video_count']:,} | {', '.join(r['keywords'])} |")
