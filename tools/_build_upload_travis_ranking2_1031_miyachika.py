# -*- coding: utf-8 -*-
"""One-off: 宮近海斗 ROLLING CRADLE x TM paint「TRIO THE CAPS / TORI-SAN」article (逆引きランキング第2弾 2026-10-31)
-> chomoand-4.blog draft, and update the brand table row in summary draft 2127."""
import re
import subprocess
import sys
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "tools/_build_travis_ranking2_1031.py").read_text(encoding="utf-8")
exec(src[:src.index("SCENE_ROWS = ")])  # THEMES, class A, VID, VTITLE
THEMES["miyachika"] = dict(main="#e57373", line="#f3d6d6", bg="#fdf3f3", th="#fbe6e6", mark="mark_red")
SCENE_ROWS = [("動画", VTITLE), ("公開", "2026年10月31日(Travis Japan公式YouTube)"), ("企画", "第2回TJメンバー逆引きランキング(7人全員参加)")]
SUMMARY_ID = 2127
PROD = "https://shop.rollingcradle.com/?pid=189667154"

a = A("miyachika")
a.p("2026年10月31日に公開されたTravis Japanの公式YouTube「逆引きランキング」の第2弾で、宮近海斗さんがかぶっていた黒のキャップが気になった方も多いはずです。",
    "正面には、オレンジの頭と青い体の鳥が3羽並んだ刺しゅうと、「ROLLING CRADLE」の文字が入っていました。",
    "調べてみたところ、このキャップは" + a.mark("ROLLING CRADLE(ローリングクレイドル)とイラストレーターのTM paintさんのコラボキャップ「TRIO THE CAPS / TORI-SAN」(5,500円)") + "とみられます。",
    "この記事では、キャップが映った場面とデザインの特徴、価格と買える場所をまとめます。")
a.wakaru(["宮近海斗さんのキャップが映った場面", "「TRIO THE CAPS / TORI-SAN」と一致するポイント", "ROLLING CRADLEとTM paintのコラボとは", "価格と今から買える場所"])
a.h2("宮近海斗のキャップが映ったのはどの場面？")
a.info(SCENE_ROWS + [("場面", "ほぼ全編(収録中ずっと同じキャップ)")])
a.p("逆引きランキングは、先にクジで1位から7位までの順位を決めて、その並びに当てはまるお題をあとから考える企画です。",
    "宮近さんは、黒の長袖のスウェットに黒のパンツを合わせた全身黒のコーディネートで、キャップも黒でまとめていました。",
    "首元には細いゴールドのチェーン、両耳には小ぶりのフープピアスを着けています。")
a.img("IMG_FRONT")
a.p("第2ラウンドで、宮近さんが自分のお題「一発ギャグ上手いランキング」を発表した場面では、フリップを持った宮近さんの正面がアップで映り、キャップの刺しゅうがはっきり見えます。")
a.h2("キャップはROLLING CRADLEの「TRIO THE CAPS / TORI-SAN」")
a.info([("ブランド", "ROLLING CRADLE(ローリングクレイドル)×TM paint"), ("商品名", "TRIO THE CAPS / TORI-SAN"), ("品番", "RC-C2857"),
        ("価格", "5,500円(税込)"), ("素材", "アクリル80%・ウール20%"), ("サイズ", "FREE")])
a.p("宮近さんがかぶっていたのは、ROLLING CRADLEの「TRIO THE CAPS / TORI-SAN」とみられます。",
    "キャップの正面を拡大して、公式の商品写真と見比べてみました。")
a.img("IMG_CAP")
a.checks(["黒のボディに、つばがまっすぐなスナップバックの形", "オレンジの頭と青い体の鳥が3羽、少しずつずれて並んだ刺しゅう", "鳥の頭の上に、白い羽根のような飾り", "鳥の足元に、白で「ROLLING CRADLE」の文字", "文字に鳥の足が重なるように入った配置"])
a.p("3羽の鳥の色や向き、文字との重なり方まで、商品写真とそろっていました。",
    "公式の商品名の「TRIO」は3羽、「TORI-SAN」は鳥さんのことで、デザインそのままの名前になっています。",
    "同じシリーズには、鳥の骨をレントゲン写真のように白で描いた色違いの「X-RAY」もあります。")
