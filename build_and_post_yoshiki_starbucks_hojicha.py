# -*- coding: utf-8 -*-
"""YOSHIKI(矢田佳暉) スタバの定番ドリンク記事: JP + KR + EN 下書き投稿(本文画像なし・アイキャッチのみ)。
ソース: KO1KEYZ 1ST ONLINE TALK Day2(2026-09-13)のヨントンレポ
  https://x.com/___yoshiking/status/2099076130892603759 (「スタバでいつも何飲む?」→「ほうじ茶クラシックティーラテ!!」)
  チャミスル: https://x.com/___yoshiking/status/2099094168081682475 / https://x.com/4sk__oO/status/2099017754833772762
収集データ: tools/Xiy/posts_20260925_yoshiki_sb*/

python build_and_post_yoshiki_starbucks_hojicha.py [--dry]
"""
import base64
import json
import re
import subprocess
import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
    return env


ENV = load_env(ROOT / ".env")
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
HA = {"Authorization": f"Basic {AUTH}"}

BASE_SLUG = "yoshiki-starbucks-hojicha-classic-tea-latte"

# YOSHIKI=ピンク(既存YOSHIKI記事13061と同じ配色)
A = "#d66b93"
SOFT = "#f4d4e0"
BG = "#fdf3f7"

MENU_URL = "https://menu.starbucks.co.jp/4524785557185"

# 内部リンク(WP APIで確認済み・すべて公開済み)
L_TALK_JP = "https://chomoand-1.com/yoshiki-favorite-type-cat-cafe-date-ko1keyz-13061"
L_WIKI_JP = "https://chomoand-1.com/yadayoshiki_wiki-3741"
L_GAKU_JP = "https://chomoand-1.com/yadayoshiki_gakureki-3744"
L_GAKU_KR = "https://chomoand-1.com/ko/yadayoshiki_gakureki-kr-10680"
L_GAKU_EN = "https://chomoand-1.com/en/yadayoshiki_gakureki-en-11533"
L_CAT_JP = "https://chomoand-1.com/what-is-the-name-of-yoshiaki-yadas-famil-12381"
L_DAIWAN_JP = "https://chomoand-1.com/does-yoshiki-look-like-the-chi-13124"
L_DAIWAN_EN = "https://chomoand-1.com/en/does-yoshiki-look-like-the-chi-en-13129"
L_KOSUKE_JP = "https://chomoand-1.com/ko1keyz-what-is-kosukes-favori-13467"
L_KOSUKE_KR = "https://chomoand-1.com/ko/ko1keyz-what-is-kosukes-favori-kr-13469"
L_KOSUKE_EN = "https://chomoand-1.com/en/ko1keyz-what-is-kosukes-favori-en-13470"
L_MATOME_JP = "https://chomoand-1.com/ko1keyzs-first-yoton-online-talk-session-13049"


# ---------- HTML部品 ----------
def para(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def html_block(inner):
    return f"<!-- wp:html -->\n{inner}\n<!-- /wp:html -->"


def mini(rows):
    """各H2直後のミニbox(ラベル+答えの先出し)"""
    ps = []
    for i, (k, v) in enumerate(rows):
        m = "0" if i == 0 else "4px 0 0 0"
        ps.append(f'<p style="margin:{m};"><strong>{k}</strong>{v}</p>')
    return html_block(
        f'<div style="border:1px solid {SOFT};border-left:4px solid {A};border-radius:4px;padding:10px 16px;'
        f'margin:0 0 16px 0;background:{BG};">\n' + "\n".join(ps) + "\n</div>"
    )


def spec_box(title, rows):
    trs = "\n".join(
        f'<tr><td style="background:{BG};border:1px solid {SOFT};padding:8px 12px;width:32%;">{k}</td>'
        f'<td style="border:1px solid {SOFT};padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return html_block(
        f'<div style="border:1px solid {SOFT};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;color:{A};">{title}</p>\n'
        f'<table style="border-collapse:collapse;width:100%;">\n{trs}\n</table>\n</div>'
    )


def toc_box(title, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return html_block(
        f'<div style="border:1px solid {SOFT};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">{title}</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">\n{lis}\n</ul>\n</div>'
    )


CHECK = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {A};border-radius:3px;'
         f'color:{A};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')


def summary_box(title, items):
    body = "<br>\n".join(f"{CHECK}{i}" for i in items)
    return html_block(
        f'<div style="border:2px solid {A};border-radius:8px;background:{BG};padding:1em 1.25em;margin:0 0 16px 0;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;color:{A};">{title}</p>\n'
        f'<p style="margin:0;">\n{body}\n</p>\n</div>'
    )


def related_box(title, links):
    lis = "\n".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for u, t in links)
    return html_block(
        f'<div style="border:1px solid {SOFT};border-left:4px solid {A};border-radius:4px;padding:14px 18px;'
        f'margin:0 0 16px 0;background:{BG};">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>'
    )


