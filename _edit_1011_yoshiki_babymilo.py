# -*- coding: utf-8 -*-
"""10/11: WoW!Korea 4K YouTube (2PgJo2sMsZ4, 55.9-56.1s) shows a pink BAPE BABY MILO plush in YOSHIKI's Gimpo bundle.
Matched to jp.bape.com AM20-182-355 BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2 PINK (4,950 yen, 15cm, polyester 100%).
Adds a new H2 section before the Mellojoy H2 and updates the info table / lead / summary in JP/KR/EN (14339/14342/14343)."""
import json, time
from pathlib import Path
import requests
from _mubank1009_helpers import WP_URL as U, HEADERS_AUTH as H, wp_upload, img_html

SRC = "https://www.youtube.com/watch?v=2PgJo2sMsZ4"
PRODUCT = "https://jp.bape.com/products/am20-182-355"
BAPE_TOP = "https://jp.bape.com/"
AC, BD, BG = "#d66b93", "#f4d4e0", "#fdf3f7"

m_full = wp_upload(Path("images/yoshiki_gimpo_babymilo_full.jpg"), "image/jpeg")
m_zoom = wp_upload(Path("images/yoshiki_gimpo_babymilo_closeup.jpg"), "image/jpeg")
print("MEDIA", m_full["id"], m_zoom["id"])


def p(t):
    return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def mini(rows):
    inner = "".join(f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}</strong>{v}</p>\n' for i, (k, v) in enumerate(rows))
    return (f'<!-- wp:html -->\n<div style="border:1px solid {BD};border-left:4px solid {AC};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">\n'
            f'{inner}</div>\n<!-- /wp:html -->')


