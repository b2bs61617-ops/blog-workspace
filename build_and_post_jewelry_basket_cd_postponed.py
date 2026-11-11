# -*- coding: utf-8 -*-
# Travis Japan「Jewelry Basket」CD発売延期(2026/11/11発表)のまとめ記事(chomoand-4.blog下書き、オシリ依頼 2026-11-11)
# usage: python build_and_post_jewelry_basket_cd_postponed.py [--dry] [--update]
import sys, json, re
import requests
import _jb_fc_lib as L
from _jb_fc_lib import p, h2, h3, minibox, whatbox, table, titlebox, linkbox, checklist, marker, a, inner, wphtml

sys.path.insert(0, str(L.ROOT / "tools"))
from honorific import add_san  # noqa: E402
import easy_read  # noqa: E402

M = L.load_media(L.ROOT / "_jb_cd_postponed_media.json", [
    ("eyecatch", "jewelry_basket_cd_postponed_eyecatch_canva.jpg"),
])

UMJ = "https://www.universal-music.co.jp/travisjapan/news/2026-11-11/"
SUPPORT = "https://support.universal-music.co.jp/hc/ja"


def x_embed(user, sid):
    tw = f"https://twitter.com/{user}/status/{sid}"
    return wphtml('<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true">'
                  f'<a href="{tw}">{tw}</a></blockquote>\n'
                  '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


BASE_TITLE = "トラジャのアルバムCD延期はなぜ？発売記念イベントはどうなる？"
assert len(BASE_TITLE) <= 35, len(BASE_TITLE)
title = "【未】" + BASE_TITLE
b = []

b.append(p([
    "Travis Japanの4thアルバム『Jewelry Basket』のCDが、発売延期になりました。",
    f"新しい発売日は、{marker('2026年12月16日(水)')}です。",
    "理由は「商品の一部に不備が見つかったため」と発表されています。",
]))
b.append(p([
    f"ただし、{marker('配信は予定どおり11月18日(水)から')}スタートします。",
    "予約したCDも、そのまま有効です。",
]))
b.append(p([
    f"気になる発売記念イベントは、{marker('中止ではなく、予定どおり1月20日・27日に開催')}されます。",
    "変わるのは、応募期間と当選発表の日だけです。",
    "この記事では、公式発表の中身と、ファンが気になるポイントをまとめました。",
]))
b.append(whatbox([
    "CD発売延期の発表内容",
    "延期の理由はなぜ？",
    "発売記念イベントはどうなる？新しい応募期間",
    "イベント応募で気をつけたいこと",
    "新しい発売日と、変わらないこと",
    "予約はどうなる？キャンセルや再予約は必要？",
    "配信は11月18日から予定どおり",
]))

# ---- 発表 ----
b.append(h2("トラジャのアルバムCD延期の発表内容は？"))
b.append(minibox([
    ("発表日", "2026年11月11日(水)"),
    ("発表元", "ユニバーサル ミュージック・Travis Japan公式X"),
    ("対象", "4thアルバム『Jewelry Basket』のCD(全7形態)"),
    ("変更前の発売日", "2026年11月18日(水)"),
    ("新しい発売日", "2026年12月16日(水)"),
]))
b.append(p([
    "延期は、2026年11月11日の朝10時ごろに発表されました。",
    "Travis Japanの公式Xと、ユニバーサル ミュージックの公式サイトで、同時にお知らせが出ています。",
]))
b.append(x_embed("TravisJapan_cr", "2120320709373346236"))
b.append(p([
    "発売のちょうど1週間前の発表だったため、驚いたファンも多かったはずです。",
    "公式Xのプロフィール欄も、すでに「12.16 CD Release」に書きかえられています。",
]))

# ---- 理由 ----
b.append(h2("CD延期の理由はなぜ？「商品の一部に不備」"))
b.append(p([
    f"延期の理由は、{marker('商品の一部に不備が確認されたため')}と書かれています。",
    "どの形態の、どの部分に不備があったのかは、11月11日の時点で発表されていません。",
]))
b.append(p([
    "公式サイトでは「皆様に安心して商品をお受け取りいただけるよう、改めて商品の確認および対応を行った上でお届けいたします」と説明しています。",
    "つまり、問題がある状態のまま届けるのではなく、全部を見直してから発売するということです。",
]))
b.append(p([
    "メンバーの体調や、収録曲の問題といった理由ではありません。",
    "あくまで「商品(CDやパッケージ)」の問題なので、アルバムの中身の曲はそのまま楽しめます。",
]))
b.append(h3("メンバーやファンにとっては残念な1か月"))
b.append(p([
    "11月18日は、ファンが待ちに待ったアルバムの発売日でした。",
    "お店に並ぶCDを手に取れる日が、約1か月先にのびたことになります。",
    "一方で、不備のある商品が届くよりは、しっかり直してから届くほうが安心ともいえます。",
]))

# ---- イベント ----
b.append(h2("発売記念イベントはどうなる？中止ではなく予定どおり開催"))
b.append(p([
    f"CDに入っている応募券で申し込む発売記念イベントは、{marker('中止にはならず、日時も場所も変わりません')}。",
    "変わるのは、応募期間と当選発表の日の2つだけです。",
]))
b.append(table(
    ["項目", "変更前", "変更後"],
    [
        ["応募期間", "11月17日(火)〜11月29日(日)23:59", "12月15日(火)10:00〜12月20日(日)23:59"],
        ["当選発表", "12月23日(水)12:00", "2027年1月13日(水)12:00"],
        ["イベントの日時・場所", "-", "変更なし"],
    ],
))
b.append(h3("発売記念イベントの日程と内容"))
b.append(minibox([
    ("イベント名", "Travis Japan 'Jewelry Basket' 発売記念イベント"),
    ("大阪", "2027年1月20日(水)大阪府内(昼の部・夜の部)"),
    ("神奈川", "2027年1月27日(水)神奈川県内(昼の部・夜の部)"),
    ("内容", "スペシャルライブ・トーク・お見送り会"),
    ("当選人数", "合計 約7,000名"),
]))
b.append(p([
    "イベントは大阪と神奈川で、1日2回ずつの合計4回行われます。",
    "ライブとトークのあとには、メンバーが1人ひとりを見送る「お見送り会」もあります。",
    "くわしい会場や集合時間は、当選した人にだけ知らされます。",
]))
b.append(h3("応募の流れと、何口まで応募できるか"))
b.append(p([
    f"応募券は、{marker('全7形態のCDに1枚ずつ')}入っています。",
    "FC限定盤にも入っているので、どの形態を買っても応募できます。",
]))
b.append(checklist([
    "CDに入っている応募券の二次元コードを読み込む",
    "応募用のサイトでシリアルナンバーを受け取る",
    "行きたい日と部(昼・夜)を1つ選んで応募する",
]))
b.append(p([
    "応募券1枚で1口応募でき、何口でも応募できます。",
    "同じ部に何口も応募しても、口ごとにちがう会場や部を選んでもOKです。",
    "ただし、1人が複数のアカウントで応募すると、応募が無効になるので注意しましょう。",
]))
b.append(h3("応募期間は6日間に短くなるので注意"))
b.append(p([
    f"いちばん気をつけたいのは、{marker('応募できる期間が13日間から6日間に短くなる')}ことです。",
    "新しい期間は、12月15日(火)10時から12月20日(日)23時59分までです。",
]))
b.append(p([
    "応募の受付は、発売日の前日の12月15日から始まります。",
    "お店によっては、発売日の前日にCDを受け取れることがあるためとみられます。",
]))
b.append(p([
    "通販で予約した人は、CDが届く日をチェックしておきましょう。",
    "届くのが遅れると、締め切りの20日までに応募できないおそれがあります。",
    "確実に応募したい人は、お店で受け取る方法も考えておくと安心です。",
]))
b.append(h3("当選発表から大阪公演までは1週間"))
b.append(p([
    "当選発表は、2027年1月13日(水)の12時です。",
    f"大阪公演の1月20日までは{marker('ちょうど1週間')}しかありません。",
    "遠くから行く人は、当たる前から交通や宿の目安を調べておくと安心です。",
]))
b.append(p([
    "交通費や宿泊費は、自分で負担する決まりです。",
    "イベントが中止になった場合も、CDの返金や交通費の払い戻しはありません。",
]))
b.append(h3("当日は本人確認あり！席はランダム"))
b.append(p([
    "当日は、顔写真つきの身分証明書(原本)で本人確認があります。",
    "当選した本人しか入れず、家族や友だちが代わりに行くことはできません。",
]))
b.append(p([
    "会場には、立って見るエリアと座って見るエリアの2種類があります。",
    "どちらになるかは選べず、当選したときにランダムで決まります。",
    "応募券やシリアルナンバーは再発行できないので、CDが届いたら大事に保管しておきましょう。",
]))
b.append(titlebox("イベントの公式情報", [
    a("https://www.universal-music.co.jp/travisjapan/news/2026-10-28/", "「Jewelry Basket」発売記念イベント開催決定|ユニバーサル ミュージック"),
]))

# ---- 変わること・変わらないこと ----
b.append(h2("新しい発売日は12月16日！変わること・変わらないこと"))
b.append(table(
    ["項目", "変更前", "変更後"],
    [
        ["CD発売日", "11月18日(水)", "12月16日(水)"],
        ["配信", "11月18日(水)", "変更なし"],
        ["価格・品番", "-", "変更なし"],
        ["商品の内容", "-", "変更なし"],
        ["予約", "-", "そのまま有効"],
    ],
))
b.append(p([
    "公式の発表では、「価格、品番、商品内容に変更はございません」と書かれています。",
    "つまり、変わるのは発売日だけで、入っている曲や特典映像はそのままです。",
]))
b.append(h3("延期になる対象の商品(全7形態)"))
b.append(p([
    "延期になるのは、『Jewelry Basket』のCD全7形態です。",
    "FC限定盤も、お店で買える初回盤・通常盤も、すべて12月16日発売に変わります。",
]))
b.append(table(
    ["形態", "品番", "値段(税込)"],
    [
        ["初回T盤(CD+Blu-ray)", "UPCC-9026", "4,480円"],
        ["初回T盤(CD+DVD)", "UPCC-9027", "3,980円"],
        ["初回J盤(CD+Blu-ray)", "UPCC-9028", "4,480円"],
        ["初回J盤(CD+DVD)", "UPCC-9029", "3,980円"],
        ["通常盤 初回プレス(CDのみ)", "UPCC-9030", "3,300円"],
        ["FC限定盤(CD+Blu-ray)", "PROJ-1942", "5,480円"],
        ["FC限定盤(CD+DVD)", "PROJ-1943", "4,980円"],
    ],
))
b.append(p([
    "初回J盤の特典映像やすべての収録曲は、別の記事でくわしく紹介しています。",
    f"{inner(1543, '初回J盤の特典映像と全収録曲の記事')}もあわせて見てみてください。",
]))

# ---- 予約 ----
b.append(h2("予約はどうなる？キャンセルや再予約は必要？"))
b.append(p([
    f"すでに予約している人は、{marker('何もしなくて大丈夫')}です。",
    "公式サイトでは「ご予約はそのまま有効」「再予約のお手続きは必要ございません」と案内されています。",
]))
b.append(p([
    "予約したお店や通販サイトから、12月16日の発売に合わせて届く流れになります。",
    "ただ、お届けの日やお店での受け取り日の案内は、お店ごとに変わることがあります。",
    "心配な人は、予約したお店やサイトからのお知らせメールを確認しておくと安心です。",
]))
b.append(h3("FC限定盤やショップ特典はどうなる？"))
b.append(p([
    "FC限定盤も、ほかの形態と同じく12月16日発売に変わります。",
    "FC限定盤の申し込み方法は、" + inner(1724, "アルバムFC盤の購入方法の記事") + "でまとめています。",
]))
b.append(p([
    "お店ごとの特典(Jewelry Charmなど)について、11月11日の時点で変更の発表はありません。",
    "特典の配り方が変わる場合は、各お店から案内が出るはずです。",
    f"お店ごとの特典は、{inner(922, 'Jewelry Basketの特典を店舗別にまとめた記事')}で確認できます。",
]))
b.append(titlebox("問い合わせ先", [
    a(SUPPORT, "ユニバーサル ミュージック カスタマー・サービスセンター(平日10:00〜18:00)"),
]))
b.append(p([
    "問い合わせの返事は、メールで届くそうです。",
    "内容によっては、返事まで時間がかかる場合もあると案内されています。",
]))

# ---- 配信 ----
b.append(h2("配信(サブスク)は11月18日から予定どおり"))
b.append(p([
    f"うれしいことに、{marker('ダウンロード配信とサブスクは11月18日(水)から予定どおり')}始まります。",
    "CDより約1か月早く、アルバムの曲をすべて聴けることになります。",
]))
b.append(p([
    "さらに公式は「12月16日のCD発売までの間も、作品に触れていただく機会を設けるべく、準備を進めております」と発表しています。",
    "まだ中身は明かされていませんが、CDを待つ間に何か企画が用意されているようです。",
    "新しい情報が出たら、この記事に追記します。",
]))
b.append(p([
    "アルバムと同じ名前のツアー『Jewelry Basket』も、2027年に予定されています。",
    f"会場や日程は、{inner(1973, 'ツアー『Jewelry Basket』の会場・日程の記事')}にまとめています。",
]))

# ---- まとめ ----
b.append(h2("まとめ"))
b.append(checklist([
    "『Jewelry Basket』のCD発売日は、11月18日から12月16日(水)に延期",
    "理由は「商品の一部に不備が確認されたため」",
    "価格・品番・中身は変わらず、予約もそのまま有効(再予約は不要)",
    "配信・サブスクは11月18日(水)から予定どおりスタート",
    "発売記念イベントは中止ではなく、1月20日(大阪)・27日(神奈川)に予定どおり開催",
    "イベントの応募期間は12月15日〜20日の6日間、当選発表は2027年1月13日に変更",
]))
b.append(p([
    "CDを手に取れる日は少し先になりましたが、曲は11月18日から聴くことができます。",
    "CD発売までの「楽しめる機会」の発表も、楽しみに待ちたいですね。",
]))
b.append(titlebox("公式情報", [
    a(UMJ, "Travis Japan「Jewelry Basket」CD発売延期のお知らせ|ユニバーサル ミュージック"),
]))
b.append(linkbox("あわせて読みたい", [
    inner(922, "【Jewelry Basket】特典どこで買う？チャーム8色は店舗別！"),
    inner(1543, "【Jewelry Basket】初回J盤の特典映像は？全収録曲も公開！"),
    inner(1630, "【Jewelry Basket】FC限定盤ユニット曲の組合わせは？"),
    inner(958, "Jewelry Basketジャケ写に隠れた虎とバスケットボール？"),
    inner(1973, "トラジャ2027ツアー『Jewelry Basket』の会場・日程まとめ！"),
]))

content = "\n\n".join(b)
content = add_san(content, "travis", [])
content = easy_read.fix(content)
out = L.ROOT / "articles" / "jewelry_basket_cd_postponed.html"
out.write_text(content, encoding="utf-8")
plain = re.sub(r"<[^>]+>", "", re.sub(r"<!--.*?-->", "", content))
print("chars:", len(re.sub(r"\s", "", plain)), "title_len:", len(BASE_TITLE))
if "--dry" in sys.argv:
    sys.exit()
if "--update" in sys.argv:
    pid = int(sys.argv[sys.argv.index("--update") + 1])
    L.update_draft(pid, [content])
    po = requests.get(f"{L.WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=L.HEADERS_AUTH).json()
    print("verify", po["status"], "12月16日" in po["content"]["raw"])
    sys.exit()

payload = {"title": title, "content": content, "status": "draft",
           "slug": "travis-japan-jewelry-basket-cd-postponed", "categories": [3], "author": 2,
           "featured_media": M["eyecatch"]["id"]}
r = requests.post(f"{L.WP_URL}/wp-json/wp/v2/posts", headers={**L.HEADERS_AUTH, "Content-Type": "application/json"},
                  data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
pid = r.json()["id"]
po = requests.get(f"{L.WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=L.HEADERS_AUTH).json()
print("POST_ID", pid, po["status"], po["author"], po["featured_media"], po["title"]["raw"],
      "content_ok", "12月16日" in po["content"]["raw"])
print(f"{L.WP_URL}/?p={pid}")
