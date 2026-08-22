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


def upload_image(local_path, filename, alt_hint, content_type="image/jpeg"):
    data = local_path.read_bytes()
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={
            **HEADERS_AUTH,
            "Content-Type": content_type,
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
        data=data,
    )
    r.raise_for_status()
    media = r.json()
    print("uploaded media id", media["id"], filename)
    return media


XIY = ROOT / "tools" / "Xiy"
img_official_rehearsal = upload_image(
    XIY / "posts_koikeyz_fanmi_day1_test" / "images" / "post_4_img_1.jpg",
    "ko1keyz_fanmi_day1_rehearsal.jpg",
    "KO1KEYZ 1ST FAN MEETING 東京公演のリハーサル後ステージ写真",
)
img_ginte = upload_image(
    XIY / "posts_koikeyz_fanmi_day1_19" / "images" / "post_1_img_1.jpg",
    "ko1keyz_fanmi_day1_ginte.jpg",
    "KO1KEYZ 1ST FAN MEETINGの銀テープ、12人全員分のサイン入り",
)
img_area_map = upload_image(
    XIY / "posts_koikeyz_fanmi_day1_11" / "images" / "post_1_img_1.jpg",
    "ko1keyz_fanmi_day1_area_map.jpg",
    "KO1KEYZ 1ST FAN MEETING TOYOTA ARENA TOKYO会場エリアマップ",
)
# 現地の座席案内板の写真(https://x.com/22everic/status/2090789679465709589)をもとに
# tools/gen_ko1keyz_fanmi_day1_seatmap.py で再作図したもの
img_seatmap_official = upload_image(
    ROOT / "images" / "ko1keyz_fanmi_day1_seatmap_official.png",
    "ko1keyz_fanmi_day1_seatmap_official.png",
    "TOYOTA ARENA TOKYOアリーナ客席図",
    content_type="image/png",
)
img_seat_chart = upload_image(
    XIY / "posts_koikeyz_fanmi_day1_10" / "images" / "post_1_img_1.jpg",
    "ko1keyz_fanmi_day1_seat_chart.jpg",
    "TOYOTA ARENA TOKYOアリーナ席の座席番号予想表",
)


def build_img_html(media, alt, caption, source_url):
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
    cap = f'出典:<a href="{source_url}" target="_blank" rel="noopener">{source_url}</a>' if not caption else caption
    return f'''<figure class="wp-block-image size-large">
<img src="{img_src}" alt="{alt}" width="{img_w}" height="{img_h}"
  style="max-width:100%;height:auto;"
  srcset="{srcset}"
  sizes="(max-width: {img_w}px) 100vw, {img_w}px">
<figcaption style="text-align:center;font-size:12px;">{cap}</figcaption>
</figure>'''


def p(text_sentences):
    body = "<br>\n".join(text_sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


ACCENT = "#8a8378"
BORDER = "#ded9d2"
BG = "#f8f6f4"


def plain_box(title, html_body):
    return wphtml(f'''<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>
{html_body}
</div>''')


def titlebar_box(title, list_html):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{title}</p>
{list_html}
</div>''')


def mini_box(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


def capbox_list(ttl, items):
    lis = "\n".join(f"<li>{t}</li>" for t in items)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{ttl}</p>
<ul style="margin:0;padding-left:1.2em;">
{lis}
</ul>
</div>''')


