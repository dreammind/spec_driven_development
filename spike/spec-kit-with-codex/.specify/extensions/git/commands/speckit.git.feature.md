---
description: "連番またはタイムスタンプ形式で機能ブランチを作成する"
---

# 機能ブランチ作成

指定された仕様に対して新しい Git 機能ブランチを作成し、切り替えます。
このコマンドは **ブランチ作成のみ** を扱います。spec ディレクトリとファイルは
コアの `/speckit.specify` ワークフローで作成されます。

## User Input

```text
$ARGUMENTS
```

入力が空でない場合、処理前に **必ず** 反映してください。

## Environment Variable Override

ユーザーが `GIT_BRANCH_NAME` を明示指定した場合（環境変数・引数・要求文）、
スクリプト実行前に `GIT_BRANCH_NAME` 環境変数として渡してください。
`GIT_BRANCH_NAME` が設定されている場合:
- その値をブランチ名としてそのまま使用（prefix/suffix 自動生成は無効）
- `--short-name` / `--number` / `--timestamp` は無視
- 先頭が数値プレフィックスなら `FEATURE_NUM` に抽出し、そうでなければブランチ名全体を `FEATURE_NUM` に設定

## Prerequisites

- `git rev-parse --is-inside-work-tree 2>/dev/null` で Git 利用可否を確認
- Git が利用できない場合は警告してブランチ作成をスキップ

## Branch Numbering Mode

次の順で設定を確認し、採番戦略を決定します:

1. `.specify/extensions/git/git-config.yml` の `branch_numbering`
2. `.specify/init-options.json` の `branch_numbering`（後方互換）
3. どちらも無ければ `sequential` を既定値とする

## Execution

ブランチ短縮名（2〜4語）を簡潔に生成:
- 機能説明を解析し、意味のあるキーワードを抽出
- 可能なら動詞-名詞形式（例: `add-user-auth`, `fix-payment-bug`）
- 技術用語や略語（OAuth2, API, JWT など）を保持

プラットフォームに応じて適切なスクリプトを実行:

- **Bash**: `.specify/extensions/git/scripts/bash/create-new-feature.sh --json --short-name "<short-name>" "<feature description>"`
- **Bash (timestamp)**: `.specify/extensions/git/scripts/bash/create-new-feature.sh --json --timestamp --short-name "<short-name>" "<feature description>"`
- **PowerShell**: `.specify/extensions/git/scripts/powershell/create-new-feature.ps1 -Json -ShortName "<short-name>" "<feature description>"`
- **PowerShell (timestamp)**: `.specify/extensions/git/scripts/powershell/create-new-feature.ps1 -Json -Timestamp -ShortName "<short-name>" "<feature description>"`

**IMPORTANT**:
- `--number` は渡さない（次番号はスクリプトが自動決定）
- JSON フラグは必須（Bash は `--json`、PowerShell は `-Json`）
- 1機能につきこのスクリプト実行は1回のみ
- JSON 出力には `BRANCH_NAME` と `FEATURE_NUM` が含まれる

## Graceful Degradation

Git 未インストール、または現在ディレクトリが Git リポジトリでない場合:
- 警告付きでブランチ作成をスキップ: `[specify] Warning: Git repository not detected; skipped branch creation`
- それでも呼び出し側が参照できるよう `BRANCH_NAME` と `FEATURE_NUM` は出力

## Output

スクリプトは次を含む JSON を出力:
- `BRANCH_NAME`: ブランチ名（例: `003-user-auth` または `20260319-143022-user-auth`）
- `FEATURE_NUM`: 使用された数値またはタイムスタンプのプレフィックス
