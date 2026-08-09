# ツール詳細

`tools/` 配下のツールの詳しい説明・仕組み・現在のステータス。CLAUDE.mdには要点だけ書いてあるので、実装の背景や過去の経緯を知りたいときはここを見る。

## Xiy(`tools/Xiy/`)

X/Instagram投稿収集 + YouTube文字起こしツール。`tools/Xiy/起動.bat`で起動。SNS調査スキル(sns-research)で使用。

YouTube文字起こしは「字幕優先(youtube-transcript-api)→無ければWhisper(faster-whisper)で音声文字起こし」の2段構成。GPUがあれば自動でCUDAを使い(無ければCPU int8)、複数動画処理時は字幕チェックの並列化・音声DLと文字起こしのパイプライン化で高速化してある(2026-07-02改良)。

**コメント欄収集(2026-08-02〜)**: 投稿本文・画像に加えてコメント欄(投稿者名+本文)も収集し、`posts.txt`とAI分析プロンプトに含める。誤情報が混じることもあるが、まず拾ってから人間/AIが真偽を判断する方針(2026-08-02・ユーザー明言)。

- **Instagram**: 投稿を開いたモーダル内で「もっと見る」ボタンのクリック+スクロールを伸び止まるまで(最大6回)繰り返してから抽出。追加のページ遷移は不要。
- **X**: タイムライン/検索結果の一覧にリプライが出ないため、ツイートごとに詳細ページを`context.new_page()`で個別に開き、下スクロールしながら新着が止まるまで取得する(`fetch_x_replies`、上限40件/ツイート)。

**bot検知対策(2026-08-02〜)**: リプライ・コメント収集でページ遷移/操作が増えた分、以下で人間らしい挙動に近づけている。
- 詳細ページを開く前後にランダムな待機(1.5〜3.5秒)とマウス移動を挟む
- X側は偽ブロックページ(`JavaScriptを使用できません`)を検知したら即座にそのツイートの収集を諦めて撤退する
- X・Instagramとも10〜15件処理するごとに15〜30秒のランダムな休憩を自動で挟む(一定間隔の機械的なアクセスパターンを避けるため)

これでも収集速度は全体的に落ち、bot検知のリスクも一覧スクロールのみの場合より上がる(トレードオフ承知の上でユーザーが有効化を選択)。

**動画投稿は非対応**: X/Instagramのフィード上の動画投稿(動画ツイート・Reels等)はテキスト・画像のみ抽出する現在の実装では中身を認識できない。X側は動画投稿からサムネイル画像すら取得できずキャプション文言がなければ丸ごとスキップされる。Instagram側はサムネイル画像1枚は取得できる場合があるが、動画の内容(音声・動き)の分析はしていない。動画内容の理解が必要な場合は、YouTube動画であれば別途YouTube文字起こし機能(字幕/Whisper)を使う。

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

当初はCanva MCPの**フォールバック**(2026-07-15追加、Canvaが認証切れなどで使えないときだけ使う想定)。HTML+Playwrightで見た目を再現するがフォントだけ本物と違う(M PLUS Rounded 1c Black)。使い方・デザイン仕様は[docs/eyecatch-style.md](eyecatch-style.md)参照。

2026-07-24〜「KO1KEYZはアイキャッチを作らない」方針で未使用になっていたが、**2026-07-30にSNS自動投稿(Instagram/Jetpack Social)の画像必須要件のため復活**([docs/sns-auto-post-setup.md](sns-auto-post-setup.md)参照)。[blog-uploadスキル](../.claude/skills/blog-upload/SKILL.md)STEP4でKO1KEYZ記事にもこのツールでアイキャッチ(兼SNS投稿用画像)を生成し、featured_mediaとして設定する。

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

## YouTubeタレント監視(`tools/youtube-talent-monitor/`)

chomoand-0.com(ジャニオタブログ)向け。STARTO ENTERTAINMENT所属・出身タレントの公式YouTubeチャンネルを毎日チェックし、新着動画が出たら文字起こし・画像解析付きでLINEに通知するツール(2026-07-29追加)。

**Why:** タレント自身が発信するYouTube動画にはロケ地・着用ファッション・食べたものなど、ファンが知りたい一次情報が豊富に含まれる。テレビ番組表監視([tv-researchスキル](../.claude/skills/tv-research/SKILL.md))より速報性・掘りやすさで優れるとユーザー判断([[chomoand0-youtube-monitor-strategy]]の経緯で導入)。

