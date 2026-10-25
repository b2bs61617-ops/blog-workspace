"""記事本文のメンバー名に「さん」を付ける(2026-10-25 ユカ指示、全サイト必須)。

タイトルには付けないので、これは本文HTMLにだけ通す。次の部分はそのまま残す:
- HTMLタグの中(属性値など)
- <a>〜</a> のリンク文字列(既存記事タイトルをそのまま使っているため)
- 「」で囲んだ引用(本人やファンの言葉をそのまま載せる部分)
- 商品名の一部(「目黒蓮特別版」など)や「〜担」

usage:
    python tools/honorific.py check <html...>   # 「さん」が抜けている箇所を表示(終了コード1)
    python tools/honorific.py fix <html...>     # その場で書き換える
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
SKIP_AFTER = ("さん", "くん", "君", "様", "氏", "特別版", "担")

_PROTECT = re.compile(r"<a\b[^>]*>.*?</a>|<[^>]+>|「[^「」]*」", re.S)


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


def _names(group):
    return GROUPS[group]


def add_san(html, group):
    pat = _pattern(_names(group))
    out, pos = [], 0
    for m in _PROTECT.finditer(html):
        out.append(pat.sub(lambda x: x.group(0) + "さん", html[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(pat.sub(lambda x: x.group(0) + "さん", html[pos:]))
    return "".join(out)


def missing(html, group):
    pat = _pattern(_names(group))
    hits, pos = [], 0
    for m in list(_PROTECT.finditer(html)) + [None]:
        end = m.start() if m else len(html)
        for x in pat.finditer(html, pos, end):
            hits.append(html[max(0, x.start() - 10):x.end() + 10].replace("\n", " "))
        if m:
            pos = m.end()
    return hits


def main(argv):
    if "--group" not in argv:
        sys.exit(f"--group を指定してワン({'/'.join(GROUPS)})")
    i = argv.index("--group")
    group = argv[i + 1]
    argv = argv[:i] + argv[i + 2:]
    mode, files = argv[0], argv[1:]
    bad = False
    for f in files:
        p = Path(f)
        html = p.read_text(encoding="utf-8")
        if mode == "fix":
            p.write_text(add_san(html, group), encoding="utf-8")
            print(f"fixed {f}")
        else:
            for h in missing(html, group):
                bad = True
                print(f"{f}: …{h}…")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
