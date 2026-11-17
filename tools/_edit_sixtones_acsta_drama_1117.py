# 2026-11-17 chomoand-0.com ID1552 (SixTONES acrylic stand history, published): add drama-goods acrylic stands
# (単身花日 2023 / アンサンブル 2025) to the list, a new H2 section with the official MerchCompany_jp photo, and the matome (Yuka request "追記して").
# Modes: build (writes articles/sixtones_acsta_1552.html from the live post) / push (checks the latest revision is ours, then updates)
import os, sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import requests, x_auto_post_buffer as xb
ENV_FILE = Path(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))
env = xb.load_env(ROOT / ".env"); env.update({k: v.strip("\"'") for k, v in xb.load_env(ENV_FILE).items() if v and not k.startswith("GOOGLE_INDEXING")})
U = env["WP_AUDITION_URL"].rstrip("/"); A = (env["WP_AUDITION_USERNAME"], env["WP_AUDITION_APP_PASSWORD"])
PID = 1552
OUT = ROOT / "articles/sixtones_acsta_1552.html"
IMG = ROOT / "images/x/sixtones_ensemble_acsta_merch.jpg"
SRC_IMG = "https://x.com/MerchCompany_jp/status/1903371072357150782"
ALT = "『アンサンブル』のグッズ。まん中が松村北斗の演じる真戸原優のアクスタ(スーツ)"
TD = '<td style="border:1px solid #ccc;padding:8px 12px;">'
TDG = '<td style="border:1px solid #ccc;padding:8px 12px;background:#f5f5f5;">'
CHK = '<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid #333333;border-radius:3px;color:#333333;font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>'

