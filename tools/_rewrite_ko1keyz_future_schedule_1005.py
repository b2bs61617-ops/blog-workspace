# -*- coding: utf-8 -*-
"""10/5 rewrite of chomoand-1 10860 (KO1KEYZ 今後のスケジュール). title is NOT changed.
input : articles/ko1keyz_future_schedule_1005.html (= live content as of 10/5, same as 0927 version)
output: same file, rewritten in place.  backup: backups/post_10860_before_1005.html"""
import re
REPO = r"C:\Users\s30se\Desktop\blog-workspace"
f = REPO + r"\articles\ko1keyz_future_schedule_1005.html"
c = open(f, encoding="utf-8").read()
open(REPO + r"\backups\post_10860_before_1005.html", "w", encoding="utf-8").write(c)

TD = 'border:1px solid #ddd9d3;padding:8px 10px;'
TDC = 'background:#f7f6f4;border:1px solid #ddd9d3;padding:8px 10px;'
CHK = '<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid #8a8378;border-radius:3px;color:#8a8378;font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>'
H2 = '<!-- wp:heading {{"className":"wp-block-heading"}} -->\n<h2 class="wp-block-heading">{}</h2>\n<!-- /wp:heading -->\n\n'
H3 = '<!-- wp:heading {{"level":3,"className":"wp-block-heading"}} -->\n<h3 class="wp-block-heading">{}</h3>\n<!-- /wp:heading -->\n\n'


def rep(c, old, new, count=1):
    n = c.count(old)
    assert n == count, (old[:70], n)
    return c.replace(old, new)


def para(*ls):
    return '<!-- wp:paragraph -->\n<p>' + "<br>\n".join(ls) + '</p>\n<!-- /wp:paragraph -->\n\n'


def box(lines):
    inner = "".join(f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}</strong>{v}</p>\n' for i, (k, v) in enumerate(lines))
    return f'<!-- wp:html -->\n<div style="border:1px solid #ddd9d3;border-left:4px solid #8a8378;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f6f4;">\n{inner}</div>\n<!-- /wp:html -->\n\n'


def h2(t): return H2.format(t)
def h3(t): return H3.format(t)


# ---- 導入 ----
old_intro = re.search(r'<!-- wp:paragraph -->\n<p>『PRODUCE 101 JAPAN 新世界』出身.*?<!-- /wp:paragraph -->\n\n<!-- wp:paragraph -->\n<p>この記事では.*?<!-- /wp:paragraph -->\n\n', c, re.S).group(0)
c = rep(c, old_intro, para(
    '『PRODUCE 101 JAPAN 新世界』出身の12人組ボーイズグループKO1KEYZ(コイキーズ)は、<strong>2026年10月7日(水)</strong>にデビューシングル「KO1KEYZ」で日韓同時デビューを迎えます。',
    'デビュー週には出演情報が次々と追加され、<strong><span class="swl-marker mark_yellow">10/5深夜のテレビ東京「プレミアMelodiX!」、10/7の日本テレビ「DayDay.」、10/8のMnet「M COUNTDOWN」日韓同時生放送、10/9深夜の日本テレビ「バズリズム02」</span></strong>と、地上波・韓国の音楽番組への出演が続きます。',
    'さらにデビュー後も、韓国盤のファンサイン会が10/16と10/17の2回、11月にはソウルでのファンミーティングが控えています。')
    + para(
    'この記事では、公式サイト・各番組の発表をもとに、10月5日からデビュー後の11月までの予定を日付順に整理しました。',
    'すでに終わった9/28〜10/3の出演や7〜9月のできごとは、記事の後半にまとめています。',
    '※2026年10月5日時点の情報です。日程・時間は変更になる可能性があるため、最新情報は公式でご確認ください。'))

c = rep(c, '<li>9/28〜11月のスケジュール早見表</li>\n<li>テレビ・配信の出演予定と見方</li>',
        '<li>10/5〜11月のスケジュール早見表</li>\n<li>デビュー週のテレビ・ラジオ出演</li>')
c = rep(c, '<li>終了した7〜9月のできごと</li>', '<li>終了した9/28〜10/3の出演と7〜9月のできごと</li>')

