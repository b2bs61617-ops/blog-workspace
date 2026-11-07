# -*- coding: utf-8 -*-
"""chomoand-4.blog: 「Would You Like One?」MVのラーメン屋(虎美寿ラーメン)ロケ地=二俣川の大龍飯店 (2026-11-07, オシリ依頼).

根拠:
- 公式MV(G056SzS3fg8, 2025-04-27公開)のフレーム: 外観は赤レンガの建物に「虎美寿ラーメン」の看板・のれん・提灯を
  付けたもの。店内は赤い丸椅子・番号札付きの木のカウンター・短冊メニュー。
- ファンの訪問報告(X, 2026-11-03)の写真: 店内に「当店がMV撮影に使われました」のPOP、外観は「中華料理 大龍飯店」、
  カウンター・丸椅子がMVと一致。→ 投稿の画像・リンクは載せない(第三者投稿ルール)。
- ホットペッパーの二俣川店の外観写真(赤レンガ3階建て、入口上に赤い「大龍飯店」の看板)がファン写真と一致。
- 店舗情報: 公式(ghwn100.gorp.jp)・ホットペッパー(strJ000212315)・相鉄ブログ。
- 撮影は2025年3月上旬、都内スタジオ+ラーメン屋を貸し切り(THE FIRST TIMES)。監督HQF & SAMSON、振付KABAO・Shungo(暴走族役でも出演)。
"""
import json, re, subprocess, sys
from urllib.parse import quote

from build_and_post_hadakanboutachi_5 import (ROOT, SITE, api, upload_media, para, h2, h3, html,
                                              mark, infobox, learnbox, minibox, table, summary, related, img)

AUTHOR_ID = 2  # momo (オシリと作った記事)
C = dict(accent="#7e57c2", border="#d9cdf0", bg="#f5f2fb", marker="mark_yellow")  # group color

MV = "https://www.youtube.com/watch?v=G056SzS3fg8"
MK = "https://www.youtube.com/watch?v=Mm2c9MDhk8s"
TITLE = "【未】トラジャのラーメンMVロケ地はどこ？二俣川の大龍飯店と判明！"
SLUG = "travis-japan-would-you-like-one-ramen-location"
IMG_DIR = ROOT / "images" / "tj_wylo_ramen"
STATE = IMG_DIR / "_state.json"
EYECATCH = IMG_DIR / "tj_wylo_ramen_eyecatch_canva.jpg"
SRC = f"YouTube「Travis Japan 'Would You Like One?' Music Video」"

IMAGES = {
    "ext": ("tj_wylo_ramen_ext.jpg", "虎美寿ラーメンの看板をつけた赤レンガの店の前に並ぶTravis Japanの7人"),
    "sign": ("tj_wylo_ramen_sign.jpg", "Travis RAMENと書かれた虎美寿ラーメンの立て看板"),
    "counter": ("tj_wylo_ramen_counter.jpg", "赤い丸椅子と番号札が並ぶ木のカウンター席"),
    "wide": ("tj_wylo_ramen_wide.jpg", "テーブル席が並ぶ店内を歩くメンバー"),
    "menuwall": ("tj_wylo_ramen_menuwall.jpg", "短冊メニューが並ぶ厨房で手を振るメンバー"),
    "gourmet": ("tj_wylo_ramen_gourmet.jpg", "虎美寿ラーメンを食べるグルメなおじいさん"),
    "members": ("tj_wylo_ramen_members.jpg", "テーブルに身を乗り出してリアクションするTravis Japanの7人"),
    "entrance": ("tj_wylo_ramen_entrance.jpg", "入口の横のレジ台にもたれるメンバー"),
    "street": ("tj_wylo_ramen_street.jpg", "出前に向かう途中、大勢の人に追いかけられながら自転車で走るメンバー"),
}

