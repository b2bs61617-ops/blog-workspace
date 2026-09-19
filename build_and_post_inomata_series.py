# -*- coding: utf-8 -*-
"""猪俣周杜 関連記事シリーズ -> chomoand.com

速報記事(既存・更新)+ ずらし記事5本(下書き)を作成し、相互リンクで回遊させる。
使い方: python build_and_post_inomata_series.py [key ...]  (省略時は全部)
key: breaking / profile / gakureki / kazoku / kanojo / 8iper
"""
import json, base64, os, sys
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
WP_URL = ENV["WP_TREND_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_TREND_USERNAME']}:{ENV['WP_TREND_APP_PASSWORD']}".encode()).decode()
HEADERS_AUTH = {"Authorization": f"Basic {AUTH}"}

ACCENT = "#546e7a"
ACCENT_BORDER = "#cfd8dc"
ACCENT_BG = "#f3f6f8"
CATEGORIES = [37]  # 芸能・トレンド
AUTHOR = 4  # Tomoki PC -> anco

TBS_URL = "https://news.yahoo.co.jp/articles/34a015511fb2a8b81fede3ad36ccd23942ac8e54"
WIKI_URL = "https://ja.wikipedia.org/wiki/%E7%8C%AA%E4%BF%A3%E5%91%A8%E6%9D%9C"


# ---------------------------------------------------------------- helpers
def link(slug):
    return f"{WP_URL}/{slug}/"


def a(key, text):
    return f'<a href="{link(META[key]["slug"])}">{text}</a>'


def p(sentences):
    body = "<br>\n".join(sentences)
    return f"<!-- wp:paragraph -->\n<p>{body}</p>\n<!-- /wp:paragraph -->"


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def wphtml(raw):
    return f"<!-- wp:html -->\n{raw}\n<!-- /wp:html -->"


def table(rows, head=None):
    def tr(cells, is_head=False):
        bg = f"background:{ACCENT_BG};" if is_head else ""
        tds = "".join(
            f'<td style="border:1px solid #ccc;padding:8px 12px;{bg}{"font-weight:bold;" if (is_head or i == 0) else ""}">{c}</td>'
            for i, c in enumerate(cells)
        )
        return f"<tr>{tds}</tr>"

    trs = []
    if head:
        trs.append(tr(head, True))
    trs += [tr(r) for r in rows]
    return (
        '<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n'
        + "\n".join(trs)
        + "\n</tbody></table></figure>\n<!-- /wp:table -->"
    )


def wakaru(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(
        f'<div style="border:1px solid {ACCENT_BORDER};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{ACCENT};color:#fff;">この記事でわかること</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{ACCENT_BG};">\n{lis}\n</ul>\n</div>'
    )


def mini(rows):
    ps = "\n".join(
        f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}:</strong>{v}</p>'
        for i, (k, v) in enumerate(rows)
    )
    return wphtml(
        f'<div style="border:1px solid {ACCENT_BORDER};border-left:4px solid {ACCENT};border-radius:4px;'
        f'padding:10px 16px;margin:0 0 16px 0;background:{ACCENT_BG};">\n{ps}\n</div>'
    )


CHECK = (
    f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {ACCENT};border-radius:3px;'
    f'color:{ACCENT};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>'
)


def matome(items):
    ps = "<br>\n".join(f"{CHECK}{i}" for i in items)
    return wphtml(
        f'<div style="border:1px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{ACCENT_BG};">\n'
        f'<p style="margin:0;">\n{ps}\n</p>\n</div>'
    )


def source_note(items):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return wphtml(f'<div style="font-size:0.85em;color:#666;margin:0 0 16px 0;">\n<p style="margin:0 0 4px 0;">参考にした情報</p>\n<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>')


def related(exclude):
    lis = "\n".join(
        f'<li><a href="{link(META[k]["slug"])}">{META[k]["related"]}</a></li>'
        for k in ORDER
        if k != exclude
    )
    return wphtml(
        f'<div style="border:1px solid {ACCENT_BORDER};border-left:4px solid {ACCENT};border-radius:4px;'
        f'padding:14px 18px;margin:16px 0 0 0;background:{ACCENT_BG};">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">猪俣周杜さんの関連記事</p>\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n{lis}\n</ul>\n</div>'
    )


def strong(t):
    return f'<strong><span class="swl-marker mark_yellow">{t}</span></strong>'


# ---------------------------------------------------------------- meta
ORDER = ["breaking", "xreaction", "audition", "shows", "profile", "gakureki", "kazoku", "kanojo", "8iper"]
META = {
    "breaking": {
        "slug": "shuto-inomata-arrested-breaking",
        "title": "猪俣周杜が傷害容疑で逮捕！コンビニで知人女性を殴った疑い？",
        "related": "【続報】猪俣周杜が傷害容疑で逮捕！コンビニで知人女性を殴った疑い",
        "status": "publish",
        "eyecatch": "inomata_breaking2_eyecatch.png",
        "eyecatch_replace": True,
    },
    "xreaction": {
        "slug": "shuto-inomata-x-reaction",
        "title": "【猪俣周杜】逮捕へのXの反応は？ファンの声まとめ！",
        "related": "猪俣周杜の逮捕へのXの反応・ファンの声まとめ",
        "status": "draft",
        "eyecatch": "inomata_xreaction_eyecatch.png",
    },
    "audition": {
        "slug": "shuto-inomata-audition-members",
        "title": "【猪俣周杜】逮捕でオーディション組が批判？声を調査！",
        "related": "猪俣周杜の逮捕でオーディション組が批判？声を調査",
        "status": "draft",
        "eyecatch": "inomata_audition_eyecatch.png",
    },
    "shows": {
        "slug": "shuto-inomata-timelesz-shows",
        "title": "【猪俣周杜】逮捕でtimeleszの番組・CMはどうなる？",
        "related": "猪俣周杜の逮捕でtimeleszの番組・CMはどうなる？",
        "status": "draft",
        "eyecatch": "inomata_shows_eyecatch.png",
    },
    "profile": {
        "slug": "shuto-inomata-profile",
        "title": "【猪俣周杜】wikiプロフィール！年齢・身長・経歴は？",
        "related": "猪俣周杜のwikiプロフィール・年齢・身長・経歴",
        "status": "draft",
        "eyecatch": "inomata_profile_eyecatch.png",
    },
    "gakureki": {
        "slug": "shuto-inomata-gakureki",
        "title": "【猪俣周杜】学歴は？高校・中学・大学進学を調査！",
        "related": "猪俣周杜の学歴(高校・中学・大学進学)",
        "status": "draft",
        "eyecatch": "inomata_gakureki_eyecatch.png",
    },
    "kazoku": {
        "slug": "shuto-inomata-kazoku",
        "title": "【猪俣周杜】家族構成は？父親の塗装会社や兄弟を調査！",
        "related": "猪俣周杜の家族構成(父親の塗装会社・兄弟)",
        "status": "draft",
        "eyecatch": "inomata_kazoku_eyecatch.png",
    },
    "kanojo": {
        "slug": "shuto-inomata-kanojo",
        "title": "【猪俣周杜】彼女はいる？歴代の熱愛の噂を調査！",
        "related": "猪俣周杜に彼女はいる？歴代の熱愛の噂",
        "status": "draft",
        "eyecatch": "inomata_kanojo_eyecatch.png",
    },
    "8iper": {
        "slug": "shuto-inomata-8iper",
        "title": "【猪俣周杜】8iper脱退の理由は？地下アイドル時代を調査！",
        "related": "猪俣周杜の8iper脱退理由・地下アイドル時代",
        "status": "draft",
        "eyecatch": "inomata_8iper_eyecatch.png",
    },
}


