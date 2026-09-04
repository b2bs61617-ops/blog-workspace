# -*- coding: utf-8 -*-
"""One-off uploader for the KO1KEYZ x Mynavi TGC 2026 A/W live-stream article (JP + KR + EN drafts)."""
import re, json, base64, urllib.request, sys

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip().strip('"')

U = env["WP_KOIKEYS_USERNAME"]; P = env["WP_KOIKEYS_APP_PASSWORD"]; BASE = env["WP_KOIKEYS_URL"]
AUTH = base64.b64encode(f"{U}:{P}".encode()).decode()


def api(path, body=None, method="GET"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Authorization", "Basic " + AUTH)
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload_media(path, filename):
    img = open(path, "rb").read()
    req = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=img, method="POST")
    req.add_header("Authorization", "Basic " + AUTH)
    req.add_header("Content-Type", "image/png")
    req.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    with urllib.request.urlopen(req) as r:
        return json.load(r)["id"]


def inline(md):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", md)


def convert(md_text):
    lines = [l for l in md_text.split("\n") if not l.startswith("# ")]
    text = "\n".join(lines).strip()
    blocks = re.split(r"\n\s*\n", text)
    out = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        if b.startswith("<!-- wp:"):
            out.append(b)
        elif b.startswith("## "):
            out.append(f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{inline(b[3:].strip())}</h2>\n<!-- /wp:heading -->')
        elif b.startswith("### "):
            out.append(f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{inline(b[4:].strip())}</h3>\n<!-- /wp:heading -->')
        elif b.startswith("<figure") or b.startswith("<iframe") or b.startswith("<p "):
            out.append(f"<!-- wp:html -->\n{b}\n<!-- /wp:html -->")
        else:
            out.append(f"<!-- wp:paragraph -->\n<p>{inline(b)}</p>\n<!-- /wp:paragraph -->")
    html = "\n\n".join(out)
    html = re.sub(r"<hr\s*/?>", "", html)
    return html


def para(t):
    return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


# ---------------- JAPANESE ----------------
md = open(REPO + r"\articles\ko1keyz_mynavi_tgc_live_stream.md", encoding="utf-8").read()
JP_CONTENT = convert(md)
JP_TITLE = "KO1KEYZのマイナビTGCは配信で見られる？ABEMA生中継！"
JP_SLUG = "ko1keyz-mynavi-tgc-live-stream"
SNS_JP = ("デビューを控えるKO1KEYZが9月19日(土)開催の「マイナビ TGC 2026 A/W」にアーティスト出演。"
          "会場は横浜アリーナでチケットは完売済みですが、当日はABEMAで無料生中継されるため、"
          "KO1KEYZのステージも自宅から無料で視聴できます。配信の日時・視聴方法・見逃し配信の有無をまとめました。")

IMG = ('<figure class="wp-block-image size-large" style="max-width:480px;margin-left:auto;margin-right:auto;">\n'
       '<img src="https://pbs.twimg.com/media/HOcpjm1bAAAbPrj.jpg?name=orig" alt="{alt}" width="1080" height="1080" '
       'style="max-width:100%;height:auto;" loading="lazy" />\n'
       '<figcaption style="text-align:center;font-size:12px;">{src}:<a href="https://x.com/KO1KEYZofficial/status/2082679120417407398" '
       'target="_blank" rel="noopener">https://x.com/KO1KEYZofficial/status/2082679120417407398</a></figcaption>\n</figure>')

MAP = ('<!-- wp:html -->\n<iframe src="https://maps.google.com/maps?q={q}&t=&z=15&ie=UTF8&iwloc=&output=embed" '
       'width="100%" height="330" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>\n<!-- /wp:html -->')

if "--dump-jp" in sys.argv:
    print(JP_CONTENT)
    sys.exit()

# ---------------- KOREAN ----------------
KR_TITLE = "KO1KEYZ의 마이나비 TGC는 중계로 볼 수 있어? ABEMA 생중계!"
KR_SLUG = JP_SLUG + "-kr"
kr = []
kr.append(para(
    "10월 7일 한일 동시 데뷔를 앞둔 KO1KEYZ(코이키즈)가 2026년 9월 19일(토) 요코하마 아리나에서 열리는 "
    "'마이나비 도쿄 걸즈 컬렉션 2026 A/W(마이나비 TGC 2026 A/W)'에 아티스트로 출연합니다.<br>\n"
    "'현장에 못 가도 볼 수 있는지' 궁금한 분이 많은데, <strong>마이나비 TGC 2026 A/W는 개최 당일 ABEMA에서 무료 생중계되기 때문에 "
    "KO1KEYZ의 무대도 집에서 무료로 시청할 수 있습니다</strong>.<br>\n"
    "이 글에서는 생중계 일시·시청 방법·다시보기 여부부터, 마이나비 TGC가 어떤 이벤트인지, KO1KEYZ 외 출연진, 당일 개최 개요까지 정리했습니다."))
kr.append('<!-- wp:html -->\n<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
    '<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">마이나비 TGC 2026 A/W 기본 정보</p>\n'
    '<table style="border-collapse:collapse;width:100%;">\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:34%;">이벤트명</td><td style="border:1px solid #ccc;padding:8px 12px;">제43회 마이나비 도쿄 걸즈 컬렉션 2026 AUTUMN/WINTER</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">개최일</td><td style="border:1px solid #ccc;padding:8px 12px;">2026년 9월 19일(토)</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">장소</td><td style="border:1px solid #ccc;padding:8px 12px;">요코하마 아리나(가나가와현)</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">KO1KEYZ 출연</td><td style="border:1px solid #ccc;padding:8px 12px;">아티스트로서 스페셜 라이브 선보임</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">생중계</td><td style="border:1px solid #ccc;padding:8px 12px;">ABEMA 무료 생중계(9월 19일 13:10〜21:30 예정)</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">다시보기</td><td style="border:1px solid #ccc;padding:8px 12px;">TGC 공식 LINE VOOM·X·YouTube에서 30분 지연 반복 송출</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">주최</td><td style="border:1px solid #ccc;padding:8px 12px;">W TOKYO</td></tr>\n'
    '</table>\n</div>\n<!-- /wp:html -->')
kr.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
    '<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#8a8378;color:#fff;">이 글에서 알 수 있는 것</p>\n'
    '<ul style="margin:0;padding:14px 18px 14px 34px;background:#f7f6f4;">\n'
    '<li>KO1KEYZ 무대를 중계로 보는 방법</li>\n<li>생중계 일시·요금·다시보기 여부</li>\n<li>마이나비 TGC가 어떤 이벤트인지</li>\n<li>KO1KEYZ 외 출연 아티스트·게스트</li>\n<li>개최일·장소·티켓 등 기본 정보</li>\n</ul>\n</div>\n<!-- /wp:html -->')
kr.append(h2("KO1KEYZ의 마이나비 TGC 출연은 중계로 볼 수 있어?"))
kr.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-left:4px solid #8a8378;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f6f4;">\n'
    '<p style="margin:0;"><strong>중계:</strong> ABEMA(무료 생중계 / \'ABEMA로 리얼타임 TGC\')</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>일시:</strong> 2026년 9월 19일(토) 13:10〜21:30 예정</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>요금:</strong> 무료(회원 가입·결제 없이 시청 가능)</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>다시보기:</strong> TGC 공식 LINE VOOM·X·YouTube에서 13:40경부터 30분 지연 반복 송출</p>\n</div>\n<!-- /wp:html -->')
