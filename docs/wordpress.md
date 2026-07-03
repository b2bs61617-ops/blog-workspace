# WordPress接続・運用ルール

## サイト一覧

| サイト | URL | 用途 | 認証情報(.envのキー) |
|---|---|---|---|
| トレンドブログ | https://chomoand.com | 時事・話題の記事 | `WP_TREND_URL` / `WP_TREND_USERNAME` / `WP_TREND_APP_PASSWORD` |
| ジャニオタブログ | https://chomoand-0.com | オーディション番組系の記事 | `WP_AUDITION_URL` / `WP_AUDITION_USERNAME` / `WP_AUDITION_APP_PASSWORD` |
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
- WordPressの設定変更(プラグイン・テーマ・サイト設定など)は必ずユーザーに確認してから行う。
- Read/下書き投稿/更新/リライトは確認不要で実行してよい。DELETE・設定変更のみ確認が必要。

## サイトマップに関する既知の問題

サイトマッププラグインが2個入っていて競合・不具合が発生していたため削除対応済み。今後サイトマップ関連の作業をする際は、プラグインが1個だけになっているか確認し、再度2個入れないよう注意する。

## Search Console

公開後のURLをGoogle Search Consoleに登録する作業は、API連携が複雑なためユーザーが手動で行う。松/Codexは公開とURL表示までを担当する。
