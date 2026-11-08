# -*- coding: utf-8 -*-
"""小嶋陽菜 結婚・出産発表 × AKB48 20周年武道館リハ「衣装が入らない」記事(chomoand.com トレンド速報)を組み立てて下書き投稿する(2026-11-08)。
usage: python tools/_build_upload_kojiharu_marriage_1108.py [--update-content]
状態は articles/kojiharu_marriage_posted.json に控え、再実行で重複投稿しない。
方針: 体型・お腹への言及はしない/妊娠時期は断定しない/元ネタのSNS投稿には触れない(docs/rules.md)。
"""
import sys, os, json, base64, socket, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "articles", "kojiharu_marriage_budokan_rehearsal.html")
POSTED = os.path.join(REPO, "articles", "kojiharu_marriage_posted.json")
BASE_TITLE = "小嶋陽菜が結婚＆出産！武道館リハ「衣装が入らない」は伏線？"
assert len(BASE_TITLE) <= 35, len(BASE_TITLE)
TITLE = "【未】" + BASE_TITLE
SLUG = "kojima-haruna-marriage-budokan-rehearsal"
CATEGORIES = [37]
AUTHORS = {"USER1": 3, "Tomoki": 4}
EYECATCH = os.path.join(REPO, "images", "kojiharu_marriage_eyecatch.png")
YT = "https://www.youtube.com/watch?v=K-ZpNL8JnrE"

A, B, BG = "#d81b60", "#f8bbd0", "#fdf2f6"
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
    return f'<strong><span class="swl-marker mark_pink" style="font-size:1.15em;">{t}</span></strong>'


def youtube(url):
    return ('<!-- wp:embed {"url":"' + url + '","type":"video","providerNameSlug":"youtube","responsive":true,'
            '"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->\n'
            '<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">'
            f'<div class="wp-block-embed__wrapper">\n{url}\n</div></figure>\n<!-- /wp:embed -->\n\n')


CHK = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {A};border-radius:3px;'
       f'color:{A};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')

out = ""
out += p("元AKB48の小嶋陽菜(こじはる)が、2026年11月7日に" + mark("結婚と第1子の出産") + "を発表しました。",
         "妊娠中には公表せず、出産を終えてからの報告だったので、驚いた人も多かったのではないでしょうか。",
         "そんな中で思い出したいのが、2025年12月のAKB48 20周年コンサートのリハーサル映像です。",
         "こじはるが「RIVER」の衣装を着て「これ絶対私の衣装じゃない」と笑っていた、あの場面です。",
         "この記事では、結婚・出産発表の内容と、武道館リハで衣装が入らなかったエピソードをまとめました。")

out += html(f'''
<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{A};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>小嶋陽菜の結婚・出産発表の内容</li>
<li>武道館リハで「衣装が入らない」となった場面</li>
<li>20周年コンサートから発表までの流れ</li>
<li>リハ映像は伏線だったのか</li>
<li>小嶋陽菜のプロフィール</li>
</ul>
</div>''')

# ---- 発表 ----
out += h2("小嶋陽菜が結婚と第1子出産を発表")
out += mini(("発表日", "2026年11月7日"), ("発表方法", "本人のX・Instagram"),
            ("お相手", "非公表(一般男性と報じられています)"), ("出産の時期・性別", "非公表"))
out += p("小嶋陽菜は11月7日、自身のXとInstagramで、結婚と第1子の出産を報告しました。",
         "コメントでは、無事に出産を迎えてから伝えたいと考えていたことを明かしていて、母子ともに健康で「穏やかな日々を過ごしております」とつづっています。",
         "あわせて、入籍したこともファンに報告しました。")
out += p("お相手については本人は触れていませんが、一般男性だと報じられています。",
         "出産の時期や赤ちゃんの性別も明かされていません。",
         "今後も仕事は続けていくそうで、コメントは「これまで以上に仕事に真摯に向き合い」と前向きな言葉で結ばれていました。")