- 監視対象は`tools/youtube-talent-monitor/channels.json`(グループ公式・現役個人・退所済み元タレント個人の各チャンネル。2026-07-29時点で29チャンネル解決済み、4チャンネルはハンドル未確認で`channel_id: null`のままスキップ)。
- **新着検知はYouTube Data APIを使わず、チャンネルごとの公開RSSフィード**(`https://www.youtube.com/feeds/videos.xml?channel_id=...`)**を使う。APIキー不要・無料枠の心配なし**(2026-07-29、当初はYouTube Data API案だったが「Xiyで文字起こしできるならAPI要らないのでは」というユーザー指摘でRSS方式に切り替え)。
- **文字起こしはリポジトリ直下の`youtube_transcript.py`をそのまま再利用**([youtube-transcriptスキル](../.claude/skills/youtube-transcript/SKILL.md)と共通コード)。新着動画ごとにベストエフォードで取得し(字幕が無ければNone、失敗しても通知は止めない)、`reports/`のJSONに保存する(1本あたり最大4,000字に切り詰め)。
- 新着判定は`monitor_state.json`(channel_id→最後に見た動画ID、Git管理外)で行う。初回実行時は既存の最新動画1本だけを「新着」とし、いきなり大量通知しない。
- **画像解析(`visual_analysis.py`)**: 文字起こしでは分からない服装・アクセサリー・訪問場所を補うため、新着動画1本ごとにyt-dlpで低解像度(480p以下)の直リンクを取得し、`opencv-python-headless`の`VideoCapture.set(CAP_PROP_POS_MSEC)`でシークして代表フレームを12枚キャプチャする(**ffmpeg不要の設計**。動画をディスクにフルダウンロードしない)。抽出したフレームは`frames/{video_id}/`に保存して残す(2026-07-29時点の方針、著作権のある動画フレームのためGit管理外)。保存したフレームをGemini 2.5 Flash(`GEMINI_API_KEY`、`koikeyz-monitor`と同じ`google-genai`SDKを流用)に渡し、服装・アクセサリー・ロケーション(画面に映る看板・地名などの文字情報含む)を箇条書きで要約させる。**この処理はClaude/マツを介さずスクリプト単体・Gemini APIのみで完結する**(2026-07-29、トモキ指示。日次の自動監視でClaude Codeのトークンを消費しないようにするため)。
- `LINE_CHANNEL_ACCESS_TOKEN`(未設定なら通知だけスキップ)を使う。LINE通知には動画タイトル・URLのみ載せ、文字起こし・画像解析結果は`reports/`のJSONと`frames/`の画像を見る。
- 実行: `python tools/youtube-talent-monitor/video_monitor.py`(`--dry-run`で状態を書き換えず新着表示のみ、`--no-transcript`で文字起こしを取得せず速報のみ、`--no-visuals`で画像解析をしない)
- **現時点では検知・通知・文字起こし・画像解析までで、記事執筆の自動化はしない**(ロケ地・私服の最終的な特定・記事化は人間かAIが`reports/`と`frames/`を見て判断する)。
- タスクスケジューラに`YouTube-Talent-Monitor`というタスク名で登録済み(2026-07-29、1台のPCで毎日**23:00 JST**実行)。実行時刻は直近8日間・76件の投稿時刻を集計して決めた(0〜6時台の投稿はゼロ、ピークは18時と21時、23時までに当日投稿の100%が出揃う。**当初は8時に登録していたが、それだと当日投稿の96%がまだ上がっていない状態でチェックしてしまうことが分析で判明し23時に変更**)。1日1回のみのため投稿からチェックまで最大約23時間のラグがあるが、「最速で書く」を優先してチェック頻度を増やす場合はx-trend-monitorと同じ複数回/日方式への変更を検討する。
- `channel_id`が`null`のまま残っている4チャンネル(Johnny's official本体、ジュニアCHANNEL、Johnny's Gaming Room、SUPER EIGHT)はハンドルが確認できず自動解決できなかった。特にSUPER EIGHT(旧関ジャニ∞)は名称が一般的すぎて誤同定リスクがあるため見送った。確認でき次第`channels.json`に手動で追記する。

## 記事本文用に動画から1コマだけ手動で切り出したい場合(2026-08-03)

