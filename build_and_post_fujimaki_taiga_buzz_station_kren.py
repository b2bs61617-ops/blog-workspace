# -*- coding: utf-8 -*-
import json, base64, os, re, subprocess, sys
from pathlib import Path

import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
WP_USER = ENV["WP_KOIKEYS_USERNAME"]
WP_PASS = ENV["WP_KOIKEYS_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

JP_POST_ID = int((ROOT / "tmp_fujimaki_taiga_buzz_station_postid.txt").read_text(encoding="utf-8").strip())
JP_SLUG = (ROOT / "tmp_fujimaki_taiga_buzz_station_slug.txt").read_text(encoding="utf-8").strip()
JP_EYECATCH_MEDIA_ID = int((ROOT / "tmp_fujimaki_taiga_buzz_station_eyecatch_mediaid.txt").read_text(encoding="utf-8").strip())

ACCENT = "#8a8378"
BORDER = "#ddd9d3"
BG = "#f7f6f4"
TDBG = "#f3f1ee"

PRTIMES_URL = "https://prtimes.jp/main/html/rd/p/000000533.000141380.html"
ZENSE_URL = "https://chomoand-1.com/produce101japanshinsekai_zense-2748"
MATOME8_URL = "https://chomoand-1.com/produce101japanshinsekai_8matome-8577"
RECIPE_URL = "https://chomoand-1.com/produce101japan_ryourirecipi-8604"


def p(text_sentences):
    return f"<!-- wp:paragraph -->\n<p>" + "<br>\n".join(text_sentences) + "</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def infotable(ttl, rows):
    tds = "\n".join(
        f'<tr><td style="background:{TDBG};border:1px solid {BORDER};padding:8px 12px;width:32%;">{k}</td>'
        f'<td style="border:1px solid {BORDER};padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{ttl}</p>
<table style="border-collapse:collapse;width:100%;">
{tds}
</table>
</div>''')


def whatbox(ttl, items):
    lis = "\n".join(f'<li style="margin:0 0 8px 0;">{t}</li>' for t in items[:-1])
    lis += f'\n<li style="margin:0;">{items[-1]}</li>'
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def mk(cls, text):
    return f'<span class="swl-marker {cls}">{text}</span>'


def mkstrong(cls, text):
    return f'<strong><span class="swl-marker {cls}" style="font-size:1.15em;">{text}</span></strong>'


def get_slug_en(title):
    slug = re.sub(r"[^a-z0-9\s-]", "", title.lower())
    slug = re.sub(r"\s+", "-", slug.strip())
    return re.sub(r"-+", "-", slug)[:30].rstrip("-")


def post_lang(title, content, slug, lang, summary, featured_media):
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "categories": [4],
        "author": 2,
        "lang": lang,
        "translations": {"ja": JP_POST_ID},
        "featured_media": featured_media,
        "meta": {"jetpack_publicize_message": summary},
    }
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    return r.json()


# =========================== KOREAN ===========================
kr_title = "프듀 신세계 후지마키 타이가, BUZZ STATION 게스트 출연! 방송일은?"

kr = []
kr.append(p([
    "『PRODUCE 101 JAPAN 신세계(일프 신세계)』에 출연했던 후지마키 타이가(藤牧大雅) 씨가, 요이코·하마구치 마사루 씨가 진행을 맡는 라디오 프로그램 「하마구치 마사루의 BUZZ STATION」에 게스트 출연하는 것이 발표되었습니다.",
    "출연 회차는 <strong>2026년 9월 18일(금) 18:00〜18:50</strong>이며, 시부야의 공개 스튜디오에서 진행되는 생방송입니다.",
    "이 기사에서는 방송 일시와 청취 방법, 「BUZZ STATION」이 어떤 프로그램인지, 그리고 후지마키 타이가 씨의 지금까지의 경력과 최근 팬미팅 정보까지 정리합니다.",
]))
kr.append(infotable("후지마키 타이가 게스트 출연 회차 기본 정보", [
    ("프로그램명", "하마구치 마사루의 BUZZ STATION"),
    ("방송 일시", "2026년 9월 18일(금) 18:00〜18:50"),
    ("방송국", "Shibuya Cross-FM(시부야 크로스FM) 93.8MHz"),
    ("진행자", "하마구치 마사루(요이코)"),
    ("형식", "시부야 공개 스튜디오 생방송"),
]))
kr.append(h2("후지마키 타이가의 「BUZZ STATION」 게스트 출연이 결정"))
kr.append(p([
    "주식회사 BUZZ GROUP의 보도자료를 통해, 후지마키 타이가 씨가 「하마구치 마사루의 BUZZ STATION」 9월 방송 회차에 게스트 출연하는 것이 밝혀졌습니다.",
    "발표에서는 「니지프로2·보이플래닛2·일프 신세계를 달려온 후지마키 타이가가 등장」이라고 소개되어 있으며, 여러 오디션 프로그램을 경험해 온 실력파로서의 출연입니다.",
    "프로그램에서는 <strong>지금까지의 오디션에서 쌓은 경험, 아티스트로서의 현재 위치, 그리고 앞으로의 도전</strong>에 대해 본인의 말로 이야기할 예정이라고 합니다.",
]))
kr.append(p([
    "일프 신세계 방송 종료 후 SNS와 라이브 방송을 중심으로 활동해 온 후지마키 타이가 씨에게, 라디오 프로그램 게스트 출연은 귀중한 기회입니다.",
    "오디션에서의 퍼포먼스뿐 아니라, 꾸밈없는 토크와 앞으로의 목표를 차분히 들을 수 있다는 점은 팬에게 놓칠 수 없는 부분입니다.",
    f'발표의 자세한 내용은 <a href="{PRTIMES_URL}" target="_blank" rel="noopener">PR TIMES 보도자료(일본어)</a>에서 확인할 수 있습니다.',
]))
kr.append(h2("「BUZZ STATION」은 어떤 프로그램일까?"))
kr.append(p([
    "「하마구치 마사루의 BUZZ STATION」은 2026년 4월 3일에 시작된 라디오 프로그램입니다.",
    "요이코의 하마구치 마사루 씨가 진행을 맡으며, 「라디오를 듣는다」에서 「라디오를 체험한다」로 이어지는 새로운 엔터테인먼트를 콘셉트로 내세우고 있습니다.",
    "방송은 매달 첫째·셋째 금요일 18:00〜18:50이며, Shibuya Cross-FM의 공개 스튜디오에서 생방송으로 진행됩니다.",
]))
kr.append(minibox('''<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">하마구치 마사루의 BUZZ STATION이란?</p>
<p style="margin:0;">Shibuya Cross-FM(93.8MHz)에서 방송 중인 라디오 프로그램.<br>
매달 첫째·셋째 금요일 18:00〜18:50에, 시부야 공개 스튜디오에서 하마구치 마사루(요이코)가 진행자로서 생방송으로 전한다.<br>
출연을 희망하는 아티스트를 상시 모집하고 있으며, 지금까지 UNIVER23, NeoStella 등의 그룹이 게스트로 출연했다.</p>'''))
kr.append(p([
    "공개 스튜디오 생방송이기 때문에, 스튜디오 현장을 보러 가면 하마구치 마사루 씨나 게스트와 같은 공간에서 라디오 녹음의 현장감을 체감할 수 있는 것도 특징입니다.",
    "후지마키 타이가 씨의 출연 회차도 같은 형식으로 방송될 것으로 보입니다.",
]))
kr.append(h2("방송은 언제? 청취 방법은?"))
kr.append(p([
    "후지마키 타이가 씨의 게스트 출연 회차는 " + mkstrong("mark_yellow", "2026년 9월 18일(금) 18:00〜18:50") + " 방송입니다.",
    "Shibuya Cross-FM은 시부야·진난 지역을 중심으로 커버하는 미니 FM 방송국으로, 주파수는 93.8MHz입니다.",
    "전파가 닿는 곳은 스튜디오 주변뿐이므로, 지역 밖에 있는 사람은 인터넷 방송으로 듣게 됩니다.",
]))
kr.append(whatbox("BUZZ STATION 청취 방법", [
    "시부야·진난 주변: FM 라디오를 93.8MHz에 맞춘다",
    "지역 밖: Shibuya Cross-FM 공식 사이트(shibuyacrossfm.jp)의 영상 포함 스트리밍으로 시청",
    "radiko(라지코)에는 대응하지 않으므로 앱으로는 들을 수 없다",
    "놓친 경우, YouTube 아카이브 영상으로 다시 볼 수 있는 경우가 있다",
]))
kr.append(p([
    "방송 직전이나 당일에는 프로그램 공식 X·Shibuya Cross-FM 공식 사이트에서 최신 방송 링크나 진행 시간이 안내되므로, 그쪽을 확인해 두면 확실합니다.",
    "생방송이므로 실시간으로 들으면 프로그램에 보낸 메시지가 읽힐 가능성도 있습니다.",
]))
kr.append(h2("후지마키 타이가는 어떤 사람?"))
kr.append(p([
    "후지마키 타이가(藤牧大雅) 씨는 수많은 오디션 프로그램에 계속 도전해 온 연습생입니다.",
    "JYP 연습생으로 약 4년 반을 보낸 뒤, 일본과 한국의 서바이벌 프로그램에 잇달아 참가해 왔습니다.",
]))
kr.append(infotable("후지마키 타이가 프로필", [
    ("이름", "후지마키 타이가(藤牧大雅)"),
    ("생년월일", "2005년 5월 17일"),
    ("출신지", "일본 도쿄도"),
    ("신장", "181cm"),
    ("특기", "작사, 랩, 댄스"),
    ("취미", "기타, 웨이트 트레이닝"),
]))
kr.append(p([
    "오디션 경력은 매우 풍부합니다.",
    "『Nizi Project Season 2』(니지프로2)에서는 한국 합숙까지 진출했고, 이어진 『BOYS II PLANET』(보이플래닛2)에서는 최종 순위 65위라는 결과였습니다.",
    "그리고 2026년 방송된 『PRODUCE 101 JAPAN 신세계』에서는 " + mk("mark_yellow", "최종 순위 42위·A클래스") + "까지 올라갔으나, 8화에서 아쉽게 탈락. 데뷔 그룹 「KO1KEYZ(코이키즈)」 합류는 이루어지지 않았습니다.",
    f'일프 신세계에서의 활약은 <a href="{MATOME8_URL}" target="_blank" rel="noopener">8화 정리 기사(일본어)</a>나 <a href="{ZENSE_URL}" target="_blank" rel="noopener">연습생 전생 일람(일본어)</a>에서도 다루고 있습니다.',
]))
kr.append(p([
    "셀 수 없이 많은 오디션을 거치고도 도전을 이어가는 자세 때문에, 팬들 사이에서는 「불굴의 도전자」라고 불립니다.",
    "랩과 작사 실력은 높은 평가를 받고 있으며, 한국어·중국어도 구사하는 멀티한 면모도 지니고 있습니다.",
]))
kr.append(h2("9월 3일에는 자비·무료 팬미팅도"))
kr.append(p([
    "라디오 출연에 앞서, 후지마키 타이가 씨는 2026년 9월 3일(목) 18:30부터 도쿄·유라쿠초의 휴릭홀 도쿄에서 첫 팬미팅을 개최합니다.",
    "주목받는 점은, 이 이벤트가 " + mkstrong("mark_yellow", "본인의 저금으로 자비 개최·입장 무료") + "라는 것입니다.",
    "니지프로2 탈락 후부터 보이플래닛2에 나가기까지의 기간에 아르바이트로 모은 돈을 사용해, 대관료 등의 경비를 직접 계산한 뒤 기획했다고 밝혔습니다.",
]))
kr.append(p([
    "퍼포먼스 구성까지 혼자 계획을 세우고, 가족의 허락도 받은 뒤 개최한다고 합니다.",
    "티켓 예약 접수는 이미 시작되었으며, 본인의 인스타그램(@taiga17517) 프로필란의 링크에서 신청할 수 있습니다.",
    "팬미팅에서 직접 만나고, 그 2주 뒤에는 라디오에서 토크를 듣는 흐름을 즐길 수 있는 9월이 될 것 같습니다.",
]))
kr.append(h2("정리"))
kr.append(wphtml(f'''<div style="border:2px solid {ACCENT};border-radius:8px;background:rgba(138,131,120,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; 후지마키 타이가가 「하마구치 마사루의 BUZZ STATION」 9월 방송 회차에 게스트 출연<br>
&#10003; 방송은 2026년 9월 18일(금) 18:00〜18:50, Shibuya Cross-FM(93.8MHz)<br>
&#10003; 지역 밖은 공식 사이트의 영상 포함 방송으로 시청, radiko는 미대응<br>
&#10003; 프로그램에서는 오디션에서 쌓은 경험과 앞으로의 도전을 이야기할 예정<br>
&#10003; 9월 3일에는 휴릭홀 도쿄에서 자비·무료 팬미팅도 개최
</p>
</div>'''))
kr.append(p([
    "일프 신세계에서 데뷔는 놓쳤지만, 후지마키 타이가 씨의 활동은 오히려 여기서부터 본격화될 것 같습니다.",
    "라디오에서 어떤 말이 나올지, 방송일을 기대하며 기다리고 싶네요!",
]))
kr.append(wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">일프 신세계 관련 기사</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{ZENSE_URL}" target="_blank" rel="noopener">【일프 신세계】연습생 전생 일람! 전 K-POP 아이돌이나 경력을 철저 조사!(일본어)</a></li>
<li><a href="{MATOME8_URL}" target="_blank" rel="noopener">【일프 신세계】8화 정리｜콘셉트 평가·KCON·2차 순위 발표식 결과!(일본어)</a></li>
<li><a href="{RECIPE_URL}" target="_blank" rel="noopener">【일프 신세계】연습생이 만든 요리 레시피 정리! 의외의 요리 남자도 판명!(일본어)</a></li>
</ul>
</div>'''))

