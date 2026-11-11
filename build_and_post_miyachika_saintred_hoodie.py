# -*- coding: utf-8 -*-
# 宮近海斗 TOKYO SPEAKEASY(2026/11/10 25時〜、戸塚祥太と)の赤パーカー=SAINT RED記事(chomoand-4.blog下書き、オシリ依頼 2026-11-11)
# usage: python build_and_post_miyachika_saintred_hoodie.py [--dry]
import sys, json, re
import requests
import _jb_fc_lib as L
from _jb_fc_lib import p, h2, h3, figure, minibox, whatbox, table, titlebox, linkbox, checklist, marker, a, inner, yt_embed, wphtml

sys.path.insert(0, str(L.ROOT / "tools"))
from honorific import add_san  # noqa: E402
import easy_read  # noqa: E402

M = L.load_media(L.ROOT / "_miyachika_saintred_media.json", [
    ("eyecatch", "miyachika_saintred_eyecatch.jpg"),
    ("radio", "miyachika_saintred_tokyofm.jpg"),
    ("zoom", "miyachika_saintred_patch_zoom.jpg"),
    ("story", "miyachika_saintred_ig_story.jpg"),
])

YT_ID = "o-M3bztA9gg"
YT = f"https://www.youtube.com/watch?v={YT_ID}"
YT_TITLE = "A.B.C-Z 戸塚祥太さんと、Travis Japan 宮近海斗さんの話を盗み聴き・・・"
CAP_YT = f'出典:{a(YT, "JFN Pods公式YouTube")}'
CAP_IG = f'出典:{a("https://www.instagram.com/travis_japan_official/", "Travis Japan公式Instagram(ストーリーズ)")}'
SR_IG = "https://www.instagram.com/liveforsaintred/"
SR_POST = "https://www.instagram.com/liveforsaintred/p/DDzsNQavyJT/"
SR_STORE = "https://saintred.store/"


def ig_embed(url, label):
    return wphtml(f'''<blockquote class="instagram-media" data-instgrm-permalink="{url}?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" style="background:#FFF;border:0;border-radius:3px;box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);margin:1px auto 16px;max-width:540px;min-width:326px;padding:0;width:99.375%;"><a href="{url}?utm_source=ig_embed&amp;utm_campaign=loading" target="_blank" rel="noopener">{label}</a></blockquote>
<script async src="https://www.instagram.com/embed.js"></script>''')


BASE_TITLE = "宮近海斗の赤パーカーはどこの？SAINT REDと判明！"
assert len(BASE_TITLE) <= 35, len(BASE_TITLE)
title = "【未】" + BASE_TITLE
b = []

b.append(p([
    "ラジオ番組『TOKYO SPEAKEASY』で、宮近海斗が着ていた赤いパーカーが気になった人も多いはずです。",
    f"胸のワッペンを調べたところ、{marker('アメリカのブランド「SAINT RED(セイントレッド)」のパーカー')}とみられます。",
    "公式ストアでの値段は350ドル(日本円で約5万円)でした。",
]))
b.append(whatbox([
    "宮近海斗の赤パーカーが映った場面",
    "SAINT REDと分かった理由(胸のワッペン)",
    "SAINT REDはどんなブランドか",
    "パーカーの値段と、今から買えるか",
    "戸塚祥太との放送で話していたこと",
]))

# ---- 場面 ----
b.append(h2("宮近海斗の赤パーカーが映ったのはどこ？"))
b.append(minibox([
    ("番組", "TOKYO FM『TOKYO SPEAKEASY』"),
    ("放送", "2026年11月10日(火)25時〜"),
    ("一緒に出た人", "A.B.C-Zの戸塚祥太"),
    ("映像", "JFN Pods公式YouTube(2026年11月10日公開)"),
]))
b.append(p([
    "赤いパーカーを着ていたのは、TOKYO FMのラジオ番組『TOKYO SPEAKEASY』の収録です。",
    "A.B.C-Zの戸塚祥太と2人で出演し、11月10日の25時から放送されました。",
]))
b.append(p([
    "番組の音声は、JFN Podsの公式YouTubeでも配信されています。",
    "動画のサムネイルには、2人が並んで座った写真が使われています。",
    "宮近海斗は白いキャップに、真っ赤なパーカーという姿でした。",
]))
b.append(figure(M["radio"], "TOKYO SPEAKEASYで戸塚祥太と並ぶ、赤いパーカーを着た宮近海斗", CAP_YT))
b.append(h3("Travis Japan公式のストーリーズにも"))
b.append(p([
    "放送の当日には、Travis Japanの公式Instagramのストーリーズにも、同じ服の写真が載りました。",
    "2人で「T」のポーズをとった1枚で、「戸塚くんとともにいい雰囲気の場所で語らせていただきました」と書かれていました。",
    "こちらの写真では、パーカーの胸のワッペンまで正面から見えます。",
]))
b.append(figure(M["story"], "Travis Japan公式Instagramのストーリーズで戸塚祥太とTポーズをする、赤いパーカー姿の宮近海斗", CAP_IG))

