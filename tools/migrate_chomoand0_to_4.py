"""chomoand-0.com の公開記事を chomoand-4.blog へ引っ越す(コンテンツ移行のみ)。

- chomoand-0.com は契約ISP(ZAQ/J:COM)のDNS横取りが未解決なので、
  正しいIP(85.131.207.35)を直接指定 + SNIで名前解決を回避して接続する。
  詳細は docs/wordpress.md の「chomoand-0.com DNS問題」参照。
- 移行するもの: タイトル / 本文(Gutenbergブロックのraw) / 抜粋 / スラッグ /
  公開日(date・date_gmt維持) / カテゴリ(chomoand-4側に作成しマッピング) /
  アイキャッチ画像 / 本文中のアップロード画像(chomoand-4へ再アップしURL貼り替え) /
  SWELL系メタ(swell_btn_cv_data・footnotes)。
- 冪等: 既に移行済みの記事・画像は台帳(tools/migrate_chomoand0_to_4_ledger.json)で
  スキップする。途中で失敗しても再実行で続きから。
- 既定は下書き(status=draft)で作成。--publish で公開状態にする。

使い方:
  python tools/migrate_chomoand0_to_4.py                 # 全42本を下書きで移行(ドライラン相当)
  python tools/migrate_chomoand0_to_4.py --limit 2       # 先頭2本だけ
  python tools/migrate_chomoand0_to_4.py --only 595,612  # 指定IDだけ
  python tools/migrate_chomoand0_to_4.py --publish       # 公開状態で作成
  python tools/migrate_chomoand0_to_4.py --redirects-only  # 台帳から redirects.csv だけ再生成
"""
import argparse
import base64
import io
import json
import os
import re
import socket
import ssl
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = ROOT / "tools" / "migrate_chomoand0_to_4_ledger.json"
REDIRECTS_CSV = ROOT / "tools" / "migrate_chomoand0_to_4_redirects.csv"

SRC_HOST = "chomoand-0.com"
SRC_IP = "85.131.207.35"          # ISPのDNS横取りを回避するための正しいIP
UPLOAD_RE = re.compile(
    r"https?://(?:www\.)?chomoand-0\.com/wp-content/uploads/"
    r"([^\s\"'\\)]+?\.(?:jpe?g|png|webp|gif|avif))",
    re.IGNORECASE,
)
SIZE_SUFFIX_RE = re.compile(r"-\d+x\d+(?=\.[A-Za-z0-9]+$)")


def load_env():
    env = {}
    p = ROOT / ".env"
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return {**env, **os.environ}


class WP:
    """最小WP RESTクライアント。pin_ip を渡すとそのIPへ直接接続(SNIはhostのまま)。"""

    def __init__(self, base_url, user, app_password, pin_ip=None):
        u = urllib.parse.urlparse(base_url)
        self.host = u.netloc
        self.pin_ip = pin_ip
        self.auth = base64.b64encode(f"{user}:{app_password}".encode()).decode()
        self.ctx = ssl.create_default_context()

    def _sock(self):
        raw = socket.create_connection((self.pin_ip or self.host, 443), timeout=60)
        return self.ctx.wrap_socket(raw, server_hostname=self.host)

    def _raw_request(self, method, path, params=None, body=None, headers=None):
        if params:
            path += ("&" if "?" in path else "?") + urllib.parse.urlencode(params, doseq=True)
        hdrs = {
            "Host": self.host,
            "User-Agent": "chomoand-migrate/1.0",
            "Accept": "*/*",
            "Authorization": f"Basic {self.auth}",
            "Connection": "close",
        }
        if headers:
            hdrs.update(headers)
        payload = b""
        if body is not None:
            if isinstance(body, (dict, list)):
                payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
                hdrs["Content-Type"] = "application/json; charset=utf-8"
            else:
                payload = body
            hdrs["Content-Length"] = str(len(payload))
        ss = self._sock()
        req = f"{method} {path} HTTP/1.1\r\n" + "".join(f"{k}: {v}\r\n" for k, v in hdrs.items()) + "\r\n"
        ss.sendall(req.encode("utf-8") + payload)
        buf = b""
        while True:
            chunk = ss.recv(65536)
            if not chunk:
                break
            buf += chunk
        ss.close()
        head, _, rest = buf.partition(b"\r\n\r\n")
        status = int(head.split(b"\r\n", 1)[0].split()[1])
        if b"transfer-encoding: chunked" in head.lower():
            rest = _dechunk(rest)
        return status, head, rest

    def api(self, method, route, params=None, body=None, headers=None):
        path = "/wp-json" + route
        st, head, rest = self._raw_request(method, path, params, body, headers)
        if st >= 400:
            raise RuntimeError(f"{method} {route} -> {st}\n{rest[:800].decode('utf-8', 'replace')}")
        return json.loads(rest.decode("utf-8")) if rest.strip() else None

    def get(self, route, params=None):
        return self.api("GET", route, params=params)

    def get_binary(self, url):
        path = urllib.parse.urlparse(url).path
        st, head, rest = self._raw_request("GET", path)
        if st >= 400:
            raise RuntimeError(f"GET binary {url} -> {st}")
        ctype = ""
        for line in head.decode("latin1").split("\r\n"):
            if line.lower().startswith("content-type:"):
                ctype = line.split(":", 1)[1].strip()
        return rest, ctype

    def upload_media(self, data, filename, ctype):
        st, head, rest = self._raw_request(
            "POST", "/wp-json/wp/v2/media", body=data,
            headers={
                "Content-Type": ctype or "application/octet-stream",
                "Content-Disposition": f'attachment; filename="{filename}"',
            },
        )
        if st >= 400:
            raise RuntimeError(f"upload {filename} -> {st}\n{rest[:500].decode('utf-8','replace')}")
        return json.loads(rest.decode("utf-8"))


