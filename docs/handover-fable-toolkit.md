# 引き継ぎ: Fable 5.2 がいるうちに作る「マツの道具」5つ(2026-11-14 ユカ依頼)

**2026-11-14 GEEKOM(トモキ)で1〜6と道具箱を作成ずみ・テストずみ。** 使い方は[toolbox.md](toolbox.md)。下の「作るもの」は設計の記録として残してある。
全部済んだらこのファイルを消し、CLAUDE.mdの「進行中の引き継ぎ」の行も消す(ファイルの削除はユーザーに確認してから)。

## 残っていること

- **各PCでの点検**: `git pull`のあと道具箱の「点検する」を押す。投稿者が「未登録」のPC・サイトは`tools/blogkit.py`の`SITES`と`docs/wordpress.md`の表に足す(GEEKOMのchomoand-1.com、ユカのMacのSnow Man以外、が未登録)。
- **MacでのPython 3.9動作確認**: GEEKOM(3.12)でしか動かしていない。3.9で落ちない書き方にしてあるが、ユカのMacで`python3 -m pytest tools/tests/test_toolbox.py tools/tests/test_toolbox_apps.py -q`を一度通す。
- **パソコンに入れるAI**: GEEKOMだけ導入ずみ(gemma3:12b)。ほかのPCは持ち主に聞いてから(手順はtoolbox.md)。
- **髙地優吾の誕生日**: Wikipediaから自動で取れなかった。公式で確かめて`tools/data/members.json`に入れる。
- **リンク切れの直し方**(2026-11-14調査の102記事): A外す/B差し替え/C週1自動チェック、トモキの返事待ち。調べる部品は`fact_check.check_url`と`nobishiro.py --links`に入れてある。
- **使い捨てスクリプトの大そうじ**: 新しい記事から`tools/_template_article.py`を使う。古い約190本は消していない(消すならユーザー確認)。
- KO1KEYZの公開(韓国語・英語・アイキャッチそろえ・韓国語のX)は`blogkit.publish`に入れていない。今までどおりpublishスキルの手順でやる。

## ユカの依頼(原文の要点)

- Fable 5.2 は期間限定。使えるうちに、**Fableがいなくなっても動くアプリ・ソフトをマツが作る**。
- または**AIをパソコンに入れる**。
- それを踏まえて、マツが出した5つの案を**全部やる**。

つまり成果物は「その場の分析結果」ではなく、**あとで誰でも(弱いモデルでも、マツ無しでも)回せる道具**にする。
判断の中身(点数の付け方・チェック項目・名前の表)をコードとデータに書き切るのが、いま頭脳を使う場所。

## 作るもの

置き場所は `tools/` 配下。すべて4台のPCに配られるので、Windows/Mac両対応で書く。

### 1. 伸びしろ診断(`tools/nobishiro/` を想定)

公開済みの記事を全サイトから集めて「直す順番つきリスト」をHTML+CSVで出す。

- 記事の取得はWP REST(`/wp-json/wp/v2/posts?status=publish`)。公開記事は認証なしで読める。
- 機械で見る項目: タイトルの長さと疑問形/本文の字数(2,500字未満)/H2・H3の数/内部リンクの数/
  どこからもリンクされていない記事/更新からの日数/アイキャッチ無し/画像のalt無し/
  `easy_read.py check` のNG数/リード文直後の区切り線。
- 内部リンク案: 記事Aの主役の名前が記事Bの本文に出るのにリンクが無い組を出す。
- Search Consoleの鍵があれば足す: 「表示は多いのにクリックが少ない」「順位8〜20位」の記事を上位に。
  鍵の流用方法は `docs/tools.md` の検索順位チェックの節(`searchAnalytics.query`)。無ければ飛ばして止めない。
- 記事は書き換えない。読むだけ。

### 2. ネタ先読みカレンダー

「検索が伸びる前に仕込む記事」を2〜4週間ぶん出す。

- データファイル(JSON)に、メンバーの誕生日・デビュー日・毎年の行事・レギュラー番組を持つ。
  `docs/annual-event-calendar.md` と `docs/wordpress.md` のメンバー情報を元にする。
- 何日前に仕込むか(リードタイム)を種類ごとに持ち、今日から見て「今週書く」「来週書く」を並べる。
- 各ネタについて、サイト内に同じ話題の記事があるかをWP検索で確かめて「新規/更新」を付ける。
- **誕生日などの事実はマツの記憶で埋めない**。公式プロフィールで確かめたものだけ入れ、未確認は`"verified": false`にして画面で「要確認」と出す。

### 3. 共通の投稿・公開ツール(大そうじ)

`tools/` に記事ごとの使い捨てスクリプトが約190本ある(`_build_*.py` `_build_upload_*.py` `_publish_*.py` `_edit_*.py`)。
毎回ほぼ同じ部品を書き直している。

- 共通の部品にまとめる: ブロックを作る関数(`p` `h2` `h3` `html` `table` `mini` `mark` `youtube` `xembed` `gmap`)、
  .envの読み込み(ローカル→Googleドライブの順)、下書き投稿、二重投稿よけの控え(`*_posted.json`)、
  公開→Indexing→X投稿の流れ。
- 見本: `tools/_build_upload_chinen_menkyo_gasshuku_1113.py`(組み立て+下書き)、
  `tools/_publish_trend_chinen_menkyo_1113.py`(公開+Indexing+X)。
