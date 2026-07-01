---
name: trend-research
description: 「トレンドを調べて」「今日の話題は?」など、今日のトレンド・話題を調査するときに使う。Yahoo JAPANのニュース面とYahoo!リアルタイム検索を取得してまとめる。
---

# トレンド調査スキル

## 1. 今日のニュース面(記事ネタ探しの基本)

以下のYahoo JAPANページを**並列で**WebFetchして取得する。

| カテゴリ | URL |
|---|---|
| トップ(主要) | https://news.yahoo.co.jp/topics/top-picks |
| エンタメ | https://news.yahoo.co.jp/topics/entertainment |
| スポーツ | https://news.yahoo.co.jp/topics/sports |
| 経済 | https://news.yahoo.co.jp/topics/business |

各ページへのプロンプト: 「表示されているニュース記事のタイトルを全部箇条書きでリストアップして」

出力はカテゴリ別に箇条書きでまとめ、ブログ記事候補をピックアップしてユーザーに提案する。

## 2. Xの急上昇ワードをリアルタイムで取得したい場合

**Yahoo!リアルタイム検索**が最も安定して取得できる(X APIなし・無料)。

- WebFetchで `https://search.yahoo.co.jp/realtime` にアクセスすると急上昇ワード・トレンド1〜20位が取得できる。

過去日付のトレンドを調べたい場合は**トレンドカレンダー**を使う: `https://jp.trend-calendar.com/trend/YYYY-MM-DD.html`(ただし当日分は反映が遅れることがある)。

## 関連スキル

- テレビ番組から旬な人物を探す場合は [tv-research](../tv-research/SKILL.md)
- タイトルの付け方は [trend-title](../trend-title/SKILL.md)
