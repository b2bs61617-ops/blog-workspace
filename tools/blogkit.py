# -*- coding: utf-8 -*-
"""マツの道具の共通部品(2026-11-14〜)。記事ごとのスクリプトが毎回書き写していた部品を1か所にまとめたもの。

- .envの読み込み(ローカル → Googleドライブの.envで補う。全PC共通)
- サイトの表(SITES)と投稿者の決め方
- WordPressの読み書き(標準ライブラリだけ。pip不要)
- 記事ブロックの部品(Blocks: p / h2 / h3 / html / table / mini / mark / youtube / xembed / gmap / checks / wakaru)
- 下書き投稿(二重投稿よけの控え articles/<key>_posted.json、【未】付き、status:draft固定)
- 公開 → Indexing → X/Threads(承認されたときだけ呼ぶ。勝手に公開しない)

Python 3.9でも動くように書く(ユカのMacが3.9.6)。`X | None` や match は使わない。

usage:
    python tools/blogkit.py check          # このPCで各サイトの鍵がそろっているか(キー名だけ表示)と接続を確認
記事スクリプトからの使い方は docs/toolbox.md を参照。
"""
import base64
import glob
import json
import mimetypes
import os
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
ARTICLES = ROOT / "articles"
UA = "Mozilla/5.0 (blog-workspace toolbox)"

# authors: hostnameの先頭(小文字で比較) → そのサイトのWordPressユーザーID(docs/wordpress.mdの表と同じ)
SITES = {
    "trend": {"env": "WP_TREND", "domain": "chomoand.com", "label": "トレンド", "group": None,
              "x_account": "trend", "authors": {"user1": 3, "tomoki": 4}},
    "sixtones": {"env": "WP_AUDITION", "domain": "chomoand-0.com", "label": "SixTONES", "group": "sixtones",
                 "x_account": "main", "authors": {"user1": 2, "tomoki": 1}},
    "ko1keyz": {"env": "WP_KOIKEYS", "domain": "chomoand-1.com", "label": "KO1KEYZ", "group": "ko1keyz",
                "x_account": "main", "authors": {"user1": 2}},
    "snowman": {"env": "WP_CHOMO2", "domain": "chomoand-2.com", "label": "Snow Man", "group": "snowman",
                "x_account": "main", "authors": {"user1": 2, "tomoki": 1, "yuka": 1}},
    "travis": {"env": "WP_CHOMO4", "domain": "chomoand-4.blog", "label": "トラジャ", "group": "travis",
               "x_account": "main", "authors": {"user1": 2, "tomoki": 1}},
    "ktl": {"env": "WP_CHOMO5", "domain": "chomoand-5.site", "label": "キテレツ", "group": "ktl",
            "x_account": "main", "authors": {"user1": 2, "tomoki": 1}},
}
LOCAL_FIRST_PREFIXES = ("GOOGLE_INDEXING",)  # PCごとにパスが違うのでローカルの値を優先するキー


# ---------------------------------------------------------------- .env
def parse_env(text):
    env = {}
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def merge_env(local, drive):
    """ドライブ側が正(空でない値で上書き)。ただしLOCAL_FIRST_PREFIXESのキーはローカルに値があればそちら。"""
    out = dict(local)
    for k, v in drive.items():
        if not v:
            continue
        if k.startswith(LOCAL_FIRST_PREFIXES) and local.get(k):
            continue
        out[k] = v
    return out


def drive_env_candidates():
    home = os.path.expanduser("~")
    c = [os.environ.get("BLOG_WORKSPACE_ENV_SRC")]
    for base in glob.glob(os.path.join(home, "Library", "CloudStorage", "GoogleDrive-*")):  # Mac
        for d in ("マイドライブ", "My Drive"):
            c += [os.path.join(base, d, ".env"), os.path.join(base, d, "ブログ関係", ".env")]
    for base in ("G:\\", "H:\\", home):  # Windows
        for d in ("マイドライブ", "My Drive"):
            c += [os.path.join(base, d, ".env"), os.path.join(base, d, "ブログ関係", ".env")]
    return [p for p in c if p]