kr.append(para(
    "마이나비 TGC는 매번 개최 당일 ABEMA에서 전편을 무료 생중계하고 있습니다.<br>\n"
    "2026 A/W도 마찬가지로 9월 19일(토) 13:10부터 ABEMA 무료 생중계가 시작되어 21:30경까지 무대가 전달될 예정입니다.<br>\n"
    "ABEMA는 스마트폰 앱에서도 PC 브라우저에서도 볼 수 있고, 회원 가입이나 티켓 구매 없이 재생할 수 있습니다.<br>\n"
    "현장에 가지 못해도 KO1KEYZ의 스페셜 라이브를 실시간으로 응원할 수 있다는 뜻입니다."))
kr.append(para(
    "실시간으로 못 보는 경우를 위해, TGC 공식 LINE VOOM·X(구 트위터)·YouTube에서는 본편 시작으로부터 약 30분 지연된 반복 생송출이 예정되어 있습니다(13:40경 시작 예정).<br>\n"
    "다만 이것은 '30분 늦춰 같은 중계를 한 번 더 트는' 방식으로, 원하는 때에 앞부분부터 골라 볼 수 있는 영구 다시보기와는 다릅니다.<br>\n"
    "TGC는 출연 시간·출연 순서가 사전에 자세히 공개되지 않는 경우도 많으므로, KO1KEYZ 무대를 확실히 보고 싶다면 13:10 생중계 시작부터 끝까지 보는 편이 안심입니다."))
