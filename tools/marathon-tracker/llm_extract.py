"""新着ツイートから「記事のリアルタイム欄に追記する内容」を構造化して取り出す。

primary: claude -p (Claude Code CLI)  /  fallback: Gemini (GEMINI_API_KEY)

戻り値(dict):
{
  "update": bool,                  # 位置情報として追記する価値があるか
  "current_location": "世田谷区・駒沢エリア(休憩中)",   # capbox 用の短いラベル
  "entries": [
     {"time": "8/30 15:42",
      "text": "世田谷区の駒沢エリアを通過。日産駒沢店で給水休憩。残り約32km。",
      "map_query": "日産 駒沢店"}          # 地図不要なら ""
  ],
  "reason": "..."
}
"""
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_env():
    env = {}
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def _build_prompt(runner, course_context, tweets, last_location, recent_entries=None):
    lines = []
    for t in tweets:
        lines.append(f"- [{t.get('date','')}] (@{t.get('source','').lstrip('@')}) {t.get('text','')}")
    tweets_block = "\n".join(lines)

    route_block = "(まだ無し)"
    if recent_entries:
        rl = []
        for e in recent_entries[:8]:
            rl.append(f"- {e.get('time','')} {e.get('text','')}")
        route_block = "\n".join(rl)

    return f"""あなたは24時間テレビ チャリティーマラソンの「現在地」速報を書く編集者です。
ランナー: {runner}
予想コースの前提: {course_context}
現在、記事に載っている最新の現在地: {last_location or "(まだ無し)"}

これまでの経路(記事に載せている時系列。新しい順):
{route_block}

以下は監視中の新着メッセージです(各行の (@xxx) が出どころ)。ここから「ランナーが今どこにいるか/どこを通過したか/どこで休憩したか」に関する事実だけを抜き出してください。

【出どころの信頼度】
- (@share_map) は追跡者(@YSB_DANCHO)のリアルタイム位置共有マップのスクショを画像解析して読んだピン位置(地図に印字された地名そのもの)。**いちばん信頼度が高い**。ここに出る市区町村・町丁目を現在地として断定してよい(「位置情報の更新」が数分前なら尚更)。文中に（緯度,経度）があれば map_query にその数値をそのまま入れる。無ければ町丁目名を入れる。「付近」「おおよそ」等がありピン位置がぼやけている場合は (@mapshot) と突き合わせ、両者が食い違うなら (@mapshot) を優先する。
- (@screen_map) / (@mapshot) はGoogleマップ画面のスクショをAIが読んだもの。地図の中心付近の地名・駅名・ランドマークは信頼度が高い。「(ラベル不鮮明)」等はっきりしない部分は使わない。
- (@yt_chat) はYouTube生配信の視聴者コメント。玉石混交。複数コメントで一致する位置情報は採用してよいが、1件だけの憶測は「〜との声」程度に留め、断定しない。番組を見ていない雑談・応援・予想だけのコメントは無視。
- (@YSB_DANCHO / @24tv24tv / @yes0724day / search:...) はXの追跡班・沿道情報。実況として信頼度は高め。伝聞は「〜との情報」の形で。
- (@heading) は前回観測地点から今回地点への移動ベクトル(距離・方位・8方位)を機械計算したもの。位置の断定には使わないが、direction と本文2文目の「どの方面へ向かっているか」を書くときの主要な根拠にする。
- 複数ソースが食い違うときは (@share_map) > (@screen_map)/(@mapshot) > 追跡班のX > 複数一致の (@yt_chat) > 単発コメント の順で信頼する。

【ルール】
- 位置に関する具体情報(地名・施設名・エリア・距離)が無いメッセージ(応援・感想・番組の感想だけ)は無視する。
- 憶測や沿道の伝聞でも「〜との情報」と分かる形で拾ってよいが、誇張しない。断定しすぎない。
- まだスタートしていない/スタート地点の当てずっぽうしか無い場合は update=false。
- **前回から移動していない(同じ施設・同じ道・同じ交差点付近にとどまっている)なら update=false**。言い換えただけの繰り返しは出さない。update=true にするのは「前回と違う地点へ進んだ」「新しい休憩地点に入った/出た」「距離の節目を通過した」と読み取れるときだけ。
- current_location は"今いる具体的な場所"を書く(例:「日産スタジアム周回コース」→ 移動後は「新横浜元石川線・新羽町付近」)。同じ場所なら文言も前回と同じにする。移動したら必ず違う文言になるはず。
- 個人の家・特定できる一般人の情報は書かない。ランナーの位置と公共の施設・地名のみ。
- 各エントリの time は「M/D HH:MM」形式。ポストの投稿時刻(JST)から推定。分からなければ現在時刻でよい。
- map_query は Googleマップで検索して正しい場所が出る日本語の地名/施設名(例「日産 駒沢店」「二子玉川駅」「府中市 郷土の森公園」)。エリアだけで施設が無ければ市区名+ランドマーク。地図が付けられないなら空文字。
- current_location は capbox に出す短いラベル。「世田谷区・駒沢エリア(走行中)」のように 場所 + (走行中/休憩中/仮眠中 など) 。※ここには進行方向を書かない(移動判定に使うため場所だけ)。
- direction は capbox に出す「今どっちへ向かっているか」の短い一文(15〜30字)。「これまでの経路」と「予想コースの前提」から推定する。例:「鶴見川沿いを北上、多摩川方面へ」「中原街道を東進し都心方向へ」。休憩中なら「◯◯で休憩中(再開後は△△方面)」。分からなければ空文字。
- entries は原則1件だけ。今回の「新しい動き」を1行にまとめる。似た内容を2件に分けない。
- 新しい位置情報が無ければ update=false。

【entries の text の書き方(重要)】
- 情報源を書かない。「GPS情報によると」「視聴者コメントによると」「配信によると」「Xの情報では」「〜との情報」等の出どころ表現は本文に入れない。事実として淡々と書く(不確実なときだけ「〜とみられます」程度でぼかす)。
- 1文目: 現在地の住所・エリア(市区町村＋町丁目や、近くの駅・交差点・橋・幹線道路名)。
- 2文目: 「これまでの経路」と「予想コースの前提」を踏まえて、いま **どの方面へ向かっているか**(例:「多摩川方面へ北上中」「中原街道を東進し都心方向へ」)。
- **現在は鶴見川沿いを北上中**。この区間は「鶴見川沿いのサイクリングロード／河川敷の遊歩道」を走っている。具体的な県道番号や幹線道路名を断定しない(「鶴見川沿いを北上」でよい)。中盤以降、川崎・世田谷・都心に入ってからは中原街道・環八・目黒通り・第一京浜などの大通り沿いになる。進行方向は「予想コースの前提」の大きな流れ(→川崎方面→世田谷→都心南部→両国)に沿って書く。
- 休憩・仮眠・再スタートなど状態変化があればそれも1文で。
- 全体で2〜3文、120字前後。

【新着ポスト】
{tweets_block}

【出力】次のJSONだけを出力。前後に説明文を付けない。
{{"update": true/false, "current_location": "...", "direction": "...", "entries": [{{"time":"M/D HH:MM","text":"...","map_query":"..."}}], "reason":"..."}}
"""


