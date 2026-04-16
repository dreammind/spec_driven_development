# Data Model: タスクタイトル編集機能

## Entity: Task (existing, updated rules)

- id: UUID（不変）
- title: string（編集対象、trim後1〜255文字）
- is_completed: boolean（編集対象外）
- is_archived: boolean（編集対象外）
- created_at: datetime（編集対象外）

## Entity: EditRequest

- task_id: string（UUID形式）
- new_title: string（trim後1〜255文字）

## Validation Rules

- `task_id` はUUIDとして妥当であること。
- `new_title` は空白のみ禁止、最大255文字。
- 存在しない `task_id` の編集は失敗。
- `is_archived=true` のタスク編集は失敗（復元後のみ可）。
- 編集成功時も `id`, `is_completed`, `is_archived`, `created_at` は不変。

## State Transitions

- 編集成功: `title` のみ更新、他属性不変。
- 編集失敗（不正ID/未存在/空文字/255文字超過/アーカイブ済み）: タスク全属性不変。

## Query/View Rules

- 一覧表示は既存仕様に従う（既定は未完了かつ非アーカイブ）。
- 編集反映後、一覧表示時に更新済みタイトルが表示される。
