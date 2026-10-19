# サイト集計ページ(site-dashboard)

全サイトのPV(アナリティクス)と収益(アドセンス)を1ページにまとめ、スマホで見られるようにするツール(2026-10-19〜)。

- **見る場所**: https://chomoand-3.moe/mypage-stats (パスワード付き固定ページ。合言葉は`G:\マイドライブ\ブログ関係\site-dashboard.json`の`password`)
- **更新**: GEEKOM機のタスクスケジューラ`BlogSiteDashboard`が1時間おきに`site_dashboard.py`を実行して中身を上書き。**このPCの電源が切れている間は更新が止まる**
- chomoand-3.moeは記事・広告なしのサイトなので置き場に使っている(広告が出るページだと自分クリックの危険があるため)。chomoand-3を本格運用するときは、広告がこのページに出ないか確認すること

## 認証のしくみ

| 対象 | 使うもの | 備考 |
|---|---|---|
| アナリティクス | Indexing用サービスアカウント`chomoand-466@...`(`.env`の`GOOGLE_INDEXING_CREDENTIALS_PATH`) | 5サイトのGA4アカウントに「閲覧者」で追加済み。プロジェクトでAnalytics Data API/Admin APIを有効化済み |
| アドセンス | トモキのOAuthトークン`G:\マイドライブ\ブログ関係\adsense-token.json` | AdSense APIはサービスアカウント非対応。OAuthクライアント`adsense-oauth.json`(デスクトップアプリ)で`adsense_auth.py`を1回実行して発行。同意画面は「本番環境」にしてあるのでトークンは期限切れしない |
| ページ更新 | `.env`の`WP_CHOMO3_*` | |

## 新しいサイトを足すとき

1. そのサイトのGA4アカウントに`chomoand-466@model-gearing-465707-d6.iam.gserviceaccount.com`を「閲覧者」で追加
2. `site_dashboard.py`の`SITES`に(表示名, ドメイン, GA4プロパティID, 色)を追加してpush

## 困ったとき

- 「アドセンス取得に失敗」と出たら、トモキがGoogleアカウントで許可を取り消した可能性。`python tools/site-dashboard/adsense_auth.py`を実行してブラウザで許可し直す
- 動作確認だけしたいとき: `python tools/site-dashboard/site_dashboard.py --dry-run`(ページは触らない)
- 「今日」のPVはアナリティクス側の集計遅れで少なめに出る(数時間で追いつく)。「今見ている人」は直近30分のリアルタイム値
