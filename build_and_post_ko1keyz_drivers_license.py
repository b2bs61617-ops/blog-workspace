# -*- coding: utf-8 -*-
"""KO1KEYZ 12人の運転免許の取得状況まとめ記事 (chomoand-1.com)

元ネタ: 2026-09-05 関西オフライントーク会レポ(X)
  https://x.com/kaibun323/status/2096181192227946737
関西オフライントーク会シリーズのスピンオフ。まとめ記事=post 12373。
"""
import json, os, re, base64, urllib.request, urllib.parse, subprocess, sys
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
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
WP_USER = ENV["WP_KOIKEYS_USERNAME"]
WP_PASS = ENV["WP_KOIKEYS_APP_PASSWORD"]
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

REPORT_URL = "https://chomoand-1.com/?p=12373"
PROFILE_URL = "https://chomoand-1.com/profile-12-9725"
SRC_TWEET = "https://x.com/kaibun323/status/2096181192227946737"
SRC_CONCEPT_PHOTO = "https://x.com/m_yoshiki_y/status/2083762494775214250"

# 本文画像(コンセプトフォトの複数人カット)。一度アップしたらIDを入れて再アップを防ぐ
BODY_IMG_PATH = ROOT / "images" / "ko1keyz_concept_group2.jpg"
EXISTING_BODY_MEDIA_ID = 12458

# 兄弟記事(50m走タイム記事)の下書きが出来たらここにURLを入れて再実行
SIBLING_50M_URL = "https://chomoand-1.com/?p=12449"

ACCENT = "#8a8378"
BORDER = "#ded9d2"
BG = "#f8f6f4"
TDBG = "#f3f1ee"


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def p(sentences):
    return f"<!-- wp:paragraph -->\n<p>" + "<br>\n".join(sentences) + "</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def titlebox(ttl, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def listbox(items):
    lis = "\n".join(f'<li style="margin:0 0 8px 0;">{t}</li>' for t in items[:-1])
    lis += f'\n<li style="margin:0;">{items[-1]}</li>'
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<ul style="margin:0;padding-left:1.3em;">
{lis}
</ul>
</div>''')


def notebox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def upload_media(path, filename, content_type="image/jpeg"):
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HEADERS_AUTH, "Content-Type": content_type,
                 "Content-Disposition": f'attachment; filename="{filename}"'},
        data=path.read_bytes(),
    )
    r.raise_for_status()
    return r.json()


def build_img_html(m, alt, src_url):
    md = m["media_details"]
    sizes = md.get("sizes", {})
    full_url, full_w, full_h = m["source_url"], md["width"], md["height"]
    large = sizes.get("large", {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    iw = large["width"]
    ih = int(iw * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {full_w}w'
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{large["source_url"]}" alt="{alt}" width="{iw}" height="{ih}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {iw}px) 100vw, {iw}px">
<figcaption style="text-align:center;font-size:12px;">出典:<a href="{src_url}" target="_blank" rel="noopener">{src_url}</a>(コンセプトフォトの二次拡散)</figcaption>
</figure>''')


if EXISTING_BODY_MEDIA_ID:
    _bm = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{EXISTING_BODY_MEDIA_ID}", headers=HEADERS_AUTH).json()
else:
    _bm = upload_media(BODY_IMG_PATH, "ko1keyz_concept_group2.jpg")
print("body image media id:", _bm["id"])
group_img = build_img_html(
    _bm,
    "KO1KEYZのコンセプトフォト(SHINHAENG・SIYOUNG・TOWA・YOSHIKI・YUKI・YURA)",
    SRC_CONCEPT_PHOTO,
)