# ---- 根拠 ----
b.append(h2("赤パーカーはSAINT REDとみられる理由"))
b.append(p([
    f"決め手は、{marker('左胸についている四角いワッペン')}です。",
    "白地のワッペンの上の段に青で「SAINT」、下の段に赤で「RED」と書かれています。",
]))
b.append(figure(M["zoom"], "宮近海斗の赤いパーカーの胸についたSAINT REDのワッペン(拡大)", f"{CAP_YT}(拡大)"))
b.append(p([
    "このワッペンは、SAINT REDの公式Instagramにのっているパーカーのロゴと同じデザインです。",
    "青・白・赤の3色の組み合わせや、文字の並びも一致しています。",
]))
b.append(ig_embed(SR_POST, "SAINT RED(@liveforsaintred)さんのInstagram投稿"))
b.append(table(
    ["見るところ", "宮近海斗のパーカー", "SAINT RED"],
    [
        ["ワッペンの場所", "左胸", "左胸"],
        ["ワッペンの文字", "SAINT / RED の2段", "SAINT / RED の2段"],
        ["色の組み合わせ", "青・白・赤", "青・白・赤"],
    ],
))
b.append(p([
    "なお、宮近海斗本人やTravis Japanの公式から、ブランド名が発表されたわけではありません。",
    "この記事では、ワッペンのデザインが一致していることから「SAINT REDとみられる」としています。",
]))

# ---- ブランド ----
b.append(h2("SAINT REDはどんなブランド？"))
b.append(minibox([
    ("ブランド名", "SAINT RED(セイントレッド)"),
    ("国", "アメリカ"),
    ("公式Instagram", a(SR_IG, "@liveforsaintred")),
    ("看板アイテム", "SAINT RED EXPRESS HOOD(パーカー)"),
]))
b.append(p([
    "SAINT REDは、アメリカ生まれのファッションブランドです。",
    "日本ではまだほとんど知られていない、かなりレアなブランドといえます。",
]))
b.append(p([
    "看板アイテムが、今回のようなパーカー「EXPRESS HOOD」です。",
    "厚手の生地を1枚ずつ裁断して縫い、そのあと色を染めて、さらに洗いをかけてから仕上げているそうです。",
    "そのため、新品でも少し着こんだような、やわらかい風合いになっています。",
]))
b.append(h3("海外のアーティストやアスリートも着用"))
b.append(p([
    "SAINT REDの公式SNSでは、海外の有名人の着用写真が紹介されています。",
    "アメリカのラッパーのD Savageや、モトクロスの選手ヘイデン・ディーガンも、このパーカーを着ていました。",
    "日本のアイドルが着ているのは、かなり珍しいケースです。",
]))

# ---- 値段 ----
b.append(h2("SAINT REDのパーカーの値段は？今から買える？"))
b.append(table(
    ["項目", "内容"],
    [
        ["商品名", "SAINT RED EXPRESS HOOD"],
        ["値段", "350ドル(約5万円)"],
        ["素材", "コットン100%"],
        ["作り", "アメリカ製"],
        ["シルエット", "少し大きめで、丈は短め"],
    ],
))
b.append(p([
    "公式ストアでの値段は、350ドルでした。",
    "1ドル150円で計算すると、日本円で約52,500円です。",
    "送料と関税はこみの値段で、少し大きめ・丈は短めの作りと紹介されていました。",
]))
b.append(p([
    f"ただ、{marker('今は公式ストアでは買えない状態')}です。",
    "商品ページは「売り切れ」の表示で、2026年11月11日の時点ではストア自体も開けなくなっていました。",
    "日本の通販サイトやフリマアプリでも、11月11日の時点で同じパーカーは見つかりませんでした。",
]))
b.append(p([
    "どうしても似た雰囲気を楽しみたい人は、赤のパーカーに小さめのワッペンがついたものを選ぶと近づけます。",
    "新しい商品の情報は、SAINT REDの公式Instagramで発表されることが多いので、チェックしておくと安心です。",
]))
b.append(titlebox("公式情報", [
    a(SR_IG, "SAINT RED 公式Instagram(@liveforsaintred)"),
    a(SR_STORE, "SAINT RED 公式ストア(11月11日時点で閉店中)"),
]))

# ---- キャップ ----
b.append(h3("白いキャップはレンジャーズのロゴ"))
b.append(p([
    "パーカーと合わせていた白いキャップには、赤い「T」のロゴが入っていました。",
    "これはアメリカのメジャーリーグの球団、テキサス・レンジャーズのロゴです。",
    "赤いパーカーと赤いロゴで色をそろえた、まとまりのあるコーデでした。",
]))
b.append(p([
    "キャップのメーカーや型番までは、写真からは分かりませんでした。",
    f"宮近海斗のキャップ好きは有名で、{inner(2155, 'ROLLING CRADLEの鳥のキャップの記事')}でも紹介しています。",
]))

