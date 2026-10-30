# -*- coding: utf-8 -*-
"""Snow Man / Travis Japan / KEY TO LIT の「メンバーの入所日一覧」記事3本を組み立てて下書き投稿する(2026-10-30)。

usage: python tools/_build_join_dates_1030.py [--dry] [snowman|travis|ktl ...]
--dry: articles/join_dates_{key}_1030.html を書き出すだけで投稿しない。
投稿済みのキーは articles/join_dates_1030_posted.json に記録して二重投稿しない。
タイトルはともき確認待ちの【未】付き。入所日はSTARTO ENTERTAINMENT公式プロフィール準拠の各種名鑑・報道で確認。
"""
import os, sys, json, base64, socket, subprocess, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from honorific import add_san  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTED = os.path.join(REPO, "articles", "join_dates_1030_posted.json")
DRY = "--dry" in sys.argv

# docs/wordpress.md の投稿者表(USER1=momo=2 / Tomoki=anco=1)
AUTHORS = {"USER1": 2, "Tomoki": 1}

# 本文に出てくるメンバー以外の人名(「さん」付け用)
OTHERS = ("京本大我", "ジェシー", "山田涼介", "橋本良亮", "佐藤勝利", "原嘉孝", "神宮寺勇太", "林蓮音", "松村北斗",
          "髙橋優斗", "黒田光輝", "横原悠毅", "藤井流星", "重岡大毅", "中山優馬", "ジャニー喜多川", "長瀬智也",
          "二宮和也", "木村拓哉", "亀梨和也", "髙橋海人", "マイケル・ジャクソン", "トラヴィス・ペイン",
          "目黒蓮", "ラウール", "宮近海斗", "中村海人", "松倉海斗", "岩﨑大昇", "佐々木大光")


class Style:
    def __init__(self, acc, line, bg, mk):
        self.acc, self.line, self.bg, self.mk = acc, line, bg, mk

    def p(self, *lines):
        return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n"

    def mark(self, t):
        return f'<strong><span style="font-size:1.1em;background:linear-gradient(transparent 60%,{self.mk} 60%);">{t}</span></strong>'

    @staticmethod
    def h2(t):
        return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n'

    @staticmethod
    def h3(t):
        return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n'

    @staticmethod
    def raw(s):
        return "<!-- wp:html -->\n" + s + "\n<!-- /wp:html -->\n"

    def listbox(self, title, items):
        lis = "\n".join(f"<li>{i}</li>" for i in items)
        return self.raw(f'<div style="border:1px solid {self.acc};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{self.acc};color:#fff;">{title}</p>\n'
                        f'<ul style="margin:0;padding:12px 18px 12px 34px;background:{self.bg};">\n{lis}\n</ul>\n</div>')

    def keybox(self, rows):
        out = [f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>' for i, (k, v) in enumerate(rows)]
        return self.raw(f'<div style="border:1px solid {self.line};border-left:4px solid {self.acc};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{self.bg};">\n'
                        + "\n".join(out) + "\n</div>")

    def table(self, rows, colors=None):
        # colors: 行ごとのメンバーカラー(淡色)。見出し行は除く
        trs = []
        for i, r in enumerate(rows):
            if i == 0:
                st = f' style="background:{self.bg};font-weight:bold;"'
            elif colors and colors[i - 1]:
                st = f' style="background:{colors[i - 1]};"'
            else:
                st = ""
            trs.append("<tr>" + "".join(f"<td{st}>{c}</td>" for c in r) + "</tr>")
        return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
                + "".join(trs) + "</tbody></table></figure>\n<!-- /wp:table -->\n")

    def related(self, items):
        lis = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in items)
        return self.raw(f'<div style="border:1px solid {self.line};border-left:4px solid {self.acc};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;">\n'
                        f'<p style="margin:0 0 6px 0;font-weight:bold;color:{self.acc};">あわせて読みたい</p>\n<ul style="margin:0;padding-left:20px;">{lis}</ul>\n</div>')


ART = {}

# ================================================================ Snow Man
S = Style("#3d5a80", "#c9d6e6", "#eef3f8", "#d6e2f0")
SM_COL = {"岩本照": "#fdf6d8", "深澤辰哉": "#efe6f7", "ラウール": "#f6f6f6", "渡辺翔太": "#e3eefa", "向井康二": "#fdeadb",
          "阿部亮平": "#e4f4e6", "目黒蓮": "#e6e6e6", "宮舘涼太": "#fbe3e3", "佐久間大介": "#fce6f0"}
