# -*- coding: utf-8 -*-
"""KO1KEYZ デジタルシングル『White Love』(2026-12-14リリース)の発表まとめ。
chomoand-1.com に JP/KR/EN の下書きを作る(author=momo)。2026-11-08 オシリ依頼。
一次ソース:
- KO1KEYZ公式X https://x.com/KO1KEYZofficial/status/2119394182733422738 (2026-11-08 20:38 JST)
- 公式サイト https://ko1keyz.com/news/detail/219 (2026.11.08)
  「DIGITAL SINGLE『White Love』2026年12月14日(月)リリース決定！」
  「ロマンチックな雰囲気の中、降り積もる雪のように少しずつ重なっていく恋を描いた、
   青春の純粋でまっすぐな愛を表現したウィンターラブソング」「詳細は追ってお知らせ」
- デビューシングル『KO1KEYZ』(10/7): オリコン週間2026/10/19付1位・初週46.0万枚。
  デビュー作で初週30万枚超えは2024/5/27付Aぇ! group「《A》BEGINNING」以来2年5ヵ月ぶり (THE FIRST TIMES p=898129)
- 恋GAME: 9/28 0:00 先行配信 (docs/research-notes/ko1keyz-members-spec.md)
- SPEED「White Love」1997-10-15発売、オリコン1位、累計約184.5万枚 (Wikipedia)
- X(11/8)の声: 初めての冬、早めのクリスマスプレゼント、デジタルだから音源頑張る、冬のラブソングでWhiteLoveは勝ち組
python build_and_post_ko1keyz_white_love.py [--dry]
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

WORK = ROOT / "images" / "ko1keyz_white_love"
EYE = ROOT / "images" / "ko1keyz_white_love_eyecatch.png"
BASE_SLUG = "ko1keyz-white-love-digital-single"
TW = "https://twitter.com/KO1KEYZofficial/status/2119394182733422738"
NEWS = "https://ko1keyz.com/news/detail/219"
L = lambda pid: f"https://chomoand-1.com/?p={pid}"
REL = {
    "ja": [(L(13208), "KO1KEYZデビュー曲の歌割りは？12人のパートまとめ！"),
           (L(13887), "KO1KEYZ「恋GAME」の歌詞・歌割りは？12人のパート！"),
           (L(15186), "KO1KEYZ初のLAPOSTA 2027！FC先行はいつまで？")],
    "ko": [(L(13220), "KO1KEYZ 타이틀곡 'KO1KEYZ' 파트 분배는? 12명 전원 총정리"),
           (L(13888), "KO1KEYZ '恋GAME' 가사・파트 분배는? 12명 총정리!"),
           (L(15187), "KO1KEYZ 첫 LAPOSTA 2027! FC 선행은 언제까지?")],
    "en": [(L(13221), "Who Sings What in KO1KEYZ's Title Track \"KO1KEYZ\"?"),
           (L(13889), "Who Sings What in KO1KEYZ's \"Koi GAME\"?"),
           (L(15188), "KO1KEYZ's First LAPOSTA 2027: Dates, Tickets & FC Presale")],
}

ui = Ui("#8a8378", "#ddd9d3", "#f7f6f4", "rgba(138,131,120,0.06)")


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def embed(lang):
    return wphtml(f'<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{TW}">{TW}</a></blockquote>\n'
                  '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def build():
    # ---------------- JP ----------------
    jp_title = "【未】KO1KEYZ新曲White Loveはいつ？配信日や曲の内容まとめ！"
    jp = [
        p("11月8日の夜、KO1KEYZ(コイキーズ)の公式Xで、新曲のリリースが発表されました。",
          "タイトルは『White Love』。",
          "10月7日のデビューから約2か月で届く、KO1KEYZにとって初めての冬の曲です。"),
        p(f"結論から言うと、『White Love』は{mk('2026年12月14日(月)リリースのデジタルシングル')}です。",
          f"公式によると、{mk('降り積もる雪のように少しずつ重なっていく恋を描いたウィンターラブソング')}とのこと。",
          "配信の時間やMV、CDの有無はまだ発表されていないので、今わかっていることと、これまでの流れから予想できることを分けてまとめていきます。"),
        ui.table("KO1KEYZ『White Love』の基本情報", [
            ("タイトル", "White Love"),
            ("形態", "DIGITAL SINGLE(配信)"),
            ("リリース日", "2026年12月14日(月)"),
            ("曲のテーマ", "青春の純粋でまっすぐな愛を表現したウィンターラブソング"),
            ("配信時間・配信サービス", "未発表(11月8日時点)"),
            ("MV・ティザー", "未発表(「詳細は追ってお知らせ」)"),
        ]),
        ui.titlebox("この記事でわかること", [
            "White Loveの発売日と発表の内容", "どんな曲になりそう？", "配信は何時から？どこで聴ける？",
            "CDは出る？デビューシングルとの違い", "同じタイトルの名曲との関係", "MV・音楽番組での披露はいつ？",
            "発表を受けたファンの反応"]),

        h2("KO1KEYZ「White Love」の発売日はいつ？"),
        ui.minibox("<strong>リリース日:</strong>2026年12月14日(月)",
                   "<strong>発表:</strong>11月8日(日)夜、公式X・公式サイトで同時に告知"),
        p("発表があったのは11月8日(日)の夜です。",
          "公式Xに「DIGITAL SINGLE 'White Love' 2026.12.14 RELEASE」という告知が投稿され、同じタイミングで公式サイトのニュースにも掲載されました。"),
        embed("ja"),
        p(f"リリース日は{mk('12月14日の月曜日')}。",
          "クリスマスの10日ほど前で、街がイルミネーションで色づき始めるころです。",
          "冬のラブソングを一番聴きたくなる時期にぴったり合わせてきた形ですね。"),
        p("公式サイトの文章は「詳細は追ってお知らせいたします。ぜひ楽しみにお待ちください！」で締められていて、ジャケット写真や配信リンクは11月8日の時点ではまだ出ていません。",
          "リリースまでは約5週間あるので、これから少しずつ情報が解禁されていくとみられます。"),

        h2("White Loveはどんな曲？"),
        ui.minibox("<strong>公式の紹介:</strong>ロマンチックな雰囲気の中、降り積もる雪のように少しずつ重なっていく恋を描いた、青春の純粋でまっすぐな愛のウィンターラブソング"),
        p("曲の内容について、公式サイトでは次のように紹介されています。",
          "「ロマンチックな雰囲気の中、降り積もる雪のように少しずつ重なっていく恋を描いた、青春の純粋でまっすぐな愛を表現したウィンターラブソング」。",
          "公式Xでも「皆さん、楽しみにしていてください」と雪の結晶の絵文字つきで呼びかけていました。"),
        p(f"ポイントは{mk('「少しずつ重なっていく恋」')}という言葉です。",
          "一目ぼれで一気に燃え上がる恋ではなく、雪が一粒ずつ積もっていくように、気持ちがゆっくり大きくなっていく様子を描いた曲になりそうです。",
          "「青春」「純粋」「まっすぐ」という言葉が並んでいるので、大人っぽい切なさよりも、10代〜20代前半のメンバーらしい初々しさが前に出た曲になると予想できます。"),
        p("これまでの曲と比べると、雰囲気の違いがよくわかります。",
          "デビュー曲「KO1KEYZ」は、サビの「キュントゥグン」(キュン+韓国語で胸が高鳴る音の「トゥグン」)が印象的な、明るく弾けるナンバーでした。",
          "カップリングの「恋GAME」は、恋をRPGにたとえたアップテンポな曲です。"),
        ui.table("KO1KEYZのこれまでの曲と『White Love』", [
            ("KO1KEYZ(デビュー曲)", "10月7日発売。「キュントゥグン」が印象的な明るい曲"),
            ("恋GAME", "9月28日に先行配信。恋をRPGにたとえたアップテンポな曲"),
            ("Key of Story", "デビューシングルの初回限定盤B・通常盤に収録"),
            ("White Love", "12月14日配信。KO1KEYZ初のウィンターラブソング"),
        ]),
        p(f"恋をテーマにしている点はこれまでと同じですが、{mk('季節を感じるバラード寄りの曲は、KO1KEYZとしては初めて')}になるかもしれません。",
          "日プ新世界のころから歌唱力に定評のあるメンバーも多いので、12人の声の重なりをじっくり聴ける曲になるのか、注目したいところです。",
          "作詞・作曲のクレジットや、曲調(バラードかミディアムか)はまだ明かされていません。"),

        h2("White Loveの配信時間は？どこで聴ける？"),
        ui.minibox("<strong>配信時間:</strong>未発表(これまでの例だと0時スタートの可能性が高い)",
                   "<strong>配信サービス:</strong>未発表(デビューシングルと同じく主要サブスクで配信されるとみられる)"),
        p("11月8日の時点では、配信が何時から始まるのか、どのサービスで聴けるのかはまだ発表されていません。",
          "ただ、9月28日に先行配信された「恋GAME」は、日本時間の0時ちょうどに配信がスタートしていました。"),
        p(f"同じ流れなら、『White Love』も{mk('12月14日(月)の0時、つまり13日(日)の深夜24時に配信開始')}となる可能性が高そうです。",
          "日曜の夜に日付が変わるのを待って、すぐに聴けるスケジュールですね。"),
        p("配信サービスは、デビューシングルの楽曲と同じく、Apple Music・Spotify・LINE MUSIC・Amazon Musicなどの主要なサブスクで聴けると考えられます。",
          "日韓同時デビューのグループなので、韓国のMelOnなどでの配信があるかどうかも気になるポイントです。",
          "配信リンクや事前保存(Pre-save)の案内が出たら、公式Xで告知されるはずなので、こまめにチェックしておきましょう。"),

        h2("CDは出ない？デビューシングルとの違い"),
        ui.minibox("<strong>今回:</strong>デジタルシングル(配信のみ)。11月8日時点でCDの発表はなし",
                   "<strong>デビューシングル:</strong>CD6形態で発売、オリコン週間1位・初週46.0万枚"),
        p(f"今回は{mk('「DIGITAL SINGLE」と明記されていて、CDの発売は発表されていません')}。",
          "デビューシングル『KO1KEYZ』は初回限定盤A・B、通常盤、FC限定盤、KEYRING Ver.、PHOTO DIARY Ver.の6形態で発売されましたが、今回は配信で届けるリリースになります。"),
        p("そのデビューシングルは、オリコン週間シングルランキング(2026年10月19日付)で1位を獲得しました。",
          f"初週の売上は{mk('46.0万枚')}で、デビュー作の初週30万枚超えは、2024年のAぇ! group「《A》BEGINNING」以来2年5か月ぶりという記録です。",
          "デビュー前に話題になった「売上ノルマは50万枚？」という噂にも、かなり近い数字を出したことになります。"),
        p("CDの枚数で結果を出した次は、配信でどれだけ聴かれるかが新しい挑戦になります。",
          "Xでも、発表直後から「WhiteLoveデジタルだから音源頑張るぞ」と、再生回数で応援しようとするファンの声が上がっていました。",
          "配信チャートやストリーミングの再生数で、デビュー曲とは違う形の記録が生まれるかもしれません。"),

        h2("SPEEDの「White Love」と同じタイトル？"),
        ui.minibox("<strong>結論:</strong>タイトルは同じだが、公式はKO1KEYZの新しいウィンターラブソングとして紹介している"),
        p("『White Love』と聞いて、1997年のSPEEDの大ヒット曲を思い浮かべた人も多いのではないでしょうか。",
          f"SPEEDの「White Love」は1997年10月15日に発売され、オリコン週間1位、{mk('累計で180万枚を超えるミリオンセラー')}になった冬の定番曲です。"),
        p("韓国でも、1990年代後半にTurboが発表した「White Love(스키장에서)」が冬の名曲として知られていて、今も冬になるとよく流れる曲です。",
          "日本と韓国のどちらにも「White Love」という冬の名曲があるのは、日韓で活動するKO1KEYZにとってちょっとおもしろい偶然ですね。"),
        p("ただ、今回の公式の発表では、カバーやリメイクとは一切書かれていません。",
          "「KO1KEYZが、この冬に届ける」「青春の純粋でまっすぐな愛を表現した」と紹介されていることから、"
          f"{mk('同じタイトルの新曲(オリジナル曲)とみるのが自然')}です。",
          "Xでも、別のアーティストの同名曲を聴いていたら発表があってびっくりした、という声が見られました。"),

        h2("MV・ティザーや音楽番組での披露はいつ？"),
        ui.minibox("<strong>MV・ティザー:</strong>未発表。デビュー曲の流れなら、リリース前にティザーが出る可能性が高い",
                   "<strong>披露の場:</strong>12月の音楽番組・年末特番、1月のLAPOSTA 2027などが候補(予想)"),
        p("MVやティザー映像の公開予定も、11月8日の時点ではまだ発表されていません。",
          "デビューのときは、楽曲タイトルの発表→ビジュアル公開→ティザー→リリースという順番で少しずつ情報が出ていました。",
          "今回も、リリースまでの約5週間でジャケット写真やティザーが順番に公開されていくとみられます。"),
        p("初披露の場所として考えられるのは、まず12月の音楽番組です。",
          "12月は年末の大型音楽特番が続く時期で、冬のラブソングは特番の雰囲気にもよく合います。",
          "KO1KEYZは10月以降、毎週のようにテレビの音楽番組に出演しているので、リリースに合わせたテレビ初披露にも期待したいですね。"),
        p(f"さらに年明けには、{mk('KO1KEYZにとって初めてのドームのステージとなるLAPOSTA 2027')}(1月23日・24日 東京ドーム、2月6日・7日 京セラドーム大阪)が控えています。",
          "冬の曲なので、ドームのセットリストに入る可能性も十分ありそうです。",
          "これはあくまで予想なので、正式な発表を待ちましょう。"),

        h2("White Love発表へのファンの反応"),
        p("発表直後のXでは、「KO1KEYZと過ごす初めての冬」を楽しみにする声があふれていました。",
          "デビューから2か月で新曲が届くことに、うれしい悲鳴を上げるファンも多かったようです。"),
        ui.minibox("「KO1KEYZと初めて過ごす冬か…最高。キュンキュンしてきた」",
                   "「早めのクリスマスプレゼントありがとうございます」",
                   "「冬って大好き。KO1KEYZからWhite Loveが来るし」",
                   "「デジタルだから音源頑張るぞ」",
                   "「冬のラブソングでWhite Loveというタイトルは、もう勝ち組」"),
        p("中には「彼氏いらなくなってきた」という声もあり、タイトルだけでファンの心をしっかりつかんでいることがわかります。",
          "まだ1秒も音源が公開されていないのに、ここまで盛り上がっているのは、デビュー曲で12人の魅力が伝わった証拠ですね。"),

        h2("まとめ"),
        ui.summary([
            "KO1KEYZの新曲『White Love』は2026年12月14日(月)リリースのデジタルシングル",
            "降り積もる雪のように少しずつ重なっていく恋を描いた、青春のウィンターラブソング",
            "配信時間は未発表。恋GAMEと同じなら12月14日0時スタートの可能性が高い",
            "CDの発売は11月8日時点で発表なし。デビューシングルはオリコン1位・初週46.0万枚",
            "SPEEDやTurboの名曲と同じタイトルだが、公式はKO1KEYZの新曲として紹介",
            "MV・ティザー・初披露の場は今後発表。年末の音楽番組やLAPOSTA 2027にも期待",
        ]),
        p("ジャケット写真やティザー、配信リンクなどの続報が出たら、この記事にも追記していきます。",
          "KO1KEYZと迎える初めての冬、12月14日を楽しみに待ちましょう！"),
        ui.quotebox("あわせて読みたい", [a(u, t) for u, t in REL["ja"]]),
    ]
    jp_sum = ("KO1KEYZの新曲『White Love』が12月14日(月)にデジタルシングルでリリース決定。"
              "降り積もる雪のように少しずつ重なる恋を描いた、デビュー後初のウィンターラブソングです。配信時間や曲の内容、CDの有無をまとめました。")

    # ---------------- KR ----------------
    kr_title = "【未】KO1KEYZ 신곡 White Love 발매일은? 공개 시간·곡 정보 정리"
    kr = [
        p("11월 8일 밤, KO1KEYZ(코이키즈) 공식 X에서 신곡 발매 소식이 전해졌어요.",
          "제목은 『White Love』. 10월 7일 데뷔 이후 약 두 달 만에 나오는, KO1KEYZ의 첫 겨울 노래예요."),
        p(f"결론부터 말하면, 『White Love』는 {mk('2026년 12월 14일(월) 발매되는 디지털 싱글')}이에요.",
          f"공식 소개에 따르면 {mk('소복이 쌓이는 눈처럼 조금씩 겹쳐 가는 사랑을 그린 윈터 러브송')}이라고 해요.",
          "공개 시간, MV, CD 여부는 아직 발표되지 않았으니 지금 알 수 있는 것과 예상을 나눠 정리해 볼게요."),
        ui.table("KO1KEYZ 『White Love』 기본 정보", [
            ("제목", "White Love"),
            ("형태", "DIGITAL SINGLE(음원)"),
            ("발매일", "2026년 12월 14일(월)"),
            ("곡의 테마", "청춘의 순수하고 곧은 사랑을 표현한 윈터 러브송"),
            ("공개 시간·음원 사이트", "미발표(11월 8일 기준)"),
            ("MV·티저", "미발표(\"자세한 내용은 추후 안내\")"),
        ]),
        h2("KO1KEYZ 'White Love' 발매일은?"),
        p("11월 8일(일) 밤, 공식 X에 \"DIGITAL SINGLE 'White Love' 2026.12.14 RELEASE\"라는 공지가 올라왔고, 같은 시간 공식 사이트 뉴스에도 게재됐어요."),
        embed("ko"),
        p(f"발매일은 {mk('12월 14일 월요일')}. 크리스마스 열흘 전쯤, 거리에 일루미네이션이 켜지기 시작할 때라 겨울 러브송을 듣기 딱 좋은 타이밍이에요.",
          "재킷 사진과 음원 링크는 아직 공개되지 않았고, 발매까지 약 5주가 남아 앞으로 하나씩 공개될 것으로 보여요."),
        h2("White Love는 어떤 곡?"),
        p("공식 사이트는 \"로맨틱한 분위기 속에서 소복이 쌓이는 눈처럼 조금씩 겹쳐 가는 사랑을 그린, 청춘의 순수하고 곧은 사랑을 표현한 윈터 러브송\"이라고 소개했어요.",
          f"포인트는 {mk('\"조금씩 겹쳐 가는 사랑\"')}이라는 표현이에요. 한눈에 반하는 사랑보다, 눈이 한 송이씩 쌓이듯 마음이 천천히 커지는 모습을 그린 곡이 될 것 같아요."),
        ui.table("KO1KEYZ의 지금까지의 곡과 『White Love』", [
            ("KO1KEYZ(데뷔곡)", "10월 7일 발매. '큥두근'이 인상적인 밝은 곡"),
            ("恋GAME", "9월 28일 선공개. 사랑을 RPG에 빗댄 업템포 곡"),
            ("Key of Story", "데뷔 싱글 초회한정반B·통상반 수록"),
            ("White Love", "12월 14일 음원 공개. KO1KEYZ 첫 윈터 러브송"),
        ]),
        p("사랑이 테마라는 점은 같지만, 계절감이 있는 발라드 계열 곡은 KO1KEYZ로서는 처음일 수도 있어요. 작사·작곡 크레딧과 곡 분위기는 아직 공개되지 않았어요."),
        h2("공개 시간은? 어디서 들을 수 있을까?"),
        p("공개 시간과 음원 사이트는 아직 발표되지 않았어요.",
          f"다만 9월 28일 선공개된 '恋GAME'은 일본 시간 0시에 공개됐기 때문에, 『White Love』도 {mk('12월 14일(월) 0시(일본 시간·한국 시간 동일)')}에 공개될 가능성이 높아 보여요.",
          "데뷔 싱글처럼 Apple Music·Spotify 등 주요 스트리밍에서 들을 수 있을 것으로 보이고, 한일 동시 데뷔 그룹인 만큼 멜론 등 한국 음원 사이트 공개 여부도 주목돼요."),
        h2("CD는 안 나올까?"),
        p(f"이번에는 {mk('\"DIGITAL SINGLE\"로 명시돼 있고 CD 발매는 발표되지 않았어요')}.",
          f"데뷔 싱글 『KO1KEYZ』는 6가지 형태로 발매돼 오리콘 주간 싱글 랭킹(2026년 10월 19일자) 1위, {mk('첫 주 46.0만 장')}을 기록했어요.",
          "데뷔작 첫 주 30만 장 돌파는 2024년 Aぇ! group 『《A》BEGINNING』 이후 2년 5개월 만이에요. 이번에는 음원 성적이 새로운 도전이 되겠네요."),
        h2("SPEED의 'White Love'와 같은 제목?"),
        p("일본에서는 1997년 SPEED의 'White Love'(오리콘 1위, 누적 180만 장 이상)가, 한국에서는 1990년대 후반 터보의 'White Love(스키장에서)'가 겨울 명곡으로 유명하죠.",
          f"하지만 공식 발표에는 커버나 리메이크라는 말이 전혀 없고, \"KO1KEYZ가 이번 겨울에 전하는\" 곡으로 소개돼 있어 {mk('같은 제목의 신곡(오리지널 곡)으로 보는 게 자연스러워요')}."),
        h2("MV·티저, 음악 방송 무대는 언제?"),
        p("MV와 티저 공개 일정도 아직이에요. 데뷔 때처럼 재킷 사진→티저→발매 순으로 공개될 것으로 보여요.",
          "첫 무대로는 12월 음악 방송과 연말 특집이 유력하고, 1월 23·24일 도쿄돔, 2월 6·7일 교세라돔 오사카에서 열리는 LAPOSTA 2027에서 부를 가능성도 있어요(예상)."),
        h2("팬들의 반응"),
        ui.minibox("\"KO1KEYZ와 처음 보내는 겨울이라니… 최고\"",
                   "\"조금 이른 크리스마스 선물 고마워요\"",
                   "\"디지털이니까 음원 열심히 돌리자\"",
                   "\"겨울 러브송에 White Love라는 제목이면 이미 승리\""),
        h2("정리"),
        ui.summary([
            "KO1KEYZ 신곡 『White Love』는 2026년 12월 14일(월) 발매 디지털 싱글",
            "눈처럼 조금씩 겹쳐 가는 사랑을 그린 청춘 윈터 러브송",
            "공개 시간은 미발표, 恋GAME처럼 0시 공개 가능성이 높음",
            "CD 발매 발표는 없음. 데뷔 싱글은 오리콘 1위·첫 주 46.0만 장",
            "SPEED·터보의 명곡과 제목은 같지만 KO1KEYZ의 신곡으로 소개됨",
            "MV·티저·첫 무대는 추후 발표, 연말 음악 방송과 LAPOSTA 2027 기대",
        ]),
        p("후속 소식이 나오면 이 글에도 추가할게요. KO1KEYZ와 맞는 첫 겨울, 12월 14일을 기다려요!"),
        ui.quotebox("함께 읽으면 좋은 글", [a(u, t) for u, t in REL["ko"]]),
    ]
    kr_sum = ("KO1KEYZ 신곡 『White Love』가 12월 14일(월) 디지털 싱글로 발매 확정. "
              "눈처럼 조금씩 겹쳐 가는 사랑을 그린 데뷔 후 첫 윈터 러브송이에요. 공개 시간·곡 정보·CD 여부를 정리했어요.")

    # ---------------- EN ----------------
    en_title = "【未】KO1KEYZ \"White Love\": Release Date, Time & What We Know"
    en = [
        p("On the evening of November 8, KO1KEYZ's official X account announced a new release: \"White Love.\"",
          "Arriving about two months after their October 7 debut, it's the group's first winter song."),
        p(f"In short: \"White Love\" is {mk('a digital single out Monday, December 14, 2026')}.",
          f"The official site describes it as {mk('a winter love song about a romance that builds little by little, like falling snow')}.",
          "Release time, music video and any CD release haven't been announced yet, so below we separate what's confirmed from what we expect."),
        ui.table("KO1KEYZ \"White Love\" at a glance", [
            ("Title", "White Love"),
            ("Format", "Digital single"),
            ("Release date", "Monday, December 14, 2026"),
            ("Theme", "A winter love song about pure, honest young love"),
            ("Release time / platforms", "Not announced (as of Nov 8)"),
            ("MV / teasers", "Not announced (\"details to follow\")"),
        ]),
        h2("When does \"White Love\" come out?"),
        p("The announcement went up on X and the official website at the same time on Sunday, November 8."),
        embed("en"),
        p(f"The release lands on {mk('Monday, December 14')}, about ten days before Christmas, right when winter love songs hit hardest.",
          "No cover art or streaming links yet; with about five weeks to go, expect details to roll out gradually."),
        h2("What kind of song is it?"),
        p("The official description: \"a winter love song expressing the pure, straightforward love of youth, depicting a romance that builds up little by little like falling snow, in a romantic atmosphere.\"",
          f"The key phrase is {mk('\"builds up little by little\"')}: less love at first sight, more feelings that grow slowly, flake by flake."),
        ui.table("KO1KEYZ songs so far", [
            ("KO1KEYZ (debut track)", "Released Oct 7; bright and bouncy with the \"kyuntugun\" hook"),
            ("Koi GAME", "Pre-released Sep 28; an up-tempo song comparing love to an RPG"),
            ("Key of Story", "On Limited Edition B and the Regular Edition of the debut single"),
            ("White Love", "Out Dec 14; KO1KEYZ's first winter love song"),
        ]),
        p("Love is still the theme, but a seasonal, ballad-leaning track would be a first for the group. Songwriting credits and the tempo haven't been revealed."),
        h2("What time does it drop, and where can I listen?"),
        p("Neither has been announced.",
          f"\"Koi GAME\" went live at midnight Japan time, so {mk('00:00 JST on December 14')} (10:00 a.m. ET on Dec 13) looks likely.",
          "Expect major streaming services like Apple Music and Spotify, as with the debut single; watch the official X account for links and pre-saves."),
        h2("Will there be a CD?"),
        p(f"It's billed as {mk('a digital single, and no CD has been announced')}.",
          f"The debut single \"KO1KEYZ\" came in six editions and topped Oricon's weekly singles chart (dated Oct 19, 2026) with {mk('460,000 copies in its first week')},",
          "the first debut single to pass 300,000 in week one since Aぇ! group's \"《A》BEGINNING\" in 2024. This time, streams will be the new test."),
        h2("Is it related to SPEED's \"White Love\"?"),
        p("Many fans immediately thought of SPEED's 1997 hit \"White Love\" (an Oricon No. 1 that sold more than 1.8 million copies), and Korean fans may think of Turbo's late-'90s winter classic \"White Love (At the Ski Resort).\"",
          f"However, the announcement never mentions a cover or remake and presents it as KO1KEYZ's own song, so {mk('it is most likely an original track that shares the title')}."),
        h2("When will we see the MV and first performance?"),
        p("Not announced yet. The debut followed a cover art, teaser, release pattern, so something similar is likely.",
          "December music shows and year-end specials are the obvious stages, and LAPOSTA 2027 (Tokyo Dome Jan 23-24, Kyocera Dome Osaka Feb 6-7) could also feature it. This is speculation."),
        h2("How did fans react?"),
        ui.minibox("\"Our first winter with KO1KEYZ... the best.\"",
                   "\"Thank you for the early Christmas present.\"",
                   "\"It's digital, so let's stream hard.\"",
                   "\"A winter love song called White Love has already won.\""),
        h2("Summary"),
        ui.summary([
            "\"White Love\" is a digital single out Monday, December 14, 2026",
            "A youthful winter love song about romance building like falling snow",
            "Release time TBA; midnight JST is likely, as with Koi GAME",
            "No CD announced; the debut single hit No. 1 on Oricon with 460,000 first-week copies",
            "Shares a title with classics by SPEED and Turbo, but presented as a new KO1KEYZ song",
            "MV, teasers and first stage TBA; watch year-end music shows and LAPOSTA 2027",
        ]),
        p("We'll update this article as more details are announced. Here's to the first winter with KO1KEYZ!"),
        ui.quotebox("Related articles", [a(u, t) for u, t in REL["en"]]),
    ]
    en_sum = ("KO1KEYZ will release the digital single \"White Love\" on Monday, December 14, their first winter love song since debuting. "
              "Here's the release date, likely drop time, what the song is about and whether there's a CD.")

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
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"), "--top", "新曲White Loveはいつ？",
                    "--main", "KO1KEYZ", "--bottom", "配信日・曲の内容まとめ！", "--out", str(EYE), "--seed", "1108"], check=True)


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    built = build()
    for (t, c, _), name in zip(built, ("JP", "KR", "EN")):
        assert "<hr" not in c
        assert t.startswith("【未】") and "KO1KEYZ" in t
        print(name, len(t.replace("【未】", "")), t, "chars:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", c)))
    assert len(built[0][0].replace("【未】", "")) <= 35
    assert len(re.sub(r"<[^>]+>|<!--.*?-->", "", built[0][1])) >= 2500
    if dry:
        WORK.mkdir(parents=True, exist_ok=True)
        (WORK / "_jp_preview.html").write_text(built[0][1], encoding="utf-8")
        sys.exit(0)
    (jt, jc, js), (kt, kc, ks), (et, ec, es) = built
    jc = honorific(jc)
    make_eyecatch()
    eye = upload(EYE, "image/png")["id"]
    jp = post_draft(jt, jc, BASE_SLUG, "ja", [66], eye, js)
    print("JP", jp["id"], jp["slug"], jp["link"])
    kr = post_draft(kt, kc, BASE_SLUG + "-kr", "ko", [74], eye, ks)
    print("KR", kr["id"], kr["slug"], kr["link"])
    en = post_draft(et, ec, BASE_SLUG + "-en", "en", [110], eye, es)
    print("EN", en["id"], en["slug"], en["link"])
    print("eyecatch", eye)
    subprocess.run([sys.executable, str(ROOT / "tools" / "check_ko1keyz_title.py"), str(jp["id"]), str(kr["id"]), str(en["id"])])
