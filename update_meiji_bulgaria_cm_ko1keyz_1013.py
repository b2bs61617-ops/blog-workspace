# -*- coding: utf-8 -*-
"""明治ブルガリアCM=KO1KEYZ説の記事(公開済み JP14529/KR14531/EN14532)を10/13の正式発表で確定版にリライトする。
続報: 10/13(火) 新WEB CM「明治ブルガリアヨーグルトONE SHOT『ワンシャウト』KO1KEYZ(コイキーズ)篇」公開
      YouTube https://youtu.be/X_Dzq6sIgkQ (株式会社 明治・71秒、楽曲 KO1KEYZ「KO1KEYZ」)
      プレスリリース https://kyodonewsprwire.jp/release/202610097601
      (CMの商品=「明治ブルガリアのむヨーグルト ピーチ風味LB81」ONE SHOT・120g・149円税込・10/20全国新発売、
       Xキャンペーン「全部腸内細菌のせいにして叫べ ワンシャウト！キャンペーン」10/13 12:10〜10/30 23:59、QUOカード5,000円分×100名)
訂正: 公開前は商品を既存のLB81 ONE SHOTと予想していたが、実際のCM商品は新発売のピーチ風味。
CM内のメンバー個人は名前テロップがないので、叫んだセリフは登場順だけで並べ、誰が言ったかは書かない。
公開済みなので title/slug は送らず、status は publish のまま content だけ更新する。
"""
import json, sys
from pathlib import Path

import requests

sys.dont_write_bytecode = True
from update_meiji_bulgaria_cm_ko1keyz_1011 import (  # noqa: E402
    WP_URL, H, tweet, minibox, table, h2, p, mark, row, li, AB, TH,
)
from update_meiji_bulgaria_cm_ko1keyz_1012 import TW_TEASER, CHECK  # noqa: E402

YT = "https://youtu.be/X_Dzq6sIgkQ"
PR_PEACH = "https://kyodonewsprwire.jp/release/202610097601"


def youtube(url):
    return f"""<!-- wp:embed {{"url": "{url}", "type": "video", "providerNameSlug": "youtube", "responsive": true, "className": "wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->
<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">
{url}
</div></figure>
<!-- /wp:embed -->"""


def infobox(title, rows):
    trs = "\n".join(f'<tr><td style="background:{TH};border:1px solid {AB};padding:8px 12px;width:28%;">{k}</td>'
                    f'<td style="border:1px solid {AB};padding:8px 12px;">{v}</td></tr>' for k, v in rows)
    return f"""<!-- wp:html -->
<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>
<table style="border-collapse:collapse;width:100%;">
{trs}
</table>
</div>
<!-- /wp:html -->"""


def note(t):
    return f'<!-- wp:html -->\n<p style="font-size:0.85em;color:#777;margin:0 0 16px 0;">{t}</p>\n<!-- /wp:html -->'


def old_row(k, v):  # 基本情報の表の既存行(width:32%)
    return row(k, v)


def old_row28(k, v):  # 商品の表の既存行(width:28%)
    return (f'<tr><td style="background:{TH};border:1px solid {AB};padding:8px 12px;width:28%;">{k}</td>'
            f'<td style="border:1px solid {AB};padding:8px 12px;">{v}</td></tr>')


# ============================== JP ==============================
JP_SHOUTS = [
    "緑が好きすぎて、10年後の自分がどうなってるかわからなーいっ！",
    "続けるのは得意なのに、休むタイミングが分からない〜！",
    "練習をバチバチストイックにやりすぎて、みんなにひかれている〜！",
    "疲れてるとき、朝アラームに気づかないーっ！",
    "人間観察をしていたら、目が合って気まずいーっ！",
    "どこでも靴下脱いじゃうー！！",
    "すごく気合いを入れないと、連絡がすぐ返せないーっ！",
    "洗濯物が、全然乾かなーいっ！！",
    "ウィンクしようと思ったら、両目つむっちゃうーっ！",
    "アニメを1話だけみるつもりが、どんどん観ちゃうーっ！",
    "いつも新しいお菓子を探しちゃうーっ！",
    "自分で言ったことを、つい自分で笑っちゃうーっ！",
]

JP_CM = "\n\n".join([
    h2("10月13日公開のCM本編は？「ワンシャウト」KO1KEYZ篇"),
    minibox([("公開：", "2026年10月13日(火)、明治のYouTube公式チャンネルなど"),
             ("長さ・楽曲：", "約1分11秒、KO1KEYZのデビュー曲「KO1KEYZ」")]),
    p("予告どおり2026年10月13日、新WEB CM「明治ブルガリアヨーグルトONE SHOT『ワンシャウト』KO1KEYZ(コイキーズ)篇」が公開されました。<br>\n"
      f"明治のプレスリリースにも出演はKO1KEYZと書かれていて、メモの絵文字から予想していたとおり、{mark('「とあるグループ」はKO1KEYZ', True)}で確定です。"),
    youtube(YT),
    p("動画の説明文には「#KO1KEYZ が腸内細菌のせいにしたいモヤモヤを叫びまくる」とあり、BGMにはデビュー曲の「KO1KEYZ」が使われています。<br>\n"
      "衣装は予告動画と同じ白・水色・デニムの青系で、鍵穴の形をした白い板の前に1人ずつ登場し、ONE SHOTを手にモヤモヤを叫んでいきます。"),
    p("CMの流れは次のとおりです。"),
    table(["時間", "映っているもの"], [
        ("0〜5秒ごろ", "1人のアップから、12人そろってONE SHOTを掲げる集合カットへ"),
        ("6〜53秒ごろ", "鍵穴の前で、1人ずつ自分のモヤモヤを叫ぶ(12人分)"),
        ("54〜61秒ごろ", "「スッキリしないモヤモヤ 腸内細菌のせいかもしれません。」の文字と、みんなで乾杯"),
        ("62〜65秒ごろ", "12人そろって「モヤモヤかかって来い！」"),
        ("66〜71秒", "ONE SHOT 3本の商品カット。ピンクのボトルに「10/20発売」"),
    ]),
    p("12人が叫んだモヤモヤを、登場した順に並べると次のとおりです(画面の手書きの文字より)。"),
    table(["順番", "叫んだモヤモヤ"], [(f"{i}人目", s) for i, s in enumerate(JP_SHOUTS, 1)]),
    p(f"打ち合わせメモにあった{mark('「全部腸内細菌のせいにして叫べ」')}が、そのままCMになった形です。<br>\n"
      "「どこでも靴下脱いじゃう」「ウィンクしようと思ったら両目つむっちゃう」など、思わずクスッとする日常のモヤモヤが並んでいます。<br>\n"
      "画面にはメンバーの名前が出ないので、誰がどのモヤモヤを叫んでいるのか、CMを見ながら探してみるのも楽しそうです。"),
])

