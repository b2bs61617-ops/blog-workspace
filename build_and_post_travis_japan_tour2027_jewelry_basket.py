# -*- coding: utf-8 -*-
# chomoand-4.blog: Travis Japan Concert Tour 2027「Jewelry Basket」の会場・日程(2026-10-28 発表)
import json, base64, os, sys, subprocess
from pathlib import Path
import requests

ROOT = Path(__file__).parent


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

IMG_DIR = ROOT / "images" / "tj_tour2027"
SCHEDULE_IMG = IMG_DIR / "travis-japan-tour-2027-jewelry-basket-schedule.png"
EYECATCH = IMG_DIR / "tj_tour2027_eyecatch_canva.jpg"
STATE = IMG_DIR / "_state.json"
DRY = "--dry" in sys.argv

TITLE = "トラジャ2027ツアー『Jewelry Basket』の会場・日程は？"
SLUG = "travis-japan-2027-tour-jewelry-basket-schedule"
LIVE_URL = "https://www.youtube.com/watch?v=GDUJdc_ytzo"
SITE = "https://chomoand-4.blog/"
EVENT_URL = "https://www.universal-music.co.jp/travisjapan/news/2026-10-28/"
EVENT_ROWS = [
    ("イベント名", "Travis Japan 'Jewelry Basket' 発売記念イベント"),
    ("日程", "2027年1月20日(水)大阪府内某所・1月27日(水)神奈川県内某所(各日 昼の部・夜の部)"),
    ("内容", "スペシャルライブ・トーク・お見送り会"),
    ("当選人数", "全体で約7,000名"),
]

# グループ記事なので紫
ACC = "#7e57c2"
BORDER = "#d9cdf0"
BG = "#f5f2fb"


def p(sentences):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(sentences) + "</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def mark(text):
    return f'<strong><span class="swl-marker mark_yellow">{text}</span></strong>'


def whatbox(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(rows):
    lines = "\n".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
        for i, (k, v) in enumerate(rows))
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{lines}
</div>''')


def table2(header, rows):
    th = "".join(f"<th>{c}</th>" for c in header)
    trs = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><thead><tr>{th}</tr></thead><tbody>
{trs}
</tbody></table></figure>
<!-- /wp:table -->'''


