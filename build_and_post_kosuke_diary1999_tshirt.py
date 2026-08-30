# -*- coding: utf-8 -*-
"""KOSUKE(照井康祐) DIARY 1999「ARC CONSTRUCTED T-SHIRT」記事: JP + KR + EN 下書き投稿。
再実行時は tmp_kosuke_diary1999_*.txt に既存IDがあれば更新にフォールバックせず新規作成する(初回想定)。
"""
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

FALLBACK_SLUG = "kosuke-diary-1999-arc-tshirt"

# --- KOSUKE メンバーカラー(赤)に寄せたパステル配色 ---
AB = "#efc9c4"   # border
AL = "#c0473d"   # accent / title bar bg (white text OK)
AL2 = "#d9635a"  # border-left accent
BG = "#fdf3f1"   # box background

# 内部リンク
HAIRMILK_JP = "https://chomoand-1.com/ko1keyz-kosukes-hair-milk-reve-11136"
PROFILE_JP = "https://chomoand-1.com/teruikosuke_profile-106"
PROFILE_KR = "https://chomoand-1.com/ko/teruikosuke_profile-kr-10623"
SHOESIZE_JP = "https://chomoand-1.com/what-are-the-shoe-sizes-of-ko1-11551"


def get_slug(title, fallback):
    try:
        import urllib.request, urllib.parse
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={urllib.parse.quote(title)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        en = "".join(seg[0] for seg in data[0])
        slug = re.sub(r"[^a-z0-9\s-]", "", en.lower())
        slug = re.sub(r"\s+", "-", slug.strip())
        slug = re.sub(r"-+", "-", slug)[:30].rstrip("-")
        if slug:
            return slug
    except Exception as e:
        print("translate failed, fallback slug:", e)
    return fallback


def plain_len(html):
    return len(re.sub(r"<!--.*?-->|<[^>]+>", "", html, flags=re.S))


def post_new(title, content, slug, categories, summary, featured_media, lang=None, ja_id=None):
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "categories": categories,
        "author": 2,
        "featured_media": featured_media,
        "meta": {"jetpack_publicize_message": summary},
    }
    if lang:
        payload["lang"] = lang
        payload["translations"] = {"ja": ja_id}
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    return r.json()


def make_eyecatch(top, main, bottom, out_name, seed, lang=None):
    out = ROOT / "images" / out_name
    cmd = [
        sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
        "--top", top, "--main", main, "--bottom", bottom,
        "--out", str(out), "--seed", str(seed),
    ]
    if lang:
        cmd += ["--lang", lang]
    subprocess.run(cmd, check=True)
    mr = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HEADERS_AUTH, "Content-Type": "image/png",
                 "Content-Disposition": f'attachment; filename="{out_name}"'},
        data=out.read_bytes(),
    )
    mr.raise_for_status()
    return mr.json()["id"]


# ============================ JAPANESE ============================
TITLE = "【KOSUKE】リールで着てたTシャツは？DIARY 1999と判明！"
md = (ROOT / "articles" / "ko1keyz_kosuke_diary1999_arc_tshirt.md").read_text(encoding="utf-8")
# strip H1 line
JP_CONTENT = re.sub(r"\A#[^\n]*\n+", "", md).strip()
assert "<hr" not in JP_CONTENT and "\n---\n" not in JP_CONTENT, "hr found"

JP_SUMMARY = ("KO1KEYZのKOSUKEが公式インスタのリール動画で着ていた黒いプリントTシャツは、"
              "イギリス発のストリートブランドDIARY 1999の「DIARY ARC CONSTRUCTED T-SHIRT」とみられます。"
              "国内参考価格は3万6300円で、ブランドの成り立ちや購入先もまとめました。")

SLUG = get_slug(TITLE, FALLBACK_SLUG)
print("JP SLUG:", SLUG, "| len(content):", plain_len(JP_CONTENT), "| len(title):", len(TITLE))

jp_eye_id = make_eyecatch(
    "KOSUKEがリールで着てたTシャツは？", "DIARY 1999", "3万6300円の黒Tと判明！",
    "kosuke_diary1999_tshirt_eyecatch.png", seed=0,
)
print("JP eyecatch media id:", jp_eye_id)

jp_post = post_new(TITLE, JP_CONTENT, SLUG, [66, 63, 102], JP_SUMMARY, jp_eye_id)
JP_ID = jp_post["id"]
print("JP_POST_ID:", JP_ID, "| slug:", jp_post["slug"], "| preview:", f"{WP_URL}/?p={JP_ID}")
(ROOT / "tmp_kosuke_diary1999_ids.txt").write_text(
    f"jp={JP_ID} slug={jp_post['slug']} jp_eyecatch={jp_eye_id}\n", encoding="utf-8")

