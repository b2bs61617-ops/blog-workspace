# -*- coding: utf-8 -*-
"""七五三掛KITCHEN(2026/11/06放送)オリジナルレシピ「背徳のサバみそ」記事を chomoand-4.blog に下書き投稿する.
再実行すると二重投稿になる. --dry で本文プレビューだけ作る."""
import json, re, subprocess, sys
import requests
from shimekake_kitchen_helpers import (ROOT, WP_URL, HEADERS_AUTH, upload_media, ACCENT, BORDER, BG,
                                       p, h2, h3, wphtml, whatbox, minibox, linkbox, checklist, xembed)

DRY = "--dry" in sys.argv
TITLE = "【未】【七五三掛KITCHEN】背徳のサバみそのレシピは？"
SLUG = "shimekake-kitchen-haitoku-saba-miso-recipe"
NONSTOP_X = "https://x.com/nonstop_fujitv/status/2118517626133749964"
NADIA_X = "https://x.com/NadiaRecipe/status/2118523872345723016"
ESSE_NABEMI_X = "https://x.com/ESSE_nabemi/status/2118177133709422784"
NADIA_SP = "https://oceans-nadia.com/special/nonstop-esse"
VLOG = "https://youtu.be/JFfV5YNVRy4"
PREVIEW = ROOT / "tmp_shimekake_kitchen_sabamiso_preview.html"


def table(header, rows):
    th = "".join(f"<th>{c}</th>" for c in header)
    trs = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout">'
            f'<thead><tr>{th}</tr></thead><tbody>\n{trs}\n</tbody></table></figure>\n<!-- /wp:table -->')


def infobox(title, rows):
    lines = "\n".join(f'<p style="margin:{"0" if i == 0 else "6px 0 0 0"};"><strong>{k}</strong>:{v}</p>'
                      for i, (k, v) in enumerate(rows))
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{title}</p>
<div style="padding:14px 18px;background:{BG};">
{lines}
</div>
</div>''')


def quotebox(lines):
    body = "<br>\n".join(lines)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#fff;">
<p style="margin:0;line-height:1.9;">{body}</p>
</div>''')


B = []
B.append(p([
    "2026年11月6日放送のフジテレビ系「ノンストップ！」の料理コーナー「めざせ！料理アイドル 七五三掛KITCHEN」で作られたのが、七五三掛龍也のオリジナルレシピ<strong>背徳のサバみそ</strong>です。",
    "中身は、王道のサバのみそ煮に、<strong>コチュジャン・バター・すりごまを混ぜるだけの「背徳ダレ」</strong>を添えたひと皿。",
    "途中でタレをつけて味変すると、甘じょっぱいみそ煮が一気に韓国風のコクのある味に変わり、スタジオでも「味変おいしい！」と大好評でした。",
    "この記事では、材料と作り方、サバをおいしく煮るコツ、放送前に七五三掛が話していたことや「今週のしめ何食べた」の宮崎グルメまでまとめます。",
]))
B.append(infobox("レシピ情報", [
    ("料理名", "背徳のサバみそ"),
    ("放送", "2026年11月6日(金)フジテレビ系「ノンストップ！」"),
    ("コーナー", "めざせ！料理アイドル 七五三掛KITCHEN"),
    ("レシピ", "七五三掛龍也のオリジナルレシピ"),
    ("分量・時間", "2人分・煮込み約7分"),
    ("使う道具", "フライパン・落としぶた"),
    ("掲載誌", "『ESSE』12月号(11月2日発売)"),
]))
B.append(whatbox([
    "背徳のサバみその材料(2人分)",
    "サバの下処理から盛りつけまで、5ステップの作り方",
    "「背徳ダレ」の中身と、味変のコツ",
    "放送前に七五三掛が話していたこと(煮魚への挑戦)",
    "「今週のしめ何食べた」吉澤閑也と宮崎で食べたもの",
]))

