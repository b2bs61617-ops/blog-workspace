"""YouTube ライブ配信のチャットから直近メッセージを取得する。

yt-dlp の live_chat 字幕ダウンロードを短時間だけ走らせ、生成された
JSON(1行=1アクション)をパースして x_fetch と同じ形の post dict を返す。

post dict:
  {"id", "date"(ISO8601 JST), "author", "text", "source": "yt_chat", "url"}

yt-dlp はライブ配信に対して「配信開始時点からの全チャット(バックログ)」を
まず一気に取得し、その後は新着をポーリングする。バックログだけで
ほぼ現在時刻まで揃うので、数十秒だけ走らせて kill すれば十分。
毎回バックログを取り直すので daemon 不要・自己回復する作り。
"""
import glob
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9))

# メンバー加入・モデレーター操作など位置情報になり得ないレンダラは無視
_TEXT_RENDERERS = (
    "liveChatTextMessageRenderer",
    "liveChatPaidMessageRenderer",      # スーパーチャット(本文あり)
    "liveChatPaidStickerRenderer",      # 本文はほぼ無いが一応
)


def _runs_to_text(message):
    out = []
    for r in (message or {}).get("runs", []):
        if "text" in r:
            out.append(r["text"])
        elif "emoji" in r:
            emo = r["emoji"]
            sc = emo.get("shortcuts") or []
            out.append(sc[0] if sc else (":" + str(emo.get("emojiId", "")) + ":"))
    return "".join(out).strip()


def _iter_actions(obj):
    """live_chat json の1行から addChatItemAction の item を yield。"""
    rca = obj.get("replayChatItemAction")
    actions = rca.get("actions", []) if rca else obj.get("actions", [])
    for a in actions:
        item = a.get("addChatItemAction", {}).get("item")
        if item:
            yield item


def parse_file(path, limit=300):
    """live_chat json をパースして post dict の list(新しい順)を返す。"""
    seen = set()
    posts = []
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue  # kill 直後の途中行など
        for item in _iter_actions(obj):
            r = None
            for key in _TEXT_RENDERERS:
                if key in item:
                    r = item[key]
                    break
            if not r:
                continue
            mid = r.get("id")
            if not mid or mid in seen:
                continue
            msg = _runs_to_text(r.get("message"))
            # スパチャは本文空でも金額ラベルが手がかりになることがあるが、
            # 位置情報用途では本文なしは捨てる
            if not msg:
                continue
            ts_usec = r.get("timestampUsec")
            try:
                dt = datetime.fromtimestamp(int(ts_usec) / 1_000_000, tz=timezone.utc).astimezone(JST)
                date_iso = dt.isoformat()
            except Exception:
                date_iso = ""
            author = ""
            an = r.get("authorName")
            if isinstance(an, dict):
                author = an.get("simpleText", "")
            seen.add(mid)
            posts.append({
                "id": f"yt:{mid}",
                "date": date_iso,
                "author": author,
                "text": msg,
                "source": "yt_chat",
                "url": "",
            })
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    return posts[:limit]


def fetch(video_url, capture_seconds=25, limit=300, python_exe=None):
    """yt-dlp で live_chat を capture_seconds 秒だけ取得してパースする。

    戻り値: post dict の list(新しい順)。取得失敗時は []。
    """
    py = python_exe or sys.executable
    workdir = Path(tempfile.mkdtemp(prefix="ytchat_"))
    out_tmpl = str(workdir / "chat.%(ext)s")
    cmd = [
        py, "-m", "yt_dlp",
        "-q", "--no-warnings", "--no-progress",
        "--skip-download", "--write-subs", "--sub-langs", "live_chat",
        "--no-part",
        "-o", out_tmpl,
        video_url,
    ]

    proc = subprocess.Popen(
        cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        cwd=str(workdir),
    )
    try:
        proc.wait(timeout=capture_seconds)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill()
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass

    files = glob.glob(str(workdir / "chat.live_chat.json*"))
    if not files:
        return []
    files.sort(key=lambda f: Path(f).stat().st_size, reverse=True)
    try:
        return parse_file(files[0], limit=limit)
    except Exception:
        return []


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?",
                    default="https://www.youtube.com/watch?v=LOJxmd-xenc")
    ap.add_argument("--seconds", type=int, default=25)
    ap.add_argument("--limit", type=int, default=50)
    a = ap.parse_args()
    res = fetch(a.url, capture_seconds=a.seconds, limit=a.limit)
    print(f"--- {len(res)} messages ---")
    for p in res:
        print(p["date"], "|", p["author"], "|", p["text"])
