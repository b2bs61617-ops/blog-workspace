# -*- coding: utf-8 -*-
"""X投稿文の案出し(2026-11-14〜)。いまの型で案を出し、ルール違反の案は機械で落とす。

型(.claude/skills/publish/SKILL.md「Xの投稿文の作り方」と同じ。ルールが変わったらここも直す):
  - 答え(ブランド名・店名・場所・結論)は書かず、ヒントだけ
  - 「コメント欄」「こちら👇」などの誘導の一言は入れない。URLも入れない
  - 本文は約115字まで、タグ込みで重み280まで。ハッシュタグは2〜4個
  - @chomoand17(main)=女性ファン口調・くん付け / @chomotirend(trend)=楽しく緊迫感・くん付けしない

usage:
    python tools/xpost_ideas.py --site snowman --post-id 687 [--hide "ブランド名,店名"] [-n 5]
    python tools/xpost_ideas.py 記事.html --site trend --title "タイトル"
    python tools/xpost_ideas.py check --text "本文" --tags "#SnowMan #目黒蓮" [--hide "..."]   # 1案だけ調べる
外部AI(ai_hub)が使えないPCでは check だけ使える。Python 3.9対応。
"""
import html as htmllib
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

MAX_WEIGHT = 280
MAX_BODY_CHARS = 125  # 「約115字」に少しゆとりを持たせた上限
LEAD_WORDS = ("コメント欄", "コメ欄", "リプ欄", "リプライ欄", "リプに", "こちら", "コチラ", "👇", "⬇", "↓", "続きは", "詳細は",
              "詳しくは", "記事は", "記事で", "ブログで", "リンクは", "リンクから", "リンク先", "URL", "プロフィールから", "プロフから", "チェックして")
OVERUSED_OPENINGS = ("待って", "ねぇ", "ねえ")
TONE = {
    "main": ("女性ファンが自分でつぶやいている話し言葉にする。メンバーは「くん」付け。絵文字は1行に1〜3個。"
             "「致死量」「供給過多」「優勝」「破壊力えぐい」「沼確定」「反則」などのオタク語を1つ入れて熱量を出す(案ごとに言葉を変える)。"
             "書き出しは案ごとに全部変える。「待って」「ねぇ」で始めない。"),
    "trend": ("女性ファン口調にはしない(くん付けもしない)。楽しそうで、続きが気になる緊迫感のある短い文で畳みかける。"
              "1行目でいちばん気になる疑問・意外な事実をぶつける。絵文字は全体で1〜3個(🚨⚡😱🔥👀など)。"
              "予測は予測と分かる言い方にし、事実とちがう煽りはしない。"),
}


def weighted_length(text):
    """Xの文字数の数え方(ASCII=1、日本語・絵文字=2)。x_auto_post_buffer.weighted_length と同じ。"""
    return sum(1 if ord(c) < 0x80 else 2 for c in text)


def tag_list(tags):
    return [t for t in (tags or "").split() if t.startswith("#") and len(t) > 1]


def proper_nouns(tags, extra=()):
    """本文に1つは入っていてほしい固有名詞: ハッシュタグの言葉 + 名簿の名前 + 追加分。"""
    words = {t[1:] for t in tag_list(tags)} | {w for w in extra if w}
    try:
        import fact_check
        for conf in fact_check.load_groups().values():
            words |= {conf["label"]} | set(conf.get("aliases", []))
            for m in conf["members"]:
                words |= {m["name"], m.get("stage") or m["name"]}
    except Exception:  # noqa: BLE001
        pass
    return {w for w in words if len(w) >= 2}


def problems(text, tags, hide=(), names=()):
    """ルール違反の一覧(空なら合格)。"""
    bad = []
    text = (text or "").strip()
    if not text:
        return ["本文が空"]
    if re.search(r"https?://|www\.|\.(com|jp|net|blog|site)\b", text):
        bad.append("URLが入っている")
    hit = [w for w in LEAD_WORDS if w in text]
    if hit:
        bad.append("誘導の一言が入っている({})".format("・".join(hit)))
    if "#" in text or "＃" in text:
        bad.append("本文にハッシュタグが入っている(タグは別に渡す)")
    n = len(text.replace("\n", ""))
    if n > MAX_BODY_CHARS:
        bad.append("本文が長い({}字。約115字まで)".format(n))
    total = weighted_length(text + "\n\n" + (tags or "").strip())
    if total > MAX_WEIGHT:
        bad.append("タグ込みで重み{}(280まで。超えると本文が切られる)".format(total))
    tl = tag_list(tags)
    if not 2 <= len(tl) <= 4:
        bad.append("ハッシュタグが{}個(2〜4個にする)".format(len(tl)))
    if not any(w in text for w in proper_nouns(tags, names)):
        bad.append("固有名詞(人物名・グループ名・番組名)が本文に無い")
    leak = [h for h in hide if h and h in text]
    if leak:
        bad.append("答えを書いてしまっている({})".format("・".join(leak)))
    return bad


def notes(text):
    """違反ではないが気をつけたい点。"""
    out = []
    if text.strip().startswith(OVERUSED_OPENINGS):
        out.append("書き出しが「待って/ねぇ」(数本に1回まで)")
    return out


