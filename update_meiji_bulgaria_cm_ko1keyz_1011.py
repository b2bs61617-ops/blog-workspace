# -*- coding: utf-8 -*-
"""明治ブルガリアCM=KO1KEYZ説の記事(公開済み JP14529/KR14531/EN14532)に10/11の続報を追記する。
続報: 10/11(日)正午 https://x.com/meiji_BY_cp/status/2109116791297589378
      「明日からのスケジュールです🤟」+ SCHEDULER画像(10/12 Mon=鍵穴に「？」、10/13 Tue=付箋「叫んでもらう」、10/14は見切れ)
公開済みなので title/slug は送らず、status は publish のまま content だけ更新する。
"""
import base64, json, sys
from pathlib import Path

import requests

sys.dont_write_bytecode = True
ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = load_env(ROOT / ".env")
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}

AB, AL, BG, TH = "#d9d4cc", "#8a8378", "#f7f6f3", "#eeebe6"
TW_SCHED = "https://twitter.com/meiji_BY_cp/status/2109116791297589378"


def tweet(url, lang):
    return f"""<!-- wp:html -->
<blockquote class="twitter-tweet" data-lang="{lang}" data-dnt="true"><a href="{url}">{url}</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
<!-- /wp:html -->"""


def minibox(rows):
    ps = [f'<p style="margin:{"0" if i == 0 else "4px 0 0 0"};"><strong>{k}</strong>{v}</p>' for i, (k, v) in enumerate(rows)]
    return f"""<!-- wp:html -->
<div style="border:1px solid {AB};border-left:4px solid {AL};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{BG};">
{chr(10).join(ps)}
</div>
<!-- /wp:html -->"""


def table(header, rows):
    th = "".join(f'<td style="background:{AL};color:#fff;border:1px solid {AB};padding:8px 10px;font-weight:bold;">{h}</td>' for h in header)
    trs = [f"<tr>{th}</tr>"]
    for i, r in enumerate(rows):
        bg = "#fff" if i % 2 == 0 else BG
        trs.append("<tr>" + "".join(f'<td style="background:{bg};border:1px solid {AB};padding:8px 10px;">{c}</td>' for c in r) + "</tr>")
    return ("<!-- wp:table -->\n<figure class=\"wp-block-table\"><table class=\"has-fixed-layout\"><tbody>"
            + "".join(trs) + "</tbody></table></figure>\n<!-- /wp:table -->")


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def p(t):
    return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"


def mark(t, big=False):
    s = ' style="font-size:1.15em;"' if big else ""
    return f'<strong><span class="swl-marker mark_yellow"{s}>{t}</span></strong>'


def row(k, v):
    return f'<tr><td style="background:{TH};border:1px solid {AB};padding:8px 12px;width:32%;">{k}</td><td style="border:1px solid {AB};padding:8px 12px;">{v}</td></tr>'


def li(t):
    return f"<li>{t}</li>"


# ============================== JP ==============================
JP_SECTION = "\n\n".join([
    h2("10月12日・13日に何がある？明治が出したスケジュール"),
    minibox([("10月12日(月)：", "鍵穴に「？」"), ("10月13日(火)：", "「叫んでもらう」")]),
    p("2026年10月11日のお昼12時、明治ブルガリアヨーグルトの公式Xに3回目の投稿が出ました。<br>\n"
      "「明日からのスケジュールです🤟」という短い文に、「SCHEDULER」と書かれたカレンダーの画像が付いています。"),
    tweet(TW_SCHED, "ja"),
    p("カレンダーに書かれている内容をまとめると、次のとおりです。"),
    table(["日付", "カレンダーの中身", "考えられること"], [
        ("10月12日(月)", "青い鍵穴の中に「？」", "鍵穴の謎が解ける＝グループ名の発表"),
        ("10月13日(火)", "付箋に手書きで「叫んでもらう」", "メンバーが叫ぶ動画やCMの公開"),
        ("10月14日(水)", "画像の端で見切れていて中身は見えない", "まだ続きの企画がありそう"),
    ]),
    p(f"いちばん気になるのは、10月12日の{mark('鍵穴の「？」', True)}です。<br>\n"
      "2回目の投稿では「モヤモヤ解決の【鍵】？🔑」と書かれていて、メモのまとめには鍵が開いた絵文字(🔓)が付いていました。<br>\n"
      "鍵を差しこむ「鍵穴」がそのまま12日の予定になっているので、この日に「とあるグループ」の正体が明かされる流れと考えるのが自然です。<br>\n"
      "グループ名に「KEY」が入るKO1KEYZにとっては、これ以上ないくらいぴったりの演出ですね。"),
    p("10月12日はスポーツの日で祝日なので、学校やお仕事が休みの人も多い日です。<br>\n"
      "これまでの2回の投稿はどちらもお昼12時に出ているので、12日も同じ時間に動きがあるかもしれません。"),
    p(f"続く10月13日の付箋には、{mark('「叫んでもらう」')}と書かれています。<br>\n"
      "ハッシュタグの「#全部腸内細菌のせいにして叫べ」とつながる言葉で、メンバーが実際に叫ぶ動画やCM本編が公開される日だとみられます。<br>\n"
      "誰に何を叫んでもらうのかはまだ書かれていないので、ファンから「叫んでほしいこと」を募る企画になる可能性もありそうです。<br>\n"
      "10月14日の欄は画像の右上で切れていて、まだ続きの予定が用意されているように見えます。"),
])

