# -*- coding: utf-8 -*-
"""七五三掛龍也が『ぽかぽか』(2026/11/11)で見せた香水(元太とおそろい=ル ラボ ベルガモット22)の記事。chomoand-4.blog ID2547下書き、【未】付き。バッグはID2550に分割(11/11オシリ指示).

TVer(ep4yl0u6hk)を720pで取得し、11:28〜14:30あたりのコーナーをフレーム+文字起こしで確認した。
- バッグ: MARNI BOXYNE スモールバッグ(BMMP0186U0P929400M72、税込493,900円。オシリが高島屋で特定、11/11)
- チャーム: MARNI アニマル アルファベット チャーム「R」(ブラウンスエード×ラインストーン、PCMO0065Q0P894600M39、海外公式€395)
- 香水: LE LABO ベルガモット22(松田元太とおそろい、ラベルの「22」と瓶の形から) / PRADA パラドックス ヴァーチャル フラワー / 銀色のアトマイザー
- 日傘2本(白×黒の折りたたみ、ブランド不明) / フィルムカメラ2台(CONTAX T2・写ルンです)
- ベストバイの炊飯器はユカが別記事(ID2530、公開済み)

python build_and_post_shimekake_pokapoka_bag_items.py --html            本文HTMLを書き出す(画像は仮URL)
python build_and_post_shimekake_pokapoka_bag_items.py --upload          フレーム画像をアップしてIDを保存
python build_and_post_shimekake_pokapoka_bag_items.py --post <eye.jpg>  下書き投稿(二重投稿注意)
"""
import json, sys, urllib.parse
from pathlib import Path

from build_and_post_hadakanboutachi_5 import (api, upload_media, para, h2, h3, html, mark, infobox, learnbox,
                                              minibox, table, summary, related, img)

ROOT = Path(__file__).resolve().parent
HTML_OUT = ROOT / "tmp_shimekake_pokapoka_bag_items.html"
IDS_FILE = ROOT / "_shimekake_pokapoka_bag_media.json"
FR = ROOT / "_scratch" / "pokapoka1111" / "fr"
TVER = "https://tver.jp/episodes/ep4yl0u6hk"
U = "https://chomoand-4.blog"
PINK = dict(accent="#e7a1c8", border="#f3c6d9", bg="#fdf1f6", marker="mark_yellow")
c = PINK

TITLE = "【未】【ぽかぽか】七五三掛龍也の香水はどこの？元太とおそろいはル ラボ！"
BAG_ID = 2550  # バッグ記事(2026-11-11に分割)
SLUG = "shimekake-ryuya-perfume-lelabo-bergamote22"
CATEGORIES = [3, 8, 7]  # Travis Japan / 七五三掛龍也 / 松田元太
AUTHOR = 2  # momo(オシリと作った記事)

LELABO_URL = "https://www.lelabofragrances.jp/products/bergamote-22_135"
COSME_PRADA = "https://www.cosme.net/variations/1182621/"
MARNI_R = "https://www.marni.com/en-nl/key-rings-PCMO0065Q0P894600M39.html"
AMZ_TAG = "chomoand03-22"
SPON = 'target="_blank" rel="nofollow sponsored noopener"'


def amazon(q):
    return f"https://www.amazon.co.jp/s?k={urllib.parse.quote_plus(q)}&tag={AMZ_TAG}"


def a(url, t):
    return f'<a href="{url}" target="_blank" rel="noopener">{t}</a>'


def inner(pid, t):
    return f'<a href="{U}/?p={pid}">{t}</a>'


def amzbox(name, note, q):
    btn = ("display:inline-block;margin:4px;padding:10px 18px;border-radius:4px;color:#fff;font-weight:bold;"
           "text-decoration:none;background:#232f3e;")
    return html(f'''<div style="border:1px solid {c["border"]};border-radius:4px;padding:16px;margin:0 0 16px 0;background:#fff;text-align:center;">
<p style="margin:0 0 4px 0;font-weight:bold;">{name}</p>
<p style="margin:0 0 8px 0;font-size:0.85em;color:#888;">{note}</p>
<a href="{amazon(q)}" {SPON} style="{btn}">Amazonで見る</a>
</div>''')