a.h2("ROLLING CRADLEとTM paintのコラボとは？")
a.p("ROLLING CRADLEは、カラフルなグラフィックのTシャツやキャップで知られる国内のブランドです。",
    "公式のWEB STOREには、ロックバンドのROTTENGRAFFTYさんやdustboxさん、フェス「AIR JAM 2026」とのコラボアイテムも並んでいて、ライブハウスやフェスのシーンとつながりの深いブランドです。")
a.p("TM paintさんは、国内外のアーティストのCDのジャケットやライブポスター、Tシャツなどを手がけているイラストレーターです。",
    "公式の商品ページでは、TM paintさん本人が「鳥オザキャップス！生身のトリさんとレントゲントリさんを被り比べてみてください。」とコメントしています。",
    "ROLLING CRADLEとTM paintさんのコラボでは、同じ鳥のキャラクターを使ったメッシュキャップやTシャツも出ていました。")
a.h2("値段と買える場所は？")
a.table(["項目", "内容"], [["ブランド", "ROLLING CRADLE×TM paint"], ["商品名", "TRIO THE CAPS / TORI-SAN(RC-C2857)"], ["価格", "5,500円(税込)"],
                         ["販売方法", "受注予約(2026年2月中旬〜下旬にお届け)"], ["2026年11月3日時点", "公式WEB STOREでは売り切れの表示"]])
a.p("このキャップは受注予約のアイテムで、12月23日までに注文を受け付け、2026年2月中旬から下旬にかけて届けられました。",
    "2026年11月3日に確認したところ、公式のWEB STOREの一覧では" + a.mark("SOLD OUT(売り切れ)") + "の表示になっていました。",
    "価格は5,500円と、宮近さんの私服の中では手に取りやすい1点です。")
a.p("いま手に入れるなら、フリマアプリや古着のお店で「ROLLING CRADLE TRIO THE CAPS」と探すのが近道です。",
    "再販や新しいコラボがあるかどうかは、ROLLING CRADLEの公式SNSで告知されることが多いので、チェックしておくと安心です。")
a.box("購入先", [f'<a href="{PROD}" target="_blank" rel="noopener">TRIO THE CAPS / TORI-SAN|ROLLING CRADLE公式WEB STORE</a>',
               "フリマアプリ・古着店(在庫は要確認)"])
a.h2("宮近海斗はキャップ好き？")
a.p("宮近さんは、ふだんの私服でもキャップをかぶっていることが多いメンバーです。",
    "2026年9月のコストコの動画では6CRAYONのフラットトップのキャップ、松田元太さんのストーリーでは'47とCarharttのコラボキャップをかぶっていました。",
    "ハイブランドから、今回のようなイラストの入ったキャップまで、幅広く取り入れているのが宮近さんらしいところです。")
a.h2("逆引きランキングでの宮近海斗")
a.p("この動画で宮近さんは、第1ラウンドで1位になり、松田さんの「初対面で正直からみにくいランキング」では「ミステリアス」「最初はあんまり喋らない」と言われていました。",
    "自分で考えた「一発ギャグ上手いランキング」では、メンバーに一発ギャグをやらせた責任を取って、自分も「ゲッツ」を披露しています。")
a.img("IMG_GETSU")
a.p("第3ラウンドの松倉海斗さんの「海外で外出歩くランキング」では、松田さんと並んで「気づいたらもう外にいない」「朝コーヒーに行く」タイプと言われていました。",
    f"動画の内容は<a href=\"https://chomoand-4.blog/?p={SUMMARY_ID}\">逆引きランキング第2弾のまとめ記事</a>で紹介しています。")
a.h2("まとめ")
a.matome(["2026年10月31日公開の逆引きランキング第2弾で、宮近海斗さんは鳥が3羽並んだ黒のキャップをかぶっていた",
          "キャップはROLLING CRADLE×TM paintのコラボ「TRIO THE CAPS / TORI-SAN」(RC-C2857)とみられる",
          "価格は5,500円(税込)で、受注予約で販売された", "2026年11月3日時点で公式WEB STOREでは売り切れの表示"])
a.related([("202", "宮近海斗がコストコでかぶってた帽子は6CRAYONと判明！"), ("693", "宮近海斗の帽子は'47×Carhartt？松田元太のストーリーで着用確認"),
           ("1695", "宮近海斗の白Tシャツはどこの？ケルティのロゴTと判明！"), (str(SUMMARY_ID), "トラジャ逆引きランキング第2弾のまとめ")])
