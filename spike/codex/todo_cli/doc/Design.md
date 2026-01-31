# 設計方針

## CLI構成
- サブコマンド方式（add/list/done/undo/delete/edit/search 等）で一貫性を保つ。

## データモデル
- Task: id, title, description, priority, due_date, categories, status, created_at, completed_at

## ストレージ
- `tasks.json` を読み書きし、単一ファイルで管理する。

## バリデーション
- 入力値の必須/形式/範囲チェックを厳密に行う。

## 並び替え/絞り込み
- フィルタ→ソート→表示の順にパイプライン化する。

## テスト
- ユースケース中心（CRUD、検索、絞り込み、ソート、境界値）。