# key: (frame file, upload name, alt)
IMAGES = {
    "bag": ("f_008.jpg", "shimekake_pokapoka_marni_bag.jpg", "ぽかぽかで七五三掛龍也が持ってきたMARNIのレザーボストンバッグ"),
    "logo": ("f_011.jpg", "shimekake_pokapoka_marni_logo.jpg", "七五三掛龍也のバッグに入ったMARNIのロゴ"),
    "charm": ("f_018.jpg", "shimekake_pokapoka_marni_r_charm.jpg", "七五三掛龍也のバッグについたMARNIのRのチャーム"),
    "lelabo": ("f_036.jpg", "shimekake_pokapoka_lelabo_prada.jpg", "七五三掛龍也の香水 ル ラボとプラダ"),
    "prada": ("f_044.jpg", "shimekake_pokapoka_prada_paradoxe.jpg", "七五三掛龍也の香水 プラダ パラドックス"),
    "atomizer": ("f_039.jpg", "shimekake_pokapoka_atomizer.jpg", "七五三掛龍也の銀色のアトマイザー"),
    "wrist": ("genta_wrist.jpg", "shimekake_pokapoka_perfume_wrist.jpg", "松田元太とおそろいの香水を手首につける七五三掛龍也"),
    "umbrella": ("f_118.jpg", "shimekake_pokapoka_higasa.jpg", "七五三掛龍也の折りたたみ日傘"),
    "camera_utsurun": ("f_163.jpg", "shimekake_pokapoka_utsurundesu.jpg", "七五三掛龍也の写ルンです"),
    "camera_contax": ("f_166.jpg", "shimekake_pokapoka_contax_t2.jpg", "七五三掛龍也のCONTAX T2"),
}


