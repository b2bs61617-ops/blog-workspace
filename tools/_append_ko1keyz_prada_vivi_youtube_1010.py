# -*- coding: utf-8 -*-
"""KO1KEYZ×プラダ リップ ジェリー記事(chomoand-1 公開中 JP14139/KR14140/EN14141)に、
2026-10-09 12:00 JST公開のViVi YouTube本編「【KO1KEYZ】潤いリップでイケメン力を競え！」の内容を追記する。

- 「アンバサダー？今後の告知は？」節: 10/9の告知=YouTube本編だったことに書き換え、日付を10/10時点に更新。
- その直後(まとめの直前)に新H2「10月9日公開のYouTube本編はどんな内容？」を追加
  (チーム分けと勝敗/12人のキャッチコピー/RYOGAの夏油傑オマージュ/推しリップ/衣装)。
- 冒頭リード・「この記事でわかること」・まとめも更新。
- タイトル・statusは送らない(公開済みのため)。id="vivi-youtube-honpen"があれば何もしない(二重追記防止)。

一次ソース: https://www.youtube.com/watch?v=1GRRJt2-G8Y (ViVi channel、23:57)。
RYOGAの台詞が夏油傑のオマージュなのは動画内のViVi字幕(7:06頃)で明記。本文画像は動画フレーム(7:14、22:32)。
衣装はViVi側のスタイリングで、概要欄・vivi.tvにクレジットなし(ブランド未特定)。

python tools/_append_ko1keyz_prada_vivi_youtube_1010.py [--dry]
"""
import json
import re
import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from ko1keyz_article_kit import WP_URL, HEADERS_AUTH as HA, Ui, wphtml, p, h2, a  # noqa: E402

IDS = {"ja": 14139, "ko": 14140, "en": 14141}
MARK = 'id="vivi-youtube-honpen"'
YT = "https://www.youtube.com/watch?v=1GRRJt2-G8Y"
IMG_RYOGA = ROOT / "images" / "ko1keyz_prada_vivi_yt_ryoga.jpg"
IMG_12 = ROOT / "images" / "ko1keyz_prada_vivi_yt_12members.jpg"
RYOGA_LIST = {"ja": 11782, "ko": 12547, "en": 12549}

