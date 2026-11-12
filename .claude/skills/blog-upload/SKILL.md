---
name: blog-upload
description: 「ブログにアップして」「アップして」「WordPressに反映して」と言われたときに使う。記事のHTML変換からWordPress下書き投稿・アイキャッチ生成・設定までを一括実行する。
---

# ブログアップロードスキル

「ブログにアップして」と言われたら以下を順番に全て実行する。投稿先サイトは[docs/wordpress.md](../../../docs/wordpress.md)の判断基準(トレンド記事→chomoand.com、**SixTONES記事→chomoand-0.com**(2026-10-27〜)、コイキーズ記事→chomoand-1.com、**Travis Japan記事(2026-09-13以降の新規記事)→chomoand-4.blog**、**KEY TO LIT(キテレツ)記事→chomoand-5.site**、**Snow Man記事→chomoand-2.com**)に従い、対応する`.env`の`WP_<SITE>_URL` / `WP_<SITE>_USERNAME` / `WP_<SITE>_APP_PASSWORD`を使う(chomoand-4.blogは`WP_CHOMO4_*`、chomoand-5.siteは`WP_CHOMO5_*`、chomoand-2.comは`WP_CHOMO2_*`、chomoand-0.comは`WP_AUDITION_*`)。

## STEP 1: 記事ファイルの読み込み・HTML変換

- `articles/` 配下の対象`.md`ファイルを読み込む
- マークダウン→HTML変換ルール:
  - H1(タイトル行)は除去(WordPressの`title`フィールドで設定するため)
  - `## ` → `<h2>`、`### ` → `<h3>`
  - `---` → `<hr>`(ただしSTEP1.5で機械的に除去される場合がある。下記参照)
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
- `<hr>` → **記事中のどこに出てきても`wp:separator`に変換せず、`<hr>`ごと削除する(2026-08-16にリード文直後限定で導入、2026-08-18に記事全体へ適用範囲を拡大・確定)。** 見出し(`<h2>`)そのものがセクションの区切りとして機能するため、H2セクションの合間を含め、記事中に横線の区切りを一切表示しない方針になった。
  - Why: 当初は「リード文の直後の`<hr>`」だけがSWELLテーマの`.post_content hr`スタイル(`border-bottom:1px solid rgba(0,0,0,.1);margin:2.5em 0`)で薄い横線として表示され不要だと指摘されていた(2026-08-12)。執筆時の注意書きだけでは別セッション・別PCで同じ`---`が再発した(2026-08-16、ID11339/11341/11353)ため、STEP1.5の変換処理自体で機械的に弾く方式にした。さらに2026-08-18、KO1KEYZファンミFCブース記事(chomoand-1.com記事ID11468)で「各セクションの下にあるこれ、なくせる?」→「これは全記事書く際必ずの約束で」とユーザーから明言され、リード文直後に限らず記事中の全`<hr>`を対象に拡大した。
  - How to apply: STEP1.5を実行する際、変換対象のHTML中に登場する`<hr>`(または`---`)は位置を問わずすべて出力から取り除く(前後の段落・見出しはそのまま残す)。`wp:separator`ブロックへの変換は行わない。新規記事の執筆時点でも最初から`---`を書かないようにする。
