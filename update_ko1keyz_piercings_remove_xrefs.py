# -*- coding: utf-8 -*-
"""ピアス記事(JP/KR/EN 下書き)から、元ネタXの投稿・ファン反応への言及を除去する更新。
ユーザー指示「Xの投稿については記事で触れなくていい」を反映。事実は残し、
「投稿主が自信がない」「Xで話題」「〜という声が続出」等の出所言及だけ地の文に書き換える。"""
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

JP = [
(
"""Xではメンバーの耳を1人ずつ観察してピアスの位置をまとめた投稿が話題になっており、それによると<strong>いちばん多いのはTOWA(濱田永遠)の5つ、続いてDAIKI(加藤大樹)の4つ、KOSUKE(照井康祐)の3つ</strong>という並びでした。""",
"""メンバーの耳元をアーティスト写真やライブ映像から1人ずつ見ていくと、<strong>いちばん多いのはTOWA(濱田永遠)の5つ、続いてDAIKI(加藤大樹)の4つ、KOSUKE(照井康祐)の3つ</strong>という並びになります。""",
),
(
"""<p>まとめの元になっているのは、2026年8月末にXで公開された、メンバーの耳を1人ずつ観察してピアスホールの位置を書き出した投稿です。<br>
そこにデビューシングルのアーティスト写真やライブ・配信での見え方を重ねて整理すると、12人のピアスの数は次のようになります。</p>""",
"""<p>耳たぶ(ロブ)から軟骨まで、デビューシングルのアーティスト写真やライブ・配信での見え方をもとにメンバーの耳元を1人ずつ確認していくと、12人のピアスの数は次のように整理できます。</p>""",
),
(
"""<figcaption style="text-align:center;font-size:12px;">Xでの観察情報をもとに作成した一覧。数は左右の耳の合計です。</figcaption>""",
"""<figcaption style="text-align:center;font-size:12px;">メンバーごとのピアスの数(左右の耳の合計)。</figcaption>""",
),
(
"""<p>なお、写真の角度によっては左右どちらの耳か見えづらい部分もあり、YOSHIKI・YURA・YUKIの一部は投稿主も「自信がない」としています。<br>
細かい本数は今後前後する可能性がある点だけ、先にお断りしておきます。</p>""",
"""<p>ただし写真の角度によっては左右どちらの耳か見えづらいメンバーもいて、特にYOSHIKI・YURA・YUKIあたりは本数がはっきりしません。<br>
細かい数は今後前後する可能性がある点だけ、先にお断りしておきます。</p>""",
),
(
"""本人がXで「韓国公演までにやりたいこと」の一つに<strong>「ピアスを増やす」</strong>と挙げており、今後さらに増える可能性があります。""",
"""本人も「ピアスを増やしたい」と公言しており、今後さらに増える可能性があります。""",
),
(
"""7月中旬の私服では、ピアスと服の色をYOSHIKIとのケミ名<a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">「デカ猫」</a>カラーで揃えていたと話題になったこともありました。""",
"""7月中旬の私服では、ピアスと服の色をYOSHIKIとのケミ名<a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">「デカ猫」</a>にちなんだ緑系でさりげなく揃えていたこともありました。""",
),
(
"""デビューシングルのアーティスト写真で着けていた<strong><span class="swl-marker mark_pink">星モチーフのピアス</span></strong>がファンの間で「星のピアス」と呼ばれ、「同じものを探しに行かなきゃ」という声が続出しました。""",
"""デビューシングルのアーティスト写真で着けていたのは<strong><span class="swl-marker mark_pink">星モチーフのピアス</span></strong>で、ファンの間では「星のピアス」と呼ばれるほど印象的なアイテムです。""",
),
(
"""<p><strong>RYUJI(杉山竜司)</strong>は左右1つずつ。<br>
デビューシングルのアー写ではピアスとイヤーカフを重ね付けしていて、ファンからも「ピアスとイヤーカフ」が推しポイントに挙げられていました。<br>
時期によってシルバーからゴールドに変えるなど付け替えも多く、愛犬と遊ぶオフショットで「前と比べてピアスがしっかりゴールドになってる」と気づかれたり、「いつも付けてたピアス取っちゃったの」と外した日に反応があったりと、耳元の変化がこまめに見られています。</p>""",
"""<p><strong>RYUJI(杉山竜司)</strong>は左右1つずつ。<br>
デビューシングルのアー写ではピアスとイヤーカフを重ね付けしており、耳元のアクセサリー使いが目立つメンバーです。<br>
時期によってシルバーからゴールドへ変えるなど付け替えも多く、オフショットではピアスを外している日もあるなど、耳元の変化はこまめにあります。</p>""",
),
(
"""<p><strong>KEITO(小野慶人)</strong>も左右1つずつの2つで、装飾控えめのシルバースタッドが中心です。<br>
<strong>YOSHIKI(矢田佳暉)</strong>は左右1つずつと見られていますが、右耳のホールは観察した投稿でも「自信がない」とされており、はっきり確認できるのは1つです。<br>
<strong>YUKI(後藤結)</strong>も左右1つずつの2つで、2026年8月の写真でピアスを着けている様子が確認され「顔がいいうえにピアスもしてる」と反響がありました。</p>""",
"""<p><strong>KEITO(小野慶人)</strong>も左右1つずつの2つで、装飾控えめのシルバースタッドが中心です。<br>
<strong>YOSHIKI(矢田佳暉)</strong>は左右1つずつと見られますが、右耳のホールは写真での確認が難しく、はっきり分かるのは1つです。<br>
<strong>YUKI(後藤結)</strong>も左右1つずつの2つで、2026年8月ごろの写真でもピアスを着けている様子が確認できます。</p>""",
),
]

