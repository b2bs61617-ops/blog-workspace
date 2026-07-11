"""X(Twitter)のトレンドを定期取得し、新しいトレンドが出たら記事化パイプライン(ヘッドレスClaude)を起動する。

- タスクスケジューラ(タスク名: X-Trend-Monitor)で6時間おきに実行される想定
- トレンド取得はkoikeyz-monitorと同じ「ログイン済みブラウザプロファイル+Playwright」方式
  (初回のみ login_x.py を手動実行してXにログインしておくこと。プロファイルは独立)
- 新トレンドを検知したら reports/trends_*.json にレポートを書き出し、
  `claude -p` で x-trend-article スキルの自動記事化(下書きまで)を起動する
- 同じトレンド語はCOOLDOWN_HOURS以内は再処理しない(monitor_state.jsonで管理)
- 多重起動防止: pipeline.lock が新しい間は次の実行をスキップする
"""
import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
PROFILE_DIR = str(Path.home() / "x_trend_monitor_profile")
STATE_FILE = ROOT / "monitor_state.json"
REPORTS_DIR = ROOT / "reports"
LOCK_FILE = ROOT / "pipeline.lock"
REPO_ROOT = ROOT.parent.parent

sys.path.insert(0, str(ROOT.parent))
from line_notify import notify  # noqa: E402

TREND_URL = "https://x.com/explore/tabs/trending"
COOLDOWN_HOURS = 24        # 同じトレンド語を再処理しない間隔
MAX_HANDOFF = 3            # 1回の実行でClaudeに渡すトレンド数の上限(コスト対策)
MAX_TRENDS_COLLECT = 30    # ページから拾うトレンドの最大数
CLAUDE_TIMEOUT_SEC = 45 * 60
CLAUDE_MODEL = "claude-sonnet-5"  # 記事化パイプラインのモデル(トークン節約のためOpusではなくSonnet)
LOCK_STALE_MIN = 90        # これより古いロックは異常終了の残骸とみなして無視する
FAILURE_NOTIFY_INTERVAL_HOURS = 6  # 取得失敗のLINE通知は6時間に1回まで(スパム防止)
STATE_META_PREFIX = "_"    # stateのメタ情報キー(トレンド名と衝突しないよう_始まり)

VOLUME_RE = re.compile(r"(件のポスト|件のツイート|posts?|Tweets?)$")
RANK_RE = re.compile(r"^\d+$")


def parse_trend_lines(lines):
    """トレンド要素(div[data-testid="trend"])のinner_textの行リストから
    {name, category, volume} を組み立てる。プロモーション枠・解釈不能な枠はNone。

    実際の行の並びの例:
        ["1", "トレンド", "大谷翔平", "12.3万件のポスト"]
        ["2", "音楽 · トレンド", "#NewJeans"]
        ["エンターテインメント · トレンド", "呪術廻戦", "5.4万件のポスト"]
    """
    lines = [line.strip() for line in lines if line.strip()]
    if any("プロモーション" in line for line in lines):
        return None

    name = None
    category = ""
    volume = ""
    for line in lines:
        if RANK_RE.match(line):  # 順位の数字行
            continue
        if VOLUME_RE.search(line):  # 「1.2万件のポスト」など
            volume = line
            continue
        # 「トレンド」「日本のトレンド」「音楽 · トレンド」などの分類行
        if line == "トレンド" or line.endswith("のトレンド") or "·" in line:
            category = line
            continue
        if name is None:
            name = line
    if not name:
        return None
    return {"name": name, "category": category, "volume": volume}


def filter_new_trends(trends, state, now=None, cooldown_hours=COOLDOWN_HOURS):
    """stateに記録済み(=cooldown内に処理済み)のトレンドを除いた新規分だけ返す。"""
    now = now or datetime.now()
    new = []
    for t in trends:
        last = state.get(t["name"])
        if isinstance(last, str):
            try:
                last_dt = datetime.fromisoformat(last)
                if now - last_dt < timedelta(hours=cooldown_hours):
                    continue
            except ValueError:
                pass
        new.append(t)
    return new