# ---- 早見表 ----
c = rep(c, 'KO1KEYZのスケジュール早見表(9/28〜11月)', 'KO1KEYZのスケジュール早見表(10/5〜11月)')
rows = [
    ('10/5(月)6:30頃', 'TOKYO FM/JFN「ONE MORNING」(SIYOUNG・YOSHIKI・YUKIがコメント出演)', False),
    ('10/5(月)', 'S Cawaii! ME 2026 AUTUMN・別冊カドカワScene 18 発売', False),
    ('10/5(月)〜10/11(日)', '大型広告掲出(東急東横線渋谷駅・阪急大阪梅田駅)', False),
    ('10/5(月)20:00〜21:00', 'AWAラウンジ「KO1KEYZ 新世界への扉をUnlock！」(無料)', False),
    ('10/5(月)深夜26:50〜27:20', 'テレビ東京「プレミアMelodiX!」', True),
    ('10/6(火)', 'DEBUT SHOWCASE(16:00/19:30開演)・タワレコ渋谷店イベント', False),
    ('<strong>10/7(水)</strong>', '<strong>デビューシングル「KO1KEYZ」発売・日韓同時デビュー</strong>', False),
    ('10/7(水)9:00〜11:10', '日本テレビ「DayDay.」', True),
    ('10/7(水)14:00頃〜', '公式YouTube「デビュー日スペシャル生配信」', True),
    ('10/7(水)〜10/18(土)', 'メンバー選曲プレイリストを1日1人ずつ公開', False),
    ('〜10/8(木)', 'キュントゥグンPOP-UP＠新宿サザンテラス', False),
    ('10/8(木)18:00〜20:00', 'Mnet「M COUNTDOWN」(日韓同時生放送)', True),
    ('10/8(木)19:00〜', 'Lemino「KO1KEYZ学園 #2」・DAIKI誕生日', True),
    ('10/9(金)深夜24:59〜25:59', '日本テレビ「バズリズム02」', True),
    ('10/16(金)', '韓国盤 FANSIGN(20:00 KST)&amp;1:1 VIDEO CALL(22:00 KST)[MAKESTAR]', False),
    ('10/16(金)・10/23(金)25:30〜', 'テレビ朝日「M:ZINE」2・3週目', True),
    ('10/17', '韓国盤 FANSIGN(19:00 KST)&amp;1:1 VIDEO CALL[Mnet Plus Chat]', False),
    ('10/25(日)12:00〜13:30', 'CSテレ朝チャンネル1「M:ZINE」90分拡大版', True),
    ('11/7(土)・11/8(日)', '1ST FAN MEETING IN SEOUL(計4公演)', False),
]
m = re.search(r'(<tr><td style="background:#8a8378;[^\n]*\n)(.*?)(</tbody></table></figure>)', c, re.S)
body = ''.join(f'<tr><td style="{TDC if tv else TD}">{d}</td><td style="{TDC if tv else TD}">{p}</td></tr>\n' for d, p, tv in rows)
c = c[:m.start(2)] + body + c[m.end(2):]
c = rep(c, '「M:ZINE」の25:30は、翌日の深夜1:30のことです。<br>\n10月2日(金)の放送なら、日付が変わった10月3日(土)の午前1時30分からになるので、録画予約の際は曜日を間違えないようにしておきましょう。',
        '深夜の「26:50」「24:59」「25:30」は、日付が変わった翌日の時刻のことです。<br>\n'
        'たとえば10/5(月)深夜26:50の「プレミアMelodiX!」は10月6日(火)の午前2時50分から、10/9(金)深夜24:59の「バズリズム02」は10月10日(土)の午前0時59分からになるので、録画予約の際は曜日を間違えないようにしておきましょう。')

