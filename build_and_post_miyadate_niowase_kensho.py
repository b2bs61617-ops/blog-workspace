# -*- coding: utf-8 -*-
"""宮舘涼太の彼女の匂わせ説を検証 -> chomoand-2.com 下書き投稿(【未】付き).

方針(2026-11-06 オシリ依頼・マツ判断):
- お相手とされる女性の名前・アカウント・出演番組名は書かない(特定・攻撃を招かないため)
- ファン・第三者のX投稿は埋め込まない(feedback: 他人の投稿は使わない)
- 「匂わせ」はファンの推測であり、交際の証拠ではないと明記する
出典: coki(2026/8/22)、東スポWEB(2026/5/5)、日刊ゲンダイ、Netflix公式X(10/14)、X上のファン投稿(10月、要旨のみ)
usage: python build_and_post_miyadate_niowase_kensho.py build|post
"""
import base64, os, sys
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
ACCENT = "#c62828"   # 宮舘涼太メンバーカラー(赤)寄り
ACCENT_BG = "#fdf3f3"
AUTHOR = 2  # momo(USER1 / オシリ)
BASE = "miyadate_niowase_kensho"
HTML_PATH = ROOT / "articles" / f"{BASE}.html"
EYECATCH_PATH = ROOT / "images" / f"{BASE}_eyecatch.jpg"

title = "【未】宮舘涼太の彼女が匂わせ？バッグ・リボン・サウナの噂を検証！"
slug = "miyadate-ryota-girlfriend-niowase"


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
        "<tr>" + "".join(f'<td style="border:1px solid #ccc;padding:8px 12px;">{c}</td>' for c in r) + "</tr>"
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


