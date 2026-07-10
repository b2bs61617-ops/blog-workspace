---
name: codex-writing
description: 記事や文書を作成するときに使う。OpenAI Codex(デスクトップアプリ/CLI)を使って生成する。
---

# Codex記事・文書作成スキル

記事・文書作成にはCodexを使用する。

## 実行ファイルの探し方

インストール場所: `%LOCALAPPDATA%\OpenAI\Codex\`

実行ファイルはバージョンごとにハッシュ付きサブフォルダに入っている(例: `%LOCALAPPDATA%\OpenAI\Codex\bin\<ハッシュ>\codex.exe`)ため、**PCによってパスが異なる**。使う前に以下で実際のパスを確認する:

```powershell
Get-ChildItem "$env:LOCALAPPDATA\OpenAI\Codex\bin" -Filter codex.exe -Recurse | Select-Object -First 1 -ExpandProperty FullName
```

PATHが通っていれば `codex` コマンドだけでも呼び出せる場合がある(`where codex` で確認)。

## 主なCLIコマンド

- `codex exec "プロンプト"` — 非インタラクティブで実行(自動化向き)
- `codex "プロンプト"` — インタラクティブセッション開始
- `codex --search exec "プロンプト"` — Web検索を有効にして実行

## How to apply

ブログ記事・文書の作成時は、上記コマンドを`codex exec`で非インタラクティブに呼び出すのが自動化に向いている。文体ルール(句点で改行など)は[docs/rules.md](../../../docs/rules.md)、記事テンプレートは[wiki-article](../wiki-article/SKILL.md)・[gakureki-kazoku-kanojo](../gakureki-kazoku-kanojo/SKILL.md)を指示に含める。

## Codexが未インストールのPCの場合(2026-07-07判明)

`Get-ChildItem "$env:LOCALAPPDATA\OpenAI\Codex\bin"`が存在しない(パスが無い)PCもある。複数PC共有のリポジトリのため、PCによってCodexの有無が異なりうる。未インストールの場合はエラーで止まらず、マツ(Claude)が直接HTML本文を執筆するフォールバックに切り替えて作業を続ける。