# ---- 9/28〜10/3 の出演 → 終了分へ移動 ----
m = re.search(r'<!-- wp:heading \{"className":"wp-block-heading"\} -->\n<h2 class="wp-block-heading">テレビ・配信の出演予定\(9/28〜10/3\)</h2>.*?(?=<!-- wp:heading \{"className":"wp-block-heading"\} -->\n<h2 class="wp-block-heading">デビュー週のイベント)', c, re.S)
old_tv = m.group(0)
done_tv = old_tv.replace('テレビ・配信の出演予定(9/28〜10/3)', '【終了分】デビュー直前の出演(9/28〜10/3)')
new_tv = (h2('デビュー週のテレビ・ラジオ出演(10/5〜10/9)')
          + box([('地上波:', 'プレミアMelodiX!(10/5深夜)、DayDay.(10/7)、バズリズム02(10/9深夜)'),
                 ('韓国の音楽番組:', 'M COUNTDOWN(10/8・日韓同時生放送)'),
                 ('ラジオ・配信:', 'ONE MORNING(10/5)、AWAラウンジ(10/5)、YouTube生配信(10/7)、学園#2(10/8)')])
          + para('デビュー週の出演は、公式サイトのメディア情報・ニュースで発表されたものだけでも地上波3番組、韓国の音楽番組1本、ラジオと配信が並びます。',
                 '1週間分の番組を日付順に詳しくまとめた<a href="https://chomoand-1.com/ko1keyz-tv-schedule-1004-1010-14165">10/4〜10/10のテレビ出演まとめ</a>もあわせてチェックしてみてください。')
          + h3('10/5(月)ONE MORNING・AWAラウンジ・プレミアMelodiX!')
          + para('デビュー週の初日は、TOKYO FM/JFN「ONE MORNING」(6:00〜9:00)にSIYOUNG・YOSHIKI・YUKIの3人がコメントで出演しました(6:30頃の出演予定と告知)。',
                 '夜20:00〜21:00には、音楽アプリAWAのAWAラウンジで「KO1KEYZ 新世界への扉をUnlock！〜デビューシングルリリース記念SP〜」が開催され、メンバーがボイスコメントで制作エピソードなどを語ります。',
                 'さらに深夜26:50〜27:20(10/6の2:50〜)には、南海キャンディーズがナビゲーターを務めるテレビ東京「プレミアMelodiX!」に、須田景凪さんとともにゲスト出演します。')
          + h3('10/7(水)日本テレビ「DayDay.」とデビュー日生配信')
          + para('デビュー当日の10月7日(水)は、日本テレビ「DayDay.」(9:00〜11:10)への出演が公式サイトのメディア情報に掲載されています。',
                 '6月8日に「101秒自己PRリレー」で生出演して以来の登場で、出演のコーナーや時間帯は10月5日時点では発表されていません。',
                 '14:00頃からは公式YouTubeチャンネルで「デビュー日スペシャル生配信」があり、ハッシュタグ「#お願いKO1KEYZ」で当日やってほしい企画が募集されています。')
          + h3('10/8(木)Mnet「M COUNTDOWN」日韓同時生放送')
          + para('デビュー翌日の10月8日(木)18:00〜20:00には、韓国の音楽番組「M COUNTDOWN」に出演します。',
                 '日本ではCSのMnetで日韓同時生放送されるほか、Mnet Plusでも視聴できます。',
                 '同じ日の19:00からはLemino「KO1KEYZ学園 #2」、21:00からは公式YouTube「KO1! KO1! KO1KEYZ!」も続き、リーダーDAIKIの誕生日とも重なる1日です。')
          + h3('10/9(金)深夜 日本テレビ「バズリズム02」')
          + para('10月9日(金)24:59〜25:59(10/10の0:59〜)には、バカリズムさんがMCを務める日本テレビの音楽番組「バズリズム02」に出演します。',
                 '公式サイトのニュースで出演決定が発表されていて、披露曲などの詳細は10月5日時点では発表されていません。',
                 'なお、同じ金曜深夜のテレビ朝日「M:ZINE」は、10/9の回はKO1KEYZの出演がないので、録画予約の際は気をつけてください。'))
c = rep(c, old_tv, new_tv)

# ---- デビュー週のイベント ----
c = rep(c, 'デビュー週のイベント(10/1〜10/8)', 'デビュー週のイベント(10/1〜10/11)')
c = rep(c, '<p style="margin:4px 0 0 0;"><strong>イベント:</strong>POP-UP(10/2〜8)、SHOWCASE(10/6)、デビュー(10/7)</p>',
        '<p style="margin:4px 0 0 0;"><strong>イベント:</strong>POP-UP(10/2〜8)、大型広告(10/5〜11)、SHOWCASE(10/6)、デビュー(10/7)</p>')
c = rep(c, '10月1日(木)に<span class="swl-marker mark_orange">MEN\'S PREPPY 11月号</span>、10月2日(金)に<span class="swl-marker mark_orange">日経エンタテインメント!11月号</span>と<span class="swl-marker mark_orange">最強ジャンプ11月号</span>、10月5日(月)に<span class="swl-marker mark_orange">S Cawaii! ME 2026 AUTUMN</span>と<span class="swl-marker mark_orange">別冊カドカワScene 18</span>が発売予定です。',
        '10月1日(木)に<span class="swl-marker mark_orange">MEN\'S PREPPY 11月号</span>、10月2日(金)に<span class="swl-marker mark_orange">日経エンタテインメント!11月号</span>と<span class="swl-marker mark_orange">最強ジャンプ11月号</span>、10月5日(月)に<span class="swl-marker mark_orange">S Cawaii! ME 2026 AUTUMN</span>と<span class="swl-marker mark_orange">別冊カドカワScene 18</span>が発売されました。')
