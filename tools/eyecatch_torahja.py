"""Travis Japan専門ブログ(chomoand-4.blog)用アイキャッチ生成ツール.

eyecatch_chomoand0.py の後継(トラジャ向け)。記事タイトルは要約せず全文をそのまま載せる
(feedback: タイトルそのまま+大きく)。そのうえで見た目だけを作り込む:

- KO1KEYZ統一テンプレと同じ極太丸ゴシック(M PLUS Rounded 1c Black)
- 改行は日本語の文節単位(Intl.Segmenter)。「飾ら/れてる」「Travis/Japan」のような泣き別れをしない
- 先頭の【...】は上部のバッジに出す(文字は省略せず、置き場所だけ変える)
- タイトル中のメンバー名はメンバーカラーのマーカーで強調
- 背景は3種類: light(明るいスモーク) / stage(暗いステージライト) / elegant(淡いグラデーション+細字セリフ調、2026-09-22〜)

使い方:
    python tools/eyecatch_torahja.py \
        --title "【Travis Japan】ガンバ大阪にサインが飾られてる理由は?" \
        --color-key "松田元太" --style stage \
        --out images/xxx_eyecatch.png
"""

from __future__ import annotations

import argparse
import html as html_mod
import json
import random
import re
import tempfile
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

CANVAS_W = 1200
CANVAS_H = 630
REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = REPO_ROOT / "assets" / "fonts" / "MPLUSRounded1c-Black.ttf"
FONT_ELEGANT_LIGHT = REPO_ROOT / "assets" / "fonts" / "NotoSerifJP-Light.ttf"
FONT_ELEGANT_REGULAR = REPO_ROOT / "assets" / "fonts" / "NotoSerifJP-Medium.ttf"

POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt/"
POLLINATIONS_MODEL = "flux"
POLLINATIONS_TIMEOUT_SEC = 45
# Pollinations.aiは無料利用だと nologo=true を付けても右下に "pollinations.ai" のロゴが焼き込まれる。
# 表示キャンバスより一回り大きく生成し、CSS側でロゴが写る右下だけ画面外にはみ出させて隠す。
BG_OVERSCAN_W = 220
BG_OVERSCAN_H = 70

# (メイン色, 明るい版で使う淡色) — 公式カラーを「きれいに映える濃さ」に調整
COLORS: dict[str, tuple[str, str]] = {
    "宮近海斗": ("#ff4d63", "#ffb3bd"),  # 赤
    "中村海人": ("#22c977", "#a6ecc8"),  # 緑
    "七五三掛龍也": ("#ff6eb4", "#ffc2e0"),  # ピンク
    "川島如恵留": ("#c3cbe0", "#e6eaf4"),  # 白(シルバー)
    "吉澤閑也": ("#ffd21f", "#fff0a0"),  # 黄
    "松田元太": ("#3d8bff", "#b2d2ff"),  # 青
    "松倉海斗": ("#ff9424", "#ffd2a0"),  # オレンジ
    "group": ("#a487cf", "#d9c9f0"),  # グループカラー(紫)
}
GROUP_PURPLE = "#7c4dff"

# AI背景生成プロンプトで使う色の英語名(メンバーカラーの雰囲気を背景に反映するため)
MEMBER_COLOR_WORDS: dict[str, str] = {
    "宮近海斗": "red",
    "中村海人": "green",
    "七五三掛龍也": "pink",
    "川島如恵留": "silver white",
    "吉澤閑也": "yellow",
    "松田元太": "blue",
    "松倉海斗": "orange",
    "group": "purple",
}

BADGE_RE = re.compile(r"^【([^】]+)】\s*")


def split_badge(title: str) -> tuple[str, str]:
    """先頭の【...】をバッジ文言と本文に分ける(なければバッジ無し)."""
    m = BADGE_RE.match(title.strip())
    if not m:
        return "", title.strip()
    return m.group(1), title.strip()[m.end():]


GROUP_WORD_RE = re.compile(r"Travis\s*Japan|トラビスジャパン|トラジャ", re.IGNORECASE)
GROUP_BRACKET_RE = re.compile(r"[【\[(（]\s*(?:Travis\s*Japan|トラビスジャパン|トラジャ)\s*[】\])）]", re.IGNORECASE)
LEADING_JUNK_RE = re.compile(r"^[のがはをにでともへ、。・\s　]+")


