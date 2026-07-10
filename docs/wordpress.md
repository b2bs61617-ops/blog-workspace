# WordPress接続・運用ルール

## サイト一覧

| サイト | URL | 用途 | 認証情報(.envのキー) |
|---|---|---|---|
| トレンドブログ | https://chomoand.com | 時事・話題の記事 | `WP_TREND_URL` / `WP_TREND_USERNAME` / `WP_TREND_APP_PASSWORD` |
| ジャニオタブログ | https://chomoand-0.com | ジャニーズ系記事全般(オーディション番組系だけでなく、グループ・メンバー個人の話題・ファンクラブ情報なども含む) | `WP_AUDITION_URL` / `WP_AUDITION_USERNAME` / `WP_AUDITION_APP_PASSWORD` |
| コイキーズブログ | https://chomoand-1.com | コイキーズ関連の記事 | `WP_KOIKEYS_URL` / `WP_KOIKEYS_USERNAME` / `WP_KOIKEYS_APP_PASSWORD` |

ユーザー名はどのサイトも共通(`b2bs61617@gmail.com`)。実際のアプリパスワードの値は`.env`(このリポジトリ直下、Git管理外)に保存する。新しいPCでは`.env.example`をコピーして、パスワードマネージャー等の安全な経路で受け取った値を入力すること。

**どのサイトに投稿するかは記事の文脈で判断する**: トレンド記事→chomoand.com、オーディション記事→chomoand-0.com、コイキーズ記事→chomoand-1.com。

## REST API

- 投稿: `POST {サイトURL}/wp-json/wp/v2/posts`
- メディアアップロード: `POST {サイトURL}/wp-json/wp/v2/media`
- 更新(公開に変更など): `POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}`
- 認証方式: Basic認証(`username:アプリパスワード`をUTF-8でBase64エンコードし`Authorization: Basic ...`ヘッダーに設定)
- テーマ: 両サイトともSWELLテーマを使用。同じCSSクラス(`swell-block-capbox`・`swl-marker`・`is-style-dent_box`など)がそのまま使える。

## 運用ルール(絶対厳守)

- **記事(投稿・固定ページ問わず)の削除・ゴミ箱移動は絶対に行わない**。DELETEメソッドや`wp post delete`などの削除系コマンドは実行しない。更新が必要な場合もPUT/PATCH(更新)のみ使用し、削除は提案もしない。
  - Why: ユーザーが「絶対に記事は勝手に消さない事」と明示的に指示。誤削除のリスクをゼロにしたい強い意図がある。
- 投稿はまず`status: draft`(下書き)で作成し、ユーザーが確認したうえで公開する([publishスキル](../.claude/skills/publish/SKILL.md)参照)。
- **「確認したい」「見れないから一度アップして」は「公開して」ではない。** 下書きが見れないという相談を「publishにすれば見れる」と解釈して勝手に公開しない。「公開して」と明示されない限りstatusはdraftのまま維持し、確認方法(wp-adminにログインしてプレビュー等)を案内する。2026-07-04にこれで一度勝手に公開してしまい、ユーザーから訂正が入った。
- WordPressの設定変更(プラグイン・テーマ・サイト設定など)は必ずユーザーに確認してから行う。
- Read/下書き投稿/更新/リライトは確認不要で実行してよい。DELETE・設定変更のみ確認が必要。
- **下書き記事の内容を`POST {サイトURL}/wp-json/wp/v2/posts/{id}`で更新するときは、`status`フィールドを必ず明示的に含める(`{"status":"draft", "content":...}`)。** `content`だけ送ってstatusを省略すると、既存の下書きが`publish`(公開)状態にリセットされてしまう事象を2026-07-10に確認した。下書き中の記事を編集する処理では省略せず、常に`status: draft`をペイロードに含めること。

## サイトマップに関する既知の問題

サイトマッププラグインが2個入っていて競合・不具合が発生していたため削除対応済み。今後サイトマップ関連の作業をする際は、プラグインが1個だけになっているか確認し、再度2個入れないよう注意する。

## 既知の問題: gen_eyecatch_batch.pyの秘密情報ハードコード

`gen_eyecatch_batch.py`(リポジトリ直下)にWP_TREND_URL/WP_USER/WP_PASS(実際のアプリパスワード)が平文でハードコードされたままGit管理下にある(2026-07-03時点で確認、初回コミットから存在)。`.env`は`.gitignore`済みだが、このファイルだけ素通しになっている。プライベートリポジトリではあるが複数人・複数PC共有のため、今後このファイルを触る機会があれば`wp_upload_batch.py`と同様に`.env`からの読み込み方式に直し、ハードコードされた値を削除するのが望ましい。気づいた時点でこの注記だけ残し、指示なく秘密情報を含むファイルの修正・コミットはしないこと。

## Search Console

公開後のURLをGoogle Search Consoleに登録する作業は、API連携が複雑なためユーザーが手動で行う。松/Codexは公開とURL表示までを担当する。
