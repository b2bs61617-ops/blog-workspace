"""記事公開時にXへ自動投稿するスクリプト(Buffer経由、2026-09-23〜)。

旧`tools/x_auto_post.py`はX API直接利用(2026年にPay-Per-Use化、URL付き投稿$0.20/件)の
コスト問題とブラウザ自動化の凍結リスクを理由に、2026-08-09からXは意図的に手動投稿にしていた
(経緯はdocs/x-auto-post-setup.md参照)。Bufferは公式にXとAPI連携済みのサービスで、投稿は
Buffer側の定額プラン内で行われるため従量課金が発生しない。全サイト(chomoand-4.blogのトラジャ含む)とも@chomoand17を共通で
使っているため、旧スクリプトと違いサイト別の認証情報は不要(Bufferのチャンネルは1つ)。

投稿の型は旧スクリプトと同じ: 「1件目=画像+フック文+ハッシュタグ(URL無し)」
「2件目=1件目へのリプライとしてURLのみ」の2連投(Xのスレッド機能で実現)。

事前準備(初回のみ、トモキ本人が実施):
  1. buffer.comで@chomoand17を接続
  2. developers.buffer.comでAPIキー(Personal Access Key)を発行
  3. .envに BUFFER_ACCESS_TOKEN / BUFFER_X_CHANNEL_ID を設定

実行:
  python tools/x_auto_post_buffer.py \
    --text "今日好き夏休み編2024新メンバープロフィール!" \
    --hashtags "#今日好き #今日好きになりました" \
    --image "https://chomoand.com/wp-content/uploads/xxxx.jpg" \
    --url "https://chomoand.com/?p=1234"

他のスクリプト(publishスキル)から使う場合:
  from tools.x_auto_post_buffer import post_thread
  post_thread(hook_text="...", hashtags="#a #b", image_url="...", article_url="...")
"""
import argparse
import json
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).parent.parent
BUFFER_API_URL = "https://api.buffer.com"


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


def weighted_length(text):
    """Xの文字数カウントの簡易近似。ASCII文字は重み1、それ以外(日本語・絵文字等)は重み2。"""
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
    """フック文とハッシュタグを結合し、Xの文字数上限(重み280)に収める。"""
    hashtags = (hashtags or "").strip()
    hook_text = (hook_text or "").strip()

    if not hashtags:
        return truncate_to_weight(hook_text, max_weight)

    separator = "\n\n"
    reserved = weighted_length(separator) + weighted_length(hashtags)
    hook_budget = max_weight - reserved

    if hook_budget <= 0:
        return truncate_to_weight(hashtags, max_weight)

    hook_text = truncate_to_weight(hook_text, hook_budget)
    return f"{hook_text}{separator}{hashtags}"


def _gql_string(value):
    """GraphQLクエリに埋め込む文字列リテラルをエスケープする。"""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def post_thread(hook_text, hashtags, image_url, article_url, due_at=None):
    """1件目(画像+フック文+タグ、URL無し)→2件目(1件目へのリプライでURLのみ)の
    スレッドをBuffer経由でXへ投稿する。due_at(ISO8601、例"2026-09-25T21:00:00+09:00")を
    渡すとその時刻に予約投稿、省略すると即時投稿。一括公開時の連投回避に使う(2026-09-25〜)。
    .envにBUFFER_ACCESS_TOKEN/BUFFER_X_CHANNEL_IDが無ければ何もせずNoneを返す
    (公開処理は止めない。Google Indexing/Naver IndexNowと同じフェイルセーフ方式)。
    """
    env = load_env(ROOT / ".env")
    token = env.get("BUFFER_ACCESS_TOKEN")
    channel_id = env.get("BUFFER_X_CHANNEL_ID")
    if not token or not channel_id:
        print("BUFFER_ACCESS_TOKEN/BUFFER_X_CHANNEL_IDが.envに未設定のためXへの自動投稿をスキップしたワン")
        return None

    text = compose_tweet_text(hook_text, hashtags)
    mode = f"mode: customScheduled\n        dueAt: {_gql_string(due_at)}" if due_at else "mode: shareNow"

    query = f"""
    mutation {{
      createPost(input: {{
        text: {_gql_string(text)}
        channelId: {_gql_string(channel_id)}
        schedulingType: automatic
        {mode}
        assets: [{{ image: {{ url: {_gql_string(image_url)} }} }}]
        metadata: {{
          twitter: {{
            thread: [
              {{ text: {_gql_string(text)}, assets: [{{ image: {{ url: {_gql_string(image_url)} }} }}] }}
              {{ text: {_gql_string(article_url)} }}
            ]
          }}
        }}
      }}) {{
        ... on PostActionSuccess {{
          post {{ id status dueAt externalLink }}
        }}
        ... on MutationError {{
          message
        }}
      }}
    }}
    """

    resp = requests.post(
        BUFFER_API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        json={"query": query},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    if "errors" in data:
        raise RuntimeError(f"Buffer API error: {data['errors']}")

    result = data["data"]["createPost"]
    if "message" in result:
        raise RuntimeError(f"Buffer投稿失敗: {result['message']}")

    post = result["post"]
    return {
        "post_id": post["id"],
        "status": post["status"],
        "due_at": post.get("dueAt"),
        "tweet_url": post.get("externalLink"),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="フック文(URL・ハッシュタグは含めない)")
    parser.add_argument("--hashtags", default="", help="例: '#今日好き #今日好きになりました'")
    parser.add_argument("--image", required=True, help="添付画像のURL(公開アクセス可能なもの)")
    parser.add_argument("--url", required=True, help="記事URL(リプライ投稿に使う)")
    parser.add_argument("--due-at", default=None, help="予約投稿時刻(ISO8601、例: 2026-09-25T21:00:00+09:00)。省略時は即時投稿")
    args = parser.parse_args()

    result = post_thread(args.text, args.hashtags, args.image, args.url, due_at=args.due_at)
    if result is None:
        sys.exit(0)
    print(json.dumps(result, ensure_ascii=False, indent=2))
