# -*- coding: utf-8 -*-
"""ユ・ヒョンスン&浅香孝太郎 京都Vlog聖地記事(chomoand-1.com JP下書き)。
元動画: ユ・ヒョンスン公式YouTube「日本人が韓国語で、韓国人が日本語で話す京都デート | VOLG」(2026-09-27公開)。
本文画像は動画から直接切り出したフレーム(scratchpadに保存、gitには入れない)。
"""
import json, re, subprocess, sys
from pathlib import Path

import requests

from ko1keyz_article_kit import ROOT, WP_URL, HEADERS_AUTH, wphtml, p, h2, a, Ui

FRAME_DIR = Path(r"C:\Users\s30se\AppData\Local\Temp\claude\c--Users-s30se-OneDrive--------CHOMO\9f44fa80-978f-44b8-8727-4c0d5f8cf927\scratchpad\kyoto\fr")
VIDEO = "https://www.youtube.com/watch?v=11O16cjVi6c"
IDS_FILE = ROOT / "tmp_hyeonseung_kotaro_kyoto_vlog_ids.json"

ACCENT, BORDER, BG = "#8a8378", "#ddd9d3", "#f7f6f4"  # KO1KEYZ非メンバー(日プ新世界)記事のウォームグレー
ui = Ui(ACCENT, BORDER, BG, "rgba(138,131,120,0.06)")

ids = json.loads(IDS_FILE.read_text(encoding="utf-8")) if IDS_FILE.exists() else {}
FRAMES = {
    "open": "hyeonseung_kotaro_kyoto_open.jpg",
    "kamo_bridge": "hyeonseung_kyoto_kamogawa.jpg",
    "soba": "hyeonseung_kotaro_takahashi_soba.jpg",
    "cafe_both": "kotaro_cafe_otowa_affogato.jpg",
    "kyuri": "hyeonseung_kotaro_kyuri_ipponzuke.jpg",
    "shakujo": "hyeonseung_kiyomizu_shakujo.jpg",
    "butai": "hyeonseung_kotaro_kiyomizu_butai.jpg",
}
media = {}
for key, fname in FRAMES.items():
    if key in ids.get("media", {}):
        media[key] = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{ids['media'][key]}", headers=HEADERS_AUTH).json()
        continue
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HEADERS_AUTH, "Content-Type": "image/jpeg",
                               "Content-Disposition": f'attachment; filename="{fname}"'},
                      data=(FRAME_DIR / f"{key}.jpg").read_bytes())
    r.raise_for_status()
    media[key] = r.json()
    print("uploaded", key, media[key]["id"])
ids["media"] = {k: v["id"] for k, v in media.items()}
IDS_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")


def img(key, alt, cap_prefix="出典:"):
    m = media[key]
    sizes = m["media_details"].get("sizes", {})
    full, fw, fh = m["source_url"], m["media_details"]["width"], m["media_details"]["height"]
    large = sizes.get("large", {"source_url": full, "width": fw})
    medium = sizes.get("medium", {"source_url": full, "width": fw})
    w = large["width"]
    h = int(w * fh / fw)
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{large["source_url"]}" alt="{alt}" width="{w}" height="{h}"
  style="max-width:100%;height:auto;"
  srcset="{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {w}w, {full} {fw}w"
  sizes="(max-width: {w}px) 100vw, {w}px">
<figcaption style="text-align:center;font-size:12px;">{cap_prefix}{VIDEO}</figcaption>
</figure>''')


def gmap(q, z=16):
    from urllib.parse import quote
    return wphtml(f'''<iframe
  src="https://maps.google.com/maps?q={quote(q)}&t=&z={z}&ie=UTF8&iwloc=&output=embed"
  width="100%" height="350" frameborder="0" scrolling="no"
  style="border:0;" loading="lazy">
</iframe>''')


def route_table(header, rows):
    th = "".join(f'<td style="background:{ACCENT};color:#fff;border:1px solid {BORDER};padding:8px 10px;"><strong>{c}</strong></td>' for c in header)
    trs = ""
    for i, r in enumerate(rows):
        bg = "#fff" if i % 2 == 0 else BG
        trs += "<tr>" + "".join(f'<td style="background:{bg};border:1px solid {BORDER};padding:8px 10px;">{c}</td>' for c in r) + "</tr>\n"
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr>{th}</tr>
{trs}</tbody></table></figure>
<!-- /wp:table -->'''


