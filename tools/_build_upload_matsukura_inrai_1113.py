# -*- coding: utf-8 -*-
"""chomoand-4.blog 松倉海斗の誕生日インライ(2026-11-13、IG Dfrf-XJjaqv)の着用アクセ記事。

usage:
  python tools/_build_upload_matsukura_inrai_1113.py build    # articles/matsukura_inrai_1113.html を書き出す
  (honorific.py / easy_read.py をかける)
  python tools/_build_upload_matsukura_inrai_1113.py upload   # 画像・アイキャッチをアップして【未】下書き投稿
  python tools/_build_upload_matsukura_inrai_1113.py update   # 下書き本文だけ上書き(status=draft)
画像は本人のインライ・アーカイブ動画から切り出したもの(images/matchu_inrai1113_*.jpg)。第三者の特定投稿は使わない。
"""
import os, sys, json, base64, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
HTML = os.path.join(REPO, "articles", "matsukura_inrai_1113.html")
STATE = os.path.join(REPO, "articles", "matsukura_inrai_1113_posted.json")
SITE = "https://chomoand-4.blog"
TITLE = "【未】【インライ】松倉海斗のネックレスと指輪はどこ？クロムハーツとエルメス"
SLUG = "matsukura-kaito-instalive-acce"
CATS = [3, 6]
AUTHOR = 2  # momo(オシリと作った記事は日韓ともmomo)
ACC, LINE, BG = "#e88a5a", "#f2b28a", "#fdf1ea"
IG = "https://www.instagram.com/p/Dfrf-XJjaqv/"
HERMES_PG = ("https://www.hermes.com/jp/ja/product/%E3%83%AA%E3%83%B3%E3%82%B0-%E3%80%8A%E3%82%B7%E3%82%A7%E3%83%BC"
             "%E3%83%8C%E3%83%BB%E3%83%80%E3%83%B3%E3%82%AF%E3%83%AB%E3%83%BB%E3%82%A2%E3%83%B3%E3%82%B7%E3%82%A7"
             "%E3%83%8D%E3%80%8B-pm-H110025Bv00/")
CH = "https://www.chromehearts.com/"
IMGS = ["main", "necklace", "ring", "watch"]


def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n"


def mk(t):
    return f'<strong><span class="swl-marker mark_orange" style="font-size:1.15em;">{t}</span></strong>'


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n'


def html(s):
    return "<!-- wp:html -->\n" + s + "\n<!-- /wp:html -->\n"


def a(url, label, spon=False):
    rel = "nofollow sponsored noopener" if spon else "noopener"
    return f'<a href="{url}" target="_blank" rel="{rel}">{label}</a>'


