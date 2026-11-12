"""スマホで読みやすく、誰でも分かる文章になっているかを機械的にチェック・修正する(2026-11-10 ユカ指示、全サイト必須)。

ユカ「ウチの記事を見に来る人はほぼスマホ。万人受けする、誰でも理解できる簡単な言い回しや漢字で書いて」。
執筆時の注意書きだけだと別セッションで守られないので、blog-upload STEP1.56 でこのツールを必ず通す。

fix  … 難しい漢字をひらがなに直す(意味が変わらないものだけ。例: 殆ど→ほとんど、出来る→できる)
       作品の略称もそろえる(ABBREV。例: いろはの恋→恋とき ※正式タイトルは残す)
check… 直しきれないものを一覧にする。NG があれば終了コード1(書き直してから投稿する)
  NG  : 1文が80字超 / 1段落が5文超 or 250字超 / 表が4列以上 / 難しい言葉(言い換え候補つき)が残っている
  注意: 1文が60〜80字(できれば2文に分ける) / 見出しが32字超(スマホで3行になる)

対象外(そのまま残す):「」の引用(本人・ファンの言葉は原文のまま)、『』の作品名、<a>のリンク文字列、HTMLタグの中。
見出し・表・枠の中も漢字チェック・修正の対象にする(文の長さチェックは <p> と <li> だけ)。

usage:
    python tools/easy_read.py fix   記事.html [...]
    python tools/easy_read.py check 記事.html [...]
"""
import html as htmllib
import re
import sys
from pathlib import Path

# ひらがなにしても意味が変わらないもの(fix で自動置換)。ふつうの新聞・雑誌でもかなで書くことが多い語。
KANA = {
    "殆ど": "ほとんど", "所謂": "いわゆる", "流石": "さすが", "勿論": "もちろん", "兎に角": "とにかく",
    "宜しく": "よろしく", "宜しい": "よろしい", "沢山": "たくさん", "何故": "なぜ", "何処": "どこ",
    "其の": "その", "此の": "この", "或いは": "あるいは", "或る": "ある", "尚、": "なお、", "又、": "また、",
    "且つ": "かつ", "即ち": "すなわち", "但し": "ただし", "更に": "さらに", "既に": "すでに", "暫く": "しばらく",
    "予め": "あらかじめ", "敢えて": "あえて", "改めて": "あらためて", "僅か": "わずか", "様々": "さまざま",
    "色々": "いろいろ", "一層": "いっそう", "頗る": "すこぶる", "概ね": "おおむね", "専ら": "もっぱら",
    "未だに": "いまだに", "恐らく": "おそらく", "然し": "しかし", "然も": "しかも", "所為": "せい",
    "出来る": "できる", "出来た": "できた", "出来ない": "できない", "出来ず": "できず", "出来ま": "できま",
    "出来れ": "できれ", "出来て": "できて", "頂く": "いただく", "頂き": "いただき", "頂け": "いただけ",
    "下さい": "ください", "下さっ": "くださっ", "の為": "のため", 
    "時々": "ときどき", "度々": "たびたび", "迄": "まで", "等の": "などの", "等が": "などが",
    "等を": "などを", "等で": "などで", "等に": "などに", "等も": "なども", 
    "凄い": "すごい", "凄く": "すごく", "素敵": "すてき", "綺麗": "きれい", "可愛い": "かわいい", "可愛く": "かわいく",
    "嬉しい": "うれしい", "嬉しく": "うれしく", "面白い": "おもしろい", "美味しい": "おいしい",
    "怖い": "こわい", "頑張": "がんば", "一緒": "いっしょ", "貰": "もら",
    "揃": "そろ", "拘": "こだわ", "呟": "つぶや", "囁": "ささや", "噂": "うわさ", "痺れ": "しびれ", "煌びやか": "きらびやか",
    "垣間見": "かいま見", "醸し出": "かもし出", "憧れ": "あこがれ", "眩し": "まぶし", "瞬く間": "またたく間",
    "是非": "ぜひ", "其々": "それぞれ", "夫々": "それぞれ", "何れ": "いずれ", "稀に": "まれに", "滅多に": "めったに",
}

