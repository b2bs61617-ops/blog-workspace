# -*- coding: utf-8 -*-
"""「ちいかわクリニック」の疑問まとめ記事(chomoand.com トレンド速報)を組み立てて下書き投稿する(2026-11-12 ユカ依頼)。
usage: python3 tools/_build_upload_chiikawa_clinic_1112.py [--build-only] [--update-content]
  --build-only    : articles/chiikawa_clinic.html を書き出すだけ(このあと easy_read fix/check をかける)
  (なし)          : articles/chiikawa_clinic.html(easy_read修正済み)を下書き投稿する
  --update-content: 投稿済み下書きのタイトル・本文を差し替える
状態は articles/chiikawa_clinic_posted.json に控え、再実行で重複投稿しない。
出典: 公式プレスリリース(PR TIMES 2本)・ちいかわマーケット商品ページ・入店チケット案内画像(Xに出回っている公式案内のスクショ)、
X/Threadsの声は tools/Xiy/_chiikawa_clinic_1112/ に収集。
アイキャッチ: トレンド速報はCanva DAGnrXY2_5I必須だが、このセッションはCanva MCP未認証のため付けていない(予備ツールは使わない)。
"""
import sys, os, json, base64, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "articles", "chiikawa_clinic.html")
POSTED = os.path.join(REPO, "articles", "chiikawa_clinic_posted.json")
BASE_TITLE = "ちいかわクリニックの抽選はいつ？予約販売の注意点と会場一覧"
assert len(BASE_TITLE) <= 35, len(BASE_TITLE)
TITLE = "【未】" + BASE_TITLE
SLUG = "chiikawa-clinic-chusen-yoyaku"
CATEGORIES = [37]
AUTHOR = 4  # anco(chomoand.comのuser id 4)。ユカのMacからのトレンド速報はVIVANT記事と同じ名義

A, B, BG = "#e8829a", "#f6d3db", "#fdf3f5"
TH = f"border:1px solid #ccc;padding:8px 12px;background:{A};color:#fff;"
TD = "border:1px solid #ccc;padding:8px 12px;"
TDZ = TD + f"background:{BG};"


def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n'


def html(s):
    return "<!-- wp:html -->\n" + s.strip() + "\n<!-- /wp:html -->\n\n"


def table(head, rows):
    h = "".join(f'<th style="{TH}">{c}</th>' for c in head) if head else ""
    body = ""
    for i, r in enumerate(rows):
        st = TDZ if i % 2 else TD
        body += "<tr>" + "".join(f'<td style="{st}">{c}</td>' for c in r) + "</tr>\n"
    thead = f"<thead><tr>{h}</tr></thead>\n" if head else ""
    return ("<!-- wp:table -->\n<figure class=\"wp-block-table\"><table class=\"has-fixed-layout\">"
            f"{thead}<tbody>\n{body}</tbody></table></figure>\n<!-- /wp:table -->\n\n")


def mini(*kv):
    inner = "".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>' for i, (k, v) in enumerate(kv))
    return html(f'<div style="border:1px solid {B};border-left:4px solid {A};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">{inner}</div>')


def mark(t):
    return f'<strong><span class="swl-marker mark_pink" style="font-size:1.15em;">{t}</span></strong>'


def gmap(q):
    return html(f'<iframe src="https://maps.google.com/maps?q={q}&t=&z=16&ie=UTF8&iwloc=&output=embed" '
                'width="100%" height="350" style="border:0;" loading="lazy"></iframe>')


CHK = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {A};border-radius:3px;'
       f'color:{A};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')
QUOTE = f'border-left:4px solid {A};padding:10px 16px;margin:0 0 16px 0;background:{BG};'


def voice(t):
    return html(f'<p style="{QUOTE}">{t}</p>')


out = ""
out += p("11月12日のお昼、SNSで「ちいかわクリニック」がトレンド入りしました。",
         "ちいかわたちがナース服や白衣を着た、" + mark("新しいグッズシリーズ") + "の発表です。")
out += p("結論から言うと、発売は" + mark("11月27日(金)") + "からです。",
         "8つの会場は入店が抽選制で、" + mark("応募は11月13日(金)10時から15日(日)23時59分まで") + "です。")
out += p("SNSでは「どうやったら買えるの？」「予約って受注生産？」といった声がたくさん出ています。",
         "この記事では、みんなが気になっている疑問をひとつずつまとめました。")