# ---- 放送回
B.append(h2("11月6日の七五三掛KITCHENはオリジナルレシピ「背徳のサバみそ」"))
B.append(minibox([
    ("放送日", "2026年11月6日(金)"),
    ("しめのイチオシ", "コチュジャン・バター・すりゴマを混ぜるだけの背徳ダレ"),
]))
B.append(p([
    "七五三掛KITCHENは、料理レシピサイト「Nadia」と雑誌『ESSE』と組んで、料理初心者の七五三掛が生放送で料理に挑戦するコーナーです。",
    "毎回Nadia Artistのレシピに挑戦する回と、七五三掛が自分で考えたオリジナルレシピの回があり、この日はオリジナル回でした。",
    "前回10月30日の放送で次回メニューが「背徳のサバみそ」と発表されたときは、ESSEの公式Xも「背徳とは？？」「映画タイトルのようなネーミング」とコメントしていて、ファンの間でも「何が背徳なの？」と話題になっていました。",
]))
B.append(p([
    "その答えが、番組公式Xが「しめのイチオシ」として紹介した<strong>コチュジャン、バター、すりゴマを混ぜるだけの背徳ダレ</strong>です。",
    "ヘルシーなイメージのサバのみそ煮に、あえてバターのコクとコチュジャンのピリ辛を足すことが「背徳」の正体でした。",
]))
B.append(xembed(NONSTOP_X))
B.append(p([
    "ESSEの担当編集さんも放送前日に「基本のサバみそをつくりながら、背徳感のある！？アレンジが効いてます」と投稿していました。",
    "まずは基本のサバのみそ煮をきちんと作り、そこにアレンジのタレを添える二段構えのレシピなので、サバのみそ煮を初めて作る人にもおすすめです。",
]))
B.append(xembed(ESSE_NABEMI_X))

# ---- 材料
B.append(h2("背徳のサバみその材料(2人分)"))
B.append(minibox([
    ("主役", "サバ2切れ(半身)・春菊100g"),
    ("背徳ダレ", "コチュジャン・バター・白すりごま"),
]))
B.append(p([
    "材料は、サバを煮る煮汁の【A】と、味変用の背徳ダレの【B】に分けて準備します。",
    "サバは切り身でも作れますが、レシピでは<strong>骨つきのサバがおすすめ</strong>とされています。骨からうまみが出て、煮汁の味がぐっと深くなります。",
    "付け合わせには、ねぎやしょうがではなく春菊を使うのがこのレシピの特徴です。春菊のほろ苦さと香りが、甘めのみそ煮とよく合います。",
]))
B.append(table(
    ["材料", "分量", "メモ"],
    [
        ["サバ", "2切れ(半身)", "骨つきがおすすめ"],
        ["春菊", "100g(約1/2束)", "4cm長さに切る"],
        ["【A】しょうが(薄切り)", "2〜3枚", "煮汁"],
        ["【A】みそ", "大さじ3", "煮汁"],
        ["【A】酒", "大さじ3", "煮汁"],
        ["【A】砂糖", "大さじ2", "煮汁"],
        ["【A】みりん", "大さじ1", "煮汁"],
        ["【A】水", "250ml", "煮汁"],
        ["【B】コチュジャン", "大さじ1/2", "背徳ダレ"],
        ["【B】バター", "20g", "背徳ダレ"],
        ["【B】白すりごま", "小さじ1", "背徳ダレ"],
    ],
))