# 意味ごと言い換えたほうが分かりやすい硬い言葉(自動では直さず check で候補を出す)。
HARD = {
    "示唆": "ほのめかす/におわせる", "看過": "見のがす", "顕著": "はっきりしている/目立つ", "起因": "〜が原因",
    "惹起": "引き起こす", "鑑み": "考えると", "踏襲": "そのまま受けつぐ", "払拭": "なくす/ぬぐい去る",
    "逼迫": "苦しい/足りない", "乖離": "ずれ/差", "齟齬": "食いちがい", "毀損": "傷つける", "瓦解": "くずれる",
    "嚆矢": "はじまり", "端緒": "きっかけ", "所以": "理由", "畢竟": "結局", "就中": "とくに", "斯様": "このよう",
    "如何": "どう/どのよう", "然るべき": "ちゃんとした", "相違ない": "まちがいない", "余儀なく": "しかたなく",
    "鑑賞に堪え": "見ごたえがある", "枚挙に暇がない": "数えきれない", "一線を画": "ほかとはちがう",
    "言わずもがな": "言うまでもなく", "垂涎": "みんながほしがる", "僥倖": "思いがけない幸運",
    "忖度": "気をつかう", "邂逅": "出会い", "刮目": "注目", "白眉": "いちばんすごい", "珠玉": "とびきりの",
    "嗜好": "好み", "趣向": "工夫", "傾倒": "夢中になる", "賞賛": "ほめる", "称賛": "ほめる", "揶揄": "からかう",
    "批判が殺到": "批判が集まる", "物議を醸": "話題になる/さわぎになる", "憶測": "想像", "推察": "おしはかる/予想",
    "推測される": "考えられる", "見受けられ": "見られ", "散見": "ちらほら見られる", "包括": "まとめる",
    "網羅": "全部まとめる", "概要": "あらまし/ざっくりした内容", "詳細": "くわしい内容", "当該": "その",
    "上記": "上の", "下記": "下の", "前述": "さっき書いた", "後述": "あとで書く", "および": "と", "ならびに": "と", "もしくは": "または", "において": "で", "における": "での",
    "に際して": "のときに", "に伴い": "にあわせて", "を踏まえ": "をもとに", "に関しては": "については",
    "を有する": "をもつ", "を要する": "が必要な", 
}

_PROTECT = re.compile(r"<a\b[^>]*>.*?</a>|<[^>]+>|「[^「」]*」|『[^『』]*』", re.S)
# 前が漢字のときは置換しない(「仕事が」「変更に」「順位の」などの誤爆防止)
_KANA_RE = re.compile(r"(?<![\u4e00-\u9fff々])(?:" + "|".join(sorted(map(re.escape, KANA), key=len, reverse=True)) + ")")
_HARD_RE = re.compile("|".join(sorted(map(re.escape, HARD), key=len, reverse=True)))


def _text_parts(html):
    """(保護しない部分か, 文字列) の列。"""
    pos = 0
    for m in _PROTECT.finditer(html):
        if m.start() > pos:
            yield True, html[pos:m.start()]
        yield False, m.group(0)
        pos = m.end()
    if pos < len(html):
        yield True, html[pos:]


# 作品の略称をそろえる(「」の中も含めて直す。HTMLタグの中は触らない)。
# 正式タイトル「いろはの恋は時代(とき)をかける」はそのまま残し、略称だけ公式の「恋とき」にする(2026-11-12 ユカ指示)。
ABBREV = [
    (re.compile(r"いろはの恋(?!は時代)"), "恋とき"),
]


def _fix_abbrev(html):
    parts = re.split(r"(<[^>]+>)", html)
    for i in range(0, len(parts), 2):
        for pat, rep in ABBREV:
            parts[i] = pat.sub(rep, parts[i])
    return "".join(parts)


