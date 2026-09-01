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

JP_POST_ID = 12030
JP_SLUG = "how-many-piercings-do-ko1keyz"
EYECATCH_MEDIA_ID = 12031  # JP版と共通(英語専用アイキャッチは作らない)
CHART_IMG = ROOT / "images" / "ko1keyz_piercing_count_chart_en.png"


def upload_media_from_file(path: Path, filename: str, content_type: str = "image/png"):
    headers = {
        **HEADERS_AUTH,
        "Content-Type": content_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=path.read_bytes())
    r.raise_for_status()
    return r.json()


chart_media = upload_media_from_file(CHART_IMG, "ko1keyz_piercing_count_chart_en.png")
print("chart_media", chart_media["id"])


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


chart_html = "<!-- wp:html -->\n" + build_img_html(
    chart_media,
    "Chart of how many ear piercings each of the 12 KO1KEYZ members has, both ears combined",
    "Compiled from fan observations shared on X. Numbers are the total for both ears.",
) + "\n<!-- /wp:html -->"


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


EMOJI_URL = "https://chomoand-1.com/summary-of-ko1keyz-member-emoj-10560"
CHEMI_URL = "https://chomoand-1.com/ko1keyz-chemi-names-11773"
SHOE_URL = "https://chomoand-1.com/what-are-the-shoe-sizes-of-ko1-11551"
RYUJI_URL = "https://chomoand-1.com/is-ryuji-left-handed-investiga-11388"

title = "How Many Piercings Do KO1KEYZ Members Have? TOWA Leads With 5"

blocks = []

blocks.append(p([
    "KO1KEYZ is a group where ear piercings really show each member's personal style.",
    "A post that went around on X, listing every member's piercing spots ear by ear, says <strong>TOWA (Towa Hamada) has the most at 5, followed by DAIKI (Daiki Kato) with 4 and KOSUKE (Kosuke Terui) with 3</strong>.",
    "In this article we lay out how many piercings all 12 members have, with a left/right breakdown, plus the designs that fans have actually spotted — star studs, gold hoops and more.",
]))

blocks.append(titlebox("What this article covers", [
    "How many piercings each of the 12 members has (with a left/right ear breakdown)",
    "Which members have the most, and which have none",
    "Spotted designs such as KOSUKE's star piercing",
]))

blocks.append(h2("How many piercings do KO1KEYZ members have? All 12"))
blocks.append(minibox('<p style="margin:0;"><strong>TOWA has the most at 5, then DAIKI with 4 and KOSUKE with 3.</strong>KEITO, RYUJI, YOSHIKI and YUKI have 2 each, and the remaining 5 have none.</p>'))
blocks.append(p([
    "The starting point is a post shared on X in late August 2026 that went through each member's ears one by one and marked where the piercing holes are.",
    "Cross-checking that against the debut single's artist photos and how their ears look in lives and streams, the counts break down like this.",
]))
blocks.append(chart_html)
blocks.append(p([
    "With the left/right ear breakdown included, the full list looks like this.",
]))
blocks.append(table_block(
    ["Member", "Right ear", "Left ear", "Total"],
    [
        ["TOWA (Towa Hamada)", "2", "3", "5"],
        ["DAIKI (Daiki Kato)", "2", "2", "4"],
        ["KOSUKE (Kosuke Terui)", "1", "2", "3"],
        ["KEITO (Keito Ono)", "1", "1", "2"],
        ["RYUJI (Ryuji Sugiyama)", "1", "1", "2"],
        ["YUKI (Yui Goto)", "1", "1", "2"],
        ["YOSHIKI (Yoshiki Yada)", "1", "1", "2"],
        ["ISSA (Issa Yanagiya)", "0", "0", "0"],
        ["YURA (Yura Abe)", "0", "0", "0"],
        ["RYOGA (Ryoga Iizuka)", "0", "0", "0"],
        ["SIYOUNG (Park Si-young)", "0", "0", "0"],
        ["SHINHAENG (Oh Shin-haeng)", "0", "0", "0"],
    ],
))
blocks.append(p([
    f'<strong><span class="swl-marker mark_green" style="font-size:1.15em;">Only TOWA has a cartilage (helix) piercing, giving him 3 on the left ear and 2 on the right for a total of 5</span></strong>, well clear of the rest.',
    "In a group where 1–2 is the norm, TOWA, DAIKI and KOSUKE make up the more heavily pierced trio.",
]))
blocks.append(p([
    "That said, camera angles make it hard to tell which ear is which in some shots, and the original poster admitted they weren't sure about parts of YOSHIKI, YURA and YUKI.",
    "So treat the exact numbers as something that could still shift a little.",
]))