# ---------------------------------------------------------------- articles
def build_breaking():
    b = []
    b.append(p([
        "timeleszの猪俣周杜さん(25)が、2026年9月19日、傷害の疑いで警視庁に逮捕されました。",
        f"報道によると、{strong('9月18日午後10時半ごろ、東京都江東区辰巳のコンビニエンスストアの駐車場に止めた車内で、20代の知人女性の顔を殴るなどした疑い')}が持たれています。",
    ]))
    b.append(p([
        "猪俣さんは調べに対し、「口論の際、手が当たってしまった」という趣旨の説明をしていると伝えられています。",
        "所属事務所のSTARTO ENTERTAINMENTの関係者は、「事実関係を確認しています」とコメントしました。",
    ]))
    b.append(p([
        "午前11時台の初報では逮捕の事実しか伝わっていませんでしたが、午後に入って詳しい内容が報じられました。",
        "この記事は、続報を反映して更新しています(9月19日午後の時点)。",
    ]))
    b.append(wakaru([
        "逮捕容疑と、事件の内容(日時・場所・被害者・本人の説明)",
        "所属事務所の対応",
        "Yahoo!ニュースのコメント欄など、ネット上の反応",
        "猪俣周杜さんのプロフィールと関連記事",
        "傷害罪とは何か、逮捕後の一般的な流れ",
    ]))

    b.append(h2("猪俣周杜さんは何をした？逮捕容疑と報道の内容"))
    b.append(table([
        ("逮捕日", "2026年9月19日(土)。逮捕したのは警視庁"),
        ("容疑", "傷害"),
        ("事件があったとされる日時", "9月18日午後10時半ごろ"),
        ("場所", "東京都江東区辰巳のコンビニエンスストアの駐車場に止めた車の中"),
        ("被害を受けた方", "20代の知人女性(顔を殴るなどした疑い)"),
        ("本人の説明", "「口論の際、手が当たってしまった」という趣旨の供述(報道による)"),
        ("報じた主な媒体", "TBS NEWS DIG、日テレNEWS NNN、東スポWEBなど"),
    ]))
    b.append(p([
        "TBS NEWS DIGは、9月19日午前11時53分に「傷害の疑いで逮捕」と第一報を配信し、13時台の更新で事件の詳細を伝えました。",
        "日テレNEWS NNNは、捜査関係者への取材で逮捕がわかったと報じています。",
    ]))
    b.append(p([
        "被害の程度や、二人の関係の詳しい経緯、けがの有無や程度といった点は、報じられていません。",
        "「手が当たってしまった」という説明と、「顔を殴るなどした」という容疑との間に、どのような違いがあるのかも、今後の捜査で明らかになる部分です。",
        "双方の話や現場の状況は、今後の捜査で確かめられていきます。現時点で断定できることは限られています。",
    ]))
    b.append(p([
        "東スポWEBは、猪俣さんが逮捕の前日の18日夜、Instagramのストーリーズで同じグループの原嘉孝さんと仕事をしていたことを投稿していたと伝えています。",
    ]))
    b.append(source_note([
        f'<a href="{TBS_URL}">TBS NEWS DIG「timeleszの猪俣周杜容疑者(25)を傷害の疑いで逮捕 コンビニ駐車場の車内で知人女性(20代)の顔面殴るなどしたか」(Yahoo!ニュース、2026年9月19日)</a>',
        '<a href="https://news.yahoo.co.jp/articles/5060e28311b28d32a983a6019364731078eef4c8">日テレNEWS NNN「人気アイドルグループ「timelesz」猪俣周杜容疑者を逮捕 傷害の疑い 警視庁」(Yahoo!ニュース、2026年9月19日)</a>',
        '<a href="https://news.yahoo.co.jp/articles/d4350d304ef587d274cd13fda612eb5b93aa2aa4">TBS NEWS DIG「傷害の疑いで逮捕 猪俣周杜 事務所関係者は〝事実関係を確認しています〟」(Yahoo!ニュース、2026年9月19日)</a>',
        '<a href="https://www.tokyo-sports.co.jp/articles/-/403688">東スポWEB「timeleszの猪俣周杜容疑者を逮捕 傷害容疑 前日にはメンバーと仕事現場一緒か」(2026年9月19日)</a>',
    ]))

    b.append(h2("所属事務所の対応は？"))
    b.append(p([
        "STARTO ENTERTAINMENTの関係者は、TBS NEWS DIGの取材に対し、「事実関係を確認しています」とのみ答えています。",
        "東スポWEBの取材申し込みには、19日昼の時点で返答がありませんでした。",
        "現時点で、公式サイトでの声明や、グループの活動方針についての発表は確認できていません。",
        f"出演中の番組やCMへの影響は{a('shows', 'こちらの記事')}にまとめています。",
    ]))

    b.append(h2("ネット上の反応は？Yahoo!ニュースのコメント欄"))
    b.append(p([
        "Yahoo!ニュースのコメント欄には、9月19日の午後の時点で2,400件を超えるコメントが集まっています。",
        "初報の配信直後は約150件でしたので、詳細が報じられて一気に反応が増えたことになります。",
    ]))
    b.append(mini([
        ("最も共感を集めた意見", "オーディションで入ったメンバーを否定する風潮が強まることへの懸念"),
        ("次に多い論点", "下積みの経験の重要性や、事務所の教育体制への疑問"),
        ("3番目の論点", "特別な形で加入した立場としての責任感を問う意見"),
        ("その他", "事実確認を待つべきだという慎重な意見。被害を受けた方への言及は限られていた"),
    ]))
    b.append(p([
        "全体では厳しい意見が大半を占め、擁護する声はほとんど見られませんでした。",
        "コメント欄にはアルコールの影響などをめぐる推測も書き込まれていますが、報道では触れられておらず、事実として確認されたものではありません。",
        f"Xでの反応は{a('xreaction', 'ファンの声をまとめた記事')}、オーディション出身メンバーへの意見は{a('audition', 'こちらの記事')}で詳しく紹介しています。",
    ]))

    b.append(h2("猪俣周杜さんとは？プロフィールをおさらい"))
    b.append(p([
        "猪俣周杜さんは2001年8月17日生まれ、茨城県出身のアイドルで、2025年2月にオーディション「timelesz project」を経てtimeleszに加入しました。",
        "加入前は地下アイドルグループ「8iper」で活動しており、グループ卒業後は父親が営む塗装会社で経理を担当していたことでも知られています。",
        f"詳しい経歴は{a('profile', '猪俣周杜さんのwikiプロフィール')}、地下アイドル時代については{a('8iper', '8iper脱退の理由をまとめた記事')}で紹介しています。",
    ]))
    b.append(p([
        f"出身校については{a('gakureki', '学歴の記事')}、家族については{a('kazoku', '家族構成の記事')}、恋愛面のうわさについては{a('kanojo', '彼女に関する記事')}にまとめました。",
        "いずれも公表されている情報と、確認できていない情報を分けて書いています。",
    ]))

    b.append(h2("「傷害」とはどんな罪？逮捕後の一般的な流れ"))
    b.append(p([
        "傷害罪(刑法204条)は、他人の身体に傷害を負わせた場合に問われる罪で、法定刑は15年以下の懲役または50万円以下の罰金です。",
        "けがをさせるに至らなかった場合は、傷害ではなく暴行罪(刑法208条)にあたります。",
        "今回は「傷害」の容疑で逮捕されたと報じられていますので、相手にけがを負わせた疑いが持たれているとみられます。",
    ]))
    b.append(p([
        "逮捕後の一般的な流れは次のとおりです。",
        "警察は逮捕から48時間以内に、事件を検察官に送ります(送検)。",
        "検察官は送検から24時間以内に、裁判官へ勾留を請求するかどうかを判断します。",
        "勾留が認められると、原則10日間、延長を含めて最長20日間、身柄が拘束されます。",
        "この間に検察官が、起訴か不起訴かを決めます。",
    ]))
    b.append(wphtml(
        f'<div style="border:1px solid {ACCENT_BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{ACCENT_BG};">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">知っておきたい注意点</p>\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n'
        f'<li>逮捕は「罪を犯した疑いがある」という段階で、有罪が確定したわけではありません</li>\n'
        f'<li>本人の説明と容疑の食い違いなど、事実関係は今後の捜査で確かめられます</li>\n'
        f'<li>被害を受けた方がいますので、憶測や誹謗中傷は控えましょう</li>\n'
        f'</ul>\n</div>'
    ))

    b.append(h2("今後の見通しと続報の確認方法"))
    b.append(p([
        "今後の焦点は、送検や勾留の有無、事務所からの正式なコメント、そしてtimeleszの活動への影響です。",
        "続報を確認するときは、事務所・警察・大手報道機関など、出どころがはっきりした情報を優先してください。",
    ]))

    b.append(h2("まとめ"))
    b.append(matome([
        "猪俣周杜さん(25)が2026年9月19日、傷害の疑いで警視庁に逮捕された",
        "9月18日午後10時半ごろ、江東区辰巳のコンビニ駐車場の車内で、20代の知人女性の顔を殴るなどした疑い",
        "猪俣さんは「口論の際、手が当たってしまった」という趣旨の説明をしていると報じられている",
        "事務所関係者は「事実関係を確認しています」とコメントし、正式な声明は出ていない",
        "逮捕は有罪の確定ではなく、今後の捜査・処分を見守る必要がある",
    ]))
    b.append(p(["新しい情報が入りしだい、この記事を更新していきます。"]))
    b.append(related("breaking"))
    return b