def _extract_json(s):
    s = s.strip()
    s = re.sub(r"^```(?:json)?", "", s).strip()
    s = re.sub(r"```$", "", s).strip()
    m = re.search(r"\{.*\}", s, re.DOTALL)
    if not m:
        raise ValueError(f"JSONが見つからない: {s[:300]}")
    return json.loads(m.group(0))


def _try_claude(prompt, timeout=300):
    exe = "claude.cmd" if os.name == "nt" else "claude"
    try:
        r = subprocess.run(
            [exe, "-p", prompt, "--output-format", "text"],
            capture_output=True, text=True, encoding="utf-8", timeout=timeout,
        )
    except FileNotFoundError:
        r = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True, text=True, encoding="utf-8", timeout=timeout,
        )
    if r.returncode != 0:
        raise RuntimeError(f"claude -p 失敗 rc={r.returncode}: {(r.stderr or '')[:300]}")
    return _extract_json(r.stdout)


GEMINI_FALLBACK_MODELS = ["gemini-3.5-flash", "gemini-3.6-flash", "gemini-3.1-flash-lite"]


def _try_gemini(prompt, model, api_key):
    import time

    from google import genai
    from google.genai import types

    # 1コールが詰まって10分枠を食い潰さないよう HTTP タイムアウトを明示(ミリ秒)。
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=40000),
    )

    # config のモデルを先頭に、既知の代替モデルを続ける。
    #  - 混雑(503/504/429 など)      → 少し待って同モデル再試行、ダメなら次モデル
    #  - モデル無効(404/NOT_FOUND 等) → 即座に次モデルへ
    #  - それ以外(認証エラー等)        → 即 raise
    models = [model] + [m for m in GEMINI_FALLBACK_MODELS if m != model]

    last_err = None
    for mi, model_name in enumerate(models):
        for attempt in range(2):
            try:
                resp = client.models.generate_content(model=model_name, contents=prompt)
                return _extract_json(resp.text)
            except Exception as e:  # noqa: BLE001
                last_err = e
                msg = str(e)
                if any(s in msg for s in ("404", "NOT_FOUND", "not available", "not found")):
                    break  # このモデルは使えない。次モデルへ
                transient = any(s in msg for s in (
                    "503", "504", "429", "500", "UNAVAILABLE", "DEADLINE_EXCEEDED",
                    "RESOURCE_EXHAUSTED", "overloaded", "high demand", "timed out", "timeout",
                ))
                if not transient:
                    raise
                if attempt == 0:
                    time.sleep(5)
        if mi < len(models) - 1:
            time.sleep(2)
    raise RuntimeError(f"Gemini 全モデルで失敗(リトライ尽きた): {last_err}")


def _normalize(d):
    d.setdefault("update", False)
    d.setdefault("current_location", "")
    d.setdefault("direction", "")
    d.setdefault("entries", [])
    d.setdefault("reason", "")
    d["direction"] = (d.get("direction") or "").strip()
    clean = []
    for e in d.get("entries") or []:
        if not isinstance(e, dict):
            continue
        txt = (e.get("text") or "").strip()
        if not txt:
            continue
        clean.append({
            "time": (e.get("time") or "").strip(),
            "text": txt,
            "map_query": (e.get("map_query") or "").strip(),
        })
    d["entries"] = clean
    if not clean:
        d["update"] = False
    return d


def extract(runner, course_context, tweets, last_location="", primary="claude",
            gemini_model="gemini-flash-latest", recent_entries=None):
    prompt = _build_prompt(runner, course_context, tweets, last_location, recent_entries)
    env = _load_env()
    gkey = env.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

    order = ["claude", "gemini"] if primary == "claude" else ["gemini", "claude"]
    errors = []
    for eng in order:
        try:
            if eng == "claude":
                return _normalize(_try_claude(prompt))
            if eng == "gemini":
                if not gkey:
                    raise RuntimeError("GEMINI_API_KEY 未設定")
                return _normalize(_try_gemini(prompt, gemini_model, gkey))
        except Exception as e:  # noqa: BLE001
            errors.append(f"{eng}: {e}")
    raise RuntimeError("LLM抽出に全て失敗: " + " / ".join(errors))