def article_text(html, limit=5000):
    s = re.sub(r"<!--.*?-->|<(script|style|iframe)\b.*?</\1>", "", html, flags=re.S)
    s = htmllib.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s).strip()[:limit]


def build_prompt(article, title="", account="main", n=5, hide=()):
    hide_line = ("\n- 次の言葉は記事の答えなので絶対に書かない: " + "、".join(hide)) if hide else ""
    return (
        "次のブログ記事を紹介するX(旧Twitter)の投稿文を{n}案作ってください。\n"
        "ルール:\n"
        "- 記事の肝心の答え(ブランド名・商品名・店名・場所・結論)は書かない。人物名・番組や場面・値段・色や形などの"
        "ヒントだけで「知りたい」と思わせる。ヒントは記事に書いてある事実だけ{hide}\n"
        "- 「コメント欄」「リプ欄」「こちら👇」「続きは」「詳細は」「記事は」などの誘導の言葉、URLは絶対に入れない\n"
        "- 本文は2〜3行・110字以内。人物名かグループ名を必ず入れる\n"
        "- {tone}\n"
        "- 最後の行にハッシュタグを2〜4個(グループ名・人物名・番組名。芸名があれば本名のタグも)。本文中には#を書かない\n"
        "- 案と案の間は「---」だけの行で区切る。前置き・番号・説明は書かない\n\n"
        "記事タイトル: {title}\n記事本文:\n{article}"
    ).format(n=n, hide=hide_line, tone=TONE.get(account, TONE["main"]), title=title, article=article)


def parse_candidates(ai_text):
    """AIの返事を (本文, タグ) の一覧にする。"""
    out = []
    for chunk in re.split(r"^\s*-{3,}\s*$", ai_text.strip(), flags=re.M):
        lines = [re.sub(r"^\s*(?:案\s*\d+[:：.]?|\d+[.)、:：]|[・*-])\s*", "", x).strip() for x in chunk.strip().splitlines()]
        lines = [x for x in lines if x and not x.startswith("```")]
        tags = [x for x in lines if x.startswith(("#", "＃"))]
        body = [x for x in lines if not x.startswith(("#", "＃"))]
        if body:
            out.append(("\n".join(body), " ".join(tags).replace("＃", "#")))
    return out


def generate(html, title="", account="main", n=5, hide=(), names=(), provider="auto"):
    """(合格した案, 落とした案) を返す。それぞれ dict(text, tags, problems, notes)。"""
    import ai_hub
    used, ans = ai_hub.call(build_prompt(article_text(html), title, account, n, hide), provider)
    ok, ng = [], []
    for text, tags in parse_candidates(ai_hub.strip_fences(ans)):
        item = {"text": text, "tags": tags, "problems": problems(text, tags, hide, names), "notes": notes(text),
                "weight": weighted_length(text + "\n\n" + tags)}
        (ng if item["problems"] else ok).append(item)
    return used, ok, ng


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="X投稿文の案出し")
    ap.add_argument("input", nargs="?", help="記事HTML、または check")
    ap.add_argument("--site")
    ap.add_argument("--post-id", type=int)
    ap.add_argument("--title", default="")
    ap.add_argument("--text")
    ap.add_argument("--tags", default="")
    ap.add_argument("--hide", default="")
    ap.add_argument("--names", default="")
    ap.add_argument("-n", type=int, default=5)
    ap.add_argument("--provider", default="auto")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    hide = [x.strip() for x in a.hide.split(",") if x.strip()]
    names = [x.strip() for x in a.names.split(",") if x.strip()]
    if a.input == "check":
        bad = problems(a.text or "", a.tags, hide, names)
        print("重み", weighted_length((a.text or "") + "\n\n" + a.tags), "/ 280")
        print("合格" if not bad else "NG: " + " / ".join(bad))
        for x in notes(a.text or ""):
            print("注意:", x)
        return 1 if bad else 0
    account, title = "main", a.title
    if a.site:
        import blogkit
        account = blogkit.site(a.site)["x_account"]
    if a.post_id:
        import blogkit
        po = blogkit.WP(a.site).get_post(a.post_id)
        html, title = po["content"]["raw"], title or po["title"]["raw"].replace("【未】", "")
    elif a.input:
        html = Path(a.input).read_text(encoding="utf-8")
    else:
        ap.error("記事ファイルか --post-id を指定する")
    used, ok, ng = generate(html, title, account, a.n, hide, names, a.provider)
    if a.json:
        print(json.dumps({"ai": used, "ok": ok, "ng": ng}, ensure_ascii=False, indent=2))
        return 0
    print("[{}] 合格 {}案 / 落とした案 {}".format(used, len(ok), len(ng)))
    for i, c in enumerate(ok, 1):
        print("\n--- 案{}(重み{}) ---\n{}\n{}".format(i, c["weight"], c["text"], c["tags"]))
        for x in c["notes"]:
            print("  注意:", x)
    for c in ng:
        print("\n(落とした: {})\n{}".format(" / ".join(c["problems"]), c["text"]))
    print("\n※ 外部AIの文なので、事実(値段・日付・名前)を記事と見くらべてから使うワン")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
