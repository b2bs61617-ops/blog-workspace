# -*- coding: utf-8 -*-
"""TOWAマーティンローズのポロ記事(14704/14706/14707)に、公式「'KO1KEYZ' (Korean ver.) Performance Video」(wCp_X6CBQS8、10/6公開)の
TOWAの名前カードの場面(約12.1秒)と、ピンクの色違い(公式ストア 674JE02110、297ポンド→148.50ポンド)を追記する。statusはdraftのまま。"""
from pathlib import Path

import cv2
import requests
from PIL import Image

import _mubank1009_helpers as h
from _mubank1009_helpers import ROOT, wp_upload, img_html, p, UI

ui = UI(AB="#d7e7bf", AL="#6fa843", BG="#f5f9ed", TH="#e6f0d8", marker="mark_green")
PV = "https://www.youtube.com/watch?v=wCp_X6CBQS8"
PINK = "https://www.martine-rose.com/products/oversized-s-s-polo-in-washed-pink"
VIDEO = Path(r"C:\Users\s30se\AppData\Local\Temp\claude\c--Users-s30se-OneDrive--------CHOMO\9f7d6c19-dad5-4a45-b1b7-fe576668dc5f\scratchpad\towa1012\pv\pv.mp4")

cap = cv2.VideoCapture(str(VIDEO))
cap.set(cv2.CAP_PROP_POS_MSEC, 10500)
for _ in range(49):
    ok, fr = cap.read()
cap.release()
out = ROOT / "images" / "towa_kr_pv_martine_rose_polo.jpg"
Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)).save(out, quality=92)
m = wp_upload(out, "image/jpeg")
print("MEDIA", m["id"])

JP_TT = "<!-- wp:paragraph -->\n<p>同じ日の夜には、公式TikTokで"
KR_TT = "<!-- wp:paragraph -->\n<p>같은 날 밤 공식 틱톡에는"
EN_TT = "<!-- wp:paragraph -->\n<p>That evening, the official TikTok"

JP_ADD = "\n\n".join([
    p("このポロは、10月6日に公開された「KO1KEYZ」(Korean ver.)のPerformance Videoでも着ています。<br>\n"
      f"メンバーを1人ずつ紹介する名前カードの場面で、{ui.mark('「TOWA」のカードに、同じグレーのボーダーのポロ姿', True)}で登場しました。<br>\n"
      "黒い襟と赤い裏地、左胸の赤い三角のロゴ、右胸の紋章まで、音楽中心の日の写真と同じです。"),
    img_html(m, "「KO1KEYZ」(Korean ver.)のPerformance VideoのTOWAの名前カード。グレーのボーダーのポロを着ている", f"出典：{PV}"),
    "",
]) + "\n\n"
KR_ADD = "\n\n".join([
    p("이 폴로는 10월 6일 공개된 'KO1KEYZ'(Korean ver.) Performance Video에서도 입었습니다.<br>\n"
      "멤버를 한 명씩 소개하는 네임 카드 장면에서 " + ui.mark("'TOWA' 카드에 같은 회색 스트라이프 폴로 차림", True) + "으로 등장했습니다."),
    img_html(m, "'KO1KEYZ'(Korean ver.) Performance Video의 TOWA 네임 카드. 회색 스트라이프 폴로", f"출처: {PV}"),
    "",
]) + "\n\n"
EN_ADD = "\n\n".join([
    p("He also wears it in the \"KO1KEYZ\" (Korean ver.) Performance Video released on October 6.<br>\n"
      "In the member name-card scene, " + ui.mark('the "TOWA" card shows him in the same gray striped polo', True) + "."),
    img_html(m, "TOWA's name card in the \"KO1KEYZ\" (Korean ver.) Performance Video, wearing the gray striped polo", f"Source: {PV}"),
    "",
]) + "\n\n"

PINK_JP = p("ちなみに、Performance Videoではほかのメンバーが同じデザインのピンクの色違いを着ている場面もあります。<br>\n"
            f"こちらは「OVERSIZED S/S POLO in WASHED PINK」(品番674JE02110)で、<a href=\"{PINK}\" target=\"_blank\" rel=\"noopener\">マーティン・ローズの公式オンラインストア</a>で買えます。<br>\n"
            f"定価297ポンドが{ui.mark('半額の148.50ポンド(1ポンド200円換算で約3万円)', True)}になっていて、10月12日時点でS・Mサイズに在庫がありました。<br>\n"
            "公式の表記ではピンクは鹿の子の綿100%なので、グレーのものとは生地の風合いが少しちがいます。")