def mark_seen(state, trends, now=None):
    """Claudeに引き渡したトレンドだけを処理済みとして記録する(未処理分は次回また検知される)。"""
    now_iso = (now or datetime.now()).isoformat(timespec="seconds")
    for t in trends:
        state[t["name"]] = now_iso
    return state


def prune_state(state, now=None, keep_days=14):
    """古い記録を掃除してstateの肥大化を防ぐ。メタ情報(_始まり)は残す。"""
    now = now or datetime.now()
    pruned = {}
    for key, value in state.items():
        if key.startswith(STATE_META_PREFIX):
            pruned[key] = value
            continue
        try:
            if now - datetime.fromisoformat(value) <= timedelta(days=keep_days):
                pruned[key] = value
        except (TypeError, ValueError):
            continue
    return pruned


def should_notify_failure(state, now=None, interval_hours=FAILURE_NOTIFY_INTERVAL_HOURS):
    """取得失敗のLINE通知を送ってよいか(前回の失敗通知から一定時間経過したか)。"""
    now = now or datetime.now()
    last = state.get("_last_failure_notify")
    if isinstance(last, str):
        try:
            if now - datetime.fromisoformat(last) < timedelta(hours=interval_hours):
                return False
        except ValueError:
            pass
    return True


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def lock_is_fresh():
    if not LOCK_FILE.exists():
        return False
    return (time.time() - LOCK_FILE.stat().st_mtime) < LOCK_STALE_MIN * 60