JP_CAMPAIGN = "\n\n".join([
    h2("ワンシャウト！キャンペーンの参加方法は？"),
    minibox([("応募期間：", "2026年10月13日(火)12:10〜10月30日(金)23:59"),
             ("賞品：", "オリジナルQUOカード5,000円分(抽選で100名)")]),
    p("CMの公開と同じ10月13日から、明治ブルガリアヨーグルトの公式Xで「全部腸内細菌のせいにして叫べ ワンシャウト！キャンペーン」が始まりました。<br>\n"
      "メモのセリフやスケジュールの「叫んでもらう」から予想していた、ファンが自分のモヤモヤを叫ぶ企画です。"),
    table(["項目", "内容"], [
        ("応募期間", "2026年10月13日(火)12:10〜10月30日(金)23:59"),
        ("参加方法", "①明治ブルガリアヨーグルト公式X(@meiji_BY_cp)をフォロー<br>②キャンペーンの画像をタップ<br>③「#全部腸内細菌のせいにして叫べ」と「@meiji_BY_cp」を付けて、自分のモヤモヤをポスト"),
        ("賞品", "オリジナルQUOカード5,000円分"),
        ("当選数", "抽選で100名"),
        ("注意", "公開アカウントのみ対象(鍵アカウントは対象外)"),
    ]),
    p(f"CMでKO1KEYZの12人がモヤモヤを叫んだように、今度は{mark('ファンが自分のモヤモヤを叫ぶ番', True)}です。<br>\n"
      "応募の細かい条件は、明治ブルガリアヨーグルトの公式Xのキャンペーン投稿で確認してください。"),
])

JP_PEACH_BOX = infobox("明治ブルガリアのむヨーグルト ピーチ風味LB81(ONE SHOT)の基本情報", [
    ("容量", "120g(1回で飲みきれるサイズ)"),
    ("値段", "希望小売価格149円(税込)"),
    ("発売日", "2026年10月20日(火)、全国で新発売"),
    ("種類", "特定保健用食品(トクホ)。ピーチ風味は無果汁"),
    ("トクホの表示", "LB81乳酸菌の働きにより、腸内細菌のバランスを整えて、おなかの調子を良好に保ちます"),
])

