# -*- coding: utf-8 -*-
# chomoand-4.blog: トラジャ松松が辰巳雄大の家でシャボン玉？トークィーンズ(2026/11/4)のエピソード
# 2026-11-06 オシリ依頼。材料: TVer本編(epbvo4wenq)の文字起こし・フレーム、辰巳雄大さん公式Instagram(2024/11/18)、
# モデルプレス(2023/4/7 王道テレビ)、日刊スポーツ・めざましmedia(2026/11/5)。
# きっかけのX投稿(一般ファン)は参考のみで本文に載せない。
import json, sys, subprocess
from pathlib import Path
import requests

from build_and_post_travis_japan_tour2027_odds_survey import (
    ROOT, WP_URL, HJSON, SITE, ACC, BORDER, BG, p, h2, h3, wphtml, mark,
    whatbox, minibox, table2, checklist, related, upload_media)

IMG_DIR = ROOT / "images" / "tj_matsumatsu_shabondama"
EYECATCH = IMG_DIR / "tj_matsumatsu_shabondama_eyecatch_canva.jpg"
STATE = IMG_DIR / "_state.json"
DRY = "--dry" in sys.argv

TITLE = "トラジャ松松が辰巳雄大の家でシャボン玉？トークィーンズのエピソード！"
SLUG = "travis-japan-matsumatsu-tatsumi-shabondama"

TVER_URL = "https://tver.jp/episodes/epbvo4wenq"
IG_URL = "https://www.instagram.com/p/DCgTdeTThs8/"
MDPR_URL = "https://mdpr.jp/news/detail/3688623"

FRAMES = {
    "yuiitsu": (IMG_DIR / "hf_284.jpg", "トークィーンズのVTRで辰巳雄大について話す松田元太と松倉海斗"),
    "card": (IMG_DIR / "hf_290.jpg", "「家でシャボン玉を吹いても絶対怒らない優しい先輩」のテロップ"),
    "tatsumi": (IMG_DIR / "hf_345.jpg", "スタジオでシャボン玉のエピソードを話す辰巳雄大"),
}

GENTA = ("松田元太の憧れの先輩は誰？山田涼介との関係とエピソード！", "matsuda-genta-senpai-yamada-ryosuke")
KAITO = ("松倉海斗の憧れの先輩は誰？二宮和也や堂本剛との関係！", "matsukura-kaito-senpai-nino-tsuyoshi")
COMBI = ("トラジャのコンビ名一覧！いちごみるくやトリプルカイトとは？", "travis-japan-combi-names")
SANSEI = ("トラジャの「さんせーい」はいつから？円陣の掛け声の由来と経緯！", "travis-japan-sansei-call-origin")

TIMELINE = [
    ("2015年", "松倉海斗さんが『Endless SHOCK』に初出演。ここからふぉ～ゆ～との付き合いが始まる"),
    ("2017年11月", "松田元太さん・松倉海斗さんがそろってTravis Japanに加入"),
    ("2023年4月", "『ふぉ～ゆ～の王道テレビ』で辰巳雄大さんが「元太・海斗はウチくるのよ」とシャボン玉の話を初披露"),
    ("2024年11月", "辰巳雄大さんがInstagramに松松との3ショット。「#家の中で #海斗が #シャボン玉やりおった」"),
    ("2026年11月4日", "『トークィーンズ』で松松がVTR出演。「家でシャボン玉をやっても許してくれる先輩」と紹介"),
    ("2026年11月11日", "ふぉ～ゆ～がシングル『BLOOM WORLD』でCDデビュー"),
]


def figure(media, alt, src_url):
    sizes = media.get("sizes", {})
    large = sizes.get("large") or sizes.get("full")
    medium = sizes.get("medium") or large
    full = sizes.get("full") or large
    return wphtml(f'''<figure class="wp-block-image size-large">
<img src="{large['url']}" alt="{alt}" width="{large['w']}" height="{large['h']}" style="max-width:100%;height:auto;" srcset="{medium['url']} {medium['w']}w, {large['url']} {large['w']}w, {full['url']} {full['w']}w" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption>出典:{src_url}</figcaption>
</figure>''')


def upload_with_sizes(path, title, alt):
    m = upload_media(path, title, alt)
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/media/{m['id']}", headers=HJSON)
    r.raise_for_status()
    d = r.json()["media_details"]
    sizes = {k: {"url": v["source_url"], "w": v["width"], "h": v["height"]} for k, v in d.get("sizes", {}).items()}
    return {"id": m["id"], "sizes": sizes}


