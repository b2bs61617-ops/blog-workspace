# -*- coding: utf-8 -*-
"""KO1KEYZのグループカラーは黄色？LAPOSTA 2027の宝箱の宝石6色を、過去のLAPOSTAの色分けと照らして検証。
chomoand-1.com に JP/KR/EN の下書きを作る(author=momo)。2026-11-04 オシリ依頼。

一次ソース:
- LAPONE公式X https://x.com/lapone_info/status/2117814102752166036 (2026-11-04 12:00 JST、FC会員先行スタート告知。宝の地図ビジュアル)
  宝箱の宝石 = 赤・紫・青(青紫)・水色・黄・ピンクの6個(拡大して確認)
- 特設サイト https://lapone.jp/feature/laposta2027 (BOYS/GIRLSのアーティスト写真 ph_artist_boys/girls)
  BOYS: 白×黄=12人(KO1KEYZ)/デニム水色=6人(DXTEEN)/赤系と紺・黒系の2組(人数・並びから赤=JO1、紺=INIとみられる)
  GIRLS: ピンク(ME:I)/紫4人(IS:SUE)
- LAPOSTA 2025 OFFICIAL GOODS一覧画像: マフラータオル・番号・トレカ包装がJO1赤/INI青/DXTEEN緑/ME:Iピンク/IS:SUE紫
- 知恵袋(2024/10): 前年のLAPOSTAグッズはJO1赤・INI青・DXTEEN緑 / 各グループの公式グループカラーは未決定
- 公式ペンライト: JO1=JAM瓶型(初代は青アクセント)、INI=水色・紫・ピンクのリング、DXTEEN=青アクセント(note redshiso)
- KO1KEYZのメンカラ黄色=杉山竜司(RYUJI)(既存記事10196/10544)
- X: 11/4にファンが「ラポスタカラー」を整理(KO1KEYZ=黄、DXTEEN=緑→水色?)。10/30にも衣装を見て「イエロー？」の声

python build_and_post_ko1keyz_group_color.py [--dry]
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

IMG = ROOT / "images" / "ko1keyz_group_color"
EYE = ROOT / "images" / "ko1keyz_group_color_eyecatch.png"
BASE_SLUG = "ko1keyz-group-color-laposta"

TW = "https://twitter.com/lapone_info/status/2117814102752166036"
TW_URL = "https://x.com/lapone_info/status/2117814102752166036"
SITE = "https://lapone.jp/feature/laposta2027"

L = lambda pid: f"https://chomoand-1.com/?p={pid}"
REL = {
    "ja": [(L(15186), "KO1KEYZ初のLAPOSTA 2027！FC先行はいつまで？"),
           (L(10196), "KO1KEYZ（コイキーズ）のメンバーカラーまとめ！担当カラーは何色？"),
           (L(10544), "JO1・INI・DXTEEN・KO1KEYZメンカラまとめ！")],
    "ko": [(L(15187), "KO1KEYZ 첫 LAPOSTA 2027! FC 선행은 언제까지?")],
    "en": [(L(15188), "KO1KEYZ's First LAPOSTA 2027: Dates, Tickets & FC")],
}

ui = Ui("#8a8378", "#ddd9d3", "#f7f6f4", "rgba(138,131,120,0.06)")


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def embed(lang):
    return wphtml(f'<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{TW}">{TW}</a></blockquote>\n'
                  '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def fig(m, alt, cap):
    if m is None:  # dry run
        return wphtml(f"<figure>[{alt}]<figcaption>{cap}</figcaption></figure>")
    sz = m["media_details"].get("sizes", {})
    full = {"source_url": m["source_url"], "width": m["media_details"]["width"], "height": m["media_details"]["height"]}
    lg = sz.get("large", full)
    md = sz.get("medium", lg)
    srcset = ", ".join(f'{s["source_url"]} {s["width"]}w' for s in (md, lg, full))
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{lg["source_url"]}" alt="{alt}" width="{lg["width"]}" height="{lg["height"]}" style="max-width:100%;height:auto;" srcset="{srcset}" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption>出典:{cap}</figcaption>
</figure>''')


def build(md):
    chest, boys, girls = md.get("chest"), md.get("boys"), md.get("girls")

    # ---------------- JP ----------------
    jp_title = "KO1KEYZのグループカラーは黄色？ラポスタの宝石6色を検証！"
    jp = [
        p("11月4日の正午、LAPONEの合同ライブ『LAPOSTA 2027』の新しいビジュアルが公開されました。",
          "宝の地図の真ん中にある島には宝箱が置かれ、中に6色の宝石が入っています。",
          "出演は6グループなので、ファンの間では「宝石は各グループの色なのでは？」「KO1KEYZ(コイキーズ)は黄色？」と話題になっています。"),
        p(f"結論から言うと、{mk('KO1KEYZのグループカラーが黄色だと公式に発表されたわけではありません')}。",
          f"ただ、過去のLAPOSTAで各グループに割り当てられてきた色と照らし合わせると、{mk('残る黄色がKO1KEYZの色である可能性はかなり高い')}と言えます。",
          "この記事では、宝石の色と過去のLAPOSTAのグッズ、今回の衣装の3つから、6グループの色を1つずつ確かめていきます。"),
        ui.table("LAPOSTA 2027の色分け(予想)", [
            ("JO1", "赤(2025年のLAPOSTAグッズも赤)"),
            ("INI", "青(2025年のLAPOSTAグッズも青)"),
            ("DXTEEN", "水色？(2025年は緑)"),
            ("KO1KEYZ", "黄色？(今回が初出演)"),
            ("ME:I", "ピンク(2025年のLAPOSTAグッズもピンク)"),
            ("IS:SUE", "紫(2025年のLAPOSTAグッズも紫)"),
        ]),
        ui.titlebox("この記事でわかること", [
            "LAPOSTA 2027の宝箱に入っている宝石の色", "過去のLAPOSTAでのグループごとの色分け",
            "KO1KEYZが黄色だと考えられる3つの理由", "DXTEENが緑から水色に変わった？という疑問",
            "各グループの公式グループカラーは決まっている？"]),

        h2("LAPOSTA 2027の宝箱の宝石は何色？"),
        ui.minibox("<strong>公開日:</strong>2026年11月4日(水)12:00(FC会員先行スタートの告知)",
                   "<strong>宝箱の宝石:</strong>赤・紫・青・水色・黄・ピンクの6色"),
        p("このビジュアルは、LAPONE ENTERTAINMENTの公式Xが、LAPOSTA 2027のFC会員先行スタートを知らせる投稿で使ったものです。",
          "金色の宝の地図に、JO1・INI・DXTEEN・KO1KEYZ・ME:I・IS:SUEの6隻の船が描かれ、真ん中の島を囲んでいます。",
          "今回のテーマ「TREASURE THE MOMENT」にちなんだ、宝探しの世界観です。"),
        embed("ja"),
        p("島の中心に置かれた宝箱を拡大すると、2段に並んだ宝石は6個。",
          f"上の段が{mk('赤・紫・青')}、下の段が{mk('水色・黄・ピンク')}です。",
          "青は少し紫がかった青で、紫とは別の色として描き分けられています。"),
        fig(chest, "LAPOSTA 2027のビジュアルの宝箱。赤・紫・青・水色・黄・ピンクの宝石が入っている", TW_URL),
        p("6隻の船に対して宝石も6個なので、1グループに1色ずつ割り当てられていると考えるのが自然です。",
          "ちなみに、島に立っている旗はLAPOSTAのロゴ入りのオレンジ。",
          "オレンジはLAPONE全体のイメージカラーとしてロゴや告知画像に使われている色で、宝石には入っていません。"),

        h2("過去のLAPOSTAのグループカラーは？"),
        ui.minibox("<strong>2025年:</strong>JO1=赤/INI=青/DXTEEN=緑/ME:I=ピンク/IS:SUE=紫",
                   "<strong>2024年:</strong>JO1=赤/INI=青/DXTEEN=緑(ファンの証言)"),
        p("LAPOSTAでは、グループごとに色を決めてグッズを作り分けてきました。",
          f"東京ドームで開かれた2025年のオフィシャルグッズを見ると、{mk('JO1が赤、INIが青、DXTEENが緑、ME:Iがピンク、IS:SUEが紫')}。",
          "マフラータオルの地色やトレーディングカードの包装、商品番号の丸の色まで、この5色でそろえられていました。"),
        ui.table("LAPOSTA 2025のグッズの色", [
            ("JO1", "赤(マフラータオル・トレカ包装・商品番号)"),
            ("INI", "青"),
            ("DXTEEN", "緑"),
            ("ME:I", "ピンク"),
            ("IS:SUE", "紫"),
        ]),
        p("その前年、Kアリーナ横浜で開かれた2024年についても、Yahoo!知恵袋には「去年のラポスタのグッズの色はJO1が赤、INIが青、DXTEENが緑だった」という回答が残っています。",
          "少なくとも2年続けて同じ色分けが使われてきたことになり、ファンの間では「ラポスタカラー」として定着しています。"),
        p(f"今回の宝石6色のうち、{mk('赤・青・ピンク・紫の4色は、2025年の色分けとぴったり重なります')}。",
          "残るのは黄色と水色の2色で、ここに新しく加わったKO1KEYZと、緑だったDXTEENが入ると考えられます。"),

        h2("KO1KEYZが黄色だと考えられる理由は？"),
        ui.minibox("<strong>理由1:</strong>宝石の中で、過去のLAPOSTAで使われていない色が黄色",
                   "<strong>理由2:</strong>アーティスト写真の衣装が白×黄色",
                   "<strong>理由3:</strong>DXTEENの衣装が水色系で、黄色と結びつかない"),
        p("1つ目の理由は、消去法です。",
          "宝石のうち、これまでのLAPOSTAでどのグループにも使われていなかった色は黄色と水色。",
          "そのうち水色は、後で触れるようにDXTEENの今回の衣装と重なるため、初出演のKO1KEYZに残るのは黄色になります。"),
        p(f"2つ目の理由は、特設サイトに載っている{mk('BOYS 4組のアーティスト写真')}です。",
          "洞窟の中に海賊風の衣装の4グループが並んでいて、上の段に座っている12人は白い衣装に黄色のネクタイやサッシュ(肩から斜めにかける帯)、黄色の手袋を合わせています。",
          "12人という人数から、この白×黄色のグループがKO1KEYZです。"),
        fig(boys, "LAPOSTA 2027のBOYSアーティスト写真。上段の12人が白×黄色、右側の6人がデニムの衣装", SITE),
        p("ほかの3組は、真ん中が赤い衣装、左側が紺や黒の衣装、右側の6人がデニムの衣装です。",
          "6人なのはDXTEENだけなので、デニムがDXTEEN。",
          "残りの2組は人数や並び方から、赤がJO1、紺がINIとみられ、2025年のグッズの色(JO1=赤・INI=青)ともそろっています。"),
        p("衣装の色がグループごとにはっきり分かれていて、その色が宝石とも重なっているのが今回のビジュアルの特徴です。",
          "公開された時点で、Xには衣装を見たファンから「グループカラーはイエロー？」という声が上がっていました。"),

        h2("DXTEENは緑から水色に変わった？"),
        ui.minibox("<strong>2025年:</strong>緑(グッズの色)",
                   "<strong>2027年:</strong>宝箱に緑の宝石は無し。衣装はデニムの水色"),
        p("今回いちばん意外だったのは、DXTEENの色です。",
          f"2025年は緑でしたが、{mk('宝箱の中には緑の宝石が入っていません')}。",
          "Xでも「DXTEENは緑だったはずなのになぜ？」「色が変わったの？」と戸惑う声が出ていました。"),
        p("宝箱の外にこぼれている宝石の中には緑っぽいものもありますが、箱の中の6個は前述のとおり水色。",
          "そして写真の衣装も、緑ではなく水色のデニムです。",
          "特設サイトに並ぶDXTEENのグループ写真も、水色のジャケットやニットでそろえた爽やかな雰囲気になっています。"),
        p(f"このため、{mk('LAPOSTA 2027ではDXTEENの色が緑から水色に変わった')}可能性があります。",
          "ただ、公式から色についての説明は出ていません。",
          "宝石の水色がたまたま青に近い色で描かれただけという見方もあり、グッズの詳細が発表されるまでは断定できません。"),

        h2("ME:IはピンクでIS:SUEは紫"),
        ui.minibox("<strong>ME:I:</strong>ピンクの宝石・ピンクの衣装",
                   "<strong>IS:SUE:</strong>紫の宝石・紫の衣装"),
        p("ガールズグループの2組は、2025年から色が変わっていないとみられます。",
          "GIRLSのアーティスト写真では、手前に並んだメンバーがピンクや白のドレス、後ろの段に立つ4人が紫の衣装です。",
          "IS:SUEは4人組なので、紫の4人がIS:SUE、ピンクがME:Iになります。"),
        fig(girls, "LAPOSTA 2027のGIRLSアーティスト写真。手前がピンク、後列の4人が紫の衣装", SITE),
        p("どちらも2025年のグッズの色(ME:I=ピンク、IS:SUE=紫)と同じで、宝石の色ともきれいに重なっています。"),

        h2("各グループの公式グループカラーは決まってる？"),
        ui.minibox("<strong>結論:</strong>JO1・INI・DXTEEN・ME:I・IS:SUEとも、グループカラーとして公式に発表された色は無い",
                   "<strong>LAPOSTAの色:</strong>合同ライブで見分けやすくするための色分けとみられる"),
        p("実は、LAPONEのグループには「グループカラーはこの色」と公式に発表されたものがありません。",
          "メンバーカラーは各グループで決まっていますが、グループ全体の色はファンの間でも意見が分かれていて、Yahoo!知恵袋でも「JO1は寒色、INIは暖色のイメージ」など人によって答えがバラバラです。"),
        p("公式ペンライトを見ても、JO1はファンネーム「JAM」にちなんだジャム瓶の形、INIは水色・紫・ピンクのリングが入った惑星のようなデザインで、どちらも1色に決まっているわけではありません。",
          "DXTEENのペンライトは青をアクセントにしたデザインですが、グループカラーとしての発表はありません。"),
        p(f"そのため、LAPOSTAの色分けは{mk('6グループが一度に出る合同ライブで、グッズや演出を見分けやすくするための色')}と考えるのが自然です。",
          "KO1KEYZについても、黄色はあくまで「LAPOSTAでの担当色」になりそうで、普段のグループカラーとは分けて考えた方がよさそうです。"),
        p(f"ちなみにKO1KEYZのメンバーカラーで黄色を担当しているのはRYUJIさん(杉山竜司さん)。",
          f"12人それぞれの色は{a(L(10196), 'KO1KEYZのメンバーカラーの記事')}にまとめています。"),

        h2("グッズで色が確定するのはいつ？"),
        p("LAPOSTAのオフィシャルグッズは、これまで公演の少し前に一覧が発表されてきました。",
          "2025年もマフラータオルやトレカの包装でグループごとの色がはっきり分かれていたので、2027年のグッズが出れば、KO1KEYZが本当に黄色なのか、DXTEENが水色になったのかが確定するはずです。"),
        p("なお、FC会員先行の受付は11月15日(日)23時59分までです。",
          f"日程やチケット代、申し込みの準備は{a(L(15186), 'KO1KEYZ初のLAPOSTA 2027の記事')}にまとめています。"),

        h2("まとめ"),
        ui.summary([
            "LAPOSTA 2027のビジュアルの宝箱には、赤・紫・青・水色・黄・ピンクの6色の宝石",
            "2025年のLAPOSTAはJO1=赤・INI=青・DXTEEN=緑・ME:I=ピンク・IS:SUE=紫",
            "過去に無かった黄色がKO1KEYZの色とみられ、衣装も白×黄色",
            "DXTEENは緑の宝石が無く、衣装も水色のデニムで水色に変わった可能性",
            "LAPONEのグループに公式のグループカラーは無く、LAPOSTAの色は合同ライブ用の色分け",
            "正式な色はグッズの発表で確定しそう",
        ]),
        p("初出演のKO1KEYZにも、先輩たちと並ぶ「自分たちの色」ができそうです。",
          "東京ドームと京セラドーム大阪の客席が6色に分かれる景色を楽しみに、グッズの発表を待ちましょう！"),
        ui.quotebox("あわせて読みたい", [a(u, t) for u, t in REL["ja"]]),
    ]
    jp_sum = ("LAPOSTA 2027のビジュアルの宝箱に6色の宝石。2025年のグッズの色分けと照らすと、"
              "初出演のKO1KEYZは黄色の可能性大。DXTEENは緑から水色に変わった？6グループの色を検証しました。")

    # ---------------- KR ----------------
    kr_title = "KO1KEYZ 그룹 컬러는 노란색? LAPOSTA 보석 6색 검증!"
    kr = [
        p("11월 4일 정오, LAPONE 합동 라이브 'LAPOSTA 2027'의 새 비주얼이 공개됐어요.",
          "보물 지도 한가운데 섬에 보물상자가 있고, 안에는 6가지 색의 보석이 들어 있어요.",
          "출연 그룹도 6팀이라서 팬들 사이에서는 '보석이 각 그룹 색 아니야?', 'KO1KEYZ는 노란색?'이라는 이야기가 나오고 있어요."),
        p(f"결론부터 말하면, {mk('KO1KEYZ의 그룹 컬러가 노란색이라고 공식 발표된 것은 아니에요')}.",
          f"다만 지금까지 LAPOSTA에서 그룹별로 정해 온 색과 비교해 보면, {mk('남는 노란색이 KO1KEYZ의 색일 가능성이 꽤 높아요')}.",
          "이 글에서는 보석 색, 과거 LAPOSTA 굿즈, 이번 의상 세 가지로 6팀의 색을 하나씩 확인해 볼게요."),
        ui.table("LAPOSTA 2027 색 구분(예상)", [
            ("JO1", "빨강(2025년 굿즈도 빨강)"),
            ("INI", "파랑(2025년 굿즈도 파랑)"),
            ("DXTEEN", "하늘색?(2025년은 초록)"),
            ("KO1KEYZ", "노랑?(이번이 첫 출연)"),
            ("ME:I", "핑크(2025년 굿즈도 핑크)"),
            ("IS:SUE", "보라(2025년 굿즈도 보라)"),
        ]),
        ui.titlebox("이 글에서 알 수 있는 것", [
            "LAPOSTA 2027 보물상자 속 보석 색", "과거 LAPOSTA의 그룹별 색 구분",
            "KO1KEYZ가 노란색으로 보이는 3가지 이유", "DXTEEN은 초록에서 하늘색으로 바뀌었을까?",
            "각 그룹의 공식 그룹 컬러가 있을까?"]),

        h2("LAPOSTA 2027 보물상자의 보석은 무슨 색?"),
        ui.minibox("<strong>공개:</strong>2026년 11월 4일(수) 12:00(FC 회원 선행 시작 안내)",
                   "<strong>보석:</strong>빨강·보라·파랑·하늘색·노랑·핑크 6색"),
        p("이 비주얼은 LAPONE ENTERTAINMENT 공식 X가 LAPOSTA 2027 FC 회원 선행 시작을 알리면서 올린 이미지예요.",
          "금색 보물 지도 위에 JO1·INI·DXTEEN·KO1KEYZ·ME:I·IS:SUE의 배 6척이 가운데 섬을 둘러싸고 있어요.",
          "이번 테마 'TREASURE THE MOMENT'에 맞춘 보물찾기 콘셉트예요."),
        embed("ko"),
        p("섬 가운데 보물상자를 확대해 보면 보석은 2줄로 6개.",
          f"윗줄이 {mk('빨강·보라·파랑')}, 아랫줄이 {mk('하늘색·노랑·핑크')}예요.",
          "파랑은 살짝 보랏빛이 도는 파랑이지만, 보라와는 다른 색으로 그려져 있어요."),
        fig(chest, "LAPOSTA 2027 비주얼의 보물상자. 빨강·보라·파랑·하늘색·노랑·핑크 보석", TW_URL),
        p("배 6척에 보석도 6개라서, 그룹마다 한 색씩 정해져 있다고 보는 게 자연스러워요.",
          "섬에 꽂힌 깃발은 LAPOSTA 로고가 들어간 오렌지색인데, 오렌지는 LAPONE 전체의 이미지 컬러로 쓰이는 색이라 보석에는 없어요."),

        h2("과거 LAPOSTA의 그룹 컬러는?"),
        ui.minibox("<strong>2025년:</strong>JO1=빨강/INI=파랑/DXTEEN=초록/ME:I=핑크/IS:SUE=보라",
                   "<strong>2024년:</strong>JO1=빨강/INI=파랑/DXTEEN=초록(팬 증언)"),
        p("LAPOSTA에서는 그룹마다 색을 정해 굿즈를 나눠 만들어 왔어요.",
          f"도쿄돔에서 열린 2025년 공식 굿즈를 보면 {mk('JO1 빨강, INI 파랑, DXTEEN 초록, ME:I 핑크, IS:SUE 보라')}.",
          "머플러 타월 바탕색, 트레이딩 카드 포장, 상품 번호의 동그라미 색까지 이 5가지 색으로 맞춰져 있었어요."),
        p("그 전 해인 2024년(K아레나 요코하마)에 대해서도, 일본 Q&A 사이트에 '작년 LAPOSTA 굿즈 색은 JO1 빨강, INI 파랑, DXTEEN 초록이었다'는 답변이 남아 있어요.",
          "적어도 2년 연속 같은 색 구분이 쓰였고, 팬들 사이에서는 '라포스타 컬러'로 자리 잡았어요."),
        p(f"이번 보석 6색 중 {mk('빨강·파랑·핑크·보라 4색은 2025년과 그대로 겹쳐요')}.",
          "남는 노랑과 하늘색에 새로 합류한 KO1KEYZ와, 초록이었던 DXTEEN이 들어간다고 볼 수 있어요."),

        h2("KO1KEYZ가 노란색으로 보이는 이유는?"),
        ui.minibox("<strong>이유1:</strong>보석 중 과거 LAPOSTA에서 안 쓰인 색이 노랑",
                   "<strong>이유2:</strong>아티스트 사진 의상이 화이트×노랑",
                   "<strong>이유3:</strong>DXTEEN 의상은 하늘색 계열이라 노랑과 연결되지 않음"),
        p("첫 번째는 소거법이에요.",
          "보석 중 지금까지 어느 그룹에도 쓰이지 않았던 색은 노랑과 하늘색.",
          "하늘색은 뒤에서 설명할 DXTEEN의 이번 의상과 겹치기 때문에, 첫 출연인 KO1KEYZ에게 남는 건 노랑이에요."),
        p(f"두 번째는 특설 사이트에 올라온 {mk('BOYS 4팀 아티스트 사진')}이에요.",
          "동굴 속에 해적풍 의상의 4팀이 모여 있는데, 위쪽에 앉은 12명은 흰 의상에 노란 넥타이와 띠, 노란 장갑을 맞췄어요.",
          "12명이라는 인원으로 볼 때 이 화이트×노랑 팀이 KO1KEYZ예요."),
        fig(boys, "LAPOSTA 2027 BOYS 아티스트 사진. 위쪽 12명이 화이트×노랑, 오른쪽 6명이 데님 의상", SITE),
        p("나머지 3팀은 가운데가 빨간 의상, 왼쪽이 네이비·블랙 의상, 오른쪽 6명이 데님 의상이에요.",
          "6명인 그룹은 DXTEEN뿐이라 데님이 DXTEEN.",
          "남은 두 팀은 인원과 위치로 보아 빨강이 JO1, 네이비가 INI로 보이며, 2025년 굿즈 색(JO1=빨강·INI=파랑)과도 맞아요."),

        h2("DXTEEN은 초록에서 하늘색으로 바뀌었을까?"),
        p("이번에 가장 의외였던 건 DXTEEN의 색이에요.",
          f"2025년에는 초록이었지만 {mk('보물상자 안에 초록 보석이 없어요')}.",
          "X에서도 'DXTEEN은 초록이었는데 왜?', '색이 바뀐 거야?'라는 반응이 나왔어요."),
        p("상자 밖에 흩어진 보석 중에는 초록빛이 도는 것도 있지만, 상자 안 6개는 하늘색이에요.",
          "사진 속 의상도 초록이 아니라 하늘색 데님이고, 특설 사이트의 DXTEEN 단체 사진도 하늘색 재킷과 니트로 맞춘 분위기예요."),
        p(f"그래서 {mk('LAPOSTA 2027에서는 DXTEEN의 색이 초록에서 하늘색으로 바뀌었을')} 가능성이 있어요.",
          "다만 공식 설명은 없고, 굿즈 상세가 나오기 전까지는 단정할 수 없어요."),

        h2("ME:I는 핑크, IS:SUE는 보라"),
        p("걸그룹 2팀은 2025년과 색이 그대로인 것으로 보여요.",
          "GIRLS 아티스트 사진에서 앞줄 멤버들은 핑크와 화이트 드레스, 뒷줄 4명은 보라색 의상이에요.",
          "IS:SUE는 4인조라서 보라 4명이 IS:SUE, 핑크가 ME:I예요."),
        fig(girls, "LAPOSTA 2027 GIRLS 아티스트 사진. 앞줄 핑크, 뒷줄 4명 보라 의상", SITE),
        p("두 팀 모두 2025년 굿즈 색(ME:I=핑크, IS:SUE=보라)과 같고, 보석 색과도 깔끔하게 겹쳐요."),

        h2("각 그룹의 공식 그룹 컬러는 정해져 있을까?"),
        p("사실 LAPONE 그룹들은 '그룹 컬러는 이 색'이라고 공식 발표한 적이 없어요.",
          "멤버 컬러는 그룹마다 정해져 있지만, 그룹 전체 색은 팬들 사이에서도 의견이 갈려요."),
        p("공식 응원봉도 JO1은 팬덤명 'JAM'에서 딴 잼 병 모양, INI는 하늘색·보라·핑크 링이 들어간 행성 같은 디자인으로, 한 가지 색으로 정해져 있지 않아요.",
          f"그래서 LAPOSTA의 색 구분은 {mk('6팀이 한꺼번에 나오는 합동 라이브에서 굿즈와 연출을 구분하기 위한 색')}으로 보는 게 자연스러워요."),
        p("참고로 KO1KEYZ 멤버 컬러에서 노랑 담당은 RYUJI예요.",
          "LAPOSTA 굿즈 목록이 발표되면 KO1KEYZ가 정말 노랑인지, DXTEEN이 하늘색이 됐는지 확정될 거예요.",
          f"일정과 티켓 정보는 {a(L(15187), 'KO1KEYZ 첫 LAPOSTA 2027 글')}에 정리했어요."),

        h2("정리"),
        ui.summary([
            "LAPOSTA 2027 비주얼 보물상자에 빨강·보라·파랑·하늘색·노랑·핑크 6색 보석",
            "2025년은 JO1=빨강·INI=파랑·DXTEEN=초록·ME:I=핑크·IS:SUE=보라",
            "과거에 없던 노랑이 KO1KEYZ의 색으로 보이며, 의상도 화이트×노랑",
            "DXTEEN은 초록 보석이 없고 의상도 하늘색 데님",
            "LAPONE 그룹에 공식 그룹 컬러는 없고, LAPOSTA 색은 합동 라이브용 구분",
            "정식 색은 굿즈 발표로 확정될 전망",
        ]),
        p("첫 출연인 KO1KEYZ에게도 선배들과 나란히 설 '우리만의 색'이 생길 것 같아요.",
          "돔 객석이 6색으로 나뉘는 모습을 기대하며 굿즈 발표를 기다려 봐요!"),
        ui.quotebox("함께 읽어 보세요", [a(u, t) for u, t in REL["ko"]]),
    ]
    kr_sum = ("LAPOSTA 2027 비주얼 보물상자에 6색 보석. 2025년 굿즈 색과 비교하면 첫 출연 KO1KEYZ는 노란색일 가능성이 높아요. "
              "DXTEEN은 초록에서 하늘색으로? 6팀의 색을 검증했어요.")

    # ---------------- EN ----------------
    en_title = "Is KO1KEYZ's Group Color Yellow? LAPOSTA's 6 Gems"
    en = [
        p("At noon on November 4, a new visual for LAPONE's joint concert LAPOSTA 2027 was released.",
          "In the middle of a treasure map sits an island with a treasure chest holding six colored gems.",
          "With six groups on the lineup, fans quickly started asking whether each gem stands for a group, and whether KO1KEYZ is yellow."),
        p(f"The short answer: {mk('there has been no official announcement that KO1KEYZ’s group color is yellow')}.",
          f"But when you compare the gems with the colors LAPOSTA has assigned to each group in past years, {mk('yellow is very likely KO1KEYZ’s color')}.",
          "Below, we check all six groups using the gems, past LAPOSTA merch and this year's costumes."),
        ui.table("LAPOSTA 2027 colors (our read)", [
            ("JO1", "Red (also red in 2025 merch)"),
            ("INI", "Blue (also blue in 2025 merch)"),
            ("DXTEEN", "Light blue? (green in 2025)"),
            ("KO1KEYZ", "Yellow? (first LAPOSTA)"),
            ("ME:I", "Pink (also pink in 2025 merch)"),
            ("IS:SUE", "Purple (also purple in 2025 merch)"),
        ]),
        ui.titlebox("What you'll learn", [
            "The gem colors in the LAPOSTA 2027 chest", "How past LAPOSTA editions color-coded each group",
            "Three reasons KO1KEYZ looks like yellow", "Did DXTEEN switch from green to light blue?",
            "Do LAPONE groups have official group colors?"]),

        h2("What colors are the gems in the chest?"),
        ui.minibox("<strong>Released:</strong>Wed, Nov 4, 2026, 12:00 JST (fan club presale announcement)",
                   "<strong>Gems:</strong>red, purple, blue, light blue, yellow, pink"),
        p("LAPONE ENTERTAINMENT's official X account used this visual in its post announcing the start of the LAPOSTA 2027 fan club presale.",
          "Six ships for JO1, INI, DXTEEN, KO1KEYZ, ME:I and IS:SUE surround the island on a golden map, matching this year's theme, \"TREASURE THE MOMENT.\""),
        embed("en"),
        p("Zoom in on the chest and you'll see six gems in two rows.",
          f"The top row is {mk('red, purple and blue')}; the bottom row is {mk('light blue, yellow and pink')}.",
          "The blue leans slightly violet, but it is clearly drawn as a different color from the purple."),
        fig(chest, "The treasure chest from the LAPOSTA 2027 visual with red, purple, blue, light blue, yellow and pink gems", TW_URL),
        p("Six ships and six gems makes one color per group the natural reading.",
          "The orange flag on the island carries the LAPOSTA logo; orange is LAPONE's overall brand color and isn't among the gems."),

        h2("What colors did past LAPOSTA editions use?"),
        ui.minibox("<strong>2025:</strong>JO1 = red / INI = blue / DXTEEN = green / ME:I = pink / IS:SUE = purple",
                   "<strong>2024:</strong>JO1 = red / INI = blue / DXTEEN = green (per fans)"),
        p("LAPOSTA has color-coded its merch by group.",
          f"The official goods for the 2025 Tokyo Dome shows used {mk('red for JO1, blue for INI, green for DXTEEN, pink for ME:I and purple for IS:SUE')}, down to the muffler towels, trading card packs and item number badges.",
          "Fans also recall the 2024 K-Arena Yokohama goods using the same red, blue and green for JO1, INI and DXTEEN."),
        p(f"Of this year's six gems, {mk('red, blue, pink and purple match the 2025 scheme exactly')}.",
          "That leaves yellow and light blue for newcomers KO1KEYZ and for DXTEEN, previously green."),

        h2("Why KO1KEYZ looks like yellow"),
        ui.minibox("<strong>Reason 1:</strong>yellow is the one gem color LAPOSTA hasn't used before",
                   "<strong>Reason 2:</strong>their costumes in the artist photo are white and yellow",
                   "<strong>Reason 3:</strong>DXTEEN's costumes are light blue, not yellow"),
        p("First, process of elimination: the only gem colors never used at LAPOSTA are yellow and light blue, and light blue lines up with DXTEEN's costumes this year.",
          f"Second, the {mk('BOYS artist photo')} on the official site shows four groups in pirate-style outfits inside a cave.",
          "The 12 members seated on the upper level wear white with yellow ties, sashes and gloves; with 12 members, that's KO1KEYZ."),
        fig(boys, "LAPOSTA 2027 BOYS artist photo: 12 members in white and yellow at the top, six in denim on the right", SITE),
        p("The other three groups wear red in the center, navy and black on the left, and denim on the right.",
          "DXTEEN is the only six-member group, so denim is DXTEEN, and by numbers and placement red appears to be JO1 and navy INI, consistent with their 2025 merch colors."),

        h2("Did DXTEEN switch from green to light blue?"),
        p(f"DXTEEN was green in 2025, but {mk('there is no green gem inside the chest')}, and fans on X have been asking whether the color changed.",
          "A few greenish gems are scattered outside the chest, but the six inside include light blue, the costumes are light blue denim, and DXTEEN's current group photo on the site is styled in pale blue too."),
        p(f"So {mk('DXTEEN may have moved from green to light blue for LAPOSTA 2027')}, though LAPONE hasn't said anything about colors, and it won't be certain until the merch is announced."),

        h2("ME:I is pink, IS:SUE is purple"),
        p("The two girl groups appear unchanged from 2025.",
          "In the GIRLS artist photo, the members in front wear pink and white, and the four in the back row wear purple. IS:SUE has four members, so purple is IS:SUE and pink is ME:I."),
        fig(girls, "LAPOSTA 2027 GIRLS artist photo: pink in front, four members in purple at the back", SITE),

        h2("Do LAPONE groups have official group colors?"),
        p("None of the LAPONE groups has officially announced a group color.",
          "Member colors are set, but group-wide colors are a matter of fan opinion, and the official light sticks aren't a single color either: JO1's is shaped like a jam jar after the fandom name JAM, and INI's has light blue, purple and pink rings."),
        p(f"So the LAPOSTA colors are best seen as {mk('a way to tell six groups apart at a joint concert')}.",
          "For reference, RYUJI holds yellow as his member color in KO1KEYZ.",
          f"Dates and tickets are in our {a(L(15188), 'KO1KEYZ LAPOSTA 2027 article')}."),

        h2("Summary"),
        ui.summary([
            "The LAPOSTA 2027 chest holds red, purple, blue, light blue, yellow and pink gems",
            "2025: JO1 red, INI blue, DXTEEN green, ME:I pink, IS:SUE purple",
            "Yellow, never used before, looks like KO1KEYZ's color, matching their white-and-yellow costumes",
            "No green gem and light blue denim suggest DXTEEN may now be light blue",
            "LAPONE groups have no official group colors; LAPOSTA colors are for the joint concert",
            "The merch announcement should settle it",
        ]),
        p("In their first LAPOSTA, KO1KEYZ look set to get a color of their own alongside their seniors. Let's wait for the merch reveal!"),
        ui.quotebox("Related articles", [a(u, t) for u, t in REL["en"]]),
    ]
    en_sum = ("The LAPOSTA 2027 visual hides six gems in a treasure chest. Compared with past LAPOSTA merch colors, "
              "first-timers KO1KEYZ look like yellow, and DXTEEN may have moved from green to light blue.")
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
    tmp = ROOT / "images" / "ko1keyz_group_color" / "_jp_body.html"
    tmp.write_text(html, encoding="utf-8")
    tool = str(ROOT / "tools" / "honorific.py")
    subprocess.run([sys.executable, tool, "fix", "--group", "ko1keyz", str(tmp)], check=True)
    subprocess.run([sys.executable, tool, "check", "--group", "ko1keyz", str(tmp)], check=True)
    return tmp.read_text(encoding="utf-8")


def make_eyecatch():
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"), "--top", "LAPOSTA 2027の宝石",
                    "--main", "KO1KEYZ", "--bottom", "グループカラーは黄色？", "--out", str(EYE), "--seed", "1104"], check=True)


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    md = {}
    if not dry:
        md = {k: upload(IMG / f, "image/jpeg") for k, f in
              (("chest", "laposta2027_chest.jpg"), ("boys", "laposta2027_boys.jpg"), ("girls", "laposta2027_girls.jpg"))}
    built = build(md)
    for (t, c, _), name in zip(built, ("JP", "KR", "EN")):
        assert "<hr" not in c
        print(name, len(t), t, "chars:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", c)))
    assert len(built[0][0]) <= 35
    if dry:
        (ROOT / "images" / "ko1keyz_group_color" / "_jp_preview.html").write_text(built[0][1], encoding="utf-8")
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
    print("eyecatch", eye, "body media", {k: v["id"] for k, v in md.items()})
    subprocess.run([sys.executable, str(ROOT / "tools" / "check_ko1keyz_title.py"), str(jp["id"]), str(kr["id"]), str(en["id"])])