def _shade(hex_color: str, amount: float) -> str:
    """#rrggbb を黒に向けて amount(0〜1) だけ暗くする."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return "#{:02x}{:02x}{:02x}".format(*(round(c * (1 - amount)) for c in (r, g, b)))


def build_bg_prompt(color_key: str, style: str) -> str:
    """メンバーカラーとstyle(light/stage/elegant)から背景生成プロンプトを組み立てる(顔・人物は描かせない)."""
    color_word = MEMBER_COLOR_WORDS.get(color_key, "purple")
    if style == "stage":
        return (
            f"abstract concert stage background, glowing {color_word} spotlight beams and "
            "bokeh light particles, dark navy gradient, atmospheric fog, empty stage with "
            "absolutely no people and no faces, no text, no logo, blog banner background, "
            "cinematic lighting, non-photorealistic digital art"
        )
    if style == "elegant":
        return (
            f"elegant watercolor floral border frame, delicate {color_word} flowers and "
            "leaves clustered densely along the four edges and corners only, vast plain "
            "white empty space filling the center, botanical watercolor illustration, "
            "blog banner background, no people, no faces, no text, no logo"
        )
    return (
        f"soft pastel {color_word} watercolor gradient background, gentle glowing light orbs, "
        "airy bright atmosphere, empty space with absolutely no people and no faces, no text, "
        "no logo, blog banner background, non-photorealistic flat illustration style"
    )


def build_pollinations_url(prompt: str, seed: int) -> str:
    """Pollinations.aiのリクエストURLを組み立てる(副作用なし)。
    ロゴを画面外に逃がすため、表示サイズよりBG_OVERSCAN分だけ大きく要求する。"""
    encoded_prompt = urllib.parse.quote(prompt)
    query = urllib.parse.urlencode({
        "width": CANVAS_W + BG_OVERSCAN_W,
        "height": CANVAS_H + BG_OVERSCAN_H,
        "model": POLLINATIONS_MODEL,
        "seed": seed,
        "nologo": "true",
    })
    return f"{POLLINATIONS_BASE_URL}{encoded_prompt}?{query}"


def generate_ai_background(prompt: str, seed: int) -> bytes:
    """Pollinations.ai(APIキー不要・無料)で背景を1枚生成する.
    既定のPython-urllib User-Agentは403で弾かれるため、ブラウザ相当のUser-Agentを付ける。"""
    url = build_pollinations_url(prompt, seed)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=POLLINATIONS_TIMEOUT_SEC) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Pollinations.aiがHTTP {resp.status}を返した")
        return resp.read()


def resolve_ai_background(use_ai: bool, color_key: str, style: str, seed: int | None) -> Path | None:
    """AI背景の一時ファイルパスを返す。無効化・生成失敗時はNone(=CSSグラデーションのみで描画)。"""
    if not use_ai:
        return None
    try:
        prompt = build_bg_prompt(color_key, style)
        image_bytes = generate_ai_background(prompt, seed if seed is not None else random.randint(0, 2**31 - 1))
        if not image_bytes:
            raise RuntimeError("Pollinations.aiから画像データが返らなかった")
        tmp_path = Path(tempfile.gettempdir()) / f"torahja_ai_bg_{uuid.uuid4().hex}.jpg"
        tmp_path.write_bytes(image_bytes)
        print(f"AI背景生成: {tmp_path}")
        return tmp_path
    except Exception as e:
        print(f"AI背景生成失敗({type(e).__name__}: {e})、CSSグラデーション背景にフォールバック")
        return None


# タイトル中のメンバー呼称(フルネーム・名字・他メンバーと被らない名前)。「海斗」は2人いるので含めない
MEMBER_ALIASES: dict[str, tuple[str, ...]] = {
    "宮近海斗": ("宮近海斗", "宮近"),
    "中村海人": ("中村海人", "中村", "海人"),
    "七五三掛龍也": ("七五三掛龍也", "七五三掛", "龍也"),
    "川島如恵留": ("川島如恵留", "川島", "如恵留"),
    "吉澤閑也": ("吉澤閑也", "吉澤", "閑也"),
    "松田元太": ("松田元太", "松田", "元太", "げんた"),
    "松倉海斗": ("松倉海斗", "松倉"),
}


def detect_color_key(title: str) -> str:
    """タイトルからメンバーカラーを決める.

    メンバーが1人だけ登場すればそのメンバー、誰も居ない/複数人ならグループ(紫)。
    """
    found = [name for name, aliases in MEMBER_ALIASES.items() if any(a in title for a in aliases)]
    return found[0] if len(found) == 1 else "group"


def strip_group_name(title: str) -> str:
    """タイトルから「Travis Japan」「トラジャ」を省略する(3行デザインのルール②).

    【Travis Japan】のように括弧だけで囲まれていれば括弧ごと消し、
    「トラジャの◯◯」のように消したあと頭に残る助詞(の/が/は…)も落とす。
    """
    t = GROUP_BRACKET_RE.sub("", title.strip())
    # 文頭・「】」直後のグループ名は、続く助詞(の/が/は…)ごと消す(「【開幕戦】Travis Japanが履いた靴」→「【開幕戦】履いた靴」)
    t = re.sub(rf"(^|】)[ 　]*(?:{GROUP_WORD_RE.pattern})[のがはをにでともへ]*", lambda m: m.group(1), t, flags=re.IGNORECASE)
    t = GROUP_WORD_RE.sub("", t)
    return LEADING_JUNK_RE.sub("", t).strip()


def parse_split(title: str, split: str) -> list[str]:
    """--split "1行目|2行目|3行目" を検証して3行に分ける.

    ルール①(タイトルをそのまま使う)を守るため、3行をつなげたものが
    (グループ名を省略した)タイトルと一致しなければエラーにする。
    """
    parts = [p.strip() for p in split.split("|")]
    if len(parts) != 3 or not all(parts):
        raise ValueError(f"--split は「1行目|2行目|3行目」の3つ(空なし)で指定: {split!r}")
    squash = lambda s: re.sub(r"\s+", "", s)
    if squash("".join(parts)) != squash(title):
        raise ValueError(
            "3行をつなげるとタイトル(グループ名省略後)と一致しない。\n"
            f"  タイトル: {title}\n  3行結合 : {''.join(parts)}"
        )
    return parts


def _script_block(body: str, mark: str, badge_html: str) -> str:
    """従来の全文1ブロック用スクリプト(文節改行+自動フィット)."""
    return f"""<script>