def _read(path):
    try:
        return parse_env(Path(path).read_text(encoding="utf-8-sig"))
    except OSError:
        return {}


def load_env():
    """ローカルの.envを読み、Googleドライブの.envがあれば補う。クラウド版(Linux)はローカルだけ。"""
    local = _read(ROOT / ".env")
    for p in drive_env_candidates():
        if os.path.exists(p):
            return merge_env(local, _read(p))
    return local


def share_env(env=None):
    """既存の道具(x_auto_post_buffer / google_indexing / naver_indexnow / ai_hub)にも同じenvを使わせる。"""
    env = env if env is not None else load_env()
    sys.path.insert(0, str(TOOLS)) if str(TOOLS) not in sys.path else None
    for name in ("x_auto_post_buffer", "google_indexing", "naver_indexnow", "ai_hub"):
        try:
            mod = __import__(name)
            mod.load_env = lambda *_a, **_k: dict(env)
        except Exception:  # noqa: BLE001  (requests等が無いPCでも止めない)
            pass
    return env


# ---------------------------------------------------------------- サイト
def site(key):
    if key not in SITES:
        raise SystemExit("サイト名は {} のどれかワン".format(" / ".join(SITES)))
    return SITES[key]


def site_by_url(url):
    host = urllib.parse.urlparse(url).netloc.lower().replace("www.", "")
    for k, s in SITES.items():
        if s["domain"] == host:
            return k
    return None


def author_for(site_key, hostname=None):
    host = (hostname or socket.gethostname()).split(".")[0].lower()
    for prefix, uid in site(site_key)["authors"].items():
        if host.startswith(prefix):
            return uid
    return None


# ---------------------------------------------------------------- WordPress
class WP(object):
    def __init__(self, site_key, env=None):
        self.key = site_key
        self.conf = site(site_key)
        env = env if env is not None else load_env()
        pre = self.conf["env"]
        self.base = (env.get(pre + "_URL") or "https://" + self.conf["domain"]).rstrip("/")
        user, pw = env.get(pre + "_USERNAME"), env.get(pre + "_APP_PASSWORD")
        self.auth = base64.b64encode("{}:{}".format(user, pw).encode()).decode() if user and pw else None

    def _req(self, path, data=None, headers=None, method="GET", auth=True, raw=False):
        url = path if path.startswith("http") else self.base + "/wp-json/wp/v2" + path
        r = urllib.request.Request(url, data=data, method=method)
        r.add_header("User-Agent", UA)
        if auth:
            if not self.auth:
                raise RuntimeError("{} の鍵が.envに無いワン({}_USERNAME / _APP_PASSWORD)".format(self.key, self.conf["env"]))
            r.add_header("Authorization", "Basic " + self.auth)
        for k, v in (headers or {}).items():
            r.add_header(k, v)
        try:
            with urllib.request.urlopen(r, timeout=120) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                return (body, resp.headers) if raw else body
        except urllib.error.HTTPError as e:
            raise RuntimeError("{} {} {}".format(e.code, url, e.read().decode("utf-8", "ignore")[:300]))

    def get(self, path, auth=True, **params):
        if params:
            path += ("&" if "?" in path else "?") + urllib.parse.urlencode(params)
        return self._req(path, auth=auth)

    def post(self, path, obj):
        return self._req(path, json.dumps(obj).encode("utf-8"), {"Content-Type": "application/json"}, "POST")

    def get_post(self, post_id):
        return self.get("/posts/{}".format(post_id), context="edit")

    def public_posts(self, fields="id,date,modified,link,slug,title,content,categories,featured_media", limit=None):
        """公開記事を全部読む(認証なし)。"""
        out, page = [], 1
        while True:
            path = "/posts?" + urllib.parse.urlencode({"per_page": 100, "page": page, "_fields": fields})
            body, headers = self._req(path, auth=False, raw=True)
            out += body
            if page >= int(headers.get("X-WP-TotalPages", 1)) or (limit and len(out) >= limit):
                return out[:limit] if limit else out
            page += 1

    def upload_media(self, file_path, alt=""):
        fn = os.path.basename(file_path)
        ctype = mimetypes.guess_type(fn)[0] or "image/png"
        with open(file_path, "rb") as f:
            m = self._req("/media", f.read(), {"Content-Type": ctype,
                          "Content-Disposition": 'attachment; filename="{}"'.format(urllib.parse.quote(fn))}, "POST")
        if alt:
            self.post("/media/{}".format(m["id"]), {"alt_text": alt})
        return m["id"]


