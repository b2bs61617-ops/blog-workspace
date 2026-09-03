# -*- coding: utf-8 -*-
import json, base64, os, subprocess, sys
from pathlib import Path
from urllib.parse import quote

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

# TOWA yellow-green (黄緑) accent, matching the existing TOWA nail-ring article
G_ACCENT = "#6fa843"
G_BORDER = "#d7e7bf"
G_BG = "#f5f9ed"
BUY_BORDER = "#ddd9d3"
BUY_BAR = "#8a8378"
BUY_BG = "#f7f6f4"

# published TOWA related articles
L_GIVENCHY = "https://chomoand-1.com/towa-givenchy-tshirt-siyoung-dance-11855"
L_LOUNGE = "https://chomoand-1.com/what-brand-is-towas-loungewear-11093"
L_JAGAIMO = "https://chomoand-1.com/is-towas-new-character-jagaimo-11691"
L_WIKI = "https://chomoand-1.com/hamadatowa_wiki-2452"

# purchase links
MORN_OFFICIAL = "https://morn-creations.jp/collections/" + quote("シャーク")
AMZ = "https://www.amazon.co.jp/s?k=" + quote("MORN CREATIONS シャークバックパック L")
RAKUTEN = "https://search.rakuten.co.jp/search/mall/" + quote("MORN CREATIONS シャークバックパック")
YAHOO = "https://shopping.yahoo.co.jp/search?p=" + quote("MORN CREATIONS シャークバックパック")


def post_draft(title, content, slug, lang, categories, featured_media, summary, translations=None):
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "draft",
        "lang": lang,
        "categories": categories,
        "featured_media": featured_media,
        "author": 2,
        "meta": {"jetpack_publicize_message": summary},
    }
    if translations:
        payload["translations"] = translations
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    return r.json()


def make_eyecatch(args, out_path):
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"), *args, "--out", str(out_path)],
        check=True,
    )
    mr = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HEADERS_AUTH, "Content-Type": "image/png",
                 "Content-Disposition": f'attachment; filename="{out_path.name}"'},
        data=out_path.read_bytes(),
    )
    mr.raise_for_status()
    return mr.json()["id"]


# ============================== JP ==============================
JP_TITLE = "TOWAが空港で背負ってたサメリュックのブランドは？"
JP_SLUG = "towa-airport-shark-backpack"

