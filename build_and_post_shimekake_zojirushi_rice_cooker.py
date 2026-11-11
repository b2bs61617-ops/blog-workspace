# -*- coding: utf-8 -*-
"""七五三掛龍也が『ぽかぽか』(2026/11/11)のベストバイで紹介した炊飯器
=象印「炎舞炊き」NX-AB10とみられる(中村海人からの誕生日プレゼント)。chomoand-4.blog下書き、【未】付き.

python build_and_post_shimekake_zojirushi_rice_cooker.py --html   本文HTMLだけ書き出す(チェック用)
python build_and_post_shimekake_zojirushi_rice_cooker.py --post <eyecatch.jpg>  下書き投稿(二重投稿注意)
"""
import os, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_OUT = ROOT / "tmp_shimekake_zojirushi_rice_cooker.html"

C_BORDER, C_ACCENT, C_BG = "#f3c6d9", "#e7a1c8", "#fdf1f6"
U = "https://chomoand-4.blog"
NONSTOP_1023_X = "https://x.com/nonstop_fujitv/status/2113444112397676934"
ZOJI_PRODUCT = "https://www.zojirushi.co.jp/syohin/rice/ricecooker/nx-ab/"
ZOJI_NEWS = "https://www.zojirushi.co.jp/corp/news/2026/260514/NXAB.html"
KAKAKU_MAG = "https://kakakumag.com/seikatsu-kaden/?id=22482"
# 楽天(生活家電ディープライス NX-AB10-BZ 107,500円 2026/11/11時点)・Amazon検索。affiliate_linker.pyで取得
RAKUTEN_URL = ("https://hb.afl.rakuten.co.jp/hgc/g00pqhin.vxz95d17.g00pqhin.vxz96678/?pc=https%3A%2F%2Fitem.rakuten.co.jp"
               "%2Fd-price%2Fnx-ab10-bz%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fd-price%2Fi%2F10099801%2F"
               "&rafcid=wsc_i_is_04cda4eb-00a4-43bd-be26-fcaa4d5caf0c")
RAKUTEN_IMG = "https://thumbnail.image.rakuten.co.jp/@0_mall/d-price/cabinet/d74/nx-ab10-bz_1.jpg?_ex=400x400"
AMAZON_URL = "https://www.amazon.co.jp/s?k=%E8%B1%A1%E5%8D%B0+%E7%82%8E%E8%88%9E%E7%82%8A%E3%81%8D+NX-AB10&tag=chomoand03-22"
SPON = 'target="_blank" rel="nofollow sponsored noopener"'


def productbox():
    btn = "display:inline-block;margin:4px;padding:10px 18px;border-radius:4px;color:#fff;font-weight:bold;text-decoration:none;"
    return wphtml(f'''<div style="border:1px solid {C_BORDER};border-radius:4px;padding:16px;margin:0 0 16px 0;background:#fff;text-align:center;">
<a href="{RAKUTEN_URL}" {SPON}><img src="{RAKUTEN_IMG}" alt="象印 圧力IH炊飯ジャー 炎舞炊き NX-AB10-BZ(黒)" width="300" height="300" style="max-width:100%;height:auto;"></a>
<p style="margin:8px 0 4px 0;font-weight:bold;">象印 圧力IH炊飯ジャー 炎舞炊き NX-AB10(5.5合炊き)</p>
<p style="margin:0 0 8px 0;font-size:0.85em;color:#888;">写真は黒(NX-AB10-BZ)。白(NX-AB10-WZ)もあります</p>
<a href="{RAKUTEN_URL}" {SPON} style="{btn}background:#bf0000;">楽天で見る</a>
<a href="{AMAZON_URL}" {SPON} style="{btn}background:#232f3e;">Amazonで見る</a>
</div>''')


