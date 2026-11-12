# -*- coding: utf-8 -*-
from common import *

T = Theme("#8a8378", "#f7f6f4", "#ddd9d3")
M = '<span class="swl-marker mark_yellow">'

# ---------- JP ----------
b = ""
b += p("デビュー7週目に入ったKO1KEYZ(コイキーズ)。",
       "2026年11月15日(日)〜21日(土)のテレビ欄と公式サイトをチェックしました。",
       f"今週いちばんの注目は、<strong>{M}11/21(土)に京セラドーム大阪で開かれる「2026 MAMA AWARDS」への出演</span></strong>です。")
b += p("当日はCSのMnet Japanや配信のMnet Plusで生中継されるので、会場に行けない方も家で見られます。",
       "週の初めの11/15(日)は、LAPOSTA 2027のFC先行と、ソウルファンミのグッズ通販の締め切りが重なります。")
b += p("この記事では、MAMAの見方に加えて、MV放送やYouTubeの更新日、締め切りの日まで日付順にまとめました。")
b += NOTE_P
b += T.toc(["11/15〜11/21のテレビ・配信スケジュール早見表", "11/21(土)MAMA AWARDSの時間と見方",
            "11/15(日)が締め切りのFC先行とグッズ通販", "MV放送とYouTubeの更新日",
            "11/22(日)札幌コレクションと12月の予定", "地上波のテレビ出演はある？"])

b += h2("KO1KEYZのテレビ・配信スケジュール早見表(11/15〜21)")
b += p("まずは1週間の予定を一覧にしました。",
       "太字がメンバーの出演やイベントで、それ以外はMV放送や締め切りなどの関連する予定です。")
b += T.table(["日時", "番組・予定"], [
    ["11/15(日)23:59", "「LAPOSTA 2027」FC会員先行の受付締め切り"],
    ["11/15(日)23:59", "ソウルファンミのグッズ事後通販(LAPONE STORE)締め切り"],
    ["11/17(火)22:00〜23:00", "エムオン!「あなたの推し曲は!? エムオン!リクエストアワー」(MV)"],
    ["11/19(木)21:00〜", "公式YouTube「KO1! KO1! KO1KEYZ!」(毎週木曜更新)"],
    ["11/21(土)12:30〜", "2026 MAMA AWARDS レッドカーペット", True],
    ["11/21(土)15:00〜", "2026 MAMA AWARDS 授賞式(京セラドーム大阪)", True],
])
b += p("先週は、YOSHIKIさんの「さんま御殿」と、DAIKIさんとRYUJIさんの「ヒルナンデス！」で、地上波の個人出演が続きました。",
       "今週は、地上波の番組表にはメンバーの名前が見つかっていません。",
       "そのかわり、週末に大きな授賞式のステージが待っています。")

b += h2("11/21(土)「2026 MAMA AWARDS」に出演")
b += T.info([("日程", "2026年11月21日(土)CHAPTER 2"),
             ("時間", "レッドカーペット12:30〜/授賞式15:00〜"),
             ("会場", "京セラドーム大阪"),
             ("見方", "CS「Mnet Japan」・配信「Mnet Plus」「Mnet Smart+」で生中継")])
b += p("KO1KEYZは、11月21日(土)の「2026 MAMA AWARDS」に出演します。",
       "MAMAは、韓国のCJ ENMが開く、アジア最大級の音楽授賞式です。",
       f"今年は<strong>{M}11月20日(金)・21日(土)の2日間、京セラドーム大阪</span></strong>で開かれます。")
b += p("KO1KEYZが出るのは、2日目の「CHAPTER 2」です。",
       "同じ日には、LE SSERAFIMやZEROBASEONE、CORTISなどの出演が発表されています。",
       "デビューして2か月足らずで、ドームの授賞式のステージに立つことになります。")
b += p("授賞式は15:00から、その前の12:30からはレッドカーペットがあります。",
       "レッドカーペットは、Mnet PlusとMAMAの公式YouTubeでも生配信されます。",
       "メンバーがどんな衣装で登場するのかにも注目です。")
b += h3("家で見るならMnet JapanかMnet Plus")
b += p("テレビで見る場合は、CS放送の「Mnet Japan」で生中継されます。",
       "スカパー！やケーブルテレビなどでの契約が必要なので、早めに確かめておきましょう。")
b += p("スマホやパソコンで見るなら、「Mnet Plus」や「Mnet Smart+」の生配信があります。",
       "どの賞にノミネートされているか、どの曲を披露するかは、発表があれば追記します。")

