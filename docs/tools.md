# ツール詳細

`tools/` 配下のツールの詳しい説明・仕組み・現在のステータス。CLAUDE.mdには要点だけ書いてあるので、実装の背景や過去の経緯を知りたいときはここを見る。

## Xiy(`tools/Xiy/`)

X/Instagram投稿収集 + YouTube文字起こしツール。`tools/Xiy/起動.bat`で起動。SNS調査スキル(sns-research)で使用。

YouTube文字起こしは「字幕優先(youtube-transcript-api)→無ければWhisper(faster-whisper)で音声文字起こし」の2段構成。GPUがあれば自動でCUDAを使い(無ければCPU int8)、複数動画処理時は字幕チェックの並列化・音声DLと文字起こしのパイプライン化で高速化してある(2026-07-02改良)。

## Codex

記事・文書生成に使用。詳細は[codex-writingスキル](../.claude/skills/codex-writing/SKILL.md)参照。

## LINE通知(`tools/line_notify.py`)

記事の更新・リライト提案時、および`koikeyz-monitor`の毎朝の監視結果報告でLINEへプッシュ通知するツール(2026-07-05追加)。

- LINE Notifyは2025年3月にサービス終了済みのため、LINE公式アカウント(Messaging API)のチャネルアクセストークンを使う方式。
- `.env`の`LINE_CHANNEL_ACCESS_TOKEN`/`LINE_USER_ID`が未設定の場合は通知だけスキップされ、他の処理は止まらない(フェイルセーフ)。
- 初回セットアップ手順は[docs/line-notify-setup.md](line-notify-setup.md)を参照(フォロワーID一覧APIは無料プランだと使えないため要注意)。
- 呼び出し元はkoikeyz-rewriteスキル(リライト提案時・更新完了時・Gemini失敗時のフォールバック要約)と`tools/koikeyz-monitor/x_monitor.py`(毎朝、結果に関わらず必ず通知)。
- なお「LINE返信でマツが自動執筆する」パイプラインは本番ドメインのDNS移行リスクを理由に見送り済み([docs/line-notify-setup.md](line-notify-setup.md)参照)。

## Canva MCP(`https://mcp.canva.com/mcp`)

chomoand-1.com(コイキーズブログ)のアイキャッチを作るための公式リモートMCP(2026-07-15追加、`.mcp.json`に登録済み)。

- **コイキーズ記事のアイキャッチは必ずこれで作る**(2026-07-15にトモキが指示・動作検証済み)。
- トモキの既存デザイン(`DAG_zqaJE_8`)のページ36を複製してテキストを差し替える方式で、フォント・レイアウトが本物と完全に一致する。
- **背景の色は毎回ランダムに変える**(サイトの全記事が違う色で統一されているため)。
- **PCごとに`/mcp`からの認証が必要**。
- 手順・ハマりどころ・色替え用アセット一覧は[docs/canva-mcp.md](canva-mcp.md)参照。

## KO1KEYZアイキャッチ生成(`tools/eyecatch_koikeyz.py`)

上記Canva MCPの**フォールバック**(2026-07-15追加)。Canvaが認証切れなどで使えないときだけ使う。HTML+Playwrightで見た目を再現するがフォントだけ本物と違う(M PLUS Rounded 1c Black)。使い方・デザイン仕様は[docs/eyecatch-style.md](eyecatch-style.md)参照。

**コイキーズ記事のアイキャッチを勝手に別デザインで作らないこと。**

## YouTube急上昇取得(`tools/youtube_trending.py`)— 現在未使用

**2026-07-14に路線撤回したため現在は未使用。** chomoand.comは恋リア特化へ方針転換したため(経緯は[docs/chomoand-pivot.md](chomoand-pivot.md)参照)。ツールとスキルは消さずに残してある。

以下は当時(chomoand.com旧方針=TikTok/YouTube発バズインフルエンサーのwiki記事)のネタ探し用ツールとしての説明:

- YouTube Data API v3で日本の急上昇動画を取得する。`.env`の`YOUTUBE_API_KEY`が必要(2026-07-06追加)。
- セットアップ手順は[docs/youtube-api-setup.md](youtube-api-setup.md)、使い方は[youtube-trendingスキル](../.claude/skills/youtube-trending/SKILL.md)参照。
- YouTube急上昇ページ・TikTok Creative CenterはどちらもJS描画でWebFetchでは中身が取れないため、API経由で取得する方式にした。TikTok側は現時点で自動取得の手段なし。

