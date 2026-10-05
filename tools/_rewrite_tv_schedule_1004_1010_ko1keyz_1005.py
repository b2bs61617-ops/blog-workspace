# -*- coding: utf-8 -*-
"""10/5 rewrite: KO1KEYZ TV schedule 10/4-10/10 (JP/KR/EN) — add ONE MORNING, AWA, プレミアMelodiX!, バズリズム02."""
import re
REPO = r"C:\Users\s30se\Desktop\blog-workspace"
TD = 'border:1px solid #ddd9d3;padding:8px 10px;'
TDC = 'background:#f7f6f4;border:1px solid #ddd9d3;padding:8px 10px;'
CHK = '<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid #8a8378;border-radius:3px;color:#8a8378;font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>'


def row(d, p, tv=False):
    s = TDC if tv else TD
    if tv:
        d, p = f"<strong>{d}</strong>", f"<strong>{p}</strong>"
    return f'<tr><td style="{s}">{d}</td><td style="{s}">{p}</td></tr>\n'


def box(lines):
    inner = "".join(f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}</strong>{v}</p>\n' for i, (k, v) in enumerate(lines))
    return f'<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-left:4px solid #8a8378;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f6f4;">\n{inner}</div>\n<!-- /wp:html -->\n\n'


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n'


def para(*ls):
    return '<!-- wp:paragraph -->\n<p>' + "<br>\n".join(ls) + '</p>\n<!-- /wp:paragraph -->\n\n'


def rep(c, old, new, count=1):
    n = c.count(old)
    assert n == count, (old[:60], n)
    return c.replace(old, new)


def ins_before(c, anchor, new):
    assert c.count(anchor) == 1, anchor[:60]
    return c.replace(anchor, new + anchor)


def ins_after(c, anchor, new):
    assert c.count(anchor) == 1, anchor[:60]
    return c.replace(anchor, anchor + new)


def find_row(c, first_cell):
    m = re.search(r'<tr><td style="border:1px solid #ddd9d3;padding:8px 10px;">' + re.escape(first_cell) + r'</td>.*?</tr>\n', c)
    assert m, first_cell
    return m.group(0)


# ---------------- JP ----------------
f = REPO + r"\articles\ko1keyz_tv_schedule_1004_1010.html"
c = open(f, encoding="utf-8").read()
c = rep(c, '地上波は10/7(水)の日本テレビ「DayDay.」、そして10/8(木)はMnet「M COUNTDOWN」の日韓同時生放送</span></strong>が公式に発表されている出演番組でした。',
        '地上波は10/7(水)の日本テレビ「DayDay.」と10/9(金)深夜の「バズリズム02」、10/5(月)深夜のテレビ東京「プレミアMelodiX!」、そして10/8(木)はMnet「M COUNTDOWN」の日韓同時生放送</span></strong>が公式に発表されている出演番組です。<br>\n'
        'さらにTOKYO FM「ONE MORNING」へのコメント出演や、AWAラウンジでのボイスコメント出演も加わり、デビュー週は月曜から金曜まで毎日何かしらの出演がある1週間になりました。')
c = rep(c, '10月3日時点', '10月5日時点', 3)
c = rep(c, '<li>同じ週の配信番組・MV放送</li>', '<li>「プレミアMelodiX!」「バズリズム02」の放送日時</li>\n<li>ラジオ・AWAラウンジの出演</li>\n<li>同じ週の配信番組・MV放送</li>')
first = find_row(c, '10/5(月)深夜25:00〜28:00')
c = ins_before(c, first, row('10/5(月)6:30頃', 'TOKYO FM/JFN「ONE MORNING」(SIYOUNG・YOSHIKI・YUKIがコメント出演)')
               + row('10/5(月)20:00〜21:00', 'AWAラウンジ デビューシングルリリース記念SP(ボイスコメント出演・無料)'))
