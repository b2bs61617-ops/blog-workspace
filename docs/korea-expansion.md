# コイキーズブログ(chomoand-1.com)の韓国語展開

KO1KEYZが韓国でもデビューするため、chomoand-1.comを多言語化した(2026-07-19、トモキ指示)。海外展開の優先順位は **韓国語 → 英語 → 中国語**(中国語はAdSenseが使えないため後回し。詳細背景は不要ならこのファイルには書かない)。英語版は2026-08-19に追加、詳細は[english-expansion.md](english-expansion.md)参照。

## サイト構成

- Polylangプラグインを導入済み(2026-07-19)。言語: 日本語(デフォルト)・한국어・English・中文(中国)の4つを登録済み。
- **URL構造はサブディレクトリ方式**(`設定 → 言語 → URLの修正`で「言語はプリティーパーマリンク内のディレクトリ名から設定される」を選択済み)。例: `chomoand-1.com/ko/記事名`
- **「URLにデフォルトの言語情報を表示しない」に必ずチェックを入れておくこと**。これが外れると既存の日本語記事のURLに`/ja/`が付いて壊れる。[絶対厳守ルール](wordpress.md)そのものに関わる最重要設定なので、触る作業をするときは必ず事前に確認する。
- メディアの言語分けは無効(2026-07-19に無効化。有効にすると画像アップロードのたびに言語選択が挟まって煩雑になるだけで、メリットがないため)。
- ブラウザーの言語自動検出も無効のまま(既存の日本読者の閲覧に影響を与えないため)。

## 運用ルール(絶対厳守)

- 韓国語版はすべて**下書き(status: draft)**で作成する。公開は既存の[publishスキル](../.claude/skills/publish/SKILL.md)を通して、ユーザーの指示があったときだけ行う(日本語記事と同じ運用)。
- 既存の日本語記事・URL・パーマリンクには一切触らない。韓国語版は常に「追加」のみで、既存コンテンツを変更・削除することは絶対にしない。
- **2026-09-07: KO1KEYZ時代(2026-06-01以降の日付の日本語公開記事)の韓国語版・英語版の一括バックフィルをトモキ指示で実施済み。** 対象範囲(2026-06〜09)の公開JP記事はKR・ENともに抜けゼロ(`scratchpad/audit_i18n.py`で確認)、作った端から公開＋Google/Naver送信まで完了。オーディション時代(2026-01〜05)の既存記事は引き続き未対応(必要になったら別途指示を受けて実施)。

## STEP: 日本語記事アップロード後、韓国語版を自動生成する(2026-07-19〜)

[blog-uploadスキル](../.claude/skills/blog-upload/SKILL.md)でchomoand-1.com(コイキーズブログ)の記事を投稿したら、STEP5完了後に**必ず自動で**以下を行う(トモキから「今後は日本語記事を作成したら自動でここまでやって欲しい」と指示あり、確認不要)。

1. **元記事の取得**: `GET {サイトURL}/wp-json/wp/v2/posts/{元記事ID}` で日本語版の`title`・`content`を取得する。
2. **韓国語ローカライズ**: 直訳ではなく韓国語読者に自然な言い回し・見出しでローカライズする。元記事のHTMLブロック構造(`wp-block-paragraph`・`is-style-dent_box`(引用/コメント紹介)・`is-style-icon_announce`・`swell-block-capbox`(プロフィール枠)・`<figure>`画像+`<figcaption>`)はそのまま維持し、テキスト部分だけ韓国語に置き換える(SWELLテーマのスタイルがこれらのクラスに依存しているため)。**元記事が[blog-uploadスキルSTEP1.5](../.claude/skills/blog-upload/SKILL.md)でGutenbergブロックコメント(`<!-- wp:xxx -->`)付きになっている場合は、そのコメント構造(`<!-- wp:heading -->`/`<!-- wp:paragraph -->`/`<!-- wp:html -->`など)もテキスト同様にそのまま維持する**(2026-07-27〜)。
3. **下書き投稿**: `POST {サイトURL}/wp-json/wp/v2/posts` で新規作成する。ボディに以下を含める:
   - `title`(韓国語)・`content`(韓国語、ブロック構造維持)
   - `status: "draft"`(絶対に`publish`にしない)
   - `slug`: 元記事のslugに`-kr`を付ける(**この命名規則は必須。下記の欠落チェックと、翻訳グループ自動紐付けmu-plugin `ko1keyz-i18n-autolink` の両方がslugの`-kr`サフィックスでJP/KR記事を突き合わせている。崩すと検知も紐付けもできなくなる**)。
   - `lang: "ko"` を含める(応答の`link`が`/ko/`配下のURLになっていればPolylang側で韓国語として登録されている証拠。GETで読み返しても`lang`フィールドは応答に出てこない仕様)。
   - **`translations: {"ja": 元記事ID}` は送っても無害だが効果はない。** Polylang 3.8.7 free の環境では REST の `translations` 書き込みが翻訳グループに反映されないことを2026-09-09に検証済み(過去の記述「REST APIがこのフィールドを認識する」は誤り。実際には言語割り当てだけが効いていて、hreflangに必要なグループ紐付けは一度も保存されていなかった)。**翻訳グループの紐付けはサイト常駐の mu-plugin `ko1keyz-i18n-autolink.php` が save 時に自動で行う**([リポジトリの `tools/wp-mu-plugins/ko1keyz-i18n-autolink.php`](../tools/wp-mu-plugins/ko1keyz-i18n-autolink.php) を chomoand-1.com の `wp-content/mu-plugins/` に設置済み)。KR/EN版を`-kr`/`-en` slug + 正しい`lang`で作れば、次の save で JP⇔KR⇔EN が自動でグループ化され `<link rel="alternate" hreflang>` が出る。
