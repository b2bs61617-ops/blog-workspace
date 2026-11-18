# ネタ見張り(2026-11-18〜)

マツ(Claude)を使わずに、PCだけで24時間ネタを見張る道具。AIは無料のGeminiを使う。

## やること
| いつ | なにを |
|---|---|
| 1時間おき | 5グループの公式YouTube(`tools/data/sources.json`)に新しい動画が出たら、Geminiに動画を見せて「話した内容・場所・服・小物・食べ物」を拾い、その場面の画像を保存 |
| 7時・13時・19時 | 公式とメンバーのX/Instagram(発信あつめと同じ名簿・同じブラウザ)の新しい投稿と写真を集めて、ネタになるか判定 |
| 0〜6時台(毎時) | **速報の自動記事**(`sokuho_auto.py`、2026-11-19〜)。Xの「速報」ラベルのニュース → 大手ニュース(NHK・スポーツ紙・ナタリーなど)で裏取り → chomoand.comに記事を書いて公開 → Indexing → @chomotirend(X/Threads)。**重い話(訃報・逮捕・事件事故・災害・不倫など)・事実チェックNG・報道/公式のXの写真が無い・2,000字未満は下書きで止める**。1回2本・1晩4本まで |
| 7時・13時・19時 | 速報の一覧だけ集める(記事は作らない) |
| 8時・20時 | たまったネタを「AIまつ」のLINEにまとめて1通で送る(ネタが無ければ送らない) |

画像とメモは `AI作業場\ネタ見張り\日付\` に残る(OneDriveで同期されるのでスマホのOneDriveアプリでも見られる)。
- YouTube: 動画ごとのフォルダに `内容.txt`・`00_サムネ.jpg`・`003m12s_小物_黒いキャップ.jpg`(ネタの場面)・`…_全体.jpg`(全体から均等に8枚)
- SNS: `SNS_1900\一覧.txt` と `img\`

## 使い方
- 自動にする(このPCで1回だけ): `powershell -ExecutionPolicy Bypass -File tools\neta_watch\register_task.ps1`
- 今すぐ動かす: `python tools/neta_watch/neta_watch.py --youtube`(`--sns` / `--digest` / `--sokuho` / `--dry-run`)
- 速報をためす(WordPressに出さない): `python tools/neta_watch/sokuho_auto.py --test`
- 1本だけ試す: `python tools/neta_watch/neta_watch.py --video 動画ID`
- 動いた記録: `tools/neta_watch/log.txt`

## 注意
- LINEは無料で月200通。友だち3人なので1回送ると3通。1日2回で月180通くらい。ほかの通知と合わせて超えそうなら送る回数を減らす。
- 場所・ブランドの当てはAIの見立て。記事にする前に画像で確かめる(`sure`が「確実」でも)。
- SNSはブラウザ(Xiyのログイン済みプロファイル)が開く。PCがスリープしている間は動かない(起きたら追いかけて動く)。
- 見張る先を増やすときは `tools/data/sources.json` に足す(X/Instagramは `checked` の日付が入っているものだけ見る)。
- 速報の自動記事はGemini(無料)が書く。無料枠はモデルごとなので、昼の動画解析で1つ目を使い切っても`GEMINI_MODELS`の次のモデルで書く。
- 速報のアイキャッチはCanvaが使えない(夜中は人がいない)ので予備の`eyecatch_chomoand.py --fallback-ok`。気になれば朝にCanvaで差し替える。
- 決まりごと(トモキ 2026-11-19): 自動公開は0〜7時だけ/重い話は下書き止め/速報ラベル+大手ニュースで確認できたものだけ/知らせは8時のLINEのまとめに入れる。
