# -*- coding: utf-8 -*-
"""KO1KEYZ ブルガリア クリアファイル記事 KR15910/EN15911 を JP15907 の11/16リライトにそろえる(WP本文へ直接パッチ)。

    python tools/_edit_1116_ko1keyz_bulgaria_clearfile_i18n.py          # 確認だけ
    python tools/_edit_1116_ko1keyz_bulgaria_clearfile_i18n.py --apply  # 更新
"""
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
b = blogkit.Blocks("#c2410c", "#f2c9a8", "#fff7ef")
w = blogkit.WP("ko1keyz")

KR_ROWS = [
    ("홋카이도(삿포로)", "ー", "이온・코프삿포로・아크스"),
    ("아오모리(중남부)", "ー", "맥스밸류・이토쿠・메가・유니버스"),
    ("후쿠시마", "ー", "요크베니마루・리온도르"),
    ("니가타(니가타시 히가시구)", "ー", "웰시아・하라신・이온"),
    ("군마", "'대량으로 발견했다'는 목소리", "ー"),
    ("기타칸토", "토리센", "ー"),
    ("사이타마", "ー", "베르크・BIGA・도부스토어"),
    ("가나가와", "소테쓰 로젠", "소테쓰 로젠(없는 매장도)"),
    ("나라", "ー", "이소카와・파켓"),
    ("후쿠오카", "ー", "하로데이・서니・맥스밸류"),
    ("가고시마", "ー", "타이요・A코프"),
    ("오키나와", "ー", "산에이"),
    ("주고쿠・시코쿠", "정보 없음", "정보 없음"),
]
EN_ROWS = [
    ("Hokkaido (Sapporo)", "–", "AEON, Co-op Sapporo, Arcs"),
    ("Aomori (central/south)", "–", "MaxValu, Itoku, Mega, Universe"),
    ("Fukushima", "–", "York-Benimaru, Lion d'or"),
    ("Niigata (Higashi Ward)", "–", "Welcia, Harashin, AEON"),
    ("Gunma", "One fan says they found \"lots\"", "–"),
    ("North Kanto", "Torisen", "–"),
    ("Saitama", "–", "Belc, BIGA, Tobu Store"),
    ("Kanagawa", "Sotetsu Rosen", "Sotetsu Rosen (not every store)"),
    ("Nara", "–", "Isokawa, Packet"),
    ("Fukuoka", "–", "Harowdey, Sunny, MaxValu"),
    ("Kagoshima", "–", "Taiyo, A-Coop"),
    ("Okinawa", "–", "San-A"),
    ("Chugoku / Shikoku", "No info yet", "No info yet"),
]

L = {
    15910: dict(
        intro=(r"<p>다만 메이지의 공식 안내는 아직 나오지 않았습니다\..*?</p>",
               b.p("다만 메이지의 공식 안내는 나오지 않았습니다.",
                   "11월 16일에는 팬이 문의한 결과 '매장별 행사라서 공식 안내 예정은 없다'는 답을 받았다는 내용도 공유됐습니다.",
                   "이 글에서는 지금까지 알려진 조건과 매장 찾는 방법, 전국 목격 정보를 정리했습니다.",
                   "※2026년 11월 16일 기준 정보입니다.").split("\n", 1)[1].rsplit("\n<!-- /wp:paragraph -->", 1)[0]),
        li=("<li>어느 매장에서 받을 수 있어?</li>\n", "<li>어느 매장에서 받을 수 있어?</li>\n<li>전국 목격 정보(11월 16일 기준)</li>\n"),
        official=("11월 15일 기준 아직 없음", "없음(매장별 행사라 안내 예정도 없다고 함)"),
        period=("미발표. 소진 시 종료 가능성", "매장마다 다름. 앞으로 시작하는 매장도, 이미 끝난 매장도 있을 수 있음"),
        sec=("어느 매장에서 받을 수 있어?", "먼저 ONE SHOT"),
        trend=("공식 공지가 나와도 매장 목록은 없을 수 있음", "메이지 공식 X의 안내나 매장 목록은 없음(이번엔 안내 예정 없음)"),
        tips=("메이지의 공식 안내가 나오면 이 글에 추가하겠습니다.", "새로 발견된 매장 정보가 나오면 이 글에 추가하겠습니다."),
        end=("정식 안내가 나와서 원하는 팬 모두에게 닿기를 바랍니다.", "더 많은 매장에 놓여서 원하는 팬 모두에게 닿기를 바랍니다."),
        summary="정리",
    ),
    15911: dict(
        intro=(r"<p>[^<]*official announcement yet\..*?</p>",
               None),
        li=("<li>Which stores have it?</li>\n", "<li>Sightings around Japan (as of Nov 16)</li>\n"),
        official=("None as of November 15", "None (stores run it themselves, and no notice is planned)"),
        period=("Not announced; may end when stock runs out", "Differs by store; some may start later, some may have already ended"),
        sec=("Which stores have it?", "Start by finding stores"),
        trend=("An official notice may not include a store list", "No official notice or store list (none is planned this time)"),
        tips=("We will update this post when Meiji makes an announcement.", "We will update this post as more stores are found."),
        end=("We hope an official notice comes soon so every fan who wants one can get it.",
             "We hope more stores start stocking it so every fan who wants one can get it."),
        summary="Summary",
    ),
}


