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
import screen_map_fetch  # noqa: E402
import share_map_fetch  # noqa: E402
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
LOCK_FILE = HERE / "tracker.lock"
LOG_DIR = HERE / "logs"
JST = timezone(timedelta(hours=9))
MAX_ENTRIES = 120
MAX_SEEN = 2000
LOCK_STALE_MINUTES = 12


def log(msg):
    print(f"[{datetime.now(JST):%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


def acquire_lock():
    """多重起動防止。手動実行とタスクの同時実行で state.json が競合するのを防ぐ。
    戻り値 True で取得成功。古いロック(> LOCK_STALE_MINUTES 分)は奪う。"""
    import os
    import time

    if LOCK_FILE.exists():
        try:
            age_min = (time.time() - LOCK_FILE.stat().st_mtime) / 60
        except Exception:
            age_min = 999
        if age_min < LOCK_STALE_MINUTES:
            return False
        # 古いロックは残骸とみなして削除
        try:
            LOCK_FILE.unlink()
        except Exception:
            pass
    try:
        LOCK_FILE.write_text(f"{os.getpid()} {datetime.now(JST).isoformat()}", encoding="utf-8")
        return True
    except Exception:
        return False


def release_lock():
    try:
        LOCK_FILE.unlink()
    except Exception:
        pass


def ping_search_console(cfg, post):
    """記事更新後、Google Indexing API に URL_UPDATED を通知(ベストエフォート)。
    .env の GOOGLE_INDEXING_CREDENTIALS_PATH 未設定/失敗でも処理は止めない。"""
    if not cfg.get("search_console_ping", False):
        return
    url = (cfg.get("article_url") or (post or {}).get("link") or "").strip()
    if not url:
        log("[warn] インデックス通知: 記事URLが不明。スキップ。")
        return
    try:
        import importlib
        gi = importlib.import_module("tools.google_indexing")
    except Exception:
        try:
            sys.path.insert(0, str(HERE.parent))  # .../tools
            import google_indexing as gi  # type: ignore
        except Exception as e:  # noqa: BLE001
            log(f"[warn] インデックス通知: google_indexing を読めない: {e}")
            return
    try:
        res = gi.notify(url)
        if res is not None:
            log(f"インデックス登録をリクエスト: {url}")
    except Exception as e:  # noqa: BLE001
        log(f"[warn] インデックス通知に失敗(処理は継続): {e}")


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
    ap.add_argument("--force", action="store_true",
                    help="現在地が同じでも/前回更新直後でも、今の内容で記事を描き直す(レイアウト変更の反映用)")
    args = ap.parse_args()

    if not args.dry_run:
        if not acquire_lock():
            log(f"別の実行が進行中(または {LOCK_STALE_MINUTES} 分以内のロックあり)。今回はスキップ。")
            return
        import atexit
        atexit.register(release_lock)

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

    _heading = cfg.get("realtime_heading") or "星野真里は今どこ？（リアルタイム更新）"

    # --force: 取得もLLMもせず、今の state の内容で記事を描き直す(レイアウト変更の反映用)
    if args.force:
        if not state.get("entries"):
            log("--force: state に entries が無い。先に通常実行で1回更新してワン。")
            return
        region = au.render_region(
            state.get("current_location", ""), state["entries"],
            updated_at=now.strftime("%m/%d %H:%M") + " JST",
            map_zoom=int(cfg.get("map_zoom", 15)), heading=_heading,
        )
        try:
            post = au.get_post(cfg)
            new_content = au.splice(post["content"], region)
        except Exception as e:  # noqa: BLE001
            log(f"[ERROR] --force 描き直しに失敗: {e}")
            return
        if args.dry_run:
            LOG_DIR.mkdir(exist_ok=True)
            prev = LOG_DIR / f"preview_force_{now:%Y%m%d_%H%M%S}.html"
            prev.write_text(new_content, encoding="utf-8")
            log(f"[DRY-RUN] --force プレビュー: {prev}")
            print(au.region_of(new_content))
            return
        bpath = au.backup(cfg, post["content"])
        log(f"旧本文を退避: {bpath}")
        status = au.put_post(cfg, new_content)
        # --force はレイアウト反映なので連続更新スロットルの起点(last_wp_update)は触らない
        save_state(state)
        log(f"--force: 記事を今の内容で描き直した(status: {status})")
        ping_search_console(cfg, post)
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

    # --- ソース2: デスクトップに出したGoogleマップ画面をスクショ→Vision で読む ---
    if cfg.get("screen_map_enabled", False):
        try:
            LOG_DIR.mkdir(exist_ok=True)
            region = cfg.get("screen_map_region") or None
            map_posts = screen_map_fetch.fetch(
                region=region,
                save_shot_to=str(LOG_DIR / "last_map_shot.png"),
                model=cfg.get("llm_model_gemini", "gemini-3.5-flash"),
            )
            log(f"Googleマップ画面 読み取り {len(map_posts)} 件"
                + (f" -> {map_posts[0]['text'][:80]}" if map_posts else " (判別不可/失敗)"))
            posts.extend(map_posts)
        except Exception as e:  # noqa: BLE001
            log(f"[warn] Googleマップ画面の読み取り失敗: {e}")

    # --- ソース(実験): 追跡者の Google マップ位置共有リンク ---
    if cfg.get("share_map_enabled", False) and cfg.get("share_map_url"):
        try:
            sm = share_map_fetch.fetch(cfg["share_map_url"])
            log(f"位置共有マップ 読み取り {len(sm)} 件"
                + (f" -> {sm[0]['text'][:70]}" if sm else " (座標取れず)"))
            posts.extend(sm)
        except Exception as e:  # noqa: BLE001
            log(f"[warn] 位置共有マップの読み取り失敗: {e}")

    # --- ソース3: X(補助・失敗しても続行) ---
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

    # 現在地が前回と実質同じ(末尾の「(走行中)」等を除いて一致)なら、
    # 移動なしとみなして記事は更新しない(トモキ指示 2026-08-29)。
    def _norm_loc(s):
        s = re.sub(r"[（(][^（()）]*[）)]\s*$", "", (s or "").strip()).strip()
        return re.sub(r"\s+", "", s)

    prev_loc = state.get("current_location", "")
    new_loc = result.get("current_location", "") or prev_loc
    if _norm_loc(new_loc) and _norm_loc(new_loc) == _norm_loc(prev_loc):
        state["seen_ids"] = (list(seen | {p["id"] for p in posts}))[-MAX_SEEN:]
        save_state(state)
        log(f"現在地が前回と同じ('{prev_loc}')。移動なしとみなし記事は更新しない。")
        return

    if throttled and not args.dry_run:
        log(f"前回更新から {min_gap} 分未満。今回はスキップ(次回反映)。")
        return

    # 1回の更新で足すエントリ数の上限(既定1)。冗長な連投を防ぐ。
    cap = int(cfg.get("max_new_entries_per_update", 1))
    fresh = result["entries"][:cap] if cap > 0 else result["entries"]

    # エントリを蓄積。time+text で重複排除
    existing_keys = {(e.get("time", ""), e.get("text", "")) for e in state["entries"]}
    added = 0
    for e in reversed(fresh):  # LLM出力は新しい順想定。古い方から prepend
        key = (e.get("time", ""), e.get("text", ""))
        if key in existing_keys:
            continue
        state["entries"].insert(0, {
            "time": e.get("time", ""), "text": e.get("text", ""),
            "map_query": e.get("map_query", ""),
        })
        existing_keys.add(key)
        added += 1

    if not added:
        state["seen_ids"] = (list(seen | {p["id"] for p in posts}))[-MAX_SEEN:]
        save_state(state)
        log("新しい追記エントリなし(全て既出)。記事は更新しない。")
        return

    # 時系列で新しい順に並べ替え("M/D HH:MM" をパース、失敗分は末尾)
    def _entry_key(e):
        m = re.match(r"\s*(\d{1,2})/(\d{1,2})\s+(\d{1,2}):(\d{2})", e.get("time", ""))
        if not m:
            return (0, 0, 0, 0)
        mo, d, h, mi = (int(x) for x in m.groups())
        return (mo, d, h, mi)
    state["entries"].sort(key=_entry_key, reverse=True)
    state["entries"] = state["entries"][:MAX_ENTRIES]
    if result.get("current_location"):
        state["current_location"] = result["current_location"]
    log(f"追記エントリ {added} 件 / 累計 {len(state['entries'])} 件 / 現在地='{state['current_location']}'")

    region = au.render_region(
        state["current_location"], state["entries"],
        updated_at=now.strftime("%m/%d %H:%M") + " JST",
        map_zoom=int(cfg.get("map_zoom", 15)), heading=_heading,
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
    ping_search_console(cfg, post)


if __name__ == "__main__":
    main()
