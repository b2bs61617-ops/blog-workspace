"""chomoand-4.blog: ドラマ『はだかんぼうたち』第1話関連の5記事を下書き投稿する(2026-10-04)."""
import base64, json, mimetypes, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


ENV = load_env(ROOT / ".env")
SITE = ENV["WP_CHOMO4_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_CHOMO4_USERNAME']}:{ENV['WP_CHOMO4_APP_PASSWORD']}".encode()).decode()
HJ = {"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"}
AUTHOR_ID = 1  # Tomoki PC -> anco (docs/wordpress.md)
IMG_DIR = ROOT / "tools" / "Xiy" / "posts_20261004_oshidoraEX" / "images"
IDS_FILE = ROOT / "tmp_hadakanboutachi_ids.json"


def api(path, payload=None, method="POST"):
    req = urllib.request.Request(f"{SITE}/wp-json/wp/v2/{path}", method=method, headers=HJ,
                                 data=json.dumps(payload).encode("utf-8") if payload is not None else None)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def upload_media(filepath, filename, alt):
    mime = mimetypes.guess_type(filename)[0] or "image/jpeg"
    req = urllib.request.Request(f"{SITE}/wp-json/wp/v2/media", data=Path(filepath).read_bytes(), method="POST",
                                 headers={"Authorization": f"Basic {AUTH}", "Content-Type": mime,
                                          "Content-Disposition": f'attachment; filename="{filename}"'})
    with urllib.request.urlopen(req, timeout=120) as r:
        media = json.loads(r.read())
    api(f"media/{media['id']}", {"alt_text": alt, "title": alt})
    return media


# ---------- color themes ----------
BLUE = dict(accent="#5b9bd5", border="#bbdefb", bg="#eef6fd", marker="mark_blue")
PURPLE = dict(accent="#7e57c2", border="#d1c4e9", bg="#f5f2fb", marker="mark_blue")


def para(text):
    """1行=1文で書いた文字列を<br>改行の段落にする."""
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n'


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n'


def html(s):
    return f"<!-- wp:html -->\n{s.strip()}\n<!-- /wp:html -->\n\n"


def mark(t, c):
    return f'<strong><span class="swl-marker {c["marker"]}" style="font-size:1.15em;">{t}</span></strong>'


def infobox(title, rows):
    trs = "".join(
        f'<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:32%;">{k}</td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>' for k, v in rows)
    return html(f'<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>'
                f'<table style="border-collapse:collapse;width:100%;"><tbody>{trs}</tbody></table></div>')


def learnbox(items, c):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return html(f'<div style="border:1px solid {c["border"]};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{c["accent"]};color:#fff;">この記事でわかること</p>'
                f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{c["bg"]};">{lis}</ul></div>')


def minibox(rows, c):
    ps = "".join(f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
                 for i, (k, v) in enumerate(rows))
    return html(f'<div style="border:1px solid {c["border"]};border-left:4px solid {c["accent"]};border-radius:4px;'
                f'padding:10px 16px;margin:0 0 16px 0;background:{c["bg"]};">{ps}</div>')


def reactbox(title, quotes, c):
    q = "<br>".join(f"「{x}」" for x in quotes)
    return html(f'<div style="border:1px solid {c["border"]};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{c["bg"]};">'
                f'<p style="margin:0 0 6px 0;font-weight:bold;font-size:0.9em;color:{c["accent"]};">{title}</p>'
                f'<p style="margin:0;font-size:0.95em;">{q}</p></div>')


def table(header, rows, c):
    th = "".join(f'<td style="border:1px solid #ccc;padding:8px 10px;background:{c["accent"]};color:#fff;"><strong>{h}</strong></td>' for h in header)
    body = ""
    for i, r in enumerate(rows):
        bg = "#fff" if i % 2 == 0 else c["bg"]
        body += "<tr>" + "".join(f'<td style="border:1px solid #ccc;padding:8px 10px;background:{bg};">{v}</td>' for v in r) + "</tr>"
    return (f'<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody><tr>{th}</tr>{body}'
            f'</tbody></table></figure>\n<!-- /wp:table -->\n\n')


CHECK = ('<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {a};border-radius:3px;'
         'color:{a};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')


def summary(items, c):
    lis = "".join(f'<li style="margin:0 0 6px 0;">{CHECK.format(a=c["accent"])}{i}</li>' for i in items)
    return html(f'<div style="border:1px solid {c["accent"]};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{c["bg"]};">'
                f'<ul style="margin:0;padding-left:0;list-style:none;">{lis}</ul></div>')


def related(title, links, c):
    lis = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in links)
    return html(f'<div style="border:1px solid {c["border"]};border-left:4px solid {c["accent"]};border-radius:4px;'
                f'padding:14px 18px;margin:0 0 16px 0;background:{c["bg"]};">'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>'
                f'<ul style="margin:0;padding-left:1.3em;">{lis}</ul></div>')


def img(media, alt, src_url):
    sizes = media["media_details"]["sizes"]
    large = sizes.get("large") or sizes.get("full")
    medium = sizes.get("medium")
    full = sizes.get("full") or {"source_url": media["source_url"], "width": media["media_details"]["width"],
                                 "height": media["media_details"]["height"]}
    srcset = ", ".join(([f"{medium['source_url']} {medium['width']}w"] if medium else []) +
                       [f"{large['source_url']} {large['width']}w", f"{full['source_url']} {full['width']}w"])
    return html(f'<figure class="wp-block-image size-large"><img src="{large["source_url"]}" alt="{alt}" '
                f'width="{large["width"]}" height="{large["height"]}" style="max-width:100%;height:auto;" '
                f'srcset="{srcset}" sizes="(max-width: 1024px) 100vw, 1024px">'
                f'<figcaption style="font-size:0.8em;color:#888;">出典:{src_url}</figcaption></figure>')