def status_table(rows):
    """rows: (member, age, status)"""
    head = (
        f'<tr>'
        f'<th style="background:{ACCENT};color:#fff;font-weight:bold;text-align:left;border:1px solid #d8d2c9;padding:9px 12px;">メンバー</th>'
        f'<th style="background:{ACCENT};color:#fff;font-weight:bold;text-align:left;border:1px solid #d8d2c9;padding:9px 12px;">年齢<br><span style="font-weight:normal;font-size:0.85em;">(2026年9月時点)</span></th>'
        f'<th style="background:{ACCENT};color:#fff;font-weight:bold;text-align:left;border:1px solid #d8d2c9;padding:9px 12px;">運転免許</th>'
        f'</tr>'
    )
    body = [head]
    for i, (m, age, st) in enumerate(rows):
        bg = "#ffffff" if i % 2 == 0 else BG
        body.append(
            f'<tr>'
            f'<td style="background:{bg};border:1px solid #e4e0da;padding:9px 12px;font-weight:bold;">{m}</td>'
            f'<td style="background:{bg};border:1px solid #e4e0da;padding:9px 12px;">{age}</td>'
            f'<td style="background:{bg};border:1px solid #e4e0da;padding:9px 12px;">{st}</td>'
            f'</tr>'
        )
    return wphtml(
        '<div style="overflow-x:auto;">\n'
        '<table style="border-collapse:collapse;width:100%;font-size:0.95em;line-height:1.5;">\n'
        + "\n".join(body)
        + "\n</table>\n</div>"
    )


title = "KO1KEYZで運転免許があるのは誰？12人の取得状況！"

blocks = []

blocks.append(p([
    "KO1KEYZの12人のなかで、車の運転免許を持っているのは誰なのか。",
    "ファンの間でたびたび話題にのぼる、素朴な疑問です。",
    "先に結論をお伝えすると、現時点で<strong>免許を持っているとみられるのはYOSHIKI・ISSA・RYOGA・RYUJI・KEITOの5人</strong>。",
    "SIYOUNGとYURAは「持っていない」と語っており、最年少のTOWA・YUKI・KOSUKEもまだのようです。",
    "DAIKIとSHINHAENGについては、取得しているかどうかが公表されていません。",
]))

blocks.append(p([
    "この記事では、2026年9月5日(土)に関西で開かれたデビュー記念のメンバー個別オフライントーク会などで語られた内容をもとに、12人ぶんの取得状況を整理していきます。",
    "なお、ここで扱う情報は公式にまとめて発表されたものではなく、メンバーがトーク会やラジオ、雑誌などで少しずつ話してきた内容にもとづくものです。",
]))

blocks.append(titlebox("この記事でわかること", [
    "運転免許を持っているメンバー",
    "持っていない・まだ取得していないメンバー",
    "取得状況が公表されていないメンバー",
    "そもそも運転免許は何歳から取れるのか",
]))

blocks.append(h2("KO1KEYZ12人の運転免許 取得状況一覧"))
blocks.append(p([
    "まずは、現在わかっている範囲で12人ぶんの状況を一覧にまとめます。",
    "年齢は2026年9月時点のものです。",
]))
blocks.append(status_table([
    ("YOSHIKI(矢田佳暉)", "22歳", "あり"),
    ("ISSA(柳谷伊冴)", "21歳", "あり"),
    ("RYOGA(飯塚亮賀)", "21歳", "あり"),
    ("RYUJI(杉山竜司)", "20歳", "あり"),
    ("KEITO(小野慶人)", "26歳", "あり"),
    ("SIYOUNG(パク・シヨン)", "23歳", "なし(本人が言及)"),
    ("YURA(安部結蘭)", "21歳", "なし(本人が言及)"),
    ("TOWA(濱田永遠)", "19歳", "なし(まだとみられる)"),
    ("YUKI(後藤結)", "18歳", "なし(まだとみられる)"),
    ("KOSUKE(照井康祐)", "18歳", "なし(まだとみられる)"),
    ("DAIKI(加藤大樹)", "21歳", "公表なし"),
    ("SHINHAENG(オ・シンヘン)", "22歳", "公表なし"),
]))
blocks.append(group_img)
blocks.append(p([
    "写真はデビュー記念のコンセプトフォトから、SHINHAENG・SIYOUNG・TOWA・YOSHIKI・YUKI・YURAの6人ぶんです。",
    "このうち免許を持っているとみられるのはYOSHIKIのみで、SIYOUNGとYURAは「持っていない」、TOWAとYUKIはまだのようです。",
]))

