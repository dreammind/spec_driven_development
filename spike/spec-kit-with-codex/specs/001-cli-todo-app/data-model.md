# Data Model: CLI版TODOタスク管理

## Entity: Task

- id: string (UUID形式, 必須, 一意)
- title: string (必須, trim後1文字以上)
- is_completed: boolean (必須, 既定 false)
- is_archived: boolean (必須, 既定 false)
- created_at: string (ISO-8601日時, 必須)

## Entity: TaskCollection

- tasks: Task[]
- 役割: タスクの作成・取得・状態更新・アーカイブ・復元の操作対象

## Validation Rules

- `id` はUUIDとして妥当であること。
- `title` は空文字/空白のみを禁止する。
- 既存でない `id` を指定した操作は失敗する。
- `is_archived=true` のタスクに対する再アーカイブは失敗する。

## Pydantic Model Rules

- `Task` は `pydantic.BaseModel` で定義し、型注釈を必須とする。
- `id` はUUID型として扱い、文字列入力時はパース失敗を検証エラーにする。
- `title` は前後空白を除去した上で最小文字数1を満たす。
- `created_at` はISO-8601互換の日時として検証し、永続化時は一貫した形式で出力する。

## State Transitions

- 新規追加: `is_completed=false`, `is_archived=false`
- 完了化: `false/false -> true/false`
- 未完了化: `true/false -> false/false`
- アーカイブ: `*/false -> */true`
- 復元: `*/true -> false/false`（復元時は常に未完了）

## Query/View Rules

- 既定一覧: `is_archived=false AND is_completed=false`
- 完了含む一覧: `is_archived=false` を満たす全タスク
- アーカイブ一覧（必要時）: `is_archived=true`
