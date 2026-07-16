# Canva MCP連携(アイキャッチ作成)

chomoand-1.com(コイキーズブログ)のアイキャッチは、トモキがCanvaの「Webinar/Keynote Presentation」テンプレで作ったデザインで全記事統一されている。マツが記事を書くときも**同じ見た目**にする必要がある(2026-07-15)。

**chomoand.com(恋愛リアリティ番組の出演者wiki)も2026-07-16からCanva MCPを使う。** ただしKO1KEYZとは別系統の独自マスターデザイン。手順は[docs/canva-mcp-chomoand.md](canva-mcp-chomoand.md)を参照。

## なぜCanva MCPを使うのか

当初は`tools/eyecatch_koikeyz.py`(HTML+Playwright)で見た目を再現したが、**フォントがCanvaの本物と違う**ためトモキから「Canvaを使って作ってほしい」と指示があった。そこでCanva公式のリモートMCPサーバーを接続し、マツがCanva上で直接デザインを作って書き出す方式に切り替えた。**2026-07-15に動作検証済み。以下のフローで本物と完全に同じアイキャッチが作れる。**

## 接続状況

- MCPサーバーURL: `https://mcp.canva.com/mcp`(Canva公式リモートMCP)
- 登録済み: プロジェクトスコープ(`.mcp.json`、Git管理・4台に配布)
- **認証はPCごと・ユーザーごとに必要**。`/mcp` → `canva` → Authenticate → ブラウザでCanvaにログインして許可。
- `.mcp.json`はセッション起動時にしか読まれないため、追加した直後のセッションでは`/mcp`に出てこない。**新しいセッションを開始してから認証する**こと。認証後もセッションを再起動しないとツールが生えてこない。
- VSCode拡張のセッションからは認証フロー(OAuth)を開始できない。**ターミナルで`claude`を起動して`/mcp`から認証**する。`claude`はPATHが通っていないPCがあるので、その場合は`& "$env:USERPROFILE\.local\bin\claude.exe"`で起動する。

## 元になるデザイン(絶対に直接編集しない)

- **デザイン名**: `Webinar Keynote Presentation`
- **design_id**: `DAG_zqaJE_8`
- **中身**: 1920×1080のスライドが39ページ。**1ページ=1記事のアイキャッチ**で、トモキが記事を書くたびにページを足していく運用になっている。
- これはトモキの資産なので、**マツはこのデザインを直接編集しない**。必ず`copy-design`で複製してから使う。

### 1ページの構造

| 要素 | 内容 |
|---|---|
| 背景画像(2枚) | 生成り地のグレイン(粒状)グラデーション + カラフルなブラシストローク |
| テキスト要素(1個だけ) | **4行が1つのテキスト要素に入っている**。行ごとにフォントサイズが違う(2行目だけ特大) |

テキスト4行の型:

```
1行目: グループ名・番組名など(小)          例: KO1KEYZ / PRODUCE 101 新世界
2行目: 記事の主題ワード(特大)               例: デカ猫 / ポジションバトル
3行目: 問いかけ・補足(中)                   例: とは？加藤大樹×矢田佳暉
4行目: 補足2行目(中)                        例: ケミ名の由来を解説！
```

## 運用フロー(検証済み)

1. **元デザインから「ページ36」だけを複製する**
   - `copy-design(design_id="DAG_zqaJE_8", page_numbers=[36])`
   - **複製元は必ずページ36にする**。理由は下の「⚠️ ページ36以外を使ってはいけない理由」を参照。
   - → 1ページだけの新デザインができる

2. **編集トランザクションを開いてテキスト要素IDを取得する**
   - `start-editing-transaction(design_id=<複製したID>)`
   - レスポンスに`element_id`と現在の4行テキスト、背景画像2枚の`element_id`、プレビュー画像が返る

3. **行単位でテキストを差し替える**
   - **必ず`find_and_replace_text`を行ごとに1回ずつ**呼ぶ(4回)
   - ⚠️ `replace_text`で4行まとめて置換すると**行ごとのフォントサイズが飛んで全部同じ大きさになる**。絶対に使わないこと。
   - ついでに`update_title`でデザイン名を記事名にしておくと後で探しやすい

