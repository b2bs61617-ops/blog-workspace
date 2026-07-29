"""STARTO ENTERTAINMENT(旧ジャニーズ)所属・出身タレントの公式YouTubeチャンネルを
定期的にチェックし、新着動画が出たらLINEに通知するツール。

chomoand-0(ジャニオタブログ)向け。タレント自身のYouTube動画には、視聴者(オタク)が
知りたいロケ地・ファッション・食べたものなどの情報が多く含まれるため、新着を早く
察知してリサーチ・記事化のきっかけにする狙い(2026-07-29導入)。

- 監視対象は channels.json(name, category, channel_id/handle/search_query)
- channel_id が未確定のチャンネルは初回実行時にYouTube Data APIで解決し、
  結果を channels.json に書き戻す(以降のAPI呼び出し節約)
- 新着判定は monitor_state.json(channel_id -> 最後に見た動画ID)で管理
- 現時点では検知・通知まで(記事化の自動起動はしない。x-trend-monitorと違い
  「ロケ地/ファッション特定」は人間の目利きが要るフェーズ1運用)

実行:
  python tools/youtube-talent-monitor/video_monitor.py            # 通常実行
  python tools/youtube-talent-monitor/video_monitor.py --dry-run  # 状態を書き換えず新着を表示するだけ
"""
import argparse
import json
import sys
import urllib.request
import urllib.parse
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent
REPO_ROOT = ROOT.parent.parent
CHANNELS_FILE = ROOT / "channels.json"
STATE_FILE = ROOT / "monitor_state.json"
REPORTS_DIR = ROOT / "reports"

CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
PLAYLIST_ITEMS_URL = "https://www.googleapis.com/youtube/v3/playlistItems"

MAX_VIDEOS_PER_CHANNEL = 5   # 1チャンネルあたり新着とみなす動画数の上限(見逃し対策の連続休止に配慮)
MAX_NOTIFY_LINES = 20        # LINE通知に載せる動画数の上限(超過分は件数のみ表示)

sys.path.insert(0, str(REPO_ROOT / "tools"))
from line_notify import notify  # noqa: E402


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


def load_channels():
    return json.loads(CHANNELS_FILE.read_text(encoding="utf-8"))


def save_channels(data):
    CHANNELS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _api_get(url, params):
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(full_url, timeout=15) as r:
        data = json.loads(r.read())
    if "error" in data:
        raise RuntimeError(data["error"].get("message", str(data["error"])))
    return data


def resolve_channel_id(api_key, entry):
    """entryのchannel_id/handle/search_queryからchannel_idを解決する。解決できなければNone。"""
    if entry.get("channel_id"):
        return entry["channel_id"]
    if entry.get("handle"):
        data = _api_get(CHANNELS_URL, {"part": "id", "forHandle": entry["handle"], "key": api_key})
        items = data.get("items", [])
        if items:
            return items[0]["id"]
    if entry.get("search_query"):
        data = _api_get(SEARCH_URL, {
            "part": "snippet", "q": entry["search_query"], "type": "channel",
            "maxResults": "1", "key": api_key,
        })
        items = data.get("items", [])
        if items:
            return items[0]["snippet"]["channelId"]
    return None


def fetch_uploads_playlist_ids(api_key, channel_ids):
    """channelId -> uploads再生リストID のdictを返す(channels.list part=contentDetails)。"""
    result = {}
    unique_ids = list(dict.fromkeys(channel_ids))
    for i in range(0, len(unique_ids), 50):
        batch = unique_ids[i:i + 50]
        data = _api_get(CHANNELS_URL, {"part": "contentDetails,snippet", "id": ",".join(batch), "key": api_key})
        for ch in data.get("items", []):
            result[ch["id"]] = {
                "uploads_playlist_id": ch["contentDetails"]["relatedPlaylists"]["uploads"],
                "channel_title": ch["snippet"]["title"],
            }
    return result


