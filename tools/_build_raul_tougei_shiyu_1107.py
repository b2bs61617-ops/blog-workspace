# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man) ラウール 月刊ザテレビジョン「Snowらいふ」第196回(初めての陶芸体験)の陶芸教室=私游 記事.

2026-11-07 オシリ依頼。
- 公式写真: 月刊ザテレビジョン公式X https://x.com/thetvjp/status/2080189444720931271 (HN5QTUpaIAA4mCJ)
- 教室情報: 公式サイト sukki.jp / じゃらん spt_guide000000185440 / アソビュー pln3000014375 / note(オーナー小池さんインタビュー)
- ファン・第三者の投稿の画像は使わない(feedback: 他人の特定投稿は使わない)。訪問の声は要旨のみ
usage: python tools/_build_raul_tougei_shiyu_1107.py build|post
"""
import base64, os, sys
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parent.parent
BASE = "raul_tougei_shiyu_1107"
HTML_PATH = ROOT / "articles" / f"{BASE}.html"
EYECATCH_PATH = ROOT / "images" / f"{BASE}_eyecatch.jpg"
PHOTO_PATH = ROOT / "images" / f"{BASE}_official.jpg"
PHOTO_URL = "https://pbs.twimg.com/media/HN5QTUpaIAA4mCJ.jpg?name=orig"
OFFICIAL_X = "https://x.com/thetvjp/status/2080189444720931271"

TITLE = "【未】【Snowらいふ】ラウールの陶芸教室はどこ？赤羽橋の私游が有力！"
SLUG = "raul-pottery-class-shiyu"
AUTHOR = 2  # momo(USER1 / オシリ)
CATEGORIES = [4, 8]

# ラウールのメンバーカラーは白なので、白に合う落ち着いたグレー系をアクセントに
ACC = "#5b6670"
BG = "#f4f5f6"
LINE = "#d6d9dc"
MK = "#dfe3e6"


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


def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n"


def mk(text):
    return f'<strong><span style="font-size:1.1em;background:linear-gradient(transparent 60%,{MK} 60%);">{text}</span></strong>'


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n'


def html(s):
    return "<!-- wp:html -->\n" + s + "\n<!-- /wp:html -->\n"


def listbox(title, items, big=False):
    fs = "font-size:1.05em;" if big else ""
    pad = "10px 18px" if big else "8px 16px"
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return html(f'<div style="border:1px solid {ACC if big else LINE};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                f'<p style="font-weight:bold;{fs}margin:0;padding:{pad};background:{ACC};color:#fff;">{title}</p>\n'
                f'<ul style="margin:0;padding:12px 18px 12px 34px;background:{BG};">\n{lis}\n</ul>\n</div>')


def keybox(rows):
    out = []
    for i, (k, v) in enumerate(rows):
        m = "0" if i == 0 else "4px 0 0 0"
        out.append(f'<p style="margin:{m};"><strong>{k}:</strong>{v}</p>')
    return html(f'<div style="border:1px solid {LINE};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">\n'
                + "\n".join(out) + "\n</div>")


def voicebox(title, lines):
    lis = "\n".join(f"<li>{l}</li>" for l in lines)
    return html(f'<div style="border:1px solid {LINE};border-radius:4px;padding:12px 18px;margin:0 0 16px 0;background:{BG};">\n'
                f'<p style="margin:0 0 6px 0;font-weight:bold;color:{ACC};">{title}</p>\n'
                f'<ul style="margin:0;padding-left:20px;">\n{lis}\n</ul>\n</div>')


def checkbox(title, items):
    lis = "\n".join(
        f'<li style="margin:0 0 6px 0;"><span style="display:inline-block;border:1px solid {ACC};border-radius:3px;'
        f'padding:0 4px;margin-right:6px;font-size:0.8em;color:{ACC};">&#10003;</span>{i}</li>' for i in items)
    return html(f'<div style="border:1px solid {ACC};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">{title}</p>\n'
                f'<ul style="list-style:none;margin:0;padding:14px 18px;background:{BG};">\n{lis}\n</ul>\n</div>')


def table(rows):
    trs = []
    for i, r in enumerate(rows):
        if i == 0:
            cells = "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;background:{ACC};color:#fff;font-weight:bold;">{c}</td>' for c in r)
        else:
            bg = "#fff" if i % 2 else BG
            cells = "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;background:{bg};">{c}</td>' for c in r)
        trs.append(f"<tr>{cells}</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            + "".join(trs) + "</tbody></table></figure>\n<!-- /wp:table -->\n")


def related(items):
    lis = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in items)
    return html(f'<div style="border:1px solid {LINE};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;">\n'
                f'<p style="margin:0 0 6px 0;font-weight:bold;color:{ACC};">あわせて読みたい</p>\n<ul style="margin:0;padding-left:20px;">{lis}</ul>\n</div>')


def photo(alt):
    return html('<figure class="wp-block-image size-large">\n'
                f'<img src="{{{{IMG:official}}}}" alt="{alt}" style="max-width:100%;height:auto;" loading="lazy">\n'
                f'<figcaption style="font-size:0.8em;color:#888;">出典:<a href="{OFFICIAL_X}" target="_blank" rel="noopener">{OFFICIAL_X}</a></figcaption>\n</figure>')


def gmap(q):
    return html(f'<iframe src="https://www.google.com/maps?q={quote(q)}&output=embed" width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy"></iframe>')


SITE = "https://chomoand-2.com"
OFFICIAL_SITE = "https://www.sukki.jp/"
JALAN = "https://www.jalan.net/kankou/spt_guide000000185440/"
ASOVIEW = "https://www.asoview.com/item/activity/pln3000014375/"


def build():
    B = []
    B.append(p(
        "月刊ザテレビジョンの連載「Snowらいふ」で、ラウールさんが初めての陶芸に挑戦した回が話題になりました。",
        "エプロン姿で大きな器を差し出す笑顔の写真を見て、「この陶芸教室はどこ？」「同じ場所で体験してみたい」と気になった人も多いはずです。",
    ))
    B.append(p(
        "調べてみると、撮影に使われた教室は、東京・港区の" + mk("「陶芸 gallery cafe 私游（しゆう）」") + "が有力です。",
        "公式写真に写っている店内の特徴が私游の教室とよく一致していて、実際に体験しに行くファンも増えています。",
        "この記事では、ラウールさんの陶芸回の内容、私游が有力といえる理由、場所や料金、聖地巡礼のポイントまでまとめました。",
    ))
    B.append(listbox("この記事でわかること", [
        "ラウールの陶芸回が載った号と内容",
        "陶芸教室が私游と考えられる理由",
        "私游の場所・アクセス",
        "陶芸体験の料金・予約方法",
        "聖地巡礼で気をつけたいこと",
    ], big=True))

    # --- 掲載号
    B.append(h2("ラウールが陶芸に挑戦した「Snowらいふ」はいつの号？"))
    B.append(keybox([
        ("掲載誌", "月刊ザテレビジョン 2026年9月号（2026年7月23日発売）"),
        ("連載", "Snow Manの「Snowらいふ」第196回「初めての陶芸体験」"),
        ("登場", "ラウール（ソロ回）"),
    ]))
    B.append(p(
        "ラウールさんの陶芸回が載ったのは、2026年7月23日に発売された月刊ザテレビジョン2026年9月号です。",
        "Snow Manの連載「Snowらいふ」は、メンバーがさまざまな体験に挑戦する人気企画で、今回が第196回でした。",
        "誌面のタイトルは「初めての陶芸体験」で、その名のとおりラウールさんにとって初めての陶芸だったそうです。",
    ))
    B.append(photo("月刊ザテレビジョンSnowらいふで陶芸に挑戦したラウール"))
    B.append(p(
        "月刊ザテレビジョン公式Xによると、この撮影はラウールさん本人のリクエストを受けて、陶芸教室で行われました。",
        "「食」と「器」に興味津々のラウールさんが、初めての陶芸に奮闘する様子が紹介されています。",
        "誌面では陶芸のほか、アートやファッションについてのインタビューも掲載されました。",
    ))
    B.append(h3("撮影では「慎重派」な一面も"))
    B.append(p(
        "公式Xは、今回の撮影について「ラウールさんの慎重派な性格が垣間見える撮影」だったと紹介していました。",
        "ステージでは大胆なダンスが印象的なラウールさんですが、ろくろの前では一つひとつの工程を丁寧に確かめながら進めていたようです。",
        "誌面には「集中して土をいじっていると落ち着くし、とてもいい精神状態になれました」という言葉も載っていて、陶芸の時間をしっかり楽しんだことが伝わってきます。",
    ))
    B.append(h3("ラウールが作った器は大きめの鉢"))
    B.append(p(
        "公開された写真でラウールさんが両手で差し出しているのは、電動ろくろで形を作った大きめの鉢です。",
        "焼く前の素地の状態なので、まだ灰色の土の色をしています。",
        "初めてとは思えないほど口がきれいに開いた形で、手の大きいラウールさんが持っていても存在感のあるサイズでした。",
        "自炊をよくするラウールさんらしく、普段の食卓で使えそうな器を選んだのかもしれません。",
    ))
    B.append(voicebox("写真公開後のファンの反応", [
        "「嬉しそう」「あまりにかわいい」",
        "「心が浄化される笑顔」",
        "「手が大きくて激メロ」",
    ]))
    B.append(p(
        "写真が公開されると、満面の笑みで器を見せる姿に反響が集まり、ニュースサイトでも取り上げられました。",
        "発売日には「陶芸姿を見るために本屋に走った」というファンも多く、ラウールさんの新しい一面に注目が集まった号になりました。",
    ))

    # --- 教室
    B.append(h2("ラウールの陶芸教室はどこ？赤羽橋の「陶芸 gallery cafe 私游」が有力"))
    B.append(keybox([
        ("有力な教室", "陶芸 gallery cafe 私游（しゆう）"),
        ("場所", "東京都港区東麻布1丁目（都営大江戸線 赤羽橋駅のすぐ裏）"),
        ("根拠", "公式写真に写る店内の特徴が一致"),
    ]))
    B.append(p(
        "月刊ザテレビジョンの誌面や公式Xでは、撮影した陶芸教室の名前は公表されていません。",
        "ただ、公式写真の背景と照らし合わせると、港区東麻布にある「陶芸 gallery cafe 私游」の教室である可能性が高いです。",
    ))
    B.append(h3("公式写真と私游の教室が一致したポイント"))
    B.append(p(
        "公式写真のラウールさんの後ろには、作品や道具が並んだ棚がはっきり写っています。",
        "私游の教室の様子と見比べると、次のような特徴が共通していました。",
    ))
    B.append(listbox("一致した店内の特徴", [
        "グレーのコンクリート壁に、明るい木材の棚を取り付けている",
        "棚は縦の木の支柱で組まれ、素焼き前の器がぎっしり並んでいる",
        "棚の下段に、緑の帯ラベルが付いた白い釉薬ボトルが並んでいる",
        "釉薬ボトルは透明のトレーに入れて棚に置かれている",
    ]))
    B.append(p(
        "1つひとつはほかの陶芸教室にもありそうな特徴ですが、壁・棚・釉薬ボトルの置き方までそろっているのは偶然とは考えにくいところです。",
        "公式写真は背景がぼかされているため、ボトルのラベルの文字までは読めず、「100%同じ」と断定はできません。",
        "それでも、店内の作りがここまで重なることから、私游がもっとも有力な候補といえます。",
    ))
    B.append(h3("実際に訪れたファンからも「ラウールと同じ教室」の声"))
    B.append(p(
        "2026年8月ごろからは、私游で陶芸体験をしたファンの声もXで見られるようになりました。",
        "教室のスタッフが、ラウールさんの撮影当日の様子を話してくれたという声が多く、温かく迎えてもらえたという感想が目立ちます。",
    ))
    B.append(voicebox("私游を訪れたファンの声（要旨）", [
        "ラウールさんが座った席や、使った釉薬の色を教えてもらえた",
        "「真面目で慎重な方でした」とスタッフから聞いた",
        "ラウールさんの大皿をまねて、同じ釉薬で作ってみた",
        "陶芸のあとはカフェでゆっくり話を聞けて最高の時間だった",
    ]))
    B.append(p(
        "スタッフの話に出てくる「慎重な方」という印象は、公式Xが紹介していた「慎重派な性格」ともぴったり重なります。",
        "こうした声からも、私游がラウールさんの撮影場所である可能性はかなり高いと考えられます。",
    ))
    B.append(h3("私游はどんな陶芸教室？"))
    B.append(p(
        "私游は、陶芸教室とギャラリー、カフェがひとつになったお店です。",
        "新人から有名作家まで、さまざまな陶芸家の作品を展示・販売していて、作品を眺めながらくつろげる空間になっています。",
        "陶芸体験は電動ろくろと手びねりの2種類があり、ほかに金継ぎ教室も開かれています。",
    ))
    B.append(p(
        "2026年4月には新店舗へリニューアルし、天井が高く開放感のある広々とした教室になりました。",
        "ラウールさんの撮影が行われたのは、このリニューアル後の教室とみられます。",
        "カフェでは、ペットの写真をもとに描く「うちの子アート」も頼めるほか、トイプードルの看板犬たちにも会えるかもしれません。",
    ))
    B.append(p(
        "オーナーの小池さんは、映画『ゴースト』のろくろの場面に憧れて陶芸を始めたそうです。",
        "インタビューでは「上手い・下手じゃなくて、自由に表現できる場所をつくりたかった」と語っていて、初心者でも気軽に楽しめる雰囲気づくりを大切にしていることがわかります。",
    ))

    # --- 場所
    B.append(h2("私游の場所・アクセス"))
    B.append(table([
        ["項目", "内容"],
        ["店名", "陶芸 gallery cafe 私游（しゆう）"],
        ["住所", "東京都港区東麻布1-27-11（公式サイト・じゃらん）<br>※アソビューの集合場所は東麻布1-28-2 1階B"],
        ["最寄り駅", "都営大江戸線「赤羽橋駅」中之橋口からすぐ（ファミリーマートの裏）"],
        ["ほかの駅", "麻布十番駅 徒歩約8分／芝公園駅 徒歩約8分／神谷町駅 徒歩約11分／浜松町駅 徒歩約17分"],
        ["営業時間", "10:00〜22:00（公式サイト）<br>※カフェは日によって営業日・時間が異なる"],
        ["定休日", "年中無休（不定休あり）"],
        ["駐車場", "なし（近くのコインパーキングを利用）"],
    ]))
    B.append(p(
        "私游は、都営大江戸線の赤羽橋駅の中之橋口を出てすぐ、ファミリーマートの裏手にあります。",
        "東京タワーのお膝元ともいえる場所で、駅からほとんど歩かずに行けるのがうれしいポイントです。",
        "なお、住所は公式サイトとじゃらんでは「東麻布1-27-11」、アソビューの集合場所は「東麻布1-28-2 1階B」と表記が分かれています。",
        "リニューアルにともなう表記の違いとみられるので、予約したサイトの案内で集合場所を確認しておくと安心です。",
    ))
    B.append(gmap("陶芸 gallery cafe 私游 東麻布"))
    B.append(p(
        "教室も注意をうながしていますが、JRの「赤羽駅」とまちがえて北区へ向かってしまう人もいるそうです。",
        "最寄りは「赤羽橋駅」なので、乗り換え検索のときは駅名をよく確かめてくださいね。",
    ))

    # --- 料金
    B.append(h2("ラウールと同じ陶芸体験をするには？料金と予約方法"))
    B.append(keybox([
        ("体験", "電動ろくろ／手びねり"),
        ("料金", "体験料3,000円〜（予約サイト・時期で変動）＋焼成・お渡し代"),
        ("予約", "じゃらん・アソビュー・公式サイトから"),
    ]))
    B.append(p(
        "ラウールさんと同じように大きな器を作りたいなら、電動ろくろのプランがおすすめです。",
        "予約サイトに出ている主な料金は次のとおりです（2026年11月時点）。",
    ))
    B.append(table([
        ["プラン・項目", "料金・内容"],
        ["電動ろくろ体験", "じゃらん：3,000円〜<br>アソビュー：4,000円〜（通常5,500円）"],
        ["手びねり体験", "アソビュー：4,000円〜"],
        ["所要時間", "電動ろくろ約60分＋釉薬の色決め約30分"],
        ["開始時間", "10:30／12:30／14:30／16:30"],
        ["焼成・お渡し（目安）", "豆皿 約1,500円／湯呑み 約1,700円／お茶碗・中皿・花瓶 約2,000円"],
        ["その他", "エプロン100円、2個目の追加500円、配送は送料1,500円〜"],
    ]))
    B.append(p(
        "体験料とは別に、作った器を焼いて仕上げる「焼成・お渡し」の料金がかかります。",
        "釉薬の色によって値段が変わることもあるので、色を選ぶときに確認しておきましょう。",
        "焼き上がりまでは時間がかかるため、遠方から来る場合は配送を頼むと安心です。",
    ))
    B.append(h3("聖地巡礼で気をつけたいこと"))
    B.append(checkbox("訪れる前のチェックポイント", [
        "体験は予約制。土日は早めに予約する",
        "最寄りは「赤羽橋駅」（赤羽駅とまちがえない）",
        "店内の撮影は、ほかのお客さんが写らないよう教室に確認してから",
        "ラウールさんの話を聞けるかはスタッフの厚意。無理に頼まない",
        "カフェの営業日・時間は日によって違うのでInstagramやLINEで確認",
    ]))
    B.append(p(
        "私游はラウールさんのファンが来ることを温かく受け入れてくれている教室です。",
        "これからも気持ちよく通える場所であるように、マナーを守って楽しみたいですね。",
    ))

    # --- 理由
    B.append(h2("ラウールが陶芸に挑戦した理由は「食」と「器」への興味"))
    B.append(p(
        "今回の陶芸回は、ラウールさん本人のリクエストから生まれた企画でした。",
        "誌面では「自炊派のラウールが考える“食”と“器”、食事の楽しみ方」がテーマになっていて、料理をよくするラウールさんが、器そのものにも関心を広げていることがうかがえます。",
    ))
    B.append(p(
        "モデルとしても活動し、アートやファッションへの感度が高いラウールさんにとって、手で形を生み出す陶芸は相性のいい趣味なのかもしれません。",
        "「集中して土をいじっていると落ち着く」という言葉からは、忙しい毎日の中で心を整える時間にもなったことが伝わってきます。",
        "今後、自作の器を使った料理の写真などが見られる日が来たら、ファンとしてはうれしいですね。",
    ))

    # --- まとめ
    B.append(h2("まとめ"))
    B.append(checkbox("この記事のまとめ", [
        "ラウールの陶芸回は月刊ザテレビジョン2026年9月号（7月23日発売）のSnowらいふ第196回",
        "撮影は本人のリクエストで、初めての陶芸に挑戦",
        "陶芸教室は名前非公表だが、店内の特徴から赤羽橋の「陶芸 gallery cafe 私游」が有力",
        "私游は赤羽橋駅のすぐ裏で、電動ろくろ体験は3,000円〜",
        "体験料のほかに焼成・お渡し代がかかる",
    ]))
    B.append(p(
        "ラウールさんと同じ教室で、同じように土に触れてみるのは、ファンならではの特別な聖地巡礼になりそうです。",
        "自分だけの器ができあがったら、ラウールさんのように笑顔で写真を撮ってみるのも楽しいですね！",
    ))
    B.append(related([
        ("ラウールの私物時計はカルティエのタンク マスト？モデルと値段", f"{SITE}/raul-cartier-tank-must-watch-497"),
        ("ラウールの「たぎる」とは？それスノで流行語になった言葉", f"{SITE}/raul-soresno-tagiru-78"),
    ]))
    return "".join(B)


def auth_headers():
    auth = base64.b64encode(f"{ENV['WP_CHOMO2_USERNAME']}:{ENV['WP_CHOMO2_APP_PASSWORD']}".encode()).decode()
    return {"Authorization": f"Basic {auth}"}


def upload(url, h, path, ctype):
    r = requests.post(f"{url}/wp-json/wp/v2/media", headers={**h, "Content-Type": ctype,
                      "Content-Disposition": f'attachment; filename="{path.name}"'},
                      data=path.read_bytes(), timeout=120)
    r.raise_for_status()
    return r.json()


def post():
    url = ENV["WP_CHOMO2_URL"].rstrip("/")
    h = auth_headers()
    if not PHOTO_PATH.exists():
        PHOTO_PATH.write_bytes(requests.get(PHOTO_URL, timeout=60).content)
    m = upload(url, h, PHOTO_PATH, "image/jpeg")
    sizes = m.get("media_details", {}).get("sizes", {})
    img = (sizes.get("medium_large") or sizes.get("large") or sizes.get("full") or {}).get("source_url", m["source_url"])
    content = HTML_PATH.read_text(encoding="utf-8").replace("{{IMG:official}}", img)
    payload = {"title": TITLE, "slug": SLUG, "content": content, "status": "draft",
               "categories": CATEGORIES, "author": AUTHOR}
    if EYECATCH_PATH.exists():
        payload["featured_media"] = upload(url, h, EYECATCH_PATH, "image/jpeg")["id"]
    r = requests.post(f"{url}/wp-json/wp/v2/posts", headers={**h, "Content-Type": "application/json"},
                      json=payload, timeout=60)
    r.raise_for_status()
    d = r.json()
    print("POST_ID", d["id"], "STATUS", d["status"], "PHOTO", m["id"], "EYECATCH", payload.get("featured_media"),
          "LINK", f"{url}/?p={d['id']}")


if __name__ == "__main__":
    if sys.argv[1] == "build":
        HTML_PATH.parent.mkdir(exist_ok=True)
        HTML_PATH.write_text(build(), encoding="utf-8")
        print("wrote", HTML_PATH)
    else:
        post()
