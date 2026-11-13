"""ちいかわクリニック記事(chomoand.com ID13107)を最新情報で書き直す(2026-11-13、ユカ依頼「1でお願い。タイトルは変えないで」)。
抽選の受付が始まった11/13のSNSの声(顔写真の不安・申し込む時間・古本屋さんの膀胱など)を足す。
公開後に管理画面で足された pasutaraisuke 埋め込み(rev13114)を残すため、公開中の本文を土台に差し込むだけにする。
タイトルは変えない。usage: python3 tools/_update_chiikawa_clinic_1113.py [--apply]
"""
import base64, json, os, subprocess, sys, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POST = 13107
EXPECT_REV = 13114  # この版より新しい人の直しがあれば止まる

env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    if "=" in line and not line.lstrip().startswith("#"):
        k, v = line.rstrip("\n").split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_TREND_USERNAME']}:{env['WP_TREND_APP_PASSWORD']}".encode()).decode()


def req(path, data=None, method=None):
    r = urllib.request.Request(BASE + path, method=method or ("POST" if data else "GET"),
                               data=json.dumps(data).encode() if data else None,
                               headers={"Authorization": "Basic " + AUTH, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r))


MP = '<strong><span class="swl-marker mark_pink" style="font-size:1.15em;">{}</span></strong>'
MO = '<strong><span class="swl-marker mark_orange"><span class="swl-fz u-fz-l">{}</span></span></strong>'


def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n"


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n'


def voice(t):
    return ('<!-- wp:html -->\n<p style="border-left:4px solid #e8829a;padding:10px 16px;margin:0 0 16px 0;'
            f'background:#fdf3f5;">{t}</p>\n<!-- /wp:html -->\n\n')


def ul(*items):
    li = "\n".join(f"<li>{i}</li>" for i in items)
    return ('<!-- wp:html -->\n<ul style="margin:0 0 16px 0;padding:12px 16px 12px 32px;background:#fdf3f5;'
            f'border-radius:4px;">\n{li}\n</ul>\n<!-- /wp:html -->\n\n')


UPDATE_NOTE = ('<!-- wp:html -->\n<p style="border:1px solid #f6d3db;border-radius:4px;padding:8px 14px;margin:0 0 16px 0;'
               'background:#fffafb;font-size:0.9em;">2026年11月13日:入店抽選の受付が始まりました。'
               '申し込みの注意点と、顔写真が不安な人向けの情報、新しいSNSの声を足しました。</p>\n<!-- /wp:html -->\n\n')

# 抽選が始まった後の新しいH3(「当日の持ち物と注意点」の前に入れる)
LOTTERY_TIPS = (
    h3("抽選は早く申し込んだほうが有利？")
    + p("SNSでは「何時に申し込むのがいいんだろう」と迷う声が出ています。",
        f"今回の11月27日〜30日の分は先着ではなく{MP.format('抽選')}です。",
        "しめきりの11月15日(日)23時59分までに申し込めば大丈夫です。")
    + p("あわてて申し込むより、行ける日と会場をしっかり決めてから応募しましょう。",
        "「申し込んだあとで、家族の予定とかぶっていた」という声もありました。")
    + p(f"当選したかどうかは、{MO.format('11月16日(月)')}に「マイチケット」で見られます。",
        "落ちた人は、16日〜18日の20時からの二次先着(上の表)もチェックしておきましょう。")
    + p("「LINEのアプリが開かない」という声も少しありました。",
        "うまく開かないときは、LINEアプリを新しい版にしてから試してみてください。")
)

FACE_PHOTO = (
    h3("顔写真の登録が不安な人は？")
    + p("抽選が始まってから、いちばん多かったのが顔写真への不安の声です。")
    + voice("「名前と顔両方って、かなり怖くない？？」")
    + p("ほかにも「すっぴんで撮りたくない」「前髪やメイクが変わったらダメなのかな」という声がありました。",
        "反対に「職場の休けい所で撮った」と、さっと済ませた人もいます。")
    + p("顔写真を何に使うのかのくわしい説明は、発表の中には見当たりませんでした。",
        f"当日は{MP.format('本人確認書類の実物')}が必要なので、本人かどうかを見るためと考えられます。")
    + p("どうしても不安な人は、入店予約がいらない通販のちいかわマーケットを使う手もあります。",
        "ちいかわらんどの入店方法は、これから公式Xで知らせるとされています。")
)