JP_ROW_CM = old_row("CM公開日", "2026年10月13日(火)")
JP_REPLACES = [
    # 導入
    ("さらに10月12日には、鍵穴の先に12人の後ろ姿が映る予告動画が出て、新WEB CMは10月13日に公開されることが決まりました。<br>\n"
     "この記事では、明治の投稿の中身と、KO1KEYZだと考えられる理由、CMに出てきそうな商品をまとめます。",
     "10月12日には鍵穴の先に12人の後ろ姿が映る予告動画が出て、10月13日、ついに<strong>新WEB CM「ワンシャウト」KO1KEYZ(コイキーズ)篇</strong>が公開されました。<br>\n"
     "明治の発表で、出演はKO1KEYZだと正式に決まっています。<br>\n"
     "この記事では、明治の投稿の流れと、公開前にKO1KEYZだと考えられた理由、CM本編の中身、CMの商品とキャンペーンをまとめます。"),
    # 基本情報の表
    ("明治ブルガリアヨーグルトの「とあるグループ」投稿の基本情報", "明治ブルガリアヨーグルトの新WEB CMの基本情報"),
    (JP_ROW_CM, old_row("CM公開日", "2026年10月13日(火)、「ワンシャウト」KO1KEYZ(コイキーズ)篇")),
    ("未発表(KO1KEYZとみられる・予告動画は12人の後ろ姿)", "KO1KEYZ(2026年10月13日に正式発表)"),
    (old_row("関係しそうな商品", "明治ブルガリアのむヨーグルトLB81(ONE SHOT)"),
     old_row("CMの商品", "明治ブルガリアのむヨーグルト ピーチ風味LB81(ONE SHOT・2026年10月20日発売)")),
    # わかること
    ("<li>CMに出てきそうな商品と値段</li>",
     li("10月13日公開のCM本編「ワンシャウト」の中身") + "\n" + li("CMの商品(ピーチ風味)と値段")),
    ("<li>ハッシュタグの意味</li>", li("ハッシュタグの意味とキャンペーンの参加方法")),
    # 注記
    ("※2026年10月12日時点で、明治・KO1KEYZのどちらからも出演グループの正式な発表は出ていません(新WEB CMは10月13日公開予定)。この記事の内容は、公開された投稿をもとにした予想です。",
     "※2026年10月13日、明治の発表で出演グループがKO1KEYZだと正式に決まりました。10月12日までの投稿を紹介している部分は、CM公開前に投稿をもとに予想した内容をそのまま残しています。"),
    # スケジュール節
    ("メンバーが叫ぶ動画やCMの公開</td>", "メンバーが叫ぶ動画やCMの公開(→実際にKO1KEYZが叫ぶCM本編が公開)</td>"),
    ("この日に「とあるグループ」の正体が明かされる流れと考えるのが自然です。<br>",
     "この日に「とあるグループ」の正体が明かされる流れと考えるのが自然です(実際は12日が予告動画で、正体がわかったのは13日のCM公開でした)。<br>"),
    ("メンバーが実際に叫ぶ動画やCM本編が公開される日だとみられます。<br>",
     "メンバーが実際に叫ぶ動画やCM本編が公開される日だとみられていて、実際にこの日、12人が叫ぶCM本編が公開されました。<br>"),
    ("ファンから「叫んでほしいこと」を募る企画になる可能性もありそうです。<br>",
     "ファンから「叫んでほしいこと」を募る企画になる可能性もありそうです(→実際にファンが自分のモヤモヤをポストするキャンペーンが始まりました)。<br>"),
    # 10/12節の締め
    ("ただし、この動画でもグループ名やメンバーの名前は出ておらず、正式な発表はまだです。<br>\n"
     "新WEB CMは<strong><span class=\"swl-marker mark_yellow\">10月13日(火)に公開</span></strong>されることが決まったので、その日にグループの正体がはっきりしそうです。<br>\n"
     "スケジュールの付箋にあった「叫んでもらう」も13日の予定だったので、CM本編でメンバーが叫ぶ姿が見られるかもしれません。",
     "この動画の時点では、グループ名やメンバーの名前は出ていませんでした。<br>\n"
     f"そして予告どおり{mark('10月13日(火)に新WEB CMが公開')}され、グループの正体はKO1KEYZだと明らかになりました。<br>\n"
     "スケジュールの付箋にあった「叫んでもらう」のとおり、CM本編は12人が1人ずつ叫ぶ内容です(次の見出しでくわしく紹介します)。"),
    # 商品節(訂正)
    ("<h2 class=\"wp-block-heading\">CMの商品は？明治ブルガリアのむヨーグルトLB81 ONE SHOT</h2>",
     "<h2 class=\"wp-block-heading\">CMの商品は？10月20日発売のピーチ風味LB81(ONE SHOT)</h2>"),
    ("<p style=\"margin:0;\"><strong>商品：</strong>明治ブルガリアのむヨーグルトLB81(ONE SHOT・120g)</p>\n"
     "<p style=\"margin:4px 0 0 0;\"><strong>値段：</strong>希望小売価格149円(税込)</p>",
     "<p style=\"margin:0;\"><strong>商品：</strong>明治ブルガリアのむヨーグルト ピーチ風味LB81(ONE SHOT・120g)</p>\n"
     "<p style=\"margin:4px 0 0 0;\"><strong>発売・値段：</strong>2026年10月20日(火)全国発売、希望小売価格149円(税込)</p>"),
    ("ここから、新しいWEB CMの商品は<strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">「明治ブルガリアのむヨーグルトLB81」の飲みきりサイズ「ONE SHOT」</span></strong>だとみられます。</p>\n<!-- /wp:paragraph -->",
     "CM公開前は、ここから商品を「明治ブルガリアのむヨーグルトLB81」の飲みきりサイズ「ONE SHOT」と予想していました。<br>\n"
     f"実際のCMもONE SHOTのCMでしたが、明治の発表によると、{mark('メインの商品は2026年10月20日に新発売される「ピーチ風味」', True)}でした。<br>\n"
     "CMの最後の商品カットでも、3本並んだONE SHOTのうち、ピンクのピーチ風味のボトルにだけ「10/20発売」と書かれています。</p>\n<!-- /wp:paragraph -->\n\n"
     + note("※CM公開前の予想(既存のLB81 ONE SHOT)から、CMの商品の情報を訂正しました。") + "\n\n" + JP_PEACH_BOX),
    ("明治ブルガリアのむヨーグルトLB81(ONE SHOT)の基本情報</p>", "参考：ONE SHOTシリーズ(既存の味)の基本情報</p>"),
    ("プレーン、ブルーベリー風味、ストロベリー風味(風味は無果汁)",
     "プレーン、ブルーベリー風味、ストロベリー風味(風味は無果汁)。2026年10月20日にピーチ風味が加わる"),
    ("<p>商品の情報は、<a href=\"https://www.meiji.co.jp/corporate/pressrelease/2026/03_28/\" target=\"_blank\" rel=\"noopener\">明治の公式プレスリリース</a>で確認できます。<br>",
     f"<p>既存の味は<a href=\"https://www.meiji.co.jp/corporate/pressrelease/2026/03_28/\" target=\"_blank\" rel=\"noopener\">明治の公式プレスリリース(2026年3月)</a>、ピーチ風味は<a href=\"{PR_PEACH}\" target=\"_blank\" rel=\"noopener\">2026年10月13日のプレスリリース</a>で確認できます。<br>"),
    ("CMが公開されたら、メンバーが飲んでいたのと同じ味を選んでみるのも楽しそうです。",
     "ピーチ風味の発売は10月20日なので、CMを見たあとにコンビニでピンクのボトルを探してみるのも楽しそうです。"),
    # ハッシュタグ節
    ("10月12日の投稿で「いよいよ明日公開」と発表されたので、12人がそれぞれのモヤモヤを叫ぶようなCMになるのか、13日の公開が楽しみです。",
     "そして10月13日に公開されたCMは、予想どおり12人がそれぞれのモヤモヤを叫ぶ内容で、ファン参加のキャンペーンも同じ日に始まりました。"),
    # タイアップ節
    ("明治ブルガリアヨーグルトのWEB CMが正式に決まれば、食品メーカーとの大きなタイアップとして、新しいファン層にグループを知ってもらうきっかけにもなりそうです。",
     "明治ブルガリアヨーグルトのWEB CMは、デビュー直後に決まった食品メーカーとの大きなタイアップで、新しいファン層にグループを知ってもらうきっかけにもなりそうです。"),
    # まとめ
    ("商品は明治ブルガリアのむヨーグルトLB81(ONE SHOT・120g、希望小売価格149円)とみられる<br>",
     "CMの商品は10月20日発売の「ピーチ風味LB81」(ONE SHOT・120g、希望小売価格149円)<br>"),
    ("新WEB CMは10月13日(火)公開。10月12日時点でグループ名の正式な発表はまだ",
     "10月13日に新WEB CM「ワンシャウト」KO1KEYZ(コイキーズ)篇が公開され、出演はKO1KEYZで確定<br>\n"
     + CHECK + "12人が1人ずつモヤモヤを叫ぶ約1分のCMで、楽曲はデビュー曲「KO1KEYZ」<br>\n"
     + CHECK + "Xの「ワンシャウト！キャンペーン」は10月30日まで、QUOカード5,000円分が100名に当たる"),
    ("絵文字・並び順・鍵のヒントがここまでそろうと、KO1KEYZの可能性はかなり高いのではないでしょうか。<br>\n"
     "10月13日の「Unlock」＝CM公開を楽しみに待ちながら、ひと足先にONE SHOTを飲んで「腸活」を始めておくのもよさそうですね！",
     "絵文字・並び順・鍵のヒントのとおり、「とあるグループ」はKO1KEYZでした。<br>\n"
     "キャンペーンで自分のモヤモヤを叫んだあとは、10月20日発売のピーチ風味で「腸活」を始めてみるのもよさそうですね！"),
]
JP_CM_ANCHOR = "<h2 class=\"wp-block-heading\">CMの商品は？10月20日発売のピーチ風味LB81(ONE SHOT)</h2>"
JP_CAMPAIGN_ANCHOR = "<h2 class=\"wp-block-heading\">KO1KEYZのデビュー後の広告・タイアップは？</h2>"

