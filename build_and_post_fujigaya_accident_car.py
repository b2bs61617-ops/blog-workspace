# -*- coding: utf-8 -*-
"""藤ヶ谷太輔(Kis-My-Ft2) 衝突事故(2026-10-31)の事故車=ベンツGLC 記事 -> chomoand.com 下書き投稿.

事故車の車種は報道に記載なし。ANNニュースの現場写真(@shisaneko の引用画像)から
メルセデス・ベンツ GLC(初代X253型)と推定。本文でも「写真から〜とみられる」と推定表記にする。
価格は2019/10/3マイナーチェンジ発表時の新車価格(Car Watch / car-repo.jp)。
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

ACCENT = "#37474f"
ACCENT_BG = "#f3f6f8"
AUTHOR = 3  # momo(オシリと作った記事は著者momo)
EXISTING_POST_ID = None
BASE = "fujigaya_accident_car"
EYECATCH_PATH = ROOT / "images" / f"{BASE}_eyecatch.png"

title = "藤ヶ谷太輔が事故時に乗っていた車は何？ベンツGLCの値段がヤバい！"
slug = "fujigaya-taisuke-accident-car"


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


B = []
B.append(p([
    "Kis-My-Ft2の藤ヶ谷太輔さんが、2026年10月31日に東京・世田谷区で車の衝突事故を起こしていたことが報じられました。",
    "けが人はいなかったものの、ニュースで流れた現場写真を見て「藤ヶ谷さんが乗っていた車は何？」と気になった人も多いようです。",
]))
B.append(p([
    "結論から言うと、現場写真に写っている藤ヶ谷さん側の車は、" + marker("黒のメルセデス・ベンツ「GLC」") + "とみられます。",
    "GLCの新車価格は、2019年の改良時点で" + marker("約690万円から") + "、高性能なAMGモデルでは900万円を超えます。",
    "この記事では、事故車の車種や値段、事故の概要、藤ヶ谷さんの謝罪内容をまとめます。",
]))
B.append(box("この記事でわかること", [
    "藤ヶ谷太輔が事故時に乗っていた車の車種",
    "ベンツGLCとはどんな車か、新車価格はいくらか",
    "事故が起きた日時・場所・状況",
    "藤ヶ谷太輔がブログでつづった謝罪の内容",
    "「一時停止違反」とはどんな違反か",
]))

B.append(h2("藤ヶ谷太輔が事故時に乗っていた車は何？"))
B.append(p([
    "藤ヶ谷さんが乗っていた車について、警察や報道機関から車種の発表は出ていません。",
    "ただ、ANNニュースが伝えた現場写真には、事故を起こした2台の車がはっきり写っています。",
]))
B.append(x_embed("shisaneko", "2117904412165451979"))
B.append(p([
    "ANNニュースの事故状況の図では、側道から国道246号に入った黒い車が藤ヶ谷さんの車、国道を走っていたシルバーのセダンが相手の車として描かれています。",
    "この黒い車の前面を見ると、大きなスリーポインテッド・スター(ベンツのマーク)が付いたグリルがあり、車体はSUVの形です。",
]))
B.append(h3("写真からベンツGLCと判断したポイント"))
B.append(box("車種を見分けたポイント", [
    "グリル中央に大きなベンツのエンブレム",
    "横に長いヘッドライトと、ボンネットの形がGLCの特徴と一致",
    "屋根にルーフレールが付いた、背の高いSUVの車体(屋根がなだらかに下がるクーペ型ではない)",
    "大きなアルミホイールとスポーティーなバンパーから、外装を引き締める「AMGライン」仕様の可能性",
]))
B.append(p([
    "これらの特徴から、藤ヶ谷さんの車は" + marker("初代メルセデス・ベンツGLC(X253型)") + "とみられます。",
    "なお、この判断は報道写真をもとにした当サイトの推定で、グレードや年式までは写真からは分かりません。",
    "また、この車が藤ヶ谷さん個人の車かどうかも報じられていません。",
]))

B.append(h2("ベンツGLCとはどんな車？"))
B.append(p([
    "GLCは、メルセデス・ベンツの人気セダン「Cクラス」をもとにしたミドルサイズのSUVです。",
    "日本では2016年に発売され、街乗りしやすい大きさと高級感から、ベンツのSUVの中でも特に人気の高いモデルの一つです。",
    "2019年10月にはマイナーチェンジ(改良)が行われ、顔つきや装備が新しくなりました。",
]))
B.append(table([
    ("メーカー", "メルセデス・ベンツ(ドイツ)"),
    ("車種", "GLC(初代・X253型)"),
    ("ボディタイプ", "ミドルサイズSUV"),
    ("日本発売", "2016年(2019年10月にマイナーチェンジ)"),
    ("特徴", "Cクラスがベースの上質な乗り心地、4MATIC(四輪駆動)のグレードが中心"),
]))

B.append(h2("ベンツGLCの値段がヤバい！新車価格はいくら？"))
B.append(p([
    "では、ベンツGLCの値段はいくらなのでしょうか。",
    "2019年10月のマイナーチェンジ時に発表された、主なグレードの新車価格は次のとおりです。",
]))
B.append(table([
    ("GLC 220 d 4MATIC", "2.0Lディーゼルターボ(194馬力)", "約690万円"),
    ("GLC 300 4MATIC", "2.0Lガソリンターボ(258馬力)", "約775万円"),
    ("メルセデスAMG GLC 43 4MATIC+", "3.0L V6ツインターボ(390馬力)", "約948万円"),
    ("メルセデスAMG GLC 63 4MATIC+", "4.0L V8ツインターボ", "約1,313万円"),
], head=["グレード", "エンジン", "新車価格(発表時)"]))
B.append(p([
    "一番手ごろなグレードでも約690万円、AMGモデルになると約950万円から1,300万円台と、一般的な乗用車とはケタが違う値段です。",
    "さらにオプションや諸費用を合わせると、実際に支払う金額はこれより高くなるのが一般的です。",
]))
B.append(p([
    "藤ヶ谷さんの車がどのグレードかは写真からは分かりませんが、仮に一番手ごろなグレードだとしても" + marker("新車なら700万円前後") + "の車ということになります。",
    "高級車であることは間違いありませんが、ベンツの中ではGクラス(2,000万円前後)のような超高級モデルではなく、実用的で人気の高いSUVを選んでいるのは意外かもしれません。",
]))

B.append(h2("藤ヶ谷太輔の衝突事故はいつ・どこで？事故の概要"))
B.append(table([
    ("日時", "2026年10月31日 夕方"),
    ("場所", "東京都世田谷区 国道246号付近"),
    ("状況", "一時停止すべき場所で止まらずに側道から国道246号に入り、走ってきた車と衝突したとされる"),
    ("けが人", "なし"),
    ("警察の対応", "警視庁が物損事故として調べている"),
]))
B.append(p([
    "捜査関係者によると、藤ヶ谷さんが運転する車は、一時停止をすべき場所で止まらずに側道から国道246号に入り、走行中の車と衝突したということです。",
    "この事故でけがをした人はいませんでした。",
    "警視庁は物損事故として、詳しい状況を調べています。",
]))
B.append(x_embed("News_ABEMA", "2117915805925146774"))

B.append(h2("藤ヶ谷太輔のブログでの謝罪内容"))
B.append(p([
    "藤ヶ谷さんは11月4日、有料会員向けのブログを更新し、事故について謝罪しました。",
    "スポーツ報知によると、ブログでは次のようにつづっています。",
]))
B.append(quote("報道にございます通り、私の不注意により交通事故（物損事故）を起こしてしまいました",
               "藤ヶ谷太輔さんのブログより(スポーツ報知の報道から引用)"))
B.append(quote("この度は、お相手の方に多大なるご迷惑をおかけしましたこと、心より深くお詫び申し上げます",
               "藤ヶ谷太輔さんのブログより(スポーツ報知の報道から引用)"))
B.append(p([
    "自分の不注意だったと認めたうえで、相手の方へのおわびをはっきりと伝えています。",
    "報道を受けて、自分の言葉で説明したかたちです。",
]))

B.append(h2("「一時停止違反」とはどんな違反？"))
B.append(p([
    "今回の事故で指摘されているのが「一時停止」をしなかった点です。",
    "「止まれ」の標識がある場所では、車は停止線の直前で必ず一度止まらなければならないと、道路交通法で決められています。",
]))
B.append(p([
    "一般的に、この「指定場所一時不停止」の違反は、普通車の場合で違反点数2点、反則金7,000円とされています。",
    "ただし、今回の事故がどのように処理されるかは警察の調べによるため、現時点では分かっていません。",
    "物損事故の場合、相手の車の修理代などは、保険会社を通じた話し合いで決めていくのが一般的です。",
]))
B.append(box("知っておきたい注意点", [
    "車種は報道写真からの推定で、公式に発表されたものではありません",
    "事故の処理や処分は、警視庁の調べにより今後決まります",
    "相手の方がいる事故のため、憶測や誹謗中傷は控えましょう",
]))

B.append(h2("まとめ"))
B.append(box("この記事のまとめ", [
    "藤ヶ谷太輔が事故時に乗っていた車は、現場写真から黒のメルセデス・ベンツGLCとみられる",
    "ベンツGLCの新車価格は約690万円から、AMGモデルは約948万円〜約1,313万円",
    "事故は2026年10月31日夕方、世田谷区の国道246号付近で起きた物損事故で、けが人はなし",
    "藤ヶ谷太輔は11月4日、ブログで「私の不注意」と認めて相手の方に謝罪した",
]))
B.append(p([
    "けが人が出なかったのは不幸中の幸いでした。",
    "新しい情報が分かりしだい、この記事に追記します。",
]))

content = "\n\n".join(B)

if "--dry" in sys.argv:
    import re
    txt = re.sub(r"<[^>]+>", "", content)
    print("chars:", len(re.sub(r"\s", "", txt)), "title len:", len(title))
    sys.exit()

if not EYECATCH_PATH.exists():
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_chomoand.py"),
                    "--top", "事故時に乗っていた車は何？", "--main", "藤ヶ谷太輔",
                    "--bottom", "ベンツGLCの値段がヤバい！", "--out", str(EYECATCH_PATH)], check=True)

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
