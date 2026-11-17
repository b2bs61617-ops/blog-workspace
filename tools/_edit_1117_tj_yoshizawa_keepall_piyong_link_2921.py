# -*- coding: utf-8 -*-
"""2026-11-17: 公開中の2921(吉澤キーポル)に、ピヨン キーホルダー記事2955へのリンク段落を1つ足す(オシリOK)。statusは送らない。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

wp = blogkit.WP("travis")
c = wp.get_post(2921)["content"]["raw"]
if "?p=2955" in c:
    raise SystemExit("もう入ってるワン")
anchor = '<!-- wp:heading -->\n<h2 class="wp-block-heading">吉澤閑也のカバンの中身は？</h2>'
assert c.count(anchor) == 1
add = blogkit.Blocks.p(
    "このキーポルのショルダーストラップには、黒猫がアイスクリームになったキーホルダーもついていました。",
    'くわしくは<a href="https://chomoand-4.blog/?p=2955" target="_blank" rel="noopener">吉澤閑也のぽかぽかのキーホルダーの記事</a>で紹介しています。',
)
wp.post("/posts/2921", {"content": c.replace(anchor, add + anchor)})
p = wp.get_post(2921)
print(p["status"], "?p=2955" in p["content"]["raw"])