const BODY = {json.dumps(body, ensure_ascii=False)};
const MARK = {json.dumps(mark, ensure_ascii=False)};
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
// 改行してよい位置を決める(Intl.Segmenterは「飾ら|れて」のように割るため、ルールベースにした):
//  ・記号の後 ・「名詞+助詞(は/が/を/に/で/と/も/の/へ)」の後 ・かな/漢字/カナ/英数の文字種の境目
const chars = [...BODY];
const HIRA = /[\\u3040-\\u309f]/, KATA = /[\\u30a0-\\u30ff]/, KANJI = /[\\u4e00-\\u9fff々]/, LATIN = /[A-Za-z0-9]/;
const PARTICLES = 'はがをにでともへの', END_MARKS = '!?！？。、';
const markAt = MARK ? BODY.indexOf(MARK) : -1, markEnd = markAt + MARK.length;
function canBreakAfter(i) {{
  if (i >= chars.length - 1) return false;
  if (markAt >= 0 && i >= markAt && i < markEnd - 1) return false; // メンバー名の途中では切らない
  const c = chars[i], n = chars[i + 1];
  if (END_MARKS.includes(n)) return false;
  if ('、。！？!?・ 　」』）】'.includes(c)) return true;
  if ('「『（【'.includes(n)) return true;
  if (PARTICLES.includes(c)) {{
    if (PARTICLES.includes(n)) return false; // には/とは など連続助詞は最後で切る
    let j = i; while (j >= 0 && PARTICLES.includes(chars[j])) j--;
    return j < 0 || !HIRA.test(chars[j]); // 直前が漢字/カナ/英数のときだけ(「食べたもの」の「も」では切らない)
  }}
  const cls = ch => KANJI.test(ch) ? 'k' : KATA.test(ch) ? 'a' : HIRA.test(ch) ? 'h' : LATIN.test(ch) ? 'l' : 'o';
  const a = cls(c), b = cls(n);
  if (a === b) return false;
  if (a === 'a' && b === 'h') return false; // 「サイン|した」のような送り仮名は切らない
  if (a === 'k' && b === 'h') return false; // 「飾|られ」
  return a !== 'o' && b !== 'o';
}}
const units = []; let cur = '', curStart = 0;
chars.forEach((ch, i) => {{
  cur += ch;
  if (canBreakAfter(i)) {{ units.push([cur, curStart]); cur = ''; curStart = i + 1; }}
}});
if (cur) units.push([cur, curStart]);
// 単位ごとにnowrapのspanで包み、メンバー名だけmarkで強調(1つのmarkにまとめて隙間を出さない)
let out = '';
for (const [text, start] of units) {{
  let html = '', buf = '', inMark = false;
  [...text].forEach((ch, k) => {{
    const m = markAt >= 0 && start + k >= markAt && start + k < markEnd;
    if (m !== inMark) {{ html += inMark ? '<mark>' + esc(buf) + '</mark>' : esc(buf); buf = ''; inMark = m; }}
    buf += ch;
  }});
  html += inMark ? '<mark>' + esc(buf) + '</mark>' : esc(buf);
  out += '<span class="w">' + html + '</span>';
}}
const t = document.getElementById('t');
t.innerHTML = out;
document.fonts.ready.then(() => {{
  const badgeEl = document.querySelector('.badge');
  const maxH = {CANVAS_H} - 2 * 60 - (badgeEl ? badgeEl.getBoundingClientRect().height + 26 : 0);
  let size = 170;
  t.style.fontSize = size + 'px';
  while (size > 30 && (t.getBoundingClientRect().height > maxH ||
         [...t.querySelectorAll('.w')].some(w => w.getBoundingClientRect().width > 1060))) {{
    size -= 2; t.style.fontSize = size + 'px';
  }}
  document.body.dataset.fitted = '1';
}});
</script>"""


def _script_3line(elegant: bool = False) -> str:
    """3行デザイン用スクリプト: 画面いっぱいに使う.

    1・3行目は大きな文字(基準112px)、2行目は特大(基準230px)+縦に引き伸ばす。
    行が横幅に収まらないときは、まず横だけ詰め(縦長の文字にする)、それでも足りなければ文字を小さくする。
    elegant=Trueのときは、極太ゴシック用のサイズだと重すぎるため基準サイズを一回り小さくする。
    """
    max1 = 117 if elegant else 112
    max2 = 132 if elegant else 230
    return f"""<script>