fn = ROOT / "articles/travis_ranking2_1031_miyachika.html"
a.save(fn.name)
subprocess.run([sys.executable, str(ROOT / "tools/honorific.py"), "fix", "--group", "travis", "--names", "TM paint", str(fn)], check=True)
html = fn.read_text(encoding="utf-8")

env = {}
for l in open(ROOT / ".env", encoding="utf-8"):
    l = l.strip()
    if "=" in l and not l.startswith("#"):
        k, v = l.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
U = env["WP_CHOMO4_URL"].rstrip("/")
AU = (env["WP_CHOMO4_USERNAME"], env["WP_CHOMO4_APP_PASSWORD"])
SRC = f'<a href="{VID}" target="_blank" rel="noopener">Travis Japan公式YouTube「【ランキング】今度は７人で逆引き！」</a>'


def upload(path):
    r = requests.post(f"{U}/wp-json/wp/v2/media", auth=AU, data=path.read_bytes(), headers={
        "Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{path.name}"'}, timeout=180)
    r.raise_for_status()
    return r.json()


IMGS = {"IMG_FRONT": ("chaka_rank1031_front.jpg", "鳥が3羽並んだ黒のキャップをかぶりフリップを持つ宮近海斗", "9:35ごろ"),
        "IMG_CAP": ("chaka_rank1031_cap.jpg", "宮近海斗のキャップの3羽の鳥とROLLING CRADLEの刺しゅう", "9:35ごろ、キャップを拡大"),
        "IMG_GETSU": ("chaka_rank1031_getsu.jpg", "一発ギャグのゲッツを披露する宮近海斗", "12:20ごろ")}
for ph, (f, alt, cap) in IMGS.items():
    m = upload(ROOT / "images" / f)
    s = m["media_details"]["sizes"]
    lg = s.get("large", s["full"]); md = s.get("medium", lg); fu = s["full"]
    html = html.replace(f"<!-- {ph} -->", f'<!-- wp:html -->\n<figure class="wp-block-image size-large">\n'
                        f'<img src="{lg["source_url"]}" alt="{alt}" width="{lg["width"]}" height="{lg["height"]}" style="max-width:100%;height:auto;" '
                        f'srcset="{md["source_url"]} {md["width"]}w, {lg["source_url"]} {lg["width"]}w, {fu["source_url"]} {fu["width"]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
                        f'<figcaption style="font-size:0.8em;color:#888;">出典:{SRC}({cap})</figcaption>\n</figure>\n<!-- /wp:html -->')
assert "<!-- IMG_" not in html
ey = upload(ROOT / "images/tj_rank2_1031_miyachika_eyecatch_canva.jpg")
r = requests.post(f"{U}/wp-json/wp/v2/posts", auth=AU, json={
    "title": "【未】宮近海斗の鳥のキャップはどこの？ROLLING CRADLEと判明！", "content": html,
    "slug": "miyachika-kaito-rolling-cradle-trio-the-caps", "status": "draft",
    "categories": [3, 9], "author": 2, "featured_media": ey["id"]}, timeout=180)
r.raise_for_status()
pid = r.json()["id"]
print("POST miyachika", pid, r.json()["status"], "chars", len(re.sub(r"\s", "", re.sub(r"<[^>]+>", "", html))))

# summary 2127: update brand table row + explanatory paragraph
p = requests.get(f"{U}/wp-json/wp/v2/posts/{SUMMARY_ID}", auth=AU, params={"context": "edit"}).json()
raw = p["content"]["raw"]
old_cell = "ROLLING CRADLE(モデルは未特定)"
assert old_cell in raw
raw = raw.replace(old_cell, f'<a href="https://chomoand-4.blog/?p={pid}">ROLLING CRADLE×TM paint</a>')
m = re.search(r"<p>宮近さんのキャップは、正面に.*?</p>", raw, re.S)
assert m
raw = raw.replace(m.group(0), "<p>宮近さんのキャップは、ROLLING CRADLEとイラストレーターのTM paintさんのコラボキャップ「TRIO THE CAPS / TORI-SAN」(5,500円)とみられます。<br>\n"
                  f'詳しくは<a href="https://chomoand-4.blog/?p={pid}">宮近海斗の鳥のキャップの記事</a>で紹介しています。</p>')
r = requests.post(f"{U}/wp-json/wp/v2/posts/{SUMMARY_ID}", auth=AU, json={"content": raw, "status": "draft"}, timeout=180)
r.raise_for_status()
print("UPDATED summary", SUMMARY_ID, r.json()["status"])
