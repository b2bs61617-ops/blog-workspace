# Google Indexing APIのセットアップ手順

**現在の状態(2026-08-30更新)**: 稼働中。プロジェクト`model-gearing-465707-d6`のサービスアカウントを3サイトのSearch Consoleオーナーとして登録済み(`chomoand-477@...`および`chomoand-466@...`。どちらの鍵でもIndexing APIは通る)。経緯は[docs/history.md](history.md)参照。

**鍵ファイルの置き場所**: `G:\マイドライブ\ブログ関係\google-indexing-key.json`(Google Drive。全PC共通パス)。`.env`の`GOOGLE_INDEXING_CREDENTIALS_PATH`をこの絶対パスにする。`.gitignore`済み。

**鍵を新規発行する手順**(既存の鍵JSONを紛失した場合。Console からは既存鍵の秘密鍵を再DLできない):
1. [サービスアカウント一覧](https://console.cloud.google.com/iam-admin/serviceaccounts?project=model-gearing-465707-d6)で`chomoand-4xx@model-gearing-465707-d6.iam.gserviceaccount.com`を開く
2. 「キー」タブ →「鍵を追加」→「新しい鍵を作成」→ JSON → 作成(自動DL)
3. `google-indexing-key.json`にリネームして上記 Drive パスへ配置
4. `python tools/google_indexing.py https://chomoand.com/` で`urlNotificationMetadata`が返れば疎通OK
5. 古いキーIDは、他PCが使っている可能性があるので全PC移行が済むまで削除しない

新しいPCでのセットアップは、この鍵ファイルが Drive にあるので`.env`のパスを合わせるだけでよい(1〜2章のCloud Console/Search Console作業を毎回やり直す必要はない)。

記事公開時に投稿URLをGoogleへ即時通知し、インデックス登録をリクエストする仕組み(`tools/google_indexing.py`)の初回セットアップ手順。[publishスキル](../.claude/skills/publish/SKILL.md)から呼ばれる。

**Why:** Google Search ConsoleのUI上の「インデックス登録をリクエスト」は手動操作のみでAPIが無い。一方Indexing APIならURLを送信するだけで即時インデックス登録をリクエストできる。

**注意(規約について):** Indexing APIはGoogleの仕様上、本来Job Posting(求人情報)またはBroadcastEvent(ライブ配信)構造化データを持つページ専用と明記されている。一般的なブログ記事への利用は規約上の想定用途ではなく、多くのSEO事業者が実利用しているため黙認されている状態(2026-07-09時点)。将来Google側の運用が変わりアカウント停止等のペナルティが発生するリスクはゼロではない点を理解した上で利用する。

## 1. サービスアカウントの作成・鍵発行(トモキ本人が実施)

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス(既存プロジェクトを流用可、[YouTube API用](youtube-api-setup.md)と同じプロジェクトでもよい)
2. 「APIとサービス」→「ライブラリ」で「**Web Search Indexing API**」(Indexing API)を検索して有効化
3. 「APIとサービス」→「認証情報」→「認証情報を作成」→「**サービスアカウント**」を作成
4. 作成したサービスアカウントの詳細画面→「鍵」タブ→「鍵を追加」→「新しい鍵を作成」→JSON形式でダウンロード
5. ダウンロードしたJSON鍵ファイルは**Gitに絶対含めない**。リポジトリ外の安全な場所(例: `.env`と同じ階層など、`.gitignore`済みの場所)に保存する
6. サービスアカウントのメールアドレス(JSON内の`client_email`、`xxx@yyy.iam.gserviceaccount.com`の形式)を控える

## 2. Search Consoleへの権限付与(トモキ本人が実施)

対象の3サイト([docs/wordpress.md](wordpress.md)参照)それぞれで以下を行う。

1. [Google Search Console](https://search.google.com/search-console)で対象サイトを開く
2. 「設定」→「ユーザーと権限」→「ユーザーを追加」
3. 手順1で控えたサービスアカウントのメールアドレスを入力し、権限は「**オーナー**」を選択

3サイト(chomoand.com / chomoand-0.com / chomoand-1.com)すべてで同じサービスアカウントを追加する。

## 3. ローカル設定(トモキ本人が実施)

1. `.env`に以下を追加(パスはJSON鍵ファイルの絶対パス):
   ```
   GOOGLE_INDEXING_CREDENTIALS_PATH=C:\path\to\your-service-account-key.json
   ```
2. 必要なライブラリをインストール:
   ```
   python -m pip install google-auth requests
   ```

マツ(Claude Code)はJSON鍵の中身や`.env`の値をチャットで教えたり代筆したりしないので、上記はユーザー自身の作業になる。

## 4. 動作確認

```
python tools/google_indexing.py https://chomoand.com/
```

エラーなくJSONレスポンス(`urlNotificationMetadata`を含む)が返れば設定完了。

## 使われている場所

- `tools/google_indexing.py`: Indexing API呼び出し本体
- [publishスキル](../.claude/skills/publish/SKILL.md): 記事公開時、公開URL確定後に自動で呼び出す。`GOOGLE_INDEXING_CREDENTIALS_PATH`未設定の場合は通知だけスキップし、公開処理自体は止まらない(LINE通知と同じフェイルセーフ方式)

## 5. Search Console API(URL Inspection、閲覧用)を使う場合(2026-08-16追加)

`tools/check_search_console.py`は、Search Console管理画面の「ページがインデックスに登録されなかった理由」に相当する情報(coverageState)を、サイトマップ上の各URLについてURL Inspection APIで一括取得するスクリプト。サービスアカウントは1〜2章で登録済みのもの(`chomoand-477@...`、3サイトともオーナー登録済み)をそのまま流用でき、2章のSearch Console権限付与をやり直す必要はない。

追加で必要な作業(トモキ本人が実施、初回のみ):

1. [Google Cloud Console](https://console.cloud.google.com/)の「APIとサービス」→「ライブラリ」で「**Search Console API**」(`searchconsole.googleapis.com`)を検索して有効化(Indexing APIとは別のAPIなので個別に有効化が必要)
2. `.env`の`GOOGLE_INDEXING_CREDENTIALS_PATH`はそのまま流用可(鍵ファイルの再発行不要)

実行:
```
python tools/check_search_console.py chomoand-1.com --output tools/search_console_report.json
```

サイトマップ(`https://<domain>/sitemap_index.xml`)から`post-sitemap`を含む子サイトマップのURLを集め、1件ずつURL Inspection APIに問い合わせてcoverageStateを集計・出力する。1リクエスト/秒程度に間引いているので件数が多いサイトは時間がかかる。

**注意:** Search Console上のプロパティが「ドメインプロパティ」(`sc-domain:example.com`形式)で登録されている場合、既定の`https://<domain>/`(URLプレフィックスプロパティ)指定では403になることがある。その場合`--site-url "sc-domain:<domain>"`を指定する。