# ---------- images (official @oshidoraEX posts) ----------
X = "https://x.com/oshidoraEX/status/"
IMAGES = {
    "opening": ("post_15_img_1.jpg", "hdk_ep1_opening.jpg", "第1話冒頭、一夜を過ごした女性と向き合う鯖崎涼(松田元太)", X + "2106384001326018582"),
    "order": ("post_12_img_1.jpg", "hdk_ep1_order.jpg", "靴店で結婚式用の靴を依頼する石羽拓(髙木雄也)と鯖崎涼(松田元太)", X + "2106385543802327477"),
    "momo": ("post_10_img_1.jpg", "hdk_ep1_momo.jpg", "バーで筒井桃(加藤ローサ)と向き合う鯖崎涼(松田元太)", X + "2106387911562473899"),
    "kiss": ("post_6_img_1.jpg", "hdk_ep1_kiss.jpg", "第1話終盤、筒井桃(加藤ローサ)にキスをする鯖崎涼(松田元太)", X + "2106390581870301327"),
    "shishi": ("post_3_img_1.jpg", "hdk_ep1_shishi.jpg", "靴工房で鯖崎涼(松田元太)と並ぶ浅野詩史(板谷由夏)", X + "2106393837065408551"),
    "wedding": ("post_8_img_1.jpg", "hdk_ep1_wedding.jpg", "結婚式場の下見をする筒井桃(加藤ローサ)と石羽拓(髙木雄也)", X + "2106389489602179384"),
    "omotesando": ("post_13_img_1.jpg", "hdk_ep1_omotesando.jpg", "表参道に立つ靴職人・鯖崎涼(松田元太)", X + "2106384500238569835"),
    "feet": ("post_11_img_1.jpg", "hdk_ep1_feet.jpg", "筒井桃の足に触れる鯖崎涼(松田元太)", X + "2106387097213178271"),
    "kyoko": ("post_2_img_3.jpg", "hdk_ep1_kyoko.jpg", "歯科医の筒井桃(加藤ローサ)と親友の堀田響子(大沢あかね)", X + "2106395095729627563"),
    "sofa": ("post_2_img_1.jpg", "hdk_ep1_sofa.jpg", "第1話で筒井桃(加藤ローサ)に迫る鯖崎涼(松田元太)", X + "2106395095729627563"),
}

TOKYO_TOWER_LINK = ("トラジャのミュージカル・声優・ドラマ出演歴をまとめた記事", "https://chomoand-4.blog/toraja-musical-voice-actor-car-903")
JB_BUY_LINK = ("4thアルバム『Jewelry Basket』の店舗別特典と予約先をまとめた記事", "https://chomoand-4.blog/jewelry-basket-where-can-i-buy-922")
JB_JACKET_LINK = ("『Jewelry Basket』のジャケット写真に隠された仕掛けを調べた記事", "https://chomoand-4.blog/travis-japan-jewelry-basket-jacket-hidden-details-958")


def article_links(slugs, exclude):
    """5記事の相互リンク(公開後のパーマリンクはslugから組み立てる)."""
    names = {
        "ep1": "はだかんぼうたち第1話のあらすじとSNSの反響",
        "song": "主題歌「EGO」と挿入歌「再会愛 Lie 期待して Cry」の曲名・発売日",
        "sabazaki": "鯖崎涼はクズ？松田元太の役どころと原作のあらすじ",
        "tver": "見逃し配信(TVer)と関西の放送時間",
        "live": "松田元太と髙木雄也の初回直前インスタライブの内容",
    }
    return [(names[k], f"{SITE}/{s}") for k, s in slugs.items() if k != exclude]


