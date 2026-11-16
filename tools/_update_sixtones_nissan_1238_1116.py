"""SixTONES日産スタジアムの服装記事(chomoand-0.com ID1238)に、ライバル見張り発の情報を足す(2026-11-16、ユカ承認「やっていいよ」)。
足すもの: 気象庁の予報(11/21・22)・日の入り・屋根のある席・開場14:30予定・グッズ整理券の確定情報・
長居の終演/規制退場の実例・生配信・Xの写真2枚・内部リンク・FAQ3つ。タイトル・スラッグは変えない。
材料: articles/sixtones_milesixtones_nissan_1116_research.md
usage: python3 tools/_update_sixtones_nissan_1238_1116.py [--apply]
"""
import os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blogkit  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POST = 1238
EXPECT_REV = 1252  # この版より新しい人の直しがあれば止まる
OUT = os.path.join(REPO, "articles", "sixtones_nissan_1238_update_1116.html")

C = "#4a3b6b"
BD = "#d3cce3"
BG = "#f4f2f9"
MARK = '<strong><span style="font-size:1.1em;background:linear-gradient(transparent 60%,#ddd5ec 60%);">{}</span></strong>'
CHECK = ('<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid #4a3b6b;border-radius:3px;'
         'color:#4a3b6b;font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')
TD = 'style="border:1px solid #d3cce3;padding:8px;"'
TH = 'style="background:#4a3b6b;color:#fff;font-weight:bold;border:1px solid #d3cce3;padding:8px;"'


def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n'


def html(s):
    return "<!-- wp:html -->\n" + s + "\n<!-- /wp:html -->\n\n"


def box(title, items):
    li = "\n".join(f"<li>{i}</li>" for i in items)
    return html(f'<div style="border:1px solid {BD};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                f'<p style="font-weight:bold;margin:0;padding:8px 16px;background:{C};color:#fff;">{title}</p>\n'
                f'<ul style="margin:0;padding:12px 18px 12px 34px;background:{BG};">\n{li}\n</ul>\n</div>')


def voice(t):
    return html(f'<p style="border-left:4px solid {C};padding:10px 16px;margin:0 0 16px 0;background:{BG};">{t}</p>')


def check_line(t):
    return f'<p style="margin:0 0 8px 0;">{CHECK}{t}</p>'


def table(head, rows):
    h = "".join(f"<td {TH}>{x}</td>" for x in head)
    b = "".join("<tr>" + "".join(f"<td {TD}>{x}</td>" for x in r) + "</tr>" for r in rows)
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            f"<tr>{h}</tr>{b}</tbody></table></figure>\n<!-- /wp:table -->\n\n")


def a(url, text):
    return f'<a href="{url}">{text}</a>'


X_KOCHI = "https://x.com/SixTONES_SME/status/2119332762721378714"
X_KYOMOTO = "https://x.com/SixTONES_SME/status/2101577116605456782"
L_SETLIST = "https://chomoand-0.com/sixtones-milesixtones-nissan-setlist-1567"
L_SEAT = "https://chomoand-0.com/sixtones-live-seat-when-1509"
L_BOOTS = "https://chomoand-0.com/sixtones-nagai-atsuzoko-boots-rain-1269"
L_SUITO = "https://chomoand-0.com/matsumura-hokuto-suito-hydroflask-1440"

UPDATE_NOTE = html('<p style="border:1px solid #d3cce3;border-radius:4px;padding:8px 14px;margin:0 0 16px 0;'
                   'background:#fbfafd;font-size:0.9em;">2026年11月16日:最新の天気予報、屋根のある席、'
                   '開場時間の予定、終演と帰りの目安、グッズの整理券の情報を足しました。</p>')

