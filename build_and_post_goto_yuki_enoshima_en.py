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

SOURCE_OFFICIAL = "https://x.com/KO1KEYZofficial/status/2090038569876545590"
SOURCE_FACE = "https://x.com/G_YUKI_FACE/status/2090076439425241137"
SOURCE_HOBBYOFF = "https://x.com/hb_hashimoto/status/2083780842472526027"

MEDIA_IDS = {
    "official": 11543,
    "img2": 11544,
    "img3": 11545,
    "img4": 11546,
    "img5": 11547,
    "img6": 11548,
    "img7": 11620,
    "eyecatch": 11550,
}

media_cache = {}
def get_media(key):
    if key not in media_cache:
        media_cache[key] = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{MEDIA_IDS[key]}", headers=HEADERS_AUTH).json()
    return media_cache[key]


def build_img_html(media, alt, source_url):
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
<figcaption style="text-align:center;font-size:12px;">Source: {source_url}</figcaption>
</figure>'''


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


img_official_html = wphtml(build_img_html(get_media("official"), "YUKI (Yui Goto) in his KO1NOTE update photo, with what appears to be Enoshima island in the background", SOURCE_OFFICIAL))
img2_html = wphtml(build_img_html(get_media("img2"), "A wooden deck walkway with reddish railings, with Enoshima visible in the distance", SOURCE_FACE))
img3_html = wphtml(build_img_html(get_media("img3"), "A view of the beach and Enoshima direction from a seaside deck", SOURCE_FACE))
img4_html = wphtml(build_img_html(get_media("img4"), "A wooden walkway inside the facility, with a building and blue sky in the background", SOURCE_FACE))
img5_html = wphtml(build_img_html(get_media("img5"), "YUKI at night in front of a parking lot lined with palm trees, with a blue-lit tower visible in the distance", SOURCE_FACE))
img6_html = wphtml(build_img_html(get_media("img6"), "YUKI at night in front of a classic car, with the same blue-lit tower visible in the background", SOURCE_FACE))
img7_html = wphtml(build_img_html(get_media("img7"), "Three \"Happy Marine\" otter plushes in different colors, stacked on top of each other", SOURCE_HOBBYOFF))


def p(sentences):
    body = "<br>\n".join(sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


ACCENT = "#8a8378"


def capbox(ttl, rows):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ddd9d3;padding:8px 12px;background:#f7f6f4;white-space:nowrap;">{k}</td>'
        f'<td style="border:1px solid #ddd9d3;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:6px;overflow:hidden;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<div style="padding:14px 18px;background:#f7f6f4;">
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>
</div>''')


def minibox(inner):
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f6f4;">
{inner}
</div>''')


def wakaru_box(items, ttl):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:#f7f6f4;">
{lis}
</ul>
</div>''')


title = "KO1KEYZ YUKI's KO1NOTE Photo: Location & Otter Revealed!"

blocks = []

blocks.append(p([
    "KO1KEYZ's YUKI (Yui Goto) updated his official fan club content \"KO1NOTE\" on August 19, 2026, and we took a closer look at the background of the photos he shared.",
    "The photos show the sea, an island silhouette, and what looks like a white tower, and it turns out this is very likely <strong>Enoshima in Fujisawa City, Kanagawa Prefecture — more specifically, the New Enoshima Aquarium (\"Enosui\")</strong>.",
    "In this article, we'll walk through the evidence found in the photos, plus take a look at the \"new family member\" (an otter) that's also been trending alongside the update.",
]))

blocks.append(capbox("KO1NOTE Update Info", [
    ("Update date", "August 19, 2026"),
    ("Member", "YUKI (Yui Goto)"),
    ("Content", "Photo and comment update"),
    ("Where to find it", "\"KO1NOTE\" on the official KO1KEYZ site"),
]))

blocks.append(wakaru_box([
    "What's really in the background of the KO1NOTE photo",
    "Why the location looks like it's the New Enoshima Aquarium (\"Enosui\")",
    "The story behind the trending \"new family member\" otter",
], "What You'll Learn in This Article"))

blocks.append(h2("Let's take a look at the photos from KO1NOTE"))
blocks.append(minibox('<p style="margin:0;"><strong>What was updated:</strong>On August 19, 2026, YUKI shared several photos with the caption "Hi KO1LY! It\'s YUKI!"</p>'))
blocks.append(img_official_html)
blocks.append(p([
    "One of the photos shows YUKI wearing a black New Era cap and carrying a large bag over his shoulder.",
    "Behind him is the sea, with a green island silhouette floating beyond it and what looks like a slender white tower standing on top of the island — a striking shot.",
    "Fans quickly reacted to the post, with comments like \"This makes me want to go to the aquarium lol,\" \"I wonder if he went to Enosui... it's close by, I'll go check it out,\" and \"So he did go to Enosui — making that the first photo is so cute.\"",
    "\"Enosui\" is the local nickname for the New Enoshima Aquarium, a familiar term among fans in the Kanagawa area.",
]))

