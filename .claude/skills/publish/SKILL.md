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
3. 公開後のURLをユーザーに表示する(`{サイトURL}/?p={記事ID}`)
4. 「このURLをSearch Consoleに登録してください」と一言添える

**Why:** Google Search ConsoleへのAPI連携は設定が複雑なため、URLの登録はユーザーが手動で行う。松/Codexは公開とURL表示までを担当する。

**How to apply:** 「公開して」「公開する」「アップ(公開)して」などの発言をトリガーとして実行する。記事の削除は絶対に行わない([docs/wordpress.md](../../../docs/wordpress.md))。
