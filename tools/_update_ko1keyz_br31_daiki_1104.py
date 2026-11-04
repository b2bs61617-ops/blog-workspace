# -*- coding: utf-8 -*-
"""Add DAIKI's double (10/16 Makestar fansign, 2htmzp 11/3) to the published KO1KEYZ Baskin-Robbins flavor articles (JP15262/KR15266/EN15267).
Edits the current raw content in place; never sends title/slug."""
import json, base64, urllib.request, sys

REPO = r"C:\Users\s30se\Desktop\blog-workspace"
DRY = "--dry" in sys.argv
env = {}
for line in open(REPO + r"\.env", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip().strip('"')
U = env["WP_KOIKEYS_USERNAME"]; P = env["WP_KOIKEYS_APP_PASSWORD"]; BASE = env["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f"{U}:{P}".encode()).decode()


def api(path, body=None, method="GET"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Authorization", "Basic " + AUTH)
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


def upload_media(path, filename):
    req = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=open(path, "rb").read(), method="POST")
    req.add_header("Authorization", "Basic " + AUTH)
    req.add_header("Content-Type", "image/jpeg")
    req.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


SRC = {"daiki": "https://x.com/2htmzp/status/2117582368244732105"}
ALTS = {
    "daiki": {"ja": "10月16日のサイン会でラムレーズンとストロベリーチーズケーキを選んだDAIKI", "ko": "10월 16일 팬사인회에서 럼 레이즌과 스트로베리 치즈케이크를 고른 DAIKI", "en": "DAIKI choosing Rum Raisin and Strawberry Cheesecake at the Oct 16 fan signing"},
}
CAP = {"ja": "出典:", "ko": "출처:", "en": "Source: "}
media = {}
if not DRY:
    for key in ALTS:
        m = upload_media(REPO + rf"\images\ko1keyz_br31_{key}.jpg", f"ko1keyz_br31_{key}.jpg")
        s = m["media_details"]["sizes"]
        full = (m["source_url"], m["media_details"]["width"], m["media_details"]["height"])
        media[key] = {"full": full,
                      "large": (s["large"]["source_url"], s["large"]["width"], s["large"]["height"]) if "large" in s else full,
                      "medium": (s["medium"]["source_url"], s["medium"]["width"], s["medium"]["height"])}
        print("img", key, m["id"])
else:
    for key in ALTS:
        media[key] = {"full": ("X", 830, 880), "large": ("X", 830, 880), "medium": ("X", 283, 300)}


def fig(key, lang):
    d = media[key]; L = d["large"]; M = d["medium"]; F = d["full"]
    return ('<figure class="wp-block-image size-large" style="margin:8px 0 0 0;"><img src="' + L[0] + '" alt="' + ALTS[key][lang].replace('"', "&quot;") + '" '
            f'width="{L[1]}" height="{L[2]}" style="max-width:100%;height:auto;" '
            f'srcset="{M[0]} {M[1]}w, {L[0]} {L[1]}w, {F[0]} {F[1]}w" sizes="(max-width: 1024px) 100vw, 1024px">\n'
            f'<figcaption class="wp-element-caption" style="text-align:center;font-size:12px;">{CAP[lang]}{SRC[key]}</figcaption></figure>')


TD = '<td style="border:1px solid #ccc;padding:8px;">'
TDZ = '<td style="border:1px solid #ccc;padding:8px;background:#f7f5f2;">'


def row(cells, zebra):
    td = TDZ if zebra else TD
    return "<tr>" + "".join(f"{td}{c}</td>" for c in cells) + "</tr>"


def box(title, paras, img):
    ps = "\n".join(f'<p style="margin:0 0 8px 0;">{p}</p>' for p in paras)
    return ('<!-- wp:html -->\n<div style="border:1px solid #d8d4cd;border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">\n'
            f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;color:#8a8378;">{title}</p>\n{ps}\n{img}\n</div>\n<!-- /wp:html -->\n\n')


def rep(c, old, new, count=1):
    n = c.count(old)
    assert n == count, (n, old[:80])
    return c.replace(old, new)


def replace_box(c, title_prefix, new_box):
    """Replace the whole wp:html member box whose title starts with title_prefix."""
    i = c.index('color:#8a8378;">' + title_prefix)
    start = c.rindex("<!-- wp:html -->", 0, i)
    end = c.index("<!-- /wp:html -->", i) + len("<!-- /wp:html -->\n\n")
    return c[:start] + new_box + c[end:]


def add_flavor_row(c, marker, cells, zebra):
    i = c.index(marker); j = c.index("</tbody>", i)
    return c[:j] + row(cells, zebra) + "\n" + c[j:]


def member_row(c, old_cells, new_cells):
    return rep(c, "<tr>" + "".join(f"{TD}{x}</td>" for x in old_cells) + "</tr>",
                  "<tr>" + "".join(f"{TD}{x}</td>" for x in new_cells) + "</tr>")


# ---------------- JP ----------------
def jp(c):
    c = member_row(c, ["DAIKI", "ストロベリーチーズケーキ", "9月のオンライントーク会"],
                      ["DAIKI", "ストロベリーチーズケーキ(ダブルならラムレーズン＋ストロベリーチーズケーキ)", "9月のオンライントーク会・10月16日のサイン会"])
    daiki = box("DAIKI:ラムレーズン＋ストロベリーチーズケーキ", [
        "DAIKIさん(加藤大樹さん、2004年10月8日生まれ・愛知県出身)は、9月のオンライントーク会で好きなサーティワンの味を「ストロベリーチーズケーキ」と答えています。<br>9月13日のトーク会では、アイドル以外でなりたい職業を聞かれて「アイスクリームを作る、サーティワンの人」と答えていました。<br>好きな味だけでなく、お店で働く側にもあこがれているのがDAIKIさんらしいところです。",
        "10月16日のサイン会では、ファンに「サーティワンでダブル選ぶとしたら？」と聞かれ、「2つね！」と笑いながらメニュー表をのぞきこみました。<br>口元に手を当ててしばらく悩んだすえ、1つ目は<strong>「ラムレーズンと〜」</strong>、2つ目は<strong>「ストロベリーチーズケーキ！」</strong>です。<br>9月のトーク会で答えたストロベリーチーズケーキを、サイン会でもしっかり選んでいて、本当にお気に入りの味なのが分かります。",
        "セット名を聞かれると、ファンの「だいきセットみたいな！」というヒントには乗らず、「えーっと」と考えてからつけた名前は<strong>「KO1(恋)しようアイスパーティー」</strong>でした。<br>グループ名のKO1KEYZ(コイキーズ)の「KO1」と「恋しよう」をかけた、リーダーらしいネーミングです。",
        "ラムレーズンは、ラム風味のレーズンが入ったアイスクリームです。<br>甘ずっぱいストロベリーチーズケーキと、少し大人っぽいラムレーズンの組み合わせになりました。",
        "トーク会でのDAIKIさんの答えは、<a href=\"https://chomoand-1.com/daiki-karaoke-johnnys-songs-ko1keyz-13517\">DAIKIがカラオケで歌うジャニーズ曲をまとめた記事</a>でも紹介しています。",
    ], fig("daiki", "ja"))
    c = replace_box(c, "DAIKI:", daiki)
    c = add_flavor_row(c, ">2種類のココアを使ったコク深いチョコレートアイス<", ["ラムレーズン", "ラム風味のレーズン入りアイスクリーム", "DAIKI", "－"], False)
    c = rep(c, "&#10003; DAIKIはストロベリーチーズケーキで、なりたい職業は「サーティワンの人」",
               "&#10003; DAIKIはラムレーズン＋ストロベリーチーズケーキの「KO1しようアイスパーティー」で、なりたい職業は「サーティワンの人」")
    return c


# ---------------- KR ----------------
def kr(c):
    c = member_row(c, ["DAIKI", "스트로베리 치즈케이크", "9월 온라인 토크회"],
                      ["DAIKI", "스트로베리 치즈케이크(더블은 럼 레이즌+스트로베리 치즈케이크)", "9월 온라인 토크회・10월 16일 팬사인회"])
    daiki = box("DAIKI: 럼 레이즌+스트로베리 치즈케이크", [
        "DAIKI(가토 다이키, 2004년 10월 8일생・아이치현 출신)는 9월 온라인 토크회에서 좋아하는 서티원 맛을 '스트로베리 치즈케이크'라고 답했습니다.<br>9월 13일 토크회에서는 아이돌 말고 되고 싶은 직업을 묻자 '아이스크림을 만드는, 서티원 사람'이라고 답했습니다.<br>좋아하는 맛뿐 아니라 가게에서 일하는 쪽에도 로망이 있다는 점이 DAIKI다운 모습입니다.",
        "10월 16일 팬사인회에서는 팬이 '배라에서 더블로 고른다면?'이라고 묻자 '두 개!'라며 웃으면서 메뉴표를 들여다봤습니다.<br>입가에 손을 대고 한참 고민한 끝에 첫 번째는 <strong>'럼 레이즌이랑~'</strong>, 두 번째는 <strong>'스트로베리 치즈케이크!'</strong>였습니다.<br>9월 토크회에서 답한 스트로베리 치즈케이크를 팬사인회에서도 골라, 정말 좋아하는 맛이라는 걸 알 수 있습니다.",
        "세트 이름을 묻자 팬의 '다이키 세트 같은 느낌으로!'라는 힌트 대신 '음~' 하고 생각한 뒤 붙인 이름은 <strong>'KO1(코이)하자 아이스크림 파티'</strong>였습니다.<br>일본어 'KO1しよう(코이시요우)'는 '사랑하자'라는 뜻의 '恋しよう'와 발음이 같아, 그룹명 KO1KEYZ의 'KO1'과 엮은 리더다운 작명입니다.",
        "럼 레이즌은 럼 풍미의 건포도가 들어간 아이스크림입니다.<br>새콤달콤한 스트로베리 치즈케이크와 조금 어른스러운 럼 레이즌의 조합이 됐습니다.",
    ], fig("daiki", "ko"))
    c = replace_box(c, "DAIKI:", daiki)
    c = add_flavor_row(c, ">두 종류의 코코아를 사용한 진한 초콜릿 아이스<", ["럼 레이즌", "럼 풍미 건포도가 들어간 아이스크림", "DAIKI", "－"], False)
    c = rep(c, "&#10003; DAIKI는 스트로베리 치즈케이크, 되고 싶은 직업은 '서티원 사람'",
               "&#10003; DAIKI는 럼 레이즌+스트로베리 치즈케이크의 'KO1하자 아이스크림 파티', 되고 싶은 직업은 '서티원 사람'")
    return c


# ---------------- EN ----------------
def en(c):
    c = member_row(c, ["DAIKI", "Strawberry Cheesecake", "September online talk event"],
                      ["DAIKI", "Strawberry Cheesecake (double: Rum Raisin + Strawberry Cheesecake)", "September online talk event / Oct 16 fan signing"])
    daiki = box("DAIKI: Rum Raisin + Strawberry Cheesecake", [
        "DAIKI (Daiki Kato, born October 8, 2004, from Aichi) named Strawberry Cheesecake as his favorite at a September online talk event.<br>At the September 13 talk event, asked what job he'd want besides being an idol, he answered \"making ice cream, a Baskin-Robbins person.\"<br>He doesn't just love the flavors; he dreams of working behind the counter too, which is very DAIKI.",
        "At the October 16 fan signing, a fan asked \"If you picked a double at Baskin-Robbins?\" and he laughed, \"Two, huh!\" before studying the menu.<br>After thinking with his hand over his mouth, he chose <strong>\"Rum Raisin and...\"</strong> and then <strong>\"Strawberry Cheesecake!\"</strong><br>He picked Strawberry Cheesecake again after naming it at the September talk event, so it really is his go-to flavor.",
        "Asked to name the set, he skipped the fan's hint (\"Something like the Daiki Set!\"), thought for a moment, and called it the <strong>\"KO1 Shiyou Ice Cream Party.\"</strong><br>\"KO1 shiyou\" sounds just like the Japanese \"koi shiyou\" (\"let's fall in love\"), a pun on the \"KO1\" in KO1KEYZ that fits the group's leader.",
        "Rum Raisin is ice cream with rum-flavored raisins.<br>Paired with the sweet-tart Strawberry Cheesecake, it makes for a slightly grown-up double.",
    ], fig("daiki", "en"))
    c = replace_box(c, "DAIKI:", daiki)
    c = add_flavor_row(c, ">Rich chocolate ice cream made with two kinds of cocoa<", ["Rum Raisin", "Ice cream with rum-flavored raisins", "DAIKI", "－"], False)
    c = rep(c, "&#10003; DAIKI: Strawberry Cheesecake, and his dream side job is \"a Baskin-Robbins person\"",
               "&#10003; DAIKI: Rum Raisin + Strawberry Cheesecake, the \"KO1 Shiyou Ice Cream Party,\" and his dream side job is \"a Baskin-Robbins person\"")
    return c


for pid, fn in [(15262, jp), (15266, kr), (15267, en)]:
    cur = api(f"/wp-json/wp/v2/posts/{pid}?context=edit&_fields=status,content")
    new = fn(cur["content"]["raw"])
    open(REPO + rf"\tools\_br31_new_{pid}.html", "w", encoding="utf-8").write(new)
    if DRY:
        print("dry ok", pid, cur["status"], len(cur["content"]["raw"]), "->", len(new))
        continue
    r = api(f"/wp-json/wp/v2/posts/{pid}", {"content": new, "status": cur["status"]}, "POST")
    print("updated", pid, r["status"], r["link"])
