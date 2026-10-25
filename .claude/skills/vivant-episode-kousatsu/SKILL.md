---
name: vivant-episode-kousatsu
description: 日曜劇場「VIVANT」をシーズン1第1話から1話ずつ深掘り考察する記事シリーズ(chomoand.com=トレンド速報に下書き)。「VIVANTの○話の考察記事」「次の話やって」で使う。
---

# VIVANT 1話ずつ考察シリーズ

2026-10-25にユカの依頼で開始。ネット上の考察記事・制作側インタビュー・X/Threadsの考察を集め、**それをさらに一段深く考察する**記事をシーズン1第1話から1話ずつ作る。
第2シーズン放送中(2026-07-26〜、通し番号で第11話〜)の速報記事(`build_and_post_vivant_19.py`・`build_and_post_vivant21.py`)とは別シリーズ。

## 進捗(1話書いたらここを更新してcommit)

| 話 | 記事ファイル | WP ID | 状態 | メモ |
|---|---|---|---|---|
| S1第1話 | articles/vivant_s1_01.html | 12636 | 下書き(2026-10-25) | 公開前に「ヴィヴァン＝テントが別班を指す呼び名」の裏取りが必要(マツの記憶ベースで書いた)。第22話(10/25放送)で薫の正体が出たら「Threadsでは第1話の薫に注目」節に追記候補 |
| S1第2話 | — | — | 未着手 | 次回。第1話末尾で「野崎・ドラム・薫との逃走劇の裏の伏線」と予告済み |

## 投稿先

- 「トレンド速報」＝**chomoand.com**(`.env`の`WP_TREND_*`)。カテゴリ37「芸能・トレンド」、author 4、**status=draft**(公開はユーザーの「公開して」待ち)
- ユカのMac(Yuka-MacBook-NEO)はリポジトリ`.env`の`WP_TREND_*`が空欄。ユカの指示で**Googleドライブの`マイドライブ/.env`**を読む: `VIVANT_ENV_FILE="$HOME/Library/CloudStorage/GoogleDrive-b2bs61617@gmail.com/マイドライブ/.env"`。他のPCは自分の`.env`に値があればそのままでよい(値は表示しない)

## 手順

1. `git pull`
2. **リサーチ**(WebSearch/WebFetch)
   - あらすじ: All About ニュース・デイリースポーツ等の放送翌日記事
   - 伏線の公式解説: 飯田和孝Pの解説(マイナビニュース `news.mynavi.jp/article/20230916-2772897/`、リアルサウンド `realsound.jp/movie/2023/09/post-1434779.html` が1〜9話を網羅)。**ここが一番信頼できる**
   - 考察サイト(ciatr等)は宣伝色が強く裏付けが弱いので、制作側解説と食い違えば制作側を優先
   - Filmarksのエピソードレビュー(当時の視聴者の疑問・感想)
3. **X/Threads収集**(Xiy、バックグラウンド実行。macOSに`timeout`コマンドは無いので付けない)
   ```
   cd tools/Xiy
   python3 x_collector.py --keyword "VIVANT ○話 考察" --tab top --no-ai --out posts_YYYYMMDD_vivant_s1eN_x
   python3 x_collector.py --keyword "VIVANT ○話 伏線" --tab top --no-ai --out posts_YYYYMMDD_vivant_s1eN_x2
   python3 x_collector.py --site threads --keyword "VIVANT ○話 考察" --no-ai --out posts_YYYYMMDD_vivant_s1eN_threads
   ```
   第2シーズン放送中は「S1の○話を見返したら〜」という投稿が多く、S2とのつながりのネタになる。誤情報混じりでも拾い、記事では「〜という声」として扱う
4. **執筆** `articles/vivant_s1_NN.html`(第1話の構成を型にする)
   - リード(結論先出し＋「最終回までのネタバレを含みます」)→この記事でわかること→あらすじ表→**見返すと気づく伏線**(制作側解説ベース)→**このブログの考察**(ネット記事より一歩先の独自解釈。必ず「ここからはこのブログの考察です」と明示)→**第2シーズンにつながる要素**(表)→**X/Threadsの考察**(放送当時の声と2026年の声を分ける)→見返すときの注目ポイント→まとめ(&#10003;リスト)→次回予告
   - 5,000字前後。句点後`<br>`、`<hr>`は使わない、全角「？」「！」
   - 第2シーズンの展開は `articles/vivant21_*.html` / `vivant_0*.html` に書いた事実の範囲で使う(推測で足さない)
5. **投稿**: `build_and_post_vivant_s1_01.py` をコピーして `ARTICLES`(ファイル名・タイトル・スラッグ)と `IDS_FILE` を書き換え、実行
   ```
   VIVANT_ENV_FILE=... PYTHONUTF8=1 python3 build_and_post_vivant_s1_NN.py
   ```
   アイキャッチは`tools/eyecatch_chomoand0.py --title`で自動生成(スクリプト内)。Mac標準のpython3は3.9なので、f-stringの`{}`内にバックスラッシュを書かない
6. この表の進捗を更新 → `git add`(該当ファイルだけ)→`git status`確認→commit→push

## タイトルの型

`VIVANT○話の伏線を考察！見返すと分かる＜その回の核心＞` (スラッグ `vivant-season1-episodeN-fukusen`)