def notebox(html_body):
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">
{html_body}
</div>''')


DEBUT_EVENTS_URL = "https://chomoand-1.com/what-events-will-be-held-to-co-2-11307"
FANCLUB_BOOTH_URL = "https://chomoand-1.com/can-i-participate-in-the-ko1ke-11468"
GOODS_EC_URL = "https://chomoand-1.com/ko1keyz-2026-1st-fan-meeting-g-10726"
FANMEETING_PREDICT_URL = "https://chomoand-1.com/ko1keyz-live-10270"

title = "KO1KEYZ1stファンミ初日セトリ・座席表・トロッコは？"

blocks = []

blocks.append(p([
    "2026年8月21日(金)、KO1KEYZ初のファンミーティング『2026 KO1KEYZ 1ST FAN MEETING』がTOYOTA ARENA TOKYOでついに開幕しました。",
    "初日はDREAMERから始まりKO1KEYZで締めるセットリスト、アンコールでの<strong>撮影OKタイム</strong>とトロッコ(客席一周)、開演前の待機列・グッズ状況まで、参戦したKO1LYたちのX投稿から当日の様子がリアルタイムでどんどん共有されました。",
    "この記事では、初日(東京公演DAY1)の様子をタイムライン順にまとめて紹介します。",
]))
blocks.append(build_img_html(
    img_official_rehearsal,
    "KO1KEYZ 1ST FAN MEETING東京公演のステージ写真",
    None,
    "https://x.com/KO1KEYZofficial/status/2090703676507922768",
))

blocks.append(plain_box("『2026 KO1KEYZ 1ST FAN MEETING』東京公演 基本情報", f'''<table style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;width:35%;">会場</td><td style="border:1px solid #ccc;padding:8px 12px;">TOYOTA ARENA TOKYO</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">DAY1</td><td style="border:1px solid #ccc;padding:8px 12px;">8月21日(金)18:30開演</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">DAY2</td><td style="border:1px solid #ccc;padding:8px 12px;">8月22日(土)13:30開演/18:30開演の2公演</td></tr>
<tr><td style="background:#f0f0f0;border:1px solid #ccc;padding:8px 12px;">DAY3</td><td style="border:1px solid #ccc;padding:8px 12px;">8月23日(日)15:00開演</td></tr>
</table>'''))

blocks.append(titlebar_box("この記事でわかること", '''<ul style="margin:0;padding:14px 18px 14px 34px;background:#f7f6f4;">
<li>会場エリアマップ・ブース配置</li>
<li>入場時の本人確認・手荷物検査</li>
<li>待機列・グッズの状況</li>
<li>初日のセットリスト</li>
<li>アンコールの撮影OKタイム</li>
<li>トロッコ・座席表</li>
</ul>'''))

blocks.append(h2("開演・終演時間は？"))
blocks.append(mini_box('<p style="margin:0;"><strong>開演:</strong>18:30<br><strong>終演:</strong>20:26<br>アンコール・トロッコあり、上演時間は正味2時間ほどでした。</p>'))
blocks.append(p([
    "現地から投稿された終演報告によると、開演は予定通り18:30、終演は20:26。",
    "アンコールとトロッコ(後述)を含めての約2時間で、現地では「たっぷり大満足」という声も見られました。",
]))

blocks.append(h2("会場エリアマップ公開！ブースの配置は？"))
blocks.append(mini_box('<p style="margin:0;">CD BOOTH・ARENA SHOP・FC BOOTH・Plus Chat BOOTH・SPORTS PARK(カプセルトイ・オフィシャルグッズ)などがメインゲート周辺に集約されたレイアウトでした。</p>'))
blocks.append(build_img_html(
    img_area_map,
    "KO1KEYZ 1ST FAN MEETING TOYOTA ARENA TOKYO会場エリアマップ",
    None,
    "https://x.com/KO1KEYZofficial/status/2090257511442244078",
))
blocks.append(p([
    "開催前にKO1KEYZ公式Xが公開したエリアマップによると、TOYOTA ARENA TOKYOの4階JOINT PARKにCD BOOTHとARENA SHOP、3階MAIN GATE付近にプレートライト専用窓口や電子チケット不備対応窓口(海外メンバー向けTicket Desk)が配置されています。",
    "4階SPORTS PARK側にはFC BOOTH・Plus Chat BOOTHが並び、1階SUB ARENA手前にはCOOL SPOT・PHOTO PANEL・カプセルトイ/オフィシャルグッズ/コイン交換のブースがまとまっていました。",
    "会場が広い分、グッズ列とCD予約列、FCブースが別動線に分かれているため、当日は自分の目的(グッズ優先かCD予約優先か)に応じて先に向かうブースを決めておくと動きやすそうです。",
]))
blocks.append(capbox_list("デビューシングル関連キャンペーンの詳細記事", [
    f'<a href="{DEBUT_EVENTS_URL}" target="_blank" rel="noopener">KO1KEYZデビューシングル特典まとめ！SHOWCASE招待・ファンミ抽選会・タワレコ限定応募券</a>',
    f'<a href="{GOODS_EC_URL}" target="_blank" rel="noopener">KO1KEYZ 1STファンミ グッズ・事前EC販売まとめ</a>',
]))

blocks.append(h2("入場時に本人確認・手荷物検査あり"))
blocks.append(mini_box('<p style="margin:0;">アリーナ席は入場時に電子チケットと顔つき身分証明書の提示が必要。スタンド席では本人確認なしという報告もありました。</p>'))
blocks.append(p([
    "開場と同時に現地から「入場開始してます本確ガチガチです」という投稿が相次ぎ、アリーナ席の入場では顔つきの身分証明書の掲示がほぼ必須だったようです。",
    "現地の投稿をまとめると、確認されていたのは主に名前がチケットと一致しているかどうかで、生年月日までは細かく見られていなかったという声もありました。",
    '一方でスタンド席の入場では本人確認がなかったという報告も見られ、<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">座席種別によって確認の厳しさに差があった可能性</span></strong>があります。',
    '手荷物検査もあわせて実施されていたとの投稿があるため、まだ参戦していない公演がある人は、<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">顔写真付きの身分証明書を忘れずに用意しておくと安心</span></strong>です。',
]))

blocks.append(h2("待機列・グッズの状況は？"))
blocks.append(mini_box('<p style="margin:0;">朝9時時点で待機列は約1,000人。13時ごろにはほぼ待ちなしになり、グッズの売り切れは確認されていません。</p>'))
blocks.append(p([
    "現地からのレポートによると、朝9時時点でのグッズ待機列は約1,000人ほど。",
    "そこから列は着実にはけていき、13時ごろにはほぼ待ち時間なしで購入できる状態になっていたようです。",
    "気になるガチャ(カプセルトイ)は15時時点でブースの半分が締め切られていたものの、グッズ自体の売り切れは報告されておらず、FCトレカ・ステッカーも開演前まで在庫があったとのことです。",
    "実際に9時過ぎに会場入りしたという参戦者からは、物販からカプセルトイまでひと通り終えるのに11時ごろまでかかったという声もあり、グッズ・ガチャの両方を回るなら2時間ほど見ておくと安心できそうです。",
    "同じ投稿者からは、土曜日は昼公演・夜公演の2公演があるため、夜公演組は列に並ぶタイミング次第でグッズ購入後の余裕時間が短くなりやすいという注意喚起もありました。",
]))
blocks.append(capbox_list("グッズ・FCブースの詳細記事", [
    f'<a href="{GOODS_EC_URL}" target="_blank" rel="noopener">KO1KEYZ 1STファンミ グッズ・事前EC販売まとめ</a>',
    f'<a href="{FANCLUB_BOOTH_URL}" target="_blank" rel="noopener">KO1KEYZファンミFCブースでトレカ・くじがもらえる？</a>',
]))

blocks.append(h2("初日(DAY1)のセットリストは？"))
blocks.append(mini_box('<p style="margin:0;">DREAMER→恋GAME→BLACK ANGEL→Neko→Soda Pop→KO1KEYZ、アンコールでRun Again・新世界・KO1KEYZという構成でした。</p>'))
blocks.append(capbox_list("東京公演DAY1 セットリスト", [
    "DREAMER(12人全員)",
    "恋GAME(この日が初披露)",
    "BLACK ANGEL(結蘭・シヨン・シンヘン・亮賀・結・竜司の6人)",
    "Neko(加藤・矢田・柳谷・濱田・照井・小野の6人)",
    "Soda Pop",
    "KO1KEYZ",
    "―アンコール―",
    "Run Again(撮影OK・トロッコあり)",
    "新世界",
    "KO1KEYZ(アンコール)",
]))
blocks.append(p([
    "複数の現地投稿を照らし合わせると、BLACK ANGELとNekoはそれぞれ既存メンバー6人ずつのユニット編成で披露され、パート割りは既存の変更なしだったようです。",
    "この日初披露となった恋GAMEは、ダンスブレイクの立ち位置(シヨンがセンターに立ち、結蘭、続いてゆらすけで馬跳びをする流れ)まで踏み込んだ報告もあり、現地では「体感BADが1番歓声やばかった」というBLACK ANGELへの反応も見られました。",
    "セットリストの合間には「古家さんと恋文企画」や「とわすけのミニコーナー」といったトーク企画も挟まれていたようですが、この部分は情報が食い違っており確定的な構成としては言い切れないため、参考情報として紹介するにとどめます。",
]))

blocks.append(h2("アンコールのトロッコ・座席表はどうだった？"))
blocks.append(mini_box('<p style="margin:0;">アンコール1曲目「Run Again」のみ撮影OK。トロッコはアリーナ席の外周通路を1周する演出でした。</p>'))
blocks.append(p([
    "アンコールでは1曲だけ撮影が解禁されるサプライズがあり、披露されたのはRun Againでした。",
    "メンバーがカメラの目の前まで近づいてくれる場面もあったようで、現地のファンからは「近くに来てくれてありがとう」「撮るのに慣れてなさすぎて」と、慌ててシャッターを切った様子がうかがえる投稿が続々と上がり、SNS上でも大きな盛り上がりを見せていました。",
]))
blocks.append(p([
    "同じくこのRun Againでは、メンバーが客席の間を回るトロッコの演出もありました。",
    "トロッコの最中にはメンバーからサインボールが客席に投げ込まれる場面もあったようで、その投げ方がふざけていて可愛かったという声も見られました。",
    "トロッコの通り道について現地で質問が飛び交っていましたが、実際に見た人の回答では、アリーナ席のブロックでいうとA-C1とA-C2の間、A-C6とA-C7の間の通路を通って1周する形だったとのことです。",
]))
blocks.append(build_img_html(
    img_seatmap_official,
    "TOYOTA ARENA TOKYOアリーナ席の座席表(客席図)",
    '現地の座席案内板(座席表)の写真をもとに作成(出典:<a href="https://x.com/22everic/status/2090789679465709589" target="_blank" rel="noopener">https://x.com/22everic/status/2090789679465709589</a>)',
    "https://x.com/22everic/status/2090789679465709589",
))
blocks.append(p([
    "現地の座席表(座席案内板)を見ると、アリーナ席はステージ側からA列・B列・C列の3列×7ブロック(1〜7)で構成され、最後列側にD2・D6という飛び番のブロックがあり、その間には機材スペースが挟まっている配置でした。",
    "この配置と照らし合わせると、トロッコはステージに向かって左右の外側寄りの通路(A-C1とA-C2の間、A-C6とA-C7の間)を回るルートだったことになります。",
    'スタンドとアリーナの間の外周を回ったという証言もあり、アリーナ席の端に近いブロックほどトロッコが近くを通りやすかったと考えられます。<br>\n各ブロックの座席番号・列数についても参戦者からの報告が集まっており、<strong>Aブロックは最大14列・Bブロックは最大16列・Cブロックは最大13列まで</strong>確認されているようです(あくまでファンの報告に基づく目安のため、実際の座席数と多少ズレる可能性があります)。',
]))
blocks.append(p([
    "本編ラストの挨拶タイムでは、RYOGAが涙腺が緩みそうになる場面もあったようです。",
    "周りのメンバーから「泣かないで」と声がかかったり、顔を手で覆って止められたりする中、RYOGA自身が首を振ってこらえ、最後は泣かずに終えられて「セーフ…!」となったという、ほほ笑ましいやり取りも現地から伝えられています。",
]))
blocks.append(p([
    "フィナーレでは銀テープ(紙吹雪演出用のテープ)も飛び、キャッチできたファンからは12人全員分のサインがデザインされたテープだったという報告もありました。",
    "持ち帰れる記念アイテムとして拾えた人には嬉しいサプライズだったようです。",
]))
blocks.append(build_img_html(
    img_ginte,
    "KO1KEYZ 1ST FAN MEETINGの銀テープ、12人全員分のサイン入り",
    None,
    "https://x.com/arigato___ryg/status/2091036014882222461",
))

blocks.append(h2("まとめ"))
blocks.append(notebox('''<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">KO1KEYZ 1STファンミ東京公演DAY1まとめ</p>
<p style="margin:0;">
&#10003; 18:30開演・20:26終演、アンコール・トロッコを含め正味約2時間<br>
&#10003; 会場はTOYOTA ARENA TOKYO、CD BOOTH・ARENA SHOP・FC BOOTHなどがエリアマップで公開済み<br>
&#10003; アリーナ入場時は顔つき身分証明書での本人確認・手荷物検査あり(スタンド席は確認なしとの報告も)<br>
&#10003; 朝9時に待機列約1,000人も13時にはほぼ解消、グッズの売り切れは報告なし<br>
&#10003; セトリはDREAMER〜KO1KEYZ、アンコールはRun Again(撮影OK・トロッコ)→新世界→KO1KEYZ
</p>'''))
blocks.append(p([
    "初日から本人確認・グッズ列・セトリ・撮影OKタイムまで盛りだくさんの情報が飛び交ったKO1KEYZ初のファンミーティング。",
    "DAY2以降に参戦予定の人は、身分証明書を忘れずに、グッズは午前中の早い時間帯を狙ってみるのがよさそうです。",
    "サインボールも投げられるようなので、運を味方につけて絶対ゲットしたいですね！家宝にしたい！！！",
]))

blocks.append(notebox(f'''<p style="margin:0 0 8px 0;"><strong>KO1KEYZ 1STファンミについては、このブログの他の記事でも詳しく紹介しています。</strong></p>
<ul style="margin:0;padding-left:1.2em;">
<li><a href="{DEBUT_EVENTS_URL}" target="_blank" rel="noopener">KO1KEYZデビューシングル特典まとめ！SHOWCASE招待・ファンミ抽選会・タワレコ限定応募券</a></li>
<li><a href="{FANCLUB_BOOTH_URL}" target="_blank" rel="noopener">KO1KEYZファンミFCブースでトレカ・くじがもらえる？</a></li>
<li><a href="{GOODS_EC_URL}" target="_blank" rel="noopener">KO1KEYZ 1STファンミ グッズ・事前EC販売まとめ</a></li>
<li><a href="{FANMEETING_PREDICT_URL}" target="_blank" rel="noopener">KO1KEYZのライブ・ファンミはいつ？ラポネ傾向から日程を大予想！</a></li>
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


SUMMARY = "KO1KEYZ初のファンミーティング東京公演DAY1の様子をまとめました。会場エリアマップ、入場時の本人確認、待機列・グッズ状況、初日のセットリスト、アンコールの撮影OKタイムとトロッコまで紹介しています。"

slug = get_slug(title, "ko1keyz-1st-fanmeeting-tokyo-day1")
print("slug:", slug)
payload = {
    "title": title,
    "content": content,
    "slug": slug,
    "status": "draft",
    "categories": [66, 62],
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

with open(ROOT / "tmp_ko1keyz_fanmi_day1_postid.txt", "w", encoding="utf-8") as f:
    f.write(str(post["id"]))