# ---- 作り方
B.append(h2("背徳のサバみその作り方は5ステップ"))
B.append(minibox([
    ("流れ", "切り目を入れる→湯通しして氷水→煮汁で7分煮る→春菊を加える→背徳ダレを添える"),
    ("加熱の目安", "落としぶたをして強めの中火で7分"),
]))
B.append(p([
    "工程はシンプルですが、<strong>サバを湯通しして汚れを落とす下処理</strong>がおいしく仕上げるいちばんのポイントです。",
    "放送でも七五三掛が丁寧にサバを洗っていて、視聴者からは「サバの下処理もしめちゃんのように丁寧にやろう」「日頃の雑な工程を反省」といった声が上がっていました。",
]))
B.append(h3("工程1:サバに切り目を入れ、春菊を切る"))
B.append(p([
    "サバは皮目に切り目を入れます。切り目を入れておくと皮が縮んで破れにくくなり、煮汁の味も中までしみこみやすくなります。",
    "春菊は4cm長さのざく切りにしておきます。",
]))
B.append(h3("工程2:サバを熱湯にくぐらせ、氷水にとって洗う"))
B.append(p([
    "沸かした熱湯にサバを一瞬くぐらせ、すぐに氷水にとります。",
    "表面が白っぽくなったら、血合いやウロコなどの汚れを指でやさしく洗い流し、キッチンペーパーで水気をふき取ります。",
    "この「霜降り」と呼ばれる下処理をすると、サバ特有の生臭さがぐっと減ります。",
]))
B.append(h3("工程3:煮汁【A】が沸いたらサバを入れ、落としぶたで7分煮る"))
B.append(p([
    "フライパンに【A】のしょうが・みそ・酒・砂糖・みりん・水を入れて火にかけます。",
    "煮立ったらサバを皮目を上にして並べ、落としぶたをして<strong>強めの中火で7分</strong>煮ます。",
    "煮汁が沸いてからサバを入れるのは、表面をすぐに固めてうまみを閉じ込め、臭みも出にくくするためです。",
]))
B.append(h3("工程4:春菊を加えて盛りつけ、煮詰めた煮汁をかける"))
B.append(p([
    "落としぶたを外して春菊を加え、しんなりしたらサバと一緒に器に盛ります。",
    "フライパンに残った煮汁は、少しとろみがつくまで煮詰めてからサバにかけます。煮詰めることで味がぎゅっと濃縮され、ごはんが進む味になります。",
]))
B.append(h3("工程5:【B】を混ぜた背徳ダレを添える"))
B.append(p([
    "【B】のコチュジャン・バター・白すりごまを混ぜて、器に添えたら完成です。",
    "最初はそのままサバのみそ煮として食べ、途中から背徳ダレをつけて味を変えながら楽しみます。",
]))

# ---- 背徳ダレ
B.append(h2("「背徳ダレ」はコチュジャン×バター×すりごまで韓国風に味変"))
B.append(minibox([
    ("材料", "コチュジャン大さじ1/2・バター20g・白すりごま小さじ1"),
    ("味", "ピリ辛+バターのコク+ごまの香ばしさで韓国風"),
]))
B.append(p([
    "この料理のいちばんの見どころが、七五三掛がしめのイチオシとして紹介した「背徳ダレ」です。",
    "作り方は、コチュジャン・バター・すりごまを混ぜるだけ。番組公式Xも「韓国風の味わいに」と紹介しています。",
    "サバのみそ煮の甘じょっぱい煮汁に、コチュジャンの辛みと甘み、バターのまろやかなコク、すりごまの香ばしさが重なって、同じひと皿とは思えないほど味が変わります。",
]))
B.append(p([
    "バターは冷蔵庫から出したばかりだとかたくて混ざりにくいので、少し室温に置いてやわらかくしておくと、なめらかなタレになります。",
    "温かいサバの上にのせると、バターがじんわりとけてみそ煮の煮汁となじみます。",
    "視聴者からも「サバ味噌にバターとは革新的」「コチュジャンという時点でもう食べたい」「サバの味噌煮はよく作るからマンネリ防止にやってみたい」と反響がありました。",
]))
B.append(p([
    "放送では、試食したスタジオの出演者から「味変おいしい！」と大絶賛の声が上がり、CMに入ったあとも千秋がおいしそうに食べ続けていたそうです。",
    "設楽統も、春菊について「鍋に入れる」と話しながら、ベタ褒めで完食していました。",
    "ファンからは「“背徳”…どんだけ？！って思ったけど、マイルド背徳よね」という声もあり、名前ほど重たくなく、誰でも食べやすい味に仕上がっていたようです。",
]))
B.append(xembed(NADIA_X))