def mk(t):
    return f'<strong><span class="swl-marker mark_pink">{t}</span></strong>'


def mk_big(t):
    return f'<strong><span class="swl-marker mark_pink" style="font-size:1.15em;">{t}</span></strong>'


def a(href, text):
    return f'<a href="{href}" target="_blank" rel="noopener">{text}</a>'


# ============================== JP ==============================
JP_TITLE = "【YOSHIKI】好きなスタバは？ヨントンで明かした定番！"
JP_CONTENT = "\n\n".join([
    para(
        "KO1KEYZ(コイキーズ)のYOSHIKIは、スタバでいつも何を頼んでいるのでしょうか。",
        f"答えは、2026年9月13日のヨントンでYOSHIKI本人が即答した{mk_big('「ほうじ茶 & クラシックティー ラテ」')}です。",
        "この記事では、YOSHIKIが明かした定番ドリンクの中身と価格、同じ一杯を頼むときのポイント、ヨントンで飛び出したもうひとつの“飲み物トーク”までまとめます。",
    ),
    toc_box("この記事でわかること", [
        "YOSHIKIがスタバでいつも飲んでいるドリンク",
        "ほうじ茶 & クラシックティー ラテの味・価格",
        "KOSUKEとの意外な共通点",
        "同じ一杯を頼むときのポイント",
        "ヨントンで話したお酒の好み",
    ]),
    para("※ヨントン(個別オンライントーク会)は映像が公開されていないため、言い回しは前後する場合があります。"),

    h2("YOSHIKIがスタバでいつも飲んでいるのは？"),
    mini([
        ("答え:", "ほうじ茶 & クラシックティー ラテ"),
        ("明かした場面:", "KO1KEYZ 1ST ONLINE TALK Day2(2026年9月13日)"),
    ]),
    para(
        "話題になったのは、デビュー前に行われた個別オンライントーク会「KO1KEYZ 1ST ONLINE TALK」の2日目です。",
        f"「スタバでいつも何飲む？」と聞かれたYOSHIKIは、迷うそぶりもなく{mk('「ほうじ茶クラシックティーラテ！」')}と答えました。",
        "考え込まずに商品名がすっと出てくるあたり、普段から本当によく頼んでいる一杯なのが伝わってきます。",
    ),
    para(
        "同じ時間には、タピオカドリンクの人気店「ゴンチャ」でいつも頼むものについても質問が飛んでいました。",
        "ただ、ヨントンは1人あたり数十秒と短く、こちらは時間切れで答えまでは聞き取れなかったそうです。",
        "ゴンチャ派の人にとっては気になるところで、次のトーク会で改めて答えが出てくるのを待ちたいですね。",
    ),
    para(
        "この回答が広まってからは、スタバで同じドリンクを頼み、YOSHIKIを表すケーキの絵文字を添えて写真をアップするKO1LY(KO1KEYZのファン)も相次ぎました。",
        "推しと同じものを味わえる手軽さもあって、ちょっとした“YOSHIKIドリンク”になりつつあります。",
    ),

    h2("「ほうじ茶 & クラシックティー ラテ」はどんなドリンク？"),
    mini([
        ("正式名:", "ほうじ茶 & クラシックティー ラテ(ホット/アイス)"),
        ("位置づけ:", "2024年6月12日から通年で飲める定番メニュー"),
    ]),
    para(
        "ほうじ茶 & クラシックティー ラテは、スターバックスのティーブランド「TEAVANA」のティーラテです。",
        "ほうじ茶2種類とブラックティー(紅茶)を合わせ、ホワイトモカ風味のシロップとフレッシュクリームを加えています。",
        f"ほうじ茶の香ばしさと紅茶のほどよい渋みに、クリーミーな甘さが重なるので、{mk('コーヒーが苦手な人でも飲みやすい')}のが魅力です。",
    ),
    para(
        "初登場は2021年6月の期間限定で、好評のうちに販売を終えていました。",
        "その後、2024年6月12日に再登場し、そのまま定番メニューの仲間入りを果たしています。",
        "季節限定ではないので、YOSHIKIと同じ一杯をいつでも注文できるのはうれしいポイントです。",
    ),
    spec_box("ほうじ茶 & クラシックティー ラテの価格(税込・店内利用)", [
        ("Short", "530円〜"),
        ("Tall", "570円〜"),
        ("Grande", "616円〜"),
        ("Venti", "660円〜"),
        ("温度", "ホット/アイスどちらも可"),
        ("購入先", f"全国のスターバックス店舗(一部店舗を除く)・公式アプリのモバイルオーダー／{a(MENU_URL, '公式メニューページ')}"),
    ]),
    para(
        "価格は2026年9月時点の公式メニューの表記で、表の金額は店内利用の価格で、持ち帰りは税率の違いで少し安くなります。",
        "一部店舗では価格が異なる場合もあるので、注文前にアプリで確認しておくと安心です。",
    ),

    h2("実はKOSUKEも同じドリンクを定番にしていた"),
    mini([
        ("共通点:", "KOSUKEもヨントンで「ほうじ茶 & クラシックティー ラテ」を定番に挙げている"),
    ]),
    para(
        "おもしろいのは、同じKO1KEYZのKOSUKEも、2026年9月23日のヨントンでこのドリンクを“よく飲む2杯”のひとつに挙げていたことです。",
        f"KOSUKEはもう1杯として抹茶 クリーム フラペチーノを挙げていて、詳しくは{a(L_KOSUKE_JP, 'KOSUKEのスタバ記事')}でまとめています。",
        f"メンバー2人の定番がそろって同じ一杯という偶然に、{mk('KO1KEYZ内での隠れた人気ドリンク')}なのでは、と思わず想像してしまいますね。",
    ),

    h2("YOSHIKIと同じ一杯を頼むときのポイント"),
    mini([
        ("おすすめ:", "まずはカスタムなしのそのままの味から"),
    ]),
    para(
        "YOSHIKIの回答には、ミルク変更やシロップ追加といったカスタマイズの話は出てきませんでした。",
        "同じ一杯を味わいたいなら、まずは何も足さない基本のレシピで頼むのが一番近いはずです。",
    ),
    para(
        "ホットとアイスのどちらを飲んでいるかまでは明かされていないので、季節や気分で選んでみてください。",
        "慣れてきたら、公式もすすめているホイップクリームやソースの追加で、自分好みにアレンジするのも楽しい飲み方です。",
        "店舗によってははちみつを自由にかけられるので、甘さを足したい人は試してみる価値があります。",
    ),

    h2("お酒ならチャミスル？ヨントンで出たもうひとつの“飲み物トーク”"),
    mini([
        ("おすすめのお酒:", "韓国焼酎「チャミスル」"),
    ]),
    para(
        "同じDay2のヨントンでは、スタバ以外にも飲み物の話題がありました。",
        f"「20歳になるからおすすめのお酒を教えて」とお願いされたYOSHIKIが挙げたのは、{mk('韓国焼酎の「チャミスル」')}です。",
    ),
    para(
        "別の回でも「じゃあ何飲も？」という流れで、関西弁まじりに「チャミスル！」と答える場面がありました。",
        "奈良県出身のYOSHIKIらしい、ふっと出る関西のイントネーションも含めて、ファンにはたまらないやり取りだったようです。",
        "カフェではやさしい甘さのティーラテ、お酒ならチャミスルと、飲み物の好みからも素顔がのぞきます。",
    ),

    h2("YOSHIKI(矢田佳暉)はどんな人？"),
    spec_box("YOSHIKIのプロフィール", [
        ("本名", "矢田佳暉(やだ よしき)"),
        ("生年月日", "2004年6月18日"),
        ("出身地", "奈良県"),
        ("身長", "177cm"),
        ("メンバーカラー", "ピンク"),
        ("日プでの成績", "『PRODUCE 101 JAPAN 新世界』最終順位2位でデビュー"),
    ]),
    para(
        "YOSHIKIは、BS日テレの歌番組『現役歌王JAPAN』でTOP10に残った経歴を持つ、低音ボイスが持ち味のボーカリストです。",
        "一方で、ヨントンでは猫になりきったり甘えた声を見せたりと、かわいらしい一面でもファンを沸かせています。",
        f"経歴は{a(L_WIKI_JP, 'YOSHIKIのwiki風経歴記事')}、ヨントンでのほかの神対応は{a(L_TALK_JP, 'YOSHIKIのトーク会記事')}で紹介しています。",
    ),

    h2("まとめ"),
    summary_box("YOSHIKIのスタバ定番まとめ", [
        "YOSHIKIがスタバでいつも飲んでいるのは「ほうじ茶 & クラシックティー ラテ」",
        "2026年9月13日のヨントン(1ST ONLINE TALK Day2)で本人が即答",
        "ほうじ茶2種×紅茶にクリーミーな甘さを合わせた通年メニューで、Tall570円〜(税込)",
        "KOSUKEも同じドリンクを定番に挙げている",
        "ゴンチャの定番は時間切れで答えが聞き取れず、まだ分かっていない",
        "おすすめのお酒は韓国焼酎「チャミスル」",
    ]),
    para(
        "次にスタバへ行くときは、YOSHIKIと同じほうじ茶 & クラシックティー ラテを片手に、KO1KEYZの曲を聴きながらひと息ついてみてはいかがでしょうか！",
    ),
    related_box("YOSHIKI(矢田佳暉)の関連記事", [
        (L_TALK_JP, "【YOSHIKI】好きなタイプは？トーク会で語った猫カフェデート！"),
        (L_CAT_JP, "YOSHIKIの猫の名前は？KO1KEYZオフライントーク会で判明"),
        (L_DAIWAN_JP, "YOSHIKIが中国キャラ「大湾鶏」に似てる？まさかの本人も知ってた！"),
        (L_WIKI_JP, "矢田佳暉のwiki風経歴は？現役歌王TOP10の実力者"),
        (L_GAKU_JP, "矢田佳暉の学歴は？奈良県内の小・中・高校出身で軽音楽部所属！"),
        (L_KOSUKE_JP, "【KOSUKE】好きなスタバは？本人が明かした定番と新作！"),
        (L_MATOME_JP, "KO1KEYZ初のヨントン！メンバー12人の神対応を総まとめ！"),
    ]),
])
JP_SUMMARY = (
    "コイキーズ・YOSHIKIがヨントンで明かしたスタバの定番は「ほうじ茶 & クラシックティー ラテ」。"
    "味や価格、KOSUKEとの共通点、おすすめのお酒チャミスルの話までまとめました。"
)

