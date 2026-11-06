# -*- coding: utf-8 -*-
"""旧ジャニーズ(STARTO系)身長ランキング42人 -> chomoand.com(トレンドブログ) 下書き投稿.

使い方: python build_and_post_starto_height_ranking.py [--dry]

2026-11-06 オシリ依頼。きっかけはXで話題の「旧ジャニーズ42人の身長比較表」画像(第三者作成)。
画像・投稿は記事に使わず、数値は独自に裏取りした([[feedback-no-third-party-identification-posts]])。
画像の誤り: 「大倉和也168cm」(正しくは大倉忠義・178cm前後)、「山田流介」(山田涼介)、ラウール190cm(192cm報道あり)。
主な出典:
- ラウール: 日刊スポーツ 2023-04-14「中居正広、Snow Manラウールに『ダルビッシュ!?』192センチの長身に驚く」
- 目黒蓮: アイランドTVで本人が184.7cmと回答(ciatr)
- 岩本照: 179cm→182cmに更新(ciatr)、深澤辰哉: 2020年公式カレンダー175cm(ciatr)
- アンケート: All About ニュース 2026-06-28/30(10〜60代300人、6/11実施)
- 大倉忠義178cm: crank-in / ranking.net
"""
import json, base64, os, re, subprocess, sys
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
AUTHOR = 3  # momo(オシリと作った記事は著者momo)
CATEGORY = 37  # 芸能・トレンド

ACCENT = "#6a1b9a"
ACCENT_BG = "#f6f0fa"

TITLE = "旧ジャニーズ身長ランキング42人！1位ラウールは何cm？意外な高身長は？"
SLUG = "starto-height-ranking"

# (名前, グループ, 身長cm)  ※身長は公表値・本人発言・主要プロフィールで多い数値
DATA = [
    ("ラウール", "Snow Man", 192),
    ("目黒蓮", "Snow Man", 185),
    ("ジェシー", "SixTONES", 184),
    ("長瀬智也", "元TOKIO", 182),
    ("岩本照", "Snow Man", 182),
    ("道枝駿佑", "なにわ男子", 180),
    ("大倉忠義", "SUPER EIGHT", 178),
    ("東山紀之", "元少年隊", 178),
    ("菊池風磨", "timelesz", 178),
    ("小山慶一郎", "NEWS", 178),
    ("阿部亮平", "Snow Man", 178),
    ("松村北斗", "SixTONES", 177),
    ("玉森裕太", "Kis-My-Ft2", 177),
    ("木村拓哉", "元SMAP", 176),
    ("相葉雅紀", "嵐", 176),
    ("中島健人", "ソロ(元Sexy Zone)", 176),
    ("高橋恭平", "なにわ男子", 176),
    ("向井康二", "Snow Man", 175.5),
    ("永瀬廉", "King & Prince", 175),
    ("神宮寺勇太", "Number_i", 175),
    ("深澤辰哉", "Snow Man", 175),
    ("加藤シゲアキ", "NEWS", 175),
    ("宮舘涼太", "Snow Man", 174),
    ("高橋海人", "King & Prince", 174),
    ("松本潤", "嵐", 173),
    ("渡辺翔太", "Snow Man", 172),
    ("櫻井翔", "嵐", 171),
    ("佐藤勝利", "timelesz", 171),
    ("平野紫耀", "Number_i", 171),
    ("増田貴久", "NEWS", 171),
    ("二宮和也", "嵐", 168),
    ("堂本光一", "DOMOTO", 168),
    ("藤原丈一郎", "なにわ男子", 168),
    ("岸優太", "Number_i", 167),
    ("松島聡", "timelesz", 167),
    ("西畑大吾", "なにわ男子", 167),
    ("大野智", "嵐", 166),
    ("堂本剛", "DOMOTO", 166),
    ("大西流星", "なにわ男子", 166),
    ("山田涼介", "Hey! Say! JUMP", 164),
    ("有岡大貴", "Hey! Say! JUMP", 164),
    ("知念侑李", "Hey! Say! JUMP", 159),
]
assert len(DATA) == 42


def fmt(h):
    return f"{h:g}cm"


def p(sentences):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(sentences) + "</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def table(rows, head):
    th = "<thead><tr>" + "".join(
        f'<th style="border:1px solid #ccc;padding:8px 12px;background:{ACCENT};color:#fff;">{h}</th>' for h in head
    ) + "</tr></thead>\n"
    trs = "\n".join(
        "<tr>" + "".join(f'<td style="border:1px solid #ccc;padding:6px 10px;">{c}</td>' for c in r) + "</tr>"
        for r in rows
    )
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout">'
            f"{th}<tbody>\n{trs}\n</tbody></table></figure>\n<!-- /wp:table -->")