c = rep(c, '10月3日(土)・4日(日)の2日間だけは、メンバーが名付けたオリジナルドリンク「キュントゥグンDRINK」の販売と、デビューシングルの予約受付(3形態セットで限定トレカ付き)も行われます。<br>\nドリンクの支払いは現金が使えずキャッシュレスのみなので、行く予定の人は準備しておくと安心です。',
        '10月3日(土)・4日(日)の2日間は、メンバーが名付けたオリジナルドリンク「キュントゥグンDRINK」の販売と、デビューシングルの予約受付(3形態セットで限定トレカ付き)も行われました。<br>\n'
        '最終日は10月8日(木)なので、パネルや映像の展示を見に行くなら日程に注意してください。<br>\n'
        '会場の様子は<a href="https://chomoand-1.com/ko1keyz-kyuntugun-popup-shinjuku-13734">キュントゥグンPOP-UPのレポ記事</a>でも紹介しています。')
ad_anchor = H3.format('10/6 DEBUT SHOWCASE・タワレコ渋谷店イベント')
c = rep(c, ad_anchor, h3('10/5〜11 渋谷駅・大阪梅田駅に大型広告')
        + para('デビューシングルのリリースを記念して、10月5日(月)〜11日(日)の1週間、東京と大阪の2都市で大型広告が掲出されます。',
               '場所は<span class="swl-marker mark_orange">東急東横線渋谷駅「ビッグ20」</span>と<span class="swl-marker mark_orange">阪急大阪梅田駅「D-St.(ディーストリート)」①〜④</span>です。',
               '見に行った際は、公式が呼びかけているハッシュタグ「#KO1KEYZに会いに恋」をつけてSNSでシェアできます。',
               '駅や近隣施設への問い合わせは控えるよう案内されているので、立ち止まる際は周りの通行の邪魔にならないよう気をつけましょう。')
        + ad_anchor)
c = rep(c, '<p>デビュー翌日の10月8日(木)は、リーダーを務める<span class="swl-marker mark_orange">DAIKIの誕生日</span>です。<br>\n同じ日の19:00にはLeminoで「KO1KEYZ学園 #2」が配信され、21時には「KO1! KO1! KO1KEYZ!」の更新日(毎週木曜)も重なります。<br>\n',
        '<p>デビュー翌日の10月8日(木)は、リーダーを務める<span class="swl-marker mark_orange">DAIKIの誕生日</span>です。<br>\n同じ日の18:00からはMnet「M COUNTDOWN」の生放送、19:00にはLeminoで「KO1KEYZ学園 #2」が配信され、21時には「KO1! KO1! KO1KEYZ!」の更新日(毎週木曜)も重なります。<br>\n')
pl_anchor = H3.format('10/8 DAIKIの誕生日・「KO1KEYZ学園 #2」')
c = rep(c, pl_anchor, h3('10/7〜18 メンバー選曲プレイリストを毎日公開')
        + para('デビューシングルのリリースを記念して、「KO1KEYZが選ぶ！君に会う前に聴きたいキュントゥグン♡プレイリスト」が10月7日から1日1人ずつ公開されます。',
               '順番は10/7 YOSHIKI、10/8 DAIKI、10/9 SIYOUNG、10/10 SHINHAENG、10/11 YURA、10/12 RYUJI、10/13 KEITO、10/14 ISSA、10/15 RYOGA、10/16 TOWA、10/17 KOSUKE、10/18 YUKIです。',
               '公開スケジュールや選ばれた曲は<a href="https://chomoand-1.com/ko1keyz-member-playlist-14182">メンバー選曲プレイリストのまとめ記事</a>で紹介しています。')
        + pl_anchor)

# ---- デビュー後 ----
c = rep(c, '<p style="margin:0;"><strong>10月:</strong>韓国盤FANSIGN&amp;VIDEO CALL(10/16)、M:ZINE(10/16・23)、CS拡大版(10/25)</p>',
        '<p style="margin:0;"><strong>10月:</strong>韓国盤FANSIGN&amp;VIDEO CALL(10/16・10/17)、M:ZINE(10/16・23)、CS拡大版(10/25)</p>')