RELATED = [
    ("【On My Road】新曲MVの撮影場所と撮影日は？", f"{SITE}/when-and-where-will-travis-jap-108"),
    ("【よにの】松倉海斗のロケ地はどこ？ラーメンは入鹿TOKYO六本木！", f"{SITE}/matsukura-kaito-yonino-channel-locations-2393"),
    ("【原宿散歩】宮近海斗と中村海人のロケ地は？なに食べた？", f"{SITE}/chakaumi-harajuku-sanpo-location-1572"),
    ("トラジャのミュージカル・声優経歴は？劇団四季やディズニーも！", f"{SITE}/toraja-musical-voice-actor-car-903"),
    ("【パナスタ】トラジャのJリーグ特別ライブ決定！チケットはいつから？", f"{SITE}/travis-japan-pansta-live-1212-2352"),
]


def yt(url):
    return (f'<!-- wp:embed {{"url": "{url}", "type": "video", "providerNameSlug": "youtube", "responsive": true, '
            f'"className": "wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->\n'
            f'<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 '
            f'wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\n{url}\n</div></figure>\n<!-- /wp:embed -->')


def gmap(q):
    return html(f'<iframe src="https://maps.google.com/maps?q={quote(q)}&t=&z=16&ie=UTF8&iwloc=&output=embed" '
                f'width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>')