# ---------------------------------------------------------------- 記事ブロック
class Blocks(object):
    """色を決めて使う。 b = Blocks("#c2410c", "#f2c9a8", "#fff7ef") → b.p(...), b.h2(...)"""

    def __init__(self, accent="#c2410c", border="#f2c9a8", bg="#fff7ef"):
        self.A, self.B, self.BG = accent, border, bg

    @staticmethod
    def p(*lines):
        return "<!-- wp:paragraph -->\n<p>" + "<br>\n".join(lines) + "</p>\n<!-- /wp:paragraph -->\n\n"

    @staticmethod
    def h2(t):
        return '<!-- wp:heading -->\n<h2 class="wp-block-heading">{}</h2>\n<!-- /wp:heading -->\n\n'.format(t)

    @staticmethod
    def h3(t):
        return '<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{}</h3>\n<!-- /wp:heading -->\n\n'.format(t)

    @staticmethod
    def html(s):
        return "<!-- wp:html -->\n" + s.strip() + "\n<!-- /wp:html -->\n\n"

    @staticmethod
    def mark(t):
        return '<strong><span class="swl-marker mark_yellow" style="font-size:1.15em;">{}</span></strong>'.format(t)

    @staticmethod
    def link(url, text):
        return '<a href="{}" target="_blank" rel="noopener">{}</a>'.format(url, text)

    def table(self, head, rows):
        th = "border:1px solid #ccc;padding:8px 12px;background:{};color:#fff;".format(self.A)
        td = "border:1px solid #ccc;padding:8px 12px;"
        h = "".join('<th style="{}">{}</th>'.format(th, c) for c in head) if head else ""
        body = ""
        for i, r in enumerate(rows):
            st = td + ("background:{};".format(self.BG) if i % 2 else "")
            body += "<tr>" + "".join('<td style="{}">{}</td>'.format(st, c) for c in r) + "</tr>\n"
        thead = "<thead><tr>{}</tr></thead>\n".format(h) if head else ""
        return ('<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout">'
                + thead + "<tbody>\n" + body + "</tbody></table></figure>\n<!-- /wp:table -->\n\n")

    def mini(self, *kv):
        inner = "".join('<p style="margin:{};"><strong>{}:</strong>{}</p>'.format("0" if i == 0 else "4px 0 0 0", k, v)
                        for i, (k, v) in enumerate(kv))
        return self.html('<div style="border:1px solid {};border-left:4px solid {};border-radius:4px;padding:10px 16px;'
                         'margin:0 0 16px 0;background:{};">{}</div>'.format(self.B, self.A, self.BG, inner))

    def checks(self, items):
        """チェックマークつきの枠(まとめ・理由の一覧)。"""
        chk = ('<span style="display:inline-block;min-width:1.1em;padding:0 3px;border:1px solid {a};border-radius:3px;'
               'color:{a};font-weight:bold;text-align:center;margin-right:6px;font-size:0.85em;">&#10003;</span>').format(a=self.A)
        inner = "".join('<p style="margin:{};">{}{}</p>'.format("0" if i == 0 else "6px 0 0 0", chk, t)
                        for i, t in enumerate(items))
        return self.html('<div style="border:1px solid {};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;'
                         'background:{};">{}</div>'.format(self.A, self.BG, inner))

    def wakaru(self, items):
        """「この記事でわかること」の枠。"""
        lis = "\n".join("<li>{}</li>".format(t) for t in items)
        return self.html('<div style="border:1px solid #ddd;border-radius:4px;margin:0 0 16px 0;overflow:hidden;">\n'
                         '<p style="font-weight:bold;font-size:1.05em;margin:0;padding:10px 18px;background:{};color:#fff;">'
                         'この記事でわかること</p>\n<ul style="margin:0;padding:14px 18px 14px 34px;background:{};">\n{}\n</ul>\n</div>'
                         .format(self.A, self.BG, lis))

    @staticmethod
    def youtube(url):
        return ('<!-- wp:embed {"url":"' + url + '","type":"video","providerNameSlug":"youtube","responsive":true,'
                '"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->\n'
                '<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube '
                'wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\n'
                + url + "\n</div></figure>\n<!-- /wp:embed -->\n\n")

    @staticmethod
    def xembed(url):
        return ('<!-- wp:embed {"url":"' + url + '","type":"rich","providerNameSlug":"twitter","responsive":true} -->\n'
                '<figure class="wp-block-embed is-type-rich is-provider-twitter wp-block-embed-twitter">'
                '<div class="wp-block-embed__wrapper">\n' + url + "\n</div></figure>\n<!-- /wp:embed -->\n\n")

    def gmap(self, q):
        return self.html('<iframe src="https://www.google.com/maps?q={}&output=embed" width="100%" height="300" '
                         'style="border:0;" allowfullscreen="" loading="lazy"></iframe>'.format(urllib.parse.quote(q)))