# --- 冒頭 ---
OLD_LEAD1 = "SixTONES初のスタジアムツアー「MILESixTONES」も、残るは大阪と神奈川の4公演です。<br>"
NEW_LEAD1 = ("SixTONES初のスタジアムツアー「MILESixTONES」も、残るは神奈川・日産スタジアムの2公演だけになりました。<br>")
OLD_LEAD3 = "この記事では、日産スタジアム公演の開演時間とアクセス、11月下旬の屋外ライブに合った服装、グッズの買い方をまとめました。</p>"
NEW_LEAD3 = ("この記事では、開演時間とアクセス、当日の気温、屋外ライブの服装、"
             "グッズの買い方、帰りの目安までまとめました。</p>\n<!-- /wp:paragraph -->\n\n"
             "<!-- wp:paragraph -->\n<p>11月23日(月)は勤労感謝の日なので、21日から3連休です。<br>\n"
             "遠くから行く人は、宿や新幹線を早めにおさえておきましょう。</p>")

OLD_TOC = "<li>11月下旬のスタジアムに合う服装</li>"
NEW_TOC = "<li>11月21日・22日の気温と天気</li>\n" + OLD_TOC
OLD_TOC2 = "<li>持ち物チェックリスト</li>"
NEW_TOC2 = OLD_TOC2 + "\n<li>終演と規制退場の目安</li>"

# --- 日程 ---
OLD_SCHED = ("開場時間やグッズ販売の時間は、公式サイトや公式アプリで直前に案内されることが多いので、"
             "前日までに確認しておくと安心です。</p>\n<!-- /wp:paragraph -->\n\n")
NEW_SCHED = (
    "ツアーの正式な名前は「SixTONES LIVE TOUR 2026『MILESixTONES』」です。</p>\n<!-- /wp:paragraph -->\n\n"
    + p(f"開場は、公式サイトで「開演の2時間前を予定」と案内されています。",
        f"日産スタジアムなら{MARK.format('14時30分ごろ開場の予定')}です。",
        "決まった時間は、前日から当日に公式アプリなどで確かめてください。")
    + p("公式Xでは、公演を「1/6公演目」のように数えています。",
        "日産スタジアムの2日間は5公演目と6公演目で、ツアーの最後になります。")
    + p("長居公演の2日目には、髙地優吾さんのメッセージと会場の看板の写真が公式Xに出ました。",
        "大きな看板の右下には、もう「NISSAN STADIUM 2026.11.21-22」の文字が入っています。")
    + "{IMG_KOCHI}"
    + p(f"日産スタジアム公演は、{MARK.format('FAMILY CLUB onlineで生配信')}されることも決まっています。",
        "チケットが取れなかった人や、当日行けない人は配信で見られます。")
    + p("当日のセトリを予習したい人は、" + a(L_SETLIST, "MILESixTONES日産スタジアムで予習したい34曲のセトリ")
        + "にまとめています。")
)

# --- 気温(新しいH2。服装の前に入れる) ---
WEATHER = (
    h2("11月21日・22日の気温と天気")
    + p(f"気象庁の週間予報(11月16日17時の発表)では、横浜は{MARK.format('2日とも晴れ時々くもり')}です。",
        "雨の確率は20%と低めですが、気温はかなり低くなりそうです。")
    + table(["日", "天気", "最高/最低"],
            [["11月21日(土)", "晴れ時々くもり", "15℃/7℃"],
             ["11月22日(日)", "晴れ時々くもり", "14℃/6℃"]])
    + p("この時期の横浜のいつもの気温は、最高16℃・最低9℃くらいです。",
        f"今年は{MARK.format('いつもの年より2〜3℃低い')}予報になっています。")
    + p("去年の11月21日・22日は、夜8時でも13℃くらいありました。",
        "今年は最低気温が6〜7℃の予報なので、終演のころは10℃を下回るかもしれません。")
    + p(f"もうひとつ気をつけたいのが、日の入りの時間です。",
        f"11月21日・22日の横浜の日の入りは{MARK.format('16時32分')}で、開演とほぼ同じ時間です。",
        "開演してすぐに暗くなり、そこから気温はどんどん下がっていきます。")
    + p("天気予報は日がたつと変わります。",
        "前の日に、もう一度気象庁や天気アプリで横浜の予報を確かめておきましょう。")
    + p("雨だった東京公演の2日目には、京本大我さんが公式Xで体調を気づかうメッセージを出していました。")
    + "{IMG_KYOMOTO}"
)
ANCHOR_FUKU = '<!-- wp:heading -->\n<h2 class="wp-block-heading">11月下旬のスタジアムに合う服装</h2>'