kr.append(h2("애초에 마이나비 TGC란? KO1KEYZ 출연이 왜 주목받나?"))
kr.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
    '<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">KO1KEYZ(코이키즈)란?</p>\n'
    '<table style="border-collapse:collapse;width:100%;">\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:30%;">그룹명</td><td style="border:1px solid #ccc;padding:8px 12px;">KO1KEYZ(코이키즈)</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">인원</td><td style="border:1px solid #ccc;padding:8px 12px;">12인</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">데뷔일</td><td style="border:1px solid #ccc;padding:8px 12px;">2026년 10월 7일(수) 한일 동시 데뷔</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">유래</td><td style="border:1px solid #ccc;padding:8px 12px;">\'PRODUCE 101 JAPAN 신세계(니치푸 신세계)\'의 최종 데뷔조 12명</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">소속사</td><td style="border:1px solid #ccc;padding:8px 12px;">LAPONE 엔터테인먼트</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">멤버</td><td style="border:1px solid #ccc;padding:8px 12px;">DAIKI·YOSHIKI·SIYOUNG·SHINHAENG·YUKI·ISSA·KEITO·YURA·RYOGA·RYUJI·KOSUKE·TOWA</td></tr>\n'
    '</table>\n</div>\n<!-- /wp:html -->')
kr.append(para(
    "도쿄 걸즈 컬렉션(TGC)은 2005년에 시작된 일본 최대급 패션&음악 축제입니다.<br>\n"
    "'일본의 리얼 클로즈(등신대의 옷)를 세계로 발신한다'는 콘셉트 아래 봄여름·가을겨울 연 2회 개최되며, 인기 모델의 런웨이와 아티스트의 라이브 스테이지가 번갈아 펼쳐집니다.<br>\n"
    "주최는 W TOKYO이며, 2026 A/W는 통산 43회째 개최로 테마는 'NEW GRAVITY'로 발표되었습니다."))
kr.append('<!-- wp:html -->\n' + IMG.format(alt="KO1KEYZ 마이나비 TGC 2026 A/W 출연 결정 고지 비주얼", src="출처") + '\n<!-- /wp:html -->')
kr.append(para(
    "KO1KEYZ에게 마이나비 TGC는 첫 국내 대형 패션 이벤트 출연입니다.<br>\n"
    "출연이 발표된 것은 2026년 7월 30일로, 10월 7일 데뷔보다 앞선 시점의 큰 무대가 됩니다.<br>\n"
    "선배격인 JO1·INI·ME:I도 같은 니치푸 시리즈에서 탄생해 TGC를 비롯한 대형 이벤트에서 존재감을 보여 왔습니다.<br>\n"
    "데뷔 전의 KO1KEYZ가 어떤 퍼포먼스를 보여줄지 기대가 높아지고 있습니다."))
kr.append(h2("언제·어디서? 마이나비 TGC 2026 A/W 개최 개요"))
kr.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-left:4px solid #8a8378;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f6f4;">\n'
    '<p style="margin:0;"><strong>개최일:</strong> 2026년 9월 19일(토)</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>장소:</strong> 요코하마 아리나(가나가와현 요코하마시 고호쿠구 신요코하마 3-10)</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>시간:</strong> 개장 12:00 / 개연 14:00 / 종연 21:00 예정</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>티켓:</strong> 매진(선행 12,000엔·일반 12,500엔 / 기념품 봉투·응원봉 포함)</p>\n</div>\n<!-- /wp:html -->')
kr.append(MAP.format(q="横浜アリーナ"))
kr.append(para(
    "장소인 요코하마 아리나는 JR·지하철 신요코하마역에서 도보 5분 정도 거리의 대형 다목적 아리나입니다.<br>\n"
    "당일은 12:00 개장, 14:00 개연, 21:00 종연 예정이며, ABEMA 무료 생중계(13:10〜)는 개연 전부터 시작됩니다.<br>\n"
    "티켓은 선행이 12,000엔(세금 포함), 일반이 12,500엔(세금 포함)으로 모두 기념품 봉투와 응원봉이 포함됩니다.<br>\n"
    "지정석에 5,000엔을 더하는 업그레이드 티켓도 있었지만, 이 글을 쓰는 시점에 티켓은 이미 매진되었습니다.<br>\n"
    "현장에 가지 못한 사람도 무료 생중계로 무대를 지켜볼 수 있습니다."))