blocks.append(h2("Who has the most? TOWA, DAIKI and KOSUKE"))
blocks.append(minibox('<p style="margin:0;"><strong>The top three are TOWA (5), DAIKI (4) and KOSUKE (3).</strong>All three have multiple holes, and the pieces they wear are well known too.</p>'))
blocks.append(p([
    "<strong>TOWA (Towa Hamada)</strong> has 3 on his left ear and 2 on his right.",
    "He has holes in the cartilage as well as the lobe, making him the only member with 5.",
    "In selfie off-shots he usually wears small silver studs or hoops, and pairs them with rings and a chain necklace to keep everything in silver — a look that has become his signature.",
]))
blocks.append(p([
    "<strong>DAIKI (Daiki Kato)</strong> has 2 on each side for a total of 4.",
    "He listed <strong>“get more piercings”</strong> as one of his goals before the group's Korea shows in a post on X, so the number could well go up.",
    f'In one mid-July outfit, fans noticed he had matched his piercings and clothes to the colors of <a href="{CHEMI_URL}" target="_blank" rel="noopener">“Dekaneko,”</a> his pairing nickname with YOSHIKI.',
]))
blocks.append(p([
    "<strong>KOSUKE (Kosuke Terui)</strong> has 1 on his right ear and 2 on his left, for 3 in total.",
    'The <strong><span class="swl-marker mark_pink">star-shaped piercing</span></strong> he wore in the debut single’s artist photo became known among fans as his “star piercing,” with lots of people saying they wanted to track down the same one.',
    f'Together with his red member color, KOSUKE’s <a href="{EMOJI_URL}" target="_blank" rel="noopener">member emoji is also a star (\U0001f31f)</a>, so the star piercing is turning into a trademark.',
]))

blocks.append(h2("Who has two each? RYUJI, KEITO, YOSHIKI and YUKI"))
blocks.append(minibox('<p style="margin:0;"><strong>RYUJI, KEITO, YOSHIKI and YUKI each have one per ear, for 2.</strong>RYUJI in particular swaps his out often.</p>'))
blocks.append(p([
    "<strong>RYUJI (Ryuji Sugiyama)</strong> has one hole in each ear.",
    "In the debut single's artist photo he layered a piercing with an ear cuff, and fans list “the piercing and ear cuff” among his best features.",
    "He also changes them out a lot — switching from silver to gold at times — with fans spotting “his piercings have gone properly gold now” in an off-shot playing with his dog, or reacting on days he takes his usual pair out.",
]))
blocks.append(p([
    "<strong>KEITO (Keito Ono)</strong> also has one per ear for 2, mostly plain silver studs.",
    "<strong>YOSHIKI (Yoshiki Yada)</strong> appears to have one per ear, but the hole on his right ear was marked “not sure” even in the observation post, so only one is clearly confirmed.",
    "<strong>YUKI (Yui Goto)</strong> has one per ear for 2 as well; an August 2026 photo showed him wearing a piercing, drawing comments that he “has the looks and the piercings.”",
]))

blocks.append(h2("Which members have no piercings? Five of them"))
blocks.append(minibox('<p style="margin:0;"><strong>ISSA, YURA, RYOGA, SIYOUNG and SHINHAENG currently have no visible piercing holes.</strong></p>'))
blocks.append(p([
    "The list lines up with members who had fewer chances to get pierced earlier on — ISSA (Issa Yanagiya), who focused on baseball, RYOGA (Ryoga Iizuka), who focused on soccer, and Korean members SIYOUNG (Park Si-young) and SHINHAENG (Oh Shin-haeng).",
    "It's entirely possible that some of them will get piercings after debut to match their makeup or stage outfits.",
    "RYUJI's own piercing colors and counts were different early in his activities, so it's best to read this list as a snapshot from autumn 2026.",
]))

blocks.append(titlebox("Summary", [
    "TOWA has the most piercings — 5 in total, including a cartilage piercing",
    "DAIKI has 4 and KOSUKE has 3; KEITO, RYUJI, YOSHIKI and YUKI have 2 each",
    "ISSA, YURA, RYOGA, SIYOUNG and SHINHAENG have no visible piercing holes",
    "Designs vary by member too, from KOSUKE's star studs to RYUJI's gold pieces and ear cuff",
]))
blocks.append(p([
    "Look at their ears and the members' tastes come through more clearly than you'd expect — TOWA keeping everything silver, KOSUKE making the star his trademark.",
    "Next time you watch a live clip or an artist photo, give their ears a closer look too!",
]))

blocks.append(minibox(f'''<p style="margin:0 0 8px 0;"><strong>We cover KO1KEYZ in more detail in other posts on this blog.</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{EMOJI_URL}" target="_blank" rel="noopener">A rundown of all 12 members' emoji and their meanings (Japanese)</a></li>
<li><a href="{SHOE_URL}" target="_blank" rel="noopener">What are KO1KEYZ members' shoe sizes? Revealed at the SHINSEKAI costume exhibit</a></li>
<li><a href="{RYUJI_URL}" target="_blank" rel="noopener">Is RYUJI left-handed? Investigating the ambidextrous theory</a></li>
<li><a href="{CHEMI_URL}" target="_blank" rel="noopener">A guide to KO1KEYZ pairing nicknames: what are “Dekaneko” and “Towasuke”?</a></li>
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

(ROOT / "tmp_ko1keyz_piercings_en_postid.txt").write_text(str(post["id"]), encoding="utf-8")
