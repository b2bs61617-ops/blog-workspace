"""chomoand.com(恋愛リアリティ番組の出演者wiki)統一アイキャッチ生成ツール.

ピンク×カップルシルエットのイラスト背景に、KO1KEYZ(tools/eyecatch_koikeyz.py)と同じ
「3段・横幅いっぱいに自動フィット」の黒太文字を重ねてHTML+Playwrightで書き出す。
背景色はCSSのhue-rotateで毎回ランダムに変える(元のピンク×白ハートのトーン感は保ったまま色相だけ回す)。

背景画像は記事ごとにPollinations.ai(https://image.pollinations.ai 、APIキー不要・無料)で新規生成する
(2026-07-30〜。当初Gemini(Nano Banana)の画像生成モデルで実装したが、画像生成モデルは
無料枠が0で課金必須と判明し、無課金で使えるPollinations.aiに切り替えた)。
生成失敗時(タイムアウト・非2xx等)は静的背景(assets/chomoand_eyecatch_bg.png)に
フォールバックする(他の.env依存ツールと同じフェイルセーフ方式)。

使い方:
    python tools/eyecatch_chomoand.py \
        --top "wiki、プロフィール、学歴、家族構成" \
        --main "大島空凱" \
        --bottom "パデル日本代表の経歴" --bottom "双子の兄弟を調査!" \
        --out images/oshima_kuga_eyecatch_chomoand.png

--bottom は複数指定で複数行になる。--hue で色相の回転角(0〜360)を固定できる(未指定ならランダム)。
--no-ai-bg で背景AI生成をスキップして静的背景を強制する(検証用・オフライン時用)。
"""

from __future__ import annotations

import argparse
import html as html_mod
import random
import tempfile
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

CANVAS_W = 1200
CANVAS_H = 675  # 16:9(既存chomoand.comアイキャッチと同じ比率)

REPO_ROOT = Path(__file__).resolve().parent.parent
BG_PATH = REPO_ROOT / "assets" / "chomoand_eyecatch_bg.png"

POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt/"
POLLINATIONS_MODEL = "flux"
POLLINATIONS_TIMEOUT_SEC = 45
BG_GEN_PROMPT = (
    "soft pastel pink watercolor illustration, romantic couple silhouette standing close "
    "together on the right side of the frame, backlit, no facial details, white thin line "
    "heart doodles, soft bokeh light circles, left half of image is plain empty pastel "
    "gradient with no subject, blog banner background, non-photorealistic, flat illustration style"
)

TEXT_COLOR = "#111111"

# 文字の最大サイズ(実際のサイズはブラウザ側で幅いっぱいまで自動フィットさせる)
MAX_SIZE_TOP = 62
MAX_SIZE_MAIN = 170
MAX_SIZE_BOTTOM = 56
FIT_WIDTH = 1080  # テキストを収める横幅(左右に少し余白)


def build_html(
    top_lines: list[str],
    main: str,
    bottom_lines: list[str],
    hue: int | None = None,
    bg_path: Path = BG_PATH,
) -> str:
    """アイキャッチのHTMLを組み立てる(副作用なし)."""
    rng = random.Random()
    hue_deg = hue if hue is not None else rng.randint(0, 359)

    top_html = ""
    if top_lines:
        lines = "<br>".join(html_mod.escape(line) for line in top_lines)
        top_html = f'<div class="fit top" data-max="{MAX_SIZE_TOP}">{lines}</div>'

    bottom_html = ""
    if bottom_lines:
        lines = "<br>".join(html_mod.escape(line) for line in bottom_lines)
        bottom_html = f'<div class="fit bottom" data-max="{MAX_SIZE_BOTTOM}">{lines}</div>'

    bg_url = bg_path.as_uri()

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: {CANVAS_W}px; height: {CANVAS_H}px; overflow: hidden; }}
.canvas {{
  position: relative;
  width: {CANVAS_W}px; height: {CANVAS_H}px;
  overflow: hidden;
  display: flex; flex-direction: column;
  align-items: flex-start; justify-content: center;
  gap: 20px;
  padding: 0 60px;
  font-family: 'Yu Gothic', 'Meiryo', 'Hiragino Kaku Gothic ProN', sans-serif;
  font-weight: 900;
  color: {TEXT_COLOR};
  text-align: left;
}}
.bg {{
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover; object-position: 60% 40%;
  filter: hue-rotate({hue_deg}deg) saturate(1.05);
  z-index: 0;
}}
.fit {{ position: relative; z-index: 1; white-space: nowrap; line-height: 1.3; }}
.main {{ letter-spacing: 0.02em; line-height: 1.05; }}
</style>
</head>
<body>
<div class="canvas">
  <img class="bg" src="{bg_url}">
  {top_html}
  <div class="fit main" data-max="{MAX_SIZE_MAIN}">{html_mod.escape(main)}</div>
  {bottom_html}
