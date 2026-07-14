# Canva MCP連携(アイキャッチ作成)

chomoand-1.com(コイキーズブログ)のアイキャッチは、トモキがCanvaの「Webinar/Keynote Presentation」テンプレで作ったデザインで全記事統一されている。マツが記事を書くときも**同じ見た目**にする必要がある(2026-07-15)。

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

1. **元デザインから1ページだけ複製する**
   - `copy-design(design_id="DAG_zqaJE_8", page_numbers=[36])`
   - ページ番号は「文言の行数構成が近い既存ページ」を選ぶ。36は4行構成の標準形。
   - → 1ページだけの新デザインができる

2. **編集トランザクションを開いてテキスト要素IDを取得する**
   - `start-editing-transaction(design_id=<複製したID>)`
   - レスポンスに`element_id`と現在の4行テキスト、プレビュー画像が返る

3. **行単位でテキストを差し替える**
   - **必ず`find_and_replace_text`を行ごとに1回ずつ**呼ぶ(4回)
   - ⚠️ `replace_text`で4行まとめて置換すると**行ごとのフォントサイズが飛んで全部同じ大きさになる**。絶対に使わないこと。
   - ついでに`update_title`でデザイン名を記事名にしておくと後で探しやすい

4. **コミットする**
   - `commit-editing-transaction(transaction_id=...)`
   - ⚠️ これを呼ばないと変更は**破棄される**

5. **PNGで書き出す**
   - `export-design(design_id=..., format={type:"png", lossless:true, width:1200, height:675})`
   - 返ってきたURLを`Invoke-WebRequest`で`images/<記事名>_eyecatch_canva.png`に保存

6. **WordPressにメディアアップロードして`featured_media`に設定**([blog-uploadスキル](../.claude/skills/blog-upload/SKILL.md))

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
  - 出力: `images/ko1keyz_dekaneko_eyecatch_canva.png`
  - 既存記事とフォント・背景が完全に一致することを確認済み(2026-07-15)
