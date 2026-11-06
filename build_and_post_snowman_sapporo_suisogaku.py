# -*- coding: utf-8 -*-
"""Snow Man ALL SUITE札幌公演(2026-10-30〜11-01)の駒大苫小牧吹奏楽局サプライズ共演はなぜ炎上? -> chomoand.com 下書き投稿.

出典: Smart FLASH(11/5)、東スポWEB(11/5)、chomoand-2.com ID459(どこの高校?記事)。
"親がアカウント削除"等の未確認情報は書かない。高校生個人は叩かない書き方にする。
"""
import json, base64, os, subprocess, sys
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
WP_URL = ENV["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_TREND_USERNAME']}:{ENV['WP_TREND_APP_PASSWORD']}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

ACCENT = "#1565c0"
ACCENT_BG = "#f1f6fc"
AUTHOR = 4  # anco(ユカのMac、VIVANT記事と同じ)
EXISTING_POST_ID = None
BASE = "snowman_sapporo_suisogaku"
EYECATCH_PATH = ROOT / "images" / f"{BASE}_eyecatch.png"

title = "Snow Man札幌公演の吹奏楽部共演はなぜ炎上？賛否の理由を整理！"
slug = "snow-man-sapporo-brass-band-controversy"


def p(sentences):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(sentences) + "</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def table(rows, head=None):
    th = ""
    if head:
        th = "<thead><tr>" + "".join(
            f'<th style="border:1px solid #ccc;padding:8px 12px;background:{ACCENT};color:#fff;">{h}</th>' for h in head
        ) + "</tr></thead>\n"
        trs = "\n".join(
            "<tr>" + "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;">{c}</td>' for c in r) + "</tr>"
            for r in rows
        )
    else:
        trs = "\n".join(
            f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;width:150px;"><strong>{k}</strong></td>'
            f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
            for k, v in rows
        )
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout">'
            f"{th}<tbody>\n{trs}\n</tbody></table></figure>\n<!-- /wp:table -->")