# ============================== KR ==============================
KR_TITLE = "YOSHIKI가 좋아하는 스타벅스는? 영통에서 밝힌 단골 메뉴!"
KR_CONTENT = "\n\n".join([
    para(
        "KO1KEYZ(코이키즈)의 YOSHIKI는 스타벅스에서 평소 무엇을 주문할까요?",
        f"정답은 2026년 9월 13일 영통에서 YOSHIKI 본인이 바로 대답한 {mk_big('\'호지차 & 클래식 티 라떼\'')}입니다.",
        "이 글에서는 YOSHIKI가 밝힌 단골 음료의 맛과 가격, 같은 음료를 주문할 때의 팁, 그리고 영통에서 나온 또 하나의 '음료 토크'까지 정리합니다.",
    ),
    toc_box("이 글에서 알 수 있는 것", [
        "YOSHIKI가 스타벅스에서 늘 마시는 음료",
        "호지차 & 클래식 티 라떼의 맛・가격",
        "KOSUKE와의 의외의 공통점",
        "같은 음료를 주문할 때의 팁",
        "영통에서 이야기한 술 취향",
    ]),
    para("※영통(개별 온라인 토크회)은 영상이 공개되지 않아 표현이 조금 다를 수 있습니다."),

    h2("YOSHIKI가 스타벅스에서 늘 마시는 음료는?"),
    mini([
        ("정답:", "호지차 & 클래식 티 라떼"),
        ("밝힌 장면:", "KO1KEYZ 1ST ONLINE TALK Day2(2026년 9월 13일)"),
    ]),
    para(
        "화제가 된 것은 데뷔 전에 진행된 개별 온라인 토크회 'KO1KEYZ 1ST ONLINE TALK' 둘째 날입니다.",
        f"\"스타벅스에서 늘 뭐 마셔?\"라는 질문에 YOSHIKI는 망설임 없이 {mk('\"호지차 클래식 티 라떼!\"')}라고 답했습니다.",
        "고민 없이 메뉴 이름이 바로 나오는 걸 보면, 평소에도 정말 자주 주문하는 음료라는 게 느껴집니다.",
    ),
    para(
        "같은 통화에서는 버블티 인기 매장 '공차'에서 늘 주문하는 메뉴에 대한 질문도 있었습니다.",
        "하지만 영통은 1인당 수십 초로 짧아, 이쪽은 시간이 끝나 답을 알아듣지 못했다고 합니다.",
        "공차파라면 궁금할 부분이니, 다음 토크회에서 다시 답이 나오기를 기다려 봐요.",
    ),
    para(
        "이 답변이 알려진 뒤로는 스타벅스에서 같은 음료를 주문하고, YOSHIKI를 뜻하는 케이크 이모지를 붙여 사진을 올리는 KO1LY(KO1KEYZ 팬)도 잇따랐습니다.",
        "최애와 같은 음료를 쉽게 맛볼 수 있다는 점에서, 작은 'YOSHIKI 음료'가 되어 가고 있습니다.",
    ),

    h2("'호지차 & 클래식 티 라떼'는 어떤 음료?"),
    mini([
        ("정식 명칭:", "호지차 & 클래식 티 라떼(핫/아이스)"),
        ("위치:", "2024년 6월 12일부터 일 년 내내 마실 수 있는 정규 메뉴"),
    ]),
    para(
        "호지차 & 클래식 티 라떼는 스타벅스 재팬의 티 브랜드 'TEAVANA'의 티 라떼입니다.",
        "호지차 2종과 블랙티(홍차)를 합치고, 화이트 모카 풍미 시럽과 프레시 크림을 더했습니다.",
        f"호지차의 고소함과 홍차의 적당한 떫은맛에 크리미한 단맛이 겹쳐, {mk('커피를 못 마시는 사람도 마시기 좋은')} 것이 매력입니다.",
    ),
    para(
        "첫 등장은 2021년 6월 기간 한정이었고, 호평 속에 판매를 마쳤습니다.",
        "이후 2024년 6월 12일에 다시 등장해 그대로 정규 메뉴가 되었습니다.",
        "계절 한정이 아니라서 YOSHIKI와 같은 음료를 언제든 주문할 수 있다는 점이 반갑습니다.",
    ),
    spec_box("호지차 & 클래식 티 라떼 가격(세금 포함・매장 이용)", [
        ("Short", "530엔~"),
        ("Tall", "570엔~"),
        ("Grande", "616엔~"),
        ("Venti", "660엔~"),
        ("온도", "핫/아이스 모두 가능"),
        ("구입처", f"일본 전국 스타벅스 매장(일부 제외)・공식 앱 모바일 오더 / {a(MENU_URL, '공식 메뉴 페이지')}"),
    ]),
    para(
        "가격은 2026년 9월 기준 공식 메뉴 표기이며, 표의 금액은 매장 이용 가격이며, 포장은 세율 차이로 조금 저렴해집니다.",
        "일부 매장은 가격이 다를 수 있으니, 주문 전에 앱으로 확인해 두면 안심입니다.",
    ),

    h2("사실 KOSUKE도 같은 음료를 단골로 꼽았다"),
    mini([
        ("공통점:", "KOSUKE도 영통에서 '호지차 & 클래식 티 라떼'를 단골 메뉴로 꼽음"),
    ]),
    para(
        "재미있는 점은 같은 KO1KEYZ의 KOSUKE도 2026년 9월 23일 영통에서 이 음료를 '자주 마시는 두 잔' 중 하나로 꼽았다는 것입니다.",
        f"KOSUKE는 다른 한 잔으로 말차 크림 프라푸치노를 골랐고, 자세한 내용은 {a(L_KOSUKE_KR, 'KOSUKE의 스타벅스 기사')}에 정리했습니다.",
        f"두 멤버의 단골이 같은 음료라는 우연에, {mk('KO1KEYZ 안에서 숨은 인기 음료')}가 아닐까 하는 상상도 하게 되네요.",
    ),

    h2("YOSHIKI와 같은 음료를 주문할 때의 팁"),
    mini([
        ("추천:", "먼저 커스텀 없이 기본 맛으로"),
    ]),
    para(
        "YOSHIKI의 답변에는 우유 변경이나 시럽 추가 같은 커스터마이즈 이야기는 나오지 않았습니다.",
        "같은 음료를 맛보고 싶다면, 먼저 아무것도 더하지 않은 기본 레시피로 주문하는 것이 가장 가까울 것입니다.",
    ),
    para(
        "핫과 아이스 중 무엇을 마시는지는 밝혀지지 않았으니, 계절이나 기분에 따라 골라 보세요.",
        "익숙해지면 공식적으로도 추천하는 휘핑크림이나 소스 추가로 내 취향에 맞게 바꿔 보는 것도 즐거운 방법입니다.",
        "매장에 따라 꿀을 자유롭게 넣을 수 있으니, 단맛을 더하고 싶다면 시도해 볼 만합니다.",
    ),

    h2("술은 참이슬? 영통에서 나온 또 하나의 '음료 토크'"),
    mini([
        ("추천 술:", "한국 소주 '참이슬'"),
    ]),
    para(
        "같은 Day2 영통에서는 스타벅스 말고도 음료 이야기가 있었습니다.",
        f"\"스무 살이 되니까 추천하는 술을 알려줘\"라는 부탁에 YOSHIKI가 꼽은 것은 {mk('한국 소주 \'참이슬\'')}입니다.",
    ),
    para(
        "다른 통화에서도 \"그럼 뭐 마실까?\"라는 흐름에서 간사이 사투리 섞인 말투로 \"참이슬!\"이라고 답하는 장면이 있었습니다.",
        "나라현 출신 YOSHIKI다운, 무심코 나오는 간사이 억양까지 팬들에게는 참을 수 없는 대화였던 것 같습니다.",
        "카페에서는 부드럽고 달콤한 티 라떼, 술은 참이슬. 음료 취향에서도 꾸밈없는 모습이 엿보입니다.",
    ),

    h2("YOSHIKI(야다 요시키)는 어떤 사람?"),
    spec_box("YOSHIKI 프로필", [
        ("본명", "야다 요시키(矢田佳暉)"),
        ("생년월일", "2004년 6월 18일"),
        ("출신지", "나라현"),
        ("키", "177cm"),
        ("멤버컬러", "핑크"),
        ("프로듀스101재팬 성적", "『PRODUCE 101 JAPAN 신세계』 최종 2위로 데뷔"),
    ]),
    para(
        "YOSHIKI는 BS닛테레 노래 프로그램 '현역가왕 JAPAN'에서 TOP10에 오른 경력을 가진, 저음 보이스가 매력인 보컬리스트입니다.",
        "한편 영통에서는 고양이 흉내를 내거나 애교 섞인 목소리를 들려주는 등 귀여운 모습으로도 팬들을 설레게 하고 있습니다.",
        f"학창 시절 이야기는 {a(L_GAKU_KR, 'YOSHIKI의 학력 기사')}에서 소개하고 있습니다.",
    ),

    h2("정리"),
    summary_box("YOSHIKI의 스타벅스 단골 정리", [
        "YOSHIKI가 스타벅스에서 늘 마시는 음료는 '호지차 & 클래식 티 라떼'",
        "2026년 9월 13일 영통(1ST ONLINE TALK Day2)에서 본인이 바로 답변",
        "호지차 2종×홍차에 크리미한 단맛을 더한 정규 메뉴로, Tall 570엔~(세금 포함)",
        "KOSUKE도 같은 음료를 단골로 꼽음",
        "공차 단골 메뉴는 시간이 끝나 답을 듣지 못해 아직 알 수 없음",
        "추천 술은 한국 소주 '참이슬'",
    ]),
    para(
        "다음에 스타벅스에 간다면, YOSHIKI와 같은 호지차 & 클래식 티 라떼를 들고 KO1KEYZ 노래를 들으며 한숨 돌려 보는 건 어떨까요!",
    ),
    related_box("YOSHIKI(야다 요시키) 관련 글", [
        (L_GAKU_KR, "야다 요시키의 학력은? 나라현 내 초・중・고 출신으로 경음악부 소속!"),
        (L_KOSUKE_KR, "KOSUKE가 좋아하는 스타벅스는? 본인이 밝힌 단골과 신메뉴!"),
        (L_TALK_JP, "YOSHIKI 토크회 기사: 이상형과 고양이 카페 데이트(일본어)"),
        (L_WIKI_JP, "야다 요시키의 경력 정리(일본어)"),
    ]),
])
KR_SUMMARY = (
    "코이키즈 YOSHIKI가 영통에서 밝힌 스타벅스 단골 메뉴는 '호지차 & 클래식 티 라떼'. "
    "맛과 가격, KOSUKE와의 공통점, 추천 술 참이슬 이야기까지 정리했습니다."
)

