# -*- coding: utf-8 -*-
"""藤牧大雅 初ファンミレポ記事(12295) パッチ v4:
- セトリ・進行を一覧表(タイトルバー付き)で見やすく挿入
- 前後の地の文を表と重複しないよう整理
"""
import json, base64, os, sys
from pathlib import Path
import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f'{ENV["WP_KOIKEYS_USERNAME"]}:{ENV["WP_KOIKEYS_APP_PASSWORD"]}'.encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}
HJSON = {**H, "Content-Type": "application/json"}
POST_ID = 12295

ACCENT = "#8a8378"
BORDER = "#ddd9d3"
BG = "#f7f6f4"
TDBG = "#f3f1ee"

ROWS = [
    ("1", "MOUNTAINS / Stray Kids"),
    ("2", "MEGAVERSE / Stray Kids"),
    ("MC&#9312;", "トーク"),
    ("3", "IF I SAY, I LOVE YOU / BOYNEXTDOOR"),
    ("MC&#9313;", "教えて！大雅のQ&amp;A！(事前質問コーナー)"),
    ("4", "JUST BREATHE feat. 3RACHA / SKY-HI"),
    ("MC&#9314;", "お着替え・ゲスト(大林悠成／山下柊)登場"),
    ("MC&#9315;", "みんなで踊ろう！ダンスチャレンジゲーム(「Kick」「neko」ほか)"),
    ("5", "DOMINANCE / INI(3人で再演)"),
    ("6", "Island(藤牧大雅のオリジナル曲)"),
    ("7", "MIROH / Stray Kids(フィナーレ)"),
]

trs = "\n".join(
    f'<tr><td style="background:{TDBG};border:1px solid {BORDER};padding:7px 10px;width:88px;text-align:center;white-space:nowrap;">{k}</td>'
    f'<td style="border:1px solid {BORDER};padding:7px 12px;">{v}</td></tr>'
    for k, v in ROWS
)
SETLIST_BOX = (
    "<!-- wp:html -->\n"
    f'<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
    f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">セトリ・当日の進行(ファンレポより)</p>\n'
    f'<table style="border-collapse:collapse;width:100%;background:{BG};">\n{trs}\n</table>\n'
    f'<p style="margin:0;padding:8px 18px;font-size:12px;background:{BG};">5番以降はプレスリリースや複数のレポをもとにした順序で、前後する可能性があります。</p>\n'
    "</div>\n<!-- /wp:html -->"
)

post = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}?context=edit", headers=H).json()
content = post["content"]["raw"]

OLD_P1 = ("<!-- wp:paragraph -->\n<p>ファンミの前半は、藤牧大雅さんのソロステージが中心でした。<br>\n"
          "ファンがまとめたレポによると、序盤はStray Kidsの「MOUNTAINS」「MEGAVERSE」でスタートし、MCを挟んでBOYNEXTDOORの「IF I SAY, I LOVE YOU」、さらにSKY-HIの「JUST BREATHE feat. 3RACHA」と続きました。<br>\n"
          "キレのあるダンスと豊かな表情で、練習生としての実力を見せています。</p>\n<!-- /wp:paragraph -->\n\n"
          "<!-- wp:paragraph -->\n<p>曲間のMCは4つのパートに分かれていて、2つ目が事前質問に答える「教えて！大雅のQ&A！」、3つ目でお着替えとゲスト2人の登場、4つ目が客席も巻き込むダンスチャレンジゲームという流れでした。<br>\n"
          "自費イベントながら、舞台には20灯以上の照明にスモーク、背面の大型スクリーンには映像やグラフィックが次々と映し出され、藤牧さんもピンマイクを着けての本格的なステージ。<br>\n"
          "「これでいくらかかったのか」と、規模の大きさに驚くファンの声も上がりました。</p>\n<!-- /wp:paragraph -->")

NEW = ("<!-- wp:paragraph -->\n<p>ファンミは、歌とダンス・MC・ゲストコラボを織り交ぜた構成でした。<br>\n"
       "ファンがまとめたレポによると、当日の進行はおおむね次のとおりです。</p>\n<!-- /wp:paragraph -->\n\n"
       + SETLIST_BOX + "\n\n"
       "<!-- wp:paragraph -->\n<p>Stray Kidsの「MOUNTAINS」「MEGAVERSE」で幕を開け、BOYNEXTDOORの「IF I SAY, I LOVE YOU」、SKY-HIの「JUST BREATHE feat. 3RACHA」と、K-POPからJ-POPまで振り幅のあるナンバーが並びました。<br>\n"
       "キレのあるダンスと豊かな表情で、練習生として積み上げてきた実力がにじむステージです。</p>\n<!-- /wp:paragraph -->\n\n"
       "<!-- wp:paragraph -->\n<p>自費イベントながら、舞台には20灯以上の照明とスモーク、背面の大型スクリーンには映像やグラフィックが次々と映し出され、藤牧さんもピンマイクを着けての本格的なステージでした。<br>\n"
       "「これでいくらかかったのか」と、規模の大きさに驚くファンの声も上がっています。</p>\n<!-- /wp:paragraph -->")

if OLD_P1 not in content:
    print("!! NOT FOUND OLD_P1")
    sys.exit(1)
content = content.replace(OLD_P1, NEW, 1)

r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}",
                  headers=HJSON,
                  data=json.dumps({"content": content, "status": "draft"}).encode("utf-8"))
r.raise_for_status()
print("patched", POST_ID, "->", r.json()["status"])
