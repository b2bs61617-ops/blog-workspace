# -*- coding: utf-8 -*-
# JUST!シン日本遺産 #14(和歌山県広川町編3・吉澤閑也+松田元太、2026-11-04放送)ロケ地記事 -> chomoand-4.blog 下書き
# 使い方: python build_and_post_shizugen_shinnihonisan14_hirogawa.py [--dry]
import json, base64, os, re, sys, subprocess, urllib.parse
from pathlib import Path
import requests

ROOT = Path(__file__).parent
DRY = "--dry" in sys.argv


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_CHOMO4_URL"].rstrip("/")
AUTH = base64.b64encode(f'{ENV["WP_CHOMO4_USERNAME"]}:{ENV["WP_CHOMO4_APP_PASSWORD"]}'.encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}
HJSON = {**HEADERS_AUTH, "Content-Type": "application/json"}

# 2人回(吉澤=黄・松田=青)なのでグループ色の紫で統一(#13と同じ)
BORDER = "#d9cdf0"
ACCENT = "#7e57c2"
BG = "#f5f2fb"

exec((ROOT / "tmp_shinnihon10" / "_helpers.py").read_text(encoding="utf-8"))

WORK = ROOT / "tmp_shinnihon14"
EYECATCH = ROOT / "images" / "shizugen_shinnihon14_eyecatch.jpg"


def upload_media(filepath: Path, filename: str, content_type: str):
    headers = {**HEADERS_AUTH, "Content-Type": content_type,
               "Content-Disposition": f'attachment; filename="{filename}"'}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=filepath.read_bytes())
    r.raise_for_status()
    return r.json()


def table(head, rows):
    th = "".join(f'<th style="border:1px solid {BORDER};padding:8px 10px;background:#ece5f7;">{h}</th>' for h in head)
    trs = "\n".join(
        "<tr>" + "".join(f'<td style="border:1px solid {BORDER};padding:8px 10px;">{c}</td>' for c in r) + "</tr>"
        for r in rows
    )
    return wphtml(f'<table style="border-collapse:collapse;width:100%;font-size:0.95em;"><thead><tr>{th}</tr></thead>\n<tbody>\n{trs}\n</tbody></table>')


title = "【未】【シン日本遺産】しずげんの広川町ロケはどこ？オーベルジュいさり・西広海岸(#14)"
TVER_SRC = "https://tver.jp/episodes/epkg13z0h7"
POST13 = f"{WP_URL}/?p=1848"
POST12 = f"{WP_URL}/?p=1710"
POST_GOODS = f"{WP_URL}/?p=1518"