# ============================== EN ==============================
EN_TITLE = "YOSHIKI's Go-To Starbucks Drink, Revealed at His Yeontong!"
EN_CONTENT = "\n\n".join([
    para(
        "What does KO1KEYZ's YOSHIKI usually order at Starbucks?",
        f"The answer is the {mk_big('Hojicha & Classic Tea Latte')}, which YOSHIKI named without hesitation during a yeontong on September 13, 2026.",
        "This article covers what's in the drink and what it costs, tips for ordering the same cup, and one more drink-related moment from his yeontong.",
    ),
    toc_box("What you'll learn", [
        "The drink YOSHIKI always orders at Starbucks",
        "What the Hojicha & Classic Tea Latte tastes like and costs",
        "A surprising thing he has in common with KOSUKE",
        "Tips for ordering the same drink",
        "His pick when it comes to alcohol",
    ]),
    para("*Yeontong (one-on-one online video call) sessions are not publicly recorded, so exact wording may vary slightly."),

    h2("What does YOSHIKI always drink at Starbucks?"),
    mini([
        ("Answer: ", "Hojicha & Classic Tea Latte"),
        ("When: ", "KO1KEYZ 1ST ONLINE TALK Day 2 (September 13, 2026)"),
    ]),
    para(
        "It came up on the second day of \"KO1KEYZ 1ST ONLINE TALK,\" the one-on-one online video call event held ahead of the group's debut.",
        f"Asked \"What do you always get at Starbucks?\", YOSHIKI answered right away: {mk('\"Hojicha Classic Tea Latte!\"')}",
        "The way the name came out instantly suggests it really is something he orders all the time.",
    ),
    para(
        "In the same session, he was also asked about his usual order at the bubble tea chain Gong cha.",
        "But each yeontong lasts only a few dozen seconds, and time ran out before that answer could be caught.",
        "Gong cha fans will have to wait for another talk event to find out.",
    ),
    para(
        "Once his answer spread, a wave of KO1LY (KO1KEYZ fans) ordered the same drink and shared photos with the cake emoji that stands for YOSHIKI.",
        "Since it's so easy to try, it's quickly becoming a little \"YOSHIKI drink.\"",
    ),

    h2("What is the Hojicha & Classic Tea Latte?"),
    mini([
        ("Official name: ", "Hojicha & Classic Tea Latte (hot or iced)"),
        ("Status: ", "A year-round regular menu item since June 12, 2024"),
    ]),
    para(
        "The Hojicha & Classic Tea Latte is a tea latte from TEAVANA, Starbucks Japan's tea line.",
        "It blends two kinds of hojicha (roasted green tea) with black tea, then adds white mocha-flavored syrup and fresh cream.",
        f"The toasty hojicha and gentle black-tea astringency meet a creamy sweetness, making it {mk('easy to enjoy even if you are not a coffee drinker')}.",
    ),
    para(
        "It first appeared as a limited-time item in June 2021 and sold out to strong reviews.",
        "It returned on June 12, 2024, and has stayed on the regular menu ever since.",
        "Because it isn't seasonal, you can order the same drink as YOSHIKI any time of year.",
    ),
    spec_box("Hojicha & Classic Tea Latte prices (tax incl., dine-in)", [
        ("Short", "From JPY 530"),
        ("Tall", "From JPY 570"),
        ("Grande", "From JPY 616"),
        ("Venti", "From JPY 660"),
        ("Temperature", "Hot or iced"),
        ("Where to buy", f"Starbucks stores across Japan (excluding some locations) and mobile order on the official app / {a(MENU_URL, 'official menu page')}"),
    ]),
    para(
        "Prices are as listed on the official menu as of September 2026; the table shows dine-in prices, and takeout is slightly cheaper due to a lower tax rate.",
        "Some stores may price it differently, so it's worth checking the app before you order.",
    ),

    h2("KOSUKE counts the same drink as a regular"),
    mini([
        ("In common: ", "KOSUKE also named the Hojicha & Classic Tea Latte as a regular at his yeontong"),
    ]),
    para(
        "Interestingly, fellow member KOSUKE also named this drink as one of his two usual orders during a yeontong on September 23, 2026.",
        f"His other pick was the Matcha Cream Frappuccino; see {a(L_KOSUKE_EN, 'our KOSUKE Starbucks article')} for details.",
        f"With two members sharing the same go-to, it's hard not to wonder if it's {mk('a quiet favorite inside KO1KEYZ')}.",
    ),

    h2("Tips for ordering the same drink as YOSHIKI"),
    mini([
        ("Our pick: ", "Start with the standard recipe, no customizations"),
    ]),
    para(
        "YOSHIKI didn't mention any customizations such as a milk swap or extra syrup.",
        "If you want to taste what he drinks, the plain standard recipe is likely the closest match.",
    ),
    para(
        "He didn't say whether he drinks it hot or iced, so pick whichever suits the season or your mood.",
        "Once you know the base flavor, adding whipped cream or a sauce, as Starbucks itself suggests, is a fun way to make it your own.",
        "Some stores also have self-serve honey, which is worth a try if you like it sweeter.",
    ),

    h2("Chamisul for drinks? Another beverage moment from his yeontong"),
    mini([
        ("Recommended drink: ", "Korean soju \"Chamisul\""),
    ]),
    para(
        "Starbucks wasn't the only drink topic on Day 2.",
        f"When asked to recommend an alcoholic drink for someone about to turn 20, YOSHIKI picked {mk('the Korean soju \"Chamisul\"')}.",
    ),
    para(
        "In another session, when the conversation turned to \"So what should we drink?\", he again answered \"Chamisul!\" with a touch of Kansai dialect.",
        "That casual hint of his hometown accent (he's from Nara Prefecture) made the exchange all the more special for fans.",
        "A gentle, sweet tea latte at the café and Chamisul for drinks: even his beverage choices show a down-to-earth side.",
    ),

    h2("Who is YOSHIKI (Yoshiki Yada)?"),
    spec_box("YOSHIKI's profile", [
        ("Real name", "Yoshiki Yada"),
        ("Birthday", "June 18, 2004"),
        ("Hometown", "Nara Prefecture"),
        ("Height", "177cm"),
        ("Member color", "Pink"),
        ("Produce 101 Japan result", "Debuted after finishing 2nd on PRODUCE 101 JAPAN: THE NEW WORLD"),
    ]),
    para(
        "YOSHIKI is a vocalist known for his low voice, and he previously made the Top 10 on BS Nippon TV's singing show \"Gen'eki Kaō JAPAN.\"",
        "At yeontong events, he has also delighted fans with a cuter side, like playing a cat or putting on a sweet voice.",
        f"For his school background, see {a(L_GAKU_EN, 'our article on YOSHIKI’s school history')}.",
    ),

    h2("Summary"),
    summary_box("YOSHIKI's Starbucks order, summarized", [
        "YOSHIKI's go-to Starbucks drink is the Hojicha & Classic Tea Latte",
        "He answered instantly at a yeontong on September 13, 2026 (1ST ONLINE TALK Day 2)",
        "A year-round tea latte of two hojicha teas and black tea with creamy sweetness, Tall from JPY 570 (tax incl.)",
        "KOSUKE also named the same drink as a regular",
        "His Gong cha order is still unknown because time ran out",
        "His recommended alcohol: the Korean soju Chamisul",
    ]),
    para(
        "Next time you're at Starbucks, why not grab the same Hojicha & Classic Tea Latte as YOSHIKI and take a break with some KO1KEYZ songs?",
    ),
    related_box("More about YOSHIKI (Yoshiki Yada)", [
        (L_GAKU_EN, "Yoshiki Yada's school history: elementary, middle, and high school in Nara"),
        (L_DAIWAN_EN, "Does YOSHIKI look like China's \"Daiwanji\"? He already knew!"),
        (L_KOSUKE_EN, "KOSUKE's favorite Starbucks: regulars and new pick, revealed"),
        (L_WIKI_JP, "Yoshiki Yada's career profile (in Japanese)"),
    ]),
])
EN_SUMMARY = (
    "KO1KEYZ's YOSHIKI revealed his go-to Starbucks drink at a yeontong: the Hojicha & Classic Tea Latte. "
    "We cover the taste, prices, what he shares with KOSUKE, and his Chamisul pick."
)


