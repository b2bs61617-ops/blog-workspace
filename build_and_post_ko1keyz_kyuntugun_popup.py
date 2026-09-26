# -*- coding: utf-8 -*-
"""KO1KEYZ DEBUT SINGLE "KO1KEYZ" キュントゥグンPOP-UP(新宿サザンテラス 10/2〜10/8)の記事。
chomoand-1.com に JP/KR/EN の下書きを作る(本文画像4枚+アイキャッチ)。

一次ソース(すべて2026-09-26発表):
- KO1KEYZ公式X https://x.com/KO1KEYZofficial/status/2103650774198714687 (概要画像+ドリンク画像)
- 公式サイト https://ko1keyz.com/news/detail/125 (開催概要・ドリンク・会場写真イメージ)
- 公式サイト https://ko1keyz.com/news/detail/118 (CD予約販売・限定トレカ)

python build_and_post_ko1keyz_kyuntugun_popup.py [--dry]
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

IMG_OVERVIEW = ROOT / "images" / "ko1keyz_kyuntugun_popup_overview.jpg"
IMG_VENUE = ROOT / "images" / "ko1keyz_kyuntugun_popup_venue.jpg"
IMG_DRINK = ROOT / "images" / "ko1keyz_kyuntugun_popup_drink.jpg"
IMG_TRECA = ROOT / "images" / "ko1keyz_kyuntugun_popup_trecard.jpg"
EYE_JP = ROOT / "images" / "ko1keyz_kyuntugun_popup_eyecatch.png"
EYE_KR = ROOT / "images" / "ko1keyz_kyuntugun_popup_eyecatch_kr.png"
BASE_SLUG = "ko1keyz-kyuntugun-popup-shinjuku"

SRC_X = "https://x.com/KO1KEYZofficial/status/2103650774198714687"
NEWS = "https://ko1keyz.com/news/detail/125"
NEWS_CD = "https://ko1keyz.com/news/detail/118"
SRC_X_CD = "https://x.com/KO1KEYZofficial/status/2103651014050242712"
MAP = ('<iframe src="https://maps.google.com/maps?q=%E6%96%B0%E5%AE%BF%E3%82%B5%E3%82%B6%E3%83%B3%E3%83%86%E3%83%A9%E3%82%B9'
       '&t=&z=16&ie=UTF8&iwloc=&output=embed" width="100%" height="350" frameborder="0" scrolling="no" '
       'style="border:0;" loading="lazy"></iframe>')

L = lambda pid: f"https://chomoand-1.com/?p={pid}"
REL = {
    "ja": [(L(10866), "デビューシングル『KO1KEYZ』の発売日・収録曲・特典まとめ"),
           (L(11307), "KO1KEYZデビューシングル特典まとめ(SHOWCASE招待・ファンミ抽選会ほか)"),
           (L(13208), "デビュー曲「KO1KEYZ」の歌割り・12人のパートまとめ"),
           (L(13675), "同じ週に渋谷で開催！KO1KEYZ大型パネル展(HMV渋谷)")],
    "ko": [(L(10869), "데뷔 싱글 『KO1KEYZ』 발매일·수록곡·특전 정리"),
           (L(11312), "KO1KEYZ 데뷔 싱글 특전 총정리"),
           (L(13220), "타이틀곡 'KO1KEYZ' 파트 분배 12명 총정리"),
           (L(13676), "같은 주 시부야에서! KO1KEYZ 대형 패널전(HMV 시부야)")],
    "en": [(L(12606), "Debut single \"KO1KEYZ\": release date, tracks, and bonuses"),
           (L(12586), "KO1KEYZ debut single bonuses roundup"),
           (L(13221), "Who sings what in the title track \"KO1KEYZ\""),
           (L(13677), "Same week in Shibuya: the KO1KEYZ giant panel exhibition at HMV")],
}

ui = Ui("#8a8378", "#ddd9d3", "#f7f6f4", "rgba(138,131,120,0.06)")


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def upload(path, ctype):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HA, "Content-Type": ctype, "Content-Disposition": f'attachment; filename="{path.name}"'},
                      data=path.read_bytes())
    r.raise_for_status()
    m = r.json()
    s = m["media_details"]["sizes"]
    full = {"source_url": m["source_url"], "width": m["media_details"]["width"], "height": m["media_details"]["height"]}
    return {"id": m["id"], "full": full, "large": s.get("large", full), "medium": s.get("medium", full)}


def fig(img, alt, src, cap):
    Lg, M, F = img["large"], img["medium"], img["full"]
    return ('<!-- wp:image {"sizeSlug":"large","linkDestination":"none"} -->\n'
            f'<figure class="wp-block-image size-large"><img src="{Lg["source_url"]}" alt="{alt}" width="{Lg["width"]}" height="{Lg["height"]}" '
            f'style="max-width:100%;height:auto;" srcset="{M["source_url"]} {M["width"]}w, {Lg["source_url"]} {Lg["width"]}w, '
            f'{F["source_url"]} {F["width"]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
            f'<figcaption class="wp-element-caption" style="text-align:center;font-size:12px;">{cap}{src}</figcaption></figure>\n'
            '<!-- /wp:image -->')


def build(io, iv, idr, it):
    # ---------------- JP ----------------
    jp_title = "KO1KEYZキュントゥグンPOP-UPはいつ・どこ？特典まとめ！"
    jp = [
        p("デビュー日の10月7日をはさんで、KO1KEYZ(コイキーズ)の初めてのPOP-UPが新宿にやってきます。",
          f"「KO1KEYZ DEBUT SINGLE \"KO1KEYZ\" キュントゥグンPOP-UP」は、{mk('2026年10月2日(金)〜10月8日(木)に新宿サザンテラス(屋外)')}で開催されます。",
          f"さらに{mk('10月3日(土)・4日(日)の2日間だけ')}、メンバーが名前を付けたオリジナルドリンクの販売と、限定トレカが付くCD予約受付も行われます。",
          "この記事では、日程・時間・場所から、土日限定コーナーの特典、支払い方法の落とし穴、ねらい目の回り方までまとめました。"),
        ui.table("キュントゥグンPOP-UP 基本情報", [
            ("イベント名", "KO1KEYZ DEBUT SINGLE \"KO1KEYZ\" キュントゥグンPOP-UP"),
            ("期間", "2026年10月2日(金)〜10月8日(木)"),
            ("時間", "11:00〜19:00(初日10月2日のみ12:00〜19:00)"),
            ("会場", "新宿サザンテラス(屋外)"),
            ("住所", "東京都渋谷区代々木2丁目2-1"),
            ("展示", "集合展示パネル・メンバー別ソロコーナー・限定自己紹介映像・MV放映"),
            ("土日限定", "10月3日(土)・4日(日)11:00〜19:00 ドリンク販売・CD予約受付"),
            ("発表", "KO1KEYZ公式X・公式サイト(2026年9月26日)"),
        ]),
        ui.titlebox("この記事でわかること", [
            "POP-UPの日程・時間・場所", "展示の内容", "土日限定ドリンクの値段と特典",
            "CD予約でもらえる限定トレカ", "支払い方法の注意点", "新宿サザンテラスへの行き方とねらい目"]),
        fig(io, "KO1KEYZキュントゥグンPOP-UPの開催概要", SRC_X, "出典:"),
        h2("キュントゥグンPOP-UPはいつ・どこで開催？"),
        ui.minibox("<strong>期間:</strong>2026年10月2日(金)〜10月8日(木)の7日間",
                   "<strong>時間:</strong>11:00〜19:00(初日のみ12:00スタート)",
                   "<strong>場所:</strong>新宿サザンテラス(屋外)"),
        p("POP-UPが開かれるのは、デビューシングル『KO1KEYZ』の発売日である10月7日(水)を含む1週間です。",
          "初日の10月2日(金)だけは開始が1時間遅い12:00なので、朝から並ぶつもりで出かけると待ちぼうけになってしまいます。",
          "2日目以降は毎日11:00〜19:00で、最終日の10月8日(木)は発売翌日にあたります。"),
        p("会場の新宿サザンテラスは、JR新宿駅の南口から代々木方面へ延びる遊歩道です。",
          "住所は渋谷区代々木になりますが、実際は新宿駅の目の前という立地。",
          "告知でも「屋外」と明記されているので、雨の日は傘、日差しが強い日は帽子など、天気に合わせた準備をしておくと安心でしょう。"),
        p("イベント名の「キュントゥグン」は、デビュー曲「KO1KEYZ」のサビに出てくるフレーズです。",
          "日本語の「キュン」と、韓国語で胸がドキドキする音を表す「두근(トゥグン)」を合わせたような言葉で、日韓同時デビューのKO1KEYZらしいネーミングといえます。",
          f"曲のどこを誰が歌っているかは{a(L(13208), 'デビュー曲「KO1KEYZ」の歌割りまとめ')}で紹介しているので、会場でMVを見る前の予習にどうぞ。"),
        wphtml(MAP),
        h2("POP-UPの展示内容は？パネル・ソロコーナー・限定映像"),
        ui.minibox("<strong>展示:</strong>集合展示パネル・メンバー別ソロコーナー",
                   "<strong>映像:</strong>ここでしか見られない自己紹介コメント映像・「KO1KEYZ」MV"),
        fig(iv, "キュントゥグンPOP-UPの会場イメージ(集合パネル・ラッピングトラック・ソロパネル)", NEWS, "出典:"),
        p("会場で展開されるのは、12人がそろった集合展示パネルと、メンバーごとのソロコーナーです。",
          "公式サイトに載っている会場イメージを見ると、デビュージャケットの集合写真を使った大きなパネルに加えて、MVを流すラッピングトラック、植え込み沿いにずらりと並ぶソロパネルが描かれています。",
          "あくまでイメージなので実際の配置は変わるかもしれませんが、推しのソロパネルを探しながら歩くのが楽しみになりそうです。"),
        p(f"映像コーナーでは、タイトル曲「KO1KEYZ」のMVとともに、{mk('ここでしか見られない限定の自己紹介コメント映像')}が流れます。",
          "12人それぞれの自己紹介はデビュー前後のこの時期にしか撮れない貴重なもので、見に行く理由としては十分でしょう。",
          "展示と映像は平日も含めて毎日見られるので、土日の混雑を避けたい人は平日に展示だけ楽しむのもひとつの手です。"),
        h2("土日限定「キュントゥグンDRINK」の値段と特典は？"),
        ui.minibox("<strong>販売日:</strong>10月3日(土)・4日(日)11:00〜19:00(予定)",
                   "<strong>値段:</strong>各1,000円(税込)・全2種",
                   "<strong>特典:</strong>1杯ごとにストロータグ1枚+直筆メッセージ入りラミネートカード1枚(各全12種ランダム)"),
        fig(idr, "キュントゥグンDRINK 2種とストロータグ・ラミネートカード", SRC_X, "出典:"),
        p("土日の2日間だけ販売されるオリジナルドリンクは2種類。",
          f"メンバーが実際に試飲してメニュー名を付けたそうで、{mk('「KO1しいブルーレモネード」と「キュンと弾けるマンゴーシャワー」')}です。",
          "ブルーレモネードにはナタデココ、マンゴーシャワーにはマンゴーの果肉が入っていて、どちらも1杯1,000円(税込)。",
          "「KO1しい」は「恋しい」、「キュンと弾ける」はイベント名の「キュン」にかけたネーミングで、メニュー名だけでも思わずクスッとしてしまいます。"),
        p(f"うれしいのは購入特典で、{mk('1杯買うごとにストロータグとラミネートカードが1枚ずつ')}もらえます。",
          "ストロータグはメンバーカラーの丸いタグで、DAIKIは緑にクローバー、YOSHIKIはピンクにケーキ、というように、1人ずつのカラーとマークがデザインされています。",
          "ラミネートカードのほうは、なんとメンバーの直筆メッセージ入り。",
          "カードもメンバーカラーの台紙になっていて、裏面は共通の絵柄です。"),
        p("どちらも全12種のランダム配布で、絵柄は選べません。",
          "特典は先着順で、予定数に達した時点で終了となります。",
          "推しを引き当てたい人は2杯、3杯と買いたくなりそうですが、ドリンクなので飲み切れる量かどうかも考えておきたいところ。",
          "なお、会場や周辺の施設でのトレード(交換・売買・譲渡)は禁止されているので、交換はその場でしないよう注意してください。"),
        h2("CD予約でもらえる「キュントゥグンPOP-UP限定トレカ」とは？"),
        ui.minibox("<strong>受付日:</strong>10月3日(土)・4日(日)11:00〜19:00のみ",
                   "<strong>条件:</strong>初回限定盤A・初回限定盤B・通常盤の3形態セット予約ごとに1枚(全12種ランダム)",
                   "<strong>1セットの金額:</strong>5,200円(税込)"),
        fig(it, "キュントゥグンPOP-UP限定トレカと対象商品", SRC_X_CD, "出典:"),
        p("もうひとつの土日限定コーナーが、デビューシングル『KO1KEYZ』の予約受付です。",
          f"初回限定盤A・初回限定盤B・通常盤の{mk('3形態をセットで予約するごとに「キュントゥグンPOP-UP限定トレカ」が1枚')}もらえます。",
          "トレカはメンバーのソロ絵柄が全12種で、サイズは縦85mm×横55mmの予定。",
          "サンプル画像では、サッカーボールや鍵盤ハーモニカなど、1人ずつ違う小物を手にしたカラフルなカットになっています。"),
        p("対象商品の価格は、初回限定盤A(CD+DVD)と初回限定盤B(CD+DVD)が各1,900円、通常盤(CD ONLY)が1,400円です。",
          "3形態を合わせると1セット5,200円(税込)になります。",
          "FC限定盤は対象外で、この限定トレカ以外の外付け特典は付きません。",
          "一方で、各形態の初回プレス限定の封入特典はしっかり入っているので安心してください。"),
        p("予約した商品は、HMV&amp;BOOKS SHIBUYAで受け取るか、自宅へ配送してもらうかを選べます。",
          "配送の場合は1会計ごとに送料900円(税込)がかかり、10月7日(水)以降に順次届く予定です。",
          "店舗受け取りは発売日前日の夕方以降なので、10月6日(火)の夕方から受け取れる計算になります。",
          "予約後の枚数変更やキャンセルはできないので、何セット予約するかは事前に決めておきましょう。"),
        p("ちなみに、受け取り先のHMV&amp;BOOKS SHIBUYAでは、10月5日(月)〜12日(月・祝)にKO1KEYZの大型パネル展も開かれます。",
          f"CDを受け取るついでにパネル展も回れるので、詳しくは{a(L(13675), 'HMV渋谷の大型パネル展の記事')}もチェックしてみてください。",
          f"デビューシングルの収録曲や、ほかのショップの特典については{a(L(10866), 'デビューシングル『KO1KEYZ』の発売日・特典まとめ')}にまとめています。"),
        h2("支払い方法に注意！ドリンクは現金NG"),
        ui.minibox("<strong>ドリンク:</strong>クレジットカード・電子マネー・QRコード決済のみ(現金不可・一括払いのみ)",
                   "<strong>CD予約:</strong>現金もOK(クレジットカード・QRコード決済・電子マネーも可)"),
        p(f"意外と見落としやすいのが支払い方法です。",
          f"ドリンク販売は{mk('現金が使えず、キャッシュレス決済のみ')}となっています。",
          "使えるのはVISA・Mastercard・JCB・American Express・Diners Club・Discover・銀聯のクレジットカード、Suica・PASMOなどの交通系電子マネー、iD・QUICPay、PayPay・d払い・楽天ペイ・au PAY・メルペイ・WeChat Pay・Alipay+です。"),
        p("一方、CD予約のほうは現金でも支払えます。",
          "同じ会場でもコーナーによってルールが違うので、「現金しか持ってこなかった」という人はドリンクが買えずに終わってしまうかもしれません。",
          "通信状況によってはキャッシュレス決済に時間がかかる、あるいは使えなくなる場合もあると案内されているため、スマホ決済とカードなど2つ以上の手段を用意しておくと安心です。"),
        h2("新宿サザンテラスへの行き方とねらい目の回り方"),
        ui.minibox("<strong>最寄り:</strong>JR新宿駅 南口・新南改札からすぐ",
                   "<strong>ねらい目:</strong>展示だけなら平日、ドリンク・トレカ目当てなら土日の早い時間"),
        p("新宿サザンテラスは、JR新宿駅の南口・新南改札を出てすぐの場所にあります。",
          "甲州街道沿いの南口から、代々木方面へ向かう遊歩道に入ればすぐ目に入るはずです。",
          "都営新宿線・京王新線の新宿駅や、代々木駅からも歩ける距離にあります。"),
        p("混雑が予想されるのは、ドリンクとCD予約がある10月3日(土)・4日(日)です。",
          "特典はどちらも数に限りがあるので、確実にほしい人は早めの時間帯に行くのがよさそうです。",
          "ただし、会場周辺での徹夜や深夜からの集合は禁止されていて、スタッフの誘導前に作った列は無効になります。",
          "近隣の迷惑にならないよう、公式の案内に従って並びましょう。"),
        p("反対に、展示と限定映像をゆっくり見たいなら平日がおすすめです。",
          "特にデビュー日の10月7日(水)は、デビューを祝いに足を運ぶファンで平日でもにぎわうかもしれません。",
          "天候や運営の都合で内容や時間が変わることもあるため、出かける前にKO1KEYZ公式Xを確認しておくと確実です。"),
        h2("まとめ"),
        ui.summary([
            "キュントゥグンPOP-UPは2026年10月2日(金)〜8日(木)、新宿サザンテラス(屋外)で開催",
            "時間は11:00〜19:00、初日の10月2日のみ12:00スタート",
            "展示は集合パネル・ソロコーナー・限定自己紹介映像・MV",
            "10月3日(土)・4日(日)限定でドリンク(各1,000円)とCD予約受付",
            "ドリンク1杯ごとにストロータグ+直筆メッセージ入りラミネートカード",
            "CD3形態セット(5,200円)予約ごとに限定トレカ1枚",
            "ドリンクは現金不可、CD予約は現金OK",
        ]),
        p("デビューの1週間を、12人のパネルや限定映像と一緒に過ごせるのは今回ならでは。",
          "推しのストロータグや直筆カードを引き当てられるか、ドキドキしながら新宿へ足を運んでみてください！"),
        ui.quotebox("あわせて読みたい", [a(u, t) for u, t in REL["ja"]]),
    ]
    jp_sum = ("KO1KEYZのデビューを記念した「キュントゥグンPOP-UP」が10/2〜10/8に新宿サザンテラスで開催。"
              "土日限定ドリンク(各1,000円・直筆カード付き)やCD予約の限定トレカ、現金NGの注意点までまとめました。")

    # ---------------- KR ----------------
    kr_title = "KO1KEYZ 팝업 언제·어디서? 신주쿠 한정 음료·특전 총정리!"
    kr = [
        p("데뷔일인 10월 7일을 사이에 두고, KO1KEYZ(코이키즈)의 첫 팝업이 도쿄 신주쿠에서 열려요.",
          f"'KO1KEYZ DEBUT SINGLE \"KO1KEYZ\" キュントゥグン(큥투근) POP-UP'은 {mk('2026년 10월 2일(금)~10월 8일(목), 신주쿠 서던테라스(야외)')}에서 개최돼요.",
          f"게다가 {mk('10월 3일(토)·4일(일) 이틀 동안만')} 멤버들이 이름을 붙인 오리지널 음료 판매와 한정 트레카가 붙는 CD 예약 접수도 진행돼요.",
          "이 글에서는 일정·시간·장소부터 주말 한정 코너의 특전, 결제 방법 주의점, 추천 방문 방법까지 정리했어요."),
        ui.table("큥투근 POP-UP 기본 정보", [
            ("이벤트명", "KO1KEYZ DEBUT SINGLE \"KO1KEYZ\" キュントゥグンPOP-UP"),
            ("기간", "2026년 10월 2일(금)~10월 8일(목)"),
            ("시간", "11:00~19:00(첫날 10월 2일만 12:00~19:00)"),
            ("장소", "신주쿠 서던테라스(新宿サザンテラス, 야외)"),
            ("주소", "東京都渋谷区代々木2丁目2-1"),
            ("전시", "단체 전시 패널·멤버별 솔로 코너·한정 자기소개 영상·MV 상영"),
            ("주말 한정", "10월 3일(토)·4일(일) 11:00~19:00 음료 판매·CD 예약 접수"),
            ("발표", "KO1KEYZ 공식 X·공식 사이트(2026년 9월 26일)"),
        ]),
        ui.titlebox("이 글에서 알 수 있는 것", [
            "팝업 일정·시간·장소", "전시 내용", "주말 한정 음료 가격과 특전",
            "CD 예약 한정 트레카", "결제 방법 주의점", "신주쿠 서던테라스 가는 법과 추천 방문일"]),
        fig(io, "KO1KEYZ 큥투근 POP-UP 개최 개요", SRC_X, "출처:"),
        h2("큥투근 POP-UP은 언제·어디서?"),
        ui.minibox("<strong>기간:</strong>2026년 10월 2일(금)~10월 8일(목), 7일간",
                   "<strong>시간:</strong>11:00~19:00(첫날만 12:00 시작)",
                   "<strong>장소:</strong>신주쿠 서던테라스(야외)"),
        p("팝업은 데뷔 싱글 『KO1KEYZ』 발매일인 10월 7일(수)을 포함한 일주일 동안 열려요.",
          "첫날인 10월 2일(금)만 시작 시간이 1시간 늦은 12:00이니 주의하세요.",
          "둘째 날부터는 매일 11:00~19:00이고, 마지막 날인 10월 8일(목)은 발매 다음 날이에요."),
        p("장소인 신주쿠 서던테라스는 JR 신주쿠역 남쪽 출구에서 요요기 방면으로 이어지는 산책로예요.",
          "주소는 시부야구 요요기지만 실제로는 신주쿠역 바로 앞이라 찾기 쉬워요.",
          "공지에 '야외'라고 적혀 있으니 날씨에 맞춰 우산이나 모자를 챙기면 좋아요."),
        p("이벤트명의 'キュントゥグン(큥투근)'은 데뷔곡 'KO1KEYZ'의 후렴에 나오는 가사예요.",
          "일본어로 설렘을 나타내는 'キュン(큥)'과 한국어 '두근'을 합친 듯한 말이라, 한일 동시 데뷔하는 KO1KEYZ다운 이름이에요.",
          f"누가 어느 파트를 부르는지는 {a(L(13220), '타이틀곡 KO1KEYZ 파트 분배 정리')}에서 확인할 수 있어요."),
        wphtml(MAP),
        h2("팝업 전시 내용은? 패널·솔로 코너·한정 영상"),
        ui.minibox("<strong>전시:</strong>단체 전시 패널·멤버별 솔로 코너",
                   "<strong>영상:</strong>여기서만 볼 수 있는 자기소개 코멘트 영상·'KO1KEYZ' MV"),
        fig(iv, "큥투근 POP-UP 현장 이미지(단체 패널·래핑 트럭·솔로 패널)", NEWS, "출처:"),
        p("현장에는 12명이 모두 담긴 단체 전시 패널과 멤버별 솔로 코너가 마련돼요.",
          "공식 사이트의 현장 이미지를 보면 데뷔 재킷 단체 사진을 쓴 대형 패널, MV를 트는 래핑 트럭, 화단을 따라 늘어선 솔로 패널이 그려져 있어요.",
          "어디까지나 이미지라 실제 배치는 달라질 수 있지만, 최애의 솔로 패널을 찾아다니는 재미가 있을 것 같아요."),
        p(f"영상 코너에서는 타이틀곡 'KO1KEYZ' MV와 함께 {mk('여기서만 볼 수 있는 한정 자기소개 코멘트 영상')}이 상영돼요.",
          "전시와 영상은 평일을 포함해 매일 볼 수 있으니, 주말 혼잡을 피하고 싶다면 평일에 전시만 즐기는 것도 방법이에요."),
        h2("주말 한정 '큥투근 DRINK' 가격과 특전은?"),
        ui.minibox("<strong>판매일:</strong>10월 3일(토)·4일(일) 11:00~19:00(예정)",
                   "<strong>가격:</strong>각 1,000엔(세금 포함)·2종",
                   "<strong>특전:</strong>1잔마다 스트로 태그 1장+친필 메시지 라미네이트 카드 1장(각 12종 랜덤)"),
        fig(idr, "큥투근 DRINK 2종과 스트로 태그·라미네이트 카드", SRC_X, "출처:"),
        p("주말 이틀 동안만 판매되는 오리지널 음료는 2종류예요.",
          f"멤버들이 직접 시음하고 메뉴 이름을 지었다고 하는데, {mk("'KO1しいブルーレモネード(블루 레모네이드)'와 'キュンと弾けるマンゴーシャワー(망고 샤워)'")}예요.",
          "블루 레모네이드에는 나타데코코, 망고 샤워에는 망고 과육이 들어 있고, 둘 다 1잔 1,000엔(세금 포함)이에요.",
          "'KO1しい'는 일본어 '恋しい(그립다)'와 발음이 같은 말장난이라 메뉴 이름부터 귀여워요."),
        p(f"가장 반가운 건 구매 특전이에요. {mk('1잔 살 때마다 스트로 태그와 라미네이트 카드를 1장씩')} 받을 수 있어요.",
          "스트로 태그는 멤버 컬러의 둥근 태그로, DAIKI는 초록에 클로버, YOSHIKI는 핑크에 케이크처럼 멤버마다 컬러와 마크가 디자인되어 있어요.",
          "라미네이트 카드에는 무려 멤버의 친필 메시지가 들어가요."),
        p("둘 다 12종 랜덤이라 디자인은 고를 수 없고, 선착순으로 예정 수량이 끝나면 종료돼요.",
          "현장과 주변 시설에서의 교환·매매·양도는 금지되어 있으니 주의하세요."),
        h2("CD 예약 특전 '큥투근 POP-UP 한정 트레카'란?"),
        ui.minibox("<strong>접수일:</strong>10월 3일(토)·4일(일) 11:00~19:00만",
                   "<strong>조건:</strong>초회한정반 A·초회한정반 B·통상반 3종 세트 예약마다 1장(12종 랜덤)",
                   "<strong>1세트 금액:</strong>5,200엔(세금 포함)"),
        fig(it, "큥투근 POP-UP 한정 트레카와 대상 상품", SRC_X_CD, "출처:"),
        p(f"또 하나의 주말 한정 코너는 데뷔 싱글 『KO1KEYZ』 예약 접수예요. {mk('3종을 세트로 예약할 때마다 한정 트레카 1장')}을 받을 수 있어요.",
          "트레카는 멤버 솔로 컷 12종으로, 크기는 세로 85mm×가로 55mm 예정이에요.",
          "대상 상품은 초회한정반 A(CD+DVD)·초회한정반 B(CD+DVD) 각 1,900엔, 통상반(CD ONLY) 1,400엔으로, 3종 합계 5,200엔이에요.",
          "FC 한정반은 대상 외이고, 이 트레카 외의 추가 특전은 없지만 초회 프레스 한정 봉입 특전은 들어 있어요."),
        p("예약 상품은 HMV&amp;BOOKS SHIBUYA에서 받거나 택배로 받을 수 있어요.",
          "택배는 1회 결제마다 배송비 900엔이 들고, 10월 7일(수) 이후 순차 발송돼요.",
          "매장 수령은 발매 전날 저녁부터라 10월 6일(화) 저녁부터 받을 수 있어요.",
          f"수령처인 HMV&amp;BOOKS SHIBUYA에서는 10월 5일~12일에 {a(L(13676), 'KO1KEYZ 대형 패널전')}도 열리니 함께 들르는 것도 추천해요."),
        h2("결제 방법 주의! 음료는 현금 불가"),
        ui.minibox("<strong>음료:</strong>신용카드·전자화폐·QR 결제만(현금 불가·일시불만)",
                   "<strong>CD 예약:</strong>현금 가능(카드·QR 결제·전자화폐도 가능)"),
        p(f"놓치기 쉬운 게 결제 방법이에요. 음료 판매는 {mk('현금을 쓸 수 없고 캐시리스 결제만')} 가능해요.",
          "VISA·Mastercard·JCB·AMEX·Diners·Discover·은련 카드, Suica·PASMO 등 교통계 IC카드, PayPay 등의 QR 결제에 더해 WeChat Pay·Alipay+도 쓸 수 있어서 한국에서 오는 분도 편리해요.",
          "반면 CD 예약은 현금으로도 결제할 수 있어요.",
          "통신 상황에 따라 결제가 늦어질 수 있다고 하니 결제 수단을 2가지 이상 준비해 두면 안심이에요."),
        h2("신주쿠 서던테라스 가는 법과 추천 방문일"),
        ui.minibox("<strong>가까운 역:</strong>JR 신주쿠역 남쪽 출구·신남쪽 개찰구 바로 앞",
                   "<strong>추천:</strong>전시만 볼 거라면 평일, 음료·트레카가 목적이라면 주말 이른 시간"),
        p("신주쿠 서던테라스는 JR 신주쿠역 남쪽 출구(南口)·신남쪽 개찰구(新南改札)를 나오면 바로 있어요.",
          "도에이 신주쿠선·게이오 신선 신주쿠역이나 요요기역에서도 걸어갈 수 있어요."),
        p("가장 붐빌 것으로 보이는 날은 음료와 CD 예약이 있는 10월 3일(토)·4일(일)이에요.",
          "특전은 수량 한정이라 꼭 받고 싶다면 이른 시간대가 좋아요.",
          "다만 밤샘이나 심야 대기는 금지이고, 스태프 안내 전에 만든 줄은 무효가 되니 공식 안내를 따라 주세요.",
          "날씨나 운영 사정으로 내용이 바뀔 수 있으니 방문 전에 KO1KEYZ 공식 X를 확인하세요."),
        h2("정리"),
        ui.summary([
            "큥투근 POP-UP은 2026년 10월 2일(금)~8일(목), 신주쿠 서던테라스(야외)",
            "시간은 11:00~19:00, 첫날만 12:00 시작",
            "전시는 단체 패널·솔로 코너·한정 자기소개 영상·MV",
            "10월 3일(토)·4일(일) 한정으로 음료(각 1,000엔)와 CD 예약",
            "음료 1잔마다 스트로 태그+친필 메시지 라미네이트 카드",
            "CD 3종 세트(5,200엔) 예약마다 한정 트레카 1장",
            "음료는 현금 불가, CD 예약은 현금 가능",
        ]),
        p("데뷔 주간을 12명의 패널과 한정 영상과 함께 보낼 수 있는 건 이번뿐이에요.",
          "최애의 스트로 태그와 친필 카드를 뽑을 수 있을지, 두근두근하며 신주쿠에 들러 보세요!"),
        ui.quotebox("함께 읽으면 좋은 글", [a(u, t) for u, t in REL["ko"]]),
    ]
    kr_sum = ("KO1KEYZ 데뷔 기념 '큥투근 POP-UP'이 10/2~10/8 신주쿠 서던테라스에서 개최돼요. "
              "주말 한정 음료(각 1,000엔·친필 카드 특전)와 CD 예약 한정 트레카, 현금 불가 주의점까지 정리했어요.")

    # ---------------- EN ----------------
    en_title = "KO1KEYZ Pop-Up in Shinjuku: When, Where, and What Bonuses?"
    en = [
        p("KO1KEYZ's first-ever pop-up is coming to Shinjuku, right around their October 7 debut.",
          f"The \"KO1KEYZ DEBUT SINGLE 'KO1KEYZ' Kyuntugun POP-UP\" runs {mk('from Friday, October 2 to Thursday, October 8, 2026, at Shinjuku Southern Terrace (outdoors)')}.",
          f"On {mk('Saturday, October 3 and Sunday, October 4 only')}, there will also be original drinks named by the members and CD pre-orders that come with an exclusive trading card.",
          "This article covers the dates, hours, and venue, the weekend-only bonuses, a payment pitfall to watch out for, and tips on when to go."),
        ui.table("Kyuntugun POP-UP: Key Info", [
            ("Event", "KO1KEYZ DEBUT SINGLE \"KO1KEYZ\" キュントゥグンPOP-UP"),
            ("Dates", "October 2 (Fri) to October 8 (Thu), 2026"),
            ("Hours", "11:00-19:00 (opening day, October 2, 12:00-19:00)"),
            ("Venue", "Shinjuku Southern Terrace (outdoors)"),
            ("Address", "2-2-1 Yoyogi, Shibuya-ku, Tokyo"),
            ("Exhibits", "Group panel, solo corners for each member, exclusive self-introduction videos, MV screening"),
            ("Weekend only", "October 3 (Sat) and 4 (Sun), 11:00-19:00: drinks and CD pre-orders"),
            ("Announced by", "KO1KEYZ official X and official website (September 26, 2026)"),
        ]),
        ui.titlebox("What you'll learn", [
            "Pop-up dates, hours, and venue", "What's on display", "Weekend-only drinks: prices and bonuses",
            "The exclusive trading card for CD pre-orders", "Payment methods to know", "How to get there and when to go"]),
        fig(io, "Overview of the KO1KEYZ Kyuntugun POP-UP", SRC_X, "Source: "),
        h2("When and where is the Kyuntugun POP-UP?"),
        ui.minibox("<strong>Dates:</strong>October 2 (Fri) to October 8 (Thu), 2026 (7 days)",
                   "<strong>Hours:</strong>11:00-19:00 (opens at 12:00 on the first day only)",
                   "<strong>Venue:</strong>Shinjuku Southern Terrace (outdoors)"),
        p("The pop-up runs for a week that includes October 7 (Wed), the release date of the debut single \"KO1KEYZ.\"",
          "Only the first day, October 2, opens an hour later at 12:00, so there's no need to show up first thing in the morning.",
          "From the second day on, it's open daily from 11:00 to 19:00, and the final day, October 8, is the day after the release."),
        p("Shinjuku Southern Terrace is a promenade that stretches from the South Exit of JR Shinjuku Station toward Yoyogi.",
          "Its address is technically in Yoyogi, Shibuya-ku, but it sits right in front of Shinjuku Station.",
          "The venue is outdoors, so bring an umbrella or a hat depending on the weather."),
        p("\"Kyuntugun\" comes from the chorus of the debut song \"KO1KEYZ.\"",
          "It sounds like a blend of the Japanese \"kyun\" (the flutter of a heart) and the Korean \"dugeun\" (a heartbeat), a fitting name for a group debuting in Japan and Korea at the same time.",
          f"For who sings which line, see {a(L(13221), 'our title track part distribution guide')}."),
        wphtml(MAP),
        h2("What's on display? Panels, solo corners, and exclusive videos"),
        ui.minibox("<strong>Exhibits:</strong>Group panel and a solo corner for each member",
                   "<strong>Videos:</strong>Exclusive self-introduction comments and the \"KO1KEYZ\" MV"),
        fig(iv, "Venue image of the Kyuntugun POP-UP: group panel, wrapped truck, and solo panels", NEWS, "Source: "),
        p("The venue features a group panel with all 12 members and a solo corner for each of them.",
          "The venue image on the official site shows a large panel using the debut jacket's group photo, a wrapped truck screening the MV, and a row of solo panels along the planters.",
          "It's only an image, so the actual layout may differ, but hunting for your bias's solo panel should be fun."),
        p(f"The video corner screens the title track MV along with {mk('self-introduction comment videos you can only see here')}.",
          "The exhibits and videos are open every day, weekdays included, so if you'd rather avoid the weekend crowds, a weekday visit works well."),
        h2("Weekend-only \"Kyuntugun DRINK\": prices and bonuses"),
        ui.minibox("<strong>On sale:</strong>October 3 (Sat) and 4 (Sun), 11:00-19:00 (planned)",
                   "<strong>Price:</strong>1,000 yen each (tax incl.; about 7 USD at 150 yen/USD), 2 kinds",
                   "<strong>Bonus:</strong>With every drink, 1 straw tag + 1 laminated card with a handwritten message (12 designs each, random)"),
        fig(idr, "The two Kyuntugun DRINKs with straw tags and laminated cards", SRC_X, "Source: "),
        p("Two original drinks will be sold on the weekend only.",
          f"The members tasted them and named them themselves: {mk('\"KO1しいブルーレモネード\" (a blue lemonade) and \"キュンと弾けるマンゴーシャワー\" (a mango shower)')}.",
          "The blue lemonade comes with nata de coco and the mango shower with mango chunks, and each costs 1,000 yen.",
          "\"KO1しい\" is a pun on the Japanese word \"koishii\" (to miss someone), which is typical KO1KEYZ wordplay."),
        p(f"The best part is the bonus: {mk('each drink comes with one straw tag and one laminated card')}.",
          "The straw tags are round tags in each member's color with their own icon, such as a green clover for DAIKI and a pink cake for YOSHIKI.",
          "The laminated cards even carry a handwritten message from a member."),
        p("Both are random out of 12 designs, and you can't choose which you get.",
          "They're first-come, first-served and end once the planned quantity runs out.",
          "Trading (exchanging, selling, or giving away) at the venue or nearby facilities is prohibited, so please don't swap on site."),
        h2("What is the \"Kyuntugun POP-UP exclusive trading card\"?"),
        ui.minibox("<strong>Pre-orders:</strong>October 3 (Sat) and 4 (Sun), 11:00-19:00 only",
                   "<strong>Condition:</strong>1 card per set of all three editions (Limited A, Limited B, Regular), random out of 12",
                   "<strong>Price per set:</strong>5,200 yen (tax incl.)"),
        fig(it, "The Kyuntugun POP-UP exclusive trading cards and eligible editions", SRC_X_CD, "Source: "),
        p(f"The other weekend-only corner is pre-orders for the debut single. {mk('For every set of all three editions you pre-order, you get one exclusive trading card')}.",
          "There are 12 solo designs, and the planned size is 85 mm by 55 mm.",
          "Limited Edition A (CD+DVD) and Limited Edition B (CD+DVD) are 1,900 yen each, and the Regular Edition (CD only) is 1,400 yen, for a total of 5,200 yen per set.",
          "The fan club edition is not eligible, and there are no other external bonuses, though the first-press inserts are included."),
        p("You can pick up your order at HMV&amp;BOOKS SHIBUYA or have it delivered.",
          "Delivery costs 900 yen per transaction and ships from October 7 onward.",
          "In-store pickup starts from the evening before release, which means the evening of October 6 (Tue).",
          f"HMV&amp;BOOKS SHIBUYA is also hosting {a(L(13677), 'the KO1KEYZ giant panel exhibition')} from October 5 to 12, so you can see both in one trip."),
        h2("Heads up on payment: no cash for drinks"),
        ui.minibox("<strong>Drinks:</strong>Credit cards, e-money, and QR code payments only (no cash, single payment only)",
                   "<strong>CD pre-orders:</strong>Cash accepted (cards, QR codes, and e-money also OK)"),
        p(f"Payment is easy to overlook. {mk('Drinks are cashless only')}.",
          "Accepted methods include VISA, Mastercard, JCB, AMEX, Diners Club, Discover, and UnionPay; transit IC cards like Suica and PASMO; iD and QUICPay; and QR payments including PayPay, WeChat Pay, and Alipay+.",
          "CD pre-orders, on the other hand, can be paid in cash.",
          "Cashless payments may be slow or unavailable depending on the connection, so having two or more payment options is a good idea."),
        h2("How to get to Shinjuku Southern Terrace and when to go"),
        ui.minibox("<strong>Nearest station:</strong>Right outside the South Exit / New South Gate of JR Shinjuku Station",
                   "<strong>Best time:</strong>Weekdays for the exhibits; early on the weekend for drinks and cards"),
        p("Shinjuku Southern Terrace is right outside the South Exit and New South Gate of JR Shinjuku Station.",
          "It's also walkable from Shinjuku Station on the Toei Shinjuku and Keio New lines, and from Yoyogi Station."),
        p("The busiest days will likely be October 3 and 4, when drinks and CD pre-orders are available.",
          "Bonuses are limited, so go early if you really want them.",
          "Overnight camping and gathering in the late night are prohibited, and lines formed before staff direct them are invalid, so follow the official instructions.",
          "Details may change due to weather or operations, so check KO1KEYZ's official X account before you go."),
        h2("Summary"),
        ui.summary([
            "The Kyuntugun POP-UP runs October 2 (Fri) to 8 (Thu), 2026, at Shinjuku Southern Terrace (outdoors)",
            "Hours are 11:00-19:00; opening day starts at 12:00",
            "Exhibits: group panel, solo corners, exclusive self-intro videos, and the MV",
            "Drinks (1,000 yen each) and CD pre-orders on October 3 and 4 only",
            "Each drink comes with a straw tag and a laminated card with a handwritten message",
            "One exclusive trading card per three-edition set (5,200 yen)",
            "No cash for drinks; cash is fine for CD pre-orders",
        ]),
        p("Spending debut week with the 12 members' panels and exclusive videos is something only this pop-up offers.",
          "If you're in Tokyo, head to Shinjuku and see whether you can pull your bias's straw tag and handwritten card!"),
        ui.quotebox("Related articles", [a(u, t) for u, t in REL["en"]]),
    ]
    en_sum = ("KO1KEYZ's debut \"Kyuntugun POP-UP\" runs Oct 2-8 at Shinjuku Southern Terrace. "
              "Weekend-only drinks (1,000 yen, with handwritten cards), an exclusive card for CD pre-orders, and why you shouldn't bring only cash.")
    join = lambda bl: "\n\n".join(bl)
    return (jp_title, join(jp), jp_sum), (kr_title, join(kr), kr_sum), (en_title, join(en), en_sum)


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
    subprocess.run([sys.executable, tool, "--top", "新宿で限定ドリンク！", "--main", "KO1KEYZ",
                    "--bottom", "POP-UPはいつ・どこ？", "--out", str(EYE_JP), "--seed", "7"], check=True)
    subprocess.run([sys.executable, tool, "--top", "신주쿠 한정 음료!", "--main", "KO1KEYZ",
                    "--bottom", "팝업 언제·어디서?", "--out", str(EYE_KR), "--seed", "7", "--lang", "kr"], check=True)


if __name__ == "__main__":
    if "--dry" in sys.argv:
        dummy = {"id": 0, "full": {"source_url": "x", "width": 1, "height": 1}}
        dummy["large"] = dummy["medium"] = dummy["full"]
        for (t, c, _), name in zip(build(dummy, dummy, dummy, dummy), ("JP", "KR", "EN")):
            assert "<hr" not in c
            print(name, len(t), t, "chars:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", c)))
        sys.exit(0)
    make_eyecatch()
    io = upload(IMG_OVERVIEW, "image/jpeg")
    iv = upload(IMG_VENUE, "image/jpeg")
    idr = upload(IMG_DRINK, "image/jpeg")
    it = upload(IMG_TRECA, "image/jpeg")
    (jt, jc, js), (kt, kc, ks), (et, ec, es) = build(io, iv, idr, it)
    jp_eye = upload(EYE_JP, "image/png")["id"]
    kr_eye = upload(EYE_KR, "image/png")["id"]
    jp = post_draft(jt, jc, BASE_SLUG, "ja", [66, 62], jp_eye, js)
    print("JP", jp["id"], jp["slug"], jp["link"])
    kr = post_draft(kt, kc, BASE_SLUG + "-kr", "ko", [74, 70], kr_eye, ks, jp["id"])
    print("KR", kr["id"], kr["slug"], kr["link"])
    en = post_draft(et, ec, BASE_SLUG + "-en", "en", [110, 112], jp_eye, es, jp["id"])
    print("EN", en["id"], en["slug"], en["link"])
    print("images", io["id"], iv["id"], idr["id"], it["id"], "eyecatch", jp_eye, kr_eye)