JP_CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZ(コイキーズ)のTOWA(濱田永遠)さんが、空港で移動する姿を見かけたというXの投稿があり、そのとき背負っていた大きめのリュックが話題になりました。<br>
大きく開いたサメの口がそのままデザインになった特徴的なリュックで、正体は<strong>香港のバッグブランド「MORN CREATIONS(モーン・クリエイションズ)」のシャークバックパック(Lサイズ・ブラック)</strong>とみられます。<br>
参考価格は<strong>14,300円(税込)</strong>です。<br>
この記事では、リュックのデザインの特徴、ブランドの成り立ち、サイズ展開、そして価格と購入先までまとめます。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">TOWA着用リュックの基本情報</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:32%;">アイテム</td><td style="border:1px solid #ccc;padding:8px 12px;">バックパック(リュック)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">ブランド</td><td style="border:1px solid #ccc;padding:8px 12px;">MORN CREATIONS(モーン・クリエイションズ)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">モデル</td><td style="border:1px solid #ccc;padding:8px 12px;">シャークバックパック L(品番 SK-101)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">カラー</td><td style="border:1px solid #ccc;padding:8px 12px;">ブラック</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">参考価格</td><td style="border:1px solid #ccc;padding:8px 12px;">14,300円(税込)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">TOWAが空港で背負っていたのはどんなリュック？</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>きっかけは、空港でTOWAさんを見かけたというXの投稿でした。<br>
移動中のオフショットで、黒くて大きなリュックを背負っている姿が写っており、そのインパクトのある見た目からどこのバッグなのか気になるファンが多かったようです。<br>
本人や運営からの公式なアイテム紹介ではありませんが、移動中に背負っていたことから、衣装ではなく私物とみられます。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>このリュックの一番の特徴は、<span class="swl-marker mark_green">正面が大きく開いたサメの口をかたどっている</span>ことです。<br>
上あごと下あごにギザギザの白い歯がぐるりと並び、口の内側は赤。<br>
遠目には黒いシンプルなバックパックに見えますが、近くで見るとひと目で「サメ」とわかる、遊び心のあるデザインになっています。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">ブランドはMORN CREATIONS(モーン・クリエイションズ)</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>調べてみたところ、このサメのリュックは<span class="swl-marker mark_green" style="font-size:1.15em;"><strong>香港のバッグブランド「MORN CREATIONS(モーン・クリエイションズ)」の「シャークバックパック」</strong></span>で間違いなさそうです。<br>
量販店やセレクトショップ、公式オンラインストアで長く売られている定番モデルで、KO1KEYZファンだけでなく雑貨好きの間でも知られた存在です。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">MORN CREATIONS(モーン・クリエイションズ)とは？</p>
<p style="margin:0;">香港のデザイナー、スティーブ・チャン(Steve Chan)が手がけるバッグブランド。<br>
2001年に香港・ソーホーで雑貨店「MORN」を開き、2004年に「MORN CREATIONS」を立ち上げました。<br>
パンダやフクロウ、サメなど動物をモチーフにしたバッグが看板で、「動物を人間のパートナーとして守ろう」というメッセージが込められています。<br>
なかでもサメ(シャーク)シリーズはブランドを代表するロングセラーです。</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>サメシリーズには、映画で怖いイメージがつきがちなサメへの誤解を解きたい、フカヒレ目的の乱獲で数を減らしているサメを知ってほしい、というデザイナーの思いがあります。<br>
口が大きく開くのは、上あご・下あごがそのまま2つの収納スペースになっているため。<br>
実用性と見た目のインパクトを両立させた作りが、20年近く愛されている理由と言えそうです。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">サイズ・カラーは？</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>シャークバックパックにはS・M・L・LLの4サイズがあり、ほかにワンショルダーのスリングバッグやウエストポーチも展開されています。<br>
TOWAさんが背負っていたのは、日常使いに一番人気のあるLサイズ(容量約20L)のブラックとみられます。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">シャークバックパックのサイズ展開</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:18%;">サイズ</td><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">寸法(約)</td><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">容量・重さ(約)</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;">S</td><td style="border:1px solid #ccc;padding:8px 12px;">25×19×13cm</td><td style="border:1px solid #ccc;padding:8px 12px;">5L / 250g</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;">M</td><td style="border:1px solid #ccc;padding:8px 12px;">36×27×15cm</td><td style="border:1px solid #ccc;padding:8px 12px;">11L / 450g</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;"><strong>L</strong></td><td style="border:1px solid #ccc;padding:8px 12px;"><strong>43×32×20cm</strong></td><td style="border:1px solid #ccc;padding:8px 12px;"><strong>20L / 550g</strong></td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;">LL</td><td style="border:1px solid #ccc;padding:8px 12px;">43×37×23cm</td><td style="border:1px solid #ccc;padding:8px 12px;">23L / ―(コーデュラ素材)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Lサイズの素材は撥水性のあるナイロンで、上あご・下あごの2気室はどちらもダブルジッパー。<br>
両サイドのエラの部分がベルクロ留めのポケットになっていて、肩ひもと背面にはパッドが入っています。<br>
カラーはブラックのほかにグレーやネイビーがあり、ネイビー×マスタードのようなツートンの「コンビ」ラインも選べます。<br>
A4サイズが入り、1〜2泊の荷物なら十分まかなえる容量なので、移動の多いアイドルの機内持ち込み用としても使いやすいサイズ感です。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">価格は？どこで買える？</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>シャークバックパックのLサイズは、定価<span class="swl-marker mark_green" style="font-size:1.15em;"><strong>14,300円(税込)</strong></span>です。<br>
ひとつ大きいLLサイズは16,500円前後、SサイズやウエストポーチはSNSでも手に取りやすい価格で販売されています。<br>
ハイブランドのバッグではなく、学生でも狙いやすい価格帯なのがうれしいところです。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_ACCENT};color:#fff;">シャークバックパックの購入先</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li style="margin:0 0 8px 0;"><a href="{MORN_OFFICIAL}" target="_blank" rel="noopener">MORN CREATIONS 公式オンラインストア(シャークシリーズ)</a></li>
<li style="margin:0 0 8px 0;"><a href="{AMZ}" target="_blank" rel="noopener">Amazonで「MORN CREATIONS シャークバックパック L」を探す</a></li>
<li style="margin:0 0 8px 0;"><a href="{RAKUTEN}" target="_blank" rel="noopener">楽天市場で「MORN CREATIONS シャークバックパック」を探す</a></li>
<li style="margin:0;"><a href="{YAHOO}" target="_blank" rel="noopener">Yahoo!ショッピングで「MORN CREATIONS シャークバックパック」を探す</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>定番モデルなので在庫は比較的安定していますが、ブラックのLサイズは人気で品切れになることもあります。<br>
サイズ違いで見え方がかなり変わるので、可能なら実店舗で背負って大きさを確かめてから選ぶと失敗が少ないでしょう。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">まとめ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:2px solid {G_ACCENT};border-radius:8px;background:rgba(111,168,67,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; TOWAが空港で背負っていたのはMORN CREATIONSの「シャークバックパック」<br>
&#10003; サイズはLサイズ(容量約20L)、カラーはブラックとみられる<br>
&#10003; MORN CREATIONSは香港発の動物モチーフバッグブランド、サメシリーズが看板<br>
&#10003; Lサイズの参考価格は14,300円(税込)。公式通販や大手モールで購入できる
</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>派手すぎず、でも背負うとしっかり目を引くサメリュックは、TOWAさんのくだけた雰囲気ともよく合っています。<br>
気になった人は、まずは公式オンラインストアでサイズとカラーをチェックしてみてはいかがでしょうか！</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">TOWA(濱田永遠)の関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">TOWAがSIYOUNGとの動画で着ていたGIVENCHYのTシャツを調べた記事</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">TOWAの部屋着(GELATO PIQUE×ドラえもん)のブランドを調べた記事</a></li>
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">TOWAの新キャラクター「じゃがいもっぷりん」を紹介した記事</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">TOWA(濱田永遠)のwiki風プロフィール・経歴をまとめた記事</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

