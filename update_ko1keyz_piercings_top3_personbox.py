# -*- coding: utf-8 -*-
"""TOP3(TOWA/DAIKI/KOSUKE)と「2つずつ」(RYUJI/KEITO/YOSHIKI/YUKI)の各メンバーを
1人ずつ細い線のpersonboxで囲む。あわせて「2つずつ」ミニボックスに改行を追加。JP/KR/EN。"""
import base64, json, os
from pathlib import Path

import requests

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f'{ENV["WP_KOIKEYS_USERNAME"]}:{ENV["WP_KOIKEYS_APP_PASSWORD"]}'.encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}

BORDER = "#ded9d2"
ACCENT = "#8a8378"


def box(name, body):
    return (
        "<!-- wp:html -->\n"
        f'<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;color:{ACCENT};">{name}</p>\n'
        f'<p style="margin:0;">{body}</p>\n'
        "</div>\n"
        "<!-- /wp:html -->"
    )


def para(html):
    return f"<!-- wp:paragraph -->\n<p>{html}</p>\n<!-- /wp:paragraph -->"


# ---- bodies ----
JP_B = {
 "TOWA": '左耳に3つ、右耳に2つ。<br>\n耳たぶだけでなく軟骨にもホールがあり、12人の中では唯一の5つ持ちです。<br>\n自撮りのオフショットではシルバーの小ぶりなスタッドやフープを着けていることが多く、指のリングやチェーンネックレスとあわせてシルバーで統一するのがTOWA流のスタイルになっています。',
 "DAIKI": '左右2つずつの合計4つ。<br>\n本人も「ピアスを増やしたい」と公言しており、今後さらに増える可能性があります。<br>\n7月中旬の私服では、ピアスと服の色をYOSHIKIとのケミ名<a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">「デカ猫」</a>にちなんだ緑系でさりげなく揃えていたこともありました。',
 "KOSUKE": '右耳1つ・左耳2つの合計3つ。<br>\nデビューシングルのアーティスト写真で着けていたのは<strong><span class="swl-marker mark_pink">星モチーフのピアス</span></strong>で、ファンの間では「星のピアス」と呼ばれるほど印象的なアイテムです。<br>\nメンバーカラーの赤とあわせて、KOSUKEの<a href="https://chomoand-1.com/summary-of-ko1keyz-member-emoj-10560" target="_blank" rel="noopener">メンバー絵文字も星(🌟)</a>なので、この星ピアスはトレードマークとして定着しつつあります。',
 "RYUJI": 'デビューシングルのアー写ではピアスとイヤーカフを重ね付けしており、耳元のアクセサリー使いが目立つメンバーです。<br>\n時期によってシルバーからゴールドへ変えるなど付け替えも多く、オフショットではピアスを外している日もあるなど、耳元の変化はこまめにあります。',
 "KEITO": '左右1つずつの2つで、装飾控えめのシルバースタッドが中心です。',
 "YOSHIKI": '左右1つずつと見られますが、右耳のホールは写真での確認が難しく、はっきり分かるのは1つです。',
 "YUKI": '左右1つずつの2つで、2026年8月ごろの写真でもピアスを着けている様子が確認できます。',
}
JP_N = {"TOWA": "TOWA(濱田永遠)", "DAIKI": "DAIKI(加藤大樹)", "KOSUKE": "KOSUKE(照井康祐)",
        "RYUJI": "RYUJI(杉山竜司)", "KEITO": "KEITO(小野慶人)", "YOSHIKI": "YOSHIKI(矢田佳暉)", "YUKI": "YUKI(後藤結)"}