JP_OLD_ROW = '<tr><td style="background:#eeebe6;border:1px solid #d9d4cc;padding:8px 12px;width:32%;">2回目</td><td style="border:1px solid #d9d4cc;padding:8px 12px;">2026年10月10日(土)正午、「打ち合わせメモ」の画像</td></tr>'
JP_REPLACES = [
    (JP_OLD_ROW, JP_OLD_ROW + "\n" + row("3回目", "2026年10月11日(日)正午、「明日からのスケジュール」の画像")),
    ('<li>ほかのヒント</li>', '<li>ほかのヒント</li>\n' + li("10月12日・13日の予告スケジュール")),
    ("※2026年10月10日時点で、明治・KO1KEYZのどちらからも出演グループの正式な発表は出ていません。",
     "※2026年10月11日時点で、明治・KO1KEYZのどちらからも出演グループの正式な発表は出ていません(10月12日に何かが明かされる予告あり)。"),
    ("CMの公開にあわせて、ファンから「叫びたいこと」を集める企画が用意されている可能性もありそうです。<br>\n"
     "12人がそれぞれのモヤモヤを叫ぶようなCMになるのか、続報が気になります。",
     "CMの公開にあわせて、ファンから「叫びたいこと」を集める企画が用意されている可能性もありそうです。<br>\n"
     "10月11日に出たスケジュールでも、10月13日の欄に「叫んでもらう」と書かれていました。<br>\n"
     "12人がそれぞれのモヤモヤを叫ぶようなCMになるのか、13日の公開が楽しみです。"),
    ("10月10日時点で、明治・KO1KEYZとも正式な発表はまだ",
     "10月11日に「明日からのスケジュール」が出て、10月12日は鍵穴に「？」、13日は「叫んでもらう」の予定<br>\n"
     + '<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid #8a8378;border-radius:3px;color:#8a8378;font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>'
     + "10月11日時点で正式な発表はまだで、10月12日にグループ名が明かされるとみられる"),
    ("正式な発表とCMの公開を楽しみに待ちながら、ひと足先にONE SHOTを飲んで「腸活」を始めておくのもよさそうですね！",
     "10月12日の「鍵穴」の日を楽しみに待ちながら、ひと足先にONE SHOTを飲んで「腸活」を始めておくのもよさそうですね！"),
]
JP_ANCHOR ='<h2 class="wp-block-heading">CMの商品は？明治ブルガリアのむヨーグルトLB81 ONE SHOT</h2>'

