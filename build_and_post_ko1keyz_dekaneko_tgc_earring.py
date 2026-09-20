# -*- coding: utf-8 -*-
"""KO1KEYZ「デカ猫」(DAIKI×YOSHIKI)がマイナビTGC 2026 A/W(2026-09-19)で着けていた
似たデザインのピアスについての記事。chomoand-1.com に JP/KR/EN の下書きを投稿し、アイキャッチを設定する。

画像は公式X(@KO1KEYZofficial)の公演後写真から自前で拡大・合成したもの(ファン投稿の画像は使わない)。
"""
import base64, json, os, re, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

import requests
from PIL import Image

ROOT = Path(__file__).parent
WORK = ROOT / "images" / "daiki-yoshiki-cat-piercing"


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = {**load_env(ROOT / ".env"), **os.environ}
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f'{ENV["WP_KOIKEYS_USERNAME"]}:{ENV["WP_KOIKEYS_APP_PASSWORD"]}'.encode()).decode()
HA = {"Authorization": f"Basic {AUTH}"}
H = {**HA, "Content-Type": "application/json"}

DAIKI_SRC = "https://x.com/KO1KEYZofficial/status/2101273598182990087"
YOSHIKI_SRC = "https://x.com/KO1KEYZofficial/status/2101274729734971751"

# 装飾色: rules.md「UIボックスのアクセントカラーはメンバーカラーと被らせない」→ウォームグレー
AB, AL, BG = "#ddd9d3", "#8a8378", "#f7f6f4"

# ---------------- 画像の合成・アップロード ----------------
daiki = Image.open(WORK / "xiy_daiki_official" / "images" / "post_1_img_1.jpg").convert("RGB")
yoshiki = Image.open(WORK / "xiy_status" / "images" / "post_3_img_1.jpg").convert("RGB")


def to_height(im, h):
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


a, b = to_height(daiki, 1200), to_height(yoshiki, 1200)
pair = Image.new("RGB", (a.width + b.width + 8, 1200), (255, 255, 255))
pair.paste(a, (0, 0))
pair.paste(b, (a.width + 8, 0))
PAIR_PATH = WORK / "official_pair_tgc.jpg"
pair.save(PAIR_PATH, quality=88)

z1 = Image.open(WORK / "daiki_earring_zoom.jpg").convert("RGB").resize((800, 800), Image.LANCZOS)
z2 = Image.open(WORK / "yoshiki_earring_zoom.jpg").convert("RGB").resize((800, 800), Image.LANCZOS)
zoom = Image.new("RGB", (1608, 800), (255, 255, 255))
zoom.paste(z1, (0, 0))
zoom.paste(z2, (808, 0))
ZOOM_PATH = WORK / "earring_zoom_pair.jpg"
zoom.save(ZOOM_PATH, quality=90)


def upload_media(path, filename, alt, mime="image/jpeg"):
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HA, "Content-Type": mime, "Content-Disposition": f'attachment; filename="{filename}"'},
        data=path.read_bytes(),
    )
    r.raise_for_status()
    m = r.json()
    requests.post(f"{WP_URL}/wp-json/wp/v2/media/{m['id']}", headers=H,
                  data=json.dumps({"alt_text": alt, "title": alt}).encode("utf-8")).raise_for_status()
    return m


pair_media = upload_media(PAIR_PATH, "ko1keyz_daiki_yoshiki_tgc_official_pair.jpg",
                          "マイナビTGC 2026 A/W後の公式写真。デニムジャケット姿のDAIKIとストライプシャツ姿のYOSHIKI")
zoom_media = upload_media(ZOOM_PATH, "ko1keyz_daiki_yoshiki_earring_zoom.jpg",
                          "DAIKIとYOSHIKIの耳元のピアスを拡大して並べた画像")
print("pair", pair_media["id"], "zoom", zoom_media["id"])


def img_html(media, alt, caption):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    fw, fh = media["media_details"]["width"], media["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": fw})
    medium = sizes.get("medium", {"source_url": full_url, "width": fw})
    iw = large["width"]
    ih = int(iw * fh / fw)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {fw}w'
    return (f'<!-- wp:html -->\n<figure class="wp-block-image size-large">\n'
            f'<img src="{large["source_url"]}" alt="{alt}" width="{iw}" height="{ih}"\n'
            f'  style="max-width:100%;height:auto;"\n  srcset="{srcset}"\n'
            f'  sizes="(max-width: {iw}px) 100vw, {iw}px">\n'
            f'<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>\n</figure>\n<!-- /wp:html -->')


def src_links(prefix, d="DAIKI", y="YOSHIKI"):
    return (f'{prefix}<a href="{DAIKI_SRC}" target="_blank" rel="noopener">@KO1KEYZofficial(X)の{d}投稿</a>・'
            f'<a href="{YOSHIKI_SRC}" target="_blank" rel="noopener">{y}投稿</a>')


def check(text):
    return (f'<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};'
            f'border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{text}</p>')


def checks(items):
    body = "\n".join(check(t) for t in items)
    return (f'<!-- wp:html -->\n<div style="border:1px solid {AB};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">\n{body}\n</div>\n<!-- /wp:html -->')


def titled_list(title, items):
    lis = "\n".join(f"<li>{t}</li>" for t in items)
    return (f'<!-- wp:html -->\n<div style="border:1px solid {AB};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
            f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AL};color:#fff;">{title}</p>\n'
            f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">\n{lis}\n</ul>\n</div>\n<!-- /wp:html -->')


def point_box(label, text):
    return (f'<!-- wp:html -->\n<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">\n'
            f'<p style="margin:0;"><strong>{label}</strong>{text}</p>\n</div>\n<!-- /wp:html -->')


