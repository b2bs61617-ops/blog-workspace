# -*- coding: utf-8 -*-
import json, base64, os, re, urllib.request, urllib.parse
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
            env[k.strip()] = v.strip().strip('"')
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_AUDITION_URL"].rstrip("/")
WP_USER = ENV["WP_AUDITION_USERNAME"]
WP_PASS = ENV["WP_AUDITION_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}


def upload_media(filepath: Path, filename: str, content_type: str):
    data = filepath.read_bytes()
    headers = {
        **HEADERS_AUTH,
        "Content-Type": content_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=data)
    r.raise_for_status()
    return r.json()


# ---------- block helpers (same green palette as ep7 = Nakamura Kaito member color) ----------
BORDER = "#cfe6d4"
ACCENT = "#66bb6a"
BG = "#f3f8f4"
BARBG = "#4a9c5d"
NAMECOL = "#3f8b52"


def p(sentences, extra_class=""):
    body = "<br>\n".join(sentences)
    cls = f' class="{extra_class}"' if extra_class else ""
    return f"<!-- wp:paragraph -->\n<p{cls}>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def infobox(title, rows):
    trs = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;width:32%;"><strong>{k}</strong></td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(
        f'<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>\n'
        f'<table style="border-collapse:collapse;width:100%;"><tbody>\n{trs}\n</tbody></table>\n</div>'
    )


def whatbox(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(
        f'<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{BARBG};color:#fff;">この記事でわかること</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">\n{lis}\n</ul>\n</div>'
    )


def minibox(rows):
    lines = "\n".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
        for i, (k, v) in enumerate(rows)
    )
    return wphtml(
        f'<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;'
        f'padding:10px 16px;margin:0 0 16px 0;background:{BG};">\n{lines}\n</div>'
    )


def personbox(name, sentences):
    body = "<br>\n".join(sentences)
    return wphtml(
        f'<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;color:{NAMECOL};">{name}</p>\n'
        f'{body}\n</div>'
    )


def image_block(src, w, h, srcset, alt, caption):
    return wphtml(
        f'<figure class="wp-block-image size-large">\n'
        f'<img src="{src}" alt="{alt}" width="{w}" height="{h}"\n'
        f'  style="max-width:100%;height:auto;"\n'
        f'  srcset="{srcset}"\n'
        f'  sizes="(max-width: {w}px) 100vw, {w}px">\n'
        f'<figcaption style="font-size:0.8em;color:#888;">出典:{caption}</figcaption>\n</figure>'
    )


