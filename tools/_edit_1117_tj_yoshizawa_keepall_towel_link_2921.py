# -*- coding: utf-8 -*-
"""2026-11-17: 公開中の2921(吉澤キーポル)に、ホグワーツ特急ハンカチ記事2968へのリンク段落を1つ足す。statusは送らない。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

wp = blogkit.WP("travis")
c = wp.get("/posts/2921", context="edit")["content"]["raw"]
if "?p=2968" in c:
    raise SystemExit("もう入ってるワン")
key = "ジャージや水のペットボトルが次々に出てきました。</p>\n<!-- /wp:paragraph -->\n"
assert c.count(key) == 1, c.count(key)
add = "\n" + blogkit.Blocks.p(
    "バッグの中からは、ハリー・ポッターのホグワーツ特急のハンカチも出てきました。",
    'くわしくは<a href="https://chomoand-4.blog/?p=2968" target="_blank" rel="noopener">吉澤閑也のぽかぽかのハンカチの記事</a>で紹介しています。',
).rstrip("\n") + "\n"
wp.post("/posts/2921", {"content": c.replace(key, key + add)})
p = wp.get("/posts/2921", context="edit")
print(p["status"], "?p=2968" in p["content"]["raw"], "?p=2955" in p["content"]["raw"])
