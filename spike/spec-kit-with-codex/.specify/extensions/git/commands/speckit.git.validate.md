---
description: "現在のブランチが機能ブランチ命名規約に従っているか検証する"
---

# 機能ブランチ検証

現在の Git ブランチ名が期待される機能ブランチ規約に一致するか検証します。

## Prerequisites

- `git rev-parse --is-inside-work-tree 2>/dev/null` で Git 利用可否を確認
- Git が利用できない場合は警告を出し、検証をスキップ:
  ```
  [specify] Warning: Git repository not detected; skipped branch validation
  ```

## Validation Rules

現在のブランチ名を取得:

```bash
git rev-parse --abbrev-ref HEAD
```

ブランチ名は次のいずれかに一致する必要があります:

1. **Sequential**: `^[0-9]{3,}-` （例: `001-feature-name`, `042-fix-bug`, `1000-big-feature`）
2. **Timestamp**: `^[0-9]{8}-[0-9]{6}-` （例: `20260319-143022-feature-name`）

## Execution

機能ブランチ上（いずれかのパターンに一致）の場合:
- 出力: `✓ On feature branch: <branch-name>`
- `specs/` 配下に対応する spec ディレクトリがあるか確認:
  - Sequential: 数値プレフィックスに一致する `specs/<prefix>-*`
  - Timestamp: `YYYYMMDD-HHMMSS` プレフィックスに一致する `specs/<prefix>-*`
- spec ディレクトリがある場合: `✓ Spec directory found: <path>`
- ない場合: `⚠ No spec directory found for prefix <prefix>`

機能ブランチ上でない場合:
- 出力: `✗ Not on a feature branch. Current branch: <branch-name>`
- 出力: `Feature branches should be named like: 001-feature-name or 20260319-143022-feature-name`

## Graceful Degradation

Git 未インストール、または Git リポジトリでない場合:
- フォールバックとして `SPECIFY_FEATURE` 環境変数を確認
- 値があれば同じ命名規則で検証
- 値がなければ警告を出して検証スキップ
