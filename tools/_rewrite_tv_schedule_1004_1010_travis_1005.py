# -*- coding: utf-8 -*-
"""10/5 rewrite: Travis Japan TV schedule 10/4-10/10 (chomoand-4 1159).
シューイチ(宮近・松倉)は10/10ではなく10/3放送(STARTO公式=10/3 5:55 VTR出演)だったので削除、
とれたてっ！(七五三掛 10/7 関西テレビ)・夢テレビ2026(中村・吉澤 10/10 SBC)を追加。"""
import re
REPO = r"C:\Users\s30se\Desktop\blog-workspace"
f = REPO + r"\articles\travis_japan_tv_schedule_1004_1010.html"
c = open(f, encoding="utf-8").read()

TD = 'border:1px solid #d9cdee;padding:8px 10px;'
TDC = 'background:#f5f2fb;border:1px solid #d9cdee;padding:8px 10px;'


def rep(c, old, new, count=1):
    n = c.count(old)
    assert n == count, (old[:60], n)
    return c.replace(old, new)


def para(*ls):
    return '<!-- wp:paragraph -->\n<p>' + "<br>\n".join(ls) + '</p>\n<!-- /wp:paragraph -->\n\n'


c = rep(c, '10月3日時点', '10月5日時点')

# --- 早見表: 行を差し替えてストライプを振り直す ---
m = re.search(r'(<tr><td style="background:#7e57c2;[^\n]*\n)(.*?)(</tbody></table></figure>)', c, re.S)
head, body = m.group(1), m.group(2)
rows = re.findall(r'<tr>(.*?)</tr>', body)
cells = [re.findall(r'<td style="[^"]*">(.*?)</td>', r) for r in rows]
cells = [x for x in cells if 'シューイチ' not in x[1]]
assert len(cells) == 10
new = []
for x in cells:
    new.append(x)
    if x[1].startswith('ぽかぽか'):
        pass
    if x[0] == '10/5(月)23:00〜23:30' or x[0] == '<strong>10/5(月)23:00〜23:30</strong>':
        new.append(['10/7(水)13:50〜', '旬感LIVE とれたてっ！(関西テレビ)', '七五三掛龍也'])
    if x[0] == '10/10(土)0:30〜0:59':
        new.append(['10/10(土)9:25〜', '夢テレビ2026(SBC信越放送)', '中村海人・吉澤閑也'])
assert len(new) == 12
out = ''
for i, x in enumerate(new):
    s = TDC if i % 2 == 1 else TD
    out += '<tr>' + ''.join(f'<td style="{s}">{v}</td>' for v in x) + '</tr>\n'
c = c[:m.start(2)] + out + c[m.end(2):]

c = rep(c, '週の後半ほど出演が多く、特に10/10(土)は朝のシューイチから夜のはだかんぼうたちまで4番組が並ぶ忙しい1日でした。',
        '週の後半ほど出演が多く、特に10/10(土)は深夜のHELP ME!!から夜のはだかんぼうたちまで、長野ローカルの番組も含めて4番組が並ぶ忙しい1日です。')

# --- 個人出演ボックス ---
c = rep(c, '<p style="margin:0;"><strong>宮近海斗:</strong>それスノSP・HELP ME!!・シューイチ</p>\n<p style="margin:4px 0 0 0;"><strong>松倉海斗:</strong>それスノSP・シューイチ</p>',
        '<p style="margin:0;"><strong>宮近海斗:</strong>それスノSP・HELP ME!!</p>\n<p style="margin:4px 0 0 0;"><strong>松倉海斗:</strong>それスノSP</p>')
c = rep(c, '<p style="margin:4px 0 0 0;"><strong>吉澤閑也:</strong>リモートシェフ</p>',
        '<p style="margin:4px 0 0 0;"><strong>吉澤閑也:</strong>リモートシェフ・夢テレビ2026(SBC)</p>\n'
        '<p style="margin:4px 0 0 0;"><strong>七五三掛龍也:</strong>とれたてっ！(関西テレビ)</p>\n'
        '<p style="margin:4px 0 0 0;"><strong>中村海人:</strong>夢テレビ2026(SBC)</p>')

# --- HELP ME!! / シューイチ の節 ---
c = rep(c, '<h3 class="wp-block-heading">10/10(土)宮近海斗「HELP ME!!」・宮近&amp;松倉「シューイチ」</h3>',
        '<h3 class="wp-block-heading">10/10(土)宮近海斗「HELP ME!!」に挑戦者として出演</h3>')
