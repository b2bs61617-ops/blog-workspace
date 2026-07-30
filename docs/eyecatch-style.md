# アイキャッチ画像スタイルガイド

## サイト別の使い分け(最初にここを見る)

| サイト | 使うテンプレ |
|---|---|
| **chomoand-1.com(コイキーズブログ)** | **KO1KEYZ統一テンプレ必須**(下記)。既存記事が全部このデザインで揃っているので勝手に変えない |
| **chomoand.com(恋愛リアリティ番組の出演者記事)** | **`tools/eyecatch_chomoand.py`必須**(2026-07-19〜)。詳細は下記「chomoand.com統一テンプレ」参照。Canva MCP版(design_id: `DAHPjgiBOTI`、[docs/canva-mcp-chomoand.md](canva-mcp-chomoand.md))は2026-07-19に運用停止(経緯は同docs参照) |
| chomoand.com(恋リア以外の旧カテゴリ記事) | 対象外。第2次転換([docs/chomoand-pivot.md](chomoand-pivot.md))で凍結済みの旧記事(トレンド系・未分類など)はそのまま放置。新デザインを適用するのは恋リア記事のみ |
| chomoand-0.com | 汎用テンプレ(1200×630px、後述) |

## chomoand.com統一テンプレ(恋愛リアリティ番組の出演者記事専用)

ピンク×カップルシルエット×白いハート/ライン装飾のイラスト背景に、KO1KEYZと同じ「3段・横幅いっぱいに自動フィット」の黒太文字を重ねる。`tools/eyecatch_chomoand.py`(HTML+Playwright)で生成する。

```bash
python tools/eyecatch_chomoand.py \
  --top "wiki、プロフィール、出身" \
  --top "高校・子役時代など重要な内容" \
  --main "福住真里" \
  --bottom "出身地・高校を調査" \
  --bottom "子役時代の経歴も解説!" \
  --hue 140 \
  --out images/fukuzumi_mari_wiki_eyecatch_chomoand.png
```

- `--top`/`--bottom`は複数指定で複数行になる。
- **背景色は`--hue`(0〜359の色相回転)で毎回変える**。未指定ならランダム。同じ特集記事内の複数記事(例: 1シーズンの出演者複数人)は色がかぶらないように手動で離れた値を選ぶ(例: 0/140/280のように120度ずつ離す)。
- 構成は3段: **上=記事の属性キーワード(wiki・プロフィール・学歴など、タイトルから該当するものを2行程度) → 中央=主役(出演者名、または特集記事なら「メンバー一覧」等のテーマ) → 下=タイトルの具体的な内容(2行程度)**。
- サイズは1200×675px(16:9、既存chomoand.comアイキャッチと同じ比率)。
- 背景に写っているのはAI生成のイラスト(実写ではない)なので、出演者本人の顔写真を使うリスク(肖像権・未成年のプライバシー)を回避できる。**出演者の実写・SNS画像を背景に使うのは禁止**(2026-07-18〜19の検討で不採用と判断)。
- **背景画像は記事ごとにPollinations.ai(APIキー不要・無料の画像生成API)で毎回新規生成する**(2026-07-30〜)。カップルシルエットが右側・左側は文字用に空けるプロンプトで固定し、ポーズや装飾の細部だけ毎回変わる。生成失敗時(タイムアウト等)は静的背景(`assets/chomoand_eyecatch_bg.png`)に自動フォールバックするため、ネット不通でも記事生成は止まらない。`--no-ai-bg`で静的背景に固定できる(検証用)。色相の変化は引き続きCSSの`hue-rotate`で行う(生成画像・静的背景どちらにも同じ仕組みが乗る)。
- 検討の経緯: 最初はMidjourney連携を検討したが公式APIが無くTOS的にグレーなため不採用。次にGemini(Nano Banana、`gemini-2.5-flash-image`)で静的背景を参照画像にした編集生成を試したが、画像生成モデルは無料枠が0で課金必須と判明し断念。無課金で使えるPollinations.aiに切り替えた。

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
