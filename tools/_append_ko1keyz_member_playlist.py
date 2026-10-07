# -*- coding: utf-8 -*-
"""KO1KEYZメンバー選曲プレイリスト記事(chomoand-1 公開中 JP14182/KR14183/EN14184)に、公開されたメンバーの選曲を追記する。

- 初回(10/7 YOSHIKI)だけ: 「公開されたプレイリストの選曲」H2を新設し、「どこで聴ける」節・基本情報表・まとめ・予想の手がかりを
  配信先確定(Spotify/Apple Music/LINE MUSIC)の内容に書き換える。
- 毎回: PLAYLISTSに足したメンバーのH3節を「どこで聴ける」H2の直前に追加し、スケジュール表のセルを埋める。
  既にH3(id=playlist-{member小文字})がある人はスキップするので、何度流しても二重にならない。
- タイトルは送らない(公開済みのため不変)。statusも送らない(publishのまま)。

曲目はSpotify埋め込みページ(open.spotify.com/embed/playlist/{id})の__NEXT_DATA__から取得。
python tools/_append_ko1keyz_member_playlist.py [--dry]
"""
import json
import re
import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from ko1keyz_article_kit import WP_URL, HEADERS_AUTH as HA, Ui, wphtml, p, h2, a  # noqa: E402

IDS = {"ja": 14182, "ko": 14183, "en": 14184}
ui = Ui("#8a8378", "#ddd9d3", "#f7f6f4", "rgba(138,131,120,0.06)")
SERVICES = {"ja": "Spotify・Apple Music・LINE MUSIC", "ko": "Spotify・Apple Music・LINE MUSIC",
            "en": "Spotify, Apple Music and LINE MUSIC"}