out += html(f'''
<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>ちいかわクリニックとは何か、なぜトレンド入りしたのか</li>
<li>いつから・どこで買えるのか(全国19か所の会場)</li>
<li>入店抽選の日程と申し込み方法、当日の持ち物</li>
<li>「予約」は受注生産なのか、通販の注意点</li>
<li>話題の臓器マスコットと、グッズの値段</li>
</ul>
</div>''')

# ---- とは ----
out += h2("ちいかわクリニックとは？なぜトレンド入りした？")
out += mini(("発表日", "2026年11月12日(木)"),
            ("第1弾の発売", "11月27日(金)"),
            ("第2弾の発売", "12月11日(金)"),
            ("売る場所", "ちいかわマーケット・ちいかわらんど・期間限定会場など全国19か所"))
out += p("ちいかわクリニックは、『ちいかわ』の" + mark("毎年恒例のグッズシリーズ") + "の2026年版です。",
         "2024年は「ちいかわ寿司」、2025年は「Chiikawa Baby(ちいかわベビー)」でした。",
         "今年のテーマは「病院」です。")
out += p("ちいかわ・ハチワレ・うさぎなど12のキャラクターが、ピンクのカーディガンを着たナース姿になっています。",
         "さらに、うさぎとラッコは白衣を着たドクター姿で登場しました。")
out += p("11月12日のお昼ごろ、公式アカウントがいっせいに発表しました。",
         "グッズの数がとても多く、入店抽選や予約のルールも細かいため、一気に話題が広がったようです。")
out += p("「いつもの新作は10月だったから、今年はないと思っていた」という声もありました。",
         "映画の公開もあった年なので、うれしいサプライズになったようです。")

# ---- いつ・どこ ----
out += h2("ちいかわクリニックはいつから？どこで買える？")
out += p("第1弾は" + mark("11月27日(金)") + "に、全国いっせいに発売されます。",
         "買える場所は、大きく分けて3つあります。")
out += table(("買える場所", "くわしく"), [
    ("ちいかわマーケット(公式通販)", "11月27日(金)11時から"),
    ("ちいかわらんど(全11店)", "11月27日(金)から"),
    ("期間限定会場(全8か所)", "会場ごとに期間がちがう"),
])
out += h3("期間限定会場8か所と期間")
out += table(("会場", "期間"), [
    ("東京駅一番街 いちばんプラザ(東京)", "11/27〜12/24"),
    ("ギンザミライミュージアム(東京)", "11/27〜12/27"),
    ("名古屋パルコ東館 地下1階(愛知)", "11/27〜12/20"),
    ("キデイランド大阪梅田店 POP UP 1(大阪)", "11/27〜12/9"),
    ("キデイランド広島パルコ店 POP UP(広島)", "11/27〜2027/1/6"),
    ("札幌アピア キデイランド POP UP SHOP(北海道)", "11/27〜2027/1/5"),
    ("仙台パルコ1 5階(宮城)", "11/27〜12/20"),
    ("アミュプラザくまもと 2階(熊本)", "11/27〜2027/1/11"),
])
out += p("いちばん早く終わるのは、" + mark("大阪梅田の12月9日まで") + "です。",
         "反対に、熊本は年明けの2027年1月11日(月・祝)まで開いています。",
         "営業時間は会場ごとにちがうので、行く前に各施設のサイトで見ておきましょう。")
out += p("いちばん大きな会場のひとつが、東京駅の地下にある「いちばんプラザ」です。",
         "営業時間は10時から20時30分までで、最終日だけ18時に閉まります。")
out += gmap("東京駅一番街 東京キャラクターストリート")
out += h3("ちいかわらんど11店")
out += p("ちいかわらんどでは、次の11店でちいかわクリニックのグッズが並びます。")
out += table(("地域", "お店"), [
    ("東京", "原宿店・新宿店・池袋パルコ店・東京スカイツリータウン・ソラマチ店"),
    ("関東", "横浜店・越谷レイクタウン店"),
    ("関西", "京都四条河原町店・心斎橋パルコ店"),
    ("そのほか", "金沢フォーラス店・福岡パルコ店・札幌パルコ店"),
])
out += p("ちいかわらんどの入店チケットについては、" + mark("後日、公式Xで知らせる") + "とされています。",
         "SNSでは「らんどの初日の予約はむずかしそう」という声も出ていました。")

# ---- 抽選 ----
out += h2("ちいかわクリニックの入店抽選はいつ？申し込み方法は？")
out += p("期間限定会場の8か所は、混雑をさけるため" + mark("LINEでの入店予約制") + "になります。",
         "初日から4日間は抽選、12月からは先着順です。")
