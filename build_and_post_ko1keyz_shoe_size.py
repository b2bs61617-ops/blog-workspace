# -*- coding: utf-8 -*-
import json, base64, os, re, subprocess, sys, urllib.request, urllib.parse
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

# 出典ツイート(HMVの『新世界』制服展示でシューズのサイズタグが見えたという報告)
SOURCE_TWEET = "https://x.com/lalabonbondrop/status/2090264614382788644"

LOCAL_IMG = ROOT / "tools" / "Xiy" / "posts_20260820_150039_url" / "images" / "post_1_img_1.jpg"


def upload_media_from_file(path: Path, filename: str, content_type: str = "image/jpeg"):
    data = path.read_bytes()
    headers = {
        **HEADERS_AUTH,
        "Content-Type": content_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=data)
    r.raise_for_status()
    return r.json()


print("uploading image...")
img1_media = upload_media_from_file(LOCAL_IMG, "ko1keyz_shoe_size_tags.jpg")
print("img1_media", img1_media["id"])


def build_img_html(media, alt, caption):
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
    return f'''<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>
</figure>'''


IMG_CAPTION = f'出典:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>'
img1_html = f"<!-- wp:html -->\n{build_img_html(img1_media, 'HMVの新世界衣装展示で撮影された、メンバー6人分のシューズサイズタグ', IMG_CAPTION)}\n<!-- /wp:html -->"


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


ACCENT = "#8a8378"
BORDER = "#ded9d2"
BG = "#f8f6f4"