kr.append(h2("KO1KEYZ 외 출연 아티스트·게스트"))
kr.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-left:4px solid #8a8378;border-radius:4px;padding:12px 16px;margin:0 0 16px 0;background:#f7f6f4;">\n'
    '<p style="margin:0;"><strong>아티스트(스페셜 라이브):</strong> AND2BLE／IS:SUE／KO1KEYZ／SWEET STEADY／Hearts2Hearts／FRUITS ZIPPER／모나키</p>\n'
    '<p style="margin:6px 0 0 0;"><strong>게스트:</strong> WATWING(구와야마 류타·스즈키 아키라·다카하시 하야테·후쿠자와 키쿠소라)／DXTEEN 다니구치 다이치 외</p>\n'
    '<p style="margin:6px 0 0 0;"><strong>MC:</strong> 와시미 레이나·미토리즈</p>\n'
    '<p style="margin:6px 0 0 0;"><strong>모델:</strong> 사쿠라자카46·히나타자카46 멤버 외 다수</p>\n</div>\n<!-- /wp:html -->')
kr.append(para(
    "2026 A/W의 아티스트 스테이지에는 KO1KEYZ 외에 FRUITS ZIPPER, IS:SUE, SWEET STEADY, 한국의 Hearts2Hearts 등 화제의 그룹이 이름을 올립니다.<br>\n"
    "게스트로 WATWING 멤버와 DXTEEN의 다니구치 다이치 등도 합류하며, 런웨이에는 사쿠라자카46·히나타자카46 멤버가 다수 등장할 예정입니다.<br>\n"
    "패션뿐 아니라 음악·아이돌 면에서도 볼거리가 많은 라인업입니다."))
kr.append(h2("시청 시 포인트"))
kr.append('<!-- wp:html -->\n<div style="border:2px solid #8a8378;border-radius:8px;background:#f7f6f4;padding:1em 1.25em;margin:0 0 16px 0;">\n<p style="margin:0;">\n'
    '&#10003; ABEMA 무료 생중계는 9월 19일(토) 13:10 시작, 시청은 무료(회원 가입·결제 불필요)<br>\n'
    '&#10003; 출연 시간·출연 순서는 사전에 자세히 공개되지 않는 경우가 많으므로, 처음부터 끝까지 보는 것이 확실<br>\n'
    '&#10003; 다시보기용 반복 송출은 TGC 공식 LINE VOOM·X·YouTube에서 30분 지연<br>\n'
    '&#10003; 감상을 올릴 때의 해시태그는 \'#マイナビTGC\' \'#ABEMAでリアタイTGC\'\n</p>\n</div>\n<!-- /wp:html -->')
kr.append(h2("정리"))
kr.append('<!-- wp:html -->\n<div style="border:2px solid #8a8378;border-radius:8px;background:#f7f6f4;padding:1em 1.25em;margin:0 0 16px 0;">\n<p style="margin:0;">\n'
    '&#10003; KO1KEYZ는 9월 19일(토) 열리는 \'마이나비 TGC 2026 A/W\'에 아티스트로 출연<br>\n'
    '&#10003; 장소는 요코하마 아리나, 티켓은 이미 매진<br>\n'
    '&#10003; 당일은 ABEMA 무료 생중계(13:10〜21:30 예정), KO1KEYZ 무대도 집에서 무료 시청 가능<br>\n'
    '&#10003; 다시보기는 TGC 공식 LINE VOOM·X·YouTube에서 30분 지연 반복<br>\n'
    '&#10003; 데뷔(10월 7일) 전으로는 첫 국내 대형 패션 이벤트 출연\n</p>\n</div>\n<!-- /wp:html -->')
kr.append(para(
    "데뷔 전에 이 정도 규모의 무대에 서는 모습을 무료 생중계로 실시간으로 볼 수 있다는 건 반가운 일입니다.<br>\n"
    "당일은 '#マイナビTGC'를 따라가며 KO1KEYZ의 첫 런웨이를 다 함께 응원하고 싶네요!"))