JP_SUMMARY = "KO1KEYZ・TOWAが空港で背負っていた大きめのリュックは、香港のバッグブランドMORN CREATIONSの「シャークバックパック」Lサイズ(ブラック)とみられます。サメの口をかたどった定番モデルで、参考価格は14,300円(税込)です。"

JP_EYECATCH_ID = make_eyecatch(
    ["--top", "TOWAが空港で背負ってたリュックは？", "--main", "KO1KEYZ", "--bottom", "サメの正体はMORN CREATIONS！"],
    ROOT / "images" / "towa_airport_shark_backpack_eyecatch.png",
)
print("JP_EYECATCH_ID", JP_EYECATCH_ID)

jp_post = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, "ja", [66, 63, 104], JP_EYECATCH_ID, JP_SUMMARY)
JP_POST_ID = jp_post["id"]
print("JP_POST_ID", JP_POST_ID, jp_post["slug"], jp_post.get("link"))


# ============================== KR ==============================
KR_TITLE = "TOWA가 공항에서 멨던 상어 백팩 브랜드는?"
KR_SLUG = f"{JP_SLUG}-kr"

KR_CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZ의 TOWA(하마다 토와)가 공항에서 이동하는 모습을 봤다는 X 게시물이 올라오면서, 그때 메고 있던 큼직한 백팩이 화제가 되었습니다.<br>
크게 벌어진 상어 입이 그대로 디자인이 된 독특한 백팩으로, 정체는 <strong>홍콩의 가방 브랜드 'MORN CREATIONS(모온 크리에이션스)'의 샤크 백팩(L 사이즈・블랙)</strong>으로 보입니다.<br>
참고가는 <strong>14,300엔(세금 포함)</strong>입니다.<br>
이 글에서는 백팩 디자인의 특징, 브랜드의 성립, 사이즈 전개, 그리고 가격과 구입처까지 정리합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">TOWA 착용 백팩의 기본 정보</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:32%;">아이템</td><td style="border:1px solid #ccc;padding:8px 12px;">백팩</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">브랜드</td><td style="border:1px solid #ccc;padding:8px 12px;">MORN CREATIONS(모온 크리에이션스)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">모델</td><td style="border:1px solid #ccc;padding:8px 12px;">샤크 백팩 L(품번 SK-101)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">컬러</td><td style="border:1px solid #ccc;padding:8px 12px;">블랙</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">참고가</td><td style="border:1px solid #ccc;padding:8px 12px;">14,300엔(세금 포함)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">TOWA가 공항에서 멘 것은 어떤 백팩?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>계기는 공항에서 TOWA를 봤다는 X 게시물이었습니다.<br>
이동 중의 오프숏으로, 검고 커다란 백팩을 메고 있는 모습이 찍혀 있어, 그 임팩트 있는 겉모습 때문에 어디 가방인지 궁금해하는 팬이 많았던 것 같습니다.<br>
본인이나 운영 측의 공식 아이템 소개는 아니지만, 이동 중에 메고 있었던 점에서 무대 의상이 아닌 사물로 보입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>이 백팩의 가장 큰 특징은 <span class="swl-marker mark_green">앞면이 크게 벌어진 상어 입을 본떴다</span>는 점입니다.<br>
위턱과 아래턱에 뾰족한 흰 이빨이 빙 둘러 나 있고, 입 안쪽은 빨간색.<br>
멀리서 보면 검고 심플한 백팩처럼 보이지만, 가까이서 보면 한눈에 '상어'라고 알 수 있는 장난기 있는 디자인입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">브랜드는 MORN CREATIONS(모온 크리에이션스)</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>알아본 결과, 이 상어 백팩은 <span class="swl-marker mark_green" style="font-size:1.15em;"><strong>홍콩의 가방 브랜드 'MORN CREATIONS(모온 크리에이션스)'의 '샤크 백팩'</strong></span>으로 틀림없어 보입니다.<br>
대형 매장이나 셀렉트 숍, 공식 온라인 스토어에서 오래 팔리고 있는 스테디셀러로, KO1KEYZ 팬뿐 아니라 잡화를 좋아하는 사람들 사이에서도 알려진 존재입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">MORN CREATIONS(모온 크리에이션스)란?</p>
<p style="margin:0;">홍콩의 디자이너 스티브 찬(Steve Chan)이 이끄는 가방 브랜드.<br>
2001년 홍콩 소호에 잡화점 'MORN'을 열었고, 2004년에 'MORN CREATIONS'를 시작했습니다.<br>
판다, 부엉이, 상어 등 동물을 모티프로 한 가방이 간판이며, '동물을 인간의 파트너로서 지키자'는 메시지가 담겨 있습니다.<br>
그중에서도 상어(샤크) 시리즈는 브랜드를 대표하는 롱셀러입니다.</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>샤크 시리즈에는 영화로 인해 무서운 이미지가 굳어지기 쉬운 상어에 대한 오해를 풀고 싶다, 샥스핀 목적의 남획으로 수가 줄고 있는 상어를 알아줬으면 한다는 디자이너의 마음이 담겨 있습니다.<br>
입이 크게 벌어지는 것은 위턱・아래턱이 그대로 두 개의 수납 공간이 되기 때문입니다.<br>
실용성과 임팩트 있는 겉모습을 양립시킨 만듦새가 20년 가까이 사랑받는 이유라고 할 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">사이즈・컬러는?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>샤크 백팩에는 S・M・L・LL 4가지 사이즈가 있고, 이 밖에 원숄더 슬링백이나 웨이스트 파우치도 전개되고 있습니다.<br>
TOWA가 메고 있던 것은 일상용으로 가장 인기 있는 L 사이즈(용량 약 20L)의 블랙으로 보입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">샤크 백팩 사이즈 전개</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:18%;">사이즈</td><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">치수(약)</td><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">용량・무게(약)</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;">S</td><td style="border:1px solid #ccc;padding:8px 12px;">25×19×13cm</td><td style="border:1px solid #ccc;padding:8px 12px;">5L / 250g</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;">M</td><td style="border:1px solid #ccc;padding:8px 12px;">36×27×15cm</td><td style="border:1px solid #ccc;padding:8px 12px;">11L / 450g</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;"><strong>L</strong></td><td style="border:1px solid #ccc;padding:8px 12px;"><strong>43×32×20cm</strong></td><td style="border:1px solid #ccc;padding:8px 12px;"><strong>20L / 550g</strong></td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;">LL</td><td style="border:1px solid #ccc;padding:8px 12px;">43×37×23cm</td><td style="border:1px solid #ccc;padding:8px 12px;">23L / ―(코듀라 소재)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>L 사이즈의 소재는 발수성이 있는 나일론이며, 위턱・아래턱의 2개 수납칸은 모두 더블 지퍼.<br>
양옆 아가미 부분이 벨크로로 여미는 포켓으로 되어 있고, 어깨끈과 등판에는 패드가 들어가 있습니다.<br>
컬러는 블랙 외에 그레이나 네이비가 있고, 네이비×머스터드 같은 투톤의 '콤비' 라인도 고를 수 있습니다.<br>
A4 사이즈가 들어가고 1~2박 짐이면 충분히 감당할 수 있는 용량이라, 이동이 많은 아이돌의 기내 반입용으로도 쓰기 좋은 사이즈감입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">가격은? 어디서 살 수 있을까?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>샤크 백팩 L 사이즈는 정가 <span class="swl-marker mark_green" style="font-size:1.15em;"><strong>14,300엔(세금 포함)</strong></span>입니다.<br>
한 단계 큰 LL 사이즈는 16,500엔 전후, S 사이즈나 웨이스트 파우치는 SNS에서도 부담 없이 살 수 있는 가격에 판매되고 있습니다.<br>
하이브랜드 가방이 아니라 학생도 노리기 쉬운 가격대인 점이 반갑습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_ACCENT};color:#fff;">샤크 백팩 구입처</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li style="margin:0 0 8px 0;"><a href="{MORN_OFFICIAL}" target="_blank" rel="noopener">MORN CREATIONS 공식 온라인 스토어(샤크 시리즈)</a></li>
<li style="margin:0 0 8px 0;"><a href="{AMZ}" target="_blank" rel="noopener">Amazon에서 'MORN CREATIONS 샤크 백팩 L' 검색</a></li>
<li style="margin:0 0 8px 0;"><a href="{RAKUTEN}" target="_blank" rel="noopener">라쿠텐 시장에서 'MORN CREATIONS 샤크 백팩' 검색</a></li>
<li style="margin:0;"><a href="{YAHOO}" target="_blank" rel="noopener">Yahoo! 쇼핑에서 'MORN CREATIONS 샤크 백팩' 검색</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>스테디셀러라서 재고는 비교적 안정적이지만, 블랙 L 사이즈는 인기가 있어 품절될 때도 있습니다.<br>
사이즈에 따라 보이는 느낌이 꽤 달라지므로, 가능하면 오프라인 매장에서 메어 보고 크기를 확인한 뒤 고르면 실패가 적습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">정리</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:2px solid {G_ACCENT};border-radius:8px;background:rgba(111,168,67,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; TOWA가 공항에서 메고 있던 것은 MORN CREATIONS의 '샤크 백팩'<br>
&#10003; 사이즈는 L 사이즈(용량 약 20L), 컬러는 블랙으로 보임<br>
&#10003; MORN CREATIONS는 홍콩발 동물 모티프 가방 브랜드, 샤크 시리즈가 간판<br>
&#10003; L 사이즈 참고가는 14,300엔(세금 포함). 공식 통판이나 대형 몰에서 구입 가능
</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>과하지 않으면서도 메면 확실히 눈길을 끄는 상어 백팩은, TOWA의 편안한 분위기와도 잘 어울립니다.<br>
궁금해진 분은 우선 공식 온라인 스토어에서 사이즈와 컬러를 확인해 보는 건 어떨까요!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">TOWA(하마다 토와) 관련 글</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">TOWA가 SIYOUNG과의 영상에서 입은 GIVENCHY 티셔츠를 알아본 글</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">TOWA의 룸웨어(GELATO PIQUE×도라에몽) 브랜드를 알아본 글</a></li>
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">TOWA의 새 캐릭터 '자가이못푸린'을 소개한 글</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">TOWA(하마다 토와)의 위키풍 프로필・경력을 정리한 글</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

