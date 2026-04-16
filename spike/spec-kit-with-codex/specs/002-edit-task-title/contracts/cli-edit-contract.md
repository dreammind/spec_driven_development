# CLI Contract: Task Title Edit

## Command Overview

| Command | Purpose | Required Args | Success Output | Failure Output |
|--------|---------|---------------|----------------|----------------|
| `todo edit` | タスクタイトルを更新 | `--id <uuid> --title <text>` | 更新済みIDと新タイトルを表示 | 入力エラー/未存在エラー/編集不可エラー |

## Input Contract

- `--id` はUUID形式であること。
- `--title` はtrim後1〜255文字。
- 未定義コマンド・不足引数はヘルプとエラーを返す。

## Output Contract

- 正常終了: 終了コード `0`
- 契約違反（不正ID、空タイトル、255文字超過、未存在ID、アーカイブ済み編集）: 終了コード `2`
- 予期しない実行時エラー: 終了コード `1`

## Behavioral Guarantees

- 編集成功時、対象タスクのタイトルのみ更新される。
- 編集失敗時、既存データは変更されない。
- アーカイブ済みタスクへの編集要求では「復元後に編集」を案内するエラーを返す。