def box(ttl, items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(
        f'<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">{ttl}</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{ACCENT_BG};">\n{lis}\n</ul>\n</div>'
    )


def quote(text, cite):
    return ('<!-- wp:quote -->\n<blockquote class="wp-block-quote"><!-- wp:paragraph -->\n'
            f"<p>{text}</p>\n<!-- /wp:paragraph --><cite>{cite}</cite></blockquote>\n<!-- /wp:quote -->")


def marker(t):
    return f'<span class="swl-marker mark_yellow">{t}</span>'


def build():
    hs = [h for _, _, h in DATA]
    avg = sum(hs) / len(hs)
    tall = sum(1 for h in hs if h >= 180)
    B = []

    B.append(p([
        "SNSで「旧ジャニーズの身長比較」が話題になっています。",
        "結論から言うと、人気の旧ジャニーズ(STARTO ENTERTAINMENT所属・出身)タレント42人で一番背が高いのは、"
        + marker("Snow Manのラウールさんで192cm") + "です。",
        f"2位は目黒蓮さんの185cm、3位はジェシーさんの184cmで、42人の平均は約{avg:.1f}cmでした。",
        "ただ、出回っている比較画像には名前や身長が間違っているところもありました。",
        "この記事では、報道・本人の発言・プロフィールの数値をもとに、42人の身長を一つずつ確かめてランキングにしました。",
    ]))

    B.append(box("この記事でわかること", [
        "旧ジャニーズ42人の身長ランキング一覧",
        "1位ラウールの身長は190cm？192cm？",
        "身長を知って驚かれた木村拓哉・堂本光一",
        "比較表で168cmとされていた大倉忠義の本当の身長",
        "一番小柄な知念侑李は何cm？",
    ]))

    # ---------------- ranking
    B.append(h2("旧ジャニーズ身長ランキング42人一覧【2026年最新】"))
    B.append(p([
        "まずは42人の一覧です。",
        "42人は、知名度や人気、グループ・世代のバランスで選ばれたメンバーです。",
        "同じ身長の人は同じ順位にしています。",
    ]))
    rows = []
    rank = 0
    prev = None
    for i, (name, grp, h) in enumerate(DATA, 1):
        if h != prev:
            rank = i
            prev = h
        rows.append([f"{rank}位", name, grp, fmt(h)])
    B.append(table(rows, ["順位", "名前", "グループ", "身長"]))
    B.append(p([
        f"一番高いラウールさん(192cm)と一番小柄な知念侑李さん(159cm)の差は、なんと{192 - 159}cmです。",
        f"180cm以上は{tall}人で、そのうち3人がSnow Manのメンバーでした。",
        "なお、STARTO ENTERTAINMENTの公式サイトには身長が載っていません。",
        "ここでの数値は、報道や本人の発言、雑誌・プロフィールで多く使われている数値です。",
        "媒体によって1〜2cmの差があることもあるので、目安として見てくださいね。",
    ]))

    # ---------------- Raul
    B.append(h2("1位はラウール！身長は190cm？192cm？"))
    B.append(h3("2023年の報道では「192センチ」"))
    B.append(p([
        "比較画像やアンケート記事では「190cm」と書かれることが多いラウールさんですが、実はもう少し高いようです。",
        "2023年4月14日の日刊スポーツは、中居正広さんがラウールさんの長身に驚いた場面を伝えていて、見出しは「192センチの長身に驚く」でした。",
        "中居さんは、ラウールさんの大きさに思わず「ダルビッシュ!?」とプロ野球選手の名前を出していたそうです。",
        "ネットでも192cmと紹介しているサイトが多く、" + marker("190cmは少し控えめな数字") + "と言えそうです。",
    ]))
    B.append(h3("加入当時は176cmだった"))
    B.append(p([
        "ラウールさんは、2019年にSnow Manに加入したころは176cmくらいだったと紹介されています。",
        "そこから数年で15cm以上伸びたことになり、ファンの間では「会うたびに大きくなる」と話題になっていました。",
        "2022年の『滝沢歌舞伎ZERO 2022』の会見では、「ずっとシークレットブーツでそう見えるだけなんですけど、本当は170cmぐらい」と冗談を言って笑わせていました。",
        "モデルとしても活躍できるのは、この身長があってこそですね。",
    ]))

    # ---------------- top 5
    B.append(h2("2位〜5位は目黒蓮・ジェシー・長瀬智也・岩本照"))
    B.append(h3("目黒蓮は185cm(本人回答は184.7cm)"))
    B.append(p([
        "2位の目黒蓮さんは185cmです。",
        "雑誌などでは185cmと書かれることが多いですが、以前アイランドTVでは本人が「184.7cm」と細かく答えていたと紹介されています。",
        "All Aboutのアンケート(2026年6月・300人)では、「身長を知って驚いた20代男性俳優」の2位にも入っていて、「もっと低いと思っていた」という声がありました。",
        "顔が小さくスタイルが良いので、数字ほど大きく見えないのかもしれません。",
    ]))
    B.append(h3("ジェシーは184cm、SixTONESで一番の長身"))
    B.append(p([
        "3位のジェシーさんは184cmで、SixTONESの中ではダントツの高さです。",
        "2番目に高い松村北斗さん(177cm)とは7cmの差があります。",
        "SixTONESは6人全員が174cm以上という、高身長ぞろいのグループです。",
    ]))
    B.append(h3("長瀬智也・岩本照は182cm"))
    B.append(p([
        "4位タイは、元TOKIOの長瀬智也さんとSnow Manの岩本照さんで、どちらも182cmです。",
        "長瀬さんは183cmと書かれることもありますが、プロフィールでは182cmとしているものが多くなっています。",
        "岩本さんは、2021年ごろは179cmとされていましたが、その後182cmに更新されたと紹介されています。",
        "6位は、なにわ男子の道枝駿佑さんで180cmでした(179cmとする媒体もあります)。",
    ]))

    # ---------------- surprise
    B.append(h2("身長を知って驚かれたのは木村拓哉と堂本光一"))
    B.append(p([
        "All Aboutニュースが2026年6月11日に10〜60代の男女300人に聞いたアンケートでは、イメージと実際の身長の違いが話題になった人がいました。",
    ]))
    B.append(table([
        ["身長を知って驚いた男性アイドル", "1位 木村拓哉(176cm)・2位 ラウール(190cm)"],
        ["もっと身長が高いように感じる男性アイドル", "1位 堂本光一(168cm)・2位 木村拓哉(176cm)"],
    ], ["アンケート", "結果"]))
    B.append(h3("木村拓哉は176cm"))
    B.append(p([
        "木村拓哉さんは176cmで、42人の中では14位タイです。",
        "日本人男性の平均(約172cm)より4cmほど高いのですが、「170cmくらいだと思っていた」「もっと低いと思った」という声が集まって「身長を知って驚いた」の1位になりました。",
        "一方で、「存在感があるから大きく見える」という理由で「もっと高いように感じる」ランキングでも2位に入っていて、見る人によってイメージが分かれる人のようです。",
    ]))
    B.append(h3("中島健人も176cm"))
    B.append(p([
        "同じく176cmなのが、ソロで活動する中島健人さんです。",
        "王子様キャラの印象が強いせいか、「意外と高い」と言われることが多い1人です。",
        "相葉雅紀さん・高橋恭平さんも同じ176cmで、木村さんと4人が並んでいます。",
    ]))
    B.append(h3("堂本光一は168cmでも「大きく見える」"))
    B.append(p([
        "堂本光一さんは168cmで、42人の中では低い方です。",
        "それでも「もっと身長が高いように感じる男性アイドル」では1位で、「堂々とした立ち振る舞いのせいか、もっと背が高いと思っていた」という声がありました。",
        "舞台『Endless SHOCK』で長年座長を務めてきた姿勢の良さが、実際より大きく見せているのかもしれません。",
    ]))

    # ---------------- okura
    B.append(h2("大倉忠義の身長は178cm！比較表の168cmは打ち間違い？"))
    B.append(p([
        "SNSで出回った比較表では、SUPER EIGHTの大倉忠義さんが168cmとされていました。",
        "でも、" + marker("大倉忠義さんの身長は一般的に178cm") + "とされています。",
        "10cmの打ち間違いの可能性があるので、この記事のランキングでは大倉さんを178cmで7位タイに入れています。",
        "画像版では名前も「大倉和也」になっていたり、Hey! Say! JUMPの山田涼介さんが「山田流介」になっていたりと、気になるところがいくつかありました。",
        "ラウールさんも190cmとされていましたが、先ほど紹介したとおり192cmという報道があります。",
        "身長の比較画像はよく出回りますが、名前や数字は一度確かめてから見るのが安心です。",
    ]))

    # ---------------- short
    B.append(h2("一番小柄なのは知念侑李で159cm"))
    B.append(p([
        "42人の中で一番小柄なのは、Hey! Say! JUMPの知念侑李さんで159cmです。",
        "同じグループの山田涼介さん・有岡大貴さんが164cmで続き、下位3人はHey! Say! JUMPのメンバーでした。",
        "知念さんはアクロバットが得意で、小柄な体を生かした身軽なパフォーマンスが魅力です。",
        "なにわ男子は道枝駿佑さん(180cm)と大西流星さん(166cm)で14cmの差があり、グループの中でも身長差が大きくなっています。",
    ]))

    # ---------------- group
    B.append(h2("グループ別に見ると高身長が多いのはSnow Man"))
    groups = {}
    for name, grp, h in DATA:
        groups.setdefault(grp, []).append(h)
    grows = []
    for g in ["Snow Man", "SixTONES", "なにわ男子", "嵐", "NEWS", "timelesz", "Number_i", "Hey! Say! JUMP"]:
        v = groups[g]
        grows.append([g, f"{len(v)}人", f"{sum(v) / len(v):.1f}cm"])
    B.append(table(grows, ["グループ", "ランキング内の人数", "平均身長"]))
    sm = groups["Snow Man"]
    B.append(p([
        f"ランキングに入ったSnow Manの8人は、平均で約{sum(sm) / len(sm):.1f}cmでした。",
        "ラウールさん・目黒蓮さん・岩本照さんの3人が180cmを超えていて、ステージで並ぶと迫力があります。",
        "ちなみに、ランキングに入っていない佐久間大介さんは168cmとされています。",
        "Snow Manは「グループの中では普通に見えるのに、ほかの人と並ぶと大きい」という意味で「身長バグ」と言われることもあります。",
        "SixTONESの2人(ジェシーさん・松村北斗さん)も平均180cmを超えていますが、ここに入っていない4人も174〜175cmとされています。",
    ]))

    # ---------------- matome
    B.append(h2("まとめ"))
    B.append(box("旧ジャニーズ身長ランキングのまとめ", [
        "1位はラウール。比較画像では190cmだが、2023年の報道では192cm",
        "2位は目黒蓮(185cm)、3位はジェシー(184cm)",
        f"42人の平均は約{avg:.1f}cm、180cm以上は{tall}人",
        "木村拓哉(176cm)は「身長を知って驚いた男性アイドル」1位",
        "堂本光一(168cm)は「もっと高く感じる男性アイドル」1位",
        "比較表の「大倉忠義168cm」は178cmの打ち間違いとみられる",
        "一番小柄なのは知念侑李(159cm)",
    ]))
    B.append(p([
        "身長の数字だけでなく、立ち姿やオーラで大きく見える人も多いのが旧ジャニーズのすごいところですね。",
        "本人が新しく身長を話す場面があれば、この記事にも追記していきます。",
    ]))
    return B


def main():
    content = "\n\n".join(build())
    if "--dry" in sys.argv:
        txt = re.sub(r"<[^>]+>", "", content)
        print("chars:", len(re.sub(r"\s", "", txt)), "title len:", len(TITLE))
        (ROOT / "images" / "starto_height_preview.html").write_text(content, encoding="utf-8")
        return

    wp_url = ENV["WP_TREND_URL"].rstrip("/")
    auth = base64.b64encode(f"{ENV['WP_TREND_USERNAME']}:{ENV['WP_TREND_APP_PASSWORD']}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}

    if "--update" in sys.argv:  # 既存下書きの本文だけ上書き
        pid = sys.argv[sys.argv.index("--update") + 1]
        r = requests.post(f"{wp_url}/wp-json/wp/v2/posts/{pid}",
                          headers={**headers, "Content-Type": "application/json"},
                          data=json.dumps({"content": content}).encode("utf-8"))
        r.raise_for_status()
        print("UPDATED", r.json()["id"], r.json()["status"])
        return

    eyecatch = ROOT / "images" / "starto_height_ranking_eyecatch.png"
    if not eyecatch.exists():
        subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_chomoand.py"),
                        "--top", "1位は何cm？", "--main", "旧ジャニーズ身長ランキング",
                        "--bottom", "42人を徹底比較！", "--out", str(eyecatch)], check=True)
    r = requests.post(f"{wp_url}/wp-json/wp/v2/media",
                      headers={**headers, "Content-Type": "image/png",
                               "Content-Disposition": f'attachment; filename="{eyecatch.name}"'},
                      data=eyecatch.read_bytes())
    r.raise_for_status()
    media_id = r.json()["id"]

    payload = {"title": TITLE, "slug": SLUG, "content": content, "status": "draft",
               "categories": [CATEGORY], "author": AUTHOR, "featured_media": media_id}
    r = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers={**headers, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    post = r.json()
    print("POST_ID", post["id"], "STATUS", post["status"], "MEDIA", media_id)


if __name__ == "__main__":
    main()
