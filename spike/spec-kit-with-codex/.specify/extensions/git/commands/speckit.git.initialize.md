---
description: "初回コミット付きで Git リポジトリを初期化する"
---

# Git リポジトリ初期化

現在のプロジェクトディレクトリに Git リポジトリが存在しない場合、初期化します。

## Execution

プロジェクトルートから適切なスクリプトを実行します:

- **Bash**: `.specify/extensions/git/scripts/bash/initialize-repo.sh`
- **PowerShell**: `.specify/extensions/git/scripts/powershell/initialize-repo.ps1`

拡張スクリプトが見つからない場合のフォールバック:
- **Bash**: `git init && git add . && git commit -m "Initial commit from Specify template"`
- **PowerShell**: `git init; git add .; git commit -m "Initial commit from Specify template"`

スクリプト内で次を処理します:
- Git が利用できない場合はスキップ
- 既に Git リポジトリ内ならスキップ
- `git init`、`git add .`、`git commit` を初期コミットメッセージ付きで実行

## Customization

必要に応じてスクリプトを差し替え、プロジェクト固有の初期化を追加できます:
- カスタム `.gitignore` テンプレート
- デフォルトブランチ名 (`git config init.defaultBranch`)
- Git LFS セットアップ
- Git フックの導入
- コミット署名設定
- Git Flow 初期化

## Output

成功時:
- `✓ Git repository initialized`

## Graceful Degradation

Git が未インストールの場合:
- ユーザーへ警告
- リポジトリ初期化をスキップ
- Git なしでもプロジェクトは継続可能（`specs/` 配下の作成は可能）

Git はあるが `git init` / `git add .` / `git commit` が失敗した場合:
- エラーをユーザーに提示
- 中途半端な状態で継続せず、このコマンドを停止