img_defs = [
    ("mission", "3つ目のJUST「食べてよし!宿泊まってよし!広川町の激推しオーベルジュ」"),
    ("tanbo", "いさりを案内してくれた現場責任者の丹保直也さん"),
    ("noren", "古民家オーベルジュ「いさり」ののれん"),
    ("point", "シン・日本遺産ポイント「国の登録有形文化財の建築物をオーベルジュとして活用」"),
    ("r101", "戸田棟101号室。畳の大座敷にベッドが置かれた客室"),
    ("rooms", "いさりの客室。キッチン付きの部屋もある"),
    ("r204", "ペットと泊まれる「204」号室の入り口"),
    ("dogrun", "204号室の専用ドッグランを走り回る吉澤閑也"),
    ("dog", "いさりで出会ったワンちゃんを抱っこする吉澤閑也"),
    ("sabaku", "釣り対決で釣った魚をシェフがさばく"),
    ("tamakue", "吉澤閑也が釣ったタマクエのカルパッチョ"),
    ("umai", "タマクエのカルパッチョに「いやいつもの5倍は美味い!」"),
    ("hamachi", "ハマチのカルパッチョ"),
    ("course", "いさりの絶品コース料理"),
    ("tachiuo", "太刀魚と鶏のジュレ"),
    ("kumanogyu", "熊野牛と山椒のソース"),
    ("ahn", "吉澤閑也からの「あ〜ん」を受ける松田元太"),
    ("inamu", "「いなむー(人型モード)」も登場"),
    ("sorbet", "デザートの「爽涼みかんのソルベ/紀州百花蜜」"),
    ("pr", "英語PR「広川町を代表するくつろぎ空間を満喫しよう!」"),
    ("demukae", "広川町のみなさんがお出迎え"),
    ("mission2", "最後のJUST「“映え”過ぎ注意!自然が作り出す奇跡の絶景」"),
    ("nishihiro", "上空から見た西広海岸"),
    ("uyuni", "シン・日本遺産ポイント「『和歌山のウユニ塩湖』と称される映えスポット」"),
    ("matsu_photo", "matsuさんが西広海岸で撮った鏡面写真"),
    ("beach", "干潮の西広海岸を歩くしずげん"),
    ("satsuei", "水面の状態を確かめるmatsuさん"),
    ("fusion", "鏡面写真「げんた×しずや【フュージョンポーズ】」"),
    ("genta_pose", "鏡面写真「げんた【爽やかTJポーズ】」"),
    ("shizuya_pose", "鏡面写真「しずや【カーニバルポーズ】」"),
    ("pikmin", "鏡面写真「げんた×しずや×上野P【手に乗る白ピクミン】」"),
    ("oka", "フラットスキムボードを教えてくれたdbjapan local riderの岡俊樹さん"),
    ("skim", "岡俊樹さんのお手本。浅い水面をボードで滑る"),
    ("norikata", "まずはボードの乗り方から"),
    ("genta_ok", "松田元太がフラットスキムボードに成功"),
    ("genta_just", "成功して「JUST!」の松田元太"),
    ("shizuya_ok", "吉澤閑也もボードに乗って滑る"),
    ("aerial", "上空から見たJUS動画の撮影風景"),
    ("pr2", "英語PRでは西広海岸を上空から"),
    ("pr2en", "「空が水面に反射して生まれる奇跡の絶景!」"),
    ("thanks", "広川町のみなさん!ありがとうございました!"),
    ("yokoku", "次回予告「初コンビ!宮崎のシン日本遺産!」"),
]

IMG = {}
for key, alt in img_defs:
    fn = f"shizugen_shinnihon14_{key}.jpg"
    if DRY:
        IMG[key] = image_block(f"images/{fn}", 1280, 720, "", alt, TVER_SRC)
        continue
    m = upload_media(ROOT / "images" / fn, fn, "image/jpeg")
    IMG[key] = image_block(*img_urls(m), alt, TVER_SRC)
    print(key, m["id"])

MARK = '<span class="swl-marker" style="font-weight:bold;font-size:1.15em;">'

b = []
b.append(p([
    "2026年11月4日放送の「Travis JapanノJUST!シン日本遺産」#14は、和歌山県広川町編の3回目で、この町の最終回です。",
    "吉澤閑也と松田元太の“しずげん”ペアが向かったのは、" + MARK + "古民家オーベルジュ「いさり」</span>と、「和歌山のウユニ塩湖」とも呼ばれる" + MARK + "西広海岸</span>の2か所でした。",
    "前回の海上釣り対決で勝った吉澤のごほうびディナーから、鏡面写真とフラットスキムボードの撮影まで、放送の流れにそってロケ地をまとめます。",
]))
b.append(infobox("番組情報", [
    ("番組タイトル", "Travis JapanノJUST!シン日本遺産 和歌山県広川町に4つのJUST!(#14)"),
    ("放送日", "2026年11月4日(水)深夜"),
    ("放送局・配信", "ABCテレビ、TVerで見逃し配信。スタジオ企画を加えた特別版はTELASAで配信"),
    ("出演", "吉澤閑也・松田元太(Travis Japan)、いなむー(広川町マスコット)"),
    ("ナレーター", "小櫃裕太郎(ABCテレビアナウンサー)"),
    ("主なロケ地", "古民家オーベルジュ「いさり」/西広海岸"),
]))
b.append(whatbox([
    "#14で巡った広川町の2つのシン日本遺産",
    "オーベルジュ「いさり」の客室(戸田棟101号室・ペットと泊まれる204号室)",
    "釣り対決のごほうびで出たタマクエ・ハマチのカルパッチョとコース料理",
    "「和歌山のウユニ塩湖」西広海岸で撮った鏡面写真",
    "フラットスキムボードの「JUS動画」の結果",
]))
b.append(table(["場面", "ロケ地", "場所"], [
    ["客室紹介・ごほうびディナー", "古民家オーベルジュ「いさり」", "広川町広(稲むらの火の館の近く)"],
    ["鏡面写真", "西広海岸", "広川町西広"],
    ["フラットスキムボード", "西広海岸", "広川町西広"],
]))

