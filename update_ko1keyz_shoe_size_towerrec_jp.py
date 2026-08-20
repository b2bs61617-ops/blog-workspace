# -*- coding: utf-8 -*-
import base64, json
import requests

def load_env(path):
    env = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env

env = load_env('.env')
WP_URL = env['WP_KOIKEYS_URL'].rstrip('/')
AUTH = base64.b64encode(f"{env['WP_KOIKEYS_USERNAME']}:{env['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
h = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}
hget = {'Authorization': f'Basic {AUTH}'}

KOSUKE_MEDIA_ID = 11635
TOWERREC_TWEET = "https://x.com/azmchan1202/status/2090335670049062963"

media = requests.get(f'{WP_URL}/wp-json/wp/v2/media/{KOSUKE_MEDIA_ID}', headers=hget).json()

def build_img_html(media, alt, caption, size_key="large"):
    sizes = media.get("media_details", {}).get("sizes", {})
    full_url = media["source_url"]
    full_w = media["media_details"]["width"]
    full_h = media["media_details"]["height"]
    chosen = sizes.get(size_key, {"source_url": full_url, "width": full_w})
    medium = sizes.get("medium", {"source_url": full_url, "width": full_w})
    img_src = chosen["source_url"]
    img_w = chosen["width"]
    img_h = int(img_w * full_h / full_w)
    srcset = f'{medium["source_url"]} {medium["width"]}w, {chosen["source_url"]} {chosen["width"]}w, {full_url} {full_w}w'
    return f'''<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">{caption}</figcaption>
</figure>'''

r = requests.get(f'{WP_URL}/wp-json/wp/v2/posts/11551?context=edit', headers=hget)
r.raise_for_status()
raw = r.json()['content']['raw']

replacements = []

old1 = '''<p>『PRODUCE 101 JAPAN 新世界』出身のKO1KEYZは、2026年10月7日のデビューへ向けて日々話題を集めているグループです。<br>
そんな中、HMVで行われているデビューシングル『新世界』の制服(衣装)展示にファンが足を運んだところ、シューズの内側に貼られたサイズタグが偶然見えてしまい、Xで報告されて話題になりました。<br>
確認できた6人のうち、<strong>もっとも大きいのはRYUJIの27.5cm、もっとも小さいのはYOSHIKIとTOWAの26.0cm</strong>という結果でした。<br>
この記事では、Xで報告された内容をもとに、メンバーごとの靴サイズを一覧にまとめます。</p>'''
new1 = '''<p>『PRODUCE 101 JAPAN 新世界』出身のKO1KEYZは、2026年10月7日のデビューへ向けて日々話題を集めているグループです。<br>
そんな中、HMVやタワーレコード渋谷店で行われているデビューシングル『新世界』の制服(衣装)展示にファンが足を運んだところ、シューズの内側に貼られたサイズタグが偶然見えてしまい、Xで報告されて話題になりました。<br>
確認できた10人のうち、<strong>もっとも大きいのはRYUJI・KOSUKE・DAIKIの27.5cm、もっとも小さいのはYOSHIKIとTOWAの26.0cm</strong>という結果でした。<br>
この記事では、Xで報告された内容をもとに、メンバーごとの靴サイズを一覧にまとめます。</p>'''
replacements.append((old1, new1))

old2 = '''<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ded9d2;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#8a8378;color:#fff;">この記事でわかること</p>'''
new2 = '''<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="border:1px solid #ded9d2;border-left:4px solid #8a8378;border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#f8f6f4;">
<p style="margin:0;"><strong>追記(2026年8月21日):</strong>タワーレコード渋谷店での新たな目撃情報により、KOSUKE・DAIKI・SIYOUNG・RYOGAの4人分のサイズが新たに判明しました。最新情報を反映して更新しています。</p>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div style="border:1px solid #ded9d2;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:#8a8378;color:#fff;">この記事でわかること</p>'''
replacements.append((old2, new2))

old3 = '<h2 class="wp-block-heading">HMVの新世界衣装展示でシューズのサイズタグが判明</h2>'
new3 = '<h2 class="wp-block-heading">HMV・タワーレコード渋谷でシューズのサイズタグが判明</h2>'
replacements.append((old3, new3))

old4 = '<p style="margin:0;"><strong>目撃場所:</strong>HMV(『新世界』制服展示)<br><strong>報告日:</strong>2026年8月20日</p>'
new4 = '<p style="margin:0;"><strong>目撃場所:</strong>HMV・タワーレコード渋谷店(『新世界』制服展示)<br><strong>報告日:</strong>2026年8月20日・21日</p>'
replacements.append((old4, new4))

