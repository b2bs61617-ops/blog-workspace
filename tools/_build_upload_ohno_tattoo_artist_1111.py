# -*- coding: utf-8 -*-
"""大野智のタトゥーの彫師(JA¥ @jay.sit.jp)記事(chomoand.com トレンド速報)を組み立てて下書き投稿する(2026-11-11)。
usage: python tools/_build_upload_ohno_tattoo_artist_1111.py [--build-only] [--update-content]
状態は articles/ohno_tattoo_artist_posted.json に控え、再実行で重複投稿しない。
方針: プライベートスタジオなので住所・地図は出さない(プロフィールに書かれた「恵比寿・代官山」まで)。
彫師本人の公開投稿(本人了承済みと明記)を公式埋め込みで出す。
"""
import sys, os, json, base64, socket, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "articles", "ohno_tattoo_artist.html")
POSTED = os.path.join(REPO, "articles", "ohno_tattoo_artist_posted.json")
BASE_TITLE = "大野智のタトゥーを彫ったのは誰？恵比寿の彫師JA¥のインスタ"
assert len(BASE_TITLE) <= 35, len(BASE_TITLE)
TITLE = "【未】" + BASE_TITLE
SLUG = "ohno-satoshi-tattoo-artist"
CATEGORIES = [37]
AUTHORS = {"USER1": 3, "Tomoki": 4}
EYECATCH = os.path.join(REPO, "images", "ohno_tattoo_artist_eyecatch.png")
IG = "https://www.instagram.com/p/De1LpIUHU7Z/"
IG_OFFICIAL = "https://www.instagram.com/reel/DahAVMwSyZy/"  # satojima_official 告知動画(タトゥーが見える)

A, B, BG = "#1e88e5", "#bbdefb", "#f1f7fd"
TH = f"border:1px solid #ccc;padding:8px 12px;background:{A};color:#fff;"
TD = "border:1px solid #ccc;padding:8px 12px;"
TDZ = TD + f"background:{BG};"


def p(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n'


def html(s):
    return "<!-- wp:html -->\n" + s.strip() + "\n<!-- /wp:html -->\n\n"


def table(head, rows):
    h = "".join(f'<th style="{TH}">{c}</th>' for c in head) if head else ""
    body = ""
    for i, r in enumerate(rows):
        st = TDZ if i % 2 else TD
        body += "<tr>" + "".join(f'<td style="{st}">{c}</td>' for c in r) + "</tr>\n"
    thead = f"<thead><tr>{h}</tr></thead>\n" if head else ""
    return ("<!-- wp:table -->\n<figure class=\"wp-block-table\"><table class=\"has-fixed-layout\">"
            f"{thead}<tbody>\n{body}</tbody></table></figure>\n<!-- /wp:table -->\n\n")


def mini(*kv):
    inner = "".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>' for i, (k, v) in enumerate(kv))
    return html(f'<div style="border:1px solid {B};border-left:4px solid {A};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">{inner}</div>')


def mark(t):
    return f'<strong><span class="swl-marker mark_blue" style="font-size:1.15em;">{t}</span></strong>'


CHK = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {A};border-radius:3px;'
       f'color:{A};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')

IG_EMBED = html(f'''<blockquote class="instagram-media" data-instgrm-permalink="{IG}?utm_source=ig_embed" data-instgrm-version="14" style="background:#FFF;border:0;margin:1px auto;max-width:540px;min-width:280px;width:calc(100% - 2px);"><a href="{IG}" target="_blank" rel="noopener">JA¥さんのInstagramの投稿を見る</a></blockquote>
<script async src="//www.instagram.com/embed.js"></script>''')

out = ""
out += p("嵐の大野智さんの左腕のタトゥーは、だれが彫ったのでしょうか。",
         "結論から言うと、" + mark("東京・恵比寿の彫師「JA¥(ジェイ)」さん") + "とみられます。",
         "JA¥さんは10月23日、自身のInstagramにタトゥーのアップ写真を投稿していました。")