# ---------------------------------------------------------------- 仕上げ・下書き・公開
def _tools_on_path():
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))


def finalize(html, site_key, names=()):
    """さん付け → ひらがな直し。投稿前に必ず通す。"""
    _tools_on_path()
    import easy_read
    import honorific
    group = site(site_key)["group"]
    if group is None:  # トレンドは名簿なし。namesで渡した人名だけに付く
        honorific.GROUPS.setdefault("none", {})
        group = "none"
    return easy_read.fix(honorific.add_san(html, group, names))


def strip_mi(title):
    return title.replace("【未】", "").strip()


def upload_draft(site_key, key, title, content, slug, categories, eyecatch=None, eyecatch_alt="",
                 names=(), update=False, force=False, env=None, check=True):
    """下書きで投稿する。控えは articles/<key>_posted.json。再実行しても二重投稿しない。

    update=True で本文を上書き(status:draft固定)。公開済みの記事は上書きしない。
    check=True のとき事実チェック係でNGがあれば止める(force=Trueで通す)。
    """
    title = strip_mi(title)
    if len(title) > 35:
        raise SystemExit("タイトルが{}字(35字まで)ワン: {}".format(len(title), title))
    ARTICLES.mkdir(exist_ok=True)
    (ARTICLES / (key + ".html")).write_text(content, encoding="utf-8")
    if check:
        _tools_on_path()
        import fact_check
        rep = fact_check.run(content, site_key=site_key, title=title, names=names, net=False)
        print(fact_check.format_report(rep))
        if rep["ng"] and not force:
            raise SystemExit("事実チェックでNGが{}件。直してからもう一度ワン(どうしても通すなら force=True)".format(len(rep["ng"])))
    wp = WP(site_key, env)
    author = author_for(site_key)
    if author is None:
        raise SystemExit("このPC({})の投稿者がSITESに無いワン。docs/wordpress.mdの表とtools/blogkit.pyに足してワン".format(socket.gethostname()))
    state_path = ARTICLES / (key + "_posted.json")
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}

    def save():
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    if "post" in state:
        cur = wp.get_post(state["post"])
        if update and cur["status"] == "draft":
            wp.post("/posts/{}".format(state["post"]), {"title": "【未】" + title, "content": content, "status": "draft"})
            print("本文を更新", state["post"])
        elif update:
            raise SystemExit("ID{}は{}。公開済みの記事は上書きしないワン(ユーザー確認が要る)".format(state["post"], cur["status"]))
        else:
            print("投稿済み", state["post"])
    else:
        po = wp.post("/posts", {"title": "【未】" + title, "content": content, "slug": slug, "status": "draft",
                                "categories": list(categories), "author": author})
        state.update({"post": po["id"], "site": site_key})
        save()
        print("下書き", po["id"])
    if eyecatch and "eyecatch" not in state and os.path.exists(str(eyecatch)):
        state["eyecatch"] = wp.upload_media(str(eyecatch), eyecatch_alt)
        save()
        wp.post("/posts/{}".format(state["post"]), {"featured_media": state["eyecatch"], "status": "draft"})
    po = wp.get_post(state["post"])
    print(po["id"], po["status"], "author", po["author"], po["categories"], "eyecatch", po["featured_media"], po["title"]["raw"])
    print("{}/?p={}".format(wp.base, po["id"]))
    return po


