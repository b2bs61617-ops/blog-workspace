# -*- coding: utf-8 -*-
# JUST!シン日本遺産 #15(宮崎県編1・川島如恵留+七五三掛龍也、2026-11-11放送)ロケ地記事 -> chomoand-4.blog 下書き
# 使い方: python build_and_post_noeshime_shinnihonisan15_miyazaki.py [--dry]
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

# 2人回(川島=白・七五三掛=ピンク)なのでグループ色の紫で統一(#13・#14と同じ)
BORDER = "#d9cdf0"
ACCENT = "#7e57c2"
BG = "#f5f2fb"

exec((ROOT / "tmp_shinnihon10" / "_helpers.py").read_text(encoding="utf-8"))

WORK = ROOT / "tmp_shinnihon15"
EYECATCH = ROOT / "images" / "noeshime_shinnihon15_eyecatch.jpg"


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


title = "【未】【シン日本遺産#15】宮崎ロケ地はどこ？加江田渓谷とひょっとこ踊り！"
TVER_SRC = "https://tver.jp/episodes/ep9zqdpk5l"
POST14 = f"{WP_URL}/shinnihonisan-14-hirogawa-shizugen-location-2261"
POST13 = f"{WP_URL}/?p=1848"
POST_STAGE = f"{WP_URL}/toraja-musical-voice-actor-car-903"

img_defs = [
    ("op_beach", "オープニングの舞台になった宮崎の海岸"),
    ("op_two", "海を背にした川島如恵留と七五三掛龍也"),
    ("dasei", "主演舞台で宮崎弁の役を演じた川島如恵留"),
    ("aerial", "上空から見た宮崎市の海岸線"),
    ("map", "宮崎県の4つのJUSTの地図"),
    ("toutei", "ヤシが並ぶ突堤の上でスタートしたのえしめ"),
    ("kominkan", "ひょっとこ踊りの舞台「新別府町公民館」"),
    ("hall", "公民館の広いホール"),
    ("dancers", "ひょっとこ踊りで出迎えてくれた踊り手さんたち"),
    ("seiyama", "やろかい清和の清山和一さん"),
    ("hyuga", "日向市が発祥のひょっとこ踊り"),
    ("group", "ひょっとこ踊り団体「やろかい清和」のみなさん"),
    ("men", "ひょっとこのお面。「火男」が語源とされる"),
    ("kihon", "ひょっとこ踊りの基本動作を教わる2人"),
    ("mj", "「令和のマイケルジャクソン」と呼ばれた清山和一さんの踊り"),
    ("taiketsu", "罰ゲームをかけたひょっとこ踊り対決"),
    ("battle", "個性で勝負するひょっとこ踊り対決"),
    ("judge", "対決後の川島如恵留"),
    ("nama", "罰ゲームはお面なしの「生ひょっとこ」"),
    ("nama2", "生ひょっとこ動画の撮影"),
    ("hyoeru", "「僕がひょえるです」"),
    ("road", "次の目的地へ向かうのえしめ"),
    ("guide", "まる宮キャニオニングの宮崎匠さん"),
    ("kaeda", "国の天然記念物として紹介された加江田渓谷"),
    ("wetsuit", "ウェットスーツとヘルメットに着替えた2人"),
    ("mizunare", "まずは川で水に慣れる"),
    ("jumpstart", "上流の岩場から「まさかのジャンプスタート」"),
    ("noel_jump", "岩場から飛び込む川島如恵留"),
    ("noel_after", "飛び込んで笑顔の川島如恵留"),
    ("high", "高さ3.5mの飛び込みに挑戦"),
    ("shime_jump", "3.5mの岩場から飛び込む"),
    ("shime_after", "飛び込んだ七五三掛龍也「めっちゃ怖かった…」"),
    ("curtain", "滝の裏側は「滝のカーテン」"),
    ("taki", "滝に打たれる川島如恵留「めっちゃ気持ちいい!」"),
    ("madam", "滝に打たれる七五三掛龍也"),
    ("letter", "「拝啓、宮崎県のご担当者様」"),
    ("enjoy", "「みんなにも来てほしいぐらい気持ちいい」"),
    ("private", "プライベート旅のような爽やかキャニオニング"),
    ("pr", "英語PR「Miyazaki is more than just the ocean!」"),
    ("pr_aerial", "上空から見た加江田渓谷"),
]

