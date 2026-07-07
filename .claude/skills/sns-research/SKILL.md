---
name: sns-research
description: ネット上に情報がない人物の学歴・家族・出身地などを、X/InstagramやYouTubeから掘り起こして調査するときに使う。「ずらし記事」の情報源。
---

# SNS調査スキル(ずらし記事の情報収集)

## 大前提

「情報がないので分かりません」と書く記事は価値ゼロ。書かない。ネット上にない情報はSNSを掘って自分で見つける。

**Why:** 大手・強いブロガーはSNSやYouTubeを深掘りしない。ここに差別化の余地がある。

## 調査ツール: Xiy

`tools/Xiy/起動.bat` で起動するX/Instagram投稿収集ツール(詳細は[reference/Xiyツール](#xiyツールの詳細)を参照)。人物のアカウントを指定すると投稿・画像・日時を一括収集できる。

## SNSから読み取れる情報の例

| 探したい情報 | SNSの手がかり |
|---|---|
| 高校・学歴 | 制服姿の写真、「卒業式」「文化祭」投稿、友人のコメント |
| 出身地・実家 | 「地元に帰った」「〇〇祭り」「方言」投稿 |
| 両親の職業 | 「親の仕事手伝い」「実家の写真」投稿 |
| 兄弟姉妹 | タグ付け、「妹と」「兄と」コメント、家族写真 |
| 歴代彼氏・彼女 | 昔の2ショット、「〇〇くんと」コメント、削除済み投稿 |
| 趣味・特技 | 日常投稿の内容 |

## YouTubeからも情報を掘る

| 動画の種類 | 読み取れる情報 |
|---|---|
| インタビュー・トーク番組 | 「実家が〇〇で…」「高校の時に…」等の発言 |
| バラエティ出演 | 家族・兄弟・出身地エピソード |
| 本人のYouTubeチャンネル | 日常投稿の中に学歴・家族情報が混入 |
| コメント欄 | ファン・関係者の書き込みにヒントあり |

動画は[youtube-transcriptスキル](../youtube-transcript/SKILL.md)で全テキスト化して情報を一括抽出する。

## 調査の流れ

1. トレンド人物のX・Instagramアカウントを特定 → Xiyツールで一括収集
2. 過去投稿・画像・コメントを時系列で遡って痕跡を探す
3. YouTubeで本人出演動画を検索 → 文字起こしスキルでテキスト化して情報抽出
4. 見つけた情報をずらし記事の根拠として使う

**How to apply:** ずらし記事を書く前に必ずXiy+YouTube文字起こしで対象人物を調査する。

## Xiyツールの詳細

- スクリプト: `tools/Xiy/x_collector.py`
- 起動ファイル: `tools/Xiy/起動.bat`(ダブルクリックで起動)
- ブラウザプロファイル: `%USERPROFILE%\x_collector_profile`(ログイン情報保存。PCごとに個別に必要)
- 設定ファイル: `tools/Xiy/xiy_config.json`(Gemini APIキー。Gitには含めない。`xiy_config.json.example`参照)

**機能:**
- URLを貼り付けて「収集開始」→ 自動スクロール&収集
- X: 投稿テキスト・日時・画像(原寸 `name=orig`)を取得
- Instagram: グリッドを左上から順にクリック→モーダルから画像・キャプション・日時を取得
- URL自動判定(x.com → Xモード、instagram.com → Instagramモード)
- YouTube URL入力時は文字起こし・チャンネル動画一覧取得・AI要約(Gemini)にも対応
- 取得完了時に音+ポップアップ通知、「保存」ボタンでテキスト+画像ファイルを書き出し

**使用技術:** Python 3.12 + tkinter(GUI)、Playwright + システムChrome + playwright-stealth(Bot検知対策)、Pillow + requests、yt-dlp、youtube-transcript-api、faster-whisper、google-genai

### X収集が0件になる場合のトラブルシュート(2026-07-07判明・解決済み)

「Xで検索しても投稿が0件のまま終わる」問題を調査したところ、原因は2つ絡んでいた。**現在はどちらも修正済み**で、実際に「釼持 吉成」で検索し780件の実ツイートを収集できることを確認済み。

1. **セレクタが古かった(本質的な原因)**: `collect_x`が記事要素を`article[data-tweet-id]`で探していたが、Xの現行DOMにはその属性が無く、ログイン状態やBot検知に関係なく常に0件になっていた。正しくは`article[data-testid="tweet"]`(本文は`[data-testid="tweetText"]`)。今後またXのDOM変更で0件病が再発したら、まずここ(実際のページのHTMLをダンプしてセレクタが現行DOMと一致しているか)を疑うこと。
2. **Bot検知**: 実際にはJSは動いているのに`navigator.webdriver`等の自動化フィンガープリントを見て「JavaScriptを使用できません」という偽のブロックページを返してくることがある。対策として`playwright-stealth`でブラウザ起動時にフィンガープリントを偽装している。それでも0件が続く場合は自動アクセスを一旦止めて、手動でXiy(GUI)からログイン状態のブラウザで普通に閲覧し、しばらく間を空けてから再試行する。
3. 未ログイン状態で検索すると投稿が表示されないため、`collect_x`/`collect_trending`はログイン済みナビ要素(`SideNav_AccountSwitcher_Button`等)の有無を見て、未ログインなら最大180秒待機してから収集ループに入る(`wait_for_x_login`)。これにより、ログイン画面の入力中にブラウザが自動で閉じることも無くなった。

### CLIモード(マツが直接自動実行する場合)

GUIを開かず、キーワードやURLを渡すだけでX/Instagramの収集→保存(→AI分析)まで自動実行できる(2026-07-07追加)。「Xで〇〇を調べて」のように頼まれたら、Xiyを起動して手動操作してもらうのではなく、まずこちらを使う。

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
python tools/Xiy/x_collector.py --keyword "釼持吉成"
```

- `--keyword "語句"`: Xでキーワード検索(デフォルトは「最新」タブ`f=live`。「話題のツイート」で見たい場合は`--tab top`)
- `--url "https://x.com/..."` / `--url "https://instagram.com/..."`: キーワードの代わりにURLを直接指定(プロフィールページ・検索結果ページなど)
- `--out "保存先ディレクトリ"`: 省略時は`tools/Xiy/posts_日時_キーワード/`に自動保存
- `--no-ai`: Gemini AI分析(プライベート情報抽出)をスキップする。省略時は`xiy_config.json`にAPIキーがあれば自動実行
- 新着投稿が10秒来なくなったら自動で収集終了。ブラウザウィンドウは(ボット判定回避のため)表示されるが、クリック操作は不要
- ログイン済みプロファイル(`%USERPROFILE%\x_collector_profile`)をGUIモードと共用するので、事前にGUIで一度ログインしておく必要がある

GUIモード(`起動.bat`)は従来通り引数なしで起動すれば使える。収集・保存・AI分析のロジックは内部でCLIと共通化されている。
