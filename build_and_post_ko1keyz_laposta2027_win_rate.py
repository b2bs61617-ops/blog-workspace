# -*- coding: utf-8 -*-
"""LAPOSTA 2027の当選確率は？FC会員先行の倍率を、LAPOSTA 2025の当落アンケートと席数から予想。
chomoand-1.com に JP/KR/EN の下書きを作る(author=momo)。2026-11-04 オシリ依頼。

一次ソース:
- KO1KEYZ公式X https://x.com/ko1keyzofficial/status/2117814122872287555 (2026-11-04 12:00 JST、FC会員先行スタート告知)
- 特設サイト https://cf.lapone.jp/feature/laposta2027
  会員先行 11/4 12:00〜11/15 23:59 / 当落 11/26 20:00 / 入金〜11/30 23:59 / 6グループいずれかのFC会員(コース不問・新規入会可)
  最速先行 10/24〜11/3(まとめて払いコース) / 当落 11/13 20:00
  1公演4枚まで・FCごとに各公演1回・複数FCから申込可 / 指定席15,400円
- LAPOSTA 2025: 東京ドーム3日間で約18万人(Lemino配信告知)、一般発売2025/1/11(予定枚数に達し次第終了)
- SNSの当落アンケート(LAPOSTA 2025):
  FC最速先行 回答約3,600件 約8割がいずれかに当選/2公演以上はほぼ無し/2/1(土)が最も低い、1/31(金)は高め/3枚以上で当選率低下/コンビニ払いやや低め
  FC先行(2次) 回答約390件 約4割が当選/最速・FC先行とも落選が約3割/枚数差は小さい/2/2(日)が申込最多で当選率最低
  座席アンケート 回答約2,170件: 最速先行=アリーナ〜2階14列で全体のおよそ8割、FC先行(5グループ)=2階スタンド1〜16列、
  ゲスト(Kep1er・ZEROBASEONE)のFC先行は最速と同じ範囲、以降dカード・三井・ローチケ系・一般先着と続いた
  ※rules.md: SNSの数字は「SNSの投稿をもとにした」と書き、元投稿へのリンクは貼らない
- X(11/4): 「最速申し込むの忘れてた」「最速昨日まででおわり」「大阪だけ申し込み済」「どこのFCから申し込むと当たる？」の声

python build_and_post_ko1keyz_laposta2027_win_rate.py [--dry]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from ko1keyz_article_kit import WP_URL, HEADERS_AUTH as HA, Ui, wphtml, p, h2, a  # noqa: E402

WORK = ROOT / "images" / "ko1keyz_laposta2027_win_rate"
EYE = ROOT / "images" / "ko1keyz_laposta2027_win_rate_eyecatch.png"
BASE_SLUG = "ko1keyz-laposta-2027-win-rate"

TW = "https://twitter.com/ko1keyzofficial/status/2117814122872287555"
SITE = "https://cf.lapone.jp/feature/laposta2027"

L = lambda pid: f"https://chomoand-1.com/?p={pid}"
REL = {
    "ja": [(L(15186), "KO1KEYZ初のLAPOSTA 2027！FC先行はいつまで？"),
           (L(15387), "KO1KEYZのグループカラーは黄色？ラポスタの宝石6色を検証！")],
    "ko": [(L(15187), "KO1KEYZ 첫 LAPOSTA 2027! FC 선행은 언제까지?"),
           (L(15388), "KO1KEYZ 그룹 컬러는 노란색? LAPOSTA 보석 6색 검증")],
    "en": [(L(15188), "KO1KEYZ's First LAPOSTA 2027: Dates, Tickets & FC Presale"),
           (L(15389), "Is KO1KEYZ's Group Color Yellow? The LAPOSTA 2027 Gems")],
}

ui = Ui("#8a8378", "#ddd9d3", "#f7f6f4", "rgba(138,131,120,0.06)")


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def embed(lang):
    return wphtml(f'<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{TW}">{TW}</a></blockquote>\n'
                  '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def build():
    # ---------------- JP ----------------
    jp_title = "LAPOSTA2027の倍率は？KO1KEYZ会員先行の当選確率！"
    jp = [
        p("11月4日の正午、KO1KEYZ(コイキーズ)の公式Xで『LAPOSTA 2027』のFC会員先行のスタートが告知されました。",
          "最速先行に申し込めなかった人や、月会費コースの人にとっては、ここが最初のチャンスです。",
          "ただ、東京ドームと京セラドームとはいえ6グループの合同ライブなので、「そもそも当たるの？」と気になっている人も多いはずです。"),
        p(f"結論から言うと、{mk('FC会員先行の当選確率は3〜4割前後')}になると予想します。",
          f"前回のLAPOSTA 2025では、SNSの当落アンケートで{mk('最速先行は約8割、2回目のFC先行は約4割')}が当選していました。",
          "この記事では、前回の当落の数字と2027年の席数・申込のルールを比べて、今回の当選確率を予想していきます。"),
        ui.table("LAPOSTA 2027 FC会員先行", [
            ("受付期間", "2026年11月4日(水)12:00〜11月15日(日)23:59"),
            ("当落発表", "11月26日(木)20:00"),
            ("入金期間", "11月26日(木)20:00〜11月30日(月)23:59"),
            ("申し込める人", "JO1・INI・DXTEEN・KO1KEYZ・ME:I・IS:SUEいずれかのFC会員(コース不問・新規入会もOK)"),
            ("当選確率(予想)", "3〜4割前後(前回の同じ段階の先行は約4割)"),
        ]),
        ui.titlebox("この記事でわかること", [
            "LAPOSTA 2025の先行ごとの当選率", "2027年の席数と、前回より増えた・減った条件",
            "FC会員先行の当選確率の予想", "当たりやすい公演・当たりにくい公演",
            "どのFCから申し込むと当たりやすい？", "当選確率を少しでも上げるコツと、落選したときのチャンス"]),

        h2("LAPOSTA 2027の会員先行はいつまで？"),
        ui.minibox("<strong>受付:</strong>11月4日(水)12:00〜11月15日(日)23:59",
                   "<strong>対象:</strong>6グループいずれかのFC会員(月会費コースでもOK)"),
        p("会員先行は、LAPOSTA 2027のFC先行の2回目にあたります。",
          "10月24日〜11月3日に行われた1回目の最速先行は、各FCの「月会費まとめて払いコース」の会員だけが対象でした。",
          f"今回は{mk('コースを問わず、FC会員なら誰でも申し込めます')}。"),
        embed("ja"),
        p("受付が始まった11月4日、Xでは「ラポスタ最速申し込むの忘れてた」「最速昨日まででおわり」という声も見かけました。",
          "最速先行を逃した人も、ここから新しくFCに入る人も、まずはこの会員先行が本命になります。"),
        p("申し込みのルールは最速先行と同じで、1公演につき4枚(自分+同行者3人)まで。",
          "1つのFCからは各公演1回ずつ、4公演すべてに申し込めます。",
          "日程やチケット代、ローソンWEB会員の準備などは、" + a(L(15186), "KO1KEYZ初のLAPOSTA 2027の記事") + "にまとめています。"),

        h2("前回LAPOSTA 2025の当選率は？"),
        ui.minibox("<strong>FC最速先行:</strong>約8割がいずれかの公演に当選(回答約3,600件)",
                   "<strong>FC先行(2回目):</strong>約4割がいずれかの公演に当選(回答約390件)"),
        p("予想の土台にするのは、前回のLAPOSTA 2025(2025年1月31日〜2月2日・東京ドーム3日間)の当落です。",
          "公式から当選率は出ていないので、ここではSNSで集められた当落アンケートをもとにした数字を使います。"),
        ui.table("LAPOSTA 2025の当選率(SNSの当落アンケートより)", [
            ("FC最速先行", "約8割がいずれかの公演に当選。2公演以上の当選はほぼ無し"),
            ("FC先行(2回目)", "約4割がいずれかの公演に当選"),
            ("両方とも落選", "約3割"),
        ]),
        p(f"最速先行は約8割と高めでしたが、{mk('2回目のFC先行になると約4割まで下がっています')}。",
          "しかも最速先行と2回目のFC先行の両方に申し込んで、どちらも外れた人が約3割いました。",
          "当選した人のほうがアンケートに答えやすいので、実際の当選率はこれより少し低かったと考えたほうがよさそうです。"),
        p("2回目のFC先行が厳しくなった理由は、座席の配分にあります。",
          f"公演後の座席アンケートによると、最速先行の当選席はアリーナから2階スタンドの前のほうまで広がっていて、{mk('全体のおよそ8割')}を占めていました。",
          "一方で2回目のFC先行の席は2階スタンドの1〜16列に集まっていて、残りの席を分け合う形だったことがわかります。"),

        h2("2027年は前回より当たりやすい？厳しい？"),
        ui.minibox("<strong>当たりやすくなる点:</strong>公演が3→4公演に増え、席数も約2割増えそう",
                   "<strong>厳しくなる点:</strong>KO1KEYZのファンが新しく加わり、全公演が土日、1人4公演まで申し込める"),
        p("では、2027年は前回と比べてどうなのでしょうか。",
          "条件を1つずつ比べてみると、プラスの材料とマイナスの材料がどちらもあります。"),
        ui.table("LAPOSTA 2025と2027の比較", [
            ("会場・公演数", "2025年:東京ドーム3公演 → 2027年:東京ドーム2公演+京セラドーム大阪2公演"),
            ("席数の目安", "2025年:約18万人(3日間の動員) → 2027年:約22万席(予想)"),
            ("出演", "2025年:5グループ+ゲスト → 2027年:KO1KEYZを加えた6グループ"),
            ("曜日", "2025年:金・土・日 → 2027年:土・日・土・日(すべて週末)"),
            ("1人が申し込める公演数", "2025年:3公演まで → 2027年:4公演まで"),
        ]),
        p("まずプラスの材料は、席の数です。",
          "前回は東京ドーム3日間で約18万人が集まったので、1日あたり約6万人。",
          f"今回は東京ドームの2日間に、コンサートで5万人前後が入る京セラドーム大阪の2日間が加わるので、{mk('全体で約22万席、前回より2割ほど多くなる')}計算です。"),
        p("前回は、Kep1erやZEROBASEONEなどのゲストグループのFCにも、最速先行と同じ範囲の席が割り当てられていました。",
          "今回発表されている出演は、LAPONE所属の6グループだけです。",
          "ゲスト分の席がLAPONEの6グループに回るとすれば、こちらもプラスに働きます。"),
        p("一方でマイナスの材料は、申し込む人が増えることです。",
          "2026年6月にFCができたKO1KEYZのファンにとっては、今回が初めてのLAPOSTA。",
          "初めてのドームに立つ姿を見たいという人は多く、新しくFCに入った人もそのまま申し込む形になります。"),
        p("さらに、前回の初日は平日の金曜日で申込が少なく、当たりやすい公演になっていました。",
          f"今回は{mk('4公演すべてが土日')}なので、そうした「穴場の平日公演」がありません。",
          "1人が申し込める公演数も3公演から4公演に増えたため、申込の数そのものは席数以上に増えると考えられます。"),

        h2("FC会員先行の当選確率は？"),
        ui.minibox("<strong>予想:</strong>FC会員先行の当選確率は3〜4割前後",
                   "<strong>参考:</strong>最速先行は前回と同じく7〜8割前後とみられる"),
        p("ここまでの材料をまとめると、席が増える分と申し込みが増える分がほぼ打ち消し合う形です。",
          f"そのため今回の会員先行も、前回の2回目のFC先行と同じく{mk('いずれかの公演に当たる確率は3〜4割前後')}になると予想します。"),
        p("言い換えると、会員先行だけに申し込んだ場合、当たる人より外れる人のほうが多い計算です。",
          "最速先行の時点で席の大半が埋まる流れは前回と同じとみられ、会員先行の席は2階スタンドなど上のほうが中心になる可能性が高いでしょう。"),
        p("ただし、この数字はあくまで前回のアンケートと席数から出した目安です。",
          "最速先行の当落が11月13日(金)に出れば、今回の当選率の傾向も少し見えてくるはずです。"),

        h2("当たりやすい公演・当たりにくい公演は？"),
        ui.minibox("<strong>人気が集まりそう:</strong>2月7日(日)の大阪最終日・1月24日(日)の東京2日目",
                   "<strong>比較的ねらい目:</strong>土曜日の公演(1月23日・2月6日)"),
        p("前回のアンケートでは、申込がいちばん多く当選率が低かったのは最終日の日曜日でした。",
          "最速先行では、土曜日の2日目も当選率が低めだったという結果が出ています。"),
        ui.table("公演ごとの予想", [
            ("1月23日(土) 東京ドーム", "18:00開演。東京初日でやや人気"),
            ("1月24日(日) 東京ドーム", "17:00開演。東京の最終日で人気が集まりそう"),
            ("2月6日(土) 京セラドーム大阪", "18:00開演。比較的ねらい目"),
            ("2月7日(日) 京セラドーム大阪", "16:00開演。ツアー最終日で、日帰りもしやすい"),
        ]),
        p("今回は東京と大阪で会場が分かれるので、住んでいる場所によって申し込みが散らばります。",
          "Xでも「大阪だけ申し込み済」「念願の大阪」という関西のファンの声がありました。",
          "最終日の2月7日は16時開演で遠方からでも日帰りしやすく、オーラスでもあるので、いちばんの激戦になりそうです。"),
        p("前回、何公演に申し込んだかと当選率の間には、はっきりした関係は見られませんでした。",
          "行ける公演があるなら、4公演すべてに申し込んでおくほうがチャンスは広がります。"),

        h2("どのFCから申し込むと当たりやすい？"),
        ui.minibox("<strong>結論:</strong>FCごとの席の割り当ては公表されておらず、前回もグループごとの大きな差は見られなかった"),
        p("Xでは「どこのFCから申し込むと当たるかな」「会員数によって当選枠違うよね？」と悩む声も出ています。",
          "LAPOSTAは複数のFCに入っていれば、それぞれのFCから申し込めるので、気になるところです。"),
        p("ただ、各FCにどれだけ席が割り当てられているかは公表されていません。",
          "前回のアンケートでも、平日初日だけDXTEENとIS:SUEのFCの当選率が高めに出たものの、回答が少なく参考程度とされていました。",
          f"今のところ、{mk('「このFCなら当たりやすい」と言える材料はありません')}。"),
        p("複数のFCに入っている人がそれぞれから申し込むのは、ルールとして認められています。",
          "ただし、同じ公演に重複して当たった場合も入金は必要で、当選後のキャンセルや譲渡はできません。",
          "行ける枚数を考えたうえで申し込みましょう。"),

        h2("当選確率を上げるコツは？"),
        ui.minibox("<strong>枚数:</strong>2枚までにする",
                   "<strong>支払い:</strong>クレジットカード払いを選ぶ",
                   "<strong>準備:</strong>ローソンWEB会員の情報をFCの登録情報とそろえる"),
        p(f"前回の最速先行のアンケートでは、{mk('1〜2枚の申し込みに比べて、3枚以上では当選率が下がる傾向')}が出ていました。",
          "コンビニ払いでは3枚以上の当選報告が0件で、コンビニ払いのほうがやや当選率が低めだったという結果もあります。",
          "抽選の仕組みは公表されていませんが、まとまった枚数の席は残りにくいので、迷ったら2枚以下にしておくのが無難です。"),
        p("また、ローソンWEB会員の名前や生年月日がFCの登録情報と違っていると、申し込みが無効になる場合があります。",
          "同行者のPlus member IDも、締め切り前に用意しておきましょう。",
          "受付の始まりと締め切り間際はアクセスが集中しやすいので、11月15日(日)より前に余裕をもって申し込むのがおすすめです。"),

        h2("会員先行で落選したらもうチャンスはない？"),
        ui.minibox("<strong>前回の流れ:</strong>FC先行のあとに、dカードGOLD先行・ローチケ関連の先行・一般発売(先着)まで続いた"),
        p("会員先行で外れても、まだあきらめる必要はありません。",
          "前回のLAPOSTA 2025では、FC先行のあとにdカードGOLD会員の先行や、ローチケのプレリクエスト先行、三井ショッピングパークの先行などが続きました。"),
        p("最後は2025年1月11日の一般発売(先着)まで行われていて、2階スタンドの後ろのほうの席が出ています。",
          "公演の直前には公式トレード(譲渡・再販)も用意されていました。",
          "2027年の一般発売や他の先行はまだ発表されていないので、続報を待ちましょう。"),

        h2("まとめ"),
        ui.summary([
            "LAPOSTA 2027のFC会員先行は11/4(水)12:00〜11/15(日)23:59、コース不問で申し込める",
            "前回LAPOSTA 2025は最速先行が約8割、2回目のFC先行が約4割の当選(SNSの当落アンケートより)",
            "2027年は席が約2割増えるが、KO1KEYZのファンが加わり全公演が土日になる",
            "FC会員先行の当選確率は3〜4割前後と予想",
            "最終日の2/7(日)大阪がいちばんの激戦になりそう",
            "申し込みは2枚まで・カード払いがおすすめ。落選しても後の先行や一般発売がある",
        ]),
        p("当落発表は11月26日(木)の20時です。",
          "KO1KEYZにとって初めてのドームのステージなので、迷っている人もまずは申し込んでおきましょう！"),
        ui.quotebox("あわせて読みたい", [a(u, t) for u, t in REL["ja"]]),
    ]
    jp_sum = ("LAPOSTA 2027のFC会員先行がスタート。前回2025年は最速先行が約8割、2回目のFC先行は約4割の当選でした。"
              "席数と申込条件を比べると、今回の会員先行の当選確率は3〜4割前後になりそうです。")

    # ---------------- KR ----------------
    kr_title = "KO1KEYZ LAPOSTA 2027 당첨 확률은? FC 회원 선행 경쟁률 예상"
    kr = [
        p("11월 4일 정오, KO1KEYZ(코이키즈) 공식 X에서 『LAPOSTA 2027』 FC 회원 선행 시작을 알렸어요.",
          "최속 선행에 신청하지 못했거나 월회비 코스인 분들에게는 이번이 첫 기회예요.",
          "도쿄돔과 교세라돔이라고는 해도 6그룹 합동 라이브라서 \"정말 당첨될까?\" 궁금한 분이 많을 거예요."),
        p(f"결론부터 말하면, {mk('FC 회원 선행 당첨 확률은 30~40% 정도')}로 예상해요.",
          f"지난 LAPOSTA 2025에서는 SNS 당락 설문 기준으로 {mk('최속 선행 약 80%, 두 번째 FC 선행 약 40%')}가 당첨됐어요.",
          "이 글에서는 지난번 당락 수치와 2027년 좌석 수·신청 규칙을 비교해 이번 당첨 확률을 예상해 볼게요."),
        ui.table("LAPOSTA 2027 FC 회원 선행", [
            ("접수 기간", "2026년 11월 4일(수) 12:00~11월 15일(일) 23:59 (일본 시간)"),
            ("당락 발표", "11월 26일(목) 20:00"),
            ("입금 기간", "11월 26일(목) 20:00~11월 30일(월) 23:59"),
            ("신청 대상", "JO1·INI·DXTEEN·KO1KEYZ·ME:I·IS:SUE 중 한 그룹의 FC 회원(코스 무관, 신규 가입 가능)"),
            ("당첨 확률(예상)", "30~40% 정도(지난번 같은 단계 선행은 약 40%)"),
        ]),
        h2("회원 선행은 언제까지?"),
        p("회원 선행은 LAPOSTA 2027 FC 선행의 두 번째 단계예요.",
          "10월 24일~11월 3일의 최속 선행은 각 FC '월회비 일괄 결제 코스' 회원만 대상이었지만,",
          f"이번에는 {mk('코스와 상관없이 FC 회원이면 누구나 신청할 수 있어요')}."),
        embed("ko"),
        p("규칙은 최속 선행과 같아요. 1공연당 4장(본인+동행 3명)까지, 한 FC에서 공연마다 1회씩 4공연 모두 신청할 수 있어요.",
          "일정과 티켓 가격은 " + a(L(15187), "KO1KEYZ 첫 LAPOSTA 2027 기사") + "에 정리해 뒀어요."),

        h2("지난 LAPOSTA 2025 당첨률은?"),
        ui.table("LAPOSTA 2025 당첨률(SNS 당락 설문 기준)", [
            ("FC 최속 선행", "약 80%가 어느 한 공연에 당첨(응답 약 3,600건). 2공연 이상 당첨은 거의 없음"),
            ("FC 선행(2차)", "약 40%가 당첨(응답 약 390건)"),
            ("둘 다 낙첨", "약 30%"),
        ]),
        p(f"최속 선행은 약 80%로 높았지만, {mk('두 번째 FC 선행은 약 40%까지 떨어졌어요')}.",
          "당첨된 사람이 설문에 더 잘 답하는 경향이 있어서 실제 당첨률은 조금 더 낮았을 가능성이 있어요.",
          "좌석 설문을 보면 최속 선행 좌석이 아레나부터 2층 스탠드 앞쪽까지 전체의 약 80%를 차지했고, 2차 FC 선행은 2층 스탠드 1~16열에 몰려 있었어요."),

        h2("2027년은 더 쉬울까, 어려울까?"),
        ui.table("LAPOSTA 2025와 2027 비교", [
            ("공연", "2025년: 도쿄돔 3공연 → 2027년: 도쿄돔 2+교세라돔 오사카 2"),
            ("좌석 수(추정)", "2025년: 약 18만 명 동원 → 2027년: 약 22만 석(예상)"),
            ("출연", "2025년: 5그룹+게스트 → 2027년: KO1KEYZ를 더한 6그룹"),
            ("요일", "2025년: 금·토·일 → 2027년: 모두 주말"),
            ("1인 신청 가능 공연 수", "2025년: 3공연 → 2027년: 4공연"),
        ]),
        p(f"좌석은 {mk('약 20% 늘어날 것')}으로 보여요. 지난번처럼 게스트 그룹 FC에 배정되던 좌석이 6그룹에 돌아간다면 이것도 플러스예요.",
          "반면 처음 LAPOSTA에 나서는 KO1KEYZ 팬이 새로 더해지고, 지난번에 비교적 쉬웠던 평일 공연이 없으며, 1인당 신청 가능한 공연도 4공연으로 늘었어요."),

        h2("FC 회원 선행 당첨 확률은?"),
        p("좌석이 늘어나는 만큼 신청도 늘어서 거의 상쇄되는 구조예요.",
          f"그래서 이번 회원 선행도 지난번 2차 FC 선행처럼 {mk('어느 한 공연에 당첨될 확률은 30~40% 정도')}로 예상해요.",
          "회원 선행 좌석은 2층 스탠드 등 위쪽이 중심이 될 가능성이 높아요. 11월 13일(금) 최속 선행 당락이 나오면 경향이 조금 더 보일 거예요."),

        h2("인기 공연과 노려볼 만한 공연"),
        p("지난번에는 마지막 날인 일요일 공연의 신청이 가장 많고 당첨률이 가장 낮았어요.",
          "이번에는 투어 마지막 날이자 16시 개연으로 당일치기도 쉬운 2월 7일(일) 오사카 공연이 가장 치열할 것 같아요.",
          "토요일 공연(1월 23일·2월 6일)은 비교적 노려볼 만해요. 신청 공연 수와 당첨률 사이에는 뚜렷한 관계가 없었으니 갈 수 있다면 4공연 모두 신청하는 게 좋아요."),

        h2("어느 FC로 신청하면 유리할까?"),
        p("FC별 좌석 배정은 공개되지 않았고, 지난번에도 그룹별 큰 차이는 보이지 않았어요.",
          "여러 FC에 가입했다면 각각 신청할 수 있지만, 같은 공연에 중복 당첨돼도 입금해야 하고 취소·양도는 불가능하니 주의하세요."),

        h2("당첨 확률을 높이는 팁"),
        p(f"지난 최속 선행 설문에서는 {mk('3장 이상 신청하면 당첨률이 떨어지는 경향')}이 있었고, 편의점 결제가 약간 낮았어요.",
          "2장 이하, 신용카드 결제를 추천해요. 로손 WEB 회원 정보를 FC 등록 정보와 맞추고, 동행자의 Plus member ID도 미리 준비하세요."),
        p("회원 선행에서 낙첨돼도 지난번에는 d카드 GOLD 선행, 로치케 관련 선행, 일반 발매(선착순)와 공식 트레이드까지 이어졌어요. 2027년 후속 판매 소식을 기다려 봐요."),

        h2("정리"),
        ui.summary([
            "FC 회원 선행은 11/4(수) 12:00~11/15(일) 23:59, 코스 무관",
            "지난 2025년은 최속 선행 약 80%, 2차 FC 선행 약 40% 당첨(SNS 설문 기준)",
            "2027년은 좌석이 약 20% 늘지만 KO1KEYZ 팬이 더해지고 모든 공연이 주말",
            "FC 회원 선행 당첨 확률은 30~40% 정도로 예상",
            "2/7(일) 오사카 마지막 공연이 가장 치열할 듯",
            "2장 이하·카드 결제 추천, 낙첨돼도 이후 판매가 있음",
        ]),
        p("당락 발표는 11월 26일(목) 20시예요. KO1KEYZ의 첫 돔 무대, 고민 중이라면 일단 신청해 봐요!"),
        ui.quotebox("함께 읽으면 좋은 글", [a(u, t) for u, t in REL["ko"]]),
    ]
    kr_sum = ("LAPOSTA 2027 FC 회원 선행이 시작됐어요. 지난 2025년은 최속 선행 약 80%, 2차 FC 선행 약 40%가 당첨. "
              "좌석 수와 신청 조건을 비교하면 이번 회원 선행 당첨 확률은 30~40% 정도로 보여요.")

    # ---------------- EN ----------------
    en_title = "KO1KEYZ at LAPOSTA 2027: Your Odds in the FC Member Presale"
    en = [
        p("At noon on November 4, KO1KEYZ's official X account announced the start of the LAPOSTA 2027 fan club member presale.",
          "For fans who missed the earliest presale or are on the monthly plan, this is the first chance to apply.",
          "Even with Tokyo Dome and Kyocera Dome Osaka, it's a six-group joint concert, so many fans are wondering what their odds really are."),
        p(f"Our estimate: {mk('roughly a 30-40% chance of winning at least one show')} in the member presale.",
          f"At LAPOSTA 2025, fan surveys on social media showed {mk('about 80% winning in the earliest FC presale and about 40% in the second FC round')}.",
          "Below, we compare last time's results with this year's seats and rules."),
        ui.table("LAPOSTA 2027 FC member presale", [
            ("Applications", "Wed, Nov 4, 2026, 12:00 to Sun, Nov 15, 23:59 (JST)"),
            ("Results", "Thu, Nov 26, 20:00"),
            ("Payment", "Nov 26, 20:00 to Mon, Nov 30, 23:59"),
            ("Eligible", "Fan club members of JO1, INI, DXTEEN, KO1KEYZ, ME:I or IS:SUE (any plan; new members welcome)"),
            ("Estimated odds", "About 30-40% (the equivalent round last time was about 40%)"),
        ]),
        h2("Who can apply, and until when?"),
        p("This is the second FC presale for LAPOSTA 2027.",
          f"The earliest presale (Oct 24-Nov 3) was limited to members on the bundled annual plan, but {mk('this round is open to members on any plan')}."),
        embed("en"),
        p("The rules are unchanged: up to four tickets per show (you plus three companions), one application per show per fan club, for all four shows.",
          "Dates and prices are in our " + a(L(15188), "KO1KEYZ LAPOSTA 2027 guide") + "."),

        h2("How did LAPOSTA 2025 go?"),
        ui.table("LAPOSTA 2025 win rates (fan surveys on social media)", [
            ("Earliest FC presale", "About 80% won at least one show (about 3,600 responses); almost nobody won two"),
            ("Second FC presale", "About 40% won (about 390 responses)"),
            ("Lost both", "About 30%"),
        ]),
        p(f"Odds {mk('fell from about 80% to about 40%')} between the two FC rounds, and winners tend to answer surveys more readily, so the real rates were probably a bit lower.",
          "Seat surveys showed the earliest presale covering the arena through the front of the second-tier stands, about 80% of all seats, while the second FC round landed mostly in rows 1-16 of the second tier."),

        h2("Easier or harder than last time?"),
        ui.table("LAPOSTA 2025 vs. 2027", [
            ("Shows", "2025: 3 at Tokyo Dome / 2027: 2 at Tokyo Dome + 2 at Kyocera Dome Osaka"),
            ("Seats (est.)", "2025: about 180,000 attended / 2027: about 220,000 (our estimate)"),
            ("Lineup", "2025: 5 groups + guests / 2027: 6 groups including KO1KEYZ"),
            ("Days", "2025: Fri, Sat, Sun / 2027: weekends only"),
            ("Shows per applicant", "2025: up to 3 / 2027: up to 4"),
        ]),
        p(f"Seats should rise {mk('by about 20%')}, and seats that went to guest groups' fan clubs last time may now go to the six LAPONE groups.",
          "On the other hand, KO1KEYZ fans are applying for the first time, there's no easier weekday show, and each fan can now apply for four shows."),

        h2("So what are the odds?"),
        p("The extra seats and the extra applications roughly cancel out.",
          f"We expect the member presale to land close to last time's second round: {mk('about 30-40% to win at least one show')}, with seats likely concentrated in the upper stands.",
          "The earliest presale results on Fri, Nov 13 should give a clearer picture."),

        h2("Which shows are hardest?"),
        p("Last time the final Sunday drew the most applications and the lowest win rate.",
          "This year, the Osaka finale on Sun, Feb 7 (16:00 start, easy to do as a day trip) looks like the toughest; the Saturday shows (Jan 23 and Feb 6) are relatively better bets.",
          "Applying for more shows didn't lower win rates last time, so apply for every show you can attend."),

        h2("Does the fan club you apply through matter?"),
        p("Seat allocations per fan club aren't published, and last time's surveys showed no meaningful difference between groups.",
          "Members of several fan clubs may apply through each, but duplicate wins must still be paid for and can't be canceled or transferred."),

        h2("Tips to improve your chances"),
        p(f"Last time's survey showed {mk('lower win rates for three or more tickets')}, and convenience store payment did slightly worse.",
          "Stick to two tickets or fewer, pay by credit card, make sure your Lawson WEB details match your fan club registration, and get companions' Plus member IDs ready."),
        p("If you lose, last time's sales continued with a d Card GOLD presale, Lawson Ticket presales, a first-come general sale and an official resale service. Watch for announcements."),

        h2("Summary"),
        ui.summary([
            "FC member presale: Nov 4, 12:00 to Nov 15, 23:59 JST, any plan",
            "LAPOSTA 2025: about 80% won the earliest presale, about 40% the second FC round (fan surveys)",
            "2027 has about 20% more seats, but adds KO1KEYZ fans and has only weekend shows",
            "Estimated member presale odds: about 30-40%",
            "The Feb 7 Osaka finale looks hardest",
            "Apply for two tickets or fewer and pay by card; more sales should follow",
        ]),
        p("Results arrive Thu, Nov 26 at 20:00. It's KO1KEYZ's first dome stage, so if you're on the fence, go ahead and apply!"),
        ui.quotebox("Related articles", [a(u, t) for u, t in REL["en"]]),
    ]
    en_sum = ("The LAPOSTA 2027 FC member presale is open. At LAPOSTA 2025, about 80% won the earliest presale and about 40% the second round. "
              "Comparing seats and rules, we put this round's odds at roughly 30-40%.")
    join = lambda bl: "\n\n".join(bl)
    return (jp_title, join(jp), jp_sum), (kr_title, join(kr), kr_sum), (en_title, join(en), en_sum)


def upload(path, ctype):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HA, "Content-Type": ctype, "Content-Disposition": f'attachment; filename="{path.name}"'},
                      data=path.read_bytes())
    r.raise_for_status()
    return r.json()


def post_draft(title, content, slug, lang, cats, media, summary):
    payload = {"title": title, "content": content, "slug": slug, "status": "draft", "lang": lang,
               "categories": cats, "featured_media": media, "author": 2,
               "meta": {"jetpack_publicize_message": summary}}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers={**HA, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    return r.json()


def honorific(html):
    WORK.mkdir(parents=True, exist_ok=True)
    tmp = WORK / "_jp_body.html"
    tmp.write_text(html, encoding="utf-8")
    tool = str(ROOT / "tools" / "honorific.py")
    subprocess.run([sys.executable, tool, "fix", "--group", "ko1keyz", str(tmp)], check=True)
    subprocess.run([sys.executable, tool, "check", "--group", "ko1keyz", str(tmp)], check=True)
    return tmp.read_text(encoding="utf-8")


def make_eyecatch():
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"), "--top", "LAPOSTA 2027の倍率は？",
                    "--main", "KO1KEYZ", "--bottom", "会員先行の当選確率を予想！", "--out", str(EYE), "--seed", "1104"], check=True)


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    built = build()
    for (t, c, _), name in zip(built, ("JP", "KR", "EN")):
        assert "<hr" not in c
        print(name, len(t), t, "chars:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", c)))
    assert len(built[0][0]) <= 35
    assert len(re.sub(r"<[^>]+>|<!--.*?-->", "", built[0][1])) >= 2500
    if dry:
        WORK.mkdir(parents=True, exist_ok=True)
        (WORK / "_jp_preview.html").write_text(built[0][1], encoding="utf-8")
        sys.exit(0)
    (jt, jc, js), (kt, kc, ks), (et, ec, es) = built
    jc = honorific(jc)
    make_eyecatch()
    eye = upload(EYE, "image/png")["id"]
    jp = post_draft(jt, jc, BASE_SLUG, "ja", [66, 62], eye, js)
    print("JP", jp["id"], jp["slug"], jp["link"])
    kr = post_draft(kt, kc, BASE_SLUG + "-kr", "ko", [74, 70], eye, ks)
    print("KR", kr["id"], kr["slug"], kr["link"])
    en = post_draft(et, ec, BASE_SLUG + "-en", "en", [110, 112], eye, es)
    print("EN", en["id"], en["slug"], en["link"])
    print("eyecatch", eye)
    subprocess.run([sys.executable, str(ROOT / "tools" / "check_ko1keyz_title.py"), str(jp["id"]), str(kr["id"]), str(en["id"])])