KR_B = {
 "TOWA": '왼쪽 귀에 3개, 오른쪽 귀에 2개.<br>\n귓불뿐 아니라 연골에도 구멍이 있어, 12명 중 유일한 5개 보유자예요.<br>\n셀카 오프숏에서는 실버 소재의 작은 스터드나 링을 착용하는 경우가 많고, 손가락 반지나 체인 목걸이와 함께 실버로 통일하는 것이 TOWA의 스타일로 자리잡았어요.',
 "DAIKI": '좌우 2개씩 합계 4개.<br>\n본인도 「피어싱을 늘리고 싶다」고 공언한 적이 있어서, 앞으로 더 늘어날 가능성이 있어요.<br>\n7월 중순 사복에서는 피어싱과 옷 색을 YOSHIKI와의 케미명 <a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">「데카네코」</a>에서 딴 초록 계열로 은근하게 맞춘 적도 있었어요.',
 "KOSUKE": '오른쪽 귀 1개・왼쪽 귀 2개로 합계 3개.<br>\n데뷔 싱글 아티스트 사진에서 착용한 것은 <strong><span class="swl-marker mark_pink">별 모티브 피어싱</span></strong>으로, 팬들 사이에서 「별 피어싱」이라 불릴 만큼 인상적인 아이템이에요.<br>\n멤버 컬러인 빨강과 함께 KOSUKE의 <a href="https://chomoand-1.com/summary-of-ko1keyz-member-emoj-10560" target="_blank" rel="noopener">멤버 이모지도 별(🌟)</a>이라서, 이 별 피어싱은 트레이드마크로 자리잡아가고 있어요.',
 "RYUJI": '데뷔 싱글 아티스트 사진에서는 피어싱과 이어 커프를 함께 착용해, 귀 부분의 액세서리 활용이 눈에 띄는 멤버예요.<br>\n시기에 따라 실버에서 골드로 바꾸는 등 교체도 잦고, 오프숏에서는 피어싱을 빼고 있는 날도 있는 등 귀 부분의 변화가 잦은 편이에요.',
 "KEITO": '좌우 1개씩 2개로, 장식이 적은 실버 스터드가 중심이에요.',
 "YOSHIKI": '좌우 1개씩으로 보이지만, 오른쪽 귀 구멍은 사진으로 확인하기 어려워 확실한 것은 1개예요.',
 "YUKI": '좌우 1개씩 2개로, 2026년 8월경 사진에서도 피어싱을 착용한 모습을 확인할 수 있어요.',
}
KR_N = {"TOWA": "TOWA(하마다 토와)", "DAIKI": "DAIKI(가토 다이키)", "KOSUKE": "KOSUKE(테루이 코스케)",
        "RYUJI": "RYUJI(스기야마 류지)", "KEITO": "KEITO(오노 케이토)", "YOSHIKI": "YOSHIKI(야다 요시키)", "YUKI": "YUKI(고토 유이)"}

EN_B = {
 "TOWA": 'Has 3 on his left ear and 2 on his right.<br>\nHe has holes in the cartilage as well as the lobe, making him the only member with 5.<br>\nIn selfie off-shots he usually wears small silver studs or hoops, and pairs them with rings and a chain necklace to keep everything in silver — a look that has become his signature.',
 "DAIKI": 'Has 2 on each side for a total of 4.<br>\nHe has said he wants to <strong>get more piercings</strong>, so the number could well go up.<br>\nIn one mid-July outfit he tied his piercings and clothes together in the green tones of <a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">“Dekaneko,”</a> his pairing nickname with YOSHIKI.',
 "KOSUKE": 'Has 1 on his right ear and 2 on his left, for 3 in total.<br>\nThe <strong><span class="swl-marker mark_pink">star-shaped piercing</span></strong> he wore in the debut single’s artist photo is striking enough that fans call it his “star piercing.”<br>\nTogether with his red member color, KOSUKE’s <a href="https://chomoand-1.com/summary-of-ko1keyz-member-emoj-10560" target="_blank" rel="noopener">member emoji is also a star (🌟)</a>, so the star piercing is turning into a trademark.',
 "RYUJI": 'In the debut single\'s artist photo he layered a piercing with an ear cuff, and he\'s one of the members whose ear styling really stands out.<br>\nHe also changes them out a lot — switching from silver to gold at times — and on some off-shots he has his piercings out entirely, so his ears are rarely the same twice.',
 "KEITO": 'One per ear for 2, mostly plain silver studs.',
 "YOSHIKI": 'Appears to have one per ear, but the hole on his right ear is hard to make out in photos, so only one is clearly confirmed.',
 "YUKI": 'One per ear for 2 as well, and photos from around August 2026 also show him wearing a piercing.',
}
EN_N = {"TOWA": "TOWA (Towa Hamada)", "DAIKI": "DAIKI (Daiki Kato)", "KOSUKE": "KOSUKE (Kosuke Terui)",
        "RYUJI": "RYUJI (Ryuji Sugiyama)", "KEITO": "KEITO (Keito Ono)", "YOSHIKI": "YOSHIKI (Yoshiki Yada)", "YUKI": "YUKI (Yui Goto)"}

