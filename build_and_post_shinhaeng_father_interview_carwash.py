# -*- coding: utf-8 -*-
"""SHINHAENG(オ・シンヘン) デビュー前の下積み(洗車場の夜勤・選挙後4年)記事: JP + KR + EN 下書き投稿(本文画像なし・アイキャッチのみ)。
ソース: 全南日報(전남일보) 2026-06-15 単独記事、父オ・ウォンオク(오원옥)氏の電話取材
  https://www.jnilbo.com/news/articleView.html?idxno=90000042697
  「[단독]선거 벽보서 아이돌 무대로…오신행, 日 데뷔 뒷얘기」(정성현 기자)
報道機関の直接取材コメントなので出典を名指し+鉤括弧で引用(feedback_media_outlet_quote_attribution_ok)。
記事内の写真(家族提供・選管キャプチャ)は転載しない。

python build_and_post_shinhaeng_father_interview_carwash.py [--dry]
"""
import base64
import json
import re
import subprocess
import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
    return env


ENV = load_env(ROOT / ".env")
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
HA = {"Authorization": f"Basic {AUTH}"}

BASE_SLUG = "shinhaeng-car-wash-night-shift-father-interview"

# SHINHAENG=ブラウン(13548と同じ配色)
A = "#8b6a4f"
SOFT = "#e6d8cc"
BG = "#faf5f0"

SRC_URL = "https://www.jnilbo.com/news/articleView.html?idxno=90000042697"

# 内部リンク(WP APIで確認済み・すべて公開済み)
L_FAMILY_JP = "https://chomoand-1.com/osinhean_family-1669"
L_WIKI_JP = "https://chomoand-1.com/ohsinhyeon_wiki-1624"
L_GAKU_JP = "https://chomoand-1.com/ohsinhyeon_gakureki-1651"
L_WIKI_KR = "https://chomoand-1.com/ko/ohsinhyeon_wiki-kr-10659"
L_GAKU_KR = "https://chomoand-1.com/ko/ohsinhyeon_gakureki-kr-10662"
L_BAITO_JP = "https://chomoand-1.com/what-is-issas-part-time-job-history-thre-13030"
L_TALK_JP = "https://chomoand-1.com/shinhaeng-confession-in-korean-ko1keyz-13548"
L_PERFUME_JP = "https://chomoand-1.com/shinhaeng-le-labo-perfume-12463"
L_PERFUME_KR = "https://chomoand-1.com/ko/shinhaeng-le-labo-perfume-kr-12557"
L_PERFUME_EN = "https://chomoand-1.com/en/shinhaeng-le-labo-perfume-en-12562"
L_ZENSE_JP = "https://chomoand-1.com/ko1keyz-12-members-zense-works-13318"
L_ZENSE_KR = "https://chomoand-1.com/ko/ko1keyz-12-members-zense-works-kr-13321"
L_ZENSE_EN = "https://chomoand-1.com/en/ko1keyz-12-members-zense-works-en-13324"


