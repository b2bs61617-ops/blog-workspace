# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _build_tv_schedule_1108_1114 import *

T = Theme("#8a8378", "#f7f6f4", "#ddd9d3")
M = '<span class="swl-marker mark_yellow">'

# ---------- JP ----------
b = ""
b += p("デビュー6週目に入ったKO1KEYZ(コイキーズ)。",
       "11月8日(日)〜14日(土)のテレビ欄と公式サイトをチェックしたところ、今週いちばんの注目は、",
       f"<strong>{M}11/10(火)20:00の日本テレビ「踊る！さんま御殿!!」にYOSHIKIが“奈良県代表”で出演すること</span></strong>です。",
       "週の初めの11/8(日)はソウルで「2026 KO1KEYZ 1ST FAN MEETING IN SEOUL」の2日目があり、11/12(木)にはCSのKNTVで「ショー！K-POPの中心」の字幕版が再放送されます。")
b += p("この記事では、出演番組の日時に加えて、MV放送やYouTubeの更新日、LAPOSTA 2027のFC先行の締め切りまで日付順にまとめています。", NOTE)
b += T.toc(["11/8〜11/14のテレビ・配信スケジュール早見表", "YOSHIKIが出る「さんま御殿」の内容",
            "ソウルのファンミーティング2日目", "KNTV「ショー！K-POPの中心」の再放送",
            "MV放送とYouTubeの更新日", "LAPOSTA 2027のFC先行の締め切り", "11月後半の出演予定"])
b += h2("KO1KEYZのテレビ・配信スケジュール早見表(11/8〜11/14)")
b += p("まずは1週間の予定を一覧にしました。",
       "太字がメンバーの出演番組やイベントで、それ以外はMV放送や配信など関連する予定です。")
b += T.table(["日時", "番組・予定"], [
    ["11/8(日)", "2026 KO1KEYZ 1ST FAN MEETING IN SEOUL(2日目)", True],
    ["11/8(日)22:00〜23:00", "エムオン!「あなたの推し曲は!? エムオン!リクエストアワー」(MV)"],
    ["11/10(火)20:00〜21:00", "日本テレビ「踊る！さんま御殿!!」(YOSHIKI)", True],
    ["11/12(木)9:45〜11:15", "スカチャン1(KNTV)「ショー！K-POPの中心」#966(字幕・再放送)", True],
    ["11/12(木)21:00〜", "公式YouTube「KO1! KO1! KO1KEYZ!」(毎週木曜更新)"],
    ["11/15(日)23:59", "「LAPOSTA 2027」FC会員先行の受付締め切り"],
])
b += p("先週はソウルのファンミーティング1日目に向けて、KNTVの字幕版やMV放送が中心の1週間でした。",
       "6週目は、メンバーが日本の地上波のゴールデン帯のトーク番組に出演します。",
       "グループでの日本のテレビ出演は11月5日時点で発表されていないので、新しい出演が決まったら追記します。")

b += h2("11/10(火)「さんま御殿」にYOSHIKIが奈良県代表で出演")
b += T.info([("放送日時", "11月10日(火)20:00〜21:00 日本テレビ"),
             ("テーマ", "ライバル隣県バトル！京都×奈良×滋賀×三重が地元の魅力アピール合戦！"),
             ("出演", "YOSHIKI(奈良県チーム)")])
b += p("11月10日(火)20:00からの日本テレビ「踊る！さんま御殿!!」に、YOSHIKIが出演します。",
       "今回のテーマは「ライバル隣県バトル」で、京都・奈良・滋賀・三重の出身者が地元の魅力をアピールし合います。",
       f"番組表の出演者欄では、<strong>{M}YOSHIKIは「奈良県」チーム</span></strong>に入っています。")
b += p("奈良県チームは、ロッチの中岡創一さん、柔道の野村忠宏さん、GALEDGE.のYUINEKOさん、ゆりやんレトリィバァさん、そしてYOSHIKIの5人です。",
       "京都府チームには大倉士門さんやギャル曽根さん、滋賀県チームにはくっきー！さん、三重県チームにはGENERATIONSの小森隼さんなどが並びます。")
