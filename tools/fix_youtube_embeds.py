# -*- coding: utf-8 -*-
"""YouTube埋め込みの再生エラー(エラー153)を機械的に直すツール。

原因: 手書きの <iframe src="https://www.youtube.com/embed/..."> に referrerpolicy が無いと、
YouTube側がリファラー無しと判断して「エラー153(動画プレーヤーの設定エラー)」で再生を拒否する。
(2026-11-10 KO1KEYZ金浦空港記事 15474 ほか35本で発覚)

直し方:
  1. <!-- wp:html --> で包んだ「div + YouTube iframe」だけのブロック
     → WordPress標準の YouTube埋め込みブロック(wp:embed)に置き換える
       (WordPressがoEmbedで referrerpolicy 付きiframeを出力する)
  2. それ以外の場所にある YouTube iframe で referrerpolicy が無いもの
     → referrerpolicy="strict-origin-when-cross-origin" を足す

使い方:
  python3 tools/fix_youtube_embeds.py --recent-minutes 60   # 全サイトの直近更新記事を検査・修正
  python3 tools/fix_youtube_embeds.py --all                 # 全サイト全記事を検査・修正
  python3 tools/fix_youtube_embeds.py --site KOIKEYS --ids 15474 15475
  python3 tools/fix_youtube_embeds.py --all --dry           # 直さずに一覧だけ
  python3 tools/fix_youtube_embeds.py --hook                # Claude Code PostToolUse フック用(stdinにJSON)

サイトは .env(と環境変数)の WP_<NAME>_URL / WP_<NAME>_USERNAME / WP_<NAME>_APP_PASSWORD
が揃っているものを全部自動で対象にする(空欄のサイトは黙ってスキップ)。
"""
import argparse
import base64
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = ROOT / "backups" / "youtube_embed_fix"
STATUSES = "publish,draft,future,pending,private"
REFPOL = 'referrerpolicy="strict-origin-when-cross-origin"'

WRAPPED_RE = re.compile(
    r'<!-- wp:html -->\s*<div[^>]*>\s*<iframe[^>]*src="https://www\.youtube(?:-nocookie)?\.com/embed/([\w-]{11})[^"]*"[^>]*>\s*</iframe>\s*</div>\s*<!-- /wp:html -->'
)
IFRAME_RE = re.compile(r'<iframe\b[^>]*youtube(?:-nocookie)?\.com/embed/[^>]*>', re.I)

# フックで反応するコマンド(記事を投稿・編集しうる python スクリプトの実行)
HOOK_CMD_RE = re.compile(r'python[0-9.]*\s.*\.py', re.S)