# ---- 放送内容 ----
b.append(h2("TOKYO SPEAKEASYで戸塚祥太と話したこと"))
b.append(p([
    "放送では、2人がジュニア時代の思い出をたっぷり話していました。",
    "宮近海斗とA.B.C-Zには、長いつながりがあります。",
]))
b.append(h3("宮近海斗の初めてのステージはA.B.C-Zのバック"))
b.append(p([
    "宮近海斗が事務所に入って初めて立ったステージは、2010年にNHKホールで行われたコンサートだったそうです。",
    "そこで踊るA.B.C-Zの姿を見て、「こんなに面白くて、アクロバットもできて踊れる人たちがいるんだ」と、いい意味でショックを受けたと話していました。",
]))
b.append(p([
    "その後もTravis Japanは、A.B.C-Zの舞台に何年もバックとして出演しています。",
    "宮近海斗は「メンバーと話しても、A.B.C-Zのあの時の、と言えば同じ景色が浮かぶ」と話していました。",
]))
b.append(h3("リーダーとしての役割やセリフの覚え方も"))
b.append(p([
    "戸塚祥太から「リーダーってどんなことをやるの？」と聞かれる場面もありました。",
    "宮近海斗は、グループを代表してコメントするのはリーダーの役目だと答えていました。",
    "7人でSNS用のコメントを撮るときも、まず自分が話してベースを作るそうです。",
]))
b.append(p([
    "セリフの覚え方については、台本を読んでいる自分の目線が頭の中に浮かぶタイプだと話していました。",
    "戸塚祥太は「チャカはすごい真面目」と、宮近海斗の姿勢をほめていました。",
]))
b.append(p([
    "ほかにも、コンビニのパスタの話や、最近見た映画の話など、ゆるいトークも楽しめる回でした。",
    "40分ほどの映像は、下のYouTubeから見られます。",
]))
b.append(yt_embed(YT_ID, YT_TITLE))

# ---- まとめ ----
b.append(h2("まとめ"))
b.append(checklist([
    "宮近海斗が『TOKYO SPEAKEASY』(2026年11月10日放送)で着ていたのは赤いパーカー",
    "胸の「SAINT / RED」のワッペンから、アメリカのブランドSAINT REDとみられる",
    "看板アイテムEXPRESS HOODの値段は350ドル(約5万円)",
    "11月11日の時点で、公式ストアは閉店中で買えない状態",
    "白いキャップはテキサス・レンジャーズの「T」ロゴ入り",
]))
b.append(p([
    "日本ではまだ知る人の少ないブランドを、さらっと着こなしていた宮近海斗でした。",
    "再販などの新しい情報が分かったら、この記事に追記します。",
]))
b.append(linkbox("あわせて読みたい", [
    inner(2155, "【ランキング】宮近海斗の鳥のキャップはどこの？ROLLING CRADLE！"),
    inner(1695, "宮近海斗の白Tシャツはどこの？ケルティのロゴTと判明！"),
    inner(1512, "【EGO】宮近海斗の指輪はどこの？TOM WOODとみられるゴールドリング！"),
    inner(1651, "宮近海斗のバッグのキーホルダーはどこの？ディズニーのフゥ タイガー！"),
    inner(1773, "宮近海斗の憧れの先輩は誰？井ノ原快彦と屋良朝幸！"),
]))

content = "\n\n".join(b)
content = add_san(content, "travis", ["戸塚祥太", "ヘイデン・ディーガン", "D Savage"])
content = easy_read.fix(content)
out = L.ROOT / "articles" / "miyachika_saintred_hoodie.html"
out.write_text(content, encoding="utf-8")
plain = re.sub(r"<[^>]+>", "", re.sub(r"<!--.*?-->", "", content))
print("chars:", len(re.sub(r"\s", "", plain)), "title_len:", len(BASE_TITLE))
if "--dry" in sys.argv:
    sys.exit()

payload = {"title": title, "content": content, "status": "draft",
           "slug": "miyachika-kaito-saint-red-hoodie", "categories": [3, 9], "author": 2,
           "featured_media": M["eyecatch"]["id"]}
r = requests.post(f"{L.WP_URL}/wp-json/wp/v2/posts", headers={**L.HEADERS_AUTH, "Content-Type": "application/json"},
                  data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
pid = r.json()["id"]
po = requests.get(f"{L.WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=L.HEADERS_AUTH).json()
print("POST_ID", pid, po["status"], po["author"], po["featured_media"], po["title"]["raw"],
      "content_ok", "SAINT RED" in po["content"]["raw"])
print(f"{L.WP_URL}/?p={pid}")