sm_rows = [("深澤辰哉", "2004年8月12日", "12歳"), ("阿部亮平", "2004年8月12日", "10歳"), ("渡辺翔太", "2005年6月26日", "12歳"),
           ("佐久間大介", "2005年9月25日", "13歳"), ("宮舘涼太", "2005年10月1日", "12歳"), ("岩本照", "2006年10月1日", "13歳"),
           ("向井康二", "2006年10月8日", "12歳"), ("目黒蓮", "2010年10月30日", "13歳"), ("ラウール", "2015年5月2日", "11歳")]
sm_jr = {"深澤辰哉": "15年5か月", "阿部亮平": "15年5か月", "渡辺翔太": "14年6か月", "佐久間大介": "14年3か月", "宮舘涼太": "14年3か月",
         "岩本照": "13年3か月", "向井康二": "13年3か月", "目黒蓮": "9年2か月", "ラウール": "4年8か月"}

ART["snowman"] = dict(
    site="CHOMO2", categories=[4, 5],
    title="【未】Snow Manの入所日一覧！9人の入所順と同期は誰？",
    slug="snow-man-member-join-dates",
    eyecatch=("tools/eyecatch_snowman.py", "入所日一覧", ["9人の入所順と", "同期は誰？"]),
    html="".join([
        S.p("Snow Manのメンバーは、いつジャニーズ事務所(現STARTO ENTERTAINMENT)に入ったのでしょうか。",
            f"一番早いのは{S.mark('2004年8月12日の深澤辰哉と阿部亮平')}で、2人は同じ日の入所です。",
            f"一番最後は{S.mark('2015年5月2日のラウール')}で、最初の2人とは10年以上の差があります。",
            "この記事では、9人の入所日を入所順に並べ、入所のきっかけや同期、デビューまでのJr.歴をまとめました。"),
        S.listbox("この記事でわかること", ["9人の入所日と入所したときの年齢", "入所が一番早いメンバー・遅いメンバー",
                                      "メンバーごとの入所のきっかけ", "同じ日に入った同期は誰？", "デビューまでのJr.歴"]),
        S.h2("Snow Manの入所日一覧"),
        S.p("9人の入所日を、入所が早い順に並べました。",
            "年齢は生年月日から計算した、入所した日の年齢です。"),
        S.table([["メンバー", "入所日", "入所時の年齢"]] + [list(r) for r in sm_rows], [SM_COL[r[0]] for r in sm_rows]),
        S.keybox([("一番早い", "深澤辰哉・阿部亮平(2004年8月12日)"), ("一番遅い", "ラウール(2015年5月2日)"),
                  ("一番若く入所", "阿部亮平(10歳)"), ("同じ日に入所", "深澤辰哉と阿部亮平")]),
        S.p("入所日は、STARTO ENTERTAINMENTの公式プロフィールをもとにした名鑑や報道で確認できる日付です。",
            "ラウールは『ジャニーズJr. MEIKAN 2019』で「2015年5月12日」と書かれており、資料によって日付が少し違います。"),
        S.h2("入所順に見るSnow Man"),
        S.p("結成時の6人(岩本照・深澤辰哉・渡辺翔太・阿部亮平・宮舘涼太・佐久間大介)は、2004年から2006年の約2年の間に入所しています。",
            "2019年に加入した3人(向井康二・目黒蓮・ラウール)のうち、向井康二は岩本照の1週間後の入所で、結成メンバーとほぼ同じ時期です。"),
        S.p("一方で、目黒蓮は2010年、ラウールは2015年の入所です。",
            f"{S.mark('最年長組の深澤辰哉・渡辺翔太・佐久間大介と、最年少のラウールの入所には10年前後の開き')}があり、Jr.時代の長さは人によって大きく違います。"),
        S.h2("メンバーごとの入所のきっかけ"),
        S.h3("深澤辰哉:2004年8月12日"),
        S.p("深澤辰哉は小学6年生のとき、母親が応募したバラエティ番組『Ya-Ya-yah』の追加オーディションに連れて行かれました。",
            "何をするのか分からないまま会場に着き、そこがジャニーズ事務所のオーディションだったそうです。",
            "最初の選考では落ちたものの、敗者復活で再び呼ばれ、約3500人の中から最終審査まで残って入所しました。"),
        S.h3("阿部亮平:2004年8月12日"),
        S.p("阿部亮平も、深澤辰哉と同じ『Ya-Ya-yah』のオーディションを受けて入所しました。",
            "当時は小学5年生で、9人の中で一番若い10歳での入所です。",
            "審査を次々と通過し、5次審査の収録のあとに「ここまで来たんだから入りたい」と思うようになったと話しています。"),
        S.h3("渡辺翔太:2005年6月26日"),
        S.p("渡辺翔太は、母親が妹のおもちゃのプレゼントに応募するついでに履歴書を送ったのがきっかけです。",
            "「NHKスタジオパークに行こう」と誘われてついて行くと、隣の部屋がオーディション会場でした。",
            "踊るだけ踊って帰るつもりが、ダンスを見たジャニー喜多川に「君いいよ」と声をかけられ、合格しています。"),
        S.h3("佐久間大介:2005年9月25日"),
        S.p("佐久間大介が通っていたダンス教室の先生は、少年隊のバックで踊っていた元Jr.でした。",
            "先生の奥さんに「履歴書送ってみたら？」とすすめられ、母親が履歴書を送りました。",
            "オーディションではジャニー喜多川に特技を聞かれてロンダートを披露し、「あの子踊れるね」と言われたそうです。"),
        S.h3("宮舘涼太:2005年10月1日"),
        S.p("宮舘涼太は、母親が本人に内緒で履歴書を送りました。",
            "「買い物に行く」と誘われて原宿へ行くと、着いた建物がオーディション会場だったそうです。",
            "100人以上の中で一番前に出てダンスを踊り、歌では「世界に一つだけの花」を歌いました。",
            "ずっと近くで見ていた人がジャニー喜多川だったことは、あとから知ったといいます。"),
        S.p("幼なじみの渡辺翔太とは、入所日が約3か月違います。",
            "同じ日に入ったわけではなく、別々のオーディションから事務所で一緒になりました。"),
        S.h3("岩本照:2006年10月1日"),
        S.p("岩本照は、マイケル・ジャクソンに憧れてダンスを仕事にしたいと考え、自分で履歴書を送りました。",
            "オーディションはKAT-TUNのデビューコンサートの会場で行われ、簡単な振り付けの審査だけでは納得できず、終わったあとにジャニー喜多川と振付師に直談判しています。",
            "約2時間踊りを見てもらった結果、「YOU出ちゃいなよ」と言われ、翌日の公演に出ることが決まりました。"),
        S.h3("向井康二:2006年10月8日"),
        S.p("向井康二は、タイで通っていたムエタイの道場に飾られていた写真が、見学に来たジャニー喜多川の目に留まりました。",
            "帰国していた自宅に電話がかかってきて、母親は最初いたずらだと思って切ったものの、1日に5回も連絡が来るほど熱心に誘われたそうです。",
            "大阪城ホールでジャニー喜多川と会い、関西ジャニーズJr.として活動を始めました。"),
        S.h3("目黒蓮:2010年10月30日"),
        S.p("目黒蓮は中学2年生、13歳のときの入所です。",
            "オーディションには何千人もの参加者がいて、その会場で原嘉孝と意気投合したことが知られています。"),
        S.h3("ラウール:2015年5月2日"),
        S.p("ラウールは小学6年生のとき、将来ダンスを仕事にしたいと考えていくつかの事務所のオーディションを受けていて、その流れで親が履歴書を送りました。",
            "ダンスが振付師の目に留まったことも、入所が決まる理由になったとされています。"),
        S.h2("同じ日に入った同期は誰？"),
        S.p("同じ日に入所したメンバーや、ほかのグループの同期をまとめました。"),
        S.table([["メンバー", "同期"],
                 ["深澤辰哉・阿部亮平", "山田涼介(Hey! Say! JUMP)、橋本良亮(A.B.C-Z)"],
                 ["岩本照", "京本大我(SixTONES)"],
                 ["向井康二", "藤井流星・重岡大毅(WEST.)、中山優馬"],
                 ["目黒蓮", "佐藤勝利・原嘉孝(timelesz)、宮近海斗・中村海人・松倉海斗(Travis Japan)"],
                 ["ラウール", "岩﨑大昇・佐々木大光(KEY TO LIT)、髙橋優斗"]]),
        S.p(f"深澤辰哉と阿部亮平は、{S.mark('同じ日に入所した「同期コンビ」')}です。",
            "岩本照は、SixTONESの京本大我が「唯一の同期」とされています。"),
        S.p("目黒蓮が入所した2010年10月30日は、Travis Japanの宮近海斗・中村海人・松倉海斗の3人と同じ日です。",
            "ラウールの2015年5月2日も、KEY TO LITの岩﨑大昇・佐々木大光と同じ日の入所です。"),
        S.h2("デビューまでのJr.歴"),
        S.p("Snow Manは2020年1月22日、SixTONESとの「D.D. / Imitation Rain」でCDデビューしました。",
            "入所日からデビュー日までの期間(Jr.歴)は、次のとおりです。"),
        S.table([["メンバー", "入所日", "デビューまで"]] + [[r[0], r[1], sm_jr[r[0]]] for r in sm_rows],
                [SM_COL[r[0]] for r in sm_rows]),
        S.p(f"深澤辰哉と阿部亮平は、{S.mark('Jr.として15年以上')}を過ごしてからのデビューです。",
            "一方、ラウールは入所から4年8か月、高校生でのデビューでした。"),
        S.listbox("まとめ", ["一番早い入所は深澤辰哉・阿部亮平の2004年8月12日(同じ日)", "一番遅い入所はラウールの2015年5月2日",
                           "一番若く入所したのは阿部亮平の10歳", "目黒蓮はTravis Japanの宮近海斗・中村海人・松倉海斗と同じ日の入所",
                           "デビューまでのJr.歴は最長15年5か月、最短4年8か月"]),
        S.related([("Snow Manの追加メンバーは誰？6人から9人になった経緯！", "https://chomoand-2.com/snow-man-added-members-224"),
                   ("Snow Manの平均身長と平均年齢は？背の順も！", "https://chomoand-2.com/snow-man-average-height-age-227")]),
    ]),
)