def section(pid):
    if pid == 15910:
        s = b.h2("어느 매장에서 받을 수 있어?")
        s += b.p("나눠 주는 매장 이름은 공개되지 않았습니다.",
                 "11월 15일 처음 받았다는 목소리는 집 근처 역에 있는 " + b.mark("사철(민영 철도) 계열 슈퍼") + "였습니다.")
        s += b.p("11월 16일에는 팬이 문의한 내용이 X에 공유됐습니다.")
        s += b.checks(["매장 자체 행사라서 " + b.mark("공식 안내 예정은 없음"),
                       "클리어 파일을 놓는 시기는 매장마다 정함",
                       "기간도 매장마다 다름. 같은 체인이라도 같다고는 할 수 없음",
                       "앞으로 시작하는 매장도, 이미 끝난 매장도 있을 수 있음"])
        s += b.p("즉, 메이지가 '이 매장에 있다'는 목록을 낼 가능성은 낮고, 직접 발로 찾아야 할 것 같습니다.",
                 "팬들 사이에서는 " + b.mark("'#KO1KEYZワンショットクリアファイルを探せ'") + " 해시태그로 찾은 매장 정보를 모으는 움직임도 시작됐습니다.")
        s += b.h3("전국 목격 정보(11월 16일 22시 기준)")
        s += b.p("팬들이 모은 전국의 목소리를 보면, 16일 시점에는 " + b.mark("아직 놓지 않은 매장이 더 많은") + " 것 같습니다.")
        s += b.table(("지역", "있었다", "없었다"), KR_ROWS)
        s += b.p("※같은 체인이라도 매장마다 다릅니다. 돌아본 일부 매장의 목소리입니다.")
        s += b.p("가나가와에서는 " + b.mark("소테쓰 로젠") + "에서 찾았다는 목소리가 여러 건 나왔습니다.",
                 "다만 같은 소테쓰 로젠에서도 '없었다'는 목소리가 있어, 매장마다 다르다는 것을 알 수 있습니다.")
        s += b.p("찾은 사람 중에는 '위쪽에 걸려 있어서 처음엔 못 보고 지나쳤다'는 사람도 있었습니다.",
                 "매장에서는 " + b.mark("요구르트 진열대 위쪽까지") + " 꼼꼼히 확인해 보세요.")
        s += b.p("'홋카이도는 늦게 놓일 것 같다', 후쿠오카에서 점원에게 물었더니 '정보조차 들어오지 않았다'고 했다는 목소리도 있었습니다.",
                 "나중에 놓는 매장도 있을 것 같으니, 없었던 매장도 며칠 뒤 다시 가 보는 것을 추천합니다.")
        s += b.h3("노려볼 만한 곳은 큰 슈퍼")
        s += b.p("음료 코너에서 자주 캠페인을 하는 큰 슈퍼가 노려볼 만하다는 이야기가 있습니다.",
                 "도쿄 도심보다 조금 교외의 " + b.mark("이온・세이유・이토요카도") + " 같은 곳이 찾을 가능성이 높다는 목소리도 있습니다.",
                 "다만 16일 시점에는 이온에서도 '없었다'는 목소리가 있어, 같은 체인이라도 매장마다 다른 것 같습니다.")
        return s
    s = b.h2("Which stores have it?")
    s += b.p("Store names have not been made public.",
             "The first fan who got one on November 15 found it at a " + b.mark("railway-run supermarket") + " near their station.")
    s += b.p("On November 16, a fan shared on X what they were told when they asked about it.")
    s += b.checks(["Stores run it themselves, so " + b.mark("no official notice is planned"),
                   "Each store decides when to put the clear files out",
                   "The period also differs by store, even within the same chain",
                   "Some stores may start later, and some may have already finished"])
    s += b.p("So a store list from Meiji is unlikely, and fans will have to search on foot.",
             "Fans have started sharing finds under the hashtag " + b.mark("#KO1KEYZワンショットクリアファイルを探せ") + ".")
    s += b.h3("Sightings around Japan (as of 10 p.m., Nov 16)")
    s += b.p("Reports collected by fans suggest that, as of the 16th, " + b.mark("most stores have not put them out yet") + ".")
    s += b.table(("Area", "Found", "Not found"), EN_ROWS)
    s += b.p("*Results differ by store, even within one chain. These are only the stores fans checked.")
    s += b.p("In Kanagawa, several fans found it at " + b.mark("Sotetsu Rosen") + ".",
             "Others said their Sotetsu Rosen did not have it, so it really depends on the store.")
    s += b.p("One fan missed it at first because it was hanging up high.",
             "Check " + b.mark("all the way up the yogurt shelf") + ".")
    s += b.p("Fans also said Hokkaido may get it later, and a Fukuoka store clerk said they had not even heard about it.",
             "Some stores may put it out later, so it is worth checking again in a few days.")
    s += b.h3("Big supermarkets are your best bet")
    s += b.p("Fans point to large supermarkets that often run drink campaigns.",
             "Suburban " + b.mark("AEON, Seiyu and Ito-Yokado") + " stores may be better bets than ones in central Tokyo.",
             "That said, some AEON stores did not have it on the 16th, so it varies by store.")
    return s


