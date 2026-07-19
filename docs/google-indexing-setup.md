# Google Indexing APIのセットアップ手順

**現在の状態(2026-07-19)**: 稼働中。サービスアカウント`chomoand-477@model-gearing-465707-d6.iam.gserviceaccount.com`を3サイトのSearch Consoleオーナーとして登録済み。経緯は[docs/history.md](history.md)参照。新しいPCでセットアップする場合、鍵ファイル(`google-indexing-key.json`)を安全な経路でコピーして`.env`にパスを設定するだけでよい(1〜2章のCloud Console/Search Console作業を毎回やり直す必要はない)。

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