# --- いさり
b.append(h2("3つ目のシン日本遺産は古民家オーベルジュ「いさり」"))
b.append(minibox([
    ("ロケ地", "ホテル「いさり」/レストラン「潮香(しおか)」(和歌山県有田郡広川町広1347)"),
    ("場面", "広川町の激推しオーベルジュを訪問。客室紹介と、釣り対決のごほうびディナー"),
]))
b.append(p([
    "広川町に用意された4つのJUSTのうち、3つ目は<strong>「食べてよし!宿泊まってよし!広川町の激推しオーベルジュ」</strong>。",
    "古い町並みが残る通りを歩いて、しずげんが「ここ?」「これ?」とのぞきこんだ先が、今回の舞台です。",
]))
b.append(IMG["mission"])
b.append(p([
    "出迎えてくれたのは、現場責任者の丹保直也さん。",
    "「オーベルジュってどういうこと?」と聞く2人に、「一般的なホテルに比べて、お食事を中心に地域を味わっていただくところ」と説明してくれました。",
]))
b.append(IMG["tanbo"])
b.append(IMG["noren"])
b.append(p([
    "のれんに書かれていたのは<strong>「いさり」</strong>の文字と、網をかたどったロゴ。",
    "ナレーションによると、かつて漁業の網を作っていた工場を改装してオーベルジュにした宿で、地元の食材をふんだんに使った料理が楽しめるそうです。",
]))
b.append(IMG["point"])
b.append(p([
    "画面のシン・日本遺産ポイントは「国の登録有形文化財の建築物をオーベルジュとして活用」。",
    "ここで建物の正体を確かめてみると、いさりの母体は、網元として栄えた戸田家が大正期に建てた<strong>旧戸田家住宅</strong>でした。",
    "旧戸田家住宅は2016年に国の登録有形文化財になった建物で、日本遺産「百世の安堵」の構成文化財にもなっています。",
]))

b.append(h3("戸田棟101号室とペットと泊まれる204号室"))
b.append(p([
    "最初に案内されたのは、画面に<strong>「戸田棟101号室」</strong>と出た客室。",
    "長い縁側の奥に畳の大座敷が広がり、ベッドと座椅子が置かれています。2人は「これ映画とかでよく見る」と大はしゃぎでした。",
]))
b.append(IMG["r101"])
b.append(p([
    "公式サイトによると、101号室は定員6名・83.22㎡の広い座敷の部屋で、特製の五右衛門風呂がついています。",
    "戸田棟にはフロントとレストランがあり、ほかに蔵を改修したヒノキ風呂の部屋(103・104号室)などもあります。",
]))
b.append(IMG["rooms"])
b.append(p([
    "さらにナレーションでは、今年8月に家族連れや長く泊まりたい人向けの別館もオープンしたと紹介。",
    "そこにあるのが、<strong>ペットと一緒に泊まれる特別な客室</strong>です。",
]))
b.append(IMG["r204"])
b.append(p([
    "扉の表札は「二〇四」。",
    "中に入ると、木の塀に囲まれた芝生の庭がまるごとドッグランになっていて、2人は「めっちゃ広いね」「ドッグランつきだ」と声を上げ、吉澤は自分が芝生を走り回っていました。",
]))
b.append(IMG["dogrun"])
b.append(p([
    "この204号室は、いさりのもうひとつの建物<strong>「久徳棟」</strong>の部屋。",
    "公式サイトでは、蔵を改修した吹き抜けの離れで、定員4名・85.33㎡、<strong>専用ドッグラン付き</strong>と書かれています。表札の番号と庭のつくりが、放送とぴったり一致していました。",
]))
b.append(IMG["dog"])
b.append(p([
    "そのあと出てきたワンちゃんを吉澤が抱っこして、メロメロになる場面も。",
    "最後には松田と2人で「WOW」「JUST」と、犬と一緒にポーズを決めていました。",
]))
b.append(IMG["sabaku"])

