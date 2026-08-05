# SNS自動投稿セットアップ(X/Instagram)

記事を**公開(publish)したタイミング**で、X(旧Twitter)・Instagramへ自動投稿するための設定手順。2026-07-30にトモキから依頼があり、既存調査([docs/wordpress.mdのSNS自動連携](wordpress.md)、2026-07-05実施)をベースに本格導入した。

対象は3ブログ全て(chomoand.com・chomoand-0.com・chomoand-1.com)。投稿文は**タイトル+URLのシンプル型**。

## 方式のまとめ

| SNS | 方式 | 理由 |
|---|---|---|
| Instagram | Jetpack Social(WordPress公式プラグイン) | 公開時に自動シェアする公式機能があり、外部サービス契約不要 |
| X(旧Twitter) | Zapier/Make/IFTTT等の外部連携 | Jetpack Socialは2023年にX対応を廃止済み。「WordPress New Post」→「X Create Tweet」で構築する |

どちらもOAuth接続やアカウント作成はブラウザ操作が必要なため、**トモキ本人が手動で行う**(マツはAPI経由のプラグインインストールまでは実行済み・以降の接続作業はできない)。

## 前提: プラグイン導入状況(2026-07-30時点)

- **chomoand.com**: `jetpack-social`プラグイン導入・有効化済み(既にJetpack接続もisActive:true)。Instagram連携が済んでいるかは要確認。
- **chomoand-1.com**: 2026-07-30にマツがREST API経由で`jetpack-social`をインストール・有効化済み。Instagram連携は未実施。
- **chomoand-0.com**: **DNS障害で外部から一時接続不可**(2026-07-30発見、原因と復旧手順は[docs/wordpress.md](wordpress.md)参照)。復旧後にプラグイン導入状況を確認すること。

## STEP A: Jetpack Social(Instagram)の接続 — サイトごとに実施

1. 対象サイトの`wp-admin`にログイン(ユーザー: `b2bs61617@gmail.com`)
2. 左メニュー「Jetpack」→「Social」(または「設定」→「共有」)を開く
3. まだの場合、WordPress.comアカウントへの接続を求められるので接続する(Jetpackプラグイン自体の登録はAPI経由で完了済みだが、ソーシャル共有機能はWordPress.comアカウントとの紐付けが別途必要)
4. 「Instagram Businessアカウントを接続」を選択し、Facebook経由でログイン
   - **前提条件**: Instagramアカウントが「ビジネスアカウント」または「クリエイターアカウント」になっていて、Facebookページと連携済みであること。個人アカウントのままだと接続できない。未対応の場合はInstagramアプリの「設定」→「アカウントの種類とツール」からプロアカウントに切り替え、Facebookページと連携する
5. 接続後、「新規投稿時に自動共有」を有効にする
6. 各サイトで下書き記事を1本publishし、実際にInstagramへ投稿されるか動作確認する

## STEP B: X(旧Twitter)の自動投稿 — Zapier等の外部連携

Zapierを例に記載(Make.com・IFTTTでも同様の構成)。

1. https://zapier.com でアカウント作成(無料プランでも可。ただし後述の制限に注意)
2. 「Create Zap」→ トリガーアプリで「WordPress」を選択
3. トリガーイベント: 「New Post」を選択
4. WordPress接続設定でサイトURL・ユーザー名(`b2bs61617@gmail.com`)・アプリパスワードを入力(`.env`の`WP_TREND_APP_PASSWORD`等と同じ値。サイトごとに別のZap/別の接続が必要)
5. **重要な確認ポイント**: このリポジトリの運用では記事はまず`status: draft`で下書き投稿し、後から[publishスキル](../.claude/skills/publish/SKILL.md)で`status: publish`に変更する2段階フロー。Zapierの「New Post」トリガーが**下書き作成時点で発火してしまわないか**を必ず確認すること。
   - トリガー設定に「Post Status」で絞り込む項目があれば`Published`のみに設定する
   - 絞り込み項目が無い場合は、Zapierの「Filter」ステップを挟み、投稿データの`status`フィールドが`publish`であることを条件に追加する(これがないと下書き段階で誤ってXに投稿されてしまう)
6. アクションアプリで「X (Twitter)」を選択し、アカウント連携(Xアカウントへのログイン、開発者アカウント契約は不要)
7. アクションイベント: 「Create Tweet」を選択
8. 投稿本文のテンプレートを設定: `{{post_title}}\n{{post_link}}` (タイトル+URL)
9. Zapをテストしてオンにする(サイトごとに1つ、計3つのZapを作成)

### 無料プランの制限に関する注意

Zapierの無料プランはアカウント全体で月100タスクまで、かつトリガーのポーリング間隔が最短15分(即時実行不可)という制限がある。3サイト分を1アカウントで運用する場合、更新頻度によっては無料枠を超える可能性がある。超えそうな場合は有料プラン(Starterプラン等)への切り替えを検討する。契約判断はトモキが行うこと。

## KO1KEYZ(chomoand-1.com)のアイキャッチ復活について

2026-07-24〜「アイキャッチ画像は作らない」方針だったが、Instagram自動投稿にはアイキャッチ画像(featured_media)が実質必須なため、2026-07-30に**方針を終了し、SNS投稿を兼ねてアイキャッチを復活**させた。[blog-uploadスキルSTEP4](../.claude/skills/blog-upload/SKILL.md)で`tools/eyecatch_koikeyz.py`を使い生成し、featured_mediaとして設定する(記事ページ上にも表示されることを許容する判断)。

## 完了確認チェックリスト

- [ ] chomoand.com: Instagram Business接続・自動共有ON・X用Zap作成
- [ ] chomoand-0.com: DNS復旧後、Jetpack Socialプラグイン導入・Instagram Business接続・自動共有ON・X用Zap作成
- [x] chomoand-1.com: Facebookページ「ちょものKo1keys情報局」新規作成・Instagram(@chomoand)連携・Threads(chomoand)連携・Jetpack Social接続完了(2026-08-02)
- [ ] chomoand-1.com: X用Zap作成
- [ ] chomoand-1.com: blog-uploadスキルでのアイキャッチ生成動作確認

### chomoand-1.com セットアップでのつまずきポイント(2026-08-02)

- `jetpack-social`プラグインは7/30に有効化した記録があったが、確認時には無効化(inactive)状態に戻っていた。原因不明だが、REST API経由で再度有効化して対応した。今後同様の相談が来たら、まずプラグイン一覧(`GET /wp-json/wp/v2/plugins`)で`status`を確認すること。
- Jetpack Socialの「アカウントに接続」を最初に試した際「No accounts/pages found」エラーになった。原因はKO1KEYZ用のFacebookページが存在しなかったこと(個人のFacebookプロフィールだけでは接続先として認識されない)。Facebookページを新規作成し、Instagramをそのページにリンク(プロアカウント化)してから再接続したら解消した。
- `.env`の`WP_KOIKEYS_APP_PASSWORD`に、WordPressの**通常ログインパスワード**を入れてしまい401エラーになったことがあった。REST API認証には`wp-admin`のプロフィール画面で発行する**アプリケーションパスワード**(`xxxx xxxx xxxx xxxx xxxx xxxx`形式)が必要で、別物。
