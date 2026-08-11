# ショート動画生成パイプラインのセットアップ手順

**現在の状態(2026-08-11)**: 未セットアップ。このMacには`Homebrew`・`ffmpeg`・`yt-dlp`のいずれも入っていない。実装([tools/shorts/](../tools/shorts/)・[shorts-videoスキル](../.claude/skills/shorts-video/SKILL.md))は完了しているが、下記1・2のインストールをまだ実行していない。

**Why:** [shorts-videoスキル](../.claude/skills/shorts-video/SKILL.md)でKO1KEYZ(chomoand-1.com)の記事をTikTok/YouTube Shorts向け動画に変換するための前提ツール。動画ダウンロードに`yt-dlp`、縦型変換・テキスト焼き込み・BGMミックスに`ffmpeg`を使う。

## 1. Homebrewのインストール(未実施・要トモキ確認)

このMacにはHomebrew自体が入っていない。インストールはシステム全体に影響する操作(`/opt/homebrew`配下にツール群が入る)なので、**マツが実行する前に一声かけてから進める**。

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

インストール後、ターミナルの案内に従って`PATH`にHomebrewを追加する(Apple Siliconなら`/opt/homebrew/bin`)。

## 2. ffmpeg・yt-dlpのインストール

Homebrewが使えるようになったら:

```
brew install ffmpeg
pip3 install yt-dlp
```

確認:
```
ffmpeg -version
yt-dlp --version
```

## 3. 動作確認

KO1KEYZの動画付きX投稿を1件用意し、一連の流れを通してみる:

```
python tools/shorts/clip_downloader.py --url "https://x.com/xxx/status/xxx" --slug test_sample
python tools/shorts/video_maker.py --clips tools/shorts/downloads/test_sample/clip_01.mp4 \
    --text "テスト動画だワン" --out tools/shorts/output/test_sample.mp4
```

`tools/shorts/output/test_sample.mp4`をQuickLook等で再生し、以下を確認する:
- 縦型(9:16、1080x1920)になっているか
- 冒頭にテキストが読める形で焼き込まれているか
- 尺が60秒以内に収まっているか

## Instagram投稿がダウンロードできない場合

Instagramは非公開/ログイン必須の投稿だと`yt-dlp`単体では取得できないことがある。その場合は`clip_downloader.py`がエラーメッセージで案内するので、トモキが手動でダウンロードしたファイルを`tools/shorts/downloads/{slug}/`に置いてから`video_maker.py`のSTEPに進む。

## 使われている場所

- `tools/shorts/clip_downloader.py`: X/Instagramの投稿から動画をダウンロード
- `tools/shorts/video_maker.py`: クリップの縦型変換・結合・テキスト焼き込み・トリム
- [shorts-videoスキル](../.claude/skills/shorts-video/SKILL.md): 上記2つを使った一連のフロー、投稿文言案の作成
- ダウンロード素材・生成物(`tools/shorts/downloads/`・`tools/shorts/output/`)は著作権のある動画のため`.gitignore`でGit管理外(ローカルのみ残す方針)
