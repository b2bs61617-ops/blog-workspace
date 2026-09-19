"""chomoand-4.blog 移行済み34記事のリライト用ヘルパー(docs/rules.md準拠のHTMLを組み立てる)。"""
import base64, json, re, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SITE = "https://chomoand-4.blog"

# bar=タイトルバー背景(白文字が読める濃さ) / accent=左線・チェックバッジ / border=薄い枠 / bg=箱の背景 / cell=表の項目名セル
PAL = {
    "group":    dict(bar="#7e57c2", accent="#7e57c2", border="#d9cdee", bg="#f5f2fb", cell="#ece5f7", mark="yellow", name="Travis Japan"),
    "miyachika": dict(bar="#d9787a", accent="#ef9a9a", border="#f3d6d6", bg="#fdf3f3", cell="#f9e4e4", mark="pink", name="宮近海斗"),
    "matsukura": dict(bar="#e0843a", accent="#f0a462", border="#f8dcc0", bg="#fef6ec", cell="#fbe9d5", mark="orange", name="松倉海斗"),
    "matsuda":   dict(bar="#4a86c5", accent="#6fa8dc", border="#cfe0f1", bg="#f1f6fb", cell="#e0ecf7", mark="blue", name="松田元太"),
    "shimekake": dict(bar="#e0679a", accent="#f48fb1", border="#f8d5e2", bg="#fdf1f6", cell="#fae0ea", mark="pink", name="七五三掛龍也"),
    "nakamura":  dict(bar="#4f9d55", accent="#81c784", border="#d0e8d1", bg="#f2f9f2", cell="#e1f1e2", mark="green", name="中村海人"),
    "kawashima": dict(bar="#7d8b99", accent="#a9b6c2", border="#dde3e8", bg="#f5f7f9", cell="#e8edf1", mark="orange", name="川島如恵留"),
    "yoshizawa": dict(bar="#b8921a", accent="#c9a227", border="#ecdca0", bg="#fdf8e6", cell="#f7edc4", mark="yellow", name="吉澤閑也"),
}

# chomoand-4.blog の記事ID -> (公開URL, 記事の主題を表すアンカー用の短い題名)
_map = {}


def load_link_map():
    import csv
    p = HERE / "redirect_mapping.csv"
    rows = list(csv.DictReader(open(ROOT / "backups/chomoand0_to_chomoand4_redirect_2026-09-18/redirect_mapping.csv", encoding="utf-8")))
    for r in rows:
        m = re.search(r"-(\d+)$", r["target"])
        _map[int(m.group(1))] = r["target"]
        # 旧chomoand-0のスラッグ末尾(ID)ではなく、chomoand-4のID(末尾)を使う
    return _map


load_link_map()


def url(pid):
    return _map[pid]


def a(pid, anchor):
    return f'<a href="{url(pid)}">{anchor}</a>'


# ---------- インライン ----------
def b(t):
    return f"<strong>{t}</strong>"


def mk(t, pal, big=True):
    style = ' style="font-size:1.15em;"' if big else ""
    return f'<strong><span class="swl-marker mark_{pal["mark"]}"{style}>{t}</span></strong>'


# ---------- ブロック ----------
def wrap(kind, inner):
    return f"<!-- wp:{kind} -->\n{inner}\n<!-- /wp:{kind} -->"


def p(*sents):
    """文(句点で終わる)を<br>改行でつなぐ。文字列に'\\n\\n'を入れても段落は割らない。"""
    body = "<br>\n".join(s.strip() for s in sents if s.strip())
    return wrap("paragraph", f"<p>{body}</p>")


def h2(t):
    return wrap("heading", f'<h2 class="wp-block-heading">{t}</h2>')


def h3(t):
    return '<!-- wp:heading {"level":3} -->\n' + f'<h3 class="wp-block-heading">{t}</h3>' + "\n<!-- /wp:heading -->"


def html(inner):
    return wrap("html", inner)


