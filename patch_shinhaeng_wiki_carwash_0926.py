# -*- coding: utf-8 -*-
"""オ・シンヘンwiki(JP1624公開/KR10659公開/EN11523下書き)に全南日報(2026-06-15)の父インタビュー内容を軽く追記し、
洗車場夜勤記事(JP13716/KR13717/EN13718)へ誘導する。
- 選挙の節: 順位「4位」→「6位」(ナ選挙区で最少の990票・当選4人なので4位はあり得ない。全南日報「6위」、韓国日報「가장 낮은 990표」)
  +出馬は父のすすめ・NHK密着を1段落
- ダンススクールの前にH3「選挙後は大学を休学、洗車場の夜勤で下積み」を新設
- JPの誤字(武安郡→務安郡、軍議会→郡議会)
公開済みは content のみ送信(title/slug/status なし)、下書きは status=draft 明示。

python patch_shinhaeng_wiki_carwash_0926.py [--apply] [--nolink] [ids...]
  --nolink : 誘導リンクboxを入れない(新記事の公開前用)。後で --apply だけで再実行するとリンクboxだけ追加される。
"""
import base64
import json
import re
import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
    return env


ENV = load_env(ROOT / ".env")
W = ENV["WP_KOIKEYS_URL"].rstrip("/") + "/wp-json/wp/v2"
HA = {"Authorization": "Basic " + base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()}
NOLINK = "--nolink" in sys.argv

NEW = {
    "ja": ("https://chomoand-1.com/shinhaeng-car-wash-night-shift-father-interview-13716",
           "【SHINHAENG】洗車場で夜勤バイト？父が明かした下積み4年！",
           "父が語った下積み時代のエピソードは、こちらの記事で詳しく紹介しています。"),
    "ko": ("https://chomoand-1.com/ko/shinhaeng-car-wash-night-shift-father-interview-kr-13717",
           "SHINHAENG, 세차장 야간 알바? 아버지가 밝힌 데뷔 전 4년!",
           "아버지가 전한 데뷔 전 이야기는 이 글에서 자세히 소개하고 있어요."),
    "en": ("https://chomoand-1.com/en/shinhaeng-car-wash-night-shift-father-interview-en-13718",
           "SHINHAENG’s Car Wash Night Shifts: His Dad on the Road to Debut",
           "Read more about his pre-debut years, as told by his father, here."),
}