# ============================== POST ==============================
def make_eyecatch(bottoms, out_name, seed, lang=None):
    out = ROOT / "images" / out_name
    cmd = [sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
           "--top", "KO1KEYZ", "--main", "YOSHIKI"]
    for b in bottoms:
        cmd += ["--bottom", b]
    cmd += ["--out", str(out), "--seed", str(seed)]
    if lang:
        cmd += ["--lang", lang]
    subprocess.run(cmd, check=True)
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HA, "Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{out_name}"'},
        data=out.read_bytes(),
    )
    r.raise_for_status()
    return r.json()["id"]


def post_draft(title, content, slug, lang, cats, media, summary, ja_id=None):
    payload = {
        "title": title, "content": content, "slug": slug, "status": "draft", "lang": lang,
        "categories": cats, "featured_media": media, "author": 2,
        "meta": {"jetpack_publicize_message": summary},
    }
    if ja_id:
        payload["translations"] = {"ja": ja_id}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers={**HA, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    for name, t, c in (("JP", JP_TITLE, JP_CONTENT), ("KR", KR_TITLE, KR_CONTENT), ("EN", EN_TITLE, EN_CONTENT)):
        assert "<hr" not in c
        text = re.sub(r"<!--.*?-->|<[^>]+>", "", c, flags=re.S)
        print(name, "title len:", len(t), "| chars:", len(text))
    if "--dry" in sys.argv:
        sys.exit(0)
    jp_eye = make_eyecatch(["スタバでいつも何飲む？", "本人が即答した定番ドリンク！"],
                           "ko1keyz_yoshiki_starbucks_hojicha_eyecatch.png", seed=618)
    kr_eye = make_eyecatch(["스타벅스에서 늘 뭐 마셔?", "본인이 바로 답한 단골 메뉴!"],
                           "ko1keyz_yoshiki_starbucks_hojicha_eyecatch_kr.png", seed=618, lang="kr")
    jp = post_draft(JP_TITLE, JP_CONTENT, BASE_SLUG, "ja", [66, 63, 84], jp_eye, JP_SUMMARY)
    JP_ID = jp["id"]
    print("JP", JP_ID, jp["slug"], f"{WP_URL}/?p={JP_ID}", "media", jp_eye)
    kr = post_draft(KR_TITLE, KR_CONTENT, BASE_SLUG + "-kr", "ko", [74, 78], kr_eye, KR_SUMMARY, JP_ID)
    print("KR", kr["id"], kr["slug"], f"{WP_URL}/?p={kr['id']}", "media", kr_eye)
    en = post_draft(EN_TITLE, EN_CONTENT, BASE_SLUG + "-en", "en", [110, 118], jp_eye, EN_SUMMARY, JP_ID)
    print("EN", en["id"], en["slug"], f"{WP_URL}/?p={en['id']}", "media", jp_eye)
    (ROOT / "tmp_yoshiki_starbucks_ids.txt").write_text(
        f"jp={JP_ID} kr={kr['id']} en={en['id']} jp_eye={jp_eye} kr_eye={kr_eye}\n", encoding="utf-8")