# ================================================================ Travis Japan
T = Style("#7e57c2", "#d9cdf0", "#f5f2fb", "#ebe4f7")
TJ_COL = {"宮近海斗": "#fbe3e5", "中村海人": "#e2f4ec", "七五三掛龍也": "#fbe8f2", "川島如恵留": "#f1f2f3",
          "吉澤閑也": "#fdf5d9", "松田元太": "#e3eef9", "松倉海斗": "#fde9de"}
tj_rows = [("川島如恵留", "2007年10月14日", "12歳"), ("七五三掛龍也", "2009年2月15日", "13歳"), ("吉澤閑也", "2009年5月24日", "13歳"),
           ("宮近海斗", "2010年10月30日", "13歳"), ("中村海人", "2010年10月30日", "13歳"), ("松倉海斗", "2010年10月30日", "12歳"),
           ("松田元太", "2011年2月10日", "11歳")]
tj_jr = {"川島如恵留": "15年0か月", "七五三掛龍也": "13年8か月", "吉澤閑也": "13年5か月", "宮近海斗": "11年11か月",
         "中村海人": "11年11か月", "松倉海斗": "11年11か月", "松田元太": "11年8か月"}

ART["travis"] = dict(
    site="CHOMO4", categories=[3, 4],
    title="【未】トラジャの入所日一覧！7人の入所順とトリプルカイトの同期は？",
    slug="travis-japan-member-join-dates",
    eyecatch=("tools/eyecatch_torahja_canva.py", "入所日一覧", ["7人の入所順と", "同期は誰？"]),
    html="".join([
        T.p("Travis Japanのメンバーは、いつジャニーズ事務所(現STARTO ENTERTAINMENT)に入ったのでしょうか。",
            f"一番早いのは{T.mark('2007年10月14日の川島如恵留')}、一番最後は{T.mark('2011年2月10日の松田元太')}です。",
            f"そして、宮近海斗・中村海人・松倉海斗の{T.mark('「トリプルカイト」の3人は、2010年10月30日の同じ日の入所')}です。",
            "この記事では、7人の入所日を入所順に並べ、入所のきっかけや同期、デビューまでのJr.歴をまとめました。"),
        T.listbox("この記事でわかること", ["7人の入所日と入所したときの年齢", "入所が一番早いメンバー・遅いメンバー",
                                      "メンバーごとの入所のきっかけ", "トリプルカイトと同じ日に入った同期", "デビューまでのJr.歴"]),
        T.h2("トラジャの入所日一覧"),
        T.p("7人の入所日を、入所が早い順に並べました。",
            "年齢は生年月日から計算した、入所した日の年齢です。"),
        T.table([["メンバー", "入所日", "入所時の年齢"]] + [list(r) for r in tj_rows], [TJ_COL[r[0]] for r in tj_rows]),
        T.keybox([("一番早い", "川島如恵留(2007年10月14日)"), ("一番遅い", "松田元太(2011年2月10日)"),
                  ("同じ日に入所", "宮近海斗・中村海人・松倉海斗(2010年10月30日)"), ("一番若く入所", "松田元太(11歳)")]),
        T.p("入所日は、STARTO ENTERTAINMENTの公式プロフィールをもとにした名鑑や報道で確認できる日付です。",
            "吉澤閑也は『ジャニーズJr. MEIKAN 2019』では「2009年4月」とされていて、資料によって少し違います。"),
        T.h2("入所順に見るトラジャ"),
        T.p("7人の入所は、2007年から2011年の約3年4か月の間に集まっています。",
            "最初の川島如恵留から、七五三掛龍也・吉澤閑也の2009年組、トリプルカイトの2010年組、最後の松田元太と続きます。"),
        T.p("Travis Japanは2012年に、振付師のトラヴィス・ペインのもとで結成されました。",
            "松田元太と松倉海斗は、2017年11月19日に正式加入しています。",
            "入所日は結成メンバーとそれほど変わらず、松倉海斗はトリプルカイトの2人と同じ日の入所です。"),
        T.h2("メンバーごとの入所のきっかけ"),
        T.h3("川島如恵留:2007年10月14日"),
        T.p("川島如恵留は、少年隊主演の舞台『PLAYZONE』の映像に強く刺激を受けたこと、母親の友人からオーディションがあると教えてもらったことがきっかけです。",
            "中学1年生でオーディションに参加し、ジャニー喜多川の前でピルエット(つま先立ちでの回転)4回転を披露しました。"),
        T.h3("七五三掛龍也:2009年2月15日"),
        T.p("七五三掛龍也は、父親が木村拓哉、母親が亀梨和也のファンで、小さいころからコンサートに通っていました。",
            f"小学6年生のときに自分で履歴書を送り、{T.mark('返事が来たのは1年半〜2年ほどあと')}だったそうです。",
            "SixTONESの松村北斗と同じ日の入所とされています。"),
        T.h3("吉澤閑也:2009年5月24日"),
        T.p("吉澤閑也は、KinKi Kidsの曲を聴いて育ち、姉の影響でHey! Say! JUMPの山田涼介に憧れました。",
            "小学4年生で自分から履歴書を送ったものの、そのときは返事が来ませんでした。",
            "2009年4月に日本テレビ系『スクール革命!』の新入生オーディションを受け、新入生には選ばれなかったものの、事務所に入所しています。"),
        T.h3("宮近海斗:2010年10月30日"),
        T.p("宮近海斗は幼稚園のころからサッカーを習っていましたが、小学3年生のときに母親にリズム感のなさを指摘され、ダンス教室に通い始めました。",
            "だんだんサッカーよりダンスに夢中になり、小学5年生でサッカーをやめてオーディションを受けています。"),
        T.h3("中村海人:2010年10月30日"),
        T.p("中村海人は、ドラマ『マイ☆ボス マイ☆ヒーロー』で主演の長瀬智也に憧れ、母親が履歴書を送りました。",
            "最初のオーディションに合格したあと、一度コンサートに呼ばれてからは声がかからなくなりました。",
            f"それでもあきらめきれず、{T.mark('ジャニー喜多川に手紙を送ったところ、もう一度オーディションに呼ばれて合格')}しています。"),
        T.h3("松倉海斗:2010年10月30日"),
        T.p("松倉海斗は、2009年に嵐の10周年ライブを見て二宮和也に憧れ、オーディションを受けました。",
            "入所したのは12歳のときで、宮近海斗・中村海人と同じ日です。"),
        T.h3("松田元太:2011年2月10日"),
        T.p("松田元太は小学4年生のとき、母親に連れられてHey! Say! JUMPのコンサートに行き、山田涼介を見てジャニーズに入ることを決めたそうです。",
            "入所は11歳で、7人の中で一番若い年齢での入所です。"),
        T.h2("トリプルカイトと同じ日に入った同期は誰？"),
        T.p("2010年10月30日は、トリプルカイトの3人のほかにも、のちにデビューするメンバーが多く入所した日です。"),
        T.table([["メンバー", "同じ日に入所した人"],
                 ["宮近海斗・中村海人・松倉海斗", "目黒蓮(Snow Man)、佐藤勝利・原嘉孝(timelesz)、神宮寺勇太、林蓮音"],
                 ["七五三掛龍也", "松村北斗(SixTONES)"]]),
        T.p(f"Snow Manの目黒蓮と、トリプルカイトの3人は{T.mark('同じ日に入所した同期')}です。",
            "同じ時期にJr.として活動を始め、それぞれ別のグループでデビューしました。"),
        T.h2("デビューまでのJr.歴"),
        T.p("Travis Japanは2022年10月28日、「JUST DANCE!」で全世界デジタルデビューしました。",
            "入所日からデビュー日までの期間(Jr.歴)は、次のとおりです。"),
        T.table([["メンバー", "入所日", "デビューまで"]] + [[r[0], r[1], tj_jr[r[0]]] for r in tj_rows],
                [TJ_COL[r[0]] for r in tj_rows]),
        T.p(f"一番長い川島如恵留は、{T.mark('ちょうど15年')}のJr.時代を過ごしてからのデビューです。",
            "7人全員が、11年以上Jr.として活動してからデビューしています。"),
        T.listbox("まとめ", ["一番早い入所は川島如恵留の2007年10月14日", "一番遅い入所は松田元太の2011年2月10日(11歳で一番若い)",
                           "トリプルカイトの3人は2010年10月30日の同じ日に入所", "目黒蓮(Snow Man)もトリプルカイトと同じ日の入所",
                           "デビューまでのJr.歴は全員11年以上、最長は川島如恵留の15年"]),
        T.related([("トラジャのデビュー日はいつ？何周年かとCDデビューも！", "https://chomoand-4.blog/travis-japan-debut-date-1935"),
                   ("トラジャのコンビ名一覧！いちごみるくやトリプルカイトとは？", "https://chomoand-4.blog/travis-japan-combi-names-1927"),
                   ("【Travis Japan】初期メンバー9人？脱退4人の現在は？", "https://chomoand-4.blog/were-there-9-initial-members-o-67")]),
    ]),
)