b.append(h3("ごほうびはタマクエとハマチのカルパッチョ"))
b.append(p([
    "ここからは、<a href=\"" + POST13 + "\">前回#13</a>の海上釣り対決で勝った吉澤への<strong>ごほうびタイム</strong>。",
    "厨房では、吉澤が釣ったタマクエとハマチをシェフがさばいていきます。",
]))
b.append(p([
    "出てきたのは<strong>「タマクエのカルパッチョ」</strong>と<strong>「ハマチのカルパッチョ」</strong>。",
    "吉澤はタマクエを一口食べて「うまい!」。テロップは「いやいつもの5倍は美味い!」で、ハマチも「脂がちゃんとのってる」と大満足でした。",
]))
b.append(IMG["tamakue"])
b.append(IMG["umai"])
b.append(IMG["hamachi"])
b.append(p([
    "負けた松田は、となりで見ているだけ。",
    "「俺、海鮮が一番好きな人間」と、本気でうらやましそうでした。",
]))

b.append(h3("いさりの絶品コース料理と「あ〜ん」の行方"))
b.append(p([
    "さらにテーブルには、いさりの<strong>絶品コース料理</strong>がずらり。",
    "画面に名前が出ていたのは<strong>「太刀魚と鶏のジュレ」</strong>と<strong>「熊野牛と山椒のソース」</strong>、デザートの<strong>「爽涼みかんのソルベ/紀州百花蜜」</strong>です。",
]))
b.append(IMG["course"])
b.append(IMG["tachiuo"])
b.append(IMG["kumanogyu"])
b.append(p([
    "番組の説明文にもあった「松田くんは吉澤くんからの『あ〜ん♡』の誘惑に打ち勝てるのか!?」という場面は、熊野牛のときに。",
    "吉澤がフォークを差し出すと、松田は迷うことなくパクリ。テロップは<strong>「普通にあ〜ん」</strong>で、誘惑にはまったく勝てていませんでした。",
]))
b.append(IMG["ahn"])
b.append(p([
    "続けて吉澤が「いなむーにも食べさせてあげたい」と言い出すと、現れたのは前回と同じ<strong>「いなむー(人型モード)」</strong>。",
    "お面のすき間からお肉を食べさせてもらっていましたが、正体はスタッフさんだったようで、松田からは鋭いツッコミが入っていました。",
]))
b.append(IMG["inamu"])
b.append(IMG["sorbet"])
b.append(p([
    "最後は英語PR「全世界80億人に届け!シン日本遺産」で、松田が「広川町を代表するくつろぎ空間を満喫しよう!」とアピールしました。",
]))
b.append(IMG["pr"])
b.append(infobox("いさり(ホテル)/潮香(レストラン)の基本情報", [
    ("住所", "和歌山県有田郡広川町広1347"),
    ("アクセス", "稲むらの火の館から徒歩約3分。道案内は公式サイトにPDFあり"),
    ("建物", "国の登録有形文化財「旧戸田家住宅」(戸田棟)と、旧久徳家の邸宅(久徳棟)を改修"),
    ("客室", "戸田棟4室(101〜104)・久徳棟5室(201〜205)。204号室は専用ドッグラン付き"),
    ("チェックイン/アウト", "15:00(最終18:00)/10:00"),
    ("レストラン潮香", "ランチコース5,500円(全5皿)・ディナーコース13,000円(全8皿)。完全予約制"),
    ("レストラン定休日", "火曜・水曜(ランチは金曜も休み)"),
    ("駐車場", "あり(無料)"),
    ("電話", "0737-63-1920"),
]))
b.append(p([
    "レストランは2営業日前まで、ホテルは1週間前までの予約が必要です。",
    "宿泊しなくても潮香のランチコースは食べられるので、日帰りの聖地巡礼でも番組の雰囲気を味わえます。",
]))
b.append(gmap("ホテルいさり 和歌山県有田郡広川町広1347"))

