"""24時間テレビ マラソン 現在地トラッカー(本体・1回実行)。

タスクスケジューラから 10 分おきに呼ばれる想定。
  1. 稼働時間帯(config: active_from〜active_until)外なら即終了
  2. 監視アカウントの最新ポストを取得
  3. 新着が無ければ記事を一切触らず終了
  4. 新着に位置情報があれば、記事のリアルタイム欄(マーカー領域)を再生成して
     status:publish のまま更新する

使い方:
  python tools/marathon-tracker/tracker.py            # 通常(実更新)
  python tools/marathon-tracker/tracker.py --dry-run  # 更新せず差分プレビューだけ
  python tools/marathon-tracker/tracker.py --reset-bootstrap
"""
import argparse
import asyncio
import json
import re
import sys
from datetime import datetime, timedelta, timezone

from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import article_updater as au  # noqa: E402
import llm_extract  # noqa: E402
import yt_chat_fetch  # noqa: E402

try:
    import x_fetch  # noqa: E402  (playwright 未インストールなら X ソースは無効)
except Exception as _x_imp_err:  # noqa: BLE001
    x_fetch = None
    _X_IMPORT_ERROR = _x_imp_err

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CONFIG_FILE = HERE / "config.json"
STATE_FILE = HERE / "state.json"
LOG_DIR = HERE / "logs"
JST = timezone(timedelta(hours=9))
MAX_ENTRIES = 120
MAX_SEEN = 2000