old5 = '''<figcaption style="text-align:center;font-size:12px;">出典:<a href="https://x.com/lalabonbondrop/status/2090264614382788644" target="_blank" rel="noopener">https://x.com/lalabonbondrop/status/2090264614382788644</a></figcaption>
</figure>
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">KO1KEYZメンバーの靴サイズ一覧</h2>'''

towerrec_img_html = build_img_html(
    media,
    'タワーレコード渋谷店の新世界衣装展示で撮影された、KOSUKEのシューズサイズタグ(型番397447-02)',
    f'出典:<a href="{TOWERREC_TWEET}" target="_blank" rel="noopener">{TOWERREC_TWEET}</a>',
)

new5 = f'''<figcaption style="text-align:center;font-size:12px;">出典:<a href="https://x.com/lalabonbondrop/status/2090264614382788644" target="_blank" rel="noopener">https://x.com/lalabonbondrop/status/2090264614382788644</a></figcaption>
</figure>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>続いて2026年8月21日には、タワーレコード渋谷店の展示を見てきたという別のファンから、「タワ渋見てきました」として、KOSUKE・DAIKI・SIYOUNG・RYOGAのシューズサイズタグを写した投稿がありました。<br>
この投稿によると、KOSUKEとDAIKIはともに27.5cm、SIYOUNGは27.0cm、RYOGAは26.5cm(タグのUSサイズ表記から推定)とのことです。<br>
投稿者いわく、角度の都合でYUKIとKEITOのタグだけはどうしても確認できなかったとのことでした。</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{towerrec_img_html}
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">KO1KEYZメンバーの靴サイズ一覧</h2>'''
replacements.append((old5, new5))

old6 = '<p style="margin:0;"><strong>確認できたのは12人中6人分。</strong>最大はRYUJIの27.5cm、最小はYOSHIKIとTOWAの26.0cmでした。</p>'
new6 = '<p style="margin:0;"><strong>確認できたのは12人中10人分。</strong>最大はRYUJI・KOSUKE・DAIKIの27.5cm、最小はYOSHIKIとTOWAの26.0cmでした。</p>'
replacements.append((old6, new6))

old7 = '''<tr><td>メンバー</td><td>サイズ(cm)</td><td>備考</td></tr>
<tr><td>YOSHIKI(矢田佳暉)</td><td>26.0</td><td>-</td></tr>
<tr><td>TOWA(濱田永遠)</td><td>26.0</td><td>-</td></tr>
<tr><td>SHINHAENG(オ・シンヘン)</td><td>26.5</td><td>-</td></tr>
<tr><td>ISSA(柳谷伊冴)</td><td>27.0</td><td>-</td></tr>
<tr><td>RYUJI(杉山竜司)</td><td>27.5</td><td>インソールなしで着用</td></tr>
<tr><td>YURA(安部結蘭)</td><td>-</td><td>サイズタグが写真に写らず未確認</td></tr>'''
new7 = '''<tr><td>メンバー</td><td>サイズ(cm)</td><td>備考</td></tr>
<tr><td>YOSHIKI(矢田佳暉)</td><td>26.0</td><td>-</td></tr>
<tr><td>TOWA(濱田永遠)</td><td>26.0</td><td>-</td></tr>
<tr><td>SHINHAENG(オ・シンヘン)</td><td>26.5</td><td>-</td></tr>
<tr><td>RYOGA(飯塚亮賀)</td><td>26.5(推定)</td><td>USサイズ8.5からの推定、cm表記は未確認</td></tr>
<tr><td>ISSA(柳谷伊冴)</td><td>27.0</td><td>-</td></tr>
<tr><td>SIYOUNG(パク・シヨン)</td><td>27.0</td><td>-</td></tr>
<tr><td>RYUJI(杉山竜司)</td><td>27.5</td><td>インソールなしで着用</td></tr>
<tr><td>KOSUKE(照井康祐)</td><td>27.5</td><td>-</td></tr>
<tr><td>DAIKI(加藤大樹)</td><td>27.5</td><td>-</td></tr>
<tr><td>YURA(安部結蘭)</td><td>-</td><td>シューズ・名前タグは確認済みだがサイズ表記は未確認</td></tr>'''
replacements.append((old7, new7))

