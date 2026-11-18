# ネタ見張り(2026-11-18〜)

マツ(Claude)を使わずに、PCだけで24時間ネタを見張る道具。AIは無料のGeminiを使う。

## やること
| いつ | なにを |
|---|---|
| 1時間おき | 5グループの公式YouTube(`tools/data/sources.json`)に新しい動画が出たら、Geminiに動画を見せて「話した内容・場所・服・小物・食べ物」を拾い、その場面の画像を保存 |
| 7時・13時・19時 | 公式とメンバーのX/Instagram(発信あつめと同じ名簿・同じブラウザ)の新しい投稿と写真を集めて、ネタになるか判定 |
| 8時・20時 | たまったネタを「AIまつ」のLINEにまとめて1通で送る(ネタが無ければ送らない) |

画像とメモは `AI作業場\ネタ見張り\日付\` に残る(OneDriveで同期されるのでスマホのOneDriveアプリでも見られる)。
- YouTube: 動画ごとのフォルダに `内容.txt`・`00_サムネ.jpg`・`003m12s_小物_黒いキャップ.jpg`(ネタの場面)・`…_全体.jpg`(全体から均等に8枚)
- SNS: `SNS_1900\一覧.txt` と `img\`

## 使い方
- 自動にする(このPCで1回だけ): `powershell -ExecutionPolicy Bypass -File tools\neta_watch\register_task.ps1`
- 今すぐ動かす: `python tools/neta_watch/neta_watch.py --youtube`(`--sns` / `--digest` / `--dry-run`)
- 1本だけ試す: `python tools/neta_watch/neta_watch.py --video 動画ID`
- 動いた記録: `tools/neta_watch/log.txt`

## 注意
- LINEは無料で月200通。友だち3人なので1回送ると3通。1日2回で月180通くらい。ほかの通知と合わせて超えそうなら送る回数を減らす。
- 場所・ブランドの当てはAIの見立て。記事にする前に画像で確かめる(`sure`が「確実」でも)。
- SNSはブラウザ(Xiyのログイン済みプロファイル)が開く。PCがスリープしている間は動かない(起きたら追いかけて動く)。
- 見張る先を増やすときは `tools/data/sources.json` に足す(X/Instagramは `checked` の日付が入っているものだけ見る)。
