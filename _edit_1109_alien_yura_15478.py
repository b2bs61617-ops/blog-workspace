# -*- coding: utf-8 -*-
"""2026-11-09 オシリ依頼: エイリアンキーホルダー記事(JP15478/KR15479/EN15480、下書き)にYURAを追加+タイトル変更。
YURAの分: WoWKorea FAN 公式YouTube WBUHuDk_BFg 5:47(347.5s)のチェックイン場面、黒いチェーンバッグに
 TOWAから10/27にもらったロケット(記事15284)と並んで蓄光グリーンのエイリアン。瞳の色は横向きで不明。
きっかけ: towadaisukiiii(ファン投稿、本文では触れない・画像使わない)。
"""
import json, re, sys
from pathlib import Path
import requests
from _mubank1009_helpers import ROOT, WP_URL, HEADERS_AUTH, wp_upload, img_html, h2, p

HJ = {**HEADERS_AUTH, "Content-Type": "application/json"}
STATE = ROOT / "images" / "_yura_alien_1109_state.json"
WOW = "https://www.youtube.com/watch?v=WBUHuDk_BFg"
MB = 'class="swl-marker mark_blue"'

state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
for k, name in [("full", "yura_gimpo1109_alien_full.jpg"), ("zoom", "yura_gimpo1109_alien_zoom.jpg")]:
    if k not in state:
        m = wp_upload(ROOT / "images" / name, "image/jpeg")
        state[k] = {"id": m["id"], "source_url": m["source_url"], "media_details": m["media_details"]}
        STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
FULL, ZOOM = state["full"], state["zoom"]


def get(pid):
    return requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", params={"context": "edit"}, headers=HEADERS_AUTH).json()


def rep(t, old, new, pid):
    assert t.count(old) == 1, (pid, old[:60], t.count(old))
    return t.replace(old, new)


def save(pid, title, content):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=HJ,
                      data=json.dumps({"title": title, "content": content}).encode("utf-8"))
    r.raise_for_status()
    print(pid, r.json()["status"], r.json()["title"]["raw"])


# ---------------- JP ----------------
d = get(15478); t = d["content"]["raw"]
t = rep(t, "TOWA(濱田永遠さん)とKOSUKE(照井康祐さん)のバッグに、そっくりなキーホルダーが下がっていました。",
        "TOWA(濱田永遠さん)とKOSUKE(照井康祐さん)、そしてYURA(安部結蘭さん)のバッグに、そっくりなキーホルダーが下がっていました。", 15478)
t = rep(t, "この記事では、キーホルダーの正体と値段、2人がおそろいなのかを調べました。",
        "この記事では、キーホルダーの正体と値段、3人がおそろいなのかを調べました。", 15478)
t = rep(t, ">TOWAとKOSUKEのキーホルダー</p>", ">TOWA・KOSUKE・YURAのキーホルダー</p>", 15478)
t = rep(t, "<li>TOWAとKOSUKEのエイリアンのキーホルダーの正体</li>",
        "<li>TOWA・KOSUKE・YURAのエイリアンのキーホルダーの正体</li>", 15478)
t = rep(t, "<li>2人はおそろいなのか</li>",
        "<li>YURAのバッグではTOWAからもらったロケットの隣に</li>\n<li>3人はおそろいなのか</li>", 15478)
yura_jp = "\n\n".join([
    h2("YURAのバッグにもエイリアン！TOWAのロケットの隣に"),
    p("同じ日、チェックインカウンターに並んだYURAのバッグにも、<strong><span " + MB + ' style="font-size:1.15em;">同じ淡い黄緑色のエイリアン</span></strong>が下がっていました。<br>\n'
      "水色のジャケットに青いキャップのYURAが、肩にかけていた黒いチェーンのバッグです。"),
    img_html(FULL, "金浦空港のチェックインカウンターに並ぶYURA(安部結蘭)", f"出典：{WOW}"),
    img_html(ZOOM, "YURA(安部結蘭)のバッグに付いたロケットとエイリアンのキーホルダー", f"出典：{WOW}"),
    p("チェーンの先には、水色のボディに紫の羽、赤い丸窓のロケットのキーホルダーと並んで、丸い大きな頭のエイリアンが付いています。<br>\n"
      "頭が横を向いているので、瞳の色までは分かりませんが、体の色と頭の形はTOWA・KOSUKEのものとそっくりです。"),
    p("注目したいのは、隣のロケットです。<br>\n"
      "このロケットは、10月27日にTOWAが練習終わりにYURAへプレゼントした、ドリームズの「プロジェクターロケット」とみられます。<br>\n"
      "<strong>TOWAからもらったロケットの隣に、TOWAとおそろいのエイリアン</strong>が付いているので、ファンの間でも「エイリアンもTOWAからのプレゼントでは？」と気になる組み合わせです。<br>\n"
      'ロケットのくわしい情報は<a href="https://chomoand-1.com/yura-towa-gift-projector-rocket-keychain-15284">YURAがTOWAにもらったロケットキーホルダーの記事</a>でまとめています。'),
])
t = rep(t, '<!-- wp:heading -->\n<h2 class="wp-block-heading">エイリアンはDETAILの「グロー エイリアン キーチェーン」</h2>',
        yura_jp + '\n\n<!-- wp:heading -->\n<h2 class="wp-block-heading">エイリアンはDETAILの「グロー エイリアン キーチェーン」</h2>', 15478)