kr.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-left:4px solid #8a8378;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f6f4;">\n'
    '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">KO1KEYZ 데뷔 관련 글</p>\n<ul style="margin:0;padding-left:1.3em;">\n'
    '<li><a href="https://chomoand-1.com/ko/what-is-ko1keyzs-future-schedu">KO1KEYZ의 8월〜10월 데뷔까지 스케줄을 정리한 글</a></li>\n'
    '<li><a href="https://chomoand-1.com/ko/when-will-ko1keyzs-debut-singl">데뷔 싱글 『KO1KEYZ』의 발매일·수록곡·특전을 정리한 글</a></li>\n'
    '<li><a href="https://chomoand-1.com/ko/where-to-buy-ko1keyz-korean-cd">KO1KEYZ 한국반 CD 구매 방법·특전·주의점을 정리한 글</a></li>\n</ul>\n</div>\n<!-- /wp:html -->')
KR_CONTENT = "\n\n".join(kr)
SNS_KR = ("데뷔를 앞둔 KO1KEYZ가 9월 19일(토) 열리는 '마이나비 TGC 2026 A/W'에 아티스트로 출연합니다. "
          "장소는 요코하마 아리나로 티켓은 매진됐지만, 당일 ABEMA에서 무료 생중계되어 KO1KEYZ 무대도 집에서 무료로 볼 수 있습니다. "
          "생중계 일시·시청 방법·다시보기 여부를 정리했습니다.")

# ---------------- ENGLISH ----------------
EN_TITLE = "Can You Watch KO1KEYZ at Mynavi TGC 2026 A/W? Free on ABEMA!"
EN_SLUG = JP_SLUG + "-en"
en = []
en.append(para(
    "Ahead of their October 7 simultaneous Japan/Korea debut, KO1KEYZ will perform as an artist at &#8220;Mynavi Tokyo Girls Collection 2026 A/W (Mynavi TGC 2026 A/W),&#8221; "
    "held at Yokohama Arena on Saturday, September 19, 2026.<br>\n"
    "Wondering whether you can watch it without being at the venue? <strong>Mynavi TGC 2026 A/W is streamed live and free on ABEMA on the day, "
    "so you can watch KO1KEYZ's stage from home at no cost</strong>.<br>\n"
    "This article covers the stream's date and time, how to watch, and whether there is a catch-up option, plus what Mynavi TGC actually is, the rest of the lineup, and the event details."))
en.append('<!-- wp:html -->\n<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
    '<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">Mynavi TGC 2026 A/W: key facts</p>\n'
    '<table style="border-collapse:collapse;width:100%;">\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:34%;">Event</td><td style="border:1px solid #ccc;padding:8px 12px;">The 43rd Mynavi Tokyo Girls Collection 2026 AUTUMN/WINTER</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Date</td><td style="border:1px solid #ccc;padding:8px 12px;">Saturday, September 19, 2026</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Venue</td><td style="border:1px solid #ccc;padding:8px 12px;">Yokohama Arena (Kanagawa)</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">KO1KEYZ</td><td style="border:1px solid #ccc;padding:8px 12px;">Performing a special live set as an artist</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Live stream</td><td style="border:1px solid #ccc;padding:8px 12px;">Free live stream on ABEMA (Sep 19, 13:10&#8211;21:30 JST, planned)</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Catch-up</td><td style="border:1px solid #ccc;padding:8px 12px;">30-minute delayed re-stream on TGC&#8217;s official LINE VOOM, X and YouTube</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Organizer</td><td style="border:1px solid #ccc;padding:8px 12px;">W TOKYO</td></tr>\n'
    '</table>\n</div>\n<!-- /wp:html -->')
en.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
    '<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#8a8378;color:#fff;">What this article covers</p>\n'
    '<ul style="margin:0;padding:14px 18px 14px 34px;background:#f7f6f4;">\n'
    '<li>How to watch KO1KEYZ&#8217;s stage via the stream</li>\n<li>The stream&#8217;s date, time, price and catch-up options</li>\n<li>What Mynavi TGC is</li>\n<li>The other artists and guests</li>\n<li>Date, venue, tickets and other basics</li>\n</ul>\n</div>\n<!-- /wp:html -->')
