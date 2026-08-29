# Search Console インデックス調査（進行中）

3サイトの Search Console を `tools/check_search_console.py`（URL Inspection API）で全記事URL一括照会し、
「エラーが出まくっている」件の実態を切り分けた記録。**他のPCからでもここから続きができる。**

- 開始: 2026-08-29
- 実行者: 松（トモキ依頼）
- サービスアカウント: 3サイトとも `siteOwner` 権限あり。**プロパティ指定は `sc-domain:<ドメイン>` が必須**
  （スクリプトのデフォルト `https://<ドメイン>/` だと 403 "You do not own this site"）。
- 生データ: [docs/research-notes/search-console-2026-08-29/](research-notes/search-console-2026-08-29/)
  - `chomoand.com.json` / `chomoand-0.com.json` / `chomoand-1.com.json` … 全URLの coverageState 一覧
  - `chomoand.com_nonindexed_detail.json` … chomoand.com 未インデックス51件の技術詳細（fetch/robots/canonical/lastCrawl）

## 実行コマンド（続きをやる場合そのまま使える）

```bash
# 3サイトそれぞれ（--site-url に sc-domain: を必ず付ける）
python tools/check_search_console.py chomoand.com   --site-url "sc-domain:chomoand.com"   --delay 0.3 --output sc_chomoand.com.json
python tools/check_search_console.py chomoand-0.com --site-url "sc-domain:chomoand-0.com" --sitemap-index "https://chomoand-0.com/sitemap.xml" --delay 0.3 --output sc_chomoand-0.com.json
python tools/check_search_console.py chomoand-1.com --site-url "sc-domain:chomoand-1.com" --sitemap-index "https://chomoand-1.com/sitemap.xml" --delay 0.3 --output sc_chomoand-1.com.json
```

- chomoand.com は Yoast の `sitemap_index.xml` があるので `--sitemap-index` 省略可。
- chomoand-0/-1 は Google Sitemap Generator プラグインで `sitemap.xml`（`sitemap_index.xml` は404）。`post-sitemap.xml` を辿る。
- 所要時間の目安: chomoand.com 140件で約6分、chomoand-1.com 333件で約25分（APIレイテンシ律速。1プロセスずつ推奨、並列だとクォータで遅くなる）。
- **注意**: `python`（`-u` なし）を `nohup ... &` するとログが完全バッファされ最後まで出力ゼロに見える。進捗を見たいときは `python -u` で起動する。

## 調査結果（2026-08-29 時点・全サイト完走）

### chomoand.com（トレンド, 全140記事）

| coverageState | 件数 |
|---|---|
| Submitted and indexed（登録済み） | 89（64%） |
| Crawled - currently not indexed（クロール済み・未登録） | 25 |
| Discovered - currently not indexed（発見のみ・未クロール） | 18 |
| URL is unknown to Google（Google未認識） | 8 |

**未インデックス51件の技術詳細（`chomoand.com_nonindexed_detail.json`）**:

- 25件 = fetch `SUCCESSFUL` / robots `ALLOWED` / indexing `INDEXING_ALLOWED`。→ **技術的な問題なし**。Googleがクロールした上で「載せる価値」判断で保留。
- 26件 = `lastCrawlTime` なし・全状態 `UNSPECIFIED`。→ **一度もクロールされていない**（クロール待ち行列）。
- canonical 不一致 **0件**、noindex **0件**、404 **0件**、5xx **0件**、robots.txt ブロック **0件**、リダイレクトエラー **0件**。

未インデックスURLの偏り: `love-jodou〜`（世が世なら2）・`shuffleisland7-*`・`kyousuki-inchon-*` に集中（直近まとめて投稿した記事群）。
残りは `*_korea` / 学歴・家族系の単発記事。

### chomoand-0.com（ジャニオタ, 全43記事）

| coverageState | 件数 |
|---|---|
| Submitted and indexed | **0** |
| Crawled - currently not indexed | 37 |
| URL is unknown to Google | 6 |

インデックス済みゼロ。既知の問題（[docs/wordpress.md](wordpress.md) の「chomoand-0.comのインデックス未登録問題」）と一致 =
新規ドメインで信頼ゼロ + 公開→ゴミ箱移動を繰り返した履歴 + 公開記事が少なすぎる の複合要因。**技術バグではない**。

### chomoand-1.com（コイキーズ, 全333記事）

| coverageState | 件数 |
|---|---|
| Submitted and indexed | **329（98.8%）** |
| URL is unknown to Google | 3 |
| Discovered - currently not indexed | 1 |

ほぼ健全。未インデックス4件は直近の KO1KEYZ 記事と韓国語版 `/ko/` ページのみ（時間で解決する範囲）。

## 結論 —「エラー」の正体

URL Inspection API で見る限り、**サーバーエラー(5xx)・リダイレクトエラー・404・noindex・robots.txt ブロック・ソフト404 といった“本物のエラー”は3サイトとも1件も無い。**

GSC の「ページのインデックス登録」レポートに大量に並んで見えるのは:

- **「クロール済み - インデックス未登録」**
- **「検出 - インデックス未登録」**

これらは *エラー扱いではなく* Google が「今はインデックスしない」と判断している状態。主因は
①ドメインの新しさ・被リンク不足、②記事の内容が競合に対して薄い/新しすぎる、③クロールバジェット。
→ 個別URLで「登録をリクエスト」を連打しても改善しない（chomoand-0 で実証済み・むしろ逆効果の可能性）。

## まだ確認できていない領域（URL Inspection API の範囲外）

トモキが見ている「エラー」がこちらの可能性もある。次にやるなら:

- [ ] リッチリザルト / 構造化データ エラー（パンくず・記事・FAQ 等）
- [ ] Core Web Vitals（ウェブに関する主な指標）の「不良」URL
- [ ] サイトマップ レポートの「取得できませんでした」
- [ ] 手動による対策 / セキュリティの問題
- [ ] `robots.txt` レポート / HTTPS レポート
- → どのレポートで何色のエラーが出ているか、スクショか文言をもらってから対応する。

## 次のアクション案（インデックス改善）

1. **chomoand.com**: `love-jodou〜`・`shuffleisland7-*` の未クロール群は内部リンクを増やす（既存の関連記事から本文リンク）。サイトマップ再送信。
2. **chomoand.com**: 「クロール済み-未登録」25件は本文加筆（各H3の情報量・独自情報）でリライトしてから再クロール依頼。
3. **chomoand-0.com**: 技術対応では動かない。記事の継続投下と被リンク獲得待ち。登録リクエスト連打はしない。
4. **chomoand-1.com**: 放置で可。`/ko/` ページの内部リンク導線だけ確認。
