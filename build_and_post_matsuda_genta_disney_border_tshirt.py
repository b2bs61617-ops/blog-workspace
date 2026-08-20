import base64, json, os, mimetypes, urllib.request
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

def get_media(media_id):
    req = urllib.request.Request(f"{SITE}/wp-json/wp/v2/media/{media_id}", headers={"Authorization": f"Basic {AUTH}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

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

EXISTING_SELFIE_MEDIA_ID = 848  # 既存記事(post 850)で使用中のディズニー自撮り画像を再利用
NECKLACE_POST_URL = "https://chomoand-0.com/?p=850"
SOURCE_URL = "https://x.com/geanyumita/status/2090266257471963494"
GENSTAGRAM_SOURCE_URL = "https://x.com/ebikanic/status/2090048548708688254"

if __name__ == "__main__":
    print("Fetching existing selfie media sizes...")
    selfie = get_media(EXISTING_SELFIE_MEDIA_ID)
    sizes = selfie["media_details"]["sizes"]
    s_large = sizes.get("large") or sizes.get("full")
    s_medium = sizes.get("medium")
    s_full = sizes.get("full") or {"source_url": selfie["source_url"], "width": selfie["media_details"]["width"], "height": selfie["media_details"]["height"]}
    s_srcset = ", ".join(filter(None, [
        f"{s_medium['source_url']} {s_medium['width']}w" if s_medium else None,
        f"{s_large['source_url']} {s_large['width']}w",
        f"{s_full['source_url']} {s_full['width']}w",
    ]))
    print("SELFIE", selfie["id"], s_large["source_url"])

    TITLE = "松田元太のディズニー私服ボーダーTシャツはMMIC?価格は?"
    SLUG = "matsuda-genta-disney-border-tshirt-mmic"

    CONTENT = f"""<!-- wp:paragraph -->
<p>Travis Japanの松田元太さんが、ディズニーでのプライベートショットで着けていたネックレスに続いて、その時に着ていたボーダーTシャツも話題になっています。<br>
調べたところ、<strong>着用していたのは「MMIC(エムエムアイシー)」の「SUNSTRIPE TEE」というボーダーTシャツ(¥7,530)</strong>とみられます。<br>
この記事では、Tシャツのブランドと、他の場面でも着用していたかについてまとめます。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#5b9bd5;color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:#eef6fd;">
<li>写真が投稿された場面(ディズニーでのプライベートショット)</li>
<li>着用していたボーダーTシャツのブランド</li>
<li>他の場面でも着用していたか</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">どんな場面の写真?ディズニーでのプライベートショット</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#eef6fd;">
<p style="margin:0;"><strong>投稿日:</strong>2026年8月19日</p>
<p style="margin:4px 0 0 0;"><strong>投稿内容:</strong>妹の誕生日を祝う家族でのディズニー旅行を振り返るオフショット</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>今回話題になっているのは、以前<a href="{NECKLACE_POST_URL}">松田元太さんが着けていたネックレスを特定した記事</a>でも取り上げた、公式Instagramに投稿されたディズニーでのオフショットです。<br>
妹の誕生日を祝うために母・妹と家族でディズニーを訪れた際の1枚で、赤とグレーのボーダーにレッドの襟をあしらったTシャツを着用しています。<br>
このボーダーTシャツについて、松田元太さんの私服を継続的に紹介しているファンアカウントが、ブランドと価格を特定して紹介していました。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<figure class="wp-block-image size-large">
<img src="{s_large['source_url']}" alt="ディズニーでのプライベートショットで、赤とグレーのボーダーTシャツを着用する松田元太" width="{s_large['width']}" height="{s_large['height']}" style="max-width:100%;height:auto;" srcset="{s_srcset}" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption style="font-size:0.8em;color:#888;">出典:{GENSTAGRAM_SOURCE_URL}</figcaption>
</figure>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">着用していたボーダーTシャツのブランドは?</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#eef6fd;">
<p style="margin:0;"><strong>ブランド:</strong>MMIC(エムエムアイシー)</p>
<p style="margin:4px 0 0 0;"><strong>商品名:</strong>SUNSTRIPE TEE(オレンジ)/¥7,530</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>着用していたのは、韓国発のブランド「MMIC」が展開する「SUNSTRIPE TEE」というボーダーTシャツで、カラー展開の中の「オレンジ」にあたるとみられます。<br>
写真では暗めの照明のせいでレンガ色に近い赤とグレーのシンプルなボーダー柄に見えますが、赤みの強いオレンジがボーダーラインに使われているデザインで、価格は7,530円と比較的手に取りやすい価格帯です。<br>
派手すぎない配色のボーダーTシャツで、ゴールドのネックレスを重ねづけしても浮かない絶妙なバランスが、私服コーディネートのセンスの良さを感じさせます。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">他の場面でも着用している?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>このボーダーTシャツが確認されたのは、ディズニーでのオフショットが初めてではないようです。<br>
松田元太さんの私服を紹介しているファンアカウントによると、FM大阪のレギュラーラジオ番組「げんラジ(Have a Nice Friday)」の収録時にも、同じボーダーTシャツを着用していたことが確認されています。<br>
ラジオ収録という仕事の場でも、プライベートのディズニーでも同じアイテムを着回している様子から、松田元太さんのお気に入りの1着であることがうかがえます。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">これは私物?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>今回のTシャツについて、本人や運営から「私物です」といった公式なコメントは出ていません。<br>
ただし、ラジオ収録の仕事着としてだけでなく、家族とのプライベートなディズニー旅行でも同じアイテムを着用していることから、<strong>私物である可能性が高い</strong>と考えられます。<br>
7,530円というアイテムとしては手に取りやすい価格帯であることも、日常的に愛用しやすいポイントといえそうです。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">まとめ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<ul style="margin:0;padding-left:1.2em;">
<li>写真は2026年8月19日、松田元太さんの公式Instagramに投稿された、妹の誕生日を祝う家族でのディズニー旅行のオフショット</li>
<li>ボーダーTシャツは<strong>MMICの「SUNSTRIPE TEE」(オレンジ、¥7,530)</strong>とみられる</li>
<li>FM大阪のラジオ収録時にも同じTシャツの着用が確認されており、私物として愛用している可能性が高い</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>1,000万円を超えるハイジュエリーのネックレスと、7,530円のシンプルなボーダーTシャツを違和感なく組み合わせるあたりに、松田元太さんならではの私服のセンスがうかがえますね。<br>
気になった方は、同じボーダーTシャツを普段のコーディネートに取り入れてみてはいかがでしょうか!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #bbdefb;border-left:4px solid #5b9bd5;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#eef6fd;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">松田元太さんの着用アイテム特定記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{NECKLACE_POST_URL}">同じディズニーでのショットで着用していたネックレスを特定した記事</a></li>
<li><a href="https://chomoand-0.com/?p=812">サマソニ衣装で着用していたベルトのブランドを調べた記事</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

    print(f"Creating draft post '{TITLE}'...")
    result = post_draft(TITLE, CONTENT, SLUG, categories=[3, 7], author=1)
    post_id = result["id"]
    print("CREATED post", post_id, result.get("link"))

    print("Setting featured image...")
    eyecatch_path = ROOT / "images" / "matsuda_genta_disney_border_tshirt_eyecatch.png"
    eyecatch = upload_media(eyecatch_path, "matsuda_genta_disney_border_tshirt_eyecatch.png",
                             alt="松田元太のディズニー私服ボーダーTシャツはMMIC?価格は?")
    set_featured(post_id, eyecatch["id"])
    print("DONE. Post ID:", post_id, "Edit URL:", f"{SITE}/wp-admin/post.php?post={post_id}&action=edit")
