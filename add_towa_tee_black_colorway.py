# -*- coding: utf-8 -*-
"""TOWAのEMIS Tシャツ記事(公開済み 14635/14636/14637)に、黒の色違い(3PACKのBK)を着ていた公式X動画の節を追記する。
出典: KO1KEYZ公式X 2089917771761205528(2026-08-19、ファンミ東京公演まであと2日)。
公開済みなので title/slug/status=draft は送らない(statusはpublishのまま)。本文は現在のrawを取り直して差し込む。
"""
from _towa_vlog_common import *

ids = load_ids()
TWEET = "https://twitter.com/KO1KEYZofficial/status/2089917771761205528"
TWEET_X = "https://x.com/KO1KEYZofficial/status/2089917771761205528"

if "media_tee_black" not in ids:
    ids["media_tee_black"] = wp_upload(ROOT / "images" / "towa_fanmeeting_countdown_emis_black_tee.jpg", "image/jpeg")["id"]
    save_ids(ids)
m_black = get_media(ids["media_tee_black"])

EMBED = f"""<!-- wp:html -->
<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true"><a href="{TWEET}">{TWEET}</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
<!-- /wp:html -->"""

CHECK = ('<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid #6fa843;border-radius:3px;'
         'color:#6fa843;font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')

SPEC = {
    14635: dict(
        before='<h2 class="wp-block-heading">EMISはどんなブランド？</h2>',
        section=[
            h2("黒の色違いも着ていた？"),
            minibox([("投稿：", "KO1KEYZ公式X(2026年8月19日)"), ("色：", "3PACK T-SHIRT SET Aの黒とみられる")]),
            p("KO1KEYZ公式Xが2026年8月19日に投稿した「1ST FAN MEETING 東京公演まであと2日」の動画では、TOWAが黒いTシャツ姿で登場しています。<br>\n"
              "KOSUKE・RYUJI・YUKIとの4人でカウントダウンをする動画で、TOWAは手前の右側に座っています。"),
            EMBED,
            img_html(m_black, "ファンミーティング前の公式動画で黒いEMISのTシャツを着たTOWA。左胸に白いemisロゴ", f"出典：{TWEET_X}"),
            p(f"左胸には、白い「emis」の文字の上にアーチ状の線が入ったロゴがあり、{mark('Vlogの白Tと同じロゴを白黒反転させたデザイン', True)}です。<br>\n"
              "EMISの公式サイトの商品写真を見ると、3PACKは黒だけが白いロゴ、白とヘザーグレーは黒いロゴになっていて、TOWAの黒Tとロゴの色・大きさ・位置が重なりました。<br>\n"
              "白と黒の両方を着ていたことから、TOWAはこの3PACKをセットで持っているのかもしれません。"),
        ],
        intro_anchor="この記事では、それぞれの見分け方",
        intro_add="さらに、ファンミーティング前の公式Xの動画では、同じTシャツの黒も着ていました。<br>\n",
        li_anchor="<li>ニット帽のブランドとモデル</li>",
        li_add="<li>黒の色違いを着ていた投稿</li>\n",
        sum_anchor="ニット帽はニューエラの「カフニット リブ」ブラックとみられ",
        sum_add="2026年8月19日の公式Xの動画では、同じ3PACKの黒とみられるTシャツも着ていた<br>\n",
    ),
    14636: dict(
        before='<h2 class="wp-block-heading">EMIS는 어떤 브랜드?</h2>',
        section=[
            h2("블랙 컬러도 입었을까?"),
            minibox([("게시물: ", "KO1KEYZ 공식 X(2026년 8월 19일)"), ("컬러: ", "3PACK T-SHIRT SET A 블랙으로 보임")]),
            p("KO1KEYZ 공식 X가 2026년 8월 19일에 올린 '1ST FAN MEETING 도쿄 공연까지 앞으로 2일' 영상에서 TOWA는 검은 티셔츠를 입고 등장합니다.<br>\n"
              "KOSUKE・RYUJI・YUKI와 넷이서 카운트다운을 하는 영상으로, TOWA는 앞줄 오른쪽에 앉아 있습니다."),
            EMBED.replace('data-lang="ja"', 'data-lang="ko"'),
            img_html(m_black, "팬미팅 전 공식 영상에서 검은 EMIS 티셔츠를 입은 TOWA. 왼쪽 가슴에 흰 emis 로고", f"출처: {TWEET_X}"),
            p(f"왼쪽 가슴에는 흰 'emis' 글자 위에 아치 선이 들어간 로고가 있어, {mark('브이로그의 흰 티와 같은 로고를 흑백 반전한 디자인', True)}입니다.<br>\n"
              "EMIS 공식 사이트 상품 사진을 보면 3PACK 중 블랙만 흰 로고이고 화이트와 헤더그레이는 검은 로고인데, TOWA의 검은 티와 로고 색・크기・위치가 겹쳤습니다.<br>\n"
              "화이트와 블랙을 모두 입은 것을 보면, TOWA는 이 3PACK을 세트로 갖고 있는지도 모릅니다."),
        ],
        intro_anchor="이 글에서는 각각을 알아보는 포인트",
        intro_add="또 팬미팅 전 공식 X 영상에서는 같은 티셔츠의 블랙도 입었습니다.<br>\n",
        sum_anchor="비니는 뉴에라 '커프 니트 리브' 블랙으로 보이며",
        sum_add="2026년 8월 19일 공식 X 영상에서는 같은 3PACK의 블랙으로 보이는 티셔츠도 입었다<br>\n",
    ),
    14637: dict(
        before='<h2 class="wp-block-heading">What kind of brand is EMIS?</h2>',
        section=[
            h2("Did he wear the black one too?"),
            minibox([("Post: ", "KO1KEYZ official X (Aug 19, 2026)"), ("Color: ", "Appears to be the black tee from 3PACK T-SHIRT SET A")]),
            p("In the \"1ST FAN MEETING: 2 days until the Tokyo show\" video that KO1KEYZ's official X posted on August 19, 2026, TOWA appears in a black tee.<br>\n"
              "It's a countdown clip with KOSUKE, RYUJI and YUKI, and TOWA is sitting front right."),
            EMBED.replace('data-lang="ja"', 'data-lang="en"'),
            img_html(m_black, "TOWA in a black EMIS tee with a white emis logo on the left chest, from the official pre-fan-meeting video", f"Source: {TWEET_X}"),
            p(f"The left chest has a white \"emis\" with an arch above it, {mark('the same logo as the white tee from the vlog, in reverse colors', True)}.<br>\n"
              "On EMIS's official product photos, only the black tee in the 3-pack has a white logo (the white and heather gray ones have black logos), and the color, size and position match TOWA's black tee.<br>\n"
              "Since he has worn both the white and the black, TOWA may own the whole 3-pack."),
        ],
        intro_anchor="This article covers how to identify them",
        intro_add="He also wore the same tee in black in an official X video before the fan meeting.<br>\n",
        sum_anchor="The beanie appears to be New Era's Rib Cuff Knit in black",
        sum_add="In an official X video from Aug 19, 2026, he also wore what appears to be the black tee from the same 3-pack<br>\n",
    ),
}

for pid, s in SPEC.items():
    raw = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=HEADERS_AUTH).json()
    status = raw["status"]
    c = raw["content"]["raw"]
    if TWEET in c:
        print("SKIP already added", pid)
        continue
    for k in ("before", "intro_anchor", "sum_anchor") + (("li_anchor",) if "li_anchor" in s else ()):
        assert c.count(s[k]) == 1, (pid, k, c.count(s[k]))
    i = c.index(s["before"])
    i = c.rindex("<!-- wp:heading -->", 0, i)
    c = c[:i] + "\n\n".join(s["section"]) + "\n\n" + c[i:]
    c = c.replace(s["intro_anchor"], s["intro_add"] + s["intro_anchor"])
    if "li_anchor" in s:
        c = c.replace(s["li_anchor"], s["li_anchor"] + "\n" + s["li_add"].rstrip("\n"))
    j = c.index(s["sum_anchor"])
    j = c.index("<br>\n", j) + len("<br>\n")
    c = c[:j] + CHECK + s["sum_add"] + c[j:]
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}",
                      headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                      data=json.dumps({"content": c, "status": status}).encode("utf-8"))
    r.raise_for_status()
    print("UPDATED", pid, r.json()["status"], len(c))