# --- 服装に足す(メンバーカラーの段落のあと) ---
OLD_COLOR_END = "マフラーや小物でさりげなく取り入れるのも人気です。</p>\n<!-- /wp:paragraph -->\n\n"
ROOF = (
    h3("屋根があるのは一部の席だけ")
    + p(f"日産スタジアムの公式の案内では、屋根があるのは{MARK.format('1階席の19列目より後ろと2階席だけ')}です。",
        "グラウンドの上のアリーナ席と、1階席の前のほうには屋根がありません。",
        "屋根の下でも、風の向きによっては雨が吹きこむことがあるそうです。")
    + p(f"また、スタジアムでは{MARK.format('傘はさせません')}。",
        "雨のときはレインポンチョやレインコートを使いましょう。",
        "自分の席がどこか分かるタイミングは、" + a(L_SEAT, "SixTONESのライブの席が当日まで分からない理由") + "で調べています。")
    + h3("長居公演に行った人の寒さ対策")
    + p("大阪・長居公演に行った人からは、こんな声が出ていました。")
    + voice("「イス冷たすぎるから敷くものあるといいよ」")
    + voice("「7ヵ所にカイロ貼ったらけっこういけました。MCのとき耳寒かったので、SixTONESタオルを頭に巻きました」")
    + voice("「グッズのタオルがまじでマフラーだった」「足元もすごく冷えてた」")
    + p("イスと足元から冷えるので、座ぶとんや厚い靴下、靴に入れるカイロがあると安心です。",
        "公式グッズのフェイスタオルを、首に巻いている人も多かったようです。",
        "ペンライトを持つ手が冷えるので、指先が出る手袋も便利です。")
    + p("電車の中は暑いので、脱いだり着たりしやすい重ね方にしておきましょう。",
        "足元の選び方は、" + a(L_BOOTS, "長居公演で話題になった厚底ブーツと雨の日の足元対策") + "も参考になります。")
)

# --- グッズ ---
OLD_GOODS = ("東京・味の素スタジアム公演では、会場でグッズを買うのに入場整理券の取得が必要でした。<br>\n"
             "日産スタジアムでも同じような方式になる可能性があるので、公式のお知らせを確認してください。</p>")
NEW_GOODS = (f"日産スタジアムの会場販売は、{MARK.format('11月21日・22日とも10時〜17時')}です。<br>\n"
             "アプリ「MERCH MARKET Goods App」で入場整理券を予約する方式で、1つの商品は2点までです。<br>\n"
             "チケットがない人も申しこめますが、開場の時間はさけて予約するよう案内されています。</p>\n"
             "<!-- /wp:paragraph -->\n\n<!-- wp:paragraph -->\n"
             "<p>グッズの中に、ブランケットなどの防寒用のものはありません。<br>\n"
             "寒さ対策にも使えるのは、フェイスタオル(2,000円)です。</p>")

# --- 持ち物 ---
OLD_CHECK_LAST = check_line("ICカード(帰りの駅で並ばずにすむ)")
NEW_CHECK_LAST = (OLD_CHECK_LAST + "\n"
                  + check_line("座ぶとん・クッション(イスが冷たい)") + "\n"
                  + check_line("貼るカイロ・靴に入れるカイロ") + "\n"
                  + check_line("指先が出る手袋(ペンライトを持ちやすい)"))
