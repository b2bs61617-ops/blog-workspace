# -*- coding: utf-8 -*-
"""chomoand-0.com: NHKドラマぎゅぎゅっと展 in 中之島で松村北斗(雉真稔)の学生服・小道具が展示された記事(2026-11-10 オシリ依頼)
元ネタ: NHK大阪公式X(2117210111609635315)のイベント告知 + 来場者のX投稿(Xiy収集 tools/Xiy/_gyugyu_minoru_1110, _gyugyu_comecome_1110)
usage: python tools/_build_hokuto_gyugyutten_minoru_1110.py [--dry]
"""
import json, base64, os, re, sys, subprocess, socket
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "articles" / "hokuto_gyugyutten_minoru_1110.html"
POSTED = ROOT / "articles" / "hokuto_gyugyutten_minoru_1110_posted.json"
EYECATCH = ROOT / "images" / "hokuto_gyugyutten_minoru_1110_eyecatch.jpg"
IMGDIR = ROOT / "tools" / "Xiy" / "_gyugyu_minoru_1110" / "images"
DRY = "--dry" in sys.argv

TITLE_BODY = "松村北斗の稔の学生服はどんな展示だった？ぎゅぎゅっと展レポ"
TITLE = "【未】" + TITLE_BODY

BAR, BG, BORDER = "#333333", "#f5f5f5", "#d5d5d5"
MARK = "#d2d3d6"

# (key, local file, source tweet, alt)
IMAGES = [
    ("sign", "post_12_img_1.jpg", "https://x.com/tomo_tomochi/status/2119314489166418024", "NHKドラマぎゅぎゅっと展 in 中之島の案内看板"),
    ("lineup", "post_19_img_1.jpg", "https://x.com/ST_mhktjcmstjky/status/2119265054105407709", "歴代朝ドラの衣装の列に並ぶ稔の学生服"),
    ("uniform", "post_6_img_2.jpg", "https://x.com/zu_n2525/status/2119407571346080116", "雉真稔(松村北斗)の学生服とマント"),
    ("dict", "post_6_img_3.jpg", "https://x.com/zu_n2525/status/2119407571346080116", "稔(松村北斗)が使用した英和辞典"),
    ("notice", "post_6_img_4.jpg", "https://x.com/zu_n2525/status/2119407571346080116", "稔の死亡告知書"),
    ("letter", "post_21_img_2.jpg", "https://x.com/T226SSK/status/2119076711459688552", "安子から稔宛の手紙"),
    ("record", "post_21_img_3.jpg", "https://x.com/T226SSK/status/2119076711459688552", "カムカムエヴリバディのレコード"),
    ("bike", "post_16_img_3.jpg", "https://x.com/huwahuwa_tail77/status/2119289216865861997", "安子と稔の思い出の自転車"),
    ("meimei", "post_12_img_3.jpg", "https://x.com/tomo_tomochi/status/2119314489166418024", "るいの命名書"),
    ("scripts", "post_5_img_4.jpg", "https://x.com/sRRIzi0B7fsubNP/status/2119575920122232950", "BK朝ドラ50作コレクションの台本展示"),
]


def p(s):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(s) + "</p>\n<!-- /wp:paragraph -->"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def mk(t):
    return f'<strong><span style="font-size:1.1em;background:linear-gradient(transparent 60%,{MARK} 60%);">{t}</span></strong>'


def box(title, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BAR};color:#fff;">{title}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(rows):
    lines = "\n".join(f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
                      for i, (k, v) in enumerate(rows))
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {BAR};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{lines}
</div>''')


def table(header, rows):
    th = "".join(f'<th style="padding:8px;border:1px solid {BORDER};">{c}</th>' for c in header)
    trs = "\n".join("<tr>" + "".join(f'<td style="padding:8px;border:1px solid {BORDER};">{c}</td>' for c in r) + "</tr>" for r in rows)
    return wphtml(f'''<div style="overflow-x:auto;margin:0 0 16px 0;">