b += p("番組表では、中岡創一さんが「リニア新幹線で奈良が京都を逆転する」と豪語したり、“奈良のウユニ塩湖”と呼ばれる絶景が紹介されたりと、奈良県チームの見せ場も予告されています。",
       "明石家さんまさんのトークの中で、YOSHIKIが地元・奈良のどんな魅力を話すのか、デビューしてすぐのゴールデン帯のトーク番組でどんな姿を見せるのかに注目です。",
       "KO1KEYZのメンバーとして番組表に名前が載っているので、録画予約は「KO1KEYZ」や「YOSHIKI」で検索すると見つけやすいです。")

b += h2("11/8(日)ソウルのファンミーティング2日目")
b += T.info([("公演名", "2026 KO1KEYZ 1ST FAN MEETING IN SEOUL"),
             ("日程", "2026年11月7日(土)・8日(日)"),
             ("会場", "BLUESQUARE WOORI WON BANKING HALL(ソウル)")])
b += p("11月8日(日)は、ソウルのBLUESQUARE WOORI WON BANKING HALLで「2026 KO1KEYZ 1ST FAN MEETING IN SEOUL」の2日目が開かれます。",
       "会場では、FC会員向けのFANCLUB BOOTHや、KO1KEYZ Chat会員限定の「Plus Chat BOOTH」(メンバーの手書きメッセージ入りカード)、BLUE SQUARE NEMOでのグッズ・アルバム販売が、10:00〜13:30と14:30〜18:00(現地時間)に行われます。",
       "オフィシャルグッズを75,000ウォン買うごとに、先着でソロ12種のトレーディングカードが1枚もらえます。",
       "支払いは韓国ウォンのみなので、現地に行く方は準備しておきましょう。")

b += h2("11/12(木)KNTV「ショー！K-POPの中心」#966の再放送")
b += T.info([("放送日時", "11月12日(木)9:45〜11:15"),
             ("チャンネル", "スカチャン1(KNTV)"),
             ("番組名", "ショー！K-POPの中心 #966(日本語字幕・再放送)")])
b += p("CSのKNTVでは、11月12日(木)9:45から、韓国MBCの音楽番組「ショー！K-POPの中心」#966の字幕版が再放送されます。",
       "番組表の出演者欄には、BOYNEXTDOOR、CRAVITY、NCT WISH、Hearts2Hearts、KickFlipなどと並んでKO1KEYZの名前があります。",
       "11/3(火)に初回放送された回なので、見逃した方はこの再放送でチェックできます。")
b += p("なお、11/10(火)14:00からの#967の出演者欄には、11月5日時点でKO1KEYZの名前はありません。",
       "KNTVの視聴には、スカパー！などでの契約が必要です。")

b += h2("MV放送とYouTubeの更新日")
b += p("メンバーの出演ではありませんが、11月8日(日)22:00からのCS・エムオン!「あなたの推し曲は!? エムオン!リクエストアワー」では、オンエア予定にKO1KEYZの名前があります。",
       "オンエア楽曲は予告なく変わる場合があるので、録画しておくと確実です。")
b += p("公式YouTubeの「KO1! KO1! KO1KEYZ!」は毎週木曜21:00更新なので、今週は11月12日(木)が更新日です。",
       "11月5日には、TikTokで「恋GAME」のオリジナルゲームエフェクトも公開されていて、「#恋GAMEで遊ぼ」をつけた投稿が呼びかけられています。")

b += h2("LAPOSTA 2027のFC先行は11/15まで")
b += p("2027年1月の東京ドーム、2月の京セラドーム大阪で行われる「LAPOSTA 2027」は、KO1KEYZ OFFICIAL FANCLUBの会員先行が受付中です。",
       "受付期間は<strong>11月4日(水)12:00〜11月15日(日)23:59</strong>で、当落発表は11月26日(木)20:00です。",
       "チケットは指定席15,400円(税込)で、別にプレイガイドの手数料がかかります。",
       "締め切りは今週末の翌日なので、申し込みを忘れないようにしておきましょう。")