def summary_box(items, pal):
    li = "\n".join(f"<li>{i}</li>" for i in items)
    return html(
        f'<div style="border:1px solid {pal["border"]};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{pal["bar"]};color:#fff;">この記事でわかること</p>\n'
        f'<ul style="margin:0;padding:14px 18px 14px 34px;background:{pal["bg"]};">\n{li}\n</ul>\n</div>'
    )


def mini_box(pairs, pal):
    """各H2直後の答え先出しbox。pairs=[(ラベル, 値), ...]"""
    ps = []
    for i, (k, v) in enumerate(pairs):
        m = "0" if i == 0 else "4px 0 0 0"
        ps.append(f'<p style="margin:{m};"><strong>{k}:</strong>{v}</p>')
    return html(
        f'<div style="border:1px solid {pal["border"]};border-left:4px solid {pal["accent"]};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{pal["bg"]};">\n'
        + "\n".join(ps) + "\n</div>"
    )


def info_box(title, rows, pal):
    """項目:値の情報box(タイトル文字+2列表)。rows=[(項目, 値), ...]"""
    trs = "\n".join(
        f'<tr><td style="background:{pal["cell"]};border:1px solid #d5d5d5;padding:8px 12px;width:30%;white-space:nowrap;"><strong>{k}</strong></td>'
        f'<td style="border:1px solid #d5d5d5;padding:8px 12px;">{v}</td></tr>'
        for k, v in rows
    )
    return html(
        f'<div style="border:1px solid {pal["border"]};border-radius:4px;padding:16px 18px;margin:0 0 16px 0;background:#fff;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 10px 0;">{title}</p>\n'
        f'<table style="border-collapse:collapse;width:100%;">\n{trs}\n</table>\n</div>'
    )


def table(headers, rows, pal):
    """独立した比較表・一覧表(wp:table コアブロック、インラインstyle)。"""
    th = "".join(
        f'<td style="background:{pal["bar"]};color:#fff;border:1px solid #d5d5d5;padding:8px 12px;font-weight:bold;">{h}</td>' for h in headers
    )
    trs = [f"<tr>{th}</tr>"]
    for i, r in enumerate(rows):
        bg = "#ffffff" if i % 2 == 0 else pal["bg"]
        tds = "".join(f'<td style="background:{bg};border:1px solid #d5d5d5;padding:8px 12px;">{c}</td>' for c in r)
        trs.append(f"<tr>{tds}</tr>")
    inner = '<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>' + "".join(trs) + "</tbody></table></figure>"
    return wrap("table", inner)


def list_box(title, items, pal, ordered=False):
    tag = "ol" if ordered else "ul"
    li = "\n".join(f'<li style="margin:0 0 6px 0;">{i}</li>' for i in items)
    return html(
        f'<div style="border:1px solid {pal["border"]};border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{pal["bar"]};color:#fff;">{title}</p>\n'
        f'<{tag} style="margin:0;padding:14px 18px 14px 34px;background:{pal["bg"]};">\n{li}\n</{tag}>\n</div>'
    )


def buy_box(items, pal, title="購入先"):
    return list_box(title, items, pal)


def sns_box(quotes, pal, title="Xでの反応"):
    q = "<br>".join(f"「{x}」" for x in quotes)
    return html(
        f'<div style="border:1px solid {pal["border"]};border-radius:4px;padding:10px 16px;margin:0 0 16px 0;background:{pal["bg"]};">\n'
        f'<p style="margin:0 0 6px 0;font-weight:bold;font-size:0.9em;color:{pal["bar"]};">{title}</p>\n'
        f'<p style="margin:0;font-size:0.95em;">{q}</p>\n</div>'
    )


def person_box(name, body_html, pal):
    return html(
        f'<div style="border:1px solid {pal["border"]};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;color:{pal["bar"]};">{name}</p>\n'
        f'<p style="margin:0;">{body_html}</p>\n</div>'
    )