t = rep(t, "<p>2人のキーホルダーは、雑貨ブランドDETAIL", "<p>3人のキーホルダーは、雑貨ブランドDETAIL", 15478)
t = rep(t, '<h2 class="wp-block-heading">TOWAとKOSUKEはおそろい？</h2>',
        '<h2 class="wp-block-heading">TOWA・KOSUKE・YURAはおそろい？</h2>', 15478)
t = rep(t, "<p>2人のキーホルダーは、同じ商品の色ちがいか、同じ色のおそろいとみられます。<br>\nTOWAのものは瞳がグリーンでした。<br>\nKOSUKEのものは映像では瞳の色が見えず、同じグリーンなのか、別の色なのかは分かりません。</p>",
        "<p>3人のキーホルダーは、同じ商品の色ちがいか、同じ色のおそろいとみられます。<br>\nTOWAのものは瞳がグリーンでした。<br>\nKOSUKEとYURAのものは映像では瞳の色が見えず、同じグリーンなのか、別の色なのかは分かりません。</p>", 15478)
t = rep(t, "どちらかが買ってプレゼントしたのか、一緒に買ったのかなど、2人がこのキーホルダーについて話したことはまだありません。<br>\nKO1KEYZでは、YURAとTOWAがロケットのキーホルダーをプレゼントしあったこともあり、メンバーどうしでキーホルダーを贈りあう仲のよさが知られています。",
        "誰かが買ってプレゼントしたのか、一緒に買ったのかなど、3人がこのキーホルダーについて話したことはまだありません。<br>\nただ、TOWAは10月27日にYURAへロケットのキーホルダーをプレゼントしていて、YURAはそのロケットとエイリアンを同じチェーンに付けていました。<br>\nキーホルダーを贈るのが好きなTOWAが、エイリアンも配ったのかもしれませんね。", 15478)
CK = '<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid #2f4a8a;border-radius:3px;color:#2f4a8a;font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>'
t = rep(t, CK + "11月9日の金浦空港で、TOWAとKOSUKEのバッグにエイリアンのキーホルダーが付いていた<br>",
        CK + "11月9日の金浦空港で、TOWA・KOSUKE・YURAのバッグにエイリアンのキーホルダーが付いていた<br>\n"
        + CK + "YURAはTOWAにもらったロケットの隣にエイリアンを付けていた<br>", 15478)
t = rep(t, CK + "TOWAのものは瞳がグリーン、KOSUKEのものは瞳の色が映像では分からない<br>",
        CK + "TOWAのものは瞳がグリーン、KOSUKE・YURAのものは瞳の色が映像では分からない<br>", 15478)
t = rep(t, "空港で並んだTOWAとKOSUKEのバッグに、さりげなくおそろいのキーホルダーが光っていました。<br>\n次の空港でも、2人のバッグのエイリアンに注目ですね！",
        "空港で並んだTOWAとKOSUKE、そしてYURAのバッグに、さりげなくおそろいのキーホルダーが光っていました。<br>\n次の空港では、ほかのメンバーのバッグにもエイリアンが増えているかもしれません！", 15478)
t = rep(t, ">TOWA・KOSUKE・KO1KEYZの関連記事</p>", ">TOWA・KOSUKE・YURA・KO1KEYZの関連記事</p>", 15478)
save(15478, "【未】【KO1KEYZ】TOWA・KOSUKE・YURAのエイリアンはどこの？", t)

# ---------------- KR ----------------
d = get(15479); t = d["content"]["raw"]
t = rep(t, "TOWA(하마다 토와)와 KOSUKE(테루이 코스케)의 가방에 똑같이 생긴 키링이 달려 있었습니다.",
        "TOWA(하마다 토와)와 KOSUKE(테루이 코스케), 그리고 YURA(아베 유라)의 가방에 똑같이 생긴 키링이 달려 있었습니다.", 15479)