ui = Ui("#8a8378", "#ddd9d3", "#f7f6f4", "rgba(138,131,120,0.06)")
L = lambda pid: f"https://chomoand-1.com/?p={pid}"


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def h2id(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading" {MARK}>{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def embed():
    return (f'<!-- wp:embed {{"url": "{YT}", "type": "video", "providerNameSlug": "youtube", "responsive": true, '
            f'"className": "wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->\n'
            f'<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">'
            f'<div class="wp-block-embed__wrapper">\n{YT}\n</div></figure>\n<!-- /wp:embed -->')


def grid(rows):
    td = "border:1px solid #ddd9d3;padding:8px 10px;vertical-align:top;"
    trs = []
    for i, row in enumerate(rows):
        bg = "background:#8a8378;color:#fff;font-weight:bold;" if i == 0 else ("" if i % 2 else "background:#f7f6f4;")
        trs.append("<tr>" + "".join(f'<td style="{td}{bg}">{c}</td>' for c in row) + "</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            + "".join(trs) + '</tbody></table></figure>\n<!-- /wp:table -->')


def fig(media, alt, caption):
    md = media["media_details"]
    sizes = md.get("sizes", {})
    full = media["source_url"]
    large = sizes.get("large", {"source_url": full, "width": md["width"]})
    medium = sizes.get("medium", {"source_url": full, "width": md["width"]})
    w = large["width"]
    h = int(w * md["height"] / md["width"])
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full} {md["width"]}w'
    return wphtml(f'<figure class="wp-block-image size-large">\n<img src="{large["source_url"]}" alt="{alt}" width="{w}" height="{h}"\n'
                  f'  style="max-width:100%;height:auto;"\n  srcset="{srcset}"\n  sizes="(max-width: {w}px) 100vw, {w}px">\n'
                  f'<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>\n</figure>')


CAP = {"ja": f'出典:{a(YT, "ViVi channel(YouTube)")}',
       "ko": f'출처: {a(YT, "ViVi channel(YouTube)")}',
       "en": f'Source: {a(YT, "ViVi channel (YouTube)")}'}

# (member, team, copy) in the order they were presented (Blue first, then Green)
COPIES = [
    ("KEITO", "blue", "君と僕を結ぶ冬の大三角形 人肌恋しいこれからの季節に"),
    ("SIYOUNG", "blue", "Lips, Dip, Kiss. I'm PRADA"),
    ("YUKI", "blue", "ぷくぷく唇へあなたを導きます PRADA リップジェリー"),
    ("ISSA", "blue", "ぷっくり潤い 惹かれる口元へ PRADA"),
    ("RYOGA", "blue", "グリーン:アフロディーテのようなふっくら唇へ<br>ブルー:ヴィーナスのようなぷっくり唇へ"),
    ("YURA", "blue", "PRADA LIP JELLY 青い鳥も気になって駆け寄ってくるリップ！！"),
    ("DAIKI", "green", "プリンよりも俺の唇"),
    ("YOSHIKI", "green", "口元に仕上げの立体感 一振りでつい目で追ってしまう高級感"),
    ("SHINHAENG", "green", "Unlock Your Lips! 今日もPRADA"),
    ("TOWA", "green", "PRADAを纏う唇"),
    ("KOSUKE", "green", "PRADAの潤いで毎日のくちびるを12ランクアップ"),
    ("RYUJI", "green", "もう割らせない。あなたの人生に笑顔とつやめきを。"),
]
COPIES_TR = {  # meaning of each copy for KR/EN readers
    "ko": {
        "KEITO": "너와 나를 잇는 겨울의 대삼각형, 사람의 온기가 그리워지는 이 계절에",
        "YUKI": "통통한 입술로 당신을 이끌어 드립니다 PRADA 립 젤리",
        "ISSA": "통통한 촉촉함, 끌리는 입가로 PRADA",
        "RYOGA": "그린: 아프로디테 같은 도톰한 입술로<br>블루: 비너스 같은 탱탱한 입술로",
        "YURA": "PRADA LIP JELLY 파랑새도 궁금해서 달려오는 립!!",
        "DAIKI": "푸딩보다 내 입술",
        "YOSHIKI": "입가에 마무리하는 입체감, 한 번 바르면 저절로 눈길이 가는 고급스러움",
        "TOWA": "PRADA를 두른 입술",
        "KOSUKE": "PRADA의 촉촉함으로 매일의 입술을 12랭크 업",
        "RYUJI": "더는 갈라지게 두지 않아. 당신의 인생에 미소와 윤기를.",
    },
    "en": {
        "KEITO": "\"The Winter Triangle that links you and me — for the season when you crave someone's warmth\"",
        "YUKI": "\"Leading you to plump, bouncy lips — PRADA Lip Jelly\"",
        "ISSA": "\"Plump moisture for lips that draw you in — PRADA\"",
        "RYOGA": "Green: \"To soft, full lips like Aphrodite's\"<br>Blue: \"To plump lips like Venus's\"",
        "YURA": "\"PRADA LIP JELLY — a lip even the bluebird can't resist running to!!\"",
        "DAIKI": "\"My lips over pudding\"",
        "YOSHIKI": "\"A finishing touch of dimension for your lips — luxury that draws the eye with one swipe\"",
        "TOWA": "\"Lips dressed in PRADA\"",
        "KOSUKE": "\"PRADA moisture takes your everyday lips up 12 ranks\"",
        "RYUJI": "\"No more cracked lips. Smiles and shine for your life.\"",
    },
}
TEAM = {"ja": {"blue": "ブルー", "green": "グリーン"}, "ko": {"blue": "블루", "green": "그린"},
        "en": {"blue": "Blue", "green": "Green"}}


def copy_table(lang):
    head = {"ja": ("メンバー", "チーム", "キャッチコピー"), "ko": ("멤버", "팀", "캐치프레이즈"),
            "en": ("Member", "Team", "Catchphrase")}[lang]
    rows = [head]
    for m, t, c in COPIES:
        cell = c if lang == "ja" else COPIES_TR[lang].get(m, c)
        rows.append((m, TEAM[lang][t], cell))
    return grid(rows)


def section(lang, med):
    ryoga_list = L(RYOGA_LIST[lang])
    if lang == "ja":
        return [
            h2id("10月9日公開のYouTube本編はどんな内容？"),
            ui.minibox("<strong>公開:</strong>2026年10月9日(金)12時、ViVi公式YouTube「ViVi channel」",
                       "<strong>長さ:</strong>約24分",
                       "<strong>結果:</strong>キャッチコピー対決でグリーンチームが勝利"),
            p("予告されていた「10/9(金)12時の次なる告知」は、ViVi公式YouTubeの本編動画でした。",
              "タイトルは「【KO1KEYZ】潤いリップでイケメン力を競え！ 個性もケミも炸裂しまくり、爆笑の20分♡」で、プラダ リップ ジェリーにちなんだ2つのミニゲームに12人が挑戦しています。",
              "Instagramの動画のラストで、メンバーがイスに座って盛り上がっていた場面は、この企画のワンシーンでした。"),
            embed(),
            p("進行役は、遅れて登場した「美容番長」のDAIKIとKEITOです。",
              "2人の説明によると、グリーンはヒアルロン酸とビタミンE入りで乾燥した唇を集中保湿、ブルーはメントールとサリチル酸入りで塗った瞬間にひんやりする清涼感があるとのこと。",
              f"さらに{mk('2つのケースはくっつけて連結できる')}ので、つなげて持ち歩けば気分や用途で使い分けられるそうです。"),
            h3("チーム分けと勝敗は？"),
            ui.table("チーム分けと結果", [
                ("グリーンチーム", "SHINHAENG・TOWA・YOSHIKI・DAIKI・KOSUKE・RYUJI"),
                ("ブルーチーム", "ISSA・YURA・RYOGA・KEITO・SIYOUNG・YUKI"),
                ("①かっこいいリップの塗り方対決", "引き分け"),
                ("②キャッチコピー対決", "グリーンチームの勝ち"),
            ]),
            p("チームは、メンバーが直感で選んだ色で2つに分かれました。",
              "1つ目の「かっこいいリップの塗り方対決」では、1人ずつ考えた「一番かっこいい塗り方」と、チームの盛り上げ方が審査されます。",
              "RYUJIがDAIKIに「月がキレイだね」とささやいて片ひざをつき、指輪の代わりにリップジェリーを差し出してプロポーズしたり、KOSUKEがターンだけで勝負したりと、個性が出すぎた結果は引き分けでした。"),
            p("決着は2つ目の「キャッチコピー対決」に持ち越され、グリーンチームが勝利。",
              "勝ったグリーンチームにはプラダ ビューティのスペシャルギフトボックスとエンディング妖精タイム、負けたブルーチームには「美リップで届ける胸キュン台詞」の披露が待っていました。",
              "YURAの「俺とキスしようぜ」、RYOGAの「俺のヴィーナスになって？」など、罰ゲームのはずのブルーチームの台詞もしっかり見どころになっています。"),
            h3("12人のキャッチコピー一覧"),
            p("2つ目の対決では、3分で考えたオリジナルのキャッチコピーをボードに書いて発表しました。",
              "発表順(ブルーチーム→グリーンチーム)に並べると次のとおりです。"),
            copy_table("ja"),
            p("KEITOは自分が01 ブルー、相手が00 グリーンを持って連結する様子を「君と僕を結ぶ」と表現し、RYOGAはローマ神話のヴィーナスとギリシャ神話のアフロディーテが同じ女神であることを2色に重ねました。",
              f"SHINHAENGは{mk('プラダのロゴの逆三角形が鍵の形にも見える')}ことに注目し、「僕たちKO1KEYZはみなさんのハートをUnlockする、でもプラダはみなさんのリップをUnlockする」とグループのキャッチフレーズにつなげています。",
              "それぞれの性格がよく出ていて、どれを選んでもいいくらいの完成度でした。"),
            h3("RYOGAの「この組織は僕が支配します」は夏油傑のオマージュ"),
            fig(med["ryoga"], "首元に手を添えて「KO1LY」と決めるRYOGA", CAP["ja"]),
            p("塗り方対決でひときわ盛り上がったのが、ブルーチームのRYOGAのパートです(動画の7:00ごろ)。",
              "指先で唇にジェリーをのせながら「みなさん！この組織は僕が支配します！」「〇〇さんこちらへ！」と語りかけ、最後は首元に手を添えて「KO1LY」と決めました。",
              f"このシーンにはViViの字幕で{mk('「『呪術廻戦』に登場する夏油傑の台詞のオマージュです」')}と説明が入っています。"),
            p("首に手を当てるポーズも、原作で夏油傑が「私に従え 猿共」と言うコマを思わせる角度です。",
              "見ていたメンバーからは「いろんな意味で敵わないでしょ？」と声が上がり、エンディングの胸キュン台詞では「俺のヴィーナスになって？」と自分のキャッチコピーにつなげていました。"),
            p("RYOGAは漫画・アニメ好きで知られていて、『呪術廻戦』の推しキャラはまさに夏油傑です。",
              f"履修済みの作品は{a(ryoga_list, 'RYOGAの漫画・アニメ一覧の記事')}でまとめています。"),
            h3("12人が選んだ推しリップはどっち？"),
            fig(med["twelve"], "推しリップを発表するKO1KEYZの12人", CAP["ja"]),
            p("最後に12人がもう一度両方を塗り比べて、推しリップを1本ずつ選びました。",
              "ブルー派からは「スースーする清涼感がいい」「塗ったら唇がぷっくりした」、グリーン派からは「寝る前の乾燥に困っていたので、ヒアルロン酸入りがうれしい」といった声が出ています。",
              f"結果は{mk('ブルーとグリーンがほぼ半々')}で、「どっちも良すぎて選べなかった」「用途によって使い分けたい」という結論になりました。"),
            h3("12人の衣装は？"),
            p("12人の衣装は、チームカラーに合わせたパステルカラーでそろえられていました。",
              "グリーンチームはミントやセージグリーンと白、ブルーチームは水色・ラベンダー・白が中心です。",
              "YURAは生成りのニットを肩に掛け、SHINHAENGは水色の透かし編みニット、KEITOは大きな襟のプルオーバーにシルバーのネックレスを重ねるなど、同じ色味の中でも1人ずつ形を変えています。"),
            p("動画の概要欄やViViの公式サイトには衣装ブランドのクレジットが載っておらず、2026年10月10日時点ではブランドは特定できていません。",
              "撮影のためにスタイリングされた衣装とみられるので、私服とは分けて見ておくのがよさそうです。"),
        ]
    if lang == "ko":
        return [
            h2id("10월 9일 공개된 YouTube 본편은 어떤 내용?"),
            ui.minibox("<strong>공개:</strong>2026년 10월 9일(금) 12시(일본 시간), ViVi 공식 YouTube 'ViVi channel'",
                       "<strong>길이:</strong>약 24분",
                       "<strong>결과:</strong>캐치프레이즈 대결에서 그린 팀 승리"),
            p("예고됐던 '10/9(금) 12시의 다음 공지'는 ViVi 공식 YouTube의 본편 영상이었어요.",
              "제목은 '【KO1KEYZ】潤いリップでイケメン力を競え！(촉촉한 립으로 훈남력을 겨뤄라!)'로, 프라다 립 젤리를 주제로 한 미니게임 2개에 12명이 도전했어요.",
              "Instagram 영상 마지막에 멤버들이 의자에 앉아 신나 하던 장면도 바로 이 기획의 한 장면이었어요."),
            embed(),
            p("진행은 뒤늦게 '뷰티 반장'으로 등장한 DAIKI와 KEITO가 맡았어요.",
              "두 사람의 설명에 따르면 그린은 히알루론산과 비타민E가 들어 있어 건조한 입술을 집중 보습하고, 블루는 멘톨과 살리실산이 들어 있어 바르는 순간 시원한 청량감이 있다고 해요.",
              f"게다가 {mk('두 케이스는 서로 연결할 수 있어서')} 붙여서 들고 다니면 기분이나 용도에 따라 골라 쓸 수 있대요."),
            h3("팀 구성과 승패는?"),
            ui.table("팀 구성과 결과", [
                ("그린 팀", "SHINHAENG・TOWA・YOSHIKI・DAIKI・KOSUKE・RYUJI"),
                ("블루 팀", "ISSA・YURA・RYOGA・KEITO・SIYOUNG・YUKI"),
                ("① 멋있게 립 바르기 대결", "무승부"),
                ("② 캐치프레이즈 대결", "그린 팀 승리"),
            ]),
            p("팀은 멤버들이 직감으로 고른 컬러에 따라 둘로 나뉘었어요.",
              "첫 번째 '멋있게 립 바르기 대결'에서는 각자 생각한 '가장 멋있게 바르는 법'과 팀의 분위기 띄우기가 심사 대상이었어요.",
              "RYUJI가 DAIKI에게 '달이 예쁘네'라고 속삭이고 한쪽 무릎을 꿇은 뒤 반지 대신 립 젤리를 내밀며 프러포즈하거나, KOSUKE가 턴 하나로 승부하는 등 개성이 넘친 결과는 무승부였어요."),
            p("승부는 두 번째 '캐치프레이즈 대결'로 넘어갔고, 그린 팀이 승리했어요.",
              "이긴 그린 팀은 프라다 뷰티 스페셜 기프트 박스와 엔딩 요정 타임을, 진 블루 팀은 '예쁜 입술로 전하는 설렘 대사'를 선보였어요.",
              "YURA의 '나랑 키스하자', RYOGA의 '내 비너스가 되어 줄래?' 등 벌칙이었던 블루 팀의 대사도 놓칠 수 없는 장면이에요."),
            h3("12명의 캐치프레이즈 모음"),
            p("두 번째 대결에서는 3분 동안 생각한 오리지널 캐치프레이즈를 보드에 써서 발표했어요.",
              "발표 순서(블루 팀→그린 팀)대로 정리하면 다음과 같아요. 일본어 문구는 의미를 번역했어요."),
            copy_table("ko"),
            p("KEITO는 자신이 01 블루, 상대가 00 그린을 들고 연결하는 모습을 '너와 나를 잇는'이라고 표현했고, RYOGA는 로마 신화의 비너스와 그리스 신화의 아프로디테가 같은 여신이라는 점을 두 컬러에 겹쳤어요.",
              f"SHINHAENG은 {mk('프라다 로고의 역삼각형이 열쇠 모양으로도 보인다')}는 점에 주목해 '우리 KO1KEYZ는 여러분의 하트를 Unlock하고, 프라다는 여러분의 입술을 Unlock한다'며 그룹의 캐치프레이즈로 연결했어요.",
              "멤버마다 성격이 잘 드러나서 어느 것을 골라도 될 만큼 완성도가 높았어요."),
            h3("RYOGA의 '이 조직은 내가 지배합니다'는 게토 스구루 오마주"),
            fig(med["ryoga"], "목에 손을 대고 'KO1LY'를 외치는 RYOGA", CAP["ko"]),
            p("립 바르기 대결에서 특히 반응이 뜨거웠던 건 블루 팀 RYOGA의 차례예요(영상 7:00쯤).",
              "손끝으로 입술에 젤리를 올리며 '여러분! 이 조직은 내가 지배합니다!', '○○ 씨 이쪽으로!'라고 말을 건넨 뒤, 마지막에 목에 손을 대고 'KO1LY'로 마무리했어요.",
              f"이 장면에는 ViVi 자막으로 {mk('\"『주술회전』에 등장하는 게토 스구루의 대사 오마주입니다\"')}라는 설명이 들어가 있어요."),
            p("목에 손을 대는 포즈도 원작에서 게토 스구루가 '나를 따르라, 원숭이들'이라고 말하는 컷을 떠올리게 하는 각도예요.",
              "지켜보던 멤버들 사이에서는 '여러 의미로 못 이기겠다'는 말이 나왔고, 엔딩의 설렘 대사에서는 '내 비너스가 되어 줄래?'라며 자신의 캐치프레이즈와 이어 갔어요."),
            p("RYOGA는 만화·애니메이션을 좋아하는 것으로 알려져 있고, 『주술회전』의 최애 캐릭터가 바로 게토 스구루예요.",
              f"RYOGA가 본 작품은 {a(ryoga_list, 'RYOGA의 만화·애니메이션 목록 글')}에서 정리하고 있어요."),
            h3("12명이 고른 최애 립은 어느 쪽?"),
            fig(med["twelve"], "최애 립을 발표하는 KO1KEYZ 12명", CAP["ko"]),
            p("마지막으로 12명이 두 컬러를 다시 발라 보고 최애 립을 하나씩 골랐어요.",
              "블루파에서는 '화한 청량감이 좋다', '바르니까 입술이 통통해졌다', 그린파에서는 '자기 전 건조함 때문에 고민이었는데 히알루론산이 들어 있어서 좋다'는 의견이 나왔어요.",
              f"결과는 {mk('블루와 그린이 거의 반반')}으로, '둘 다 너무 좋아서 못 고르겠다', '용도에 따라 나눠 쓰고 싶다'는 결론이 났어요."),
            h3("12명의 의상은?"),
            p("12명의 의상은 팀 컬러에 맞춘 파스텔 톤으로 맞춰져 있었어요.",
              "그린 팀은 민트·세이지 그린과 화이트, 블루 팀은 하늘색·라벤더·화이트가 중심이에요.",
              "YURA는 아이보리 니트를 어깨에 두르고, SHINHAENG은 하늘색 비침 니트, KEITO는 큰 칼라의 풀오버에 실버 목걸이를 매치하는 등 같은 색감 안에서도 한 명씩 실루엣을 바꿨어요."),
            p("영상 설명란이나 ViVi 공식 사이트에는 의상 브랜드 크레디트가 없어서 2026년 10월 10일 기준으로 브랜드는 확인되지 않았어요.",
              "촬영용으로 스타일링된 의상으로 보이니 사복과는 구분해서 보는 게 좋겠어요."),
        ]
    return [
        h2id("What's in the full YouTube video released on October 9?"),
        ui.minibox("<strong>Released:</strong>October 9 (Fri), 2026 at 12:00 JST on ViVi's official YouTube channel, \"ViVi channel\"",
                   "<strong>Length:</strong>about 24 minutes",
                   "<strong>Result:</strong>Team Green won the catchphrase battle"),
        p("The \"next announcement on 10/9 (Fri) at 12:00\" turned out to be the full video on ViVi's official YouTube channel.",
          "Titled \"[KO1KEYZ] Compete in handsome power with moisturizing lips!\", it has all 12 members taking on two mini games built around the Prada Lip Jelly.",
          "The scene at the end of the Instagram video, with the members cheering in their chairs, was a moment from this project."),
        embed(),
        p("The hosts were DAIKI and KEITO, who showed up late as the \"beauty captains.\"",
          "According to their explanation, Green contains hyaluronic acid and vitamin E for intensive moisture on dry lips, while Blue contains menthol and salicylic acid for a cool, refreshing feel the moment you apply it.",
          f"On top of that, {mk('the two cases snap together')}, so you can carry them linked and switch depending on your mood or what you need."),
        h3("How were the teams split, and who won?"),
        ui.table("Teams and results", [
            ("Team Green", "SHINHAENG, TOWA, YOSHIKI, DAIKI, KOSUKE, RYUJI"),
            ("Team Blue", "ISSA, YURA, RYOGA, KEITO, SIYOUNG, YUKI"),
            ("(1) Coolest way to apply lip balm", "Draw"),
            ("(2) Catchphrase battle", "Team Green wins"),
        ]),
        p("The members split into two teams based on the color they picked on instinct.",
          "In the first game, \"the coolest way to apply lip balm,\" each member's idea and how well his team hyped him up were judged.",
          "RYUJI whispered \"The moon is beautiful, isn't it\" to DAIKI, went down on one knee and held out the Lip Jelly instead of a ring, while KOSUKE competed with nothing but a spin. With that much personality on display, the result was a draw."),
        p("The decision carried over to the second game, the catchphrase battle, and Team Green won.",
          "The winners got the PRADA BEAUTY special gift box and an \"ending fairy\" moment, while the losing Team Blue had to deliver heart-fluttering lines \"with beautiful lips.\"",
          "Lines like YURA's \"Let's kiss\" and RYOGA's \"Will you be my Venus?\" make Team Blue's penalty one of the highlights."),
        h3("All 12 catchphrases"),
        p("In the second game, each member wrote an original catchphrase on a board in three minutes and presented it.",
          "Here they are in presentation order (Team Blue, then Team Green). Japanese phrases are translated for meaning."),
        copy_table("en"),
        p("KEITO described linking his 01 Blue with someone else's 00 Green as \"linking you and me,\" and RYOGA matched the two shades to Venus of Roman myth and Aphrodite of Greek myth, who are the same goddess.",
          f"SHINHAENG pointed out that {mk('the inverted triangle of the Prada logo also looks like a key')}, tying it to the group's catchphrase: \"KO1KEYZ unlocks your heart, but Prada unlocks your lips.\"",
          "Every phrase reflected its writer's personality, and any of them could have won."),
        h3("RYOGA's \"I will rule this organization\" is a nod to Suguru Geto"),
        fig(med["ryoga"], "RYOGA striking a pose with his hand at his neck for \"KO1LY\"", CAP["en"]),
        p("The part that got the biggest reaction in the lip balm game was Team Blue's RYOGA (around 7:00 in the video).",
          "Dabbing the jelly onto his lips with a fingertip, he said \"Everyone! I will rule this organization!\" and \"Mr./Ms. So-and-so, this way!\", then finished with his hand at his neck and the word \"KO1LY.\"",
          f"ViVi's on-screen caption explains it as {mk('\"an homage to a line by Suguru Geto from Jujutsu Kaisen\"')}."),
        p("The hand-on-the-neck pose also recalls the manga panel where Geto says \"Obey me, you monkeys.\"",
          "His teammates reacted with \"There's no beating that, in more ways than one,\" and in the ending he tied it back to his catchphrase with \"Will you be my Venus?\""),
        p("RYOGA is known as a big manga and anime fan, and his favorite Jujutsu Kaisen character is none other than Suguru Geto.",
          f"We list the titles he's read in {a(ryoga_list, 'our article on RYOGA’s manga and anime list')}."),
        h3("Which lip did the 12 members pick as their favorite?"),
        fig(med["twelve"], "The 12 KO1KEYZ members revealing their favorite Lip Jelly", CAP["en"]),
        p("At the end, all 12 tried both shades again and each picked a favorite.",
          "Blue fans said things like \"I love the minty, cooling feel\" and \"my lips got plumper,\" while Green fans said \"I've been struggling with dryness before bed, so the hyaluronic acid is great.\"",
          f"The result was {mk('an almost even split between Blue and Green')}, ending with \"they're both too good to choose\" and \"I want to use them for different things.\""),
        h3("What were the 12 members wearing?"),
        p("The outfits were coordinated in pastels matching each team's color.",
          "Team Green wore mostly mint, sage green and white, while Team Blue wore light blue, lavender and white.",
          "YURA had an ecru knit draped over his shoulders, SHINHAENG wore a light-blue open-knit sweater, and KEITO layered a silver necklace over a big-collared pullover, so each member's silhouette differs within the same palette."),
        p("Neither the video description nor ViVi's official site credits the clothing brands, so as of October 10, 2026, the brands have not been identified.",
          "These appear to be outfits styled for the shoot, so it's best not to treat them as the members' own clothes."),
    ]


EDITS = {
    "ja": [
        ("この記事では、動画の中身と12人の登場シーン、2色の違い、どんなリップなのか、どこで買えるのかまでまとめました。</p>",
         "この記事では、動画の中身と12人の登場シーン、2色の違い、どんなリップなのか、どこで買えるのかまでまとめました。<br>\n"
         "2026年10月9日にViVi公式YouTubeで公開された本編動画の内容も追記しています。</p>"),
        ("<li>プラダのアンバサダー？今後の告知は？</li>",
         "<li>プラダのアンバサダー？10月9日の告知は？</li>\n<li>YouTube本編の内容・勝敗とRYOGAの夏油傑オマージュ</li>"),
        ("<strong>アンバサダー:</strong>2026年10月3日時点で発表なし(ViViのPR企画)",
         "<strong>アンバサダー:</strong>2026年10月10日時点で発表なし(ViViとプラダ ビューティのコラボ企画)"),
        ("<strong>次の告知:</strong>2026年10月9日(金)12時にViViから",
         "<strong>10月9日(金)12時の告知:</strong>ViVi公式YouTubeで本編動画を公開"),
        ("2026年10月3日時点では、", "2026年10月10日時点でも、"),
        (re.compile(r"<p>気になるのは、ViViの投稿文に.*?</p>", re.S),
         "<p>ViViの投稿文で予告されていた" + mk("「来週10/9(金)の12時には、次なる告知が…！」") + "の中身は、ViVi公式YouTubeでの本編動画の公開でした。<br>\n"
         "Instagramの動画のラストに映っていた「Coming Soon...」の場面も、この本編の一部です。<br>\n"
         "どんな企画だったのかは、次の章でくわしく紹介します。</p>"),
        ("ViViから10月9日(金)12時に次の告知が予定されている",
         "10月9日(金)12時にViVi公式YouTubeで本編が公開され、キャッチコピー対決でグリーンチームが勝利<br>"
         + ui.check("RYOGAの「この組織は僕が支配します」は『呪術廻戦』夏油傑の台詞のオマージュ(ViViの字幕で明記)")),
    ],
    "ko": [
        ("<li>프라다 앰버서더? 다음 공지는?</li>",
         "<li>프라다 앰버서더? 10월 9일 공지는?</li>\n<li>YouTube 본편 내용·승패와 RYOGA의 게토 스구루 오마주</li>"),
        ("<strong>앰버서더:</strong>2026년 10월 3일 기준 발표 없음(ViVi의 PR 기획)",
         "<strong>앰버서더:</strong>2026년 10월 10일 기준 발표 없음(ViVi와 프라다 뷰티의 콜라보 기획)"),
        ("<strong>다음 공지:</strong>2026년 10월 9일(금) 12시 ViVi에서",
         "<strong>10월 9일(금) 12시 공지:</strong>ViVi 공식 YouTube에서 본편 영상 공개"),
        ("2026년 10월 3일 기준으로는 ", "2026년 10월 10일 기준으로도 "),
        (re.compile(r"<p>눈길을 끄는 건 ViVi 게시글에.*?</p>", re.S),
         "<p>ViVi 게시글에서 예고했던 " + mk("'다음 주 10/9(금) 12시에는 다음 공지가…!'") + "의 정체는 ViVi 공식 YouTube의 본편 영상 공개였어요.<br>\n"
         "Instagram 영상 마지막에 나온 'Coming Soon...' 장면도 이 본편의 일부예요.<br>\n"
         "어떤 기획이었는지는 다음 장에서 자세히 소개할게요.</p>"),
        ("ViVi에서 10월 9일(금) 12시에 다음 공지 예정",
         "10월 9일(금) 12시 ViVi 공식 YouTube에서 본편 공개, 캐치프레이즈 대결에서 그린 팀 승리<br>"
         + ui.check("RYOGA의 '이 조직은 내가 지배합니다'는 『주술회전』 게토 스구루 대사 오마주(ViVi 자막에 명시)")),
    ],
    "en": [
        ("<li>Are they Prada ambassadors? What's next?</li>",
         "<li>Are they Prada ambassadors? What was announced on October 9?</li>\n<li>The full YouTube video, who won, and RYOGA's Suguru Geto homage</li>"),
        ("<strong>Ambassadors:</strong>no announcement as of October 3, 2026 (this was a ViVi PR project)",
         "<strong>Ambassadors:</strong>no announcement as of October 10, 2026 (a ViVi x PRADA BEAUTY collaboration)"),
        ("<strong>Next announcement:</strong>October 9 (Fri), 2026 at 12:00 JST from ViVi",
         "<strong>October 9 (Fri) 12:00 JST announcement:</strong>the full video on ViVi's official YouTube channel"),
        ("As of October 3, 2026, ", "As of October 10, 2026, "),
        (re.compile(r"<p>What's intriguing is that ViVi's caption teases.*?</p>", re.S),
         "<p>The teaser in ViVi's caption, " + mk("\"another announcement next week, 10/9 (Fri) at 12:00...!\"") + ", turned out to be the release of the full video on ViVi's official YouTube channel.<br>\n"
         "The \"Coming Soon...\" scene at the end of the Instagram video is part of it.<br>\n"
         "We cover what the project was about in the next section.</p>"),
        ("ViVi has another announcement scheduled for October 9 (Fri) at 12:00 JST",
         "ViVi released the full video on YouTube on October 9 (Fri) at 12:00 JST, and Team Green won the catchphrase battle<br>"
         + ui.check("RYOGA's \"I will rule this organization\" is an homage to Suguru Geto of Jujutsu Kaisen (stated in ViVi's caption)")),
    ],
}
SUMMARY_H2 = {"ja": "まとめ", "ko": "정리", "en": "Summary"}


def apply(lang, raw, med):
    for old, new in EDITS[lang]:
        if isinstance(old, re.Pattern):
            raw, n = old.subn(lambda _m: new, raw, count=1)
        else:
            n = raw.count(old)
            raw = raw.replace(old, new, 1)
        assert n == 1, (lang, str(old)[:60], n)
    anchor = f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{SUMMARY_H2[lang]}</h2>'
    assert raw.count(anchor) == 1, (lang, "summary anchor")
    raw = raw.replace(anchor, "\n\n".join(section(lang, med)) + "\n\n" + anchor)
    return raw


def upload(path):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HA, "Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{path.name}"'},
                      data=path.read_bytes())
    r.raise_for_status()
    return r.json()


DUMMY = {"source_url": "x", "media_details": {"width": 1280, "height": 720, "sizes": {}}}

if __name__ == "__main__":
    dry = "--dry" in sys.argv
    raws = {}
    for lang, pid in IDS.items():
        d = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=HA).json()
        if MARK in d["content"]["raw"]:
            print(lang, pid, "already appended, skip")
            continue
        raws[lang] = d["content"]["raw"]
    if not raws:
        sys.exit(0)
    med = {"ryoga": DUMMY, "twelve": DUMMY} if dry else {"ryoga": upload(IMG_RYOGA), "twelve": upload(IMG_12)}
    for lang, raw in raws.items():
        new = apply(lang, raw, med)
        assert "<hr" not in new
        plain = re.sub(r"<[^>]+>|<!--.*?-->", "", new, flags=re.S)
        print(lang, IDS[lang], "chars:", len(plain))
        if dry:
            (ROOT / f"tmp_prada_append_{lang}.html").write_text(new, encoding="utf-8")
            continue
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{IDS[lang]}", headers={**HA, "Content-Type": "application/json"},
                          data=json.dumps({"content": new}).encode("utf-8"))
        r.raise_for_status()
        print("  updated:", r.json()["status"], r.json()["link"])