def _dechunk(data):
    out = b""
    while data:
        line, _, rest = data.partition(b"\r\n")
        try:
            size = int(line.strip() or b"0", 16)
        except ValueError:
            break
        if size == 0:
            break
        out += rest[:size]
        data = rest[size + 2:]
    return out


def load_ledger():
    if LEDGER_PATH.exists():
        return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return {"posts": {}, "media": {}, "categories": {}}


def save_ledger(ledger):
    LEDGER_PATH.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def sync_categories(src, dst, ledger):
    """chomoand-0 のカテゴリを chomoand-4 に作成し、旧ID->新ID を返す。"""
    src_cats = src.get("/wp/v2/categories", {"per_page": 100,
                        "_fields": "id,name,slug,description,parent"})
    dst_cats = dst.get("/wp/v2/categories", {"per_page": 100,
                        "_fields": "id,name,slug"})
    by_slug = {c["slug"]: c["id"] for c in dst_cats}
    id_map = {}
    # parent を先に作るため親なし→親ありの順
    for c in sorted(src_cats, key=lambda x: x["parent"]):
        if c["slug"] == "uncategorized":
            continue
        if c["slug"] in by_slug:
            new_id = by_slug[c["slug"]]
        else:
            payload = {"name": c["name"], "slug": c["slug"],
                       "description": c.get("description", "")}
            if c["parent"] and c["parent"] in id_map:
                payload["parent"] = id_map[c["parent"]]
            created = dst.api("POST", "/wp/v2/categories", body=payload)
            new_id = created["id"]
            by_slug[c["slug"]] = new_id
            print(f"  [cat] created {c['slug']} -> {new_id}")
        id_map[c["id"]] = new_id
    ledger["categories"] = {str(k): v for k, v in id_map.items()}
    return id_map


def migrate_image(src, dst, src_url, ledger, dry_run):
    """画像1枚(サイズ違いは元画像に正規化)を chomoand-4 に再アップ。新URLを返す。"""
    base_url = SIZE_SUFFIX_RE.sub("", src_url)
    key = urllib.parse.urlparse(base_url).path
    if key in ledger["media"]:
        return ledger["media"][key]["new_url"]
    if dry_run:
        print(f"    [img] (dry-run) would upload {base_url}")
        return src_url
    data, ctype = src.get_binary(base_url)
    if not data or len(data) < 100:
        # 元サイズが無い場合は与えられたURLをそのまま取得
        data, ctype = src.get_binary(src_url)
        base_url = src_url
    filename = urllib.parse.unquote(Path(urllib.parse.urlparse(base_url).path).name)
    media = dst.upload_media(data, filename, ctype)
    rec = {"new_id": media["id"], "new_url": media["source_url"], "src_url": base_url}
    ledger["media"][key] = rec
    print(f"    [img] {filename} -> {media['id']}")
    return media["source_url"]