def wphtml(s): return f"<!-- wp:html -->\n{s}\n<!-- /wp:html -->"
def p(lines): return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->"
def h2(t): return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'
def h3(t): return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->'
def marker(t): return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'
def a(url, t): return f'<a href="{url}" target="_blank" rel="noopener">{t}</a>'
def inner(pid, t): return f'<a href="{U}/?p={pid}">{t}</a>'
def xembed(url):
    return wphtml(f'<blockquote class="twitter-tweet" data-lang="ja"><a href="{url}"></a></blockquote>'
                  '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def titlebox(title, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {C_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{C_ACCENT};color:#fff;">{title}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{C_BG};">
{lis}
</ul>
</div>''')


def minibox(rows):
    ps = "\n".join(f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
                   for i, (k, v) in enumerate(rows))
    return wphtml(f'''<div style="border:1px solid {C_BORDER};border-left:4px solid {C_ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{C_BG};">
{ps}
</div>''')


def table(header, rows):
    th = "".join(f"<td><strong>{c}</strong></td>" for c in header)
    trs = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            f'<tr style="background:{C_BG};">{th}</tr>\n{trs}\n</tbody></table></figure>\n<!-- /wp:table -->')


def checklist(items):
    chk = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {C_ACCENT};border-radius:3px;'
           f'color:{C_ACCENT};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')
    ps = "\n".join(f'<p style="margin:0 0 8px 0;">{chk}{i}</p>' for i in items)
    return wphtml(f'<div style="border:1px solid {C_BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{C_BG};">\n{ps}\n</div>')


def linkbox(title, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {C_BORDER};border-left:4px solid {C_ACCENT};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{C_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


TITLE = "【未】【ぽかぽか】七五三掛龍也の炊飯器はどこの？中村海人からの誕プレ！"
SLUG = "shimekake-ryuya-zojirushi-enbudaki-rice-cooker"
b = []

b.append(wphtml('<p style="font-size:12px;color:#888;">本記事はプロモーションを含みます</p>'))
b.append(p([
    "Travis Japanの七五三掛龍也が、2026年11月11日の『ぽかぽか』(フジテレビ系)に出演しました。",
    "番組の「ベストバイ」で紹介したのは、なんと自宅で使っている炊飯器です。",
    f"この炊飯器は{marker('象印の「炎舞炊き」')}で、メンバーの中村海人からの誕生日プレゼントでした。",
]))
b.append(p([
    "この記事では、炊飯器の型番や値段、どんなところがすごいのかをまとめます。",
    "『ノンストップ！』で話していた炊飯器のエピソードも紹介します。",
]))
b.append(titlebox("この記事でわかること", [
    "七五三掛龍也の炊飯器のメーカーと型番",
    "炊飯器の値段と、今から買えるか",
    "炎舞炊きのすごいところ",
    "中村海人から誕生日にもらった話",
    "ノンストップ！で話していた炊飯器の話",
]))

# ---- answer ----
b.append(h2("七五三掛龍也の炊飯器は象印の炎舞炊き"))
b.append(minibox([
    ("メーカー", "象印マホービン"),
    ("商品名", "圧力IH炊飯ジャー「炎舞炊き」"),
    ("型番", "NX-AB10(5.5合炊き)とみられる"),
    ("色", "黒(NX-AB10-BZ)と白(NX-AB10-WZ)の2色"),
    ("発売日", "2026年6月21日"),
    ("値段", "オープン価格(ネットでは10万円前後)"),
]))
b.append(productbox())
b.append(p([
    "七五三掛龍也は、11月11日の『ぽかぽか』に、伊原六花と一緒に出演しました。",
    "2人はドラマ『小麦とバターと復讐と』で共演していて、その宣伝をかねた出演です。",
]))
b.append(p([
    "番組には、出演者が最近買ってよかった物を紹介する「ベストバイ」があります。",
    "七五三掛龍也が持ってきたのは、ふだん家で使っている炊飯器そのものでした。",
    "スタジオで紹介された炊飯器は、象印の「炎舞炊き」です。",
]))
b.append(p([
    "炎舞炊きは、象印の炊飯器の中でいちばん上のシリーズです。",
    "今売られている5.5合炊きの最新モデルは、2026年6月21日発売の「NX-AB10」です。",
    "放送では型番まで言っていないため、このNX-AB10とみられます。",
]))
b.append(p([
    "見た人の声では、スタジオの炊飯器は黒だったようです。",
    "メンバーカラーのピンクではなく、シンプルな黒を使っているのも七五三掛龍也らしいところです。",
]))

b.append(h3("ぽかぽかで話した炊飯器のこと"))
b.append(p([
    "七五三掛龍也は、この炊飯器をもらう前は5,000円くらいの炊飯器を使っていたそうです。",
    "炎舞炊きにしてから、ご飯のおいしさが全然ちがうと話していました。",
]))
b.append(p([
    "スタジオでは、伊原六花が炊飯器をのぞきこんで、きれいに使っているかチェックする場面もありました。",
    "Xでは、本体に貼られた注意書きのシールがそのままだったことに気づいた人もいました。",
    "大事に使っている様子が伝わってきて、ほっこりした人も多かったようです。",
]))
b.append(p([
    "「ベストバイ」なのに、自分で買ったのではなくもらった物だったことも話題になりました。",
    "それだけ中村海人からのプレゼントがうれしくて、みんなに見せたかったのかもしれません。",
]))

# ---- price ----
b.append(h2("七五三掛龍也の炊飯器の値段は？"))
b.append(p([
    "炎舞炊きNX-AB10は、メーカーが値段を決めていない「オープン価格」の商品です。",
    "そのため、お店によって値段がちがいます。",
]))
b.append(p([
    f"{a(KAKAKU_MAG, '価格.comマガジン')}の2026年9月の記事では、最安値は95,437円でした。",
    "2026年11月11日に楽天市場を見ると、黒は10万6千円くらいから売られていました。",
    f"だいたい{marker('10万円前後')}の、かなり高い炊飯器です。",
]))
b.append(table(
    ["", "NX-AB10", "NX-AB18"],
    [
        ["炊ける量", "0.5〜5.5合", "1合〜1升"],
        ["色", "黒・白", "黒・白"],
        ["発売日", "2026年6月21日", "2026年6月21日"],
    ],
))
b.append(p([
    "ひとり暮らしや2〜3人の家なら、5.5合炊きのNX-AB10で十分です。"  # 管理画面で「十分」に直された(easy_read fixで戻るので注意),
    "一度にたくさん炊きたい家族なら、1升炊きのNX-AB18もあります。",
]))

b.append(h3("今から買える？"))
b.append(p([
    "NX-AB10は今も売られている最新モデルなので、家電量販店や通販で買えます。",
    "ただし、お店によっては在庫切れになっていることもあります。",
    "値段もお店ごとにちがうので、いくつか比べてから買うのがおすすめです。",
]))
b.append(titlebox("購入先", [
    a(ZOJI_PRODUCT, "象印公式サイト(炎舞炊き NX-AB型)"),
    f'<a href="{RAKUTEN_URL}" {SPON}>楽天市場(NX-AB10-BZ 黒)</a>',
    f'<a href="{AMAZON_URL}" {SPON}>Amazon(炎舞炊き NX-AB10)</a>',
    "家電量販店(店頭・ネットショップ)",
]))

# ---- features ----
b.append(h2("炎舞炊きのすごいところは？"))
b.append(p([
    "炎舞炊きは、昔のかまどで炊いたようなご飯を目指して作られた炊飯器です。",
    "かまどの火がゆらゆらと動くように、釜の中のお米をしっかりかき混ぜながら炊きます。",
]))
b.append(h3("底のヒーターが順番に熱くなる"))
b.append(p([
    "炎舞炊きの底には、6つのIHヒーターが並んでいます。",
    "そのうち2つずつを順番に強く熱くして、釜の中に大きな流れを作ります。",
    "象印はこれを「3DローテーションIH構造」とよんでいます。",
]))
b.append(p([
    "お米が釜の中でよく動くので、まん中までムラなく熱が伝わります。",
    "その結果、一粒一粒がふっくらとした、甘みのあるご飯に炊き上がります。",
]))
b.append(h3("2026年モデルは「蒸らし」が新しくなった"))
b.append(p([
    f"{a(ZOJI_NEWS, '象印の発表')}によると、NX-AB型では「蒸らし」のやり方が新しくなりました。",
    "蒸らしのときも、底のヒーターで部分的に強く熱くする「集中加熱蒸らし」です。",
    "これで、前のモデルよりご飯の弾力がさらに増したそうです。",
]))
b.append(h3("好みのかたさに炊き分けられる"))
b.append(p([
    "「炊き分けセレクト」では、かたさ3段階と粘り5段階を組み合わせて、15通りから選べます。",
    "さらに「わが家炊き」では、食べた感想を入力すると、121通りの中から好みの味に近づけてくれます。",
]))
b.append(p([
    "保温は「極め保温」で、最大40時間おいしく保てます(メニューによってちがいます)。",
    "時間がないときは、白米1合なら約15分で炊ける「特急」メニューも使えます。",
]))
b.append(h3("お手入れはかんたん"))
b.append(p([
    "毎回洗う部品は、内ぶたと内釜の2つだけです。",
    "内ぶたは食器洗い乾燥機でも洗えます。",
    "料理を始めたばかりの人でも、毎日気軽に使いやすい炊飯器です。",
]))

# ---- Nakamura ----
b.append(h2("中村海人から誕生日にもらった炊飯器"))
b.append(p([
    "七五三掛龍也の誕生日は6月23日です。",
    "この炊飯器は、メンバーの中村海人から誕生日プレゼントとしてもらった物です。",
    "炎舞炊きの最新モデルが出たのは6月21日なので、出たばかりの新品だった可能性もあります。",
]))
b.append(p([
    "ファンの間では、2人のコンビは「しめんちゅ」とよばれています。",
    "高価な炊飯器を贈った中村海人と、それをテレビで何度も紹介する七五三掛龍也。",
    f"{marker('2人の仲の良さ')}が伝わるエピソードに、Xでは喜ぶ声がたくさん上がっていました。",
]))
b.append(p([
    "放送を見て、「同じ炊飯器を買いたい」「うちも炎舞炊きでおいしい」という声も多く見られました。",
]))

# ---- Nonstop ----
b.append(h2("ノンストップ！でも炊飯器の話をしていた"))
b.append(p([
    "七五三掛龍也は、フジテレビ系『ノンストップ！』で料理コーナー「七五三掛KITCHEN」を担当しています。",
    "料理を始めたばかりの七五三掛龍也が、「料理アイドル」を目指すコーナーです。",
]))
b.append(p([
    "炊飯器の話が出たのは、2026年10月23日の放送です。",
    "この日は「鮭のムニエル クリーミーソース」を作りました。",
]))
# 2026-11-11 管理画面でX埋め込みが削除されたので入れない(ID2530 rev2533)
b.append(p([
    "料理を作る前のトークで、七五三掛龍也は「メンバーから炊飯器をもらった」とうれしそうに話しました。",
    "すると設楽統が「メンバーカラーの炊飯器？」と勘ちがいして、スタジオは笑いに包まれました。",
    "七五三掛龍也のメンバーカラーはピンクなので、ピンクの炊飯器を想像したようです。",
]))
b.append(p([
    "10月30日の放送のころには、家でおにぎりを作っていた話もしていました。",
    "もらった炊飯器が、毎日の料理で大活躍しているのが伝わってきます。",
    f'七五三掛KITCHENのレシピは、{inner(2406, "【七五三掛KITCHEN】背徳のサバみそのレシピは？")}でも紹介しています。',
]))

# ---- other topics ----
b.append(h2("ぽかぽかではほかにどんな話をした？"))
b.append(p([
    "11月11日の『ぽかぽか』では、炊飯器のほかにもたくさんの話題がありました。",
    "とくにXで盛り上がったのは、次の2つです。",
]))
b.append(h3("竹中直人が「海人元気？」"))
b.append(p([
    "伊原六花へのサプライズゲストとして、俳優の竹中直人がスタジオに登場しました。",
    "竹中直人は、七五三掛龍也に「海人元気？」と何度も聞いていました。",
]))
b.append(p([
    "竹中直人は、ドラマで中村海人のお父さん役をしたことがあります。",
    "Travis Japanにはカイトが3人いるので、七五三掛龍也は一瞬「どのカイト？」という顔に。",
    "炊飯器に続いて、ここでも中村海人の名前が出たことに、ファンは大喜びでした。",
]))
b.append(h3("神田愛花がかいた七五三掛龍也の絵"))
b.append(p([
    "神田愛花がかいた七五三掛龍也の絵も、スタジオを大いにわかせました。",
    "体型のことを心配した結果、ふっくらした七五三掛龍也の絵になっていたのです。",
    "一方で、岩井勇気がかいた絵は、キラキラした王子様のようだと好評でした。",
]))
b.append(p([
    "番組では、週5回ジムに通って体を整えていることも話していました。",
    "このあともジムに行く予定だと話していて、ストイックな一面も見せていました。",
]))

# ---- summary ----
b.append(h2("まとめ"))
b.append(checklist([
    "七五三掛龍也が『ぽかぽか』のベストバイで紹介した炊飯器は、象印の「炎舞炊き」",
    "型番は2026年6月発売の最新モデルNX-AB10(5.5合炊き)とみられる",
    "値段はオープン価格で、ネットでは10万円前後",
    "メンバーの中村海人からの誕生日プレゼント",
    "10月23日の『ノンストップ！』でも炊飯器の話をしていた",
]))
b.append(p([
    "高価な炊飯器を贈った中村海人と、それを大切に使う七五三掛龍也の仲の良さが伝わる放送でした。",
    "七五三掛龍也の手料理が、これからどんどん上手になっていくのも楽しみですね。",
]))
b.append(linkbox("あわせて読みたい", [
    inner(2406, "【七五三掛KITCHEN】背徳のサバみそのレシピは？"),
    inner(2450, "【ノンストップ】七五三掛龍也の金ネックレスはどこのブランド？"),
    inner(2204, "七五三掛龍也のピアスはどこの？クロムハーツのタイニーCHプラス！"),
]))

content = "\n\n".join(b)

if "--html" in sys.argv:
    HTML_OUT.write_text(content, encoding="utf-8")
    print("wrote", HTML_OUT, len(content))
    sys.exit()

if "--post" in sys.argv:
    import requests
    sys.path.insert(0, str(ROOT / "tools"))
    import x_auto_post_buffer as xb
    env = xb.load_env(ROOT / ".env")
    env.update({k: v.strip("\"'") for k, v in xb.load_env(Path(os.path.expanduser(
        "~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))).items() if v})
    WP = env["WP_CHOMO4_URL"].rstrip("/"); A = (env["WP_CHOMO4_USERNAME"], env["WP_CHOMO4_APP_PASSWORD"])
    final_html = HTML_OUT.read_text(encoding="utf-8")  # honorific/easy_read で直した版を使う
    eye = Path(sys.argv[sys.argv.index("--post") + 1])
    m = requests.post(f"{WP}/wp-json/wp/v2/media", auth=A, timeout=120, data=eye.read_bytes(),
                      headers={"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{eye.name}"'}).json()
    print("MEDIA", m.get("id"))
    r = requests.post(f"{WP}/wp-json/wp/v2/posts", auth=A, timeout=120, json={
        "title": TITLE, "content": final_html, "slug": SLUG, "status": "draft",
        "categories": [3, 8, 10], "author": 2, "featured_media": m.get("id")}).json()
    print("POST", r.get("id"), r.get("status"), r.get("link"))

if "--update" in sys.argv:  # 下書き2530の本文だけ差し替える(写真・アフィリエイト追加 2026-11-11 ユカ依頼)
    import requests
    sys.path.insert(0, str(ROOT / "tools"))
    import x_auto_post_buffer as xb
    env = xb.load_env(ROOT / ".env")
    env.update({k: v.strip("\"'") for k, v in xb.load_env(Path(os.path.expanduser(
        "~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))).items() if v})
    WP = env["WP_CHOMO4_URL"].rstrip("/"); A = (env["WP_CHOMO4_USERNAME"], env["WP_CHOMO4_APP_PASSWORD"])
    pid = int(sys.argv[sys.argv.index("--update") + 1])
    r = requests.post(f"{WP}/wp-json/wp/v2/posts/{pid}", auth=A, timeout=120,
                      json={"content": HTML_OUT.read_text(encoding="utf-8")}).json()
    print("UPDATE", r.get("id"), r.get("status"), r.get("title", {}).get("rendered"))
