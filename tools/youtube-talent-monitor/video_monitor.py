"""STARTO ENTERTAINMENT(旧ジャニーズ)所属・出身タレントの公式YouTubeチャンネルを
定期的にチェックし、新着動画が出たら文字起こしを添えてLINEに通知するツール。

chomoand-0(ジャニオタブログ)向け。タレント自身のYouTube動画には、視聴者(オタク)が
知りたいロケ地・ファッション・食べたものなどの情報が多く含まれるため、新着を早く
察知してリサーチ・記事化のきっかけにする狙い(2026-07-29導入)。

新着検知はYouTube Data APIを使わず、チャンネルごとの公開RSSフィード
(https://www.youtube.com/feeds/videos.xml?channel_id=...)を使う(APIキー不要・無料枠の
心配がない)。文字起こしはリポジトリ直下の youtube_transcript.py(youtube-transcript-api、
sns-research/youtube-transcriptスキルと共通)をそのまま再利用する。

- 監視対象は channels.json(name, category, channel_id)。channel_idがnullの項目は
  ハンドルが確認できていないので自動ではスキップする(手動で埋めてから対象に入れる)
- 新着判定は monitor_state.json(channel_id -> 最後に見た動画ID)で管理
- 現時点では検知・通知・文字起こし保存まで(ロケ地/ファッション特定そのものは
  まだ自動化していない。reports/配下のJSONを見て人間かAIが確認するフェーズ1運用)

実行:
  python tools/youtube-talent-monitor/video_monitor.py            # 通常実行
  python tools/youtube-talent-monitor/video_monitor.py --dry-run  # 状態を書き換えず新着を表示するだけ
  python tools/youtube-talent-monitor/video_monitor.py --no-transcript  # 文字起こしを取得しない(速報のみ)
"""
import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent
REPO_ROOT = ROOT.parent.parent
CHANNELS_FILE = ROOT / "channels.json"
STATE_FILE = ROOT / "monitor_state.json"
REPORTS_DIR = ROOT / "reports"

FEED_URL = "https://www.youtube.com/feeds/videos.xml"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}

MAX_NOTIFY_LINES = 20        # LINE通知に載せる動画数の上限(超過分は件数のみ表示)
MAX_TRANSCRIPT_CHARS = 4000  # レポートに保存する文字起こしの上限(肥大化防止)

sys.path.insert(0, str(REPO_ROOT / "tools"))
sys.path.insert(0, str(REPO_ROOT))
from line_notify import notify  # noqa: E402


def load_channels():
    return json.loads(CHANNELS_FILE.read_text(encoding="utf-8"))


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_feed_xml(xml_text):
    """RSSフィード(Atom)のXMLテキストから[{video_id, title, published_at}, ...]を
    新しい順(フィード本来の順)のまま返す(純粋関数)。"""
    root = ET.fromstring(xml_text)
    videos = []
    for entry in root.findall("atom:entry", ATOM_NS):
        video_id = entry.findtext("yt:videoId", namespaces=ATOM_NS)
        title = entry.findtext("atom:title", namespaces=ATOM_NS)
        published = entry.findtext("atom:published", namespaces=ATOM_NS)
        if video_id:
            videos.append({"video_id": video_id, "title": title, "published_at": published})
    return videos


def fetch_channel_videos(channel_id):
    url = f"{FEED_URL}?channel_id={channel_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        xml_text = r.read().decode("utf-8")
    return parse_feed_xml(xml_text)


def diff_new_videos(videos, last_seen_id):
    """フィード(新しい順)のうち、last_seen_idより新しい(=まだ見ていない)動画だけを返す。
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


def fetch_transcript_safe(video_id):
    """文字起こしをベストエフォートで取得する。字幕が無い等で失敗したらNone(呼び出し側で通知は止めない)。
    youtube_transcript.py はimport時にsys.stdoutをUTF-8ラップし直す副作用があるため、
    pytest収集時に壊れないようここで遅延importする。"""
    try:
        from youtube_transcript import get_transcript
        text = get_transcript(video_id)
        return text[:MAX_TRANSCRIPT_CHARS] if text else None
    except Exception as e:
        print(f"  文字起こし取得失敗({video_id}): {type(e).__name__}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="状態を書き換えず新着を表示するだけ")
    parser.add_argument("--no-transcript", action="store_true", help="文字起こしを取得しない(速報のみ)")
    args = parser.parse_args()

    channels_data = load_channels()
    entries = [c for c in channels_data["channels"] if c.get("channel_id")]
    skipped = [c["name"] for c in channels_data["channels"] if not c.get("channel_id")]
    if skipped:
        print(f"channel_id未確定でスキップ: {', '.join(skipped)}")

    state = load_state()
    new_by_channel = {}

    for entry in entries:
        name, cid = entry["name"], entry["channel_id"]
        try:
            videos = fetch_channel_videos(cid)
        except Exception as e:
            print(f"取得失敗: {name}: {type(e).__name__}: {e}")
            continue
        last_seen = state.get(cid)
        new_videos = diff_new_videos(videos, last_seen)
        if new_videos:
            new_by_channel[name] = new_videos
        if videos:
            state[cid] = videos[0]["video_id"]

    total_new = sum(len(v) for v in new_by_channel.values())
    print(f"チェック {len(entries)}チャンネル / 新着 {total_new}件")
    for name, videos in new_by_channel.items():
        for v in videos:
            print(f"  [{name}] {v['title']}")

    if args.dry_run:
        return

    save_state(state)

    if not new_by_channel:
        return

    if not args.no_transcript:
        for name, videos in new_by_channel.items():
            for v in videos:
                v["transcript"] = fetch_transcript_safe(v["video_id"])

    REPORTS_DIR.mkdir(exist_ok=True)
    from datetime import datetime
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report_path = REPORTS_DIR / f"videos_{stamp}.json"
    report_path.write_text(json.dumps({
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "new_videos": new_by_channel,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"レポート出力: {report_path}")

    try:
        notify(format_notification(new_by_channel))
    except Exception as e:
        print(f"LINE通知に失敗(処理は続行): {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
