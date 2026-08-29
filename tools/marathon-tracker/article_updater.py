"""WordPress 記事の「リアルタイム情報」セクション内のマーカー領域だけを差し替える。

- 触るのは <!-- MARATHON_TRACKER:BEGIN --> 〜 <!-- MARATHON_TRACKER:END --> の間だけ。
- 更新 POST には status:publish を必ず含める(省略すると下書きに戻る事象があるため)。
- 上書き前に旧本文を backups/ に保存。
"""
import base64
import html
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BACKUP_DIR = HERE / "backups"

BEGIN = "<!-- MARATHON_TRACKER:BEGIN -->"
END = "<!-- MARATHON_TRACKER:END -->"


def load_env():
    env = {}
    f = ROOT / ".env"
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def _auth(cfg):
    env = load_env()
    pre = cfg["wp_env_prefix"]
    url = env[f"{pre}_URL"].rstrip("/")
    user = env[f"{pre}_USERNAME"]
    pw = env[f"{pre}_APP_PASSWORD"]
    return url, base64.b64encode(f"{user}:{pw}".encode()).decode()


def get_post(cfg):
    url, auth = _auth(cfg)
    api = f"{url}/wp-json/wp/v2/posts/{cfg['post_id']}?context=edit"
    req = urllib.request.Request(api, headers={"Authorization": f"Basic {auth}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read())
    return {
        "id": d["id"],
        "status": d["status"],
        "title": d["title"]["raw"],
        "content": d["content"]["raw"],
        "modified": d.get("modified"),
        "link": d.get("link", ""),
    }


def put_post(cfg, new_content):
    """content を更新。status:publish を明示。戻り値は更新後の status。"""
    url, auth = _auth(cfg)
    api = f"{url}/wp-json/wp/v2/posts/{cfg['post_id']}"
    body = json.dumps({"content": new_content, "status": "publish"}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        api, data=body, method="POST",
        headers={"Authorization": f"Basic {auth}",
                 "Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read())
    return d.get("status")


def backup(cfg, content):
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    p = BACKUP_DIR / f"{cfg['post_id']}_{ts}.html"
    p.write_text(content, encoding="utf-8")
    return p


def _map_iframe(query, zoom=15):
    q = urllib.parse.quote(query)
    return (
        f'<iframe src="https://maps.google.com/maps?q={q}&t=&z={zoom}&ie=UTF8&iwloc=&output=embed" '
        f'width="100%" height="350" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>'
    )


def render_region(current_location, entries, updated_at, map_zoom=15,
                  heading="星野真里は今どこ？（リアルタイム更新）"):
    """entries: [{"time","text","map_query"}]  新しい順で渡すこと。

    先頭に H2 見出しを含める(記事の一番上に置く前提)。
    """
    loc = html.escape(current_location or "確認中")
    parts = [BEGIN]
    if heading:
        parts.append("<!-- wp:heading -->")
        parts.append(f'<h2 class="wp-block-heading">{html.escape(heading)}</h2>')
        parts.append("<!-- /wp:heading -->")
    parts.append("<!-- wp:html -->")
    parts.append(
        '<div style="border:1px solid #ddd;border-left:4px solid #d24;border-radius:4px;'
        'padding:10px 16px;margin:16px 0;background:#fff7f7;">'
    )
    parts.append(f'<p style="margin:0;"><strong>現在地(自動更新):</strong> {loc}</p>')
    parts.append(
        f'<p style="margin:4px 0 0 0;font-size:0.9em;color:#666;">最終更新: {html.escape(updated_at)}'
        "／地図・YouTube生配信のチャット・Xの沿道情報をもとに自動で追記しています。正確な通過地点は番組の公式発表が基準です。</p>"
    )
    parts.append("</div>")
    parts.append("<!-- /wp:html -->")

    for e in entries:
        t = html.escape(e.get("time", "").strip())
        body = html.escape(e.get("text", "").strip())
        mq = e.get("map_query", "").strip()
        parts.append("<!-- wp:html -->")
        head = f"<strong>【{t}】</strong>" if t else ""
        parts.append(f"<p>{head}{body}</p>")
        if mq:
            parts.append(_map_iframe(mq, map_zoom))
        parts.append("<!-- /wp:html -->")

    parts.append(END)
    return "\n".join(parts)


def splice(content, region_html, section_contains=None, next_contains=None):
    """マーカー領域を常に「記事の最初の H2 の直前」に置く。

    既存のマーカー領域はどこにあっても本文から除去してから、先頭側へ挿入し直す。
    (トモキ指示 2026-08-29: 更新される見出しを記事の一番上に)
    section_contains / next_contains は後方互換のため受け取るだけ(未使用)。
    """
    # 既存マーカー領域を丸ごと除去
    if BEGIN in content and END in content:
        pre = content.split(BEGIN, 1)[0].rstrip()
        post = content.split(END, 1)[1].lstrip()
        content = pre + ("\n\n" if pre and post else "") + post

    # 最初の見出し(直前の wp:heading コメントごと)の位置。無ければ本文先頭。
    m = re.search(r"(<!--\s*wp:heading[^>]*-->\s*)?<h2[\s>]", content)
    insert_at = m.start() if m else 0

    block = region_html.rstrip() + "\n\n"
    return content[:insert_at] + block + content[insert_at:]


def region_of(content):
    if BEGIN in content and END in content:
        return BEGIN + content.split(BEGIN, 1)[1].split(END, 1)[0] + END
    return ""
