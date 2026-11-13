# -*- coding: utf-8 -*-
"""デビュー公約まとめ(JP15827/KR15828/EN15829)に「並び順=実行順なら2週間おき」の予想を追記する(2026-11-13)。
使い方: python tools/_append_ko1keyz_kouyaku_order_1113.py [画像パス]   (画像は公式動画から切り出した12人の並びカード)
"""
import json, subprocess, sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from _mubank1009_helpers import WP_URL, HEADERS_AUTH, wp_upload, img_html, h2, p, UI
from honorific import add_san

ui = UI(AB="#d9d9de", AL="#5b5f6b", BG="#f5f5f7", TH="#e8e8ec", marker="mark_yellow")
MARK = "<!-- kouyaku-order-1113 -->"
SRC = "出典：https://www.youtube.com/watch?v=jH4XQx0JCxk"

ORDER = [("RYUJI", "11月12日", "似顔絵(実行済み)"), ("RYOGA", "11月26日", "マンガのプレゼン"),
         ("SIYOUNG", "12月10日", "バクラヴァ"), ("YUKI", "12月24日", "クリスマスのサンタ"),
         ("YURA", "1月7日", "書き初め"), ("KOSUKE", "1月21日", "国内旅行"),
         ("SHINHAENG", "2月4日", "コスプレダンス"), ("DAIKI", "2月18日", "お悩み解決"),
         ("TOWA", "3月4日", "感謝の手紙"), ("YOSHIKI", "3月18日", "スイーツパーティー"),
         ("ISSA", "4月1日", "好きな食べ物"), ("KEITO", "4月15日", "夢の国")]


def jp(img):
    rows = [(n, f"{d}ごろ<br><span style=\"font-size:12px;color:#888;\">{s}</span>") for n, d, s in ORDER]
    return "\n\n".join([MARK,
        "<!-- wp:heading {\"level\":3} -->\n<h3 class=\"wp-block-heading\">並び順のとおりなら、YUKIの回が誕生日の12月24日に？</h3>\n<!-- /wp:heading -->",
        p("ファンの間では、「並び順が公約の実行順では？」という予想が話題になっています。<br>\n"
          "RYUJI編の動画の最初に、12人の名前とマークが決まった順番で並ぶ画面が出てくるからです。"),
        img or "",
        p(f"並びは、RYUJI・RYOGA・SIYOUNG・YUKI・YURA・KOSUKE…の順です。<br>\n"
          f"もし{ui.mark('2週間おきに1人ずつ公開', True)}されるなら、4人目のYUKIはちょうど12月24日になります。<br>\n"
          "12月24日はYUKIの誕生日で、公約は「クリスマスにサンタになる」なので、ぴったり重なります。"),
        ui.infobox("並び順どおり2週間おきだった場合の予想", rows, w="30%"),
        p("さらに5人目のYURAは1月7日になり、「書き初め」の公約とも時期が合います。<br>\n"
          "季節に合わせた公約の2人がそろって当てはまるのは、偶然にしてはできすぎですね。"),
        p("ただし、これは公式の発表ではなく、あくまで予想です。<br>\n"
          "旅行や夢の国のように、撮影に時間がかかる公約は、順番が入れかわることもありそうです。<br>\n"
          "まずは11月26日ごろに、RYOGAの「マンガのプレゼン」が来るかどうかに注目です。"),
    ])


KR = MARK + "\n\n" + p("팬들 사이에서는 RYUJI 편 영상에 나온 12명의 순서(RYUJI, RYOGA, SIYOUNG, YUKI, YURA, KOSUKE…)가 "
    "공약 실행 순서라는 예상이 나오고 있습니다. 2주 간격이라면 RYOGA 11월 26일, SIYOUNG 12월 10일, "
    "YUKI는 생일인 12월 24일, YURA는 1월 7일로 '산타'와 '새해 서예' 공약 시기와 딱 맞습니다. 공식 발표가 아닌 예상입니다.")
EN = MARK + "\n\n" + p("Fans noticed that the RYUJI episode shows the 12 members in a set order (RYUJI, RYOGA, SIYOUNG, YUKI, YURA, KOSUKE...). "
    "If that is the release order and a new episode comes every two weeks, RYOGA lands on Nov 26, SIYOUNG on Dec 10, "
    "YUKI on his birthday, Dec 24, and YURA on Jan 7, matching both the Santa and New Year calligraphy pledges. This is only a fan theory, not an official schedule.")

JP_ANCHOR = "新しい回が公開されたら、この記事の一覧も更新していきます。</p>\n<!-- /wp:paragraph -->"
KR_ANCHOR = "새 회차가 공개되면 이 글도 업데이트하겠습니다.</p>\n<!-- /wp:paragraph -->"
EN_ANCHOR = "We'll update this post as new episodes come out.</p>\n<!-- /wp:paragraph -->"


def patch(pid, anchor, add):
    raw = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=HEADERS_AUTH).json()["content"]["raw"]
    if MARK in raw:
        print(pid, "already"); return
    assert raw.count(anchor) == 1, (pid, raw.count(anchor))
    new = raw.replace(anchor, anchor + "\n\n" + add)
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                      data=json.dumps({"content": new}).encode("utf-8"))
    r.raise_for_status()
    chk = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=HEADERS_AUTH).json()["content"]["raw"]
    print(pid, "ok" if MARK in chk else "NOT REFLECTED", len(chk))


if __name__ == "__main__":
    img = ""
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        m = wp_upload(Path(args[0]), "image/jpeg")
        print("MEDIA", m["id"])
        img = img_html(m, "デビュー公約の12人が並んだ画面", SRC)
    html = add_san(jp(img), "ko1keyz")
    f = ROOT / "tmp_kouyaku_matome" / "order_1113.html"
    f.write_text(html, encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools" / "easy_read.py"), "fix", str(f)], check=True)
    rc = subprocess.run([sys.executable, str(ROOT / "tools" / "easy_read.py"), "check", str(f)]).returncode
    if "--dry" in sys.argv:
        print(f.read_text(encoding="utf-8")); sys.exit(0)
    patch(15827, JP_ANCHOR, f.read_text(encoding="utf-8"))
    patch(15828, KR_ANCHOR, KR)
    patch(15829, EN_ANCHOR, EN)