blocks.append(h2("運転免許を持っているメンバー"))
blocks.append(listbox([
    "YOSHIKI(矢田佳暉)",
    "ISSA(柳谷伊冴)",
    "RYOGA(飯塚亮賀)",
    "RYUJI(杉山竜司)",
    "KEITO(小野慶人)",
]))
blocks.append(p([
    "この5人は、トーク会やこれまでの発言で「免許を持っている」と伝えられているメンバーです。",
    "いずれも20歳を超えており、デビュー準備が本格化する前の期間に、教習所へ通ったり合宿免許で一気に取得したりしていたとみられます。",
    "グループ最年長で26歳のKEITOは、練習生になる以前から免許を持っていた可能性が高いところです。",
    "ただし、免許があるからといって自分の車を持っているとは限りません。",
    "あくまで「運転できる資格がある」という段階だという点は押さえておきたいです。",
]))

blocks.append(h2("持っていない・まだ取得していないメンバー"))
blocks.append(p([
    "SIYOUNGとYURAは、はっきり「持っていない」と話しています。",
    "加えて、最年少のTOWA・YUKI・KOSUKEの3人も、まだ取得していないとみられます。",
]))
blocks.append(p([
    "SIYOUNG(23歳)とYURA(21歳)は、年齢的には十分に取得できます。",
    "それでも取っていないのは、韓国と日本を行き来する活動や日々の多忙さのなかで、まだ必要性を感じていないのかもしれません。",
    "TOWA(19歳)、そしてYUKI・KOSUKE(ともに18歳)は、日本で普通免許が取れる18歳になったばかりです。",
    "とくにKOSUKEとYUKIは2007年12月生まれで、2025年の年末にようやく18歳を迎えたところ。",
    "デビュー準備やレッスンに追われるなかで、教習所に通うまとまった時間を確保するのは難しかったと考えられます。",
]))

blocks.append(h2("取得状況が公表されていないメンバー"))
blocks.append(p([
    "DAIKI(21歳)とSHINHAENG(22歳)については、免許を持っているかどうかがはっきり語られていません。",
    "年齢的にはどちらも取得できる年ですが、トーク会などで話題にのぼらなかったため、この記事では「公表なし」という扱いにしています。",
    "今後、ラジオや雑誌のインタビューで触れられれば、はっきりしてくる部分です。",
]))

blocks.append(h2("そもそも運転免許は何歳から？KO1KEYZの免許事情"))
blocks.append(p([
    "日本では、普通自動車免許は満18歳から取得できます。",
    "教習所に通う場合は2〜3か月、合宿免許なら最短2週間ほどで取れるのが一般的です。",
    "KO1KEYZは12人中10人が19歳以上で、最年少のKOSUKE・YUKIも18歳。",
    "つまり全員が「取ろうと思えば取れる」年齢には達しています。",
]))
blocks.append(p([
    "韓国籍のSIYOUNGとSHINHAENGについても、韓国で運転免許を取れるのは満18歳からです。",
    "韓国で取得した免許は、日本の免許へ切り替える手続き(外国免許切替、いわゆる外免切替)をすれば、そのまま国内でも運転できます。",
    "アイドルやアーティストは移動の多くをマネージャーの運転や新幹線・飛行機でまかなうため、「免許はあるけれど普段は運転しない」というケースも珍しくありません。",
]))
blocks.append(p([
    "一方で、地方出身のメンバーは帰省したときに車が欠かせず、早めに免許を取る傾向があります。",
    "KO1KEYZは茨城・群馬・埼玉・愛知・高知など、生活に車が根づいた地域の出身者が多いグループです。",
    "これから地元トークが増えていくなかで、「実家では運転している」といったエピソードが出てくる可能性もありそうです。",
]))

blocks.append(h2("まとめ"))
blocks.append(wphtml(f'''<div style="border:2px solid {ACCENT};border-radius:8px;background:rgba(138,131,120,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; 運転免許を持っているとみられるのはYOSHIKI・ISSA・RYOGA・RYUJI・KEITOの5人<br>
&#10003; SIYOUNG・YURAは「持っていない」と発言、最年少のTOWA・YUKI・KOSUKEもまだとみられる<br>
&#10003; DAIKI・SHINHAENGは取得状況が公表されていない<br>
&#10003; 日本の普通免許は18歳から。KO1KEYZは12人全員が取得できる年齢にある<br>
&#10003; これらは公式発表ではなく、トーク会などでの本人の発言にもとづく情報
</p>
</div>'''))
blocks.append(p([
    "運転免許の話題は、地元やプライベートが少しだけ垣間見える、意外と奥行きのあるトピックです。",
    "今後のラジオや雑誌インタビューで新しい情報が出てきたら、この記事にも追記していきます。",
]))