def checklist(title, items):
    lis = "\n".join(
        f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {ACC};border-radius:3px;color:{ACC};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{i}</p>'
        for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">{title}</p>
<div style="padding:14px 18px;background:{BG};">
{lis}
</div>
</div>''')


def related(items):
    lis = "\n".join(f'<li style="margin:0 0 6px 0;"><a href="{SITE}{s}">{t}</a></li>' for t, s in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACC};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


def image(media, alt, caption):
    return f'''<!-- wp:image {{"id":{media["id"]},"sizeSlug":"full"}} -->
<figure class="wp-block-image size-full"><img src="{media["url"]}" alt="{alt}" class="wp-image-{media["id"]}"/><figcaption style="font-size:0.8em;color:#888;">{caption}</figcaption></figure>
<!-- /wp:image -->'''


def youtube(url):
    return f'''<!-- wp:embed {{"url":"{url}","type":"video","providerNameSlug":"youtube","responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->
<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">
{url}
</div></figure>
<!-- /wp:embed -->'''


def gmap(q):
    from urllib.parse import quote
    return wphtml(f'<iframe src="https://maps.google.com/maps?q={quote(q)}&t=&z=15&ie=UTF8&iwloc=&output=embed" width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>')


def build(sched_media):
    b = []
    b.append(p([
        "Travis Japanの次のツアーがついに発表されました！",
        f"2026年10月28日のデビュー4周年記念の生配信で、{mark('「Travis Japan Concert Tour 2027『Jewelry Basket』」')}の開催が明らかになっています。",
        f"初日は{mark('2027年1月4日(月)の横浜アリーナ')}で、5月23日(日)の静岡・エコパアリーナまで全国8会場を回ります。",
        "さらに1月には、大阪と神奈川でアルバムの発売記念イベントが開かれることも決まりました。",
        "この記事では、発表された日程と会場の一覧に加えて、発売記念イベントの応募方法、過去のツアーとの違いや会場ごとのポイント、ファンクラブ受付の見通しをまとめました。",
    ]))
    b.append(whatbox([
        "2027年ツアー「Jewelry Basket」の日程と会場一覧",
        "ツアーが発表されたタイミング",
        "1月の発売記念イベントの日程と応募方法",
        "過去3年のツアーとの違い",
        "会場ごとのポイント(2年ぶり・改修明けの会場など)",
        "ファンクラブ受付はいつから始まりそうか",
        "初日・横浜アリーナへのアクセス",
    ]))

    # ---- schedule ----
    b.append(h2("トラジャ2027ツアー「Jewelry Basket」の日程と会場は？"))
    b.append(minibox([
        ("ツアー名", "Travis Japan Concert Tour 2027「Jewelry Basket」"),
        ("期間", "2027年1月4日(月)〜5月23日(日)"),
        ("会場", "全国8会場・計19日間"),
        ("発表", "2026年10月28日 デビュー4周年記念YouTube生配信"),
    ]))
    b.append(p([
        "発表されたツアーの日程は、次のとおりです。",
    ]))
    b.append(image(sched_media, "Travis Japan Concert Tour 2027 Jewelry Basket ツアー日程",
                   f"出典:{LIVE_URL}"))
    b.append(table2(
        ["日程", "地域", "会場"],
        [
            ["1/4(月)〜1/7(木)", "神奈川", "横浜アリーナ"],
            ["1/16(土)〜1/17(日)", "宮城", "セキスイハイムスーパーアリーナ"],
            ["2/13(土)〜2/14(日)", "福岡", "マリンメッセ福岡A館"],
            ["2/20(土)〜2/21(日)", "愛知", "Aichi Sky Expo(愛知県国際展示場)Aホール"],
            ["3/26(金)〜3/28(日)", "千葉", "ららアリーナ 東京ベイ"],
            ["4/3(土)〜4/4(日)", "北海道", "真駒内セキスイハイムアイスアリーナ"],
            ["5/1(土)〜5/2(日)", "大阪", "大阪城ホール"],
            ["5/22(土)〜5/23(日)", "静岡", "エコパアリーナ"],
        ],
    ))
    b.append(p([
        "ツアー名は、11月18日に発売される4thアルバムと同じ「Jewelry Basket」です。",
        "これまでのツアーと同じように、新しいアルバムを引っ提げて全国を回るツアーになります。",
        f"横浜アリーナの4日間と千葉の3日間をのぞくと、{mark('ほとんどの会場が土日の2日間')}になっているのも特徴です。",
        "平日に休みを取りにくい人でも、遠征の予定を立てやすい日程といえるでしょう。",
        "なお、各日の公演数や開演時間は、10月28日の発表の時点ではまだ明らかになっていません。",
    ]))

    # ---- announcement ----
    b.append(h2("ツアーはいつ発表された？デビュー4周年の生配信で解禁"))
    b.append(minibox([
        ("発表日", "2026年10月28日(水)"),
        ("発表の場", "公式YouTube「【Travis Japan】4th Anniversary YouTube LIVE」(21時〜)"),
    ]))
    b.append(p([
        "10月28日は、Travis Japanが2022年に世界デビューした記念日です。",
        "4周年を迎えたこの日の21時から公式YouTubeで生配信が行われ、その中で2027年のツアー開催が発表されました。",
        "2023年・2024年・2025年もツアーの発表はデビュー記念日の10月28日だったので、4年続けてこの日にツアーが告知されたことになります。",
        "配信ではアルバム「Jewelry Basket」の裏話なども語られ、記念日らしいにぎやかな時間になりました。",
    ]))
    b.append(youtube(LIVE_URL))
    b.append(p([
        "配信のアーカイブは公式YouTubeチャンネルで見ることができます。",
        "ツアー発表の場面を見逃した人は、チェックしてみてください。",
    ]))

    # ---- release event ----
    b.append(h2("1月にはアルバムの発売記念イベントも！大阪・神奈川で2都市4公演"))
    b.append(minibox(EVENT_ROWS))
    b.append(p([
        "同じ生配信では、ツアーとは別に「Travis Japan 'Jewelry Basket' 発売記念イベント」の開催も発表されました。",
        f"{mark('1月20日(水)に大阪府内、1月27日(水)に神奈川県内')}で、それぞれ昼の部・夜の部の2回ずつ、合わせて2都市4公演が行われます。",
        "会場はどちらも「某所」とされていて、集合時間や会場は当選した人にだけ知らされます。",
    ]))
    b.append(p([
        "イベントでは、スペシャルライブとトークのほか、終わったあとにメンバーが参加者を見送る「お見送り会」も予定されています。",
        "当選人数は全体でおよそ7,000名と発表されています。",
        "ツアーでは1月17日の宮城公演と2月13日の福岡公演の間が空いていますが、イベントはちょうどその間の日程です。",
    ]))
    b.append(h3("応募方法は？アルバムに入っている応募券で申し込む"))
    b.append(table2(
        ["対象商品", "品番", "価格(税込)"],
        [
            ["初回盤T(CD+Blu-ray)", "UPCC-9026", "4,480円"],
            ["初回盤T(CD+DVD)", "UPCC-9027", "3,980円"],
            ["初回盤J(CD+Blu-ray)", "UPCC-9028", "4,480円"],
            ["初回盤J(CD+DVD)", "UPCC-9029", "3,980円"],
            ["通常盤(初回プレス・CDのみ)", "UPCC-9030", "3,300円"],
            ["FC限定盤(CD+Blu-ray)", "PROJ-1942", "5,480円"],
            ["FC限定盤(CD+DVD)", "PROJ-1943", "4,980円"],
        ],
    ))
    b.append(p([
        f"応募券は、11月18日発売の4thアルバム「Jewelry Basket」の{mark('全7形態に1枚ずつ')}封入されています。",
        "応募券のQRコードを読み込むと応募サイトに進み、そこでもらえるシリアルナンバーを使って申し込む流れです。",
        "シリアルナンバーは1回しか使えませんが、応募券を何枚使うかに制限はなく、同じ公演に何口も申し込んだり、別の会場・回に申し込んだりすることもできます。",
        "3形態セットで買えば、そのぶん3口応募できることになります。",
    ]))
    b.append(minibox([
        ("応募期間", "2026年11月17日(火)〜11月29日(日)23:59"),
        ("当選発表", "2026年12月23日(水)12:00予定"),
        ("当日の注意", "当選した本人のみ・顔写真付きの公的身分証の原本が必要"),
    ]))
    b.append(p([
        "当日は当選した本人しか入場できず、同行者の申し込みもできません。",
        "スタンディングエリアか座席エリアかはランダムで決まり、選ぶことはできないとされています。",
        "応募券やシリアルナンバーの再発行・譲渡はできないので、届いたアルバムの応募券はなくさないようにしまっておきましょう。",
        f'詳しくは<a href="{EVENT_URL}">ユニバーサルミュージックの公式ニュース</a>で確認できます。',
        '店舗ごとの予約特典は<a href="https://chomoand-4.blog/jewelry-basket-where-can-i-buy-922">【Jewelry Basket】特典どこで買う？チャーム8色は店舗別！</a>で紹介しています。',
    ]))

    # ---- comparison ----
    b.append(h2("過去のツアーと比べると？4年連続で1月4日の横アリから開幕"))
    b.append(table2(
        ["ツアー", "初日", "最終公演の会場", "会場数"],
        [
            ["2024 Road to Authenticity", "1/4 横浜アリーナ", "真駒内(3/23〜24)", "8会場"],
            ["2025 VIIsual", "1/4 横浜アリーナ", "ららアリーナ(6/7〜8)", "8会場"],
            ["2026 's travelers", "1/4 横浜アリーナ", "ららアリーナ(5/22〜24)", "8会場"],
            ["2027 Jewelry Basket", "1/4 横浜アリーナ", "エコパアリーナ(5/22〜23)", "8会場"],
        ],
    ))
    b.append(p([
        f"今回もツアーの初日は1月4日の横浜アリーナで、{mark('2024年から4年続けて「1月4日・横アリ」スタート')}となりました。",
        "2025年・2026年と同じく、横浜アリーナは1月4日〜7日の4日間です。",
        "8会場を回る形もこれまでと変わりません。",
    ]))
    b.append(p([
        "一方で、大きく変わったのが最終公演の会場です。",
        "2025年・2026年はどちらも千葉のららアリーナ東京ベイで千秋楽を迎えていましたが、今回のららアリーナは3月で、最後は静岡のエコパアリーナになりました。",
        "エコパアリーナは2024年から毎年使われている会場ですが、千秋楽になるのは今回が初めてです。",
    ]))

    # ---- venues ----
    b.append(h2("会場ごとのポイントは？"))
    b.append(p([
        "8会場の中には、毎年おなじみの会場もあれば、久しぶりに帰ってくる会場もあります。",
        "過去3年のツアーと見比べながら、会場ごとのポイントを見ていきましょう。",
    ]))
    b.append(table2(
        ["会場", "2024年", "2025年", "2026年", "2027年"],
        [
            ["横浜アリーナ", "○", "○", "○", "○"],
            ["マリンメッセ福岡A館", "○", "○", "○", "○"],
            ["エコパアリーナ", "○", "○", "○", "○(千秋楽)"],
            ["大阪城ホール", "○", "○", "○", "○"],
            ["ららアリーナ 東京ベイ", "―", "○", "○", "○"],
            ["セキスイハイムスーパーアリーナ", "○", "○", "―", "○"],
            ["真駒内アイスアリーナ", "○", "○", "―", "○"],
            ["Aichi Sky Expo", "―", "○", "―", "○"],
            ["日本ガイシホール(現・クロコくんホール)", "○", "―", "○", "―"],
            ["北海きたえーる", "―", "―", "○", "―"],
            ["朱鷺メッセ", "○", "―", "―", "―"],
            ["サンドーム福井", "―", "―", "○", "―"],
        ],
    ))
    b.append(p([
        f"横浜アリーナ・マリンメッセ福岡・エコパアリーナ・大阪城ホールの4会場は、{mark('4年連続')}でツアーに入っています。",
        "反対に、2026年に回った北海きたえーる・サンドーム福井・名古屋のガイシホール(現・クロコくんホール)は今回入っていません。",
    ]))
    b.append(h3("宮城・セキスイハイムスーパーアリーナは2年ぶり"))
    b.append(p([
        "宮城公演は1月16日(土)・17日(日)で、横浜アリーナの次の2カ所目になります。",
        "2026年のツアーには宮城公演がなかったので、セキスイハイムスーパーアリーナに来るのは2025年の「VIIsual」以来2年ぶりです。",
        "1月の東北は雪が心配な時期なので、遠征する人は交通機関の運行情報もこまめに確認しておくと安心です。",
    ]))
    b.append(h3("愛知は2025年以来のAichi Sky Expo"))
    b.append(p([
        "愛知公演の会場は、常滑市にあるAichi Sky Expo(愛知県国際展示場)のAホールです。",
        "2026年は名古屋市内のガイシホールでしたが、今回は2025年の「VIIsual」以来、2年ぶりにAichi Sky Expoに戻ってきます。",
        "中部国際空港(セントレア)のすぐそばにある会場なので、飛行機での遠征がしやすい反面、名古屋駅からは名鉄で30分ほどかかる点は覚えておきたいところです。",
    ]))
    b.append(h3("真駒内は改修工事明けの4月に開催"))
    b.append(p([
        "北海道公演は、2024年・2025年に使った真駒内セキスイハイムアイスアリーナに戻ってきました。",
        "真駒内は2026年11月中旬から2027年3月中旬まで改修工事が予定されていて、4月3日(土)・4日(日)はその工事が終わったあとの日程です。",
        "2026年に使った北海きたえーるではなく、2年ぶりに真駒内での開催になります。",
    ]))
    b.append(h3("大阪城ホールは休館明けのゴールデンウィーク"))
    b.append(p([
        "大阪城ホールは、2027年1月12日から3月10日まで改修工事で休館することが発表されています。",
        "今回の大阪公演は5月1日(土)・2日(日)で、休館が明けたあとのゴールデンウィークに入りました。",
        "大阪公演がGWになるのは、5月4日〜6日に開催した2025年以来です。",
        "連休中は新幹線や大阪市内のホテルが混みやすいので、早めの予約がおすすめです。",
    ]))
    b.append(h3("ららアリーナ東京ベイは3日間、千秋楽は初のエコパ"))
    b.append(p([
        "千葉のららアリーナ東京ベイは3月26日(金)〜28日(日)の3日間で、横浜アリーナに次いで日数の多い会場です。",
        "2025年・2026年はツアーの最後を飾った会場ですが、今回はツアーの中盤での開催となりました。",
        "そして千秋楽は、5月22日(土)・23日(日)の静岡・エコパアリーナです。",
        "エコパアリーナは最寄りの愛野駅から歩いて15分ほどの場所にあり、終演後の駅はかなり混み合います。",
        "千秋楽に遠征する人は、帰りの電車の時間に余裕を持たせておきましょう。",
    ]))

    # ---- prediction ----
    b.append(h2("会場予想は当たった？空き日程からの予想と比べてみた"))
    b.append(p([
        "ちょものTravis Japan情報局では、2026年9月に各会場の空き日程から2027年ツアーの会場を予想していました。",
        "発表された日程と見比べると、次のような結果になりました。",
    ]))
    b.append(table2(
        ["予想", "結果"],
        [
            ["初日は1月4日〜7日ごろの横浜アリーナ", "的中(1/4〜1/7)"],
            ["大阪城ホールは休館明け(3月中旬以降)", "的中(5/1〜2)"],
            ["真駒内は改修明けの3月下旬以降", "的中(4/3〜4)"],
            ["福岡は4月か5月中旬以降", "外れ(2/13〜14)"],
            ["千秋楽は5〜6月のららアリーナ", "外れ(3/26〜28、千秋楽はエコパ)"],
        ],
    ))
    b.append(p([
        "初日の横浜アリーナや、工事が明けてからの大阪城ホール・真駒内は予想どおりでした。",
        "一方で、マリンメッセ福岡は2月、ららアリーナは3月と、予想より早い時期に組まれています。",
        '予想の詳しい中身は<a href="https://chomoand-4.blog/travis-japan-2027-tour-venue-prediction-926">トラジャ2027年ツアーも横アリ初日？会場を空き日程から予想！</a>にまとめています。',
    ]))

    # ---- FC ----
    b.append(h2("ファンクラブ受付はいつから？例年は発表の翌日から約1週間"))
    b.append(minibox([
        ("2027年ツアーの受付", "10月28日の発表時点では未発表"),
        ("2026年ツアーの例", "発表翌日の10/29(水)12:00〜11/4(火)12:00"),
        ("FCの入会費用", "入会金1,000円+年会費4,000円+手数料140円=5,140円"),
    ]))
    b.append(p([
        "ファンクラブ会員向けのチケット受付の日程は、10月28日の発表の時点ではまだ出ていません。",
        "ただ、2026年のツアーでは発表の翌日12時にファンクラブ受付が始まり、締め切りはその6日後でした。",
        f"過去3年を見ても、受付は発表の1〜4日後から始まり、{mark('期間はおよそ1週間')}しかありません。",
        "ファンクラブの申し込みには会員番号が必要なので、まだ入会していない人は早めに手続きを済ませておきましょう。",
        '入会の流れや費用は<a href="https://chomoand-4.blog/travis-japan-fanclub-when-to-join-1643">トラジャのFCはいつ入るのが正解？ツアー発表は毎年10月末！</a>で詳しく紹介しています。',
    ]))
    b.append(p([
        "チケットの価格も、まだ発表されていません。",
        "参考までに、2025年の「VIIsual」はファンクラブ価格が9,500円、一般価格が10,000円(いずれも税込)でした。",
        "受付日程や価格が発表されたら、この記事にも追記していきます。",
    ]))

    # ---- album ----
    b.append(h2("ツアーのもとになるアルバム「Jewelry Basket」とは？"))
    b.append(p([
        "ツアーと同じタイトルの4thアルバム「Jewelry Basket」は、2026年11月18日(水)に発売されます。",
        "アルバムのプロデュースを担当したのは吉澤閑也で、テーマは「王道アイドルエンターテインメント」です。",
        "7人を宝石に見立ててバスケットに集めるというコンセプトで、ツアーでもそのキラキラした世界観がどう表現されるのか楽しみにしているファンは多そうです。",
    ]))
    b.append(p([
        "これまでのツアーは、2024年が川島如恵留、2025年が中村海人、2026年が松倉海斗と、毎年違うメンバーが演出やプロデュースを担ってきました。",
        "2027年のツアーの演出を誰が担当するのかは、10月28日の時点ではまだ発表されていません。",
        '歴代のプロデュースの流れは<a href="https://chomoand-4.blog/is-toraja-concert-produced-by-214">トラジャのアルバム・コンサートは毎年違うメンバーがプロデュース？</a>でまとめています。',
    ]))
    b.append(p([
        "ツアーまでにアルバムを聴き込んでおきたい人は、予約特典もチェックしておきましょう。",
        '店舗ごとに色の違うチャームがもらえる特典については、<a href="https://chomoand-4.blog/jewelry-basket-where-can-i-buy-922">【Jewelry Basket】特典どこで買う？チャーム8色は店舗別！</a>で紹介しています。',
    ]))

    # ---- access ----
    b.append(h2("初日・横浜アリーナへのアクセスは？"))
    b.append(minibox([
        ("住所", "神奈川県横浜市港北区新横浜3-10"),
        ("最寄り駅", "新横浜駅(JR・新幹線・地下鉄ブルーライン・相鉄・東急)"),
        ("駐車場", "なし(車での来場は控えるよう案内あり)"),
    ]))
    b.append(p([
        "ツアー初日の横浜アリーナは、新横浜駅から歩いて5分ほどの場所にあります。",
        "地下鉄ブルーライン・相鉄・東急は出口7・8から、JR横浜線は北口から、東海道新幹線は東口から向かうのが近道です。",
        "会場には駐車場がないので、電車で向かうようにしましょう。",
        "今回の横アリ公演は1月4日(月)〜7日(木)と平日にかかるため、仕事帰りに向かう人は開演時間が発表されたら移動時間も確認しておくと安心です。",
    ]))
    b.append(gmap("横浜アリーナ"))

    # ---- matome ----
    b.append(h2("まとめ"))
    b.append(checklist("この記事のポイント", [
        "Travis Japan Concert Tour 2027「Jewelry Basket」は2027年1月4日〜5月23日の全国8会場",
        "発表は2026年10月28日、デビュー4周年記念のYouTube生配信",
        "1/20大阪・1/27神奈川で発売記念イベント(応募はアルバムの応募券、11/17〜11/29)",
        "初日は4年連続で1月4日の横浜アリーナ、千秋楽は初めてエコパアリーナ",
        "宮城・愛知(Aichi Sky Expo)・真駒内は2年ぶり、大阪城ホールは休館明けのGW",
        "ファンクラブ受付・チケット価格は発表待ち(2026年ツアーは発表翌日から約1週間)",
        "ツアーのもとになる4thアルバム「Jewelry Basket」は11月18日発売",
    ]))
    b.append(p([
        "4年連続の横アリ開幕で、2027年もTravis Japanのお正月はツアーから始まります。",
        "受付日程などの続報が出たら、この記事でもお知らせしていきます！",
    ]))
    b.append(related([
        ("トラジャ2027年ツアーも横アリ初日？会場を空き日程から予想！", "travis-japan-2027-tour-venue-prediction-926"),
        ("トラジャのFCはいつ入るのが正解？ツアー発表は毎年10月末！", "travis-japan-fanclub-when-to-join-1643"),
        ("トラジャのアルバム・コンサートは毎年違うメンバーがプロデュース？", "is-toraja-concert-produced-by-214"),
        ("【Jewelry Basket】特典どこで買う？チャーム8色は店舗別！", "jewelry-basket-where-can-i-buy-922"),
    ]))
    return "\n\n".join(b)


def upload_media(path, title, alt=""):
    ctype = "image/png" if path.suffix == ".png" else "image/jpeg"
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers={
        **HEADERS_AUTH, "Content-Disposition": f'attachment; filename="{path.name}"', "Content-Type": ctype},
        data=path.read_bytes())
    r.raise_for_status()
    m = r.json()
    if alt:
        requests.post(f"{WP_URL}/wp-json/wp/v2/media/{m['id']}", headers=HJSON, json={"alt_text": alt, "title": title})
    return {"id": m["id"], "url": m["source_url"]}


def main():
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    if DRY:
        html = build({"id": 0, "url": "DRY"})
        (IMG_DIR / "_dry.html").write_text(html, encoding="utf-8")
        print("dry chars:", len(html))
        return
    if "sched" not in state:
        state["sched"] = upload_media(SCHEDULE_IMG, "Travis Japan Concert Tour 2027 Jewelry Basket 日程",
                                      "Travis Japan Concert Tour 2027 Jewelry Basket ツアー日程")
        STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    html = build(state["sched"])
    tmp = IMG_DIR / "_post.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis", str(tmp)], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "check", "--group", "travis", str(tmp)], check=True)
    html = tmp.read_text(encoding="utf-8")
    if not EYECATCH.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
                        "--main", "2027ツアー", "--bottom", "Jewelry Basketの会場は？",
                        "--bottom", "1/4横アリから全8会場！", "--color-key", "group", "--out", str(EYECATCH)], check=True)
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