b += h2("11/15(日)はFC先行とグッズ通販の締め切り")
b += h3("「LAPOSTA 2027」のFC会員先行")
b += p("2027年1月の東京ドーム、2月の京セラドーム大阪で行われる「LAPOSTA 2027」は、FC会員先行の受付が11月15日(日)23:59までです。",
       "当落の発表は、11月26日(木)20:00の予定です。",
       "チケットは指定席15,400円(税込)で、別にプレイガイドの手数料がかかります。")
b += h3("ソウルファンミのグッズ事後通販")
b += p(f"ソウルの「2026 KO1KEYZ 1ST FAN MEETING IN SEOUL」のグッズは、<strong>{M}LAPONE STOREで11月15日(日)23:59まで</span></strong>事後通販をしています。",
       "税込7,000円ごとに、先着でソロ12種のトレーディングカードがランダムで1枚つきます。",
       "数に限りがあり、上限に達したら販売終了になるので、ほしい方は早めに申し込みましょう。")
b += p("発送は2026年12月末ごろの予定です。",
       "どちらも同じ日の23:59が締め切りなので、忘れないように気をつけましょう。")

b += h2("MV放送とYouTubeの更新日")
b += p("メンバーの出演ではありませんが、11月17日(火)22:00からのCS・エムオン!「あなたの推し曲は!? エムオン!リクエストアワー」では、オンエア予定にKO1KEYZの名前があります。",
       "オンエアの曲は予告なく変わることがあるので、録画しておくと確実です。")
b += p("公式YouTubeの「KO1! KO1! KO1KEYZ!」は毎週木曜21:00更新なので、今週は11月19日(木)が更新日です。",
       "MAMAの前の週なので、準備の様子などが見られるかもしれません。")

b += h2("11/22(日)札幌コレクションと12月の予定")
b += p("MAMAの翌日、11月22日(日)には、札幌コンベンションセンターで開かれる「SAPPORO COLLECTION 2026 AUTUMN/WINTER」にアーティストとして出演します。",
       "開演は14:00の予定で、大阪から札幌へと2日続けてのステージになります。")
b += p("12月14日(月)には、デジタルシングル「White Love」の配信も決まっています。",
       "冬のラブソングになりそうなタイトルで、続報が楽しみです。")

b += h2("地上波のテレビ出演はある？")
b += p("11月12日時点で、11/15〜11/19の地上波の番組表には、KO1KEYZのメンバーの名前は見つかりませんでした。",
       "11/20(金)・21(土)分はまだ番組表が出ていないので、新しい出演が決まったら追記します。")
b += p("先週分は<a href=\"https://chomoand-1.com/ko1keyz-tv-schedule-1108-1114-15407\">11/8〜11/14の放送予定まとめ</a>にまとめているので、あわせてご覧ください。")

b += h2("まとめ")
b += T.summary(["11/21(土)京セラドーム大阪の「2026 MAMA AWARDS」に出演",
                "レッドカーペット12:30〜、授賞式15:00〜",
                "Mnet Japan(CS)・Mnet Plus・Mnet Smart+で生中継",
                "LAPOSTA 2027のFC先行は11/15(日)23:59まで、当落は11/26(木)",
                "ソウルファンミのグッズ事後通販も11/15(日)23:59まで",
                "MVは11/17(火)22:00エムオン!、YouTube更新は11/19(木)21:00",
                "11/22(日)SAPPORO COLLECTION、12/14(月)White Love配信"])
b += p("デビュー7週目は、週末のMAMAで大きなステージに立つ1週間になりそうです。",
       "締め切りが2つ重なる11/15(日)も、忘れないようにしておきましょう！")
b += T.related("あわせて読みたいKO1KEYZの番組・スケジュール記事", [
    ("https://chomoand-1.com/ko1keyz-tv-schedule-1108-1114-15407", "KO1KEYZのテレビ出演 11/8〜11/14まとめ"),
    ("https://chomoand-1.com/ko1keyz-tv-schedule-1101-1107-15316", "KO1KEYZのテレビ出演 11/1〜11/7まとめ"),
    ("https://chomoand-1.com/ko1keyz-venue101-autograph-board-15246", "KO1KEYZのVenue101サインは？")])
save("ko1keyz_tv_schedule_1115_1121.html", b)

# ---------- KR ----------
k = ""
k += p("데뷔 7주 차에 들어선 KO1KEYZ(코이키즈).",
       "2026년 11월 15일(일)~21일(토) 일본 TV 편성표와 공식 사이트를 확인했어요.",
       f"이번 주 가장 큰 일정은 <strong>{M}11/21(토) 교세라돔 오사카에서 열리는 '2026 MAMA AWARDS' 출연</span></strong>이에요.")
