# -*- coding: utf-8 -*-
"""ネタ見張り(2026-11-18〜 トモキ依頼)。マツ(Claude)を使わずにPCだけで動く。

- YouTube: 5グループの公式チャンネル(tools/data/sources.json)に新しい動画が出たら、
  Gemini(無料)に動画そのものを見せて「話した内容・行った場所・服・小物・食べ物」を拾い、
  その場面の画像を保存する。
- SNS: 公式・メンバーのX/Instagram(発信あつめ tools/hasshin と同じ名簿・同じブラウザ)の新しい投稿と写真を集め、
  Geminiにネタになりそうか判定させる。
- LINE: 「AIまつ」公式アカウントで1日2回(8時・20時)まとめて送る(無料は月200通、友だち3人なので1回=3通)。
- 画像と内容メモは AI作業場\\ネタ見張り\\日付\\ に残す(OneDriveで同期されるのでスマホでも見られる)。

usage:
    python tools/neta_watch/neta_watch.py --auto        # タスクスケジューラから1時間おきに呼ぶ(時刻で中身を決める)
    python tools/neta_watch/neta_watch.py --youtube     # YouTubeだけ今すぐ
    python tools/neta_watch/neta_watch.py --sns         # SNSだけ今すぐ(ブラウザが開く)
    python tools/neta_watch/neta_watch.py --digest      # たまったネタを今すぐLINEへ
    --dry-run(LINEに送らず中身を表示) / --hours 24(最初の1回でさかのぼる時間) / --video VIDEO_ID(1本だけ解析)
"""
import argparse
import asyncio
import datetime
import json
import os
import re
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
REPO = TOOLS.parent
for _p in (TOOLS, TOOLS / "hasshin", TOOLS / "rival_watch", TOOLS / "Xiy", REPO):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import hasshin  # noqa: E402
import line_notify  # noqa: E402

sys.path.insert(0, str(HERE))
import sokuho_auto  # noqa: E402

# 記録はOneDriveの外に置く(OneDriveが同期中にファイルをつかんでいて、保存が「アクセス拒否」になるため)
WORK = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "neta_watch"
WORK.mkdir(parents=True, exist_ok=True)
STATE = WORK / "state.json"
LOCK = WORK / "running.lock"
LOG = WORK / "log.txt"
OUT = Path(os.environ.get("NETA_WATCH_OUT") or (REPO.parent / "ネタ見張り"))
MEMBERS = TOOLS / "data" / "members.json"

GEMINI_MODEL = "gemini-flash-latest"
SNS_HOURS = (7, 13, 19)        # SNSを集める時刻
DIGEST_HOURS = (8, 20)         # LINEに送る時刻
MAX_VIDEOS_PER_RUN = 6         # 1回で解析する動画の上限(残りは次の回へ)
MAX_TRIES = 6                  # 解析に失敗した動画をやり直す回数(プレミア公開前・ライブ中など)
UNIFORM_FRAMES = 8             # 場面の画像とは別に、動画全体から均等に残す画像の数
SNS_JUDGE_BATCH = 20           # SNSの判定を1回のGeminiにまとめる件数
LINE_BUBBLE_CHARS = 4800       # LINEの吹き出し1つの上限(5000字)より少し小さく
LINE_MAX_BUBBLES = 5           # 1回の送信で送れる吹き出しの数(5つまでなら1通として数えられる)
LOCK_STALE_MIN = 90

KIND_ICON = {"場所": "📍", "服": "👕", "小物": "💍", "食べ物": "🍴", "その他": "💡"}


# ---------------------------------------------------------------- 小さな部品(テストあり)
def safe_name(text, limit=40):
    """フォルダ名・ファイル名に使えない文字を消して短くする。"""
    text = re.sub(r'[\\/:*?"<>|\r\n\t]+', " ", str(text or "")).strip()
    text = re.sub(r"\s+", " ", text)
    return text[:limit].rstrip(" .") or "no_title"


def mmss(sec):
    try:
        sec = int(float(sec))
    except (TypeError, ValueError):
        return ""
    return "{}:{:02d}".format(sec // 60, sec % 60) if sec < 3600 else "{}:{:02d}:{:02d}".format(sec // 3600, sec % 3600 // 60, sec % 60)


def parse_json_text(text):
    """Geminiの返事からJSONを取り出す(```json で囲まれていてもよい)。"""
    text = (text or "").strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1).strip()
    try:
        return json.loads(text)
    except ValueError:
        m = re.search(r"[\[{].*[\]}]", text, re.S)
        return json.loads(m.group(0)) if m else None