## Xトレンド監視(`tools/x-trend-monitor/`)— 現在停止中

**2026-07-14にユーザー指示で停止中**(タスクスケジューラの`X-Trend-Monitor`を`Disable-ScheduledTask`で無効化。削除はしていないので`Enable-ScheduledTask`で復帰できる)。**再開の指示があるまで勝手に有効化しないこと。**

以下は仕組みの説明:

chomoand.com(トレンドブログ)の全自動記事化パイプラインの入口(2026-07-10追加)。タスクスケジューラ(タスク名: `X-Trend-Monitor`)で6時間おきに`trend_monitor.py`がXのトレンドページ(x.com/explore/tabs/trending)を取得し、新トレンド(同一語24時間クールダウン、1回最大3件、プロモーション枠除外)を検知すると`claude -p`でヘッドレスClaudeを起動して[x-trend-articleスキル](../.claude/skills/x-trend-article/SKILL.md)の自動記事化(リサーチ→執筆→**下書き**投稿→LINE通知)を実行する。

- トークン節約のため、実行間隔は当初の30分から6時間に延ばし、パイプラインが呼ぶClaudeも`--model claude-sonnet-5`(定数`CLAUDE_MODEL`)でSonnet指定にしてある(2026-07-11、ユーザー指示)。
- `claude`はネイティブインストール(`~/.local/bin/claude.exe`)でタスクスケジューラの最小PATH環境では名前解決できないため、`resolve_claude_command()`がフルパスで解決する(PATH非依存)。
- フェーズ1運用のため**公開は必ずユーザー承認制**(LINE通知を見て「公開して」と指示)。
- koikeyz-monitorと同じログイン済みプロファイル方式だがプロファイルは独立(`%USERPROFILE%\x_trend_monitor_profile`、初回にPCごとに`login_x.py`を手動実行)。
- 多重起動は`pipeline.lock`とタスク側`IgnoreNew`で防止。`monitor_state.json`・`reports/`はGit管理外。
- ログイン状態とタスク登録がPC固有なため、登録したPC上でのみ動作する。

## 商品アフィリエイトリンク生成(`tools/affiliate_linker.py`)

コイキーズブログ(chomoand-1.com)の既存記事に載っているブランド・商品の言及に、楽天/Amazonのアフィリエイトリンクを付けるための候補取得ツール(2026-07-26追加)。使い方・対象範囲・承認フローは[koikeyz-affiliateスキル](../.claude/skills/koikeyz-affiliate/SKILL.md)参照。

- 楽天は楽天商品検索API(要`RAKUTEN_APP_ID`)でキーワード検索し、`RAKUTEN_AFFILIATE_ID`を渡すことでレスポンスの`affiliateUrl`がそのままトラッキング付きリンクになる。
- Amazonは商品ページの個別特定はせず、検索結果ページへの`AMAZON_ASSOCIATE_TAG`付きリンク(`https://www.amazon.co.jp/s?k=...&tag=...`)を作るだけ。PA-API(要審査・直近実績)は使わない方針。
- どちらのキーも`.env`未設定なら例外を投げずにスキップ・フォールバックする(他ツールと同じフェイルセーフ方式)。
- 実行例: `python tools/affiliate_linker.py "BADBLOOD DO YOU WANT IT Tシャツ"`

## Googleインデックス登録(`tools/google_indexing.py`)

記事公開時にURLをGoogle Indexing APIへ送信し、即時インデックス登録をリクエストするツール(2026-07-09追加)。[publishスキル](../.claude/skills/publish/SKILL.md)から自動で呼ばれる。

- サービスアカウントのJSON鍵が必要で、`.env`の`GOOGLE_INDEXING_CREDENTIALS_PATH`が未設定の場合は通知だけスキップされ、公開処理自体は止まらない(LINE通知と同じフェイルセーフ方式)。
- セットアップ手順は[docs/google-indexing-setup.md](google-indexing-setup.md)参照。
- Indexing APIは規約上Job Posting/BroadcastEvent専用が本来の用途で、ブログ記事への利用は黙認されている状態である点に注意。