</div>
<script>
// 各行を横幅いっぱい({FIT_WIDTH}px)まで拡大する
document.fonts.ready.then(() => {{
  for (const el of document.querySelectorAll('.fit')) {{
    const max = parseInt(el.dataset.max, 10);
    let size = max;
    el.style.fontSize = size + 'px';
    while (size > 16 && el.getBoundingClientRect().width > {FIT_WIDTH}) {{
      size -= 2;
      el.style.fontSize = size + 'px';
    }}
  }}
  document.body.dataset.fitted = '1';
}});
</script>
</body>
</html>
"""


def build_pollinations_url(seed: int) -> str:
    """Pollinations.aiのリクエストURLを組み立てる(副作用なし)."""
    encoded_prompt = urllib.parse.quote(BG_GEN_PROMPT)
    query = urllib.parse.urlencode({
        "width": CANVAS_W,
        "height": CANVAS_H,
        "model": POLLINATIONS_MODEL,
        "seed": seed,
        "nologo": "true",
    })
    return f"{POLLINATIONS_BASE_URL}{encoded_prompt}?{query}"


def generate_ai_background(seed: int) -> bytes:
    """Pollinations.ai(APIキー不要)で新しい背景バリエーションを1枚生成する.
    既定のPython-urllib User-Agentは403で弾かれるため、ブラウザ相当のUser-Agentを付ける。"""
    url = build_pollinations_url(seed)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=POLLINATIONS_TIMEOUT_SEC) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Pollinations.aiがHTTP {resp.status}を返した")
        return resp.read()


def resolve_background(use_ai: bool, seed: int | None = None) -> tuple[Path, Path | None]:
    """使用する背景パスを決める。戻り値は(背景パス, 生成した場合は削除すべき一時ファイルパス)。
    AI生成が無効・生成失敗のいずれかの場合は静的背景にフォールバックする。"""
    if not use_ai:
        return BG_PATH, None
    try:
        image_bytes = generate_ai_background(seed if seed is not None else random.randint(0, 2**31 - 1))
        if not image_bytes:
            raise RuntimeError("Pollinations.aiから画像データが返らなかった")
        tmp_path = Path(tempfile.gettempdir()) / f"chomoand_ai_bg_{uuid.uuid4().hex}.jpg"
        tmp_path.write_bytes(image_bytes)
        print(f"AI背景生成: {tmp_path}")
        return tmp_path, tmp_path
    except Exception as e:
        print(f"AI背景生成失敗({type(e).__name__}: {e})、静的背景にフォールバック")
        return BG_PATH, None


def render(html_text: str, out_path: Path) -> Path:
    """HTMLをPNGに書き出す."""
    from playwright.sync_api import sync_playwright

    out_path = Path(out_path).resolve()  # file:// URIにするため絶対パス化
    out_path.parent.mkdir(parents=True, exist_ok=True)
    html_path = out_path.with_suffix(".html")
    html_path.write_text(html_text, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H})
        page.goto(html_path.as_uri())
        page.wait_for_selector("body[data-fitted='1']")  # フォント読込+文字サイズ自動フィット完了待ち
        page.screenshot(path=str(out_path))
        browser.close()
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="chomoand.com統一アイキャッチ生成")
    parser.add_argument("--top", action="append", default=[], help="上段(複数指定で複数行)")
    parser.add_argument("--main", required=True, help="中央の主役テキスト(出演者名)")
    parser.add_argument("--bottom", action="append", default=[], help="下段(複数指定で複数行)")
    parser.add_argument("--out", required=True, help="出力PNGパス")
    parser.add_argument("--hue", type=int, default=None, help="背景の色相回転角(0-359)を固定する場合に指定")
    parser.add_argument(
        "--ai-bg", action=argparse.BooleanOptionalAction, default=True,
        help="背景をPollinations.aiで毎回AI生成する(既定で有効)。--no-ai-bgで静的背景に固定",
    )
    parser.add_argument("--seed", type=int, default=None, help="背景生成のseedを固定する場合に指定(未指定ならランダム)")
    args = parser.parse_args()

    bg_path, tmp_bg = resolve_background(args.ai_bg, args.seed)
    try:
        path = render(build_html(args.top, args.main, args.bottom, args.hue, bg_path), Path(args.out))
        print(f"done: {path}")
    finally:
        if tmp_bg is not None:
            tmp_bg.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