# --- 西広海岸
b.append(h2("最後のシン日本遺産は「和歌山のウユニ塩湖」西広海岸"))
b.append(minibox([
    ("ロケ地", "西広海岸(和歌山県有田郡広川町西広)"),
    ("場面", "鏡面世界で映え写真/フラットスキムボードで「JUS動画」撮影"),
]))
b.append(p([
    "広川町のみなさんに温かく出迎えられたあと、しずげんはいなむーと一緒に海へ。",
    "広川町ラストのJUSTは<strong>「“映え”過ぎ注意!自然が作り出す奇跡の絶景」</strong>です。",
]))
b.append(IMG["demukae"])
b.append(IMG["mission2"])
b.append(IMG["nishihiro"])
b.append(p([
    "上空からの映像には、はっきり<strong>「西広海岸」</strong>のテロップ。",
    "遠浅の砂浜に潮だまりがいくつも残り、沖には小さな島が浮かんでいます。松の木の間を抜けて砂浜に出る遊歩道も、西広海岸の入口そのものでした。",
]))
b.append(IMG["uyuni"])
b.append(p([
    "シン・日本遺産ポイントは「『和歌山のウユニ塩湖』と称される映えスポット」。",
    "西広海岸は、潮が引いたあとの浅い水面に空が映りこむ写真がSNSで話題になり、「広川のウユニ塩湖」とも呼ばれています。",
]))

b.append(h3("matsuさんと撮った鏡面写真"))
b.append(p([
    "案内役は、この海岸で鏡面写真を撮っているカメラマンの<strong>matsuさん</strong>。",
    "スタッフが「matsuさんが撮影した写真見てみます?」と見せてくれたのは、空と雲が上下にぴったり映りこんだ写真や、夕焼けの中に人のシルエットが映る写真でした。",
]))
b.append(IMG["matsu_photo"])
b.append(p([
    "番組が今SNSをがんばっていると聞いた吉澤は「俺フォローしてるよね」。すかさずテロップで「絶対しないやつだ」とつっこまれていました。",
]))
b.append(IMG["beach"])
b.append(p([
    "ただ、この日の浜は風があって水面がざわざわ。",
    "「今日はちょっと無理っぽいです」「波がちょっとでも立つとダメ」と難しそうな空気が流れ、matsuさんは場所を変えながら水面を探していきます。",
]))
b.append(IMG["satsuei"])
b.append(p([
    "それでも、水がたまっている場所を見つけて撮ってみると、2人の姿がしっかり水面に映りました。",
    "完成したのは、2人で手を合わせた<strong>「げんた×しずや【フュージョンポーズ】」</strong>。",
]))
b.append(IMG["fusion"])
b.append(p([
    "ひとりずつのショットは、松田の<strong>【爽やかTJポーズ】</strong>と、吉澤の<strong>【カーニバルポーズ】</strong>。",
]))
b.append(IMG["genta_pose"])
b.append(IMG["shizuya_pose"])
b.append(p([
    "最後は、2人の手のひらの上に、奥に立つ上野Pが乗っているように見える<strong>【手に乗る白ピクミン】</strong>。",
    "前回#13で白いパーカーのスタッフについた「白ピクミン」のあだ名が、ここで回収されました。",
]))
b.append(IMG["pikmin"])

