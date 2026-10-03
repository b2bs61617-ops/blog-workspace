# -*- coding: utf-8 -*-
"""KO1KEYZ 12人がViVi公式InstagramのPR動画「KO1KEYZ meets PRADA BEAUTY」(2026-10-02)で手にしていた
三角形のコスメ = プラダ ビューティ「プラダ リップ ジェリー」(00 グリーン/01 ブルー、各7,700円税込)の記事。
chomoand-1.com に JP/KR/EN の下書きを作る。

一次ソース:
- ViVi公式Instagram リール https://www.instagram.com/reel/Dd_HBl6ypLN/ (2026-10-02 09:00、#PR、
  「みんなが手に持っているのは、今日全国発売のプラダ リップ ジェリー」、来週10/9(金)12時に次の告知、
  動画内に「sponsored by PRADA BEAUTY」、12人がアルファベット順に1人ずつ登場、最後は「Coming Soon...」)
- 商品情報: MAQUIA https://maquia.hpplus.jp/skincare/news/121242/ ・Precious https://precious.jp/articles/-/63185
  ・8and(2026-10-02)。先行9/25(金)公式オンライン+プラダ ビューティ トウキョウ、全国10/2(金)、各7,700円。
  00 グリーン=ヒアルロン酸・ビタミンE・イリス根エキス、乾燥による縦ジワケア/01 ブルー=メントールのプランピング。
  公式サイト jp.pradabeauty.com は curl だと403(ブラウザでは開ける)、商品個別URLは取れなかったのでトップへ文字リンク。
本文画像はリールから切り出したフレーム(冒頭・12人コラージュ・商品カット)。公式商品画像のDL・アップはしない。
ケースは2色とも同じグリーンで、色は中身でしか見分けられない。中身が見えるのはKOSUKE・RYOGA・SHINHAENG・YOSHIKIのカット(水色)。
グループPR記事で個人の私物特定ではないため、アフィリエイト自動付与(STEP1.6)は対象外。

python build_and_post_ko1keyz_prada_lip_jelly.py [--dry]
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

BASE_SLUG = "ko1keyz-prada-lip-jelly"
EYE_JP = ROOT / "images" / "ko1keyz_prada_lip_jelly_eyecatch.png"
EYE_KR = ROOT / "images" / "ko1keyz_prada_lip_jelly_eyecatch_kr.png"
IMG_GROUP = ROOT / "images" / "ko1keyz_prada_lipjelly_group.jpg"
IMG_12 = ROOT / "images" / "ko1keyz_prada_lipjelly_12members.jpg"
IMG_PROD = ROOT / "images" / "ko1keyz_prada_lipjelly_product.jpg"

REEL = "https://www.instagram.com/reel/Dd_HBl6ypLN/"
PRADA = "https://jp.pradabeauty.com/"

L = lambda pid: f"https://chomoand-1.com/?p={pid}"
REL = {
    "ja": [(L(13609), "ViViのぬりえ企画！KO1KEYZのチェキ応募方法と12人の作品"),
           (L(11837), "KO1KEYZの雑誌掲載情報まとめ"),
           (L(109), "KEITOの愛用スキンケアと美容法"),
           (L(10860), "KO1KEYZの今後のスケジュール")],
    "ko": [(L(13613), "ViVi 컬러링 기획! KO1KEYZ 체키 응모 방법과 12명의 작품"),
           (L(11840), "KO1KEYZ 잡지 화보 총정리"),
           (L(10863), "KO1KEYZ 향후 스케줄")],
    "en": [(L(13614), "ViVi's coloring project: how to enter the KO1KEYZ cheki giveaway"),
           (L(11841), "KO1KEYZ magazine appearances"),
           (L(12624), "KO1KEYZ's upcoming schedule")],
}

ui = Ui("#8a8378", "#ddd9d3", "#f7f6f4", "rgba(138,131,120,0.06)")
CAP = f'出典:<a href="{REEL}" target="_blank" rel="noopener">ViVi公式Instagram</a>'
CAP_KR = f'출처: <a href="{REEL}" target="_blank" rel="noopener">ViVi 공식 Instagram</a>'
CAP_EN = f'Source: <a href="{REEL}" target="_blank" rel="noopener">ViVi official Instagram</a>'


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def color_table(rows):
    td = "border:1px solid #ddd9d3;padding:8px 10px;vertical-align:top;"
    trs = []
    for i, row in enumerate(rows):
        bg = "background:#8a8378;color:#fff;font-weight:bold;" if i == 0 else ("" if i % 2 else "background:#f7f6f4;")
        trs.append("<tr>" + "".join(f'<td style="{td}{bg}">{c}</td>' for c in row) + "</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            + "".join(trs) + '</tbody></table></figure>\n<!-- /wp:table -->')


def reactions(title, quotes):
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f6f4;">
<p style="margin:0 0 6px 0;font-weight:bold;font-size:0.9em;color:#8a8378;">{title}</p>
<p style="margin:0;font-size:0.95em;">{"<br>".join(quotes)}</p>
</div>''')


def steps(title, items):
    lis = "\n".join(f'<li style="margin:0 0 8px 0;">{i}</li>' for i in items[:-1]) + f'\n<li style="margin:0;">{items[-1]}</li>'
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#8a8378;color:#fff;">{title}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:#f7f6f4;">
{lis}
</ul>
</div>''')


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


def build(m):
    # ---------------- JP ----------------
    jp_title = "KO1KEYZが持ってたプラダのリップは何？値段・色まとめ！"
    jp = [
        p("KO1KEYZ(コイキーズ)の12人が、緑色の三角形のアイテムを手に次々とカメラに向かってポーズを決める動画が公開されました。",
          f"メンバーが持っていたのは、{mk('プラダ ビューティの「プラダ リップ ジェリー」')}というリップトリートメントです。",
          f"価格は{mk('00 グリーン・01 ブルーの2色とも7,700円(税込)')}で、動画が公開された2026年10月2日(金)に全国発売されたばかりの新作でした。",
          "この記事では、動画の中身と12人の登場シーン、2色の違い、どんなリップなのか、どこで買えるのかまでまとめました。"),
        fig(m["group"], "KO1KEYZ meets PRADA BEAUTYの動画冒頭", CAP),
        ui.table("プラダ リップ ジェリー 基本情報", [
            ("商品名", "プラダ リップ ジェリー"),
            ("ブランド", "PRADA BEAUTY(プラダ ビューティ)"),
            ("カラー", "00 グリーン/01 ブルー"),
            ("価格", "各7,700円(税込)"),
            ("先行発売", "2026年9月25日(金) 公式オンラインストア・プラダ ビューティ トウキョウ"),
            ("全国発売", "2026年10月2日(金)"),
            ("KO1KEYZの登場", "ViVi公式Instagramの動画「KO1KEYZ meets PRADA BEAUTY」(2026年10月2日公開)"),
        ]),
        ui.titlebox("この記事でわかること", [
            "KO1KEYZが持っていた三角形のコスメの正体", "12人それぞれの登場シーン", "値段と2色(グリーン・ブルー)の違い",
            "どんなリップ？特徴と使い方", "どこで買える？購入先", "プラダのアンバサダー？今後の告知は？"]),
        h2("KO1KEYZが持っていた三角形のコスメは「プラダ リップ ジェリー」"),
        ui.minibox("<strong>アイテム:</strong>プラダ ビューティ「プラダ リップ ジェリー」",
                   "<strong>登場した動画:</strong>ViVi公式Instagram「KO1KEYZ meets PRADA BEAUTY」(2026年10月2日)",
                   "<strong>位置づけ:</strong>プラダ ビューティがスポンサーのPR動画(本人の私物として紹介されたものではない)"),
        p("動画が投稿されたのは、ファッション誌ViViの公式Instagramです。",
          "2026年10月2日の朝9時に「KO1KEYZ meets PRADA BEAUTY」というタイトルの縦型動画が公開され、メンバー12人が1人ずつ登場しました。",
          f"投稿文には{mk('「みんなが手に持っているのは、今日全国発売のプラダ リップ ジェリー」')}とはっきり書かれています。"),
        p("三角形のケースは、プラダのロゴでおなじみの逆三角形をそのまま形にしたデザインです。",
          "ふたには「PRADA MILANO」の文字が浮き彫りになっていて、色はやわらかいミントのような緑。",
          "一瞬映っただけでも「プラダだ」と分かるのは、このアイコニックな形のおかげでしょう。"),
        p("注意しておきたいのは、この動画が「#PR」のついたタイアップ企画だという点です。",
          "動画の下には「sponsored by PRADA BEAUTY」と表示されていて、メンバーがふだんから使っている愛用品として紹介されたものではありません。",
          "とはいえ、デビュー直前のKO1KEYZにハイブランドのコスメ案件が届いたこと自体、大きな話題になりました。"),
        h2("12人それぞれの登場シーンは？"),
        ui.minibox("<strong>登場順:</strong>DAIKI→ISSA→KEITO→KOSUKE→RYOGA→RYUJI→SHINHAENG→SIYOUNG→TOWA→YOSHIKI→YUKI→YURA",
                   "<strong>動画の長さ:</strong>約24秒"),
        fig(m["twelve"], "プラダ リップ ジェリーを持つKO1KEYZの12人", CAP),
        p("動画は3人が並ぶにぎやかなオープニングから始まり、そのあとメンバーが名前の表示とともにアルファベット順で1人ずつ登場します。",
          "1人あたりの登場時間は2秒前後と短めですが、それぞれがリップジェリーの持ち方やポーズを変えていて、何度も見返したくなる作りです。"),
        steps("12人の見どころ", [
            "DAIKI:頬の横に三角ケースを添え、カメラから少し目線を外したカット",
            "ISSA:片目を閉じたウインク気味の表情から、唇をとがらせるキス顔まで",
            "KEITO:ケースを顔の横に掲げ、まっすぐカメラを見つめるクールな表情",
            "KOSUKE:ふたを開けて中のジェリーを見せる、商品紹介らしいカット",
            "RYOGA:開けたケースを口元に近づけて、伏し目がちに",
            "RYUJI:金髪をなびかせ、ケースを顔の横に添えて流し目",
            "SHINHAENG:唇に指を当てたり口元を隠したり、表情豊か",
            "SIYOUNG:ケースで片目を隠したり、唇に当てたりと遊び心のあるポーズ",
            "TOWA:ケースを頭の上にのせたり、あごの下に持ったり",
            "YOSHIKI:ピンクの髪に合わせるように、ケースを頭上に掲げて",
            "YUKI:ケースを頬に寄せて、やわらかい表情",
            "YURA:ラストはウインクで締めくくり",
        ]),
        p("なかでも注目したいのは、ふたを開けて中身を見せているメンバーがいる点です。",
          "KOSUKE・RYOGA・SHINHAENG・YOSHIKIのカットでは、ケースの中に水色のジェリーが見えていて、01 ブルーを持っていたとみられます。",
          "一方、ふたを閉じたまま持っているメンバーは、後で説明するとおりケースの見た目だけではどちらの色か判別できません。"),
        p("12人分のカットが終わると、メンバーがイスに座って何かのリアクションをとる場面に切り替わり、「Coming Soon...」という文字で動画は終わります。",
          "この意味深なラストについては、記事の後半で触れます。"),
        h2("値段はいくら？2色の違いは？"),
        ui.minibox("<strong>価格:</strong>00 グリーン・01 ブルーとも7,700円(税込)",
                   "<strong>違い:</strong>グリーン=保湿重視、ブルー=メントールでぷっくり"),
        p(f"プラダ リップ ジェリーの値段は、{mk('1個7,700円(税込)')}です。",
          "ドラッグストアのリップクリームと比べるとぐっと高めですが、プラダのコスメとしては手に取りやすい価格帯。",
          "ハイブランドのアイテムを初めて買ってみたい人や、プレゼントを探している人にも選ばれそうです。"),
        reactions("Xでの反応", ["「さすがPRADA」", "「軽率に欲しい」", "「意外と安くていいな」", "「お値段は可愛くなかった」"]),
        p("2色の違いは、ジェリーの色と配合されている成分です。"),
        color_table([
            ["カラー", "00 グリーン", "01 ブルー"],
            ["ジェリーの色", "うすい緑", "水色"],
            ["特徴", "乾燥しがちな唇の水分の蒸発を防ぎ、縦ジワをケアしながらなめらかに", "メントールのひんやりした刺激とプランピング効果で、ぷっくりした唇に"],
            ["主な成分", "ヒアルロン酸・ビタミンE・イリス根エキス", "上記に加えてメントールなど"],
            ["向いている人", "毎日の保湿ケア・夜のケアを重視したい人", "ツヤとボリューム感を出したい人"],
        ]),
        fig(m["prod"], "プラダ リップ ジェリーのグリーンとブルー", CAP),
        p(f"見落としやすいのが、{mk('ケースの色は2色とも同じグリーン')}だということです。",
          "どちらを持っていても外から見ると同じ見た目なので、色が分かるのはふたを開けて中のジェリーが見えたときだけ。",
          "動画の中でも、閉じたケースだけが映っているカットでは、グリーンかブルーかは区別できませんでした。"),
        p("推しと同じものを買いたい場合は、ふたを開けていたKOSUKE・RYOGA・SHINHAENG・YOSHIKIのカットを参考にするなら01 ブルーが候補になります。",
          "どちらか迷ったら、保湿重視ならグリーン、ぷっくり感を楽しみたいならブルーという選び方がしやすいはずです。"),
        h2("どんなリップ？特徴と使い方"),
        ui.minibox("<strong>テクスチャー:</strong>体温でバームからジェリーに変わる",
                   "<strong>使い方:</strong>リップベース・トップコート・夜のリップケアの3通り"),
        p("プラダ リップ ジェリーは、プラダ ビューティから登場したリップトリートメントです。",
          f"いちばんの特徴は、{mk('唇の体温を感知すると、固めのバームからみずみずしいジェリーへ変化する')}テクスチャーにあります。",
          "塗るときはバームのようになめらかで、仕上がりはジェリーのように透き通ったツヤが出るのが魅力です。"),
        steps("プラダ リップ ジェリーの3つの使い方", [
            "リップベース:メイク前に塗って唇を整え、口紅のノリをよくする",
            "トップコート:口紅の上から重ねて、ツヤを足したり調整したりする",
            "ナイトケア:寝る前にたっぷり塗って、唇を集中保湿する",
        ]),
        p("色つきのリップではなく、仕上がりは透明感のあるツヤなので、男性でも使いやすいのがポイント。",
          "動画の中のメンバーも、ジェリーを塗ったようなうるっとした唇で登場していて、ViViの投稿文でも「ぷるぷるリップ」と紹介されていました。"),
        p("三角形のケースは薄くてポーチに入れやすいサイズ感です。",
          "プラダのロゴをそのまま形にしたデザインなので、持ち歩くだけで気分が上がるアイテムになりそうですね。"),
        h2("どこで買える？購入先まとめ"),
        ui.minibox("<strong>購入先:</strong>プラダ ビューティ公式オンラインストア・プラダ ビューティ トウキョウ・全国の取扱店",
                   "<strong>発売日:</strong>先行2026年9月25日(金)、全国2026年10月2日(金)"),
        steps("プラダ リップ ジェリーの購入先", [
            f"{a(PRADA, 'プラダ ビューティ公式オンラインストア')}(9月25日から先行発売)",
            "プラダ ビューティ トウキョウ(9月25日から先行発売)",
            "全国のプラダ ビューティ取扱店(百貨店のコスメカウンターなど、10月2日から)",
        ]),
        p("先行発売は2026年9月25日(金)から公式オンラインストアとプラダ ビューティ トウキョウで始まり、10月2日(金)から全国で発売されました。",
          "公式オンラインストアでは2色とも7,700円(税込)で、色見本や商品写真も確認できます。"),
        p("年末にかけてはギフト需要が増える時期でもあり、人気色が品薄になる可能性もあります。",
          "KO1KEYZの動画で気になった人は、早めに店頭やオンラインストアで在庫をチェックしておくと安心です。"),
        h2("KO1KEYZはプラダのアンバサダー？今後の告知は？"),
        ui.minibox("<strong>アンバサダー:</strong>2026年10月3日時点で発表なし(ViViのPR企画)",
                   "<strong>次の告知:</strong>2026年10月9日(金)12時にViViから"),
        p("「KO1KEYZはプラダのアンバサダーになったの？」と気になった人も多いかもしれません。",
          f"2026年10月3日時点では、{mk('プラダ ビューティとKO1KEYZのアンバサダー契約の発表は見当たりません')}。",
          "今回の動画は、プラダ ビューティがスポンサーとなったViViのPR企画という位置づけです。"),
        p(f"気になるのは、ViViの投稿文に{mk('「来週10/9(金)の12時には、次なる告知が…！」')}と予告されていることです。",
          "動画のラストにも「Coming Soon...」の文字が入っていて、メンバーが驚いたり盛り上がったりしている様子が映っていました。",
          "何が告知されるのかはまだ明かされていないので、10月9日のお昼はViViの公式Instagramをチェックしておきたいところです。"),
        p("ViViとKO1KEYZといえば、メンバーがギャルデコのぬりえに挑戦した企画も話題になりました。",
          f"ぬりえ企画の中身やチェキの応募方法は{a(L(13609), 'ViViぬりえ企画の記事')}で紹介しています。"),
        h2("まとめ"),
        ui.summary([
            "KO1KEYZが持っていた三角形のコスメは、プラダ ビューティ「プラダ リップ ジェリー」",
            "ViVi公式Instagramの「KO1KEYZ meets PRADA BEAUTY」(2026年10月2日)で12人が1人ずつ登場",
            "プラダ ビューティがスポンサーのPR動画で、本人の愛用品として紹介されたものではない",
            "価格は00 グリーン・01 ブルーとも7,700円(税込)、2026年10月2日に全国発売",
            "ケースは2色とも同じグリーンで、中身が見えたKOSUKE・RYOGA・SHINHAENG・YOSHIKIは水色(01 ブルー)とみられる",
            "体温でバームからジェリーに変わり、リップベース・トップコート・夜のケアに使える",
            "ViViから10月9日(金)12時に次の告知が予定されている",
        ]),
        p("デビュー前からプラダのコスメ企画に登場したKO1KEYZ。",
          "推しと同じ三角ケースのリップで、ぷるぷるの唇を目指してみてはいかがでしょうか！"),
        ui.quotebox("あわせて読みたい", [a(u, t) for u, t in REL["ja"]]),
    ]
    jp_sum = ("KO1KEYZ12人がViViのPR動画で持っていた三角形のコスメは、プラダ ビューティの新作「プラダ リップ ジェリー」。"
              "グリーン・ブルー各7,700円で10/2全国発売。2色の違いや購入先、10/9の次の告知までまとめました。")

    # ---------------- KR ----------------
    kr_title = "KO1KEYZ가 들고 있던 프라다 립은? 가격·컬러 총정리!"
    kr = [
        p("KO1KEYZ(코이키즈) 12명이 초록색 삼각형 아이템을 손에 들고 차례로 카메라 앞에서 포즈를 취하는 영상이 공개됐어요.",
          f"멤버들이 들고 있던 건 {mk('프라다 뷰티의 \'프라다 립 젤리\'')}라는 립 트리트먼트예요.",
          f"가격은 {mk('00 그린·01 블루 두 가지 모두 7,700엔(세금 포함)')}이고, 영상이 공개된 2026년 10월 2일(금)에 일본 전국 발매된 신제품이었어요.",
          "이 글에서는 영상 내용과 12명의 등장 장면, 두 컬러의 차이, 어떤 립인지, 어디서 살 수 있는지까지 정리했어요."),
        fig(m["group"], "KO1KEYZ meets PRADA BEAUTY 영상 오프닝", CAP_KR),
        ui.table("프라다 립 젤리 기본 정보", [
            ("상품명", "프라다 립 젤리(PRADA LIP JELLY)"),
            ("브랜드", "PRADA BEAUTY(프라다 뷰티)"),
            ("컬러", "00 그린 / 01 블루"),
            ("가격(일본)", "각 7,700엔(세금 포함)"),
            ("선행 발매(일본)", "2026년 9월 25일(금) 공식 온라인 스토어·프라다 뷰티 도쿄"),
            ("전국 발매(일본)", "2026년 10월 2일(금)"),
            ("KO1KEYZ 등장", "ViVi 공식 Instagram 영상 'KO1KEYZ meets PRADA BEAUTY'(2026년 10월 2일 공개)"),
        ]),
        ui.titlebox("이 글에서 알 수 있는 것", [
            "KO1KEYZ가 들고 있던 삼각형 코스메의 정체", "12명 각각의 등장 장면", "가격과 두 컬러(그린·블루)의 차이",
            "어떤 립? 특징과 사용법", "어디서 살 수 있을까? 구매처", "프라다 앰버서더? 다음 공지는?"]),
        h2("KO1KEYZ가 들고 있던 삼각형 코스메는 '프라다 립 젤리'"),
        ui.minibox("<strong>아이템:</strong>프라다 뷰티 '프라다 립 젤리'",
                   "<strong>등장 영상:</strong>ViVi 공식 Instagram 'KO1KEYZ meets PRADA BEAUTY'(2026년 10월 2일)",
                   "<strong>성격:</strong>프라다 뷰티가 스폰서인 PR 영상(멤버의 애용품으로 소개된 것은 아님)"),
        p("영상이 올라온 곳은 일본 패션지 ViVi의 공식 Instagram이에요.",
          "2026년 10월 2일 오전 9시에 'KO1KEYZ meets PRADA BEAUTY'라는 세로형 영상이 공개됐고, 멤버 12명이 한 명씩 등장했어요.",
          f"게시글에는 {mk('\'모두가 손에 들고 있는 건 오늘 전국 발매된 프라다 립 젤리\'')}라고 분명히 적혀 있어요."),
        p("삼각형 케이스는 프라다 로고로 익숙한 역삼각형을 그대로 형태로 만든 디자인이에요.",
          "뚜껑에는 'PRADA MILANO' 글자가 양각으로 새겨져 있고, 색은 부드러운 민트 같은 초록색이에요.",
          "잠깐만 비쳐도 '프라다다!' 하고 알아볼 수 있는 건 이 아이코닉한 모양 덕분이죠."),
        p("알아 둘 점은 이 영상이 '#PR'이 붙은 협찬 기획이라는 거예요.",
          "영상 하단에는 'sponsored by PRADA BEAUTY'라고 표시되어 있어서, 멤버들이 평소 쓰는 애용품으로 소개된 건 아니에요.",
          "그래도 데뷔 직전의 KO1KEYZ에게 하이브랜드 코스메 협업이 들어왔다는 것 자체가 큰 화제가 됐어요."),
        h2("12명 각각의 등장 장면은?"),
        ui.minibox("<strong>등장 순서:</strong>DAIKI→ISSA→KEITO→KOSUKE→RYOGA→RYUJI→SHINHAENG→SIYOUNG→TOWA→YOSHIKI→YUKI→YURA",
                   "<strong>영상 길이:</strong>약 24초"),
        fig(m["twelve"], "프라다 립 젤리를 든 KO1KEYZ 12명", CAP_KR),
        p("영상은 세 명이 나란히 선 활기찬 오프닝으로 시작해, 이어서 멤버들이 이름 자막과 함께 알파벳 순으로 한 명씩 등장해요.",
          "한 사람당 등장 시간은 2초 안팎으로 짧지만, 각자 립 젤리를 드는 방법과 포즈를 다르게 해서 몇 번이고 돌려 보고 싶어지는 구성이에요."),
        steps("12명의 볼거리", [
            "DAIKI: 볼 옆에 삼각 케이스를 대고 카메라에서 살짝 시선을 돌린 컷",
            "ISSA: 윙크하는 듯한 표정부터 입술을 내민 뽀뽀 표정까지",
            "KEITO: 케이스를 얼굴 옆에 들고 카메라를 똑바로 바라보는 쿨한 표정",
            "KOSUKE: 뚜껑을 열어 안의 젤리를 보여 주는 제품 소개다운 컷",
            "RYOGA: 연 케이스를 입가에 가까이 대고 살짝 내리깐 눈",
            "RYUJI: 금발을 휘날리며 케이스를 얼굴 옆에 대고 곁눈질",
            "SHINHAENG: 입술에 손가락을 대거나 입을 가리는 등 풍부한 표정",
            "SIYOUNG: 케이스로 한쪽 눈을 가리거나 입술에 대는 장난스러운 포즈",
            "TOWA: 케이스를 머리 위에 올리거나 턱 아래에 들고",
            "YOSHIKI: 핑크 머리에 맞추듯 케이스를 머리 위로 들고",
            "YUKI: 케이스를 볼에 가까이 대고 부드러운 표정",
            "YURA: 마지막은 윙크로 마무리",
        ]),
        p("특히 주목할 점은 뚜껑을 열어 안을 보여 준 멤버가 있다는 거예요.",
          "KOSUKE·RYOGA·SHINHAENG·YOSHIKI의 컷에서는 케이스 안에 하늘색 젤리가 보여서 01 블루를 들고 있었던 것으로 보여요.",
          "반면 뚜껑을 닫은 채 들고 있는 멤버는, 뒤에서 설명하듯 케이스 겉모습만으로는 어느 컬러인지 구분할 수 없어요."),
        p("12명의 컷이 끝나면 멤버들이 의자에 앉아 무언가에 리액션하는 장면으로 바뀌고, 'Coming Soon...'이라는 문구로 영상이 끝나요.",
          "이 의미심장한 엔딩은 글 후반에서 다룰게요."),
        h2("가격은 얼마? 두 컬러의 차이는?"),
        ui.minibox("<strong>가격:</strong>00 그린·01 블루 모두 7,700엔(세금 포함)",
                   "<strong>차이:</strong>그린=보습 중심, 블루=멘톨로 도톰하게"),
        p(f"프라다 립 젤리의 일본 가격은 {mk('1개 7,700엔(세금 포함)')}이에요.",
          "드러그스토어 립밤에 비하면 꽤 비싸지만, 프라다 코스메 중에서는 비교적 부담 없이 고를 수 있는 가격대예요.",
          "하이브랜드 아이템을 처음 사 보고 싶은 사람이나 선물을 찾는 사람에게도 인기가 있을 것 같아요."),
        p("두 컬러의 차이는 젤리 색과 배합 성분이에요."),
        color_table([
            ["컬러", "00 그린", "01 블루"],
            ["젤리 색", "연한 초록", "하늘색"],
            ["특징", "건조해지기 쉬운 입술의 수분 증발을 막고 세로 주름을 케어하며 매끄럽게", "멘톨의 시원한 자극과 플럼핑 효과로 도톰한 입술로"],
            ["주요 성분", "히알루론산·비타민E·아이리스 뿌리 추출물", "위 성분에 멘톨 등 추가"],
            ["추천", "매일 보습 케어·나이트 케어를 중시하는 사람", "윤기와 볼륨감을 내고 싶은 사람"],
        ]),
        fig(m["prod"], "프라다 립 젤리 그린과 블루", CAP_KR),
        p(f"놓치기 쉬운 점은 {mk('케이스 색이 두 컬러 모두 같은 그린')}이라는 거예요.",
          "어느 쪽을 들고 있어도 겉으로는 똑같아 보여서, 색을 알 수 있는 건 뚜껑을 열어 젤리가 보일 때뿐이에요.",
          "영상에서도 닫힌 케이스만 나온 컷에서는 그린인지 블루인지 구분할 수 없었어요."),
        p("최애와 같은 걸 사고 싶다면, 뚜껑을 열었던 KOSUKE·RYOGA·SHINHAENG·YOSHIKI의 컷을 참고하면 01 블루가 후보가 돼요.",
          "고민된다면 보습 중심이면 그린, 도톰한 느낌을 즐기고 싶다면 블루로 고르면 쉬워요."),
        h2("어떤 립? 특징과 사용법"),
        ui.minibox("<strong>텍스처:</strong>체온에 따라 밤에서 젤리로 변화",
                   "<strong>사용법:</strong>립 베이스·톱코트·나이트 립 케어 3가지"),
        p("프라다 립 젤리는 프라다 뷰티에서 나온 립 트리트먼트예요.",
          f"가장 큰 특징은 {mk('입술의 체온을 감지하면 단단한 밤에서 촉촉한 젤리로 변하는')} 텍스처예요.",
          "바를 때는 밤처럼 부드럽고, 마무리는 젤리처럼 투명한 윤기가 나는 게 매력이에요."),
        steps("프라다 립 젤리의 3가지 사용법", [
            "립 베이스: 메이크업 전에 발라 입술을 정돈하고 립스틱 밀착력을 높인다",
            "톱코트: 립스틱 위에 덧발라 윤기를 더하거나 조절한다",
            "나이트 케어: 자기 전에 듬뿍 발라 입술을 집중 보습한다",
        ]),
        p("색이 진하게 나는 립이 아니라 투명한 윤기로 마무리되기 때문에 남성도 쓰기 쉬운 게 포인트예요.",
          "영상 속 멤버들도 젤리를 바른 듯 촉촉한 입술로 등장했고, ViVi 게시글에서도 '탱글탱글 립'으로 소개됐어요."),
        p("삼각형 케이스는 얇아서 파우치에 넣기 좋은 크기예요.",
          "프라다 로고를 그대로 형태로 만든 디자인이라 들고 다니기만 해도 기분이 좋아지는 아이템이 될 것 같아요."),
        h2("어디서 살 수 있을까? 구매처 정리"),
        ui.minibox("<strong>구매처(일본):</strong>프라다 뷰티 공식 온라인 스토어·프라다 뷰티 도쿄·전국 취급점",
                   "<strong>발매일:</strong>선행 2026년 9월 25일(금), 전국 2026년 10월 2일(금)"),
        steps("프라다 립 젤리 구매처(일본)", [
            f"{a(PRADA, '프라다 뷰티 일본 공식 온라인 스토어')}(9월 25일부터 선행 발매)",
            "프라다 뷰티 도쿄(9월 25일부터 선행 발매)",
            "일본 전국 프라다 뷰티 취급점(백화점 코스메 카운터 등, 10월 2일부터)",
        ]),
        p("일본에서는 2026년 9월 25일(금)부터 공식 온라인 스토어와 프라다 뷰티 도쿄에서 선행 발매가 시작됐고, 10월 2일(금)부터 전국에서 발매됐어요.",
          "일본 공식 온라인 스토어에서는 두 컬러 모두 7,700엔(세금 포함)이고, 컬러 견본과 제품 사진도 확인할 수 있어요."),
        p("한국 등 다른 나라에서의 발매 여부나 가격은 지역마다 다를 수 있으니, 각 나라의 프라다 뷰티 공식 사이트에서 확인해 보세요.",
          "연말에는 선물 수요가 늘어나는 시기라 인기 컬러가 품귀될 수도 있어요."),
        h2("KO1KEYZ는 프라다 앰버서더? 다음 공지는?"),
        ui.minibox("<strong>앰버서더:</strong>2026년 10월 3일 기준 발표 없음(ViVi의 PR 기획)",
                   "<strong>다음 공지:</strong>2026년 10월 9일(금) 12시 ViVi에서"),
        p("'KO1KEYZ가 프라다 앰버서더가 된 거야?' 하고 궁금했던 분도 많을 거예요.",
          f"2026년 10월 3일 기준으로는 {mk('프라다 뷰티와 KO1KEYZ의 앰버서더 계약 발표는 찾을 수 없어요')}.",
          "이번 영상은 프라다 뷰티가 스폰서로 참여한 ViVi의 PR 기획이에요."),
        p(f"눈길을 끄는 건 ViVi 게시글에 {mk('\'다음 주 10/9(금) 12시에는 다음 공지가…!\'')}라고 예고되어 있다는 점이에요.",
          "영상 마지막에도 'Coming Soon...' 문구가 들어가 있고, 멤버들이 놀라거나 신나 하는 모습이 담겨 있었어요.",
          "무엇이 공지될지는 아직 밝혀지지 않았으니, 10월 9일 낮(일본 시간)에는 ViVi 공식 Instagram을 확인해 두면 좋겠어요."),
        p("ViVi와 KO1KEYZ라고 하면, 멤버들이 갸루 데코 컬러링에 도전한 기획도 화제가 됐어요.",
          f"컬러링 기획 내용과 체키 응모 방법은 {a(L(13613), 'ViVi 컬러링 기획 글')}에서 소개하고 있어요."),
        h2("정리"),
        ui.summary([
            "KO1KEYZ가 들고 있던 삼각형 코스메는 프라다 뷰티 '프라다 립 젤리'",
            "ViVi 공식 Instagram 'KO1KEYZ meets PRADA BEAUTY'(2026년 10월 2일)에서 12명이 한 명씩 등장",
            "프라다 뷰티가 스폰서인 PR 영상으로, 멤버의 애용품으로 소개된 것은 아님",
            "일본 가격은 00 그린·01 블루 모두 7,700엔(세금 포함), 2026년 10월 2일 전국 발매",
            "케이스는 두 컬러 모두 같은 그린, 안이 보인 KOSUKE·RYOGA·SHINHAENG·YOSHIKI는 하늘색(01 블루)으로 보임",
            "체온으로 밤에서 젤리로 변하고, 립 베이스·톱코트·나이트 케어로 사용 가능",
            "ViVi에서 10월 9일(금) 12시에 다음 공지 예정",
        ]),
        p("데뷔 전부터 프라다 코스메 기획에 등장한 KO1KEYZ.",
          "최애와 같은 삼각 케이스 립으로 탱글탱글한 입술을 노려 보는 건 어떨까요!"),
        ui.quotebox("함께 읽으면 좋은 글", [a(u, t) for u, t in REL["ko"]]),
    ]
    kr_sum = ("KO1KEYZ 12명이 ViVi PR 영상에서 들고 있던 삼각형 코스메는 프라다 뷰티 신작 '프라다 립 젤리'. "
              "그린·블루 각 7,700엔으로 10/2 일본 전국 발매. 두 컬러의 차이와 구매처, 10/9 다음 공지까지 정리했어요.")

    # ---------------- EN ----------------
    en_title = "What Prada Lip Product Did KO1KEYZ Hold? Price & Colors!"
    en = [
        p("A video has been released of all 12 KO1KEYZ members posing for the camera one after another, each holding a green triangular item.",
          f"What they were holding is {mk('PRADA BEAUTY\'s \"Prada Lip Jelly\"')}, a lip treatment.",
          f"It costs {mk('7,700 yen (tax included) for either shade, 00 Green or 01 Blue')}, and it went on sale nationwide in Japan on October 2, 2026 (Fri), the very day the video came out.",
          "This article covers what's in the video, each member's scene, the difference between the two shades, what kind of lip product it is, and where to buy it."),
        fig(m["group"], "Opening of the KO1KEYZ meets PRADA BEAUTY video", CAP_EN),
        ui.table("Prada Lip Jelly at a glance", [
            ("Product", "Prada Lip Jelly"),
            ("Brand", "PRADA BEAUTY"),
            ("Shades", "00 Green / 01 Blue"),
            ("Price (Japan)", "7,700 yen each (tax included)"),
            ("Early release (Japan)", "September 25 (Fri), 2026, official online store and PRADA BEAUTY TOKYO"),
            ("Nationwide release (Japan)", "October 2 (Fri), 2026"),
            ("KO1KEYZ appearance", "ViVi official Instagram video \"KO1KEYZ meets PRADA BEAUTY\" (October 2, 2026)"),
        ]),
        ui.titlebox("What you'll learn", [
            "What the triangular cosmetic KO1KEYZ held is", "Each member's scene", "Price and the difference between Green and Blue",
            "What kind of lip product it is and how to use it", "Where to buy it", "Are they Prada ambassadors? What's next?"]),
        h2("The triangular cosmetic KO1KEYZ held is the Prada Lip Jelly"),
        ui.minibox("<strong>Item:</strong>PRADA BEAUTY \"Prada Lip Jelly\"",
                   "<strong>Video:</strong>ViVi official Instagram, \"KO1KEYZ meets PRADA BEAUTY\" (October 2, 2026)",
                   "<strong>Context:</strong>a PR video sponsored by PRADA BEAUTY (not presented as the members' personal favorites)"),
        p("The video was posted on the official Instagram of the Japanese fashion magazine ViVi.",
          "At 9 a.m. on October 2, 2026, a vertical video titled \"KO1KEYZ meets PRADA BEAUTY\" went up, with the 12 members appearing one by one.",
          f"The caption states clearly that {mk('\"what everyone is holding is the Prada Lip Jelly, on sale nationwide today\"')}."),
        p("The triangular case is shaped exactly like Prada's familiar inverted-triangle logo.",
          "The lid is embossed with \"PRADA MILANO,\" and the color is a soft, minty green.",
          "That iconic shape is why you can tell it's Prada even from a split-second glimpse."),
        p("One thing to keep in mind: this video is a sponsored collaboration tagged \"#PR.\"",
          "\"sponsored by PRADA BEAUTY\" appears at the bottom of the video, so it wasn't presented as something the members use every day.",
          "Even so, a high-end beauty collaboration landing just before KO1KEYZ's debut became big news among fans."),
        h2("Each member's scene"),
        ui.minibox("<strong>Order:</strong>DAIKI → ISSA → KEITO → KOSUKE → RYOGA → RYUJI → SHINHAENG → SIYOUNG → TOWA → YOSHIKI → YUKI → YURA",
                   "<strong>Length:</strong>about 24 seconds"),
        fig(m["twelve"], "The 12 KO1KEYZ members holding the Prada Lip Jelly", CAP_EN),
        p("The video opens with a lively shot of three members side by side, then the members appear one at a time in alphabetical order with their names on screen.",
          "Each gets only about two seconds, but everyone holds the lip jelly differently and strikes a different pose, so it's the kind of clip you'll want to replay."),
        steps("Highlights for each member", [
            "DAIKI: the case held beside his cheek, gaze slightly off camera",
            "ISSA: from a near-wink to a pouty kiss face",
            "KEITO: the case raised beside his face, looking straight into the camera",
            "KOSUKE: opening the lid to show the jelly inside, like a product demo",
            "RYOGA: the open case brought up near his lips, eyes lowered",
            "RYUJI: blond hair swept aside, case at his cheek and a sidelong glance",
            "SHINHAENG: a finger on his lips, then covering his mouth, full of expressions",
            "SIYOUNG: playful poses, covering one eye with the case and touching it to his lips",
            "TOWA: the case balanced on his head, then held under his chin",
            "YOSHIKI: the case held up over his pink hair",
            "YUKI: the case close to his cheek with a soft expression",
            "YURA: closing things out with a wink",
        ]),
        p("What stands out is that some members open the lid and show what's inside.",
          "In KOSUKE's, RYOGA's, SHINHAENG's and YOSHIKI's shots, light-blue jelly is visible, so they appear to be holding 01 Blue.",
          "Members who keep the case closed are a different story: as explained below, you can't tell the shade from the outside."),
        p("After the 12 individual shots, the video cuts to the members sitting on chairs and reacting to something, then ends with the words \"Coming Soon...\"",
          "We'll come back to that teasing ending later in the article."),
        h2("How much is it, and how do the two shades differ?"),
        ui.minibox("<strong>Price:</strong>7,700 yen (tax included) for both 00 Green and 01 Blue",
                   "<strong>Difference:</strong>Green focuses on moisture; Blue uses menthol for a plumper look"),
        p(f"In Japan the Prada Lip Jelly costs {mk('7,700 yen (tax included)')}.",
          "That's well above a drugstore lip balm, but it's one of the more approachable price points among Prada's beauty products.",
          "It could be a good pick for someone trying a luxury brand for the first time or looking for a gift."),
        p("The two shades differ in jelly color and ingredients."),
        color_table([
            ["Shade", "00 Green", "01 Blue"],
            ["Jelly color", "Pale green", "Light blue"],
            ["Key benefit", "Locks in moisture on dry lips and smooths fine vertical lines", "A cool menthol tingle and plumping effect for fuller-looking lips"],
            ["Main ingredients", "Hyaluronic acid, vitamin E, iris root extract", "The above plus menthol and more"],
            ["Best for", "Daily moisture and overnight care", "Adding shine and volume"],
        ]),
        fig(m["prod"], "Prada Lip Jelly in Green and Blue", CAP_EN),
        p(f"An easy detail to miss: {mk('the case is the same green for both shades')}.",
          "From the outside they look identical, so you can only tell which is which when the lid is open and the jelly shows.",
          "In the video, too, shots with only a closed case don't reveal whether it's Green or Blue."),
        p("If you want to match your bias, the open-lid shots of KOSUKE, RYOGA, SHINHAENG and YOSHIKI point to 01 Blue.",
          "If you're torn, a simple rule of thumb is Green for moisture and Blue for a plumper look."),
        h2("What kind of lip product is it? Features and how to use it"),
        ui.minibox("<strong>Texture:</strong>turns from balm to jelly with body heat",
                   "<strong>Uses:</strong>lip base, top coat, or overnight lip care"),
        p("The Prada Lip Jelly is a lip treatment from PRADA BEAUTY.",
          f"Its signature feature is a texture that {mk('changes from a firm balm into a fresh jelly when it senses the warmth of your lips')}.",
          "It glides on smoothly like a balm and finishes with a clear, jelly-like shine."),
        steps("Three ways to use the Prada Lip Jelly", [
            "Lip base: apply before makeup to prep your lips and help lipstick go on smoothly",
            "Top coat: layer over lipstick to add or adjust shine",
            "Overnight care: apply generously before bed for intensive moisture",
        ]),
        p("It isn't a tinted lip product; the finish is a clear shine, which makes it easy for anyone to wear, men included.",
          "The members in the video show off glossy, hydrated-looking lips, and ViVi's caption described them as \"plump, bouncy lips.\""),
        p("The triangular case is slim enough to slip into a pouch.",
          "Since the design is Prada's logo turned into an object, just carrying it around might lift your mood."),
        h2("Where to buy it"),
        ui.minibox("<strong>Where (Japan):</strong>PRADA BEAUTY official online store, PRADA BEAUTY TOKYO, and retailers nationwide",
                   "<strong>Release:</strong>early on September 25 (Fri), 2026; nationwide on October 2 (Fri), 2026"),
        steps("Where to buy the Prada Lip Jelly (Japan)", [
            f"{a(PRADA, 'PRADA BEAUTY Japan official online store')} (early release from September 25)",
            "PRADA BEAUTY TOKYO (early release from September 25)",
            "PRADA BEAUTY retailers across Japan, such as department store beauty counters (from October 2)",
        ]),
        p("In Japan, the early release began on September 25, 2026 (Fri) at the official online store and PRADA BEAUTY TOKYO, followed by the nationwide release on October 2 (Fri).",
          "The Japanese official online store lists both shades at 7,700 yen (tax included), with swatches and product photos."),
        p("Availability and pricing outside Japan may vary by region, so check your local PRADA BEAUTY website.",
          "Gift demand also picks up toward the end of the year, so popular shades could sell out."),
        h2("Are KO1KEYZ Prada ambassadors? What's coming next?"),
        ui.minibox("<strong>Ambassadors:</strong>no announcement as of October 3, 2026 (this was a ViVi PR project)",
                   "<strong>Next announcement:</strong>October 9 (Fri), 2026 at 12:00 JST from ViVi"),
        p("Plenty of fans have probably wondered whether KO1KEYZ have become Prada ambassadors.",
          f"As of October 3, 2026, {mk('there is no announcement of an ambassador deal between PRADA BEAUTY and KO1KEYZ')}.",
          "This video is a ViVi PR project with PRADA BEAUTY as the sponsor."),
        p(f"What's intriguing is that ViVi's caption teases {mk('\"another announcement next week, 10/9 (Fri) at 12:00...!\"')}",
          "The end of the video also carries \"Coming Soon...\" and shows the members looking surprised and excited.",
          "Nothing has been revealed yet, so it's worth checking ViVi's official Instagram around noon (JST) on October 9."),
        p("Speaking of ViVi and KO1KEYZ, the project where the members tried gyaru-deco coloring pages also got a lot of attention.",
          f"We cover it and how to enter the cheki giveaway in {a(L(13614), 'our ViVi coloring project article')}."),
        h2("Summary"),
        ui.summary([
            "The triangular cosmetic KO1KEYZ held is PRADA BEAUTY's \"Prada Lip Jelly\"",
            "All 12 members appear one by one in ViVi's Instagram video \"KO1KEYZ meets PRADA BEAUTY\" (October 2, 2026)",
            "It's a PR video sponsored by PRADA BEAUTY, not a look at the members' personal favorites",
            "7,700 yen (tax included) in Japan for both 00 Green and 01 Blue, released nationwide on October 2, 2026",
            "Both shades share the same green case; KOSUKE, RYOGA, SHINHAENG and YOSHIKI's open cases show light blue (01 Blue)",
            "It turns from balm to jelly with body heat and works as a lip base, top coat or overnight care",
            "ViVi has another announcement scheduled for October 9 (Fri) at 12:00 JST",
        ]),
        p("KO1KEYZ landed a Prada beauty project even before their debut.",
          "Why not try the same triangle-case lip jelly as your bias and go for those glossy lips!"),
        ui.quotebox("Related articles", [a(u, t) for u, t in REL["en"]]),
    ]
    en_sum = ("The triangular cosmetic all 12 KO1KEYZ members held in ViVi's PR video is PRADA BEAUTY's new Prada Lip Jelly, "
              "7,700 yen in Green or Blue, out nationwide in Japan on 10/2. Shade differences, where to buy, and the 10/9 teaser.")
    join = lambda bl: "\n\n".join(bl)
    return (jp_title, join(jp), jp_sum), (kr_title, join(kr), kr_sum), (en_title, join(en), en_sum)


def upload(path, ctype):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HA, "Content-Type": ctype, "Content-Disposition": f'attachment; filename="{path.name}"'},
                      data=path.read_bytes())
    r.raise_for_status()
    return r.json()


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
    subprocess.run([sys.executable, tool, "--top", "12人が持ってたコスメは？", "--main", "KO1KEYZ",
                    "--bottom", "プラダのリップジェリー！", "--out", str(EYE_JP), "--seed", "1002"], check=True)
    subprocess.run([sys.executable, tool, "--top", "12명이 든 코스메는?", "--main", "KO1KEYZ",
                    "--bottom", "프라다 립 젤리!", "--out", str(EYE_KR), "--seed", "1002", "--lang", "kr"], check=True)


DUMMY = {"source_url": "x", "media_details": {"width": 720, "height": 1280, "sizes": {}}}

if __name__ == "__main__":
    dry = "--dry" in sys.argv
    if dry:
        media = {"group": DUMMY, "twelve": DUMMY, "prod": DUMMY}
    else:
        media = {"group": upload(IMG_GROUP, "image/jpeg"), "twelve": upload(IMG_12, "image/jpeg"),
                 "prod": upload(IMG_PROD, "image/jpeg")}
    built = build(media)
    for (t, c, _), name in zip(built, ("JP", "KR", "EN")):
        assert "<hr" not in c
        print(name, len(t), t, "chars:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", c, flags=re.S)))
    assert len(built[0][0]) <= 35
    if dry:
        (ROOT / "tmp_ko1keyz_prada_preview.html").write_text(built[0][1], encoding="utf-8")
        sys.exit(0)
    make_eyecatch()
    (jt, jc, js), (kt, kc, ks), (et, ec, es) = built
    jp_eye = upload(EYE_JP, "image/png")["id"]
    kr_eye = upload(EYE_KR, "image/png")["id"]
    jp = post_draft(jt, jc, BASE_SLUG, "ja", [66, 62], jp_eye, js)
    print("JP", jp["id"], jp["slug"], jp["link"])
    kr = post_draft(kt, kc, BASE_SLUG + "-kr", "ko", [74, 70], kr_eye, ks, jp["id"])
    print("KR", kr["id"], kr["slug"], kr["link"])
    en = post_draft(et, ec, BASE_SLUG + "-en", "en", [110, 112], jp_eye, es, jp["id"])
    print("EN", en["id"], en["slug"], en["link"])
    print("eyecatch", jp_eye, kr_eye, "images", {k: v["id"] for k, v in media.items()})