old_shu = re.search(r'<!-- wp:paragraph -->\n<p>同じ日の朝は、日本テレビ「シューイチ」.*?<!-- /wp:paragraph -->\n\n', c, re.S).group(0)
c = rep(c, old_shu, para(
    'なお、宮近海斗と松倉海斗がプロのクリーニング術を学ぶ日本テレビ「シューイチ」の企画は、10/10(土)ではなく<strong>10月3日(土)5:55からの放送(VTR出演)</strong>でした。',
    'STARTO ENTERTAINMENT公式サイトの出演情報でも10/3放送として掲載されていて、10/10のシューイチの番組表にはトラジャの名前はありません。',
    '見逃した方は、TVerなどの見逃し配信に残っていないか確認してみてください。'))

# --- ローカル局の節 ---
c = rep(c, '<h3 class="wp-block-heading">CS・関西ローカルの放送もチェック</h3>',
        '<h3 class="wp-block-heading">CS・ローカル局の放送もチェック</h3>')
anchor = '<!-- wp:paragraph -->\n<p>ちなみに10月4日(日)20:50からのテレビ東京'
c = rep(c, anchor, para(
    '10月7日(水)13:50からは、関西テレビの生放送情報番組「旬感LIVE とれたてっ！」に七五三掛龍也が出演します。',
    '同じ日の夜23:00には、七五三掛龍也が出演するカンテレ制作のドラマ「小麦とバターと復讐と」が始まるため、ドラマの初回放送に合わせた出演とみられます。',
    '生放送のため内容が変わる場合があると案内されていて、どのコーナーで登場するかは10月5日時点では発表されていません。')
    + para(
    '10月10日(土)9:25からは、長野県のSBC信越放送「夢テレビ2026」に中村海人と吉澤閑也が出演します。',
    'SBCは長野県のローカル局なので、基本的に長野県内での放送になります。',
    '番組内での2人の役割や出演時間は10月5日時点では発表されていないので、長野にお住まいの方は番組表をチェックしておきましょう。')
    + anchor)

# --- メンバー別表 ---
c = rep(c, 'それスノSP(10/9)・HELP ME!!(10/10)・シューイチ(10/10)', 'それスノSP(10/9)・HELP ME!!(10/10)')
c = rep(c, '>なし(今週はけるとめるのみ)</td></tr>\n<tr><td style="border:1px solid #d9cdee;padding:8px 10px;">七五三掛龍也',
        '>夢テレビ2026(10/10・SBC信越放送)</td></tr>\n<tr><td style="border:1px solid #d9cdee;padding:8px 10px;">七五三掛龍也')
c = rep(c, '>小麦とバターと復讐と(10/7)</td>', '>とれたてっ！(10/7・関西テレビ)・小麦とバターと復讐と(10/7)</td>')
c = rep(c, '>リモートシェフ(10/4)</td>', '>リモートシェフ(10/4)・夢テレビ2026(10/10・SBC信越放送)</td>')
c = rep(c, '>それスノSP(10/9)・シューイチ(10/10)</td>', '>それスノSP(10/9)</td>')
c = rep(c, '個人出演が一番多いのは宮近海斗と松田元太で、どちらも3番組に登場します。<br>\n中村海人と川島如恵留は、関東の地上波ではけるとめるでの出演が中心の週になりました。',
        '個人出演が一番多いのは松田元太で、ぽかぽか・ドッキリGP SP・はだかんぼうたちの3番組に登場します。<br>\n'
        '七五三掛龍也と吉澤閑也もそれぞれ2番組あり、中村海人は長野ローカルの「夢テレビ2026」に吉澤閑也と一緒に出演します。<br>\n'
        '川島如恵留は、今週はけるとめるでの出演が中心の週になりました。')

# --- まとめ ---
c = rep(c, '宮近・松倉は10/9(金)それスノSPと10/10(土)シューイチ<br>\n',
        '宮近・松倉は10/9(金)それスノSP、宮近は10/10(土)HELP ME!!にも出演<br>\n')
chk = re.search(r'<span style="display:inline-block;[^>]*>&#10003;</span>', c).group(0)
c = rep(c, '吉澤は10/4(日)リモートシェフ、松田は10/10(土)ドッキリGP SPにも出演</p>',
        '吉澤は10/4(日)リモートシェフ、松田は10/10(土)ドッキリGP SPにも出演<br>\n'
        + chk + 'ローカル局では七五三掛が10/7(水)関西テレビ「とれたてっ！」、中村・吉澤が10/10(土)SBC「夢テレビ2026」</p>')
assert 'シューイチ(10/10)' not in c
open(f, "w", encoding="utf-8").write(c)
print("ok")
