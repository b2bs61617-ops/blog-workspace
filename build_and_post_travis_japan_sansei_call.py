# -*- coding: utf-8 -*-
# chomoand-4.blog: トラジャの「さんせーい」とは？円陣の掛け声がファンとのコールになった経緯
# 2026-11-05 オシリ依頼。材料は Xiy で集めたX投稿(tools/Xiy/posts_1105_sansei_x_top, posts_1105_sansei_enjin_x)。
# Threadsは「さんせーい」「トラジャ 円陣」とも0件だった。一般ファンの投稿は要約のみ(引用・リンクなし)。
import json, sys, subprocess
from pathlib import Path
import requests

from build_and_post_travis_japan_tour2027_odds_survey import (
    ROOT, WP_URL, HJSON, SITE, ACC, BORDER, BG, p, h2, h3, wphtml, mark,
    whatbox, minibox, table2, checklist, related, upload_media)

IMG_DIR = ROOT / "images" / "tj_sansei_call"
EYECATCH = IMG_DIR / "tj_sansei_call_eyecatch_canva.jpg"
STATE = IMG_DIR / "_state.json"
DRY = "--dry" in sys.argv

TITLE = "トラジャの「さんせーい」はいつから？円陣の掛け声の由来と経緯！"
SLUG = "travis-japan-sansei-call-origin"

X_DIR = ROOT / "tools" / "Xiy"
LOGO_SRC = X_DIR / "posts_1105_sansei_enjin_x" / "images" / "post_50_img_1.jpg"
LOGO_URL = "https://x.com/tj__sweetO623/status/1335788454983024641"
MIYAZAKI_SRC = X_DIR / "posts_1105_sansei_x_top" / "images" / "post_7_img_1.jpg"
MIYAZAKI_URL = "https://x.com/MiyazakiCity_PR/status/2117079596797739475"

# frames cut from official YouTube videos (rules.md: official YouTube -> cut frames directly)
TEASER_URL = "https://www.youtube.com/watch?v=FsUisvoVOik"  # 's travelers Teaser, 0:04 / 0:08
BONUS_URL = "https://www.youtube.com/watch?v=JIcOL8nzJOY"  # 's travelers Bonus Disc Trailer (Limited), 1:14
FRAMES = {
    "codeword": (IMG_DIR / "frame_teaser_codeword.jpg", "'s travelersの開演前にスクリーンに映る「Travis Japanと一緒にコンサート盛り上がっちゃってもいいですか？」", TEASER_URL),
    "seven": (IMG_DIR / "frame_teaser_seven.jpg", "'s travelersのステージに登場したTravis Japanの7人", TEASER_URL),
    "backstage": (IMG_DIR / "frame_bonus_backstage.jpg", "'s travelersの楽屋で円陣を組んで手を上げるTravis Japan", BONUS_URL),
}

KOROPEN = ("「コロペン」とは？ペンライトの色を変える意味を解説！", "what-is-koropen-penlight-color-change-597")
PRODUCE = ("トラジャのアルバム・コンサートは毎年違うメンバーがプロデュース？", "is-toraja-concert-produced-by-214")
SCHEDULE = ("トラジャ2027ツアー『Jewelry Basket』の会場・日程まとめ！", "travis-japan-2027-tour-jewelry-basket-schedule-1973")
FC = ("トラジャのFCはいつ入るのが正解？ツアー発表は毎年10月末！", "travis-japan-fanclub-when-to-join-1643")

