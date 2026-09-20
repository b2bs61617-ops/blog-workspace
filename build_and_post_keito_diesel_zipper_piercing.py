# -*- coding: utf-8 -*-
"""KEITO(小野慶人)がプラチャでつけていたDIESELのジッパー型ピアス記事。
chomoand-1.com に JP + KR + EN の下書きを作る(本文画像なし・アイキャッチのみ)。

python build_and_post_keito_diesel_zipper_piercing.py
"""
import base64
import json
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

EYE_JP = ROOT / "images" / "ko1keyz_keito_diesel_zipper_piercing_eyecatch.png"
EYE_KR = ROOT / "images" / "ko1keyz_keito_diesel_zipper_piercing_eyecatch_kr.png"
BASE_SLUG = "keito-diesel-zipper-piercing"

# KEITO=オレンジ(Miu Miu記事と同じ配色)
A = "#e0812f"
BG = "#fdf6ee"
SOFT = "#f2ddc4"

L_PIERCE = "https://chomoand-1.com/how-many-piercings-do-ko1keyz-12030"
L_MIUMIU = "https://chomoand-1.com/what-shirt-did-keito-wear-on-t-11924"
L_ARIMINO = "https://chomoand-1.com/keito-arimino-spiceplus-package-11994"
L_NIGHT = "https://chomoand-1.com/how-much-does-ko1keyz-keitos-f-11083"
DIESEL = "https://www.diesel.co.jp/"
ZOZO = "https://zozo.jp/brand/diesel/"


def get_link(pid):
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?_fields=link", headers=HA)
    r.raise_for_status()
    return r.json()["link"]


L_PIERCE_KR = get_link(12034)
L_PIERCE_EN = get_link(12038)


