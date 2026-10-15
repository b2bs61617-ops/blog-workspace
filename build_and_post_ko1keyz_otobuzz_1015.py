# -*- coding: utf-8 -*-
"""KO1KEYZが「Amazon Music presents オトバズ」#1に出演(2026-10-15発表)。
一次情報:
- KO1KEYZ公式X https://x.com/KO1KEYZofficial/status/2110578899252019619 (10/15 12:49 JST)
- Amazon Music JP公式X https://x.com/amazonmusicjp/status/2110573936148873333 (10/15 12:30 JST、予告動画つき)
- アマゾンジャパンのプレスリリース https://www.zaikei.co.jp/releases/3664642/ (10/15)
  全6エピソード、10/22(木)からPrime Videoで独占配信。Prime会員でなくてもAmazonアカウントがあれば視聴可。
  MC=チョコレートプラネット(長田庄平・松尾駿)・北山宏光。#1ゲスト=KO1KEYZ・コブクロ(メジャーデビュー25周年)・≠ME。
  目玉企画=チョコプラのオリジナル楽曲制作。ゲストのアドバイスでブラッシュアップし、第6話で披露。
  ビデオポッドキャスト「オトバズMAGAZINE」をAmazon Musicアプリ(iOS/Android、全サブスクプラン)で10/22から本編に合わせて配信。
  配信時刻・2話以降の配信日・各回ゲスト・KO1KEYZの披露曲は未発表(10/15時点)。
- ko1keyz.com /schedule/list には10/15時点でまだ掲載なし。
公式X投稿は埋め込み(画像のダウンロード・アップロードはしない)。グループ記事なのでUI色はウォームグレー。
"""
import base64, json, os, re, subprocess, sys
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
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

AB = "#ddd9d3"
AL = "#8a8378"
BG = "#f7f6f4"
TH = "#ece9e4"

TW_KO1 = "https://twitter.com/KO1KEYZofficial/status/2110578899252019619"
TW_AMZ = "https://twitter.com/amazonmusicjp/status/2110573936148873333"

JP_REL = [
    ("https://chomoand-1.com/ko1keyz-tv-schedule-1011-1017-14586", "KO1KEYZのテレビ出演は？10/11〜10/17の放送予定まとめ"),
    ("https://chomoand-1.com/meiji-bulgaria-yogurt-cm-ko1keyz-14529", "明治ブルガリアヨーグルト新CMはKO1KEYZ！ONE SHOT新WEB CM"),
    ("https://chomoand-1.com/ko1keyz-koigame-move-jordan-trunner-14736", "「恋GAME」ダンス動画で12人が履いていたスニーカー"),
    ("https://chomoand-1.com/ko1keyz-member-playlist-14182", "KO1KEYZ選曲プレイリストまとめ(12人が選んだ曲)"),
]
KR_REL = [
    ("https://chomoand-1.com/ko/meiji-bulgaria-yogurt-cm-ko1keyz-kr-14531", "메이지 불가리아 요구르트 새 CM은 KO1KEYZ!"),
    ("https://chomoand-1.com/ko/ko1keyz-koigame-move-jordan-trunner-kr-14738", "'恋GAME' 댄스 영상 속 12명의 스니커즈"),
    ("https://chomoand-1.com/ko/ko1keyz-member-playlist-kr-14183", "KO1KEYZ 멤버 선곡 플레이리스트 총정리"),
]
EN_REL = [
    ("https://chomoand-1.com/en/meiji-bulgaria-yogurt-cm-ko1keyz-en-14532", "KO1KEYZ in Meiji Bulgaria Yogurt's new web CM"),
    ("https://chomoand-1.com/en/ko1keyz-koigame-move-jordan-trunner-en-14739", "The sneakers in KO1KEYZ's \"Koi GAME\" dance video"),
]


def wp_upload(path, mime):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HEADERS_AUTH, "Content-Type": mime,
                               "Content-Disposition": f'attachment; filename="{path.name}"'},
                      data=path.read_bytes())
    r.raise_for_status()
    return r.json()


