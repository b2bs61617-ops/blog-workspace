# マツの道具箱(2026-11-14〜)

Fable 5.2 がいなくなっても、マツ無しでも回せる道具をまとめたもの(ユカ依頼、GEEKOMでトモキと作成)。
判断の中身(点数の付け方・チェック項目・名簿)はコードとデータに書いてあるので、弱いモデルでも人でも同じ結果になる。

## 開き方

- Windows: `tools\toolbox\run.bat` をダブルクリック
- Mac: `tools/toolbox/run.command` をダブルクリック(初回だけ右クリック→開く)
- ブラウザに道具箱が開く。黒い画面は開いたままにする(閉じると止まる)。そのPCの中だけで動き、外からは見えない。
- マツに「道具箱ひらいて」と言われたら、見える別ウィンドウで上のファイルを起動する(サジェスト穴場ファインダーと同じやり方)。

## 入っている道具

| 道具 | ファイル | すること |
|---|---|---|
| 共通の部品 | `tools/blogkit.py` | .envの読み込み(ローカル→ドライブ)、サイトの表、WordPressの読み書き、記事ブロック、下書き投稿、公開→Indexing→X |
| 事実チェック係 | `tools/fact_check.py` | 日付と曜日、名前の字、年齢・誕生日・メンバーカラー、タイトル、字数、さん付け、読みにくい文、気をつける言葉、リンク切れ |
| 伸びしろ診断 | `tools/nobishiro/nobishiro.py` | 公開記事を全部読み、直す順番つきリストをHTML+CSVで出す。検索データ(表示・クリック・順位)と内部リンクの案つき |
| ネタ先読みカレンダー | `tools/neta_calendar/neta_calendar.py` | 誕生日・行事・毎週の番組から「今すぐ/今週/来週書く」を出す。サイト内に関連記事があれば「更新」 |
| X投稿文の案出し | `tools/xpost_ideas.py` | いまの型で案を作り、URL入り・誘導の一言・長さ超え・固有名詞なし・答えバレを機械で落とす |
| パソコンに入れるAI | `tools/ai_hub.py` の `ollama` | 外部AIが全部だめなときの最後の予備。鍵いらず・ネットいらず |
| 記事スクリプトのひな形 | `tools/_template_article.py` | コピーして本文のデータだけ書く。部品の書き写しをやめる |

どれも記事を勝手に書き換えない・公開しない。公開は今までどおりユーザーの承認のあと(`blogkit.publish`)。

## マツ(Claude)が使うとき

```
python tools/fact_check.py 記事.html --site snowman --title "タイトル" --names "内村光良"   # 投稿前(blog-upload STEP1.57)
python tools/fact_check.py --site trend --post-id 13187                                  # 下書き・公開記事を直接
python tools/xpost_ideas.py check --text "本文" --tags "#SnowMan #目黒蓮" --hide "ブランド名"  # 公開前(publish)
python tools/xpost_ideas.py --site snowman --post-id 687 --hide "答え"                     # 案を外部AIに出させる
python tools/nobishiro/nobishiro.py --site snowman --no-open
python tools/neta_calendar/neta_calendar.py --no-open
python tools/blogkit.py check                                                             # 鍵と接続(キー名だけ表示)
```

- 事実チェックの**NGは直してから投稿**する。注意は読んで判断する。「年を確かめる」「要確認」は公式で確かめる。
- 新しい記事スクリプトは `tools/_template_article.py` をコピーして作る。古い `_build_*.py` は消さない。
- `blogkit.upload_draft` は投稿の前に事実チェックを自動でかけ、NGがあれば止まる。

## データの直し方(ここを育てると道具が賢くなる)

- `tools/data/members.json` … 名簿。メンバーの追加、よくある字のまちがい(`wrong`)、メンバーカラー、誕生日。
  誕生日は記憶で書かない。`python tools/neta_calendar/verify_birthdays.py` がWikipediaで確かめて埋める。
  見つからない人(2026-11-14時点: 髙地優吾)は公式で確かめて手で入れ、`source`に出どころを書く。
- `tools/data/events.json` … 行事・記念日・毎週の番組。`verified:false` は画面に「要確認」と出る。
  ドラマが始まった・終わった、特番の日が決まった、というときはここを直す。
- 伸びしろ診断の点数は `nobishiro.py` の `score()`、X文のNGワードは `xpost_ideas.py` の `LEAD_WORDS`。
  ルールが変わったら、スキルの文章だけでなくここも直す(機械が止めてくれるようになる)。

## 新しいPCで使えるようにする

1. `git pull` する(道具は全部リポジトリに入っている)。
2. 道具箱を開き、いちばん下の「点検する」を押す。足りないものと直し方が出る。
   - Pythonの部品が無い → 「足りない部品を入れる」ボタン
   - 鍵が足りない → Googleドライブの`.env`が見えているか確かめる(見つからなければトモキに聞く)
   - 投稿者が「未登録」→ `docs/wordpress.md` の投稿者の表と `tools/blogkit.py` の `SITES` にそのPCを足す
3. 読むだけの道具(事実チェック・伸びしろ診断・ネタ先読み)は、鍵が無くても動く。

### パソコンに入れるAI(Ollama)

無くても道具は全部動く。入れるのは「無料枠が切れた・ネットが無い」ときの予備がほしいPCだけ。**そのPCの持ち主に一言伝えてから入れる。**

1. Ollamaを入れる: Windows `winget install Ollama.Ollama` / Mac `brew install ollama` → `brew services start ollama`
2. 道具箱の「パソコンに入れるAIのモデルを入れる」を押す(メモリを見て自動で選ぶ)

| メモリ | 入るモデル | 目安 |
|---|---|---|
| 24GB以上(GEEKOMなど) | `gemma3:12b`(約8GB) | 短い質問で15秒くらい。2026-11-14にGEEKOMへ導入ずみ |
| 8〜16GB(ユカのMacなど) | `gemma3:4b`(約3GB) | 速いが日本語はあやしい |

- 日本語の質はGeminiの無料枠より下(変な言葉を作ることがある)。使い道は**X文案の下書きと食いちがい探しの予備まで**。記事の本文は書かせない。
- `ai_hub.py` は Gemini → OpenRouter → Groq → 最後に ollama の順で自動で切り替える。指定したいときは `--provider ollama`。
- 別のモデルを使うときは `.env` に `OLLAMA_MODEL=モデル名`。

## テスト

`python -m pytest tools/tests/test_toolbox.py tools/tests/test_toolbox_apps.py -q`(名簿のまちがい表が正しい名前を巻き込んでいないかも見ている)