c = ins_after(c, first, row('10/5(月)深夜26:50〜27:20', 'テレビ東京「プレミアMelodiX!」', True))
c = ins_before(c, find_row(c, '10/9(金)深夜25:30〜'), row('10/9(金)深夜24:59〜25:59', '日本テレビ「バズリズム02」', True))
c = rep(c, '<p>テレビ出演が集中しているのは、デビュー当日の10/7(水)と翌日の10/8(木)の2日間です。<br>\n',
        '<p>テレビ出演は、デビュー前夜にあたる10/5(月)深夜の「プレミアMelodiX!」から始まり、デビュー当日の10/7(水)、翌日の10/8(木)、そして10/9(金)深夜の「バズリズム02」まで続きます。<br>\n')
sec = (h2('深夜の音楽番組「プレミアMelodiX!」「バズリズム02」にも出演')
       + box([('プレミアMelodiX!:', '10/5(月)深夜26:50〜27:20 テレビ東京'), ('バズリズム02:', '10/9(金)深夜24:59〜25:59 日本テレビ')])
       + para('デビュー週は、朝の情報番組や韓国の音楽番組だけでなく、日本の深夜音楽番組にも2本出演します。',
              'どちらも公式サイトのメディア情報・ニュースで出演が告知されている番組です。')
       + h3('10/5(月)深夜 テレビ東京「プレミアMelodiX!」')
       + para('1本目は、10月6日(火)2:50〜3:20(10/5の月曜深夜26:50〜)放送のテレビ東京「プレミアMelodiX!」です。',
              'ナビゲーターは南海キャンディーズの2人で、番組公式サイトでは次回ゲストとして<strong>KO1KEYZと須田景凪さん</strong>の名前が発表されています。',
              '山里亮太さんは、10/7に出演する「DayDay.」のMCでもあるので、デビュー前夜とデビュー当日の朝に続けて顔を合わせることになりますね。',
              '番組公式サイトでも放送時間が変わる可能性があると案内されているため、録画予約は番組表で時間を確認してからが安心です。')
       + h3('10/9(金)深夜 日本テレビ「バズリズム02」')
       + para('2本目は、10月9日(金)24:59〜25:59(10/10の0:59〜)放送の日本テレビ「バズリズム02」です。',
              'バカリズムさんがMCを務める音楽番組で、KO1KEYZ公式サイトで出演決定が発表されました。',
              'デビュー曲のリリースから2日後の放送なので、デビュー直後のメンバーの様子が見られる番組になりそうです。',
              'ただし、トークのみかパフォーマンスもあるのか、披露曲は10月5日時点では発表されていません。')
       + h3('ラジオ「ONE MORNING」とAWAラウンジにもコメント出演')
       + para('テレビ以外では、10月5日(月)のTOKYO FM/JFN「ONE MORNING」(6:00〜9:00)に、SIYOUNG・YOSHIKI・YUKIの3人がコメントで出演しました(6:30頃の出演予定と告知)。',
              '同じ日の20:00〜21:00には、音楽アプリAWAのAWAラウンジで「KO1KEYZ 新世界への扉をUnlock！〜デビューシングルリリース記念SP〜」が開催されます。',
              'メンバーがボイスコメントで登場し、デビューシングル「KO1KEYZ」の制作エピソードや、メンバーを深掘りするトークコーナーが予定されています。',
              'AWAアプリを入れれば誰でも無料で参加できるので、テレビの前に気軽に楽しめるコンテンツです。'))
c = ins_before(c, h2('今週お休みの番組は？M:ZINEの次回放送日'), sec)
c = rep(c, '毎週録画予約をしている方は、10/9の回はKO1KEYZが出ないので注意してください。<br>\n',
        '毎週録画予約をしている方は、10/9の回はKO1KEYZが出ないので注意してください。<br>\n'
        'その代わり、同じ金曜深夜は日本テレビ「バズリズム02」(24:59〜)にKO1KEYZが出演するので、こちらの録画を忘れないようにしておきましょう。<br>\n')
c = rep(c, '10/8(木)18:00〜20:00 Mnet「M COUNTDOWN」日韓同時生放送<br>\n',
        '10/8(木)18:00〜20:00 Mnet「M COUNTDOWN」日韓同時生放送<br>\n'
        + CHK + '10/5(月)深夜26:50 テレ東「プレミアMelodiX!」、10/9(金)深夜24:59 日テレ「バズリズム02」<br>\n'
        + CHK + '10/5(月)はONE MORNINGにコメント出演、20:00からAWAラウンジ<br>\n')