EN_INTRO = ("<p>Meiji has not made an official announcement.<br>\n"
            "On November 16, a fan who asked about it shared that stores run it themselves, so no official notice is planned.<br>\n"
            "This post sums up how to get it, how to find stores, and sightings around Japan.<br>\n"
            "*Information as of November 16, 2026.</p>")

KR_SUM = ["KO1KEYZ×ONE SHOT 오리지널 클리어 파일이 일본 일부 매장에서 배포 중",
          "받은 팬에 따르면 조건은 대상 상품 2개 구매",
          "매장별 행사라서 공식 안내나 매장 목록은 없을 전망",
          "놓는 시기・기간은 매장마다 다름. 앞으로 시작하는 매장도 있음",
          "11월 16일 기준 소테쓰 로젠(가나가와)・토리센(기타칸토) 등에서 찾았다는 목소리",
          "교외의 큰 슈퍼가 노려볼 만함. 진열대 위쪽까지 확인"]
EN_SUM = ["An original KO1KEYZ × ONE SHOT clear file is being given out at some stores in Japan",
          "According to a fan who got one, you need to buy two eligible products",
          "Stores run it themselves, so no official notice or store list is expected",
          "Timing and period differ by store; some stores have not started yet",
          "As of Nov 16, fans found it at Sotetsu Rosen (Kanagawa) and Torisen (North Kanto)",
          "Big suburban supermarkets are the best bet; check the top of the shelf"]


def patch(pid):
    c = L[pid]
    t = w.get_post(pid)["content"]["raw"]
    n0 = len(t)

    def rep(old, new):
        nonlocal t
        if t.count(old) != 1:
            raise SystemExit("{}: 見つからない({}) {}".format(pid, t.count(old), old[:50]))
        t = t.replace(old, new)

    intro_new = EN_INTRO if pid == 15911 else c["intro"][1]
    t, k = re.subn(c["intro"][0], lambda _m: intro_new, t, count=1, flags=re.S)
    if k != 1:
        raise SystemExit("{}: 冒頭が見つからない".format(pid))
    if pid == 15911:
        rep(c["li"][0], c["li"][0] + c["li"][1])
    else:
        rep(*c["li"])
    rep(*c["official"])
    rep(*c["period"])
    i = t.index('<!-- wp:heading -->\n<h2 class="wp-block-heading">{}</h2>'.format(c["sec"][0]))
    j = t.index('<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{}'.format(c["sec"][1]))
    t = t[:i] + section(pid) + t[j:]
    rep(*c["trend"])
    rep(*c["tips"])
    m = re.search(r'(<h2 class="wp-block-heading">{}</h2>\n<!-- /wp:heading -->\n\n)<!-- wp:html -->.*?<!-- /wp:html -->\n\n'.format(c["summary"]), t, re.S)
    t = t[:m.end(1)] + b.checks(KR_SUM if pid == 15910 else EN_SUM) + t[m.end():]
    rep(*c["end"])
    print(pid, n0, "->", len(t))
    if "--apply" in sys.argv:
        w.post("/posts/{}".format(pid), {"content": t})
        got = w.get_post(pid)["content"]["raw"]
        key = "소테쓰 로젠" if pid == 15910 else "Sotetsu Rosen"
        print(pid, "反映OK" if key in got and "#KO1KEYZワンショットクリアファイルを探せ" in got else "反映されてない！")


for pid in (15910, 15911):
    patch(pid)
