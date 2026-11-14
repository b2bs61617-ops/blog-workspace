# -*- coding: utf-8 -*-
"""記事スクリプトのひな形(2026-11-14〜)。これをコピーして「本文のデータだけ」書きかえる。

共通の部品は tools/blogkit.py にある。記事ごとのスクリプトに req() や .env の読み込みを書き写さない。

    python tools/_build_xxx.py                # 組み立て → 事実チェック → 下書き投稿(【未】付き・status:draft)
    python tools/_build_xxx.py --build-only   # articles/<KEY>.html を作るだけ
    python tools/_build_xxx.py --update       # 下書きの本文を上書き(公開済みは上書きしない)
    python tools/_build_xxx.py --publish      # ユーザーが「公開して」と言ったあとだけ。公開 → Indexing → X/Threads
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

# ---- ここから記事ごとに書きかえる ----
SITE = "trend"                      # trend / sixtones / ko1keyz / snowman / travis / ktl
KEY = "sample_article_1114"         # 控えのファイル名(articles/<KEY>_posted.json)。記事ごとに変える
TITLE = "サンプル記事のタイトルはどう書く？"   # 35字まで。【未】は自動で付く
SLUG = "sample-article"
CATEGORIES = [37]
NAMES = ["伊野尾慧", "有岡大貴"]    # さんを付ける「メンバー以外の人名」
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.png")   # あれば自動でアップ
EYECATCH_ALT = "サンプル"
X_TEXT = ""                         # 公開のときのX本文(答えは書かない・誘導の一言なし)
X_TAGS = ""                         # 例 "#SnowMan #目黒蓮"

b = blogkit.Blocks("#c2410c", "#f2c9a8", "#fff7ef")
out = ""
out += b.p("1文目。", "2文目に" + b.mark("大事なところ") + "を入れる。")
out += b.wakaru(["わかること1", "わかること2"])
out += b.h2("見出し")
out += b.mini(("番組名", "『サンプル』"), ("放送", "2026年11月18日(水)"))
out += b.table(("項目", "内容"), [("A", "1"), ("B", "2")])
out += b.h2("まとめ")
out += b.checks(["まとめ1", "まとめ2"])
out += b.p("まとめの枠のあとに、ファン目線の感想を1〜2文。")
# ---- ここまで ----

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = blogkit.finalize(out, SITE, NAMES)   # さん付け → ひらがな直し
    if "--publish" in sys.argv:
        import json
        state = json.loads((blogkit.ARTICLES / (KEY + "_posted.json")).read_text(encoding="utf-8"))
        blogkit.publish(SITE, state["post"], X_TEXT, X_TAGS)
    elif "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