yura_kr = "\n\n".join([
    h2("YURA의 가방에도 에일리언! TOWA가 준 로켓 옆에"),
    p("같은 날 체크인 카운터에 선 YURA의 검은 체인 가방에도 같은 연두색 에일리언이 달려 있었습니다.<br>\n"
      "물색 바디에 보라색 날개의 로켓 키링 바로 옆입니다. 머리가 옆을 향하고 있어 눈 색은 보이지 않습니다."),
    img_html(FULL, "김포공항 체크인 카운터의 YURA", f"출처: {WOW}"),
    img_html(ZOOM, "YURA 가방의 로켓과 에일리언 키링", f"출처: {WOW}"),
    p("이 로켓은 10월 27일 TOWA가 연습 후 YURA에게 선물한 드림즈 '프로젝터 로켓'으로 보입니다.<br>\n"
      "TOWA에게 받은 로켓 옆에 TOWA와 같은 에일리언이 달려 있는 셈입니다. "
      '(<a href="https://chomoand-1.com/ko/yura-towa-gift-projector-rocket-keychain-kr-15286">YURA와 TOWA의 로켓 키링 글</a>)'),
])
t = rep(t, '<!-- wp:heading -->\n<h2 class="wp-block-heading">DETAIL \'글로우 에일리언 키체인\'</h2>',
        yura_kr + '\n\n<!-- wp:heading -->\n<h2 class="wp-block-heading">DETAIL \'글로우 에일리언 키체인\'</h2>', 15479)
t = rep(t, "두 사람은 커플템?", "세 사람은 커플템?", 15479)
t = rep(t, "TOWA는 그린, KOSUKE는 영상으로 눈 색이 확인되지 않습니다. 두 사람이 이 키링에 대해 직접 말한 적은 아직 없습니다.",
        "TOWA는 그린, KOSUKE와 YURA는 영상으로 눈 색이 확인되지 않습니다. 세 사람이 이 키링에 대해 직접 말한 적은 아직 없습니다.", 15479)
t = rep(t, "TOWA와 KOSUKE의 가방에 빛나는 에일리언 키링", "TOWA・KOSUKE・YURA의 가방에 빛나는 에일리언 키링", 15479)
save(15479, "【未】【KO1KEYZ】TOWA・KOSUKE・YURA 에일리언 키링은 커플템?", t)

# ---------------- EN ----------------
d = get(15480); t = d["content"]["raw"]
t = rep(t, "TOWA (Hamada Towa) and KOSUKE (Terui Kosuke) had look-alike keychains on their bags",
        "TOWA (Hamada Towa), KOSUKE (Terui Kosuke) and YURA (Abe Yura) had look-alike keychains on their bags", 15480)
yura_en = "\n\n".join([
    h2("YURA has one too, right next to TOWA's rocket"),
    p("At the check-in counter the same day, YURA's black chain bag also carried the same pale-green alien.<br>\n"
      "It hangs right beside a light-blue rocket keychain with purple fins. The alien's head faces sideways, so its eye color can't be seen."),
    img_html(FULL, "YURA at the Gimpo Airport check-in counter", f"Source: {WOW}"),
    img_html(ZOOM, "The rocket and alien keychains on YURA's bag", f"Source: {WOW}"),
    p("That rocket appears to be the Dreams 'Projector Rocket' TOWA gave YURA after practice on October 27.<br>\n"
      "So the alien matching TOWA's sits right next to TOWA's gift. "
      '(<a href="https://chomoand-1.com/en/yura-towa-gift-projector-rocket-keychain-en-15287">YURA and TOWA\'s rocket keychains</a>)'),
])
t = rep(t, '<!-- wp:heading -->\n<h2 class="wp-block-heading">DETAIL\'s Glow Alien Keychain</h2>',
        yura_en + '\n\n<!-- wp:heading -->\n<h2 class="wp-block-heading">DETAIL\'s Glow Alien Keychain</h2>', 15480)
t = rep(t, "TOWA's has green eyes; KOSUKE's eye color can't be confirmed. Neither has talked about it yet.",
        "TOWA's has green eyes; KOSUKE's and YURA's eye colors can't be confirmed. None of them has talked about it yet.", 15480)
t = rep(t, "TOWA and KOSUKE both had glow-in-the-dark alien keychains", "TOWA, KOSUKE and YURA all had glow-in-the-dark alien keychains", 15480)
save(15480, "【未】[KO1KEYZ] TOWA, KOSUKE & YURA's Matching Alien Keychains?", t)
