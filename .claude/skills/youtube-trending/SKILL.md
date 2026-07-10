---
name: youtube-trending
description: 「旬なYouTuber/TikTokerを探して」など、chomoand.comの新記事(バズインフルエンサーの学歴・経歴wiki)のネタになる人物を発見するときに使う。YouTube急上昇動画から旬な人物を絞り込む。
---

# YouTube急上昇・旬な人物発見スキル

chomoand.comの新方針(TikTok/YouTube発バズインフルエンサーの学歴・経歴wiki、[docs/chomoand-pivot.md](../../../docs/chomoand-pivot.md)参照)のためのネタ探しスキル。

## 前提

`YOUTUBE_API_KEY`が`.env`に未設定の場合は使えない。未設定なら[docs/youtube-api-setup.md](../../../docs/youtube-api-setup.md)のセットアップ手順をユーザーに案内する(APIキー発行はユーザー本人が行う。マツは代筆・入力しない)。

## 手順

1. `python tools/youtube_trending.py`を実行し、日本の急上昇動画上位50件(チャンネル名・タイトル・再生数)を取得する。
2. 下記の「対象外にする動画」ルールで除外する。
3. 下記の「省く人物」ルールでフィルタリングする。
4. 残った人物(チャンネル)を、話題性・記事化のしやすさ順にユーザーに提案する。

## 対象外にする動画(ジャンルフィルタ)

- 企業・メディアの公式チャンネル(ニュース番組の切り抜き、公式MV、企業広告など)
- ゲーム実況・楽曲そのものが主役で「人物」が主役でない動画
- 声優・アニメ公式チャンネル(wiki-article/gakureki-kazoku-kanojoスキルの対象外)

対象にするのは「個人またはグループ本人が主役で、TikTok/YouTube発で知名度を得ている(または急上昇している)人物」。

## 省く人物のルール

**目的:** 既に大量に記事・wikiがある大物YouTuber/TikTokerは検索流入の伸びしろが薄いため、まだ情報が薄い旬な人物に絞る(tv-researchスキルと同じ発想)。

**① 固定除外リスト(毎回省く):** ヒカキン、はじめしゃちょー、フィッシャーズ、東海オンエア、コムドット、水溜りボンド、きまぐれクック、その他登録者数トップクラスで既に多数のwiki・まとめ記事が存在する大手YouTuber/TikTokerグループ。ユーザーから追加指示があれば随時更新する。

**② 動的フィルタ:** `tools/youtube_trending.py`の出力で「同チャンネル複数本ランクイン」の注記が付いている場合、継続的に話題になっている=既にある程度知名度が定着している可能性が高いので、優先度を下げる(完全除外はしない)。

## 注意事項

- YouTube急上昇はジャンルが幅広いため、人物系以外(音楽MV、企業広告等)が混ざる前提でフィルタリングすること。
- TikTok単体の急上昇は現時点で自動取得の手段がない(TikTok Creative CenterはJS描画でWebFetch不可、2026-07-06確認)。YouTube経由で見つかる人物のうちTikTok発の人物も含まれることを期待する運用。
- 記事化の型(wiki-article/gakureki-kazoku-kanojoの流用 or 専用スキル新設)は別途検討中([docs/chomoand-pivot.md](../../../docs/chomoand-pivot.md)の未解決事項参照)。
