# -*- coding: utf-8 -*-
"""Upload the KEY TO LIT Sasaki Taiko "THE神業チャレンジ" (2026-10-20) article to chomoand-5.site as a draft.

usage: python tools/_upload_ktl_kamiwaza_1020.py <img_dir> <eyecatch.jpg>
img_dir must contain jr.jpg (jr_official_X photo) and thumb.jpg (official SNS video thumbnail).
"""
import sys, os, re, json, base64, urllib.request, urllib.error

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
from _ktl_items_lib import p, mark, h2, h3, learn, info, checks, table, build, _html  # noqa: E402

# Sasaki Taiko's member color (blue), same values as THEMES in _upload_ktl_items_1018.py
THEME = dict(acc="#3a78c9", light="#eef4fc", border="#c5d9f2", cell="#dce9f8", mark="#cddff6")


def apply_theme(html):
    t = THEME
    html = (html.replace("#3d5a80", t["acc"]).replace("#eef3f8", t["light"])
                .replace("#c9d6e6", t["border"]).replace("#e3ebf4", t["cell"]))
    return html.replace('<span class="swl-marker mark_yellow" style="font-size:1.1em;">',
                        f'<span style="font-size:1.1em;background:linear-gradient(transparent 60%,{t["mark"]} 60%);">')

env = {}
for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
BASE = env["WP_CHOMO5_URL"].rstrip("/")
AUTH = base64.b64encode(f"{env['WP_CHOMO5_USERNAME']}:{env['WP_CHOMO5_APP_PASSWORD']}".encode()).decode()
AUTHOR = 1  # hostname Tomoki-GEEKOM -> anco

TITLE = "佐々木大光の神業チャレンジ太鼓の達人の結果は？曲は青のすみか！"
SLUG = "sasaki-taiko-kamiwaza-taiko-no-tatsujin"
CATS = [4, 10]
TVER = "https://tver.jp/episodes/epopy9ad0i"
SRC_JR = "https://x.com/jr_official_X/status/2112453805149499621"
SRC_VID = "https://x.com/saigenkamiwaza/status/2112476418806264024"


def req(path, data=None, headers=None, method="POST"):
    r = urllib.request.Request(BASE + path, data=data, method=method)
    r.add_header("Authorization", "Basic " + AUTH)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode('utf-8', 'ignore')[:500]}")


def jpost(path, obj):
    return req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"})