b += h2("11月後半の出演予定は？")
b += p("ソウルのファンミーティングのあとは、21日(土)に京セラドーム大阪で行われる「2026 MAMA AWARDS」に出演し、翌22日(日)には札幌の「SAPPORO COLLECTION 2026 AUTUMN/WINTER」に出演します。",
       "11/13(金)・14(土)の番組表や、テレビの新しい出演が発表されたら追記します。",
       "先週分は<a href=\"https://chomoand-1.com/ko1keyz-tv-schedule-1101-1107-15316\">11/1〜11/7の放送予定まとめ</a>にまとめているので、あわせてご覧ください。")

b += h2("まとめ")
b += T.summary(["11/10(火)20:00「さんま御殿」にYOSHIKIが奈良県チームで出演",
                "11/8(日)はソウルで1ST FAN MEETINGの2日目",
                "11/12(木)9:45にKNTVで「ショー！K-POPの中心」#966字幕版の再放送",
                "MVは11/8(日)22:00エムオン!、YouTube更新は11/12(木)21:00",
                "LAPOSTA 2027のFC先行は11/15(日)23:59まで、当落は11/26(木)",
                "11/21(土)MAMA AWARDS、11/22(日)SAPPORO COLLECTIONに出演"])
b += p("デビュー6週目は、ソウルでのファンミーティングの締めくくりと、YOSHIKIの地上波トーク番組への出演が重なる1週間になりそうです。",
       "さんま御殿はゴールデン帯の放送なので、録画予約を忘れないようにしておきましょう！")
b += T.related("あわせて読みたいKO1KEYZの番組・スケジュール記事", [
    ("https://chomoand-1.com/ko1keyz-tv-schedule-1101-1107-15316", "KO1KEYZのテレビ出演 11/1〜11/7まとめ"),
    ("https://chomoand-1.com/ko1keyz-tv-schedule-1025-1031-15178", "KO1KEYZのテレビ出演 10/25〜10/31まとめ"),
    ("https://chomoand-1.com/ko1keyz-venue101-autograph-board-15246", "KO1KEYZのVenue101サインは？")])
save("ko1keyz_tv_schedule_1108_1114.html", b)

# ---------- KR ----------
NOTE_KR = "※2026년 11월 5일 기준 정보입니다. 11/13(금)·14(토)는 아직 편성표가 나오지 않아 알 수 있는 범위에서만 실었습니다. 방송 내용·시간은 바뀔 수 있으니 최신 정보는 공식 사이트나 편성표에서 확인해 주세요."
k = ""
k += p("데뷔 6주 차에 들어선 KO1KEYZ(코이키즈).",
       "11월 8일(일)~14일(토)의 일본 TV 편성표와 공식 사이트를 확인해 보니, 이번 주 가장 큰 화제는",
       f"<strong>{M}11/10(화) 20:00 니혼TV '오도루! 산마 고텐!!'에 YOSHIKI가 '나라현 대표'로 출연</span></strong>하는 것입니다.",
       "11/8(일)에는 서울에서 '2026 KO1KEYZ 1ST FAN MEETING IN SEOUL' 둘째 날 공연이 있고, 11/12(목)에는 CS 채널 KNTV에서 '쇼! 음악중심' 일본어 자막판이 재방송됩니다.")
