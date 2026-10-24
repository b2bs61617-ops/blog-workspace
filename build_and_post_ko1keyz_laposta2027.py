# -*- coding: utf-8 -*-
"""LAPONE合同ライブ『LAPOSTA 2027』開催決定(東京ドーム1/23・24、京セラドーム大阪2/6・7)。KO1KEYZは初出演。
chomoand-1.com に JP/KR/EN の下書きを作る(本文画像は公式X埋め込みのみ+アイキャッチ)。

一次ソース:
- LAPONE ENTERTAINMENT公式X https://x.com/lapone_info/status/2113797634981056920 (2026-10-24 10:00 JST)
- 特設サイト https://cf.lapone.jp/feature/laposta2027 (日程・開場/開演・チケット15,400円・先行2つの条件・注意事項)
- ニュース https://cf.lapone.jp/special_site/laposta2027/detail/91 (6グループ・2023年から4度目・テーマTREASURE THE MOMENT)
- ニュース https://cf.lapone.jp/special_site/laposta2027/detail/92 (新規入会・お友達紹介キャンペーン=グループ別スマホストラップ)
- 過去開催: 2023有明アリーナ/2024 Kアリーナ横浜/2025東京ドーム3日間・5組(東洋経済・デイリー・crank-in)
- KO1KEYZ FC: 月会費550円/月会費まとめて払い6,600円(PR TIMES・Fanplus、2026年6月開設時)
- KOSUKEはLAPOSTA 2024でJO1ファンに(13055)、KEITOはLAPOSTAでJO1「YOUNG」をやりたい(13521)

python build_and_post_ko1keyz_laposta2027.py [--dry]
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

EYE_JP = ROOT / "images" / "ko1keyz_laposta2027_eyecatch.png"
EYE_KR = ROOT / "images" / "ko1keyz_laposta2027_eyecatch_kr.png"
BASE_SLUG = "ko1keyz-laposta-2027"

TW = "https://twitter.com/lapone_info/status/2113797634981056920"
SITE = "https://cf.lapone.jp/feature/laposta2027"
NEWS = "https://cf.lapone.jp/special_site/laposta2027/detail/91"
CAMP = "https://cf.lapone.jp/special_site/laposta2027/detail/92"

L = lambda pid: f"https://chomoand-1.com/?p={pid}"
REL = {
    "ja": [(L(14275), "KO1KEYZ公式アプリでできることは？電子チケット・通知まとめ！"),
           (L(10415), "【KO1KEYZ】ファンミーティングのチケット倍率は？当選確率を徹底分析！"),
           (L(14839), "KO1KEYZソウルファンミのグッズは？事前EC販売の値段と特典！"),
           (L(13055), "【KOSUKE】好きな女性のタイプは？ヨントンで語った恋愛観！")],
    "ko": [(L(14276), "KO1KEYZ 공식 앱으로 할 수 있는 것은? 전자티켓・알림 총정리!"),
           (L(14841), "KO1KEYZ 서울 팬미팅 굿즈는? 사전 EC 판매 가격과 특전!"),
           (L(14870), "KO1KEYZ 파미마 프린트 언제까지? 가격·종류 총정리!")],
    "en": [(L(14277), "KO1KEYZ Official App: Features, E-Tickets & How to Log In"),
           (L(14842), "KO1KEYZ Seoul Fan Meeting Goods: Prices, Pre-Order Dates and Bonus"),
           (L(14871), "KO1KEYZ FamiMa Print: Until When? Price & Photos!")],
}

ui = Ui("#8a8378", "#ddd9d3", "#f7f6f4", "rgba(138,131,120,0.06)")


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def embed(tw, lang):
    return wphtml(f'<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{tw}">{tw}</a></blockquote>\n'
                  '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def build():
    # ---------------- JP ----------------
    jp_title = "KO1KEYZ初のLAPOSTA 2027！FC先行はいつまで？"
    jp = [
        p("LAPONEのグループが集まる合同ライブ『LAPOSTA 2027』の開催が、10月24日に発表されました。",
          f"会場は{mk('東京ドーム(2027年1月23日・24日)と京セラドーム大阪(2月6日・7日)')}の計4日間です。",
          "10月7日にデビューしたばかりのKO1KEYZ(コイキーズ)にとっては、初めてのLAPOSTAになります。",
          f"チケットは{mk('指定席15,400円(税込)')}で、FC最速先行は{mk('11月3日(火)23時59分まで')}。",
          "この記事では、日程と開演時間、2つのFC先行の違い、申し込み前に準備しておきたいことをまとめました。"),
        ui.table("LAPOSTA 2027 基本情報", [
            ("公演名", "LAPOSTA 2027(読み:ラポスタニーゼロニーナナ)"),
            ("東京", "東京ドーム 2027年1月23日(土)・24日(日)"),
            ("大阪", "京セラドーム大阪 2027年2月6日(土)・7日(日)"),
            ("出演", "JO1・INI・DXTEEN・KO1KEYZ・ME:I・IS:SUE(全6グループ)"),
            ("チケット", "指定席 15,400円(税込)※別途プレイガイド手数料"),
            ("FC最速先行", "10月24日(土)12:00〜11月3日(火)23:59"),
            ("FC会員先行", "11月4日(水)12:00〜11月15日(日)23:59"),
        ]),
        ui.titlebox("この記事でわかること", [
            "LAPOSTA 2027はどんなライブ？", "4公演の開場・開演時間", "チケットの値段と枚数",
            "FC最速先行と会員先行の違い", "申し込み前に準備すること", "会場限定の入会キャンペーン"]),

        h2("LAPOSTA 2027とは？KO1KEYZは初出演"),
        ui.minibox("<strong>内容:</strong>LAPONE所属6グループの合同ライブ",
                   "<strong>テーマ:</strong>「TREASURE THE MOMENT」"),
        p("LAPONE ENTERTAINMENTの公式Xは10月24日の午前10時、「LAPONEグループ所属アーティスト集結！」として開催を発表しました。",
          "ハッシュタグには、JO1・INI・DXTEEN・KO1KEYZの4組の名前が並んでいます。"),
        embed(TW, "ja"),
        p(f"特設サイトのニュースによると、出演するのは{mk('全6グループ')}。",
          "LAPONE ENTERTAINMENTのボーイズグループJO1・INI・DXTEEN・KO1KEYZに、LAPONE GIRLSのガールズグループME:I・IS:SUEが加わります。",
          "テーマは「TREASURE THE MOMENT」で、特設サイトには「宝物は、きみといっしょにいる時間だから。」という言葉が添えられています。"),
        p("LAPOSTAが始まったのは2023年で、今回が4度目です。",
          "1回目は有明アリーナ、2回目はKアリーナ横浜、3回目の2025年は東京ドームで3日間開かれました。",
          "2025年の出演は5組で、今回はそこにKO1KEYZが加わり、はじめて東京と大阪の2つのドームを回ります。"),
        p("KO1KEYZのメンバーにとっても、LAPOSTAはなじみのあるステージです。",
          f"KOSUKEはJO1を好きになったきっかけに「LAPOSTA 2024で見たラップステージ」を挙げていて({a(L(13055), 'KOSUKEの好きなタイプの記事')})、",
          f"KEITOはトーク会で、LAPOSTAでやってみたい曲としてJO1の「YOUNG」の名前を出していました({a(L(13521), 'KEITOのヨントン記事')})。",
          "客席から見ていたLAPOSTAに、今度は出る側として立つことになります。"),

        h2("日程・会場・開演時間は？"),
        ui.minibox("<strong>東京:</strong>東京ドーム 1月23日(土)・24日(日)",
                   "<strong>大阪:</strong>京セラドーム大阪 2月6日(土)・7日(日)"),
        ui.table("LAPOSTA 2027 公演スケジュール", [
            ("1月23日(土)", "東京ドーム 開場16:00/開演18:00"),
            ("1月24日(日)", "東京ドーム 開場15:00/開演17:00"),
            ("2月6日(土)", "京セラドーム大阪 開場16:00/開演18:00"),
            ("2月7日(日)", "京セラドーム大阪 開場14:00/開演16:00"),
        ]),
        p("土曜日はどちらも18時開演で、日曜日は東京が17時、大阪が16時と少し早めです。",
          "大阪の最終日は開場が14時なので、遠方から日帰りする人も帰りの時間を組みやすい日程になっています。"),
        p("公演についての問い合わせ先は、東京がDISK GARAGE、大阪がキョードーインフォメーション(0570-200-888/土日祝を除く12:00〜17:00)です。",
          "公式は、公演内容や日程、出演者が急に変わる場合があるとしています。"),

        h2("チケットの値段は？何枚まで申し込める？"),
        ui.minibox("<strong>値段:</strong>指定席 15,400円(税込)",
                   "<strong>枚数:</strong>1公演につき4枚まで(申込者+同行者)"),
        p(f"席は{mk('指定席の1種類だけで、15,400円(税込)')}。",
          "このほかにプレイガイドの手数料がかかります。",
          "3歳以上は有料で、3歳未満は入場できません。"),
        p("申し込みは、1つの先行につき1人1公演1回まで。",
          "1公演で4枚(自分の分+同行者の分)まで申し込めて、4公演それぞれに1回ずつエントリーできます。",
          "複数のグループのFCに入っている人は、入っているFCそれぞれから申し込めるのもポイントです。"),

        h2("FC最速先行はいつまで？申し込める人は？"),
        ui.minibox("<strong>受付:</strong>10月24日(土)12:00〜11月3日(火)23:59",
                   "<strong>対象:</strong>各グループFCの「月会費まとめて払いコース」会員"),
        ui.table("OFFICIAL FANCLUB 最速先行", [
            ("受付期間", "10月24日(土)12:00〜11月3日(火)23:59"),
            ("当落発表", "11月13日(金)20:00"),
            ("入金期間", "11月13日(金)20:00〜11月16日(月)23:59"),
            ("申込者", "JO1・INI・DXTEEN・KO1KEYZ・ME:I・IS:SUEいずれかのFCの月会費まとめて払いコース会員(またはJO1 FCの2019年12月から続く月会費コース会員)"),
            ("同行者", "登録不要。会員でなくても申し込めるが、Plus member IDが必要"),
        ]),
        p(f"最速先行を申し込めるのは、{mk('「月会費まとめて払いコース」の会員だけ')}です。",
          "KO1KEYZのFCの場合、毎月払う月会費コースが550円、まとめて払いコースが6,600円(どちらも税込、2026年6月の開設時点)。",
          "月会費コースの人も、これからまとめて払いコースに入る・切り替える人も、受付期間中なら申し込めます。"),
        p("ただし、同じ月のうちに月会費コースからまとめて払いコースに変えると、最初の月だけは両方のコースの会費がかかると案内されています。",
          "当落発表は11月13日(金)の20時で、入金は16日(月)の23時59分までです。"),

        h2("FC会員先行との違いは？"),
        ui.minibox("<strong>受付:</strong>11月4日(水)12:00〜11月15日(日)23:59",
                   "<strong>対象:</strong>各グループFCの会員(コースは問わない)"),
        ui.table("OFFICIAL FANCLUB 会員先行", [
            ("受付期間", "11月4日(水)12:00〜11月15日(日)23:59"),
            ("当落発表", "11月26日(木)20:00"),
            ("入金期間", "11月26日(木)20:00〜11月30日(月)23:59"),
            ("申込者", "6グループいずれかのFC会員(コース不問)"),
            ("同行者", "登録不要。会員でなくても申し込めるが、Plus member IDが必要"),
        ]),
        p(f"最速先行の受付が終わると、翌日の11月4日からは{mk('コースを問わないFC会員先行')}が始まります。",
          "こちらは月会費コースの人もそのまま申し込めます。",
          "まとめて払いコースの人は、最速先行で外れても会員先行でもう一度チャンスがある形です。"),
        p("どちらの先行も抽選なので、受付開始直後に急いで申し込む必要はありません。",
          "ただ、受付の始まりと締め切り間際はアクセスが集中しやすいので、時間に余裕をもって申し込んでおくと安心です。"),

        h2("申し込む前に準備しておくことは？"),
        ui.minibox("<strong>必要なもの:</strong>ローソンWEB会員(無料)・同行者のPlus member ID",
                   "<strong>チケット:</strong>「チケプラ電子チケット」アプリで発券"),
        p(f"申し込みには{mk('ローソンWEB会員(無料)への登録')}が必要です。",
          "FCに登録している情報とローソンWEB会員の情報が一致していないと、申し込みが無効や落選になる場合があるので、名前や生年月日などをそろえておきましょう。"),
        p("チケットは転売対策のため、「チケプラ電子チケット」アプリで受け取る電子チケットです。",
          "受け取れるのは各公演日のおよそ1週間前で、座席は公演の前日に表示される予定です。",
          "同行者にはチケットを必ず分配する必要があるので、一緒に行く人には先にPlus member IDを取ってもらっておくとスムーズです。"),
        p("チケットには申込者と同行者の名前が表示され、会場では顔写真付きの身分証で本人確認をする場合があります。",
          "申し込み後の名前の変更や、家族・友だちへの譲渡はできません。",
          "また、申し込みから公演日までFCの会員でいる必要があり、途中で退会すると入場できなくなります。"),
        p(f"KO1KEYZのデジタル会員証や電子チケットまわりの使い方は、{a(L(14275), 'KO1KEYZ公式アプリの記事')}でも紹介しています。"),

        h2("会場限定の新規入会・お友達紹介キャンペーンも"),
        ui.minibox("<strong>入会期間:</strong>2026年10月24日(土)〜11月3日(火)",
                   "<strong>特典:</strong>グループ別オリジナルスマホストラップ(公演当日に会場のFANCLUB BOOTHで受け取り)"),
        p(f"LAPOSTA 2027に合わせて、{mk('FCの新規入会・お友達紹介キャンペーン')}も行われます。",
          "期間中に月会費まとめて払いコースへ新規入会した人と、友だちを紹介したまとめて払いコースの会員が対象で、公演当日に会場のFANCLUB BOOTHへ行くと、グループ別のオリジナルスマホストラップがもらえます。",
          "チケットを持っていない人も参加できます。"),
        p("今回は、違うグループのFC同士での紹介も対象です。",
          "たとえばJO1のFC会員が、KO1KEYZのFCに新しく入った友だちを紹介した場合、2人ともKO1KEYZのFCの特典を受け取れます。",
          "月会費コースは対象外で、紹介した人と入会した人が一緒にブースへ行く必要がある点には注意してください。",
          "特典はなくなり次第終了で、引き換えは公演当日だけです。"),

        h2("まとめ"),
        ui.summary([
            "LAPOSTA 2027は東京ドーム(1/23・24)と京セラドーム大阪(2/6・7)の計4日間",
            "出演はJO1・INI・DXTEEN・KO1KEYZ・ME:I・IS:SUEの6グループ、KO1KEYZは初出演",
            "チケットは指定席15,400円(税込)、1公演4枚まで",
            "FC最速先行は11/3(火)23:59まで、まとめて払いコース会員が対象",
            "FC会員先行は11/4(水)12:00〜11/15(日)23:59、コース不問",
            "ローソンWEB会員の登録と、同行者のPlus member IDを先に準備",
            "期間中の新規入会・紹介で会場限定スマホストラップがもらえる",
        ]),
        p("デビューから約3か月半で迎える、KO1KEYZにとって初めてのドームのステージです。",
          "先輩たちと一緒に立つLAPOSTAで12人がどんな姿を見せてくれるのか、続報を待ちながら申し込みの準備を進めておきましょう！"),
        ui.quotebox("あわせて読みたい", [a(u, t) for u, t in REL["ja"]]),
    ]
    jp_sum = ("LAPONE合同ライブ『LAPOSTA 2027』が東京ドーム・京セラドーム大阪で開催決定、KO1KEYZは初出演。"
              "チケット15,400円、FC最速先行は11/3 23:59まで。日程・先行の条件・準備をまとめました。")

    # ---------------- KR ----------------
    kr_title = "KO1KEYZ 첫 LAPOSTA 2027! FC 선행은 언제까지?"
    kr = [
        p("LAPONE 소속 그룹이 한자리에 모이는 합동 라이브 『LAPOSTA 2027』 개최가 10월 24일 발표됐어요.",
          f"공연장은 {mk('도쿄돔(2027년 1월 23일·24일)과 교세라돔 오사카(2월 6일·7일)')}, 총 4일이에요.",
          "10월 7일에 막 데뷔한 KO1KEYZ(코이키즈)에게는 첫 LAPOSTA예요.",
          f"티켓은 {mk('지정석 15,400엔(세금 포함)')}이고, FC 최속 선행은 {mk('11월 3일(화) 23시 59분(일본 시간)까지')}예요.",
          "이 글에서는 일정과 공연 시간, 두 가지 FC 선행의 차이, 신청 전에 준비할 것을 정리했어요."),
        ui.table("LAPOSTA 2027 기본 정보", [
            ("공연명", "LAPOSTA 2027"),
            ("도쿄", "도쿄돔 2027년 1월 23일(토)·24일(일)"),
            ("오사카", "교세라돔 오사카 2027년 2월 6일(토)·7일(일)"),
            ("출연", "JO1·INI·DXTEEN·KO1KEYZ·ME:I·IS:SUE(총 6팀)"),
            ("티켓", "지정석 15,400엔(세금 포함)※별도 수수료"),
            ("FC 최속 선행", "10월 24일(토) 12:00~11월 3일(화) 23:59"),
            ("FC 회원 선행", "11월 4일(수) 12:00~11월 15일(일) 23:59"),
        ]),
        ui.titlebox("이 글에서 알 수 있는 것", [
            "LAPOSTA 2027은 어떤 라이브?", "4공연의 입장·시작 시간", "티켓 가격과 매수",
            "FC 최속 선행과 회원 선행의 차이", "신청 전 준비할 것", "현장 한정 가입 캠페인"]),

        h2("LAPOSTA 2027이란? KO1KEYZ는 첫 출연"),
        ui.minibox("<strong>내용:</strong>LAPONE 소속 6팀의 합동 라이브",
                   "<strong>테마:</strong>'TREASURE THE MOMENT'"),
        p("LAPONE ENTERTAINMENT 공식 X는 10월 24일 오전 10시, 'LAPONE 그룹 소속 아티스트 집결!'이라며 개최를 발표했어요.",
          "해시태그에는 JO1·INI·DXTEEN·KO1KEYZ 4팀의 이름이 들어 있어요."),
        embed(TW, "ko"),
        p(f"특설 사이트 뉴스에 따르면 출연은 {mk('총 6팀')}이에요.",
          "LAPONE ENTERTAINMENT의 보이그룹 JO1·INI·DXTEEN·KO1KEYZ에, LAPONE GIRLS의 걸그룹 ME:I·IS:SUE가 함께해요.",
          "테마는 'TREASURE THE MOMENT'로, 특설 사이트에는 '보물은, 너와 함께 있는 시간이니까.'라는 문장이 적혀 있어요."),
        p("LAPOSTA는 2023년에 시작해 이번이 4번째예요.",
          "1회는 아리아케 아레나, 2회는 K아레나 요코하마, 3회인 2025년에는 도쿄돔에서 3일간 열렸어요.",
          "2025년 출연은 5팀이었고, 이번에는 KO1KEYZ가 더해져 처음으로 도쿄와 오사카 두 돔을 돌아요."),
        p("KO1KEYZ 멤버들에게도 LAPOSTA는 익숙한 무대예요.",
          "KOSUKE는 JO1을 좋아하게 된 계기로 'LAPOSTA 2024에서 본 랩 무대'를 꼽았고, KEITO는 토크회에서 LAPOSTA에서 해 보고 싶은 곡으로 JO1의 'YOUNG'을 말했어요.",
          "객석에서 보던 LAPOSTA에, 이번에는 무대에 서는 쪽으로 서게 되는 거예요."),

        h2("일정·공연장·공연 시간은?"),
        ui.minibox("<strong>도쿄:</strong>도쿄돔 1월 23일(토)·24일(일)",
                   "<strong>오사카:</strong>교세라돔 오사카 2월 6일(토)·7일(일)"),
        ui.table("LAPOSTA 2027 공연 스케줄(일본 시간)", [
            ("1월 23일(토)", "도쿄돔 입장 16:00/시작 18:00"),
            ("1월 24일(일)", "도쿄돔 입장 15:00/시작 17:00"),
            ("2월 6일(토)", "교세라돔 오사카 입장 16:00/시작 18:00"),
            ("2월 7일(일)", "교세라돔 오사카 입장 14:00/시작 16:00"),
        ]),
        p("토요일은 두 곳 모두 18시 시작이고, 일요일은 도쿄가 17시, 오사카가 16시로 조금 이른 편이에요.",
          "오사카 마지막 날은 14시 입장이라, 멀리서 오는 사람도 돌아가는 시간을 잡기 쉬운 일정이에요."),
        p("공연 문의처는 도쿄가 DISK GARAGE, 오사카가 교도 인포메이션이에요.",
          "공식은 공연 내용·일정·출연자가 갑자기 바뀔 수 있다고 안내하고 있어요."),

        h2("티켓 가격은? 몇 장까지 신청할 수 있을까?"),
        ui.minibox("<strong>가격:</strong>지정석 15,400엔(세금 포함)",
                   "<strong>매수:</strong>1공연당 4장까지(신청자+동행자)"),
        p(f"좌석은 {mk('지정석 한 종류로 15,400엔(세금 포함)')}이에요.",
          "여기에 플레이가이드 수수료가 따로 붙어요.",
          "3세 이상은 유료이고, 3세 미만은 입장할 수 없어요."),
        p("신청은 선행마다 1인 1공연 1회까지예요.",
          "1공연에 4장(본인+동행자)까지 신청할 수 있고, 4공연 각각에 1번씩 엔트리할 수 있어요.",
          "여러 그룹의 FC에 가입한 사람은 가입한 FC마다 따로 신청할 수 있다는 점도 포인트예요."),

        h2("FC 최속 선행은 언제까지? 신청할 수 있는 사람은?"),
        ui.minibox("<strong>접수:</strong>10월 24일(토) 12:00~11월 3일(화) 23:59",
                   "<strong>대상:</strong>각 그룹 FC '월회비 일괄 결제 코스' 회원"),
        ui.table("OFFICIAL FANCLUB 최속 선행(일본 시간)", [
            ("접수 기간", "10월 24일(토) 12:00~11월 3일(화) 23:59"),
            ("당락 발표", "11월 13일(금) 20:00"),
            ("입금 기간", "11월 13일(금) 20:00~11월 16일(월) 23:59"),
            ("신청자", "6팀 중 어느 한 FC의 월회비 일괄 결제 코스 회원(또는 2019년 12월부터 이어진 JO1 FC 월회비 코스 회원)"),
            ("동행자", "등록 불필요. 비회원도 가능하지만 Plus member ID 필요"),
        ]),
        p(f"최속 선행은 {mk('\'월회비 일괄 결제 코스\' 회원만')} 신청할 수 있어요.",
          "KO1KEYZ FC의 경우 매달 내는 월회비 코스가 550엔, 일괄 결제 코스가 6,600엔이에요(모두 세금 포함, 2026년 6월 개설 시점).",
          "지금 월회비 코스인 사람도, 접수 기간 중에 일괄 결제 코스로 가입·변경하면 신청할 수 있어요."),
        p("단, 같은 달에 월회비 코스에서 일괄 결제 코스로 바꾸면 첫 달만 두 코스의 회비가 모두 든다고 안내돼 있어요.",
          "당락 발표는 11월 13일(금) 20시, 입금은 16일(월) 23시 59분까지예요."),

        h2("FC 회원 선행과의 차이는?"),
        ui.minibox("<strong>접수:</strong>11월 4일(수) 12:00~11월 15일(일) 23:59",
                   "<strong>대상:</strong>각 그룹 FC 회원(코스 무관)"),
        ui.table("OFFICIAL FANCLUB 회원 선행(일본 시간)", [
            ("접수 기간", "11월 4일(수) 12:00~11월 15일(일) 23:59"),
            ("당락 발표", "11월 26일(목) 20:00"),
            ("입금 기간", "11월 26일(목) 20:00~11월 30일(월) 23:59"),
            ("신청자", "6팀 중 어느 한 FC 회원(코스 무관)"),
            ("동행자", "등록 불필요. 비회원도 가능하지만 Plus member ID 필요"),
        ]),
        p(f"최속 선행이 끝나면 다음 날인 11월 4일부터 {mk('코스와 상관없는 FC 회원 선행')}이 시작돼요.",
          "이쪽은 월회비 코스 회원도 그대로 신청할 수 있어요.",
          "일괄 결제 코스 회원은 최속 선행에서 떨어져도 회원 선행에서 한 번 더 기회가 있는 셈이에요."),
        p("두 선행 모두 추첨이라 접수 시작 직후에 서두를 필요는 없어요.",
          "다만 시작 직후와 마감 직전에는 접속이 몰리기 쉬우니 여유 있게 신청해 두면 안심이에요."),

        h2("신청 전에 준비할 것은?"),
        ui.minibox("<strong>필요한 것:</strong>로손 WEB 회원(무료)·동행자의 Plus member ID",
                   "<strong>티켓:</strong>'티케프라 전자티켓' 앱으로 발권"),
        p(f"신청하려면 {mk('로손 WEB 회원(무료) 가입')}이 필요해요.",
          "FC에 등록한 정보와 로손 WEB 회원 정보가 다르면 신청이 무효나 낙선이 될 수 있으니 이름 등을 똑같이 맞춰 두세요."),
        p("티켓은 전매 방지를 위해 '티케프라 전자티켓' 앱으로 받는 전자티켓이에요.",
          "받을 수 있는 건 각 공연일 약 1주일 전이고, 좌석은 공연 전날 표시될 예정이에요.",
          "동행자에게는 티켓을 꼭 분배해야 하니, 함께 갈 사람에게 미리 Plus member ID를 만들어 달라고 해 두면 편해요."),
        p("해외 회원은 접수 페이지 아래의 'Overseas members' 버튼으로 신청해요.",
          "전자티켓은 해외 스마트폰에서도 쓸 수 있지만 SMS 기능이 꼭 필요하고, 공식 리세일(티케프라 트레이드)은 일본 국내 계좌가 없으면 출품할 수 없어요."),
        p("티켓에는 신청자와 동행자의 이름이 표시되고, 현장에서 사진이 있는 신분증으로 본인 확인을 할 수 있어요.",
          "신청 후 이름 변경이나 가족·친구에게 양도하는 것은 안 돼요.",
          "또 신청부터 공연일까지 FC 회원을 유지해야 하고, 중간에 탈퇴하면 입장할 수 없어요."),

        h2("현장 한정 신규 가입·친구 소개 캠페인도"),
        ui.minibox("<strong>가입 기간:</strong>2026년 10월 24일(토)~11월 3일(화)",
                   "<strong>특전:</strong>그룹별 오리지널 스마트폰 스트랩(공연 당일 현장 FANCLUB BOOTH에서 수령)"),
        p(f"LAPOSTA 2027에 맞춰 {mk('FC 신규 가입·친구 소개 캠페인')}도 열려요.",
          "기간 중 월회비 일괄 결제 코스에 새로 가입한 사람과, 친구를 소개한 일괄 결제 코스 회원이 대상이고, 공연 당일 현장 FANCLUB BOOTH에 가면 그룹별 오리지널 스마트폰 스트랩을 받을 수 있어요.",
          "티켓이 없는 사람도 참가할 수 있어요."),
        p("이번에는 다른 그룹 FC끼리의 소개도 인정돼요.",
          "예를 들어 JO1 FC 회원이 KO1KEYZ FC에 새로 가입한 친구를 소개하면, 두 사람 모두 KO1KEYZ FC 특전을 받아요.",
          "월회비 코스는 대상이 아니고, 소개한 사람과 가입한 사람이 함께 부스에 가야 해요.",
          "특전은 소진되면 종료되고, 교환은 공연 당일에만 가능해요."),

        h2("정리"),
        ui.summary([
            "LAPOSTA 2027은 도쿄돔(1/23·24)과 교세라돔 오사카(2/6·7) 총 4일",
            "출연은 JO1·INI·DXTEEN·KO1KEYZ·ME:I·IS:SUE 6팀, KO1KEYZ는 첫 출연",
            "티켓은 지정석 15,400엔(세금 포함), 1공연 4장까지",
            "FC 최속 선행은 11/3(화) 23:59까지, 일괄 결제 코스 회원 대상",
            "FC 회원 선행은 11/4(수) 12:00~11/15(일) 23:59, 코스 무관",
            "로손 WEB 회원 가입과 동행자 Plus member ID를 미리 준비",
            "기간 중 신규 가입·소개로 현장 한정 스마트폰 스트랩",
        ]),
        p("데뷔 약 3개월 반 만에 맞이하는, KO1KEYZ의 첫 돔 무대예요.",
          "선배들과 함께 서는 LAPOSTA에서 12명이 어떤 모습을 보여 줄지, 후속 소식을 기다리며 신청 준비를 해 두세요!"),
        ui.quotebox("함께 읽으면 좋은 글", [a(u, t) for u, t in REL["ko"]]),
    ]
    kr_sum = ("LAPONE 합동 라이브 『LAPOSTA 2027』 도쿄돔·교세라돔 오사카 개최 결정, KO1KEYZ 첫 출연. "
              "티켓 15,400엔, FC 최속 선행은 11/3 23:59까지. 일정·선행 조건·준비할 것을 정리했어요.")

    # ---------------- EN ----------------
    en_title = "KO1KEYZ's First LAPOSTA 2027: Dates, Tickets & FC Presale"
    en = [
        p("LAPONE's joint concert LAPOSTA 2027 was announced on October 24.",
          f"It runs for four days: {mk('Tokyo Dome on January 23-24, 2027, and Kyocera Dome Osaka on February 6-7')}.",
          "For KO1KEYZ, who debuted on October 7, it will be their first LAPOSTA.",
          f"Tickets are {mk('15,400 yen (reserved seat, tax included)')}, and the fastest fan club presale runs {mk('until November 3 (Tue), 23:59 JST')}.",
          "Here are the dates and show times, the difference between the two fan club presales, and what to prepare before applying."),
        ui.table("LAPOSTA 2027 at a glance", [
            ("Event", "LAPOSTA 2027"),
            ("Tokyo", "Tokyo Dome, Jan 23 (Sat) & 24 (Sun), 2027"),
            ("Osaka", "Kyocera Dome Osaka, Feb 6 (Sat) & 7 (Sun), 2027"),
            ("Lineup", "JO1, INI, DXTEEN, KO1KEYZ, ME:I, IS:SUE (6 groups)"),
            ("Tickets", "Reserved seat 15,400 yen (tax incl.) + service fee"),
            ("Fastest FC presale", "Oct 24 (Sat) 12:00 - Nov 3 (Tue) 23:59 JST"),
            ("FC member presale", "Nov 4 (Wed) 12:00 - Nov 15 (Sun) 23:59 JST"),
        ]),
        ui.titlebox("In this article", [
            "What is LAPOSTA 2027?", "Doors and start times for all 4 shows", "Ticket price and limits",
            "Fastest presale vs. member presale", "What to prepare before applying", "On-site fan club campaign"]),

        h2("What is LAPOSTA 2027? KO1KEYZ's first appearance"),
        ui.minibox("<strong>What:</strong>A joint concert of six LAPONE groups",
                   "<strong>Theme:</strong>\"TREASURE THE MOMENT\""),
        p("LAPONE ENTERTAINMENT's official X account announced the concert at 10 a.m. on October 24, calling it a gathering of all LAPONE artists.",
          "The hashtags list JO1, INI, DXTEEN and KO1KEYZ."),
        embed(TW, "en"),
        p(f"According to the official site, {mk('six groups')} will perform.",
          "LAPONE ENTERTAINMENT's boy groups JO1, INI, DXTEEN and KO1KEYZ are joined by LAPONE GIRLS' girl groups ME:I and IS:SUE.",
          "The theme is \"TREASURE THE MOMENT,\" with the line \"Because the treasure is the time I spend with you.\""),
        p("LAPOSTA started in 2023, and this is the fourth edition.",
          "The first was held at Ariake Arena, the second at K-Arena Yokohama, and the third, in 2025, ran for three days at Tokyo Dome.",
          "Five groups performed in 2025. This time KO1KEYZ joins, and the event plays two domes, Tokyo and Osaka, for the first time."),
        p("LAPOSTA is a familiar stage for the KO1KEYZ members.",
          "KOSUKE has said he became a JO1 fan after seeing their rap stage at LAPOSTA 2024, and KEITO told fans at a talk event that JO1's \"YOUNG\" is a song he'd like to perform at LAPOSTA someday.",
          "This time they'll be on stage instead of in the audience."),

        h2("Dates, venues and show times"),
        ui.minibox("<strong>Tokyo:</strong>Tokyo Dome, Jan 23 (Sat) & 24 (Sun)",
                   "<strong>Osaka:</strong>Kyocera Dome Osaka, Feb 6 (Sat) & 7 (Sun)"),
        ui.table("LAPOSTA 2027 schedule (JST)", [
            ("Jan 23 (Sat)", "Tokyo Dome, doors 16:00 / start 18:00"),
            ("Jan 24 (Sun)", "Tokyo Dome, doors 15:00 / start 17:00"),
            ("Feb 6 (Sat)", "Kyocera Dome Osaka, doors 16:00 / start 18:00"),
            ("Feb 7 (Sun)", "Kyocera Dome Osaka, doors 14:00 / start 16:00"),
        ]),
        p("Both Saturday shows start at 18:00. On Sunday, Tokyo starts at 17:00 and Osaka at 16:00.",
          "The Osaka finale opens its doors at 14:00, which makes it easier for out-of-town fans to plan a trip home."),
        p("Inquiries go to DISK GARAGE for Tokyo and Kyodo Information for Osaka.",
          "The organizers note that the program, dates and performers may change without notice."),

        h2("How much are tickets, and how many can you apply for?"),
        ui.minibox("<strong>Price:</strong>Reserved seat 15,400 yen (tax incl.)",
                   "<strong>Limit:</strong>Up to 4 tickets per show (you + companions)"),
        p(f"There is {mk('one seat type: reserved seating at 15,400 yen (tax included)')}.",
          "A ticketing service fee is added on top.",
          "Children aged 3 and over need a ticket, and children under 3 can't enter."),
        p("You can apply once per show for each presale.",
          "Each application covers up to four tickets (yourself plus companions), and you can enter for all four shows.",
          "If you belong to more than one group's fan club, you can apply separately through each one."),

        h2("When does the fastest fan club presale end? Who can apply?"),
        ui.minibox("<strong>Applications:</strong>Oct 24 (Sat) 12:00 - Nov 3 (Tue) 23:59 JST",
                   "<strong>Eligible:</strong>Members on the \"annual lump-sum\" plan of any group's fan club"),
        ui.table("OFFICIAL FANCLUB fastest presale (JST)", [
            ("Applications", "Oct 24 (Sat) 12:00 - Nov 3 (Tue) 23:59"),
            ("Results", "Nov 13 (Fri) 20:00"),
            ("Payment", "Nov 13 (Fri) 20:00 - Nov 16 (Mon) 23:59"),
            ("Applicant", "Lump-sum plan member of the JO1, INI, DXTEEN, KO1KEYZ, ME:I or IS:SUE fan club (or JO1 monthly members continuously since Dec 2019)"),
            ("Companions", "No registration needed; non-members OK with a Plus member ID"),
        ]),
        p(f"The fastest presale is {mk('only for members on the lump-sum (annual) plan')}.",
          "For the KO1KEYZ fan club, the monthly plan is 550 yen a month and the lump-sum plan is 6,600 yen (tax included, as of the club's launch in June 2026).",
          "Monthly members, and anyone joining now, can still apply by joining or switching to the lump-sum plan during the window."),
        p("Note that if you switch from the monthly plan to the lump-sum plan within the same month, you'll pay both fees for that first month.",
          "Results come out on November 13 (Fri) at 20:00, and payment is due by 23:59 on the 16th (Mon)."),

        h2("How is the fan club member presale different?"),
        ui.minibox("<strong>Applications:</strong>Nov 4 (Wed) 12:00 - Nov 15 (Sun) 23:59 JST",
                   "<strong>Eligible:</strong>Any fan club member (any plan)"),
        ui.table("OFFICIAL FANCLUB member presale (JST)", [
            ("Applications", "Nov 4 (Wed) 12:00 - Nov 15 (Sun) 23:59"),
            ("Results", "Nov 26 (Thu) 20:00"),
            ("Payment", "Nov 26 (Thu) 20:00 - Nov 30 (Mon) 23:59"),
            ("Applicant", "Member of any of the six fan clubs (any plan)"),
            ("Companions", "No registration needed; non-members OK with a Plus member ID"),
        ]),
        p(f"The day after the fastest presale closes, {mk('a member presale open to all plans')} starts on November 4.",
          "Monthly members can apply as they are.",
          "Lump-sum members who miss out in the first round get a second chance here."),
        p("Both presales are lotteries, so there's no need to rush the moment they open.",
          "Traffic tends to spike right after opening and just before closing, so give yourself some time."),

        h2("What to prepare before applying"),
        ui.minibox("<strong>You need:</strong>A free Lawson WEB membership and your companions' Plus member IDs",
                   "<strong>Tickets:</strong>Issued in the \"Tixplus e-ticket\" app"),
        p(f"Applying requires {mk('a Lawson WEB membership (free)')}.",
          "If your fan club details and Lawson WEB details don't match, your application may be voided or treated as a loss, so make sure your name and other information are identical."),
        p("To prevent resale, tickets are electronic and issued in the Tixplus e-ticket app.",
          "They become available about one week before each show, and seat numbers appear the day before.",
          "You must distribute tickets to your companions, so ask them to create a Plus member ID in advance."),
        p("Overseas members apply through the \"Overseas members\" button at the bottom of the application page.",
          "E-tickets work on overseas smartphones, but SMS is required, and the official resale service (Tixplus Trade) can't be used without a Japanese bank account."),
        p("Tickets show the names of the applicant and companions, and photo ID checks may be carried out at the venue.",
          "Names can't be changed after applying, and tickets can't be transferred, even to family or friends.",
          "You also need to stay a fan club member until the show; if you cancel your membership, you won't be able to enter."),

        h2("On-site campaign for new members and referrals"),
        ui.minibox("<strong>Join between:</strong>Oct 24 (Sat) - Nov 3 (Tue), 2026",
                   "<strong>Gift:</strong>A group-specific phone strap, picked up at the venue's FANCLUB BOOTH on show day"),
        p(f"LAPOSTA 2027 also comes with {mk('a fan club new member and referral campaign')}.",
          "New members who join on the lump-sum plan during the period, and lump-sum members who refer a friend, can get an original phone strap for their group at the FANCLUB BOOTH on show day.",
          "You can take part even without a concert ticket."),
        p("This time, referrals across different groups' fan clubs count too.",
          "For example, if a JO1 fan club member refers a friend who newly joins the KO1KEYZ fan club, both receive the KO1KEYZ fan club gift.",
          "Monthly plans aren't eligible, and the referrer and the new member have to visit the booth together.",
          "Gifts are limited and can only be collected on show days."),

        h2("Summary"),
        ui.summary([
            "LAPOSTA 2027: Tokyo Dome (Jan 23-24) and Kyocera Dome Osaka (Feb 6-7)",
            "Six groups: JO1, INI, DXTEEN, KO1KEYZ, ME:I, IS:SUE; KO1KEYZ's first LAPOSTA",
            "Reserved seat 15,400 yen (tax incl.), up to 4 tickets per show",
            "Fastest FC presale until Nov 3 (Tue) 23:59 JST, lump-sum plan members only",
            "FC member presale Nov 4 (Wed) 12:00 - Nov 15 (Sun) 23:59 JST, any plan",
            "Register for Lawson WEB and get companions' Plus member IDs ready",
            "Join or refer during the period for a venue-only phone strap",
        ]),
        p("About three and a half months after their debut, this will be KO1KEYZ's first dome stage.",
          "While we wait to see what the 12 members bring to LAPOSTA alongside their seniors, get your application ready!"),
        ui.quotebox("Related articles", [a(u, t) for u, t in REL["en"]]),
    ]
    en_sum = ("LAPOSTA 2027 hits Tokyo Dome and Kyocera Dome Osaka, with KO1KEYZ appearing for the first time. "
              "Tickets 15,400 yen; fastest FC presale until Nov 3 23:59 JST. Dates, presale rules and prep.")
    join = lambda bl: "\n\n".join(bl)
    return (jp_title, join(jp), jp_sum), (kr_title, join(kr), kr_sum), (en_title, join(en), en_sum)


def upload(path, ctype):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HA, "Content-Type": ctype, "Content-Disposition": f'attachment; filename="{path.name}"'},
                      data=path.read_bytes())
    r.raise_for_status()
    return r.json()["id"]


def post_draft(title, content, slug, lang, cats, media, summary, ja_id=None):
    payload = {"title": title, "content": content, "slug": slug, "status": "draft", "lang": lang,
               "categories": cats, "featured_media": media, "author": 2,
               "meta": {"jetpack_publicize_message": summary}}
    if ja_id:
        payload["translations"] = {"ja": ja_id}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers={**HA, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    return r.json()


def make_eyecatch():
    tool = str(ROOT / "tools" / "eyecatch_koikeyz.py")
    subprocess.run([sys.executable, tool, "--top", "LAPOSTA 2027開催決定！", "--main", "KO1KEYZ",
                    "--bottom", "FC先行はいつまで？", "--out", str(EYE_JP), "--seed", "1024"], check=True)
    subprocess.run([sys.executable, tool, "--top", "LAPOSTA 2027 개최 결정!", "--main", "KO1KEYZ",
                    "--bottom", "FC 선행은 언제까지?", "--out", str(EYE_KR), "--seed", "1024", "--lang", "kr"], check=True)


if __name__ == "__main__":
    built = build()
    for (t, c, _), name in zip(built, ("JP", "KR", "EN")):
        assert "<hr" not in c
        print(name, len(t), t, "chars:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", c)))
    assert len(built[0][0]) <= 35
    if "--dry" in sys.argv:
        sys.exit(0)
    make_eyecatch()
    (jt, jc, js), (kt, kc, ks), (et, ec, es) = built
    jp_eye = upload(EYE_JP, "image/png")
    kr_eye = upload(EYE_KR, "image/png")
    jp = post_draft(jt, jc, BASE_SLUG, "ja", [66, 62], jp_eye, js)
    print("JP", jp["id"], jp["slug"], jp["link"])
    kr = post_draft(kt, kc, BASE_SLUG + "-kr", "ko", [74, 70], kr_eye, ks, jp["id"])
    print("KR", kr["id"], kr["slug"], kr["link"])
    en = post_draft(et, ec, BASE_SLUG + "-en", "en", [110, 112], jp_eye, es, jp["id"])
    print("EN", en["id"], en["slug"], en["link"])
    print("eyecatch", jp_eye, kr_eye)
