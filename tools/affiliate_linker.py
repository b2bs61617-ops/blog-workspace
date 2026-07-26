"""コイキーズ記事(chomoand-1.com)の商品(ブランド・小物など)に楽天/Amazonのアフィリエイトリンクを
提案するためのスクリプト。実際のリンク挿入・記事更新は行わず、候補を提示するだけ。
koikeyz-affiliateスキルから、記事本文中に見つけたブランド・商品名をキーワードとして呼び出す想定。

事前準備(初回のみ、.envに設定):
  RAKUTEN_APP_ID       楽天ウェブサービスで発行したアプリID (https://webservice.rakuten.co.jp/)
  RAKUTEN_AFFILIATE_ID 楽天アフィリエイトで発行したアフィリエイトID (https://affiliate.rakuten.co.jp/)
  AMAZON_ASSOCIATE_TAG Amazonアソシエイトのトラッキングタグ

実行:
  python tools/affiliate_linker.py "商品名やブランド名"
"""
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAKUTEN_ITEM_SEARCH_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
AMAZON_SEARCH_URL = "https://www.amazon.co.jp/s"


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


def build_amazon_search_url(keyword, tag):
    """Amazon検索結果ページへのアソシエイトタグ付きリンクを作る(PA-APIは使わない検索リンク方式)。"""
    params = {"k": keyword}
    if tag:
        params["tag"] = tag
    return f"{AMAZON_SEARCH_URL}?{urllib.parse.urlencode(params)}"


def parse_rakuten_items(raw_items):
    """楽天商品検索APIのItems配列を、記事提案用の簡易dictのリストに変換する。"""
    candidates = []
    for entry in raw_items:
        item = entry.get("Item", entry)
        image_urls = item.get("mediumImageUrls") or []
        image = None
        if image_urls:
            first = image_urls[0]
            image = first.get("imageUrl") if isinstance(first, dict) else first
        candidates.append({
            "name": item.get("itemName"),
            "price": item.get("itemPrice"),
            "shop": item.get("shopName"),
            "url": item.get("affiliateUrl") or item.get("itemUrl"),
            "image": image,
            "review_average": item.get("reviewAverage"),
            "review_count": item.get("reviewCount"),
        })
    return candidates


def fetch_rakuten_items(app_id, affiliate_id, keyword, hits=5):
    params = {
        "applicationId": app_id,
        "keyword": keyword,
        "hits": hits,
        "sort": "standard",
        "format": "json",
    }
    if affiliate_id:
        params["affiliateId"] = affiliate_id
    url = f"{RAKUTEN_ITEM_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=15) as r:
        data = json.loads(r.read())
    if "error" in data:
        raise RuntimeError(data.get("error_description", data["error"]))
    return parse_rakuten_items(data.get("Items", []))


def search_product(keyword, env=None):
    """楽天の商品候補(APIキー未設定ならスキップ)とAmazon検索リンクをまとめて返す。"""
    if env is None:
        env = load_env(ROOT / ".env")

    result = {"keyword": keyword, "rakuten": [], "amazon_search_url": None, "rakuten_error": None}

    app_id = env.get("RAKUTEN_APP_ID")
    affiliate_id = env.get("RAKUTEN_AFFILIATE_ID")
    if app_id:
        try:
            result["rakuten"] = fetch_rakuten_items(app_id, affiliate_id, keyword)
        except Exception as e:
            result["rakuten_error"] = str(e)
    else:
        result["rakuten_error"] = "RAKUTEN_APP_IDが.envに未設定のため楽天検索はスキップしたワン"

    tag = env.get("AMAZON_ASSOCIATE_TAG")
    result["amazon_search_url"] = build_amazon_search_url(keyword, tag)
    if not tag:
        result["amazon_tag_missing"] = True

    return result


def print_result(result):
    print(f"# 「{result['keyword']}」の候補\n")
    if result["rakuten"]:
        print("## 楽天")
        for i, c in enumerate(result["rakuten"], 1):
            price = f"{c['price']:,}円" if c.get("price") else "価格不明"
            print(f"{i}. {c['name']} — {price} ({c['shop']})")
            print(f"   {c['url']}")
    elif result.get("rakuten_error"):
        print(f"## 楽天: {result['rakuten_error']}")

    print("\n## Amazon(検索結果ページ)")
    print(f"   {result['amazon_search_url']}")
    if result.get("amazon_tag_missing"):
        print("   ※ AMAZON_ASSOCIATE_TAGが.envに未設定のためタグなしリンクワン")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python tools/affiliate_linker.py \"商品名やブランド名\"")
        sys.exit(1)
    keyword = sys.argv[1]
    print_result(search_product(keyword))
