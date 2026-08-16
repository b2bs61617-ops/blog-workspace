"""Google Search Console API(URL Inspection)でインデックス未登録URLを一括チェックするスクリプト。

Search Console管理画面の「ページがインデックスに登録されなかった理由」レポートは
一括エクスポートAPIが無いため、代わりにサイトマップからURL一覧を集め、
1件ずつURL Inspection APIに問い合わせて coverageState(「クロール済み-インデックス未登録」等)を集計する。

事前準備: docs/google-indexing-setup.md で作成済みのサービスアカウント鍵をそのまま使う。
サービスアカウントは既に3サイトのSearch Consoleに「オーナー」登録済みなので、
Search Console API(searchconsole.googleapis.com)をGoogle Cloud Console側で有効化するだけでよい。

実行:
  python tools/check_search_console.py chomoand-1.com
  python tools/check_search_console.py chomoand-1.com --site-url "sc-domain:chomoand-1.com" --limit 50
"""
import argparse
import json
import sys
import time
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).parent.parent
WEBMASTERS_READONLY_SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
INSPECT_URL = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


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


def parse_sitemap_xml(xml_bytes):
    """サイトマップXML(1個分)から<loc>のURL一覧を返す純粋関数。

    <sitemapindex>(子サイトマップへのリンク集)なら子サイトマップのURL一覧を、
    <urlset>(実際のページ一覧)ならページURL一覧を返す。どちらか呼び出し側で判別する。
    """
    root = ElementTree.fromstring(xml_bytes)
    tag = root.tag.replace(SITEMAP_NS, "")
    locs = []
    if tag == "sitemapindex":
        for sitemap in root.findall(f"{SITEMAP_NS}sitemap"):
            loc = sitemap.find(f"{SITEMAP_NS}loc")
            if loc is not None and loc.text:
                locs.append(loc.text.strip())
    elif tag == "urlset":
        for url in root.findall(f"{SITEMAP_NS}url"):
            loc = url.find(f"{SITEMAP_NS}loc")
            if loc is not None and loc.text:
                locs.append(loc.text.strip())
    return tag, locs


def fetch_post_urls(sitemap_index_url, include_pattern="post-sitemap", timeout=15):
    """サイトマップインデックスを辿って記事URL一覧を集める。

    include_patternに一致する子サイトマップだけ展開する(category/author/page等のノイズを除外)。
    """
    import requests

    resp = requests.get(sitemap_index_url, timeout=timeout)
    resp.raise_for_status()
    tag, locs = parse_sitemap_xml(resp.content)

    if tag == "urlset":
        return locs

    urls = []
    for child_sitemap_url in locs:
        if include_pattern and include_pattern not in child_sitemap_url:
            continue
        child_resp = requests.get(child_sitemap_url, timeout=timeout)
        child_resp.raise_for_status()
        _, child_locs = parse_sitemap_xml(child_resp.content)
        urls.extend(child_locs)
    return urls


def inspect_url(session, inspection_url, site_url):
    resp = session.post(
        INSPECT_URL,
        json={"inspectionUrl": inspection_url, "siteUrl": site_url},
    )
    if resp.status_code == 429:
        time.sleep(5)
        resp = session.post(
            INSPECT_URL,
            json={"inspectionUrl": inspection_url, "siteUrl": site_url},
        )
    resp.raise_for_status()
    return resp.json()


def build_session(credentials_path):
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession

    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=[WEBMASTERS_READONLY_SCOPE]
    )
    return AuthorizedSession(creds)


def main():
    parser = argparse.ArgumentParser(description="Search Console URL Inspection APIで未インデックスURLを調べる")
    parser.add_argument("domain", help="例: chomoand-1.com")
    parser.add_argument("--site-url", default=None, help='Search Console上のプロパティ指定。省略時は "https://<domain>/"')
    parser.add_argument("--sitemap-index", default=None, help="省略時は https://<domain>/sitemap_index.xml")
    parser.add_argument("--limit", type=int, default=None, help="チェックするURL数の上限(未指定なら全件)")
    parser.add_argument("--delay", type=float, default=1.0, help="APIリクエスト間隔(秒、デフォルト1秒)")
    parser.add_argument("--output", default=None, help="詳細結果を書き出すJSONファイルパス")
    args = parser.parse_args()

    env = load_env(ROOT / ".env")
    credentials_path = env.get("GOOGLE_INDEXING_CREDENTIALS_PATH")
    if not credentials_path:
        print("エラー: .envにGOOGLE_INDEXING_CREDENTIALS_PATHが未設定のワン。docs/google-indexing-setup.md参照ワン。")
        sys.exit(1)
    if not Path(credentials_path).exists():
        print(f"エラー: 鍵ファイルが見つからないワン: {credentials_path}")
        sys.exit(1)

    site_url = args.site_url or f"https://{args.domain}/"
    sitemap_index = args.sitemap_index or f"https://{args.domain}/sitemap_index.xml"

    print(f"サイトマップからURL一覧を取得中... ({sitemap_index})")
    urls = fetch_post_urls(sitemap_index)
    if args.limit:
        urls = urls[: args.limit]
    print(f"{len(urls)}件のURLをチェックするワン")

    session = build_session(credentials_path)
    results = []
    by_state = {}
    for i, url in enumerate(urls, 1):
        try:
            data = inspect_url(session, url, site_url)
        except Exception as e:
            print(f"[{i}/{len(urls)}] ERROR {url}: {e}")
            continue

        index_result = data.get("inspectionResult", {}).get("indexStatusResult", {})
        coverage_state = index_result.get("coverageState", "UNKNOWN")
        results.append(
            {
                "url": url,
                "coverageState": coverage_state,
                "verdict": index_result.get("verdict"),
                "lastCrawlTime": index_result.get("lastCrawlTime"),
                "pageFetchState": index_result.get("pageFetchState"),
                "robotsTxtState": index_result.get("robotsTxtState"),
            }
        )
        by_state.setdefault(coverage_state, []).append(url)
        print(f"[{i}/{len(urls)}] {coverage_state}: {url}")
        time.sleep(args.delay)

    print("\n=== 集計 ===")
    for state, state_urls in sorted(by_state.items(), key=lambda kv: -len(kv[1])):
        print(f"{state}: {len(state_urls)}件")

    if args.output:
        Path(args.output).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n詳細を書き出したワン: {args.output}")


if __name__ == "__main__":
    main()
