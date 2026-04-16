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

基本的な流れは、constitution → specify → clarify → plan → tasks → implement

### /speckit.constitution で開発原則を決める

* vscode + codex extension の画面を開いて/speckit.constitution を選択し、リターンキーを押す
* そうすると、`./specify/memory/constitution.md` が自動生成される
*  `constitution.md` にTDDなどの原則を追記する

### /speckit.specify で仕様を決める

* `specs/001-cli-todo-app`が生成され、`specs/001-cli-todo-app/spec.md`, `specs/001-cli-todo-app/checklists/requirements.md`が生成された
* `spec.md`の一部と`requirement.md`が英語だったので、日本語化した

### /speckit.clarify で曖昧な仕様を決める

* 曖昧な仕様を質問形式で聞かれる。それに答えていくと仕様が確定する

### /speckit.git commit でここまでの変更をcommit

### /speckit.plan で計画を立てる

* cli-contract.md, data-model.md, plan.md, quickstart.md, research.mdが生成される
```text
$ tree specs/001-cli-todo-app
specs/001-cli-todo-app
├── checklists
│   └── requirements.md
├── contracts
│   └── cli-contract.md
├── data-model.md
├── plan.md
├── quickstart.md
├── research.md
└── spec.md
```

### 下記を追加した
* テストカバレッジ90%以上を目標にします
* ライブラリのpydantic でデータの検証と型管理したいです
* 型チェックによる安全性を確保したいです
* python は uv を使いたいです

## /speckit.tasks でタスクを作る

* タスクを作成した

## /speckit.implement で実装

* `specs/001-cli-todo-app/tasks.md`に沿って実装が進む。完了した時にチェックが入る
* CLIの実行は `python -m` なしで `uv run todo ...` を使えるようにした
```bash
uv run todo list
uv run todo add --title "牛乳を買う"
```

## ステップ2に進む


## /speckit.Git Feature

* タスクタイトルの編集機能が欲しいとした
* 通常なら、別ブランチが作成されるはずだが、されなかった。
* codexに修正してもらった
* /speckit.Git Feature で002-edit-task-title ブランチが作成された

## /speckit.Specify タスクタイトルの編集機能が欲しいと
