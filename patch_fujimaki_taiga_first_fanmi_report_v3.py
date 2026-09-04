# -*- coding: utf-8 -*-
"""藤牧大雅 初ファンミレポ記事(12295) パッチ v3:
- セトリを実際の曲順+SKY-HI「JUST BREATHE feat. 3RACHA」+MC構成で書き直し
- 自費なのに本格的な演出(照明20灯超・スモーク・大型スクリーン映像・ピンマイク)の一文追加
- JYP節にスクリーンへ当時の3ショット自撮りが映った旨を追記
出典: @tai_ga17517 / @_TruTH4me の当日レポ
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

post = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}?context=edit", headers=H).json()
content = post["content"]["raw"]

REPLACEMENTS = [
    # 1) セトリ節の導入2段落を、実際の曲順・MC構成に書き直し
    ("<!-- wp:paragraph -->\n<p>ファンミの前半は、藤牧大雅さんのソロステージが中心でした。<br>\nStray Kidsの「MOUNTAINS」「MEGAVERSE」、BOYNEXTDOORの「IF I SAY, I LOVE YOU」などを、キレのあるダンスと豊かな表情で披露しています。</p>\n<!-- /wp:paragraph -->",
     "<!-- wp:paragraph -->\n<p>ファンミの前半は、藤牧大雅さんのソロステージが中心でした。<br>\n"
     "ファンがまとめたレポによると、序盤はStray Kidsの「MOUNTAINS」「MEGAVERSE」でスタートし、MCを挟んでBOYNEXTDOORの「IF I SAY, I LOVE YOU」、さらにSKY-HIの「JUST BREATHE feat. 3RACHA」と続きました。<br>\n"
     "キレのあるダンスと豊かな表情で、練習生としての実力を見せています。</p>\n<!-- /wp:paragraph -->\n\n"
     "<!-- wp:paragraph -->\n<p>曲間のMCは4つのパートに分かれていて、2つ目が事前質問に答える「教えて！大雅のQ&A！」、3つ目でお着替えとゲスト2人の登場、4つ目が客席も巻き込むダンスチャレンジゲームという流れでした。<br>\n"
     "自費イベントながら、舞台には20灯以上の照明にスモーク、背面の大型スクリーンには映像やグラフィックが次々と映し出され、藤牧さんもピンマイクを着けての本格的なステージ。<br>\n"
     "「これでいくらかかったのか」と、規模の大きさに驚くファンの声も上がりました。</p>\n<!-- /wp:paragraph -->"),
    # 2) JYP節: スクリーンに3ショット自撮りが映った
    ("それまではNiziUのMAKOさんに通訳してもらっていたそうです。</p>\n<!-- /wp:paragraph -->",
     "それまではNiziUのMAKOさんに通訳してもらっていたそうです。<br>\n"
     "トーク中にはスクリーンへ当時の3ショット自撮りが映し出され、加工アプリで撮ったようなレトロな写りに「時代を感じる」と会場がどよめきました。</p>\n<!-- /wp:paragraph -->"),
    # 3) まとめボックスのセトリ行を補足
    ("&#10003; セトリはStray Kids「MOUNTAINS」「MEGAVERSE」「MIROH」、オリジナル曲「Island」など<br>",
     "&#10003; セトリはStray Kids「MOUNTAINS」「MEGAVERSE」「MIROH」、SKY-HI「JUST BREATHE feat. 3RACHA」、オリジナル曲「Island」など<br>"),
]

for old, new in REPLACEMENTS:
    if old not in content:
        print("!! NOT FOUND:\n", old[:140])
        sys.exit(1)
    content = content.replace(old, new, 1)

r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{POST_ID}",
                  headers=HJSON,
                  data=json.dumps({"content": content, "status": "draft"}).encode("utf-8"))
r.raise_for_status()
print("patched", POST_ID, "->", r.json()["status"])
