"""外部AIの共通窓口。マツ(Claude)のトークン節約のため、調査・翻訳・X投稿文の下書きを外部AIに任せる。

対応プロバイダ(.envにキーがあるものだけ使われる):
  gemini      GEMINI_API_KEY      無料枠(Flash系)。翻訳・要約・X投稿文の本命
  grok        XAI_API_KEY         console.x.ai。X内検索(research)ができる唯一の窓口。X Premiumとは別契約
  groq        GROQ_API_KEY        無料枠。速いが日本語はやや弱い。軽い要約向け
  openrouter  OPENROUTER_API_KEY  :free モデルは無料。DeepSeek/Qwen等の中国系モデルもここ経由で使う
                                  (中国企業の直APIはデータが中国国内に保存されるため使わない方針)
  mistral     MISTRAL_API_KEY     Experiment(無料)プラン。翻訳品質が高い。1分2回までなので連投は不可
  cerebras    CEREBRAS_API_KEY    無料枠(1日100万トークン)。とても速い
  tavily      TAVILY_API_KEY      AI用検索API(月1000回無料)。research でGrokが無いときの検索役

モデル名は各社がよく改廃するので .env の *_MODEL で上書きできる。

使い方(結果はファイル出力にすると、マツが長文を読まずに済む):
  python tools/ai_hub.py providers
  python tools/ai_hub.py ask "質問" [--provider gemini]
  python tools/ai_hub.py translate articles/x.html --to en -o articles/x_en.html
  python tools/ai_hub.py xpost articles/x.html
  python tools/ai_hub.py research "トレンド名" -o tmp_research.md
      # Grokがあれば X+Web を検索。無ければ Tavily で検索 → 他のAIで要約(X内の投稿は拾えない)
"""
import argparse
import json
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]

# auto のときに試す順番(無料で日本語に強い順)
AUTO_ORDER = ["gemini", "mistral", "openrouter", "grok", "cerebras", "groq"]

OPENAI_COMPAT = {
    # name: (base_url, key_env, model_env, default_model)
    "grok": ("https://api.x.ai/v1", "XAI_API_KEY", "GROK_MODEL", "grok-4-1-fast"),
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY", "GROQ_MODEL", "openai/gpt-oss-120b"),
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", "OPENROUTER_MODEL", "google/gemma-4-31b-it:free"),
    "mistral": ("https://api.mistral.ai/v1", "MISTRAL_API_KEY", "MISTRAL_MODEL", "mistral-large-latest"),
    "cerebras": ("https://api.cerebras.ai/v1", "CEREBRAS_API_KEY", "CEREBRAS_MODEL", "gpt-oss-120b"),
}
GEMINI_MODELS = ["gemini-flash-latest", "gemini-3.5-flash", "gemini-3.1-flash-lite"]

TRANSIENT = ("429", "500", "502", "503", "504", "UNAVAILABLE", "RESOURCE_EXHAUSTED",
             "DEADLINE_EXCEEDED", "overloaded", "timed out", "timeout")

LANG_NAMES = {"en": "English", "ko": "Korean (한국어)", "kr": "Korean (한국어)", "ja": "Japanese"}


def load_env(path=None):
    env = {}
    f = Path(path) if path else ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def available_providers(env):
    out = []
    if env.get("GEMINI_API_KEY"):
        out.append("gemini")
    for name, (_, key_env, _, _) in OPENAI_COMPAT.items():
        if env.get(key_env):
            out.append(name)
    return out


def resolve_order(provider, env):
    avail = available_providers(env)
    if provider == "auto":
        order = [p for p in AUTO_ORDER if p in avail]
    else:
        order = [provider] if provider in avail else []
    if not order:
        raise SystemExit(f"使えるプロバイダがありません(指定={provider}, .envで有効={avail or 'なし'})")
    return order


def is_transient(msg):
    return any(s in msg for s in TRANSIENT)


def _call_gemini(prompt, env, system=None):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=env["GEMINI_API_KEY"], http_options=types.HttpOptions(timeout=120000))
    models = [env.get("GEMINI_MODEL") or GEMINI_MODELS[0]] + GEMINI_MODELS
    cfg = types.GenerateContentConfig(system_instruction=system) if system else None
    last = None
    for m in dict.fromkeys(models):
        try:
            return client.models.generate_content(model=m, contents=prompt, config=cfg).text
        except Exception as e:  # noqa: BLE001
            last = e
            if not (is_transient(str(e)) or "404" in str(e) or "NOT_FOUND" in str(e)):
                raise
    raise RuntimeError(f"gemini 全モデル失敗: {last}")