en.append(h2("Can you watch KO1KEYZ at Mynavi TGC via the stream?"))
en.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-left:4px solid #8a8378;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f6f4;">\n'
    '<p style="margin:0;"><strong>Stream:</strong> ABEMA (free live stream / &#8220;Watch TGC live on ABEMA&#8221;)</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>When:</strong> Saturday, September 19, 2026, 13:10&#8211;21:30 JST (planned)</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>Price:</strong> Free (no sign-up or payment required)</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>Catch-up:</strong> 30-minute delayed re-stream on TGC&#8217;s official LINE VOOM, X and YouTube from around 13:40</p>\n</div>\n<!-- /wp:html -->')
en.append(para(
    "Every edition of Mynavi TGC is streamed in full, for free, on ABEMA on the day of the event.<br>\n"
    "2026 A/W is the same: the free ABEMA live stream starts at 13:10 JST on Saturday, September 19, and is scheduled to run until around 21:30.<br>\n"
    "You can watch ABEMA on the smartphone app or in a PC browser, and no account or ticket purchase is needed to press play.<br>\n"
    "In other words, even if you can&#8217;t get to the venue, you can cheer KO1KEYZ&#8217;s special live set in real time."))
en.append(para(
    "If you can&#8217;t watch live, there is a fallback: TGC&#8217;s official LINE VOOM, X (formerly Twitter) and YouTube are set to run a repeat live stream about 30 minutes behind the main broadcast (starting around 13:40).<br>\n"
    "That is a &#8220;same stream, shifted 30 minutes&#8221; format, though &#8211; not a permanent archive you can scrub back through whenever you like.<br>\n"
    "TGC often doesn&#8217;t publish a detailed running order in advance, so if you want to be sure to catch KO1KEYZ, it&#8217;s safest to watch from the 13:10 start."))
en.append(h2("What is Mynavi TGC, and why is KO1KEYZ&#8217;s appearance notable?"))
en.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
    '<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">Who are KO1KEYZ?</p>\n'
    '<table style="border-collapse:collapse;width:100%;">\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:30%;">Group</td><td style="border:1px solid #ccc;padding:8px 12px;">KO1KEYZ</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Members</td><td style="border:1px solid #ccc;padding:8px 12px;">12</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Debut</td><td style="border:1px solid #ccc;padding:8px 12px;">October 7, 2026 (simultaneous Japan/Korea debut)</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Origin</td><td style="border:1px solid #ccc;padding:8px 12px;">The final debut lineup of 12 from &#8220;PRODUCE 101 JAPAN THE NEW WORLD&#8221;</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Agency</td><td style="border:1px solid #ccc;padding:8px 12px;">LAPONE Entertainment</td></tr>\n'
    '<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Members</td><td style="border:1px solid #ccc;padding:8px 12px;">DAIKI, YOSHIKI, SIYOUNG, SHINHAENG, YUKI, ISSA, KEITO, YURA, RYOGA, RYUJI, KOSUKE, TOWA</td></tr>\n'
    '</table>\n</div>\n<!-- /wp:html -->')
en.append(para(
    "Tokyo Girls Collection (TGC) is one of Japan&#8217;s largest fashion and music festivals, first held in 2005.<br>\n"
    "Built around the idea of showing Japan&#8217;s &#8220;real clothes&#8221; (everyday, wearable fashion) to the world, it runs twice a year &#8211; spring/summer and autumn/winter &#8211; alternating model runways with artist live stages.<br>\n"
    "It is organized by W TOKYO, and 2026 A/W is the 43rd edition, held under the theme &#8220;NEW GRAVITY.&#8221;"))
en.append('<!-- wp:html -->\n' + IMG.format(alt="KO1KEYZ Mynavi TGC 2026 A/W appearance announcement visual", src="Source") + '\n<!-- /wp:html -->')
en.append(para(
    "For KO1KEYZ, Mynavi TGC is their first appearance at a major domestic fashion event.<br>\n"
    "The appearance was announced on July 30, 2026, making it a big stage that comes before their October 7 debut.<br>\n"
    "Their seniors JO1, INI and ME:I also came out of the same PRODUCE 101 JAPAN series and have made their mark at TGC and other large events.<br>\n"
    "Anticipation is building over what a pre-debut KO1KEYZ will bring to the stage."))
