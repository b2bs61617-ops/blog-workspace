# marathon-tracker — 24時間テレビ マラソン「現在地」自動追記ツール

その年のマラソンランナーの現在地を、**YouTubeライブ配信のチャット**(＋任意でXの沿道情報)から
**10分おき**に読み取り、新しい位置情報があれば chomoand.com の該当記事の
「リアルタイム情報」セクションへ地図つきで自動追記する。今回の対象:

- 記事: `https://chomoand.com/24h-hoshinomari/`(投稿ID **12158**、status: publish)
- ランナー: 星野真里(24時間テレビ49 / 2026)
- 監視配信: `https://www.youtube.com/watch?v=LOJxmd-xenc`(【生配信】24時間テレビマラソン 星野真里を追跡！)

## 仕組み

```
tracker.py (10分おき・タスクスケジューラ)
  ├─ 稼働時間帯(config.active_from〜active_until)外 → 即終了
  ├─ yt_chat_fetch.py … 監視配信の live_chat を yt-dlp で25秒だけ取得→パース
  │                     (バックログでほぼ現在時刻まで揃うので daemon 不要・毎回取り直し)
  ├─ x_fetch.py       … 任意。config.x_enabled=true かつ playwright 導入時のみ
  ├─ 新着なし         → 記事を触らず終了
  ├─ llm_extract.py   … 新着メッセージ → {現在地ラベル, 時系列ログ文, 地図クエリ} を JSON 抽出
  │                     primary: config.llm_primary(このPCは "gemini")/ fallback: claude -p
  └─ article_updater.py … 記事の <!-- MARATHON_TRACKER:BEGIN/END --> 領域だけ再生成し
                          status:publish を明示して更新(下書きに戻さない)
```

- 触るのはマーカー領域だけ。トモキが手で書いた分・他セクションには一切触れない。
- 上書き前に旧本文を `backups/<id>_<日時>.html` に退避。
- マーカーが記事に無ければ「リアルタイム情報」見出しと「ゴール予想時刻」見出しの
  あいだに自動で作る。**トモキが数回手で追記した後にツールを起動すれば**、その続きに
  マーカー領域が作られ、以降は自動で真似して追記していく。
- YouTubeチャットは玉石混交なので、LLM 側で「複数コメントが一致した位置情報」を優先し、
  1件だけの憶測は「〜との声」程度に落とすよう指示している。

## セットアップ(このPC = Tomoki-GEEKOM で実施済みの分)

- Python 3.12 を `%LOCALAPPDATA%\Programs\Python\Python312` に導入済み
- `pip install yt-dlp google-genai requests` 済み
- `run.bat` は Store版stubに邪魔されないよう Python を明示パスで呼ぶ + `PYTHONUTF8=1`

### トモキがやること(残り)

1. **`blog-workspace\.env` を作る**(`.env.example` をコピーして値を入れる)。最低限:
   - `WP_TREND_URL` / `WP_TREND_USERNAME` / `WP_TREND_APP_PASSWORD`(chomoand.com)
   - `GEMINI_API_KEY`(このPCには `claude` CLI が無いので**必須**)
2. まず様子見(記事は更新しない・差分プレビューだけ):
   ```
   tools\marathon-tracker\run.bat --dry-run
   ```
   初回は「既存チャットを既読化するだけ」で終了。もう一度実行すると新着を LLM 判定して
   `logs\preview_*.html` に差分を書き出す(記事は触らない)。
3. 問題なければ10分おきのタスク登録(管理者PowerShell推奨):
   ```
   powershell -ExecutionPolicy Bypass -File tools\marathon-tracker\register_task.ps1
   ```

### Xの沿道情報も併用したい場合(任意)

```
pip install playwright
python -m playwright install chrome
python tools\marathon-tracker\login.py      # ブラウザでXにログイン
```
その後 `config.json` の `"x_enabled": true`、必要なら `"x_accounts": ["実況アカウント"]` を入れる。

## config.json のキー

| キー | 意味 |
|---|---|
| `post_id` / `wp_env_prefix` | 更新先の記事ID / `.env` の認証キー接頭辞(chomoand.com は `WP_TREND`) |
| `youtube_enabled` / `youtube_video_url` | YouTubeチャット監視の on/off と対象URL |
| `yt_capture_seconds` | 1回あたり yt-dlp を走らせる秒数(既定25) |
| `max_yt_messages` | 1回で拾うチャット最大件数 |
| `x_enabled` / `x_accounts` / `x_search_fallback` | X源(既定off)。アカウント未設定でも検索で動く |
| `active_from` / `active_until` | 稼働時間帯(JST・ISO8601)。外の時間は即終了 |
| `section_heading_contains` / `next_heading_contains` | マーカー領域を置く見出しの目印 |
| `min_minutes_between_wp_updates` | 連続更新の最小間隔(分) |
| `first_run_lookback_minutes` | 2回目以降、何分前まで遡って拾うか |
| `noise_patterns` | この正規表現に当たるメッセージは無視(プレゼント企画など) |
| `course_context` | LLM に渡すコース前提のメモ |
| `llm_primary` | `gemini` か `claude`(このPCは `gemini`) |

## 初回起動の挙動

初回は「既存メッセージを全部既読にするだけ」で記事は更新しない。
2回目以降の実行から、新しく増えたメッセージだけを反映する。
やり直したいときは `run.bat --reset-bootstrap`(または `state.json` を削除)。

## 終わったら

```powershell
Unregister-ScheduledTask -TaskName MarathonTracker_HoshinoMari -Confirm:$false
```

## 注意

- WordPress 記事を**確認なしで自動上書き**するツール。今回トモキの明示指示による特例
  (通常は記事の内容変更は事前確認。CLAUDE.md / docs/wordpress.md)。
- 取得失敗・LLM失敗の回は「何もせず終了」。次回リトライ。
- `state.json` / `backups/` / `logs/` はローカル生成物(Git管理外)。