def img_urls(media):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    full_w = media["media_details"]["width"]
    full_h = media["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    img_src = large["source_url"]
    img_w = large["width"]
    img_h = int(img_w * full_h / full_w)
    srcset = (
        f'{medium["source_url"]} {medium["width"]}w, '
        f'{large["source_url"]} {large["width"]}w, {full_url} {full_w}w'
    )
    return img_src, img_w, img_h, srcset


def gmap(q):
    return wphtml(
        f'<iframe\n  src="https://maps.google.com/maps?q={urllib.parse.quote(q)}&t=&z=14&ie=UTF8&iwloc=&output=embed"\n'
        f'  width="100%" height="350" frameborder="0" scrolling="no"\n  style="border:0;" loading="lazy">\n</iframe>'
    )


def sumbox(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(
        f'<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>'
    )


def linkbox(title, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(
        f'<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;'
        f'margin:0 0 16px 0;padding:14px 18px;background:{BG};">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>'
    )


# ---------- images (frames from the OFFICIAL Travis Japan YouTube channel's "chira-mise" teaser clip) ----------
YT_CHIRAMI8 = "https://youtu.be/YTirIoaWHIY"

img_defs = [
    ("shark", "ishigaki8_hammerhead_shark.jpg", "travis_japan_shinnihonisan_ishigaki8_hammerhead_shark.jpg",
     "水面近くで暴れるハンマーヘッドシャーク。テロップに「かかったのはハンマーヘッドシャーク!」", YT_CHIRAMI8),
    ("hanseikai", "ishigaki8_hanseikai_3shot.jpg", "travis_japan_shinnihonisan_ishigaki8_hanseikai_3shot.jpg",
     "フサキビーチリゾートの客室で行われた1日目の反省会。中村海人と、テロップで「上野P」と紹介されたスタッフ、もう1人のスタッフの3人", YT_CHIRAMI8),
    ("dinner", "ishigaki8_dinner_gazami.jpg", "travis_japan_shinnihonisan_ishigaki8_dinner_gazami.jpg",
     "総料理長の伊藤穣さんが「ガザミの大きいやつ」ことノコギリガザミを運んでくる場面。テーブルには麻婆豆腐や石垣牛も並ぶ", YT_CHIRAMI8),
]
IMG = {}
for key, localname, upname, alt, src in img_defs:
    m = upload_media(ROOT / "images" / localname, upname, "image/jpeg")
    iu = img_urls(m)
    IMG[key] = image_block(iu[0], iu[1], iu[2], iu[3], alt, src)
    print(f"{key} media id:", m["id"])

# ---------- content ----------
title = "石垣島カジキ釣り完結編！結末とヒットの正体は？"

blocks = []

blocks.append(p([
    "2026年9月9日深夜(日付上は10日)に配信された「Travis JapanノJUST!シン日本遺産」石垣島カジキ釣り特別編の完結編(#8)は、中村海人がひとりで挑んだカジキ釣りに決着がつく回でした。",
    "結論から言うと、前編ラストでヒットしていた大物の正体は<strong>ハンマーヘッドシャーク</strong>で、引き寄せた直後に糸が切れて取り込めず終わっています。",
    "そして肝心のカジキも、2日目の制限時間いっぱいまで粘ったものの<strong>ヒットせず、今回は釣れないまま完結</strong>という結果に終わりました。",
    "この記事では、大物の正体・ホテルでの反省会で起きた\"みにくい争い\"・夕食のご当地グルメ・2日目本番の結末までを、放送された映像をもとに順番に紹介していきます。",
]))

blocks.append(p([
    "前編(#7)では、石垣島「フサキビーチリゾート ホテル＆ヴィラズ」からロケがスタートし、釣り船「fishing reef 紗虹丸」でパヤオへ向かった中村が、ジギングでヒットさせた獲物をサメ(ツマジロ)に食べられて熱中症でダウン。",
    "体力を回復させたあとキハダマグロを生き餌にしてカジキ本番に挑むも、「続きは次回!」のテロップで前編が終わっていました。",
    "前編の詳しいロケ地・釣り船・船長の情報は、<a href=\"https://chomoand-0.com/shinnihonisan-ishigaki-kajiki\" target=\"_blank\" rel=\"noopener\">シン日本遺産の石垣島ロケ地は?中村海人の釣り船を特定!</a>で先にまとめています。",
]))

blocks.append(infobox("番組情報", [
    ("番組タイトル", "Travis JapanノJUST!シン日本遺産 特別編 カジキ釣り in 石垣島(完結編・#8)"),
    ("放送・配信", "2026年9月9日(水)深夜〜10日(木)未明とみられる。ABCテレビ系列、TVerで見逃し配信。TELASAではスタジオ企画を加えた特別版を独占配信"),
    ("出演", "中村海人(ロケ)、Travis Japan(スタジオ)"),
    ("企画内容", "前編(#7)から続く中村海人単独ロケの完結編。カジキ釣り1日目終盤〜2日目の決着までを描く"),
]))

blocks.append(whatbox([
    "前編ラストでヒットした大物の正体",
    "カジキ釣りの最終的な結末",
    "ホテルでの反省会で起きた\"みにくい争い\"",
    "夕食で堪能したご当地グルメ",
    "2日目本番の展開",
]))

blocks.append(h2("大物の正体はまさかのハンマーヘッドシャークだった"))
blocks.append(minibox([
    ("正体", "ハンマーヘッドシャーク(シュモクザメの仲間)"),
    ("結末", "水面まで引き寄せた直後に糸が切れて取り込めず"),
]))
blocks.append(p([
    "1日目の残り時間20分、カジキ用の竿に何かがHITした場面から放送は再開しました。",
    "「魚います」と中村が声を上げ、慎重にリールを巻き続けると、水面に姿を見せたのはカジキではなく<strong>ハンマーヘッドシャーク</strong>。",
    "頭部が横に張り出した独特の姿が画面に大きく映り、テロップでも「かかったのはハンマーヘッドシャーク!」とはっきり示されていました。",
]))
blocks.append(IMG["shark"])
blocks.append(p([
    "せっかく水面近くまで寄せたものの、その直後に「切れた」のテロップとともに糸が切断され、ハンマーヘッドシャークは海へ帰っていきました。",
    "結果としてこの日は取り込みまでは至らず、サメとの遭遇はここで終了。",
    "番組内では「サメで始まってサメで終わりましたね」という一言もあり、1日目は前編のツマジロ、後編のハンマーヘッドシャークと、サメに始まりサメで幕を閉じる展開になったことが振り返られていました。",
]))
blocks.append(p([
    "肝心のカジキは1日目には姿を見せず、この時点で「1日目終了」のテロップとともにロケは一区切り。",
    "中村たちは船を降り、宿泊先のフサキビーチリゾートへと戻っていきました。",
]))

blocks.append(h2("ホテルでの「反省会」で起きたスタッフの言い争いとは"))
blocks.append(minibox([
    ("場所", "フサキビーチリゾートの客室"),
    ("参加者", "中村海人＋スタッフ2人(うち1人はテロップで「上野P」と紹介)"),
    ("内容", "船酔いを巡るやり取りから\"みにくい争い\"に発展"),
]))
blocks.append(p([
    "客室に戻った中村は、マリンアクティビティやスパで癒やされたあと、「1日目の反省会を開く」というテロップとともにスタッフ2人と合流します。",
    "画面には中村を挟んで2人のスタッフが座り、そのうち1人は「上野P」というテロップ付きで紹介されていました。",
]))
blocks.append(IMG["hanseikai"])
blocks.append(p([
    "話題に上がったのは、この日の船上で「ずっと船酔い」だったというスタッフの様子。",
    "それをからかうように「ヘタレですね」という言葉が飛び、からかわれた側が「すみませんでした」と繰り返し謝る一幕もありました。",
    "その後、船酔いを巡るやり取りは次第にヒートアップし、画面には<strong><span class=\"swl-marker mark_green\" style=\"font-size:1.15em;\">みにくい争い</span></strong>というテロップが表示される展開に。",
    "とはいえ3人とも終始笑いながらのやり取りで、深刻な喧嘩というより、船酔いのお詫びを巡るコミカルな\"言い合い\"として描かれていました。",
]))

blocks.append(h2("夕食で堪能した石垣島グルメの数々"))
blocks.append(minibox([
    ("会場", "フサキビーチリゾート内レストラン(1日目の夕食)"),
    ("料理", "ノコギリガザミのブラックペッパー炒め、島豆腐と葉ニンニクの四川麻婆豆腐、石垣牛など"),
    ("総料理長", "伊藤穣さん"),
]))
blocks.append(p([
    "反省会のあとは、そのままホテル内のレストランで食事会に移りました。",
    "出迎えたのはテロップで「総料理長 伊藤穣さん」と紹介されたシェフで、まず運ばれてきたのが「ガザミの大きいやつ」ことノコギリガザミ。",
    "小浜島で獲れたという大ぶりの一杯で、ブラックペッパーを効かせた炒め物として提供されていました。",
]))
blocks.append(IMG["dinner"])
blocks.append(p([
    "テーブルにはほかにも、島豆腐と葉ニンニクを使った四川麻婆豆腐や、ジューシー(沖縄風の炊き込みご飯)、石垣牛の一皿などが並び、中村たちは「うんめぇ〜」を連発しながら舌鼓を打っていました。",
    "麻婆豆腐は見た目以上に辛かったようで、「あぁ辛っ!」という声も上がっていたのが印象的でした。",
]))
blocks.append(p([
    "なお2日目の昼は、待ち時間に釣り上げたカツオを船上でその場で刺身にして味わう場面もありました。",
    "石垣の人は酢を入れて食べるという豆知識も紹介され、「超新鮮なカツオの刺身」に中村は「うんめぇ〜」と大満足の様子でした。",
]))

blocks.append(h2("2日目のカジキ釣り本番、結末はどうなった?"))
blocks.append(minibox([
    ("スケジュール", "6:00出船〜8:00パヤオ着・カジキ釣り〜13:00終了〜17:00ロケ終了"),
    ("結果", "制限時間までカジキはヒットせず、今回は釣れないまま完結"),
]))
blocks.append(p([
    "最終日は「カジキ釣り最終日」のテロップとともに、中村が朝日に手を合わせるシーンからスタート。",
    "船上に掲げられた「2日目のスケジュール」のボードには、6:00出船・8:00パヤオ着からカジキ釣り開始・13:00終了・15:00帰港・17:00ロケ終了という工程が示されていました。",
]))
blocks.append(p([
    "カジキ釣りの生き餌を確保するため、まずは電動リールを使ってキハダマグロ狙いに挑戦し、115cm・18kgという立派なキハダマグロを釣り上げます。",
    "ここで中村は「このキハダマグロを持ち帰って食べるか、これを生き餌にしてカジキを狙うか」という選択を迫られますが、「夢を追いましょう」の一言でカジキ挑戦の続行を選択。",
    "大きな夢を諦めない姿勢に、放送直後のXでも「カッコ良すぎる」「諦めない気持ちが素晴らしい」といった声が多く見られました。",
]))
blocks.append(p([
    "本番では鳥が集まる場所や、プランクトンが発生しやすい潮目を狙うなど、船長のアドバイスを受けながら粘り強く探索を続けました。",
    "しかし午後2時、「TIME UP」のテロップとともにタイムリミットが到来し、この特別編でカジキがヒットすることはありませんでした。",
]))
blocks.append(p([
    "夢が叶わなかった中村に対し、スタッフは「また帰ってくればいい」と声をかけ、中村自身も「もちろんです!またリベンジでやりましょうか」と前向きにリベンジを宣言。",
    "英語字幕でも「A life-or-death battle with a giant marlin.(巨大カジキとの死闘)」「Though, to be honest, I will definitely get my revenge.(正直に言うと、絶対にリベンジします)」という中村の言葉が紹介され、後日のリベンジ企画を予感させる形でこの特別編は幕を閉じました。",
]))

blocks.append(h2("まとめ"))
blocks.append(sumbox([
    "前編ラストでヒットした大物の正体は<strong>ハンマーヘッドシャーク</strong>で、水面まで引き寄せた直後に糸が切れて取り込めず",
    "1日目は前編のツマジロ・後編のハンマーヘッドシャークと、\"サメに始まりサメで終わる\"展開に",
    "ホテルの反省会では、船酔いを巡るスタッフ同士のやり取りが<strong>\"みにくい争い\"</strong>としてコミカルに描かれた",
    "夕食はノコギリガザミや石垣牛など地元グルメを堪能(総料理長:伊藤穣さん)",
    "2日目のカジキ釣り本番はTIME UPまでヒットなく、今回は<strong>釣れないまま完結</strong>。中村海人は「またリベンジ」を宣言",
]))
blocks.append(p([
    "公式な後日談の発表はまだありませんが、「また帰ってくればいい」というスタッフの言葉や本人のリベンジ宣言からすると、いずれ続編企画が組まれる可能性はありそうです。",
    "初挑戦であそこまでカジキに肉薄した中村海人だからこそ、次こそは念願の一匹を釣り上げる瞬間を見てみたいですね!",
]))
blocks.append(linkbox("Travis Japanのロケ地・釣り関連記事", [
    '<a href="https://chomoand-0.com/shinnihonisan-ishigaki-kajiki" target="_blank" rel="noopener">シン日本遺産の石垣島ロケ地は?中村海人の釣り船を特定!(前編)</a>',
    '<a href="https://chomoand-0.com/is-travis-japans-fishing-pond" target="_blank" rel="noopener">Travis Japanの釣り堀ロケ地は武蔵野園?食べたメニューも紹介</a>',
    '<a href="https://chomoand-0.com/just-where-is-the-sendai-filmi" target="_blank" rel="noopener">JUST!シン日本遺産の仙台ロケ地はどこ?屋台飯も紹介</a>',
]))

content = "\n\n".join(blocks)

# ---------- eyecatch ----------
eyecatch = upload_media(
    ROOT / "images" / "travis_japan_shinnihonisan_ishigaki8_kajiki_kanketsu_eyecatch.png",
    "travis_japan_shinnihonisan_ishigaki8_kajiki_kanketsu_eyecatch.png",
    "image/png",
)
print("EYECATCH media id:", eyecatch["id"])

# ---------- create new draft post ----------
payload = {
    "title": title,
    "slug": "shinnihonisan-ishigaki-kajiki-kanketsu",
    "content": content,
    "status": "draft",
    "categories": [3, 7],
    "author": 1,
    "featured_media": eyecatch["id"],
}
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("POST_ID", post["id"])
print("SLUG", post["slug"])
print("STATUS", post["status"])
print("PREVIEW", f"{WP_URL}/?p={post['id']}")
