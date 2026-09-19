"""Travis Japan専門ブログ(chomoand-4.blog)用アイキャッチ生成ツール.

eyecatch_chomoand0.py の後継(トラジャ向け)。記事タイトルは要約せず全文をそのまま載せる
(feedback: タイトルそのまま+大きく)。そのうえで見た目だけを作り込む:

- KO1KEYZ統一テンプレと同じ極太丸ゴシック(M PLUS Rounded 1c Black)
- 改行は日本語の文節単位(Intl.Segmenter)。「飾ら/れてる」「Travis/Japan」のような泣き別れをしない
- 先頭の【...】は上部のバッジに出す(文字は省略せず、置き場所だけ変える)
- タイトル中のメンバー名はメンバーカラーのマーカーで強調
- 背景は2種類: light(明るいスモーク) / stage(暗いステージライト)

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
import re
from pathlib import Path

CANVAS_W = 1200
CANVAS_H = 630
REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = REPO_ROOT / "assets" / "fonts" / "MPLUSRounded1c-Black.ttf"

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


# タイトル中のメンバー呼称(フルネーム・名字・他メンバーと被らない名前)。「海斗」は2人いるので含めない
MEMBER_ALIASES: dict[str, tuple[str, ...]] = {
    "宮近海斗": ("宮近海斗", "宮近"),
    "中村海人": ("中村海人", "中村", "海人"),
    "七五三掛龍也": ("七五三掛龍也", "七五三掛", "龍也"),
    "川島如恵留": ("川島如恵留", "川島", "如恵留"),
    "吉澤閑也": ("吉澤閑也", "吉澤", "閑也"),
    "松田元太": ("松田元太", "松田", "元太"),
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


def _script_3line() -> str:
    """3行デザイン用スクリプト: 画面いっぱいに使う.

    1・3行目は大きな文字(基準112px)、2行目は特大(基準230px)+縦に引き伸ばす。
    行が横幅に収まらないときは、まず横だけ詰め(縦長の文字にする)、それでも足りなければ文字を小さくする。
    """
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
  const h1 = fit(l1, 112, 0.62), h3 = fit(l3, 112, 0.62);
  const h2 = fit(l2, 230, 0.7, 1.3);
  // 残りの高さを2行目の縦伸ばしで使い切る(最大1.7倍)
  const sy = Math.max(1, Math.min(1.7, (USABLE_H - h1 - h3 - GAP * 2) / h2));
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
) -> str:
    """lines(3要素)を渡すと3行デザイン(2行目を最大・マーカー強調)、なければ従来の全文1ブロック."""
    if color_key not in COLORS:
        raise ValueError(f"unknown color_key: {color_key!r} (known: {', '.join(COLORS)})")
    if style not in ("light", "stage"):
        raise ValueError("style must be 'light' or 'stage'")
    main, tint = COLORS[color_key]
    badge, body = split_badge(title)
    # メンバー名(color-key)が本文にあれば強調対象にする
    mark = color_key if color_key != "group" and color_key in body else ""
    font_url = FONT_PATH.as_uri()
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
    if lines:
        badge_html = ""
        title_html = "".join(
            f'<div class="l l{i}" id="l{i}">{html_mod.escape(text)}</div>'
            for i, text in enumerate(lines, start=1)
        )
        script = _script_3line()
    else:
        title_html = '<div class="title" id="t"></div>'
        script = _script_block(body, mark, badge_html)

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
@font-face {{ font-family: 'Rounded'; src: url('{font_url}') format('truetype'); font-weight: 900; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: {CANVAS_W}px; height: {CANVAS_H}px; overflow: hidden; font-family: 'Rounded', 'Yu Gothic', sans-serif; font-weight: 900; }}
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
.frame {{ position: absolute; inset: 18px; border: 3px solid {"rgba(255,255,255,0.28)" if dark else "rgba(255,255,255,0.9)"}; border-radius: 26px; }}
.badge {{ position: relative; z-index: 2; font-size: 44px; letter-spacing: 0.06em; padding: 8px 34px 10px; border-radius: 999px;
  color: {"#fff" if dark else "#fff"}; background: {main if dark else "#2b1a55"}; {"color:#1b1030;" if dark and color_key in ("吉澤閑也","川島如恵留") else ""}
  box-shadow: 0 6px 24px {main}88; }}
.title {{ position: relative; z-index: 2; width: 1060px; text-align: center; line-height: 1.22; letter-spacing: 0.02em;
  color: {"#fff" if dark else "#1c1c1c"}; text-wrap: balance;
  text-shadow: {"0 0 24px rgba(20,8,50,.85), 0 3px 0 rgba(20,8,50,.5)" if dark else "0 0 14px rgba(255,255,255,.9)"}; }}
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
  <div class="glow g1"></div><div class="glow g2"></div><div class="glow g3"></div>
  <div class="beam b1"></div><div class="beam b2"></div><div class="beam b3"></div>
  <div class="dot" style="left:96px;top:70px;width:9px;height:9px"></div>
  <div class="dot" style="left:1040px;top:120px;width:7px;height:7px"></div>
  <div class="dot" style="left:180px;top:540px;width:6px;height:6px"></div>
  <div class="dot" style="left:1110px;top:500px;width:10px;height:10px"></div>
  <div class="dot" style="left:600px;top:44px;width:5px;height:5px"></div>
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
    ap.add_argument("--style", default="stage", choices=["light", "stage"])
    ap.add_argument(
        "--split",
        default=None,
        help='3行デザイン: "1行目|2行目|3行目"。2行目=タイトルで一番強調したい内容。'
        "Travis Japan/トラジャは自動で省略され、3行をつなげるとタイトルと一致する必要がある",
    )
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    color_key = detect_color_key(args.title) if args.color_key == "auto" else args.color_key
    print(f"color-key: {color_key}")
    if args.split:
        stripped = strip_group_name(args.title)
        lines = parse_split(stripped, args.split)
        html_text = build_html(stripped, color_key, args.style, lines)
    else:
        html_text = build_html(args.title, color_key, args.style)
    print(f"done: {render(html_text, Path(args.out))}")


if __name__ == "__main__":
    main()
