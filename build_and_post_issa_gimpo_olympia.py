# -*- coding: utf-8 -*-
"""ISSA(柳谷伊冴)が2026-10-07夜に金浦空港へ到着したときの「OLYMPIA」トラッカーキャップ。
元ネタ: WoW!Korea公式YouTube 4K https://www.youtube.com/watch?v=2PgJo2sMsZ4 (105〜108秒)
裏取り: Trucker Hat USA「Olympia Beer Hat」(SKU LBTOlympia, 18.99USD, Brown/White Front等)の商品写真とロゴ・配色が一致。
日本ではRAWDRIP「Trucker Hat USA Olympia Brewing Company - Brown」6,600円(税込)。
ジャケット(こげ茶のジップ、袖に赤いステッチ)は未特定。
使い方: python build_and_post_issa_gimpo_olympia.py --dry で文字数確認のみ
"""
import re, sys
from pathlib import Path

from _mubank1009_helpers import ROOT, WP_URL, UI, wp_upload, img_html, post_draft, make_eyecatch, h2, p

DRY = "--dry" in sys.argv
ui = UI(AB="#c8e6f0", AL="#2f8fb3", BG="#eef8fb", TH="#dff0f6", marker="mark_blue")

SRC = "https://www.youtube.com/watch?v=2PgJo2sMsZ4"
THU = "https://truckerhatusa.com/olympia-beer-hat-trucker-hats-mesh-hat-snap-back-hat/"
RAWDRIP = "https://www.rawdrip.jp/product/2820"
DAIKI_JP = "https://chomoand-1.com/daiki-gimpo-airport-bape-paisley-shark-hoodie-14296"
DAIKI_KR = "https://chomoand-1.com/ko/daiki-gimpo-airport-bape-paisley-shark-hoodie-kr-14298"
DAIKI_EN = "https://chomoand-1.com/en/daiki-gimpo-airport-bape-paisley-shark-hoodie-en-14299"

JP_REL = [
    ("https://chomoand-1.com/issa-radio-check-shirt-b-omnivore-14086", "ISSAがラジオで着たチェックシャツはビーオムニボーだった記事"),
    ("https://chomoand-1.com/issa-jesse-saint-logo-tee-14062", "ISSAとジェシーがお揃い？セントマイケルのTシャツの記事"),
    ("https://chomoand-1.com/issa-autograph-parttime-job-13848", "ISSAのサインがバイト先で生まれた話の記事"),
    ("https://chomoand-1.com/issa-shinhaeng-bento-13411", "ISSAの弁当は塚田農場？SHINHAENGとの偶然の記事"),
    ("https://chomoand-1.com/issa_no_wiki-2907", "ISSA(柳谷伊冴)のwiki風プロフィール・経歴の記事"),
]
KR_REL = [
    ("https://chomoand-1.com/ko/issa-radio-check-shirt-b-omnivore-kr-14089", "ISSA가 라디오에서 입은 체크셔츠는 B omnivore였다는 글"),
    ("https://chomoand-1.com/ko/issa-jesse-saint-logo-tee-kr-14065", "ISSA와 제시가 같은 옷? 세인트 마이클 티셔츠 글"),
    ("https://chomoand-1.com/ko/issa-shinhaeng-bento-kr-13415", "ISSA의 도시락은 츠카다 농장? SHINHAENG과의 우연 글"),
]
EN_REL = [
    ("https://chomoand-1.com/en/issa-radio-check-shirt-b-omnivore-en-14092", "ISSA's radio check shirt: B omnivore"),
    ("https://chomoand-1.com/en/issa-jesse-saint-logo-tee-en-14068", "ISSA and SixTONES' Jesse in matching Saint Michael tees?"),
    ("https://chomoand-1.com/en/issa-shinhaeng-bento-en-13416", "ISSA's bento and a coincidence with SHINHAENG"),
]

if DRY:
    m_full = m_cap = {"source_url": "x", "media_details": {"width": 800, "height": 1016, "sizes": {}}}
else:
    m_full = wp_upload(ROOT / "images" / "issa_gimpo_olympia_full.jpg", "image/jpeg")
    m_cap = wp_upload(ROOT / "images" / "issa_gimpo_olympia_cap.jpg", "image/jpeg")
    print("MEDIA", m_full["id"], m_cap["id"])
