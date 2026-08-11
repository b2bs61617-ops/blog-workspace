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
  - テーブル(`|...|`)→ `<table><tbody><tr><td>` に変換。罫線・背景色は必ずインラインstyleで直接指定する([docs/rules.mdの表のスタイルルール](../../../docs/rules.md)参照。class頼みだと罫線が表示されないことがある)
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
- **テーブル(`|...|`)は上記の「SWELL独自装飾」には含めない。`<!-- wp:table -->`のコアブロックとして変換する**(2026-08-02判明): `<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>...</tbody></table></figure>`という形にし、`<!-- wp:html -->`では囲まない。既存の公開済み記事(例:chomoand-0.com ID184「けるとめる」)の実データを確認したところ全てこの形式で、SWELL側の`.wp-block-table`用CSSが効いて列幅が均等に割り付けられ見やすく表示される。一方`<!-- wp:html -->`で生の`<table><tbody>`をそのまま囲むと、SWELLの表スタイルが当たらず列幅が詰まって読みにくくなる不具合を確認した(松田元太の私服特定記事で「表が見づらい」とユーザーから指摘され判明)。
  - Why: STEP1.5導入時は表もSWELL独自装飾の一種として`wp:html`で無難に囲む方針にしていたが、実際にはコアの`wp:table`ブロックのマークアップ(`wp-block-table`クラス+`has-fixed-layout`)がそのまま使えており、既存記事は全てその形式だった。
  - How to apply: 記事に表を入れるときは`<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>...(各行<tr><td>...</td>...</tr>、見出し行も他行と同じ<td>でよい)...</tbody></table></figure>\n<!-- /wp:table -->`の形式で組み立てる。

**初回運用時の確認**: このルールは実際にSWELLのブロック仕様を検証した上でのものではなく、標準的なGutenbergブロックコメント構文に基づく最善の推測。次にこのSTEPを使って記事を投稿したら、`context=edit`でPOST後の`content.raw`を確認し、可能であればユーザーに管理画面のブロックエディタで開いて崩れ(「不正なコンテンツ」警告など)が出ていないか確認してもらう。問題があればこのSTEPのルールを修正する。

