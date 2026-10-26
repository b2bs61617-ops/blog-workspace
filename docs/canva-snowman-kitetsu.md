# Snow Man・KEY TO LIT のアイキャッチ(Canva上書き)

2026-10-27〜、chomoand-2.com(Snow Man)と chomoand-5.site(KEY TO LIT)のアイキャッチは、トモキが作ったCanvaデザインのページを**複製せず上書き**して書き出す。
`tools/eyecatch_snowman.py` / `tools/eyecatch_kitetsu.py` は使わない(Canva MCPが使えないときの予備)。

| サイト | デザイン | サイズ |
|---|---|---|
| chomoand-2.com | `DAHYbnGesOc`(https://www.canva.com/design/DAHYbnGesOc/U_MPN595p2Df79TlKsoGvA/edit) | 344×208 → 書き出し1200×725 |
| chomoand-5.site | `DAHYbqcAORI`(https://www.canva.com/design/DAHYbqcAORI/TKGEu3TgouFj_1BJ5DpYQw/edit) | 1920×1080 → 書き出し1200×675 |

## ページ

- Snow Man: p1=グループ(青) p2=グループ(9色) p3佐久間大介 p4岩本照 p5深澤辰哉 p6ラウール p7渡辺翔太 p8向井康二 p9阿部亮平 p10目黒蓮 p11宮舘涼太
- KEY TO LIT: p1〜p4=グループ(色違い) p5井上瑞稀 p6猪狩蒼弥 p7佐々木大光 p8中村嶺亜 p9岩﨑大昇
- タイトルにメンバーが1人だけ→そのメンバーのページ。グループ・複数人→グループのページ。

## 文字の型(1つの文字枠に、行ごとにサイズの違う区切りが入っている)

| | 1行目(小) | 2行目(大) | 3行目以降(小) |
|---|---|---|---|
| Snow Man メンバー | Snow Man | メンバー名 | タイトルの残り2行(各約12字まで) |
| Snow Man グループ | Snow Man | 話題キーワード(5字以内) | タイトルの残り2行 |
| KEY TO LIT メンバー | KEY TO LIT | メンバー名 | タイトルの残り2行(各約10字まで) |
| KEY TO LIT グループ | タイトル前半(12字まで) | KEY TO LIT | タイトルの残り(1〜2行、各10字まで) |

- タイトルからメンバー名・グループ名・【】は省く。2行に収まらないときは助詞や日付を少し削ってよい。

## 手順

1. `read-design`(open_transaction)で対象ページの文字枠の`locator_id`と今の文字を確認する。
2. `edit-design`の`find_and_replace_text`で区切りごとに置き換える。下段の「1行目\n2行目」は1つの区切りなので、`\n`込みで丸ごと置換する。
   - 名前の区切りを触るときは「大の文字→新しい名前」を先に置換する(小の行に同じ文字があると先にそっちが当たる)。
3. サムネイルで折り返しがないか確認 → `commit`。
4. `export-design`(jpg / quality 92 / width 1200 / pages=[対象ページ])。
5. 書き出しURLをダウンロード → WordPressにmedia POST → `featured_media`に設定(blog-upload STEP5)。
6. 同じページで複数記事を作るときは、1本ずつ「上書き→保存→書き出し」を繰り返す。

## ハマりどころ

- 2行しかない枠に行を足すと、足した行が名前と同じ特大サイズになる。`add_text`で足すとフォントが普通のゴシックになって見本と合わない。→ 枠の作りが足りないときはトモキにCanva上で仮の行を入れてもらう。
- 2026-10-27に既存記事を全部差し替え済み(Snow Man 14本+トモキ手作り4本はそのまま、KEY TO LIT 58本)。復元用: `backups/chomoand2_eyecatch_canva_2026-10-27/`・`backups/chomoand5_eyecatch_canva_2026-10-27/`(`apply.py restore`)。