# ============================== KR ==============================
KR_SHOUTS = [
    "초록색을 너무 좋아해서, 10년 후의 내가 어떻게 될지 모르겠다~!",
    "계속하는 건 자신 있는데, 쉬는 타이밍을 모르겠다~!",
    "연습을 너무 빡세게 스토익하게 해서, 다들 질려 한다~!",
    "피곤할 때 아침 알람을 못 듣는다~!",
    "사람 구경을 하다가 눈이 마주쳐서 어색하다~!",
    "어디서든 양말을 벗어 버린다~!!",
    "단단히 마음먹지 않으면 연락에 바로 답장을 못 한다~!",
    "빨래가 전혀 안 마른다~!!",
    "윙크하려고 했는데 두 눈을 다 감아 버린다~!",
    "애니메이션 1화만 보려고 했는데 계속 보게 된다~!",
    "늘 새로운 과자를 찾게 된다~!",
    "내가 한 말에 나도 모르게 웃어 버린다~!",
]
KR_CM = "\n\n".join([
    h2("10월 13일 공개된 CM 본편은? '원샤우트' KO1KEYZ 편"),
    minibox([("공개: ", "2026년 10월 13일(화), 메이지 공식 YouTube 채널 등"),
             ("길이・곡: ", "약 1분 11초, KO1KEYZ 데뷔곡 'KO1KEYZ'")]),
    p("예고대로 2026년 10월 13일, 새 WEB CM '메이지 불가리아 요구르트 ONE SHOT 「원샤우트(ワンシャウト)」 KO1KEYZ(코이키즈) 편'이 공개되었습니다.<br>\n"
      f"메이지 보도자료에도 출연은 KO1KEYZ로 적혀 있어, 메모의 이모지로 예상했던 대로 {mark("'어느 그룹'은 KO1KEYZ", True)}로 확정입니다."),
    youtube(YT),
    p("영상 설명란에는 '#KO1KEYZ 가 장내 세균 탓으로 하고 싶은 답답함을 마구 외친다'라고 적혀 있고, BGM은 데뷔곡 'KO1KEYZ'입니다.<br>\n"
      "의상은 예고 영상과 같은 흰색・하늘색・데님의 파란 계열이며, 열쇠 구멍 모양의 하얀 판 앞에 한 명씩 등장해 ONE SHOT을 들고 답답함을 외칩니다."),
    table(["시간", "영상 내용"], [
        ("0~5초쯤", "한 명의 클로즈업에서 12명이 ONE SHOT을 든 단체 컷으로"),
        ("6~53초쯤", "열쇠 구멍 앞에서 한 명씩 자신의 답답함을 외친다(12명)"),
        ("54~61초쯤", "'개운하지 않은 답답함, 장내 세균 탓일지도 모릅니다.' 자막과 다 함께 건배"),
        ("62~65초쯤", "12명이 함께 '답답함아 덤벼라!(モヤモヤかかって来い！)'"),
        ("66~71초", "ONE SHOT 3병 상품 컷. 분홍색 병에 '10/20 발매'"),
    ]),
    p("12명이 외친 답답함을 등장 순서대로 정리하면 다음과 같습니다(화면의 손글씨 자막을 번역)."),
    table(["순서", "외친 답답함"], [(f"{i}번째", s) for i, s in enumerate(KR_SHOUTS, 1)]),
    p(f"회의 메모에 있던 {mark("'전부 장내 세균 탓으로 하고 외쳐라'")}가 그대로 CM이 된 셈입니다.<br>\n"
      "'어디서든 양말을 벗어 버린다', '윙크하려다 두 눈을 다 감아 버린다' 등 피식 웃게 되는 일상의 답답함이 이어집니다.<br>\n"
      "화면에 멤버 이름은 나오지 않으니, 누가 어떤 답답함을 외치는지 CM을 보며 찾아보는 것도 재미있겠네요."),
])
KR_CAMPAIGN = "\n\n".join([
    h2("원샤우트! 캠페인 참여 방법은?"),
    minibox([("응모 기간: ", "2026년 10월 13일(화) 12:10~10월 30일(금) 23:59(일본 시간)"),
             ("상품: ", "오리지널 QUO카드 5,000엔분(추첨 100명)")]),
    p("CM 공개와 같은 10월 13일부터 메이지 불가리아 요구르트 공식 X에서 '전부 장내 세균 탓으로 하고 외쳐라 원샤우트! 캠페인'이 시작되었습니다.<br>\n"
      "메모의 대사와 스케줄의 '외치게 한다'에서 예상했던, 팬이 자신의 답답함을 외치는 기획입니다."),
    table(["항목", "내용"], [
        ("응모 기간", "2026년 10월 13일(화) 12:10~10월 30일(금) 23:59(일본 시간)"),
        ("참여 방법", "① 메이지 불가리아 요구르트 공식 X(@meiji_BY_cp) 팔로우<br>② 캠페인 이미지 탭<br>③ '#全部腸内細菌のせいにして叫べ'와 '@meiji_BY_cp'를 붙여 자신의 답답함을 포스트"),
        ("상품", "오리지널 QUO카드 5,000엔분"),
        ("당첨 수", "추첨 100명"),
        ("주의", "공개 계정만 대상(비공개 계정 제외)"),
    ]),
    p("QUO카드는 일본에서 쓰는 선불카드이므로, 자세한 응모 조건은 메이지 불가리아 요구르트 공식 X의 캠페인 게시물에서 꼭 확인해 주세요."),
])
KR_PEACH_BOX = infobox("메이지 불가리아 마시는 요구르트 피치 풍미 LB81(ONE SHOT) 기본 정보", [
    ("용량", "120g(한 번에 마시기 좋은 사이즈)"),
    ("가격", "희망 소매가 149엔(세금 포함)"),
    ("발매일", "2026년 10월 20일(화), 일본 전국 신발매"),
    ("종류", "특정보건용식품(토쿠호). 피치 풍미는 무과즙"),
])
KR_REPLACES = [
    ("이어서 10월 12일에는 열쇠 구멍 너머 12명의 뒷모습이 나오는 예고 영상이 공개되었고, 새 WEB CM은 10월 13일에 공개되는 것으로 정해졌습니다.<br>\n"
     "이 글에서는 메이지의 게시물 내용과 KO1KEYZ로 보이는 이유, CM에 나올 것 같은 상품을 정리합니다.",
     "10월 12일에는 열쇠 구멍 너머 12명의 뒷모습이 나오는 예고 영상이 나왔고, 10월 13일 드디어 <strong>새 WEB CM '원샤우트' KO1KEYZ(코이키즈) 편</strong>이 공개되었습니다.<br>\n"
     "메이지의 발표로 출연은 KO1KEYZ로 공식 확정되었습니다.<br>\n"
     "이 글에서는 메이지 게시물의 흐름과 공개 전 KO1KEYZ로 보였던 이유, CM 본편 내용, CM 상품과 캠페인을 정리합니다."),
    ("메이지 불가리아 요구르트 '어느 그룹' 게시물 기본 정보", "메이지 불가리아 요구르트 새 WEB CM 기본 정보"),
    (old_row("CM 공개일", "2026년 10월 13일(화)"), old_row("CM 공개일", "2026년 10월 13일(화), '원샤우트' KO1KEYZ(코이키즈) 편")),
    ("미발표(KO1KEYZ로 보임・예고 영상은 12명의 뒷모습)", "KO1KEYZ(2026년 10월 13일 공식 발표)"),
    (old_row("관련 상품", "메이지 불가리아 마시는 요구르트 LB81(ONE SHOT)"),
     old_row("CM 상품", "메이지 불가리아 마시는 요구르트 피치 풍미 LB81(ONE SHOT・2026년 10월 20일 발매)")),
    ("※2026년 10월 12일 기준, 메이지와 KO1KEYZ 모두 출연 그룹을 공식 발표하지 않았습니다(새 WEB CM은 10월 13일 공개 예정).",
     "※2026년 10월 13일, 메이지의 발표로 출연 그룹이 KO1KEYZ로 공식 확정되었습니다. 10월 12일까지의 게시물을 소개하는 부분은 CM 공개 전 예상을 그대로 남겨 두었습니다."),
    ("이날 '어느 그룹'의 정체가 밝혀질 가능성이 높아 보입니다.<br>",
     "이날 '어느 그룹'의 정체가 밝혀질 가능성이 높아 보입니다(실제로는 12일이 예고 영상이었고, 정체는 13일 CM 공개로 밝혀졌습니다).<br>"),
    ("멤버가 실제로 외치는 영상이나 CM 본편이 공개되는 날로 보입니다.<br>",
     "멤버가 실제로 외치는 영상이나 CM 본편이 공개되는 날로 보였고, 실제로 이날 12명이 외치는 CM 본편이 공개되었습니다.<br>"),
    ("다만 이 영상에서도 그룹명이나 멤버 이름은 나오지 않아, 공식 발표는 아직입니다.<br>\n"
     "새 WEB CM은 <strong><span class=\"swl-marker mark_yellow\">10월 13일(화)에 공개</span></strong>되는 것으로 정해졌기 때문에, 그날 그룹의 정체가 확실해질 것 같습니다.<br>\n"
     "스케줄 포스트잇의 '외치게 한다'도 13일 일정이었으니, CM 본편에서 멤버들이 외치는 모습을 볼 수 있을지도 모릅니다.",
     "이 영상 시점에는 그룹명이나 멤버 이름이 나오지 않았습니다.<br>\n"
     f"그리고 예고대로 {mark('10월 13일(화)에 새 WEB CM이 공개')}되어, 그룹의 정체는 KO1KEYZ로 밝혀졌습니다.<br>\n"
     "스케줄 포스트잇의 '외치게 한다'대로, CM 본편은 12명이 한 명씩 외치는 내용입니다(다음 제목에서 자세히 소개)."),
    ("<h2 class=\"wp-block-heading\">CM 상품은? 메이지 불가리아 마시는 요구르트 LB81 ONE SHOT</h2>",
     "<h2 class=\"wp-block-heading\">CM 상품은? 10월 20일 발매 피치 풍미 LB81(ONE SHOT)</h2>"),
    ("<p style=\"margin:0;\"><strong>상품: </strong>메이지 불가리아 마시는 요구르트 LB81(ONE SHOT・120g)</p>\n"
     "<p style=\"margin:4px 0 0 0;\"><strong>가격: </strong>희망 소매가 149엔(세금 포함)</p>",
     "<p style=\"margin:0;\"><strong>상품: </strong>메이지 불가리아 마시는 요구르트 피치 풍미 LB81(ONE SHOT・120g)</p>\n"
     "<p style=\"margin:4px 0 0 0;\"><strong>발매・가격: </strong>2026년 10월 20일(화) 일본 전국 발매, 희망 소매가 149엔(세금 포함)</p>"),
    ("CM 상품은 <strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">메이지 불가리아 마시는 요구르트 LB81의 ONE SHOT</span></strong>으로 보입니다.</p>\n<!-- /wp:paragraph -->",
     "CM 공개 전에는 상품을 메이지 불가리아 마시는 요구르트 LB81의 ONE SHOT으로 예상했습니다.<br>\n"
     f"실제 CM도 ONE SHOT CM이었지만, 메이지 발표에 따르면 {mark('메인 상품은 2026년 10월 20일 새로 발매되는 피치 풍미', True)}였습니다.<br>\n"
     "CM 마지막 상품 컷에서도 3병 중 분홍색 피치 풍미 병에만 '10/20 발매'라고 적혀 있습니다.</p>\n<!-- /wp:paragraph -->\n\n"
     + note("※CM 공개 전 예상(기존 LB81 ONE SHOT)에서 CM 상품 정보를 정정했습니다.") + "\n\n" + KR_PEACH_BOX),
    ("메이지 불가리아 마시는 요구르트 LB81(ONE SHOT) 기본 정보</p>", "참고: ONE SHOT 시리즈(기존 맛) 기본 정보</p>"),
    ("플레인, 블루베리 풍미, 딸기 풍미</td>", "플레인, 블루베리 풍미, 딸기 풍미. 2026년 10월 20일 피치 풍미 추가</td>"),
    ("CM 공개에 맞춰 팬들의 '외치고 싶은 것'을 모으는 기획이 있을 가능성도 있습니다.",
     "CM 공개에 맞춰 팬들의 '외치고 싶은 것'을 모으는 기획이 있을 가능성도 있다고 봤는데, 실제로 10월 13일 CM은 12명이 각자의 답답함을 외치는 내용이었고, 팬 참여 캠페인도 같은 날 시작되었습니다."),
    ("상품은 메이지 불가리아 마시는 요구르트 LB81(ONE SHOT・120g, 149엔)으로 보임<br>",
     "CM 상품은 10월 20일 발매 '피치 풍미 LB81'(ONE SHOT・120g, 149엔)<br>"),
    ("새 WEB CM은 10월 13일(화) 공개. 10월 12일 기준 그룹명 공식 발표는 아직",
     "10월 13일 새 WEB CM '원샤우트' KO1KEYZ(코이키즈) 편이 공개되어, 출연은 KO1KEYZ로 확정<br>\n"
     + CHECK + "12명이 한 명씩 답답함을 외치는 약 1분짜리 CM이며, 곡은 데뷔곡 'KO1KEYZ'<br>\n"
     + CHECK + "X '원샤우트! 캠페인'은 10월 30일까지, QUO카드 5,000엔분 100명 추첨"),
    ("이모지・순서・열쇠 힌트가 이렇게까지 갖춰졌다면 KO1KEYZ일 가능성이 꽤 높지 않을까요?<br>\n"
     "10월 13일 'Unlock' = CM 공개를 기대하며 기다려 보면 좋겠네요!",
     "이모지・순서・열쇠 힌트대로, '어느 그룹'은 KO1KEYZ였습니다.<br>\n"
     "CM을 보면서 누가 어떤 답답함을 외치는지 찾아보는 것도 즐거울 것 같네요!"),
]
KR_CM_ANCHOR = "<h2 class=\"wp-block-heading\">CM 상품은? 10월 20일 발매 피치 풍미 LB81(ONE SHOT)</h2>"
KR_CAMPAIGN_ANCHOR = "<h2 class=\"wp-block-heading\">정리</h2>"