OLD_CHECK_END = "<!-- /wp:html -->\n\n" + h2("日産スタジアム公演についてよくある質問")
CHECK_AFTER = p("ひざかけや水筒を会場に持ちこめるかは、スタジアムの案内では「主催者に確認を」となっていました。",
                "主催者の決まりは見つからなかったので、当日の案内に従いましょう。",
                "温かい飲み物を入れる水筒は、" + a(L_SUITO, "松村北斗さんがライブにも持っていく愛用水筒") + "も人気です。")
TAIJO = (
    h2("終演と規制退場は何時ごろ？")
    + p("終演の時間は、公式には発表されていません。",
        "長居公演(17時開演)では、19時45分〜20時ごろに終わったという声が多くありました。",
        "そのあとの規制退場は、30分くらいかかったそうです。")
    + p(f"日産スタジアムは30分早い16時30分開演です。",
        f"同じ流れなら、{MARK.format('19時15分〜30分ごろに終演、最後のブロックが出るのは20時ごろ')}になりそうです。",
        "ただし、これは長居の例から考えた目安です。")
    + p("規制退場を待つ時間も、外で冷える時間になります。",
        "最後まで上着はぬがず、カイロも少し残しておきましょう。",
        "帰りの新幹線は、余裕をもって21時より後の便にしておくと安心です。")
)

# --- FAQ ---
OLD_FAQ_GOODS = ("<p>東京公演では、整理券を取ればチケットがなくてもグッズを買えたと伝えられています。<br>\n"
                 "日産公演の方式は、公式のお知らせで確認してください。</p>")
NEW_FAQ_GOODS = ("<p>買えます。<br>\n"
                 "日産公演も、チケットがなくてもアプリで整理券を予約できると公式に案内されています。</p>")
FAQ_ADD = (
    h3("開場は何時？")
    + p("公式は「開演の2時間前を予定」としているので、14時30分ごろの予定です。")
    + h3("アリーナ席に屋根はある？")
    + p("ありません。", "屋根があるのは1階席の19列目より後ろと2階席だけです。")
    + h3("当日行けない人は見られる？")
    + p("日産スタジアム公演は、FAMILY CLUB onlineで生配信されます。")
)
ANCHOR_FAQ_END = ('<!-- wp:paragraph -->\n<p>大阪公演の服装やアクセスは<a href="https://chomoand-0.com/?p=1172">')

# --- まとめ ---
OLD_SUM_COLD = check_line("11月下旬の夜は真冬並みの防寒が必要")
NEW_SUM_COLD = (check_line("予報は最高14〜15℃・最低6〜7℃、日の入りは開演とほぼ同じ16時32分") + "\n"
                + check_line("屋根は1階19列目より後ろと2階席だけ、傘はさせない") + "\n"
                + check_line("終演は19時15分〜30分ごろ、規制退場は20時ごろまでの見込み"))
OLD_END = ("<p>グループ初のスタジアムツアーのラストを飾る日産スタジアム。<br>\n"
           "しっかり準備して、6人と最高の締めくくりを楽しみましょう！</p>")
NEW_END = ("<p>グループ初のスタジアムツアーのラストを飾る日産スタジアム。<br>\n"
           "次の日の11月23日(月)0時からは、全曲のサブスク解禁も決まっています。<br>\n"
           "2027年のドームツアー「1'MM AHEAD」の前に、6人と最高の締めくくりを楽しみましょう！</p>")

OLD_REL = '<li><a href="https://chomoand-0.com/?p=1172">'
NEW_REL = (f'<li><a href="{L_SETLIST}">MILESixTONES日産スタジアムのセトリ予習</a></li>\n'
           f'<li><a href="{L_SEAT}">SixTONESのライブの席が当日まで分からない理由</a></li>\n' + OLD_REL)


IMGS = {
    "IMG_KOCHI": ("tools/Xiy/posts_sixtones_milesixtones_nissan_1116_nagai/images/post_3_img_1.jpg",
                  "sixtones_nissan_1238_nagai_board_1116.jpg",
                  "MILESixTONES長居公演の看板(右下に日産スタジアム11月21日・22日の文字)", X_KOCHI),
    "IMG_KYOMOTO": ("tools/Xiy/posts_sixtones_milesixtones_nissan_1116_ajista/images/post_6_img_1.jpg",
                    "sixtones_nissan_1238_ajista_rain_1116.jpg",
                    "雨の味の素スタジアムに下がるMILESixTONESの垂れ幕", X_KYOMOTO),
}


