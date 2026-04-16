# CLI Contract: TODO App

## Command Overview

| Command | Purpose | Required Args | Success Output | Failure Output |
|--------|---------|---------------|----------------|----------------|
| `todo add` | タスク追加 | `--title <text>` | 追加IDとタイトルを表示 | 入力エラーメッセージ |
| `todo list` | タスク一覧表示 | なし | 既定で未完了タスク一覧 | なし（空状態メッセージ） |
| `todo list --all-active` | 完了済み含む一覧 | なし | 未アーカイブの全タスク一覧 | なし |
| `todo complete` | タスク完了化 | `--id <uuid>` | 更新結果を表示 | ID不正/未存在エラー |
| `todo reopen` | タスク未完了化 | `--id <uuid>` | 更新結果を表示 | ID不正/未存在エラー |
| `todo archive` | タスクをアーカイブ | `--id <uuid>` | アーカイブ完了を表示 | ID不正/未存在/再アーカイブエラー |
| `todo restore` | アーカイブ復元 | `--id <uuid>` | 復元完了（未完了化）を表示 | ID不正/未存在/非アーカイブエラー |

## Input Contract

- すべての `--id` はUUID文字列であること。
- `todo add --title` はtrim後1文字以上。
- 未定義コマンド/不足引数はヘルプとエラー文を返す。

## Output Contract

- 正常終了時の終了コード: `0`
- 契約違反（入力不正・未存在ID等）: `2`
- 予期しない実行時エラー: `1`

## Behavioral Guarantees

- `todo list` は既定で未完了かつ非アーカイブのみ表示。
- `todo archive` 実行後、対象タスクは既定一覧から除外される。
- `todo restore` 実行後、対象タスクは常に未完了で既定一覧に戻る。