def box(ttl, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(
        f'<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{ACCENT_BG};">\n{lis}\n</ul>\n</div>'
    )


def x_embed(user, sid):
    tw = f"https://twitter.com/{user}/status/{sid}"
    return wphtml('<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true">'
                  f'<a href="{tw}">{tw}</a></blockquote>\n'
                  '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def quote(text, cite):
    return ('<!-- wp:quote -->\n<blockquote class="wp-block-quote"><!-- wp:paragraph -->\n'
            f"<p>{text}</p>\n<!-- /wp:paragraph --><cite>{cite}</cite></blockquote>\n<!-- /wp:quote -->")


def marker(t):
    return f'<span class="swl-marker mark_yellow">{t}</span>'



def gmap(q):
    import urllib.parse
    src = "https://www.google.com/maps?q=" + urllib.parse.quote(q) + "&output=embed"
    return wphtml(f'<iframe src="{src}" width="100%" height="350" style="border:0;" allowfullscreen="" loading="lazy"></iframe>')


S2 = "https://chomoand-2.com/snow-man-sapporo-marching-band-school-459"

B = []
B.append(p([
    "Snow Manのドームツアー「ALL SUITE」札幌公演で、地元の高校の吹奏楽部がサプライズで登場し、ネットで「炎上している」と話題になっています。",
    "「何があったの？」「なぜ炎上？」と気になっている人も多いのではないでしょうか。",
]))
B.append(p([
    "結論から言うと、炎上のきっかけは" + marker("「お金を払ってSnow Manを見に来たのに、高校生の演奏はいらない」という一部のファンの不満") + "です。",
    "ただ、その後は" + marker("「演出として呼ばれた高校生を責めるのはおかしい」という反論") + "のほうが大きく広がり、今は「ファン同士の賛否」が議論の中心になっています。",
    "この記事では、札幌公演で起きたことと、批判・擁護それぞれの理由、そして吹奏楽部が呼ばれた背景を整理します。",
]))
B.append(box("この記事でわかること", [
    "Snow Man札幌公演で何があったのか",
    "吹奏楽部との共演が炎上した理由",
    "共演を称賛・擁護する声が多い理由",
    "なぜ高校の吹奏楽部が呼ばれたのか(考えられる背景)",
    "名古屋・福岡・東京・大阪でも共演はあるのか",
]))

B.append(h2("Snow Man札幌公演で何があった？吹奏楽部サプライズ共演の内容"))
B.append(p([
    "Snow Manは2026年10月30日から11月1日までの3日間、札幌の大和ハウス プレミストドーム(旧・札幌ドーム)で、ドームツアー「ALL SUITE」の北海道公演を行いました。",
    "3日間で12万人以上が集まった大きな公演で、海外で撮影中だった目黒蓮さんも合流し、9人そろってステージに立ちました。",
]))
B.append(table([
    ("公演", "Snow Man DOME TOUR 2026-2027 ALL SUITE 北海道公演"),
    ("日程", "2026年10月30日(金)・31日(土)・11月1日(日)"),
    ("会場", "大和ハウス プレミストドーム(旧・札幌ドーム)"),
    ("共演", "駒澤大学附属苫小牧高校 吹奏楽局"),
    ("場面", "公演の終盤、数曲で生演奏"),
    ("事前告知", "なし(当日のサプライズ)"),
]))
B.append(p([
    "この公演の終盤に、北海道苫小牧市にある駒澤大学附属苫小牧高校の吹奏楽局が登場し、数曲で生演奏を披露しました。",
    "事前に「高校生が出演する」というお知らせはなく、ほとんどの人が会場で初めて知ったかたちです。",
]))
B.append(gmap("大和ハウス プレミストドーム"))
B.append(h3("メンバーも楽器を持って共演したショー演出"))
B.append(p([
    "初日に参加した人のレポによると、吹奏楽局が登場したのは「EMPIRE」の場面です。",
    "ブラスの生演奏に合わせて、Snow Manのメンバーもスネアドラムなどの打楽器や、カラーガードのフラッグを持って加わる、マーチングショーのような構成だったと伝えられています。",
    "つまり、高校生がただゲストとして出てきたのではなく、" + marker("メンバーと一緒に練習を重ねて作り上げた演出") + "だったと考えられます。",
]))
B.append(p([
    "出演した高校や演奏の場面のくわしい内容は、こちらの記事でまとめています。",
    f'<a href="{S2}">Snow Man札幌のマーチングバンドはどこの高校？他会場も出る？</a>',
]))

B.append(h2("Snow Manと吹奏楽部の共演はなぜ炎上した？"))
B.append(p([
    "では、なぜこの共演が「炎上」と言われるほど話題になったのでしょうか。",
    "批判的な声を整理すると、大きく3つの理由が見えてきます。",
]))
B.append(h3("理由1:チケット代を払って「Snow Manだけ」を見に来ている"))
B.append(p([
    "一番多かったのは、「金払ってファンだけが集まるライブには必要ない」という意見です(Smart FLASHの報道より)。",
    "Snow Manのドーム公演はチケットの倍率が高く、やっと当たった1公演を「9人だけを少しでも長く見たい」と思って参加する人も少なくありません。",
    "そのため、限られた時間の一部を外部の出演者が使うことに、不満を感じた人がいたようです。",
]))
B.append(h3("理由2:遠方から遠征してきたファンが多かった"))
B.append(p([
    "東スポWEBによると、北海道公演には地元の人だけでなく、東京など全国から飛行機や前泊で来たファンが多かったそうです。",
    "交通費や宿泊費をかけて来た人ほど、「地元の高校との共演」というサプライズを素直に楽しめなかった面もあるのかもしれません。",
]))
B.append(h3("理由3:事前告知も理由の説明もなかった"))
B.append(p([
    "今回の共演は、事前のお知らせもなく、なぜコラボしたのかの説明も出ていません。",
    "ある芸能関係者は、「24時間テレビのような番組企画なら、芸能人と高校生の共演は受け入れられやすい」とコメントしています。",
    "テレビ番組の企画の延長などの「理由」が見えていれば、受け止め方は違ったという声もあります。",
    "別の関係者は、批判の矛先は演奏そのものではなく「ゲストが出てくる構成」で、説明がなかったことで疑問が噴き出した可能性があると分析しています。",
]))

B.append(h2("共演を称賛・擁護する声のほうが多い理由"))
B.append(p([
    "一方で、共演を好意的に受け止める声もとても多く上がっています。",
    "特に会場にいた人からは、演奏をほめる感想がたくさん見られました。",
]))
B.append(box("称賛・擁護する声の主な内容", [
    "生楽器の迫力がすごく、録音の音源とは違う感動があった",
    "プロかと思うほど演奏のレベルが高かった",
    "北海道ならではの共演で、地元への貢献にもなる",
    "地方の高校生でも頑張ればSnow Manと同じステージに立てるのは夢がある",
    "演出はSnow Man側が決めたこと。高校生を責めるのはちがう",
]))
B.append(p([
    "特に大きく広がったのが、" + marker("「依頼されて出演した高校生を叩くのはおかしい」") + "という意見です。",
    "高校生たちは自分から出たいと言ったのではなく、アーティスト側の演出として呼ばれ、限られた時間で練習して本番にのぞんでいます。",
    "「不満があるとしても、その矛先を高校生に向けるのはちがう」「推しの評判を下げることになる」という声が多く集まり、批判への反論がさらに注目を集めました。",
    "吹奏楽部の保護者の立場から、生徒を気づかう声も見られました。",
]))

B.append(h2("なぜ高校の吹奏楽部が呼ばれた？考えられる背景"))
B.append(p([
    "Snow Man側や事務所のSTARTO ENTERTAINMENTから、共演の理由についての説明は2026年11月6日時点で出ていません。",
    "ここからは、報道や公演の内容から考えられる背景をまとめます。",
]))
B.append(h3("「ALL SUITE」はショーを見せるツアー"))
B.append(p([
    "今回のツアー「ALL SUITE」は、ホテルをイメージした大がかりなセットで、ショーのように見せる演出が特徴です。",
    "メンバー自身がスネアやフラッグを持ってマーチングに加わる場面は、まさに「ショー」としての見せ場の一つだったと考えられます。",
    "生のブラスバンドと一緒に作ることで、ドームならではの迫力を出したかった可能性があります。",
]))
B.append(h3("サプライズになったのは情報管理の厳しさから"))
B.append(p([
    "東スポWEBは、STARTO社は外部とのコラボのときに演出や情報の管理を厳しくチェックすることで知られていると伝えています。",
    "今回も高校側と念入りに打ち合わせをして、情報がもれないよう頼んでいたとみられ、その結果として完全なサプライズになったという見方です。",
    "サプライズで驚かせたかった一方で、事前に知らされなかったことが一部の反発につながったとも言えそうです。",
]))
B.append(h3("旧ジャニーズ系では珍しいが、前例もある"))
B.append(p([
    "旧ジャニーズ事務所・STARTO社のグループが、コンサートで高校の吹奏楽部と共演するケースは多くありません。",
    "ただ、2024年にはSUPER EIGHTがアリーナツアーで、高校野球の応援ソングとしても知られる「オモイダマ」を高校の吹奏楽部と共演したことがあります。",
    "駒大苫小牧の吹奏楽局も、そのSUPER EIGHTの北海道公演に参加したと地元紙で報じられており、大きなステージでの共演経験があるチームでした。",
]))

B.append(h2("駒大苫小牧の吹奏楽局ってどんなチーム？"))
B.append(p([
    "共演した駒大苫小牧の吹奏楽局は、マーチングの全国大会に20回以上出場している北海道の強豪です。",
    "プロ野球・北海道日本ハムファイターズの試合での演奏や、アーティストのライブへの出演経験もあり、ドームのような大きな会場での演奏にも慣れています。",
    "東スポWEBも「全国レベルの演奏力」と紹介しており、演奏のレベルそのものを否定する声はほとんど見られません。",
]))
B.append(table([
    ("学校", "駒澤大学附属苫小牧高等学校(北海道苫小牧市)"),
    ("チーム", "吹奏楽局(マーチングにも力を入れている)"),
    ("実績", "マーチングバンド全国大会に20回以上出場"),
    ("主な出演", "プロ野球の試合での演奏、アーティストのライブ出演など"),
]))

B.append(h2("名古屋・福岡・東京・大阪でも吹奏楽部との共演はある？"))
B.append(p([
    "このあとの公演で地元の高校が出演するかどうかは、2026年11月6日時点で発表されていません。",
    "札幌公演も事前のお知らせはなかったため、ほかの会場でも当日まで分からない可能性があります。",
]))
B.append(table([
    ("バンテリンドーム ナゴヤ", "2026年11月26日(木)〜29日(日)"),
    ("みずほPayPayドーム福岡", "2026年12月4日(金)〜6日(日)"),
    ("東京ドーム", "2026年12月23日(水)〜26日(土)"),
    ("京セラドーム大阪", "2027年1月4日(月)〜7日(木)"),
], head=["会場", "日程"]))
B.append(p([
    "今回の賛否を受けて、ほかの会場でも同じ演出が続くのか、内容が変わるのかにも注目が集まっています。",
    "「各地の高校の演奏を聴き比べたい」と楽しみにしている人がいる一方で、気になっている人もいるので、続報を待ちたいところです。",
]))

B.append(h2("「炎上」の本当のところは？"))
B.append(p([
    "「大炎上」という言葉が一人歩きしていますが、中身を見ると、" + marker("Snow Man本人や演奏した高校生が何か問題を起こしたわけではありません") + "。",
    "実際には「演出に疑問を持った一部のファン」と「それに反論するファン」の意見がぶつかり、議論が大きくなったというのが実態に近いです。",
    "会場にいた人の感想は好意的なものが多く、演奏のレベルの高さは多くの人が認めています。",
]))
B.append(box("知っておきたい注意点", [
    "共演の理由は公式に発表されていません(この記事の背景は報道をもとにした推測を含みます)",
    "演出への意見は、出演した高校生や学校ではなく、主催者への問い合わせなどで伝えましょう",
    "未成年の高校生への誹謗中傷や、個人を特定するような投稿は控えましょう",
]))

B.append(h2("まとめ"))
B.append(box("この記事のまとめ", [
    "Snow Man「ALL SUITE」札幌公演(10/30〜11/1)で、駒大苫小牧高校の吹奏楽局がサプライズ出演した",
    "炎上のきっかけは「お金を払ってSnow Manを見に来たのに」という一部のファンの不満",
    "事前告知や理由の説明がなかったことも、疑問が広がった原因とみられる",
    "一方で演奏への称賛や、「高校生を責めるのはちがう」という反論のほうが大きく広がった",
    "共演の理由は未発表。名古屋・福岡・東京・大阪での共演も発表されていない",
]))
B.append(p([
    "ファンの思いがあるからこそ意見が分かれた今回の共演ですが、ステージに立った高校生たちにとっては一生の思い出になったはずです。",
    "名古屋公演以降で新しい情報が出たら、この記事に追記します。",
]))

content = "\n\n".join(B)

if "--dry" in sys.argv:
    import re
    Path("/private/tmp/claude-501/-Users-yuka/edfd8399-ade4-4a41-aeef-1f94b8ce7608/scratchpad/snow_body.html").write_text(content, encoding="utf-8")
    txt = re.sub(r"<[^>]+>", "", content)
    print("chars:", len(re.sub(r"\s", "", txt)), "title len:", len(title))
    sys.exit()

if "--html" in sys.argv:
    content = Path(sys.argv[sys.argv.index("--html") + 1]).read_text(encoding="utf-8")

if not EYECATCH_PATH.exists():
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_chomoand.py"),
                    "--top", "札幌公演の吹奏楽部共演", "--main", "Snow Man",
                    "--bottom", "なぜ炎上？", "--bottom", "賛否の理由を整理！", "--out", str(EYECATCH_PATH)], check=True)

r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                  headers={**HEADERS_AUTH, "Content-Type": "image/png",
                           "Content-Disposition": f'attachment; filename="{BASE}_eyecatch.png"'},
                  data=EYECATCH_PATH.read_bytes())
r.raise_for_status()
media_id = r.json()["id"]

payload = {"content": content, "status": "draft", "categories": [37], "author": AUTHOR, "featured_media": media_id}
if not EXISTING_POST_ID:
    payload.update({"title": title, "slug": slug})
endpoint = f"{WP_URL}/wp-json/wp/v2/posts" + (f"/{EXISTING_POST_ID}" if EXISTING_POST_ID else "")
r = requests.post(endpoint, headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                  data=json.dumps(payload).encode("utf-8"))
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"], "STATUS", post["status"], "MEDIA", media_id)
print("EDIT", f"{WP_URL}/wp-admin/post.php?post={post['id']}&action=edit")