# regenerate JP eyecatch with real post id as seed (keep look tied to post), reuse same media (optional skip)

# ============================ KOREAN ============================
kr_title = "KO1KEYZ KOSUKE가 릴스에서 입은 티셔츠는? 브랜드는 DIARY 1999!"

KR_CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZ의 KOSUKE(테루이 코스케)가 2026년 8월 29일경 그룹 공식 인스타그램(@ko1keyzofficial)에 올라온 릴스 영상에서 입고 있던, 가슴에 「DIARY」라고 크게 프린트된 검은 티셔츠에 「어느 브랜드야?」라는 목소리가 나오고 있습니다.<br>
먼저 결론부터 말씀드리면, 이 티셔츠는 <strong>DIARY 1999(다이어리 1999)의 「DIARY ARC CONSTRUCTED T-SHIRT」</strong>로 보이며, 일본 국내 참고 가격은 <strong><span class="swl-marker mark_pink" style="font-size:1.15em;">3만 6300엔(세금 포함)</span></strong>입니다.<br>
이 기사에서는 KOSUKE가 티셔츠를 입고 있던 영상의 모습, 티셔츠의 특징과 DIARY 1999라는 브랜드, 그리고 가격과 살 수 있는 곳까지 순서대로 정리합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">KOSUKE 착용 티셔츠 기본 정보</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:35%;">브랜드</td><td style="border:1px solid #ccc;padding:8px 12px;">DIARY 1999(다이어리 1999／영국에서 시작된 브랜드)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">아이템</td><td style="border:1px solid #ccc;padding:8px 12px;">DIARY ARC CONSTRUCTED T-SHIRT(블랙・반팔)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">포인트</td><td style="border:1px solid #ccc;padding:8px 12px;">가슴의 아치형 「DIARY」 칼리지 로고, 어깨에 절개 패널이 들어간 빅 실루엣</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">소재</td><td style="border:1px solid #ccc;padding:8px 12px;">코튼 100%</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">참고 가격</td><td style="border:1px solid #ccc;padding:8px 12px;">3만 6300엔(세금 포함／일본 국내 셀렉트숍)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">착용 장면</td><td style="border:1px solid #ccc;padding:8px 12px;">2026년 8월 29일경 게시된 KO1KEYZ 공식 인스타그램 릴스 영상(KOSUKE 솔로)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AL};color:#fff;">이 기사에서 알 수 있는 것</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>KOSUKE가 티셔츠를 입은 영상・장면</li>
<li>티셔츠의 브랜드와 아이템명</li>
<li>DIARY 1999라는 브랜드의 배경</li>
<li>참고 가격과 살 수 있는 곳</li>
<li>사복인지 여부</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">KOSUKE는 어느 영상에서 이 티셔츠를 입었을까?</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #ddd;border-left:4px solid {AL2};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>착용 장면:</strong>2026년 8월 29일경 KO1KEYZ 공식 인스타그램에 게시된 KOSUKE 혼자 나오는 릴스 영상. 빌딩 옥상 같은 장소에서 카메라를 향해 짧은 댄스와 핸드 사인을 보여주는 세로형 쇼트 영상입니다.</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>KO1KEYZ 공식 인스타그램에서는 멤버 각자의 솔로 릴스가 연달아 공개되고 있으며, KOSUKE 편에서는 옥상 같은 장소에서 촬영한 몇 초짜리 댄스 영상이 올라왔습니다.<br>
후렴에 맞춰 몸을 흔들고, 마지막에 손가락으로 L자를 만드는 듯한 핸드 사인으로 카메라를 바라보는, 짧고 경쾌한 내용입니다.<br>
영상의 주인공은 KOSUKE의 표정과 댄스지만, 그 뒤로 「입고 있는 검은 티셔츠는 어디 거야?」라고 궁금해한 팬이 많았는지, 브랜드를 찾는 글이 X와 댓글에서 보였습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>이 영상에서 KOSUKE는 검은 프린트 티셔츠 안에 꽃무늬 같은 올오버 패턴의 긴팔 티를 겹쳐 입고, 허리에는 카키색 셔츠를 둘렀습니다.<br>
하의도 같은 카키 계열의 와이드 팬츠이고, 목에는 열쇠 모티브가 달린 가느다란 실버 네크리스, 손가락에는 얇은 실버 링을 여러 개 겹쳐 끼고 있습니다.<br>
전체적으로 헐렁한 사이즈로 정리한, 스트리트 무드의 사복 스타일입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>가장 눈길을 끄는 것이 가슴에 크게 프린트된 「DIARY」라는 글자입니다.<br>
아치를 그리듯 배치된 칼리지풍 로고이고, 색은 그레이입니다.<br>
이 로고의 형태와 서체, 그리고 어깨 부분에 절개 패널이 들어간 만듦새를 단서로, 어느 브랜드의 어느 아이템인지 조사해 봤습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">KOSUKE의 티셔츠는 DIARY 1999 「ARC CONSTRUCTED T-SHIRT」</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>시판 아이템과 대조해 보니, 특징이 딱 겹치는 한 벌을 찾았습니다.<br>
결정적인 단서가 된 것은 <strong><span class="swl-marker mark_pink" style="font-size:1.15em;">아치형으로 늘어선 그레이의 「DIARY」 칼리지 로고, 어깨에서 소매로 이어지는 부분에 다른 원단을 이어 붙인 절개 패널, 드롭 숄더의 각진 빅 실루엣</span></strong> 이 3가지입니다.<br>
이것들은 모두 DIARY 1999가 전개하고 있는 「DIARY ARC CONSTRUCTED T-SHIRT」의 사양과 일치합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>「ARC(아치)」는 그대로 가슴 로고가 호를 그린 레이아웃을 가리키고, 「CONSTRUCTED」는 한 장의 원단이 아니라 여러 파츠를 꿰매어 입체적으로 조립한 만듦새를 뜻합니다.<br>
어깨 위치를 일부러 어긋나게 하고 거기에 다른 원단을 이었기 때문에, 입으면 자연스럽게 몸에서 뜨는 듯한 볼륨이 생기는 것이 특징입니다.<br>
소재는 코튼 100%이고, 컬러는 블랙 외에도 전개가 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>다만 영상에 비치는 것만으로는, 이 티셔츠가 KOSUKE 본인의 사복인지, 촬영용으로 준비된 것인지까지는 알 수 없습니다.<br>
여기서는 「KOSUKE가 영상에서 입고 있던 티셔츠와 같은 브랜드・같은 디자인의 아이템」이라는 전제로 소개합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">DIARY 1999(다이어리 1999)는 어떤 브랜드?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>DIARY 1999(다이어리 1999)는 디자이너 마일스 헨리크 홀이 전개하는 스트리트 브랜드입니다.<br>
홀은 인기 브랜드 1017 ALYX 9SM의 창립자이자 지방시의 전 크리에이티브 디렉터이기도 한 매튜 M. 윌리엄스 밑에서 경험을 쌓은 인물로, 이후 파리 패션위크에서 자신의 브랜드로서 DIARY 1999를 시작했습니다.<br>
「for the youth, by the youth(젊은 세대를 위해, 젊은 세대의 손으로)」를 내걸고, 젊은 세대의 문화와 커뮤니티에 뿌리를 둔 만들기를 표방하는 것이 특징입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>디자인 면에서는, 영국 노동자 계급의 무드와 스트리트 컬처를 섞은 세계관이 축이 되고 있습니다.<br>
칼리지 로고나 아치형 레터링, 일부러 거칠게 보이는 가공과 절개 등, 어딘가 향수를 불러일으키는 미국 빈티지풍 요소를 요즘 감각으로 재구성한 아이템이 많습니다.<br>
일본에서는 NUBIAN(누비안) 등의 셀렉트숍이 취급하고 있고, 한국의 아이돌이나 래퍼가 입은 모습도 종종 화제가 됩니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">티셔츠 가격은? 국내에서는 약 3만 6천 엔</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>DIARY ARC CONSTRUCTED T-SHIRT는 일본 국내 셀렉트숍에서의 참고 가격이 <strong><span class="swl-marker mark_pink" style="font-size:1.15em;">3만 6300엔(세금 포함)</span></strong>입니다.<br>
하이 브랜드는 아니지만, 디자이너스 스트리트 브랜드답게 티셔츠치고는 높은 가격대에 해당합니다.<br>
사이즈는 XS・S・L・XL 전개이고, 총장은 61〜67.5cm 정도, 가슴 너비도 55〜61.5cm로 넉넉한 치수입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>DIARY 1999의 공식 온라인 스토어(diary1999.com)에서는 같은 모델이 210달러 안팎(1달러 150엔 환산으로 약 3만 1000엔)에 게재되어 있었지만, 확인한 시점에는 품절 표시였습니다.<br>
인기 컬러・인기 사이즈는 회전이 빠르기 때문에, 재고를 발견하면 빨리 잡는 것이 무난합니다.<br>
도저히 찾을 수 없는 경우에는, 같은 「아치 로고・절개 패널・빅 실루엣」 조건으로 해외 통판이나 빈티지를 찾으면 비슷한 것에 도달할 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AL};color:#fff;">DIARY ARC CONSTRUCTED T-SHIRT 구입처</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>ADDICTED(어딕티드)・NUBIAN(누비안) 등 한국・일본 셀렉트숍의 온라인 스토어／매장</li>
<li>ANSWER(answerclothing.com) 등 일본 국내 셀렉트숍 통판</li>
<li>DIARY 1999 공식 온라인 스토어(diary1999.com／해외 배송・재고는 유동적)</li>
<li>Slam Jam 등 해외 배송에 대응하는 통판</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">정리</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:2px solid {AL};border-radius:8px;background:rgba(192,71,61,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; KOSUKE가 2026년 8월 29일경 게시된 공식 인스타그램 릴스에서 입고 있던 검은 프린트 티셔츠<br>
&#10003; DIARY 1999(다이어리 1999)의 「DIARY ARC CONSTRUCTED T-SHIRT」로 보임<br>
&#10003; 포인트는 가슴의 아치형 「DIARY」 칼리지 로고・어깨 절개 패널・각진 빅 실루엣<br>
&#10003; 소재는 코튼 100%, 컬러는 블랙 등을 전개<br>
&#10003; 일본 국내 참고 가격은 3만 6300엔(세금 포함), 공식 스토어 표기는 210달러 안팎(약 3만 1000엔)
</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>꽃무늬 긴팔 티나 허리에 두른 셔츠와 매치한 레이어드는, DIARY 1999가 지닌 빈티지한 무드와 잘 어울려서, 가지고 있는 옷으로도 따라 하기 쉬운 스타일입니다.<br>
KOSUKE는 지금까지도 사복 센스가 주목받아 온 만큼, 다음 릴스나 오프숏에서 어떤 아이템을 보여줄지도 기대되네요!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">관련 기사</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{PROFILE_KR}" target="_blank" rel="noopener">KOSUKE(테루이 코스케)의 프로필을 정리한 기사</a></li>
<li><a href="{HAIRMILK_JP}" target="_blank" rel="noopener">KOSUKE가 애용하는 헤어 밀크 브랜드를 조사한 기사(일본어)</a></li>
<li><a href="{SHOESIZE_JP}" target="_blank" rel="noopener">KO1KEYZ 멤버 12명의 신발 사이즈를 조사한 기사(일본어)</a></li>
</ul>
</div>
<!-- /wp:html -->"""

print("KR len(content):", plain_len(KR_CONTENT), "| len(title):", len(kr_title))
kr_eye_id = make_eyecatch(
    "KOSUKE가 릴스에서 입은 티셔츠는?", "DIARY 1999", "3만 6300엔 블랙 티로 판명!",
    "kosuke_diary1999_tshirt_eyecatch_kr.png", seed=JP_ID, lang="kr",
)
print("KR eyecatch media id:", kr_eye_id)
kr_summary = ("KO1KEYZ의 KOSUKE가 공식 인스타그램 릴스에서 입은 검은 프린트 티셔츠는 영국 스트리트 브랜드 "
              "DIARY 1999의 「DIARY ARC CONSTRUCTED T-SHIRT」로 보입니다. 일본 국내 참고 가격은 3만 6300엔. "
              "브랜드의 배경과 구입처도 정리했습니다.")
kr_post = post_new(kr_title, KR_CONTENT, jp_post["slug"] + "-kr", [74, 78], kr_summary, kr_eye_id, lang="ko", ja_id=JP_ID)
print("KR_POST_ID:", kr_post["id"], "| slug:", kr_post["slug"], "| preview:", f"{WP_URL}/?p={kr_post['id']}")

# ============================ ENGLISH ============================
en_title = "Which Brand Is KOSUKE's Reel T-Shirt? It's DIARY 1999"

EN_CONTENT = f"""<!-- wp:paragraph -->
<p>KOSUKE of KO1KEYZ wore a black tee with a large "DIARY" print across the chest in a reel posted around August 29, 2026 to the group's official Instagram (@ko1keyzofficial), and fans have been asking which brand it is.<br>
The short answer: it appears to be the <strong>"DIARY ARC CONSTRUCTED T-SHIRT" from DIARY 1999</strong>, with a reference price in Japan of <strong><span class="swl-marker mark_pink" style="font-size:1.15em;">36,300 yen (tax included)</span></strong>.<br>
This article walks through the reel itself, the details of the tee, the DIARY 1999 label, and where you can buy it.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">KOSUKE's T-Shirt at a Glance</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:35%;">Brand</td><td style="border:1px solid #ccc;padding:8px 12px;">DIARY 1999 (UK-born streetwear label)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Item</td><td style="border:1px solid #ccc;padding:8px 12px;">DIARY ARC CONSTRUCTED T-SHIRT (black, short sleeve)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Tell-tale details</td><td style="border:1px solid #ccc;padding:8px 12px;">Arched "DIARY" collegiate logo on the chest, paneled shoulders, boxy oversized fit</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Material</td><td style="border:1px solid #ccc;padding:8px 12px;">100% cotton</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Reference price</td><td style="border:1px solid #ccc;padding:8px 12px;">36,300 yen incl. tax (Japanese select shops)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Where seen</td><td style="border:1px solid #ccc;padding:8px 12px;">KO1KEYZ official Instagram reel posted around Aug 29, 2026 (KOSUKE solo)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AL};color:#fff;">What you'll learn</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>The reel and scene where KOSUKE wore the tee</li>
<li>The brand and the item name</li>
<li>Background on DIARY 1999</li>
<li>The reference price and where to buy it</li>
<li>Whether it is his own clothing</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Which reel was KOSUKE wearing this T-shirt in?</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #ddd;border-left:4px solid {AL2};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>Scene:</strong> A solo reel of KOSUKE posted around August 29, 2026 to KO1KEYZ's official Instagram. It is a vertical short clip filmed on what looks like a building rooftop, with KOSUKE doing a brief dance and a hand sign to the camera.</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>KO1KEYZ's official Instagram has been rolling out solo reels for each member, and KOSUKE's turn was a few seconds of dancing shot on a rooftop-like spot.<br>
He sways to the hook and finishes by looking into the camera with a hand sign shaped a little like the letter L, in a short and snappy clip.<br>
The focus is KOSUKE's expression and dancing, but plenty of fans wanted to know where the black tee was from, and posts hunting for the brand showed up on X and in the comments.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>In the clip, KOSUKE layers the black print tee over a long-sleeve top with an all-over floral-style pattern, with a khaki shirt tied around his waist.<br>
His bottoms are wide khaki-toned trousers, and he wears a thin silver necklace with a key charm plus several slim silver rings stacked on his fingers.<br>
The whole look is loose and relaxed in fit, reading as street-leaning everyday clothes.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>The part that stands out most is the big "DIARY" lettering across the chest.<br>
It is a collegiate-style logo laid out in an arc, printed in grey.<br>
Using the shape and typeface of that logo, plus the paneled construction around the shoulders, we looked into which brand and which item it is.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">KOSUKE's tee is the DIARY 1999 "ARC CONSTRUCTED T-SHIRT"</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Lined up against items on sale, one piece matches point for point.<br>
The clinchers are <strong><span class="swl-marker mark_pink" style="font-size:1.15em;">the grey "DIARY" collegiate logo set in an arc, the panels of contrast fabric pieced in from the shoulder down the sleeve, and the drop-shoulder, boxy oversized cut</span></strong>.<br>
All of these line up with the specs of the "DIARY ARC CONSTRUCTED T-SHIRT" that DIARY 1999 sells.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>"ARC" refers to the arched layout of the chest logo, while "CONSTRUCTED" means the body is built from several panels sewn together for a three-dimensional shape rather than cut from a single piece.<br>
Because the shoulder seams are deliberately dropped and joined with separate fabric, the tee sits away from the body with a bit of volume when worn.<br>
The material is 100% cotton, and it comes in colors other than black as well.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>That said, from the video alone there is no way to tell whether the tee is KOSUKE's own or something prepared for the shoot.<br>
Here we cover it as "the same brand and same design as the T-shirt KOSUKE wore in the reel."</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What kind of brand is DIARY 1999?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>DIARY 1999 is a streetwear label from designer Myles Henrik Hall.<br>
Hall trained under Matthew M. Williams, the founder of 1017 ALYX 9SM and a former creative director of Givenchy, and later launched DIARY 1999 as his own label during Paris Fashion Week.<br>
Its motto is "for the youth, by the youth," and it leans into making clothes rooted in young people's culture and communities.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>On the design side, the label mixes the mood of the British working class with street culture.<br>
Collegiate logos, arched lettering, and intentionally rough-looking finishes and paneling give many pieces a nostalgic, American-vintage feel rebuilt in a current way.<br>
In Japan it is carried by select shops such as NUBIAN, and Korean idols and rappers are often seen wearing it too.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How much is the tee? Around 36,000 yen in Japan</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The DIARY ARC CONSTRUCTED T-SHIRT has a reference price at Japanese select shops of <strong><span class="swl-marker mark_pink" style="font-size:1.15em;">36,300 yen (tax included)</span></strong>.<br>
It is not a luxury house, but as a designer streetwear label it still sits at the high end for a T-shirt.<br>
Sizes run XS, S, L and XL, with body lengths of roughly 61-67.5cm and chest widths of 55-61.5cm, so the fit is generous.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>On the DIARY 1999 official online store (diary1999.com), the same model was listed at around 210 US dollars (roughly 31,000 yen at 150 yen to the dollar), but it showed as sold out when we checked.<br>
Popular colors and sizes move quickly, so grabbing one when you find stock is the safe move.<br>
If you cannot track it down, searching overseas retailers or the secondhand market for the same "arc logo, paneled, oversized" combination will get you close.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AL};color:#fff;">Where to buy the DIARY ARC CONSTRUCTED T-SHIRT</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>Select shops such as ANSWER (answerclothing.com) and NUBIAN, online and in store</li>
<li>DIARY 1999 official online store (diary1999.com; ships internationally, stock varies)</li>
<li>Slam Jam and other retailers that ship to Japan</li>
<li>Resale and vintage platforms if you are after a used one</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Summary</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:2px solid {AL};border-radius:8px;background:rgba(192,71,61,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; KOSUKE wore a black print tee in a KO1KEYZ official Instagram reel posted around Aug 29, 2026<br>
&#10003; It appears to be DIARY 1999's "DIARY ARC CONSTRUCTED T-SHIRT"<br>
&#10003; Key details: arched "DIARY" collegiate logo, paneled shoulders, boxy oversized cut<br>
&#10003; Material is 100% cotton, offered in black among other colors<br>
&#10003; Reference price in Japan is 36,300 yen incl. tax; the official store listed it at about 210 USD (~31,000 yen)
</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Layered with the floral long-sleeve and the shirt tied at the waist, the tee suits DIARY 1999's vintage-leaning mood and is an easy look to recreate with clothes you already own.<br>
KOSUKE's off-duty style has drawn attention before, so it will be fun to see what he pulls out in the next reel or off-shot.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">Related articles</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{PROFILE_JP}" target="_blank" rel="noopener">KOSUKE (Kosuke Terui) profile (in Japanese)</a></li>
<li><a href="{HAIRMILK_JP}" target="_blank" rel="noopener">The hair milk brand KOSUKE uses (in Japanese)</a></li>
<li><a href="{SHOESIZE_JP}" target="_blank" rel="noopener">Shoe sizes of all 12 KO1KEYZ members (in Japanese)</a></li>
</ul>
</div>
<!-- /wp:html -->"""

print("EN len(content):", plain_len(EN_CONTENT), "| len(title):", len(en_title))
en_summary = ("The black DIARY-print tee KOSUKE of KO1KEYZ wore in an official Instagram reel appears to be "
              "the DIARY ARC CONSTRUCTED T-SHIRT from UK streetwear label DIARY 1999. Reference price in Japan "
              "is 36,300 yen. We cover the brand's background and where to buy it.")
en_post = post_new(en_title, EN_CONTENT, jp_post["slug"] + "-en", [110, 112], en_summary, jp_eye_id, lang="en", ja_id=JP_ID)
print("EN_POST_ID:", en_post["id"], "| slug:", en_post["slug"], "| preview:", f"{WP_URL}/?p={en_post['id']}")

(ROOT / "tmp_kosuke_diary1999_ids.txt").write_text(
    f"jp={JP_ID} slug={jp_post['slug']} jp_eyecatch={jp_eye_id}\n"
    f"kr={kr_post['id']} slug={kr_post['slug']} kr_eyecatch={kr_eye_id}\n"
    f"en={en_post['id']} slug={en_post['slug']} en_eyecatch={jp_eye_id}\n",
    encoding="utf-8")
print("\nDONE.")
print("JP edit:", f"{WP_URL}/wp-admin/post.php?post={JP_ID}&action=edit")
