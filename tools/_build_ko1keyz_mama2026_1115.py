# -*- coding: utf-8 -*-
"""KO1KEYZ「2026 MAMA AWARDS」出演は何時から?見方(chomoand-1.com)。2026-11-15 公式サイトのSCHEDULEから。

    python tools/_build_ko1keyz_mama2026_1115.py              # 日本語版を下書き投稿
    python tools/_build_ko1keyz_mama2026_1115.py --build-only
    python tools/_build_ko1keyz_mama2026_1115.py --update
KR/ENは tools/_upload_ko1keyz_mama2026_i18n_1115.py (blog-upload STEP6/7)。
ノミネートや披露曲が発表されたら --update で足す。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "ko1keyz"
KEY = "ko1keyz_mama2026_1115"
TITLE = "【KO1KEYZ】MAMA2026は何時から？出演日と見方まとめ！"
SLUG = "ko1keyz-mama-awards-2026"
CATEGORIES = [66, 62]
NAMES = []
EYECATCH = blogkit.ROOT / "images" / (KEY + "_eyecatch.jpg")
EYECATCH_ALT = "KO1KEYZの2026 MAMA AWARDS出演"

OFFICIAL = "https://ko1keyz.com"
MAMA = "https://mnetjp.com/mama/2026/"
BC = "https://bestcalendar.jp/press/162209"
S = "https://chomoand-1.com/"

b = blogkit.Blocks("#c2410c", "#f2c9a8", "#fff7ef")
L = b.link
out = ""
out += b.p("KO1KEYZ(コイキーズ)が、" + b.mark("11月21日(土)の「2026 MAMA AWARDS」") + "に出演します。",
           "会場は京セラドーム大阪で、授賞式は15時から、レッドカーペットは12時30分からです。",
           "テレビならCSの「Mnet Japan」、スマホなら「Mnet Plus」などで生中継を見られます。")
out += b.p("この記事では、出演する日と時間、家で見る方法、そして同じ日の出演者をまとめました。",
           "※2026年11月15日時点の情報です。")
out += b.wakaru(["MAMAってどんな授賞式？",
                 "KO1KEYZが出るのはいつ？何時から？",
                 "テレビ・スマホでの見方",
                 "同じ日に出演するアーティスト",
                 "MAMAの前後のKO1KEYZの予定"])

out += b.h2("MAMAってどんな授賞式？")
out += b.p("MAMA AWARDSは、韓国のCJ ENMが毎年開いている、アジア最大級の音楽の授賞式です。",
           "K-POPのアーティストが多く集まり、1年間で活やくした歌手やグループに賞がおくられます。",
           "授賞式の中で、アーティストのステージもたっぷり見られるのが特長です。")
out += b.p("2026年は、" + b.mark("11月20日(金)・21日(土)の2日間、京セラドーム大阪") + "で開かれます。",
           "1日目が「CHAPTER 1」、2日目が「CHAPTER 2」とよばれています。")

out += b.h2("KO1KEYZが出るのはいつ？何時から？")
out += b.mini(("イベント", "2026 MAMA AWARDS"),
              ("日にち", "2026年11月21日(土)(2日目・CHAPTER 2)"),
              ("会場", "京セラドーム大阪"),
              ("レッドカーペット", "12:30から"),
              ("授賞式", "15:00から"))
out += b.p("KO1KEYZの公式サイトのスケジュールには、11月21日(土)に「2026 MAMA AWARDS」と書かれています。",
           "2日目の授賞式は15時から、その前の12時30分からはレッドカーペットがあります。")
out += b.p("出典:" + L(OFFICIAL, "KO1KEYZ公式サイト(SCHEDULE)") + "/" + L(BC, "ベストカレンダー(MAMAの時間)"))
out += b.h3("出番の時間はわかる？")
out += b.p("授賞式の中で、何時ごろにKO1KEYZが登場するかは発表されていません。",
           "授賞式は長い時間続くので、出番を見のがしたくない人は、始まりから見ておくのが安心です。",
           "レッドカーペットでは、メンバーがどんな衣装で登場するのかにも注目です。")
out += b.h3("何の賞にノミネートされている？")
out += b.p("11月15日の時点で、KO1KEYZがどの賞の候補になっているか、どの曲を披露するかは確認できていません。",
           "発表があれば、この記事に追記します。")

out += b.h2("テレビ・スマホでの見方")
out += b.p("会場に行けない人も、家から生中継で見ることができます。",
           "見る方法は、大きく分けて3つです。")
out += b.table(("見る方法", "どこで", "ポイント"),
               [("Mnet Japan", "テレビ(CS放送)", "スカパー！などの契約が必要"),
                ("Mnet Smart+", "スマホ・パソコン", "日本向けの配信サービス"),
                ("Mnet Plus", "スマホ・パソコン", "世界に向けた生配信")])
out += b.h3("テレビで見るなら「Mnet Japan」")
out += b.p("テレビで見る場合は、CS放送の「Mnet Japan」で生中継されます。",
           "番組表では、レッドカーペットが12時15分から、2日目の授賞式が15時から20時までの予定です。",
           "スカパー！やケーブルテレビでの契約が必要なので、早めに確かめておきましょう。")
out += b.h3("スマホで見るならMnetの配信")
out += b.p("スマホやパソコンで見るなら、日本向けの「Mnet Smart+」か、世界に向けた「Mnet Plus」の生配信があります。",
           "どちらも、事前にアプリを入れたり、登録したりしておくとスムーズです。",
           "見方のくわしい案内は、" + L(MAMA, "MAMAの日本の公式サイト") + "にのっています。")

out += b.h2("同じ日に出演するアーティスト")
out += b.p("2日目の「CHAPTER 2」には、日本でも人気の高いグループが多く出演します。",
           "第1弾で発表された出演者は、次のとおりです(日にちの分け方は発表時のものです)。")
out += b.table(("日にち", "出演者(第1弾の発表)"),
               [("11/20(金)CHAPTER 1", "ALPHA DRIVE ONE、BABYMONSTER、ENHYPEN、ILLIT、INI、NCT WISH、RESCENE"),
                ("11/21(土)CHAPTER 2", "CORTIS、KiiiKiii、LE SSERAFIM、NAYEON(TWICE)、ZEROBASEONE")])
out += b.p("出演者はこのあとも追加で発表されています。",
           "当日の出演者は、MAMAの公式サイトで最新の情報を確かめてください。")
out += b.p("KO1KEYZは、デビューから2か月ほどで、ドームの授賞式のステージに立つことになります。",
           "大先輩のグループが並ぶ中で、どんなステージを見せるのか注目が集まっています。")

out += b.h2("MAMAの前後のKO1KEYZの予定")
out += b.p("MAMAの週末は、KO1KEYZにとって大きなステージが続きます。")
out += b.table(("日時", "予定"),
               [("11/21(土)9:00", "Mnet「KCON LA 2026 × M COUNTDOWN」字幕版#1(CS)"),
                ("11/21(土)12:30", "MAMA レッドカーペット"),
                ("11/21(土)15:00", "MAMA 授賞式(2日目)"),
                ("11/22(日)", "SAPPORO COLLECTION 2026 AUTUMN/WINTER"),
                ("12/14(月)", "デジタルシングル「White Love」配信")])
out += b.p("MAMAの当日の朝には、アメリカ・ロサンゼルスの「KCON LA 2026」のステージの放送もあります。",
           "そして次の日の11月22日(日)には、札幌の「SAPPORO COLLECTION」に出演します。",
           "大阪から札幌へ、2日続けてのステージです。")
out += b.p("その週のテレビ出演は " + L(S + "ko1keyz-tv-schedule-1115-1121-15789", "【KO1KEYZ】テレビ出演は？11/15〜21の放送予定まとめ") +
           "、新曲については " + L(S + "ko1keyz-white-love-digital-single-15458", "KO1KEYZ新曲White Loveはいつ？") + " でまとめています。")
out += b.h3("大阪の会場の近くでもイベントがある")
out += b.p("MAMAに合わせて、11月9日から21日まで「MAMA FAN FESTA」も開かれています。",
           "11月19日からは、なんばひろばにファン向けのラウンジやフォトゾーンができます。",
           "大阪に行く人は、授賞式の前に立ち寄ってみるのも楽しそうです。")

out += b.h2("まとめ")
out += b.checks(["KO1KEYZは11月21日(土)の「2026 MAMA AWARDS」2日目に出演",
                 "会場は京セラドーム大阪。レッドカーペット12:30〜、授賞式15:00〜",
                 "テレビはCSの「Mnet Japan」、スマホは「Mnet Smart+」「Mnet Plus」",
                 "出番の時間・ノミネート・披露曲はまだ発表されていない",
                 "次の日の11月22日(日)はSAPPORO COLLECTIONに出演"])
out += b.p("デビューの年に、アジア最大級の授賞式のステージに立つKO1KEYZ。",
           "12人がドームでどんなパフォーマンスを見せてくれるのか、今から楽しみです。")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = blogkit.finalize(out, SITE, NAMES)
    if "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (KEY + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (KEY + ".html"))
    else:
        blogkit.upload_draft(SITE, KEY, TITLE, out, SLUG, CATEGORIES, EYECATCH, EYECATCH_ALT, names=NAMES,
                             update="--update" in sys.argv)