# ---- リハ ----
out += h2("AKB48 20周年武道館リハで「衣装が入らない」")
out += p("話はさかのぼって、2025年12月です。",
         "AKB48は結成20周年を記念して、日本武道館で20周年記念コンサートを開きました。",
         "こじはるはOGメンバーとして出演していて、その" + mark("リハーサルの裏側") + "を自身のYouTubeチャンネルで公開しています。")
out += youtube(YT)
out += mini(("動画タイトル", "【おもしろ場面】AKB48リハの裏側まとめました❣️【カラオケ】"),
            ("公開日", "2026年3月6日"), ("チャンネル", "小嶋陽菜 公式YouTubeチャンネル"))
out += p("この動画の中で、こじはるが「RIVER」の衣装を試着する場面があります。",
         "軍服風のワンピース衣装の前を留めてもらいながら、「私これ入らなくない？」「これ絶対私の衣装じゃない」と大笑い。",
         "さらに「今こんな薄着でこんなパツパツ」とぼやいていて、画面には" + mark("「※1週間前は入ったのに」") + "というテロップも出ていました。")
out += p("スタッフに手伝ってもらいながら、最後はなんとか着替えを終えています。",
         "この衣装は早着替えのために前が開きやすいつくりになっていたと伝えられていて、留め具がはじけるハプニングもありました。",
         "動画では、峯岸みなみと「RIVER」の振り付けを自己流で踊って指原莉乃を笑わせたり、遅刻を高橋みなみにつっこまれたりと、OGメンバーとのにぎやかなやりとりも見られます。")

# ---- 本番 ----
out += h2("20周年コンサート本番でのこじはるは？")
out += mini(("公演", "AKB48 20周年記念コンサート"), ("会場", "日本武道館"), ("日程", "2025年12月4日〜7日"))
out += p("20周年記念コンサートは、2025年12月4日から7日までの4日間、日本武道館で開かれました。",
         "高橋みなみ、峯岸みなみ、柏木由紀、指原莉乃、横山由依などOGメンバーと、現役メンバーが同じステージに立つ特別な公演でした。")
out += p("こじはるは、OGメンバーとして「RIVER」などのステージに出演しました。",
         "12月6日の公演ではその日の出演者で最年長の37歳で、オープニングのMCで年長らしいあいさつをして会場を笑わせています。",
         "現役メンバーとは「ハート型ウイルス」も披露していて、リハで苦戦した衣装の場面がうそのように、本番は昔と変わらないこじはるらしさでファンを喜ばせていました。")

# ---- 時系列 ----
out += h2("20周年コンサートから結婚発表までの流れ")
out += table(("時期", "出来事"), [
    ("2025年12月4日〜7日", "AKB48 20周年記念コンサート(日本武道館)に出演"),
    ("2025年12月28日", "YouTubeで武道館の振り返り動画を公開"),
    ("2026年3月6日", "YouTubeでリハーサルの裏側動画を公開(衣装の場面)"),
    ("2026年11月7日", "結婚と第1子出産を発表"),
])
out += p("リハーサルが行われたのは、コンサート本番の直前の2025年12月です。",
         "そこから約11か月後に、結婚と出産が発表されたことになります。")

# ---- 伏線？ ----
out += h2("武道館リハの「衣装が入らない」は伏線だった？")
out += p("出産の発表を受けて、あのリハ映像を思い出したファンも多いかもしれません。",
         "ただ、こじはるは出産の時期を明かしていないので、" + mark("リハーサルの時点でどうだったのかは本人にしかわかりません") + "。",
         "動画の中のこじはるは、衣装の件を自分から笑いに変えていて、いつものマイペースなこじはるらしい場面でした。")
out += p("とはいえ、時期を考えてみると、まったくありえない話ではなさそうです。",
         "ここで「12月から十月十日なら、生まれるのは10月ごろ。11月の発表と合わないのでは？」と思った人もいるかもしれません。",
         "ただ、「十月十日(とつきとおか)」は最後の生理が始まった日を妊娠0週0日として数える言い方で、日数にすると約280日(40週)です。",
         "妊娠に気づくころにはすでに「妊娠2か月」になっていることが多いので、" + mark("そこから出産までは残り約8か月") + "になります。")
