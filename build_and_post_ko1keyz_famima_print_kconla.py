# -*- coding: utf-8 -*-
"""KCON LA 2026 のファミマプリント(ブロマイド)に KO1KEYZ が登場(2026-10-16〜11-30)。
chomoand-1.com に JP/KR/EN の下書きを作る(本文画像は公式X埋め込みのみ+アイキャッチ)。

一次ソース:
- KCON USA公式X https://x.com/kconusa/status/2111260907183485427 (2026-10-17 10:00 JST、告知画像「10/16(金)〜11/30(月) ファミマプリント販売スタート！」・7組)
- ファミマプリント公式 https://famima-print.family.co.jp/kpop/kcon-la-2026/ (7組102種。KO1KEYZは12人×#1/#2=24種)
  各商品ページ: 2026年11月30日(月)23時59分まで、ブロマイドL判 片面1枚200円/2L判 片面1枚300円(税込)、プリント番号KKC1038003〜026
  サンプル画像は確認用に見ただけ(#1=白背景のポートレート・ユニフォーム衣装、#2=ステージのライブカット)。記事には載せない。
- ご利用ガイド https://famima-print.family.co.jp/information/usage ・ QR https://famima-print.family.co.jp/information/usage_qr
- KCON JAPAN 2026 ファミマプリントは 7/1〜7/31、L判200円/2L判300円(東京バーゲンマニア)

python build_and_post_ko1keyz_famima_print_kconla.py [--dry]
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

EYE_JP = ROOT / "images" / "ko1keyz_famima_print_kconla_eyecatch.png"
EYE_KR = ROOT / "images" / "ko1keyz_famima_print_kconla_eyecatch_kr.png"
BASE_SLUG = "ko1keyz-famima-print-kcon-la"

TW = "https://twitter.com/kconusa/status/2111260907183485427"
FP = "https://famima-print.family.co.jp/kpop/kcon-la-2026/"
FP_ITEM = "https://famima-print.family.co.jp/kpop/kcon-la-2026/kcon-la-2026-05/KKC1038{:03d}.html"
FP_USAGE = "https://famima-print.family.co.jp/information/usage"
FP_QR = "https://famima-print.family.co.jp/information/usage_qr"
STORE = "https://networkprint.ne.jp/search_store/map.html?stype=ALL&fco[]=968442&lock=true"

MEMBERS = ["DAIKI", "ISSA", "KEITO", "KOSUKE", "RYOGA", "RYUJI",
           "SHINHAENG", "SIYOUNG", "TOWA", "YOSHIKI", "YUKI", "YURA"]

L = lambda pid: f"https://chomoand-1.com/?p={pid}"
REL = {
    "ja": [(L(14098), "KO1KEYZのPHOTOGRAYはどこで撮れる？KCON LAフレームの期間・値段"),
           (L(11353), "KO1KEYZのKCON LA 2026衣装、背番号「07・10・26」の意味は？"),
           (L(11016), "KCON LA 2026のKO1KEYZの視聴方法まとめ"),
           (L(14216), "KO1KEYZがファミマTVに！どこで見れる？時間帯と期間")],
    "ko": [(L(14099), "KO1KEYZ 포토그레이 어디서 찍을 수 있을까? KCON LA 프레임 기간·가격"),
           (L(12673), "KO1KEYZ의 KCON LA 2026 의상, 등번호 '07·10·26'의 의미는?"),
           (L(11019), "KCON LA 2026 KO1KEYZ 시청 방법 정리"),
           (L(14220), "KO1KEYZ 파미마TV 출연! 방송 시간과 기간")],
    "en": [(L(14100), "Where can you take KO1KEYZ PHOTOGRAY photos? KCON LA frame dates & price"),
           (L(12675), "KO1KEYZ's KCON LA 2026 outfits: what do the numbers 07, 10, 26 mean?"),
           (L(12604), "How to watch KO1KEYZ at KCON LA 2026")],
}

ui = Ui("#8a8378", "#ddd9d3", "#f7f6f4", "rgba(138,131,120,0.06)")


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def embed(tw, lang):
    return wphtml(f'<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{tw}">{tw}</a></blockquote>\n'
                  '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def steps(title, items):
    lis = "\n".join(f'<li style="margin:0 0 8px 0;">{i}</li>' for i in items[:-1]) + f'\n<li style="margin:0;">{items[-1]}</li>'
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#8a8378;color:#fff;">{title}</p>
<ol style="margin:0;padding:14px 18px 14px 34px;background:#f7f6f4;">
{lis}
</ol>
</div>''')


def number_rows():
    rows = []
    for i, m in enumerate(MEMBERS):
        n1, n2 = 3 + i * 2, 4 + i * 2
        rows.append((m, f'#1 {a(FP_ITEM.format(n1), f"KKC1038{n1:03d}")}<br>#2 {a(FP_ITEM.format(n2), f"KKC1038{n2:03d}")}'))
    return rows


def build():
    # ---------------- JP ----------------
    jp_title = "KO1KEYZのファミマプリントはいつまで？値段・種類まとめ！"
    jp = [
        p("8月にアメリカ・ロサンゼルスで開かれたKCON LA 2026で撮られたKO1KEYZ(コイキーズ)の写真が、ファミリーマートで買えるようになりました。",
          f"コンビニのマルチコピー機で印刷する「ファミマプリント」のブロマイドで、販売期間は{mk('2026年10月16日(金)〜11月30日(月)23時59分')}です。",
          f"値段は{mk('L判1枚200円・2L判1枚300円(税込)')}で、12人それぞれに2種類ずつ、全24種がそろっています。",
          "この記事では、どんな写真なのか、メンバー別のプリント番号、マルチコピー機での買い方と注意点までまとめました。"),
        ui.table("KCON LA 2026 ファミマプリント 基本情報", [
            ("販売期間", "2026年10月16日(金)〜11月30日(月)23:59"),
            ("商品", "ブロマイド(片面)L判・2L判"),
            ("値段", "L判1枚200円/2L判1枚300円(税込)"),
            ("KO1KEYZ", "12人×2種類(#1・#2)=24種"),
            ("出演アーティスト", "ALPHA DRIVE ONE・izna・JO1・KickFlip・KO1KEYZ・MODYSSEY・ZEROBASEONE(全102種)"),
            ("買える場所", "全国のファミリーマート(写真プリント対応のマルチコピー機がある店舗)"),
            ("発表", "KCON USA公式X(2026年10月17日)"),
        ]),
        ui.titlebox("この記事でわかること", [
            "どんな写真が買える？", "販売期間と値段", "12人のプリント番号一覧",
            "マルチコピー機での買い方", "買う前の注意点", "ほかの出演アーティスト"]),
        h2("KO1KEYZのKCON LA 2026ファミマプリントとは？どんな写真？"),
        ui.minibox("<strong>内容:</strong>KCON LA 2026で撮影されたメンバーのブロマイド",
                   "<strong>種類:</strong>1人につき#1(白背景のポートレート)と#2(ステージ写真)の2種類"),
        p("KCON USAの公式Xは10月17日、「KCON LA 2026の感動をもう一度」としてファミマプリントの販売開始を告知しました。",
          "告知画像には「10/16(金)〜11/30(月)」の期間と、出演した7組のロゴが並んでいます。"),
        embed(TW, "ja"),
        p("KO1KEYZがKCON LA 2026のステージに立ったのは、8月14日(金)。",
          "10月7日のデビューより前、12人にとって初めての大きな海外のステージでした。",
          "その日の姿が、日本のコンビニで手に取れる写真になって戻ってきた形です。"),
        p(f"ファミマプリントの公式ページでサンプルを見てみると、{mk('#1は白い背景で撮ったポートレート、#2はステージ上のライブ写真')}という分け方になっていました。",
          "#1はネイビー×白のユニフォーム風衣装で、手をあごに添えたり胸元に置いたりと、1人ずつポーズを決めたアップの1枚です。",
          "#2はパフォーマンス中のカットで、ユニフォーム衣装のメンバーもいれば、赤い背景に白い衣装で歌うメンバーもいます。"),
        p("どの写真も右下に「KCON LA 2026」のロゴが入っていて、イベントの記念品らしい仕上がりです。",
          f"ユニフォームの胸の背番号「07」「10」「26」に込められた意味は、{a(L(11353), 'KCON LA 2026衣装の背番号をまとめた記事')}で紹介しています。",
          "キメ顔の#1と、ステージの熱気が伝わる#2を並べて飾るのも楽しそうです。"),
        h2("いつまで買える？販売期間と値段"),
        ui.minibox("<strong>期間:</strong>2026年10月16日(金)〜11月30日(月)23時59分",
                   "<strong>値段:</strong>L判1枚200円/2L判1枚300円(税込)"),
        p(f"販売期間は{mk('11月30日(月)の23時59分まで')}で、約1か月半あります。",
          "告知は10月17日でしたが、販売そのものは前日の16日から始まっていました。"),
        p("サイズは、一般的な写真と同じL判(89×127mm)と、ひと回り大きい2L判(127×178mm)の2つ。",
          "どちらも片面印刷で、トレカケースやフォトフレームに入れるならL判、部屋に飾るなら2L判が使いやすいサイズです。"),
        ui.table("まとめて買うといくら？(税込)", [
            ("1人分(2種類)", "L判400円/2L判600円"),
            ("12人分(24種類)", "L判4,800円/2L判7,200円"),
        ]),
        p("推し1人の2種類なら、L判で400円。",
          "12人全員の24種類をコンプリートしてもL判なら4,800円で、遠征せずに近所のコンビニでそろえられるのはうれしいポイントです。"),
        p("同じKCONでは、5月のKCON JAPAN 2026のブロマイドも7月の1か月間ファミマプリントで販売され、値段は今回と同じL判200円・2L判300円でした。",
          "販売が終わるとあとから買い直す方法はなく、フリマアプリで定価より高く出回ることもあります。",
          "ほしい写真があるなら、期間中に印刷しておくのが確実です。"),
        h2("KO1KEYZ 12人のプリント番号一覧"),
        ui.minibox("<strong>プリント番号:</strong>KKC1038003〜KKC1038026(12人×2種類)",
                   "<strong>使い方:</strong>マルチコピー機で番号を入力すると、その写真を直接選べる"),
        p("マルチコピー機では、商品ごとに決まった「プリント番号」を入力すると、目当ての写真にすぐたどり着けます。",
          "KO1KEYZの24種類の番号は下の通りです。",
          "番号をタップすると、ファミマプリントの商品ページ(サンプル画像・QRコードつき)が開きます。"),
        ui.table("KO1KEYZ プリント番号(#1=ポートレート/#2=ステージ)", number_rows()),
        p(f"ほかの出演アーティストも含めた一覧は、{a(FP, 'ファミマプリントのKCON LA 2026ページ')}で見られます。",
          "ランダム販売ではなく、写真を自分で選んで買える方式なので、推しの番号だけ控えておけば大丈夫です。"),
        h2("ファミマプリントの買い方は？マルチコピー機での手順"),
        ui.minibox("<strong>方法1:</strong>プリント番号を入力して買う",
                   "<strong>方法2:</strong>商品ページのQRコードを読み取らせて買う"),
        p("ファミマプリントは、ファミリーマートの店内にあるマルチコピー機で買います。",
          "ネット通販はないので、お店に行って印刷する必要があります。"),
        steps("プリント番号で買う手順", [
            "マルチコピー機の液晶画面右下の青い枠をタッチ",
            "コンテンツサービスの【famima PRINT】をタッチし、利用規約に同意する",
            "【プリント番号入力】をタッチして、ほしい写真の番号(KKC1038〜)を入力",
            "サイズ(L判/2L判)と枚数を選んで【購入】をタッチ",
            "プリント排出口から写真が出てくる",
        ]),
        p(f"もう1つの方法が、{mk('商品ページのQRコードを使うやり方')}です。",
          "スマホで商品ページを開き、QRコード(スクリーンショットでもOK)を用意しておけば、番号を打ち込む手間がかかりません。"),
        steps("QRコードで買う手順", [
            "買いたい商品ページを開き、QRコードを表示する",
            "マルチコピー機の液晶画面右側の「2次元コードを持っている」をタッチ",
            "コードリーダーにQRコードをかざし、同意事項を確認して「同意する」",
            "サイズと枚数を確認して【購入】をタッチ",
        ]),
        p(f"細かい操作は{a(FP_USAGE, 'ファミマプリントのご利用ガイド')}と{a(FP_QR, 'QRコードのご利用方法')}にも、画面の写真つきで載っています。"),
        h2("買う前に知っておきたい注意点"),
        ui.minibox("<strong>店舗:</strong>写真プリントができないマルチコピー機では買えない",
                   "<strong>返品:</strong>印刷のミスがある場合を除き、交換・返金はできない"),
        p(f"気をつけたいのは、{mk('すべてのファミリーマートで買えるわけではない')}ことです。",
          "写真プリントに対応していないマルチコピー機や、コインを入れる部分が細長く小さいタイプのマルチコピー機では、ファミマプリントを利用できません。"),
        p(f"行く前に{a(STORE, 'コンビニ店舗検索')}で、「写真プリント(L判)」「写真プリント(2L判)」「ファミリーマート」にチェックを入れて調べておくと、対応しているお店だけが表示されます。",
          "2L判がほしいときは、2L判にも対応しているかまで見ておくと安心です。"),
        p("また、印刷されたものは、印刷上の不具合がある場合を除いて交換や返金ができません。",
          "スマホの画面で見るサンプルと、実際の写真では色や明るさが少し違うこともあるため、番号とサイズをよく確かめてから【購入】を押しましょう。"),
        p("支払いはマルチコピー機のその場で行うので、小銭や千円札を多めに持っていくとスムーズです。",
          "12人分をまとめて印刷するなら、混んでいない時間帯を選ぶと後ろの人を待たせずに済みます。"),
        h2("ほかの出演アーティストのファミマプリントも"),
        ui.minibox("<strong>出演アーティスト:</strong>全7組・102種類",
                   "<strong>JO1:</strong>同じLAPONE所属の先輩グループも18種類"),
        p("今回のファミマプリントには、KCON LA 2026に出演した7組が登場しています。"),
        ui.table("KCON LA 2026 ファミマプリントのラインナップ", [
            ("ALPHA DRIVE ONE", "6人×2種類=12種"),
            ("izna", "6人×2種類=12種"),
            ("JO1", "9人×2種類=18種"),
            ("KickFlip", "6人×2種類=12種"),
            ("KO1KEYZ", "12人×2種類=24種"),
            ("MODYSSEY", "7人×2種類=14種"),
            ("ZEROBASEONE", "5人×2種類=10種"),
        ]),
        p("7組の中でいちばん種類が多いのが、12人のKO1KEYZです。",
          "同じLAPONE ENTERTAINMENT所属の先輩・JO1も並んでいるので、両方を応援しているファンなら一緒に印刷するのもよさそうですね。"),
        p("KCON LA 2026の衣装のメンバーと写真が撮れるPHOTOGRAYのフレームも、10月31日まで原宿や全国の店舗で楽しめます。",
          f"場所や料金は{a(L(14098), 'KO1KEYZのPHOTOGRAYフレームの記事')}にまとめているので、あわせてチェックしてみてください。"),
        h2("まとめ"),
        ui.summary([
            "KCON LA 2026のKO1KEYZの写真がファミマプリントのブロマイドに",
            "販売期間は2026年10月16日(金)〜11月30日(月)23:59",
            "L判1枚200円・2L判1枚300円(税込)",
            "12人×2種類=24種、#1は白背景のポートレート、#2はステージ写真",
            "プリント番号はKKC1038003〜KKC1038026",
            "番号入力かQRコードで、ファミリーマートのマルチコピー機から買える",
            "写真プリントに対応していない店舗では買えないので事前に検索を",
        ]),
        p("デビュー前、12人で立ったKCON LAのステージは、ファンにとっても忘れられない夏の思い出です。",
          "近くのファミリーマートで、推しの1枚を印刷しに行ってみてはいかがでしょうか！"),
        ui.quotebox("あわせて読みたい", [a(u, t) for u, t in REL["ja"]]),
    ]
    jp_sum = ("KCON LA 2026のKO1KEYZの写真がファミマプリントに。10/16〜11/30 23:59、L判200円・2L判300円、12人×2種類の24種。"
              "プリント番号一覧と、マルチコピー機での買い方・注意点をまとめました。")

    # ---------------- KR ----------------
    kr_title = "KO1KEYZ 파미마 프린트 언제까지? 가격·종류 총정리!"
    kr = [
        p("8월 미국 로스앤젤레스에서 열린 KCON LA 2026에서 촬영된 KO1KEYZ(코이키즈) 사진을 일본 패밀리마트에서 살 수 있게 됐어요.",
          f"편의점 멀티 복사기로 인쇄하는 '파미마 프린트(famima PRINT)' 브로마이드로, 판매 기간은 {mk('2026년 10월 16일(금)~11월 30일(월) 23시 59분')}이에요.",
          f"가격은 {mk('L판 1장 200엔·2L판 1장 300엔(세금 포함)')}이고, 12명 각각 2종씩 총 24종이 준비되어 있어요.",
          "이 글에서는 어떤 사진인지, 멤버별 프린트 번호, 멀티 복사기에서 사는 방법과 주의할 점까지 정리했어요."),
        ui.table("KCON LA 2026 파미마 프린트 기본 정보", [
            ("판매 기간", "2026년 10월 16일(금)~11월 30일(월) 23:59(일본 시간)"),
            ("상품", "브로마이드(단면) L판·2L판"),
            ("가격", "L판 1장 200엔/2L판 1장 300엔(세금 포함)"),
            ("KO1KEYZ", "12명×2종(#1·#2)=24종"),
            ("출연 아티스트", "ALPHA DRIVE ONE·izna·JO1·KickFlip·KO1KEYZ·MODYSSEY·ZEROBASEONE(총 102종)"),
            ("구매 장소", "일본 전국 패밀리마트(사진 인쇄가 되는 멀티 복사기가 있는 매장)"),
            ("발표", "KCON USA 공식 X(2026년 10월 17일)"),
        ]),
        ui.titlebox("이 글에서 알 수 있는 것", [
            "어떤 사진을 살 수 있을까?", "판매 기간과 가격", "12명의 프린트 번호 목록",
            "멀티 복사기에서 사는 방법", "사기 전 주의할 점", "다른 출연 아티스트"]),
        h2("KO1KEYZ KCON LA 2026 파미마 프린트란? 어떤 사진?"),
        ui.minibox("<strong>내용:</strong>KCON LA 2026에서 촬영된 멤버 브로마이드",
                   "<strong>종류:</strong>멤버마다 #1(흰 배경 포트레이트)과 #2(무대 사진) 2종"),
        p("KCON USA 공식 X는 10월 17일 'KCON LA 2026의 감동을 다시 한번'이라며 파미마 프린트 판매 시작을 알렸어요.",
          "공지 이미지에는 '10/16(금)~11/30(월)'이라는 기간과 출연한 7팀의 로고가 들어 있어요."),
        embed(TW, "ko"),
        p("KO1KEYZ가 KCON LA 2026 무대에 선 건 8월 14일(금)이에요.",
          "10월 7일 데뷔보다 앞선, 12명에게 처음으로 큰 해외 무대였죠.",
          "그날의 모습이 일본 편의점에서 손에 쥘 수 있는 사진이 되어 돌아온 셈이에요."),
        p(f"파미마 프린트 공식 페이지에서 샘플을 보면 {mk('#1은 흰 배경에서 찍은 포트레이트, #2는 무대 위 라이브 사진')}으로 나뉘어 있어요.",
          "#1은 네이비×화이트 유니폼 스타일 의상을 입고, 턱에 손을 대거나 가슴 앞에 두는 등 한 명씩 포즈를 취한 클로즈업 컷이에요.",
          "#2는 퍼포먼스 중인 컷으로, 유니폼 의상의 멤버도 있고 붉은 배경에서 흰 의상을 입고 노래하는 멤버도 있어요."),
        p("모든 사진 오른쪽 아래에 'KCON LA 2026' 로고가 들어가 있어서 이벤트 기념품 느낌이 나요.",
          f"유니폼 가슴의 등번호 '07' '10' '26'에 담긴 의미는 {a(L(12673), 'KCON LA 2026 의상 등번호 정리 글')}에서 소개하고 있어요.",
          "멋진 표정의 #1과 무대의 열기가 전해지는 #2를 나란히 장식해 두는 것도 좋겠어요."),
        h2("언제까지 살 수 있을까? 판매 기간과 가격"),
        ui.minibox("<strong>기간:</strong>2026년 10월 16일(금)~11월 30일(월) 23시 59분",
                   "<strong>가격:</strong>L판 1장 200엔/2L판 1장 300엔(세금 포함)"),
        p(f"판매 기간은 {mk('11월 30일(월) 23시 59분까지')}로 약 한 달 반이에요.",
          "공지는 10월 17일이었지만 판매 자체는 하루 전인 16일부터 시작됐어요."),
        p("사이즈는 일반 사진과 같은 L판(89×127mm)과 한 단계 큰 2L판(127×178mm) 두 가지예요.",
          "둘 다 단면 인쇄이고, 탑로더나 포토 프레임에 넣을 거라면 L판, 방에 장식할 거라면 2L판이 쓰기 좋아요."),
        ui.table("한꺼번에 사면 얼마?(세금 포함)", [
            ("1명분(2종)", "L판 400엔/2L판 600엔"),
            ("12명분(24종)", "L판 4,800엔/2L판 7,200엔"),
        ]),
        p("최애 1명의 2종이면 L판으로 400엔이에요.",
          "12명 24종을 모두 모아도 L판이면 4,800엔이라, 동네 편의점에서 컴플리트할 수 있다는 게 반가운 포인트예요."),
        p("5월에 열린 KCON JAPAN 2026의 브로마이드도 7월 한 달 동안 파미마 프린트에서 판매됐고, 가격은 이번과 같은 L판 200엔·2L판 300엔이었어요.",
          "판매가 끝나면 다시 살 방법이 없고, 중고 거래 앱에서 정가보다 비싸게 거래되기도 해요.",
          "갖고 싶은 사진이 있다면 기간 안에 인쇄해 두는 게 확실해요."),
        h2("KO1KEYZ 12명의 프린트 번호 목록"),
        ui.minibox("<strong>프린트 번호:</strong>KKC1038003~KKC1038026(12명×2종)",
                   "<strong>사용법:</strong>멀티 복사기에 번호를 입력하면 그 사진을 바로 고를 수 있음"),
        p("멀티 복사기에서는 상품마다 정해진 '프린트 번호'를 입력하면 원하는 사진으로 바로 갈 수 있어요.",
          "KO1KEYZ 24종의 번호는 아래와 같아요.",
          "번호를 누르면 파미마 프린트 상품 페이지(샘플 이미지·QR코드 포함)가 열려요."),
        ui.table("KO1KEYZ 프린트 번호(#1=포트레이트/#2=무대)", number_rows()),
        p(f"다른 출연 아티스트까지 포함한 목록은 {a(FP, '파미마 프린트 KCON LA 2026 페이지')}에서 볼 수 있어요.",
          "랜덤 판매가 아니라 사진을 직접 골라서 사는 방식이라, 최애의 번호만 메모해 두면 돼요."),
        h2("파미마 프린트 사는 방법은? 멀티 복사기 순서"),
        ui.minibox("<strong>방법 1:</strong>프린트 번호를 입력해서 구매",
                   "<strong>방법 2:</strong>상품 페이지의 QR코드를 읽혀서 구매"),
        p("파미마 프린트는 일본 패밀리마트 매장 안에 있는 멀티 복사기에서 구매해요.",
          "온라인 판매는 없어서 매장에 직접 가서 인쇄해야 해요.",
          "화면은 일본어지만 순서는 단순하니, 일본 여행 중에 들러 보는 것도 방법이에요."),
        steps("프린트 번호로 사는 순서", [
            "멀티 복사기 화면 오른쪽 아래의 파란 테두리를 터치",
            "콘텐츠 서비스의 【famima PRINT】를 터치하고 이용 약관에 동의",
            "【プリント番号入力(프린트 번호 입력)】을 터치하고 원하는 사진 번호(KKC1038~)를 입력",
            "사이즈(L판/2L판)와 매수를 고르고 【購入(구매)】를 터치",
            "프린트 배출구에서 사진이 나옴",
        ]),
        p(f"또 하나는 {mk('상품 페이지의 QR코드를 이용하는 방법')}이에요.",
          "스마트폰으로 상품 페이지를 열고 QR코드(스크린샷도 OK)를 준비해 두면 번호를 입력하는 수고를 덜 수 있어요."),
        steps("QR코드로 사는 순서", [
            "사고 싶은 상품 페이지를 열어 QR코드를 띄운다",
            "멀티 복사기 화면 오른쪽의 '2次元コードを持っている(2차원 코드를 가지고 있다)'를 터치",
            "코드 리더에 QR코드를 대고 동의 사항을 확인한 뒤 '同意する(동의)'",
            "사이즈와 매수를 확인하고 【購入(구매)】를 터치",
        ]),
        p(f"자세한 조작은 {a(FP_USAGE, '파미마 프린트 이용 가이드')}와 {a(FP_QR, 'QR코드 이용 방법')}에 화면 사진과 함께 나와 있어요."),
        h2("사기 전에 알아 둘 주의할 점"),
        ui.minibox("<strong>매장:</strong>사진 인쇄가 안 되는 멀티 복사기에서는 구매 불가",
                   "<strong>반품:</strong>인쇄 불량이 아닌 이상 교환·환불 불가"),
        p(f"주의할 점은 {mk('모든 패밀리마트에서 살 수 있는 건 아니라는 것')}이에요.",
          "사진 인쇄를 지원하지 않는 멀티 복사기나, 동전 넣는 부분이 가늘고 작은 타입의 멀티 복사기에서는 파미마 프린트를 이용할 수 없어요."),
        p(f"가기 전에 {a(STORE, '편의점 매장 검색')}에서 '写真プリント(L判)' '写真プリント(2L判)' 'ファミリーマート'에 체크해서 찾아보면 지원하는 매장만 표시돼요.",
          "2L판을 원한다면 2L판까지 지원하는지 확인해 두면 안심이에요."),
        p("또 인쇄된 상품은 인쇄상 불량이 있는 경우를 제외하고 교환이나 환불이 안 돼요.",
          "스마트폰 화면의 샘플과 실제 사진은 색감이나 밝기가 조금 다를 수 있으니, 번호와 사이즈를 잘 확인한 뒤 【購入】를 누르세요."),
        p("결제는 멀티 복사기에서 바로 하기 때문에 동전이나 1,000엔 지폐를 넉넉히 챙겨 가면 편해요.",
          "12명분을 한꺼번에 인쇄할 거라면 붐비지 않는 시간대를 고르면 뒷사람을 기다리게 하지 않아도 돼요."),
        h2("다른 출연 아티스트의 파미마 프린트도"),
        ui.minibox("<strong>출연 아티스트:</strong>총 7팀·102종",
                   "<strong>JO1:</strong>같은 LAPONE 소속 선배 그룹도 18종"),
        p("이번 파미마 프린트에는 KCON LA 2026에 출연한 7팀이 등장해요."),
        ui.table("KCON LA 2026 파미마 프린트 라인업", [
            ("ALPHA DRIVE ONE", "6명×2종=12종"),
            ("izna", "6명×2종=12종"),
            ("JO1", "9명×2종=18종"),
            ("KickFlip", "6명×2종=12종"),
            ("KO1KEYZ", "12명×2종=24종"),
            ("MODYSSEY", "7명×2종=14종"),
            ("ZEROBASEONE", "5명×2종=10종"),
        ]),
        p("7팀 중 가장 종류가 많은 건 12명의 KO1KEYZ예요.",
          "같은 LAPONE ENTERTAINMENT 소속 선배 JO1도 있어서, 두 그룹을 모두 응원하는 팬이라면 함께 인쇄해도 좋겠어요."),
        p("KCON LA 2026 의상을 입은 멤버와 사진을 찍을 수 있는 PHOTOGRAY 프레임도 10월 31일까지 하라주쿠와 일본 각지 매장에서 즐길 수 있어요.",
          f"장소와 가격은 {a(L(14099), 'KO1KEYZ PHOTOGRAY 프레임 글')}에 정리해 두었으니 함께 확인해 보세요."),
        h2("정리"),
        ui.summary([
            "KCON LA 2026 KO1KEYZ 사진이 파미마 프린트 브로마이드로",
            "판매 기간은 2026년 10월 16일(금)~11월 30일(월) 23:59",
            "L판 1장 200엔·2L판 1장 300엔(세금 포함)",
            "12명×2종=24종, #1은 흰 배경 포트레이트, #2는 무대 사진",
            "프린트 번호는 KKC1038003~KKC1038026",
            "번호 입력 또는 QR코드로 일본 패밀리마트 멀티 복사기에서 구매",
            "사진 인쇄가 안 되는 매장도 있으니 미리 검색",
        ]),
        p("데뷔 전 12명이 함께 선 KCON LA 무대는 팬들에게도 잊지 못할 여름의 추억이에요.",
          "일본에 갈 일이 있다면 가까운 패밀리마트에서 최애의 한 장을 인쇄해 보는 건 어떨까요!"),
        ui.quotebox("함께 읽으면 좋은 글", [a(u, t) for u, t in REL["ko"]]),
    ]
    kr_sum = ("KCON LA 2026 KO1KEYZ 사진이 일본 파미마 프린트에. 10/16~11/30 23:59, L판 200엔·2L판 300엔, 12명×2종 24종. "
              "프린트 번호 목록과 멀티 복사기 구매 방법·주의점을 정리했어요.")

    # ---------------- EN ----------------
    en_title = "KO1KEYZ FamiMa Print: Until When? Price & Photos!"
    en = [
        p("Photos of KO1KEYZ taken at KCON LA 2026, held in Los Angeles in August, can now be bought at FamilyMart in Japan.",
          f"They're \"FamiMa Print\" bromides that you print on the store's multi-copy machine, on sale {mk('from October 16 (Fri) to November 30 (Mon), 2026, 23:59 JST')}.",
          f"Prices are {mk('200 yen for an L-size print and 300 yen for a 2L-size print (tax included)')}, with two photos for each of the 12 members, 24 in total.",
          "This article covers what the photos look like, each member's print number, and how to buy them at the multi-copy machine."),
        ui.table("KCON LA 2026 FamiMa Print at a glance", [
            ("Sale period", "October 16 (Fri) - November 30 (Mon), 2026, 23:59 JST"),
            ("Item", "Single-sided bromide, L size or 2L size"),
            ("Price", "L 200 yen / 2L 300 yen per print (tax included)"),
            ("KO1KEYZ", "12 members x 2 photos (#1, #2) = 24"),
            ("Artists", "ALPHA DRIVE ONE, izna, JO1, KickFlip, KO1KEYZ, MODYSSEY, ZEROBASEONE (102 photos in total)"),
            ("Where", "FamilyMart stores in Japan with a photo-print-capable multi-copy machine"),
            ("Announced by", "KCON USA official X (October 17, 2026)"),
        ]),
        ui.titlebox("What you'll learn", [
            "What the photos look like", "Sale period and price", "Print numbers for all 12 members",
            "How to buy at the multi-copy machine", "Things to check first", "The other artists"]),
        h2("What is the KO1KEYZ KCON LA 2026 FamiMa Print?"),
        ui.minibox("<strong>Contents:</strong>bromides of the members shot at KCON LA 2026",
                   "<strong>Types:</strong>#1 (portrait on a white background) and #2 (stage shot) for each member"),
        p("On October 17, KCON USA's official X announced the FamiMa Print release with the line \"relive the excitement of KCON LA 2026.\"",
          "The announcement image shows the dates, 10/16 (Fri) - 11/30 (Mon), along with the logos of the seven groups."),
        embed(TW, "en"),
        p("KO1KEYZ took the KCON LA 2026 stage on August 14 (Fri).",
          "It came before their October 7 debut and was the 12 members' first big overseas stage.",
          "Now that day is back as photos you can hold in your hand, printed at a Japanese convenience store."),
        p(f"Looking at the samples on the official FamiMa Print page, {mk('#1 is a portrait shot against a white background and #2 is a live shot on stage')}.",
          "In #1, each member wears the navy-and-white football-jersey outfit and strikes a close-up pose, hand to chin or over the chest.",
          "#2 captures them mid-performance: some in the jersey outfit, others singing in white outfits against a red backdrop."),
        p("Every photo carries the KCON LA 2026 logo in the bottom-right corner, so it feels like a proper event souvenir.",
          f"We explain the jersey numbers 07, 10 and 26 in {a(L(12675), 'our article on the KCON LA 2026 outfits')}.",
          "Displaying the posed #1 next to the high-energy #2 would make a nice pair."),
        h2("Until when can you buy them? Dates and price"),
        ui.minibox("<strong>Dates:</strong>October 16 (Fri) - November 30 (Mon), 2026, 23:59 JST",
                   "<strong>Price:</strong>L 200 yen / 2L 300 yen per print (tax included)"),
        p(f"The sale runs {mk('until 23:59 on November 30 (Mon)')}, about a month and a half.",
          "The announcement came on October 17, but sales had already started the day before, on the 16th."),
        p("There are two sizes: L (89 x 127 mm), the standard photo size, and the larger 2L (127 x 178 mm).",
          "Both are single-sided. L fits toploaders and small photo frames, while 2L is better for displaying on a wall or shelf."),
        ui.table("How much for a full set? (tax included)", [
            ("One member (2 photos)", "L 400 yen / 2L 600 yen"),
            ("All 12 members (24 photos)", "L 4,800 yen / 2L 7,200 yen"),
        ]),
        p("Both photos of your bias come to 400 yen in L size.",
          "Even the full 24-photo set is 4,800 yen in L size, and you can complete it at your neighborhood convenience store."),
        p("The KCON JAPAN 2026 bromides were also sold on FamiMa Print for one month in July, at the same 200 yen / 300 yen prices.",
          "Once the sale ends there's no way to buy them again, and they sometimes appear on resale apps above the original price.",
          "If there's a photo you want, printing it during the sale period is the safe choice."),
        h2("Print numbers for all 12 KO1KEYZ members"),
        ui.minibox("<strong>Print numbers:</strong>KKC1038003 - KKC1038026 (12 members x 2)",
                   "<strong>How to use:</strong>enter the number on the multi-copy machine to go straight to that photo"),
        p("On the multi-copy machine, entering an item's print number takes you straight to the photo you want.",
          "Here are the numbers for all 24 KO1KEYZ photos.",
          "Tap a number to open its FamiMa Print item page, with a sample image and QR code."),
        ui.table("KO1KEYZ print numbers (#1 = portrait / #2 = stage)", number_rows()),
        p(f"The full list including the other artists is on {a(FP, 'the FamiMa Print KCON LA 2026 page')}.",
          "It isn't a random draw; you choose the exact photo, so just note down your bias's numbers."),
        h2("How do you buy FamiMa Print? Steps at the machine"),
        ui.minibox("<strong>Option 1:</strong>enter the print number",
                   "<strong>Option 2:</strong>scan the QR code from the item page"),
        p("FamiMa Print is sold through the multi-copy machines inside FamilyMart stores in Japan.",
          "There's no online shop, so you need to go to a store and print it there.",
          "The screens are in Japanese, but the steps are simple, so it's a fun stop if you're visiting Japan."),
        steps("Buying with a print number", [
            "Touch the blue frame at the bottom right of the machine's screen",
            "Touch [famima PRINT] under content services and agree to the terms",
            "Touch [プリント番号入力] (enter print number) and type the number (KKC1038...)",
            "Choose the size (L/2L) and quantity, then touch [購入] (buy)",
            "The photo comes out of the print slot",
        ]),
        p(f"The other way is to {mk('use the QR code on the item page')}.",
          "Open the item page on your phone and have the QR code ready (a screenshot works too), and you won't need to type anything."),
        steps("Buying with a QR code", [
            "Open the item page you want and display its QR code",
            "Touch \"2次元コードを持っている\" (I have a 2D code) on the right side of the screen",
            "Hold the QR code to the reader, check the terms and touch \"同意する\" (agree)",
            "Check the size and quantity, then touch [購入] (buy)",
        ]),
        p(f"Step-by-step screenshots are in {a(FP_USAGE, 'the FamiMa Print user guide')} and {a(FP_QR, 'the QR code guide')}."),
        h2("Things to check before you go"),
        ui.minibox("<strong>Stores:</strong>machines that can't print photos won't sell it",
                   "<strong>Returns:</strong>no exchanges or refunds unless there's a printing defect"),
        p(f"Keep in mind that {mk('not every FamilyMart can sell these prints')}.",
          "FamiMa Print isn't available on multi-copy machines without photo printing, or on the type with a narrow, small coin slot section."),
        p(f"Before heading out, search the {a(STORE, 'convenience store finder')} with \"写真プリント(L判)\", \"写真プリント(2L判)\" and \"ファミリーマート\" checked to show only compatible stores.",
          "If you want 2L prints, make sure the store supports 2L as well."),
        p("Printed items also can't be exchanged or refunded unless there's a printing defect.",
          "Colors and brightness may look slightly different from the sample on your phone, so double-check the number and size before touching [購入]."),
        p("You pay right at the machine, so bringing coins and 1,000-yen bills makes things smoother.",
          "If you're printing all 12 members at once, picking a quiet time means you won't keep people waiting behind you."),
        h2("FamiMa Prints of the other KCON LA artists"),
        ui.minibox("<strong>Artists:</strong>7 groups, 102 photos",
                   "<strong>JO1:</strong>the senior group from the same agency, LAPONE, has 18"),
        p("This FamiMa Print release features seven groups that performed at KCON LA 2026."),
        ui.table("KCON LA 2026 FamiMa Print lineup", [
            ("ALPHA DRIVE ONE", "6 members x 2 = 12"),
            ("izna", "6 members x 2 = 12"),
            ("JO1", "9 members x 2 = 18"),
            ("KickFlip", "6 members x 2 = 12"),
            ("KO1KEYZ", "12 members x 2 = 24"),
            ("MODYSSEY", "7 members x 2 = 14"),
            ("ZEROBASEONE", "5 members x 2 = 10"),
        ]),
        p("With 12 members, KO1KEYZ has the most photos of the seven groups.",
          "JO1, their senior group at LAPONE ENTERTAINMENT, is in the lineup too, so fans of both can print them together."),
        p("The PHOTOGRAY frame that lets you pose with members in their KCON LA 2026 outfits is also available until October 31 in Harajuku and at stores across Japan.",
          f"See {a(L(14100), 'our KO1KEYZ PHOTOGRAY frame article')} for locations and prices."),
        h2("Summary"),
        ui.summary([
            "KO1KEYZ's KCON LA 2026 photos are now FamiMa Print bromides",
            "On sale October 16 (Fri) - November 30 (Mon), 2026, 23:59 JST",
            "200 yen for L size, 300 yen for 2L size (tax included)",
            "12 members x 2 = 24 photos: #1 is a white-background portrait, #2 a stage shot",
            "Print numbers KKC1038003 - KKC1038026",
            "Buy by print number or QR code at FamilyMart multi-copy machines in Japan",
            "Some stores can't print photos, so search for a compatible one first",
        ]),
        p("The KCON LA stage the 12 stood on before their debut is a summer memory fans won't forget.",
          "If you're in Japan, why not stop by a FamilyMart and print your bias's photo!"),
        ui.quotebox("Related articles", [a(u, t) for u, t in REL["en"]]),
    ]
    en_sum = ("KO1KEYZ's KCON LA 2026 photos are on FamiMa Print in Japan, Oct 16-Nov 30 23:59 JST: 200 yen (L) / 300 yen (2L), 24 photos. "
              "Print numbers for all 12 members and how to buy at the machine.")
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
    subprocess.run([sys.executable, tool, "--top", "KCON LAの写真がファミマに！", "--main", "KO1KEYZ",
                    "--bottom", "ファミマプリントはいつまで？", "--out", str(EYE_JP), "--seed", "1016"], check=True)
    subprocess.run([sys.executable, tool, "--top", "KCON LA 사진이 파미마에!", "--main", "KO1KEYZ",
                    "--bottom", "파미마 프린트 언제까지?", "--out", str(EYE_KR), "--seed", "1016", "--lang", "kr"], check=True)


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
