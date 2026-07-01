import sys, os, base64, json, urllib.request
from PIL import Image, ImageDraw, ImageFont

WP_URL = "https://chomoand.com/wp-json/wp/v2"
WP_USER = "b2bs61617@gmail.com"
WP_PASS = "yXsF iR9W C8bS lQRz KQfO ynwD"
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS = {"Authorization": f"Basic {AUTH}"}

ARTICLES = [
    (11458, "【花田藍衣】契約解除の理由なぜ？", "坊主を強要された真相と今後を徹底解説！", "速報・炎上"),
    (11459, "【花田藍衣】学歴・高校はどこ？",   "捜真女学校出身！偏差値や中学も調査！",   "学歴・経歴"),
    (11460, "【花田藍衣】家族構成を調査！",       "姉や両親について徹底リサーチ！",           "家族・プロフィール"),
    (11461, "【花田藍衣】趣味や特技は？",         "魚をさばくヒロアカ好きアイドルの素顔！",   "趣味・特技"),
]

FONT_PATHS = [
    "C:/Windows/Fonts/YuGothB.ttc",
    "C:/Windows/Fonts/YuGothR.ttc",
    "C:/Windows/Fonts/meiryo.ttc",
    "C:/Windows/Fonts/msgothic.ttc",
]

def get_font(size, bold=True):
    for p in FONT_PATHS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                continue
    return ImageFont.load_default()

def draw_gradient(draw, width, height):
    for y in range(height):
        r = int(255 - (y / height) * 55)
        g = int(230 - (y / height) * 50)
        b = int(235 + (y / height) * 10)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def make_eyecatch(post_id, line1, line2, tag, out_dir="images"):
    os.makedirs(out_dir, exist_ok=True)
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), (255, 230, 235))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, W, H)

    # 外枠
    draw.rectangle([18, 18, W-18, H-18], outline=(255,255,255), width=7)
    draw.rectangle([30, 30, W-30, H-30], outline=(210, 140, 170), width=3)

    # タグ帯
    draw.rectangle([75, 65, 380, 120], fill=(180, 100, 140))
    f_tag = get_font(22)
    draw.text((95, 75), tag, font=f_tag, fill=(255,255,255))

    # ハート装飾
    for pos in [(60,55), (W-80,55), (60,H-75), (W-80,H-75)]:
        draw.text(pos, "♥", font=get_font(36), fill=(255,200,220))

    # メインタイトル line1（影付き）
    f1 = get_font(52)
    draw.text((62, 152), line1, font=f1, fill=(80,30,60))
    draw.text((60, 150), line1, font=f1, fill=(170, 50, 100))

    # メインタイトル line2
    f2 = get_font(40)
    draw.text((62, 222), line2, font=f2, fill=(80,30,60))
    draw.text((60, 220), line2, font=f2, fill=(150, 60, 110))

    # ピンク帯（下部）
    draw.rectangle([0, 490, W, 580], fill=(190, 100, 140))
    f_sub = get_font(22, bold=False)
    draw.text((60, 510), "chomoand.com | トレンドブログ", font=f_sub, fill=(255,255,255))

    path = f"{out_dir}/hanada_mei_{post_id}_eyecatch.png"
    img.save(path, "PNG")
    return path

def upload_media(filepath, filename):
    with open(filepath, "rb") as f:
        data = f.read()
    req = urllib.request.Request(
        f"{WP_URL}/media",
        data=data,
        method="POST",
        headers={
            "Authorization": f"Basic {AUTH}",
            "Content-Type": "image/png",
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def set_featured(post_id, media_id):
    payload = json.dumps({"featured_media": media_id}).encode()
    req = urllib.request.Request(
        f"{WP_URL}/posts/{post_id}",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Basic {AUTH}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

for post_id, line1, line2, tag in ARTICLES:
    print(f"\n[{post_id}] {line1[:20]}...")
    path = make_eyecatch(post_id, line1, line2, tag)
    print(f"  画像生成: {path}")
    fname = os.path.basename(path)
    media = upload_media(path, fname)
    media_id = media["id"]
    print(f"  アップロード: media_id={media_id}")
    set_featured(post_id, media_id)
    print(f"  アイキャッチ設定完了 → https://chomoand.com/?p={post_id}")

print("\n全記事のアイキャッチ設定が完了しました！")