def box(rows):
    ps = "".join(f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>' for i, (k, v) in enumerate(rows))
    return f'<!-- wp:html -->\n<div style="border:1px solid #d5d5d5;border-left:4px solid #333333;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f5f5f5;">{ps}</div>\n<!-- /wp:html -->'
def para(t): return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"
def h(t, lv=2):
    return (f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->' if lv == 3
            else f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->')

def figure():
    m = requests.get(f"{U}/wp-json/wp/v2/media?search=sixtones_ensemble_acsta_merch", auth=A, timeout=60).json()
    m = m[0] if m else requests.post(f"{U}/wp-json/wp/v2/media", data=IMG.read_bytes(), auth=A, timeout=120,
        headers={"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{IMG.name}"'}).json()
    requests.post(f"{U}/wp-json/wp/v2/media/{m['id']}", json={"alt_text": ALT}, auth=A, timeout=60)
    s = m["media_details"]["sizes"]; lg = s.get("large") or s["medium"]
    srcset = ", ".join(f'{s[k]["source_url"]} {s[k]["width"]}w' for k in ("medium", "medium_large") if k in s) + f', {m["source_url"]} {m["media_details"]["width"]}w'
    return (f'<!-- wp:image {{"id":{m["id"]},"sizeSlug":"large"}} -->\n<figure class="wp-block-image size-large"><img src="{lg["source_url"]}" alt="{ALT}" class="wp-image-{m["id"]}" '
            f'width="{lg["width"]}" height="{lg["height"]}" style="max-width:100%;height:auto;" srcset="{srcset}" sizes="(max-width: 1024px) 100vw, 1024px">'
            f'<figcaption style="font-size:0.8em;color:#888;">出典:{SRC_IMG}</figcaption></figure>\n<!-- /wp:image -->')

def section():
    return "\n\n".join([
        h("出演ドラマのアクスタ(2023年・2025年)"),
        para("メンバーが出たドラマのグッズとして、アクスタが売られたこともあります。<br>\nこちらはドラマに出たメンバーだけのアクスタです。"),
        h("『単身花日』(2023年)", 3),
        para("田中樹さんが出演した、テレビ朝日系のドラマ『単身花日』のグッズです。<br>\n主演はジャニーズWESTの重岡大毅さんでした。"),
        box([("発売日", "2023年10月14日(土)"), ("どこで", "ジャニーズドラマコレクション(オンラインだけ)"),
             ("いっしょに出たグッズ", "コレクションカード・ステッカーセット"), ("今は", "2024年10月15日に販売終了")]),
        para("お店では売られず、オンラインだけの販売でした。<br>\n値段は、公式の記録が見つからなかったので、ここでは書いていません。"),
        para('出典:<a href="https://x.com/MerchCompany_jp/status/1712309620281381277" target="_blank" rel="noopener">ファミクラストア(X)</a>'),
        h("『アンサンブル』(2025年)", 3),
        figure(),
        para("松村北斗さんが出演した、日本テレビ系のドラマ『アンサンブル』のグッズです。<br>\n松村北斗さんが演じた弁護士・真戸原優の<strong><span class=\"swl-marker mark_yellow\" style=\"font-size:1.15em;\">スーツ姿のアクスタ</span></strong>が出ました。"),
        box([("発売日", "オンラインは2025年1月17日(金)10時から、お店は1月28日(火)から"), ("どこで", "ファミクラストア(お店・オンライン)"),
             ("いっしょに出たグッズ", "コレクションカード・ふせん"), ("今は", "2026年1月15日にオンラインの販売が終了")]),
        para("ドラマの役の衣装のアクスタなので、ドラマの思い出として集めたファンも多いグッズです。<br>\n値段は、公式の記録が見つからなかったので、ここでは書いていません。"),
        para('出典:<a href="https://x.com/SixTONESinfo/status/1879485946477089074" target="_blank" rel="noopener">SixTONES info(X)</a>'),
    ])

def build():
    c = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()["content"]["raw"]
    if "出演ドラマのアクスタ" in c: sys.exit("already added")
    def rep(old, new):
        nonlocal c
        assert c.count(old) == 1, old[:60]; c = c.replace(old, new)
    # list table: insert 2 rows by date, then re-zebra
    row10 = f'<tr>{TD}2025年5月</td>'
    rep(row10, f'<tr>{TD}2023年10月</td>{TD}『単身花日』ドラマグッズ</td>{TD}公式の記録が見つからず</td></tr>\n'
               f'<tr>{TDG}2025年1月</td>{TDG}『アンサンブル』ドラマグッズ</td>{TDG}公式の記録が見つからず</td></tr>\n<tr>{TD}2025年5月</td>')
    rep("大きく分けると、ジャニーズJr.時代のもの、デビュー後のオンライン限定のもの、結成10周年のものの3つです。<br>\nどれもメンバー1人ずつの個人のアクスタで、6人分そろえて飾るファンも多いです。",
        "大きく分けると、Jr.時代のもの、オンライン限定のもの、ドラマのもの、結成10周年のものの4つです。<br>\nどれもメンバー1人ずつのアクスタです。<br>\nドラマ以外は6人分あるので、そろえて飾るファンも多いです。")
    rep(h("結成10周年の両面アクスタ(2025年)"), section() + "\n\n" + h("結成10周年の両面アクスタ(2025年)"))
    rep("これまでは記念日やオンラインの企画に合わせて出ていたので、", "これまでは記念日やオンラインの企画、ドラマに合わせて出ていたので、")
    rep(f'2022年のアクスタFestは各1,200円</p>',
        f'2022年のアクスタFestは各1,200円</p><p style="margin:6px 0 0 0;">{CHK}『単身花日』『アンサンブル』のドラマグッズにもアクスタがあった</p>')
    OUT.write_text(c, encoding="utf-8"); print("built", OUT, len(c))

def push():
    p = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}?context=edit", auth=A, timeout=60).json()
    rv = requests.get(f"{U}/wp-json/wp/v2/posts/{PID}/revisions", auth=A, timeout=60).json()
    print("latest revision", rv[0]["id"], "author", rv[0]["author"], rv[0]["modified"], "| post modified", p["modified"])
    if rv[0]["author"] != 1: sys.exit("someone else edited after us; stop")
    r = requests.post(f"{U}/wp-json/wp/v2/posts/{PID}", json={"content": OUT.read_text(encoding="utf-8")}, auth=A, timeout=60).json()
    print("updated", r["id"], r["status"], r["link"])

{"build": build, "push": push}[sys.argv[1]]()
