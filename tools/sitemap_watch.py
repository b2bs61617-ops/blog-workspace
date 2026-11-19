"""Search Consoleのサイトマップ点検(週1回)。問題があるときだけ「AIまつ」LINEに知らせる。

サイトマップは1回登録すればGoogleが自分で読み直すので、毎日送り直す必要はない。
代わりにこのツールで「登録もれ・エラー・長く読みに来ていない」を見張る(2026-11-19〜)。

調べること(Search Consoleにある全サイト。新しいサイトを足せば自動で対象になる):
  1. サイトマップが1つも登録されていない → 登録もれ(--fixで自動送信)
  2. サイトマップのエラー・警告が1件以上
  3. Googleが最後に読んだ日が STALE_DAYS 日より前
  4. サイトの sitemap.xml が開けない(200以外)

鍵: .env の GOOGLE_INDEXING_CREDENTIALS_PATH(Indexing APIと同じサービスアカウント。全サイトでオーナー)
通知: tools/line_notify.py(LINE_CHANNEL_ACCESS_TOKEN)。何も問題がなければ送らない(無料枠の節約)。

実行:
  python tools/sitemap_watch.py            # 点検して、問題があればLINE
  python tools/sitemap_watch.py --dry-run  # LINEに送らず結果を表示
  python tools/sitemap_watch.py --fix      # 登録もれのサイトに https://<domain>/sitemap.xml を送ってから点検
定期実行: GEEKOMで tools/sitemap_watch_register_task.ps1 を1回実行(毎週月曜9:00)
"""
import argparse
import datetime
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))
import line_notify  # noqa: E402

API = "https://www.googleapis.com/webmasters/v3"
SCOPE = "https://www.googleapis.com/auth/webmasters"
STALE_DAYS = 10


def domain_of(site_url):
    """'sc-domain:chomoand.com' / 'https://chomoand-4.blog/' → 'chomoand.com' / 'chomoand-4.blog'"""
    if site_url.startswith("sc-domain:"):
        return site_url[len("sc-domain:"):]
    return urllib.parse.urlparse(site_url).netloc


def parse_time(s):
    if not s:
        return None
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def judge_site(sitemaps, now, sitemap_status=200, stale_days=STALE_DAYS):
    """1サイト分のサイトマップ情報から問題点の一覧(文字列)を返す純粋関数。空なら問題なし。"""
    problems = []
    if sitemap_status != 200:
        problems.append(f"sitemap.xmlが開けない(HTTP {sitemap_status})")
    if not sitemaps:
        problems.append("Search Consoleにサイトマップが未登録")
        return problems
    for m in sitemaps:
        name = m.get("path", "").rsplit("/", 1)[-1] or m.get("path", "")
        errors, warnings = int(m.get("errors", 0) or 0), int(m.get("warnings", 0) or 0)
        if errors or warnings:
            problems.append(f"{name}: エラー{errors}件・警告{warnings}件")
        downloaded = parse_time(m.get("lastDownloaded"))
        if downloaded is None:
            submitted = parse_time(m.get("lastSubmitted"))
            if submitted and (now - submitted).days > stale_days:
                problems.append(f"{name}: 送信から{(now - submitted).days}日たってもGoogleが読んでいない")
        elif (now - downloaded).days > stale_days:
            problems.append(f"{name}: Googleが{(now - downloaded).days}日読みに来ていない")
    return problems


def session(env):
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    path = env.get("GOOGLE_INDEXING_CREDENTIALS_PATH")
    if not path or not Path(path).exists():
        raise RuntimeError("GOOGLE_INDEXING_CREDENTIALS_PATH が.envに無いか、鍵ファイルが見つからないワン")
    creds = service_account.Credentials.from_service_account_file(path, scopes=[SCOPE])
    return AuthorizedSession(creds)


def q(s):
    return urllib.parse.quote(s, safe="")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="LINEに送らず表示だけ")
    ap.add_argument("--fix", action="store_true", help="未登録のサイトに sitemap.xml を送る")
    args = ap.parse_args()

    s = session(line_notify.load_env(ROOT / ".env"))
    now = datetime.datetime.now(datetime.timezone.utc)
    sites = s.get(f"{API}/sites", timeout=30).json().get("siteEntry", [])
    report, fixed = [], []
    for e in sorted(sites, key=lambda x: domain_of(x["siteUrl"])):
        site, domain = e["siteUrl"], domain_of(e["siteUrl"])
        sitemap_url = f"https://{domain}/sitemap.xml"
        try:
            status = s.get(sitemap_url, timeout=30).status_code
        except Exception:
            status = 0
        maps = s.get(f"{API}/sites/{q(site)}/sitemaps", timeout=30).json().get("sitemap", [])
        if not maps and args.fix and status == 200:
            r = s.put(f"{API}/sites/{q(site)}/sitemaps/{q(sitemap_url)}", timeout=30)
            if r.status_code in (200, 204):
                fixed.append(domain)
                maps = s.get(f"{API}/sites/{q(site)}/sitemaps", timeout=30).json().get("sitemap", [])
        problems = judge_site(maps, now, status)
        print(f"{domain}: {'OK' if not problems else ' / '.join(problems)}")
        if problems:
            report.append(f"■ {domain}\n" + "\n".join("・" + p for p in problems))

    if fixed:
        report.append("サイトマップを送ったワン: " + "、".join(fixed))
    if not report:
        print("全サイト問題なしワン(LINEは送らない)")
        return
    text = "🗺 サイトマップ点検(Search Console)\n\n" + "\n\n".join(report) + "\n\nマツに「サイトマップ直して」と言ってワン"
    if args.dry_run:
        print("\n--- LINE(dry-run) ---\n" + text)
    else:
        line_notify.notify(text)
        print("LINEに送ったワン")


if __name__ == "__main__":
    main()