`youtube-talent-monitor`の`visual_analysis.py`と同じyt-dlp+opencv方式を、監視ツールを介さずその場で単発実行したいとき(例:記事に使う特定シーンの画像が欲しい)のやり方。

- `yt_dlp.YoutubeDL({"format": "best[height<=720][ext=mp4]/best[height<=720]"})`で直リンクを取得し、`cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)`でシークして`cv2.imwrite`で保存する。
  - **`cv2.CAP_FFMPEG`を明示的に指定しないと失敗することがある**(2026-08-03確認、opencv-python 5.0.0)。バックエンド自動判定がgooglevideo.comの直リンクURLを誤って`CAP_IMAGES`(連番画像リーダー)と判定し、`error: (-5:Bad argument) CAP_IMAGES: error, expected '0?[1-9][du]' pattern`で失敗する。
- どのタイムスタンプが目的のシーンか分からない場合、数秒〜数十秒間隔で広くフレームを抜いてPillowで1枚のコンタクトシート(サムネイル一覧画像)に敷き詰めると、少ない画像読み込み回数で目視確認できて効率的(1シートあたり160×90px前後のタイル×40〜80枚程度)。
- ユーザーが動画URL+大まかなタイムスタンプ(「1:59あたり」等)を指定してくれた場合は、その前後数秒〜十数秒だけ1秒刻みで抜けば十分。
- 抽出したフレームは記事のアイキャッチではなく本文画像として、`wp/v2/media`にアップロード→記事の`content`にfigure+figcaptionで埋め込む(下記「画像埋め込みルール」参照)。

### 追記(2026-08-05): 高解像度フレームの取り方・レターボックス除去・「全員写ってる画像」の探し方

- **`yt_dlp`が`No supported JavaScript runtime could be found`警告を出す環境では、`format: "best[height<=720]"`のような結合フォーマット指定だと360p(`18`)しか取れないことがある**(署名解読にJSランタイムが必要な高解像度の結合フォーマットが選べないため)。フレーム抽出は音声不要なので、`info['formats']`から**映像のみのフォーマット(例:`format_id == '137'`で1080p mp4/avc1)を直接指定**すれば`cv2.VideoCapture`でそのまま高解像度フレームが取れる。`ffmpeg`が無くても映像onlyストリームなら結合不要でそのまま使える。
- MVなど映画的画角(シネマスコープ)の動画は上下に黒帯(レターボックス)が入っていることが多い。そのままだと本文画像に不要な黒帯が写るため、`cv2`でグレースケール化して行ごとの平均輝度が閾値以下の行を上下から削る(黒帯除去)と綺麗にトリミングできる。
- **メンバー全員など「N人全員が写っている画像がほしい」と頼まれたときは、候補シーンを選ぶ前にその画角でN人が横に並びきるかを確認する**。寄りのカット(例:エンディングの整列ショット)は1人あたりの横幅が大きく、7人グループでも16:9フレームに5人程度しか収まらないことがある(2026-08-05、Travis Japan「On My Road -Stadium ver.-」記事で確認)。全員を収めたい場合は、寄りのカットに固執せず、サビの隊形シーンや俯瞰・引きのカットなど**カメラが遠い/広い画角のタイムスタンプ**を優先して探す方が確実。

### 追記(2026-08-09): `.set(POS_MSEC)`のシーク精度は呼び出し方で変わる

複数の候補シーンを見比べながら本文画像を選ぶとき、`cv2.VideoCapture`をどう使うかでシークの正確さが変わることを確認した(Travis Japan「【俺節】げんたに会いに大阪に行ったよ♪」記事で判明)。

- **同一の`VideoCapture`オブジェクトを使い回し、時系列順(昇順)に`.set(POS_MSEC, t)`→`.read()`を繰り返す方式は正確にシークできる**。コンタクトシート作成(既存の方式)がまさにこれで、狙った時刻の場面が確実に取れる。
- 一方、**「毎回新しく`VideoCapture`を開いて1回だけ`.set()`→`.read()`する」方式や、時系列を無視してランダムな順にシークする方式は、`ret=True`が返ってきても実際には数十秒〜1分近くズレた別の場面のフレームが返ってくることがある**(googlevideo.comの直リンクに対するffmpegバックエンドのシーク挙動が、コールドスタートやランダムアクセスだと不正確になるとみられる)。
- **How to apply**: 「このタイムスタンプ付近の1枚が欲しい」だけの場合でも、まず広め(前後100〜200秒程度)の範囲を同一セッション内で昇順にコンタクトシート化し、目視で正しい場面のタイムスタンプを特定してから、そのタイムスタンプで(同じ昇順ループの流れの中で)本番のフル解像度フレームを保存するのが確実。範囲を絞った単発の`.set()`だけで済ませようとすると誤ったフレームを掴みやすい。