def build_profile():
    b = []
    b.append(p([
        f"timeleszの猪俣周杜(いのまた しゅうと)さんは、{strong('2001年8月17日生まれの25歳、茨城県出身、身長172cm')}のアイドルです。",
        f"2026年9月19日に傷害の疑いで逮捕されたと報じられ(詳しくは{a('breaking', '速報記事')})、あらためて経歴に注目が集まっています。",
    ]))
    b.append(p([
        "この記事では、基本プロフィールから8iper時代を含む経歴、timeleszでの出演作までをwiki風にまとめました。",
    ]))
    b.append(wakaru([
        "基本プロフィール(年齢・身長・血液型など)",
        "前世(8iper)から、timelesz加入までの経歴",
        "timeleszでの活動と主な出演作",
        "人柄が分かるエピソード",
    ]))

    b.append(h2("猪俣周杜さんのwiki風プロフィール"))
    b.append(h3("基本プロフィール"))
    b.append(table([
        ("名前", "猪俣 周杜(いのまた しゅうと)"),
        ("生年月日", "2001年8月17日(2026年9月時点で25歳)"),
        ("出身地", "茨城県"),
        ("身長", "172cm"),
        ("血液型", "AB型"),
        ("所属", "STARTO ENTERTAINMENT / timelesz"),
        ("メンバーカラー", "黄色"),
        ("愛称", "「シュートくん」と呼ばれたいと語っている"),
        ("趣味", "食べること、スポーツ・アニメ・ドラマ観賞"),
        ("特技", "体を動かすこと(学生時代はサッカーに打ち込んでいた)"),
    ]))
    b.append(h3("どんな人？"))
    b.append(p([
        "猪俣さんは、オーディション「timelesz project」の配信内で行われた「努力がハンパないと思った候補生ランキング」で第1位に選ばれた努力家です。",
        "メンバーの松島聡さんは、誰からも愛される人柄で、苦しい状況でもポジティブに乗り越えていく姿勢を高く評価していました。",
        "菊池風磨さんや佐藤勝利さんも、努力を見せずにひたむきに自分と向き合う姿や、壁にぶつかっても自力で乗り越える姿を挙げています。",
    ]))
    b.append(p([
        "プライベートでは、食べることやアニメ、ドラマ鑑賞が好きで、お酒は弱いと明かしています。",
        f"サッカーは学生時代から続けており、バラエティ番組で披露することもありました(学生時代の話は{a('gakureki', '学歴の記事')}で紹介しています)。",
    ]))

    b.append(h2("猪俣周杜さんのwiki風経歴"))
    b.append(h3("前世は？8iperで約1年半の活動"))
    b.append(p([
        "猪俣さんは、timeleszに加入する前に、アイドルグループ「8iper(ハイパー)」に所属して約1年半活動していました。",
        "2022年11月にデビューし、2024年5月末にグループを卒業したとされています。",
        f"卒業の経緯や、timelesz projectとの関係については{a('8iper', '8iper脱退の理由をまとめた記事')}で詳しく紹介しています。",
    ]))
    b.append(h3("父の塗装会社で経理を担当"))
    b.append(p([
        "8iperを卒業した後は、父親が営む塗装会社で働いていました。",
        "本人は「塗装自体は全く経験がなく、経理を担当していた」と語っています。",
        f"実家や家族については{a('kazoku', '家族構成の記事')}にまとめました。",
    ]))
    b.append(h3("timelesz projectを経て加入"))
    b.append(p([
        "timelesz projectに参加した理由について、猪俣さんは、Sexy Zoneの配信ラストライブを見て言葉にできないほど心を動かされ、その直後にオーディションが発表されたためと語っています。",
        "オーディションを経て、2025年2月にtimeleszの新メンバーとして加入しました。",
        "同年3月21日に個人の公式Instagramを開設し、4月にはSTARTO ENTERTAINMENTの「FAMILY CLUB web」で個人ブログも始めています。",
    ]))

    b.append(h2("timeleszでの活動・主な出演作"))
    b.append(table([
        ("ドラマ", "『パパと親父のウチご飯』(テレビ朝日)阿久津竜也役", "2025年10月〜12月(第3話〜最終話)"),
        ("配信ドラマ", "『阿久津の夢と俺レシピ』(TELASA)主演", "2025年11月(前編・後編)"),
        ("ドラマ", "『東京P.D. 警視庁広報2係』(フジテレビ)川畑礼介役", "2026年1月27日・2月3日(第3話・第4話)"),
        ("バラエティ", "『ニカゲーム』(テレビ朝日)", "2025年4月〜"),
        ("バラエティ", "『今夜はナゾトレ』(フジテレビ)レギュラー", "2025年10月〜2026年3月"),
        ("バラエティ", "『せいや&猪俣の3行キッチン』(中京テレビ)", "2026年3月"),
        ("CM", "Hamee「ByGLOW」ブランドアンバサダー", "2025年12月〜"),
    ], head=("種別", "作品・役", "時期")))
    b.append(p([
        "加入から1年余りで、ドラマ・バラエティ・CMと活動の場を広げてきました。",
        "『東京P.D. 警視庁広報2係』では、好青年の顔を持つ犯人役という、これまでのイメージとは違う役どころに挑戦しています。",
    ]))

    b.append(h2("まとめ"))
    b.append(matome([
        "猪俣周杜さんは2001年8月17日生まれ、茨城県出身、身長172cm、血液型はAB型",
        "8iperで約1年半活動した後、父親の塗装会社で経理を担当し、2025年2月にtimeleszへ加入",
        "timelesz projectの「努力がハンパないと思った候補生ランキング」で1位に選ばれた努力家",
        "加入後はドラマ・バラエティ・CMに出演し、活動の場を広げてきた",
    ]))
    b.append(p([
        "2026年9月19日に逮捕が報じられましたが、事実関係は今後の捜査や発表で明らかになるとみられます。",
        "続報が入りしだい、関連記事も更新していきます。",
    ]))
    b.append(source_note([f'<a href="{WIKI_URL}">猪俣周杜 - Wikipedia</a>', "timelesz公式サイト(Over The Top)のメンバープロフィール"]))
    b.append(related("profile"))
    return b


