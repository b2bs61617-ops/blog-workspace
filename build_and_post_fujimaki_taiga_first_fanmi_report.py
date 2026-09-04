# -*- coding: utf-8 -*-
"""藤牧大雅 初ファンミ レポまとめ記事 (chomoand-1.com / 日プ新世界カテゴリ)"""
import json, base64, os, re, subprocess, sys, urllib.request
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

# ---- 出典・関連リンク --------------------------------------------------------
WIKI_URL = "https://chomoand-1.com/fujimakitaiga_wiki-1025"
FANMI_URL = "https://chomoand-1.com/taiga-no-meeting-10345"
ZENSE_URL = "https://chomoand-1.com/produce101japanshinsekai_zense-2748"
PRTIMES_URL = "https://prtimes.jp/main/html/rd/p/000000537.000141380.html"
SRC_UCHIWA = "https://x.com/_TruTH4me/status/2095440697465958494"
SRC_JYP = "https://x.com/kina32ponponxu/status/2095574733245030805"

UCHIWA_PBS = "https://pbs.twimg.com/media/HRR_u_wbIAA0pHK.jpg?name=orig"
JYP_PBS = "https://pbs.twimg.com/media/HRT6HOcaAAEhLir.jpg?name=orig"

IMG_DIR = ROOT / "images"
IMG_DIR.mkdir(exist_ok=True)


def fetch(url, dest: Path):
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        dest.write_bytes(r.read())
    return dest


UCHIWA_PATH = fetch(UCHIWA_PBS, IMG_DIR / "fujimaki_taiga_first_fanmi_uchiwa.jpg")
JYP_PATH = fetch(JYP_PBS, IMG_DIR / "fujimaki_taiga_first_fanmi_jyp_showcase.jpg")


def upload_media(path: Path, filename: str):
    headers = {
        **HEADERS_AUTH,
        "Content-Type": "image/jpeg",
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=path.read_bytes())
    r.raise_for_status()
    return r.json()


uchiwa_media = upload_media(UCHIWA_PATH, "fujimaki_taiga_first_fanmi_uchiwa.jpg")
jyp_media = upload_media(JYP_PATH, "fujimaki_taiga_first_fanmi_jyp_showcase.jpg")
print("uchiwa media", uchiwa_media["id"], "jyp media", jyp_media["id"])

# ---- ヘルパー --------------------------------------------------------------
ACCENT = "#8a8378"   # 日プ新世界(KO1KEYZ非メンバー)記事のニュートラルなウォームグレー
BORDER = "#ddd9d3"
BG = "#f7f6f4"
TDBG = "#f3f1ee"


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def mk(cls, text):
    return f'<span class="swl-marker {cls}">{text}</span>'


def mkstrong(cls, text):
    return f'<strong><span class="swl-marker {cls}" style="font-size:1.15em;">{text}</span></strong>'


def infotable(ttl, rows):
    tds = "\n".join(
        f'<tr><td style="background:{TDBG};border:1px solid {BORDER};padding:8px 12px;width:32%;">{k}</td>'
        f'<td style="border:1px solid {BORDER};padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{ttl}</p>
<table style="border-collapse:collapse;width:100%;">
{tds}
</table>
</div>''')


def whatbox(ttl, items):
    lis = "\n".join(f'<li style="margin:0 0 8px 0;">{t}</li>' for t in items[:-1])
    lis += f'\n<li style="margin:0;">{items[-1]}</li>'
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


def img_block(media, alt, source_url):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    full_w = media["media_details"]["width"]
    full_h = media["media_details"]["height"]
    large = sizes.get("large", {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    img_src = large["source_url"]
    img_w = large["width"]
    img_h = int(img_w * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {large["source_url"]} {large["width"]}w, {full_url} {full_w}w'
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">出典:{source_url}</figcaption>
</figure>''')


# ---- 本文 ----------------------------------------------------------------
title = "藤牧大雅の初ファンミレポまとめ！内容やゲストは？"

blocks = []

blocks.append(p([
    "『PRODUCE 101 JAPAN 新世界』(日プ新世界)に出演した藤牧大雅さんが、2026年9月3日(木)に東京・有楽町のヒューリックホール東京で<strong>初のファンミーティング</strong>を開催しました。",
    "アルバイト代で会場を押さえた" + mkstrong("mark_yellow", "自費開催・入場無料") + "のイベントながら約900席のホールは満員となり、日プ新世界のポジションバトルで共演した大林悠成さん・山下柊さんもサプライズで登場。Q&Aコーナーでは、NiziUメンバーと同期だったJYP練習生時代の秘話も飛び出しました。",
    "この記事では、当日会場に足を運んだファンのレポをもとに、開催概要・セトリ・ゲスト・Q&Aの内容をまとめます。",
]))