IMG = {}
for key, alt in img_defs:
    fn = f"noeshime_shinnihon15_{key}.jpg"
    if DRY:
        IMG[key] = image_block(f"images/{fn}", 1280, 720, "", alt, TVER_SRC)
        continue
    m = upload_media(ROOT / "images" / fn, fn, "image/jpeg")
    IMG[key] = image_block(*img_urls(m), alt, TVER_SRC)
    print(key, m["id"])

MARK = '<span class="swl-marker" style="font-weight:bold;font-size:1.15em;">'

b = []
b.append(p([
    "2026年11月11日放送の「Travis JapanノJUST!シン日本遺産」#15から、新しく宮崎県編が始まりました。",
    "川島如恵留と七五三掛龍也の“のえしめ”ペアが訪れたのは、" + MARK + "新別府町公民館</span>のひょっとこ踊りと、" + MARK + "加江田渓谷</span>のキャニオニングです。",
    "オープニングの海岸もふくめて、放送の流れにそってロケ地をまとめます。",
]))
b.append(infobox("番組情報", [
    ("番組タイトル", "Travis JapanノJUST!シン日本遺産 宮崎県に4つのJUST!(#15)"),
    ("放送日", "2026年11月11日(水)深夜"),
    ("放送局・配信", "ABCテレビ、TVerで見逃し配信。スタジオ企画を加えた特別版はTELASAで配信"),
    ("出演", "川島如恵留・七五三掛龍也(Travis Japan)"),
    ("ナレーター", "小櫃裕太郎(ABCテレビアナウンサー)"),
    ("主なロケ地", "サンビーチ一ツ葉(とみられる)/新別府町公民館/加江田渓谷"),
]))
b.append(whatbox([
    "#15の宮崎編で巡ったロケ地3か所",
    "ひょっとこ踊りを教わった公民館と、踊り対決の結果",
    "1つ目のシン日本遺産「加江田渓谷のキャニオニング」の中身",
    "キャニオニングのツアー会社・料金・集合場所",
    "次回以降に残っている3つのJUST",
]))
b.append(table(["場面", "ロケ地", "場所"], [
    ["オープニング", "サンビーチ一ツ葉(とみられる)", "宮崎市新別府町"],
    ["ひょっとこ踊り", "新別府町公民館", "宮崎市新別府町"],
    ["キャニオニング", "加江田渓谷", "宮崎市鏡洲"],
]))

# --- OP
b.append(h2("オープニングは宮崎市の海岸(サンビーチ一ツ葉とみられる)"))
b.append(minibox([
    ("ロケ地", "サンビーチ一ツ葉とみられる(宮崎県宮崎市新別府町前浜)"),
    ("場面", "宮崎県編のスタート。のえしめ初コンビのあいさつ"),
]))
b.append(p([
    "宮崎県編の始まりは、ヤシの木が並ぶ青い海の前でした。",
    "のえしめが2人だけでロケをするのは、これが初めて。テロップも「宮崎県でのえしめ初コンビ!」です。",
]))
b.append(IMG["op_beach"])
b.append(IMG["op_two"])
b.append(p([
    "川島は「宮崎来たかったんですよ 僕」とうれしそう。",
    "主演舞台『惰性クラブ』で宮崎弁を話す役を演じたそうです。",
    "「気付いたらネイティブみたいに」なっていたと話していました。",
]))
b.append(IMG["dasei"])
b.append(p([
    "その言葉どおり、川島は「てげうめぇもんいっぱいありますから」と宮崎弁を連発。",
    "「てげ」は宮崎弁で「とても」という意味です。ロケ中も、無意識に宮崎弁が出る場面が何度もありました。",
]))
b.append(IMG["aerial"])
b.append(p([
    "このオープニングの海岸は、宮崎市の<strong>サンビーチ一ツ葉</strong>とみられます。",
    "1つ目の理由は、2人が立っていたのが、ヤシの植え込みと石畳の道がある突堤だったことです。",
    "2つ目は、上空からの映像に一ツ葉の長い松林と、シーガイアの高いホテルらしき建物が映っていたこと。3つ目は、このあと向かう公民館と同じ新別府町にあることです。",
]))
b.append(IMG["toutei"])
b.append(p([
    "突堤の上で渡されたのは、宮崎県の4つのJUSTが書かれた地図。",
    "日向市のサバゲーフィールド、花火を見下ろす特等席、生産量全国3位の高級食材、そして渓谷アドベンチャーの4つです。",
]))
b.append(IMG["map"])
b.append(infobox("サンビーチ一ツ葉の基本情報", [
    ("住所", "宮崎県宮崎市新別府町前浜1400-16"),
    ("施設", "みやざき臨海公園の中の人工の砂浜。北ビーチと南ビーチがある"),
    ("設備", "トイレ・シャワー・緑地広場・バーベキュー広場"),
    ("入場料", "無料(駐車場あり)"),
]))
b.append(gmap("サンビーチ一ツ葉 宮崎県宮崎市新別府町前浜1400-16"))