open(f, "w", encoding="utf-8").write(c)

# ---------------- KR ----------------
f = REPO + r"\articles\ko1keyz_tv_schedule_1004_1010_kr.html"
c = open(f, encoding="utf-8").read()
c = rep(c, "지상파는 10/7(수) 니혼TV 'DayDay.', 그리고 10/8(목)에는 Mnet 'M COUNTDOWN' 한일 동시 생방송</span></strong>이 공식 발표된 출연 프로그램이었어요.",
        "지상파는 10/7(수) 니혼TV 'DayDay.'와 10/10(토) 새벽 '버즈리듬02', 10/6(화) 새벽 TV도쿄 '프리미어 MelodiX!', 그리고 10/8(목)에는 Mnet 'M COUNTDOWN' 한일 동시 생방송</span></strong>이 공식 발표된 출연 프로그램이에요.<br>\n"
        "여기에 TOKYO FM 'ONE MORNING' 코멘트 출연과 AWA 라운지 보이스 코멘트 출연까지 더해져, 데뷔 주간은 월요일부터 금요일까지 매일 출연이 있는 일주일이 됐어요.")
c = rep(c, '10월 3일 기준', '10월 5일 기준', 3)
c = rep(c, '<li>같은 주의 온라인 콘텐츠·MV 방송</li>', "<li>'프리미어 MelodiX!'·'버즈리듬02' 방송 일시</li>\n<li>라디오·AWA 라운지 출연</li>\n<li>같은 주의 온라인 콘텐츠·MV 방송</li>")
first = find_row(c, '10/6(화) 1:00~4:00')
c = ins_before(c, first, row('10/5(월) 6:30경', "TOKYO FM/JFN 'ONE MORNING'(SIYOUNG·YOSHIKI·YUKI 코멘트 출연)")
               + row('10/5(월) 20:00~21:00', 'AWA 라운지 데뷔 싱글 발매 기념 SP(보이스 코멘트 출연·무료)'))
c = ins_after(c, first, row('10/6(화) 2:50~3:20', "TV도쿄 '프리미어 MelodiX!'", True))
c = ins_before(c, find_row(c, '10/10(토) 1:30~'), row('10/10(토) 0:59~1:59', "니혼TV '버즈리듬02'", True))
c = rep(c, '<p>TV 출연이 몰려 있는 날은 데뷔 당일인 10/7(수)과 다음 날인 10/8(목) 이틀이에요.<br>\n',
        "<p>TV 출연은 데뷔 전야인 10/6(화) 새벽의 '프리미어 MelodiX!'부터 시작해 데뷔 당일 10/7(수), 다음 날 10/8(목), 그리고 10/10(토) 새벽 '버즈리듬02'까지 이어져요.<br>\n")