PINK_KR = p("Performance Video에서는 다른 멤버가 같은 디자인의 핑크 컬러를 입은 장면도 있습니다.<br>\n"
            f"'OVERSIZED S/S POLO in WASHED PINK'(품번 674JE02110)로, <a href=\"{PINK}\" target=\"_blank\" rel=\"noopener\">마틴 로즈 공식 온라인 스토어</a>에서 정가 297파운드의 {ui.mark('반값 148.50파운드', True)}에 판매 중이며 10월 12일 기준 S・M 사이즈 재고가 있었습니다.")
PINK_EN = p("In the Performance Video, another member wears the same design in pink.<br>\n"
            f"That's the \"OVERSIZED S/S POLO in WASHED PINK\" (674JE02110), on the <a href=\"{PINK}\" target=\"_blank\" rel=\"noopener\">Martine Rose official store</a> at {ui.mark('half price, £148.50 (from £297)', True)}, with S and M in stock as of October 12.")

edits = {
    14704: [
        (JP_TT, JP_ADD + JP_TT),
        ("<td style=\"border:1px solid #d7e7bf;padding:8px 12px;\">2026年10月10日 MBC「ショー！音楽中心」出演日の公式写真、同日公開の公式TikTok</td>",
         "<td style=\"border:1px solid #d7e7bf;padding:8px 12px;\">「KO1KEYZ」(Korean ver.)のPerformance Video、2026年10月10日 MBC「ショー！音楽中心」出演日の公式写真と公式TikTok</td>"),
        ("公式写真にも公式TikTokにも同じポロで登場していて、この日の「KO1KEYZ」の活動のために用意された衣装です。",
         "Performance Videoにも、音楽中心の日の公式写真とTikTokにも同じポロで登場していて、「KO1KEYZ」(Korean ver.)の活動の衣装です。"),
        ("<p>マーティン・ローズの公式オンラインストアには、10月12日時点でこのポロは並んでいませんでした。<br>\n"
         "セールで動いているサイズはすぐなくなりやすいので、気になる人は早めにチェックしておくと安心です。</p>\n<!-- /wp:paragraph -->",
         "<p>マーティン・ローズの公式オンラインストアには、10月12日時点でこのグレーのポロは並んでいませんでした。<br>\n"
         "セールで動いているサイズはすぐなくなりやすいので、気になる人は早めにチェックしておくと安心です。</p>\n<!-- /wp:paragraph -->\n\n" + PINK_JP),
        ("：新作のチェックに", "：ピンクの色違い(674JE02110)が148.50ポンド"),
    ],
    14706: [
        (KR_TT, KR_ADD + KR_TT),
        ("공식 사진과 틱톡 모두 같은 폴로로 등장해, 이날 'KO1KEYZ' 활동을 위해 준비된 의상입니다.",
         "Performance Video와 음악중심 날 공식 사진・틱톡 모두 같은 폴로로 등장해, 'KO1KEYZ'(Korean ver.) 활동 의상입니다."),
        ("(배송비・관세 별도).</p>\n<!-- /wp:paragraph -->",
         "(배송비・관세 별도).</p>\n<!-- /wp:paragraph -->\n\n" + PINK_KR),
    ],
    14707: [
        (EN_TT, EN_ADD + EN_TT),
        ("It shows up in both the official photo and the TikTok, so it's his stage costume for the \"KO1KEYZ\" promotions that day.",
         "It appears in the Performance Video as well as the Music Core-day photo and TikTok, so it's his costume for the \"KO1KEYZ\" (Korean ver.) promotions."),
        ("Shipping and duties are extra.</p>\n<!-- /wp:paragraph -->",
         "Shipping and duties are extra.</p>\n<!-- /wp:paragraph -->\n\n" + PINK_EN),
    ],
}

for pid, reps in edits.items():
    r = requests.get(f"{h.WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=h.HEADERS_AUTH, timeout=60).json()
    assert r["status"] == "draft", (pid, r["status"])
    raw = r["content"]["raw"]
    for a, b in reps:
        assert raw.count(a) == 1, (pid, raw.count(a), a[:40])
        raw = raw.replace(a, b)
    u = requests.post(f"{h.WP_URL}/wp-json/wp/v2/posts/{pid}", headers=h.HEADERS_AUTH,
                      json={"content": raw, "status": "draft"}, timeout=60)
    print(pid, u.status_code, u.json().get("status"))