mk = ui.mark

# ============================== JP ==============================
JP_TITLE = "【ISSA】金浦空港のキャップはまさかのビールロゴ！値段は？"
JP_SLUG = "issa-gimpo-airport-olympia-beer-trucker-hat"

JP = "\n\n".join([
    p("KO1KEYZ(コイキーズ)が韓国の音楽番組に出演するため、2026年10月7日の夜にソウルの金浦(キンポ)国際空港へ到着しました。<br>\n"
      "マスクにこげ茶のジャケットというシックな格好で現れたISSAの頭の上で目を引いたのが、クリーム色と茶色のトラッカーキャップです。<br>\n"
      "正面のロゴは、アメリカのビール<strong>「Olympia(オリンピア)」のロゴをプリントした、Trucker Hat USAの「Olympia Beer Hat」</strong>とみられます。<br>\n"
      "この記事では、キャップのデザインと元になったビールのこと、価格と買える場所をまとめます。"),
    ui.infobox("ISSAの金浦空港キャップの基本情報", [
        ("着用シーン", "2026年10月7日夜、金浦国際空港への到着時"),
        ("キャップ", "Trucker Hat USA「Olympia Beer Hat」(ブラウン×クリーム)とみられる"),
        ("ロゴ", "アメリカのビール「Olympia」(1896年創業)"),
        ("価格", "日本の取扱店で6,600円(税込)/アメリカの公式通販で18.99ドル"),
    ]),
    ui.knowbox("この記事でわかること", ["金浦空港でのISSAの私服", "キャップのブランドとロゴ", "オリンピアビールってどんなビール？", "価格と購入先"]),

    h2("ISSAが金浦空港でかぶっていたキャップは？"),
    ui.minibox([("キャップ：", "クリーム×茶色のトラッカーキャップ(OLYMPIAのロゴ)"),
                ("服装：", "こげ茶のジップジャケット+グレーのスウェットパンツ")]),
    p("韓国の芸能メディアWoW!Koreaが公式YouTubeに公開した4Kの到着映像では、1分45秒ごろからISSAがDAIKIと並んで歩く姿がしっかり映っています。<br>\n"
      "キャップを深めにかぶり、黒いショルダーバッグを斜めがけにして、少しうつむきかげんで歩いていました。<br>\n"
      "前を見るたびにキャップの正面がカメラに向き、白っぽい生地に入った丸いロゴがはっきり見えます。"),
    img_html(m_full, "金浦空港に到着したISSA。クリーム色と茶色のトラッカーキャップにこげ茶のジャケット", f"出典：{SRC}"),
    p(f"アップにすると、ロゴの下には{mk('紺色の大きな文字で「OLYMPIA」', True)}と書かれていました。<br>\n"
      "その上には金色の丸い紋章があり、真ん中に馬のひづめの形(馬蹄)、まわりに小さく「BEER」「SINCE 1896」の文字が入っています。<br>\n"
      "さらに「OLYMPIA」の下には、筆記体で小さく「It's the Water」と添えられていました。"),
    img_html(m_cap, "ISSAがかぶっていたOLYMPIAのロゴ入りトラッカーキャップのアップ", f"出典：{SRC}"),
    p("前はクリーム色のスポンジ素材、つばと後ろのメッシュはこげ茶という、昔ながらのアメリカのトラッカーキャップの形です。<br>\n"
      "こげ茶のジャケットとキャップの茶色がそろっていて、全体を落ち着いたブラウンでまとめたコーデになっていました。"),

    h2("キャップはTrucker Hat USAの「Olympia Beer Hat」"),
    ui.minibox([("ブランド：", "Trucker Hat USA(トラッカーハットUSA)"),
                ("モデル：", "Olympia Beer Hat(ブラウン×クリーム系)とみられる")]),
    p("「BEER」「SINCE 1896」の入った丸い紋章、馬蹄、紺色の「OLYMPIA」、筆記体の「It's the Water」という組み合わせで探してみると、アメリカのキャップ専門店「Trucker Hat USA」が販売している「Olympia Beer Hat」が見つかりました。<br>\n"
      f"商品写真と見くらべると、{mk('ロゴの配置・文字の色・前がクリームでつばと後ろが茶色という配色', True)}まで、ISSAのキャップとそろっています。<br>\n"
      "日本でも、このキャップの茶色を扱っているセレクトショップがありました。<br>\n"
      "ただ、本人がどこで買ったのかは明かされていないので、同じデザインのキャップとして紹介します。"),
    ui.infobox("Olympia Beer Hatのスペック", [
        ("ブランド", "Trucker Hat USA"),
        ("商品名", "Olympia Beer Hat(Trucker Hats, Mesh Hat, Snap Back Hat)"),
        ("カラー", "ブラウン×ホワイト(クリーム)など20色以上"),
        ("素材", "フォーム55%・メッシュ45%"),
        ("形", "5パネルのトラッカーキャップ、カーブしたつば"),
        ("サイズ", "フリーサイズ(後ろのスナップで調節)"),
        ("価格", "18.99ドル(アメリカの公式通販)/6,600円(日本の取扱店・税込)"),
    ]),
    p("Trucker Hat USAは、昔のアメリカの企業ロゴやビールのロゴを、80年代風のメッシュキャップにのせて販売しているお店です。<br>\n"
      "前がスポンジ、後ろがメッシュというトラッカーキャップは、もともとアメリカのトラック運転手や農家に、企業がおまけで配っていたもの。<br>\n"
      "その名残りで、ビールや自動車用品のロゴ入りキャップは、今でもアメカジ好きに人気のアイテムになっています。"),

    h2("オリンピアビール(Olympia)ってどんなビール？"),
    ui.minibox([("発祥：", "アメリカ・ワシントン州(1896年創業)"),
                ("合言葉：", "It's the Water(おいしさの秘密は水)")]),
    ui.leftbox("Olympia(オリンピア)ビールとは？",
               "<p style=\"margin:0;\">1896年に、ドイツからの移民レオポルド・シュミットがアメリカ・ワシントン州のタムウォーターで始めたビールです。<br>\n"
               "最初の社名はキャピタル・ブルーイングで、1902年に「オリンピア」に変わりました。<br>\n"
               "地元のわき水を使ってつくっていたことから、「It's the Water(水がちがう)」というキャッチコピーで親しまれてきました。</p>"),
    p("ロゴの真ん中の馬蹄は幸運のお守りとして知られる形で、その中に描かれているのは、ビール工場のそばにあった滝です。<br>\n"
      "ブランドはのちにアメリカのビール会社パブスト(Pabst)のものになり、2021年1月には生産を一時休止すると発表されました。<br>\n"
      "ビールそのものは手に入りにくくなりましたが、レトロなロゴはTシャツやキャップのデザインとして今も人気で、ISSAのキャップもそのひとつです。"),
    p("ちなみにこの日、ISSAのとなりを歩いていたDAIKIは、BAPEの赤いペイズリー柄のシャークパーカーを着ていました。<br>\n"
      f"DAIKIの私服は<a href=\"{DAIKI_JP}\" target=\"_blank\" rel=\"noopener\">金浦空港のDAIKIの私服を調べた記事</a>で紹介しています。"),

    h2("値段は？どこで買える？"),
    ui.minibox([("価格：", "6,600円(税込、日本の取扱店)/18.99ドル(アメリカ)"),
                ("購入先：", "RAWDRIP(日本)・Trucker Hat USA公式通販(アメリカ)")]),
    p(f"日本で買うなら、セレクトショップRAWDRIPの通販で「Trucker Hat USA Olympia Brewing Company - Brown」が{mk('6,600円(税込)', True)}で売られています。<br>\n"
      "2026年10月11日の時点では、数量を選んでカートに入れられる状態でした。<br>\n"
      "アメリカのTrucker Hat USA公式通販では18.99ドル(1ドル150円換算で約2,850円)と手ごろですが、日本への発送ができるかや送料は、注文の前に確認しておきましょう。"),
    ui.barbox("OLYMPIAのトラッカーキャップの購入先", [
        f'<a href="{RAWDRIP}" target="_blank" rel="noopener">RAWDRIP「Trucker Hat USA Olympia Brewing Company - Brown」</a>:6,600円(税込)',
        f'<a href="{THU}" target="_blank" rel="noopener">Trucker Hat USA公式通販「Olympia Beer Hat」</a>:18.99ドル、カラーは「Brown / White Front」など',
        "古着屋・フリマアプリ:昔のオリンピアビールのノベルティキャップも出回っている",
    ]),
    p("ネットで探すと、オリンピアのロゴ入りキャップはほかにもいろいろなデザインが見つかります。<br>\n"
      "ISSAと同じものを選びたいときは、丸い紋章の下に「OLYMPIA」の文字があり、前がクリーム色でつばが茶色のものを目印にすると選びやすいはずです。"),

    h2("ジャケットやパンツはどこの？"),
    ui.minibox([("ジャケット：", "こげ茶のジップジャケット(ブランドは未特定)"),
                ("パンツ：", "グレーのワイドなスウェットパンツ")]),
    p("ジャケットは首元が高めのこげ茶のジップアップで、両方の袖に赤い短いステッチがぽつぽつと入った、少し変わったデザインでした。<br>\n"
      "前のファスナーは上まで閉めず、中に黒いTシャツを合わせています。<br>\n"
      "ロゴやタグは映像からは見えず、ブランドまでは分かりませんでした。"),
    p("下はグレーのゆったりしたスウェットパンツで、黒いショルダーバッグを肩からななめにかけていました。<br>\n"
      "キャップとジャケットを茶色でそろえ、パンツをグレーで軽く見せた、まねしやすい空港コーデです。"),

    h2("まとめ"),
    ui.summarybox([
        "ISSAが2026年10月7日に金浦空港へ到着したときのキャップは、ビールの「OLYMPIA」のロゴ入りトラッカーキャップ",
        "ロゴ・配色が一致したのは、Trucker Hat USAの「Olympia Beer Hat」(ブラウン×クリーム系)",
        "日本ではRAWDRIPで6,600円(税込)、アメリカの公式通販では18.99ドル",
        "Olympiaは1896年にワシントン州で生まれたビールで、合言葉は「It's the Water」",
        "こげ茶のジャケットはブランドまでは分からなかった",
    ]),
    p("ビールのロゴを選ぶあたりに、ISSAのアメカジ好きな一面がのぞいていました。<br>\n"
      "1万円以下で手に入るキャップなので、ISSAとおそろいの空港コーデを楽しんでみてはいかがでしょうか！"),
    ui.linkbox("ISSA(柳谷伊冴)の関連記事", JP_REL),
])