def build_gakureki():
    b = []
    b.append(p([
        f"猪俣周杜さんの出身校は、{strong('茨城県立藤代紫水高校(取手市)とされています')}が、本人や事務所が学校名を公表したものではありません。",
        f"2026年9月19日に傷害の疑いで逮捕されたと報じられたこともあり(詳しくは{a('breaking', '速報記事')})、学歴を調べる人が増えています。",
    ]))
    b.append(p([
        "この記事では、小学校から高校までの推定と、その根拠、大学へ進学したかどうかを整理しました。",
        "確定情報と推測を分けて書いていますので、あわせて確認してください。",
    ]))
    b.append(wakaru(["小学校・中学校", "高校(藤代紫水高校とされる根拠)", "大学への進学の有無", "サッカーに打ち込んだ学生時代"]))

    b.append(h2("猪俣周杜さんの学歴は？"))
    b.append(mini([
        ("小学校", "つくば市立谷田部小学校とされる(推定)"),
        ("中学校", "つくば市立谷田部中学校とされる(推定)"),
        ("高校", "茨城県立藤代紫水高校とされる(推定)"),
        ("大学", "進学していないとみられる"),
    ]))
    b.append(p([
        "猪俣さんは茨城県出身で、学校名は本人の口から明確には語られていません。",
        "ネット上で「谷田部小→谷田部中→藤代紫水高」と言われているのは、所属していたサッカーチームの拠点や、修学旅行の行き先に関する発言などから推測されたものです。",
        "確定情報ではないため、以下では「〜とされる」という書き方で紹介します。",
    ]))

    b.append(h3("小学校・中学校は？"))
    b.append(p([
        "小学校はつくば市立谷田部小学校、中学校は同じ地域の谷田部中学校とされています。",
        "小学生のころから地元のサッカーチームでフォワードとして活躍し、小学6年生(2013年)には茨城県南地区のU-12選抜に選ばれたと伝えられています。",
        "中学ではサッカー部に所属し、リフティングが得意だったそうです。",
    ]))
    b.append(p([
        "サッカーへの熱中ぶりは、大人になった今も変わりません。",
        "大みそかにひとりでサッカーをして骨折した経験があると、バラエティ番組などで語られています。",
    ]))

    b.append(h3("高校は藤代紫水高校？"))
    b.append(p([
        "高校は、茨城県取手市にある県立の共学校、藤代紫水高校とされています。",
        "根拠として挙げられているのは、猪俣さんが「修学旅行で沖縄に行った」と発言したことと、2019年の同校の修学旅行先が沖縄だったことが一致する点です。",
        "偏差値は40台前半とする情報があり、高校時代もサッカー部に所属して部活動に打ち込んでいたとされています。",
        "また、高校時代にはアルバイトも経験していたそうです。",
    ]))
    b.append(wphtml(
        f'<div style="border:1px solid {ACCENT_BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{ACCENT_BG};">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">藤代紫水高校ってどんな学校？</p>\n'
        f'<p style="margin:0;">茨城県取手市にある県立の共学校です。<br>猪俣さんの出身校であることは公式に発表されたものではなく、上記の発言などからの推測です。</p>\n</div>'
    ))
    b.append(wphtml(
        '<iframe src="https://maps.google.com/maps?q=%E8%8C%A8%E5%9F%8E%E7%9C%8C%E7%AB%8B%E8%97%A4%E4%BB%A3%E7%B4%AB%E6%B0%B4%E9%AB%98%E7%AD%89%E5%AD%A6%E6%A0%A1&t=&z=14&ie=UTF8&iwloc=&output=embed" '
        'width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>'
    ))

    b.append(h3("大学は？"))
    b.append(p([
        "猪俣さんは2001年生まれで、2020年3月に高校を卒業した計算になります。",
        "その後は大学へ進学せず、2022年11月に8iperのメンバーとして芸能活動を始めたとされています。",
        f"高校卒業から8iperのデビューまでの約2年半に何をしていたかは、公表されていません。8iperでの活動は{a('8iper', 'こちらの記事')}で紹介しています。",
    ]))

    b.append(h2("まとめ"))
    b.append(matome([
        "小学校・中学校・高校ともに、学校名は本人が公表したものではなく、推測の情報",
        "小学校は谷田部小学校、中学校は谷田部中学校、高校は藤代紫水高校とされている",
        "小学6年で茨城県南U-12選抜に選ばれるなど、サッカーに打ち込んだ学生時代だった",
        "大学へは進学せず、2022年に8iperで芸能活動を始めたとみられる",
    ]))
    b.append(p([
        "確かな学歴情報は、今後の本人のインタビューや公式プロフィールで明らかになるかもしれません。",
        "分かり次第、この記事も更新します。",
    ]))
    b.append(related("gakureki"))
    return b


