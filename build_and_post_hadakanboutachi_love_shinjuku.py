"""chomoand-4.blog: はだかんぼうたち公式オフショット「鯖とLOVEで待ち合わせ」(2026-11-03)の撮影場所
=新宿アイランドタワー前のLOVEオブジェ(西新宿6-5-1)。ホンノウスイッチ公式「聖とLOVEで待ち合わせ」(2025-01-23)と同じ場所・同じ構図.

usage:
  python build_and_post_hadakanboutachi_love_shinjuku.py --dry   -> articles/hadakanboutachi_love_shinjuku.html を書き出す(画像はダミー)
  python build_and_post_hadakanboutachi_love_shinjuku.py         -> 画像・アイキャッチをアップしてHTMLを書き出す
  (tools/honorific.py fix をかける)
  python build_and_post_hadakanboutachi_love_shinjuku.py --post  -> 書き出したHTMLで下書き作成(2回目以降は上書き)
"""
import json, re, sys

from build_and_post_hadakanboutachi_5 import (ROOT, SITE, api, upload_media, para, h2, h3, html,
                                              mark, infobox, learnbox, minibox, table, summary, related, img)

AUTHOR_ID = 2  # USER1 -> momo (docs/wordpress.md)
STATE = ROOT / "backups" / "hadakanboutachi_love_shinjuku_state.json"
OUT_HTML = ROOT / "articles" / "hadakanboutachi_love_shinjuku.html"

TITLE = "はだかんぼうたちのLOVEはどこ？ホンノウスイッチと同じ新宿！"
SLUG = "hadakanboutachi-love-shinjuku-island"
EYECATCH = "hadakanbou_love_eyecatch_canva.jpg"

# red / blue (宮近海斗+松田元太)
C = dict(accent="#d9546a", border="#f5c6cf", bg="#fdf0f2", marker="mark_yellow")

X_SABA = "https://x.com/oshidoraEX/status/2117451708507066672"
X_HIJIRI = "https://x.com/oshidoraEX/status/1882421499312877851"
IMAGES = {
    "saba": ("hadakanbou_love_saba.jpg", "新宿アイランドタワー前のLOVEのオブジェに座る鯖崎涼(松田元太)", X_SABA),
    "hijiri": ("hadakanbou_love_hijiri.jpg", "新宿アイランドタワー前のLOVEのオブジェに座る秋山聖(宮近海斗)", X_HIJIRI),
}

MAP = html('<iframe src="https://maps.google.com/maps?q=%E6%96%B0%E5%AE%BF%E3%82%A2%E3%82%A4%E3%83%A9%E3%83%B3%E3%83%89%E3%82%BF%E3%83%AF%E3%83%BC+LOVE&t=&z=17&ie=UTF8&iwloc=&output=embed" '
           'width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>')

RELATED = [
    ("はだかんぼうたち2話にも紅孔雀？鯖崎のスマホに宮田快斗・松永界斗", f"{SITE}/?p=1472"),
    ("鯖崎涼はクズ？松田元太の役どころと原作のあらすじ", f"{SITE}/?p=1184"),
    ("はだかんぼうたちの見逃し配信(TVer)と関西の放送時間", f"{SITE}/?p=1186"),
]