# ============================== KR ==============================
KR_TITLE = "【ISSA】김포공항 모자는 설마 맥주 로고? 가격은?"
KR = "\n\n".join([
    p("KO1KEYZ가 한국 음악 방송 출연을 위해 2026년 10월 7일 밤 서울 김포국제공항에 도착했습니다.<br>\n"
      "마스크에 짙은 갈색 재킷으로 차분하게 등장한 ISSA의 머리 위에서 눈길을 끈 것은 크림색과 갈색의 트러커 캡이었습니다.<br>\n"
      "정면 로고는 미국 맥주 <strong>'Olympia(올림피아)' 로고를 프린트한 Trucker Hat USA의 'Olympia Beer Hat'</strong>으로 보입니다.<br>\n"
      "이 글에서는 모자 디자인과 원조 맥주 이야기, 가격과 구매처를 정리합니다."),
    ui.infobox("ISSA 김포공항 모자 기본 정보", [
        ("착용 장면", "2026년 10월 7일 밤, 김포국제공항 도착 시"),
        ("모자", "Trucker Hat USA 'Olympia Beer Hat'(브라운×크림)으로 보임"),
        ("로고", "미국 맥주 'Olympia'(1896년 창업)"),
        ("가격", "일본 판매점 6,600엔(세금 포함)/미국 공식몰 18.99달러"),
    ]),
    h2("ISSA가 김포공항에서 쓴 모자는?"),
    ui.minibox([("모자: ", "크림×갈색 트러커 캡(OLYMPIA 로고)"), ("복장: ", "짙은 갈색 집업 재킷+회색 스웨트 팬츠")]),
    p("한국 연예 매체 WoW!Korea가 공식 유튜브에 공개한 4K 입국 영상에서는 1분 45초쯤부터 ISSA가 DAIKI와 나란히 걷는 모습이 또렷하게 담겨 있습니다.<br>\n"
      "모자를 깊게 눌러쓰고 검은 숄더백을 크로스로 멘 채 살짝 고개를 숙이고 걸었습니다.<br>\n"
      "앞을 볼 때마다 모자 정면이 카메라를 향해, 밝은 원단에 들어간 둥근 로고가 잘 보입니다."),
    img_html(m_full, "김포공항에 도착한 ISSA. 크림색과 갈색 트러커 캡에 짙은 갈색 재킷", f"출처: {SRC}"),
    p(f"확대해 보면 로고 아래에는 {mk('남색의 큰 글자로 \'OLYMPIA\'', True)}라고 적혀 있습니다.<br>\n"
      "그 위에는 금색 원형 문장이 있고, 가운데에 말굽 모양, 주변에 작게 'BEER' 'SINCE 1896' 글자가 들어가 있습니다.<br>\n"
      "'OLYMPIA' 아래에는 필기체로 작게 'It's the Water'라고 쓰여 있었습니다."),
    img_html(m_cap, "ISSA가 쓴 OLYMPIA 로고 트러커 캡 클로즈업", f"출처: {SRC}"),
    h2("모자는 Trucker Hat USA의 'Olympia Beer Hat'"),
    ui.minibox([("브랜드: ", "Trucker Hat USA"), ("모델: ", "Olympia Beer Hat(브라운×크림 계열)으로 보임")]),
    p("'BEER' 'SINCE 1896'이 들어간 원형 문장, 말굽, 남색 'OLYMPIA', 필기체 'It's the Water'라는 조합으로 찾아보니, 미국 모자 전문점 'Trucker Hat USA'가 판매하는 'Olympia Beer Hat'이 나왔습니다.<br>\n"
      f"상품 사진과 비교하면 {mk('로고 배치・글자 색・앞은 크림이고 챙과 뒤는 갈색인 배색', True)}까지 ISSA의 모자와 일치합니다.<br>\n"
      "다만 본인이 어디서 샀는지는 밝혀지지 않았기 때문에, 같은 디자인의 모자로 소개합니다."),
    ui.infobox("Olympia Beer Hat 스펙", [
        ("브랜드", "Trucker Hat USA"),
        ("컬러", "브라운×화이트(크림) 등 20색 이상"),
        ("소재", "폼 55%・메시 45%"),
        ("사이즈", "원사이즈(뒤 스냅으로 조절)"),
        ("가격", "18.99달러(미국 공식몰)/6,600엔(일본 판매점, 세금 포함)"),
    ]),
    h2("올림피아 맥주(Olympia)는 어떤 맥주?"),
    ui.minibox([("발상: ", "미국 워싱턴주(1896년 창업)"), ("슬로건: ", "It's the Water")]),
    ui.leftbox("Olympia(올림피아) 맥주란?",
               "<p style=\"margin:0;\">1896년 독일 출신 이민자 레오폴드 슈미트가 미국 워싱턴주 텀워터에서 시작한 맥주입니다.<br>\n"
               "처음 회사 이름은 캐피털 브루잉이었고, 1902년에 '올림피아'로 바뀌었습니다.<br>\n"
               "지역의 샘물로 만든다는 점에서 'It's the Water(물이 다르다)'라는 문구로 사랑받아 왔습니다.</p>"),
    p("로고 가운데의 말굽은 행운의 상징으로 알려진 모양이고, 그 안에 그려진 것은 양조장 근처에 있던 폭포입니다.<br>\n"
      "브랜드는 이후 미국 맥주 회사 팹스트(Pabst)의 소유가 되었고, 2021년 1월에는 생산을 일시 중단한다고 발표했습니다.<br>\n"
      "맥주 자체는 구하기 어려워졌지만, 레트로한 로고는 티셔츠나 모자 디자인으로 지금도 인기입니다."),
    p("참고로 이날 ISSA 옆을 걷던 DAIKI는 BAPE의 빨간 페이즐리 샤크 후디를 입고 있었습니다.<br>\n"
      f"DAIKI의 사복은 <a href=\"{DAIKI_KR}\" target=\"_blank\" rel=\"noopener\">김포공항 DAIKI 사복 글</a>에서 소개하고 있습니다."),
    h2("가격은? 어디서 살 수 있을까?"),
    ui.minibox([("가격: ", "6,600엔(일본 판매점)/18.99달러(미국)"), ("구매처: ", "RAWDRIP(일본)・Trucker Hat USA 공식몰(미국)")]),
    p(f"미국 Trucker Hat USA 공식몰에서는 {mk('18.99달러', True)}에 판매 중입니다.<br>\n"
      "일본 셀렉트 숍 RAWDRIP 온라인몰에서는 'Trucker Hat USA Olympia Brewing Company - Brown'이 6,600엔(세금 포함)이며, 2026년 10월 11일 기준 장바구니에 담을 수 있는 상태였습니다.<br>\n"
      "해외 배송 가능 여부와 배송비는 주문 전에 꼭 확인하세요."),
    ui.barbox("OLYMPIA 트러커 캡 구매처", [
        f'<a href="{THU}" target="_blank" rel="noopener">Trucker Hat USA 공식몰 \'Olympia Beer Hat\'</a>: 18.99달러',
        f'<a href="{RAWDRIP}" target="_blank" rel="noopener">RAWDRIP(일본) \'Trucker Hat USA Olympia Brewing Company - Brown\'</a>: 6,600엔',
        "빈티지 숍・중고 거래 앱: 옛 올림피아 맥주 노벨티 모자도 거래됨",
    ]),
    h2("재킷과 바지는 어디 제품?"),
    ui.minibox([("재킷: ", "짙은 갈색 집업 재킷(브랜드 미확인)"), ("바지: ", "회색 와이드 스웨트 팬츠")]),
    p("재킷은 목 부분이 높은 짙은 갈색 집업으로, 양쪽 소매에 빨간 짧은 스티치가 군데군데 들어간 독특한 디자인이었습니다.<br>\n"
      "로고나 태그는 영상에서 보이지 않아 브랜드까지는 알 수 없었습니다.<br>\n"
      "하의는 회색의 넉넉한 스웨트 팬츠로, 모자와 재킷을 갈색으로 맞추고 바지는 회색으로 가볍게 연출했습니다."),
    h2("정리"),
    ui.summarybox([
        "ISSA가 2026년 10월 7일 김포공항에 도착했을 때 쓴 모자는 맥주 'OLYMPIA' 로고 트러커 캡",
        "로고와 배색이 일치한 것은 Trucker Hat USA의 'Olympia Beer Hat'(브라운×크림 계열)",
        "미국 공식몰 18.99달러, 일본 RAWDRIP 6,600엔(세금 포함)",
        "Olympia는 1896년 워싱턴주에서 탄생한 맥주로, 슬로건은 'It's the Water'",
        "짙은 갈색 재킷은 브랜드까지는 확인하지 못함",
    ]),
    p("맥주 로고를 고르는 센스에서 ISSA의 아메카지 취향이 엿보였습니다.<br>\n"
      "부담 없는 가격의 모자라서, ISSA와 커플룩 공항 코디를 즐겨 보는 것도 좋겠습니다!"),
    ui.linkbox("ISSA(야나기야 이사) 관련 글", KR_REL),
])

