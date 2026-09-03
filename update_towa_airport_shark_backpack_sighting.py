# -*- coding: utf-8 -*-
"""Add the concrete Incheon Airport (2026-07-31) sighting context to the
TOWA shark backpack drafts (JP 12193 / KR 12197 / EN 12198)."""
import json, base64, os
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
WP_URL = ENV["WP_KOIKEYS_URL"].rstrip("/")
AUTH = base64.b64encode(f"{ENV['WP_KOIKEYS_USERNAME']}:{ENV['WP_KOIKEYS_APP_PASSWORD']}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}"}
HJSON = {**H, "Content-Type": "application/json"}

EDITS = {
    12193: {  # JP
        "title": "TOWAが仁川空港で背負ってたサメリュックのブランドは？",
        "replacements": [
            ("KO1KEYZ(コイキーズ)のTOWA(濱田永遠)さんが、空港で移動する姿を見かけたというXの投稿があり、そのとき背負っていた大きめのリュックが話題になりました。",
             "KO1KEYZ(コイキーズ)のTOWA(濱田永遠)さんが、2026年7月末に仁川(インチョン)空港で目撃された際に背負っていた大きめのリュックが話題になりました。"),
            ("<h2 class=\"wp-block-heading\">TOWAが空港で背負っていたのはどんなリュック？</h2>",
             "<h2 class=\"wp-block-heading\">TOWAが仁川空港で背負っていたのはどんなリュック？</h2>"),
            ("<p>きっかけは、空港でTOWAさんを見かけたというXの投稿でした。<br>\n移動中のオフショットで、黒くて大きなリュックを背負っている姿が写っており、そのインパクトのある見た目からどこのバッグなのか気になるファンが多かったようです。<br>\n本人や運営からの公式なアイテム紹介ではありませんが、移動中に背負っていたことから、衣装ではなく私物とみられます。</p>",
             "<p>きっかけは、2026年7月31日に仁川(インチョン)空港でKO1KEYZの姿をとらえたファンの動画がXに投稿されたことでした。<br>\n黒いタンクトップにキャップというラフな装いのTOWAさんが、黒くて大きなリュックを背負って歩く様子が写っており、そのインパクトのある見た目からどこのバッグなのか気になるファンが多かったようです。<br>\n本人や運営からの公式なアイテム紹介ではありませんが、移動中に背負っていたことから、衣装ではなく私物とみられます。</p>"),
            ("&#10003; TOWAが空港で背負っていたのはMORN CREATIONSの「シャークバックパック」<br>",
             "&#10003; TOWAが2026年7月末に仁川空港で背負っていたのはMORN CREATIONSの「シャークバックパック」<br>"),
        ],
        "summary": "KO1KEYZ・TOWAが2026年7月末に仁川空港で背負っていた大きめのリュックは、香港のバッグブランドMORN CREATIONSの「シャークバックパック」Lサイズ(ブラック)とみられます。サメの口をかたどった定番モデルで、参考価格は14,300円(税込)です。",
    },
    12197: {  # KR
        "title": "TOWA가 인천공항에서 멨던 상어 백팩 브랜드는?",
        "replacements": [
            ("KO1KEYZ의 TOWA(하마다 토와)가 공항에서 이동하는 모습을 봤다는 X 게시물이 올라오면서, 그때 메고 있던 큼직한 백팩이 화제가 되었습니다.",
             "KO1KEYZ의 TOWA(하마다 토와)가 2026년 7월 말 인천공항에서 목격됐을 때 메고 있던 큼직한 백팩이 화제가 되었습니다."),
            ("<h2 class=\"wp-block-heading\">TOWA가 공항에서 멘 것은 어떤 백팩?</h2>",
             "<h2 class=\"wp-block-heading\">TOWA가 인천공항에서 멘 것은 어떤 백팩?</h2>"),
            ("<p>계기는 공항에서 TOWA를 봤다는 X 게시물이었습니다.<br>\n이동 중의 오프숏으로, 검고 커다란 백팩을 메고 있는 모습이 찍혀 있어, 그 임팩트 있는 겉모습 때문에 어디 가방인지 궁금해하는 팬이 많았던 것 같습니다.<br>\n본인이나 운영 측의 공식 아이템 소개는 아니지만, 이동 중에 메고 있었던 점에서 무대 의상이 아닌 사물로 보입니다.</p>",
             "<p>계기는 2026년 7월 31일 인천공항에서 KO1KEYZ의 모습을 담은 팬 영상이 X에 올라온 것이었습니다.<br>\n검은 탱크톱에 캡을 쓴 편안한 차림의 TOWA가 검고 커다란 백팩을 메고 걷는 모습이 찍혀 있어, 그 임팩트 있는 겉모습 때문에 어디 가방인지 궁금해하는 팬이 많았던 것 같습니다.<br>\n본인이나 운영 측의 공식 아이템 소개는 아니지만, 이동 중에 메고 있었던 점에서 무대 의상이 아닌 사물로 보입니다.</p>"),
            ("&#10003; TOWA가 공항에서 메고 있던 것은 MORN CREATIONS의 '샤크 백팩'<br>",
             "&#10003; TOWA가 2026년 7월 말 인천공항에서 메고 있던 것은 MORN CREATIONS의 '샤크 백팩'<br>"),
        ],
        "summary": "KO1KEYZ TOWA가 2026년 7월 말 인천공항에서 메고 있던 큼직한 백팩은 홍콩 가방 브랜드 MORN CREATIONS의 '샤크 백팩' L 사이즈(블랙)로 보입니다. 상어 입을 본뜬 스테디셀러 모델로 참고가는 14,300엔(세금 포함)입니다.",
    },
    12198: {  # EN
        "title": "What Brand Is TOWA's Shark Backpack from Incheon Airport?",
        "replacements": [
            ("<p>A post on X said KO1KEYZ's TOWA (Towa Hamada) was spotted moving through an airport, and the oversized backpack he had on drew a lot of attention.",
             "<p>The oversized backpack KO1KEYZ's TOWA (Towa Hamada) had on when he was spotted at Incheon Airport in late July 2026 drew a lot of attention."),
            ("<p>It started with a post on X from someone who saw TOWA at an airport.<br>\nThe candid travel shot showed him carrying a big black backpack, and its bold look had a lot of fans wondering which brand it was.<br>\nThere's no official item note from TOWA or the agency, but since he was carrying it while traveling, it looks like a personal item rather than a stage piece.</p>",
             "<p>It started with a fan video posted to X on July 31, 2026, showing KO1KEYZ walking through Incheon Airport.<br>\nTOWA, dressed down in a black tank top and a cap, was filmed walking with a big black backpack, and its bold look had a lot of fans wondering which brand it was.<br>\nThere's no official item note from TOWA or the agency, but since he was carrying it while traveling, it looks like a personal item rather than a stage piece.</p>"),
            ("&#10003; The bag TOWA carried at the airport is MORN CREATIONS' \"Shark Backpack\"<br>",
             "&#10003; The bag TOWA carried at Incheon Airport in late July 2026 is MORN CREATIONS' \"Shark Backpack\"<br>"),
        ],
        "summary": "KO1KEYZ's TOWA was spotted carrying an oversized backpack at Incheon Airport in late July 2026. It's the Shark Backpack (L size, black) from the Hong Kong brand MORN CREATIONS, a shark-mouth staple that lists at 14,300 yen (tax incl.).",
    },
}

for pid, spec in EDITS.items():
    cur = requests.get(f"{WP_URL}/wp-json/wp/v2/posts/{pid}?context=edit", headers=H)
    cur.raise_for_status()
    content = cur.json()["content"]["raw"]
    for old, new in spec["replacements"]:
        if old not in content:
            raise SystemExit(f"[{pid}] pattern not found:\n{old[:120]}")
        content = content.replace(old, new, 1)
    payload = {
        "status": "draft",
        "title": spec["title"],
        "content": content,
        "meta": {"jetpack_publicize_message": spec["summary"]},
    }
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", headers=HJSON,
                      data=json.dumps(payload).encode("utf-8"))
    r.raise_for_status()
    print(f"updated {pid}: {r.json()['title']['raw']}")

print("DONE")
