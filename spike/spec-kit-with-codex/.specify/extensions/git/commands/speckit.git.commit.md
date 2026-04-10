---
description: "Spec Kit コマンド完了後に変更を自動コミットする"
---

# 変更の自動コミット

Spec Kit コマンド完了後に、変更を自動でステージしてコミットします。

## Behavior

このコマンドはコアコマンドの前後フックとして呼び出され、次を行います:

1. フック文脈からイベント名を判定（例: `after_specify`, `before_plan`）
2. `.specify/extensions/git/git-config.yml` の `auto_commit` セクションを確認
3. イベント固有キーで自動コミット有効化を確認
4. イベント設定がない場合は `auto_commit.default` にフォールバック
5. 設定された `message` があれば使用、なければ既定メッセージを使用
6. 有効かつ未コミット変更がある場合、`git add .` と `git commit` を実行

## Execution

このコマンドを起動したフックのイベント名を判定し、スクリプトを実行します:

- **Bash**: `.specify/extensions/git/scripts/bash/auto-commit.sh <event_name>`
- **PowerShell**: `.specify/extensions/git/scripts/powershell/auto-commit.ps1 <event_name>`

`<event_name>` には実際のイベント（`after_specify`, `before_plan`, `after_implement` など）を設定します。

## Configuration

`.specify/extensions/git/git-config.yml`:

```yaml
auto_commit:
  default: false          # 全体トグル。すべてのコマンドで有効化するなら true
  after_specify:
    enabled: true         # コマンド単位の上書き
    message: "[Spec Kit] Add specification"
  after_plan:
    enabled: false
    message: "[Spec Kit] Add implementation plan"
```

## Graceful Degradation

- Git が利用できない、またはリポジトリでない: 警告してスキップ
- 設定ファイルがない: スキップ（既定で無効）
- コミット対象の変更がない: メッセージを出してスキップ
