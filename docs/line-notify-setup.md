# LINE通知のセットアップ手順

記事更新時にLINEへプッシュ通知する仕組み(`tools/line_notify.py`)の初回セットアップ手順。LINE Notifyは2025年3月にサービス終了済みのため、LINE公式アカウント(Messaging API)経由で通知する。

## 1. LINE公式アカウント作成

1. LINE Official Account Manager(https://manager.line.biz/)で公式アカウントを作成(すでにLINEアカウントがあればそれでログイン)
2. 右上の歯車アイコン →「Messaging API」→「Messaging APIを利用する」で有効化(プロバイダー名は任意)
3. 有効化後の画面(またはLINE Developersコンソール `https://developers.line.biz/console/` の対象チャネル →「Messaging API設定」タブ)で**チャネルアクセストークン(長期)**を発行し、`.env`の`LINE_CHANNEL_ACCESS_TOKEN`に設定する
4. 同じ画面のQRコードを、通知を受け取りたい本人のLINEアプリで友だち追加する

## 2. 通知先のuserIdを取得する

**`tools/line_notify.py --get-user-id`(フォロワーID一覧API `/v2/bot/followers/ids`)は無料の「コミュニケーション」プランだと`403 Access to this API is not available for your account`で使えない**(2026-07-05確認)。代わりにWebhookで直接受け取る方式を使う。

1. `cloudflared`(Cloudflare Quick Tunnel、アカウント登録不要)をダウンロードする
   ```
   curl -sL -o cloudflared.exe "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
   ```
2. ローカルでWebhook受信用の簡易HTTPサーバーを起動する(POST bodyの`events[].source.userId`を拾って表示・保存するだけの`http.server`ベースの小さなスクリプトでよい)
3. `./cloudflared.exe tunnel --url http://127.0.0.1:{ポート}` を起動し、発行された`https://xxxx.trycloudflare.com`のURLを控える
4. LINE Developersコンソールの対象チャネル →「Messaging API設定」タブで、そのURLを「Webhook URL」に設定して保存 →「検証」ボタンで疎通確認 →「Webhookの利用」をオンにする(この「検証」ボタンや「Webhookの利用」トグルはOfficial Account Manager側の簡易画面には無く、LINE Developersコンソール側にしかないので注意)
5. 友だち追加した公式アカウントに、LINEアプリから何か一言メッセージを送る
6. ローカルサーバーがWebhookを受信し、`source.userId`(`U`で始まる33文字の文字列)をキャッチできる。それを`.env`の`LINE_USER_ID`に設定する
7. セットアップ完了後は、ローカルサーバー・トンネルのプロセスを停止し、一時ファイルは削除してよい(Webhookの利用をオフに戻しても、オンのままにしても以降のpush通知には影響しない。オンのままだとトンネルが無いため単に疎通エラーが記録されるだけ)

## 3. 動作確認

```
python tools/line_notify.py "テスト通知"
```

LINEに届けば設定完了。届かない場合は`.env`の`LINE_CHANNEL_ACCESS_TOKEN`/`LINE_USER_ID`の値・友だち追加状況を確認する。

## 使われている場所

- [koikeyz-rewriteスキル](../.claude/skills/koikeyz-rewrite/SKILL.md): リライト提案時・記事更新完了時にLINE通知
- `tools/koikeyz-monitor/x_monitor.py`: 毎朝7時の監視でGeminiが「記事化に値する新情報あり」と判定した場合にLINE通知(2026-07-05追加)
