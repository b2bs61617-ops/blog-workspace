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
    {
        "member": "DAIKI", "date": ("10月8日", "10월 8일", "October 8"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2107969225776415040",
        "lnk": "https://KO1KEYZ.lnk.to/DAIKI_KO1KEYZ",
        "spotify": "2TtSh54NmxcL4NBr6qrSDA",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("Neko(ねこ) - KO1KEYZ ver.", "KO1KEYZ", "Neko - KO1KEYZ ver.", "KO1KEYZ"),
            ("Doctor! Doctor!", "ZEROBASEONE", "Doctor! Doctor!", "ZEROBASEONE"),
            ("キミアトラクション", "Hey! Say! JUMP", "Kimi Attraction", "Hey! Say! JUMP"),
            ("Lovin' you", "King & Prince", "Lovin' you", "King & Prince"),
            ("White Love", "Hey! Say! JUMP", "White Love", "Hey! Say! JUMP"),
            ("Call me", "SixTONES", "Call me", "SixTONES"),
            ("Luv Bias", "Kis-My-Ft2", "Luv Bias", "Kis-My-Ft2"),
            ("DEAR MY LOVER", "Hey! Say! JUMP", "DEAR MY LOVER", "Hey! Say! JUMP"),
            ("恋をするんだ", "Hey! Say! JUMP", "Koi wo Surunda", "Hey! Say! JUMP"),
        ],
        "cell": ("Hey! Say! JUMPの曲4曲ほか全10曲", "Hey! Say! JUMP 4곡 등 총 10곡",
                 "10 songs, incl. 4 by Hey! Say! JUMP"),
        # 予想の手がかり節の行に結果を書き足す
        "reps": {
            "ja": [("DAIKI:カラオケでSixTONES「Imitation Rain」、Hey! Say! JUMP「ウィークエンダー」</li>",
                    "DAIKI:カラオケでSixTONES「Imitation Rain」、Hey! Say! JUMP「ウィークエンダー」→曲は違ったが、SixTONESとHey! Say! JUMPはプレイリスト入り</li>")],
            "ko": [("DAIKI: 노래방에서 SixTONES 'Imitation Rain', Hey! Say! JUMP '위켄더'</li>",
                    "DAIKI: 노래방에서 SixTONES 'Imitation Rain', Hey! Say! JUMP '위켄더' → 곡은 달랐지만 SixTONES와 Hey! Say! JUMP는 플레이리스트에 들어감</li>")],
            "en": [("DAIKI: at karaoke, SixTONES \"Imitation Rain\" and Hey! Say! JUMP \"Weekender\"</li>",
                    "DAIKI: at karaoke, SixTONES \"Imitation Rain\" and Hey! Say! JUMP \"Weekender\" (different songs, but both artists made his playlist)</li>")],
        },
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>Hey! Say! JUMPの曲が4曲"),
                p("2人目は、ちょうど公開日の10月8日が22歳の誕生日だったDAIKI。",
                  "選んだのは全10曲で、1曲目は表題曲「KO1KEYZ」、2曲目はKO1KEYZとして歌う「Neko(ねこ) - KO1KEYZ ver.」です。",
                  "YOSHIKIが2曲目に「Key of Story」を入れていたのに対して、DAIKIは「ねこ」を選んでいて、ここから早くも個性が分かれました。"),
                m["table"],
                p(f"ひと目で分かるのが、{mk('Hey! Say! JUMPの曲が4曲も入っている')}こと。",
                  "「キミアトラクション」「White Love」「DEAR MY LOVER」「恋をするんだ」と、10曲のうち4曲がHey! Say! JUMPでした。"),
                p("さらにKing & Prince「Lovin' you」、SixTONES「Call me」、Kis-My-Ft2「Luv Bias」も入っていて、KO1KEYZ以外の8曲のうち7曲が日本の男性アイドルグループの曲です。",
                  "トーク会ではカラオケで歌う曲としてSixTONES「Imitation Rain」とHey! Say! JUMP「ウィークエンダー」を挙げていたので、曲は違ってもアーティストはぴったり重なりました。"),
                p("残りの1曲はZEROBASEONEの「Doctor! Doctor!」で、ここだけK-POPです。",
                  "「White Love」「DEAR MY LOVER」「恋をするんだ」と恋の曲が並んでいて、こちらもテーマどおりの約39分のプレイリストになっています。",
                  f"聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>Hey! Say! JUMP 곡이 4곡"),
                p("두 번째 주자는 공개일인 10월 8일이 마침 22번째 생일이었던 DAIKI예요.",
                  "총 10곡으로, 1번은 타이틀곡 'KO1KEYZ', 2번은 KO1KEYZ가 부른 'Neko(ねこ) - KO1KEYZ ver.'입니다."),
                m["table"],
                p(f"가장 눈에 띄는 건 {mk('Hey! Say! JUMP 곡이 4곡이나 들어 있다는 점')}이에요.",
                  "여기에 King & Prince, SixTONES, Kis-My-Ft2까지, KO1KEYZ 곡을 뺀 8곡 중 7곡이 일본 남자 아이돌 그룹 곡이에요.",
                  "토크회에서 노래방 곡으로 SixTONES 'Imitation Rain'과 Hey! Say! JUMP '위켄더'를 꼽았었는데, 곡은 달라도 아티스트는 그대로 겹쳤습니다."),
                p("나머지 1곡은 ZEROBASEONE의 'Doctor! Doctor!'로, 약 39분 길이의 플레이리스트예요.",
                  f"{a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>4 songs by Hey! Say! JUMP"),
                p("Second up was DAIKI, whose playlist dropped on October 8, his 22nd birthday.",
                  "He picked 10 songs, opening with the title track \"KO1KEYZ\" followed by \"Neko - KO1KEYZ ver.\""),
                m["table"],
                p(f"The obvious standout: {mk('four of the ten songs are by Hey! Say! JUMP')}.",
                  "Add King & Prince, SixTONES and Kis-My-Ft2, and seven of the eight non-KO1KEYZ songs come from Japanese boy groups.",
                  "At a fan talk event he'd named SixTONES \"Imitation Rain\" and Hey! Say! JUMP \"Weekender\" as karaoke picks, so the songs differ but the artists match."),
                p("The one K-pop pick is ZEROBASEONE's \"Doctor! Doctor!\", rounding out a roughly 39-minute playlist.",
                  f"Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
    {
        "member": "SIYOUNG", "date": ("10月9日", "10월 9일", "October 9"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2108331605022462339",
        "lnk": "https://ko1keyz.lnk.to/SIYOUNG_KO1KEYZ",
        "spotify": "5JSNbgJ5vGTsefDWhzttVU",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("BLACK ANGEL - KO1KEYZ ver.", "KO1KEYZ", "BLACK ANGEL - KO1KEYZ ver.", "KO1KEYZ"),
            ("Human Nature", "Michael Jackson", "Human Nature", "Michael Jackson"),
            ("Is There Someone Else?", "The Weeknd", "Is There Someone Else?", "The Weeknd"),
            ("Fantasy", "Nuz, Lúcia", "Fantasy", "Nuz, Lúcia"),
            ("Take My Breath", "The Weeknd", "Take My Breath", "The Weeknd"),
            ("You Rock My World", "Michael Jackson", "You Rock My World", "Michael Jackson"),
            ("Wanna Love You Girl - Main", "Robin Thicke, Pharrell Williams", "Wanna Love You Girl - Main", "Robin Thicke, Pharrell Williams"),
            ("Timeless (feat Playboi Carti)", "The Weeknd, Playboi Carti", "Timeless (feat Playboi Carti)", "The Weeknd, Playboi Carti"),
            ("I'm The Man", "ADÉLA", "I'm The Man", "ADÉLA"),
        ],
        "cell": ("The Weeknd・マイケル・ジャクソンほか全10曲", "The Weeknd・마이클 잭슨 등 총 10곡",
                 "10 songs, incl. The Weeknd and Michael Jackson"),
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>KO1KEYZ以外の8曲がすべて洋楽"),
                p("3人目はSIYOUNG。",
                  "選んだのは全10曲で、1曲目は表題曲「KO1KEYZ」、2曲目は「BLACK ANGEL - KO1KEYZ ver.」です。",
                  "「BLACK ANGEL」は1ST FAN MEETINGでSIYOUNGを含む6人が披露した曲で、2曲目はYOSHIKIが「Key of Story」、DAIKIが「ねこ」と、ここまで3人とも違う曲を選んでいます。"),
                m["table"],
                p(f"YOSHIKIは日本のバンド、DAIKIは日本の男性アイドルグループが中心でしたが、SIYOUNGは{mk('KO1KEYZ以外の8曲がすべて洋楽')}でした。",
                  "The Weekndが「Is There Someone Else?」「Take My Breath」「Timeless」の3曲、マイケル・ジャクソンが「Human Nature」「You Rock My World」の2曲で、この2人だけで半分を占めています。"),
                p("ほかにもRobin ThickeとPharrell Williamsの「Wanna Love You Girl」など、R&Bやダンスポップ寄りの曲がそろいました。",
                  "自分のことを「パフォーマンスリーダー」と話していたSIYOUNGらしく、踊りたくなるようなリズムの曲が多い選曲です。"),
                p("「You Rock My World」「Wanna Love You Girl」と恋を歌う曲も入っていて、全部で約39分のプレイリストです。",
                  f"聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>KO1KEYZ 곡을 뺀 8곡이 모두 팝송"),
                p("세 번째 주자는 SIYOUNG이에요.",
                  "총 10곡으로, 1번은 타이틀곡 'KO1KEYZ', 2번은 'BLACK ANGEL - KO1KEYZ ver.'입니다.",
                  "'BLACK ANGEL'은 1ST FAN MEETING에서 SIYOUNG을 포함한 6명이 선보인 곡이에요."),
                m["table"],
                p(f"가장 눈에 띄는 건 {mk('KO1KEYZ 곡을 뺀 8곡이 모두 팝송')}이라는 점이에요.",
                  "The Weeknd 3곡, 마이클 잭슨 2곡으로 이 두 아티스트가 절반을 차지하고, R&B와 댄스 팝 느낌의 곡이 많아요.",
                  "스스로 '퍼포먼스 리더'라고 말했던 SIYOUNG다운 선곡입니다."),
                p("약 39분 길이의 플레이리스트로, "
                  f"{a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>all 8 non-KO1KEYZ songs are Western pop and R&amp;B"),
                p("Third up was SIYOUNG.",
                  "He picked 10 songs, opening with the title track \"KO1KEYZ\" followed by \"BLACK ANGEL - KO1KEYZ ver.\", a song he performed with five other members at the 1ST FAN MEETING."),
                m["table"],
                p(f"YOSHIKI leaned on Japanese bands and DAIKI on Japanese boy groups, but {mk('every one of SIYOUNG’s eight other picks is a Western song')}.",
                  "The Weeknd has three songs and Michael Jackson two, so those two artists alone fill half the list."),
                p("With Robin Thicke and Pharrell Williams' \"Wanna Love You Girl\" also in the mix, it's a groove-heavy, roughly 39-minute playlist that suits the self-described \"performance leader\".",
                  f"Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
    {
        "member": "SHINHAENG", "date": ("10月10日", "10월 10일", "October 10"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2108693992942817294",
        "lnk": "https://ko1keyz.lnk.to/SHINHAENG_KO1KEYZ",
        "spotify": "3Ydv1zebp3qH4rXroIl1t8",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("Key of Story", "KO1KEYZ", "Key of Story", "KO1KEYZ"),
            ("something between us (Romance 101 X george)", "george", "something between us (Romance 101 X george)", "george"),
            ("beside you", "keshi", "beside you", "keshi"),
            ("love.", "wave to earth", "love.", "wave to earth"),
            ("Forever Has Always Been", "Redoor", "Forever Has Always Been", "Redoor"),
            ("一目惚れ", "舟津真翔", "Hitomebore (Love at First Sight)", "舟津真翔"),
            ("Vanilla Days", "LNGSHOT", "Vanilla Days", "LNGSHOT"),
            ("Can't Stop (Seungmin, I.N)", "Stray Kids", "Can't Stop (Seungmin, I.N)", "Stray Kids"),
            ("Best Luck", "CHEN", "Best Luck", "CHEN"),
        ],
        "cell": ("wave to earth「love.」・Stray Kidsほか全10曲", "wave to earth 'love.'・Stray Kids 등 총 10곡",
                 '10 songs, incl. wave to earth "love." and Stray Kids'),
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>恋を思わせるタイトルが並ぶ、しっとりめの選曲"),
                p("4人目は、韓国・木浦出身のSHINHAENG。",
                  "選んだのは全10曲で、1曲目は表題曲「KO1KEYZ」、2曲目はカップリング曲「Key of Story」です。",
                  "2曲目はここまでYOSHIKIが「Key of Story」、DAIKIが「ねこ」、SIYOUNGが「BLACK ANGEL」とばらばらでしたが、SHINHAENGはYOSHIKIと同じ「Key of Story」を選びました。"),
                m["table"],
                p(f"目を引くのは、{mk('「beside you」「love.」「一目惚れ」と、恋を思わせるタイトルの曲がずらりと並んでいる')}ところ。",
                  "「something between us」「Forever Has Always Been」も含めて、テーマの「君に会う前に聴きたい」にいちばんまっすぐ答えたような選曲です。"),
                p("アーティストを見ると、韓国のバンドwave to earth、アメリカで活動するkeshi、Stray Kids(スンミンとアイエンのユニット曲)、EXOのCHENと、国も雰囲気もさまざま。",
                  "その中で日本語の曲は、舟津真翔の「一目惚れ」の1曲だけでした。"),
                p("SIYOUNGのダンス寄りの選曲とは反対に、ゆったり聴けるR&Bやバンドの曲が中心で、全部で約36分と、ここまでの4人ではいちばん短いプレイリストです。",
                  f"聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>사랑을 떠올리게 하는 제목이 이어지는 잔잔한 선곡"),
                p("네 번째 주자는 목포 출신 SHINHAENG이에요.",
                  "총 10곡으로, 1번은 타이틀곡 'KO1KEYZ', 2번은 커플링곡 'Key of Story'입니다.",
                  "2번 트랙에 'Key of Story'를 고른 건 YOSHIKI에 이어 두 번째예요."),
                m["table"],
                p(f"가장 눈에 띄는 건 {mk('beside you, love., 一目惚れ(첫눈에 반함)처럼 사랑을 떠올리게 하는 제목이 이어진다는 점')}이에요.",
                  "wave to earth, keshi, Stray Kids(승민·아이엔 유닛곡), EXO 첸 등 아티스트도 다양하고, 일본어 곡은 舟津真翔의 '一目惚れ' 1곡뿐이에요."),
                p("잔잔한 R&B와 밴드 곡 위주로, 지금까지 4명 중 가장 짧은 약 36분 길이의 플레이리스트예요.",
                  f"{a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>a mellow list full of love-song titles"),
                p("Fourth up was SHINHAENG, from Mokpo, South Korea.",
                  "He picked 10 songs, opening with the title track \"KO1KEYZ\" followed by the B-side \"Key of Story\", the same second track YOSHIKI chose."),
                m["table"],
                p(f"The standout: {mk('titles like \"beside you\", \"love.\" and \"Hitomebore\" (Love at First Sight)')}, which make this the most on-theme list yet for \"songs to hear before meeting you\".",
                  "The artists range from Korean band wave to earth and keshi to Stray Kids (a Seungmin and I.N unit track) and EXO's CHEN, with just one Japanese-language song."),
                p("Built around laid-back R&amp;B and band tracks, it runs about 36 minutes, the shortest of the four so far.",
                  f"Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
    {
        "member": "YURA", "date": ("10月11日", "10월 11일", "October 11"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2109056385040191575",
        "lnk": "https://ko1keyz.lnk.to/YURA_KO1KEYZ",
        "spotify": "5Z8QIeeK3VULxDDX4aPHIG",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("Key of Story", "KO1KEYZ", "Key of Story", "KO1KEYZ"),
            ("Make It Right", "BTS", "Make It Right", "BTS"),
            ("Love", "Kaive Noir", "Love", "Kaive Noir"),
            ("Photograph", "Ed Sheeran", "Photograph", "Ed Sheeran"),
            ("恋唄", "清水翔太", "Koiuta", "Shota Shimizu"),
            ("ライラック", "Mrs. GREEN APPLE", "Lilac", "Mrs. GREEN APPLE"),
            ("Best Part", "Joseph Vincent", "Best Part", "Joseph Vincent"),
            ("しわあわせ", "Vaundy", "Shiwaawase", "Vaundy"),
            ("beside you", "keshi", "beside you", "keshi"),
        ],
        "cell": ("BTS・Mrs. GREEN APPLE・Vaundyほか全10曲", "BTS・Mrs. GREEN APPLE・Vaundy 등 총 10곡",
                 "10 songs, incl. BTS, Mrs. GREEN APPLE and Vaundy"),
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>K-POP・洋楽・J-POPがほどよく混ざった選曲"),
                p("5人目は、茨城県出身のYURA。",
                  "選んだのは全10曲で、1曲目は表題曲「KO1KEYZ」、2曲目はカップリング曲「Key of Story」です。",
                  "2曲目に「Key of Story」を選んだのは、YOSHIKI・SHINHAENGに続いて3人目になりました。"),
                m["table"],
                p(f"ここまでの4人は、日本のバンド(YOSHIKI)、日本の男性アイドルグループ(DAIKI)、洋楽(SIYOUNG)、しっとりした恋の曲(SHINHAENG)と色がはっきり分かれていましたが、YURAは{mk('K-POP・洋楽・J-POPがほどよく混ざった')}プレイリストです。",
                  "日本語の曲は清水翔太「恋唄」、Mrs. GREEN APPLE「ライラック」、Vaundy「しわあわせ」の3曲で、ほかはBTS「Make It Right」やEd Sheeran「Photograph」などが並びました。"),
                p("BTSの「Make It Right」はEd Sheeranが制作に関わった曲なので、3曲目と5曲目はEd Sheeranつながりになっています。",
                  "デビュー前に韓国のグループPICKUSで活動していたYURAらしく、日本と韓国、そして英語圏の曲を行き来するような並びです。"),
                p(f"もうひとつ目を引くのが、最後の10曲目。{mk('keshiの「beside you」は、前日のSHINHAENGも選んでいた曲')}で、KO1KEYZの曲以外でメンバーの選曲がかぶったのはこれが初めてです。",
                  "全部で約38分のプレイリストで、聴くときは"
                  f"{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>K-POP・팝송・J-POP이 고르게 섞인 선곡"),
                p("다섯 번째 주자는 이바라키현 출신 YURA예요.",
                  "총 10곡으로, 1번은 타이틀곡 'KO1KEYZ', 2번은 커플링곡 'Key of Story'입니다.",
                  "2번 트랙에 'Key of Story'를 고른 건 YOSHIKI, SHINHAENG에 이어 세 번째예요."),
                m["table"],
                p(f"가장 눈에 띄는 건 {mk('K-POP・팝송・J-POP이 고르게 섞여 있다는 점')}이에요.",
                  "일본어 곡은 시미즈 쇼타 '恋唄', Mrs. GREEN APPLE '라일락', Vaundy 'しわあわせ' 3곡이고, BTS 'Make It Right'와 에드 시런 'Photograph'도 들어 있어요.",
                  "'Make It Right'는 에드 시런이 제작에 참여한 곡이라 3번과 5번이 에드 시런으로 이어집니다."),
                p(f"10번 트랙 {mk('keshi의 beside you는 전날 SHINHAENG도 고른 곡')}으로, KO1KEYZ 곡을 빼고 멤버끼리 선곡이 겹친 건 이번이 처음이에요.",
                  f"약 38분 길이의 플레이리스트로, {a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>an even mix of K-pop, Western pop and J-pop"),
                p("Fifth up was YURA, from Ibaraki Prefecture.",
                  "He picked 10 songs, opening with the title track \"KO1KEYZ\" followed by \"Key of Story\", making him the third member, after YOSHIKI and SHINHAENG, to choose it as his second track."),
                m["table"],
                p(f"Where the first four leaned clearly one way, {mk('YURA mixes K-pop, Western pop and J-pop')}.",
                  "The three Japanese songs are Shota Shimizu's \"Koiuta\", Mrs. GREEN APPLE's \"Lilac\" and Vaundy's \"Shiwaawase\", alongside BTS's \"Make It Right\" and Ed Sheeran's \"Photograph\".",
                  "Ed Sheeran co-wrote \"Make It Right\", so tracks 3 and 5 share a link."),
                p(f"The closer, {mk('keshi’s \"beside you\", was also on SHINHAENG’s list the day before')}, the first time two members picked the same non-KO1KEYZ song.",
                  f"It runs about 38 minutes. Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
    {
        "member": "RYUJI", "date": ("10月12日", "10월 12일", "October 12"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2109418770112352298",
        "lnk": "https://ko1keyz.lnk.to/RYUJI_KO1KEYZ",
        "spotify": "6ytjzHYTvGhmFoyZx66eII",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("Key of Story", "KO1KEYZ", "Key of Story", "KO1KEYZ"),
            ("ALL MINE", "Kenya Fujita", "ALL MINE", "Kenya Fujita"),
            ("夢中", "BE:FIRST", "Muchu", "BE:FIRST"),
            ("Glowing", "PSYCHIC FEVER from EXILE TRIBE", "Glowing", "PSYCHIC FEVER from EXILE TRIBE"),
            ("LOVE RAIN ～恋の雨～", "久保田利伸", "LOVE RAIN ~Koi no Ame~", "Toshinobu Kubota"),
            ("Plumeria", "林 和希", "Plumeria", "Kazuki Hayashi"),
            ("Sugar Honey", "WOLF HOWL HARMONY from EXILE TRIBE", "Sugar Honey", "WOLF HOWL HARMONY from EXILE TRIBE"),
            ("WISH", "INI", "WISH", "INI"),
            ("LOOP", "SIRUP", "LOOP", "SIRUP"),
        ],
        "cell": ("WOLF HOWL HARMONY・INI・BE:FIRSTほか全10曲", "WOLF HOWL HARMONY・INI・BE:FIRST 등 총 10곡",
                 "10 songs, incl. WOLF HOWL HARMONY, INI and BE:FIRST"),
        "reps": {
            "ja": [("RYUJI:カラオケの十八番は中西保志「最後の雨」、歌ってほしい曲はAAA「風に薫る夏の記憶」",
                    "RYUJI:カラオケの十八番は中西保志「最後の雨」、歌ってほしい曲はAAA「風に薫る夏の記憶」→どちらも入らなかったが、雨の曲として久保田利伸「LOVE RAIN ～恋の雨～」がプレイリスト入り")],
            "ko": [("RYUJI: 노래방 애창곡은 나카니시 야스시 '마지막 비(最後の雨)', 불러 줬으면 하는 곡은 AAA '바람에 실린 여름의 기억'",
                    "RYUJI: 노래방 애창곡은 나카니시 야스시 '마지막 비(最後の雨)', 불러 줬으면 하는 곡은 AAA '바람에 실린 여름의 기억' → 둘 다 들어가지 않았지만, 비 노래로 쿠보타 토시노부 'LOVE RAIN ～恋の雨～'가 플레이리스트에 들어감")],
            "en": [("RYUJI: his karaoke go-to is Yasushi Nakanishi \"Saigo no Ame\"; a song he'd like sung to him is AAA \"Kaze ni Kaoru Natsu no Kioku\"",
                    "RYUJI: his karaoke go-to is Yasushi Nakanishi \"Saigo no Ame\"; a song he'd like sung to him is AAA \"Kaze ni Kaoru Natsu no Kioku\" (neither made it, but another rain song, Toshinobu Kubota's \"LOVE RAIN ~Koi no Ame~\", did)")],
        },
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>日本のダンス&ボーカルグループとR&Bが中心、兄のグループと言われるWOLF HOWL HARMONYの曲も"),
                p("6人目は、埼玉県出身のRYUJI。",
                  "選んだのは全10曲で、1曲目は表題曲「KO1KEYZ」、2曲目はカップリング曲「Key of Story」です。",
                  "2曲目に「Key of Story」を選んだのは、YOSHIKI・SHINHAENG・YURAに続いて4人目になりました。"),
                m["table"],
                p(f"KO1KEYZ以外の8曲は、{mk('すべて日本のアーティストの曲')}。",
                  "BE:FIRST「夢中」、PSYCHIC FEVER「Glowing」、WOLF HOWL HARMONY「Sugar Honey」、INI「WISH」と、日本のダンス&ボーカルグループの曲が4曲並びました。",
                  "そこに久保田利伸「LOVE RAIN ～恋の雨～」やSIRUP「LOOP」といったR&Bの曲が加わって、歌とグルーヴを大事にした大人っぽい選曲になっています。"),
                p(f"いちばん気になるのは、8曲目のWOLF HOWL HARMONY「Sugar Honey」。{mk('WOLF HOWL HARMONYのRYOJIさんは、RYUJIのお兄さんだと伝えられています')}。",
                  "公式に兄弟だと発表されたわけではありませんが、もしそうならお兄さんのグループの曲を自分のプレイリストに入れたことになり、ファンの間でも話題になりそうです。",
                  "PSYCHIC FEVERも同じEXILE TRIBEのグループで、LDH系の曲が2曲入っています。"),
                p("9曲目のINIは、同じ「PRODUCE 101 JAPAN」シリーズのSEASON2から生まれたグループ。",
                  "トーク会では、INIで仲良くなりたいメンバーとして理人さんの名前を挙げていたこともあり、先輩グループの曲を選んだのもRYUJIらしいところです。"),
                p("カラオケの十八番だと話していた中西保志「最後の雨」は入りませんでしたが、代わりに同じ「雨」がテーマの「LOVE RAIN ～恋の雨～」が選ばれていました。",
                  f"全部で約38分のプレイリストで、聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>일본 댄스&보컬 그룹과 R&B 중심, 형의 그룹으로 알려진 WOLF HOWL HARMONY 곡도"),
                p("여섯 번째 주자는 사이타마현 출신 RYUJI예요.",
                  "총 10곡으로, 1번은 타이틀곡 'KO1KEYZ', 2번은 커플링곡 'Key of Story'입니다.",
                  "2번 트랙에 'Key of Story'를 고른 건 YOSHIKI, SHINHAENG, YURA에 이어 네 번째예요."),
                m["table"],
                p(f"KO1KEYZ 곡을 뺀 8곡은 {mk('모두 일본 아티스트의 곡')}이에요.",
                  "BE:FIRST, PSYCHIC FEVER, WOLF HOWL HARMONY, INI까지 일본 댄스&보컬 그룹 곡이 4곡이고, 쿠보타 토시노부 'LOVE RAIN ～恋の雨～'와 SIRUP 'LOOP' 같은 R&B 곡이 더해졌어요."),
                p(f"특히 8번 트랙 WOLF HOWL HARMONY 'Sugar Honey'가 눈에 띄어요. {mk('WOLF HOWL HARMONY의 RYOJI가 RYUJI의 형이라고 알려져 있기 때문')}이에요.",
                  "공식적으로 형제라고 발표된 건 아니지만, 사실이라면 형의 그룹 곡을 직접 고른 셈이에요."),
                p("9번 트랙 INI는 같은 'PRODUCE 101 JAPAN' 시리즈 SEASON2에서 탄생한 그룹으로, RYUJI는 토크회에서 INI 중 친해지고 싶은 멤버로 리히토를 꼽은 적이 있어요.",
                  f"약 38분 길이의 플레이리스트로, {a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>Japanese dance-vocal groups and R&B, including WOLF HOWL HARMONY, reportedly his brother's group"),
                p("Sixth up was RYUJI, from Saitama Prefecture.",
                  "He picked 10 songs, opening with \"KO1KEYZ\" and \"Key of Story\", making him the fourth member, after YOSHIKI, SHINHAENG and YURA, to choose it as his second track."),
                m["table"],
                p(f"{mk('All eight non-KO1KEYZ songs are by Japanese artists')}.",
                  "Four come from Japanese dance-vocal groups: BE:FIRST, PSYCHIC FEVER, WOLF HOWL HARMONY and INI, with R&B from Toshinobu Kubota and SIRUP rounding it out."),
                p(f"The standout is track 8, WOLF HOWL HARMONY's \"Sugar Honey\": {mk('the group’s RYOJI is reported to be RYUJI’s older brother')}.",
                  "It hasn't been officially confirmed, but if true, he put his brother's group on his own list."),
                p("INI, on track 9, came out of PRODUCE 101 JAPAN SEASON2, the same audition series, and RYUJI has named INI's Rihito as a member he'd like to get closer to.",
                  f"It runs about 38 minutes. Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
    {
        "member": "KEITO", "date": ("10月13日", "10월 13일", "October 13"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2109781160540639409",
        "lnk": "https://ko1keyz.lnk.to/KEITO_KO1KEYZ",
        "spotify": "13j7LiZNDMZhEEqpovjQnU",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("Neko(ねこ) - KO1KEYZ ver.", "KO1KEYZ", "Neko - KO1KEYZ ver.", "KO1KEYZ"),
            ("Love 119", "RIIZE", "Love 119", "RIIZE"),
            ("Spring Snow", "10CM", "Spring Snow", "10CM"),
            ("Even if we disappear", "DAWN", "Even if we disappear", "DAWN"),
            ("WANTCHU", "keshi", "WANTCHU", "keshi"),
            ("Focus", "Shota Aratani, Mamiko Suzuki, TOSHIKI HAYASHI(%C)", "Focus", "Shota Aratani, Mamiko Suzuki, TOSHIKI HAYASHI(%C)"),
            ("After Party", "yonawo", "After Party", "yonawo"),
            ("携帯電話", "RADWIMPS", "Keitai Denwa", "RADWIMPS"),
            ("結び", "Ayumu Imazu", "Musubi", "Ayumu Imazu"),
        ],
        "cell": ("RIIZE・keshi・RADWIMPSほか全10曲", "RIIZE・keshi・RADWIMPS 등 총 10곡",
                 "10 songs, incl. RIIZE, keshi and RADWIMPS"),
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>K-POP・洋楽・J-POPをバランスよく、keshiは3人連続で登場"),
                p("7人目は、高知県出身で最年長のKEITO。",
                  "選んだのは全10曲で、1曲目は表題曲「KO1KEYZ」、2曲目は「Neko(ねこ) - KO1KEYZ ver.」です。",
                  "2曲目に「ねこ」を選んだのは、誕生日に公開されたDAIKIに続いて2人目になりました。"),
                m["table"],
                p(f"KO1KEYZ以外の8曲は、{mk('韓国・海外・日本のアーティストがほどよく混ざった選曲')}。",
                  "RIIZE「Love 119」、10CM「Spring Snow」、DAWN「Even if we disappear」と、前半には韓国のアーティストの曲が3曲並びました。",
                  "後半はyonawo「After Party」、RADWIMPS「携帯電話」、Ayumu Imazu「結び」と日本の曲が続き、落ち着いた雰囲気で締めくくっています。"),
                p(f"気になるのは、6曲目のkeshi「WANTCHU」。{mk('keshiはSHINHAENG・YURAに続いて3人目の登場')}です。",
                  "ただ、2人が選んだのはどちらも「beside you」で、KEITOは別の曲を選んでいました。",
                  "メンバーの間でkeshiが人気なのが、プレイリストからも伝わってきます。"),
                p("ラストの曲が「結び」なのも、プレイリストの締めくくりらしいところ。",
                  f"全部で約36分のプレイリストで、聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>K-POP・팝・J-POP을 고루 섞은 선곡, keshi는 세 명 연속 등장"),
                p("일곱 번째 주자는 고치현 출신이자 최연장자인 KEITO예요.",
                  "총 10곡으로, 1번은 타이틀곡 'KO1KEYZ', 2번은 'Neko(ねこ) - KO1KEYZ ver.'입니다.",
                  "2번 트랙에 '네코'를 고른 건 생일에 공개된 DAIKI에 이어 두 번째예요."),
                m["table"],
                p(f"KO1KEYZ 곡을 뺀 8곡은 {mk('한국・해외・일본 아티스트를 고루 섞은 선곡')}이에요.",
                  "앞쪽에는 RIIZE 'Love 119', 10CM 'Spring Snow', DAWN 'Even if we disappear'까지 한국 아티스트 곡이 3곡, 뒤쪽에는 yonawo, RADWIMPS, Ayumu Imazu의 일본 곡이 이어져요."),
                p(f"6번 트랙 keshi 'WANTCHU'도 눈에 띄어요. {mk('keshi는 SHINHAENG, YURA에 이어 세 번째 등장')}이에요.",
                  "다만 두 사람은 모두 'beside you'를 골랐고, KEITO는 다른 곡을 골랐어요."),
                p(f"약 36분 길이의 플레이리스트로, {a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>A balanced mix of K-pop, Western and Japanese songs, with keshi showing up for a third member in a row"),
                p("Seventh up was KEITO, the oldest member, from Kochi Prefecture.",
                  "He picked 10 songs, opening with \"KO1KEYZ\" and \"Neko - KO1KEYZ ver.\", making him the second member, after DAIKI, to choose it as his second track."),
                m["table"],
                p(f"{mk('The eight non-KO1KEYZ songs mix Korean, Western and Japanese artists')}.",
                  "The first half features three Korean acts: RIIZE, 10CM and DAWN. The second half turns to Japanese songs from yonawo, RADWIMPS and Ayumu Imazu."),
                p(f"Track 6 is keshi's \"WANTCHU\": {mk('keshi has now appeared on three lists in a row, after SHINHAENG and YURA')}.",
                  "Both of them picked \"beside you\", though, while KEITO went with a different song."),
                p(f"It runs about 36 minutes. Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
    {
        "member": "ISSA", "date": ("10月14日", "10월 14일", "October 14"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2110143550914732384",
        "lnk": "https://ko1keyz.lnk.to/ISSA_KO1KEYZ",
        "spotify": "42tcH7AVdLok8pZwP4ztqK",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("Key of Story", "KO1KEYZ", "Key of Story", "KO1KEYZ"),
            ("Intentions", "Justin Bieber, Quavo", "Intentions", "Justin Bieber, Quavo"),
            ("I Would", "Justin Bieber", "I Would", "Justin Bieber"),
            ("Home To Mama", "Justin Bieber, Cody Simpson", "Home To Mama", "Justin Bieber, Cody Simpson"),
            ("Thinking out Loud", "Ed Sheeran", "Thinking out Loud", "Ed Sheeran"),
            ("I Like Me Better", "Lauv", "I Like Me Better", "Lauv"),
            ("I'm Gonna Love You", "D.O., Wonstein", "I'm Gonna Love You", "D.O., Wonstein"),
            ("君が好き", "清水翔太", "Kimi ga Suki", "Shota Shimizu"),
            ("花束", "back number", "Hanataba", "back number"),
        ],
        "cell": ("ジャスティン・ビーバー・back numberほか全10曲", "Justin Bieber・back number 등 총 10곡",
                 "10 songs, incl. Justin Bieber and back number"),
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>ジャスティン・ビーバーが3曲、締めは清水翔太とback numberのラブソング"),
                p("8人目は、群馬県出身で野球少年だったISSA。",
                  "選んだのは全10曲で、1曲目は表題曲「KO1KEYZ」、2曲目は「Key of Story」です。",
                  "2曲目に「Key of Story」を選んだのは、YOSHIKI・SHINHAENG・YURA・RYUJIに続いて5人目になりました。"),
                m["table"],
                p(f"まず目を引くのは、{mk('ジャスティン・ビーバーの曲が3曲続けて並んでいる')}ところ。",
                  "3曲目のQuavoとの「Intentions」から、「I Would」、Cody Simpsonとの「Home To Mama」まで、同じアーティストの曲を3曲連続で並べたのはISSAが初めてです(DAIKIのHey! Say! JUMPやSIYOUNGのThe Weekndは間に別の曲が入っていました)。",
                  "そのあとにはEd Sheeran「Thinking out Loud」、Lauv「I Like Me Better」と、甘いラブソングが続きます。"),
                p(f"8曲目はD.O.とWonsteinの「I'm Gonna Love You」で、{mk('韓国のアーティストの曲はこの1曲だけ')}。",
                  "最後の2曲は清水翔太「君が好き」、back number「花束」と、日本語のラブソングで締めくくっています。"),
                p(f"重なりで見ると、{mk('Ed Sheeranと清水翔太は、YURAのプレイリストにも入っていたアーティスト')}です。",
                  "ただ、YURAが選んだのは「Photograph」と「恋唄」で、曲そのものはどちらも別でした。",
                  "デビュー準備の間に仲良くなったと話していた2人なので、音楽の好みも近いのかもしれません。"),
                p("タイトルに「好き」「Love」が入る曲が多く、企画名の「キュントゥグン」にいちばん素直に向き合ったような選曲です。",
                  f"全部で約37分のプレイリストで、聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>저스틴 비버 3곡, 마지막은 시미즈 쇼타와 back number의 러브송"),
                p("여덟 번째 주자는 군마현 출신이자 야구 소년이었던 ISSA예요.",
                  "총 10곡으로, 1번은 타이틀곡 'KO1KEYZ', 2번은 'Key of Story'입니다.",
                  "2번 트랙에 'Key of Story'를 고른 건 YOSHIKI, SHINHAENG, YURA, RYUJI에 이어 다섯 번째예요."),
                m["table"],
                p(f"가장 눈에 띄는 건 {mk('저스틴 비버의 곡이 3곡 연속으로 들어간')} 점이에요.",
                  "Quavo와 함께한 'Intentions', 'I Would', Cody Simpson과 함께한 'Home To Mama'까지, 같은 아티스트의 곡을 3곡 연속으로 배치한 건 ISSA가 처음이에요.",
                  "이어서 Ed Sheeran 'Thinking out Loud', Lauv 'I Like Me Better' 같은 달달한 러브송이 이어져요."),
                p(f"8번 트랙은 디오(D.O.)와 원슈타인의 'I'm Gonna Love You'로, {mk('한국 아티스트 곡은 이 1곡뿐')}이에요.",
                  "마지막 두 곡은 시미즈 쇼타 '君が好き(너를 좋아해)', back number '花束(꽃다발)'로 일본어 러브송으로 마무리했어요."),
                p(f"{mk('Ed Sheeran과 시미즈 쇼타는 YURA의 플레이리스트에도 있었던 아티스트')}예요.",
                  "다만 YURA가 고른 곡은 'Photograph'와 '恋唄'로, 곡 자체는 달랐어요."),
                p(f"약 37분 길이의 플레이리스트로, {a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>Three Justin Bieber songs, closing with love songs by Shota Shimizu and back number"),
                p("Eighth up was ISSA, a former youth baseball player from Gunma Prefecture.",
                  "He picked 10 songs, opening with \"KO1KEYZ\" and \"Key of Story\", making him the fifth member, after YOSHIKI, SHINHAENG, YURA and RYUJI, to choose it as his second track."),
                m["table"],
                p(f"{mk('Three Justin Bieber songs come back to back')}: \"Intentions\" with Quavo, \"I Would\" and \"Home To Mama\" with Cody Simpson.",
                  "He's the first member to put three songs by the same artist in a row. Ed Sheeran's \"Thinking out Loud\" and Lauv's \"I Like Me Better\" keep the sweet mood going."),
                p(f"Track 8, \"I'm Gonna Love You\" by D.O. and Wonstein, is {mk('the only song by a Korean artist')}.",
                  "He closes with two Japanese love songs: Shota Shimizu's \"Kimi ga Suki\" and back number's \"Hanataba\"."),
                p(f"{mk('Ed Sheeran and Shota Shimizu were also on YURA’s list')}, though YURA picked different songs (\"Photograph\" and \"Koiuta\")."),
                p(f"It runs about 37 minutes. Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
    {
        "member": "RYOGA", "date": ("10月15日", "10월 15일", "October 15"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2110505943427428634",
        "lnk": "https://ko1keyz.lnk.to/RYOGA_KO1KEYZ",
        "spotify": "0nzQQJjyS1onsHW8KE2xUS",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("BLACK ANGEL - KO1KEYZ ver.", "KO1KEYZ", "BLACK ANGEL - KO1KEYZ ver.", "KO1KEYZ"),
            ("チェックのワンピース", "back number", "Check no One-piece", "back number"),
            ("幸せ", "back number", "Shiawase", "back number"),
            ("fish", "back number", "fish", "back number"),
            ("透明", "Novelbright", "Toumei", "Novelbright"),
            ("サマーワンダーランド", "back number", "Summer Wonderland", "back number"),
            ("言えない", "MIMiNARI, asmi", "Ienai", "MIMiNARI, asmi"),
            ("センチメートル", "the peggies", "Centimeter", "the peggies"),
            ("花の塔", "Sayuri", "Hana no Tou", "Sayuri"),
        ],
        "cell": ("back number・Sayuri・Novelbrightほか全10曲", "back number・Sayuri・Novelbright 등 총 10곡",
                 "10 songs, incl. back number and Sayuri"),
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>back numberが4曲、アニメの主題歌も2曲"),
                p("9人目は、3歳からサッカーを続けてきたアニメ好きのRYOGA。",
                  "選んだのは全10曲で、1曲目は表題曲「KO1KEYZ」、2曲目は「BLACK ANGEL - KO1KEYZ ver.」です。",
                  "2曲目に「BLACK ANGEL」を選んだのは、SIYOUNGに続いて2人目になりました。"),
                m["table"],
                p(f"まず目を引くのは、{mk('back numberの曲が4曲も入っている')}ところ。",
                  "「チェックのワンピース」「幸せ」「fish」「サマーワンダーランド」と、KO1KEYZ以外の8曲のうち半分がback numberです。",
                  "同じアーティストを4曲選んだのは、Hey! Say! JUMPを4曲入れたDAIKIと並んで最多タイになりました。"),
                p("back numberは、前日のISSAも「花束」を選んでいたバンド。",
                  "曲は1つも重なっていませんが、2日続けてback numberのラブソングがプレイリストに入ったことになります。"),
                p(f"アニメ好きのRYOGAらしく、{mk('アニメの主題歌が2曲')}入っているのもポイント。",
                  "the peggies「センチメートル」はTVアニメ『彼女、お借りします』のオープニング、ラストのSayuri「花の塔」はTVアニメ『リコリス・リコイル』のエンディングとして知られる曲です。"),
                p(f"Novelbright「透明」、MIMiNARIとasmiの「言えない」も含めて、{mk('KO1KEYZ以外の8曲はすべて日本のアーティスト')}。",
                  "全曲が日本の曲だったのは、YOSHIKI・RYUJIに続いて3人目です。",
                  f"全部で約41分と、YOSHIKIと並んでここまででいちばん長いプレイリストで、聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>back number 4곡, 애니메이션 주제가 2곡"),
                p("아홉 번째 주자는 세 살 때부터 축구를 해 온 애니메이션 좋아하는 RYOGA예요.",
                  "총 10곡으로, 1번은 타이틀곡 'KO1KEYZ', 2번은 'BLACK ANGEL - KO1KEYZ ver.'입니다.",
                  "2번 트랙에 'BLACK ANGEL'을 고른 건 SIYOUNG에 이어 두 번째예요."),
                m["table"],
                p(f"가장 눈에 띄는 건 {mk('back number의 곡이 4곡이나 들어간')} 점이에요.",
                  "'チェックのワンピース', '幸せ', 'fish', 'サマーワンダーランド'로, KO1KEYZ 곡을 뺀 8곡 중 절반이 back number예요.",
                  "같은 아티스트를 4곡 고른 건 Hey! Say! JUMP를 4곡 넣은 DAIKI와 함께 최다 타이 기록입니다."),
                p("back number는 전날 ISSA도 '花束(꽃다발)'를 골랐던 밴드예요. 곡은 겹치지 않았어요."),
                p(f"{mk('애니메이션 주제가가 2곡')} 들어간 것도 포인트예요.",
                  "the peggies 'センチメートル'는 TV 애니메이션 '여친, 빌리겠습니다'의 오프닝, 마지막 곡 Sayuri '花の塔'는 TV 애니메이션 '리코리스 리코일'의 엔딩으로 알려진 곡이에요."),
                p(f"{mk('KO1KEYZ 곡을 뺀 8곡이 모두 일본 아티스트')}로, YOSHIKI, RYUJI에 이어 세 번째예요.",
                  f"약 41분으로 YOSHIKI와 함께 지금까지 가장 긴 플레이리스트이고, {a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>Four back number songs and two anime theme songs"),
                p("Ninth up was RYOGA, an anime fan who has played soccer since he was three.",
                  "He picked 10 songs, opening with \"KO1KEYZ\" and \"BLACK ANGEL - KO1KEYZ ver.\", making him the second member, after SIYOUNG, to choose \"BLACK ANGEL\" as his second track."),
                m["table"],
                p(f"{mk('Four of his picks are by back number')}: \"Check no One-piece\", \"Shiawase\", \"fish\" and \"Summer Wonderland\".",
                  "That ties DAIKI (four Hey! Say! JUMP songs) for the most songs by one artist. ISSA had picked back number's \"Hanataba\" the day before, though none of the songs overlap."),
                p(f"True to his love of anime, {mk('two anime theme songs')} made the list: the peggies' \"Centimeter\", the opening of Rent-A-Girlfriend, and Sayuri's \"Hana no Tou\", known as the ending of Lycoris Recoil."),
                p(f"With Novelbright and MIMiNARI & asmi as well, {mk('all eight non-KO1KEYZ songs are by Japanese artists')}, making him the third member to do so after YOSHIKI and RYUJI.",
                  f"At about 41 minutes, it ties YOSHIKI's for the longest so far. Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
    {
        "member": "TOWA", "date": ("10月16日", "10월 16일", "October 16"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2110868322237763930",
        "lnk": "https://ko1keyz.lnk.to/TOWA_KO1KEYZ",
        "spotify": "2Iv1Gc0pFzJprNetOrx0hI",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("恋GAME", "KO1KEYZ", "Koi GAME", "KO1KEYZ"),
            ("Good Mood - Original Song From Paw Patrol: The Movie", "Adam Levine", "Good Mood - Original Song From Paw Patrol: The Movie", "Adam Levine"),
            ("There's Nothing Holdin' Me Back", "Shawn Mendes", "There's Nothing Holdin' Me Back", "Shawn Mendes"),
            ("Could Have Been Me", "Halsey", "Could Have Been Me", "Halsey"),
            ("Maps", "Maroon 5", "Maps", "Maroon 5"),
            ("AS IF IT'S YOUR LAST - KR Ver.", "BLACKPINK", "AS IF IT'S YOUR LAST - KR Ver.", "BLACKPINK"),
            ("I Feel Good", "BOYNEXTDOOR", "I Feel Good", "BOYNEXTDOOR"),
            ("WE GO UP", "BABYMONSTER", "WE GO UP", "BABYMONSTER"),
            ("Pop Off Pop Off", "KiiiKiii", "Pop Off Pop Off", "KiiiKiii"),
        ],
        "cell": ("BLACKPINK・Maroon 5・BABYMONSTERほか全10曲", "BLACKPINK・Maroon 5・BABYMONSTER 등 총 10곡",
                 "10 songs, incl. BLACKPINK and Maroon 5"),
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>2曲目に初めて「恋GAME」、前半は洋楽・後半はK-POP"),
                p("10人目はTOWA。",
                  "選んだのは全10曲で、1曲目は表題曲「KO1KEYZ」、2曲目は「恋GAME」です。",
                  f"ここまでの9人は2曲目に「Key of Story」「ねこ」「BLACK ANGEL」のどれかを選んでいたので、{mk('2曲目に「恋GAME」を入れたのはTOWAが初めて')}になりました。"),
                m["table"],
                p("3曲目から6曲目は洋楽で、Adam Levine「Good Mood」、Shawn Mendes「There's Nothing Holdin' Me Back」、Halsey「Could Have Been Me」、Maroon 5「Maps」と続きます。",
                  "「Good Mood」は映画『パウ・パトロール ザ・ムービー』のための曲で、歌っているAdam LevineはMaroon 5のボーカル。",
                  "つまり洋楽4曲のうち2曲が、同じ人の歌声ということになります。"),
                p(f"後半の4曲は、{mk('BLACKPINK・BOYNEXTDOOR・BABYMONSTER・KiiiKiiiとすべてK-POP')}。",
                  "BABYMONSTERはBLACKPINKと同じYGエンターテインメントのグループなので、7曲目と9曲目は先輩・後輩の曲が並んでいることになります。"),
                p(f"KO1KEYZ以外の8曲には日本語の曲が1曲もなく、{mk('洋楽とK-POPだけで組んだのはTOWAが初めて')}です(SIYOUNGは8曲すべて洋楽でした)。",
                  "テンポのいい曲が多く、ここまでのしっとりしたラブソング中心のプレイリストとは雰囲気ががらっと変わります。"),
                p("全部で約30分と、ここまででいちばん短いプレイリスト。",
                  f"聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>2번 트랙에 처음으로 '恋GAME', 전반은 팝·후반은 K-POP"),
                p("열 번째 주자는 TOWA예요.",
                  "총 10곡으로, 1번은 타이틀곡 'KO1KEYZ', 2번은 '恋GAME'입니다.",
                  f"지금까지 9명은 2번 트랙에 'Key of Story', '네코', 'BLACK ANGEL' 중 하나를 골랐기 때문에, {mk('2번 트랙에 恋GAME을 넣은 건 TOWA가 처음')}이에요."),
                m["table"],
                p("3~6번은 팝으로 Adam Levine, Shawn Mendes, Halsey, Maroon 5가 이어져요.",
                  "'Good Mood'는 영화 '퍼피 구조대 더 무비'를 위한 곡이고, 부른 Adam Levine은 Maroon 5의 보컬이라 팝 4곡 중 2곡이 같은 사람의 목소리예요."),
                p(f"후반 4곡은 {mk('BLACKPINK, BOYNEXTDOOR, BABYMONSTER, KiiiKiii로 모두 K-POP')}이에요.",
                  "BABYMONSTER는 BLACKPINK와 같은 YG엔터테인먼트 그룹이라 선후배 곡이 함께 들어간 셈이에요."),
                p(f"{mk('일본어 곡 없이 팝과 K-POP만으로 구성한 건 TOWA가 처음')}이에요.",
                  f"약 30분으로 지금까지 가장 짧은 플레이리스트이고, {a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>The first to pick \"Koi GAME\" as track 2; Western pop first, K-pop second"),
                p("Tenth up was TOWA.",
                  "He picked 10 songs, opening with \"KO1KEYZ\" and \"Koi GAME\".",
                  f"The nine members before him all chose \"Key of Story\", \"Neko\" or \"BLACK ANGEL\" as their second track, so {mk('TOWA is the first to go with \"Koi GAME\"')}."),
                m["table"],
                p("Tracks 3 to 6 are Western pop: Adam Levine, Shawn Mendes, Halsey and Maroon 5.",
                  "\"Good Mood\" was written for PAW Patrol: The Movie, and Adam Levine is Maroon 5's lead singer, so two of the four feature the same voice."),
                p(f"The last four are {mk('all K-pop: BLACKPINK, BOYNEXTDOOR, BABYMONSTER and KiiiKiii')}.",
                  "BABYMONSTER is also a YG Entertainment group, so BLACKPINK and their juniors share the list."),
                p(f"{mk('He is the first to build his list from Western pop and K-pop only')}, with no Japanese songs besides KO1KEYZ's (SIYOUNG's eight were all Western).",
                  f"At about 30 minutes, it's the shortest so far. Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
    {
        "member": "KOSUKE", "date": ("10月17日", "10월 17일", "October 17"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2111230716725915941",
        "lnk": "https://ko1keyz.lnk.to/KOSUKE_KO1KEYZ",
        "spotify": "3HqdyLpDrSr6WBe23uGPTx",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("BLACK ANGEL - KO1KEYZ ver.", "KO1KEYZ", "BLACK ANGEL - KO1KEYZ ver.", "KO1KEYZ"),
            ("seasons", "Joon", "seasons", "Joon"),
            ("B.Y.S.", "keshi", "B.Y.S.", "keshi"),
            ("E.T.A.", "Justin Bieber", "E.T.A.", "Justin Bieber"),
            ("Bambi", "BAEKHYUN", "Bambi", "BAEKHYUN"),
            ("ユーモア", "King Gnu", "Humor", "King Gnu"),
            ("ONLY FOR U", "Woody", "ONLY FOR U", "Woody"),
            ("WINTER WITHOUT YOU", "XG", "WINTER WITHOUT YOU", "XG"),
            ("Mask In Love", "Kenya Fujita", "Mask In Love", "Kenya Fujita"),
        ],
        "cell": ("keshi・BAEKHYUN・King Gnuほか全10曲", "keshi・BAEKHYUN・King Gnu 등 총 10곡",
                 "10 songs, incl. keshi, BAEKHYUN and King Gnu"),
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全10曲(うちKO1KEYZの曲が2曲)",
                           "<strong>注目:</strong>keshiは4人目、ほかのメンバーとアーティストが重なる曲が多め"),
                p("11人目はKOSUKE。",
                  "選んだのは全10曲で、1曲目は表題曲「KO1KEYZ」、2曲目は「BLACK ANGEL - KO1KEYZ ver.」です。",
                  "2曲目に「BLACK ANGEL」を選んだのは、SIYOUNG・RYOGAに続いて3人目になりました。"),
                m["table"],
                p(f"4曲目のkeshi「B.Y.S.」で、{mk('keshiの曲を選んだメンバーは4人目')}。",
                  "SHINHAENGとYURAは「beside you」、KEITOは「WANTCHU」だったので、KOSUKEはまた別の曲を選んだことになります。"),
                p(f"ほかにも、{mk('ここまでのメンバーとアーティストが重なる曲')}がいくつも入っています。",
                  "Justin Bieber「E.T.A.」はISSAが3曲選んでいたアーティストで、ラストのKenya Fujita「Mask In Love」はRYUJIが「ALL MINE」を選んでいたアーティスト。",
                  "BAEKHYUN「Bambi」はEXOのメンバーのソロ曲で、ISSAが選んだD.O.もEXOのメンバーです。",
                  "どれも曲そのものは別で、同じアーティストの違う曲を選んでいるのが面白いところです。"),
                p("日本のアーティストはKing Gnu「ユーモア」と、日本人メンバーのガールズグループXGの「WINTER WITHOUT YOU」、Kenya Fujitaの3組。",
                  "洋楽・K-POP・J-POPがバランスよく混ざった選曲です。"),
                p(f"全部で約33分のプレイリストで、聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 10곡(그중 KO1KEYZ 곡 2곡)",
                           "<strong>주목:</strong>keshi는 네 번째, 다른 멤버와 아티스트가 겹치는 곡이 많아요"),
                p("열한 번째 주자는 KOSUKE예요.",
                  "총 10곡으로, 1번은 타이틀곡 'KO1KEYZ', 2번은 'BLACK ANGEL - KO1KEYZ ver.'입니다.",
                  "2번 트랙에 'BLACK ANGEL'을 고른 건 SIYOUNG, RYOGA에 이어 세 번째예요."),
                m["table"],
                p(f"4번 트랙 keshi 'B.Y.S.'로 {mk('keshi의 곡을 고른 멤버는 네 번째')}예요.",
                  "SHINHAENG과 YURA는 'beside you', KEITO는 'WANTCHU'였으니 KOSUKE는 또 다른 곡을 골랐어요."),
                p(f"{mk('지금까지의 멤버와 아티스트가 겹치는 곡')}도 많아요.",
                  "Justin Bieber는 ISSA가 3곡 고른 아티스트, Kenya Fujita는 RYUJI가 'ALL MINE'을 고른 아티스트예요.",
                  "BAEKHYUN 'Bambi'는 EXO 멤버의 솔로곡이고, ISSA가 고른 디오(D.O.)도 EXO 멤버예요. 곡 자체는 모두 달랐어요."),
                p("일본 아티스트는 King Gnu, 일본인 멤버로 구성된 걸그룹 XG, Kenya Fujita의 3팀이에요.",
                  f"약 33분 길이의 플레이리스트로, {a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>10 songs (2 of them by KO1KEYZ)",
                           "<strong>Highlight:</strong>The fourth member to pick keshi, plus several artists shared with other members"),
                p("Eleventh up was KOSUKE.",
                  "He picked 10 songs, opening with \"KO1KEYZ\" and \"BLACK ANGEL - KO1KEYZ ver.\", making him the third member, after SIYOUNG and RYOGA, to choose \"BLACK ANGEL\" as his second track."),
                m["table"],
                p(f"With keshi's \"B.Y.S.\" at track 4, {mk('he is the fourth member to pick a keshi song')}, and a different one again: SHINHAENG and YURA chose \"beside you\" and KEITO chose \"WANTCHU\"."),
                p(f"{mk('Several more artists overlap with other members')}: Justin Bieber (three songs on ISSA's list) and Kenya Fujita (\"ALL MINE\" on RYUJI's).",
                  "BAEKHYUN's \"Bambi\" is a solo song by a member of EXO, and ISSA had picked a song by D.O., also of EXO. In every case the songs themselves are different."),
                p("The Japanese artists are King Gnu, XG, a girl group made up of Japanese members, and Kenya Fujita.",
                  f"It runs about 33 minutes. Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
            ],
        },
    },
    {
        "member": "YUKI", "date": ("10月18日", "10월 18일", "October 18"),
        "tweet": "https://twitter.com/KO1KEYZofficial/status/2111593104566301147",
        "lnk": "https://ko1keyz.lnk.to/YUKI_KO1KEYZ",
        "spotify": "0x3KKIbR789g8RehmpPAkj",
        "tracks": [
            ("KO1KEYZ", "KO1KEYZ", "KO1KEYZ", "KO1KEYZ"),
            ("恋GAME", "KO1KEYZ", "Koi GAME", "KO1KEYZ"),
            ("Love Jang", "&TEAM", "Love Jang", "&TEAM"),
            ("Call Me", "BOYNEXTDOOR", "Call Me", "BOYNEXTDOOR"),
            ("Through the Night", "IU", "Through the Night", "IU"),
            ("give it back", "Cö shu Nie", "give it back", "Cö shu Nie"),
            ("Lucky to be loved", "TWS", "Lucky to be loved", "TWS"),
            ("勇者", "YOASOBI", "The Brave", "YOASOBI"),
            ("晴る", "ヨルシカ", "Haru", "Yorushika"),
        ],
        "cell": ("YOASOBI・ヨルシカ・IUほか全9曲", "YOASOBI・요루시카・IU 등 총 9곡",
                 "9 songs, incl. YOASOBI, Yorushika and IU"),
        "body": {
            "ja": lambda m: [
                ui.minibox("<strong>曲数:</strong>全9曲(うちKO1KEYZの曲が2曲)、12人で1人だけ10曲未満",
                           "<strong>注目:</strong>2曲目は「恋GAME」、ラスト2曲は『葬送のフリーレン』のオープニング曲"),
                p("12人目、ラストを飾ったのはYUKI。",
                  f"ほかの11人がそろって全10曲だったなか、{mk('YUKIだけが全9曲')}のプレイリストになりました。",
                  "1曲目は表題曲「KO1KEYZ」、2曲目は「恋GAME」で、2曲目に「恋GAME」を選んだのはTOWAに続いて2人目です。"),
                m["table"],
                p("3曲目からは&TEAM「Love Jang」、BOYNEXTDOOR「Call Me」、IU「Through the Night」、Cö shu Nie「give it back」、TWS「Lucky to be loved」と続きます。",
                  "IU「Through the Night」は、韓国語のタイトル「밤편지(夜の手紙)」で知られる曲です。",
                  "&TEAM・BOYNEXTDOOR・TWSの3組は、どれもHYBE傘下のレーベルに所属するグループです。"),
                p("BOYNEXTDOORは、TOWAも「I Feel Good」を選んでいたグループ。",
                  f"マンネラインの2人は、{mk('2曲目の「恋GAME」に続いてアーティストまで重なりました')}(曲は別)。"),
                p(f"最後の2曲はYOASOBI「勇者」とヨルシカ「晴る」で、{mk('どちらもアニメ『葬送のフリーレン』のオープニング曲')}。",
                  "「勇者」が第1クール、「晴る」が第2クールのオープニングなので、放送順のとおりに並んでいます。"),
                p("韓国と日本のアーティストを組み合わせた選曲で、洋楽は1曲も入っていません。",
                  "全部で約30分と、TOWAとほぼ同じ長さ。わずかな差で、12人の中でいちばん短いプレイリストになりました。",
                  f"聴くときは{a(m['lnk'], '公式の共通リンク')}から、使っているサービスを選んでください。"),
            ],
            "ko": lambda m: [
                ui.minibox("<strong>곡 수:</strong>총 9곡(그중 KO1KEYZ 곡 2곡), 12명 중 유일하게 10곡 미만",
                           "<strong>주목:</strong>2번 트랙은 '恋GAME', 마지막 2곡은 《장송의 프리렌》 오프닝곡"),
                p("열두 번째, 마지막 주자는 YUKI예요.",
                  f"다른 11명이 모두 10곡이었는데, {mk('YUKI만 총 9곡')}으로 구성했어요.",
                  "1번은 타이틀곡 'KO1KEYZ', 2번은 '恋GAME'으로, 2번 트랙에 恋GAME을 고른 건 TOWA에 이어 두 번째예요."),
                m["table"],
                p("3번부터는 &TEAM, BOYNEXTDOOR, IU, Cö shu Nie, TWS가 이어져요.",
                  "IU 'Through the Night'는 '밤편지'로 잘 알려진 곡이고, &TEAM・BOYNEXTDOOR・TWS는 모두 HYBE 산하 레이블 그룹이에요."),
                p(f"BOYNEXTDOOR는 TOWA도 'I Feel Good'을 고른 그룹이라, 막내 라인 두 사람은 {mk('2번 트랙 恋GAME에 이어 아티스트까지 겹쳤어요')}(곡은 달라요)."),
                p(f"마지막 2곡은 YOASOBI '勇者'와 요루시카 '晴る'로, {mk('둘 다 애니메이션 《장송의 프리렌》 오프닝곡')}이에요.",
                  "'勇者'가 1쿨, '晴る'가 2쿨 오프닝이라 방송 순서대로 들어가 있어요."),
                p("한국과 일본 아티스트로만 구성했고 팝은 한 곡도 없어요.",
                  f"약 30분으로 TOWA와 거의 같은 길이인데, 아주 근소한 차이로 12명 중 가장 짧은 플레이리스트예요. {a(m['lnk'], '공식 링크')}에서 사용하는 서비스를 골라 들을 수 있어요."),
            ],
            "en": lambda m: [
                ui.minibox("<strong>Length:</strong>9 songs (2 of them by KO1KEYZ), the only list under 10",
                           "<strong>Highlight:</strong>\"Koi GAME\" as track 2, and two Frieren opening themes to finish"),
                p("Twelfth and last was YUKI.",
                  f"All eleven members before him picked 10 songs, but {mk('YUKI went with 9')}.",
                  "He opens with \"KO1KEYZ\" and \"Koi GAME\", the second member after TOWA to choose \"Koi GAME\" as track 2."),
                m["table"],
                p("Next come &TEAM, BOYNEXTDOOR, IU, Cö shu Nie and TWS.",
                  "IU's \"Through the Night\" is better known by its Korean title, \"Bam Pyeonji\", and &TEAM, BOYNEXTDOOR and TWS all belong to HYBE labels."),
                p(f"TOWA had also picked BOYNEXTDOOR (\"I Feel Good\"), so {mk('the two maknae-line members share an artist as well as their track 2')}, though not the same song."),
                p(f"He closes with YOASOBI's \"The Brave\" and Yorushika's \"Haru\", {mk('both opening themes of the anime Frieren: Beyond Journey’s End')}, in broadcast order (first and second cour)."),
                p("Every artist is Korean or Japanese, with no Western pop.",
                  f"At about 30 minutes, it's almost exactly as long as TOWA's and, by a few seconds, the shortest of all twelve. Use {a(m['lnk'], 'the official link')} to pick your streaming service."),
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
    # styleを付けるとブロックエディタで無効扱いになるので、thead/thだけで組む
    head = {"ja": ("No.", "曲名", "アーティスト"), "ko": ("No.", "곡명", "아티스트"), "en": ("No.", "Song", "Artist")}[lang]
    rows = [(str(n), (t[2] if lang == "en" else t[0]), (t[3] if lang == "en" else t[1])) for n, t in enumerate(tracks, 1)]
    thead = "<thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead>"
    tbody = "<tbody>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody>"
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout">'
            + thead + tbody + '</table></figure>\n<!-- /wp:table -->')


H2_LISTEN = {"ja": "プレイリストはどこで聴ける？", "ko": "플레이리스트는 어디서 들을 수 있을까?", "en": "Where can you listen to the playlists?"}
H2_PICKS = {"ja": "12人が選んだプレイリストの曲目", "ko": "12명이 고른 플레이리스트 곡 목록", "en": "All 12 members' playlists"}  # 10/18に_finalize_で改名
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
    pat = re.compile(rf'({re.escape(m["member"])}</td><td(?: style="[^"]*")?>){re.escape(PENDING[lang])}(</td>)')
    c, n = pat.subn(rf'\g<1><a href="#{anchor}">{m["cell"][li]}</a>\g<2>', c)
    assert n == 1, (lang, m["member"], n)
    for old, new in m.get("reps", {}).get(lang, []):
        assert c.count(old) == 1, (lang, old, c.count(old))
        c = c.replace(old, new)
    return c, True


def unstyle_tables(c):
    """style付きの旧形式の表(1行目が見出し)を、style無し+thead/thの形に直す。"""
    def fix(mo):
        t = mo.group(0)
        if "style=" not in t:
            return t
        t = re.sub(r'<(td|th) style="[^"]*">', r"<\1>", t)
        first = re.search(r"<tbody><tr>(.*?)</tr>", t, re.S)
        head = first.group(1).replace("<td>", "<th>").replace("</td>", "</th>")
        t = t.replace(first.group(0), f"<thead><tr>{head}</tr></thead><tbody>", 1)
        assert "style=" not in t, t[:200]
        return t
    return re.sub(r"<!-- wp:table -->.*?<!-- /wp:table -->", fix, c, flags=re.S)


def main():
    dry = "--dry" in sys.argv
    for lang, pid in IDS.items():
        r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=HA)
        r.raise_for_status()
        post = r.json()
        assert post["status"] == "publish"
        c0 = post["content"]["raw"]
        c = unstyle_tables(first_time(c0, lang))
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