# 公開済みメンバーの選曲。tracks = (JP曲名, JPアーティスト, EN表記曲名, ENアーティスト)
PLAYLISTS = [
    {
        "member": "YOSHIKI", "date": ("10月7日", "10월 7일", "October 7"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2107608577007571445",
        "lnk": "https://KO1KEYZ.lnk.to/YOSHIKI_KO1KEYZ",
        "spotify": "6w6qWx7uBQkGNfiJfjqzfV",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("Key of Story", "KO1KEYZ", "Key of Story", "KO1KEYZ"),
            ("ラブソング", "Marcy", "Love Song", "Marcy"),
            ("ラベンダー", "the shes gone", "Lavender", "the shes gone"),
            ("長い髪", "FOMARE", "Nagai Kami", "FOMARE"),
            ("ランデヴー", "shytaupe", "Rendezvous", "shytaupe"),
            ("幸せの花束を", "Marcy", "Shiawase no Hanataba wo", "Marcy"),
            ("魔法にかけられて", "Saucy Dog", "Mahou ni Kakerarete", "Saucy Dog"),
            ("なんでもないよ、", "マカロニえんぴつ", "Nandemonaiyo,", "Macaroni Enpitsu"),
            ("きらきら", "もさを。", "Kirakira", "mosawo."),
        ],
        "cell": ('the shes gone「ラベンダー」ほか全10曲', "the shes gone '라벤더' 등 총 10곡",
                 '10 songs, incl. the shes gone "Lavender"'),
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>トーク会で名前を挙げていたthe shes gone「ラベンダー」"),
                p("トップバッターのYOSHIKIが選んだのは、全10曲。",
                  "1曲目と2曲目には、デビューシングルから表題曲「KO1KEYZ」とカップリング曲「Key of Story」が入っていて、デビュー日らしい始まり方になっています。"),
                m["table"],
                p(f"いちばんの注目は、{mk('以前トーク会で「カバーしてみたい曲」として名前を挙げていたthe shes gone「ラベンダー」')}がしっかり入っていたこと。",
                  "本当に好きな曲なんだと分かって、うれしくなったファンも多いはずです。"),
                p("ほかにもSaucy Dog「魔法にかけられて」、マカロニえんぴつ「なんでもないよ、」、FOMARE「長い髪」と、バンドの曲が多めの選曲です。",
                  "Marcyは「ラブソング」と「幸せの花束を」の2曲が入っていて、KO1KEYZ以外で2曲選ばれたのはMarcyだけでした。"),
                p("「ラブソング」「ランデヴー」「魔法にかけられて」と、恋を思わせるタイトルの曲が並んでいるのも印象的。",
                  "「君に会う前に聴きたい」というテーマにまっすぐ答えた、全部で約41分のプレイリストです。",
                  f"聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>토크회에서 언급했던 the shes gone '라벤더'"),
                p("첫 번째 주자 YOSHIKI가 고른 곡은 총 10곡이에요.",
                  "1번과 2번 트랙은 데뷔 싱글의 타이틀곡 'KO1KEYZ'와 커플링곡 'Key of Story'로, 데뷔 날다운 시작입니다."),
                m["table"],
                p(f"가장 눈에 띄는 건 {mk('예전에 토크회에서 커버해 보고 싶은 곡으로 꼽았던 the shes gone \'라벤더\'')}가 들어 있다는 점이에요.",
                  "Saucy Dog, 마카로니 엔피츠, FOMARE 등 일본 밴드 곡이 많고, Marcy는 '러브송'과 '행복의 꽃다발을' 2곡이 선택됐어요."),
                p("'러브송', '랑데부', '마법에 걸려서'처럼 사랑을 떠올리게 하는 제목이 이어져, '너를 만나기 전에 듣고 싶은'이라는 테마에 딱 맞는 약 41분의 플레이리스트입니다.",
                  f"{a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>the shes gone \"Lavender\", a song he'd mentioned at a talk event"),
                p("Leading things off, YOSHIKI picked 10 songs.",
                  "Tracks 1 and 2 are the title track \"KO1KEYZ\" and the B-side \"Key of Story\", a fitting way to open on debut day."),
                m["table"],
                p(f"The standout: {mk('the shes gone \"Lavender\", which he once named at a fan talk event as a song he would like to cover')}, made the list.",
                  "The rest leans toward Japanese bands such as Saucy Dog, Macaroni Enpitsu and FOMARE, and Marcy is the only other artist with two songs."),
                p("With titles like \"Love Song\", \"Rendezvous\" and \"Mahou ni Kakerarete\" (Enchanted), it's a roughly 41-minute playlist that fits the \"before meeting you\" theme perfectly.",
                  f"Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
]


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def h3(text, anchor):
    return (f'<!-- wp:heading {{"level":3,"anchor":"{anchor}"}} -->\n'
            f'<h3 class="wp-block-heading" id="{anchor}">{text}</h3>\n<!-- /wp:heading -->')


def embed_tweet(url, lang):
    return wphtml(f'<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{url}">{url}</a></blockquote>\n'
                  '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')


def spotify(pid):
    return wphtml(f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{pid}" width="100%" height="352" '
                  'frameborder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>')


def track_table(tracks, lang):
    head = {"ja": ("No.", "曲名", "アーティスト"), "ko": ("No.", "곡명", "아티스트"), "en": ("No.", "Song", "Artist")}[lang]
    td = "border:1px solid #ddd9d3;padding:8px 10px;vertical-align:top;"
    trs = []
    for i, row in enumerate([head] + [(str(n), (t[2] if lang == "en" else t[0]), (t[3] if lang == "en" else t[1]))
                                      for n, t in enumerate(tracks, 1)]):
        bg = "background:#8a8378;color:#fff;font-weight:bold;" if i == 0 else ("" if i % 2 else "background:#f7f6f4;")
        trs.append("<tr>" + "".join(f'<td style="{td}{bg}">{c}</td>' for c in row) + "</tr>")
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>'
            + "".join(trs) + '</tbody></table></figure>\n<!-- /wp:table -->')


H2_LISTEN = {"ja": "プレイリストはどこで聴ける？", "ko": "플레이리스트는 어디서 들을 수 있을까?", "en": "Where can you listen to the playlists?"}
H2_PICKS = {"ja": "公開されたプレイリストの選曲", "ko": "공개된 플레이리스트 선곡", "en": "The playlists released so far"}
H3_TXT = {"ja": "{m}が選んだ曲({d}公開)", "ko": "{m}가 고른 곡({d} 공개)", "en": "{m}'s picks (released {d})"}
NEXT_H2 = {"ja": "企画名の「キュントゥグン」の意味は？", "ko": "기획명에 들어간 '큥두근'의 의미는?", "en": "What does \"kyun-dugeun\" mean?"}
PENDING = {"ja": "公開後に追記", "ko": "공개 후 추가 예정", "en": "To be added"}


def listen_section(lang):
    first = PLAYLISTS[0]
    svc = SERVICES[lang]
    if lang == "ja":
        return [ui.minibox(f"<strong>配信サービス:</strong>{svc}",
                           "<strong>リンク:</strong>公式Xに載る共通リンクから各サービスへ"),
                p(f"プレイリストは{mk(svc + 'の3つ')}で公開されています。",
                  f"公式Xに載っている共通リンク(1人目は{a(first['lnk'], 'YOSHIKIのリンク')})を開くと、使っているサービスを選んで飛べるしくみです。"),
                p("Spotifyでは「KO1KEYZ YOSHIKIが選ぶ 君に会う前に聴きたいキュントゥグンプレイリスト」という名前で、KO1KEYZ名義のプレイリストとして公開されていました。",
                  "なお、10月5日にデビュー記念のAWAラウンジが開かれたAWAは、今回の共通リンクの行き先には入っていません。",
                  "2人目以降のプレイリストも公開されたら、上の一覧に順番に追記していきます。")]
    if lang == "ko":
        return [ui.minibox(f"<strong>음원 서비스:</strong>{svc}"),
                p(f"플레이리스트는 {mk(svc + ' 3곳')}에서 공개되고 있어요.",
                  f"공식 X에 올라오는 공통 링크(첫 번째는 {a(first['lnk'], 'YOSHIKI 링크')})를 열면 사용하는 서비스를 골라 이동할 수 있습니다.",
                  "다음 멤버의 플레이리스트도 공개되는 대로 위 목록에 추가할게요.")]
    return [ui.minibox(f"<strong>Streaming services:</strong>{svc}"),
            p(f"The playlists are available on {mk(svc)}.",
              f"Each one is announced on the official X account with a shared link (the first is {a(first['lnk'], 'YOSHIKI’s link')}) that lets you choose your service.",
              "We'll add each member's picks to the list above as they come out.")]


def section_bounds(c, h2text):
    i = c.index(f'<h2 class="wp-block-heading">{h2text}</h2>')
    start = c.rindex("<!-- wp:heading -->", 0, i)
    return start


def first_time(c, lang):
    """配信先確定に伴う書き換え + 選曲H2の新設(初回だけ)。"""
    if f'<h2 class="wp-block-heading">{H2_PICKS[lang]}</h2>' in c:
        return c
    svc = SERVICES[lang]
    # どこで聴ける節を丸ごと差し替え
    s = section_bounds(c, H2_LISTEN[lang])
    e = section_bounds(c, NEXT_H2[lang])
    new_listen = "\n\n".join([h2(H2_LISTEN[lang])] + listen_section(lang)) + "\n\n"
    c = c[:s] + h2(H2_PICKS[lang]) + "\n\n" + new_listen + c[e:]
    reps = {
        "ja": [("告知時点では発表なし", svc),
               ("配信サービスは10月4日の告知時点では未発表", f"配信先は{svc}"),
               ("<p>プレイリストの中身はまだ分かりませんが、これまでに話していた好きな曲がヒントになりそうです。<br>",
                "<p>まだ公開前のメンバーの選曲は、これまでに話していた好きな曲がヒントになりそうです。<br>\n"
                "実際にYOSHIKIは、カバーしてみたい曲として話していた「ラベンダー」をプレイリストに入れていました。<br>"),
               ("YOSHIKI:カバーしてみたい曲としてThe Shes Gone「ラベンダー」",
                "YOSHIKI:カバーしてみたい曲としてthe shes gone「ラベンダー」→プレイリスト入り")],
        "ko": [("발표 시점에는 미공개", svc),
               ("음원 서비스는 10월 4일 시점에는 미공개", f"음원 서비스는 {svc}"),
               ("YOSHIKI: 커버해 보고 싶은 곡으로 The Shes Gone '라벤더'",
                "YOSHIKI: 커버해 보고 싶은 곡으로 the shes gone '라벤더' → 실제로 플레이리스트에 들어감")],
        "en": [("Not announced as of October 4", svc),
               ("The streaming service had not been announced as of October 4", f"Available on {svc}"),
               ("YOSHIKI: a song he'd like to cover, The Shes Gone \"Lavender\"",
                "YOSHIKI: a song he'd like to cover, the shes gone \"Lavender\" (it made his playlist)")],
    }[lang]
    for old, new in reps:
        assert c.count(old) == 1, (lang, old, c.count(old))
        c = c.replace(old, new)
    return c


def add_member(c, lang, m):
    anchor = f"playlist-{m['member'].lower()}"
    if f'id="{anchor}"' in c:
        return c, False
    li = ("ja", "ko", "en").index(lang)
    m = {**m, "table": track_table(m["tracks"], lang)}
    blocks = [h3(H3_TXT[lang].format(m=m["member"], d=m["date"][li]), anchor),
              embed_tweet(m["tweet"], lang)] + m["body"][lang](m) + [spotify(m["spotify"])]
    s = section_bounds(c, H2_LISTEN[lang])
    c = c[:s] + "\n\n".join(blocks) + "\n\n" + c[s:]
    # スケジュール表のセル
    pat = re.compile(rf'({re.escape(m["member"])}</td><td style="[^"]*">){re.escape(PENDING[lang])}(</td>)')
    c, n = pat.subn(rf'\g<1><a href="#{anchor}">{m["cell"][li]}</a>\g<2>', c)
    assert n == 1, (lang, m["member"], n)
    return c, True


def main():
    dry = "--dry" in sys.argv
    for lang, pid in IDS.items():
        r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=HA)
        r.raise_for_status()
        post = r.json()
        assert post["status"] == "publish"
        c0 = post["content"]["raw"]
        c = first_time(c0, lang)
        added = []
        for m in PLAYLISTS:
            c, ok = add_member(c, lang, m)
            if ok:
                added.append(m["member"])
        assert "<hr" not in c
        print(lang, pid, "added:", added, "chars:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", c, flags=re.S)))
        if c == c0:
            continue
        if dry:
            (ROOT / f"tmp_playlist_{lang}.html").write_text(c, encoding="utf-8")
            continue
        u = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers={**HA, "Content-Type": "application/json"},
                          data=json.dumps({"content": c}).encode("utf-8"))
        u.raise_for_status()
        print("  updated", u.json()["status"], u.json()["link"])


if __name__ == "__main__":
    main()
