# タスクのデータスキーマ

## Task
- id: string
  - 一意識別子
- title: string
  - 必須
- description: string | null
  - 任意
- priority: "high" | "medium" | "low"
  - 必須
- due_date: string | null
  - 日付形式: YYYY-MM-DD
- categories: string[]
  - 任意（複数可）
- status: "open" | "done"
  - 既定: open
- created_at: string
  - 日時（ISO 8601）
- completed_at: string | null
  - 日時（ISO 8601）

## 保存形式
- `tasks.json` に保存する。

## ルール
- title は空文字不可
- categories は重複を許可しない
- categories は大小文字を区別しない（保存時は小文字に正規化）
- due_date が指定される場合、過去日付も許容する
- completed_at は status が done の場合のみセットされる
- status が open に戻る場合、completed_at は null に戻る
