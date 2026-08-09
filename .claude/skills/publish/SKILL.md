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
6. **Xへの自動投稿(2026-08-09〜)**。記事の内容に合わせてマツ自身がフック文・ハッシュタグを作文し、`python tools/x_auto_post.py --site {trend|audition|koikeys} --text "{フック文}" --hashtags "{ハッシュタグ}" --image "{アイキャッチ画像URL}" --url "{公開URL}"` を実行する
   - siteはchomoand.com=`trend`、chomoand-0.com=`audition`、chomoand-1.com=`koikeys`
   - `.env`にそのサイトの`X_*`キーが未設定の場合はスキップされるだけで、公開処理自体は止めない(セットアップ手順は[docs/x-auto-post-setup.md](../../../docs/x-auto-post-setup.md)参照)
   - **フック文にはURLを含めない**(`--url`で渡した内容がスクリプト側で自動的に2件目のリプライとして投稿される。本文にURLを入れるとXのアルゴリズム上リーチが落ちるため)
   - フック文・ハッシュタグの作文方針は下記「Xの投稿文の作り方」を参照
7. 公開後のURLとインデックス登録・SNS投稿リクエストの結果をユーザーに表示する

## Xの投稿文の作り方

記事タイプに応じて以下のパターンを使い分ける(2026-08-09、SNS拡散調査の結果を反映)。

| 記事タイプ | フック文の型 | ハッシュタグ | 備考 |
|---|---|---|---|
| 新シーズン・出演者発表速報(koi-real) | 「【〇〇編】メンバー解禁!」+一行の煽り | 番組全体タグ+シーズン限定タグの2〜4個 | 速報性が命。同じ告知を数日おきに再投稿するのも有効 |
| 個人プロフィール・wiki(wiki-article/gakureki-kazoku-kanojo) | 記事タイトルをほぼそのまま流用した疑問形 | 人物・番組タグ中心に2〜3個 | 単発投稿でよい |
| 私服・ブランド特定 | 「これ気になった人いる?」等の問いかけ | ブランド・番組タグ | 画像は該当シーンの切り抜きを使う |
| 歴代まとめ・保存版(teiban-navi型) | 「歴代〇〇一覧」の網羅性を煽る一言 | 汎用タグ中心 | 資産コンテンツなので数ヶ月おきに同じ記事をリバイバル投稿してよい |
| ネタバレ・あらすじ | 「〇〇に大事件?」等の煽り一行 | 番組全体タグ+話数/エピソードタグ | 放送直後〜翌朝に投稿、連投もあり |

いずれも本文は結論・フックを冒頭2行以内に収め、ハッシュタグは2〜4個(多すぎるとスパム的に見える)。

**Why:** 以前はGoogle Search ConsoleへのAPI連携が複雑なためユーザーが手動でURL登録していたが、2026-07-09にIndexing API経由での自動化に変更した。Indexing APIは本来Job Posting/BroadcastEvent専用と規約上明記されているが、ブログ記事への利用は黙認されている状態であることをユーザーが承知の上で選択している([docs/google-indexing-setup.md](../../../docs/google-indexing-setup.md)参照)。

**How to apply:** 「公開して」「公開する」「アップ(公開)して」などの発言をトリガーとして実行する。記事の削除は絶対に行わない([docs/wordpress.md](../../../docs/wordpress.md))。