def neta_timestamps(neta, duration, uniform=UNIFORM_FRAMES):
    """ネタが映る時刻 + 動画全体から均等な時刻。[(秒, ラベル), ...] を時刻順で返す。"""
    out = []
    for n in neta or []:
        try:
            t = float(n.get("time_sec"))
        except (TypeError, ValueError):
            continue
        if duration and not (0 <= t <= duration):
            continue
        out.append((t, "{}_{}".format(n.get("kind") or "ネタ", n.get("what") or "")))
    if duration and duration > 0 and uniform > 0:
        for i in range(uniform):
            out.append((duration * (0.05 + 0.9 * i / max(uniform - 1, 1)), "全体"))
    out.sort(key=lambda x: x[0])
    return out


def split_bubbles(blocks, header, limit=LINE_BUBBLE_CHARS, max_bubbles=LINE_MAX_BUBBLES):
    """文のかたまりをLINEの吹き出しに詰める。入りきらない数を返す。"""
    bubbles, cur, dropped = [], header, 0
    for b in blocks:
        if len(cur) + len(b) + 2 > limit:
            bubbles.append(cur)
            cur = ""
            if len(bubbles) >= max_bubbles:
                dropped += 1
                continue
        if len(bubbles) >= max_bubbles:
            dropped += 1
            continue
        cur = (cur + "\n\n" + b) if cur else b
    if cur and len(bubbles) < max_bubbles:
        bubbles.append(cur)
    return bubbles, dropped


def due(hour, hours, last_iso, now, gap_hours=3):
    """いまがその時刻で、少し前にまだやっていなければTrue。"""
    if hour not in hours:
        return False
    if not last_iso:
        return True
    try:
        last = datetime.datetime.fromisoformat(last_iso)
    except ValueError:
        return True
    return (now - last).total_seconds() > gap_hours * 3600


# ---------------------------------------------------------------- 準備
def log(*args):
    msg = " ".join(str(a) for a in args)
    line = "[{}] {}".format(datetime.datetime.now().strftime("%m/%d %H:%M:%S"), msg)
    try:
        print(line, flush=True)
    except Exception:  # noqa: BLE001  pythonwでは画面が無い
        pass
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def trim_log():
    try:
        lines = LOG.read_text(encoding="utf-8").splitlines()
        if len(lines) > 3000:
            LOG.write_text("\n".join(lines[-2000:]) + "\n", encoding="utf-8")
    except OSError:
        pass


def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except ValueError:
            pass
    return {}


def save_state(state):
    state["yt_seen"] = state.get("yt_seen", [])[-3000:]
    state["sns_seen"] = state.get("sns_seen", [])[-5000:]
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    for attempt in range(5):
        try:
            tmp.replace(STATE)
            return
        except PermissionError:  # ウイルス対策などが一瞬つかんでいるとき
            time.sleep(1 + attempt)
    STATE.write_text(tmp.read_text(encoding="utf-8"), encoding="utf-8")


def env():
    return line_notify.load_env(REPO / ".env")


def gemini_client():
    key = env().get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(".envにGEMINI_API_KEYが無い")
    from google import genai
    return genai.Client(api_key=key)


def member_names(group):
    try:
        g = json.loads(MEMBERS.read_text(encoding="utf-8"))["groups"].get(group) or {}
        return "、".join(m["name"] for m in g.get("members", []))
    except Exception:  # noqa: BLE001
        return ""


def day_dir(now):
    d = OUT / now.astimezone().strftime("%Y-%m-%d")
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------- YouTube
YT_PROMPT = """あなたはアイドルファン向けブログのネタ探し係です。
これは{glabel}の公式YouTubeの動画「{title}」です。メンバー: {members}
動画を最後まで見て(聞いて)、次の形のJSONだけを返してください。

{{"summary": "どんな動画か3〜4文で",
 "talk": ["話した内容のポイント。誰が何を言ったか(最大8つ)"],
 "neta": [{{"kind": "場所|服|小物|食べ物|その他", "what": "何か(例: 黒いニット帽)", "who": "メンバー名(分かれば)",
           "detail": "画面に見えた文字・ロゴ・店名・特徴・発言。分からなければ『特定できず』",
           "time_sec": そのものがいちばんはっきり映る秒数, "sure": "確実|たぶん|不明"}}],
 "blog_ideas": ["ファンが検索しそうな疑問形の記事タイトル案(最大3つ)"]}}

ルール:
- ブログのネタになりそうなもの(行った場所・お店、着ている服、アクセサリーや持ち物、食べた物、話した思い出・エピソード)をできるだけ拾う(最大15こ)。
- ブランド名・店名・地名は、画面の文字やロゴ・発言で確かめられたときだけ書く。推測なら sure を「たぶん」、分からなければ「不明」にする。
- 日本語で書く。JSON以外は書かない。"""