# ================================================================ KEY TO LIT
K = Style("#3d5a80", "#c9d6e6", "#eef3f8", "#d6e2f0")
KTL_COL = {"岩﨑大昇": "#f1f2f3", "井上瑞稀": "#fbe3e3", "中村嶺亜": "#fce6f0", "猪狩蒼弥": "#e4f4e6", "佐々木大光": "#e3eefa"}
ktl_rows = [("中村嶺亜", "2009年10月3日", "12歳", "7 MEN 侍"), ("井上瑞稀", "2009年10月3日", "8歳", "HiHi Jets"),
            ("猪狩蒼弥", "2013年6月16日", "10歳", "HiHi Jets"), ("佐々木大光", "2015年5月2日", "12歳", "7 MEN 侍"),
            ("岩﨑大昇", "2015年5月2日", "12歳", "美 少年")]
ktl_jr = {"中村嶺亜": "17年2か月", "井上瑞稀": "17年2か月", "猪狩蒼弥": "13年5か月", "佐々木大光": "11年7か月", "岩﨑大昇": "11年7か月"}

ART["ktl"] = dict(
    site="CHOMO5", categories=[4, 5],
    title="【未】キテレツの入所日一覧！5人の入所順と同期は誰？",
    slug="key-to-lit-member-join-dates",
    eyecatch=("tools/eyecatch_kitetsu.py", "入所日一覧", ["5人の入所順と", "同期は誰？"]),
    html="".join([
        K.p("KEY TO LIT(キテレツ)のメンバーは、いつジャニーズ事務所(現STARTO ENTERTAINMENT)に入ったのでしょうか。",
            f"一番早いのは{K.mark('2009年10月3日の中村嶺亜と井上瑞稀')}で、2人は同じオーディションから入所しています。",
            f"一番最後は{K.mark('2015年5月2日の佐々木大光と岩﨑大昇')}で、こちらも同じ日の入所です。",
            "この記事では、5人の入所日を入所順に並べ、入所のきっかけや同期、CDデビューまでのJr.歴をまとめました。"),
        K.listbox("この記事でわかること", ["5人の入所日と入所したときの年齢", "入所が一番早いメンバー・遅いメンバー",
                                      "メンバーごとの入所のきっかけ", "同じ日に入った同期は誰？", "CDデビューまでのJr.歴"]),
        K.h2("キテレツの入所日一覧"),
        K.p("5人の入所日を、入所が早い順に並べました。",
            "年齢は生年月日から計算した、入所した日の年齢です。"),
        K.table([["メンバー", "入所日", "入所時の年齢", "前のグループ"]] + [list(r) for r in ktl_rows],
                [KTL_COL[r[0]] for r in ktl_rows]),
        K.keybox([("一番早い", "中村嶺亜・井上瑞稀(2009年10月3日)"), ("一番遅い", "佐々木大光・岩﨑大昇(2015年5月2日)"),
                  ("一番若く入所", "井上瑞稀(8歳)"), ("同じ日に入所", "中村嶺亜と井上瑞稀/佐々木大光と岩﨑大昇")]),
        K.p("入所日は、STARTO ENTERTAINMENTの公式プロフィールをもとにした名鑑や報道で確認できる日付です。"),
        K.h2("入所順に見るキテレツ"),
        K.p("5人の入所日は、2009年・2013年・2015年の3つの日に分かれます。",
            f"5人のうち{K.mark('2組が同じ日の入所')}で、入所日がほかの誰とも重ならないのは猪狩蒼弥だけです。"),
        K.p("KEY TO LITは2025年2月、HiHi Jets・美 少年・7 MEN 侍のメンバーが集まって結成されました。",
            "前のグループはばらばらでも、中村嶺亜と井上瑞稀、佐々木大光と岩﨑大昇は、入所したときから同期だったことになります。"),
        K.h2("メンバーごとの入所のきっかけ"),
        K.h3("中村嶺亜:2009年10月3日"),
        K.p("中村嶺亜は、母親の知り合いが本人に無断で履歴書を送ったのがきっかけです。",
            "当時はスケートボードの大会に真剣に取り組んでいて、最初のオーディションの知らせには行きませんでした。",
            f"2回目の知らせで親に「受かったらスケボーの大会で優勝するよりすごいことだよ」と言われ、{K.mark('受かったらやめるつもりで参加し、合格')}しています。"),
        K.h3("井上瑞稀:2009年10月3日"),
        K.p("井上瑞稀は小学3年生の8歳のとき、Hey! Say! JUMPの山田涼介のダンスに憧れ、自分で履歴書を送りました。",
            "オーディション当日はやる気を見せられなかったものの、同じオーディションを受けていた中村嶺亜と一緒に写真撮影に連れて行かれました。",
            "その場で、Jr.内ユニット「スノープリンス合唱団」への加入が決まったそうです。"),
        K.p("スノープリンス合唱団は、2009年に期間限定で結成された11人組のユニットです。",
            "井上瑞稀は、オーディションを受けたその日にユニットのメンバーに選ばれたことになります。"),
        K.h3("猪狩蒼弥:2013年6月16日"),
        K.p("猪狩蒼弥は、父親の趣味だったローラースケートをスケート場で滑っていたところ、ジャニー喜多川にスカウトされました。",
            "もともとアイドルになりたいと思っていたわけではなかったそうです。",
            "その後、ローラースケートが得意なユニットとして結成されたHiHi Jetsに、井上瑞稀らと一緒に入っています。"),
        K.h3("佐々木大光:2015年5月2日"),
        K.p("佐々木大光はダンスをしていて、同じダンスコンテストに出ていた髙橋海人がテレビ『ザ少年倶楽部』に出ているのを偶然見ました。",
            "それをきっかけに「俺も入ってみようかな」と、事務所への応募を決めたそうです。"),
        K.h3("岩﨑大昇:2015年5月2日"),
        K.p("岩﨑大昇は、母親が履歴書を送ったのがきっかけで、オーディションを受けて入所しました。",
            "佐々木大光とは同じ日の入所で、のちに美 少年と7 MEN 侍で別々のグループに入り、KEY TO LITで同じグループになりました。"),
        K.h2("同じ日に入った同期は誰？"),
        K.p("メンバー同士の同期と、ほかのグループの同期をまとめました。"),
        K.table([["入所日", "同じ日に入所した人"],
                 ["2009年10月3日", "中村嶺亜、井上瑞稀"],
                 ["2015年5月2日", "佐々木大光、岩﨑大昇、ラウール(Snow Man)、髙橋優斗、黒田光輝、横原悠毅(IMP.)"]]),
        K.p(f"佐々木大光と岩﨑大昇が入所した2015年5月2日は、{K.mark('Snow Manのラウールと同じ日')}です。",
            "岩﨑大昇は、元HiHi Jetsの髙橋優斗とも「同期コンビ」として紹介されています。"),
        K.h2("CDデビューまでのJr.歴"),
        K.p("KEY TO LITは2026年12月9日に、ユニバーサルミュージックからCDデビューします。",
            "入所日からデビュー日までの期間(Jr.歴)は、次のとおりです。"),
        K.table([["メンバー", "入所日", "デビューまで"]] + [[r[0], r[1], ktl_jr[r[0]]] for r in ktl_rows],
                [KTL_COL[r[0]] for r in ktl_rows]),
        K.p(f"5人とも{K.mark('Jr.として11年以上')}活動してからのデビューです。",
            "中村嶺亜と井上瑞稀は、17年以上のJr.時代を過ごしてデビューを迎えます。"),
        K.listbox("まとめ", ["一番早い入所は中村嶺亜・井上瑞稀の2009年10月3日(同じオーディション)", "一番遅い入所は佐々木大光・岩﨑大昇の2015年5月2日(同じ日)",
                           "一番若く入所したのは井上瑞稀の8歳", "佐々木大光・岩﨑大昇はSnow Manのラウールと同じ日の入所",
                           "CDデビュー(2026年12月9日)までのJr.歴は全員11年以上"]),
        K.related([("キテレツの結成はいつ？前のグループやファンネーム、メンカラも！", "https://chomoand-5.site/key-to-lit-formation-history-fan-name-34")]),
    ]),
)