old8 = '<p><strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">もっとも大きいRYUJI(27.5cm)ともっとも小さいYOSHIKI・TOWA(26.0cm)の間には1.5cmの差</span></strong>があることも分かりました。</p>'
new8 = '<p><strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">もっとも大きいRYUJI・KOSUKE・DAIKI(27.5cm)ともっとも小さいYOSHIKI・TOWA(26.0cm)の間には1.5cmの差</span></strong>があることも分かりました。</p>'
replacements.append((old8, new8))

old9 = '<p style="margin:0;"><strong>シューズはPUMAの「CLUB II ERA(クラブ II エラ)」、型番は6人とも共通の「397447-02」でした。</strong></p>'
new9 = '<p style="margin:0;"><strong>シューズはPUMAの「CLUB II ERA(クラブ II エラ)」、型番はここまで確認できた10人とも共通の「397447-02」でした。</strong></p>'
replacements.append((old9, new9))

old10 = '<p>サイズタグをよく見ると、シューズはPUMAのモデルで、6人とも型番「397447-02」が共通していることが分かります。<br>'
new10 = '<p>サイズタグをよく見ると、シューズはPUMAのモデルで、ここまで確認できた10人とも型番「397447-02」が共通していることが分かります。<br>'
replacements.append((old10, new10))

old11 = '<h2 class="wp-block-heading">サイズが確認できなかった6人は?</h2>'
new11 = '<h2 class="wp-block-heading">サイズが確認できなかった2人は?</h2>'
replacements.append((old11, new11))

old12 = '<p style="margin:0;"><strong>今回タグが判明したのは6人。</strong>残るKOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNGは未確認です。</p>'
new12 = '<p style="margin:0;"><strong>ここまでタグが判明したのは10人。</strong>残るYUKI・KEITOは未確認です。</p>'
replacements.append((old12, new12))

old13 = '''<p>今回の投稿でサイズタグが確認できたのは、YOSHIKI・TOWA・SHINHAENG・ISSA・RYUJI・YURAの6人分でした。<br>
残るKOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNGの6人については、投稿者も別会場(タワーレコードなど)を確認できていないとのことで、現時点ではサイズが分かっていません。<br>
もし他の会場での目撃情報が出てきたら、この記事でも追ってお伝えします。</p>'''
new13 = '''<p>ここまでの投稿でサイズタグが確認できたのは、YOSHIKI・TOWA・SHINHAENG・ISSA・RYUJI・KOSUKE・DAIKI・SIYOUNG・RYOGAの9人と、シューズ本体・名前タグのみ確認できたYURAを合わせた10人でした。<br>
残るYUKI・KEITOの2人については、HMV・タワーレコードどちらの投稿者も角度の都合で確認できなかったとのことで、現時点ではサイズが分かっていません。<br>
もし他の目撃情報が出てきたら、この記事でも追ってお伝えします。</p>'''
replacements.append((old13, new13))

old14 = '''<li>HMVの『新世界』制服展示で、6人分のシューズのサイズタグが偶然見えたと話題に</li>
<li>サイズはYOSHIKI・TOWAが26.0cm、SHINHAENGが26.5cm、ISSAが27.0cm、RYUJIが27.5cm</li>
<li>シューズはPUMAの「CLUB II ERA」(型番397447-02)を全員でサイズ違いで着用、参考価格は10,450円(税込)</li>
<li>残る6人(KOSUKE・KEITO・DAIKI・RYOGA・YUKI・SIYOUNG)のサイズは未確認</li>'''
new14 = '''<li>HMV・タワーレコード渋谷の『新世界』制服展示で、10人分のシューズのサイズタグが偶然見えたと話題に</li>
<li>サイズはYOSHIKI・TOWAが26.0cm、SHINHAENG・RYOGAが26.5cm、ISSA・SIYOUNGが27.0cm、RYUJI・KOSUKE・DAIKIが27.5cm</li>
<li>シューズはPUMAの「CLUB II ERA」(型番397447-02)をここまで確認できた10人がサイズ違いで着用、参考価格は10,450円(税込)</li>
<li>残る2人(YUKI・KEITO)のサイズは未確認</li>'''
replacements.append((old14, new14))

for i, (old, new) in enumerate(replacements, 1):
    cnt = raw.count(old)
    assert cnt == 1, f"replacement {i} matched {cnt} times, expected 1"
    raw = raw.replace(old, new)

ur = requests.post(f'{WP_URL}/wp-json/wp/v2/posts/11551', headers=h, data=json.dumps({"content": raw}).encode('utf-8'))
ur.raise_for_status()
print("JP updated, length:", len(ur.json()['content']['raw']))
open('tmp_jp_updated.html', 'w', encoding='utf-8').write(raw)
