"""KO1KEYZ(コイキーズ)関連の公式YouTubeチャンネルを定期的にチェックし、
新着動画が出たら文字起こしを添えてLINEに通知するツール。

chomoand-1(コイキーズブログ)向け。tools/youtube-talent-monitor/(chomoand-0向け)と
同じ設計を流用している(2026-07-30導入)。新着動画には視聴者(KO1LY)が知りたい
ロケ地・ファッション・食べたものなどの情報が多く含まれるため、新着を早く察知して
リサーチ・記事化のきっかけにする狙い。

新着検知はYouTube Data APIを使わず、チャンネルごとの公開RSSフィード
(https://www.youtube.com/feeds/videos.xml?channel_id=...)を使う(APIキー不要・無料枠の
心配がない)。文字起こしはリポジトリ直下の youtube_transcript.py(youtube-transcript-api、
sns-research/youtube-transcriptスキルと共通)をそのまま再利用する。

服装・アクセサリー・訪問場所は文字起こしだけでは分からないため、visual_analysis.py
(同ディレクトリ)でフレーム画像を抽出しGemini Visionに解析させる。この処理は
Claude/マツを介さずスクリプト単体で完結する(日次の自動実行でClaude Codeのトークンを
消費しないようにするため、youtube-talent-monitorと同じ方針)。

- 監視対象は channels.json(name, category, channel_id)。メンバー12人は2026-07-30時点で
  デビュー前(2026-10-07デビュー予定)のため個人チャンネルが確認できず、公式2チャンネル
  (KO1KEYZ公式・PRODUCE 101 JAPAN公式)のみが対象。デビュー後に個人チャンネルが出来たら
  ここに追加すること。
- 新着判定は monitor_state.json(channel_id -> 最後に見た動画ID)で管理
- 検知・通知・文字起こし・画像解析まで自動化済み。ロケ地・私服の特定そのもの(記事執筆)は
  まだ自動化しておらず、reports/配下のJSON+frames/配下の画像を人間かAI(記事執筆時)が
  見て判断するフェーズ1.5運用(youtube-talent-monitorと同じ)

実行:
  python tools/koikeyz-youtube-monitor/video_monitor.py               # 通常実行
  python tools/koikeyz-youtube-monitor/video_monitor.py --dry-run     # 状態を書き換えず新着を表示するだけ
  python tools/koikeyz-youtube-monitor/video_monitor.py --no-transcript  # 文字起こしを取得しない(速報のみ)
  python tools/koikeyz-youtube-monitor/video_monitor.py --no-visuals  # 画像解析をしない(文字起こしのみ)
"""
import argparse
import json
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
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
FIRST_RUN_LOOKBACK_DAYS = 7  # 新規チャンネル初回チェック時、何日前までの動画を「新着」扱いにするか
RSS_RETRIES = 3              # RSSフィードが断続的に404/500を返すことがあるためのリトライ回数
RSS_RETRY_WAIT_SEC = 3       # リトライ間隔
CHANNEL_INTERVAL_SEC = 0.5   # チャンネル間の待機(連続アクセスによる一時的なブロックを避ける)

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


def fetch_channel_videos(channel_id, retries=RSS_RETRIES, retry_wait=RSS_RETRY_WAIT_SEC):
    """RSSフィードを取得してパースする。YouTube側が404/500を断続的に返すことがある
    (同じchannel_idでも数秒後に再試行すると成功する)ため、軽くリトライする。"""
    url = f"{FEED_URL}?channel_id={channel_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last_error = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                xml_text = r.read().decode("utf-8")
            return parse_feed_xml(xml_text)
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                time.sleep(retry_wait)
    raise last_error


def diff_new_videos(videos, last_seen_id, now=None):
    """フィード(新しい順)のうち、last_seen_idより新しい(=まだ見ていない)動画だけを返す。
    last_seen_idがNone(初回)の場合、「最新1件だけ」だと監視開始直前に投稿された動画を
    永久に見逃すため、初回はFIRST_RUN_LOOKBACK_DAYS日以内に投稿された分をまとめて
    「新着」として返す(該当が無い長期休止チャンネルは最新1件のみ)。"""
    if last_seen_id is None:
        now = now or datetime.now(timezone.utc)
        cutoff = now - timedelta(days=FIRST_RUN_LOOKBACK_DAYS)
        recent = []
        for v in videos:
            try:
                pub = datetime.fromisoformat(v["published_at"])
            except (KeyError, TypeError, ValueError):
                continue
            if pub >= cutoff:
                recent.append(v)
        return recent or videos[:1]
    new = []
    for v in videos:
        if v["video_id"] == last_seen_id:
            break
        new.append(v)
    return new


def format_notification(new_by_channel):
    """{channel_name: [video, ...]} からLINE通知本文を組み立てる(純粋関数)。"""
    lines = ["KO1KEYZ系YouTubeに新着動画があるワン"]
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


def analyze_visuals_safe(video_id, title):
    """visual_analysis.pyはimport時にcv2/yt_dlp等の重い依存を読み込むため、
    使うときだけ遅延importする(pytest収集やno-visuals時の起動を軽くする)。"""
    from visual_analysis import analyze_video_visuals
    return analyze_video_visuals(video_id, title)


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
    parser.add_argument("--no-visuals", action="store_true", help="画像解析(服装・アクセサリー・ロケ地)をしない")
    args = parser.parse_args()

    channels_data = load_channels()
    entries = [c for c in channels_data["channels"] if c.get("channel_id")]
    skipped = [c["name"] for c in channels_data["channels"] if not c.get("channel_id")]
    if skipped:
        print(f"channel_id未確定でスキップ: {', '.join(skipped)}")

    state = load_state()
    new_by_channel = {}

    for i, entry in enumerate(entries):
        name, cid = entry["name"], entry["channel_id"]
        if i > 0:
            time.sleep(CHANNEL_INTERVAL_SEC)
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

    if not args.no_visuals:
        for name, videos in new_by_channel.items():
            for v in videos:
                visual = analyze_visuals_safe(v["video_id"], v["title"])
                if visual:
                    v["visual_notes"] = visual["visual_notes"]
                    v["frame_paths"] = visual["frame_paths"]

    REPORTS_DIR.mkdir(exist_ok=True)
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