GROUP = {"snowman": "snowman", "travis": "travis", "ktl": "ktl"}


def load_env():
    env = {}
    for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env


def req(base, auth, path, data=None, headers=None):
    r = urllib.request.Request(base + path, data=data, method="POST")
    r.add_header("Authorization", "Basic " + auth)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode('utf-8', 'ignore')[:500]}")


def main():
    keys = [k for k in sys.argv[1:] if not k.startswith("--")] or list(ART)
    posted = json.load(open(POSTED, encoding="utf-8")) if os.path.exists(POSTED) else {}
    env = load_env()
    host = socket.gethostname().split(".")[0]
    author = next((v for k, v in AUTHORS.items() if host.lower().startswith(k.lower())), None)
    for k in keys:
        a = ART[k]
        html = add_san(a["html"], GROUP[k], OTHERS)
        path = os.path.join(REPO, "articles", f"join_dates_{k}_1030.html")
        open(path, "w", encoding="utf-8").write(html)
        print(k, "chars", len(__import__("re").sub(r"<[^>]+>", "", html)))
        if DRY:
            continue
        if k in posted:
            print("skip", k, posted[k])
            continue
        if author is None:
            sys.exit(f"hostname {host} の投稿者がdocs/wordpress.mdの表に無いワン")
        s = a["site"]
        base = env[f"WP_{s}_URL"].rstrip("/")
        auth = base64.b64encode(f"{env[f'WP_{s}_USERNAME']}:{env[f'WP_{s}_APP_PASSWORD']}".encode()).decode()
        tool, main_txt, bottoms = a["eyecatch"]
        img = os.path.join(REPO, "images", f"join_dates_{k}_1030_eyecatch.jpg")
        cmd = [sys.executable, tool, "--main", main_txt, "--color-key", "group", "--out", img]
        for b in bottoms:
            cmd += ["--bottom", b]
        subprocess.run(cmd, check=True, cwd=REPO)
        post = req(base, auth, "/wp-json/wp/v2/posts", json.dumps({
            "title": a["title"], "content": html, "slug": a["slug"], "status": "draft",
            "categories": a["categories"], "author": author}).encode("utf-8"), {"Content-Type": "application/json"})
        media = req(base, auth, "/wp-json/wp/v2/media", open(img, "rb").read(),
                    {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{os.path.basename(img)}"'})
        req(base, auth, f"/wp-json/wp/v2/media/{media['id']}", json.dumps({"alt_text": a["title"]}).encode("utf-8"),
            {"Content-Type": "application/json"})
        req(base, auth, f"/wp-json/wp/v2/posts/{post['id']}", json.dumps({"featured_media": media["id"]}).encode("utf-8"),
            {"Content-Type": "application/json"})
        posted[k] = {"id": post["id"], "media": media["id"], "url": f"{base}/?p={post['id']}"}
        json.dump(posted, open(POSTED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("draft", post["id"], "media", media["id"], a["title"])
    for k, v in posted.items():
        print(v["url"], ART[k]["title"])


if __name__ == "__main__":
    main()
