# WordPress接続・運用ルール

## サイト一覧

| サイト | URL | 用途 | 認証情報(.envのキー) |
|---|---|---|---|
| 恋リアブログ | https://chomoand.com | **恋愛リアリティ番組の出演者wiki**(2026-07-14〜)。旧「トレンドブログ」。`.env`のキー名は`WP_TREND_*`のまま(改名すると全PCの`.env`更新が必要なため据え置き) | `WP_TREND_URL` / `WP_TREND_USERNAME` / `WP_TREND_APP_PASSWORD` |
| ジャニオタブログ | https://chomoand-0.com | ジャニーズ系記事全般(オーディション番組系だけでなく、グループ・メンバー個人の話題・ファンクラブ情報なども含む) | `WP_AUDITION_URL` / `WP_AUDITION_USERNAME` / `WP_AUDITION_APP_PASSWORD` |
| コイキーズブログ | https://chomoand-1.com | コイキーズ関連の記事 | `WP_KOIKEYS_URL` / `WP_KOIKEYS_USERNAME` / `WP_KOIKEYS_APP_PASSWORD` |

ユーザー名はどのサイトも共通(`b2bs61617@gmail.com`)。実際のアプリパスワードの値は`.env`(このリポジトリ直下、Git管理外)に保存する。新しいPCでは`.env.example`をコピーして、パスワードマネージャー等の安全な経路で受け取った値を入力すること。

**どのサイトに投稿するかは記事の文脈で判断する**: 恋愛リアリティ番組の出演者記事→chomoand.com、ジャニーズ系記事→chomoand-0.com、コイキーズ記事→chomoand-1.com。

## カテゴリID(判明分)

`GET {サイトURL}/wp-json/wp/v2/categories?per_page=50`で確認できる。投稿時に迷ったら都度確認すればよいが、chomoand-1.com(コイキーズブログ)は以下が判明済み(2026-07-14):

| ID | 名前 |
|---|---|
| 66 | KO1KEYZ |
| 62 | まとめ |
| 10 | wiki |
| 11 | 学歴 |
| 12 | 家族構成 |
| 63 | 愛用品 |
| 4 | 日プ4 |

グループ・メンバー全体の話題(メンカラ・絵文字まとめなど)は`[66, 62]`(KO1KEYZ+まとめ)を使うとよい。

### chomoand.com(恋リアブログ)

2026-07-14時点のカテゴリと記事数。**恋リア用のカテゴリはまだ無い**ので、1本目の投稿時に番組名カテゴリ(例:「今日、好きになりました。」)を新設する必要がある。

| ID | 名前 | 記事数 |
|---|---|---|
| 1 | 未分類 | 55 |
| 13 | 現役歌王 | 17 |
| 18 | DREAM STAGE | 17 |
| 17 | TAGRIGHT | 10 |
| 30 | トレンド | 8 |
| 16 | NAZE | 8 |
| 19 | TORINNER | 6 |
| 31 | キンパとおにぎり | 4 |
| 28 | WORLD SCOUT | 3 |
| 33 | Youtuber | 0 |
| 20 | ドラマ | 0 |

既存記事はオーディション番組系(現役歌王・DREAM STAGE・TAGRIGHTなど)が中心で、元々「番組出演者wiki」寄りの資産がある。恋リア転換はこの延長線上にあたる。既存記事は削除しない(そもそも削除は絶対厳守で禁止)。

## REST API

- 投稿: `POST {サイトURL}/wp-json/wp/v2/posts`
- メディアアップロード: `POST {サイトURL}/wp-json/wp/v2/media`
- 更新(公開に変更など): `POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}`
- プラグイン一覧取得: `GET {サイトURL}/wp-json/wp/v2/plugins`
- プラグインのインストール・有効化: `POST {サイトURL}/wp-json/wp/v2/plugins` に `{"slug": "プラグインのslug", "status": "active"}` をJSONで送る(WordPress.orgディレクトリのプラグインならZIPアップロード不要でスラッグ指定だけでインストールできる。2026-07-06、WP Sitemap Page導入時に確認)。ただしプラグインのインストール・有効化自体はサイト設定変更にあたるため、CLAUDE.mdのルール通り必ずユーザーに確認してから実行する。
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

- **2026-07-06に判明・対応**: 上記削除対応の際、固定ページ`/site_map/`(HTML形式の人間向けサイトマップ)で使っていた`[wp_sitemap_page]`ショートコードの提供元プラグインまで一緒に消えてしまい、ページ上にショートコード文字列がそのままプレーンテキスト表示される不具合が発生していた。検索エンジン向けのXMLサイトマップ(`sitemap_index.xml`等、Rank Math製)は影響を受けておらず常に正常だった。「WP Sitemap Page」プラグイン(REST API経由でインストール・有効化可能)を再導入して復旧。
  - Why: プラグイン整理は`/site_map/`ページの表示機能への影響も考慮しないと、意図せず別機能を巻き添えで壊すことがある。
  - How to apply: 今後サイトマップ関連でプラグインを触るときは、XMLサイトマップ(検索エンジン向け)とHTMLサイトマップページ(`/site_map/`、人間向け、`[wp_sitemap_page]`ショートコード)の両方の表示を確認すること。