def build(M, slugs):
    B, P = BLUE, PURPLE
    I = lambda k: img(M[k], IMAGES[k][2], IMAGES[k][3])
    posts = {}

    # ============ 1. 第1話の反響 ============
    c = B
    body = para(f"""
Travis Japanの松田元太さんが主演するドラマ『はだかんぼうたち』が、2026年10月3日(土)の夜にスタートしました。
放送直後からXでは「はだかんぼうたち」がトレンド上位に入り、{mark("2024年のドラマ『東京タワー』から浅野詩史(板谷由夏さん)がサプライズで登場した", c)}ことにも驚きの声が広がっています。
この記事では、第1話のあらすじをネタバレありで振り返りながら、SNSでの反響と第2話の情報をまとめました。
""")
    body += infobox("『はだかんぼうたち』第1話 基本情報", [
        ("放送日", "2026年10月3日(土)23:00〜23:30"),
        ("関西の放送", "阪神の優勝特番のため0:20〜に変更"),
        ("放送枠", "テレビ朝日系「オシドラサタデー」"),
        ("主演", "松田元太(Travis Japan)/鯖崎涼 役"),
        ("見逃し配信", "TVerで第1話を無料配信中"),
    ])
    body += learnbox(["第1話のあらすじ(ネタバレ)", "浅野詩史のサプライズ登場", "SNSの反響", "トレンドの順位", "第2話の放送日"], c)

    body += h2("はだかんぼうたち第1話のあらすじをネタバレ")
    body += minibox([("主な舞台", "表参道の靴店・桃の歯科医院・結婚式場"), ("ラスト", "鯖崎が婚約中の桃にキス")], c)
    body += h3("冒頭からいきなり鯖崎の「愛のない夜」")
    body += para("""
物語は、靴職人の鯖崎涼(松田元太さん)が女性と夜を過ごすシーンから始まります。
「真実の愛。そんなものは、存在しない」という鯖崎のモノローグが重なり、彼がどんな恋愛観を持っているのかが最初の数分で伝わる構成でした。
翌朝、鯖崎は「昨日は最高に楽しかったよ」と軽やかに告げて部屋を出ていきます。
先行カットで話題になっていたシャワーシーンもこの冒頭に登場し、公式Xも「衝撃の連続キスで開幕」と紹介していました。
""")
    body += I("opening")
    body += h3("表参道で美しいパンプスの女性に目を奪われる")
    body += para("""
職場のある表参道へ向かう途中、鯖崎は交差点の雑踏で、ひときわ美しいパンプスを履いた女性に目を奪われます。
その女性こそ、加藤ローサさん演じる歯科医の筒井桃でした。
「靴を見れば、その人が分かる」と考える鯖崎にとって、桃の足元は一瞬で心をつかまれるほど特別なものだったようです。
""")
    body += h3("店に来た客・石羽の婚約者が、あの女性だった")
    body += para("""
その日、鯖崎の勤める靴店に、髙木雄也さん(Hey! Say! JUMP)演じる石羽拓が訪れます。
依頼は、結婚式で履くためのオーダーメイドシューズでした。
「ご結婚、されるんですか？」と何気なく声をかける鯖崎ですが、この時点ではまだ、石羽の婚約者が交差点で見かけた桃だとは気づいていません。
""")
    body += I("order")
    body += h3("桃との再会、そして「…キス、したかったから」")
    body += para("""
やがて鯖崎は桃と再会し、靴をきっかけに距離を縮めていきます。
「足、触ってもいい？」と桃の足元に触れる場面や、「この靴を選んだ桃ちゃんは、きっと着飾るために靴を履く人じゃない」と語りかける場面は、鯖崎の危うい魅力が一番出ていたところかもしれません。
一方の桃は、石羽と結婚式場を下見しながらも「どうして私は…結婚を選ぶんだろう」と心が揺れていきます。
そしてラストでは、鯖崎が桃にキスをし、理由を聞かれて「…キス、したかったから」と答えたところで、Travis Japanの主題歌「EGO」が流れ出しました。
""")
    body += I("momo")
    body += I("kiss")
    body += para(f"""
婚約者のいる女性と、愛を信じない年下の靴職人。
第1話は、2人が一線を越えそうになる瞬間までを一気に描き切る、密度の高い30分でした。
鯖崎がどんな人物なのかをもう少し詳しく知りたい方は、<a href="{SITE}/{slugs['sabazaki']}">鯖崎涼の役どころと原作のあらすじをまとめた記事</a>もあわせてどうぞ。
""")

    body += h2("『東京タワー』の浅野詩史がサプライズ登場！")
    body += minibox([("登場した人物", "浅野詩史(板谷由夏さん・友情出演)"), ("場面", "鯖崎の働く靴工房に客として来店")], c)
    body += para(f"""
第1話でいちばん大きな驚きを呼んだのが、板谷由夏さん演じる浅野詩史の登場でした。
詩史は、2024年4月期にテレビ朝日で放送されたドラマ『東京タワー』(永瀬廉さん主演)の登場人物です。
同じ江國香織さんの小説が原作で、松田元太さんも大原耕二役で出演していました。
今回の『はだかんぼうたち』は、その『東京タワー』のスタッフが再集結して作られた作品でもあります。
""")
    body += I("shishi")
    body += para("""
劇中で詩史は、鯖崎の働く靴工房を訪れ「新しい靴、またお願いできる？」と声をかけます。
どうやら2人は以前からの顔なじみのようで、2つのドラマの世界がつながっていることを感じさせる演出でした。
公式Xによると、松田元太さんが『東京タワー』を思わせる仕草をする場面もあったそうです。
詩史が登場したときのBGMも、『東京タワー』のテーマを新しくアレンジしたものだったと気づいたファンも多くいました。
""")
    body += para(f"""
板谷由夏さんは「撮影現場では『東京タワー』チームの皆さんと再会することができ、とても懐かしく、温かい気持ちになりました」とコメントしています。
松田さんについては、{mark("「もう少し一緒にお芝居をしてみたかった」", c)}と語っていました。
『東京タワー』の本編では耕二と詩史が同じ場面に出ることはほとんどなかったため、2年越しの共演にうれしくなった人も多かったのではないでしょうか。
""")
    body += reactbox("Xでの反応", ["詩史さん出てきてびっくり", "2年経っても詩史さんは詩史さんだった", "とーるとこーじにも会いたい"], c)
    body += para(f"""
松田元太さんのこれまでのドラマ出演については、<a href="{TOKYO_TOWER_LINK[1]}">{TOKYO_TOWER_LINK[0]}</a>でも紹介しています。
""")

    body += h2("はだかんぼうたち第1話へのSNSの反響は？")
    body += minibox([("多かった声", "鯖崎の色気・憎めなさ、詩史の登場、主題歌EGO"), ("トレンド", "「はだかんぼうたち」「詩史さん」がトレンド入り")], c)
    body += para("""
放送中から放送後にかけて、Xには感想の投稿が次々と寄せられました。
特に多かったのは、松田元太さん演じる鯖崎の色気と、それでいてどこか無邪気で憎めないキャラクターへの反応です。
""")
    body += reactbox("鯖崎の色気について", ["色気と可愛さを両方兼ね備える罪深い男", "口元と指先に欲望が表れまくってる", "鯖崎ー悪い男すぎる"], c)
    body += para("""
冒頭からかなり大胆なシーンが続いたこともあり、「30分があっという間だった」「何度も声に出して驚いた」という声も目立ちました。
主題歌「EGO」や、Hey! Say! JUMPの挿入歌「再会愛 Lie 期待して Cry」が初めて流れたことも、両グループのファンにとって大きな話題になっています。
""")
    body += reactbox("主題歌・挿入歌について", ["EGOかかった瞬間静かになった", "今までになかった曲調でカッコいい", "早くフルで聴きたい"], c)
    body += para(f"""
2曲の曲名や収録アルバム、発売日については、<a href="{SITE}/{slugs['song']}">主題歌・挿入歌の情報をまとめた記事</a>で詳しく紹介しています。
""")

    body += h2("トレンドは何位？阪神優勝と並んで上位に")
    body += minibox([("同じ夜の話題", "阪神タイガースのセ・リーグ連覇"), ("関西の放送", "優勝特番のため0:20〜に変更")], c)
    body += para(f"""
放送があった10月3日は、阪神タイガースが2年連続のセ・リーグ優勝を決めた日でもありました。
そのためXのトレンドは阪神一色に近い状態でしたが、「はだかんぼうたち」も放送中から上位に入り、ファンの間では一時2位まで上がったという声も出ていました。
「詩史さん」もあわせてトレンド入りしており、第1話の注目度の高さがうかがえます。
""")
    body += para(f"""
なお、関西地区(ABCテレビ)では阪神の優勝特番が組まれたため、第1話は0時20分からの放送に変更されています。
放送時間の変更や見逃し配信の詳細は、<a href="{SITE}/{slugs['tver']}">見逃し配信と関西の放送時間をまとめた記事</a>をご覧ください。
""")

    body += h2("はだかんぼうたち第2話はいつ？")
    body += minibox([("第2話", "2026年10月10日(土)23:00〜"), ("予告", "第1話放送後に解禁済み")], c)
    body += para("""
第2話は、2026年10月10日(土)の夜11時から放送されます。
第1話の放送後には公式Xで第2話の予告も公開されました。
桃の親友で3児の母・堀田響子(大沢あかねさん)と鯖崎の関係がどう動くのかも、次回以降の大きな見どころになりそうです。
第1話を見逃した方は、TVerで無料配信されているので、第2話の前にチェックしておくのがおすすめです。
""")

    body += h2("まとめ")
    body += summary([
        "第1話は鯖崎の「愛のない夜」から始まり、婚約中の桃へのキスで幕を閉じた",
        "石羽が結婚式用の靴を依頼した相手が鯖崎で、婚約者が桃だった",
        "『東京タワー』の浅野詩史(板谷由夏)が友情出演でサプライズ登場",
        "主題歌EGOと挿入歌「再会愛 Lie 期待して Cry」も初解禁",
        "第2話は10月10日(土)23:00から放送",
    ], c)
    body += para("""
初回から刺激の強い展開と、『東京タワー』とのつながりという大きなサプライズが詰まった第1話でした。
まだ見ていない方は、TVerで鯖崎の危険な魅力を一度体験してみてはいかがでしょうか！
""")
    body += related("はだかんぼうたちの関連記事", article_links(slugs, "ep1") + [TOKYO_TOWER_LINK], c)
    posts["ep1"] = dict(
        title="はだかんぼうたち1話の反響は？詩史サプライズにSNS騒然！",
        content=body, categories=[3], eyecatch="hadakanbou_ep1_eyecatch.png",
        alt="はだかんぼうたち第1話の反響と浅野詩史のサプライズ登場を紹介する記事のアイキャッチ")

    # ============ 2. 主題歌・挿入歌 ============
    c = P
    body = para(f"""
松田元太さん主演のドラマ『はだかんぼうたち』で流れた曲が気になって、曲名を調べた人も多いのではないでしょうか。
結論から言うと、{mark("主題歌はTravis Japanの「EGO」、挿入歌はHey! Say! JUMPの「再会愛 Lie 期待して Cry」", c)}です。
どちらも10月3日の第1話で初めて流れた新曲で、主演の松田さんと、石羽拓役の髙木雄也さんのそれぞれのグループが歌っています。
この記事では、2曲の曲名・曲調・収録アルバムの発売日と、第1話のどの場面で流れたのかをまとめました。
""")
    body += infobox("『はだかんぼうたち』の楽曲 基本情報", [
        ("主題歌", "Travis Japan「EGO」"),
        ("主題歌の収録", "4thアルバム『Jewelry Basket』(2026年11月18日発売)"),
        ("挿入歌", "Hey! Say! JUMP「再会愛 Lie 期待して Cry」"),
        ("挿入歌の収録", "13thアルバム『Juliet』(2026年11月11日発売)"),
        ("初解禁", "2026年10月3日(土)第1話の放送"),
    ])
    body += learnbox(["主題歌「EGO」の曲調", "EGOが流れた場面", "挿入歌「再会愛 Lie 期待して Cry」の曲調", "収録アルバムと発売日", "SNSの反応"], c)
    body += table(["", "主題歌", "挿入歌"], [
        ["曲名", "EGO", "再会愛 Lie 期待して Cry"],
        ["歌", "Travis Japan", "Hey! Say! JUMP"],
        ["ドラマとの縁", "松田元太が主演(鯖崎涼)", "髙木雄也が出演(石羽拓)"],
        ["曲調", "艶やかで緊張感のあるダンスサウンド", "大人っぽいシティポップ"],
        ["収録アルバム", "Jewelry Basket(11/18)", "Juliet(11/11)"],
    ], c)

    body += h2("主題歌はTravis Japanの「EGO」")
    body += minibox([("発表日", "2026年9月18日"), ("テーマ", "「愛することはエゴなのか」")], c)
    body += para(f"""
主題歌を担当するのは、主演の松田元太さんが所属するTravis Japanです。
曲名は「EGO」で、2026年9月18日に主題歌に決まったことが発表されました。
艶やかさと緊張感をまとったダンスサウンドに乗せて、{mark("「愛することはエゴなのか」という問い", c)}を描いた大人のラブソングだと紹介されています。
""")
    body += para("""
歌詞には、プライドや虚栄、欲望、孤独といった、誰かを愛することでむき出しになる感情が込められているそうです。
愛を信じない鯖崎と、結婚を前に心が揺れる桃の物語にそのまま重なるテーマで、ドラマの世界観とリンクするように作られた1曲と言えます。
これまでのTravis Japanの明るく華やかな楽曲とは違う、色気を前面に出した曲調に驚いたファンも多かったようです。
""")
    body += h3("EGOが流れたのは第1話ラストのキスシーン")
    body += para("""
第1話で「EGO」が流れたのは、鯖崎が桃にキスをし、「…キス、したかったから」とつぶやく終盤の場面でした。
公式Xもこの場面の写真に「#EGO」のハッシュタグを添えて投稿しています。
物語がいちばん動いた瞬間に曲が入ってくる演出に、「EGOがかかった瞬間に静かになった」「急に主題歌がかかって叫んだ」という声が多く見られました。
""")
    body += I("kiss")
    body += h3("EGOが収録される『Jewelry Basket』の発売日")
    body += para(f"""
「EGO」は、Travis Japanの4thアルバム『Jewelry Basket』に収録されます。
発売日は2026年11月18日(水)です。
今のところドラマで流れているのは一部分だけなので、フルで聴けるのはアルバムの発売日、もしくはそれより前に配信や音楽番組で解禁されたタイミングになりそうです。
アルバムの予約先や店舗別の特典は<a href="{JB_BUY_LINK[1]}">{JB_BUY_LINK[0]}</a>に、ジャケット写真の細かな仕掛けは<a href="{JB_JACKET_LINK[1]}">{JB_JACKET_LINK[0]}</a>にまとめています。
""")

    body += h2("挿入歌はHey! Say! JUMPの「再会愛 Lie 期待して Cry」")
    body += minibox([("歌", "Hey! Say! JUMP(髙木雄也さんが所属)"), ("収録", "13thアルバム『Juliet』(2026年11月11日発売)")], c)
    body += para(f"""
挿入歌は、石羽拓役で出演している髙木雄也さんが所属するHey! Say! JUMPの新曲です。
タイトルは{mark("「再会愛 Lie 期待して Cry」", c)}で、声に出して読みたくなるような言葉遊びの効いた曲名になっています。
このドラマのために書き下ろされた曲で、Hey! Say! JUMPが得意とする洗練されたリズムダンスと、大人っぽいシティポップの雰囲気を組み合わせた仕上がりだそうです。
""")
    body += I("wedding")
    body += para("""
第1話では、桃と石羽が結婚式場を下見する場面のあたりで初めて流れました。
放送前には公式Xが、この式場の場面のオフショットに「再会愛 Lie 期待して Cry」が似合いそうな素敵な式場ですね、と添えて紹介していました。
主演グループが主題歌、共演者のグループが挿入歌という形で、ドラマの中に2つのグループの新曲が流れるのは珍しい組み合わせです。
「再会愛 Lie 期待して Cry」は、2026年11月11日発売のHey! Say! JUMPの13thアルバム『Juliet』に収録されます。
""")

    body += h2("主題歌・挿入歌へのSNSの反応は？")
    body += minibox([("多かった声", "曲調のかっこよさ、フルで聴きたい"), ("両グループのファン", "それぞれのメンバーのパートに期待")], c)
    body += para("""
放送後のXでは、2曲とも「早くフルで聴きたい」という声が目立ちました。
Travis Japanのファンからは、色気のある曲調への驚きや、メンバーそれぞれの歌割りへの期待が多く寄せられています。
Hey! Say! JUMPのファンの間でも、ドラマでの初解禁を楽しみにしていたという投稿が多く見られました。
""")
    body += reactbox("Xでの反応", ["今までに無かった曲調でとてもカッコイイ", "主題歌と挿入歌がよすぎる", "早くフルで聴きたい"], c)

    body += h2("まとめ")
    body += summary([
        "主題歌はTravis Japanの「EGO」(4thアルバム『Jewelry Basket』11月18日発売)",
        "EGOは第1話ラストの鯖崎と桃のキスシーンで流れた",
        "挿入歌はHey! Say! JUMPの「再会愛 Lie 期待して Cry」(『Juliet』11月11日発売)",
        "主演の松田と、共演の髙木のグループがそれぞれ楽曲を担当",
    ], c)
    body += para("""
ドラマの名場面と一緒に流れる2曲は、回を重ねるごとに印象が深まっていきそうです。
毎週土曜の夜は、物語の展開だけでなく、どの場面で曲が入ってくるのかにも注目して見てみてください！
""")
    body += related("はだかんぼうたちの関連記事", article_links(slugs, "song") + [JB_BUY_LINK], c)
    posts["song"] = dict(
        title="はだかんぼうたちの主題歌・挿入歌は誰？曲名と発売日も！",
        content=body, categories=[3, 4], eyecatch="hadakanbou_song_eyecatch.png",
        alt="はだかんぼうたちの主題歌EGOと挿入歌を紹介する記事のアイキャッチ")

    # ============ 3. 鯖崎涼はクズ？ ============
    c = B
    body = para(f"""
『はだかんぼうたち』で松田元太さんが演じる鯖崎涼が、第1話の放送後「クズすぎる」「でも憎めない」と話題になっています。
結論から言うと、鯖崎は{mark("恋愛に“愛”を求めず、婚約者がいる女性にも、その親友にも惹かれていく危うい男", c)}で、松田さん自身も「悪(わる)っ！」と思ったほどの役どころです。
この記事では、鯖崎涼のプロフィールと「クズ」と言われる理由、主な登場人物の関係、原作小説のあらすじをまとめました。
""")
    body += infobox("鯖崎涼のプロフィール", [
        ("演じる人", "松田元太(Travis Japan)"),
        ("職業", "オーダーメイドの靴メーカーに勤める靴職人兼販売員"),
        ("職場", "表参道の靴工房兼販売店「ならはし」"),
        ("師匠", "オーナーの奈良橋匠(平子祐希さん)"),
        ("恋愛観", "「真実の愛。そんなものは、存在しない」"),
    ])
    body += learnbox(["鯖崎涼はどんな人？", "クズと言われる理由", "それでも憎めない理由", "登場人物の関係", "原作小説のあらすじ"], c)

    body += h2("鯖崎涼はどんな人？")
    body += minibox([("仕事", "オーダーメイドの靴職人兼販売員"), ("口ぐせ", "「靴を見れば、その人が分かる」")], c)
    body += para("""
鯖崎涼は、表参道にある靴工房兼販売店「ならはし」で働く靴職人です。
オーナーで師匠の奈良橋匠(アルコ＆ピースの平子祐希さん)のもと、オーダーメイドの靴を作りながら接客もこなしています。
「靴を見れば、その人が分かる」というほど靴へのこだわりが強く、相手の足元からその人の生き方まで読み取ろうとするのが鯖崎らしさです。
""")
    body += I("omotesando")
    body += para("""
その一方で、恋愛については驚くほど身軽です。
第1話の冒頭では、女性と一夜を過ごした翌朝に「昨日は最高に楽しかったよ」と軽やかに去っていく姿が描かれました。
公式の紹介では、まるで「欲望に手足が生えた」ような生き物とも表現されています。
""")

    body += h2("鯖崎涼がクズと言われる理由")
    body += minibox([("理由1", "愛はいらないと言い切る恋愛観"), ("理由2", "婚約者がいる桃にも、その親友の響子にも惹かれる")], c)
    body += h3("「真実の愛は存在しない」と言い切る")
    body += para("""
鯖崎は第1話で「真実の愛。そんなものは、存在しない」と語ります。
女性と夜を過ごしても、そこに愛があるかどうかは気にしない。
そんな割り切った姿勢が、見ている側からすると「クズ」に映る大きな理由です。
""")
    body += h3("婚約中の桃に近づき、その親友にも惹かれていく")
    body += para(f"""
鯖崎が心を奪われるのは、10歳年上の歯科医・筒井桃(加藤ローサさん)です。
しかも桃は、鯖崎の店で結婚式用の靴を注文した石羽拓(髙木雄也さん)の婚約者でした。
それを知っても鯖崎は桃に近づき、第1話のラストではキスまでしてしまいます。
さらに物語の中で鯖崎は、{mark("桃の高校時代からの親友で3児の母・堀田響子(大沢あかねさん)にも興味を示していく", c)}と紹介されています。
欲望のままに2人の女性の間を揺れ動く危うさこそが、この役のいちばんの特徴です。
""")
    body += I("feet")
    body += h3("松田元太本人も「悪っ！」と思った役")
    body += para("""
松田元太さんは、テレビ朝日の連続ドラマに主演するのはこれが初めてです。
役が決まったときには、鯖崎について「悪(わる)っ！」と思ったと明かしていて、ファンに向けて「どうか嫌いにならないでください！」とコメントしていました。
第1話の放送前には「第1話から、鯖崎が暴れます。浅はかで、“悪い男”の部分が、少しずつ見えてきます」とも語っています。
""")

    body += h2("それでも鯖崎涼が憎めない理由")
    body += minibox([("ポイント", "無邪気さ・靴への誠実さ・孤独の気配")], c)
    body += para("""
ここまで読むと完全な悪役のようですが、放送後のXでは「クズなのに憎めない」という感想が多く見られました。
その理由の1つが、松田さんが持つ無邪気な雰囲気です。
甘い声やくだけた口調で距離を縮めてくる一方、ふとした瞬間に寂しげな表情を見せるので、どこか放っておけない男に見えてきます。
""")
    body += para("""
もう1つは、靴に対しては驚くほど誠実なところです。
「この靴を選んだ桃ちゃんは、きっと着飾るために靴を履く人じゃない」という言葉は口説き文句でありながら、相手をよく見ているからこそ出てくるセリフでもありました。
欲望に正直な部分と、職人としてのまっすぐさが同居していることが、鯖崎という人物を単なるクズで終わらせていないのかもしれません。
""")
    body += reactbox("Xでの反応", ["悪い男すぎる", "かわいいのにすごい男", "鯖崎みたいな人には絶対振り回されちゃう"], c)

    body += h2("はだかんぼうたちの登場人物の関係")
    body += minibox([("三角関係", "鯖崎・桃・響子"), ("桃の婚約者", "石羽拓(髙木雄也さん)")], c)
    body += table(["役名", "キャスト", "鯖崎との関係"], [
        ["筒井桃", "加藤ローサ", "10歳年上の歯科医。鯖崎が惹かれる女性"],
        ["堀田響子", "大沢あかね", "桃の親友で3児の母。鯖崎が興味を示す"],
        ["石羽拓", "髙木雄也", "桃の婚約者。鯖崎に結婚式用の靴を依頼"],
        ["奈良橋匠", "平子祐希", "靴工房「ならはし」のオーナーで鯖崎の師匠"],
        ["陽", "伊藤歩", "桃の姉。鯖崎とは恋愛感情のない友人"],
        ["由紀", "萬田久子", "桃の母"],
        ["堀田隼人", "淵上泰史", "響子の夫"],
        ["水崎葉月", "片岡凜", "鯖崎とのただならぬ関係を予感させる女性"],
        ["石羽みな子", "白宮みずほ", "石羽の妹。桃を慕っている"],
    ], c)
    body += I("kyoko")
    body += para("""
桃の姉・陽は鯖崎の友人という立場で、2人の関係を見守る存在として描かれるそうです。
また、片岡凜さん演じる水崎葉月は、鯖崎との「ただならぬ関係」を予感させる人物として紹介されています。
鯖崎の過去に何があったのかも、今後の物語の鍵になりそうです。
""")

    body += h2("原作小説『はだかんぼうたち』のあらすじ")
    body += minibox([("原作", "江國香織『はだかんぼうたち』(2013年刊行)"), ("映像化", "今回のドラマが初")], c)
    body += para(f"""
原作は、直木賞作家・江國香織さんが2013年に発表した長編小説『はだかんぼうたち』です。
年齢も境遇も違う男女が抱える孤独と愛を、赤裸々に描いた恋愛群像劇で、映像化は今回のドラマが初めてになります。
江國さんの作品では、2024年に同じテレビ朝日の枠で『東京タワー』がドラマ化されており、今回はそのチームが再集結しました。
""")
    body += para("""
原作でも、鯖崎は年上の歯科医・桃と関係を持ちながら、桃の親友の響子へと惹かれていきます。
恋人や夫婦といった「関係の名前」に縛られることへの違和感が、作品全体を通して描かれているのが特徴です。
原作の読者の間では、誰か1人を選んで結ばれる王道の結末ではない、という感想が多く見られます。
ドラマでは鯖崎の過去や新しい登場人物も加わっているので、原作とは違う結末になる可能性もありそうです。
""")

    body += h2("まとめ")
    body += summary([
        "鯖崎涼は表参道の靴工房「ならはし」で働くオーダーメイドの靴職人",
        "「真実の愛は存在しない」と言い切り、婚約中の桃にも親友の響子にも惹かれていく",
        "松田元太本人も「悪っ！」と思ったほどの役で、テレ朝連ドラ初主演作",
        "無邪気さと靴への誠実さがあり、「クズなのに憎めない」という声が多い",
        "原作は江國香織の2013年の小説で、今回が初の映像化",
    ], c)
    body += para(f"""
クズと言われながらも目が離せない鯖崎涼は、松田元太さんの新しい一面が見られる役になりそうです。
第1話の詳しい流れは<a href="{SITE}/{slugs['ep1']}">第1話のあらすじと反響をまとめた記事</a>で紹介しているので、2話の前にあわせてチェックしてみてください！
""")
    body += related("はだかんぼうたちの関連記事", article_links(slugs, "sabazaki") + [TOKYO_TOWER_LINK], c)
    posts["sabazaki"] = dict(
        title="鯖崎涼はクズ？松田元太の役どころと原作のあらすじ！",
        content=body, categories=[3], eyecatch="hadakanbou_sabazaki_eyecatch.png",
        alt="松田元太が演じる鯖崎涼の役どころを紹介する記事のアイキャッチ")

    # ============ 4. 見逃し配信・関西 ============
    c = B
    body = para(f"""
『はだかんぼうたち』の第1話を見逃してしまった、関西だと放送が遅れていた、という声がXで多く上がっています。
結論から言うと、{mark("見逃し配信はTVerで無料、関西(ABCテレビ)の第1話は阪神の優勝特番のため0時20分からの放送", c)}でした。
この記事では、見逃し配信の見方と配信期間の目安、関西で放送時間が変わった理由、第2話の放送日をまとめました。
""")
    body += infobox("『はだかんぼうたち』放送・配信情報", [
        ("通常の放送", "毎週土曜23:00〜23:30(テレビ朝日系)"),
        ("第1話の関西", "10月4日(日)0:20〜(阪神優勝特番のため変更)"),
        ("無料の見逃し配信", "TVer"),
        ("その他の配信", "TELASA(配信予定)"),
        ("第2話", "10月10日(土)23:00〜"),
    ])
    body += learnbox(["見逃し配信はどこで見られる？", "TVerの配信期間の目安", "関西で放送時間が変わった理由", "第2話の放送日"], c)

    body += h2("はだかんぼうたちの見逃し配信はどこ？")
    body += minibox([("無料", "TVer(第1話を配信中)"), ("その他", "TELASA")], c)
    body += para(f"""
『はだかんぼうたち』の見逃し配信は、{mark("無料動画サービスのTVerで見ることができます", c)}。
公式Xでも、第1話の放送後すぐに「TVerで無料配信中」と案内されていました。
アプリをインストールすればスマートフォンやタブレット、テレビからも見られます。
""")
    body += para("""
番組ページで「お気に入り登録」をしておくと、新しい話が配信されたときに通知が届くので見逃しにくくなります。
公式Xも放送前から、見逃し防止のためにTVerのお気に入り登録を呼びかけていました。
また、テレビ朝日系の動画配信サービスTELASAでも配信が予定されているので、過去の回をまとめて見たい方はこちらも選択肢になりそうです。
""")
    body += h3("TVerの配信期間はいつまで？")
    body += para("""
TVerの無料配信は、放送終了後から次の話の放送までのおよそ1週間が目安になることが多いです。
『はだかんぼうたち』の第1話も、第2話が放送される10月10日(土)ごろまでに見ておくのが安心でしょう。
正確な配信終了日時はTVerのエピソードページに表示されるので、見る前に確認しておくのがおすすめです。
""")
    body += I("sofa")

    body += h2("関西のはだかんぼうたちはなぜ遅れた？")
    body += minibox([("理由", "阪神タイガースのセ・リーグ連覇を受けた優勝特番"), ("第1話の放送", "10月4日(日)0:20〜")], c)
    body += para(f"""
10月3日の夜、関西でテレビをつけた人の中には「はだかんぼうたちがやっていない」と驚いた人も多かったようです。
この日は、{mark("阪神タイガースが2年連続8回目のセ・リーグ優勝を決めた日", c)}でした。
2リーグ制になってから、阪神がリーグ連覇を果たすのは球団史上初めてのことです。
""")
    body += para("""
関西の放送局は優勝を受けて夜に特番を組み、テレビ朝日系のABCテレビでも23時台の番組が変更になりました。
そのため『はだかんぼうたち』の第1話は、関西地区では日付が変わった10月4日(日)の0時20分からの放送になっています。
公式Xも「関西地区の皆さまお待たせしました」と、0時20分からの放送を案内していました。
""")
    body += reactbox("関西のファンの声", ["関西は阪神やってる、遅れて放送なの？", "ド深夜に飛ばされた", "TVerでリアタイするもんっ"], c)
    body += para("""
関東などでは予定どおり23時から放送されたので、Xのトレンドでは阪神の優勝と『はだかんぼうたち』の感想が並ぶ珍しい光景になりました。
関西の方で放送を待てなかった人は、TVerのリアルタイム配信や見逃し配信で先に見ていたようです。
""")

    body += h2("TVerで見るときのポイント")
    body += minibox([("リアルタイム配信", "地上波と同じ時間に配信で見られる"), ("見逃し配信", "放送後から無料で見られる")], c)
    body += para("""
TVerでは、放送後の見逃し配信だけでなく、地上波と同じ時間に番組を流すリアルタイム配信が行われることもあります。
今回の第1話でも、関西に住んでいて放送が遅れたファンや、外出先にいたファンが、TVerのリアルタイム配信で23時から見ていたようです。
放送時間に家のテレビの前にいられない日も、スマートフォンがあれば同じタイミングで追いかけられるのは心強いですね。
""")
    body += para("""
見逃し配信は無料で見られる代わりに、途中でCMが入ります。
また、配信期間を過ぎると見られなくなるので、「あとで見よう」と思っている回は早めにチェックしておきましょう。
第1話の冒頭はかなり大胆なシーンから始まるので、家族と一緒の場所で見るときは少しだけ気をつけておくと安心かもしれません。
""")
    body += h3("見逃した人向けの第1話おさらい")
    body += para(f"""
第1話では、靴職人の鯖崎涼(松田元太さん)が、表参道で美しいパンプスを履いた歯科医・筒井桃(加藤ローサさん)に目を奪われます。
同じ日に店を訪れて結婚式用の靴を依頼した石羽拓(髙木雄也さん)こそが、桃の婚約者でした。
ラストでは、鯖崎が桃にキスをし、Travis Japanの主題歌「EGO」が流れて幕を閉じています。
『東京タワー』の浅野詩史(板谷由夏さん)がサプライズで登場したことも大きな話題になりました。
鯖崎がどんな人物なのかは、<a href="{SITE}/{slugs['sabazaki']}">鯖崎涼の役どころをまとめた記事</a>で詳しく紹介しています。
""")

    body += h2("はだかんぼうたちの放送地域は？")
    body += minibox([("放送", "テレビ朝日系列の各局")], c)
    body += para("""
『はだかんぼうたち』は、テレビ朝日の土曜夜11時のドラマ枠「オシドラサタデー」で放送されています。
テレビ朝日系列の各局で放送されますが、地域によってはスポーツ中継や特番で今回の関西のように時間が変わることがあります。
系列局のない地域に住んでいる方や、放送時間に間に合わない方は、TVerで見るのがいちばん確実です。
""")

    body += h2("はだかんぼうたち第2話はいつ？")
    body += minibox([("第2話", "2026年10月10日(土)23:00〜")], c)
    body += para(f"""
第2話は、2026年10月10日(土)の夜11時から放送されます。
第1話の放送後には公式Xで第2話の予告も公開されていて、鯖崎と桃、そして桃の親友・響子の関係がさらに動き出しそうです。
第1話の内容を振り返りたい方は<a href="{SITE}/{slugs['ep1']}">第1話のあらすじと反響をまとめた記事</a>を、主題歌や挿入歌が気になった方は<a href="{SITE}/{slugs['song']}">主題歌・挿入歌の曲名をまとめた記事</a>もあわせてどうぞ。
""")

    body += h2("まとめ")
    body += summary([
        "見逃し配信はTVerで無料、TELASAでも配信予定",
        "TVerの配信は次の話の放送までの約1週間が目安",
        "関西の第1話は阪神のリーグ連覇の特番により10月4日0:20〜に変更",
        "第2話は10月10日(土)23:00から放送",
    ], c)
    body += para("""
阪神の優勝と重なり、関西では少し待つことになった第1話ですが、TVerを使えばいつでも追いかけられます。
まだ見ていない方は、第2話の放送前にTVerでチェックしてみてください！
""")
    body += related("はだかんぼうたちの関連記事", article_links(slugs, "tver"), c)
    posts["tver"] = dict(
        title="はだかんぼうたちの見逃し配信はどこ？関西の放送時間も！",
        content=body, categories=[3], eyecatch="hadakanbou_tver_eyecatch.png",
        alt="はだかんぼうたちの見逃し配信と関西の放送時間を紹介する記事のアイキャッチ")

    # ============ 5. インスタライブ ============
    c = B
    body = para(f"""
『はだかんぼうたち』の初回放送直前の10月3日夜、主演の松田元太さんと共演の髙木雄也さん(Hey! Say! JUMP)が、2人でインスタライブを行いました。
ドラマでは恋敵の2人ですが、配信では{mark("東京タワーが見える場所から登場した松田さんの「自宅なんですよ」というボケに、髙木さんがすかさずツッコむ", c)}など、和やかなやりとりが話題になっています。
この記事では、インスタライブの内容と、放送前の2人の関係がわかるトークをまとめました。
""")
    body += infobox("初回放送直前スペシャルインスタライブ", [
        ("配信日", "2026年10月3日(土)"),
        ("時間", "22時台(22時から予定、2人のコラボは22時18分ごろから)"),
        ("出演", "松田元太・髙木雄也"),
        ("配信アカウント", "それぞれの公式Instagram"),
    ])
    body += learnbox(["インスタライブの配信時間", "インスタライブで話したこと", "2人の関係と共演の印象", "放送前のイベントでのトーク", "SNSの反応"], c)

    body += h2("インスタライブはいつ配信された？")
    body += minibox([("予定", "10月3日(土)22時から"), ("実際", "22時18分ごろから2人のコラボ配信")], c)
    body += para("""
テレビ朝日は放送前から、初回放送当日の夜10時ごろに2人がそれぞれのInstagramで「初回放送直前スペシャルインスタライブ」を行うと発表していました。
ファンの投稿によると、実際には22時18分ごろから松田さんと髙木さんのコラボ配信が始まり、22時50分ごろまで続いたようです。
放送開始の23時まであと少しというタイミングで、ドラマへの気持ちを一気に高めてくれる配信になりました。
""")

    body += h2("インスタライブで何を話した？")
    body += minibox([("松田さん", "東京タワーが見える場所から配信"), ("名場面", "「自宅なんですよ」→髙木さんがツッコミ")], c)
    body += h3("松田元太の「自宅なんですよ」に髙木雄也がツッコミ")
    body += para(f"""
松田さんは、背景に東京タワーが見える夜景のきれいな場所から配信していました。
それを見た髙木さんが「すっげーイイトコでインスタライブしてんじゃん」と声をかけると、松田さんは{mark("「自宅なんですよ」", c)}と返して、ひと笑い起きたそうです。
『東京タワー』に出演していた松田さんが、東京タワーを背にして配信していたのも、ファンにはうれしいポイントでした。
""")
    body += h3("髙木雄也はリラックスした姿で登場")
    body += para("""
一方の髙木さんは、自宅からとみられるリラックスした装いで配信に参加していました。
ドラマで演じる一途なエリートサラリーマン・石羽拓とはまったく違う素の雰囲気に、Hey! Say! JUMPのファンだけでなくTravis Japanのファンも反応していたようです。
放送直前ということもあり、2人とも第1話の見どころやドラマへの思いを話しながら、オンエアに向けてファンと一緒に盛り上がっていました。
""")
    body += reactbox("Xでの反応", ["インスタライブめっちゃイケメンだった", "ドラマも最高だった", "楽しみしかなくてドキドキが止まらない"], c)

    body += h2("松田元太と髙木雄也の関係は？")
    body += minibox([("事務所", "同じ事務所の先輩(髙木)と後輩(松田)"), ("ドラマ", "今回が初共演で、役柄は恋敵")], c)
    body += para(f"""
松田さんと髙木さんは、同じ事務所の先輩と後輩にあたります。
ドラマでの共演は今回が初めてで、劇中では桃をめぐってヒリヒリした関係になりますが、撮影現場では常に和気あいあいとしているそうです。
""")
    body += I("order")
    body += para(f"""
公式Xで公開されたスペシャルトークでは、お互いの印象を聞かれ、髙木さんが松田さんについて{mark("「魅せ方が上手だし、かっこいいし色気もある人」", c)}と話していました。
一方の松田さんは、髙木さんについて「はずかしがり屋さんですか？」と質問を投げかけていて、2人の距離感の近さが伝わってきます。
""")

    body += h2("インスタライブのアーカイブは見られる？")
    body += minibox([("アーカイブ", "残すかどうかは配信した本人のアカウント次第")], c)
    body += para("""
Instagramのライブ配信は、配信した本人がアーカイブとして残すかどうかを選べる仕組みになっています。
今回の配信がアーカイブとして公開されているかどうかは、松田元太さんと髙木雄也さんそれぞれのInstagramで確認するのが確実です。
リアルタイムで見られなかった方は、まずは2人のアカウントのリール欄やストーリーズを確認してみてください。
""")
    body += para("""
なお、Xではインスタライブの録画を配布するといった投稿も見かけますが、こうした転載は権利者の許可を得ていないものがほとんどです。
公式に公開されている範囲で楽しむのが、2人を応援するうえでもいちばん安心でしょう。
""")
    body += h3("ドラマ公式のSNSでも2人のトークが見られる")
    body += para(f"""
インスタライブを見逃した方には、ドラマ公式Xで公開されているスペシャルトーク動画もおすすめです。
part1ではお互いの印象を語り合っていて、インスタライブと同じく、ドラマとは正反対の和やかな2人の姿が見られます。
第1話の内容や反響が気になる方は、<a href="{SITE}/{slugs['ep1']}">第1話のあらすじとSNSの反響をまとめた記事</a>もチェックしてみてください。
""")

    body += h2("放送前のイベントでも息の合ったトーク")
    body += minibox([("9月26日", "ガールズアワードにサプライズ出演"), ("9月28日", "制作発表記者会見")], c)
    body += para("""
2人は放送前のイベントでも、何度も一緒に登場していました。
9月26日には千葉・幕張メッセで行われた「Rakuten GirlsAward 2026 AUTUMN/WINTER」に、キャストとしてサプライズで登場しています。
""")
    body += para(f"""
9月28日の制作発表記者会見では、松田さんがジャケットの胸元を見せて「はだかんぼうたちです！」とボケて会場を沸かせました。
撮影の様子を聞かれた松田さんが「楽しく、楽しく撮影しています」と答えると、髙木さんが「それ、何の“ですね”なの？」とツッコむ場面もあり、先輩・後輩の掛け合いが印象的でした。
「好きな人をどう落とす？」という二択の質問では、松田さんが「好きになったら『好きです』って言うかな」とストレートな答え。
髙木さんは「落とすっていう考えがあまりない」と大人の回答をし、松田さんが{mark("「かっこいい。ドラマチック」", c)}と絶賛していました。
""")

    body += h2("まとめ")
    body += summary([
        "初回放送直前の10月3日22時台に、2人でインスタライブを配信",
        "松田は東京タワーが見える場所から登場し「自宅なんですよ」とボケた",
        "髙木はリラックスした素の姿で参加し、ファンの間で話題に",
        "2人は同じ事務所の先輩・後輩で、今回が初共演",
        "制作発表でも髙木が松田にツッコむ息の合った掛け合いを見せた",
    ], c)
    body += para("""
ドラマでは恋敵として火花を散らす2人ですが、カメラの外では仲のいい先輩と後輩の関係です。
今後も番宣などで2人が並ぶ機会があれば、ドラマとのギャップを楽しみながら見てみてください！
""")
    body += related("はだかんぼうたちの関連記事", article_links(slugs, "live"), c)
    posts["live"] = dict(
        title="松田元太と髙木雄也のインスタライブで何話した？内容まとめ！",
        content=body, categories=[3, 4], eyecatch="hadakanbou_instalive_eyecatch.png",
        alt="松田元太と髙木雄也のインスタライブの内容を紹介する記事のアイキャッチ")
    return posts


