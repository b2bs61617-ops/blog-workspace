# -*- coding: utf-8 -*-
"""KO1KEYZ「恋GAME」歌割り(パート分け)+歌詞のゲーム用語解説記事。chomoand-1.com に JP/KR/EN 下書き。

元ネタ: ファンの聞き取り(絵文字割当の歌割り表、X 2104234265559081180 / 9/27)。
docs/rules.md・歌割り記事ルール([[feedback_koikeyz_utawari_source_and_quotebox_style]])に従い、
出典URLは本文に貼らず「SNSで話題の聞き取り」止まり。歌詞は丸写しせず、場面の説明+短いキーワードのみ。
絵文字→メンバー: ⚾ISSA ⚽RYOGA 🎀YUKI 🥔SHINHAENG 🚀YURA ⚡SIYOUNG 🐲RYUJI 🌟KOSUKE 🍎TOWA 🍀DAIKI 🍰YOSHIKI 🏃KEITO

python build_and_post_ko1keyz_koigame_utawari.py [--dry]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from ko1keyz_article_kit import WP_URL, HEADERS_AUTH as HA, Ui, wphtml, p, h2, a  # noqa: E402

EYE_JP = ROOT / "images" / "ko1keyz_koigame_utawari_eyecatch.png"
EYE_KR = ROOT / "images" / "ko1keyz_koigame_utawari_eyecatch_kr.png"
BASE_SLUG = "ko1keyz-koi-game-utawari"
MEDLEY = "https://www.youtube.com/watch?v=pCz0zV_E_i0"

L = lambda pid: f"https://chomoand-1.com/?p={pid}"

ACC, BOR, BG = "#8a8378", "#ddd9d3", "#f7f6f4"
ui = Ui(ACC, BOR, BG, "rgba(138,131,120,0.06)")

COLOR = {"YOSHIKI": "#d63384", "TOWA": "#5a9e1a", "SIYOUNG": "#6c757d", "DAIKI": "#1a8f4c",
         "SHINHAENG": "#8b5a2b", "KEITO": "#e8730c", "ISSA": "#2ba3c9", "YURA": "#1565c0",
         "YUKI": "#7b2fb5", "RYUJI": "#b8860b", "KOSUKE": "#d7263d", "RYOGA": "#283593"}


def mk(t):
    return f'<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{t}</span></strong>'


def nm(names):
    return "・".join(f'<span style="color:{COLOR[n]};font-weight:bold;">{n}</span>' for n in names.split("・"))


def note(html):
    return wphtml(f'<div style="border-left:3px solid {ACC};background:{BG};padding:8px 14px;margin:0 0 12px 0;'
                  f'font-size:0.9em;color:#555;">{html}</div>')


TD = f"border:1px solid {BOR};padding:6px 10px;vertical-align:top;"


def parts_table(heads, sections):
    """sections: [(section_label, [(members, scene), ...]), ...]"""
    th = "".join(f'<th style="border:1px solid {BOR};padding:6px 10px;background:{ACC};color:#fff;text-align:left;'
                 f'{"white-space:nowrap;" if i < 2 else ""}">{h}</th>' for i, h in enumerate(heads))
    body = ""
    for label, rows in sections:
        for i, (who, scene) in enumerate(rows):
            body += "<tr>\n"
            if i == 0:
                body += (f'<td rowspan="{len(rows)}" style="{TD}background:{BG};font-weight:bold;white-space:nowrap;">'
                         f"{label}</td>\n")
            body += f'<td style="{TD}">{nm(who)}</td>\n<td style="{TD}">{scene}</td>\n</tr>\n'
    return wphtml(f'''<div style="overflow-x:auto;">
<table style="border-collapse:collapse;width:100%;font-size:0.9em;">
<thead>
<tr>
{th}
</tr>
</thead>
<tbody>
{body}</tbody>
</table>
</div>''')


def grid(rows):
    head = "".join(f'<td style="background:{ACC};color:#fff;font-weight:bold;padding:8px;">{c}</td>' for c in rows[0])
    body = ""
    for i, r in enumerate(rows[1:]):
        bg = f' style="background:{BG};"' if i % 2 == 0 else ""
        body += f"<tr{bg}>" + "".join(f'<td style="padding:8px;">{c}</td>' for c in r) + "</tr>\n"
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>\n'
            f"<tr>{head}</tr>\n{body}</tbody></table></figure>\n<!-- /wp:table -->")


def embed(url):
    attrs = {"url": url, "type": "video", "providerNameSlug": "youtube", "responsive": True,
             "className": "wp-embed-aspect-16-9 wp-has-aspect-ratio"}
    return (f"<!-- wp:embed {json.dumps(attrs)} -->\n"
            '<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">'
            f'<div class="wp-block-embed__wrapper">\n{url}\n</div></figure>\n<!-- /wp:embed -->')


OFFICIAL_X = "https://x.com/KO1KEYZofficial/status/2104224546119438762"
STREAM = "https://lnk.to/KKZ_KOIGAME"


def xembed(url):
    attrs = {"url": url, "type": "rich", "providerNameSlug": "twitter", "responsive": True}
    return (f"<!-- wp:embed {json.dumps(attrs)} -->\n"
            '<figure class="wp-block-embed is-type-rich is-provider-twitter wp-block-embed-twitter">'
            f'<div class="wp-block-embed__wrapper">\n{url}\n</div></figure>\n<!-- /wp:embed -->')


PHOTO = wphtml('''<figure class="wp-block-image size-large">
<img src="https://chomoand-1.com/wp-content/uploads/2026/07/ko1keyz_profile_photo-406x500.jpg" alt="{alt}" width="406" height="500" style="max-width:100%;height:auto;" srcset="https://chomoand-1.com/wp-content/uploads/2026/07/ko1keyz_profile_photo-243x300.jpg 243w, https://chomoand-1.com/wp-content/uploads/2026/07/ko1keyz_profile_photo-406x500.jpg 406w, https://chomoand-1.com/wp-content/uploads/2026/07/ko1keyz_profile_photo.jpg 780w" sizes="(max-width: 1024px) 100vw, 1024px">
<figcaption style="text-align:center;font-size:12px;">{src}<a href="https://x.com/KO1KEYZofficial/status/2067443433015525830/photo/1" target="_blank" rel="noopener">KO1KEYZ(コイキーズ)公式X(@KO1KEYZofficial)</a></figcaption>
</figure>''')

# ---------------------------------------------------------------- パート表
PARTS_JA = [
    ("1番の出だし", [
        ("KOSUKE", "ゲーム開始の合図「Pi」で幕を開ける歌い出し。続けて、この気持ちが「一目惚れ」だと気づく一節も担当"),
        ("SIYOUNG", "ゲームのコツが少しずつ分かってきた、という手応えを歌うパート"),
        ("YUKI", "初めて味わう「新感覚」に胸が躍る場面"),
        ("TOWA", "二人の関係を難易度「Tough」のモードや、強化すべき「装備」にたとえるパート"),
        ("KEITO", "TOWAの歌の語尾を追いかける掛け合い(ステージの聞き取りのみ。音源の聞き取りでは表記なし)"),
        ("YURA", "気づけば一晩中プレイしてしまうほど夢中になっている場面"),
        ("RYOGA", "1番の出だしを締める「Oh, yeah」"),
    ]),
    ("1番の中盤", [
        ("SHINHAENG・DAIKI", "「導いて」と手を引いてほしい気持ちと、「魔法」「ボタン連打」のフレーズを2人で交互に歌う"),
        ("RYUJI", "恋を「RPG」にたとえ、キミと一緒なら無敵だと言い切る決めのワンフレーズ"),
        ("ISSA", "秘密のアイテムは自分が探す、と頼もしく宣言する場面"),
        ("RYOGA", "「一緒に始めよう」と誘い、「We love game」で盛り上げる(2行)"),
        ("YOSHIKI", "RYOGAの間に入る「1st round」へのカウント"),
    ]),
    ("サビ前", [
        ("TOWA", "協力しないと「Bad end」、相手は誰でもいいわけじゃないと呼び寄せる場面"),
        ("KOSUKE", "二人で挑みたい、と「必殺のCombo attack」につなげるパート"),
    ]),
    ("1サビ", [
        ("YURA", "サビの頭。本気で好きになっていく「New game」、止められない恋を3行続けて歌う"),
        ("DAIKI", "1回目の「キミとキミとClear」"),
        ("SIYOUNG", "新しい世界へ踏み出す英語フレーズ"),
        ("YOSHIKI", "「共に旅する」「Continue」「pauseしない」の3行"),
        ("SHINHAENG", "もっと「レベル」を上げたい、と願う一言"),
        ("YUKI", "2回目の「キミとキミとClear」"),
        ("KEITO", "「Push Push」"),
        ("RYUJI", "サビを締めくくる「Final attack」"),
    ]),
    ("サビ後", [
        ("SIYOUNG", "「Imma get it」をくり返すフックの前半(3行)"),
        ("RYOGA", "必須アイテム(マストアイテム)は「Your love」だと告げる一言"),
        ("ISSA", "「Imma get it」のフックを引き継ぐ後半(3行)"),
        ("KOSUKE", "「Push Push」「Again and again」でブロックを締める"),
    ]),
    ("2番の出だし", [
        ("TOWA", "ダメならまた「Continue」、朝まで勝負を続ける夜の場面(3行)"),
        ("KOSUKE", "ドキドキしながら「恋人になろう」と告げる、2番の告白パート(3行)"),
    ]),
    ("2番の中盤", [
        ("YOSHIKI・RYOGA", "1番でSHINHAENG・DAIKIが歌ったフレーズを、今度はこの2人が交互に担当"),
        ("YUKI", "RPGを極めよう、シナリオの数は「無限大」と歌う決めのワンフレーズ"),
        ("SHINHAENG", "僕の「HP(ハートポイント)」はキミで満たす、と歌う2番オリジナルの一節"),
        ("ISSA", "「一緒に始めよう」「We love game」(2行)"),
        ("KEITO", "ISSAの間に入る「next round」へのカウント"),
    ]),
    ("2番サビ前", [
        ("KOSUKE", "「Bad end」「Come here」の2行。1番のTOWAパートを引き継ぐ"),
        ("DAIKI", "「二人で挑みたい」「必殺のCombo attack」の2行。1番のKOSUKEパートを引き継ぐ"),
    ]),
    ("ラスサビ前", [
        ("SIYOUNG", "「Again and again」"),
        ("YURA", "「Push Push Push」でラスサビへなだれ込む"),
    ]),
    ("ラスサビ", [
        ("ISSA", "サビの頭3行。1サビのYURAパートを担当"),
        ("RYOGA", "1回目の「キミとキミとClear」"),
        ("TOWA", "新しい世界へ踏み出す英語フレーズ"),
        ("SHINHAENG", "「共に旅する」「Continue」「pauseしない」の3行"),
        ("YOSHIKI", "「レベル」を上げたい、の一言(1サビとSHINHAENGと入れ替え)"),
        ("YUKI", "2回目の「キミとキミとClear」"),
        ("KEITO", "「Push Push」"),
        ("RYUJI", "ここでも「Final attack」でサビを締める"),
    ]),
    ("ラスト", [
        ("YURA", "「Imma get it」のフック前半(3行)"),
        ("DAIKI", "マストアイテムは「Your love」"),
        ("SIYOUNG", "「Imma get it」のフック後半(3行)"),
        ("TOWA", "「Push Push」「Again and again」で曲を締めくくる"),
    ]),
]

PARTS_KO = [
    ("1절 도입", [
        ("KOSUKE", "게임 시작 신호 'Pi'와 함께 막을 여는 첫 소절. 이 감정이 '첫눈에 반한 것'이라고 깨닫는 구절도 담당"),
        ("SIYOUNG", "게임 요령을 조금씩 알게 됐다는 손맛을 노래하는 파트"),
        ("YUKI", "처음 느끼는 '신감각'에 가슴이 뛰는 장면"),
        ("TOWA", "두 사람의 관계를 'Tough' 모드나 강화해야 할 '장비'에 비유하는 파트"),
        ("KEITO", "TOWA의 끝말을 따라 부르는 주고받기(무대 받아쓰기에만 있고 음원 받아쓰기에는 표기 없음)"),
        ("YURA", "정신 차려 보니 밤새 플레이할 만큼 빠져 있는 장면"),
        ("RYOGA", "1절 도입을 마무리하는 'Oh, yeah'"),
    ]),
    ("1절 중반", [
        ("SHINHAENG・DAIKI", "'이끌어 줘'라는 마음과 '마법', '버튼 연타' 구절을 둘이 번갈아 부름"),
        ("RYUJI", "사랑을 'RPG'에 비유하며 너와 함께라면 무적이라고 말하는 킬링 파트"),
        ("ISSA", "비밀 아이템은 내가 찾겠다고 든든하게 선언하는 장면"),
        ("RYOGA", "'같이 시작하자'와 'We love game'(2줄)"),
        ("YOSHIKI", "RYOGA 사이에 들어가는 '1st round'"),
    ]),
    ("후렴 전", [
        ("TOWA", "협력하지 않으면 'Bad end', 아무나 괜찮은 게 아니라며 상대를 부르는 장면"),
        ("KOSUKE", "둘이서 도전하고 싶다며 '필살 Combo attack'으로 잇는 파트"),
    ]),
    ("1절 후렴", [
        ("YURA", "후렴 첫머리. 진심으로 좋아지는 'New game', 멈출 수 없는 사랑을 3줄 연속"),
        ("DAIKI", "첫 번째 '너와 너와 Clear'"),
        ("SIYOUNG", "새로운 세계로 나아가는 영어 구절"),
        ("YOSHIKI", "'함께 여행하는', 'Continue', 'pause하지 않아' 3줄"),
        ("SHINHAENG", "더 '레벨'을 올리고 싶다는 한마디"),
        ("YUKI", "두 번째 '너와 너와 Clear'"),
        ("KEITO", "'Push Push'"),
        ("RYUJI", "후렴을 마무리하는 'Final attack'"),
    ]),
    ("후렴 뒤", [
        ("SIYOUNG", "'Imma get it' 반복 훅 전반(3줄)"),
        ("RYOGA", "필수 아이템은 'Your love'라는 한마디"),
        ("ISSA", "'Imma get it' 훅 후반(3줄)"),
        ("KOSUKE", "'Push Push', 'Again and again'으로 마무리"),
    ]),
    ("2절 도입", [
        ("TOWA", "안 되면 다시 'Continue', 아침까지 승부를 이어 가는 밤 장면(3줄)"),
        ("KOSUKE", "두근거리며 '연인이 되자'고 고백하는 2절 파트(3줄)"),
    ]),
    ("2절 중반", [
        ("YOSHIKI・RYOGA", "1절에서 SHINHAENG・DAIKI가 부른 구절을 이번엔 두 사람이 번갈아 담당"),
        ("YUKI", "RPG를 마스터하자, 시나리오는 '무한대'라는 킬링 파트"),
        ("SHINHAENG", "나의 'HP(하트 포인트)'는 너로 채운다는 2절만의 구절"),
        ("ISSA", "'같이 시작하자'와 'We love game'(2줄)"),
        ("KEITO", "ISSA 사이에 들어가는 'next round'"),
    ]),
    ("2절 후렴 전", [
        ("KOSUKE", "'Bad end', 'Come here' 2줄. 1절 TOWA 파트를 이어받음"),
        ("DAIKI", "'둘이서 도전하고 싶어', '필살 Combo attack' 2줄. 1절 KOSUKE 파트를 이어받음"),
    ]),
    ("마지막 후렴 전", [
        ("SIYOUNG", "'Again and again'"),
        ("YURA", "'Push Push Push'로 마지막 후렴에 돌입"),
    ]),
    ("마지막 후렴", [
        ("ISSA", "후렴 첫 3줄. 1절 YURA 파트"),
        ("RYOGA", "첫 번째 '너와 너와 Clear'"),
        ("TOWA", "새로운 세계로 나아가는 영어 구절"),
        ("SHINHAENG", "'함께 여행하는', 'Continue', 'pause하지 않아' 3줄"),
        ("YOSHIKI", "'레벨'을 올리고 싶다는 한마디(1절과 SHINHAENG과 교대)"),
        ("YUKI", "두 번째 '너와 너와 Clear'"),
        ("KEITO", "'Push Push'"),
        ("RYUJI", "여기서도 'Final attack'으로 후렴 마무리"),
    ]),
    ("엔딩", [
        ("YURA", "'Imma get it' 훅 전반(3줄)"),
        ("DAIKI", "머스트 아이템은 'Your love'"),
        ("SIYOUNG", "'Imma get it' 훅 후반(3줄)"),
        ("TOWA", "'Push Push', 'Again and again'으로 곡을 마무리"),
    ]),
]

PARTS_EN = [
    ("Verse 1 opening", [
        ("KOSUKE", "Opens the song with the game-start beep \"Pi,\" and later realizes this feeling is love at first sight"),
        ("SIYOUNG", "Sings about finally getting the hang of the game"),
        ("YUKI", "The thrill of a brand-new sensation"),
        ("TOWA", "Compares the relationship to a \"Tough\" difficulty mode and gear that needs upgrading"),
        ("KEITO", "Echoes the ends of TOWA's lines (heard on stage; not marked in the audio transcription)"),
        ("YURA", "So hooked he plays all night without noticing"),
        ("RYOGA", "The \"Oh, yeah\" that closes the first verse"),
    ]),
    ("Verse 1 middle", [
        ("SHINHAENG・DAIKI", "Trade lines about wanting to be guided, a spell, and button-mashing"),
        ("RYUJI", "The killing line comparing love to an \"RPG\" and declaring they're invincible together"),
        ("ISSA", "Promises to find the secret item himself"),
        ("RYOGA", "\"Let's start it together\" and \"We love game\" (2 lines)"),
        ("YOSHIKI", "The \"1st round\" call between RYOGA's lines"),
    ]),
    ("Pre-chorus", [
        ("TOWA", "Without teamwork it's a \"Bad end\"; not just anyone will do, so \"Come here\""),
        ("KOSUKE", "Wants to take it on as a pair, leading into the \"Combo attack\""),
    ]),
    ("Chorus 1", [
        ("YURA", "Opens the chorus: a \"New game\" of falling for real, and a love that can't stop (3 lines)"),
        ("DAIKI", "The first \"Kimi to kimi to Clear\""),
        ("SIYOUNG", "The English line about heading to a new world"),
        ("YOSHIKI", "Traveling together, \"Continue,\" and no pausing (3 lines)"),
        ("SHINHAENG", "Wants to level up"),
        ("YUKI", "The second \"Kimi to kimi to Clear\""),
        ("KEITO", "\"Push Push\""),
        ("RYUJI", "Closes the chorus with \"Final attack\""),
    ]),
    ("Post-chorus", [
        ("SIYOUNG", "First half of the \"Imma get it\" hook (3 lines)"),
        ("RYOGA", "The must-have item is \"Your love\""),
        ("ISSA", "Second half of the \"Imma get it\" hook (3 lines)"),
        ("KOSUKE", "Wraps up with \"Push Push\" and \"Again and again\""),
    ]),
    ("Verse 2 opening", [
        ("TOWA", "If it fails, \"Continue\" again, playing on until morning (3 lines)"),
        ("KOSUKE", "The verse 2 confession: heart pounding, asking to be a couple (3 lines)"),
    ]),
    ("Verse 2 middle", [
        ("YOSHIKI・RYOGA", "Take over the lines SHINHAENG and DAIKI sang in verse 1"),
        ("YUKI", "The killing line about mastering the RPG with endless scenarios"),
        ("SHINHAENG", "A verse 2-only line about filling his \"HP (heart points)\" with you"),
        ("ISSA", "\"Let's start it together\" and \"We love game\" (2 lines)"),
        ("KEITO", "The \"next round\" call between ISSA's lines"),
    ]),
    ("Pre-chorus 2", [
        ("KOSUKE", "The \"Bad end\" and \"Come here\" lines, taking over TOWA's verse 1 part"),
        ("DAIKI", "The \"Combo attack\" lines, taking over KOSUKE's verse 1 part"),
    ]),
    ("Before the final chorus", [
        ("SIYOUNG", "\"Again and again\""),
        ("YURA", "\"Push Push Push\" into the final chorus"),
    ]),
    ("Final chorus", [
        ("ISSA", "Opens the chorus (3 lines), YURA's part in chorus 1"),
        ("RYOGA", "The first \"Kimi to kimi to Clear\""),
        ("TOWA", "The English line about heading to a new world"),
        ("SHINHAENG", "Traveling together, \"Continue,\" and no pausing (3 lines)"),
        ("YOSHIKI", "Wants to level up (swapped with SHINHAENG from chorus 1)"),
        ("YUKI", "The second \"Kimi to kimi to Clear\""),
        ("KEITO", "\"Push Push\""),
        ("RYUJI", "Closes the chorus with \"Final attack\" again"),
    ]),
    ("Ending", [
        ("YURA", "First half of the \"Imma get it\" hook (3 lines)"),
        ("DAIKI", "The must-have item is \"Your love\""),
        ("SIYOUNG", "Second half of the \"Imma get it\" hook (3 lines)"),
        ("TOWA", "Ends the song with \"Push Push\" and \"Again and again\""),
    ]),
]

# 行数(音源の聞き取り表の行単位。KEITOのステージでの掛け合いは含まない)
COUNT = [("KOSUKE", 11), ("TOWA", 10), ("ISSA", 9), ("SIYOUNG", 9), ("YURA", 8), ("SHINHAENG", 7),
         ("YOSHIKI", 7), ("RYOGA", 7), ("DAIKI", 6), ("YUKI", 4), ("KEITO", 3), ("RYUJI", 3)]
WHERE_JA = {"KOSUKE": "歌い出し・サビ前・2番の告白", "TOWA": "1番の出だし・サビ前・2番の出だし・曲のラスト",
            "ISSA": "フック・ラスサビの頭", "SIYOUNG": "フック(2回)・ラスサビ前", "YURA": "1サビの頭・ラストのフック",
            "SHINHAENG": "中盤・ラスサビ", "YOSHIKI": "1サビ・2番中盤", "DAIKI": "中盤・2番サビ前",
            "RYOGA": "Oh, yeah・中盤・マストアイテム", "YUKI": "Clear(毎サビ)・2番の決め", "KEITO": "Push Push(毎サビ)・next round",
            "RYUJI": "RPGの決め・Final attack(毎サビ)"}
WHERE_KO = {"KOSUKE": "첫 소절・후렴 전・2절 고백", "TOWA": "1절 도입・후렴 전・2절 도입・엔딩",
            "ISSA": "훅・마지막 후렴 첫머리", "SIYOUNG": "훅(2번)・마지막 후렴 전", "YURA": "1절 후렴 첫머리・엔딩 훅",
            "SHINHAENG": "중반・마지막 후렴", "YOSHIKI": "1절 후렴・2절 중반", "DAIKI": "중반・2절 후렴 전",
            "RYOGA": "Oh, yeah・중반・머스트 아이템", "YUKI": "Clear(매 후렴)・2절 킬링", "KEITO": "Push Push(매 후렴)・next round",
            "RYUJI": "RPG 킬링・Final attack(매 후렴)"}
WHERE_EN = {"KOSUKE": "Opening, pre-chorus, verse 2 confession", "TOWA": "Verse 1, pre-chorus, verse 2, ending",
            "ISSA": "Hook, start of final chorus", "SIYOUNG": "Hook (twice), before the final chorus", "YURA": "Start of chorus 1, final hook",
            "SHINHAENG": "Verse middles, final chorus", "YOSHIKI": "Chorus 1, verse 2 middle", "DAIKI": "Verse middles, pre-chorus 2",
            "RYOGA": "\"Oh, yeah,\" verse middles, must-have item", "YUKI": "\"Clear\" (every chorus), verse 2 killing line",
            "KEITO": "\"Push Push\" (every chorus), \"next round\"", "RYUJI": "RPG killing line, \"Final attack\" (every chorus)"}


def count_rows(head, where, unit):
    return [head] + [(nm(n), f"{c}{unit}", where[n]) for n, c in COUNT]


GAME_JA = [
    ("ゲーム用語", "ゲームでの意味", "恋GAMEの中での使われ方"),
    ("Pi(起動音)", "ゲームを始めるときの電子音", "恋が始まった瞬間の合図"),
    ("モード(Tough)", "難易度の設定", "二人の恋はそう簡単にクリアできない高難度"),
    ("装備・強化", "キャラの武器や防具を強くすること", "好きな人に振り向いてもらうための自分磨き"),
    ("Button連打", "ボタンを何度も押すこと", "気持ちを抑えきれず何度もアタックする様子"),
    ("RPG", "ロールプレイングゲーム。物語を進めて成長していく", "恋そのもの。キミと一緒なら無敵という世界観"),
    ("アイテム", "冒険を助ける道具", "「秘密のアイテム」を探す、必須アイテムは「Your love」"),
    ("round", "対戦の区切り(1回戦・次の回戦)", "恋の駆け引きの1戦目、そして次の戦い"),
    ("Field・Bad end", "ステージと、失敗のエンディング", "協力しないとハッピーエンドにならない二人の関係"),
    ("Combo attack", "技を連続でつなげる攻撃", "二人で息を合わせて挑むアプローチ"),
    ("HP", "ヒットポイント(体力)", "歌詞では「ハートポイント」と読み替え、キミで満たされる心"),
    ("New game・Continue・pause", "最初から遊ぶ・続きから遊ぶ・一時停止", "何度でも続けたい、止めたくない恋"),
    ("レベル上げ", "経験を積んでキャラを強くすること", "もっと相手にふさわしい自分になりたい気持ち"),
    ("Clear・Final attack・Win", "ステージ突破・最後の一撃・勝利", "恋を実らせるゴールに向かう決め手"),
]
GAME_KO = [
    ("게임 용어", "게임에서의 뜻", "恋GAME에서의 쓰임"),
    ("Pi(시작음)", "게임을 시작할 때 나는 전자음", "사랑이 시작된 순간의 신호"),
    ("모드(Tough)", "난이도 설정", "쉽게 클리어할 수 없는 고난도 사랑"),
    ("장비・강화", "캐릭터의 무기나 방어구를 강하게 하는 것", "좋아하는 사람을 위한 자기 관리"),
    ("버튼 연타", "버튼을 여러 번 누르는 것", "마음을 참지 못하고 계속 어택하는 모습"),
    ("RPG", "롤플레잉 게임. 이야기를 진행하며 성장", "사랑 그 자체. 너와 함께라면 무적"),
    ("아이템", "모험을 돕는 도구", "'비밀 아이템'을 찾고, 필수 아이템은 'Your love'"),
    ("round", "대전의 구분(1라운드・다음 라운드)", "사랑의 밀당 1라운드, 그리고 다음 승부"),
    ("Field・Bad end", "스테이지와 실패 엔딩", "협력하지 않으면 해피엔딩이 안 되는 두 사람"),
    ("Combo attack", "기술을 연속으로 잇는 공격", "둘이 호흡을 맞춰 도전하는 어프로치"),
    ("HP", "히트 포인트(체력)", "가사에서는 '하트 포인트'로 바꿔 읽음, 너로 채워지는 마음"),
    ("New game・Continue・pause", "처음부터・이어서・일시정지", "몇 번이고 계속하고 싶은, 멈추기 싫은 사랑"),
    ("레벨 업", "경험을 쌓아 캐릭터를 강하게 함", "상대에게 어울리는 내가 되고 싶은 마음"),
    ("Clear・Final attack・Win", "스테이지 돌파・마지막 일격・승리", "사랑을 이루는 결정타"),
]
GAME_EN = [
    ("Game term", "In games", "In \"Koi GAME\""),
    ("Pi (start beep)", "The sound when a game boots up", "The signal that love has begun"),
    ("Mode (Tough)", "Difficulty setting", "A love that isn't easy to clear"),
    ("Gear / upgrade", "Making weapons and armor stronger", "Working on yourself for the one you like"),
    ("Button-mashing", "Pressing a button over and over", "Making move after move, unable to hold back"),
    ("RPG", "Role-playing game where you grow through a story", "Love itself; invincible together"),
    ("Item", "Tools that help your quest", "A \"secret item\"; the must-have item is \"Your love\""),
    ("Round", "A stage of a match", "Round one of the romance, then the next"),
    ("Field / Bad end", "The stage and a failed ending", "Without teamwork, no happy ending"),
    ("Combo attack", "Chaining moves together", "An approach made in sync as a pair"),
    ("HP", "Hit points (health)", "Reread as \"heart points,\" filled up by you"),
    ("New game / Continue / pause", "Start over, resume, pause", "A love you want to keep playing forever"),
    ("Level up", "Getting stronger with experience", "Wanting to become worthy of them"),
    ("Clear / Final attack / Win", "Beat the stage, final blow, victory", "The finishing move toward a love that comes true"),
]

REL = {
    "ja": [(L(13208), "KO1KEYZデビュー曲「KO1KEYZ」の歌割りまとめ"),
           (L(12980), "「Run Again」の歌割りまとめ"),
           (L(12983), "「BLACK ANGEL」の歌割りまとめ"),
           (L(11644), "KO1KEYZ 1stファンミ初日のセトリ・座席表"),
           (L(13824), "KO1KEYZのロゴは誰が書いてる？(ガルアワのドット文字も)"),
           (L(13202), "KO1KEYZ×JOYSOUNDコラボキャンペーンの応募方法")],
    "ko": [(L(13220), "KO1KEYZ 타이틀곡 'KO1KEYZ' 파트 분배"),
           (L(12989), "'Run Again' 파트 분배"),
           (L(12992), "'BLACK ANGEL' 파트 분배"),
           (L(13829), "KO1KEYZ 로고는 누가 쓸까?"),
           (L(13214), "KO1KEYZ×JOYSOUND 콜라보 캠페인 참여 방법")],
    "en": [(L(13221), "Who sings what in KO1KEYZ's title track \"KO1KEYZ\""),
           (L(12990), "Who sings what in \"Run Again\""),
           (L(12993), "Who sings what in \"BLACK ANGEL\""),
           (L(13830), "Who draws the KO1KEYZ logo?"),
           (L(13217), "KO1KEYZ x JOYSOUND collab campaign: how to enter")],
}


def build():
    # ================================================================ JP
    jp_title = "KO1KEYZ「恋GAME」の歌詞・歌割りは？12人のパート！"
    jp = [
        p("恋愛をゲームにたとえたKO1KEYZ(コイキーズ)の新曲「恋GAME」。",
          "デビューシングルの発売に先がけて、2026年9月28日0時から各音楽配信サービスで先行配信がスタートしました。",
          f"配信音源の聞き取りで歌割りを数えてみると、{mk('最も多くのパートを歌っているのはKOSUKE、僅差でTOWAが続きます')}。",
          "この記事では、SNSで話題になっているファンの聞き取り(配信音源とステージの2種類)を照らし合わせて12人のパート分けを一覧にし、1番と2番でのパートの入れ替わりや、歌詞にちりばめられたゲーム用語の意味まで詳しくまとめました。"),
        ui.table("「恋GAME」基本情報", [
            ("曲名", "恋GAME"),
            ("収録", "DEBUT SINGLE『KO1KEYZ』(初回限定盤A・通常盤に収録)"),
            ("先行配信", f"2026年9月28日(日)0:00〜 {a(STREAM, '各音楽配信サービス')}"),
            ("CD発売日", "2026年10月7日(水)"),
            ("初披露", "2026年8月21日「KO1KEYZ 1ST FAN MEETING」東京公演DAY1(TOYOTA ARENA TOKYO)"),
            ("最近の披露", "2026年9月26日「GirlsAward 2026 AUTUMN/WINTER」(幕張メッセ)"),
            ("作詞・作曲", "公式サイトの収録内容ページでは未掲載(CDの歌詞カードで確認予定)"),
        ]),
        ui.titlebox("この記事でわかること", [
            "「恋GAME」はどんな曲か", "12人の歌割り(パート分け)一覧", "メンバー別のパート数",
            "1番と2番で入れ替わるパート・固定パート", "歌詞に出てくるゲーム用語の意味"]),
        h2("「恋GAME」はどんな曲？デビューシングルのカップリング曲"),
        ui.minibox("<strong>位置づけ:</strong>デビューシングル『KO1KEYZ』のカップリング曲(初回限定盤A・通常盤)",
                   "<strong>テーマ:</strong>恋愛をゲームにたとえた、ポップで遊び心のあるラブソング",
                   "<strong>聴き方:</strong>9月28日から先行配信中(フルで聴ける)"),
        p("「恋GAME」は、2026年10月7日に発売されるKO1KEYZのデビューシングル『KO1KEYZ』に収録されるカップリング曲です。",
          "公式サイトの収録内容によると、この曲が入っているのは初回限定盤Aと通常盤の2形態で、初回限定盤Bには収録されていません。",
          "もう1曲のカップリング「Key of Story」は初回限定盤Bと通常盤に入っているため、3曲すべてを聴きたいなら通常盤を選ぶのが確実でしょう。"),
        p("そして9月28日0時、「恋GAME」はCD発売より一足早く先行配信がスタートしました。",
          "公式Xでも配信開始が告知され、Spotify・Apple Musicなどのサービスでフルサイズを聴けるようになっています。"),
        xembed(OFFICIAL_X),
        p("それより前の9月10日には、シングルの収録曲を少しずつ聴ける「HIGHLIGHT MEDLEY」も公式YouTubeチャンネルで公開されていました。",
          "表題曲・カップリング曲の雰囲気をまとめてつかみたいときは、こちらの動画も便利です。"),
        embed(MEDLEY),
        p("ステージでの初披露は、8月21日にTOYOTA ARENA TOKYOで開かれた「KO1KEYZ 1ST FAN MEETING」東京公演の初日でした。",
          "セットリストでは1曲目の「DREAMER」に続く2曲目という早い位置に置かれ、ダンスブレイクではSIYOUNGがセンターに立ち、YURAとKOSUKEが馬跳びを見せる演出が話題になりました。",
          f"当日の流れは{a(L(11644), '1stファンミ初日のセトリ・座席表をまとめた記事')}で紹介しています。"),
        p("9月26日に幕張メッセで開催された「GirlsAward 2026 AUTUMN/WINTER」では、「KO1KEYZ」「ねこ」に続く3曲目、ステージの締めくくりとして「恋GAME」が披露されました。",
          "先行配信のわずか2日前というタイミングで、弾むようなパフォーマンスが会場を盛り上げています。",
          "この日のサインボードに書かれたKO1KEYZのロゴは、ゲーム画面を思わせるドット文字。",
          "曲の世界観に合わせたような遊び心も、ファンの間で注目を集めていました。"),
        note(f"ドット文字のロゴを含め、KO1KEYZの手書きロゴについては{a(L(13824), 'KO1KEYZのロゴは誰が書いてる？という記事')}で詳しくまとめています。"),
        PHOTO.replace("{alt}", "KO1KEYZ(コイキーズ)メンバー12人のプロフィール写真").replace("{src}", "出典:"),
        h2("「恋GAME」の歌割り(パート分け)一覧【全12人】"),
        ui.minibox("<strong>歌い出し:</strong>KOSUKE",
                   "<strong>曲のラスト:</strong>TOWA",
                   "<strong>毎サビ固定:</strong>YUKI(Clear)・KEITO(Push Push)・RYUJI(Final attack)"),
        p("SNSで話題になっているファンの聞き取りをもとに、12人がそれぞれどの場面を歌っているのかを曲の流れに沿って整理しました。",
          "配信音源をもとにした聞き取りと、ステージでの聞き取りの2種類を照らし合わせたところ、違いは1番の出だしを締める「Oh, yeah」の担当(音源ではRYOGA)くらいで、ほぼ同じ内容でした。",
          "歌詞の一言一句ではなく、どんな場面・フレーズを担当しているかという単位でまとめています。",
          "名前の色はメンバーカラーに対応させています(白のSIYOUNGのみ、読みやすさのためグレーで表示)。"),
        parts_table(("曲の展開", "歌うメンバー", "担当する場面・フレーズ"), PARTS_JA),
        p("「1番の出だし」「サビ後」などの区切りは、聞き取りの並びをもとにした目安です。",
          "公式の歌割りが発表されているわけではないため、ユニゾンやハモりの範囲は聞き方によって前後する可能性があります。",
          "10月7日にCDが発売されたら、歌詞カードと照らし合わせてみるのも面白そうです。"),
        h2("メンバー別のパート数は？KOSUKEが最多、TOWAが僅差で続く"),
        ui.minibox("<strong>最多:</strong>KOSUKE(11行)、2位はTOWA(10行)",
                   "<strong>続いて:</strong>ISSA・SIYOUNG(各9行)、YURA(8行)",
                   "<strong>少なくても存在感:</strong>RYUJI・KEITOは毎サビの決めフレーズを担当"),
        p("聞き取りの行数をメンバーごとに数えると、次のようになりました。",
          "1行の長さはフレーズによってまちまちなので、歌っている秒数とは必ずしも一致しない点には気をつけてください。"),
        grid(count_rows(("メンバー", "行数", "主な担当"), WHERE_JA, "行")),
        p(f"トップは{mk('KOSUKEの11行')}、1行差でTOWAの10行が続きます。",
          "KOSUKEは曲の歌い出しを任され、1番ではサビ前の「Combo attack」、2番では「恋人になろう」と告げる告白パートまで担当しています。",
          "TOWAは1番で「Tough」「装備」のパートとサビ前を歌い、2番の頭と曲の最後の「Again and again」も担当する、曲の最初から最後まで出ずっぱりの配置です。",
          "RYOGAは音源の聞き取りで1番の「Oh, yeah」が加わり、中盤の「We love game」や「マストアイテム」の一言と合わせて7行になりました。"),
        p("行数だけ見るとRYUJIとKEITOは3行ずつですが、どちらも毎回のサビで同じフレーズを任されている点が見逃せません。",
          "RYUJIは恋を「RPG」にたとえる決めのワンフレーズと、サビを締める「Final attack」を担当。",
          "KEITOはサビの「Push Push」と2番の「To the next round」を担当。",
          "ステージではTOWAの語尾を追いかける掛け合いも聞こえていて、短くても耳に残るパートがそろっています。"),
        h2("歌割りの注目ポイント！1番と2番でパートが入れ替わる"),
        ui.minibox("<strong>固定パート:</strong>YUKIの「Clear」、KEITOの「Push Push」、RYUJIの「Final attack」",
                   "<strong>入れ替わり:</strong>サビ前・サビ・フックのパートは1番と2番で担当が交代"),
        p("「恋GAME」の歌割りで面白いのは、同じメロディーが2回出てくる場面で、担当メンバーががらりと入れ替わる点です。",
          "たとえば1番の中盤でSHINHAENGとDAIKIが交互に歌ったフレーズは、2番ではYOSHIKIとRYOGAのコンビに引き継がれます。",
          "サビ前も、1番のTOWA→KOSUKEから、2番ではKOSUKE→DAIKIへとバトンが渡される形です。"),
        p("サビの中でも入れ替わりは続きます。",
          f"1サビの頭をYURAが歌ったのに対し、{mk('ラスサビの頭を任されたのはISSA')}。",
          "「共に旅する」から始まる3行と「レベル上げたい」の一言は、1サビではYOSHIKI→SHINHAENG、ラスサビではSHINHAENG→YOSHIKIと、2人がちょうど役割を交換しています。",
          "「Imma get it」のフックも、1回目はSIYOUNGとISSA、ラストはYURAとSIYOUNGが担当し、間に入る「マストアイテム Your love」の一言はRYOGAからDAIKIへ受け渡されています。"),
        p("その一方で、どのサビでも同じメンバーが歌う「固定パート」もあります。",
          "2回目の「キミとキミとClear」は必ずYUKI、「Push Push」は必ずKEITO、サビを締める「Final attack」は必ずRYUJI。",
          "入れ替わるパートと固定パートが組み合わさることで、12人が満遍なく目立ちつつ、サビのたびに「ここはこの人」という聞きどころも生まれています。"),
        p("曲の頭と終わりにも注目です。",
          "ゲーム開始の合図で始まる歌い出しはKOSUKE、最後の「Again and again」で曲を閉じるのはTOWA。",
          "KOSUKEとTOWAは「とわすけ」のコンビ名で親しまれる同い年の2人で、その2人が曲の入口と出口を担っているのも、ファンにはうれしいポイントでしょう。"),
        note(f"各メンバーの絵文字とカラーの対応は{a('https://chomoand-1.com/summary-of-ko1keyz-member-emoj-10560', 'KO1KEYZメンバー絵文字まとめの記事')}、カラー一覧は{a('https://chomoand-1.com/ko1keyz-no-color-10196', 'メンバーカラーの記事')}で確認できます。"),
        h2("「恋GAME」の歌詞に出てくるゲーム用語の意味は？"),
        ui.minibox("<strong>テーマ:</strong>恋をRPG(ロールプレイングゲーム)にたとえ、二人で協力してクリアを目指す",
                   "<strong>特徴:</strong>HPを「ハートポイント」と読み替えるなど、ゲーム用語を恋の言葉に置き換えている"),
        p("「恋GAME」の歌詞には、ゲームを遊ぶ人ならおなじみの言葉がたくさん登場します。",
          "ゲームに詳しくなくても歌詞の意味がすっと入ってくるよう、主なゲーム用語と、曲の中でどんな恋の場面にたとえられているのかを表にしました。"),
        grid(GAME_JA),
        p("ゲームの始まりを告げる起動音から始まり、モードを選び、装備を整え、アイテムを探し、ラウンドを重ね、最後の一撃でクリアを目指す。",
          "歌詞の流れは、まさに1本のゲームを最初から最後まで遊ぶような構成になっています。",
          "恋の始まりから、二人で力を合わせて気持ちを実らせるまでを、プレイの進行に重ねているわけです。"),
        p(f"なかでも印象的なのが、{mk('HPを「ハートポイント」と読み替えている')}ところ。",
          "ゲームのHPは体力を表す数字ですが、この曲ではキミの存在で満たされていく心の数値として描かれています。",
          "「Bad end」を避けるには協力が欠かせない、という一節も、一人では攻略できない恋を二人で乗り越えようとするメッセージとして受け取れそうです。"),
        p("12人のグループが歌うからこそ、「協力プレイ」というテーマがより生きてくるのもこの曲の魅力です。",
          "パートを細かく受け渡しながら1曲を進めていく歌割りそのものが、みんなでゲームを攻略していく様子と重なって聞こえてきます。"),
        h2("まとめ"),
        ui.summary([
            "「恋GAME」はデビューシングル『KO1KEYZ』(初回限定盤A・通常盤)に収録、10月7日発売",
            "8月21日の1stファンミ東京公演DAY1で初披露、9月26日のガルアワでも披露",
            "9月28日0時から先行配信スタート、CDは10月7日発売",
            "パート数はKOSUKEが11行で最多、TOWAが10行で2位、歌い出しはKOSUKE、ラストはTOWA",
            "YUKIの「Clear」、KEITOの「Push Push」、RYUJIの「Final attack」は毎サビ固定",
            "サビ前・サビ・フックは1番と2番で担当メンバーが入れ替わる",
            "歌詞は恋をRPGにたとえ、HPを「ハートポイント」と読み替えるなどゲーム用語が満載",
            "歌割りは配信音源とステージの聞き取りを照らし合わせたもので、公式発表ではない",
        ]),
        p("先行配信がはじまった今なら、フルサイズの音源で歌割りをじっくり確かめられます。",
          "この一覧を片手に配信を聴きながら、推しのパートを覚えてからステージ映像を見返してみてください！"),
        ui.quotebox("あわせて読みたい", [a(u, t) for u, t in REL["ja"]]),
    ]
    jp_sum = ("KO1KEYZのデビューシングル収録曲「恋GAME」の歌割りを12人分まとめました。"
              "9/28から先行配信中。最多はKOSUKE、毎サビ固定のパートや1番と2番の入れ替わり、歌詞のゲーム用語の意味も解説。")

    # ================================================================ KR
    kr_title = "KO1KEYZ '恋GAME' 가사・파트 분배는? 12명 총정리!"
    kr = [
        p("연애를 게임에 비유한 KO1KEYZ(코이키즈)의 신곡 '恋GAME(코이 GAME, 사랑 GAME)'.",
          "데뷔 싱글 발매에 앞서 2026년 9월 28일 0시부터 각 음원 사이트에서 선공개가 시작됐어요.",
          f"음원 받아쓰기로 파트를 세어 보니 {mk('가장 많은 파트를 부르는 멤버는 KOSUKE, 그 뒤를 TOWA가 바짝 쫓아요')}.",
          "이 글에서는 SNS에서 화제가 된 팬들의 받아쓰기(음원・무대 2종류)를 비교해 12명의 파트 분배를 정리하고, 1절과 2절의 파트 교대, 가사 속 게임 용어의 의미까지 소개해요."),
        ui.table("'恋GAME' 기본 정보", [
            ("곡명", "恋GAME"),
            ("수록", "DEBUT SINGLE 『KO1KEYZ』(초회 한정반 A・통상반 수록)"),
            ("선공개", f"2026년 9월 28일(일) 0:00~ {a(STREAM, '각 음원 사이트')}"),
            ("CD 발매일", "2026년 10월 7일(수)"),
            ("첫 공개", "2026년 8월 21일 'KO1KEYZ 1ST FAN MEETING' 도쿄 공연 DAY1(TOYOTA ARENA TOKYO)"),
            ("최근 무대", "2026년 9월 26일 'GirlsAward 2026 AUTUMN/WINTER'(마쿠하리 멧세)"),
            ("작사・작곡", "공식 사이트 수록 내용 페이지에는 미기재(발매 후 가사 카드에서 확인 예정)"),
        ]),
        ui.titlebox("이 글에서 알 수 있는 것", [
            "'恋GAME'은 어떤 곡?", "12명 파트 분배 목록", "멤버별 파트 수",
            "1절과 2절에서 바뀌는 파트・고정 파트", "가사 속 게임 용어의 의미"]),
        h2("'恋GAME'은 어떤 곡? 데뷔 싱글 커플링곡"),
        ui.minibox("<strong>위치:</strong>데뷔 싱글 『KO1KEYZ』 커플링곡(초회 한정반 A・통상반)",
                   "<strong>테마:</strong>연애를 게임에 비유한 팝하고 장난기 있는 러브송",
                   "<strong>듣는 법:</strong>9월 28일부터 선공개 중(풀버전)"),
        p("'恋GAME'은 2026년 10월 7일 발매되는 KO1KEYZ 데뷔 싱글 『KO1KEYZ』의 커플링곡이에요.",
          "공식 사이트에 따르면 초회 한정반 A와 통상반에 수록되고, 초회 한정반 B에는 들어 있지 않아요.",
          "또 다른 커플링곡 'Key of Story'는 초회 한정반 B와 통상반에 수록되니, 세 곡을 모두 듣고 싶다면 통상반이 확실해요."),
        p("그리고 9월 28일 0시, '恋GAME'이 CD 발매보다 먼저 선공개됐어요.",
          "공식 X에서도 공개 소식을 알렸고, Spotify・Apple Music 등에서 풀버전을 들을 수 있어요."),
        xembed(OFFICIAL_X),
        p("그보다 앞선 9월 10일에는 수록곡 일부를 들을 수 있는 'HIGHLIGHT MEDLEY'도 공식 YouTube에 공개됐어요."),
        embed(MEDLEY),
        p("첫 무대는 8월 21일 TOYOTA ARENA TOKYO에서 열린 'KO1KEYZ 1ST FAN MEETING' 도쿄 공연 첫날이었어요.",
          "세트리스트 2번째 곡으로 선보였고, 댄스 브레이크에서 SIYOUNG이 센터에 서고 YURA와 KOSUKE가 말뚝박기(등 짚고 넘기)를 하는 연출이 화제가 됐어요.",
          "9월 26일 마쿠하리 멧세 'GirlsAward 2026 AUTUMN/WINTER'에서는 'KO1KEYZ', 'ねこ'에 이어 마지막 곡으로 무대에 올랐고, 이날 사인보드의 KO1KEYZ 로고는 게임 화면 같은 도트 글씨였어요."),
        note(f"도트 글씨 로고를 포함한 KO1KEYZ 손글씨 로고 이야기는 {a(L(13829), 'KO1KEYZ 로고는 누가 쓸까? 글')}에서 볼 수 있어요."),
        PHOTO.replace("{alt}", "KO1KEYZ(코이키즈) 멤버 12명 프로필 사진").replace("{src}", "출처: "),
        h2("'恋GAME' 파트 분배 목록【12명 전원】"),
        ui.minibox("<strong>첫 소절:</strong>KOSUKE",
                   "<strong>엔딩:</strong>TOWA",
                   "<strong>매 후렴 고정:</strong>YUKI(Clear)・KEITO(Push Push)・RYUJI(Final attack)"),
        p("SNS에서 화제가 된 팬들의 받아쓰기를 바탕으로, 12명이 각각 어떤 장면을 부르는지 곡 흐름에 따라 정리했어요.",
          "음원 기반 받아쓰기와 무대 받아쓰기를 비교해 보니, 차이는 1절 도입의 'Oh, yeah' 담당(음원에서는 RYOGA) 정도로 거의 같았어요.",
          "가사 한 줄 한 줄이 아니라 어떤 장면・구절을 맡았는지 단위로 정리했어요.",
          "이름 색은 멤버 컬러에 맞췄어요(흰색인 SIYOUNG만 가독성을 위해 회색으로 표시)."),
        parts_table(("곡 전개", "멤버", "담당 장면・구절"), PARTS_KO),
        p("구간 구분은 받아쓰기 순서를 바탕으로 한 기준이에요.",
          "공식 파트 분배가 발표된 건 아니라서 유니즌・화음 범위는 듣는 방법에 따라 조금 다를 수 있어요."),
        h2("멤버별 파트 수는? KOSUKE가 최다, TOWA가 근소한 차이로 2위"),
        ui.minibox("<strong>최다:</strong>KOSUKE(11줄), 2위 TOWA(10줄)",
                   "<strong>다음:</strong>ISSA・SIYOUNG(각 9줄), YURA(8줄)"),
        p("받아쓰기 줄 수를 멤버별로 세면 다음과 같아요. 줄마다 길이가 달라서 부르는 초 수와 꼭 일치하지는 않아요."),
        grid(count_rows(("멤버", "줄 수", "주요 담당"), WHERE_KO, "줄")),
        p(f"1위는 {mk('KOSUKE의 11줄')}, 1줄 차이로 TOWA가 10줄이에요.",
          "KOSUKE는 첫 소절과 1절 후렴 전 'Combo attack', 2절 고백 파트까지 맡았고, TOWA는 1절 'Tough'・'장비' 파트와 후렴 전부터 곡의 마지막 'Again and again'까지 처음부터 끝까지 활약해요.",
          "RYOGA는 음원 받아쓰기에서 1절 'Oh, yeah'가 더해져 7줄이 됐어요.",
          "RYUJI와 KEITO는 3줄씩이지만 매 후렴마다 같은 구절을 맡아서, 듣자마자 알 수 있는 인상적인 파트예요."),
        h2("파트 분배 포인트! 1절과 2절에서 파트가 바뀐다"),
        ui.minibox("<strong>고정:</strong>YUKI 'Clear', KEITO 'Push Push', RYUJI 'Final attack'",
                   "<strong>교대:</strong>후렴 전・후렴・훅은 1절과 2절에서 담당이 바뀜"),
        p("같은 멜로디가 두 번 나오는 부분에서 담당 멤버가 완전히 바뀌는 게 이 곡의 재미예요.",
          "1절 중반에 SHINHAENG과 DAIKI가 번갈아 부른 구절은 2절에서 YOSHIKI와 RYOGA가 이어받고, 후렴 전도 1절 TOWA→KOSUKE에서 2절 KOSUKE→DAIKI로 바통이 넘어가요.",
          f"1절 후렴 첫머리는 YURA, {mk('마지막 후렴 첫머리는 ISSA')}가 맡았고, YOSHIKI와 SHINHAENG은 '함께 여행하는' 3줄과 '레벨 업' 한마디를 서로 바꿔 불러요."),
        p("반면 매 후렴 두 번째 '너와 너와 Clear'는 YUKI, 'Push Push'는 KEITO, 'Final attack'은 RYUJI로 고정이에요.",
          "첫 소절은 KOSUKE, 마지막은 TOWA로, '토와스케'로 불리는 동갑 콤비가 곡의 입구와 출구를 맡은 것도 팬에게는 반가운 포인트예요."),
        h2("'恋GAME' 가사 속 게임 용어의 뜻은?"),
        ui.minibox("<strong>테마:</strong>사랑을 RPG에 비유해 둘이 협력해서 클리어를 목표로 함",
                   "<strong>특징:</strong>HP를 '하트 포인트'로 바꿔 읽는 등 게임 용어를 사랑의 말로 치환"),
        p("가사에는 게임을 하는 사람이라면 익숙한 단어가 가득해요. 주요 용어와 곡 속 의미를 표로 정리했어요."),
        grid(GAME_KO),
        p("시작음으로 막을 열고, 모드를 고르고, 장비를 갖추고, 아이템을 찾고, 라운드를 거쳐 마지막 일격으로 클리어를 노리는 흐름은 게임 한 편을 처음부터 끝까지 플레이하는 구성이에요.",
          f"특히 {mk('HP를 \'하트 포인트\'로 바꿔 읽은')} 부분이 인상적이에요.",
          "12명이 파트를 주고받으며 곡을 이어 가는 모습 자체가 다 함께 게임을 공략하는 '협력 플레이'처럼 들려요."),
        h2("정리"),
        ui.summary([
            "'恋GAME'은 데뷔 싱글 『KO1KEYZ』(초회 한정반 A・통상반) 수록, 10월 7일 발매",
            "8월 21일 1st 팬미팅 도쿄 DAY1에서 첫 공개, 9월 26일 걸즈어워드에서도 무대",
            "9월 28일 0시부터 선공개, CD는 10월 7일 발매",
            "파트 수는 KOSUKE가 11줄로 최다, TOWA가 10줄로 2위, 첫 소절은 KOSUKE, 엔딩은 TOWA",
            "YUKI 'Clear', KEITO 'Push Push', RYUJI 'Final attack'은 매 후렴 고정",
            "가사는 사랑을 RPG에 비유, HP를 '하트 포인트'로 바꿔 읽는 등 게임 용어 가득",
            "파트 분배는 음원・무대 받아쓰기를 비교한 것으로 공식 발표는 아님",
        ]),
        p("선공개가 시작된 지금은 풀버전 음원으로 파트를 꼼꼼히 확인할 수 있어요.",
          "이 목록을 보면서 음원을 듣고, 최애의 파트를 외운 뒤 무대 영상을 다시 보는 것도 좋아요!"),
        ui.quotebox("함께 읽으면 좋은 글", [a(u, t) for u, t in REL["ko"]]),
    ]
    kr_sum = ("KO1KEYZ 데뷔 싱글 수록곡 '恋GAME'의 파트 분배를 12명 전원 정리했어요. "
              "9/28 선공개 중. 최다는 KOSUKE, 매 후렴 고정 파트와 1・2절 교대, 가사 속 게임 용어도 해설해요.")

    # ================================================================ EN
    en_title = "Who Sings What in KO1KEYZ's \"Koi GAME\"? Lyrics and All 12 Parts!"
    en = [
        p("\"Koi GAME\" (恋GAME, \"Love GAME\") is a new KO1KEYZ song that compares romance to a video game.",
          "Ahead of the CD release, it began streaming early on all major platforms at midnight JST on September 28, 2026.",
          f"Counting the parts from a transcription of the released audio, {mk('KOSUKE has the most lines, with TOWA just one behind')}.",
          "Comparing two fan transcriptions circulating on social media (one from the audio, one from live stages), this article lists all 12 members' parts, explains how parts swap between verse 1 and verse 2, and breaks down the gaming terms in the lyrics."),
        ui.table("\"Koi GAME\" at a glance", [
            ("Title", "恋GAME (Koi GAME)"),
            ("Included on", "DEBUT SINGLE \"KO1KEYZ\" (Limited Edition A and Regular Edition)"),
            ("Early streaming", f"From 0:00 JST, September 28, 2026 ({a(STREAM, 'streaming links')})"),
            ("CD release", "October 7, 2026 (Wed)"),
            ("First performed", "August 21, 2026, \"KO1KEYZ 1ST FAN MEETING\" Tokyo Day 1 (TOYOTA ARENA TOKYO)"),
            ("Recent stage", "September 26, 2026, \"GirlsAward 2026 AUTUMN/WINTER\" (Makuhari Messe)"),
            ("Credits", "Not listed on the official tracklist page yet (expected in the CD booklet)"),
        ]),
        ui.titlebox("What you'll learn", [
            "What kind of song \"Koi GAME\" is", "All 12 members' parts", "Line count by member",
            "Parts that swap and parts that stay fixed", "What the gaming terms in the lyrics mean"]),
        h2("What is \"Koi GAME\"? A B-side on the debut single"),
        ui.minibox("<strong>Release:</strong>B-side on debut single \"KO1KEYZ\" (Limited A and Regular)",
                   "<strong>Theme:</strong>A playful pop love song that treats romance like a game",
                   "<strong>Listen:</strong>Streaming in full since September 28"),
        p("\"Koi GAME\" is a B-side on KO1KEYZ's debut single \"KO1KEYZ,\" out October 7, 2026.",
          "According to the official site, it appears on Limited Edition A and the Regular Edition, but not on Limited Edition B.",
          "The other B-side, \"Key of Story,\" is on Limited Edition B and the Regular Edition, so the Regular Edition is the one to get if you want all three songs."),
        p("At midnight JST on September 28, \"Koi GAME\" was released for streaming ahead of the CD.",
          "The official X account announced it, and the full song is now on Spotify, Apple Music, and other services."),
        xembed(OFFICIAL_X),
        p("Earlier, on September 10, the official YouTube channel released a \"HIGHLIGHT MEDLEY\" with short previews of the single's songs."),
        embed(MEDLEY),
        p("The song was first performed on August 21 at TOYOTA ARENA TOKYO, on Day 1 of the \"KO1KEYZ 1ST FAN MEETING\" in Tokyo.",
          "It was second on the setlist, and the dance break, with SIYOUNG at center and YURA and KOSUKE doing leapfrog, became a talking point.",
          "They performed it again on September 26 at \"GirlsAward 2026 AUTUMN/WINTER\" at Makuhari Messe as the closer after \"KO1KEYZ\" and \"Neko,\" and there the KO1KEYZ logo on the sign board was drawn in game-style pixel letters."),
        note(f"For more on the handwritten KO1KEYZ logo, including the pixel version, see {a(L(13830), 'our article on who draws the KO1KEYZ logo')}."),
        PHOTO.replace("{alt}", "Profile photo of the 12 KO1KEYZ members").replace("{src}", "Source: "),
        h2("\"Koi GAME\" part distribution (all 12 members)"),
        ui.minibox("<strong>Opening line:</strong>KOSUKE",
                   "<strong>Final line:</strong>TOWA",
                   "<strong>Fixed every chorus:</strong>YUKI (\"Clear\"), KEITO (\"Push Push\"), RYUJI (\"Final attack\")"),
        p("Based on a fan transcription that has been circulating on social media, here is what each member sings, in song order.",
          "Comparing a transcription of the released audio with one from live stages, the only difference was who sings the \"Oh, yeah\" that closes verse 1 (RYOGA, per the audio).",
          "The table describes each scene or phrase rather than quoting every line.",
          "Name colors match each member's color (SIYOUNG's white is shown in gray for readability)."),
        parts_table(("Section", "Member", "Scene / phrase"), PARTS_EN),
        p("The section labels are approximate, based on the order of the transcription.",
          "No official part distribution has been published, so unison and harmony sections may vary depending on how you hear them."),
        h2("How many lines does each member sing? KOSUKE leads, TOWA close behind"),
        ui.minibox("<strong>Most:</strong>KOSUKE (11 lines), then TOWA (10)",
                   "<strong>Next:</strong>ISSA and SIYOUNG (9 each), YURA (8)"),
        p("Here's the line count per member. Lines vary in length, so this won't exactly match singing time."),
        grid(count_rows(("Member", "Lines", "Main parts"), WHERE_EN, "")),
        p(f"At the top is {mk('KOSUKE with 11 lines')}, followed by TOWA with 10.",
          "KOSUKE opens the song, sings the \"Combo attack\" pre-chorus in verse 1, and has the confession part in verse 2. TOWA sings the \"Tough\" and gear lines and the pre-chorus in verse 1, plus the song's final \"Again and again.\"",
          "RYOGA reaches 7 lines with the verse 1 \"Oh, yeah\" heard in the audio transcription.",
          "RYUJI and KEITO have only three lines each, but both get the same standout phrase in every chorus."),
        h2("Highlights: parts swap between verse 1 and verse 2"),
        ui.minibox("<strong>Fixed:</strong>YUKI's \"Clear,\" KEITO's \"Push Push,\" RYUJI's \"Final attack\"",
                   "<strong>Swapped:</strong>Pre-chorus, chorus, and hook parts change hands in verse 2"),
        p("When a melody comes back, the members singing it often change completely.",
          "The lines SHINHAENG and DAIKI trade in verse 1 go to YOSHIKI and RYOGA in verse 2, and the pre-chorus passes from TOWA and KOSUKE to KOSUKE and DAIKI.",
          f"YURA opens the first chorus, while {mk('ISSA opens the final chorus')}, and YOSHIKI and SHINHAENG swap the \"traveling together\" lines and the \"level up\" line."),
        p("Meanwhile, the second \"Kimi to kimi to Clear\" always goes to YUKI, \"Push Push\" to KEITO, and \"Final attack\" to RYUJI.",
          "KOSUKE opens the song and TOWA closes it, a nice touch for fans of the same-age duo known as \"Towasuke.\""),
        h2("What do the gaming terms in \"Koi GAME\" mean?"),
        ui.minibox("<strong>Theme:</strong>Love as an RPG that two people clear together",
                   "<strong>Signature twist:</strong>HP is reread as \"heart points\""),
        p("The lyrics are packed with words any gamer will recognize. Here's what they mean in games and in the song."),
        grid(GAME_EN),
        p("The song moves like a full playthrough: a start beep, choosing a mode, gearing up, finding items, going round by round, and landing the final attack to clear the game.",
          f"The standout idea is {mk('reading HP as \"heart points\"')}, filled up by the person you love.",
          "With 12 members passing lines back and forth, the song itself sounds like a co-op game played together."),
        h2("Summary"),
        ui.summary([
            "\"Koi GAME\" is on the debut single \"KO1KEYZ\" (Limited A and Regular), out October 7",
            "First performed August 21 at the Tokyo fan meeting, and again at GirlsAward on September 26",
            "Streaming since midnight JST on September 28; the CD is out October 7",
            "KOSUKE has the most lines (11), TOWA is second (10); KOSUKE opens and TOWA closes",
            "YUKI's \"Clear,\" KEITO's \"Push Push,\" and RYUJI's \"Final attack\" are fixed every chorus",
            "The lyrics treat love as an RPG, even reading HP as \"heart points\"",
            "The parts compare audio and live transcriptions and are not official",
        ]),
        p("Now that the full song is streaming, you can check every part in detail.",
          "Listen along with this guide, learn your bias's lines, and then rewatch the stage clips!"),
        ui.quotebox("Related articles", [a(u, t) for u, t in REL["en"]]),
    ]
    en_sum = ("All 12 members' parts in KO1KEYZ's \"Koi GAME\" from the debut single. Streaming since Sept 28; KOSUKE leads, "
              "plus the fixed chorus parts, verse swaps, and the gaming terms in the lyrics.")
    join = lambda bl: "\n\n".join(bl)
    return (jp_title, join(jp), jp_sum), (kr_title, join(kr), kr_sum), (en_title, join(en), en_sum)


def upload(path, ctype):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media",
                      headers={**HA, "Content-Type": ctype, "Content-Disposition": f'attachment; filename="{path.name}"'},
                      data=path.read_bytes())
    r.raise_for_status()
    return r.json()["id"]


def post_draft(title, content, slug, lang, cats, media, summary):
    payload = {"title": title, "content": content, "slug": slug, "status": "draft", "lang": lang,
               "categories": cats, "featured_media": media, "author": 2,
               "meta": {"jetpack_publicize_message": summary}}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers={**HA, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    return r.json()


def make_eyecatch():
    tool = str(ROOT / "tools" / "eyecatch_koikeyz.py")
    subprocess.run([sys.executable, tool, "--top", "「恋GAME」の歌割りは？", "--main", "KO1KEYZ",
                    "--bottom", "歌詞と12人のパート！", "--out", str(EYE_JP), "--seed", "23"], check=True)
    subprocess.run([sys.executable, tool, "--top", "'恋GAME' 파트 분배는?", "--main", "KO1KEYZ",
                    "--bottom", "가사와 12명 파트!", "--out", str(EYE_KR), "--seed", "23", "--lang", "kr"], check=True)


IDS = {"ja": 13887, "ko": 13888, "en": 13889}


def update_draft(pid, content, summary):
    payload = {"content": content, "status": "draft", "meta": {"jetpack_publicize_message": summary}}
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers={**HA, "Content-Type": "application/json"},
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    out = build()
    for (t, c, s), name in zip(out, ("JP", "KR", "EN")):
        assert "<hr" not in c
        print(name, len(t), t, "chars:", len(re.sub(r"<[^>]+>|<!--.*?-->", "", c, flags=re.S)), "sum:", len(s))
    Path(ROOT / "articles" / "ko1keyz_koigame_utawari.html").write_text(out[0][1], encoding="utf-8")
    if "--dry" in sys.argv:
        sys.exit(0)
    if "--update" in sys.argv:
        for (t, c, sm), lang in zip(out, ("ja", "ko", "en")):
            r = update_draft(IDS[lang], c, sm)
            print("updated", r["id"], r["status"])
        sys.exit(0)
    make_eyecatch()
    (jt, jc, js), (kt, kc, ks), (et, ec, es) = out
    jp_eye = upload(EYE_JP, "image/png")
    kr_eye = upload(EYE_KR, "image/png")
    jp = post_draft(jt, jc, BASE_SLUG, "ja", [66, 62], jp_eye, js)
    print("JP", jp["id"], jp["slug"], jp["link"])
    kr = post_draft(kt, kc, BASE_SLUG + "-kr", "ko", [74, 70], kr_eye, ks)
    print("KR", kr["id"], kr["slug"], kr["link"])
    en = post_draft(et, ec, BASE_SLUG + "-en", "en", [110, 112], jp_eye, es)
    print("EN", en["id"], en["slug"], en["link"])
    print("eyecatch", jp_eye, kr_eye)
