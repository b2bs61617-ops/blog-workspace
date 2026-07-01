---
name: youtube-transcript
description: 「この動画を調べて」「動画の内容を確認して」など、YouTube動画の文字起こしを取得してリサーチするときに使う。記事化はしない(別途指示待ち)。
---

# YouTube文字起こし取得スキル

## スクリプトの場所

`youtube_transcript.py`(リポジトリ直下)

## 使い方(PowerShell)

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
python youtube_transcript.py "<YouTubeURL>"
```

出力をファイルに保存する場合:

```powershell
python youtube_transcript.py "<YouTubeURL>" | Out-File -FilePath "transcripts/xxx.txt" -Encoding utf8
```

## 仕様

- YouTube URLまたは動画IDを受け取る
- 日本語字幕を優先取得(なければ英語、それもなければ利用可能な言語を自動選択)
- Python 3.12 + youtube-transcript-api

## 注意事項

- **文字起こし取得後、すぐに記事にしない。調査・確認が目的。記事化はユーザーの指示を待つ。**
- PowerShellのPATHは毎回環境変数から再取得が必要(セッション間でリセットされるため、Windowsの新規インストール直後は特に注意)。

## 関連

- 取得したテキストから学歴・家族・彼氏彼女情報を探すときは[sns-researchスキル](../sns-research/SKILL.md)と組み合わせる。