document.fonts.ready.then(() => {{
  const [l1, l2, l3] = ['l1', 'l2', 'l3'].map(id => document.getElementById(id));
  const FIT_W = 1130, USABLE_H = 560, GAP = 40;
  // 文字サイズ(max)で並べ、幅超過なら横を詰める(minSx まで)。それでも超えるなら文字自体を小さくする
  const fit = (el, max, minSx, growSx = 1) => {{
    el.style.fontSize = max + 'px';
    const w = el.getBoundingClientRect().width;
    let size = max, sx = 1;
    if (w < FIT_W) sx = Math.min(growSx, FIT_W / w);  // 短い行は横にも伸ばして画面を使う(growSx>1のときだけ)
    if (w > FIT_W) {{
      sx = FIT_W / w;
      if (sx < minSx) {{ size = Math.floor(max * FIT_W / (w * minSx)); sx = minSx; }}
    }}
    el.style.fontSize = size + 'px';
    el.dataset.sx = sx; el.dataset.sy = 1;
    return size;
  }};
  const h1 = fit(l1, {max1}, 0.62), h3 = fit(l3, {max1}, 0.62);
  const h2 = fit(l2, {max2}, 0.7, 1.3);
  // 残りの高さを2行目の縦伸ばしで使い切る(最大1.7倍)。elegantは縦長にせず等倍のまま
  const sy = {"1" if elegant else "Math.max(1, Math.min(1.7, (USABLE_H - h1 - h3 - GAP * 2) / h2))"};
  l2.dataset.sy = sy;
  for (const el of [l1, l2, l3]) {{
    const size = parseFloat(el.style.fontSize), sy2 = parseFloat(el.dataset.sy);
    el.style.transform = `scale(${{el.dataset.sx}}, ${{sy2}})`;
    el.style.margin = (size * (sy2 - 1) / 2) + 'px 0';  // 縦に伸ばした分の場所を確保
  }}
  document.querySelector('.stage').style.gap = GAP + 'px';
  document.body.dataset.fitted = '1';
}});
</script>"""


def build_html(
    title: str,
    color_key: str = "group",
    style: str = "stage",
    lines: list[str] | None = None,
    bg_path: Path | None = None,
) -> str:
    """lines(3要素)を渡すと3行デザイン(2行目を最大・マーカー強調)、なければ従来の全文1ブロック."""
    if color_key not in COLORS:
        raise ValueError(f"unknown color_key: {color_key!r} (known: {', '.join(COLORS)})")
    if style not in ("light", "stage", "elegant"):
        raise ValueError("style must be 'light', 'stage' or 'elegant'")
    main, tint = COLORS[color_key]
    badge, body = split_badge(title)
    # メンバー名(color-key)が本文にあれば強調対象にする
    mark = color_key if color_key != "group" and color_key in body else ""
    elegant = style == "elegant"
    font_url = FONT_ELEGANT_LIGHT.as_uri() if elegant else FONT_PATH.as_uri()
    font_url_regular = FONT_ELEGANT_REGULAR.as_uri()
    badge_html = f'<div class="badge">{html_mod.escape(badge)}</div>' if badge else ""
    dark = style == "stage"
    theme_css = ""
    if lines and dark and color_key != "group":
        # メンバー記事: 背景全体をそのメンバーカラーにする(グループ記事は従来の紫のステージ)。
        # 白文字が読めるよう、公式色を少し暗くしたグラデーションにし、2行目の帯は同色の濃い版にする
        deep, mid = _shade(main, 0.6), _shade(main, 0.3)
        theme_css = f"""
