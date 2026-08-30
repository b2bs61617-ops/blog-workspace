# -*- coding: utf-8 -*-
"""藤牧大雅 BUZZ STATION 記事の追記パッチ(v2):
- 藤牧大雅 wiki記事(1025)・既存ファンミ記事(10345)への内部リンク追加
- 生放送/公開スタジオ/観覧の可否についての加筆 + スタジオのGoogleマップ
"""
import json, base64, os
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
H = {"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"}

WIKI = "https://chomoand-1.com/fujimakitaiga_wiki-1025"
FANMI = "https://chomoand-1.com/taiga-no-meeting-10345"
MAP = ('<!-- wp:html -->\n<iframe src="https://maps.google.com/maps?q=%E6%B8%8B%E8%B0%B7%E3%82%AF%E3%83%AD%E3%82%B9FM&t=&z=16&ie=UTF8&iwloc=&output=embed" '
       'width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>\n<!-- /wp:html -->')

PATCHES = {
    11941: [
        # 1) intro line: 観覧の可否 を追加
        ("放送の日時と聴き方、「BUZZ STATION」がどんな番組なのか、",
         "放送の日時と聴き方・観覧の可否、「BUZZ STATION」がどんな番組なのか、"),
        # 2) 基本情報テーブルの「形式」
        ("<td style=\"border:1px solid #ddd9d3;padding:8px 12px;\">渋谷の公開スタジオからの生放送</td>",
         "<td style=\"border:1px solid #ddd9d3;padding:8px 12px;\">渋谷・神南の公開スタジオからの生放送(観覧できる建て付け)</td>"),
        # 3) 「見に行けば」段落を全面差し替え + マップ
        ("<!-- wp:paragraph -->\n<p>公開スタジオからの生放送のため、スタジオの様子を見に行けば、濱口優さんやゲストと同じ空間でラジオ収録の臨場感を体感できるのも特徴です。<br>\n藤牧大雅さんの出演回も同じ形式で放送されるとみられます。</p>\n<!-- /wp:paragraph -->",
         "<!-- wp:paragraph -->\n<p>放送はすべて生放送で、収録は渋谷・神南のシダックス・カルチャービレッジ1階にある公開スタジオから行われます。<br>\n"
         "ファイヤー通り沿いの歩道からガラス越しにスタジオが見える立地で、番組は「観覧に来たリスナーが濱口優さんやゲストと同じ空間で番組を楽しめる」体験型ラジオをうたっています。<br>\n"
         "つまり、収録を生で見に行くことも想定された番組です。</p>\n<!-- /wp:paragraph -->\n\n"
         "<!-- wp:paragraph -->\n<p>ただし、藤牧大雅さんの回に一般向けの観覧枠が設けられるのか、整理券や事前申し込みが必要かどうかは、現時点でアナウンスされていません。<br>\n"
         "観覧を考えている場合は、番組公式X(@BUZZ_STATION1)やShibuya Cross-FMの公式サイトで直前の案内を必ず確認してください。<br>\n"
         "藤牧大雅さんの出演回も、放送そのものは同じ生放送の形で届けられるとみられます。</p>\n<!-- /wp:paragraph -->\n\n" + MAP),
        # 4) プロフィール導入に wiki リンク
        ("JYPの練習生として約4年半を過ごしたのち、日本と韓国のサバイバル番組に立て続けに参加してきました。</p>",
         "JYPの練習生として約4年半を過ごしたのち、日本と韓国のサバイバル番組に立て続けに参加してきました。<br>\n"
         f'より詳しい生い立ち・経歴は<a href="{WIKI}" target="_blank" rel="noopener">藤牧大雅のwiki風経歴記事</a>にまとめています。</p>'),
        # 5) ファンミ節に既存記事リンク
        ("本人のInstagram(@taiga17517)のプロフィール欄のリンクから申し込めます。<br>\nファンミーティングで直接会い、",
         "本人のInstagram(@taiga17517)のプロフィール欄のリンクから申し込めます。<br>\n"
         f'開催日・会場・内容の詳細は<a href="{FANMI}" target="_blank" rel="noopener">ファンミーティングまとめ記事</a>で紹介しています。<br>\n'
         "ファンミーティングで直接会い、"),
        # 6) まとめボックス
        ("&#10003; 放送は2026年9月18日(金)18:00〜18:50、Shibuya Cross-FM(93.8MHz)<br>",
         "&#10003; 放送は2026年9月18日(金)18:00〜18:50、Shibuya Cross-FM(93.8MHz)の生放送<br>\n"
         "&#10003; 渋谷・神南の公開スタジオで、収録を見に行ける建て付け(藤牧回の観覧枠の有無は未案内)<br>"),
        # 7) 関連記事ボックス
        ('<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">日プ新世界の関連記事</p>\n<ul style="margin:0;padding-left:1.3em;">\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_zense-2748" target="_blank" rel="noopener">【日プ新世界】練習生の前世一覧！元K-POPアイドルや経歴を徹底調査！</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_8matome-8577" target="_blank" rel="noopener">【日プ新世界】第8話まとめ｜コンセプト評価・KCON・第2回順位発表式結果！</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japan_ryourirecipi-8604" target="_blank" rel="noopener">【日プ新世界】練習生が作った料理のレシピまとめ！意外な料理男子も判明！</a></li>',
         '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">藤牧大雅・日プ新世界の関連記事</p>\n<ul style="margin:0;padding-left:1.3em;">\n'
         f'<li><a href="{WIKI}" target="_blank" rel="noopener">藤牧大雅のwiki風経歴は？EXPG・JYP出身で虹プロ2やボイプラ2経験者！</a></li>\n'
         f'<li><a href="{FANMI}" target="_blank" rel="noopener">藤牧大雅のファンミーティングは無料！開催日や会場・内容は？</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_zense-2748" target="_blank" rel="noopener">【日プ新世界】練習生の前世一覧！元K-POPアイドルや経歴を徹底調査！</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_8matome-8577" target="_blank" rel="noopener">【日プ新世界】第8話まとめ｜コンセプト評価・KCON・第2回順位発表式結果！</a></li>'),
    ],
    11946: [
        ("이 기사에서는 방송 일시와 청취 방법, 「BUZZ STATION」이 어떤 프로그램인지,",
         "이 기사에서는 방송 일시와 청취 방법·관람 가능 여부, 「BUZZ STATION」이 어떤 프로그램인지,"),
        ("<td style=\"border:1px solid #ddd9d3;padding:8px 12px;\">시부야 공개 스튜디오 생방송</td>",
         "<td style=\"border:1px solid #ddd9d3;padding:8px 12px;\">시부야·진난 공개 스튜디오 생방송(관람 가능한 형태)</td>"),
        ("<!-- wp:paragraph -->\n<p>공개 스튜디오 생방송이기 때문에, 스튜디오 현장을 보러 가면 하마구치 마사루 씨나 게스트와 같은 공간에서 라디오 녹음의 현장감을 체감할 수 있는 것도 특징입니다.<br>\n후지마키 타이가 씨의 출연 회차도 같은 형식으로 방송될 것으로 보입니다.</p>\n<!-- /wp:paragraph -->",
         "<!-- wp:paragraph -->\n<p>방송은 모두 생방송이며, 녹음은 시부야·진난의 시닥스 컬처 빌리지 1층에 있는 공개 스튜디오에서 이루어집니다.<br>\n"
         "'파이어 거리' 쪽 보도에서 유리 너머로 스튜디오가 보이는 위치이며, 프로그램은 '관람하러 온 청취자가 하마구치 마사루 씨나 게스트와 같은 공간에서 프로그램을 즐길 수 있는' 체험형 라디오를 표방합니다.<br>\n"
         "즉, 녹음을 직접 보러 가는 것도 상정된 프로그램입니다.</p>\n<!-- /wp:paragraph -->\n\n"
         "<!-- wp:paragraph -->\n<p>다만, 후지마키 타이가 씨의 회차에 일반 관람석이 마련되는지, 정리권이나 사전 신청이 필요한지는 현시점에서 안내되지 않았습니다.<br>\n"
         "관람을 생각한다면, 프로그램 공식 X(@BUZZ_STATION1)나 Shibuya Cross-FM 공식 사이트에서 방송 직전 안내를 반드시 확인해 주세요.<br>\n"
         "후지마키 타이가 씨의 출연 회차도 방송 자체는 같은 생방송 형태로 전해질 것으로 보입니다.</p>\n<!-- /wp:paragraph -->\n\n" + MAP),
        ("JYP 연습생으로 약 4년 반을 보낸 뒤, 일본과 한국의 서바이벌 프로그램에 잇달아 참가해 왔습니다.</p>",
         "JYP 연습생으로 약 4년 반을 보낸 뒤, 일본과 한국의 서바이벌 프로그램에 잇달아 참가해 왔습니다.<br>\n"
         f'더 자세한 성장 과정·경력은 <a href="{WIKI}" target="_blank" rel="noopener">후지마키 타이가의 wiki풍 경력 기사(일본어)</a>에 정리되어 있습니다.</p>'),
        ("본인의 인스타그램(@taiga17517) 프로필란의 링크에서 신청할 수 있습니다.<br>\n팬미팅에서 직접 만나고,",
         "본인의 인스타그램(@taiga17517) 프로필란의 링크에서 신청할 수 있습니다.<br>\n"
         f'개최일·장소·내용의 자세한 사항은 <a href="{FANMI}" target="_blank" rel="noopener">팬미팅 정리 기사(일본어)</a>에서 소개하고 있습니다.<br>\n'
         "팬미팅에서 직접 만나고,"),
        ("&#10003; 방송은 2026년 9월 18일(금) 18:00〜18:50, Shibuya Cross-FM(93.8MHz)<br>",
         "&#10003; 방송은 2026년 9월 18일(금) 18:00〜18:50, Shibuya Cross-FM(93.8MHz) 생방송<br>\n"
         "&#10003; 시부야·진난의 공개 스튜디오에서 녹음을 보러 갈 수 있는 형태(후지마키 회차의 관람석 유무는 미안내)<br>"),
        ('<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">일프 신세계 관련 기사</p>\n<ul style="margin:0;padding-left:1.3em;">\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_zense-2748" target="_blank" rel="noopener">【일프 신세계】연습생 전생 일람! 전 K-POP 아이돌이나 경력을 철저 조사!(일본어)</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_8matome-8577" target="_blank" rel="noopener">【일프 신세계】8화 정리｜콘셉트 평가·KCON·2차 순위 발표식 결과!(일본어)</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japan_ryourirecipi-8604" target="_blank" rel="noopener">【일프 신세계】연습생이 만든 요리 레시피 정리! 의외의 요리 남자도 판명!(일본어)</a></li>',
         '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">후지마키 타이가·일프 신세계 관련 기사</p>\n<ul style="margin:0;padding-left:1.3em;">\n'
         f'<li><a href="{WIKI}" target="_blank" rel="noopener">후지마키 타이가의 wiki풍 경력은? EXPG·JYP 출신으로 니지프로2·보이플래닛2 경험자!(일본어)</a></li>\n'
         f'<li><a href="{FANMI}" target="_blank" rel="noopener">후지마키 타이가의 팬미팅은 무료! 개최일과 장소·내용은?(일본어)</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_zense-2748" target="_blank" rel="noopener">【일프 신세계】연습생 전생 일람! 전 K-POP 아이돌이나 경력을 철저 조사!(일본어)</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_8matome-8577" target="_blank" rel="noopener">【일프 신세계】8화 정리｜콘셉트 평가·KCON·2차 순위 발표식 결과!(일본어)</a></li>'),
    ],
    11947: [
        ("This article covers the broadcast date and how to listen, what kind of program BUZZ STATION is,",
         "This article covers the broadcast date, how to listen and whether you can watch in person, what kind of program BUZZ STATION is,"),
        ("<td style=\"border:1px solid #ddd9d3;padding:8px 12px;\">Live from an open studio in Shibuya</td>",
         "<td style=\"border:1px solid #ddd9d3;padding:8px 12px;\">Live from an open studio in Shibuya/Jinnan (viewing possible)</td>"),
        ("<!-- wp:paragraph -->\n<p>Because it airs live from an open studio, visitors can watch the recording and feel the atmosphere in the same room as Hamaguchi and the guests.<br>\nFujimaki's episode is expected to follow the same format.</p>\n<!-- /wp:paragraph -->",
         "<!-- wp:paragraph -->\n<p>Every episode is broadcast live, recorded from an open studio on the first floor of SHIDAX Culture Village in the Jinnan area of Shibuya.<br>\n"
         "The booth is visible through glass from the sidewalk along Fire Street, and the show bills itself as \"experiential radio\" where listeners who come to watch share the same room as Hamaguchi and the guests.<br>\n"
         "In other words, going to watch the recording in person is part of the concept.</p>\n<!-- /wp:paragraph -->\n\n"
         "<!-- wp:paragraph -->\n<p>That said, it has not been announced whether Fujimaki's episode will have a public viewing area, or whether numbered tickets or advance sign-up will be required.<br>\n"
         "If you are thinking of going, be sure to check the program's official X account (@BUZZ_STATION1) and the Shibuya Cross-FM website for last-minute details.<br>\n"
         "Either way, his episode should be delivered in the same live format.</p>\n<!-- /wp:paragraph -->\n\n" + MAP),
        ("After spending about four and a half years as a JYP trainee, he took part in Japanese and Korean survival programs one after another.</p>",
         "After spending about four and a half years as a JYP trainee, he took part in Japanese and Korean survival programs one after another.<br>\n"
         f'For a fuller look at his background and career, see our <a href="{WIKI}" target="_blank" rel="noopener">wiki-style profile of Taiga Fujimaki (in Japanese)</a>.</p>'),
        ("Ticket reservations are already open, via the link in the profile section of his Instagram (@taiga17517).<br>\nMeeting him in person",
         "Ticket reservations are already open, via the link in the profile section of his Instagram (@taiga17517).<br>\n"
         f'The date, venue and content are covered in our <a href="{FANMI}" target="_blank" rel="noopener">fan meeting roundup (in Japanese)</a>.<br>\n'
         "Meeting him in person"),
        ("&#10003; Airs Friday, September 18, 2026, 18:00-18:50 on Shibuya Cross-FM (93.8MHz)<br>",
         "&#10003; Airs live Friday, September 18, 2026, 18:00-18:50 on Shibuya Cross-FM (93.8MHz)<br>\n"
         "&#10003; Recorded at an open studio in Shibuya/Jinnan that you can go to watch (no viewing details yet for his episode)<br>"),
        ('<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">Related articles on Nippro Shinsekai</p>\n<ul style="margin:0;padding-left:1.3em;">\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_zense-2748" target="_blank" rel="noopener">Nippro Shinsekai: trainee backgrounds list (in Japanese)</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_8matome-8577" target="_blank" rel="noopener">Nippro Shinsekai: Episode 8 recap (in Japanese)</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japan_ryourirecipi-8604" target="_blank" rel="noopener">Nippro Shinsekai: trainee cooking recipes roundup (in Japanese)</a></li>',
         '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">Related articles: Taiga Fujimaki &amp; Nippro Shinsekai</p>\n<ul style="margin:0;padding-left:1.3em;">\n'
         f'<li><a href="{WIKI}" target="_blank" rel="noopener">Wiki-style profile of Taiga Fujimaki (in Japanese)</a></li>\n'
         f'<li><a href="{FANMI}" target="_blank" rel="noopener">Taiga Fujimaki\'s free fan meeting: date, venue and details (in Japanese)</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_zense-2748" target="_blank" rel="noopener">Nippro Shinsekai: trainee backgrounds list (in Japanese)</a></li>\n'
         '<li><a href="https://chomoand-1.com/produce101japanshinsekai_8matome-8577" target="_blank" rel="noopener">Nippro Shinsekai: Episode 8 recap (in Japanese)</a></li>'),
    ],
}

for pid, repls in PATCHES.items():
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers={"Authorization": f"Basic {AUTH}"})
    r.raise_for_status()
    c = r.json()["content"]["raw"]
    ok = True
    for old, new in repls:
        if old not in c:
            print(f"  [{pid}] NOT FOUND: {old[:60]!r}")
            ok = False
        else:
            c = c.replace(old, new, 1)
    if not ok:
        print(f"[{pid}] aborted, no changes pushed")
        continue
    up = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}",
                       headers=H, data=json.dumps({"content": c, "status": "draft"}).encode("utf-8"))
    up.raise_for_status()
    j = up.json()
    plain = len(__import__("re").sub(r"<[^>]+>|<!--.*?-->", "", j["content"]["raw"]))
    print(f"[{pid}] updated -> {j['status']}, chars={plain}")