def _call_openai_compat(name, prompt, env, system=None):
    base, key_env, model_env, default_model = OPENAI_COMPAT[name]
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    r = requests.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {env[key_env]}", "Content-Type": "application/json"},
        json={"model": env.get(model_env) or default_model, "messages": messages},
        timeout=180,
    )
    if r.status_code != 200:
        raise RuntimeError(f"{name} HTTP {r.status_code}: {r.text[:300]}")
    return r.json()["choices"][0]["message"]["content"]


def call(prompt, provider="auto", env=None, system=None):
    """プロバイダを順に試し、(使ったプロバイダ名, 応答テキスト)を返す。"""
    env = env if env is not None else load_env()
    errors = []
    for p in resolve_order(provider, env):
        for attempt in range(2):
            try:
                text = _call_gemini(prompt, env, system) if p == "gemini" else _call_openai_compat(p, prompt, env, system)
                return p, text
            except Exception as e:  # noqa: BLE001
                errors.append(f"{p}: {e}")
                if attempt == 0 and is_transient(str(e)):
                    time.sleep(5)
                    continue
                break
    raise RuntimeError("全プロバイダ失敗\n" + "\n".join(errors))


RESEARCH_TASK = (
    "1. Xやネットで多い疑問(「？」付きのもの)を最大5つ\n"
    "2. それぞれの答え(分かっている事実)と出典URL\n"
    "3. 答えが確認できないものは「未確認」と書き、有力な予想があれば「予想:」として添える\n"
    "日本語の箇条書きで、全体1500字以内。前置き不要。"
)


def tavily_search(query, env, max_results=8, **opts):
    r = requests.post(
        "https://api.tavily.com/search",
        headers={"Authorization": f"Bearer {env['TAVILY_API_KEY']}", "Content-Type": "application/json"},
        json={"query": query, "max_results": max_results, "search_depth": "basic", "include_answer": False, **opts},
        timeout=60,
    )
    if r.status_code != 200:
        raise RuntimeError(f"tavily HTTP {r.status_code}: {r.text[:300]}")
    return r.json().get("results", [])


def format_sources(results, per_item=1200):
    blocks = []
    for i, x in enumerate(results, 1):
        blocks.append(f"[{i}] {x.get('title', '')}\nURL: {x.get('url', '')}\n{(x.get('content') or '')[:per_item]}")
    return "\n\n".join(blocks)


def merge_results(*lists):
    """URLの重複を除いて順に結合する。"""
    seen, out = set(), []
    for lst in lists:
        for x in lst:
            if x.get("url") and x["url"] not in seen:
                seen.add(x["url"])
                out.append(x)
    return out


def tavily_research(topic, env, provider="auto"):
    """Tavilyで検索し、結果を他のAIに要約させる(Grokが無いときの無料ルート)。
    直近1週間のニュース + 一般検索(X投稿・Instagram等も拾える)の2回=2クレジット使う。"""
    results = merge_results(
        tavily_search(topic, env, 6, topic="news", days=7),
        tavily_search(topic, env, 6, topic="general"),
    )
    if not results:
        return "tavily", "検索結果なし"
    prompt = (
        f"話題「{topic}」について、以下の検索結果だけを根拠にまとめて。検索結果に無いことは書かない。\n"
        + RESEARCH_TASK + "\n出典URLは検索結果のURLをそのまま使う。\n\n" + format_sources(results)
    )
    used, text = call(prompt, provider, env)
    return f"tavily+{used}", text


def research(topic, env=None, provider="auto"):
    env = env if env is not None else load_env()
    if env.get("XAI_API_KEY"):
        return "grok", grok_research(topic, env)
    if env.get("TAVILY_API_KEY"):
        return tavily_research(topic, env, provider)
    raise SystemExit("research には XAI_API_KEY か TAVILY_API_KEY が必要です")