c = rep(c, '10/16 韓国盤のFANSIGN&amp;1:1 VIDEO CALL EVENT', '10/16・10/17 韓国盤のFANSIGN&amp;1:1 VIDEO CALL EVENT')
c = rep(c, '応募はMAKESTARで対象商品を購入する形で、受付期間は9月29日(火)23:59(KST)まで、日本時間なら同じ日の23:59なので、狙っている人は締め切りに注意してください。</p>\n<!-- /wp:paragraph -->\n\n',
        '応募はMAKESTARで対象商品を購入する形で、受付は9月29日(火)23:59(KST)で締め切られています。</p>\n<!-- /wp:paragraph -->\n\n'
        + para('さらに9月30日には、2回目となる<span class="swl-marker mark_yellow">Mnet Plus Chat主催のFANSIGN&amp;1:1 VIDEO CALL EVENT</span>の開催も発表されました。',
               'こちらは10月17日の<span class="swl-marker mark_orange">19:00(KST)からカフェで行われる対面ファンサイン会(当選50名)</span>で、終了後には参加者向けのハイバイ会も予定されています。',
               '1:1ビデオ通話はファンサイン会のあとに行われ、当選人数は1回目と同じく各メンバー15名(計180名)です。',
               '対象は韓国盤のPHOTO DIARY Ver.で、KO1KEYZ SHOPでの購入が応募条件になり、応募期間は10月6日(火)23:59(KST)までです。',
               'なお、公式の告知では「10月17日(金)」と書かれていますが、2026年10月17日は土曜日なので、正確な日程はMnet Plus Chatのイベントページでも確認しておくと安心です。'))
c = rep(c, '間の10月9日の放送回には登場しないため、3週連続ではない点に気をつけてください。',
        '間の10月9日の放送回には登場しないため、3週連続ではない点に気をつけてください(10/9の深夜は日本テレビ「バズリズム02」に出演します)。')

# ---- 終了分: 9/28〜10/3 の出演を7〜9月ダイジェストの前に置く ----
dig = H2.format('【終了分】7〜9月のできごとダイジェスト')
c = rep(c, dig, done_tv + dig)

# ---- まとめ ----
c = rep(c, '<strong>9/28〜10/3</strong>:Lemino Behind #2(9/28)、学園#1&amp;KO1! KO1! KO1KEYZ!(10/1)、M:ZINE(10/2深夜)、MUSIC FAIR(10/3)<br>\n',
        '<strong>テレビ・ラジオ</strong>:ONE MORNING&amp;AWAラウンジ(10/5)、プレミアMelodiX!(10/5深夜)、DayDay.(10/7)、M COUNTDOWN(10/8)、バズリズム02(10/9深夜)<br>\n')
c = rep(c, '<strong>デビュー週</strong>:雑誌5誌(10/1〜5)、POP-UP＠新宿サザンテラス(10/2〜8)、SHOWCASE(10/6)、デビュー(10/7)、DAIKI誕生日&amp;学園#2(10/8)<br>\n',
        '<strong>デビュー週</strong>:大型広告(10/5〜11)、SHOWCASE(10/6)、デビュー&amp;YouTube生配信(10/7)、POP-UP最終日・DAIKI誕生日&amp;学園#2(10/8)、選曲プレイリスト(10/7〜18)<br>\n')
c = rep(c, '<strong>10月中旬〜</strong>:韓国盤FANSIGN&amp;VIDEO CALL(10/16)、M:ZINE(10/16・23)、CS拡大版(10/25)<br>\n',
        '<strong>10月中旬〜</strong>:韓国盤FANSIGN&amp;VIDEO CALL(10/16・10/17)、M:ZINE(10/16・23)、CS拡大版(10/25)<br>\n')
c = rep(c, '<p>デビュー直前の1週間は、配信・地上波・イベントが毎日のように続く、ファンにとっても忙しい期間になりそうです。<br>\n',
        '<p>デビュー週は、地上波・韓国の音楽番組・ラジオ・配信が毎日のように続く、ファンにとっても忙しい1週間になりそうです。<br>\n')
c = rep(c, 'これまでKO1KEYZをあまり追えていなかったという方も、まずは10月3日の「MUSIC FAIR」で12人のパフォーマンスを見てみてはいかがでしょうか!',
        'これまでKO1KEYZをあまり追えていなかったという方も、まずは10月7日の「DayDay.」や10月9日深夜の「バズリズム02」で12人の姿を見てみてはいかがでしょうか!')
c = rep(c, '<li><a href="https://chomoand-1.com/ko1keyz-new-program-will-be-di-11311">',
        '<li><a href="https://chomoand-1.com/ko1keyz-tv-schedule-1004-1010-14165">KO1KEYZのテレビ出演まとめ(10/4〜10/10)</a></li>\n<li><a href="https://chomoand-1.com/ko1keyz-new-program-will-be-di-11311">')

open(f, "w", encoding="utf-8").write(c)
print("ok", len(re.sub(r"<[^>]+>", "", c)))
