# -*- coding: utf-8 -*-
# anan AWARD 2026(11/14 13:30〜 anan公式YouTube無料生配信)にSixTONES・KEY TO LITが登壇決定
# 2026-11-07 オシリ依頼(元ネタ: オリコン 11/6配信「SixTONES＆KEY TO LIT、『anan AWARD 2026』登壇が決定」)
# chomoand-0.com(SixTONES目線) と chomoand-5.site(KEY TO LIT目線) に1本ずつ下書き
# 出典: ananweb.jp/award(公式: START 13:30 / CLOSE 15:00、配信URL youtube.com/live/FZCoDW52xXA)
#       PR TIMES 000000705.000030125(第1弾出演者・過去受賞者・2026年は13:00〜15:00予定と記載)
#       THE FIRST TIMES 0000914200 / 音楽ナタリー(Yahoo b20dbf71…) / モデルプレス(Yahoo 1b7b709f…)
#       2020年の授賞式: モデルプレス 2296811 等、マイナビ 20201109-1470919
# 使い方: python build_and_post_anan_award_2026.py [sixtones|ktl|all] [--dry]
import json, base64, os, sys, subprocess
from pathlib import Path
import requests

ROOT = Path(__file__).parent
DRY = "--dry" in sys.argv
IMG_DIR = ROOT / "images" / "anan_award_2026"
LIVE_ID = "FZCoDW52xXA"
OFFICIAL = "https://ananweb.jp/award"
YT_CH = "https://www.youtube.com/@anan_magazine"
OTHER_NAMES = "黒柳徹子,永島優美,小田切ヒロ,長谷川あかり,髙石あかり,上田綺世,坂井瑠星,今田美桜,岡田准一,山田涼介,菊池風磨,渡辺翔太,大橋和也,ラウール,岩本照"


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}

SITES = {
    "sixtones": dict(key="AUDITION", site="https://chomoand-0.com/", group="sixtones", cats=[15],
                     acc="#6a8caf", border="#cddbe9", bg="#eef3f8"),
    "ktl": dict(key="CHOMO5", site="https://chomoand-5.site/", group="ktl", cats=[4],
                acc="#3d5a80", border="#c9d6e6", bg="#eef3f8"),
}
C = {}


def p(*sentences):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(sentences) + "</p>\n<!-- /wp:paragraph -->"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def mark(t):
    return f'<strong><span class="swl-marker mark_yellow">{t}</span></strong>'


def link(url, t):
    return f'<a href="{url}" target="_blank" rel="noopener">{t}</a>'


def ilink(slug, t):
    return f'<a href="{C["site"]}{slug}">{t}</a>'