out += p("11月10日には女性自身が、この投稿のことを記事にしています。",
         "この記事では、彫師のJA¥さんがどんな人なのか、投稿の中身とあわせてまとめました。")

out += html(f'''
<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>大野智のタトゥーを彫った彫師は誰か</li>
<li>彫師のInstagramに書かれていたこと</li>
<li>彫師JA¥のスタジオと予約方法</li>
<li>タトゥーのデザインと色の意味</li>
<li>大野智がタトゥーについて話したこと</li>
</ul>
</div>''')

# ---- 彫師は誰 ----
out += h2("大野智のタトゥーを彫った彫師は誰？")
out += mini(("名前", "JA¥(ジェイ)"), ("Instagram", "@jay.sit.jp"),
            ("拠点", "東京・恵比寿"), ("スタジオ", "笑顔芸術工房(プライベートスタジオ)"))
out += p("大野智さんのタトゥーを彫ったとみられるのは、JA¥さんという彫師です。",
         "Instagramのアカウントは「@jay.sit.jp」で、プロフィールには「東京 恵比寿」と書かれています。")
out += p("10月23日、JA¥さんは大野さんのタトゥーのアップ写真を投稿しました。",
         "投稿には「#さと島」のハッシュタグも付いていて、" + mark("大野さん本人の了承をとったうえでの投稿") + "だと書かれています。")
out += IG_EMBED
out += p("写真には、赤・黄色・むらさき・青などの色がくっきり写っています。",
         "肌のきめまで見えるほどのアップなので、施術を担当した彫師でないと撮れない写真といえそうです。")

# ---- 投稿の中身 ----
out += h2("彫師のInstagramの投稿に書かれていたこと")
out += p("JA¥さんの投稿には、短いメッセージが添えられていました。",
         "内容をまとめると、次のとおりです。")
out += mini(("1行目", "「大王ご来店」"), ("2行目", "「島民として誇りです」"),
            ("3行目", "「今後ともよろしくお願いします」"), ("そのほか", "「※本人了承済みです」「#tokyotattoo #さと島」"))
out += p("「大王」と「島民」は、大野さんの個人サロン「さと島」で使われている言葉です。",
         "さと島は「さとしの島」を略した名前で、ファンは" + mark("「島民」") + "と呼ばれています。",
         "その島をおさめる大野さんが「大王」というわけです。")
out += p("つまりJA¥さんは、自分もファンの一人として、大王の来店を誇りに思うと伝えていたことになります。",
         "女性自身も、彫師はファンの一人とみられると伝えていました。")
out += p("投稿の位置情報は「恵比寿西」になっていました。",
         "コメント欄には、デザインの美しさや、さと島への愛を感じるといった声が集まっています。")

# ---- どんな人 ----
out += h2("彫師JA¥はどんな人？スタジオと予約方法")
out += table(None, [
    ("<strong>名前</strong>", "JA¥(ジェイ)"),
    ("<strong>Instagram</strong>", "@jay.sit.jp(フォロワー約4,100人)"),
    ("<strong>所属</strong>", "笑顔芸術工房(@smileink.studio)"),
    ("<strong>場所</strong>", "東京・代官山/恵比寿エリア"),
    ("<strong>予約</strong>", "InstagramのDMで受付"),
])
out += p("JA¥さんのプロフィールには、" + mark("「11・12月 DMにて予約受付中」") + "と書かれています。",
         "所属先として紹介されているのが「笑顔芸術工房」というスタジオです。")
out += p("笑顔芸術工房は、代官山・恵比寿にあるプライベートスタジオです。",
         "予約や問い合わせは、どちらもInstagramのDMで受け付けています。",
         "完全予約制のスタジオなので、住所は公開されていません。")