def fetch_latest_videos(api_key, playlist_id, max_results=MAX_VIDEOS_PER_CHANNEL):
    """再生リストの新しい順で最大max_results件の{video_id, title, published_at}を返す。"""
    data = _api_get(PLAYLIST_ITEMS_URL, {
        "part": "snippet", "playlistId": playlist_id, "maxResults": str(max_results), "key": api_key,
    })
    videos = []
    for item in data.get("items", []):
        sn = item["snippet"]
        videos.append({
            "video_id": sn["resourceId"]["videoId"],
            "title": sn["title"],
            "published_at": sn["publishedAt"],
        })
    return videos


def diff_new_videos(videos, last_seen_id):
    """再生リスト(新しい順)のうち、last_seen_idより新しい(=まだ見ていない)動画だけを返す。
    last_seen_idがNone(初回)の場合は最新1件だけを「新着」とし、いきなり大量通知しない。"""
    if last_seen_id is None:
        return videos[:1]
    new = []
    for v in videos:
        if v["video_id"] == last_seen_id:
            break
        new.append(v)
    return new


def format_notification(new_by_channel):
    """{channel_name: [video, ...]} からLINE通知本文を組み立てる(純粋関数)。"""
    lines = ["ジャニーズ系YouTubeに新着動画があるワン"]
    count = 0
    total = sum(len(vs) for vs in new_by_channel.values())
    for channel_name, videos in new_by_channel.items():
        for v in videos:
            if count >= MAX_NOTIFY_LINES:
                break
            lines.append(f"・[{channel_name}] {v['title']} https://youtu.be/{v['video_id']}")
            count += 1
        if count >= MAX_NOTIFY_LINES:
            break
    if total > MAX_NOTIFY_LINES:
        lines.append(f"…ほか{total - MAX_NOTIFY_LINES}件")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="状態を書き換えず新着を表示するだけ")
    args = parser.parse_args()

    env = load_env(REPO_ROOT / ".env")
    api_key = env.get("YOUTUBE_API_KEY")
    if not api_key:
        print("エラー: .envにYOUTUBE_API_KEYが設定されてないワン(docs/youtube-api-setup.md参照)")
        sys.exit(1)

    channels_data = load_channels()
    entries = channels_data["channels"]
    state = load_state()

    channels_dirty = False
    resolved_ids = []
    for entry in entries:
        cid = resolve_channel_id(api_key, entry)
        if not cid:
            print(f"未解決: {entry['name']}(handle/search_queryで見つからなかった)")
            continue
        if entry.get("channel_id") != cid:
            entry["channel_id"] = cid
            channels_dirty = True
        resolved_ids.append((entry["name"], entry["category"], cid))

    if channels_dirty and not args.dry_run:
        save_channels(channels_data)

    playlist_info = fetch_uploads_playlist_ids(api_key, [cid for _, _, cid in resolved_ids])

    new_by_channel = {}
    for name, category, cid in resolved_ids:
        info = playlist_info.get(cid)
        if not info:
            print(f"再生リスト取得失敗: {name}")
            continue
        try:
            videos = fetch_latest_videos(api_key, info["uploads_playlist_id"])
        except Exception as e:
            print(f"動画取得失敗: {name}: {type(e).__name__}: {e}")
            continue
        last_seen = state.get(cid)
        new_videos = diff_new_videos(videos, last_seen)
        if new_videos:
            new_by_channel[name] = new_videos
        if videos:
            state[cid] = videos[0]["video_id"]

    total_new = sum(len(v) for v in new_by_channel.values())
    print(f"チェック {len(resolved_ids)}チャンネル / 新着 {total_new}件")
    for name, videos in new_by_channel.items():
        for v in videos:
            print(f"  [{name}] {v['title']}")

    if args.dry_run:
        return

    save_state(state)

    if not new_by_channel:
        return

    REPORTS_DIR.mkdir(exist_ok=True)
    from datetime import datetime
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report_path = REPORTS_DIR / f"videos_{stamp}.json"
    report_path.write_text(json.dumps({
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "new_videos": new_by_channel,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    try:
        notify(format_notification(new_by_channel))
    except Exception as e:
        print(f"LINE通知に失敗(処理は続行): {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
