# LINE通知のセットアップ手順

記事更新時にLINEへ通知する仕組み(`tools/line_notify.py`)の初回セットアップ手順。LINE Notifyは2025年3月にサービス終了済みのため、LINE公式アカウント(Messaging API)経由で通知する。

**方式はブロードキャスト**(公式アカウントを友だち追加している全員に一斉送信)。2026-07-06に、複数人への通知(同僚に届かない問題)をきっかけに、特定userIdへのpush方式から切り替えた。userIdを個別に取得・登録する必要はない。

## 1. LINE公式アカウント作成

1. LINE Official Account Manager(https://manager.line.biz/)で公式アカウントを作成(すでにLINEアカウントがあればそれでログイン)
2. 右上の歯車アイコン →「Messaging API」→「Messaging APIを利用する」で有効化(プロバイダー名は任意)
3. 有効化後の画面(またはLINE Developersコンソール `https://developers.line.biz/console/` の対象チャネル →「Messaging API設定」タブ)で**チャネルアクセストークン(長期)**を発行し、`.env`の`LINE_CHANNEL_ACCESS_TOKEN`に設定する
4. 同じ画面のQRコードを、通知を受け取りたい人全員(本人・同僚など)のLINEアプリで友だち追加してもらう。以降、友だち追加した人全員に自動で通知が届く

## 2. 動作確認

```
python tools/line_notify.py "テスト通知"
```

友だち追加している全員にLINEが届けば設定完了。届かない場合は`.env`の`LINE_CHANNEL_ACCESS_TOKEN`の値・友だち追加状況を確認する。

## 注意点

- ブロードキャストは無料プランの月間メッセージ配信数(無料枠)を、送信1回につき「友だち人数分」消費する。人数が増えると枠の消費が早くなる点に注意。
- 特定の人だけに送り分けたい場合はこの方式では不可(その場合はWebhookでuserIdを個別取得し、multicast/push方式に戻す必要がある)。

## 使われている場所

- [koikeyz-rewriteスキル](../.claude/skills/koikeyz-rewrite/SKILL.md): リライト提案時・記事更新完了時にLINE通知
- `tools/koikeyz-monitor/x_monitor.py`: 毎朝7時の監視結果を**結果に関わらず毎日必ず**LINE通知する(新着なし/新着ありだが記事化価値なし/記事化価値あり(要約付き)/AI要約失敗、の4パターン。2026-07-05に「あり判定のときだけ通知」から「毎日必ず通知」に変更)
- Gemini要約が失敗した日は、次にセッションを開いたときにマツが生データを目視要約して追加でLINE送信する([koikeyz-rewriteスキル](../.claude/skills/koikeyz-rewrite/SKILL.md)参照)

## 検討したが見送った案: LINE返信トリガーによる記事自動執筆パイプライン(2026-07-05)

「LINE通知に『リライト』『新規作成』と返信するだけで、マツが調査・執筆・WordPress投稿まで自動実行する」仕組みを設計・計画したが、実装前にユーザー判断で見送りになった。

- 技術的にはLINEの返信はWebhookでしかリアルタイム受信できず(ポーリング不可)、安定した固定URLを得るには**chomoand.comをCloudflareに登録してネームサーバーを切り替える**必要があった(本番ドメインのメール(MX/SPF/DKIM)・サイトのDNSに影響するリスクがある変更)。
- ユーザーが「現時点ではこれは怖い」と判断し中止。DNS移行を伴わない、より安全なシンプルな日次通知(上記)に落ち着いた。
- 設計の全体像(アーキテクチャ図・ファイル構成案・実行順序)は`C:\Users\ti071\.claude\plans\optimized-greeting-sunset.md`(このPCのローカルファイル、Git管理外)に残っている。再検討する場合はそちらを参照。
- 再検討する際は、chomoand.com本番DNSに触らない代替案(例: webhook専用の別ドメインを新規取得してCloudflareに登録する)も選択肢に入れるとよい。
