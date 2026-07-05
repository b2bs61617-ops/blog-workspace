---
name: koikeyz-rewrite
description: コイキーズブログ(chomoand-1.com)の既存記事をリライトするときに使う。対象範囲・実行フロー・監視ツールの使い方をまとめたルール。
---

# コイキーズ既存記事リライトスキル

## 対象範囲(重要)

**KO1KEYZの正式デビューメンバー12人、またはグループ全体に関する記事のみ**をリライト対象にする。

デビューできなかった元練習生(脱落者)個人の記事はリライトしない。読まれる見込みが薄く、労力に見合わないため。

デビューメンバー12人(2026年6月確定):
加藤大樹・矢田佳暉・パク・シヨン・オ・シンヘン・後藤結・柳谷伊冴・小野慶人・安部結蘭・飯塚亮賀・杉山竜司・照井康祐・濱田永遠

判定方法: タイトルに上記メンバー名、または「KO1KEYZ」「コイキーズ」が含まれる記事が対象。

## リライトの実行フロー(重要)

1. 対象記事の現在の本文をWordPress REST API(`context=edit`)で取得
2. 最新情報をリサーチ(WebSearch、または後述の監視ツールのレポート)して裏取りする
3. **リライト内容(何をどう変えるか)を先にチャットで報告し、ユーザーのOKを待ってから実行する。** 1記事ずつ、都度確認する運用(2026-07-04にユーザーから指示)。報告と同時に`tools/line_notify.py`でLINE通知を送る(例:`python tools/line_notify.py "コイキーズ記事「{タイトル}」のリライト提案があるワン、確認してほしいワン"`)。`.env`に`LINE_CHANNEL_ACCESS_TOKEN`/`LINE_USER_ID`が未設定の場合は通知はスキップされるだけなので、そのまま作業を続けてよい。
4. OKが出たらWordPress REST API(`POST /wp-json/wp/v2/posts/{id}`)で`content`を直接更新する。既に公開済みの記事なので下書き経由は不要([docs/wordpress.md](../../../docs/wordpress.md)の「更新/リライトは確認不要で実行してよい」に該当)。更新が成功したら`tools/line_notify.py`でLINE通知を送る(例:`python tools/line_notify.py "コイキーズ記事「{タイトル}」を更新したワン https://chomoand-1.com/?p={ID}"`)。
5. **タイトル・スラッグは基本変更しない。** 公開済み記事のSEO評価(検索順位・被リンク)を守るため。よほど明確な改善がある場合のみユーザーに相談する。
6. 文体ルール(句点ごとの`<br>`改行など)は[docs/rules.md](../../../docs/rules.md)に従う。

## 目安の文字数

ルール上は最低2,500字が目安([docs/rules.md](../../../docs/rules.md))。ただし家族構成など実際の情報量が少ないテーマでは、事実を捏造せず確認できる範囲で最大限厚くすればよく、無理に2,500字に到達させる必要はない。

## 新着情報の監視ツール(tools/koikeyz-monitor/)

X(Twitter)でメンバー12人+グループ名を毎日検索し、新着投稿を検知する専用ツール。`tools/Xiy/`(手動操作用の普段使いツール)とは別物、完全に独立している。

- **スクリプト**: `tools/koikeyz-monitor/x_monitor.py`
- **ログイン**: `tools/koikeyz-monitor/login_x.py`を一度手動実行してXにログイン(PCごとに1回、`%USERPROFILE%\koikeyz_monitor_profile`にブラウザプロファイル保存)
- **実行頻度**: Windowsタスクスケジューラで毎朝7時に自動実行(タスク名: `KO1KEYZ-Monitor`)。ログイン状態がPC固有なため、このPC上でのみ動作する。
- **差分検知**: `monitor_state.json`に前回までの投稿IDを保存し、新着分だけを`monitor_reports/report_*.json`に出力する
- **ノイズ除外**: トレカ交換・好き顔診断コピペ・アフィリエイト広告(`#PR`等)・同行募集などの定型ノイズはレポート生成前にスクリプト側(正規表現)で除外し、同一告知文の重複投稿も1件にまとめる(マツが読むトークン量削減のため、2026-07-05追加)
- **AI要約(Gemini)**: `monitor_config.json`(`monitor_config.json.example`をコピーして`gemini_api_key`を設定、Git管理外)にGemini APIキーがあれば、ノイズ除外後のデータをGeminiに渡し「記事に使えそうな情報」だけの要約(`report_*.summary.txt`)を作る。マツはこの要約を優先して読み、最終確認だけ行う。**APIキー未設定、またはクォータ超過などで失敗した場合は自動的に生データ(`report_*.json`)のみの出力にフォールバックする**(2026-07-05追加。GeminiのクォータとAnthropic側のトークン使用量は別枠なので、Geminiが落ちてもマツの動作自体は止まらない)。
- **セッション開始時の報告**: `.claude/koikeyz-monitor-check.ps1`(SessionStartフック)が未処理レポートを検知すると、マツが自動で`.summary.txt`(あれば優先)または`.json`を読み込み、記事に使えそうな情報だけ抽出して報告する。報告後は該当ファイルを`monitor_reports/processed/`に移動する。
- `monitor_state.json`・`monitor_config.json`・`monitor_reports/`はPCローカルの生成データ・秘密情報なので`.gitignore`済み(Git管理外)。

**How to apply:** 「コイキーズの記事をリライトして」「リライトの続き」などの発言、またはセッション開始時の監視レポート報告をトリガーとして、このスキルのフローに従う。
