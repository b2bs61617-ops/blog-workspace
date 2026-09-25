# X(旧Twitter)自動投稿のセットアップ手順

**現在の状態(2026-09-23更新)**: **Buffer経由で自動投稿を再開済み**。`tools/x_auto_post_buffer.py`が[publishスキル](../.claude/skills/publish/SKILL.md)から自動で呼ばれる。

Bufferは公式にXとAPI連携している外部サービスで、投稿はBuffer側の定額プラン(無料枠あり)内で行われるため、下記「料金についての判明事項」にあるX API単体のPay-Per-Use課金($0.20/URL付き投稿)は発生しない。ブラウザ自動化(下記「検討した代替案」)のような凍結リスクもない(BufferはXの正規パートナーとしてOAuth連携しているため)。全サイト(2026-09-25からchomoand-4.blogのトラジャ記事も対象)で@chomoand17を共通利用しているため、旧方式(サイト別Developer App)と違いBufferのチャンネルは1つだけでよい。

**セットアップ済みの内容**(2026-09-23、トモキ本人+マツで実施):
1. buffer.comで無料アカウント作成、@chomoand17を接続
2. developers.buffer.comでPersonal Access Key発行(有効期限は無期限〜長期のものを選択)
3. `.env`に`BUFFER_ACCESS_TOKEN`・`BUFFER_X_CHANNEL_ID`を設定
4. Buffer API(GraphQL、`https://api.buffer.com`)で実投稿テスト済み。`createPost`の`metadata.twitter.thread`でスレッド(1件目=画像+テキスト→2件目=リプライ)を組み、`mode: shareNow`で即時投稿。画像は公開URLを渡すだけでアップロード不要
5. `tools/x_auto_post_buffer.py`を作成、`post_thread(hook_text, hashtags, image_url, article_url)`で呼び出し可能。戻り値に`tweet_url`(投稿されたツイートの実URL)を含む
6. (2026-09-25追加)`--due-at`/`due_at`引数で予約投稿に対応(`mode: customScheduled`+`dueAt`)。一括公開時の連投回避に使う。**無料プランは予約枠が最大10件**なので、それ以上は枠が空いてから追加する

以下は旧方式(X API直接利用)の検討記録。参考として残す。`tools/x_auto_post.py`自体もコードは削除せず置いてある(現在は未使用)。

## 料金についての判明事項(2026-08-09調査)

- 2026年2月にFree/Basic/Proの月額プランが廃止され、新規開発者はPay-Per-Use(従量課金)一択になった([Enterprise](https://developer.x.com/)は別途、月4万ドル超級)
- 単価(2026-04-20改定後): 通常投稿$0.015、**URL付き投稿$0.20**(通常の約13倍)、自分のデータ読み取り$0.001
- **リプライに逃がしてもAPI課金は減らない**: このツールの「1件目=URL無し→2件目=リプでURLのみ」という設計はXのアルゴリズム上のリーチ対策(本文にURLがあるとリーチが落ちる)のためであって、課金対策ではない。URLを含むツイートである以上、本文だろうとリプだろうと$0.20かかる
- 月100投稿(記事50本×2連投)の試算: 50×($0.015+$0.20)=**約$10.75/月**(1ドル≒160円で約1,700円)。ここに画像アップロードのコストが追加でかかる可能性があるが単価は未確認
- 出典: [X API 料金改定まとめ(2026年4月20日適用)](https://qiita.com/ma7ma7pipipi/items/4cef4326138edc295c31)、[X's $0.20 Link Fee](https://opentweet.io/blog/x-api-link-post-fee)、[How Much Does the X API Cost in 2026?](https://twitterapi.io/blog/x-api-cost-breakdown-2026)

## 検討した代替案(不採用)

**ブラウザ自動化(Xiyと同じPlaywright方式)で投稿すれば課金ゼロにできる**という案も検討した。技術的には可能(Xiyが既に同じ方式でログイン済みブラウザを操作している)だが、読み取り専用のスクレイピングと違い書き込み(投稿)の自動化はX側の検知・アカウント凍結リスクがより高いと考えられるため、2026-08-09時点では見送り。将来コスト以上にリスクが許容できると判断したら再検討する。

## 手動投稿の手順(当面の運用)

Xへの投稿は当面手動で行う。[publishスキル](../.claude/skills/publish/SKILL.md)の「Xの投稿文の作り方」の型(記事タイプ別のフック文・ハッシュタグのパターン)は手動投稿でもそのまま使う。

1. 1件目: 記事の画像を添付し、フック文＋ハッシュタグを投稿(**本文にURLを含めない**)
2. 2件目: 1件目の**返信(リプライ、吹き出しアイコン)**からURLのみを投稿(「引用する」は使わない。引用は新しい独立投稿になり、それ自体がURL付き投稿としてリーチが落ちるため別物)

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
