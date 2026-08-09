# X(旧Twitter)自動投稿のセットアップ手順

**現在の状態(2026-08-09)**: 実装済み・**トモキ本人によるDeveloper App作成待ち**。3サイトぶんのAPIキー・アクセストークンが`.env`に設定されるまでは、[publishスキル](../.claude/skills/publish/SKILL.md)から呼ばれても自動でスキップされる(公開処理自体は止まらない)。

記事公開時にXへ自動投稿する仕組み(`tools/x_auto_post.py`)の初回セットアップ手順。旧来のZapier連携([docs/sns-auto-post-setup.md](sns-auto-post-setup.md)参照、X部分は本ドキュメントに置き換え・廃止)から移行した。

**Why:** ZapierのCreate TweetアクションはXアカウントへのOAuthログインだけで済み手軽だったが、(1)本文にURLを含めるとXのアルゴリズム上リーチが30〜50%減る、(2)リプライスレッド(本文はURL無し→1件目へのリプでURLのみ)を組めない、という2つの制約があった。自前でX API v2を叩けば両方解決できるため、2026-08-09にユーザーと相談の上で自作ソフトへの置き換えを決定した。

**投稿の型:** 1件目=画像+フック文+ハッシュタグ(URL無し)→2件目=1件目へのリプライとしてURLのみ、の2連投。文面は記事の内容にあわせてマツ(Claude)がその都度作文し、スクリプトは投稿の実行だけを担当する。

## 1. X Developer Appの作成(サイトごとに、トモキ本人が実施)

3ブログは別アカウント運用なので、**サイトごとに別のXアカウント・別のDeveloper App**が必要(chomoand.com用、chomoand-0.com用、chomoand-1.com用の3セット)。

1. 投稿に使いたいXアカウントで[developer.x.com](https://developer.x.com/)にログインし、Developer Portalでプロジェクト・Appを作成する
2. Appの「User authentication settings」で以下を設定する:
   - App permissions: **Read and write**(投稿に書き込み権限が必須。デフォルトのRead-onlyのままだと投稿が401/403で失敗する)
   - Type of App: Web App(またはNative App。Callback URL等はダミーでよい。今回はOAuth 1.0aのAPIキー方式のみ使うのでOAuth2のリダイレクト自体は使わない)
3. 「Keys and tokens」タブで以下4つを発行・控える:
   - **API Key**(Consumer Key)
   - **API Key Secret**(Consumer Secret)
   - **Access Token**
   - **Access Token Secret**
   - Access Token/Secretは、直前にApp permissionsを「Read and write」に変更した**後**に再生成すること(先に発行したトークンは権限が反映されず書き込みに使えない)

## 2. ローカル設定(トモキ本人が実施)

1. `.env`に3サイトぶん追加(`.env.example`にひな形あり):
   ```
   X_TREND_API_KEY=...
   X_TREND_API_SECRET=...
   X_TREND_ACCESS_TOKEN=...
   X_TREND_ACCESS_TOKEN_SECRET=...

   X_AUDITION_API_KEY=...
   （以下同様、X_AUDITION_*/X_KOIKEYS_*）
   ```
2. 必要なライブラリをインストール:
   ```
   python -m pip install tweepy requests
   ```

マツ(Claude Code)はAPIキーの値をチャットで教えたり代筆したりしないので、上記はユーザー自身の作業になる。

## 3. 動作確認

```
python tools/x_auto_post.py --site trend \
  --text "テスト投稿ワン" \
  --hashtags "" \
  --image "https://chomoand.com/wp-content/uploads/xxxxx.jpg" \
  --url "https://chomoand.com/"
```

JSON形式で`main_tweet_url`/`reply_tweet_url`が返り、実際にXで2件連続投稿(2件目が1件目へのリプライになっている)を確認できれば設定完了。3サイト分(`--site trend/audition/koikeys`)それぞれで確認する。

## 使われている場所

- `tools/x_auto_post.py`: 投稿本体(画像アップロード→1件目投稿→2件目をリプライとして投稿)
- [publishスキル](../.claude/skills/publish/SKILL.md): 記事公開時、公開URL確定後に自動で呼び出す。サイトの`X_*`キーが未設定の場合は投稿だけスキップし、公開処理自体は止まらない(Google Indexing/Naver IndexNowと同じフェイルセーフ方式)

## Instagramについて

Instagram側は引き続き[Jetpack Social](sns-auto-post-setup.md)を使う(単一画像+キャプションの自動シェア)。カルーセル(複数画像スワイプ)投稿の自作化は将来の拡張として別途検討する。
