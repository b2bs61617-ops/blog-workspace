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
  - 冒頭の`<!-- TITLE: ... -->`・`<!-- KEYWORDS: ... -->`・`<!-- STRUCTURE: ... -->`コメント([docs/rules.mdの記録ルール](../../../docs/rules.md)参照)も本文から除去してから投稿する
  - `## ` → `<h2>`、`### ` → `<h3>`
  - `---` → `<hr>`
  - `**text**` → `<strong>text</strong>`
  - テーブル(`|...|`)→ `<table><tbody><tr><td>` に変換
  - 通常段落 → `<p>`タグで囲む(句点で`<br>`改行、[docs/rules.md](../../../docs/rules.md)参照)
  - SNS由来の画像を記事に埋め込む場合は[docs/rules.mdの画像埋め込みルール](../../../docs/rules.md)に従う(メディアライブラリの自動生成サイズ+`max-width:100%`でレスポンシブにする、`<figcaption>`で出典を明記する)。絵文字は使わない。

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

## STEP 4: アイキャッチ画像の生成

- **chomoand-1.com(コイキーズブログ)の記事は必ずCanva MCPで作る**([docs/canva-mcp.md](../../../docs/canva-mcp.md)の運用フローに従う)。サイト全記事がトモキのCanvaテンプレの見た目で揃っているため、勝手に別デザインを作らないこと。要点:
  - 元デザイン`DAG_zqaJE_8`の**ページ36だけ**を`copy-design`で複製する(他ページは`find_and_replace_text`がサイレント失敗するので使わない)
  - 4行のテキストを`find_and_replace_text`で**行ごとに1回ずつ**置換する(`replace_text`はフォントサイズが飛ぶので禁止)
  - **背景のブラシストロークを毎回ランダムな色に差し替える**(`update_fill` + `resize_element`/`position_element`)。サイトのアイキャッチは全記事で色が違うのが売りなので、**色替えは必須**(2026-07-15トモキ指示)
  - `export-design`で1200×675のPNGにして`images/`に保存
  - Canva MCPが認証切れ等で使えないときだけ、フォールバックとして`python tools/eyecatch_koikeyz.py`(HTML再現版・フォントが別物)を使う
- **chomoand.comの記事も必ずCanva MCPで作る**(2026-07-16〜、[docs/canva-mcp-chomoand.md](../../../docs/canva-mcp-chomoand.md)の運用フローに従う)。要点:
  - 専用マスターデザイン(design_id: `DAHPjgiBOTI`、1ページのみ)を`copy-design`で複製する(`page_numbers`指定不要)
  - 3つの独立したテキスト要素(1行目=番組名/2行目=出演者名/3〜4行目=疑問形+補足)を`replace_text`で置換する(KO1KEYZと違い要素が分かれているのでフォントサイズが飛ぶ心配はない)
  - **背景のブラシストロークを毎回ランダムな色に差し替える**(KO1KEYZと同じアセット一覧を使い回せる)
  - `export-design`で1200×675のPNGにして`images/`に保存
  - Canva MCPが使えないときのフォールバックは[docs/eyecatch-style.md](../../../docs/eyecatch-style.md)の汎用テンプレ(1200×630px)
- chomoand-0.comのデザイン仕様は[docs/eyecatch-style.md](../../../docs/eyecatch-style.md)参照(1200×630px)
- 保存先: `images/{ファイル名}_eyecatch.png`

## STEP 5: アイキャッチをWordPressにアップロード・設定

- 画像をバイナリで読み込み、`POST {サイトURL}/wp-json/wp/v2/media`にアップロード(`Content-Type: image/png`、`Content-Disposition: attachment; filename="xxx.png"`)
- 取得した**メディアID**をSTEP3の記事に設定: `POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}` ボディ `{ "featured_media": メディアID }`

## 完了報告

全STEP終了後、以下をユーザーに報告する:
- 記事ID・スラッグ・確認URL(`{サイトURL}/?p={id}`)
- アイキャッチ画像のメディアID

**How to apply:** 「ブログにアップして」「アップして」「WordPressに反映して」などの発言をトリガーとしてSTEP1〜5を順番に実行する。記事の削除は絶対に行わない([docs/wordpress.md](../../../docs/wordpress.md))。公開自体は別途[publishスキル](../publish/SKILL.md)で行う。
