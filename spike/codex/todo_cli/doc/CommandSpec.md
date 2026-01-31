# コマンド仕様表

## 共通
- IDはタスクの一意識別子
- 日付形式: YYYY-MM-DD
- 優先度: high / medium / low
- カテゴリは複数指定可（`,`区切り）
- 実行形式: `pipenv run python -m todo_cli.cli <command> ...`

## add
- 目的: タスクを追加する
- 形式: `pipenv run python -m todo_cli.cli add <title> [--description <text>] --priority <high|medium|low> [--due <YYYY-MM-DD>] [--category <c1,c2,...>]`
- 出力例:
  - `Added task: 12 "Write spec"`

## list
- 目的: タスク一覧を表示する
- 形式: `pipenv run python -m todo_cli.cli list [--status <all|open|done>] [--priority <high|medium|low>] [--category <name>] [--sort <due|priority|created>] [--overdue]`
- 出力例:
  - `12 [open] (high) 2026-02-05 Write spec #work`

## done
- 目的: タスクを完了にする
- 形式: `pipenv run python -m todo_cli.cli done <id>`
- 出力例:
  - `Marked done: 12`

## undo
- 目的: 完了済みタスクを未完了に戻す
- 形式: `pipenv run python -m todo_cli.cli undo <id>`
- 出力例:
  - `Marked open: 12`

## delete
- 目的: タスクを削除する
- 形式: `pipenv run python -m todo_cli.cli delete <id>`
- 出力例:
  - `Deleted: 12`

## edit
- 目的: タスクを編集する
- 形式: `pipenv run python -m todo_cli.cli edit <id> [--title <text>] [--description <text>] [--priority <high|medium|low>] [--due <YYYY-MM-DD>] [--category <c1,c2,...>]`
- 出力例:
  - `Updated: 12`

## search
- 目的: キーワード検索する
- 形式: `pipenv run python -m todo_cli.cli search <keyword>`
- 出力例:
  - `12 [open] (high) 2026-02-05 Write spec #work`
