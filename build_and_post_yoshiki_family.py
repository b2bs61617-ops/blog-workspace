# -*- coding: utf-8 -*-
"""KO1KEYZ YOSHIKI(矢田佳暉)の家族構成記事。chomoand-1.com に JP/KR/EN の下書き(author=momo)。
2026-11-10 オシリ依頼(Xiy調査)。
根拠(すべて本人発言・番組公式の範囲。家族の名前・父の勤務先の社名・顔/容姿は書かない方針):
- 姉: 9/21ヨントンレポ(@yy_kirako1 2101924885434146879)「Q.お姉ちゃんとは何歳差？ 4！」
       9/5 大阪オフライン特典会レポ(@hihi_okey_soso 2097566665030676809 画像)ファンの名札を見て「お姉ちゃんと名前一緒！」
- 母: 9/12ヨントン Day1 レポ(@_kirakira_yy 2098684050060030363 画像)ロールモデル=テミンの理由「お母さん！お母さんがずっと大好きで、ソロコンサートも行ってる」「SM大好き」
       ファンブックに母は川尻蓮(JO1)のファンと記載(@ysk_nyan 2090741034259189989 / @memochoukawari 2090776123600998661、8/21)
- 父: 『踊る！さんま御殿!!』11/10(火)20時 日本テレビ 初出演「関西隣県バトル」公式予告
       「関西ではお馴染みの会社に勤めるお父さんとの思い出も！」/11/9追加告知「緊張でなかなか話に入れずも…お父さんの話でついにトークの輪へ！」
- 日プ最終回(6/6)の家族席に母と姉(@kaemonmon1119 2063448503590990006。容姿には触れない)
- デビューライブPR: YOSHIKI「12人で家族のように、10年、20年続く」(build_and_post_ko1keyz_debut_live_1min_pr.py)
python build_and_post_yoshiki_family.py [--dry]
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

WORK = ROOT / "images" / "yoshiki_family"
EYE = ROOT / "images" / "yoshiki_family_eyecatch.png"
BASE_SLUG = "yoshiki-yada-family"
L = lambda pid: f"https://chomoand-1.com/?p={pid}"
REL = {
    "ja": [(L(3741), "矢田佳暉のwiki風経歴は？現役歌王TOP10の実力者"),
           (L(3744), "矢田佳暉の学歴は？奈良県内の小・中・高校出身"),
           (L(15013), "矢田佳暉の日プ順位推移は？海外票トップで最終2位！"),
           (L(11059), "TOWA(濱田永遠)の家族構成は？父親は韓国人と判明！")],
}

ui = Ui("#d9819b", "#f2cfd9", "#fdf5f8", "rgba(217,129,155,0.07)")


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def build():
    # ---------------- JP ----------------
    jp_title = "【未】【KO1KEYZ】矢田佳暉の家族構成は？父・母・4歳上の姉を調査！"
    jp = [
        p("『PRODUCE 101 JAPAN 新世界』で最終2位に輝き、KO1KEYZ(コイキーズ)のメンバーとしてデビューしたYOSHIKI(矢田佳暉)。",
          "11月10日(火)には『踊る！さんま御殿!!』に初出演し、お父さんとの思い出を話すことが予告されています。",
          "ヨントンやトーク会でも、家族の話がたびたび出てきていました。"),
        p(f"結論から言うと、YOSHIKIさんの家族は{mk('父・母・4歳上の姉')}がいることがわかっています。",
          "本人が話した内容と番組の公式情報だけをもとに、お父さん・お母さん・お姉ちゃんについてまとめました。"),
        ui.table("YOSHIKI(矢田佳暉)のプロフィール", [
            ("名前", "矢田 佳暉(やだ よしき)"),
            ("生年月日", "2004年6月18日(22歳)"),
            ("出身地", "奈良県"),
            ("身長", "177cm"),
            ("メンバーカラー", "ピンク"),
            ("経歴", "『PRODUCE 101 JAPAN 新世界』最終2位 → 2026年10月7日にKO1KEYZとしてデビュー"),
        ]),
        ui.titlebox("この記事でわかること", [
            "YOSHIKIは何人家族？", "父親は？さんま御殿で話す「関西でおなじみの会社」",
            "母親は？テミンとJO1川尻蓮のファン", "お姉ちゃんは何歳差？", "実家は音楽一家？トランペットとバイオリン", "実家では猫を2匹飼っている", "日プ最終回の家族席", "家族思いのエピソード"]),

        h2("YOSHIKI(矢田佳暉)の家族構成は？"),
        ui.minibox("<strong>わかっている家族:</strong>父・母・姉(4歳上)・YOSHIKIさん本人",
                   "<strong>兄弟の有無:</strong>兄・弟・妹についての発言は見当たらない"),
        p("YOSHIKIさんがこれまでに話した家族は、お父さん・お母さん・お姉ちゃんの3人です。",
          "兄や弟、妹について話したことはなく、お姉ちゃんとの2人きょうだいの可能性が高そうです。",
          f"そのため、{mk('父・母・姉・YOSHIKIさんの4人家族')}とみられます。",
          "公式プロフィールで家族構成が発表されているわけではないので、ここからは本人が話した内容をひとつずつ見ていきます。"),

        h2("父親は？「関西ではお馴染みの会社」に勤める"),
        ui.minibox("<strong>わかっていること:</strong>関西ではおなじみの会社に勤めている",
                   "<strong>出典:</strong>『踊る！さんま御殿!!』(日本テレビ)11月10日放送回の公式予告"),
        p("お父さんについて初めて具体的な話が出るのが、11月10日(火)よる8時放送の『踊る！さんま御殿!!』です。",
          "この回のテーマは「関西隣県バトル」で、YOSHIKIさんは奈良県出身の代表として初登場します。"),
        p("番組の公式Xでは、放送前に次のような予告が出ていました。"),
        ui.quotebox("『踊る！さんま御殿!!』公式の予告", [
            "奈良vs滋賀のバトルになかなか参戦できないYOSHIKIさん 実はあるワケが…",
            f"{mk('関西ではお馴染みの会社に勤めるお父さんとの思い出も！')}",
            "(11月9日の追加告知)緊張でなかなか話に入れずも…お父さんの話でついにトークの輪へ！初々しい姿に注目です"]),
        p("バラエティ番組での初めてのトークで、緊張して話に入れずにいたところを、お父さんの話題で盛り返したようです。",
          "「関西ではお馴染み」というくらいなので、関西に住んでいる人なら誰でも知っている会社なのかもしれません。"),
        p("予告が出た日には、ファンのあいだでも「お父さんの話、楽しみ」「生い立ちの秘密が明かされる？」と話題になっていました。",
          "高校時代は軽音楽部でギター＆ボーカルを担当していたYOSHIKIさんが、どんな家庭で育ったのかがわかるエピソードになりそうですね。"),
        ui.minibox("<strong>※お父さんの勤め先について</strong>",
                   "お父さんは一般の方のため、この記事では勤務先の会社名は書かないことにしています。放送で話されたお父さんとの思い出は、放送後にこの記事へ追記します。"),

        h2("母親は？テミンとJO1川尻蓮のファン"),
        ui.minibox("<strong>わかっていること:</strong>長年のテミン(SHINee)のファンで、ソロコンサートにも行っている",
                   "<strong>出典:</strong>9月12日のヨントン(オンライントーク会)、公式ファンブック"),
        p("お母さんについては、YOSHIKIさん本人がヨントンで話しています。",
          "9月12日のヨントンで、ファンから「ロールモデルはテミンって言ってたやん？その理由とか経緯が知りたい！」と聞かれたときの答えがこちらです。"),
        ui.quotebox("9月12日ヨントンでのやりとり", [
            "ファン:ロールモデルはテミンって言ってたやん？その理由とか経緯が知りたい！",
            f"YOSHIKI:{mk('お母さん！お母さんがずっと大好きで、ソロコンサートも行ってる')}",
            "ファン:え、SM好き？？",
            "YOSHIKI:SM大好き！"]),
        p("YOSHIKIさんのロールモデルであるSHINeeのテミンさんは、もともとお母さんが長年大好きなアーティストだったんですね。",
          "ソロコンサートにも行っているそうなので、YOSHIKIさんも小さいころからお母さんの影響でK-POPに触れていたのかもしれません。",
          "この日のヨントンでは、SMエンターテインメントのアーティストでほかに好きな人を聞かれて「チャンミンさん！」(東方神起)と答えていました。"),
        p("さらに、KO1KEYZのファンブックには、お母さんが JO1の川尻蓮さんのファンだということも書かれていたそうです。",
          f"川尻蓮さんは同じLAPONEエンタテインメントの先輩で、{mk('お母さんの推しの直属の後輩に息子がなった')}ことになります。",
          "ファンのあいだでも「センスが良すぎる」「推しの後輩になったのすごい」と話題になりました。"),
        p("なお、トーク会は映像が公開されているものではないため、セリフの言い回しは実際と少し違っている場合があります。"),

        h2("お姉ちゃんは何歳差？4歳上の姉がいる"),
        ui.minibox("<strong>わかっていること:</strong>4歳上のお姉ちゃんがいる(2000年度ごろの生まれ)",
                   "<strong>出典:</strong>9月21日のヨントン、9月5日の大阪オフライン特典会"),
        p("YOSHIKIさんには、お姉ちゃんがいます。",
          "9月21日のヨントンで「お姉ちゃんとは何歳差？」と聞かれ、YOSHIKIさんは「4！」と答えていました。"),
        ui.quotebox("9月21日ヨントンでのやりとり", [
            "ファン:お姉ちゃんとは何歳差？",
            f"YOSHIKI:{mk('4！')}"]),
        p(f"YOSHIKIさんは2004年6月生まれなので、お姉ちゃんは{mk('2000年ごろの生まれで、2026年時点で26歳前後')}とみられます。"),
        p("9月5日にインテックス大阪で行われたオフライン特典会(個別トーク会)では、ファンの名札をじーっと見て「お姉ちゃんと名前一緒！！！」と驚く場面もあったそうです。",
          "お姉ちゃんの名前をふだんから意識しているのが伝わる、仲の良さがわかるエピソードですね。"),
        ui.minibox("<strong>※お姉ちゃんの名前について</strong>",
                   "お姉ちゃんは一般の方のため、この記事では名前は書きません。"),
        p("『NYLON JAPAN』12月号のKO1KEYZエディションでは、「子どものころにもらって印象に残っているプレゼント」として、YOSHIKIさんはクリスマスにもらった「ニンテンドー3DS」を挙げていました。",
          "「やっと自分専用のゲーム機ができた」とうれしかったそうなので、それまではお姉ちゃんとゲーム機を一緒に使っていたのかもしれません。",
          "年の近いきょうだいとして、いっしょに遊びながら育ってきた様子が想像できますね。"),

        h2("実家は音楽一家？トランペットとバイオリンがある"),
        ui.minibox("<strong>わかっていること:</strong>実家にトランペットとバイオリンがある",
                   "<strong>出典:</strong>公式のQ&A動画(本人の回答)"),
        p("公式のQ&A動画で「ギター以外にできる楽器はありますか？」という質問が届いたとき、YOSHIKIさんは「家にはトランペットとバイオリンがあるので」と答えていました。",
          f"ギター以外にも、{mk('実家にあるトランペットやバイオリンに触れられる環境')}で育ったようです。"),
        p("トランペットとバイオリンがふつうに家にあるのは珍しく、家族のだれかが演奏していた可能性もありそうです。",
          "誰の楽器なのかまでは明かしていませんが、お母さんが長年のアイドル好きだったことも合わせると、音楽が身近な家庭だったことがうかがえます。",
          "高校時代は軽音楽部で部長を務め、ギター＆ボーカルを担当していたYOSHIKIさんの音楽好きは、こうした家庭環境で育まれたのかもしれません。"),

        h2("実家では猫を2匹飼っている"),
        ui.minibox("<strong>わかっていること:</strong>猫を2匹飼っている",
                   "<strong>出典:</strong>『MZINE』(2026年10月はじめ放送)の「素顔POINT」"),
        p("デビュー直前のKO1KEYZを特集した『MZINE』では、メンバーが15秒で自分の魅力をアピールするコーナーがありました。",
          f"そこで紹介されたYOSHIKIさんの「素顔POINT」の1つが{mk('猫を2匹飼っている')}です。",
          "画面には、カゴの中でおなかを出してくつろぐキジトラ白の猫の写真が映っていました。"),
        p("ほかの素顔POINTは「高校時代は軽音楽部(部長)」「ミセスの大ファン」「お菓子作りが得意」。",
          "ファンのあいだで「デカ猫」と呼ばれるYOSHIKIさんですが、家族の一員として本物の猫2匹と暮らしてきたんですね。"),

        h2("日プ最終回には母と姉が家族席に"),
        p("6月6日に放送された『PRODUCE 101 JAPAN 新世界』の最終回では、会場の家族席が映る場面がありました。",
          "放送を見たファンによると、YOSHIKIさんの家族席にはお母さんとお姉ちゃんの姿があったそうです。"),
        p(f"YOSHIKIさんはこの最終回で{mk('最終2位')}に選ばれ、KO1KEYZのメンバーとしてデビューが決まりました。",
          "デビューが決まる瞬間を、お母さんとお姉ちゃんが会場で見届けていたことになります。"),

        h2("家族思いのエピソード"),
        p("YOSHIKIさんはトーク会や番組で、家族のことを飾らずにうれしそうに話すタイプです。",
          "お母さんの推しがきっかけでロールモデルが決まったり、ファンの名前を見てお姉ちゃんを思い出したりと、家族の存在がいつも近くにあることが伝わってきます。"),
        ui.quotebox("ファンの声", [
            "「お姉ちゃんと仲良し佳暉くん、よしよし」",
            "「お母さんの推しの後輩になったのすごい」",
            "「お母さんと一緒にライブに行ってたのかわいすぎる」",
            "「お父さんの話でトークの輪に入れるの嬉しい、楽しみ」"]),
        p("デビュー前のライブPRでは、YOSHIKIさんは「12人で家族のように、10年、20年続くグループに」と話していました。",
          "実の家族を大切にしているYOSHIKIさんらしい言葉ですね。"),

        h2("まとめ"),
        ui.summary([
            "<strong>家族構成</strong>:父・母・4歳上の姉・本人の4人家族とみられる",
            "<strong>父親</strong>:関西ではおなじみの会社に勤める(さんま御殿11/10放送で思い出を披露)",
            "<strong>母親</strong>:テミンの長年のファンでソロコンサートにも。JO1川尻蓮さんのファンでもある",
            "<strong>姉</strong>:4歳上(9/21ヨントンで本人談)。日プ最終回は母と姉が家族席に",
            "<strong>家庭環境</strong>:実家にはトランペットとバイオリン、猫が2匹。お母さんの影響でK-POPにも触れて育った",
        ]),
        p("『踊る！さんま御殿!!』でお父さんとのどんな思い出が語られるのか、放送が楽しみですね。",
          "放送後にはこの記事にもエピソードを追記します。家族の支えを受けて夢をつかんだYOSHIKIさんを、これからも応援していきましょう！"),
        ui.quotebox("あわせて読みたい", [a(u, t) for u, t in REL["ja"]]),
    ]
    jp_sum = ("KO1KEYZのYOSHIKI(矢田佳暉)の家族構成を調査。4歳上のお姉ちゃん、テミン推しのお母さん、"
              "11/10さんま御殿で話す「関西でおなじみの会社」に勤めるお父さん。本人発言をもとにまとめました。")

    # ---------------- KR ----------------
    kr_title = "【未】【KO1KEYZ】YOSHIKI 가족 관계는? 아빠·엄마·4살 위 누나"
    kr = [
        p("『PRODUCE 101 JAPAN 新世界』 최종 2위로 KO1KEYZ(코이키즈) 멤버로 데뷔한 YOSHIKI(야다 요시키).",
          "11월 10일(화)에는 일본 예능 『踊る！さんま御殿!!(오도루! 산마고텐)』에 첫 출연해 아버지와의 추억을 이야기할 예정이에요."),
        p(f"결론부터 말하면, YOSHIKI의 가족은 {mk('아빠·엄마·4살 위 누나')}가 있는 것으로 알려져 있어요.",
          "본인이 직접 말한 내용과 방송 공식 정보만을 바탕으로 정리했어요."),
        ui.table("YOSHIKI(야다 요시키) 프로필", [
            ("이름", "矢田 佳暉(야다 요시키)"),
            ("생년월일", "2004년 6월 18일"),
            ("출신", "일본 나라현"),
            ("키", "177cm"),
            ("멤버 컬러", "핑크"),
            ("경력", "『PRODUCE 101 JAPAN 新世界』 최종 2위 → 2026년 10월 7일 KO1KEYZ로 데뷔"),
        ]),
        h2("YOSHIKI의 가족 구성은?"),
        p("지금까지 YOSHIKI가 이야기한 가족은 아빠, 엄마, 누나 3명이에요.",
          f"형이나 남동생, 여동생에 대한 언급은 없어서 {mk('아빠·엄마·누나·YOSHIKI의 4인 가족')}으로 보여요.",
          "공식 프로필에 가족 구성이 발표된 것은 아니에요."),
        h2("아버지는? '간사이에서 친숙한 회사'에 근무"),
        p("11월 10일 밤 8시(일본 시간) 방송되는 『踊る！さんま御殿!!』의 주제는 '간사이 이웃 현 배틀'로, YOSHIKI는 나라현 대표로 첫 출연해요.",
          "방송 공식 X에는 이런 예고가 올라왔어요."),
        ui.quotebox("『踊る！さんま御殿!!』 공식 예고", [
            "나라 vs 시가 배틀에 좀처럼 끼지 못하는 YOSHIKI 씨, 사실 이유가…",
            f"{mk('간사이에서는 친숙한 회사에 다니는 아버지와의 추억도!')}",
            "(11/9 추가 예고) 긴장해서 좀처럼 대화에 끼지 못했지만… 아버지 이야기로 드디어 토크에 합류!"]),
        p("첫 예능 토크에서 긴장했지만 아버지 이야기로 분위기를 살린 것 같아요.",
          "아버지는 일반인이기 때문에 이 글에서는 회사 이름은 적지 않아요. 방송 후 에피소드를 추가할게요."),
        h2("어머니는? 태민·JO1 카와시리 렌의 팬"),
        p("9월 12일 영통에서 '롤모델이 태민인 이유'를 묻자 YOSHIKI는 이렇게 답했어요."),
        ui.quotebox("9월 12일 영통", [
            "팬: 롤모델이 태민이라고 했잖아? 이유가 궁금해!",
            f"YOSHIKI: {mk('엄마! 엄마가 계속 정말 좋아해서 솔로 콘서트도 가고 있어')}",
            "팬: SM 좋아해?",
            "YOSHIKI: SM 엄청 좋아해!"]),
        p("롤모델 태민은 원래 어머니가 오랫동안 좋아한 아티스트였던 거예요. 같은 날 SM에서 또 좋아하는 사람으로 '창민 씨!'(동방신기)를 꼽기도 했어요.",
          f"또 KO1KEYZ 팬북에는 어머니가 JO1 카와시리 렌의 팬이라고 적혀 있었다고 해요. {mk('엄마의 최애의 직속 후배가 된 셈')}이죠.",
          "영통은 영상이 공개되지 않아 실제 말투와 조금 다를 수 있어요."),
        h2("누나와는 몇 살 차이? 4살 위 누나"),
        ui.quotebox("9월 21일 영통", ["팬: 누나랑 몇 살 차이야?", f"YOSHIKI: {mk('4!')}"]),
        p("YOSHIKI는 2004년 6월생이니 누나는 2000년 무렵생으로 보여요.",
          "9월 5일 오사카 오프라인 특전회에서는 팬의 이름표를 보고 '누나랑 이름 똑같아!!!'라며 놀랐다고 해요. 누나는 일반인이라 이름은 적지 않아요."),
        h2("본가에는 트럼펫과 바이올린, 고양이 2마리"),
        p("공식 Q&A 영상에서 '기타 외에 다룰 수 있는 악기가 있나요?'라는 질문에 YOSHIKI는 '집에 트럼펫과 바이올린이 있어서'라고 답했어요.",
          f"또 일본 방송 『MZINE』(10월 초 방송)의 '맨얼굴 POINT'에서는 {mk('고양이 2마리를 키우고 있다')}고 소개됐어요. 고등학교 때는 경음악부 부장이었다고 해요."),
        h2("일프 최종회 가족석에 엄마와 누나"),
        p(f"6월 6일 방송된 최종회에서 YOSHIKI는 {mk('최종 2위')}로 데뷔를 확정했어요. 방송에 비친 가족석에는 어머니와 누나가 있었다고 해요."),
        h2("팬들의 반응"),
        ui.minibox("\"누나랑 사이좋은 요시키 귀여워\"",
                   "\"엄마 최애의 후배가 되다니 대단해\"",
                   "\"엄마랑 같이 콘서트 다녔다니 너무 귀여워\"",
                   "\"아버지 이야기로 토크에 합류했다니 기대돼\""),
        h2("정리"),
        ui.summary([
            "<strong>가족 구성</strong>: 아빠·엄마·4살 위 누나·본인의 4인 가족으로 보임",
            "<strong>아버지</strong>: 간사이에서 친숙한 회사 근무 (11/10 산마고텐에서 추억 공개)",
            "<strong>어머니</strong>: 태민의 오랜 팬, JO1 카와시리 렌의 팬",
            "<strong>누나</strong>: 4살 위 (9/21 영통 본인 발언). 최종회 가족석에 엄마와 함께",
            "<strong>본가</strong>: 트럼펫과 바이올린이 있고 고양이 2마리를 키움",
        ]),
        p("방송 후 아버지와의 에피소드도 추가할게요. 가족의 응원을 받아 꿈을 이룬 YOSHIKI를 계속 응원해요!"),
    ]
    kr_sum = ("KO1KEYZ YOSHIKI(야다 요시키)의 가족 구성. 4살 위 누나, 태민 팬인 엄마, "
              "11/10 산마고텐에서 이야기할 '간사이에서 친숙한 회사'에 다니는 아빠까지 본인 발언으로 정리했어요.")

    # ---------------- EN ----------------
    en_title = "【未】KO1KEYZ YOSHIKI's Family: Parents & Older Sister"
    en = [
        p("YOSHIKI (Yoshiki Yada) finished 2nd on \"PRODUCE 101 JAPAN SHINSEKAI\" and debuted with KO1KEYZ.",
          "On November 10 he makes his first appearance on the NTV talk show \"Odoru! Sanma Goten!!\", where he's set to share a memory of his father."),
        p(f"In short: YOSHIKI's family includes {mk('his father, his mother and a sister four years older')}.",
          "This article sticks to what YOSHIKI himself has said and what the show has officially announced."),
        ui.table("YOSHIKI (Yoshiki Yada) profile", [
            ("Name", "Yoshiki Yada (矢田佳暉)"),
            ("Birthday", "June 18, 2004"),
            ("Hometown", "Nara Prefecture, Japan"),
            ("Height", "177 cm"),
            ("Member color", "Pink"),
            ("Career", "2nd place on PRODUCE 101 JAPAN SHINSEKAI; debuted with KO1KEYZ on Oct 7, 2026"),
        ]),
        h2("How many people are in YOSHIKI's family?"),
        p("YOSHIKI has talked about three family members: his dad, his mom and his older sister.",
          f"He has never mentioned a brother or a younger sibling, so it appears to be {mk('a family of four')}. There's no official family profile."),
        h2("His father works at a well-known Kansai company"),
        p("The Nov 10 episode (8 p.m. JST) is a \"Kansai neighbors battle,\" and YOSHIKI appears as Nara's representative. The show's official X teased:"),
        ui.quotebox("\"Odoru! Sanma Goten!!\" official preview", [
            "YOSHIKI just can't jump into the Nara vs. Shiga battle... and there's a reason why",
            f"{mk('Plus memories of his dad, who works at a company everyone in Kansai knows!')}",
            "(Nov 9 update) Too nervous to join in at first... until talk of his father finally pulled him into the conversation!"]),
        p("His father is a private individual, so we won't name the company. We'll add the episode after it airs."),
        h2("His mother is a longtime Taemin fan"),
        p("At a September 12 online fan call, a fan asked why his role model is SHINee's Taemin."),
        ui.quotebox("Sep 12 online fan call", [
            "Fan: You said your role model is Taemin. Why?",
            f"YOSHIKI: {mk('My mom! My mom has loved him forever. She even goes to his solo concerts.')}",
            "Fan: So you like SM?",
            "YOSHIKI: I love SM!"]),
        p("He also named TVXQ's Changmin when asked about other SM artists he likes.",
          f"According to fans, the KO1KEYZ fanbook says his mother is also a fan of JO1's Ren Kawashiri, which means {mk('her son became a direct junior of her favorite idol')} at LAPONE.",
          "Fan-call quotes come from fan reports, as the calls aren't broadcast, so wording may differ slightly."),
        h2("His older sister is four years older"),
        ui.quotebox("Sep 21 online fan call", ["Fan: How many years apart are you and your sister?", f"YOSHIKI: {mk('Four!')}"]),
        p("Since YOSHIKI was born in June 2004, his sister was likely born around 2000.",
          "At an offline event in Osaka on September 5, he reportedly glanced at a fan's name tag and exclaimed, \"Same name as my sister!\" She's a private individual, so we won't share her name."),
        h2("A trumpet, a violin and two cats at home"),
        p("In an official Q&A video, asked whether he plays any instruments besides guitar, YOSHIKI answered, \"We have a trumpet and a violin at home.\"",
          f"On the TV show \"MZINE\" (aired in early October), one of his \"real me\" points was that {mk('he has two cats')}. He was also president of his high school's light music club."),
        h2("Mom and sister at the PRODUCE 101 finale"),
        p(f"YOSHIKI secured his debut by finishing {mk('2nd')} in the June 6 finale. Viewers noticed his mother and sister in the family seats."),
        h2("Summary"),
        ui.summary([
            "<strong>Family</strong>: father, mother, older sister and YOSHIKI (likely a family of four)",
            "<strong>Father</strong>: works at a well-known Kansai company; story airs on Sanma Goten Nov 10",
            "<strong>Mother</strong>: longtime Taemin fan; also a fan of JO1's Ren Kawashiri",
            "<strong>Sister</strong>: four years older (Sep 21 fan call); attended the finale with their mom",
            "<strong>Home</strong>: a trumpet and a violin, plus two cats",
        ]),
        p("We'll update this article after the broadcast. Keep cheering on YOSHIKI!"),
    ]
    en_sum = ("KO1KEYZ's YOSHIKI has a sister four years older, a mom who's a longtime Taemin fan, "
              "and a dad at a well-known Kansai company he talks about on Sanma Goten (Nov 10).")

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
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"), "--top", "YOSHIKIの家族構成は？",
                    "--main", "KO1KEYZ", "--bottom", "父・母・4歳上の姉を調査！", "--out", str(EYE), "--seed", "1110"], check=True)


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
    if "--update" in sys.argv:
        for pid, c in ((15541, jc), (15542, kc), (15543, ec)):
            r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers={**HA, "Content-Type": "application/json"},
                              data=json.dumps({"content": c, "status": "draft"}).encode("utf-8"))
            r.raise_for_status()
            print("UPDATED", pid, r.json()["status"])
        sys.exit(0)
    make_eyecatch()
    eye = upload(EYE, "image/png")["id"]
    jp = post_draft(jt, jc, BASE_SLUG, "ja", [66, 12, 84], eye, js)
    print("JP", jp["id"], jp["slug"], jp["link"])
    kr = post_draft(kt, kc, BASE_SLUG + "-kr", "ko", [74], eye, ks)
    print("KR", kr["id"], kr["slug"], kr["link"])
    en = post_draft(et, ec, BASE_SLUG + "-en", "en", [110], eye, es)
    print("EN", en["id"], en["slug"], en["link"])
    print("eyecatch", eye)
    subprocess.run([sys.executable, str(ROOT / "tools" / "check_ko1keyz_title.py"), str(jp["id"]), str(kr["id"]), str(en["id"])])