out += table(("リハ(2025年12月上旬)の時点で", "出産予定日の目安", "11月7日の発表まで"), [
    ("妊娠5週(2か月目)だった場合", "2026年8月上旬", "約3か月"),
    ("妊娠9週(3か月目)だった場合", "2026年7月上旬", "約4か月"),
])
out += p("つまり、もしリハのころに妊娠していたとすると、出産は2026年の7〜8月ごろになる計算です。",
         "そうなると、11月7日の発表は" + mark("出産から3〜4か月たってから") + "ということになります。",
         "産後しばらくは赤ちゃんのお世話で手いっぱいの時期なので、生活が落ち着いてから報告したと考えれば、時期としては不自然ではありません。",
         "もちろん、こじはるは出産の時期を明かしていないので、これはあくまで時期から考えた可能性のひとつです。")
out += p("本人は「無事に出産を迎えてから伝えたかった」と話しています。",
         "大事な時期を静かに過ごして、落ち着いてから報告するという選択だったのでしょう。",
         "答え合わせをするよりも、今はリハ映像を見返しながら、ファンとしてお祝いしたいところですね。")

# ---- プロフィール ----
out += h2("小嶋陽菜のプロフィール")
out += table(None, [
    ("<strong>名前</strong>", "小嶋陽菜(こじま はるな)"),
    ("<strong>愛称</strong>", "こじはる"),
    ("<strong>生年月日</strong>", "1988年4月19日(38歳)"),
    ("<strong>出身地</strong>", "埼玉県"),
    ("<strong>経歴</strong>", "2005年にAKB48の1期生として加入、2017年に卒業"),
    ("<strong>現在</strong>", "モデル・実業家。株式会社heart relationのCCO、ブランド「Her lip to」をプロデュース"),
])
out += p("こじはるはAKB48の1期生で、2008年には高橋みなみ・峯岸みなみとのユニット「ノースリーブス」としても活動しました。",
         "2017年にグループを卒業してからは、モデルとして活動しながら、2018年にライフスタイルブランド「Her lip to」を立ち上げています。",
         "今では会社のCCOとしてブランドを率いる実業家としても知られています。")

# ---- まとめ ----
out += h2("まとめ")
items = [
    "小嶋陽菜は2026年11月7日に結婚と第1子出産をXとInstagramで発表",
    "お相手・出産時期・性別は非公表(お相手は一般男性と報道)",
    "2025年12月のAKB48 20周年武道館リハで「RIVER」の衣装が入らないハプニング",
    "その様子は2026年3月6日公開の本人のYouTube動画で見られる",
    "リハーサル時点のことは本人にしかわからず、時期は明かされていない",
]
out += html(f'<div style="border:1px solid {A};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">'
            + "".join(f'<p style="margin:{"0" if i == 0 else "6px 0 0 0"};">{CHK}{t}</p>' for i, t in enumerate(items)) + "</div>")
out += p("こじはる、結婚と出産おめでとうございます！",
         "まだ見ていない人は、武道館リハの裏側動画で、OGメンバーとわちゃわちゃするこじはるをチェックしてみてください。")

sys.path.insert(0, os.path.join(REPO, "tools"))
from honorific import add_san  # noqa: E402
out = add_san(out, "ko1keyz", ["小嶋陽菜", "こじはる", "高橋みなみ", "峯岸みなみ", "指原莉乃", "柏木由紀", "横山由依"])
out = out.replace("小嶋陽菜(こじはるさん)", "小嶋陽菜さん(こじはる)").replace("小嶋陽菜さん 公式YouTube", "小嶋陽菜 公式YouTube")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(out)
print(OUT, len(out))
if "--build-only" in sys.argv:
    sys.exit()

# ================= upload =================
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
    jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": "小嶋陽菜 結婚と出産を発表 武道館リハの衣装エピソード"})
    state["eyecatch"] = m["id"]
    save()
    jpost(f"/wp-json/wp/v2/posts/{state['post']}", {"featured_media": state["eyecatch"]})
po = req(f"/wp-json/wp/v2/posts/{state['post']}?context=edit", method="GET")
print(po["id"], po["status"], po["author"], po["categories"], po["featured_media"], po["title"]["raw"])
print(f"{BASE}/?p={po['id']}")