## KO1KEYZ YouTube監視(`tools/koikeyz-youtube-monitor/`)【2026-07-30〜未使用】

chomoand-1.com(コイキーズブログ)向けに、上記YouTubeタレント監視(chomoand-0向け)と同じ設計を流用して試作したツール(2026-07-30作成)。**同日中にユーザー判断でKO1KEYZには使わない方針となり、タスクスケジューラ登録(`KO1KEYZ-YouTube-Monitor`)は削除済み。** KO1KEYZの情報収集は引き続き下記の「KO1KEYZ監視ツール」(X監視)を主軸とする。コード自体は動作確認済み(KO1KEYZ公式のダンス練習動画で画像解析による服装・アクセサリー・ロケーション抽出を確認済み)のまま、将来また使う可能性に備えて残置している。

- 監視対象は`tools/koikeyz-youtube-monitor/channels.json`。KO1KEYZ公式(`@KO1KEYZOFFICIAL`)とPRODUCE 101 JAPAN公式(`@PRODUCE101JAPAN`)の2チャンネル(channel_id解決済み)。
- 仕組み自体はYouTubeタレント監視と同じ(RSS新着検知・文字起こし・Gemini Vision画像解析・LINE通知)。再度使う場合は`schtasks /Create`でタスク再登録すればよい(登録コマンドはこのセッションの会話履歴参照、またはyoutube-talent-monitor側の登録内容を参考に時刻をずらして作成)。

## 商品アフィリエイトリンク生成(`tools/affiliate_linker.py`)

コイキーズブログ(chomoand-1.com)の既存記事に載っているブランド・商品の言及に、楽天/Amazonのアフィリエイトリンクを付けるための候補取得ツール(2026-07-26追加)。使い方・対象範囲・承認フローは[koikeyz-affiliateスキル](../.claude/skills/koikeyz-affiliate/SKILL.md)参照。

- 楽天は楽天商品検索API(要`RAKUTEN_APP_ID`+`RAKUTEN_ACCESS_KEY`。2026年5月の仕様移行でエンドポイントが`openapi.rakuten.co.jp/ichibams/api/...`に変わり、`accessKey`パラメータが必須になった)でキーワード検索し、`RAKUTEN_AFFILIATE_ID`を渡すことでレスポンスの`affiliateUrl`がそのままトラッキング付きリンクになる。アプリ登録時は「アプリケーションタイプ: バックエンドサービス」を選び、実行環境のグローバルIPを許可リストに登録する必要がある(動的IPだと変わるたびに更新が必要)。
- Amazonは商品ページの個別特定はせず、検索結果ページへの`AMAZON_ASSOCIATE_TAG`付きリンク(`https://www.amazon.co.jp/s?k=...&tag=...`)を作るだけ。PA-API(要審査・直近実績)は使わない方針。
- どちらのキーも`.env`未設定なら例外を投げずにスキップ・フォールバックする(他ツールと同じフェイルセーフ方式)。
- 実行例: `python tools/affiliate_linker.py "BADBLOOD DO YOU WANT IT Tシャツ"`

## Googleインデックス登録(`tools/google_indexing.py`)

記事公開時にURLをGoogle Indexing APIへ送信し、即時インデックス登録をリクエストするツール(2026-07-09追加)。[publishスキル](../.claude/skills/publish/SKILL.md)から自動で呼ばれる。

- サービスアカウントのJSON鍵が必要で、`.env`の`GOOGLE_INDEXING_CREDENTIALS_PATH`が未設定の場合は通知だけスキップされ、公開処理自体は止まらない(LINE通知と同じフェイルセーフ方式)。
- セットアップ手順は[docs/google-indexing-setup.md](google-indexing-setup.md)参照。
- Indexing APIは規約上Job Posting/BroadcastEvent専用が本来の用途で、ブログ記事への利用は黙認されている状態である点に注意。