out += h3("抽選(11月27日〜30日の入店分)")
out += mini(("応募期間", "11月13日(金)10:00〜11月15日(日)23:59"),
            ("当選発表", "11月16日(月)中(申し込みページの「マイチケット」で確認)"),
            ("対象の入店日", "11月27日(金)〜11月30日(月)"),
            ("申し込み", "LINEアプリ(顔写真と名前の登録が必要)"))
out += p("申し込みには、" + mark("顔写真と名前の登録") + "がいります。",
         "名前は、本人確認書類と同じ書き方で入れるよう案内されています。")
out += p("抽選で空きが出たら、会場ごとに二次の先着予約もあります。",
         "受付はどれも20時からです。")
out += table(("二次先着の受付", "会場"), [
    ("11/16(月)20:00〜", "札幌アピア・仙台パルコ・広島パルコ・アミュプラザくまもと"),
    ("11/17(火)20:00〜", "名古屋パルコ・大阪梅田"),
    ("11/18(水)20:00〜", "いちばんプラザ・ギンザミライミュージアム"),
])
out += h3("先着(12月1日〜10日の入店分)")
out += p("12月1日(火)から10日(木)の入店分は、先着順の予約です。",
         "受付は" + mark("行きたい日の前の日の18時から") + "始まります。",
         "たとえば12月1日の分は、11月30日(月)18時からです。")
out += p("大阪梅田だけは、会場が12月9日(水)で終わるので注意してください。",
         "11日からの予約は、まだ案内が出ていません。")
out += h3("当日の持ち物と注意点")
out += p("当日は" + mark("本人確認書類を必ず持っていく") + "必要があります。",
         "コピーやスクリーンショットは使えません。")
out += mini(("申し込み", "1日1会場、1人1回まで"),
            ("チケット", "本人だけ有効。ゆずったり売ったりはできない"),
            ("入店", "チケット1枚につき1人・1会計"),
            ("同伴", "小学生以下の子どもや介助の人は原則1人まで(制限のあるグッズは買えない)"),
            ("QRコード", "入店の5分前にLINEに届き、30分たつと使えなくなる"))
out += p("入店予約は安全のためのもので、" + mark("グッズを買えることの約束ではない") + "とされています。",
         "人気のグッズは、入れても売り切れている場合があるので気をつけましょう。")
out += p("SNSでは「顔写真が必要なのは転売対策になって良い」という声が多く見られました。",
         "いっぽうで「顔写真まで出すのは少し不安」「申し込んでまで行かなくてもいいかな」という人もいます。")

# ---- 予約 ----
out += h2("ちいかわクリニックの「予約」は受注生産？通販の注意点")
out += p("今回いちばん多かった疑問が、ちいかわマーケットの「予約」についてです。",
         "「予約ってことは、待てば必ず買えるの？」と思った人も多いようです。")
out += p("答えは、" + mark("受注生産ではありません") + "。",
         "商品ページには「数量には限りがございます。受注生産ではございません。」と書かれています。",
         "つまり、予約も先着順で、数がなくなればそこで終わりです。")
out += mini(("予約の受付", "11月27日(金)11時から"),
            ("届く時期", "2026年12月中旬以降、入荷しだい順番に発送"),
            ("キャンセル", "発送がおくれてもできない"),
            ("いっしょに買えるもの", "予約の商品どうしだけ(ふつうの商品と同時に買うと注文がキャンセルになる)"))
out += p("また、" + mark("全部のグッズが予約できるわけではありません") + "。",
         "マスコットやタオルのように予約がある商品と、当日に売るだけの商品があります。")
out += p("SNSでは「ぬいぐるみを予約にしてくれてありがとう」と喜ぶ声が目立ちました。",
         "いっぽうで「欲しいのは予約がないものばかり」と、なやむ人もいます。")
out += voice("「受注では無く予約？数に限りがある？通常販売もする？文章の意味がわからな過ぎる」")
out += p("こうした声もあったように、予約と通常販売の両方がある点で混乱が起きています。",
         "すぐ欲しくない人は予約、すぐ欲しい人は通常販売、と分けて考えるとわかりやすいです。")

# ---- 臓器 ----
out += h2("臓器マスコットは何？だれがどの臓器？")
out += p("SNSでいちばん盛り上がったのが、" + mark("臓器の形をしたグッズ") + "です。",
         "「ナース姿かわいい」と見ていたら、臓器が出てきてびっくりした人が多かったようです。")
out += mini(("ないぞういろいろマスコット", "全9種・1回990円・1日5回まで(ちいかわくじで販売)"),
            ("臓器磁器", "3種・各2,200円"),
            ("ないぞういろいろホログラムステッカー", "全9種(ちいかわマーケットの購入特典)"))