SLUGS = {
    "ep1": "hadakanboutachi-ep1-reaction",
    "song": "hadakanboutachi-theme-song-ego",
    "sabazaki": "sabazaki-ryo-genta-matsuda-role",
    "tver": "hadakanboutachi-tver-kansai-time",
    "live": "genta-matsuda-yuya-takaki-instagram-live",
}


def plain_len(s):
    return len(re.sub(r"<[^>]+>|\s", "", s))


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    if dry:
        fake = {"media_details": {"sizes": {"large": {"source_url": "x", "width": 1, "height": 1}}, "width": 1, "height": 1}, "source_url": "x"}
        posts = build({k: fake for k in IMAGES}, SLUGS)
        for k, p in posts.items():
            print(k, len(p["title"]), p["title"], "chars:", plain_len(p["content"]))
        sys.exit(0)

    print("uploading images...")
    M = {}
    for k, (src, name, alt, _) in IMAGES.items():
        M[k] = upload_media(IMG_DIR / src, name, alt)
        print(" ", k, M[k]["id"])
    posts = build(M, SLUGS)
    ids = {}
    for k, p in posts.items():
        ec = upload_media(ROOT / "images" / p["eyecatch"], p["eyecatch"], p["alt"])
        r = api("posts", {"title": p["title"], "content": p["content"], "slug": SLUGS[k], "status": "draft",
                          "categories": p["categories"], "author": AUTHOR_ID, "featured_media": ec["id"]})
        ids[k] = {"id": r["id"], "eyecatch": ec["id"], "slug": r.get("slug") or SLUGS[k]}
        print("CREATED", k, r["id"], "eyecatch", ec["id"])
    IDS_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(ids, ensure_ascii=False))
