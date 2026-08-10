# -*- coding: utf-8 -*-
import json, base64, os, re, urllib.request, urllib.parse
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

FRAME_DIR = Path(
    r"C:\Users\s30se\AppData\Local\Temp\claude\c--Users-s30se-OneDrive--------CHOMO\081b291d-b063-4ebc-bfba-1785432edfb9\scratchpad\frames"
)

VIDEO_URL = "https://youtu.be/bipgdNcr3ok"


def upload_media(filepath: Path, filename: str, content_type: str):
    data = filepath.read_bytes()
    headers = {
        **HEADERS_AUTH,
        "Content-Type": content_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=data)
    r.raise_for_status()
    return r.json()


EXISTING_MEDIA_IDS = [11080, 11081, 11082]

if all(EXISTING_MEDIA_IDS):
    print("reusing already-uploaded images...", EXISTING_MEDIA_IDS)
    img1_media, img2_media, img3_media = [
        requests.get(f"{WP_URL}/wp-json/wp/v2/media/{mid}", headers=HEADERS_AUTH).json()
        for mid in EXISTING_MEDIA_IDS
    ]
else:
    print("uploading images...")
    img1_media = upload_media(FRAME_DIR / "frame_320.jpg", "keito_night_routine_ledmask.jpg", "image/jpeg")
    img2_media = upload_media(FRAME_DIR / "frame_372.jpg", "keito_night_routine_ems.jpg", "image/jpeg")
    img3_media = upload_media(FRAME_DIR / "frame_440.jpg", "keito_night_routine_protein.jpg", "image/jpeg")
print("img1", img1_media["id"], "img2", img2_media["id"], "img3", img3_media["id"])


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