out += p("「ないぞういろいろマスコット」は、オンラインくじの「ちいかわくじ」で売られます。",
         "心臓・胃・肺・肝臓・大腸などの形に、キャラクターの顔がついたボールチェーンのマスコットです。")
out += p("だれがどの臓器かは、顔を見るとわかるようになっています。",
         "SNSで特に話題なのが、" + mark("くりまんじゅうが肝臓") + "という組み合わせです。")
out += p("くりまんじゅうは、お酒が大好きなキャラクターです。",
         "原作には、くりまんじゅうがシーサーに「自分を肝臓だと思いなさい」と話す場面もあります。",
         "そのため「ぴったりすぎる」「ジワる」と笑う人が続出しました。")
out += p("ほかにも「大腸のシーサーが欲しい」「膵臓が買える」といった声が出ています。",
         "「なぜその臓器になったのか考察してほしい」という人もいて、しばらく話題が続きそうです。")

# ---- 値段 ----
out += h2("ちいかわクリニックのグッズの値段は？")
out += p("第1弾は、マスコットからポーチ、シールまでたくさんの種類があります。",
         "主なグッズの値段は次のとおりです(すべて税込)。")
out += table(("グッズ", "値段"), [
    ("おだいじにね。マスコット(ナース姿・12種)", "1,650〜1,980円"),
    ("われわれにおまかせください。マスコット(ドクター姿・2種)", "各1,980円"),
    ("おくすりになっちゃったポーチ(3種)", "各1,650円"),
    ("おくすり袋風なポーチ", "1,980円"),
    ("レントゲンなクリアポーチ", "1,430円"),
    ("視力検査なデイリーユーストート", "3,850円"),
    ("ナースなみんなのショルダーポケットポーチ", "2,970円"),
    ("マルチケース", "3,300円"),
    ("臓器磁器(3種)", "各2,200円"),
    ("近況報告マグネット(5種)", "各550円"),
    ("絆創膏風フレークシール", "550円"),
])
out += p("ナース姿のマスコットは12種あります。",
         "ちいかわ・ハチワレ・うさぎ・モモンガ・くりまんじゅう・ラッコの6人がまずそろいます。",
         "さらにシーサー・古本屋・あのこ・カブトムシ・オデ・ポシェットの鎧さんも加わります。")
out += p("ドクター姿は、うさぎとラッコの2種です。")
out += p("マスコットをぜんぶそろえると、" + mark("2万円をこえる") + "計算になります。",
         "SNSでは「マスコットだけで2万近い？」「大破産」という声も上がっていました。")
out += p("ほかにも、ウイルス姿のオデや、バイキン姿のゴブリンのミニマスコットもあります。",
         "「うがいしよう！」「手を洗おう！」という名前がついていて、ちいかわらしい遊び心を感じますね。")

# ---- 特典・制限 ----
out += h2("特典(ノベルティ)と購入制限は？")
out += p("買った金額に応じて、もらえる特典があります。",
         "通販と会場でちがうので、分けて紹介します。")
out += h3("ちいかわマーケット(通販)の特典")
out += table(("買った金額(1回の注文)", "もらえるもの"), [
    ("1,100円ごと", "ないぞういろいろホログラムステッカー(全9種から1枚)"),
    ("3,300円以上", "ちいかわクリニックのオリジナルBOXに入れて届く"),
    ("8,800円以上", "ぬいぐるみおかおバッジ(全8種から1個)"),
])
out += h3("期間限定会場の特典")
out += table(("買った金額(1会計)", "もらえるもの"), [
    ("3,300円以上", "プラスチックカード(全8種から1枚)"),
    ("5,500円以上", "サラサクリップボールペン(1本)"),
    ("8,800円以上", "ぬいぐるみおかおバッジ(全8種から1個)"),
])
out += p("どの特典も、" + mark("なくなりしだい終わり") + "です。",
         "送料は金額にふくまれないので注意しましょう。")
out += p("会場では、記念のグッズは1会計につき各1個までです。",
         "ランダムのグッズは1箱まで、カプセルトイは2種あわせて10回までとされています。")

# ---- 第2弾 ----
out += h2("ちいかわクリニック第2弾はいつ？")
out += p("第2弾は" + mark("12月11日(金)") + "に発売されます。",
         "どんなグッズが出るかは、これから順番に発表されるそうです。")
out += p("SNSでは「第2弾でぼっちゃりシリーズが復活しそう」と予想する声がありました。",
         "ステッカーやタオルに「ぼっちゃり」の絵柄が入っていることから、期待が高まっているようです。",
         "第1弾でお金を使いすぎないよう、予算を分けておくのがよさそうですね。")