YT_FALLBACK_PROMPT = """以下は{glabel}の公式YouTube動画「{title}」から抜き出した画像{count}枚と、文字起こしです。メンバー: {members}
動画を見られなかったので、これだけを手がかりに、次の形のJSONだけを返してください。time_sec は書かなくてよいです。
{{"summary": "...", "talk": ["..."], "neta": [{{"kind": "場所|服|小物|食べ物|その他", "what": "...", "who": "...", "detail": "...", "sure": "確実|たぶん|不明"}}], "blog_ideas": ["..."]}}
推測で断定しないこと。

文字起こし:
{transcript}"""


def video_info(video_id):
    import yt_dlp
    # 画面を取るだけなので音なしの映像でよい。opencvが読みやすいH.264(avc1)を優先、縦動画もあるので幅・高さとも1280まで
    opts = {"quiet": True, "no_warnings": True,
            "format": "bv*[vcodec^=avc1][height<=1280][width<=1280]/bv*[ext=mp4][height<=1280]/b[height<=1280]/bv*/b"}
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info("https://www.youtube.com/watch?v=" + video_id, download=False)


def grab_frames(stream_url, stamps, folder):
    """ストリームから指定の時刻の画像を保存する(動画は丸ごと落とさない)。保存したファイル名の一覧を返す。"""
    import cv2
    saved = []
    cap = cv2.VideoCapture(stream_url)
    try:
        if not cap.isOpened():
            return saved
        for t, label in stamps:
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ok, frame = cap.read()
            if not ok:
                continue
            ok, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            if not ok:
                continue
            name = "{:03d}m{:02d}s_{}.jpg".format(int(t) // 60, int(t) % 60, safe_name(label, 30))
            (folder / name).write_bytes(buf.tobytes())
            saved.append(name)
    finally:
        cap.release()
    return saved


def ask_gemini_video(client, video_id, title, group, duration):
    from google.genai import types
    prompt = YT_PROMPT.format(glabel=hasshin.glabel(group), title=title, members=member_names(group) or "不明")
    cfg = {"response_mime_type": "application/json"}
    if duration and duration > 30 * 60:
        cfg["media_resolution"] = types.MediaResolution.MEDIA_RESOLUTION_LOW  # 長い動画は軽くして見る
    part = types.Part(file_data=types.FileData(file_uri="https://www.youtube.com/watch?v=" + video_id))
    res = client.models.generate_content(model=GEMINI_MODEL, contents=[part, prompt],
                                         config=types.GenerateContentConfig(**cfg))
    return parse_json_text(res.text)


def ask_gemini_fallback(client, title, group, folder, frames, video_id):
    from google.genai import types
    transcript = ""
    try:
        from youtube_transcript import get_transcript
        transcript = (get_transcript(video_id) or "")[:6000]
    except Exception:  # noqa: BLE001
        transcript = "(取れなかった)"
    parts = [types.Part.from_bytes(data=(folder / f).read_bytes(), mime_type="image/jpeg") for f in frames[:12]]
    prompt = YT_FALLBACK_PROMPT.format(glabel=hasshin.glabel(group), title=title, count=len(parts),
                                       members=member_names(group) or "不明", transcript=transcript)
    res = client.models.generate_content(model=GEMINI_MODEL, contents=[*parts, prompt],
                                         config=types.GenerateContentConfig(response_mime_type="application/json"))
    return parse_json_text(res.text)


def write_video_memo(folder, item, result, frames):
    url = item["url"]
    watch = "https://www.youtube.com/watch?v=" + item["key"].split(":", 1)[1]
    lines = ["{} 公式YouTube「{}」".format(hasshin.glabel(item["group"]), item["text"]), url,
             "公開: " + hasshin.when(item["date"]), "", "■ どんな動画", result.get("summary", ""), "", "■ 話した内容"]
    lines += ["・" + t for t in result.get("talk", [])]
    lines += ["", "■ ネタになりそうなもの(AIの見立て。記事にする前に画像で確かめてワン)"]
    for n in result.get("neta", []):
        t = n.get("time_sec")
        at = " [{}] {}&t={}s".format(mmss(t), watch, int(float(t))) if mmss(t) else ""
        lines.append("{} {}: {}{}({}){}".format(KIND_ICON.get(n.get("kind"), "💡"), n.get("kind", ""), n.get("what", ""),
                                               " / " + n["who"] if n.get("who") else "", n.get("sure", ""), at))
        if n.get("detail"):
            lines.append("    " + n["detail"])
    if result.get("blog_ideas"):
        lines += ["", "■ 記事タイトル案"] + ["・" + t for t in result["blog_ideas"]]
    lines += ["", "■ 画像({}枚)".format(len(frames))] + ["  " + f for f in frames]
    (folder / "内容.txt").write_text("\n".join(lines), encoding="utf-8")


def analyze_video(client, item, now):
    """動画1本を解析して、画像とメモを保存し、LINE用のネタを返す。まだ見られない動画は None。"""
    vid = item["key"].split(":", 1)[1]
    info = {}
    try:
        info = video_info(vid)
    except Exception as e:  # noqa: BLE001  画面が取れないだけなら、解析は続ける
        log("  動画の情報が取れなかった:", str(e)[:150])
    if info.get("live_status") in ("is_upcoming", "is_live"):
        raise RuntimeError("まだ公開前かライブ中")
    duration = info.get("duration") or 0
    stream = info.get("url") or ""
    folder = day_dir(now) / safe_name("{}_YouTube_{}".format(hasshin.glabel(item["group"]), item["text"]), 60)
    folder.mkdir(parents=True, exist_ok=True)
    result, how, frames = None, "動画を見た", []
    for attempt in range(3):
        try:
            result = ask_gemini_video(client, vid, item["text"], item["group"], duration)
            break
        except Exception as e:  # noqa: BLE001
            busy = any(s in str(e) for s in ("503", "UNAVAILABLE", "overloaded", "high demand"))
            log("  動画を直接見られなかった{}: {}".format("(混雑・{}回目)".format(attempt + 1) if busy else "", str(e)[:120]))
            if not busy or attempt == 2:
                break
            time.sleep(30 * (attempt + 1))  # 混んでいるだけなら少し待ってやり直す
    if not isinstance(result, dict):
        frames = grab_frames(stream, neta_timestamps([], duration, 12), folder) if stream else []
        if not frames:
            raise RuntimeError("動画も画像も見られなかった")
        result, how = ask_gemini_fallback(client, item["text"], item["group"], folder, frames, vid), "画像+文字起こし"
        if not isinstance(result, dict):
            raise RuntimeError("Geminiの返事が読めなかった")
    elif stream:
        frames = grab_frames(stream, neta_timestamps(result.get("neta"), duration), folder)
    try:
        thumb = hasshin.fetch("https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(vid), 15)
        (folder / "00_サムネ.jpg").write_bytes(thumb)
    except Exception:  # noqa: BLE001
        pass
    write_video_memo(folder, item, result, frames)
    log("  解析OK({}) ネタ{}こ 画像{}枚 → {}".format(how, len(result.get("neta", [])), len(frames), folder))
    return {"group": item["group"], "platform": "YouTube", "account": item["account"], "title": item["text"],
            "url": item["url"], "date": item["date"].isoformat(), "summary": result.get("summary", ""),
            "talk": result.get("talk", []), "neta": result.get("neta", []), "ideas": result.get("blog_ideas", []),
            "folder": str(folder.relative_to(OUT))}


def run_youtube(state, now, first_hours, only_video=None):
    sources = json.loads(hasshin.SOURCES.read_text(encoding="utf-8"))
    accounts = [(g, "youtube", a) for g, d in sources["groups"].items() for a in d.get("youtube", []) if a.get("channel_id")]
    items, failed = hasshin.collect_youtube(accounts, now, 24 * 7)
    for f in failed:
        log("  " + f)
    seen = set(state.setdefault("yt_seen", []))
    tries = state.setdefault("yt_tries", {})
    first = not state.get("yt_started")
    todo = []
    for it in sorted(items, key=lambda i: i["date"]):
        if only_video:
            if it["key"] == "yt:" + only_video:
                todo.append(it)
            continue
        if it["key"] in seen:
            continue
        if first and (now - it["date"]).total_seconds() > first_hours * 3600:
            seen.add(it["key"])  # 見張りを始める前の古い動画は解析しない
            continue
        todo.append(it)
    if not only_video:
        state["yt_started"] = state.get("yt_started") or now.isoformat()
    log("YouTube: {}チャンネル / 新しい動画 {}本".format(len(accounts), len(todo)))
    if not todo:
        state["yt_seen"] = list(seen)
        return
    client = gemini_client()
    for it in todo[:MAX_VIDEOS_PER_RUN]:
        log("  解析: [{}] {}".format(hasshin.glabel(it["group"]), it["text"]))
        try:
            state.setdefault("pending", []).append(analyze_video(client, it, now))
            seen.add(it["key"])
            tries.pop(it["key"], None)
        except Exception as e:  # noqa: BLE001
            n = tries.get(it["key"], 0) + 1
            tries[it["key"]] = n
            log("  失敗({}回目): {}".format(n, str(e)[:150]))
            if n >= MAX_TRIES:
                seen.add(it["key"])
                state.setdefault("pending", []).append({
                    "group": it["group"], "platform": "YouTube", "account": it["account"], "title": it["text"],
                    "url": it["url"], "date": it["date"].isoformat(), "summary": "(自動で中身を見られなかった。動画を直接見てワン)",
                    "neta": [], "ideas": [], "folder": ""})
        state["yt_seen"] = list(seen)
        save_state(state)
        time.sleep(5)


# ---------------------------------------------------------------- SNS
SNS_PROMPT = """あなたはアイドルファン向けブログのネタ探し係です。グループ: {glabel}(メンバー: {members})
下の投稿{count}件(本文と写真)を見て、ブログ記事のネタになりそうかを判定し、JSONの配列だけを返してください。
ネタになる例: 私服・アクセサリー・持ち物・行った場所やお店・食べた物・新しいお仕事(CM・ドラマ・雑誌・イベント)の発表・ファンが「これどこ？」「何？」と気になりそうなもの。
ネタにならない例: ただの告知の繰り返し・リポストだけ・中身のない投稿。

[{{"no": 投稿の番号, "neta": true/false, "what": "ネタの中身(例: 目黒蓮さんの黒いレザージャケット)", "kind": "場所|服|小物|食べ物|お仕事|その他",
  "detail": "写真や本文から読み取れる文字・ロゴ・店名など。分からなければ『特定できず』", "question": "ファンが検索しそうな疑問(例: ○○のジャケットはどこの？)"}}]
ブランド名・店名は写真の文字や本文で確かめられたときだけ書く。日本語で。"""


def judge_sns(client, group, batch, folder):
    from google.genai import types
    parts, lines = [], []
    for no, it in enumerate(batch, 1):
        lines.append("【{}】{} {} {}: {}".format(no, hasshin.PLATFORM[it["platform"]], it["account"],
                                               "(リポスト)" if it["repost"] else "", it["text"][:400]))
        for img in it.get("images", [])[:2]:
            p = folder / img
            if p.exists():
                parts.append(types.Part.from_text(text="【{}】の写真".format(no)))
                parts.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/jpeg"))
    prompt = SNS_PROMPT.format(glabel=hasshin.glabel(group), members=member_names(group) or "不明", count=len(batch))
    res = client.models.generate_content(model=GEMINI_MODEL, contents=[*parts, prompt + "\n\n" + "\n".join(lines)],
                                         config=types.GenerateContentConfig(response_mime_type="application/json"))
    data = parse_json_text(res.text)
    return data if isinstance(data, list) else []


def run_sns(state, now, first_hours):
    sources = json.loads(hasshin.SOURCES.read_text(encoding="utf-8"))
    accounts = [a for a in hasshin.active_accounts(sources) if a[1] in ("x", "instagram")]
    first = not state.get("sns_started")
    hours = first_hours if first else 30
    ig_seen = state.setdefault("ig_seen", {})
    ig_cache = state.setdefault("ig_cache", {})
    log("SNS: {}アカウントを見に行く(直近{}時間)".format(len(accounts), hours))
    items, failed = asyncio.run(hasshin.collect_browser(accounts, now, hours, 0, ig_seen, ig_cache))
    for f in failed:
        log("  " + f)
    seen = set(state.setdefault("sns_seen", []))
    new = [i for i in items if i["key"] not in seen]  # 固定投稿も新しければ拾う(古いものは時間で外れる)
    state["sns_started"] = state.get("sns_started") or now.isoformat()
    state["sns_last"] = now.isoformat()
    state["ig_cache"] = dict(sorted(ig_cache.items(), key=lambda kv: kv[1]["date"])[-300:])
    state["ig_seen"] = dict(sorted(ig_seen.items(), key=lambda kv: kv[1])[-3000:])
    log("  新しい投稿 {}件".format(len(new)))
    if not new:
        save_state(state)
        return
    folder = day_dir(now) / "SNS_{}".format(now.astimezone().strftime("%H%M"))
    hasshin.save_images(new, folder)
    client = gemini_client()
    memo = ["SNSの新しい投稿 {}件({})".format(len(new), now.astimezone().strftime("%m/%d %H:%M")), ""]
    for group in [s["group"] for s in hasshin.blogkit.SITES.values() if s["group"]]:
        gi = [i for i in new if i["group"] == group]
        for start in range(0, len(gi), SNS_JUDGE_BATCH):
            batch = gi[start:start + SNS_JUDGE_BATCH]
            try:
                verdicts = {v.get("no"): v for v in judge_sns(client, group, batch, folder) if isinstance(v, dict)}
            except Exception as e:  # noqa: BLE001
                log("  判定に失敗({}): {}".format(group, str(e)[:120]))
                verdicts = {}
            for no, it in enumerate(batch, 1):
                v = verdicts.get(no) or {}
                memo += ["■ {} {} {} {}".format(hasshin.glabel(group), hasshin.PLATFORM[it["platform"]], it["account"], hasshin.when(it["date"])),
                         "  " + it["url"], "  " + it["text"].replace("\n", " ")[:200]]
                memo += ["  写真: " + im for im in it.get("images", [])]
                if v.get("neta"):
                    memo.append("  ★ネタ: {} / {} / 疑問: {}".format(v.get("what", ""), v.get("detail", ""), v.get("question", "")))
                    state.setdefault("pending", []).append({
                        "group": group, "platform": hasshin.PLATFORM[it["platform"]], "account": it["account"],
                        "title": it["text"].replace("\n", " ")[:60], "url": it["url"], "date": it["date"].isoformat(),
                        "summary": "", "neta": [{"kind": v.get("kind", "その他"), "what": v.get("what", ""), "detail": v.get("detail", "")}],
                        "ideas": [v["question"]] if v.get("question") else [], "folder": str(folder.relative_to(OUT))})
                memo.append("")
            time.sleep(3)
    (folder / "一覧.txt").write_text("\n".join(memo), encoding="utf-8")
    seen.update(i["key"] for i in new)
    state["sns_seen"] = list(seen)
    save_state(state)
    log("  SNSの記録 → {}".format(folder))


# ---------------------------------------------------------------- LINE
def entry_text(p):
    lines = ["▶{} {}".format(p["platform"], p["title"][:50])]
    if p.get("summary"):
        lines.append("📝" + p["summary"][:300])
    talk = (p.get("talk") or [])[:4]
    if talk:
        lines.append("🗣話した内容")
        lines += ["・" + t[:80] for t in talk]
    for n in (p.get("neta") or [])[:6]:
        t = " ({})".format(mmss(n.get("time_sec"))) if mmss(n.get("time_sec")) else ""
        d = n.get("detail") or ""
        d = "" if not d or "特定できず" in d else ":" + d[:40]
        lines.append("{}{}{}{}".format(KIND_ICON.get(n.get("kind"), "💡"), n.get("what", "")[:40], d, t))
    for q in (p.get("ideas") or [])[:2]:
        lines.append("❓" + q[:60])
    lines.append(p["url"])
    return "\n".join(lines)


def build_digest(pending, now):
    order = ["sokuho"] + [s["group"] for s in hasshin.blogkit.SITES.values() if s["group"]]
    pending = sorted(pending, key=lambda p: (order.index(p["group"]) if p["group"] in order else 99, p["platform"] != "YouTube", p["date"]))
    part = "朝" if now.astimezone().hour < 12 else "夜"
    header = "🐶ネタ見張り {} {}のまとめワン\nYouTube {}本・SNS {}件・速報 {}件".format(
        now.astimezone().strftime("%m/%d"), part,
        sum(1 for p in pending if p["platform"] == "YouTube"),
        sum(1 for p in pending if p["platform"] not in ("YouTube", "速報")),
        sum(1 for p in pending if p["platform"] == "速報"))
    blocks, cur = [], None
    for p in pending:
        txt = entry_text(p)
        if p["group"] != cur:
            cur = p["group"]
            txt = "■" + ("⚡速報(chomoand.com)" if cur == "sokuho" else hasshin.glabel(cur)) + "\n" + txt
        blocks.append(txt)
    days = sorted({p["folder"].split(os.sep)[0].split("/")[0] for p in pending if p.get("folder")})
    footer = "📷画像とくわしいメモ: OneDrive › デスクトップ › AI作業場 › ネタ見張り › " + "・".join(days) if days else ""
    bubbles, dropped = split_bubbles(blocks + ([footer] if footer else []), header)
    if dropped:
        bubbles[-1] += "\n\n…ほか{}件はフォルダのメモを見てワン".format(dropped)
    return bubbles


def send_line(bubbles):
    token = env().get("LINE_CHANNEL_ACCESS_TOKEN")
    if not token:
        raise RuntimeError(".envにLINE_CHANNEL_ACCESS_TOKENが無い")
    data = {"messages": [{"type": "text", "text": b} for b in bubbles[:LINE_MAX_BUBBLES]]}
    return line_notify._request(line_notify.API_BASE + "/message/broadcast", token, data=data, method="POST")


def run_digest(state, now, dry_run=False):
    pending = state.get("pending", [])
    if not pending:
        log("LINE: 新しいネタが無いので送らない")
        state["digest_last"] = now.isoformat()
        save_state(state)
        return
    bubbles = build_digest(pending, now)
    if dry_run:
        print("\n\n=====(LINEの吹き出し)=====\n\n".join(bubbles))
        return
    state["digest_last"] = now.isoformat()
    send_line(bubbles)
    log("LINE: {}件を吹き出し{}つで送った".format(len(pending), len(bubbles)))
    state["pending"] = []
    save_state(state)


# ---------------------------------------------------------------- 入口
def take_lock():
    if LOCK.exists() and time.time() - LOCK.stat().st_mtime < LOCK_STALE_MIN * 60:
        return False
    LOCK.write_text(str(os.getpid()), encoding="utf-8")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description="ネタ見張り")
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--youtube", action="store_true")
    ap.add_argument("--sns", action="store_true")
    ap.add_argument("--digest", action="store_true")
    ap.add_argument("--sokuho", action="store_true", help="速報を今すぐ(0〜7時以外は下書きで止まる)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--hours", type=int, default=24, help="最初の1回でさかのぼる時間")
    ap.add_argument("--video", default="", help="この動画IDだけ解析する(ためし用)")
    a = ap.parse_args(argv)
    if not (a.auto or a.youtube or a.sns or a.digest or a.video or a.sokuho):
        ap.print_help()
        return 1
    if not take_lock():
        log("前の回がまだ動いているので今回は休むワン")
        return 0
    try:
        trim_log()
        now = datetime.datetime.now(datetime.timezone.utc)
        hour = now.astimezone().hour
        state = load_state()
        steps = []
        if a.auto or a.youtube or a.video:
            steps.append(("YouTube", lambda: run_youtube(state, now, a.hours, a.video or None)))
        if a.sokuho or (a.auto and hour in sokuho_auto.NIGHT_HOURS):
            steps.append(("速報(夜)", lambda: sokuho_auto.run(state, now, "night")))
        elif a.auto and due(hour, sokuho_auto.DAY_HOURS, state.get("sokuho_last"), now):
            steps.append(("速報(一覧)", lambda: sokuho_auto.run(state, now, "list")))
        if a.sns or (a.auto and due(hour, SNS_HOURS, state.get("sns_last"), now)):
            steps.append(("SNS", lambda: run_sns(state, now, a.hours)))
        if a.digest or (a.auto and due(hour, DIGEST_HOURS, state.get("digest_last"), now)):
            steps.append(("LINE", lambda: run_digest(state, now, a.dry_run)))
        for name, fn in steps:
            try:
                fn()
            except Exception as e:  # noqa: BLE001  1つ失敗しても次へ進む
                log("{}でエラー: {}".format(name, e))
                log(traceback.format_exc()[-800:])
        save_state(state)
        return 0
    finally:
        try:
            LOCK.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
