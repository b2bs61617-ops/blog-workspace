---
name: shorts-video
description: 「ショート動画にして」「TikTok用の動画作って」「Shorts化して」と言われたときに使う。KO1KEYZ(chomoand-1.com)の記事をTikTok/YouTube Shorts向けの縦型ショート動画に変換する。試験導入としてコイキーズのみ対象。
---

# ショート動画生成スキル(試験導入・コイキーズ限定)

**対象は chomoand-1.com(コイキーズ)の記事のみ**。chomoand.com・chomoand-1.com以外(トレンド・ジャニオタ)は今回の試験導入では対象外(動作確認が済んだら拡大を検討する)。

**投稿(TikTok/YouTube Shortsへのアップロード)は自動化しない。** 動画ファイルの生成までを自動で行い、アップロードはトモキが手動で行う(TikTok Content Posting APIは事前のアプリ審査が必要でハードルが高いため、他のSNS連携と同じく自動化できる部分から段階導入する方針)。

## 前提条件

`ffmpeg`・`yt-dlp`が必要。未セットアップの場合は先に[docs/shorts-video-setup.md](../../../docs/shorts-video-setup.md)の手順を案内する。

## 著作権・規約についての注記(毎回必ず伝える)

このスキルは、記事執筆時にXiyで収集したX/Instagramの投稿動画を切り出して再編集する仕組み。他人が投稿した動画をトリミング・加工して別プラットフォーム(TikTok/YouTube Shorts)に自分のコンテンツとして投稿する形になるため、**著作権侵害・各プラットフォーム規約違反のリスクをトモキが承知の上で運用する**という前提(2026-08-11、ユーザーが方針として選択)。動画を生成するたびに、この点を一言添えて報告する。

## 実行フロー

### STEP1: 対象記事と動画ソースの特定

- 対象記事(タイトルまたは記事ID)を確認する
- その記事を書いたときに使った`tools/Xiy/posts_*/posts.txt`(または`sns-research`スキルでの収集結果)から、**動画付きのX投稿URL**を探す
  - 見つからない場合、またはXiyの収集データが動画の有無を明示していない場合は、ユーザーに動画ソースのURLを確認する
- 複数の動画候補がある場合は、記事の一番のフック(見どころ)に合う1〜3本を選ぶ(長すぎる動画は避ける。合計尺はSTEP3で60秒にトリムされる)

### STEP2: クリップのダウンロード

`tools/shorts/clip_downloader.py`で動画をダウンロードする:

```
python tools/shorts/clip_downloader.py --url "{投稿URL}" --slug {記事slug}
```

- `--slug`には[blog-upload/STEP2](../blog-upload/SKILL.md)で使った記事スラッグを使う(`tools/shorts/downloads/{slug}/clip_01.mp4`のように自動保存される)
- 複数クリップが必要な場合は投稿URLごとにこのコマンドを繰り返す(`clip_02.mp4`...と自動採番される)
- Instagram投稿でダウンロードに失敗した場合(非公開/ログイン必須の投稿でありがち)は、トモキに手動ダウンロードを依頼し、`tools/shorts/downloads/{slug}/`に置いてもらってから次に進む

### STEP3: 動画の編集(縦型変換・テキストオーバーレイ)

冒頭に焼き込むフック文を作る。文体は[publish/SKILL.mdの「Xの投稿文の作り方」](../publish/SKILL.md#xの投稿文の作り方)の型を流用し、記事タイプに応じた煽り・疑問形にする(絵文字は使わない、[docs/rules.md](../../../docs/rules.md)の文体ルールに準拠)。

`tools/shorts/video_maker.py`で編集する:

```
python tools/shorts/video_maker.py --clips tools/shorts/downloads/{slug}/clip_01.mp4 [clip_02.mp4 ...] \
    --text "{フック文}" --out tools/shorts/output/{slug}.mp4
```

- 複数クリップは結合され、9:16(1080x1920)にスケール+パディングされる
- 合計尺は自動で60秒にトリムされる
- BGMは既定でなし。トモキが用意した音源ファイルがあれば`--bgm {パス}`で指定する(著作権フリー音源は同梱していない)

### STEP4: 投稿案内(手動アップロード)

完成した動画ファイル(`tools/shorts/output/{slug}.mp4`)のパスをユーザーに提示し、以下を一緒に案内する:

- **TikTok用キャプション・ハッシュタグ案**: publishスキルのXの投稿文パターンを踏まえた短いキャプション+2〜4個のハッシュタグ
- **YouTube Shorts用タイトル・説明文案**: 記事タイトルをベースにした疑問形タイトル、説明文に記事URLを含める
- アップロードは**トモキが手動**でTikTokアプリ・YouTube Studioから行う旨を案内する(自動投稿は今回のスコープ外)
- 著作権・規約についての注記(上記)を添える

## How to apply

「ショート動画にして」「TikTok用の動画作って」「Shorts化して」などの発言をトリガーとして、STEP1〜4を順番に実行する。対象は現状コイキーズ(chomoand-1.com)の記事のみ。他サイトの記事を頼まれた場合は、試験導入中である旨を伝えた上でユーザーの判断を仰ぐ。