# ============================== EN ==============================
EN_SHOUTS = [
    "I love green so much, I have no idea what I'll be like in 10 years!",
    "I'm great at keeping going, but I never know when to take a break!",
    "I practice so hard and so stoically that everyone's weirded out!",
    "When I'm tired, I sleep right through my morning alarm!",
    "I was people-watching and we locked eyes. So awkward!",
    "I take my socks off anywhere!!",
    "Unless I really psych myself up, I can't reply to messages right away!",
    "My laundry just won't dry!!",
    "I try to wink and end up closing both eyes!",
    "I mean to watch just one episode of an anime, then keep going!",
    "I'm always hunting for new snacks!",
    "I always end up laughing at what I just said!",
]
EN_CM = "\n\n".join([
    h2("The commercial released Oct 13: \"One Shout\" featuring KO1KEYZ"),
    minibox([("Released: ", "Oct 13, 2026 (Tue), on Meiji's official YouTube channel and more"),
             ("Length & song: ", "About 1 min 11 sec, set to KO1KEYZ's debut song \"KO1KEYZ\"")]),
    p("As teased, the new web commercial \"Meiji Bulgaria Yogurt ONE SHOT 'One Shout (ワンシャウト)' KO1KEYZ version\" came out on October 13, 2026.<br>\n"
      f"Meiji's press release also names KO1KEYZ, so just as the memo emojis suggested, {mark('the \"certain group\" is confirmed as KO1KEYZ', True)}."),
    youtube(YT),
    p("The video description says \"#KO1KEYZ shout out all the frustrations they want to blame on their gut bacteria,\" and the background music is their debut song \"KO1KEYZ.\"<br>\n"
      "Dressed in the same white, light-blue and denim outfits as the teaser, the members step up one at a time in front of a white keyhole-shaped board and shout, ONE SHOT in hand."),
    table(["Time", "What the video shows"], [
        ("About 0-5 sec", "From a close-up of one member to all 12 holding up ONE SHOT"),
        ("About 6-53 sec", "One by one, each member shouts a frustration in front of the keyhole (12 in all)"),
        ("About 54-61 sec", "On-screen text: \"That foggy feeling might be your gut bacteria.\" Everyone toasts"),
        ("About 62-65 sec", "All 12 together: \"Bring it on, frustrations!\" (モヤモヤかかって来い！)"),
        ("66-71 sec", "Product shot of three ONE SHOT bottles; the pink one is marked \"on sale 10/20\""),
    ]),
    p("Here are the 12 frustrations in order of appearance (translated from the handwritten on-screen text)."),
    table(["Order", "What they shout"], [(f"#{i}", s) for i, s in enumerate(EN_SHOUTS, 1)]),
    p(f"The memo's {mark('\"blame it all on your gut bacteria and shout\"')} became the commercial itself.<br>\n"
      "Lines like \"I take my socks off anywhere\" and \"I try to wink and end up closing both eyes\" are everyday frustrations that are hard not to smile at.<br>\n"
      "No names appear on screen, so it's fun to watch and guess which member shouts which line."),
])
EN_CAMPAIGN = "\n\n".join([
    h2("How to join the \"One Shout!\" campaign"),
    minibox([("Entry period: ", "Oct 13, 2026 (Tue) 12:10 - Oct 30 (Fri) 23:59 JST"),
             ("Prize: ", "Original QUO Card worth 5,000 yen (100 winners by lottery)")]),
    p("Starting the same day as the commercial, Meiji Bulgaria Yogurt's official X account launched the \"Blame it all on your gut bacteria and shout: One Shout! campaign.\"<br>\n"
      "It's the fan participation campaign the memo lines and the \"we'll have them shout\" note hinted at."),
    table(["Item", "Details"], [
        ("Entry period", "Oct 13, 2026 (Tue) 12:10 - Oct 30 (Fri) 23:59 JST"),
        ("How to enter", "1. Follow @meiji_BY_cp on X<br>2. Tap the campaign image<br>3. Post your frustration with #全部腸内細菌のせいにして叫べ and @meiji_BY_cp"),
        ("Prize", "Original QUO Card worth 5,000 yen"),
        ("Winners", "100, by lottery"),
        ("Note", "Public accounts only (private accounts are not eligible)"),
    ]),
    p("QUO Cards are prepaid cards used in Japan, so check the full terms in the campaign post on Meiji Bulgaria Yogurt's official X account before entering."),
])
EN_PEACH_BOX = infobox("Meiji Bulgaria Drinking Yogurt Peach Flavor LB81 (ONE SHOT)", [
    ("Size", "120g single-serve bottle"),
    ("Price", "Suggested retail price 149 yen (tax incl.)"),
    ("Release", "Oct 20, 2026 (Tue), nationwide in Japan"),
    ("Type", "FOSHU (Food for Specified Health Uses); peach flavor contains no fruit juice"),
])
EN_REPLACES = [
    ("On October 12, a teaser showed 12 people seen from behind through a keyhole, and the new web commercial was set for October 13.<br>\n"
     "This article covers what Meiji posted, why it looks like KO1KEYZ, and the product likely featured in the commercial.",
     "On October 12, a teaser showed 12 people seen from behind through a keyhole, and on October 13 the <strong>new web commercial \"One Shout\" featuring KO1KEYZ</strong> finally came out.<br>\n"
     "Meiji has officially confirmed that the group is KO1KEYZ.<br>\n"
     "This article covers how Meiji's posts unfolded, why it looked like KO1KEYZ before the release, what's in the commercial, the product and the fan campaign."),
    ("Meiji Bulgaria Yogurt's \"certain group\" posts at a glance", "Meiji Bulgaria Yogurt's new web CM at a glance"),
    (old_row("CM release", "Oct 13, 2026 (Tue)"), old_row("CM release", "Oct 13, 2026 (Tue): \"One Shout\" KO1KEYZ version")),
    ("Not announced (appears to be KO1KEYZ; the teaser shows 12 people from behind)", "KO1KEYZ (officially announced Oct 13, 2026)"),
    (old_row("Likely product", "Meiji Bulgaria Drinking Yogurt LB81 (ONE SHOT)"),
     old_row("Product", "Meiji Bulgaria Drinking Yogurt Peach Flavor LB81 (ONE SHOT, on sale Oct 20, 2026)")),
    ("* As of Oct 12, 2026, neither Meiji nor KO1KEYZ has officially named the group (the new web CM is due out Oct 13). This article is a prediction based on the public posts.",
     "* On Oct 13, 2026, Meiji officially confirmed the group as KO1KEYZ. The parts covering the posts up to Oct 12 keep the predictions made before the commercial came out."),
    ("October 12 looks like the day the \"certain group\" is revealed, a perfect fit for a group with \"KEY\" in its name.",
     "October 12 looks like the day the \"certain group\" is revealed, a perfect fit for a group with \"KEY\" in its name (in the end, Oct 12 brought a teaser, and the group was revealed with the commercial on Oct 13)."),
    ("so that day will likely bring a video or the commercial itself with the members shouting.<br>",
     "so that day looked likely to bring the commercial with the members shouting, and it did: the commercial of all 12 shouting came out that day.<br>"),
    ("<p>Still, the video shows no group or member names, so there is no official announcement yet.<br>\n"
     "The new web commercial is set to <strong><span class=\"swl-marker mark_yellow\">come out on October 13 (Tue)</span></strong>, which is likely when the group will be confirmed.<br>\n"
     "The \"we'll have them shout\" note on the schedule was also for the 13th, so the commercial may show the members shouting.",
     "<p>At that point, the video showed no group or member names.<br>\n"
     f"Then, as teased, {mark('the new web commercial came out on October 13 (Tue)')}, revealing the group as KO1KEYZ.<br>\n"
     "True to the \"we'll have them shout\" note, the commercial has all 12 members shouting one by one (details in the next section)."),
    ("<h2 class=\"wp-block-heading\">The product: Meiji Bulgaria Drinking Yogurt LB81 ONE SHOT</h2>",
     "<h2 class=\"wp-block-heading\">The product: the new Peach Flavor LB81 (ONE SHOT), out Oct 20</h2>"),
    ("<p style=\"margin:0;\"><strong>Product: </strong>Meiji Bulgaria Drinking Yogurt LB81 (ONE SHOT, 120g)</p>\n"
     "<p style=\"margin:4px 0 0 0;\"><strong>Price: </strong>Suggested retail price 149 yen (tax incl.)</p>",
     "<p style=\"margin:0;\"><strong>Product: </strong>Meiji Bulgaria Drinking Yogurt Peach Flavor LB81 (ONE SHOT, 120g)</p>\n"
     "<p style=\"margin:4px 0 0 0;\"><strong>Release & price: </strong>Oct 20, 2026 (Tue) nationwide in Japan, suggested retail price 149 yen (tax incl.)</p>"),
    ("so the commercial is likely for <strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">Meiji Bulgaria Drinking Yogurt LB81 ONE SHOT</span></strong>.</p>\n<!-- /wp:paragraph -->",
     "so before the release we predicted the commercial would be for Meiji Bulgaria Drinking Yogurt LB81 ONE SHOT.<br>\n"
     f"It is a ONE SHOT commercial, but according to Meiji, {mark('the featured product is the new peach flavor, out October 20, 2026', True)}.<br>\n"
     "In the closing product shot, only the pink peach bottle among the three ONE SHOT bottles is marked \"on sale 10/20.\"</p>\n<!-- /wp:paragraph -->\n\n"
     + note("* We corrected the product information from our pre-release prediction (the existing LB81 ONE SHOT).") + "\n\n" + EN_PEACH_BOX),
    ("Meiji Bulgaria Drinking Yogurt LB81 (ONE SHOT)</p>\n<table", "For reference: the ONE SHOT line (existing flavors)</p>\n<table"),
    ("Plain, blueberry flavor, strawberry flavor</td>", "Plain, blueberry flavor, strawberry flavor; peach flavor added Oct 20, 2026</td>"),
    ("so a fan campaign collecting things to shout may be planned alongside the commercial.",
     "so we guessed a fan campaign collecting things to shout might come with the commercial. The Oct 13 commercial did show all 12 shouting their frustrations, and a fan campaign started the same day."),
    ("The product is likely Meiji Bulgaria Drinking Yogurt LB81 ONE SHOT (120g, 149 yen)<br>",
     "The commercial's product is the new Peach Flavor LB81 ONE SHOT (120g, 149 yen), out Oct 20<br>"),
    ("The new web CM comes out Oct 13 (Tue); no official group announcement as of Oct 12",
     "On Oct 13, the new web CM \"One Shout\" featuring KO1KEYZ came out, confirming the group as KO1KEYZ<br>\n"
     + CHECK + "The roughly one-minute commercial has the 12 members shouting one by one, set to their debut song \"KO1KEYZ\"<br>\n"
     + CHECK + "The \"One Shout!\" campaign on X runs until Oct 30, with 5,000-yen QUO Cards for 100 winners"),
    ("With the emojis, order and key hints all lining up, KO1KEYZ looks very likely.<br>\n"
     "Let's look forward to the \"Unlock\" on October 13, when the commercial comes out!",
     "Just as the emojis, order and key hints suggested, the \"certain group\" was KO1KEYZ.<br>\n"
     "Watch the commercial and try guessing which member shouts which frustration!"),
]
EN_CM_ANCHOR = "<h2 class=\"wp-block-heading\">The product: the new Peach Flavor LB81 (ONE SHOT), out Oct 20</h2>"
EN_CAMPAIGN_ANCHOR = "<h2 class=\"wp-block-heading\">Summary</h2>"


