# -*- coding: utf-8 -*-
"""chomoand.com下書き「セットログで垢BANされる？」(2026-11-19 オシリ依頼、ネタ見張りの速報から)。

根拠: setlog公式 利用規約(2026-09-19施行、setlog.kr/tos)・児童の安全ポリシー(2026-04-08、setlog.kr/csampolicy)、
App Store(13+・無料ソーシャル1位・評価4.6/約5.8万件、11/19時点)、Web担当者Forum/Yahoo!ニュース(学割アプリ調査 8/17)、
Sensor Tower(5月 日本133万DL、isotop/0115765経由)。公式に明確なBAN基準・異議申し立て窓口は無い → そう書く。
ブロック・退出の違いは個人ブログ情報なので「とされています」で。

    python tools/_build_trend_setlog_ban_1119.py                # 下書き投稿
    python tools/_build_trend_setlog_ban_1119.py --build-only
    python tools/_build_trend_setlog_ban_1119.py --update
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "trend"
KEY = "trend_setlog_ban_1119"
TITLE = "セットログで垢BANされる？停止になる行為と通報の仕組みは？"
SLUG = "setlog-account-ban"
CATEGORIES = [37]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.png")
EYECATCH_ALT = "セットログで垢BANされる？"
X_TEXT = ""
X_TAGS = "#セットログ #setlog"

TOS = "https://setlog.kr/tos/"
CSAM = "https://setlog.kr/csampolicy"
APPSTORE = "https://apps.apple.com/jp/app/setlog/id6587576438"
YAHOO = "https://news.yahoo.co.jp/articles/7ef147cc420bc35b0f9fa3e574347395824b3536"
PRTIMES = "https://prtimes.jp/main/html/rd/p/000000135.000041941.html"
MEDIA_CACHE = blogkit.ARTICLES / (KEY + "_media.json")
PHOTOS = {  # 画像はZ Venture Capitalのプレスリリース(PR TIMES 2026-10-28)のもの
    "app": (blogkit.ROOT / "images" / (KEY + "_app.jpg"), "セットログ(setlog)のアプリ画面(撮影・ログ・メッセージ)"),
}

b = blogkit.Blocks("#0f766e", "#99d5cc", "#f0fbf9")
p, h2, h3, mk, L = b.p, b.h2, b.h3, b.mark, b.link


def photo(key):
    import json
    path, alt = PHOTOS[key]
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
                  '出典:<a href="{}" target="_blank" rel="noopener">PR TIMES(Z Venture Capital株式会社)</a></figcaption></figure>'
                  .format(src, alt, w, h, PRTIMES))


out = ""

out += p("Z世代のあいだで広がっている韓国発のアプリ「セットログ(setlog)」。",
         "使っている人が増えるほど気になるのが「垢BAN(アカウント停止)ってあるの？」という点です。")
out += p("結論から言うと、" + mk("セットログにも垢BANはあります。"),
         "公式の利用規約には、ルール違反のときに「利用を制限・終了できる」と書かれています。",
         "子どもを守るためのルールでは「停止」や「永久BAN」まではっきり書かれています。")
out += p("ただし、何回で停止になるのかといった細かい基準は公開されていません。",
         "BANされたときの異議申し立ての窓口も、規約には書かれていません。")
out += b.wakaru([
    "セットログで垢BANはあるのか(公式の規約から)",
    "停止になりやすい行為はどれか",
    "13歳未満が使うとどうなるか",
    "通報・ブロックの仕組み",
    "BANされたかも？と思ったときの対処法",
])

out += h2("セットログとは？日本のZ世代に広がる理由")
out += p("セットログは、1日の中の短い動画を撮りためて、自動でVlogにしてくれるアプリです。",
         "通知に合わせて約2秒の動画を撮ると、1日分がつながって1本の動画になります。")
out += b.mini(("アプリ名", "setlog(セットログ)"),
              ("開発元", "New Chat Inc.(韓国ソウルとアメリカに拠点)"),
              ("対象年齢", "13歳以上(App Storeでも13+)"),
              ("料金", "無料"),
              ("人気", "App Storeの無料ソーシャルで1位(2026年11月19日時点)"))
out += photo("app")
out += p("2026年10月のプレスリリースでは、" + mk("いまは日本がいちばん大きな市場") + "だと発表されました。",
         "日本では1日に約750万人が使っているそうです。")
out += p("App Storeでの評価は5点中4.6で、約5.8万件の評価が集まっています。",
         "調査会社Sensor Towerのデータでは、2026年5月の日本のダウンロード数は約133万件でした。",
         "この月は、本場の韓国を上回ったと伝えられています。")
out += p("学割アプリの調査(学生479人)では、" + mk("約74%が「使っている」") + "と答えました。",
         "使い始めたきっかけは「友だちに招待された」が約71%で一番多かったそうです("
         + L(YAHOO, "Yahoo!ニュース") + ")。")
out += p("友だち同士の招待でどんどん広がるので、「とりあえず入れた」という人も多いはずです。",
         "だからこそ、ルールを知らずに使ってトラブルになる心配も出てきます。")

out += h2("セットログで垢BANはある？公式の規約を確認")
out += h3("利用規約に「利用を制限・終了できる」とある")
out += p("セットログの" + L(TOS, "利用規約") + "は、2026年9月19日から新しい内容になっています。",
         "その中に、会社がアカウントを止められるという決まりがあります。")
out += p("内容をやさしく言いかえると、次のとおりです。")
out += b.checks(["規約に違反したと考えられるとき、会社は利用を制限したり終了したりできる",
                 "安全や法律の面で危ないと考えられるときも同じ",
                 "できる場合は、そのことを本人に知らせる"])
out += p("つまり、" + mk("違反が「疑われる」だけでも止められる") + "書き方になっています。",
         "「できる場合は知らせる」なので、お知らせなしで止まる可能性もゼロではありません。")
out += h3("子どもを守るルールには「永久BAN」まで書かれている")
out += p("セットログは、利用規約とは別に" + L(CSAM, "「児童の安全ポリシー」") + "も出しています。",
         "子どもを傷つける投稿や行為は、きびしく禁止されています。")
out += p("違反したときの対応として、投稿の削除や機能の制限が書かれています。",
         "さらに、" + mk("アカウントの停止や永久BAN") + "もはっきり書かれています。",
         "悪質なときは、警察などに知らせるとも書かれています。")

out += h2("セットログで停止になりやすい行為は？")
out += p("利用規約の「禁止されていること」をまとめると、次の表のようになります。",
         "右の列は「たとえばこんなこと」というイメージです(当サイトの例)。")
out += b.table(("禁止されていること", "たとえば"), [
    ("法律や規約を破ること", "人の顔や家を勝手に流す"),
    ("他人のアカウントや情報を勝手に使う", "友だちのスマホでなりすまし投稿"),
    ("アプリの動きをじゃまする", "不具合をわざと悪用する"),
    ("許可なくbotや自動ツールを使う", "外部ツールで動画を自動で集める"),
    ("人をいじめる・おどす", "ログ内で悪口を言い続ける"),
    ("人の権利をおかす・有害な投稿", "他人のプライベートを撮って流す"),
])
out += p("いちばん気をつけたいのは、" + mk("周りの人が写りこむ動画") + "です。",
         "セットログは通知のタイミングで撮るので、教室や電車で人が写りがちです。")
out += p("中高生のあいだでは、授業中に撮ることがマナーの問題になっているとも言われています。",
         "勝手に撮られた人が嫌な思いをすれば、通報されてもおかしくありません。",
         "「人の権利をおかす投稿」と見られる可能性もあるので、人が写らない向きで撮るのが安心です。")
out += h3("写真や動画は「仲間うち」でも安心しきらない")
out += p("セットログは、招待コードを知っている人しか見られない仕組みです。",
         "ただ、仲間うちの動画でも、メンバーが画面録画などで外に出すことはできます。")
out += p("仲間うちだからと気をゆるめず、外に出ても困らない動画だけを撮るのが大切です。")

out += h2("13歳未満がセットログを使うとどうなる？")
out += p("利用規約では、" + mk("セットログを使えるのは13歳以上") + "と決められています。",
         "住んでいる国の法律がもっと上の年齢を決めていれば、そちらに合わせます。")
out += p("児童の安全ポリシーでも、13歳未満と知りながら使わせることはしないと書かれています。",
         "そのため、年齢をごまかして登録していると分かれば、アカウントを消される可能性があります。")
out += p("小学生のきょうだいが、お兄さん・お姉さんのまねをして入れるケースもありそうです。",
         "家族で使うなら、年齢の決まりを先に確認しておきましょう。")

out += h2("セットログの通報・ブロックの仕組みは？")
out += h3("アプリの中から通報できる")
out += p("児童の安全ポリシーには、アプリの中に通報の機能があると書かれています。",
         "通報できるのは次の4つです。")
out += b.checks(["ユーザー", "メッセージ", "写真・動画", "あやしい行為・有害な行為"])
out += p("つまり、嫌な動画やいやがらせを受けたときは、アプリから運営に知らせられます。",
         "子どもの安全に関わることは、運営のメールにも直接知らせられます。")
out += h3("ブロックとログからの退出はちがう")
out += p("使い方を紹介しているブログなどでは、ブロックと退出は別の機能だとされています。",
         "退出はログ(グループ)から抜けること、ブロックは特定の相手との関係を切ることです。")
out += p("一度ログから抜けると、自分だけでは元に戻れないことが多いとされています。",
         "もう一度入るには、メンバーから招待コードをもらう必要があります。")
out += p("新しい人を入れたくないときは「ルームロック」をオンにする方法もあります。",
         "知らない人が入ってくるのが心配なら、こちらも使ってみてください。")

out += h2("セットログで垢BANされたかも？と思ったら")
out += h3("まずは「ただの不具合」かを確かめる")
out += p("ログインできないときは、BANではなく不具合のことも多いです。",
         "アプリを最新にする、一度ログアウトしてから入り直す、スマホの空き容量を見る、を試しましょう。")
out += p("iPhoneでパスキーを使っている人は、別のApple IDで入れ直すとログインできないことがあります。",
         "機種変更のあとに入れなくなったときは、Apple IDが同じかを確かめてください。")
out += h3("それでもダメなら運営にメールする")
out += p("利用規約には、BANへの異議申し立ての手順は書かれていません。",
         "そのため、公式サイトにのっている問い合わせ用のメール(hi@newchat.kr)に送るのが現実的です。")
out += p("送るときは、登録しているアカウントの情報と、いつから使えないかを書くと話が早くなります。",
         "運営は韓国とアメリカにあるので、返事に時間がかかったり、英語で返ってきたりする可能性もあります。")

out += h2("セットログでBANされないための使い方")
out += b.checks(["人の顔が写らない向きで撮る(とくに教室・電車・お店)",
                 "授業中やバイト中は撮らない",
                 "友だちのアカウントを勝手に使わない",
                 "外部の自動ツールは使わない",
                 "13歳未満は使わない(年齢をごまかさない)",
                 "嫌なことをされたら、やり返さずに通報する"])
out += p("どれも、ほかのSNSと同じ「ふつうのマナー」です。",
         "1日のほとんどをこまめに撮るアプリなので、そのぶん気をつける場面が多いと考えておきましょう。")

out += h2("まとめ")
out += b.checks(["セットログにも垢BANはある(規約で利用の制限・終了、子どもを守るルールで永久BAN)",
                 "細かいBANの基準や異議申し立ての窓口は公開されていない",
                 "禁止はなりすまし・bot・いじめ・人の権利をおかす投稿など",
                 "使えるのは13歳以上",
                 "通報はアプリの中から、困ったら運営にメール"])
out += p("2秒だけの動画でも、写っている人にとっては大切なプライバシーです。",
         "みんなが気持ちよく使えるように、撮る前にちょっとだけ周りを見てから撮りたいですね。")
out += p("参考: " + L(TOS, "setlog 利用規約") + "/" + L(CSAM, "setlog 児童の安全ポリシー")
         + "/" + L(APPSTORE, "App Store setlog"))

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
