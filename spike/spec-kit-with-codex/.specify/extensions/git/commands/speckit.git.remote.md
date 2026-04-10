---
description: "GitHub 連携用に Git リモート URL を検出する"
---

# Git リモート URL 検出

GitHub サービス（例: Issue 作成）連携のため、Git リモート URL を検出します。

## Prerequisites

- `git rev-parse --is-inside-work-tree 2>/dev/null` で Git 利用可否を確認
- Git が利用できない場合は警告を出し、空結果を返す:
  ```
  [specify] Warning: Git repository not detected; cannot determine remote URL
  ```

## Execution

リモート URL 取得のため、次を実行:

```bash
git config --get remote.origin.url
```

## Output

リモート URL を解析して次を判定:

1. **Repository owner**: URL から抽出（例: `https://github.com/github/spec-kit.git` の `github`）
2. **Repository name**: URL から抽出（例: `https://github.com/github/spec-kit.git` の `spec-kit`）
3. **Is GitHub**: リモートが GitHub リポジトリかどうか

対応 URL 形式:
- HTTPS: `https://github.com/<owner>/<repo>.git`
- SSH: `git@github.com:<owner>/<repo>.git`

> [!CAUTION]
> リモート URL が実際に github.com を指す場合のみ GitHub リポジトリとして報告すること。
> 形式が似ていても、条件に一致しなければ GitHub と見なしてはいけません。

## Graceful Degradation

Git 未インストール、Git リポジトリ外、またはリモート未設定の場合:
- 空結果を返す
- エラーにはしない（他ワークフローが Git リモート情報なしで継続できるようにする）
