# SNS自動投稿セットアップ(Facebook/Instagram/Threads/X)

**2026-08-09追記: X(旧Twitter)部分は廃止・置き換え済み。** ZapierのCreate Tweetアクションは本文にURLを含めると読まれてしまいXのアルゴリズム上リーチが落ちる上、リプライスレッド(URLを2件目のリプライに逃がす形)も組めないという制約があったため、自前のPythonスクリプトに置き換えた。**X関連のセットアップは[docs/x-auto-post-setup.md](x-auto-post-setup.md)を参照**(このページのSTEP B以下は廃止済みの記録として残すのみ)。Facebook/Instagram/Threads部分(下記STEP A)は引き続き有効で、**2026-08-10〜chomoand.com・chomoand-0.comへの展開作業中**。

記事を**公開(publish)したタイミング**で、Facebook・Instagram・Threads・X(旧Twitter)へ自動投稿するための設定手順。2026-07-30にトモキから依頼があり、既存調査([docs/wordpress.mdのSNS自動連携](wordpress.md)、2026-07-05実施)をベースに本格導入した。

対象は3ブログ全て(chomoand.com・chomoand-0.com・chomoand-1.com)。投稿文は**タイトル+URLのシンプル型**。

## 方式のまとめ

| SNS | 方式 | 理由 |
|---|---|---|
| Facebook / Instagram / Threads | Jetpack Social(WordPress公式プラグイン) | 1つのプラグイン接続で3ネットワークとも公開時に自動シェアできる公式機能があり、外部サービス契約不要 |
| X(旧Twitter) | ~~Zapier/Make/IFTTT等の外部連携~~ **→廃止、[docs/x-auto-post-setup.md](x-auto-post-setup.md)の自作スクリプトに置き換え(2026-08-09)、さらにAPI課金化により2026-08-10〜手動投稿運用に変更** | Jetpack Socialは2023年にX対応を廃止済み |

Facebook・Instagram・Threadsいずれも、アカウント連携・OAuth接続はブラウザ操作が必要なため**トモキ本人が手動で行う**(マツはAPI経由のプラグインインストール/有効化までは実行できるが、以降のOAuth接続作業はできない)。

## サイトごとの現状(2026-08-10時点)

| サイト | プラグイン導入 | Facebook Page | Instagram | Threads | 自動共有ON |
|---|---|---|---|---|---|
| chomoand-1.com(コイキーズ) | ✅ | ✅ 「ちょものKo1keys情報局」 | ✅ @chomoand | ✅ chomoand | ✅(2026-08-02完了、稼働中) |
| chomoand.com(トレンド) | ✅ 導入済み | 未着手 | 未接続 | 未接続 | ー |
| chomoand-0.com(ジャニオタ) | 要確認(DNS障害で長期間確認不可だったが解消済み) | 未着手 | 未接続 | 未接続 | ー |

chomoand-0.comのDNS障害(2026-07-30発見)は、実際にはXserver側ではなくトモキ自宅Wi-Fi回線(ZAQ/J:COM)のISP側DNS横取りが原因と判明し解消済み([docs/history.md](history.md)参照)。2026-08-10時点で`https://chomoand-0.com/wp-json/`への外部接続は正常(HTTP 200)なので、プラグイン導入から着手できる。

## STEP A: Jetpack Social(Facebook/Instagram/Threads)の接続 — サイトごとに実施

chomoand-1.comで実際にこの手順で接続できている(2026-08-02完了)。chomoand.com・chomoand-0.comも同じ手順で進める。

1. 対象サイトの`wp-admin`にログイン(ユーザー: `b2bs61617@gmail.com`)
2. `jetpack-social`プラグインが未導入/無効化の場合はマツがREST API経由でインストール・有効化する(`.env`に該当サイトの`WP_*_USERNAME`/`WP_*_APP_PASSWORD`が必要。このPCの`.env`は現状`WP_TREND_*`・`WP_AUDITION_*`のUSERNAME/APP_PASSWORDが未設定なので、先にトモキが埋める必要あり)
   - 過去にchomoand-1.comで「有効化したはずが確認時に無効化(inactive)状態に戻っていた」ことがあったので、疑わしい場合は`GET /wp-json/wp/v2/plugins`で`status`を確認すること
3. 左メニュー「Jetpack」→「Social」(または「設定」→「共有」)を開く
4. まだの場合、WordPress.comアカウントへの接続を求められるので接続する(Jetpackプラグイン自体の登録はAPI経由で完了済みでも、ソーシャル共有機能はWordPress.comアカウントとの紐付けが別途必要)
5. **Facebookページを接続**
   - 対象サイト用のFacebookページが無ければ先に新規作成する(個人のFacebookプロフィールだけでは接続先として認識されない。chomoand-1.comでは「No accounts/pages found」エラーになり、ページ作成後に解消した実績あり)
6. **Instagram Businessアカウントを接続**
   - **前提条件**: Instagramアカウントが「ビジネスアカウント」または「クリエイターアカウント」になっていて、上記5で作ったFacebookページと連携済みであること。個人アカウントのままだと接続できない。未対応の場合はInstagramアプリの「設定」→「アカウントの種類とツール」からプロアカウントに切り替え、Facebookページと連携する
7. **Threadsアカウントを接続**(Instagramアカウントに紐づくThreadsアカウントとして接続される)
8. 接続後、Facebook/Instagram/Threadsそれぞれについて「新規投稿時に自動共有」を有効にする(ネットワークごとに個別トグルなので、3つとも入れ忘れがないか確認する)
9. 各サイトで下書き記事を1本publishし、実際にFacebook・Instagram・Threadsへ投稿されるか動作確認する

## STEP B: X(旧Twitter)の自動投稿 — Zapier等の外部連携【廃止済み・2026-08-09】