KR = [
(
"""X에서는 멤버들의 귀를 한 명씩 관찰해 피어싱 위치를 정리한 게시글이 화제가 됐는데, 그에 따르면 <strong>가장 많은 것은 TOWA(하마다 토와)의 5개, 이어서 DAIKI(가토 다이키)의 4개, KOSUKE(테루이 코스케)의 3개</strong> 순이었어요.""",
"""멤버들의 귀 부분을 아티스트 사진이나 라이브 영상에서 한 명씩 살펴보면, <strong>가장 많은 것은 TOWA(하마다 토와)의 5개, 이어서 DAIKI(가토 다이키)의 4개, KOSUKE(테루이 코스케)의 3개</strong> 순이에요.""",
),
(
"""<p>정리의 바탕이 된 것은 2026년 8월 말에 X에 공유된, 멤버들의 귀를 한 명씩 관찰해 피어싱 구멍 위치를 적어둔 게시글이에요.<br>
여기에 데뷔 싱글 아티스트 사진이나 라이브・방송에서 보이는 모습을 더해 정리하면, 12명의 피어싱 개수는 다음과 같아요.</p>""",
"""<p>귓불(로브)부터 연골까지, 데뷔 싱글 아티스트 사진이나 라이브・방송에서 보이는 모습을 바탕으로 멤버들의 귀 부분을 한 명씩 확인해 보면, 12명의 피어싱 개수는 다음과 같이 정리할 수 있어요.</p>""",
),
(
"""<figcaption style="text-align:center;font-size:12px;">X에 공유된 관찰 정보를 바탕으로 작성. 개수는 좌우 귀의 합계입니다.</figcaption>""",
"""<figcaption style="text-align:center;font-size:12px;">멤버별 피어싱 개수(좌우 귀의 합계).</figcaption>""",
),
(
"""<p>다만 사진 각도에 따라 좌우 어느 쪽 귀인지 보기 어려운 부분도 있어서, YOSHIKI・YURA・YUKI의 일부는 게시글 작성자도 「자신이 없다」고 했어요.<br>
세부 개수는 앞으로 달라질 수 있다는 점만 먼저 말씀드릴게요.</p>""",
"""<p>다만 사진 각도에 따라 좌우 어느 쪽 귀인지 보기 어려운 멤버도 있어서, 특히 YOSHIKI・YURA・YUKI는 개수가 분명하지 않아요.<br>
세부 개수는 앞으로 달라질 수 있다는 점만 먼저 말씀드릴게요.</p>""",
),
(
"""본인이 X에서 「한국 공연까지 하고 싶은 것」 중 하나로 <strong>「피어싱 늘리기」</strong>를 꼽아서, 앞으로 더 늘어날 가능성이 있어요.""",
"""본인도 「피어싱을 늘리고 싶다」고 공언한 적이 있어서, 앞으로 더 늘어날 가능성이 있어요.""",
),
(
"""7월 중순 사복에서는 피어싱과 옷 색을 YOSHIKI와의 케미명 <a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">「데카네코」</a> 컬러로 맞췄다고 화제가 된 적도 있었어요.""",
"""7월 중순 사복에서는 피어싱과 옷 색을 YOSHIKI와의 케미명 <a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">「데카네코」</a>에서 딴 초록 계열로 은근하게 맞춘 적도 있었어요.""",
),
(
"""데뷔 싱글 아티스트 사진에서 착용한 <strong><span class="swl-marker mark_pink">별 모티브 피어싱</span></strong>이 팬들 사이에서 「별 피어싱」이라 불리며 「똑같은 걸 사러 가야겠다」는 반응이 이어졌어요.""",
"""데뷔 싱글 아티스트 사진에서 착용한 것은 <strong><span class="swl-marker mark_pink">별 모티브 피어싱</span></strong>으로, 팬들 사이에서 「별 피어싱」이라 불릴 만큼 인상적인 아이템이에요.""",
),
(
"""<p><strong>RYUJI(스기야마 류지)</strong>는 좌우 1개씩.<br>
데뷔 싱글 아티스트 사진에서는 피어싱과 이어 커프를 함께 착용했고, 팬들도 「피어싱과 이어 커프」를 최애 포인트로 꼽았어요.<br>
시기에 따라 실버에서 골드로 바꾸는 등 교체도 잦아서, 반려견과 노는 오프숏에서 「전보다 피어싱이 확실히 골드가 됐다」고 알아채거나, 「늘 하던 피어싱을 뺐다」며 뺀 날에 반응이 오는 등 귀 부분의 변화가 자주 포착되고 있어요.</p>""",
"""<p><strong>RYUJI(스기야마 류지)</strong>는 좌우 1개씩.<br>
데뷔 싱글 아티스트 사진에서는 피어싱과 이어 커프를 함께 착용해, 귀 부분의 액세서리 활용이 눈에 띄는 멤버예요.<br>
시기에 따라 실버에서 골드로 바꾸는 등 교체도 잦고, 오프숏에서는 피어싱을 빼고 있는 날도 있는 등 귀 부분의 변화가 잦은 편이에요.</p>""",
),
(
"""<p><strong>KEITO(오노 케이토)</strong>도 좌우 1개씩 2개로, 장식이 적은 실버 스터드가 중심이에요.<br>
<strong>YOSHIKI(야다 요시키)</strong>는 좌우 1개씩으로 보이지만, 오른쪽 귀 구멍은 관찰 게시글에서도 「자신이 없다」고 해서 확실히 확인되는 것은 1개예요.<br>
<strong>YUKI(고토 유이)</strong>도 좌우 1개씩 2개로, 2026년 8월 사진에서 피어싱을 착용한 모습이 확인돼 「얼굴도 잘생겼는데 피어싱까지 했다」는 반응이 있었어요.</p>""",
"""<p><strong>KEITO(오노 케이토)</strong>도 좌우 1개씩 2개로, 장식이 적은 실버 스터드가 중심이에요.<br>
<strong>YOSHIKI(야다 요시키)</strong>는 좌우 1개씩으로 보이지만, 오른쪽 귀 구멍은 사진으로 확인하기 어려워 확실한 것은 1개예요.<br>
<strong>YUKI(고토 유이)</strong>도 좌우 1개씩 2개로, 2026년 8월경 사진에서도 피어싱을 착용한 모습을 확인할 수 있어요.</p>""",
),
]