def build_kazoku():
    b = []
    b.append(p([
        f"猪俣周杜さんの実家は、{strong('茨城県で塗装会社を営んでいる')}ことが分かっています。",
        f"2026年9月19日に傷害の疑いで逮捕されたと報じられたこともあり(詳しくは{a('breaking', '速報記事')})、家族構成を調べる人が増えています。",
    ]))
    b.append(p([
        "この記事では、本人が語った内容や公表されている情報にしぼって、家族構成を整理しました。",
        "家族は一般の方ですので、名前や勤務先の特定につながる詮索は行いません。",
    ]))
    b.append(wakaru(["何人家族？", "父親の塗装会社と、猪俣さんが働いた経緯", "母親・兄弟について", "実家はどこ？"]))

    b.append(h2("猪俣周杜さんの家族構成"))
    b.append(h3("何人家族？"))
    b.append(mini([
        ("父親", "茨城県で塗装会社を経営"),
        ("母親", "詳細は公表されていない"),
        ("兄弟姉妹", "情報が食い違っており確定できない"),
    ]))
    b.append(p([
        "家族構成の全体像は、公式には明かされていません。",
        "確かなのは、父親が塗装会社を営んでいることと、実家が茨城県にあることの2点です。",
    ]))

    b.append(h3("父親は塗装会社を経営"))
    b.append(p([
        "猪俣さんの父親は、茨城県で塗装屋を営んでいます。",
        f"猪俣さんは{a('8iper', '8iperを卒業')}した後、この父親の会社で働いていました。",
        "本人は「塗装自体は全く経験がなく、経理を担当していた」と語っており、職人ではなく事務の仕事を手伝っていたようです。",
    ]))
    b.append(p([
        "地方で家業を手伝いながら、次の道を考える時間があったことが、その後のオーディション挑戦につながったとも受け取れます。",
        f"アイドルを目指したきっかけは{a('profile', 'プロフィールの記事')}でも紹介しています。",
    ]))

    b.append(h3("母親は？"))
    b.append(p([
        "母親については、職業や年齢などの情報は公表されていません。",
        "SNSなどでは、母親と仲の良い様子がうかがえるとされていますが、詳しいエピソードは確認できていません。",
    ]))

    b.append(h3("兄弟・姉妹は？"))
    b.append(p([
        "きょうだいについては、出どころによって情報が食い違っています。",
        "「弟がいる」という情報がある一方で、猪俣さん自身が「甥っ子が5人いる」と話していたとも伝えられており、後者が本当であれば年上のきょうだいがいる計算になります。",
        "どちらも本人や事務所が正式に説明したものではなく、現時点では兄弟姉妹の人数を確定できません。",
    ]))

    b.append(h3("実家はどこ？"))
    b.append(p([
        "実家は茨城県にあるとされ、猪俣さんが過去の動画で「めっちゃ田舎、茨城」と話していたと伝えられています。",
        "ネット上では、つくば市や土浦市周辺ではないかという推測もありますが、公表されていないため確かなことは分かりません。",
        "家族の生活に関わる情報ですので、これ以上の詮索は控えたいところです。",
    ]))

    b.append(h2("まとめ"))
    b.append(matome([
        "父親は茨城県で塗装会社を経営している",
        "猪俣さんは8iper卒業後、その会社で経理を担当した",
        "母親・兄弟姉妹の詳細は公表されておらず、確定できない",
        "実家は茨城県にあり、それ以上の場所は公表されていない",
    ]))
    b.append(p([
        "家族に関する情報は、本人の口から語られた分だけが確かな情報です。",
        "今後の発言や報道で新しいことが分かれば、この記事を更新します。",
    ]))
    b.append(related("kazoku"))
    return b


def build_kanojo():
    b = []
    b.append(p([
        f"猪俣周杜さんの交際については、{strong('公式に発表された彼女の情報は確認できていません')}。",
        f"2026年9月19日に傷害の疑いで逮捕されたと報じられたこともあり(詳しくは{a('breaking', '速報記事')})、恋愛面のうわさを調べる人が増えています。",
    ]))
    b.append(p([
        "この記事では、ネット上で話題になった噂を整理し、確認できている事実と、確認できていない情報を分けてまとめました。",
        "噂に名前が挙がった一般の方の特定につながる情報は、書きません。",
    ]))
    b.append(wakaru(["現在、彼女はいる？", "熱愛の噂と、その真偽", "好きなタイプ・恋愛観", "逮捕報道との関係"]))

    b.append(h2("猪俣周杜さんに現在彼女はいる？"))
    b.append(mini([
        ("結論", "公式に認められた交際相手の情報はない"),
        ("熱愛報道", "大手メディアによる熱愛報道は確認できていない"),
    ]))
    b.append(p([
        "猪俣さんや所属事務所が、交際相手の存在を認めたり、熱愛について説明したりしたことは、確認できていません。",
        "現在の交際の有無は、公表されていない以上、分からないというのが正確なところです。",
    ]))

    b.append(h2("歴代の彼女・熱愛の噂は？"))
    b.append(p([
        "ネット上では、過去に撮影されたとされる画像などが取り沙汰されたことがあります。",
        "SNSに出回った画像から、当時交際していた相手がいたのではないか、と推測する声が上がりました。",
    ]))
    b.append(p([
        "ただ、こうした画像は、本人のものかどうかや、撮影された時期が確認できていません。",
        "相手として名前が挙がった人物自身が関係を否定したと伝えられており、特定には至っていない状況です。",
        "つまり、噂は広まったものの、交際を裏付ける確かな根拠は見つかっていません。",
    ]))
    b.append(p([
        "アイドルの過去の交際は、噂が先行しやすく、真偽不明の情報が事実のように拡散されることも少なくありません。",
        "根拠のない情報をそのまま信じたり、相手とされる一般の方を詮索したりすることは避けたいところです。",
    ]))

    b.append(h2("好きなタイプ・恋愛観は？"))
    b.append(p([
        "猪俣さんが好きな異性のタイプや恋愛観について、雑誌やテレビで明確に語った内容は、確認できていません。",
        f"確認できるのは、食べることやスポーツ、アニメが好きで、お酒は弱いといった人柄の部分です({a('profile', 'プロフィールの記事')}で紹介しています)。",
        "今後、雑誌のインタビューやバラエティ番組で語られる機会があれば、この記事に追記します。",
    ]))

    b.append(h2("逮捕報道との関係は？"))
    b.append(p([
        "2026年9月19日に報じられた傷害の疑いでの逮捕では、被害を受けた方は20代の知人女性と報じられています。",
        "二人の関係が交際だったのかどうかは、報じられていません。",
        "根拠のない結びつけや、被害を受けた方を詮索するような書き込みは、当事者を傷つけることにもなりますので、避ける必要があります。",
    ]))

    b.append(h2("まとめ"))
    b.append(matome([
        "公式に認められた彼女の情報は確認できていない",
        "過去の交際をめぐる噂はあるが、画像や相手の特定などを含め、真偽は確認できていない",
        "好きなタイプ・恋愛観を本人が語った内容も、確認できていない",
        "今回の逮捕で被害を受けたのは20代の知人女性と報じられているが、二人の関係は報じられていない",
    ]))
    b.append(p([
        "噂と事実を分けて受け止めることが、ファンとして大切なスタンスと言えそうです。",
        "新しい情報が確認できたら、この記事を更新します。",
    ]))
    b.append(related("kanojo"))
    return b