- 記事ごとのスクリプトは「本文のデータだけ」の短いファイルになるのが目標。
- **古いスクリプトは消さない**(削除はユーザー確認が要る)。新しい記事から共通ツールを使う形にする。
- 公開は今までどおりユーザー承認制。共通化しても勝手に公開しない。

### 4. 投稿前の事実チェック係

下書きを機械で調べ、公開前に直すところを出す。`blog-upload` の手順に組み込む(注意書きではなく機械で強制)。

- 日付と曜日が合っているか(例「11月18日(水)」)。計算で分かる。
- メンバー名の字のまちがい(名簿と照合。例: 髙地/高地、岩﨑/岩崎)。
- 年齢と生年月日のずれ、メンバーカラーのまちがい(名簿があるもの)。
- リンク切れ、タイトルと本文の数字のずれ、字数、`easy_read.py` と `honorific.py` の結果もまとめて出す。
- 未成年・一般人まわりの言葉(学校名の断定など)に印を付ける。線引きは `koi-real` スキル。
- おまけ: `ai_hub.py` で外部AIに「本文の中で食いちがう記述」を聞く(無くても動く)。

### 5. X投稿文の案出し

`ai_hub.py xpost` がすでにあるが、型が古い(女性ファン口調・115字のみ)。

- いまの型は [publish](../.claude/skills/publish/SKILL.md) の「Xの投稿文の作り方」。
  **誘導の一言は入れない、答えは書かずヒントだけ、URLは本文に入れない**(2026-10-29〜トモキ指示)。
- 案を複数出したあと、機械で落とす: URL入り/「コメント欄」「こちら👇」入り/長さ超え(`x_auto_post_buffer.weighted_length`)/固有名詞なし。

### 6. パソコンに入れるAI

- 正直な説明: AIを一から作るのではなく、**無料で公開されているAIをパソコンに入れる**形になる。
- Ollamaを入れ、`ai_hub.py` に`ollama`を最後の予備として足す(ネットが無くても、無料枠が切れても動く)。
- ユカのMacはメモリ8GB(A18 Pro)。入るのは4B級の小さいモデルまで。日本語の質はGeminiの無料枠より下。
  用途はX文案の下書きと食いちがい探しの予備にとどめる。記事の本文は書かせない。
- メモリの多いPC(GEEKOMなど)ならもっと大きいモデルが入る。PCごとに決める。
- インストールはPCごとの作業。そのPCの持ち主に一言伝えてから入れる。

### まとめ役: マツの道具箱

1〜5をボタンで動かせる入口を1つ作る。ダブルクリックで開く(Macは`.command`、Windowsは`.bat`)。
サジェスト穴場ファインダー(`tools/suggest-finder/run.bat`)と同じ考え方。Pythonの標準ライブラリだけで画面を出す(nodeは無い)。

## 進める順番

1. 共通の部品(.env読み込み・WP読み書き)…ほかの全部が使う
2. 事実チェック係(4)…毎日の記事にすぐ効く
3. 伸びしろ診断(1)
4. ネタ先読みカレンダー(2)
5. X投稿文(5)と入れるAI(6)
6. 道具箱の入口、`docs/tools.md`とCLAUDE.mdのツール表、メンバーへのお知らせ

純粋関数には `tools/tests/` にテストを足す(CLAUDE.mdのルール)。

## 調べて分かったこと(作るときの注意)

- **ユカのMacのPythonは3.9.6**(`/usr/bin/python3`、`python`コマンドは無い)。`str | None` や `match` は使わない。
  `tools/affiliate_box.py` は `str | None` を使っているので、このMacでは`from __future__ import annotations`が無いと落ちるはず(未確認、要チェック)。
- ユカのMacのローカル`.env`には `WP_TREND_*` `WP_AUDITION_*` `WP_KOIKEYS_*` などしか無い。
  `WP_CHOMO2_*` `WP_CHOMO4_*` `WP_CHOMO5_*` `BUFFER_*` はGoogleドライブの`.env`
  (`~/Library/CloudStorage/GoogleDrive-<アカウント>/マイドライブ/.env`)から補う。
  `GOOGLE_INDEXING_CREDENTIALS_PATH` だけはローカル優先(ドライブ側はWindowsのパス)。
  いまは各スクリプトがこの読み込みを書き写しているので、共通部品で一本化する。
- `.env`の中身は画面に出さない。確かめるときはキー名だけ見る。
- ユカのMacにはnode・ollamaが無い。brewとffmpegはある。
- 外部AIは `tools/ai_hub.py` の `call()` を使う(Gemini→ほかの順に自動で切り替え)。新しく窓口を作らない。
- 使える既存の部品: `easy_read.py`(`fix`/`check`)、`honorific.py`(`add_san`/`missing`)、
  `x_auto_post_buffer.py`(`weighted_length` `fetch_article_images` `post_thread`)、
  `google_indexing.notify`、`check_search_console.py`(`build_session` `fetch_post_urls`)。
- zshでは `echo ===` がエラーになる(`=`始まりの展開)。区切りは `echo "---"` と書く。

## 止まっている別の宿題(この件とは別)

- VIVANTアイキャッチ18件の作り直し: `backups/vivant_eyecatch_redo_2026-11-13/plan.json`。Canvaの認証待ち。
- トレンド速報アイキャッチ12件の差し替え: `backups/chomoand_trend_eyecatch_canva_2026-11-10/plan.json`。同じくCanva待ち。