def related_box(title, links):
    lis = "\n".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for u, t in links)
    return (f'<!-- wp:html -->\n<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">\n'
            f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>\n<!-- /wp:html -->')


def table(rows):
    td = f'border:1px solid {AB};padding:8px 10px;vertical-align:top;'
    trs = []
    for i, row in enumerate(rows):
        bg = f"background:{BG};font-weight:bold;" if i == 0 else ""
        trs.append("<tr>" + "".join(f'<td style="{td}{bg}">{c}</td>' for c in row) + "</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            + "".join(trs) + '</tbody></table></figure>\n<!-- /wp:table -->')


def p(text):
    return f"<!-- wp:paragraph -->\n<p>{text}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


# ================= JAPANESE =================
JP_TITLE = "デカ猫のピアスはお揃い？DAIKIとYOSHIKIがTGCで着用"
JP_FALLBACK_SLUG = "ko1keyz-dekaneko-tgc-matching-earrings"

jp_pair = img_html(pair_media, "マイナビTGC 2026 A/W後の公式写真。デニムジャケット姿のDAIKIとストライプシャツ姿のYOSHIKI",
                   src_links("出典:", "DAIKI", "YOSHIKI"))
jp_zoom = img_html(zoom_media, "DAIKIとYOSHIKIの耳元のピアスを拡大して並べた画像",
                   "左:DAIKI、右:YOSHIKI(上の公式写真を拡大)")

JP_CONTENT = "\n\n".join([
    p("2026年9月19日、横浜アリーナで開かれた「マイナビ TGC 2026 A/W」に初出演したKO1KEYZ(コイキーズ)。<br>"
      "公演後に公式Xが1人ずつ投稿した写真を見返すと、ファンの間でケミ名「デカ猫」と呼ばれているDAIKI(加藤大樹)さんとYOSHIKI(矢田佳暉)さんが、よく似たキラキラのピアスを着けていることに気づきます。<br>"
      "結論から言うと、2人とも<strong>中央に大きめの石、そのまわりに小粒の石をぐるりと並べた「花(ヘイロー)型」のゴールド系ピアス</strong>に見えますが、ブランド名や商品名は公式には明かされておらず、現時点では特定できていません。<br>"
      "この記事では、公式写真をもとに2人の耳元を拡大して見比べ、「本当にお揃いなのか」「どこのピアスなのか」を整理していきます。"),
    titled_list("この記事でわかること", [
        "2人が9/19のTGCで着けていたピアスの見た目",
        "拡大して並べるとどこが似ていて、どこが違うのか",
        "ブランド・商品名は分かっているのか",
        "「両耳お揃い」「1つずつ分けっこ」の可能性はあるのか",
        "デカ猫と「Neko」、そしてTGCの意外な関係",
    ]),
    h2("9/19のTGCで何があった？KO1KEYZ初のファッションイベント出演"),
    point_box("イベント概要:", "「マイナビ TGC 2026 A/W」2026年9月19日(土)・横浜アリーナ。KO1KEYZは10月7日のデビュー前に初出演し、デニム衣装で「新世界(SHINSEKAI)-KO1KEYZ ver.-」「Neko(ねこ)-KO1KEYZ TGC ver.-」「KO1KEYZ」の3曲を披露した"),
    p("KO1KEYZにとって、TGCは国内の大型ファッションイベントへの初出演の舞台でした。<br>"
      "披露されたのは、「新世界(SHINSEKAI)」のKO1KEYZ ver.、オーディション番組『PRODUCE 101 JAPAN 新世界』のコンセプト評価曲として知られる「Neko」のTGC特別バージョン、そしてデビュー曲「KO1KEYZ」の3曲です。<br>"
      "配信の視聴方法などは<a href=\"https://chomoand-1.com/ko1keyz-mynavi-tgc-live-stream-12280\" target=\"_blank\" rel=\"noopener\">KO1KEYZのマイナビTGC生中継について調べた記事</a>で紹介しています。<br>"
      "ステージ後、公式Xはメンバー1人ずつの写真を続けて投稿しました。今回の話題の元になっているのが、その中のDAIKIさんとYOSHIKIさんの2枚です。"),
    h2("公式写真で確認できる2人の耳元"),
    jp_pair,
    p("DAIKIさんは褪せた色合いのデニムジャケット姿で、両手を胸の前で交差させたポーズ。指には細身のゴールドリングが複数重なり、耳元には向かって左の耳にキラリと光るピアスが見えます。<br>"
      "YOSHIKIさんはピンクの髪にブルーストライプのシャツ姿で、握りこぶしを頬に添えたポーズ。向かって右の耳にピアスが光り、指にはシルバー系の指輪を着けています。<br>"
      "衣装もポーズも違う2枚ですが、耳元の輝き方がとてもよく似ているのが、今回気になったポイントです。"),
    h2("ピアスを拡大して比べてみた"),
    jp_zoom,
    p("公式写真の原寸画像から、それぞれの耳元だけを切り出して並べたのが上の画像です。<br>"
      "小さなパーツなので細部までは読み取れませんが、見える範囲で特徴を整理すると次のようになります。"),
    table([
        ["項目", "DAIKI", "YOSHIKI"],
        ["見えている耳", "向かって左の耳", "向かって右の耳"],
        ["全体の形", "丸みのあるオーバル(楕円)型", "花のように花弁が広がる丸型"],
        ["石の配置", "中央にやや大きめの石、まわりに小粒の石を一周", "中央に大きめの石、まわりに小粒の石を一周"],
        ["色味", "透明〜シャンパン系の石とゴールド系の台座", "透明の石とゴールド系の台座"],
        ["耳たぶの下", "台座以外のパーツは確認できない", "ゴールドの細いリング状パーツが見える(フープ型の可能性)"],
        ["ほかのアクセ", "ゴールドの指輪を両手に複数", "シルバー系の指輪を1つ"],
    ]),
    p("共通しているのは、「中央の主役の石」+「小粒の石のふち取り」+「ゴールド系の台座」という組み立てです。<br>"
      "ただ、DAIKIさんのものはやや平たく丸いシルエット、YOSHIKIさんのものは花びらが外へ広がるような立体感があり、写真の解像度と角度の違いを差し引いても、<strong>完全に同じ商品だと言い切れるほどの一致は確認できません</strong>。<br>"
      "「同じブランドの色違い・サイズ違い」「同じシリーズの別モデル」「まったく別のピアスがたまたま似ていた」のいずれも、写真だけでは否定できない状態です。"),
    h2("ブランドや商品名は分かっている？"),
    point_box("現時点の結論:", "公式からブランド名・商品名の発表はなく、特定できていない。断定は避け、続報があれば追記する"),
    p("ブランドについては、公式Xの投稿文にも、TGC関連の公開情報にも、アクセサリーの提供元やスタイリング協力先の記載は見つかりませんでした。<br>"
      "TGCは全メンバーがデニム衣装で統一されていたステージだったため、耳元や指のアクセサリーも、衣装と合わせてスタイリストが用意したものだった可能性があります。<br>"
      "一方で、DAIKIさんは左右2つずつピアスホールがあり、日頃からアクセサリーを楽しんでいるメンバーでもあるため、ご本人の私物である可能性も十分考えられます。<br>"
      "どちらなのかを判断できる材料が今のところないため、「衣装の一部か私物か」も含めて不明、というのが正直なところです。<br>"
      "似た雰囲気のアイテムを探す場合は、「フラワー」「ハロー(ヘイロー)」「クラスター」「ジルコニア」「ゴールド」「スタッド」「ミニフープ」といったキーワードで探すと、デザインの近い商品が見つかりやすいでしょう。<br>"
      "ただし、あくまで見た目が近いだけで、本人着用品と同じとは限らない点にはご注意ください。"),
    h2("両耳お揃い？それとも1つずつの「分けっこ」？"),
    p("もう1つ気になるのが、写真に写っている耳の向きです。<br>"
      "DAIKIさんは向かって左の耳、YOSHIKIさんは向かって右の耳と、<strong>見えているのが左右逆の耳</strong>になっています。<br>"
      "ここから「同じペアのピアスを片耳ずつ着けているのでは？」「両耳とも同じデザインなのでは？」という見方も出てきますが、反対側の耳は確認が難しいのが実情です。<br>"
      "DAIKIさんの反対側の耳には、ごく小さな光がわずかに写っているものの、形までは判別できません。<br>"
      "YOSHIKIさんの反対側の耳は、髪に隠れていて写っていません。<br>"
      "なお、以前まとめた<a href=\"https://chomoand-1.com/how-many-piercings-do-ko1keyz-12030\" target=\"_blank\" rel=\"noopener\">KO1KEYZメンバーのピアスの数の記事</a>では、DAIKIさんは左右2つずつの計4つ、YOSHIKIさんは左右1つずつの計2つと整理しています。<br>"
      "もしYOSHIKIさんが両耳に着けていたとしても、ホールの数は左右1つずつなので、見た目の上では矛盾しません。<br>"
      "つまり「片耳ずつ分けている」可能性も「両耳お揃い」の可能性も、どちらも成り立つ状況で、今の写真だけでは決め手に欠けます。"),
    checks([
        "2人とも、中央の石+小粒の石のふち取り+ゴールド系の台座という、よく似た組み立てのピアスに見える",
        "ただし形や立体感には違いがあり、同一商品かどうかは写真からは判断できない",
        "見えている耳は、DAIKIが向かって左・YOSHIKIが向かって右で左右逆",
        "反対側の耳は写っておらず、「両耳お揃い」か「1つずつ分けっこ」かは未確定",
    ]),
    h2("そもそも「デカ猫」とは？Nekoとの意外なつながり"),
    p("「デカ猫」は、DAIKIさん(178cm)とYOSHIKIさん(177cm)の2人に、ファンが付けた愛称(ケミ名)です。<br>"
      "由来は、『PRODUCE 101 JAPAN 新世界』のコンセプト評価で2人が同じチームで披露した楽曲「Neko」。背の高い2人が愛らしい猫を全力で演じたギャップから、「デカい猫」=デカ猫と呼ばれるようになりました。<br>"
      "詳しい成り立ちは<a href=\"https://chomoand-1.com/ko1keyz-dekaneko-daiki-yoshiki-10569\" target=\"_blank\" rel=\"noopener\">デカ猫の由来を解説した記事</a>、他のケミ名は<a href=\"https://chomoand-1.com/ko1keyz-chemi-names-11773\" target=\"_blank\" rel=\"noopener\">ケミ名まとめ記事</a>で紹介しています。<br>"
      "そして今回のTGCで披露された3曲の中に、まさにその「Neko」が含まれていました。<br>"
      "デカ猫の原点になった曲を、デビュー前の初の大舞台で2人が並んで歌ったその日に、耳元まで似た輝きだったというのは、ファンにとってたまらない偶然です。<br>"
      "もちろん、これが意図的なお揃いなのか、たまたまなのかは分かりません。それでも「ちょっとお揃いっぽい」と受け取れる余地があること自体が、デカ猫というペアの魅力なのだと思います。"),
    p("実は2人の関係にちなんだ色合わせをしていた前例もあります。<br>"
      "7月中旬の私服では、DAIKIさんがピアスと服の色を、YOSHIKIさんとのケミ名「デカ猫」にちなんだ緑系でさりげなく揃えていたことが確認できます(詳細は上記のピアスの数の記事に掲載)。<br>"
      "また、DAIKIさんは<a href=\"https://chomoand-1.com/midori_kinari_osoroi-8418\" target=\"_blank\" rel=\"noopener\">オーディション時代に別のメンバーとお揃いのピアスをしていると話題になった</a>ことがあり、小物を仲間と合わせるのが好きなタイプなのかもしれません。<br>"
      "本人たちが「お揃い」と公言した事実は確認できていないため、こちらも推測の範囲にとどまります。"),
    h2("まとめ"),
    checks([
        "2026年9月19日のマイナビTGC 2026 A/W後の公式写真で、DAIKIとYOSHIKIが似た花型のキラキラピアスを着けていた",
        "中央の石+小粒の石のふち取り+ゴールド系の台座は共通だが、同一商品と断定できる材料はない",
        "ブランド・商品名は公式に明かされておらず、衣装の一部か私物かも不明",
        "見えている耳が左右逆のため「分けっこ」説も出るが、反対側の耳が確認できず未確定",
        "その日は2人の原点である「Neko」も披露され、デカ猫ファンには忘れられない1日になった",
    ]),
    p("ブランドや着用意図が分かる情報(本人の発信、スタイリストやブランド側の投稿、後日の高解像度写真など)が出てきたら、この記事に追記します。<br>"
      "10月7日のデビューまでに、デカ猫の2人がどんな耳元を見せてくれるのかも楽しみに待ちたいところです。"),
    related_box("デカ猫・DAIKI・YOSHIKIの関連記事", [
        ("https://chomoand-1.com/ko1keyz-dekaneko-daiki-yoshiki-10569", "デカ猫の由来とケミ名の意味を解説した記事"),
        ("https://chomoand-1.com/how-many-piercings-do-ko1keyz-12030", "KO1KEYZメンバー12人のピアスの数をまとめた記事"),
        ("https://chomoand-1.com/ko1keyz-chemi-names-11773", "KO1KEYZのケミ名を全ペア一覧にした記事"),
        ("https://chomoand-1.com/ko1keyz-mynavi-tgc-live-stream-12280", "マイナビTGCの配信・生中継について調べた記事"),
    ]),
])

JP_SUMMARY = ("9/19のマイナビTGCで、デカ猫のDAIKIとYOSHIKIが似た花型のキラキラピアスを着用。"
              "公式写真を拡大して見比べ、ブランドの手がかりと「お揃い？分けっこ？」の可能性を整理しました。")

# ================= KOREAN =================
KR_TITLE = "데카네코 피어싱은 커플템? DAIKI와 YOSHIKI가 TGC에서 착용"
KR_SLUG_SUFFIX = "-kr"

kr_pair = img_html(pair_media, "마이나비 TGC 2026 A/W 이후 공식 사진. 데님 재킷 차림의 DAIKI와 스트라이프 셔츠 차림의 YOSHIKI",
                   f'출처: <a href="{DAIKI_SRC}" target="_blank" rel="noopener">@KO1KEYZofficial(X)의 DAIKI 게시물</a>・'
                   f'<a href="{YOSHIKI_SRC}" target="_blank" rel="noopener">YOSHIKI 게시물</a>')
kr_zoom = img_html(zoom_media, "DAIKI와 YOSHIKI의 귀 부분 피어싱을 확대해 나란히 놓은 이미지",
                   "왼쪽: DAIKI, 오른쪽: YOSHIKI (위 공식 사진을 확대)")

KR_CONTENT = "\n\n".join([
    p("2026년 9월 19일 요코하마 아레나에서 열린 「마이나비 TGC 2026 A/W」에 첫 출연한 KO1KEYZ(코이키즈).<br>"
      "공연 후 공식 X가 멤버 한 명씩 올린 사진을 다시 보면, 팬들 사이에서 케미명 「데카네코(デカ猫)」로 불리는 DAIKI(가토 다이키)와 YOSHIKI(야다 요시키)가 매우 비슷한 반짝이는 피어싱을 하고 있다는 것을 알 수 있습니다.<br>"
      "결론부터 말하면 두 사람 모두 <strong>중앙에 큰 스톤, 그 주위에 작은 스톤을 빙 둘러 배치한 「꽃(헤일로) 모양」 골드 계열 피어싱</strong>으로 보이지만, 브랜드명이나 상품명은 공식적으로 밝혀지지 않아 현재로서는 특정할 수 없습니다.<br>"
      "이 글에서는 공식 사진을 바탕으로 두 사람의 귀 부분을 확대해 비교하고, 「정말 커플템인지」 「어디 제품인지」를 정리합니다."),
    titled_list("이 글에서 알 수 있는 것", [
        "두 사람이 9/19 TGC에서 착용한 피어싱의 모습",
        "확대해서 나란히 놓으면 어디가 비슷하고 어디가 다른지",
        "브랜드・상품명은 밝혀졌는지",
        "「양쪽 귀 커플템」 「한 짝씩 나눠 착용」의 가능성",
        "데카네코와 「Neko」, 그리고 TGC의 뜻밖의 관계",
    ]),
    h2("9/19 TGC에서 무슨 일이? KO1KEYZ 첫 패션 이벤트 출연"),
    point_box("이벤트 개요:", "「마이나비 TGC 2026 A/W」 2026년 9월 19일(토)・요코하마 아레나. KO1KEYZ는 10월 7일 데뷔 전에 첫 출연해 데님 의상으로 「신세계(SHINSEKAI)-KO1KEYZ ver.-」 「Neko(네코)-KO1KEYZ TGC ver.-」 「KO1KEYZ」 3곡을 선보였다"),
    p("KO1KEYZ에게 TGC는 일본 국내 대형 패션 이벤트 첫 출연 무대였습니다.<br>"
      "선보인 곡은 「신세계(SHINSEKAI)」 KO1KEYZ ver., 오디션 프로그램 『PRODUCE 101 JAPAN 신세계』의 콘셉트 평가곡으로 알려진 「Neko」의 TGC 스페셜 버전, 그리고 데뷔곡 「KO1KEYZ」 3곡입니다.<br>"
      "시청 방법 등은 <a href=\"https://chomoand-1.com/ko/ko1keyz-mynavi-tgc-live-stream-kr-12284\" target=\"_blank\" rel=\"noopener\">KO1KEYZ 마이나비 TGC 생중계를 조사한 글</a>에서 소개했습니다.<br>"
      "무대 후 공식 X는 멤버 한 명씩의 사진을 연달아 올렸고, 이번 화제의 발단이 된 것이 그중 DAIKI와 YOSHIKI의 두 장입니다."),
    h2("공식 사진으로 확인되는 두 사람의 귀 부분"),
    kr_pair,
    p("DAIKI는 빛바랜 색감의 데님 재킷 차림으로, 두 손을 가슴 앞에서 교차한 포즈입니다. 손가락에는 가느다란 골드 링이 여러 개 겹쳐 있고, 귀에는 정면 기준 왼쪽 귀에 반짝이는 피어싱이 보입니다.<br>"
      "YOSHIKI는 핑크빛 머리에 블루 스트라이프 셔츠 차림으로, 주먹을 뺨에 갖다 댄 포즈입니다. 정면 기준 오른쪽 귀에 피어싱이 빛나고, 손가락에는 실버 계열 반지를 끼고 있습니다.<br>"
      "의상도 포즈도 다른 두 장이지만, 귀 부분의 반짝임이 매우 닮았다는 것이 이번에 눈에 띈 포인트입니다."),
    h2("피어싱을 확대해서 비교해 봤다"),
    kr_zoom,
    p("공식 사진 원본에서 각자의 귀 부분만 잘라 나란히 놓은 것이 위 이미지입니다.<br>"
      "작은 파츠라 세부까지는 읽을 수 없지만, 보이는 범위에서 특징을 정리하면 다음과 같습니다."),
    table([
        ["항목", "DAIKI", "YOSHIKI"],
        ["보이는 귀", "정면 기준 왼쪽 귀", "정면 기준 오른쪽 귀"],
        ["전체 형태", "둥근 느낌의 오벌(타원)형", "꽃잎이 퍼지는 듯한 둥근 형태"],
        ["스톤 배치", "중앙에 약간 큰 스톤, 주위에 작은 스톤을 한 바퀴", "중앙에 큰 스톤, 주위에 작은 스톤을 한 바퀴"],
        ["색감", "투명~샴페인 계열 스톤과 골드 계열 세팅", "투명 스톤과 골드 계열 세팅"],
        ["귓불 아래", "세팅 외의 파츠는 확인되지 않음", "골드색 가는 링 모양 파츠가 보임(후프형일 가능성)"],
        ["기타 액세서리", "양손에 골드 반지 여러 개", "실버 계열 반지 1개"],
    ]),
    p("공통점은 「중앙의 주인공 스톤」+「작은 스톤 테두리」+「골드 계열 세팅」이라는 구성입니다.<br>"
      "다만 DAIKI의 것은 조금 납작하고 둥근 실루엣, YOSHIKI의 것은 꽃잎이 바깥으로 퍼지는 입체감이 있어, 사진 해상도와 각도 차이를 감안해도 <strong>완전히 같은 상품이라고 단정할 만큼의 일치는 확인되지 않습니다</strong>.<br>"
      "「같은 브랜드의 색상・사이즈 차이」 「같은 시리즈의 다른 모델」 「전혀 다른 피어싱이 우연히 닮았을 뿐」 모두 사진만으로는 부정할 수 없는 상태입니다."),
    h2("브랜드나 상품명은 밝혀졌을까?"),
    point_box("현재 결론:", "공식에서 브랜드명・상품명 발표는 없으며 특정되지 않았다. 단정은 피하고 후속 정보가 있으면 추가한다"),
    p("브랜드에 대해서는 공식 X 게시글에도, TGC 관련 공개 정보에도 액세서리 제공처나 스타일링 협력처 기재를 찾을 수 없었습니다.<br>"
      "TGC 무대는 전 멤버가 데님 의상으로 통일되어 있었기 때문에, 귀와 손가락의 액세서리도 의상에 맞춰 스타일리스트가 준비한 것일 가능성이 있습니다.<br>"
      "한편 DAIKI는 좌우 2개씩 피어싱 구멍이 있고 평소 액세서리를 즐기는 멤버이기도 해서, 본인 소지품일 가능성도 충분히 생각할 수 있습니다.<br>"
      "어느 쪽인지 판단할 자료가 지금은 없기 때문에 「의상의 일부인지 소지품인지」를 포함해 불명이라는 것이 솔직한 결론입니다.<br>"
      "비슷한 분위기의 아이템을 찾는다면 「플라워」 「헤일로」 「클러스터」 「지르코니아」 「골드」 「스터드」 「미니 후프」 같은 키워드로 찾으면 디자인이 가까운 상품을 발견하기 쉽습니다.<br>"
      "다만 어디까지나 겉모습이 비슷할 뿐, 본인 착용품과 같다고는 할 수 없다는 점에 유의해 주세요."),
    h2("양쪽 귀 커플템? 아니면 한 짝씩 나눠 낀 걸까?"),
    p("또 하나 궁금한 것은 사진에 보이는 귀의 방향입니다.<br>"
      "DAIKI는 정면 기준 왼쪽 귀, YOSHIKI는 정면 기준 오른쪽 귀로 <strong>보이는 귀가 좌우 반대</strong>입니다.<br>"
      "여기서 「같은 한 쌍의 피어싱을 한 짝씩 나눠 낀 게 아닐까?」 「양쪽 귀 모두 같은 디자인이 아닐까?」라는 시각도 나오지만, 반대쪽 귀는 확인이 어려운 것이 실정입니다.<br>"
      "DAIKI의 반대쪽 귀에는 아주 작은 빛이 희미하게 찍혀 있지만 형태까지는 알 수 없습니다.<br>"
      "YOSHIKI의 반대쪽 귀는 머리카락에 가려 찍혀 있지 않습니다.<br>"
      "참고로 앞서 정리한 <a href=\"https://chomoand-1.com/ko/how-many-piercings-do-ko1keyz-kr-12034\" target=\"_blank\" rel=\"noopener\">KO1KEYZ 멤버 피어싱 개수 글</a>에서는 DAIKI는 좌우 2개씩 총 4개, YOSHIKI는 좌우 1개씩 총 2개로 정리했습니다.<br>"
      "YOSHIKI가 양쪽 귀에 착용했더라도 구멍 수는 좌우 1개씩이라 겉모습상 모순은 없습니다.<br>"
      "즉 「한 짝씩 나눴다」는 가능성도 「양쪽 귀 커플템」 가능성도 모두 성립하는 상황이라, 지금 사진만으로는 결정타가 없습니다."),
    checks([
        "두 사람 모두 중앙 스톤+작은 스톤 테두리+골드 계열 세팅이라는 닮은 구성의 피어싱으로 보인다",
        "다만 형태와 입체감에 차이가 있어 동일 상품인지는 사진으로 판단할 수 없다",
        "보이는 귀는 DAIKI가 정면 기준 왼쪽, YOSHIKI가 오른쪽으로 좌우 반대",
        "반대쪽 귀는 찍혀 있지 않아 「양쪽 귀 커플템」인지 「한 짝씩 나눔」인지는 미확정",
    ]),
    h2("애초에 「데카네코」란? Neko와의 뜻밖의 연결고리"),
    p("「데카네코」는 DAIKI(178cm)와 YOSHIKI(177cm) 두 사람에게 팬들이 붙인 애칭(케미명)입니다.<br>"
      "유래는 『PRODUCE 101 JAPAN 신세계』 콘셉트 평가에서 두 사람이 같은 팀으로 선보인 곡 「Neko」. 키 큰 두 사람이 사랑스러운 고양이를 전력으로 연기한 갭 때문에 「큰 고양이」=데카네코로 불리게 되었습니다.<br>"
      "자세한 유래는 <a href=\"https://chomoand-1.com/ko/ko1keyz-dekaneko-daiki-yoshiki-kr-10797\" target=\"_blank\" rel=\"noopener\">데카네코 유래를 해설한 글</a>, 다른 케미명은 <a href=\"https://chomoand-1.com/ko/ko1keyz-chemi-names-kr-12754\" target=\"_blank\" rel=\"noopener\">케미명 모음 글</a>에서 소개하고 있습니다.<br>"
      "그리고 이번 TGC에서 선보인 3곡 중에 바로 그 「Neko」가 포함되어 있었습니다.<br>"
      "데카네코의 원점이 된 곡을 데뷔 전 첫 대형 무대에서 두 사람이 나란히 부른 그날, 귀 부분까지 비슷하게 반짝였다는 것은 팬들에게는 참을 수 없는 우연입니다.<br>"
      "물론 이것이 의도적인 커플템인지 우연인지는 알 수 없습니다. 그래도 「약간 커플템 같다」고 받아들일 여지가 있다는 것 자체가 데카네코라는 페어의 매력이라고 생각합니다."),
    h2("정리"),
    checks([
        "2026년 9월 19일 마이나비 TGC 2026 A/W 후 공식 사진에서 DAIKI와 YOSHIKI가 닮은 꽃 모양 반짝이 피어싱을 착용",
        "중앙 스톤+작은 스톤 테두리+골드 계열 세팅은 공통이지만 동일 상품이라고 단정할 자료는 없음",
        "브랜드・상품명은 공식적으로 밝혀지지 않았고 의상의 일부인지 소지품인지도 불명",
        "보이는 귀가 좌우 반대라 「한 짝씩 나눔」설도 나오지만 반대쪽 귀가 확인되지 않아 미확정",
        "그날은 두 사람의 원점인 「Neko」도 선보여 데카네코 팬에게 잊을 수 없는 하루가 됨",
    ]),
    p("브랜드나 착용 의도를 알 수 있는 정보(본인 발신, 스타일리스트나 브랜드 측 게시, 후일의 고해상도 사진 등)가 나오면 이 글에 추가하겠습니다.<br>"
      "10월 7일 데뷔까지 데카네코 두 사람이 어떤 귀 부분을 보여줄지도 기대하며 기다려 보겠습니다."),
    related_box("데카네코・DAIKI・YOSHIKI 관련 글", [
        ("https://chomoand-1.com/ko/ko1keyz-dekaneko-daiki-yoshiki-kr-10797", "데카네코 유래와 케미명의 의미를 해설한 글"),
        ("https://chomoand-1.com/ko/how-many-piercings-do-ko1keyz-kr-12034", "KO1KEYZ 멤버 12명의 피어싱 개수를 정리한 글"),
        ("https://chomoand-1.com/ko/ko1keyz-chemi-names-kr-12754", "KO1KEYZ 케미명을 전 페어 목록으로 만든 글"),
        ("https://chomoand-1.com/ko/ko1keyz-mynavi-tgc-live-stream-kr-12284", "마이나비 TGC 중계에 대해 조사한 글"),
    ]),
])

KR_SUMMARY = ("9/19 마이나비 TGC에서 데카네코 DAIKI와 YOSHIKI가 비슷한 꽃 모양 반짝이 피어싱을 착용. "
              "공식 사진을 확대해 비교하고 브랜드 단서와 「커플템? 한 짝씩 나눔?」 가능성을 정리했습니다.")

# ================= ENGLISH =================
EN_TITLE = "Are Dekaneko's Earrings a Match? DAIKI and YOSHIKI at TGC"

en_pair = img_html(pair_media, "Official photos after Mynavi TGC 2026 A/W: DAIKI in a denim jacket and YOSHIKI in a striped shirt",
                   f'Source: <a href="{DAIKI_SRC}" target="_blank" rel="noopener">@KO1KEYZofficial (X), DAIKI post</a> / '
                   f'<a href="{YOSHIKI_SRC}" target="_blank" rel="noopener">YOSHIKI post</a>')
en_zoom = img_html(zoom_media, "Close-up of DAIKI's and YOSHIKI's earrings side by side",
                   "Left: DAIKI, right: YOSHIKI (enlarged from the official photos above)")

EN_CONTENT = "\n\n".join([
    p("KO1KEYZ made their first appearance at the Mynavi TGC 2026 A/W at Yokohama Arena on September 19, 2026.<br>"
      "Looking back at the individual photos the official X account posted after the show, DAIKI (Daiki Kato) and YOSHIKI (Yoshiki Yada), the pair fans call \"Dekaneko,\" appear to be wearing very similar sparkling earrings.<br>"
      "In short, both look like <strong>gold-toned \"flower (halo) style\" earrings with a larger stone in the center ringed by small stones</strong>, but no brand or product name has been officially disclosed, so it can't be identified at this point.<br>"
      "This article enlarges their ears from the official photos to compare them and sort out whether they are truly a matching pair and where they might be from."),
    titled_list("What this article covers", [
        "What the earrings the two wore at TGC on 9/19 look like",
        "What looks the same and what differs when you enlarge them side by side",
        "Whether the brand or product name is known",
        "Whether they could be a matching pair or one earring each",
        "The unexpected link between Dekaneko, \"Neko,\" and TGC",
    ]),
    h2("What happened at TGC on 9/19? KO1KEYZ's first fashion event"),
    point_box("Event overview:", "Mynavi TGC 2026 A/W, Saturday, September 19, 2026, Yokohama Arena. Ahead of their October 7 debut, KO1KEYZ made their first appearance in denim outfits and performed three songs: \"Shinsekai (SHINSEKAI) -KO1KEYZ ver.-,\" \"Neko -KO1KEYZ TGC ver.-,\" and \"KO1KEYZ\""),
    p("TGC was KO1KEYZ's first appearance at a major fashion event in Japan.<br>"
      "They performed the KO1KEYZ version of \"Shinsekai (SHINSEKAI),\" a special TGC version of \"Neko\" (known from the concept evaluation of the audition show PRODUCE 101 JAPAN THE NEW WORLD), and their debut song \"KO1KEYZ.\"<br>"
      "For how to watch, see <a href=\"https://chomoand-1.com/en/ko1keyz-mynavi-tgc-live-stream-en-12285\" target=\"_blank\" rel=\"noopener\">our article on the KO1KEYZ Mynavi TGC live stream</a>.<br>"
      "After the stage, the official X account posted a photo of each member in turn, and the buzz here started with the ones of DAIKI and YOSHIKI."),
    h2("What the official photos show of their ears"),
    en_pair,
    p("DAIKI wears a faded denim jacket and crosses both hands in front of his chest. Several slim gold rings are stacked on his fingers, and a sparkling earring is visible on the ear on the left side of the frame.<br>"
      "YOSHIKI, with pink hair and a blue-striped shirt, rests a fist against his cheek. A sparkling earring shows on the ear on the right side of the frame, and he wears a silver-toned ring.<br>"
      "The outfits and poses differ, but the sparkle at their ears looks strikingly alike, and that's the point that stood out."),
    h2("Comparing the earrings up close"),
    en_zoom,
    p("The image above is cut from the original-resolution official photos, showing only each ear.<br>"
      "The pieces are tiny so fine details can't be read, but here is what can be made out."),
    table([
        ["Item", "DAIKI", "YOSHIKI"],
        ["Visible ear", "Left side of the frame", "Right side of the frame"],
        ["Overall shape", "Rounded oval", "Round, with petals fanning outward like a flower"],
        ["Stones", "A slightly larger center stone ringed by small stones", "A larger center stone ringed by small stones"],
        ["Color", "Clear to champagne-toned stones with a gold-toned setting", "Clear stones with a gold-toned setting"],
        ["Below the lobe", "No other parts visible besides the setting", "A thin gold ring-like part is visible (possibly a hoop type)"],
        ["Other accessories", "Several gold rings on both hands", "One silver-toned ring"],
    ]),
    p("What they share is the construction: a \"center stone,\" a \"border of small stones,\" and a \"gold-toned setting.\"<br>"
      "However, DAIKI's looks slightly flatter and rounder, while YOSHIKI's has a three-dimensional feel with petals spreading outward. Even allowing for differences in resolution and angle, <strong>there isn't enough match to say they are the very same product</strong>.<br>"
      "\"Same brand in a different color or size,\" \"different models from the same series,\" and \"two unrelated earrings that happen to look alike\" can't be ruled out from the photos alone."),
    h2("Is the brand or product name known?"),
    point_box("Current conclusion:", "No brand or product name has been announced officially, so it can't be identified. We avoid drawing conclusions and will update if more information appears"),
    p("Neither the official X post text nor the public TGC information gives any credit for who supplied the accessories or handled the styling.<br>"
      "Since all members were in unified denim outfits on the TGC stage, the accessories on ears and fingers may have been prepared by a stylist to go with the costumes.<br>"
      "On the other hand, DAIKI has two piercing holes on each side and enjoys accessories in everyday life, so they could well be his own.<br>"
      "There's currently nothing to tell which it is, so the honest answer is that it's unknown, including whether it is a costume piece or personal.<br>"
      "If you want something with a similar look, searching keywords like \"flower,\" \"halo,\" \"cluster,\" \"zirconia,\" \"gold,\" \"stud,\" and \"mini hoop\" should turn up items with a close design.<br>"
      "Just keep in mind that a similar look doesn't mean it's the same as what they wore."),
    h2("Matching in both ears, or one each?"),
    p("Another thing that stands out is which ears are visible.<br>"
      "DAIKI's visible ear is on the left side of the frame and YOSHIKI's on the right, so <strong>the ears shown are opposite sides</strong>.<br>"
      "That invites theories such as \"could they be wearing one of the same pair each?\" or \"are both ears the same design?\", but the far ears are hard to confirm.<br>"
      "On DAIKI's far ear, a very small glint appears faintly, but its shape can't be made out.<br>"
      "YOSHIKI's far ear is hidden by his hair and isn't visible.<br>"
      "For reference, in <a href=\"https://chomoand-1.com/en/how-many-piercings-do-ko1keyz-en-12038\" target=\"_blank\" rel=\"noopener\">our article on how many piercings each KO1KEYZ member has</a>, we counted DAIKI at two on each side (four total) and YOSHIKI at one on each side (two total).<br>"
      "Even if YOSHIKI wore them in both ears, that is one hole per side, so it doesn't contradict what we see.<br>"
      "In other words, both \"one each\" and \"matching in both ears\" are possible, and the current photos aren't decisive."),
    checks([
        "Both appear to wear earrings built the same way: center stone, border of small stones, gold-toned setting",
        "But shape and depth differ, so we can't tell from the photos whether it's the same product",
        "The visible ears are opposite sides: DAIKI on the left of the frame, YOSHIKI on the right",
        "The far ears aren't visible, so \"matching in both ears\" versus \"one each\" is unconfirmed",
    ]),
    h2("What is \"Dekaneko\" anyway? The unexpected link to \"Neko\""),
    p("\"Dekaneko\" is the nickname (chemistry name) fans gave DAIKI (178 cm) and YOSHIKI (177 cm).<br>"
      "It comes from \"Neko,\" the song the two performed on the same team in the concept evaluation of PRODUCE 101 JAPAN THE NEW WORLD. The gap of two tall members playing adorable cats with full commitment led to the name \"big cat,\" or Dekaneko.<br>"
      "For the full story see <a href=\"https://chomoand-1.com/en/ko1keyz-dekaneko-daiki-yoshiki-en-11527\" target=\"_blank\" rel=\"noopener\">our explainer on the origin of Dekaneko</a>, and for other pairs see <a href=\"https://chomoand-1.com/en/ko1keyz-chemi-names-en-12756\" target=\"_blank\" rel=\"noopener\">our roundup of chemistry names</a>.<br>"
      "And among the three songs performed at TGC was exactly that \"Neko.\"<br>"
      "On the day the two stood side by side singing the song that started Dekaneko at their first big stage before debut, their ears sparkled alike, which is a coincidence fans can't resist.<br>"
      "Whether it's an intentional match or chance is unknown. Still, the room to read it as \"a little bit matching\" is part of what makes Dekaneko so appealing."),
    h2("Summary"),
    checks([
        "In official photos after Mynavi TGC 2026 A/W on September 19, 2026, DAIKI and YOSHIKI wore similar flower-style sparkling earrings",
        "They share a center stone, border of small stones, and gold-toned setting, but nothing proves they are the same product",
        "No brand or product name has been disclosed, and whether it's costume or personal is unknown",
        "The visible ears are opposite sides, which fuels the \"one each\" theory, but the far ears can't be confirmed",
        "The day also included \"Neko,\" the song behind Dekaneko, making it a day Dekaneko fans won't forget",
    ]),
    p("If information about the brand or the intent appears (a post from the members, the stylist or the brand, or higher-resolution photos later), we'll update this article.<br>"
      "We're also looking forward to what the Dekaneko pair shows at their ears before the October 7 debut."),
    related_box("Related articles on Dekaneko, DAIKI, and YOSHIKI", [
        ("https://chomoand-1.com/en/ko1keyz-dekaneko-daiki-yoshiki-en-11527", "An explainer on the origin and meaning of Dekaneko"),
        ("https://chomoand-1.com/en/how-many-piercings-do-ko1keyz-en-12038", "How many piercings each of the 12 KO1KEYZ members has"),
        ("https://chomoand-1.com/en/ko1keyz-chemi-names-en-12756", "A full list of KO1KEYZ chemistry names"),
        ("https://chomoand-1.com/en/ko1keyz-mynavi-tgc-live-stream-en-12285", "How to watch the Mynavi TGC stream"),
    ]),
])

EN_SUMMARY = ("At Mynavi TGC on 9/19, Dekaneko's DAIKI and YOSHIKI wore similar flower-style sparkling earrings. "
              "We enlarged the official photos to compare them and sort out the brand clues and the matching-pair theories.")


# ---------------- 投稿 ----------------
def get_slug(title, fallback):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={urllib.parse.quote(title)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        en = "".join(seg[0] for seg in data[0])
        slug = re.sub(r"[^a-z0-9\s-]", "", en.lower())
        slug = re.sub(r"\s+", "-", slug.strip())
        slug = re.sub(r"-+", "-", slug)[:30].rstrip("-")
        if slug:
            return slug
    except Exception as e:
        print("translate failed, using fallback slug:", e)
    return fallback


def plain_len(c):
    return len(re.sub(r"<!--.*?-->|<[^>]+>", "", c, flags=re.S))


def upload_png(path, name):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HA, "Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{name}"'},
                      data=path.read_bytes())
    r.raise_for_status()
    return r.json()["id"]


def post_draft(title, content, slug, cats, summary, lang=None, ja_id=None):
    payload = {"title": title, "content": content, "slug": slug, "status": "draft",
               "categories": cats, "author": 2, "meta": {"jetpack_publicize_message": summary}}
    if lang:
        payload["lang"] = lang
        payload["translations"] = {"ja": ja_id}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=H, data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    post = r.json()
    print(f"[{lang or 'ja'}] id={post['id']} slug={post['slug']} chars={plain_len(content)} link={post['link']}")
    return post


def set_featured(post_id, media_id):
    requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{post_id}", headers=H,
                  data=json.dumps({"featured_media": media_id}).encode("utf-8")).raise_for_status()


# JP
JP_SLUG = get_slug(JP_TITLE, JP_FALLBACK_SLUG)
jp = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, [66, 62], JP_SUMMARY)