def infobox(title, body):
    return (f'<!-- wp:html -->\n<div style="border:1px solid {BD};border-left:4px solid {AC};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">\n'
            f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n<p style="margin:0;">{body}</p>\n</div>\n<!-- /wp:html -->')


def spec(title, rows):
    tr = "".join(f'<tr><td style="background:#f9e3ec;border:1px solid {BD};padding:8px 12px;width:32%;">{k}</td><td style="border:1px solid {BD};padding:8px 12px;">{v}</td></tr>\n' for k, v in rows)
    return (f'<!-- wp:html -->\n<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
            f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>\n<table style="border-collapse:collapse;width:100%;">\n{tr}</table>\n</div>\n<!-- /wp:html -->')


def shop(title, items):
    li = "".join(f'<li style="margin:{"0" if i == len(items) - 1 else "0 0 8px 0"};">{x}</li>\n' for i, x in enumerate(items))
    return (f'<!-- wp:html -->\n<div style="border:1px solid {BD};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
            f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AC};color:#fff;">{title}</p>\n'
            f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">\n{li}</ul>\n</div>\n<!-- /wp:html -->')


def mk(t):
    return f'<strong><span class="swl-marker mark_pink" style="font-size:1.15em;">{t}</span></strong>'


CHECK = f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AC};border-radius:3px;color:{AC};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>'
LINK = lambda text: f'<a href="{PRODUCT}" target="_blank" rel="noopener">{text}</a>'

JP = "\n\n".join([
    h2("ピンクのサルはBAPEの「ベイビーマイロ」"),
    mini([("ブランド：", "A BATHING APE(BAPE)のBABY MILO STORE"),
          ("アイテム：", "BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2(ピンク)とみられる")]),
    p("写真ではタグまで読めなかったぬいぐるみの束ですが、韓国の芸能メディアWoW!Koreaが公式YouTubeに公開した4Kの到着映像で見直すと、1つだけはっきり正体が分かるものがありました。<br>\n"
      "映像の56秒ごろ、YOSHIKIが歩きながら振り返った瞬間に、リュックの横で束が正面を向きます。<br>\n"
      "その中ほどにいたのが、全身ピンクのサルのぬいぐるみでした。"),
    img_html(m_full, "金浦空港でリュックにピンクのぬいぐるみキーホルダーの束をつけて歩くYOSHIKI", f"出典：{SRC}"),
    p("近くで見ると、大きな丸い顔に小さな点の目、への字の口元という、ひと目でBAPE(ア ベイシング エイプ)のキャラクター<strong>「BABY MILO(ベイビーマイロ)」</strong>と分かる顔立ちです。<br>\n"
      "ふだんは茶色い体に黄色っぽい顔で知られるマイロですが、YOSHIKIのものは体がピンク、顔が薄いピンクという珍しい配色でした。<br>\n"
      "体の右わきには、白い小さなタグも見えています。"),
    img_html(m_zoom, "YOSHIKIのキーホルダーの束に入っていたピンクのベイビーマイロのぬいぐるみ", f"出典：{SRC}"),
    p(f"BAPE公式通販のぬいぐるみキーホルダーを1つずつ見くらべたところ、いちばん近かったのが{LINK('「BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2」のピンク')}です。<br>\n"
      f"{mk('体はピンク・顔だけ薄いピンク・目と鼻もピンク・手足の先が白っぽい・体の横にタグ')}という特徴が、映像のマイロとそろっていました。<br>\n"
      "BAPEのマイロのキーホルダーは茶色のモデルがほとんどで、全身ピンクで顔まで薄いピンクのものは、2026年10月11日時点の公式通販ではこのモデルくらいしか見当たりません。<br>\n"
      "ただ、本人や運営からの発表はないので、あくまで見た目からの推測です。"),
    infobox("BABY MILO(ベイビーマイロ)とは？",
            "1993年に東京・原宿で生まれたストリートブランド「A BATHING APE(BAPE)」の、サルのマスコットキャラクターです。<br>\n"
            "子ども服や雑貨を扱う「BABY MILO STORE」の看板キャラで、Tシャツやバッグ、ぬいぐるみなど、たくさんのアイテムに登場しています。<br>\n"
            "最近はぬいぐるみをバッグにつける「ぬい活」の流れもあって、マイロのぬいぐるみキーホルダーも、公式通販で売り切れになっているモデルが少なくありません。"),
    p("ちなみにこの日は、DAIKIもBAPEのシャークパーカーを着て空港に現れていました。<br>\n"
      "メンバー2人が別々のアイテムでBAPEを取り入れていたことになり、ファンにとってはうれしい偶然と言えるかもしれません。"),
    spec("BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2", [
        ("ブランド", "A BATHING APE(BABY MILO STORE)"),
        ("カラー", "ピンク"),
        ("価格", "4,950円(税込)"),
        ("サイズ", "たて15cm"),
        ("素材", "ポリエステル100%"),
        ("品番", "AM20-182-355"),
        ("公式通販に登場", "2026年7月24日"),
    ]),
    p(f"価格は{mk('4,950円(税込)')}で、たて15cmと、バッグにつけても大きすぎないサイズです。<br>\n"
      "2026年10月11日の時点では、BAPEの公式通販で在庫ありになっていました。<br>\n"
      "マイロのぬいぐるみは人気が高く、品切れになるとフリマアプリで定価より高く出回ることもあるので、気になる人は早めにチェックしておくと安心です。"),
    shop("ベイビーマイロのキーホルダーの購入先", [
        f'{LINK("BAPE公式通販「BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2」")}:4,950円(税込)、ピンク',
        f'<a href="{BAPE_TOP}" target="_blank" rel="noopener">BAPE公式通販(bape.com)</a>:茶色など、ほかのマイロのぬいぐるみキーホルダーも',
        "BAPE STORE・BABY MILO STOREの店舗:取り扱いや在庫は店舗ごとに確認を",
    ]),
])

KR = "\n\n".join([
    h2("핑크 원숭이는 BAPE의 '베이비 마일로'"),
    mini([("브랜드: ", "A BATHING APE(BAPE)의 BABY MILO STORE"),
          ("아이템: ", "BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2(핑크)로 보임")]),
    p("사진으로는 태그까지 읽을 수 없었던 인형 묶음이지만, 한국 연예 매체 WoW!Korea가 공식 유튜브에 공개한 4K 입국 영상으로 다시 보니 정체가 확실히 보이는 것이 하나 있었습니다.<br>\n"
      "영상 56초쯤, YOSHIKI가 걸으면서 돌아보는 순간 백팩 옆의 묶음이 정면을 향합니다.<br>\n"
      "그 한가운데에 있던 것이 온몸이 핑크인 원숭이 인형이었습니다."),
    img_html(m_full, "김포공항에서 백팩에 핑크 인형 키링 묶음을 달고 걷는 YOSHIKI", f"출처: {SRC}"),
    p("가까이 보면 크고 둥근 얼굴에 작은 점 같은 눈, 시무룩한 입매로, 한눈에 BAPE(어 베이싱 에이프)의 캐릭터 <strong>'BABY MILO(베이비 마일로)'</strong>임을 알 수 있습니다.<br>\n"
      "보통은 갈색 몸에 노르스름한 얼굴로 알려진 마일로지만, YOSHIKI의 것은 몸이 핑크, 얼굴이 연핑크인 보기 드문 배색이었습니다.<br>\n"
      "몸 오른쪽 옆에는 작은 흰색 태그도 보입니다."),
    img_html(m_zoom, "YOSHIKI의 키링 묶음에 있던 핑크 베이비 마일로 인형", f"출처: {SRC}"),
    p(f"BAPE 일본 공식몰의 인형 키링을 하나씩 비교해 보니, 가장 가까운 것은 {LINK('\'BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2\' 핑크')}였습니다.<br>\n"
      f"{mk('몸은 핑크・얼굴만 연핑크・눈과 코도 핑크・손발 끝이 하얀 편・몸 옆에 태그')}라는 특징이 영상 속 마일로와 일치했습니다.<br>\n"
      "BAPE의 마일로 키링은 대부분 갈색 모델이고, 온몸이 핑크에 얼굴까지 연핑크인 것은 2026년 10월 11일 기준 공식몰에서 이 모델 정도밖에 보이지 않습니다.<br>\n"
      "다만 본인이나 운영 측의 발표는 없기 때문에, 어디까지나 겉모습을 바탕으로 한 추측입니다."),
    infobox("BABY MILO(베이비 마일로)란?",
            "1993년 도쿄 하라주쿠에서 탄생한 스트리트 브랜드 'A BATHING APE(BAPE)'의 원숭이 마스코트 캐릭터입니다.<br>\n"
            "아동복과 잡화를 다루는 'BABY MILO STORE'의 간판 캐릭터로, 티셔츠와 가방, 인형 등 많은 아이템에 등장합니다.<br>\n"
            "최근에는 가방에 인형을 다는 유행도 있어, 마일로 인형 키링도 공식몰에서 품절된 모델이 적지 않습니다."),
    p("참고로 이날은 DAIKI도 BAPE의 샤크 후디를 입고 공항에 나타났습니다.<br>\n"
      "두 멤버가 각자 다른 아이템으로 BAPE를 착용한 셈이라, 팬들에게는 반가운 우연이라고 할 수 있겠습니다."),
    spec("BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2", [
        ("브랜드", "A BATHING APE(BABY MILO STORE)"),
        ("컬러", "핑크"),
        ("가격", "4,950엔(세금 포함, 일본 공식몰)"),
        ("사이즈", "세로 15cm"),
        ("소재", "폴리에스터 100%"),
        ("품번", "AM20-182-355"),
        ("공식몰 등록", "2026년 7월 24일"),
    ]),
    p(f"가격은 {mk('4,950엔(세금 포함)')}이고, 세로 15cm로 가방에 달아도 너무 크지 않은 사이즈입니다.<br>\n"
      "2026년 10월 11일 기준 BAPE 일본 공식몰에서는 재고가 있는 상태였습니다.<br>\n"
      "마일로 인형은 인기가 많아 품절되면 중고 거래 앱에서 정가보다 비싸게 거래되기도 하니, 관심 있는 분은 일찍 확인해 두는 것이 좋습니다."),
    shop("베이비 마일로 키링 구매처", [
        f'{LINK("BAPE 일본 공식몰 \'BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2\'")}: 4,950엔(세금 포함), 핑크',
        f'<a href="{BAPE_TOP}" target="_blank" rel="noopener">BAPE 일본 공식몰(bape.com)</a>: 갈색 등 다른 마일로 인형 키링도',
        "BAPE STORE・BABY MILO STORE 매장: 취급 여부와 재고는 매장마다 확인 필요",
    ]),
])

EN = "\n\n".join([
    h2("The pink monkey is BAPE's \"Baby Milo\""),
    mini([("Brand: ", "A BATHING APE (BAPE), BABY MILO STORE"),
          ("Item: ", "Likely the BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2 (pink)")]),
    p("The tags on the bundle couldn't be read in photos, but rewatching the 4K arrival footage that Korean entertainment outlet WoW!Korea posted on its official YouTube channel, one of the plushies turns out to be clearly identifiable.<br>\n"
      "Around the 56-second mark, YOSHIKI glances back while walking and the bundle at the side of his backpack swings to face the camera.<br>\n"
      "Right in the middle is an all-pink monkey plush."),
    img_html(m_full, "YOSHIKI walking through Gimpo Airport with a bundle of pink plush charms on his backpack", f"Source: {SRC}"),
    p("Up close, the big round face, tiny dot eyes and downturned mouth make it instantly recognizable as BAPE's character <strong>BABY MILO</strong>.<br>\n"
      "Milo is usually known for a brown body and a yellowish face, but YOSHIKI's has an unusual color scheme: a pink body with a pale pink face.<br>\n"
      "A small white tag is also visible on its right side."),
    img_html(m_zoom, "The pink Baby Milo plush in YOSHIKI's charm bundle", f"Source: {SRC}"),
    p(f"Comparing the plush keychains on BAPE's official Japanese online store one by one, the closest match is {LINK('the pink BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2')}.<br>\n"
      f"{mk('Pink body, pale pink face, pink eyes and nose, whitish hands and feet, and a tag on the side')} all line up with the Milo in the footage.<br>\n"
      "Most of BAPE's Milo keychains are brown, and as of October 11, 2026, this is about the only all-pink model with a pale pink face on the official store.<br>\n"
      "That said, neither YOSHIKI nor his agency has confirmed it, so this is an educated guess based on appearance."),
    infobox("What is BABY MILO?",
            "Baby Milo is the monkey mascot of A BATHING APE (BAPE), the streetwear brand born in Harajuku, Tokyo, in 1993.<br>\n"
            "He's the face of BABY MILO STORE, BAPE's kids' clothing and goods line, and appears on everything from tees and bags to plush toys.<br>\n"
            "With plush bag charms trending lately, quite a few Milo plush keychains are sold out on the official store."),
    p("Fun fact: DAIKI also showed up at the airport that day in a BAPE shark hoodie.<br>\n"
      "Two members wearing BAPE in completely different ways makes for a nice little coincidence for fans."),
    spec("BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2", [
        ("Brand", "A BATHING APE (BABY MILO STORE)"),
        ("Color", "Pink"),
        ("Price", "4,950 yen incl. tax (about $33 at 150 yen/$)"),
        ("Size", "15 cm tall"),
        ("Material", "100% polyester"),
        ("Item no.", "AM20-182-355"),
        ("Listed on official store", "July 24, 2026"),
    ]),
    p(f"It's priced at {mk('4,950 yen (tax included)')} and stands 15 cm tall, a size that won't overwhelm a bag.<br>\n"
      "As of October 11, 2026, it was in stock on BAPE's official Japanese online store.<br>\n"
      "Milo plushies are popular and can resell above retail once they sell out, so it's worth checking early if you want one."),
    shop("Where to buy the Baby Milo keychain", [
        f'{LINK("BAPE official Japan store: BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2")}: 4,950 yen incl. tax, pink',
        f'<a href="{BAPE_TOP}" target="_blank" rel="noopener">BAPE official Japan store (bape.com)</a>: brown and other Milo plush keychains too',
        "BAPE STORE / BABY MILO STORE shops: check availability with each store",
    ]),
])

# (old, new) replacements per post; each old string must exist exactly once
REPL = {
    14339: [
        ("この記事では、キーホルダーの中身とメロジョイがどんなブランドか、",
         "束の中にはBAPEの<strong>「BABY MILO(ベイビーマイロ)」のピンクのぬいぐるみ</strong>も入っていました。<br>\nこの記事では、キーホルダーの中身とベイビーマイロ・メロジョイがどんなブランドか、"),
        ("Mellojoy(メロジョイ)のドーナツ型スクイーズ</td></tr>",
         "Mellojoy(メロジョイ)のドーナツ型スクイーズ/BAPEのBABY MILO(ベイビーマイロ)のぬいぐるみ</td></tr>"),
        ("/ミニランドは2個入り3,598円</td></tr>",
         "/ミニランドは2個入り3,598円/ベイビーマイロは4,950円</td></tr>"),
        ("<li>ドーナツのスクイーズのブランド</li>",
         "<li>ピンクのサルのぬいぐるみのブランド</li>\n<li>ドーナツのスクイーズのブランド</li>"),
        ("ぬいぐるみのほうは、アップの写真でもキャラクター名やブランドが分かるタグまでは読み取れず、どこのキャラクターなのかまでは分かりませんでした。<br>\n一方、ドーナツには小さなブランドロゴが入っていて、こちらはブランドまでたどることができました。",
         "ぬいぐるみの多くは、アップの写真でもキャラクター名やブランドが分かるタグまでは読み取れませんでした。<br>\nそれでも、ピンクのサルのぬいぐるみは顔立ちから、ドーナツは小さなブランドロゴから、それぞれブランドまでたどることができました。"),
        ("そのなかのピンクのドーナツは、Mellojoy(メロジョイ)のスクイーズとみられる<br>",
         f"ピンクのサルのぬいぐるみは、BAPEの「BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2」(4,950円)とみられる<br>\n{CHECK}ピンクのドーナツは、Mellojoy(メロジョイ)のスクイーズとみられる<br>"),
        ("ほかのぬいぐるみは、キャラクターまでは分からなかった", "残りのぬいぐるみは、キャラクターまでは分からなかった"),
    ],
    14342: [
        ("이 글에서는 키링 구성과 멜로조이가",
         "묶음 안에는 BAPE의 <strong>'BABY MILO(베이비 마일로)' 핑크 인형</strong>도 들어 있었습니다.<br>\n이 글에서는 키링 구성과 베이비 마일로・멜로조이가"),
        ("Mellojoy(멜로조이) 도넛 스퀴시</td></tr>",
         "Mellojoy(멜로조이) 도넛 스퀴시/BAPE의 BABY MILO(베이비 마일로) 인형</td></tr>"),
        ("/미니랜드는 2개입 3,598엔</td></tr>", "/미니랜드는 2개입 3,598엔/베이비 마일로는 4,950엔</td></tr>"),
        ("인형들은 클로즈업 사진에서도 캐릭터 이름이나 브랜드를 알 수 있는 태그까지는 읽을 수 없어, 어떤 캐릭터인지까지는 알 수 없었습니다.<br>\n반면 도넛에는 작은 브랜드 로고가 있어 브랜드까지 확인할 수 있었습니다.",
         "인형 대부분은 클로즈업 사진에서도 캐릭터 이름이나 브랜드를 알 수 있는 태그까지는 읽을 수 없었습니다.<br>\n그래도 핑크 원숭이 인형은 얼굴 생김새로, 도넛은 작은 브랜드 로고로 각각 브랜드까지 확인할 수 있었습니다."),
        ("그중 핑크 도넛은 Mellojoy(멜로조이) 스퀴시로 보인다<br>",
         f"핑크 원숭이 인형은 BAPE의 'BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2'(4,950엔)로 보인다<br>\n{CHECK}핑크 도넛은 Mellojoy(멜로조이) 스퀴시로 보인다<br>"),
        ("다른 인형들은 캐릭터까지는 확인하지 못했다", "나머지 인형들은 캐릭터까지는 확인하지 못했다"),
    ],
    14343: [
        ("This article covers what was on his bag, what Mellojoy is,",
         "The bundle also included a <strong>pink BABY MILO plush from BAPE</strong>.<br>\nThis article covers what was on his bag, what Baby Milo and Mellojoy are,"),
        ("Mellojoy donut squishy</td></tr>", "Mellojoy donut squishy / BAPE BABY MILO plush</td></tr>"),
        ("/ Mini Land: 3,598 yen for 2</td></tr>", "/ Mini Land: 3,598 yen for 2 / Baby Milo: 4,950 yen</td></tr>"),
        ("Even in the close-up photo, no tag showing a character name or brand could be read, so we couldn't tell which characters they are.<br>\nThe donut, though, carries a small brand logo, which let us trace the brand.",
         "Even in the close-up photo, most of the plushies had no readable tag showing a character name or brand.<br>\nStill, the pink monkey could be traced by its face, and the donut by its small brand logo."),
        ("The pink donut among them appears to be a Mellojoy squishy<br>",
         f"The pink monkey plush appears to be BAPE's BABY MILO FAUX FUR PLUSH DOLL KEYCHAIN #2 (4,950 yen)<br>\n{CHECK}The pink donut appears to be a Mellojoy squishy<br>"),
        ("The other plushies couldn't be identified", "The remaining plushies couldn't be identified"),
    ],
}
NEW = {14339: JP, 14342: KR, 14343: EN}
H2_MARK = '<!-- wp:heading -->\n<h2 class="wp-block-heading">'

for pid in (14339, 14342, 14343):
    raw = requests.get(f"{U}/wp-json/wp/v2/posts/{pid}", headers=H, params={"context": "edit"}).json()["content"]["raw"]
    Path(f"backups/{pid}_before_1011_babymilo.html").write_text(raw, encoding="utf-8")
    assert "BABY MILO" not in raw, f"{pid} already edited"
    for old, new in REPL[pid]:
        assert raw.count(old) == 1, (pid, old[:40], raw.count(old))
        raw = raw.replace(old, new)
    i = raw.index(H2_MARK, raw.index(H2_MARK) + 1)  # second H2 = Mellojoy section
    raw = raw[:i] + NEW[pid] + "\n\n" + raw[i:]
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{pid}", headers={**H, "Content-Type": "application/json"},
                      data=json.dumps({"content": raw, "status": "draft"}).encode("utf-8"))
    r.raise_for_status()
    print(pid, r.json()["status"])
    time.sleep(2)

for pid in (14339, 14342, 14343):
    raw = requests.get(f"{U}/wp-json/wp/v2/posts/{pid}", headers=H, params={"context": "edit"}).json()["content"]["raw"]
    print(pid, "verify", raw.count("BABY MILO"), "AM20-182-355" in raw, str(m_zoom["id"]) in raw or "babymilo_closeup" in raw)