.stage {{ background: linear-gradient(135deg, {deep} 0%, {mid} 50%, {deep} 100%); }}
.g1 {{ background: {main}; opacity: 0.6; }}
.g2 {{ background: {main}; opacity: 0.4; }}
.g3 {{ background: #fff; opacity: 0.14; }}
.l2 {{ background: linear-gradient(transparent 60%, {_shade(main, 0.62)}d9 60%, {_shade(main, 0.62)}d9 93%, transparent 93%); }}
.l1::before, .l1::after, .l3::before, .l3::after {{ background: #fff; box-shadow: 0 0 12px #fff; opacity: 0.85; }}
"""
    elif lines and dark:
        # グループ記事(紫): 帯だけメンバー記事と同じく濃い色にして、白文字のコントラストを揃える
        theme_css = f"""
.l2 {{ background: linear-gradient(transparent 60%, #6a3fdbe6 60%, #6a3fdbe6 93%, transparent 93%); }}
"""
    elif lines and elegant:
        # エレガント版: ビビッドな色ブロックではなく、メンバー(またはグループ紫)の淡い水彩背景+細い下線で控えめに強調
        theme_css = f"""
.stage {{ background: linear-gradient(135deg, #ffffff 0%, {tint} 55%, #ffffff 100%); }}
.blob {{ position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.4; }}
.eb1 {{ width: 620px; height: 620px; left: -220px; top: -260px; background: {tint}; }}
.eb2 {{ width: 560px; height: 560px; right: -200px; bottom: -240px; background: {main}; opacity: 0.22; }}
.eb3 {{ width: 420px; height: 420px; left: 34%; top: 20%; background: #ffffff; opacity: 0.45; }}
.l {{ color: #3a3532; text-shadow: none; }}
.l1, .l3 {{ letter-spacing: 0.12em; opacity: 0.82; font-family: 'Mincho'; font-weight: 300; }}
.l2 {{ letter-spacing: 0.03em; padding: 0 4px 14px; background: none; border-bottom: 2px solid {main}; font-family: 'Mincho'; font-weight: 300; color: #2c2622; }}
.l1::before, .l1::after, .l3::before, .l3::after {{ display: none; }}
"""
    if lines:
        badge_html = ""
        title_html = "".join(
            f'<div class="l l{i}" id="l{i}">{html_mod.escape(text)}</div>'
            for i, text in enumerate(lines, start=1)
        )
        script = _script_3line(elegant)
    else:
        title_html = '<div class="title" id="t"></div>'
        script = _script_block(body, mark, badge_html)

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
@font-face {{ font-family: '{"Mincho" if elegant else "Rounded"}'; src: url('{font_url}') format('truetype'); font-weight: {300 if elegant else 900}; }}
{f"@font-face {{ font-family: 'Mincho'; src: url('{font_url_regular}') format('truetype'); font-weight: 400; }}" if elegant else ""}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: {CANVAS_W}px; height: {CANVAS_H}px; overflow: hidden; font-family: '{"Mincho" if elegant else "Rounded"}', 'Yu Gothic', sans-serif; font-weight: {300 if elegant else 900}; }}
.stage {{ width: {CANVAS_W}px; height: {CANVAS_H}px; position: relative; overflow: hidden;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 26px;
  background: {"linear-gradient(135deg,#12082b 0%,#2a1160 55%,#150a33 100%)" if dark else "#f6f2fb"}; }}
.glow {{ position: absolute; border-radius: 50%; filter: blur({70 if dark else 60}px); }}
.g1 {{ width: 640px; height: 640px; right: -140px; top: -200px; background: {main}; opacity: {0.55 if dark else 0.75}; }}
.g2 {{ width: 560px; height: 560px; left: -170px; bottom: -230px; background: {GROUP_PURPLE if dark else tint}; opacity: {0.6 if dark else 0.8}; }}
.g3 {{ width: 380px; height: 380px; left: 36%; top: 30%; background: {"#ffffff" if dark else tint}; opacity: {0.10 if dark else 0.5}; }}
.beam {{ position: absolute; top: -120px; width: 200px; height: 900px; opacity: {0.13 if dark else 0}; filter: blur(14px);
  background: linear-gradient(to bottom, #fff, transparent 85%); transform-origin: top center; }}
.b1 {{ left: 240px; transform: rotate(24deg); }} .b2 {{ left: 620px; transform: rotate(-16deg); }} .b3 {{ left: 900px; transform: rotate(30deg); }}
.dot {{ position: absolute; border-radius: 50%; background: #fff; opacity: {0.7 if dark else 0}; box-shadow: 0 0 10px #fff; }}
.frame {{ position: absolute; inset: 18px; border: {"1px solid rgba(60,50,60,0.16)" if elegant else f"3px solid {'rgba(255,255,255,0.28)' if dark else 'rgba(255,255,255,0.9)'}"}; border-radius: {6 if elegant else 26}px; }}
.ai-bg {{ position: absolute; top: 0; left: 0; width: {CANVAS_W + BG_OVERSCAN_W}px; height: {CANVAS_H + BG_OVERSCAN_H}px; z-index: 0; }}
.scrim {{ position: absolute; inset: 0; z-index: 0;
  background: {"rgba(255,255,255,0.1)" if elegant else ("linear-gradient(135deg, rgba(18,8,43,0.55) 0%, rgba(42,17,96,0.68) 55%, rgba(21,10,51,0.72) 100%)" if dark else "rgba(246,242,251,0.62)")}; }}
.badge {{ position: relative; z-index: 2; font-size: 44px; letter-spacing: 0.06em; padding: 8px 34px 10px; border-radius: 999px;
  color: {"#fff" if dark else "#fff"}; background: {main if dark else "#2b1a55"}; {"color:#1b1030;" if dark and color_key in ("吉澤閑也","川島如恵留") else ""}
  box-shadow: 0 6px 24px {main}88; }}
.title {{ position: relative; z-index: 2; width: 1060px; text-align: center; line-height: 1.22; letter-spacing: 0.02em;
  color: {"#2c2622" if elegant else ("#fff" if dark else "#1c1c1c")}; text-wrap: balance;
  text-shadow: {"0 1px 3px rgba(0,0,0,0.08)" if elegant else ("0 0 24px rgba(20,8,50,.85), 0 3px 0 rgba(20,8,50,.5)" if dark else "0 0 14px rgba(255,255,255,.9)")}; }}
.title .w {{ white-space: nowrap; }}
.title mark {{ color: inherit; background: linear-gradient(transparent 58%, {main if dark else tint} 58%, {main if dark else tint} 94%, transparent 94%);
  padding: 0 4px; {"text-shadow: 0 0 24px rgba(20,8,50,.85);" if dark else ""} }}
/* 3行デザイン: 1・3行目は控えめ、2行目だけ特大+メンバーカラーのマーカー */
.l {{ position: relative; z-index: 2; white-space: nowrap; text-align: center; line-height: 1;
  color: {"#fff" if dark else "#1c1c1c"};
  text-shadow: {"0 0 22px rgba(20,8,50,.9), 0 3px 0 rgba(20,8,50,.45)" if dark else "0 0 14px rgba(255,255,255,.9)"}; }}
.l1, .l3 {{ letter-spacing: 0.05em; opacity: 0.94; }}
.l2 {{ letter-spacing: 0.01em; padding: 0 22px;
  background: linear-gradient(transparent 60%, {main if dark else tint} 60%, {main if dark else tint} 93%, transparent 93%); }}
.l1::before, .l1::after, .l3::before, .l3::after {{ content: ''; display: inline-block; width: 32px; height: 5px; border-radius: 3px;
  vertical-align: middle; margin: 0 12px; background: {main}; box-shadow: 0 0 12px {main}; }}
{theme_css}
</style>
</head>
<body>
<div class="stage">
  {f'<img class="ai-bg" src="{bg_path.resolve().as_uri()}"><div class="scrim"></div>' if bg_path else ""}
  {"" if elegant else '<div class="glow g1"></div><div class="glow g2"></div><div class="glow g3"></div><div class="beam b1"></div><div class="beam b2"></div><div class="beam b3"></div><div class="dot" style="left:96px;top:70px;width:9px;height:9px"></div><div class="dot" style="left:1040px;top:120px;width:7px;height:7px"></div><div class="dot" style="left:180px;top:540px;width:6px;height:6px"></div><div class="dot" style="left:1110px;top:500px;width:10px;height:10px"></div><div class="dot" style="left:600px;top:44px;width:5px;height:5px"></div>'}
  {'<div class="blob eb1"></div><div class="blob eb2"></div><div class="blob eb3"></div>' if (elegant and not bg_path) else ""}
  <div class="frame"></div>
  {badge_html}
  {title_html}
</div>
{script}
</body>
</html>
"""


def render(html_text: str, out_path: Path) -> Path:
    from playwright.sync_api import sync_playwright

    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    html_path = out_path.with_suffix(".html")
    html_path.write_text(html_text, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H})
        page.goto(html_path.as_uri())
        page.wait_for_selector("body[data-fitted='1']")
        page.screenshot(path=str(out_path))
        browser.close()
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="chomoand-4.blog(Travis Japan)アイキャッチ生成")
    ap.add_argument("--title", required=True, help="記事タイトル全文(要約しない)")
    ap.add_argument(
        "--color-key",
        default="auto",
        choices=["auto", *sorted(COLORS)],
        help="メンバー名 or group。auto(既定)=タイトルにメンバー名が1人だけ→そのメンバーカラー、なし/複数→group(紫)",
    )
    ap.add_argument("--style", default="stage", choices=["light", "stage", "elegant"])
    ap.add_argument(
        "--split",
        default=None,
        help='3行デザイン(タイトルをそのまま使う版): "1行目|2行目|3行目"。2行目=タイトルで一番強調したい内容。'
        "Travis Japan/トラジャは自動で省略され、3行をつなげるとタイトルと一致する必要がある",
    )
    ap.add_argument(
        "--lines",
        default=None,
        help='3行デザイン(自由文言版): "1行目|2行目|3行目"。--titleとの一致チェックをしない。'
        "マツが記事本文を読んでキャッチーな見出しを組み立てる場合に使う(--splitと同時指定はできない)",
    )
    ap.add_argument(
        "--ai-bg", action=argparse.BooleanOptionalAction, default=True,
        help="背景をPollinations.aiで毎回AI生成する(既定で有効・人物なしの抽象ステージ演出)。--no-ai-bgでCSSグラデーションに固定",
    )
    ap.add_argument("--seed", type=int, default=None, help="背景生成のseedを固定する場合に指定(未指定ならランダム)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.split and args.lines:
        raise SystemExit("--split と --lines は同時に指定できない")
    color_key = detect_color_key(args.title) if args.color_key == "auto" else args.color_key
    print(f"color-key: {color_key}")
    bg_path = resolve_ai_background(args.ai_bg, color_key, args.style, args.seed)
    try:
        if args.split:
            stripped = strip_group_name(args.title)
            lines = parse_split(stripped, args.split)
            html_text = build_html(stripped, color_key, args.style, lines, bg_path)
        elif args.lines:
            parts = [p.strip() for p in args.lines.split("|")]
            if len(parts) != 3 or not all(parts):
                raise SystemExit(f'--lines は「1行目|2行目|3行目」の3つ(空なし)で指定: {args.lines!r}')
            html_text = build_html("", color_key, args.style, parts, bg_path)
        else:
            html_text = build_html(args.title, color_key, args.style, bg_path=bg_path)
        print(f"done: {render(html_text, Path(args.out))}")
    finally:
        if bg_path is not None:
            bg_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
