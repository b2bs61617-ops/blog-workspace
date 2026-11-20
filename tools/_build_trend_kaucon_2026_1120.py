# -*- coding: utf-8 -*-
"""chomoand.com下書き「カウコン2026の会場と出演者は？当選報告は何のこと？」(2026-11-20 ユカ依頼、Xトレンド「カウコン」10位)。

トレンドの理由: 11/20 14時になにわ男子 DOME LIVE 2026-2027「ND⁵+」(12/31京セラ22時=年越し)の当落 → ファンが「カウコン当選」と投稿、
「そもそもカウコン申し込み来た？」と混乱。同日 Netflix 12月ラインナップ(modelpress 11/20 12:31)にカウコン(12/31世界独占LIVE配信・アーカイブあり)。
根拠: STARTO公式 live/10596(12/31開催、詳細は決定次第)、NetflixJP X 9/22(30周年・190以上の国と地域)、
modelpress 4866963(なにわ公演日時)、前回: NetflixJP X 1/7(出演12組)、mediadogs(東京ドーム・FC抽選13,000円・受付12/6〜12/10・当落12/19・18歳未満不可)。
会場・出演者・チケットは未発表 → そう書く。WEST.の話は裏が取れないので書かない。

    python3 tools/_build_trend_kaucon_2026_1120.py                # 下書き投稿
    python3 tools/_build_trend_kaucon_2026_1120.py --build-only
    python3 tools/_build_trend_kaucon_2026_1120.py --update
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "trend"
KEY = "trend_kaucon_2026_1120"
TITLE = "カウコン2026の会場と出演者は？当選報告は何のこと？"
SLUG = "countdown-concert-2026-2027"
CATEGORIES = [37]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "カウコン2026の会場と出演者は？"
X_TEXT = ""
X_TAGS = "#カウコン #STARTOtoWORLD"

OFFICIAL = "https://starto.jp/s/p/live/10596"
X_NETFLIX = "https://x.com/NetflixJP/status/2102473002298261519"
X_NETFLIX_PREV = "https://x.com/NetflixJP/status/2008887597238555040"
MDPR_NANIWA = "https://mdpr.jp/music/4866963"
MDPR_NETFLIX = "https://mdpr.jp/news/4880005"
MEDIA_CACHE = blogkit.ARTICLES / (KEY + "_media.json")
PHOTOS = {
    "netflix": (blogkit.ROOT / "images" / (KEY + "_netflix.jpg"),
                "COUNTDOWN CONCERT 2026-2027 STARTO to WORLDのNetflixライブ配信告知", X_NETFLIX),
}

b = blogkit.Blocks("#3b82c4", "#bcd8f0", "#f2f8fd")
p, h2, h3, mk, L = b.p, b.h2, b.h3, b.mark, b.link


def photo(key):
    import json
    path, alt, src_url = PHOTOS[key]
    if "--build-only" in sys.argv:
        src, w, h = "x", 1080, 1350
    else:
        cache = json.loads(MEDIA_CACHE.read_text(encoding="utf-8")) if MEDIA_CACHE.exists() else {}
        if key not in cache:
            wp = blogkit.WP(SITE)
            mid = wp.upload_media(str(path), alt)
            cache[key] = wp.get("/media/{}".format(mid))
            MEDIA_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        m = cache[key]
        big = m["media_details"].get("sizes", {}).get("large") or {
            "source_url": m["source_url"], "width": m["media_details"]["width"], "height": m["media_details"]["height"]}
        src, w, h = big["source_url"], big["width"], big["height"]
    return b.html('<figure class="wp-block-image size-large"><img src="{}" alt="{}" width="{}" height="{}" '
                  'style="max-width:100%;height:auto;"><figcaption style="font-size:0.8em;color:#888;">'
                  '出典:<a href="{}" target="_blank" rel="noopener">{}</a></figcaption></figure>'
                  .format(src, alt, w, h, src_url, src_url))


out = ""

out += p("11月20日、Xで「カウコン」がトレンド入りしました。",
         "「カウコン当たった！」という声が並ぶ一方で、「そもそもカウコンの申し込みって来た？」と首をかしげる人も出ています。")
out += p("結論から言うと、" + mk("今日の「当選」は、なにわ男子の年越しライブのこと") + "です。",
         "STARTO ENTERTAINMENTの全体のカウコンは、会場も出演者もまだ発表されていません。")
out += p("この記事では、2つのカウコンのちがいを整理しました。",
         "あわせて、2026年のカウコンで分かっていることと、チケットの予想もまとめています。")
out += b.mini(("公演名", "COUNTDOWN CONCERT 2026-2027 STARTO to WORLD"),
              ("日にち", "2026年12月31日(木)"),
              ("会場・出演者", "まだ発表されていない(11月20日時点)"),
              ("配信", "Netflixで世界190以上の国と地域にライブ配信"),
              ("チケット", "まだ発表されていない"))
out += b.wakaru([
    "今日の「カウコン当選」は何のことか",
    "2026年のカウコンの会場と出演者",
    "Netflixでの配信の予定",
    "チケットの申し込みはいつごろになりそうか",
    "前回(2025-2026)のカウコンのふり返り",
])

out += h2("今日の「カウコン当選」は何のこと？")
out += b.mini(("答え", "なにわ男子の京セラドーム年越しライブ(12/31)の当落のこと"))
out += p("11月20日の14時、なにわ男子のドームライブの当落が出ました。",
         "その中の" + mk("12月31日の京セラドーム大阪公演は、22時に始まる年越しライブ") + "です。")
out += p("年をまたいでカウントダウンをするので、ファンのあいだでは「カウコン」とも呼ばれています。",
         "そのため「カウコン当選！」という投稿が一気に増え、トレンド入りしました。")
out += b.table(("日にち", "会場", "開演"), [
    ("2026年12月31日(木)", "京セラドーム大阪", "22:00"),
    ("2027年1月1日(金・祝)", "京セラドーム大阪", "18:00"),
    ("2027年1月15日(金)", "東京ドーム", "18:00"),
    ("2027年1月16日(土)", "東京ドーム", "17:00"),
])
out += p("正式なタイトルは「なにわ男子 DOME LIVE 2026-2027『ND⁵+ ～あけおめぇ 初夢ぇ Stay with MEE～』」です("
         + L(MDPR_NANIWA, "モデルプレス") + ")。",
         "10月28日のアリーナツアーの公演中に、サプライズで発表されました。")
out += h3("STARTO全体のカウコンとは別もの")
out += p("一方、毎年おなじみの「カウコン」は、STARTO ENTERTAINMENTのグループがたくさん集まる年越しコンサートです。",
         "こちらは" + mk("まだチケットの申し込みも始まっていません。"))
out += p("「カウコンの申し込みなんて来てないのに？」と戸惑った人は、このちがいが理由です。",
         "同じ大みそかの夜なので、どちらのことか確かめながら情報を追うのがおすすめです。")

out += h2("カウコン2026の会場と出演者は？")
out += b.mini(("答え", "11月20日時点では、会場・出演者・開演時間とも未発表"))
out += p("2026年のカウコンの正式な名前は「COUNTDOWN CONCERT 2026-2027 STARTO to WORLD」です。",
         "9月22日に、12月31日(木)に開くことが発表されました。")
out += photo("netflix")
out += p("ただ、STARTOの" + L(OFFICIAL, "公式サイト") + "には、今も「詳細は決定次第お知らせ」とだけ書かれています。",
         mk("会場・出演者・開演時間は、まだどれも発表されていません。"))
out += h3("なにわ男子は京セラドームに出るので……")
out += p("なにわ男子は、同じ12月31日の22時から京セラドーム大阪でライブをします。",
         "そのため、カウコンの会場にずっといるのはむずかしいとみられます。")
out += p("中継などでつながる形になるのかは、まだ分かっていません。",
         "出演者の発表を待ちましょう。")
out += h3("今年はカウコン30周年")
out += p("カウコンは1996年に始まり、2026年で30周年をむかえます。",
         "Netflixの告知でも「30周年を迎える“カウコン”」と紹介されていて、特別な回になりそうです。")

out += h2("カウコン2026はNetflixで世界に生配信")
out += b.mini(("答え", "12月31日にNetflixで世界独占ライブ配信、アーカイブもあり"))
out += p("今回いちばんの話題は、" + mk("Netflixで世界190以上の国と地域に生配信される") + "ことです。",
         "日本初の、世界同時のライブ配信とうたわれています。")
out += p("11月20日に出たNetflixの12月の配信予定にも、カウコンが入りました("
         + L(MDPR_NETFLIX, "モデルプレス") + ")。",
         "あとから見られるアーカイブもあるので、年越しの瞬間に見られない人も安心です。")
out += b.table(("配信されるもの", "時期"), [
    ("カウコンへの思いを語る番組", "12月"),
    ("カウコン本番のライブ", "12月31日(アーカイブあり)"),
    ("舞台裏に密着した番組", "2027年1月下旬"),
])
out += p("Netflixで見るには、Netflixの会員になっている必要があります。",
         "ファンクラブの配信サイトでも見られるのかは、まだ発表されていません。")

out += h2("カウコン2026のチケットはいつ申し込める？")
out += b.mini(("答え", "未発表。前回と同じなら12月上旬にファンクラブで抽選"))
out += p("会場のチケットについては、11月20日時点で何も発表されていません。",
         "参考になるのが、前回(2025-2026)の流れです。")
out += b.table(("前回の流れ", "日にち"), [
    ("ファンクラブで申し込み", "2025年12月6日(土)〜10日(水)"),
    ("当落の発表", "2025年12月19日(金)"),
    ("チケットの値段", "1枚13,000円(税込)"),
])
out += p("前回は、" + mk("申し込みが始まったのは本番の1か月前ほど") + "でした。",
         "今回も同じなら、11月の終わりから12月の初めに案内が来るかもしれません。")
out += p("また、前回は深夜0時をまたぐため、18歳未満は会場に入れませんでした。",
         "東京都の条例によるもので、今回も会場によっては同じ決まりになる可能性があります。")

out += h2("前回のカウコン(2025-2026)をふり返り")
out += p("前回の「STARTO to MOVE」は、東京ドームで3年ぶりに開かれました。",
         "出演したのは、次の12組です(" + L(X_NETFLIX_PREV, "Netflix公式X") + ")。")
out += b.checks(["NEWS / Hey! Say! JUMP / Kis-My-Ft2",
                 "timelesz / 中島健人 / A.B.C-Z",
                 "King & Prince / SixTONES / Snow Man",
                 "なにわ男子 / Travis Japan / Aぇ! group"])
out += p("グループの垣根をこえたシャッフルメドレーや、年男の企画が話題になりました。",
         "このときもNetflixで配信されましたが、配信が始まったのは年が明けた1月7日でした。")
out += p("今回は大みそかに生で世界に届けられるので、前回よりスケールが大きくなりそうです。")

out += h2("まとめ")
out += b.checks(["今日の「カウコン当選」は、なにわ男子の京セラ年越しライブ(12/31 22時)のこと",
                 "STARTO全体のカウコンは12月31日(木)開催、会場・出演者は未発表",
                 "Netflixで世界190以上の国と地域に生配信、アーカイブあり",
                 "チケットは未発表、前回は12月上旬にファンクラブで抽選",
                 "2026年はカウコン30周年"])
out += p("年越しの予定が少しずつ決まってきて、わくわくする季節になりましたね。",
         "出演者が発表されたら追記するので、ときどきチェックしてみてはいかがでしょうか！")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = blogkit.finalize(out, SITE, NAMES)
    if "--publish" in sys.argv:
        import json
        state = json.loads((blogkit.ARTICLES / (KEY + "_posted.json")).read_text(encoding="utf-8"))
        blogkit.publish(SITE, state["post"], X_TEXT, X_TAGS)
    elif "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
