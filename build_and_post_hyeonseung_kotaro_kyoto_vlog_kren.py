# -*- coding: utf-8 -*-
"""ユ・ヒョンスン&浅香孝太郎 京都Vlog聖地記事のKR/EN下書き。JP版(build_and_post_hyeonseung_kotaro_kyoto_vlog.py)の後に実行。"""
import json, re, subprocess, sys
from urllib.parse import quote

import requests

from ko1keyz_article_kit import ROOT, WP_URL, HEADERS_AUTH, wphtml, p, h2, a, Ui

IDS_FILE = ROOT / "tmp_hyeonseung_kotaro_kyoto_vlog_ids.json"
ids = json.loads(IDS_FILE.read_text(encoding="utf-8"))
JP_ID, JP_SLUG = ids["jp"], ids["jp_slug"]
VIDEO = "https://www.youtube.com/watch?v=11O16cjVi6c"

ACCENT, BORDER, BG = "#8a8378", "#ddd9d3", "#f7f6f4"
ui = Ui(ACCENT, BORDER, BG, "rgba(138,131,120,0.06)")
media = {k: requests.get(f"{WP_URL}/wp-json/wp/v2/media/{v}", headers=HEADERS_AUTH).json() for k, v in ids["media"].items()}


def img(key, alt, cap):
    m = media[key]
    sizes = m["media_details"].get("sizes", {})
    full, fw, fh = m["source_url"], m["media_details"]["width"], m["media_details"]["height"]
    large = sizes.get("large", {"source_url": full, "width": fw})
    medium = sizes.get("medium", {"source_url": full, "width": fw})
    w = large["width"]
    h = int(w * fh / fw)
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{large["source_url"]}" alt="{alt}" width="{w}" height="{h}"
  style="max-width:100%;height:auto;"
  srcset="{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {w}w, {full} {fw}w"
  sizes="(max-width: {w}px) 100vw, {w}px">
<figcaption style="text-align:center;font-size:12px;">{cap}{VIDEO}</figcaption>
</figure>''')


def gmap(q, z=16):
    return wphtml(f'''<iframe
  src="https://maps.google.com/maps?q={quote(q)}&t=&z={z}&ie=UTF8&iwloc=&output=embed"
  width="100%" height="350" frameborder="0" scrolling="no"
  style="border:0;" loading="lazy">
</iframe>''')


def route_table(header, rows):
    th = "".join(f'<td style="background:{ACCENT};color:#fff;border:1px solid {BORDER};padding:8px 10px;"><strong>{c}</strong></td>' for c in header)
    trs = ""
    for i, r in enumerate(rows):
        bg = "#fff" if i % 2 == 0 else BG
        trs += "<tr>" + "".join(f'<td style="background:{bg};border:1px solid {BORDER};padding:8px 10px;">{c}</td>' for c in r) + "</tr>\n"
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr>{th}</tr>
{trs}</tbody></table></figure>
<!-- /wp:table -->'''