def rewrite_content(src, dst, content, ledger, dry_run):
    urls = sorted(set(UPLOAD_RE.findall(content)))
    for rel in urls:
        old = f"https://chomoand-0.com/wp-content/uploads/{rel}"
        # http/www ゆらぎも拾う
        candidates = {old,
                      old.replace("https://", "http://"),
                      old.replace("chomoand-0.com", "www.chomoand-0.com")}
        new = migrate_image(src, dst, old, ledger, dry_run)
        for c in candidates:
            content = content.replace(c, new)
    return content


def migrate_post(src, dst, post, cat_map, ledger, dry_run, publish):
    old_id = post["id"]
    if str(old_id) in ledger["posts"]:
        print(f"[skip] {old_id} 既に移行済み -> {ledger['posts'][str(old_id)]['new_id']}")
        return
    title = post["title"]["raw"]
    print(f"[post] {old_id} {title[:48]}")
    content = rewrite_content(src, dst, post["content"]["raw"], ledger, dry_run)

    featured_new = 0
    if post.get("featured_media"):
        try:
            fm = src.get(f"/wp/v2/media/{post['featured_media']}",
                         {"_fields": "source_url,title"})
            new_url = migrate_image(src, dst, fm["source_url"], ledger, dry_run)
            if not dry_run:
                key = urllib.parse.urlparse(SIZE_SUFFIX_RE.sub("", fm["source_url"])).path
                featured_new = ledger["media"].get(key, {}).get("new_id", 0)
        except Exception as e:
            print(f"    [warn] featured media {post['featured_media']}: {e}")

    payload = {
        "title": title,
        "content": content,
        "excerpt": post["excerpt"]["raw"],
        "slug": post["slug"],
        "status": "publish" if publish else "draft",
        "date": post["date"],
        "date_gmt": post["date_gmt"],
        "categories": [cat_map.get(c, c) for c in post["categories"]],
        "comment_status": post.get("comment_status", "closed"),
        "ping_status": post.get("ping_status", "closed"),
    }
    meta = {k: v for k, v in (post.get("meta") or {}).items()
            if k in ("swell_btn_cv_data", "footnotes") and v}
    if meta:
        payload["meta"] = meta
    if featured_new:
        payload["featured_media"] = featured_new

    if dry_run:
        print(f"    [dry-run] would create: slug={payload['slug']} "
              f"cats={payload['categories']} date={payload['date']} "
              f"imgs_in_body={len(set(UPLOAD_RE.findall(post['content']['raw'])))}")
        return

    created = dst.api("POST", "/wp/v2/posts", body=payload)
    src_path = urllib.parse.urlparse(post["link"]).path
    new_path = urllib.parse.urlparse(created["link"]).path
    ledger["posts"][str(old_id)] = {
        "old_id": old_id, "old_link": post["link"], "old_path": src_path,
        "new_id": created["id"], "new_link": created["link"], "new_path": new_path,
        "status": created["status"],
    }
    save_ledger(ledger)
    print(f"    -> chomoand-4 #{created['id']} ({created['status']}) {created['link']}")


def write_redirects_csv(ledger):
    rows = ["source,target,code"]
    for rec in ledger["posts"].values():
        rows.append(f'{rec["old_path"]},{rec["new_link"]},301')
    REDIRECTS_CSV.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"redirects: {REDIRECTS_CSV}  ({len(ledger['posts'])} 件)")


