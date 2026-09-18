# -*- coding: utf-8 -*-
"""RYOGA(飯塚亮賀)がKO1KEYZ新番組「KO1!KO1!KO1KEYZ」EP.1の自己紹介コーナーで見せた
謎のポーズ(NARUTOの口寄せの術？進撃の巨人の巨人化？ドラゴンボールの元気玉？)を考察する記事。
chomoand-1.com にJP下書きを投稿し、アイキャッチを生成・設定する。
"""
import base64, json, os, re, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

import requests

ROOT = Path(__file__).parent
IMG_DIR = ROOT / "frames_tmp" / "ryoga_ep1" / "final"


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

VIDEO_URL = "https://www.youtube.com/watch?v=KTlObvSe1SM"
VIDEO_LABEL = "KO1KEYZ公式YouTube「[EP.1] KO1! KO1! KO1KEYZ｜キュントゥグン学園〜新入生オーディション〜」"

IMG_KICK = IMG_DIR / "ryoga_jikoshoukai_soccer_kick.jpg"
IMG_POSE = IMG_DIR / "ryoga_jikoshoukai_mystery_pose.jpg"
IMG_REVEAL = IMG_DIR / "ryoga_jikoshoukai_anime_reveal.jpg"

# RYOGA公式メンバーカラー(群青)に寄せたパステル配色(既存のRYOGA記事と統一)
AB = "#c3cbe0"   # border
AL = "#5b6fa8"   # accent(title bar / left bar)
BG = "#f0f2f8"   # box background

RYOGA_PROFILE_IMG = "https://chomoand-1.com/wp-content/uploads/2026/08/ryoga_concept_photo1-333x500.jpg"
RYOGA_PROFILE_IMG_SRCSET = ("https://chomoand-1.com/wp-content/uploads/2026/08/ryoga_concept_photo1-200x300.jpg 200w, "
                             "https://chomoand-1.com/wp-content/uploads/2026/08/ryoga_concept_photo1-333x500.jpg 333w, "
                             "https://chomoand-1.com/wp-content/uploads/2026/08/ryoga_concept_photo1.jpg 780w")


def upload_media_from_file(path: Path, filename: str, alt: str):
    headers = {
        **HEADERS_AUTH,
        "Content-Type": "image/jpeg",
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, data=path.read_bytes())
    r.raise_for_status()
    media = r.json()
    r2 = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media/{media['id']}",
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps({"alt_text": alt, "title": alt}).encode("utf-8"),
    )
    r2.raise_for_status()
    return media


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


print("uploading kick image...")
kick_media = upload_media_from_file(
    IMG_KICK, "ryoga_jikoshoukai_soccer_kick.jpg",
    "自己紹介中、サッカーのキック動作を再現するRYOGA(飯塚亮賀)",
)
print("kick", kick_media["id"])

print("uploading pose image...")
pose_media = upload_media_from_file(
    IMG_POSE, "ryoga_jikoshoukai_mystery_pose.jpg",
    "自己紹介の途中、両腕を大きく動かす謎のポーズを見せるRYOGA(飯塚亮賀)",
)
print("pose", pose_media["id"])

print("uploading reveal image...")
reveal_media = upload_media_from_file(
    IMG_REVEAL, "ryoga_jikoshoukai_anime_reveal.jpg",
    "一連の動きの後、真顔で「アニメと漫画が大好きです」と言い切るRYOGA(飯塚亮賀)",
)
print("reveal", reveal_media["id"])

kick_caption = f'出典:{VIDEO_LABEL}'
pose_caption = f'出典:{VIDEO_LABEL}'
reveal_caption = f'出典:{VIDEO_LABEL}'

kick_html = f"<!-- wp:html -->\n{build_img_html(kick_media, '自己紹介中、サッカーのキック動作を再現するRYOGA(飯塚亮賀)', kick_caption)}\n<!-- /wp:html -->"
pose_html = f"<!-- wp:html -->\n{build_img_html(pose_media, '自己紹介の途中、両腕を大きく動かす謎のポーズを見せるRYOGA(飯塚亮賀)', pose_caption)}\n<!-- /wp:html -->"
reveal_html = f"<!-- wp:html -->\n{build_img_html(reveal_media, '真顔で「アニメと漫画が大好きです」と言い切るRYOGA(飯塚亮賀)', reveal_caption)}\n<!-- /wp:html -->"