# ============================== KR ==============================
KR_SECTION = "\n\n".join([
    h2("10월 12일・13일에는 무슨 일이? 메이지가 공개한 스케줄"),
    minibox([("10월 12일(월): ", "열쇠 구멍에 '?'"), ("10월 13일(화): ", "'외치게 한다(叫んでもらう)'")]),
    p("2026년 10월 11일 낮 12시, 메이지 불가리아 요구르트 공식 X에 세 번째 게시물이 올라왔습니다.<br>\n"
      "'내일부터의 스케줄입니다🤟'라는 짧은 글과 함께 'SCHEDULER'라고 적힌 달력 이미지가 붙어 있습니다."),
    tweet(TW_SCHED, "ko"),
    table(["날짜", "달력 내용", "예상"], [
        ("10월 12일(월)", "파란 열쇠 구멍 안에 '?'", "열쇠 구멍의 수수께끼가 풀린다 = 그룹명 발표"),
        ("10월 13일(화)", "포스트잇에 손글씨로 '叫んでもらう(외치게 한다)'", "멤버가 외치는 영상이나 CM 공개"),
        ("10월 14일(수)", "이미지 끝에서 잘려 보이지 않음", "아직 이어지는 기획이 있을 듯"),
    ]),
    p(f"가장 궁금한 것은 10월 12일의 {mark('열쇠 구멍 속 \"?\"', True)}입니다.<br>\n"
      "두 번째 게시물에는 '답답함을 해결할 【열쇠】? 🔑'라는 문장이 있었고, 메모의 정리에는 열린 자물쇠(🔓)가 붙어 있었습니다.<br>\n"
      "열쇠를 꽂는 '열쇠 구멍'이 12일의 일정으로 그려져 있어, 이날 '어느 그룹'의 정체가 밝혀질 가능성이 높아 보입니다.<br>\n"
      "그룹명에 'KEY'가 들어가는 KO1KEYZ에게 딱 맞는 연출이네요."),
    p("10월 12일은 일본의 공휴일(스포츠의 날)이고, 지금까지 두 번의 게시물은 모두 낮 12시(일본 시간)에 올라왔습니다.<br>\n"
      "10월 13일 포스트잇의 '외치게 한다'는 해시태그 '#全部腸内細菌のせいにして叫べ'와 이어지는 말로, 멤버가 실제로 외치는 영상이나 CM 본편이 공개되는 날로 보입니다.<br>\n"
      "10월 14일 칸은 이미지 오른쪽 위에서 잘려 있어, 이후에도 일정이 이어질 것 같습니다."),
])
KR_OLD_ROW = '<tr><td style="background:#eeebe6;border:1px solid #d9d4cc;padding:8px 12px;width:32%;">2번째</td><td style="border:1px solid #d9d4cc;padding:8px 12px;">2026년 10월 10일(토) 정오, \'회의 메모\' 이미지</td></tr>'
KR_REPLACES = [
    (KR_OLD_ROW, KR_OLD_ROW + "\n" + row("3번째", "2026년 10월 11일(일) 정오, '내일부터의 스케줄' 이미지")),
    ("※2026년 10월 10일 기준, 메이지와 KO1KEYZ 모두 출연 그룹을 공식 발표하지 않았습니다.",
     "※2026년 10월 11일 기준, 메이지와 KO1KEYZ 모두 출연 그룹을 공식 발표하지 않았습니다(10월 12일에 무언가가 공개된다는 예고 있음)."),
    ("10월 10일 기준 공식 발표는 아직",
     "10월 11일 '내일부터의 스케줄' 공개, 12일은 열쇠 구멍에 '?', 13일은 '외치게 한다'<br>\n"
     + '<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid #8a8378;border-radius:3px;color:#8a8378;font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>'
     + "10월 11일 기준 공식 발표는 아직, 10월 12일에 그룹명이 밝혀질 것으로 보임"),
    ("공식 발표와 CM 공개를 기대하며 기다려 보면 좋겠네요!",
     "10월 12일 '열쇠 구멍'의 날을 기대하며 기다려 보면 좋겠네요!"),
]
KR_ANCHOR = '<h2 class="wp-block-heading">CM 상품은? 메이지 불가리아 마시는 요구르트 LB81 ONE SHOT</h2>'