# ---- 放送前のコメント
B.append(h2("放送前に七五三掛が話していたこと"))
B.append(minibox([
    ("テーマ", "一人暮らしではなかなか挑戦できなかった煮魚"),
    ("今後", "いろんな魚料理に挑戦したい"),
]))
B.append(p([
    "番組公式Xに投稿された放送前のコメント動画で、七五三掛は今回のメニューについてこう話しています。",
]))
B.append(quotebox([
    "「今日は背徳のサバみそを作るんですけど、煮魚ってなかなかお家で、一人暮らしだとなかなか挑戦できなかったので、今回挑戦できて嬉しいなって思う」",
    "「今後もどんどんいろんな魚料理に挑戦したいなって思ってます。頑張ります！」",
]))
B.append(p([
    "これまでの七五三掛KITCHENのオリジナルレシピは、ステーキチャーハンや鮭のムニエル クリーミーソースなど、焼く・炒める料理が中心でした。",
    "煮汁の加減や下処理が必要な煮魚は、料理初心者にとってはハードルの高いジャンル。そこに自分から挑戦し、さらにアレンジまで考えてきたところに、料理アイドルとしての成長が感じられます。",
]))
B.append(h3("ハプニングなしで完走、エプロンは紺の花柄"))
B.append(p([
    "この日は、おなじみのペッパーミルのパフォーマンスはなく、煮る・混ぜるが中心の工程だったこともあり、大きなハプニングもなく最後まで完走。",
    "視聴者からは「危なっかしいところもなくて安心して最後まで見れた」「本当にお料理上手になったね」という声が多く、最後の「ありがとうございました」もどこか誇らしげな表情だったと話題になっていました。",
    "衣装はグレーと白のボーダーのヘンリーネックのトップスに、紺地に小花の刺しゅうが入ったエプロン。肩ひもと腰のリボンだけが淡いピンクになっていて、「ピンクが差し色でかわいい」と好評でした。",
]))

# ---- 今週のしめ何食べた
B.append(h2("今週のしめ何食べた？吉澤閑也と宮崎で鰻&ステーキ丼"))
B.append(minibox([
    ("今週のしめ何食べた", "吉澤閑也と宮崎で鰻&ステーキ丼・チキン南蛮"),
    ("宮崎に行った理由", "Jリーグ・テゲバジャーロ宮崎のホームゲームに来場"),
]))
B.append(p([
    "コーナー恒例の「今週のしめ何食べた」で七五三掛が紹介したのは、メンバーの吉澤閑也と一緒に訪れた宮崎で食べたグルメでした。",
    "コメント動画では、こう話しています。",
]))
B.append(quotebox([
    "「今週はメンバーのしずやと宮崎に行かせてもらったんですけど、お仕事で」",
    "「宮崎で、うなぎとステーキの混ざったやつ、丼があって、それをおいしくいただいたんですけど、すごくおいしくて」",
    "「宮崎、うなぎも有名と聞いたので、本当に食べてみたかったので嬉しかったです」",
    "「あと、チキン南蛮を食べたんですけど、チキン南蛮も本当においしくて、結構大量に食べましたね。最高でした」",
]))
B.append(p([
    "宮崎県は、うなぎの養殖が盛んな「うなぎどころ」として知られ、宮崎牛も全国的に有名です。",
    "その両方をいっぺんに味わえる鰻とステーキの丼に、宮崎発祥のご当地グルメとして知られるチキン南蛮まで、宮崎の名物をしっかり堪能してきたようです。",
]))
B.append(p([
    "2人が宮崎を訪れたのは、Jリーグの<strong>テゲバジャーロ宮崎のホームゲーム(栃木シティ戦)</strong>に来場するためでした。",
    "Travis JapanはJリーグ2026/27シーズンのスペシャルアンバサダーを務めていて、この日は七五三掛と吉澤が会場のいちご宮崎新富サッカー場を訪れ、試合前のピッチやスタンドを盛り上げたほか、キックインセレモニーやハーフタイムのイベントにも参加しました。",
    f'当日の様子をまとめた観戦vlogは<a href="{VLOG}" target="_blank" rel="noopener">YouTube</a>で公開されていて、2人による選手紹介やキックインの様子も見ることができます。',
]))

