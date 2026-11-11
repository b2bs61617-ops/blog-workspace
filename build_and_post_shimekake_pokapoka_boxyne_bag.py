# -*- coding: utf-8 -*-
"""七五三掛龍也が『ぽかぽか』(2026/11/11)のカバンの中身で持ってきたバッグ=MARNI BOXYNE スモールバッグ。
chomoand-4.blog下書き、【未】付き。香水の記事(ID2547)と2本に分けた(2026-11-11オシリ指示)。

- バッグ: MARNI BOXYNE スモールバッグ BMMP0186U0P929400M72 税込493,900円(高島屋・三越伊勢丹・松屋銀座で在庫あり、オシリが特定)
- チャーム: MARNI アニマル アルファベット チャーム「R」(PCMO0065Q0P894600M39、海外公式€395、JP公式ページなし)
- 画像はID2547用にアップ済みのTVerフレーム(2536/2537/2538)を流用

python build_and_post_shimekake_pokapoka_boxyne_bag.py --html
python build_and_post_shimekake_pokapoka_boxyne_bag.py --post <eye.jpg>   下書き投稿(二重投稿注意)
"""
import json, sys
from pathlib import Path

from build_and_post_hadakanboutachi_5 import api, upload_media, para, h2, h3, mark, learnbox, minibox, table, summary, related, img
from build_and_post_shimekake_pokapoka_bag_items import IMAGES, IDS_FILE, TVER, U, c, a, inner, MARNI_R

ROOT = Path(__file__).resolve().parent
HTML_OUT = ROOT / "tmp_shimekake_pokapoka_boxyne_bag.html"
PERFUME_ID = 2547
PRICE_BIG = '<strong><span class="swl-marker mark_yellow" style="font-size:1.5em;">税込493,900円</span></strong>'  # 11/11オシリ指示で大きく

TITLE = "【ぽかぽか】七五三掛龍也のバッグはどこの？マルニのBOXYNE！"
SLUG = "shimekake-ryuya-marni-boxyne-bag"
CATEGORIES = [3, 8]  # Travis Japan / 七五三掛龍也
AUTHOR = 2  # momo


