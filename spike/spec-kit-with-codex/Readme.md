# github spec-kit を使って仕様駆動型開発を試してみる

## 前提

* codex(OpenAI)
* vscode
* Codex – OpenAI’s coding agent  extension

## 準備

* codexをインストール
```bash
$ brew install codex
```

* spec-kit のプロジェクトを新規作成
```bash
$ mkdir spec-kit-with-codex
$ cd !$
$ specify init . --ai codex --ai-skills
```

## 開発のお試し

### /speckit.constitution で開発原則を決める

* vscode + codex extension の画面を開いて/speckit.constitution を選択し、リターンキーを押す
* そうすると、`./specify/memory/constitution.md` が自動生成される
*  `constitution.md` にTDDなどの原則を追記する