# ---- まとめ
B.append(h2("まとめ"))
B.append(checklist([
    "2026年11月6日の「ノンストップ！」七五三掛KITCHENのメニューは、七五三掛龍也のオリジナルレシピ<strong>背徳のサバみそ</strong>(『ESSE』12月号に掲載)",
    "材料はサバ2切れ・春菊100gと、しょうが・みそ・酒・砂糖・みりん・水の煮汁(2人分)",
    "作り方は「切り目を入れる→湯通しして氷水で洗う→煮汁で7分煮る→春菊を加えて盛る→背徳ダレを添える」の5ステップ",
    "「背徳」の正体は、<strong>コチュジャン・バター・すりごまを混ぜるだけの背徳ダレ</strong>。途中で韓国風に味変できる",
    "スタジオでは「味変おいしい！」と大好評、放送はハプニングなしで完走",
    "今週のしめ何食べたは、<strong>吉澤閑也と宮崎で食べた鰻&ステーキ丼とチキン南蛮</strong>",
]))
B.append(p([
    "基本のサバのみそ煮をしっかり作りつつ、タレひとつで味を変えられるので、いつものサバみそがマンネリになってきた人にもぴったりです。",
    "背徳ダレは混ぜるだけで作れるので、ぜひ試してみてください！",
    f'これまで七五三掛KITCHENで作ったレシピは、<a href="{NADIA_SP}" target="_blank" rel="noopener">Nadiaの特設ページ</a>でもチェックできます。',
]))
B.append(linkbox("あわせて読みたい", [
    '<a href="https://chomoand-4.blog/shimekake-kitchen-cheese-meatball-tomato-stew-recipe-2032" target="_blank" rel="noopener">【七五三掛KITCHEN】チーズミートボールのトマト煮込みのレシピは？</a>',
    '<a href="https://chomoand-4.blog/shimekake-kitchen-chicken-satsumaimo-mustard-mayo-recipe-1621" target="_blank" rel="noopener">【七五三掛KITCHEN】鶏肉とさつまいものマスタードマヨソースのレシピは？</a>',
    '<a href="https://chomoand-4.blog/shimekake-kitchen-steak-chahan-recipe-1389" target="_blank" rel="noopener">七五三掛のステーキチャーハンのレシピは？オリジナルの材料と作り方！</a>',
]))

content = "\n\n".join(B)
PREVIEW.write_text(content, encoding="utf-8")
# add honorifics (さん) to names in body text
subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis",
                "--names", "千秋,設楽統", str(PREVIEW)], check=True)
content = PREVIEW.read_text(encoding="utf-8").replace("七五三掛さんKITCHEN", "七五三掛KITCHEN")
PREVIEW.write_text(content, encoding="utf-8")
print("chars", len(re.sub(r"<[^>]+>", "", content)))
if DRY:
    sys.exit()

eye = upload_media(ROOT / "images" / "shimekake_kitchen_sabamiso_eyecatch_canva.jpg",
                   "shimekake_kitchen_sabamiso_eyecatch.jpg", "image/jpeg")
print("eyecatch media", eye["id"])
payload = {"title": TITLE, "slug": SLUG, "content": content, "status": "draft",
           "categories": [3, 8], "author": 2, "featured_media": eye["id"]}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts",
                  headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                  data=json.dumps(payload).encode("utf-8"), timeout=120)
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"], post["status"], post["slug"])
print("PREVIEW", f"{WP_URL}/?p={post['id']}&preview=true")
(ROOT / "tmp_shimekake_kitchen_sabamiso_postid.txt").write_text(str(post["id"]), encoding="utf-8")
