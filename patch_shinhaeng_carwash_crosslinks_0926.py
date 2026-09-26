# -*- coding: utf-8 -*-
"""SHINHAENG洗車場夜勤記事(JP13716/KR13717/EN13718)への誘導を既存記事に軽く追記する。
- 1669 オ・シンヘンの家族構成(JP公開)          : 父が語った4年間の短いセクション+誘導
- 13030 KO1KEYZバイト歴まとめ(JP公開)          : SHINHAENGの節を追加、「残る8人」→7人、追記注記(タイトルは据え置き)
- 13497/13498 同KR/EN(下書き)                  : 同じ内容をKR/ENで
公開済み記事は title/slug/status を送らず content だけ送る。下書きは status=draft を明示。
既存の build_and_post_ko1keyz_baito_history.py は title+status=draft を送るため再実行しないこと(公開記事が下書きに戻る)。

python patch_shinhaeng_carwash_crosslinks_0926.py [--apply] [ids...]
"""
import base64
import json
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
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
HA = {"Authorization": f"Basic {AUTH}"}

NEW_JP = "https://chomoand-1.com/shinhaeng-car-wash-night-shift-father-interview-13716"
NEW_KR = "https://chomoand-1.com/ko/shinhaeng-car-wash-night-shift-father-interview-kr-13717"
NEW_EN = "https://chomoand-1.com/en/shinhaeng-car-wash-night-shift-father-interview-en-13718"

G_BORDER, G_ACCENT, G_BG = "#ded9d2", "#8a8378", "#f8f6f4"


def para(*lines):
    return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->"