# ---- 反応 ----
out += h2("ちいかわクリニックへのSNSの反応は？")
out += p("発表からすぐに、SNSにはたくさんの声があつまりました。",
         "多かったのは、キャラクターのナース姿・ドクター姿へのツッコミです。")
out += voice("「こういう貫禄ある婦長さん居るよね」")
out += p("ナース姿のくりまんじゅうは、「師長さんみたい」「婦長み」と大人気です。",
         "ふだんお酒を飲んでいる姿から「ほぼ患者では？」というツッコミもありました。")
out += voice("「うさぎは耳鼻科ドクターなんですね。最近あまり見ない額帯鏡つけてる」")
out += p("ドクター姿のうさぎは、頭に丸い鏡(額帯鏡)をつけていて「昭和のお医者さん」と話題です。",
         "メガネをかけたラッコ先生には「イケメン」「動悸、息切れ」という声が集まりました。")
out += p("ほかにも、こんな声がありました。")
out += html(f'''<ul style="margin:0 0 16px 0;padding:12px 16px 12px 32px;background:{BG};border-radius:4px;">
<li>「なんでいつも金曜日の11時なんだろう」(平日の昼で買いにくい)</li>
<li>「歯医者さんなど病院がライバルになりそう」</li>
<li>「職場につけても許される気がする」</li>
<li>「医療職としてはアツい」</li>
<li>「検索するとサジェストに“いちかわクリニック”が出てくる」</li>
</ul>''')
out += p("病院がテーマなので、医療の仕事をしている人からの反応が多いのも今回の特徴です。",
         "病院で働く人のあいだでも、争奪戦になるかもしれません。")

# ---- まとめ ----
out += h2("まとめ")
items = [
    "ちいかわクリニックは毎年恒例のグッズシリーズの2026年版(テーマは病院)",
    "第1弾は11月27日(金)、第2弾は12月11日(金)に発売",
    "期間限定会場8か所の入店抽選は11月13日(金)10時〜15日(日)23時59分",
    "申し込みはLINEで、顔写真と名前の登録・当日の本人確認書類が必要",
    "ちいかわマーケットの「予約」は受注生産ではなく、数に限りあり",
    "臓器マスコットはくじで販売、くりまんじゅうの肝臓が大きな話題に",
]
out += html(f'<div style="border:1px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">'
            + "".join(f'<p style="margin:{"0" if i == 0 else "6px 0 0 0"};">{CHK}{t}</p>' for i, t in enumerate(items)) + "</div>")
out += p("まずは11月13日(金)10時からの入店抽選を忘れずに申し込みましょう。",
         "通販派の人は、11月27日(金)11時の予約受付が勝負です。")
out += p('出典:<a href="https://prtimes.jp/main/html/rd/p/000000083.000168561.html" target="_blank" rel="noopener">PR TIMES「ちいかわクリニック」第一弾アイテム</a>/'
         '<a href="https://prtimes.jp/main/html/rd/p/000000412.000001117.html" target="_blank" rel="noopener">PR TIMES 期間限定ショップ『ちいかわクリニック』</a>')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
if "--build-only" in sys.argv:
    open(OUT, "w", encoding="utf-8").write(out)
    print(OUT, len(out))
    sys.exit()

# ================= upload =================
out = open(OUT, encoding="utf-8").read()  # easy_read fix 後のファイルを使う
env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_TREND_USERNAME']}:{env['WP_TREND_APP_PASSWORD']}".encode()).decode()


def req(path, data=None, headers=None, method="POST"):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode('utf-8', 'ignore')[:500]}")


def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})


state = json.load(open(POSTED, encoding="utf-8")) if os.path.exists(POSTED) else {}
if "post" in state:
    if "--update-content" in sys.argv:
        jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"title": TITLE, "content": out, "status": "draft"})
        print("content updated", state["post"])
    else:
        print("already posted", state["post"])
else:
    po = jpost("/wp-json/wp/v2/posts", {"title": TITLE, "content": out, "slug": SLUG, "status": "draft",
                                        "categories": CATEGORIES, "author": AUTHOR})
    state["post"] = po["id"]
    json.dump(state, open(POSTED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("draft", po["id"])
po = req(f"/wp-json/wp/v2/posts/{state['post']}?context=edit", method="GET")
print(po["id"], po["status"], po["author"], po["categories"], po["featured_media"], po["title"]["raw"])
print(f"{BASE}/wp-admin/post.php?post={po['id']}&action=edit")
