# -*- coding: utf-8 -*-
"""SixTONES「ABRACADABRA」はどの曲?(chomoand-0.com)。2026-11-14 サジェスト穴場◎から。

    python tools/_build_sixtones_abracadabra.py              # 下書き投稿(【未】は blogkit が自動で付ける)
    python tools/_build_sixtones_abracadabra.py --build-only
    python tools/_build_sixtones_abracadabra.py --update
楽天APIが403(11/14)だったので、商品の枠はAmazonだけ。楽天が直ったら枠に足す。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402
import affiliate_box  # noqa: E402
import affiliate_linker  # noqa: E402

SITE = "sixtones"
KEY = "sixtones_abracadabra_1114"
TITLE = "SixTONESのアブラカタブラは何に収録？曲の魅力も！"
SLUG = "sixtones-abracadabra"
CATEGORIES = [15]
NAMES = ["福本莉子", "新井和輝", "レディー・ガガ"]
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "SixTONESのABRACADABRA"

DISCO = "https://www.sixtones.jp/discography/d024/"
BILLBOARD = "https://www.billboard-japan.com/special/detail/4763"

tag = blogkit.load_env().get("AMAZON_ASSOCIATE_TAG", "")
AMAZON = affiliate_linker.build_amazon_search_url("SixTONES バリア 初回盤", tag)
BOX = affiliate_box.build_box(None, None, "SixTONES 14thシングル『バリア』初回盤(CD+DVD)", AMAZON,
                              note="「ABRACADABRA」が入っているのは初回盤だけ", border="#d5d5d5")

b = blogkit.Blocks("#333333", "#d5d5d5", "#f5f5f5")
L = b.link
out = ""
out += affiliate_box.NOTICE + "\n\n"
out += b.p("SixTONESの「ABRACADABRA(アブラカタブラ)」は、14枚目のシングル『バリア』の初回盤に入っている曲です。",
           "通常盤には入っていないので、" + b.mark("聴くなら初回盤を選ぶ") + "必要があります。",
           "この記事では、どのCDに入っているのかと、曲の魅力をまとめました。")
out += b.wakaru(["「ABRACADABRA」が入っているCD",
                 "初回盤・通常盤・MTV Unplugged盤のちがい",
                 "どんな曲？曲の魅力",
                 "表題曲「バリア」とのちがい",
                 "同じ名前のほかの曲との見分け方"])

out += b.h2("結論:『バリア』の初回盤だけに入っている")
out += b.mini(("曲名", "ABRACADABRA"),
              ("入っているCD", "14thシングル『バリア』初回盤(CD+DVD)"),
              ("発売日", "2025年3月19日"),
              ("値段", "1,980円"),
              ("品番", "SECJ-107〜108"))
out += b.p("「ABRACADABRA」は、シングル『バリア』のカップリング曲として作られた新しい曲です。",
           "公式サイトでも、初回盤には表題曲「バリア」に加えて、新曲「ABRACADABRA」が入っていると紹介されています。")
out += BOX + "\n\n"
out += b.p("出典:" + L(DISCO, "SixTONES Official web site(バリア)"))

out += b.h2("『バリア』の3つの形のちがい")
out += b.p("『バリア』は、初回盤・通常盤・MTV Unplugged盤の3つの形で発売されました。",
           "形によって、入っている曲がまったくちがいます。")
out += b.table(("形", "値段", "入っている曲"),
               [("初回盤", "1,980円", "バリア・ABRACADABRA"),
                ("通常盤", "1,210円", "バリア・Snooze・崩壊前夜など"),
                ("MTV Unplugged盤", "4,950円", "バリア・アコースティックのライブ")])
out += b.h3("初回盤")
out += b.p("CDには「バリア」と「ABRACADABRA」の2曲が入っています。",
           "DVDには、「バリア」のミュージックビデオとメイキング、2種類のダンス映像が入っています。")
out += b.h3("初回盤のDVDの中身")
out += b.table(("映像", "内容"),
               [("Music Video", "「バリア」のミュージックビデオ"),
                ("Music Video Making", "ミュージックビデオのメイキング"),
                ("Street Dance Performance Only ver.", "ダンスだけを見られる映像(Street)"),
                ("Museum Dance Performance Only ver.", "ダンスだけを見られる映像(Museum)")])
out += b.p("ダンスだけを見られる映像が2種類入っているのが、初回盤のうれしいところです。",
           "「ABRACADABRA」を聴くついでに、6人のダンスもじっくり楽しめます。")
out += b.h3("通常盤")
out += b.p("新しい曲「Snooze」「崩壊前夜」のほか、「GONG」と「ここに帰ってきて」のリミックスが入っています。",
           "「GONG」のリミックスは、King Gnuの新井和輝さんが手がけました。",
           "「ABRACADABRA」は入っていないので、まちがえないようにしましょう。")
out += b.h3("MTV Unplugged盤")
out += b.p("2024年12月に行われた、アコースティックのライブ「MTV Unplugged: SixTONES」を収めたものです。",
           "CDとDVDのセットで、こちらにも「ABRACADABRA」は入っていません。")

out += b.h2("「ABRACADABRA」はどんな曲？")
out += b.p("「ABRACADABRA」は、" + b.mark("ほとんどが英語の歌詞のクラブミュージック") + "です。",
           "「ABRACADABRA」と歌うサビのフレーズが、一度聴くと耳に残ります。")
out += b.p("音楽サイトのBillboard JAPANでは、どこの国の音楽ともいえない「無国籍なクラブ・ミュージック」と紹介されています。",
           "音の数をおさえたビートが中心で、思ったより軽やかに聴こえる曲だと書かれています。")
out += b.h3("ライブで盛り上がりそうな曲")
out += b.p("Billboard JAPANのコラムでは、「新たなライブアンセムになりそうな一曲だ」と評価されています。",
           "ライブアンセムとは、会場がひとつになって盛り上がる、ライブの定番の曲のことです。")
out += b.p("英語の歌詞が多いので、はじめはむずかしく感じるかもしれません。",
           "でも、サビの「ABRACADABRA」だけでもいっしょに口ずさめるのが楽しいところです。")
out += b.p("出典:" + L(BILLBOARD, "Billboard JAPAN"))

out += b.h2("表題曲「バリア」とのちがい")
out += b.p("表題曲の「バリア」は、大切な人を守る思いを歌った、ロックの曲です。",
           "ジェシーさんと福本莉子さんがダブル主演した映画『お嬢と番犬くん』の主題歌でした。")
out += b.p("一方の「ABRACADABRA」は、「バリア」とは真逆ともいえる雰囲気の曲です。",
           "熱い思いをぶつける「バリア」と、クールに体をゆらす「ABRACADABRA」。",
           "1枚のCDで、SixTONESの" + b.mark("まったくちがう2つの顔") + "を楽しめます。")
out += b.p("『お嬢と番犬くん』は、2026年4月からアマプラでも見放題で配信されています。",
           "映画を見てから2曲を聴きくらべると、ちがいがもっとよくわかります。")

out += b.h2("同じ名前のほかの曲との見分け方")
out += b.p("「アブラカタブラ」は、魔法の呪文として有名な言葉です。",
           "そのため、同じ名前の曲がほかのアーティストにもあります。")
out += b.p("たとえば、2025年にはレディー・ガガさんも「Abracadabra」という曲を出しています。",
           "音楽アプリで探すときは、「SixTONES ABRACADABRA」のように、グループ名といっしょに検索するのがおすすめです。")
out += b.checks(["アーティスト名がSixTONESになっているか",
                 "『バリア』の初回盤に入っている曲か",
                 "曲名がすべて大文字の「ABRACADABRA」か"])

out += b.h2("ABRACADABRAについてよくある質問")
out += b.h3("サブスクで聴ける？")
out += b.p("『バリア』は、2025年5月にサブスクでの配信が始まりました。",
           "ただ、「ABRACADABRA」が入っているかは、使っている音楽アプリで「SixTONES ABRACADABRA」と検索して確かめてください。")
out += b.h3("今から初回盤を買える？")
out += b.p("初回盤は、作られる数が決まっていることが多いCDです。",
           "お店によっては売り切れていることもあるので、通販サイトで在庫を確かめてみましょう。")
out += b.h3("歌詞はどこで見られる？")
out += b.p("歌詞は、初回盤についている歌詞カードで確かめられます。",
           "歌詞サイトにのっているかどうかは、サイトによってちがいます。")

out += b.h2("まとめ")
out += b.checks(["「ABRACADABRA」は14thシングル『バリア』の初回盤だけに入っている",
                 "初回盤は2025年3月19日発売・1,980円",
                 "ほとんどが英語の歌詞のクラブミュージック",
                 "「バリア」とは真逆の雰囲気で、ライブで盛り上がりそうな曲",
                 "探すときは「SixTONES ABRACADABRA」で検索"])
out += b.p("カップリング曲だからこそ、SixTONESの新しい一面が見える1曲です。",
           "いつかライブで、会場みんなで「ABRACADABRA」と叫べる日が来たらうれしいですね。")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    import sixtones_theme
    out = blogkit.finalize(out, SITE, NAMES)
    out = out.replace('<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">',
                      '<div style="border:1px solid #d5d5d5;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">')
    out = sixtones_theme.per_section(out)
    if "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
