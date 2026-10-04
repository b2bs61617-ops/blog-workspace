# -*- coding: utf-8 -*-
"""KO1KEYZ デビューシングル『KO1KEYZ』リリース記念「KO1KEYZが選ぶ！君に会う前に聴きたいキュントゥグン♡プレイリスト」
(メンバー選曲プレイリスト、10/7〜10/18に1日1人ずつ公開)のまとめ記事。chomoand-1.com に JP/KR/EN の下書きを作る。

一次ソース:
- 公式X https://x.com/KO1KEYZofficial/status/2106569997422309517 (2026-10-04 11:20 JST)
- 公式サイト https://ko1keyz.com/news/detail/144 (公開スケジュール12人分。配信サービス名の記載なし)
収録曲・先行配信は自社記事(恋GAME歌割り13887)で確認済み: KO1KEYZ / 恋GAME(初回A・通常) / Key of Story(初回B・通常)、恋GAMEは9/28先行配信。
公開後は毎日その日のメンバーの選曲を追記していく前提(タイトルは件数なし・追記で古くならない形)。

python build_and_post_ko1keyz_member_playlist.py [--dry]
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

BASE_SLUG = "ko1keyz-member-playlist"
EYE_JP = ROOT / "images" / "ko1keyz_member_playlist_eyecatch.png"
EYE_KR = ROOT / "images" / "ko1keyz_member_playlist_eyecatch_kr.png"

TW = "https://twitter.com/KO1KEYZofficial/status/2106569997422309517"
NEWS = "https://ko1keyz.com/news/detail/144"

L = lambda pid: f"https://chomoand-1.com/?p={pid}"
REL = {
    "ja": [(L(13208), "デビュー曲「KO1KEYZ」の歌割り"),
           (L(13887), "カップリング曲「恋GAME」の歌詞・歌割り"),
           (L(13734), "キュントゥグンPOP-UP(新宿)の日程と特典"),
           (L(14165), "KO1KEYZのテレビ出演予定(10/4〜10/10)"),
           (L(10860), "KO1KEYZの今後のスケジュール")],
    "ko": [(L(13220), "타이틀곡 'KO1KEYZ' 파트 분배"),
           (L(13888), "'恋GAME' 가사・파트 분배"),
           (L(13735), "신주쿠 팝업 일정과 특전"),
           (L(14166), "KO1KEYZ TV 출연 일정(10/4~10/10)"),
           (L(10863), "KO1KEYZ 향후 스케줄")],
    "en": [(L(13221), "Who sings what in the title track \"KO1KEYZ\""),
           (L(13889), "\"Koi GAME\" lyrics and line distribution"),
           (L(13736), "The KO1KEYZ pop-up in Shinjuku"),
           (L(14167), "KO1KEYZ TV appearances (10/4-10/10)"),
           (L(12624), "KO1KEYZ's upcoming schedule")],
}

ui = Ui("#8a8378", "#ddd9d3", "#f7f6f4", "rgba(138,131,120,0.06)")

# (日付, 曜日JP, 曜日KR, 曜日EN, メンバー)
SCHEDULE = [
    ("10/7", "水", "수", "Wed", "YOSHIKI"), ("10/8", "木", "목", "Thu", "DAIKI"),
    ("10/9", "金", "금", "Fri", "SIYOUNG"), ("10/10", "土", "토", "Sat", "SHINHAENG"),
    ("10/11", "日", "일", "Sun", "YURA"), ("10/12", "月", "월", "Mon", "RYUJI"),
    ("10/13", "火", "화", "Tue", "KEITO"), ("10/14", "水", "수", "Wed", "ISSA"),
    ("10/15", "木", "목", "Thu", "RYOGA"), ("10/16", "金", "금", "Fri", "TOWA"),
    ("10/17", "土", "토", "Sat", "KOSUKE"), ("10/18", "日", "일", "Sun", "YUKI"),
]


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def embed(lang):
    return ("<!-- wp:html -->\n"
            f'<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{TW}">{TW}</a></blockquote>\n'
            '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n'
            "<!-- /wp:html -->")


def table(rows):
    td = "border:1px solid #ddd9d3;padding:8px 10px;vertical-align:top;"
    trs = []
    for i, row in enumerate(rows):
        bg = "background:#8a8378;color:#fff;font-weight:bold;" if i == 0 else ("" if i % 2 else "background:#f7f6f4;")
        trs.append("<tr>" + "".join(f'<td style="{td}{bg}">{c}</td>' for c in row) + "</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            + "".join(trs) + '</tbody></table></figure>\n<!-- /wp:table -->')


def build():
    # ---------------- JP ----------------
    jp_title = "KO1KEYZ選曲プレイリストはいつ？12人が選んだ曲まとめ！"
    sched_jp = table([("公開日", "メンバー", "選んだ曲")] +
                     [(f"{d}({w})", m, "公開後に追記") for d, w, _, _, m in SCHEDULE])
    jp = [
        p("デビュー日を目前にしたKO1KEYZ(コイキーズ)から、ファンにはたまらない企画が発表されました。",
          f"デビューシングル『KO1KEYZ』のリリースを記念して、{mk('メンバー12人がそれぞれ選曲したプレイリストを1日1人ずつ公開')}するというものです。",
          f"公開は{mk('2026年10月7日(水)のYOSHIKIからスタートし、10月18日(日)のYUKIまで12日間')}続きます。",
          "この記事では、12人の公開スケジュールと、どこで聴けるのか、企画名の「キュントゥグン」の意味、デビューシングルの収録曲までまとめました。",
          "各メンバーの選曲は、公開され次第この記事に追記していきます。"),
        embed("ja"),
        ui.table("メンバー選曲プレイリスト 基本情報", [
            ("企画名", "KO1KEYZが選ぶ！君に会う前に聴きたいキュントゥグン♡プレイリスト"),
            ("きっかけ", "デビューシングル『KO1KEYZ』のリリース記念"),
            ("公開期間", "2026年10月7日(水)〜10月18日(日)"),
            ("公開ペース", "1日1人ずつ、12人分を順番に公開"),
            ("配信サービス", "告知時点では発表なし"),
            ("発表元", a(NEWS, "KO1KEYZ公式サイトのお知らせ") + "(2026年10月4日)"),
        ]),
        ui.titlebox("この記事でわかること", [
            "メンバー選曲プレイリストとはどんな企画？", "12人の公開スケジュール", "どこで聴ける？配信サービス",
            "「キュントゥグン」の意味", "選曲の予想の手がかり", "デビューシングル『KO1KEYZ』の収録曲"]),

        h2("KO1KEYZのメンバー選曲プレイリストとは？"),
        ui.minibox("<strong>企画名:</strong>KO1KEYZが選ぶ！君に会う前に聴きたいキュントゥグン♡プレイリスト",
                   "<strong>内容:</strong>メンバーそれぞれが選んだ曲のプレイリストを順番に公開"),
        p("この企画は、2026年10月4日に公式Xと公式サイトで同時に発表されました。",
          "10月7日(水)に配信がはじまるデビューシングル『KO1KEYZ』を記念したもので、12人が1人ずつ自分の好きな曲を選んでプレイリストにしています。"),
        p("タイトルにある「君に会う前に聴きたい」という言葉からは、ライブやイベントへ向かう道中、推しに会う前に気分を上げてほしいという思いが伝わってきます。",
          "公式サイトのお知らせも「一緒にキュントゥグン♡してくださいね！」という呼びかけで締めくくられていました。"),
        p("メンバーがふだんどんな音楽を聴いているのかは、なかなか知る機会がありません。",
          "それぞれの選曲から、12人の意外な音楽の好みが見えてくるかもしれませんね。"),

        h2("12人の公開スケジュールはいつ？"),
        ui.minibox("<strong>トップバッター:</strong>10月7日(水) YOSHIKI",
                   "<strong>ラスト:</strong>10月18日(日) YUKI"),
        p("公式サイトで発表された公開順は、下の表のとおりです。",
          "デビュー日の10月7日から毎日1人ずつ、12日間かけて全員のプレイリストがそろいます。"),
        sched_jp,
        p(f"気になるのは、{mk('2日目の10月8日(木)がちょうどDAIKIの誕生日')}だという点です。",
          "2004年10月8日生まれのDAIKIは、この日に22歳を迎えます。",
          "誕生日当日に本人の選んだ曲が届くので、お祝いしながら聴くのにぴったりのタイミングでしょう。"),
        p("公開順は、メンバーカラーの順や日プ新世界の最終順位の順とも違っていて、決め方は特に説明されていません。",
          "誰の番がいつなのか、推しの日をカレンダーに入れておくと聴き逃さずに済みます。"),

        h2("プレイリストはどこで聴ける？"),
        ui.minibox("<strong>配信サービス:</strong>告知時点(10月4日)では発表なし",
                   "<strong>確認先:</strong>公式X・公式サイトのお知らせ"),
        p(f"10月4日の告知では、{mk('どの音楽配信サービスでプレイリストを公開するのかはまだ書かれていません')}。",
          "公式サイトのお知らせも、公開スケジュールと企画の趣旨だけが載っている状態です。"),
        p("参考になるのが、9月28日0時にはじまったカップリング曲「恋GAME」の先行配信です。",
          "このときはSpotifyやApple Musicなど、主な音楽配信サービスでいっせいに聴けるようになりました。",
          "プレイリストも同じように主なサービスで公開されるのか、特定のサービス限定になるのかは、10月7日の公開時に分かりそうです。"),
        p("公開されたらこの記事でも聴ける場所を追記するので、当日はここをチェックしてみてください。"),

        h2("企画名の「キュントゥグン」の意味は？"),
        ui.minibox("<strong>キュントゥグン:</strong>デビュー曲「KO1KEYZ」のサビに出てくる歌詞"),
        p("企画名についている「キュントゥグン」は、デビュー曲「KO1KEYZ」のサビに出てくるフレーズです。",
          "日本語の「キュン」と、韓国語で胸がドキドキする様子を表す「두근(トゥグン)」を組み合わせたような言葉で、恋に落ちる瞬間の胸の高鳴りを表しています。"),
        p("デビュー曲は、初恋の胸の高鳴りから、その気持ちを恋だと自覚するまでを描いた曲です。",
          f"12人それぞれのパートについては{a(L(13208), 'デビュー曲「KO1KEYZ」の歌割りをまとめた記事')}で詳しく紹介しています。"),
        p("10月2日から新宿で開かれているPOP-UPも「キュントゥグンPOP-UP」という名前で、デビュー期の合言葉のようになっています。",
          f"会場や特典は{a(L(13734), 'キュントゥグンPOP-UPの記事')}にまとめました。"),

        h2("どんな曲を選ぶ？予想の手がかり"),
        ui.minibox("<strong>手がかり:</strong>トーク会やファンミーティングで話していた好きな曲・カラオケの十八番"),
        p("プレイリストの中身はまだ分かりませんが、これまでに話していた好きな曲がヒントになりそうです。",
          "トーク会などで出てきた曲を、メンバーごとに並べてみました。"),
        ui.quotebox("これまでに話していた曲", [
            "DAIKI:カラオケでSixTONES「Imitation Rain」、Hey! Say! JUMP「ウィークエンダー」",
            "RYUJI:カラオケの十八番は中西保志「最後の雨」、歌ってほしい曲はAAA「風に薫る夏の記憶」",
            "YOSHIKI:カバーしてみたい曲としてThe Shes Gone「ラベンダー」",
        ]),
        p("J-POPの名曲から男性アイドルの曲、バンドの曲まで、すでに好みはばらばらです。",
          "今回は「君に会う前に聴きたい」というテーマがあるので、ふだんの好きな曲とは別に、恋愛ソングや気分が上がる曲を選んでくる人もいそうですね。"),
        p("日本人メンバーと韓国人メンバーが一緒に活動しているグループなので、J-POPとK-POPがどう混ざるのかも楽しみなところ。",
          "SIYOUNGとSHINHAENGのプレイリストには、韓国の曲が入っているかもしれません。",
          "なお、トーク会は映像が公開されているものではないため、曲名は実際と少し違っている場合があります。"),

        h2("デビューシングル『KO1KEYZ』の収録曲は？"),
        ui.minibox("<strong>発売・配信:</strong>2026年10月7日(水)",
                   "<strong>収録曲:</strong>KO1KEYZ/恋GAME/Key of Story"),
        p(f"プレイリストのきっかけになったデビューシングル『KO1KEYZ』は、{mk('2026年10月7日(水)に発売・配信開始')}です。",
          "表題曲「KO1KEYZ」に加えて、カップリング曲として「恋GAME」と「Key of Story」が収録されています。"),
        p("CDは形態によって入っている曲が違い、「恋GAME」は初回限定盤Aと通常盤、「Key of Story」は初回限定盤Bと通常盤に収録。",
          "3曲すべてをCDで聴きたいなら、通常盤を選ぶのが確実です。"),
        p(f"「恋GAME」は9月28日から先行配信されていて、歌詞と12人のパートは{a(L(13887), '「恋GAME」の歌詞・歌割りの記事')}で紹介しています。",
          "プレイリストを聴く前に、まずはデビューシングルの3曲を聴き込んでおくのもおすすめです。"),

        h2("デビュー週のほかの予定もチェック"),
        ui.minibox("<strong>POP-UP:</strong>新宿で10月8日(木)まで",
                   "<strong>テレビ:</strong>デビュー週は音楽番組などへの出演が続く"),
        p("プレイリストの公開がはじまる10月7日の前後は、KO1KEYZにとって予定が詰まった時期です。",
          "新宿のPOP-UPは10月8日まで開かれていて、テレビ出演も続いています。"),
        p(f"放送予定は{a(L(14165), '10月4日〜10日のテレビ出演をまとめた記事')}に、その先の予定は{a(L(10860), '今後のスケジュールの記事')}にまとめています。",
          "毎日のプレイリストとあわせて、デビュー週を思いきり楽しんでください。"),

        h2("まとめ"),
        ui.summary([
            "デビューシングル『KO1KEYZ』のリリースを記念したメンバー選曲プレイリスト",
            "企画名は「KO1KEYZが選ぶ！君に会う前に聴きたいキュントゥグン♡プレイリスト」",
            "10月7日(水)のYOSHIKIから10月18日(日)のYUKIまで、1日1人ずつ公開",
            "10月8日(木)のDAIKIの日は、本人の22歳の誕生日",
            "配信サービスは10月4日の告知時点では未発表",
            "「キュントゥグン」はデビュー曲「KO1KEYZ」のサビの歌詞",
        ]),
        p("12日間、毎日だれかのプレイリストが届くのは、デビューを待つファンにとってうれしいプレゼントです。",
          "推しが選んだ曲を聴きながら、KO1KEYZに会いに行く日を待ってみてはいかがでしょうか！"),
        ui.quotebox("関連記事", [a(u, t) for u, t in REL["ja"]]),
    ]
    jp_sum = ("KO1KEYZのデビューシングル『KO1KEYZ』リリース記念で、12人がそれぞれ選曲した「キュントゥグン♡プレイリスト」を"
              "10/7のYOSHIKIから10/18のYUKIまで1日1人ずつ公開。10/8のDAIKIの日は本人の誕生日。全員の公開日と、どこで聴けるかをまとめました。")

    # ---------------- KR ----------------
    kr_title = "KO1KEYZ 멤버 선곡 플레이리스트는 언제? 12명이 고른 곡 총정리!"
    sched_kr = table([("공개일", "멤버", "선곡")] +
                     [(f"{d}({w})", m, "공개 후 추가 예정") for d, _, w, _, m in SCHEDULE])
    kr = [
        p("데뷔를 앞둔 KO1KEYZ가 팬들을 설레게 할 기획을 발표했습니다.",
          f"데뷔 싱글 『KO1KEYZ』 발매를 기념해 {mk('멤버 12명이 직접 고른 곡으로 만든 플레이리스트를 하루에 한 명씩 공개')}한다고 해요.",
          f"공개는 {mk('2026년 10월 7일(수) YOSHIKI부터 10월 18일(일) YUKI까지 12일 동안')} 이어집니다.",
          "이 글에서는 12명의 공개 일정, 어디서 들을 수 있는지, 기획명에 들어간 '큥두근'의 의미, 데뷔 싱글 수록곡까지 정리했어요.",
          "각 멤버의 선곡은 공개되는 대로 이 글에 추가할 예정입니다."),
        embed("ko"),
        ui.table("멤버 선곡 플레이리스트 기본 정보", [
            ("기획명", "KO1KEYZ가 고른! 너를 만나기 전에 듣고 싶은 큥두근♡ 플레이리스트"),
            ("계기", "데뷔 싱글 『KO1KEYZ』 발매 기념"),
            ("공개 기간", "2026년 10월 7일(수)~10월 18일(일)"),
            ("공개 방식", "하루에 한 명씩, 12명 순서대로"),
            ("음원 서비스", "발표 시점에는 미공개"),
            ("출처", a(NEWS, "KO1KEYZ 공식 사이트 공지") + "(2026년 10월 4일)"),
        ]),
        ui.titlebox("이 글에서 알 수 있는 것", [
            "멤버 선곡 플레이리스트는 어떤 기획?", "12명의 공개 일정", "어디서 들을 수 있을까?",
            "'큥두근'의 의미", "선곡 예상 힌트", "데뷔 싱글 『KO1KEYZ』 수록곡"]),
        h2("KO1KEYZ 멤버 선곡 플레이리스트란?"),
        ui.minibox("<strong>내용:</strong>멤버가 각자 고른 곡의 플레이리스트를 순서대로 공개"),
        p("이 기획은 2026년 10월 4일 공식 X와 공식 사이트를 통해 동시에 발표됐어요.",
          "10월 7일(수) 발매되는 데뷔 싱글 『KO1KEYZ』를 기념해, 12명이 한 명씩 좋아하는 곡을 골라 플레이리스트로 만들었습니다."),
        p("'너를 만나기 전에 듣고 싶은'이라는 제목에서는, 공연이나 이벤트에 가는 길에 기분을 끌어올려 줬으면 하는 마음이 느껴지네요.",
          "공식 사이트 공지도 '함께 큥두근♡ 해 주세요!'라는 말로 마무리됐습니다."),
        h2("12명의 공개 일정은 언제?"),
        ui.minibox("<strong>첫 번째:</strong>10월 7일(수) YOSHIKI", "<strong>마지막:</strong>10월 18일(일) YUKI"),
        p("공식 사이트에 발표된 공개 순서는 아래 표와 같아요."),
        sched_kr,
        p(f"눈에 띄는 건 {mk('두 번째 날인 10월 8일(목)이 DAIKI의 생일')}이라는 점입니다.",
          "2004년 10월 8일생인 DAIKI는 이날 만 22세가 돼요.",
          "생일 당일에 본인이 고른 곡이 공개되니, 축하하면서 듣기 딱 좋은 타이밍이겠죠."),
        p("공개 순서가 어떻게 정해졌는지는 따로 설명되지 않았습니다.",
          "최애의 날짜를 캘린더에 적어 두면 놓치지 않을 거예요."),
        h2("플레이리스트는 어디서 들을 수 있을까?"),
        ui.minibox("<strong>음원 서비스:</strong>10월 4일 발표 시점에는 미공개"),
        p(f"10월 4일 공지에는 {mk('어느 음원 서비스에서 공개되는지 아직 적혀 있지 않아요')}.",
          "9월 28일 0시에 시작된 커플링곡 '恋GAME(코이GAME)' 선공개 때는 Spotify, Apple Music 등 주요 서비스에서 동시에 들을 수 있었습니다.",
          "플레이리스트가 어디서 공개되는지는 10월 7일에 알 수 있을 것 같아요. 공개되면 이 글에도 추가할게요."),
        h2("기획명에 들어간 '큥두근'의 의미는?"),
        ui.minibox("<strong>큥두근:</strong>데뷔곡 'KO1KEYZ' 후렴 가사"),
        p("기획명의 '큥두근(キュントゥグン)'은 데뷔곡 'KO1KEYZ'의 후렴에 나오는 표현이에요.",
          "일본어로 설렘을 뜻하는 '큥(キュン)'과 한국어 '두근'을 합친 듯한 말로, 사랑에 빠지는 순간의 두근거림을 나타냅니다."),
        p(f"12명의 파트는 {a(L(13220), '타이틀곡 KO1KEYZ 파트 분배 글')}에서 자세히 소개하고 있어요.",
          f"10월 2일부터 신주쿠에서 열리고 있는 팝업도 '큥두근 POP-UP'이라는 이름이에요. 자세한 내용은 {a(L(13735), '신주쿠 팝업 글')}을 참고해 주세요."),
        h2("어떤 곡을 고를까? 예상 힌트"),
        ui.minibox("<strong>힌트:</strong>토크회 등에서 이야기한 좋아하는 곡・노래방 애창곡"),
        ui.quotebox("지금까지 이야기한 곡", [
            "DAIKI: 노래방에서 SixTONES 'Imitation Rain', Hey! Say! JUMP '위켄더'",
            "RYUJI: 노래방 애창곡은 나카니시 야스시 '마지막 비(最後の雨)', 불러 줬으면 하는 곡은 AAA '바람에 실린 여름의 기억'",
            "YOSHIKI: 커버해 보고 싶은 곡으로 The Shes Gone '라벤더'",
        ]),
        p("J-POP 명곡부터 아이돌 곡, 밴드 곡까지 취향이 다양하죠.",
          "한국인 멤버 SIYOUNG과 SHINHAENG의 플레이리스트에는 K-POP이 들어갈지도 몰라요.",
          "토크회는 영상이 공개된 것이 아니어서 곡명이 실제와 조금 다를 수 있습니다."),
        h2("데뷔 싱글 『KO1KEYZ』 수록곡은?"),
        ui.minibox("<strong>발매・음원 공개:</strong>2026년 10월 7일(수)", "<strong>수록곡:</strong>KO1KEYZ / 恋GAME / Key of Story"),
        p(f"데뷔 싱글 『KO1KEYZ』는 {mk('2026년 10월 7일(수) 발매・음원 공개')}예요.",
          "타이틀곡 'KO1KEYZ'와 커플링곡 '恋GAME', 'Key of Story'가 수록됩니다.",
          "CD는 형태마다 수록곡이 달라서, 3곡을 모두 CD로 듣고 싶다면 통상반이 확실합니다."),
        p(f"'恋GAME' 가사와 파트는 {a(L(13888), '恋GAME 가사・파트 분배 글')}에서 소개하고 있어요."),
        h2("정리"),
        ui.summary([
            "데뷔 싱글 『KO1KEYZ』 발매 기념 멤버 선곡 플레이리스트",
            "10월 7일(수) YOSHIKI부터 10월 18일(일) YUKI까지 하루에 한 명씩 공개",
            "10월 8일(목) DAIKI의 날은 본인의 22번째 생일",
            "음원 서비스는 10월 4일 시점에는 미공개",
            "'큥두근'은 데뷔곡 'KO1KEYZ'의 후렴 가사",
        ]),
        p("12일 동안 매일 누군가의 플레이리스트가 도착하는 건, 데뷔를 기다리는 팬들에게 반가운 선물이에요.",
          "최애가 고른 곡을 들으며 KO1KEYZ를 만나러 갈 날을 기다려 보는 건 어떨까요!"),
        ui.quotebox("관련 글", [a(u, t) for u, t in REL["ko"]]),
    ]
    kr_sum = ("KO1KEYZ 데뷔 싱글 발매 기념으로 12명이 직접 고른 '큥두근♡ 플레이리스트'를 10/7 YOSHIKI부터 10/18 YUKI까지 "
              "하루에 한 명씩 공개. 10/8 DAIKI의 날은 본인 생일. 전원의 공개일과 어디서 들을 수 있는지 정리했어요.")

    # ---------------- EN ----------------
    en_title = "KO1KEYZ Member Playlists: When Is Each One Out?"
    sched_en = table([("Release date", "Member", "Songs picked")] +
                     [(f"{d} ({w})", m, "To be added") for d, _, _, w, m in SCHEDULE])
    en = [
        p("Just ahead of their debut, KO1KEYZ have announced a treat for fans.",
          f"To celebrate the debut single \"KO1KEYZ\", {mk('each of the 12 members has put together a playlist of songs they picked, released one member per day')}.",
          f"The series runs for {mk('12 days, from YOSHIKI on October 7 (Wed), 2026 to YUKI on October 18 (Sun)')}.",
          "Here we cover the full release schedule, where to listen, what \"kyun-dugeun\" in the title means, and the tracks on the debut single.",
          "We'll add each member's song picks to this article as they come out."),
        embed("en"),
        ui.table("Member playlists at a glance", [
            ("Project title", "\"Chosen by KO1KEYZ! Kyun-dugeun Playlists to Listen to Before Meeting You\""),
            ("Occasion", "Release of the debut single \"KO1KEYZ\""),
            ("Period", "October 7 (Wed) - October 18 (Sun), 2026"),
            ("Pace", "One member per day, 12 in total"),
            ("Streaming service", "Not announced as of October 4"),
            ("Source", a(NEWS, "KO1KEYZ official website") + " (October 4, 2026)"),
        ]),
        ui.titlebox("What you'll learn", [
            "What the member playlist project is", "The release schedule for all 12 members", "Where to listen",
            "What \"kyun-dugeun\" means", "Hints at what they might pick", "The tracks on the debut single \"KO1KEYZ\""]),
        h2("What is the KO1KEYZ member playlist project?"),
        ui.minibox("<strong>What:</strong>playlists picked by each member, released in turn"),
        p("The project was announced on October 4, 2026 on KO1KEYZ's official X account and website.",
          "It marks the release of the debut single \"KO1KEYZ\" on October 7 (Wed), with each of the 12 members choosing songs they love."),
        p("The phrase \"to listen to before meeting you\" suggests songs to hype fans up on the way to a show or event.",
          "The official announcement closes with \"Let's go kyun-dugeun together!\""),
        h2("When is each member's playlist released?"),
        ui.minibox("<strong>First:</strong>YOSHIKI on October 7 (Wed)", "<strong>Last:</strong>YUKI on October 18 (Sun)"),
        p("Here is the order announced on the official website (dates in Japan time)."),
        sched_en,
        p(f"One nice detail: {mk('day two, October 8 (Thu), is DAIKI’s birthday')}.",
          "Born on October 8, 2004, DAIKI turns 22 that day, so his playlist doubles as a birthday celebration.",
          "No explanation was given for the order, so it's worth noting your bias's date."),
        h2("Where can you listen to the playlists?"),
        ui.minibox("<strong>Streaming service:</strong>not announced as of October 4"),
        p(f"The October 4 announcement {mk('does not yet say which streaming service will host the playlists')}.",
          "When the B-side \"Koi GAME\" was pre-released on September 28, it went up on major services such as Spotify and Apple Music at the same time.",
          "We should find out where the playlists live on October 7, and we'll update this article then."),
        h2("What does \"kyun-dugeun\" mean?"),
        ui.minibox("<strong>Kyun-dugeun:</strong>a lyric from the chorus of the debut song \"KO1KEYZ\""),
        p("\"Kyun-dugeun\" (キュントゥグン) comes from the chorus of the debut song \"KO1KEYZ\".",
          "It blends the Japanese \"kyun\" (a heart-squeezing flutter) with the Korean \"dugeun\" (a pounding heartbeat), describing the moment you fall in love."),
        p(f"Each member's part is covered in {a(L(13221), 'our line distribution guide for \"KO1KEYZ\"')}, and the Shinjuku pop-up running since October 2 also carries the name; see {a(L(13736), 'our pop-up guide')}."),
        h2("What might they pick? Some hints"),
        ui.minibox("<strong>Hints:</strong>songs the members have mentioned at fan talk events"),
        ui.quotebox("Songs the members have mentioned", [
            "DAIKI: at karaoke, SixTONES \"Imitation Rain\" and Hey! Say! JUMP \"Weekender\"",
            "RYUJI: his karaoke go-to is Yasushi Nakanishi \"Saigo no Ame\"; a song he'd like sung to him is AAA \"Kaze ni Kaoru Natsu no Kioku\"",
            "YOSHIKI: a song he'd like to cover, The Shes Gone \"Lavender\"",
        ]),
        p("Their tastes already range from J-pop classics to idol songs and band tracks.",
          "SIYOUNG and SHINHAENG, the Korean members, might well include some K-pop.",
          "Talk events aren't publicly recorded, so song titles may differ slightly from what was actually said."),
        h2("What's on the debut single \"KO1KEYZ\"?"),
        ui.minibox("<strong>Release:</strong>October 7 (Wed), 2026", "<strong>Tracks:</strong>KO1KEYZ / Koi GAME / Key of Story"),
        p(f"The debut single \"KO1KEYZ\" is {mk('out on CD and streaming on October 7 (Wed), 2026')}.",
          "Alongside the title track \"KO1KEYZ\", it includes the B-sides \"Koi GAME\" and \"Key of Story\".",
          "Track lists differ by CD edition, so the regular edition is the safe pick if you want all three on CD."),
        p(f"For \"Koi GAME\" lyrics and parts, see {a(L(13889), 'our \"Koi GAME\" guide')}."),
        h2("Summary"),
        ui.summary([
            "Member-picked playlists celebrating the debut single \"KO1KEYZ\"",
            "One per day, from YOSHIKI on October 7 (Wed) to YUKI on October 18 (Sun)",
            "DAIKI's day, October 8 (Thu), is his 22nd birthday",
            "The streaming service had not been announced as of October 4",
            "\"Kyun-dugeun\" is a lyric from the chorus of the debut song",
        ]),
        p("Twelve days of playlists, one from a different member each day, is a lovely gift for fans waiting on the debut.",
          "Why not count down to seeing KO1KEYZ with the songs your bias picked!"),
        ui.quotebox("Related articles", [a(u, t) for u, t in REL["en"]]),
    ]
    en_sum = ("To celebrate their debut single, all 12 KO1KEYZ members picked their own \"kyun-dugeun\" playlists, released one per day "
              "from YOSHIKI on 10/7 to YUKI on 10/18. DAIKI's day, 10/8, is his birthday. Full schedule and where to listen.")
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


def make_eyecatch():
    tool = str(ROOT / "tools" / "eyecatch_koikeyz.py")
    subprocess.run([sys.executable, tool, "--top", "12人が選んだ曲は？", "--main", "KO1KEYZ",
                    "--bottom", "選曲プレイリスト公開！", "--out", str(EYE_JP), "--seed", "1004"], check=True)
    subprocess.run([sys.executable, tool, "--top", "12명이 고른 곡은?", "--main", "KO1KEYZ",
                    "--bottom", "선곡 플레이리스트 공개!", "--out", str(EYE_KR), "--seed", "1004", "--lang", "kr"], check=True)


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    built = build()
    for (t, c, _), name in zip(built, ("JP", "KR", "EN")):
        assert "<hr" not in c
        print(name, len(t), t, "chars:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", c, flags=re.S)))
    assert len(built[0][0]) <= 35
    assert len(re.sub(r"<[^>]+>|<!--.*?-->", "", built[0][1], flags=re.S)) >= 2500
    if dry:
        (ROOT / "tmp_ko1keyz_playlist_preview.html").write_text(built[0][1], encoding="utf-8")
        sys.exit(0)
    make_eyecatch()
    (jt, jc, js), (kt, kc, ks), (et, ec, es) = built
    jp_eye = upload(EYE_JP, "image/png")["id"]
    kr_eye = upload(EYE_KR, "image/png")["id"]
    jp = post_draft(jt, jc, BASE_SLUG, "ja", [66, 62], jp_eye, js)
    print("JP", jp["id"], jp["slug"], jp["link"])
    kr = post_draft(kt, kc, BASE_SLUG + "-kr", "ko", [74, 70], kr_eye, ks)
    print("KR", kr["id"], kr["slug"], kr["link"])
    en = post_draft(et, ec, BASE_SLUG + "-en", "en", [110, 112], jp_eye, es)
    print("EN", en["id"], en["slug"], en["link"])
    print("eyecatch", jp_eye, kr_eye)
