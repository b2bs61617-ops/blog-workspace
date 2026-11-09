# -*- coding: utf-8 -*-
# chomoand-4.blog: はだかんぼうたち 特別展示(テレビ朝日本社1階アトリウム 11/10〜12/20)まとめ+行き方
# 2026-11-09 オシリ依頼(元ネタ: https://x.com/oshidoraEX/status/2119764198096060416)。「行き方とかも」入れる。
# 出典: ドラマ公式X(上記)、アトリウムの開放時間・アクセスはるるぶ/tenki.jpの施設情報(公式の時間発表は無し)
import json, sys, subprocess
import requests

from build_and_post_travis_japan_tour2027_odds_survey import (
    ROOT, WP_URL, HJSON, ACC, BORDER, BG, p, h2, h3, wphtml, mark, link,
    whatbox, minibox, table2, checklist, upload_media)

IMG_DIR = ROOT / "images" / "hadakanboutachi_exhibit_1110"
EYECATCH = IMG_DIR / "hadakanboutachi_exhibit_1110_eyecatch_canva.jpg"
PHOTOS = {
    "overview": (IMG_DIR / "exhibit_overview.jpg", "はだかんぼうたち特別展示 テレビ朝日アトリウム 全体"),
    "boots": (IMG_DIR / "exhibit_brown_boots.jpg", "はだかんぼうたち特別展示 ブラウンのレースアップブーツ"),
    "bw": (IMG_DIR / "exhibit_black_white_shoes.jpg", "はだかんぼうたち特別展示 黒と白の革靴"),
}
STATE = IMG_DIR / "_state.json"
DRY = "--dry" in sys.argv

TITLE = "【未】はだかんぼうたち展示の行き方は？テレ朝で鯖崎の靴や名刺！"
assert len(TITLE.replace("【未】", "")) <= 35, len(TITLE.replace("【未】", ""))
SLUG = "hadakanboutachi-exhibit-tv-asahi-atrium"
SITE = "https://chomoand-4.blog/"
TWEET = ("oshidoraEX", "2119764198096060416")
SRC_X = "https://x.com/oshidoraEX/status/2119764198096060416"

R = {
    "beer": ("はだかんぼうたちのビール瓶にトラジャの隠し要素？紅孔雀も！", "hadakanboutachi-beer-bottle-javantispar-1240"),
    "role": ("鯖崎涼はクズ？松田元太の役どころと原作のあらすじ！", "sabazaki-ryo-genta-matsuda-role-1184"),
    "ep1": ("はだかんぼうたち1話ロケ地はどこ？松田元太の靴店やホテルも！", "hadakanboutachi-ep1-filming-locations-1208"),
    "ep3": ("はだかんぼうたち3話ロケ地はどこ？青山のイタリアンや広場も！", "hadakanboutachi-ep3-filming-locations-1560"),
    "ep5": ("はだかんぼうたち5話ロケ地はどこ？麻布台ヒルズやバーも！", "hadakanboutachi-ep5-filming-locations-2081"),
    "love": ("はだかんぼうたちのLOVEはどこ？ホンノウスイッチと同じ新宿！", "hadakanboutachi-love-shinjuku-island-2208"),
    "tver": ("はだかんぼうたちの見逃し配信はどこ？関西の放送時間も！", "hadakanboutachi-tver-kansai-time-1186"),
    "ep5c": ("はだかんぼうたち5話の鯖崎の衣装は？ダブルのスーツやタイも！", "hadakanboutachi-ep5-sabazaki-costume-2109"),
}


def a(key):
    t, s = R[key]
    return f'<a href="{SITE}{s}">{t}</a>'


def src(url, text):
    return wphtml(f'<p style="font-size:12px;color:#888;margin:-8px 0 16px 0;">出典:{link(url, text)}</p>')


def infobox(title, rows):
    tds = "".join(
        f'<tr><td style="border:1px solid #d9cdee;padding:8px 12px;background:#ece5f7;width:32%;"><strong>{k}</strong></td>'
        f'<td style="border:1px solid #d9cdee;padding:8px 12px;background:#fff;">{v}</td></tr>' for k, v in rows)
    return wphtml(f'<div style="border:1px solid {ACC};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;background:{BG};">'
                  f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>'
                  f'<table style="border-collapse:collapse;width:100%;"><tbody>{tds}</tbody></table></div>')