TIMELINE = [
    ("2020年1月", "ジャニーズJr.チャンネルの全国ツアー発表回で、7人が円陣を組んで「さんせーい」"),
    ("2020年6月〜", "公式Instagramのストーリーズで、楽屋の円陣がたびたび公開される"),
    ("2020年12月", "初の全国ツアー名が「IMAGE NATION ～全国ツアーしちゃってもいいですかっ!?～」に。ロゴも円陣の手のデザイン"),
    ("2021年3月〜", "IMAGE NATIONツアーで、客席も手を前に出して一緒に「さんせーい」。ファンとのコールに"),
    ("2023年〜", "デビュー後のツアーでも、アンコールの最後は客席と円陣が定番"),
    ("2024年", "「THE夜会」「RIDE ON TIME」「ラヴィット！」などテレビでも円陣が映り、ファン以外にも広まる"),
    ("2025年", "VIIsualツアーでは、日替わりの「円陣担当」メンバーが掛け声を担当"),
    ("2026年", "'s travelersツアーは「さんせーい」から始まる演出に。曲「Dance With Me ～Lesson 2～」にも賛成のセリフが入る"),
    ("2026年8月〜", "Jリーグのハーフタイムショー、サマソニ、宮崎市の公式アカウントでも「さんせーい」"),
]


def figure(media, alt, src_url):
    sizes = media.get("sizes", {})
    large = sizes.get("large") or sizes.get("full")
    medium = sizes.get("medium") or large
    full = sizes.get("full") or large
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{large['url']}" alt="{alt}" width="{large['w']}" height="{large['h']}" style="max-width:100%;height:auto;" srcset="{medium['url']} {medium['w']}w, {large['url']} {large['w']}w, {full['url']} {full['w']}w" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption>出典:{src_url}</figcaption>
</figure>''')


def upload_with_sizes(path, title, alt):
    m = upload_media(path, title, alt)
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{m['id']}", headers=HJSON)
    r.raise_for_status()
    d = r.json()["media_details"]
    sizes = {k: {"url": v["source_url"], "w": v["width"], "h": v["height"]} for k, v in d.get("sizes", {}).items()}
    return {"id": m["id"], "sizes": sizes}


def timeline_box():
    rows = "\n".join(
        f'<div style="display:flex;margin:0 0 10px 0;"><span style="flex:0 0 7.5em;font-weight:bold;color:{ACC};">{y}</span><span style="flex:1;">{t}</span></div>'
        for y, t in TIMELINE)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">「さんせーい」の年表</p>
<div style="padding:14px 18px 6px 18px;background:{BG};">
{rows}
</div>
</div>''')