def publish(site_key, post_id, text, tags, due_at=None, env=None, x=True):
    """公開 → Indexing → X/Threads。ユーザーが「公開して」と言った記事にだけ使う。

    タイトルは【未】を外すだけで変えない。X文は xpost_ideas.problems でルール違反があれば投稿しない。
    """
    _tools_on_path()
    env = share_env(env)
    wp = WP(site_key, env)
    if x:
        import xpost_ideas
        bad = xpost_ideas.problems(text, tags)
        if bad:
            raise SystemExit("X投稿文がルール違反ワン: " + " / ".join(bad))
    cur = wp.get_post(post_id)
    if cur["status"] == "publish":
        link = cur["link"]
        print("公開済み", post_id, link)
    else:
        r = wp.post("/posts/{}".format(post_id), {"status": "publish", "title": strip_mi(cur["title"]["raw"])})
        link = r.get("link")
        print("公開", post_id, r.get("status"), link, flush=True)
    result = {"link": link}
    try:
        import google_indexing
        result["indexing"] = google_indexing.notify(link)
        print("Indexing", result["indexing"], flush=True)
    except Exception as e:  # noqa: BLE001
        print("Indexing 失敗(公開は済み)", e, flush=True)
    if x:
        try:
            import x_auto_post_buffer as xb
            imgs = xb.fetch_article_images(wp.base, post_id)
            account = site(site_key)["x_account"]
            result["x"] = xb.post_thread(text, tags, imgs, link, due_at=due_at, account=account)
            print("X", len(imgs), "枚", result["x"], flush=True)
        except Exception as e:  # noqa: BLE001
            print("X 失敗(公開は済み)", e, flush=True)
    return result


# ---------------------------------------------------------------- CLI
def _check():
    env = load_env()
    drive = [p for p in drive_env_candidates() if os.path.exists(p)]
    print("PC:", socket.gethostname(), "/ Python", sys.version.split()[0])
    print("ローカル.env:", "あり" if (ROOT / ".env").exists() else "なし", "/ ドライブ.env:", "あり" if drive else "見つからない")
    ok = True
    for k, s in SITES.items():
        pre = s["env"]
        miss = [n for n in ("_URL", "_USERNAME", "_APP_PASSWORD") if not env.get(pre + n)]
        try:
            n = len(WP(k, env).get("/posts", auth=False, per_page=1, _fields="id"))
            net = "つながる" if n else "記事0件"
        except Exception as e:  # noqa: BLE001
            net = "つながらない({})".format(str(e)[:40])
        who = author_for(k)
        print("  {:9s} 鍵:{} / 接続:{} / 投稿者:{}".format(
            k, "OK" if not miss else "不足 " + ",".join(pre + m for m in miss), net, who if who else "未登録"))
        ok = ok and not miss
    extra = ["BUFFER_ACCESS_TOKEN", "GEMINI_API_KEY", "GOOGLE_INDEXING_CREDENTIALS_PATH"]
    print("  そのほか:", ", ".join("{}={}".format(k, "あり" if env.get(k) else "なし") for k in extra))
    return 0 if ok else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1:2] == ["check"]:
        sys.exit(_check())
    print(__doc__)
