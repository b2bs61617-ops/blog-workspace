# ショート動画生成パイプラインのセットアップ手順

**現在の状態(2026-08-11)**: セットアップ完了・動作確認済み。このMacにHomebrew・`ffmpeg-full`・`yt-dlp`を導入し、実際にKO1KEYZ関連のX投稿動画1本でダウンロード→縦型変換→テキスト焼き込みの一連の流れを確認した(下記3の実績)。

**Why:** [shorts-videoスキル](../.claude/skills/shorts-video/SKILL.md)でKO1KEYZ(chomoand-1.com)の記事をTikTok/YouTube Shorts向け動画に変換するための前提ツール。動画ダウンロードに`yt-dlp`、縦型変換・テキスト焼き込み・BGMミックスに`ffmpeg`を使う。

## 1. Homebrewのインストール

システム全体に影響する操作(`/opt/homebrew`配下にツール群が入る)で、かつ管理者(sudo)権限が必要なため、**トモキ本人がターミナルで実行する**(2026-08-11実施済み・このMacでは完了)。

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

新しいPCでセットアップする場合、インストール後に`~/.zprofile`へ以下を追加する(このMacでは追加済み):
```
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## 2. ffmpeg-full・yt-dlpのインストール

**注意: 標準の`ffmpeg`フォーミュラには`drawtext`フィルタ(テキスト焼き込みに必須)が入っていない**(freetype/fontconfigがビルドに含まれていないため、`brew install ffmpeg`だけだと`No such filter: 'drawtext'`で失敗する。2026-08-11判明)。必ず`ffmpeg-full`を入れる。

```
brew install ffmpeg-full
pip3 install yt-dlp
```

`ffmpeg-full`は`ffmpeg`と衝突するためkeg-only(自動でPATHに乗らない)。`~/.zshrc`へ以下を追加する(このMacでは追加済み):
```
export PATH="/opt/homebrew/opt/ffmpeg-full/bin:$PATH"
```

確認:
```
ffmpeg -version
ffmpeg -filters | grep drawtext   # 何か表示されればOK
yt-dlp --version
```

## 3. 動作確認(2026-08-11実施済み)

KO1KEYZ関連のX投稿(KEITOナイトルーティン動画の転載、69.9秒)で実際に通した:

```
python tools/shorts/clip_downloader.py --url "https://x.com/xxx/status/xxx" --slug test_sample
python tools/shorts/video_maker.py --clips tools/shorts/downloads/test_sample/clip_01.mp4 \
    --text "美顔器がスゴい:これマジ!?" --out tools/shorts/output/test_sample.mp4
```

`ffprobe`で出力(`tools/shorts/output/test_sample.mp4`)を確認した結果:
- 1080x1920(縦型9:16)、h264、59.97秒(60秒トリム通り)
- フレームを切り出して目視確認、冒頭のテキストオーバーレイ(コロン込みのエスケープ処理も含め)が正しく焼き込まれていることを確認済み

**注意点(判明した制約)**:
- 全てのX投稿に動画があるわけではない(画像のみの投稿も多い)。事前にXiyの収集データや投稿を目視で確認してから動画付きの投稿URLを選ぶこと
- 一部のツイート(KO1KEYZ公式アカウントの投稿で発生)で`HTTP Error 403: Forbidden`になるケースを確認した。原因未特定(投稿ごとに発生有無が変わる、ログイン必須の設定やyt-dlp側の一時的な問題の可能性)。失敗した場合は別の投稿URLで試すか、時間を置いて再試行する

## Instagram投稿がダウンロードできない場合

Instagramは非公開/ログイン必須の投稿だと`yt-dlp`単体では取得できないことがある。その場合は`clip_downloader.py`がエラーメッセージで案内するので、トモキが手動でダウンロードしたファイルを`tools/shorts/downloads/{slug}/`に置いてから`video_maker.py`のSTEPに進む。

## 使われている場所

- `tools/shorts/clip_downloader.py`: X/Instagramの投稿から動画をダウンロード
- `tools/shorts/video_maker.py`: クリップの縦型変換・結合・テキスト焼き込み・トリム
- [shorts-videoスキル](../.claude/skills/shorts-video/SKILL.md): 上記2つを使った一連のフロー、投稿文言案の作成
- ダウンロード素材・生成物(`tools/shorts/downloads/`・`tools/shorts/output/`)は著作権のある動画のため`.gitignore`でGit管理外(ローカルのみ残す方針)