def build(logo=None, miyazaki=None, frames=None):
    frames = frames or {}

    def fr(key):
        if key in frames:
            b.append(figure(frames[key], FRAMES[key][1], FRAMES[key][2]))

    b = []
    b.append(p([
        f"Travis Japanのライブで聞こえる「さんせーい！」は、{mark('もともとメンバー7人だけでやっていた円陣の掛け声')}です。",
        "メンバーが「〇〇しちゃってもいいですか！」と聞いて、全員で「さんせーい！」と返します。",
        f"それが2021年の初の全国ツアー「IMAGE NATION」から{mark('客席も一緒に手を出して返すコール')}になり、今ではトラジャとトラジャ担の合言葉になっています。",
        "この記事では、「さんせーい」の意味と、円陣の掛け声がファンとのコール&レスポンスに広がった経緯を、Xに残っているライブのレポや公式の発信から年表にしてまとめます。",
    ]))
    b.append(whatbox([
        "トラジャの「さんせーい」の意味とやり方",
        "円陣の掛け声はいつから？誰が言い出した？",
        "ファンも一緒に言うようになった経緯",
        "テレビ・Jリーグ・サマソニまで広がった最近の「さんせーい」",
        "ライブで「さんせーい」を言うときのポイント",
    ]))

    # ---- what ----
    b.append(h2("トラジャの「さんせーい」とは？円陣の掛け声"))
    b.append(minibox([
        ("呼びかけ", "メンバー「〇〇しちゃってもいいですか！？」"),
        ("返し", "全員「さんせーい！」(手を上にあげる)"),
        ("使う場面", "本番前の円陣、ライブの最後、テレビの歌の前など"),
        ("そのあと", "メンバー同士でハグすることが多い"),
    ]))
    b.append(p([
        "「さんせーい」は、Travis Japanが円陣を組んだときの掛け声です。",
        "1人が「これから〇〇しちゃってもいいですか！」と問いかけて、残りのメンバーが「さんせーい！」と答えます。",
        "「〇〇」の部分は毎回ちがっていて、その日の会場や気分に合わせて変わるのが特徴です。",
    ]))
    b.append(p([
        "ライブのレポを見ると、こんな呼びかけがありました。",
    ]))
    b.append(table2(["公演", "呼びかけ(要約)"], [
        ["2021年 大阪", "TravisJapan、また大阪来ちゃってもいーですか！"],
        ["2021年 札幌", "北海道みたいに、でっかいグループになっちゃってもいーですか！"],
        ["2025年 大阪", "みんなのこと、たこやきに詰め込んで食べちゃってもいいですかっ！？"],
        ["2026年 北海道", "北海道みたいにでっかい愛で、まるごとTravis Japan包んじゃってもいいですかっ！"],
        ["2026年 愛知", "“あいち”あっちゃってもいいですかっ！"],
    ]))
    b.append(p([
        "ご当地ネタやダジャレが入ることも多く、会場ごとの「今日の呼びかけ」がファンのレポで毎回話題になります。",
        "否定せずに全員で「賛成！」と返す形なので、「メンバーのアイデアを否定せずに面白がって作っていくトラジャらしさそのもの」と受け止めているファンも多いです。",
    ]))
    b.append(h3("中村海人さんの手だけ上向き"))
    b.append(p([
        "トラジャの円陣には、もうひとつ有名なポイントがあります。",
        f"みんなが手を重ねるとき、{mark('いちばん下の中村海人さんだけ手のひらを上に向けている')}ことです。",
        "「さんせーい！」のタイミングで、下から全員の手を押し上げるような形になっていて、「全員の手の重みを受け止めている」とファンの間では有名です。",
        "そして「さんせーい！」のあとは、メンバー全員でハグをするところまでが一連の流れになっています。",
    ]))
    fr("backstage")
    b.append(p([
        "2026年の「's travelers」ツアーのBlu-ray&DVD初回盤のツアードキュメンタリーにも、楽屋で円陣を組んで、全員で手を上げて「賛成」と叫ぶ場面が入っています。",
        "ステージの上だけでなく、本番前の楽屋でも同じように円陣を組んでいることが分かります。",
    ]))

    # ---- origin ----
    b.append(h2("「さんせーい」はいつから？円陣の掛け声の始まり"))
    b.append(p([
        f"誰が最初に考えたのかは、{mark('メンバーからはっきり語られていません')}。",
        "ファンの用語集のブログなどでは「トラジャ自身が考えた円陣の掛け声」と紹介されていて、「ジャニーズWESTにヒントをもらった」という説もありますが、こちらは裏付けが見つかりませんでした。",
        "ただ、Xに残っている投稿をさかのぼると、ジャニーズJr.時代の2020年にはすでに定番になっていたことが分かります。",
    ]))
    b.append(h3("2020年1月：全国ツアー決定の発表で円陣"))
    b.append(p([
        "2020年1月、ジャニーズJr.チャンネルの動画で、Travis Japanの全国ツアー決定が発表されました。",
        "このときの意気込みの場面で、川島如恵留さんの「円陣組んじゃいますか？」から7人で円陣を組み、宮近海斗さんの「皆さんを楽しませてもいいですか？」に全員で「さんせーい」と返しています。",
        "同じ年の6月ごろからは、公式Instagramのストーリーズで楽屋の円陣の動画がたびたび公開され、「円陣が見られてうれしい」という声が増えていきました。",
        "YouTubeの「童謡を踊ってみた」企画でも、「アルプス一万尺かっこよく踊ってもいいですか？」「さんせーい！」と円陣を組む場面があり、ファンの間では「トラジャといえば円陣」というイメージが広がっていきます。",
    ]))
    b.append(h3("2020年12月：ツアー名が「しちゃってもいいですかっ!?」に"))
    b.append(p([
        "大きな転機になったのが、2020年12月に発表された初の全国ツアーのタイトルです。",
        f"ツアー名は{mark('「Travis Japan Live tour 2021 IMAGE NATION ～全国ツアーしちゃってもいいですかっ!?～」')}で、円陣の呼びかけそのものがサブタイトルになりました。",
        "ツアーのロゴも、7つの王冠から手が伸びて円陣を組んでいるデザインです。",
    ]))
    if logo:
        b.append(figure(logo, "Travis Japan Live tour 2021 IMAGE NATIONのツアーロゴ", LOGO_URL))
    b.append(p([
        "よく見ると、7本の手のうち1本だけ手のひらの向きがちがっていて、「中村海人さんの手まで再現されている」とファンの間で話題になりました。",
        "ハッシュタグも「#全国ツアーしちゃってもいいですかっ！？」「#さんせーい」が使われ、ここで「さんせーい」がファン全体の言葉になっていきます。",
    ]))

    # ---- fans ----
    b.append(h2("ファンも一緒に「さんせーい」を言うようになった経緯"))
    b.append(h3("2021年IMAGE NATIONツアー：客席も手を出して円陣に"))
    b.append(p([
        f"ファンが一緒に「さんせーい」を言うようになったのは、{mark('2021年3月から始まったIMAGE NATIONツアー')}からです。",
        "ライブの最後に宮近海斗さんが「みんなで円陣組んで終わりましょう、皆さんも手を前に出して」と呼びかけ、客席も手を前に出して、メンバーの「〇〇しちゃってもいいですか！」に「さんせーい！」と返す形になりました。",
        "当時のレポでは、福岡・大阪・京都・横浜・宮城・札幌と、どの会場でも最後はこの円陣で締めくくられています。",
        "「トラジャと客席のみんなで円陣を組んだのがすごくよかった」「グループの一員になれた気分」という感想が多く、ここから「さんせーい」がメンバーとファンのコール&レスポンスとして定着しました。",
    ]))
    b.append(p([
        "あとから「ライブでもファンみんなでやろうって決めたのは誰なんだろう、発案した人に感謝しかない」という投稿も見られ、ファンにとって特別な時間になっていることが分かります。",
    ]))
    b.append(h3("デビュー後も「ライブの最後は円陣」が定番に"))
    b.append(p([
        "2022年のデビュー後も、この流れはずっと続いています。",
        "2023年のデビューツアー「THE SHOW」、2024年の「Road to Authenticity」でも、アンコールの最後は客席と一緒に円陣を組んで「さんせーい」で終わるのが定番でした。",
        "2024年1月の横浜アリーナ公演では、見学に来ていた後輩も客席で一緒に「さんせーい」をしていたというレポもあります。",
        "2025年の「VIIsual」ツアーでは、日替わりで「円陣担当」のメンバーが掛け声を担当していて、松倉海斗さんの「たこやき」の呼びかけや、吉澤閑也さん・中村海人さんの呼びかけなど、メンバーごとの個性が出る場面になっていました。",
    ]))
    b.append(h3("2026年's travelers：「さんせーい」から始まるライブ"))
    b.append(p([
        f"2026年の「's travelers」ツアーでは、{mark('客席みんなの「さんせーい」からライブが始まる演出')}がありました。",
        "公式のティーザー映像を見ると、開演前のスクリーンに「CODE WORD FINAL」として「Travis Japanと一緒にコンサート盛り上がっちゃってもいいですか？」と映し出され、会場全体が「さんせーい！！！」と答えています。",
    ]))
    fr("codeword")
    b.append(p([
        "この「さんせーい」を合図に、メンバー7人がステージに登場してライブが始まります。",
    ]))
    fr("seven")
    b.append(p([
        "ライブの始まりと終わりの両方に「さんせーい」が入る形で、参加したファンからは「声を出してさんせーいしてから始まるコンサートが楽しすぎた」という声が多く見られます。",
        f'このツアーは松倉海斗さんがプロデュースした回です(<a href="{SITE}{PRODUCE[1]}">{PRODUCE[0]}</a>)。',
        "Blu-ray&DVDの発売時には、CDショップの告知でも「トラジャと一緒に時間旅行しちゃってもいいですかっ!?」「さんせーい」と書かれていて、お店側まで乗っかるほど定着しています。",
    ]))
    b.append(p([
        "2026年4月15日リリースの「Dance With Me ～Lesson 2～」には、歌詞の掛け声パートに「いいですか」「賛成」のセリフが入っていて、とうとう曲の中でも「さんせーい」ができるようになりました。",
        "ファンコールが入る曲としては、公式YouTubeの「ファンコール講座」で「JUST DANCE!」「Would You Like One?」のコールもメンバー自身が教えています。",
    ]))

    # ---- spread ----
    b.append(h2("テレビ・Jリーグ・サマソニにも広がった「さんせーい」"))
    b.append(h3("テレビで円陣が映って、ファン以外にも知られるように"))
    b.append(p([
        "2024年には、テレビ番組でも円陣が映る機会が増えました。",
        "5月の「THE夜会」では、トラジャ担にとっては当たり前の「さんせーい」が、知らない人から見ると珍しい掛け声だと改めて気づいた、という感想が出ています。",
        "7月のドキュメンタリー「RIDE ON TIME」でも円陣とハグが映り、8月の「ラヴィット！」でメンバー7人が全員集合したときは、歌の前に円陣を組んで「さんせーい」をする姿が流れました。",
        "「TJポーズの次はさんせーいが世に知れ渡る番だ」という声もあり、この年をきっかけにファン以外にも知られていきます。",
    ]))
    b.append(h3("2026年：渋谷のビジョン、Jリーグ、サマソニ"))
    b.append(p([
        "2026年は、ライブ以外の場所でも「さんせーい」が聞こえる1年になりました。",
        "6月には、ディズニープラスのアメリカ旅番組のCMが渋谷のビジョンで流れ、スクランブル交差点に「さんせーい」の声が響いたという投稿が話題になっています。",
        f"8月にJリーグ2026/27シーズンのスペシャルアンバサダーに就任したあとは、ハーフタイムショーの本番前に{mark('「いい歌届けちゃっていいですか？」「さんせーい」')}といつもの円陣をしていて、「緊張していない、いつも通りのトラジャ」とファンを安心させました。",
        "同じ8月のサマソニでは、出番前のステージ裏から7人の「さんせーい」が聞こえてきたというレポや、客席の「さんせーい」の声が地面に響くくらい大きかったというレポもあります。",
    ]))
    b.append(h3("宮崎市の公式アカウントも「さんせーい」"))
    b.append(p([
        "2026年11月3日のテゲバジャーロ宮崎の試合に七五三掛龍也さんと吉澤閑也さんが来場したときは、宮崎市の公式Xがトラジャ担に向けて歓迎のメッセージを出しました。",
        f"その中には{mark('「宮崎楽しんじゃってもいいですかっ！？ ＼さんせーい／」')}という一文があり、宮崎市観光案内所の黒板にも「トラジャ担のみなさん ようこそ宮崎へ」と書かれていました。",
    ]))
    if miyazaki:
        b.append(figure(miyazaki, "宮崎市観光案内所のトラジャ担歓迎の黒板", MIYAZAKI_URL))
    b.append(p([
        "自治体の公式アカウントが使うほど、「さんせーい」はTravis Japanを表す言葉として広く知られるようになっています。",
    ]))
    b.append(h3("日常でも「さんせーい」するトラジャ担"))
    b.append(p([
        "ファンの間では、ライブ以外でも「さんせーい」が合言葉として使われています。",
        "メンバーのお祝いの日や新曲の発売日には「〇〇しちゃってもいいですか？」「さんせーい」という投稿があふれます。",
        "部活の大会前の円陣でトラジャの掛け声をまねしたら勝ち進めたという話や、2歳の子どもが「いつか親子参戦しようね」に「さんせーい！」と返してくれるようになったという話もありました。",
        "「同意をするシステムが平和で、Travis Japanを象徴している」という声もあり、グループの雰囲気そのものを表す言葉として愛されています。",
    ]))

    # ---- timeline ----
    b.append(h2("「さんせーい」の歴史を年表でおさらい"))
    b.append(timeline_box())

    # ---- how to ----
    b.append(h2("ライブで「さんせーい」を言うときのポイント"))
    b.append(p([
        "初めてトラジャのライブに行く人のために、「さんせーい」のポイントをまとめます。",
    ]))
    b.append(checklist("初参戦でも安心のポイント", [
        "メンバーが「〇〇しちゃってもいいですか！」と言ったら、元気に「さんせーい！」と返す",
        "円陣のときは、メンバーに合わせて手を前に出し、「さんせーい！」で手を上にあげる",
        "呼びかけの中身は毎回ちがうので、最後の「いいですか！」を聞き逃さなければ大丈夫",
        "ペンライトを持ったままでもOK、周りに当たらないように気をつける",
        "声出しのルールは公演ごとの案内に従う",
    ]))
    b.append(p([
        "「さんせーい」は覚える歌詞もなく、その場で誰でも参加できるのがいいところです。",
        f'ペンライトの使い方は<a href="{SITE}{KOROPEN[1]}">{KOROPEN[0]}</a>でもくわしく紹介しています。',
        f'2027年のツアー「Jewelry Basket」の会場・日程は<a href="{SITE}{SCHEDULE[1]}">{SCHEDULE[0]}</a>にまとめています。',
    ]))

    # ---- matome ----
    b.append(h2("まとめ"))
    b.append(checklist("この記事のポイント", [
        "「さんせーい」は、Travis Japanが円陣を組むときの掛け声",
        "メンバーの「〇〇しちゃってもいいですか！」に、全員で「さんせーい！」と返す",
        "誰が考えたかは公表されていないが、ジャニーズJr.時代の2020年にはすでに定番",
        "2021年の全国ツアー名が「IMAGE NATION ～全国ツアーしちゃってもいいですかっ!?～」に",
        "IMAGE NATIONツアーから、客席も手を出して一緒に言うコールになった",
        "2026年は's travelersツアーの始まり、Jリーグ、サマソニ、宮崎市の公式アカウントでも「さんせーい」",
    ]))
    b.append(p([
        "2027年のツアーでも、どんな「〇〇しちゃってもいいですか！」が聞けるのか楽しみですね！",
        "我が家もチケットが当たれば、親子で参戦する予定です！",
        "トラジャ担のみんなが、トラジャと楽しい時間を過ごせますように！",
    ]))
    b.append(related([KOROPEN, PRODUCE, SCHEDULE, FC]))
    return "\n\n".join(b)


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    if DRY:
        html = build()
        (IMG_DIR / "_dry.html").write_text(html, encoding="utf-8")
        print("dry chars:", len(html))
        return
    if "logo" not in state:
        state["logo"] = upload_with_sizes(LOGO_SRC, "IMAGE NATION ツアーロゴ", "Travis Japan Live tour 2021 IMAGE NATIONのツアーロゴ")
    if "miyazaki" not in state:
        state["miyazaki"] = upload_with_sizes(MIYAZAKI_SRC, "宮崎市観光案内所の黒板", "宮崎市観光案内所のトラジャ担歓迎の黒板")
    state.setdefault("frames", {})
    for key, (path, alt, _) in FRAMES.items():
        if key not in state["frames"]:
            state["frames"][key] = upload_with_sizes(path, alt, alt)
    STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    html = build(state["logo"], state["miyazaki"], state["frames"])
    tmp = IMG_DIR / "_post.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis", str(tmp)], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "check", "--group", "travis", str(tmp)], check=True)
    html = tmp.read_text(encoding="utf-8")
    if not EYECATCH.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
                        "--main", "さんせーい", "--bottom", "円陣の掛け声はいつから？",
                        "--bottom", "ファンとのコールになった経緯！", "--color-key", "group", "--out", str(EYECATCH)], check=True)
    if "eyecatch" not in state:
        state["eyecatch"] = upload_media(EYECATCH, TITLE, TITLE)
        STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    body = {"title": TITLE, "slug": SLUG, "content": html, "status": "draft",
            "categories": [3], "author": 2, "featured_media": state["eyecatch"]["id"]}
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