# ============================== EN ==============================
EN_SECTION = "\n\n".join([
    h2("What's coming on Oct 12 and 13? Meiji's schedule teaser"),
    minibox([("Oct 12 (Mon): ", "A keyhole with a \"?\""), ("Oct 13 (Tue): ", "\"We'll have them shout\"")]),
    p("At noon on October 11, 2026, Meiji Bulgaria Yogurt's official X account posted a third time.<br>\n"
      "The short caption reads \"Here's the schedule starting tomorrow 🤟,\" with a calendar image titled \"SCHEDULER.\""),
    tweet(TW_SCHED, "en"),
    table(["Date", "What the calendar shows", "What it likely means"], [
        ("Oct 12 (Mon)", "A blue keyhole with a \"?\" inside", "The mystery is \"unlocked\": the group is revealed"),
        ("Oct 13 (Tue)", "A sticky note reading 叫んでもらう (\"we'll have them shout\")", "A video or the commercial with the members shouting"),
        ("Oct 14 (Wed)", "Cut off at the edge of the image", "More plans seem to follow"),
    ]),
    p(f"The biggest hint is the {mark('keyhole with a \"?\" on October 12', True)}.<br>\n"
      "The second post called this \"the 【KEY】🔑 to clearing up that foggy feeling,\" and the memo's summary had an unlocked padlock (🔓).<br>\n"
      "With a keyhole on the calendar, October 12 looks like the day the \"certain group\" is revealed, a perfect fit for a group with \"KEY\" in its name."),
    p("October 12 is Sports Day, a public holiday in Japan, and both earlier posts went up at noon JST.<br>\n"
      "The October 13 note ties in with the hashtag #全部腸内細菌のせいにして叫べ, so that day will likely bring a video or the commercial itself with the members shouting.<br>\n"
      "The October 14 slot is cut off at the top right of the image, suggesting the campaign continues after that."),
])
EN_OLD_ROW = '<tr><td style="background:#eeebe6;border:1px solid #d9d4cc;padding:8px 12px;width:32%;">2nd post</td><td style="border:1px solid #d9d4cc;padding:8px 12px;">Oct 10, 2026 (Sat) at noon JST: "meeting memo" image</td></tr>'
EN_REPLACES = [
    (EN_OLD_ROW, EN_OLD_ROW + "\n" + row("3rd post", "Oct 11, 2026 (Sun) at noon JST: \"schedule starting tomorrow\" image")),
    ("* As of Oct 10, 2026, neither Meiji nor KO1KEYZ has officially named the group.",
     "* As of Oct 11, 2026, neither Meiji nor KO1KEYZ has officially named the group (a reveal is teased for Oct 12)."),
    ("No official announcement as of Oct 10",
     "On Oct 11, Meiji posted a schedule: a keyhole with a \"?\" on Oct 12 and \"we'll have them shout\" on Oct 13<br>\n"
     + '<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid #8a8378;border-radius:3px;color:#8a8378;font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>'
     + "No official announcement as of Oct 11; the group is likely revealed on Oct 12"),
    ("Let's look forward to the official announcement and the commercial!",
     "Let's look forward to the \"keyhole\" reveal on October 12!"),
]
EN_ANCHOR = '<h2 class="wp-block-heading">The product: Meiji Bulgaria Drinking Yogurt LB81 ONE SHOT</h2>'


def apply(raw, section, replaces, anchor):
    assert TW_SCHED not in raw, "already updated"
    for old, new in replaces:
        assert raw.count(old) == 1, f"not found exactly once: {old[:60]}"
        raw = raw.replace(old, new)
    block = "<!-- wp:heading -->\n" + anchor
    assert raw.count(block) == 1, f"anchor missing: {anchor}"
    return raw.replace(block, section + "\n\n" + block)


def main(dry):
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    for pid, section, replaces, anchor in [
        (14529, JP_SECTION, JP_REPLACES, JP_ANCHOR),
        (14531, KR_SECTION, KR_REPLACES, KR_ANCHOR),
        (14532, EN_SECTION, EN_REPLACES, EN_ANCHOR),
    ]:
        r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=H)
        r.raise_for_status()
        post = r.json()
        new = apply(post["content"]["raw"], section, replaces, anchor)
        print(pid, post["status"], len(post["content"]["raw"]), "->", len(new))
        if out:
            (out / f"{pid}_new.html").write_text(new, encoding="utf-8")
        if dry:
            continue
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}",
                          headers={**H, "Content-Type": "application/json"},
                          data=json.dumps({"content": new, "status": post["status"]}).encode("utf-8"))
        r.raise_for_status()
        chk = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=H).json()
        assert TW_SCHED in chk["content"]["raw"], f"{pid} not reflected"
        print(pid, "updated", chk["modified"], chk["status"])


if __name__ == "__main__":
    main(dry=(len(sys.argv) > 1 and sys.argv[1] == "--dry"))
