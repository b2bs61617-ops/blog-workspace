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

IMG_DIR = ROOT / "tools" / "Xiy" / "posts_matsuda_necklace_disney" / "x_images"

if __name__ == "__main__":
    print("Uploading selfie photo (necklace close-up)...")
    selfie = upload_media(IMG_DIR / "x_img1.jpg", "matsuda_genta_disney_necklace_selfie.jpg",
                           alt="ディズニーでのプライベートショットで、重ねづけしたゴールドのネックレスを着用する松田元太")
    selfie_sizes = selfie["media_details"]["sizes"]
    s_large = selfie_sizes.get("large") or selfie_sizes.get("full")
    s_medium = selfie_sizes.get("medium")
    s_full = selfie_sizes.get("full") or {"source_url": selfie["source_url"], "width": selfie["media_details"]["width"], "height": selfie["media_details"]["height"]}
    s_srcset = ", ".join(filter(None, [
        f"{s_medium['source_url']} {s_medium['width']}w" if s_medium else None,
        f"{s_large['source_url']} {s_large['width']}w",
        f"{s_full['source_url']} {s_full['width']}w",
    ]))
    print("SELFIE", selfie["id"], s_large["source_url"])

    print("Uploading Tiffany official product comparison image...")
    product = upload_media(IMG_DIR / "x_img2.jpg", "matsuda_genta_disney_necklace_tiffany_product.jpg",
                            alt="ティファニー公式サイトのハードウェア グラジュエイテッド リンク ネックレス(イエローゴールド×パヴェダイヤモンド)の商品画像")
    product_sizes = product["media_details"]["sizes"]
    p_large = product_sizes.get("large") or product_sizes.get("full")
    p_medium = product_sizes.get("medium")
    p_full = product_sizes.get("full") or {"source_url": product["source_url"], "width": product["media_details"]["width"], "height": product["media_details"]["height"]}
    p_srcset = ", ".join(filter(None, [
        f"{p_medium['source_url']} {p_medium['width']}w" if p_medium else None,
        f"{p_large['source_url']} {p_large['width']}w",
        f"{p_full['source_url']} {p_full['width']}w",
    ]))
    print("PRODUCT", product["id"], p_large["source_url"])

    TITLE = "【松田元太】ディズニー着用ネックレスはティファニー?価格は?"
    SLUG = "matsuda-genta-disney-necklace-tiffany"
    SOURCE_URL = "https://x.com/ebikanic/status/2090048548708688254"

    CONTENT = f"""<!-- wp:paragraph -->
<p>Travis Japanの松田元太さんが、ディズニーでのプライベートショットを投稿したInstagramの中で着けていたネックレスが話題になっています。<br>
調べたところ、<strong>着用していたのはTiffany &amp; Co.(ティファニー)の「ハードウェア グラジュエイテッド リンク ネックレス」</strong>とみられます。<br>
この記事では、写真が投稿された場面と、ネックレスのブランド・価格帯についてまとめます。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#5b9bd5;color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:#eef6fd;">
<li>写真が投稿された場面(ディズニーでのプライベートショット)</li>
<li>着用していたネックレスのブランド</li>
<li>ネックレスの価格帯</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">どんな場面の写真?ディズニーでのプライベートショット</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#eef6fd;">
<p style="margin:0;"><strong>投稿日:</strong>2026年8月19日</p>
<p style="margin:4px 0 0 0;"><strong>投稿内容:</strong>ディズニーでの家族時間を振り返るオフショット</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>今回話題になっているのは、松田元太さんの公式Instagramに投稿された複数枚の写真のうちの1枚です。<br>
投稿には「#スプラッシュマウンテン」「#トイストーリー」「#ファミリー時間」といったハッシュタグが添えられており、ディズニーパークで過ごしたプライベートな時間を振り返る内容になっています。<br>
キャプションでは他グループのデビューを祝う言葉や、妹の誕生日を祝う一文もつづられていて、家族思いな一面がうかがえる投稿です。<br>
その中の自撮りショットで、首元に重ねづけしたゴールドのネックレスがはっきりと写り込んでいたことから、ファンの間でブランド特定の話題が広がりました。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<figure class="wp-block-image size-large">
<img src="{s_large['source_url']}" alt="ディズニーでのプライベートショットで、重ねづけしたゴールドのネックレスを着用する松田元太" width="{s_large['width']}" height="{s_large['height']}" style="max-width:100%;height:auto;" srcset="{s_srcset}" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption style="font-size:0.8em;color:#888;">出典:{SOURCE_URL}</figcaption>
</figure>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">着用していたネックレスのブランドは?</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#eef6fd;">
<p style="margin:0;"><strong>ブランド:</strong>Tiffany &amp; Co.(ティファニー)</p>
<p style="margin:4px 0 0 0;"><strong>商品名:</strong>ハードウェア グラジュエイテッド リンク ネックレス</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>写真に写るネックレスは、太めのゴールドチェーンの中央部分にダイヤモンドをあしらったリンクが連なるデザインで、Tiffany &amp; Co.の「ティファニー ハードウェア(Tiffany HardWear)」シリーズの「グラジュエイテッド リンク ネックレス」とほぼ同じ意匠であることが確認できます。<br>
ハードウェアシリーズは、無骨なチェーンパーツを大胆に組み合わせたデザインが特徴で、シルバーからイエロー・ローズ・ホワイトゴールドまで素材展開されている定番ラインです。<br>
中でもグラジュエイテッド リンクは、太さの異なるリンクを段階的(グラジュエイテッド)に配置し、中央にパヴェダイヤモンドをあしらった華やかなデザインが特徴で、松田元太さんが着けていたのもイエローゴールド×ダイヤモンドの組み合わせに近い見た目でした。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<figure class="wp-block-image size-large">
<img src="{p_large['source_url']}" alt="ティファニー公式サイトのハードウェア グラジュエイテッド リンク ネックレス(イエローゴールド×パヴェダイヤモンド)の商品画像" width="{p_large['width']}" height="{p_large['height']}" style="max-width:100%;height:auto;" srcset="{p_srcset}" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption style="font-size:0.8em;color:#888;">出典:{SOURCE_URL}(ティファニー公式サイトの商品画像)</figcaption>
</figure>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">気になる価格は?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>ティファニー ハードウェアのグラジュエイテッド リンク ネックレスは、素材やダイヤモンドの有無によって価格帯に大きな幅があります。<br>
一番手に取りやすいスターリングシルバーのシンプルなタイプで<strong>45万円前後</strong>、ダイヤモンドを使わないイエローゴールドのタイプでも<strong>330万円前後</strong>という価格帯です。<br>
一方、松田元太さんが着けていたようなパヴェダイヤモンドをあしらったゴールドの上位モデルになると価格は一気に跳ね上がり、ホワイトゴールド×ダイヤモンドのタイプで1,000万円台に達するモデルも存在します。<br>
今回話題になった投稿でも、参考価格として<strong>1,468万5,000円</strong>という金額が紹介されており、ハードウェアシリーズの中でもかなり上位のモデルにあたることがうかがえます。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">これは私物?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>今回のネックレスについて、本人や運営から「私物です」といった公式なコメントは出ていません。<br>
ただし、写真が投稿されたのは仕事のオフショットではなく、家族とディズニーで過ごした時間を振り返る本人の公式Instagram投稿であることを踏まえると、<strong>私物である可能性が高い</strong>と考えられます。<br>
1,000万円を超えるハイジュエリーをプライベートの外出時にも身につけているとすれば、松田元太さんのアクセサリー選びのこだわりの強さがうかがえるエピソードといえそうです。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">まとめ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>写真は2026年8月19日、松田元太さんの公式Instagramに投稿されたディズニーでのプライベートショット</li>
<li>ネックレスは<strong>Tiffany &amp; Co.「ハードウェア グラジュエイテッド リンク ネックレス」</strong>とみられる</li>
<li>シリーズの価格帯は45万円台〜1,000万円台まで幅広く、今回のモデルの参考価格は1,468万5,000円と紹介されている</li>
<li>仕事のオフショットではなくプライベートな投稿での着用のため、私物である可能性が高い</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>普段のステージ衣装だけでなく、家族との時間にもハイブランドのジュエリーをさりげなく取り入れている松田元太さんのセンスには驚かされますね。<br>
気になった方は、ティファニー ハードウェアシリーズの他のラインナップもチェックしてみてはいかがでしょうか!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#eef6fd;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">松田元太さんの着用アイテム特定記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-0.com/?p=812">サマソニ衣装で着用していたベルトのブランドを調べた記事</a></li>
<li><a href="https://chomoand-0.com/?p=638">On My Roadで履いていたスニーカーを特定した記事</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

    print(f"Creating draft post '{TITLE}'...")
    result = post_draft(TITLE, CONTENT, SLUG, categories=[3, 7], author=1)
    post_id = result["id"]
    print("CREATED post", post_id, result.get("link"))

    print("Setting featured image...")
    eyecatch_path = ROOT / "images" / "matsuda_genta_disney_necklace_eyecatch.png"
    eyecatch = upload_media(eyecatch_path, "matsuda_genta_disney_necklace_eyecatch.png",
                             alt="【松田元太】ディズニー着用ネックレスはティファニー?価格は?")
    set_featured(post_id, eyecatch["id"])
    print("DONE. Post ID:", post_id, "Edit URL:", f"{SITE}/wp-admin/post.php?post={post_id}&action=edit")