_rel = [
    f'<li><a href="{REPORT_URL}" target="_blank" rel="noopener">KO1KEYZオフライントーク会(関西)のレポまとめ記事</a></li>',
]
if not SIBLING_50M_URL.startswith("__"):
    _rel.append(f'<li><a href="{SIBLING_50M_URL}" target="_blank" rel="noopener">KO1KEYZメンバーの50m走のタイムを調べた記事</a></li>')
_rel.append(f'<li><a href="{PROFILE_URL}" target="_blank" rel="noopener">KO1KEYZメンバー全員のプロフィールを紹介した記事</a></li>')
blocks.append(notebox(
    '<p style="margin:0 0 8px 0;"><strong>KO1KEYZについては、このブログの他の記事でも詳しく紹介しています。</strong></p>\n'
    '<ul style="margin:0;padding-left:1.2em;">\n' + "\n".join(_rel) + "\n</ul>"
))

content = "\n\n".join(blocks)
plain_len = len(re.sub(r"<[^>]+>|<!--.*?-->", "", content))
print("content length (chars):", plain_len)
print("title length:", len(title))


def get_slug(title, fallback, maxlen=40):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={urllib.parse.quote(title)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        en = "".join(seg[0] for seg in data[0])
        slug = re.sub(r"[^a-z0-9\s-]", "", en.lower())
        slug = re.sub(r"\s+", "-", slug.strip())
        slug = re.sub(r"-+", "-", slug)[:maxlen].rstrip("-")
        if slug:
            return slug
    except Exception as e:
        print("translate failed, using fallback slug:", e)
    return fallback


SUMMARY = ("2026年9月5日のKO1KEYZオフライントーク会などで語られた、メンバー12人の運転免許の取得状況を整理。"
           "YOSHIKI・ISSA・RYOGA・RYUJI・KEITOが取得済みで、最年少組はこれからとみられます。")

EXISTING_POST_ID = 12446         # 新規作成時はNone。更新するときはIDを入れる
EXISTING_EYECATCH_MEDIA_ID = 12447

if EXISTING_POST_ID:
    payload = {"title": title, "content": content, "status": "draft", "meta": {"jetpack_publicize_message": SUMMARY}}
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_POST_ID}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print("UPDATED POST_ID", post["id"])
else:
    slug = get_slug(title, "ko1keyz-drivers-license-members")
    print("slug:", slug)
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "categories": [66, 62],
        "author": 2,
        "meta": {"jetpack_publicize_message": SUMMARY},
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
print("PREVIEW", f"{WP_URL}/?p={post['id']}")

if not EXISTING_EYECATCH_MEDIA_ID:
    EYECATCH_PATH = ROOT / "images" / "ko1keyz_drivers_license_eyecatch.png"
    subprocess.run([
        sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
        "--top", "運転免許があるのは誰？",
        "--main", "KO1KEYZ",
        "--bottom", "12人の取得状況を調査！",
        "--out", str(EYECATCH_PATH),
        "--seed", str(post["id"]),
    ], check=True)

    eyecatch_media = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={
            **HEADERS_AUTH,
            "Content-Type": "image/png",
            "Content-Disposition": 'attachment; filename="ko1keyz_drivers_license_eyecatch.png"',
        },
        data=EYECATCH_PATH.read_bytes(),
    )
    eyecatch_media.raise_for_status()
    eyecatch_id = eyecatch_media.json()["id"]
    print("eyecatch media id:", eyecatch_id)

    featured_r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps({"featured_media": eyecatch_id, "status": "draft"}).encode("utf-8"),
    )
    featured_r.raise_for_status()
    print("FEATURED_MEDIA set to", eyecatch_id)

(ROOT / "tmp_ko1keyz_drivers_license_postid.txt").write_text(str(post["id"]), encoding="utf-8")
print("DONE")
print("JP:", post["id"], post.get("link"))