# ---------- HTML部品 ----------
def para(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def html_block(inner):
    return f"<!-- wp:html -->\n{inner}\n<!-- /wp:html -->"


def a(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'


def mk(t):
    return f'<strong><span class="swl-marker mark_orange">{t}</span></strong>'


def mini(rows):
    ps = []
    for i, (k, v) in enumerate(rows):
        m = "0" if i == 0 else "4px 0 0 0"
        ps.append(f'<p style="margin:{m};"><strong>{k}</strong>{v}</p>')
    return html_block(
        f'<div style="border:1px solid {SOFT};border-left:4px solid {A};border-radius:4px;padding:10px 16px;'
        f'margin:0 0 16px 0;background:{BG};">\n' + "\n".join(ps) + "\n</div>"
    )


def info_box(title, rows):
    """導入直後の線囲みのみの基本情報box"""
    trs = "\n".join(
        f'<tr><td style="background:{BG};border:1px solid {SOFT};padding:8px 12px;width:30%;">{k}</td>'
        f'<td style="border:1px solid {SOFT};padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return html_block(
        f'<div style="border:1px solid {SOFT};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>\n'
        f'<table style="border-collapse:collapse;width:100%;">\n{trs}\n</table>\n</div>'
    )


def spec_box(title, rows):
    trs = "\n".join(
        f'<tr><td style="background:{BG};border:1px solid {SOFT};padding:8px 12px;width:32%;">{k}</td>'
        f'<td style="border:1px solid {SOFT};padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return html_block(
        f'<div style="border:1px solid {SOFT};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;color:{A};">{title}</p>\n'
        f'<table style="border-collapse:collapse;width:100%;">\n{trs}\n</table>\n</div>'
    )


def toc_box(title, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return html_block(
        f'<div style="border:1px solid {SOFT};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">{title}</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">\n{lis}\n</ul>\n</div>'
    )


def quote_box(label, quotes):
    body = "<br>".join(quotes)
    return html_block(
        f'<div style="border:1px solid {SOFT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">\n'
        f'<p style="margin:0 0 6px 0;font-weight:bold;font-size:0.9em;color:{A};">{label}</p>\n'
        f'<p style="margin:0;font-size:0.95em;">{body}</p>\n</div>'
    )


CHECK = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {A};border-radius:3px;'
         f'color:{A};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')


def summary_box(title, items):
    body = "<br>\n".join(f"{CHECK}{i}" for i in items)
    return html_block(
        f'<div style="border:2px solid {A};border-radius:8px;background:{BG};padding:1em 1.25em;margin:0 0 16px 0;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;color:{A};">{title}</p>\n'
        f'<p style="margin:0;">\n{body}\n</p>\n</div>'
    )


def related_box(title, links):
    lis = "\n".join(f"<li>{a(u, t)}</li>" for u, t in links)
    return html_block(
        f'<div style="border:1px solid {SOFT};border-left:4px solid {A};border-radius:4px;padding:14px 18px;'
        f'margin:0 0 16px 0;background:{BG};">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>'
    )


def gmap(q):
    return html_block(
        f'<iframe src="https://maps.google.com/maps?q={q}&t=&z=13&ie=UTF8&iwloc=&output=embed" '
        f'width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>'
    )


MAP_UNIV = gmap("Mokpo+National+University")
MAP_MOKPO = gmap("Mokpo,+Jeollanam-do")


# ============================== JAPANESE ==============================
JP_TITLE = "【SHINHAENG】洗車場で夜勤バイト？父が明かした下積み4年！"

JP_CONTENT = "\n\n".join([
    para(
        "KO1KEYZ(コイキーズ)のSHINHAENGといえば、18歳で韓国の地方選挙に出馬した異色の経歴で知られています。",
        f"そんなSHINHAENGが、デビュー前のソウルで{mk('夜10時から翌朝8時まで洗車場で働きながら、歌とダンスのレッスンを続けていた')}ことが、父・オ・ウォンオクさんへの取材で明らかになりました。",
        "この記事では、選挙のあとに大学を休学してからデビューまでの4年間、家族が出した「あと2年」という期限、選挙出馬の裏話、そしてデビュー後の「お給料の10%」の約束まで、父が語ったエピソードをまとめて紹介します。",
    ),
    info_box("今回のエピソードの出どころ", [
        ("媒体", "全南日報(チョンナムイルボ)。韓国・光州/全羅南道の地方紙"),
        ("掲載日", "2026年6月15日(単独記事)"),
        ("語り手", "父・オ・ウォンオクさん(電話インタビュー)"),
        ("時期", "日プ新世界のファイナルで4位に入り、KO1KEYZデビューが決まった直後"),
    ]),
    toc_box("この記事でわかること", [
        "選挙後の休学と4年間の準備",
        "洗車場での夜勤バイト",
        "家族が出した「期限」",
        "番組の「木浦」表記に父が喜んだ理由",
        "選挙出馬の裏話",
        "「お給料の10%」の約束",
    ]),

    h2("父が語ったSHINHAENGの「日本デビューの裏話」とは？"),
    mini([
        ("記事の見出し: ", "「選挙ポスターからアイドルのステージへ…オ・シンヘン、日本デビューの裏話」"),
        ("中身: ", "父・オ・ウォンオクさんが語った、2022年の選挙からデビューまでの4年間"),
    ]),
    para(
        "今回のエピソードの出どころは、SHINHAENGの地元・全羅南道の地方紙「全南日報」が2026年6月15日に出した単独記事です。",
        "同紙は6月12日にも「木浦大学出身の『全南最年少候補』オ・シンヘン、日本のアイドルデビュー」と報じており、その続報として父・オ・ウォンオクさんに電話取材をしています。",
        "このあと鉤括弧で紹介するコメントは、すべて全南日報が報じた父の発言を日本語に訳したものです。",
    ),
    para(
        "オ・ウォンオクさんは、2022年の選挙でSHINHAENGと同じ選挙区から出馬したお父さんです。",
        f"木浦で長く地域政治に挑戦してきた人物で、家族構成や父の経歴は{a(L_FAMILY_JP, 'オ・シンヘンの家族構成をまとめた記事')}で詳しく紹介しています。",
        "今回は、デビュー決定を受けて父の目線から「この4年間に何があったのか」が語られた、貴重なインタビューでした。",
    ),

    h2("選挙のあとは大学を休学、木浦とソウルで計4年の準備"),
    mini([
        ("休学: ", "国立木浦大学 ファッション衣類学科"),
        ("準備期間: ", "木浦で約2年+ソウルで約2年"),
    ]),
    para(
        "父によると、SHINHAENGは2022年の選挙が終わったあと、在籍していた木浦大学のファッション衣類学科を休学しています。",
        "父のコメントは次の通りです。",
    ),
    quote_box("全南日報が報じた父のコメント(日本語訳)", [
        "「選挙が終わった後、シンヘンが木浦大学のファッション衣類学科を休学した」",
        "「木浦にいた時もオルタナティブスクールに通いながら2年ほど歌とダンスを習い、その後ソウルに上京してさらに2年準備した」",
    ]),
    para(
        "つまり、歌とダンスの準備は木浦時代から少しずつ始まっていて、そこからソウルでの2年を合わせた約4年をかけて、日プ新世界の舞台にたどり着いたことになります。",
        f"飛び級で大学に進んだ経緯や在学中の活動は、{a(L_GAKU_JP, 'オ・シンヘンの学歴をまとめた記事')}でも紹介しています。",
    ),
    para(
        "家族にとっても、この進路はまったくの予想外だったようです。",
        "父は「家には歌やダンスが上手な人はいなかった」と振り返り、「経営学科か経済学科に行くと思っていたのに、ファッション衣類学科に進み、そこでまた別の道を見つけていった」とも話しています。",
        "政治、ファッション、そしてアイドルと、興味のままに道を切り開いてきたSHINHAENGらしさがよく伝わるエピソードです。",
    ),
    MAP_UNIV,

    h2("ソウルでは夜10時〜翌朝8時まで洗車場で夜勤"),
    mini([
        ("バイト先: ", "洗車場(夜勤)"),
        ("時間帯: ", "夜10時〜翌朝8時"),
    ]),
    para(
        "今回いちばん驚かされたのが、ソウル時代の生活です。",
        f"SHINHAENGはボーカルとダンスを習いながら、{mk('夜間のアルバイトを掛け持ちしていた')}といいます。",
    ),
    quote_box("全南日報が報じた父のコメント(日本語訳)", [
        "「夜10時から翌朝8時まで洗車場で働きながら準備した」",
        "「親も一部は手伝ったが、本人も働きながら耐え抜いた」",
    ]),
    para(
        "夜10時から翌朝8時までというと、休憩を挟んでも10時間近い夜勤です。",
        "昼間はレッスン、夜は洗車場という生活を続けていたとすれば、睡眠時間を削りながらの毎日だったのでしょう。",
        "親に頼りきりにせず、自分で働いて夢を支えていたところに、SHINHAENGの芯の強さが見えます。",
    ),
    para(
        f"KO1KEYZメンバーのアルバイト経験は{a(L_BAITO_JP, 'KO1KEYZメンバーのバイト歴をまとめた記事')}でも紹介していますが、夜勤の洗車場というのはメンバーの中でもかなりハードな部類かもしれません。",
    ),

    h2("「あと2年だけ」家族が出した期限と、日プとの出会い"),
    mini([
        ("家族の条件: ", "「2年くらいだけもう少しやってみよう」"),
        ("日プを知ったきっかけ: ", "ソウルで通っていたスクールなど"),
    ]),
    para(
        "デビューが約束された道ではなかっただけに、家族の心配も大きかったようです。",
        "父は当時の気持ちを次のように話しています。",
    ),
    quote_box("全南日報が報じた父のコメント(日本語訳)", [
        "「いつ受かるのか、受からないのか、心配ばかりしていた」",
        "「復学するにしても軍隊に行くにしても決めなければならないので、あと2年ほどやってみようと時間を与えたが、最後に良いチャンスが来たようだ」",
    ]),
    para(
        "韓国の男性には兵役があるため、20代前半は「復学するか、入隊するか」を決めなければならない時期でもあります。",
        "家族が区切りとして与えた2年の最後に日プ新世界のチャンスが巡ってきたと考えると、まさにギリギリのタイミングでつかんだデビューでした。",
    ),
    para(
        "日プ新世界への挑戦は、ソウルで通っていたスクールなどを通じて情報を得たのがきっかけだったそうです。",
        "父は「『PRODUCE 101 JAPAN』は4回目から国際化の流れに乗ったようだ」「外国人の参加者も一緒に挑戦できる仕組みが、シンヘンにとってチャンスになった」と分析しています。",
        "実際にKO1KEYZにも、SHINHAENGとSIYOUNGという韓国出身のメンバーが2人います。",
        f"{a(L_ZENSE_JP, 'KO1KEYZメンバー12人の前世(デビュー前の活動)をまとめた記事')}を見ると、メンバーそれぞれが違う道からこのオーディションに集まってきたことがよく分かります。",
    ),

    h2("番組の「木浦」表記に父がいちばん喜んだ理由"),
    mini([
        ("番組での表記: ", "オ・シンヘン(木浦)"),
        ("住所地と生活圏: ", "住所は務安郡、生まれ育ったのは木浦"),
    ]),
    para(
        "父がいちばんうれしかったと話したのは、意外にも順位ではなく、番組でSHINHAENGの出身地が「木浦」と表示されたことでした。",
    ),
    quote_box("全南日報が報じた父のコメント(日本語訳)", [
        "「住所地は務安だが、生まれ育った場所と生活圏は木浦だった」",
        "「1番目も2番目も3番目も、みんな木浦大学に進んだ。子どもたちが地域とのつながりを持って生きてほしいという願いがいつもあった」",
    ]),
    para(
        f"SHINHAENGは3人きょうだいの真ん中で、{a(L_FAMILY_JP, '家族構成の記事')}で紹介しているお姉さん・妹さんとともに、3人全員が地元の木浦大学に進んだことになります。",
        "木浦を背負ってデビューする息子の姿は、地域への思いを大切にしてきた父にとって特別なものだったはずです。",
    ),
    MAP_MOKPO,

    h2("選挙出馬は父のすすめだった！最初は毎日反発していた"),
    mini([
        ("出馬: ", "2022年 第8回全国同時地方選挙・務安郡議会議員(ナ選挙区)、無所属"),
        ("結果: ", "得票率5.88%、6位で落選"),
    ]),
    para(
        "2022年の地方選挙への出馬も、実は父のすすめでした。",
        "当時は公職選挙法の改正で、被選挙権の年齢が満25歳から満18歳に引き下げられた直後だったのです。",
    ),
    quote_box("全南日報が報じた父のコメント(日本語訳)", [
        "「25歳から18歳に下がったのは大きな変化だった。歴史の中にお前も一緒にいなさいという意味で出馬を勧めた」",
        "「本人はまったく選挙のことを考えていなかった。最初は、なぜ出なければならないのかと毎日問い詰めてきたが、諦めずに最後までやってくれと頼んだ」",
    ]),
    para(
        "最初は乗り気ではなかったSHINHAENGですが、選挙戦は大きな学びの時間になったそうです。",
        "父によると、オルタナティブスクールに通っていたSHINHAENGは、韓国の10代が抱える悩みを直接経験してきたわけではなかったものの、インタビューを受けたり勉強したりするうちに「青少年のためにできることがある」と考えるようになったといいます。",
    ),
    para(
        f"掲げたスローガンは「青少年による、青少年のための、青少年候補」で、{mk('青少年のフェアトラベル、青少年への株式投資金の支給、青少年総会、ゴミの分別圧縮機の設置')}などを公約にしていました。",
        "結果は得票率5.88%の6位で落選でしたが、父は「当選するかどうかが第一の目標ではなかった」「何をするにしても、自分ひとりの人生ではなく、共同体とともに歩む人生を送ってほしかった」と話しています。",
        "当時は日本のNHKもSHINHAENGを3日間にわたって取材していたそうで、日本との縁はこの頃から始まっていたのかもしれません。",
        f"選挙から日プ出演までの経歴は{a(L_WIKI_JP, 'オ・シンヘンのwiki風経歴の記事')}にもまとめています。",
    ),

    h2("デビュー後は「お給料の10%ずつを両親に」と宣言"),
    mini([
        ("本人が話していたこと: ", "お給料をもらったら、お母さんとお父さんにそれぞれ10%ずつ渡す"),
        ("時期: ", "デビュー直前(2026年6月)の時点での話"),
    ]),
    para(
        "インタビューの最後には、ファンにとってたまらないエピソードも語られています。",
    ),
    quote_box("全南日報が報じた父のコメント(日本語訳)", [
        "「日本は韓国と違って、デビュー初期から月給が出る仕組みだと聞いた」",
        "「シンヘンが、忙しくてお金を使う時間もないと言いながら、月給をもらったらお母さんとお父さんにそれぞれ10%ずつあげると言っていた」",
    ]),
    para(
        "夜勤で自分の夢を支えてきた息子が、今度は両親に恩返しをしようとしているのです。",
        "父が笑顔でこの話をしたと記事は伝えていて、読んでいるこちらまで温かい気持ちになります。",
        "なお、これはデビュー前の時点で本人が話していた予定で、実際にいつからどう渡しているかまでは明かされていません。",
    ),
    para(
        "父は、日本語を習ったことがないSHINHAENGがコメントを求められる場面で苦労しないか心配していたとも話しています。",
        "「幸い通訳がそばにいて、本人もうまくやれたようだ」と安心した様子で、今のトーク会で日本語や韓国語を織り交ぜてファンと話す姿を思うと、ここ数か月の成長ぶりにも驚かされます。",
        f"トーク会での神対応ぶりは{a(L_TALK_JP, 'SHINHAENGのトーク会エピソードの記事')}で紹介しています。",
    ),
    para(
        "父は最後に「これからはひとりではなくチームで活動するのだから、周りへの気配りが必要だ」「実力を伸ばして認められ、いつかは木浦と地域にも役立つ人になってほしい」と、息子へのメッセージで締めくくっていました。",
    ),

    h2("SHINHAENG(オ・シンヘン)のプロフィール"),
    spec_box("SHINHAENGの基本プロフィール", [
        ("本名", "オ・シンヘン(오신행)"),
        ("生年月日", "2004年5月3日"),
        ("出身", "韓国・全羅南道木浦市(住所地は務安郡)"),
        ("身長", "177cm"),
        ("メンバーカラー", "ブラウン"),
        ("日プ新世界の順位", "最終4位でKO1KEYZとしてデビュー"),
    ]),
    para(
        "SHINHAENGは、2022年に18歳で地方選挙に出馬し「全国最年少候補」として注目されたあと、日プ新世界で最終4位に入りKO1KEYZのメンバーになりました。",
        f"香水はル ラボの「THÉ MATCHA 26」を愛用していると本人が明かしていて、詳しくは{a(L_PERFUME_JP, 'SHINHAENGの香水の記事')}で紹介しています。",
    ),

    h2("まとめ"),
    summary_box("SHINHAENGの下積み時代まとめ", [
        "2022年の選挙後、木浦大学ファッション衣類学科を休学",
        "木浦で約2年、ソウルで約2年、計4年かけて歌とダンスを準備",
        "ソウルでは夜10時〜翌朝8時まで洗車場で夜勤バイト",
        "家族は「あと2年だけ」と期限を出していた",
        "選挙出馬は父のすすめで、最初は本人が毎日反発していた",
        "デビュー後は「お給料の10%ずつを両親に」と話していた",
        "いずれも父・オ・ウォンオクさんが全南日報(2026年6月15日)の取材で語った内容",
    ]),
    para(
        "キラキラしたステージの裏に、夜勤と練習を重ねた4年間があったと知ると、SHINHAENGのパフォーマンスがまた違って見えてきますね！",
    ),
    related_box("SHINHAENG(オ・シンヘン)の関連記事", [
        (L_FAMILY_JP, "オ・シンヘンの家族構成は？父親は政治家を目指す学校長！"),
        (L_WIKI_JP, "オ・シンヘンのwiki風経歴は？18歳で議員選挙出馬から芸能の道へ"),
        (L_GAKU_JP, "オ・シンヘンの学歴は？飛級で大学進学！"),
        (L_BAITO_JP, "KO1KEYZメンバーのバイト歴は？"),
        (L_TALK_JP, "【SHINHAENG】韓国語の告白！トーク会で見せた甘い神対応！"),
        (L_PERFUME_JP, "KO1KEYZシンヘンの香水はル ラボ『THÉ MATCHA 26』"),
    ]),
])
JP_SUMMARY = (
    "KO1KEYZのSHINHAENGはデビュー前、ソウルで夜10時〜翌朝8時まで洗車場で働きながら歌とダンスを準備していた。"
    "父が全南日報に語った選挙後の4年間と「お給料の10%」の約束をまとめました。"
)


# ============================== KOREAN ==============================
KR_TITLE = "SHINHAENG, 세차장 야간 알바? 아버지가 밝힌 데뷔 전 4년!"

KR_CONTENT = "\n\n".join([
    para(
        "KO1KEYZ(코이키즈)의 SHINHAENG은 18세에 한국 지방선거에 출마한 독특한 이력으로 잘 알려져 있어요.",
        f"그런 SHINHAENG이 데뷔 전 서울에서 {mk('밤 10시부터 다음 날 아침 8시까지 세차장에서 일하며 노래와 춤 레슨을 병행했다')}는 사실이 아버지 오원옥 씨의 인터뷰로 전해졌습니다.",
        "이 글에서는 선거 후 대학을 휴학하고 데뷔하기까지의 4년, 가족이 정한 '2년'이라는 기한, 선거 출마 뒷이야기, 그리고 데뷔 후 '월급의 10%' 약속까지 아버지가 들려준 에피소드를 정리해 봤어요.",
    ),
    info_box("이번 에피소드의 출처", [
        ("매체", "전남일보(광주·전남 지역 일간지)"),
        ("보도일", "2026년 6월 15일(단독 기사)"),
        ("인터뷰", "아버지 오원옥 씨(유선 인터뷰)"),
        ("시기", "일본 프로듀스 신세계 파이널 4위로 KO1KEYZ 데뷔가 확정된 직후"),
    ]),
    toc_box("이 글에서 알 수 있는 것", [
        "선거 후 휴학과 4년간의 준비",
        "세차장 야간 아르바이트",
        "가족이 정한 '기한'",
        "방송의 '목포' 표기에 아버지가 기뻐한 이유",
        "선거 출마 뒷이야기",
        "'월급의 10%' 약속",
    ]),

    h2("아버지가 전한 SHINHAENG의 '일본 데뷔 뒷얘기'란?"),
    mini([
        ("기사 제목: ", "「[단독]선거 벽보서 아이돌 무대로…오신행, 日 데뷔 뒷얘기」"),
        ("내용: ", "아버지 오원옥 씨가 전한 2022년 선거부터 데뷔까지의 4년"),
    ]),
    para(
        "이번 에피소드의 출처는 SHINHAENG의 고향 전남 지역 일간지 전남일보가 2026년 6월 15일에 낸 단독 기사예요.",
        "전남일보는 6월 12일에도 「목포대 출신 '전남 최연소 후보' 오신행, 일본 아이돌 데뷔」를 보도했고, 그 후속으로 아버지 오원옥 씨를 유선으로 인터뷰했습니다.",
        "아래 따옴표 속 발언은 모두 전남일보가 보도한 아버지의 말을 그대로 옮긴 것입니다.",
    ),
    para(
        "오원옥 씨는 2022년 선거에서 SHINHAENG과 같은 선거구에 출마했던 아버지예요.",
        f"선거 출마부터 일프 참가까지의 이력은 {a(L_WIKI_KR, '오신행의 위키풍 경력 글')}에서도 자세히 소개하고 있어요.",
    ),

    h2("선거 후 대학 휴학, 목포와 서울에서 총 4년 준비"),
    mini([
        ("휴학: ", "국립목포대학교 패션의류학과"),
        ("준비 기간: ", "목포에서 약 2년 + 서울에서 약 2년"),
    ]),
    para("아버지에 따르면 SHINHAENG은 2022년 선거가 끝난 뒤 목포대 패션의류학과를 휴학했어요."),
    quote_box("전남일보가 보도한 아버지의 말", [
        "“선거가 끝난 뒤 신행이가 목포대 패션의류학과를 휴학했다”",
        "“목포에 있을 때도 대안학교를 다니면서 2년 정도 춤과 노래를 배웠고, 이후 서울에 올라가 다시 2년을 준비했다”",
    ]),
    para(
        "노래와 춤 준비는 목포 시절부터 조금씩 시작됐고, 서울에서의 2년까지 합쳐 약 4년 만에 일프 신세계 무대에 선 셈이에요.",
        f"월반으로 대학에 진학한 과정은 {a(L_GAKU_KR, '오신행의 학력 글')}에서 볼 수 있어요.",
    ),
    para(
        "가족에게도 전혀 예상하지 못한 진로였다고 해요.",
        "아버지는 “집안에 노래나 춤을 잘하는 사람이 없었다”, “경영학과나 경제학과에 갈 줄 알았는데 패션의류학과로 진학했고, 거기서 또 다른 길을 찾아갔다”고 돌아봤습니다.",
        "정치, 패션, 그리고 아이돌까지, 관심 가는 길을 스스로 개척해 온 SHINHAENG다운 이야기예요.",
    ),
    MAP_UNIV,

    h2("서울에서는 밤 10시~아침 8시 세차장 야간 근무"),
    mini([
        ("아르바이트: ", "세차장(야간)"),
        ("시간: ", "밤 10시~다음 날 아침 8시"),
    ]),
    para("가장 놀라운 건 서울 생활이었어요.",
        f"SHINHAENG은 보컬과 댄스를 배우면서 {mk('야간 아르바이트를 병행했다')}고 합니다."),
    quote_box("전남일보가 보도한 아버지의 말", [
        "“밤 10시부터 다음 날 아침 8시까지 세차장에서 일하며 준비했다”",
        "“부모가 일부 도왔지만, 본인도 일을 하면서 버텼다”",
    ]),
    para(
        "밤 10시부터 아침 8시까지면 쉬는 시간을 빼도 10시간 가까운 야간 근무예요.",
        "낮에는 레슨, 밤에는 세차장이었다면 잠을 줄여 가며 버틴 나날이었을 거예요.",
        "부모님께만 기대지 않고 스스로 일하며 꿈을 지켜 온 모습에서 SHINHAENG의 단단함이 느껴집니다.",
    ),

    h2("'2년만 더' 가족이 정한 기한과 일프와의 만남"),
    mini([
        ("가족의 조건: ", "“2년 정도만 더 해보자”"),
        ("일프를 알게 된 계기: ", "서울에서 다니던 학원 등"),
    ]),
    para("데뷔가 보장된 길이 아니었기에 가족의 걱정도 컸다고 해요."),
    quote_box("전남일보가 보도한 아버지의 말", [
        "“언제 될지, 안 될지 걱정만 됐다”",
        "“복학을 하든 군대를 가든 결정해야 하니 2년 정도만 더 해보자고 시간을 줬는데, 마지막에 좋은 기회가 온 것 같다”",
    ]),
    para(
        "가족이 정해 준 2년의 끝자락에 일프 신세계라는 기회가 찾아왔다고 생각하면, 정말 아슬아슬한 타이밍에 잡은 데뷔였어요.",
        "도전의 계기는 서울에서 다니던 학원 등을 통해 정보를 접한 것이었다고 합니다.",
        "아버지는 “'프로듀스101재팬'이 4회째부터 국제화 흐름을 탄 것 같다”, “외국인 참가자들도 함께 도전하는 구조가 신행이에게 기회가 된 것 같다”고 설명했어요.",
        f"다른 멤버들이 데뷔 전 어떤 활동을 했는지는 {a(L_ZENSE_KR, 'KO1KEYZ 12명의 전생 정리 글')}에서 볼 수 있어요.",
    ),

    h2("방송의 '목포' 표기에 아버지가 가장 기뻐한 이유"),
    mini([
        ("방송 표기: ", "오신행(목포)"),
        ("주소지와 생활권: ", "주소는 무안, 나고 자란 곳은 목포"),
    ]),
    para("아버지가 가장 반가웠다고 한 건 순위가 아니라, 방송에서 SHINHAENG의 지역명이 '목포'로 표기된 점이었어요."),
    quote_box("전남일보가 보도한 아버지의 말", [
        "“주소지는 무안이지만 태어나 자란 곳과 생활권은 목포였다”",
        "“첫째, 둘째, 셋째가 모두 목포대로 갔다. 자녀들이 지역과 연결점을 두고 살았으면 하는 바람이 늘 있었다”",
    ]),
    para(
        "SHINHAENG은 누나와 여동생 사이의 둘째로, 삼 남매 모두 고향의 목포대에 진학한 셈이에요.",
        "목포를 대표해 데뷔하는 아들의 모습은 지역을 아껴 온 아버지에게 남다른 의미였을 거예요.",
    ),
    MAP_MOKPO,

    h2("선거 출마는 아버지의 권유! 처음엔 매일 따졌다"),
    mini([
        ("출마: ", "2022년 제8회 전국동시지방선거 무안군의원 나선거구, 무소속"),
        ("결과: ", "득표율 5.88%, 6위로 낙선"),
    ]),
    para(
        "2022년 지방선거 출마도 사실 아버지의 권유였어요.",
        "당시는 공직선거법 개정으로 피선거권 연령이 만 25세에서 만 18세로 낮아진 직후였습니다.",
    ),
    quote_box("전남일보가 보도한 아버지의 말", [
        "“25세에서 18세로 내려간 것은 큰 변화였다. 역사 안에 너도 함께 있으라는 뜻에서 출마를 권유했다”",
        "“본인은 전혀 선거를 생각하지 않았다. 처음에는 왜 나가야 하느냐고 매일 따졌고, 포기하지 말고 끝까지 가달라고 부탁했다”",
    ]),
    para(
        "처음엔 내키지 않았던 SHINHAENG이지만, 선거 과정은 큰 배움의 시간이 됐다고 해요.",
        "인터뷰를 하고 공부하면서 청소년을 위해 할 일이 있겠다는 생각을 하게 됐다고 아버지는 전했어요.",
        f"슬로건은 '청소년에 의한, 청소년을 위한, 청소년 후보'였고, {mk('청소년 공정여행, 청소년 주식 투자금 지급, 청소년 총회, 쓰레기 분리 압축기계 설치')} 등을 공약으로 내걸었습니다.",
        "결과는 5.88%로 6위 낙선이었지만, 아버지는 “당선되고 안 되고가 첫 번째 목표는 아니었다”고 말했어요.",
        "당시 일본 NHK가 SHINHAENG을 3일간 취재하기도 했다니, 일본과의 인연은 이때부터 시작된 걸지도 모르겠어요.",
    ),

    h2("데뷔 후엔 '월급의 10%씩 부모님께' 선언"),
    mini([
        ("본인의 말: ", "월급을 받으면 엄마와 아빠에게 각각 10%씩 주겠다"),
        ("시점: ", "데뷔 직전(2026년 6월) 기준의 계획"),
    ]),
    para("인터뷰 마지막에는 팬들이 들으면 흐뭇해질 이야기도 나왔어요."),
    quote_box("전남일보가 보도한 아버지의 말", [
        "“일본은 한국과 달리 데뷔 초기부터 월급을 주는 구조라고 들었다”",
        "“신행이가 바빠서 돈 쓸 시간도 없다고 하면서, 월급을 받으면 엄마와 아빠에게 각각 10%씩 주겠다고 하더라”",
    ]),
    para(
        "야간 근무로 꿈을 지켜 온 아들이 이제는 부모님께 보답하려 한다니, 읽는 사람까지 마음이 따뜻해져요.",
        "다만 이건 데뷔 전 시점에 본인이 말한 계획이고, 실제로 언제부터 어떻게 드리고 있는지는 알려지지 않았어요.",
        "아버지는 일본어를 배운 적이 없는 SHINHAENG이 소감을 말할 때 힘들지 않을까 걱정했지만, “다행히 통역이 곁에 있었고, 본인도 잘해낸 것 같다”며 안도했다고 해요.",
        "마지막으로 “이제는 혼자가 아니라 팀으로 활동하게 된 만큼 주변을 배려해야 한다”, “언젠가는 목포와 지역에도 도움이 되는 사람이 됐으면 좋겠다”는 메시지를 남겼습니다.",
    ),

    h2("SHINHAENG(오신행) 프로필"),
    spec_box("SHINHAENG 기본 프로필", [
        ("본명", "오신행"),
        ("생년월일", "2004년 5월 3일"),
        ("출신", "전남 목포(주소지는 무안군)"),
        ("키", "177cm"),
        ("멤버 컬러", "브라운"),
        ("일프 신세계 순위", "최종 4위로 KO1KEYZ 데뷔"),
    ]),
    para(
        "SHINHAENG은 2022년 18세의 나이로 지방선거에 출마해 '전국 최연소 후보'로 주목받은 뒤, 일본 프로듀스 신세계에서 최종 4위를 기록하며 KO1KEYZ 멤버가 됐어요.",
        f"본인이 밝힌 향수 이야기는 {a(L_PERFUME_KR, 'SHINHAENG의 향수 글')}에서 볼 수 있어요.",
    ),

    h2("정리"),
    summary_box("SHINHAENG의 데뷔 전 이야기 정리", [
        "2022년 선거 후 목포대 패션의류학과 휴학",
        "목포에서 약 2년, 서울에서 약 2년, 총 4년간 노래와 춤 준비",
        "서울에서는 밤 10시~아침 8시 세차장 야간 아르바이트",
        "가족은 '2년만 더'라는 기한을 줬다",
        "선거 출마는 아버지의 권유, 처음엔 본인이 매일 따졌다",
        "데뷔 후 '월급의 10%씩 부모님께' 드리겠다고 말했다",
        "모두 아버지 오원옥 씨가 전남일보(2026년 6월 15일)에 전한 내용",
    ]),
    para("화려한 무대 뒤에 야간 근무와 연습을 이어 온 4년이 있었다는 걸 알고 나면, SHINHAENG의 무대가 또 다르게 보일 거예요!"),
    related_box("SHINHAENG(오신행) 관련 글", [
        (L_WIKI_KR, "오신행의 위키풍 경력은? 18세에 의원 선거 출마부터 연예계 도전까지"),
        (L_GAKU_KR, "오신행의 학력은? 월반으로 대학 진학!"),
        (L_PERFUME_KR, "신행의 향수는 르 라보의 「말차」? 본인이 밝혔다"),
        (L_ZENSE_KR, "KO1KEYZ 12명의 전생은? 지금 다시 볼 수 있는 작품 총정리!"),
        (L_FAMILY_JP, "오신행의 가족 구성(일본어)"),
    ]),
])
KR_SUMMARY = (
    "KO1KEYZ SHINHAENG은 데뷔 전 서울에서 밤 10시~아침 8시 세차장 야간 알바를 하며 노래와 춤을 준비했다. "
    "아버지가 전남일보에 전한 선거 후 4년과 '월급 10%' 약속을 정리했어요."
)


# ============================== ENGLISH ==============================
EN_TITLE = "SHINHAENG's Car Wash Night Shifts: His Dad on the Road to Debut"

EN_CONTENT = "\n\n".join([
    para(
        "KO1KEYZ's SHINHAENG is known for an unusual past: he ran in a South Korean local election at just 18.",
        f"Now an interview with his father, Oh Won-ok, has revealed that before debuting, SHINHAENG {mk('worked night shifts at a car wash in Seoul, from 10 p.m. to 8 a.m., while taking singing and dance lessons')}.",
        "In this article, we go through what his father shared: the leave of absence from university after the election, the four years of preparation, the two-year deadline his family set, the story behind his election run, and his promise to give his parents 10% of his salary.",
    ),
    info_box("Where these stories come from", [
        ("Outlet", "Jeonnam Ilbo, a regional daily in Gwangju / South Jeolla Province, Korea"),
        ("Date", "June 15, 2026 (exclusive)"),
        ("Interviewee", "His father, Oh Won-ok (phone interview)"),
        ("Timing", "Right after SHINHAENG finished 4th in the PRODUCE 101 JAPAN: THE NEW WORLD final and joined KO1KEYZ"),
    ]),
    toc_box("What you'll learn", [
        "His leave from university and four years of preparation",
        "His overnight job at a car wash",
        "The deadline his family set",
        "Why his dad loved the \"Mokpo\" caption on the show",
        "The story behind his election run",
        "His \"10% of my salary\" promise",
    ]),

    h2("What did SHINHAENG's father reveal?"),
    mini([
        ("Headline: ", "\"From Election Posters to the Idol Stage: Oh Shin-haeng's Japan Debut Backstory\""),
        ("Content: ", "His father's account of the four years between the 2022 election and his debut"),
    ]),
    para(
        "These stories come from an exclusive published on June 15, 2026, by Jeonnam Ilbo, a regional newspaper in SHINHAENG's home province of South Jeolla.",
        "The paper had already reported his debut on June 12, and followed up with a phone interview with his father, Oh Won-ok.",
        "All quotes below are our English translations of his father's words as reported by Jeonnam Ilbo.",
    ),
    para(
        "Oh Won-ok is the father who ran in the same district as SHINHAENG in the 2022 election.",
        f"For more on SHINHAENG's family, see {a(L_FAMILY_JP, 'our article on his family (in Japanese)')}.",
    ),

    h2("A leave from university, then four years of training in Mokpo and Seoul"),
    mini([
        ("On leave from: ", "Mokpo National University, Department of Fashion and Clothing"),
        ("Training: ", "About 2 years in Mokpo + about 2 years in Seoul"),
    ]),
    para("According to his father, SHINHAENG took a leave of absence from university after the 2022 election."),
    quote_box("His father, as reported by Jeonnam Ilbo", [
        "\"After the election ended, Shin-haeng took a leave of absence from the Department of Fashion and Clothing at Mokpo National University.\"",
        "\"Even while he was in Mokpo, he attended an alternative school and learned dance and singing for about two years. Then he went up to Seoul and prepared for another two years.\"",
    ]),
    para(
        "In other words, his training started back in Mokpo, and it took about four years in total before he reached the stage of THE NEW WORLD.",
        "It wasn't the path his family had expected, either.",
        "His father recalled, \"No one in our family was good at singing or dancing,\" and added, \"I thought he would study business or economics, but he went into fashion and clothing, and from there he found yet another path.\"",
    ),
    MAP_UNIV,

    h2("In Seoul, he worked overnight at a car wash from 10 p.m. to 8 a.m."),
    mini([
        ("Job: ", "Car wash (night shift)"),
        ("Hours: ", "10 p.m. to 8 a.m. the next morning"),
    ]),
    para("The most surprising part is his life in Seoul.",
        f"While studying vocals and dance, SHINHAENG {mk('also held down an overnight job')}."),
    quote_box("His father, as reported by Jeonnam Ilbo", [
        "\"He prepared while working at a car wash from 10 p.m. to 8 a.m. the next morning.\"",
        "\"We helped a bit as parents, but he held out by working, too.\"",
    ]),
    para(
        "That's close to ten hours overnight, even with breaks.",
        "With lessons during the day and the car wash at night, he must have been getting by on very little sleep.",
        "Supporting his own dream instead of relying entirely on his parents says a lot about his resilience.",
    ),

    h2("\"Just two more years\": his family's deadline and finding PRODUCE 101 JAPAN"),
    mini([
        ("Family's condition: ", "\"Let's try for about two more years\""),
        ("How he found the show: ", "Through the academy he attended in Seoul, among others"),
    ]),
    para("Because debut was never guaranteed, his family worried a great deal."),
    quote_box("His father, as reported by Jeonnam Ilbo", [
        "\"All we could do was worry about when, or whether, it would happen.\"",
        "\"He had to decide whether to go back to school or go to the military, so we gave him about two more years, and at the very end a good opportunity seems to have come.\"",
    ]),
    para(
        "Korean men are required to do military service, so the early twenties are when many have to choose between returning to school and enlisting.",
        "Considering the chance came right at the end of those two years, it was a debut seized at the last possible moment.",
        "His father also noted, \"PRODUCE 101 JAPAN seems to have gone international from its fourth season,\" and \"the format where foreign participants can take part too became an opportunity for Shin-haeng.\"",
        f"To see how the other members got here, check out {a(L_ZENSE_EN, 'what KO1KEYZ’s 12 members were doing before debut')}.",
    ),

    h2("Why his dad was happiest about the \"Mokpo\" caption"),
    mini([
        ("On-screen caption: ", "Oh Shin-haeng (Mokpo)"),
        ("Address vs. hometown: ", "Registered in Muan County, but born and raised in Mokpo"),
    ]),
    para("What delighted his father most wasn't the ranking, but the fact that the show listed SHINHAENG's hometown as Mokpo."),
    quote_box("His father, as reported by Jeonnam Ilbo", [
        "\"His registered address is Muan, but the place he was born and raised, and where he lived his life, was Mokpo.\"",
        "\"Our first, second, and third children all went to Mokpo National University. I always hoped my children would stay connected to the region.\"",
    ]),
    para("SHINHAENG is the middle of three siblings, between an older sister and a younger sister, which means all three went to their hometown university."),
    MAP_MOKPO,

    h2("Running for office was his dad's idea, and he pushed back every day"),
    mini([
        ("Election: ", "2022 8th Nationwide Local Elections, Muan County Council (District Na), independent"),
        ("Result: ", "5.88% of the vote, 6th place, not elected"),
    ]),
    para(
        "His 2022 run was actually his father's suggestion.",
        "It came right after a revision of Korea's election law lowered the minimum candidate age from 25 to 18.",
    ),
    quote_box("His father, as reported by Jeonnam Ilbo", [
        "\"Lowering it from 25 to 18 was a big change. I encouraged him to run so that he, too, would be part of that history.\"",
        "\"He had never thought about the election at all. At first he argued with me every day about why he had to run, and I asked him not to give up and to see it through to the end.\"",
    ]),
    para(
        "Reluctant at first, SHINHAENG came to see the campaign as a learning experience, his father said, as interviews and study led him to think there were things he could do for young people.",
        f"His slogan was \"A youth candidate, by youth, for youth,\" and his pledges included {mk('fair-trade travel for teens, stock investment funds for young people, a youth assembly, and trash sorting-and-compacting machines')}.",
        "He finished 6th with 5.88% of the vote, but his father said, \"Winning or losing was not the first goal.\"",
        "Japan's NHK even followed him for three days during the campaign, so perhaps his connection to Japan started back then.",
    ),

    h2("After debut: \"10% of my salary to each of my parents\""),
    mini([
        ("What he said: ", "Once he gets paid, he'll give 10% each to his mom and dad"),
        ("When: ", "A plan he shared just before debut (June 2026)"),
    ]),
    para("The interview ended with a story sure to warm fans' hearts."),
    quote_box("His father, as reported by Jeonnam Ilbo", [
        "\"I heard that in Japan, unlike Korea, you get a monthly salary from the start of your debut.\"",
        "\"Shin-haeng said he's so busy he doesn't even have time to spend money, and that when he gets his salary he'll give 10% each to his mom and dad.\"",
    ]),
    para(
        "The son who once worked night shifts to support his dream now wants to give back to his parents.",
        "Note that this was a plan he shared before debut; how and when he has actually done it has not been made public.",
        "His father also admitted he worried SHINHAENG, who had never studied Japanese, would struggle when asked to speak, but said with relief, \"Fortunately an interpreter was by his side, and he seems to have done well.\"",
        "He closed with a message for his son: \"Now that he's active as part of a team, not alone, he has to be considerate of those around him,\" and \"I hope someday he becomes someone who helps Mokpo and the region.\"",
    ),

    h2("SHINHAENG (Oh Shin-haeng) profile"),
    spec_box("SHINHAENG's profile", [
        ("Real name", "Oh Shin-haeng"),
        ("Birthday", "May 3, 2004"),
        ("Hometown", "Mokpo, South Jeolla Province, Korea (registered in Muan County)"),
        ("Height", "177cm"),
        ("Member color", "Brown"),
        ("THE NEW WORLD result", "Debuted in KO1KEYZ after finishing 4th"),
    ]),
    para(
        "After drawing attention in 2022 as the nation's youngest candidate at 18, SHINHAENG finished 4th on PRODUCE 101 JAPAN: THE NEW WORLD and became a member of KO1KEYZ.",
        f"He has also revealed his signature scent; see {a(L_PERFUME_EN, 'our article on SHINHAENG’s perfume')}.",
    ),

    h2("Summary"),
    summary_box("SHINHAENG's pre-debut years, summarized", [
        "After the 2022 election, he took leave from Mokpo National University's fashion department",
        "About 2 years of training in Mokpo and 2 in Seoul: 4 years in total",
        "In Seoul, he worked overnight at a car wash from 10 p.m. to 8 a.m.",
        "His family gave him \"two more years\" as a deadline",
        "Running for office was his father's idea, and he pushed back at first",
        "Before debut, he said he'd give 10% of his salary to each parent",
        "All from his father Oh Won-ok's interview with Jeonnam Ilbo (June 15, 2026)",
    ]),
    para("Knowing there were four years of night shifts and practice behind the spotlight, SHINHAENG's performances may look a little different next time you watch!"),
    related_box("More about SHINHAENG", [
        (L_PERFUME_EN, "SHINHAENG's perfume is Le Labo's matcha scent? He said so himself"),
        (L_ZENSE_EN, "What were KO1KEYZ's 12 members doing before debut?"),
        (L_FAMILY_JP, "Oh Shin-haeng's family (in Japanese)"),
        (L_WIKI_JP, "Oh Shin-haeng's career profile (in Japanese)"),
    ]),
])
EN_SUMMARY = (
    "Before debuting in KO1KEYZ, SHINHAENG worked overnight at a Seoul car wash, 10 p.m. to 8 a.m., while training. "
    "His father told Jeonnam Ilbo about the four years after his election run and his 10% salary promise."
)


# ============================== POST ==============================
def make_eyecatch(bottoms, out_name, seed, lang=None):
    out = ROOT / "images" / out_name
    cmd = [sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
           "--top", "KO1KEYZ", "--main", "SHINHAENG"]
    for b in bottoms:
        cmd += ["--bottom", b]
    cmd += ["--out", str(out), "--seed", str(seed)]
    if lang:
        cmd += ["--lang", lang]
    subprocess.run(cmd, check=True)
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HA, "Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{out_name}"'},
        data=out.read_bytes(),
    )
    r.raise_for_status()
    return r.json()["id"]


def post_draft(title, content, slug, lang, cats, media, summary, ja_id=None):
    payload = {
        "title": title, "content": content, "slug": slug, "status": "draft", "lang": lang,
        "categories": cats, "featured_media": media, "author": 2,
        "meta": {"jetpack_publicize_message": summary},
    }
    if ja_id:
        payload["translations"] = {"ja": ja_id}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers={**HA, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    for name, t, c in (("JP", JP_TITLE, JP_CONTENT), ("KR", KR_TITLE, KR_CONTENT), ("EN", EN_TITLE, EN_CONTENT)):
        assert "<hr" not in c
        text = re.sub(r"<!--.*?-->|<[^>]+>", "", c, flags=re.S)
        print(name, "title len:", len(t), "| chars:", len(text))
    assert len(JP_TITLE) <= 35
    if "--dry" in sys.argv:
        (ROOT / "tmp_shinhaeng_carwash_jp.html").write_text(JP_CONTENT, encoding="utf-8")
        sys.exit(0)
    jp_eye = make_eyecatch(["洗車場で夜勤バイト？", "父が明かした下積み4年！"],
                           "ko1keyz_shinhaeng_carwash_father_eyecatch.png", seed=503)
    kr_eye = make_eyecatch(["세차장 야간 알바?", "아버지가 밝힌 데뷔 전 4년!"],
                           "ko1keyz_shinhaeng_carwash_father_eyecatch_kr.png", seed=503, lang="kr")
    jp = post_draft(JP_TITLE, JP_CONTENT, BASE_SLUG, "ja", [66, 88], jp_eye, JP_SUMMARY)
    JP_ID = jp["id"]
    print("JP", JP_ID, jp["slug"], f"{WP_URL}/?p={JP_ID}", "media", jp_eye)
    kr = post_draft(KR_TITLE, KR_CONTENT, BASE_SLUG + "-kr", "ko", [74], kr_eye, KR_SUMMARY, JP_ID)
    print("KR", kr["id"], kr["slug"], f"{WP_URL}/?p={kr['id']}", "media", kr_eye)
    en = post_draft(EN_TITLE, EN_CONTENT, BASE_SLUG + "-en", "en", [110], jp_eye, EN_SUMMARY, JP_ID)
    print("EN", en["id"], en["slug"], f"{WP_URL}/?p={en['id']}", "media", jp_eye)
    (ROOT / "tmp_shinhaeng_carwash_ids.txt").write_text(
        f"jp={JP_ID} kr={kr['id']} en={en['id']} jp_eye={jp_eye} kr_eye={kr_eye}\n", encoding="utf-8")
