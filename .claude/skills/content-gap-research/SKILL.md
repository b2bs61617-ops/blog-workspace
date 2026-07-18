---
name: content-gap-research
description: 競合サイトが既に書いている記事の中から「内容が薄い」ものを探し、chomoandがより詳しく書き直せば上位表示を狙えるトピックを見つけるときに使う。恋愛リアリティ番組の出演者ネタで、大量のページ読み込みが必要なためAgentサブエージェントに調査を委任してトークンを節約する。
---

# コンテンツギャップ調査スキル

競合(恋愛ふりーくす=fstopics.com、定番ナビ=teiban-navi.com、はぴにゃんブログ=hapinyan.com。詳細は[docs/koi-real-competitor-analysis.md](../../../docs/koi-real-competitor-analysis.md))が既に書いた話題をそのまま書いてもSEO的価値は無い。しかし競合記事の中には「一応書いてあるが薄い」ものが多数ある(文字数が少ない・SNSリンクが無い・学歴や家族構成が「不明」で終わっている等)。ここを狙えば後発でも上位表示を取れる。

## なぜサブエージェントに委任するか

この調査は「出演者1人ずつ×3サイトの記事を読んで薄さを判定する」という物量作業で、メインセッションで直接やるとページ本文の読み込みだけで大量にトークンを消費する。**Agentツールでgeneral-purposeサブエージェントを起動し、調査対象を渡して、返信は「機会サイズが大きい上位N件と理由」だけに絞って報告させる。** 詳細(記事本文の引用・比較表)はサブエージェントに`docs/research-notes/`配下のファイルへ直接保存させ、メインセッションには持ち帰らせない。

## 調査対象の探し方(競合記事検索)

各競合サイトはWordPress REST APIの検索が使える。人名やキーワードで直接ヒットする記事を引ける。

```
https://fstopics.com/wp-json/wp/v2/posts?search={キーワード}&_fields=id,title,link,date,content
https://teiban-navi.com/wp-json/wp/v2/posts?search={キーワード}&_fields=id,title,link,date,content
https://hapinyan.com/wp-json/wp/v2/posts?search={キーワード}&_fields=id,title,link,date,content
```

全件を俯瞰したい場合は`/wp-json/wp/v2/posts?per_page=100&page=N`でページングして全記事のタイトル・カテゴリを取得する方法もある(既存の競合分析で使用済み。件数が多いサイトは`per_page=100`で数十ページになるためサブエージェント任せにする)。

## 薄さの判定基準

記事を「薄い」と判定する目安(1つでも当てはまれば機会あり):

- 文字数が明らかに少ない(chomoandの最低基準2,500字を大きく下回る)
- SNS(インスタ・TikTok・X)へのリンクや言及が無い
- 高校・学歴について「不明」「非公開」で終わっている
- 家族構成・恋愛経験・現在の活動について触れていない
- 3サイトの中でそもそも1サイトも記事が無い(=完全な空白。最も価値が高い)

## サブエージェントへの依頼テンプレート

Agentツール(`subagent_type: general-purpose`, `run_in_background: true`)で以下の要領で依頼する。

1. 対象の番組・出演者リストを明示する(番組名・シーズン名・出演者名が分かっていれば渡す。分かっていなければ先にWebSearchで確定させる指示を含める)
2. 上記のWP REST API検索の使い方と、薄さの判定基準を渡す
3. 出力は`docs/research-notes/content-gap-{番組名スラッグ}.md`に保存させる(**gitのcommit/pushはサブエージェントにさせず、人間側で確認してからまとめてコミットする**)
4. メインセッションへの返信は300語程度に絞らせる(機会サイズ大の上位5〜10件+理由のみ)

## 関連

- 競合サイトの全体像・記事タイプ・タイトルフォーミュラ: [docs/koi-real-competitor-analysis.md](../../../docs/koi-real-competitor-analysis.md)
- 記事の書き方・プライバシーの線引き: [koi-real](../koi-real/SKILL.md)