blocks.append(h2("What's the island and tower in the background?"))
blocks.append(minibox('<p style="margin:0;"><strong>Likely identity of the background:</strong>"Enoshima" in Fujisawa City, Kanagawa Prefecture — the white tower appears to be the "Enoshima Sea Candle" observation lighthouse</p>'))
blocks.append(p([
    "Looking closely at the background, you can make out the outline of an island floating in the sea, along with a thin white tower standing near its peak.",
    "The shape of this island and the position of the tower match the well-known features of Enoshima, a tourist spot in Fujisawa City, Kanagawa Prefecture, and the \"Enoshima Sea Candle\" observation lighthouse located inside Samuel Cocking Garden on the island.",
    "Enoshima is one of the Shonan area's signature tourist destinations, and the Sea Candle rising above the island's greenery is a landmark that locals know well.",
    "Given the angle of the shot, it looks like it was taken somewhere along the coast that faces Enoshima across the water.",
]))

blocks.append(h2("Was the New Enoshima Aquarium (\"Enosui\") the actual filming spot?"))
blocks.append(minibox('<p style="margin:0;"><strong>Likely specific spot:</strong>A wooden seaside deck facing Enoshima, with a walkway featuring distinctive reddish railings</p>'))
blocks.append(p([
    "Looking at related images posted the same day as the KO1NOTE update, we found several photos of a walkway with wood-grain decking and reddish railings.",
    "The view from this deck also shows Enoshima and the Sea Candle floating beyond the sea, a composition very similar to YUKI's photo.",
]))
blocks.append(img2_html)
blocks.append(p([
    "The atmosphere of this deck — a covered walkway lined with benches — closely resembles the walkway connecting the interior of the New Enoshima Aquarium (\"Enosui\") to its outdoor terrace.",
    "Enosui sits right on Katase Beach and is known for its views of Enoshima across the water from its windows and outdoor deck.",
]))
blocks.append(img3_html)
blocks.append(img4_html)
blocks.append(p([
    "Given the sandy beach, the coastline, and the wooden walkway that continues through the shots, it seems quite likely that this area is within the aquarium's grounds.",
    "While we can't say for certain, the fact that an island resembling Enoshima appears consistently across multiple photos strongly suggests that YUKI's destination that day was <strong>the New Enoshima Aquarium (\"Enosui\"), facing Katase Beach</strong>.",
]))

blocks.append(h2("What about the \"new family member\" otter?"))
blocks.append(minibox('<p style="margin:0;"><strong>Likely identity of the new family member:</strong>"Happy Marine," a small-clawed otter plush won from the New Enoshima Aquarium\'s no-lose plush prize draw (1st through 3rd prize, etc.)</p>'))
blocks.append(p([
    "Alongside the aquarium theory, fans have also been talking about a \"new family member\" that YUKI apparently welcomed.",
    "Looking into it, this plush appears to be <strong>\"Happy Marine,\" a small-clawed otter plush that's a popular prize from the New Enoshima Aquarium's (\"Enosui\") plush prize draw</strong>.",
    "With its round eyes, plump and adorable shape, and squishy, soft texture, it's a popular souvenir and comfort item among visitors.",
]))
blocks.append(img7_html)
blocks.append(p([
    "As the photo shows, it seems to come in <strong>three colors — light brown, brown, and dark brown</strong> — and lining them up together only makes them cuter.",
    "This particular prize draw is a no-lose draw with tiers such as 1st through 3rd prize, making it an easy, low-pressure game to try while at the aquarium.",
    "According to the \"Otter Shop\" page on the aquarium's official website, the \"Otter\" plush prize draw costs <strong>1,100 yen per try</strong>, and it's a no-lose draw — everyone wins a plush.",
    "The prize sizes vary quite a bit by tier, as shown below.",
]))
blocks.append('''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr><td>Prize Tier</td><td>Approx. Size</td></tr>
<tr><td>1st Prize</td><td>About 90cm</td></tr>
<tr><td>2nd Prize</td><td>About 57cm</td></tr>
<tr><td>3rd Prize</td><td>About 33cm</td></tr>
</tbody></table></figure>
<!-- /wp:table -->''')
blocks.append(p([
    "Quantities are limited, with the draw ending once stock runs out.",
    "It's not known exactly which prize tier (and which size) YUKI actually won, but given how much the sizes differ, it's an intriguing detail to wonder about.",
    "Combined with the aquarium visit, this lines up with our theory that the KO1NOTE photos were taken at the New Enoshima Aquarium, making it quite likely he picked up \"Happy Marine\" there through the prize draw.",
    "That said, YUKI himself hasn't given any details yet — so this remains speculation based on the photos, comments, and product information alone.",
]))