sec = (h2("심야 음악 프로그램 '프리미어 MelodiX!'·'버즈리듬02'에도 출연")
       + box([('프리미어 MelodiX!:', '10/6(화) 2:50~3:20 TV도쿄(10/5 월요일 심야)'), ('버즈리듬02:', '10/10(토) 0:59~1:59 니혼TV(10/9 금요일 심야)')])
       + para('데뷔 주간에는 아침 정보 프로그램과 한국 음악 방송뿐 아니라, 일본 심야 음악 프로그램에도 2번 출연해요.',
              '두 프로그램 모두 공식 사이트의 미디어 정보·뉴스에서 출연이 공지됐어요.')
       + h3("10/5(월) 심야 TV도쿄 '프리미어 MelodiX!'")
       + para("첫 번째는 10월 6일(화) 2:50~3:20(10/5 월요일 심야) 방송되는 TV도쿄 '프리미어 MelodiX!'예요.",
              "내비게이터는 개그 콤비 난카이캔디즈이고, 프로그램 공식 사이트에 다음 게스트로 <strong>KO1KEYZ와 스다 케이나</strong>가 발표됐어요.",
              "야마사토 료타는 10/7에 출연하는 'DayDay.'의 MC이기도 해서, 데뷔 전야와 데뷔 당일 아침에 연달아 만나게 되네요.",
              '방송 시간이 바뀔 수 있다는 안내도 있으니, 편성표에서 시간을 다시 확인해 두면 안심이에요.')
       + h3("10/9(금) 심야 니혼TV '버즈리듬02'")
       + para("두 번째는 10월 10일(토) 0:59~1:59(10/9 금요일 심야) 방송되는 니혼TV '버즈리듬02(バズリズム02)'예요.",
              '바카리즘이 MC를 맡은 음악 프로그램으로, KO1KEYZ 공식 사이트에서 출연 확정이 발표됐어요.',
              '데뷔곡 발매 이틀 뒤 방송이라, 데뷔 직후 멤버들의 모습을 볼 수 있는 프로그램이 될 것 같아요.',
              '다만 토크만 하는지 무대도 있는지, 무대 곡은 10월 5일 기준 발표되지 않았어요.')
       + h3("라디오 'ONE MORNING'과 AWA 라운지에도 코멘트 출연")
       + para("TV 외에도 10월 5일(월) TOKYO FM/JFN 'ONE MORNING'(6:00~9:00)에 SIYOUNG·YOSHIKI·YUKI 세 명이 코멘트로 출연했어요(6:30경 출연 예정으로 공지).",
              "같은 날 20:00~21:00에는 음악 앱 AWA의 AWA 라운지에서 'KO1KEYZ 신세계로의 문을 Unlock! ~데뷔 싱글 발매 기념 SP~'가 열려요.",
              "멤버들이 보이스 코멘트로 등장해 데뷔 싱글 'KO1KEYZ'의 제작 에피소드와 멤버를 깊이 파고드는 토크 코너를 전할 예정이에요.",
              'AWA 앱만 있으면 누구나 무료로 참여할 수 있어요.'))
c = ins_before(c, h2('이번 주 쉬는 프로그램은? M:ZINE 다음 방송일'), sec)
c = rep(c, "10/8(목) 18:00~20:00 Mnet 'M COUNTDOWN' 한일 동시 생방송<br>\n",
        "10/8(목) 18:00~20:00 Mnet 'M COUNTDOWN' 한일 동시 생방송<br>\n"
        + CHK + "10/6(화) 2:50 TV도쿄 '프리미어 MelodiX!', 10/10(토) 0:59 니혼TV '버즈리듬02'<br>\n"
        + CHK + '10/5(월) ONE MORNING 코멘트 출연, 20:00부터 AWA 라운지<br>\n')
open(f, "w", encoding="utf-8").write(c)

# ---------------- EN ----------------
f = REPO + r"\articles\ko1keyz_tv_schedule_1004_1010_en.html"
c = open(f, encoding="utf-8").read()
c = rep(c, 'the officially announced TV appearances are Nippon TV\'s "DayDay." on Wed 10/7 and Mnet\'s "M COUNTDOWN," broadcast live in Japan and Korea, on Thu 10/8</span></strong>.',
        'the officially announced TV appearances are TV Tokyo\'s "Premier MelodiX!" (early hours of Tue 10/6), Nippon TV\'s "DayDay." on Wed 10/7, Mnet\'s "M COUNTDOWN," broadcast live in Japan and Korea, on Thu 10/8, and Nippon TV\'s "Buzz Rhythm 02" (early hours of Sat 10/10)</span></strong>.<br>\n'
        'Add a comment appearance on TOKYO FM\'s "ONE MORNING" and voice comments in an AWA Lounge, and there is something every day from Monday to Friday.')
c = rep(c, 'as of October 3', 'as of October 5', 3)
c = rep(c, '<li>Streaming content and MV airings that week</li>', '<li>When "Premier MelodiX!" and "Buzz Rhythm 02" air</li>\n<li>Radio and AWA Lounge appearances</li>\n<li>Streaming content and MV airings that week</li>')
first = find_row(c, 'Tue 10/6 1:00-4:00')
c = ins_before(c, first, row('Mon 10/5 around 6:30', 'TOKYO FM/JFN "ONE MORNING" (comments from SIYOUNG, YOSHIKI and YUKI)')
               + row('Mon 10/5 20:00-21:00', 'AWA Lounge debut single release special (voice comments, free)'))