- **SWELL独自の装飾HTML(`swell-block-capbox`のdiv、`is-style-dent_box`/`is-style-onborder_ttl`などのスタイル付き`<p>`、`swl-marker`の`<span>`、Googleマップiframe埋め込み、画像`<figure>`+`<figcaption>`など)は、正確なブロックJSON仕様(SWELL側の実際のブロック登録定義)が不明なため無理にコアブロックへ変換しない。まとまりごと`<!-- wp:html -->` 〜 `<!-- /wp:html -->` で囲む**(WordPressの「カスタムHTML」ブロックとして扱われ、見た目は今までと変わらず、かつ常に有効なブロックとして保存される。ブロックエディタ上では生HTMLとして編集する形になる)。
- **テーブル(`|...|`)は上記の「SWELL独自装飾」には含めない。`<!-- wp:table -->`のコアブロックとして変換する**(2026-08-02判明): `<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>...</tbody></table></figure>`という形にし、`<!-- wp:html -->`では囲まない。既存の公開済み記事(例:chomoand-0.com ID184「けるとめる」)の実データを確認したところ全てこの形式で、SWELL側の`.wp-block-table`用CSSが効いて列幅が均等に割り付けられ見やすく表示される。一方`<!-- wp:html -->`で生の`<table><tbody>`をそのまま囲むと、SWELLの表スタイルが当たらず列幅が詰まって読みにくくなる不具合を確認した(松田元太の私服特定記事で「表が見づらい」とユーザーから指摘され判明)。
  - Why: STEP1.5導入時は表もSWELL独自装飾の一種として`wp:html`で無難に囲む方針にしていたが、実際にはコアの`wp:table`ブロックのマークアップ(`wp-block-table`クラス+`has-fixed-layout`)がそのまま使えており、既存記事は全てその形式だった。
  - How to apply: 記事に表を入れるときは`<!-- wp:table -->\n<figure class="wp-block-table"><table class="has-fixed-layout"><tbody>...(各行<tr><td>...</td>...</tr>、見出し行も他行と同じ<td>でよい)...</tbody></table></figure>\n<!-- /wp:table -->`の形式で組み立てる。

**初回運用時の確認**: このルールは実際にSWELLのブロック仕様を検証した上でのものではなく、標準的なGutenbergブロックコメント構文に基づく最善の推測。次にこのSTEPを使って記事を投稿したら、`context=edit`でPOST後の`content.raw`を確認し、可能であればユーザーに管理画面のブロックエディタで開いて崩れ(「不正なコンテンツ」警告など)が出ていないか確認してもらう。問題があればこのSTEPのルールを修正する。

