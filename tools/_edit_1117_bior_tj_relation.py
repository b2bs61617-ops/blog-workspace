# -*- coding: utf-8 -*-
"""chomoand-4.blog ID2798(公開中): 「biorとトラジャの関係は？」の節を「これまでのbiorのCMは？」の前に追加(2026-11-17、オシリ依頼)。

出典:
- 月刊ネット販売 https://nethanbai.co.jp/archives/15985 (2024/6/29アンバサダー起用、「オファー当時、世界進出に向け努力していた彼らの姿が…」同社コメント)
- tjnews https://tjnews.net/biororganics_tj/ (2023/3/13 クッションファンデのイメージキャラクター就任、曲「Still on the journey」)
- 公式X https://x.com/bior_organics/status/1806900527588053347 (アンバサダー就任)
- ORICON https://www.oricon.co.jp/news/2226581/full/ (2022/3/3 LA留学発表)
- ファンの話(Jr.時代に依頼→LA留学で受けられず→他と契約せず待っていた)は公式の裏付けなし。投稿は埋め込まずぼかして紹介。
WP本文に直接パッチ(スクリプト_build_travis_bior_cm_coffret_1116.pyは古い。公開済みなのでstatusは送らない)。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

POST = 2798
ANCHOR = '<!-- wp:heading -->\n<h2 class="wp-block-heading">これまでのbiorのCMは？</h2>'
MARK = "biorとトラジャの関係は？"
NETHAN = "https://nethanbai.co.jp/archives/15985"

b = blogkit.Blocks("#3b6fb6", "#bcd2ef", "#f1f6fd")
sec = ""
sec += b.h2(MARK)
sec += b.p(
    "Travis Japanとbior organicsのつきあいは、2023年から続いています。",
    "最初はファンデーションのイメージキャラクターで、2024年からはブランドアンバサダーになりました。",
)
sec += b.table(("時期", "できごと"), [
    ("2022年3月", "Travis JapanがLA留学を発表(当時はジャニーズJr.)"),
    ("2022年10月", "世界デビュー"),
    ("2023年3月", "クッションファンデのイメージキャラクターに就任"),
    ("2024年6月", "bior organicsのブランドアンバサダーに就任"),
    ("2025年1月", "パフダンスのCMが放送スタート"),
    ("2026年11月", "スキンケアの新CMが放送スタート"),
])
sec += b.h3("bior側が話した起用の理由")
sec += b.p(
    "2024年にアンバサダーに起用したとき、bior organicsは理由をこう話しています。",
    "オファーした当時、" + b.mark("世界進出に向けて努力していた彼らの姿") + "が、自分たちの考えに重なったそうです。",
)
sec += b.p(
    "その考えとは、「オーガニック化粧品という狭い市場の中で世界を見据えて展開したい」というものです。",
    "世界をめざすトラジャと、世界をめざすブランドが、同じ方向を向いていたということですね。",
    "(出典:" + b.link(NETHAN, "月刊ネット販売") + ")",
)
sec += b.h3("「Jr.時代から待っていてくれた」という話も")
sec += b.p(
    "ファンの間では、biorがJr.時代のトラジャにも仕事を依頼していた、という話が語られています。",
    "そのときはLA留学が決まっていたので受けられなかったものの、ほかのタレントとは契約せずに帰りを待っていてくれた、という内容です。",
)
sec += b.p(
    "ただし、この話は" + b.mark("公式からは発表されていません") + "。",
    "公式に分かっているのは、bior側が「世界進出に向けて努力する姿」にひかれて起用した、というところまでです。",
    "それでも、2023年から3年以上ずっと同じブランドとCMを続けているのは、おたがいの信頼があるからこそと言えそうです。",
)

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    wp = blogkit.WP("travis")
    p = wp.get_post(POST)
    cur = p["content"]["raw"]
    if MARK in cur:
        raise SystemExit("もう入っているワン")
    if cur.count(ANCHOR) != 1:
        raise SystemExit("差し込み位置が見つからないワン")
    new = cur.replace(ANCHOR, sec + ANCHOR)
    if "--dry" in sys.argv:
        print(sec)
        raise SystemExit
    wp.post("/posts/{}".format(POST), {"content": new})
    chk = wp.get_post(POST)
    raw = chk["content"]["raw"]
    print(chk["status"], chk["title"]["raw"], MARK in raw, "公式からは発表されていません" in raw, len(cur), "->", len(raw))