kr_content = "\n\n".join(kr)
print("KR content length:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", kr_content)))
print("KR title length:", len(kr_title))

# KR eyecatch (Black Han Sans / --lang kr)
KR_EYE_PATH = ROOT / "images" / "fujimaki_taiga_buzz_station_eyecatch_kr.png"
subprocess.run([
    sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
    "--top", "일프 신세계 후지마키 타이가",
    "--main", "BUZZ STATION",
    "--bottom", "라디오에 게스트 출연!",
    "--lang", "kr",
    "--out", str(KR_EYE_PATH),
    "--seed", str(JP_POST_ID),
], check=True)
mr = requests.post(
    f"{WP_URL}/wp-json/wp/v2/media",
    headers={**HEADERS_AUTH, "Content-Type": "image/png",
             "Content-Disposition": 'attachment; filename="fujimaki_taiga_buzz_station_eyecatch_kr.png"'},
    data=KR_EYE_PATH.read_bytes(),
)
mr.raise_for_status()
KR_EYE_ID = mr.json()["id"]
print("KR_EYECATCH_MEDIA_ID", KR_EYE_ID)

kr_summary = ("일프 신세계에 출연했던 후지마키 타이가가 요이코·하마구치 마사루의 라디오 프로그램 "
              "「하마구치 마사루의 BUZZ STATION」에 게스트 출연. 방송은 2026년 9월 18일(금) 18시부터 "
              "Shibuya Cross-FM. 청취 방법과 경력, 9월 3일 자비·무료 팬미팅 정보도 정리했습니다.")
