# 引き継ぎ: アイドルYouTube監視（2026-11-18）

GEEKOM機で調べた結果。スマホ（クラウド版）で続きをやるためのメモ。

## わかったこと
- 道具は `tools/youtube-talent-monitor/video_monitor.py`（公式YouTubeのRSSで新着を見る→文字起こし→Gemini画像解析→LINE通知）。
- **GEEKOMではタスク登録されておらず、一度も自動で動いていない**（monitor_state.json も reports/ も無い）。前のPCで登録したまま、移行時に抜けたと思われる。
- `--dry-run --no-transcript --no-visuals` で試したら新着はちゃんと取れた（道具は壊れていない）。
- 名簿 `tools/youtube-talent-monitor/channels.json` は2026-07時点の「旧ジャニーズ全般（chomoand-0向け）」のまま。今のサイト構成と合っていない。
  - 今の担当: chomoand-2=Snow Man / chomoand-0=SixTONES / chomoand-4=Travis Japan / chomoand-5=KEY TO LIT / KO1KEYZ
- `tools/koikeyz-youtube-monitor/` は2026-07-30から使っていない（KO1KEYZはX監視にする方針だった）。
- 似た道具の「発信あつめ」`tools/hasshin/hasshin.py` も公式YouTube（RSS）を見ている。名簿は `tools/data/sources.json`。11/14に手で3回動かしただけで、自動にはなっていない。
- LINE通知がまだ届くかは未確認（LINE Notifyは終了済みの可能性があるので要確認）。

## トモキに聞いている選択肢（返事待ち）
1. 名簿を今の5グループ＋メンバー個人に入れ替えて、毎日自動で動くように登録する（マツのおすすめ）
2. 「発信あつめ」のほうを毎日自動にして、YouTube監視はそっちにまとめる
3. 今はこのままにしておく

## クラウド版でできること / できないこと
- できる: channels.json や sources.json の名簿の更新（チャンネルIDはRSSで確認できる）、コードの手直し、GitHubへのpush。
- できない: GEEKOMのタスクスケジューラへの登録。これはPCに戻ってから `git pull` → `schtasks` で登録する（毎日23:00、python は絶対パスで呼ぶ）。