def matome_box(items, pal):
    badge = (
        f'<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {pal["accent"]};border-radius:3px;'
        f'color:{pal["bar"]};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>'
    )
    lines = "<br>\n".join(f"{badge}{i}" for i in items)
    return html(
        f'<div style="border:2px solid {pal["accent"]};border-radius:8px;background:{pal["bg"]};padding:1em 1.25em;margin:0 0 16px 0;">\n'
        f'<p style="margin:0;">\n{lines}\n</p>\n</div>'
    )


def related_box(links, pal, title="あわせて読みたい関連記事"):
    """links=[(pid, アンカー文), ...] 具体的なアンカーで、記事の一番下に置く。"""
    li = "\n".join(f'<li><a href="{url(pid)}">{t}</a></li>' for pid, t in links)
    return html(
        f'<div style="border:1px solid {pal["border"]};border-left:4px solid {pal["accent"]};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:{pal["bg"]};">\n'
        f'<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">{title}</p>\n'
        f'<ul style="margin:0;padding-left:1.3em;">\n{li}\n</ul>\n</div>'
    )


def map_embed(q, height=350):
    from urllib.parse import quote
    return html(
        f'<iframe src="https://maps.google.com/maps?q={quote(q)}&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=&amp;output=embed" '
        f'width="100%" height="{height}" frameborder="0" scrolling="no" style="border:0;" loading="lazy"></iframe>'
    )


# ---------- 既存画像の再利用 ----------
def figures(orig_html):
    """元記事の<figure>(画像)を抜き出し、figcaptionを'出典:URL'のみに正規化して返す。"""
    out = []
    for m in re.finditer(r"<figure[^>]*>.*?</figure>", orig_html, re.S):
        f = m.group(0)
        if "wp-block-table" in f:
            continue
        cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", f, re.S)
        if cap:
            u = re.search(r"https?://\S+", re.sub(r"<[^>]+>", " ", cap.group(1)))
            newcap = f'<figcaption class="wp-element-caption">出典:{u.group(0)}</figcaption>' if u else cap.group(0)
            f = f.replace(cap.group(0), newcap)
        out.append(f)
    return out


def with_cap(figure_html, text):
    """figcaptionを指定の出典文に差し替える(なければ追加)。"""
    cap = f'<figcaption class="wp-element-caption">{text}</figcaption>'
    if "<figcaption" in figure_html:
        return re.sub(r"<figcaption[^>]*>.*?</figcaption>", cap, figure_html, flags=re.S)
    return figure_html.replace("</figure>", cap + "</figure>")


def fig(figure_html):
    if 'class="wp-block-image' not in figure_html:
        figure_html = figure_html.replace("<figure", '<figure class="wp-block-image size-large"', 1)
    return '<!-- wp:image {"sizeSlug":"large"} -->\n' + figure_html + "\n<!-- /wp:image -->"


def build(blocks):
    return "\n\n".join(blocks) + "\n"


# ---------- WordPress ----------
def _env():
    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _hdr():
    e = _env()
    tok = base64.b64encode(f"{e['WP_CHOMO4_USERNAME']}:{e['WP_CHOMO4_APP_PASSWORD']}".encode()).decode()
    return e["WP_CHOMO4_URL"].rstrip("/"), {"Authorization": "Basic " + tok, "Content-Type": "application/json"}


def original(pid):
    return (HERE / "original" / f"{pid}.html").read_text(encoding="utf-8")


def push(pid, content, title=None, dry=False):
    """本文(とタイトル)を更新。公開状態は維持するので status=publish を明示する。"""
    base, h = _hdr()
    payload = {"content": content, "status": "publish"}
    if title:
        payload["title"] = title
    if dry:
        return None
    req = urllib.request.Request(f"{base}/wp-json/wp/v2/posts/{pid}", data=json.dumps(payload).encode("utf-8"), headers=h, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            d = json.load(r)
            return d["status"], d["link"]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")[:300]
