# 新しいPCでのセットアップ手順

このリポジトリを別のPC(自分の別マシン、または共同作業者のPC)で使い始めるときの手順です。

## 1. 前提

- GitHubの非公開リポジトリへのアクセス権(コラボレーターとして招待されていること)
- Claude Code(松)がインストール済みであること

## 2. Gitのインストール

PowerShellで:
```powershell
winget install --id Git.Git -e --source winget
winget install --id GitHub.cli -e --source winget
```
インストール後、一度PowerShellを開き直す(またはPATHを再読み込みする)。

## 3. Git・GitHubの認証設定

```powershell
git config --global user.name "<自分の名前>"
git config --global user.email "<自分のメールアドレス>"
gh auth login
```
`gh auth login`はブラウザでコードを入力する認証フロー。指示に従って進める。

## 4. リポジトリのクローン

デスクトップなど好きな場所で:
```powershell
gh repo clone b2bs61617-ops/blog-workspace "ブログ作業場"
cd "ブログ作業場"
```

## 5. 秘密情報のローカル設定(重要)

Gitには含まれていないため、以下を手動で作成する。値は**Gitではなく**パスワードマネージャーなど別の安全な経路で受け取ること。

**`.env`**(リポジトリ直下。`.env.example`をコピーして値を埋める):
```powershell
Copy-Item .env.example .env
notepad .env
```
`WP_TREND_*` / `WP_AUDITION_*` / `WP_KOIKEYS_*` の3サイト分のURL・ユーザー名・アプリパスワードを入力する。

**`tools/Xiy/xiy_config.json`**(`xiy_config.json.example`をコピーして値を埋める):
```powershell
Copy-Item tools\Xiy\xiy_config.json.example tools\Xiy\xiy_config.json
notepad tools\Xiy\xiy_config.json
```
`gemini_api_key`を入力する。

## 6. Xiyツールの動作環境(Python)

Xiyツール(`tools/Xiy/`)はPython 3.12を使う。未インストールなら:
```powershell
winget install --id Python.Python.3.12 -e --source winget
```
必要なパッケージ:
```powershell
py -3 -m pip install pillow requests playwright google-genai yt-dlp youtube-transcript-api faster-whisper
py -3 -m playwright install chromium
```
初回起動時にブラウザでX/Instagramへのログインを求められる。ログイン情報は`%USERPROFILE%\x_collector_profile`にPCごとに個別保存されるので、**PCごとに1回ログインが必要**。

`tools/Xiy/起動.bat`をダブルクリックすると起動する。

## 7. KO1KEYZ監視ツール(任意・コイキーズ担当PCのみ)

コイキーズブログのリライト用に、X(Twitter)上のKO1KEYZメンバー新着投稿を毎日自動チェックするツール([koikeyz-rewriteスキル](../.claude/skills/koikeyz-rewrite/SKILL.md)参照)。

```powershell
py -3 -m pip install playwright requests
py -3 -m playwright install chromium
```

初回のみXへのログインが必要:
```powershell
cd tools\koikeyz-monitor
py -3 login_x.py
```
ブラウザが開くのでXにログインし、ターミナルでEnterキーを押す。

その後、Windowsタスクスケジューラで`tools\koikeyz-monitor\x_monitor.py`を毎朝7時に自動実行するタスク(`KO1KEYZ-Monitor`)を登録する。セットアップ済みのPCの設定を参考にするか、以下で登録できる:
```powershell
$pyPath = (Get-Command py).Source
$action = New-ScheduledTaskAction -Execute $pyPath -Argument '-3 "x_monitor.pyへのフルパス"' -WorkingDirectory "tools\koikeyz-monitorへのフルパス"
$trigger = New-ScheduledTaskTrigger -Daily -At 7:00AM
Register-ScheduledTask -TaskName "KO1KEYZ-Monitor" -Action $action -Trigger $trigger -Description "KO1KEYZメンバー12人のX新着投稿を毎日チェック"
```

## 8. 動作確認

- Claude Code(松)をリポジトリ直下(`ブログ作業場`フォルダ)で起動し、`CLAUDE.md`が読み込まれ「松」として振る舞うか確認する
- `.claude/skills/`配下のスキル(例: wiki-article)を使う作業を試す
- WordPress投稿テスト: `python wp_upload_batch.py`(対象記事を書き換えてから)、またはチャットで「ブログにアップして」と依頼して[blog-uploadスキル](../.claude/skills/blog-upload/SKILL.md)が動くか確認
- `tools/Xiy/起動.bat`でXiyツールが起動するか確認

## 9. 日常の運用

- 作業を始める前に必ず `git pull`
- 新しいスキル・ルールを学んだら `CLAUDE.md` / `docs/` / `.claude/skills/` に反映し、`git add` → `git commit` → `git push`(pushは内容を確認してから)
- 記事下書き・画像などの成果物も同じリポジトリにコミットして他PCと共有する
