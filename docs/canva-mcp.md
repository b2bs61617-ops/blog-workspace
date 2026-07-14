# Canva MCP連携(アイキャッチ作成)

chomoand-1.com(コイキーズブログ)のアイキャッチは、トモキがCanvaの「Webinar/Keynote Presentation」テンプレで作ったデザインで全記事統一されている。マツが記事を書くときも**同じ見た目**にする必要がある(2026-07-15)。

## なぜCanva MCPを使うのか

当初は`tools/eyecatch_koikeyz.py`(HTML+Playwright)で見た目を再現したが、**フォントがCanvaの本物と違う**ためトモキから「Canvaを使って作ってほしい」と指示があった。そこでCanva公式のリモートMCPサーバーを接続し、マツがCanva上で直接デザインを作って書き出す方式に切り替える。

## 接続状況

- MCPサーバーURL: `https://mcp.canva.com/mcp`(Canva公式リモートMCP)
- 登録済み: プロジェクトスコープ(`.mcp.json`、Git管理・4台に配布)+ユーザースコープ(このPCの`~/.claude.json`)
- **認証はPCごと・ユーザーごとに必要**。`/mcp` → `canva` → Authenticate → ブラウザでCanvaにログインして許可。
- `.mcp.json`はセッション起動時にしか読まれないため、追加した直後のセッションでは`/mcp`に出てこない。**新しいセッションを開始してから認証する**こと。

## プランごとにできること(公式ドキュメント)

| 機能 | 必要プラン |
|---|---|
| デザインの作成・編集・検索・書き出し・アセットアップロード | 全プラン |
| デザインのリサイズ | Canva Pro以上 |
| **ブランドテンプレのAutofill(テキスト自動差し込み)** | **Enterprise** |

→ Autofillは使えない前提で、**既存デザインをCanva内で検索 → 複製 → テキストを差し替え → PNG書き出し**の流れで作る。

## 運用フロー(認証後)

1. Canva内で既存のコイキーズ用アイキャッチデザインを検索する(「Webinar/Keynote Presentation」ベース)
2. それを複製し、3段のテキスト(上=問いかけ・中央=グループ名/メンバー名・下=説明1〜2行)を記事に合わせて差し替える
3. PNG/JPGで書き出し、`images/`に保存
4. WordPressにメディアアップロードして`featured_media`に設定([blog-uploadスキル](../.claude/skills/blog-upload/SKILL.md))

## フォールバック

Canva MCPが使えない・認証切れのときは`tools/eyecatch_koikeyz.py`(HTML再現版)で作る。見た目はほぼ同じだがフォントだけ別物(M PLUS Rounded 1c Black)。仕様は[docs/eyecatch-style.md](eyecatch-style.md)参照。

## 未確認事項(次にやること)

- 認証後、Canva MCPで**既存デザインの複製+テキスト差し替え**が実際にできるか検証する(できなければ、トモキが使っている日本語フォント名を聞いて、そのフォント指定で新規作成する)
- 検証用の題材: 「デカ猫」記事(chomoand-1.com、記事ID **10569**、下書き)。現在のアイキャッチはHTML再現版(メディアID 10576)なので、Canva版ができたら差し替える。