blocks.append(whatbox("この記事でわかること", [
    "初ファンミの開催概要(日時・会場・入場)",
    "セトリとパフォーマンスの内容",
    "サプライズゲストで登場したメンバー",
    "Q&AでのNiziU・JYP練習生時代の秘話",
    "ファンの反応",
]))

blocks.append(h2("藤牧大雅の初ファンミはどんなイベントだった？"))
blocks.append(p([
    "初ファンミは「TAIGA FUJIMAKI FIRST FAN MEETING」と題し、藤牧大雅さんが企画・構成・演出までを一人で手がけたイベントです。",
    "会場費などの経費はオーディションの合間に働いたアルバイト代でまかない、支えてくれたファンへ感謝を直接伝えたいという思いから" + mk("mark_yellow", "入場無料") + "で開催されました。",
    "チケットの受け付けは「BUZZチケ」で行われ、座席は番号による完全ランダム。当日は会場に座席表が貼り出され、ステージには「ありがとう 〜感謝の気持ちを込めて〜」という手書きのメッセージが映し出されました。",
]))
blocks.append(infotable("初ファンミの開催概要", [
    ("開催日", "2026年9月3日(木)"),
    ("会場", "ヒューリックホール東京(東京都千代田区・有楽町)"),
    ("入場料", "無料(本人の貯金による自費開催)"),
    ("チケット受付", "BUZZチケ"),
    ("座席", "番号による完全ランダム(当日発表)"),
    ("内容", "歌・ダンス、Q&A、ゲストコラボ、ハイタッチ会"),
]))
blocks.append(img_block(uchiwa_media,
    "『ありがとう 〜感謝の気持ちを込めて〜』と映し出されたステージとファンプロジェクトのうちわ", SRC_UCHIWA))
blocks.append(p([
    "入場時にはうちわとサイリウムが配られましたが、これらは" + mk("mark_yellow", "ファンダム有志が用意したもの") + "だったことが後から明かされ、「本人だけでなくファン側の準備もすごい」と驚きが広がりました。",
    "うちわは紫地に金色の「Taiga」ロゴと「TAIGA FUJIMAKI 03,09,2026」の文字があしらわれたデザインです。",
]))
blocks.append(wphtml('<iframe src="https://maps.google.com/maps?q=ヒューリックホール東京&t=&z=16&ie=UTF8&iwloc=&output=embed" width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>'))

blocks.append(h2("セトリ・パフォーマンスのレポは？"))
blocks.append(p([
    "ファンミの前半は、藤牧大雅さんのソロステージが中心でした。",
    "Stray Kidsの「MOUNTAINS」「MEGAVERSE」、BOYNEXTDOORの「IF I SAY, I LOVE YOU」などを、キレのあるダンスと豊かな表情で披露しています。",
]))
blocks.append(p([
    "中盤では、練習生仲間との思い出を込めて制作したというオリジナル曲「Island」を披露。",
    "パートナーのパートを客席と一緒に歌う場面もあり、会場が一体となりました。",
]))
blocks.append(p([
    "ラストはStray Kidsの「MIROH」。",
    "藤牧さんが客席をあおって盛り上げ、ゲストの2人も再びステージに戻ってフィナーレを迎えています。",
]))

blocks.append(h2("ゲストは誰？大林悠成・山下柊がサプライズ登場"))
blocks.append(p([
    "スペシャルゲストとして登場したのは、日プ新世界で共に戦った" + mk("mark_yellow", "大林悠成さん(YUSEI)と山下柊さん(SHU)") + "です。",
    "3人は日プ新世界のポジションバトルでINIの「DOMINANCE」を一緒に披露した仲。",
    "当日は、ふだんのレッスンだと思っていたらINIのメンバー本人からサプライズで直接指導を受けて驚いた、という裏話も語られました。",
]))
blocks.append(p([
    "トークのあと、3人は「サビだけダンスチャレンジ」に挑戦し、「Kick」「neko」などの流行曲を次々にカバー。",
    "最後はオーディションで披露した「DOMINANCE」を、あらためて3人で踊りました。",
]))
blocks.append(p([
    "MCを務めたのは、日本テレビ「DayDay.」の虹プロ2特集でナレーションを担当していた松浦マイさん。",
    "虹プロ2の頃から藤牧さんを見てきた人物が司会に立ったことに、「そこまで込みで泣ける」という声も上がりました。",
    "藤牧さんのパートナーだった金田栄都さん(EITO)も応援に駆けつけています。",
]))