KR_SUMMARY = "KO1KEYZ TOWA가 공항에서 메고 있던 큼직한 백팩은 홍콩 가방 브랜드 MORN CREATIONS의 '샤크 백팩' L 사이즈(블랙)로 보입니다. 상어 입을 본뜬 스테디셀러 모델로 참고가는 14,300엔(세금 포함)입니다."

KR_EYECATCH_ID = make_eyecatch(
    ["--top", "TOWA가 공항에서 멘 백팩은?", "--main", "KO1KEYZ", "--bottom", "정체는 MORN CREATIONS 상어!", "--lang", "kr"],
    ROOT / "images" / "towa_airport_shark_backpack_eyecatch_kr.png",
)
print("KR_EYECATCH_ID", KR_EYECATCH_ID)

kr_post = post_draft(KR_TITLE, KR_CONTENT, KR_SLUG, "ko", [74, 78, 104], KR_EYECATCH_ID, KR_SUMMARY,
                     translations={"ja": JP_POST_ID})
print("KR_POST_ID", kr_post["id"], kr_post["slug"], kr_post.get("link"))


# ============================== EN ==============================
EN_TITLE = "What Brand Is TOWA's Shark Backpack Seen at the Airport?"
EN_SLUG = f"{JP_SLUG}-en"

EN_CONTENT = f"""<!-- wp:paragraph -->
<p>A post on X said KO1KEYZ's TOWA (Towa Hamada) was spotted moving through an airport, and the oversized backpack he had on drew a lot of attention.<br>
It's a distinctive bag shaped like a wide-open shark's mouth, and it turns out to be the <strong>Shark Backpack (size L, black) from the Hong Kong bag brand "MORN CREATIONS"</strong>.<br>
The reference price is <strong>14,300 yen (tax incl.)</strong>.<br>
This article covers the bag's design, the brand's background, the size lineup, and the price and where to buy it.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">TOWA's backpack at a glance</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:32%;">Item</td><td style="border:1px solid #ccc;padding:8px 12px;">Backpack</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Brand</td><td style="border:1px solid #ccc;padding:8px 12px;">MORN CREATIONS</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Model</td><td style="border:1px solid #ccc;padding:8px 12px;">Shark Backpack L (code SK-101)</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Color</td><td style="border:1px solid #ccc;padding:8px 12px;">Black</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Reference price</td><td style="border:1px solid #ccc;padding:8px 12px;">14,300 yen (tax incl.)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What kind of backpack was it?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>It started with a post on X from someone who saw TOWA at an airport.<br>
The candid travel shot showed him carrying a big black backpack, and its bold look had a lot of fans wondering which brand it was.<br>
There's no official item note from TOWA or the agency, but since he was carrying it while traveling, it looks like a personal item rather than a stage piece.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>The bag's signature feature is that <span class="swl-marker mark_green">the front is molded into a wide-open shark's mouth</span>.<br>
Jagged white teeth run all the way around the upper and lower jaw, and the inside of the mouth is red.<br>
From a distance it reads as a plain black backpack, but up close it's unmistakably a shark — a playful design.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The brand is MORN CREATIONS</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Digging into it, this shark bag is almost certainly the <span class="swl-marker mark_green" style="font-size:1.15em;"><strong>"Shark Backpack" from the Hong Kong bag brand "MORN CREATIONS"</strong></span>.<br>
It's a long-running staple sold at big retailers, select shops and the brand's own online store, and it's well known not just to KO1KEYZ fans but to people who like quirky goods in general.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">What is MORN CREATIONS?</p>
<p style="margin:0;">A bag brand from Hong Kong designer Steve Chan.<br>
He opened a homeware shop called "MORN" in Hong Kong's Soho in 2001, then launched "MORN CREATIONS" in 2004.<br>
Its signature products are bags built around animal motifs — panda, owl, shark and more — carrying a message to protect animals as human partners.<br>
The shark series is the brand's defining long-seller.</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>The shark series reflects the designer's wish to undo the scary image movies have given sharks, and to draw attention to how overfishing for shark-fin soup has cut their numbers.<br>
The mouth opens so wide because the upper and lower jaws double as two separate storage compartments.<br>
Pairing everyday usefulness with an eye-catching shape is a big part of why it has lasted for close to 20 years.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Sizes and colors</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The Shark Backpack comes in four sizes — S, M, L and LL — plus one-shoulder sling bags and waist pouches.<br>
What TOWA had on looks like the L size (about 20L capacity) in black, the most popular pick for everyday use.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">Shark Backpack size lineup</p>
<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:18%;">Size</td><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Dimensions (approx.)</td><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">Capacity / weight (approx.)</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;">S</td><td style="border:1px solid #ccc;padding:8px 12px;">25×19×13cm</td><td style="border:1px solid #ccc;padding:8px 12px;">5L / 250g</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;">M</td><td style="border:1px solid #ccc;padding:8px 12px;">36×27×15cm</td><td style="border:1px solid #ccc;padding:8px 12px;">11L / 450g</td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;"><strong>L</strong></td><td style="border:1px solid #ccc;padding:8px 12px;"><strong>43×32×20cm</strong></td><td style="border:1px solid #ccc;padding:8px 12px;"><strong>20L / 550g</strong></td></tr>
<tr><td style="border:1px solid #ccc;padding:8px 12px;">LL</td><td style="border:1px solid #ccc;padding:8px 12px;">43×37×23cm</td><td style="border:1px solid #ccc;padding:8px 12px;">23L / — (Cordura fabric)</td></tr>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>The L size is made of water-repellent nylon, and both jaw compartments have double zippers.<br>
The gill sections on each side are hook-and-loop pockets, and the shoulder straps and back panel are padded.<br>
Colors include grey and navy alongside black, and there's also a two-tone "Combi" line such as navy and mustard.<br>
It fits A4 and holds enough for a night or two away, which makes it a handy carry-on size for idols who travel a lot.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Price and where to buy</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The Shark Backpack in L size lists at <span class="swl-marker mark_green" style="font-size:1.15em;"><strong>14,300 yen (tax incl.)</strong></span>.<br>
The bigger LL runs around 16,500 yen, while the S size and the waist pouches sit at more casual, impulse-buy prices.<br>
It's not a luxury-brand bag, so the price is friendly enough for students — a nice plus.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{G_ACCENT};color:#fff;">Where to buy the Shark Backpack</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{G_BG};">
<li style="margin:0 0 8px 0;"><a href="{MORN_OFFICIAL}" target="_blank" rel="noopener">MORN CREATIONS official online store (Shark series)</a></li>
<li style="margin:0 0 8px 0;"><a href="{AMZ}" target="_blank" rel="noopener">Search Amazon for "MORN CREATIONS Shark Backpack L"</a></li>
<li style="margin:0 0 8px 0;"><a href="{RAKUTEN}" target="_blank" rel="noopener">Search Rakuten for "MORN CREATIONS Shark Backpack"</a></li>
<li style="margin:0;"><a href="{YAHOO}" target="_blank" rel="noopener">Search Yahoo! Shopping for "MORN CREATIONS Shark Backpack"</a></li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>As a staple model the stock is fairly steady, but the black L size is popular and can sell out.<br>
The look changes a lot between sizes, so if you can, try one on in a store to check the scale before you choose.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Summary</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:2px solid {G_ACCENT};border-radius:8px;background:rgba(111,168,67,0.08);padding:1em 1.25em;margin:0 0 16px 0;">
<p style="margin:0;">
&#10003; The bag TOWA carried at the airport is MORN CREATIONS' "Shark Backpack"<br>
&#10003; It looks like the L size (about 20L) in black<br>
&#10003; MORN CREATIONS is a Hong Kong animal-motif bag brand, with the shark series as its flagship<br>
&#10003; The L size lists at 14,300 yen (tax incl.) and is sold on the official store and major marketplaces
</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>Not too loud, but a real head-turner once it's on your back, the shark bag suits TOWA's laid-back vibe well.<br>
If it caught your eye, start by checking the sizes and colors on the official online store!</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {G_BORDER};border-left:4px solid {G_ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{G_BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">More on TOWA (Towa Hamada)</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="{L_GIVENCHY}" target="_blank" rel="noopener">Looking into the GIVENCHY tee TOWA wore in his video with SIYOUNG</a></li>
<li><a href="{L_LOUNGE}" target="_blank" rel="noopener">Identifying the brand of TOWA's loungewear (GELATO PIQUE x Doraemon)</a></li>
<li><a href="{L_JAGAIMO}" target="_blank" rel="noopener">A look at TOWA's new character "Jagaimoppurin"</a></li>
<li><a href="{L_WIKI}" target="_blank" rel="noopener">A wiki-style profile and career rundown for TOWA (Towa Hamada)</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

EN_SUMMARY = "A post on X spotted KO1KEYZ's TOWA carrying an oversized backpack at an airport. It's the Shark Backpack (L size, black) from the Hong Kong brand MORN CREATIONS, a shark-mouth staple that lists at 14,300 yen (tax incl.)."

en_post = post_draft(EN_TITLE, EN_CONTENT, EN_SLUG, "en", [110, 114], JP_EYECATCH_ID, EN_SUMMARY,
                     translations={"ja": JP_POST_ID})
print("EN_POST_ID", en_post["id"], en_post["slug"], en_post.get("link"))

print("\n=== DONE ===")
print("JP", JP_POST_ID, f"{WP_URL}/wp-admin/post.php?post={JP_POST_ID}&action=edit")
print("KR", kr_post["id"], f"{WP_URL}/wp-admin/post.php?post={kr_post['id']}&action=edit")
print("EN", en_post["id"], f"{WP_URL}/wp-admin/post.php?post={en_post['id']}&action=edit")