**このSTEP Bは実施不要。** [docs/x-auto-post-setup.md](x-auto-post-setup.md)の自作スクリプトに置き換えたため、Zapierのセットアップ自体を行う必要はなくなった。既にZapを作成済みの場合は重複投稿を避けるためオフにすること。以下は廃止前の記録として残す。

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

- [ ] chomoand.com: `.env`の`WP_TREND_USERNAME`/`WP_TREND_APP_PASSWORD`をトモキが設定(2026-08-10時点でこのPCの`.env`は未設定、マツがプラグイン状態を確認・操作するために必要)
- [ ] chomoand.com: Facebookページ新規作成・Instagram Business接続・Threads接続・自動共有ON(3ネットワークとも)
- [ ] chomoand-0.com: `.env`の`WP_AUDITION_USERNAME`/`WP_AUDITION_APP_PASSWORD`をトモキが設定
- [ ] chomoand-0.com: Jetpack Socialプラグイン導入状況の確認(DNS障害は解消済み、2026-08-10時点で`https://chomoand-0.com/wp-json/`は正常応答)
- [ ] chomoand-0.com: Facebookページ新規作成・Instagram Business接続・Threads接続・自動共有ON(3ネットワークとも)
- [x] chomoand-1.com: Facebookページ「ちょものKo1keys情報局」新規作成・Instagram(@chomoand)連携・Threads(chomoand)連携・Jetpack Social接続完了(2026-08-02)
- [ ] chomoand-1.com: 直近の下書きpublishでFacebook/Instagram/Threadsに実際に投稿されるか再確認(過去にプラグインが無効化状態に戻っていたことがあるため)
- [ ] chomoand-1.com: blog-uploadスキルでのアイキャッチ生成動作確認

X用Zap作成は2026-08-10時点で対象外(X自動投稿はAPI課金化のため手動運用に変更済み、[docs/x-auto-post-setup.md](x-auto-post-setup.md)参照)。

### chomoand-1.com セットアップでのつまずきポイント(2026-08-02)

- `jetpack-social`プラグインは7/30に有効化した記録があったが、確認時には無効化(inactive)状態に戻っていた。原因不明だが、REST API経由で再度有効化して対応した。今後同様の相談が来たら、まずプラグイン一覧(`GET /wp-json/wp/v2/plugins`)で`status`を確認すること。
- Jetpack Socialの「アカウントに接続」を最初に試した際「No accounts/pages found」エラーになった。原因はKO1KEYZ用のFacebookページが存在しなかったこと(個人のFacebookプロフィールだけでは接続先として認識されない)。Facebookページを新規作成し、Instagramをそのページにリンク(プロアカウント化)してから再接続したら解消した。
- `.env`の`WP_KOIKEYS_APP_PASSWORD`に、WordPressの**通常ログインパスワード**を入れてしまい401エラーになったことがあった。REST API認証には`wp-admin`のプロフィール画面で発行する**アプリケーションパスワード**(`xxxx xxxx xxxx xxxx xxxx xxxx`形式)が必要で、別物。

### X用Zap作成が「403 Forbidden」で詰まっている件(2026-08-06、未解決・作業中)

ZapierでWordPressアカウントを接続しようとすると、毎回同じ`認証に失敗しました: 403 Forbidden: アクセスが拒否されました`で失敗する。以下は全て確認済みで、原因ではないと判明したもの:

- WordPress REST API自体の認証は正常(`WP_KOIKEYS_*`の資格情報で直接APIを叩くと`AUTH_OK`、ログイン名`anco`)
- Zapier公式の「Zapier for WordPress」プラグイン(スラッグ`zapier`)は正規品・インストール済み・active(2026-08-06にマツがREST API経由で導入)
- CloudSecure WP Securityの「シンプルWAF」→検知履歴は空、無関係
- CloudSecure WP Securityの「XML-RPC無効化」→一時OFFにして再試行しても改善せず、再度ONに戻し済み
- CloudSecure WP Securityの「ログイン無効化」(ブルートフォース対策)→ロック時間は最大60秒設定なので長時間の詰まりの説明にならない。「ログイン履歴」に出てくる大量の失敗ログイン(XML-RPC、ユーザー名`momo`等)は無関係な外部からの一般的な攻撃ノイズで、Zapierとは無関係(そもそもZapierはREST API経由でこのログには載らない)
- XserverサーバーパネルのWAF設定(シンプルWAF)→全項目OFF、無関係
- WordPress一般設定のサイトURLが`http://`のままだった件、およびXserverの常時SSL化(HTTPS転送設定)が未設定だった件→両方修正済み(2026-08-06)だが403は解消せず

**現在の最有力説**: [Zapier公式ヘルプ](https://help.zapier.com/hc/en-us/articles/8495969550989-Common-Problems-with-WordPress)に、「Jetpack Protectモジュールが、ZapierがアクセスしてくるAWS us-east-1のIP帯を自動ブロックすることがある」という既知の問題が明記されている。chomoand-1.comには単体の「Jetpack Protect」プラグインは入っていないが、今回Jetpack SocialのWordPress.comアカウント接続をした際に、Jetpackの共有クラウド側で同種の保護機能が自動有効化された可能性がある。

**次にやること**: `wp-admin`→「Jetpack」→「My Jetpack」、または`https://cloud.jetpack.com/`のダッシュボードで「Protect」「ブルートフォース攻撃対策」的な項目を探し、一時OFFにしてZapier再接続を試す。改善したら、Protect自体は再度ONに戻しつつAWS us-east-1のIP帯だけホワイトリスト登録する(公式ヘルプに手順あり)。

2026-08-06時点でこの続きは別セッション(スマホ)で継続予定。