blocks.append(h2("Q&AコーナーのレポまとめとNiziU・JYP時代の秘話"))
blocks.append(p([
    "Q&Aコーナーは、事前にInstagramで募った質問に藤牧大雅さんが答える形で進みました。",
    "ファンがまとめたレポによると、韓国語の習得法からアイドルを目指したきっかけ、練習生時代のエピソードまで幅広く語られています。",
]))
blocks.append(p([
    "特に反響が大きかったのが、韓国語をどう覚えたかという質問への答えです。",
    "藤牧さんはNiziUのMIIHIさん・RIMAさんとJYPの同期で、当時は3人一緒に韓国語のレッスンに通っていたものの、2人より覚えるのが遅かったと明かしました。",
    "その後NEXZのユウヒ(ヒュイ)さんが入社して藤牧さんが通訳を任される立場になり、「このままではダメだ」と韓国人の友人と積極的に会話を重ねて一気に上達。",
    "それまではNiziUのMAKOさんに通訳してもらっていたそうです。",
]))
blocks.append(img_block(jyp_media,
    "2019年のJYP練習生ショーケースのポスター。藤牧大雅(TAIGA)やNiziUのMIIHI・RIMA・MAKOらが並ぶ", SRC_JYP))
blocks.append(p([
    "この話に、日プ新世界から藤牧さんを知ったファンからは「JYP同期がNiziU?」と驚く声が続出。",
    "Xでは2019年のJYP練習生ショーケースのポスターが「伝説のJYP画像」として広まり、藤牧さんが当時から実力者と並んでいたことが再注目されました。",
]))
blocks.append(p([
    "そのほかのQ&Aでは、次のような回答が共有されています。",
]))
blocks.append(listbox([
    "<strong>ダンス以外の習い事</strong>:空手・水泳・公文。空手は小学1〜2年生のころ、友達に誘われて始めた。",
    "<strong>アイドルを目指したきっかけ</strong>:東方神起のユンホさんへの憧れ。SMのオーディションを受けて合宿まで進んだが脱落し、その後JYPのグローバルオーディションに合格して入社した。",
    "<strong>JYP入社後のエピソード</strong>:宿舎では料理担当。フレンチトーストを大量に焼いて8人で食べたり、パスタやチャーハンをフライパンごとテーブルに出したりしていた。初めて作ったパスタを塩辛くしてしまったが、ユウヒさんとトモヤさん(NEXZ)が「おいしい」と完食してくれたという。",
    "<strong>行き詰まったときの立て直し方</strong>:終わったことに執着せず、反省だけしっかりして次に切り替える。以前は1回のミスで落ち込んでいたが、切り替えないとアイドルにはなれないと考えるようになった。",
    "<strong>すてきだと思う女性有名人3名</strong>:伊藤あさこさん、NiziUのMAYUKAさん、日本テレビの水卜麻美アナウンサー。笑顔がすてきで思いやりのある、雰囲気のやわらかい人がタイプだという。",
    "<strong>ファンとデートするなら</strong>:ドライブ。虹プロ2のあとに合宿免許で運転免許を取得済みで、遠出して食べ歩きをしながらたくさん話したいとのこと。国内旅行の経験が少なく、北海道や沖縄に行ってみたいとも話した。",
]))

blocks.append(h2("ファンの反応は？"))
blocks.append(p([
    "自費・無料でここまでの規模のイベントを実現したことに、SNSでは「タダなのが信じられない」「感謝を伝えたい気持ちが強すぎる」と胸を打たれる声が目立ちました。",
    "入場者に配られたうちわやサイリウムがファンダム有志の手によるものだと分かると、演者とファンの双方の熱量に感動したという投稿も相次いでいます。",
]))
blocks.append(p([
    "Q&Aで語られたJYP練習生時代の話は、日プ新世界からのファンにとって初耳の情報が多く、「NiziUと同期だったなんて」と驚く声が広がりました。",
    "大林悠成さん・山下柊さんとの「DOMINANCE」再演にも、「ポジションバトルの3人がまた揃った」と沸く反応が見られました。",
]))

