# marathon-tracker — 24時間テレビ マラソン「現在地」自動追記ツール

特定の X アカウント(その年のマラソンランナーの現在地を実況しているアカウント)を
**10分おき**に確認し、新しい位置情報が投稿されたら chomoand.com の該当記事の
「リアルタイム情報」セクションへ地図つきで自動追記する。今回の対象:

- 記事: `https://chomoand.com/24h-hoshinomari/`(投稿ID **12158**、status: publish)
- ランナー: 星野真里(24時間テレビ49 / 2026）

## 仕組み

```
tracker.py (10分おき・タスクスケジューラ)
  ├─ 稼働時間帯(config.active_from〜active_until)外 → 即終了
  ├─ x_fetch.py     … 監視アカウントの最新ポストを取得(ログイン済みプロファイル使用)
  ├─ 新着なし       → 記事を触らず終了
  ├─ llm_extract.py … 新着ポスト → {現在地ラベル, 時系列ログ文, 地図クエリ} を JSON 抽出
  │                    primary: claude -p  /  fallback: Gemini
  └─ article_updater.py … 記事の <!-- MARATHON_TRACKER:BEGIN/END --> 領域だけ再生成し
                          status:publish を明示して更新(下書きに戻さない)
```

- 触るのはマーカー領域だけ。トモキが手で書いた分・他セクションには一切触れない。
- 上書き前に旧本文を `backups/<id>_<日時>.html` に退避。
- マーカーが記事に無ければ「リアルタイム情報」見出しと「ゴール予想時刻」見出しの
  あいだに自動で作る。**トモキが数回手で追記した後にツールを起動すれば**、その続きに
  マーカー領域が作られ、以降は自動で真似して追記していく。

## セットアップ

```bash
# 1. 初回だけ X にログイン(ブラウザが開く)
python tools/marathon-tracker/login.py

# 2. 当日、実況アカウントが分かったら config.json に入れる
#    "x_accounts": ["account_name"]        ← 先頭@なし。複数可
#    ※ 空のままでも x_search_fallback のリアルタイム検索で動くが精度は落ちる

# 3. まず様子見(記事は更新しない・差分プレビューだけ)
python tools/marathon-tracker/tracker.py --dry-run

# 4. 問題なければ10分おきのタスク登録(管理者PowerShell推奨)
powershell -ExecutionPolicy Bypass -File tools/marathon-tracker/register_task.ps1
```

手動1回実行は `tools/marathon-tracker/run.bat`(`run.bat --dry-run` も可)。

## 初回起動の挙動

初回は「既存ポストを全部既読にするだけ」で記事は更新しない。
2回目以降の実行から、新しく増えたポストだけを反映する。
やり直したいときは `python tools/marathon-tracker/tracker.py --reset-bootstrap`。

## config.json のキー

| キー | 意味 |
|---|---|
| `post_id` / `wp_env_prefix` | 更新先の記事ID / `.env` の認証キー接頭辞(chomoand.com は `WP_TREND`) |
| `x_accounts` | 監視する X アカウント(先頭@なし・複数可)。当日入れる |
| `x_search_fallback` | アカウント未設定時に使うリアルタイム検索語 |
| `active_from` / `active_until` | 稼働時間帯(JST・ISO8601)。外の時間は即終了 |
| `section_heading_contains` / `next_heading_contains` | マーカー領域を置く見出しの目印 |
| `min_minutes_between_wp_updates` | 連続更新の最小間隔(分) |
| `noise_patterns` | この正規表現に当たるポストは無視(プレゼント企画など) |
| `course_context` | LLM に渡すコース前提のメモ |
| `llm_primary` | `claude` か `gemini` |

## 終わったら

```powershell
Unregister-ScheduledTask -TaskName MarathonTracker_HoshinoMari -Confirm:$false
```

## 注意

- WordPress 記事を**確認なしで自動上書き**するツール。今回トモキの明示指示による特例
  (通常は記事の内容変更は事前確認。CLAUDE.md / docs/wordpress.md)。
- ログイン切れ・取得失敗の回は「何もせず終了」。次回リトライ。
- `state.json` / `backups/` / `logs/` はローカル生成物(Git管理外)。