# --- ひょっとこ
b.append(h2("ひょっとこ踊りの舞台は新別府町公民館"))
b.append(minibox([
    ("ロケ地", "新別府町公民館(宮崎県宮崎市新別府町)"),
    ("場面", "宮崎の伝統芸能・ひょっとこ踊りを体験。罰ゲームをかけた踊り対決"),
]))
b.append(p([
    "シン日本遺産に行く前に、まずは「宮崎の文化を体験!」。",
    "2人が入っていった建物の入口には、はっきりと<strong>「新別府町公民館」</strong>の文字がありました。",
]))
b.append(IMG["kominkan"])
b.append(IMG["hall"])
b.append(p([
    "広いホールに「むかしむかし 日向の国の永田村に」というナレーションが流れます。",
    "すると、お面をつけた踊り手さんたちが次々と登場。テロップで「無限ひょっとこ」とつっこまれ、2人は大笑いしていました。",
]))
b.append(IMG["dancers"])
b.append(p([
    "教えてくれたのは、ひょっとこ踊り団体<strong>「やろかい清和」</strong>のみなさんです。",
    "清山和一は、お面を頭にのせたまま「宮崎の伝統芸能」だと紹介してくれました。",
]))
b.append(IMG["seiyama"])
b.append(IMG["group"])

b.append(h3("ひょっとこ踊りは日向市生まれの伝統芸能"))
b.append(p([
    "画面の説明によると、ひょっとこ踊りは<strong>宮崎県北部の日向市が発祥</strong>。",
    "豊作や商売繁盛を願う踊りです。",
]))
b.append(IMG["hyuga"])
b.append(p([
    "日向市では毎年夏に「日向ひょっとこ夏祭り」が開かれています。",
    "2026年は第43回で、7月31日と8月1日に開かれました。約2,000人が踊る、宮崎を代表するお祭りです。",
]))
b.append(p([
    "ちなみに「ひょっとこ」の名前は、<strong>「火男」が語源</strong>という説があります(諸説あり)。",
    "かまどの火を吹くような、とがった口元のお面が特徴です。",
]))
b.append(IMG["men"])