out += p("フォロワーは約4,100人と、知る人ぞ知る彫師といった感じです。",
         "大きな有名スタジオではなく、落ち着いて施術を受けられるプライベートスタジオを選んだのも、大野さんらしいですね。")

# ---- デザイン ----
out += h2("大野智のタトゥーのデザインは？色の意味")
out += p("女性自身によると、このタトゥーのデザインは" + mark("さと島のファンクラブのロゴと同じ") + "です。",
         "「SATO島」という文字を、独特の書体でアレンジしたものだそうです。")
out += p("ポイントは「島」の部分に使われている色です。",
         "ここには、嵐のメンバーカラーの5色が入っていると伝えられています。")
out += table(("メンバー", "メンバーカラー"), [
    ("大野智", "青"),
    ("櫻井翔", "赤"),
    ("相葉雅紀", "緑"),
    ("二宮和也", "黄色"),
    ("松本潤", "むらさき"),
])
out += p("さらに、ふつうは黒で書かれる文字の一部が、あざやかな青になっているそうです。",
         "青は大野さん自身のメンバーカラーですね。",
         "グループを大切にしながら、自分の色もしっかり入れたデザインといえそうです。")

# ---- 流れ ----
out += h2("タトゥーが話題になるまでの流れ")
out += table(("時期", "出来事"), [
    ("2026年7月8日", "さと島の告知動画で左腕のタトゥーが見える"),
    ("2026年7月15日", "個人サロン「さと島」がオープン"),
    ("2026年8月", "公開された写真で、オレンジや白など色が増えていた"),
    ("2026年10月23日", "JA¥がタトゥーのアップ写真を投稿"),
    ("2026年10月30日", "VOGUE JAPAN 12月号でタトゥーについて話す"),
    ("2026年11月10日", "女性自身が彫師の投稿を記事にする"),
])
out += p("左腕のタトゥーが最初に話題になったのは、7月のさと島の告知動画です。",
         "ひじから手首にかけて、「SATOSHI」と読める大きな絵柄が入っていました。")
out += html(f'''<blockquote class="instagram-media" data-instgrm-permalink="{IG_OFFICIAL}?utm_source=ig_embed" data-instgrm-version="14" style="background:#FFF;border:0;margin:1px auto;max-width:540px;min-width:280px;width:calc(100% - 2px);"><a href="{IG_OFFICIAL}" target="_blank" rel="noopener">さと島公式Instagramの投稿を見る</a></blockquote>
<script async src="//www.instagram.com/embed.js"></script>''')
out += p("こちらが、さと島の公式Instagramに投稿された告知動画です。",
         "ソファに座って話す場面で、" + mark("左腕のタトゥー") + "がはっきり見えます。",
         "シャツ姿の場面でも、手首の近くに色の入ったタトゥーがのぞいていました。")
out += p("8月に公開された写真では、オレンジや白などの色が加わっていて、デザインが変わっていたそうです。",
         "時間をかけて少しずつ仕上げていったのかもしれません。",
         "10月のJA¥さんの「ご来店」は、その仕上げや色の追加だった可能性もありそうです。")

# ---- 本人の言葉 ----
out += h2("大野智がタトゥーについて話したこと")
out += p("大野さんは、10月30日発売の「VOGUE JAPAN」12月号のインタビューで、はじめてタトゥーについて話しました。",
         "その中で、次のように話しています。")
out += html(f'<p style="border-left:4px solid {A};padding:10px 16px;margin:0 0 16px 0;background:{BG};">'
            '「自分の体はキャンバスみたいなものですけど、一応親の許可も取ってますよ」</p>')
out += p("絵を描くことが大好きな大野さんらしく、自分の体をキャンバスにたとえていました。",
         "親の許可もとっていると話していて、家族思いな一面も見えます。")
out += p("7月の告知動画のころから、デザインが2008年の個展「FREESTYLE」の作品に似ていると話題でした。",
         "アートで自分を表してきた大野さんにとって、タトゥーも作品のひとつなのかもしれません。")