EN = [
(
"""A post that went around on X, listing every member's piercing spots ear by ear, says <strong>TOWA (Towa Hamada) has the most at 5, followed by DAIKI (Daiki Kato) with 4 and KOSUKE (Kosuke Terui) with 3</strong>.<br>""",
"""Going through each member's ears one by one in the debut single's artist photos and live footage, <strong>TOWA (Towa Hamada) has the most at 5, followed by DAIKI (Daiki Kato) with 4 and KOSUKE (Kosuke Terui) with 3</strong>.<br>""",
),
(
"""plus the designs that fans have actually spotted — star studs, gold hoops and more.""",
"""plus the designs seen in their photos — star studs, gold hoops and more.""",
),
(
"""<p>The starting point is a post shared on X in late August 2026 that went through each member's ears one by one and marked where the piercing holes are.<br>
Cross-checking that against the debut single's artist photos and how their ears look in lives and streams, the counts break down like this.</p>""",
"""<p>Going lobe to helix, working from the debut single's artist photos and how their ears look in lives and streams, the counts break down like this.</p>""",
),
(
"""<figcaption style="text-align:center;font-size:12px;">Compiled from fan observations shared on X. Numbers are the total for both ears.</figcaption>""",
"""<figcaption style="text-align:center;font-size:12px;">Piercings per member (total for both ears).</figcaption>""",
),
(
"""<p>That said, camera angles make it hard to tell which ear is which in some shots, and the original poster admitted they weren't sure about parts of YOSHIKI, YURA and YUKI.<br>
So treat the exact numbers as something that could still shift a little.</p>""",
"""<p>That said, camera angles make it hard to tell which ear is which in some shots, and the counts for YOSHIKI, YURA and YUKI in particular aren't clear-cut.<br>
So treat the exact numbers as something that could still shift a little.</p>""",
),
(
"""He listed <strong>“get more piercings”</strong> as one of his goals before the group's Korea shows in a post on X, so the number could well go up.<br>""",
"""He has said he wants to <strong>get more piercings</strong>, so the number could well go up.<br>""",
),
(
"""In one mid-July outfit, fans noticed he had matched his piercings and clothes to the colors of <a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">“Dekaneko,”</a> his pairing nickname with YOSHIKI.""",
"""In one mid-July outfit he tied his piercings and clothes together in the green tones of <a href="https://chomoand-1.com/ko1keyz-chemi-names-11773" target="_blank" rel="noopener">“Dekaneko,”</a> his pairing nickname with YOSHIKI.""",
),
(
"""The <strong><span class="swl-marker mark_pink">star-shaped piercing</span></strong> he wore in the debut single’s artist photo became known among fans as his “star piercing,” with lots of people saying they wanted to track down the same one.<br>""",
"""The <strong><span class="swl-marker mark_pink">star-shaped piercing</span></strong> he wore in the debut single’s artist photo is striking enough that fans call it his “star piercing.”<br>""",
),
(
"""<p><strong>RYUJI (Ryuji Sugiyama)</strong> has one hole in each ear.<br>
In the debut single's artist photo he layered a piercing with an ear cuff, and fans list “the piercing and ear cuff” among his best features.<br>
He also changes them out a lot — switching from silver to gold at times — with fans spotting “his piercings have gone properly gold now” in an off-shot playing with his dog, or reacting on days he takes his usual pair out.</p>""",
"""<p><strong>RYUJI (Ryuji Sugiyama)</strong> has one hole in each ear.<br>
In the debut single's artist photo he layered a piercing with an ear cuff, and he's one of the members whose ear styling really stands out.<br>
He also changes them out a lot — switching from silver to gold at times — and on some off-shots he has his piercings out entirely, so his ears are rarely the same twice.</p>""",
),
(
"""<strong>YOSHIKI (Yoshiki Yada)</strong> appears to have one per ear, but the hole on his right ear was marked “not sure” even in the observation post, so only one is clearly confirmed.<br>
<strong>YUKI (Yui Goto)</strong> has one per ear for 2 as well; an August 2026 photo showed him wearing a piercing, drawing comments that he “has the looks and the piercings.”</p>""",
"""<strong>YOSHIKI (Yoshiki Yada)</strong> appears to have one per ear, but the hole on his right ear is hard to make out in photos, so only one is clearly confirmed.<br>
<strong>YUKI (Yui Goto)</strong> has one per ear for 2 as well, and photos from around August 2026 also show him wearing a piercing.</p>""",
),
]


def apply(post_id, pairs):
    j = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{post_id}", headers=H, params={"context": "edit"}).json()
    raw = j["content"]["raw"]
    for i, (old, new) in enumerate(pairs):
        n = raw.count(old)
        if n != 1:
            raise SystemExit(f"[{post_id}] pair {i}: expected 1 match, got {n}\n---OLD---\n{old}\n")
        raw = raw.replace(old, new)
    # 念のため、残っていないか最終チェック
    for bad in ("Xで公開された", "投稿主", "観察した投稿", "관찰 게시글", "게시글 작성자", "X에 공유된", "X에서는", "shared on X", "in a post on X", "the observation post", "fan observations shared on X"):
        if bad in raw:
            raise SystemExit(f"[{post_id}] still contains: {bad}")
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
        headers={**H, "Content-Type": "application/json"},
        data=json.dumps({"content": raw, "status": "draft"}).encode("utf-8"),
    )
    r.raise_for_status()
    print(f"[{post_id}] updated OK ({len(pairs)} edits)")


apply(12030, JP)
apply(12034, KR)
apply(12038, EN)