k += p("Mnet Japan과 Mnet Plus에서 생중계되니, 현장에 못 가는 분들도 집에서 볼 수 있어요.",
       "11/15(일)은 LAPOSTA 2027 FC 선행과 서울 팬미팅 굿즈 사후 통판 마감일이 겹쳐요.")
k += p("※2026년 11월 12일 기준 정보예요.", "11/20(금)·21(토) 편성표는 아직 나오지 않아 공식 발표로 알 수 있는 범위만 실었어요.",
       "방송 내용·시간은 바뀔 수 있으니 공식 사이트에서 확인해 주세요.")
k += h2("KO1KEYZ 일정 한눈에 보기(11/15~21)")
k += T.table(["일시", "프로그램·일정"], [
    ["11/15(일)23:59", "'LAPOSTA 2027' FC 회원 선행 접수 마감"],
    ["11/15(일)23:59", "서울 팬미팅 굿즈 사후 통판(LAPONE STORE) 마감"],
    ["11/17(화)22:00~23:00", "엠온! '엠온! 리퀘스트 아워'(MV)"],
    ["11/19(목)21:00~", "공식 YouTube 'KO1! KO1! KO1KEYZ!'(매주 목요일 업데이트)"],
    ["11/21(토)12:30~", "2026 MAMA AWARDS 레드카펫", True],
    ["11/21(토)15:00~", "2026 MAMA AWARDS 시상식(교세라돔 오사카)", True],
])
k += h2("11/21(토) '2026 MAMA AWARDS' 출연")
k += T.info([("일정", "2026년 11월 21일(토) CHAPTER 2"), ("시간", "레드카펫 12:30~ / 시상식 15:00~"),
             ("장소", "교세라돔 오사카"), ("시청 방법", "Mnet Japan(CS)·Mnet Plus·Mnet Smart+ 생중계")])
k += p("KO1KEYZ는 11월 21일(토) '2026 MAMA AWARDS' CHAPTER 2에 출연해요.",
       "올해 MAMA는 11월 20일(금)·21일(토) 이틀간 교세라돔 오사카에서 열려요.",
       "같은 날에는 LE SSERAFIM, ZEROBASEONE, CORTIS 등이 출연할 예정이에요.")
k += p("레드카펫은 12:30부터 Mnet Plus와 MAMA 공식 YouTube에서도 생중계돼요.",
       "데뷔 2개월도 안 돼 돔 시상식 무대에 서는 만큼, 무대와 의상 모두 기대돼요.")
k += h2("11/15(일) FC 선행·굿즈 사후 통판 마감")
k += p("'LAPOSTA 2027'(2027년 1월 도쿄돔, 2월 교세라돔 오사카) FC 회원 선행은 11월 15일(일) 23:59까지예요.",
       "당락 발표는 11월 26일(목) 20:00 예정이고, 지정석은 15,400엔(세금 포함)이에요.")
k += p("서울 팬미팅 굿즈는 LAPONE STORE에서 11월 15일(일) 23:59까지 사후 통판 중이에요.",
       "7,000엔(세금 포함)마다 선착순으로 솔로 트레이딩 카드(12종 랜덤) 1장을 받을 수 있고, 발송은 12월 말 예정이에요.")
k += h2("MV 방송·YouTube·다음 일정")
k += p("11월 17일(화) 22:00 CS 엠온! '리퀘스트 아워' 방송 예정 곡에 KO1KEYZ가 포함돼 있어요.",
       "공식 YouTube 'KO1! KO1! KO1KEYZ!'는 11월 19일(목) 21:00에 업데이트돼요.")
k += p("MAMA 다음 날인 11월 22일(일)에는 '삿포로 컬렉션 2026 AUTUMN/WINTER'에 출연하고, 12월 14일(월)에는 디지털 싱글 'White Love'가 발매돼요.",
       "11/15~11/19 일본 지상파 편성표에서는 멤버 이름을 찾지 못했어요. 새 출연이 정해지면 추가할게요.")
k += p("지난주 일정은 <a href=\"https://chomoand-1.com/ko/ko1keyz-tv-schedule-1108-1114-kr-15408\">11/8~11/14 방송 일정 정리</a>에서 볼 수 있어요.")
k += h2("정리")
k += T.summary(["11/21(토) 교세라돔 오사카 '2026 MAMA AWARDS' 출연",
                "레드카펫 12:30~, 시상식 15:00~, Mnet Japan·Mnet Plus 생중계",
                "LAPOSTA 2027 FC 선행·굿즈 사후 통판 모두 11/15(일) 23:59 마감",
                "MV 11/17(화) 22:00 엠온!, YouTube 11/19(목) 21:00",
                "11/22(일) 삿포로 컬렉션, 12/14(월) White Love 발매"])