blocks.append(h2("まとめ"))
blocks.append(wphtml(f'''<div style="border:2px solid {ACCENT};border-radius:8px;background:rgba(138,131,120,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; 藤牧大雅の初ファンミは2026年9月3日、ヒューリックホール東京で開催<br>
&#10003; 本人の貯金による自費開催・入場無料で、約900席のホールが満員に<br>
&#10003; セトリはStray Kids「MOUNTAINS」「MEGAVERSE」「MIROH」、オリジナル曲「Island」など<br>
&#10003; ゲストは大林悠成(YUSEI)・山下柊(SHU)、MCは松浦マイ、金田栄都も応援に登場<br>
&#10003; Q&AではNiziUのMIIHI・RIMA・MAKOと同期だったJYP練習生時代の秘話を披露
</p>
</div>'''))
blocks.append(p([
    "デビューは逃したものの、支えてくれたファンへ自分にできる形で恩返しをした今回の初ファンミ。",
    "同じ日プ新世界のゲストと肩を並べるステージを見て、これからの活動を現地で追いかけたくなったファンも多かったのではないでしょうか。",
]))
blocks.append(p([
    f'発表の詳細は<a href="{PRTIMES_URL}" target="_blank" rel="noopener">PR TIMESのプレスリリース</a>で確認できます。',
]))
blocks.append(wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">日プ新世界・藤牧大雅の関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{WIKI_URL}" target="_blank" rel="noopener">藤牧大雅のwiki風経歴は？EXPG・JYP出身で虹プロ2やボイプラ2経験者！</a></li>
<li><a href="{FANMI_URL}" target="_blank" rel="noopener">藤牧大雅のファンミーティングは無料！開催日や会場・内容は？</a></li>
<li><a href="{ZENSE_URL}" target="_blank" rel="noopener">【日プ新世界】練習生の前世一覧！元K-POPアイドルや経歴を徹底調査！</a></li>
</ul>
</div>'''))

content = "\n\n".join(blocks)
plain_len = len(re.sub(r"<[^>]+>|<!--.*?-->", "", content))
print("content length (chars):", plain_len)
print("title length:", len(title))

SUMMARY = ("日プ新世界の藤牧大雅が2026年9月3日、ヒューリックホール東京で初のファンミーティングを開催。"
           "バイト代による自費・無料開催で満員、大林悠成・山下柊もサプライズ登場。セトリ、ゲスト、"
           "NiziUと同期だったJYP時代を語ったQ&Aまで、当日のファンレポをまとめました。")

slug = "taiga-fujimaki-first-fan-meeting-report"
payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": "draft",
    "categories": [4],
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

EYECATCH_PATH = ROOT / "images" / "fujimaki_taiga_first_fanmi_report_eyecatch.png"
subprocess.run([
    sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
    "--top", "日プ新世界 藤牧大雅",
    "--main", "初ファンミ レポ",
    "--bottom", "ファンのレポまとめ",
    "--bottom", "内容・ゲストは？",
    "--out", str(EYECATCH_PATH),
    "--seed", str(post["id"]),
], check=True)

media2 = requests.post(
    f"{WP_URL}/wp-json/wp/v2/media",
    headers={
        **HEADERS_AUTH,
        "Content-Type": "image/png",
        "Content-Disposition": 'attachment; filename="fujimaki_taiga_first_fanmi_report_eyecatch.png"',
    },
    data=EYECATCH_PATH.read_bytes(),
)
media2.raise_for_status()
EYECATCH_MEDIA_ID = media2.json()["id"]
print("EYECATCH_MEDIA_ID", EYECATCH_MEDIA_ID)

featured_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"featured_media": EYECATCH_MEDIA_ID, "status": "draft"}).encode("utf-8"),
)
featured_r.raise_for_status()
print("FEATURED_MEDIA set to", EYECATCH_MEDIA_ID)

(ROOT / "tmp_fujimaki_taiga_first_fanmi_report_postid.txt").write_text(str(post["id"]), encoding="utf-8")
(ROOT / "tmp_fujimaki_taiga_first_fanmi_report_ids.txt").write_text(
    f"post={post['id']}\neyecatch={EYECATCH_MEDIA_ID}\nuchiwa={uchiwa_media['id']}\njyp={jyp_media['id']}\nslug={post['slug']}\n",
    encoding="utf-8",
)