async def collect_trends(max_items=MAX_TRENDS_COLLECT):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR, headless=False, channel="chrome", slow_mo=30,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(TREND_URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(4000)

        trends = []
        elements = await page.query_selector_all('div[data-testid="trend"]')
        for el in elements[:max_items]:
            try:
                text = await el.inner_text()
            except Exception:
                continue
            parsed = parse_trend_lines(text.split("\n"))
            if parsed and all(parsed["name"] != t["name"] for t in trends):
                parsed["rank"] = len(trends) + 1
                trends.append(parsed)
        await context.close()
    return trends


def claude_candidates(home=None, env=None):
    """claude CLIの実行パス候補を優先順に返す(存在チェックはしない・純粋関数)。

    タスクスケジューラの最小PATH環境ではnpmや ~/.local/bin がPATHに乗らず
    `claude` を名前で呼べないため、既知のインストール先を明示的に候補に含める。
    """
    home = Path(home) if home else Path.home()
    env = env if env is not None else os.environ
    cands = []
    if env.get("CLAUDE_BIN"):
        cands.append(env["CLAUDE_BIN"])
    # ネイティブインストーラ(推奨)の既定パス
    cands.append(str(home / ".local" / "bin" / "claude.exe"))
    cands.append(str(home / ".local" / "bin" / "claude"))
    # npmグローバルインストール
    if env.get("APPDATA"):
        cands.append(str(Path(env["APPDATA"]) / "npm" / "claude.cmd"))
    return cands


def pick_claude_path(candidates, exists):
    """候補のうち最初に存在するパスを返す。無ければNone(純粋関数・テスト用)。"""
    for c in candidates:
        if c and exists(c):
            return c
    return None


def resolve_claude_command():
    """claude CLIの実行パスを解決する。PATH解決を優先し、失敗したら既知の候補を探す。"""
    found = shutil.which("claude")
    if found:
        return found
    return pick_claude_path(claude_candidates(), lambda p: Path(p).exists())


def build_claude_cmd(claude_path, prompt, model=CLAUDE_MODEL):
    """claude実行パスからsubprocess用のコマンド配列を組み立てる。
    .cmd/.batはcmd経由でないと実行できない。.exeは直接呼べる(純粋関数)。"""
    args = ["-p", prompt, "--model", model, "--dangerously-skip-permissions"]
    lower = claude_path.lower()
    if lower.endswith(".cmd") or lower.endswith(".bat"):
        return ["cmd", "/c", claude_path, *args]
    return [claude_path, *args]


def run_claude_pipeline(report_path):
    """ヘッドレスClaudeでx-trend-articleスキルの自動記事化を起動する。標準出力はログに保存。"""
    prompt = (
        f"x-trend-articleスキルに従って、Xトレンドレポート {report_path} を処理してほしいワン。"
        "記事は下書きまで(絶対に公開しない)、完了・見送りはLINE通知で報告するルールだワン。"
    )
    log_path = Path(str(report_path).replace(".json", ".claude.log"))
    claude_cmd = resolve_claude_command()
    if not claude_cmd:
        log_path.write_text(
            "claude CLIが見つからなかった。PATHが通っていないか未インストール。"
            "CLAUDE_BIN環境変数でフルパスを明示できる。",
            encoding="utf-8",
        )
        return False
    cmd = build_claude_cmd(claude_cmd, prompt)
    LOCK_FILE.write_text(datetime.now().isoformat(), encoding="utf-8")
    try:
        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=CLAUDE_TIMEOUT_SEC,
        )
        log_path.write_text(
            f"returncode: {result.returncode}\n\n--- stdout ---\n{result.stdout}\n\n--- stderr ---\n{result.stderr}",
            encoding="utf-8",
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        log_path.write_text("timeout", encoding="utf-8")
        return False
    finally:
        LOCK_FILE.unlink(missing_ok=True)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-claude", action="store_true",
                        help="レポート出力までで止める(記事化パイプラインを起動しない)")
    parser.add_argument("--dry-run", action="store_true",
                        help="トレンド取得と新規判定だけ行い、state更新もレポート出力もしない")
    args = parser.parse_args()

    if lock_is_fresh():
        print("前回の記事化パイプラインがまだ実行中(pipeline.lockが新しい)なのでスキップするワン")
        return

    state = load_state()

    try:
        trends = await collect_trends()
    except Exception as e:
        print(f"トレンド取得に失敗: {type(e).__name__}: {e}")
        trends = []

    if not trends:
        print("トレンドが1件も取得できなかった(ログイン切れ・ページ構造変更の可能性)")
        if not args.dry_run and should_notify_failure(state):
            try:
                notify("Xトレンドの取得に失敗したワン。ログイン切れかもしれないから login_x.py を確認してほしいワン")
                state["_last_failure_notify"] = datetime.now().isoformat(timespec="seconds")
                save_state(state)
            except Exception as e:
                print(f"LINE通知に失敗(処理は続行): {type(e).__name__}: {e}")
        return

    new_trends = filter_new_trends(trends, state)
    print(f"取得 {len(trends)}件 / 新規 {len(new_trends)}件")
    for t in new_trends:
        print(f"  [{t['rank']}] {t['name']} {t['category']} {t['volume']}")

    if args.dry_run:
        return
    if not new_trends:
        return

    handoff = new_trends[:MAX_HANDOFF]
    REPORTS_DIR.mkdir(exist_ok=True)
    stamp = f"{datetime.now().strftime('%Y-%m-%d')}_{int(time.time())}"
    report_path = REPORTS_DIR / f"trends_{stamp}.json"
    report_path.write_text(json.dumps({
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source": TREND_URL,
        "trends": handoff,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"レポート出力: {report_path}")

    state = prune_state(mark_seen(state, handoff))
    save_state(state)

    if args.no_claude:
        return

    ok = run_claude_pipeline(report_path)
    if not ok:
        try:
            notify(f"Xトレンドの記事化パイプラインが失敗したワン。ログを確認してほしいワン: {report_path.name}")
        except Exception as e:
            print(f"LINE通知に失敗: {type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
