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

JP_POST_ID = 12245
JP_SLUG = "ko1keyz-kobe-fan-meeting-strea"
JP_EYECATCH_MEDIA_ID = 12244


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


def titlebox(ttl, items, ordered=False):
    tag = "ol" if ordered else "ul"
    lis = "\n".join(f"<li>{t}</li>" for t in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>
<{tag} style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
{lis}
</{tag}>
</div>''')


def minibox(html_body):
    return wphtml(f'''<div style="border:1px solid #ddd;border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f7f7f7;">
{html_body}
</div>''')


def notebox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def wptable(headers, rows):
    thead = "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;font-weight:bold;">{h}</td>' for h in headers)
    trs = "\n".join(
        "<tr>" + "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;">{c}</td>' for c in row) + "</tr>"
        for row in rows
    )
    return f'''<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>
<tr>{thead}</tr>
{trs}
</tbody></table></figure>
<!-- /wp:table -->'''


OFFICIAL_NEWS = "https://ko1keyz.com/news/detail/99"
CAMERA_URL = "https://chomoand-1.com/en/?p=11734"

title = "KO1KEYZ's Kobe fan meeting will be live streamed: how to watch"

blocks = []

blocks.append(p([
    "On September 3, 2026, KO1KEYZ posted on their official X account and website that the Hyogo shows of their first fan meeting, <strong>\"2026 KO1KEYZ 1ST FAN MEETING,\" will be live streamed worldwide</strong>.",
    "Only <strong>one show &mdash; the Day 2 evening performance in Hyogo</strong> &mdash; will be streamed, starting <strong>at 6:30pm JST on Thursday, September 10, 2026</strong>. There is no archive (replay) stream.",
    "This article covers which show is being streamed, the viewing ticket price and sales window, the steps from purchase to watching, and the outlook for an archive or Blu-ray release.",
]))

blocks.append(titlebox("What this article covers", [
    "Which performance is being live streamed",
    "The stream date, time, and viewing ticket price",
    "The ticket sales window and how to watch",
    "Whether there will be an archive stream or a Blu-ray/DVD release",
]))

blocks.append(h2("Only the Day 2 evening show in Hyogo will be streamed"))
blocks.append(minibox('<p style="margin:0;"><strong>Stream target:</strong> Hyogo (Kobe World Memorial Hall), Day 2 evening performance</p>\n<p style="margin:4px 0 0 0;"><strong>Date &amp; time:</strong> Thursday, September 10, 2026, 6:30pm JST &mdash; starts as the evening show begins</p>'))
blocks.append(p([
    "The Hyogo leg of \"2026 KO1KEYZ 1ST FAN MEETING\" runs for two days, on Wednesday September 9 and Thursday September 10, with four shows in total across matinee and evening slots at Kobe World Memorial Hall. The only one being live streamed is the final show: the <strong>evening performance on Thursday, September 10</strong>.",
    "The stream begins at 6:30pm JST, the same time the evening show starts. It is a live broadcast only, with <strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">no archive (replay) stream</span></strong>, so you need to watch in real time on the day.",
    "The Tokyo shows (August 21&ndash;23 at TOYOTA ARENA TOKYO) have already finished, so this Hyogo evening stream is effectively the only chance to see the first fan meeting on video.",
]))
blocks.append(wptable(
    ["Show", "Doors", "Start", "Live stream"],
    [
        ["Sep 9 (Wed) matinee", "12:30", "13:30", "No"],
        ["Sep 9 (Wed) evening<br>[added show]", "17:30", "18:30", "No"],
        ["Sep 10 (Thu) matinee<br>[added show]", "12:30", "13:30", "No"],
        ["Sep 10 (Thu) evening", "17:30", "18:30", "Yes &mdash; streamed"],
    ],
))
blocks.append(p([
    "The announcement went out through the official X account (@KO1KEYZofficial) and the website news page, and spread quickly alongside the phrase \"Hyogo show to be live streamed worldwide.\" It is a strong sign of how much attention this first fan meeting is drawing, even before the group's debut.",
    "For fans who missed out on tickets, or who live too far away or overseas to travel to the Kansai region, this stream is a rare chance to see all the members together.",
]))

blocks.append(h2("Viewing ticket price and streaming services"))
blocks.append(minibox('<p style="margin:0;"><strong>Viewing ticket:</strong> 3,600 yen (tax included) + system fees</p>\n<p style="margin:4px 0 0 0;"><strong>Streaming services:</strong> In Japan: Lemino and Lawson Ticket / a separate service is provided for overseas viewers</p>'))
blocks.append(p([
    "<strong><span class=\"swl-marker mark_yellow\">The viewing ticket costs 3,600 yen (tax included)</span></strong>. On top of that, each streaming platform adds its own system fee.",
    f"<span class=\"swl-marker mark_yellow\">In Japan the stream is offered on Lemino and Lawson Ticket</span>, and a separate streaming service is provided for overseas viewers. You can check the full list of platforms and payment methods on the <a href=\"{OFFICIAL_NEWS}\" target=\"_blank\" rel=\"noopener\">official news page</a>.",
    "Compared with a seat at the venue, the stream lets you watch from home for around 3,600 yen, so the barrier to joining in is fairly low &mdash; an easy way to get a look at a pre-debut group's fan meeting.",
]))
blocks.append(p([
    "The added system fee differs by platform. On X, fans who compared the two Japanese options reported that the totals came out a few hundred yen apart, since both Lemino and Lawson Ticket add a Ticket Plus handling fee.",
    "Some fans also noted that Lawson Ticket only accepts in-store payment at Lawson or Ministop convenience stores, with no credit card option. If you want to pay quickly by card, Lemino is the easier choice; if you would rather pay in cash at a store, Lawson Ticket works. Always check the final total on each service's checkout screen before buying.",
]))

blocks.append(h2("Ticket sales window and how to watch"))
blocks.append(minibox('<p style="margin:0;"><strong>Sales window:</strong> Thursday, September 3, 2026, 12:00pm &ndash; Thursday, September 10, 2026, 7:00pm (JST)</p>'))
blocks.append(p([
    "Viewing tickets are on sale from <strong>12:00pm JST on Thursday, September 3 until 7:00pm JST on Thursday, September 10</strong>. You can still buy for a short while after the evening show starts at 18:30, but sales close at 19:00. With no archive available, it is safer to get your ticket early if you plan to watch.",
]))
blocks.append(titlebox("From buying a ticket to watching", [
    "Go to the streaming page you want to use &mdash; Lemino or Lawson Ticket in Japan, or the overseas service",
    "Buy and pay for a viewing ticket (3,600 yen + system fee) within the sales window (Sep 3, 12:00pm &ndash; Sep 10, 7:00pm JST)",
    "On the day, log in to the same service's app or website with the same account",
    "Start watching when the stream begins at 6:30pm JST on Thursday, September 10 (no replay afterwards)",
], ordered=True))
blocks.append(p([
    "If you are watching from outside Japan, mind the time difference. Because it is live only, convert the 6:30pm JST start time to your local time and plan around it in advance.",
    "On the day, watch from somewhere with a stable connection, ideally on Wi-Fi. Traffic can spike right before the start, so open the streaming page with a little time to spare.",
]))

blocks.append(h2("What will the stream show?"))
blocks.append(p([
    "The first fan meeting is built around talk segments, games between the members, song performances, and a photo-OK time near the end. At the earlier Tokyo shows, moments like the members riding a cart around the arena and the photo time during the encore became big talking points among fans.",
    "The Hyogo evening show being streamed is the last of the four performances, so the members' mood after two full days and their closing remarks should be worth watching too.",
]))

blocks.append(h2("Will there be an archive stream or a Blu-ray release?"))
blocks.append(minibox('<p style="margin:0;"><strong>Archive stream:</strong> None (live only)</p>\n<p style="margin:4px 0 0 0;"><strong>Blu-ray/DVD release:</strong> Not announced as of September 3, 2026</p>'))
blocks.append(p([
    "This stream has no archive (replay). You will not be able to rewatch the same broadcast afterwards, so plan for real-time viewing.",
    f"There is also no official word yet on a Blu-ray or DVD of the shows. For more on the recording cameras spotted at the venue and the chances of a physical release, see <a href=\"{CAMERA_URL}\">Were there cameras at KO1KEYZ's 1st fan meeting? Will it get a Blu-ray release?</a>.",
    "Note that a separate special program following the fan meeting preparations has been announced for Lemino, but that is a documentary-style piece rather than the show itself. It is a different piece of content from this Hyogo evening stream.",
]))

blocks.append(h2("Summary"))
blocks.append(notebox('''<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">KO1KEYZ Kobe fan meeting live stream: key points</p>
<p style="margin:0;">
&#10003; Only the Hyogo (Kobe World Memorial Hall) Day 2 evening show is streamed<br>
&#10003; It airs at 6:30pm JST on Thursday, September 10, 2026, with no archive stream<br>
&#10003; The viewing ticket is 3,600 yen (tax incl.) + system fee; in Japan it is on Lemino and Lawson Ticket<br>
&#10003; System fees vary by service, and Lawson Ticket reportedly takes in-store payment only<br>
&#10003; Sales run from Sep 3, 12:00pm to Sep 10, 7:00pm (JST)<br>
&#10003; No physical release announced; the Lemino special program is separate from the show itself
</p>'''))
blocks.append(p([
    "Even if you cannot be there in person, getting to watch the very first fan meeting live is a nice thing. Mind the time difference and the sales deadline, and open the streaming page early on the day to wait for it to start.",
]))

blocks.append(notebox(f'''<p style="margin:0 0 8px 0;"><strong>More on KO1KEYZ's fan meeting on this blog:</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{CAMERA_URL}" target="_blank" rel="noopener">Were there cameras at KO1KEYZ's 1st fan meeting? Will it get a Blu-ray release?</a></li>
<li><a href="{OFFICIAL_NEWS}" target="_blank" rel="noopener">KO1KEYZ official news page (live stream details)</a></li>
</ul>'''))

content = "\n\n".join(blocks)
print("content chars:", len(content))

slug = f"{JP_SLUG}-en"

EN_POST_ID = 12250  # update in place

payload = {
    "title": title,
    "content": content,
    "status": "draft",
    "slug": slug,
    "lang": "en",
    "translations": {"ja": JP_POST_ID},
    "featured_media": JP_EYECATCH_MEDIA_ID,
    "categories": [66, 62],
    "author": 2,
}
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{EN_POST_ID}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps(payload).encode("utf-8"),
)
r.raise_for_status()
post = r.json()
print("EN POST_ID", post["id"])
print("EN SLUG", post["slug"])
print("EN LINK", post.get("link", f"{WP_URL}/en/?p={post['id']}"))

with open(ROOT / "tmp_ko1keyz_kobe_fanmi_streaming_en_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