# ---- old paragraph blocks currently in each post ----
JP_OLD = {
 "TOWA": para('<strong>TOWA(濱田永遠)</strong>は左耳に3つ、右耳に2つ。<br>\n耳たぶだけでなく軟骨にもホールがあり、12人の中では唯一の5つ持ちです。<br>\n自撮りのオフショットではシルバーの小ぶりなスタッドやフープを着けていることが多く、指のリングやチェーンネックレスとあわせてシルバーで統一するのがTOWA流のスタイルになっています。'),
 "DAIKI": para('<strong>DAIKI(加藤大樹)</strong>は左右2つずつの合計4つ。<br>\n本人も「ピアスを増やしたい」と公言しており、今後さらに増える可能性があります。<br>\n7月中旬の私服では、ピアスと服の色をYOSHIKIとのケミ名<a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">「デカ猫」</a>にちなんだ緑系でさりげなく揃えていたこともありました。'),
 "KOSUKE": para('<strong>KOSUKE(照井康祐)</strong>は右耳1つ・左耳2つの合計3つ。<br>\nデビューシングルのアーティスト写真で着けていたのは<strong><span class="swl-marker mark_pink">星モチーフのピアス</span></strong>で、ファンの間では「星のピアス」と呼ばれるほど印象的なアイテムです。<br>\nメンバーカラーの赤とあわせて、KOSUKEの<a href="https://chomoand-1.com/summary-of-ko1keyz-member-emoj-10560" target="_blank" rel="noopener">メンバー絵文字も星(🌟)</a>なので、この星ピアスはトレードマークとして定着しつつあります。'),
 "RYUJI": para('<strong>RYUJI(杉山竜司)</strong>は左右1つずつ。<br>\nデビューシングルのアー写ではピアスとイヤーカフを重ね付けしており、耳元のアクセサリー使いが目立つメンバーです。<br>\n時期によってシルバーからゴールドへ変えるなど付け替えも多く、オフショットではピアスを外している日もあるなど、耳元の変化はこまめにあります。'),
 "KYY": para('<strong>KEITO(小野慶人)</strong>も左右1つずつの2つで、装飾控えめのシルバースタッドが中心です。<br>\n<strong>YOSHIKI(矢田佳暉)</strong>は左右1つずつと見られますが、右耳のホールは写真での確認が難しく、はっきり分かるのは1つです。<br>\n<strong>YUKI(後藤結)</strong>も左右1つずつの2つで、2026年8月ごろの写真でもピアスを着けている様子が確認できます。'),
}
KR_OLD = {
 "TOWA": para('<strong>TOWA(하마다 토와)</strong>는 왼쪽 귀에 3개, 오른쪽 귀에 2개.<br>\n귓불뿐 아니라 연골에도 구멍이 있어, 12명 중 유일한 5개 보유자예요.<br>\n셀카 오프숏에서는 실버 소재의 작은 스터드나 링을 착용하는 경우가 많고, 손가락 반지나 체인 목걸이와 함께 실버로 통일하는 것이 TOWA의 스타일로 자리잡았어요.'),
 "DAIKI": para('<strong>DAIKI(가토 다이키)</strong>는 좌우 2개씩 합계 4개.<br>\n본인도 「피어싱을 늘리고 싶다」고 공언한 적이 있어서, 앞으로 더 늘어날 가능성이 있어요.<br>\n7월 중순 사복에서는 피어싱과 옷 색을 YOSHIKI와의 케미명 <a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">「데카네코」</a>에서 딴 초록 계열로 은근하게 맞춘 적도 있었어요.'),
 "KOSUKE": para('<strong>KOSUKE(테루이 코스케)</strong>는 오른쪽 귀 1개・왼쪽 귀 2개로 합계 3개.<br>\n데뷔 싱글 아티스트 사진에서 착용한 것은 <strong><span class="swl-marker mark_pink">별 모티브 피어싱</span></strong>으로, 팬들 사이에서 「별 피어싱」이라 불릴 만큼 인상적인 아이템이에요.<br>\n멤버 컬러인 빨강과 함께 KOSUKE의 <a href="https://chomoand-1.com/summary-of-ko1keyz-member-emoj-10560" target="_blank" rel="noopener">멤버 이모지도 별(🌟)</a>이라서, 이 별 피어싱은 트레이드마크로 자리잡아가고 있어요.'),
 "RYUJI": para('<strong>RYUJI(스기야마 류지)</strong>는 좌우 1개씩.<br>\n데뷔 싱글 아티스트 사진에서는 피어싱과 이어 커프를 함께 착용해, 귀 부분의 액세서리 활용이 눈에 띄는 멤버예요.<br>\n시기에 따라 실버에서 골드로 바꾸는 등 교체도 잦고, 오프숏에서는 피어싱을 빼고 있는 날도 있는 등 귀 부분의 변화가 잦은 편이에요.'),
 "KYY": para('<strong>KEITO(오노 케이토)</strong>도 좌우 1개씩 2개로, 장식이 적은 실버 스터드가 중심이에요.<br>\n<strong>YOSHIKI(야다 요시키)</strong>는 좌우 1개씩으로 보이지만, 오른쪽 귀 구멍은 사진으로 확인하기 어려워 확실한 것은 1개예요.<br>\n<strong>YUKI(고토 유이)</strong>도 좌우 1개씩 2개로, 2026년 8월경 사진에서도 피어싱을 착용한 모습을 확인할 수 있어요.'),
}
EN_OLD = {
 "TOWA": para('<strong>TOWA (Towa Hamada)</strong> has 3 on his left ear and 2 on his right.<br>\nHe has holes in the cartilage as well as the lobe, making him the only member with 5.<br>\nIn selfie off-shots he usually wears small silver studs or hoops, and pairs them with rings and a chain necklace to keep everything in silver — a look that has become his signature.'),
 "DAIKI": para('<strong>DAIKI (Daiki Kato)</strong> has 2 on each side for a total of 4.<br>\nHe has said he wants to <strong>get more piercings</strong>, so the number could well go up.<br>\nIn one mid-July outfit he tied his piercings and clothes together in the green tones of <a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">“Dekaneko,”</a> his pairing nickname with YOSHIKI.'),
 "KOSUKE": para('<strong>KOSUKE (Kosuke Terui)</strong> has 1 on his right ear and 2 on his left, for 3 in total.<br>\nThe <strong><span class="swl-marker mark_pink">star-shaped piercing</span></strong> he wore in the debut single’s artist photo is striking enough that fans call it his “star piercing.”<br>\nTogether with his red member color, KOSUKE’s <a href="https://chomoand-1.com/summary-of-ko1keyz-member-emoj-10560" target="_blank" rel="noopener">member emoji is also a star (🌟)</a>, so the star piercing is turning into a trademark.'),
 "RYUJI": para('<strong>RYUJI (Ryuji Sugiyama)</strong> has one hole in each ear.<br>\nIn the debut single\'s artist photo he layered a piercing with an ear cuff, and he\'s one of the members whose ear styling really stands out.<br>\nHe also changes them out a lot — switching from silver to gold at times — and on some off-shots he has his piercings out entirely, so his ears are rarely the same twice.'),
 "KYY": para('<strong>KEITO (Keito Ono)</strong> also has one per ear for 2, mostly plain silver studs.<br>\n<strong>YOSHIKI (Yoshiki Yada)</strong> appears to have one per ear, but the hole on his right ear is hard to make out in photos, so only one is clearly confirmed.<br>\n<strong>YUKI (Yui Goto)</strong> has one per ear for 2 as well, and photos from around August 2026 also show him wearing a piercing.'),
}