blocks.append(h2("Has YUKI always been fond of Enoshima?"))
blocks.append(minibox('<p style="margin:0;"><strong>Hometown:</strong>Kanagawa Prefecture (the same prefecture as Fujisawa City, where Enoshima is located)</p>'))
blocks.append(p([
    "The same post also included what appear to be photos taken at night.",
    "One shot shows YUKI in front of a parking lot lined with palm trees, with a tower faintly glowing blue in the distance.",
]))
blocks.append(img5_html)
blocks.append(p([
    "The Enoshima Sea Candle is known for lighting up in different colors at night, and this blue lighting is one of its familiar looks.",
    "Another photo shows YUKI in front of a classic car, with the same blue tower light visible in the same spot.",
]))
blocks.append(img6_html)
blocks.append(p([
    "Since these night shots appear to have been taken on a different day from the daytime KO1NOTE photo, it suggests YUKI may have visited Enoshima more than once, not just this time.",
    "YUKI is originally from Kanagawa Prefecture, the same prefecture where Fujisawa City (home to Enoshima) is located.",
    "In fact, one comment on the post that appears to be from a local fan reads \"Thanks for visiting my hometown,\" suggesting the Enoshima area feels close to home for local fans too.",
]))

blocks.append(h2("What kind of place is the New Enoshima Aquarium (\"Enosui\")?"))
blocks.append(p([
    "The New Enoshima Aquarium (\"Enosui\") sits on Katase Beach in Fujisawa City, Kanagawa Prefecture, and is known for exhibits like the \"Sagami Bay Zone,\" which focuses on creatures from Sagami Bay, and the popular \"Jellyfish Fantasy Hall.\"",
    "It's also known for its great views — Enoshima can be seen across the water from inside the aquarium — making it a popular spot for both dates and sightseeing.",
    "As one of the Shonan area's most popular attractions, confirmation that a KO1KEYZ member visited on his own time is likely to get local fans especially excited.",
]))
blocks.append(wphtml('''<iframe
  src="https://maps.google.com/maps?q=%E6%96%B0%E6%B1%9F%E3%83%8E%E5%B3%B6%E6%B0%B4%E6%97%8F%E9%A4%A8&t=&z=15&ie=UTF8&iwloc=&output=embed"
  width="100%" height="350" frameborder="0" scrolling="no"
  style="border:0;" loading="lazy">
</iframe>'''))

blocks.append(h2("Summary"))
blocks.append(wphtml(f'''<div style="border:1px solid #ddd9d3;border-radius:6px;overflow:hidden;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">YUKI's KO1NOTE Photo Location, Summarized</p>
<div style="padding:14px 18px;background:#f7f6f4;">
<p style="margin:0;">
✔ <strong>Date:</strong>Shared in the KO1NOTE update on August 19, 2026<br>
✔ <strong>Background:</strong>Likely Enoshima in Fujisawa City, Kanagawa Prefecture, with the white tower likely being the "Enoshima Sea Candle" observation lighthouse<br>
✔ <strong>Likely location:</strong>The New Enoshima Aquarium ("Enosui"), which has a seaside deck facing Enoshima<br>
✔ <strong>The trending "family member":</strong>Likely "Happy Marine," a small-clawed otter plush won from the New Enoshima Aquarium's no-lose plush prize draw<br>
✔ <strong>Past visits:</strong>Night photos suggest he may have visited Enoshima before this trip as well
</p>
</div>
</div>'''))

blocks.append(p([
    "He seems to love Enoshima enough that you half expect to run into him there someday — whether at the aquarium itself or just somewhere around Kanagawa!",
    "According to the official site, this prize draw has limited quantities and <strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;text-decoration:underline;\">ends once supplies run out</span></strong>.",
    "If you want to welcome the same \"Happy Marine\" into your own family as YUKI did, it sounds like you'll need to head to the New Enoshima Aquarium sooner rather than later! It's making us want to go right now... anyone else in, let's go try our luck together!",
]))

blocks.append(wphtml(f'''<div style="border:1px solid #ddd9d3;border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f6f4;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">Related Articles</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-1.com/what-is-the-family-structure-o-10480">An article looking into YUKI (Yui Goto)'s family (in Japanese)</a></li>
<li><a href="https://chomoand-1.com/what-is-the-room-allocation-at-11122">An article predicting KO1KEYZ's dorm room assignments (in Japanese)</a></li>
<li><a href="https://chomoand-1.com/ko1keyz-why-was-the-debut-date-10449">An article explaining the reasoning behind KO1KEYZ's debut date (in Japanese)</a></li>
</ul>
</div>'''))

content = "\n\n".join(blocks)
print("content length (chars):", len(content))

JP_POST_ID = 11552
EXISTING_EN_POST_ID = 11562
slug = "where-is-yukis-goto-yui-koi-no-en"

if EXISTING_EN_POST_ID:
    payload = {
        "title": title,
        "content": content,
        "status": "draft",
    }
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_EN_POST_ID}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print("UPDATED_EN_POST_ID", post["id"])
    print("SLUG", post["slug"])
    print("LINK", post.get("link"))
else:
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "categories": [66],
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
    print("SLUG", post["slug"])
    print("LINK", post.get("link"))

    r2 = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps({"status": "draft", "featured_media": MEDIA_IDS["eyecatch"]}).encode("utf-8"),
    )
    r2.raise_for_status()

print("PREVIEW", f"{WP_URL}/?p={post['id']}")