save("ko1keyz_tv_schedule_1115_1121_kr.html", k)

# ---------- EN ----------
e = ""
e += p("KO1KEYZ is now in week 7 since debut.",
       "We checked Japanese TV listings and the official site for November 15-21, 2026.",
       f"The big one this week: <strong>{M}KO1KEYZ performs at the 2026 MAMA AWARDS at Kyocera Dome Osaka on 11/21 (Sat)</span></strong>.")
e += p("The show airs live on Mnet Japan and streams on Mnet Plus, so you can watch from home.",
       "Sunday 11/15 is also the deadline for both the LAPOSTA 2027 fan club presale and the Seoul fan meeting goods mail order.")
e += p("*Information as of November 12, 2026.", "Listings for 11/20-21 are not out yet, so those are based on official announcements.",
       "Times may change, so please check the official sites.")
e += h2("KO1KEYZ Schedule at a Glance (11/15-11/21)")
e += T.table(["Date/Time (JST)", "Program / Event"], [
    ["11/15 (Sun) 23:59", "LAPOSTA 2027 fan club presale deadline"],
    ["11/15 (Sun) 23:59", "Seoul fan meeting goods mail order (LAPONE STORE) deadline"],
    ["11/17 (Tue) 22:00-23:00", "M-ON! Request Hour (MV)"],
    ["11/19 (Thu) 21:00-", "Official YouTube \"KO1! KO1! KO1KEYZ!\" (every Thursday)"],
    ["11/21 (Sat) 12:30-", "2026 MAMA AWARDS red carpet", True],
    ["11/21 (Sat) 15:00-", "2026 MAMA AWARDS ceremony (Kyocera Dome Osaka)", True],
])
e += h2("11/21 (Sat): 2026 MAMA AWARDS")
e += T.info([("Date", "Saturday, November 21, 2026 (CHAPTER 2)"), ("Time", "Red carpet 12:30- / Ceremony 15:00- (JST)"),
             ("Venue", "Kyocera Dome Osaka"), ("How to watch", "Live on Mnet Japan (CS), Mnet Plus and Mnet Smart+")])
e += p("KO1KEYZ will appear on day 2 (CHAPTER 2) of the 2026 MAMA AWARDS, held at Kyocera Dome Osaka on November 20-21.",
       "LE SSERAFIM, ZEROBASEONE and CORTIS are also on the CHAPTER 2 lineup.",
       "The red carpet also streams live on Mnet Plus and the official MAMA YouTube channel.")
e += p("Less than two months after debut, the group takes a dome awards stage.",
       "We will add their nominations and performance details once announced.")
e += h2("11/15 (Sun): Two Deadlines")
e += p("The fan club presale for LAPOSTA 2027 (Tokyo Dome in January, Kyocera Dome Osaka in February 2027) closes on November 15 at 23:59.",
       "Results come out on November 26 (Thu) at 20:00, and reserved seats cost 15,400 yen (tax included).")
e += p("Goods from the Seoul fan meeting are on sale by mail order at LAPONE STORE until November 15 at 23:59.",
       "Every 7,000 yen spent gets you one random solo trading card (12 kinds) while supplies last, with shipping around late December.")
e += h2("MV Airing, YouTube and What's Next")
e += p("M-ON! \"Request Hour\" on 11/17 (Tue) at 22:00 lists KO1KEYZ among the planned songs.",
       "The official YouTube series \"KO1! KO1! KO1KEYZ!\" updates on 11/19 (Thu) at 21:00.")
e += p("The day after MAMA, KO1KEYZ performs at SAPPORO COLLECTION 2026 AUTUMN/WINTER on 11/22 (Sun), and the digital single \"White Love\" drops on 12/14 (Mon).",
       "We found no member names in Japan's terrestrial listings for 11/15-11/19, and will update if new TV appearances are announced.")
e += p("Last week's schedule: <a href=\"https://chomoand-1.com/en/ko1keyz-tv-schedule-1108-1114-en-15409\">KO1KEYZ TV Appearances 11/8-11/14</a>.")
e += h2("Summary")
e += T.summary(["11/21 (Sat): 2026 MAMA AWARDS at Kyocera Dome Osaka",
                "Red carpet 12:30-, ceremony 15:00-, live on Mnet Japan / Mnet Plus",
                "LAPOSTA 2027 presale and Seoul goods mail order both close 11/15 23:59",
                "MV on M-ON! 11/17 22:00, YouTube update 11/19 21:00",
                "SAPPORO COLLECTION 11/22, \"White Love\" out 12/14"])
save("ko1keyz_tv_schedule_1115_1121_en.html", e)