def build(M):
    I = lambda k: img(M[k], IMAGES[k][1], SRC)
    b = ""
    b += para(f"""
Travis Japanの「Would You Like One?」のMVに出てくる、レトロなラーメン屋「虎美寿(トラビス)ラーメン」。
作中の店名は架空のものですが、撮影に使われたのは実在するお店です。
MVの映像と店舗の写真を見くらべたところ、{mark("ロケ地は神奈川県横浜市旭区・二俣川にある中華料理店「大龍飯店」", C)}だとわかりました。
この記事では、MVのどのシーンで特定できたのかという理由と、お店の場所・営業時間・メニュー、聖地巡礼のポイントをまとめます。
""")
    b += infobox("MVの情報", [
        ("曲名", "Would You Like One?(Travis Japan)"),
        ("タイアップ", "映画『たべっ子どうぶつ THE MOVIE』主題歌(2025年5月1日公開)"),
        ("配信日", "2025年4月28日(MVは4月27日公開)"),
        ("監督", "HQF & SAMSON"),
        ("作中の店名", "虎美寿(トラビス)ラーメン"),
        ("ロケ地", "大龍飯店(横浜市旭区二俣川)"),
    ])
    b += learnbox(["虎美寿ラーメンのロケ地はどこ？", "大龍飯店と特定できた理由", "MVのストーリーと撮影の様子",
                   "大龍飯店の場所・アクセス・営業時間", "大龍飯店の名物メニュー", "聖地巡礼で気をつけたいこと"], C)
    b += yt(MV)

    # --- answer
    b += h2("トラジャのラーメンMVのロケ地は二俣川の大龍飯店")
    b += minibox([("店名", "中華料理 大龍飯店(だいりゅうはんてん)"),
                  ("場所", "神奈川県横浜市旭区二俣川1-64(相鉄線・二俣川駅から徒歩5〜6分)"),
                  ("MVでの役", "メンバー7人が切り盛りする「虎美寿(トラビス)ラーメン」")], C)
    b += para(f"""
「Would You Like One?」のMVは、味も見た目もイマイチだった「虎美寿ラーメン」を、メンバーがスープと麺を研究して立て直していくストーリーです。
報道では、撮影は2025年3月上旬に、都内のスタジオと{mark("貸し切りにしたラーメン屋", C)}で行われたと伝えられていました。
ただ、どこのお店なのかは公式には発表されていません。
""")
    b += para("""
そのお店が、二俣川駅の近くにある「大龍飯店」です。
地元では「豚バラニンニク丼」で知られる、町の中華料理店で、MVではお店の看板やのれんを「虎美寿ラーメン」のものに付け替えて撮影されていました。
""")
    b += I("ext")

    # --- reasons
    b += h2("大龍飯店と特定できた3つの理由")
    b += para("""
MVの映像と、大龍飯店の店舗写真をコマ送りで見くらべました。
決め手になったのは、次の3つです。
""")
    b += table(["見くらべたところ", "MV", "大龍飯店"], [
        ["建物の外観", "赤レンガの壁、入口の上に看板", "赤レンガの3階建て、入口の上に赤い看板"],
        ["入口のつくり", "看板の右上に防犯カメラ", "同じ位置に防犯カメラ"],
        ["カウンター席", "赤い丸椅子と番号札つきの木のカウンター", "同じ赤い丸椅子と番号札つきのカウンター"],
        ["お店からの案内", "-", "店内に「当店がMV撮影に使われました」のPOP"],
    ], C)

    b += h3("理由1:赤レンガの外観と入口のつくりが同じ")
    b += para(f"""
MVの1分すぎ、メンバー7人がお店の前に並ぶシーンでは、{mark("赤いレンガの壁", C)}に「虎美寿ラーメン」の白い看板、赤いのれん、「ラーメン」と書かれた提灯が飾られています。
大龍飯店も赤レンガの建物で、入口の上の看板の位置や、その右上にある防犯カメラの位置までMVと同じでした。
撮影のときは、ふだんの赤い「大龍飯店」の看板の上に、虎美寿ラーメンの看板をかぶせていたと考えられます。
""")
    b += para("""
入口の横には「Travis RAMEN」と書かれた立て看板も置かれていました。
看板には「New!」の文字とラーメンのイラストが入っていて、「Travis」のロゴ入りの丼が描かれているのも細かいポイントです。
""")
    b += I("sign")

    b += h3("理由2:赤い丸椅子と番号札のカウンターが一致")
    b += para(f"""
MVの冒頭は、お客さんがいない店内のカウンターから始まります。
木のカウンターの前に{mark("赤い座面の丸椅子", C)}が並び、席ごとに「1」「2」と番号札が貼られているのが特徴です。
大龍飯店のカウンター席も、同じ形の赤い丸椅子と番号札がそのまま使われています。
""")
    b += I("counter")
    b += para("""
カウンターの上の割りばし立てや調味料のボトル、カウンターの奥のステンレスの厨房も、ふだんのお店の様子とよく似ています。
厨房の上に並んだ短冊メニューは、MV用に作られた小道具のようで、「天津飯」「八宝菜」「ギョーザ」などの品名と値段が書かれていました。
""")
    b += I("menuwall")

    b += h3("理由3:お店にMV撮影のPOPが飾られている")
    b += para(f"""
大龍飯店の店内には、{mark("「当店がMV撮影に使われました」", C)}と書かれたPOPが飾られています。
POPには、虎美寿ラーメンの前に並ぶメンバー7人の写真と、「Would You Like One?」のジャケット写真が入っていて、お店公認のロケ地になっています。
SNSでも、実際にお店を訪れたファンから「お店の人が『いっぱい見ていって』と声をかけてくれた」「ボリューム満点でおいしかった」という声が上がっていました。
""")

    # --- story
    b += h2("虎美寿ラーメンのMVのストーリー")
    b += para("""
MVの舞台は、1980年代を思わせるレトロなラーメン屋です。
メンバーは虎美寿ラーメンの店員になりきっていて、最初はお客さんもまばらで、カウンターでぐったりしているところから始まります。
""")
    b += I("wide")
    b += para(f"""
そこから、スープと麺を研究して作った一杯を、お店にやってきた{mark("グルメなおじいさん", C)}が「美味」と認めたことで、お店は大繁盛。
テレビの取材まで来るほどの人気店になっていきます。
""")
    b += I("gourmet")
    b += I("members")
    b += para("""
ところが後半では、暴走族がお店に乗り込んできて、ラーメンの価値がおびやかされるピンチに。
メンバーはダンスバトルで店を守ります。
この暴走族を演じているのは、この曲の振付を担当したKABAOさんとShungoさんたちで、振付師がそのまま出演しているのも見どころです。
""")
    b += I("entrance")
    b += para("""
ラーメンの丼の上でメンバーが踊るシーンや、金色の「美味」の文字の前で踊るシーンは、スタジオで撮影したCGの合成です。
お店が大人気になると、出前の注文も入ってきます。
メンバーが「虎美寿ラーメン」の袋を持って入口から飛び出し、自転車で出前に向かう途中で、大勢の人に追いかけられるシーンもあります。
この出前のシーンはお店の近くの道路で撮影したとみられますが、場所までは特定できていません。
""")
    b += I("street")

    b += h3("メイキングでは撮影の合間も店員になりきり")
    b += para(f"""
2025年5月3日には、MVのメイキング映像も公開されています。
「ラーメン1つ、かため」「替え玉ありますか？」とお客さん役とやりとりする場面など、撮影の合間も{mark("ラーメン屋の店員になりきっている", C)}メンバーの姿が見られます。
松田元太さんが映画で声を担当したライオンくんにちなんだ「ライオンダンス」の振付が入っていることも、メイキングで紹介されていました。
""")
    b += para("""
メンバーは「まさか俺らがラーメン屋を経営することになるとは思わなかった」と話しつつ、「コンセプトが面白くて、楽しみながらやらしてもらってます」と撮影をふり返っていました。
MVを見たあとにメイキングを見ると、大龍飯店の厨房やカウンターがもっとよくわかります。
""")
    b += yt(MK)

    # --- shop info
    b += h2("大龍飯店の場所・アクセス・営業時間")
    b += para(f"""
大龍飯店があるのは、相鉄線の二俣川駅から歩いて5〜6分ほどのところです。
二俣川駅は、横浜駅から相鉄線で15分ほど。
神奈川県の運転免許センターがある駅としても知られています。
""")
    b += minibox([("住所", "神奈川県横浜市旭区二俣川1-64"),
                  ("アクセス", "相鉄本線・いずみ野線 二俣川駅から徒歩5〜6分"),
                  ("営業時間", "11:00〜21:30(ラストオーダー20:45)"),
                  ("定休日", "なし(年末年始は休み)"),
                  ("席数", "110席(1階・2階、カウンター席・座敷・個室あり)"),
                  ("駐車場", "あり(7台)")], C)
    b += gmap("大龍飯店 横浜市旭区二俣川1-64")
    b += para("""
110席ある大きなお店で、1階にはMVにも出てきたカウンター席とテーブル席、ほかに座敷や個室もあります。
宴会にも使われているお店なので、大人数でも入りやすいのがうれしいポイントです。
営業時間や定休日は変わることがあるので、行く前にお店の情報を確認しておきましょう。
""")

    b += h3("大龍飯店の名物は豚バラニンニク丼")
    b += para(f"""
大龍飯店の名物は、{mark("「豚バラニンニク丼」", C)}です。
2013年の「ガチ丼グランプリ」で銀賞をとったことのある一品で、スタジアムグルメのグランプリでもベストイレブンに選ばれています。
お弁当のテイクアウトもあり、地元では「二俣川の定番」として長く愛されているお店です。
""")
    b += para("""
ほかにも、横浜のご当地ラーメン「サンマーメン」や、麻婆チャーハン、ネギチャーシューチャーハン、餃子など、町の中華の定番メニューがそろっています。
どの料理もボリュームがあるのが特徴で、MVのように「美味！」と言いたくなる一皿が見つかるはずです。
店内のレジの近くには、小泉孝太郎さんなど、お店を訪れた有名人のサインも飾られています。
""")

    # --- tips
    b += h2("大龍飯店へ聖地巡礼するときのポイント")
    b += para("""
大龍飯店は、地元のお客さんでにぎわう営業中のお店です。
MVの撮影は貸し切りで行われましたが、ふだんはお昼どきを中心に混み合うので、ランチのピークをずらして行くのがおすすめです。
""")
    b += para("""
店内で写真を撮るときは、ほかのお客さんが写り込まないように気をつけて、お店の人にひと声かけてから撮りましょう。
MVで使われたカウンター席に座りたいときも、混雑時は無理を言わず、空いているときにお願いするのがマナーです。
注文をしてしっかり食べることが、ロケ地を応援することにもつながります。
""")

    # --- summary
    b += h2("まとめ")
    b += summary([
        "Would You Like One?のMVの虎美寿ラーメンは架空の店で、ロケ地は二俣川の大龍飯店",
        "赤レンガの外観・防犯カメラの位置・赤い丸椅子のカウンターがMVと一致",
        "お店には「当店がMV撮影に使われました」というPOPが飾られている",
        "撮影は2025年3月上旬。看板やのれんを付け替えて撮影された",
        "大龍飯店は二俣川駅から徒歩5〜6分、11:00〜21:30、定休日なし",
        "名物は豚バラニンニク丼。サンマーメンなど町中華の定番もそろう",
    ], C)
    b += para("""
トラジャのメンバーが店員になりきって踊った虎美寿ラーメンのお店は、横浜の二俣川で今もふつうに営業している町の中華料理店でした。
MVを見返してから行くと、カウンターや厨房を見るだけでも楽しめるはずです。
ボリューム満点の中華を味わいに、ぜひ足を運んでみてはいかがでしょうか！
""")
    b += related("トラジャの関連記事", RELATED, C)
    return b