kr_post = post_lang(kr_title, kr_content, JP_SLUG + "-kr", "ko", kr_summary, KR_EYE_ID)
print("KR_POST_ID", kr_post["id"])
print("KR_SLUG", kr_post["slug"])
print("KR_PREVIEW", f"{WP_URL}/?p={kr_post['id']}")
(ROOT / "tmp_fujimaki_taiga_buzz_station_kr_postid.txt").write_text(str(kr_post["id"]), encoding="utf-8")


# =========================== ENGLISH ===========================
en_title = "Taiga Fujimaki to Guest on Radio Show BUZZ STATION: Date and How to Listen"

en = []
en.append(p([
    "Taiga Fujimaki, who appeared on <em>PRODUCE 101 JAPAN The Newcomers</em> (Nippro Shinsekai), has been announced as a guest on the radio show \"Masaru Hamaguchi's BUZZ STATION,\" hosted by Masaru Hamaguchi of the comedy duo Yoiko.",
    "His episode airs on <strong>Friday, September 18, 2026, from 18:00 to 18:50</strong>, broadcast live from an open studio in Shibuya.",
    "This article covers the broadcast date and how to listen, what kind of program BUZZ STATION is, and Fujimaki's career so far, plus details on his upcoming fan meeting.",
]))
en.append(infotable("Fujimaki's Guest Episode at a Glance", [
    ("Program", "Masaru Hamaguchi's BUZZ STATION"),
    ("Air date", "Fri, September 18, 2026, 18:00-18:50 (JST)"),
    ("Station", "Shibuya Cross-FM, 93.8MHz"),
    ("Host", "Masaru Hamaguchi (Yoiko)"),
    ("Format", "Live from an open studio in Shibuya"),
]))
en.append(h2("Fujimaki's BUZZ STATION Guest Appearance Is Confirmed"))
en.append(p([
    "A press release from BUZZ GROUP Inc. revealed that Taiga Fujimaki will guest on the September episode of \"Masaru Hamaguchi's BUZZ STATION.\"",
    "The announcement introduces him as \"Taiga Fujimaki, who powered through Nizi Project 2, Boys II Planet, and Nippro Shinsekai,\" appearing as a skilled performer with a long audition-show resume.",
    "On the show he is expected to talk in his own words about <strong>the experience he gained through auditions, where he stands now as an artist, and the challenges ahead</strong>.",
]))
en.append(p([
    "Since Nippro Shinsekai wrapped, Fujimaki has been active mainly through social media and live streams, so a radio guest spot is a valuable opportunity.",
    "Beyond his audition performances, fans get to hear his unguarded talk and his goals for the future.",
    f'Full details are in the <a href="{PRTIMES_URL}" target="_blank" rel="noopener">PR TIMES press release (in Japanese)</a>.',
]))
en.append(h2("What Is BUZZ STATION?"))
en.append(p([
    "\"Masaru Hamaguchi's BUZZ STATION\" is a radio program that launched on April 3, 2026.",
    "Hosted by Masaru Hamaguchi of Yoiko, it is built around the concept of moving from \"listening to radio\" to \"experiencing radio.\"",
    "It airs on the first and third Friday of each month from 18:00 to 18:50, broadcast live from Shibuya Cross-FM's open studio.",
]))
en.append(minibox('''<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">About Masaru Hamaguchi's BUZZ STATION</p>
<p style="margin:0;">A radio program on Shibuya Cross-FM (93.8MHz).<br>
Aired live from an open studio in Shibuya on the first and third Friday of each month, 18:00-18:50, hosted by Masaru Hamaguchi (Yoiko).<br>
It is always looking for artists to appear, and past guests include groups such as UNIVER23 and NeoStella.</p>'''))
en.append(p([
    "Because it airs live from an open studio, visitors can watch the recording and feel the atmosphere in the same room as Hamaguchi and the guests.",
    "Fujimaki's episode is expected to follow the same format.",
]))
en.append(h2("When Does It Air, and How Can You Listen?"))
en.append(p([
    "Fujimaki's guest episode airs on " + mkstrong("mark_yellow", "Friday, September 18, 2026, 18:00-18:50 (JST)") + ".",
    "Shibuya Cross-FM is a mini-FM station covering mainly the Shibuya and Jinnan area, on 93.8MHz.",
    "The signal only reaches the area around the studio, so listeners elsewhere will need to tune in via internet stream.",
]))
en.append(whatbox("How to Listen to BUZZ STATION", [
    "Around Shibuya/Jinnan: tune an FM radio to 93.8MHz",
    "Outside the area: watch the video-enabled stream on the Shibuya Cross-FM website (shibuyacrossfm.jp)",
    "It is not available on radiko, so you cannot listen through that app",
    "If you miss it, an archive video on YouTube may let you catch up later",
]))
en.append(p([
    "Right before and on the day of the broadcast, the program's official X account and the Shibuya Cross-FM website post the latest stream link and timing, so it is worth checking there.",
    "Since it is live, listening in real time means your message to the show might be read on air.",
]))
en.append(h2("Who Is Taiga Fujimaki?"))
en.append(p([
    "Taiga Fujimaki is a trainee who has kept challenging himself across a long string of audition shows.",
    "After spending about four and a half years as a JYP trainee, he took part in Japanese and Korean survival programs one after another.",
]))
en.append(infotable("Taiga Fujimaki Profile", [
    ("Name", "Taiga Fujimaki"),
    ("Date of birth", "May 17, 2005"),
    ("Hometown", "Tokyo, Japan"),
    ("Height", "181cm"),
    ("Skills", "Songwriting, rap, dance"),
    ("Hobbies", "Guitar, weight training"),
]))
en.append(p([
    "His audition history is extensive.",
    "On <em>Nizi Project Season 2</em> he advanced to the Korea training camp, and on <em>BOYS II PLANET</em> he finished 65th.",
    "On 2026's <em>PRODUCE 101 JAPAN The Newcomers</em>, he climbed to " + mk("mark_yellow", "42nd place in Class A") + " before being eliminated in Episode 8, missing out on the debut group KO1KEYZ.",
    f'His run on the show is also covered in our <a href="{MATOME8_URL}" target="_blank" rel="noopener">Episode 8 recap (in Japanese)</a> and <a href="{ZENSE_URL}" target="_blank" rel="noopener">trainee backgrounds list (in Japanese)</a>.',
]))
en.append(p([
    "Because he keeps going after so many auditions, fans call him \"the unbreakable challenger.\"",
    "His rap and songwriting are highly rated, and he also speaks Korean and Chinese.",
]))
en.append(h2("A Self-Funded, Free Fan Meeting on September 3"))
en.append(p([
    "Ahead of the radio appearance, Fujimaki will hold his first fan meeting on Thursday, September 3, 2026, from 18:30 at Hulic Hall Tokyo in Yurakucho, Tokyo.",
    "What has drawn attention is that the event is " + mkstrong("mark_yellow", "self-funded from his own savings and free to attend") + ".",
    "He used money he earned from a part-time job between his elimination from Nizi Project 2 and his appearance on Boys II Planet, and planned it after calculating the venue and other costs himself.",
]))
en.append(p([
    "He planned everything down to the performance setlist on his own, and went ahead with his family's permission.",
    "Ticket reservations are already open, via the link in the profile section of his Instagram (@taiga17517).",
    "Meeting him in person and then hearing him talk on the radio two weeks later makes for a packed September.",
]))
en.append(h2("Summary"))
en.append(wphtml(f'''<div style="border:2px solid {ACCENT};border-radius:8px;background:rgba(138,131,120,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; Taiga Fujimaki guests on the September episode of "Masaru Hamaguchi's BUZZ STATION"<br>
&#10003; Airs Friday, September 18, 2026, 18:00-18:50 on Shibuya Cross-FM (93.8MHz)<br>
&#10003; Outside the area, watch the video stream on the official site; not on radiko<br>
&#10003; He will talk about the experience gained through auditions and the challenges ahead<br>
&#10003; He also holds a self-funded, free fan meeting at Hulic Hall Tokyo on September 3
</p>
</div>'''))
en.append(p([
    "He missed out on debuting through Nippro Shinsekai, but Fujimaki's career looks set to pick up speed from here.",
    "It will be worth waiting for the broadcast to hear what he has to say.",
]))
en.append(wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">Related articles on Nippro Shinsekai</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{ZENSE_URL}" target="_blank" rel="noopener">Nippro Shinsekai: trainee backgrounds list (in Japanese)</a></li>
<li><a href="{MATOME8_URL}" target="_blank" rel="noopener">Nippro Shinsekai: Episode 8 recap (in Japanese)</a></li>
<li><a href="{RECIPE_URL}" target="_blank" rel="noopener">Nippro Shinsekai: trainee cooking recipes roundup (in Japanese)</a></li>
</ul>
</div>'''))

en_content = "\n\n".join(en)
print("EN content length:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", en_content)))
print("EN title length:", len(en_title))

en_summary = ("Taiga Fujimaki, a former PRODUCE 101 JAPAN The Newcomers contestant, will guest on "
              "Masaru Hamaguchi's radio show BUZZ STATION on Friday, September 18, 2026, at 18:00 JST "
              "on Shibuya Cross-FM. Includes how to listen, his career, and his free September 3 fan meeting.")
en_post = post_lang(en_title, en_content, JP_SLUG + "-en", "en", en_summary, JP_EYECATCH_MEDIA_ID)
print("EN_POST_ID", en_post["id"])
print("EN_SLUG", en_post["slug"])
print("EN_PREVIEW", f"{WP_URL}/?p={en_post['id']}")
(ROOT / "tmp_fujimaki_taiga_buzz_station_en_postid.txt").write_text(str(en_post["id"]), encoding="utf-8")
