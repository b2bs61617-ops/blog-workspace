# アイキャッチ画像スタイルガイド

## サイト別の使い分け(最初にここを見る)

| サイト | 使うテンプレ |
|---|---|
| **chomoand-1.com(コイキーズブログ)** | **KO1KEYZ統一テンプレ必須**(下記)。既存記事が全部このデザインで揃っているので勝手に変えない |
| **chomoand.com(恋愛リアリティ番組の出演者wiki)** | **Canva MCP必須**(2026-07-16〜)。専用マスターデザイン(design_id: `DAHPjgiBOTI`)を使う。手順は[docs/canva-mcp-chomoand.md](canva-mcp-chomoand.md)参照。以下の「汎用テンプレ」節はCanva MCPが使えないときのフォールバックとして残す |
| chomoand-0.com | 汎用テンプレ(1200×630px、後述) |

## KO1KEYZ統一テンプレ(chomoand-1.com専用)

トモキがCanvaの「Webinar/Keynote Presentation」テンプレで作ってきたアイキャッチと同じ見た目を、`tools/eyecatch_koikeyz.py`(HTML+Playwright)で再現する。マツがコイキーズ記事を書くときは**必ずこれを使う**。

```bash
python tools/eyecatch_koikeyz.py \
  --top "ファンミーティングの会場は?" \
  --main "KO1KEYZ" \
  --bottom "アクセスや会場のキャパを調査!" \
  --out images/ko1keyz_xxx_eyecatch.png
```

- `--bottom`は複数指定で複数行になる。`--seed`で背景の滲みを固定できる(未指定なら毎回ランダム)。
- デザイン仕様: 1200×675px(16:9)/ オフホワイト`#f2efe9`+中央にパステルスモーク(ピンク・オレンジ・ラベンダー・グリーン)/ 極太丸ゴシック(M PLUS Rounded 1c Black、`assets/fonts/`に同梱・OFLライセンス)/ 黒文字・全センター揃え。
- 構成は3段: **上=問いかけや所属 → 中央=主役(グループ名・メンバー名を超大きく) → 下=説明1〜2行**。各行はブラウザ側で横幅いっぱいに自動フィットされる(Canva版の「文字が画面いっぱい」の質感)。
- メンバー個人の記事は`--top "KO1KEYZ" --main "YUKI"`のように、上段にグループ名・中央に個人名を置くのが既存記事の型。

## 汎用テンプレ(chomoand-0.com / chomoand.comのフォールバック用)

サイズ: 1200×630px(OGP/WordPress標準)。人物名を超大きく中央に、グラデーションblobの背景、色はランダムで毎回変える。

### 作り方(2通り)

1. **HTMLテンプレート方式(推奨・人物系記事)**: 下記テンプレートで人物名を大きく配置したHTMLを作成し、ブラウザで開いてスクリーンショット→PNG化する。保存先は `ブログ作業場/[人物名]/アイキャッチ_[記事番号].html`。
2. **PowerShell(System.Drawing)方式**: `System.Drawing`で直接1200×630pxのPNGを生成する。フォントは`Meiryo`または`Yu Gothic`(日本語対応)。保存先は`images/`配下。

### デザイン仕様(HTMLテンプレート方式)

### レイアウト(上から順)
1. 番組名・所属(中サイズ・太字) 例:「AKB48 19期生」
2. 人物名(超大きく・最も目立つ・110px前後) 例:「花田 藍衣」
3. 記事トピック(中大サイズ・太字・2行程度) 例:「学歴は?捜真女学校出身!」

### 背景スタイル
- ベース: オフホワイト/クリーム(`#f5f0eb`など)
- 装飾: ソフトなグラデーションblobを複数配置(`filter: blur(40〜60px)`で滲ませる)
- テキスト色: ダーク(`#1a1a1a`〜`#2d2d2d`)
- **色はランダムで毎回変える**(パステル系・柔らかいトーン)

### 実装テンプレート

```html
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 1200px; height: 630px; overflow: hidden;
  font-family: 'Yu Gothic', 'Meiryo', 'Hiragino Kaku Gothic ProN', sans-serif; }
.container {
  width: 1200px; height: 630px;
  background: #f5f0eb;
  position: relative;
  display: flex; flex-direction: column;
  justify-content: center; align-items: center; gap: 20px;
  overflow: hidden;
}
.blob1 {
  position: absolute; width: 700px; height: 700px; border-radius: 50%;
  background: radial-gradient(circle, [COLOR1] 0%, [COLOR2] 40%, transparent 70%);
  opacity: 0.55; right: -150px; top: -150px; filter: blur(55px);
}
.blob2 {
  position: absolute; width: 400px; height: 400px; border-radius: 50%;
  background: radial-gradient(circle, [COLOR3] 0%, transparent 70%);
  opacity: 0.4; left: -80px; bottom: -80px; filter: blur(40px);
}
.top-text { font-size: 36px; font-weight: 700; color: #2d2d2d; letter-spacing: 0.1em; z-index: 1; }
.name { font-size: 110px; font-weight: 900; color: #1a1a1a; letter-spacing: 0.08em; z-index: 1; text-align: center; line-height: 1.1; }
.bottom-text { font-size: 38px; font-weight: 700; color: #2d2d2d; letter-spacing: 0.05em; z-index: 1; text-align: center; line-height: 1.6; }
</style>
</head>
<body>
<div class="container">
  <div class="blob1"></div>
  <div class="blob2"></div>
  <div class="top-text">[所属・番組名]</div>
  <div class="name">[人物名]</div>
  <div class="bottom-text">[記事トピック1行目]<br>[記事トピック2行目]</div>
</div>
</body>
</html>
```

### 色パターン例(毎回変える)
- 紫×青: `rgba(179,157,219,0.7)` + `rgba(144,202,249,0.6)`
- オレンジ×珊瑚: `rgba(255,183,77,0.7)` + `rgba(239,154,154,0.6)`
- 緑×ティール: `rgba(165,214,167,0.7)` + `rgba(128,203,196,0.6)`
- 赤×ピンク: `rgba(239,154,154,0.7)` + `rgba(206,147,216,0.6)`
- 黄×ライム: `rgba(255,238,88,0.7)` + `rgba(197,225,165,0.6)`
- ピーチ×ラベンダー: `rgba(255,204,188,0.7)` + `rgba(179,157,219,0.6)`

### 別バリエーション(ハート装飾つき)

一部の記事では以下の構成も使う: 背景はピンク〜ラベンダーの線形グラデーション、白い二重枠線、四隅に薄いハート(♥)装飾、上部タグライン、メインタイトルを2行に分割して中央配置(影付き・濃いピンク)、ピンク帯の中にサブコピー、下部にサイト名。フォントは`Yu Gothic`。

## WordPressへの反映

1. 画像をバイナリで読み込み、`POST {サイトURL}/wp-json/wp/v2/media`にアップロード(`Content-Type: image/png`)
2. 取得したメディアIDを記事に設定: `POST {サイトURL}/wp-json/wp/v2/posts/{記事ID}` ボディ `{ "featured_media": メディアID }`

詳細な自動化手順は[blog-uploadスキル](../.claude/skills/blog-upload/SKILL.md)を参照。
