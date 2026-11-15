# -*- coding: utf-8 -*-
"""KO1KEYZ MAMA2026記事(JP ID15899)の韓国語版・英語版の下書き(blog-upload STEP6/7)。2026-11-15。

    python tools/_upload_ko1keyz_mama2026_i18n_1115.py           # KR/ENを下書き投稿(控え: articles/ko1keyz_mama2026_1115_i18n_posted.json)
    python tools/_upload_ko1keyz_mama2026_i18n_1115.py --update  # 下書きの本文を上書き
このMacではai_hubの外部AIが使えなかったので、マツが訳した本文をここに書いている。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

JP_ID = 15899
MEDIA = 15900
BASE_SLUG = "ko1keyz-mama-awards-2026"
OFFICIAL = "https://ko1keyz.com"
MAMA = "https://mnetjp.com/mama/2026/"
BC = "https://bestcalendar.jp/press/162209"
STATE = blogkit.ARTICLES / "ko1keyz_mama2026_1115_i18n_posted.json"

b = blogkit.Blocks("#c2410c", "#f2c9a8", "#fff7ef")
L = b.link


def kr():
    o = ""
    o += b.p("KO1KEYZ(코이키즈)가 " + b.mark("11월 21일(토) '2026 MAMA AWARDS'") + "에 출연합니다.",
             "장소는 교세라 돔 오사카이며, 시상식은 오후 3시, 레드카펫은 낮 12시 30분부터 시작합니다(모두 일본 시간).",
             "Mnet Plus 등에서 생중계로 볼 수 있습니다.")
    o += b.p("이 글에서는 출연 날짜와 시간, 시청 방법, 같은 날 출연하는 아티스트를 정리했습니다.",
             "※2026년 11월 15일 기준 정보입니다.")
    o += b.wakaru(["MAMA는 어떤 시상식?", "KO1KEYZ 출연은 언제? 몇 시부터?", "TV・스마트폰으로 보는 방법",
                   "같은 날 출연하는 아티스트", "MAMA 전후 KO1KEYZ 일정"])
    o += b.h2("MAMA는 어떤 시상식?")
    o += b.p("MAMA AWARDS는 한국 CJ ENM이 매년 여는 아시아 최대급 음악 시상식입니다.",
             "K-POP 아티스트가 많이 모이고, 1년 동안 활약한 가수와 그룹에게 상을 줍니다.",
             "시상식 중간에 아티스트들의 무대를 많이 볼 수 있는 것도 특징입니다.")
    o += b.p("2026년에는 " + b.mark("11월 20일(금)・21일(토) 이틀간, 교세라 돔 오사카") + "에서 열립니다.",
             "첫째 날은 'CHAPTER 1', 둘째 날은 'CHAPTER 2'라고 부릅니다.")
    o += b.h2("KO1KEYZ 출연은 언제? 몇 시부터?")
    o += b.mini(("이벤트", "2026 MAMA AWARDS"), ("날짜", "2026년 11월 21일(토)(둘째 날・CHAPTER 2)"),
                ("장소", "교세라 돔 오사카"), ("레드카펫", "12:30부터(일본 시간)"), ("시상식", "15:00부터(일본 시간)"))
    o += b.p("KO1KEYZ 공식 사이트 스케줄에는 11월 21일(토)에 '2026 MAMA AWARDS'라고 적혀 있습니다.",
             "둘째 날 시상식은 오후 3시부터, 그 전 낮 12시 30분부터는 레드카펫이 있습니다.",
             "일본과 한국은 시차가 없어서 한국에서도 같은 시간입니다.")
    o += b.p("출처: " + L(OFFICIAL, "KO1KEYZ 공식 사이트(SCHEDULE)") + " / " + L(BC, "베스트 캘린더(MAMA 시간)"))
    o += b.h3("출연 순서는 알 수 있을까?")
    o += b.p("시상식 중 몇 시쯤 KO1KEYZ가 등장하는지는 발표되지 않았습니다.",
             "시상식은 오랜 시간 이어지기 때문에, 놓치고 싶지 않다면 처음부터 보는 것이 안심입니다.",
             "레드카펫에서 멤버들이 어떤 의상으로 등장할지도 주목입니다.")
    o += b.h3("어떤 상 후보에 올랐을까?")
    o += b.p("11월 15일 기준으로, KO1KEYZ가 어떤 상의 후보인지, 어떤 곡을 선보일지는 확인되지 않았습니다.",
             "발표가 나오면 이 글에 추가하겠습니다.")
    o += b.h2("TV・스마트폰으로 보는 방법")
    o += b.p("현장에 가지 못하는 분도 집에서 생중계로 볼 수 있습니다.")
    o += b.table(("보는 방법", "어디서", "포인트"),
                 [("Mnet Plus", "스마트폰・PC", "전 세계 생중계"),
                  ("Mnet Japan", "TV(일본 CS 방송)", "일본에서 계약 필요"),
                  ("Mnet Smart+", "스마트폰・PC", "일본용 스트리밍")])
    o += b.p("한국이나 해외에서 본다면 전 세계에 생중계하는 'Mnet Plus'가 가장 편합니다.",
             "앱을 미리 설치하고 가입해 두면 당일에 바로 볼 수 있습니다.",
             "자세한 시청 안내는 " + L(MAMA, "MAMA 일본 공식 사이트") + "에 있습니다.")
    o += b.h2("같은 날 출연하는 아티스트")
    o += b.p("둘째 날 'CHAPTER 2'에는 인기 그룹이 많이 출연합니다.",
             "1차로 발표된 출연자는 다음과 같습니다(날짜 구분은 발표 당시 기준).")
    o += b.table(("날짜", "출연자(1차 발표)"),
                 [("11/20(금) CHAPTER 1", "ALPHA DRIVE ONE, BABYMONSTER, ENHYPEN, ILLIT, INI, NCT WISH, RESCENE"),
                  ("11/21(토) CHAPTER 2", "CORTIS, KiiiKiii, LE SSERAFIM, NAYEON(TWICE), ZEROBASEONE")])
    o += b.p("출연자는 이후에도 추가로 발표되고 있습니다.",
             "KO1KEYZ는 데뷔 약 2개월 만에 돔 시상식 무대에 서게 됩니다.")
    o += b.h2("MAMA 전후 KO1KEYZ 일정")
    o += b.table(("일시", "일정"),
                 [("11/21(토) 9:00", "Mnet 'KCON LA 2026 × M COUNTDOWN' 자막판 #1(일본 CS)"),
                  ("11/21(토) 12:30", "MAMA 레드카펫"), ("11/21(토) 15:00", "MAMA 시상식(둘째 날)"),
                  ("11/22(일)", "SAPPORO COLLECTION 2026 AUTUMN/WINTER"),
                  ("12/14(월)", "디지털 싱글 'White Love' 발매")])
    o += b.p("MAMA 다음 날인 11월 22일(일)에는 삿포로의 'SAPPORO COLLECTION'에 출연합니다.",
             "오사카에서 삿포로까지, 이틀 연속 무대입니다.")
    o += b.h3("오사카 회장 근처 이벤트")
    o += b.p("MAMA에 맞춰 11월 9일부터 21일까지 'MAMA FAN FESTA'도 열리고 있습니다.",
             "11월 19일부터는 난바히로바에 팬 라운지와 포토존이 생깁니다.")
    o += b.h2("정리")
    o += b.checks(["KO1KEYZ는 11월 21일(토) '2026 MAMA AWARDS' 둘째 날에 출연",
                   "장소는 교세라 돔 오사카. 레드카펫 12:30〜, 시상식 15:00〜",
                   "해외에서는 'Mnet Plus' 생중계가 편리",
                   "출연 시간・후보・무대 곡은 아직 미발표",
                   "다음 날 11월 22일(일)은 SAPPORO COLLECTION 출연"])
    o += b.p("데뷔한 해에 아시아 최대급 시상식 무대에 서는 KO1KEYZ.",
             "12명이 돔에서 어떤 퍼포먼스를 보여줄지 벌써 기대됩니다.")
    return o


def en():
    o = ""
    o += b.p("KO1KEYZ will perform at the " + b.mark("2026 MAMA AWARDS on Saturday, November 21") + ".",
             "The venue is Kyocera Dome Osaka. The red carpet starts at 12:30 and the ceremony at 15:00 (Japan time).",
             "You can watch it live on Mnet Plus and other services.")
    o += b.p("This guide covers the date and time, how to watch, and who else performs that day.",
             "*Information as of November 15, 2026.")
    o += b.wakaru(["What are the MAMA AWARDS?", "When do KO1KEYZ appear?", "How to watch on TV or online",
                   "Other artists on the same day", "KO1KEYZ's schedule around MAMA"])
    o += b.h2("What are the MAMA AWARDS?")
    o += b.p("The MAMA AWARDS are one of Asia's biggest music award shows, held every year by CJ ENM of Korea.",
             "Many K-pop artists take part, and awards go to the singers and groups who stood out that year.",
             "The show is also known for its many live stages.")
    o += b.p("In 2026 the show runs for " + b.mark("two days, November 20 and 21, at Kyocera Dome Osaka") + ".",
             "Day 1 is called CHAPTER 1 and Day 2 is CHAPTER 2.")
    o += b.h2("When do KO1KEYZ appear?")
    o += b.mini(("Event", "2026 MAMA AWARDS"), ("Date", "Saturday, November 21, 2026 (Day 2, CHAPTER 2)"),
                ("Venue", "Kyocera Dome Osaka"), ("Red carpet", "from 12:30 JST"), ("Ceremony", "from 15:00 JST"))
    o += b.p("The schedule on the KO1KEYZ official site lists \"2026 MAMA AWARDS\" on November 21.",
             "On Day 2, the red carpet begins at 12:30 and the ceremony at 15:00 Japan time (UTC+9).")
    o += b.p("Sources: " + L(OFFICIAL, "KO1KEYZ official site (SCHEDULE)") + " / " + L(BC, "Best Calendar (MAMA times)"))
    o += b.h3("Is their stage time known?")
    o += b.p("The time KO1KEYZ will appear during the ceremony has not been announced.",
             "The show runs for several hours, so watching from the start is the safest way not to miss them.",
             "Keep an eye on the red carpet too, to see the members' outfits.")
    o += b.h3("Are they nominated?")
    o += b.p("As of November 15, we could not confirm any nominations or which song they will perform.",
             "We will update this post when it is announced.")
    o += b.h2("How to watch on TV or online")
    o += b.table(("Service", "Where", "Notes"),
                 [("Mnet Plus", "Phone / PC", "Worldwide live stream"),
                  ("Mnet Japan", "TV (CS in Japan)", "Subscription in Japan"),
                  ("Mnet Smart+", "Phone / PC", "Streaming for Japan")])
    o += b.p("Outside Japan, Mnet Plus is the easiest option because it streams worldwide.",
             "Install the app and sign up in advance so you can start watching right away.",
             "Viewing details are on the " + L(MAMA, "MAMA official site for Japan") + ".")
    o += b.h2("Other artists on the same day")
    o += b.p("Many popular groups perform on Day 2. These are the artists from the first lineup announcement",
             "(day split as announced at the time).")
    o += b.table(("Date", "First lineup"),
                 [("Nov 20 (Fri) CHAPTER 1", "ALPHA DRIVE ONE, BABYMONSTER, ENHYPEN, ILLIT, INI, NCT WISH, RESCENE"),
                  ("Nov 21 (Sat) CHAPTER 2", "CORTIS, KiiiKiii, LE SSERAFIM, NAYEON (TWICE), ZEROBASEONE")])
    o += b.p("More performers have been added since then.",
             "KO1KEYZ will stand on a dome award-show stage only about two months after their debut.")
    o += b.h2("KO1KEYZ's schedule around MAMA")
    o += b.table(("Date / time (JST)", "Schedule"),
                 [("Nov 21 (Sat) 9:00", "Mnet \"KCON LA 2026 × M COUNTDOWN\" subtitled #1 (CS, Japan)"),
                  ("Nov 21 (Sat) 12:30", "MAMA red carpet"), ("Nov 21 (Sat) 15:00", "MAMA ceremony (Day 2)"),
                  ("Nov 22 (Sun)", "SAPPORO COLLECTION 2026 AUTUMN/WINTER"),
                  ("Dec 14 (Mon)", "Digital single \"White Love\" release")])
    o += b.p("The day after MAMA, on November 22, they appear at SAPPORO COLLECTION in Sapporo.",
             "That makes two stages in a row, from Osaka to Sapporo.")
    o += b.h3("Fan events near the venue")
    o += b.p("MAMA FAN FESTA runs from November 9 to 21.",
             "From November 19, a fan lounge and photo zones open at Namba Hiroba in Osaka.")
    o += b.h2("Summary")
    o += b.checks(["KO1KEYZ perform on Day 2 of the 2026 MAMA AWARDS, Saturday, November 21",
                   "Kyocera Dome Osaka. Red carpet from 12:30, ceremony from 15:00 (JST)",
                   "Outside Japan, watch live on Mnet Plus",
                   "Stage time, nominations and song are not announced yet",
                   "On November 22 they appear at SAPPORO COLLECTION"])
    o += b.p("In their debut year, KO1KEYZ take the stage at one of Asia's biggest award shows.",
             "We can't wait to see what the 12 members show us at the dome.")
    return o


JOBS = [
    dict(lang="ko", suffix="-kr", cats=[74, 70], body=kr,
         title="【未】【KO1KEYZ】2026 MAMA 출연은 몇 시? 출연일과 시청 방법 정리!"),
    dict(lang="en", suffix="-en", cats=[110, 112], body=en,
         title="【未】[KO1KEYZ] 2026 MAMA AWARDS: Date, Time & How to Watch"),
]

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    wp = blogkit.WP("ko1keyz")
    author = blogkit.author_for("ko1keyz")
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    for j in JOBS:
        content = j["body"]()
        (blogkit.ARTICLES / "ko1keyz_mama2026_1115_{}.html".format(j["lang"])).write_text(content, encoding="utf-8")
        if j["lang"] in state:
            if "--update" in sys.argv:
                wp.post("/posts/{}".format(state[j["lang"]]), {"title": j["title"], "content": content, "status": "draft"})
                print("更新", j["lang"], state[j["lang"]])
            else:
                print("投稿済み", j["lang"], state[j["lang"]])
            continue
        p = wp.post("/posts", {"title": j["title"], "slug": BASE_SLUG + j["suffix"], "content": content,
                               "status": "draft", "categories": j["cats"], "author": author,
                               "featured_media": MEDIA, "lang": j["lang"]})
        state[j["lang"]] = p["id"]
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        print(j["lang"], p["id"], p["slug"], p["link"])
