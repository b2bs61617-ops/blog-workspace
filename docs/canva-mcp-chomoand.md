# Canva MCP連携(chomoand.comのアイキャッチ作成)

chomoand.com(恋愛リアリティ番組の出演者wiki)のアイキャッチも、chomoand-1.com(コイキーズ)と同じ運用でCanva MCPを使う(2026-07-16)。Canva MCPの基本的な仕組み・認証手順は[docs/canva-mcp.md](canva-mcp.md)を参照。ここにはchomoand.com専用の差分だけ書く。

## 元になるデザイン(chomoand.com専用の新規マスター)

- **デザイン名**: `chomoand.com 恋リア出演者wiki アイキャッチ ベーステンプレート`
- **design_id**: `DAHPjgiBOTI`
- KO1KEYZの`DAG_zqaJE_8`(トモキの資産)とは**完全に別系統のデザイン**。KO1KEYZ側を直接編集も複製元にも使わずに、Canva MCPの`generate-design`(AI生成)→`resize-design`(1920×1080化)→`perform-editing-operations`で一から組み立てた。
- 1ページだけのデザイン(KO1KEYZのように39ページはない)。**複製するときは`page_numbers`指定不要**、デザインごと`copy-design`する。

### 1ページの構造

| 要素 | 内容 |
|---|---|
| 背景画像(2枚) | グレイン地グラデーション(`MAEn_b947YY`) + カラフルなブラシストローク(初期値`MAEn_VZqPFM`) |
| テキスト要素(**3個・独立**) | 1行目(小)・2行目(特大)・3〜4行目(中・1要素に2行) |

テキストの型(ユーザー指定どおり):

```
1行目: 番組名(小)            例: 今日、好きになりました
2行目: 出演者名(特大)
3〜4行目: 疑問形トピック+補足(中・同一要素に\n区切りで2行)  例: 学歴は？出身高校を調査 / 家族構成や彼氏の噂も解説！
```

## KO1KEYZ方式との違い(重要)

KO1KEYZのページ36は「1つのテキスト要素の中に4行がそれぞれ独立したregionとして入っている」構造で、これは人間がCanvaエディタ上で手作業により行ごとにフォントサイズを変えて作ったもの。**Canva MCPの編集APIには新しいテキスト要素を追加する操作が存在しない**ため、この構造をAPIだけでゼロから複製することはできない(検証済み)。

そのため、このchomoand.com用デザインでは方針を変え、**4行を3つの独立したテキスト要素に分けた**:

- 1行目(番組名)・2行目(出演者名)は単独の要素
- 3行目(疑問形)と4行目(補足)は同じサイズでよいため、1つの要素に`\n`で2行入れる

この結果、KO1KEYZ側の罠(`find_and_replace_text`が改行より後ろのテキストに対してサイレント失敗する)を**回避できている**。検証済み: 3〜4行目の要素に対して`find_and_replace_text`で2行目(`\n`より後ろ)を書き換えても正常に反映される(2026-07-16確認)。ただし念のため、置換は`replace_text`(要素まるごと置換)を使う運用を基本とする。3要素とも「1要素=1サイズ」なので`replace_text`でフォントサイズが飛ぶ心配もない(KO1KEYZ側で`replace_text`が禁止されているのはこの罠を回避するため)。

## フォントについて(既知の制約)

Canva MCPの編集API(`format_text`)は**フォントサイズ・太さ・スタイルは変更できるが、フォントファミリー(書体)は変更できない**(公式ツールの仕様)。このデザインは`generate-design`のAI生成結果からベースを作っているため、KO1KEYZ(トモキが選んだ書体)と**厳密に同一の書体ではない**(太めの丸ゴシック系で近い見た目にはなっている)。書体を完全一致させたい場合はCanva UI上で手動調整が必要。

## 運用フロー

1. **マスターをデザインごと複製する**
   - `copy-design(design_id="DAHPjgiBOTI")`(`page_numbers`指定不要、1ページしかない)

2. **編集トランザクションを開いてテキスト要素IDを取得する**
   - `start-editing-transaction(design_id=<複製したID>)`
   - **要素IDは複製のたびに変わる**ので、必ずレスポンスから毎回取得すること(ハードコードしない)。`richtexts`配列に3要素が返る。テキストの内容(`今日、好きになりました`/`出演者名`/`学歴は？出身高校を調査\n家族構成や彼氏の噂も解説！`)で見分けられる。

3. **3つのテキスト要素を`replace_text`で置換する**
   - 1行目要素 → 番組名
   - 2行目要素 → 出演者名
   - 3〜4行目要素 → `疑問形トピック\n補足`(`\n`で2行にする)

4. **背景の色を変える(毎回必ずやる)**
   - ブラシストローク要素(alt_textが`a colorful gradient brush stroke`のほう)に対して、下の背景アセット一覧から**ランダムに1つ選んで**`update_fill`
   - `resize_element`(`preserve_aspect_ratio: true`、width 1600〜2300程度)+ `position_element`でランダムに配置する(初期値: width 2100 / left -90 / top -430)
   - グレイン地(alt_textが`a decorative grainy gradient background`のほう、asset_id `MAEn_b947YY`)は下地なのでそのままでよい

5. **コミットする**
   - `commit-editing-transaction(transaction_id=...)`

6. **PNGで書き出す**
   - `export-design(design_id=..., format={type:"png", lossless:true, width:1200, height:675})`
   - `images/<記事名>_eyecatch_canva.png`に保存

7. **WordPressにメディアアップロードして`featured_media`に設定**([blog-uploadスキル](../.claude/skills/blog-upload/SKILL.md))

## 背景アセット一覧(色替え用)

KO1KEYZと**全く同じCanva標準ストックアセット**(「Glowy Gradient Abstract Brush Stroke Blob」シリーズ)を使う。トモキ個人の資産ではなくCanva公式のストック素材なので、chomoand.com側でも同じIDがそのまま使える(2026-07-16に`get-assets`で確認済み)。一覧は[docs/canva-mcp.mdの背景アセット一覧](canva-mcp.md#背景アセット一覧色替え用ここからランダムに選ぶ)を参照。

## 検証済みの実例

- マスターデザイン作成時のサンプル(記事に紐付いていないテンプレート確認用)
  - `images/chomoand_eyecatch_template_sample.png`
  - 内容: 「今日、好きになりました / 出演者名 / 学歴は？出身高校を調査 / 家族構成や彼氏の噂も解説！」
  - 背景: `MAEn_VZqPFM`
  - 3要素とも`replace_text`・`find_and_replace_text`双方で正常に置換できることを確認(2026-07-16)
