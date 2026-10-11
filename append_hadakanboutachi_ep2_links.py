"""chomoand-4.blog: 公開済みの1話記事(1208ロケ地・1240ビール瓶)に、2話記事(1465ロケ地・1472紅孔雀・1481衣装)への導線を足す(2026-10-11).

2話記事が下書きのままだとリンク切れになるので、リンク先がすべて公開済みのときだけ書き込む(--force-draft-links以外)。
公開記事なのでtitleは送らない。毎回最新のraw contentを取り直してから差し込む。
"""
import sys

from build_and_post_hadakanboutachi_5 import api

LOC2, BENI, COS = 1465, 1472, 1481
LI_STYLE = ""  # 関連記事boxの<li>は素のまま


def link_of(pid):
    r = api(f"posts/{pid}?context=edit&_fields=status,link,title", method="GET")
    return r["status"], r["link"], r["title"]["raw"]


def li(url, text):
    return f'<li><a href="{url}">{text}</a></li>'


def para(lines):
    return ("<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n")


def insert_after(raw, anchor, block):
    i = raw.find(anchor)
    if i < 0:
        raise SystemExit(f"anchor not found: {anchor[:40]}")
    j = raw.find("<!-- /wp:paragraph -->", i) + len("<!-- /wp:paragraph -->\n\n")
    return raw[:j] + block + raw[j:]


def prepend_related(raw, items):
    key = '<ul style="margin:0;padding-left:1.3em;">'
    i = raw.rfind(key)
    if i < 0:
        raise SystemExit("related box not found")
    i += len(key)
    return raw[:i] + "".join(items) + raw[i:]


def main():
    links = {}
    for pid in (LOC2, BENI, COS):
        st, url, title = link_of(pid)
        print(pid, st, url, title)
        if st != "publish" and "--force-draft-links" not in sys.argv:
            raise SystemExit(f"{pid} is {st}: 公開してから実行する(下書きへのリンクは読者には404)")
        links[pid] = url

    # ---- 1208 (1話ロケ地)
    raw = api("posts/1208?context=edit&_fields=content", method="GET")["content"]["raw"]
    if str(LOC2) in raw or "hadakanboutachi-ep2" in raw:
        print("1208: already linked, skip")
    else:
        raw = insert_after(raw, "モルタルの大きなテーブルで撮られています。", para([
            "第2話では、この建物が鯖崎たちの暮らすシェアハウス「Share House Takaban」として登場しました。",
            f'外観や第2話のほかのロケ地は、<a href="{links[LOC2]}">第2話のロケ地をまとめた記事</a>で紹介しています。',
        ]))
        raw = insert_after(raw, "ただし、ここは実際に診療している歯科医院です。", para([
            "第2話のエンドロールでは、撮影協力に「代官山デンタルクリニック」の名前が入っていました。",
        ]))
        raw = insert_after(raw, "第1話だけでも、都内から埼玉・千葉まで", para([
            f'第2話のロケ地は<a href="{links[LOC2]}">こちらの記事</a>、鯖崎の衣装は<a href="{links[COS]}">こちらの記事</a>にまとめています。',
        ]))
        raw = prepend_related(raw, [
            li(links[LOC2], "はだかんぼうたち2話のロケ地(シェアハウス・表参道ヒルズなど)"),
            li(links[COS], "はだかんぼうたち2話の鯖崎の衣装とTAGARUのスーツ"),
            li(links[BENI], "はだかんぼうたち2話にも紅孔雀？鯖崎のスマホの連絡先"),
        ])
        r = api("posts/1208", {"content": raw, "status": "publish"})
        print("1208 updated", r["status"], r["modified"])

    # ---- 1240 (ビール瓶)
    raw = api("posts/1240?context=edit&_fields=content", method="GET")["content"]["raw"]
    if str(BENI) in raw or "hadakanboutachi-ep2" in raw:
        print("1240: already linked, skip")
    else:
        old = ("<p>第2話は、2026年10月10日(土)よる11時から放送です。<br>\n"
               "第1話の瓶の場面はTVerで見返せるので、放送前にもう一度探してみるのもおすすめです。</p>")
        new = ("<p>実際に第2話では、鯖崎のスマホの連絡先に宮近海斗さん・松倉海斗さんを思わせる「宮田快斗」「松永界斗」が登場し、このビール瓶もシェアハウスの場面で再登場しました。<br>\n"
               f'くわしくは<a href="{links[BENI]}">第2話の紅孔雀の隠し要素をまとめた記事</a>で紹介しています。</p>')
        if old not in raw:
            raise SystemExit("1240 anchor paragraph not found")
        raw = raw.replace(old, new)
        raw = prepend_related(raw, [
            li(links[BENI], "はだかんぼうたち2話にも紅孔雀？鯖崎のスマホに宮田快斗・松永界斗"),
            li(links[LOC2], "はだかんぼうたち2話のロケ地(シェアハウス・表参道ヒルズなど)"),
        ])
        r = api("posts/1240", {"content": raw, "status": "publish"})
        print("1240 updated", r["status"], r["modified"])


if __name__ == "__main__":
    main()