def build(M):
    def pic(k):
        return img(M[k], IMAGES[k][2], TVER)

    b = ""
    b += html('<p style="font-size:12px;color:#888;">本記事はプロモーションを含みます</p>')
    b += para(f"""
Travis Japanの七五三掛龍也が、2026年11月11日の『ぽかぽか』(フジテレビ系)に出演しました。
「カバンの中身」のコーナーで、いつも持ち歩いている香水を見せてくれました。
香水は3本あり、日によって香りを変えているそうです。
""")
    b += para(f"""
とくに話題になったのが、{mark("松田元太とおそろいの香水", c)}です。
ラベルの数字と瓶の形から、ル ラボの「ベルガモット 22」とみられます。
この記事では、香水3本のブランドと値段を、放送の画面とあわせてまとめます。
""")
    b += learnbox([
        "松田元太とおそろいの香水はどれか",
        "ル ラボ ベルガモット 22とわかる理由と値段",
        "ほかの香水2本のブランド",
        "香水のつけ方",
        "カバンに入っていたほかの物",
    ], c)

    b += h2("七五三掛龍也の香水とカバンの中身一覧")
    b += table(["アイテム", "ブランド・名前"], [
        ["香水1", "LE LABO ベルガモット 22(元太とおそろい)"],
        ["香水2", "PRADA パラドックス ヴァーチャル フラワー"],
        ["香水3", "銀色のアトマイザー(中身は不明)"],
        ["日傘", "白と黒の折りたたみ日傘を2本"],
        ["カメラ", "CONTAX T2と写ルンです"],
        ["バッグ", f'{inner(BAG_ID, "MARNI BOXYNE スモールバッグ")}'],
    ], c)
    b += para("""
七五三掛龍也は、ドラマ『小麦とバターと復讐と』で共演中の伊原六花と一緒に出演しました。
番組のテーマは、ズボラな伊原六花と心配性な七五三掛龍也の「性格が真逆なコンビ」です。
カバンの中身にも、心配性らしさがしっかり出ていました。
""")

    # ---- perfume ----
    b += h2("松田元太とおそろいの香水はル ラボのベルガモット 22")
    b += minibox([("ブランド", "LE LABO(ル ラボ)"), ("商品名", "ベルガモット 22 オードパルファム"),
                  ("値段", "15ml 14,300円・50ml 32,230円・100ml 47,190円"), ("おそろい", "松田元太と同じ香り")], c)
    b += amzbox("ル ラボ ベルガモット 22 オードパルファム", "15ml・50ml・100mlの3サイズがあります", "ル ラボ ベルガモット22")
    b += pic("lelabo")
    b += para("""
カバンからまず出てきたのは、香水でした。
七五三掛龍也は「全部香りがちがって、日によって、そのときの気分によって変えている」と話していました。
手には、香水が3本にぎられていました。
""")
    b += h3("「これは元ちゃんと一緒なんですよ」")
    b += pic("wrist")
    b += para(f"""
香水のつけ方を聞かれた七五三掛龍也は、小さな四角い瓶を手に取りました。
そして{mark("「これは元ちゃん(松田元太)と一緒なんですよ」", c)}と明かしました。
2人で同じ香りを使っているそうです。
""")
    b += para("""
つけ方は、手首のあたりにシュッとふきかけるやり方でした。
スタジオには松田元太はいませんでしたが、メンバー同士の仲の良さが伝わる場面でした。
Xでも「しめげんおそろい」とよろこぶ声がたくさん上がっていました。
""")
    b += h3("ル ラボのベルガモット 22とわかる理由")
    b += para("""
手首につけた瓶は、四角いガラスに銀色のキャップ、白い紙のラベルという形でした。
これはル ラボの香水の瓶とまったく同じ形です。
アップの画面では、ラベルの左上に「22」という数字が読めます。
""")
    b += para(f"""
ル ラボの香水は、名前の後ろに数字がつくのがお決まりです。
定番の香りで「22」がつくのは、{mark("ベルガモット 22", c)}だけです。
瓶の大きさから、持ち歩き用の15mlサイズとみられます。
""")
    b += h3("ベルガモット 22はどんな香り？")
    b += para(f"""
ベルガモット 22は、2006年にル ラボができたときからある定番の香りです。
{a(LELABO_URL, "公式サイト")}では、ベルガモットのさわやかさに、グレープフルーツのほろ苦さが合わさった香りと説明されています。
最後はアンバーとムスクのあまさに、ベチバーの男らしさが少しだけ残ります。
""")
    b += para("""
柑橘系なのでさわやかで、男女どちらにも使いやすい香りです。
2026年11月11日に公式サイトを見ると、15mlは14,300円でした。
50mlは32,230円、100mlは47,190円です。
""")
    b += para(f"""
松田元太といえば、松倉海斗とおそろいのメゾン マルジェラの香水も有名です。
くわしくは{inner(1278, "トラジャの愛用香水まとめ")}で紹介しています。
香りを使い分ける松田元太が、七五三掛龍也とも同じ香水を使っているのはうれしい発見でした。
""")

    b += h3("プラダのパラドックス ヴァーチャル フラワー")
    b += minibox([("ブランド", "PRADA BEAUTY(プラダ ビューティ)"), ("商品名", "プラダ パラドックス ヴァーチャル フラワー オーデパルファム"),
                  ("値段", "10mL 7,480円・30mL 13,970円")], c)
    b += pic("prada")
    b += para("""
いちばん大きい瓶は、プラダの香水でした。
ななめにカットされたような透明な瓶に、黒いキャップがついています。
瓶には「PRADA」の文字と、その上に「VIRTUAL FLOWER」の文字が見えました。
""")
    b += para(f"""
これはプラダの「パラドックス」シリーズの「ヴァーチャル フラワー」です。
{a(COSME_PRADA, "アットコスメ")}によると、日本では2024年8月に発売されました。
値段は30mLで13,970円、10mLで7,480円です。
""")
    b += amzbox("プラダ パラドックス ヴァーチャル フラワー オーデパルファム", "10mL・30mLなどのサイズがあります", "プラダ パラドックス ヴァーチャル フラワー")
    b += h3("銀色のアトマイザー")
    b += pic("atomizer")
    b += para("""
3本目は、銀色のリングを重ねたような筒形のボトルでした。
香水を小分けして持ち歩く「アトマイザー」とみられます。
中に入っている香水のブランドは、放送からはわかりませんでした。
""")

    # ---- umbrella ----
    b += h2("日傘を2本持ち歩くのは心配性だから")
    b += minibox([("中身", "折りたたみの日傘2本"), ("色", "外が白・内側が黒、もう1本は黒"),
                  ("理由", "1本がこわれたときのため")], c)
    b += pic("umbrella")
    b += para("""
2つ目のアイテムは、日傘でした。
七五三掛龍也は「遮光100%くらいのもの。紫外線がやっぱり敵なので」と話しています。
美容に気をつかう七五三掛龍也らしいアイテムです。
""")
    b += para(f"""
おどろいたのは、日傘が{mark("2本", c)}入っていたことです。
理由は「この傘がもしこわれたときのために、もう1本」でした。
風が強くて傘が折れてしまうことがあるから、という心配性ならではの理由です。
""")
    b += para("""
スタジオからは「こわれても、短いまま持てばその日は乗り切れる」とツッコミが入りました。
それでも七五三掛龍也は「行けないんですよ」と、2本持ちをゆずりませんでした。
日傘のブランドは、放送からはわかりませんでした。
""")

    # ---- camera ----
    b += h2("フィルムカメラはCONTAX T2と写ルンです")
    b += minibox([("1台目", "CONTAX T2(コンタックス)"), ("2台目", "写ルンです(富士フイルム)"),
                  ("使い方", "マネージャーさんに撮ってもらう")], c)
    b += pic("camera_contax")
    b += para(f"""
3つ目は、フィルムカメラが2台でした。
銀色のカメラには「CONTAX」の文字があり、{inner(1814, "インスタにも写っていたCONTAX T2")}です。
1990年に出た高級なコンパクトカメラで、今も人気があります。
""")
    b += pic("camera_utsurun")
    b += para("""
もう1台は、緑の箱が目印の「写ルンです」でした。
フィルムが入った使い切りのカメラで、レトロな写りが楽しめます。
""")
    b += h3("撮るのはマネージャーさん")
    b += para("""
このカメラは、インスタにのせる写真用です。
ただし、七五三掛龍也は「僕は1回も使わない」と話していました。
写真を撮るのはマネージャーさんで、被写体はいつも七五三掛龍也なのだそうです。
""")
    b += para(f"""
撮るときは、まずマネージャーさんを立たせて「この画角で」と見本を見せます。
そのあと入れかわって、同じ画角で撮ってもらうというこだわりぶりでした。
マネージャーさんも{mark("髪型が同じでイケメン", c)}だと話題になり、スタジオは笑いに包まれました。
""")

    # ---- bag (別記事2550へ) ----
    b += h2("カバンはマルニのBOXYNE")
    b += pic("bag")
    b += para(f"""
香水が入っていたカバンは、マルニの「BOXYNE スモールバッグ」でした。
値段は税込493,900円で、大きな「R」のチャームもマルニです。
くわしくは{inner(BAG_ID, "七五三掛龍也のバッグはどこの？マルニのBOXYNE！")}でまとめています。
""")

    # ---- best buy ----
    b += h2("ベストバイは中村海人からもらった炊飯器")
    b += para(f"""
カバンの中身のあとは、七五三掛龍也の「ベストバイ」のコーナーでした。
紹介したのは、メンバーの中村海人から誕生日にもらった象印の炊飯器「炎舞炊き」です。
くわしくは{inner(2530, "【ぽかぽか】七五三掛龍也の炊飯器はどこの？")}でまとめています。
""")

    # ---- summary ----
    b += h2("まとめ")
    b += summary([
        "松田元太とおそろいの香水は、ル ラボのベルガモット 22とみられる",
        "ラベルの「22」と瓶の形が決め手",
        "ほかにプラダのパラドックス ヴァーチャル フラワーとアトマイザーも",
        "日傘はこわれたときのために2本持ち",
        "フィルムカメラはCONTAX T2と写ルンです",
        "カバンはマルニのBOXYNE スモールバッグ",
    ], c)
    b += para("""
香水やカバンの中身から、おしゃれで美容好き、そして心配性な七五三掛龍也の素顔が見えた放送でした。
松田元太とおそろいの香りをまとって、今日もお仕事をがんばっているのかもしれませんね。
""")
    b += related("あわせて読みたい", [
        ("【ぽかぽか】七五三掛龍也のバッグはどこの？マルニのBOXYNE！", f"{U}/?p={BAG_ID}"),
        ("【ぽかぽか】七五三掛龍也の炊飯器はどこの？中村海人からの誕プレ！", f"{U}/?p=2530"),
        ("七五三掛龍也のフィルムカメラはどれ？コンタックスT2と判明！", f"{U}/?p=1814"),
        ("トラジャの愛用香水まとめ！中村海人はトムフォード、松松はマルジェラ？", f"{U}/?p=1278"),
    ], c)
    return b