def whatbox(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {C["border"]};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{C["acc"]};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{C["bg"]};">
{lis}
</ul>
</div>''')


def minibox(rows):
    lines = "\n".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
        for i, (k, v) in enumerate(rows))
    return wphtml(f'''<div style="border:1px solid {C["border"]};border-left:4px solid {C["acc"]};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{C["bg"]};">
{lines}
</div>''')


def table(header, rows):
    th = "".join(f'<td style="background:{C["acc"]};color:#fff;font-weight:bold;border:1px solid {C["border"]};">{c}</td>' for c in header)
    trs = []
    for i, r in enumerate(rows):
        bg = "#fff" if i % 2 == 0 else C["bg"]
        trs.append("<tr>" + "".join(f'<td style="background:{bg};border:1px solid {C["border"]};">{c}</td>' for c in r) + "</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n'
            f"<tr>{th}</tr>\n" + "\n".join(trs) + "\n</tbody></table></figure>\n<!-- /wp:table -->")


def checklist(title, items):
    lis = "\n".join(
        f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {C["acc"]};border-radius:3px;color:{C["acc"]};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{i}</p>'
        for i in items)
    return wphtml(f'''<div style="border:1px solid {C["border"]};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{C["acc"]};color:#fff;">{title}</p>
<div style="padding:14px 18px;background:{C["bg"]};">
{lis}
</div>
</div>''')


def personbox(name, *sentences):
    body = "<br>\n".join(sentences)
    return wphtml(f'''<div style="border:1px solid {C["border"]};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;color:{C["acc"]};">{name}</p>
<p style="margin:0;">{body}</p>
</div>''')


def related(items):
    lis = "\n".join(f'<li style="margin:0 0 6px 0;"><a href="{u if u.startswith("http") else C["site"] + u}">{t}</a></li>' for t, u in items)
    return wphtml(f'''<div style="border:1px solid {C["border"]};border-left:4px solid {C["acc"]};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{C["bg"]};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


def yt_embed():
    return wphtml(f'''<figure style="margin:0 0 16px 0;">
<div style="position:relative;width:100%;padding-top:56.25%;">
<iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://www.youtube.com/embed/{LIVE_ID}" title="anan AWARD 2026 授賞式 生配信" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
<figcaption style="text-align:center;font-size:12px;color:#888;">出典:anan公式YouTubeチャンネル(配信ページ)</figcaption>
</figure>''')


def event_section():
    return [
        h2("anan AWARD 2026はいつ？配信は何時から？"),
        minibox([("日時", "2026年11月14日(土)13:30〜15:00(公式サイトの表記)"),
                 ("配信", "anan公式YouTubeチャンネル(@anan_magazine)で生配信"),
                 ("料金", "無料(会員登録・チケット不要)"),
                 ("ハッシュタグ", "#ananAWARD2026")]),
        p("授賞式は会場に観客を入れて見に行くタイプではなく、オンラインの生配信で見るスタイルです。",
          f"配信はanan公式YouTubeチャンネルで、{mark('誰でも無料で視聴できます')}。",
          "YouTubeのアカウントがなくても再生はできるので、スマホ1台あればOKです。"),
        p("時間について、ひとつだけ注意点があります。",
          f"10月に出たプレスリリースでは「13:00〜15:00(予定)」となっていましたが、{link(OFFICIAL, '公式サイト')}のカウントダウンでは「START 13:30」と表示されています。",
          "最新の公式表記は13:30開始なので、13時ごろには配信ページを開いて待っておくと、どちらでも見逃さずに済みます。"),
        p("配信ページはすでに公開されていて、下の画面からそのまま再生できます。",
          "「通知を受け取る」を押しておくと、配信が始まったときにYouTubeからお知らせが届きます。"),
        yt_embed(),
        p("アーカイブ(あとから見返せる録画)が残るかどうかは、11月7日時点で公式に案内がありません。",
          "残らなかった場合に備えて、推しの登壇シーンはリアルタイムで見ておくのがいちばん安心です。"),
    ]


def about_section():
    return [
        h2("anan AWARDってどんな賞？"),
        minibox([("主催", "マガジンハウス(雑誌『anan』)"),
                 ("始まり", "2020年(『anan』創刊50周年の年)"),
                 ("トロフィー", "金のananパンダ")]),
        p("『anan』は1970年創刊の女性向け週刊誌で、2025年に55周年を迎えました。",
          "anan AWARDは創刊50周年の2020年に立ち上がったアワードで、その年のムーブメントの先駆けになった人や、時代を象徴する人・モノ・コトを「時代の顔」として表彰します。",
          "受賞者には、ananのマスコットでおなじみのパンダをかたどった「金のananパンダトロフィー」が贈られます。"),
        p("2026年で7回目の開催です。",
          "開会宣言は今年も黒柳徹子さんが特別映像で担当し、これで7年連続になります。",
          "MCはフリーアナウンサーの永島優美さんが務めます。"),
        p("賞の名前(〇〇部門など)と受賞内容は、毎年授賞式の当日に発表される決まりです。",
          "そのため、今の時点でどのグループがどの賞をもらうかは公表されていません。"),
    ]


def winners_table():
    return table(["年", "大賞", "STARTO所属・出身の受賞(大賞以外)"], [
        ["2020", "SixTONES・Snow Man", "-"],
        ["2021", "岡田准一", "ホープ部門 なにわ男子"],
        ["2022", "山田涼介", "チャレンジ部門 Travis Japan"],
        ["2023", "菊池風磨", "エモーショナル部門 Aぇ! group"],
        ["2024", "渡辺翔太", "ドラマティック部門 Aぇ! group"],
        ["2025", "timelesz", "スーパーアイドル部門 大橋和也(なにわ男子)"],
    ])


def cast_section(self_group):
    other = []
    if self_group == "sixtones":
        other.append(personbox("KEY TO LIT(キテレツ)",
                               "岩﨑大昇さん・井上瑞稀さん・中村嶺亜さん・猪狩蒼弥さん・佐々木大光さんの5人組で、2026年12月9日にCDデビューします。",
                               "7月8日発売の『anan』2503号で5人そろって初めて表紙を飾り、発売後すぐに緊急重版になりました。",
                               "なお佐々木大光さんは膝のケガのため、今回の授賞式には出演しません。",
                               f"詳しくは姉妹サイトの{link('https://chomoand-5.site/sasaki-taiko-meniscus-retear-637', '佐々木大光さんの半月板再断裂の記事')}でまとめています。"))
    else:
        other.append(personbox("SixTONES",
                               "ジェシーさん・京本大我さん・松村北斗さん・髙地優吾さん・森本慎太郎さん・田中樹さんの6人組で、2026年でデビュー6周年です。",
                               "グループとして『anan』の表紙を通算14回飾っていて、anan AWARDへの登壇は2020年の第1回(大賞を受賞)以来2度目になります。",
                               "KEY TO LITにとっては、同じ事務所の先輩グループと同じステージに立つ授賞式です。"))
    return [
        h2("一緒に登壇するのは誰？発表済みの出演者"),
        minibox([("登壇", "SixTONES、KEY TO LIT、小田切ヒロさん、長谷川あかりさん、髙石あかりさん"),
                 ("映像出演", "上田綺世さん、坂井瑠星さん、ブラックオニキス(『超かぐや姫！』より)"),
                 ("開会宣言・MC", "黒柳徹子さん(映像)・永島優美さん")]),
        p("出演者は10月15日の第1弾発表と、11月6日の追加発表の2回に分けて公表されました。",
          "第1弾ではヘア＆メイクアップアーティストの小田切ヒロさんと料理家の長谷川あかりさんが発表され、11月6日にSixTONESとKEY TO LITが追加されています。"),
        *other,
        p("ほかに、俳優の髙石あかりさんの登壇も報じられています。",
          "映像出演には、サッカー日本代表の上田綺世さん、騎手の坂井瑠星さん、アニメ『超かぐや姫！』のキャラクター・ブラックオニキスが名を連ねていて、ジャンルを問わず「今年の顔」が集まる顔ぶれです。",
          "出演者は今後さらに追加される可能性もあるので、直前まで公式サイトをチェックしておくと安心です。"),
    ]


def build_sixtones():
    out = [
        p("2026年11月14日(土)に開催される『anan AWARD 2026』に、SixTONESが登壇することが11月6日に発表されました。",
          f"授賞式は{mark('11月14日13:30からanan公式YouTubeで無料生配信')}され、SixTONESがanan AWARDに出るのは{mark('2020年の第1回(大賞受賞)以来2度目')}です。"),
        p("この記事では、配信の時間と見方、anan AWARDがどんな賞なのか、6年前の大賞受賞の思い出、そして今年は何の賞になりそうかを、過去の受賞者の傾向から予想していきます。"),
        whatbox(["配信の日時と見方", "anan AWARDとは", "2020年の大賞受賞", "anan表紙の歴史", "今年の受賞予想", "共演者"]),
        *event_section(),
        *about_section(),
        h2("SixTONESは2度目の登壇！2020年は大賞を受賞"),
        minibox([("前回", "anan AWARD 2020(第1回)"),
                 ("受賞", "大賞(Snow Manと同時受賞)"),
                 ("今回", "6年ぶり2度目の登壇")]),
        p("SixTONESが最初にanan AWARDに登場したのは、アワードが始まった2020年です。",
          "授賞式は2020年11月8日に東京で、イベント「SHIBUYA SCRAMBLE FESTIVAL 2020」の一部として行われました。",
          f"この年、SixTONESは同じ日にCDデビューしたSnow Manと並んで{mark('大賞')}を受賞しています。"),
        p("授賞式にはSixTONESからジェシーさんと田中樹さんが登壇しました。",
          "ジェシーさんは、1月22日のデビューから11月11日発売の3rdシングルまで「あっという間だった」と振り返り、2020年は自分たちの音楽やパフォーマンスをより多くの人に届けられた年だったと話しています。",
          "田中樹さんは「スターとは？」と聞かれて、先輩たちこそスターだとしたうえで、SixTONESの6人もスターになれたらと、願いを込めた言葉を残しました。"),
        p("デビューした年に「時代の顔」として選ばれてから6年がたち、今年はデビュー6周年の節目です。",
          "あのとき「スターになれたら」と話していたグループが、今どんな言葉を語るのかにも注目が集まりそうです。"),
        h2("SixTONESの『anan』表紙は通算14回"),
        minibox([("表紙の回数", "グループとして通算14回(2026年11月時点の報道)"),
                 ("2026年の主な表紙", "新年1号目・結成日号・バディ表紙・映画コラボ")]),
        p("今回の登壇の背景には、SixTONESと『anan』の深いつながりがあります。",
          f"SixTONESはグループとして『anan』の表紙を{mark('通算14回')}飾っていて、そのたびに話題になってきました。",
          "2026年だけでも、6人そろっての表紙からメンバーのペア表紙まで、何度も登場しています。"),
        table(["号", "発売日", "表紙の内容"], [
            ["2478号", "1月7日", "新年1号目の表紙(新年1号目は4回目)"],
            ["2494号", "5月1日", "結成日に発売の6周年イヤー記念表紙"],
            ["2509号", "8月26日", "髙地優吾×森本慎太郎のバディ表紙(第7弾)"],
            ["2510号", "9月2日", "松村北斗×今田美桜(映画『白鳥とコウモリ』)"],
        ]),
        p("とくに5月1日の2494号は、SixTONESの結成日にあわせた記念号でした。",
          "メンバー2人ずつが登場する「バディ表紙」もシリーズとして続いていて、8月の髙地優吾さんと森本慎太郎さんの回で第7弾になります。",
          "これだけ表紙を重ねてきたグループだからこそ、アワードの舞台にもう一度呼ばれたと考えると納得感があります。"),
        h2("今年は何の賞？過去の受賞者から予想"),
        minibox([("発表", "受賞名・受賞内容は11月14日の当日発表"),
                 ("傾向", "STARTOのグループ・メンバーは毎年なにかしらの賞を受賞")]),
        p("先にお伝えしたとおり、SixTONESが何の賞を受け取るのかは当日まで公表されません。",
          "ただ、これまでの受賞者を見ると、STARTO ENTERTAINMENT(旧ジャニーズ事務所)のグループやメンバーは毎年のように賞を受けています。"),
        winners_table(),
        p("大賞は2021年以降、岡田准一さん、山田涼介さん、菊池風磨さん、渡辺翔太さん、そして2025年のtimeleszと、毎年STARTOのタレントが選ばれてきました。",
          "部門賞も「チャレンジ」「エモーショナル」「スーパーアイドル」など、その年の活躍ぶりに合わせて名前が毎回変わるのが特徴です。"),
        p("SixTONESは2026年、デビュー6周年イヤーとしてライブツアー「MILESixTONES」を行い、音楽・バラエティ・ドラマ・映画と幅広く活躍してきました。",
          "大賞はすでに2020年に受賞しているので、今年は「6年分の歩み」や「ライブの熱量」を表すような、SixTONESのためだけの新しい部門名が付くかもしれません。",
          "あくまで予想ですが、どんな言葉で「時代の顔」と表されるのかは、当日のいちばんの見どころになりそうです。"),
        p(f"同じ時期には、{ilink('modelpress-kotoshi-no-kao-2026-sixtones', 'モデルプレスの「今年の顔」の投票')}も行われていて、年末に向けてSixTONESの1年をふり返る企画が続きます。"),
        *cast_section("sixtones"),
        h2("当日見逃さないためのポイント"),
        minibox([("準備", "配信ページで「通知を受け取る」をオン"),
                 ("時間", "13時ごろから待機(公式表記は13:30開始)"),
                 ("実況", "#ananAWARD2026 で感想を共有")]),
        p("授賞式は約1時間半で、SixTONESが何時ごろに登場するかの出番順は発表されていません。",
          "登壇者が多いイベントなので、最初から最後まで通して見られるようにしておくと確実です。"),
        p("当日は公式ハッシュタグ「#ananAWARD2026」が使われるので、実況しながら見るのも楽しみ方のひとつです。",
          "anan公式のXやInstagramでは、授賞式の写真やオフショットが当日中に出ることも多いので、配信後もチェックしておきたいところです。",
          "11月14日は土曜日の昼なので、ほかの予定とかぶらないよう早めに時間をあけておきましょう。"),
        h2("まとめ"),
        checklist("anan AWARD 2026 × SixTONESのポイント", [
            "11月14日(土)13:30〜15:00、anan公式YouTubeで無料生配信",
            "SixTONESの登壇は2020年の第1回(大賞)以来2度目",
            "『anan』の表紙はグループ通算14回",
            "受賞名・受賞内容は当日発表",
            "KEY TO LITも登壇(佐々木大光は欠席)",
        ]),
        p("6年前に大賞をもらったときの「スターになれたら」という言葉から、どんな新しい肩書きが付くのか楽しみですね。",
          "当日は配信をつなぎながら、SixTONESの1年をみんなでお祝いしましょう！"),
        related([
            ("モデルプレス今年の顔の投票方法は？締切と発表日も！", "modelpress-kotoshi-no-kao-2026-sixtones"),
            ("SixTONESのテレビ出演は？11/8〜11/14の放送予定まとめ！", "sixtones-tv-schedule-1108-1114"),
            ("MILESixTONESのDVD内容は？初回盤と通常盤の違いは？", "milesixtones-bluray-dvd-contents"),
            ("SixTONESの2026年リーダーは京本大我？毎年変わる理由は？", "sixtones-leader-2026-kyomoto"),
        ]),
    ]
    return "\n\n".join(out)


def build_ktl():
    out = [
        p("2026年11月14日(土)に開催される『anan AWARD 2026』に、KEY TO LIT(キテレツ)が登壇することが11月6日に発表されました。",
          f"授賞式は{mark('11月14日13:30からanan公式YouTubeで無料生配信')}され、KEY TO LITにとっては{mark('anan AWARD初登壇')}です。",
          f"ただし{mark('佐々木大光さんは膝のケガのため出演しません')}。"),
        p("この記事では、配信の時間と見方、anan AWARDがどんな賞なのか、なぜKEY TO LITが選ばれたのか、そして過去の受賞者からデビュー前のグループがどんな賞をもらってきたのかを整理します。"),
        whatbox(["配信の日時と見方", "anan AWARDとは", "選ばれた理由", "佐々木大光の欠席", "今年の受賞予想", "共演者"]),
        *event_section(),
        *about_section(),
        h2("KEY TO LITはなぜ選ばれた？anan表紙の緊急重版"),
        minibox([("初表紙", "『anan』2503号(2026年7月8日発売)"),
                 ("反響", "発売後すぐに売り切れ→緊急重版"),
                 ("デビュー", "2026年12月9日『KEY TERUYA2 ～キテルヤツ～』")]),
        p("KEY TO LITと『anan』の大きな接点は、7月8日発売の2503号です。",
          f"5人そろって初めて『anan』の表紙を飾ったこの号は、ネットでも店頭でもすぐに売り切れ、{mark('緊急重版')}が決まりました。",
          "今回の発表でも「実力派揃いの注目のグループ」と紹介されていて、この表紙の反響が登壇につながったと考えられます。"),
        p("KEY TO LITは2025年2月に結成された5人組で、2026年12月9日にデビューシングル『KEY TERUYA2 ～キテルヤツ～』でCDデビューします。",
          "デビューを1か月後に控えたこの時期に「時代の顔」を表彰する場に呼ばれたことは、グループにとって大きな追い風です。"),
        p(f"『anan』以外にも、デビュー前から雑誌の表紙が続き、売り切れや重版をくり返しています。",
          f"表紙号の一覧は{ilink('key-to-lit-magazine-cover-nov-dec-2026-494', 'キテレツ表紙の雑誌まとめ')}で紹介しています。"),
        h2("佐々木大光は欠席…登壇は4人"),
        minibox([("出演", "岩﨑大昇さん・井上瑞稀さん・中村嶺亜さん・猪狩蒼弥さんの4人"),
                 ("欠席", "佐々木大光さん(膝半月板損傷部分の再断裂)")]),
        p("今回の発表には「佐々木大光は、今回の授賞式には出演しない」という一文が添えられていました。",
          "佐々木大光さんは11月6日、以前ケガをした膝の半月板の損傷部分が再び断裂したと発表されていて、再手術とリハビリに入ります。",
          "ステージなど膝に負担のかかる活動は当面見合わせになっているため、授賞式は4人での登壇になります。"),
        p("5人そろった姿を見たかったファンにとっては残念ですが、膝に影響のない活動は無理のない範囲で続けると案内されています。",
          "授賞式の場で、4人がどんなふうに佐々木さんのことに触れるのかにも注目が集まりそうです。",
          f"ケガの経緯やデビューへの影響は{ilink('sasaki-taiko-meniscus-retear-637', '佐々木大光さんの半月板再断裂の記事')}で詳しくまとめています。"),
        h2("今年は何の賞？デビュー前のグループの受賞例"),
        minibox([("発表", "受賞名・受賞内容は11月14日の当日発表"),
                 ("注目", "デビュー直前・直後のグループが部門賞を受けた例あり")]),
        p("KEY TO LITが何の賞を受け取るのかは、当日まで公表されません。",
          "ただ、これまでの受賞者を見ると、STARTO ENTERTAINMENT(旧ジャニーズ事務所)のグループやメンバーは毎年のように賞を受けています。"),
        winners_table(),
        p("ここで注目したいのが、デビュー前後のグループの受賞です。",
          "2021年の「ホープ部門」を受けたなにわ男子は、その年の11月にCDデビューしたばかりの時期でした。",
          "2023年の「エモーショナル部門」を受けたAぇ! groupは、まだCDデビュー前(デビューは2024年5月)で、翌2024年にも「ドラマティック部門」で2年連続の受賞を果たしています。"),
        p("KEY TO LITも、12月9日のデビューを目前に控えたタイミングでの登壇です。",
          "あくまで予想ですが、なにわ男子の「ホープ」のように、これからの飛躍を期待する意味の部門名が付く可能性がありそうです。",
          "一方で、表紙号の緊急重版という実績もあるので、「話題性」や「勢い」を表す言葉が選ばれるかもしれません。"),
        *cast_section("ktl"),
        h2("当日見逃さないためのポイント"),
        minibox([("準備", "配信ページで「通知を受け取る」をオン"),
                 ("時間", "13時ごろから待機(公式表記は13:30開始)"),
                 ("実況", "#ananAWARD2026 で感想を共有")]),
        p("授賞式は約1時間半で、KEY TO LITが何時ごろに登場するかの出番順は発表されていません。",
          "登壇者が多いイベントなので、最初から最後まで通して見られるようにしておくと確実です。"),
        p("当日は公式ハッシュタグ「#ananAWARD2026」が使われるので、実況しながら見るのも楽しみ方のひとつです。",
          "同じ11月14日の夜には、佐々木大光さんが出演する『いくらかわかる金？』の放送もあります。",
          f"その週のテレビ出演は{ilink('key-to-lit-tv-schedule-1108-1114-582', 'KEY TO LITの11/8〜14の放送予定まとめ')}でチェックできます。"),
        h2("まとめ"),
        checklist("anan AWARD 2026 × KEY TO LITのポイント", [
            "11月14日(土)13:30〜15:00、anan公式YouTubeで無料生配信",
            "KEY TO LITはanan AWARD初登壇",
            "『anan』2503号の初表紙は緊急重版に",
            "佐々木大光はケガのため欠席、登壇は4人",
            "受賞名・受賞内容は当日発表",
        ]),
        p("デビュー前に先輩のSixTONESと同じ授賞式に立てるのは、キテレツにとって忘れられない1日になりそうですね。",
          "当日は配信をつなぎながら、4人の晴れ舞台と、画面の向こうの佐々木さんにもエールを送りましょう！"),
        related([
            ("【佐々木大光】膝の半月板再断裂はなぜ？デビューへの影響や復帰時期は？", "sasaki-taiko-meniscus-retear-637"),
            ("キテレツ表紙の雑誌は？11〜12月発売の9冊と売り切れ情報！", "key-to-lit-magazine-cover-nov-dec-2026-494"),
            ("【KEY TO LIT】テレビ出演は？11/8〜14の放送予定まとめ！", "key-to-lit-tv-schedule-1108-1114-582"),
            ("キテレツの入所日一覧！入所順や年齢、入所のきっかけは？", "key-to-lit-member-join-dates-528"),
        ]),
    ]
    return "\n\n".join(out)


ARTICLES = {
    "sixtones": dict(title="【未】【anan AWARD】SixTONES2度目の登壇！配信は何時から？",
                     slug="anan-award-2026-sixtones", build=build_sixtones,
                     eye=["--main", "anan AWARD", "--bottom", "2度目の登壇決定！", "--bottom", "配信は何時から？",
                          "--color-key", "group"], tool="eyecatch_sixtones.py"),
    "ktl": dict(title="【未】【anan AWARD 2026】キテレツ初登壇！配信は何時から？",
                slug="anan-award-2026-key-to-lit", build=build_ktl,
                eye=["--main", "anan AWARD", "--bottom", "初登壇決定！", "--bottom", "配信は何時から？",
                     "--color-key", "group"], tool="eyecatch_kitetsu.py"),
}


def run(name):
    C.clear()
    C.update(SITES[name])
    a = ARTICLES[name]
    body_title = a["title"].replace("【未】", "")
    assert len(body_title) <= 35, (body_title, len(body_title))
    html = a["build"]()
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = IMG_DIR / f"_{name}.html"
    tmp.write_text(html, encoding="utf-8")
    hon = [sys.executable, str(ROOT / "tools" / "honorific.py")]
    subprocess.run(hon + ["fix", "--group", C["group"], "--names", OTHER_NAMES, str(tmp)], check=True)
    subprocess.run(hon + ["check", "--group", C["group"], "--names", OTHER_NAMES, str(tmp)], check=True)
    html = tmp.read_text(encoding="utf-8")
    import re
    plain = re.sub(r"<!--.*?-->|<[^>]+>", "", html, flags=re.S)
    print(name, "title len", len(body_title), "text chars", len(re.sub(r"\s", "", plain)))
    if DRY:
        return
    k = C["key"]
    base = ENV[f"WP_{k}_URL"].rstrip("/")
    auth = base64.b64encode(f'{ENV[f"WP_{k}_USERNAME"]}:{ENV[f"WP_{k}_APP_PASSWORD"]}'.encode()).decode()
    H = {"Authorization": f"Basic {auth}"}
    state_p = IMG_DIR / f"_{name}_state.json"
    state = json.loads(state_p.read_text(encoding="utf-8")) if state_p.exists() else {}
    eye = IMG_DIR / f"anan_award_2026_{name}_eyecatch.jpg"
    if not eye.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / a["tool"]), *a["eye"], "--out", str(eye)], check=True)
    if "media" not in state:
        r = requests.post(f"{base}/wp-json/wp/v2/media", headers={**H, "Content-Type": "image/jpeg",
                          "Content-Disposition": f'attachment; filename="{eye.name}"'}, data=eye.read_bytes(), timeout=120)
        r.raise_for_status()
        state["media"] = r.json()["id"]
        requests.post(f"{base}/wp-json/wp/v2/media/{state['media']}", headers=H,
                      json={"alt_text": body_title, "title": body_title}, timeout=60)
        state_p.write_text(json.dumps(state), encoding="utf-8")
    body = {"title": a["title"], "slug": a["slug"], "content": html, "status": "draft",
            "categories": C["cats"], "author": 2, "featured_media": state["media"]}
    url = f"{base}/wp-json/wp/v2/posts" + (f"/{state['post_id']}" if "post_id" in state else "")
    r = requests.post(url, headers=H, json=body, timeout=120)
    r.raise_for_status()
    post = r.json()
    state["post_id"] = post["id"]
    state_p.write_text(json.dumps(state), encoding="utf-8")
    print("post", post["id"], post["status"], f"{base}/?p={post['id']}", "media", state["media"])


if __name__ == "__main__":
    which = next((x for x in sys.argv[1:] if not x.startswith("--")), "all")
    for n in (["sixtones", "ktl"] if which == "all" else [which]):
        run(n)