def relink_internal(dst, ledger):
    """移行済み記事どうしの内部リンク(chomoand-0.com/... のaタグ)を
    chomoand-4 側の新URLへ貼り替える。移行対象外の記事へのリンクは
    chomoand-0 側の301に任せるためそのまま残す。"""
    url_map = {}
    for rec in ledger["posts"].values():
        for base in ("https://chomoand-0.com", "http://chomoand-0.com",
                     "https://www.chomoand-0.com", "http://www.chomoand-0.com"):
            url_map[base + rec["old_path"]] = rec["new_link"]
        # 下書き時に埋まった ?p=ID 形式も本パーマリンクへ寄せる
        if not rec["new_link"].endswith(f"?p={rec['new_id']}"):
            url_map[f'https://chomoand-4.blog/?p={rec["new_id"]}'] = rec["new_link"]
    # 長いパスから先に置換(前方一致の誤爆防止)
    ordered = sorted(url_map.items(), key=lambda kv: -len(kv[0]))
    for old_id, rec in ledger["posts"].items():
        try:
            cur = dst.get(f"/wp/v2/posts/{rec['new_id']}",
                          {"context": "edit", "_fields": "content"})["content"]["raw"]
            new = cur
            hits = 0
            for old_url, new_url in ordered:
                if old_url in new:
                    new = new.replace(old_url, new_url)
                    hits += 1
            if new != cur:
                dst.api("POST", f"/wp/v2/posts/{rec['new_id']}", body={"content": new})
                print(f"  #{rec['new_id']} 内部リンク {hits} 種を貼り替え")
        except Exception as e:
            print(f"  [ERROR] relink {old_id} -> #{rec['new_id']}: {e}")
    print("relink 完了。残った chomoand-0 リンクは移行対象外の記事宛て(301任せ)。")


def publish_migrated(dst, ledger):
    """台帳の全記事を publish にし、確定した本パーマリンクで台帳を更新する。"""
    for old_id, rec in ledger["posts"].items():
        try:
            if rec.get("status") != "publish":
                dst.api("POST", f"/wp/v2/posts/{rec['new_id']}",
                        body={"status": "publish"})
            fresh = dst.get(f"/wp/v2/posts/{rec['new_id']}",
                            {"_fields": "link,status"})
            rec["new_link"] = fresh["link"]
            rec["new_path"] = urllib.parse.urlparse(fresh["link"]).path
            rec["status"] = fresh["status"]
            print(f"  #{rec['new_id']} {fresh['status']} {fresh['link']}")
        except Exception as e:
            print(f"  [ERROR] {old_id} -> #{rec['new_id']}: {e}")
    save_ledger(ledger)
    write_redirects_csv(ledger)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--dry-run", action="store_true",
                    help="投稿も画像アップも行わず、何をするかだけ表示")
    ap.add_argument("--redirects-only", action="store_true")
    ap.add_argument("--publish-migrated", action="store_true",
                    help="台帳の全記事を publish にし、本URLで redirects.csv を再生成")
    ap.add_argument("--relink", action="store_true",
                    help="移行済み記事どうしの内部リンクを chomoand-4 の新URLへ貼り替え")
    args = ap.parse_args()

    ledger = load_ledger()
    if args.redirects_only:
        write_redirects_csv(ledger)
        return

    env = load_env()
    src = WP("https://chomoand-0.com", env["WP_AUDITION_USERNAME"],
             env["WP_AUDITION_APP_PASSWORD"], pin_ip=SRC_IP)
    dst = WP("https://chomoand-4.blog", env["WP_CHOMO4_USERNAME"],
             env["WP_CHOMO4_APP_PASSWORD"])

    if args.relink:
        print("== 内部リンク貼り替え ==")
        relink_internal(dst, ledger)
        return

    if args.publish_migrated:
        print("== 移行済み記事を公開 ==")
        publish_migrated(dst, ledger)
        return

    print("== カテゴリ同期 ==")
    cat_map = sync_categories(src, dst, ledger)
    save_ledger(ledger)
    print(f"  cat_map = {cat_map}")

    print("== 記事取得 ==")
    posts = src.get("/wp/v2/posts", {
        "per_page": 100, "status": "publish", "context": "edit", "orderby": "date",
        "order": "asc",
        "_fields": "id,slug,link,date,date_gmt,title,content,excerpt,"
                   "categories,featured_media,comment_status,ping_status,meta",
    })
    if args.only:
        want = {int(x) for x in args.only.split(",") if x.strip()}
        posts = [p for p in posts if p["id"] in want]
    if args.limit:
        posts = posts[: args.limit]
    print(f"  対象 {len(posts)} 本  (publish={args.publish}, dry_run={args.dry_run})")

    for i, post in enumerate(posts, 1):
        print(f"--- {i}/{len(posts)} ---")
        try:
            migrate_post(src, dst, post, cat_map, ledger, args.dry_run, args.publish)
        except Exception as e:
            print(f"    [ERROR] post {post['id']}: {e}")
        time.sleep(0.4)

    save_ledger(ledger)
    if not args.dry_run:
        write_redirects_csv(ledger)
    print("\n完了。台帳:", LEDGER_PATH)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