def h2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def a(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'


def gbox(*rows, border=G_BORDER, accent=G_ACCENT, bg=G_BG):
    ps = "\n".join(r if r.startswith("<ul") else f'<p style="margin:{0 if i == 0 else "4px 0 0 0"};">{r}</p>'
                   for i, r in enumerate(rows))
    return (f'<!-- wp:html -->\n<div style="border:1px solid {border};border-left:4px solid {accent};border-radius:4px;'
            f'padding:10px 16px;margin:0 0 16px 0;background:{bg};">\n{ps}\n</div>\n<!-- /wp:html -->')


def check(text):
    return (f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {G_ACCENT};border-radius:3px;'
            f'color:{G_ACCENT};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>{text}')


H2_OPEN = '<!-- wp:heading -->\n<h2 class="wp-block-heading">'


def before_h2(raw, heading, insert):
    key = f"{H2_OPEN}{heading}</h2>"
    assert raw.count(key) == 1, f"heading not unique/found: {heading}"
    return raw.replace(key, insert + "\n\n" + key)


def rep(raw, old, new):
    assert raw.count(old) == 1, f"not unique/found: {old[:60]}"
    return raw.replace(old, new)


def after_first_para(raw, insert):
    end = "<!-- /wp:paragraph -->"
    i = raw.index(end) + len(end)
    return raw[:i] + "\n\n" + insert + raw[i:]


# ---------------- 1669 家族構成(JP・公開) ----------------
def patch_1669(raw):
    sec = "\n\n".join([
        h2("父が語ったデビューまでの4年間(2026年9月追記)"),
        para(
            "父のオ・ウォンオクさんは、KO1KEYZのデビューが決まった直後の2026年6月、地元紙・全南日報の電話インタビューに応じています。",
            "選挙のあとに木浦大学を休学したこと、ソウルでは夜10時から翌朝8時まで洗車場で働きながら歌とダンスを準備していたこと、そして「月給をもらったらお母さんとお父さんに10%ずつあげる」と話していたことなどが語られました。",
            "3人きょうだい全員が木浦大学に進んだという話も出ていて、家族そろって地元とのつながりを大切にしてきたことが伝わってきます。",
        ),
        gbox("<strong>父が語ったエピソードは、こちらの記事で詳しく紹介しています。</strong>",
             f'<ul style="margin:6px 0 0 0;padding-left:1.2em;"><li>{a(NEW_JP, "【SHINHAENG】洗車場で夜勤バイト？父が明かした下積み4年！")}</li></ul>'),
    ])
    return before_h2(raw, "政治家からアイドルへ！KO1KEYZデビューを果たす", sec)


# ---------------- 13030 バイト歴(JP・公開) ----------------
def patch_13030(raw):
    raw = after_first_para(raw, gbox(
        "<strong>2026年9月26日追記</strong>",
        "SHINHAENGのバイト歴が分かったので追記しました。タイトルは「4人」のままですが、本文ではSHINHAENGを加えた5人を紹介しています。"))
    raw = rep(raw, "<li>残るメンバーの状況</li>", "<li>SHINHAENGの洗車場バイト</li>\n<li>残るメンバーの状況</li>")
    sec = "\n\n".join([
        h2("SHINHAENG(オ・シンヘン)は洗車場の夜勤"),
        gbox("<strong>バイト先:</strong>ソウルの洗車場(夜勤)", "<strong>時間帯:</strong>夜10時〜翌朝8時"),
        para(
            "SHINHAENGは、デビュー前のソウル時代に洗車場で夜勤をしていました。",
            "父のオ・ウォンオクさんが地元紙・全南日報の取材で「夜10時から翌朝8時まで洗車場で働きながら準備した」と話していて、昼間は歌とダンスのレッスン、夜は洗車場という生活だったようです。",
            "接客系のバイトが多いメンバーの中で、夜通しの洗車は少し珍しいパターンと言えるでしょう。",
        ),
        gbox("<strong>SHINHAENGの下積み時代は、こちらの記事で詳しく紹介しています。</strong>",
             f'<ul style="margin:6px 0 0 0;padding-left:1.2em;"><li>{a(NEW_JP, "【SHINHAENG】洗車場で夜勤バイト？父が明かした下積み4年！")}</li></ul>'),
    ])
    raw = before_h2(raw, "残る8人のバイト歴は非公表", sec)
    raw = rep(raw, f"{H2_OPEN}残る8人のバイト歴は非公表</h2>", f"{H2_OPEN}残る7人のバイト歴は非公表</h2>")
    raw = rep(raw, "ISSA・RYOGA・YOSHIKI・TOWA以外の8人", "ISSA・RYOGA・YOSHIKI・TOWA・SHINHAENG以外の7人")
    raw = rep(raw, "KEITO・DAIKI・KOSUKE・RYUJI・SHINHAENG・SIYOUNG・YUKI・YURAの8人は",
              "KEITO・DAIKI・KOSUKE・RYUJI・SIYOUNG・YUKI・YURAの7人は")
    raw = rep(raw, "残る8人のバイト歴は現時点で非公表",
              "SHINHAENGはデビュー前、ソウルの洗車場で夜10時〜翌朝8時の夜勤<br>\n" + check("残る7人のバイト歴は現時点で非公表"))
    return raw


# ---------------- 13497 バイト歴(KR・下書き) ----------------
def patch_13497(raw):
    raw = after_first_para(raw, gbox(
        "<strong>2026년 9월 26일 추가</strong>",
        "SHINHAENG의 아르바이트 경력이 밝혀져 내용을 추가했어요. 제목은 '4명' 그대로지만, 본문에서는 SHINHAENG까지 5명을 소개합니다."))
    raw = rep(raw, "<li>나머지 멤버들의 상황</li>", "<li>SHINHAENG의 세차장 아르바이트</li>\n<li>나머지 멤버들의 상황</li>")
    sec = "\n\n".join([
        h2("SHINHAENG(오신행)은 세차장 야간 근무"),
        gbox("<strong>아르바이트: </strong>서울의 세차장(야간)", "<strong>시간: </strong>밤 10시~다음 날 아침 8시"),
        para(
            "SHINHAENG은 데뷔 전 서울에서 세차장 야간 아르바이트를 했어요.",
            "아버지 오원옥 씨가 전남일보 인터뷰에서 “밤 10시부터 다음 날 아침 8시까지 세차장에서 일하며 준비했다”고 밝혔고, 낮에는 노래와 춤 레슨, 밤에는 세차장이라는 생활이었던 것 같아요.",
            "접객 아르바이트가 많은 멤버들 가운데 밤샘 세차는 조금 특별한 경우라고 할 수 있어요.",
        ),
        gbox("<strong>SHINHAENG의 데뷔 전 이야기는 이 글에서 자세히 소개하고 있어요.</strong>",
             f'<ul style="margin:6px 0 0 0;padding-left:1.2em;"><li>{a(NEW_KR, "SHINHAENG, 세차장 야간 알바? 아버지가 밝힌 데뷔 전 4년!")}</li></ul>'),
    ])
    raw = before_h2(raw, "나머지 8명의 아르바이트 경력은 비공개", sec)
    raw = rep(raw, f"{H2_OPEN}나머지 8명의 아르바이트 경력은 비공개</h2>", f"{H2_OPEN}나머지 7명의 아르바이트 경력은 비공개</h2>")
    raw = rep(raw, "ISSA·RYOGA·YOSHIKI·TOWA를 제외한 8명", "ISSA·RYOGA·YOSHIKI·TOWA·SHINHAENG을 제외한 7명")
    raw = rep(raw, "KEITO·DAIKI·KOSUKE·RYUJI·SHINHAENG·SIYOUNG·YUKI·YURA 8명은", "KEITO·DAIKI·KOSUKE·RYUJI·SIYOUNG·YUKI·YURA 7명은")
    i = raw.index("나머지 8명의 아르바이트 경력은 현")
    j = raw.index("<", i)
    old_tail = raw[i:j]
    raw = raw[:i] + "SHINHAENG은 데뷔 전 서울의 세차장에서 밤 10시~아침 8시 야간 근무<br>\n" + check(old_tail.replace("8명", "7명")) + raw[j:]
    return raw


# ---------------- 13498 バイト歴(EN・下書き) ----------------
def patch_13498(raw):
    raw = after_first_para(raw, gbox(
        "<strong>Update (September 26, 2026)</strong>",
        "We've added SHINHAENG's part-time job. The title still says four members, but this article now covers five, including SHINHAENG."))
    raw = rep(raw, "<li>The status of the remaining members</li>",
              "<li>SHINHAENG's car wash job</li>\n<li>The status of the remaining members</li>")
    sec = "\n\n".join([
        h2("SHINHAENG (Oh Shin-haeng) Worked Night Shifts at a Car Wash"),
        gbox("<strong>Job: </strong>A car wash in Seoul (night shift)", "<strong>Hours: </strong>10 p.m. to 8 a.m."),
        para(
            "Before debuting, SHINHAENG worked overnight at a car wash in Seoul.",
            "His father, Oh Won-ok, told the Korean regional paper Jeonnam Ilbo, \"He prepared while working at a car wash from 10 p.m. to 8 a.m. the next morning,\" so it seems his days went to singing and dance lessons and his nights to the car wash.",
            "Among members who mostly worked customer-service jobs, an all-night car wash shift stands out.",
        ),
        gbox("<strong>Read more about SHINHAENG's pre-debut years here.</strong>",
             f'<ul style="margin:6px 0 0 0;padding-left:1.2em;"><li>{a(NEW_EN, "SHINHAENG’s Car Wash Night Shifts: His Dad on the Road to Debut")}</li></ul>'),
    ])
    raw = before_h2(raw, "The Remaining 8 Members&#039; Job Histories Are Still Unknown"
                    if "Remaining 8 Members&#039;" in raw else "The Remaining 8 Members' Job Histories Are Still Unknown", sec)
    raw = raw.replace("The Remaining 8 Members' Job Histories Are Still Unknown</h2>",
                      "The Remaining 7 Members' Job Histories Are Still Unknown</h2>")
    raw = rep(raw, "the remaining 8 members besides ISSA, RYOGA, YOSHIKI, and TOWA",
              "the remaining 7 members besides ISSA, RYOGA, YOSHIKI, TOWA, and SHINHAENG")
    raw = rep(raw, "KEITO, DAIKI, KOSUKE, RYUJI, SHINHAENG, SIYOUNG, YUKI, and YURA are",
              "KEITO, DAIKI, KOSUKE, RYUJI, SIYOUNG, YUKI, and YURA are")
    i = raw.index("The remaining 8 members' job histories are still")
    j = raw.index("<", i)
    old_tail = raw[i:j]
    raw = raw[:i] + "SHINHAENG worked night shifts (10 p.m. to 8 a.m.) at a Seoul car wash before debut<br>\n" + \
        check(old_tail.replace("8 members", "7 members")) + raw[j:]
    return raw


TARGETS = {1669: (patch_1669, True), 13030: (patch_13030, True), 13497: (patch_13497, False), 13498: (patch_13498, False)}
S = Path(r"C:\Users\s30se\AppData\Local\Temp\claude\c--Users-s30se-OneDrive--------CHOMO\5c5044f2-52fd-4f48-9577-cf453ce3ec7f\scratchpad")

if __name__ == "__main__":
    apply = "--apply" in sys.argv
    ids = [int(x) for x in sys.argv[1:] if x.isdigit()] or list(TARGETS)
    for pid in ids:
        fn, published = TARGETS[pid]
        d = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", params={"context": "edit"}, headers=HA).json()
        raw = d["content"]["raw"]
        assert "13716" not in raw and "13717" not in raw and "13718" not in raw, f"{pid} already patched"
        assert d["status"] == ("publish" if published else "draft"), (pid, d["status"])
        new = fn(raw)
        (S / f"patched_{pid}.html").write_text(new, encoding="utf-8")
        print(pid, d["status"], len(raw), "->", len(new))
        if not apply:
            continue
        payload = {"content": new} if published else {"content": new, "status": "draft"}
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers={**HA, "Content-Type": "application/json"},
                          data=json.dumps(payload).encode("utf-8"))
        r.raise_for_status()
        v = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", params={"context": "edit"}, headers=HA).json()
        ok = ("13716" in v["content"]["raw"] or "13717" in v["content"]["raw"] or "13718" in v["content"]["raw"])
        print("  UPDATED", pid, v["status"], "verified" if ok else "NOT REFLECTED")
