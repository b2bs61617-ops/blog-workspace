# -*- coding: utf-8 -*-
"""KO1KEYZ メンバーの50m走タイムまとめ記事 (chomoand-1.com)

元ネタ: 2026-09-05 関西オフライントーク会レポ(X)
  https://x.com/kaibun323/status/2096181192227946737
  https://x.com/HACHIWAREtoGOTO/status/2096151845182075045
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
YUKI_WIKI_URL = "https://chomoand-1.com/yu-ki-wiki-278"

# 兄弟記事(運転免許記事)の下書きURL。作成後にここを埋めて再実行
SIBLING_LICENSE_URL = "https://chomoand-1.com/?p=12446"

ACCENT = "#8a8378"
BORDER = "#ded9d2"
BG = "#f8f6f4"


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


def notebox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def time_table(rows):
    """rows: (member, time, note)"""
    head = (
        f'<tr>'
        f'<th style="background:{ACCENT};color:#fff;font-weight:bold;text-align:left;border:1px solid #d8d2c9;padding:9px 12px;">メンバー</th>'
        f'<th style="background:{ACCENT};color:#fff;font-weight:bold;text-align:left;border:1px solid #d8d2c9;padding:9px 12px;">50m走タイム</th>'
        f'<th style="background:{ACCENT};color:#fff;font-weight:bold;text-align:left;border:1px solid #d8d2c9;padding:9px 12px;">補足</th>'
        f'</tr>'
    )
    body = [head]
    for i, (m, t, note) in enumerate(rows):
        bg = "#ffffff" if i % 2 == 0 else BG
        body.append(
            f'<tr>'
            f'<td style="background:{bg};border:1px solid #e4e0da;padding:9px 12px;font-weight:bold;">{m}</td>'
            f'<td style="background:{bg};border:1px solid #e4e0da;padding:9px 12px;">{t}</td>'
            f'<td style="background:{bg};border:1px solid #e4e0da;padding:9px 12px;">{note}</td>'
            f'</tr>'
        )
    return wphtml(
        '<div style="overflow-x:auto;">\n'
        '<table style="border-collapse:collapse;width:100%;font-size:0.95em;line-height:1.5;">\n'
        + "\n".join(body)
        + "\n</table>\n</div>"
    )


title = "KO1KEYZの50m走のタイムは？速いメンバーは誰？"

blocks = []

blocks.append(p([
    "KO1KEYZのメンバーは、50メートル走がどのくらい速いのか。",
    "2026年9月5日(土)に関西で開かれたデビュー記念のメンバー個別オフライントーク会で、メンバーの50m走のタイムが話題になりました。",
    "判明しているのは6人ぶんで、<strong>ISSAとYOSHIKIが6.2秒前後、DAIKI・YUKIが6.3秒、KOSUKEが6.4秒</strong>、そして<strong>TOWAは「7秒台」</strong>。",
    "多くが6秒台前半で、成人男性の平均タイムをはっきり上回る数字です。",
]))

blocks.append(p([
    "この記事では、判明しているメンバーのタイムを一覧で紹介し、一般的な平均タイムと比べてどのくらい速いのか、背景にある各メンバーのスポーツ経歴もあわせて見ていきます。",
    "なお、タイムはトーク会に参加したファンの報告にもとづくもので、レポートによってYOSHIKIの数値が6.2秒と6.3秒に分かれるなど、多少のばらつきがあります。",
]))

blocks.append(titlebox("この記事でわかること", [
    "判明しているメンバーの50m走タイム",
    "一般的な50m走の平均タイムとの比較",
    "速さの背景にあるメンバーのスポーツ経歴",
]))

blocks.append(h2("KO1KEYZメンバーの50m走タイム一覧"))
blocks.append(p([
    "このオフライントーク会は、メンバーと1対1で短時間だけ会話できる企画でした。",
    "そのなかで「50m走が速いらしい」という話が出て、具体的な秒数を教えてくれたメンバーがいたことから、レポートを通じてタイムが広まっています。",
    "名前が挙がっていたのは、次の6人です。",
    "残る6人のタイムは、今のところ公表されていません。",
]))
blocks.append(time_table([
    ("ISSA(柳谷伊冴)", "6.2秒", "野球経験者"),
    ("YOSHIKI(矢田佳暉)", "6.2〜6.3秒", "レポートにより数値に差"),
    ("DAIKI(加藤大樹)", "6.3秒", "2TOPの一角"),
    ("YUKI(後藤結)", "6.3秒", "野球・バレー経験者"),
    ("KOSUKE(照井康祐)", "6.4秒", "最年少クラス"),
    ("TOWA(濱田永遠)", "7秒台", "グループ最年少級"),
]))
blocks.append(p([
    "こうして並べてみると、6.2秒から6.4秒のあいだにほとんどのメンバーが収まっているのが分かります。",
    "0.2秒の差はあるものの、6人中5人が6秒台前半という、かなりそろった数字です。",
    "TOWAだけ「7秒台」と一段のんびりした数字ですが、これはグループでも最年少級の19歳であることを踏まえると、決して遅いわけではありません。",
]))

blocks.append(h2("一般的な50m走の平均タイムと比べると？"))
blocks.append(p([
    "スポーツ庁の体力・運動能力調査(新体力テスト)によると、20〜24歳の男性の50m走の平均は、おおむね7.4秒前後です。",
    "この数字を基準にすると、6秒台前半というのは高校・大学の運動部でも通用するレベルの走力にあたります。",
    "参考までに、年代別のおおまかな平均タイムの目安を並べておきます。",
]))
blocks.append(wphtml(
    '<div style="overflow-x:auto;">\n'
    '<table style="border-collapse:collapse;width:100%;font-size:0.95em;line-height:1.5;">\n'
    f'<tr><th style="background:{ACCENT};color:#fff;font-weight:bold;text-align:left;border:1px solid #d8d2c9;padding:9px 12px;">区分</th>'
    f'<th style="background:{ACCENT};color:#fff;font-weight:bold;text-align:left;border:1px solid #d8d2c9;padding:9px 12px;">50m走の平均</th>'
    f'<th style="background:{ACCENT};color:#fff;font-weight:bold;text-align:left;border:1px solid #d8d2c9;padding:9px 12px;">備考</th></tr>\n'
    f'<tr><td style="background:#ffffff;border:1px solid #e4e0da;padding:9px 12px;">中学2年生 男子</td><td style="background:#ffffff;border:1px solid #e4e0da;padding:9px 12px;">約8.0秒</td><td style="background:#ffffff;border:1px solid #e4e0da;padding:9px 12px;">新体力テストの平均</td></tr>\n'
    f'<tr><td style="background:{BG};border:1px solid #e4e0da;padding:9px 12px;">高校2年生 男子</td><td style="background:{BG};border:1px solid #e4e0da;padding:9px 12px;">約7.4秒</td><td style="background:{BG};border:1px solid #e4e0da;padding:9px 12px;">新体力テストの平均</td></tr>\n'
    f'<tr><td style="background:#ffffff;border:1px solid #e4e0da;padding:9px 12px;">20〜24歳 男性</td><td style="background:#ffffff;border:1px solid #e4e0da;padding:9px 12px;">約7.4秒前後</td><td style="background:#ffffff;border:1px solid #e4e0da;padding:9px 12px;">新体力テストの平均</td></tr>\n'
    f'<tr><td style="background:{BG};border:1px solid #e4e0da;padding:9px 12px;font-weight:bold;">KO1KEYZ(判明分)</td><td style="background:{BG};border:1px solid #e4e0da;padding:9px 12px;font-weight:bold;">6.2〜7秒台</td><td style="background:{BG};border:1px solid #e4e0da;padding:9px 12px;">6人中5人が6秒台前半</td></tr>\n'
    '</table>\n</div>'
))
blocks.append(p([
    "陸上競技のタイム換算でいうと、50mで6.2秒はおおよそ100mで12秒前後に相当します。",
    "部活動でいえば短距離のレギュラー級で、学生アスリートとしてはっきり「速い」と言える部類です。",
    "TOWAの「7秒台」も平均前後の数字で、成長途中の年齢を考えれば十分に健闘しています。",
]))
blocks.append(p([
    "KO1KEYZはパフォーマンスを重視するグループで、日々のダンスレッスンで下半身をよく使っています。",
    "そうした日常的な運動量の多さも、全体的に走力が高いことの一因になっているとみられます。",
]))

blocks.append(h2("速さの背景にあるメンバーのスポーツ経歴"))
blocks.append(p([
    "6秒台前半という数字は、体を動かしてきた下地があってこそのものです。",
    "タイムが判明したメンバーを中心に、これまでのスポーツ経歴を振り返ってみます。",
]))
blocks.append(p([
    "<strong>ISSA(柳谷伊冴)</strong>は、公式のコンセプトフォトで野球ボールを手にしていたことからも分かるとおり、野球経験者です。",
    "走塁やベースランニングで鍛えた瞬発力が、6.2秒という数字に表れているとみられます。",
]))
blocks.append(p([
    "<strong>YUKI(後藤結)</strong>は、小学生時代に野球を6年間続け、中学ではバレーボール部に所属していた本格的なスポーツ少年でした。",
    "ビーチバレーで全国大会に出場した経験もあり、運動神経の高さはファンの間でもよく知られています。",
    "6.3秒というタイムも、その下地があってこそと言えそうです。",
]))
blocks.append(p([
    "<strong>RYOGA(飯塚亮賀)</strong>は、コンセプトフォトでサッカーボールを持っており、サッカー経験者です。",
    "今回タイムそのものは公表されていませんが、身のこなしの軽さには定評があります。",
]))
blocks.append(p([
    "<strong>DAIKI(加藤大樹)</strong>・<strong>YOSHIKI(矢田佳暉)</strong>・<strong>KOSUKE(照井康祐)</strong>は、特定の競技経歴が大きく取り上げられているわけではありません。",
    "それでもそろって6秒台の数字を出しており、地力の高さがうかがえます。",
]))

blocks.append(h2("まとめ"))
blocks.append(wphtml(f'''<div style="border:2px solid {ACCENT};border-radius:8px;background:rgba(138,131,120,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; 9月5日のオフライントーク会で、6人ぶんの50m走タイムが語られた<br>
&#10003; ISSA・YOSHIKIが6.2秒前後、DAIKI・YUKIが6.3秒、KOSUKEが6.4秒、TOWAは7秒台<br>
&#10003; 20〜24歳男性の平均は約7.4秒。6秒台前半は運動部レベルの速さ<br>
&#10003; ISSAは野球、YUKIは野球・バレー、RYOGAはサッカーの経験者<br>
&#10003; タイムはファンの報告にもとづくもので、YOSHIKIは6.2秒と6.3秒で報告が分かれている
</p>
</div>'''))
blocks.append(p([
    "スポーツ経歴のあるメンバーが多いことは知られていましたが、具体的な数字が出てくると速さがより実感できます。",
    "残る6人のタイムや、関東会場のトーク会で新しい情報が出てきたら、この記事にも追記していきます。",
]))

_rel = [
    f'<li><a href="{REPORT_URL}" target="_blank" rel="noopener">KO1KEYZオフライントーク会(関西)のレポまとめ記事</a></li>',
]
if not SIBLING_LICENSE_URL.startswith("__"):
    _rel.append(f'<li><a href="{SIBLING_LICENSE_URL}" target="_blank" rel="noopener">KO1KEYZメンバーの運転免許の取得状況をまとめた記事</a></li>')
_rel.append(f'<li><a href="{YUKI_WIKI_URL}" target="_blank" rel="noopener">運動神経ばつぐんのYUKI(後藤結)のプロフィールをまとめた記事</a></li>')
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


SUMMARY = ("2026年9月5日のKO1KEYZオフライントーク会で語られた、メンバーの50m走のタイムを紹介。"
           "ISSA・YOSHIKIが6.2秒前後、DAIKI・YUKIが6.3秒、KOSUKEが6.4秒、TOWAは7秒台と、一般平均よりかなり速い数字です。")

EXISTING_POST_ID = 12449
EXISTING_EYECATCH_MEDIA_ID = 12450

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
    slug = get_slug(title, "ko1keyz-50m-sprint-time")
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
    EYECATCH_PATH = ROOT / "images" / "ko1keyz_50m_time_eyecatch.png"
    subprocess.run([
        sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
        "--top", "50m走のタイムは？",
        "--main", "KO1KEYZ",
        "--bottom", "6秒台前半が続出！",
        "--out", str(EYECATCH_PATH),
        "--seed", str(post["id"]),
    ], check=True)

    eyecatch_media = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={
            **HEADERS_AUTH,
            "Content-Type": "image/png",
            "Content-Disposition": 'attachment; filename="ko1keyz_50m_time_eyecatch.png"',
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

(ROOT / "tmp_ko1keyz_50m_time_postid.txt").write_text(str(post["id"]), encoding="utf-8")
print("DONE")
print("JP:", post["id"], post.get("link"))