k += p("이 글에서는 출연 프로그램 일정과 함께 MV 방송, YouTube 업데이트일, LAPOSTA 2027 FC 선행 마감일까지 날짜순으로 정리했습니다.", NOTE_KR)
k += T.table(["일시(일본 시간)", "프로그램·일정"], [
    ["11/8(일)", "2026 KO1KEYZ 1ST FAN MEETING IN SEOUL(2일 차)", True],
    ["11/8(일) 22:00~23:00", "M-ON! '엠온! 리퀘스트 아워'(MV)"],
    ["11/10(화) 20:00~21:00", "니혼TV '오도루! 산마 고텐!!'(YOSHIKI)", True],
    ["11/12(목) 9:45~11:15", "스카챤1(KNTV) '쇼! 음악중심' #966(일본어 자막·재방송)", True],
    ["11/12(목) 21:00~", "공식 YouTube 'KO1! KO1! KO1KEYZ!'(매주 목요일 업데이트)"],
    ["11/15(일) 23:59", "'LAPOSTA 2027' FC 회원 선행 접수 마감"],
])
k += h2("11/10(화) '산마 고텐'에 YOSHIKI가 나라현 대표로 출연")
k += T.info([("방송", "11월 10일(화) 20:00~21:00 니혼TV"),
             ("주제", "라이벌 이웃 현 배틀! 교토×나라×시가×미에 지역 매력 어필 대결"),
             ("출연", "YOSHIKI(나라현 팀)")])
k += p("11월 10일(화) 20:00부터 방송되는 니혼TV의 인기 토크 프로그램 '오도루! 산마 고텐!!'에 YOSHIKI가 출연합니다.",
       "이번 주제는 '라이벌 이웃 현 배틀'로, 교토·나라·시가·미에 출신 출연자들이 고향의 매력을 서로 어필합니다.",
       f"편성표 출연자 목록에서 <strong>{M}YOSHIKI는 '나라현' 팀</span></strong>에 이름을 올렸습니다.")
k += p("나라현 팀은 롯치의 나카오카 소이치, 유도 선수 출신 노무라 타다히로, GALEDGE.의 YUINEKO, 유리양 레트리버, 그리고 YOSHIKI 5명입니다.",
       "아카시야 산마의 토크 속에서 YOSHIKI가 고향 나라의 어떤 매력을 이야기할지, 데뷔 직후 골든 타임 토크 프로그램에서 어떤 모습을 보여줄지 주목됩니다.")
k += h2("11/8(일) 서울 팬미팅 2일 차")
k += p("11월 8일(일)에는 서울 BLUESQUARE 우리WON뱅킹홀에서 '2026 KO1KEYZ 1ST FAN MEETING IN SEOUL' 2일 차 공연이 열립니다.",
       "현장에서는 FANCLUB BOOTH, KO1KEYZ Chat 회원 한정 'Plus Chat BOOTH', BLUE SQUARE NEMO의 굿즈·앨범 판매가 10:00~13:30, 14:30~18:00(현지 시간)에 진행됩니다.",
       "오피셜 굿즈를 75,000원 구매할 때마다 선착순으로 솔로 트레이딩 카드(12종 중 랜덤) 1장을 받을 수 있습니다.")
k += h2("11/12(목) KNTV '쇼! 음악중심' #966 재방송")
k += p("일본 CS 채널 KNTV에서는 11월 12일(목) 9:45부터 MBC '쇼! 음악중심' #966 일본어 자막판이 재방송됩니다.",
       "편성표 출연자 목록에는 BOYNEXTDOOR, CRAVITY, NCT WISH, Hearts2Hearts, KickFlip 등과 함께 KO1KEYZ의 이름이 있습니다.",
       "11/3(화)에 처음 방송된 회차라서, 놓친 분들은 이번 재방송으로 볼 수 있습니다.")
k += h2("MV 방송과 YouTube 업데이트")
k += p("11월 8일(일) 22:00 M-ON! '엠온! 리퀘스트 아워'의 방송 예정 목록에 KO1KEYZ의 이름이 있습니다.",
       "공식 YouTube 'KO1! KO1! KO1KEYZ!'는 매주 목요일 21:00에 업데이트되므로 이번 주는 11월 12일(목)입니다.",
       "11월 5일에는 TikTok에서 '恋GAME(코이 GAME)' 오리지널 게임 이펙트도 공개되었습니다.")
