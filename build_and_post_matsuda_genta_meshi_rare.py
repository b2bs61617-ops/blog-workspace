import base64, json, os, mimetypes, urllib.request, urllib.parse, re
from pathlib import Path

ROOT = Path(__file__).parent

def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env

ENV = {**load_env(ROOT / ".env"), **os.environ}
SITE = ENV["WP_AUDITION_URL"].rstrip("/")
USER = ENV["WP_AUDITION_USERNAME"]
APP_PW = ENV["WP_AUDITION_APP_PASSWORD"]
AUTH = base64.b64encode(f"{USER}:{APP_PW}".encode()).decode()
HEADERS_JSON = {"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"}

def upload_media(filepath, filename, alt=None):
    data = Path(filepath).read_bytes()
    mime = mimetypes.guess_type(filename)[0] or "image/jpeg"
    req = urllib.request.Request(
        f"{SITE}/wp-json/wp/v2/media",
        data=data,
        method="POST",
        headers={
            "Authorization": f"Basic {AUTH}",
            "Content-Type": mime,
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        media = json.loads(r.read())
    if alt:
        try:
            req2 = urllib.request.Request(
                f"{SITE}/wp-json/wp/v2/media/{media['id']}",
                data=json.dumps({"alt_text": alt, "title": alt}).encode("utf-8"),
                method="POST",
                headers=HEADERS_JSON,
            )
            with urllib.request.urlopen(req2, timeout=30) as r:
                json.loads(r.read())
        except Exception as e:
            print("warn: could not set alt text", e)
    return media

def post_draft(title, content, slug, categories, author):
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "categories": categories,
        "author": author,
    }
    req = urllib.request.Request(
        f"{SITE}/wp-json/wp/v2/posts",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers=HEADERS_JSON,
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def set_featured(post_id, media_id):
    req = urllib.request.Request(
        f"{SITE}/wp-json/wp/v2/posts/{post_id}",
        data=json.dumps({"featured_media": media_id}).encode("utf-8"),
        method="POST",
        headers=HEADERS_JSON,
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def get_existing_post(post_id):
    req = urllib.request.Request(f"{SITE}/wp-json/wp/v2/posts/{post_id}", headers={"Authorization": f"Basic {AUTH}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def img_block(media, alt, source_url):
    sizes = media["media_details"]["sizes"]
    large = sizes.get("large") or sizes.get("full")
    medium = sizes.get("medium")
    full = sizes.get("full") or {"source_url": media["source_url"], "width": media["media_details"]["width"], "height": media["media_details"]["height"]}
    src = large["source_url"]
    w, h = large["width"], large["height"]
    srcset_parts = []
    if medium:
        srcset_parts.append(f"{medium['source_url']} {medium['width']}w")
    srcset_parts.append(f"{large['source_url']} {large['width']}w")
    srcset_parts.append(f"{full['source_url']} {full['width']}w")
    srcset = ", ".join(srcset_parts)
    return f'''<!-- wp:html -->
<figure class="wp-block-image size-large">
<img src="{src}" alt="{alt}" width="{w}" height="{h}" style="max-width:100%;height:auto;" srcset="{srcset}" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption style="font-size:0.8em;color:#888;">出典:{source_url}</figcaption>
</figure>
<!-- /wp:html -->
'''

IMAGES_DIR = Path(r"C:\Users\s30se\AppData\Local\Temp\claude\c--Users-s30se-OneDrive--------CHOMO\acc5f382-ce55-4330-beb2-54cebd3baf93\scratchpad\genta_meshi_rare")

if __name__ == "__main__":
    print("Uploading images...")
    m1 = upload_media(IMAGES_DIR / "tweet1_img1.jpg", "genta_meshi_rare_package.jpg", alt="「元太めし 元太ソーダ味」のパッケージと、中央に見える色違いのレア型")
    m2 = upload_media(IMAGES_DIR / "tweet1_img2.jpg", "genta_meshi_rare_closeup.jpg", alt="「元太めし 元太ソーダ味」のレア型を拡大したクローズアップ写真")
    m3 = upload_media(IMAGES_DIR / "tweet2_img1.jpg", "genta_meshi_hospital_konbini.jpg", alt="病院内のコンビニで見つかった「元太めし」の中身")
    eyecatch = upload_media(ROOT / "images" / "matsuda_genta_meshi_rare_eyecatch.png", "matsuda_genta_meshi_rare_eyecatch.png", alt="松田元太「元太めし」のレア型を紹介する記事のアイキャッチ")
    print("uploaded", m1["id"], m2["id"], m3["id"], "eyecatch", eyecatch["id"])

    img1_block = img_block(m1, "「元太めし 元太ソーダ味」のパッケージと、中央に見える色違いのレア型", "https://x.com/naty_tj7/status/2091753719662772727")
    img2_block = img_block(m2, "「元太めし 元太ソーダ味」のレア型を拡大したクローズアップ写真", "https://x.com/naty_tj7/status/2091753719662772727")
    img3_block = img_block(m3, "病院内のコンビニで見つかった「元太めし」の中身", "https://x.com/HiyoHiyori0221/status/2092124648473502003")

    TITLE = "元太めしの「レア型」って何？買えた場所も紹介！"
    SLUG = "genta-meshi-rare-type"

    CONTENT = f"""<!-- wp:paragraph -->
<p>Travis Japan・松田元太さん公認の「元太めし 元太ソーダ味」を買った人たちの間で、<strong><span class="swl-marker mark_blue" style="font-size:1.15em;">パッケージに"レア型"が入っている</span></strong>ことが話題になっています。<br>
実際に「元」の文字が浮き出たレア型を引き当てたという投稿や、病院内のコンビニで購入できたという声も出ています。<br>
この記事では、レア型の正体と、実際に見つかった投稿、買えた場所についてまとめます。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#eef6fd;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">商品情報</p>
<table style="border-collapse:collapse;width:100%;"><tbody>
<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;"><strong>商品名</strong></td><td style="border:1px solid #ccc;padding:8px 12px;">元太めし 元太ソーダ味</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;"><strong>発売日</strong></td><td style="border:1px solid #ccc;padding:8px 12px;">2026年8月24日(月)</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;"><strong>発売元</strong></td><td style="border:1px solid #ccc;padding:8px 12px;">UHA味覚糖株式会社</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;"><strong>公認タレント</strong></td><td style="border:1px solid #ccc;padding:8px 12px;">松田元太(Travis Japan)</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;background:#f0f0f0;"><strong>販売場所</strong></td><td style="border:1px solid #ccc;padding:8px 12px;">全国のスーパー・コンビニ</td></tr>
</tbody></table>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#5b9bd5;color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:#eef6fd;">
<li>パッケージに書かれた「レア型」の予告</li>
<li>実際に見つかった「元」の文字入りレア型</li>
<li>病院内のコンビニでの購入例</li>
<li>元太めしが買える場所</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">パッケージに「レア型が入っているかも」の予告</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#eef6fd;">
<p style="margin:0;"><strong>表示場所:</strong>パッケージ左下</p>
<p style="margin:4px 0 0 0;"><strong>文言:</strong>「レア型が入っているかも」+「?」マーク</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>「元太めし 元太ソーダ味」のパッケージをよく見ると、左下に「レア型が入っているかも」という文言と、赤い「?」マークが印刷されています。<br>
つまり、袋の中に入っている複数のラムネ状のタブレットのうち、まれに通常とは違う特別な形・見た目のものが混ざっている仕様だということです。<br>
お菓子のパッケージ自体にこうした"当たり"要素が明記されているのは珍しく、購入者の間で「本当に入っているのか」「どんな形なのか」と早くも話題になっていました。</p>
<!-- /wp:paragraph -->

{img1_block}

<!-- wp:heading -->
<h2 class="wp-block-heading">実際に「元」の文字入りレア型が見つかった</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#eef6fd;">
<p style="margin:0;"><strong>発見日:</strong>2026年8月24日</p>
<p style="margin:4px 0 0 0;"><strong>内容:</strong>1袋目で、「元」の文字が浮き出た色違いのレア型が出現</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>発売初日の2026年8月24日、Xでは<strong><span class="swl-marker mark_blue" style="font-size:1.15em;">1袋目でレア型を引き当てた</span></strong>という投稿が話題になりました。<br>
写真を見ると、通常の白いタブレットに混じって、黄色みがかった1粒だけ色が異なるものが確認できます。<br>
拡大すると、その1粒には「元」の文字が浮き彫りになっており、松田元太さんの名前にちなんだデザインになっていることがうかがえます。<br>
投稿には「『元』って入ってるの面白いね」「え、元太めしでレア型でたの!?それはテンション上がる」といった反応が寄せられ、発売初日から話題を集めました。</p>
<!-- /wp:paragraph -->

{img2_block}

<!-- wp:heading -->
<h2 class="wp-block-heading">病院内のコンビニでも購入できた</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#eef6fd;">
<p style="margin:0;"><strong>発見日:</strong>2026年8月25日</p>
<p style="margin:4px 0 0 0;"><strong>購入場所:</strong>病院内のコンビニ</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>発売翌日の2026年8月25日には、病院内に入っているコンビニで「元太めし」を見つけたという投稿もありました。<br>
袋を開けたタブレットの中に、他とは形が少し違って見える1粒が写っており、投稿者は「これはレア?」と気になった様子をつづっています。<br>
断定はできないものの、通常のスーパー・コンビニだけでなく病院内の売店のような場所にまで商品が行き渡っていたことがわかる投稿で、発売直後から幅広い店舗で展開されていたことがうかがえます。</p>
<!-- /wp:paragraph -->

{img3_block}

<!-- wp:heading -->
<h2 class="wp-block-heading">元太めしはどこで買える?</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#eef6fd;">
<p style="margin:0;"><strong>公式発表の販売場所:</strong>全国のスーパー・コンビニ</p>
<p style="margin:4px 0 0 0;"><strong>実際の目撃例:</strong>病院内のコンビニでも購入報告あり</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>発売元のUHA味覚糖は、公式Xアカウントで「元太めし 元太ソーダ味」について「8月24日(月)から全国のスーパーやコンビニで発売」と発表しており、特定のチェーン名までは明かしていません。<br>
既存の忍者めしシリーズがセブン-イレブンをはじめとする大手コンビニや全国のスーパー・ドラッグストアで幅広く扱われていることを踏まえると、「元太めし ソーダ味」も同様に広い販路で展開されているとみられます。<br>
実際、上で紹介した病院内のコンビニでの購入報告からも、発売直後の時点で相当数の店舗に商品が行き渡っていたことがうかがえます。<br>
近隣のスーパー・コンビニで見当たらない場合は、少し範囲を広げて別の店舗やドラッグストアも探してみると出会える可能性がありそうです。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">まとめ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>&#10003; 「元太めし 元太ソーダ味」のパッケージには「レア型が入っているかも」の文言があり、"当たり"要素が公式に予告されている</li>
<li>&#10003; 発売初日には、「元」の文字が浮き出た色違いのレア型を引き当てたという投稿が話題に</li>
<li>&#10003; 病院内のコンビニでも購入できたという報告があり、幅広い店舗で発売されている</li>
<li>&#10003; 公式発表の販売場所は全国のスーパー・コンビニ</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>発売直後からレア型の目撃情報が飛び交っている「元太めし ソーダ味」。<br>
これから購入する方は、袋を開けたら色や形が違うタブレットが混ざっていないか、ぜひチェックしてみてください!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#eef6fd;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">松田元太さんの関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-0.com/when-does-genta-meshi-soda-rel-607">「元太めし ソーダ味」の発売日・価格・商品概要をまとめた記事</a></li>
<li><a href="https://chomoand-0.com/how-much-is-the-gift-yamazaki-572">舞台『俺節』出演中に贈られた差し入れ「山崎18年」の価格を調査した記事</a></li>
<li><a href="https://chomoand-0.com/what-is-genta-matsudas-dressin-625">『俺節』の楽屋ルーティン・私物アイテムをまとめた記事</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

    print("Creating draft post...")
    AUTHOR_ID = 1  # b2bs61617@gmail.com固定(chomoand-0.com例外ルール)
    CATEGORIES = [3, 7]  # ジャニーズ + Travis Japan
    result = post_draft(TITLE, CONTENT, SLUG, categories=CATEGORIES, author=AUTHOR_ID)
    post_id = result["id"]
    print("CREATED", post_id, result.get("link"))

    print("Setting featured image...")
    set_featured(post_id, eyecatch["id"])
    print("DONE. Draft post ID:", post_id)