**既知の不具合(2026-08-06判明、2026-08-11にchomoand-1.comでも確認): `swell-block-capbox`が`<!-- wp:html -->`内だと無枠で表示される**。宮近海斗のApple Watch記事(chomoand-0.com記事ID428)で、`is-style-small_ttl`・`is-style-onborder_ttl`のどちらも、タイトル行+本文が枠線・背景色なしのただのプレーンテキストとして表示される不具合をユーザーがプレビュー画面で確認・報告した。SWELLのcapbox用CSS/JSが、実際の`swell/capbox`ブロックがページ内に存在する場合のみ読み込まれ、`wp:html`(カスタムHTMLブロック)経由で流し込んだ生divには適用されない可能性が高い。**2026-08-11、KO1KEYZの部屋割り予想記事(chomoand-1.com記事ID11122/11125)でも同じ無枠表示になることをユーザーが確認**しており、chomoand-0.com限定の不具合ではなく両サイト(SWELLテーマ共通)の問題と判明した。
- **回避策**: capbox風の見た目が欲しい箇所は、クラス名(`swell-block-capbox`等)に頼らず、`<div style="border:1px solid #ddd;border-left:4px solid {アクセント色};border-radius:4px;padding:14px 18px;margin:0 0 16px 0;background:#f7f7f7;">`のようなインラインstyleで直接枠・背景を指定する(タイトル部分は`<p style="font-weight:bold;font-size:1.05em;margin:0 0 8px 0;">`)。タイトルバー型(見出し行に背景色を敷くパターン)も同様に`<p style="...;padding:10px 18px;background:{アクセント色};color:#fff;">`+その下に`<ul>`/`<div>`をインラインstyleで続ける形にする。表(`swl-marker`ではなくtable)側で既にインラインstyle方式に切り替え済みなのと同じ考え方。KO1KEYZ記事でアクセント色を選ぶときは[docs/rules.mdの「UIボックスのアクセントカラーはメンバーカラーと被らせない」](../../../docs/rules.md#uiボックスのアクセントカラーはメンバーカラーと被らせないko1keyz2026-08-11追加)を参照。
- **How to apply**: chomoand-0.com・chomoand-1.comどちらでも、新しくcapboxを使う記事を書くときは最初からこのインラインstyle版を使う(クラスベースの`swell-block-capbox`は`wp:html`経由では使わない)。もし将来的にクラスベースで正常表示されるケースを確認できたら(テーマ側の対応が入った等)、この回避策の要否を見直す。

## STEP 1.55: 人名に「さん」を付ける(全サイト共通・必須、2026-10-25〜)

STEP1.5のあと、POSTする本文HTMLに`python tools/honorific.py fix --group {グループ} --names "メンバー以外の人名,カンマ区切り" 記事.html`をかけ、続けて`check`で抜けが0件なのを確認する(Snow Man=`snowman`、キテレツ=`ktl`、トラジャ=`travis`、KO1KEYZ=`ko1keyz`)。タイトル(`title`フィールド)・見出し・表・まとめの枠・「この記事でわかること」の枠には付けない(ツールが自動で除外し、付いていたら外す)。ルールの詳細・付けない箇所は[docs/rules.md](../../../docs/rules.md)の「本文中のメンバー名には必ず「さん」を付ける」。`GROUPS`に無い人物の記事は執筆時に手で付ける。

**chomoand-0.com(SixTONES)はこのあと`tools/sixtones_theme.py`で枠・マーカー・表をメンバーカラーに差し替える**(1人の記事=`--member 名前`、まとめ記事=`--per-section`。2026-11-07〜、詳細は[docs/rules.md](../../../docs/rules.md)の「SixTONES(chomoand-0.com)の記事も、枠・マーカー・表の色はメンバーカラーにする」)。

## STEP 1.56: スマホ向けのやさしい文章チェック(全サイト共通・必須、2026-11-10〜)

STEP1.55のあと、本文HTMLに`python tools/easy_read.py fix 記事.html`(難しい漢字をひらがなに自動で直す。「」の引用・『』の作品名・リンク文字列は触らない)→`python tools/easy_read.py check 記事.html`をかける。**NGが1件でもあれば(終了コード1)、その箇所を書き直してから投稿する**(80字超の文は2〜3文に分ける、5文超・250字超の段落は2つに分ける、4列以上の表は分けるか箇条書きに、硬い言葉は候補を見て言い換え、**「まとめに一言感想が無い」はまとめの枠の直後にファン目線の感想1〜2文を`<p>`で足す**(2026-11-12 ユカ指示))。「注意」(60〜80字の文・長い見出し・max-widthの無い画像)も直せるものは直す。ルールの詳細は[docs/rules.md](../../../docs/rules.md)の「スマホで読みやすく、誰でも分かる言葉で書く」。

## STEP 1.6: 楽天/Amazonアフィリエイトの自動挿入(全サイト・楽天/Amazonで買える商品の記事、2026-11-11〜ユカ指示)

**どのサイトでも、記事で紹介する商品が楽天かAmazonで売られていれば、確認なしでアフィリエイトを入れる**(2026-11-11ユカ指示「次回の記事から、楽天やアマゾンで取り扱いのある商品の記事はアフィリエイトを入れてほしい」。それまではchomoand-1.comの私物特定記事だけだった)。私服・アクセサリー・コスメ・家電・食品・本・グッズなど、商品の種類は問わない。

1. **記事の主役の商品**: `python tools/affiliate_box.py "ブランド 商品名 型番"`で楽天の候補を出し、**型番・色が記事の商品と合う候補**を選んで`--pick N --title "…" --note "色違いなど" --amazon "Amazon検索語" --border "{記事のアクセント色}" -o 枠.html`で「商品写真+楽天で見る/Amazonで見る」の枠を作る。答えを書いた最初のH2の情報ボックスのすぐ下に置く(例: chomoand-4.blog ID2530 しめちゃんの炊飯器記事)。
   - ふるさと納税・中古・セット品・別型番は選ばない(ツールが×を付ける)。合う候補が無ければ楽天は見送り、Amazon検索リンクだけ(`build_box`は片方だけでも作れる)。韓国ブランドなど両方に無ければ枠ごと見送る。
   - 写真は楽天の商品画像をそのままリンク(画像URLをWordPressにアップし直さない)。他人の「特定」投稿の画像を使わないルール([docs/rules.md](../../../docs/rules.md))があるので、商品写真が欲しいときはこの枠で出す。
2. **それ以外に出てくる商品**: ブランド名+商品が厳密一致で書かれている言及の直後に、`(<a href="{楽天アフィリエイトURL}" ... rel="nofollow sponsored noopener">楽天で見る</a> / <a href="{Amazon検索URL}" ... rel="nofollow sponsored noopener">Amazonで見る</a>)`をinlineで追記する。同一商品は本文で最初の1回だけ。判定基準・見送りルールは[koikeyz-affiliate](../koikeyz-affiliate/SKILL.md)の「新規記事執筆時の自動付与」と同じ(コイキーズ以外のサイトにもそのまま当てはめる)。
3. リンクを1つ以上入れたら本文の一番上に`python tools/affiliate_box.py --notice`のPR表記(本記事はプロモーションを含みます)を入れる(重複させない)。
4. 「購入先」box(rules.mdで必須)にも楽天/Amazonのリンクを並べる(公式ショップがあればそれが先)。
5. 値段を書くときは「〇月〇日に楽天市場を見ると〜円くらいから」のように日付を付ける(値段は毎日変わる)。
6. 商品がない記事(ライブ・番組・スケジュール・プロフィールなど)ではこのSTEPは丸ごとスキップ。韓国語版・英語版(STEP 6/7)にはリンクを引き継がない。
- キーはローカル`.env`、無ければGoogleドライブの`.env`から`affiliate_box.py`が自動で読む。
- 既存記事に後から足すときは、本文を丸ごと差し替える前に最新リビジョンを確認し、人が管理画面で直した分を上書きしない(2026-11-11 ID2530で上書きしてしまい、差分から入れ直した)。

## STEP 2: スラッグの生成

- Google翻訳API(client=gtx)でタイトルを英語に翻訳: `https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=en&dt=t&q={encoded_title}`
- 英語テキストをスラッグ化: 小文字に変換 → 記号除去(英数字・スペース・ハイフン以外) → スペースをハイフンに置換 → 連続ハイフンを1つに統合 → 先頭から30文字で切り捨て(末尾ハイフンも除去)
- 例:「並木雲楓に彼氏はいる?…」→ `does-kaede-namiki-have-a-boyfr`

## STEP 3: WordPressに下書き投稿

- **【絶対】最初に下書きで上げるときは、どのサイトの記事でも`title`の先頭に必ず「【未】」を付ける**(例:「【未】【すとらじ】SixTONESの私服はどこの？…」、2026-11-06オシリ指示「これは絶対の約束事」)。KR/EN版の下書きも同じ。35文字制限は【未】を除いた本体で数える。【未】は公開時に外す([publish](../publish/SKILL.md) STEP0)。
  - Why: 2026-11-06、すとらじ私服記事(chomoand-0.com ID1341)を【未】なしで下書きに上げて「【未】つけてってば」と指摘された。以前から付けていた記事もあったが、ルールとして書かれていなかったため抜けた。

- エンドポイント: `POST {サイトURL}/wp-json/wp/v2/posts`
- 投稿データ: `title`・`content`(HTML)・`slug`(STEP2)・`status: draft`・`categories`(サイト・カテゴリに応じて設定)・`author`(作業中のPCのhostnameから[docs/wordpress.mdの投稿者設定表](../../../docs/wordpress.md)を引いて該当ユーザーIDを設定。省略するとサイトの認証ユーザー本人が投稿者になってしまうため必須)
- 投稿成功後、**記事ID**を控える(STEP5で使用)
- **chomoand-1.comは投稿直後に`python tools/check_ko1keyz_title.py {記事ID}`を実行する**(2026-10-24〜)。タイトルにグループ名「KO1KEYZ」が無いとNG(終了コード1)。NGならタイトルを「【KO1KEYZ】RYOGAの〜」の形に直してから次のSTEPへ進む(詳細は[docs/rules.md](../../../docs/rules.md)の「メンバー個人記事も、タイトルに必ずグループ名」)

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

- **【全サイト共通】YouTube動画の回の記事は、アイキャッチ上段(小さい1行目)にYouTubeの企画名を入れる**(2026-11-12ユカ指示「次回の記事から、YouTubeの名前は上に入れてほしい」→同日「他のサイトも同じようにしてほしい」。見本: chomoand-0.com ID1503「手作りスパイスカレー/松村北斗/ピンクのジャージはどこの？/品番や値段は？」)。
  - ツールで作るサイト(SixTONES・トラジャ・予備ツール全般): `--top "企画名"`を付ける(既定のグループ名の代わり)。
  - Canva上書きのサイト(Snow Man・KEY TO LIT・KO1KEYZ・トレンド速報): 1行目(小)の区切りを企画名に置き換える(グループ名・タイトル前半・前置きの代わり)。2行目(大)はメンバー名/話題のまま、下段はタイトルの残り。
  - 企画名はYouTubeのタイトルの【】の中など、短い呼び名にする(長ければ約12字までに縮める)。YouTube回でない記事は今まで通り。
- **2026-11-03〜 chomoand-1.com(コイキーズブログ)のアイキャッチはCanva`DAG_zqaJE_8`のページを上書き→書き出しで作る(トモキ指示)。手順は[docs/canva-snowman-kitetsu.md](../../../docs/canva-snowman-kitetsu.md)の「KO1KEYZ」節。KR/ENはJPと同じ画像。以下の`eyecatch_koikeyz.py`はCanva MCPが使えないときの予備。**
- (旧ルール)**chomoand-1.com(コイキーズブログ)は、記事本文の写真の有無にかかわらず必ず`tools/eyecatch_koikeyz.py`の文字入りテンプレで生成する**(2026-08-17にユーザーが再確認・上書き。[docs/eyecatch-style.md](../../../docs/eyecatch-style.md)の「KO1KEYZ統一テンプレ必須、既存記事が全部このデザインで揃っているので勝手に変えない」が現行ルール)。使い方は`tools/eyecatch_koikeyz.py`のdocstring参照(`--top`/`--main`/`--bottom`/`--out`、KR/EN版はJPと同じ画像を使う。`--lang kr`で韓国語版を別に作る旧運用は2026-11-03に廃止)。
  - **(誤った過去の試験導入・現在は無効)2026-08-11〜08-17の一時期のみ、「本文中に埋め込んだ写真の1枚目をfeatured_mediaに使い、テキストeyecatchは作らない」という運用を試したことがあるが、2026-08-17にユーザーから「ちがうよ基本文字入れだよアイキャッチは」と明確に否定された。** KO1KEYZ「KO1WORLD」ロケ地特定記事(下書きID11410)でこの旧ルールに従い本文写真をfeatured_mediaにしたところ即座に修正指示が入り、テキスト入りeyecatchへ差し替えた実例あり。今後このSTEP4を読むときは本項目(文字入り必須)を正としてそのまま使うこと。
- **2026-11-03〜 chomoand.com(トレンド速報)のアイキャッチは、トモキのCanvaデザイン`DAGnrXY2_5I`の15ページから背景をランダムに1枚選んで上書き→書き出しで作る(トモキ指示)。手順は[docs/canva-snowman-kitetsu.md](../../../docs/canva-snowman-kitetsu.md)の「トレンド速報(chomoand.com)」節。下の`DAHPjgiBOTI`複製方式・`eyecatch_chomoand.py`は使わない(Canva MCPが使えないときだけ予備)。**
- (旧ルール)**chomoand.comの記事は必ずCanva MCPで作る**(2026-07-16〜、[docs/canva-mcp-chomoand.md](../../../docs/canva-mcp-chomoand.md)の運用フローに従う)。要点:
  - 専用マスターデザイン(design_id: `DAHPjgiBOTI`、1ページのみ)を`copy-design`で複製する(`page_numbers`指定不要)
  - 3つの独立したテキスト要素(1行目=番組名/2行目=出演者名/3〜4行目=疑問形+補足)を`replace_text`で置換する(KO1KEYZと違い要素が分かれているのでフォントサイズが飛ぶ心配はない)
  - **背景のブラシストロークを毎回ランダムな色に差し替える**(KO1KEYZと同じアセット一覧を使い回せる)
  - `export-design`で1200×675のPNGにして`images/`に保存
  - Canva MCPが使えないときのフォールバックは[docs/eyecatch-style.md](../../../docs/eyecatch-style.md)の汎用テンプレ(1200×630px)
- chomoand-0.comのデザイン仕様は[docs/eyecatch-style.md](../../../docs/eyecatch-style.md)参照(1200×630px)
- **chomoand-4.blog(Travis Japan専門ブログ)は、確認なしで自動的に`tools/eyecatch_torahja_canva.py`のCanva水彩デザインで作る**(2026-10-02〜。**紫3行の`eyecatch_torahja.py`・旧ベージュの`eyecatch_chomoand0_old.py`は使わない**。2026-10-04にこのSTEPが紫3行のまま古く、記事ID1213で誤って紫3行を使い作り直した)。手順:
  1. `--main`=個人記事はメンバー名、グループ・2人以上が同格の回は話題キーワード。`--top`は既定の「Travis Japan」(YouTube回は企画名、上の全サイト共通ルール)。`--bottom`=タイトルの残り(1〜2行、`--bottom`を2回まで)。記号は全角(？！)。
  2. `python tools/eyecatch_torahja_canva.py --main "松田元太" --bottom "インスタライブのジャージはどこの？" --bottom "中村海人デザインと判明！" --color-key 松田元太 --out images/{ファイル名}_eyecatch_canva.jpg`(`--color-key`は個人=メンバー名、グループ=`group`、複数メンバー回=`group_warm`)。
  3. 生成後に目視確認し、STEP5で`image/jpeg`としてアップロードしてfeatured_mediaに設定する。完了報告に上段/中央/下段の分け方を一言添える。
  - 仕様の正は[docs/eyecatch-style.mdの「chomoand-4.blog Canva水彩デザイン」](../../../docs/eyecatch-style.md)。
- **chomoand-2.com(Snow Man)・chomoand-5.site(KEY TO LIT)は、確認なしでトモキのCanvaデザインを上書きして作る**(2026-10-27〜、トモキ指示)。Snow Man=`DAHYbnGesOc`、KEY TO LIT=`DAHYbqcAORI`。メンバーのページ(グループ回はグループのページ)の文字を`find_and_replace_text`で置き換え→commit→jpg width1200で書き出し→STEP5でアップしてfeatured_mediaに設定。ページ対応・文字の型・ハマりどころは[docs/canva-snowman-kitetsu.md](../../../docs/canva-snowman-kitetsu.md)。
  - `tools/eyecatch_snowman.py`・`tools/eyecatch_kitetsu.py`はCanva MCPが使えないときの予備(普段は使わない)。
  - カテゴリIDは[docs/wordpress.md](../../../docs/wordpress.md)の各サイトの表(基本`[4]`+メンバーのカテゴリ)。
- **chomoand-0.com(SixTONES専門ブログ)は、確認なしで自動的に`tools/eyecatch_sixtones.py`で作る**(2026-10-27〜。SixTONES用のCanvaデザインができたらSnow Manと同じ上書き方式に切り替える):
  1. `--main`=個人記事はメンバー名、グループ回は話題キーワード。`--top`は既定の「SixTONES」。**ただしYouTube動画の回の記事は、`--top`にYouTubeの企画名(例:`--top "手作りスパイスカレー"`)を入れる**(2026-11-12ユカ指示「次回の記事から、YouTubeの名前は上に入れてほしい」。ID1503で初適用)。`--bottom`=タイトルの残り(1〜2行)。記号は全角(？！)。
  2. `python tools/eyecatch_sixtones.py --main "松村北斗" --bottom "私服のジャケットはどこの？" --bottom "ブランドを調査！" --color-key 松村北斗 --out images/{ファイル名}_eyecatch.jpg`(`--color-key`は個人=メンバー名、グループ=`group`、2人回=`松村北斗+田中樹`)。
  3. 目視確認→STEP5で`image/jpeg`としてアップロードしてfeatured_mediaに設定。
  - カテゴリIDは[docs/wordpress.md](../../../docs/wordpress.md)のchomoand-0.comの表(基本`[15]`+メンバーのカテゴリ)。
- 保存先: `images/{ファイル名}_eyecatch.png`

## STEP 5: アイキャッチをWordPressにアップロード・設定

- **STEP4で記事内の写真を使うことになった場合(コイキーズ・写真ありの記事)**: 新規アップロードは不要。STEP1で取得済みのそのメディアIDをそのままSTEP3の記事に設定: `POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}` ボディ `{ "featured_media": メディアID }`
- **STEP4で生成アイキャッチを使うことになった場合(それ以外)**: 画像をバイナリで読み込み、`POST {サイトURL}/wp-json/wp/v2/media`にアップロード(`Content-Type: image/png`、`Content-Disposition: attachment; filename="xxx.png"`)。取得した**メディアID**をSTEP3の記事に設定: `POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}` ボディ `{ "featured_media": メディアID }`

## STEP 0(chomoand-1.com限定・作業開始時に1回): 多言語版(韓国語・英語)の抜け漏れチェック

chomoand-1.com向けにこのスキルを実行する**最初に**、`python tools/check_translation_gaps.py`を実行し、過去の記事で韓国語版・英語版(下書き含む)が見つからないものがないか確認する。STEP6・STEP7は同一セッション内の続き処理として動くため、途中で中断すると気づかれないまま抜けることがある(詳細は[docs/korea-expansion.md](../../../docs/korea-expansion.md)の「なぜ抜け漏れが起きるか」参照)。抜け漏れが見つかっても、**英語版の既存記事への一括バックフィルは対象外**(2026-08-19時点、[docs/english-expansion.md](../../../docs/english-expansion.md)参照。適用範囲は2026-08-19以降の新規アップロードのみ)。韓国語版の抜け漏れは、新規記事の作業に入る前にSTEP6相当の処理で先に埋める。

## STEP 6(chomoand-1.com限定): 韓国語版下書きの自動生成

コイキーズブログ(chomoand-1.com)の記事は、STEP3完了後に**確認なしで自動的に**韓国語版の下書きも作成する(2026-07-19〜、トモキ指示)。ローカライズの方法・POSTする`lang`フィールドの使い方は[docs/korea-expansion.md](../../../docs/korea-expansion.md)を参照。**slugは必ず元記事slug+`-kr`にする**(翻訳グループの紐付けはサイト常駐mu-plugin `ko1keyz-i18n-autolink` がslug規則で自動判定するため。REST の `translations` フィールドは効かない、詳細は同docs参照)。**韓国語版も日本語版と同じアイキャッチ画像をfeatured_mediaに設定する**(2026-07-30〜、日本語版のアイキャッチ復活に合わせて変更)。chomoand.com・chomoand-0.comの記事にはこのSTEPは適用しない。STEP6を終えたら、slugが元記事の`-kr`命名規則に従っていることを確認する(次回以降のSTEP0の突き合わせに必要)。

## STEP 7(chomoand-1.com限定): 英語版下書きの自動生成(2026-08-19〜)

コイキーズブログ(chomoand-1.com)の記事は、STEP6(韓国語版)に続けて**確認なしで自動的に**英語版の下書きも作成する(2026-08-19〜、トモキ指示。海外展開の優先順位「韓国語→英語→中国語」の2段階目)。ローカライズの方法・POSTする`lang`フィールドの使い方は[docs/english-expansion.md](../../../docs/english-expansion.md)を参照。**slugは必ず元記事slug+`-en`にする**(翻訳グループの紐付けはmu-plugin `ko1keyz-i18n-autolink` がslug規則で自動判定。REST の `translations` フィールドは効かない)。韓国語版と同じく、日本語版と同じアイキャッチ画像をfeatured_mediaに設定する(英語専用のテキスト入りアイキャッチは作らない)。chomoand.com・chomoand-0.comの記事にはこのSTEPは適用しない。**適用範囲は2026-08-19以降の新規アップロードのみ**(既存記事への英語版バックフィルは別途指示があるまで行わない)。STEP7を終えたら、slugが元記事の`-en`命名規則に従っていることを確認する(次回以降のSTEP0の突き合わせに必要)。あわせて`python tools/check_ko1keyz_title.py {日本語版ID} {韓国語版ID} {英語版ID}`を実行し、韓国語版・英語版のタイトルにも「KO1KEYZ」が入っていることを確認する(NGなら直す)。

## STEP 8(全サイト共通・必須): YouTube埋め込みの再生エラー対策(2026-11-10〜)

下書きを全部(翻訳版も含む)作り終えたら、`python tools/fix_youtube_embeds.py --recent-minutes 60`を実行する。直近60分に更新された全サイトの記事を調べて、`referrerpolicy`が無いYouTube iframe(読者の画面で「エラー153」になって再生できない)を、WordPress標準の埋め込みブロックに置き換える。直した件数は完了報告に含める。YouTubeを埋め込むときは最初からiframeを手書きしないで`<!-- wp:embed -->`ブロックを使う(書き方は同ツールの`embed_block()`)。経緯は[publish](../publish/SKILL.md) 0.7。

## 完了報告

全STEP終了後、以下をユーザーに報告する:
- 記事ID・スラッグ・確認URL(`{サイトURL}/?p={id}`)
- アイキャッチ画像のメディアID(chomoand-1.com以外)
- (chomoand-1.comの場合)韓国語下書き・英語下書きのID・スラッグ
- (STEP1.6を実行した場合)どの商品に楽天/Amazonの枠・リンクを入れたか(楽天はどの店・値段か)、見送った商品があればその理由

**How to apply:** 「ブログにアップして」「アップして」「WordPressに反映して」などの発言をトリガーとしてSTEP1〜7を順番に実行する。STEP1.5(ブロック変換)は全サイト共通で必ず行う。chomoand-1.comはSTEP0(セッション最初の1回のみ)→STEP1→STEP1.5→STEP1.6(楽天/Amazonで買える商品の記事・アフィリエイト自動挿入)→STEP2→STEP3→STEP3.5(SNS投稿文)→STEP4→STEP5→STEP6→STEP7、それ以外のサイトはSTEP1→STEP1.5→STEP1.6(商品の記事のみ)→STEP2〜5(STEP3.5は現状コイキーズ限定)。記事の削除は絶対に行わない([docs/wordpress.md](../../../docs/wordpress.md))。公開自体は別途[publishスキル](../publish/SKILL.md)で行う。公開後の自動SNS投稿(Facebook/Instagram/Threads=Jetpack Social・X=手動運用)の仕組みは[docs/sns-auto-post-setup.md](../../../docs/sns-auto-post-setup.md)参照。