ORGAN_ADD = p("抽選が始まった13日には「古本屋さんが膀胱なのマジで何」という声も出ました。",
              "「肝臓と肺がほしい」と、ほしい臓器を決めている人もいます。")

SNS_ADD = (
    p("11月13日に抽選の受付が始まると、こんな声も出てきました。")
    + ul("「ちいかわクリニック当選してくれ〜🙏」",
         "「争奪戦負けた時の保険に悪あがきやけど 梅田のちいかわクリニック抽選申込した！」",
         "「看護師免許提示で優遇してくれない？」",
         "「グッズ欲しすぎるけど買えなさそうで鬱」")
)

OLD_LEAD = MO.format("応募は11月13日(金)10時から15日(日)23時59分まで") + "です。</p>"
NEW_LEAD = ("応募は11月13日(金)10時に始まり、" + MO.format("しめきりは15日(日)23時59分") + "です。</p>")

OLD_TOC = "<li>入店抽選の日程と申し込み方法、当日の持ち物</li>"
NEW_TOC = OLD_TOC + "\n<li>顔写真の登録が不安な人へ</li>"

OLD_END = ("<p>まずは11月13日(金)10時からの入店抽選を忘れずに申し込みましょう。<br>\n"
           "通販派の人は、11月27日(金)11時の予約受付が勝負です。</p>")
NEW_END = ("<p>入店抽選のしめきりは、11月15日(日)23時59分です。<br>\n"
           "16日(月)の当選発表も見わすれないようにしましょう。<br>\n"
           "通販派の人は、11月27日(金)11時の予約受付が勝負です。</p>")

OLD_SUM = "期間限定会場8か所の入店抽選は11月13日(金)10時〜15日(日)23時59分"
NEW_SUM = "期間限定会場8か所の入店抽選は11月15日(日)23時59分まで(当選発表は16日)"


def build(c):
    def rep(old, new):
        nonlocal c
        assert c.count(old) == 1, f"見つからない/複数: {old[:40]}"
        c = c.replace(old, new)

    rep(OLD_LEAD, NEW_LEAD)
    first_p = "<!-- wp:paragraph -->\n<p>2026年11月12日のお昼"
    rep(first_p, UPDATE_NOTE + first_p)
    rep(OLD_TOC, NEW_TOC)
    anchor = '<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">当日の持ち物と注意点</h3>'
    rep(anchor, LOTTERY_TIPS + anchor)
    # 「予約」H2の直前(=当日の持ち物の最後)に顔写真のH3
    yoyaku = '<!-- wp:heading -->\n<h2 class="wp-block-heading">ちいかわクリニックの「予約」は受注生産？通販の注意点</h2>'
    rep(yoyaku, FACE_PHOTO + yoyaku)
    organ_last = "しばらく話題が続きそうです。</p>\n<!-- /wp:paragraph -->\n\n"
    rep(organ_last, organ_last + ORGAN_ADD)
    sns_last = "病院で働く人のあいだでも、争奪戦になるかもしれません。</p>\n<!-- /wp:paragraph -->\n\n"
    rep(sns_last, sns_last + SNS_ADD)
    rep(OLD_SUM, NEW_SUM)
    rep(OLD_END, NEW_END)
    rep("<th>買える場所</th><th>詳細</th>", "<th>買える場所</th><th>くわしく</th>")
    return c


if __name__ == "__main__":
    po = req(f"/wp-json/wp/v2/posts/{POST}?context=edit")
    revs = req(f"/wp-json/wp/v2/posts/{POST}/revisions?per_page=1")
    assert revs[0]["id"] == EXPECT_REV, f"新しい直しがある(rev{revs[0]['id']})。差分を見てから進める"
    out = build(po["content"]["raw"])
    path = os.path.join(REPO, "articles", "chiikawa_clinic_1113_update.html")
    open(path, "w", encoding="utf-8").write(out)
    subprocess.run([sys.executable, os.path.join(REPO, "tools", "easy_read.py"), "fix", path], check=True)
    r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "easy_read.py"), "check", path])
    if r.returncode != 0:
        sys.exit("easy_read NGあり。直してから --apply")
    if "--apply" in sys.argv:
        out = open(path, encoding="utf-8").read()
        res = req(f"/wp-json/wp/v2/posts/{POST}", {"content": out})  # タイトル・ステータスは触らない
        print("更新OK", res["modified"], res["title"]["raw"], res["link"])
