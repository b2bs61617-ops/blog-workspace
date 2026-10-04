# スマホからマツに指示する(Claude Code クラウド版)

パソコンが無くても、スマホの Claude アプリから記事の公開・X/Threads投稿ができるようにする手順。
作業はクラウドのパソコンで行うので、家のPCは電源オフでよい。

## 1. 最初の設定(1回だけ・PCのブラウザでやると楽)

1. https://claude.ai/code を開き、GitHub と連携して **b2bs61617-ops/blog-workspace** を選べるようにする。
2. 環境(Environment)を新規作成し、次のように設定する。
   - **ネットワークアクセス: 「Full(すべて許可)」**
     WordPress 7サイト・Buffer・楽天にアクセスするため。既定の「Trusted」だと投稿できない。
   - **環境変数**: Googleドライブの `ブログ関係/.env` を開き、中身の行(`KEY=値`)を**そのまま全部貼り付ける**。
     (`GOOGLE_INDEXING_CREDENTIALS_PATH` の行は不要。下の5を参照)
   - **セットアップスクリプト**: 空でOK(セッション開始時にフックが自動で準備する)。
3. **エックスサーバーの「国外IPアクセス制限」でREST APIをOFFにする**(サーバーパネル → WordPress → WordPressセキュリティ設定 → ドメインごと)。
   クラウドは海外IPなので、ONのままだとWordPressが全部403になる。ダッシュボード・XML-RPCはONのままでよい。
   2026-10-04、旅行のためにOFFにした → **帰宅後はONに戻す**。
4. 環境変数は自分で貼るだけ。**チャットでマツに値を教えないこと。**
5. (任意)Googleインデックス登録も使う場合は、`google-indexing-key.json` を base64 にした文字列を
   `GOOGLE_INDEXING_KEY_B64=...` として環境変数に追加する。無くても記事公開・X投稿は動く。
   - PowerShellで作る例: `[Convert]::ToBase64String([IO.File]::ReadAllBytes("google-indexing-key.json"))`

## 2. 出発前のテスト

スマホの Claude アプリ → Code → blog-workspace を選んで、次の順に送る。

1. `python3 tools/cloud/cloud_check.py を実行して結果を見せて`
   - WordPress 7サイト・Buffer が全部 OK なら合格。
   - 楽天は NG でも可(Amazonリンクだけで記事は書ける)。
   - アイキャッチのテスト画像を開いて文字化け(□□□)が無いか見てもらう。
2. `テスト記事をchomoand.comに下書きで1本作って、アイキャッチも付けて。公開はしないで`
   - スマホで下書きのプレビューURLを確認 → 確認後「そのテスト下書きは削除して」。
3. `Bufferの下書き(draft)でX投稿のテストして` (実際には投稿されない)

ここまで通れば旅行中も使える。

## 3. 旅行中の指示の出し方

いつも通りの言葉でOK。

- 「速報トレンドで記事3本書いて下書き→URL見せて」
- 「OK、全部公開してX/Threadsも即時投稿」
- 「KO1KEYZの○○の記事、3言語で公開して」

## 4. できないこと・注意

- 楽天APIはIP制限で失敗しやすい → 楽天リンク無しで公開になることがある。
- Xのブラウザ自動収集(ログインが必要なもの)は使えない → ネタ探しはWeb検索で代用。
- クラウドのマツがmainへpushできない場合は別ブランチに保存される → **帰宅後に「クラウドのブランチをmainにマージして」とマツに頼む。**
- 仕組み: `.claude/settings.json` の SessionStart フックが、クラウドのときだけ `tools/cloud/session_start.sh` を実行し、
  `.env` 生成・Pythonパッケージ・日本語フォント・Chromium を準備する。WindowsのPowerShellフックはクラウドでは飛ばす。