b.append(h3("基本動作を教わって、まさかの踊り対決へ"))
b.append(p([
    "基本は「出した足と同じ方の手を前に伸ばし、反対の手は耳の横へ」。",
    "さらに「手を追うように見ながら首を動かす」のがコツだそうです。",
]))
b.append(IMG["kihon"])
b.append(p([
    "応用編では、清山和一が自由自在に踊る姿に、テロップで「令和のマイケルジャクソン」。",
    "「動きに個性を出すのが大切」と教わり、2人も赤いはっぴにお面姿で踊りました。",
]))
b.append(IMG["mj"])
b.append(p([
    "ここでスタッフから「負けた方は罰ゲーム」の一言。",
    "急きょ、<strong>罰ゲームをかけたひょっとこ踊り対決</strong>が始まりました。",
]))
b.append(IMG["taiketsu"])
b.append(IMG["battle"])
b.append(p([
    "お面で前が見えないなか、2人は「フリーダムひょっとこ対決」をくり広げます。",
    "判定の結果、負けたのは川島。罰ゲームは、お面なしで踊る<strong>「生ひょっとこ」</strong>の披露でした。",
]))
b.append(IMG["judge"])
b.append(IMG["nama"])
b.append(p([
    "七五三掛がスマホを構えて「生ひょっとこ動画」を撮影。",
    "川島はテンポの速い踊りを全力で見せました。最後はカメラに向かって「僕がひょえるです」と決めていました。",
]))
b.append(IMG["nama2"])
b.append(IMG["hyoeru"])
b.append(p([
    "新別府町公民館は、地域の人が使う公民館です。",
    "観光施設ではないので、外から見るだけにして、中には入らないようにしましょう。",
]))
b.append(gmap("新別府町公民館 宮崎県宮崎市新別府町"))

# --- 加江田渓谷
b.append(h2("1つ目のシン日本遺産は加江田渓谷のキャニオニング"))
b.append(minibox([
    ("ロケ地", "加江田渓谷(宮崎県宮崎市鏡洲)"),
    ("場面", "まる宮キャニオニングのガイドで、川を下るキャニオニングに挑戦"),
]))
b.append(p([
    "次の目的地は、地図にあった「海だけじゃない!宮崎県が激推しする渓谷アドベンチャー」。",
    "山あいの道を歩いて着いた先で、ガイドさんが待っていました。",
]))
b.append(IMG["road"])
b.append(p([
    "ガイドは<strong>まる宮キャニオニング</strong>の宮崎匠。",
    "出身を聞かれて「宮崎在住の宮崎です」と答え、2人を笑わせていました。",
]))
b.append(IMG["guide"])
b.append(p([
    "キャニオニングは、体ひとつで川を下るアウトドアの遊びです。",
    "宮崎は「海からと街からすごく近い所に本格的な山と川がある」のが強みだと教えてくれました。",
]))
b.append(IMG["kaeda"])
b.append(p([
    "舞台は、画面で<strong>「国の天然記念物 加江田渓谷」</strong>と紹介された渓谷です。",
    "地図では、宮崎空港の南西、青島の西に星マークがついていました。",
    "宮崎県の観光サイトでも、渓谷のある山の一帯が1969年に国の天然記念物になったと紹介されています。",
]))

b.append(h3("まる宮キャニオニングとわかる理由"))
b.append(p([
    "ツアー会社は、ガイドさんの名前の字幕に<strong>「まる宮キャニオニング」</strong>と出ていました。",
    "まる宮キャニオニングは、加江田渓谷の丸野駐車場に集まって出発するツアーを開いています。",
    "予約サイトのプラン名も「『宮崎=海』の印象がガラリと変わる」で、番組の「海だけじゃない!」とぴったり重なります。",
]))

b.append(h3("水に慣れたら、上流でジャンプスタート"))
b.append(p([
    "ウェットスーツとライフジャケット、ヘルメットに着替えたら、まずは浅い川で「水に慣れよう」。",
    "七五三掛は日よけのハットをヘルメットの下にかぶっていました。",
]))
b.append(IMG["wetsuit"])
b.append(IMG["mizunare"])
b.append(p([
    "上流へ向かうと、いよいよ本番。",
    "スタート地点は岩場の上で、テロップは<strong>「まさかのジャンプスタート」</strong>でした。",
]))
b.append(IMG["jumpstart"])
b.append(p([
    "スタッフからのミッションは「爽やかなキャニオニング動画」を撮ること。",
    "宮崎県のPRになるよう、自撮りで爽やかな映像をねらいます。",
]))
b.append(p([
    "先に飛んだ川島は、カメラを持ったままエメラルドグリーンの淵へジャンプ。",
    "水から顔を出すと、満面の笑みでした。",
]))
b.append(IMG["noel_jump"])
b.append(IMG["noel_after"])