def upload_images(wp):
    import shutil, tempfile
    out = {}
    tmp = tempfile.mkdtemp()
    for key, (src, name, alt, url) in IMGS.items():
        dst = os.path.join(tmp, name)
        shutil.copy(os.path.join(REPO, src), dst)
        mid = wp.upload_media(dst, alt)
        m = wp.get(f"/media/{mid}")
        sz = m["media_details"]["sizes"]
        s = sz.get("large") or sz.get("medium_large") or sz["full"]
        out[key] = html(f'<figure class="wp-block-image size-large"><img src="{s["source_url"]}" alt="{alt}" '
                        f'width="{s["width"]}" height="{s["height"]}" style="max-width:100%;height:auto;">'
                        f'<figcaption style="font-size:0.8em;color:#888;">出典:{url}</figcaption></figure>')
        print("media", mid, s["source_url"])
    return out


def build(c):
    def rep(old, new):
        nonlocal c
        assert c.count(old) == 1, f"見つからない/複数({c.count(old)}): {old[:50]}"
        c = c.replace(old, new)

    rep(OLD_LEAD1, NEW_LEAD1)
    rep(OLD_LEAD3, NEW_LEAD3)
    lead_end = "宿や新幹線を早めにおさえておきましょう。</p>\n<!-- /wp:paragraph -->\n\n"
    rep(lead_end, lead_end + UPDATE_NOTE)
    rep(OLD_TOC, NEW_TOC)
    rep(OLD_TOC2, NEW_TOC2)
    rep(OLD_SCHED, NEW_SCHED)
    rep(ANCHOR_FUKU, WEATHER + ANCHOR_FUKU)
    rep(OLD_COLOR_END, OLD_COLOR_END + ROOF)
    rep(OLD_GOODS, NEW_GOODS)
    rep(OLD_CHECK_LAST, NEW_CHECK_LAST)
    rep(OLD_CHECK_END, "<!-- /wp:html -->\n\n" + CHECK_AFTER + TAIJO + h2("日産スタジアム公演についてよくある質問"))
    rep(OLD_FAQ_GOODS, NEW_FAQ_GOODS)
    rep(ANCHOR_FAQ_END, FAQ_ADD + ANCHOR_FAQ_END)
    rep(OLD_SUM_COLD, NEW_SUM_COLD)
    rep(OLD_END, NEW_END)
    rep(OLD_REL, NEW_REL)
    return c


if __name__ == "__main__":
    wp = blogkit.WP("sixtones")
    po = wp.get(f"/posts/{POST}", context="edit")
    revs = wp.get(f"/posts/{POST}/revisions", per_page=1)
    assert revs[0]["id"] == EXPECT_REV, f"新しい直しがある(rev{revs[0]['id']})。差分を見てから進める"
    built = build(po["content"]["raw"])
    if "--apply" in sys.argv:
        for k, v in upload_images(wp).items():
            built = built.replace("{" + k + "}", v)
    else:
        for k, (src, name, alt, url) in IMGS.items():
            built = built.replace("{" + k + "}", html(f'<figure><img src="PREVIEW" alt="{alt}"><figcaption>出典:{url}</figcaption></figure>'))
    out = blogkit.finalize(built, "sixtones")
    open(OUT, "w", encoding="utf-8").write(out)
    r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "easy_read.py"), "check", OUT])
    if r.returncode != 0:
        sys.exit("easy_read NGあり。直してから --apply")
    if "--apply" in sys.argv:
        res = wp.post(f"/posts/{POST}", {"content": open(OUT, encoding="utf-8").read()})
        print("更新OK", res["modified"], res["link"])
    else:
        print("build-only OK", OUT)
