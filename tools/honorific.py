"""記事本文の人名に「さん」を付ける(2026-10-25 ユカ指示、全サイト必須)。

メンバーは GROUPS から自動で拾う。メンバー以外(共演者・ゲスト・スタッフなど)は記事ごとに
--names(関数では extra)で渡す。役名・歴史上の人物は渡さない。

タイトルには付けないので、これは本文HTMLにだけ通す。次の部分はそのまま残す:
- HTMLタグの中(属性値など)
- <a>〜</a> のリンク文字列(既存記事タイトルをそのまま使っているため)
- 「」で囲んだ引用(本人やファンの言葉をそのまま載せる部分)と『』で囲んだ番組名・作品名(「内村光良のオールナイトニッポン」など)
- 商品名の一部(「目黒蓮特別版」など)や「〜担」
- 見出し・表・まとめの枠・「この記事でわかること」の枠(2026-10-25 ユカ指示。ここは「さん」無しにそろえる。
  付いていたら外す)

usage:
    python tools/honorific.py check <html...>   # 「さん」が抜けている箇所を表示(終了コード1)
    python tools/honorific.py fix <html...>     # その場で書き換える
    --names "内村光良,LISA"                    # メンバー以外の人名(カンマ区切り)
グループは --group で必ず指定する(名字だけの「中村」「阿部」などが他の人に誤爆しないよう、グループごとに分けている)。
"""
import re
import sys
from pathlib import Path

# フルネーム → 単独でも使う名字(フルネームの一部として出てくる場合は除く)
GROUPS = {
    "snowman": {
        "岩本照": "岩本", "深澤辰哉": "深澤", "ラウール": None, "渡辺翔太": "渡辺",
        "向井康二": "向井", "阿部亮平": "阿部", "目黒蓮": "目黒", "宮舘涼太": "宮舘",
        "佐久間大介": "佐久間",
    },
    "ktl": {
        "岩﨑大昇": "岩﨑", "井上瑞稀": "井上", "中村嶺亜": "中村", "猪狩蒼弥": "猪狩",
        "佐々木大光": "佐々木",
    },
    "travis": {
        "宮近海斗": "宮近", "中村海人": None, "七五三掛龍也": "七五三掛", "川島如恵留": "川島",
        "吉澤閑也": "吉澤", "松田元太": None, "松倉海斗": None,
    },
    "ko1keyz": {
        "加藤大樹": None, "矢田佳暉": None, "パクシヨン": None, "オシンヘン": None, "後藤結": None,
        "柳谷伊冴": None, "小野慶人": None, "安部結蘭": None, "飯塚亮賀": None, "杉山竜司": None,
        "照井康祐": None, "濱田永遠": None,
    },
}

# 名前の直後がこれなら付けない(敬称済み・商品名・ファン呼称など)
SKIP_AFTER = ("さん", "くん", "君", "様", "氏", "特別版", "担", "(")

_PROTECT = re.compile(r"<a\b[^>]*>.*?</a>|<[^>]+>|「[^「」]*」|『[^『』]*』", re.S)

# 「さん」無しにする塊: 見出し / 表 / 「この記事でわかること」の枠 / まとめ見出し直後の枠・チェックマークの枠
_NO_SAN_BLOCKS = re.compile(
    r"<h2\b[^>]*>まとめ[^<]*</h2>\s*<!-- /wp:heading -->\s*<!-- wp:html -->.*?<!-- /wp:html -->"
    r"|<h[1-6]\b[^>]*>.*?</h[1-6]>"
    r"|<figure class=\"wp-block-table\".*?</figure>|<table\b.*?</table>"
    r"|<div\b(?:(?!<div\b).)*?この記事でわかること.*?</div>"
    r"|<div\b(?:(?!<div\b).)*?&#10003;.*?</div>"
    , re.S)


def _pattern(names):
    alts = []
    for full, short in names.items():
        alts.append(re.escape(full))
        if short:
            given = re.escape(full[len(short):])
            alts.append(re.escape(short) + f"(?!{given})")
    alts.sort(key=len, reverse=True)
    skip = "|".join(re.escape(s) for s in SKIP_AFTER)
    return re.compile(f"(?:{'|'.join(alts)})(?!{skip})")


def _names(group, extra=()):
    names = dict(GROUPS[group])
    names.update({n: None for n in extra})
    return names


def _segments(html):
    """(text, kind) に分ける。kind = "text"(さんを付ける) / "keep"(触らない) / "nosan"(さんを外す)"""
    segs, pos = [], 0
    for b in _NO_SAN_BLOCKS.finditer(html):
        segs += _inline_segments(html[pos:b.start()])
        segs.append((b.group(0), "nosan"))
        pos = b.end()
    return segs + _inline_segments(html[pos:])


def _inline_segments(chunk):
    segs, pos = [], 0
    for m in _PROTECT.finditer(chunk):
        segs += [(chunk[pos:m.start()], "text"), (m.group(0), "keep")]
        pos = m.end()
    return segs + [(chunk[pos:], "text")]


def _strip_san(block, names):
    alts = sorted({re.escape(n) for full, short in names.items() for n in (full, short) if n}, key=len, reverse=True)
    return re.sub(f"({'|'.join(alts)})さん", r"\1", block)


def add_san(html, group, extra=()):
    names = _names(group, extra)
    pat = _pattern(names)
    out = []
    for text, kind in _segments(html):
        if kind == "text":
            text = pat.sub(lambda x: x.group(0) + "さん", text)
        elif kind == "nosan":
            text = _strip_san(text, names)
        out.append(text)
    return "".join(out)


def missing(html, group, extra=()):
    pat = _pattern(_names(group, extra))
    hits = []
    for text, kind in _segments(html):
        if kind == "text":
            hits += [text[max(0, x.start() - 10):x.end() + 10].replace("\n", " ") for x in pat.finditer(text)]
    return hits


def main(argv):
    if "--group" not in argv:
        sys.exit(f"--group を指定してワン({'/'.join(GROUPS)})")
    i = argv.index("--group")
    group = argv[i + 1]
    argv = argv[:i] + argv[i + 2:]
    extra = ()
    if "--names" in argv:
        j = argv.index("--names")
        extra = tuple(n.strip() for n in argv[j + 1].split(",") if n.strip())
        argv = argv[:j] + argv[j + 2:]
    mode, files = argv[0], argv[1:]
    bad = False
    for f in files:
        p = Path(f)
        html = p.read_text(encoding="utf-8")
        if mode == "fix":
            p.write_text(add_san(html, group, extra), encoding="utf-8")
            print(f"fixed {f}")
        else:
            for h in missing(html, group, extra):
                bad = True
                print(f"{f}: …{h}…")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