4. **アイキャッチは作らない**(2026-07-24〜。それまでは韓国語テキスト入りの専用アイキャッチを別途生成する運用だったが、コイキーズブログ全体でアイキャッチ自体を廃止したためこのSTEPは不要になった)。
5. **完了報告**: 日本語版の報告に加えて、韓国語下書きのID・スラッグをユーザーに報告する。

### なぜ抜け漏れが起きるか、どう検知するか(2026-08-02追記)

STEP6は「STEP3完了後に同じ作業の続きとして自動実行する」設計であり、cronのような独立処理ではない。そのため以下のケースで**エラーも記録も残らないまま韓国語版が作られない**ことがある:

- STEP1.5(Gutenbergブロック変換)など前段のSTEPでフォーマットの解釈が変わり、そのままの勢いでSTEP6まで実行されない
- 作業セッションがSTEP5で区切られてしまい、STEP6まで続けて実行されない

**GETでは`lang`/`translations`が返らないため、公開後のサイトマップやフロントページを見ても「下書きのまま止まっているだけ」なのか「本当に作られていない」のか区別できない。** 判定には認証付きで`status=draft`も含めて取得する必要がある。

[`tools/check_translation_gaps.py`](../tools/check_translation_gaps.py)(2026-08-19に韓国語専用の`check_kr_translation_gaps.py`から改名・拡張。英語版のチェックも同時に行う)を使うと、chomoand-1.comの全記事(下書き含む)をslugの前方一致で突き合わせ、韓国語版が見つからない日本語記事を一覧化できる。**chomoand-1.com向けにblog-uploadスキルを実行する作業の最初に、まずこのスクリプトを実行して既存の抜け漏れがないか確認し、あれば先にSTEP6相当の処理で埋めてから新規記事の作業に入ること。**

### hreflang(翻訳グループ紐付け)— mu-pluginで自動化(2026-09-09)

**背景**: docs記載の「REST の `translations` フィールドで紐付く」は Polylang 3.8.7 free では動いていなかった。2026-09-09時点で公開JP記事136本すべてが翻訳グループ未紐付け＝`<link rel="alternate" hreflang>` が1件も出ていない状態だった(言語割り当て `/ko/` `/en/` はできていたが、グループ関係が未保存)。

**恒久対策**: サイト常駐 mu-plugin [`tools/wp-mu-plugins/ko1keyz-i18n-autolink.php`](../tools/wp-mu-plugins/ko1keyz-i18n-autolink.php) を chomoand-1.com の `wp-content/mu-plugins/` に設置。`wp_after_insert_post` フックで、記事のPolylang言語とslug(`{base}` / `{base}-kr` / `{base}-en`)からグループを組み立て `pll_save_post_translations()` を呼ぶ。下書き・予約投稿も対象。言語未設定の記事や `-kr`/`-en` 規則から外れたslugには触らない(誤爆防止)。**blog-uploadのSTEP6/7で `-kr`/`-en` slug と正しい `lang` さえ守れば、以後の記事は保存時に自動でhreflangが出る。**

**一括バックフィル(2026-09-09・単発)**: 既存140グループ(公開136+下書き4)を、SSH不要のブラウザ実行版スクリプト(`wp-load.php` を自前ロードしてトークンガード付きで `pll_save_post_translations()` をループ)で紐付け済み。実行後136/136の公開JP記事でhreflang出力を確認、スクリプトは削除済み。同等の監査は `tools/check_translation_gaps.py`(slug突き合わせ)+ フロントHTMLの `hreflang` grep で可能。

**注意**: mu-plugin は本番投入時に一度、適当なJP記事を開いて `<head>` に `hreflang="ja"/"ko"/"en"` の3行(EN未作成なら2行)が出るか確認する。slug衝突で `-kr-2` 等になった相手は完全一致検索から漏れるので、その場合だけ手動 or バックフィルスクリプトで補う。

### PowerShellでのREST API呼び出しの注意(2026-07-19に確認)

- [blog-uploadスキルSTEP3](../.claude/skills/blog-upload/SKILL.md)に既出の`Get-Content -Raw`→`[string]`キャストの注意と同根の問題として、`ConvertTo-Json`は長い文字列を`{"value":"...","ReadCount":1}`のような形に壊すことがある(原因未特定。`[string]`キャストで直る場合と直らない場合がある)。**確実なのはJSON文字列を手動で組み立てる方法**: バックスラッシュ→`\\`、ダブルクォート→`\"`、改行→`\n`の順に置換してから`'{"title":"' + $escTitle + '","content":"' + $escContent + '"}'`のように文字列連結でJSONを作り、`[System.Text.Encoding]::UTF8.GetBytes($json)`でバイト列化して送信する。
- 送信前に必ず`content.raw`の文字数を投稿元と見比えて、本文が空(0文字)で保存されていないか確認する(2026-07-19に実際に本文が空で保存される事故があった。原因はConvertTo-Jsonの上記不具合)。

関連: [wordpress.md](wordpress.md)(絶対厳守ルール全般)、[eyecatch-style.md](eyecatch-style.md)(アイキャッチのデザイン仕様)
