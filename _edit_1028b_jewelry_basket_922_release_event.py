# -*- coding: utf-8 -*-
# 発売記念イベント(2027/1/20大阪・1/27神奈川)の応募券の節を、c4公開記事922(Jewelry Basket特典)に追加
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import requests
from build_and_post_travis_japan_tour2027_jewelry_basket import (
    WP_URL, HJSON, p, h2, minibox, mark, EVENT_URL, EVENT_ROWS)

DRY = "--dry" in sys.argv


def replace_once(html, old, new):
    n = html.count(old)
    assert n == 1, (n, old[:80])
    return html.replace(old, new)


def get(pid):
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=HJSON)
    r.raise_for_status()
    return r.json()["content"]["raw"]


def put(pid, html, must):
    if DRY:
        print(pid, "dry ok", len(html))
        return
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=HJSON, json={"content": html})
    r.raise_for_status()
    raw = get(pid)
    assert all(m in raw for m in must), "not reflected"
    print(pid, r.json()["status"], "updated")

html = get(922)
html = replace_once(html, "<li>予約前の注意点</li>",
                    "<li>1月の発売記念イベントの応募券</li>\n<li>予約前の注意点</li>")
section = "\n\n".join([
    h2("全形態に発売記念イベントの応募券が入る？"),
    minibox(EVENT_ROWS + [
        ("応募期間", "2026年11月17日(火)〜11月29日(日)23:59"),
        ("当選発表", "2026年12月23日(水)12:00予定"),
    ]),
    p([
        "2026年10月28日のデビュー4周年記念の生配信で、「Travis Japan 'Jewelry Basket' 発売記念イベント」の開催が発表されました。",
        f"1月20日(水)に大阪府内、1月27日(水)に神奈川県内で、それぞれ昼の部・夜の部の2回ずつ行われ、{mark('スペシャルライブ・トーク・お見送り会')}が予定されています。",
    ]),
    p([
        f"このイベントの応募券は、{mark('初回盤T・初回盤J・通常盤・FC限定盤の全7形態に1枚ずつ')}入っています。",
        "応募券のQRコードから応募サイトに進み、もらえるシリアルナンバーで申し込む流れです。",
        "応募券を何枚使うかに制限はないので、3形態セットで買えば3口、FC限定盤も合わせれば4口応募できます。",
        "Jewelry Charmの対象にならないFC限定盤にも、応募券はしっかり入っているのがうれしいところです。",
    ]),
    p([
        "当日は当選した本人しか入場できず、顔写真付きの公的身分証の原本が必要です。",
        "応募券やシリアルナンバーは再発行できないので、アルバムが届いたらなくさないように保管しておきましょう。",
        f'詳しい応募条件は<a href="{EVENT_URL}">ユニバーサルミュージックの公式ニュース</a>で確認できます。',
    ]),
])
anchor = '<!-- wp:heading -->\n<h2 class="wp-block-heading">予約前に確認したい注意点は？</h2>'
html = replace_once(html, anchor, section + "\n\n" + anchor)
put(922, html, ["全形態に発売記念イベントの応募券が入る？", "1月の発売記念イベントの応募券"])
