# -*- coding: utf-8 -*-
"""chomoand-4.blog: 『小麦とバターと復讐と』第7話(2026-11-18放送)直後の疑問記事(2026-11-18).

Xの#小麦とバターと復讐と の「？」= ①冷蔵庫に2人を閉じこめた犯人は誰？伊能先生がいたのはわざと？ ②8話はどうなる？
根拠:
- 公式X(@suidora11) 2123061648454025569: 8話PR動画+本文「冷蔵庫に閉じ込められたミチルと優吾」
  「辻岡さんのことは、僕が守ります」「突如現れた優吾の"幼馴染"ユナ」/8話は11月25日(水)23時。画像はこの動画から切り出し。
- ザテレビジョン 8話ページの出演者: 清乃あさ姫=後野マナカ、烏森まど=戸倉サツキ、寺本莉緒=杉本カナエ。ユナ役は未記載。
- 7話の流れ: 公式あらすじ(小林のパン開発・試作品の評価・優吾8年ぶりの修業)+放送中のXの声(肩で寝落ち/マナカの仕業の声多数)。
- 原作(ciatr要約): マナカは優吾のはとこ、ミチルに「優吾には許嫁がいる」と告げる。最終的にミチルと優吾は結ばれる。

python tools/_build_komugi_ep7_yuna.py --upload      画像アップ(articles/komugi_ep7_yuna_media.json)
python tools/_build_komugi_ep7_yuna.py --build-only  articles/komugi_ep7_yuna.html
python tools/_build_komugi_ep7_yuna.py               下書き投稿(【未】付き)
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "travis"
KEY = "komugi_ep7_yuna"
TITLE = "【小麦とバターと復讐と】伊能先生の幼馴染ユナは誰？冷蔵庫の犯人も！"
SLUG = "komugi-butter-fukushu-ep7-yuna-reizouko"
CATEGORIES = [3, 8]
NAMES = ["伊原六花", "清乃あさ姫", "寺本莉緒", "朝加真由美", "小手伸也", "味方良介", "烏森まど", "小林きな子", "トラウデン直美"]
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "小麦とバターと復讐と7話の幼馴染ユナと冷蔵庫の犯人を解説する記事のアイキャッチ"
X_TEXT = "伊能先生と冷蔵庫に閉じこめられるとか夢すぎて無理😭💕 わざと閉めたのは誰…？しかも来週は“幼なじみ”の女の子まで登場するってほんと！？七五三掛龍也くんの「僕が守ります」だけで1週間生きられる🥹🍞"
X_TAGS = "#小麦とバターと復讐と #七五三掛龍也 #TravisJapan"

SRC = "https://x.com/suidora11/status/2123061648454025569"
MEDIA_FILE = blogkit.ARTICLES / (KEY + "_media.json")
S = "https://chomoand-4.blog/"
EP6 = S + "komugi-butter-fukushu-ep6-filming-locations-2636"
SANDO = S + "komugi-butter-fukushu-atsuyaki-tamago-sando-recipe-2638"
EP5 = S + "komugi-butter-fukushu-ep5-filming-locations-2283"
GRAIN = S + "shimekake-ryuya-komugi-ino-grain-tote-1752"
COLLAB = S + "komugi-butter-fukushu-bread-espresso-collab-1677"

IMAGES = {
    "f001": "冷蔵室の中で、外の様子をうかがう伊能優吾(七五三掛龍也)",
    "f004": "冷蔵室の扉の取っ手に、モップの柄がつっかえ棒のように差しこまれている",
    "f008": "冷蔵室に閉じこめられ、おどろいた顔のミチル(伊原六花)",
    "f013": "段ボールにくるまって寒さをしのぐミチルと伊能優吾",
    "f017": "寒さの中で身を寄せ合うミチルと伊能優吾",
    "f034": "サングラスを外す、優吾の幼なじみ・ユナ",
    "f036": "料亭「小林」で、ヤエの前で優吾の腕に手をそえるユナ",
    "f055": "8話の予告で、おどろいた表情を見せる伊能優吾(七五三掛龍也)",
}

b = blogkit.Blocks("#d4789a", "#f2cfdc", "#fdf3f6")


def mark(t):
    return '<strong><span class="swl-marker mark_pink" style="font-size:1.15em;">{}</span></strong>'.format(t)


def fig(M, k):
    m = M[k]
    sz = m["media_details"]["sizes"]
    large = sz.get("large") or sz.get("full")
    medium = sz.get("medium")
    full = sz.get("full") or {"source_url": m["source_url"], "width": m["media_details"]["width"],
                              "height": m["media_details"]["height"]}
    srcset = ", ".join(([medium["source_url"] + " {}w".format(medium["width"])] if medium else [])
                       + [large["source_url"] + " {}w".format(large["width"]), full["source_url"] + " {}w".format(full["width"])])
    return b.html('<figure class="wp-block-image size-large"><img src="{}" alt="{}" width="{}" height="{}" '
                  'style="max-width:100%;height:auto;" srcset="{}" sizes="(max-width: 1024px) 100vw, 1024px">'
                  '<figcaption style="font-size:0.8em;color:#888;">出典:{}</figcaption></figure>'
                  .format(large["source_url"], IMAGES[k], large["width"], large["height"], srcset, SRC))


def related(links):
    lis = "".join('<li><a href="{}">{}</a></li>'.format(u, t) for t, u in links)
    return b.html('<div style="border:1px solid #f2cfdc;border-left:4px solid #d4789a;border-radius:4px;'
                  'padding:14px 18px;margin:0 0 16px 0;background:#fdf3f6;">'
                  '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">小麦とバターと復讐との関連記事</p>'
                  '<ul style="margin:0;padding-left:1.3em;">{}</ul></div>'.format(lis))


def build(M):
    o = ""
    o += b.p("『小麦とバターと復讐と』の第7話が、11月18日に放送されました。",
             "ラストでミチルが冷蔵室に閉じこめられ、なんと奥には伊能先生も！という急展開でした。")
    o += b.p("放送直後に公開された8話の予告では、" + mark("伊能先生の「幼なじみ」ユナ") + "が登場します。",
             "閉じこめたのは誰なのか、ユナは何者なのかを、予告と原作から読み解きます。")
    o += b.table(("項目", "内容"), [
        ("ドラマ", "小麦とバターと復讐と"),
        ("第7話", "2026年11月18日(水)23時"),
        ("第8話", "2026年11月25日(水)23時"),
        ("放送局", "カンテレ・フジテレビ系"),
        ("七五三掛龍也の役", "伊能優吾(料理教室の先生)"),
    ])
    o += b.wakaru(["7話のかんたんなあらすじ", "冷蔵庫に閉じこめた犯人は誰？", "伊能先生が中にいたのはわざと？",
                   "8話の予告の内容", "幼なじみ・ユナは誰？", "原作ではどうなる？"])

    # --- 7話
    o += b.h2("小麦とバターと復讐と7話のかんたんなあらすじ")
    o += b.mini(("ミチル", "料亭「小林」のパン作りを任される"), ("伊能先生", "8年ぶりに「小林」で修業をやり直す"))
    o += b.p("6話で、料亭「小林」の女将・ヤエが伊能先生のおばあさんだとわかりました。",
             "7話では、ミチルが「小林」のためのパン作りを任されます。")
    o += b.p("ところが、心をこめて作った試作のパンは、思うような評価をもらえません。",
             "ミチルは「小林」の料理を一から学び直し、何が足りないのかを考えます。")
    o += b.p("伊能先生も、8年ぶりに「小林」の調理場に戻りました。",
             "料理教室では先生だった伊能先生が、今度は白い調理着を着て、教わる側に回ります。")
    o += b.p("思うようにいかず悔しそうな顔を見せる場面も多く、ファンの胸がきゅっとなる回でした。",
             "そんな中、2人はおたがいのがんばる姿に支えられていきます。")
    o += b.h3("伊能先生がミチルの肩で寝落ち")
    o += b.p("つかれた伊能先生が、ミチルの肩にもたれて眠ってしまう場面もありました。",
             "放送中のXでは「寝顔がきれいすぎる」「かわいい」という声があふれていました。")
    o += b.p("帰ろうとするミチルに「あのっ、また明日…！」と声をかける姿も話題に。",
             "完全に好きな人への声のかけ方だ、と受け取った人も多かったようです。")

    # --- 犯人
    o += b.h2("冷蔵庫に閉じこめた犯人は誰？")
    o += b.mini(("答え", "「小林」の見習い・後野マナカ(清乃あさ姫)という見方が多い"))
    o += b.p("7話のラストで、ミチルは「小林」の冷蔵室に閉じこめられてしまいます。",
             "扉の取っ手には、モップの柄がつっかえ棒のように差しこまれていました。")
    o += fig(M, "f004")
    o += b.p("外から開かないように細工されているので、うっかりではなく" + mark("だれかがわざと閉めた") + "ことになります。",
             "放送を見た人の間では、「小林」の見習い・後野マナカのしわざだという声が多く上がりました。")
    o += b.p("マナカを演じているのは、清乃あさ姫さんです。",
             "「リベンジ・スパイ」や「クジャクのダンス、誰が見た？」などに出てきた若手の俳優さんです。")
    o += fig(M, "f008")
    o += b.h3("カナエを疑う声も")
    o += b.p("一方で、「またカナエ(寺本莉緒さん)が裏で仕込んでいるのでは」と疑う声もありました。",
             "カナエはもともとミチルの助手で、ミチルをねたんでいる人物だからです。")
    o += b.p("ただ、7話では卜部(小手伸也さん)がカナエに、ミチルへのいやがらせをやめるようくぎを刺していました。",
             "そのため、今回はカナエではなく、「小林」の中の人のしわざと見るのが自然かもしれません。")

    # --- わざと？
    o += b.h2("伊能先生が冷蔵庫の中にいたのはわざと？")
    o += b.mini(("答え", "犯人が知っていたかは不明。ミチルだけをねらった可能性が高そう"))
    o += b.p("閉じこめられたミチルがふり返ると、冷蔵室の奥には伊能先生が立っていました。",
             "「いつからいたの？」「涼しい顔で出てきた」と、Xはおどろきの声でいっぱいに。")
    o += fig(M, "f001")
    o += b.p("考えられるのは、次の2つです。")
    o += b.table(("考え方", "理由"), [
        ("ミチルだけをねらった", "犯人は中に伊能先生がいると気づかずに閉めた"),
        ("2人をくっつけたかった", "仲のいい2人をわざと一緒に閉じこめた"),
    ])
    o += b.p("扉を外から細工するほどなので、ミチルへのいやがらせだった見方が強めです。",
             "伊能先生は「小林」の跡取りなので、わざと閉じこめれば大問題になります。")
    o += b.p("つまり、" + mark("犯人も伊能先生が中にいるとは知らなかった") + "可能性が高そうです。",
             "「閉じこめたのが2人だったのは、犯人もびっくりかも」という声もありました。")

    # --- 8話予告
    o += b.h2("8話の予告の内容は？「僕が守ります」")
    o += b.mini(("8話", "2026年11月25日(水)23時"), ("見どころ", "冷蔵室の中で、2人が初めて本音を知る"))
    o += b.p("7話の放送後、公式Xで8話の予告動画が公開されました。",
             "予告の言葉は「絶体絶命」「初めて知る互いの本音」です。")
    o += fig(M, "f013")
    o += b.p("冷えきった冷蔵室で、2人は段ボールにくるまって寒さをしのぎます。",
             "そして伊能先生の「" + mark("辻岡さんのことは、僕が守ります") + "」というせりふが流れました。")
    o += fig(M, "f017")
    o += b.p("身を寄せ合う2人の姿に、Xでは「来週まで待てない」という声が続出。",
             "閉じこめられたことで、2人の距離が一気に近づく回になりそうです。")

    # --- ユナ
    o += b.h2("伊能先生の幼なじみ・ユナは誰？")
    o += b.mini(("答え", "8話から登場する、伊能優吾の幼なじみ"), ("演じる人", "11月18日時点で未発表"))
    o += b.p("予告の後半は「そして、事態は思わぬ方向へ」という言葉に切りかわります。",
             "公式の説明では、" + mark("突如あらわれた優吾の“幼馴染”ユナ") + "が新たな波乱を起こすそうです。")
    o += fig(M, "f034")
    o += b.p("ユナは、スーツケースを持って「小林」の玄関に立っていました。",
             "サングラスをかけた大人っぽい女性で、遠くから帰ってきたような雰囲気です。")
    o += fig(M, "f036")
    o += b.p("ヤエの前では、白い調理着の伊能先生の腕に、親しげに手をそえていました。",
             "おばあさんのヤエとも顔見知りのようで、昔から「小林」と深いつながりがありそうです。")
    o += b.p("ユナを演じる俳優さんの名前は、7話の放送直後の時点ではまだ出ていません。",
             "8話のキャストが発表されたら、この記事に書き足します。")
    o += fig(M, "f055")

    # --- 原作
    o += b.h2("原作ではどうなる？ユナは許嫁の可能性")
    o += b.mini(("原作のマナカ", "伊能優吾のはとこ"), ("原作の展開", "「優吾には許嫁がいる」とミチルに告げる"))
    o += b.p("『小麦とバターと復讐と』は、LINEマンガなどで配信されている漫画が原作です。",
             "原作では、マナカは伊能先生の「はとこ」として出てきます。")
    o += b.p("そのマナカが、ミチルに「優吾には許嫁がいる」と告げる場面があります。",
             "ドラマの「幼なじみ・ユナ」は、この許嫁にあたる人物なのかもしれません。")
    o += b.p("原作のマナカは、悪い記者と組んでミチルをわなにかけようともします。",
             "ドラマでも、ユナの登場をきっかけにマナカの動きが大きくなりそうです。")
    o += b.p("ただし、原作の最後で" + mark("ミチルと伊能先生はかけがえのないパートナーとして結ばれます") + "。",
             "ドラマは原作と結末を変える可能性もありますが、2人の恋の行方に期待したいですね。")
    o += b.p("伊能先生のこれまでの話は、" + b.link(EP6, "6話のロケ地の記事") + "や"
             + b.link(SANDO, "父の卵サンドのレシピの記事") + "でもくわしく紹介しています。")

    # --- まとめ
    o += b.h2("まとめ")
    o += b.checks([
        "7話のラストで、ミチルと伊能先生が「小林」の冷蔵室に閉じこめられた",
        "犯人は「小林」の見習い・後野マナカ(清乃あさ姫)という見方が多い",
        "伊能先生が中にいたのは、犯人も知らなかった可能性が高い",
        "8話の予告では「辻岡さんのことは、僕が守ります」というせりふが流れた",
        "8話から伊能先生の幼なじみ・ユナが登場。演じる人は未発表",
        "原作ではマナカが「優吾には許嫁がいる」と告げる展開がある",
    ])
    o += b.p("「僕が守ります」の一言だけで、1週間ドキドキが止まりません。",
             "ユナの登場で2人の関係がどうなるのか、11月25日の8話を楽しみに待ちましょう！")
    o += related([
        ("【小麦とバターと復讐と】第6話ロケ地は？料亭小林は千葉？病院は東京？", EP6),
        ("【小麦とバターと復讐と】伊能の父の卵サンドレシピは？", SANDO),
        ("【小麦とバターと復讐と】第5話ロケ地は？祝勝ランチは大塚のカフェ！", EP5),
        ("伊能先生のバッグはどこの？七五三掛龍也のトートはGRAIN！", GRAIN),
        ("【小麦とバターと復讐と】コラボメニューはどこで買える？徹底調査！", COLLAB),
    ])
    return o


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    wp = blogkit.WP(SITE)
    if "--publish" in sys.argv:
        state = json.loads((blogkit.ARTICLES / (KEY + "_posted.json")).read_text(encoding="utf-8"))
        blogkit.publish(SITE, state["post"], X_TEXT, X_TAGS)
        sys.exit()
    if "--upload" in sys.argv:
        ids = json.loads(MEDIA_FILE.read_text(encoding="utf-8")) if MEDIA_FILE.exists() else {}
        for k, alt in IMAGES.items():
            if k not in ids:
                ids[k] = wp.upload_media(str(blogkit.ROOT / "images" / "komugi_ep7_{}.jpg".format(k)), alt)
                MEDIA_FILE.write_text(json.dumps(ids, indent=1), encoding="utf-8")
                print("img", k, ids[k])
        sys.exit()
    ids = json.loads(MEDIA_FILE.read_text(encoding="utf-8"))
    M = {k: wp.get("/media/{}".format(v)) for k, v in ids.items()}
    out = blogkit.finalize(build(M), SITE, NAMES)
    if "--build-only" in sys.argv:
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
        sys.exit()
    if not EYECATCH.exists():
        cmd = [sys.executable, str(blogkit.ROOT / "tools" / "eyecatch_torahja_canva.py"),
               "--top", "小麦とバターと復讐と", "--main", "七五三掛龍也",
               "--bottom", "幼なじみユナは誰？", "--bottom", "冷蔵庫の犯人は？",
               "--color-key", "七五三掛龍也", "--out", str(EYECATCH)]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(r.stdout[-300:], r.stderr[-300:])
    blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                         update="--update" in sys.argv)
