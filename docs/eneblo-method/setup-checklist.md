# エネブロ式 ブログ立ち上げ 統合チェックリスト

出典: hide000.net（エネブロ）+ トモキ提供PDF「サイトの立上げ」「プラグイン一覧」。
各項目の詳細は [reference/](reference/) の該当ページ参照。

凡例: ★=必須 / ☆=推奨 / △=任意・後回し可

---

## Phase 0. サーバー・ドメイン

- ★ Xserver 契約（`reference/xserver_intro.md`）
- ★ 独自ドメイン取得 … 信頼性重視で `.com` / `.net` / `.jp` 推奨（他TLDでもSEO/アドセンスに影響はないがユーザーがクリックを警戒しやすい）（`reference/domain_server.md`）
- ★ ネームサーバー = 「エックスサーバーを設定する（標準）」
- ★ 無料独自SSL を利用する
- ★ HTTPS転送 を ON（httpアクセスをhttpsへ301）
- △ AIクローラー遮断（ドメイン設定のチェック）
- ★ WordPress簡単インストール（ブログ名／ユーザー名／パスワード／メール）
- ☆ Xserver 手動バックアップを定期取得 … データファイル + データベースの2点（ホームディレクトリ一括は時間がかかるのでドメイン単位で）

## Phase 1. WordPress 初期設定（★記事を1本も書く前に）

- ★ 設定→一般 … サイトタイトル、キャッチフレーズ
- ★ 設定→投稿設定→更新情報サービス（ping）… 下記15行を貼り付け
  ```
  http://api.my.yahoo.co.jp/RPC2
  http://blog.goo.ne.jp/XMLRPC
  http://blogsearch.google.co.jp/ping/RPC2
  http://blogsearch.google.com/ping/RPC2
  http://ping.blo.gs/
  http://ping.blogranking.net/
  http://ping.dendou.jp/
  http://ping.fc2.com/
  http://ping.freeblogranking.com/xmlrpc/
  http://ping.myblog.jp/
  http://pingoo.jp/ping/
  http://rpc.weblogs.com/RPC2
  http://serenebach.net/rep.cgi
  http://taichistereo.net/xmlrpc/
  http://www.i-learn.jp/ping/
  ```
- 設定→表示設定／ディスカッション … 基本変更不要
- ★ 設定→メディア … 画像「大」サイズを **幅500 / 高さ500**（初期1024は大きすぎて見切れ・はみ出しの恐れ）
- ★ 設定→パーマリンク … カスタム構造 `/%postname%-%post_id%`（1記事でも公開後に変えるとURLが変わり表示されなくなるので厳禁）（`reference/permalink.md` / `initial_setting.md`）

## Phase 2. テーマ

- ★ SWELL（有料・強く推奨）または Cocoon（無料）。あとからの乗り換えは非常に手間なので最初にSWELLが理想（`reference/theme_intro.md`）
- ★ 親テーマ + 子テーマ を両方インストールし、**子テーマを有効化**（親を有効化するとアップデートで設定が初期化される）（`reference/master_child.md`）
- ☆ SWELL外観カスタマイズ／書式設定 … デフォルトで動くが一度は確認

## Phase 3. プラグイン（★すべてインストール＆有効化）

共通（SWELL / Cocoon 両方）:

| # | プラグイン | 設定 |
|---|---|---|
| 1 | Contact Form 7 | 生成される「Contact form 1」のショートコードをお問い合わせ固定ページに貼る |
| 2 | Converter for Media | 一般設定: 変換戦略=最速化(隔離化) / 出力=WebP / 対応ディレクトリ=`/uploads`のみ / 拡張子=jpg・png・webp / 変換方法=Imagick / 「元ファイルより大きい形式を自動削除」ON / 「アップロード時に自動変換」ON。高度な設定: 統計ON |
| 3 | Site Kit by Google | Phase 4 で設定。アナリティクスは**新規作成**を選ぶ |
| 4 | Throws SPAM Away | 「日本語文字含有数」 3→**5**。コメント欄下の注意文＝「コメントに日本語が含まれない場合は表示できません！」、判定エラー文＝「日本語を規定文字数以上含まない記事は投稿できません。」 |
| 5 | WP Content Copy Protection & No Right Click | 設定不要 |
| 6 | WP Sitemap Page | サイトマップ固定ページで `[wp_sitemap_page]` を使う |
| 7 | XML Sitemap Generator for Google | 「HTML形式でのサイトマップを含める」の**チェックを外す**。`sitemap.xml` のURLを控えて Phase 4 で Search Console に送信。※必ず実施 |
| 8 | WP Multibyte Patch | 有効化のみ |
| 9 | WP Revisions Control | 設定不要（記事執筆時に「残すリビジョン数」2〜3、任意） |
| 10 | Bulk Datetime Change | 設定不要（リライト時に日付一括更新に使う。おまじないレベル） |
| 11 | Advanced Ads | **AdSense合格後**に配布 zip(`advancedAds_base.zip`)を解凍してインポート |
| 12 | Broken Link Checker | 有効化時に「**ローカル版**」を選択。設定は初期のまま |
| 13 | SiteGuard WP Plugin | 有効化したら初期設定のまま |