en.append(h2("When and where? Mynavi TGC 2026 A/W event details"))
en.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-left:4px solid #8a8378;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f6f4;">\n'
    '<p style="margin:0;"><strong>Date:</strong> Saturday, September 19, 2026</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>Venue:</strong> Yokohama Arena (3-10 Shin-Yokohama, Kohoku-ku, Yokohama, Kanagawa)</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>Times:</strong> Doors 12:00 / Start 14:00 / End 21:00 (planned)</p>\n'
    '<p style="margin:4px 0 0 0;"><strong>Tickets:</strong> Sold out (advance 12,000 yen / general 12,500 yen; includes gift bag and penlight)</p>\n</div>\n<!-- /wp:html -->')
en.append(MAP.format(q="横浜アリーナ"))
en.append(para(
    "The venue, Yokohama Arena, is a large multi-purpose arena about a five-minute walk from Shin-Yokohama Station (JR and subway).<br>\n"
    "On the day, doors open at 12:00, the show starts at 14:00, and it is scheduled to end at 21:00; the free ABEMA live stream (from 13:10) begins before the show starts.<br>\n"
    "Tickets were 12,000 yen (tax incl.) in advance and 12,500 yen (tax incl.) general, both including a gift bag and a penlight.<br>\n"
    "There was also an upgrade ticket adding 5,000 yen to a reserved seat, but tickets are already sold out as of this writing.<br>\n"
    "Anyone who couldn&#8217;t attend in person can still watch the stage on the free live stream."))
en.append(h2("The rest of the lineup: artists and guests"))
en.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-left:4px solid #8a8378;border-radius:4px;padding:12px 16px;margin:0 0 16px 0;background:#f7f6f4;">\n'
    '<p style="margin:0;"><strong>Artists (special live):</strong> AND2BLE / IS:SUE / KO1KEYZ / SWEET STEADY / Hearts2Hearts / FRUITS ZIPPER / Monaki</p>\n'
    '<p style="margin:6px 0 0 0;"><strong>Guests:</strong> WATWING (Ryota Kuwayama, Akira Suzuki, Hayate Takahashi, Kikusora Fukuzawa) / Taichi Taniguchi of DXTEEN, and more</p>\n'
    '<p style="margin:6px 0 0 0;"><strong>MC:</strong> Reina Washimi and Mitorizu</p>\n'
    '<p style="margin:6px 0 0 0;"><strong>Models:</strong> Members of Sakurazaka46 and Hinatazaka46, and many more</p>\n</div>\n<!-- /wp:html -->')
en.append(para(
    "Alongside KO1KEYZ, the 2026 A/W artist stage features buzzy groups such as FRUITS ZIPPER, IS:SUE, SWEET STEADY and Korea&#8217;s Hearts2Hearts.<br>\n"
    "Guests include members of WATWING and Taichi Taniguchi of DXTEEN, while the runway is set to feature many members of Sakurazaka46 and Hinatazaka46.<br>\n"
    "It&#8217;s a lineup with plenty to enjoy on the music and idol side as well as the fashion."))
en.append(h2("Tips for watching"))
en.append('<!-- wp:html -->\n<div style="border:2px solid #8a8378;border-radius:8px;background:#f7f6f4;padding:1em 1.25em;margin:0 0 16px 0;">\n<p style="margin:0;">\n'
    '&#10003; The free ABEMA live stream starts at 13:10 JST on Saturday, September 19; viewing is free (no sign-up or payment)<br>\n'
    '&#10003; A detailed running order usually isn&#8217;t released in advance, so watching from the start is the safe bet<br>\n'
    '&#10003; The catch-up repeat runs 30 minutes behind on TGC&#8217;s official LINE VOOM, X and YouTube<br>\n'
    '&#10003; Hashtags for posting: #マイナビTGC and #ABEMAでリアタイTGC\n</p>\n</div>\n<!-- /wp:html -->')
en.append(h2("Summary"))
en.append('<!-- wp:html -->\n<div style="border:2px solid #8a8378;border-radius:8px;background:#f7f6f4;padding:1em 1.25em;margin:0 0 16px 0;">\n<p style="margin:0;">\n'
    '&#10003; KO1KEYZ perform as an artist at &#8220;Mynavi TGC 2026 A/W&#8221; on Saturday, September 19<br>\n'
    '&#10003; The venue is Yokohama Arena, and tickets are already sold out<br>\n'
    '&#10003; It is streamed live and free on ABEMA on the day (13:10&#8211;21:30 JST, planned), so KO1KEYZ&#8217;s stage can be watched from home for free<br>\n'
    '&#10003; The catch-up is a 30-minute delayed repeat on TGC&#8217;s official LINE VOOM, X and YouTube<br>\n'
    '&#10003; It is their first major domestic fashion event, coming before their October 7 debut\n</p>\n</div>\n<!-- /wp:html -->')
