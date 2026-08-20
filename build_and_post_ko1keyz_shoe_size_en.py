# -*- coding: utf-8 -*-
import json, base64, os
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

JP_POST_ID = 11551
JP_SLUG = "what-are-the-shoe-sizes-of-ko1"
IMG_MEDIA_ID = 11549
EYECATCH_MEDIA_ID = 11553

SOURCE_TWEET = "https://x.com/lalabonbondrop/status/2090264614382788644"

img1_media = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{IMG_MEDIA_ID}", headers=HEADERS_AUTH).json()


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


IMG_CAPTION = f'Source:<a href="{SOURCE_TWEET}" target="_blank" rel="noopener">{SOURCE_TWEET}</a>'
img1_html = f"<!-- wp:html -->\n{build_img_html(img1_media, 'Shoe size tags for six KO1KEYZ members, photographed at the HMV SHINSEKAI costume exhibit', IMG_CAPTION)}\n<!-- /wp:html -->"


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

title = "What Are KO1KEYZ Members' Shoe Sizes? Revealed at the SHINSEKAI Costume Exhibit"

blocks = []

blocks.append(p([
    "KO1KEYZ, formed through 'PRODUCE 101 JAPAN SHINSEKAI', keep making headlines every day as their October 7, 2026 debut approaches.",
    "This time, a fan who visited the costume exhibit for their debut single 'SHINSEKAI' at HMV happened to spot the size tags inside the shoes on display, and shared the discovery on X.",
    f"Among the six sizes that could be read, <strong>RYUJI had the largest at 27.5cm, while YOSHIKI and TOWA had the smallest at 26.0cm</strong>.<br>\nIn this article, we've put together each member's shoe size based on what was shared on X.",
]))

blocks.append(titlebox("What this article covers", [
    "Members' shoe sizes revealed at the HMV SHINSEKAI costume exhibit",
    "The shoe brand and model number found on the size tags",
    "Which members' sizes could not be confirmed this time",
]))

blocks.append(h2("Shoe size tags spotted at the HMV SHINSEKAI costume exhibit"))
blocks.append(minibox('<p style="margin:0;"><strong>Where:</strong>HMV (\'SHINSEKAI\' costume exhibit)<br><strong>Shared on:</strong>August 20, 2026</p>'))
blocks.append(p([
    "On August 20, 2026, a fan who visited the 'SHINSEKAI' costume exhibit at HMV posted on X that they could see the size tags inside the shoes on display.",
    "The post included photos of the size tags from the inside of six pairs of shoes, revealing each member's foot size in the process.",
    "According to the poster, this particular exhibit could only be seen at HMV, and they weren't able to check Tower Records due to store hours.",
]))
blocks.append(img1_html)

blocks.append(h2("KO1KEYZ members' shoe sizes"))
blocks.append(minibox('<p style="margin:0;"><strong>Six out of twelve members\' sizes were confirmed.</strong>RYUJI had the largest size at 27.5cm, while YOSHIKI and TOWA had the smallest at 26.0cm.</p>'))
blocks.append(p([
    "Here's what was written on each member's size tag, organized in a table.",
]))
blocks.append(table_block(
    ["Member", "Size (cm)", "Notes"],
    [
        ["YOSHIKI (Kaki Yada)", "26.0", "-"],
        ["TOWA (Towa Hamada)", "26.0", "-"],
        ["SHINHAENG (Oh Sin-haeng)", "26.5", "-"],
        ["ISSA (Issa Yanagiya)", "27.0", "-"],
        ["RYUJI (Ryuji Sugiyama)", "27.5", "Worn without an insole"],
        ["YURA (Yura Abe)", "-", "Size tag wasn't visible in the photo"],
    ],
))
blocks.append(p([
    f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">There\'s a 1.5cm gap between the largest size (RYUJI, 27.5cm) and the smallest (YOSHIKI and TOWA, 26.0cm)</span></strong>.',
]))

blocks.append(h2("The shoe brand and model number were also revealed"))
blocks.append(minibox('<p style="margin:0;"><strong>The shoes are by PUMA, and all six tags shared the same model number, "397447-02."</strong></p>'))
blocks.append(p([
    "A closer look at the size tags shows the shoes are a PUMA model, and all six members' tags share the same model number, \"397447-02.\"",
    "The tags also carry a \"MADE IN CHINA\" mark and what looks like a production date, \"07/25,\" suggesting the group is wearing the same shoe model in different sizes.",
    "It appears the matching shoes were chosen as part of the performance costume for the debut single 'SHINSEKAI', and this tag discovery is a reminder of how much detail goes into styling the group down to their feet.",
]))

blocks.append(h2("What about the other six members?"))
blocks.append(minibox('<p style="margin:0;"><strong>Six members\' sizes were confirmed this time.</strong>KOSUKE, KEITO, DAIKI, RYOGA, YUKI, and SIYOUNG remain unconfirmed.</p>'))
blocks.append(p([
    "The size tags confirmed in this post belonged to YOSHIKI, TOWA, SHINHAENG, ISSA, RYUJI, and YURA.",
    "The remaining six members — KOSUKE, KEITO, DAIKI, RYOGA, YUKI, and SIYOUNG — weren't confirmed, as the original poster wasn't able to check other exhibit locations such as Tower Records.",
    "If any sightings from other venues come up, we'll update this article with the details.",
]))

blocks.append(titlebox("Summary", [
    "Six members' shoe size tags were unexpectedly spotted at the HMV 'SHINSEKAI' costume exhibit",
    "Sizes: YOSHIKI and TOWA at 26.0cm, SHINHAENG at 26.5cm, ISSA at 27.0cm, and RYUJI at 27.5cm",
    "All six wore the same PUMA model (No. 397447-02) in different sizes",
    "The remaining six members (KOSUKE, KEITO, DAIKI, RYOGA, YUKI, SIYOUNG) are still unconfirmed",
]))
blocks.append(p([
    "Little discoveries like this are a fun way to learn something new about KO1KEYZ as they count down to their debut!",
]))

blocks.append(minibox(f'''<p style="margin:0 0 8px 0;"><strong>Check out more KO1KEYZ articles on this blog:</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{HEYAWARI_URL}" target="_blank" rel="noopener">Predicting KO1KEYZ's dorm room assignments!</a></li>
<li><a href="{RYUJI_LEFTHANDED_URL}" target="_blank" rel="noopener">Is RYUJI left-handed? Investigating the ambidextrous theory!</a></li>
<li><a href="{DEBUT_SINGLE_URL}" target="_blank" rel="noopener">When is KO1KEYZ's debut single out? Tracklist and bonus items</a></li>
</ul>'''))

content = "\n\n".join(blocks)

slug = JP_SLUG + "-en"
payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": "draft",
    "categories": [66, 62],
    "author": 2,
    "lang": "en",
    "translations": {"ja": JP_POST_ID},
}
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("EN_POST_ID", post["id"])
print("EN_SLUG", post["slug"])
print("EN_LINK", post.get("link"))

featured_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"featured_media": EYECATCH_MEDIA_ID, "status": "draft"}).encode("utf-8"),
)
featured_r.raise_for_status()
print("FEATURED_MEDIA set to", EYECATCH_MEDIA_ID)

with open(ROOT / "tmp_ko1keyz_shoe_size_en_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
