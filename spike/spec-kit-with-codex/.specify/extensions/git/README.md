# Git ブランチ運用拡張

Spec Kit 向けに、Git リポジトリ初期化、機能ブランチ作成、採番（連番/タイムスタンプ）、
検証、リモート検出、自動コミットを提供します。

## Overview

この拡張は、任意で利用できる自己完結モジュールとして Git 操作を提供します。
主な機能:

- 設定可能なコミットメッセージによる **リポジトリ初期化**
- 連番 (`001-feature-name`) / タイムスタンプ (`20260319-143022-feature-name`) の **機能ブランチ作成**
- 命名規則順守を確認する **ブランチ検証**
- GitHub 連携（Issue 作成など）向け **Git リモート検出**
- コアコマンド後の **自動コミット**（コマンド単位で有効化/メッセージ設定可能）

## Commands

| Command | Description |
|---------|-------------|
| `speckit.git.initialize` | 設定可能なコミットメッセージで Git リポジトリを初期化 |
| `speckit.git.feature` | 連番またはタイムスタンプで機能ブランチを作成 |
| `speckit.git.validate` | 現在ブランチが機能ブランチ命名規約に従うか検証 |
| `speckit.git.remote` | GitHub 連携のため Git リモート URL を検出 |
| `speckit.git.commit` | 変更を自動コミット（コマンド単位で有効/無効とメッセージ設定可） |

## Hooks

| Event | Command | Optional | Description |
|-------|---------|----------|-------------|
| `before_constitution` | `speckit.git.initialize` | No | 憲章作成前に git リポジトリを初期化 |
| `before_specify` | `speckit.git.feature` | No | 仕様作成前に機能ブランチを作成 |
| `before_clarify` | `speckit.git.commit` | Yes | 明確化前に未コミット変更をコミット |
| `before_plan` | `speckit.git.commit` | Yes | 計画前に未コミット変更をコミット |
| `before_tasks` | `speckit.git.commit` | Yes | タスク生成前に未コミット変更をコミット |
| `before_implement` | `speckit.git.commit` | Yes | 実装前に未コミット変更をコミット |
| `before_checklist` | `speckit.git.commit` | Yes | チェックリスト前に未コミット変更をコミット |
| `before_analyze` | `speckit.git.commit` | Yes | 分析前に未コミット変更をコミット |
| `before_taskstoissues` | `speckit.git.commit` | Yes | Issue 同期前に未コミット変更をコミット |
| `after_constitution` | `speckit.git.commit` | Yes | 憲章更新後に自動コミット |
| `after_specify` | `speckit.git.commit` | Yes | 仕様作成後に自動コミット |
| `after_clarify` | `speckit.git.commit` | Yes | 明確化後に自動コミット |
| `after_plan` | `speckit.git.commit` | Yes | 計画後に自動コミット |
| `after_tasks` | `speckit.git.commit` | Yes | タスク生成後に自動コミット |
| `after_implement` | `speckit.git.commit` | Yes | 実装後に自動コミット |
| `after_checklist` | `speckit.git.commit` | Yes | チェックリスト後に自動コミット |
| `after_analyze` | `speckit.git.commit` | Yes | 分析後に自動コミット |
| `after_taskstoissues` | `speckit.git.commit` | Yes | Issue 同期後に自動コミット |

## Configuration

設定は `.specify/extensions/git/git-config.yml` に保存されます:

```yaml
# ブランチ採番戦略: "sequential" または "timestamp"
branch_numbering: sequential

# git init 用のカスタムコミットメッセージ
init_commit_message: "[Spec Kit] Initial commit"

# コマンド単位の自動コミット設定（既定はすべて無効）
# 例: specify 後の自動コミットを有効化
auto_commit:
  default: false
  after_specify:
    enabled: true
    message: "[Spec Kit] Add specification"
```

## Installation

```bash
# 同梱の git 拡張をインストール（ネットワーク不要）
specify extension add git
```

## Disabling

```bash
# git 拡張を無効化（spec 作成はブランチ作成なしで継続）
specify extension disable git

# 再度有効化
specify extension enable git
```

## Graceful Degradation

Git 未インストール、または Git リポジトリでない場合:
- `specs/` 配下の spec ディレクトリ作成は継続
- ブランチ作成は警告付きでスキップ
- ブランチ検証は警告付きでスキップ
- リモート検出は空結果を返す

## Scripts

この拡張はクロスプラットフォームスクリプトを同梱:

- `scripts/bash/create-new-feature.sh` — Bash 実装
- `scripts/bash/git-common.sh` — 共有 Git ユーティリティ（Bash）
- `scripts/powershell/create-new-feature.ps1` — PowerShell 実装
- `scripts/powershell/git-common.ps1` — 共有 Git ユーティリティ（PowerShell）