b.append(h3("フラットスキムボードで「JUS動画」に挑戦"))
b.append(p([
    "続いては「映え動画」の撮影。",
    "教えてくれたのは、<strong>dbjapan local riderの岡俊樹さん</strong>です。",
]))
b.append(IMG["oka"])
b.append(p([
    "挑戦したのは、SNSでも話題の<strong>フラットスキムボード</strong>。",
    "ボードを浅い水面に投げて、走って飛び乗り、そのまま水の上をすべるアクティビティです。岡さんのお手本を見た吉澤は「見ただけでできるってわかる!」と自信満々でした。",
]))
b.append(IMG["skim"])
b.append(IMG["norikata"])
b.append(p([
    "ところが、テロップいわく「乗るだけでも至難の業!?」。",
    "「重心は低めで」と教わっても、ボードだけがすべっていったり、しりもちをついたりと、2人ともなかなか乗れません。",
]))
b.append(p([
    "練習をくり返して、いよいよ<strong>「JUS動画撮影 本番」</strong>。",
    "先に決めたのは松田で、ボードに飛び乗ってきれいに水面をすべり、思わず「JUST!」。",
]))
b.append(IMG["genta_ok"])
b.append(IMG["genta_just"])
b.append(p([
    "黄色いタオルを頭に巻いた“ラーメン店主しずや”も、本番でしっかりボードに乗ってすべりきりました。",
    "最後に松田が「『Travis Japan』本番強いよね」と言っていたとおり、2人とも本番で成功しています。",
]))
b.append(IMG["shizuya_ok"])
b.append(IMG["aerial"])
b.append(p([
    "英語PRでは、上空から見た西広海岸に「空が水面に反射して生まれる奇跡の絶景!(A magical view where the sky reflects on the water!)」の字幕。",
    "これで広川町の4つのJUSTはすべてクリアとなりました。",
]))
b.append(IMG["pr2"])
b.append(IMG["pr2en"])
b.append(infobox("西広海岸の基本情報", [
    ("住所", "和歌山県有田郡広川町西広"),
    ("アクセス", "JR紀勢本線 広川ビーチ駅から徒歩約15分/湯浅御坊道路 広川ICから約4km"),
    ("駐車場", "周辺の有料駐車場を利用"),
    ("設備", "トイレ・シャワー・コインロッカーのある施設あり"),
    ("特徴", "遠浅の砂浜。西向きで夕景が美しく、和歌山県の「朝日・夕陽100選」にも選ばれている"),
    ("問い合わせ", "広川町 地域振興課 0737-23-7764"),
]))
b.append(p([
    "鏡面写真が撮れるのは、<strong>干潮で水が薄く残っていて、風のない時間</strong>。",
    "番組でも風のせいで苦戦していたように、条件がそろう日は限られます。行く前に潮見表で干潮の時刻を調べ、風の弱い朝か夕方を狙うのがおすすめです。",
    "沖に出すぎると離岸流もあるので、波打ち際で遊ぶようにしましょう。",
]))
b.append(gmap("西広海岸 和歌山県有田郡広川町西広"))

# --- 聖地巡礼
b.append(h2("広川町で聖地巡礼するときのポイント"))
b.append(p([
    "<strong>いさり</strong>は稲むらの火の館から歩いて約3分。<a href=\"" + POST12 + "\">#12</a>で吉澤が歩いた広村堤防や稲むらの火の館とあわせて回れます。",
    "<strong>西広海岸</strong>はJR広川ビーチ駅から歩いて約15分で、駅前には<a href=\"" + POST13 + "\">#13</a>のカレーうどんが食べられる広川町立ふれあい館もあります。",
    "鏡面写真を狙うなら夕方の干潮に合わせて海岸へ行き、そのままいさりに泊まる流れにすると、しずげんの#14をまるごとたどれます。ペット連れなら204号室を早めに予約しておきましょう。",
]))

# --- 次回
b.append(h2("次回#15は初コンビの宮崎編"))
b.append(p([
    "広川町編はこれで完結。",
    "予告では<strong>「初コンビ!宮崎のシン日本遺産!」</strong>のテロップとともに、サンタ風の衣装のメンバーや、渓谷の水に入る姿が映っていました。",
    "どのメンバーの組み合わせなのかも、次回の楽しみです。",
]))
b.append(IMG["yokoku"])
b.append(IMG["thanks"])

