# -*- coding: utf-8 -*-
"""Upload drafts: キテレツキテル！第5回(佐久間大介×HYROX) 概要 + ロケ地(WARRIORS GYM) to chomoand-5.site."""
import re, json, base64, urllib.request

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip().strip('"')
BASE = env["WP_CHOMO5_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_CHOMO5_USERNAME']}:{env['WP_CHOMO5_APP_PASSWORD']}".encode()).decode()
SRC = "https://tver.jp/episodes/epbo6c6c0e"
CHK = ('<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid #d6588a;border-radius:3px;'
       'color:#d6588a;font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')


def req(path, data=None, headers=None):
    r = urllib.request.Request(BASE + path, data=data, method="POST" if data is not None else "GET")
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    with urllib.request.urlopen(r) as resp:
        return json.loads(resp.read().decode("utf-8"))


def jpost(path, obj):
    return req(path, json.dumps(obj).encode(), {"Content-Type": "application/json"})


def media(fn, alt=""):
    m = req("/wp-json/wp/v2/media", open(REPO + rf"\images\{fn}", "rb").read(),
            {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{fn}"'})
    if alt:
        jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": alt})
    return m


def build(html_file, prefix, imgs):
    html = open(REPO + rf"\articles\{html_file}", encoding="utf-8").read()
    html = html.replace("[[CHK]]", CHK).replace("[[LINK_613]]", BASE + "/?p=613")
    for k, alt in imgs.items():
        m = media(f"{prefix}_{k}.jpg", alt)
        fig = ('<!-- wp:image {"id":%d,"sizeSlug":"full","linkDestination":"none"} -->\n'
               '<figure class="wp-block-image size-full"><img src="%s" alt="%s" class="wp-image-%d" style="max-width:100%%;height:auto;"/>'
               '<figcaption style="font-size:0.8em;color:#888;">出典:%s</figcaption></figure>\n'
               '<!-- /wp:image -->') % (m["id"], m["source_url"], alt, m["id"], SRC)
        html = html.replace(f"[[IMG_{k}]]", fig)
    return re.sub(r"<hr\s*/?>", "", html).strip()


EP5_IMGS = {
    "01": "キテレツキテル！にゲスト出演したSnow Manの佐久間大介",
    "02": "HYROXに挑戦するKEY TO LITの5人",
    "03": "HYROXパフォーマンスコーチの宮崎紗衣さん",
    "04": "キテレツキテル！オリジナルHYROXレースのコース",
    "05": "HYROXレースのスタート",
    "06": "スレッドプッシュに挑戦する井上瑞稀",
    "07": "ローイングに挑戦する岩﨑大昇",
    "08": "HYROXレースのタイムは19分55秒",
    "09": "次回予告は中間淳太をおもてなし",
}
GYM_IMGS = {
    "01": "キテレツキテル！のロケ地WARRIORS GYMのテロップ",
    "02": "WARRIORS GYMの六角形のライト",
    "03": "WARRIORS GYMの入口のシャンデリア",
    "04": "WARRIORS GYMのスレッドプッシュ用のそり",
    "05": "WARRIORS GYMのスキーエルゴ",
    "06": "WARRIORS GYMの赤いカーペットに並ぶKEY TO LIT",
}

ep5_html = build("kitetsu_kiteru_ep5_sakuma_hyrox.html", "ktl_ep5_hyrox", EP5_IMGS)
gym_html = build("kitetsu_kiteru_ep5_gym_location.html", "ktl_ep5_gym", GYM_IMGS)
eye1 = media("ktl_ep5_hyrox_eyecatch.jpg", "キテレツキテル！佐久間大介 HYROX回")["id"]
eye2 = media("ktl_ep5_gym_eyecatch.jpg", "キテレツキテル！HYROX回のロケ地")["id"]

p1 = jpost("/wp-json/wp/v2/posts", {
    "title": "【未】【キテレツキテル】佐久間大介とHYROX挑戦！結果は？未公開シーンも",
    "slug": "kitetsu-kiteru-ep5-sakuma-hyrox",
    "content": "", "status": "draft", "categories": [4], "author": 2, "featured_media": eye1})
p2 = jpost("/wp-json/wp/v2/posts", {
    "title": "【未】【キテレツキテル】HYROX回のロケ地のジムはどこ？料金や行き方も",
    "slug": "kitetsu-kiteru-hyrox-gym-location",
    "content": "", "status": "draft", "categories": [4], "author": 2, "featured_media": eye2})
ep5_html = ep5_html.replace("[[LINK_GYM]]", f"{BASE}/?p={p2['id']}")
gym_html = gym_html.replace("[[LINK_EP5]]", f"{BASE}/?p={p1['id']}")
for h in (ep5_html, gym_html):
    assert "[[" not in h, re.findall(r"\[\[[^\]]+\]\]", h)
jpost(f"/wp-json/wp/v2/posts/{p1['id']}", {"content": ep5_html})
jpost(f"/wp-json/wp/v2/posts/{p2['id']}", {"content": gym_html})
for p, eye in ((p1, eye1), (p2, eye2)):
    g = req(f"/wp-json/wp/v2/posts/{p['id']}?context=edit&_fields=id,status,title,content,featured_media,author")
    print(g["id"], g["status"], g["title"]["raw"], "len", len(g["content"]["raw"]),
          "imgs", g["content"]["raw"].count("wp-image-"), "eye", g["featured_media"], "author", g["author"])