def x_embed(user, tid):
    return wphtml(f'''<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><a href="https://twitter.com/{user}/status/{tid}">https://twitter.com/{user}/status/{tid}</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>''')


def gmap(q):
    return wphtml(f'<iframe src="https://www.google.com/maps?q={q}&output=embed" width="100%" height="380" '
                  'style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')


def figure(url, alt, cap):
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{url}" alt="{alt}" style="max-width:100%;height:auto;">
<figcaption>{cap}</figcaption>
</figure>''')


def build(img):
    cap = f'出典:{link(SRC_X, "ドラマ『はだかんぼうたち』公式X")}'
    b = []
    b.append(p([
        f"松田元太さん(Travis Japan)主演のドラマ『はだかんぼうたち』の{mark('特別展示')}が、2026年11月10日(火)から東京・六本木のテレビ朝日本社1階アトリウムで始まります。",
        "11月9日にドラマ公式Xが発表したもので、鯖崎涼(松田元太)が履いている靴や、松田さんが自分で書いたメッセージ入りの名刺など、劇中に登場した小道具が期間限定で並びます。",
        "本編では一瞬しか映らなかったアイテムも、ガラスケース越しにじっくり見られます。",
        f"展示期間は<strong>12月20日(日)までの予定</strong>で、アトリウムは誰でも入れる無料のスペースです。",
        "この記事では、展示されるアイテムと見どころ、テレビ朝日本社への行き方、行く時間帯や混雑の注意点、近くで回れるロケ地までまとめています。",
    ]))
    b.append(infobox("特別展示の基本情報", [
        ("展示名", "ドラマ『はだかんぼうたち』特別展示"),
        ("期間", "2026年11月10日(火)〜12月20日(日)予定<br>※変更の場合あり(最新情報は公式SNS)"),
        ("場所", "テレビ朝日本社 1階アトリウム<br>東京都港区六本木6-9-1(六本木ヒルズ内)"),
        ("入場料", "無料(アトリウムは一般開放のエリア)"),
        ("予約", "告知に予約の案内はなし"),
        ("最寄り駅", "日比谷線 六本木駅(1C出口)から徒歩約5分<br>大江戸線 六本木駅から徒歩約6分"),
        ("主な展示", "鯖崎の名刺(松田元太さん直筆)、瓶ビール、鯖崎・石羽の靴、靴工房「ならはし」の看板、石羽のメガネ ほか"),
    ]))
    b.append(whatbox([
        "はだかんぼうたちの特別展示ってなに？",
        "展示されるアイテム一覧",
        "鯖崎の靴・石羽の靴はどれ？",
        "直筆名刺とトラジャ仕様のビール瓶",
        "テレビ朝日本社への行き方(六本木駅・麻布十番駅から)",
        "アトリウムは何時から何時まで？",
        "行く前に知っておきたい注意点",
        "展示のついでに回れるロケ地",
    ]))

    # ---- what ----
    b.append(h2("はだかんぼうたちの特別展示はいつからどこで？"))
    b.append(minibox([
        ("発表", "2026年11月9日(ドラマ公式X)"),
        ("期間", "11月10日(火)〜12月20日(日)予定"),
        ("場所", "テレビ朝日本社1階アトリウム(六本木ヒルズ内)"),
    ]))
    b.append(p([
        "特別展示が発表されたのは、11月9日の夜です。",
        "ドラマ公式Xが「いつも『はだかんぼうたち』を応援してくださる皆さまへ」と、展示の写真3枚と一緒に告知しました。",
    ]))
    b.append(x_embed(*TWEET))
    b.append(p([
        "会場は、六本木ヒルズの中にあるテレビ朝日本社の1階「アトリウム」です。",
        "ガラス張りの吹き抜けになっている広いエントランスで、ふだんから番組のパネルやディスプレイが並び、誰でも自由に入って見学できます。",
        "展示期間は11月10日(火)から12月20日(日)までの予定で、約6週間あります。",
        "ただし公式は「展示期間は変更となる場合がございます」としているので、行く前に公式SNSを確認しておくと安心です。",
    ]))
    b.append(figure(img["overview"]["url"], PHOTOS["overview"][1], cap))
    b.append(p([
        "公式が公開した写真を見ると、真ん中にガラスケースの展示台があり、左に靴工房「ならはし」の赤い看板、右にドラマのポスターが立てられています。",
        "ケースの中には、白と黒の革靴、ブラウンのブーツ、緑のビール瓶、名刺などが白いサテンの布の上に並べられていました。",
        "窓の外には青いイルミネーションが写っていて、夜に行くとクリスマスらしい雰囲気の中で見られそうです。",
    ]))

    # ---- items ----
    b.append(h2("はだかんぼうたちの展示アイテムは？鯖崎の靴や名刺も"))
    b.append(minibox([
        ("公式が発表したアイテム(一部)", "名刺・瓶ビール・鯖崎と石羽の靴・ならはしの看板・石羽のメガネ"),
        ("ポイント", "「一部」とあるので、ほかの小道具も並んでいる可能性あり"),
    ]))
    b.append(p([
        "公式が発表した展示アイテムは、次の5つです。",
        "告知には「展示アイテム(一部)」と書かれているので、現地ではこのほかの小道具も見られるかもしれません。",
    ]))
    b.append(table2(["展示アイテム", "どんなもの？"], [
        ["メッセージ入りの名刺", "交差点で鯖崎が桃に渡した名刺。メッセージは松田元太本人の直筆"],
        ["瓶ビール", "ラウンジで鯖崎が飲むビール。Travis Japan仕様のラベル"],
        ["鯖崎・石羽の靴", "鯖崎が履いている靴と、石羽の靴"],
        ["靴工房「ならはし」の看板", "鯖崎が働く靴工房の赤い看板"],
        ["石羽のメガネ", "石羽拓(髙木雄也)がかけているメガネ"],
    ]))

    b.append(h3("松田元太が直筆したメッセージ入りの名刺"))
    b.append(p([
        f"いちばんの目玉は、鯖崎が交差点で桃に渡した{mark('メッセージ入りの名刺')}です。",
        "公式によると、名刺に書かれたメッセージは松田元太さん本人の直筆です。",
        "放送では鯖崎の手元が一瞬映るだけだったので、どんな字でどんな言葉が書かれていたのか、近くで見られるのはファンにとってかなりうれしいポイントです。",
        "写真では、ケースの手前に名刺らしいカードが立てて置かれているのが見えます。",
    ]))

    b.append(h3("トラジャ仕様のビール瓶「JAVANTISPAR」"))
    b.append(p([
        "ラウンジで鯖崎が飲んでいた緑の瓶ビールも並びます。",
        "公式が「#TravisJapan 仕様のラベル」と書いているとおり、このビールのラベルには「JAVANTISPAR」という名前が入っています。",
        f"文字を並べ替えると「TRAVISJAPAN」になるアナグラムで、ラベルの虎と孔雀のイラストは、宮近海斗さん・松田元太さん・松倉海斗さんの{mark('「紅孔雀」がモチーフ')}です。",
        "第1話の放送後に公式Xで明かされ、トラジャ担の間で話題になりました。",
        f"ラベルのくわしい中身は{a('beer')}でまとめています。",
    ]))

    b.append(h3("鯖崎の靴と石羽の靴"))
    b.append(p([
        "靴職人の鯖崎の物語らしく、展示の中心は靴です。",
        "公式の写真には、ブラウンのレースアップブーツと、黒と白の革靴の2足が写っています。",
    ]))
    b.append(figure(img["boots"]["url"], PHOTOS["boots"][1], cap))
    b.append(p([
        "1足目は、つま先に穴飾り(ブローグ)が入った、ブラウンのウイングチップのレースアップブーツです。",
        "かかとやつま先には履きジワがあり、実際に撮影で使われてきた雰囲気が伝わってきます。",
        "第1話の冒頭で、鯖崎がホテルの部屋でブーツを磨いて身支度をする場面があり、この1足が鯖崎の靴とみられます。",
    ]))
    b.append(figure(img["bw"]["url"], PHOTOS["bw"][1], cap))
    b.append(p([
        "2足目は、黒いつま先と白い甲を組み合わせた、とがったシルエットの革靴です。",
        "甲の部分が大きくくり抜かれていて、グレーの細いひもで結ぶ、かなり個性的なデザインです。",
        "中には木製のシューツリーが入れられていて、仕立てたばかりの靴のように大事に飾られています。",
        "石羽は鯖崎の店で結婚式用の靴を注文していたので、こちらは石羽の靴とみられます(どちらが誰の靴かは公式の写真からの推測です)。",
        f"鯖崎の役どころや石羽との関係は{a('role')}でくわしく紹介しています。",
    ]))

    b.append(h3("靴工房「ならはし」の看板と石羽のメガネ"))
    b.append(p([
        "展示台の左には、赤い板に白い文字で「Narahashi 靴工房」と書かれた看板が立っています。",
        "鯖崎が働き、師匠の奈良橋匠(平子祐希さん)が営む靴工房の看板で、ドラマでは工房の入口の上に掛けられていました。",
        f"工房の撮影場所は元麻布の靴店「元麻布スピカ」で、撮影のときだけこの看板に付け替えていたとみられます。{a('ep3')}で外観を紹介しています。",
        "石羽拓(髙木雄也さん)がかけているメガネも展示されます。",
        "髙木さん演じる石羽のきっちりした印象を作っているアイテムなので、こちらもじっくり見ておきたいところです。",
    ]))

    # ---- access ----
    b.append(h2("テレビ朝日本社への行き方は？六本木駅から徒歩5分"))
    b.append(minibox([
        ("住所", "東京都港区六本木6-9-1(六本木ヒルズ内)"),
        ("いちばん近い駅", "東京メトロ日比谷線 六本木駅(1C出口)から徒歩約5分"),
        ("駐車場", "テレビ朝日の駐車場はなし(六本木ヒルズの有料駐車場を利用)"),
    ]))
    b.append(p([
        "テレビ朝日本社は、六本木ヒルズの敷地の中、六本木ヒルズアリーナ(屋外のイベント広場)の目の前にあります。",
        "最寄り駅は六本木駅と麻布十番駅で、電車で行くのがいちばん便利です。",
    ]))
    b.append(table2(["駅・路線", "徒歩の目安"], [
        ["東京メトロ日比谷線 六本木駅(1C出口)", "約5分"],
        ["都営大江戸線 六本木駅", "約6分"],
        ["都営大江戸線 麻布十番駅", "約10分"],
        ["東京メトロ南北線 麻布十番駅", "約11分"],
    ]))
    b.append(h3("日比谷線 六本木駅からの行き方(いちばんわかりやすい)"))
    b.append(p([
        "初めて行く人には、日比谷線 六本木駅の1C出口から行くルートがおすすめです。",
        "1C出口は改札を出て地下通路をまっすぐ進んだ先にあり、そのまま六本木ヒルズの入口「メトロハット」につながっています。",
        "メトロハットのエスカレーターで上がると六本木ヒルズの中に出るので、案内板の「テレビ朝日」「六本木ヒルズアリーナ」の方向に進みます。",
        "アリーナの広場に出たら、正面に見えるガラス張りの大きな建物がテレビ朝日本社で、その1階がアトリウムです。",
        "屋根のある通路が多いので、雨の日でもぬれにくいルートです。",
    ]))
    b.append(h3("大江戸線 六本木駅・麻布十番駅からの行き方"))
    b.append(p([
        "大江戸線の六本木駅はホームがとても深いところにあるので、地上に出るまでに数分かかります。",
        "地上に出たら、六本木通り沿いに六本木ヒルズの方向へ歩くと、徒歩6分ほどで着きます。",
        "麻布十番駅からは、坂を上って六本木ヒルズに向かう形になり、徒歩10分ほどです。",
        "麻布十番からのルートは、テレビ朝日の裏手にある毛利庭園の近くを通るので、散歩がてら歩くのも楽しいです。",
    ]))
    b.append(gmap("テレビ朝日本社 東京都港区六本木6-9-1"))
    b.append(p([
        "車で行く場合、テレビ朝日には来館者用の駐車場がないため、六本木ヒルズの有料駐車場を使うことになります。",
        "週末や12月のイベントシーズンは周辺の道路も駐車場も混みやすいので、できれば電車で行くのがおすすめです。",
    ]))

    # ---- hours ----
    b.append(h2("アトリウムは何時から何時まで入れる？"))
    b.append(minibox([
        ("開放時間の目安", "9:30〜20:30(日曜は20:00まで)"),
        ("注意", "展示の時間は公式から発表されていない"),
    ]))
    b.append(p([
        "今回の告知では、展示を見られる時間帯は発表されていません。",
        f"観光ガイドなどの施設情報によると、テレビ朝日のアトリウムが開いているのは{mark('9時30分〜20時30分(日曜は20時まで)')}が目安です。",
        "展示もこの時間内に見られると考えられますが、番組の生放送やイベントの都合で入れる範囲が変わることもあるので、遅い時間に行く場合は時間に余裕を持っておきましょう。",
        "公式の写真は夜に撮られたもので、窓の外にイルミネーションが光っていました。",
        "仕事帰りや夕食の前後に立ち寄るのもいいですね。",
    ]))

    # ---- tips ----
    b.append(h2("はだかんぼうたちの展示に行く前の注意点"))
    b.append(minibox([
        ("ポイント", "期間変更の可能性・撮影ルール・混雑・テレビ局内でのマナー"),
    ]))
    b.append(h3("展示期間が変わることがある"))
    b.append(p([
        "公式は「展示期間は変更となる場合がございます」と案内しています。",
        "特に最終日近くに行く予定の人は、出かける前にドラマ公式Xを確認しておきましょう。",
    ]))
    b.append(h3("写真を撮る前に現地の案内を確認"))
    b.append(p([
        "今回の告知では、写真撮影ができるかどうかは書かれていません。",
        "アトリウムのほかの展示は記念撮影する人も多い場所ですが、展示ごとにルールが違うこともあるので、現地の掲示やスタッフの案内に従いましょう。",
        "撮影できる場合も、ほかの来場者が写り込まないように気をつけたいですね。",
    ]))
    b.append(h3("土日・放送翌日は混みやすい"))
    b.append(p([
        "ドラマは毎週土曜の夜に放送されているので、放送翌日の日曜日や週末は見に来る人が増えそうです。",
        "展示台は1つで、ケースの前に立てる人数は限られています。",
        "ゆっくり見たい人は平日の昼間がねらい目です。",
        "見終わったら次の人に場所をゆずるなど、譲り合って楽しみましょう。",
    ]))
    b.append(h3("テレビ局の中だというのを忘れずに"))
    b.append(p([
        "アトリウムはテレビ朝日の正面エントランスで、社員の方や番組の出演者、関係者も出入りする場所です。",
        "大きな声で騒いだり、通路をふさいだりしないように気をつけましょう。",
        "出演者の入り待ち・出待ちのような行為も、ほかの人の迷惑になるのでやめておきましょう。",
    ]))

    # ---- nearby ----
    b.append(h2("展示のついでに回れるはだかんぼうたちのロケ地は？"))
    b.append(minibox([
        ("近くのロケ地", "元麻布スピカ(鯖崎の靴工房)・麻布台ヒルズ(第5話)"),
    ]))
    b.append(p([
        "テレビ朝日のある六本木ヒルズの周りには、『はだかんぼうたち』のロケ地もあります。",
        "展示とあわせて回ると、ちょっとした聖地巡礼が楽しめます。",
    ]))
    b.append(table2(["ロケ地", "場面", "六本木ヒルズからの目安"], [
        ["元麻布スピカ(港区元麻布)", "鯖崎が働く靴工房「ならはし」", "歩いて行ける距離(元麻布方面)"],
        ["麻布台ヒルズ(港区麻布台)", "第5話で鯖崎と桃が歩いた場所", "歩いて行ける距離(麻布台方面)"],
        ["表参道ヒルズ(渋谷区神宮前)", "第1話で鯖崎が通行人の足元を眺める場所", "電車で約15分(日比谷線→銀座線など)"],
    ]))
    b.append(p([
        "特に元麻布スピカは、展示されている「ならはし」の看板が実際に掛けられていた靴店なので、展示で看板を見てから外観を見に行くと、ドラマの場面がよみがえります。",
        "ただし元麻布スピカは実際に営業している靴のお店で、水曜日が定休日です。",
        "外観を見るだけにして、お店の迷惑にならないようにしましょう。",
        f"それぞれのロケ地は{a('ep1')}や{a('ep5')}でくわしくまとめています。",
    ]))

    # ---- drama info ----
    b.append(h2("はだかんぼうたちはどんなドラマ？"))
    b.append(minibox([
        ("放送", "テレビ朝日系「オシドラサタデー」毎週土曜23時〜(2026年10月3日スタート)"),
        ("原作", "江國香織『はだかんぼうたち』"),
    ]))
    b.append(p([
        "『はだかんぼうたち』は、江國香織さんの小説を原作にしたラブストーリーです。",
        "松田元太さんにとって、テレビ朝日の連続ドラマで初めての主演作になりました。",
        "松田さん演じる靴職人の鯖崎涼が、10歳年上の歯科医・筒井桃(加藤ローサさん)に惹かれていく物語で、桃の婚約者・石羽拓を髙木雄也さんが演じています。",
        "監督・脚本などの制作チームは、2024年のドラマ『東京タワー』のメンバーが再集結しています。",
    ]))
    b.append(table2(["役名", "キャスト"], [
        ["鯖崎涼", "松田元太(Travis Japan)"],
        ["筒井桃", "加藤ローサ"],
        ["石羽拓", "髙木雄也"],
        ["堀田響子", "大沢あかね"],
        ["奈良橋匠", "平子祐希"],
        ["水崎葉月", "片岡凜"],
        ["筒井陽", "伊藤歩"],
    ]))
    b.append(p([
        f"見逃した回は、TVerやTELASAで見られます。くわしくは{a('tver')}をどうぞ。",
        "展示を見る前に、名刺や靴が出てきた場面を見返しておくと、実物を前にしたときの感動が大きくなりそうです。",
    ]))

    # ---- matome ----
    b.append(h2("まとめ"))
    b.append(checklist("この記事のポイント", [
        "『はだかんぼうたち』の特別展示が2026年11月10日(火)〜12月20日(日)予定で開催",
        "場所はテレビ朝日本社1階アトリウム(六本木ヒルズ内)、入場無料",
        "松田元太直筆メッセージ入りの名刺、トラジャ仕様のビール瓶、鯖崎・石羽の靴、ならはしの看板、石羽のメガネなど",
        "ブラウンのブーツが鯖崎の靴、黒と白の革靴が石羽の靴とみられる",
        "日比谷線 六本木駅1C出口からメトロハット経由で徒歩約5分",
        "アトリウムの開放時間の目安は9:30〜20:30(日曜は20:00まで)",
        "期間変更の可能性あり、撮影ルールは現地の案内に従う",
        "元麻布スピカ・麻布台ヒルズなど近くのロケ地もあわせて回れる",
    ]))
    b.append(p([
        "ドラマでは一瞬しか映らなかった名刺や靴を、実物で見られるのはうれしいですね！",
        "松田さんの直筆メッセージは、きっと現地でしか味わえない特別感があるはずです。",
        "クリスマスのイルミネーションが始まった六本木ヒルズで、鯖崎の世界にひたってみてください！",
    ]))
    keys = ["beer", "role", "ep1", "ep3", "ep5", "ep5c", "love", "tver"]
    lis = "\n".join(f'<li style="margin:0 0 6px 0;"><a href="{SITE}{R[k][1]}">{R[k][0]}</a></li>' for k in keys)
    b.append(wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACC};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい『はだかんぼうたち』の記事</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>'''))
    return "\n\n".join(b)