# --- まとめ
b.append(h2("まとめ"))
b.append(checklist([
    "3つ目のシン日本遺産は、国の登録有形文化財を活かした古民家オーベルジュ「いさり」",
    "客室は戸田棟101号室と、専用ドッグラン付きの久徳棟204号室を紹介",
    "ごほうびはタマクエ・ハマチのカルパッチョと、熊野牛などのコース料理。松田元太は「普通にあ〜ん」",
    "最後のシン日本遺産は「和歌山のウユニ塩湖」と呼ばれる西広海岸",
    "鏡面写真4枚を撮影し、フラットスキムボードの「JUS動画」は2人とも本番で成功",
]))
b.append(p([
    "釣り対決のごほうびから鏡面写真まで、しずげんの仲の良さがたっぷり見られた広川町編の最終回でした。",
    "いさりは文化財の建物に泊まれる宿、西広海岸は条件がそろえば空が映る海岸です。番組を見て気になった方は、夕方の干潮に合わせて広川町を訪ねてみてはいかがでしょうか!",
]))
b.append(linkbox("あわせて読みたい", [
    f'<a href="{POST13}" target="_blank" rel="noopener">【Travis Japan】シン日本遺産の広川町ロケはどこ？(#13)</a>',
    f'<a href="{POST12}" target="_blank" rel="noopener">【シン日本遺産】吉澤閑也の広川町ロケはどこ？無人島サバイバルの結果も(#12)</a>',
    f'<a href="{POST_GOODS}" target="_blank" rel="noopener">【シン日本遺産】トラジャス公式グッズの予約はいつまで？値段や届く日も！</a>',
]))

content = "\n\n".join(b)
# 文中の「。」の後ろにも<br>(docs/rules.md 文体ルール)。段落ブロックの中だけ、カギカッコ内は除く
def _br(m):
    out, depth = [], 0
    s = m.group(0)
    for i, ch in enumerate(s):
        out.append(ch)
        depth += ch == "「"
        depth -= ch == "」"
        if ch == "。" and depth <= 0 and i + 1 < len(s) and s[i + 1] not in "<」）)":
            out.append("<br>\n")
    return "".join(out)
content = re.sub(r"<p>.*?</p>", _br, content, flags=re.S)

ART = ROOT / "articles" / "shizugen_shinnihonisan14_hirogawa.html"
ART.write_text(content, encoding="utf-8")
# 人名に「さん」(blog-upload STEP1.55)
OTHERS = "丹保直也,岡俊樹,小櫃裕太郎"
subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis", "--names", OTHERS, str(ART)], check=True)
chk = subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "check", "--group", "travis", "--names", OTHERS, str(ART)],
                     capture_output=True, text=True, encoding="utf-8", errors="replace")
print(chk.stdout[-500:], chk.stderr[-300:])
content = ART.read_text(encoding="utf-8")
print("CHARS", len(re.sub(r"<!--.*?-->|<[^>]+>|\s", "", content, flags=re.S)))
if DRY:
    sys.exit()

eye = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
     "--main", "しずげん",
     "--bottom", "【シン日本遺産】広川町ロケはどこ？", "--bottom", "いさり・西広海岸！",
     "--color-key", "吉澤閑也+松田元太", "--out", str(EYECATCH)],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
)
print(eye.stdout[-300:], eye.stderr[-300:])
eye.check_returncode()
em = upload_media(EYECATCH, EYECATCH.name, "image/jpeg")
print("eyecatch", em["id"])

payload = {"title": title, "content": content, "status": "draft",
           "slug": "shinnihonisan-14-hirogawa-shizugen-location",
           "categories": [3, 12, 7], "author": 2, "featured_media": em["id"]}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"], post["status"])
print("PREVIEW", f"{WP_URL}/?p={post['id']}")
(WORK / "postid.txt").write_text(str(post["id"]))
