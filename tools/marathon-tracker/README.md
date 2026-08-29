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
  ├─ yt_chat_fetch.py    … 監視配信の live_chat を yt-dlp で25秒だけ取得→パース(補助)
  ├─ x_fetch.py          … 追跡班アカウントの最新ポスト(沿道情報・補助)。playwright 必須
  ├─ x_fetch.map_url_from_tweet … 【主軸】config.danchou_map_tweet(@YSB_DANCHO の
  │                        「本官の現在地」ポスト)を毎回開き、貼られた Google マップの
  │                        位置共有リンクを取り直す。t.co / カード表示(アンカー文字列が
  │                        "google.com" だけ)でも展開して拾う。GPS を切って貼り直されても
  │                        同じポストを直読みするので追随する。取れなければ最新TLをスキャン→
  │                        config.share_map_url にフォールバック。
  ├─ share_map_fetch.py … その位置共有リンクをヘッドレスで開き、内部RPCから14桁精度の
  │                        座標を取得(URL由来の座標も可)。座標→住所は逆ジオコーディング。
  │                        12分より古い位置/関東外は捨てる。地図スクショも撮る。
  ├─ bearing_note()   … 前回観測座標→今回座標の移動ベクトル(距離km・方位・8方位)を
  │                     機械計算し (@heading) として LLM に渡す(進行方向予測の根拠)
  ├─ 新着なし / 前回と同じ現在地 → 記事を触らず終了
  ├─ llm_extract.py   … 新着メッセージ → {現在地ラベル, 進行方向, 時系列ログ文, 地図クエリ} を JSON 抽出
  │                     primary: config.llm_primary(このPCは "gemini")/ fallback: claude -p
  ├─ article_updater.py … 記事の <!-- MARATHON_TRACKER:BEGIN/END --> 領域を再生成し
  │                       (常に記事の最初の H2 の直前に配置)status:publish で更新。
  │                       各エントリは「HH:MM｜市区町村＋町丁目」の H3 + 座標ピンの
  │                       Google マップ埋め込み + 本文(住所＋進行方向)で1ブロック。時刻ごとに積み上げる。
  └─ google_indexing.notify … 更新できた回だけ Google Indexing API に URL_UPDATED を通知
```

- share_map の座標は「@YSB_DANCHO の位置共有リンクの実座標」。その座標を最新エントリの
  地図ピン(`q=lat,lng`)にそのまま使い、逆ジオコーディングした住所を H3 見出しに併記する。
- 記事末尾の注記(「最終更新: …／…正確な通過地点は番組の公式発表が基準です。」)は
  出さない(2026-08-30 トモキ指示)。

- 多重起動は `tracker.lock` で防止(手動実行とタスクの同時実行で state.json が壊れるのを回避)。
- インデックス通知は「実際に記事を更新した回」だけ。移動なしでスキップした回は送らない
  (Indexing API の 1日 200 リクエスト制限の節約 & 無変更 URL の連投回避)。

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

### Googleマップ画面を読ませる(任意・`screen_map_enabled: true`)

**人がやること**: デスクトップに Google マップ(ランナーの現在地を追える地図。位置共有リンクや
その日の追跡ピンなど)を開いたままにしておく。z=14〜16 くらいで地名が読める状態に。
PC はスリープ・ロックさせない(ロック中のスクショは真っ黒)。

**ツールがやること**: 10分ごとにプライマリ画面をスクショ(4K→長辺1600pxに縮小)し、
Gemini Vision に中心付近の地名・駅名・ランドマークを読ませて1件のメッセージとして
llm_extract に渡す。「判別不可」と返ったら何もしない。最後のスクショは
`logs/last_map_shot.png` に残る。特定ウィンドウだけ撮りたいときは config の
`screen_map_region` に `[left, top, width, height]` を入れる。

### Xの沿道情報も併用する(config は既に `x_enabled: true`)

`config.json` に監視アカウント(`24tv24tv` / `yes0724day`)は設定済み。あとは**Xに一度ログイン**するだけ:

```
pip install playwright
python -m playwright install chromium
$env:PYTHONUTF8=1
python tools\marathon-tracker\login.py      # Chromium が開くので X にログイン→ターミナルで Enter
```

- ログイン状態は `~/marathon_tracker_profile` に保存され、以降 tracker.py がヘッドレスで再利用する。
- ログイン前は「X取得 0 件」で素通り(YouTube+地図で動作)。ログイン後に自動で沿道情報も混ざる。
- 既定は playwright 同梱 chromium を使う。Google Chrome を使いたい場合は環境変数
  `MARATHON_PW_CHANNEL=chrome`(または `msedge`)。
- 監視アカウントを変えるときは `config.json` の `x_accounts`(先頭 @ なし・複数可)。

## config.json のキー

| キー | 意味 |
|---|---|
| `post_id` / `wp_env_prefix` | 更新先の記事ID / `.env` の認証キー接頭辞(chomoand.com は `WP_TREND`) |
| `article_url` / `search_console_ping` | 記事の公開URL / 記事更新のたび Google Indexing API に URL_UPDATED を通知するか(既定 true。`.env` の `GOOGLE_INDEXING_CREDENTIALS_PATH` かリポジトリ直下 `google-indexing-key.json` が必要。未設定なら自動スキップ) |
| `youtube_enabled` / `youtube_video_url` | YouTubeチャット監視の on/off と対象URL |
| `yt_capture_seconds` | 1回あたり yt-dlp を走らせる秒数(既定25) |
| `max_yt_messages` | 1回で拾うチャット最大件数 |
| `screen_map_enabled` / `screen_map_region` | デスクトップのGoogleマップ画面をスクショ→Vision で読む on/off と撮影範囲(nullでプライマリ全体) |
| `share_map_enabled` / `danchou_account` / `danchou_map_tweet` / `share_map_url` | 【主軸】位置共有トラッキング。`danchou_map_tweet` に指定した @YSB_DANCHO の「本官の現在地」ポストを毎回開いて位置共有リンクを取り直す。取れなければ `danchou_account` の最新TLをスキャン → 最後に `share_map_url`(既定の goo.gl リンク)にフォールバック |
| `x_enabled` / `x_accounts` / `x_search_fallback` | X源(沿道情報・補助)。`danchou_account` は自動で先頭に足される。アカウント未設定でも検索で動く |
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