def marker(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


title = "ヒョンスン＆孝太郎の京都Vlog聖地は？蕎麦・カフェ・清水寺！"

B = []
B.append(p(
    "日プ新世界で注目を集めたユ・ヒョンスンと浅香孝太郎の2人が、京都を1日満喫するVlogを公開しました。",
    "鴨川で水遊びをして、お蕎麦を食べて、清水寺でかき氷…と、見ているだけで京都に行きたくなる内容です。",
    "動画に映っていたお店を調べてみたところ、お昼ご飯は<strong>五条河原町の「蕎麦手打ち たか橋」</strong>、休憩したカフェは<strong>清水寺のすぐそばの「CAFE OTOWA(カフェ オトワ)」</strong>でした。",
    "この記事では、2人が回ったルートを順番に追いながら、お店のメニューや営業時間、聖地巡礼するときのポイントまでまとめています。",
))
B.append(ui.table("京都Vlogの基本情報", [
    ("動画タイトル", "日本人が韓国語で、韓国人が日本語で話す京都デート | VOLG"),
    ("公開日", "2026年9月27日"),
    ("チャンネル", "ユ・ヒョンスン公式YouTube(유현승 ヒョンスン)"),
    ("出演", "ユ・ヒョンスン、浅香孝太郎"),
    ("長さ", "約13分半"),
]))
B.append(img("open", "京都Vlogのオープニング、並んであいさつするユ・ヒョンスン(赤髪)と浅香孝太郎(金髪)"))
B.append(ui.titlebox("この記事でわかること", [
    "京都Vlogの内容と2人の関係",
    "2人が回ったルート",
    "水遊びをした鴨川の場所",
    "お昼ご飯の蕎麦屋",
    "かき氷を食べたカフェ",
    "清水寺で挑戦したこと",
    "聖地巡礼のモデルコース",
]))
B.append(route_table(["順番", "場所", "2人がしたこと"], [
    ("1", "京都駅周辺〜鴨川(七条大橋付近)", "裸足で川に入って水遊び"),
    ("2", "蕎麦手打ち たか橋(五条河原町)", "お昼ご飯にざる蕎麦と天ぷら"),
    ("3", "五条坂〜CAFE OTOWA", "いちごかき氷と抹茶アフォガートで休憩"),
    ("4", "清水坂のお店", "きゅうりの一本漬けに初挑戦"),
    ("5", "清水寺", "弁慶の錫杖に挑戦、清水の舞台で記念撮影"),
    ("6", "大阪(長堀エリア)", "夜は映画を観て解散"),
]))

# ---- 動画の内容 ----
B.append(h2("ヒョンスン＆孝太郎の京都Vlogはどんな動画？"))
B.append(ui.minibox("<strong>コンセプト:</strong>日本人の孝太郎が韓国語、韓国人のヒョンスンが日本語で話す京都デート",
                    "<strong>公開先:</strong>ユ・ヒョンスン公式YouTubeチャンネル"))
B.append(p(
    "今回の動画は、ユ・ヒョンスンのYouTubeチャンネルで2026年9月27日に公開されたVlogです。",
    "タイトルどおり、日本人の浅香孝太郎があえて韓国語で、韓国人のヒョンスンが日本語で話すというルールで京都を歩いています。",
    "途中で「なんでお互いに言語を変えて話してるんですか？」と自分たちでツッコむ場面もあり、この逆転ルールがいい味を出していました。",
))
B.append(p(
    "2人はもともと、韓国のボーイズグループPICKUS(ピカス)の元メンバー同士です。",
    "その後、韓国のオーディション番組「PROJECT 7(プジェ)」を経て、2026年春の「PRODUCE 101 JAPAN 新世界(日プ4)」にもそろって参加していました。",
    "長い時間を一緒に過ごしてきた2人だけに、会話のテンポや遠慮のない掛け合いからも仲の良さが伝わってきます。",
    f"2人の経歴については、{a('https://chomoand-1.com/yoohyeonseung_wiki-1732', 'ユ・ヒョンスンのwiki風プロフィール記事')}と{a('https://chomoand-1.com/asakakotaro_wiki-1228', '浅香孝太郎のwiki風プロフィール記事')}で詳しく紹介しています。",
))
B.append(p(
    "動画の中では、行き先を「タロくんのおすすめで」決める場面があり、京都案内は大阪出身の孝太郎が担当していたようです。",
    "ヒョンスンにとっては今回が初めての京都だったようで、冒頭から「修学旅行！」とテンションが上がっていました。",
    "街中に貼られていた展覧会のポスター(会期は2026年7月25日〜8月23日)や、日傘と携帯扇風機が手放せない様子から、撮影は今年の真夏とみられます。",
))

# ---- 鴨川 ----
B.append(h2("水遊びをした鴨川はどこ？七条大橋付近とみられる"))
B.append(ui.minibox("<strong>場所(推定):</strong>京都市立芸術大学の近く、七条大橋付近の鴨川",
                    "<strong>最寄り駅:</strong>京阪「七条」駅、JR「京都」駅から徒歩圏"))
B.append(p(
    "電車で京都に着いた2人がまず向かったのは、ヒョンスンいわく「すごく綺麗なところ」という鴨川でした。",
    "途中では京都市立芸術大学のギャラリー「@KCUA」の展覧会ポスターの前を通っており、京都駅の東側、鴨川沿いの崇仁エリアを歩いていたことが分かります。",
))
B.append(img("kamo_bridge", "鴨川の浅瀬に裸足で入るユ・ヒョンスン、背後に連なるアーチ橋"))
B.append(p(
    "川に着くなり、ヒョンスンは靴を脱いで浅瀬へ入り、「兄さんも来てください〜！」と孝太郎を呼び込んでいました。",
    "背景に写っているいくつものアーチが連なる橋は、1913年に完成した鴨川で現存最古の橋、<strong>七条大橋</strong>の姿によく似ています。",
    "京都市立芸大からも歩いてすぐの場所なので、2人が水遊びをしたのは七条大橋のすぐ上流あたりとみてよさそうです。",
))
B.append(p(
    "もうひとつ見逃せないのが、ヒョンスンの「ハト好き」です。",
    "植え込みにいたハトに夢中になって「ハト、めっちゃ好きです」と話し、石垣を登るハトには「登山ハト」と名前をつけて大はしゃぎ。",
    "孝太郎から「カカオトークのプロフィール写真、ハトだったじゃん」とツッコまれる場面もあり、筋金入りのハト好きのようです。",
))
B.append(gmap("七条大橋 京都"))

# ---- たか橋 ----
B.append(h2("お昼の蕎麦屋は五条河原町の「蕎麦手打ち たか橋」"))
B.append(ui.minibox("<strong>店名:</strong>蕎麦手打ち たか橋(soba restaurant Takahashi)",
                    "<strong>住所:</strong>京都府京都市下京区平居町23(河原町五条の交差点から南へ約100m)",
                    "<strong>食べたもの:</strong>ざる蕎麦と天ぷら(鶏天とみられる揚げ物・海老天など)"))
B.append(p(
    "鴨川でひと遊びしたあと、「お腹空いてる」という2人がお昼ご飯に選んだのが、五条河原町にある「蕎麦手打ち たか橋」です。",
    "「今日のお昼ご飯のメニュー」というテロップとともに映っていたのは、竹ざるに盛られた蕎麦と、大皿の天ぷらでした。",
))
B.append(img("soba", "蕎麦手打ち たか橋で2人が食べたざる蕎麦と天ぷら、わさび・ねぎ・大根おろしの薬味"))
B.append(p(
    "天ぷらのお皿には、ごろっとした衣の揚げ物と青菜の天ぷらが盛られており、もう1皿には海老天も見えます。",
    f"たか橋では鶏肉の天ぷらを添えた{marker('「かしわ天ざる」')}が以前から定番メニューとして紹介されており、映像の揚げ物もこのかしわ天(鶏天)である可能性が高そうです。",
    "食べ終わったあとの2人は「食べました〜！」と満足げで、「あそこはたぶん、天ぷらがめっちゃ」と天ぷらを絶賛していました。",
))
B.append(p(
    "たか橋は、祇園で修業した職人が打つ手打ち蕎麦のお店です。",
    "粗挽きの「外一(といち)蕎麦」と細挽きの「十割蕎麦」の2種類があり、両方を食べ比べられる「二種盛り」も人気メニューのひとつです。",
    "お店はかつてのお茶屋の建物をそのまま活かしていて、外観や看板にも当時の面影が残っています。",
    "動画に映っていた、和箪笥が並ぶ落ち着いた店内も、この古い建物ならではの雰囲気でした。",
))
B.append(ui.table("蕎麦手打ち たか橋の店舗情報", [
    ("住所", "京都府京都市下京区平居町23"),
    ("アクセス", "京阪「清水五条」駅から徒歩約3分"),
    ("営業時間", "昼 11:30〜15:00(木・金・土は夜 18:00〜21:00も営業、夜は予約推奨)"),
    ("定休日", "月曜日"),
    ("予算", "1,000〜2,000円ほど"),
    ("メニュー例", "かしわ天ざる、二種盛り(外一・十割)など"),
]))
B.append(p(
    "メニューや価格、営業時間は変わることがあるので、訪れる前にお店の最新情報をチェックしておくと安心です。",
    "河原町通から少し入った路地にあるので、地図を見ながら向かうのがおすすめです。",
))
B.append(gmap("蕎麦手打ち たか橋 京都市下京区平居町23", 17))

# ---- CAFE OTOWA ----
B.append(h2("かき氷を食べたカフェは清水寺そばの「CAFE OTOWA」"))
B.append(ui.minibox("<strong>店名:</strong>CAFE OTOWA(カフェ オトワ)",
                    "<strong>住所:</strong>京都府京都市東山区五条橋東6-583-31(五条坂・茶わん坂のすぐそば)",
                    "<strong>食べたもの:</strong>いちごのかき氷、抹茶アフォガート"))
B.append(p(
    "お昼のあとは五条坂を上って清水寺方面へ。",
    "「溶けそう」と言いながら坂を歩いた2人が逃げ込んだのが、清水寺の参道のすぐ手前にある「CAFE OTOWA」でした。",
    "店内に入った孝太郎は、ピンクの携帯扇風機を片手に「涼しくなりました」とひと息ついていました。",
))
B.append(img("cafe_both", "CAFE OTOWAで抹茶を注ぐ浅香孝太郎、手前にいちごのかき氷"))
B.append(p(
    f"テーブルに並んだのは、果肉たっぷりのソースがかかった{marker('いちごのかき氷')}と、バニラアイスに抹茶をかけて食べる{marker('抹茶アフォガート')}です。",
    "孝太郎はショットグラスの抹茶を自分でアイスに回しかけていて、濃い緑の抹茶がとろりとアイスを包む様子がとても美味しそうでした。",
    "かき氷はヒョンスンが「思っていたよりずっと大きいね」と驚くほどのボリュームで、大きさにも注目です。",
))
B.append(p(
    "CAFE OTOWAは2016年オープンのカフェで、京抹茶を使ったスイーツやオリジナルシロップのかき氷、軽食まで楽しめるお店です。",
    "いちごのかき氷は練乳をトッピングできて、抹茶アフォガートは抹茶のほろ苦さとさっぱりしたバニラの相性が良いと評判のメニューです。",
    "木のぬくもりを感じる店内はカウンターとテーブル合わせて25席ほどで、観光の合間にゆっくり休めるのもうれしいポイントでしょう。",
))
B.append(p(
    "ちなみに、このカフェでは「【孝太郎・23】※貧乏性」というテロップ付きのトークも飛び出しました。",
    "「こんなのも食べたい気持ち…」「アイドルはダメ」「かしこまりました…」という2人の掛け合いには、思わず笑ってしまいます。",
))
B.append(ui.table("CAFE OTOWAの店舗情報", [
    ("住所", "京都府京都市東山区五条橋東6-583-31"),
    ("アクセス", "京阪「清水五条」駅から徒歩約15分、清水寺参道からすぐ"),
    ("営業時間", "11:00〜18:00ごろ(開店時間は11:30とする情報もあり)"),
    ("定休日", "水曜日(不定休の場合あり)"),
    ("予算", "1,000円前後〜"),
    ("メニュー例", "いちごかき氷、抹茶アフォガート、抹茶パフェ、ホットドッグなど"),
]))
B.append(p(
    "営業時間や定休日は情報源によって少し違うため、行く前にお店のSNSなどで確認しておくのがおすすめです。",
    "かき氷は季節によってメニューが変わることもあります。",
))
B.append(gmap("CAFE OTOWA 京都市東山区五条橋東6-583-31", 17))

# ---- 清水寺 ----
B.append(h2("清水寺ではきゅうりの一本漬けと弁慶の錫杖に挑戦"))
B.append(ui.minibox("<strong>食べ歩き:</strong>清水坂のお店のきゅうりの一本漬け",
                    "<strong>挑戦:</strong>本堂前の「弁慶の錫杖」を持ち上げる",
                    "<strong>記念撮影:</strong>清水の舞台で2ショット"))
B.append(p(
    "カフェで涼んだあとは、いよいよ清水寺へ。",
    "参道のお店で2人の目に留まったのが、氷水で冷やされたきゅうりの一本漬けです。",
    "テロップには「生まれて初めて見る食べ物…」と書かれていて、2人とも「初挑戦」の一本漬けを並んでかじっていました。",
))
B.append(img("kyuri", "清水寺の参道できゅうりの一本漬けを食べるユ・ヒョンスンと浅香孝太郎"))
B.append(p(
    "清水寺の境内でヒョンスンが挑戦したのが、本堂の入口付近に置かれた「弁慶の錫杖」です。",
    "清水寺の七不思議のひとつにも数えられていて、大錫杖は長さ約2.6m・重さ約96kg、小錫杖でも約17kgもあります。",
    "持ち上げられると願いが叶うともいわれていますが、テロップで「最後のラスボス」と紹介された大錫杖には、ヒョンスンも「全然無理でした」と完敗していました。",
))
B.append(img("shakujo", "清水寺の弁慶の錫杖に挑戦するユ・ヒョンスン"))
B.append(p(
    "最後は清水の舞台で、緑に囲まれた本堂を背景に2ショットを撮影。",
    "舞台では天気雨の話題になり、「日本では『狐の嫁入り』って言うんだって」「韓国では『狐雨』って言います」と、日韓の言葉の共通点で盛り上がっていました。",
))
B.append(img("butai", "清水寺の舞台で並んで写るユ・ヒョンスンと浅香孝太郎"))
B.append(gmap("清水寺", 16))

# ---- 夜 ----
B.append(h2("夜は大阪に戻って映画、京都旅の締めくくり"))
B.append(ui.minibox("<strong>夜の行き先:</strong>大阪(看板から長堀エリアとみられる)",
                    "<strong>したこと:</strong>映画館で映画を鑑賞"))
B.append(p(
    "京都を満喫した2人は、電車で「帰ります〜！」と京都をあとにしました。",
    "夜のシーンは映画館のロビーから始まり、ポップコーンを片手に映画を観たあと、夜の街を歩きながら感想を話しています。",
    "映り込んでいた「クリスタ長堀」の看板から、夜は大阪の心斎橋・長堀エリアにいたとみられます。",
    "最後はヒョンスンが「京都成功！」とサムズアップして、1日の旅が締めくくられていました。",
))

# ---- 聖地巡礼 ----
B.append(h2("ヒョンスン＆孝太郎の京都Vlog聖地巡礼モデルコース"))
B.append(ui.minibox("<strong>所要時間の目安:</strong>半日〜1日(徒歩中心)",
                    "<strong>注意:</strong>たか橋は月曜、CAFE OTOWAは水曜が定休日"))
B.append(p(
    "動画のルートはほぼ徒歩でつながっているので、同じ順番で回る聖地巡礼がしやすいのも魅力です。",
    "京都駅から鴨川へ歩き、北上してたか橋でお昼、そのまま五条坂を上ってCAFE OTOWA、清水寺という流れなら無理なく回れます。",
))
B.append(wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">京都Vlog聖地巡礼ルート</p>
<ol style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li style="margin:0 0 8px 0;">JR京都駅から東へ歩き、京都市立芸大の横を通って七条大橋付近の鴨川へ</li>
<li style="margin:0 0 8px 0;">鴨川沿いを北へ歩き、河原町五条の「蕎麦手打ち たか橋」でお昼ご飯</li>
<li style="margin:0 0 8px 0;">五条坂を上って「CAFE OTOWA」でかき氷と抹茶アフォガート</li>
<li style="margin:0 0 8px 0;">清水坂でキンキンに冷えたきゅうりの一本漬け</li>
<li style="margin:0;">清水寺で弁慶の錫杖に挑戦し、清水の舞台で記念撮影</li>
</ol>
</div>'''))
B.append(p(
    "たか橋は月曜日、CAFE OTOWAは水曜日が定休日なので、両方行きたい場合は火・木〜日曜日を選ぶと安心です。",
    "たか橋のランチは15時まで、清水寺周辺は夕方になると混雑するため、午前中のうちに鴨川からスタートするのがおすすめです。",
    "夏場に歩くなら、2人のように日傘や携帯扇風機、飲み物の準備もお忘れなく。",
))

# ---- まとめ ----
B.append(h2("まとめ"))
B.append(ui.summary([
    "<strong>動画:</strong>2026年9月27日公開、ヒョンスンが日本語・孝太郎が韓国語で話す京都デートVlog",
    "<strong>鴨川:</strong>京都市立芸大の近く、七条大橋付近とみられる",
    "<strong>お昼:</strong>五条河原町の「蕎麦手打ち たか橋」でざる蕎麦と天ぷら",
    "<strong>カフェ:</strong>清水寺そばの「CAFE OTOWA」でいちごかき氷と抹茶アフォガート",
    "<strong>清水寺:</strong>きゅうりの一本漬け、弁慶の錫杖、清水の舞台で2ショット",
    "<strong>夜:</strong>大阪に戻って映画を鑑賞",
]))
B.append(p(
    "元PICKUSの2人らしい息の合った掛け合いと、京都の定番スポットがぎゅっと詰まったVlogでした。",
    "動画を見返しながら同じルートを歩けば、2人と一緒に京都旅をしている気分になれそうですね！",
))
B.append(wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-1.com/yoohyeonseung_wiki-1732">ユ・ヒョンスンのwiki風経歴・プロフィール</a></li>
<li><a href="https://chomoand-1.com/yoohyeonseung_gakureki-1956">ユ・ヒョンスンの学歴(芸術高校・大学)</a></li>
<li><a href="https://chomoand-1.com/asakakotaro_wiki-1228">浅香孝太郎のwiki風経歴・バレエ歴</a></li>
<li><a href="https://chomoand-1.com/ko-taro-chrome-hearts-8177">浅香孝太郎のピアスのブランド考察</a></li>
<li><a href="https://chomoand-1.com/when-and-where-is-the-ricky-hy-11719">リッキー&amp;ヒョンスン合同イベントの日程・会場</a></li>
<li><a href="https://chomoand-1.com/produce101japan_kyoutsuuten-1351">日プ新世界 練習生の仲良しペア・同グループまとめ</a></li>
</ul>
</div>'''))

