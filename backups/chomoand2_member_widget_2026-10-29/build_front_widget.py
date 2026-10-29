# -*- coding: utf-8 -*-
"""chomoand-2.com(Snow Man)のトップページ上部(front_top)に「メンバーから探す」ウィジェットを置く。
トラジャ(backups/torahja_redesign_2026-09-17/build_front_widget.py)と同じ作りで、実写は使わず
メンバーカラーの丸+名前+色名のカード。色はtools/eyecatch_snowman.pyのSNOWMAN_WATERCOLORSに揃える。

  python build_front_widget.py          # 作成(作ったIDをwidget_id.txtに保存)
  python build_front_widget.py update   # 作成済みのウィジェットの中身を差し替え
  python build_front_widget.py restore  # 削除して元の空の状態に戻す
"""
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ENV = HERE.parents[1] / ".env"
env = {}
for line in ENV.read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"')
WP_URL = env["WP_CHOMO2_URL"].rstrip("/")
AUTH = (env["WP_CHOMO2_USERNAME"], env["WP_CHOMO2_APP_PASSWORD"])

# (名前, カテゴリslug, 色名, 丸の色, 枠の色)  並びは公式の紹介順
MEMBERS = [
    ("岩本照", "iwamoto-hikaru", "黄", "#f2cf4a", "#e0b92a"),
    ("深澤辰哉", "fukazawa-tatsuya", "紫", "#a98bd6", "#8c6cc4"),
    ("ラウール", "raul", "白", "#ffffff", "#b9bdc2"),
    ("渡辺翔太", "watanabe-shota", "青", "#6fa8e0", "#4f8bc9"),
    ("向井康二", "mukai-koji", "オレンジ", "#f2a14f", "#dd8530"),
    ("阿部亮平", "abe-ryohei", "緑", "#5fbf7a", "#43a45f"),
    ("目黒蓮", "meguro-ren", "黒", "#3a3b3f", "#7d8087"),
    ("宮舘涼太", "miyadate-ryota", "赤", "#e0646f", "#c84854"),
    ("佐久間大介", "sakuma-daisuke", "ピンク", "#ec92c2", "#d873ab"),
]
# 色名の文字色(白・黒は丸の色だと読めないのでグレーにする)
LABEL = {"白": "#8f949a", "黒": "#3a3b3f", "黄": "#c9a21c"}


def card_html(name, slug, cname, fill, border):
    href = f"{WP_URL}/category/snowman/{slug}"
    label = LABEL.get(cname, border)
    return f"""
<a href="{href}" style="display:flex;flex-direction:column;align-items:center;text-decoration:none;width:19%;max-width:80px;min-width:0;">
  <span style="display:block;width:clamp(38px,12vw,56px);height:clamp(38px,12vw,56px);box-sizing:border-box;border-radius:50%;background:{fill};border:3px solid {border};box-shadow:0 2px 6px rgba(0,0,0,0.12);"></span>
  <span style="margin-top:6px;font-size:clamp(10px,3vw,12px);font-weight:bold;color:#333;line-height:1.3;text-align:center;white-space:nowrap;">{name}</span>
  <span style="font-size:10px;color:{label};">{cname}</span>
</a>"""


# 1段目4人・2段目5人(9人だと1人だけ下に残るので段を固定する、2026-10-29トモキ指示)
ROWS = [MEMBERS[:4], MEMBERS[4:]]
ROW_STYLE = "display:flex;flex-wrap:nowrap;justify-content:center;gap:clamp(4px,2vw,14px);"


def build_html():
    cards = "\n".join(
        f'<div style="{ROW_STYLE}{"margin-top:14px;" if i else ""}">'
        + "\n".join(card_html(*m) for m in row) + "</div>"
        for i, row in enumerate(ROWS))
    # 上の細いラインはメンバー9色のグラデーション
    stripe = ",".join(m[3] if m[3] != "#ffffff" else "#d6d9dc" for m in MEMBERS)
    return f"""
<div style="background:#f8f9fc;border:1px solid #e3e6ee;border-radius:12px;padding:20px 16px;margin:0 0 24px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:5px;background:linear-gradient(90deg,{stripe});"></div>
  <h2 style="margin:4px 0 14px;font-size:1.15em;color:#333;text-align:center;">メンバーから探す</h2>
  {cards}
</div>
"""


def create():
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/widgets", auth=AUTH, json={
        "id_base": "block",
        "sidebar": "front_top",
        "instance": {"raw": {"content": f"<!-- wp:html -->{build_html()}<!-- /wp:html -->"}},
    })
    r.raise_for_status()
    wid = r.json()["id"]
    # このサイトは作成直後に「使用停止中」へ入ってしまうので、front_topへ移し直す(2026-10-29)
    if r.json().get("sidebar") != "front_top":
        requests.post(f"{WP_URL}/wp-json/wp/v2/widgets/{wid}", auth=AUTH,
                      json={"sidebar": "front_top"}).raise_for_status()
    (HERE / "widget_id.txt").write_text(wid, encoding="utf-8")
    print(wid, "created on front_top")


def update():
    wid = (HERE / "widget_id.txt").read_text(encoding="utf-8").strip()
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/widgets/{wid}", auth=AUTH, json={
        "sidebar": "front_top",
        "instance": {"raw": {"content": f"<!-- wp:html -->{build_html()}<!-- /wp:html -->"}},
    })
    r.raise_for_status()
    print(wid, "updated")


def restore():
    wid = (HERE / "widget_id.txt").read_text(encoding="utf-8").strip()
    r = requests.delete(f"{WP_URL}/wp-json/wp/v2/widgets/{wid}", auth=AUTH, params={"force": "true"})
    print(wid, r.status_code)


if __name__ == "__main__":
    {"restore": restore, "update": update}.get((sys.argv[1:] or [""])[0], create)()