BR = {
 12030: ('<strong>RYUJI・KEITO・YOSHIKI・YUKIの4人は左右1つずつの合計2つ。</strong>中でもRYUJIはピアスをよく付け替えるタイプです。',
         '<strong>RYUJI・KEITO・YOSHIKI・YUKIの4人は左右1つずつの合計2つ。</strong><br>中でもRYUJIはピアスをよく付け替えるタイプです。'),
 12034: ('<strong>RYUJI・KEITO・YOSHIKI・YUKI 4명은 좌우 1개씩 합계 2개.</strong>그중 RYUJI는 피어싱을 자주 바꿔 끼는 타입이에요.',
         '<strong>RYUJI・KEITO・YOSHIKI・YUKI 4명은 좌우 1개씩 합계 2개.</strong><br>그중 RYUJI는 피어싱을 자주 바꿔 끼는 타입이에요.'),
 12038: ('<strong>RYUJI, KEITO, YOSHIKI and YUKI each have one per ear, for 2.</strong>RYUJI in particular swaps his out often.',
         '<strong>RYUJI, KEITO, YOSHIKI and YUKI each have one per ear, for 2.</strong><br>RYUJI in particular swaps his out often.'),
}


def build(pid, OLD, N, B):
    pairs = []
    for k in ("TOWA", "DAIKI", "KOSUKE", "RYUJI"):
        pairs.append((OLD[k], box(N[k], B[k])))
    pairs.append((OLD["KYY"], "\n\n".join(box(N[k], B[k]) for k in ("KEITO", "YOSHIKI", "YUKI"))))
    pairs.append(BR[pid])
    return pairs


ALL = {12030: build(12030, JP_OLD, JP_N, JP_B),
       12034: build(12034, KR_OLD, KR_N, KR_B),
       12038: build(12038, EN_OLD, EN_N, EN_B)}

for pid, pairs in ALL.items():
    j = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=H, params={"context": "edit"}).json()
    raw = j["content"]["raw"]
    for i, (old, new) in enumerate(pairs):
        c = raw.count(old)
        if c != 1:
            raise SystemExit(f"[{pid}] pair {i}: expected 1, got {c}\n---\n{old[:160]}")
        raw = raw.replace(old, new)
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{pid}",
        headers={**H, "Content-Type": "application/json"},
        data=json.dumps({"content": raw, "status": "draft"}).encode("utf-8"),
    )
    r.raise_for_status()
    print(f"[{pid}] updated OK ({len(pairs)} edits)")