def fix(html):
    html = _fix_abbrev(html)
    return "".join(_KANA_RE.sub(lambda m: KANA[m.group(0)], s) if ok else s for ok, s in _text_parts(html))


def _plain(fragment):
    return htmllib.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def _sentences(text):
    # 「」の中の句点では切らない
    out, buf, depth = [], "", 0
    for ch in text:
        buf += ch
        if ch in "「『":
            depth += 1
        elif ch in "」』":
            depth = max(depth - 1, 0)
        elif ch in "。！？!?" and depth == 0:
            out.append(buf.strip())
            buf = ""
    if buf.strip():
        out.append(buf.strip())
    return [s for s in out if s]


def check(html):
    ng, warn = [], []
    body = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    body = re.sub(r"<(script|style|iframe|figcaption|blockquote)\b.*?</\1>", "", body, flags=re.S)

    for m in re.finditer(r"<(p|li)\b[^>]*>(.*?)</\1>", body, re.S):
        text = _plain(m.group(2))
        if not text:
            continue
        sents = _sentences(text)
        if m.group(1) == "p" and (len(sents) > 5 or len(text) > 250):
            ng.append(f"段落が長い({len(sents)}文・{len(text)}字。スマホで画面が文字だけになる→2つに分ける): {text[:40]}…")
        for s in sents:
            n = len(re.sub(r"「[^「」]*」", "「」", s))  # 引用の中身は数えない
            if n > 80:
                ng.append(f"1文が長い({n}字→2〜3文に分ける): {s[:50]}…")
            elif n > 60:
                warn.append(f"1文がやや長い({n}字): {s[:50]}…")

    for m in re.finditer(r"<h([23])\b[^>]*>(.*?)</h\1>", body, re.S):
        text = _plain(m.group(2))
        if len(text) > 32:
            warn.append(f"見出しが長い({len(text)}字。スマホで3行になる): {text}")

    for t in re.findall(r"<table\b.*?</table>", body, re.S):
        cols = max((len(re.findall(r"<t[dh]\b", r)) for r in re.findall(r"<tr\b.*?</tr>", t, re.S)), default=0)
        if cols >= 4:
            ng.append(f"表が{cols}列ある(スマホでは文字が縦に1〜2字ずつになる→3列以下に分けるか箇条書きにする)")

    for m in re.finditer(r"<img\b[^>]*>", body):
        tag = m.group(0)
        if "max-width" not in tag and "wp-image-" not in tag and "size-" not in tag:
            warn.append(f"画像に max-width:100% が無い(スマホではみ出すかも): {tag[:60]}")

    for pat, rep in ABBREV:
        for m in pat.finditer(re.sub(r"<[^>]+>", "", body)):
            ng.append(f"略称「{m.group(0)}」→「{rep}」(fix で自動で直る)")
    for ok, s in _text_parts(body):
        if not ok:
            continue
        for m in _KANA_RE.finditer(s):
            ng.append(f"ひらがなにできる漢字「{m.group(0)}」→「{KANA[m.group(0)]}」(fix で自動で直る)")
        for m in _HARD_RE.finditer(s):
            ng.append(f"難しい言葉「{m.group(0)}」→ 言い換え候補: {HARD[m.group(0)]}")
    return ng, warn


def main(argv):
    if len(argv) < 2 or argv[0] not in ("fix", "check"):
        print(__doc__)
        return 2
    rc = 0
    for f in argv[1:]:
        p = Path(f)
        src = p.read_text(encoding="utf-8")
        if argv[0] == "fix":
            new = fix(src)
            if new != src:
                p.write_text(new, encoding="utf-8")
                print(f"{f}: ひらがなに直した")
            else:
                print(f"{f}: 直すところなし")
            continue
        ng, warn = check(src)
        print(f"== {f}: NG {len(ng)}件 / 注意 {len(warn)}件")
        for x in ng:
            print("  NG  ", x)
        for x in warn:
            print("  注意", x)
        if ng:
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
