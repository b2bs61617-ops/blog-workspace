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

## リポジトリ本体が原因不明で消失→GitHubから復元(2026-07-19、このPC)

作業中、`ブログ作業場`フォルダの中身が`docs`配下の1ファイルを除いて全て消える事故が発生した(`.git`・`.claude`・`articles`・`images`・`tools`・`CLAUDE.md`等が消失)。マツ自身はこのセッションで削除系コマンドを実行しておらず、原因は特定できていない。ごみ箱にも該当ファイルは無かった(`Remove-Item`等はごみ箱を経由しないため)。

**復元手順:**
1. `gh repo clone b2bs61617-ops/blog-workspace` で別フォルダに最新コミットをクローン→中身を確認
2. GitHubの最新コミットが事故直前に確認していたHEADと完全一致していたため、コミット済みの内容はロス無しと判断
3. 消える前に新規作成していた1ファイル(未コミット)をクローン側にコピーしてから、空になった元フォルダを`ブログ作業場_空フォルダ退避_20260719`にリネームして退避し、クローンを`ブログ作業場`にリネームして本来の場所に復帰
4. `.gitignore`対象の`.env`・`google-indexing-key.json`はGit履歴に無いため復元できなかったが、`Desktop\AI作業場\ブログ作業場\`に古い完全バックアップ(2026-07-19朝時点)が残っており、そこからコピーして復旧

**Why:** 原因不明のまま作業を続けている状態。同じ事故が再発する可能性があるため、今後同様の消失に気づいたら、まず`Desktop\AI作業場\ブログ作業場\`にバックアップが無いか確認し、無ければGitHub(`b2bs61617-ops/blog-workspace`)からクローンして復元するとよい。`.env`等の秘密情報はGit管理外なので、`AI作業場`側のバックアップか他PC・パスワードマネージャーからの再取得が必要になる。

## Netflix『ラヴ上等 シーズン2』出演者11人wiki記事44本を一括作成・投稿(2026-07-19)

配信開始(2026-08-04)前の出演者発表を受けて、koi-realスキルの通常方針を拡張した対応を行った。

- **調査**: 出演者11人(Kii-chan/Tsu-chan/Baby/Amo/Milk/Otosan/Nisei/Tenten/Tekarin/Tackle/Yanbo)をAgentサブエージェント3グループに分けて調査。結果は[docs/research-notes/love-joto-season2-cast-research.md](research-notes/love-joto-season2-cast-research.md)。
- **プライバシー方針の一時拡張(トモキ承認済み)**: koi-realスキルの「書いてよい情報源」は本来、番組内発言・本人公開SNS・公式発表の3つに限定しているが、本作は出演者が成人(未成年ではない)の「元不良」設定のため、トモキの指示で**第三者ブログ・SNSの噂・憶測も出典を明記した上で記事に含める**方針に拡張した。「トモキが自分で最終確認する」ことが前提。犯罪歴も同様の扱い。今日好き等の未成年出演者にはこの拡張を適用しないこと。
- **記事構成**: 1人につき「wiki/プロフィール」「職業・年収」「学歴」「犯罪歴」の4記事、11人×4=44記事(ファイル名`articles/lovejoto_{name}_{wiki|shokugyo_nenshu|gakureki|hanzaireki}.html`)。犯罪歴が報道・本人告白で確認できたのはTsu-chan(少年院送致)とYanbo(大麻取締法違反)のみで、他は「情報なし」または本人告白ベースと明記。
- **投稿**: chomoand.comに新規カテゴリ「ラヴ上等」(ID 36)を作成し、`wp_upload_lovejoto.py`(リポジトリ直下、`wp_upload_batch.py`の作り方を流用)で44件を下書き一括投稿(記事ID 11642〜11685)。**アイキャッチ画像は未設定のまま**(Canva MCPがこのセッションで未認証だったため)。次にこの続きをやる際は、Canva MCP認証後に[docs/canva-mcp-chomoand.md](canva-mcp-chomoand.md)の手順でアイキャッチを追加する。
- **タイトル修正(2026-07-20)**: トモキの指示でタイトルの「(シーズン2)」を削除し、先頭を「ラヴ上等」→「ラヴ上等2」に変更(`wp_retitle_lovejoto.py`、44件更新)。
- **アイキャッチ・公開(2026-07-20)**: chomoand.comの現行ルール通り(Canva MCPではなく)`tools/eyecatch_chomoand.py`で44枚を生成([docs/eyecatch-style.md](eyecatch-style.md)の「chomoand.com統一テンプレ」)。11人ごとにhueを33度ずつずらして色被りを回避(`wp_eyecatch_lovejoto.py`、メディアID 11731〜11774、featured_media設定まで自動化)。続けて`wp_publish_lovejoto.py`で44件を`publish`に変更しGoogle Indexing APIにも送信、全件公開完了。
- **タイトル形式の再修正(2026-07-22)**: 上記「タイトル修正(2026-07-20)」が実際には反映されておらず、公開後も先頭が`ラヴ上等｜`/`ラヴ上等 `(括弧なし)、末尾が`(シーズン1)`のままだったことが判明(原因不明。`wp_retitle_lovejoto.py`が別IDに対して実行された可能性がある)。トモキの指示で「chomoand.comは恋リア特化サイトなので番組名を必ずタイトル先頭に`【番組名】`で入れる」ルールを明確化し、44件全てを`【ラヴ上等2】{属性文言}`形式(`(シーズン1)`表記は削除、シーズン自体はこの回で合っている)に一括更新した。ルールは[koi-realスキルのタイトルの型](../.claude/skills/koi-real/SKILL.md)に反映済み(既存の個別記事タイトル例も括弧なし表記だったため合わせて修正)。
- **実は未反映だった重複記事18件の発見・整理(2026-07-27)**: 「10記事書いても順位が付かない」という相談を受けてchomoand.comの恋リアカテゴリ(ID 34/35/36)91件を全件調査したところ、上記07-22の修正は**るる・尾田優也の8件にしか反映されておらず**、残りは未反映のまま放置されていたと判明。加えて、`wp_retitle_lovejoto.py`が意図せず**新規重複投稿を作っていた**ことも判明: きぃちゃん・つーちゃん・Baby・あも・Milkの5人分(wiki/学歴/職業/逮捕歴の4記事×5人=18記事、ID 11624〜11641、`(シーズン2)`サフィックス付き)が、本来の44件(ID 11642〜11685)とほぼ同一内容(冒頭の配信日表記が違うだけ)のまま別記事として`publish`状態で生き続けていた。
  - **対応**: 重複18件(ID 11624〜11641)を`draft`に戻す(削除はしない)。本来の44件+あっすん・緋咲一馬の6件、計50件のタイトル先頭を`【ラヴ上等】`→`【ラヴ上等2】`に一括修正。
  - **Why**: 同一人物についてほぼ同一内容の記事が2つ`publish`で存在する状態はGoogleの重複コンテンツ判定を招き、公開後もインデックスされない主因の一つと推測される(`site:chomoand.com`で見ても新ジャンルの記事がほぼインデックスされていなかった)。
  - **How to apply**: 一括投稿・一括リタイトルスクリプトを走らせた後は、必ずWordPress REST APIで実際のタイトル・件数を再取得して「意図した通りに反映されたか」を確認すること。ログに「◯件更新しました」と出力されても、実際にAPI側で反映されているかは別問題(今回は本人もこのズレに5日間気づかなかった)。
