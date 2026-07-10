# YouTube Data APIのセットアップ手順

chomoand.comの新方針(TikTok/YouTube発バズインフルエンサーの学歴・経歴wiki、[docs/chomoand-pivot.md](chomoand-pivot.md)参照)のための「旬な人物発見」の情報源として、YouTube急上昇動画をAPI経由で取得する仕組み(`tools/youtube_trending.py`)の初回セットアップ手順。

**Why:** YouTubeの急上昇ページ・TikTok Creative CenterはどちらもJS描画のため、WebFetchでは中身が取得できない(2026-07-06確認)。YouTube Data API v3を使えば急上昇動画・チャンネルを安定して構造化データで取得できる。TikTokには同等の公式APIがなく、当面は後回し。

## 1. APIキーの発行(トモキ本人が実施)

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス(既存のGoogleアカウントでログイン)
2. プロジェクトを選択または新規作成
3. 「APIとサービス」→「ライブラリ」で「YouTube Data API v3」を検索して有効化
4. 「APIとサービス」→「認証情報」→「認証情報を作成」→「APIキー」で発行
5. 発行したキーの「アプリケーションの制限」「API制限」から、**API制限を「YouTube Data API v3」のみに絞る**(不正利用対策)
6. 発行したキーを`.env`の`YOUTUBE_API_KEY`に設定する

マツ(Claude Code)はこのAPIキーの値をチャットで教えたり代筆したりしないので、上記はユーザー自身の作業になる。

## 2. 動作確認

```
python tools/youtube_trending.py
```

日本の急上昇動画が「チャンネル名・タイトル・再生数」付きで一覧表示されれば設定完了。同じチャンネルが複数本ランクインしている場合は件数を注記する(tv-researchの「複数回登場は旬度が低い」フィルタと同じ発想)。

## 3. 無料枠について

YouTube Data API v3は1日10,000ユニットの無料枠があり、`videos.list`は1回あたり数ユニット程度なので、通常の調査頻度(1日数回)では枠を超える心配はほぼない。

## 使われている場所

- `tools/youtube_trending.py`: 急上昇動画取得スクリプト本体
- 発見の仕組み・記事化の型は今後スキルとして整備予定([docs/chomoand-pivot.md](chomoand-pivot.md)の未解決事項参照)
