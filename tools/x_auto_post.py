"""記事公開時にXへ自動投稿するスクリプト(2026-08-09〜、Zapierから自前実装へ置き換え)。

Zapierの「Create Tweet」はリプライスレッドを作れず、本文にURLを含めると
Xのアルゴリズム上リーチが大きく落ちる(2026年のアルゴリズム変更でURL付き投稿は
リーチ30〜50%減、リンクのみの投稿は最大40%減という調査結果あり)。
そのため本スクリプトは「1件目=画像+フック文+ハッシュタグ(URL無し)」
「2件目=1件目へのリプライとしてURLのみ」の2連投で投稿する。

事前準備(初回のみ、トモキ本人が実施): docs/x-auto-post-setup.md 参照。
サイトごとに別のXアカウントを想定し、.envに X_TREND_*/X_AUDITION_*/X_KOIKEYS_* を設定する。

実行:
  python tools/x_auto_post.py --site trend \
    --text "今日好き夏休み編2024新メンバープロフィール!" \
    --hashtags "#今日好き #今日好きになりました" \
    --image "https://chomoand.com/wp-content/uploads/xxxx.jpg" \
    --url "https://chomoand.com/?p=1234"

他のスクリプト(publishスキル)から使う場合:
  from tools.x_auto_post import post_thread
  post_thread(site="trend", hook_text="...", hashtags="#a #b", image_url="...", article_url="...")
"""
import argparse
import json
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent

SITE_ENV_PREFIX = {
    "trend": "X_TREND",       # chomoand.com
    "audition": "X_AUDITION", # chomoand-0.com
    "koikeys": "X_KOIKEYS",   # chomoand-1.com
}


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


def get_site_credentials(site, env):
    """サイトキー(trend/audition/koikeys)からX API認証情報を取り出す。
    どれか1つでも未設定ならNoneを返す(呼び出し側でスキップ判定に使う)。
    """
    prefix = SITE_ENV_PREFIX.get(site)
    if prefix is None:
        raise ValueError(f"不明なsite指定: {site}(trend/audition/koikeysのいずれか)")

    keys = {
        "api_key": env.get(f"{prefix}_API_KEY"),
        "api_secret": env.get(f"{prefix}_API_SECRET"),
        "access_token": env.get(f"{prefix}_ACCESS_TOKEN"),
        "access_token_secret": env.get(f"{prefix}_ACCESS_TOKEN_SECRET"),
    }
    if not all(keys.values()):
        return None
    return keys


def weighted_length(text):
    """Xの文字数カウントの簡易近似。ASCII文字は重み1、それ以外(日本語・絵文字等)は重み2。
    (公式のtwitter-text仕様の厳密な範囲表とは完全一致しないが、日本語オンリー文章の
    実質上限が140文字相当になる挙動を再現するには十分な精度)
    """
    return sum(1 if ord(c) < 0x80 else 2 for c in text)


def truncate_to_weight(text, max_weight):
    """weighted_lengthがmax_weight以下になるまで末尾から削る。"""
    if weighted_length(text) <= max_weight:
        return text
    result = []
    total = 0
    for c in text:
        w = 1 if ord(c) < 0x80 else 2
        if total + w > max_weight:
            break
        result.append(c)
        total += w
    return "".join(result)


def compose_tweet_text(hook_text, hashtags, max_weight=280):
    """フック文とハッシュタグを結合し、Xの文字数上限(重み280)に収める。
    ハッシュタグは削らず、フック文側を必要に応じて末尾から短縮する。
    """
    hashtags = (hashtags or "").strip()
    hook_text = (hook_text or "").strip()

    if not hashtags:
        return truncate_to_weight(hook_text, max_weight)

    separator = "\n\n"
    reserved = weighted_length(separator) + weighted_length(hashtags)
    hook_budget = max_weight - reserved

    if hook_budget <= 0:
        # ハッシュタグだけで埋まる極端なケース。ハッシュタグ側を削る。
        return truncate_to_weight(hashtags, max_weight)

    hook_text = truncate_to_weight(hook_text, hook_budget)
    return f"{hook_text}{separator}{hashtags}"


def download_to_tempfile(url):
    suffix = Path(url.split("?")[0]).suffix or ".jpg"
    fd, path = tempfile.mkstemp(suffix=suffix)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r, open(fd, "wb") as f:
        f.write(r.read())
    return path


def post_thread(site, hook_text, hashtags, image_url, article_url):
    """1件目(画像+フック文+タグ、URL無し)→2件目(1件目へのリプライでURLのみ)の順に投稿する。
    .envにそのサイトのX認証情報が無ければ何もせずNoneを返す(公開処理は止めない)。
    """
    env = load_env(ROOT / ".env")
    creds = get_site_credentials(site, env)
    if creds is None:
        prefix = SITE_ENV_PREFIX.get(site, site)
        print(f"{prefix}_* が.envに未設定のためXへの自動投稿をスキップしたワン")
        return None

    import tweepy

    auth = tweepy.OAuth1UserHandler(
        creds["api_key"], creds["api_secret"],
        creds["access_token"], creds["access_token_secret"],
    )
    api_v1 = tweepy.API(auth)
    client = tweepy.Client(
        consumer_key=creds["api_key"], consumer_secret=creds["api_secret"],
        access_token=creds["access_token"], access_token_secret=creds["access_token_secret"],
    )

    image_path = download_to_tempfile(image_url)
    try:
        media = api_v1.media_upload(filename=image_path)
    finally:
        Path(image_path).unlink(missing_ok=True)

    text = compose_tweet_text(hook_text, hashtags)
    main_resp = client.create_tweet(text=text, media_ids=[media.media_id])
    main_id = main_resp.data["id"]

    reply_resp = client.create_tweet(text=article_url, in_reply_to_tweet_id=main_id)
    reply_id = reply_resp.data["id"]

    return {
        "main_tweet_id": main_id,
        "main_tweet_url": f"https://x.com/i/status/{main_id}",
        "reply_tweet_id": reply_id,
        "reply_tweet_url": f"https://x.com/i/status/{reply_id}",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, choices=list(SITE_ENV_PREFIX))
    parser.add_argument("--text", required=True, help="フック文(URL・ハッシュタグは含めない)")
    parser.add_argument("--hashtags", default="", help="例: '#今日好き #今日好きになりました'")
    parser.add_argument("--image", required=True, help="添付画像のURL")
    parser.add_argument("--url", required=True, help="記事URL(リプライ投稿に使う)")
    args = parser.parse_args()

    result = post_thread(args.site, args.text, args.hashtags, args.image, args.url)
    if result is None:
        sys.exit(0)
    print(json.dumps(result, ensure_ascii=False, indent=2))
