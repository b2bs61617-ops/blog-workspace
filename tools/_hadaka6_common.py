# -*- coding: utf-8 -*-
"""はだかんぼうたち第6話の記事3本で共通の部品(2026-11-15)。"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blogkit  # noqa: E402

SITE = "travis"
TVER = "https://tver.jp/episodes/ep2voa79tr"
BASE = "https://chomoand-4.blog"
NAMES = ["加藤ローサ", "髙木雄也", "大沢あかね", "伊藤歩", "平子祐希", "MEGUMI", "片岡凜", "白宮みずほ", "安藤忠雄"]
b = blogkit.Blocks("#5b9bd5", "#bbdefb", "#eef6fd")
MEDIA_CACHE = blogkit.ARTICLES / "hadaka6_media.json"

EP5_LOC = BASE + "/hadakanboutachi-ep5-filming-locations-2081"
EP5_COS = BASE + "/hadakanboutachi-ep5-sabazaki-costume-2109"
EP4_LOC = BASE + "/hadakanboutachi-ep4-filming-locations-1875"
EP1_LOC = BASE + "/hadakanboutachi-ep1-filming-locations-1208"
EXHIBIT = BASE + "/hadakanboutachi-exhibit-tv-asahi-atrium-2491"
ROLE = BASE + "/sabazaki-ryo-genta-matsuda-role-1184"
TVER_ART = BASE + "/hadakanboutachi-tver-kansai-time-1186"


def infobox(title, rows):
    trs = "".join('<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:32%;">{}</td>'
                  '<td style="border:1px solid #ccc;padding:8px 12px;">{}</td></tr>'.format(k, v) for k, v in rows)
    return b.html('<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">'
                  '<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{}</p>'
                  '<table style="border-collapse:collapse;width:100%;"><tbody>{}</tbody></table></div>'.format(title, trs))


def related(title, links):
    lis = "".join('<li><a href="{}">{}</a></li>'.format(u, t) for t, u in links)
    return b.html('<div style="border:1px solid {B};border-left:4px solid {A};border-radius:4px;padding:14px 18px;'
                  'margin:0 0 16px 0;background:{BG};"><p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{t}</p>'
                  '<ul style="margin:0;padding-left:1.3em;">{l}</ul></div>'.format(B=b.B, A=b.A, BG=b.BG, t=title, l=lis))


def media(keys_alts, dry=False):
    """images/hadakanbou_ep6_<key>.jpg をアップして {key: media json}。二重アップしないよう控えを残す。"""
    cache = json.loads(MEDIA_CACHE.read_text(encoding="utf-8")) if MEDIA_CACHE.exists() else {}
    out = {}
    wp = None if dry else blogkit.WP(SITE)
    for k, alt in keys_alts.items():
        if dry:
            out[k] = {"source_url": "x", "media_details": {"width": 1280, "height": 720, "sizes": {}}}
            continue
        if k not in cache:
            mid = wp.upload_media(str(blogkit.ROOT / "images" / "hadakanbou_ep6_{}.jpg".format(k)), alt)
            cache[k] = wp.get("/media/{}".format(mid))
            MEDIA_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            print("img", k, mid)
        out[k] = cache[k]
    return out


def img(m, alt):
    sizes = m["media_details"].get("sizes", {})
    large = sizes.get("large") or sizes.get("full") or {"source_url": m["source_url"],
                                                        "width": m["media_details"]["width"], "height": m["media_details"]["height"]}
    return b.html('<figure class="wp-block-image size-large"><img src="{}" alt="{}" width="{}" height="{}" '
                  'style="max-width:100%;height:auto;"><figcaption style="font-size:0.8em;color:#888;">出典:{}</figcaption>'
                  '</figure>'.format(large["source_url"], alt, large["width"], large["height"], TVER))


DRAMA_ROWS = [
    ("タイトル", "はだかんぼうたち 第6話「白くて、柔らかそうな肉体」"),
    ("放送日", "2026年11月14日(土)23時〜"),
    ("放送枠", "テレビ朝日系「オシドラサタデー」"),
    ("出演", "松田元太・加藤ローサ・髙木雄也・大沢あかね ほか"),
    ("原作", "江國香織『はだかんぼうたち』"),
    ("見逃し配信", "TVer(無料)・TELASA"),
]


def run(key, title, slug, body, eyecatch, eyecatch_alt, categories=(3, 7)):
    out = blogkit.finalize(body, SITE, NAMES)
    if "--build-only" in sys.argv:
        blogkit.ARTICLES.mkdir(exist_ok=True)
        (blogkit.ARTICLES / (key + ".html")).write_text(out, encoding="utf-8")
        print("作った:", blogkit.ARTICLES / (key + ".html"))
        return
    blogkit.upload_draft(SITE, key, title, out, slug, list(categories), blogkit.ROOT / "images" / eyecatch,
                         eyecatch_alt, names=NAMES, update="--update" in sys.argv)