def insert_before(raw, anchor, section):
    block = "<!-- wp:heading -->\n" + anchor
    assert raw.count(block) == 1, f"anchor missing: {anchor}"
    return raw.replace(block, section + "\n\n" + block)


def apply(raw, cm, campaign, replaces, cm_anchor, campaign_anchor):
    assert YT not in raw, "already updated"
    assert TW_TEASER in raw, "10/12 update missing"
    for old, new in replaces:
        assert raw.count(old) == 1, f"not found exactly once ({raw.count(old)}): {old[:70]}"
        raw = raw.replace(old, new)
    raw = insert_before(raw, cm_anchor, cm)
    return insert_before(raw, campaign_anchor, campaign)


def main(dry):
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    for pid, cm, campaign, replaces, a1, a2 in [
        (14529, JP_CM, JP_CAMPAIGN, JP_REPLACES, JP_CM_ANCHOR, JP_CAMPAIGN_ANCHOR),
        (14531, KR_CM, KR_CAMPAIGN, KR_REPLACES, KR_CM_ANCHOR, KR_CAMPAIGN_ANCHOR),
        (14532, EN_CM, EN_CAMPAIGN, EN_REPLACES, EN_CM_ANCHOR, EN_CAMPAIGN_ANCHOR),
    ]:
        r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=H)
        r.raise_for_status()
        post = r.json()
        new = apply(post["content"]["raw"], cm, campaign, replaces, a1, a2)
        print(pid, post["status"], len(post["content"]["raw"]), "->", len(new))
        if out:
            (out / f"{pid}_new.html").write_text(new, encoding="utf-8")
        if dry:
            continue
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}",
                          headers={**H, "Content-Type": "application/json"},
                          data=json.dumps({"content": new, "status": post["status"]}).encode("utf-8"))
        r.raise_for_status()
        chk = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=H).json()
        assert YT in chk["content"]["raw"], f"{pid} not reflected"
        print(pid, "updated", chk["modified"], chk["status"])


if __name__ == "__main__":
    main(dry=(len(sys.argv) > 1 and sys.argv[1] == "--dry"))