# ============================== EN ==============================
EN_TITLE = "[ISSA] His Gimpo Airport Cap Has a Beer Logo? How Much?"
EN = "\n\n".join([
    p("KO1KEYZ landed at Gimpo International Airport in Seoul on the night of October 7, 2026, ahead of appearances on Korean music shows.<br>\n"
      "ISSA arrived in a low-key look of a mask and a dark brown jacket, and what caught the eye was his cream-and-brown trucker cap.<br>\n"
      "The logo on the front appears to be <strong>Trucker Hat USA's \"Olympia Beer Hat,\" printed with the logo of the American beer Olympia</strong>.<br>\n"
      "This article covers the cap's design, the beer behind the logo, and the price and where to buy it."),
    ui.infobox("ISSA's Gimpo airport cap at a glance", [
        ("Scene", "Arrival at Gimpo International Airport, night of Oct 7, 2026"),
        ("Cap", "Appears to be Trucker Hat USA's Olympia Beer Hat (brown x cream)"),
        ("Logo", "Olympia, an American beer founded in 1896"),
        ("Price", "18.99 USD (official US store) / 6,600 yen incl. tax (Japanese retailer)"),
    ]),
    h2("What cap did ISSA wear at Gimpo Airport?"),
    ui.minibox([("Cap: ", "Cream x brown trucker cap with an OLYMPIA logo"), ("Outfit: ", "Dark brown zip jacket + grey sweatpants")]),
    p("In the 4K arrival footage posted on the official YouTube channel of Korean entertainment outlet WoW!Korea, ISSA can be seen clearly walking beside DAIKI from around 1:45.<br>\n"
      "He wore the cap pulled low, a black shoulder bag across his body, and walked with his head slightly down.<br>\n"
      "Whenever he looked ahead, the front of the cap faced the camera and the round logo on the light fabric was easy to see."),
    img_html(m_full, "ISSA arriving at Gimpo Airport in a cream-and-brown trucker cap and a dark brown jacket", f"Source: {SRC}"),
    p(f"Up close, the logo reads {mk('\"OLYMPIA\" in large navy letters', True)}.<br>\n"
      "Above it is a gold round emblem with a horseshoe in the middle and small \"BEER\" and \"SINCE 1896\" lettering around it.<br>\n"
      "Below \"OLYMPIA,\" a small script line reads \"It's the Water.\""),
    img_html(m_cap, "Close-up of the OLYMPIA logo trucker cap ISSA wore", f"Source: {SRC}"),
    h2("The cap: Trucker Hat USA's Olympia Beer Hat"),
    ui.minibox([("Brand: ", "Trucker Hat USA"), ("Model: ", "Appears to be the Olympia Beer Hat (brown x cream)")]),
    p("Searching for that combination of a round \"BEER / SINCE 1896\" emblem, a horseshoe, navy \"OLYMPIA\" lettering and a script \"It's the Water\" leads to the Olympia Beer Hat sold by US cap shop Trucker Hat USA.<br>\n"
      f"Compared with the product photo, {mk('the logo layout, lettering colors, and cream front with brown brim and mesh', True)} all match ISSA's cap.<br>\n"
      "He hasn't said where he bought it, though, so we're presenting it as a cap with the same design."),
    ui.infobox("Olympia Beer Hat specs", [
        ("Brand", "Trucker Hat USA"),
        ("Colors", "Brown / White Front and 20+ other colors"),
        ("Material", "55% foam, 45% mesh"),
        ("Size", "One size (snapback)"),
        ("Price", "18.99 USD (official US store) / 6,600 yen incl. tax (Japan)"),
    ]),
    h2("What is Olympia beer?"),
    ui.minibox([("Origin: ", "Washington State, USA (founded 1896)"), ("Slogan: ", "It's the Water")]),
    ui.leftbox("What is Olympia beer?",
               "<p style=\"margin:0;\">Olympia was started in 1896 by German immigrant Leopold Schmidt in Tumwater, Washington.<br>\n"
               "The company was first called Capital Brewing and became Olympia in 1902.<br>\n"
               "Brewed with local artesian water, it was long known for the slogan \"It's the Water.\"</p>"),
    p("The horseshoe at the center of the logo is a well-known good-luck symbol, and inside it is the waterfall that stood near the brewery.<br>\n"
      "The brand later became part of Pabst, which announced a temporary pause in production in January 2021.<br>\n"
      "The beer itself is now hard to find, but the retro logo lives on in tees and caps like ISSA's."),
    p("By the way, DAIKI, walking next to ISSA that day, wore BAPE's red paisley shark hoodie.<br>\n"
      f"See <a href=\"{DAIKI_EN}\" target=\"_blank\" rel=\"noopener\">our article on DAIKI's Gimpo airport outfit</a> for details."),
    h2("Price and where to buy"),
    ui.minibox([("Price: ", "18.99 USD (US) / 6,600 yen (Japan)"), ("Where: ", "Trucker Hat USA official store, RAWDRIP (Japan)")]),
    p(f"Trucker Hat USA's official online store sells it for {mk('18.99 USD', True)}.<br>\n"
      "In Japan, select shop RAWDRIP lists the \"Trucker Hat USA Olympia Brewing Company - Brown\" for 6,600 yen (tax included), and it could be added to the cart as of October 11, 2026.<br>\n"
      "Check international shipping options and fees before ordering."),
    ui.barbox("Where to buy the OLYMPIA trucker cap", [
        f'<a href="{THU}" target="_blank" rel="noopener">Trucker Hat USA official store: Olympia Beer Hat</a> (18.99 USD)',
        f'<a href="{RAWDRIP}" target="_blank" rel="noopener">RAWDRIP (Japan): Trucker Hat USA Olympia Brewing Company - Brown</a> (6,600 yen)',
        "Vintage shops and resale apps: old Olympia promo caps also turn up",
    ]),
    h2("What about the jacket and pants?"),
    ui.minibox([("Jacket: ", "Dark brown zip jacket (brand not identified)"), ("Pants: ", "Grey wide sweatpants")]),
    p("The jacket was a high-neck dark brown zip-up with short red stitches dotted along both sleeves, a slightly unusual design.<br>\n"
      "No logo or tag was visible in the footage, so the brand couldn't be identified.<br>\n"
      "He paired it with loose grey sweatpants, matching the cap and jacket in brown and lightening things up with grey below."),
    h2("Summary"),
    ui.summarybox([
        "ISSA's cap at Gimpo Airport on Oct 7, 2026 is a trucker cap with the logo of Olympia beer",
        "The logo and colors match Trucker Hat USA's Olympia Beer Hat (brown x cream)",
        "18.99 USD on the official US store, 6,600 yen (tax incl.) at RAWDRIP in Japan",
        "Olympia is a beer born in Washington State in 1896, known for \"It's the Water\"",
        "The dark brown jacket's brand couldn't be identified",
    ]),
    p("Picking a vintage beer logo shows off ISSA's love of American casual style.<br>\n"
      "The cap is affordable, so matching ISSA's airport look could be fun!"),
    ui.linkbox("More on ISSA", EN_REL),
])


