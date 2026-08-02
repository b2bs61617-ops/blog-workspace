---
name: publish
description: 「公開して」「公開する」と言われたときに使う。WordPressの下書き記事を公開(publish)に変更してURLを表示する。
---

# 公開スキル

「公開して」と言われたら以下を実行する:

1. 対象の記事IDを確認する(直前の作業の記事ID、または指定された記事ID)
2. [docs/wordpress.md](../../../docs/wordpress.md)の接続情報でREST APIを叩き、ステータスを`publish`に変更
   - エンドポイント: `POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}`
   - ボディ: `{ "status": "publish" }`
3. 公開後のURL(`{サイトURL}/?p={記事ID}`)を確定する
4. `python tools/google_indexing.py {公開URL}` を実行し、Google Indexing APIへ即時インデックス登録をリクエストする
   - `.env`の`GOOGLE_INDEXING_CREDENTIALS_PATH`が未設定の場合はスキップされるだけで、公開処理自体は止めない(セットアップ手順は[docs/google-indexing-setup.md](../../../docs/google-indexing-setup.md)参照)
5. **chomoand-1.com(コイキーズブログ)の記事のみ**、`python tools/naver_indexnow.py {公開URL}` も実行し、IndexNowプロトコル経由でNaverへ即時インデックス登録をリクエストする(2026-08-02〜)
   - `.env`の`NAVER_INDEXNOW_KEY`が未設定の場合はスキップされるだけで、公開処理自体は止めない(セットアップ手順は[docs/naver-search-advisor-setup.md](../../../docs/naver-search-advisor-setup.md)参照)
   - chomoand.com・chomoand-0.comの記事にはこのSTEPは適用しない(Naverキー検証ファイルはchomoand-1.com直下にのみ置く運用のため)
6. 公開後のURLとインデックス登録リクエストの結果をユーザーに表示する

**Why:** 以前はGoogle Search ConsoleへのAPI連携が複雑なためユーザーが手動でURL登録していたが、2026-07-09にIndexing API経由での自動化に変更した。Indexing APIは本来Job Posting/BroadcastEvent専用と規約上明記されているが、ブログ記事への利用は黙認されている状態であることをユーザーが承知の上で選択している([docs/google-indexing-setup.md](../../../docs/google-indexing-setup.md)参照)。

**How to apply:** 「公開して」「公開する」「アップ(公開)して」などの発言をトリガーとして実行する。記事の削除は絶対に行わない([docs/wordpress.md](../../../docs/wordpress.md))。
