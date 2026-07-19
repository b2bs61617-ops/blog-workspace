# 運用上の経緯・インシデント記録

CLAUDE.mdは「今どう動くべきか」だけを載せる方針にしているため、過去の経緯や個別インシデントの詳しい記録はここに集約する。

## 複数セッション同時実行時のコミット混入(2026-07-09)

複数セッションが同時に動いていると、`git add`直後に別セッションの`commit`が割り込み、無関係な変更同士が1つのコミットに混ざることがあると判明した。

**現在のルール(CLAUDE.mdにも記載):** `git add`の後は`git commit`前に必ず`git status`で意図したファイルだけがステージされているか確認する。見覚えのない変更が混ざっていたら一旦止めてユーザーに報告する。すでにコミットされてしまっていても、中身が両方とも正当な変更なら実害はないことが多いので、無理に`reset`で分離しようとせず状況を説明するだけでよい。

## chomoand.comの方針転換

詳細は[docs/chomoand-pivot.md](chomoand-pivot.md)を参照(第1次転換の検討→撤回→第2次転換=恋リアwiki特化、の経緯)。

## ツールの導入・廃止の経緯

各ツールの導入時期・現在使われていないツールの背景は[docs/tools.md](tools.md)を参照(YouTube急上昇取得・Xトレンド監視など)。

## 恋愛リアリティ競合調査→koi-realスキル強化→記事7本公開(2026-07-19)

一晩の作業でchomoand.comの恋リアコンテンツ戦略を一通り更新した。流れ:

1. **競合3サイト調査**: 恋愛ふりーくす(fstopics.com)・定番ナビ(teiban-navi.com)・はぴにゃんブログ(hapinyan.com)の全記事タイトルをWordPress REST APIで取得・分析。結果は[docs/koi-real-competitor-analysis.md](koi-real-competitor-analysis.md)。
2. **koi-realスキル更新**: 分析結果から対象番組表に「シャッフルアイランド」を追加(2026-07時点で3サイト共通の最新ホット番組と判明)、タイトルのフォーミュラを競合分析ベースに刷新。
3. **content-gap-researchスキルを新設**: 競合記事が薄い/存在しないトピックをAgentサブエージェントに委任して探す手法を[.claude/skills/content-gap-research/SKILL.md](../.claude/skills/content-gap-research/SKILL.md)に記録。
4. **未放送番組調査**: [docs/research-notes/upcoming-love-reality-2026-07.md](research-notes/upcoming-love-reality-2026-07.md)。今日好き夏休み編2026(新規4人)は実は前日07-18のセッションで既に執筆・投稿済みだったことが判明(くうが・けいは公開済み、みのり・まり・一覧は下書き)。
5. **コンテンツギャップ調査**: シャッフルアイランド7・今日好きインチョン編の出演者24名を競合カバー状況で調査、機会サイズ「大」の7名を特定。[docs/research-notes/content-gap-shuffleisland7-kyousuki-inchon.md](research-notes/content-gap-shuffleisland7-kyousuki-inchon.md)。
6. **記事7本を執筆・公開**: 上記7名(そら・たまき・あんじゅ・ゆうとく・とおる・はるな・きよ)をAgentサブエージェントで並行執筆(既存記事`oshima_kuga_wiki.html`を型として、koi-realのプライバシー線引きを厳守)。WordPress下書き投稿・アイキャッチ生成(`tools/eyecatch_chomoand.py`)・「シャッフルアイランド」カテゴリ新設(ID 35)まで実施し、最終的に全記事公開。記事ID: 11603・11606・11609・11612・11615・11618・11621。
7. **記事の完了報告ルール**: 記事完成時はタイトル・想定検索キーワード・記事構成(見出し一覧)をチャットで報告する運用に(ファイルへの埋め込みは不要、[docs/rules.md](rules.md)参照)。

## Google Indexing APIのセットアップ完了(2026-07-19)

[docs/google-indexing-setup.md](google-indexing-setup.md)の手順に沿って本PCで初めて完了させた。

- 過去に`chomoand-466@model-gearing-465707-d6.iam.gserviceaccount.com`というサービスアカウントを3サイトのSearch Consoleオーナーとして登録済みだったが、対応するJSON鍵ファイルがどのPCにも残っていなかった(紛失)。
- 鍵を再発行する代わりに、新しいサービスアカウント`chomoand-477@model-gearing-465707-d6.iam.gserviceaccount.com`を作成し、そちらを3サイト(chomoand.com/chomoand-0.com/chomoand-1.com)のSearch Consoleオーナーとして追加登録した(466は残したまま、実害無し)。
- 鍵ファイルは`ブログ作業場/google-indexing-key.json`に保存(Git管理外。`.gitignore`にパターンを追加して誤コミットを防止済み)。`.env`に`GOOGLE_INDEXING_CREDENTIALS_PATH`を追記して動作確認済み。
- **Why:** 新しいPCでこの機能を使うときは、466の鍵を探すのではなく、477用の鍵ファイルを該当PCにコピーするか、そのPC用に新しいサービスアカウントを作ってSearch Consoleに追加するのが早い。
