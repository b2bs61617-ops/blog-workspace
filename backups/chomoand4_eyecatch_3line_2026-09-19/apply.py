"""chomoand-4.blog 全記事のアイキャッチを3行デザインに差し替える(2026-09-19).

使い方(repo直下から):
    python backups/chomoand4_eyecatch_3line_2026-09-19/apply.py gen      # 画像生成のみ(images/chomoand4_3line/)
    python backups/chomoand4_eyecatch_3line_2026-09-19/apply.py upload   # メディアUP+featured_media差し替え
    python backups/chomoand4_eyecatch_3line_2026-09-19/apply.py restore  # before.json の元画像IDに戻す

記事のタイトル・スラッグ・本文・ステータスは一切変更しない(featured_mediaのみ)。
SPLITS: 記事ID -> "1行目|2行目|3行目"(2行目=一番強調したい内容。3行をつなげるとグループ名省略後のタイトルと一致すること)
"""

from __future__ import annotations

import base64
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import eyecatch_torahja as ec  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = ROOT / "images" / "chomoand4_3line"

SPLITS = {
    19: "【トークィーンズ】|3人の恋愛観|がヤバすぎる？",
    22: "『けるとめる』|WANGANフェス|の倍率は？当日の内容も！",
    46: "【マグロ一本釣り】宮近海斗の|帽子・Tシャツ・靴|のブランドは？",
    49: "【マグロ一本釣り】宮近海斗のメガネは|Ray-Ban|？価格も調査！",
    51: "運転免許を持つ|4人は誰？|車内トークも！",
    57: "釣り堀ロケ地は|武蔵野園？|食べたメニューは？",
    59: "【ドライブ】中村海人の|ニット帽|はモンクレ×リック？",
    65: "【リズム天国】松倉海斗の|ONE PIECE|Tシャツはどこの？",
    67: "初期メンバー9人？|脱退4人|の現在は？",
    72: "【FM大阪収録】松田元太の|私服シャツと靴下|のブランドは？",
    76: "【On My Road】川島如恵留の|スニーカー|はアディダス？",
    80: "【On My Road】宮近海斗の|赤いスニーカー|はどこの？",
    85: "【JUST!シン日本遺産】|仙台ロケ地はどこ？|屋台飯も紹介！",
    88: "【シン日本遺産】宮近海斗の|Apple Watch|が話題に？",
    92: "【リズム天国】宮近海斗の|黒T|はsacai×インターステラー？",
    95: "【リズム天国】川島如恵留の|ピアス|はティファニー？",
    98: "【リズム天国】七五三掛龍也の|Tシャツ|はPRADA？",
    103: "ピンクスホットドッグス|日本上陸|は聖地の店？",
    108: "【On My Road】新曲MVの|撮影場所と撮影日|は？",
    111: "【STAR】七五三掛龍也の|ワインレッドの靴|はSamba LT？",
    115: "【音楽の日】松倉海斗の|ピアス|はクロムハーツ？",
    122: "【げんたに会いに大阪】の|ロケ地は？|お店と注文品を特定！",
    129: "松田元太『俺節』|楽屋ルーティン|と私物アイテムは？",
    132: "【発売中】元太めし|元太ソーダ味|はどこで買える？",
    137: "【ノンストップ！】七五三掛龍也の|シャツ|はMM6？",
    142: "【Jリーグ開幕戦】|履いていた靴|は？",
    145: "【Instagram】七五三掛龍也の|黄色Tシャツ|はロエベ？",
    149: "【開幕戦】宮近海斗の白Tは|Levi's|×Sky High Farm？",
    154: "【WANGANフェス】松倉海斗の|指輪|はクロムハーツ？",
    158: "【STAR】松倉海斗の|牛柄スニーカー|はどこの？",
    161: "メンバーカラーは|なぜ変わった？|紫の意味も！",
    168: "松田元太への差し入れ|「山崎18年」|の価格は？買える？",
    171: "【リズム天国】宮近海斗の|メガネ|はTHOM BROWNE？",
    174: "【Jリーグ開幕記念マッチ】松倉海斗の|Tシャツ|は？",
    188: "松倉海斗がコストコで着てたTシャツは|Acne Studios|と判明！",
    189: "コストコで|買ったもの|は？店舗はどこ？",
    198: "川島如恵留がコストコで着ていたTシャツは？|MM6|と判明！",
    202: "宮近海斗がコストコでかぶってた帽子は|6CRAYON|と判明！",
    207: "宮近海斗がコストコで着てたTシャツは|Carhartt WIP|と判明！",
    214: "アルバム・コンサートは|毎年違うメンバー|がプロデュース？",
    215: "全員が振り付けした|曲は？|メンバー別に紹介",
    223: "ガンバ大阪に|サインが飾られてる|理由は?",
    243: "八ヶ岳ロケ地はどこ？|やま里・えほん村|を特定",
    250: "けるとめる-いわきFC回で|行った店・食べたもの|まとめ",
}


def load_before() -> list[dict]:
    return json.loads((HERE / "before.json").read_text(encoding="utf-8"))


def gen() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for post in load_before():
        pid, title = post["id"], post["title"]
        color_key = ec.detect_color_key(title)
        stripped = ec.strip_group_name(title)
        lines = ec.parse_split(stripped, SPLITS[pid])  # 不一致ならここで止まる
        html = ec.build_html(stripped, color_key, "stage", lines)
        path = ec.render(html, OUT / f"id{pid}.png")
        print(f"{pid:4d} {color_key:8s} {' / '.join(lines)}")
        path.with_suffix(".html").unlink(missing_ok=True)


def _wp():
    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(WP_CHOMO4_\w+)=(.*)$", line.strip())
        if m:
            env[m.group(1)] = m.group(2).strip().strip('"')
    url = env["WP_CHOMO4_URL"].rstrip("/")
    tok = base64.b64encode(f"{env['WP_CHOMO4_USERNAME']}:{env['WP_CHOMO4_APP_PASSWORD']}".encode()).decode()
    return url, {"Authorization": "Basic " + tok}


def _set_featured(url: str, headers: dict, pid: int, media_id: int) -> dict:
    req = urllib.request.Request(
        f"{url}/wp-json/wp/v2/posts/{pid}",
        data=json.dumps({"featured_media": media_id}).encode(),
        method="POST",
        headers={**headers, "Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req))


def upload() -> None:
    url, headers = _wp()
    log_path = HERE / "after.json"
    done = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else {}
    for post in load_before():
        pid = post["id"]
        if str(pid) in done:
            continue
        data = (OUT / f"id{pid}.png").read_bytes()
        req = urllib.request.Request(
            f"{url}/wp-json/wp/v2/media",
            data=data,
            method="POST",
            headers={**headers, "Content-Type": "image/png",
                     "Content-Disposition": f"attachment; filename=chomoand4_id{pid}_eyecatch_3line.png"},
        )
        media = json.load(urllib.request.urlopen(req))
        r = _set_featured(url, headers, pid, media["id"])
        assert r["title"]["raw"] == post["title"] if "raw" in r["title"] else True
        done[str(pid)] = media["id"]
        log_path.write_text(json.dumps(done, indent=1), encoding="utf-8")  # 途中で止まっても再開できる
        print(f"{pid:4d} {r['status'][:3]} media={media['id']} {post['title']}")


def restore() -> None:
    url, headers = _wp()
    for post in load_before():
        r = _set_featured(url, headers, post["id"], post["featured_media"])
        print(f"{post['id']:4d} -> media {r['featured_media']}")


if __name__ == "__main__":
    {"gen": gen, "upload": upload, "restore": restore}[sys.argv[1]]()
