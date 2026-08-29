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


def _build_prompt(runner, course_context, tweets, last_location):
    lines = []
    for t in tweets:
        lines.append(f"- [{t.get('date','')}] (@{t.get('source','').lstrip('@')}) {t.get('text','')}")
    tweets_block = "\n".join(lines)
    return f"""あなたは24時間テレビ チャリティーマラソンの「現在地」速報を書く編集者です。
ランナー: {runner}
予想コースの前提: {course_context}
現在、記事に載っている最新の現在地: {last_location or "(まだ無し)"}

以下は監視中のXアカウントの新着ポストです。ここから「ランナーが今どこにいるか/どこを通過したか/どこで休憩したか」に関する事実だけを抜き出してください。

【ルール】
- 位置に関する具体情報(地名・施設名・エリア・距離)が無いポスト(応援・感想・番組の感想だけ)は無視する。
- 憶測や沿道の伝聞でも「〜との情報」と分かる形で拾ってよいが、誇張しない。断定しすぎない。
- 個人の家・特定できる一般人の情報は書かない。ランナーの位置と公共の施設・地名のみ。
- 各エントリの time は「M/D HH:MM」形式。ポストの投稿時刻(JST)から推定。分からなければ現在時刻でよい。
- map_query は Googleマップで検索して正しい場所が出る日本語の地名/施設名(例「日産 駒沢店」「二子玉川駅」「府中市 郷土の森公園」)。エリアだけで施設が無ければ市区名+ランドマーク。地図が付けられないなら空文字。
- current_location は capbox に出す短いラベル。「世田谷区・駒沢エリア(休憩中)」のように 場所 + (走行中/休憩中/仮眠中 など) 。
- 新しい位置情報が無ければ update=false。

【新着ポスト】
{tweets_block}

【出力】次のJSONだけを出力。前後に説明文を付けない。
{{"update": true/false, "current_location": "...", "entries": [{{"time":"M/D HH:MM","text":"...","map_query":"..."}}], "reason":"..."}}
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


def _try_gemini(prompt, model, api_key):
    from google import genai

    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(model=model, contents=prompt)
    return _extract_json(resp.text)


def _normalize(d):
    d.setdefault("update", False)
    d.setdefault("current_location", "")
    d.setdefault("entries", [])
    d.setdefault("reason", "")
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
            gemini_model="gemini-flash-latest"):
    prompt = _build_prompt(runner, course_context, tweets, last_location)
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