## 既知の問題: gen_eyecatch_batch.pyの秘密情報ハードコード

`gen_eyecatch_batch.py`(リポジトリ直下)にWP_TREND_URL/WP_USER/WP_PASS(実際のアプリパスワード)が平文でハードコードされたままGit管理下にある(2026-07-03時点で確認、初回コミットから存在)。`.env`は`.gitignore`済みだが、このファイルだけ素通しになっている。プライベートリポジトリではあるが複数人・複数PC共有のため、今後このファイルを触る機会があれば`wp_upload_batch.py`と同様に`.env`からの読み込み方式に直し、ハードコードされた値を削除するのが望ましい。気づいた時点でこの注記だけ残し、指示なく秘密情報を含むファイルの修正・コミットはしないこと。

## Search Console

公開後のURLは、Google Indexing API経由で[publishスキル](../.claude/skills/publish/SKILL.md)が自動でインデックス登録をリクエストする(2026-07-09〜)。初回セットアップ手順・API利用上の注意点は[docs/google-indexing-setup.md](google-indexing-setup.md)参照。`tools/google_indexing.py`が実体。

### chomoand-0.comのインデックス未登録問題(2026-07-07調査)

GSCで「ページがインデックスに登録されていない(noindexタグ/404/4xx/403)」という警告が出た件を調査した記録。

- **調査手法**: REST API(`?status=trash`や`?status=publish`を`context=edit`で叩く)で投稿・固定ページの件数を確認。各公開URLのHTMLをcurlで取得してmeta robotsタグ・canonical・X-Robots-Tagヘッダー・Googlebot UAでの応答コードを確認。`site:chomoand-0.com`のWeb検索でインデックス実態を確認。
- **判明した事実**:
  - 投稿36件+固定ページ3件、計39件がゴミ箱(trash)ステータスになっていた(2026-06-17〜2026-07-05にかけて複数回に分けて実施された形跡)。これが404警告の主因。ユーザーに確認したところ**復元は不要**とのことで、意図した状態(このまま放置でよい)。
  - 現在の公開記事はわずか5件のみ。各記事にnoindexタグ・403ブロックなどの技術的な問題は無し(正常にインデックス可能な状態)。
  - にもかかわらず`site:chomoand-0.com`は検索結果0件 = サイト全体がGoogleにまだインデックスされていない。
  - サイト自体が新しい(WordPress初期投稿「Hello world!」の作成日が2026-06-11で、開設から1ヶ月未満)。
- **結論**: 技術的なバグではなく、①新規ドメインでまだGoogleの信頼が無い、②公開記事数が少なすぎる、③公開→ゴミ箱移動を短期間で繰り返した履歴がクロール評価に悪影響、の複合要因と推測される。GSCの「インデックス登録をリクエスト」を毎日連打しても改善しない(むしろ逆効果の可能性)。
  - **How to apply**: 同様の「インデックスされない」相談が来たら、まず個別記事のnoindex/403/canonicalを技術チェックしたうえで、ドメインの新しさ・公開記事数・ゴミ箱移動履歴も確認すること。技術的に問題が無ければ「時間と実績が必要な状態」であることをユーザーに伝え、インデックス登録リクエストの連打はやめて記事を継続的に増やすよう案内する。

## SNS自動連携(記事公開時にX/Instagram/Threadsへ自動投稿したい場合)

2026-07-05にユーザーから相談があり調査した内容。3サイトとも同じ構成で使える。

- **Instagram・Threads**: WordPress.com公式の「Jetpack Social」で自動投稿できる。WordPress.com管理画面 →「設定」→「共有(Jetpack Social)」からInstagram Business/Threadsアカウントを接続すれば、記事公開時にタイトル+抜粋+アイキャッチ画像+リンクが自動シェアされる。
  - 注意: Instagramはアイキャッチ画像が必須(画像なしの記事は投稿不可)。1枚画像のみ対応で、複数画像のカルーセル投稿は不可。
- **X(旧Twitter)**: Jetpack Socialは2023年5月にX API規約・料金変更を理由に自動シェア機能を廃止しており、2026年現在も非対応(対応しているのはFacebook Pages・Instagram Business・Threads・LinkedIn・Bluesky・Nextdoor・Tumblr・Mastodonの8つでXは含まれない)。Xへの自動投稿はZapier/Make/IFTTTなど外部連携サービスで別途構築する必要がある(「WordPress New Post」トリガー→「X Create Tweet」アクション)。外部サービス側がAPI契約を持つため、ユーザー自身がX Developerアカウントを契約する必要はない。

**How to apply:** 記事公開時のSNS自動投稿について聞かれたら、Instagram/ThreadsはJetpack Social、XはZapier等の外部連携、という切り分けで案内する。