def x_embed(user, sid):
    tw = f"https://twitter.com/{user}/status/{sid}"
    return wphtml('<blockquote class="twitter-tweet" data-lang="ja" data-dnt="true">'
                  f'<a href="{tw}">{tw}</a></blockquote>\n'
                  '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def build():
    B = []
    B.append(p([
        "ここ最近、Xで「宮舘涼太さんの彼女が匂わせしている」という投稿をよく見かけます。",
        "バッグがおそろい、リボンがかぶった、サウナの写真のタイミングが同じ…など、いろいろな説が出回っていますよね。",
        "この記事では、話題になった匂わせ説を時系列でまとめ、それぞれに本当に根拠があるのかを検証しました。",
    ]))
    B.append(p([
        "先に結論をお伝えすると、宮舘涼太さんの交際は本人も事務所も認めておらず、匂わせとされるものもすべてファンの推測です。",
        "交際を裏付ける決定的な材料は、2026年11月6日時点で見つかっていません。",
    ]))
    B.append(box("この記事でわかること", [
        "宮舘涼太の匂わせ説が出たきっかけ(2026年2月の交際報道)",
        "事務所・本人の対応",
        "8月のバッグ、10月のリボン・サウナなど匂わせ説の中身",
        "匂わせ説を検証した結果と、ファンの受け止め方",
    ]))

    B.append(h2("宮舘涼太に彼女はいる？匂わせ説が出たきっかけ"))
    B.append(p([
        "匂わせ説の出発点は、2026年2月25日に「女性セブンプラス」が報じた交際報道です。",
        "お相手は、テレビ局に勤める20代の女性アナウンサーと報じられました。",
        "記事では、2人がバラエティ番組での共演をきっかけに知り合い、港区の会員制バーで再会して関係を深めたとされています。",
        "宮舘さんの自宅を訪れる様子を撮った写真も掲載され、ファンの間に大きな衝撃が走りました。",
    ]))
    B.append(p([
        "この記事では、お相手とされる女性の名前やSNSアカウントは書きません。",
        "交際は確定しておらず、名前を広めることでSNS上の攻撃につながるおそれがあるためです。",
    ]))
    B.append(h3("事務所のコメントは「友人の一人」"))
    B.append(p([
        "報道に対し、宮舘さんの所属するSTARTO ENTERTAINMENTは「友人の一人です」とコメントしました。",
        "お相手側のテレビ局も「社員のプライベートについてはお答えしていない」という対応で、どちらも交際を認めても否定してもいません。",
    ]))
    B.append(h3("宮舘涼太本人はファンクラブ向けブログで謝罪"))
    B.append(p([
        "報道から少しあとの2026年3月中旬、宮舘さんはファンクラブ向けのブログで、ファンを不安にさせたことを謝罪したと報じられています。",
        "ただ、ブログでは「様々な憶測が飛び交う世の中」といった表現にとどめ、交際しているかどうかには触れませんでした。",
        "はっきり否定しなかったことで、「やっぱり付き合っているのでは」と受け取ったファンも多く、これが後の匂わせ探しにつながっています。",
    ]))
    B.append(h3("その後の報道は？"))
    B.append(p([
        "2026年5月には東スポWEBが、報道後は2人がそのバーで見かけられなくなったと伝えました。",
        "一方で、交際が続いているのか、破局したのかについては、どのメディアもはっきりした情報を出していません。",
        "つまり今の時点で言えるのは「交際報道は出たが、本人たちは何も認めていない」ということだけです。",
    ]))

    B.append(h2("宮舘涼太の彼女の匂わせとされるものまとめ"))
    B.append(p([
        "交際報道のあと、Xでは「匂わせでは？」とされる出来事が何度か話題になりました。",
        "主なものを時系列で表にまとめます。",
    ]))
    B.append(table([
        ("2026年8月21日ごろ", "デニム素材のキルティングバッグ", "宮舘さんが2025年10月ごろに私服投稿で持っていたシャネルのバッグに似ている"),
        ("2026年10月11日", "白い大きなリボン", "同じ日の宮舘さん出演番組でも白いボウタイのブラウスを着ていた"),
        ("2026年10月14日〜17日", "サウナの写真", "宮舘さん出演ドラマのサウナ場面の解禁から3日後に、お相手側もサウナ写真を出した"),
        ("2026年10月中旬", "高級ブランドの話題", "番組で宮舘さんの「ハイブランドに高級バッグ」の私服が話題になり、バッグの件が再び注目された"),
    ], head=["時期", "アイテム", "匂わせとされた理由"]))

    B.append(h3("匂わせ1:シャネル風のデニムバッグ(8月)"))
    B.append(p([
        "いちばん大きく話題になったのが、2026年8月のバッグの件です。",
        "8月21日ごろ、お相手とされる女性のインスタグラムのストーリーに、水色のデニム素材のキルティングバッグが写っていたとされています。",
        "このバッグが、宮舘さんが2025年10月ごろにインスタグラムの私服投稿で持っていたシャネルのデニムバッグに似ているとして、比較画像がXで広まりました。",
    ]))
    B.append(p([
        "ストーリーは24時間で消える機能のため、元の投稿は今は見られず、スクリーンショットだけが出回っている状態です。",
        "同じバッグかどうか、ブランドや型番まで一致しているかは確認できていません。",
        "シャネルのキルティングバッグは人気の定番デザインで、デニム素材のものも毎年のように出ているため、持っている人が重なること自体は珍しくありません。",
    ]))
    B.append(h3("匂わせ2:白い大きなリボン(10月11日)"))
    B.append(p([
        "10月11日には、お相手とされる女性が出演した番組で、白い大きなリボンが付いたブラウスを着ていたことが話題になりました。",
        "同じ日に放送された宮舘さん出演の番組『限界インストール』で、宮舘さんも黒いベロアのジャケットに白い大きなボウタイのブラウスを合わせていたため、「リボン合わせでは？」という声が出ました。",
    ]))
    B.append(p([
        "ただ、この説はファンの間でも「さすがに偶然では」という見方が多めです。",
        "どちらもテレビ番組の衣装で、スタイリストが用意したものと考えるのが自然です。",
        "白い大きなリボンは今季のトレンドで、宮舘さんのファンにもリボンを取り入れる人が多いことから、「リボン合わせはむしろファンのほう」という声もありました。",
        "Xでも、自分から「#なんでもこじつけるオタク」というハッシュタグを付けて紹介するファンがいたほどで、半分ネタとして扱われている印象です。",
    ]))
    B.append(h3("匂わせ3:サウナの写真(10月14日〜17日)"))
    B.append(p([
        "10月14日、Netflixシリーズ『俺のこと、なんか言ってた？』の公式Xが、宮舘さんの出演決定とサウナの場面写真を公開しました。",
        "同作は10月22日から世界独占配信されています。",
    ]))
    B.append(p([
        "その3日後の10月17日、お相手とされる女性が担当番組の宣伝でサウナの写真を出したことから、「サウナつながりの匂わせでは」と言われました。",
        "しかし、こちらは番組の宣伝として出された写真で、内容も番組側の企画によるものです。",
        "本人が自由に選んで投稿したものとは言いにくく、匂わせと考えるには無理がある説といえます。",
        "投稿した人自身も「#すぐに匂わせこじつけるオタク」とタグを付けており、本気の告発というより「つい結びつけてしまう」というファン心理の表れでしょう。",
    ]))
    B.append(h3("番組で私服が「クズっぽい」と言われバッグの件が再燃(10月中旬)"))
    B.append(p([
        "10月16日放送のTBS系『それSnow Manにやらせて下さいSP』では、ドラマで共演した俳優の竹財輝之助さんが、撮影現場での宮舘さんの私服を「ちょっとクズっぽかった」と冗談まじりに明かしました。",
        "竹財さんによると、宮舘さんはいつもハイブランドを身につけ、サングラスに高級バッグという姿だったそうです。",
        "宮舘さんは「それキャラじゃなくて、リアルにやってます」と返し、スタジオの笑いを誘いました。",
    ]))
    B.append(p([
        "この放送をきっかけに、宮舘さんのシャネルのバッグが改めて注目され、8月のバッグの件をまとめ直す投稿がXで再び出回りました。",
        "新しい匂わせが見つかったわけではなく、過去の話題がもう一度広まった形です。",
    ]))

    B.append(h2("宮舘涼太の彼女の匂わせ説を検証した結果"))
    B.append(p([
        "ここまでの匂わせ説を、根拠の強さで整理しました。",
    ]))
    B.append(table([
        ("デニムバッグ(8月)", "△", "似ているのは事実だが、同じ商品かは不明。人気の定番デザイン"),
        ("白いリボン(10月11日)", "×", "どちらも番組衣装で、今季のトレンドアイテム"),
        ("サウナの写真(10月17日)", "×", "番組宣伝の写真で、本人が選んだ投稿ではない"),
        ("私服の話題(10月中旬)", "-", "新しい材料ではなく、8月の件が再び広まっただけ"),
    ], head=["匂わせ説", "根拠の強さ", "理由"]))
    B.append(p([
        "どの説も「同じようなものが写っていた」というレベルで、交際を証明するものはひとつもありませんでした。",
        "そもそも匂わせかどうかは、投稿した本人にしか分かりません。",
        "流行のアイテムや仕事での写真まで匂わせとして扱われてしまうのは、交際報道が出た相手だからこそ、どんな投稿にも意味を探してしまうファン心理が大きいといえます。",
    ]))
    B.append(h3("ファンの受け止め方は大きく分けて3つ"))
    B.append(box("Xで見られた主な反応", [
        "匂わせに見えて不快、やめてほしいという声",
        "偶然にすぎない、こじつけだとネタにする声",
        "交際していてもいいから、宮舘さん本人の仕事を応援したいという声",
    ]))
    B.append(p([
        "ドラマ出演や番組での活躍が続く中で、「役者としての宮舘さんを応援したい」と、噂とは距離をおくファンも目立ちます。",
        "一方で、お相手とされる女性を強い言葉で非難する投稿も一部で見られます。",
        "確定していない噂をもとに、特定の人を攻撃するのは控えたいところです。",
    ]))

    B.append(h2("まとめ"))
    B.append(box("この記事のまとめ", [
        "宮舘涼太の交際は2026年2月に報じられたが、事務所は「友人の一人」とし、本人も認めていない",
        "8月のデニムバッグは似ているものの、同じ商品かは確認できていない",
        "10月のリボン・サウナは、トレンドや番組宣伝によるもので匂わせの根拠としては弱い",
        "2026年11月6日時点で、交際を裏付ける決定的な情報はない",
    ]))
    B.append(p([
        "宮舘涼太さんの彼女の匂わせ説は、どれも推測の域を出ないものでした。",
        "新しい報道や本人のコメントが出た場合は、この記事に追記していきます。",
        "今後の宮舘さんの活躍も楽しみですね！",
    ]))
    return "\n\n".join(b for b in B if b)


def post():
    url = ENV["WP_CHOMO2_URL"].rstrip("/")
    auth = base64.b64encode(f"{ENV['WP_CHOMO2_USERNAME']}:{ENV['WP_CHOMO2_APP_PASSWORD']}".encode()).decode()
    h = {"Authorization": f"Basic {auth}"}
    content = HTML_PATH.read_text(encoding="utf-8")
    media_id = None
    if EYECATCH_PATH.exists():
        r = requests.post(f"{url}/wp-json/wp/v2/media", headers={**h, "Content-Type": "image/jpeg",
                          "Content-Disposition": f'attachment; filename="{EYECATCH_PATH.name}"'},
                          data=EYECATCH_PATH.read_bytes(), timeout=60)
        r.raise_for_status()
        media_id = r.json()["id"]
    payload = {"title": title, "slug": slug, "content": content, "status": "draft",
               "categories": [4, 13], "author": AUTHOR}
    if media_id:
        payload["featured_media"] = media_id
    r = requests.post(f"{url}/wp-json/wp/v2/posts", headers={**h, "Content-Type": "application/json"},
                      json=payload, timeout=60)
    r.raise_for_status()
    d = r.json()
    print("POST_ID", d["id"], "STATUS", d["status"], "MEDIA", media_id, "LINK", f"{url}/?p={d['id']}")


if __name__ == "__main__":
    if sys.argv[1] == "build":
        HTML_PATH.parent.mkdir(exist_ok=True)
        HTML_PATH.write_text(build(), encoding="utf-8")
        print("wrote", HTML_PATH, len(HTML_PATH.read_text(encoding="utf-8")))
    else:
        post()
