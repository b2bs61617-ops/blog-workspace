# wp-mu-plugins/

WordPress の **must-use プラグイン**（`wp-content/mu-plugins/` に置くと有効化操作なしで常時読み込まれる）。
リポジトリでバージョン管理し、各サイトへは手動で設置する（REST では入れられないため）。

| ファイル | 対象サイト | 役割 |
|---|---|---|
| `ko1keyz-i18n-autolink.php` | chomoand-1.com | `-kr` / `-en` slug 命名規則から JP/KR/EN を Polylang 翻訳グループへ自動紐付け（hreflang 出力のため）。`wp_after_insert_post` フック。 |

## ko1keyz-i18n-autolink.php

**なぜ必要か**: Polylang 3.8.7 free では WP REST API（`wp/v2/posts`）で `translations` フィールドを送っても
翻訳グループが保存されない（2026-09-09 検証）。blog-upload STEP6/7 で韓国語版・英語版を作っても
hreflang が出ないため、save 時に `pll_save_post_translations()` を代行する。

**前提**: KR は `{base}-kr` + Polylang 言語 `ko`、EN は `{base}-en` + 言語 `en`、JP は `{base}`。
言語割り当て自体は既存フロー（REST の `lang` 指定）で行われている前提で、言語未設定の記事や
命名規則外の slug には触らない（誤爆防止）。

**設置手順**:
1. chomoand-1.com の `wp-content/mu-plugins/`（無ければ作成）に `ko1keyz-i18n-autolink.php` をアップロード
2. mu-plugin は自動有効。管理画面「プラグイン」→「Must-Use」に表示される
3. 確認: 適当な JP 記事を開いて `<head>` に `<link rel="alternate" hreflang="ja">` と
   `hreflang="ko"` / `hreflang="en"`（EN 未作成なら ja/ko の2行）が出ていれば OK

**既知の制限**: slug 衝突で相手が `{base}-kr-2` 等になった場合は完全一致検索から漏れる。
その分は `tools/check_translation_gaps.py` で洗い出して手動対応。

**関連**: [docs/korea-expansion.md](../../docs/korea-expansion.md)（「hreflang（翻訳グループ紐付け）」の節）