SWELL利用者のみ追加:

| 14 | SEO SIMPLE PACK | 設定不要 |

補足: スパム対策で **Akismet** も別途セットアップ可（APIキーは配布資料記載の `c672c6c59d8a`、全サイト共通）。エネブロのメインのプラグイン表には含まれない扱い。

## Phase 4. Google 連携（`reference/sc_setup.md` / `ga_base.md` / `index.md`）

- ★ Google Search Console 導入 … **ドメインプロパティ**で登録（`https://` を外してドメイン名だけ入力）。表示された TXT レコードを Xserver の「DNSレコード設定」に種別TXTで追加 → 所有権確認（反映に最大15分）
- ★ Google Analytics（GA4）… プロパティを新規作成（アカウント名は任意）
- ★ Site Kit で Search Console + Analytics を連携
- ★ Search Console →「サイトマップ」に `sitemap.xml` を送信
- 運用: 公開記事は Search Console のURL検査で毎回インデックス申請。不要記事（アクセスが来ない記事）は週2〜3本ペースで削除（404の大量発生を避ける）

## Phase 5. 固定ページ・サイト構成（★収益化時の信用性に必須）

- ★ お問い合わせ（Contact Form 7 のショートコード）
- ★ プロフィール（内容は「適当に」でよい）
- ★ プライバシーポリシー（サンプル全文: `reference/sample_privacy.md`）
- ★ 免責事項（サンプル全文: `reference/sample_menseki.md`）
- ★ サイトマップ（HTMLブロックに `[wp_sitemap_page]`）
- ★ カテゴリー設定（ジャンルごとに用意。パーマリンク短く英字）
- ☆ ウィジェット（サイドバー: プロフィール・検索・カテゴリー等）
- ★ グローバルメニュー（ヘッダーに **各カテゴリー / プロフィール / お問い合わせ / プライバシーポリシー / サイトマップ / 免責事項** を並べる … AdSense審査の最低フォーマット）
- ☆ パンくずリスト（SWELL標準。Search Consoleでエラー監視）（`reference/breadcrumb.md`）
- クリーンアップ: 初期投稿「Hello world!」・「サンプルページ」を削除

## Phase 6. ビジュアル（△任意だが推奨）

- △ サイトアイコン 1500×1500px（CANVA で作成）
- △ メインビジュアル 1600×400px（CANVA で作成）

## Phase 7. AdSense（記事20〜30本・200〜300PV/日 到達後）（`reference/adsense.md` ほか）

- Google のビジネスモデル/SEO を理解（`reference/ads_gbm_seo.md` / `ads_article_app.md`）
- TOPページヘッダーに Phase 5 の固定ページ一式が並んでいること
- AdSense 申請（合格しやすい時期・しにくい時期がある。1〜2回落ちたら1〜2ヶ月空けて再申請）（`reference/ads_apply.md`）
- ads.txt を設置
- Advanced Ads で広告コードを配置（`reference/ads_kind_code.md`）
- 初期は「エイジングフィルター対策」でPVを作る

## 付記: content 系（サイト設定ではなく記事制作）

キーワード選定/タイトル（`reference/kw.md`）、スキル実践編（`reference/kiwami.md`）、PVネタ集（`reference/pv.md`）、ネタ選定（`reference/neta.md`）は動画+配布PDF中心。テキストで取れた分のみ reference に保存。