**既知の不具合(2026-08-06判明、2026-08-11にchomoand-1.comでも確認): `swell-block-capbox`が`<!-- wp:html -->`内だと無枠で表示される**。宮近海斗のApple Watch記事(chomoand-0.com記事ID428)で、`is-style-small_ttl`・`is-style-onborder_ttl`のどちらも、タイトル行+本文が枠線・背景色なしのただのプレーンテキストとして表示される不具合をユーザーがプレビュー画面で確認・報告した。SWELLのcapbox用CSS/JSが、実際の`swell/capbox`ブロックがページ内に存在する場合のみ読み込まれ、`wp:html`(カスタムHTMLブロック)経由で流し込んだ生divには適用されない可能性が高い。**2026-08-11、KO1KEYZの部屋割り予想記事(chomoand-1.com記事ID11122/11125)でも同じ無枠表示になることをユーザーが確認**しており、chomoand-0.com限定の不具合ではなく両サイト(SWELLテーマ共通)の問題と判明した。
- **回避策**: capbox風の見た目が欲しい箇所は、クラス名(`swell-block-capbox`等)に頼らず、`<div style="border:1px solid #ddd;border-left:4px solid {アクセント色};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f7f7;">`のようなインラインstyleで直接枠・背景を指定する(タイトル部分は`<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">`)。タイトルバー型(見出し行に背景色を敷くパターン)も同様に`<p style="...;padding:10px 18px;background:{アクセント色};color:#fff;">`+その下に`<ul>`/`<div>`をインラインstyleで続ける形にする。表(`swl-marker`ではなくtable)側で既にインラインstyle方式に切り替え済みなのと同じ考え方。KO1KEYZ記事でアクセント色を選ぶときは[docs/rules.mdの「UIボックスのアクセントカラーはメンバーカラーと被らせない」](../../../docs/rules.md#uiボックスのアクセントカラーはメンバーカラーと被らせないko1keyz2026-08-11追加)を参照。
- **How to apply**: chomoand-0.com・chomoand-1.comどちらでも、新しくcapboxを使う記事を書くときは最初からこのインラインstyle版を使う(クラスベースの`swell-block-capbox`は`wp:html`経由では使わない)。もし将来的にクラスベースで正常表示されるケースを確認できたら(テーマ側の対応が入った等)、この回避策の要否を見直す。

## STEP 2: スラッグの生成

- Google翻訳API(client=gtx)でタイトルを英語に翻訳: `https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={encoded_title}`
- 英語テキストをスラッグ化: 小文字に変換 → 記号除去(英数字・スペース・ハイフン以外) → スペースをハイフンに置換 → 連続ハイフンを1つに統合 → 先頭から30文字で切り捨て(末尾ハイフンも除去)
- 例:「並木雲楓に彼氏はいる?…」→ `does-kaede-namiki-have-a-boyfr`

## STEP 3: WordPressに下書き投稿

- エンドポイント: `POST {サイトURL}/wp-json/wp/v2/posts`
- 投稿データ: `title`・`content`(HTML)・`slug`(STEP2)・`status: draft`・`categories`(サイト・カテゴリに応じて設定)・`author`(作業中のPCのhostnameから[docs/wordpress.mdの投稿者設定表](../../../docs/wordpress.md)を引いて該当ユーザーIDを設定。省略するとサイトの認証ユーザー本人が投稿者になってしまうため必須)
- 投稿成功後、**記事ID**を控える(STEP5で使用)

**【重要】PowerShell 5.1でJSONを組み立てる際の注意:**
- `Get-Content -Raw`はFileInfoオブジェクトを返すため`ConvertTo-Json`すると`{"value":"...","ReadCount":1}`になる。必ず`[string]`キャストを使う: `$content = [string](Get-Content "path" -Raw -Encoding UTF8)`
- HTMLの`<>`が`<`等にエスケープされるため送信前に戻す: `-replace '\\u003c','<' -replace '\\u003e','>' -replace '\\u0026','&'`
- JSONは手動組み立て: `$json = "{\"title\":$jTitle,\"content\":$jContent,...}"`
- 送信は`[System.Text.Encoding]::UTF8.GetBytes($json)`でバイト列化してから`Invoke-RestMethod -Body`に渡す
- Python(`wp_upload_batch.py`)を使う場合は`.env`から`WP_<SITE>_URL`等を読み込む実装済みなのでそのまま使える

## STEP 3.5: SNS投稿文の作成(コイキーズ限定・試験導入、2026-08-11〜)

Facebook/Instagram/Threadsへの自動投稿(publishスキルからJetpack Socialが実行)で使われる投稿文をカスタマイズする。未設定のままだとWordPressが本文の先頭を機械的に切っただけの文(自動抜粋)が使われてしまうため、記事内容を踏まえてマツが100〜140字程度の簡潔な要約文を作成する。

- 要約文は記事の結論・一番の見どころを冒頭に置き、タイトルの言い換えで終わらせない(タイトルはSNS投稿の別枠で自動的に見えるプラットフォームもあるため、要約文自体に情報量を持たせる)
- 絵文字は使わない([docs/rules.md](../../../docs/rules.md)の文体ルールに準拠)
- STEP3の投稿データに`meta`フィールドとして含める: `{ ..., "meta": { "jetpack_publicize_message": "{要約文}" } }`(STEP3のPOST時に一緒に送るか、STEP3完了後に記事IDへ`POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}` ボディ`{ "meta": { "jetpack_publicize_message": "{要約文}" } }`で追送してもよい)
- 試験導入としてコイキーズのみ対象。他2サイトはこの後の動作確認次第で拡大する

## STEP 4: アイキャッチ画像の生成

- **chomoand-1.com(コイキーズブログ)は、記事本文中に[画像埋め込みルール](../../../docs/rules.md#画像埋め込みルール必ずxの画像を使う2026-07-27にユーザー指示)で埋め込んだ写真があれば、その中で本文中に最初に登場する1枚をfeatured_mediaとして使う(2026-08-11〜、SNS自動投稿の画像をブランド統一グラフィックではなく記事内の実写真にする方針変更。試験導入としてコイキーズのみ対象、他2サイトはこの後の動作確認次第で拡大)。その写真はSTEP1で画像埋め込みルールに従いWordPressメディアライブラリへアップロード済みのため、**新たに画像を生成・アップロードする必要はない**。既に控えてあるそのメディアIDをそのままSTEP5で使う
  - **本文中に使える写真が1枚もない記事(文章のみのwiki記事など)は、従来通り`tools/eyecatch_koikeyz.py`で生成する**(2026-07-24〜「アイキャッチを作らない」方針だったが、2026-07-30にSNS自動投稿(Instagram/Jetpack Social)の画像必須要件のため方針終了・復活。詳細は[docs/sns-auto-post-setup.md](../../../docs/sns-auto-post-setup.md)参照)。使い方は`tools/eyecatch_koikeyz.py`のdocstring参照(`--top`/`--main`/`--bottom`/`--out`)
- **chomoand.comの記事は必ずCanva MCPで作る**(2026-07-16〜、[docs/canva-mcp-chomoand.md](../../../docs/canva-mcp-chomoand.md)の運用フローに従う)。要点:
  - 専用マスターデザイン(design_id: `DAHPjgiBOTI`、1ページのみ)を`copy-design`で複製する(`page_numbers`指定不要)
  - 3つの独立したテキスト要素(1行目=番組名/2行目=出演者名/3〜4行目=疑問形+補足)を`replace_text`で置換する(KO1KEYZと違い要素が分かれているのでフォントサイズが飛ぶ心配はない)
  - **背景のブラシストロークを毎回ランダムな色に差し替える**(KO1KEYZと同じアセット一覧を使い回せる)
  - `export-design`で1200×675のPNGにして`images/`に保存
  - Canva MCPが使えないときのフォールバックは[docs/eyecatch-style.md](../../../docs/eyecatch-style.md)の汎用テンプレ(1200×630px)
- chomoand-0.comのデザイン仕様は[docs/eyecatch-style.md](../../../docs/eyecatch-style.md)参照(1200×630px)
- 保存先: `images/{ファイル名}_eyecatch.png`

## STEP 5: アイキャッチをWordPressにアップロード・設定

- **STEP4で記事内の写真を使うことになった場合(コイキーズ・写真ありの記事)**: 新規アップロードは不要。STEP1で取得済みのそのメディアIDをそのままSTEP3の記事に設定: `POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}` ボディ `{ "featured_media": メディアID }`
- **STEP4で生成アイキャッチを使うことになった場合(それ以外)**: 画像をバイナリで読み込み、`POST {サイトURL}/wp-json/wp/v2/media`にアップロード(`Content-Type: image/png`、`Content-Disposition: attachment; filename="xxx.png"`)。取得した**メディアID**をSTEP3の記事に設定: `POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}` ボディ `{ "featured_media": メディアID }`

## STEP 0(chomoand-1.com限定・作業開始時に1回): 韓国語版の抜け漏れチェック

chomoand-1.com向けにこのスキルを実行する**最初に**、`python tools/check_kr_translation_gaps.py`を実行し、過去の記事で韓国語版(下書き含む)が見つからないものがないか確認する。STEP6は同一セッション内の続き処理として動くため、途中で中断すると気づかれないまま韓国語版が抜けることがある(詳細は[docs/korea-expansion.md](../../../docs/korea-expansion.md)の「なぜ抜け漏れが起きるか」参照)。抜け漏れが見つかったら、新規記事の作業に入る前にSTEP6相当の処理(元記事取得→韓国語ローカライズ→下書き投稿)で先に埋める。

## STEP 6(chomoand-1.com限定): 韓国語版下書きの自動生成

コイキーズブログ(chomoand-1.com)の記事は、STEP3完了後に**確認なしで自動的に**韓国語版の下書きも作成する(2026-07-19〜、トモキ指示)。ローカライズの方法・Polylangの`lang`/`translations`フィールドの使い方は[docs/korea-expansion.md](../../../docs/korea-expansion.md)を参照。**韓国語版も日本語版と同じアイキャッチ画像をfeatured_mediaに設定する**(2026-07-30〜、日本語版のアイキャッチ復活に合わせて変更)。chomoand.com・chomoand-0.comの記事にはこのSTEPは適用しない。STEP6を終えたら、slugが元記事の`-kr`命名規則に従っていることを確認する(次回以降のSTEP0の突き合わせに必要)。

## 完了報告

全STEP終了後、以下をユーザーに報告する:
- 記事ID・スラッグ・確認URL(`{サイトURL}/?p={id}`)
- アイキャッチ画像のメディアID(chomoand-1.com以外)
- (chomoand-1.comの場合)韓国語下書きのID・スラッグ

**How to apply:** 「ブログにアップして」「アップして」「WordPressに反映して」などの発言をトリガーとしてSTEP1〜6を順番に実行する。STEP1.5(ブロック変換)は全サイト共通で必ず行う。chomoand-1.comはSTEP0(セッション最初の1回のみ)→STEP1→STEP1.5→STEP2→STEP3→STEP3.5(SNS投稿文)→STEP4→STEP5→STEP6、それ以外のサイトはSTEP1→STEP1.5→STEP2〜5(STEP3.5は現状コイキーズ限定)。記事の削除は絶対に行わない([docs/wordpress.md](../../../docs/wordpress.md))。公開自体は別途[publishスキル](../publish/SKILL.md)で行う。公開後の自動SNS投稿(Facebook/Instagram/Threads=Jetpack Social・X=手動運用)の仕組みは[docs/sns-auto-post-setup.md](../../../docs/sns-auto-post-setup.md)参照。