content = "\n\n".join(B)
plain = re.sub(r"<[^>]+>|<!--.*?-->", "", content)
print("chars:", len(plain), "| title len:", len(title))
assert len(title) <= 35

summary = ("ユ・ヒョンスンと浅香孝太郎の京都Vlogの聖地をまとめました。鴨川(七条大橋付近)、お昼の「蕎麦手打ち たか橋」、"
           "清水寺そばの「CAFE OTOWA」のかき氷と抹茶アフォガート、弁慶の錫杖まで。聖地巡礼ルートも紹介！")


def get_slug(fallback):
    return fallback


payload = {"title": title, "content": content, "status": "draft", "categories": [4], "author": 2,
           "meta": {"jetpack_publicize_message": summary}}
if ids.get("jp"):
    url = f"{WP_URL}/wp-json/wp/v2/posts/{ids['jp']}"
else:
    url = f"{WP_URL}/wp-json/wp/v2/posts"
    payload["slug"] = "hyeonseung-kotaro-kyoto-vlog"
r = requests.post(url, headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                  data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
ids["jp"] = post["id"]
ids["jp_slug"] = post["slug"]
IDS_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
print("JP_POST", post["id"], post["status"], post["slug"])

if not ids.get("eyecatch_jp"):
    out = ROOT / "images" / "hyeonseung_kotaro_kyoto_vlog_eyecatch.png"
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
                    "--top", "ヒョンスン＆孝太郎",
                    "--main", "京都Vlog",
                    "--bottom", "聖地はどこ？蕎麦・カフェ・清水寺！",
                    "--out", str(out), "--seed", str(post["id"])], check=True)
    m = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HEADERS_AUTH, "Content-Type": "image/png",
                               "Content-Disposition": 'attachment; filename="hyeonseung_kotaro_kyoto_vlog_eyecatch.png"'},
                      data=out.read_bytes())
    m.raise_for_status()
    ids["eyecatch_jp"] = m.json()["id"]
    IDS_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
fr = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}", headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                   data=json.dumps({"featured_media": ids["eyecatch_jp"], "status": "draft"}).encode("utf-8"))
fr.raise_for_status()
print("featured", ids["eyecatch_jp"], "PREVIEW", f"{WP_URL}/?p={post['id']}")
