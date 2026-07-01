# AGENTS.md

このファイルはCodexがこのリポジトリで作業する際のガイドです。
複数のPC・複数人でこのリポジトリを共有しています。ここに書かれた内容は全員・全PC共通のルールです。
詳細な方針はすべて [CLAUDE.md](CLAUDE.md) と同じなので、そちらを正としてください。ここでは要点のみ記載します。

## プロジェクト概要

トレンドブログの作業場です。人物・話題の記事を調査・執筆し、WordPressに投稿します。
運営サイトは3つ(chomoand.com / chomoand-0.com / chomoand-1.com)。詳細は [docs/wordpress.md](docs/wordpress.md)。

## 作業方針

- 返答は常に日本語で行う
- 記事はトレンド(時事・流行)に関するテーマを扱う
- 読者にとって分かりやすく、検索されやすい文章を意識する
- 記事作成の詳細ルール: [docs/rules.md](docs/rules.md)
- 記事テンプレート: [.claude/skills/wiki-article/SKILL.md](.claude/skills/wiki-article/SKILL.md)、[.claude/skills/gakureki-kazoku-kanojo/SKILL.md](.claude/skills/gakureki-kazoku-kanojo/SKILL.md)
- WordPress記事の削除・ゴミ箱移動は絶対に行わない

## 秘密情報

WordPressのアプリパスワード等は`.env`にローカル保存(Gitには含めない)。テンプレートは`.env.example`参照。

## 運用ルール(複数PC共有)

- 作業前に`git pull`、更新後は内容をCLAUDE.md/docs/skillsに反映して`git commit`(pushはユーザー確認後)。
