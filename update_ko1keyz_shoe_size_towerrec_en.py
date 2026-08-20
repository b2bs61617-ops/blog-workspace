# -*- coding: utf-8 -*-
import base64, json
import requests

def load_env(path):
    env = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env

env = load_env('.env')
WP_URL = env['WP_KOIKEYS_URL'].rstrip('/')
AUTH = base64.b64encode(f"{env['WP_KOIKEYS_USERNAME']}:{env['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
h = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}
hget = {'Authorization': f'Basic {AUTH}'}

KOSUKE_MEDIA_ID = 11635
TOWERREC_TWEET = "https://x.com/azmchan1202/status/2090335670049062963"

media = requests.get(f'{WP_URL}/wp-json/wp/v2/media/{KOSUKE_MEDIA_ID}', headers=hget).json()

def build_img_html(media, alt, caption, size_key="large"):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    full_w = media["media_details"]["width"]
    full_h = media["media_details"]["height"]
    chosen = sizes.get(size_key, {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    img_src = chosen["source_url"]
    img_w = chosen["width"]
    img_h = int(img_w * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {chosen["source_url"]} {chosen["width"]}w, {full_url} {full_w}w'
    return f'''<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>
</figure>'''

r = requests.get(f'{WP_URL}/wp-json/wp/v2/posts/11558?context=edit', headers=hget)
r.raise_for_status()
raw = r.json()['content']['raw']

replacements = []

old1 = '''<p>KO1KEYZ, formed through 'PRODUCE 101 JAPAN SHINSEKAI', keep making headlines every day as their October 7, 2026 debut approaches.<br>
This time, a fan who visited the costume exhibit for their debut single 'SHINSEKAI' at HMV happened to spot the size tags inside the shoes on display, and shared the discovery on X.<br>
Among the six sizes that could be read, <strong>RYUJI had the largest at 27.5cm, while YOSHIKI and TOWA had the smallest at 26.0cm</strong>.<br>
In this article, we've put together each member's shoe size based on what was shared on X.</p>'''
new1 = '''<p>KO1KEYZ, formed through 'PRODUCE 101 JAPAN SHINSEKAI', keep making headlines every day as their October 7, 2026 debut approaches.<br>
Fans who visited the costume exhibits for their debut single 'SHINSEKAI' at HMV and Tower Records Shibuya happened to spot the size tags inside the shoes on display, and shared their discoveries on X.<br>
Among the ten sizes that could be read, <strong>RYUJI, KOSUKE, and DAIKI had the largest at 27.5cm, while YOSHIKI and TOWA had the smallest at 26.0cm</strong>.<br>
In this article, we've put together each member's shoe size based on what was shared on X.</p>'''
replacements.append((old1, new1))

old2 = '''<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ded9d2;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#8a8378;color:#fff;">What this article covers</p>'''
new2 = '''<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ded9d2;border-left:4px solid #8a8378;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f8f6f4;">
<p style="margin:0;"><strong>Update (August 21, 2026):</strong>New sightings shared from Tower Records Shibuya confirmed four more sizes — KOSUKE, DAIKI, SIYOUNG, and RYOGA. This article has been updated with the latest information.</p>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div style="border:1px solid #ded9d2;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#8a8378;color:#fff;">What this article covers</p>'''
replacements.append((old2, new2))

old3 = '<h2 class="wp-block-heading">Shoe size tags spotted at the HMV SHINSEKAI costume exhibit</h2>'
new3 = '<h2 class="wp-block-heading">Shoe size tags spotted at the HMV and Tower Records Shibuya SHINSEKAI costume exhibits</h2>'
replacements.append((old3, new3))

old4 = '<p style="margin:0;"><strong>Where:</strong>HMV (\'SHINSEKAI\' costume exhibit)<br><strong>Shared on:</strong>August 20, 2026</p>'
new4 = '<p style="margin:0;"><strong>Where:</strong>HMV and Tower Records Shibuya (\'SHINSEKAI\' costume exhibits)<br><strong>Shared on:</strong>August 20-21, 2026</p>'
replacements.append((old4, new4))

old5 = '''<figcaption style="text-align:center;font-size:12px;">Source:<a href="https://x.com/lalabonbondrop/status/2090264614382788644" target="_blank" rel="noopener">https://x.com/lalabonbondrop/status/2090264614382788644</a></figcaption>
</figure>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">KO1KEYZ members' shoe sizes</h2>'''

towerrec_img_html = build_img_html(
    media,
    "KOSUKE's shoe size tag (model No. 397447-02), photographed at the Tower Records Shibuya SHINSEKAI costume exhibit",
    f'Source:<a href="{TOWERREC_TWEET}" target="_blank" rel="noopener">{TOWERREC_TWEET}</a>',
)

new5 = f'''<figcaption style="text-align:center;font-size:12px;">Source:<a href="https://x.com/lalabonbondrop/status/2090264614382788644" target="_blank" rel="noopener">https://x.com/lalabonbondrop/status/2090264614382788644</a></figcaption>
</figure>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Then on August 21, 2026, another fan who checked out the exhibit at Tower Records Shibuya posted photos of the size tags for KOSUKE, DAIKI, SIYOUNG, and RYOGA.<br>
According to that post, both KOSUKE and DAIKI came in at 27.5cm, SIYOUNG at 27.0cm, and RYOGA at an estimated 26.5cm (based on the US size shown on the tag).<br>
The poster mentioned that the angle made it impossible to check the tags for YUKI and KEITO.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{towerrec_img_html}
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">KO1KEYZ members' shoe sizes</h2>'''
replacements.append((old5, new5))

old6 = '<p style="margin:0;"><strong>Six out of twelve members\' sizes were confirmed.</strong>RYUJI had the largest size at 27.5cm, while YOSHIKI and TOWA had the smallest at 26.0cm.</p>'
new6 = '<p style="margin:0;"><strong>Ten out of twelve members\' sizes have been confirmed.</strong>RYUJI, KOSUKE, and DAIKI had the largest size at 27.5cm, while YOSHIKI and TOWA had the smallest at 26.0cm.</p>'
replacements.append((old6, new6))

old7 = '''<tr><td>Member</td><td>Size (cm)</td><td>Notes</td></tr>
<tr><td>YOSHIKI (Kaki Yada)</td><td>26.0</td><td>-</td></tr>
<tr><td>TOWA (Towa Hamada)</td><td>26.0</td><td>-</td></tr>
<tr><td>SHINHAENG (Oh Sin-haeng)</td><td>26.5</td><td>-</td></tr>
<tr><td>ISSA (Issa Yanagiya)</td><td>27.0</td><td>-</td></tr>
<tr><td>RYUJI (Ryuji Sugiyama)</td><td>27.5</td><td>Worn without an insole</td></tr>
<tr><td>YURA (Yura Abe)</td><td>-</td><td>Size tag wasn\'t visible in the photo</td></tr>'''
new7 = '''<tr><td>Member</td><td>Size (cm)</td><td>Notes</td></tr>
<tr><td>YOSHIKI (Kaki Yada)</td><td>26.0</td><td>-</td></tr>
<tr><td>TOWA (Towa Hamada)</td><td>26.0</td><td>-</td></tr>
<tr><td>SHINHAENG (Oh Sin-haeng)</td><td>26.5</td><td>-</td></tr>
<tr><td>RYOGA (Ryoga Iizuka)</td><td>26.5 (estimated)</td><td>Estimated from the US 8.5 size shown; cm figure not directly confirmed</td></tr>
<tr><td>ISSA (Issa Yanagiya)</td><td>27.0</td><td>-</td></tr>
<tr><td>SIYOUNG (Park Si-yeong)</td><td>27.0</td><td>-</td></tr>
<tr><td>RYUJI (Ryuji Sugiyama)</td><td>27.5</td><td>Worn without an insole</td></tr>
<tr><td>KOSUKE (Kosuke Terui)</td><td>27.5</td><td>-</td></tr>
<tr><td>DAIKI (Daiki Kato)</td><td>27.5</td><td>-</td></tr>
<tr><td>YURA (Yura Abe)</td><td>-</td><td>Shoe and name tag confirmed, but the size figure wasn\'t visible</td></tr>'''
replacements.append((old7, new7))

old8 = '<p><strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">There\'s a 1.5cm gap between the largest size (RYUJI, 27.5cm) and the smallest (YOSHIKI and TOWA, 26.0cm)</span></strong>.</p>'
new8 = '<p><strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">There\'s a 1.5cm gap between the largest sizes (RYUJI, KOSUKE, and DAIKI at 27.5cm) and the smallest (YOSHIKI and TOWA, 26.0cm)</span></strong>.</p>'
replacements.append((old8, new8))

old9 = '<p style="margin:0;"><strong>The shoes are PUMA\'s "Club II Era," and all six tags shared the same model number, "397447-02."</strong></p>'
new9 = '<p style="margin:0;"><strong>The shoes are PUMA\'s "Club II Era," and all ten confirmed tags shared the same model number, "397447-02."</strong></p>'
replacements.append((old9, new9))

old10 = '<p>A closer look at the size tags shows the shoes are a PUMA model, and all six members\' tags share the same model number, "397447-02."<br>'
new10 = '<p>A closer look at the size tags shows the shoes are a PUMA model, and all ten confirmed members\' tags share the same model number, "397447-02."<br>'
replacements.append((old10, new10))

old11 = '<h2 class="wp-block-heading">What about the other six members?</h2>'
new11 = '<h2 class="wp-block-heading">What about the other two members?</h2>'
replacements.append((old11, new11))

old12 = '<p style="margin:0;"><strong>Six members\' sizes were confirmed this time.</strong>KOSUKE, KEITO, DAIKI, RYOGA, YUKI, and SIYOUNG remain unconfirmed.</p>'
new12 = '<p style="margin:0;"><strong>Ten members\' sizes have been confirmed so far.</strong>YUKI and KEITO remain unconfirmed.</p>'
replacements.append((old12, new12))

old13 = '''<p>The size tags confirmed in this post belonged to YOSHIKI, TOWA, SHINHAENG, ISSA, RYUJI, and YURA.<br>
The remaining six members — KOSUKE, KEITO, DAIKI, RYOGA, YUKI, and SIYOUNG — weren\'t confirmed, as the original poster wasn\'t able to check other exhibit locations such as Tower Records.<br>
If any sightings from other venues come up, we\'ll update this article with the details.</p>'''
new13 = '''<p>Between the two posts, the size tags confirmed so far belong to YOSHIKI, TOWA, SHINHAENG, ISSA, RYUJI, KOSUKE, DAIKI, SIYOUNG, and RYOGA — nine members — plus YURA, whose shoe and name tag were confirmed even though the size figure wasn\'t.<br>
The remaining two members, YUKI and KEITO, weren\'t confirmed at either HMV or Tower Records, as both posters said the angle made it impossible to see their tags.<br>
If any further sightings come up, we\'ll update this article with the details.</p>'''
replacements.append((old13, new13))

old14 = '''<li>Six members\' shoe size tags were unexpectedly spotted at the HMV \'SHINSEKAI\' costume exhibit</li>
<li>Sizes: YOSHIKI and TOWA at 26.0cm, SHINHAENG at 26.5cm, ISSA at 27.0cm, and RYUJI at 27.5cm</li>
<li>All six wore PUMA\'s "Club II Era" (No. 397447-02) in different sizes, retailing around ¥10,450 (tax included)</li>
<li>The remaining six members (KOSUKE, KEITO, DAIKI, RYOGA, YUKI, SIYOUNG) are still unconfirmed</li>'''
new14 = '''<li>Ten members\' shoe size tags were unexpectedly spotted at the HMV and Tower Records Shibuya \'SHINSEKAI\' costume exhibits</li>
<li>Sizes: YOSHIKI and TOWA at 26.0cm, SHINHAENG and RYOGA at 26.5cm, ISSA and SIYOUNG at 27.0cm, and RYUJI, KOSUKE, and DAIKI at 27.5cm</li>
<li>All ten confirmed members wore PUMA\'s "Club II Era" (No. 397447-02) in different sizes, retailing around ¥10,450 (tax included)</li>
<li>The remaining two members (YUKI, KEITO) are still unconfirmed</li>'''
replacements.append((old14, new14))

for i, (old, new) in enumerate(replacements, 1):
    cnt = raw.count(old)
    assert cnt == 1, f"replacement {i} matched {cnt} times, expected 1"
    raw = raw.replace(old, new)

ur = requests.post(f'{WP_URL}/wp-json/wp/v2/posts/11558', headers=h, data=json.dumps({"content": raw}).encode('utf-8'))
ur.raise_for_status()
print("EN updated, length:", len(ur.json()['content']['raw']))
open('tmp_en_updated.html', 'w', encoding='utf-8').write(raw)