def plain_len(s):
    return len(re.sub(r"<[^>]+>|\s", "", s))


if __name__ == "__main__":
    t = TITLE.replace("【未】", "")
    assert len(t) <= 35, (len(t), t)
    tmp = ROOT / "tmp_tj_wylo_ramen.html"
    if "--dry" in sys.argv:
        fake = {"media_details": {"sizes": {"large": {"source_url": "x", "width": 1, "height": 1}}, "width": 1, "height": 1},
                "source_url": "x", "id": 0}
        body = build({k: fake for k in IMAGES})
        tmp.write_text(body, encoding="utf-8")
        print(len(t), TITLE, "chars:", plain_len(body))
        sys.exit(0)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    M = state.setdefault("media", {})
    for k, (fn, alt) in IMAGES.items():
        if k not in M:
            M[k] = upload_media(ROOT / "images" / fn, fn, alt)
            STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        print("img", k, M[k]["id"])
    body = build(M)
    tmp.write_text(body, encoding="utf-8")
    names = "小泉孝太郎,KABAO,Shungo"
    for mode in ("fix", "check"):
        subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), mode, "--group", "travis", "--names", names, str(tmp)], check=True)
    body = tmp.read_text(encoding="utf-8")
    if "eyecatch" not in state:
        eye = subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
                              "--main", "虎美寿ラーメン",
                              "--bottom", "MVのロケ地はどこ？", "--bottom", "二俣川の大龍飯店と判明！",
                              "--color-key", "group", "--out", str(EYECATCH)],
                             capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(eye.stdout[-300:], eye.stderr[-300:])
        if eye.returncode == 0:
            state["eyecatch"] = upload_media(EYECATCH, EYECATCH.name, "トラジャのWould You Like One?MVのラーメン屋のロケ地を紹介する記事のアイキャッチ")
            STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    payload = {"title": TITLE, "content": body, "slug": SLUG, "status": "draft", "categories": [3], "author": AUTHOR_ID}
    if "eyecatch" in state:
        payload["featured_media"] = state["eyecatch"]["id"]
    path = f"posts/{state['post_id']}" if "post_id" in state else "posts"
    r = api(path, payload)
    state["post_id"] = r["id"]
    STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    print("POST", r["id"], r["status"], r.get("slug"), "eyecatch", payload.get("featured_media"))