# このMacの .env で空欄の鍵はGoogleドライブの .env から補う(ビルドスクリプトと同じ読み方)。
# 補わないと、ドライブにしか鍵が無いサイト(chomoand-2.com等)を黙ってスキップしてしまう(2026-11-12 Snow Man ID626で発覚)
DRIVE_ENV = Path(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"))


def load_env():
    env = {}
    for p in (ROOT / ".env", DRIVE_ENV):
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"\'')
            if v and not env.get(k):
                env[k] = v
    env.update({k: v for k, v in os.environ.items() if k.startswith("WP_")})
    return env


def sites(env, only=None):
    out = []
    for k, url in env.items():
        m = re.fullmatch(r"WP_([A-Z0-9]+)_URL", k)
        if not m or not url:
            continue
        name = m.group(1)
        if only and name != only:
            continue
        user, pw = env.get(f"WP_{name}_USERNAME"), env.get(f"WP_{name}_APP_PASSWORD")
        if not user or not pw:
            continue
        auth = base64.b64encode(f"{user}:{pw}".encode()).decode()
        out.append((name, url.rstrip("/"), {"Authorization": f"Basic {auth}"}))
    return out


def embed_block(vid):
    url = f"https://www.youtube.com/watch?v={vid}"
    return (
        f'<!-- wp:embed {{"url":"{url}","type":"video","providerNameSlug":"youtube","responsive":true,'
        f'"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->\n'
        f'<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube '
        f'wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\n{url}\n'
        f"</div></figure>\n<!-- /wp:embed -->"
    )


def fix_html(raw):
    """(新しいHTML, 直した件数) を返す。直す所が無ければ件数0。"""
    n1 = 0

    def to_embed(m):
        nonlocal n1
        if "referrerpolicy" in m.group(0).lower():  # already playable; leave as is
            return m.group(0)
        n1 += 1
        return embed_block(m.group(1))

    new = WRAPPED_RE.sub(to_embed, raw)

    n2 = 0

    def add_refpol(m):
        nonlocal n2
        tag = m.group(0)
        if "referrerpolicy" in tag.lower():
            return tag
        n2 += 1
        return re.sub(r"^<iframe\b", f"<iframe {REFPOL}", tag, flags=re.I)

    new = IFRAME_RE.sub(add_refpol, new)
    return new, n1 + n2


def fetch_posts(base, headers, ids=None, recent_minutes=None):
    if ids:
        for pid in ids:
            r = requests.get(f"{base}/wp-json/wp/v2/posts/{pid}", headers=headers,
                             params={"context": "edit"}, timeout=30)
            r.raise_for_status()
            yield r.json()
        return
    cutoff = None
    if recent_minutes:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=recent_minutes)
    page = 1
    while True:
        params = {"context": "edit", "status": STATUSES, "per_page": 100 if not cutoff else 30,
                  "page": page, "orderby": "modified", "order": "desc",
                  "_fields": "id,status,title,content,modified_gmt"}
        r = requests.get(f"{base}/wp-json/wp/v2/posts", headers=headers, params=params, timeout=60)
        if r.status_code == 400:  # ページ範囲外
            return
        r.raise_for_status()
        js = r.json()
        if not js:
            return
        for p in js:
            if cutoff:
                mod = datetime.fromisoformat(p["modified_gmt"]).replace(tzinfo=timezone.utc)
                if mod < cutoff:
                    return
            yield p
        page += 1


def run(args):
    env = load_env()
    results = []
    for name, base, headers in sites(env, args.site):
        try:
            for p in fetch_posts(base, headers, args.ids, args.recent_minutes):
                raw = p["content"]["raw"]
                new, n = fix_html(raw)
                if not n:
                    continue
                pid = p["id"]
                label = f"{name}:{pid}({p.get('status')})"
                if args.dry:
                    results.append(f"{label} 要修正{n}件")
                    continue
                BACKUP_DIR.mkdir(parents=True, exist_ok=True)
                stamp = datetime.now().strftime("%Y%m%d%H%M%S")
                (BACKUP_DIR / f"{name}_{pid}_{stamp}.html").write_text(raw, encoding="utf-8")
                r = requests.post(f"{base}/wp-json/wp/v2/posts/{pid}",
                                  headers={**headers, "Content-Type": "application/json"},
                                  json={"content": new}, timeout=60)
                r.raise_for_status()
                rend = r.json()["content"]["rendered"]
                bad = [t for t in IFRAME_RE.findall(rend) if "referrerpolicy" not in t.lower()]
                results.append(f"{label} 修正{n}件" + (" ※まだreferrerpolicy無しが残る" if bad else ""))
        except requests.RequestException as e:
            results.append(f"{name}: 取得/更新エラー {e}")
    return results


def hook_main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    cmd = (data.get("tool_input") or {}).get("command", "")
    if not HOOK_CMD_RE.search(cmd) or "fix_youtube_embeds" in cmd:
        return 0
    args = argparse.Namespace(site=None, ids=None, recent_minutes=30, dry=False)
    try:
        results = run(args)
    except Exception as e:  # フックで作業を止めない
        results = [f"fix_youtube_embeds フックでエラー: {e}"]
    if results:
        msg = "YouTube埋め込みの再生エラー対策(referrerpolicy)を自動適用しました: " + ", ".join(results)
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                 "additionalContext": msg}}, ensure_ascii=False))
    return 0


def main():
    if "--hook" in sys.argv:
        return hook_main()
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", help="WP_<NAME>_URL の NAME (例: KOIKEYS)")
    ap.add_argument("--ids", type=int, nargs="+")
    ap.add_argument("--recent-minutes", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    if not (args.ids or args.recent_minutes or args.all):
        ap.error("--ids / --recent-minutes / --all のどれかを指定")
    if args.ids and not args.site:
        ap.error("--ids には --site が必要")
    for line in run(args) or ["直す所なし"]:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