def main():
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    if DRY:
        fake = {k: {"url": "https://example.com/x.jpg"} for k in PHOTOS}
        html = build(fake)
        (IMG_DIR / "_dry.html").write_text(html, encoding="utf-8")
        print("dry chars:", len(html))
        return
    for k, (path, alt) in PHOTOS.items():
        if k not in state:
            state[k] = upload_media(path, alt, alt)
            STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    html = build(state)
    tmp = IMG_DIR / "_post.html"
    tmp.write_text(html, encoding="utf-8")
    names = "加藤ローサ,平子祐希,大沢あかね,片岡凜,伊藤歩,江國香織,髙木雄也"
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis", "--names", names, str(tmp)], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "check", "--group", "travis", "--names", names, str(tmp)], check=True)
    html = tmp.read_text(encoding="utf-8")
    if not EYECATCH.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
                        "--main", "松田元太",
                        "--bottom", "はだかんぼうたち展示の行き方は？", "--bottom", "テレ朝で鯖崎の靴や名刺！",
                        "--color-key", "松田元太", "--out", str(EYECATCH)], check=True)
    if "eyecatch" not in state:
        state["eyecatch"] = upload_media(EYECATCH, TITLE, TITLE.replace("【未】", ""))
        STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    body = {"title": TITLE, "slug": SLUG, "content": html, "status": "draft",
            "categories": [3], "author": 2, "featured_media": state["eyecatch"]["id"]}
    if "post_id" in state:
        body.pop("title"); body.pop("slug")
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{state['post_id']}", headers=HJSON, json=body)
    else:
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, json=body)
    r.raise_for_status()
    post = r.json()
    state["post_id"] = post["id"]
    STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    print("post", post["id"], post["status"], post["link"], "chars", len(html), "media", state["eyecatch"]["id"])


if __name__ == "__main__":
    main()