def log(msg):
    print(f"[{datetime.now(JST):%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_dt(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def is_noise(text, patterns):
    for p in patterns:
        try:
            if re.search(p, text):
                return True
        except re.error:
            if p in text:
                return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reset-bootstrap", action="store_true")
    ap.add_argument("--headful", action="store_true", help="ブラウザを表示して取得(デバッグ用)")
    args = ap.parse_args()

    cfg = load_json(CONFIG_FILE, {})
    state = load_json(STATE_FILE, {})
    state.setdefault("bootstrap_done", False)
    state.setdefault("seen_ids", [])
    state.setdefault("entries", [])
    state.setdefault("current_location", "")
    state.setdefault("last_wp_update", "")

    if args.reset_bootstrap:
        state["bootstrap_done"] = False
        save_state(state)
        log("bootstrap をリセットした。次回実行で既存ポストを既読化する。")
        return

    now = datetime.now(JST)
    af = parse_dt(cfg["active_from"])
    au_ = parse_dt(cfg["active_until"])
    if af and now < af:
        log(f"稼働開始前({cfg['active_from']})。終了。")
        return
    if au_ and now > au_:
        log(f"稼働終了({cfg['active_until']})を過ぎている。終了。")
        return

    posts = []

    # --- ソース1: YouTube ライブチャット(主軸) ---
    yt_url = (cfg.get("youtube_video_url") or "").strip()
    if cfg.get("youtube_enabled", True) and yt_url:
        try:
            yt_posts = yt_chat_fetch.fetch(
                yt_url,
                capture_seconds=int(cfg.get("yt_capture_seconds", 25)),
                limit=int(cfg.get("max_yt_messages", 250)),
            )
            log(f"YouTubeチャット取得 {len(yt_posts)} 件")
            posts.extend(yt_posts)
        except Exception as e:  # noqa: BLE001
            log(f"[warn] YouTubeチャット取得失敗: {e}")
    elif cfg.get("youtube_enabled", True):
        log("[warn] youtube_video_url 未設定(config.json)。YouTubeソースはスキップ。")

    # --- ソース2: X(補助・失敗しても続行) ---
    accounts = [a.lstrip("@").strip() for a in cfg.get("x_accounts", []) if a.strip()]
    fallback = cfg.get("x_search_fallback") or None
    if cfg.get("x_enabled", True) and x_fetch is None:
        log(f"[warn] X有効だが playwright 未インストールのためスキップ: {_X_IMPORT_ERROR}")
    if cfg.get("x_enabled", True) and x_fetch is not None and (accounts or fallback):
        log(f"X取得開始: accounts={accounts or '(なし)'} fallback={fallback if not accounts else '(未使用)'}")
        try:
            x_posts = asyncio.run(x_fetch.fetch(
                accounts, search_fallback=fallback,
                limit=int(cfg.get("max_tweets_per_account", 30)),
                headless=not args.headful,
            ))
            log(f"X取得 {len(x_posts)} 件")
            posts.extend(x_posts)
        except Exception as e:  # noqa: BLE001
            log(f"[warn] X取得失敗(Playwright/ログイン未設定?): {e}")

    log(f"取得合計 {len(posts)} 件")
    if not posts:
        log("どのソースからも取得できなかった(配信終了/ログイン切れ/一時的な失敗)。終了。")
        return

    seen = set(state["seen_ids"])

    # 初回: 既存を全部既読にするだけ。記事は触らない
    if not state["bootstrap_done"]:
        state["seen_ids"] = (list(seen | {p["id"] for p in posts}))[-MAX_SEEN:]
        state["bootstrap_done"] = True
        save_state(state)
        log(f"初回起動。既存 {len(posts)} 件を既読化した。次回から新着だけ反映する。")
        return

    lookback = int(cfg.get("first_run_lookback_minutes", 0))
    floor_dt = af if af else (now - timedelta(hours=24))
    if lookback:
        floor_dt = min(floor_dt, now - timedelta(minutes=lookback))

    noise = cfg.get("noise_patterns", [])
    new = []
    for p in posts:
        if p["id"] in seen:
            continue
        if is_noise(p.get("text", ""), noise):
            continue
        dt = parse_dt(p.get("date", ""))
        if dt and dt < floor_dt:
            continue
        new.append(p)

    if not new:
        log("新着なし。記事は触らず終了。")
        # 取得できたIDは既読に足しておく(ノイズ含む)
        state["seen_ids"] = (list(seen | {p["id"] for p in posts}))[-MAX_SEEN:]
        save_state(state)
        return

    new.sort(key=lambda x: (parse_dt(x.get("date", "")) or now))
    log(f"新着 {len(new)} 件を LLM で判定")

    # 連続更新の抑制
    last_up = parse_dt(state.get("last_wp_update", ""))
    min_gap = int(cfg.get("min_minutes_between_wp_updates", 8))
    throttled = bool(last_up and (now - last_up) < timedelta(minutes=min_gap))

    try:
        result = llm_extract.extract(
            cfg.get("runner_name", ""),
            cfg.get("course_context", ""),
            new,
            last_location=state.get("current_location", ""),
            primary=cfg.get("llm_primary", "claude"),
            gemini_model=cfg.get("llm_model_gemini", "gemini-flash-latest"),
        )
    except Exception as e:  # noqa: BLE001
        log(f"[ERROR] LLM抽出に失敗: {e}  (既読にせず次回リトライ)")
        return

    log(f"LLM判定: update={result['update']} reason={result.get('reason','')[:120]}")

    if not result["update"] or not result["entries"]:
        state["seen_ids"] = (list(seen | {p["id"] for p in posts}))[-MAX_SEEN:]
        save_state(state)
        log("位置情報なしと判定。記事は触らず終了。")
        return

    if throttled and not args.dry_run:
        log(f"前回更新から {min_gap} 分未満。今回はスキップ(次回反映)。")
        return

    # エントリを蓄積(新しい順)。time+text で重複排除
    existing_keys = {(e.get("time", ""), e.get("text", "")) for e in state["entries"]}
    added = 0
    for e in reversed(result["entries"]):  # LLM出力は新しい順想定。古い方から prepend
        key = (e.get("time", ""), e.get("text", ""))
        if key in existing_keys:
            continue
        state["entries"].insert(0, {
            "time": e.get("time", ""), "text": e.get("text", ""),
            "map_query": e.get("map_query", ""),
        })
        existing_keys.add(key)
        added += 1
    state["entries"] = state["entries"][:MAX_ENTRIES]
    if result.get("current_location"):
        state["current_location"] = result["current_location"]
    log(f"追記エントリ {added} 件 / 累計 {len(state['entries'])} 件 / 現在地='{state['current_location']}'")

    region = au.render_region(
        state["current_location"], state["entries"],
        updated_at=now.strftime("%m/%d %H:%M") + " JST",
        map_zoom=int(cfg.get("map_zoom", 15)),
    )

    try:
        post = au.get_post(cfg)
    except Exception as e:  # noqa: BLE001
        log(f"[ERROR] 記事取得に失敗: {e}")
        return

    try:
        new_content = au.splice(
            post["content"], region,
            cfg.get("section_heading_contains", "リアルタイム情報"),
            cfg.get("next_heading_contains", "ゴール予想時刻"),
        )
    except Exception as e:  # noqa: BLE001
        log(f"[ERROR] セクション差し込みに失敗(記事構造が変わった?): {e}")
        return

    LOG_DIR.mkdir(exist_ok=True)
    if args.dry_run:
        prev = LOG_DIR / f"preview_{now:%Y%m%d_%H%M%S}.html"
        prev.write_text(new_content, encoding="utf-8")
        log(f"[DRY-RUN] 更新せず。プレビュー: {prev}")
        print("\n----- 差し替わるマーカー領域 -----\n")
        print(au.region_of(new_content))
        return

    bpath = au.backup(cfg, post["content"])
    log(f"旧本文を退避: {bpath}")
    try:
        status = au.put_post(cfg, new_content)
    except Exception as e:  # noqa: BLE001
        log(f"[ERROR] 記事更新に失敗: {e}")
        return

    if status != "publish":
        log(f"[WARN] 更新後の status が '{status}' になっている。手動で公開へ戻してワン。")
    else:
        log("記事を更新(status: publish 維持)")

    state["seen_ids"] = (list(seen | {p["id"] for p in posts}))[-MAX_SEEN:]
    state["last_wp_update"] = now.isoformat()
    save_state(state)
    log(f"完了。現在地='{state['current_location']}' 反映エントリ累計 {len(state['entries'])}")


if __name__ == "__main__":
    main()
