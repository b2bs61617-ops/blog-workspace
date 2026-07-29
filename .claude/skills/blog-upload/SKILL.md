---
name: blog-upload
description: 「ブログにアップして」「アップして」「WordPressに反映して」と言われたときに使う。記事のHTML変換からWordPress下書き投稿・アイキャッチ生成・設定までを一括実行する。
---

# ブログアップロードスキル

「ブログにアップして」と言われたら以下を順番に全て実行する。投稿先サイトは[docs/wordpress.md](../../../docs/wordpress.md)の判断基準(トレンド記事→chomoand.com、オーディション記事→chomoand-0.com、コイキーズ記事→chomoand-1.com)に従い、対応する`.env`の`WP_<SITE>_URL` / `WP_<SITE>_USERNAME` / `WP_<SITE>_APP_PASSWORD`を使う。

## STEP 1: 記事ファイルの読み込み・HTML変換

- `articles/` 配下の対象`.md`ファイルを読み込む
- マークダウン→HTML変換ルール:
  - H1(タイトル行)は除去(WordPressの`title`フィールドで設定するため)
  - `## ` → `<h2>`、`### ` → `<h3>`
  - `---` → `<hr>`
  - `**text**` → `<strong>text</strong>`
  - テーブル(`|...|`)→ `<table><tbody><tr><td>` に変換
  - 通常段落 → `<p>`タグで囲む(句点で`<br>`改行、[docs/rules.md](../../../docs/rules.md)参照)
  - SNS由来の画像を記事に埋め込む場合は[docs/rules.mdの画像埋め込みルール](../../../docs/rules.md)に従う(メディアライブラリの自動生成サイズ+`max-width:100%`でレスポンシブにする、`<figcaption>`で出典を明記する)。絵文字は使わない。

## STEP 1.5: Gutenbergブロック形式への変換(全サイト共通、2026-07-27〜、2026-07-29に全サイトへ拡大)

**すべてのサイト(chomoand.com・chomoand-0.com・chomoand-1.com)の記事で、STEP3でPOSTする前に必ずこのSTEPを行う。**

背景: STEP1で作るcontentが素のHTMLタグ(`<p>`・`<h2>`・`<div class="swell-block-capbox">`など)を並べただけでGutenbergのブロックコメント(`<!-- wp:xxx -->`)が付いていないと、フロント表示自体はSWELLのCSSクラスで崩れないが、**記事途中への広告差し込みが機能しない**(広告はブロックの区切りに挿入される仕組みのため、ブロックコメントがないと1個の塊として扱われ、途中に広告が出ない)。当初コイキーズ限定で対応していたが、2026-07-29にジャニオタブログ(chomoand-0.com)でも同じ問題が確認されたため、全サイト共通のSTEPに変更した。

変換ルール(素のHTML→ブロックコメント付き):
- `<h2 class="wp-block-heading">...</h2>` → `<!-- wp:heading -->` と `<!-- /wp:heading -->` で挟む
- `<h3 class="wp-block-heading">...</h3>` → `<!-- wp:heading {"level":3} -->` と `<!-- /wp:heading -->` で挟む
- 装飾クラスなしの通常`<p>...</p>` → `<!-- wp:paragraph -->` と `<!-- /wp:paragraph -->` で挟む
- `<hr>` → `<!-- wp:separator --><hr class="wp-block-separator has-alpha-channel-opacity"/><!-- /wp:separator -->` に置き換え
- **SWELL独自の装飾HTML(`swell-block-capbox`のdiv、`is-style-dent_box`/`is-style-onborder_ttl`などのスタイル付き`<p>`、`swl-marker`の`<span>`、Googleマップiframe埋め込み、画像`<figure>`+`<figcaption>`など)は、正確なブロックJSON仕様(SWELL側の実際のブロック登録定義)が不明なため無理にコアブロックへ変換しない。まとまりごと`<!-- wp:html -->` 〜 `<!-- /wp:html -->` で囲む**(WordPressの「カスタムHTML」ブロックとして扱われ、見た目は今までと変わらず、かつ常に有効なブロックとして保存される。ブロックエディタ上では生HTMLとして編集する形になる)。

**初回運用時の確認**: このルールは実際にSWELLのブロック仕様を検証した上でのものではなく、標準的なGutenbergブロックコメント構文に基づく最善の推測。次にこのSTEPを使って記事を投稿したら、`context=edit`でPOST後の`content.raw`を確認し、可能であればユーザーに管理画面のブロックエディタで開いて崩れ(「不正なコンテンツ」警告など)が出ていないか確認してもらう。問題があればこのSTEPのルールを修正する。

## STEP 2: スラッグの生成

- Google翻訳API(client=gtx)でタイトルを英語に翻訳: `https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={encoded_title}`
- 英語テキストをスラッグ化: 小文字に変換 → 記号除去(英数字・スペース・ハイフン以外) → スペースをハイフンに置換 → 連続ハイフンを1つに統合 → 先頭から30文字で切り捨て(末尾ハイフンも除去)
- 例:「並木雲楓に彼氏はいる?…」→ `does-kaede-namiki-have-a-boyfr`