# ---------- HTML部品 ----------
def para(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def html_block(inner):
    return f"<!-- wp:html -->\n{inner}\n<!-- /wp:html -->"


def spec_box(title, rows):
    trs = "\n".join(
        f'<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:32%;">{k}</td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return html_block(
        '<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>\n'
        f'<table style="border-collapse:collapse;width:100%;">\n{trs}\n</table>\n</div>'
    )


def note_box(title, body_html):
    return html_block(
        f'<div style="border:1px solid {SOFT};border-left:4px solid {A};border-radius:4px;padding:14px 18px;'
        f'margin:0 0 16px 0;background:{BG};">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n'
        f'<p style="margin:0;">{body_html}</p>\n</div>'
    )


def titlebar_list(title, items):
    lis = "\n".join(f'<li style="margin:0 0 8px 0;">{i}</li>' for i in items)
    return html_block(
        f'<div style="border:1px solid {SOFT};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">{title}</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">\n{lis}\n</ul>\n</div>'
    )


def summary_box(items):
    body = "<br>\n".join(f"&#10003; {i}" for i in items)
    return html_block(
        f'<div style="border:2px solid {A};border-radius:8px;background:rgba(224,129,47,0.08);padding:1em 1.25em;margin:0 0 16px 0;">\n'
        f'<p style="margin:0;">\n{body}\n</p>\n</div>'
    )


def related_box(title, links):
    lis = "\n".join(f'<li><a href="{u}">{t}</a></li>' for u, t in links)
    return html_block(
        f'<div style="border:1px solid {SOFT};border-left:4px solid {A};border-radius:4px;padding:14px 18px;'
        f'margin:0 0 16px 0;background:{BG};">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>'
    )


def mk(t):
    return f'<span class="swl-marker mark_orange">{t}</span>'


def mk_big(t):
    return f'<span class="swl-marker mark_orange" style="font-size:1.15em;"><strong>{t}</strong></span>'


# ============================== JP ==============================
JP_TITLE = "KEITOのジッパーピアスはどこの？プラチャでDIESELと判明！"
JP_CONTENT = "\n\n".join([
    para(
        "KO1KEYZ(コイキーズ)のKEITO(小野慶人)が、9月19日に届いたファンクラブ向けの「KO1KEYZ Chat(プラチャ)」の写真で、"
        "耳元に<strong>ジッパー(チャック)の引き手</strong>のようなピアスを着けていて、「どこのブランド？」と話題になっています。",
        f"調べたところ、このピアスはDIESEL(ディーゼル)の「ピアス(両耳用)」と形が一致し、参考価格は{mk_big('16,500円(税込)')}でした。",
        "この記事では、ピアスのデザインの特徴、DIESELと言える決め手、これまでのKEITOのピアスとの違い、買える場所までまとめます。",
    ),
    spec_box("KEITOのジッパー型ピアス 基本情報", [
        ("ブランド", "DIESEL(ディーゼル／イタリア)"),
        ("アイテム", "ピアス(両耳用)。左右でデザインが違う2個セット"),
        ("デザイン", "ジッパーの引き手(プル)型と、ロゴ入りの丸いボタン型"),
        ("参考価格", "16,500円(税込)"),
        ("確認できた場面", "2026年9月19日のプラチャ(KO1KEYZ Chat)の写真"),
    ]),
    h2("KEITOのジッパー型ピアスはどこで確認できた？"),
    para(
        "話題になっているのは、9月19日に届いたプラチャの写真です。",
        "髪の隙間から見える耳たぶに、銀色のジッパーの引き手がすっとぶら下がっていて、ひと目で「チャックみたい」と気づくほど存在感があります。",
        "「ジッパーのピアスってかわいい」「どこのブランド？」と、ファンの間でも耳元に注目が集まりました。",
    ),
    para(
        "プラチャはファンクラブ会員向けの配信のため、写真の掲載は控えます。",
        "衣装撮影ではなく普段の姿を届ける場ですが、本人が購入の経緯などに触れているわけではないので、私物かスタイリストが用意したものかまでは分かりません。",
    ),
    h2("DIESELのジッパー型ピアスはどんなデザイン？"),
    para(
        "DIESEL公式オンラインストアに掲載されている「ピアス(両耳用)」は、<strong>左右でデザインが違う2個セット</strong>です。",
        "片方がジッパーの引き手(プル)、もう片方がDIESELのロゴが入った丸いボタンをかたどっています。",
    ),
    para(
        "ジッパー側は、上に四角いスライダー(引き手の金具)、下に向かって細くなる台形のフォルム、下端に抜けた穴があり、面には「DIESEL」のロゴが縦向きに浮き彫りされています。",
        "ボタン側は、円のふちに沿って「FOR SUCCESSFUL LIVING」の文字が並び、中央にブランドのロゴがあしらわれたデザインです。",
        "耳に留めるのはスタッド(post)タイプで、ジッパー側は留め具の真下にプルが垂れ下がる作りです。",
    ),
    note_box(
        "DIESEL(ディーゼル)とは？",
        "1978年にイタリアで生まれたデニム発のファッションブランド。<br>"
        "ジッパーやリベット、ボタンといった洋服のパーツをそのままアクセサリーやバッグのデザインに落とし込むのが得意で、"
        "ピアスのジッパーとボタンもその流れにあるアイテムです。<br>"
        "「FOR SUCCESSFUL LIVING(成功のための暮らし)」はブランドのスローガンとして知られています。",
    ),
    h2("KEITOのピアスがDIESELと言える決め手は？"),
    para(
        "ジッパー型のピアスは雑貨ブランドやハンドメイドにも数多くあり、写真からロゴの文字までは読み取れません。",
        "ただ、形の細かい部分を見比べると、DIESELの商品画像と重なる点がいくつもあります。",
    ),
    titlebar_list("見比べた3つのポイント", [
        "<strong>引き手の形</strong>:上が四角いスライダーで、下に向かって細くなる台形。下側に台形の穴が抜けている",
        "<strong>ぶら下がり方</strong>:耳に留める丸い土台の真下にプルがぶら下がり、耳たぶから垂れる構造",
        "<strong>質感と大きさ</strong>:光沢のあるシルバーで、耳たぶにおさまるコンパクトなサイズ感",
    ]),
    para(
        "3点とも一致していて、公式ストアで16,500円で取り扱われている形でもあることから、KEITOのピアスはDIESELのジッパー型と考えてよさそうです。",
        "ただし、ブランドや商品名について本人から公表があったわけではありません。",
    ),
    h2("KEITOのピアスはこれまでと変わった？"),
    para(
        "6月ごろの映像や写真では、KEITOの耳たぶには小さく光るシンプルなピアスが着いていて、髪の隙間からちらりと見える程度でした。",
        "9月のファンミーティングでも、髪の陰でピアスがきらめく姿が見られています。",
        "それに対して今回のジッパーは引き手が下に垂れるモチーフで、耳元の印象はぐっと大きく変わりました。",
    ),
    para(
        f'KEITOのピアスは、<a href="{L_PIERCE}">KO1KEYZ12人のピアスの数をまとめた記事</a>では両耳合わせて2つです。',
        "DIESELのピアスはちょうど2個セットなので、両耳に1つずつ着けている可能性もありますが、もう片耳の様子は今回の写真では確認できませんでした。",
        "セットのうちジッパー側だけを片耳に着けて、ワンポイントとして遊ぶ着こなしもできそうです。",
    ),
    h2("値段は？どこで買える？"),
    para(
        f"DIESEL公式オンラインストアでの参考価格は{mk_big('16,500円(税込)')}で、左右セットの値段です。",
        "同じDIESELの片耳用ピアスは1万円台前半のものが多く、ジッパーとボタンの2個入りとしては標準的な価格帯といえます。",
    ),
    titlebar_list("DIESELピアスの購入先", [
        f'<a href="{DIESEL}" target="_blank" rel="noopener">DIESEL公式オンラインストア</a>(ジュエリー・ピアスから「ピアス(両耳用)」を探す)',
        "DIESEL直営店・取扱店(店舗は公式サイトの店舗検索で確認)",
        f'<a href="{ZOZO}" target="_blank" rel="noopener">ZOZOTOWN</a>のDIESEL取扱ページ(ジュエリー・アクセサリー)',
    ]),
    para(
        "取扱状況や在庫は時期によって変わります。",
        "DIESELのピアスにはロゴ入りスタッドなど似た名前の別デザインも多いので、商品画像でジッパー型とボタン型の組み合わせかどうかを確認して選ぶと安心です。",
    ),
    h2("まとめ"),
    summary_box([
        "KEITOは9月19日のプラチャの写真で、ジッパーの引き手のような銀色のピアスを着けていた",
        "形が一致するのはDIESELの「ピアス(両耳用)」で、ジッパー型とロゴ入りボタン型の2個セット",
        "参考価格は16,500円(税込)。公式ストアや取扱店で探せる",
        "6月ごろの小さく光るピアスから、ぐっと個性的な耳元に変わった",
    ]),
    para(
        "髪の隙間からちらりと見えるだけでも、耳元の小さな変化で印象が変わるのがピアスの面白いところです。",
        "気になった人は、DIESELのジッパー型ピアスを一度手に取って眺めてみてはいかがでしょうか！",
    ),
    related_box("KEITO(小野慶人)の関連記事", [
        (L_PIERCE, "KO1KEYZ12人のピアスの数をまとめた記事"),
        (L_MIUMIU, "KEITOがTikTokのセルフィーで着ていたシャツを調べた記事"),
        (L_ARIMINO, "アリミノ スパイスプラスのパッケージモデルはKEITOか調べた記事"),
        (L_NIGHT, "KEITOのナイトルーティンで使っている美顔器を調べた記事"),
    ]),
])
JP_SUMMARY = (
    "KO1KEYZ・KEITOが9月19日のプラチャでつけていたジッパー型ピアスは、DIESELの「ピアス(両耳用)」と形が一致。"
    "ジッパーの引き手とロゴ入りボタンの2個セットで、参考価格は16,500円(税込)。特徴や見分けるポイント、購入先をまとめました。"
)

# ============================== KR ==============================
KR_TITLE = "KEITO의 지퍼 피어싱은 어디 거? 프라챗에서 DIESEL로 판명!"
KR_CONTENT = "\n\n".join([
    para(
        "KO1KEYZ(코이키즈)의 KEITO(오노 케이토)가 9월 19일 팬클럽 회원용 'KO1KEYZ Chat(프라챗)' 사진에서 "
        "<strong>지퍼(지퍼 손잡이)</strong> 모양의 피어싱을 하고 있어 '어느 브랜드지?' 하고 화제가 되고 있습니다.",
        f"확인해 보니 이 피어싱은 DIESEL(디젤)의 '피어싱(양쪽 귀용)'과 모양이 일치했고, 참고 가격은 {mk_big('16,500엔(세금 포함)')}이었습니다.",
        "이 글에서는 피어싱의 디자인 특징, DIESEL이라고 볼 수 있는 근거, 지금까지의 KEITO 피어싱과의 차이, 구매처까지 정리합니다.",
    ),
    spec_box("KEITO 지퍼 피어싱 기본 정보", [
        ("브랜드", "DIESEL(디젤/이탈리아)"),
        ("아이템", "피어싱(양쪽 귀용). 좌우 디자인이 다른 2개 세트"),
        ("디자인", "지퍼 손잡이(풀) 모양과 로고가 들어간 둥근 버튼 모양"),
        ("참고 가격", "16,500엔(세금 포함)"),
        ("확인된 장면", "2026년 9월 19일 프라챗(KO1KEYZ Chat) 사진"),
    ]),
    h2("KEITO의 지퍼 피어싱은 어디서 확인됐나?"),
    para(
        "화제가 된 것은 9월 19일에 올라온 프라챗 사진입니다.",
        "머리카락 사이로 보이는 귓불에 은색 지퍼 손잡이가 쓱 늘어져 있어, 한눈에 '지퍼 같다'고 알아볼 만큼 존재감이 있습니다.",
        "'지퍼 피어싱 귀엽다' '어디 브랜드지?' 하며 팬들 사이에서도 귓가에 시선이 모였습니다.",
    ),
    para(
        "프라챗은 팬클럽 회원 대상 서비스라 사진은 게재하지 않습니다.",
        "의상 촬영이 아니라 평소 모습을 전하는 자리이지만, 본인이 구매 경위 등을 언급한 것은 아니어서 개인 소지품인지 스타일리스트가 준비한 것인지는 알 수 없습니다.",
    ),
    h2("DIESEL 지퍼 피어싱은 어떤 디자인?"),
    para(
        "DIESEL 공식 온라인 스토어에 올라와 있는 '피어싱(양쪽 귀용)'은 <strong>좌우 디자인이 다른 2개 세트</strong>입니다.",
        "한쪽은 지퍼 손잡이(풀), 다른 한쪽은 DIESEL 로고가 들어간 둥근 버튼을 본뜬 모양입니다.",
    ),
    para(
        "지퍼 쪽은 위에 네모난 슬라이더, 아래로 갈수록 좁아지는 사다리꼴 형태, 하단에 뚫린 구멍이 있고, 면에는 'DIESEL' 로고가 세로로 양각되어 있습니다.",
        "버튼 쪽은 원 테두리를 따라 'FOR SUCCESSFUL LIVING' 문구가 이어지고 가운데에 브랜드 로고가 들어간 디자인입니다.",
        "귀에 고정하는 방식은 스터드(포스트) 타입이며, 지퍼 쪽은 잠금 부품 바로 아래로 풀이 늘어지는 구조입니다.",
    ),
    note_box(
        "DIESEL(디젤)이란?",
        "1978년 이탈리아에서 탄생한 데님 출신 패션 브랜드.<br>"
        "지퍼, 리벳, 버튼 같은 옷의 부품을 그대로 액세서리나 가방 디자인으로 옮기는 데 능하며, 이 피어싱의 지퍼와 버튼도 그 흐름의 아이템입니다.<br>"
        "'FOR SUCCESSFUL LIVING(성공을 위한 삶)'은 브랜드 슬로건으로 알려져 있습니다.",
    ),
    h2("KEITO의 피어싱이 DIESEL이라고 볼 수 있는 근거는?"),
    para(
        "지퍼 모양 피어싱은 잡화 브랜드나 핸드메이드에도 많고, 사진만으로는 로고 글자까지 읽을 수 없습니다.",
        "하지만 세부 형태를 비교해 보면 DIESEL 상품 이미지와 겹치는 점이 여러 개 있습니다.",
    ),
    titlebar_list("비교해 본 3가지 포인트", [
        "<strong>손잡이 모양</strong>: 위는 네모난 슬라이더, 아래로 갈수록 좁아지는 사다리꼴. 아래쪽에 사다리꼴 구멍이 뚫려 있음",
        "<strong>늘어지는 방식</strong>: 귀에 고정하는 둥근 받침 바로 아래로 풀이 매달려 귓불에서 늘어지는 구조",
        "<strong>질감과 크기</strong>: 광택이 있는 실버이고, 귓불에 들어가는 컴팩트한 크기",
    ]),
    para(
        "세 가지 모두 일치하고 공식 스토어에서 16,500엔에 판매되는 모양이기도 해서, KEITO의 피어싱은 DIESEL의 지퍼 타입으로 봐도 좋아 보입니다.",
        "다만 브랜드나 상품명에 대해 본인이 공표한 것은 아닙니다.",
    ),
    h2("KEITO의 피어싱은 예전과 달라졌나?"),
    para(
        "6월경 영상과 사진에서 KEITO의 귓불에는 작게 반짝이는 심플한 피어싱이 있었고, 머리카락 사이로 살짝 보이는 정도였습니다.",
        "9월 팬미팅에서도 머리카락 그늘에서 피어싱이 반짝이는 모습이 보였습니다.",
        "이에 비해 이번 지퍼는 손잡이가 아래로 늘어지는 모티프라 귓가의 인상이 크게 달라졌습니다.",
    ),
    para(
        f'KEITO의 피어싱은 <a href="{L_PIERCE_KR}">KO1KEYZ 12명의 피어싱 개수를 정리한 글</a>에서 양쪽 귀 합쳐 2개입니다.',
        "DIESEL 피어싱은 마침 2개 세트라 양쪽 귀에 하나씩 착용했을 가능성도 있지만, 반대쪽 귀는 이번 사진에서 확인되지 않았습니다.",
        "세트 중 지퍼 쪽만 한쪽 귀에 포인트로 착용하는 스타일링도 가능해 보입니다.",
    ),
    h2("가격은? 어디서 살 수 있나?"),
    para(
        f"DIESEL 공식 온라인 스토어의 참고 가격은 {mk_big('16,500엔(세금 포함)')}이며, 좌우 세트 가격입니다.",
        "같은 DIESEL의 한쪽 귀용 피어싱은 1만 엔대 초반이 많아, 지퍼와 버튼 2개 구성으로는 표준적인 가격대입니다.",
    ),
    titlebar_list("DIESEL 피어싱 구매처", [
        f'<a href="{DIESEL}" target="_blank" rel="noopener">DIESEL 공식 온라인 스토어</a>(주얼리·피어싱에서 \'피어싱(양쪽 귀용)\' 찾기)',
        "DIESEL 직영점·취급점(매장은 공식 사이트 매장 검색으로 확인)",
        f'<a href="{ZOZO}" target="_blank" rel="noopener">ZOZOTOWN</a> DIESEL 취급 페이지(주얼리·액세서리)',
    ]),
    para(
        "취급 상황과 재고는 시기에 따라 달라집니다.",
        "DIESEL 피어싱에는 로고 스터드 등 이름이 비슷한 다른 디자인도 많으니, 상품 이미지에서 지퍼형과 버튼형 조합인지 확인하고 고르면 안심입니다.",
    ),
    h2("정리"),
    summary_box([
        "KEITO는 9월 19일 프라챗 사진에서 지퍼 손잡이 같은 은색 피어싱을 착용했다",
        "모양이 일치하는 것은 DIESEL의 '피어싱(양쪽 귀용)'으로, 지퍼형과 로고 버튼형의 2개 세트",
        "참고 가격은 16,500엔(세금 포함). 공식 스토어와 취급점에서 찾을 수 있다",
        "6월경의 작게 반짝이던 피어싱에서 훨씬 개성 있는 귓가로 바뀌었다",
    ]),
    para(
        "머리카락 사이로 살짝 보이기만 해도 귓가의 작은 변화로 인상이 달라지는 것이 피어싱의 매력입니다.",
        "궁금해진 분들은 DIESEL 지퍼 피어싱을 한번 직접 살펴보는 건 어떨까요!",
    ),
    related_box("KEITO(오노 케이토) 관련 글", [
        (L_PIERCE_KR, "KO1KEYZ 12명의 피어싱 개수를 정리한 글"),
    ]),
])
KR_SUMMARY = (
    "KO1KEYZ KEITO가 9월 19일 프라챗에서 착용한 지퍼 피어싱은 DIESEL '피어싱(양쪽 귀용)'과 모양이 일치. "
    "지퍼 손잡이와 로고 버튼의 2개 세트로 참고 가격은 16,500엔(세금 포함). 특징과 구분 포인트, 구매처를 정리했습니다."
)

# ============================== EN ==============================
EN_TITLE = "KEITO's Zipper Earring? It's DIESEL, Seen in Pracha!"
EN_CONTENT = "\n\n".join([
    para(
        "In a photo from the fan-club-only \"KO1KEYZ Chat\" (Pracha) that arrived on September 19, KO1KEYZ's KEITO (Ono Keito) "
        "was wearing an earring shaped like a <strong>zipper pull</strong>, and fans immediately started asking which brand it is.",
        f"After checking, the shape matches DIESEL's \"Earrings (for both ears)\" set, with a reference price of {mk_big('JPY 16,500 (tax included)')}.",
        "Here is a look at the design, what points to the DIESEL match, how it differs from KEITO's earlier earrings, and where to buy it.",
    ),
    spec_box("KEITO's Zipper Earring: Basics", [
        ("Brand", "DIESEL (Italy)"),
        ("Item", "Earrings (for both ears): a two-piece set with a different design for each ear"),
        ("Design", "A zipper-pull piece and a round button piece with the logo"),
        ("Reference price", "JPY 16,500 (tax included)"),
        ("Where it was seen", "A photo in Pracha (KO1KEYZ Chat), September 19, 2026"),
    ]),
    h2("Where Was KEITO's Zipper Earring Seen?"),
    para(
        "The earring appears in a photo from Pracha that arrived on September 19.",
        "A silver zipper pull hangs from his earlobe between strands of hair, and it is prominent enough that you notice \"that's a zipper\" at a glance.",
        "Fans quickly began asking \"Where is that from?\" and praising how cute it looks.",
    ),
    para(
        "Pracha is available to fan club members only, so the photo is not reproduced here.",
        "It is a place for everyday moments rather than a costume shoot, but KEITO has not mentioned how he got the earring, "
        "so whether it is his own or was prepared by a stylist is unknown.",
    ),
    h2("What Does DIESEL's Zipper Earring Look Like?"),
    para(
        "The \"Earrings (for both ears)\" listed on DIESEL's official online store are a <strong>two-piece set with a different design on each side</strong>.",
        "One piece is modeled on a zipper pull; the other is a round button with the DIESEL logo.",
    ),
    para(
        "The zipper piece has a square slider on top, a trapezoid body that narrows toward the bottom, an open hole at the lower end, "
        "and the \"DIESEL\" logo embossed vertically on its face.",
        "The button piece has \"FOR SUCCESSFUL LIVING\" running around its rim with the brand logo in the center.",
        "Both are stud (post) types, and the zipper piece hangs its pull directly below the fastening.",
    ),
    note_box(
        "What Is DIESEL?",
        "A fashion brand born in Italy in 1978 with denim at its roots.<br>"
        "It is known for turning garment parts such as zippers, rivets and buttons into accessories and bags, and this earring set follows that idea.<br>"
        "\"FOR SUCCESSFUL LIVING\" is widely known as the brand's slogan.",
    ),
    h2("What Points to DIESEL?"),
    para(
        "Zipper-shaped earrings also come from accessory labels and handmade shops, and the logo lettering cannot be read in the photo.",
        "Still, comparing the details shows several overlaps with DIESEL's product images.",
    ),
    titlebar_list("Three details compared", [
        "<strong>Pull shape</strong>: a square slider on top, a trapezoid narrowing downward, and a trapezoid hole at the bottom",
        "<strong>How it hangs</strong>: the pull drops straight from the round base that fastens to the ear",
        "<strong>Finish and size</strong>: glossy silver, compact enough to sit on the earlobe",
    ]),
    para(
        "All three match, and it is a shape sold for JPY 16,500 in DIESEL's official store, so it is reasonable to treat KEITO's earring as DIESEL's zipper piece.",
        "That said, neither the brand nor the product name has been announced by KEITO himself.",
    ),
    h2("Has KEITO's Earring Style Changed?"),
    para(
        "In footage and photos from around June, KEITO wore a small, simple earring that sparkled and was only glimpsed between strands of hair.",
        "At the September fan meeting, too, the earring could be seen glinting in the shade of his hair.",
        "The zipper, with its pull hanging down, changes the impression of his ear considerably.",
    ),
    para(
        f'In our <a href="{L_PIERCE_EN}">roundup of how many piercings each KO1KEYZ member has</a>, KEITO has two in total across both ears.',
        "The DIESEL set has exactly two pieces, so he may wear one in each ear, but the other ear cannot be seen in this photo.",
        "Wearing only the zipper piece in one ear as a single accent would also work.",
    ),
    h2("How Much Is It, and Where Can You Buy It?"),
    para(
        f"The reference price on DIESEL's official online store is {mk_big('JPY 16,500 (tax included)')} for the pair.",
        "DIESEL's single-ear earrings are often in the low JPY 10,000 range, so this is a standard price for a two-piece set.",
    ),
    titlebar_list("Where to buy DIESEL earrings", [
        f'<a href="{DIESEL}" target="_blank" rel="noopener">DIESEL official online store (Japan)</a>: look for "Earrings (for both ears)" under jewelry',
        "DIESEL stores and retailers (check the store locator on the official site)",
        f'<a href="{ZOZO}" target="_blank" rel="noopener">ZOZOTOWN</a>: DIESEL brand page (jewelry and accessories)',
    ]),
    para(
        "Availability and stock change over time.",
        "DIESEL also sells similarly named designs such as logo studs, so check the product photo to confirm it is the zipper-and-button combination.",
    ),
    h2("Summary"),
    summary_box([
        "In a September 19 Pracha photo, KEITO wore a silver earring shaped like a zipper pull",
        "The shape matches DIESEL's \"Earrings (for both ears)\", a set of a zipper piece and a logo button piece",
        "Reference price is JPY 16,500 (tax included), available from the official store and retailers",
        "It is a bolder look than the small sparkling earring he wore around June",
    ]),
    para(
        "Even a glimpse between strands of hair shows how a small change at the ear can shift a whole impression.",
        "If it caught your eye, why not take a look at DIESEL's zipper earrings yourself!",
    ),
    related_box("More about KEITO (Ono Keito)", [
        (L_PIERCE_EN, "How many piercings does each KO1KEYZ member have?"),
    ]),
])
EN_SUMMARY = (
    "The zipper-shaped earring KO1KEYZ's KEITO wore in a September 19 Pracha photo matches DIESEL's \"Earrings (for both ears)\". "
    "A set of a zipper pull and a logo button, priced at JPY 16,500 (tax included). Design details, how we matched it, and where to buy."
)


# ============================== POST ==============================
def upload_png(path):
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HA, "Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{path.name}"'},
        data=path.read_bytes(),
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
    import re
    for name, c in (("JP", JP_CONTENT), ("KR", KR_CONTENT), ("EN", EN_CONTENT)):
        assert "<hr" not in c
        text = re.sub(r"<[^>]+>", "", c)
        print(name, "chars:", len(text))
    if "--dry" in sys.argv:
        sys.exit(0)
    jp_eye = upload_png(EYE_JP)
    kr_eye = upload_png(EYE_KR)
    jp = post_draft(JP_TITLE, JP_CONTENT, BASE_SLUG, "ja", [66, 63, 94], jp_eye, JP_SUMMARY)
    JP_ID = jp["id"]
    print("JP", JP_ID, jp["slug"], jp["link"], "media", jp_eye)
    kr = post_draft(KR_TITLE, KR_CONTENT, BASE_SLUG + "-kr", "ko", [74, 78], kr_eye, KR_SUMMARY, JP_ID)
    print("KR", kr["id"], kr["slug"], kr["link"], "media", kr_eye)
    en = post_draft(EN_TITLE, EN_CONTENT, BASE_SLUG + "-en", "en", [110, 118], jp_eye, EN_SUMMARY, JP_ID)
    print("EN", en["id"], en["slug"], en["link"], "media", jp_eye)