def build_8iper():
    b = []
    b.append(p([
        f"猪俣周杜さんがtimeleszに加入する前に所属していた「8iper(ハイパー)」を卒業したのは、{strong('2024年5月末')}とされています。",
        f"公式が明かした理由は「健康上の理由」でしたが、2026年9月19日に傷害の疑いで逮捕されたと報じられたこともあり(詳しくは{a('breaking', '速報記事')})、地下アイドル時代の経歴にも関心が集まっています。",
    ]))
    b.append(p([
        "この記事では、8iperでの活動期間、卒業の経緯、timelesz projectとの関係を時系列で整理しました。",
    ]))
    b.append(wakaru(["8iperとはどんなグループ？", "卒業(脱退)の時期と公式の理由", "timelesz projectとの関係", "時系列の年表"]))

    b.append(h2("猪俣周杜さんの8iper時代"))
    b.append(h3("8iperとは？"))
    b.append(mini([
        ("グループ", "男性アイドルグループ「8iper(ハイパー)」"),
        ("猪俣さんの活動期間", "2022年11月〜2024年5月(約1年半)"),
        ("グループの解散", "2025年2月24日"),
    ]))
    b.append(p([
        "8iperは、いわゆる地下アイドルとして活動していた男性グループです。",
        "猪俣さんは2022年11月に初期メンバーとしてデビューし、約1年半、ライブ活動などを中心にアイドルとして経験を積みました。",
        f"高校卒業からデビューまでのことは{a('gakureki', '学歴の記事')}で触れています。",
    ]))

    b.append(h3("脱退(卒業)の理由は？"))
    b.append(p([
        "猪俣さんの卒業は、2024年5月2日に8iperの公式サイトで発表されました。",
        "発表では、猪俣さんから体調不良の報告を受け、関係者と話し合った結果、グループを卒業することになったと説明されています。",
        "実際の卒業日は、その約1か月後の2024年5月31日とされています。",
    ]))
    b.append(p([
        "この公式の理由に加えて、ネット上では別の見方も広がりました。",
        "同じ時期に、timelesz projectへの参加を考えていたという情報が伝わったためで、「オーディションを受けるために卒業したのではないか」という推測が飛び交っています。",
        "ただし、この点について猪俣さん本人が詳しい経緯を語ったものは確認できていません。",
    ]))

    b.append(h3("timelesz projectとの関係は？"))
    b.append(p([
        "猪俣さんは、timelesz projectに参加した理由について、Sexy Zoneの配信ラストライブを見て心を動かされ、その直後にオーディションが発表されたためと語っています。",
        "8iperの卒業後は父親の塗装会社で経理を担当し(詳しくは" + a('kazoku', '家族構成の記事') + "を参照)、その後にオーディションへ挑戦しました。",
        "オーディションを経て、2025年2月にtimeleszの新メンバーとなっています。",
    ]))
    b.append(p([
        "地下アイドルからオーディションを勝ち上がった経歴は、努力型と評される猪俣さんの人柄を象徴するものとして語られてきました。",
        f"加入後の活動は{a('profile', 'wikiプロフィールの記事')}にまとめています。",
    ]))

    b.append(h2("猪俣周杜さんの経歴年表"))
    b.append(table([
        ("2020年3月", "高校を卒業したとされる"),
        ("2022年11月", "8iperの初期メンバーとしてデビュー"),
        ("2024年5月2日", "8iper公式が「健康上の理由」による卒業を発表"),
        ("2024年5月31日", "8iperを卒業したとされる"),
        ("卒業後〜2025年", "父親の塗装会社で経理を担当"),
        ("2025年2月", "timelesz projectを経てtimeleszに加入"),
        ("2025年2月24日", "8iperが解散"),
    ], head=("時期", "出来事")))

    b.append(h2("まとめ"))
    b.append(matome([
        "8iperでの活動は2022年11月〜2024年5月の約1年半",
        "卒業は2024年5月2日に発表され、公式の理由は「健康上の理由」",
        "同時期にtimelesz projectへの参加を検討していたという情報があり、関係を推測する声もあるが、本人による説明は確認できていない",
        "その後、父親の塗装会社を経て、2025年2月にtimeleszへ加入した",
    ]))
    b.append(p([
        "卒業の本当の事情は、本人が語らない限り確かなことは分かりません。",
        "推測と事実を分けて、今後の発言を待ちたいところです。",
    ]))
    b.append(related("8iper"))
    return b



def build_xreaction():
    b = []
    b.append(p([
        f"2026年9月19日、timeleszの猪俣周杜さんが傷害の疑いで逮捕されたと報じられると、Xでは{strong('「何が起きたのか」という驚きと、詳細が分からないことへの戸惑い')}が一気に広がりました。",
        f"報道の内容は{a('breaking', '速報記事')}にまとめています。この記事では、Xの投稿の傾向を整理しました。",
    ]))
    b.append(p([
        "9月19日の午後には、事件の詳しい内容(9月18日夜、江東区のコンビニ駐車場の車内で20代の知人女性を殴るなどした疑い)も報じられました。",
        "以下のXの傾向は、初報直後の投稿を中心に集めたもので、続報後のYahoo!ニュースのコメント欄の傾向は後半で紹介します。",
    ]))
    b.append(p([
        "Xの「猪俣周杜 逮捕」の検索結果(話題順)を収集し、9月19日の午前11時台から12時30分ごろまでの約80件を確認しています。",
        "投稿の引用や投稿者名は出さず、傾向だけを紹介します。",
    ]))
    b.append(wakaru([
        "Xの反応の大きな流れ(驚き・戸惑い・批判)",
        "報道のされ方に対する声",
        "ファンや一般ユーザーが知りたがっていること",
        "反応を見るときの注意点",
    ]))

    b.append(h2("Xの反応は？投稿の傾向を分類"))
    b.append(table([
        ("驚き・「何が起きた？」", "最も多い。速報を見てすぐ検索したが情報が出てこない、という投稿が目立つ"),
        ("報道のされ方への戸惑い", "速報が一瞬で終わり、すぐ別のニュースや天気予報に切り替わったことへの困惑"),
        ("イメージとのギャップ", "暴力とは縁遠い印象だったため、人柄との落差に驚く声"),
        ("オーディション出身への意見", "新メンバーとして迎えた経緯を踏まえた、残念がる声や厳しい意見"),
        ("デマ・宣伝の疑い", "ドラマや映画の宣伝のようだ、誤報ではないか、と信じられない声"),
        ("揶揄や憶測", "面白がる投稿や、根拠のない原因の推測(少数)"),
    ], head=("傾向", "投稿の内容")))
    b.append(p([
        "全体の印象としては、批判や非難よりも、まず「本当なのか」という驚きが圧倒的でした。",
        "詳細が何も出ていない段階だけに、事実を確認できないまま反応が先に広がっている状態と言えます。",
    ]))

    b.append(h3("速報の出し方への戸惑い"))
    b.append(p([
        "テレビで見たという投稿では、「逮捕」のテロップが一瞬だけ流れ、すぐにCMや天気予報に切り替わったという報告が複数ありました。",
        "情報番組の合間に、写真だけが差し込まれて速報が流れたという声もあります。",
        "詳細がないまま終わってしまい、心配で落ち着かないとして、報じ方に不満を述べる投稿も見られました。",
    ]))
    b.append(p([
        "また、報道では「メンバー」ではなく「容疑者」と表記されたことに、あらためて事態の重さを感じたという投稿も目立ちました。",
    ]))

    b.append(h3("人柄とのギャップに驚く声"))
    b.append(p([
        "猪俣さんは、オーディションの配信内で「努力がハンパないと思った候補生ランキング」1位に選ばれた努力家で、周囲から人柄を高く評価されてきました(" + a('profile', 'プロフィールの記事') + "を参照)。",
        "そのため、暴力とは縁遠い印象だった、加入後は順調に見えていた、といった人柄との落差に驚く声が多く上がっています。",
        "一方で、事件の内容は何も分かっていないため、こうした印象が事実と合っているかどうかを判断することはできません。",
    ]))

    b.append(h3("オーディション組への意見も"))
    b.append(p([
        "元の3人が、批判されるリスクを覚悟してまで新メンバーを迎え入れたのに残念、という声が複数ありました。",
        "オーディション出身であることと今回の件を結びつける意見も一部にあり、賛否が分かれています。",
        f"この点は{a('audition', '別の記事')}で詳しくまとめました。",
    ]))

    b.append(h2("みんなが知りたいこと・記事にできるテーマ"))
    b.append(p([
        "投稿を見ると、読者の関心は次のような点に集まっています。",
    ]))
    b.append(mini([
        ("何をしたのか", "9月18日午後10時半ごろ、江東区辰巳のコンビニ駐車場の車内で、20代の知人女性の顔を殴るなどした疑いと報じられた。けがの程度などは報じられていません"),
        ("本人の説明", "「口論の際、手が当たってしまった」という趣旨の説明をしていると報じられた"),
        ("事務所・グループの対応", "事務所関係者は「事実関係を確認しています」とコメント。正式な声明は未発表"),
        ("番組やCMはどうなる", "出演中の仕事への影響。" + a('shows', 'こちらの記事') + "で整理しています"),
        ("猪俣さんの過去", "経歴・家族・8iper時代など。" + a('profile', 'wikiプロフィール') + "や" + a('8iper', '8iperの記事') + "にまとめました"),
    ]))

    b.append(h2("続報後のYahoo!ニュースのコメント欄は？"))
    b.append(p([
        "事件の詳細が報じられたあと、Yahoo!ニュースのコメント欄には2,400件を超えるコメントが集まりました。",
        "最も共感を集めたのは、オーディションで入ったメンバーを否定する風潮が強まることへの懸念で、次いで下積みの経験や事務所の教育体制を問う意見、特別な形で加入した立場の責任を問う意見が続いています。",
        "擁護する声はほとんどなく、被害を受けた方への言及は限られていました。",
    ]))

    b.append(h2("反応を見るときの注意点"))
    b.append(p([
        "事件の内容がまだ一部しか分かっていない段階では、SNSの憶測が事実のように広まりやすくなります。",
        "実際、Xには根拠のない原因の推測や、特定の人物やグループを攻撃する投稿も見られました。",
        "被害を受けた方がいる可能性もありますので、確かな情報が出るまでは、拡散や書き込みを慎重にしたいところです。",
    ]))

    b.append(h2("まとめ"))
    b.append(matome([
        "Xの反応で最も多かったのは、批判よりも「本当なのか」という驚きと戸惑い",
        "速報が一瞬で終わり、詳細が出ていないことへの不満も多かった",
        "人柄とのギャップに驚く声や、オーディション出身メンバーをめぐる意見も見られた",
        "詳しい内容が出そろっていない段階での憶測や攻撃は、控える必要がある",
    ]))
    b.append(p([
        "続報や公式の発表が出た段階で、反応の変化もあわせて更新していきます。",
    ]))
    b.append(related("xreaction"))
    return b