## STEP 3: WordPressに下書き投稿

- エンドポイント: `POST {サイトURL}/wp-json/wp/v2/posts`
- 投稿データ: `title`・`content`(HTML)・`slug`(STEP2)・`status: draft`・`categories`(サイト・カテゴリに応じて設定)
- 投稿成功後、**記事ID**を控える(STEP5で使用)

**【重要】PowerShell 5.1でJSONを組み立てる際の注意:**
- `Get-Content -Raw`はFileInfoオブジェクトを返すため`ConvertTo-Json`すると`{"value":"...","ReadCount":1}`になる。必ず`[string]`キャストを使う: `$content = [string](Get-Content "path" -Raw -Encoding UTF8)`
- HTMLの`<>`が`<`等にエスケープされるため送信前に戻す: `-replace '\\u003c','<' -replace '\\u003e','>' -replace '\\u0026','&'`
- JSONは手動組み立て: `$json = "{\"title\":$jTitle,\"content\":$jContent,...}"`
- 送信は`[System.Text.Encoding]::UTF8.GetBytes($json)`でバイト列化してから`Invoke-RestMethod -Body`に渡す
- Python(`wp_upload_batch.py`)を使う場合は`.env`から`WP_<SITE>_URL`等を読み込む実装済みなのでそのまま使える

## STEP 4: アイキャッチ画像の生成(chomoand-1.comは対象外)

- **chomoand-1.com(コイキーズブログ)の記事はアイキャッチを作らない**(2026-07-24〜トモキ指示。それまではCanva MCP必須だったが方針転換)。STEP4・STEP5・STEP6内のアイキャッチ関連処理はすべてスキップし、STEP3の下書き投稿だけで完了とする。
- **chomoand.comの記事は必ずCanva MCPで作る**(2026-07-16〜、[docs/canva-mcp-chomoand.md](../../../docs/canva-mcp-chomoand.md)の運用フローに従う)。要点:
  - 専用マスターデザイン(design_id: `DAHPjgiBOTI`、1ページのみ)を`copy-design`で複製する(`page_numbers`指定不要)
  - 3つの独立したテキスト要素(1行目=番組名/2行目=出演者名/3〜4行目=疑問形+補足)を`replace_text`で置換する(KO1KEYZと違い要素が分かれているのでフォントサイズが飛ぶ心配はない)
  - **背景のブラシストロークを毎回ランダムな色に差し替える**(KO1KEYZと同じアセット一覧を使い回せる)
  - `export-design`で1200×675のPNGにして`images/`に保存
  - Canva MCPが使えないときのフォールバックは[docs/eyecatch-style.md](../../../docs/eyecatch-style.md)の汎用テンプレ(1200×630px)
- chomoand-0.comのデザイン仕様は[docs/eyecatch-style.md](../../../docs/eyecatch-style.md)参照(1200×630px)
- 保存先: `images/{ファイル名}_eyecatch.png`

## STEP 5: アイキャッチをWordPressにアップロード・設定(chomoand-1.comは対象外)

- 画像をバイナリで読み込み、`POST {サイトURL}/wp-json/wp/v2/media`にアップロード(`Content-Type: image/png`、`Content-Disposition: attachment; filename="xxx.png"`)
- 取得した**メディアID**をSTEP3の記事に設定: `POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}` ボディ `{ "featured_media": メディアID }`

## STEP 6(chomoand-1.com限定): 韓国語版下書きの自動生成

コイキーズブログ(chomoand-1.com)の記事は、STEP3完了後に**確認なしで自動的に**韓国語版の下書きも作成する(2026-07-19〜、トモキ指示)。ローカライズの方法・Polylangの`lang`/`translations`フィールドの使い方は[docs/korea-expansion.md](../../../docs/korea-expansion.md)を参照。**韓国語版もアイキャッチは作らない**(2026-07-24〜)。chomoand.com・chomoand-0.comの記事にはこのSTEPは適用しない。

## 完了報告

全STEP終了後、以下をユーザーに報告する:
- 記事ID・スラッグ・確認URL(`{サイトURL}/?p={id}`)
- アイキャッチ画像のメディアID(chomoand-1.com以外)
- (chomoand-1.comの場合)韓国語下書きのID・スラッグ

**How to apply:** 「ブログにアップして」「アップして」「WordPressに反映して」などの発言をトリガーとしてSTEP1〜6を順番に実行する。STEP1.5(ブロック変換)は全サイト共通で必ず行う。chomoand-1.comはSTEP1→STEP1.5→STEP2→STEP3→STEP6(STEP4・5はスキップ)、それ以外のサイトはSTEP1→STEP1.5→STEP2〜5。記事の削除は絶対に行わない([docs/wordpress.md](../../../docs/wordpress.md))。公開自体は別途[publishスキル](../publish/SKILL.md)で行う。
