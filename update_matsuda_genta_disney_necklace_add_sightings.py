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

def get_post(post_id):
    req = urllib.request.Request(f"{SITE}/wp-json/wp/v2/posts/{post_id}?context=edit", headers={"Authorization": f"Basic {AUTH}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def update_content(post_id, content):
    payload = {"content": content, "status": "draft"}
    req = urllib.request.Request(
        f"{SITE}/wp-json/wp/v2/posts/{post_id}",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers=HEADERS_JSON,
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

POST_ID = 850
IMG_DIR = ROOT / "tools" / "Xiy" / "posts_matsuda_necklace_disney" / "x_images"

if __name__ == "__main__":
    print("Fetching current content...")
    post = get_post(POST_ID)
    content = post["content"]["raw"]

    print("Uploading pokapoka TV screenshot...")
    tv = upload_media(IMG_DIR / "pokapoka_tv.jpg", "matsuda_genta_pokapoka_necklace_tv.jpg",
                       alt="情報番組「ぽかぽか」出演時に太いゴールドチェーンネックレスを着用する松田元太")
    tv_sizes = tv["media_details"]["sizes"]
    tv_large = tv_sizes.get("large") or tv_sizes.get("full")
    tv_medium = tv_sizes.get("medium")
    tv_full = tv_sizes.get("full") or {"source_url": tv["source_url"], "width": tv["media_details"]["width"], "height": tv["media_details"]["height"]}
    tv_srcset = ", ".join(filter(None, [
        f"{tv_medium['source_url']} {tv_medium['width']}w" if tv_medium else None,
        f"{tv_large['source_url']} {tv_large['width']}w",
        f"{tv_full['source_url']} {tv_full['width']}w",
    ]))
    print("TV IMAGE", tv["id"], tv_large["source_url"])

    # 1. 「この記事でわかること」boxに項目追加
    old_box = """<li>写真が投稿された場面(ディズニーでのプライベートショット)</li>
<li>着用していたネックレスのブランド</li>
<li>ネックレスの価格帯</li>"""
    new_box = """<li>写真が投稿された場面(ディズニーでのプライベートショット)</li>
<li>着用していたネックレスのブランド</li>
<li>ネックレスの価格帯</li>
<li>「ぽかぽか」など他の番組でも着用していたか</li>"""
    assert old_box in content, "box not found"
    content = content.replace(old_box, new_box)

    # 2. どんな場面の写真?セクションに家族情報を追記
    old_para = """<!-- wp:paragraph -->
<p>今回話題になっているのは、松田元太さんの公式Instagramに投稿された複数枚の写真のうちの1枚です。<br>
投稿には「#スプラッシュマウンテン」「#トイストーリー」「#ファミリー時間」といったハッシュタグが添えられており、ディズニーパークで過ごしたプライベートな時間を振り返る内容になっています。<br>
キャプションでは他グループのデビューを祝う言葉や、妹の誕生日を祝う一文もつづられていて、家族思いな一面がうかがえる投稿です。<br>
その中の自撮りショットで、首元に重ねづけしたゴールドのネックレスがはっきりと写り込んでいたことから、ファンの間でブランド特定の話題が広がりました。</p>
<!-- /wp:paragraph -->"""
    new_para = """<!-- wp:paragraph -->
<p>今回話題になっているのは、松田元太さんの公式Instagramに投稿された複数枚の写真のうちの1枚です。<br>
投稿には「#スプラッシュマウンテン」「#トイストーリー」「#ファミリー時間」といったハッシュタグが添えられており、ディズニーパークで過ごしたプライベートな時間を振り返る内容になっています。<br>
キャプションでは他グループのデビューを祝う言葉に加え、「妹よ、誕生日おめでとう」という一文もつづられており、<strong>妹の誕生日を祝うために母・妹と3人で家族旅行としてディズニーを訪れた</strong>ことがうかがえる内容になっています。<br>
その中の自撮りショットで、首元に重ねづけしたゴールドのネックレスがはっきりと写り込んでいたことから、ファンの間でブランド特定の話題が広がりました。</p>
<!-- /wp:paragraph -->"""
    assert old_para in content, "para not found"
    content = content.replace(old_para, new_para)

    # 3. 「これは私物?」セクションの前に新セクションを挿入
    anchor = """<!-- wp:heading -->
<h2 class="wp-block-heading">これは私物?</h2>
<!-- /wp:heading -->"""
    new_section = f"""<!-- wp:heading -->
<h2 class="wp-block-heading">他の番組でも着用している?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>このネックレスが確認されたのは、今回のディズニーでのオフショットが初めてではありません。<br>
松田元太さんが月曜パーソナリティを務める情報番組「ぽかぽか」(フジテレビ系)でも、太めのゴールドチェーンネックレスを着けている姿がたびたび画面に映っており、ファンの間では放送のたびに話題になっています。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<figure class="wp-block-image size-large">
<img src="{{tv_large_url}}" alt="情報番組「ぽかぽか」出演時に太いゴールドチェーンネックレスを着用する松田元太" width="{{tv_large_w}}" height="{{tv_large_h}}" style="max-width:100%;height:auto;" srcset="{{tv_srcset}}" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption style="font-size:0.8em;color:#888;">出典:https://x.com/kidukudeshow/status/2071426836979134845</figcaption>
</figure>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>さらに2026年5月5日、福岡で行われたTravis Japanのファンミーティング「#stravelers」では、今回とほぼ同じティファニー ハードウェアのダイヤモンドネックレスを着用した姿が確認されており、ファンからは「合計9カラット以上のダイヤモンドが照明に当たって虹色に輝いていた」と話題になりました。<br>
FM大阪のレギュラーラジオ番組「Have a Nice Friday」の収録オフショットでもゴールドのネックレスを着けている様子が見られ、テレビ・ラジオ・プライベートを問わず愛用しているアイテムであることがうかがえます。</p>
<!-- /wp:paragraph -->

{anchor}"""
    new_section = new_section.replace("{tv_large_url}", tv_large["source_url"])
    new_section = new_section.replace("{tv_large_w}", str(tv_large["width"]))
    new_section = new_section.replace("{tv_large_h}", str(tv_large["height"]))
    new_section = new_section.replace("{tv_srcset}", tv_srcset)
    assert anchor in content, "anchor not found"
    content = content.replace(anchor, new_section)

    print("Updating post content...")
    result = update_content(POST_ID, content)
    print("UPDATED", result.get("id"), "status:", result.get("status"), "modified:", result.get("modified"))