4. **背景の色を変える(毎回必ずやる)**
   - トモキの指示(2026-07-15):「サイトのアイキャッチは全部色が違ってカラフル。**毎回色を変えること**。色使いはマツがランダムに選んでよい」
   - ブラシストローク要素(ページ36では`...-LBsTwKB5X1rWZS4T`、alt_textが`a colorful gradient brush stroke`のほう)に対して:
     - `update_fill`で**下のアセット一覧からランダムに1つ選んで**差し替える
     - `resize_element`(`preserve_aspect_ratio: true`、width 1600〜2300程度)+ `position_element`でランダムに配置する
   - ブラシが画面の外に大きくはみ出していると色がほとんど出ない。**画面中央〜全体を覆うくらいに配置する**と色がはっきり出る(例: width 2100 / left -90 / top -430)
   - もう1枚のグレイン地(`MAEn_b947YY`、alt_textなし・decorative)は下地なのでそのままでよい

5. **コミットする**
   - `commit-editing-transaction(transaction_id=...)`
   - ⚠️ これを呼ばないと変更は**破棄される**

6. **PNGで書き出す**
   - `export-design(design_id=..., format={type:"png", lossless:true, width:1200, height:675})`
   - 返ってきたURLを`Invoke-WebRequest`で`images/<記事名>_eyecatch_canva.png`に保存

7. **WordPressにメディアアップロードして`featured_media`に設定**([blog-uploadスキル](../.claude/skills/blog-upload/SKILL.md))

## 背景アセット一覧(色替え用・ここからランダムに選ぶ)

すべてCanva標準の「Glowy Gradient Abstract Brush Stroke Blob」シリーズ。トモキが既存記事で実際に使っているものなので、どれを選んでもサイトの世界観から外れない。

| asset_id | 色味 |
|---|---|
| `MAEn_R6sFPg` | 紫+オレンジ+赤+水色(鮮やか) |
| `MAEn_fa8Kow` | 赤+黄+緑+紫(レインボー) |
| `MAEn_YBWNzA` | 青メイン+黄+赤 |
| `MAEn_XQvXLE` | 青+黄+オレンジ |
| `MAEn_avMm94` | 赤+オレンジ+水色+紫 |
| `MAEn_YuJcNg` | 青紫+赤+緑 |
| `MAEn_VCWBdg` | 青+黄+ピンク |
| `MAEn_UrK2cA` | 青+赤(淡いパステル) |
| `MAEn_VZqPFM` | サーモン+緑(ページ36の初期値) |

## ⚠️ ページ36以外を使ってはいけない理由(ハマりどころ)

`find_and_replace_text`には**「1つの行ブロック(region)の中の、改行より後ろのテキストは置換できない」**という挙動がある。しかも失敗しても`status: success`が返る(**サイレント失敗**)ので気づきにくい。

- ページ36は4行が**それぞれ独立したregion**になっているため、4行すべて置換できる ✅
- ページ11などは3〜4行目が`"12人分の意味・由来は？\n徹底解説！\n"`のように**1つのregionに結合**していて、後半の行がどうやっても置換できない ❌

もし別ページを使いたくなったら、`start-editing-transaction`のレスポンスで`richtexts[].regions[].text`を確認し、**途中に`\n`を含むregionが無いこと**を必ず確かめること。

なお、**色を変えるのに複製元ページを変える必要はない**(ページ36 + `update_fill`でのアセット差し替えで色は十分変わる)。

## できること・できないこと(プラン制限)

| 機能 | 可否 |
|---|---|
| デザインの検索・読み取り・複製(ページ指定可) | ✅ |
| テキストの差し替え・書式変更・要素の移動/リサイズ | ✅ |
| PNG/JPG書き出し(サイズ指定可) | ✅ |
| **ページの新規追加・ページ単位の複製** | ❌ APIに操作がない → だから`copy-design`でデザインごと複製する |
| ブランドテンプレのAutofill(テキスト自動差し込み) | ❌ Enterpriseプランのみ |
| デザインのリサイズ | Canva Pro以上 |

## フォールバック

Canva MCPが使えない・認証切れのときは`tools/eyecatch_koikeyz.py`(HTML再現版)で作る。見た目はほぼ同じだがフォントだけ別物(M PLUS Rounded 1c Black)。仕様は[docs/eyecatch-style.md](eyecatch-style.md)参照。

## 検証済みの実例

- 「デカ猫」記事(chomoand-1.com、記事ID **10569**、下書き)
  - 複製先デザイン: `DAHPXycEI_w`(元の36ページ目を複製)
  - 背景: `MAEn_XQvXLE`(青+黄+オレンジ)に差し替え、width 2100 / left -90 / top -430 で配置
  - 出力: `images/ko1keyz_dekaneko_eyecatch_canva.png` → WordPressメディアID 10578
  - 既存記事とフォントが完全に一致し、かつ色は他記事とかぶらないことを確認済み(2026-07-15)