VIDEO_CAPTION = f'出典:KO1KEYZ公式YouTube「🌙 KO1KEYZ Night Routine...⭐️」({VIDEO_URL})'
img1_html = f"<!-- wp:html -->\n{build_img_html(img1_media, 'KEITOがLEDマスク型の美顔器をつけながらストレッチしているシーン', VIDEO_CAPTION)}\n<!-- /wp:html -->"
img2_html = f"<!-- wp:html -->\n{build_img_html(img2_media, 'KEITOが白いハンズフリー型の美顔器を顔に当てているシーン', VIDEO_CAPTION)}\n<!-- /wp:html -->"
img3_html = f"<!-- wp:html -->\n{build_img_html(img3_media, 'KEITOがプロテインシェイカーを振っているシーン', VIDEO_CAPTION)}\n<!-- /wp:html -->"


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def hr():
    return '<!-- wp:separator --><hr class="wp-block-separator has-alpha-channel-opacity"/><!-- /wp:separator -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def capbox(ttl, rows, style="is-style-small_ttl"):
    tds = "\n".join(
        f'<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;white-space:nowrap;">{k}</td>'
        f'<td style="border:1px solid #ccc;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return wphtml(f'''<div class="swell-block-capbox cap_box {style}">
<div class="cap_box_ttl">{ttl}</div>
<div class="cap_box_content">
<table style="border-collapse:collapse;width:100%;"><tbody>
{tds}
</tbody></table>
</div>
</div>''')


def capbox_list(ttl, items, style="is-style-small_ttl"):
    lis = "\n".join(f"<li>「{t}」</li>" for t in items)
    return wphtml(f'''<div class="swell-block-capbox cap_box {style}">
<div class="cap_box_ttl">{ttl}</div>
<div class="cap_box_content">
<ul>
{lis}
</ul>
</div>
</div>''')


title = "KO1KEYZ慶人の美顔器はいくら?ナイトルーティンで判明"

blocks = []

blocks.append(p([
    "KO1KEYZの公式YouTubeチャンネルで、メンバーそれぞれのお風呂上がりから就寝までを追った「🌙 KO1KEYZ Night Routine...⭐️」が公開されました。",
    "そのなかでもKEITO(小野慶人)のパートは<strong>美顔器を2種類使い分ける本格的なスキンケア</strong>が披露されており、Xでは使用アイテムの合計金額を計算する投稿まで登場して話題になっています。",
    "この記事では、KEITOが使っている美顔器の正体と価格、そしてナイトルーティン全体の流れを詳しく紹介します。",
]))
blocks.append(hr())

blocks.append(h2("動画情報"))
blocks.append(capbox("動画情報", [
    ("動画タイトル", "🌙 KO1KEYZ Night Routine...⭐️"),
    ("チャンネル", "KO1KEYZ公式YouTube"),
    ("公開日", "2026年8月10日"),
    ("出演", "DAIKI・ISSA・KEITO・KOSUKE・RYOGA・RYUJI・SHINHAENG・SIYOUNG・TOWA・YOSHIKI・YUKI・YURAの12人(この記事ではKEITOのパートを中心に紹介)"),
    ("URL", f'<a href="{VIDEO_URL}" target="_blank" rel="noopener">{VIDEO_URL}</a>'),
]))
blocks.append(hr())

blocks.append(h2("KEITO(小野慶人)はどんな人?"))
blocks.append(capbox("KEITOのプロフィール", [
    ("本名", "小野慶人(おの けいと)"),
    ("生年月日", "2000年7月25日"),
    ("年齢", "25歳(KO1KEYZ最年長)"),
    ("出身地", "高知県"),
    ("身長", "172cm"),
    ("MBTI", "ENTJ"),
    ("日プでの成績", "最終順位7位(408,598票)、圏外からのランクアップでデビューを掴む"),
]))
blocks.append(p([
    "KEITOは『PRODUCE 101 JAPAN 新世界』参加前、平日は<a href=\"https://chomoand-1.com/keito_work-10086\" target=\"_blank\" rel=\"noopener\">会社員として働きながら美容情報を発信するクリエイター</a>としても活動していた経歴の持ち主です。",
    "Popteenや MEN'S VOCE といったファッション・美容誌でモデルも務めており、美容にまつわる知識と経験の蓄積は12人のなかでも群を抜いています。",
    "以前公開されていた愛用スキンケアの調査記事(<a href=\"https://chomoand-1.com/keito_no_item-109\" target=\"_blank\" rel=\"noopener\">小野慶人の美容法まとめ！愛用スキンケアや美肌の秘訣を徹底調査！</a>)でも保湿と透明感ケアへのこだわりが紹介されていましたが、今回のナイトルーティンではさらに踏み込んだ美顔器のこだわりが明らかになりました。",
]))
blocks.append(hr())

blocks.append(h2("お風呂上がりから就寝まで、こだわりの美容ルーティン"))
blocks.append(wphtml('''<div style="border:1px solid #f3caa0;border-left:4px solid #e8871e;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#fff6ea;">
<p style="margin:0;"><strong>流れ:</strong>入浴→ストレッチをしながら美顔器(10分)→青汁→スキンケア(美顔器2回)→ドライヤー→かっさ→プロテインで就寝</p>
</div>'''))
blocks.append(img1_html)
blocks.append(p([
    "動画はKEITOが「早速お風呂に入ってきます」と言って浴室へ向かうシーンからスタートします。",
    "お風呂上がりにまず取り入れているのが柔軟(ストレッチ)で、その間にLEDマスク型の美顔器を装着し、赤く光る画面を見せながら「美顔器が10分なので、10分柔軟しながら時間を無駄にしないように使ってます」とコメント。",
    "ストレッチと並行して毎日青汁を飲むことも習慣にしているそうで、限られた時間のなかでケアと体調管理を同時に済ませる効率の良さがうかがえます。",
    "美顔器を外したあとは化粧水にたどり着くまでにいくつもの工程があるというスキンケアへ移り、髪を乾かしてから翌朝のむくみを防ぐための軽いかっさで締めくくるという、かなり丁寧な流れになっていました。",
]))
blocks.append(hr())

blocks.append(h2("判明した美顔器は2種類、合計いくら?"))
blocks.append(img2_html)
blocks.append(p([
    "動画に映っていた美顔器を確認したところ、性質の異なる2つの機器を使い分けていることが分かりました。",
    "1つ目は入浴後のストレッチタイムに装着していたLEDマスク型の機器で、CurrentBody Skin(カレントボディスキン)の「LEDライトセラピーマスク シリーズ2」とみられます。",
    "赤色を中心としたLEDライトを肌に照射するタイプの美顔器で、世界的にもシェアの大きいブランドの上位モデルです。",
    "2つ目はスキンケアの工程で顔に当てていた白いハンズフリー型の機器で、資生堂とヤーマンが共同開発した美容ブランド「EFFECTIM(エフェクティム)」の「クイック フェイシャル トレーナー」と特徴が一致します。",
    "独自の「干渉波EMS」技術により、わずか3分の使用で表情筋に働きかける設計になっている美顔器です。",
]))
blocks.append(capbox("使用アイテムの価格まとめ", [
    ("CurrentBody Skin LEDライトセラピーマスク シリーズ2", "77,000円(税込)"),
    ("EFFECTIM クイック フェイシャル トレーナー", "59,400円(税込)"),
    ("<strong>合計</strong>", "<strong>136,400円(税込)</strong>"),
], style="is-style-onborder_ttl"))
blocks.append(p([
    "2つ合わせると税込<strong>136,400円</strong>という金額になり、Xでもこの合計額を算出した投稿が反応を集めていました。",
    "動画内でKEITOは、2つ目のEFFECTIMについて「明日撮影あるんでむくみを予防するための美顔器」と説明しており、翌日の仕事に向けたコンディション調整として使い分けている様子が伝わってきます。",
    "スキンケアの最後には「明日の朝むくみたくないっていう時は夜もやってますが、朝も起きたらやります」とも話しており、朝晩どちらのタイミングでも使えるアイテムとして活用しているようです。",
]))
blocks.append(hr())

blocks.append(h2("撮影前ならではの、プロテインで締めくくる夜"))
blocks.append(img3_html)
blocks.append(p([
    "スキンケアと髪を乾かし終えたあと、KEITOは「今日夜ご飯が早かったからめっちゃお腹が減ってて」と空腹を明かしつつも、「とはいえむくみたくないし夜も遅いし明日撮影なのでプロテインを飲んで寝ます」と、あえて食事ではなくプロテインを選んで一日を締めくくっていました。",
    "美顔器でむくみ予防に気を配った直後だけに、就寝前の食事内容にも同じ意識が向いていることが分かるシーンです。",
    "美容情報発信者としての経験に裏打ちされた、体の内側と外側の両方をケアする姿勢が垣間見えるナイトルーティンでした。",
]))
blocks.append(hr())

blocks.append(h2("SNSでの反応"))
blocks.append(capbox_list("美顔器の光量に驚く声", [
    "美顔器のあまりの光量にビビり散らかしてる神",
    "声裏返ってるかわいい",
    "ガチで慌てた声しててwww",
]))
blocks.append(capbox_list("美容へのこだわりに反応する声", [
    "小野慶人と美顔器の組み合わせがおもしろい",
    "この美顔器ほしくてずっとカートに入れてるけど未だに買えず……",
    "彼の信条がまず身体は食べるものから作られるだろうから、美顔器ってそこクリアした後なんよね",
]))
blocks.append(p([
    "動画公開直後から、美顔器の存在感や使い方の丁寧さに驚く声が多く見られました。",
    "なかには気になっていても価格の高さから購入をためらっているという共感の声もあり、136,400円という金額のインパクトの大きさがうかがえます。",
]))
blocks.append(hr())

blocks.append(h2("まとめ"))
blocks.append(wphtml('''<div class="swell-block-capbox cap_box is-style-small_ttl">
<div class="cap_box_ttl">KEITOのナイトルーティンまとめ</div>
<div class="cap_box_content">
<p class="has-border -border02 wp-block-paragraph">
✔ <strong>使用アイテム</strong>:CurrentBody Skin LEDライトセラピーマスク シリーズ2(77,000円)+EFFECTIM クイック フェイシャル トレーナー(59,400円)<br>
✔ <strong>合計金額</strong>:136,400円(税込)<br>
✔ <strong>使うタイミング</strong>:入浴後のストレッチ中と、スキンケアの工程内(むくみ予防)<br>
✔ <strong>締めくくり</strong>:翌日撮影のため夜食の代わりにプロテインを選択<br>
✔ <strong>背景</strong>:デビュー前から美容クリエイター・モデルとして活動していた経歴
</p>
<p>元美容クリエイターというキャリアそのままに、機材選びから使うタイミングまで理にかなったナイトルーティンでした。<br>
まだKEITOの美容知識に詳しくないという人も、これをきっかけに本編の動画も見てみてはいかがでしょうか!</p>
</div>
</div>'''))
blocks.append(p([
    "KEITOについては、このブログの他の記事でも詳しく紹介しています。",
]))
blocks.append(wphtml('''<ul>
<li><a href="https://chomoand-1.com/keito_work-10086" target="_blank" rel="noopener">会社員時代の勤務先を調査した記事</a></li>
<li><a href="https://chomoand-1.com/keito_zoff-7563" target="_blank" rel="noopener">愛用メガネのブランドを調査した記事</a></li>
<li><a href="https://chomoand-1.com/meimon-keitooo-71" target="_blank" rel="noopener">出身高校・大学の学歴を調査した記事</a></li>
<li><a href="https://chomoand-1.com/ono-keito-p101-68" target="_blank" rel="noopener">モデル・クリエイターとしての経歴をまとめた記事</a></li>
<li><a href="https://chomoand-1.com/keito_no_item-109" target="_blank" rel="noopener">愛用スキンケアアイテムをまとめた記事</a></li>
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


EXISTING_POST_ID = 11083

if EXISTING_POST_ID:
    payload = {"content": content, "status": "draft"}
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{EXISTING_POST_ID}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print("UPDATED POST_ID", post["id"])
else:
    slug = get_slug(title, "ko1keyz-keito-beauty-device-p")
    print("slug:", slug)
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "categories": [66, 63],
        "author": 2,
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

with open(ROOT / "tmp_keito_night_routine_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