def ig_embed(u, label):
    return f"""<!-- wp:html -->
<div style="max-width:540px;margin:0 auto 16px;"><blockquote class="instagram-media" data-instgrm-permalink="{u}" data-instgrm-version="14" style="background:#FFF;border:0;border-radius:3px;box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15);margin:1px;max-width:540px;min-width:326px;padding:0;width:calc(100% - 2px);"><a href="{u}" target="_blank" rel="noopener">{label}</a></blockquote>
<script async src="https://www.instagram.com/embed.js"></script></div>
<!-- /wp:html -->"""


def timeline_box():
    rows = "\n".join(
        f'<div style="display:flex;margin:0 0 10px 0;"><span style="flex:0 0 8.5em;font-weight:bold;color:{ACC};">{y}</span><span style="flex:1;">{t}</span></div>'
        for y, t in TIMELINE)
    return wphtml(f'''<div style="border:1px solid {BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">
<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACC};color:#fff;">松松とふぉ～ゆ～・シャボン玉の年表</p>
<div style="padding:14px 18px 6px 18px;background:{BG};">
{rows}
</div>
</div>''')


def build(frames=None):
    frames = frames or {}

    def fr(key):
        if key in frames:
            b.append(figure(frames[key], FRAMES[key][1], TVER_URL))

    b = []
    b.append(p([
        f"Travis Japanの松田元太さんと松倉海斗さん(松松)が、ふぉ～ゆ～の辰巳雄大さんの家で{mark('部屋の中なのにシャボン玉を吹いた')}というエピソードが話題になっています。",
        "2026年11月4日放送の『トークィーンズ』(フジテレビ)で、松松がVTRで辰巳雄大さんを「家でシャボン玉をやっても許してくれる先輩」と紹介し、辰巳雄大さん本人がスタジオでその夜のことをくわしく話しました。",
        f"実はこの話、{mark('2023年のテレビ、2024年の辰巳雄大さんのInstagramに続いて3回目')}の登場で、ふぉ～ゆ～とトラジャの間では鉄板ネタになっています。",
        "この記事では、トークィーンズで話された内容と、これまでのシャボン玉エピソード、松松とふぉ～ゆ～の関係をまとめます。",
    ]))
    b.append(whatbox([
        "トークィーンズで松松が話した辰巳雄大の「シャボン玉」エピソード",
        "シャボン玉を吹いたのは元太？海斗？辰巳くんのInstagramのハッシュタグ",
        "2023年の『王道テレビ』でも話していた？これまでの流れ",
        "松松が話したふぉ～ゆ～4人それぞれの人柄",
        "松松とふぉ～ゆ～の出会いは『Endless SHOCK』",
    ]))
    b.append(minibox([
        ("番組", "トークィーンズ(フジテレビ)"),
        ("放送日", "2026年11月4日(水)"),
        ("ゲスト", "ふぉ～ゆ～(福田悠太・辰巳雄大・越岡裕貴・松崎祐介)"),
        ("VTR出演", "Travis Japan 松田元太・松倉海斗"),
        ("見逃し配信", f'<a href="{TVER_URL}" target="_blank" rel="noopener">TVer</a>'),
    ]))

    # ---- toukqueens ----
    b.append(h2("トークィーンズで松松が話した「シャボン玉」エピソード"))
    b.append(p([
        "ふぉ～ゆ～は2026年11月11日にシングル『BLOOM WORLD』でCDデビューします。",
        "デビュー発表後、グループとして初めてのテレビ出演となったこの回で、「ふぉ～ゆ～大好き後輩」として登場したのが松田元太さんと松倉海斗さんです。",
        "2人はおそろいのアディダスのトラックトップ姿でVTRに出演し、「10年以上お世話になっている」ふぉ～ゆ～のメンバー1人ずつについて、どんな人なのかを話しました。",
    ]))
    b.append(h3("「唯一、シャボン玉を家でやっても許してくれる先輩」"))
    b.append(p([
        "辰巳雄大さんについて聞かれた2人は、「2人でご飯に連れて行ってくださったりして、そのまま辰巳くんの家に行ったりとかして」と話し始めます。",
        f"そして松田元太さんが、辰巳雄大さんは{mark('「唯一、シャボン玉を家でやっても許してくれる先輩」')}だと紹介しました。",
        "VTRでは「僕らが持ってきたシャボン玉を家で吹かせてもらったり」とも話していて、隣の松倉海斗さんは大笑いでした。",
    ]))
    fr("yuiitsu")
    b.append(p([
        "番組のテロップでは、辰巳雄大さんは「家でシャボン玉を吹いても絶対怒らない優しい先輩」とまとめられました。",
    ]))
    fr("card")
    b.append(p([
        "このVTRを見たスタジオでは、ファーストサマーウイカさんが「怖い」「持ってくるのも怖いし、許すのも怖い」とツッコみ、笑いが起きていました。",
        "ちなみに福田悠太さんについては「親戚のおじいさんみたい」「介護というか、優しく接してあげたい」と話していて、後輩から先輩への愛のあるイジりがたっぷりのVTRでした。",
    ]))

    b.append(h3("辰巳雄大が話した「1時間後、辰巳くんの家集合」の夜"))
    b.append(p([
        "VTRのあと、辰巳雄大さんがスタジオでその夜のことを話しました。",
        f"ある日、松松から「辰巳くん今どこにいますか？」と連絡が来て、知り合いとご飯を食べていると返すと、{mark('「わかりました、じゃあ1時間後に辰巳くんの家集合でいいですか？」')}と返ってきたそうです。",
        "「ご飯食べてるよって言ってるのに」と思いつつ、ちょうど終わりそうだったので「じゃあうちの前集合な」と答えると、2人は両手いっぱいにコンビニでいろいろ買い込んでやって来ました。",
    ]))
    fr("tatsumi")
    b.append(p([
        "袋の中には乾杯用の飲み物やおつまみと一緒に、なぜかシャボン玉が入っていました。",
        "辰巳雄大さんは「まあまあ、ボケだろう」と思って気にせず、一緒に乾杯して「最近トラジャどうだ」と近況を話していたそうです。",
        f"ところが返事は「まあ、そうっすね～」と言いながら、{mark('タバコを吸うようにシャボン玉を「シュー」')}。",
        "「全然タバコじゃない」「やめろ」とツッコんだという話に、スタジオは大笑いでした。",
        "あまりに話が長かったので、若槻千夏さんから「シャボン玉の話長いな」とツッコまれる場面もありました。",
    ]))

    # ---- instagram ----
    b.append(h2("シャボン玉を吹いたのはまちゅ？辰巳雄大のInstagram"))
    b.append(p([
        "このシャボン玉事件、実は辰巳雄大さん本人のInstagramにも残っています。",
        "2024年11月18日、辰巳雄大さんは「元太と海斗がSHOCKに来たぞ～！」と、松松との3ショットを投稿しました。",
    ]))
    b.append(ig_embed(IG_URL, "辰巳雄大さん(@yudai_tatsumi__1125)のInstagram投稿"))
    b.append(p([
        "注目はハッシュタグで、つなげて読むと1つの文章になっています。",
    ]))
    b.append(table2(["ハッシュタグ", "意味"], [
        ["#クソかわいい弟", "松松はかわいい弟分"],
        ["#ご飯食べて #辰巳家来て", "『Endless SHOCK』のあと、ご飯→辰巳家へ"],
        ["#家の中で #海斗が #シャボン玉やりおった", "部屋の中でシャボン玉を吹いたのは松倉海斗さん"],
        ["#元太は #俺大人なんでやらないっす #ってこんな顔でみてた", "松田元太さんは「俺大人なんでやらないっす」と言って見ていた"],
        ["#やりたそうだった", "でも本当はやりたそうだった"],
        ["#家来てシャボン玉するのやめれる？", "家に来てシャボン玉するの、やめてくれる？"],
    ]))
    b.append(p([
        f"このときに実際にシャボン玉を吹いたのは{mark('松倉海斗さん')}で、松田元太さんは「俺大人なんでやらないっす」とクールに見ていたそうです。",
        "それでも辰巳雄大さんいわく「やりたそうだった」とのことで、2人のキャラクターがよく出ています。",
        "最後の「#家来てシャボン玉するのやめれる？」からは、1回だけのことではなく、辰巳家に来るたびにシャボン玉が出てくることがうかがえます。",
        "トークィーンズでは「2人が持ってきたシャボン玉」と話されていたので、今では松田元太さんも一緒に楽しんでいるのかもしれません。",
    ]))
    b.append(p([
        "投稿は『Endless SHOCK』の公演期間中のもので、昔一緒に舞台に立っていた後輩の松松が観に来て、そのまま辰巳家で遊んだことが分かります。",
    ]))

    # ---- 2023 ----
    b.append(h2("2023年の『ふぉ～ゆ～の王道テレビ』でも話していた"))
    b.append(p([
        f"シャボン玉の話が最初にテレビで出たのは、2023年4月6日深夜放送の『ふぉ～ゆ～の王道テレビ ～これにかけてるんで！』(日本テレビ系)です(<a href=\"{MDPR_URL}\" target=\"_blank\" rel=\"noopener\">モデルプレス</a>)。",
        "松松がゲストで出演した回で、辰巳雄大さんが「元太・海斗はウチくるのよ」と切り出しました。",
        f"2人は{mark('「辰巳くん家で楽しもうと思ってシャボン玉買っちゃいました」')}と言って、家の中でシャボン玉を始めたそうです。",
        "「部屋の中で？ベランダとかじゃないの？」と聞かれると、松松は手を合わせて謝るポーズをしながら笑ってうなずいていました。",
    ]))
    b.append(p([
        "2023年にテレビで話し、2024年にInstagramで報告し、2026年のトークィーンズで改めて松松の口から語られた、という流れです。",
        "ふぉ～ゆ～のデビューという大事なタイミングで、昔からのおなじみの話を後輩の松松が持ってきたことに、Xでも喜ぶファンの声が見られました。",
    ]))
    b.append(timeline_box())

    # ---- others ----
    b.append(h2("松松が話したふぉ～ゆ～4人の人柄"))
    b.append(p([
        "トークィーンズのVTRでは、辰巳雄大さん以外のメンバーについても松松がエピソードを話しています。",
    ]))
    b.append(table2(["メンバー", "松松から見た姿"], [
        ["福田悠太", "親戚のおじいさんみたい。介護というか、優しく接してあげたい"],
        ["辰巳雄大", "家でシャボン玉をやっても許してくれる唯一の先輩"],
        ["越岡裕貴", "めちゃくちゃ優しいフッ軽兄さん"],
        ["松崎祐介", "松倉海斗さんの「師匠」"],
    ]))
    b.append(h3("越岡裕貴は深夜1時でも来てくれる「フッ軽兄さん」"))
    b.append(p([
        "越岡裕貴さんについては、深夜1時ごろにご飯を食べているときにノリで電話して「来てくださいよ」と誘ったら、数十分後に本当に来てくれたというエピソードが出ました。",
        "松倉海斗さんは「気を使わない距離感が、後輩からするとありがたい」と話しています。",
        "スタッフから入所同期にKAT-TUNの上田竜也さんがいると聞かれると、KAT-TUNの先輩にはできないと言いつつ、越岡裕貴さんには「めっちゃいけます」と声をそろえていました。",
    ]))
    b.append(h3("松崎祐介は「殺陣はまず横から」の師匠"))
    b.append(p([
        "松倉海斗さんが「師匠」と呼んでいるのが松崎祐介さんです。",
        "『Endless SHOCK』に殺陣(たて)のナンバーがあり、松倉海斗さんが「殺陣ってどうやったらうまくなりますか？」と相談したところ、松崎祐介さんは「まず殺陣をうまくなろうとするな、まずは横からだ」とアドバイスしたそうです。",
        "殺陣を「縦」と素で間違えていたのでは？という話に、スタジオでは松崎祐介さんが「緊張を和らげようとした」「斜めもいけたけど、あえて横だよ」と弁解し、若槻千夏さんから「師匠、30年何やってたんですか？」とツッコまれていました。",
    ]))
    b.append(h3("「ステージに立つとプロ集団」とリスペクトも"))
    b.append(p([
        "イジりの多いVTRでしたが、最後には「パフォーマンスするときはずば抜けてレベルやスキルが高い」「そのギャップがかっこいい」「本当にプロ集団」と、先輩へのリスペクトも語っています。",
        "松田元太さんは初めてふぉ～ゆ～に会ったとき、事務所の人ではなく外部のダンサーさんだと思っていたそうで、「それくらい全部が完璧」「嫌いな人は絶対いない」と話していました。",
    ]))

    # ---- relation ----
    b.append(h2("松松とふぉ～ゆ～の出会いは『Endless SHOCK』"))
    b.append(p([
        "松松とふぉ～ゆ～をつないだのは、堂本光一さん主演の舞台『Endless SHOCK』です。",
        f"トークィーンズのVTRで松倉海斗さんは、{mark('初めて『SHOCK』の舞台に出たのが2015年、17歳のとき')}で、そこから11年くらいお世話になっていると話しています。",
        "松田元太さんもちょうど同じころからの付き合いで、2人ともふぉ～ゆ～を「本当にお兄ちゃんみたいな存在」と表現しました。",
    ]))
    b.append(p([
        "2023年の『王道テレビ』では、松田元太さんが「ジャニーズの方とは思ってないままお会いして、俳優さんの枠で出られていると思っていた」と、初対面の印象を明かしています(<a href=\"" + MDPR_URL + "\" target=\"_blank\" rel=\"noopener\">モデルプレス</a>)。",
        "松田元太さんと松倉海斗さんは2017年11月にそろってTravis Japanに加入しましたが、その前の舞台時代から、ふぉ～ゆ～にかわいがられてきた後輩なのです。",
        f'松田元太さん・松倉海斗さんそれぞれの憧れの先輩については、<a href="{SITE}{GENTA[1]}">{GENTA[0]}</a>・<a href="{SITE}{KAITO[1]}">{KAITO[0]}</a>でも紹介しています。',
    ]))

    # ---- matome ----
    b.append(h2("まとめ"))
    b.append(checklist("この記事のポイント", [
        "2026年11月4日の『トークィーンズ』で、松松が辰巳雄大を「唯一、家でシャボン玉をやっても許してくれる先輩」と紹介",
        "「1時間後、辰巳くんの家集合でいいですか？」と連絡し、コンビニ袋にシャボン玉を入れて訪問",
        "近況を聞かれながら、タバコのようにシャボン玉を「シュー」",
        "2024年の辰巳雄大のInstagramでは「#海斗が #シャボン玉やりおった」「#元太は #俺大人なんでやらないっす」",
        "最初に話されたのは2023年の『ふぉ～ゆ～の王道テレビ』",
        "松松とふぉ～ゆ～は『Endless SHOCK』からの10年以上の付き合い",
    ]))
    b.append(p([
        "デビューを控えたふぉ～ゆ～のお祝いの回で、松松らしいかわいいエピソードが聞けてほっこりしました！",
        "ふぉ～ゆ～のデビューシングル『BLOOM WORLD』は2026年11月11日発売です。",
        "これからも松松とふぉ～ゆ～の仲良しエピソードが聞けるのが楽しみですね！",
    ]))
    b.append(related([GENTA, KAITO, COMBI, SANSEI]))
    return "\n\n".join(b)


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    if DRY:
        html = build()
        (IMG_DIR / "_dry.html").write_text(html, encoding="utf-8")
        print("dry chars:", len(html))
        return
    state.setdefault("frames", {})
    for key, (path, alt) in FRAMES.items():
        if key not in state["frames"]:
            state["frames"][key] = upload_with_sizes(path, alt, alt)
    STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    html = build(state["frames"])
    tmp = IMG_DIR / "_post.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "fix", "--group", "travis", str(tmp)], check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "honorific.py"), "check", "--group", "travis", str(tmp)], check=True)
    html = tmp.read_text(encoding="utf-8")
    if not EYECATCH.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_torahja_canva.py"),
                        "--main", "松松", "--bottom", "辰巳くんの家でシャボン玉？",
                        "--bottom", "トークィーンズのエピソード！", "--color-key", "松田元太+松倉海斗",
                        "--out", str(EYECATCH)], check=True)
    if "eyecatch" not in state:
        state["eyecatch"] = upload_media(EYECATCH, TITLE, TITLE)
        STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    body = {"title": TITLE, "slug": SLUG, "content": html, "status": "draft",
            "categories": [3], "author": 2, "featured_media": state["eyecatch"]["id"]}
    if "post_id" in state:
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{state['post_id']}", headers=HJSON, json=body)
    else:
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=HJSON, json=body)
    r.raise_for_status()
    post = r.json()
    state["post_id"] = post["id"]
    STATE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    print("post", post["id"], post["status"], post["link"], "chars", len(html))


if __name__ == "__main__":
    main()