def build(M):
    def pic(k, alt=None):
        return img(M[k], alt or IMAGES[k][2], TVER)

    b = ""
    b += para(f"""
Travis Japanの七五三掛龍也が、2026年11月11日の『ぽかぽか』(フジテレビ系)に出演しました。
「カバンの中身」のコーナーで、ふだん使っているバッグを持ってきてくれました。
そのバッグは、{mark("MARNI(マルニ)の「BOXYNE スモールバッグ」", c)}です。
""")
    b += para(f"""
値段は{PRICE_BIG}で、デパートで今も買えるモデルです。
この記事では、バッグの商品名や値段、そう言える理由を、放送の画面とあわせてまとめます。
バッグについていた「R」のチャームも紹介します。
""")
    b += learnbox([
        "七五三掛龍也のバッグのブランドと商品名",
        "バッグの値段とサイズ",
        "BOXYNEだとわかる理由",
        "どこで買えるか",
        "Rのチャームのブランド",
    ], c)

    # ---- answer ----
    b += h2("七五三掛龍也のバッグはマルニのBOXYNE スモールバッグ")
    b += minibox([("ブランド", "MARNI(マルニ)"), ("商品名", "BOXYNE(ボクシーン) スモールバッグ"),
                  ("品番", "BMMP0186U0P929400M72"), ("色", "こげ茶"),
                  ("サイズ", "高さ約18cm×幅約28cm×奥行き約12cm"), ("値段", PRICE_BIG)], c)
    b += pic("bag", "ぽかぽかで七五三掛龍也が持ってきたマルニのBOXYNE スモールバッグ")
    b += para("""
七五三掛龍也は、ドラマ『小麦とバターと復讐と』で共演中の伊原六花と一緒に出演しました。
赤い布の下から出てきたのは、こげ茶のレザーのバッグでした。
スタジオでは「カッコいい！」という声が上がっていました。
""")
    b += para("""
ツヤのあるシワっぽい革に、金色のファスナーが何本も並んだデザインです。
持ち手は2本で、手に持っても腕にかけても使えます。
ブラウンのジャケットに合わせて、秋らしいコーデになっていました。
""")

    b += h3("BOXYNEとわかる理由")
    b += pic("logo", "七五三掛龍也のバッグの正面にある金色のMARNIのロゴ")
    b += para("""
アップの画面では、正面に金色の「MARNI」の文字がはっきり映っています。
デパートの通販サイトにのっているBOXYNE スモールバッグの写真と、放送のバッグをくらべてみました。
すると、次のところが同じでした。
""")
    b += table(["見るところ", "放送のバッグ・BOXYNE"], [
        ["ロゴ", "持ち手のあいだに金色のMARNIの文字"],
        ["前ポケット", "ロゴの下に横長のポケット"],
        ["金具", "持ち手のつけ根に金色のリング"],
        ["ファスナー", "上に金色のファスナーが何本も並ぶ"],
        ["革", "ツヤのあるこげ茶のレザー"],
    ], c)
    b += para(f"""
形・色・金具の場所まで、すべてがそろっています。
そのため、七五三掛龍也のバッグは{mark("BOXYNE スモールバッグ", c)}とみられます。
""")

    b += h3("BOXYNEはどんなバッグ？")
    b += para("""
BOXYNEは、なめらかでツヤのあるカーフレザー(牛の革)で作られたバッグです。
ファスナーで開け閉めできる部屋が3つある「3層構造」になっています。
内側には、小物を差しこめるポケットもついています。
""")
    b += para("""
大きさは、高さ約18cm・幅約28cm・奥行き約12cmです。
A4の書類は入りませんが、毎日の荷物を入れるにはちょうどいいサイズです。
部屋が3つあるので、香水やカメラなどの小物を分けて入れられます。
""")
    b += para("""
七五三掛龍也のバッグには、香水・日傘2本・フィルムカメラ2台が入っていました。
スタジオでは「パンパンじゃない？」と聞かれ、「そうなんですよね」と笑っていました。
小さめのバッグに、こだわりの物をぎゅっとつめて持ち歩いているようです。
""")

    b += h3("値段とどこで買える？")
    b += para(f"""
BOXYNE スモールバッグの値段は、{PRICE_BIG}です。
2026年11月11日に見ると、高島屋・三越伊勢丹・松屋銀座のオンラインストアで在庫がありました。
在庫はお店ごとにちがうので、気になる人は早めにチェックしてみてください。
""")
    b += related("BOXYNE スモールバッグの購入先", [
        ("高島屋オンラインストア", "https://www.takashimaya.co.jp/"),
        ("三越伊勢丹オンラインストア", "https://www.mistore.jp/"),
        ("マルニ公式オンラインストア", "https://www.marni.com/ja-jp/"),
    ], c)

    # ---- charm ----
    b += h2("バッグのRのチャームもマルニ")
    b += minibox([("ブランド", "MARNI(マルニ)"), ("商品名", "アニマル アルファベット チャーム「R」とみられる"),
                  ("素材", "ブラウンのスエード×ラインストーン"), ("値段", "海外の公式サイトで395ユーロ")], c)
    b += pic("charm", "七五三掛龍也のバッグについたマルニのRのチャーム")
    b += para("""
バッグの持ち手には、キラキラした大きな「R」のチャームがついていました。
七五三掛龍也は「名前が龍也なので、Rになってて」と説明しています。
「同じブランドの？」と聞かれると、「ブランドのやつです」と答えていました。
""")
    b += para(f"""
マルニには、アルファベットを動物の形にした「アニマル アルファベット チャーム」があります。
{a(MARNI_R, "海外の公式サイト")}には、ブラウンのスエードにラインストーンをちりばめた「R」がのっていました。
Rの上の部分が動物の顔のような形になっていて、放送のチャームとよく似ています。
""")
    b += para("""
海外の公式サイトでの値段は395ユーロです。
2026年11月11日に日本の公式サイトを見ると、このチャームのページは見つかりませんでした。
今から買うなら、マルニの店舗に在庫を問い合わせるのが確実です。
""")
    b += para("""
七五三掛龍也は、このバッグとチャームを「ずっと愛用してます」と話していました。
自分のイニシャルを、同じブランドのチャームでさりげなく入れるのがおしゃれですね。
""")

    # ---- contents ----
    b += h2("バッグの中身は香水・日傘・カメラ")
    b += para(f"""
バッグの中から出てきたのは、香水・日傘・フィルムカメラの3つでした。
香水のうち1本は、{mark("松田元太とおそろい", c)}だと明かして話題になりました。
香水のブランドは、{inner(PERFUME_ID, "七五三掛龍也の香水はどこの？元太とおそろいはル ラボ！")}でくわしくまとめています。
""")
    b += para(f"""
日傘は「こわれたときのために」と2本持ち歩いていて、心配性な一面ものぞきました。
カメラは、{inner(1814, "インスタにも写っていたCONTAX T2")}と写ルンですの2台です。
""")

    # ---- marni ----
    b += h2("七五三掛龍也はマルニが好き")
    b += para(f"""
七五三掛龍也は、バッグ以外でもマルニのアイテムをよく身につけています。
インスタでは、{inner(1599, "マルニのベルト付きブルゾン")}を着た写真をのせていました。
大阪でのインスタライブで着ていた{inner(1336, "コートもマルニ")}でした。
""")
    b += para(f"""
御殿場のアウトレットでは、{inner(970, "マルニのボーダーT")}を買ったこともあります。
カラフルで遊び心のあるマルニは、七五三掛龍也のふんいきにぴったりのブランドです。
""")

    # ---- summary ----
    b += h2("まとめ")
    b += summary([
        "七五三掛龍也のバッグは、マルニのBOXYNE スモールバッグ",
        "値段は税込493,900円で、高島屋や三越伊勢丹で買える",
        "ロゴ・前ポケット・金具・ファスナーが一致",
        "Rのチャームもマルニで、龍也のRにちなんだもの",
        "中身は香水・日傘2本・フィルムカメラ2台",
    ], c)
    b += para("""
大切な物をぎゅっとつめた、七五三掛龍也らしいおしゃれなバッグでした。
同じバッグを持てば、七五三掛龍也とおそろいの気分になれそうですね。
""")
    b += related("あわせて読みたい", [
        ("【ぽかぽか】七五三掛龍也の香水はどこの？元太とおそろいはル ラボ！", f"{U}/?p={PERFUME_ID}"),
        ("【ぽかぽか】七五三掛龍也の炊飯器はどこの？中村海人からの誕プレ！", f"{U}/?p=2530"),
        ("七五三掛龍也インスタの秋コートはどこの？マルニのブルゾンと判明！", f"{U}/?p=1599"),
        ("七五三掛龍也のフィルムカメラはどれ？コンタックスT2と判明！", f"{U}/?p=1814"),
    ], c)
    return b


if __name__ == "__main__":
    ids = json.loads(IDS_FILE.read_text(encoding="utf-8"))
    if "--html" in sys.argv:
        M = {k: api(f"media/{ids[k]}", method="GET") for k in ("bag", "logo", "charm")}
        HTML_OUT.write_text(build(M), encoding="utf-8")
        print("wrote", HTML_OUT)
    if "--update" in sys.argv:  # 本文だけ差し替え(title/status/アイキャッチは触らない)
        pid = int(sys.argv[sys.argv.index("--update") + 1])
        r = api(f"posts/{pid}", {"content": HTML_OUT.read_text(encoding="utf-8")})
        print("UPDATE", r["id"], r["status"])
    if "--post" in sys.argv:
        eye = Path(sys.argv[sys.argv.index("--post") + 1])
        final_html = HTML_OUT.read_text(encoding="utf-8")
        m = upload_media(eye, eye.name, "七五三掛龍也のバッグ マルニのBOXYNE")
        r = api("posts", {"title": TITLE, "content": final_html, "slug": SLUG, "status": "draft",
                          "categories": CATEGORIES, "author": AUTHOR, "featured_media": m["id"]})
        print("POST", r["id"], r["status"], r["link"])