def listbox(title, items, big=False):
    fs = "font-size:1.05em;" if big else ""
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return html(f'<div style="border:1px solid {LINE};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                f'<p style="font-weight:bold;{fs}margin:0;padding:10px 18px;background:{ACC};color:#fff;">{title}</p>\n'
                f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">\n{lis}\n</ul>\n</div>')


def keybox(rows):
    out = [f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>' for i, (k, v) in enumerate(rows)]
    return html(f'<div style="border:1px solid {LINE};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">\n'
                + "\n".join(out) + "\n</div>")


def checks(items):
    ps = "\n".join(f'<p style="margin:0 0 6px 0;">&#10003; {i}</p>' for i in items)
    return html(f'<div style="border:1px solid {LINE};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">\n{ps}\n</div>')


def table(rows):
    trs = []
    for i, r in enumerate(rows):
        st = f' style="background:{BG};font-weight:bold;"' if i == 0 else ""
        trs.append("<tr>" + "".join(f"<td{st}>{c}</td>" for c in r) + "</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            + "".join(trs) + "</tbody></table></figure>\n<!-- /wp:table -->\n")


def figure(name, alt, when):
    return html(f'<figure class="wp-block-image size-large"><img src="{{{{IMG:{name}}}}}" alt="{alt}" style="max-width:100%;height:auto;" loading="lazy">'
                f'<figcaption style="font-size:0.8em;color:#888;">出典:{a(IG, "松倉海斗さん公式Instagram(@machu_tj_1114)のインスタライブ")}({when})</figcaption></figure>')


def ig_embed():
    u = IG + "?utm_source=ig_embed&amp;utm_campaign=loading"
    return html(f'<div style="max-width:540px;margin:0 auto 16px;"><blockquote class="instagram-media" data-instgrm-permalink="{u}" data-instgrm-version="14" '
                'style="background:#FFF;border:0;border-radius:3px;box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);margin:1px;max-width:540px;min-width:326px;padding:0;width:calc(100% - 2px);">'
                f'<a href="{u}" target="_blank" rel="noopener">松倉海斗(@machu_tj_1114)さんのInstagram投稿</a></blockquote>\n'
                '<script async src="https://www.instagram.com/embed.js"></script></div>')


def build():
    import affiliate_box as ab, affiliate_linker as al
    tag = ab.load_keys().get("AMAZON_ASSOCIATE_TAG", "")
    AMZ_CH = al.build_amazon_search_url("クロムハーツ ベビーファット ネックレス", tag)
    AMZ_HM = al.build_amazon_search_url("エルメス シェーヌダンクル リング", tag)

    body = "".join([
        html('<p style="font-size:0.85em;color:#888;margin:0 0 12px 0;">本記事はプロモーションを含みます</p>'),
        p("2026年11月13日の夜、松倉海斗さんが自分のInstagramで「まちゅLv.29いんらい」を配信しました。",
          "29歳の誕生日(11月14日)を1日早くファンとお祝いした、約1時間のインスタライブです。",
          "アップで映ったアクセサリーを確かめると、ネックレスは" + mk("クロムハーツ「ベビーファット クロス」のダイヤ入り") + "、指輪は" + mk("エルメス「シェーヌ・ダンクル・アンシェネ」") + "とみられます。"),
        listbox("この記事でわかること", ["インライで松倉海斗が着けていたアクセサリー",
                                    "十字のネックレスはクロムハーツのどのモデル？",
                                    "鎖の形の指輪はエルメスのどのモデル？値段は？",
                                    "腕時計はいつものカルティエ？",
                                    "ジップアップのニットはどこの？",
                                    "どこで買える？"], big=True),

        h2("松倉海斗の誕生日インライはいつ？"),
        keybox([("配信", "2026年11月13日の夜(松倉海斗さん本人のInstagram)"),
                ("タイトル", "まちゅLv.29いんらい"),
                ("長さ", "約62分(アーカイブで見られる)"),
                ("着けていたもの", "ネックレス・指輪3つ・腕時計")]),
        p("配信は、オレンジの風船と金色の「HAPPY BIRTHDAY」の文字で飾られた部屋からでした。",
          "とちゅうで「Happy Birthday Machu」と書かれたいちごのケーキも登場しています。"),
        figure("main", "誕生日インスタライブの松倉海斗。白Tシャツの首元に十字のネックレス", "3:51ごろ"),
        p("服は、セリーヌのネイビーのジップアップニットに白いTシャツです。",
          "白Tシャツの上に、小さな十字のネックレスがはっきり映っています。"),
        ig_embed(),
        p("投稿には「ちょいと早めのバースデーだけど、みんなが集まってくれて最高に楽しい幸せな時間でした」とつづられていました。"),

        h2("ネックレスはクロムハーツの「ベビーファット クロス」"),
        keybox([("ブランド", "CHROME HEARTS(クロムハーツ)"),
                ("モデル", "ベビーファット クロス(パヴェダイヤ)とみられる"),
                ("素材", "シルバー"),
                ("大きさ", "縦 約24mm・横 約9mm(同じモデルの例)")]),
        figure("necklace", "松倉海斗のクロムハーツのベビーファットクロスのネックレスの拡大", "26:52ごろ、右は首元を拡大"),
        p("ネックレスがいちばん大きく映るのは、26分50秒ごろに松倉海斗さんがカメラに近づいた場面です。",
          "十字の形をアップで見ると、クロムハーツの特徴がそろっていました。"),
        checks(["十字の4本のうでが、ぽってりと丸くて太い",
                "うでのまわりに、ふちどりのような段がある",
                "十字の上に丸カンがあり、そこにチェーンを通している",
                "全体が細かくキラキラ光っていて、ダイヤが敷きつめられている"]),
        p("同じクロムハーツの十字でも、「タイニーCHクロス」は先がとがったダガーのような形です。",
          "今回の十字は先が丸くてずんぐりしているので、" + mk("「ベビーファット」") + "の形にいちばん近いです。"),
        h3("ゴールドではなくシルバー"),
        p("部屋の照明がオレンジっぽいので、チェーンが少し金色に見える場面もあります。",
          "ただ、白いTシャツや銀色のジッパーと並べると、十字そのものは白っぽい銀色でした。",
          "ベビーファットのダイヤ入りは22Kゴールドもありますが、今回はシルバーとみられます。"),
        h3("値段は？"),
        p("クロムハーツは、日本の公式サイトで値段を出していません。",
          "海外の中古ショップでは、シルバーのダイヤ入りが約3,900ドルでした。",
          "これはボールチェーン付きの値段です(11月13日に確認)。",
          "22Kゴールドのダイヤ入りは、中古で30万〜40万円ほどで取り引きされています。"),
        p("ダイヤの量やチェーンの長さで、値段は大きく変わります。",
          "買うときは、クロムハーツの直営店で確かめるのがいちばん確実です。"),
        h3("いつものティファニーとはちがうネックレス"),
        p("最近の松倉海斗さんは、ティファニーの「ロック」のネックレスをよく着けていました。",
          'くわしくは<a href="' + SITE + '/matsukura-kaito-tiffany-lock-diamond-pendant">ティファニーのロックの記事</a>で紹介しています。',
          "誕生日の配信では、十字のネックレスに替えていたのも見どころです。"),

        h2("指輪はエルメスの「シェーヌ・ダンクル・アンシェネ」"),
        keybox([("ブランド", "HERMÈS(エルメス)"),
                ("モデル", "リング《シェーヌ・ダンクル・アンシェネ》PM とみられる"),
                ("着けていた指", "右手の中指"),
                ("素材", "シルバーとみられる(ダイヤなし)")]),
        figure("ring", "松倉海斗の右手中指のエルメスのシェーヌダンクルの指輪", "21:53ごろ"),
        p("21分50秒ごろ、松倉海斗さんが両手をぎゅっと胸の前でにぎる場面があります。",
          "このとき、右手の中指に鎖の形の指輪がはっきり映りました。"),
        checks(["楕円の輪っかの真ん中に、横に1本の棒が入っている",
                "その輪っかが、指のまわりをぐるっとつながっている",
                "輪っかの表面はつるんとしていて、ダイヤはない"]),
        p("「シェーヌ・ダンクル」は、船のいかりの鎖をモチーフにしたエルメスの定番デザインです。",
          "輪っかがつながった指輪は「アンシェネ」という名前で、細めのPMサイズとみられます。"),
        h3("シルバー？ピンクゴールド？"),
        p("同じデザインには、ピンクゴールドやダイヤ入りもあります。",
          "でも、左手の薬指のシルバーの指輪と色を比べると、同じ白っぽい銀色でした。",
          "ネックレスも時計も銀色なので、" + mk("シルバー") + "でそろえていたとみられます。"),
        table([["素材", "値段(税込)"],
               ["シルバー", "中古で9万円台"],
               ["ピンクゴールド", "48万700円"],
               ["ダイヤ入り", "195万8,000円"]]),
        p("ピンクゴールドとダイヤ入りは、11月13日にエルメス公式オンラインストアで確認した値段です。",
          "ピンクゴールドの商品番号はH110025B 00047、はばは0.58cmです。",
          "シルバーは公式で新品の値段が見つからず、中古のお店で9万円台でした。"),
        h3("左手の指輪は？"),
        p("左手の人差し指には四角い台のついた指輪、薬指には模様の入ったシルバーの指輪をしていました。",
          "どちらも動画の画質ではブランドまで分からなかったので、わかりしだい追記します。"),

        h2("腕時計はいつものカルティエのタンク"),
        figure("watch", "松倉海斗の左手首の角形の腕時計", "14:04ごろ、右は手首を拡大"),
        p("14分ごろ、両手を合わせる場面で、左手首に四角い腕時計が映りました。",
          "銀色の角形のケースに、茶色の革ベルトの組み合わせです。"),
        p("これは、逆引きランキングの動画でも着けていたカルティエの「タンク」とみられます。",
          'くわしくは<a href="' + SITE + '/matsukura-kaito-cartier-tank-ranking">カルティエのタンクの記事</a>で紹介しています。'),

        h2("ニットはセリーヌの「トリオンフ」ジップアップ"),
        keybox([("ブランド", "CELINE(セリーヌ)"),
                ("商品名", "ジップアップ セーター トリオンフ(トリオンフ トラッカーセーター)とみられる"),
                ("品番", "RY09T0ZPV.07MR"),
                ("色", "ネイビー"),
                ("素材", "ウール100%")]),
        p("インライで着ていたニットは、セリーヌの「トリオンフ」のジップアップセーターとみられます。",
          "胸元に、セリーヌのマーク「トリオンフ」の小さなししゅうが入っています。"),
        checks(["首まで立ち上がるスタンドネックのジップアップ",
                "太いうねのリブ編みで、ゆったりした形",
                "胸元にトリオンフの小さなししゅう",
                "インスタライブの画面は左右が反転するので、ロゴの位置も商品と合う"]),
        p("動画では黒っぽく見えますが、部屋の照明のせいで、色はネイビーとみられます。",
          "同じセリーヌには黒のハーフジップもありますが、こちらは首元から裾まで全部ジッパーです。"),
        p("セリーヌ公式の日本での値段は、見つかりませんでした。",
          f"並行輸入のお店の{a('https://www.magaseek.com/commodity/SMSR2030D/C03377EM001647/', 'マガシーク')}では、税込21万5,787円でした(11月13日に確認)。"),

        h2("どこで買える？"),
        listbox("購入先", [f"クロムハーツ:全国の直営店({a(CH, '公式サイト')})",
                         f"エルメス:{a(HERMES_PG, 'エルメス公式オンラインストア(ピンクゴールド)')}・全国のエルメスのお店",
                         f"セリーヌのニット:{a('https://www.magaseek.com/commodity/SMSR2030D/C03377EM001647/', 'マガシーク')}・全国のセリーヌのお店",
                         f"Amazon:{a(AMZ_CH, 'クロムハーツのベビーファットを見る', True)}・{a(AMZ_HM, 'エルメスのシェーヌダンクルを見る', True)}"]),
        p("クロムハーツもエルメスも、人気のアクセサリーは品切れのことが多いです。",
          "中古やネット通販で買うときは、本物の証明(ギャランティ)があるかを必ず確かめてください。"),

        html(f'<div style="border:1px solid {LINE};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;">\n'
             f'<p style="margin:0 0 6px 0;font-weight:bold;color:{ACC};">あわせて読みたい</p>\n<ul style="margin:0;padding-left:20px;">'
             f'<li><a href="{SITE}/matsukura-kaito-chrome-hearts-tiny-scroll-hoop">【ランキング】松倉海斗のピアスはどこの？クロムハーツのフープ！</a></li>'
             f'<li><a href="{SITE}/matsukura-kaito-tiffany-lock-diamond-pendant">【ランキング】松倉海斗のネックレスはどこの？ティファニーのロック！</a></li>'
             f'<li><a href="{SITE}/matsukura-kaito-cartier-tank-ranking">【ランキング】松倉海斗の腕時計はどこの？カルティエのタンク！</a></li>'
             f'<li><a href="{SITE}/matsukura-kaito-tiffany-hardwear-bracelet">【ランキング】松倉海斗のブレスレットはティファニーのハードウェア？</a></li>'
             '</ul>\n</div>'),

        h2("まとめ"),
        listbox("まとめ", ["松倉海斗が11/13の誕生日インライで着けていたアクセサリーを調べた",
                         "ネックレスはクロムハーツ「ベビーファット クロス」のダイヤ入り(シルバー)",
                         "指輪はエルメス「シェーヌ・ダンクル・アンシェネ」PM(シルバー、ダイヤなし)",
                         "腕時計はいつものカルティエのタンク",
                         "ニットはセリーヌのトリオンフのジップアップ(ネイビー)",
                         "左手の2つの指輪はブランド調査中"], big=True),
        p("誕生日の配信に、クロムハーツとエルメスを合わせてくるのはさすがまちゅですね！",
          "29歳の松倉海斗さんがどんなアクセサリーを選ぶのか、これからも楽しみです。"),
    ])
    open(HTML, "w", encoding="utf-8").write(body)
    base = TITLE.replace("【未】", "")
    assert TITLE.startswith("【未】") and len(base) <= 35, (len(base), base)
    print("title len", len(base), "html", len(body))


# ---------------- upload ----------------
def env():
    e = {}
    for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            e[k.strip()] = v.strip().strip('"')
    return e


E = None


def req(path, data=None, headers=None, method="POST"):
    base = E["WP_CHOMO4_URL"].rstrip("/")
    auth = base64.b64encode(f"{E['WP_CHOMO4_USERNAME']}:{E['WP_CHOMO4_APP_PASSWORD']}".encode()).decode()
    r = urllib.request.Request(base + path, data=data, method=method)
    r.add_header("Authorization", "Basic " + auth)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as ex:
        raise RuntimeError(f"{ex.code} {ex.read().decode('utf-8', 'ignore')[:500]}")


def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})


def media(fn, alt):
    m = req("/wp-json/wp/v2/media", open(os.path.join(REPO, "images", fn), "rb").read(),
            {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{fn}"'})
    jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": alt})
    return m


def with_images(st, body):
    imgs = st.setdefault("imgs", {})
    for n in IMGS:
        if n not in imgs:
            m = media(f"matchu_inrai1113_{n}.jpg", TITLE.replace("【未】", ""))
            imgs[n] = m["source_url"]
            json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        body = body.replace("{{IMG:%s}}" % n, imgs[n])
    return body


def upload(update=False):
    global E
    E = env()
    st = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    body = with_images(st, open(HTML, encoding="utf-8").read())
    if update:
        jpost(f"/wp-json/wp/v2/posts/{st['id']}", {"content": body, "status": "draft"})
        print("updated", st["id"])
        return
    if "id" in st:
        sys.exit(f"already posted {st['id']}")
    post = jpost("/wp-json/wp/v2/posts", {"title": TITLE, "content": body, "slug": SLUG, "status": "draft",
                                          "categories": CATS, "author": AUTHOR})
    st["id"] = post["id"]
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    m = media("matchu_inrai1113_eyecatch_canva.jpg", TITLE.replace("【未】", ""))
    jpost(f"/wp-json/wp/v2/posts/{post['id']}", {"featured_media": m["id"]})
    st["eyecatch"] = m["id"]
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("draft", post["id"], "eyecatch", m["id"], f"{SITE}/?p={post['id']}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        build()
    else:
        upload(update=(cmd == "update"))
