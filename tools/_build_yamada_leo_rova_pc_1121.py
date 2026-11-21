# -*- coding: utf-8 -*-
"""chomoand.com: 山田涼介(LEO)の木目調PC「RØVA」は売り切れ？値段と再販・ノートPC(2026-11-21 ユカ依頼)

根拠:
- 会見: WEBザテレビジョン https://thetv.jp/news/detail/1459702/ (2026/11/21 12:39)
- 会見の発言(ブラウン・ゲーム部屋・メンバーの反応): モデルプレス(Yahoo!転載) https://news.yahoo.co.jp/articles/60be23b18d2b1beca4a31c7872a03dae31c6c9ec
- 3モデルの値段・スペック・発表日: PC Watch https://pc.watch.impress.co.jp/docs/news/2145710.html (2026/10/5)
- 在庫: store.rova.jp の各商品 .js を 2026-11-21 に確認 → 6種とも available:false(売り切れ表示)、発送は「12月末から順次」
- 渋谷の広告: X @yamamichan_0509 (11/23〜29 東横渋谷スーパーボード)
- 写真: tools/Xiy/_yamada_rova_1121/rova_leo/images
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "trend"
KEY = "yamada_leo_rova_pc_1121"
TITLE = "山田涼介のPC「RØVA」は売り切れ？値段と再販・ノートPCは？"
SLUG = "yamada-ryosuke-leo-rova-pc-urikire-nedan"
CATEGORIES = [37]
NAMES = ["山田涼介", "髙野大知"]
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "山田涼介 LEO RØVA 木目調PC 売り切れ 値段"
X_TEXT = "山田涼介(LEO)の木目調PC「RØVA」、公式ストアを見たら6種ぜんぶ同じ表示に…😳\n今日の会見では木目調のノートPCも出ると発表！\nメンバーからは「いつの間にPCなんて作ってたんだよ」の声も"
X_TAGS = "#山田涼介 #LEO #RØVA"
MEDIA_JSON = blogkit.ARTICLES / (KEY + "_media.json")

THETV = "https://thetv.jp/news/detail/1459702/"
MDPR = "https://news.yahoo.co.jp/articles/60be23b18d2b1beca4a31c7872a03dae31c6c9ec"
PCW = "https://pc.watch.impress.co.jp/docs/news/2145710.html"
STORE = "https://store.rova.jp/collections/all"

PHOTOS = {
    "kaiken": ("山田涼介 LEO RØVA記者発表", "https://x.com/modelpress/status/2123985714954019196"),
    "pc": ("山田涼介 LEO 木目調PC RØVA", "https://x.com/hVj1AoUCgm32779/status/2123981188604051602"),
    "sofa": ("山田涼介 LEO ゲーム部屋のセット", "https://x.com/mo_mo1959/status/2124038851572453816"),
    "shibuya": ("RØVA 東横渋谷スーパーボードの広告", "https://x.com/yamamichan_0509/status/2124054912439124065"),
}

b = blogkit.Blocks("#9a6b3f", "#e3cfb6", "#fbf6ef")
L = b.link


def fig(name, ids, upload):
    alt, src = PHOTOS[name]
    fn = "{}_{}.jpg".format(KEY, name)
    if upload and name not in ids:
        wp = blogkit.WP(SITE)
        mid = wp.upload_media(str(blogkit.ROOT / "images" / fn), alt)
        m = wp.get("/media/{}".format(mid))
        ids[name] = {"id": mid, "url": m["source_url"]}
        MEDIA_JSON.write_text(json.dumps(ids, ensure_ascii=False, indent=2), encoding="utf-8")
    m = ids.get(name, {"id": 0, "url": "images/" + fn})
    return ('<!-- wp:image {"id":%d,"sizeSlug":"full","linkDestination":"none"} -->\n'
            '<figure class="wp-block-image size-full"><img src="%s" alt="%s" class="wp-image-%d" '
            'style="max-width:100%%;height:auto;"/>'
            '<figcaption style="font-size:0.8em;color:#888;">出典:%s</figcaption></figure>\n'
            '<!-- /wp:image -->\n') % (m["id"], m["url"], alt, m["id"], src)


def build(upload):
    ids = json.loads(MEDIA_JSON.read_text(encoding="utf-8")) if MEDIA_JSON.exists() else {}
    F = lambda n: fig(n, ids, upload)  # noqa: E731
    o = ""
    o += b.p(
        "山田涼介のPC「RØVA(ロヴァ)」は、" + b.mark("11月21日(土)の時点で全6種が売り切れ") + "でした。",
        "公式ストアでは、3モデル×2色のすべてに「売り切れ」と出ています。",
        "再販や追加の受付は、まだ発表されていません。",
    )
    o += b.p(
        "値段は" + b.mark("27万1,720円から30万600円") + "で、発送は12月末から順番に始まります。",
        "11月21日の会見では、同じ木目調の" + b.mark("ノートPCを出す") + "ことも発表されました。",
        "この記事では、値段とスペック、ノートPC、会見で話したことをまとめます。",
    )
    o += b.wakaru([
        "RØVAは売り切れ？再販はある？",
        "3モデルの値段とちがい",
        "木目調のノートPCはいつ出る？",
        "会見で山田涼介が話したこと",
        "渋谷駅の大きな広告はいつまで？",
    ])
    o += F("kaiken")

    # ---- 売り切れ ----
    o += b.h2("山田涼介のPC「RØVA」は売り切れ？")
    o += b.p(
        "11月21日(土)に" + L(STORE, "RØVAの公式ストア") + "を見ると、" + b.mark("6種すべてが売り切れ") + "の表示でした。",
        "ベージュとブラウンの2色、それぞれ3モデルがあり、どれも注文できない状態です。",
    )
    o += b.table(("モデル", "ベージュ", "ブラウン"), [
        ("RV-A7R55", "売り切れ", "売り切れ"),
        ("RV-A7R56", "売り切れ", "売り切れ"),
        ("RV-A7R56T", "売り切れ", "売り切れ"),
    ])
    o += b.mini(
        ("確認した日", "2026年11月21日(土)"),
        ("買える場所", "RØVAの公式ストアだけ(家電店などの案内はなし)"),
        ("発送", "12月末から順番に"),
        ("再販", "まだ発表なし"),
    )
    o += b.h3("再販や追加の受付はある？")
    o += b.p(
        "今のところ、再販や追加の受付のお知らせは出ていません。",
        "ただ、会見ではRØVAは「第一弾」とされ、これから続いていくプロジェクトです。",
        "ノートPCの発売も決まっているので、デスクトップも追加で受け付ける可能性はありそうです。",
    )
    o += b.p(
        "欲しい人は、Crazy Raccoonの公式Xと公式ストアをこまめに見ておくと安心です。",
        "動きがあれば、この記事に追記します。",
    )

    # ---- 値段 ----
    o += b.h2("RØVAの値段は？3モデルのちがい")
    o += b.p(
        "RØVAは、10月5日(月)に" + L(PCW, "発表") + "された木目調のゲーミングPCです。",
        "3モデルあり、ちがうのは" + b.mark("映像を動かす部品(グラフィックボード)だけ") + "です。",
        "ほかの中身は、3モデルとも同じです。",
    )
    o += b.table(("モデル", "グラフィックボード", "値段(税込)"), [
        ("RV-A7R55", "RTX 5050", "<strong>27万1,720円</strong>"),
        ("RV-A7R56", "RTX 5060", "29万970円"),
        ("RV-A7R56T", "RTX 5060 Ti", "30万600円"),
    ])
    o += b.p(
        "数字が大きいモデルほど、重いゲームもなめらかに動かしやすくなります。",
        "いちばん安いモデルと高いモデルの差は、約3万円です。",
    )
    o += F("pc")
    o += b.h3("3モデル共通のスペック")
    o += b.mini(
        ("CPU", "Ryzen 7 5700X"),
        ("メモリ", "32GB"),
        ("保存する場所(SSD)", "1TB(2TBにも変えられる)"),
        ("電源", "650W"),
        ("OS", "Windows 11 Home"),
        ("大きさ", "幅29.5×奥行35.5×高さ34.7cm"),
        ("色", "ベージュ・ブラウン"),
    )
    o += b.p(
        "注文のときに、静かなファンへの変更やOfficeの追加も選べました。",
        "同じくらいの性能のPCとくらべると、値段は高めという声もあります。",
        "そのぶん、家具のような見た目と、山田涼介が考えたデザインに価値があるPCです。",
    )
    o += b.h3("山田涼介はブラウンを使う予定")
    o += b.p(
        "会見で山田涼介は、2色のうち自分は" + L(MDPR, "「ちょっと濃いブラウンの方」") + "を使うと思うと話していました。",
        "自分の部屋のデスクや棚が、すべてウッド調だからだそうです。",
        "どちらの色にするか迷った人は、ブラウンにすれば山田涼介とおそろいになります。",
    )

    # ---- ノートPC ----
    o += b.h2("木目調のノートPCも出る！発売はいつ？")
    o += b.p(
        "11月21日の会見で、Crazy Raccoon代表の髙野大知が" + b.mark("木目調のノートPC") + "を出すと" + L(THETV, "発表") + "しました。",
        "デスクトップと同じく、木目調のデザインになります。",
    )
    o += b.mini(
        ("メモリ", "32GB(予定)"),
        ("SSD", "1TB(予定)"),
        ("名前・値段", "まだ発表なし"),
        ("発売日", "まだ発表なし"),
    )
    o += b.p(
        "山田涼介も「めちゃめちゃかっこいいし、スタイリッシュです」と見た目をアピールしました。",
        "Xでは会見の写真を見たファンから「しれっとノートパソコン持ってる」「オシャレすぎ」という声も出ていました。",
    )
    o += F("sofa")
    o += b.p(
        "デスクトップが売り切れで買えなかった人には、うれしいニュースです。",
        "ノートPCなら置き場所もとらないので、ゲームをしない人も使いやすそうです。",
        "名前や値段、発売日が出たら、この記事に追記します。",
    )

    # ---- 会見 ----
    o += b.h2("会見で山田涼介が話したこと")
    o += b.p(
        "会見は2026年11月21日(土)に東京都内で行われました。",
        "山田涼介は、ストリーマーの「LEO」として登場しました。",
        "ステージは、ゲーム部屋をイメージしたセットになっていました。",
    )
    o += b.h3("木目調にした理由")
    o += b.p(
        "山田涼介は、PCは無機質なものが多いと感じていたそうです。",
        "そこで「部屋に馴染むような、インテリアとしても成立するPC」が欲しいと話し、形にしてもらいました。",
        "完成したPCは「僕の部屋にもピッタリはまるPC」と笑顔で話しました。",
    )
    o += b.p(
        "ゲーム部屋のセットに座ると、「本当に今からゲームをしだしそうな感覚」になったそうです。",
        "最後は「たくさんの方の元に届くことを願っています」と呼びかけました。",
    )
    o += b.h3("Hey! Say! JUMPのメンバーの反応")
    o += b.p(
        "PCを作ったことを知ったメンバーからは、" + b.mark("「いつの間にPCなんて作ってたんだよ」") + "とおどろかれたそうです。",
        "山田涼介は、いろいろな反応があって「嬉しかった」と話していました。",
    )
    o += b.h3("Crazy Raccoonに入って1年")
    o += b.p(
        "山田涼介は2025年8月に、プロゲーミングチームのCrazy Raccoonに入りました。",
        "それまではYouTubeのゲームチャンネル「LEOの遊び場」の動画編集も、ひとりで全部していたそうです。",
        "今はチームが手伝ってくれるので、「気持ちが楽になりました」と感謝していました。",
    )
    o += b.p(
        "まわりからは「CRに加入してるんだよね」「LEO様だよね」と声をかけられることも増えたそうです。",
        "髙野大知も、加入の反響はとても大きかったと話していました。",
    )
    o += b.h3("キャッチコピーは「バトルプリンス」")
    o += b.p(
        "「ゲームのキャラクターになるなら弱点は？」という質問には、" + b.mark("高い所がこわい") + "と答えました。",
        "ゲームでよくある空から飛びおりる場面で、上からジャンプできない弱点にするかもと話しました。",
    )
    o += b.p(
        "ゲーム中の自分のキャッチコピーを聞かれると、しばらく考えて" + b.mark("「バトルプリンス」") + "と答えました。",
        "言ったあとに「恥ずかしいです」と照れ笑いし、会場をなごませていました。",
    )

    # ---- 渋谷 ----
    o += b.h2("渋谷駅にRØVAの大きな広告！いつまで？")
    o += b.p(
        "東急の渋谷駅にある「東横渋谷スーパーボード」に、RØVAの広告が出ると話題です。",
        "期間は" + b.mark("11月23日(月・祝)から29日(日)まで") + "です。",
        "Xでは「渋谷に9mの広告！？」とおどろく声も出ていました。",
    )
    o += F("shibuya")
    o += b.mini(
        ("場所", "東急 渋谷駅「東横渋谷スーパーボード」"),
        ("期間", "2026年11月23日(月・祝)〜29日(日)"),
    )
    o += b.p(
        "駅の中の広告なので、写真をとるときはほかの人の通行のじゃまにならないよう気をつけましょう。",
    )

    # ---- 年表 ----
    o += b.h2("LEOとRØVAのこれまで")
    o += b.table(("時期", "できごと"), [
        ("2025年8月", "Crazy Raccoonに入る"),
        ("2026年10月5日ごろ", "木目調PC「RØVA」を発表"),
        ("2026年11月21日", "記者発表の会見・ノートPCを発表"),
        ("2026年11月23〜29日", "渋谷駅に広告"),
        ("2026年12月末", "デスクトップの発送が始まる"),
    ])
    o += b.p(
        "会見の日は、ほかにもラジオや大河ドラマの宣伝などで予定がぎっしりだったようです。",
        "Xでは、いそがしくてもつかれを見せない姿に「プロのアイドルすぎる」という声も見られました。",
    )

    # ---- まとめ ----
    o += b.h2("まとめ")
    o += b.checks([
        "RØVAは11月21日の時点で、全6種が売り切れ。再販はまだ発表なし",
        "値段は27万1,720円〜30万600円。ちがいはグラフィックボードだけ",
        "発送は12月末から順番に",
        "木目調のノートPCも出る。メモリ32GB・SSD 1TBの予定で、値段と発売日はまだ",
        "11月23日〜29日は渋谷駅に大きな広告",
    ])
    o += b.p(
        "山田涼介のこだわりがつまった、部屋になじむPCでした。",
        "ノートPCの続報も楽しみに待ちましょう。",
    )
    return o


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "--publish" in sys.argv:
        state = json.loads((blogkit.ARTICLES / (KEY + "_posted.json")).read_text(encoding="utf-8"))
        blogkit.publish(SITE, state["post"], X_TEXT, X_TAGS)
    elif "--build-only" in sys.argv:
        out = blogkit.finalize(build(False), SITE, NAMES)
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        out = blogkit.finalize(build(True), SITE, NAMES)
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