def build_audition():
    b = []
    b.append(p([
        f"猪俣周杜さんの逮捕が報じられたあと(詳しくは{a('breaking', '速報記事')})、Xでは{strong('オーディション出身メンバーへの風当たりを心配する声')}が上がっています。",
        "一方で、事件と加入の経緯は別の問題だという意見も多く、賛否が分かれています。",
    ]))
    b.append(p([
        "この記事では、timelesz projectとメンバー構成の事実を確認したうえで、Xで見られた意見を整理しました。",
    ]))
    b.append(wakaru([
        "timeleszの現在の体制とオーディションの経緯",
        "Xで見られた意見(残念がる声・批判・擁護)",
        "「オーディション出身だから」という見方は妥当か",
    ]))

    b.append(h2("timeleszの体制とオーディションの経緯"))
    b.append(mini([
        ("メンバー", "佐藤勝利・菊池風磨・松島聡と、新メンバー5人の計8人"),
        ("新メンバー", "寺西拓人・原嘉孝・橋本将生・猪俣周杜・篠塚大輝"),
        ("加入の経緯", "オーディション「timelesz project」を経て、2025年2月15日に発表"),
    ]))
    b.append(p([
        "timeleszは、Sexy Zoneから改名したグループで、3人体制だったところに、オーディション「timelesz project」で選ばれた5人が加わり、2025年から8人体制になりました。",
        "新メンバーには、元ジャニーズJr.の経験者など、さまざまな経歴の人がいます。",
        f"猪俣さんは、地下アイドルの経験を経て参加しており、詳しい経歴は{a('8iper', '8iperの記事')}や{a('profile', 'プロフィールの記事')}で紹介しています。",
    ]))

    b.append(h2("Xで見られた意見は？"))
    b.append(p([
        "9月19日の午前11時台から12時30分ごろまでに、Xで見られた投稿から、この件に関する意見を分類しました(投稿者名や原文の引用は控えています)。",
    ]))
    b.append(table([
        ("残念がる声", "元の3人が批判を覚悟して迎え入れ、本人も苦労して合格したのに、という落胆"),
        ("加入経路と結びつけられる懸念", "事件との因果関係はないとしつつ、ジュニアを経ていないからという見方をされても仕方ない、という受け止め"),
        ("厳しい批判", "地下アイドル出身者の加入そのものを否定する強い意見(少数)"),
        ("冷静な意見", "個人の件であり、グループ全体や加入の経緯とは分けて考えるべき、という慎重な声"),
    ], head=("意見の種類", "内容")))
    b.append(p([
        "Yahoo!ニュースのコメント欄(2,400件超)でも同じ流れが見られました。",
        "最も共感を集めたのは、オーディションで入った人はいらないという風潮が強まることへの懸念で、共感は1万5,000件を超えています。",
        "次いで、下積みの経験の重要性や事務所の教育体制を問う意見(共感約9,900件)、特別な形で加入した立場の責任を問う意見(共感約8,300件)が並びました。",
        "一方で、事実確認を待つべきだという慎重な意見も、一定数ありました。",
    ]))

    b.append(h2("「オーディション出身だから」という見方は妥当？"))
    b.append(p([
        "結論から言うと、現時点でオーディション出身であることと今回の逮捕を結びつける根拠は、報じられていません。",
        "報道されているのは、9月18日夜にコンビニの駐車場の車内で知人女性の顔を殴るなどした疑い、という個人の行為に関する内容で、加入の経緯との関連を示すものは含まれていないためです。",
    ]))
    b.append(p([
        "また、刑事事件は、どのような経歴の人にも起こりうるものです。",
        "加入の経路によって、個人の行動が決まるわけではありません。",
        "個人の問題をグループ全体や加入の仕組みの問題にすり替えてしまうと、ほかのメンバーやオーディションを勝ち上がった人たちに、事実と関係のない批判が向かうおそれもあります。",
    ]))
    b.append(p([
        "オーディションの様子は配信で公開されており、猪俣さんは「努力がハンパないと思った候補生ランキング」で1位に選ばれ、周囲から高く評価されていました。",
        "その評価があっただけに、落胆する声が大きくなっているとも言えそうです。",
    ]))

    b.append(h2("今後の焦点は？"))
    b.append(p([
        "今後は、事務所からの正式なコメント、捜査の進展、そして番組などの活動への影響が焦点になります(" + a('shows', '番組・CMへの影響の整理') + "もあわせてご覧ください)。",
        "事実関係が確かめられる前に、ほかのメンバーや加入の経緯への批判を強めることは避けたいところです。",
    ]))

    b.append(h2("まとめ"))
    b.append(matome([
        "timeleszは、元の3人と、オーディションで選ばれた5人の8人体制",
        "Xでは、オーディション出身メンバーへの風当たりを心配する声と、加入の経緯とは分けて考える声が並んだ",
        "オーディション出身であることと今回の逮捕を結びつける根拠は、現時点で報じられていない",
        "事実が分からない段階で、グループ全体や加入の仕組みを批判するのは控えたい",
    ]))
    b.append(p([
        "続報が出た段階で、この記事も更新します。",
    ]))
    b.append(related("audition"))
    return b