def x_embed(url):
    u = url.replace("x.com", "twitter.com")
    return html(f'<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><a href="{u}">{u}</a></blockquote>'
                '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def build(M):
    c = C
    I = lambda k: img(M[k], IMAGES[k][1], f'<a href="{IMAGES[k][2]}">「はだかんぼうたち」「ホンノウスイッチ」公式X(@oshidoraEX)</a>')
    b = ""
    b += para(f"""
松田元太さん主演のドラマ『はだかんぼうたち』の公式Xが、2026年11月3日に「鯖とLOVEで待ち合わせ」というオフショットを投稿しました。
大きな赤い「LOVE」の文字の中に、スーツ姿の鯖崎涼(松田元太)がしゃがんでいる1枚です。
実はこの写真、宮近海斗さん主演の『ホンノウスイッチ』の公式Xが2025年1月に出した「聖とLOVEで待ち合わせ」と、同じ場所・同じポーズになっています。
撮影場所は{mark("東京・西新宿の新宿アイランドタワー前にある「LOVE」のオブジェ", c)}です。
この記事では、場所の決め手やアクセス、2つのドラマのつながりをまとめます。
""")
    b += infobox("撮影場所の情報", [
        ("撮影場所", "新宿アイランドタワー前の「LOVE」のオブジェ"),
        ("住所", "東京都新宿区西新宿6-5-1"),
        ("最寄り駅", "東京メトロ丸ノ内線「西新宿駅」すぐ"),
        ("作者", "ロバート・インディアナ(アメリカのポップアーティスト)"),
        ("見学", "屋外に置かれていて、いつでも無料で見られる"),
    ])
    b += learnbox(["「鯖とLOVEで待ち合わせ」の投稿の中身", "撮影場所が新宿アイランドのLOVEだとわかる決め手",
                   "ホンノウスイッチの聖と同じ場所・同じポーズの写真", "LOVEのオブジェの場所・アクセス・ジンクス",
                   "ホンノウスイッチとはだかんぼうたちはつながっている？"], c)

    # --- post
    b += h2("はだかんぼうたちの「鯖とLOVEで待ち合わせ」はどんな投稿？")
    b += minibox([("投稿日", "2026年11月3日"),
                  ("投稿したアカウント", "「はだかんぼうたち」公式X(@oshidoraEX)"),
                  ("文面", "「#オフはだかんぼうたち ＼鯖とLOVEで待ち合わせ／」"),
                  ("引用した投稿", "「ホンノウスイッチ」公式の「聖とLOVEで待ち合わせ」(2025年1月23日)")], c)
    b += x_embed(X_SABA)
    b += para("""
『はだかんぼうたち』と『ホンノウスイッチ』は、どちらもテレビ朝日の土曜深夜のドラマ枠「オシドラサタデー」の作品で、公式Xも同じアカウントを使っています。
今回の投稿は、約1年10か月前の「聖とLOVEで待ち合わせ」をそのまま引用する形で出されました。
文面も「聖」が「鯖」に変わっただけで、最初から見比べてもらうつもりで撮ったオフショットだとわかります。
""")
    b += I("saba")
    b += para("""
写真の鯖崎は、紺のスーツにストライプのネクタイ、黒の革靴という、劇中の仕事の日と同じような服装です。
「LOVE」の「E」と「V」のあいだのすき間に腰を下ろし、片手をポケットに入れて、少しおどけた顔でこちらを見ています。
赤い文字の内側には青と緑の色がのぞいていて、鯖崎のスーツの紺色がよく映えていました。
""")

    # --- location
    b += h2("はだかんぼうたちのLOVEの撮影場所は新宿アイランドタワー前")
    b += minibox([("撮影場所", "新宿アイランドタワー(新宿アイランド)の正面入口前"),
                  ("住所", "東京都新宿区西新宿6-5-1"),
                  ("アクセス", "東京メトロ丸ノ内線「西新宿駅」直結、都営大江戸線「都庁前駅」からも歩いてすぐ")], c)
    b += para("""
都内にはいくつか「LOVE」の文字のオブジェがありますが、写真の手がかりを1つずつ確かめると、西新宿の新宿アイランドのものだとわかります。
""")
    b += h3("決め手①赤・青・緑の配色と、斜めに傾いた「O」")
    b += para(f"""
オブジェは、「LO」と「VE」を2段に積み、左上の「O」だけを斜めに傾けたデザインです。
表は赤、文字の内側は青と緑に塗り分けられていて、これはアメリカの作家ロバート・インディアナさんの代表作{mark("「LOVE」", c)}の形そのものです。
新宿アイランドのLOVEは人が中に座れるほど大きく、写真のように「E」と「V」のあいだに腰かけられるサイズになっています。
""")
    b += h3("決め手②右上に見える歩道橋と高層ビル")
    b += para("""
写真の右上には、オブジェの後ろを横切るように通る屋根付きの歩道橋(ペデストリアンデッキ)が写っています。
背景にはガラス張りの高層オフィスビルと、街路樹の並ぶ広い歩道が広がっています。
西新宿の超高層ビル街の中にあり、ビルどうしを歩道橋でつないだ新宿アイランドならではの景色です。
""")
    b += h3("決め手③ホンノウスイッチの聖と同じ場所・同じ構図")
    b += I("hijiri")
    b += para(f"""
こちらは、2025年1月に『ホンノウスイッチ』の公式Xが投稿した、宮近海斗さん演じる秋山聖の写真です。
キャメルのダッフルコートにチェックのマフラーを巻いた聖が、鯖崎と{mark("まったく同じ「E」と「V」のあいだ", c)}にしゃがんでいます。
オブジェの向き、右上の歩道橋、後ろのビルまで同じで、カメラを構えた位置もほぼ同じだとわかります。
""")
    b += table(["", "ホンノウスイッチ", "はだかんぼうたち"], [
        ["役", "秋山聖(宮近海斗)", "鯖崎涼(松田元太)"],
        ["投稿日", "2025年1月23日", "2026年11月3日"],
        ["文面", "聖とLOVEで待ち合わせ", "鯖とLOVEで待ち合わせ"],
        ["服装", "ダッフルコート・マフラー・デニム", "紺のスーツ・ネクタイ・革靴"],
        ["背景の木", "黄色く色づいた街路樹", "緑の葉が残る街路樹"],
    ], c)
    b += para("""
大きく違うのは季節感です。
聖の写真は街路樹が黄色く色づいていて、秋の終わりごろに撮ったとみられます。
鯖崎の写真はまだ葉が緑で、同じ場所でも撮った時期がちがうことがよくわかります。
""")

    # --- LOVE info
    b += h2("新宿アイランドのLOVEのオブジェとは？")
    b += table(["項目", "内容"], [
        ["作品名", "LOVE"],
        ["作者", "ロバート・インディアナ(1928〜2018年)"],
        ["場所", "新宿アイランドタワー正面入口前(東京都新宿区西新宿6-5-1)"],
        ["アクセス", "東京メトロ丸ノ内線「西新宿駅」直結/都営大江戸線「都庁前駅」から徒歩約5分/JR「新宿駅」西口から徒歩約10分"],
        ["料金", "無料(屋外にあり、いつでも見られる)"],
    ], c)
    b += para("""
「LOVE」は、ロバート・インディアナさんが1960年代から手がけてきたシリーズで、ニューヨークやフィラデルフィアなど世界各地に置かれています。
新宿アイランドのLOVEは、ビル街の中でもひときわカラフルで目立つため、昔から待ち合わせの目印として親しまれてきました。
""")
    b += para(f"""
このオブジェには、{mark("「VとEのあいだを体に触れずに通り抜けると恋が叶う」", c)}というジンクスもあります。
鯖崎と聖が座っていたのは、まさにそのVとEのあいだです。
恋愛ドラマのオフショットにこの場所が選ばれたのも、ジンクスにかけた遊び心なのかもしれません。
""")
    b += MAP

    # --- connection
    b += h2("ホンノウスイッチとはだかんぼうたちはつながってる？")
    b += para("""
今回の投稿を見て、SNSでは「2つのドラマは同じ世界線なの？」と考えるファンも出てきています。
""")
    b += html(f'<div style="border:1px solid {C["border"]};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{C["bg"]};">'
              f'<p style="margin:0 0 6px 0;font-weight:bold;font-size:0.9em;color:{C["accent"]};">SNSの声</p>'
              '<p style="margin:0;font-size:0.95em;">「ホンノウスイッチとはだかんぼうたち、なにかある？宮近くんのクランクアップに元太くん来てたし、鯖のスマホに&quot;カイト&quot;いるし。同じ世界線だったりする？」</p></div>')
    b += para("""
ファンがつながりを感じる理由は、大きく3つあります。
""")
    b += table(["つながり", "内容"], [
        ["同じドラマ枠", "どちらもテレビ朝日「オシドラサタデー」(土曜23時)の作品"],
        ["クランクアップ", "2025年3月、『ホンノウスイッチ』の宮近海斗のクランクアップを松田元太がお祝い"],
        ["鯖崎のスマホ", "第2話で鯖崎の連絡先に「宮田快斗」「海斗」の名前が登録されていた"],
        ["LOVEのオフショット", "同じ場所・同じポーズ・同じ文面でオフショットを投稿"],
    ], c)
    b += para(f"""
『ホンノウスイッチ』の撮影が終わったときには、松田元太さんが宮近海斗さんのクランクアップをお祝いしたことが報じられました。
さらに『はだかんぼうたち』第2話では、鯖崎のスマホの連絡先に「宮田快斗」「海斗」という、宮近さんを思わせる名前が入っていました。
くわしくは<a href="{SITE}/?p=1472">鯖崎のスマホの連絡先の記事</a>でまとめています。
""")
    b += para("""
ただし、公式から「2つのドラマは同じ世界の話」という説明は出ていません。
『ホンノウスイッチ』はゲーム会社で働く幼なじみのピュアなラブストーリー、『はだかんぼうたち』は大人の恋愛と人間関係を描くドラマで、話の中身も直接はつながっていません。
同じ枠の先輩ドラマへのオマージュと、トラジャのメンバー同士の仲の良さを生かしたファンサービスと見るのが自然でしょう。
""")

    # --- visit
    b += h2("LOVEのオブジェに聖地巡礼するときのポイント")
    b += summary([
        "丸ノ内線の西新宿駅から地上に出ればすぐ。新宿駅西口からも歩いて10分ほど",
        "鯖崎・聖と同じ写真を撮るなら、「E」と「V」のあいだに座り、右上に歩道橋が入る向きから撮る",
        "平日の朝夕は会社員の通勤路になるので、人の少ない土日や昼すぎがねらい目",
        "ほかの人も写真を撮りに来る人気スポット。長い時間ひとりじめしないよう順番にゆずり合う",
        "秋の終わりは、聖の写真のように黄色い街路樹といっしょに撮れる",
    ], c)
    b += para("""
新宿駅からも歩ける距離なので、買い物や東京都庁の展望室とあわせて立ち寄りやすい場所です。
鯖崎のスーツ姿か、聖のダッフルコート姿か、どちらのポーズをまねするか考えながら行くのも楽しそうです。
""")

    # --- summary
    b += h2("まとめ")
    b += summary([
        "『はだかんぼうたち』公式Xが2026年11月3日に「鯖とLOVEで待ち合わせ」のオフショットを投稿",
        "撮影場所は東京・西新宿の新宿アイランドタワー前にある「LOVE」のオブジェ",
        "『ホンノウスイッチ』公式の「聖とLOVEで待ち合わせ」(2025年1月)と同じ場所・同じポーズ",
        "丸ノ内線「西新宿駅」すぐで、いつでも無料で見られる",
        "2つのドラマが同じ世界という公式の説明はなく、同じ枠・紅孔雀つながりのファンサービスとみられる",
    ], c)
    b += para("""
宮近さんの聖から松田さんの鯖崎へ、同じオシドラサタデー枠のバトンがLOVEのオブジェでつながったような、ファンにはうれしい投稿でした。
新宿に行く機会があれば、2人と同じ「E」と「V」のあいだで写真を撮ってみてはいかがでしょうか！
""")
    b += related("はだかんぼうたちの関連記事", RELATED, c)
    return b


def plain_len(s):
    return len(re.sub(r"<[^>]+>|\s", "", s))


if __name__ == "__main__":
    if "--dry" in sys.argv:
        fake = {"media_details": {"sizes": {"large": {"source_url": "x", "width": 1, "height": 1}}, "width": 1, "height": 1},
                "source_url": "x"}
        body = build({k: fake for k in IMAGES})
        OUT_HTML.write_text(body, encoding="utf-8")
        print(len(TITLE), TITLE, "chars:", plain_len(body))
        sys.exit(0)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"media": {}}
    for k, (fn, alt, _) in IMAGES.items():
        if k not in state["media"]:
            state["media"][k] = upload_media(ROOT / "images" / fn, fn, alt)
    if "eyecatch" not in state:
        state["eyecatch"] = upload_media(ROOT / "images" / EYECATCH, EYECATCH,
                                         "はだかんぼうたちのLOVEのオブジェの撮影場所を紹介する記事のアイキャッチ")["id"]
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    if "--post" not in sys.argv:
        body = build(state["media"])
        OUT_HTML.write_text(body, encoding="utf-8")
        print("built", OUT_HTML, "chars:", plain_len(body), "-> honorific.py fix のあと --post で投稿")
        sys.exit(0)
    body = OUT_HTML.read_text(encoding="utf-8")  # honorific.py fix 済みのものを送る
    payload = {"title": TITLE, "content": body, "slug": SLUG, "status": "draft", "categories": [3, 7, 9],
               "author": AUTHOR_ID, "featured_media": state["eyecatch"]}
    r = api(f"posts/{state['post']}" if state.get("post") else "posts", payload)
    state["post"] = r["id"]
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print("POST", r["id"], r["status"], f"{SITE}/?p={r['id']}")
