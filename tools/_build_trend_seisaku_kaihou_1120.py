# -*- coding: utf-8 -*-
"""chomoand.com下書き「制作開放席とは？当落はいつ分かる？席は後ろ確定？」(2026-11-20 ユカ依頼、Xトレンド「制作開放」27位)。

根拠: X検索(11/13〜11/20)。SixTONES日産(11/21・22 16:30開演)の制作開放の当落が11/20夕方に出て、
「案内メール」「1名義1枚・同行者なし」「PayPay/カードの引き落としで先に分かる」「落選は支払い取消」
「最後列・ステージ横もあれば、ちゃんとした席も」の声。日時はXiyのUTC表記→JSTに直した(当選報告は17時半〜18時台)。
STARTO公式に制作開放の説明ページは無い → 「公式にくわしい説明はない」と書き、SNSの声はそう明記。
写真: SixTONES公式X 9/19(味の素スタジアム、スタジアムツアー初日)。

    python3 tools/_build_trend_seisaku_kaihou_1120.py                # 下書き投稿
    python3 tools/_build_trend_seisaku_kaihou_1120.py --build-only
    python3 tools/_build_trend_seisaku_kaihou_1120.py --update
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "trend"
KEY = "trend_seisaku_kaihou_1120"
TITLE = "制作開放席とは？当落はいつ分かる？席は後ろ確定？"
SLUG = "starto-seisaku-kaihou-seki"
CATEGORIES = [37]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "制作開放席とは？当落はいつ分かる？"
X_TEXT = ""
X_TAGS = "#制作開放"

X_STO = "https://x.com/SixTONES_SME/status/2101212193576349795"
MEDIA_CACHE = blogkit.ARTICLES / (KEY + "_media.json")
PHOTOS = {
    "stadium": (blogkit.ROOT / "images" / (KEY + "_stadium.jpg"),
                "SixTONESスタジアムツアー「MILESixTONES」初日の味の素スタジアム", X_STO),
}

b = blogkit.Blocks("#3b82c4", "#bcd8f0", "#f2f8fd")
p, h2, h3, mk, L = b.p, b.h2, b.h3, b.mark, b.link


def photo(key):
    import json
    path, alt, src_url = PHOTOS[key]
    if "--build-only" in sys.argv:
        src, w, h = "x", 1200, 675
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

out += p("11月20日の夕方、Xで「制作開放」という言葉がトレンド入りしました。",
         "SixTONESの日産スタジアム公演を前に、「当たった！」「明日なのに何も準備してない！」という声があふれています。")
out += p("制作開放席とは、" + mk("ステージの準備が終わったあとに追加で出される席") + "のことです。",
         "落選した人の一部に案内が届き、申し込んで当たれば公演に行けます。")
out += p("この記事では、制作開放席のしくみと、当落が分かるタイミングをまとめました。",
         "「席は後ろ確定？」「1枚しか申し込めないの？」といった疑問にも答えていきます。")
out += b.mini(("制作開放席", "機材などの配置が決まったあとに追加で出る席"),
              ("案内", "落選した人の一部にメールで届く(全員ではない)"),
              ("時期", "公演の1週間前〜前日ごろ"),
              ("当落", "公演前日の夕方ごろに分かることが多い"),
              ("席", "後ろ・ステージ横などが多いが、ふつうの席のことも"))
out += b.wakaru([
    "制作開放席とはどんな席か",
    "案内が届く人・届くタイミング",
    "当落はいつ・どうやって分かるか",
    "1枚しか申し込めないのか",
    "席は後ろや見切れ確定なのか",
])

out += h2("制作開放席とは？")
out += b.mini(("答え", "ステージや機材の配置が決まってから、あいた場所に追加で出る席"))
out += p("コンサートでは、チケットを売る時点ではステージの形や機材の置き場がまだ決まっていません。",
         "そのため、機材が置かれるかもしれない場所は、はじめは売らずに取っておきます。")
out += p("準備が進んで「ここは使わない」と分かった場所が、" + mk("制作開放席") + "として追加で出されます。",
         "「制作」はコンサートを作る側、「開放」は席を開けるという意味です。")
out += p("STARTO ENTERTAINMENTのファンクラブ(FC)の公演では、おなじみのチケットの取り方です。",
         "ただし、公式のサイトにくわしい説明はのっていません。",
         "この記事は、これまでの案内の流れと、SNSに集まった体験の声をもとにまとめています。")
out += photo("stadium")
out += h3("復活当選とのちがい")
out += p("よくまちがえられるのが「復活当選」です。",
         "復活当選は、お金を払えば席が用意される形で、ほぼ当選が決まっています。")
out += p("一方、制作開放席は" + mk("案内が届いた時点ではまだ当選ではありません。"),
         "申し込んだ人の中から、もう一度抽選になります。")
out += b.table(("", "制作開放席", "復活当選"), [
    ("届くもの", "申し込みの案内", "当選のお知らせ"),
    ("当選", "申し込んだあと抽選", "ほぼ決まっている"),
    ("時期", "公演の直前が多い", "公演によってちがう"),
])

out += h2("制作開放の案内は誰に・いつ届く？")
out += b.mini(("答え", "落選した人の一部に、公演の1週間前〜前日ごろメールで届く"))
out += p("案内は、そのツアーに申し込んで落選した人の中から、一部の人にだけ届きます。",
         "どんな人に届くのか、基準は公表されていません。")
out += p("SNSでは「代表者ではなく同行者に案内が来た」「いつもと違う名義に来た」という声もありました。",
         "同じ公演で別の日に当選していると来ないのでは、と考えている人もいます。")
out += h3("届くタイミングは公演によってちがう")
out += p("今回のSixTONESの日産スタジアム公演は、11月21日(土)・22日(日)の16時30分開演です。",
         "SNSでは、" + mk("1週間ほど前に案内が届いた人と、前日に届いた人") + "がいました。")
out += p("名古屋公演の案内が届いたという声や、Snow Manの案内を待つ声も出ています。",
         "公演の直前は、メールをこまめに見ておくのがおすすめです。")

out += h2("制作開放の当落はいつ分かる？")
out += b.mini(("答え", "公演前日の夕方ごろ、当選メールで分かることが多い"))
out += p("日産スタジアム初日(11月21日)の分は、" + mk("前日20日の17時半すぎから") + "当選の報告が続きました。",
         "前の年の公演でも、当選メールは18時台に届いたという声があります。")
out += p("前日の夕方に分かるので、当たってから準備する時間はほとんどありません。",
         "「明日なのに防寒の用意をしていない！」という声がたくさん出ていたのはこのためです。")
out += h3("支払いの動きで先に気づく人も")
out += p("SNSでは、PayPayやクレジットカードの支払いの動きで、メールより先に気づいたという声もありました。",
         "反対に、支払いが取り消された通知で落選が分かった人もいます。")
out += p("ただし、これは公式の案内ではなく、SNSの体験談です。",
         "正式な結果は、届いたメールやファンクラブのページで確かめてください。")

out += h2("制作開放は1枚しか申し込めない？")
out += b.mini(("答え", "今回は「1名義1枚で同行者なし」という声が多い"))
out += p("今回の案内について、" + mk("「1枚でしか申し込めなかった」") + "という声がたくさん出ています。",
         "同行者を登録できず、1人で行く形になるようです。")
out += p("「制作開放こそ誰かと行きたかった」という残念がる声もありました。",
         "ただ、申し込める枚数は公演ごとの案内で決まるので、届いたメールの内容を必ず確かめましょう。")
out += h3("リセールといっしょに申し込める？")
out += p("「公式リセールと同じ日に、制作開放にも申し込めるの？」という質問も出ていました。",
         "こうした決まりは公演ごとにちがうので、案内メールの注意書きを読んで判断してください。")

out += h2("制作開放席は後ろや見切れ確定？")
out += b.mini(("答え", "後ろ・ステージ横が多いが、ふつうに見える席のこともある"))
out += p("制作開放席は、機材を置くかもしれなかった場所なので、" + mk("後ろの方やステージの横") + "になりやすいです。",
         "SNSでも「一番後ろだった」という声がありました。")
out += p("一方で、「ステージ横かと思ったら、ちゃんとした席が用意されていた」という声もあります。",
         "どこになるかは当日まで分からないので、双眼鏡を持っていくと安心です。")
out += p("見切れ席(ステージの一部が見えにくい席)として出る場合は、案内にその説明が書かれるのがふつうです。",
         "申し込む前に、メールの席の説明をよく読んでおきましょう。")
out += h3("スタジアムは寒さ対策も大切")
out += p("日産スタジアムは屋根のない屋外の会場で、11月下旬の夜はかなり冷えます。",
         "制作開放で当たった人は、前日の夜にあわてないよう、防寒の服やカイロを先に用意しておくと安心です。")

out += h2("制作開放に当たったら気をつけること")
out += b.checks(["当選メールの入場方法(電子チケットなど)をすぐ確かめる",
                 "1人で入る前提で、時間に余裕をもって会場へ向かう",
                 "席が後ろでも見えるように双眼鏡を用意する",
                 "屋外の会場なら防寒具をしっかり持つ",
                 "チケットの転売や名義の書きかえはしない"])
out += p("STARTOのコンサートは、本人確認が行われることがあります。",
         "決まりを守って、気持ちよく当日を楽しみましょう。")

out += h2("まとめ")
out += b.checks(["制作開放席は、機材の配置が決まったあとに追加で出る席",
                 "案内は落選した人の一部に、公演の1週間前〜前日ごろ届く",
                 "当落は公演前日の夕方ごろ、メールで分かることが多い",
                 "今回は1名義1枚・同行者なしという声が多い",
                 "席は後ろやステージ横が多いが、ふつうの席のことも"])
out += p("落選してもまだチャンスがあるのが、制作開放席のうれしいところですね。",
         "案内が届いたら、当たったときの準備を先にしておいてはいかがでしょうか！")

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
