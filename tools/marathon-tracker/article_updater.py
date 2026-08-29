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


def render_region(current_location, entries, updated_at, map_zoom=15):
    """entries: [{"time","text","map_query"}]  新しい順で渡すこと。"""
    loc = html.escape(current_location or "確認中")
    parts = [BEGIN]
    parts.append("<!-- wp:html -->")
    parts.append(
        '<div style="border:1px solid #ddd;border-left:4px solid #d24;border-radius:4px;'
        'padding:10px 16px;margin:16px 0;background:#fff7f7;">'
    )
    parts.append(f'<p style="margin:0;"><strong>現在地(自動更新):</strong> {loc}</p>')
    parts.append(
        f'<p style="margin:4px 0 0 0;font-size:0.9em;color:#666;">最終更新: {html.escape(updated_at)}'
        "／YouTube生配信のチャットやXの沿道情報をもとに自動で追記しています。正確な通過地点は番組の公式発表が基準です。</p>"
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


def splice(content, region_html, section_contains, next_contains):
    """マーカー領域を region_html で置換。無ければ該当セクション末尾に挿入。"""
    if BEGIN in content and END in content:
        pre = content.split(BEGIN, 1)[0]
        post = content.split(END, 1)[1]
        return pre + region_html + post

    # セクション見出し(h2 に section_contains を含む)を探す
    sec = re.search(r"<h2[^>]*>[^<]*" + re.escape(section_contains) + r"[^<]*</h2>", content)
    if not sec:
        raise RuntimeError(f"セクション見出しが見つからない: ...{section_contains}...")

    # そのセクション以降で、次の見出し(h2 に next_contains を含む)の直前 wp:heading コメントを探す
    after = content[sec.end():]
    nxt = re.search(r"(<!-- wp:heading -->\s*)?<h2[^>]*>[^<]*" + re.escape(next_contains) + r"[^<]*</h2>", after)
    if not nxt:
        raise RuntimeError(f"次セクション見出しが見つからない: ...{next_contains}...")

    insert_at = sec.end() + nxt.start()
    block = region_html + "\n\n"
    return content[:insert_at] + block + content[insert_at:]


def region_of(content):
    if BEGIN in content and END in content:
        return BEGIN + content.split(BEGIN, 1)[1].split(END, 1)[0] + END
    return ""