b.append(h3("七五三掛は高さ3.5mの岩場にガチビビリ"))
b.append(p([
    "続いては<strong>高さ3.5mの飛び込み</strong>。",
    "スタッフに「バンジーより怖いですか?」と聞かれるほど、七五三掛はおびえていました。",
]))
b.append(IMG["high"])
b.append(IMG["shime_jump"])
b.append(p([
    "それでも勇気を出して飛び込み、なんとか成功。",
    "水の中から出た第一声は「めっちゃ怖かった…」でした。",
]))
b.append(IMG["shime_after"])

b.append(h3("滝のカーテンで「プライベート旅」風の動画に"))
b.append(p([
    "後半は、岩のすき間を流れる滝へ。",
    "滝の裏側に入ると、まるで<strong>「滝のカーテン」</strong>のような景色が広がります。",
]))
b.append(IMG["curtain"])
b.append(p([
    "川島は滝に打たれて「めっちゃ気持ちいい!」。",
    "七五三掛は水を浴びて、テロップで「豪雨にあったマダム?」とつっこまれていました。",
]))
b.append(IMG["taki"])
b.append(IMG["madam"])
b.append(p([
    "七五三掛の自撮りには「拝啓、宮崎県のご担当者様」というテロップ。",
    "「みんなにも来てほしいぐらい気持ちいい」と、手紙を読むようにPRしていました。",
]))
b.append(IMG["letter"])
b.append(IMG["enjoy"])
b.append(p([
    "川島は「しめとのあの宮崎旅行」「俺らのプライベート旅に密着してもらって」と話し、仲よし旅の動画風に。",
    "画面のタイトルも「のえしめの夏休み!? 爽やかキャニオニング」でした。",
]))
b.append(IMG["private"])
b.append(p([
    "最後の英語PRは川島の担当。",
    "「Miyazaki is more than just the ocean!(宮崎県の魅力は海だけじゃない!)」と、緑に囲まれた川をアピールしました。",
]))
b.append(IMG["pr"])
b.append(IMG["pr_aerial"])
b.append(infobox("まる宮キャニオニングの基本情報", [
    ("場所", "加江田渓谷(宮崎県宮崎市鏡洲)"),
    ("集合場所", "加江田渓谷 丸野駐車場(無料・約100台)"),
    ("料金", "大人6,000円〜(ライフジャケット・シューズ・ヘルメット込み)"),
    ("オプション", "ウェットスーツ1,500円、ツアー動画3,000円など"),
    ("所要時間", "集合から解散まで約3時間(体験は約2時間30分)"),
    ("開始時間", "9:00〜12:00/13:00〜16:00の2枠"),
    ("対象年齢", "6〜79歳(12歳未満は保護者の同伴が必要)"),
    ("予約", "予約サイト(アソビュー・じゃらんなど)から"),
]))
b.append(p([
    "料金や開催時期は年によって変わることがあります。予約サイトで最新の情報を確かめてください。",
    "水着かインナーを着て集合し、タオルや着替え、すね丈の靴下を持っていくと安心です。",
]))
b.append(infobox("加江田渓谷の基本情報", [
    ("住所", "宮崎県宮崎市鏡洲"),
    ("アクセス", "宮崎空港から車で約20分/JR日南線 木花駅から車で約10分"),
    ("駐車場", "丸野駐車場(無料)"),
    ("特徴", "約8〜10kmの清流ぞいに遊歩道がある渓谷。日本有数の照葉樹林が広がる"),
]))
b.append(gmap("加江田渓谷 丸野駐車場 宮崎県宮崎市鏡洲"))

# --- 聖地巡礼
b.append(h2("宮崎で聖地巡礼するときのポイント"))
b.append(p([
    "<strong>サンビーチ一ツ葉</strong>と<strong>新別府町公民館</strong>は、どちらも宮崎市の新別府町にあります。",
    "公民館は地域の施設なので、巡礼は海岸の突堤を中心にするのがおすすめです。",
]))
b.append(p([
    "<strong>加江田渓谷</strong>は宮崎空港から車で約20分。",
    "のえしめと同じキャニオニングを体験するなら、夏のシーズン中にまる宮キャニオニングを予約しましょう。",
    "遊歩道を歩くだけでも、2人が見た清流の景色を楽しめます。",
]))