k += h2("LAPOSTA 2027 FC 선행은 11/15까지")
k += p("2027년 1월 도쿄돔, 2월 교세라돔 오사카에서 열리는 'LAPOSTA 2027'의 KO1KEYZ OFFICIAL FANCLUB 회원 선행 접수가 진행 중입니다.",
       "접수 기간은 <strong>11월 4일(수) 12:00~11월 15일(일) 23:59</strong>(일본 시간)이며, 당첨 발표는 11월 26일(목) 20:00입니다.",
       "티켓은 지정석 15,400엔(세금 포함)입니다.")
k += h2("11월 후반 일정은?")
k += p("서울 팬미팅 이후에는 21일(토) 교세라돔 오사카에서 열리는 '2026 MAMA AWARDS'에, 22일(일)에는 삿포로의 'SAPPORO COLLECTION 2026 AUTUMN/WINTER'에 출연합니다.",
       "새로운 TV 출연이 발표되면 추가하겠습니다.",
       "지난주 일정은 <a href=\"https://chomoand-1.com/ko/ko1keyz-tv-schedule-1101-1107-kr-15317\">11/1~11/7 방송 일정 정리</a>에서 확인할 수 있습니다.")
k += h2("정리")
k += T.summary(["11/10(화) 20:00 '산마 고텐'에 YOSHIKI가 나라현 팀으로 출연",
                "11/8(일) 서울 1ST FAN MEETING 2일 차",
                "11/12(목) 9:45 KNTV '쇼! 음악중심' #966 자막판 재방송",
                "MV는 11/8(일) 22:00 M-ON!, YouTube 업데이트는 11/12(목) 21:00",
                "LAPOSTA 2027 FC 선행은 11/15(일) 23:59까지, 당첨 발표 11/26(목)",
                "11/21(토) MAMA AWARDS, 11/22(일) SAPPORO COLLECTION 출연"])
save("ko1keyz_tv_schedule_1108_1114_kr.html", k)

# ---------- EN ----------
NOTE_EN = "*Information as of November 5, 2026 (all times JST). Listings for Nov 13-14 have not been released yet. Broadcast details may change, so please check official sites and TV listings for the latest information."
e = ""
e += p("KO1KEYZ are now in their sixth week since debut.",
       f"Looking through Japanese TV listings and the official site for November 8-14, the biggest news this week is that <strong>{M}YOSHIKI appears on Nippon TV's talk show \"Odoru! Sanma Goten!!\" on Tuesday, Nov 10 at 20:00 as a representative of Nara Prefecture</span></strong>.",
       "The week opens with day two of the \"2026 KO1KEYZ 1ST FAN MEETING IN SEOUL\" on Sunday, Nov 8, and KNTV re-airs the subtitled Show! Music Core episode featuring KO1KEYZ on Thursday, Nov 12.")
e += p("This post lists the TV appearances along with MV airplay, the YouTube update day and the LAPOSTA 2027 fan club ticket deadline in date order.", NOTE_EN)
e += T.table(["Date / time (JST)", "Program / event"], [
    ["Sun 11/8", "2026 KO1KEYZ 1ST FAN MEETING IN SEOUL (Day 2)", True],
    ["Sun 11/8 22:00-23:00", "M-ON! \"M-ON! Request Hour\" (MV)"],
    ["Tue 11/10 20:00-21:00", "Nippon TV \"Odoru! Sanma Goten!!\" (YOSHIKI)", True],
    ["Thu 11/12 9:45-11:15", "Sky Channel 1 (KNTV) \"Show! Music Core\" #966 (subtitled rerun)", True],
    ["Thu 11/12 21:00-", "Official YouTube \"KO1! KO1! KO1KEYZ!\" (weekly Thursday update)"],
    ["Sun 11/15 23:59", "LAPOSTA 2027 fan club presale closes"],
])
e += h2("YOSHIKI on \"Sanma Goten\" as Team Nara (Tue 11/10)")
e += p("YOSHIKI joins Nippon TV's prime-time talk show \"Odoru! Sanma Goten!!\" on Tuesday, November 10 from 20:00.",
       "The theme is a \"neighboring prefecture rivalry battle\" in which guests from Kyoto, Nara, Shiga and Mie promote the charms of their hometowns.",
       "According to the listing, YOSHIKI is on Team Nara alongside Soichi Nakaoka (Rotchi), judo legend Tadahiro Nomura, YUINEKO (GALEDGE.) and Yuriyan Retriever.",
       "It is one of the first solo appearances by a KO1KEYZ member on a prime-time terrestrial talk show, so it is well worth recording.")
