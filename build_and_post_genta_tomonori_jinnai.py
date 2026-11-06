# -*- coding: utf-8 -*-
# chomoand-4.blog: 松田元太の「TJ トモノリジンナイ」の意味と始まりの経緯
# 2026-11-06 オシリ依頼。材料: オリコン(2023-10-08 ニノさん予告 / 2024-11-08 VOGUE会見)、
# THE FIRST TIMES(2024-10 金スマ)、スポーツブル(2025-04 THE神業チャレンジ)、entax(2025-11-07 ニノさん2時間SP)、
# 週刊女性PRIME(2024-12)、陣内智則さん本人のX(2023-10-13)、松田元太さん本人のInstagram(プロフィール・投稿3件)。
# ファンブログ・一般ファンのXは要約のみ(引用・リンクなし)。
import json, sys, subprocess

import requests

from build_and_post_travis_japan_tour2027_odds_survey import (
    ROOT, WP_URL, HJSON, SITE, ACC, BORDER, BG, p, h2, h3, wphtml, mark,
    whatbox, minibox, table2, checklist, related, upload_media)

IMG_DIR = ROOT / "images" / "genta_tomonori_jinnai"
EYECATCH = IMG_DIR / "genta_tomonori_jinnai_eyecatch_canva.jpg"
STATE = IMG_DIR / "_state.json"
DRY = "--dry" in sys.argv

TITLE = "松田元太の「TJ トモノリジンナイ」とは？意味と始まりの経緯！"
SLUG = "matsuda-genta-tj-tomonori-jinnai-origin"

JINNAI_X = ("jinnai_tomonori", "1712764821131980813")
IG_KINSUMA1 = "https://www.instagram.com/p/DAt70olTcJr/"
IG_KINSUMA2 = "https://www.instagram.com/p/DBYsadXTmJc/"
IG_KAMIWAZA = "https://www.instagram.com/p/DIdx3CTT9hW/"

SENPAI = ("松田元太の憧れの先輩は誰？山田涼介さんとの関係とエピソード！", "matsuda-genta-senpai-yamada-ryosuke")
SANSEI = ("トラジャの「さんせーい」はいつから？円陣の掛け声の由来と経緯！", "travis-japan-sansei-call-origin")
CARNIVAL = ("吉澤閑也のカーニバルとは？由来は風間俊介との一発ギャグ！", "yoshizawa-shizuya-carnival-origin")
TV = ("トラジャのテレビ出演は？11/8〜11/14の放送予定まとめ！", "travis-japan-tv-schedule-1108-1114")

TIMELINE = [
    ("2023年10月8日", "『ニノさん』に『ゼイチョー』チームで出演。名前を忘れる催眠術の流れで「TJ」と振られ「Tomonori Jinnai」と答える"),
    ("2023年10月13日", "陣内智則さんがXで「巻き込まれTJ事故してます」と反応"),
    ("2023年〜2024年", "ほかのバラエティでも「TJ Travis Japan トモノリジンナイ」とあいさつするのが定番に"),
    ("2024年10月", "『金スマ』で陣内智則さんと共演。2人でTJポーズの写真をInstagramに投稿"),
    ("2024年11月8日", "VOGUE JAPANの会見で、川島如恵留さんが陣内智則さんに感謝"),
    ("2025年4月", "『THE神業チャレンジ』で共演し、またツーショットを投稿"),
    ("2025年11月7日", "『ニノさん』2時間SPで「ちょっと邪魔…」と本音、優勝して「卒業」すると宣言"),
    ("2026年11月", "Instagramのプロフィールには今も「トモノリジンナイ」の文字"),
]


def xembed(user, sid):
    return (f'<!-- wp:html -->\n<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><a href="https://twitter.com/{user}/status/{sid}">'
            f'https://twitter.com/{user}/status/{sid}</a></blockquote>\n'
            '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n<!-- /wp:html -->')


def igembed(url, label):
    return wphtml(f'''<div style="max-width:540px;margin:0 auto 16px;"><blockquote class="instagram-media" data-instgrm-permalink="{url}?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" style="background:#FFF;border:0;border-radius:3px;box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);margin:1px;max-width:540px;min-width:326px;padding:0;width:calc(100% - 2px);"><a href="{url}?utm_source=ig_embed&amp;utm_campaign=loading" target="_blank" rel="noopener">{label}</a></blockquote>
<script async src="https://www.instagram.com/embed.js"></script></div>''')