<table style="border-collapse:collapse;width:100%;min-width:480px;font-size:0.92em;">
<thead><tr style="background:{BAR};color:#fff;">{th}</tr></thead>
<tbody>
{trs}
</tbody></table></div>''')


def summary(items):
    lis = "\n".join(
        f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {BAR};border-radius:3px;color:{BAR};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{i}</p>'
        for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BAR};color:#fff;">まとめ</p>
<div style="padding:14px 18px;background:{BG};">
{lis}
</div>
</div>''')


def linkbox(items):
    lis = "\n".join(f'<li><a href="{u}">{t}</a></li>' for u, t in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {BAR};border-radius:4px;margin:0 0 16px 0;padding:14px 18px;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい</p>
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


# ---------- WordPress ----------
env = {}
for line in open(ROOT / ".env", encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_AUDITION_URL"].rstrip("/")
AUTH = {"Authorization": "Basic " + base64.b64encode(f"{env['WP_AUDITION_USERNAME']}:{env['WP_AUDITION_APP_PASSWORD']}".encode()).decode()}
posted = json.loads(POSTED.read_text(encoding="utf-8")) if POSTED.exists() else {}
media = posted.setdefault("media", {})


def upload(key, fname, alt):
    if key in media:
        return media[key]
    if DRY:
        return {"large": f"https://example.com/{fname}", "w": 768, "h": 1024, "srcset": ""}
    path = IMGDIR / fname
    r = requests.post(f"{BASE}/wp-json/wp/v2/media", headers={**AUTH, "Content-Type": "image/jpeg",
                      "Content-Disposition": f'attachment; filename="gyugyutten-minoru-{key}.jpg"'}, data=path.read_bytes())
    r.raise_for_status()
    m = r.json()
    requests.post(f"{BASE}/wp-json/wp/v2/media/{m['id']}", headers=AUTH, json={"alt_text": alt})
    sizes = m["media_details"].get("sizes", {})
    big = sizes.get("large") or sizes.get("full")
    srcset = ", ".join(f'{sizes[s]["source_url"]} {sizes[s]["width"]}w' for s in ("medium", "large", "full") if s in sizes)
    media[key] = {"id": m["id"], "large": big["source_url"], "w": big["width"], "h": big["height"], "srcset": srcset}
    POSTED.write_text(json.dumps(posted, ensure_ascii=False, indent=2), encoding="utf-8")
    return media[key]


IMG = {}
for key, fname, src, alt in IMAGES:
    IMG[key] = (upload(key, fname, alt), src, alt)


def fig(key):
    m, src, alt = IMG[key]
    ss = f' srcset="{m["srcset"]}" sizes="(max-width: 1024px) 100vw, 1024px"' if m.get("srcset") else ""
    return wphtml(f'''<figure class="wp-block-image size-large"><img src="{m["large"]}" alt="{alt}" width="{m["w"]}" height="{m["h"]}" style="max-width:100%;height:auto;"{ss}><figcaption>出典:{src}</figcaption></figure>''')


NHK_TWEET = "https://twitter.com/nhk_osaka_JOBK/status/2117210111609635315"
EMBED = wphtml(f'''<blockquote class="twitter-tweet" data-lang="ja"><p lang="ja" dir="ltr">＼イベントのお知らせ／<br>#ブラッサム 🌸や #豊臣兄弟 ！ 過去のNHK大阪制作朝ドラ作品まで…展示や体験が大阪・中之島にぎゅぎゅっと大集合！</p>&mdash; NHK大阪放送局 (@nhk_osaka_JOBK) <a href="{NHK_TWEET}">2026年11月2日</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>''')

# ---------- body ----------
b = []
b.append(p([
    "2026年11月7日・8日の2日間だけ、大阪中之島美術館で「NHKドラマぎゅぎゅっと展 in 中之島」が開かれました。",
    "NHK大阪放送局が制作した朝ドラや大河ドラマの衣装・小道具が集まったイベントで、なかでも注目を集めたのが、" + mk("『カムカムエヴリバディ』で松村北斗が演じた雉真稔の学生服と小道具") + "です。",
    "稔さんの学生服のほか、英和辞典、死亡告知書、安子からの手紙、思い出の自転車まで展示され、会場には長い行列ができました。",
    "同じ週末にはSixTONESのスタジアムライブが大阪・ヤンマースタジアム長居で開かれていたこともあり、ライブ前に立ち寄ったファンも多かったようです。",
    "短い開催期間で、行きたくても行けなかった人も多かったはずです。",
    "そこでこの記事では、展示された稔さんゆかりの品を" + mk("写真つきでひとつずつレポート") + "します。",
    "会場の様子や当日の混雑ぶりもあわせて紹介するので、行った気分で楽しんでください。",
]))
b.append(box("この記事でわかること", [
    "NHKドラマぎゅぎゅっと展はどんなイベントだった？",
    "雉真稔(松村北斗)の学生服と小道具の展示レポ(写真つき)",
    "カムカムエヴリバディのほかに展示された作品",
    "当日の混雑・待ち時間と会場の様子",
    "今から展示を見る方法はある？",
]))

b.append(h2("NHKドラマぎゅぎゅっと展はどんなイベントだった？"))
b.append(p([
    "「NHKドラマぎゅぎゅっと展 in 中之島」は、NHK大阪放送局が開いた入場無料のイベントです。",
    "放送中の朝ドラ『ブラッサム』や大河ドラマ『豊臣兄弟！』に加えて、過去にNHK大阪が制作した朝ドラの展示や体験コーナーが、ひとつの会場に“ぎゅぎゅっと”集められました。",
    "NHK大阪放送局の公式Xでも、11月2日にイベントの告知が出ていました。",
]))
b.append(EMBED)
b.append(minibox([
    ("イベント名", "NHKドラマぎゅぎゅっと展 in 中之島"),
    ("日時", "2026年11月7日(土)・8日(日) 午前10時〜午後5時"),
    ("会場", "大阪中之島美術館"),
    ("入場料", "無料"),
    ("主催", "NHK大阪放送局"),
]))
b.append(fig("sign"))
b.append(p([
    "会場の入り口には案内の看板が立ち、アンケートに答えると、イラストレーターの井上涼さんがデザインしたポストカードがもらえる企画もありました。",
    "大阪中之島美術館では、同じ時期に「NHK日曜美術館50年展」(12月20日まで・有料)も開かれていて、2つの展示をはしごした人もいたようです。",
    "なお、ぎゅぎゅっと展は" + mk("11月8日(日)で終了") + "しています。",
]))

b.append(h2("松村北斗(雉真稔)の展示レポ！何があった？"))
b.append(p([
    "『カムカムエヴリバディ』は、2021年11月から2022年4月に放送されたNHK大阪制作の朝ドラです。",
    "安子(上白石萌音)・るい(深津絵里)・ひなた(川栄李奈)の3世代、100年にわたる物語で、松村北斗は安子の夫となる" + mk("雉真稔") + "を演じました。",
    "放送から5年近くたった今回の展示でも、カムカムのコーナーは稔さんゆかりの品が中心で、会場でひときわ人が集まる場所になっていました。",
    "展示されていた主な品は、次のとおりです。",
]))
b.append(table(["展示品", "どんなもの？"], [
    ["学生服(マント付き)", "雉真稔役・松村北斗が着た学生服"],
    ["英和辞典", "稔が使用した辞書。表紙に「雉真稔」の名前"],
    ["死亡告知書", "稔の戦死を家族に知らせた書類"],
    ["手紙", "安子から稔に宛てた手紙と封筒"],
    ["自転車", "安子と稔の思い出の自転車"],
    ["命名書・レコードなど", "るいの命名書、レコード、ラジオ英語講座のテキストなど"],
]))

b.append(h3("稔さんの学生服は歴代ヒロインの衣装と並んで展示"))
b.append(fig("lineup"))
b.append(p([
    "会場の中央には、NHK大阪が制作した歴代の朝ドラの衣装がずらりと並んでいました。",
    "その列のいちばん端に置かれていたのが、稔さんの学生服です。",
    "ヒロインたちの着物やワンピースが並ぶ中に、男性キャラクターの衣装が1着だけ入っている形で、それだけ稔さんが作品を代表するキャラクターとして扱われていることがわかります。",
]))
b.append(fig("uniform"))
b.append(p([
    "学生服は、黒の詰襟に金ボタン、その上に丈の長いマントを羽織ったスタイルです。",
    "名札には「雉真稔役 松村北斗 学生服」と書かれていました。",
    "稔さんが大阪の大学に通っていたころの姿で、安子と出会い、心を通わせていった時代を思い出させる衣装です。",
    "実際に目の前で見ると、背の高さや肩幅の大きさがよくわかり、ヒロインの衣装と並ぶことで大きさに驚いたという声も多く見られました。",
]))

b.append(h3("表紙に名前が書かれた英和辞典"))
b.append(fig("dict"))
b.append(p([
    "茶色い革の表紙に、筆で「雉真稔」と書かれた英和辞典です。",
    "説明の札には「稔(松村北斗)が使用した英和辞典」とありました。",
    "稔さんは英語やアメリカの音楽に強い関心を持っていて、安子に英語の楽しさを伝えた人物でもあります。",
    "この英語へのあこがれは、安子からるい、そしてひなたへと受け継がれていく物語の大切な軸になりました。",
    "表紙の角のすれや色あせまで細かく作り込まれていて、見ているだけで英語を勉強したくなったという感想も見られました。",
]))

b.append(h3("胸がしめつけられる死亡告知書と安子の手紙"))
b.append(fig("notice"))
b.append(p([
    "物語の中でもっともつらい場面につながるのが、この死亡告知書です。",
    "書類には、海軍中尉・雉真稔が昭和20年8月、南九州の洋上で戦死したことが記されていました。",
    "戦地に向かった稔さんが帰らなかったことを家族に知らせる1枚で、ドラマを見ていた人にとっては「稔さんロス」を思い出す展示です。",
]))
b.append(fig("letter"))
b.append(p([
    "死亡告知書の近くには、安子が稔さんに宛てて書いた手紙も展示されていました。",
    "封筒の宛名は「雉真稔様」。",
    "便箋には何枚にもわたって文字がつづられていて、離れて暮らす稔さんを思う安子の気持ちが伝わってきます。",
    "届けたい相手に宛てた手紙と、その相手の死を知らせる書類が近くに並んでいることに、涙が出たという来場者も少なくありませんでした。",
    "ドラマを知らずに見た人からは、手紙の字のきれいさに驚く声も上がっていたそうです。",
]))

b.append(h3("安子と稔の思い出の自転車"))
b.append(fig("bike"))
b.append(p([
    "会場の床に、チェーンで囲われて置かれていたのが黒い自転車です。",
    "安子と稔さんの思い出が詰まった自転車で、フレームやサドル、荷台まで当時の雰囲気そのままでした。",
    "ガラスケースに入っていない大きな展示なので、ぐるりと回りながら見られるのもうれしいポイントでした。",
]))

b.append(h3("るいの命名書やレコードも"))
b.append(fig("meimei"))
b.append(p([
    "稔さんと安子の娘・るいの命名書も展示されていました。",
    "「るい」という名前は、稔さんが大好きだったジャズ・トランペッターのルイ・アームストロングにちなんだものです。",
    "ほかにも、劇中で印象的に使われたレコードや、物語とつながるラジオ英語講座のテキストなど、稔さんの思いが次の世代へつながっていくことを感じられる品が並んでいました。",
]))
b.append(fig("record"))

b.append(h2("カムカムのほかに展示された作品は？"))
b.append(p([
    "ぎゅぎゅっと展では、カムカムエヴリバディのほかにも、NHK大阪(BK)が制作したさまざまな作品の展示がありました。",
    "主な展示は次のとおりです。",
]))
b.append(table(["作品", "主な展示・体験"], [
    ["ブラッサム(放送中の朝ドラ)", "桜の木のオブジェ、YOASOBIが選んだ宇野千代のことばの「咲き誇れみくじ」、衣装"],
    ["豊臣兄弟！(大河ドラマ)", "出演者の等身大パネル"],
    ["ばけばけ", "劇中に登場した絵"],
    ["カーネーション", "糸子のミシン"],
    ["スカーレットほか歴代朝ドラ", "ヒロインたちの衣装"],
    ["BK朝ドラ50作コレクション", "NHK大阪が制作した朝ドラ50作品すべての台本"],
]))
b.append(fig("scripts"))
b.append(p([
    "壁一面に並んだ「BK朝ドラ50作コレクション」には、NHK大阪制作の朝ドラ50作品の台本がそろっていました。",
    "その中にはもちろん、カムカムエヴリバディの台本(第1週)も展示されていました。",
    "会場の大きなスクリーンでは朝ドラの歴史を振り返る映像が流れていて、カムカムの稔さんが映った瞬間、会場がうっとりとした空気に包まれたという声もありました。",
]))

b.append(h2("当日の混雑・待ち時間は？"))
b.append(p([
    "ぎゅぎゅっと展は2日間だけの開催だったこともあり、会場はとても混み合いました。",
    "Xに投稿された来場者の声をもとに、日にちごとの様子をまとめると次のようになります。",
]))
b.append(table(["日時", "様子"], [
    ["11月7日(土) 昼ごろ", "稔さんの展示前は5人ほど。カムカムの展示だけなら10〜15分で見られた"],
    ["11月8日(日) 午前〜昼", "入場まで30分〜1時間半ほど並んだという声が多数"],
    ["11月8日(日) 午後", "最終日で行列がさらに伸びる。会場の外まで列が続いた"],
]))
b.append(p([
    "とくに2日目の8日は、" + mk("1時間半並んだという声も出るほどの大行列") + "になりました。",
    "8日はSixTONESのライブツアー「MILESixTONES」大阪公演の2日目で、開演は午後5時。",
    "ライブ前の時間を使って中之島に立ち寄ったファンが多く、来場者の投稿でも、SixTONESファンの多さや北斗さんの人気の高さを実感したという声が目立ちました。",
    "一方で、稔さんの展示の前だけ人の流れが止まってしまい、ほかの作品を見たい人が待つ場面もあったようです。",
    "人気の展示ほど、写真を撮ったら次の人にゆずる気づかいが大切ですね。",
]))
b.append(p([
    "大阪公演の服装や開演時間については、<a href=\"https://chomoand-0.com/sixtones-stadium-osaka-fashion-goods-1172\">SixTONES大阪スタジアムの服装は？開演時間とグッズも！</a>でまとめています。",
]))

b.append(h2("今からでも稔さんの展示は見られる？"))
b.append(p([
    "ぎゅぎゅっと展は11月8日で終わってしまったため、今のところ同じ展示を見る方法はありません。",
    "ただ、NHK大阪放送局では、これまでもBKプラザなどで朝ドラの衣装や小道具を展示するイベントを行ってきました。",
    "今回の大行列を見ると、カムカムや稔さんの展示が再び企画される可能性もありそうです。",
    "新しい展示の情報は、NHK大阪放送局の公式Xで告知されることが多いので、チェックしておくと安心です。",
    "再展示などの情報が出たら、この記事にも追記します。",
]))
b.append(p([
    "稔さんの役で、松村北斗はザテレビジョンドラマアカデミー賞の助演男優賞を受賞するなど、俳優としての評価を大きく高めました。",
    "その後も映画やドラマへの出演が続き、最新の主演映画については<a href=\"https://chomoand-0.com/matsumura-hokuto-mada-minu-kimi-e-1284\">松村北斗主演「まだ見ぬ君へ」公開日はいつ？</a>でまとめています。",
    "放送から5年近くたっても、これだけ多くの人が会いに来る稔さんは、まさに「忘れられない人」と言えそうです。",
]))

b.append(h2("まとめ"))
b.append(summary([
    "NHKドラマぎゅぎゅっと展 in 中之島は、2026年11月7日・8日に大阪中之島美術館で開催(入場無料・終了済み)",
    "カムカムエヴリバディの雉真稔(松村北斗)の学生服が、歴代朝ドラヒロインの衣装と並んで展示",
    "英和辞典・死亡告知書・安子の手紙・自転車・るいの命名書なども展示",
    "SixTONESの大阪公演と重なり、8日は1時間半待ちの声も出るほどの大行列",
]))
b.append(p([
    "学生服から辞書、手紙まで、稔さんの人生をたどるような展示に、会場では多くの人が足を止めていました。",
    "行けなかった人も、このレポで少しでも会場の雰囲気を感じてもらえたらうれしいです。",
    "見に行けなかった人も、写真を見ながら、もう一度カムカムエヴリバディを見返してみてはいかがでしょうか。",
]))
b.append(linkbox([
    ("https://chomoand-0.com/matsumura-hokuto-mada-minu-kimi-e-1284", "松村北斗主演「まだ見ぬ君へ」公開日はいつ？堀田真由とのあらすじと原作は？"),
    ("https://chomoand-0.com/matsumura-hokuto-hamaru-kokuhaku-kujo-1175", "松村北斗にハマる人が急増なぜ？告白と九条の大罪が話題！"),
    ("https://chomoand-0.com/matsumura-hokuto-profile-education-1150", "松村北斗の学歴は？出身地の静岡島田と大学・経歴まとめ！"),
    ("https://chomoand-0.com/matsumura-hokuto-suito-hydroflask-1440", "松村北斗の愛用水筒はどこの？アメリカのボトルブランドと判明！"),
]))

content = "\n\n".join(b)
OUT.write_text(content, encoding="utf-8")
print("title len (without 【未】):", len(TITLE_BODY))


def run(*args):
    r = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    print(r.stdout[-500:], r.stderr[-500:])
    if r.returncode != 0:
        sys.exit(f"failed: {args}")


run(ROOT / "tools" / "honorific.py", "fix", "--group", "sixtones", "--names", "上白石萌音,深津絵里,川栄李奈,井上涼", OUT)
run(ROOT / "tools" / "honorific.py", "check", "--group", "sixtones", "--names", "上白石萌音,深津絵里,川栄李奈,井上涼", OUT)
run(ROOT / "tools" / "sixtones_theme.py", OUT, "--member", "松村北斗")
content = OUT.read_text(encoding="utf-8")
plain = re.sub(r"<!--.*?-->|<[^>]+>", "", content, flags=re.S)
print("chars:", len(re.sub(r"\s", "", plain)))
if DRY:
    sys.exit()

AUTHORS = {"USER1": 2, "Tomoki": 1, "Yuka-MacBook-NEO": 1}
host = socket.gethostname().split(".")[0]
AUTHOR = next((v for k, v in AUTHORS.items() if host.lower().startswith(k.lower())), 2)

if "post_id" in posted:
    requests.post(f"{BASE}/wp-json/wp/v2/posts/{posted['post_id']}", headers=AUTH, json={"content": content}).raise_for_status()
    print("UPDATED", posted["post_id"])
    sys.exit()

r = requests.post(f"{BASE}/wp-json/wp/v2/posts", headers=AUTH, json={
    "title": TITLE, "content": content, "status": "draft", "slug": "matsumura-hokuto-gyugyutten-minoru",
    "categories": [15, 18], "author": AUTHOR})
r.raise_for_status()
post = r.json()
posted["post_id"] = post["id"]
POSTED.write_text(json.dumps(posted, ensure_ascii=False, indent=2), encoding="utf-8")
print("POST_ID", post["id"], post["status"], post["link"])

eye = subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_sixtones.py"), "--top", "カムカムエヴリバディ", "--main", "松村北斗",
                      "--bottom", "稔の学生服はどんな展示？", "--bottom", "ぎゅぎゅっと展レポ！",
                      "--color-key", "松村北斗", "--out", str(EYECATCH)],
                     capture_output=True, text=True, encoding="utf-8", errors="replace")
print(eye.stdout[-300:], eye.stderr[-300:])
if eye.returncode == 0:
    m = requests.post(f"{BASE}/wp-json/wp/v2/media", headers={**AUTH, "Content-Type": "image/jpeg",
                      "Content-Disposition": f'attachment; filename="{EYECATCH.name}"'}, data=EYECATCH.read_bytes())
    m.raise_for_status()
    requests.post(f"{BASE}/wp-json/wp/v2/posts/{post['id']}", headers=AUTH,
                  json={"featured_media": m.json()["id"], "status": "draft"}).raise_for_status()
    print("eyecatch media", m.json()["id"])
print("DONE")