def para(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->"


def h3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->'


def linkbox(lang):
    url, title, lead = NEW[lang]
    return ('<!-- wp:html -->\n<div class="shinhaeng-carwash-link" style="border:1px solid #e6d8cc;border-left:4px solid #8b6a4f;'
            'border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:#faf5f0;">\n'
            f'<p style="margin:0;"><strong>{lead}</strong></p>\n'
            f'<ul style="margin:6px 0 0 0;padding-left:1.2em;"><li><a href="{url}" target="_blank" rel="noopener">{title}</a></li></ul>\n'
            '</div>\n<!-- /wp:html -->')


def rep(raw, old, new):
    assert raw.count(old) == 1, f"not unique/found: {old[:70]}"
    return raw.replace(old, new)


def before(raw, key, insert):
    assert raw.count(key) == 1, f"anchor not unique/found: {key[:70]}"
    return raw.replace(key, insert + "\n\n" + key)


def after(raw, key, insert):
    assert raw.count(key) == 1, f"anchor not unique/found: {key[:70]}"
    return raw.replace(key, key + "\n\n" + insert)


# ---------------- 各言語の追記内容 ----------------
SPEC = {
    1624: dict(
        lang="ja", published=True,
        marker="選挙後は大学を休学、洗車場の夜勤で下積み",
        fixes=[
            ("<strong>選挙結果5.88％(得票数:990)を得票し、4位にとどまり落選</strong>しました。",
             "<strong>選挙結果5.88％(得票数:990)を得票し、6位で落選</strong>しました。<br>\n同じ選挙区の候補者の中では最も少ない票数で、4つの議席はすべて共に民主党の候補が獲得しています。"),
            ("<span class=\"swl-marker mark_yellow\">全羅南道武安郡</span>", "<span class=\"swl-marker mark_yellow\">全羅南道務安郡</span>"),
            ("<span class=\"swl-marker mark_yellow\">軍議会議員選挙</span>", "<span class=\"swl-marker mark_yellow\">郡議会議員選挙</span>"),
        ],
        election_anchor="<p>彼にとって18歳での挑戦は、結果ではなく挑戦した事に大きな意味があったのではないでしょうか。</p>\n<!-- /wp:paragraph -->",
        election_add=para(
            "実はこの出馬、父のオ・ウォンオクさんのすすめによるものでした。",
            "父は地元紙・全南日報の取材で「歴史の中にお前も一緒にいなさいという意味で出馬を勧めた」と話していて、本人は最初「なぜ出なければならないのか」と毎日のように反発していたそうです。",
            "選挙期間中は日本のNHKも3日間にわたって密着取材しており、日本との縁はこの頃から始まっていたのかもしれません。",
        ),
        section_before='<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">ダンススクール</h3>',
        section=lambda: [
            h3("選挙後は大学を休学、洗車場の夜勤で下積み"),
            para(
                "選挙が終わると、オ・シンヘンさんは在籍していた木浦大学のファッション衣類学科を休学し、アイドルを目指す準備に専念しました。",
                "木浦ではオルタナティブスクールに通いながら約2年、その後ソウルでさらに約2年と、日プ新世界に出るまでの準備期間は約4年に及びます。",
                "ソウル時代は夜10時から翌朝8時まで洗車場で働きながらレッスンを続けていて、家族からは「あと2年だけやってみよう」と期限を出されていたそうです。",
                "その期限ぎりぎりでつかんだのが、日プ新世界への挑戦でした。",
            ),
        ],
        link_after="その期限ぎりぎりでつかんだのが、日プ新世界への挑戦でした。</p>\n<!-- /wp:paragraph -->",
    ),
    10659: dict(
        lang="ko", published=True, plain=True,
        marker="선거 후 대학 휴학, 세차장 야간 근무로 준비",
        fixes=[
            ("<strong>선거 결과 5.88%(득표수: 990표)를 얻어 4위에 그쳐 낙선</strong>했습니다.",
             "<strong>선거 결과 5.88%(득표수: 990표)를 얻어 6위로 낙선</strong>했습니다.<br>\n같은 선거구 후보 가운데 가장 적은 득표였고, 4석은 모두 더불어민주당 후보가 차지했습니다."),
        ],
        election_anchor=None,
        election_add=para(
            "사실 이 출마는 아버지 오원옥 씨의 권유였어요.",
            "아버지는 전남일보 인터뷰에서 “역사 안에 너도 함께 있으라는 뜻에서 출마를 권유했다”고 밝혔고, 본인은 처음에 “왜 나가야 하느냐”며 매일 따졌다고 해요.",
            "선거 기간에는 일본 NHK도 3일간 밀착 취재했다고 하니, 일본과의 인연은 이때부터 시작됐는지도 모르겠어요.",
        ),
        section_before='<h3 class="wp-block-heading">댄스스쿨</h3>',
        section=lambda: [
            h3("선거 후 대학 휴학, 세차장 야간 근무로 준비"),
            para(
                "선거가 끝난 뒤 오신행 씨는 목포대 패션의류학과를 휴학하고 아이돌 준비에 전념했어요.",
                "목포에서 대안학교를 다니며 약 2년, 이후 서울에서 약 2년 등 일프 신세계에 나서기까지 준비 기간은 약 4년이었습니다.",
                "서울에서는 밤 10시부터 아침 8시까지 세차장에서 일하며 레슨을 이어 갔고, 가족은 “2년 정도만 더 해보자”는 기한을 줬다고 해요.",
                "그 기한의 끝자락에서 잡은 기회가 바로 일프 신세계였습니다.",
            ),
        ],
        link_after="그 기한의 끝자락에서 잡은 기회가 바로 일프 신세계였습니다.</p>\n<!-- /wp:paragraph -->",
    ),
    11523: dict(
        lang="en", published=False,
        marker="A Leave From University and Night Shifts at a Car Wash",
        fixes=[("finishing 4th and losing the race", "finishing 6th and losing the race")],
        election_anchor=None,
        election_add=para(
            "In fact, running for office was his father Oh Won-ok's idea.",
            "His father told the regional paper Jeonnam Ilbo, \"I encouraged him to run so that he, too, would be part of that history,\" and said that at first his son argued with him every day about why he had to run.",
            "Japan's NHK even followed him for three days during the campaign, so perhaps his connection to Japan began back then.",
        ),
        section_before=None,
        section=lambda: [
            h3("A Leave From University and Night Shifts at a Car Wash"),
            para(
                "After the election, he took a leave of absence from the Department of Fashion and Clothing at Mokpo National University to focus on becoming an idol.",
                "He trained for about two years in Mokpo while attending an alternative school, then for about two more in Seoul: roughly four years in total before THE NEW WORLD.",
                "In Seoul, he worked overnight at a car wash from 10 p.m. to 8 a.m. while taking lessons, and his family gave him about two more years as a deadline.",
                "The chance he seized right at the end of that deadline was PRODUCE 101 JAPAN: THE NEW WORLD.",
            ),
        ],
        link_after="The chance he seized right at the end of that deadline was PRODUCE 101 JAPAN: THE NEW WORLD.</p>\n<!-- /wp:paragraph -->",
    ),
}


def find_block_end_after(raw, needle):
    """needleを含む段落ブロックの終わり(<!-- /wp:paragraph -->)を返す"""
    i = raw.index(needle)
    end = "<!-- /wp:paragraph -->" if "<!-- /wp:paragraph -->" in raw[i:i + 3000] else "</p>"
    j = raw.index(end, i) + len(end)
    return raw[:j], raw[j:]


def strip_blocks(html):
    """ブロックコメントなしの素のHTML記事(KR10659)用"""
    html = re.sub(r"<!-- /?wp:[^>]*-->\n?", "", html)
    return html.replace("<p>", '<p class="wp-block-paragraph">')


def patch(pid, raw):
    s = SPEC[pid]
    conv = strip_blocks if s.get("plain") else (lambda x: x)
    if s["marker"] in raw:
        # 本文は追記済み → リンクboxだけ足す
        assert "shinhaeng-carwash-link" not in raw, f"{pid} already fully patched"
        assert not NOLINK, "already patched without link; run without --nolink"
        la = s["link_after"].replace("\n<!-- /wp:paragraph -->", "") if s.get("plain") else s["link_after"]
        return after(raw, la, conv(linkbox(s["lang"])))
    for old, new in s["fixes"]:
        raw = rep(raw, old, new)
    # 選挙の節: 結果段落の後ろ(JPは結びの一文の後ろ)に1段落
    if s["election_anchor"]:
        raw = after(raw, s["election_anchor"], s["election_add"])
    else:
        head, tail = find_block_end_after(raw, s["fixes"][0][1][:25])
        raw = head + "\n\n" + conv(s["election_add"]) + tail
    # 新しいH3をダンススクールの前に
    sec = s["section"]()
    if not NOLINK:
        sec.append(linkbox(s["lang"]))
    block = conv("\n\n".join(sec))
    if s["section_before"]:
        raw = before(raw, s["section_before"], block)
    else:
        key = next(k for k in ('<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">Dance School</h3>',
                               '<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">Dance school</h3>') if k in raw)
        raw = before(raw, key, block)
    return raw


S = Path(r"C:\Users\s30se\AppData\Local\Temp\claude\c--Users-s30se-OneDrive--------CHOMO\5c5044f2-52fd-4f48-9577-cf453ce3ec7f\scratchpad")

if __name__ == "__main__":
    apply = "--apply" in sys.argv
    ids = [int(x) for x in sys.argv[1:] if x.isdigit()] or list(SPEC)
    for pid in ids:
        spec = SPEC[pid]
        d = requests.get(f"{W}/posts/{pid}", params={"context": "edit"}, headers=HA).json()
        assert d["status"] == ("publish" if spec["published"] else "draft"), (pid, d["status"])
        raw = d["content"]["raw"]
        new = patch(pid, raw)
        (S / f"wiki_patched_{pid}.html").write_text(new, encoding="utf-8")
        print(pid, d["status"], len(raw), "->", len(new))
        if not apply:
            continue
        payload = {"content": new} if spec["published"] else {"content": new, "status": "draft"}
        r = requests.post(f"{W}/posts/{pid}", headers={**HA, "Content-Type": "application/json"},
                          data=json.dumps(payload).encode("utf-8"))
        r.raise_for_status()
        v = requests.get(f"{W}/posts/{pid}", params={"context": "edit"}, headers=HA).json()
        ok = spec["marker"] in v["content"]["raw"] and (NOLINK or "shinhaeng-carwash-link" in v["content"]["raw"])
        print("  UPDATED", pid, v["status"], "verified" if ok else "NOT REFLECTED")
