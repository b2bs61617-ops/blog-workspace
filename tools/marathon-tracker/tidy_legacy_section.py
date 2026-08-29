"""一度きりの整理スクリプト(2026-08-29)。

自動更新セクションを記事の一番上に移した後、記事下部に残った手書きの
旧「星野真里は今どこ？リアルタイム情報」セクション(見出し＋capbox＋
プレースホルダー4行)を、情報源の説明だけ残す形に置き換える。

    python tools/marathon-tracker/tidy_legacy_section.py --dry-run
    python tools/marathon-tracker/tidy_legacy_section.py
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import article_updater as au  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

NEW_SECTION = """<!-- wp:heading -->
<h2 class="wp-block-heading">星野真里の現在地・情報源について</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<p><strong>最新の現在地は、この記事のいちばん上「星野真里は今どこ？（マラソン現在地・リアルタイム更新）」で随時更新しています。</strong><br>
ここでは、現在地を自分で確認する方法をまとめています。</p>
<!-- /wp:html -->

<!-- wp:html -->
<p>星野真里さんのマラソンは、番組内で不定期に中継が入る形で進みます。<br>
「今どこを走っているか」をいちばん早く知る方法は、<span class="swl-marker mark_yellow">日本テレビ系の生放送</span>と日テレ公式のライブ配信を追うことです。<br>
中継が入っていない時間帯は、Xで「星野真里 マラソン」「24時間テレビ マラソン 現在地」などとリアルタイム検索すると、沿道で見かけた人の投稿から通過エリアがつかめることがあります。<br>
正確な通過地点は番組の公式発表を基準にするのが確実です。</p>
<!-- /wp:html -->

"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    post = au.get_post(cfg)
    c = post["content"]

    m1 = re.search(r"(<!--\s*wp:heading[^>]*-->\s*)?<h2[^>]*>[^<]*リアルタイム情報[^<]*</h2>", c)
    m2 = re.search(r"(<!--\s*wp:heading[^>]*-->\s*)?<h2[^>]*>[^<]*ゴール予想時刻[^<]*</h2>", c)
    if not m1 or not m2 or m2.start() <= m1.start():
        print("旧セクションが見つからない(すでに整理済み?)。何もしない。")
        return

    new_c = c[:m1.start()] + NEW_SECTION + c[m2.start():]
    print(f"置換範囲: {m1.start()}..{m2.start()} ({m2.start() - m1.start()} 文字) -> {len(NEW_SECTION)} 文字")

    if args.dry_run:
        out = HERE / "logs" / "tidy_preview.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(new_c, encoding="utf-8")
        print(f"[DRY-RUN] プレビュー: {out}")
        print("---- 置換後のこの部分 ----")
        print(new_c[m1.start():m1.start() + len(NEW_SECTION)])
        return

    bpath = au.backup(cfg, c)
    print(f"旧本文を退避: {bpath}")
    status = au.put_post(cfg, new_c)
    print(f"更新完了(status: {status})")


if __name__ == "__main__":
    main()