def grok_research(topic, env=None):
    """Grok(xAI)のサーバー側ツールでX+Webを検索させ、Xで出ている疑問と答えを出典付きで返す。"""
    env = env if env is not None else load_env()
    if not env.get("XAI_API_KEY"):
        raise SystemExit("XAI_API_KEY が .env にありません(console.x.ai で発行。X Premiumとは別契約)")
    prompt = (
        f"Xの速報トレンド「{topic}」について調べて。\n"
        "1. Xの投稿で多い疑問(「？」付きのもの)を最大5つ\n"
        "2. それぞれの答え(分かっている事実)と出典URL(X投稿URLまたはニュースURL)\n"
        "3. 答えが確認できないものは「未確認」と書き、有力な予想があれば「予想:」として添える\n"
        "日本語の箇条書きで、全体1500字以内。前置き不要。"
    )
    r = requests.post(
        "https://api.x.ai/v1/responses",
        headers={"Authorization": f"Bearer {env['XAI_API_KEY']}", "Content-Type": "application/json"},
        json={
            "model": env.get("GROK_MODEL") or OPENAI_COMPAT["grok"][3],
            "input": [{"role": "user", "content": prompt}],
            "tools": [{"type": "x_search"}, {"type": "web_search"}],
        },
        timeout=300,
    )
    if r.status_code != 200:
        raise RuntimeError(f"grok research HTTP {r.status_code}: {r.text[:300]}")
    return extract_response_text(r.json())


def extract_response_text(data):
    """Responses API形式の応答から本文テキストだけを取り出す。"""
    if data.get("output_text"):
        return data["output_text"]
    parts = []
    for item in data.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") in ("output_text", "text") and c.get("text"):
                    parts.append(c["text"])
    return "\n".join(parts)


def translate_prompt(text, lang):
    target = LANG_NAMES.get(lang, lang)
    return (
        f"Translate the following Japanese blog article into natural {target} for K-POP/J-POP fans.\n"
        "Rules:\n"
        "- Keep ALL HTML tags, attributes, URLs, shortcodes and WordPress block comments (<!-- wp:... -->) exactly as they are. Translate only human-readable text (including alt text).\n"
        "- Keep person names in their commonly used romanization / Hangul spelling.\n"
        "- Output only the translated content. No explanations, no code fences.\n\n"
        f"{text}"
    )


def xpost_prompt(text):
    return (
        "以下のブログ記事を告知するX投稿文を3案作って。\n"
        "ルール: 女性ファンの話し言葉(「〜すぎて無理😭💕」系)で絵文字多め、メンバーはくん付け、"
        "本文は約115字以内(URLとハッシュタグ除く)。ハッシュタグはステージネームに加えて本名も併記"
        "(例 #ISSA #柳谷伊冴)。各案を「---」で区切り、前置き不要。\n\n"
        f"{text[:6000]}"
    )


def strip_fences(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip()


def _emit(text, out, used):
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"[{used}] {len(text)}文字 → {out}")
    else:
        print(f"[{used}]\n{text}")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="外部AI共通窓口")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("providers")
    for name in ("ask", "translate", "xpost", "research"):
        s = sub.add_parser(name)
        s.add_argument("input", help="ask=質問文 / research=トピック / translate・xpost=ファイルパス")
        s.add_argument("--provider", default="auto")
        s.add_argument("-o", "--out")
        if name == "translate":
            s.add_argument("--to", required=True, help="en / ko")
    a = ap.parse_args(argv)
    env = load_env()

    if a.cmd == "providers":
        avail = available_providers(env)
        for p in ["gemini", *OPENAI_COMPAT]:
            print(f"{p:11s} {'OK' if p in avail else '未設定'}")
        print(f"{'tavily':11s} {'OK' if env.get('TAVILY_API_KEY') else '未設定'}  (検索専用)")
        return
    if a.cmd == "research":
        used, text = research(a.input, env, a.provider)
        _emit(text, a.out, used)
        return
    if a.cmd == "ask":
        used, text = call(a.input, a.provider, env)
    else:
        src = Path(a.input).read_text(encoding="utf-8")
        prompt = translate_prompt(src, a.to) if a.cmd == "translate" else xpost_prompt(src)
        used, text = call(prompt, a.provider, env)
        text = strip_fences(text)
    _emit(text, a.out, used)


if __name__ == "__main__":
    main()
