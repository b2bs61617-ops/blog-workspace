# -*- coding: utf-8 -*-
"""KOSUKE(照井康祐) スタバの推しドリンク記事: JP + KR + EN 下書き投稿。
ソース: ヨントン(2026-09-23実施)でのファンとのやり取り(X投稿 https://x.com/SFWhQ4SqDE67110/status/2102653362718310549)。
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

FALLBACK_SLUG = "kosuke-starbucks-order-yontong"

# KOSUKEのメンバーカラー(赤)に寄せたパステル配色
ACCENT = "#d94f4f"
AB = "#efc9c4"
BG = "#fdf3f1"

# 内部リンク
PROFILE_JP = "https://chomoand-1.com/teruikosuke_profile-106"
PROFILE_KR = "https://chomoand-1.com/ko/teruikosuke_profile-kr-10623"
HAIRMILK_JP = "https://chomoand-1.com/ko1keyz-kosukes-hair-milk-reve-11136"
MEMBERCOLOR_JP = "https://chomoand-1.com/ko1keyz-no-color-10196"
MEMBERCOLOR_KR = "https://chomoand-1.com/ko/ko1keyz-no-color-kr-10749"
PROFILE_ALL_JP = "https://chomoand-1.com/profile-12-9725"
PROFILE_ALL_KR = "https://chomoand-1.com/ko/profile-12-kr-10734"


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


def p(sentences):
    body = "<br>\n".join(sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def capbox(ttl, rows):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;white-space:nowrap;">{k}</td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{ttl}</p>
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>''')


def summarybox(ttl, checklist, closing):
    items = "<br>\n".join(f"&#10003; {t}" for t in checklist)
    return wphtml(f'''<div style="border:2px solid {ACCENT};border-radius:8px;background:rgba(217,79,79,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{ttl}</p>
<p style="margin:0 0 10px 0;">{items}</p>
<p style="margin:0;">{closing}</p>
</div>''')


def linksbox(ttl, items):
    lis = "\n".join(f'<li><a href="{href}" target="_blank" rel="noopener">{text}</a></li>' for text, href in items)
    return wphtml(f'''<div style="border:1px solid {AB};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{ttl}</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


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


def make_eyecatch(top, main, bottoms, out_name, seed, lang=None):
    out = ROOT / "images" / out_name
    cmd = [sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
           "--top", top, "--main", main]
    for b in bottoms:
        cmd += ["--bottom", b]
    cmd += ["--out", str(out), "--seed", str(seed)]
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
TITLE = "【KO1KEYZ】KOSUKEの推しスタバは？定番オーダーと今ハマり中の一杯"

blocks = []

blocks.append(p([
    "KO1KEYZの照井康祐(KOSUKE)が、2026年9月23日に行われたヨントン(ビデオ通話でファンと直接話せる交流イベント)で、スタバでよく頼むドリンクについて聞かれる場面がありました。",
    "気になって調べてみたところ、照井は普段からよく飲む定番の2杯に加えて、今いちばんお気に入りだという一杯まで教えてくれていたことが分かりました。",
    "この記事では、照井が挙げたドリンクの正体と、実際に頼めるお店での価格・販売状況を詳しくまとめます。",
]))

blocks.append(h2("ヨントンで語られたスタバの話題"))
blocks.append(capbox("ヨントンの概要", [
    ("実施日", "2026年9月23日"),
    ("形式", "ビデオ通話形式のファン交流イベント「ヨントン」"),
    ("話題", "スタバでよく飲むドリンクについての質問への回答"),
]))
blocks.append(p([
    "照井は、普段よく飲むドリンクとして<strong>抹茶フラペチーノ</strong>と<strong>ほうじ茶クラシックティーラテ</strong>の2つを挙げ、そのうえで「今はお芋のやつが好き」と、現在お気に入りの一杯があることも明かしています。",
    "定番2種類だけでなく、旬の新作らしき一杯まで教えてくれる、ファンにとってはうれしい回答になりました。",
]))

blocks.append(h2("照井康祐(KOSUKE)はどんな人？"))
blocks.append(capbox("KOSUKEのプロフィール", [
    ("本名", "照井康祐(てるい こうすけ)"),
    ("生年月日", "2007年12月2日"),
    ("出身地", "千葉県"),
    ("身長", "174cm"),
    ("MBTI", "ISTP"),
    ("メンバーカラー", "赤"),
    ("日プでの成績", "『PRODUCE 101 JAPAN 新世界』最終順位11位(381,605票)、初回評価Cクラスからの逆転デビュー"),
]))
blocks.append(p([
    "ダンス実力派のイメージが強い照井ですが、今回のようにスタバの好みを聞かれてすぐ答えてくれるところからは、素顔の親しみやすさも伝わってきます。",
    "プロフィールをより詳しく知りたい人は、過去に書いた<a href=\"" + PROFILE_JP + "\" target=\"_blank\" rel=\"noopener\">照井康祐のプロフィール記事</a>もあわせてチェックしてみてください。",
]))

blocks.append(h2("定番オーダーは「抹茶 クリーム フラペチーノ」と「ほうじ茶 & クラシックティー ラテ」"))
blocks.append(p([
    "照井が定番として挙げた1杯目は、スターバックスの通年メニューにある<strong>抹茶 クリーム フラペチーノ</strong>です。",
    "抹茶パウダーをブレンドしたクリームベースのフラペチーノで、ミルクと氷でさっぱりとした飲み口に仕上げているのが特徴です。",
]))
blocks.append(p([
    "もう1杯は<strong>ほうじ茶 & クラシックティー ラテ</strong>です。",
    "ほうじ茶と紅茶を合わせたすっきりとした味わいに、クリーミーな甘さが溶け合う一杯で、2024年6月に定番商品として復活して以来、通年で飲めるメニューになっています。",
]))
blocks.append(capbox("定番2杯の価格(Tallサイズ)", [
    ("抹茶 クリーム フラペチーノ", "税込595円(店内利用)"),
    ("ほうじ茶 & クラシックティー ラテ", "税込570円(店内利用)"),
]))

blocks.append(h2("今ハマっているのは秋の「蜜芋」シリーズ？"))
blocks.append(p([
    "照井が「今はお芋のやつが好き」と話していたタイミングは、ちょうどスターバックスで秋のさつまいもメニューが出そろった時期と重なります。",
    "どの商品を指しているかまでは明言されていませんが、ヨントンが行われた2026年9月23日時点で販売されている「お芋」系のドリンクは次の3つです。",
]))
blocks.append(capbox("2026年9月発売の「蜜芋」シリーズ", [
    ("とろり蜜芋 紅はるか フラペチーノ", "2026年9月2日発売、Tallサイズ税込687円(持ち帰り)/700円(店内利用)"),
    ("とろり蜜芋 紅はるか ムース ティー ラテ", "2026年9月2日発売"),
    ("蜜芋 ミルク", "2026年9月18日発売、Tallサイズ税込618円(持ち帰り)/630円(店内利用)"),
]))
blocks.append(p([
    "なかでも「とろり蜜芋 紅はるか フラペチーノ」は、国産の紅はるかを使ったなめらかな蜜芋ペーストに、香ばしい焼き芋風味のソースを重ねた一杯で、ヨントンの時点ですでに発売から3週間ほど経っていた定番格の存在でした。",
    "照井が挙げた「お芋のやつ」は、この秋限定の蜜芋シリーズのいずれかを指している可能性が高そうです。",
    "なくなり次第終了の季節限定メニューなので、気になる人は早めにチェックしておくのがおすすめです。",
]))
blocks.append(capbox("購入先", [
    ("販売店舗", "全国のスターバックス店舗(一部店舗を除く)"),
    ("注文方法", "店頭注文のほか、Starbucks公式アプリのモバイルオーダーにも対応"),
]))

blocks.append(h2("まとめ"))
blocks.append(summarybox(
    "KOSUKEのスタバオーダーまとめ",
    [
        "定番は「抹茶 クリーム フラペチーノ」と「ほうじ茶 & クラシックティー ラテ」の2杯",
        "今お気に入りなのは「お芋のやつ」、2026年秋の蜜芋シリーズを指しているとみられる",
        "情報の出どころは2026年9月23日実施のヨントンでのやり取り",
        "蜜芋シリーズは9月2日・18日発売でいずれも季節限定、なくなり次第終了",
    ],
    "普段何気なく頼んでいるドリンクと同じものを、照井も飲んでいるかもしれないと思うと親近感がわいてきますね。<br>気になった人は、次にスタバに行ったときぜひ試してみてはいかがでしょうか!",
))
blocks.append(linksbox("あわせて読みたい", [
    ("照井康祐(KOSUKE)のプロフィールを詳しく紹介した記事", PROFILE_JP),
    ("照井康祐が愛用するヘアミルクのブランドを特定した記事", HAIRMILK_JP),
    ("KO1KEYZメンバーカラーをまとめた記事", MEMBERCOLOR_JP),
    ("KO1KEYZメンバー全員のプロフィールを紹介した記事", PROFILE_ALL_JP),
]))

JP_CONTENT = "\n\n".join(blocks)
print("JP len(content):", plain_len(JP_CONTENT), "| len(title):", len(TITLE))

JP_SUMMARY = ("KO1KEYZの照井康祐(KOSUKE)がヨントンで明かしたスタバの定番オーダーは、"
              "抹茶クリームフラペチーノとほうじ茶&クラシックティーラテ。今ハマっているのは秋の蜜芋シリーズとみられ、"
              "価格・販売状況もまとめました。")

EXISTING_JP_ID = 13467
EXISTING_JP_SLUG = "ko1keyz-what-is-kosukes-favori"
EXISTING_JP_EYECATCH = 13466

if EXISTING_JP_ID:
    JP_ID = EXISTING_JP_ID
    jp_eye_id = EXISTING_JP_EYECATCH
    jp_post = {"id": JP_ID, "slug": EXISTING_JP_SLUG}
    print("reusing existing JP post:", JP_ID, EXISTING_JP_SLUG)
else:
    SLUG = get_slug(TITLE, FALLBACK_SLUG)
    print("JP SLUG:", SLUG)

    jp_eye_id = make_eyecatch(
        "KO1KEYZ", "KOSUKE",
        ["スタバの推しドリンクは?", "定番2杯+今ハマり中の1杯を告白!"],
        "kosuke_starbucks_order_eyecatch.png", seed=0,
    )
    print("JP eyecatch media id:", jp_eye_id)

    jp_post = post_new(TITLE, JP_CONTENT, SLUG, [66, 63, 102], JP_SUMMARY, jp_eye_id)
    JP_ID = jp_post["id"]
    print("JP_POST_ID:", JP_ID, "| slug:", jp_post["slug"], "| preview:", f"{WP_URL}/?p={JP_ID}")

# ============================ KOREAN ============================
KR_TITLE = "KO1KEYZ KOSUKE가 자주 마시는 스타벅스는? 단골 메뉴와 요즘 빠진 한 잔"

kr_blocks = []
kr_blocks.append(p([
    "KO1KEYZ의 KOSUKE(테루이 코스케)가 2026년 9월 23일에 진행된 영통(영상통화로 팬과 직접 이야기하는 교류 이벤트)에서, 스타벅스에서 자주 마시는 음료에 대한 질문을 받았습니다.",
    "찾아보니 KOSUKE는 평소 즐겨 마시는 단골 메뉴 두 잔에 더해, 요즘 가장 마음에 든다는 한 잔까지 알려준 것으로 확인됐습니다.",
    "이 기사에서는 KOSUKE가 언급한 음료의 정체와, 실제 매장에서 주문할 수 있는 가격・판매 상황을 자세히 정리합니다.",
]))

kr_blocks.append(h2("영통에서 나온 스타벅스 이야기"))
kr_blocks.append(capbox("영통 개요", [
    ("실시일", "2026년 9월 23일"),
    ("형식", "영상통화 형식의 팬 교류 이벤트 「영통」"),
    ("화제", "스타벅스에서 자주 마시는 음료에 대한 질문 답변"),
]))
kr_blocks.append(p([
    "KOSUKE는 평소 즐겨 마시는 음료로 <strong>말차 크림 프라푸치노</strong>와 <strong>호지차 & 클래식 티 라떼</strong> 두 가지를 꼽았고, 이어서 \"지금은 고구마 나오는 거 좋아해요\"라며 요즘 마음에 든 한 잔이 있다는 것도 밝혔습니다.",
    "단골 메뉴 두 가지뿐 아니라, 최근 나온 신메뉴로 보이는 음료까지 알려준 팬들에게는 반가운 답변이었습니다.",
]))

kr_blocks.append(h2("테루이 코스케(KOSUKE)는 어떤 사람?"))
kr_blocks.append(capbox("KOSUKE 프로필", [
    ("본명", "테루이 코스케(照井康祐)"),
    ("생년월일", "2007년 12월 2일"),
    ("출신지", "치바현"),
    ("키", "174cm"),
    ("MBTI", "ISTP"),
    ("멤버컬러", "빨강"),
    ("프로듀스101재팬 성적", "『PRODUCE 101 JAPAN 신세계』 최종순위 11위(381,605표), 첫 평가 C클래스에서 역전 데뷔"),
]))
kr_blocks.append(p([
    "댄스 실력파 이미지가 강한 KOSUKE지만, 이번처럼 스타벅스 취향을 물어보면 바로 대답해 주는 모습에서는 친근한 매력도 느껴집니다.",
    f"프로필을 더 자세히 알고 싶다면 <a href=\"{PROFILE_KR}\" target=\"_blank\" rel=\"noopener\">KOSUKE의 프로필을 정리한 기사</a>도 함께 확인해 보세요.",
]))

kr_blocks.append(h2("단골 메뉴는 「말차 크림 프라푸치노」와 「호지차 & 클래식 티 라떼」"))
kr_blocks.append(p([
    "KOSUKE가 단골로 꼽은 첫 번째 음료는 스타벅스의 상시 메뉴인 <strong>말차 크림 프라푸치노</strong>입니다.",
    "말차 파우더를 블렌드한 크림 베이스의 프라푸치노로, 우유와 얼음으로 산뜻하게 마무리한 것이 특징입니다.",
]))
kr_blocks.append(p([
    "두 번째는 <strong>호지차 & 클래식 티 라떼</strong>입니다.",
    "호지차와 홍차를 더한 깔끔한 맛에 크리미한 단맛이 어우러진 음료로, 2024년 6월 상시 메뉴로 부활한 이후 사계절 내내 즐길 수 있는 메뉴가 됐습니다.",
]))
kr_blocks.append(capbox("단골 2잔 가격(Tall 사이즈)", [
    ("말차 크림 프라푸치노", "세금 포함 595엔(매장 이용)"),
    ("호지차 & 클래식 티 라떼", "세금 포함 570엔(매장 이용)"),
]))

kr_blocks.append(h2("요즘 빠진 건 가을 한정 「꿀고구마」 시리즈?"))
kr_blocks.append(p([
    "KOSUKE가 \"지금은 고구마 나오는 거 좋아해요\"라고 말한 시점은, 마침 스타벅스에서 가을 고구마 메뉴가 전부 나온 시기와 겹칩니다.",
    "어떤 상품을 가리키는지 명확히 밝히지는 않았지만, 영통이 진행된 2026년 9월 23일 기준으로 판매 중인 '고구마' 계열 음료는 다음 3가지입니다.",
]))
kr_blocks.append(capbox("2026년 9월 발매 「꿀고구마」 시리즈", [
    ("토로리 꿀고구마 베니하루카 프라푸치노", "2026년 9월 2일 발매, Tall 사이즈 세금 포함 687엔(테이크아웃)/700엔(매장)"),
    ("토로리 꿀고구마 베니하루카 무스 티 라떼", "2026년 9월 2일 발매"),
    ("꿀고구마 밀크", "2026년 9월 18일 발매, Tall 세금 포함 618엔(테이크아웃)/630엔(매장)"),
]))
kr_blocks.append(p([
    "그중에서도 「토로리 꿀고구마 베니하루카 프라푸치노」는 국산 베니하루카를 사용한 부드러운 꿀고구마 페이스트에, 고소한 군고구마 풍미 소스를 더한 음료로, 영통 시점에는 이미 발매된 지 3주 정도 지난 인기 메뉴였습니다.",
    "KOSUKE가 말한 \"고구마 나오는 거\"는 이 가을 한정 꿀고구마 시리즈 중 하나를 가리킬 가능성이 높아 보입니다.",
    "소진되면 종료되는 계절 한정 메뉴인 만큼, 관심 있는 분들은 서둘러 확인해 보는 것을 추천합니다.",
]))
kr_blocks.append(capbox("구입처", [
    ("판매 매장", "전국 스타벅스 매장(일부 매장 제외)"),
    ("주문 방법", "매장 주문 외에 스타벅스 공식 앱의 모바일 오더도 가능"),
]))

kr_blocks.append(h2("정리"))
kr_blocks.append(summarybox(
    "KOSUKE의 스타벅스 오더 정리",
    [
        "단골 메뉴는 「말차 크림 프라푸치노」와 「호지차 & 클래식 티 라떼」 두 잔",
        "요즘 마음에 든 건 \"고구마 나오는 거\", 2026년 가을 꿀고구마 시리즈를 가리키는 것으로 보임",
        "정보 출처는 2026년 9월 23일에 진행된 영통에서의 대화",
        "꿀고구마 시리즈는 9월 2일・18일 발매로 모두 계절 한정, 소진되면 종료",
    ],
    "평소 무심코 주문하던 음료를 KOSUKE도 똑같이 마시고 있을지도 모른다고 생각하면 왠지 친근하게 느껴지네요.<br>궁금하다면 다음에 스타벅스에 갔을 때 한번 시도해 보는 건 어떨까요!",
))
kr_blocks.append(linksbox("함께 보면 좋은 기사", [
    ("KOSUKE(테루이 코스케)의 프로필을 정리한 기사", PROFILE_KR),
    ("KOSUKE가 애용하는 헤어 밀크 브랜드를 조사한 기사(일본어)", HAIRMILK_JP),
    ("KO1KEYZ 멤버컬러를 정리한 기사", MEMBERCOLOR_KR),
    ("KO1KEYZ 멤버 12명의 프로필을 소개한 기사", PROFILE_ALL_KR),
]))

KR_CONTENT = "\n\n".join(kr_blocks)
print("KR len(content):", plain_len(KR_CONTENT), "| len(title):", len(KR_TITLE))

kr_summary = ("KO1KEYZ의 KOSUKE가 영통에서 밝힌 스타벅스 단골 메뉴는 말차 크림 프라푸치노와 호지차 & 클래식 티 라떼. "
              "요즘 마음에 든 건 가을 꿀고구마 시리즈로 보이며, 가격・판매 상황도 정리했습니다.")

kr_eye_id = make_eyecatch(
    "KO1KEYZ", "KOSUKE",
    ["즐겨 마시는 스타벅스는?", "단골 2잔+요즘 빠진 한 잔을 공개!"],
    "kosuke_starbucks_order_eyecatch_kr.png", seed=JP_ID, lang="kr",
)
print("KR eyecatch media id:", kr_eye_id)

kr_post = post_new(KR_TITLE, KR_CONTENT, jp_post["slug"] + "-kr", [74, 78], kr_summary, kr_eye_id, lang="ko", ja_id=JP_ID)
print("KR_POST_ID:", kr_post["id"], "| slug:", kr_post["slug"], "| preview:", f"{WP_URL}/?p={kr_post['id']}")

# ============================ ENGLISH ============================
EN_TITLE = "What Starbucks Drinks Does KOSUKE Order? His Go-To Picks and Current Favorite"

en_blocks = []
en_blocks.append(p([
    "KOSUKE of KO1KEYZ (Kosuke Terui) fielded a question about his go-to Starbucks order during a yeontong (a video-call fan meeting) held on September 23, 2026.",
    "Digging into it, we found that he named two drinks he regularly orders, plus one more he says he is currently into.",
    "This article breaks down what those drinks actually are, along with their prices and availability at Starbucks Japan.",
]))

en_blocks.append(h2("What came up during the yeontong"))
en_blocks.append(capbox("Event info", [
    ("Date", "September 23, 2026"),
    ("Format", "Video-call fan event (\"yeontong\")"),
    ("Topic", "A fan question about his regular Starbucks order"),
]))
en_blocks.append(p([
    "KOSUKE named the <strong>Matcha Cream Frappuccino</strong> and the <strong>Hojicha & Classic Tea Latte</strong> as the two drinks he usually orders, then added that he is \"into the sweet potato one\" right now.",
    "Along with his two regulars, he pointed fans toward what sounds like a newer seasonal pick too.",
]))

en_blocks.append(h2("Who is KOSUKE?"))
en_blocks.append(capbox("KOSUKE's profile", [
    ("Real name", "Kosuke Terui"),
    ("Birthday", "December 2, 2007"),
    ("Hometown", "Chiba Prefecture"),
    ("Height", "174cm"),
    ("MBTI", "ISTP"),
    ("Member color", "Red"),
    ("Produce 101 Japan result", "Finished 11th (381,605 votes) on PRODUCE 101 JAPAN: THE NEW WORLD, coming back from a Class C first evaluation to debut"),
]))
en_blocks.append(p([
    "KOSUKE is known for his dance skills, but answering a casual coffee-order question so readily also shows a more approachable side of him.",
    f"For more on his background, see our <a href=\"{PROFILE_JP}\" target=\"_blank\" rel=\"noopener\">KOSUKE profile article (in Japanese)</a>.",
]))

en_blocks.append(h2("His regulars: Matcha Cream Frappuccino and Hojicha & Classic Tea Latte"))
en_blocks.append(p([
    "The first drink KOSUKE named is the <strong>Matcha Cream Frappuccino</strong>, a year-round item on the Starbucks Japan menu.",
    "It blends matcha powder into a cream-based Frappuccino, finished with milk and ice for a light, refreshing taste.",
]))
en_blocks.append(p([
    "The second is the <strong>Hojicha & Classic Tea Latte</strong>.",
    "It mixes hojicha (roasted green tea) with black tea for a clean flavor rounded out with creamy sweetness, and has been on the year-round menu since it returned as a regular item in June 2024.",
]))
en_blocks.append(capbox("Regular menu prices (Tall)", [
    ("Matcha Cream Frappuccino", "595 yen tax included (in-store)"),
    ("Hojicha & Classic Tea Latte", "570 yen tax included (in-store)"),
]))

en_blocks.append(h2("Is his current favorite the fall \"honey sweet potato\" lineup?"))
en_blocks.append(p([
    "The timing of KOSUKE saying he is \"into the sweet potato one\" lines up with when Starbucks Japan's full fall sweet-potato lineup had just rolled out.",
    "He did not specify exactly which item, but as of September 23, 2026 (when the yeontong took place), three sweet-potato drinks were on sale.",
]))
en_blocks.append(capbox("Sweet-potato drinks on sale in September 2026", [
    ("Toron Mitsuimo Beniharuka Frappuccino", "Released Sept 2, 2026; Tall 687 yen to-go / 700 yen in-store, tax included"),
    ("Toron Mitsuimo Beniharuka Mousse Tea Latte", "Released Sept 2, 2026"),
    ("Mitsuimo Milk", "Released Sept 18, 2026; Tall 618 yen to-go / 630 yen in-store, tax included"),
]))
en_blocks.append(p([
    "The Toron Mitsuimo Beniharuka Frappuccino in particular pairs a smooth honey sweet-potato paste made from domestic Beniharuka potatoes with a roasted-sweet-potato-style sauce, and had already been on sale for about three weeks by the time of the yeontong, making it something of a fall staple.",
    "KOSUKE's \"sweet potato one\" most likely refers to one of these seasonal drinks.",
    "They are limited-time items that end once stock runs out, so it is worth checking them out sooner rather than later.",
]))
en_blocks.append(capbox("Where to get it", [
    ("Locations", "Starbucks stores nationwide (excluding some locations)"),
    ("Ordering", "In-store, or via mobile order on the Starbucks Japan app"),
]))

en_blocks.append(h2("Summary"))
en_blocks.append(summarybox(
    "KOSUKE's Starbucks order, summarized",
    [
        "His regulars are the Matcha Cream Frappuccino and the Hojicha & Classic Tea Latte",
        "His current favorite, \"the sweet potato one,\" likely points to the fall 2026 honey sweet-potato lineup",
        "The information comes from a yeontong held on September 23, 2026",
        "The honey sweet-potato drinks released Sept 2 and Sept 18 are both seasonal, ending once stock runs out",
    ],
    "It's a fun thought that KOSUKE might be ordering the exact same drink you usually get.<br>Next time you're at Starbucks, why not give one of these a try!",
))
en_blocks.append(linksbox("Related articles", [
    ("KOSUKE (Kosuke Terui) profile (in Japanese)", PROFILE_JP),
    ("The hair milk brand KOSUKE uses (in Japanese)", HAIRMILK_JP),
    ("KO1KEYZ member colors, explained (in Japanese)", MEMBERCOLOR_JP),
    ("Profiles of all 12 KO1KEYZ members (in Japanese)", PROFILE_ALL_JP),
]))

EN_CONTENT = "\n\n".join(en_blocks)
print("EN len(content):", plain_len(EN_CONTENT), "| len(title):", len(EN_TITLE))

en_summary = ("KO1KEYZ's KOSUKE named his go-to Starbucks order during a video-call fan event: the Matcha Cream "
              "Frappuccino and the Hojicha & Classic Tea Latte. His current favorite appears to be the fall honey "
              "sweet-potato lineup. We cover prices and availability too.")

en_post = post_new(EN_TITLE, EN_CONTENT, jp_post["slug"] + "-en", [110, 118], en_summary, jp_eye_id, lang="en", ja_id=JP_ID)
print("EN_POST_ID:", en_post["id"], "| slug:", en_post["slug"], "| preview:", f"{WP_URL}/?p={en_post['id']}")

(ROOT / "tmp_kosuke_starbucks_order_ids.txt").write_text(
    f"jp={JP_ID} slug={jp_post['slug']} jp_eyecatch={jp_eye_id}\n"
    f"kr={kr_post['id']} slug={kr_post['slug']} kr_eyecatch={kr_eye_id}\n"
    f"en={en_post['id']} slug={en_post['slug']} en_eyecatch={jp_eye_id}\n",
    encoding="utf-8")

print("\nALL DONE.")