def post_draft(title, content, slug, lang, categories, featured_media, summary, translations=None):
    payload = {"title": title, "content": content, "slug": slug, "status": "draft", "lang": lang,
               "categories": categories, "featured_media": featured_media, "author": 2,
               "meta": {"jetpack_publicize_message": summary}}
    if translations:
        payload["translations"] = translations
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts",
                      headers={**HEADERS_AUTH, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    return r.json()


def make_eyecatch(args, out_path):
    subprocess.run([sys.executable, str(ROOT / "tools" / "eyecatch_koikeyz.py"), *args, "--out", str(out_path)], check=True)
    return wp_upload(out_path, "image/png")["id"]


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def p(t):
    return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"


def mark(t, big=False):
    s = ' style="font-size:1.15em;"' if big else ""
    return f'<strong><span class="swl-marker mark_yellow"{s}>{t}</span></strong>'


def html(block):
    return f"<!-- wp:html -->\n{block}\n<!-- /wp:html -->"


def minibox(rows):
    ps = [f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}</strong>{v}</p>' for i, (k, v) in enumerate(rows)]
    return html(f'<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">\n'
                + "\n".join(ps) + "\n</div>")


def infobox(title, rows, w="32%"):
    trs = "\n".join(f'<tr><td style="background:{TH};border:1px solid {AB};padding:8px 12px;width:{w};">{k}</td>'
                    f'<td style="border:1px solid {AB};padding:8px 12px;">{v}</td></tr>' for k, v in rows)
    return html(f'<div style="border:1px solid #ccc;border-radius:4px;padding:16px 18px;margin:0 0 16px 0;">\n'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>\n'
                f'<table style="border-collapse:collapse;width:100%;">\n{trs}\n</table>\n</div>')


def barbox(title, items, ordered=False):
    tag = "ol" if ordered else "ul"
    lis = "\n".join(f'<li style="margin:{"0" if i == len(items) - 1 else "0 0 8px 0"};">{it}</li>' for i, it in enumerate(items))
    return html(f'<div style="border:1px solid {AB};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{AL};color:#fff;">{title}</p>\n'
                f'<{tag} style="margin:0;padding:14px 18px 14px 34px;background:{BG};">\n{lis}\n</{tag}>\n</div>')


def personbox(name, body):
    return html(f'<div style="border:1px solid {AB};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">\n'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;color:{AL};">{name}</p>\n'
                f'<p style="margin:0;">{body}</p>\n</div>')


def linkbox(title, links):
    lis = "\n".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for u, t in links)
    return html(f'<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{BG};">\n'
                f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n'
                f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>')


CHECK = (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {AL};border-radius:3px;'
         f'color:{AL};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>')


def summarybox(items):
    return html(f'<div style="border:2px solid {AL};border-radius:8px;background:{BG};padding:1em 1.25em;margin:0 0 16px 0;">\n<p style="margin:0;">\n'
                + "<br>\n".join(CHECK + it for it in items) + "\n</p>\n</div>")


def note(t):
    return p(f'<span style="font-size:0.9em;color:#666;">{t}</span>')


def tweet(url, lang="ja"):
    return html(f'<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{url}">{url}</a></blockquote>\n'
                '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


# ============================== JP ==============================
JP_TITLE = "KO1KEYZがオトバズ初回に出演！配信日は？無料で見られる？"
JP_SLUG = "ko1keyz-otobuzz-prime-video"

JP_CONTENT = "\n\n".join([
    p("デビューから1週間あまり、KO1KEYZ(コイキーズ)に新しい出演情報が届きました。<br>\n"
      f"2026年10月15日、Amazon Musicの新しい音楽バラエティ番組{mark('「Amazon Music presents オトバズ」の#1(初回)にKO1KEYZが出演する', True)}ことが発表されています。<br>\n"
      f"配信は{mark('10月22日(木)スタートで、Prime Videoの独占配信')}です。<br>\n"
      "しかもPrime会員でなくても、Amazonのアカウントがあれば無料で見られます。<br>\n"
      "この記事では、配信日や見る方法、MC・共演ゲスト、番組の企画からKO1KEYZの見どころまで順番に紹介します。"),
    infobox("「オトバズ」#1の基本情報", [
        ("番組名", "Amazon Music presents オトバズ"),
        ("配信開始", "2026年10月22日(木)"),
        ("配信先", "Prime Video(独占配信)"),
        ("料金", "無料(Amazonアカウントがあれば、Prime会員でなくても視聴可)"),
        ("話数", "全6エピソード"),
        ("MC", "チョコレートプラネット(長田庄平・松尾駿)、北山宏光"),
        ("#1のゲスト", "KO1KEYZ、コブクロ、≠ME"),
        ("連動コンテンツ", "ビデオポッドキャスト「オトバズMAGAZINE」(Amazon Musicアプリ)"),
    ]),
    barbox("この記事でわかること", [
        "「オトバズ」はどんな番組？",
        "配信日と話数",
        "無料で見る方法",
        "MCと#1の共演ゲスト",
        "KO1KEYZの見どころ",
        "オトバズMAGAZINEとは？",
    ]),

    h2("KO1KEYZが出演する「オトバズ」はどんな番組？"),
    minibox([("番組：", "Amazon Music presents オトバズ"), ("ジャンル：", "音楽×お笑いの新感覚音楽バラエティ")]),
    p("「オトバズ」は、Amazon Musicが手がける音楽バラエティ番組です。<br>\n"
      "世代やジャンルをこえたアーティストがゲストに登場し、トークと音楽パフォーマンスでその魅力に迫っていきます。<br>\n"
      "音楽とコメディをかけ合わせた構成になっていて、ふつうの歌番組とはひと味違う空気になりそうです。"),
    p("KO1KEYZの公式Xでは、10月15日のお昼に出演が告知されました。<br>\n"
      "投稿には「#オトバズ」「#AmazonMusic」のハッシュタグも添えられています。"),
    tweet(TW_KO1),
    p("同じ日にはAmazon Music公式Xも番組のスタートを発表し、予告動画を公開しています。<br>\n"
      "番組の雰囲気が気になる方は、まずこちらの動画をチェックしてみてください。"),
    tweet(TW_AMZ),
    p("番組名の「バズ」には、SNSなどで話題になる「バズる」の意味が込められているようです。<br>\n"
      "MCの長田庄平さんも、視聴を呼びかける言葉として「とにかくバズれ！」を使っていて、番組全体のテーマになっているのが伝わってきますね。"),

    h2("オトバズの配信日はいつ？何話まである？"),
    minibox([("配信開始：", "2026年10月22日(木)"), ("話数：", "全6エピソード(KO1KEYZは#1に出演)")]),
    p(f"「オトバズ」は{mark('2026年10月22日(木)から、Prime Videoで独占配信', True)}されます。<br>\n"
      "番組は全6エピソードで、KO1KEYZが出るのは第1話にあたる#1です。<br>\n"
      "つまり、配信が始まった初日からKO1KEYZの出演回を見られることになります。"),
    p("一方で、配信が始まる時刻と、#2以降がどのペースで更新されるのかは、10月15日の時点ではまだ発表されていません。<br>\n"
      "KO1KEYZ公式サイトのスケジュールにもまだ載っていないので、近くなったら公式サイトやAmazon Music公式Xで追加の案内が出るかもしれません。"),
    p("10月22日の週は、ほかにも10月23日(金)深夜にテレビ朝日「M:ZINE」の放送が予定されています。<br>\n"
      "デビュー後のテレビ・配信の出演は、<a href=\"https://chomoand-1.com/ko1keyz-tv-schedule-1011-1017-14586\" target=\"_blank\" rel=\"noopener\">KO1KEYZの週間テレビ出演まとめ</a>でも日付順に紹介しています。"),

    h2("オトバズは無料で見られる？見る方法は？"),
    minibox([("料金：", "無料"), ("必要なもの：", "Amazonのアカウント(Prime会員でなくてもOK)")]),
    p(f"Prime Videoの番組と聞くと、Prime会員にならないと見られないイメージがあるかもしれません。<br>\n"
      f"ですが「オトバズ」は{mark('Prime会員かどうかに関係なく、Amazonのアカウントを持っている人なら誰でも見られる', True)}番組です。<br>\n"
      "ふだんAmazonで買い物をしている方なら、そのアカウントでそのまま見られます。"),
    barbox("オトバズの見方", [
        "Amazonのアカウントを用意する(持っていない場合は無料で作成)",
        "スマホ・タブレットならPrime Videoアプリ、パソコンならAmazonのサイトからPrime Videoを開く",
        "Amazonのアカウントでログインする",
        "検索で「オトバズ」と入れて、#1を再生する",
    ], ordered=True),
    p("テレビの大きな画面で見たい場合は、Fire TV StickやPrime Videoアプリが入っているスマートテレビでも同じアカウントで見られます。<br>\n"
      "配信が始まる前でも、作品ページが公開されたら「ウォッチリスト」に入れておくと、当日に探す手間がはぶけて便利です。"),

    h2("オトバズのMCと#1の共演ゲストは？"),
    minibox([("MC：", "チョコレートプラネット(長田庄平・松尾駿)、北山宏光"), ("#1ゲスト：", "KO1KEYZ、コブクロ、≠ME")]),
    p("MCを務めるのは、お笑いコンビのチョコレートプラネットと、歌手・俳優の北山宏光さんの3人です。<br>\n"
      "#1にはKO1KEYZのほかに、コブクロと≠ME(ノットイコールミー)も登場します。"),
    personbox("チョコレートプラネット(MC)",
              "長田庄平さん(1980年1月28日生まれ、京都府出身)と松尾駿さん(1982年8月18日生まれ、神奈川県出身)の2人による、吉本興業所属のお笑いコンビです。<br>\n"
              "コントやものまねでおなじみで、今回は音楽番組のMCという新しい役どころに挑みます。<br>\n"
              "長田さんは、アーティストの曲作りとお笑いのネタ作りには共通点があると感じたそうです。"),
    personbox("北山宏光(MC)",
              "1985年9月17日生まれ、神奈川県出身の歌手・俳優です。<br>\n"
              "Kis-My-Ft2のメンバーとして活動したあと、2023年8月にグループを離れ、現在はソロで音楽活動と俳優業を続けています。<br>\n"
              "番組では、自身の音楽活動の経験を生かして、アーティストの魅力や楽曲にこめた思いを深く届けたいと話しています。"),
    personbox("コブクロ(#1ゲスト)",
              "小渕健太郎さんと黒田俊介さんによる2人組の音楽ユニットです。<br>\n"
              "2001年にメジャーデビューし、2026年はメジャーデビュー25周年の節目にあたります。<br>\n"
              "「蕾」「桜」など、世代をこえて歌いつがれる曲を数多く持っています。"),
    personbox("≠ME(#1ゲスト)",
              "指原莉乃さんがプロデュースするアイドルグループです。<br>\n"
              "2019年に結成され、=LOVE(イコールラブ)・≒JOY(ニアリーイコールジョイ)と並ぶ「イコノイジョイ」の一員として活動しています。"),
    p("25周年のベテランデュオ、人気アイドルグループ、そしてデビューしたばかりのKO1KEYZという、まさに世代もジャンルもバラバラな顔ぶれです。<br>\n"
      "番組が掲げる「世代やジャンルをこえる」というコンセプトが、初回からはっきり表れた組み合わせといえます。"),

    h2("KO1KEYZはオトバズで何をする？見どころは？"),
    minibox([("内容：", "トークと音楽パフォーマンス"), ("番組の目玉：", "チョコプラのオリジナル楽曲づくりにゲストがアドバイス")]),
    p("番組では、ゲストのアーティストがトークと音楽パフォーマンスを披露します。<br>\n"
      "KO1KEYZがどの曲を披露するのか、どんな話をするのかは、まだ明かされていません。"),
    p(f"注目したいのは、番組の目玉になっている{mark('チョコレートプラネットのオリジナル楽曲づくり')}です。<br>\n"
      "チョコプラが各回のゲストからヒントやアドバイスをもらいながら少しずつ曲を仕上げていき、最終回の第6話で完成した曲を披露します。<br>\n"
      "#1はその最初の回なので、KO1KEYZが曲づくりのスタートにどう関わるのかも気になるところです。"),
    p("KO1KEYZは12人組のグループで、歌もダンスもラップもこなすメンバーがそろっています。<br>\n"
      "ダンスの振りやパフォーマンスの見せ方など、ボーイズグループならではの目線で、チョコプラの曲にアドバイスをする場面があるかもしれません。<br>\n"
      "コブクロや≠MEとはタイプの違うアドバイスになりそうで、3組の意見がどう混ざり合うのかも楽しみですね。"),
    p("また、KO1KEYZはテレビ朝日「M:ZINE」の「バラエティー101新世界」のように、デビュー直後からバラエティでも存在感を見せています。<br>\n"
      "お笑い芸人のチョコプラとの掛け合いで、12人のどのメンバーが笑いを取りにいくのかも見逃せません。<br>\n"
      "10月7日に日韓同時デビューしたばかりのKO1KEYZにとって、Prime Videoの番組は日本でさらに名前を知ってもらうきっかけにもなりそうです。"),

    h2("オトバズMAGAZINEとは？どこで見られる？"),
    minibox([("内容：", "ビデオポッドキャスト"), ("配信先：", "Amazon Musicアプリ(iOS・Android)")]),
    p("番組本編とあわせて、ビデオポッドキャスト「Amazon Music presents オトバズMAGAZINE」も10月22日から配信されます。<br>\n"
      "ビデオポッドキャストは、ポッドキャストを「聴く」だけでなく、映像つきで「観る」こともできる新しい形のコンテンツです。"),
    p("見られるのはiOS・AndroidのAmazon Musicアプリで、Amazon Musicのすべてのプランが対象になっています。<br>\n"
      "本編の更新に合わせて新しいエピソードが追加されていくので、本編では見られない話が出てくる可能性もありそうです。<br>\n"
      "KO1KEYZの回のMAGAZINEがあるかどうかもふくめて、配信が始まったらアプリをのぞいてみてください。"),
    note("※2026年10月15日時点の情報です。配信の時刻や内容は変わる場合があるので、最新の情報はAmazon Music・KO1KEYZの公式サイトやXでご確認ください。"),

    h2("まとめ"),
    summarybox([
        "KO1KEYZは「Amazon Music presents オトバズ」の#1(初回)に出演",
        "配信は2026年10月22日(木)から、Prime Videoで独占配信(全6エピソード)",
        "Amazonアカウントがあれば、Prime会員でなくても無料で見られる",
        "MCはチョコレートプラネットと北山宏光、#1の共演はコブクロと≠ME",
        "チョコプラのオリジナル楽曲づくりにゲストがアドバイスし、第6話で披露",
        "Amazon Musicアプリではビデオポッドキャスト「オトバズMAGAZINE」も配信",
    ]),
    p("無料で見られるので、Prime会員でない友だちにもすすめやすい番組です。<br>\n"
      "10月22日の配信開始に向けて、ウォッチリストに入れて待っておきましょう！"),
    linkbox("KO1KEYZの関連記事", JP_REL),
])

JP_SUMMARY = ("コイキーズ(KO1KEYZ)が、Amazon Musicの新番組「オトバズ」#1に出演！10月22日(木)からPrime Videoで独占配信、Amazonアカウントがあれば無料で見られます。MCはチョコプラと北山宏光。")

# ============================== KR ==============================
KR_TITLE = "KO1KEYZ, 오토바즈 첫 회 출연! 공개일은? 무료로 볼 수 있을까?"
KR_SLUG = f"{JP_SLUG}-kr"

KR_CONTENT = "\n\n".join([
    p("데뷔한 지 일주일여 만에 KO1KEYZ(코이키즈)의 새로운 출연 소식이 전해졌습니다.<br>\n"
      f"2026년 10월 15일, Amazon Music의 새 음악 버라이어티 {mark('「Amazon Music presents 오토바즈(オトバズ)」#1(첫 회)에 KO1KEYZ가 출연', True)}한다고 발표됐어요.<br>\n"
      f"공개는 {mark('10월 22일(목)부터 Prime Video 독점')}입니다.<br>\n"
      "게다가 Prime 회원이 아니어도 Amazon 계정만 있으면 무료로 볼 수 있어요.<br>\n"
      "이 글에서는 공개일, 시청 방법, MC와 함께 출연하는 게스트, 프로그램 기획과 KO1KEYZ의 볼거리까지 순서대로 정리했습니다."),
    infobox("'오토바즈' #1 기본 정보", [
        ("프로그램", "Amazon Music presents オトバズ(오토바즈)"),
        ("공개 시작", "2026년 10월 22일(목)"),
        ("공개처", "Prime Video(독점)"),
        ("요금", "무료(Amazon 계정이 있으면 Prime 회원이 아니어도 시청 가능)"),
        ("에피소드", "총 6회"),
        ("MC", "초콜릿 플래닛(나가타 쇼헤이・마츠오 슌), 키타야마 히로미츠"),
        ("#1 게스트", "KO1KEYZ, 코부쿠로, ≠ME"),
        ("연동 콘텐츠", "비디오 팟캐스트 'オトバズMAGAZINE'(Amazon Music 앱)"),
    ]),
    barbox("이 글에서 알 수 있는 것", [
        "'오토바즈'는 어떤 프로그램?",
        "공개일과 에피소드 수",
        "무료로 보는 방법",
        "MC와 #1 게스트",
        "KO1KEYZ의 볼거리",
    ]),
    h2("KO1KEYZ가 출연하는 '오토바즈'는 어떤 프로그램?"),
    minibox([("프로그램: ", "Amazon Music presents オトバズ"), ("장르: ", "음악×코미디의 신감각 음악 버라이어티")]),
    p("'오토바즈'는 Amazon Music이 선보이는 음악 버라이어티 프로그램입니다.<br>\n"
      "세대와 장르를 넘나드는 아티스트가 게스트로 나와 토크와 음악 퍼포먼스로 그 매력을 파헤칩니다.<br>\n"
      "음악과 코미디를 결합한 구성이라 일반적인 음악 방송과는 또 다른 분위기가 될 것 같아요."),
    p("KO1KEYZ 공식 X는 10월 15일 낮에 출연 소식을 알렸습니다."),
    tweet(TW_KO1, "ko"),
    p("같은 날 Amazon Music 공식 X도 프로그램 시작을 발표하고 예고 영상을 공개했어요."),
    tweet(TW_AMZ, "ko"),
    h2("'오토바즈' 공개일은 언제? 몇 회까지?"),
    minibox([("공개 시작: ", "2026년 10월 22일(목)"), ("에피소드: ", "총 6회(KO1KEYZ는 #1 출연)")]),
    p(f"'오토바즈'는 {mark('2026년 10월 22일(목)부터 Prime Video에서 독점 공개', True)}됩니다.<br>\n"
      "총 6회 구성이며, KO1KEYZ가 나오는 회차는 첫 회인 #1이에요.<br>\n"
      "공개 첫날부터 KO1KEYZ 출연분을 볼 수 있는 셈입니다."),
    p("다만 공개 시각과 #2 이후의 업데이트 주기는 10월 15일 기준 아직 발표되지 않았습니다.<br>\n"
      "KO1KEYZ 공식 사이트 스케줄에도 아직 올라와 있지 않으니, 가까워지면 공식 사이트나 Amazon Music 공식 X에서 추가 안내가 나올 수도 있어요."),
    h2("'오토바즈'는 무료로 볼 수 있을까? 시청 방법은?"),
    minibox([("요금: ", "무료"), ("필요한 것: ", "Amazon 계정(Prime 회원이 아니어도 OK)")]),
    p(f"Prime Video 프로그램이라고 하면 Prime 회원이어야 볼 수 있을 것 같지만, '오토바즈'는 {mark('Prime 회원 여부와 관계없이 Amazon 계정이 있는 사람이라면 누구나 볼 수 있는', True)} 프로그램입니다."),
    barbox("'오토바즈' 보는 방법", [
        "Amazon 계정을 준비한다(없으면 무료로 생성)",
        "스마트폰・태블릿은 Prime Video 앱, PC는 Amazon 사이트에서 Prime Video를 연다",
        "Amazon 계정으로 로그인한다",
        "'オトバズ'를 검색해 #1을 재생한다",
    ], ordered=True),
    note("※일본 이외의 지역에서는 Prime Video의 공개 여부가 다를 수 있습니다."),
    h2("'오토바즈' MC와 #1 게스트는?"),
    minibox([("MC: ", "초콜릿 플래닛, 키타야마 히로미츠"), ("#1 게스트: ", "KO1KEYZ, 코부쿠로, ≠ME")]),
    personbox("초콜릿 플래닛(MC)",
              "나가타 쇼헤이(1980년 1월 28일생, 교토부 출신)와 마츠오 슌(1982년 8월 18일생, 가나가와현 출신)으로 이루어진 요시모토 흥업 소속 개그 콤비입니다.<br>\n"
              "콩트와 성대모사로 잘 알려져 있으며, 이번에는 음악 프로그램 MC에 도전합니다."),
    personbox("키타야마 히로미츠(MC)",
              "1985년 9월 17일생, 가나가와현 출신의 가수 겸 배우입니다.<br>\n"
              "Kis-My-Ft2 멤버로 활동한 뒤 2023년 8월 그룹을 떠나, 현재는 솔로로 음악과 연기 활동을 하고 있어요."),
    personbox("코부쿠로(#1 게스트)",
              "코부치 켄타로와 쿠로다 슌스케의 2인조 음악 유닛입니다.<br>\n"
              "2001년 메이저 데뷔해 2026년에 메이저 데뷔 25주년을 맞았습니다."),
    personbox("≠ME(#1 게스트)",
              "사시하라 리노가 프로듀스하는 아이돌 그룹으로, 2019년에 결성됐습니다."),
    h2("KO1KEYZ는 '오토바즈'에서 무엇을 할까? 볼거리는?"),
    minibox([("내용: ", "토크와 음악 퍼포먼스"), ("핵심 기획: ", "초콜릿 플래닛의 오리지널 곡 만들기에 게스트가 조언")]),
    p("KO1KEYZ가 어떤 곡을 선보이고 어떤 이야기를 할지는 아직 공개되지 않았습니다.<br>\n"
      f"주목할 점은 {mark('초콜릿 플래닛의 오리지널 곡 제작')} 기획이에요.<br>\n"
      "매회 게스트에게 힌트와 조언을 받으며 곡을 다듬어 가고, 마지막 6화에서 완성곡을 공개합니다.<br>\n"
      "#1은 그 첫 회인 만큼, KO1KEYZ가 곡 만들기의 출발점에 어떻게 관여할지도 궁금해지네요."),
    p("12인조 보이즈 그룹다운 안무와 퍼포먼스 시선으로 조언하는 장면이 나올지도 모릅니다.<br>\n"
      "10월 7일 한일 동시 데뷔한 KO1KEYZ에게 Prime Video 프로그램은 일본에서 이름을 더 알릴 좋은 기회가 될 것 같아요."),
    h2("'오토바즈 MAGAZINE'이란?"),
    minibox([("내용: ", "비디오 팟캐스트"), ("공개처: ", "Amazon Music 앱(iOS・Android)")]),
    p("본편과 함께 비디오 팟캐스트 'Amazon Music presents オトバズMAGAZINE'도 10월 22일부터 공개됩니다.<br>\n"
      "Amazon Music 앱의 모든 요금제가 대상이며, 본편 업데이트에 맞춰 새 에피소드가 추가될 예정이에요."),
    note("※2026년 10월 15일 기준 정보입니다. 최신 정보는 Amazon Music・KO1KEYZ 공식 사이트와 X에서 확인해 주세요."),
    h2("정리"),
    summarybox([
        "KO1KEYZ는 'Amazon Music presents 오토바즈' #1(첫 회)에 출연",
        "2026년 10월 22일(목)부터 Prime Video 독점 공개(총 6회)",
        "Amazon 계정만 있으면 Prime 회원이 아니어도 무료 시청 가능",
        "MC는 초콜릿 플래닛과 키타야마 히로미츠, #1 게스트는 코부쿠로와 ≠ME",
        "초콜릿 플래닛의 오리지널 곡 제작에 게스트가 조언, 6화에서 공개",
    ]),
    p("무료로 볼 수 있으니 주변에도 추천하기 좋은 프로그램이에요.<br>\n"
      "10월 22일 공개를 기대하며 기다려 봐요!"),
    linkbox("KO1KEYZ 관련 글", KR_REL),
])

KR_SUMMARY = ("코이키즈(KO1KEYZ)가 Amazon Music 새 프로그램 '오토바즈' #1에 출연! 10월 22일(목)부터 Prime Video 독점 공개, Amazon 계정만 있으면 무료로 볼 수 있어요.")

# ============================== EN ==============================
EN_TITLE = "KO1KEYZ on OTOBUZZ Episode 1: Release Date and How to Watch Free"
EN_SLUG = f"{JP_SLUG}-en"

EN_CONTENT = "\n\n".join([
    p("Just over a week after their debut, KO1KEYZ have another new appearance lined up.<br>\n"
      f"On October 15, 2026, it was announced that {mark('KO1KEYZ will appear in episode 1 of \"Amazon Music presents OTOBUZZ (オトバズ)\"', True)}, a new music variety show from Amazon Music.<br>\n"
      f"The show {mark('starts streaming on Thursday, October 22, exclusively on Prime Video')}.<br>\n"
      "Even better, you don't need a Prime membership: anyone with an Amazon account can watch it for free.<br>\n"
      "This article covers the release date, how to watch, the hosts and fellow guests, the show's main project and what to look forward to from KO1KEYZ."),
    infobox("OTOBUZZ episode 1 at a glance", [
        ("Show", "Amazon Music presents オトバズ (OTOBUZZ)"),
        ("Premiere", "Thursday, October 22, 2026"),
        ("Where", "Prime Video (exclusive)"),
        ("Price", "Free with an Amazon account (no Prime membership needed)"),
        ("Episodes", "6"),
        ("Hosts", "Chocolate Planet (Shohei Osada, Shun Matsuo) and Hiromitsu Kitayama"),
        ("Episode 1 guests", "KO1KEYZ, Kobukuro, ≠ME"),
        ("Companion content", "Video podcast \"OTOBUZZ MAGAZINE\" (Amazon Music app)"),
    ], w="30%"),
    barbox("In this article", [
        "What is OTOBUZZ?",
        "Release date and number of episodes",
        "How to watch for free",
        "Hosts and episode 1 guests",
        "What to expect from KO1KEYZ",
    ]),
    h2("What is OTOBUZZ, the show KO1KEYZ will appear on?"),
    minibox([("Show: ", "Amazon Music presents オトバズ"), ("Genre: ", "A music-meets-comedy variety show")]),
    p("OTOBUZZ is a music variety show produced by Amazon Music.<br>\n"
      "Artists from different generations and genres appear as guests, and the show digs into their appeal through talk segments and live performances.<br>\n"
      "Because it mixes music with comedy, it should feel quite different from a standard music program."),
    p("KO1KEYZ's official X account announced the appearance around noon on October 15."),
    tweet(TW_KO1, "en"),
    p("On the same day, Amazon Music Japan's official X account announced the show and shared a trailer."),
    tweet(TW_AMZ, "en"),
    h2("When does OTOBUZZ start, and how many episodes are there?"),
    minibox([("Premiere: ", "Thursday, October 22, 2026"), ("Episodes: ", "6 (KO1KEYZ appear in episode 1)")]),
    p(f"OTOBUZZ {mark('starts streaming exclusively on Prime Video on Thursday, October 22, 2026', True)}.<br>\n"
      "The series has six episodes, and KO1KEYZ appear in the very first one.<br>\n"
      "That means fans can watch KO1KEYZ's episode from day one."),
    p("As of October 15, the release time and the schedule for episode 2 onward haven't been announced.<br>\n"
      "The show isn't on KO1KEYZ's official schedule page yet either, so more details may come from the official site or Amazon Music's X account closer to the date."),
    h2("Can you watch OTOBUZZ for free? How to watch"),
    minibox([("Price: ", "Free"), ("What you need: ", "An Amazon account (Prime membership not required)")]),
    p(f"Prime Video shows usually require a Prime membership, but OTOBUZZ {mark('can be watched by anyone with an Amazon account, whether or not they are a Prime member', True)}."),
    barbox("How to watch OTOBUZZ", [
        "Get an Amazon account (it's free to create one)",
        "Open the Prime Video app on your phone or tablet, or Prime Video on the Amazon website on a computer",
        "Sign in with your Amazon account",
        "Search for \"オトバズ\" and play episode 1",
    ], ordered=True),
    note("* Availability on Prime Video may differ outside Japan."),
    h2("Who are the hosts and the episode 1 guests?"),
    minibox([("Hosts: ", "Chocolate Planet, Hiromitsu Kitayama"), ("Episode 1 guests: ", "KO1KEYZ, Kobukuro, ≠ME")]),
    personbox("Chocolate Planet (hosts)",
              "A Yoshimoto Kogyo comedy duo made up of Shohei Osada (born January 28, 1980, from Kyoto) and Shun Matsuo (born August 18, 1982, from Kanagawa).<br>\n"
              "Known for sketches and impressions, they take on a new role as music show hosts."),
    personbox("Hiromitsu Kitayama (host)",
              "A singer and actor born September 17, 1985, in Kanagawa.<br>\n"
              "After performing as a member of Kis-My-Ft2, he left the group in August 2023 and now works as a solo artist and actor."),
    personbox("Kobukuro (episode 1 guest)",
              "A music duo of Kentaro Kobuchi and Shunsuke Kuroda.<br>\n"
              "They made their major debut in 2001, and 2026 marks their 25th anniversary."),
    personbox("≠ME (episode 1 guest)",
              "An idol group produced by Rino Sashihara, formed in 2019."),
    h2("What will KO1KEYZ do on OTOBUZZ?"),
    minibox([("Content: ", "Talk and a music performance"), ("Main project: ", "Guests advise Chocolate Planet on writing an original song")]),
    p("Which song KO1KEYZ will perform and what they'll talk about hasn't been revealed yet.<br>\n"
      f"The highlight of the series is {mark('Chocolate Planet writing an original song')}.<br>\n"
      "They polish it bit by bit with hints and advice from each episode's guests, and perform the finished song in episode 6.<br>\n"
      "Since episode 1 is where it all begins, it'll be interesting to see how KO1KEYZ help get the song started."),
    p("As a 12-member boy group, KO1KEYZ might offer advice from a dance and performance angle.<br>\n"
      "For a group that debuted in Japan and Korea on October 7, a Prime Video show is a great chance to reach even more viewers in Japan."),
    h2("What is OTOBUZZ MAGAZINE?"),
    minibox([("Format: ", "Video podcast"), ("Where: ", "Amazon Music app (iOS and Android)")]),
    p("Alongside the main show, a video podcast called \"Amazon Music presents オトバズMAGAZINE\" also starts on October 22.<br>\n"
      "It's available on all Amazon Music plans, with new episodes added as the main show updates."),
    note("* Information as of October 15, 2026. Please check Amazon Music's and KO1KEYZ's official sites and X accounts for the latest details."),
    h2("Summary"),
    summarybox([
        "KO1KEYZ appear in episode 1 of \"Amazon Music presents OTOBUZZ\"",
        "Streaming starts Thursday, October 22, 2026, exclusively on Prime Video (6 episodes)",
        "Free to watch with an Amazon account, no Prime membership needed",
        "Hosted by Chocolate Planet and Hiromitsu Kitayama, with Kobukuro and ≠ME also on episode 1",
        "Guests help Chocolate Planet write an original song, performed in episode 6",
    ]),
    p("Since it's free, it's an easy show to recommend to friends, too.<br>\n"
      "Let's look forward to October 22!"),
    linkbox("More on KO1KEYZ", EN_REL),
])

EN_SUMMARY = ("KO1KEYZ will appear in episode 1 of Amazon Music's new show OTOBUZZ, streaming free on Prime Video from Oct 22 with just an Amazon account.")


def count(c):
    t = re.sub(r"<!--.*?-->|<script.*?</script>|<[^>]+>", "", c, flags=re.S)
    return len(re.sub(r"\s", "", t))


if __name__ == "__main__":
    for name, c in [("JP", JP_CONTENT), ("KR", KR_CONTENT), ("EN", EN_CONTENT)]:
        print(name, "chars:", count(c))
    print("JP title len", len(JP_TITLE))
    assert count(JP_CONTENT) >= 2500 and len(JP_TITLE) <= 35
    if "--dry" in sys.argv:
        sys.exit()

    JP_EYECATCH_ID = make_eyecatch(
        ["--top", "Amazon Music「オトバズ」", "--main", "KO1KEYZ", "--bottom", "初回に出演！", "--bottom", "10/22からPrime Videoで無料配信"],
        ROOT / "images" / "ko1keyz_otobuzz_1015_eyecatch.png")
    print("JP_EYECATCH_ID", JP_EYECATCH_ID)
    jp = post_draft(JP_TITLE, JP_CONTENT, JP_SLUG, "ja", [66, 62], JP_EYECATCH_ID, JP_SUMMARY)
    print("JP_POST_ID", jp["id"], jp["slug"])

    KR_EYECATCH_ID = make_eyecatch(
        ["--top", "Amazon Music '오토바즈'", "--main", "KO1KEYZ", "--bottom", "첫 회 출연!", "--bottom", "10/22부터 Prime Video 무료 공개", "--lang", "kr"],
        ROOT / "images" / "ko1keyz_otobuzz_1015_eyecatch_kr.png")
    kr = post_draft(KR_TITLE, KR_CONTENT, KR_SLUG, "ko", [74, 70], KR_EYECATCH_ID, KR_SUMMARY, translations={"ja": jp["id"]})
    print("KR_POST_ID", kr["id"], kr["slug"])

    en = post_draft(EN_TITLE, EN_CONTENT, EN_SLUG, "en", [110, 112], JP_EYECATCH_ID, EN_SUMMARY, translations={"ja": jp["id"]})
    print("EN_POST_ID", en["id"], en["slug"])