def titlebox(ttl, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</ul>
</div>''')


def minibox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def table_block(headers, rows):
    thead = "".join(f"<td>{h}</td>" for h in headers)
    trows = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr>{thead}</tr>
{trows}
</tbody></table></figure>
<!-- /wp:table -->'''


HEYAWARI_URL = "https://chomoand-1.com/what-is-the-room-allocation-at-11122"
RYUJI_LEFTHANDED_URL = "https://chomoand-1.com/is-ryuji-left-handed-investiga-11388"
DEBUT_SINGLE_URL = "https://chomoand-1.com/when-will-ko1keyzs-debut-singl-10866"

title = "KO1KEYZメンバーの靴サイズは？新世界衣装展示で判明！"

blocks = []

blocks.append(p([
    "『PRODUCE 101 JAPAN 新世界』出身のKO1KEYZは、2026年10月7日のデビューへ向けて日々話題を集めているグループです。",
    "そんな中、HMVで行われているデビューシングル『新世界』の制服(衣装)展示にファンが足を運んだところ、シューズの内側に貼られたサイズタグが偶然見えてしまい、Xで報告されて話題になりました。",
    f"確認できた6人のうち、<strong>もっとも大きいのはRYUJIの27.5cm、もっとも小さいのはYOSHIKIとTOWAの26.0cm</strong>という結果でした。<br>\nこの記事では、Xで報告された内容をもとに、メンバーごとの靴サイズを一覧にまとめます。",
]))

blocks.append(titlebox("この記事でわかること", [
    "HMVの新世界衣装展示で判明したメンバーの靴サイズ",
    "サイズタグから読み取れたシューズのブランド・型番",
    "今回サイズが確認できなかったメンバー",
]))

blocks.append(h2("HMVの新世界衣装展示でシューズのサイズタグが判明"))
blocks.append(minibox('<p style="margin:0;"><strong>目撃場所:</strong>HMV(『新世界』制服展示)<br><strong>報告日:</strong>2026年8月20日</p>'))
blocks.append(p([
    "Xでは2026年8月20日、『新世界』の制服展示をHMVで見てきたというファンから、「新世界の制服展示見にきたら靴のサイズタグが見えたよ」という報告がありました。",
    "投稿には6人分のシューズ内側のサイズタグを撮影した写真が添えられており、メンバーごとの足のサイズがそのまま判明する形になりました。",
    "投稿者によると、この展示が見られるのはHMVのみで、タワーレコードは営業時間の都合で確認できなかったとのことです。",
]))
blocks.append(img1_html)

blocks.append(h2("KO1KEYZメンバーの靴サイズ一覧"))
blocks.append(minibox('<p style="margin:0;"><strong>確認できたのは12人中6人分。</strong>最大はRYUJIの27.5cm、最小はYOSHIKIとTOWAの26.0cmでした。</p>'))
blocks.append(p([
    "サイズタグに書かれていた内容を、メンバーごとに一覧表でまとめました。",
]))
blocks.append(table_block(
    ["メンバー", "サイズ(cm)", "備考"],
    [
        ["YOSHIKI(矢田佳暉)", "26.0", "-"],
        ["TOWA(濱田永遠)", "26.0", "-"],
        ["SHINHAENG(オ・シンヘン)", "26.5", "-"],
        ["ISSA(柳谷伊冴)", "27.0", "-"],
        ["RYUJI(杉山竜司)", "27.5", "インソールなしで着用"],
        ["YURA(安部結蘭)", "-", "サイズタグが写真に写らず未確認"],
    ],
))
blocks.append(p([
    f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">もっとも大きいRYUJI(27.5cm)ともっとも小さいYOSHIKI・TOWA(26.0cm)の間には1.5cmの差</span></strong>があることも分かりました。',
]))

blocks.append(h2("靴のブランド・型番も判明?"))
blocks.append(minibox('<p style="margin:0;"><strong>シューズはPUMA、型番は6人とも共通の「397447-02」でした。</strong></p>'))
blocks.append(p([
    "サイズタグをよく見ると、シューズはPUMAのモデルで、6人とも型番「397447-02」が共通していることが分かります。",
    "タグには「MADE IN CHINA」の表記や「07/25」という生産時期とみられる数字も入っており、同じモデルのシューズをメンバーごとに異なるサイズで履き分けている様子がうかがえます。",
    "デビューシングル『新世界』のパフォーマンス衣装として揃いのシューズを採用していると考えられ、足元までしっかりスタイリングされていることが、今回のタグ確認であらためて分かりました。",
]))

blocks.append(h2("サイズが確認できなかった6人は?"))
blocks.append(minibox('<p style="margin:0;"><strong>今回タグが判明したのは6人。</strong>残るKOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNGは未確認です。</p>'))
blocks.append(p([
    "今回の投稿でサイズタグが確認できたのは、YOSHIKI・TOWA・SHINHAENG・ISSA・RYUJI・YURAの6人分でした。",
    "残るKOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNGの6人については、投稿者も別会場(タワーレコードなど)を確認できていないとのことで、現時点ではサイズが分かっていません。",
    "もし他の会場での目撃情報が出てきたら、この記事でも追ってお伝えします。",
]))

blocks.append(titlebox("まとめ", [
    "HMVの『新世界』制服展示で、6人分のシューズのサイズタグが偶然見えたと話題に",
    "サイズはYOSHIKI・TOWAが26.0cm、SHINHAENGが26.5cm、ISSAが27.0cm、RYUJIが27.5cm",
    "シューズはPUMAの同じモデル(型番397447-02)を全員でサイズ違いで着用",
    "残る6人(KOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNG)のサイズは未確認",
]))
blocks.append(p([
    "こうした細かい発見も、デビューを控えたKO1KEYZの新しい魅力を知るきっかけになりますね!",
]))

blocks.append(minibox(f'''<p style="margin:0 0 8px 0;"><strong>KO1KEYZについては、このブログの他の記事でも詳しく紹介しています。</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{HEYAWARI_URL}" target="_blank" rel="noopener">KO1KEYZ宿舎の部屋割り予想!</a></li>
<li><a href="{RYUJI_LEFTHANDED_URL}" target="_blank" rel="noopener">RYUJIは左利き?両利き説の真相を調査!</a></li>
<li><a href="{DEBUT_SINGLE_URL}" target="_blank" rel="noopener">デビューシングル『KO1KEYZ』はいつ発売?収録曲・特典まとめ</a></li>
</ul>'''))

content = "\n\n".join(blocks)

print("content length (chars):", len(re.sub(r"<[^>]+>|<!--.*?-->", "", content)))


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


SUMMARY = "HMVの『新世界』衣装展示でシューズのサイズタグが偶然見えたと話題に。RYUJIの27.5cmからYOSHIKI・TOWAの26.0cmまで、判明した6人分のサイズと靴のブランドをまとめます。"

slug = get_slug(title, "ko1keyz-members-shoe-size")
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

EYECATCH_PATH = ROOT / "images" / "ko1keyz_shoe_size_eyecatch.png"
subprocess.run([
    sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
    "--top", "メンバーの靴サイズは？",
    "--main", "KO1KEYZ",
    "--bottom", "新世界衣装展示でタグが判明！",
    "--out", str(EYECATCH_PATH),
    "--seed", str(post["id"]),
], check=True)

media_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/media",
    headers={
        **HEADERS_AUTH,
        "Content-Type": "image/png",
        "Content-Disposition": 'attachment; filename="ko1keyz_shoe_size_eyecatch.png"',
    },
    data=EYECATCH_PATH.read_bytes(),
)
media_r.raise_for_status()
EYECATCH_MEDIA_ID = media_r.json()["id"]
print("EYECATCH_MEDIA_ID", EYECATCH_MEDIA_ID)

featured_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"featured_media": EYECATCH_MEDIA_ID, "status": "draft"}).encode("utf-8"),
)
featured_r.raise_for_status()
print("FEATURED_MEDIA set to", EYECATCH_MEDIA_ID)

with open(ROOT / "tmp_ko1keyz_shoe_size_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
with open(ROOT / "tmp_ko1keyz_shoe_size_slug.txt", "w", encoding="utf-8") as f:
    f.write(str(post["slug"]))
with open(ROOT / "tmp_ko1keyz_shoe_size_eyecatch_mediaid.txt", "w", encoding="utf-8") as f:
    f.write(str(EYECATCH_MEDIA_ID))