JP_EYE = ROOT / "images" / "ko1keyz_dekaneko_tgc_earring_eyecatch.png"
subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
                "--top", "デカ猫のピアスはお揃い？",
                "--main", "KO1KEYZ",
                "--bottom", "TGCで着けていた花型ピアス",
                "--out", str(JP_EYE), "--seed", str(jp["id"])], check=True)
jp_media = upload_png(JP_EYE, "ko1keyz_dekaneko_tgc_earring_eyecatch.png")
set_featured(jp["id"], jp_media)
print("JP eyecatch", jp_media)

# KR
kr = post_draft(KR_TITLE, KR_CONTENT, jp["slug"] + "-kr", [74, 70], KR_SUMMARY, "ko", jp["id"])
KR_EYE = ROOT / "images" / "ko1keyz_dekaneko_tgc_earring_eyecatch_kr.png"
subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
                "--top", "데카네코 피어싱은 커플템?",
                "--main", "KO1KEYZ",
                "--bottom", "TGC에서 착용한 꽃 모양 피어싱",
                "--out", str(KR_EYE), "--seed", str(kr["id"]), "--lang", "kr"], check=True)
kr_media = upload_png(KR_EYE, "ko1keyz_dekaneko_tgc_earring_eyecatch_kr.png")
set_featured(kr["id"], kr_media)
print("KR eyecatch", kr_media)

# EN
en = post_draft(EN_TITLE, EN_CONTENT, jp["slug"] + "-en", [110], EN_SUMMARY, "en", jp["id"])
set_featured(en["id"], jp_media)

(ROOT / "tmp_ko1keyz_dekaneko_tgc_earring_ids.txt").write_text(
    f"jp={jp['id']} slug={jp['slug']} media={jp_media}\nkr={kr['id']} slug={kr['slug']} media={kr_media}\nen={en['id']} slug={en['slug']}\n"
    f"pair_media={pair_media['id']} zoom_media={zoom_media['id']}\n", encoding="utf-8")
print("DONE")