profile_img_html = f"""<!-- wp:html -->
<figure class="wp-block-image size-large" style="text-align:center;">
  <img src="{RYOGA_PROFILE_IMG}" alt="RYOGA(飯塚亮賀) プロフィール写真" style="max-width:333px;width:100%;height:auto;margin:0 auto;" srcset="{RYOGA_PROFILE_IMG_SRCSET}">
  <figcaption style="text-align:center;font-size:12px;">出典:<a href="https://x.com/KO1KEYZofficial/status/2081673449924374924" target="_blank" rel="noopener">@KO1KEYZofficial(X)</a></figcaption>
</figure>
<!-- /wp:html -->"""


TITLE = "RYOGAの自己紹介がまさかの口寄せの術？NARUTOネタに会場騒然"
FALLBACK_SLUG = "ryoga-jikoshoukai-naruto-kuchiyose"

CONTENT = f"""<!-- wp:paragraph -->
<p>KO1KEYZ(コイキーズ)の新番組「KO1! KO1! KO1KEYZ」の記念すべき第1話で、RYOGA(飯塚亮賀)さんの自己紹介コーナーがSNSで大きな話題になっています。<br>
音楽が突然止まったかと思うと、サッカーのキック動作、そして両腕を使った謎めいたポーズを次々に披露し、真顔で「アニメと漫画が大好きです」と言い切るという、1分間に情報量を詰め込みすぎた自己紹介だったからです。<br>
ファンの間では、このポーズの元ネタが「NARUTOの口寄せの術では」「いや進撃の巨人の巨人化っぽい」「ドラゴンボールの元気玉じゃない?」と割れており、真相はまだはっきりしていません。<br>
この記事では、番組の内容を振り返りながら、RYOGAさんの自己紹介で何が起きていたのか、そしてあのポーズの元ネタが何だったのかを考察していきます。</p>
<!-- /wp:paragraph -->

{profile_img_html}

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AL};color:#fff;">この記事でわかること</p>
<ul style="margin:0;padding:14px 18px 14px 34px;background:{BG};">
<li>「KO1! KO1! KO1KEYZ」第1話がどんな番組か</li>
<li>RYOGAさんの自己紹介で実際に何が起きたか</li>
<li>謎のポーズの元ネタ候補(NARUTO・進撃の巨人・ドラゴンボール)</li>
<li>NARUTO説が有力とみられる理由</li>
<li>RYOGAさんは元々「自己紹介職人」だったという過去のエピソード</li>
<li>SNSでのファンの反応</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">「KO1!KO1!KO1KEYZ」第1話はどんな番組?</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>番組:</strong>KO1! KO1! KO1KEYZ 第1話「キュントゥグン学園〜新入生オーディション〜」</p>
<p style="margin:4px 0 0 0;"><strong>配信:</strong>KO1KEYZ公式YouTubeで無料配信、2026年9月17日(木)21:00〜、毎週木曜更新</p>
<p style="margin:4px 0 0 0;"><strong>内容:</strong>12人のメンバーが「キュントゥグン学園」の新入生という設定で、1人1分間の自己紹介をした後、「一番仲良くなりたい」と思った1人に投票する</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>「KO1! KO1! KO1KEYZ」は、KO1KEYZの公式YouTubeチャンネルで2026年9月17日(木)21:00から無料配信がスタートした新番組です。<br>
記念すべき第1話は「キュントゥグン学園〜新入生オーディション〜」と題した学園コント企画で、メンバー12人が同じクラスに転入してきた新入生という設定で登場します。<br>
ルールは、1人ずつ1分間の自己紹介をした後、全員の自己紹介が終わったところで「一番友達になりたいと思った人」に1票を投じるというもの。<br>
最多得票を集めたメンバーが「友達になりたい新入生ナンバーワン」に輝く仕組みで、メンバーたちは持ち時間1分をフルに使って個性をアピールしていました。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">RYOGAの自己紹介で何が起きた?流れを徹底解説</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>数ある自己紹介の中でも、SNSで特に反響が大きかったのがRYOGAさんの自己紹介です。<br>
「群馬県出身の飯塚亮賀と申します」と名乗ると、同じく群馬県出身のメンバーから「仲良くなれたら」と声がかかり、「どうやって来たの?」という質問に「普通に電車で」と冗談を返すなど、序盤は和やかな空気で進みます。<br>
ところがここから、RYOGAさんの自己紹介は一気に加速していきます。</p>
<!-- /wp:paragraph -->

{kick_html}

<!-- wp:paragraph -->
<p>まず飛び出したのが、「サッカーを15年間やっていました。なので運動には少し自信があります」という自己紹介に合わせた、本格的なキック動作です。<br>
中学・高校でサッカーに打ち込んできたRYOGAさんらしい、言葉だけでなく体で語る自己紹介ですが、これはまだ序章にすぎませんでした。</p>
<!-- /wp:paragraph -->

{pose_html}

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>話題のポイント:</strong>キック動作の直後、RYOGAさんは両腕を大きく動かす謎のポーズを披露。<br>正体が分からない同級生役のメンバーたちから「そして」「何それ?何それ?」という戸惑いの声が上がった</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>音楽が一瞬止まるほどの間を作ったうえで放たれたこのポーズに、周りのメンバーは思わず「何それ?何それ?」と声を揃えるほど困惑した様子。<br>
そして、あれだけ動き回った直後とは思えないほど落ち着いた真顔で放たれたのが、<strong>「アニメと漫画が大好きです」</strong>のひとことでした。</p>
<!-- /wp:paragraph -->

{reveal_html}

<!-- wp:paragraph -->
<p>さらに畳みかけるように「で、あの見た目で引きこもることも大好きです」と付け加え、「皆さんあいつちょっと仲良くしてください」と締めくくるという、最後まで予測不能な自己紹介でした。<br>
物腰やわらかな見た目とのギャップに、周りのメンバーからは「あの見た目で?」「でもちょっと気になるかも」「気になるよね、もっと話聞きたいもん」といった反応が飛び出し、結果的にRYOGAさんは「一番友達になりたい新入生」の投票で複数票を獲得することになりました。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">謎のポーズの正体は?NARUTO・進撃の巨人・ドラゴンボール説を考察</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>話題のポイント:</strong>SNSでは、RYOGAさんが披露したポーズの元ネタについて「NARUTOの口寄せの術」「進撃の巨人の巨人化」「ドラゴンボールの元気玉」という3つの説が飛び交い、意見が割れている</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>放送直後からSNSでは、あのポーズが一体何のパロディなのかをめぐって考察合戦が起こりました。<br>
中には「自己紹介の亮賀くん、巨人化やら口寄せの術やら元気玉やら言われてるけど、どれも伝わらなくて調べた」と、複数の説が同時に飛び交って収拾がつかなくなっている様子を報告するファンもいたほどです。<br>
候補に挙がった3作品を整理すると、次のようになります。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0 0 8px 0;font-weight:bold;">ポーズの元ネタ候補</p>
<ul style="margin:0;padding-left:1.3em;">
<li><strong>NARUTO「口寄せの術」説</strong> — 両手で印を結んでから技を発動する忍術シーン。「新しいクラスになった時に自己紹介で口寄せの術やるタイプなんだ」というファンの投稿もあり、最も多く挙がった説</li>
<li><strong>進撃の巨人「巨人化」説</strong> — 主人公が覚醒して巨人に変身する際の、腕を突き上げるような激しい動作をイメージした説</li>
<li><strong>ドラゴンボール「元気玉」説</strong> — 両手を掲げてエネルギーを集める、必殺技を放つ前のチャージ動作をイメージした説</li>
</ul>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>3つとも少年漫画・アニメの中でも屈指の人気作品で、いずれも「両手を使った大きな動作」という共通点があるため、動画のワンシーンだけで一つに断定するのは正直かなり難しいところです。<br>
ただし、<a href="https://chomoand-1.com/ryoga-iizuka-anime-manga-list-11782" target="_blank" rel="noopener">RYOGAさんの漫画・アニメ好きを調べた別記事</a>で明らかになっている情報と照らし合わせると、<strong>NARUTO説が最も有力</strong>だと考えられます。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">NARUTO説が有力とみられる理由</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>RYOGAさんは、メンバー・ファンとやり取りできるアプリ「KO1KEYZ Chat(プラチャ)」で以前から漫画・アニメネタを連発していることで知られており、その中でも<strong>「亮賀が好きなのが確定している漫画はNARUTO・呪術廻戦・ONE PIECE」</strong>と紹介されるほど、NARUTOへの愛情の深さは折り紙付きです。<br>
2026年9月8日のプラチャでは「疾風伝までなんとか頑張って見てくれ」「疾風伝からもう止まれない」とNARUTOについて長文で熱弁し、これから見るファンに向けて視聴継続のアドバイスまで送っていたほどでした。<br>
一方、今回候補に挙がった進撃の巨人やドラゴンボールについては、これまでの調査で「好き」という発言や作品リストへの掲載が確認できていません。<br>
これだけ日常的にNARUTOの話をしているRYOGAさんが、自己紹介という注目の場面でNARUTOの必殺技風ポーズを選んだと考えるのは、決して不自然ではないでしょう。<br>
もちろん本人からの正式なコメントがあるわけではないため断定はできませんが、「口寄せの術」説はRYOGAさんの人物像と最も矛盾しない考察だと言えそうです。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">実はRYOGAは「自己紹介職人」?過去にも数々の伝説あり</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
<p style="margin:0;"><strong>話題のポイント:</strong>RYOGAさんの個性的な自己紹介は今回が初めてではなく、『PRODUCE 101 JAPAN 新世界』時代からたびたび話題になっていた</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>今回の自己紹介が「らしい」と感じたファンが多かったのには理由があります。<br>
RYOGAさんはオーディション番組『PRODUCE 101 JAPAN 新世界』時代から、印象的な自己紹介を何度も披露してきた「自己紹介職人」だったのです。<br>
たとえば101秒間の自己紹介リレー企画では「群馬県出身の亮賀です、15年間サッカーをやってきた」と、今回と同じ持ちネタである群馬県出身・サッカー歴15年を早くも披露していました。<br>
また別の自己紹介では「なぜか足つぼマットの上で縄跳びをする」という、脈絡のなさが逆に話題になったこともあります。<br>
抑揚を抑えた独特な話し方も当時から「クセになる」とファンの間で評判で、飾らない天然なキャラクターは今も昔も変わっていないようです。<br>
つまり今回のNARUTO(?)ポーズ入りの自己紹介は、こうした「予測不能な自己紹介」の系譜に連なる、いわば集大成のような一幕だったと言えそうです。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">SNSでのファンの反応</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>放送直後のSNSは、RYOGAさんの自己紹介の感想で大いに盛り上がりました。<br>
「自己紹介するだけでスーパー亮賀タイムを作り出せる」「音が止まりすぎて腹痛い」「R-1グランプリ並みに作り込まれている」など、その完成度の高さを称賛する声が多く見られます。<br>
一方で「電波ちゃんすぎてやばい」「独特すぎて個別配信を見てみたくなる」といった、RYOGAさんらしいマイペースなキャラクターを面白がる声も目立ちました。<br>
サッカーのキック動作についても「ありえないアニメ・漫画の動きよりも、サッカーを蹴るモーションの方がガチですごい」と、細部までこだわった演技を評価するコメントが上がっています。<br>
「引きこもることも大好き」というくだりには「そんなこと自分から言う人いない」と笑いの声も上がり、見た目とのギャップも含めて総合的に愛される自己紹介になったようです。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">まとめ</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>「KO1!KO1!KO1KEYZ」第1話「キュントゥグン学園」で、RYOGAさんの自己紹介が大きな話題に</p>
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>サッカーのキック動作→謎のポーズ→真顔で「アニメと漫画が大好き」という、緩急のある1分間の自己紹介</p>
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>謎のポーズはNARUTO「口寄せの術」・進撃の巨人「巨人化」・ドラゴンボール「元気玉」の3説が浮上</p>
<p style="margin:0 0 6px 0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>RYOGA本人の確定済みの「好きな漫画」にNARUTOが含まれることから、口寄せの術説が最有力</p>
<p style="margin:0;"><span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>オーディション時代から個性的な自己紹介で知られる「自己紹介職人」で、今回はその集大成的な一幕だった</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>1分間という短い持ち時間に、サッカー・アニメ・見た目とのギャップまで詰め込んでみせたRYOGAさんの自己紹介。<br>
謎のポーズの真相はまだ本人の口から明かされていませんが、「KO1!KO1!KO1KEYZ」は毎週木曜日に更新される番組なので、続報や本人からの種明かしがあれば改めてお伝えします。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">RYOGA(飯塚亮賀)さんの関連記事</p>
<ul style="margin:0;padding-left:1.3em;">
<li><a href="https://chomoand-1.com/ryoga-iizuka-anime-manga-list-11782" target="_blank" rel="noopener">RYOGAの漫画・アニメ好きと履修済み作品一覧を調べた記事</a></li>
<li><a href="https://chomoand-1.com/ryo-ga-school_soccer-8966" target="_blank" rel="noopener">中学・高校の学歴とサッカー経歴を調べた記事</a></li>
<li><a href="https://chomoand-1.com/iidukaryouga_wiki-1047" target="_blank" rel="noopener">歌・ダンス未経験で日プ新世界に挑戦したwiki風経歴の記事</a></li>
<li><a href="https://chomoand-1.com/ryoga-mark-gonzales-longtee-12828" target="_blank" rel="noopener">韓国Vlogで着ていた私服ロンTを特定した記事</a></li>
</ul>
</div>
<!-- /wp:html -->
"""