def upload(path, fn, alt):
    m = req("/wp-json/wp/v2/media", open(path, "rb").read(),
            {"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{fn}"'})
    jpost(f"/wp-json/wp/v2/media/{m['id']}", {"alt_text": alt})
    return m


def figure(m, alt, cap):
    sz = m.get("media_details", {}).get("sizes", {})
    full = m["source_url"]
    fw, fh = m["media_details"].get("width"), m["media_details"].get("height")
    lg = sz.get("large") or {"source_url": full, "width": fw, "height": fh}
    srcset = [f"{sz[k]['source_url']} {sz[k]['width']}w" for k in ("medium", "large") if k in sz]
    srcset.append(f"{full} {fw}w")
    return ("<!-- wp:html -->\n<figure class=\"wp-block-image size-large\">\n"
            f"<img src=\"{lg['source_url']}\" alt=\"{alt}\" width=\"{lg['width']}\" height=\"{lg['height']}\"\n"
            "  style=\"max-width:100%;height:auto;\"\n"
            f"  srcset=\"{', '.join(srcset)}\"\n  sizes=\"(max-width: 1024px) 100vw, 1024px\">\n"
            f"<figcaption style=\"font-size:0.8em;color:#888;\">出典:{cap}</figcaption>\n</figure>\n<!-- /wp:html -->")


def related(items):
    lis = "\n".join(f'<li><a href="{BASE}/?p={pid}">{t}</a></li>' for pid, t in items)
    return _html(
        '<div style="border:1px solid #c9d6e6;border-left:4px solid #3d5a80;border-radius:4px;margin:0 0 16px 0;'
        'padding:14px 18px;background:#eef3f8;">\n'
        '<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">あわせて読みたい</p>\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>')


def blocks():
    return [
        p("KEY TO LIT(キテレツ)の佐々木大光が、10月20日(火)放送のTBS『THE神業チャレンジ』2時間スペシャルで「画面隠し太鼓の達人」に挑戦しました。",
          f"結果は、{mark('課題曲『青のすみか』で見事フルコンボを達成し、チャレンジ成功')}です。",
          "放送中からXでは「大光くん」がトレンド入りし、番組の公式アカウントも「Xトレンド1位」を報告するほどの盛り上がりになりました。",
          "この記事では、挑戦の結果や課題曲、練習の裏側、年末の大会、賞金の使い道まで、放送後にXで多かった疑問に順番に答えていきます。"),
        learn(["神業チャレンジの結果", "画面隠し太鼓の達人のルールと課題曲", "練習期間と練習の様子",
               "年末の最強王者決定戦への出場", "賞金の使い道", "見逃し配信の見方"]),
        info([("番組", "THE神業チャレンジ 2時間スペシャル(TBS系)"),
               ("放送", "2026年10月20日(火)よる7時〜8時55分"),
               ("企画", "画面隠し太鼓の達人"),
               ("挑戦者", "佐々木大光(KEY TO LIT)"),
               ("ほかの出演", "河合郁人(ゲスト)、篠塚大輝(timelesz・神業クレーンゲーム)、向井康二(Snow Man・神業テニス)"),
               ("見逃し配信", f'<a href="{TVER}" target="_blank" rel="noopener">TVer</a>')]),
        figure(M["jr"], "THE神業チャレンジのパネル前でピースする佐々木大光", SRC_JR),

        h2("佐々木大光の神業チャレンジの結果は？"),
        info([("結果", "フルコンボ達成でチャレンジ成功"), ("ご褒美", "賞金+年末の最強王者決定戦への出場")]),
        p(f"佐々木大光の画面隠し太鼓の達人は、{mark('最後までミスなく叩き切るフルコンボで成功')}しました。",
          "番組の告知では「KEY TO LITが誇る最強ドラマー・佐々木大光が緊急参戦」と紹介されていて、目標は年末の最強王者決定戦に出るためのフルコンボでした。",
          "その目標を、本番できっちり達成した形です。"),
        p("ただ、すんなり成功したわけではありませんでした。",
          "Xでは、1回目のチャレンジは最初の1打目でつまずいてしまい、見ている側も一気に緊張したという声が多く見られます。",
          "そこから気持ちを立て直し、後がない場面でリズムをつかんで最後まで叩き切ったことに「やるときはやる」「最後の一手で決めるのがさすが」と感動する投稿が相次ぎました。"),
        p("成功した瞬間、張りつめていた表情がふっとほどけ、目をきらきらさせながら「緊張した」と話す姿も映っていました。",
          "ナレーションがさりげなく「大光様」と呼んでいたことも、ファンの間でちょっとした話題になっています。"),

        h2("画面隠し太鼓の達人とは？課題曲は何？"),
        info([("企画", "画面の一部を隠した状態で太鼓の達人をプレイ"), ("課題曲", "青のすみか(King Gnu)")]),
        p("「画面隠し太鼓の達人」は、太鼓の達人の画面の一部を隠した状態でプレイし、流れてくる音符を最後まで見られないまま叩き切る企画です。",
          "普通にプレイするよりも、曲のリズムや譜面を体で覚えておく力が求められます。",
          "番組ではこれまでも太鼓の達人の上級者や芸能人が挑戦してきた人気企画で、年末には1年の王者を決める大会も開かれています。"),
        p(f"佐々木大光の課題曲は、{mark('King Gnuの『青のすみか』')}でした。",
          "TVアニメ『呪術廻戦』懐玉・玉折のオープニングテーマとして大ヒットした曲で、テンポが速く、細かい連打が続くのが特徴です。",
          "Xでも「青のすみかはテンポが速くて大変そう」と心配する声と、「好きな曲だから余計にうれしい」という声の両方が上がっていました。"),
        h3("最強ドラマーでも「ドラムと太鼓の達人は別物」"),
        p("佐々木大光はKEY TO LITのライブでドラムを担当していて、グループの中でも「最強ドラマー」と呼ばれる存在です。",
          "それでも、ドラムと太鼓の達人では叩き方も譜面の読み方もまったく違います。",
          "ファンの間でも「ドラムと太鼓の達人は別物」という見方が多く、太鼓の達人はほぼ未経験の状態からのスタートだったと受け止められています。",
          "スタジオでは河合郁人が温かいコメントを送り、後輩の挑戦を見守っていました。"),

        h2("練習期間はどのくらい？"),
        info([("練習期間", "Xでは約10日間という声"), ("練習の時間帯", "仕事の合間や夜中から朝4時ごろまで")]),
        p("番組では、佐々木大光が本番までに練習を重ねる様子もたっぷり紹介されました。",
          f"Xでの感想をまとめると、練習期間は{mark('およそ10日間')}で、ツアーやロケ、『ぽかぽか』出演などの合間をぬって練習していたようです。",
          "夜中から朝4時ごろまで練習していた場面もあり、デビュー前後の忙しい時期にここまで時間を作ったことに驚く人が多く見られました。"),
        p("練習中のTシャツが中村嶺亜と色違いだったことに気づいたファンもいます。",
          "練習する佐々木大光の後ろで、中村嶺亜がフェイスパックをしている姿が映り込んでいたのも、キテレツらしい和やかなひとコマでした。",
          "ガチャピンと一緒にぴょんぴょん跳ねて遊んだあとに、また練習に戻る場面もあったそうです。"),
        figure(M["thumb"], "THE神業チャレンジ10月20日放送の告知映像", SRC_VID),
        h3("「キテレツのために」という挑戦の理由"),
        p("放送前に番組が公開したSNS限定動画では、KEY TO LITのメンバーが見守るなかで、佐々木大光が意気込みを語っていました。",
          "本編でも、今回の挑戦はグループのためだという思いを繰り返し口にしています。"),
        p(f"特に反響が大きかったのが、{mark('「自分の神業チャレンジがきっかけでKEY TO LITを見てくれて、ほかのメンバーを好きになってくれても全然いい」')}という趣旨の言葉です。",
          "少しでもKEY TO LITの名前が広まればいい、全国の人に愛される存在になりたい、という思いも語られました。",
          "個人の仕事をグループに返そうとする姿勢に、放送後は「グループ愛に泣いた」という感想があふれています。"),

        h2("年末の最強王者決定戦には出場する？"),
        info([("結論", "フルコンボ成功で年末の大会への出場が決定")]),
        p("今回のチャレンジは、年末に放送される太鼓の達人の最強王者決定戦(年間大会)への出場をかけたものでした。",
          f"フルコンボに成功したことで、佐々木大光は{mark('年末の大会に出場できることになりました')}。",
          "Xでは「年末も見られるのがうれしい」「年末決戦もがんばって」と、早くも次の舞台を楽しみにする声が並んでいます。"),
        p("番組は2026年の年間王者を決める大会の観覧キッズを募集していて、大会は会場に観客を入れて行われる予定です。",
          "太鼓の達人の上級者たちとどこまで戦えるのか、放送日などの詳しい情報が出たら、このブログでもお知らせします。"),

        h2("賞金の使い道は？ハンバーグ発言が話題に"),
        info([("今回", "「今日はハンバーグを食べに行きたい」"), ("2022年のダンレボ", "賞金100万円の半分はグループの機材に")]),
        p(f"成功のあとに賞金の使い道を聞かれた佐々木大光は、{mark('「これで今日はハンバーグを食べに行きたいと思います」')}と答えました。",
          "かっこよくフルコンボを決めた直後の、食いしん坊らしいかわいい答えに、Xには「おいしいハンバーグたくさん食べてね」という祝福があふれました。",
          "大食いが得意で、過去にはバラエティの大食い企画にも出ているだけに、どれだけ食べたのか気になるところです。"),
        h3("神業チャレンジは2回目の成功"),
        p("実は佐々木大光が神業チャレンジで成功するのは、今回が初めてではありません。",
          f"7 MEN 侍のメンバーだった2022年6月の放送では、{mark('「神業ダンスダンスレボリューション」で成功し、賞金100万円を獲得')}しています。",
          "このときは「ジャニーズJr.No.1ダンサー」として紹介され、ダンスの実力を全国に見せました。"),
        p("当時の賞金は、半分をグループの音楽のための機材に使い、管理は矢花黎に任せると話していたことがファンの間で知られています。",
          "残りの半分は自分へのご褒美に使うと話していて、その使い方にも好感が集まりました。",
          "ダンスと太鼓の達人、ジャンルの違う神業を2回とも成功させたことになります。"),
        table(["放送", "企画", "結果"],
              [["2022年6月", "神業ダンスダンスレボリューション(7 MEN 侍として)", "成功・賞金100万円"],
               ["2026年10月20日", "画面隠し太鼓の達人(KEY TO LITとして)", "フルコンボ成功・年末の大会へ"]]),

        h2("放送で流れたKEY TO LITの映像"),
        p("今回の放送では、佐々木大光の紹介VTRにKEY TO LITの映像が数多く使われました。",
          "ライブでドラムを叩く姿や増上寺でのパフォーマンス、大食い企画の映像、さらにフジテレビ『ぽかぽか』で緑の全身タイツ姿になった場面まで登場しています。",
          "他局の番組の映像まで入れてくれたことに、驚きと感謝の声が上がっていました。"),
        p("デビュー発表のときの映像や、メンバーからの応援コメントも流れました。",
          "Tシャツ姿で応援する岩﨑大昇の姿もあり、メンバーみんなで佐々木大光の挑戦を支えていたことが伝わる構成でした。",
          "家族で見ていたら家族も佐々木大光を覚えた、という投稿もあり、グループを知ってもらうきっかけになった放送と言えそうです。"),

        h2("見逃し配信はどこで見られる？"),
        p(f'見逃した人は、<a href="{TVER}" target="_blank" rel="noopener">TVer</a>で配信されている今回の放送回から見ることができます。',
          "佐々木大光のチャレンジは、番組の後半(配信の1時間21分ごろから)に出てきます。",
          "配信期間には限りがあるので、気になる人は早めにチェックしておくのがおすすめです。"),
        p("ファンの間では、TVerでのお気に入り登録や、番組への感想の投稿で応援しようという動きも広がっています。",
          "年末の大会に向けて、番組をもう一度見て応援しておくのも楽しみ方のひとつです。"),

        h2("まとめ"),
        checks(["佐々木大光は10月20日の『THE神業チャレンジ』で画面隠し太鼓の達人に挑戦",
                "課題曲はKing Gnuの『青のすみか』",
                "1回目は1打目でつまずくも、本番でフルコンボを達成して成功",
                "約10日間、仕事の合間や夜中に練習を重ねた",
                "成功で年末の最強王者決定戦への出場が決定",
                "賞金の使い道は「今日はハンバーグを食べに行きたい」",
                "2022年のダンレボに続き、神業チャレンジは2回目の成功"]),
        p("忙しい時期に練習を重ね、プレッシャーのなかで結果を出した佐々木大光の姿は、キテレツを知らない人にもしっかり届いたはずです。",
          "年末の最強王者決定戦でどんな神業を見せてくれるのか、今から放送が待ち遠しいですね！"),
        related([(30, "キテレツのテレビ出演は？10/18〜10/24の放送予定まとめ！"),
                 (34, "キテレツの結成はいつ？前のグループやファンネーム、メンカラも！"),
                 (175, "佐々木大光の愛用香水は？シャネルのココ マドモアゼル！"),
                 (193, "【キテレツキテル】武勇伝メンチ対決の中身は？一番の漢はガリネム！")]),
    ]


M = {}


def main():
    img_dir, eye = sys.argv[1], sys.argv[2]
    assert len(TITLE) <= 35, len(TITLE)
    M["jr"] = upload(os.path.join(img_dir, "jr.jpg"), "ktl_sasaki_kamiwaza_01.jpg", "THE神業チャレンジのパネル前の佐々木大光")
    M["thumb"] = upload(os.path.join(img_dir, "thumb.jpg"), "ktl_sasaki_kamiwaza_02.jpg", "THE神業チャレンジ10月20日放送の告知映像")
    html = apply_theme(build(blocks()))
    html = re.sub(r"<hr\s*/?>", "", html)
    text = re.sub(r"<[^>]+>", "", html)
    print("chars", len(re.sub(r"\s", "", text)))
    em = upload(eye, "ktl_sasaki_kamiwaza_eyecatch.jpg", TITLE)
    post = jpost("/wp-json/wp/v2/posts", {"title": TITLE, "content": html, "slug": SLUG, "status": "draft",
                                         "categories": CATS, "author": AUTHOR, "featured_media": em["id"]})
    print("post", post["id"], post["status"], "eyecatch", em["id"], f"{BASE}/?p={post['id']}")


if __name__ == "__main__":
    main()
