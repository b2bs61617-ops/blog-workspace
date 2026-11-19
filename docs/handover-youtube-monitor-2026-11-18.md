# 引き継ぎ: アイドルYouTube監視（2026-11-18）→ 完了

**2026-11-18に「ネタ見張り」`tools/neta_watch/` として完成・稼働中。** 使い方は [tools/neta_watch/README.md](../tools/neta_watch/README.md)。

## 決まったこと（トモキ）
- 公式YouTubeが更新されたら内容を解析（話した内容のまとめ・行った場所・服・小物）。分からないものは人が見るので、**場面の画像を必ず残す**。
- SNS（公式・メンバー）も常に集めて、ネタになりそうなものを知らせる。
- 知らせは「AIまつ」LINEで1日2回（8時・20時）まとめて。マツ（Claude）のトークンは使わない（AIはGemini無料）。
- GEEKOMのタスク `NetaWatch` が1時間おきに動く。記録とログは `%LOCALAPPDATA%\neta_watch\`、画像とメモは `AI作業場\ネタ見張り\日付\`。

## 残っていること
- SNSの名簿 `tools/data/sources.json` に、SixTONES・トラジャ・キテレツのメンバー個人Instagram、KO1KEYZ公式Instagramが入っていない（Snow Manは公式＋9人登録済み）。足すときは `checked` を null で書き、`python tools/hasshin/hasshin.py --check` で本物か確かめてから日付を入れる。
- TikTok・Threads・ストーリー・返信は見ていない。
- 旧 `tools/youtube-talent-monitor/` は使わない。
