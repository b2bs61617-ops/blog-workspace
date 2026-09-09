# コイキーズブログ(chomoand-1.com)の英語展開

KO1KEYZの海外展開の第2弾として、英語版の自動生成を追加した(2026-08-19、トモキ指示)。優先順位「韓国語→英語→中国語」([korea-expansion.md](korea-expansion.md)参照)の2段階目にあたる。

サイト全体のPolylang設定(URL構造・言語一覧・「URLにデフォルトの言語情報を表示しない」設定など)は韓国語版導入時に済ませてあり、Polylangには最初からEnglishも言語として登録済み。共通のインフラ部分は[korea-expansion.md](korea-expansion.md)を参照し、ここには英語版固有のルールのみ書く。

## 運用ルール(絶対厳守)

- 英語版もすべて**下書き(status: draft)**で作成する。公開は既存の[publishスキル](../.claude/skills/publish/SKILL.md)を通して、ユーザーの指示があったときだけ行う(日本語・韓国語と同じ運用)。
- 既存の日本語記事・韓国語記事・URL・パーマリンクには一切触らない。英語版は常に「追加」のみ。
- **適用範囲は2026-08-19以降にblog-uploadスキルで新規アップロードする記事のみ。** それ以前に公開済み・下書き済みの既存記事への英語版の一括バックフィルは原則対象外(トモキの意向で「今後の新規記事の自動化を優先、既存記事はまた別途」となった)。まとめて作りたくなったら、そのときあらためて指示を受けて[抜け漏れチェック](#抜け漏れチェック)で対象を洗い出してから行う。
  - **2026-09-07: KO1KEYZ時代(2026-06-01以降の日付の日本語公開記事)の英語版・韓国語版の一括バックフィルをトモキ指示で実施済み。** 対象範囲(2026-06〜09)の公開JP記事はKR・ENともに抜けゼロ(`scratchpad/audit_i18n.py`で確認)。作った端から公開＋Google/Naver送信まで完了。オーディション時代(2026-01〜05)の既存記事は引き続き対象外。

## STEP: 日本語記事アップロード後、英語版を自動生成する(2026-08-19〜)

[blog-uploadスキル](../.claude/skills/blog-upload/SKILL.md)でchomoand-1.com(コイキーズブログ)の記事を投稿したら、韓国語版(STEP6)に続けてSTEP7で英語版も**必ず自動で**作成する(トモキから確認不要の指示)。

1. **元記事の取得**: 日本語版の`title`・`content`(STEP6で既に取得済みならそのまま使い回してよい)。
2. **英語ローカライズ**: 直訳ではなく英語圏読者に自然な言い回し・見出しでローカライズする。元記事のHTMLブロック構造(`wp-block-paragraph`・`is-style-dent_box`・`is-style-icon_announce`・`swell-block-capbox`・`<figure>`画像+`<figcaption>`など)とGutenbergブロックコメント(`<!-- wp:xxx -->`)はそのまま維持し、テキスト部分だけ英語に置き換える(韓国語版と同じ考え方、[korea-expansion.md](korea-expansion.md)参照)。
3. **下書き投稿**: `POST {サイトURL}/wp-json/wp/v2/posts` で新規作成する。
   - `title`(英語)・`content`(英語、ブロック構造維持)
   - `status: "draft"`(絶対に`publish`にしない)
   - `slug`: 元記事のslugに`-en`を付ける(**必須。抜け漏れチェックと翻訳グループ自動紐付けmu-plugin `ko1keyz-i18n-autolink` の両方がslugの`-en`サフィックスでJP/EN記事を突き合わせている**)。
   - `lang: "en"` を含める(応答の`link`が`/en/`配下のURLになっていれば言語登録OK)。
   - **`translations: {"ja": 元記事ID}` は効果なし**(Polylang 3.8.7 free で REST の `translations` 書き込みが反映されないことを2026-09-09に検証。[korea-expansion.md](korea-expansion.md)の「hreflang（翻訳グループ紐付け）」参照)。**紐付けはサイト常駐 mu-plugin [`ko1keyz-i18n-autolink.php`](../tools/wp-mu-plugins/ko1keyz-i18n-autolink.php) が save 時に自動実行する。** `-en` slug + 正しい `lang` で作れば以後は自動でhreflangが出る。
4. **アイキャッチは日本語版と同じ画像をfeatured_mediaに設定する**(韓国語版と同じ運用。テキスト入りの英語専用アイキャッチは別途作らない)。
5. **完了報告**: 日本語版・韓国語版の報告に加えて、英語下書きのID・スラッグをユーザーに報告する。

## 抜け漏れチェック

[tools/check_translation_gaps.py](../tools/check_translation_gaps.py)(2026-08-19に韓国語専用の`check_kr_translation_gaps.py`から改名・拡張)で、chomoand-1.comの全記事(下書き含む)をslugの前方一致で突き合わせ、韓国語版・英語版それぞれが見つからない日本語記事を一覧化できる。[blog-uploadスキルSTEP0](../.claude/skills/blog-upload/SKILL.md)で作業開始時に実行する。

関連: [korea-expansion.md](korea-expansion.md)(Polylang共通インフラ・韓国語版の詳細)、[wordpress.md](wordpress.md)(絶対厳守ルール全般)、[eyecatch-style.md](eyecatch-style.md)(アイキャッチのデザイン仕様)
