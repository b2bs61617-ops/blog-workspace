# -*- coding: utf-8 -*-
"""2026-11-07: KO1KEYZ DAIKI-team Korea vlog shops article (JP 12714 / KR 12965 / EN 12966).
- Soul Button: add closure notice (reported Nov 2026, no official announcement)
- Butter tteok: likely bought at Soul Button (taken from its bag right after leaving; menu has 버터떡 2,000won)
- Condensed milk: SIYOUNG said "always dip", SHINHAENG "not really" (DAIKI was the one asking)
Usage: python _edit_1107_soulbutton_closed.py [--apply]
"""
import sys, json, base64, urllib.request

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"')
BASE = env["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f'{env["WP_KOIKEYS_USERNAME"]}:{env["WP_KOIKEYS_APP_PASSWORD"]}'.encode()).decode()

TD_L = '<tr><td style="background:#e7e1d4;font-weight:bold;color:#4a4640;border:1px solid #d3cfc4;padding:8px 11px;vertical-align:top;white-space:nowrap;">'
TD_R = '</td><td style="border:1px solid #d3cfc4;padding:8px 11px;vertical-align:top;">'
RED = '<span style="color:#c0392b;font-weight:bold;">'


def notice(title, body):
    return ('<!-- wp:html -->\n<div style="border:2px solid #c0392b;border-radius:6px;padding:12px 16px;margin:0 0 16px 0;background:#fdf1ef;">\n'
            f'<p style="margin:0 0 6px 0;font-weight:bold;color:#c0392b;">{title}</p>\n'
            f'<p style="margin:0;">{body}</p>\n</div>\n<!-- /wp:html -->\n\n')


EDITS = {
    12714: [
        ("<li>屋台で買ったバター餅・クマのストローなど</li>", "<li>バター餅(Soul Buttonで購入とみられる)・クマのストローなど</li>"),
        ("<li>ドリンクを頼んだカフェ「Soul Button」</li>", "<li>ドリンクを頼んだカフェ「Soul Button」と閉店の情報</li>"),
        ("ドバイチョコ系クッキー／バター餅／クマのストロー</td>", "ドバイチョコ系クッキー／クマのストロー</td>"),
        ("(12:00〜22:00・月曜休)</td>", "(12:00〜22:00・月曜休)<br>" + RED + "※2026年11月 閉店の情報あり</span></td>"),
        ("抹茶クリーム／抹茶キャラメル／ローズミルクティー</td></tr>", "抹茶クリーム／抹茶キャラメル／ローズミルクティー／バター餅</td></tr>"),
        ("弘大の屋台で食べた「バター餅」とクマのストロー</h2>", "食べ歩きの「バター餅」とクマのストロー</h2>"),
        ("<strong>店：</strong>弘大の屋台・露店(名称のテロップなし)", "<strong>店：</strong>バター餅はSoul Button(後述)で買ったとみられる／ストローは店名のテロップなし"),
        ("「ドバイクッキーの次に来ている」流行りのスイーツで、屋台で買ったものは", "「ドバイクッキーの次に来ている」流行りのスイーツで、3人が買ったものは"),
        ("DAIKIは練乳につける派、SHINHAENGはつけない派でした。<br>",
         "DAIKIさんの「練乳をつけますか？」という質問に、SIYOUNGさんは「俺は絶対つける」、SHINHAENGさんは「あんまり」と答えていました。<br>\n"
         "このバター餅は、3人がSoul Buttonを出てすぐにお店の袋から取り出していて、Soul Buttonのメニューにもバター餅(버터떡・2,000ウォン)があるので、Soul Buttonで買ったものとみられます。<br>"),
        ("(2)ドリンクを頼んだカフェ「Soul Button」</h2>\n<!-- /wp:heading -->\n\n",
         "(2)ドリンクを頼んだカフェ「Soul Button」</h2>\n<!-- /wp:heading -->\n\n"
         + notice("【2026年11月追記】閉店の情報があります",
                  "2026年11月、現地の店舗が閉まっていて、閉店したという情報が出ています(お店からの正式な発表は確認できていません)。<br>行く前にNAVER地図やカカオマップで、営業しているか確認してください。")),
        ("<strong>頼んだもの：</strong>抹茶クリーム／抹茶キャラメル／ローズ(薔薇)ミルクティー<br>",
         "<strong>頼んだもの：</strong>抹茶クリーム／抹茶キャラメル／ローズ(薔薇)ミルクティー／バター餅(とみられる)<br>"),
        ('background:#f4f1ea;">月曜</td></tr>',
         'background:#f4f1ea;">月曜</td></tr>\n' + TD_L + "営業状況" + TD_R + RED + "2026年11月 閉店の情報あり</span>(正式な発表は未確認)</td></tr>"),
        ("&#10003; 屋台＝ドバイチョコ系クッキー、バター餅(バタートック)、クマのストロー<br>",
         "&#10003; 食べ歩き＝ドバイチョコ系クッキー、クマのストロー<br>"),
        ("&#10003; (2)Soul Button＝抹茶クリーム／抹茶キャラメル／ローズミルクティー<br>",
         "&#10003; (2)Soul Button＝抹茶クリーム／抹茶キャラメル／ローズミルクティー＋バター餅(※2026年11月 閉店の情報あり)<br>"),
    ],
    12965: [
        ("<li>노점에서 산 버터떡·곰 빨대 등</li>", "<li>버터떡(Soul Button에서 산 것으로 추정)·곰 빨대 등</li>"),
        ("<li>음료를 주문한 카페 'Soul Button'</li>", "<li>음료를 주문한 카페 'Soul Button'과 폐업 정보</li>"),
        ("두바이 초콜릿 계열 쿠키／버터떡／곰 빨대</td>", "두바이 초콜릿 계열 쿠키／곰 빨대</td>"),
        ("(12:00~22:00·월요일 휴무)</td>", "(12:00~22:00·월요일 휴무)<br>" + RED + "※2026년 11월 폐업 정보 있음</span></td>"),
        ("말차 크림／말차 카라멜／로즈 밀크티</td></tr>", "말차 크림／말차 카라멜／로즈 밀크티／버터떡</td></tr>"),
        ("홍대 노점에서 먹은 '버터떡'과 곰 빨대</h2>", "먹방 투어의 '버터떡'과 곰 빨대</h2>"),
        ("<strong>가게: </strong>홍대 노점(가게명 자막 없음)", "<strong>가게: </strong>버터떡은 Soul Button(뒤에서 소개)에서 산 것으로 추정／빨대는 가게명 자막 없음"),
        ("노점에서 산 것은 겉이", "3명이 산 것은 겉이"),
        ("DAIKI는 연유에 찍는 파, SHINHAENG은 안 찍는 파였습니다.<br>",
         "DAIKI가 '연유 찍어요? 안 찍어요?'라고 묻자 SIYOUNG은 '나는 무조건 찍는다', SHINHAENG은 '별로'라고 답했습니다.<br>\n"
         "이 버터떡은 3명이 Soul Button에서 나오자마자 가게 봉투에서 꺼냈고, Soul Button 메뉴에도 버터떡(2,000원)이 있어서 Soul Button에서 산 것으로 보입니다.<br>"),
        ("(2) 음료를 주문한 카페 'Soul Button'</h2>\n<!-- /wp:heading -->\n\n",
         "(2) 음료를 주문한 카페 'Soul Button'</h2>\n<!-- /wp:heading -->\n\n"
         + notice("【2026년 11월 추가】폐업 정보가 있습니다",
                  "2026년 11월, 매장이 닫혀 있어 폐업했다는 정보가 나오고 있습니다(가게의 공식 발표는 확인되지 않았습니다).<br>방문 전에 네이버 지도나 카카오맵에서 영업 중인지 꼭 확인하세요.")),
        ("<strong>주문한 것: </strong>말차 크림／말차 카라멜／로즈(장미) 밀크티<br>",
         "<strong>주문한 것: </strong>말차 크림／말차 카라멜／로즈(장미) 밀크티／버터떡(추정)<br>"),
        ('background:#f4f1ea;">월요일</td></tr>',
         'background:#f4f1ea;">월요일</td></tr>\n' + TD_L + "영업 상황" + TD_R + RED + "2026년 11월 폐업 정보 있음</span>(공식 발표 미확인)</td></tr>"),
        ("&#10003; 노점＝두바이 초콜릿 계열 쿠키, 버터떡(버터 톡), 곰 빨대<br>",
         "&#10003; 먹방 투어＝두바이 초콜릿 계열 쿠키, 곰 빨대<br>"),
        ("&#10003; (2) Soul Button＝말차 크림／말차 카라멜／로즈 밀크티<br>",
         "&#10003; (2) Soul Button＝말차 크림／말차 카라멜／로즈 밀크티＋버터떡(※2026년 11월 폐업 정보 있음)<br>"),
    ],
    12966: [
        ("<li>The butter tteok, bear straw and more they bought at street stalls</li>",
         "<li>The butter tteok (likely from Soul Button), bear straw and more</li>"),
        ('<li>The cafe "Soul Button" where they got drinks</li>', '<li>The cafe "Soul Button" where they got drinks, and news of its closure</li>'),
        ("Dubai-chocolate-style cookie / butter tteok / bear straw</td>", "Dubai-chocolate-style cookie / bear straw</td>"),
        ("(12:00&ndash;22:00, closed Mondays)</td>", "(12:00&ndash;22:00, closed Mondays)<br>" + RED + "*Reported closed (Nov 2026)</span></td>"),
        ("Matcha cream / matcha caramel / rose milk tea</td></tr>", "Matcha cream / matcha caramel / rose milk tea / butter tteok</td></tr>"),
        ('The "butter tteok" and bear straw from Hongdae street stalls</h2>', 'The "butter tteok" and bear straw from their food walk</h2>'),
        ("<strong>Shop: </strong>Hongdae street stalls (no name caption)",
         "<strong>Shop: </strong>The butter tteok was likely bought at Soul Button (see below); no name caption for the straw"),
        ("The one they bought from a stall was hard", "The one they bought was hard"),
        ("DAIKI dips his in condensed milk; SHINHAENG doesn't.<br>",
         "When DAIKI asked whether they dip it in condensed milk, SIYOUNG said \"I always do\" and SHINHAENG said \"not really\".<br>\n"
         "They took the butter tteok out of a shop bag right after leaving Soul Button, and Soul Button's menu lists butter tteok (버터떡, 2,000 won), so it was most likely bought there.<br>"),
        ('(2) The cafe "Soul Button", where they got drinks</h2>\n<!-- /wp:heading -->\n\n',
         '(2) The cafe "Soul Button", where they got drinks</h2>\n<!-- /wp:heading -->\n\n'
         + notice("[Update, Nov 2026] Soul Button is reported to have closed",
                  "In November 2026 the shop was found shut, and it is reported to have closed (we have not found an official announcement from the shop).<br>Before you go, check on Naver Map or KakaoMap whether it is open.")),
        ("<strong>What they ordered: </strong>Matcha cream / matcha caramel / rose milk tea<br>",
         "<strong>What they ordered: </strong>Matcha cream / matcha caramel / rose milk tea / butter tteok (likely)<br>"),
        ('background:#f4f1ea;">Mondays</td></tr>',
         'background:#f4f1ea;">Mondays</td></tr>\n' + TD_L + "Status" + TD_R + RED + "Reported closed (Nov 2026)</span> (no official announcement found)</td></tr>"),
        ("&#10003; Street stalls = Dubai-chocolate-style cookie, butter tteok (butter tok), bear straw<br>",
         "&#10003; Food walk = Dubai-chocolate-style cookie, bear straw<br>"),
        ("&#10003; (2) Soul Button = matcha cream / matcha caramel / rose milk tea<br>",
         "&#10003; (2) Soul Button = matcha cream / matcha caramel / rose milk tea + butter tteok (*reported closed, Nov 2026)<br>"),
    ],
}


def api(path, body=None, method="GET"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Authorization", "Basic " + AUTH)
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


apply = "--apply" in sys.argv
for pid, edits in EDITS.items():
    raw = open(REPO + rf"\backups\{pid}_before_1107_soulbutton_closed.html", encoding="utf-8").read()
    live = api(f"/wp-json/wp/v2/posts/{pid}?context=edit")["content"]["raw"]
    assert live == raw, f"{pid}: live content changed since backup"
    for old, new in edits:
        n = raw.count(old)
        assert n == 1, (pid, n, old[:60])
        raw = raw.replace(old, new)
    print(pid, "ok", len(edits), "edits")
    if apply:
        r = api(f"/wp-json/wp/v2/posts/{pid}", {"content": raw}, "POST")
        print("  updated", r["status"], r["modified"], r["link"])
