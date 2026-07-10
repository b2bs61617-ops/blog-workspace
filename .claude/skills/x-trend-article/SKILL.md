---
name: x-trend-article
description: Xトレンド監視ツール(tools/x-trend-monitor/)が検知した新トレンドを、リサーチ→執筆→chomoand.comへ下書き投稿まで全自動で処理するときに使う。ヘッドレスClaude(claude -p)から起動される想定。
---

# Xトレンド自動記事化スキル

`tools/x-trend-monitor/trend_monitor.py`(30分おきのタスクスケジューラ実行)が新トレンドを検知すると、
`claude -p` 経由でこのスキルが呼ばれる。**フェーズ1運用: 下書きまで全自動、公開はユーザー承認制**(2026-07-10開始)。

## 絶対ルール(フェーズ1)

- **公開しない。** 投稿は必ず`status: draft`。publishへの変更はユーザーが「公開して」と言ったときだけ([publish](../publish/SKILL.md)スキル)。
- **削除しない。** WordPress記事・ファイルの削除は一切行わない([docs/wordpress.md](../../../docs/wordpress.md))。
- **裏取りできない情報は書かない。** 全自動運用なので、誤情報・名誉毀損リスクは通常より厳しく見る。

## 実行フロー

1. **レポートを読む**: 引数で渡された `tools/x-trend-monitor/reports/trends_*.json` を読む(最大3トレンド)。

2. **記事化の判断**(トレンドごと):
   - **採用**: 人物・グループ・作品・出来事で「なぜ？」「誰？」「何があった？」と検索されそうなもの。[trend-title](../trend-title/SKILL.md)の「ずらし記事」で戦えるもの。
   - **見送り**: 以下は記事化しない。
     - 災害・事故・事件(被害者や逮捕者が絡むもの)。名誉毀損・不謹慎リスクが高いため
     - 政治・選挙・宗教などの敏感なテーマ
     - テレビ番組の実況タグ・大喜利タグなど、検索需要が続かない定型ハッシュタグ
     - 企業キャンペーン・プロモーション由来のトレンド
     - リサーチしても「なぜトレンド入りしたか」が特定できなかったもの
   - 判断に迷ったら見送り(見送り理由は最後のLINE通知に含める)。

3. **リサーチ**: WebSearchで「なぜ今トレンド入りしたか」を特定し、事実関係を複数ソースで裏取りする。
   Yahoo!リアルタイム検索(`https://search.yahoo.co.jp/realtime/search?p={トレンド語}`)のWebFetchも有効。

4. **重複チェック**: `GET https://chomoand.com/wp-json/wp/v2/posts?search={キーワード}`で既存記事を検索。
   同一テーマの記事が既にあれば新規作成せずスキップ(LINE通知にその旨を含める)。

5. **執筆**: [trend-title](../trend-title/SKILL.md)でタイトル決定(疑問形)、[docs/rules.md](../../../docs/rules.md)準拠で執筆。
   - 結論ファースト、最低2,500字、句点で文が終わったら`<br>`改行
   - 場所が特定できていればGoogleマップ埋め込み
   - 人物ネタは[wiki-article](../wiki-article/SKILL.md)/[gakureki-kazoku-kanojo](../gakureki-kazoku-kanojo/SKILL.md)のテンプレを流用してよい
   - 既存の関連記事があれば内部リンクを張る
   - 推測は「〜の可能性があります」と明示し、断定しない

6. **下書き投稿**: [blog-upload](../blog-upload/SKILL.md)の手順で**chomoand.com**(`WP_TREND_*`)に`status: draft`で投稿し、アイキャッチも生成・設定する([docs/eyecatch-style.md](../../../docs/eyecatch-style.md))。
   下書き更新時は`status: draft`を必ずペイロードに含める([docs/wordpress.md](../../../docs/wordpress.md)の2026-07-10の注意点)。

7. **LINE通知**: 処理結果をまとめて1通送る。
   - 下書きあり: `python tools/line_notify.py "トレンド「{語}」の記事下書きができたワン。中身を確認して「公開して」と言ってほしいワン。タイトル: {タイトル} 編集: https://chomoand.com/wp-admin/post.php?post={ID}&action=edit"`
   - 全件見送り: `python tools/line_notify.py "Xトレンド{N}件を検知したけど、記事化は見送ったワン。理由: {簡潔に}"`

8. **後片付け**: 処理済みレポート(`.json`と`.claude.log`)を `tools/x-trend-monitor/reports/processed/` に移動する。

## 運用メモ

- フェーズ2(確認なし全自動公開)への切り替えはユーザーが判断する。指示があるまで下書き止め。
- 監視ツール側の仕様(30分間隔・同一トレンド24時間クールダウン・1回最大3件)は[tools/x-trend-monitor/trend_monitor.py](../../../tools/x-trend-monitor/trend_monitor.py)参照。
