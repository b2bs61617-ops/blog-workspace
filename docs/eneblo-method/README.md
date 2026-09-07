# エネブロ式 ブログ立ち上げメソッド（hide000.net）

トモキの友人 **Hideki** が運営する教材サイト **「省エネブログマスターパック（エネブロ）」** = `https://hide000.net/` の、ブログ立ち上げ手順をまとめたもの。
新規サイト（chomoand-2〜5 など）を立ち上げる／点検するときの**基準**にする。

## このフォルダの中身

| ファイル | 内容 |
|---|---|
| [setup-checklist.md](setup-checklist.md) | **統合チェックリスト**。エネブロの全手順を1枚に集約した実務用リスト。まずこれを見る |
| [conformance-2026-09-07.md](conformance-2026-09-07.md) | chomoand-2〜5 の適合状況スナップショット（2026-09-07 時点） |
| [reference/](reference/) | 出典ページを1枚ずつ抽出・整形したもの（原文に近い形での保存） |

## 出典（hide000.net）

ロードマップ本体: `https://hide000.net/cooa_blogroadmap/`（パスワード: `cooablog-2025`）

パスワード保護ページと解錠キー（トモキから共有、2026-09-07）:

| ページ | URL | パスワード | reference |
|---|---|---|---|
| テーマ選定とプラグインの初期設定 | `/cooa_wardpress_settings/` | `eneblo1_2025` | reference/wpset.md |
| キーワード選定とタイトル作成の秘訣 | `/kw_taittle/` | `eneblo2_2025` | reference/kw.md |
| トレンドブログを極めるスキル実践編 | `/trend_kiwami/` | `eneblo3_2025` | reference/kiwami.md |
| PV爆発リアルネタ集 | `/pv_access/` | `eneblo4_2025` | reference/pv.md |
| ネタ選定コンサル動画 | `/netasentei/` | `eneblo5_2025` | reference/neta.md |
| Google Adsenseで広告運用を開始しよう！ | `/google_adsense_koukoku/` | `eneblo6_2025` | reference/adsense.md |

> 動画（Vimeo）と配布PDF/zip 本体は取り込んでいない。テキストで読める部分のみ抽出済み。
> トモキが別途くれた PDF「サイトの立上げ」「プラグイン一覧」は、上記 `cooa_wardpress_settings` と同じ内容の配布資料。

## 使い方（松向けメモ）

- 新サイトを立ち上げる／既存サイトを点検するときは [setup-checklist.md](setup-checklist.md) の Phase 順に確認する。
- WordPress の設定変更・プラグイン操作は CLAUDE.md のルールどおり**トモキに確認してから**実行する。
- REST API（アプリパスワード）でできること・できないことは conformance ドキュメントの「実施メモ」を参照。