# --- 次回
b.append(h2("次回は残り3つのJUSTへ"))
b.append(p([
    "宮崎県の4つのJUSTのうち、#15でクリアしたのは渓谷アドベンチャーの1つだけ。",
    "残りは、日向市のサバゲーフィールド、花火を見下ろす特等席、生産量全国3位の高級食材です。",
    "のえしめの「30代男子のイチャイチャ旅」がどう続くのか、次回も楽しみです。",
]))

# --- まとめ
b.append(h2("まとめ"))
b.append(checklist([
    "#15から宮崎県編がスタート。のえしめが初めて2人だけでロケ",
    "オープニングの海岸は、宮崎市のサンビーチ一ツ葉とみられる",
    "ひょっとこ踊りは新別府町公民館で「やろかい清和」のみなさんに教わった",
    "踊り対決は川島如恵留の負けで、罰ゲームは「生ひょっとこ」",
    "1つ目のシン日本遺産は、加江田渓谷のキャニオニング(まる宮キャニオニング)",
]))
b.append(p([
    "初コンビとは思えないほど息ぴったりで、ずっと笑っていたのえしめの宮崎旅でした。",
    "飛び込みにおびえながらも挑戦した七五三掛と、宮崎弁が止まらない川島の姿に、宮崎へ行きたくなったファンも多いはずです!",
]))
b.append(linkbox("あわせて読みたい", [
    f'<a href="{POST14}" target="_blank" rel="noopener">【シン日本遺産#14】広川町ロケ地はどこ？古民家いさりと西広海岸！</a>',
    f'<a href="{POST13}" target="_blank" rel="noopener">【Travis Japan】シン日本遺産の広川町ロケはどこ？(#13)</a>',
    f'<a href="{POST_STAGE}" target="_blank" rel="noopener">トラジャのミュージカル・声優経歴は？劇団四季やディズニーも！</a>',
]))

content = "\n\n".join(b)
# 文中の「。」の後ろにも<br>。段落ブロックの中だけ、カギカッコ内は除く
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

ART = ROOT / "articles" / "noeshime_shinnihonisan15_miyazaki.html"
ART.write_text(content, encoding="utf-8")
OTHERS = "清山和一,宮崎匠,小櫃裕太郎"
subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis", "--names", OTHERS, str(ART)], check=True)
chk = subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "check", "--group", "travis", "--names", OTHERS, str(ART)],
                     capture_output=True, text=True, encoding="utf-8", errors="replace")
print(chk.stdout[-500:], chk.stderr[-300:])
subprocess.run([sys.executable, str(ROOT / "tools" / "easy_read.py"), "fix", str(ART)])
er = subprocess.run([sys.executable, str(ROOT / "tools" / "easy_read.py"), "check", str(ART)],
                    capture_output=True, text=True, encoding="utf-8", errors="replace")
print("EASY_READ rc", er.returncode)
print(er.stdout[-3000:])
content = ART.read_text(encoding="utf-8")
print("CHARS", len(re.sub(r"<!--.*?-->|<[^>]+>|\s", "", content, flags=re.S)))
if DRY or er.returncode != 0:
    sys.exit()

eye = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
     "--main", "のえしめ",
     "--bottom", "【シン日本遺産】宮崎ロケはどこ？", "--bottom", "加江田渓谷・ひょっとこ踊り！",
     "--color-key", "川島如恵留+七五三掛龍也", "--out", str(EYECATCH)],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
)
print(eye.stdout[-300:], eye.stderr[-300:])
eye.check_returncode()
em = upload_media(EYECATCH, EYECATCH.name, "image/jpeg")
print("eyecatch", em["id"])

payload = {"title": title, "content": content, "status": "draft",
           "slug": "shinnihonisan-15-miyazaki-noeshime-location",
           "categories": [3, 11, 8], "author": 2, "featured_media": em["id"]}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"], post["status"])
print("PREVIEW", f"{WP_URL}/?p={post['id']}")
(WORK / "postid.txt").write_text(str(post["id"]))
