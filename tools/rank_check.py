"""指定キーワードでの検索結果順位を実際にブラウザで検索して確認するツール。

Search Console API(searchAnalytics.query)は「Googleが記録した実績」しか見えず、
公開直後の記事や超ロングテールなキーワードだと反映まで数日ラグがある。
このツールは実際にPlaywrightでブラウザを起動し、指定キーワードで検索して
「今何位に出ているか」をその場で確認する。

**Yahoo!検索のみ対応。Googleは自動アクセス検知(CAPTCHA)でブロックされるため非対応**
(2026-09-22確認: ヘッドレスChromeでgoogle.com/searchへアクセス直後に
/sorry/index へリダイレクトされる。突破にはブラウザ偽装等の
ボット対策回避が必要になるためやらない判断)。
Googleの順位を知りたい場合は Search Console API(check_search_console.py 相当。
現状は searchAnalytics.query 用の専用スクリプトは無いのでその場でAPI呼び出しする)か、
トモキ本人によるシークレットウィンドウでの目視確認に頼る。

実行:
  python tools/rank_check.py "トークィーンズ Travis Japan 恋愛観" chomoand-4.blog
  python tools/rank_check.py "Travis Japan 八ヶ岳 ロケ地" chomoand-4.blog --num 30
"""
import argparse
import json
from urllib.parse import quote

from playwright.sync_api import sync_playwright

YAHOO_RESULT_LINK_SELECTOR = "div.sw-CardBase a[href^='http'], .Algo a[href^='http'], a.C_qh6[href^='http']"


def find_rank(urls, target_domain):
    """重複除去済みURLリストの中から、target_domainが最初に登場する順位(1始まり)を返す純粋関数。

    見つからなければ(None, None)。
    """
    seen = []
    for href in urls:
        if href not in seen:
            seen.append(href)
    for i, href in enumerate(seen, 1):
        if target_domain in href:
            return i, href
    return None, None


def dedupe_urls(urls, exclude_substrings=()):
    """検索結果リンクからノイズ(検索エンジン自身へのリンク等)を除いて重複除去する純粋関数。"""
    seen = []
    for href in urls:
        if any(s in href for s in exclude_substrings):
            continue
        if href not in seen:
            seen.append(href)
    return seen


def check_yahoo_rank(keyword, target_domain, num=20, headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=headless)
        try:
            context = browser.new_context(
                locale="ja-JP",
                viewport={"width": 1280, "height": 1600},
            )
            page = context.new_page()
            q = quote(keyword)
            page.goto(f"https://search.yahoo.co.jp/search?p={q}", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(1500)

            raw_links = page.eval_on_selector_all(
                YAHOO_RESULT_LINK_SELECTOR, "els => els.map(e => e.href)"
            )
            urls = dedupe_urls(raw_links, exclude_substrings=["search.yahoo.co.jp/"])[:num]
            rank, matched_url = find_rank(urls, target_domain)

            return {
                "engine": "yahoo",
                "keyword": keyword,
                "target_domain": target_domain,
                "rank": rank,
                "matched_url": matched_url,
                "top_results": [{"rank": i, "url": u} for i, u in enumerate(urls, 1)],
            }
        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser(description="Yahoo!検索で指定キーワードの検索結果順位を確認する")
    parser.add_argument("keyword", help='検索キーワード(例: "トークィーンズ Travis Japan 恋愛観")')
    parser.add_argument("domain", help="順位を調べたいサイトのドメイン(例: chomoand-4.blog)")
    parser.add_argument("--num", type=int, default=20, help="確認する検索結果の件数(デフォルト20)")
    parser.add_argument("--show", action="store_true", help="ブラウザ画面を表示して実行(デバッグ用)")
    args = parser.parse_args()

    result = check_yahoo_rank(args.keyword, args.domain, num=args.num, headless=not args.show)

    if result["rank"]:
        print(f"「{args.keyword}」で {args.domain} は {result['rank']}位 ({result['matched_url']})")
    else:
        print(f"「{args.keyword}」の上位{args.num}件に {args.domain} は見つからなかったワン")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