SUMMARY = ("KO1KEYZの新番組「KO1!KO1!KO1KEYZ」でRYOGA(飯塚亮賀)が披露した自己紹介の謎ポーズが話題に。"
           "NARUTOの口寄せの術？進撃の巨人？ドラゴンボール？SNSで割れた考察と、有力説の根拠をまとめました。")


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


SLUG = get_slug(TITLE, FALLBACK_SLUG)
print("SLUG", SLUG)

plain_len = len(re.sub(r"<!--.*?-->|<[^>]+>", "", CONTENT, flags=re.S))
print("content length (chars):", plain_len)

payload = {
    "title": TITLE,
    "content": CONTENT,
    "slug": SLUG,
    "status": "draft",
    "categories": [66, 98],
    "author": 2,
    "meta": {"jetpack_publicize_message": SUMMARY},
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

EYECATCH_PATH = ROOT / "images" / "ryoga_jikoshoukai_naruto_eyecatch.png"
subprocess.run([
    sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"),
    "--top", "RYOGAの自己紹介がまさかの口寄せの術？",
    "--main", "KO1KEYZ",
    "--bottom", "NARUTOネタに会場騒然！",
    "--out", str(EYECATCH_PATH),
    "--seed", str(post["id"]),
], check=True)

media_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/media",
    headers={
        **HEADERS_AUTH,
        "Content-Type": "image/png",
        "Content-Disposition": 'attachment; filename="ryoga_jikoshoukai_naruto_eyecatch.png"',
    },
    data=EYECATCH_PATH.read_bytes(),
)
media_r.raise_for_status()
EYECATCH_MEDIA_ID = media_r.json()["id"]
print("EYECATCH_MEDIA_ID", EYECATCH_MEDIA_ID)

featured_r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts/{post['id']}",
    headers={**HEADERS_AUTH, "Content-Type": "application/json"},
    data=json.dumps({"featured_media": EYECATCH_MEDIA_ID}).encode("utf-8"),
)
featured_r.raise_for_status()

(ROOT / "tmp_ryoga_jikoshoukai_ids.txt").write_text(
    f"post={post['id']} slug={post['slug']} kick={kick_media['id']} pose={pose_media['id']} reveal={reveal_media['id']} eyecatch={EYECATCH_MEDIA_ID}\n",
    encoding="utf-8",
)
print("DONE. Edit URL:", f"{WP_URL}/wp-admin/post.php?post={post['id']}&action=edit")