def plain(s):
    return re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", s))


print("JP title", len(JP_TITLE), JP_TITLE, "| body", len(plain(JP)))
if DRY:
    (ROOT / "tmp_issa_olympia_preview.html").write_text(JP, encoding="utf-8")
    sys.exit()

JP_SUM = ("KO1KEYZのISSAが10月7日に金浦空港でかぶっていたクリーム×茶色のキャップは、アメリカのビール「Olympia」のロゴ入り。"
          "Trucker Hat USAのOlympia Beer Hatとみられ、日本では6,600円で買えます。")
KR_SUM = ("KO1KEYZ ISSA가 10월 7일 김포공항에서 쓴 크림×갈색 모자는 미국 맥주 'Olympia' 로고 트러커 캡. "
          "Trucker Hat USA의 Olympia Beer Hat으로 보이며 18.99달러입니다.")
EN_SUM = ("The cream-and-brown cap KO1KEYZ's ISSA wore at Gimpo Airport on Oct 7 carries the logo of American beer Olympia. "
          "It appears to be Trucker Hat USA's Olympia Beer Hat, priced at 18.99 USD.")

jp_eye = make_eyecatch(["--top", "ISSAの空港キャップは？", "--main", "KO1KEYZ", "--bottom", "まさかのビールのロゴ！"],
                       ROOT / "images" / "issa_gimpo_olympia_eyecatch.png")
jp = post_draft(JP_TITLE, JP, JP_SLUG, "ja", [66, 92, 63], jp_eye, JP_SUM)
print("JP", jp["id"], jp["slug"])
kr_eye = make_eyecatch(["--top", "ISSA 공항 모자는?", "--main", "KO1KEYZ", "--bottom", "설마 맥주 로고!", "--lang", "kr"],
                       ROOT / "images" / "issa_gimpo_olympia_eyecatch_kr.png")
kr = post_draft(KR_TITLE, KR, f"{JP_SLUG}-kr", "ko", [74, 78], kr_eye, KR_SUM, translations={"ja": jp["id"]})
print("KR", kr["id"], kr["slug"])
en = post_draft(EN_TITLE, EN, f"{JP_SLUG}-en", "en", [110, 118], jp_eye, EN_SUM, translations={"ja": jp["id"]})
print("EN", en["id"], en["slug"])
print("DONE", f"{WP_URL}/?p={jp['id']}", f"{WP_URL}/?p={kr['id']}", f"{WP_URL}/?p={en['id']}")