e += h2("Seoul fan meeting, Day 2 (Sun 11/8)")
e += p("Day two of the \"2026 KO1KEYZ 1ST FAN MEETING IN SEOUL\" takes place on November 8 at BLUESQUARE WOORI WON BANKING HALL.",
       "The fan club booth, the KO1KEYZ Chat \"Plus Chat BOOTH\" and the merch and album sales at BLUE SQUARE NEMO run from 10:00-13:30 and 14:30-18:00 local time.",
       "Every 75,000 won spent on official merch gets you a random solo trading card while supplies last.")
e += h2("KNTV re-airs Show! Music Core #966 (Thu 11/12)")
e += p("On Thursday, November 12 at 9:45, the Japanese CS channel KNTV re-airs the subtitled version of MBC's Show! Music Core #966.",
       "KO1KEYZ are listed among the performers along with BOYNEXTDOOR, CRAVITY, NCT WISH, Hearts2Hearts and KickFlip.",
       "This episode first aired in Japan on November 3, so the rerun is a second chance to catch it.")
e += h2("MV airplay and YouTube")
e += p("KO1KEYZ are on the planned playlist for M-ON!'s \"M-ON! Request Hour\" on Sunday, November 8 at 22:00.",
       "The official YouTube series \"KO1! KO1! KO1KEYZ!\" updates every Thursday at 21:00, so the next episode is due on November 12.",
       "A \"Koi GAME\" game effect was also released on TikTok on November 5.")
e += h2("LAPOSTA 2027 fan club presale ends 11/15")
e += p("The KO1KEYZ OFFICIAL FANCLUB presale for LAPOSTA 2027 (Tokyo Dome in January and Kyocera Dome Osaka in February 2027) is open from November 4 at 12:00 until <strong>November 15 at 23:59 JST</strong>.",
       "Results will be announced on November 26 at 20:00, and reserved seats cost 15,400 yen including tax.")
e += h2("What's next in November?")
e += p("After Seoul, KO1KEYZ will perform at the \"2026 MAMA AWARDS\" at Kyocera Dome Osaka on Saturday, November 21, and at \"SAPPORO COLLECTION 2026 AUTUMN/WINTER\" in Sapporo on Sunday, November 22.",
       "We will add any new TV appearances as they are announced.",
       "Last week's schedule is in <a href=\"https://chomoand-1.com/en/ko1keyz-tv-schedule-1101-1107-en-15318\">KO1KEYZ TV Appearances 11/1-11/7</a>.")
e += h2("Summary")
e += T.summary(["Tue 11/10 20:00: YOSHIKI on \"Sanma Goten\" as Team Nara",
                "Sun 11/8: Day 2 of the 1ST FAN MEETING in Seoul",
                "Thu 11/12 9:45: KNTV re-airs subtitled Show! Music Core #966",
                "MV on M-ON! (Sun 11/8 22:00), YouTube update Thu 11/12 21:00",
                "LAPOSTA 2027 fan club presale closes Sun 11/15 23:59, results 11/26",
                "MAMA AWARDS on 11/21 and SAPPORO COLLECTION on 11/22"])
save("ko1keyz_tv_schedule_1108_1114_en.html", e)