# ---- ファンの反応 ----
out += h2("ファンの反応は？")
out += p("JA¥さんの投稿のコメント欄には、作品の美しさをほめる声が多く寄せられています。",
         "「さと島への愛を感じる」といった声もあり、彫師もファンだったことに喜ぶ人が多いようです。")
out += p("7月にタトゥーが見えたときも、ネット上では好意的な声が多かったと伝えられています。",
         "隠さずに見せる姿や、いきいきとした様子を応援する声が目立ちました。")
out += p("さと島では11月1日の愛知を皮切りに、島民限定のバースデーイベント「さと島 SATOSHI OHNO 45→46」が開かれています。",
         "このあとも東京・福岡・大阪・宮城で予定されているので、会場でタトゥーを見られるかもしれませんね。")

# ---- まとめ ----
out += h2("まとめ")
items = [
    "大野智のタトゥーを彫ったとみられるのは、恵比寿の彫師JA¥(@jay.sit.jp)",
    "2026年10月23日に本人了承のうえでタトゥーのアップ写真を投稿",
    "投稿には「大王ご来店」「島民として誇りです」とファン目線のメッセージ",
    "所属は代官山・恵比寿のプライベートスタジオ「笑顔芸術工房」、予約はDM",
    "デザインはさと島のロゴで、「島」に嵐のメンバーカラー5色",
]
out += html(f'<div style="border:1px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">'
            + "".join(f'<p style="margin:{"0" if i == 0 else "6px 0 0 0"};">{CHK}{t}</p>' for i, t in enumerate(items)) + "</div>")
out += p("ファンでもある彫師が、心をこめて彫ったタトゥーだったんですね。",
         "気になる人は、JA¥さんのInstagramでアップ写真をチェックしてみてください。")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(out)
print(OUT, len(out))
if "--build-only" in sys.argv:
    sys.exit()

# ================= upload =================
out = open(OUT, encoding="utf-8").read()  # easy_read fix 後のファイルを使う
env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_TREND_USERNAME']}:{env['WP_TREND_APP_PASSWORD']}".encode()).decode()
host = socket.gethostname().split(".")[0]
AUTHOR = next((v for k, v in AUTHORS.items() if host.lower().startswith(k.lower())), None)
if AUTHOR is None:
    sys.exit(f"hostname {host} の投稿者がdocs/wordpress.mdの表に無いワン")


def req(path, data=None, headers=None, method="POST"):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode('utf-8', 'ignore')[:500]}")


def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})


state = json.load(open(POSTED, encoding="utf-8")) if os.path.exists(POSTED) else {}


def save():
    json.dump(state, open(POSTED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if "post" in state:
    if "--update-content" in sys.argv:
        jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"content": out, "status": "draft"})
        print("content updated", state["post"])
    else:
        print("already posted", state["post"])
else:
    po = jpost("/wp-json/wp/v2/posts", {"title": TITLE, "content": out, "slug": SLUG, "status": "draft",
                                        "categories": CATEGORIES, "author": AUTHOR})
    state["post"] = po["id"]
    save()
    print("draft", po["id"])
if "eyecatch" not in state and os.path.exists(EYECATCH):
    fn = os.path.basename(EYECATCH)
    m = req("/wp-json/wp/v2/media", open(EYECATCH, "rb").read(),
            {"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{fn}"'})
    jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": "大野智のタトゥーを彫った彫師は誰？"})
    state["eyecatch"] = m["id"]
    save()
    jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"featured_media": state["eyecatch"]})
po = req(f"/wp-json/wp/v2/posts/{state['post']}?context=edit", method="GET")
print(po["id"], po["status"], po["author"], po["categories"], po["featured_media"], po["title"]["raw"])
print("raw_len", len(po["content"]["raw"]), "has_ig", "instagram-media" in po["content"]["raw"])
print(f"{BASE}/?p={po['id']}")