def timeline_box():
    rows = "\n".join(
        f'<div style="display:flex;margin:0 0 10px 0;"><span style="flex:0 0 8.5em;font-weight:bold;color:{ACC};">{y}</span><span style="flex:1;">{t}</span></div>'
        for y, t in TIMELINE)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">「トモノリジンナイ」の年表</p>
<div style="padding:14px 18px 6px 18px;background:{BG};">
{rows}
</div>
</div>''')


def build():
    b = []
    b.append(p([
        f"松田元太さんがバラエティでよく言う「TJ Travis Japan トモノリジンナイ」は、{mark('Travis Japanの頭文字「TJ」と、お笑い芸人・陣内智則さんの頭文字「TJ(Tomonori Jinnai)」をかけたあいさつ')}です。",
        f"始まりは、{mark('2023年10月8日放送の『ニノさん』(日本テレビ系)')}でした。",
        "「自分の名前を忘れる」催眠術をかけられたあと、「TJ」と何度も振られた松田元太さんが、スタジオにいた陣内智則さんの名前で「Tomonori Jinnai」と答えたのがきっかけです。",
        "この記事では、「トモノリジンナイ」の意味、生まれた日の流れ、陣内智則さん本人の反応、2025年の「卒業」宣言までを年表でまとめます。",
    ]))
    b.append(whatbox([
        "「TJ トラビスジャパン トモノリジンナイ」の意味",
        "いつから？きっかけになった『ニノさん』の回",
        "陣内智則さん本人の反応と、2人のTJポーズ",
        "メンバーの川島如恵留さんが感謝した理由",
        "2025年の「卒業」宣言と、今も言っているのか",
    ]))

    # ---- meaning ----
    b.append(h2("「TJ トラビスジャパン トモノリジンナイ」の意味は？"))
    b.append(minibox([
        ("TJ", "Travis Japan(トラビスジャパン)の頭文字"),
        ("もうひとつのTJ", "Tomonori Jinnai(陣内智則さん)の頭文字"),
        ("言い方", "TJポーズをしながら「TJ、Travis Japan、トモノリジンナイ」"),
        ("言う人", "松田元太さん(主にバラエティ番組のあいさつ)"),
    ]))
    b.append(p([
        "「トモノリジンナイ」は、お笑い芸人の陣内智則(じんない・とものり)さんの名前を、英語のように「名前→名字」の順にした言い方です。",
        "ローマ字にすると「Tomonori Jinnai」で、頭文字はTravis Japanと同じ「TJ」になります。",
        f"つまり{mark('「TJといえばTravis Japan、そしてTomonori Jinnai」')}という、頭文字がたまたま同じことを使ったギャグです。",
        "陣内智則さんとTravis Japanの間に、もともと特別なつながりがあったわけではありません。",
    ]))
    b.append(h3("TJポーズとセットのあいさつ"))
    b.append(p([
        "このフレーズは、手でTravis Japanの頭文字「T」と「J」を作る「TJポーズ」とセットで使われます。",
        "番組の自己紹介で「TJ、Travis Japan……トモノリジンナイ！」と、TJポーズのまま最後に陣内智則さんの名前を言うのがお決まりの流れです。",
        "表記は「トモノリジンナイ」「とものりじんない」「智則陣内」「Tomonori Jinnai」などいろいろありますが、どれも同じネタを指しています。",
    ]))
    b.append(h3("Instagramのプロフィールにも「トモノリジンナイ」"))
    b.append(p([
        f"松田元太さん本人のInstagram(@tj_gentamatsuda_official)のプロフィールには、{mark('「Travis Japan /トモノリジンナイ/マツダマン」')}と書かれています。",
        "所属グループのTravis Japan、ソロの企画で生まれたキャラクターの「マツダマン」と並べて書いているので、本人にとっても大事な肩書きのひとつになっているようです。",
    ]))

    # ---- origin ----
    b.append(h2("いつから？始まりは2023年10月8日の『ニノさん』"))
    b.append(p([
        "「トモノリジンナイ」が生まれたのは、二宮和也さんがMCを務める日本テレビ系のバラエティ番組『ニノさん』です。",
        "放送は2023年10月8日(日)の午前10時25分からの回でした。",
    ]))
    b.append(h3("ドラマ『ゼイチョー』チームとしてゲスト出演"))
    b.append(p([
        "この回の松田元太さんは、2023年10月14日にスタートする土曜ドラマ『ゼイチョー〜「払えない」にはワケがある〜』の宣伝でゲスト出演していました。",
        "ドラマで主演の菊池風磨さん、共演の山田杏奈さんと3人での出演です。",
    ]))
    b.append(table2(["立場", "出演者"], [
        ["MC", "二宮和也"],
        ["ニノさんファミリー", "陣内智則・朝日奈央"],
        ["ゲスト(ゼイチョーチーム)", "菊池風磨・山田杏奈・松田元太"],
    ]))
    b.append(p([
        f"ポイントは、{mark('陣内智則さんが番組のレギュラー「ニノさんファミリー」としてスタジオにいた')}ことです。",
        "オリコンの番組紹介では、松田元太さんが大先輩の二宮和也さんに緊張して「日本語がおかしなことになる」とも書かれていて、この時点でかなりにぎやかな回になっていました。",
    ]))
    b.append(h3("「自分の名前を忘れる」催眠術で「ニクサキ」に"))
    b.append(p([
        "この回では、山田杏奈さんの「催眠術にかかりたい！」というリクエストで、スタジオに催眠療法士が登場しました。",
        "山田杏奈さんと松田元太さんが体験し、松田元太さんは「自分の名前を忘れる」催眠術をかけられます。",
        "番組の予告でも「松田さんがトンデモナイコトに」「スタジオは大パニックと最大級の爆笑」と紹介されていたほどの場面です。",
        f"自分の名前を思い出せなくなった松田元太さんは、存在しない漢字を書いて{mark('「Travis Japanのニクサキです」')}と名乗り、ここで「ニクサキ」というあだ名も生まれました。",
    ]))
    b.append(h3("「TJ」と振られて「Tomonori Jinnai」"))
    b.append(p([
        "名前を思い出せない松田元太さんに、二宮和也さんや菊池風磨さんは「TJ」と何度も振ります。",
        "本来なら「Travis Japan」と返すところですが、松田元太さんはTJポーズをしながら、なぜか「Tomonori Jinnai」と答えました。",
        f"これが{mark('「TJ Travis Japan トモノリジンナイ」の始まり')}です。",
        "どうして陣内智則さんの名前が出てきたのか、本人がはっきり説明したことはありません。",
        "ただ、同じ「TJ」の頭文字を持つ陣内智則さんがちょうど目の前のスタジオにいたので、頭文字から名前がとっさに出てきたと考えるのが自然です。",
    ]))

    # ---- jinnai ----
    b.append(h2("陣内智則さん本人の反応は？"))
    b.append(h3("放送5日後に「巻き込まれTJ事故」"))
    b.append(p([
        "陣内智則さんは放送の5日後、2023年10月13日に自分のXでこのネタに触れています。",
        "「ニノさん」を見ていないと誰も分からないノリのせいで、「巻き込まれTJ事故してます」という内容でした。",
        "あわせて『ゼイチョー』の出演者に「頑張ってください」とエールも送っています。",
    ]))
    b.append(xembed(*JINNAI_X))
    b.append(p([
        "「Travis Japan松田くん(ニクサキ)」と書いているところからも、陣内智則さんがあの回の流れをちゃんと面白がっていたことが伝わります。",
        "困ったふりをしながらもネタに乗っていて、ここから松田元太さんが堂々と名乗りやすくなったとも言えそうです。",
    ]))
    b.append(h3("2024年10月『金スマ』で2人のTJポーズ"))
    b.append(p([
        "2024年10月4日放送のTBS系『中居正広の金スマスペシャル』で、松田元太さんは陣内智則さんと共演しました。",
        "放送に合わせて、松田元太さんはInstagramに陣内智則さんとTJポーズをしたツーショットを投稿しています。",
        f"ハッシュタグは{mark('「#トモノリジンナイさんに会えた」「#めっちゃ嬉しかった」「#いつも優しい」')}で、ファンからは「本家のTJ！」という声も上がりました。",
    ]))
    b.append(igembed(IG_KINSUMA1, "松田元太さんのInstagram投稿(2024年10月)"))
    b.append(p([
        "10月18日放送の『金スマ』でも再び共演し、今度は「#トモノリジンナイ」のハッシュタグで、2人が寄り添ってTJポーズをする写真を投稿しました。",
    ]))
    b.append(igembed(IG_KINSUMA2, "松田元太さんのInstagram投稿(2024年10月)"))
    b.append(h3("2025年4月『THE神業チャレンジ』でもツーショット"))
    b.append(p([
        "2025年4月15日放送のTBS系『THE神業チャレンジ』でも2人は共演しています。",
        "翌16日には「#おちかれ」「#トモノリジンナイ」「#陣内智則さん」のハッシュタグで、またツーショットを公開しました。",
        "共演するたびに写真を撮っているので、2人の関係はすっかり「公認のTJ同士」になっています。",
    ]))
    b.append(igembed(IG_KAMIWAZA, "松田元太さんのInstagram投稿(2025年4月)"))

    # ---- members ----
    b.append(h2("トラジャ全体に広がった「TJ」の効果"))
    b.append(p([
        "松田元太さんが「トモノリジンナイ」と言い続けたことは、Travis Japan全体にもいい影響があったようです。",
    ]))
    b.append(h3("川島如恵留さん「あやかる場面もたくさんあった」"))
    b.append(p([
        "2024年11月8日、Travis Japanは『VOGUE JAPAN』の「THE ONES TO WATCH 2024」の授賞記者会見に登壇しました。",
        "この会見で川島如恵留さんは、「とにかく松田元太が各所で『TJ Travis Japan トモノリジンナイ』と言い続けた結果、我々のトモノリジンナイさんにあやかる場面もたくさんあった」と話しています。",
        f"さらに「{mark('陣内智則さんがTravis Japanのおかげで仕事が増えたってなるくらい')}Travis Japanには頑張っていただきたい」と、川島如恵留さんらしい言い回しで感謝を伝えました。",
        "同じ会見で松田元太さんが「おバカなTravis Japanはもう封印します！」と宣言し、川島如恵留さんに「グループの活動が休止します」と止められる場面もあり、会場は笑いに包まれています。",
    ]))
    b.append(h3("スタッフや共演者もTJポーズをしてくれるように"))
    b.append(p([
        "週刊女性PRIMEの記事(2024年12月)によると、松田元太さんはグループやメンバーの人柄をもっと多くの人に知ってもらい、自分が活躍して恩返しをしたいという思いで、事あるごとにTJポーズを続けてきたそうです。",
        "その結果、番組のスタッフや共演者が、ほかのメンバーに会ったときにもTJポーズをしてくれるようになったといいます。",
        "1人のメンバーのギャグが、グループの名前を覚えてもらうきっかけになった、トラジャらしいエピソードです。",
    ]))

    # ---- graduation ----
    b.append(h2("2025年11月に「卒業」宣言？今も言ってる？"))
    b.append(h3("『ニノさん』2時間SPで「ちょっと邪魔…」"))
    b.append(p([
        "生まれた場所の『ニノさん』で、このネタにひと区切りがつく場面もありました。",
        "2025年11月7日放送の『ニノさん 2時間SP』で、陣内智則さんに「最近“Tomonori Jinnai”言ってる？」と聞かれた松田元太さんは、神妙な顔で「ちょっと邪魔…」と答えます。",
        "陣内智則さんは「ちょっと邪魔かい。あれだけ言っといて」とツッコミ、「枷(かせ)になってきた？」と聞かれた松田元太さんは小声で「はい」と認めました。",
    ]))
    b.append(p([
        f"そして松田元太さんは「恩がある番組なので、{mark('優勝して卒業します')}」と宣言します。",
        "二宮和也さんは「卒業スペシャルだ」と盛り上げ、陣内智則さんは「卒業するんかい」とツッコんで、スタジオは大笑いになりました。",
        "生みの親の番組で、本家の陣内智則さんの前で「卒業」を宣言するところまで含めて、きれいにオチがついた形です。",
    ]))
    b.append(h3("今もプロフィールには「トモノリジンナイ」"))
    b.append(p([
        "ただ、「卒業」宣言のあとも、松田元太さんのInstagramのプロフィールには2026年11月時点で「トモノリジンナイ」の文字が残っています。",
        "2026年7月20日に松田元太さんがMCを務めたテレビ東京の特番『失敗のススメ。』の放送日にも、ファンの間では「トモノリジンナイには本当にお世話になった」と振り返る声がありました。",
        "毎回のあいさつで言う時期は過ぎたとしても、松田元太さんがブレイクするきっかけのひとつとして、ファンにとっては今も大事なネタになっています。",
        "番組で陣内智則さんと共演したときに、また2人のTJポーズが見られるかもしれません。",
    ]))

    # ---- timeline ----
    b.append(h2("「トモノリジンナイ」の年表"))
    b.append(p(["ここまでの流れを年表にまとめます。"]))
    b.append(timeline_box())
    b.append(p([
        "松田元太さんのバラエティでのエピソードは、ほかのメンバーのギャグと同じく「その場のノリ」から生まれたものが多いです。",
        f'吉澤閑也さんの「カーニバル」の由来は<a href="{SITE}{CARNIVAL[1]}">{CARNIVAL[0]}</a>、トラジャの円陣の掛け声は<a href="{SITE}{SANSEI[1]}">{SANSEI[0]}</a>でまとめています。',
    ]))

    # ---- matome ----
    b.append(h2("まとめ"))
    b.append(checklist("この記事のポイント", [
        "「トモノリジンナイ」は、Travis Japanと陣内智則(Tomonori Jinnai)の頭文字「TJ」をかけたギャグ",
        "始まりは2023年10月8日放送の『ニノさん』、ゼイチョーチームでのゲスト出演回",
        "名前を忘れる催眠術のあと「TJ」と振られ、スタジオにいた陣内智則の名前で答えた",
        "陣内智則はXで「巻き込まれTJ事故」と反応、2024年の『金スマ』で2人のTJポーズが実現",
        "川島如恵留は「トモノリジンナイさんにあやかる場面もたくさんあった」と感謝",
        "2025年11月の『ニノさん』で「卒業」宣言、ただしInstagramのプロフィールには今も残っている",
    ]))
    b.append(p([
        "催眠術でたまたま出てきた一言が、2年以上たっても語られる松田元太さんの代名詞になりました。",
        "陣内智則さんとの次の共演で、「卒業」したはずのTJポーズがまた見られるのか楽しみですね！",
        f'トラジャのテレビ出演予定は<a href="{SITE}{TV[1]}">{TV[0]}</a>でチェックしてみてください。',
    ]))
    b.append(related([SENPAI, SANSEI, CARNIVAL, TV]))
    return "\n\n".join(b)


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    html = build()
    tmp = IMG_DIR / "_post.html"
    tmp.write_text(html, encoding="utf-8")
    names = "陣内智則,二宮和也,菊池風磨,山田杏奈,朝日奈央"
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis", "--names", names, str(tmp)], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "check", "--group", "travis", "--names", names, str(tmp)], check=True)
    html = tmp.read_text(encoding="utf-8")
    if DRY:
        print("dry chars:", len(html))
        return
    if not EYECATCH.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
                        "--main", "松田元太", "--bottom", "「TJ トモノリジンナイ」とは？",
                        "--bottom", "意味と始まりの経緯！", "--color-key", "松田元太", "--out", str(EYECATCH)], check=True)
    if "eyecatch" not in state:
        state["eyecatch"] = upload_media(EYECATCH, TITLE, TITLE)
        STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    body = {"title": TITLE, "slug": SLUG, "content": html, "status": "draft",
            "categories": [3, 7], "author": 2, "featured_media": state["eyecatch"]["id"]}
    if "post_id" in state:
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{state['post_id']}", headers=HJSON, json=body)
    else:
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, json=body)
    r.raise_for_status()
    post = r.json()
    state["post_id"] = post["id"]
    STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    print("post", post["id"], post["status"], post["link"], "chars", len(html))


if __name__ == "__main__":
    main()