c = ins_after(c, first, row('Tue 10/6 2:50-3:20', 'TV Tokyo "Premier MelodiX!"', True))
c = ins_before(c, find_row(c, 'Sat 10/10 1:30'), row('Sat 10/10 0:59-1:59', 'Nippon TV "Buzz Rhythm 02"', True))
c = rep(c, '<p>The TV appearances are packed into two days: debut day on Wednesday 10/7 and the following Thursday 10/8.<br>\n',
        '<p>The TV appearances start with "Premier MelodiX!" in the early hours of Tuesday 10/6, peak on debut day (Wed 10/7) and the following Thursday 10/8, and wrap up with "Buzz Rhythm 02" in the early hours of Saturday 10/10.<br>\n')
sec = (h2('Late-night music shows: "Premier MelodiX!" and "Buzz Rhythm 02"')
       + box([('Premier MelodiX!:', 'Tue 10/6 2:50-3:20, TV Tokyo (Monday late night)'), ('Buzz Rhythm 02:', 'Sat 10/10 0:59-1:59, Nippon TV (Friday late night)')])
       + para('Besides the morning show and the Korean music show, KO1KEYZ also appears on two Japanese late-night music programs during debut week.',
              'Both appearances have been announced in the media and news sections of the official website.')
       + h3('"Premier MelodiX!" on TV Tokyo (late Monday 10/5)')
       + para('The first is TV Tokyo\'s "Premier MelodiX!", airing Tuesday, October 6, 2:50-3:20 (late Monday night).',
              'The show is hosted by the comedy duo Nankai Candies, and the official website lists <strong>KO1KEYZ and Keina Suda</strong> as the next guests.',
              'Ryota Yamasato is also an MC of "DayDay.", so the members will meet him on the night before their debut and again on debut-day morning.',
              'The official site notes that the airtime may change, so double-check the listings before setting a recording.')
       + h3('"Buzz Rhythm 02" on Nippon TV (late Friday 10/9)')
       + para('The second is Nippon TV\'s "Buzz Rhythm 02", airing Saturday, October 10, 0:59-1:59 (late Friday night).',
              'It is a music show hosted by Bakarhythm, and the KO1KEYZ official site announced the appearance.',
              'It airs two days after the debut single\'s release, so it should give a look at the members right after their debut.',
              'Whether they will perform, and which song, had not been announced as of October 5.')
       + h3('Radio "ONE MORNING" and AWA Lounge')
       + para('Outside TV, SIYOUNG, YOSHIKI and YUKI appeared via comments on TOKYO FM/JFN\'s "ONE MORNING" (6:00-9:00) on Monday, October 5 (announced for around 6:30).',
              'The same day from 20:00 to 21:00, the music app AWA hosts the AWA Lounge "KO1KEYZ Unlock the Door to a New World! Debut Single Release Special".',
              'The members join with voice comments, sharing stories behind the debut single "KO1KEYZ" and a talk segment that digs into each member.',
              'Anyone can join for free with the AWA app.'))
c = ins_before(c, h2('Which show is off this week? Next "M:ZINE" airdate'), sec)
c = rep(c, 'Thu 10/8, 18:00-20:00: Mnet "M COUNTDOWN," live in Japan and Korea<br>\n',
        'Thu 10/8, 18:00-20:00: Mnet "M COUNTDOWN," live in Japan and Korea<br>\n'
        + CHK + 'Tue 10/6 2:50: TV Tokyo "Premier MelodiX!"; Sat 10/10 0:59: Nippon TV "Buzz Rhythm 02"<br>\n'
        + CHK + 'Mon 10/5: comments on ONE MORNING, AWA Lounge from 20:00<br>\n')
open(f, "w", encoding="utf-8").write(c)
print("ok")