def dummy_media(k):
    u = f"https://example.invalid/{IMAGES[k][1]}"
    s = {"source_url": u, "width": 1280, "height": 720}
    return {"source_url": u, "media_details": {"width": 1280, "height": 720, "sizes": {"large": s, "full": s}}}


if __name__ == "__main__":
    if "--upload" in sys.argv:
        ids = json.loads(IDS_FILE.read_text(encoding="utf-8")) if IDS_FILE.exists() else {}
        for k, (f, name, alt) in IMAGES.items():
            if k in ids:
                continue
            m = upload_media(FR / f, name, alt)
            ids[k] = m["id"]
            print("uploaded", k, m["id"])
            IDS_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
        sys.exit()

    if "--html" in sys.argv:
        if IDS_FILE.exists():
            ids = json.loads(IDS_FILE.read_text(encoding="utf-8"))
            M = {k: api(f"media/{v}", method="GET") for k, v in ids.items()}
        else:
            M = {k: dummy_media(k) for k in IMAGES}
        HTML_OUT.write_text(build(M), encoding="utf-8")
        print("wrote", HTML_OUT)
        sys.exit()

    if "--update" in sys.argv:  # 2547を香水記事に書き直し(2026-11-11)。titleは【未】付きの下書きのまま
        pid = int(sys.argv[sys.argv.index("--update") + 1])
        r = api(f"posts/{pid}", {"title": TITLE, "slug": SLUG, "content": HTML_OUT.read_text(encoding="utf-8"),
                                 "status": "draft"})
        print("UPDATE", r["id"], r["status"])
        if len(sys.argv) > sys.argv.index("--update") + 2:
            eye = Path(sys.argv[sys.argv.index("--update") + 2])
            m = upload_media(eye, eye.name, "七五三掛龍也の香水 元太とおそろい")
            api(f"posts/{pid}", {"featured_media": m["id"]})
            print("EYECATCH", m["id"])

    if "--post" in sys.argv:
        eye = Path(sys.argv[sys.argv.index("--post") + 1])
        final_html = HTML_OUT.read_text(encoding="utf-8")  # honorific/easy_read で直した版
        assert "example.invalid" not in final_html, "run --upload then --html first"
        m = upload_media(eye, eye.name, "七五三掛龍也のカバンの中身")
        r = api("posts", {"title": TITLE, "content": final_html, "slug": SLUG, "status": "draft",
                          "categories": CATEGORIES, "author": AUTHOR, "featured_media": m["id"]})
        print("POST", r["id"], r["status"], r["link"])