def olbox(title, items):
    lis = "\n".join(f'<li style="margin:0 0 8px 0;">{i}</li>' for i in items[:-1]) + f'\n<li style="margin:0;">{items[-1]}</li>'
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{title}</p>
<ol style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ol>
</div>''')


def related(title, links):
    lis = "\n".join(f'<li><a href="{u}">{t}</a></li>' for u, t in links)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


def marker(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def post_lang(title, content, slug, lang, summary, featured, key):
    payload = {"title": title, "content": content, "status": "draft", "categories": [4], "author": 2,
               "lang": lang, "featured_media": featured, "meta": {"jetpack_publicize_message": summary}}
    if ids.get(key):
        url = f"{WP_URL}/wp-json/wp/v2/posts/{ids[key]}"
    else:
        url = f"{WP_URL}/wp-json/wp/v2/posts"
        payload["slug"] = slug
    r = requests.post(url, headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    j = r.json()
    ids[key] = j["id"]
    IDS_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
    print(lang, j["id"], j["status"], j["slug"], len(re.sub(r"<[^>]+>|<!--.*?-->", "", content)), "chars")
    return j


# =========================== KOREAN ===========================
K = []
kr_title = "현승 & 코타로 교토 브이로그 성지는? 소바・카페・기요미즈데라!"
K.append(p(
    "일본 프로듀스 신세계(일프4)에서 주목받은 유현승과 아사카 코타로(浅香孝太郎)가 교토에서 하루를 즐기는 브이로그를 공개했습니다.",
    "가모가와 강에서 물놀이를 하고, 소바를 먹고, 기요미즈데라 근처에서 빙수까지…보기만 해도 교토에 가고 싶어지는 영상입니다.",
    "영상에 나온 가게를 찾아본 결과, 점심은 <strong>고조가와라마치의 「소바 테우치 타카하시(蕎麦手打ち たか橋)」</strong>, 쉬어 간 카페는 <strong>기요미즈데라 바로 옆 「CAFE OTOWA(카페 오토와)」</strong>였습니다.",
    "이 글에서는 두 사람이 돌아본 코스를 순서대로 따라가며 메뉴와 영업시간, 성지순례 팁까지 정리했습니다.",
))
K.append(ui.table("교토 브이로그 기본 정보", [
    ("영상 제목", "日本人が韓国語で、韓国人が日本語で話す京都デート | VOLG"),
    ("공개일", "2026년 9월 27일"),
    ("채널", "유현승 공식 YouTube(유현승 ヒョンスン)"),
    ("출연", "유현승, 아사카 코타로"),
    ("길이", "약 13분 30초"),
]))
K.append(img("open", "교토 브이로그 오프닝에서 인사하는 유현승(빨간 머리)과 아사카 코타로(금발)", "출처: "))
K.append(ui.titlebox("이 글에서 알 수 있는 것", [
    "교토 브이로그의 내용과 두 사람의 관계",
    "두 사람이 돌아본 코스",
    "물놀이를 한 가모가와의 위치",
    "점심을 먹은 소바 가게",
    "빙수를 먹은 카페",
    "기요미즈데라에서 도전한 것",
    "성지순례 추천 코스",
]))
K.append(route_table(["순서", "장소", "한 일"], [
    ("1", "교토역 주변〜가모가와(시치조 대교 부근)", "맨발로 강에 들어가 물놀이"),
    ("2", "소바 테우치 타카하시(고조가와라마치)", "점심으로 자루소바와 튀김"),
    ("3", "고조자카〜CAFE OTOWA", "딸기 빙수와 말차 아포가토로 휴식"),
    ("4", "기요미즈자카의 가게", "오이 절임 꼬치(잇폰즈케) 첫 도전"),
    ("5", "기요미즈데라", "벤케이의 석장에 도전, 기요미즈 무대에서 기념사진"),
    ("6", "오사카(나가호리 지역)", "밤에는 영화를 보고 해산"),
]))
K.append(h2("현승 & 코타로 교토 브이로그는 어떤 영상?"))
K.append(ui.minibox("<strong>콘셉트:</strong>일본인 코타로는 한국어로, 한국인 현승은 일본어로 말하는 교토 데이트",
                    "<strong>공개 채널:</strong>유현승 공식 YouTube"))
K.append(p(
    "이번 영상은 2026년 9월 27일 유현승의 YouTube 채널에 공개된 브이로그입니다.",
    "제목 그대로 일본인인 아사카 코타로가 일부러 한국어로, 한국인인 현승이 일본어로 말한다는 규칙으로 교토를 돌아다닙니다.",
    "중간에 「왜 서로 언어를 바꿔서 말하고 있는 거예요?」라며 스스로 태클을 거는 장면도 있어, 이 반전 규칙이 영상의 재미를 더해 줍니다.",
))
K.append(p(
    "두 사람은 원래 한국 보이그룹 PICKUS(피커스)의 전 멤버입니다.",
    "이후 한국 오디션 프로그램 「PROJECT 7」을 거쳐, 2026년 봄 「PRODUCE 101 JAPAN 신세계(일프4)」에도 함께 참가했습니다.",
    "오랜 시간을 함께 보낸 사이답게, 대화의 호흡과 편안한 티키타카에서도 두 사람의 친분이 느껴집니다.",
    f"두 사람의 경력은 {a('https://chomoand-1.com/yoohyeonseung_wiki-1732', '유현승 위키 프로필 글(일본어)')}과 {a('https://chomoand-1.com/asakakotaro_wiki-1228', '아사카 코타로 위키 프로필 글(일본어)')}에서 자세히 소개하고 있습니다.",
))
K.append(p(
    "영상에서는 행선지를 「타로의 추천으로」 정하는 장면이 있어, 교토 안내는 오사카 출신인 코타로가 맡았던 것으로 보입니다.",
    "현승에게는 이번이 첫 교토였던 듯, 초반부터 「수학여행!」이라며 신이 난 모습이었습니다.",
    "거리에 붙어 있던 전시회 포스터(회기 2026년 7월 25일〜8월 23일)와 양산・휴대용 선풍기를 놓지 못하는 모습을 보면, 촬영은 올여름 한창 더울 때로 보입니다.",
))
K.append(h2("물놀이를 한 가모가와는 어디? 시치조 대교 부근으로 추정"))
K.append(ui.minibox("<strong>장소(추정):</strong>교토시립예술대학 근처, 시치조 대교(七条大橋) 부근의 가모가와",
                    "<strong>가까운 역:</strong>게이한 「시치조」역, JR 「교토」역에서 도보권"))
K.append(p(
    "기차로 교토에 도착한 두 사람이 가장 먼저 향한 곳은, 현승 말로 「정말 예쁜 곳」인 가모가와(鴨川)였습니다.",
    "가는 길에 교토시립예술대학 갤러리 「@KCUA」의 전시회 포스터 앞을 지나고 있어, 교토역 동쪽 가모가와 강변의 스진(崇仁) 지역을 걸었다는 것을 알 수 있습니다.",
))
K.append(img("kamo_bridge", "가모가와 얕은 물에 맨발로 들어간 유현승, 뒤로 아치가 이어진 다리", "출처: "))
K.append(p(
    "강에 도착하자마자 현승은 신발을 벗고 얕은 물로 들어가 「형도 와요〜!」라며 코타로를 불렀습니다.",
    "뒤에 보이는 여러 개의 아치가 이어진 다리는, 1913년에 완공된 가모가와에서 현존하는 가장 오래된 다리 <strong>시치조 대교</strong>와 매우 닮았습니다.",
    "교토시립예술대학에서도 걸어서 금방인 곳이라, 두 사람이 물놀이를 한 곳은 시치조 대교 바로 상류 부근으로 봐도 좋을 것 같습니다.",
))
K.append(p(
    "또 하나 놓칠 수 없는 것이 현승의 「비둘기 사랑」입니다.",
    "화단에 있던 비둘기에 푹 빠져 「비둘기 정말 좋아해요」라고 말하고, 돌담을 오르는 비둘기에게는 「등산 비둘기」라는 이름까지 붙이며 신나 했습니다.",
    "코타로에게 「카카오톡 프로필 사진도 비둘기였잖아」라는 말을 듣는 장면도 있어, 알고 보니 찐 비둘기 러버인 듯합니다.",
))
K.append(gmap("七条大橋 京都"))
K.append(h2("점심 소바 가게는 고조가와라마치의 「소바 테우치 타카하시」"))
K.append(ui.minibox("<strong>가게 이름:</strong>蕎麦手打ち たか橋(soba restaurant Takahashi)",
                    "<strong>주소:</strong>京都府京都市下京区平居町23(가와라마치고조 교차로에서 남쪽으로 약 100m)",
                    "<strong>먹은 음식:</strong>자루소바와 튀김(닭튀김으로 보이는 튀김・새우튀김 등)"))
K.append(p(
    "가모가와에서 한바탕 논 뒤, 「배고프다」는 두 사람이 점심으로 고른 곳이 고조가와라마치에 있는 「소바 테우치 타카하시」입니다.",
    "「오늘의 점심 메뉴」라는 자막과 함께 나온 것은 대나무 채반에 담긴 소바와 큰 접시의 튀김이었습니다.",
))
K.append(img("soba", "소바 테우치 타카하시에서 먹은 자루소바와 튀김", "출처: "))
K.append(p(
    "튀김 접시에는 두툼한 튀김옷의 튀김과 채소 튀김이 담겨 있고, 다른 접시에는 새우튀김도 보입니다.",
    f"타카하시에서는 닭고기 튀김을 곁들인 {marker('「가시와텐 자루」')}가 예전부터 대표 메뉴로 소개되어 왔기 때문에, 영상 속 튀김도 이 닭튀김일 가능성이 높아 보입니다.",
    "다 먹은 두 사람은 「먹었습니다〜!」라며 만족스러워했고, 「거기는 아마 튀김이 정말」이라며 튀김을 극찬했습니다.",
))
K.append(p(
    "타카하시는 기온에서 수련한 장인이 직접 면을 뽑는 수타 소바 가게입니다.",
    "굵게 간 「토이치 소바」와 곱게 간 「주와리(100%) 소바」 두 종류가 있고, 두 가지를 비교해 먹을 수 있는 「니슈모리(2종 모둠)」도 인기 메뉴입니다.",
    "가게는 옛 오차야(찻집) 건물을 그대로 살려, 외관과 간판에도 당시의 분위기가 남아 있습니다.",
    "영상에 나온 전통 서랍장이 놓인 차분한 실내도 이 오래된 건물만의 분위기입니다.",
))
K.append(ui.table("소바 테우치 타카하시 가게 정보", [
    ("주소", "京都府京都市下京区平居町23"),
    ("교통", "게이한 「기요미즈고조」역에서 도보 약 3분"),
    ("영업시간", "점심 11:30〜15:00(목・금・토는 저녁 18:00〜21:00도 영업, 저녁은 예약 권장)"),
    ("정기휴일", "월요일"),
    ("예산", "1,000〜2,000엔 정도"),
    ("메뉴 예", "가시와텐 자루, 니슈모리(토이치・주와리) 등"),
]))
K.append(p(
    "메뉴와 가격, 영업시간은 바뀔 수 있으니 방문 전에 최신 정보를 확인하면 안심입니다.",
    "가와라마치 거리에서 조금 들어간 골목에 있어서 지도를 보면서 가는 것을 추천합니다.",
))
K.append(gmap("蕎麦手打ち たか橋 京都市下京区平居町23", 17))
K.append(h2("빙수를 먹은 카페는 기요미즈데라 옆 「CAFE OTOWA」"))
K.append(ui.minibox("<strong>가게 이름:</strong>CAFE OTOWA(카페 오토와)",
                    "<strong>주소:</strong>京都府京都市東山区五条橋東6-583-31(고조자카・차완자카 바로 옆)",
                    "<strong>먹은 음식:</strong>딸기 빙수, 말차 아포가토"))
K.append(p(
    "점심 후에는 고조자카를 올라 기요미즈데라 방향으로.",
    "「녹을 것 같아」라며 언덕을 걷던 두 사람이 피신한 곳이 기요미즈데라 참배길 바로 앞에 있는 「CAFE OTOWA」였습니다.",
    "가게에 들어온 코타로는 분홍색 휴대용 선풍기를 들고 「시원해졌어요」라며 한숨 돌렸습니다.",
))
K.append(img("cafe_both", "CAFE OTOWA에서 말차를 붓는 아사카 코타로, 앞에는 딸기 빙수", "출처: "))
K.append(p(
    f"테이블에 놓인 것은 과육 가득한 소스를 얹은 {marker('딸기 빙수')}와 바닐라 아이스에 말차를 부어 먹는 {marker('말차 아포가토')}입니다.",
    "코타로는 샷 잔의 말차를 직접 아이스 위에 둘러 부었는데, 진한 초록색 말차가 아이스를 감싸는 모습이 정말 맛있어 보였습니다.",
    "빙수는 현승이 「생각보다 훨씬 크네」라고 놀랄 만큼 양이 많았습니다.",
))
K.append(p(
    "CAFE OTOWA는 2016년에 문을 연 카페로, 교토 말차를 사용한 디저트와 오리지널 시럽 빙수, 가벼운 식사까지 즐길 수 있는 곳입니다.",
    "딸기 빙수는 연유 토핑이 가능하고, 말차 아포가토는 말차의 쌉싸름함과 산뜻한 바닐라의 조합이 좋다고 평판이 난 메뉴입니다.",
    "나무의 따뜻함이 느껴지는 실내는 카운터와 테이블을 합쳐 25석 정도로, 관광 중간에 여유롭게 쉴 수 있는 것도 장점입니다.",
))
K.append(p(
    "참고로 이 카페에서는 「【코타로・23】※궁상 체질(貧乏性)」이라는 자막이 붙은 토크도 나왔습니다.",
    "「이런 것도 먹고 싶은 마음…」「아이돌은 안 돼」「알겠습니다…」라는 두 사람의 티키타카에 절로 웃음이 납니다.",
))
K.append(ui.table("CAFE OTOWA 가게 정보", [
    ("주소", "京都府京都市東山区五条橋東6-583-31"),
    ("교통", "게이한 「기요미즈고조」역에서 도보 약 15분, 기요미즈데라 참배길에서 바로"),
    ("영업시간", "11:00〜18:00 무렵(오픈을 11:30으로 안내하는 정보도 있음)"),
    ("정기휴일", "수요일(부정기 휴무가 있을 수 있음)"),
    ("예산", "1,000엔 전후〜"),
    ("메뉴 예", "딸기 빙수, 말차 아포가토, 말차 파르페, 핫도그 등"),
]))
K.append(p(
    "영업시간과 휴일은 정보마다 조금씩 달라서, 방문 전에 가게 SNS 등으로 확인하는 것을 추천합니다.",
    "빙수는 계절에 따라 메뉴가 바뀔 수도 있습니다.",
))
K.append(gmap("CAFE OTOWA 京都市東山区五条橋東6-583-31", 17))
K.append(h2("기요미즈데라에서는 오이 절임과 벤케이의 석장에 도전"))
K.append(ui.minibox("<strong>길거리 음식:</strong>기요미즈자카 가게의 오이 절임 꼬치(잇폰즈케)",
                    "<strong>도전:</strong>본당 앞 「벤케이의 석장(錫杖)」 들어 올리기",
                    "<strong>기념사진:</strong>기요미즈 무대에서 투샷"))
K.append(p(
    "카페에서 더위를 식힌 뒤, 드디어 기요미즈데라로.",
    "참배길 가게에서 두 사람의 눈에 띈 것은 얼음물에 차갑게 담가 둔 오이 절임 꼬치 「잇폰즈케」입니다.",
    "자막에는 「태어나서 처음 보는 음식…」이라고 적혀 있었고, 두 사람 모두 「첫 도전」인 잇폰즈케를 나란히 베어 물었습니다.",
))
K.append(img("kyuri", "기요미즈데라 참배길에서 오이 절임 꼬치를 먹는 유현승과 아사카 코타로", "출처: "))
K.append(p(
    "기요미즈데라 경내에서 현승이 도전한 것은 본당 입구 근처에 놓인 「벤케이의 석장」입니다.",
    "기요미즈데라 7대 불가사의 중 하나로 꼽히며, 큰 석장은 길이 약 2.6m・무게 약 96kg, 작은 석장도 약 17kg이나 됩니다.",
    "들어 올리면 소원이 이루어진다고도 하지만, 자막에서 「마지막 끝판왕」으로 소개된 큰 석장에는 현승도 「전혀 무리였어요」라며 완패했습니다.",
))
K.append(img("shakujo", "기요미즈데라 벤케이의 석장에 도전하는 유현승", "출처: "))
K.append(p(
    "마지막은 기요미즈 무대에서 초록 숲에 둘러싸인 풍경을 배경으로 투샷을 찍었습니다.",
    "무대에서는 여우비 이야기가 나와 「일본에서는 『여우의 시집가기(狐の嫁入り)』라고 한대」「한국에서는 『여우비』라고 해요」라며 한일 언어의 공통점으로 이야기꽃을 피웠습니다.",
))
K.append(img("butai", "기요미즈데라 무대에서 나란히 선 유현승과 아사카 코타로", "출처: "))
K.append(gmap("清水寺", 16))
K.append(h2("밤에는 오사카로 돌아가 영화, 교토 여행의 마무리"))
K.append(ui.minibox("<strong>밤의 행선지:</strong>오사카(간판으로 보아 나가호리 지역으로 추정)",
                    "<strong>한 일:</strong>영화관에서 영화 관람"))
K.append(p(
    "교토를 만끽한 두 사람은 기차에서 「돌아갑니다〜!」라며 교토를 떠났습니다.",
    "밤 장면은 영화관 로비에서 시작되고, 팝콘을 들고 영화를 본 뒤 밤거리를 걸으며 감상을 나눴습니다.",
    "화면에 비친 「크리스타 나가호리(CRYSTA長堀)」 간판으로 보아, 밤에는 오사카 신사이바시・나가호리 지역에 있었던 것으로 보입니다.",
    "마지막에는 현승이 「교토 성공!」이라며 엄지를 치켜세우며 하루 여행을 마무리했습니다.",
))
K.append(h2("현승 & 코타로 교토 브이로그 성지순례 추천 코스"))
K.append(ui.minibox("<strong>소요 시간:</strong>반나절〜하루(도보 중심)",
                    "<strong>주의:</strong>타카하시는 월요일, CAFE OTOWA는 수요일 정기휴일"))
K.append(p(
    "영상 속 코스는 거의 도보로 이어져 있어서, 같은 순서로 성지순례하기 쉬운 것도 매력입니다.",
    "교토역에서 가모가와로 걸어가 북쪽으로 올라가 타카하시에서 점심, 그대로 고조자카를 올라 CAFE OTOWA, 기요미즈데라 순서라면 무리 없이 돌 수 있습니다.",
))
K.append(olbox("교토 브이로그 성지순례 코스", [
    "JR 교토역에서 동쪽으로 걸어 교토시립예술대학 옆을 지나 시치조 대교 부근의 가모가와로",
    "가모가와를 따라 북쪽으로 걸어 가와라마치고조의 「소바 테우치 타카하시」에서 점심",
    "고조자카를 올라 「CAFE OTOWA」에서 빙수와 말차 아포가토",
    "기요미즈자카에서 시원한 오이 절임 꼬치",
    "기요미즈데라에서 벤케이의 석장에 도전하고 기요미즈 무대에서 기념사진",
]))
K.append(p(
    "타카하시는 월요일, CAFE OTOWA는 수요일이 정기휴일이라 두 곳 모두 가고 싶다면 화・목〜일요일을 고르는 것이 좋습니다.",
    "타카하시의 점심은 15시까지이고 기요미즈데라 주변은 저녁이 되면 붐비므로, 오전 중에 가모가와에서 출발하는 것을 추천합니다.",
    "여름에 걷는다면 두 사람처럼 양산과 휴대용 선풍기, 음료도 꼭 챙기세요.",
))
K.append(h2("정리"))
K.append(ui.summary([
    "<strong>영상:</strong>2026년 9월 27일 공개, 현승은 일본어・코타로는 한국어로 말하는 교토 데이트 브이로그",
    "<strong>가모가와:</strong>교토시립예술대학 근처, 시치조 대교 부근으로 추정",
    "<strong>점심:</strong>고조가와라마치 「소바 테우치 타카하시」에서 자루소바와 튀김",
    "<strong>카페:</strong>기요미즈데라 옆 「CAFE OTOWA」에서 딸기 빙수와 말차 아포가토",
    "<strong>기요미즈데라:</strong>오이 절임 꼬치, 벤케이의 석장, 기요미즈 무대에서 투샷",
    "<strong>밤:</strong>오사카로 돌아가 영화 관람",
]))
K.append(p(
    "전 PICKUS 멤버다운 찰떡 호흡과 교토의 대표 명소가 꽉 담긴 브이로그였습니다.",
    "영상을 다시 보면서 같은 코스를 걸으면, 두 사람과 함께 교토 여행을 하는 기분을 느낄 수 있을 것 같아요!",
))
K.append(related("관련 글", [
    ("https://chomoand-1.com/yoohyeonseung_wiki-1732", "유현승 위키 경력・프로필(일본어)"),
    ("https://chomoand-1.com/asakakotaro_wiki-1228", "아사카 코타로 위키 경력・발레 경력(일본어)"),
    ("https://chomoand-1.com/ko/when-and-where-is-the-ricky-hy-kr-12558", "리키 & 현승 합동 이벤트 일정・장소"),
]))
kr_content = "\n\n".join(K)

if not ids.get("eyecatch_kr"):
    out = ROOT / "images" / "hyeonseung_kotaro_kyoto_vlog_eyecatch_kr.png"
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
                    "--top", "현승 & 코타로", "--main", "교토 VLOG",
                    "--bottom", "성지는 어디? 소바・카페・기요미즈데라!",
                    "--lang", "kr", "--out", str(out), "--seed", str(JP_ID)], check=True)
    m = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HEADERS_AUTH, "Content-Type": "image/png",
                               "Content-Disposition": 'attachment; filename="hyeonseung_kotaro_kyoto_vlog_eyecatch_kr.png"'},
                      data=out.read_bytes())
    m.raise_for_status()
    ids["eyecatch_kr"] = m.json()["id"]
    IDS_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
kr_summary = ("유현승과 아사카 코타로의 교토 브이로그 성지를 정리했습니다. 가모가와(시치조 대교 부근), 점심 「소바 테우치 타카하시」, "
              "기요미즈데라 옆 「CAFE OTOWA」의 빙수와 말차 아포가토, 벤케이의 석장까지. 성지순례 코스도 소개!")
post_lang(kr_title, kr_content, JP_SLUG + "-kr", "ko", kr_summary, ids["eyecatch_kr"], "kr")

# =========================== ENGLISH ===========================
E = []
en_title = "Hyeonseung & Kotaro's Kyoto Vlog Spots: Soba, Cafe & Kiyomizu-dera"
E.append(p(
    "Yoo Hyeonseung and Kotaro Asaka, who both drew attention on PRODUCE 101 JAPAN THE NEW WORLD, released a vlog of a full day out in Kyoto.",
    "They splash around in the Kamo River, eat soba, and cool off with shaved ice near Kiyomizu-dera. It is the kind of video that makes you want to book a trip to Kyoto.",
    "We looked into the places that appear in the video: lunch was at <strong>Soba Teuchi Takahashi in Gojo-Kawaramachi</strong>, and the cafe they rested at was <strong>CAFE OTOWA, right next to Kiyomizu-dera</strong>.",
    "This article follows their route in order and covers the menus, opening hours, and tips for visiting the same spots.",
))
E.append(ui.table("Kyoto Vlog Basics", [
    ("Video title", "日本人が韓国語で、韓国人が日本語で話す京都デート | VOLG"),
    ("Released", "September 27, 2026"),
    ("Channel", "Yoo Hyeonseung's official YouTube (유현승 ヒョンスン)"),
    ("Starring", "Yoo Hyeonseung, Kotaro Asaka"),
    ("Length", "About 13.5 minutes"),
]))
E.append(img("open", "Yoo Hyeonseung (red hair) and Kotaro Asaka (blond) greeting viewers at the start of the Kyoto vlog", "Source: "))
E.append(ui.titlebox("What This Article Covers", [
    "What the Kyoto vlog is about and how the two know each other",
    "The route they took",
    "Where on the Kamo River they played",
    "The soba restaurant for lunch",
    "The cafe where they had shaved ice",
    "What they tried at Kiyomizu-dera",
    "A model route for fans",
]))
E.append(route_table(["Order", "Place", "What they did"], [
    ("1", "Around Kyoto Station to the Kamo River (near Shichijo Ohashi Bridge)", "Waded barefoot into the river"),
    ("2", "Soba Teuchi Takahashi (Gojo-Kawaramachi)", "Zaru soba and tempura for lunch"),
    ("3", "Gojozaka to CAFE OTOWA", "Strawberry shaved ice and matcha affogato"),
    ("4", "A shop on Kiyomizuzaka", "First try at a whole pickled cucumber on a stick"),
    ("5", "Kiyomizu-dera", "Tried lifting Benkei's staff, photos on the Kiyomizu stage"),
    ("6", "Osaka (Nagahori area)", "Watched a movie at night"),
]))
E.append(h2("What Is Hyeonseung & Kotaro's Kyoto Vlog About?"))
E.append(ui.minibox("<strong>Concept:</strong>A Kyoto day out where Japanese Kotaro speaks Korean and Korean Hyeonseung speaks Japanese",
                    "<strong>Posted on:</strong>Yoo Hyeonseung's official YouTube channel"))
E.append(p(
    "The video is a vlog posted on Yoo Hyeonseung's YouTube channel on September 27, 2026.",
    "As the title says, the rule for the day is that Kotaro, who is Japanese, speaks Korean, while Hyeonseung, who is Korean, speaks Japanese.",
    "At one point they even laugh at themselves, asking why they are both speaking each other's language, and the role reversal gives the whole video its charm.",
))
E.append(p(
    "The two are former bandmates from the Korean boy group PICKUS.",
    "They later went through the Korean audition show PROJECT 7, and both took part in PRODUCE 101 JAPAN THE NEW WORLD in spring 2026.",
    "Having spent so much time together, their easy back-and-forth makes it clear how close they are.",
    f"For more on their careers, see our {a('https://chomoand-1.com/yoohyeonseung_wiki-1732', 'Yoo Hyeonseung profile (Japanese)')} and {a('https://chomoand-1.com/asakakotaro_wiki-1228', 'Kotaro Asaka profile (Japanese)')}.",
))
E.append(p(
    "In the video, Hyeonseung says they picked their stops based on Taro's recommendations, so Kotaro, who is from Osaka, seems to have been the tour guide.",
    "It appears to have been Hyeonseung's first time in Kyoto, and he was excited from the start, calling it a school trip.",
    "An exhibition poster on the street (running July 25 to August 23, 2026) and the parasols and handheld fans they never put down suggest the vlog was filmed in the middle of this summer.",
))
E.append(h2("Where on the Kamo River Did They Play? Likely Near Shichijo Ohashi Bridge"))
E.append(ui.minibox("<strong>Location (estimated):</strong>The Kamo River near Shichijo Ohashi Bridge, close to Kyoto City University of Arts",
                    "<strong>Nearest stations:</strong>Keihan Shichijo Station; walkable from JR Kyoto Station"))
E.append(p(
    "After arriving in Kyoto by train, their first stop was the Kamo River, which Hyeonseung described as a really beautiful place.",
    "On the way they pass a poster for an exhibition at @KCUA, the gallery of Kyoto City University of Arts, which places them in the Sujin area east of Kyoto Station along the river.",
))
E.append(img("kamo_bridge", "Yoo Hyeonseung standing barefoot in the shallows of the Kamo River, with a multi-arched bridge behind him", "Source: "))
E.append(p(
    "As soon as they reached the river, Hyeonseung took off his shoes, stepped into the shallows, and called for Kotaro to join him.",
    "The bridge in the background, with its row of arches, closely resembles <strong>Shichijo Ohashi</strong>, completed in 1913 and the oldest surviving bridge on the Kamo River.",
    "Since it is just a short walk from the arts university, it is safe to say they were playing just upstream of Shichijo Ohashi.",
))
E.append(p(
    "Another highlight is Hyeonseung's love of pigeons.",
    "He gets completely absorbed watching pigeons in a flower bed, says he really likes pigeons, and even names one climbing a stone wall the mountain-climbing pigeon.",
    "Kotaro teases him that his KakaoTalk profile picture used to be a pigeon, so it seems he is a true pigeon fan.",
))
E.append(gmap("七条大橋 京都"))
E.append(h2("Lunch: Soba Teuchi Takahashi in Gojo-Kawaramachi"))
E.append(ui.minibox("<strong>Name:</strong>蕎麦手打ち たか橋 (soba restaurant Takahashi)",
                    "<strong>Address:</strong>23 Hiraicho, Shimogyo-ku, Kyoto (about 100 m south of the Kawaramachi-Gojo intersection)",
                    "<strong>What they ate:</strong>Zaru soba and tempura (what looks like chicken tempura, shrimp tempura, and more)"))
E.append(p(
    "After playing in the river, the hungry pair headed to Soba Teuchi Takahashi in Gojo-Kawaramachi for lunch.",
    "With the caption \"today's lunch menu,\" the video shows soba on a bamboo tray alongside a large plate of tempura.",
))
E.append(img("soba", "Zaru soba and tempura at Soba Teuchi Takahashi", "Source: "))
E.append(p(
    "The tempura plate holds chunky battered pieces and leafy greens, and a second plate appears to include shrimp tempura.",
    f"Takahashi has long been known for its {marker('kashiwa-ten zaru')}, cold soba served with chicken tempura, so the fried pieces in the video are very likely that chicken tempura.",
    "After the meal, the two happily said they had eaten well and raved that the tempura there is really good.",
))
E.append(p(
    "Takahashi serves handmade soba by a chef who trained in Gion.",
    "It offers two types, a coarse-ground \"toichi\" soba and a fine-ground 100% buckwheat \"juwari\" soba, and a two-kind platter lets you compare both.",
    "The restaurant is housed in a former teahouse, and its exterior and signboard still carry the feel of that era.",
    "The calm dining room with traditional wooden chests seen in the video comes from the character of this old building.",
))
E.append(ui.table("Soba Teuchi Takahashi Info", [
    ("Address", "23 Hiraicho, Shimogyo-ku, Kyoto"),
    ("Access", "About 3 minutes on foot from Keihan Kiyomizu-Gojo Station"),
    ("Hours", "Lunch 11:30-15:00 (also dinner 18:00-21:00 Thu-Sat; reservations recommended for dinner)"),
    ("Closed", "Mondays"),
    ("Budget", "About 1,000-2,000 yen"),
    ("Menu examples", "Kashiwa-ten zaru, two-kind platter (toichi and juwari)"),
]))
E.append(p(
    "Menus, prices, and hours can change, so it is a good idea to check the latest information before you go.",
    "The restaurant sits on a side alley just off Kawaramachi Street, so it helps to follow a map.",
))
E.append(gmap("蕎麦手打ち たか橋 京都市下京区平居町23", 17))
E.append(h2("Shaved Ice at CAFE OTOWA, Right by Kiyomizu-dera"))
E.append(ui.minibox("<strong>Name:</strong>CAFE OTOWA",
                    "<strong>Address:</strong>6-583-31 Gojobashi-higashi, Higashiyama-ku, Kyoto (right by Gojozaka and Chawanzaka)",
                    "<strong>What they ate:</strong>Strawberry shaved ice, matcha affogato"))
E.append(p(
    "After lunch, they climbed Gojozaka toward Kiyomizu-dera.",
    "Saying they felt like they were melting, the two ducked into CAFE OTOWA, located just before the temple approach.",
    "Once inside, Kotaro held up a pink handheld fan and sighed that it had finally cooled down.",
))
E.append(img("cafe_both", "Kotaro Asaka pouring matcha at CAFE OTOWA, with strawberry shaved ice in front", "Source: "))
E.append(p(
    f"On the table were {marker('strawberry shaved ice')} topped with a chunky fruit sauce and a {marker('matcha affogato')}, vanilla ice cream you finish by pouring matcha over it.",
    "Kotaro poured the shot of matcha over the ice cream himself, and the thick green matcha coating the vanilla looked delicious.",
    "The shaved ice was so big that Hyeonseung was surprised it was much larger than he expected.",
))
E.append(p(
    "CAFE OTOWA opened in 2016 and serves Kyoto matcha sweets, shaved ice with house-made syrups, and light meals.",
    "The strawberry shaved ice can be topped with condensed milk, and the matcha affogato is popular for the balance of bitter matcha and light vanilla.",
    "The warm, wood-filled interior seats about 25 across the counter and tables, making it a relaxing break during sightseeing.",
))
E.append(p(
    "The cafe is also where a caption labeled Kotaro, 23, as frugal to a fault, and the two traded lines like \"I kind of want to eat this too...\" \"Idols can't,\" and \"Understood...\", which is hard not to laugh at.",
))
E.append(ui.table("CAFE OTOWA Info", [
    ("Address", "6-583-31 Gojobashi-higashi, Higashiyama-ku, Kyoto"),
    ("Access", "About 15 minutes on foot from Keihan Kiyomizu-Gojo Station, steps from the Kiyomizu-dera approach"),
    ("Hours", "Around 11:00-18:00 (some sources list an 11:30 opening)"),
    ("Closed", "Wednesdays (may also close irregularly)"),
    ("Budget", "Around 1,000 yen and up"),
    ("Menu examples", "Strawberry shaved ice, matcha affogato, matcha parfait, hot dogs"),
]))
E.append(p(
    "Hours and closing days differ slightly between sources, so check the cafe's social media before visiting.",
    "The shaved ice menu may also change with the seasons.",
))
E.append(gmap("CAFE OTOWA 京都市東山区五条橋東6-583-31", 17))
E.append(h2("At Kiyomizu-dera: Pickled Cucumber and Benkei's Staff"))
E.append(ui.minibox("<strong>Street food:</strong>A whole pickled cucumber on a stick from a shop on Kiyomizuzaka",
                    "<strong>Challenge:</strong>Trying to lift Benkei's staff in front of the main hall",
                    "<strong>Photo spot:</strong>A two-shot on the Kiyomizu stage"))
E.append(p(
    "Cooled off, they finally headed to Kiyomizu-dera.",
    "Along the approach, a tray of cucumbers chilling in ice water caught their eye: ippon-zuke, a whole pickled cucumber served on a stick.",
    "The caption called it a food they were seeing for the first time in their lives, and the two bit into their first ippon-zuke side by side.",
))
E.append(img("kyuri", "Yoo Hyeonseung and Kotaro Asaka eating pickled cucumbers on sticks near Kiyomizu-dera", "Source: "))
E.append(p(
    "Inside the temple grounds, Hyeonseung took on Benkei's staffs, displayed near the entrance of the main hall.",
    "They are counted among the Seven Wonders of Kiyomizu-dera: the large staff is about 2.6 m long and weighs about 96 kg, and even the small one weighs about 17 kg.",
    "Lifting one is said to make your wish come true, but against the large staff, introduced in the captions as the final boss, Hyeonseung admitted it was completely impossible.",
))
E.append(img("shakujo", "Yoo Hyeonseung trying to lift Benkei's staff at Kiyomizu-dera", "Source: "))
E.append(p(
    "To finish, they took a two-shot on the Kiyomizu stage with the green hillside behind them.",
    "Talk turned to sun showers, and they bonded over how Japan calls it a fox's wedding while Korea calls it fox rain, noting how similar the two languages can be.",
))
E.append(img("butai", "Yoo Hyeonseung and Kotaro Asaka side by side on the Kiyomizu stage", "Source: "))
E.append(gmap("清水寺", 16))
E.append(h2("Back to Osaka for a Movie to End the Day"))
E.append(ui.minibox("<strong>Evening:</strong>Osaka (likely the Nagahori area, based on signage)",
                    "<strong>What they did:</strong>Watched a movie at a cinema"))
E.append(p(
    "After a full day in Kyoto, the two headed home by train.",
    "The night scenes begin in a cinema lobby, and after watching a movie with popcorn, they walk the streets at night sharing their thoughts.",
    "A CRYSTA Nagahori sign in the background suggests they were in Osaka's Shinsaibashi and Nagahori area.",
    "Hyeonseung wrapped up the day with a thumbs-up, declaring the Kyoto trip a success.",
))
E.append(h2("A Model Route for Visiting the Kyoto Vlog Spots"))
E.append(ui.minibox("<strong>Time needed:</strong>Half a day to a full day, mostly on foot",
                    "<strong>Note:</strong>Takahashi is closed Mondays and CAFE OTOWA is closed Wednesdays"))
E.append(p(
    "The route in the video is almost entirely walkable, which makes it easy to follow in the same order.",
    "Walk from Kyoto Station to the Kamo River, head north for lunch at Takahashi, then climb Gojozaka to CAFE OTOWA and Kiyomizu-dera.",
))
E.append(olbox("Kyoto Vlog Route", [
    "Walk east from JR Kyoto Station past Kyoto City University of Arts to the Kamo River near Shichijo Ohashi",
    "Follow the river north and have lunch at Soba Teuchi Takahashi in Gojo-Kawaramachi",
    "Climb Gojozaka for shaved ice and matcha affogato at CAFE OTOWA",
    "Grab an ice-cold pickled cucumber on Kiyomizuzaka",
    "Try lifting Benkei's staff at Kiyomizu-dera and take photos on the Kiyomizu stage",
]))
E.append(p(
    "Because Takahashi closes on Mondays and CAFE OTOWA on Wednesdays, choose Tuesday or Thursday through Sunday if you want to visit both.",
    "Takahashi's lunch service ends at 15:00 and the area around Kiyomizu-dera gets crowded in the late afternoon, so starting at the river in the morning works best.",
    "If you go in summer, bring a parasol, a handheld fan, and plenty to drink, just like the two of them.",
))
E.append(h2("Summary"))
E.append(ui.summary([
    "<strong>Video:</strong>Released September 27, 2026; a Kyoto vlog where Hyeonseung speaks Japanese and Kotaro speaks Korean",
    "<strong>Kamo River:</strong>Likely near Shichijo Ohashi, close to Kyoto City University of Arts",
    "<strong>Lunch:</strong>Zaru soba and tempura at Soba Teuchi Takahashi in Gojo-Kawaramachi",
    "<strong>Cafe:</strong>Strawberry shaved ice and matcha affogato at CAFE OTOWA by Kiyomizu-dera",
    "<strong>Kiyomizu-dera:</strong>Pickled cucumber, Benkei's staff, and a two-shot on the stage",
    "<strong>Night:</strong>Back to Osaka for a movie",
]))
E.append(p(
    "With the easy chemistry of two former PICKUS bandmates and a lineup of classic Kyoto spots, this vlog is a treat from start to finish.",
    "Rewatch the video and walk the same route, and it will feel like you are traveling through Kyoto with them!",
))
E.append(related("Related Articles", [
    ("https://chomoand-1.com/yoohyeonseung_wiki-1732", "Yoo Hyeonseung profile and career (Japanese)"),
    ("https://chomoand-1.com/asakakotaro_wiki-1228", "Kotaro Asaka profile and ballet background (Japanese)"),
    ("https://chomoand-1.com/en/when-and-where-is-the-ricky-hy-en-12560", "When and where is the RICKEY & HYEONSEUNG joint event?"),
]))
en_content = "\n\n".join(E)
en_summary = ("A guide to the spots in Yoo Hyeonseung and Kotaro Asaka's Kyoto vlog: the Kamo River near Shichijo Ohashi, "
              "lunch at Soba Teuchi Takahashi, shaved ice and matcha affogato at CAFE OTOWA, and Benkei's staff at Kiyomizu-dera. Plus a model route!")
post_lang(en_title, en_content, JP_SLUG + "-en", "en", en_summary, ids["eyecatch_jp"], "en")