def build_shows():
    b = []
    b.append(p([
        f"猪俣周杜さんの逮捕が報じられたことを受けて(詳しくは{a('breaking', '速報記事')})、{strong('timeleszの番組・CM・ライブがどうなるのか')}を心配する声がXで広がっています。",
        "所属事務所の関係者は「事実関係を確認しています」とコメントしていますが、出演についての正式な発表は確認できていません(9月19日午後の時点)。",
    ]))
    b.append(p([
        "この記事では、猪俣さんが関わっている主な仕事を整理し、分かっていることと分かっていないことを分けてまとめました。",
    ]))
    b.append(wakaru([
        "猪俣周杜さんが関わる主な番組・CM",
        "すでに終了・完走している仕事",
        "現時点で発表されていること",
        "続報の確認方法",
    ]))

    b.append(h2("猪俣周杜さんが関わる主な番組・CM"))
    b.append(table([
        ("バラエティ", "『ニカゲーム』(テレビ朝日)", "2025年4月から出演"),
        ("バラエティ", "『せいや&猪俣の3行キッチン』(中京テレビ)", "2026年3月に放送"),
        ("CM", "Hamee「ByGLOW」ブランドアンバサダー", "2025年12月から就任"),
        ("バラエティ", "『今夜はナゾトレ』(フジテレビ)", "2025年10月期のレギュラー(2026年3月24日まで)"),
        ("ドラマ", "『東京P.D. 警視庁広報2係』『パパと親父のウチご飯』ほか", "すでに放送済み"),
    ], head=("種別", "作品・仕事", "状況")))
    b.append(p([
        "上の表は、公表されている出演情報をもとに整理したものです。",
        "現在も継続している番組やCMがどれかは、各局・企業の公式発表を待つ必要があります。",
        f"出演作の全体は{a('profile', 'wikiプロフィールの記事')}にまとめています。",
    ]))

    b.append(h2("ライブ・グループとしての活動は？"))
    b.append(p([
        "timeleszは、2026年5月から「We're timelesz LIVE TOUR 2026 episode 2 MOMENTUM」を開催し、最終日は8月30日の宮城公演でした。",
        "ツアーはすでに完走しており、逮捕の報道が今回のツアーに影響することはありません。",
        "一方で、9月以降のライブや、グループとしての新しい発表について、この記事の調査では確認できていません。",
    ]))

    b.append(h2("現時点で分かっていること・分かっていないこと"))
    b.append(mini([
        ("分かっていること", "猪俣さんが傷害の疑いで警視庁に逮捕されたと報道。事務所関係者は「事実関係を確認しています」とコメント"),
        ("分かっていないこと", "事務所の正式な声明、各局・企業の対応、今後の出演の扱い、グループの活動方針"),
    ]))
    b.append(p([
        "一般に、芸能人が逮捕された場合は、所属事務所が出演番組やイベントへの対応、本人の処分について発表することが多くなります。",
        "今回もその発表を待つことになりますが、捜査が始まったばかりの現時点では、対応を予測することはできません。",
    ]))

    b.append(h2("Xでのファンの声"))
    b.append(p([
        "Xでは、「これからのtimeleszはどうなるのか」といった、グループの体制や活動を案じる投稿が見られました。",
        "詳細が分からないまま速報だけが流れたことで、不安を抱えているファンが多いようです。",
        f"反応の全体像は{a('xreaction', 'Xの反応をまとめた記事')}で紹介しています。",
    ]))

    b.append(h2("続報の確認方法"))
    b.append(p([
        "番組やCM、グループの活動については、次の公式情報で確認するのが確実です。",
    ]))
    b.append(wphtml(
        f'<div style="border:1px solid {ACCENT_BORDER};border-left:4px solid {ACCENT};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{ACCENT_BG};">\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n'
        f'<li>timelesz公式サイトやFAMILY CLUBのお知らせ</li>\n'
        f'<li>STARTO ENTERTAINMENTの公式発表</li>\n'
        f'<li>各番組・各企業の公式サイトやSNS</li>\n'
        f'</ul>\n</div>'
    ))
    b.append(p([
        "SNSの真偽不明な情報に惑わされないよう、出どころのはっきりした発表を優先してください。",
    ]))

    b.append(h2("まとめ"))
    b.append(matome([
        "事務所関係者は「事実関係を確認しています」とコメントしたが、出演についての正式な発表は確認できていない",
        "猪俣さんが関わる主な仕事は、『ニカゲーム』、『せいや&猪俣の3行キッチン』、ByGLOWのCMなど",
        "ライブツアー「MOMENTUM」は8月30日に完走済みで、逮捕の影響は受けない",
        "今後の対応は、事務所や各社の発表を待つ必要がある",
    ]))
    b.append(p([
        "発表があり次第、この記事を更新します。",
    ]))
    b.append(related("shows"))
    return b


BUILDERS = {
    "breaking": build_breaking,
    "xreaction": build_xreaction,
    "audition": build_audition,
    "shows": build_shows,
    "profile": build_profile,
    "gakureki": build_gakureki,
    "kazoku": build_kazoku,
    "kanojo": build_kanojo,
    "8iper": build_8iper,
}


# ---------------------------------------------------------------- WP
def find_post_by_slug(slug):
    r = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        params={"slug": slug, "status": "any", "context": "edit", "_fields": "id,status,featured_media"},
        headers=HEADERS_AUTH,
    )
    r.raise_for_status()
    rows = r.json()
    return rows[0] if rows else None


def upload_eyecatch(fname):
    data = (ROOT / "images" / fname).read_bytes()
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        headers={**HEADERS_AUTH, "Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{fname}"'},
        data=data,
    )
    r.raise_for_status()
    return r.json()["id"]


def post_article(key):
    m = META[key]
    content = "\n\n".join(BUILDERS[key]())
    existing = find_post_by_slug(m["slug"])
    payload = {
        "title": m["title"],
        "content": content,
        "slug": m["slug"],
        "status": m["status"],
        "categories": CATEGORIES,
        "author": AUTHOR,
    }
    if existing:
        # 既存記事の公開状態は変えない(下書きなら下書き、公開済みなら公開のまま)
        payload["status"] = existing["status"]
        # 公開済み記事のタイトル・スラッグは絶対に変更しない(2026-09-19 トモキ指示)
        if existing["status"] == "publish":
            payload.pop("title", None)
            payload.pop("slug", None)
        if m.get("eyecatch_replace"):
            payload["featured_media"] = upload_eyecatch(m["eyecatch"])
        elif existing.get("featured_media"):
            payload["featured_media"] = existing["featured_media"]
        elif m.get("eyecatch"):
            payload["featured_media"] = upload_eyecatch(m["eyecatch"])
        endpoint = f"{WP_URL}/wp-json/wp/v2/posts/{existing['id']}"
    else:
        if m.get("eyecatch"):
            payload["featured_media"] = upload_eyecatch(m["eyecatch"])
        endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
    r = requests.post(
        endpoint,
        headers={**HEADERS_AUTH, "Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
    )
    r.raise_for_status()
    post = r.json()
    print(f"{key}: ID={post['id']} status={post['status']} slug={post['slug']} chars={len(content)}")
    print(f"   preview: {WP_URL}/?p={post['id']}")
    return post


if __name__ == "__main__":
    keys = sys.argv[1:] or ORDER
    for k in keys:
        post_article(k)