en.append(para(
    "Being able to watch them take a stage this big before they&#8217;ve even debuted &#8211; live and for free &#8211; is a real treat.<br>\n"
    "On the day, follow #マイナビTGC and let&#8217;s all cheer on KO1KEYZ&#8217;s first runway together!"))
en.append('<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-left:4px solid #8a8378;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f6f4;">\n'
    '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">More on KO1KEYZ&#8217;s debut</p>\n<ul style="margin:0;padding-left:1.3em;">\n'
    '<li><a href="https://chomoand-1.com/en/what-is-ko1keyzs-future-schedu">A rundown of KO1KEYZ&#8217;s schedule from August to the October debut</a></li>\n'
    '<li><a href="https://chomoand-1.com/en/when-will-ko1keyzs-debut-singl">The debut single &#8220;KO1KEYZ&#8221;: release date, track list and bonuses</a></li>\n'
    '<li><a href="https://chomoand-1.com/en/where-to-buy-ko1keyz-korean-cd">How to buy the KO1KEYZ Korean CD: bonuses and things to watch for</a></li>\n</ul>\n</div>\n<!-- /wp:html -->')
EN_CONTENT = "\n\n".join(en)
SNS_EN = ("Ahead of their debut, KO1KEYZ perform at &#8220;Mynavi TGC 2026 A/W&#8221; on Saturday, September 19. "
          "The venue is Yokohama Arena and tickets are sold out, but the show streams live and free on ABEMA that day, "
          "so KO1KEYZ&#8217;s stage can be watched from home for free. Here are the stream time, how to watch, and catch-up options.")

if "--dump-kr" in sys.argv:
    print(KR_CONTENT); sys.exit()
if "--dump-en" in sys.argv:
    print(EN_CONTENT); sys.exit()

# ---------------- UPLOAD ----------------
jp = api("/wp-json/wp/v2/posts", {
    "title": JP_TITLE, "slug": JP_SLUG, "content": JP_CONTENT, "status": "draft",
    "categories": [66, 62], "author": 2,
    "meta": {"jetpack_publicize_message": SNS_JP},
}, "POST")
JP_ID = jp["id"]
print("JP draft id:", JP_ID, "| preview:", BASE + "/?p=" + str(JP_ID))

jp_media = upload_media(REPO + r"\images\ko1keyz_mynavi_tgc_live_stream_eyecatch.png", "ko1keyz_mynavi_tgc_live_stream_eyecatch.png")
api("/wp-json/wp/v2/posts/" + str(JP_ID), {"featured_media": jp_media, "status": "draft"}, "POST")
print("JP eyecatch media id:", jp_media)

kr_media = upload_media(REPO + r"\images\ko1keyz_mynavi_tgc_live_stream_eyecatch_kr.png", "ko1keyz_mynavi_tgc_live_stream_eyecatch_kr.png")
kr = api("/wp-json/wp/v2/posts", {
    "title": KR_TITLE, "slug": KR_SLUG, "content": KR_CONTENT, "status": "draft",
    "categories": [66, 62], "author": 2, "featured_media": kr_media,
    "lang": "ko", "translations": {"ja": JP_ID},
    "meta": {"jetpack_publicize_message": SNS_KR},
}, "POST")
KR_ID = kr["id"]
print("KR draft id:", KR_ID, "| link:", kr.get("link"), "| kr media:", kr_media)

en = api("/wp-json/wp/v2/posts", {
    "title": EN_TITLE, "slug": EN_SLUG, "content": EN_CONTENT, "status": "draft",
    "categories": [66, 62], "author": 2, "featured_media": jp_media,
    "lang": "en", "translations": {"ja": JP_ID},
    "meta": {"jetpack_publicize_message": SNS_EN},
}, "POST")
EN_ID = en["id"]
print("EN draft id:", EN_ID, "| link:", en.get("link"))

for pid in (JP_ID, KR_ID, EN_ID):
    chk = api(f"/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content,slug", method="GET")
    print(f"  post {pid} slug={chk['slug']} content.raw length:", len(chk["content"]["raw"]))
